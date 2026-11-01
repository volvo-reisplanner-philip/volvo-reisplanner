import gzip
import json
import urllib.request

# Openbare NDW-gegevens
LOCATIES_URL = "https://opendata.ndw.nu/charging_point_locations_ocpi.json.gz"
TARIEVEN_URL = "https://opendata.ndw.nu/charging_point_tariffs_ocpi.json.gz"


def download_ndw(url):
    """Download en lees een gecomprimeerd NDW JSON-bestand."""
    with urllib.request.urlopen(url, timeout=120) as response:
        compressed = response.read()

    return json.loads(gzip.decompress(compressed).decode("utf-8"))
def main():
    print("NDW-laadlocaties downloaden...")
    locaties = download_ndw(LOCATIES_URL)

    print("NDW-laadtarieven downloaden...")
    tarieven = download_ndw(TARIEVEN_URL)

    print("Download geslaagd!")
    print("Type locatiegegevens:", type(locaties).__name__)
    print("Type tariefgegevens:", type(tarieven).__name__)
    print("Aantal locaties:", len(locaties))
    print("Aantal tarieven:", len(tarieven))
    from collections import Counter

    soorten = Counter()

    for tarief in tarieven:
        for element in tarief.get("elements", []):
            for onderdeel in element.get("price_components", []):
                soorten[onderdeel.get("type", "ONBEKEND")] += 1
    tarieven_met_parkeerkosten = 0

    for tarief in tarieven:
        heeft_parkeerkosten = any(
            onderdeel.get("type") == "PARKING_TIME"
            and float(onderdeel.get("price") or 0) > 0
            for element in tarief.get("elements", [])
            for onderdeel in element.get("price_components", [])
        )

        if heeft_parkeerkosten:
            tarieven_met_parkeerkosten += 1

    print(
        "Tarieven met positieve parkeertijdkosten:",
        tarieven_met_parkeerkosten
    )
    voorbeelden_parkeerkosten = []

    for tarief in tarieven:
        for element in tarief.get("elements", []):
            for onderdeel in element.get("price_components", []):
                if (
                    onderdeel.get("type") == "PARKING_TIME"
                    and float(onderdeel.get("price") or 0) > 0
                ):
                    voorbeelden_parkeerkosten.append({
                        "tarief_id": tarief.get("id"),
                        "prijs": onderdeel.get("price"),
                        "stapgrootte": onderdeel.get("step_size"),
                        "voorwaarden": element.get("restrictions")
                    })
                    break

        if len(voorbeelden_parkeerkosten) >= 5:
            break
    for tarief in tarieven:
        if tarief.get("id") == "508b9eea-b4e8-4bc1-b76f-e50a0d25e921":
            print("Valuta parkeertarief:", tarief.get("currency"))
            print("Volledige tariefopbouw:", tarief.get("elements"))
            break
    print("Voorbeelden parkeertijdtarieven:")
    for voorbeeld in voorbeelden_parkeerkosten:
        print(voorbeeld)
    from collections import Counter

    parkeerprijzen = Counter()

    for tarief in tarieven:
        for element in tarief.get("elements", []):
            for onderdeel in element.get("price_components", []):
                if onderdeel.get("type") == "PARKING_TIME":
                    prijs = float(onderdeel.get("price") or 0)
                    if prijs > 0:
                        parkeerprijzen[prijs] += 1

    print("Meest voorkomende positieve parkeertijdtarieven:")

    for prijs, aantal in parkeerprijzen.most_common(10):
        print(f"EUR {prijs:.2f}: {aantal} keer")    
    print("Overzicht prijscomponenten:")
    tarieven_met_startkosten = 0

    for tarief in tarieven:
        heeft_startkosten = any(
            onderdeel.get("type") == "FLAT"
            for element in tarief.get("elements", [])
            for onderdeel in element.get("price_components", [])
        )

        if heeft_startkosten:
            tarieven_met_startkosten += 1

    print("Tarieven met vaste kosten:", tarieven_met_startkosten)
    tarieven_met_positieve_startkosten = 0

    for tarief in tarieven:
        heeft_positieve_startkosten = any(
            onderdeel.get("type") == "FLAT"
            and float(onderdeel.get("price") or 0) > 0
            for element in tarief.get("elements", [])
            for onderdeel in element.get("price_components", [])
        )

        if heeft_positieve_startkosten:
            tarieven_met_positieve_startkosten += 1

    print(
        "Tarieven met positieve startkosten:",
        tarieven_met_positieve_startkosten
    )
    vaste_bedragen = []

    for tarief in tarieven:
        for element in tarief.get("elements", []):
            for onderdeel in element.get("price_components", []):
                if onderdeel.get("type") == "FLAT":
                    bedrag = float(onderdeel.get("price") or 0)
                    if bedrag > 0:
                        vaste_bedragen.append(bedrag)

    if vaste_bedragen:
        print("Laagste vaste kosten:", min(vaste_bedragen))
        print("Hoogste vaste kosten:", max(vaste_bedragen))
        print(
            "Gemiddelde vaste kosten:",
            round(sum(vaste_bedragen) / len(vaste_bedragen), 2)
        )
    for soort, aantal in soorten.most_common():
        print(f"{soort}: {aantal}")
    if locaties:
        print("Velden eerste locatie:", list(locaties[0].keys()))

    if tarieven:
        print("Velden eerste tarief:", list(tarieven[0].keys()))
    gezochte_tarief_id = "558604132"

    gevonden_tarief = next(
        (t for t in tarieven if str(t.get("id")) == gezochte_tarief_id),
        None
    )

    if gevonden_tarief:
        print("Gevonden tarief:", gevonden_tarief)
        for element in gevonden_tarief.get("elements", []):
            for onderdeel in element.get("price_components", []):
                print(
                    "Prijscomponent:",
                    onderdeel.get("type"),
                    "Prijs:", onderdeel.get("price"),
                    "BTW:", onderdeel.get("vat"),
                    "Stapgrootte:", onderdeel.get("step_size")
                )
    else:
        print("Tarief-ID niet gevonden:", gezochte_tarief_id)
    if locaties:
        eerste_locatie = locaties[0]
        print("Eerste locatie-ID:", eerste_locatie.get("id"))
        print("Aantal aansluitingen:", len(eerste_locatie.get("evses") or []))

        if eerste_locatie.get("evses"):
            eerste_evse = eerste_locatie["evses"][0]
            print("Velden eerste aansluiting:", list(eerste_evse.keys()))
            print("Eerste aansluiting:", eerste_evse)
            for connector in eerste_evse.get("connectors", []):
                print("Connector-ID:", connector.get("id"))
                print("Tarief-ID's:", connector.get("tariff_ids"))
                print("Connectorgegevens:", connector)
