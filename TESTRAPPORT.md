# Testrapport — 6 november 2026

## Uitgevoerd en geslaagd

- **24 reken-/tarief-/adviestests**: Nederlandse komma, €12,40- en €13,00-regressie, korte rit, laden uitsluitend voor terugreis, seizoens-/handmatig bereik, resterende accuruimte, volledige sessiebetaling, energieafronding, btw, start-/tijd-/parkeertijdkosten, gezamenlijke tijdafronding, vlak tarief, onbekende/complexe tarieven, geldigheid, duurvalidatie, Shuttel/parkeertoeslagen en prijsrangschikking.
- **10 integratiescenario's** met gecontroleerde antwoorden: onafhankelijke heen-/terugroutes; top3 met onbekenden apart en uitsluiting van bezet of 501 m lopen; tarief overnemen en herberekenen; handmatige tariefwijziging; adresboek; NDW-netwerkfout; live locaties zonder prijsbestand; ontbrekende looproute; lokale instellingen en afzonderlijke sleutelopslag.
- **Werkelijke NDW-bronnen opnieuw verwerkt**: 83.647 ontvangen locaties en 106.322 tarieven; 82.243 Nederlandse AC Type 2-locaties verwerkt; 17 locaties met onbruikbare coördinaten niet opgenomen in de tegels.
- **Alle 132 tegels gecontroleerd**: 82.226 locaties, 202.651 aansluitingen, 5.294 expliciet onbekende tariefverwijzingen; juiste geografische indeling, AC Type 2-filter, aantallen en alle tariefreferenties. Ophaalmoment: 6 november 2026, 13:36:08 Nederlandse tijd.
- **Rechtstreekse NDW-interface werkelijk benaderd**: HTTP 200, 47 GeoJSON-locaties in een klein testgebied bij Apeldoorn. Dit bewijst de serverbereikbaarheid en gegevensvorm; dit is geen bewijs van browser-CORS-toegang of fysieke beschikbaarheid.
- **Browsercontrole**: app geladen, tabs bediend, Nederlandse komma ingevoerd; 120 km met 60 km thuis, 20 km bijgeladen en 40 km benzine toont €3,00 + €1,40 + €8,00 = **€12,40**. Herladen bewaart route- en kosteninvoer en toont meteen 120 km. Laadvolume 12,5 kWh blijft bewaard; volledige sessie toont €4,38 openbaar laden en €15,38 totaal bij €0,35/kWh.
- **Mobiele weergave** gecontroleerd op 390 × 844; kostenvelden, berekening en tabnavigatie bruikbaar. Schermopname meegeleverd.
- JavaScript-syntaxis gecontroleerd. Repositoryback-up met volledige Git-geschiedenis geverifieerd.

## Niet in een echte gebruikerssessie geverifieerd

Google Maps met een werkelijke API-sleutel, browser-CORS voor de rechtstreekse NDW-status, microfoontoestemming/dicteren op iOS, de deelactie naar een externe app, afdrukuitvoer als PDF en ontvangst van een bestemming in de fysieke Volvo zijn hier niet end-to-end getest. Het bronpad voor deze bestaande functies is behouden; de nieuwe logica gebruikt daarnaast integratietests met gecontroleerde antwoorden. Echte Shuttel-acceptatie, Shuttel-eindprijzen en gemeentelijk parkeergeld zijn niet geverifieerd.

De oorspronkelijke aparte HTML en volledige oudere planning waren niet beschikbaar. Daarom is niet te bewijzen dat niet genoemde wensen uit oudere gesprekken zijn geïmplementeerd. De expliciete eisen uit de huidige opdracht zijn verwerkt, met de hierboven beschreven grenzen.

## Zelf herhalen

```sh
node tests/core.test.cjs
node tests/integration.test.cjs
python3 tests/audit_ndw.py
```

Node 22 of hoger en Python 3.9 of hoger. Geen extra testpakketten, echte API-sleutel of netwerk nodig voor deze controles. Voor nieuwe brongegevens: `python3 scripts/update_laadprijzen.py` vereist internet, gevolgd door opnieuw de tegelcontrole.

## Toevoeging laadadvies

Zeven aanvullende berekeningstests geslaagd: benzine goedkoper, laden goedkoper, start-/tijdkosten veranderen het advies, gelijke kosten, geen nuttige bijlaadkilometers, begrenzing door werkelijk laadvolume en ontbrekende invoer. Een extra app-integratietest bevestigt dat de zichtbare tekst automatisch wisselt bij gewijzigde prijzen. Totaal: 34 automatische tests. De eerdere browsercontrole dateert van vóór deze toevoeging; het nieuwe advies is met de app-integratietest gecontroleerd.

## Aanpassing adreslijsten Mac

