# Ergebnisse

Die Dateien in diesem Ordner stammen aus den Läufen des Notebooks, mit folgenden Ausnahmen: `bewertung_v2.csv`, `bewertung_v2_abschluss.json` und `zweitbewertung_v2.csv` sind Exporte der Bewertungswerkzeuge, und die beiden `*_pruefmodus_*`-Dateien sind aus der Ausgabe des abgegebenen Notebooks übernommen. Der Prüfmodus liest sie und schreibt Neuberechnungen nach `pruefmodus/`. Keine Datei enthält die Regelhefte im Volltext; die Laufprotokolle speichern nur die Kennungen der Kontext-Chunks.

| Datei | Inhalt |
|---|---|
| `versuchsplan.json` | eingefrorene Konfiguration, Regelgruppen und Prüfsumme des Hauptversuchs (A, B, C) |
| `quellenmanifest.csv` | URL, Abrufdatum und SHA-256 je Regelheft |
| `laufprotokoll.jsonl` | jede Modellantwort aus A, B, C mit Kontext-IDs, Tokenzahlen, Modellversion und Abbruchgrund |
| `zusatz_d/versuchsplan_d.json`, `zusatz_d/laufprotokoll_d.jsonl` | Prüfsumme und Antworten des Zusatzversuchs D |
| `bewertungen.csv`, `bewertung_schluessel.csv` | Bewertungsbogen v1 (108 Fälle; bewertet sind die 90 Testfälle, die 18 Entwicklungsfälle bleiben leer) und Zuordnung Fall → Bedingung |
| `bewertungen_archiv_*.csv` | Kalibrierung an den Entwicklungsfragen, geht in keine Kennzahl ein |
| `zweitbewertung_auswahl.csv`, `bewertungen_zweitperson.csv` | vorab gezogene 30 Fälle und ihre Zweitbewertung (Schema v1) |
| `bewertung_v2.csv` | Bewertung v2: je Fall die erfassten Merkmale, Zeitstempel und Rubrik-Prüfsumme |
| `bewertung_v2_abschluss.json` | Zeitpunkt, zu dem Bewertung v2 abgeschlossen wurde |
| `zweitbewertung_v2.csv` | Zweitbewertung v2: 40 vorab gezogene Fälle (Z01–Z40), unverändert aus dem Offline-Werkzeug exportiert; Zuordnung in `bewertung_v2/zweitbewertung/auswahl_zweit.csv` |
| `zweitbewertung_v2_vergleich.csv` | Stufe und Merkmalsübereinstimmung je Fall, Autor gegen zweite Person |
| `vergleich_v1_v2.csv` | Stufe je Fall nach v1 und v2 |
| `korrektheit_gesamt.csv`, `korrektheit_nach_fragetyp.csv`, `korrektheit_mit_d.csv`, `korrektheit_je_frage_mit_d.csv` | Anteile vollständig korrekter Antworten (v2) |
| `bootstrap.csv` | alle Vergleiche mit Permutationstest und Bootstrap-Intervall (10.000 Ziehungen) |
| `fehlerdiagnose.csv`, `fehlerprofil.csv` | Befund je Frage aus B/C und Retrieval, Merkmalshäufigkeiten je Bedingung |
| `retrieval_metriken.csv`, `topk_justierung.*`, `segmentierung_pruefung.csv`, `konstruktionsvaliditaet.csv` | Retrieval-Kennzahlen und Kontrollen zu Wissensbasis und Katalog |
| `abschlusspruefung_pruefmodus_2026-09-29.csv`, `versionen_pruefmodus_2026-09-29.csv` | Abschlussprüfung (24 von 24) und Programmversionen des dokumentierten Prüflaufs vom 29.09.2026 auf Stand `b9664aa`, aus der Ausgabe des abgegebenen Notebooks übernommen |
| `abschlusspruefung_datenlauf_2026-09-28.csv` | historisch: Abschlusskontrolle des Datenlaufs vom 28.09.2026 (18 Prüfungen, vor der Überarbeitung) |
| `versionen.csv` | Programmversionen des Datenlaufs vom 28.09.2026 |
| `schema.sql` | optionales Supabase-/pgvector-Schema |
| `ergebnisse.png` | Abbildung 1 |

Der Bogen und der Schlüssel der Bewertung v2 liegen unter `bewertung_v2/`.
