# Erstellen des Musterdatenkataloges

Mit diesem Script wird der endgültige Musterdatenkatalog mit dem Ergebnis des ML Modells (predict) erstellt.  
Der Algorithmus sagt den Musterdatensatz (Kombination aus Thema und Bezeichnung) vorher. Wir benutzen unsere API um diese "aufzuspalten".

## NRW

Es kann und wird sicherlich vorkommen, dass der Algorithmus einen anderen Musterdatensatz vorhersagt, als im Musterdatenkatalog NRW aufgelistet ist.
Da dies zur Verwirrung führen kann, haben wir uns entschieden das Ergebnis des Algorithmus zu überschreiben.

__Was heißt das konkret?__

Jeder Datensatz, der im Musterdatenkatalog NRW vorhanden ist "behält" seinen Musterdatensatz. Das Ergebnis des Algorithmus wird ignoriert und überschrieben.
Wir tun dass, weil wir davon ausgehen, dass die zuvor manuell erstellte Zuordnung von 2.500 Datensätzen aus NRW (Version 2) etwas genauer ist als die vom Algorithmus erstellte Version. So haben wir insgesamt ein besseres Ergebnis.


# Installation und Ausführung
Zum ausführen des Scripts müssen zuerst die Pakete installiert werden.

```
pip install -r requirements.txt
```

Zum Erstellen des endgültigen Katalogs wird die Datei des [NRW Kataloges](../nrw) benötigt.  
Ausführen des Script via:

```
python musterdatenkatalog.py
```

Das Ergenbnis ist der Musterdatenkatalog Deutschland als csv Datei.
