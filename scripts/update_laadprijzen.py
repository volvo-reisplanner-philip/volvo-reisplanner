"""Maak een compacte Nederlandse Type 2-laadlocatiecatalogus uit NDW OCPI.

Let op: NDW CPO-tarieven zijn geen gegarandeerde Shuttel-eindprijzen.
De status is een momentopname; parkeerbelasting en betaling worden niet geregeld.
"""

import gzip
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

LOCATIES_URL = "https://opendata.ndw.nu/charging_point_locations_ocpi.json.gz"
TARIEVEN_URL = "https://opendata.ndw.nu/charging_point_tariffs_ocpi.json.gz"
UITVOER = Path("data/laadprijzen.json")


def download_ndw(url):
    request = urllib.request.Request(url, headers={"User-Agent": "VolvoReisplanner/1.0"})
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.loads(gzip.decompress(response.read()).decode("utf-8"))


def tekst(value):
    return str(value) if value is not None else ""


def main():
    print("NDW-laadlocaties downloaden...")
    locaties = download_ndw(LOCATIES_URL)
    print("NDW-laadtarieven downloaden...")
    tarieven = download_ndw(TARIEVEN_URL)
    print(f"Ontvangen: {len(locaties)} locaties, {len(tarieven)} tarieven")

    # Unieke koppeling op land, aanbieder en tarief-ID. Dubbele sleutels
    # worden niet geraden: ze blijven als onduidelijk gemarkeerd.
    tarief_index = {}
    for tarief in tarieven:
        key = (tekst(tarief.get("country_code")), tekst(tarief.get("party_id")), tekst(tarief.get("id")))
        tarief_index.setdefault(key, []).append(tarief)

    resultaat = {
        "bijgewerkt": datetime.now(timezone.utc).isoformat(),
        "bron": "NDW Open Data (OCPI)",
        "testbestand": False,
        "opmerking": (
            "NDW-tarieven zijn niet noodzakelijk Shuttel-eindprijzen. "
            "Beschikbaarheid is niet gegarandeerd actueel. "
            "Gemeentelijke parkeerkosten en directe betaling worden niet aangeboden."
        ),
        "laadpalen": [],
    }
    onduidelijke_koppelingen = 0
    aansluitingen_totaal = 0

    for locatie in locaties:
        if locatie.get("country_code") != "NL":
            continue
        land = tekst(locatie.get("country_code"))
        aanbieder = tekst(locatie.get("party_id"))
        aansluitingen = []

        for evse in locatie.get("evses") or []:
            for connector in evse.get("connectors") or []:
                if connector.get("standard") != "IEC_62196_T2":
                    continue

                gekoppelde_tarieven = []
                onduidelijke_tarief_ids = []
                for tarief_id in connector.get("tariff_ids") or []:
                    kandidaten = tarief_index.get((land, aanbieder, tekst(tarief_id)), [])
                    if len(kandidaten) == 1:
                        tarief = kandidaten[0]
                        gekoppelde_tarieven.append({
                            "id": tarief.get("id"),
                            "aanbieder": tarief.get("party_id"),
                            "landcode": tarief.get("country_code"),
                            "valuta": tarief.get("currency"),
                            "prijsopbouw": tarief.get("elements") or [],
                        })
                    else:
                        onduidelijke_tarief_ids.append(tekst(tarief_id))
                        onduidelijke_koppelingen += 1

                aansluitingen.append({
                    "evse_id": evse.get("evse_id"),
                    "status": evse.get("status"),
                    "status_bijgewerkt": evse.get("last_updated"),
                    "type": connector.get("standard"),
                    "tarief_ids": connector.get("tariff_ids") or [],
                    "tarieven": gekoppelde_tarieven,
                    "onduidelijke_tarief_ids": onduidelijke_tarief_ids,
                })
                aansluitingen_totaal += 1

        if aansluitingen:
            resultaat["laadpalen"].append({
                "id": locatie.get("id"),
                "naam": locatie.get("name"),
                "plaats": locatie.get("city"),
                "adres": locatie.get("address"),
                "coordinaten": locatie.get("coordinates"),
                "aansluitingen": aansluitingen,
            })

    UITVOER.parent.mkdir(parents=True, exist_ok=True)
    UITVOER.write_text(json.dumps(resultaat, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Opgeslagen: {len(resultaat['laadpalen'])} Nederlandse Type 2-locaties")
    print(f"Type 2-aansluitingen: {aansluitingen_totaal}")
    print(f"Niet eenduidig gekoppelde tariefverwijzingen: {onduidelijke_koppelingen}")
    print(f"Bestand: {UITVOER} ({UITVOER.stat().st_size / 1024 / 1024:.1f} MiB)")


if __name__ == "__main__":
    main()
