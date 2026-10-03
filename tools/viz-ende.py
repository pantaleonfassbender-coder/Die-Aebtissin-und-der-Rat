"""Draw assets/viz/ende.svg: the 55 abbesses of St. Clare 1280-1563 after
Koppius (1628), and the end in instalments: the convent's numbers 1527-1596.
Every mark links to the unit that documents it.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz" / "ende.svg"
L = "#/text/"
YEARS = [1280, 1282, 1294, 1295, 1297, 1299, 1300, 1303, 1305, 1307, 1311, 1317, 1323, 1324, 1327, 1332,
         1333, 1335, 1337, 1339, 1341, 1344, 1349, 1350, 1355, 1362, 1363, 1365, 1367, 1370, 1373, 1380,
         1382, 1389, 1393, 1395, 1401, 1403, 1406, 1412, 1418, 1420, 1430, 1439, 1442, 1450, 1460, 1463,
         1466, 1470, 1488, 1503, 1532, 1533, 1563]
assert len(YEARS) == 55
NAMED = {52: "Caritas", 53: "Clara", 54: "Katharina", 55: "Ursula Muffel"}
W, H = 900, 600


def x(year):
    """Year to x coordinate, 1270-1605 across the width."""
    return 40 + (year - 1270) * (W - 80) / (1605 - 1270)


def xb(year):
    """Lower panel: 1520-1600 across the width."""
    return 60 + (year - 1520) * (W - 120) / (1600 - 1520)


def main():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="en-t en-d" font-family="var(--serif)">',
         '<title id="en-t">55 Äbtissinnen und das Ende auf Raten, 1280–1596</title>',
         '<desc id="en-d">Oben die Amtsantritte der 55 Äbtissinnen von St. Klara nach Koppius 1628, von 1280 bis 1563. Unten die Zahl der Schwestern: 52 im Jahr 1527, drei Klarissen um 1586, die letzte Klarisse 1591, die letzte Bewohnerin 1596.</desc>',
         '<text x="16" y="30" font-size="17" font-weight="bold" fill="var(--ink)">Dreihundert Jahre, und das Ende auf Raten</text>',
         '<text x="16" y="50" font-size="13" fill="var(--ink2)">Oben: Amtsantritt jeder Äbtissin nach Koppius 1628. Unten: wie viele Schwestern es noch gab.</text>']
    # axis
    ay = 170
    o.append(f'<line x1="{x(1270)}" y1="{ay}" x2="{x(1600)}" y2="{ay}" stroke="var(--ink2)"/>')
    for t in range(1300, 1601, 50):
        o.append(f'<line x1="{x(t):.0f}" y1="{ay}" x2="{x(t):.0f}" y2="{ay + 6}" stroke="var(--ink2)"/><text x="{x(t):.0f}" y="{ay + 22}" text-anchor="middle" font-size="12" fill="var(--ink2)">{t}</text>')
    # abbess ticks
    for i, yr in enumerate(YEARS, 1):
        c = "konvent" if i >= 52 else "nachwelt"
        h = 46 if i >= 52 else 26
        o.append(f'<a href="{L}ende/koppius/{2 if i >= 52 else 1}"><line x1="{x(yr):.1f}" y1="{ay}" x2="{x(yr):.1f}" y2="{ay - h}" stroke="var(--{c})" stroke-width="{3 if i >= 52 else 1.6}"/></a>')
    o.append(f'<text x="{x(1280):.0f}" y="{ay - 34}" font-size="12.5" fill="var(--ink2)">1. Kunigunde, 1280</text>')
    o.append(f'<a href="{L}ende/koppius/2"><text x="{x(1503) - 4:.0f}" y="{ay - 52}" text-anchor="end" font-size="13" font-weight="bold" fill="var(--konvent)" text-decoration="underline">52. Caritas 1503</text></a>')
    o.append(f'<a href="{L}ende/koppius/2"><text x="{x(1563) - 6:.0f}" y="{ay - 74}" text-anchor="end" font-size="13" font-weight="bold" fill="var(--konvent)" text-decoration="underline">55. Ursula Muffel 1563, ‚die letzte‘</text></a>')
    # events
    for yr, lab, href, c in [(1525, "1525 Reformation", L + "prediger/oculi/1", "rat"), (1596, "1596", L + "ende/koppius/4", "rat")]:
        o.append(f'<a href="{href}"><line x1="{x(yr):.0f}" y1="{ay + 28}" x2="{x(yr):.0f}" y2="{ay - 8}" stroke="var(--{c})" stroke-dasharray="4 3"/><text x="{x(yr):.0f}" y="{ay + 44}" text-anchor="middle" font-size="12.5" fill="var(--{c})">{lab}</text></a>')
    # lower panel: numbers of sisters
    by = 520
    o.append(f'<text x="16" y="{ay + 62}" font-size="14" font-weight="bold" fill="var(--ink)">Die Schwestern nach 1525</text>')
    o.append(f'<line x1="{xb(1520):.0f}" y1="{by}" x2="{xb(1600):.0f}" y2="{by}" stroke="var(--ink2)"/>')
    for t in range(1520, 1601, 10):
        o.append(f'<text x="{xb(t):.0f}" y="{by + 18}" text-anchor="middle" font-size="12" fill="var(--ink2)">{t}</text>')
    scale = 5.2
    pts = [(1527, 52, "52 Schwestern bei der Visitation", L + "ordnung/visitation/6", "konvent"),
           (1586, 3, "um 1586: 3 Klarissen", L + "ende/koppius/3", "konvent"),
           (1591, 1, "1591: die letzte Klarisse stirbt", L + "ende/koppius/4", "konvent")]
    for yr, n, lab, href, c in pts:
        o.append(f'<a href="{href}"><rect x="{xb(yr) - 9:.0f}" y="{by - n * scale:.0f}" width="18" height="{n * scale:.0f}" fill="var(--{c})"/></a>')
    o.append(f'<a href="{L}ordnung/visitation/6"><text x="{xb(1527) + 14:.0f}" y="{by - 52 * scale + 14:.0f}" font-size="13" fill="var(--ink)" text-decoration="underline">52 Schwestern bei der Visitation 1527</text></a>')
    o.append(f'<a href="{L}ende/koppius/3"><rect x="{xb(1586) + 10:.0f}" y="{by - 6 * scale:.0f}" width="18" height="{6 * scale:.0f}" fill="var(--familien)"/></a>')
    o.append(f'<a href="{L}ende/koppius/3"><text x="{xb(1586) - 14:.0f}" y="{by - 6 * scale - 34:.0f}" text-anchor="end" font-size="13" fill="var(--ink)" text-decoration="underline">um 1586: 3 Klarissen</text>'
             f'<text x="{xb(1586) - 14:.0f}" y="{by - 6 * scale - 18:.0f}" text-anchor="end" font-size="13" fill="var(--familien)" text-decoration="underline">und 6 Augustinerinnen aus Pillenreuth</text></a>')
    o.append(f'<a href="{L}ende/koppius/4"><circle cx="{xb(1596):.0f}" cy="{by - 5}" r="6" fill="var(--familien)"/></a>')
    o.append(f'<a href="{L}ende/koppius/4"><text x="{xb(1596) - 10:.0f}" y="{by + 40}" text-anchor="end" font-size="12.5" fill="var(--ink)" text-decoration="underline">1591 die letzte Klarisse, 1596 die letzte Bewohnerin</text></a>')
    o.append(f'<a href="{L}ende/kaeterlein/3"><text x="{xb(1539):.0f}" y="{by - 36}" text-anchor="middle" font-size="12.5" fill="var(--ink2)" text-decoration="underline">1539: ‚die stärkste ist gestorben‘</text><line x1="{xb(1539):.0f}" y1="{by - 30}" x2="{xb(1539):.0f}" y2="{by}" stroke="var(--ink2)" stroke-dasharray="3 3"/></a>')
    o.append(f'<text x="16" y="{H - 8}" font-size="12.5" fill="var(--ink2)">Zwischen 1527 und 1586 gibt es keine Zahl; die Säulen sind keine Kurve. Violett: Klarissen; grün: Augustinerinnen aus Pillenreuth.</text>')
    o.append("</svg>")
    OUT.write_text("\n".join(o), encoding="utf-8")
    print(OUT.name)


main()
