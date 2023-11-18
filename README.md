![logo](logo.jpg)

# Een Eeuw Eefde

Compilatie van oude foto's van Eefde door Dirk Roorda. 

[[https://github.com/dirkroorda/historisch-eefde/blob/master/logo.jpg|alt=logo]]

Elke foto bevat een beschrijving, GPS coordinaten van wat erop staat, en de
datum waarop hij genomen is.

## Doel

Al deze foto's zijn al ergens anders te zien. Met name de beeldbank van het
Erfgoedcentrum Zutphen geeft een heel mooie toegang tot al deze foto's en meer.

Mijn doel was om een hieruit een selectie te maken die gevoel kan geven hoe
Eefde er de laatste eeuw heeft uitgezien, en hoe het was om hier je leven te
leiden. Hoe zou het zijn om per straat door de tijd te kunnen wandelen?

## Methode

Ik heb uit de 1300+ fotos van Eefde die beeldbank heeft er 400+ geselecteerd.
Alle gegevens over de foto (de *metadata*) heb ik in de foto's zelf opgeslagen.
Op die manier kan het fotoprogramma dat je gebruikt ze op allerlei manieren
rangschikken.

Tot de metadata van elke foto behoren 

*   de tijd waarop hij genomen is; soms is de onzekerheid groot;
*   de plaats waar hij genomen is; ik heb ze allemaal op een satellietkaart
    bekeken en het vermoedelijke standpunt van de fotograaf nauwkeurig aangegeven;
*   sleutelwoorden die iets zeggen over het onderwerp of de straatnaam, 
    zoals *brand*, *brug*, *sluis*, *mettray*, *almenseweg*, *schoolstraat*,
    *huisdevoorst*;
*   de beschrijving die het Erfgoedcentrum erbij heeft gezet;
    hierbij heb ik soms dingen verbeterd en aangevuld, met behulp van het boek
    [Eefde Kroniek van een Verknipt Dorp van de Elf Marken](https://www.deelfmarken.nl/eefde-kroniek-van-een-verknipt-dorp.html);
*   de herkomst van de foto, met de vervaardiger/uitgever en een link naar het
    origineel bij het Erfgoedcentrum.

Al deze informatie is in elke foto ingebakken, maar ook los verkrijgbaar in een
apart bestandje met dezelfde naam als de foto.

## Bron

Alle vrijwel alle foto's heb ik gedownload van de
[Beeldbank Erfgoedcentrum Zutphen](https://erfgoedcentrumzutphen.nl/onderzoeken/beeldbank/?q=eefde).
In de beschrijving van elke foto staat een directe link naar de foto op het
Erfgoedcentrum.

## Waar te zien?

Je kunt de foto's
[hier](https://github.com/dirkroorda/historisch-eefde/tree/master/photos)
online bekijken. Maar dat is niet de beste ervaring.

## Downloaden

Je kunt alle photos in één keer downloaden vanuit deze
[bewaarplaats]().

Je krijgt ze dan snel en efficiënt op je computer.

## Volgende stap

De meeste controle krijg je als je de foto's importeert in je eigen fotoprogramma.
Je kunt dan bijvoorbeeld je eigen recente foto's eraan toevoegen, en zelf albums maken.
Bovendien heb je de foto's dan zelf.

Na importeren is het mogelijk even zoeken waar ze gebleven zijn temidden van je
andere fotos, omdat deze foto's in een ver verleden genomen zijn. Je
fotoprogramma begraaft ze dan temidden van foto's van jaren geleden.

Maar meestal geven die programma's je ook een inzicht per datum van invoeren
(*camera roll*), waar je ze allemaal bijelkaar ziet.

Een andere methode is: zoeken op *keyword*: ze hebben allemaal de keywords
**historisch** en **Eefde**.

Elke foto heeft ook de straatnaam als sleutelwoord, bv **kapperallee** of
**boedelhofweg**.  In je fotoprogramma kun je daar op zoeken, en kun je albums
maken per sleutelwoord.

Als je alle foto's selecteert en naar de sleutelwoorden kijkt, kun je zien
welke er allemaal voorkomen.

## Wat mag ik met deze foto's doen?

Je kunt deze foto's zonder meer downloaden en gebruiken in de persoonlijke sfeer.
Wil je andere dingen doen, dan moet je ervan uitgaan dat er op de foto's copyright rust.
Niet van mij, niet van de Beeldbank, maar van de vervaardiger/uitgever van het
origineel.  Waar bekend, heb ik die informatie in de foto opgenomen.
Volg de directe link naar de betreffende foto bij het Erfgoedcentrum, waar nog
iets meer informatie bij de foto staat.

Wat je ook met de foto's doet, de beleefdheid gebiedt om bronvermelding toe te passen.

Dat kan heel simpel:

**Hele compilatie of meerdere foto's**:

Bron: *Een Eeuw Eefde*.
Compilatie samengesteld door Dirk Roorda uit de Beeldbank van het
Erfgoedcentrum Zutphen. 
Link: https://github.com/dirkroorda/historisch-eefde

## Techniek

De metadata van de foto's sla ik op in platte tekst files, `.yaml` om precies te zijn.
Vervolgens meng ik die metadata in de bijbehorende beeldbestanden, `.jpg`.
Zie [photo-workflow](https://github.com/dirkroorda/photo-workflow).

### Details

*NB: Twee soorten metadata*:
Je ziet in deze bewaarplaats twee mappen met metadata:

*   [metdatafull](https://github.com/dirkroorda/historisch-eefde/tree/master/metadatafull)
    Hier zit de volledige metadata van elke foto in.
*   [metdata](https://github.com/dirkroorda/historisch-eefde/tree/master/metadata)
    Hier zit de essentiële metadata in.

*Toelichting*:
Delen van de metadata zijn redundant in de zin dat het standaard waarden zijn of dat
ze uit andere metadata afgeleid kunnen worden.

Als je het redundante gedeelte weglaat, hou je de essentiële metadata over.

*Datums*:
In de *metadata* van sommmige foto's zie je het veld *datetime*.
Dit vbevat de datum van de foto wanneer die niet al in het origineel van de foto
was opgeslagen. Deze datum hebben we in de hier gepubliceerde versie van de foto
erbij ingeschreven.

Bij nieuwere foto's waar de datum wel klopt, zie je de *datetime* niet onder *metadata*.

In de *metadatafull* heeft iedere foto zodoende een *datetime* gekregen.
