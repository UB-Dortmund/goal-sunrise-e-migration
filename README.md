# Markierung von nicht zu migrierenden Titeldaten in Sunrise

## Ansprechpartner

Dipl.-Math. Hans-Georg Becker (M.L.I.S.)\
ORCID iD https://orcid.org/0000-0003-0432-294X

Technische Universität Dortmund\
Universitätsbibliothek\
Informationssysteme und Datenmanagement\
https://www.ub.tu-dortmund.de

## Konzept aus der FEx Daten

Das hbz stellt ID-Listen mit hbz-Titel-IDs, getrennt nach Kollektionen, zu Verfügung. 
Diese Titeldaten wird das hbz entweder bei der Migration aus der CZ in der NZ
aktivieren oder als P2E migrieren. Diese Titelmengen sind bei der
Migration aus den ILS auszuschließen und über Feld MARC-035 zu markieren
mittels Textstring IZEXCLUDE.

**Technische Lösung SISIS:**

- die technische Umsetzung findet per Batch im Filesystem auf Basis der
extrahierten Daten statt (Manipulation der MARC-XML-Datei)
- die technische Lösung wird von der UB Dortmund (Hr. Becker)
erarbeitet und bereitgestellt
- Ergebnis: Titel-Migrationsdatei, in der bei einzelnen Titeln das Feld
035, Unterfeld a existiert mit Inhalt "(IZEXCLUDE)<catkey>"

Schutz des Feldes 035 vor Überschreiben aus der NZ:

Wenn das Feld 035 bei Titeln, die ggf. aufgrund Bestellungen im ILS
doch migriert werden, erhalten bleiben soll, so kann nach derzeitigem
Stand kein Unterfeld 9 mit dem Wert "local" ergänzt werden. Das Feld 035
kann zurzeit noch nicht in Alma als "local extension" genutzt werden.
Lösung: zusätzlich zum Feld 035 ein lokales Feld (9xx) erzeugen.

**TODO:** Definition der lokalen Felder (9xx)

## Umsetzung der technischen Lösung für SISIS

Das Skript erwartet ID-Listen des hbz im Ordner `data/id_lists/nzexclude`. Die Listen
aus Sicht der IZ werden in `data/id_lists/izexclude` erwartet.

Die Listen sind einfache Textdateien, in der pro Zeile eine hbz-ID oder ein Catkey enthalten ist.

Für die NZ z.B.

```
HT017065150
HT019609130
```

bzw. für die IZ:

```
1505893
1506737
1660270
1578603
1494764
1649744
```

Für die NZ-Fälle wird folgendes im MARCXML-Record ergänzt:

```
<marc:datafield tag="035" ind1=" " ind2=" ">
        <marc:subfield code="a">(IZEXCLUDE)(NZ)HT017065150</marc:subfield>
</marc:datafield>
```

Für die IZ-Fälle gilt:

```
<marc:datafield tag="035" ind1=" " ind2=" ">
        <marc:subfield code="a">(IZEXCLUDE)(IZ)1505893</marc:subfield>
</marc:datafield>
```

Ferner prüft das Skript, ob in `85640.u` oder `8564 .u` das Pattern `/ezeit/?` enthalten ist.
Sollte das der Fall sein, wird folgendes im MARCXML-Record ergänzt:

```
<marc:datafield tag="035" ind1=" " ind2=" ">
        <marc:subfield code="a">(IZEXCLUDE)(EZB)1674734</marc:subfield>
</marc:datafield>
```

Das Skript zerlegt die MARCXML-Quelldatei aus SISIS in Teildateien mit 200.000 Records, da
das Limit von ExLibris auf diese Anzahl angegeben ist. Die Anzahl kann in der Konfiguration
auch angepasst werden (Parameter `PART_SIZE`).

## Installation der Lösung

* Installieren von OpenJDK 8
* Installieren von Python >= 3.6
* `git clone https://github.com/UB-Dortmund/goal-sunrise-e-migration`
* ggf. anpassen der Konfiguration
* Start: `/usr/bin/python3.6 e-migration.py` (ggf. vorher noch ins Code-Verzeichnis wechseln)
* Be happy :-)

**Konfiguration:**

Editieren der Datei `config.py` (falls notwendig):

```
# ID lists
NZEXCLUDE_DIR = 'data/id_lists/nzexclude'
IZEXCLUDE_DIR = 'data/id_lists/izexclude'

ID_MAP_DIR = 'data/tmp/id_maps'

# DATA CONF
#SOURCES_DIR = 'data/sources'
SOURCES_DIR = '/home/mhagbeck/data/GOAL/src'
TMP_SOURCES_DIR = 'data/tmp/sources'
RESULTS_DIR = 'data/results'

PART_SIZE = 200000

# METAFACTURE
FLUX_START_SCRIPT = 'metafacture/dist/flux.sh'
METAFACTURE_PROJECTS_DIR = 'metafacture/project'

NUMBER_OF_WORKERS = 8

# LOGGING
LOG_FILE = 'log/e-migration.log'
```


# License

> MIT License

> Copyright 2020 UB Dortmund <daten.ub@tu-dortmund.de> 

> Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

> The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
