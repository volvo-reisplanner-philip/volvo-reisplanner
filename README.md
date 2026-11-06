## Starten op de Mac in Chrome — nieuwste versie

Dubbelklik in deze map op **Start Volvo Reisplanner.command**. Het startprogramma opent Google Chrome op de vaste lokale website `http://127.0.0.1:8788/`. Laat Terminal open staan zolang je de planner gebruikt. Stoppen kan met Ctrl+C. Open niet langer een los index.html-bestand voor dagelijks gebruik.

Microfoon onthouden: klik in Chrome links van het webadres op Sitegegevens → Site-instellingen → Microfoon → **Toestaan**. Als Chrome een keuze toont, kies **Toestaan tijdens bezoek aan de site**, niet **Deze keer toestaan**. Dit is een browserinstelling; de app kan die niet zelf afdwingen. Toestemming kan door Chrome later vervallen, bijvoorbeeld na lange inactiviteit. De microfoon start uitsluitend wanneer je op de microfoonknop klikt. Bron: https://support.google.com/chrome/answer/2693767

Op de vaste lokale website moet je mogelijk je bestaande Google-browsersleutel opnieuw zelf invoeren. Als die op websites is beperkt, voeg dan alleen deze lokale website toe aan de toegestane websites, zonder bestaande productiebeperkingen te verwijderen. Lokale opslag en microfoontoestemming zijn gebonden aan de browser en website. De live website en sleutels zijn niet gewijzigd.

Het oorspronkelijke Google Maps-keuzemenu is weer direct zichtbaar bij vertrek en bestemming; de gewone resultatenlijst blijft als alternatief beschikbaar. Typ of dicteer straat, huisnummer en plaats; wacht kort of klik **Zoek adres**, en kies een resultaat. Het oorspronkelijke Google-keuzemenu staat boven het extra zoekveld en is niet ingeklapt. Google geeft slechts een beperkte verzameling overeenkomsten terug: als het juiste adres er niet bij staat, verfijn de tekst. Er is geen oneindige lijst met extra adressen door verder te scrollen.

# Volvo Reisplanner — complete lokale oplevering

Gebaseerd op de bestaande repository, commit `6713a447004512328d70e672f3c0bfadd3536b68` van 6 november 2026. De live repository is niet gewijzigd. De bestaande vormgeving, tabs, standaardwaarden, opslagcodes, dicteerfunctie, adresboek, routeberekening, historische Shuttel-informatie en eigen laadpaalwaarnemingen zijn behouden in de bron. De afzonderlijke `/mnt/data/Volvo_Reisplanner_NDW_nieuw.html` was niet beschikbaar. In de opgehaalde chat staat geen volledige oudere planning; de expliciete eisen uit de opdracht vormen daarom de aanvullende scope.

## Zelf openen

1. Pak het ZIP-bestand uit.
2. Open Terminal in de uitgepakte map `volvo-reisplanner`.
3. Start `python3 -m http.server 8765 --bind 127.0.0.1`.
4. Open `http://127.0.0.1:8765` in je browser. Stop met Ctrl+C in Terminal.

Dubbelklikken op `index.html` is niet geschikt voor het ophalen van NDW-tegels. Voor gebruik op je iPhone publiceer je de bestanden via GitHub Pages zoals hieronder beschreven.

Zonder Google-sleutel werken handmatige afstanden, bereik, kosten en adresboek. Google Maps-links openen zonder API-sleutel. Automatische routes, adressuggesties en bevestigde loopafstanden vereisen je eigen correct ingestelde Google Maps-browsersleutel. Vul die alleen zelf in onder **Meer**, nooit in broncode, GitHub, ZIP of een chat. De app stuurt adressen en coördinaten naar Google wanneer je die diensten gebruikt.

## Aanpassing adreslijsten op Mac

De Google-adreslijsten hebben een maximale hoogte en eigen verticale scrollruimte via het gedocumenteerde `prediction-list`-onderdeel. Je kunt ook de pijltoetsen en Enter gebruiken. Als het Google-keuzemenu blijft vastlopen: typ of dicteer het adres in het extra zoekveld en klik op **Zoek adres zonder keuzemenu**. Kies daarna een resultaat in de gewone knoppenlijst. Deze alternatieve zoekactie gebruikt de bestaande Google Geocoder en verandert de adressen pas na jouw keuze. De Google-sleutel blijft lokaal opgeslagen.

De browsercontrole gebruikte voorbeeldresultaten; de reparatie is nog niet bevestigd in de Google-sessie van de gebruiker. Technische referentie: https://developers.google.com/maps/documentation/javascript/reference/places-widget#PlaceAutocompleteElement