def schrijf_testbestand():
    from pathlib import Path
    from datetime import datetime, timezone

    locaties = download_ndw(LOCATIES_URL)

    resultaat = {
        "bijgewerkt": datetime.now(timezone.utc).isoformat(),
        "bron": "NDW Open Data",
        "laadpalen": []
    }

       for locatie in locaties[:5]:
        aansluitingen = []

        for evse in locatie.get("evses") or []:
            for connector in evse.get("connectors") or []:
                if connector.get("standard") == "IEC_62196_T2":
                    aansluitingen.append({
                        "evse_id": evse.get("evse_id"),
                        "status": evse.get("status"),
                        "type": connector.get("standard"),
                        "tarief_ids": connector.get("tariff_ids") or []
                    })

        resultaat["laadpalen"].append({
            "id": locatie.get("id"),
            "naam": locatie.get("name"),
            "plaats": locatie.get("city"),
            "adres": locatie.get("address"),
            "coordinaten": locatie.get("coordinates"),
            "aansluitingen": aansluitingen
        })

    uitvoerbestand = Path("data/laadprijzen.json")
    uitvoerbestand.parent.mkdir(parents=True, exist_ok=True)

    uitvoerbestand.write_text(
        json.dumps(resultaat, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("Testbestand aangemaakt met 5 laadlocaties.")
if __name__ == "__main__":
    main()
    schrijf_testbestand()