Twee extra integratiecontroles slagen: alternatief adreszoeken/selecteren voor vertrek én bestemming en aanwezigheid van de begrensde scrollstijl. Totaal nu 24 rekentests en 12 integratiecontroles = 36. De scrollstijl gebruikt Googles gedocumenteerde prediction-list CSS-part.

Aanvullende browsertest met een geïsoleerd voorbeeldwidget en zonder API-sleutel: beide lijsten meten 324 px hoog bij 750 px inhoud, met overflow:auto. Een scrollactie binnen de vertrekresultaten verandert scrollTop van 0 naar 100, terwijl de bestemmingslijst op 0 blijft. De alternatieve adreskeuze vult na het aanklikken Teststraat 1, Nederland als bestemming in. De voorbeeldwidget controleert onze vormgeving en browserbediening; dit is geen bevestiging van de reparatie in de werkelijke Google-sessie op de Mac van de gebruiker.

## Chrome-herstel na aanhoudende melding

De eerdere wijziging aan het ingebouwde Google-menu is niet door de gebruiker als werkend bevestigd. Daarom staat de gewone resultatenlijst nu standaard in beeld en blijft het ingebouwde menu optioneel ingeklapt. Zoekopdrachten na typen worden vertraagd; verouderde antwoorden overschrijven geen nieuwe zoektekst. Microfoonherkenning wordt alleen na klikken gestart en de instantie wordt hergebruikt. De daadwerkelijke Chrome-microfoontoestemming is niet automatisch ingesteld of als blijvend bevestigd.

24 rekentests en 13 app-integratiecontroles slagen (37 JavaScript-controles), waaronder standaard gewone lijst en geen automatische microfoonstart. Drie Python-startprogrammatests slagen: nieuwe server, hergebruik van dezelfde server en weigeren van een andere actieve server. De browserstart is daarin vervangen door een testfunctie; werkelijk starten van Chrome en echte adresresultaten/microfoon op de Mac zijn nog niet opnieuw end-to-end bevestigd.

## Herstel zichtbaarheid Google-menu

Het Google Maps-keuzemenu staat weer direct zichtbaar boven het alternatieve zoekveld bij vertrek en bestemming. De integratietest controleert deze plaatsing en behoud van de scrollstijl; 24 rekentests en 13 integratiecontroles slagen opnieuw. De uitgepakte map volvo-reisplanner 3 is bijgewerkt na vergelijking met de eerdere versie en met een back-up. Het echte scrollgedrag in de Chrome/Google-sessie van de gebruiker is nog niet bevestigd.

## Concrete adresfout uit gebruikerssessie

In de werkelijke Chrome-pagina is na Zoek adres de fout `Cannot read properties of undefined (reading 'results')` waargenomen. De verwerking gebruikt nu een wrapper voor zowel de callback- als Promise-interface van Google Geocoding. Twee nieuwe tests slagen: een callback met undefined als returnwaarde geeft resultaten, en REQUEST_DENIED wordt direct bij het betrokken veld getoond. Microfoonfouten worden eveneens bij het veld getoond, met onderscheid tussen toestemming, netwerk en geen spraak.

24 rekentests en 15 integratiecontroles: 39 JavaScript-controles. De poging tot herladen/controleren in de echte Chrome-pagina liep daarna vast in de computerbediening. Een succesvolle echte adreszoekopdracht of microfoonopname na deze wijziging is dus niet bevestigd.

## Knop Dit is mijn keuze

Drie nieuwe integratiecontroles slagen: een laadpaal kiezen markeert de kaart/bewaart de keuze/koppelt het tarief; een andere keuze verwijdert de oude markering; een onbekend tarief gebruikt niet stilzwijgend de prijs van de vorige laadpaal. Totaal 24 rekentests en 18 integratiecontroles = 42 JavaScript-controles. Geen nieuwe handmatige browsercontrole uitgevoerd voor deze knop. De uitgepakte map volvo-reisplanner 3 is met back-up bijgewerkt.

## Regresstest werkelijk NDW-tarief Laan van Bovenduist

Het type AD_HOC_PAYMENT was onterecht niet toegestaan door de berekening. De NDW-fixture NL|QWC|442 bevat ENERGY 0,55/kWh en TIME/PARKING_TIME 0,25/uur. Test bij 10 kWh, 60 minuten laden en 90 minuten aangesloten: energie 5,50, laden 0,25, niet-laden 0,125, totale raming 5,875 euro volgens de ingevulde btw-/toeslaginstellingen. Een integratietest kiest dit tarief via de zichtbare keuze-knop en controleert openbaar tarief 0,55000000, extra kosten 0,37500000 en de betaalde sessie in het kostenoverzicht.

