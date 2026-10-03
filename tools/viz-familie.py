"""Draw assets/viz/familie.svg: the Pirckheimer women in the cloisters and
Willibald as the link to council, reformers and humanists. Every node and
edge links to the unit that documents it.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz" / "familie.svg"
T = "#/text/"
W, H, NW, NH = 900, 600, 172, 54

# id: (x, y, name, line, colour, href)
NODES = {
    "willibald": (450, 300, "Willibald", "Ratsherr, Humanist, † 1530", "nachwelt", T + "willibald/melanchthon/1"),
    "caritas": (180, 150, "Caritas", "Äbtissin 1503–1532", "konvent", T + "ende/koppius/2"),
    "klara": (180, 300, "Klara", "Schwester; Äbtissin 1532/33", "konvent", T + "willibald/klara/1"),
    "toechter": (180, 450, "zwei Töchter", "in St. Klara (Brief 1525)", "konvent", T + "willibald/melanchthon/1"),
    "katharina": (180, 555, "Katharina", "Äbtissin 1533–1563", "konvent", T + "ende/koppius/2"),
    "bergen": (450, 520, "Sabina, Euphemia", "Äbtissinnen in Bergen", "konvent", T + "ende/koppius/2"),
    "melanchthon": (735, 120, "Melanchthon", "Brief 1525; Besuch Nov. 1525", "reform", T + "willibald/melanchthon/1"),
    "rat": (735, 300, "Der Rat", "‚Patres conscripti‘, 1530", "rat", T + "willibald/oratio/2"),
    "celtis": (450, 90, "Celtis", "Lehrer der Schwester, 1502", "nachwelt", T + "gelehrte/celtis/8"),
    "pfleger": (735, 470, "Kaspar Nützel", "Pfleger; Antworten mit Rat", "rat", T + "willibald/klara/4"),
}
# (a, b, label, href, dashed)
EDGES = [
    ("willibald", "caritas", "Bücher, Korrektur, Rat", T + "gelehrte/bruder/4", False),
    ("klara", "willibald", "‚keinen Menschen außer dir‘", T + "willibald/klara/1", False),
    ("willibald", "toechter", "‚ich irrte mit den anderen‘", T + "willibald/melanchthon/1", False),
    ("toechter", "katharina", "eine von ihnen?", T + "willibald/klara/2", True),
    ("willibald", "bergen", "Schwestern (Müllner, nach Höfler)", T + "ende/koppius/2", True),
    ("willibald", "melanchthon", "bittet um Hilfe", T + "willibald/melanchthon/3", False),
    ("willibald", "rat", "Rede im Namen der Nonnen", T + "willibald/oratio/6", False),
    ("willibald", "celtis", "Freund, 1502", T + "gelehrte/celtis/8", False),
    ("willibald", "pfleger", "‚stell ihr eine Form‘", T + "willibald/klara/4", True),
]


def cut(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    L = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / L, dy / L

    def c(x, y, sx, sy):
        tx = (NW / 2 + 5) / abs(sx) if sx else 1e9
        ty = (NH / 2 + 5) / abs(sy) if sy else 1e9
        t = min(tx, ty)
        return x + sx * t, y + sy * t
    return c(x1, y1, ux, uy), c(x2, y2, -ux, -uy)


def main():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="fa-t fa-d" font-family="var(--serif)">',
         '<title id="fa-t">Die Pirckheimer und das Kloster</title>',
         '<desc id="fa-d">Willibald Pirckheimer in der Mitte; links die Frauen der Familie in St. Klara (Caritas, Klara, zwei Töchter, darunter Katharina), unten Sabina und Euphemia in Bergen; rechts Melanchthon, der Rat und der Pfleger; oben Celtis.</desc>',
         '<defs><marker id="fa-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--ink2)"/></marker></defs>',
         '<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">Die Pirckheimer und das Kloster</text>',
         '<text x="16" y="47" font-size="13" fill="var(--ink2)">Violett: Frauen der Familie im Kloster. Gestrichelt: nur erschlossen oder aus zweiter Hand.</text>',
         f'<rect x="60" y="100" width="240" height="490" rx="14" fill="var(--konvent)" opacity="0.06"/>',
         '<text x="70" y="120" font-size="12.5" fill="var(--konvent)">St. Klara, Nürnberg</text>']
    labels = []
    for a, b, lab, href, dashed in EDGES:
        (x1, y1), (x2, y2) = cut(*NODES[a][:2], *NODES[b][:2])
        d = ' stroke-dasharray="6 4"' if dashed else ""
        o.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="var(--ink2)" stroke-width="1.4"{d} marker-end="url(#fa-a)"/>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - (20 if abs(y2 - y1) < 5 else 6)
        labels.append(f'<a href="{href}"><text x="{mx:.0f}" y="{my:.0f}" text-anchor="middle" font-size="12.5" fill="var(--ink)" stroke="var(--panel)" stroke-width="5" paint-order="stroke" text-decoration="underline">{escape(lab)}</text></a>')
    for nid, (x, y, name, line, c, href) in NODES.items():
        bold = nid == "willibald"
        o.append(f'<a href="{href}"><g><rect x="{x - NW / 2}" y="{y - NH / 2}" width="{NW}" height="{NH}" rx="8" fill="var(--panel)" stroke="var(--{c})" stroke-width="{2.4 if bold else 1.5}"/>'
                 f'<text x="{x}" y="{y - 4}" text-anchor="middle" font-size="15" font-weight="{"bold" if bold else "normal"}" fill="var(--{c})">{escape(name)}</text>'
                 f'<text x="{x}" y="{y + 14}" text-anchor="middle" font-size="11.5" fill="var(--ink2)">{escape(line)}</text></g></a>')
    o += labels
    o.append("</svg>")
    OUT.write_text("\n".join(o), encoding="utf-8")
    print(OUT.name)


main()