## Nieuw: laden of benzine?

Onder **Kosten** verschijnt automatisch een advies met het geschatte verschil in euro's en de totale ritkosten met en zonder bijladen. Vul onder Route het verwachte extra elektrische bereik in en onder Laden het werkelijke laadvolume. Het advies rekent altijd de volledige laadsessie af, ook als de bestaande ritkostenmethode op alleen verbruikte energie staat. Start-/extra kosten uit Kosten tellen mee; bij een gekoppeld NDW-tarief zitten daarin ook de berekende tijdkosten. Bij handmatige tarieven moet je die extra kosten zelf invullen.

De benzinebesparing is begrensd door zowel de extra elektrische kilometers op de terugreis als de energie die je daadwerkelijk bijlaadt. Ongebruikte energie krijgt binnen deze vergelijking geen waarde; onbekende toeslagen blijven onzeker. Het advies gaat alleen over bijkomend openbaar laden op bestemming, niet over het vervangen van reeds aanwezige thuisstroom.

## Wat is aangevuld of gecorrigeerd?

- Nederlandse decimale komma in alle numerieke velden, ook op apparaten die komma's in numerieke HTML-velden anders verwerken.
- Terugroute openen en bestemming delen/kopiëren naast de bestaande heenroute.
- Adresboekselectie start opnieuw de automatische routeberekening. Oude routeantwoorden overschrijven geen intussen gewijzigde adressen.
- Bestaande methode voor ritkosten blijft de standaard. Optioneel betaal je de **volledige laadsessie**, inclusief energie die na de rit overblijft. Het laadvolume staat onder Laden; dit is bewust een afzonderlijke gebruikerskeuze en bepaalt niet automatisch de extra elektrische kilometers.
- Een overgenomen NDW-tarief schakelt de ritraming naar de volledige sessie. Volume, laadduur, aangesloten tijd en bijkomende kosten rekenen de gekoppelde prijs opnieuw door. Handmatig aanpassen van openbaar tarief of startkosten verbreekt de koppeling.
- Alle laadinstellingen blijven lokaal bewaard, naast de bestaande route-/kosteninstellingen. De Google-sleutel blijft onder zijn bestaande afzonderlijke lokale opslagcode.
- Top 3 op geschatte totale berekenbare sessiekosten, bij gelijke prijs de kortste loopafstand. Ouderdom van beschikbaarheid staat apart en verandert de prijsvolgorde niet.
- Alle gevonden locaties met niet vergelijkbare tarieven staan afzonderlijk; zij kunnen goedkoper zijn. De lijst is dus geen garantie van de absoluut drie goedkoopste locaties.
- Alleen bevestigde Google-looproutes **van laadpaal naar bestemming** van maximaal 500 meter worden aanbevolen. Een ontbrekende of mislukte looproute telt niet als bevestigd. Hemelsbrede afstand is alleen een voorselectie.
- ENERGY, FLAT, TIME en PARKING_TIME met btw-keuze en sessieafronding. PARKING_TIME betekent aangesloten tijd zonder laden. Totale aangesloten tijd moet minimaal de laadduur zijn.
- Vlakke tarieven zonder energiecomponent zijn berekenbaar. Onbekende valuta, profieltarieven, prijslimieten, ongeldige geldigheid, meerdere tariefkeuzes per aansluiting en niet ondersteunde voorwaarden blijven onbekend.
- De NDW-verwerker behoudt nu ook tarieftype/prijslimieten en filtert expliciet AC Type 2. Onbruikbare Nederlandse coördinaten komen niet meer in de tegels.
- Bij uitval van het prijsbestand kunnen rechtstreeks gevonden locaties met onbekende prijs verschijnen. Bij uitval van rechtstreekse NDW-status wordt de momentopname nadrukkelijk als oud/onbevestigd aangeduid.
- Waarschuwingen voor onbekende Shuttel-prijzen/acceptatie en niet geverifieerd gemeentelijk parkeergeld zijn direct zichtbaar.
- Afdrukken neemt alle tabbladen mee. De API-sleutelinvoer wordt na verbinden geleegd, zoals in de bestaande app.

## Naar de Volvo

Open de bestemming in Google Maps. Bij een ondersteunde auto/account kan daar een functie om naar de auto te sturen beschikbaar zijn. De app doet geen directe Volvo-accountaanmelding en beweert niet dat een bestemming door de auto is ontvangen.

Voor Sensus Navigation beschrijft Volvo het zoeken van de bestemming en **Send to car** in de Volvo Cars-app. Delen/kopiëren helpt om het adres over te nemen. Ondersteuning hangt af van model, software en diensten. Er zijn geen onbevestigde Volvo-appkoppelingen toegevoegd.

