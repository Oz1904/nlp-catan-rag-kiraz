# Einfluss von Retrieval-Augmented Generation auf die Korrektheit deutschsprachiger Spielregelantworten am Beispiel von CATAN

Semesterabschließende Ausarbeitung im Modul **Natural Language Processing (SoSe 2026)**
Fachhochschule Südwestfalen · M.Sc. Angewandte Künstliche Intelligenz

**Autor:** Ozan Kiraz · **Matrikelnummer:** _eintragen_
**Betreuung:** Prof. Dr. Christian Gawron
**Abgabe:** 29. September 2026

[![In Colab öffnen](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fhswf/<REPOSITORY-NAME>/blob/main/NLP_Hausarbeit_CATAN_RAG.ipynb)

---

## Worum es geht

Sprachmodelle beantworten Fragen zu populären Gesellschaftsspielen flüssig, aber nicht immer regelkonform. Besonders fehleranfällig sind Fälle, in denen eine Erweiterung Regeln des Grundspiels **ersetzt** statt sie zu ergänzen — bei *CATAN – Städte & Ritter* betrifft das unter anderem die Siegpunktschwelle, die Sondersiegpunkttafeln, die Gründungsphase und die Entwicklungskarten.

**Forschungsfrage:** Wie verändert die automatische Bereitstellung relevanter Regelabschnitte aus den offiziellen Regelheften die Korrektheit der Antworten desselben Sprachmodells bei Fakten-, Ausnahme- und Anwendungsfragen?

**Diagnostische Zusatzfrage:** Welche Fehler bleiben bestehen, wenn dem Modell alle erforderlichen Belegstellen manuell bereitgestellt werden?

## Versuchsaufbau

Drei Bedingungen desselben Modells, identisch in Modellversion, Generierungseinstellungen, Instruktion und Antwortformat — verschieden ausschließlich im Kontext:

| Bedingung | Kontext | Funktion |
|---|---|---|
| **A** | kein Regeltext | Was leistet das parametrische Modellwissen allein? |
| **B** | automatisch abgerufene Abschnitte (Top-k) | das eigentliche RAG-System |
| **C** | alle annotierten Belegstellen | Diagnose: Was bleibt bei perfektem Retrieval falsch? |

Bedingung C ist eine Diagnose, **keine** garantierte Obergrenze.

## Auswertung auf zwei Ebenen

**Retrieval.** Precision@k, Recall@k und F1 gegen die annotierten Belegstellen. Ein Treffer gilt als relevant, wenn er von einer Belegseite stammt. Zusätzlich Hit@k, der Anteil vollständig gefundener Belege und der Zitat-Recall (wurde der Chunk mit der entscheidenden Aussage gefunden?).

**Antwortkorrektheit.** Anteil vollständig korrekter Antworten, verblindet bewertet gegen vorab festgelegte zwingende Aussagen und Fehlerkriterien. Unsicherheit über einen gepaarten **Cluster-Bootstrap auf Regelgruppenebene**, da Fragen derselben Regelgruppe inhaltlich abhängig sind.

## Was in diesem Repository liegt

```
├── NLP_Hausarbeit_CATAN_RAG.ipynb   Ausarbeitung mit allen Zellausgaben des dokumentierten Laufs
├── README.md
├── quellen/
│   └── README.md                    Bezugsquelle und Prüfsummen der Regelhefte (PDFs selbst nicht enthalten)
└── ergebnisse/                      vom Notebook erzeugt
    ├── quellenmanifest.csv          URL, Abrufdatum, SHA-256 je PDF-Fassung
    ├── versuchsplan.json            eingefrorene Konfiguration mit Prüfsumme
    ├── schema.sql                   Supabase-/pgvector-Schema inkl. Suchfunktion match_chunks
    ├── laufprotokoll.jsonl          jede Modellantwort mit Kontext-IDs, Tokens, Modellversion
    ├── bewertungen.csv              verblindeter Bewertungsbogen (ausgefüllt)
    ├── bewertung_schluessel.csv     Zuordnung Fall → Bedingung
    ├── retrieval_metriken.csv       Precision@k, Recall@k, F1, Hit@k, Zitat-Recall je Frage
    ├── korrektheit_*.csv            Korrektheit gesamt und je Fragetyp
    ├── bootstrap.csv                Cluster-Bootstrap mit 95-%-Intervallen
    ├── fehlerdiagnose.csv           Retrieval- vs. Generierungsfehler
    └── *.png                        Abbildungen
```

Die Ordnerstruktur entspricht dem Arbeitsordner `NLP_CATAN` in Google Drive — ohne die PDFs.

**Nicht im Repository:** die Original-PDFs, die extrahierten Volltexte und die gefüllte Wissensdatenbank. Das Notebook zeigt aus den Regelheften nur kurze Auszüge und Schlüsselzitate mit Seitenangabe.

## Urheberrecht

Beide Regelhefte sind urheberrechtlich geschützt (© KOSMOS). Ein öffentlicher Download begründet kein Recht zur Weiterveröffentlichung. Im Repository liegen deshalb nur das Quellenmanifest und der Code zur Wiederherstellung; in der Auswertung werden kurze Belegzitate mit Seitenangabe im Rahmen des Zitatrechts verwendet.

| Dokument | Artikelnummer | Seiten | Impressum |
|---|---|---:|---|
| CATAN – Das Spiel | 684655 | 12 | © 1995, 2025 KOSMOS |
| CATAN – Städte & Ritter | 684754 | 16 | © 1998, 2025 KOSMOS |

## Ausführung

Das Notebook ist für Google Colab ausgelegt und trainiert kein Modell — eine GPU wird nicht benötigt.

1. Original-PDFs gemäß Quellenmanifest herunterladen und in Google Drive unter `Meine Ablage/NLP_CATAN/quellen/` ablegen. Der Dateiname ist egal: Das Notebook erkennt die Hefte an Artikelnummer bzw. Inhalt und vergleicht die SHA-256-Prüfsumme mit der dokumentierten Fassung. Fehlt ein Heft, öffnet sich ein Upload-Dialog.
2. In Colab unter *Secrets* (Schlüsselsymbol) `OPENAI_API_KEY` anlegen und den Notebook-Zugriff aktivieren; optional `SUPABASE_URL` und `SUPABASE_KEY`.
3. *Laufzeit → Alle ausführen* und den Zugriff auf Google Drive bestätigen.

Alle Ergebnisse landen in `Meine Ablage/NLP_CATAN/ergebnisse/` und überstehen einen Neustart der Laufzeit; der Durchlauf setzt nach einem Abbruch an der richtigen Stelle fort.

**Supabase (optional).** Das SQL aus `ergebnisse/schema.sql` einmalig im SQL-Editor des Supabase-Projekts ausführen. Das Notebook schreibt die Chunks samt Vektoren in die Datenbank und prüft per Konsistenztest, dass Supabase dieselben Treffer liefert wie der lokale Pfad. Ohne Zugangsdaten läuft alles lokal. Schlüssel stehen weder im Notebook noch im Repository.

**Phasen.** Solange `ENDLAUF = False` gilt, stellt das Notebook nur die Entwicklungsfragen. Nach Fertigstellung und Prüfung des Katalogs wird `ENDLAUF = True` gesetzt; ausgewertet werden dann ausschließlich die Testfragen.

**Laufzeit und Kosten.** Die Laufzeit wird von den API-Aufrufen bestimmt. Die Indexierung der beiden Hefte kostet mit `text-embedding-3-small` (0,02 USD je 1 Mio. Tokens) weniger als einen Cent. Der vollständige A/B/C-Durchlauf liegt bei rund 120 Aufrufen (etwa 40 Fragen × 3 Bedingungen); das eingeplante Budget beträgt 10–20 USD.

## Reproduktion in drei Stufen

1. **Ergebnisse prüfen** — Notebook mit gespeicherten Ausgaben lesen. Kein API-Zugang nötig.
2. **Wissensbasis neu aufbauen** — PDFs, Manifest und Extraktionscode. Kein API-Zugang für die Extraktion nötig, für die Indexierung schon.
3. **Neue Fragen stellen** — eigener API-Schlüssel und Supabase-Instanz oder lokaler Suchpfad.

## Bewusste Einschränkungen

- **Vorwissen des Modells.** CATAN ist in Trainingsdaten stark vertreten. Bedingung A misst „Modell mit unkontrolliertem Vorwissen unbekannter Editionsaktualität", nicht „Modell ohne Wissen". Bei Faktenfragen ist deshalb nur ein geringer Effekt zu erwarten.
- **Ungleiche Fragetypverteilung.** Ausnahme- und Anwendungsfragen sind bewusst übergewichtet. Ergebnisse werden primär je Fragetyp berichtet; der gepoolte Wert ist keine „typische Leistung".
- **Statistische Aussagekraft.** Bei diesem Katalogumfang liegt die praktische Nachweisgrenze bei etwa 20–25 Prozentpunkten. Die Studie ist nicht darauf ausgelegt, kleine oder moderate Effekte nachzuweisen. Der Katalog wird nicht vergrößert, um Signifikanz zu erreichen.
- **Ein Durchlauf je Frage und Bedingung.** Die Varianz wiederholter Generierungen wird nicht geschätzt.
- **Bewertung.** Falls keine Zweitbewertung vorliegt, wird das als Einschränkung offengelegt.
- **Bedingung C** ist eine Diagnose, keine Obergrenze. „B falsch, C richtig" ist ein Hinweis auf ein Retrievalproblem, keine bewiesene Ursache.

## Literatur

1. Lewis, P. et al. (2020): *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 33. https://arxiv.org/abs/2005.11401
2. *Retrieval-Augmented Generation for Natural Language Processing: A Survey.* arXiv:2407.13193
3. Es, S. et al. (2024): *RAGAS: Automated Evaluation of Retrieval Augmented Generation.* EACL 2024 (Demos). https://arxiv.org/abs/2309.15217
4. Karpukhin, V. et al. (2020): *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. https://arxiv.org/abs/2004.04906
5. Möller, T.; Risch, J.; Pietsch, M. (2021): *GermanQuAD and GermanDPR.* MRQA 2021. https://aclanthology.org/2021.mrqa-1.4/
6. Efron, B.; Tibshirani, R. J. (1993): *An Introduction to the Bootstrap.* Chapman & Hall/CRC.

Die vollständige Quellenliste steht im Notebook.

## Einsatz von KI-Werkzeugen

Sprachmodelle wurden als Werkzeug bei Codeentwurf und sprachlicher Überarbeitung eingesetzt. Die fachliche Prüfung sämtlicher Referenzantworten und Belegstellen sowie die Bewertung der Modellantworten erfolgten manuell durch den Autor. _Ausgestaltung an die Vorgaben der Hochschule anpassen._