25 rekentests en 19 integratiecontroles slagen (44 JavaScript-controles). De tekst voor de betalingsmethode staat expliciet op de kaart en bij Kosten. De daadwerkelijke Shuttel-prijs is niet geverifieerd. De handmatige browsercontrole liet vooraf lege openbare tariefvelden zien; de nieuwe verwerking is na deze wijziging met de echte NDW-fixture en app-integratietest gecontroleerd.

## Ritstand vervangen door aankomstmelding

De eerdere scanner voor nabijgelegen laadpalen is vervangen door controle van uitsluitend de gekozen laadpaal. Twintig afzonderlijke tests behandelen beschikbaar, bezet en onbekend, oude/ontbrekende/ongeldige status, gekozen bestemming en oude opgeslagen keuze, expliciete start, grens van 2 km, herhaalde of gewijzigde status, onnauwkeurige/verouderde GPS, frequentiebeperking, verborgen pagina, stoppen, late antwoorden, geweigerde locatie en routefouten. De app-integratietest controleert de gekozen locatie met gecontroleerde Google-/NDW-antwoorden.

Browserproef met duidelijk gemarkeerde voorbeeldgegevens: bij 1,8 km tot de gekozen laadpaal wordt de vrije Type 2-aansluiting gemeld. De spraaktekst is geregistreerd; echt geluid en een echte rijdende GPS-proef zijn niet getest. Stop schakelt de functie uit. Screenshot aankomstmelding-2km-test.jpg. Geen automatische wijziging in de ingebouwde Volvo-navigatie en geen alternatiefzoeker geïmplementeerd.

## Apple-contactenimport, aparte Ritstand-tab en microfoonstatus

12 nieuwe parser-/adresboektests slagen: standaard Apple-vCard, meerdere adressen en Apple-labels, regelvouwing, Unicode en escapes, quoted-printable vCard 2.1, naamfallback, alleen naam/postadres, contacten zonder adres, meerdere kaarten, onvolledige/te grote bestanden, behoud/deduplicatie, filterindex en systeemkiezerconversie. Vier extra app-integratiecontroles slagen: importvoorbeeld zonder opslag/netwerk en alleen geselecteerde contact bewaren; gebruik als vertrek/bestemming; exacte vijf-tabvolgorde en afgescheiden Ritstand-view; actuele microfoonstatus zonder automatische opname.

Totaal 25 rekentests + 24 app-integratiecontroles + 15 ritstandtests + 12 contactentests = 76 JavaScript-controles. De bestaande startprogrammatests blijven afzonderlijk beschikbaar.

Browsercontrole met twee zelfgemaakte voorbeeldcontacten: de filechooser laadde het lokale .vcf-bestand; beide adressen werden eerst als aanvinkbaar voorbeeld getoond. Na het uitvinken van Bram werd alleen Anna lokaal toegevoegd. Kiezen als Vertrekadres vulde Voorbeeldstraat 7, 1234 AB, Testplaats, Nederland in en liet Bestemming leeg. Ritstand werd via de knop tussen Route en Laden geopend en had een eigen scherm. De microfoonstatus in de testbrowser toonde correct dat toestemming nog niet was verleend. Er zijn geen echte Apple-contacten gelezen of geïmporteerd en er zijn geen echte Chrome-microfoonrechten gewijzigd. Screenshot contacten-en-ritstand-test.jpg bevat uitsluitend fictieve voorbeeldcontacten.

## Huidige regressiecontrole

25 rekentests + 24 app-integratiecontroles + 20 aankomstmeldingtests + 12 contactentests = 81 JavaScript-controles. De oude beschrijving van 76 controles hierboven betreft de eerdere versie.

## Andere paal-tab en Google Maps-overdracht

Vier nieuwe integratiescenario’s geslaagd: precies één actuele vrije andere locatie met een exacte coördinatenlink en behoud van bezoekadres; aanklikken koppelt de nieuwe keuze en het tarief; geen vrije locatie biedt geen knop; mislukte NDW-hercontrole biedt geen onzekere optie. Totaal nu 85 JavaScript-controles (25 rekenen, 28 integratie, 20 aankomst, 12 contacten). Geen fysieke iPhone/Volvo-overdracht getest. Geen publicatie uitgevoerd.

## Definitieve publicatiecontrole

Echte Chrome/Google-sessie: beide ingebouwde adresmenu’s geven resultaten. De eigen lijst haalt nu Google Places-voorspellingen op, met Geocoding als terugval. Voor vertrek (Amsterdam) en bestemming (Amersfoort) is daadwerkelijk naar de laatste resultaten gescrold; de interne schuifbalk staat onderaan. Microfoon gestart en gestopt zonder nieuwe toestemmingsvraag; auditieve herkenning op iPhone nog niet getest. 86 JavaScript-controles inclusief de nieuwe Places-selectie; iPhone/Volvo-overdracht vereist nog een fysieke proef.