Bron: https://www.volvocars.com/uk/support/topic/c7bac0678accca8bc0a80151259ca619/

## Publiceren op de bestaande GitHub Pages-site

Deze handelingen zijn bewust niet uitgevoerd. Er is geen push, pull request, merge of publicatie gedaan.

1. Maak voor publicatie ook een back-up van je **browsergegevens**. De repositoryback-up bevat geen lokale API-sleutel, adresboek of instellingen van je iPhone. Verwijder geen websitegegevens. Instellingen blijven alleen behouden op dezelfde website, in dezelfde browser en hetzelfde profiel; een lokale voorvertoning heeft een andere opslagruimte.
2. Haal de nieuwste versie van de repository op. De NDW-workflow kan sinds deze oplevering nieuwere data hebben geschreven. Maak een aparte wijzigingstak vanaf die nieuwste versie.
3. Neem `index.html`, `planner-core.js`, `ride-mode.js`, `contacts-book.js`, `scripts/update_laadprijzen.py` en de nieuwe map `tests` over. Bewaar overige bestaande bestanden. Lees deze README en het testrapport mee in de wijziging.
4. Laat de vernieuwde NDW-verwerker **vóór publicatie** opnieuw lopen met `python3 scripts/update_laadprijzen.py`. Gebruik geen oudere tegels samen met de nieuwe rekenlogica: de nieuwe tegels bewaren extra tariefinformatie. Voer daarna `python3 tests/audit_ndw.py` uit en voeg de complete nieuwe `data`-map toe, inclusief verwijderingen van oude ongeldige tegels. Het meegeleverde ZIP bevat al een passend, getest gegevensbestand van 6 november; een nieuwe verwerking verdient de voorkeur zodra je later publiceert.
5. Controleer met `node tests/core.test.cjs` en `node tests/integration.test.cjs` (Node 22 of hoger), en bekijk de wijziging in een pull request. De integratietests gebruiken gecontroleerde voorbeeldantwoorden, geen echte Google-sleutel.
6. Controleer in GitHub onder Settings → Pages welke branch/map wordt gepubliceerd. Behoud die bestaande instelling. Laat de wijziging pas na jouw beoordeling/toestemming samenvoegen. Op de gebruikelijke main/root-configuratie werkt de nieuwe app op dezelfde bestaande URL.
7. De bestaande NDW-workflow blijft ongewijzigd meegeleverd, inclusief zijn planning. Voor automatische data-updates moet de workflow schrijfrechten op repository-inhoud hebben. Controleer bij een mislukte run de Actions-log en de bestaande instelling Workflow permissions. Verleen alleen de benodigde rechten.
8. Open de live URL opnieuw op je iPhone. Controleer de lokale instellingen, verbind Google Maps indien nodig en zoek een bekende bestemming. Test ontvangst in de auto afzonderlijk.

### Google Maps instellen

Beperk de browsersleutel in Google Cloud tot de eigen website en vereiste API's. Voor de bestaande integratie zijn Maps JavaScript API, Places API (New), Routes API en geocodering nodig, met geactiveerde facturering. Controleer ook de Geocoding API-rechten voor de gebruikte Geocoder. Een browser-API-sleutel is zichtbaar voor de browser en Google; lokaal opslaan maakt hem niet tot een serversleutel. Website-/API-beperkingen en quota zijn daarom noodzakelijk. Publiceer nooit een onbeperkte sleutel.

Voeg alleen wanneer je lokaal wilt testen ook de eigen localhost-origin aan de toegestane websites toe. De publieke GitHub Pages-origin en een eventuele eigen domeinnaam blijven de productiebeperkingen. De sleutel zelf gaat niet mee in dit pakket.

Google-route-API: https://developers.google.com/maps/documentation/javascript/routes/get-a-route
Google Maps-links: https://developers.google.com/maps/documentation/urls/get-started

## Herstellen

De oorspronkelijke repository is inclusief geschiedenis opgeslagen in `volvo-reisplanner-backup.bundle`. Je kunt deze lokaal herstellen met:

```sh
git clone /volledig/pad/naar/volvo-reisplanner-backup.bundle volvo-reisplanner-herstel
```

Er is tevens een kleinere oorspronkelijke bestandsback-up in `volvo-reisplanner-origineel.zip`. Voor het terugdraaien van een latere publicatie verdient het terugdraaien van alleen de app-wijziging in GitHub de voorkeur: zo blijven recentere NDW-data behouden. Verwijder geen browseropslag. **Invoer herstellen** bewaart adresboek, API-sleutel en eigen waarnemingen, en wist route-/kosten-/laadinvoer en de geselecteerde tariefkoppeling.

