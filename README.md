# Einfluss von Retrieval-Augmented Generation auf die Korrektheit deutschsprachiger Spielregelantworten am Beispiel von CATAN

Semesterabschließende Ausarbeitung im Modul **Natural Language Processing (SoSe 2026)**
Fachhochschule Südwestfalen · M.Sc. Angewandte Künstliche Intelligenz

**Autor:** Ozan Kiraz · **Matrikelnummer:** 30500695
**Betreuung:** Prof. Dr. Christian Gawron
**Abgabe:** 29. September 2026

[![In Colab öffnen](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Oz1904/nlp-catan-rag-kiraz/blob/main/NLP_Hausarbeit_CATAN_RAG.ipynb)

---

## Für Prüfende: Ergebnisse nachrechnen, ohne Zugangsdaten

Alles, was zur Bewertung nötig ist, liegt in diesem Repository. Es wird **kein** API-Schlüssel, **kein** Google Drive und **keine** Datenbank benötigt.

1. [Notebook in Colab öffnen](https://colab.research.google.com/github/Oz1904/nlp-catan-rag-kiraz/blob/main/NLP_Hausarbeit_CATAN_RAG.ipynb)
2. *Laufzeit → Alle ausführen*

Die Abgabefassung startet mit `PRUEFMODUS = True`; es ist nichts umzustellen. Das Notebook klont dieses Repository, lädt die beiden Regelhefte von der offiziellen Downloadseite, baut die Wissensbasis daraus neu auf und prüft, ob Fragenkatalog, Regelgruppen, Prompt- und Retrieval-Code **zeichengenau die Prüfsumme des Abgabelaufs** ergeben. Anschließend rechnet es Korrektheitsanteile, Bootstrap-Intervalle, Fehlerdiagnose und Abbildungen aus den gespeicherten Antworten und Bewertungen neu. Es entstehen keine Modellantworten und keine Kosten.

Neu berechnete Dateien schreibt der Prüfmodus in den Unterordner `ergebnisse/pruefmodus/`. Die abgegebenen Ergebnisdateien bleiben dabei unverändert; passen gespeicherte Bewertungen und Katalog nicht zusammen, bricht der Lauf mit einer Begründung ab, statt Dateien zu überschreiben.

Wer nur lesen möchte: Beide Notebooks im Repository enthalten alle Zellausgaben des jeweiligen Laufs, auch ohne Ausführung.

Voraussetzung bleibt eine Python-Umgebung mit Internetzugang — „ohne API-Zugang" heißt nicht „offline". Die Regelhefte werden zur Laufzeit von catan.de geladen.

## Ergebnisse in Kurzform

Über 30 Testfragen, jede in drei Bedingungen, 90 einzeln bewertete Antworten:

| Bedingung | Kontext | vollständig korrekt |
|---|---|---:|
| **A** | kein Regeltext | 16,7 % (5/30) |
| **B** | automatisch abgerufene Abschnitte (Top-k, k = 4) | 50,0 % (15/30) |
| **C** | Chunks mit den annotierten Schlüsselzitaten | 73,3 % (22/30) |

B gegen A: **+33,3 Prozentpunkte**, 95-%-Intervall des gepaarten Cluster-Bootstraps über 13 Regelgruppen **+14,3 bis +54,5**. C gegen B: +23,3 Punkte [+2,9; +46,2].

Der aufschlussreichere Befund steht in der Fehlerverteilung: Erfundene Regeln gehen von 19 über 8 auf 4 Nennungen zurück, fälschlich übertragene Grundspielregeln von 6 über 1 auf 0 — **interne Widersprüche bleiben** (5 / 7 / 4) und machen mit bereitgestelltem Kontext rund die Hälfte der verbleibenden Fehler aus. Acht Fragen bleiben auch mit perfekt ausgewählten Belegen falsch, bei zwei verschlechtert der Belegkontext eine zuvor korrekte Antwort.

Einordnung, Grenzen und die nicht gestützte Hypothese H2 stehen in Kapitel 11 und 12 des Notebooks.

## Worum es geht

Sprachmodelle beantworten Fragen zu populären Gesellschaftsspielen flüssig, aber nicht immer regelkonform. Besonders fehleranfällig sind Fälle, in denen eine Erweiterung Regeln des Grundspiels **ersetzt** statt sie zu ergänzen — bei *CATAN – Städte & Ritter* betrifft das unter anderem die Siegpunktschwelle, die Sondersiegpunkttafeln, die Gründungsphase und die Entwicklungskarten.

**Forschungsfrage:** Wie verändert die automatische Bereitstellung relevanter Regelabschnitte aus den offiziellen Regelheften die Korrektheit der Antworten desselben Sprachmodells bei Fakten-, Ausnahme- und Anwendungsfragen?

**Diagnostische Zusatzfrage:** Welche Fehler bleiben bestehen, wenn dem Modell alle erforderlichen Belegstellen manuell bereitgestellt werden?

## Versuchsaufbau

Drei Bedingungen desselben Modells (`gpt-4.1-mini-2025-04-14`, Temperatur 0), identisch in Modellversion, Generierungseinstellungen, Instruktion und Antwortformat — verschieden ausschließlich im Kontext:

| Bedingung | Kontext | Funktion |
|---|---|---|
| **A** | kein Regeltext | Was leistet das parametrische Modellwissen allein? |
| **B** | automatisch abgerufene Abschnitte (Top-k) | das eigentliche RAG-System |
| **C** | die Chunks mit den annotierten Schlüsselzitaten (Gold-Chunks) | Diagnose: Was bleibt bei perfektem Retrieval falsch? |

Bedingung C erhält die Chunks mit den Schlüsselzitaten, nicht die vollständigen Belegseiten. Sie ist eine Diagnose, **keine** garantierte Obergrenze: Zusätzlicher Kontext kann auch ablenken.

36 Fragen in 13 Regelgruppen, davon 6 Entwicklungsfragen für die Kalibrierung und 30 Testfragen. Die Entwicklungsfragen gehen in keine berichtete Kennzahl ein.

## Auswertung auf zwei Ebenen

**Retrieval.** Precision@k, Recall@k und F1 gegen die annotierten Belegstellen, dazu Hit@k, der Anteil vollständig gefundener Belege und der Zitat-Recall.

**Antwortkorrektheit.** Anteil vollständig korrekter Antworten, verblindet bewertet gegen vorab festgelegte zwingende Aussagen und Fehlerkriterien. Unsicherheit über einen gepaarten **Cluster-Bootstrap auf Regelgruppenebene**, da Fragen derselben Regelgruppe inhaltlich abhängig sind. Der zusätzlich berichtete Vorzeichentest setzt unabhängige Paare voraus und wird deshalb nur ergänzend genannt; maßgeblich ist der Bootstrap.

**Zweitbewertung.** 30 Fälle wurden von einer zweiten Person handschriftlich bewertet (Übereinstimmung 96,7 %, Cohens κ = 0,933 binär). Dieser Wert ist **kein** Nachweis unabhängiger Bewerterzuverlässigkeit — die Einschränkungen stehen in Abschnitt 12.4 des Notebooks und betreffen unter anderem, dass die Fehlerarten nur von einer Person vergeben wurden.

## Was in diesem Repository liegt

```
├── NLP_Hausarbeit_CATAN_RAG.ipynb   Abgabefassung, im Prüfmodus ausgeführt, mit allen Zellausgaben
├── endlauf_2026-09-27.ipynb         derselbe Code im Datenlauf ausgeführt: 108 Modellaufrufe,
│                                    Tokenzahlen, Laufzeit, bestätigte Modellversion
├── README.md
├── quellen/
│   └── README.md                    Bezugsquelle und Prüfsummen der Regelhefte (PDFs nicht enthalten)
└── ergebnisse/                      vom Notebook erzeugt, siehe ergebnisse/README.md
    ├── versuchsplan.json            eingefrorene Konfiguration mit Prüfsumme 2577d51e…
    ├── quellenmanifest.csv          URL, Abrufdatum, SHA-256 je PDF-Fassung
    ├── laufprotokoll.jsonl          jede Modellantwort mit Kontext-IDs, Tokens, Modellversion
    ├── bewertungen.csv              verblindeter Bewertungsbogen (ausgefüllt)
    ├── bewertung_schluessel.csv     Zuordnung Fall → Bedingung, getrennt vom Bogen
    ├── bewertungen_zweitperson.csv  Zweitbewertung von 30 Fällen
    ├── retrieval_metriken.csv       Precision@k, Recall@k, F1, Hit@k, Zitat-Recall je Frage
    ├── korrektheit_*.csv            Korrektheit gesamt und je Fragetyp
    ├── bootstrap.csv                Cluster-Bootstrap, gesamt und je Fragetyp
    ├── fehlerdiagnose.csv           Befundzuordnung je Frage aus dem A/B/C-Vergleich
    ├── abschlusspruefung.csv        Ergebnis der automatischen Abschlusskontrollen (Datenlauf: 17 von 17)
    ├── versionen.csv                Programmversionen des Abgabelaufs
    └── *.png                        Abbildungen
```

**Verbindlich ist dieses Repository.** Das Notebook klont es beim Start in die Colab-Sitzung.

**Nicht im Repository:** die Original-PDFs, die extrahierten Volltexte und die gefüllte Wissensdatenbank. Die PDFs bezieht jede Person beim Ausführen selbst von der offiziellen Downloadseite. Gezeigt werden nur kurze Belegzitate mit Seitenangabe.

## Urheberrecht

Beide Regelhefte sind urheberrechtlich geschützt (© KOSMOS). Ein öffentlicher Download begründet kein Recht zur Weiterveröffentlichung. Im Repository liegen deshalb nur das Quellenmanifest und der Code zur Wiederherstellung; in der Auswertung werden kurze Belegzitate mit Seitenangabe im Rahmen des Zitatrechts verwendet.

| Dokument | Artikelnummer | Seiten | Impressum |
|---|---|---:|---|
| CATAN – Das Spiel | 684655 | 12 | © 1995, 2025 KOSMOS |
| CATAN – Städte & Ritter | 684754 | 16 | © 1998, 2025 KOSMOS |

## Betriebsarten

Das Notebook ist für Google Colab ausgelegt und trainiert kein Modell — eine GPU wird nicht benötigt. Zwei Schalter in der Konfigurationszelle bestimmen die Betriebsart:

| Schalter | Wirkung | Voraussetzungen |
|---|---|---|
| `PRUEFMODUS = True` *(Voreinstellung)* | Gespeicherte Ergebnisse des Abgabelaufs laden, Prüfsumme nachrechnen und alle Kennzahlen neu berechnen | Internet |
| `PRUEFMODUS = False`, `ENDLAUF = True` *(Voreinstellung)* | Vollständiger Durchlauf über alle 36 Fragen | API-Schlüssel |
| `PRUEFMODUS = False`, `ENDLAUF = False` | Entwicklungsphase, nur die 6 Entwicklungsfragen | API-Schlüssel |

Die dritte Zeile bricht ab, wenn bereits bewertete Testfälle vorliegen: Ein Entwicklungslauf würde ein Ergebnispaket ohne Kennzahlen erzeugen und damit den Abgabestand ersetzen.

Der Schalter `ABLAGE` bestimmt den Arbeitsordner. Die Abgabe verwendet `"github"`: Das Repository wird in die Colab-Sitzung geklont und am Ende jedes Datenlaufs ein `ergebnisse_paket.zip` zum Herunterladen erzeugt. Die Alternativen `"drive"` und `"colab"` sind vorhanden, für die Bewertung aber nicht nötig.

**Für einen eigenen Datenlauf**

1. Nichts herunterladen: Das Notebook lädt beide Regelhefte beim ersten Lauf von [catan.de](https://www.catan.de/catan-verstehen/spielregeln) und vergleicht die SHA-256-Prüfsumme mit der dokumentierten Fassung. Scheitert der Download, öffnet sich ein Upload-Dialog.
2. In Colab unter *Secrets* (Schlüsselsymbol) `OPENAI_API_KEY` anlegen und den Notebook-Zugriff aktivieren; optional `SUPABASE_URL` und `SUPABASE_KEY`. Schlüssel stehen weder im Notebook noch im Repository.
3. `PRUEFMODUS = False` setzen und *Laufzeit → Alle ausführen*.

Der Durchlauf setzt nach einem Abbruch an der richtigen Stelle fort: Bereits erzeugte Antworten zur aktuellen Prüfsumme gelten als erledigt.

**Supabase (optional).** Das SQL aus `ergebnisse/schema.sql` einmalig im SQL-Editor des Supabase-Projekts ausführen. Das Notebook schreibt die Chunks samt Vektoren in die Datenbank und prüft, dass Supabase dieselben Treffer liefert wie der lokale Pfad. Ohne Zugangsdaten läuft alles lokal im Arbeitsspeicher.

**Laufzeit und Kosten.** Der dokumentierte Datenlauf umfasste 108 Modellaufrufe (36 Fragen × 3 Bedingungen) mit rund 74.000 Tokens in etwa fünf Minuten. Die Indexierung beider Hefte mit `text-embedding-3-small` kostet weniger als einen Cent; der gesamte Durchlauf liegt im Bereich einiger Cent.

## Reproduktion in drei Stufen

1. **Ergebnisse prüfen** — Voreinstellung. Wissensbasis wird neu aufgebaut und gegen die Prüfsumme des Abgabelaufs gehalten; Kennzahlen, Intervalle und Abbildungen werden aus den gespeicherten Antworten und Bewertungen neu berechnet. Kein API-Zugang nötig.
2. **Eigene Bewertung** — denselben Bewertungsbogen mit eigenen Urteilen ausfüllen und Schritt 1 wiederholen. Die Zuordnung zu den Bedingungen steht getrennt in `bewertung_schluessel.csv`, die Bewertung bleibt damit verblindet möglich. Kein API-Zugang nötig.
3. **Neuen Durchlauf erzeugen** — eigener API-Schlüssel, optional eine eigene Supabase-Instanz. Die Ergebnisse des Abgabelaufs bleiben erhalten, weil eine geänderte Konfiguration eine neue Prüfsumme erzeugt.

## Bewusste Einschränkungen

- **Vorwissen des Modells.** CATAN ist in Trainingsdaten stark vertreten. Bedingung A misst „Modell mit unkontrolliertem Vorwissen unbekannter Editionsaktualität", nicht „Modell ohne Wissen".
- **Ungleiche Fragetypverteilung.** Ausnahme- und Anwendungsfragen sind bewusst übergewichtet. Ergebnisse werden primär je Fragetyp berichtet; der gepoolte Wert ist keine „typische Leistung".
- **Statistische Aussagekraft.** 30 Testfragen in 13 Regelgruppen; der Bootstrap arbeitet effektiv mit 13 Einheiten. Die praktische Nachweisgrenze wurde vorab bei 20–25 Prozentpunkten genannt. Kleine oder moderate Effekte kann diese Arbeit nicht nachweisen, und der Katalog wurde nicht vergrößert, um Signifikanz zu erreichen.
- **Nur drei Grundspielfragen.** Sie dienen als Kontrolle für das Vorwissen, tragen aber keine eigene Aussage über das Grundspiel.
- **Ein Durchlauf je Frage und Bedingung.** Die Streuung wiederholter Generierungen ist nicht gemessen und in den Intervallen nicht enthalten.
- **Bewertung.** Die Bewertung ist nicht unabhängig von Vorkenntnis entstanden; die Fehlerarten wurden nur von einer Person vergeben. Einzelheiten in Abschnitt 12.4 des Notebooks.
- **Herkunft der Fragen.** **Alle 36 Fragen sind KI-Entwürfe** (Feld `entwurf` = `ki_entwurf`). Die Prüfung gegen das Regelheft und die Freigabe erfolgten durch den Autor. Eine Auswahlverzerrung zugunsten von Regeln, die das Antwortmodell ohnehin beherrscht, ist nicht auszuschließen.
- **Bedingung C** ist eine Diagnose, keine Obergrenze. „B falsch, C richtig" ist ein Hinweis auf ein Retrievalproblem, keine bewiesene Ursache.

## Einsatz von KI-Werkzeugen

Bei dieser Arbeit wurden Sprachmodelle in erheblichem Umfang als Werkzeug eingesetzt. Der vollständige, nach Arbeitsschritten getrennte Hinweis steht in **Abschnitt 13 des Notebooks** und ist Teil der Abgabe. In Kurzform:

**Mit KI-Unterstützung entstanden** das Versuchsdesign und der Programmcode, alle 36 Fragen als Entwürfe, die Referenzantworten, Pflichtaussagen und Fehlerkriterien, ein Teil der annotierten Belegstellen sowie Gliederung, Formulierung und Vorschläge zur Einordnung der Ergebnisse.

**Eigenleistung des Autors** sind die Prüfung jeder Referenzantwort, jeder Belegstelle und jeder Seitenangabe am Regelheft, die Auswahl eines Teils der Regelstellen, die Durchführung der Läufe, die Bewertung der 90 Testfälle und alle inhaltlichen Entscheidungen.

Eine Prozentangabe zum Gesamtanteil wird bewusst nicht gemacht, weil sie nicht belegbar wäre.

## Literatur

1. Lewis, P.; Perez, E.; Piktus, A.; Petroni, F.; Karpukhin, V.; Goyal, N.; Küttler, H.; Lewis, M.; Yih, W.; Rocktäschel, T.; Riedel, S.; Kiela, D. (2020): *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* In: Advances in Neural Information Processing Systems 33 (NeurIPS 2020), S. 9459–9474. https://proceedings.neurips.cc/paper_files/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf
2. Karpukhin, V.; Oguz, B.; Min, S.; Lewis, P.; Wu, L.; Edunov, S.; Chen, D.; Yih, W. (2020): *Dense Passage Retrieval for Open-Domain Question Answering.* In: Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), S. 6769–6781. https://doi.org/10.18653/v1/2020.emnlp-main.550
3. Wu, S.; Xiong, Y.; Cui, Y.; Wu, H.; Chen, C.; Yuan, Y.; Huang, L.; Liu, X.; Kuo, T.-W.; Guan, N.; Xue, C. J. (2026): *Retrieval-augmented generation for natural language processing: a survey.* Artificial Intelligence Review 59(9), Artikel 192. https://doi.org/10.1007/s10462-026-11605-7
4. Yu, H.; Gan, A.; Zhang, K.; Tong, S.; Liu, Q.; Liu, Z. (2025): *Evaluation of Retrieval-Augmented Generation: A Survey.* In: Zhu, W. et al. (Hrsg.): Big Data. Communications in Computer and Information Science, Bd. 2301. Singapur: Springer, S. 102–120. https://doi.org/10.1007/978-981-96-1024-2_8
5. Es, S.; James, J.; Espinosa Anke, L.; Schockaert, S. (2024): *RAGAs: Automated Evaluation of Retrieval Augmented Generation.* In: Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics: System Demonstrations, S. 150–158. https://doi.org/10.18653/v1/2024.eacl-demo.16
6. Shi, F.; Chen, X.; Misra, K.; Scales, N.; Dohan, D.; Chi, E. H.; Schärli, N.; Zhou, D. (2023): *Large Language Models Can Be Easily Distracted by Irrelevant Context.* In: Proceedings of the 40th International Conference on Machine Learning (ICML), PMLR 202, S. 31210–31227. https://proceedings.mlr.press/v202/shi23a.html
7. Cohen, J. (1960): *A Coefficient of Agreement for Nominal Scales.* Educational and Psychological Measurement 20(1), S. 37–46. https://doi.org/10.1177/001316446002000104
8. Longpre, S.; Perisetla, K.; Chen, A.; Ramesh, N.; DuBois, C.; Singh, S. (2021): *Entity-Based Knowledge Conflicts in Question Answering.* In: Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing (EMNLP), S. 7052–7063. https://doi.org/10.18653/v1/2021.emnlp-main.565
9. Efron, B.; Tibshirani, R. J. (1993): *An Introduction to the Bootstrap.* New York: Chapman & Hall.
10. Field, C. A.; Welsh, A. H. (2007): *Bootstrapping Clustered Data.* Journal of the Royal Statistical Society: Series B (Statistical Methodology) 69(3), S. 369–390. https://doi.org/10.1111/j.1467-9868.2007.00593.x
11. Dror, R.; Baumer, G.; Shlomov, S.; Reichart, R. (2018): *The Hitchhiker's Guide to Testing Statistical Significance in Natural Language Processing.* In: Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), S. 1383–1392. https://doi.org/10.18653/v1/P18-1128
12. McNemar, Q. (1947): *Note on the Sampling Error of the Difference Between Correlated Proportions or Percentages.* Psychometrika 12(2), S. 153–157. https://doi.org/10.1007/BF02295996
13. Manning, C. D.; Raghavan, P.; Schütze, H. (2008): *Introduction to Information Retrieval.* Cambridge: Cambridge University Press, Kap. 8 (Evaluation in Information Retrieval).
14. Liu, N. F.; Lin, K.; Hewitt, J.; Paranjape, A.; Bevilacqua, M.; Petroni, F.; Liang, P. (2024): *Lost in the Middle: How Language Models Use Long Contexts.* Transactions of the Association for Computational Linguistics 12, S. 157–173. https://doi.org/10.1162/tacl_a_00638

Technische Dokumentation (OpenAI-Embeddings, pgvector) und die Primärquellen des Korpus stehen im Notebook, Abschnitt 13.
