# Quellen: offizielle Regelhefte

Die beiden Regelhefte sind urheberrechtlich geschützt (© KOSMOS) und liegen deshalb **nicht** in diesem Repository. Sie stehen auf der offiziellen CATAN-Seite frei zum Download bereit; das Notebook lädt sie beim ersten Lauf automatisch von dort.

| Dokument | Artikelnummer | Seiten | SHA-256 der verwendeten Fassung |
|---|---|---:|---|
| CATAN – Das Spiel. Spielregel | 684655 | 12 | `a5c1ea3e00ae96aea4a1ed6ade96cdf862a4bc681446a4e8d716f8d27d9f418b` |
| CATAN – Städte & Ritter. Spielregel | 684754 | 16 | `d069c5ec8fc8a0f47ba1d0cca695bcf5680206b29da87f34da9bb150546ae1c7` |

Offizielle Downloadseite: https://www.catan.de/catan-verstehen/spielregeln

- Grundspiel: https://www.catan.de/sites/default/files/2025-03/4002051684655_CAT_NE_Basis34_Manual_DE_web.pdf
- Städte & Ritter: https://www.catan.de/sites/default/files/2025-03/400205684754_CAT_NE_SuR_Manual_DE_web.pdf

**Verwendung**

- *Google Colab:* nichts zu tun – das Notebook lädt die PDFs nach `Meine Ablage/NLP_CATAN/quellen/`. Scheitert der Download, erscheint ein Upload-Dialog.
- *Lokal:* PDFs in diesen Ordner legen und das Notebook im Repository-Wurzelverzeichnis starten.

Der Dateiname ist beliebig. Das Notebook erkennt die Hefte an Artikelnummer und Seitenzahl und vergleicht die Prüfsumme mit der oben dokumentierten Fassung. Bei Abweichung erscheint ein Hinweis, weil sich dann Seitenangaben im Fragenkatalog verschieben können.
