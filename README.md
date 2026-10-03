# Die Äbtissin und der Rat. Caritas Pirckheimer und das Nürnberger Klarakloster 1524–1528

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23121995.svg)](https://doi.org/10.5281/zenodo.23121995)

Ein Quellenapparat zum Streit um das Nürnberger Klarakloster in der Reformation: die Denkwürdigkeiten der Äbtissin Caritas Pirckheimer (1466/67–1532), ihre Bittschriften und Briefe, die Stimmen des Rats, der Familien und der Reformatoren, vom Beginn 1524 bis zum Ende der Aufzeichnungen 1528, mit einem Ausblick bis zum Tod der letzten Bewohnerin des Klosters 1596. Gemeinfreie Quellen, das frühneuhochdeutsche oder lateinische Original neben einer neuhochdeutschen Arbeitsübersetzung, eine Zeitleiste mit Verweisen in die Texte und eine Liste dessen, was geprüft und nicht aufgenommen wurde.

Live: https://die-aebtissin-und-der-rat.netlify.app/

These, an den Texten zu prüfen: Die Äbtissin verlor den Streit mit dem Rat und behielt ihre Schwestern. Der Rat nahm ihnen die Franziskaner als Beichtväter, schickte seine Prediger und ließ keine neuen Schwestern mehr zu; aber bis 1530 verließ außer den drei Töchtern, die ihre Mütter 1525 herausholten, nur eine Schwester das Kloster, und aufgelöst hat der Rat es nie.

Stufe 1 ist geschlossen (Version 1.0.0, 3. Oktober 2026) und enthält zehn Module mit 139 Einheiten:

- **Die gelehrte Äbtissin, 1502–1515** — Pirckheimers *Opera* (Frankfurt 1610, benutzt in der Ausgabe 1665), S. 340–345, und E. Münch, *Charitas Pirkheimer* (Nürnberg 1826): Caritas' lateinische Briefe an Celtis und an den Bruder, Celtis' Ode, Scheurls Lob; Latein mit Arbeitsübersetzung.
- **Die große Sündflut: der Anfang, 1524** — C. Höfler (Hg.), *Denkwürdigkeiten der Charitas Pirkheimer* (Bamberg 1852), S. [1], 3–19: der Beginn der Aufzeichnungen, die Briefe an Pfleger und Verwandte, die Bittschrift an den Rat vom Advent 1524.
- **Verhört man doch einen Dieb: Margaretha Tetzel, 1525** — Höfler S. 19–33: eine Mutter will ihre Tochter heraus, die Tochter will bleiben, und die Äbtissin verlangt, dass das Kind angehört werde.
- **Die Väter genommen, die Prediger geschickt, März bis Juni 1525** — Höfler S. 33–58, 69–71, 84–96 in Auswahl: der Abzug der Franziskaner, die Predigten, die fünf Artikel des Rats vom Pfingstmittwoch.
- **Da stee ich: die Töchter, Juni 1525** — Höfler S. 97–111: die drei Töchter, die ihre Mütter am Vorabend von Fronleichnam herausholten, und Müllners spätere Fassung.
- **Melanchthon im Beichthaus, Herbst 1525** — Höfler S. 127–176 in Auswahl: Wenzeslaus Linck und Melanchthons Besuch, ‚einig, nur in den Gelübden nicht‘.
- **Visitiert und verlassen, 1526–1528** — Höfler S. 176–191: die weltliche Visitation, der Austritt der Anna Schwarz, die Vorladung nach Bamberg, das Ende der Aufzeichnungen.
- **Der Bruder: Willibald Pirckheimer und das Kloster, 1524–1530** — Pirckheimers *Opera*, Appendix S. 374–385, und Münch 1826: der Brief an Melanchthon, die lateinische Verteidigungsrede im Namen der Nonnen, die Briefe der Schwester Klara.
- **Bis 1596: das Ende des Klosters** — Höfler S. 192–207: das Glaser-Käterlein 1539 und der Bericht des Christian Koppius von 1628 mit der Liste der Äbtissinnen.
- **Luther und die Nonnen, 1523 und 1526** — Luther, *Ursach und Antwort, daß Jungfrauen Klöster göttlich verlassen mögen* (1523), Weimarer Ausgabe Bd. 11, S. 394–400, und Herzog Georgs von Sachsen Instruktion von 1526 nach Höfler, S. LXII–LXV: eine Gegenüberstellung, keine behauptete Verbindung.

Jeder Auszug ist am Seitenbild des Digitalisats gelesen; die Texterkennung der Fraktur- und Antiquadrucke ist unbrauchbar. Jedes Modul hat gemeinfreie Bildtafeln und eine Visualisierung; dazu kommen eine Zeitleiste mit 28 Stationen, 42 Tafeln und 26 Vergleiche, darunter: Die Bibel hinter der Klausur, Gewissen gegen Gewissen, Ungehört, Welche Gewalt hat eine Mutter?, Zwei Fassungen eines Tages, Der Kammerwagen, zweimal, Der Henker, zweimal, Glauben mit Gewalt, ‚Die laß man bleiben‘, Die Eltern, umgekehrt. Die Anmerkungen benennen Widersprüche der Quellen und die Gewalt beider Seiten.

Was geprüft und nicht aufgenommen wurde, steht mit Begründung in `data/modules.json` (`missing`) und auf der Seite ‚Texte‘.

## Daten bauen

```
python tools/build-gelehrte.py
python tools/build-sindflut.py
python tools/build-dieb.py
python tools/build-prediger.py
python tools/build-toechter.py
python tools/build-melanchthon.py
python tools/build-ordnung.py
python tools/build-willibald.py
python tools/build-ende.py
python tools/build-vergleich.py
python tools/verify.py
```

Bildtafeln: `python tools/make-plates.py`; Visualisierungen: `tools/make-viz.py` und `tools/viz-*.py`.

Das Begleitspiel *Verhört man doch einen Dieb* nimmt seinen Titel von der Schwester Margaretha Tetzel (1525).

Code MIT; Editionen und Arbeitsübersetzungen CC0; redaktionelle Texte CC BY 4.0 (siehe `LICENSES.md`).

## Zitieren

Fassbender, Pantaleon. *Die Äbtissin und der Rat. Caritas Pirckheimer und das Nürnberger Klarakloster 1524–1528. Ein Quellenapparat.* 2026. https://doi.org/10.5281/zenodo.23121995 (alle Versionen; Version 1.0.0: https://doi.org/10.5281/zenodo.23121996). Bitte zitieren Sie für jede wörtlich übernommene Stelle auch die gedruckte Quelle. Metadaten: `CITATION.cff`, `.zenodo.json`.
