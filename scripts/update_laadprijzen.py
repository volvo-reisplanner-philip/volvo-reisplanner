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


if __name__ == "__main__":
    main()
