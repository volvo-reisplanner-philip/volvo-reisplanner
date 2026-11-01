"""Maak compacte NDW Type 2-catalogus voor Volvo Reisplanner.

NDW-tarieven zijn niet noodzakelijk Shuttel-eindprijzen. Status kan verouderd
zijn. Gemeentelijke parkeerkosten en betalingen worden niet afgehandeld.
"""
import gzip
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict
import shutil
import math

LOCATIES_URL = "https://opendata.ndw.nu/charging_point_locations_ocpi.json.gz"
TARIEVEN_URL = "https://opendata.ndw.nu/charging_point_tariffs_ocpi.json.gz"
UITVOER = Path("data/laadprijzen.json")
MAX_BYTES = 95_000_000  # Ruim onder GitHub's limiet van 100 MB.
TEGELS_MAP = Path("data/laadpunten")
TEGEL_GROOTTE = 0.25  # graden; ook de aangrenzende tegels doorzoeken voor 500 meter


def download_ndw(url):
    request = urllib.request.Request(url, headers={"User-Agent": "VolvoReisplanner/1.0"})
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.loads(gzip.decompress(response.read()).decode("utf-8"))


def tekst(waarde):
    return str(waarde) if waarde is not None else ""


def prijsopbouw_compact(elementen):
    """Behoud prijscomponenten en alle niet-lege beperkingen."""
    uitvoer = []
    for element in elementen or []:
        componenten = [
            {"type": c.get("type"), "prijs": c.get("price"),
             "btw": c.get("vat"), "stap": c.get("step_size")}
            for c in element.get("price_components") or []
        ]
        if not componenten:
            continue
        voorwaarden = {k: v for k, v in (element.get("restrictions") or {}).items()
                       if v is not None}
        uitvoer.append({"componenten": componenten, "voorwaarden": voorwaarden})
    return uitvoer