## Grenzen van de gegevens

NDW-status is geen garantie van fysieke aanwezigheid, werking of een vrije parkeerplek bij aankomst. De rechtstreekse status is een telling per locatie; die bewijst niet dat juist de aansluiting met het goedkoopste tarief vrij is. Bij meerdere mogelijke geografische matches wordt geen status toegekend. De browser kan de rechtstreekse interface blokkeren; de app toont dan de opgeslagen momentopname met een waarschuwing.

De raming gebruikt de ingevulde laadduur, verbonden tijd, btw-behandeling en eventuele toeslagen. Onbekende toeslagen met invoer €0 betekenen niet dat laden of parkeren gratis is. Laadverlies, werkelijk hybride rijgedrag en toekomstige tariefwisselingen zijn niet automatisch gemodelleerd. Complexe tarieven worden daarom niet als gegarandeerde eindprijs gepresenteerd.

NDW-interface: https://docs.ndw.nu/en/data-uitwisseling/interface-beschrijvingen/dafne-api/dafne_api_consumer_pull/
OCPI-tarieven: https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_tariffs.asciidoc

## Laadpaal kiezen

Iedere gevonden laadpaal heeft nu een direct zichtbare knop **Dit is mijn keuze**. De gekozen kaart wordt groen gemarkeerd en de knop krijgt een vinkje. Er kan één laadpaal tegelijk gekozen zijn; de keuze blijft lokaal bewaard en is gekoppeld aan de bestemming. Bij een berekenbaar tarief wordt dit gebruikt voor de volledige laadsessie in de ritkosten. Bij een onbekend tarief wordt een eerder gekozen prijs gewist en moet je de kosten handmatig invullen; een onbekende prijs wordt niet als gratis getoond. De knop legt je voorkeur vast en reserveert geen laadpaal.

## Herstel tarief naar Kosten

Eenvoudige NDW-tarieven van het officiële type AD_HOC_PAYMENT worden nu herkend naast REGULAR. Op de kaart en in de gekoppelde kosten staat duidelijk dat dit een tarief voor direct betalen is en geen bevestigd Shuttel-tarief. Na herladen: zoek laadpalen opnieuw en klik opnieuw op **Dit is mijn keuze**, zodat een eerder als onbekend opgeslagen tarief opnieuw wordt gekoppeld. De opties voor ritkosten heten nu **Alleen stroom die je tijdens deze rit verbruikt** en **Alles wat je bij de laadpaal betaalt (aanbevolen)**. De laatste optie telt de volledige sessie af en wordt bij het kiezen automatisch ingesteld.

OCPI-bron: https://ocpi.github.io/openapi-specification/ocpi/2.2.1/roles/cpo-interface.html#tag/TariffType

## Ritstand: melding bij de gekozen laadpaal

1. Kies onder Laden een laadlocatie met **Dit is mijn keuze**.
2. Open Ritstand, test de gesproken melding en start de aankomstmelding vóór vertrek.
3. Houd de planner zichtbaar op een ontgrendeld toestel en geef locatietoestemming.

De planner controleert de autoroute vanaf je GPS-positie naar de gekozen laadlocatie. Vanaf maximaal 2 km aanrijafstand controleert hij de NDW-status en meldt hij vrij, geen vrije aansluiting of onbekend. Alleen actuele AC Type 2-status met geldige aantallen telt mee; status ouder dan 15 minuten is onbekend. Dit is geen reservering en de situatie kan vóór aankomst veranderen. Er is geen kostenmelding of veld voor resterende ritkilometers meer in Ritstand; laadadvies blijft beschikbaar bij Kosten.

Stop beëindigt locatievolging. Een andere laadpaal kiezen of het vertrek/bestemmingsadres veranderen stopt de ritstand. De app bewaart geen GPS-ritgeschiedenis. Routecontroles delen coördinaten met Google; beschikbaarheidscontroles gebruiken NDW.

### Andere paal — één optie voor Google Maps

Bij een actueel niet-vrij gemelde gekozen laadlocatie rond 2 km zoekt de planner een alternatief bij de oorspronkelijke bezoekbestemming. Hij controleert maximaal acht nabijgelegen kandidaten met actuele vrije NDW-status, een looproute van maximaal 500 m naar je bezoekadres en een autoroute vanaf je positie. De kortste bevestigde autoroute wordt aangeboden; dit is niet noodzakelijk de goedkoopste laadpaal. De status wordt voor aanbieden opnieuw opgehaald. Ontbrekende routes of onzekere status geven geen optie.

