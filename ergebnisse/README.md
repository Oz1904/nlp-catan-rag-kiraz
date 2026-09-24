# Ergebnisse

Alle Dateien in diesem Ordner erzeugt das Notebook. Nach jedem Lauf packt es sie als `ergebnisse_paket.zip`; der Inhalt wird unverändert hierher übernommen. Solange dieser Ordner leer ist, hat der Abgabelauf noch nicht stattgefunden und der Prüfmodus des Notebooks findet nichts zum Auswerten.

| Datei | Inhalt |
|---|---|
| `versuchsplan.json` | eingefrorene Konfiguration, Regelgruppenregister und Prüfsumme des Laufs |
| `quellenmanifest.csv` | URL, Abrufdatum und SHA-256 je verwendeter PDF-Fassung |
| `laufprotokoll.jsonl` | jede Modellantwort mit Kontext-IDs, Tokenzahl, Modellversion, Abbruchgrund |
| `bewertungen.csv` | verblindeter Bewertungsbogen, ausgefüllt |
| `bewertung_schluessel.csv` | Zuordnung Fall → Frage und Bedingung, getrennt vom Bogen |
| `zweitbewertung_auswahl.csv` | vorab gezogene Fälle für die Zweitbewertung |
| `bewertungen_zweitperson.csv` | Bewertung derselben Fälle durch eine zweite Person, handschriftlich erhoben und übertragen (Abschnitt 5.3) |
| `bewertungen_archiv_*.csv`, `bewertung_schluessel_archiv_*.csv` | Bögen früherer Prüfsummen; sie belegen die Kalibrierung an den Entwicklungsfragen (Abschnitt 5.3) und gehen in keine Kennzahl ein |
| `retrieval_metriken.csv` | Precision@k, Recall@k, F1, Zitat-Recall je Frage |
| `topk_justierung.csv`, `topk_justierung.png` | Justierung von Top-k an den Entwicklungsfragen |
| `korrektheit_gesamt.csv`, `korrektheit_nach_fragetyp.csv` | Anteile vollständig korrekter Antworten |
| `bootstrap.csv` | Cluster-Bootstrap mit 95-%-Intervallen, mit Prüfsumme des Laufs |
| `fehlerdiagnose.csv` | Befundzuordnung je Frage aus dem A/B/C-Vergleich |
| `segmentierung_pruefung.csv`, `konstruktionsvaliditaet.csv` | Kontrollen zur Wissensbasis und zum Katalog |
| `abschlusspruefung.csv`, `versionen.csv` | Ergebnis der automatischen Abschlusskontrolle, Programmversionen |
| `schema.sql` | Supabase-/pgvector-Schema inklusive Suchfunktion |
| `ergebnisse.png` | Abbildung zur Antwortkorrektheit |

Keine Datei enthält die vollständigen Texte der Regelhefte: Das Laufprotokoll speichert nur die IDs der Kontext-Chunks, nicht deren Text.
