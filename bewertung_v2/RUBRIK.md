# Bewertungsrubrik v2 (eingefroren vor Beginn der Neubewertung)

Stand: 29.09.2026. Diese Datei wird vor der ersten Bewertung committet und danach nicht mehr verändert. Ihre SHA-256-Prüfsumme wird im Bewertungswerkzeug angezeigt und mit jeder Bewertung gespeichert.

## Anlass

Die erste Bewertung (v1, 90 Testfälle) enthält dokumentierte Inkonsistenzen: gleiche Fehlerbilder erhielten unterschiedliche Stufen, und 5 von 15 Fällen der Stufe 1 hatten eine als falsch markierte Entscheidung, obwohl Stufe 1 laut Schema eine richtige Entscheidung voraussetzt. Die binäre Hauptkennzahl war davon nicht betroffen, die dreistufige Skala und die Fehlerarten aber schon.

Ursache: In v1 hat die bewertende Person die Stufe direkt vergeben und die Regeln dabei im Kopf angewendet. In v2 erfasst sie nur Beobachtungen. Die Stufe berechnet der Code mit einer festen Regel.

## Was bewertet wird

- 120 Fälle: die 90 Testantworten aus A, B und C sowie 30 Testantworten aus dem Zusatzversuch D.
- Neue Kennungen (`V001` …), neu gemischt. Die Zuordnung zur Bedingung liegt in einer getrennten Schlüsseldatei, die erst nach Abschluss geöffnet wird.
- Die Fälle erscheinen nach Fragen gruppiert. Frage- und Antwortreihenfolge sind zufällig, damit Antworten derselben Frage mit denselben Maßstäben nacheinander bewertet werden.
- Chunk-Kennungen sind aus den Antworten entfernt, wie in v1.
- Die Regelhefte liegen beim Bewerten bereit. Jede als regelwidrig markierte Aussage wird am Heft geprüft.
- Die Bewertungen aus v1 werden während der Bewertung nicht eingesehen.

## Erfasste Merkmale je Fall

**P – Pflichtaussagen.** Für jede Pflichtaussage der Frage genau einer von drei Werten:

| Wert | Bedeutung |
|---|---|
| `enthalten` | Die Antwort trifft die Aussage sinngleich und stellt an keiner Stelle das Gegenteil auf. |
| `fehlt` | Die Aussage kommt nicht vor, auch nicht sinngleich. Eine unvollständige Angabe (z. B. „eine Handelsware“ statt „Papier“) gilt als `fehlt`. |
| `falsch` | Die Antwort stellt zu diesem Punkt eine abweichende oder gegenteilige Angabe auf, auch wenn an anderer Stelle die richtige steht. Enthält die Pflichtaussage eine Begründung („weil …“), ist sie auch dann `falsch`, wenn die Antwort dieselbe Entscheidung mit einer dem Heft widersprechenden Begründung trifft. |

**K – Fehlerkriterien.** Für jedes Fehlerkriterium `ja` oder `nein`. Ein Kriterium ist erfüllt, wenn die Antwort die beschriebene Behauptung **an irgendeiner Stelle** aufstellt, auch wenn sie sich später korrigiert.

**R – Entscheidung auf erfundene Regel gestützt** (`ja`/`nein`). `ja`, wenn die Antwort die verlangte Entscheidung oder Zahl ausschließlich oder überwiegend mit einer Regel begründet, die es im Heft nicht gibt oder die dort anders lautet. Steht daneben eine zutreffende Begründung, die die Entscheidung allein trägt, gilt `nein`; die falsche Begründung zählt dann unter Z.

**Z – falsche Zusatzbehauptung** (`ja`/`nein`). `ja`, wenn die Antwort mindestens eine weitere Aussage enthält, die dem Regelheft widerspricht, gefragt oder ungefragt, und die nicht schon unter P, K oder R erfasst ist. Dazu zählt eine allgemein formulierte Aussage, die in einem Fall falsch wird, den die Frage oder die Antwort selbst ausdrücklich nennt. **Nicht** dazu zählen Aussagen, zu denen das Heft schweigt, Zweckangaben („um das Spiel auszugleichen“) und Quellenangaben. Bei `ja`: Stelle im Heft in der Notiz angeben.

