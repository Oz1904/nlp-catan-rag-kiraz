"""Setzt bogen_v2.json in die Vorlage ein und schreibt die Bewertungsseite."""
import json
from pathlib import Path

HIER = Path(__file__).resolve().parent
bogen = json.loads((HIER / "bogen_v2.json").read_text(encoding="utf-8"))
vorlage = (HIER / "bewertung_template.html").read_text(encoding="utf-8")
daten = json.dumps(bogen, ensure_ascii=False).replace("</", "<\\/")
(HIER / "bewertung_v2.html").write_text(vorlage.replace("/*__BOGEN__*/null", daten), encoding="utf-8")
print("bewertung_v2.html geschrieben,", bogen["n"], "Faelle")
