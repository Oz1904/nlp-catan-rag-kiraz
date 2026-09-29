"""Erzeugt den verblindeten Bewertungsbogen v2 (Rubrik: RUBRIK.md).

Eingaben:  ergebnisse/laufprotokoll.jsonl        (A, B, C; Pruefsumme des Hauptversuchs)
           ergebnisse/zusatz_d/laufprotokoll_d.jsonl  (D)
           ergebnisse/bewertungen.csv + bewertung_schluessel.csv
               (nur fuer Fragetext, Referenz, Pflichtaussagen, Fehlerkriterien)
Ausgaben:  bewertung_v2/bogen_v2.json       Faelle ohne Bedingung und ohne Fragekennung
           bewertung_v2/schluessel_v2.csv   Zuordnung Fall -> Frage, Bedingung
                                            (erst nach Abschluss der Bewertung oeffnen)

Reihenfolge: Fragen in zufaelliger Reihenfolge, innerhalb jeder Frage die vier
Antworten in zufaelliger Reihenfolge (Seed 20260929). Kennungen V001 ... V120
folgen dieser Reihenfolge.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

WURZEL = Path(__file__).resolve().parent.parent
ERG = WURZEL / "ergebnisse"
AUS = WURZEL / "bewertung_v2"
HAUPT_PRUEFSUMME = "2577d51e1f8487c8eabe39abd12fb6e75e0002043f9e7749233d865dd082946f"
SEED_V2 = 20260929

# identisch zu verblinde() im Notebook (Abschnitt 10)
CHUNK_MARKE = re.compile(r"\[?\b(?:GS|SR)-\d{2}-\d{2}\b\]?")


def verblinde(antwort: str) -> str:
    ohne = CHUNK_MARKE.sub("", str(antwort))
    ohne = re.sub(r"\(\s*\)|\[\s*\]", "", ohne)
    ohne = re.sub(r"\s+([,.;:])", r"\1", ohne)
    return re.sub(r"\s{2,}", " ", ohne).strip()


def lies_jsonl(pfad: Path) -> list:
    with open(pfad, encoding="utf-8") as datei:
        return [json.loads(z) for z in datei if z.strip()]


def main(ohne_d: bool = False) -> None:
    haupt = pd.DataFrame([z for z in lies_jsonl(ERG / "laufprotokoll.jsonl")
                          if z.get("pruefsumme") == HAUPT_PRUEFSUMME and z.get("erfolg")])
    haupt = haupt[haupt["question_id"].str.startswith("T")]
    assert len(haupt) == 90 and not haupt.duplicated(["question_id", "bedingung"]).any()

    teile = [haupt[["question_id", "bedingung", "antwort"]]]
    d_pfad = ERG / "zusatz_d" / "laufprotokoll_d.jsonl"
    if d_pfad.exists():
        plan = json.load(open(ERG / "zusatz_d" / "versuchsplan_d.json", encoding="utf-8"))
        d = pd.DataFrame([z for z in lies_jsonl(d_pfad)
                          if z.get("pruefsumme") == plan["pruefsumme"] and z.get("erfolg")])
        d = d.drop_duplicates("question_id", keep="first")
        assert len(d) == 30, f"{len(d)} D-Antworten statt 30"
        teile.append(d[["question_id", "bedingung", "antwort"]])
    elif not ohne_d:
        sys.exit("D-Antworten fehlen (ergebnisse/zusatz_d/laufprotokoll_d.jsonl).")
    faelle = pd.concat(teile, ignore_index=True)
    faelle["antwort"] = faelle["antwort"].map(verblinde)

    # Fragetext, Referenz, Pflichtaussagen und Fehlerkriterien aus dem Bogen v1
    b1 = pd.read_csv(ERG / "bewertungen.csv", encoding="utf-8-sig", dtype=str)
    s1 = pd.read_csv(ERG / "bewertung_schluessel.csv", encoding="utf-8-sig", dtype=str)
    katalog = (b1.merge(s1, on="fall_id")
               .drop_duplicates("question_id")
               .set_index("question_id")[["frage", "referenzantwort",
                                          "zwingende_aussagen", "fehlerkriterien"]])
    # Kontrolle: Die verblindeten Antworten aus A, B, C stimmen mit Bogen v1 ueberein
    v1 = b1.merge(s1, on="fall_id").set_index(["question_id", "bedingung"])["antwort"]
    for z in faelle.itertuples():
        if z.bedingung != "D_volltext":
            assert v1.loc[(z.question_id, z.bedingung)] == z.antwort, (z.question_id, z.bedingung)

    rng = np.random.default_rng(SEED_V2)
    fragen = sorted(faelle["question_id"].unique())
    reihenfolge = [fragen[i] for i in rng.permutation(len(fragen))]
    zeilen, faelle_json = [], []
    nummer = 0
    for gruppe, qid in enumerate(reihenfolge, start=1):
        teil = faelle[faelle["question_id"] == qid].sort_values("bedingung").reset_index(drop=True)
        for pos, i in enumerate(rng.permutation(len(teil)), start=1):
            nummer += 1
            fall = teil.iloc[i]
            kennung = f"V{nummer:03d}"
            k = katalog.loc[qid]
            faelle_json.append({
                "id": kennung, "gruppe": gruppe, "pos": pos, "n_in_gruppe": len(teil),
                "frage": k["frage"], "antwort": fall["antwort"],
                "referenz": k["referenzantwort"],
                "pflicht": k["zwingende_aussagen"].split(" | "),
                "kriterien": k["fehlerkriterien"].split(" | "),
            })
            zeilen.append({"fall_id": kennung, "question_id": qid, "bedingung": fall["bedingung"]})

    rubrik_sha = hashlib.sha256((AUS / "RUBRIK.md").read_bytes()).hexdigest()
    bogen = {"rubrik_sha256": rubrik_sha, "seed": SEED_V2, "n": len(faelle_json),
             "faelle": faelle_json}
    (AUS / "bogen_v2.json").write_text(json.dumps(bogen, ensure_ascii=False, indent=1),
                                       encoding="utf-8")
    pd.DataFrame(zeilen).to_csv(AUS / "schluessel_v2.csv", index=False, encoding="utf-8-sig")
    print(f"{len(faelle_json)} Faelle in {len(reihenfolge)} Fragen; Rubrik {rubrik_sha[:12]}")
    print("Bedingungen:", pd.DataFrame(zeilen)["bedingung"].value_counts().to_dict())


if __name__ == "__main__":
    main(ohne_d="--ohne-d" in sys.argv)
