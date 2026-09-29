"""Wandelt den Export der Bewertungsseite (ein JSON je Fall) in ergebnisse/bewertung_v2.csv."""
import json
import sys
from pathlib import Path

import pandas as pd

quelle = Path(sys.argv[1])            # Ordner mit bewertungen/V001.json ...
repo = Path(sys.argv[2])
zeilen = []
for datei in sorted((quelle / "bewertungen").glob("V*.json")):
    roh = json.loads(datei.read_text(encoding="utf-8"))
    doc = roh.get("data", roh)
    zeilen.append({
        "fall_id": doc["id"], "p": "|".join(doc["p"]), "k": "|".join(doc["k"]),
        "r": doc["r"], "z": doc["z"], "w": doc["w"], "g": doc["g"],
        "notiz": doc.get("notiz", ""), "erstmals": doc.get("erstmals", ""),
        "gespeichert": doc["gespeichert"], "aenderungen": doc.get("aenderungen", 0),
        "rubrik_sha256": doc["rubrik_sha256"],
    })
frame = pd.DataFrame(zeilen).sort_values("fall_id")
frame.to_csv(repo / "ergebnisse" / "bewertung_v2.csv", index=False, encoding="utf-8-sig")
abschluss = quelle / "status" / "abschluss.json"
if abschluss.exists():
    roh = json.loads(abschluss.read_text(encoding="utf-8"))
    (repo / "ergebnisse" / "bewertung_v2_abschluss.json").write_text(
        json.dumps(roh.get("data", roh), ensure_ascii=False, indent=2), encoding="utf-8")
print(len(frame), "Faelle exportiert")
