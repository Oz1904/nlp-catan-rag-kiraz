"""Gibt die Ziehung der Zweitbewertung v2 wieder und prueft sie gegen auswahl_zweit.csv.

Aufruf aus dem Wurzelordner des Repositorys:
    python bewertung_v2/zweitbewertung/ziehe_stichprobe.py

Ablauf (Seed 202609292, numpy.random.default_rng):
1. Aus den 20 Testfragen, die in der Zweitbewertung v1 nicht vorkamen, werden
   zehn ohne Zuruecklegen gezogen.
2. Die Reihenfolge der zehn Fragen wird zufaellig permutiert.
3. Je Frage werden ihre vier Faelle aus Bewertung v2 (nach Fallkennung sortiert)
   zufaellig permutiert und fortlaufend Z01 bis Z40 genannt.

Das urspruenglich verwendete Skript war nicht im Repository abgelegt. Dieses
Skript rekonstruiert die Ziehung und bricht ab, wenn sie nicht exakt der
abgelegten Auswahl entspricht.
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 202609292
WURZEL = Path(__file__).resolve().parents[2]

auswahl_v1 = pd.read_csv(WURZEL / "ergebnisse/zweitbewertung_auswahl.csv", dtype=str, encoding="utf-8-sig")
schluessel_v1 = pd.read_csv(WURZEL / "ergebnisse/bewertung_schluessel.csv", dtype=str, encoding="utf-8-sig")
schluessel_v2 = pd.read_csv(WURZEL / "bewertung_v2/schluessel_v2.csv", dtype=str, encoding="utf-8-sig")
abgelegt = pd.read_csv(WURZEL / "bewertung_v2/zweitbewertung/auswahl_zweit.csv", dtype=str, encoding="utf-8-sig")

fragen_v1 = set(schluessel_v1.loc[schluessel_v1["fall_id"].isin(auswahl_v1["fall_id"]), "question_id"])
testfragen = sorted(schluessel_v2.loc[schluessel_v2["question_id"].str.startswith("T"), "question_id"].unique())
uebrige = [q for q in testfragen if q not in fragen_v1]
assert len(uebrige) == 20, len(uebrige)

rng = np.random.default_rng(SEED)
gezogen = rng.choice(uebrige, 10, replace=False).tolist()
reihenfolge = rng.permutation(sorted(gezogen)).tolist()

zeilen = []
for frage in reihenfolge:
    faelle = schluessel_v2.loc[schluessel_v2["question_id"] == frage, "fall_id"].sort_values().tolist()
    for fall in rng.permutation(faelle).tolist():
        zeilen.append({"fall_zweit": f"Z{len(zeilen) + 1:02d}", "fall_v2": fall})
neu = pd.DataFrame(zeilen)

print("Gezogene Fragen in Reihenfolge:", ", ".join(reihenfolge))
if not neu.equals(abgelegt[["fall_zweit", "fall_v2"]].reset_index(drop=True)):
    raise SystemExit("Abweichung: Die Ziehung ergibt nicht die abgelegte auswahl_zweit.csv.")
print("Die Ziehung ergibt auswahl_zweit.csv exakt (40 Faelle, Kennungen und Reihenfolge).")
