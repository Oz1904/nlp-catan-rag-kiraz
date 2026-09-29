# Einfluss von Retrieval-Augmented Generation auf die Korrektheit deutschsprachiger Spielregelantworten am Beispiel von CATAN

Semesterabschließende Ausarbeitung im Modul **Natural Language Processing (SoSe 2026)**<br>
Fachhochschule Südwestfalen · M.Sc. Angewandte Künstliche Intelligenz

**Autor:** Ozan Kiraz · **Matrikelnummer:** 30500695<br>
**Betreuung:** Prof. Dr. Christian Gawron<br>
**Abgabe:** 29. September 2026 · **Abgabestand:** Branch `abgabe` (nach der Abgabe unverändert)

[![In Colab öffnen](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Oz1904/nlp-catan-rag-kiraz/blob/abgabe/NLP_Hausarbeit_CATAN_RAG.ipynb)

Die Ausarbeitung ist das Notebook `NLP_Hausarbeit_CATAN_RAG.ipynb`. Es enthält Text, Code und alle Ausgaben des Prüflaufs. Dieses README beschreibt nur, wie man die Ergebnisse nachrechnet und was im Repository liegt.

## Für Prüfende: nachrechnen ohne Zugangsdaten

1. Notebook über den Colab-Link oben öffnen.
2. *Laufzeit → Alle ausführen*.

Voreingestellt ist `PRUEFMODUS = True`. Benötigt werden weder API-Schlüssel noch Google Drive noch eine Datenbank, und es entstehen keine Kosten. Eine Internetverbindung ist nötig: Das Notebook klont den Abgabestand (Branch `abgabe`) dieses Repositorys und lädt die Regelhefte von catan.de.

Der Prüflauf macht Folgendes:

- Er baut die Wissensbasis aus den PDFs neu auf.
- Er prüft, ob Katalog, Konfiguration, Prompt- und Suchcode zeichengenau die Prüfsumme des Abgabelaufs ergeben (Hauptversuch und Zusatzversuch D getrennt).
- Er prüft, ob jeder Bewertungsfall genau die protokollierte Antwort zeigt.
- Er berechnet danach die Kennzahlen, Tests, Intervalle und Abbildungen der Auswertung aus den gespeicherten Antworten und Bewertungen neu. Die Top-k-Justierung wird aus der gespeicherten Datei geladen.

Jeder Prüflauf legt in Colab einen eigenen, frischen Klon an und gibt den geprüften Commit aus; ein Ordner aus einem früheren Lauf wird weder verwendet noch verändert. Neu berechnete Dateien landen in `ergebnisse/pruefmodus/`; die abgegebenen Dateien bleiben unverändert.

**Dokumentierter Prüflauf.** Das abgegebene Notebook wurde am 29.09.2026 in einer frischen Colab-Sitzung ohne API-Schlüssel im Prüfmodus vollständig ausgeführt (Zellen 1–33 fortlaufend). Geprüft wurde der Stand `b9664aa` des Branches `abgabe`; 24 von 24 Prüfungen sind bestanden, und die Prüfsummen von Hauptversuch und Zusatzversuch D wurden reproduziert. Der Bericht liegt in `ergebnisse/abschlusspruefung_pruefmodus_2026-09-29.csv`, die Programmversionen des Laufs in `ergebnisse/versionen_pruefmodus_2026-09-29.csv`. Der Abgabe-Commit ändert gegenüber `b9664aa` nur die Ausgaben des Notebooks (Quelltext aller Zellen unverändert), diese beiden Berichtsdateien und die beiden README-Dateien; alle Daten, Bewertungen und der Code sind unverändert. Die Prüfungen kontrollieren Vollständigkeit, Zuordnung und Reproduzierbarkeit, nicht die inhaltliche Richtigkeit der Bewertungen. Die dichte Suche wird nicht wiederholt, weil sie neue Embeddings bräuchte. Die Retrieval-Kennzahlen werden aus den gespeicherten Treffern neu berechnet.

## Ergebnisse in Kurzform

Bewertung v2, 30 Testfragen, Anteil vollständig korrekter Antworten:

| Bedingung | gesamt | Fakten (6) | Ausnahme (12) | Anwendung (12) |
|---|---:|---:|---:|---:|
| **A** ohne Kontext | 16,7 % (5/30) | 16,7 % | 16,7 % | 16,7 % |
| **B** Retrieval, Top-4 | 50,0 % (15/30) | 66,7 % | 50,0 % | 41,7 % |
| **C** Gold-Chunks | 76,7 % (23/30) | 83,3 % | 75,0 % | 75,0 % |
| **D** gesamtes Regelwerk (explorativ) | 66,7 % (20/30) | 100,0 % | 91,7 % | 25,0 % |

- **B gegen A (Hauptvergleich):** +33,3 Prozentpunkte. Der exakte Permutationstest über 13 Regelgruppen ergibt p = 0,016; alle 7 Gruppen mit einem Unterschied sprechen für B. Das 95-%-Intervall des Cluster-Bootstraps reicht von +14,3 bis +54,8. H1 ist für diesen Katalog gestützt, der Nachweis aber knapp: Ein einzelnes umgekehrtes Urteil kann ihn über die Schwelle heben.
- **Nicht nachweisbar** sind C gegen B (+26,7; p = 0,094), D gegen B (+16,7; p = 0,367), D gegen C (−10,0; p = 0,453) und alle Zugewinne je Fragetyp. Ob sich die Zugewinne der Fragetypen voneinander unterscheiden, wurde nicht direkt getestet; die von H2 erwartete Reihenfolge zeigt sich in den Punktschätzungen nicht.
- **Beschreibend:** Mit Kontext wurden deutlich weniger Antworten mit erfundenen oder übertragenen Grundspielregeln annotiert; Selbstwidersprüche und, nach den Notizen, Rechenfehler bei Anwendungsfragen traten auch mit Kontext auf. Mit dem gesamten Regelwerk (D) sind nur 3 von 12 Anwendungsfragen vollständig korrekt. Die Fehlerkategorien R und Z grenzt eine zweite Person anders ab; die Fehleranalyse ist beobachtend.
- **Retrieval:** BM25 mit Stammformen oder Zeichen-4-Grammen findet die Belege auf den Testfragen mindestens so oft wie die verwendete dichte Suche.
- **Bewertung v1 gegen v2:** binär 89 von 90 Urteilen gleich (κ = 0,978).
- **Zweitbewertung v2:** Eine zweite Person hat 40 der 120 Fälle verblindet nach derselben Rubrik bewertet. Binär sind 38 von 40 Urteilen gleich (κ = 0,899). Beide Abweichungen betreffen B, beide zugunsten von B. Die Merkmale R und Z ordnen beide Personen verschieden zu (je 67,5 % gleich).

Einordnung und Grenzen stehen in den Kapiteln 11 und 12 des Notebooks.

## Versuchsaufbau

Dasselbe Modell (`gpt-4.1-mini-2025-04-14`, Temperatur 0) beantwortet 30 Testfragen zu *CATAN* und *CATAN – Städte & Ritter* (Ausgabe 2025) unter vier Bedingungen, die sich nur im Kontext unterscheiden:

| Bedingung | Kontext |
|---|---|
| **A** | kein Regeltext |
| **B** | vier abgerufene Abschnitte (dichte Suche mit `text-embedding-3-small`, Anwendbarkeitsfilter) |
| **C** | die Abschnitte mit den annotierten Schlüsselzitaten (Gold-Chunks) |
| **D** | alle für die Spielvariante zulässigen Abschnitte, je nach Variante rund 5.100 bis 16.300 Tokens; nachträglich ergänzt, explorativ |

Der Katalog umfasst 6 Entwicklungs- und 30 Testfragen in 19 getrennten Regelgruppen. Die Testfragen verteilen sich auf 6 Fakten-, 12 Ausnahme- und 12 Anwendungsfragen. Bewertet wird der Anteil vollständig korrekter Antworten gegen vorab festgelegte Pflichtaussagen und Fehlerkriterien. Die Unsicherheit bestimmen ein exakter Permutationstest und ein Cluster-Bootstrap auf Ebene der 13 Test-Regelgruppen.

## Bewertung v1 und v2

Die erste Bewertung (v1) der 90 Antworten aus A, B und C enthielt dokumentierte Inkonsistenzen. Alle 120 Antworten aus A bis D wurden deshalb nach einer vorab eingefrorenen, geschärften Rubrik neu bewertet (v2). Dabei werden nur Merkmale erfasst; die Stufe berechnet der Code. Grundlage der Ergebnisse ist v2, v1 wird vollständig zum Vergleich berichtet. Einzelheiten stehen in `bewertung_v2/RUBRIK.md` und in Abschnitt 5.3 des Notebooks.

## Was im Repository liegt

```
├── NLP_Hausarbeit_CATAN_RAG.ipynb   Ausarbeitung, im Prüfmodus ausgeführt (maßgebliche Fassung)
├── endlauf_2026-09-28.ipynb         Laufbeleg des Hauptversuchs, unverändert: erneute Suche, die 108
│                                    protokollierten Antworten (erzeugt am 24.09.2026). Text und
│                                    Auswertung dort auf damaligem Stand (Bewertung v1)
├── zusatz_d_lauf_2026-09-29.ipynb   Laufbeleg von Bedingung D, unverändert: Erzeugung der 30 Antworten.
│                                    Text und Auswertung dort auf damaligem Stand
├── bewertung_v2/
│   ├── RUBRIK.md                    eingefrorene Rubrik v2 und vorab festgelegte Auswertung
│   ├── stufe.py                     Regel Merkmale → Stufe
│   ├── erzeuge_bogen.py, baue_seite.py, bewertung_template.html, bewertung_v2.html
│   │                                Bogen und Bewertungswerkzeug
│   ├── exportiere.py                Export des Werkzeugs → ergebnisse/bewertung_v2.csv
│   ├── bogen_v2.json                120 verblindete Fälle
│   ├── schluessel_v2.csv            Zuordnung Fall → Frage, Bedingung
│   └── zweitbewertung/              Zweitbewertung v2: vorab festgelegtes Vorgehen (README.md),
│                                    Stichprobe (auswahl_zweit.csv, bogen_zweit.json, ziehe_stichprobe.py),
│                                    Offline-Werkzeug (CATAN_Zweitbewertung.html, zweitbewertung_template.html)
├── ergebnisse/
│   ├── versuchsplan.json            eingefrorene Konfiguration, Prüfsumme 2577d51e…
│   ├── laufprotokoll.jsonl          jede Modellantwort A–C mit Kontext-IDs, Tokens, Modellversion
│   ├── zusatz_d/                    Versuchsplan und Laufprotokoll von D
│   ├── bewertungen.csv, bewertung_schluessel.csv, bewertungen_zweitperson.csv
│   │                                Bewertung v1 und Zweitbewertung
│   ├── bewertung_v2.csv             Bewertung v2 (Merkmale je Fall)
│   ├── zweitbewertung_v2.csv, zweitbewertung_v2_vergleich.csv
│   │                                Zweitbewertung v2 (40 Fälle) und Vergleich mit v2
│   ├── vergleich_v1_v2.csv          v1 gegen v2 je Fall
│   ├── bootstrap.csv                Tests und Intervalle aller Vergleiche
│   ├── korrektheit_*.csv, fehlerdiagnose.csv, fehlerprofil.csv, retrieval_metriken.csv
│   ├── abschlusspruefung_*.csv, versionen*.csv   Prüfberichte und Programmversionen
│   └── *.png                        Abbildungen
└── quellen/README.md                Bezugsquelle und Prüfsummen der Regelhefte (PDFs nicht enthalten)
```

Nicht enthalten sind die Regelhefte, die extrahierten Volltexte und eine gefüllte Datenbank (Urheberrecht, © KOSMOS). Das Notebook lädt die Hefte von der offiziellen Seite und prüft ihre SHA-256-Prüfsummen.

## Betriebsarten

| Einstellung | Wirkung | Voraussetzung |
|---|---|---|
| `PRUEFMODUS = True` (Voreinstellung) | gespeicherte Ergebnisse prüfen und die Kennzahlen der Auswertung neu berechnen | Internet |
| `PRUEFMODUS = False`, `ENDLAUF = True` | Datenlauf: Suche neu ausführen, gespeicherte Antworten zur selben Prüfsumme wiederverwenden, fehlende erzeugen | `OPENAI_API_KEY` in den Colab-Secrets |
| `PRUEFMODUS = False`, `ENDLAUF = False` | Entwicklungsphase, nur die sechs Entwicklungsfragen | `OPENAI_API_KEY` |
| `ZUSATZ_D_ERZEUGEN = True` (Abschnitt 9.2) | erzeugt die D-Antworten, falls sie fehlen | `OPENAI_API_KEY` |

`ABLAGE` wählt den Arbeitsordner: `"github"` (Repository-Klon in der Sitzung, Voreinstellung), `"drive"` oder `"colab"`. Jede Antwort wird sofort ins Laufprotokoll geschrieben; ein abgebrochener Lauf setzt beim nächsten Start fort. Der Supabase-Pfad (`ergebnisse/schema.sql`) ist optional und wurde in den dokumentierten Läufen nicht verwendet. Ein kompletter Datenlauf kostet einige Cent.

## Änderungen vor dem Einfrieren des Hauptversuchs

| Bereich | Änderung |
|---|---|
| Belegkontext | C erhält Gold-Chunks statt vollständiger Belegseiten. |
| Katalog | Vorgaben zu Spielvarianten und geschlossenen Fragen ergänzt; bei E03 eine fehlende Teilfrage ergänzt; bei E04 eine nicht gefragte Pflichtaussage entfernt; bei T01/T02 Schlüsselzitate ergänzt; bei T16 ein nicht belegtes Fehlerkriterium gestrichen. |
| Retrieval-Metriken | Precision, Recall und F1 einheitlich auf Chunk-Ebene. |
| Textextraktion | Steuerzeichen aus PDF-Symbolen entfernt. |
| Verblindung | Quellenkennungen werden ersatzlos entfernt. |

## Änderungen nach dem Endlauf (29.09.2026)

- Zusatzversuch D mit eigener Prüfsumme; Hauptversuch unverändert.
- Neubewertung v2 aller 120 Antworten nach eingefrorener Rubrik.
- Nachweisaussagen stützen sich auf den exakten Permutationstest; Bootstrap mit 10.000 statt 2.000 Ziehungen, nur beschreibend.
- Text gekürzt und neu gegliedert; verwandte Arbeiten [19, 20] ergänzt.

Nachträglich ergänzt und als explorativ gekennzeichnet sind außerdem der BM25-Vergleich (Abschnitt 8.2) und der Kipppunkt (Abschnitt 11.2).

## Einsatz von KI-Werkzeugen

Eingesetzt wurden Claude (Anthropic) und ChatGPT (OpenAI). Claude in erheblichem Umfang: für Versuchsdesign und Code, für alle Fragen und Bewertungskriterien als Entwürfe, für den Text und für die Überarbeitung am 29.09.2026. ChatGPT zur kritischen Begutachtung von Zwischenständen; übernommene Hinweise wurden mit Claude umgesetzt. Die Bewertungen v1 und v2 stammen vom Autor, die Zweitbewertungen von einer zweiten Person ohne KI-Werkzeug. Die Aufschlüsselung nach Arbeitsschritten steht in Kapitel 13 des Notebooks.
