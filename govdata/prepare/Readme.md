# Aufbereitung der RDF Dateien für ML

Nach dem Download der RDF Dateien von govdata müssen diese noch für die Benutzung aufbereitet werden. Zum einen müssen die Dateien identifiziert werden, die Daten von Kommunen sind und zum anderen diese zusammengefügt werden in eine CSV Datei.  

## Welche Kommumen veröffentlichen auf govdata?

Das klingt nach einer einfachen Frage, stellt sich aber bei näherer Betrachtung als ziemlich komplex heraus.  
Denn, eine detaillierte Übersicht über alle Kommunen Deutschlands gab es zum Zeitpunkt der Erstellung dieses Musterdatenkataloges nicht. Es gibt die Arbeit von Thomas Tursics, aber diese war nicht vollständig und nicht alle dort aufgeführten Kommunen sind auch auf govdata vertreten. 

Eigentlich bietet auch govdata.de selbst eine Liste aller veröffentlichenden Organisationen an, aber die Betonung liegt auf _veröffentlichenden_ Organisationen. Das sind im Fall von govdata aber die Landesportale.  
Und auch einige Landesportale veröffentlichen Listen von Organisationen, aber diese sind nicht immer vollständig und enthalten auch keine Informationen, ob die Organisation eine Kommune ist oder nicht.  

Es gibt ein tolles Feld in der API das nennt sich `maintainer_city`, aber leider heißt das nicht unbedingt, dass das auch Daten der Kommune sind. Genauso gut kann es sein, dass dort eine Bundes- oder Landesbehörde angesiedelt ist.

Wir haben am Ende eine Kombination aus vielen Feldern benutzt um möglichst alle Kommunen zu erfassen. Diese mussten dann aber manuell dursucht und bewertet werden, ob es sich hier um Daten einer Kommune handelt.

Betrachtet wurden:

* `maintainer`
* `publisher`
* `creator`
* `author`

Oder genauer in DCAT-AP Notation:

* 'vcard:fn'
* 'dct:publisher' -> 'foaf:name'
* 'dcatde:maintainer' -> 'foaf:name'
* 'dct:maintainer' -> 'foaf:name'
* 'dct:creator' -> 'foaf:name'

Das Ergebnis ist die Datei `cities.csv`, diese ist sicher nicht vollständig und wir freuen uns über jede Hilfe dabei diese zu verbessern.  

## Aufbereitung

Aus den RDF Dateien werden die für uns wichtigen Informationen, der Titel, die Beschreibung, die Kategorien und die Tags, gefiltert.
Darüber hinaus wird geschaut, ob der Datensatz auch zu einer Kommune gehört. Dazu werden die oben genannten Felder überprüft und dann mit Hilfe der `cities.csv` einer Kommune zugeordnet.

## Benutzung

__Installieren der Bibliotheken:__

```
pip install -r requirements.txt
```

Laufen des Programms:

```
python process.py
```

Das Ergebnis ist eine Datei mit den Datensätzen, die benutzt werden können um mit dem Machine Learning Modell einen Musterdatensatz zu bestimmen.  
