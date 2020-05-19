# Markierung von nicht zu migrierenden Titeldaten in Sunrise

## Ansprechpartner

Dipl.-Math. Hans-Georg Becker (M.L.I.S.)\
ORCID iD https://orcid.org/0000-0003-0432-294X

Technische Universität Dortmund\
Universitätsbibliothek\
Informationssysteme und Datenmanagement\
https://www.ub.tu-dortmund.de

## Konzept aus der FEx Daten

Das hbz stellt ca. 2 Wochen vor der 1. Testmigration ID-Listen mit
hbz-Titel-IDs, getrennt nach Kollektionen, zu Verfügung. Diese
Titeldaten wird das hbz entweder bei der Migration aus der CZ in der NZ
aktivieren oder als P2E migrieren. Diese Titelmengen sind bei der
Migration aus den ILS auszuschließen und über Feld MARC-035 zu markieren
mittels Textstring IZEXCLUDE.

(IZEXCLUDE ist das Hauptkriterium für ExLibris -> Alle Titel werden mit IZEXCLUDE markiert;
ggf. zusätzliche Marker gesetzt.)

**Technische Lösung SISIS:**

- konzeptionell wie Aleph
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

## NEU!!!! EZB-Titel via URL (Pattern: ezeit)

Pattern: ezeit oder 663 mit "Interna: EZB; Bez.: 0" -> EXCLUDE


## Umsetzung der technischen Lösung für SISIS

* Install OpenJDK 8
* Install Python 3
* Get e-migration project -> github
* Edit config.py -> Erläuterungen
* Start
* Be happy :-)

# License

> MIT License

> UB Dortmund <daten.ub@tu-dortmund.de> 

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
