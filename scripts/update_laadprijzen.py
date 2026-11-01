"""Maak een testbestand met vijf NDW-laadlocaties en gekoppelde OCPI-tarieven.

Dit script wijzigt uitsluitend data/laadprijzen.json, niet de reisplanner zelf.
"""

import gzip
import json
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

LOCATIES_URL = "https://opendata.ndw.nu/charging_point_locations_ocpi.json.gz"
TARIEVEN_URL = "https://opendata.ndw.nu/charging_point_tariffs_ocpi.json.gz"
UITVOERBESTAND = Path("data/laadprijzen.json")
AANTAL_TESTLOCATIES = 5


def download_ndw(url):
    """Download een gecomprimeerd NDW-bestand en lees de JSON-inhoud."""
    request = urllib.request.Request(url, headers={"User-Agent": "VolvoReisplanner/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        inhoud = response.read()
    gegevens = json.loads(gzip.decompress(inhoud).decode("utf-8"))
    if not isinstance(gegevens, list):
        raise ValueError("Onverwacht NDW-formaat: een lijst werd verwacht")
    return gegevens


def main():
    print("NDW-laadlocaties downloaden...")
    locaties = download_ndw(LOCATIES_URL)
    print("NDW-laadtarieven downloaden...")
    tarieven = download_ndw(TARIEVEN_URL)
    print(f"Aantal locaties: {len(locaties)}")
    print(f"Aantal tarieven: {len(tarieven)}")

    # Een tarief-ID kan bij meer dan één aanbieder voorkomen. Bewaar alle
    # kandidaten en koppel uitsluitend automatisch wanneer de ID uniek is.
    tarieven_op_id = defaultdict(list)
    for tarief in tarieven:
        tarief_id = tarief.get("id")
        if tarief_id is not None:
            tarieven_op_id[str(tarief_id)].append(tarief)

    dubbelzinnige_ids = sum(len(kandidaten) > 1 for kandidaten in tarieven_op_id.values())
    print(f"Verschillende tarief-ID's: {len(tarieven_op_id)}")
    print(f"Tarief-ID's met meerdere kandidaten: {dubbelzinnige_ids}")

    resultaat = {
        "bijgewerkt": datetime.now(timezone.utc).isoformat(),
        "bron": "NDW Open Data (OCPI)",
        "testbestand": True,
        "opmerking": (
            "NDW-tarieven zijn niet noodzakelijk de uiteindelijke Shuttel-prijzen. "
            "Statusgegevens kunnen verouderd zijn; parkeerkosten zijn niet berekend."
        ),
        "laadpalen": [],
    }

    telling = Counter()
    for locatie in locaties[:AANTAL_TESTLOCATIES]:
        aansluitingen = []
        for evse in locatie.get("evses") or []:
            for connector in evse.get("connectors") or []:
                if connector.get("standard") != "IEC_62196_T2":
                    continue

                gekoppelde_tarieven = []
                onduidelijke_tarief_ids = []
                for tarief_id in connector.get("tariff_ids") or []:
                    kandidaten = tarieven_op_id.get(str(tarief_id), [])
                    if len(kandidaten) == 1:
                        tarief = kandidaten[0]
                        gekoppelde_tarieven.append({
                            "id": tarief.get("id"),
                            "aanbieder": tarief.get("party_id"),
                            "landcode": tarief.get("country_code"),
                            "valuta": tarief.get("currency"),
                            "prijsopbouw": tarief.get("elements"),
                        })
                        telling["gekoppeld"] += 1
                    elif len(kandidaten) > 1:
                        onduidelijke_tarief_ids.append(str(tarief_id))
                        telling["dubbelzinnig"] += 1
                    else:
                        telling["niet_gevonden"] += 1

                aansluitingen.append({
                    "evse_id": evse.get("evse_id"),
                    "status": evse.get("status"),
                    "status_bijgewerkt": evse.get("last_updated"),
                    "type": connector.get("standard"),
                    "tarief_ids": connector.get("tariff_ids") or [],
                    "tarieven": gekoppelde_tarieven,
                    "onduidelijke_tarief_ids": onduidelijke_tarief_ids,
                })
                telling["type2"] += 1

        resultaat["laadpalen"].append({
            "id": locatie.get("id"),
            "naam": locatie.get("name"),
            "plaats": locatie.get("city"),
            "adres": locatie.get("address"),
            "coordinaten": locatie.get("coordinates"),
            "aansluitingen": aansluitingen,
        })

    UITVOERBESTAND.parent.mkdir(parents=True, exist_ok=True)
    UITVOERBESTAND.write_text(
        json.dumps(resultaat, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Testbestand opgeslagen: {UITVOERBESTAND}")
    print(f"Testlocaties: {len(resultaat['laadpalen'])}")
    print(f"Type 2-aansluitingen: {telling['type2']}")
    print(f"Uniek gekoppelde tarieven: {telling['gekoppeld']}")
    print(f"Dubbelzinnige tariefverwijzingen: {telling['dubbelzinnig']}")
    print(f"Niet gevonden tariefverwijzingen: {telling['niet_gevonden']}")


if __name__ == "__main__":
    main()
