"""Berechnung der Stufe aus den erfassten Merkmalen (Rubrik v2, RUBRIK.md).

Die bewertende Person erfasst nur Beobachtungen; diese Funktion leitet daraus
die Stufe 0/1/2 ab. Sie wird unveraendert im Notebook verwendet.
"""

P_WERTE = ("enthalten", "fehlt", "falsch")


def stufe_v2(p: list, k: list, r: bool, z: bool, w: bool) -> int:
    """p: Status je Pflichtaussage, k: je Fehlerkriterium True/False."""
    if not p or any(x not in P_WERTE for x in p):
        raise ValueError(f"ungueltige Pflichtaussagen: {p}")
    if any(k) or "falsch" in p or r or "enthalten" not in p:
        return 0
    if all(x == "enthalten" for x in p) and not z and not w:
        return 2
    return 1


if __name__ == "__main__":
    assert stufe_v2(["enthalten", "enthalten"], [False, False], False, False, False) == 2
    assert stufe_v2(["enthalten", "fehlt"], [False], False, False, False) == 1
    assert stufe_v2(["enthalten", "enthalten"], [False], False, True, False) == 1
    assert stufe_v2(["enthalten", "enthalten"], [False], False, False, True) == 1
    assert stufe_v2(["enthalten", "falsch"], [False], False, False, False) == 0
    assert stufe_v2(["enthalten", "enthalten"], [True], False, False, False) == 0
    assert stufe_v2(["enthalten", "enthalten"], [False], True, False, False) == 0
    assert stufe_v2(["fehlt", "fehlt"], [False], False, False, False) == 0
    print("stufe_v2: alle Pruefungen bestanden")