def main():
    print("NDW-laadlocaties downloaden...")
    locaties = download_ndw(LOCATIES_URL)
    print("NDW-laadtarieven downloaden...")
    tarieven = download_ndw(TARIEVEN_URL)
    print(f"Ontvangen: {len(locaties)} locaties en {len(tarieven)} tarieven")

    # Tarieven slechts één keer opslaan, niet opnieuw bij iedere laadpaal.
    index = {}
    for tarief in tarieven:
        sleutel = (tekst(tarief.get("country_code")),
                  tekst(tarief.get("party_id")), tekst(tarief.get("id")))
        index.setdefault(sleutel, []).append(tarief)

    gebruikte_tarieven = {}
    laadpalen = []
    aansluitingen_totaal = 0
    onduidelijk = 0

    for locatie in locaties:
        if locatie.get("country_code") != "NL":
            continue
        aanbieder = tekst(locatie.get("party_id"))
        aansluitingen = []
        for evse in locatie.get("evses") or []:
            for connector in evse.get("connectors") or []:
                if connector.get("standard") != "IEC_62196_T2":
                    continue
                refs = []
                onbekend = []
                for tarief_id in connector.get("tariff_ids") or []:
                    sleutel = ("NL", aanbieder, tekst(tarief_id))
                    kandidaten = index.get(sleutel, [])
                    if len(kandidaten) != 1:
                        onbekend.append(tekst(tarief_id))
                        onduidelijk += 1
                        continue
                    ref = "|".join(sleutel)
                    if ref not in gebruikte_tarieven:
                        tarief = kandidaten[0]
                        gebruikte_tarieven[ref] = {
                            "valuta": tarief.get("currency"),
                            "prijsopbouw": prijsopbouw_compact(tarief.get("elements")),
                            "geldig_vanaf": tarief.get("start_date_time"),
                            "geldig_tot": tarief.get("end_date_time"),
                        }
                    refs.append(ref)
                aansluitingen.append({
                    "id": evse.get("evse_id"),
                    "status": evse.get("status"),
                    "bijgewerkt": evse.get("last_updated"),
                    "tarieven": refs,
                    "onbekende_tarieven": onbekend,
                })
                aansluitingen_totaal += 1
        if aansluitingen:
            coord = locatie.get("coordinates") or {}
            laadpalen.append({
                "id": locatie.get("id"),
                "naam": locatie.get("name"),
                "plaats": locatie.get("city"),
                "adres": locatie.get("address"),
                "lat": coord.get("latitude"),
                "lon": coord.get("longitude"),
                "aansluitingen": aansluitingen,
            })

    resultaat = {
        "bijgewerkt": datetime.now(timezone.utc).isoformat(),
        "bron": "NDW Open Data (OCPI)",
        "testbestand": False,
        "opmerking": "NDW-prijzen zijn geen gegarandeerde Shuttel-prijzen; status kan verouderd zijn; gemeentelijke parkeerkosten en betalingen ontbreken.",
        "tarieven": gebruikte_tarieven,
        "laadpalen": laadpalen,
    }
    UITVOER.parent.mkdir(parents=True, exist_ok=True)
    inhoud = json.dumps(resultaat, ensure_ascii=False, separators=(",", ":"))
    grootte = len(inhoud.encode("utf-8"))
    print(f"Nederlandse Type 2-locaties: {len(laadpalen)}")
    print(f"Type 2-aansluitingen: {aansluitingen_totaal}")
    print(f"Unieke gebruikte tarieven: {len(gebruikte_tarieven)}")
    print(f"Onduidelijke tariefverwijzingen: {onduidelijk}")
    print(f"Uitvoer: {grootte / 1_000_000:.2f} MB")
    if grootte >= MAX_BYTES:
        raise RuntimeError("Catalogus is nog te groot voor GitHub. Geen bestand geschreven; opsplitsen is nodig.")
    UITVOER.write_text(inhoud, encoding="utf-8")
    print(f"Opgeslagen: {UITVOER}")

    # Kleine geografische deelbestanden voor snel zoeken op een iPhone.
    # Iedere tegel bevat alleen de tarieven die de laadpalen in die tegel gebruiken.
    tegels = defaultdict(list)
    overgeslagen = 0
    for paal in laadpalen:
        try:
            lat, lon = float(paal["lat"]), float(paal["lon"])
            if not (math.isfinite(lat) and math.isfinite(lon)):
                raise ValueError("Ongeldige coördinaten")
            sleutel = (math.floor(lat / TEGEL_GROOTTE), math.floor(lon / TEGEL_GROOTTE))
            tegels[sleutel].append(paal)
        except (TypeError, ValueError):
            overgeslagen += 1

    # Pas opruimen nadat de NDW-download en de volledige catalogus zijn gelukt.
    if TEGELS_MAP.exists():
        shutil.rmtree(TEGELS_MAP)
    TEGELS_MAP.mkdir(parents=True, exist_ok=True)
    register = {}
    for (lat_index, lon_index), palen in sorted(tegels.items()):
        naam = f"tegel_{lat_index}_{lon_index}.json"
        gebruikte_refs = {
            ref
            for paal in palen
            for aansluiting in paal["aansluitingen"]
            for ref in aansluiting["tarieven"]
        }
        deel = {
            "bijgewerkt": resultaat["bijgewerkt"],
            "bron": resultaat["bron"],
            "laadpalen": palen,
            "tarieven": {ref: gebruikte_tarieven[ref] for ref in sorted(gebruikte_refs)},
        }
        pad = TEGELS_MAP / naam
        pad.write_text(json.dumps(deel, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        if pad.stat().st_size >= MAX_BYTES:
            raise RuntimeError(f"Geografisch deelbestand te groot: {pad}")
        register[f"{lat_index}_{lon_index}"] = {"bestand": naam, "aantal": len(palen)}

    manifest = {
        "bijgewerkt": resultaat["bijgewerkt"],
        "bron": resultaat["bron"],
        "tegel_grootte_graden": TEGEL_GROOTTE,
        "tegels": register,
        "opmerking": resultaat["opmerking"],
    }
    (TEGELS_MAP / "index.json").write_text(
        json.dumps(manifest, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    print(f"Geografische deelbestanden: {len(register)}; locaties zonder bruikbare coördinaten: {overgeslagen}")
    print(f"Manifest: {TEGELS_MAP / 'index.json'}")


if __name__ == "__main__":
    main()
