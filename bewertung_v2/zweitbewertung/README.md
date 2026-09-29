# Zweitbewertung zu Bewertung v2

Festgelegt am 29.09.2026, bevor die zweite Person bewertet hat:

- **Auswahl:** 10 Testfragen mit je allen vier Antworten (A, B, C, D), also 40 Fälle. Gezogen mit Seed `202609292` aus den 20 Testfragen, die in der ersten Zweitbewertung (Schema v1) nicht vorkamen: T02, T03, T06, T07, T19, T20, T22, T26, T27, T30.
- **Verblindung:** neue Kennungen Z01–Z40 und neue Reihenfolge. `auswahl_zweit.csv` ordnet sie den Fällen V001–V120 zu; die Bedingung steht nur in `../schluessel_v2.csv`.
- **Rubrik:** dieselbe eingefrorene Rubrik v2 (`../RUBRIK.md`), dieselben Merkmale; die Stufe berechnet `../stufe.py`.
- **Ablauf:** Die zweite Person bewertet allein im Offline-Werkzeug `CATAN_Zweitbewertung.html`, mit Regelheft, ohne KI-Werkzeuge und ohne die Urteile des Autors zu kennen. Die exportierte CSV geht ungeöffnet in `ergebnisse/zweitbewertung_v2.csv`.
- **Auswertung:** Übereinstimmung mit Bewertung v2 (binär und dreistufig, Cohens κ; zusätzlich je Merkmal). Bewertung v2 wird dadurch nicht verändert.

## Durchführung

Die exportierte Datei ist am 29.09.2026 eingegangen und wurde unverändert als `ergebnisse/zweitbewertung_v2.csv` übernommen (SHA-256 `5c3992426fc23734d073121936a1ee465c283ba75fe22a9dcb86c1c975254a11`). Die Auswertung steht im Notebook (Kapitel 10, Abschnitt 11.1).