**W – Selbstwiderspruch** (`ja`/`nein`). `ja`, wenn zwei Aussagen derselben Antwort einander ausschließen, z. B. erst „nicht möglich“, dann ein Weg, wie es geht, oder zwei verschiedene Werte für dieselbe Größe. Ein Widerspruch zum Regelheft oder zur Fragesituation ist **kein** Selbstwiderspruch; er fällt unter P, K, R oder Z.

**G – Grundspielregel übertragen** (`ja`/`nein`). `ja`, wenn die Antwort bei einer Frage zu *Städte & Ritter* eine Grundspielregel anwendet, die die Erweiterung ersetzt oder abwandelt. Dieses Merkmal beeinflusst die Stufe nicht und dient nur der Fehleranalyse.

**Notiz.** Pflicht, wenn ein P `falsch` ist oder R, Z oder W `ja` ist: ein Satz, was falsch ist, bei Z mit Seitenangabe.

## Berechnung der Stufe

Die Regel wird in dieser Reihenfolge angewendet:

1. **Stufe 0**, wenn mindestens eines gilt:
   - ein Fehlerkriterium ist erfüllt;
   - eine Pflichtaussage ist `falsch`;
   - R = `ja`;
   - keine einzige Pflichtaussage ist `enthalten` (Ausweichen oder Enthaltung).
2. **Stufe 2**, wenn alle Pflichtaussagen `enthalten` sind und Z = `nein` und W = `nein`.
3. **Stufe 1** in allen übrigen Fällen.

„Vollständig korrekt“ heißt Stufe 2. Das Bewertungswerkzeug zeigt die Stufe während der Bewertung nicht an, damit nicht von einer gewünschten Stufe auf die Merkmale zurückgeschlossen wird.

## Fehlerprofil

Die Fehleranalyse zählt die Merkmale selbst statt frei vergebener Kategorien: Fehlerkriterium erfüllt, Pflichtaussage falsch, Pflichtaussage fehlt, R, Z, W und G. Jedes Merkmal ist über die Definitionen oben an eine prüfbare Beobachtung gebunden.

## Vorab festgelegte Auswertung

Festgelegt vor Beginn der Bewertung v2:

1. **Grundlage** der berichteten Ergebnisse ist Bewertung v2. Bewertung v1 wird vollständig als Vergleich berichtet, zusammen mit der Übereinstimmung zwischen v1 und v2 auf den 90 gemeinsamen Fällen (Anteil gleicher Urteile und Cohens κ, binär und dreistufig) und einer Liste aller Fälle, deren binäres Urteil sich ändert.
2. **Hauptvergleich** bleibt B gegen A, Kennzahl: Anteil vollständig korrekter Antworten.
3. **Unsicherheit:**
   - Nachweisaussagen stützen sich auf einen exakten, zweiseitigen Permutationstest mit Vorzeichenwechsel der Differenzen je Regelgruppe (13 Gruppen, α = 0,05).
   - Die Größe des Effekts beschreibt ein gepaarter Cluster-Bootstrap über Regelgruppen (10.000 Ziehungen, Seed 42, Perzentilintervall).
   - Weil die Zahl der Gruppen klein ist, wird das Intervall nicht als Test verwendet.
4. **Explorativ**, jeweils mit demselben Verfahren: C gegen B, D gegen B, D gegen C sowie alle Vergleiche je Fragetyp. Je Fragetyp werden keine Nachweisaussagen getroffen, wenn der exakte Test das nicht trägt.
5. D ist nachträglich ergänzt und wird durchgehend als explorativ gekennzeichnet.
6. Nach dem Öffnen des Schlüssels wird keine Bewertung mehr geändert. Übertragungsfehler, die vor dem Öffnen auffallen, werden mit Zeitstempel korrigiert und dokumentiert.

## Grenzen dieses Vorgehens

- Die bewertende Person hat alle 90 Antworten aus A, B und C bereits in v1 bewertet und kennt die Ergebnisse. Die neue Verblindung verhindert, dass die Bedingung angezeigt wird. Sie verhindert nicht, dass einzelne Antworten wiedererkannt werden.
- Antworten mit Kontext verraten sich teils durch Formulierungen wie „laut Regel“. Die Verblindung ist deshalb, wie in v1, nicht vollständig.
- Es gibt keine unabhängige Zweitbewertung von v2.
