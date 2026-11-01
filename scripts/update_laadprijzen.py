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
if __name__ == "__main__":
    main()
