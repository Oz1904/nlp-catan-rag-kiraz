# CATAN: Retrieval-Augmented Generation bei deutschsprachigen Regelfragen

NLP-Hausarbeit, FH Südwestfalen · M.Sc. Angewandte Künstliche Intelligenz

Autor: Ozan Kiraz · Betreuung: Prof. Dr. Christian Gawron  
Abgabe: **28. September 2026** · Matrikelnummer: noch einzutragen

[Notebook in Colab öffnen](https://colab.research.google.com/github/Oz1904/nlp-catan-rag-kiraz/blob/main/4_NLP_Hausarbeit_CATAN_RAG.ipynb)

## Aktueller Stand

Dies ist ein **Entwicklungsstand**, keine abgeschlossene Teststudie:

- sechs Entwicklungsfragen und 18 erfolgreiche Antworten (A/B/C);
- null eingetragene menschliche Bewertungen;
- noch keine Testfragen, endgültigen Korrektheitswerte oder Bootstrap-Ergebnisse.

Die fachliche Prüfung und Freigabe der Referenzantworten sowie die menschliche
Bewertung bleiben erforderlich. Die bisherige KI-Prüfung ist keine unabhängige
menschliche Zweitbewertung. Fragenherkunft wird im Notebook dokumentiert.

## Für Prüfende: ohne persönliche Zugänge

1. Notebook über den Colab-Link öffnen oder das Repository herunterladen und das
   Notebook in Jupyter öffnen.
2. `PRUEFMODUS = True` beibehalten (Standard).
3. **Alle ausführen** wählen.

Der Prüfmodus benötigt weder Drive noch PDFs, Supabase, OpenAI-Schlüssel, GPU oder
zusätzliche Python-Pakete. Er verwendet ausschließlich die Python-Standardbibliothek.
Mit einem lokalen `ergebnisse/`-Ordner funktioniert er offline. Ohne diesen Ordner
lädt er die benötigten Ergebnisdateien aus einem festgelegten GitHub-Commit; dann
ist eine Internetverbindung erforderlich.

Geprüft werden Dateihashes, die Lauf-Prüfsumme, vollständige Frage-Bedingungs-Paare
und die Übereinstimmung aller Antworttexte zwischen Protokoll und Bewertungsbogen.
Retrieval-Mittelwerte werden aus den gespeicherten Einzelwerten neu berechnet.
Die Prüfung berechnet keine Embeddings und wiederholt nicht die Suche.
Eine fachliche Quellenprüfung erfordert zusätzlich die Originalhefte.

Der aktuelle Prüf-Snapshot bezieht sich auf Commit
`b13d2c9cf808dd0d9518fca6a8f9a5ee6013b010` und Lauf
`600302a0f540367c33f61f00e4db08519cffc6d3b9404a1ff0384f641c05adaf`.
Geänderte Dateien führen absichtlich zu einem Hash-Fehler. Nach abgeschlossener
Bewertung muss ein neuer, gemeinsam versionierter Prüf-Snapshot erstellt werden.
Eine alternative Bewertung darf nicht unbemerkt an die Stelle der Abgabe treten.

Alle gespeicherten Ausgaben der neuen Notebook-Fassung stammen aus dem lokalen
Prüflauf. Historische experimentelle Ausgaben stehen in der Git-Vorgängerversion.

## Forschungsfrage und Versuchsbedingungen

Wie verändert automatisch bereitgestellter Regeltext die Korrektheit desselben
Sprachmodells bei Fakten-, Ausnahme- und Anwendungsfragen zu CATAN?

| Bedingung | Kontext |
|---|---|
| A | Kein Regeltext |
| B | Automatisch abgerufene Regel-Chunks |
| C | Anhand annotierter Belegzitate ausgewählte Gold-Chunks |

C dient der Diagnose, ist keine garantierte Obergrenze und beweist keine
Fehlerursache. Modell: `gpt-4.1-mini-2025-04-14`; Embeddings:
`text-embedding-3-small`; aktuell Top-k = 4.

Retrieval-Precision, Recall und F1 beziehen sich in der aktuellen Fassung auf
Gold-Chunks; der Zitat-Recall wird zusätzlich ausgewiesen. Primäre Antwortkennzahl
ist der Anteil vollständig korrekter Antworten nach Fragetyp. Unterschiede
zwischen verwandten Fragen werden im geplanten Cluster-Bootstrap berücksichtigt.
Die Studie ist nicht für einen zuverlässigen Nachweis kleiner Effekte ausgelegt;
eine feste Prozentpunkte-Nachweisgrenze wird nicht behauptet.

## Vorhandene Dateien

| Datei | Inhalt |
|---|---|
| `4_NLP_Hausarbeit_CATAN_RAG.ipynb` | Ausarbeitung, Prüfmodus und experimenteller Code |
| `ergebnisse/versuchsplan.json` | Vorläufiger Entwicklungsplan mit Lauf-Prüfsumme |
| `ergebnisse/laufprotokoll.jsonl` | Zwei Entwicklungsdurchläufe mit jeweils 18 Antworten |
| `ergebnisse/bewertungen.csv` | Aktuelle Antworten und noch leere Bewertungsfelder |
| `ergebnisse/bewertung_schluessel.csv` | Fall-ID, Frage, Bedingung und Prüfsumme |
| `ergebnisse/retrieval_metriken.csv` | Einzelwerte der sechs Entwicklungsfragen |
| `ergebnisse/topk_justierung.csv`, `.png` | Entwicklungsauswertung unterschiedlicher k-Werte |
| `ergebnisse/segmentierung_pruefung.csv` | Fundstellen der Belegzitate |
| `ergebnisse/konstruktionsvaliditaet.csv` | Sprachliche Überschneidung mit Belegtexten |
| `ergebnisse/quellenmanifest.csv` | URLs und SHA-256 der Hefte; Abrufdaten noch offen |
| `ergebnisse/schema.sql` | Supabase-/pgvector-Schema |
| `ergebnisse/versionen.csv` | Protokollierte Softwarestände |
| `ergebnisse/abschlusspruefung.csv` | Historischer Abschlusscheck des Entwicklungslaufs |
| `ergebnisse/*_archiv_*.csv` | Älterer Bewertungsstand; nicht mit aktuellen Fällen mischen |

Die Abschlussprüfung aus CSV ist ein historisches Artefakt; sie wird durch den
Prüfmodus nicht überschrieben. Endgültige Testmetriken und Bootstrap-Dateien
existieren noch nicht. Literatur und Quellenbelege stehen im Notebook.

## Neues Experiment mit eigenen Zugängen

Für den experimentellen Weg `PRUEFMODUS = False` setzen, die Laufzeit neu starten
und das Notebook ausführen. Dieser Weg installiert Pakete und verwendet die
bisherige Colab-/Drive-Arbeitsablage `Meine Ablage/NLP_CATAN/`.
`ENDLAUF = False` bleibt bis zur Freigabe des Testkatalogs bestehen.

- OpenAI-Schlüssel in Colab-Secrets als `OPENAI_API_KEY` hinterlegen.
- Die Originalhefte werden nach Möglichkeit von den Manifest-URLs geladen und
  anhand ihrer SHA-256 geprüft; alternativ ist manueller Upload vorgesehen.
- Für Supabase `schema.sql` im eigenen Projekt ausführen und `SUPABASE_URL` sowie
  `SUPABASE_KEY` als Secrets hinterlegen.

**Noch offene Implementierung:** B verwendet derzeit weiterhin den lokalen
Suchpfad. Supabase als verbindlicher Hauptweg und der strenge Konsistenztest
beider Suchpfade sind vor dem Endlauf fertigzustellen. Dieser README-Stand
behauptet dafür keine bereits nachgewiesene Gleichwertigkeit.

Ein neuer Modelllauf erzeugt kostenpflichtige API-Aufrufe. Bei gleicher
Lauf-Prüfsumme nutzt das vorhandene Wiederaufnahmeverfahren gespeicherte Antworten.
Für neue Experimente eine getrennte Arbeitskopie/Arbeitsablage verwenden und die
abgegebenen Ergebnisdateien erhalten.

## Quellen und Veröffentlichung

Verwendet werden die offiziellen Regelhefte zum Grundspiel (Art.-Nr. 684655)
und Städte & Ritter (Art.-Nr. 684754), Ausgabe mit Impressum 2025.

Entsprechend der Projektfestlegung werden **keine PDFs, extrahierten Volltexte,
gefüllten Vektorindizes oder persönlichen Zugangsschlüssel** veröffentlicht.
Bezugsquellen und Prüfsummen stehen im Quellenmanifest. Ergebnisse enthalten
Modellantworten, eigene Annotationen und kurze Belegzitate.

## Noch vor der Abgabe

- Bewertungsregeln abschließen und Entwicklungsantworten menschlich bewerten.
- Testkatalog fachlich freigeben (Ziel 30, mindestens 25 Fragen).
- Testschutz, Quellenumfang und Supabase-Hauptweg abschließend prüfen.
- Zweitbewertung vorab organisieren und Protokoll einfrieren.
- Testlauf, verblindete Bewertung, Auswertung und eigene Diskussion abschließen.
- Abrufdaten, Matrikelnummer und KI-Erklärung vervollständigen; Textumfang prüfen.
- Prüf-Snapshot auf den endgültigen Datenstand aktualisieren und ohne persönliche
  Zugänge erneut vollständig ausführen.
