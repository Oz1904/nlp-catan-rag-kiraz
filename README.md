# Einfluss von Retrieval-Augmented Generation auf die Korrektheit deutschsprachiger Spielregelantworten am Beispiel von CATAN

Semesterabschließende Ausarbeitung im Modul **Natural Language Processing (SoSe 2026)**
Fachhochschule Südwestfalen · M.Sc. Angewandte Künstliche Intelligenz

**Autor:** Ozan Kiraz · **Matrikelnummer:** _eintragen_
**Betreuung:** Prof. Dr. Christian Gawron
**Abgabe:** 29. September 2026

[![In Colab öffnen](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Oz1904/nlp-catan-rag-kiraz/blob/main/NLP_Hausarbeit_CATAN_RAG.ipynb)

---

## Für Prüfende: Ergebnisse in fünf Minuten nachvollziehen

Alles, was zur Bewertung nötig ist, liegt in diesem Repository. Ein Zugang zu Google Drive, ein API-Schlüssel oder eine Datenbank wird **nicht** benötigt.

1. Notebook in Colab öffnen: [NLP_Hausarbeit_CATAN_RAG.ipynb in Colab](https://colab.research.google.com/github/Oz1904/nlp-catan-rag-kiraz/blob/main/NLP_Hausarbeit_CATAN_RAG.ipynb)
2. In der Konfigurationszelle `PRUEFMODUS = True` setzen.
3. *Laufzeit → Alle ausführen*.

Das Notebook holt dann die gespeicherten Ergebnisse des Abgabelaufs aus diesem Repository, lädt die beiden Regelhefte von der offiziellen Downloadseite, baut die Wissensbasis daraus neu auf und vergleicht sie mit der Prüfsumme des Abgabelaufs. Anschließend rechnet es Korrektheitsanteile, Bootstrap-Intervalle, Fehlerdiagnose und Abbildungen aus den gespeicherten Antworten und Bewertungen neu. Es werden keine Modellantworten erzeugt.

Wer nur lesen möchte: Das Notebook enthält alle Zellausgaben des dokumentierten Laufs, auch ohne Ausführung.

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
| **C** | die Chunks mit den annotierten Schlüsselzitaten (Gold-Chunks) | Diagnose: Was bleibt bei perfektem Retrieval falsch? |

Bedingung C erhält die Chunks mit den Schlüsselzitaten, nicht die vollständigen Belegseiten: B erhält immer k Chunks, eine ganze Seite je nach Frage weniger oder deutlich mehr. Bedingung C ist eine Diagnose, **keine** garantierte Obergrenze.

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

Die Ordnerstruktur entspricht dem Arbeitsordner `NLP_CATAN` in Google Drive — ohne die PDFs. **Verbindlich ist dieses Repository**: Drive ist nur die Arbeitsablage des Autors für Colab und die heruntergeladenen Regelhefte; ein Zugang dazu wird für die Bewertung nicht benötigt. Zusätzlich liegt im Ergebnisordner `zweitbewertung_auswahl.csv` mit den vorab gezogenen Fällen für die Zweitbewertung.

**Nicht im Repository:** die Original-PDFs, die extrahierten Volltexte und die gefüllte Wissensdatenbank. Die PDFs bezieht jede Person beim Ausführen selbst von der offiziellen Downloadseite. Das Notebook zeigt aus den Regelheften nur kurze Auszüge und Schlüsselzitate mit Seitenangabe.

## Urheberrecht

Beide Regelhefte sind urheberrechtlich geschützt (© KOSMOS). Ein öffentlicher Download begründet kein Recht zur Weiterveröffentlichung. Im Repository liegen deshalb nur das Quellenmanifest und der Code zur Wiederherstellung; in der Auswertung werden kurze Belegzitate mit Seitenangabe im Rahmen des Zitatrechts verwendet.

| Dokument | Artikelnummer | Seiten | Impressum |
|---|---|---:|---|
| CATAN – Das Spiel | 684655 | 12 | © 1995, 2025 KOSMOS |
| CATAN – Städte & Ritter | 684754 | 16 | © 1998, 2025 KOSMOS |

## Ausführung

Das Notebook ist für Google Colab ausgelegt und trainiert kein Modell — eine GPU wird nicht benötigt. Zwei Schalter in der Konfigurationszelle bestimmen die Betriebsart:

| Schalter | Wirkung | Voraussetzungen |
|---|---|---|
| `PRUEFMODUS = True` | Gespeicherte Ergebnisse des Abgabelaufs laden und neu auswerten | keine |
| `PRUEFMODUS = False`, `ENDLAUF = False` | Entwicklungsphase: nur die Entwicklungsfragen | API-Schlüssel |
| `PRUEFMODUS = False`, `ENDLAUF = True` | Vollständiger Durchlauf über die Testfragen | API-Schlüssel |

Für einen eigenen Durchlauf:

1. Nichts herunterladen: Das Notebook lädt beide Regelhefte beim ersten Lauf von der offiziellen Downloadseite ([catan.de](https://www.catan.de/catan-verstehen/spielregeln)) nach `Meine Ablage/NLP_CATAN/quellen/` und vergleicht die SHA-256-Prüfsumme mit der dokumentierten Fassung. Scheitert der Download, öffnet sich ein Upload-Dialog.
2. In Colab unter *Secrets* (Schlüsselsymbol) `OPENAI_API_KEY` anlegen und den Notebook-Zugriff aktivieren; optional `SUPABASE_URL` und `SUPABASE_KEY`.
3. *Laufzeit → Alle ausführen* und den Zugriff auf Google Drive bestätigen.

Alle Ergebnisse landen in `Meine Ablage/NLP_CATAN/ergebnisse/` und überstehen einen Neustart der Laufzeit; der Durchlauf setzt nach einem Abbruch an der richtigen Stelle fort.

**Supabase (optional).** Das SQL aus `ergebnisse/schema.sql` einmalig im SQL-Editor des Supabase-Projekts ausführen. Das Notebook schreibt die Chunks samt Vektoren in die Datenbank und prüft per Konsistenztest, dass Supabase dieselben Treffer liefert wie der lokale Pfad. Ohne Zugangsdaten läuft alles lokal. Schlüssel stehen weder im Notebook noch im Repository.

**Phasen.** Solange `ENDLAUF = False` gilt, stellt das Notebook nur die Entwicklungsfragen. Nach Fertigstellung und Prüfung des Katalogs wird `ENDLAUF = True` gesetzt; ausgewertet werden dann ausschließlich die Testfragen.

**Laufzeit und Kosten.** Die Laufzeit wird von den API-Aufrufen bestimmt. Die Indexierung der beiden Hefte kostet mit `text-embedding-3-small` (0,02 USD je 1 Mio. Tokens) weniger als einen Cent. Der vollständige A/B/C-Durchlauf liegt bei rund 120 Aufrufen (etwa 40 Fragen × 3 Bedingungen); das eingeplante Budget beträgt 10–20 USD.

## Reproduktion in drei Stufen

1. **Ergebnisse prüfen** — `PRUEFMODUS = True`. Wissensbasis wird neu aufgebaut und gegen die Prüfsumme des Abgabelaufs gehalten; Kennzahlen, Intervalle und Abbildungen werden aus den gespeicherten Antworten und Bewertungen neu berechnet. Kein API-Zugang nötig.
2. **Eigene Bewertung** — denselben Bewertungsbogen mit eigenen Urteilen ausfüllen und Schritt 1 wiederholen. Die Zuordnung zu den Bedingungen steht getrennt in `bewertung_schluessel.csv`, die Bewertung bleibt damit verblindet möglich. Kein API-Zugang nötig.
3. **Neuen Durchlauf erzeugen** — eigener API-Schlüssel, optional eine eigene Supabase-Instanz. Die Ergebnisse des Abgabelaufs bleiben dabei erhalten, weil eine geänderte Konfiguration eine neue Prüfsumme erzeugt.

## Bewusste Einschränkungen

- **Vorwissen des Modells.** CATAN ist in Trainingsdaten stark vertreten. Bedingung A misst „Modell mit unkontrolliertem Vorwissen unbekannter Editionsaktualität", nicht „Modell ohne Wissen". Bei Faktenfragen ist deshalb nur ein geringer Effekt zu erwarten.
- **Ungleiche Fragetypverteilung.** Ausnahme- und Anwendungsfragen sind bewusst übergewichtet. Ergebnisse werden primär je Fragetyp berichtet; der gepoolte Wert ist keine „typische Leistung".
- **Statistische Aussagekraft.** Bei diesem Katalogumfang liegt die praktische Nachweisgrenze bei etwa 20–25 Prozentpunkten. Die Studie ist nicht darauf ausgelegt, kleine oder moderate Effekte nachzuweisen. Der Katalog wird nicht vergrößert, um Signifikanz zu erreichen.
- **Ein Durchlauf je Frage und Bedingung.** Die Varianz wiederholter Generierungen wird nicht geschätzt.
- **Bewertung.** Falls keine Zweitbewertung vorliegt, wird das als Einschränkung offengelegt.
- **Herkunft der Fragen.** Jede Frage trägt im Feld `entwurf`, ob sie selbst formuliert, sprachlich KI-überarbeitet oder ein KI-Entwurf ist. Die fachliche Prüfung gegen das Regelheft erfolgt in allen Fällen durch den Autor. Bei KI-Entwürfen ist eine Auswahlverzerrung zugunsten von Regeln, die das Antwortmodell ohnehin beherrscht, nicht auszuschließen.
- **Bedingung C** ist eine Diagnose, keine Obergrenze. „B falsch, C richtig" ist ein Hinweis auf ein Retrievalproblem, keine bewiesene Ursache.

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

## Einsatz von KI-Werkzeugen

Sprachmodelle wurden als Werkzeug bei Codeentwurf und sprachlicher Überarbeitung eingesetzt. Die fachliche Prüfung sämtlicher Referenzantworten und Belegstellen sowie die Bewertung der Modellantworten erfolgten manuell durch den Autor. _Ausgestaltung an die Vorgaben der Hochschule anpassen._
