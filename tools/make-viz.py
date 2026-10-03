"""Draw assets/viz/briefnetz.svg: who wrote to whom about Caritas, 1502-1515.

The SVG is injected inline by app.js, so it can use the page's CSS variables.
Every edge label links to the unit that documents it. Label positions are set
by hand, so that no label crosses another.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz" / "briefnetz.svg"
W, H, NW, NH = 900, 640, 150, 50
C1, C2, C3 = 120, 450, 780
R1, R2, R3, R4 = 95, 270, 435, 565

# id: (x, y, title, subtitle, colour variable)
NODES = {
    "erasmus": (C1, R1, "Erasmus", "Basel", "nachwelt"),
    "celtis": (C2, R1, "Konrad Celtis", "Dichter", "nachwelt"),
    "scheurl": (C3, R1, "Christoph Scheurl", "Bologna 1506", "nachwelt"),
    "willibald": (C1, R2, "Willibald", "Bruder, Lehrer", "nachwelt"),
    "caritas": (C2, R2, "Caritas", "Nonne, ab 1503 Äbtissin", "konvent"),
    "tucher": (C3, R2, "Sixtus Tucher", "an Caritas und Apollonia", "nachwelt"),
    "franz": (C1, R3, "Die Franziskaner", "‚Holzfüße‘, Beichtväter", "red"),
    "klara": (C2, R3, "Klara", "Schwester, Nonne", "konvent"),
    "peypus": (C3, R3, "Peypus, Drucker", "Nürnberg 1515", "gold"),
    "muench": (C3, R4, "Ernst Münch", "Herausgeber 1826", "nachwelt"),
}

# (from, to, label lines, href, offset, dashed, (label x, label y, anchor))
EDGES = [
    ("celtis", "caritas", ["Roswitha,", "Nürnberg-Buch, Ode"], "#/text/gelehrte/celtis/3", 14, False, (C2 - 24, 175, "end")),
    ("caritas", "celtis", ["Trost, Mahnung,", "1502"], "#/text/gelehrte/celtis/1", 14, False, (C2 + 24, 165, "start")),
    ("caritas", "willibald", ["Abschrift zur Korrektur"], "#/text/gelehrte/celtis/8", 12, False, ((C1 + C2) / 2, R2 - 20, "middle")),
    ("willibald", "caritas", ["Plutarch, Prudentius,", "Hieronymus"], "#/text/gelehrte/bruder/1", 12, False, ((C1 + C2) / 2, R2 + 34, "middle")),
    ("willibald", "celtis", ["1504: ‚Äbtissin geworden‘"], "#/text/gelehrte/bruder/5", 0, False, (318, 150, "middle")),
    ("willibald", "erasmus", ["‚sie lesen das", "Neue Testament‘"], "#/text/gelehrte/bruder/6", 0, False, (C1 + 10, 175, "start")),
    ("franz", "caritas", ["verbieten das Latein"], "#/text/gelehrte/bruder/5", 0, True, (262, 365, "middle")),
    ("scheurl", "caritas", ["Brief und Büchlein 1506"], "#/text/gelehrte/scheurl/1", 0, False, (668, 160, "start")),
    ("tucher", "caritas", ["geistliche Briefe"], "#/text/gelehrte/scheurl/3", 0, False, (615, R2 - 9, "middle")),
    ("caritas", "peypus", ["Briefe ‚durch Zufall‘", "gedruckt"], "#/text/gelehrte/scheurl/4", 0, True, (640, 345, "start")),
    ("caritas", "klara", ["lesen zusammen"], "#/text/gelehrte/bruder/4", 0, False, (C2 + 10, 360, "start")),
    ("peypus", "muench", ["übersetzt,", "widerspricht"], "#/text/gelehrte/muench/2", 0, True, (C3 + 10, 495, "start")),
]


def edge_points(a, b, off):
    (x1, y1), (x2, y2) = NODES[a][:2], NODES[b][:2]
    dx, dy = x2 - x1, y2 - y1
    L = (dx * dx + dy * dy) ** 0.5
    nx, ny = -dy / L, dx / L  # normal: the same offset puts a->b and b->a on opposite sides
    x1, y1, x2, y2 = x1 + nx * off, y1 + ny * off, x2 + nx * off, y2 + ny * off
    ux, uy = dx / L, dy / L

    def cut(x, y, sx, sy):  # from the centre (x, y) to just outside the box, in direction (sx, sy)
        tx = (NW / 2 + 6) / abs(sx) if sx else 1e9
        ty = (NH / 2 + 6) / abs(sy) if sy else 1e9
        t = min(tx, ty)
        return x + sx * t, y + sy * t

    return cut(x1, y1, ux, uy), cut(x2, y2, -ux, -uy)


def main():
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="bn-t bn-d" font-family="var(--serif)">',
           '<title id="bn-t">Briefnetz um Caritas Pirckheimer, 1502–1515</title>',
           '<desc id="bn-d">Wer wem über Caritas schrieb oder schickte: Celtis, Willibald, Scheurl, Sixtus Tucher, Erasmus, der Drucker Peypus, die Franziskaner, und Münch 1826. Jede Beschriftung verlinkt die Stelle im Modul.</desc>',
           '<defs><marker id="bn-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           '<path d="M0,0 L10,5 L0,10 z" fill="var(--ink2)"/></marker>'
           '<marker id="bn-r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           '<path d="M0,0 L10,5 L0,10 z" fill="var(--red)"/></marker></defs>',
           '<text x="16" y="30" font-size="17" font-weight="bold" fill="var(--ink)">Briefnetz, 1502–1515</text>',
           '<text x="16" y="50" font-size="13" fill="var(--ink2)">Wer an wen schrieb oder schickte. Die Beschriftungen führen zur Stelle.</text>']
    labels = []
    for a, b, lines, href, off, dashed, (lx, ly, anchor) in EDGES:
        (x1, y1), (x2, y2) = edge_points(a, b, off)
        red = a == "franz"
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="var(--{"red" if red else "ink2"})" '
                   f'stroke-width="1.4"{dash} marker-end="url(#bn-{"r" if red else "a"})"/>')
        tsp = "".join(f'<tspan x="{lx:.0f}" dy="{0 if i == 0 else 16}">{escape(t)}</tspan>' for i, t in enumerate(lines))
        labels.append(f'<a href="{href}"><text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anchor}" font-size="14" fill="var(--ink)" '
                      f'stroke="var(--panel)" stroke-width="5" paint-order="stroke" text-decoration="underline">{tsp}</text></a>')
    for nid, (x, y, t, sub, colour) in NODES.items():
        main_ = nid == "caritas"
        out.append(f'<g><rect x="{x - NW / 2}" y="{y - NH / 2}" width="{NW}" height="{NH}" rx="8" fill="var(--panel)" '
                   f'stroke="var(--{colour})" stroke-width="{2.4 if main_ else 1.6}"/>'
                   f'<text x="{x}" y="{y - 3}" text-anchor="middle" font-size="16"{" font-weight=\"bold\"" if main_ else ""} fill="var(--{colour})">{escape(t)}</text>'
                   f'<text x="{x}" y="{y + 15}" text-anchor="middle" font-size="12" fill="var(--ink2)">{escape(sub)}</text></g>')
    out += labels
    out.append(f'<text x="16" y="{H - 30}" font-size="12.5" fill="var(--ink2)">Gestrichelt: ohne Zutun der Schreiberin (das Verbot, der Druck) und die spätere Lektüre.</text>')
    out.append(f'<text x="16" y="{H - 12}" font-size="12.5" fill="var(--ink2)">Das Verbot und Willibalds Sätze an Celtis und Erasmus kennt der Apparat nur aus Münchs Zitaten.</text>')
    out.append("</svg>")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(OUT.name, len(EDGES), "Kanten")


main()