Het nieuwe tabblad **Andere paal** toont uitsluitend die ene laadlocatie met één link: **Kies deze laadpaal en open Google Maps**. De link bewaart je nieuwe laadpaalkeuze, neemt het bekende tarief over (of wist de oude prijs bij onbekend tarief) en opent de coördinaten in Google Maps. Je bezoekadres blijft behouden. De ritstand stopt na de nieuwe keuze; opnieuw starten doe je wanneer je stilstaat. Een latere GPS-controle kan de aangeboden optie vervangen of verwijderen.

Op de iPhone opent Google Maps als die app beschikbaar is; anders opent de webversie. Kies daar Naar auto sturen als jouw account/auto deze optie aanbiedt. **Ontvangst in de Volvo en automatisch omleiden zijn niet bevestigd of getest.** De planner opent nooit zelfstandig een andere app vanuit een locatie-update. Gebruik de knop stilstaand of met hulp van een passagier. De knop bevat geen API-sleutel.

Bron voor Maps-links: https://developers.google.com/maps/documentation/urls/get-started

De browserfunctie werkt alleen op de voorgrond en probeert het scherm wakker te houden. Meldingen bij vergrendeld scherm of een verborgen pagina zijn niet gegarandeerd. Het lokale adres http://127.0.0.1:8788/ werkt alleen op de Mac. Voor de iPhone is eerst bereikbare HTTPS-hosting nodig; er is niet gepubliceerd.

Technische bronnen: https://www.w3.org/TR/geolocation/#request-a-position en https://w3c.github.io/screen-wake-lock/

## Apple Contacten gebruiken

Het tabblad **Meer** bevat nu **Adresboek en contacten**. Op de Mac/iPhone is dit een lokale vCard-import; de website krijgt geen directe of blijvende toegang tot Apple Contacten en synchroniseert die niet automatisch.

1. Open op je Mac Contacten en selecteer de gewenste personen. Kies Archief → Exporteer → Exporteer vCard. Bewaar het bestand op je eigen apparaat.
2. Kies in de planner onder Meer het .vcf-bestand. Je ziet eerst een voorbeeld; er wordt nog niets toegevoegd. Alleen namen en bruikbare postadressen worden verwerkt, geen telefoon, e-mail, notities of foto's.
3. Vink gewenste adressen aan en klik Geselecteerde contacten bewaren. Het bestaande adresboek blijft behouden en dubbele naam/adres-combinaties worden overgeslagen. Contacten zonder postadres worden gemeld.
4. Kies bij Gekozen adres gebruiken als **Vertrekadres** of **Bestemming**, zoek op naam/plaats en selecteer het contact. Pas bij gebruik voor adres-/routeberekening wordt het gekozen adres met Google gedeeld.

De import blijft op dit apparaat en in deze browser. Je hoeft geen contactenbestand in de chat te delen en er is geen upload naar GitHub. Wil je contacten op een tweede apparaat gebruiken, dan moet je ze daar afzonderlijk importeren. Op browsers die een systeem-contactenkiezer mét postadressen ondersteunen, is er bovendien een knop voor expliciet gekozen contacten; op Mac/iPhone gebruik je de vCard-route.

Apple-handleiding: https://support.apple.com/nl-nl/108306
Browserbeperking/contactenkiezer: https://developer.chrome.com/docs/capabilities/web-apis/contact-picker

## Tabvolgorde en microfoon

De volgorde is **Route → Ritstand → Andere paal → Laden → Kosten → Meer**. Ritstand is niet meer opgenomen in de Route-tab.

Onder Meer staat de huidige microfoontoestemming, als de browser die kan uitlezen. Veranderingen van toegestaan naar geblokkeerd of andersom worden getoond. Dit vraagt geen nieuwe microfoontoegang en start geen opname. Voor toegang bij volgende bezoeken kies je in Chrome **Toestaan tijdens bezoek aan de site** of zet je Microfoon onder Site-instellingen op Toestaan. De website kan die browserinstelling niet afdwingen of onbeperkt vasthouden. Aan de bestaande microfoonknoppen en hun expliciete start/stop is niets verwijderd.

## Adreszoeken en scrollen — publicatieversie

Typ in het extra Google Maps-zoekveld of dicteer. Onder Zoek adres verschijnt een eigen lijst met Google Places-resultaten, maximaal 180 pixels hoog; veeg of scroll binnen die lijst. Kiezen haalt het volledige adres op. Als Places geen resultaten geeft, gebruikt de planner Geocoding. Het ingebouwde Google-menu blijft beschikbaar.
