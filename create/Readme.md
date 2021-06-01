# Erstellen des Musterdatenkataloges

Mit diesem Script wird der endgültige Musterdatenkatalog mit dem Ergebnis des ML Modells (predict) erstellt.

## NRW

Um konsistent zu bleiben, haben wir uns entschieden, den NRW Katalog nicht nur als Trainingsgrundlage zu benutzen, sondern die Datensätze die dort gescored wurden auch in den Musterdatenkatalog D aufzunehmen und das Ergebnis für diese Datensätze zu überschreiben.

Der Algorithmus sagt den Musterdatensatz (Kombination aus Thema und Bezeichnung) vorher, wir benutzen unsere API um diese "aufzuspalten".
