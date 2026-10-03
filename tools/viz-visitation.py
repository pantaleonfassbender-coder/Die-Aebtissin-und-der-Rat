"""Draw assets/viz/visitation.svg: the 52 sisters at the secular visitation of
All Souls 1527 (16 heard first, 23 heard after the abbess intervened, 13 who
refused), and the council's measures 1525-1528. Every element links.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz" / "visitation.svg"
W, H = 900, 520
L = "#/text/ordnung/"

GROUPS = [(16, "zuerst einzeln befragt", "reform"), (23, "nach Zureden der Äbtissin befragt", "nachwelt"), (13, "verweigert", "konvent")]
STEPS = [
    ("Aug. 1525", "Wein nur mit Zettel vom Ungelter", L + "visitation/1"),
    ("2. Jan. 1526", "der Biermesser", L + "visitation/1"),
    ("Nov. 1527", "300 Gulden gefordert", L + "visitation/5"),
    ("2. Nov. 1527", "weltliche Visitation", L + "visitation/2"),
    ("24. Febr. 1528", "Anna Schwarz geht", L + "anna/3"),
    ("10. März 1528", "Rückzahlung, Quittung", L + "anna/4"),
    ("1. Aug. 1528", "Antwort an den Bischof", L + "bamberg/1"),
]


def main():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="vi-t vi-d" font-family="var(--serif)">',
         '<title id="vi-t">Die 52 Schwestern bei der Visitation 1527</title>',
         '<desc id="vi-d">52 Punkte für die Schwestern des Konvents: 16 zuerst einzeln befragt, 23 nach Zureden der Äbtissin, 13 verweigerten. Darunter die Eingriffe des Rates von 1525 bis 1528.</desc>',
         '<text x="16" y="30" font-size="17" font-weight="bold" fill="var(--ink)">Allerseelen 1527: 52 Schwestern, einzeln befragt?</text>',
         '<text x="16" y="50" font-size="13" fill="var(--ink2)">Zahlen nach Caritas, Höfler S. 184. Ein Punkt je Schwester.</text>']
    x0, y0, step, per_row = 40, 92, 30, 26
    i = 0
    for n, lab, c in GROUPS:
        for _ in range(n):
            x = x0 + (i % per_row) * step
            y = y0 + (i // per_row) * step
            o.append(f'<a href="{L}visitation/6"><circle cx="{x}" cy="{y}" r="11" fill="var(--{c})"/></a>')
            i += 1
    ly = y0 + 2 * step + 10
    lx = 16
    for n, lab, c in GROUPS:
        o.append(f'<circle cx="{lx + 10}" cy="{ly + 14}" r="8" fill="var(--{c})"/><text x="{lx + 26}" y="{ly + 19}" font-size="14" fill="var(--ink)"><tspan font-weight="bold">{n}</tspan> {escape(lab)}</text>')
        lx += 70 + len(lab) * 7.6
    o.append(f'<text x="16" y="{ly + 50}" font-size="13" fill="var(--ink2)">Die Befragten blieben ‚fast alle‘ bei derselben Antwort; die Visitatoren: ‚sie pfeifen alle in ein Rohr‘.</text>')
    o.append(f'<text x="16" y="{ly + 68}" font-size="13" fill="var(--ink2)">Eine sprach vom Abendmahl unter beiderlei Gestalt: Anna Schwarz, die im Februar 1528 ging.</text>')
    ty = ly + 104
    o.append(f'<line x1="16" y1="{ty}" x2="{W - 16}" y2="{ty}" stroke="var(--line)"/>')
    o.append(f'<text x="16" y="{ty + 26}" font-size="14" font-weight="bold" fill="var(--ink)">Der Rat im Kloster, 1525–1528</text>')
    bw = (W - 32) / len(STEPS)
    for k, (d, t, href) in enumerate(STEPS):
        x = 16 + k * bw
        c = "rat" if k != 4 else "familien"
        o.append(f'<a href="{href}"><g><rect x="{x + 2}" y="{ty + 40}" width="{bw - 8}" height="74" rx="6" fill="var(--panel)" stroke="var(--{c})"/>'
                 f'<text x="{x + 9}" y="{ty + 60}" font-size="12.5" font-weight="bold" fill="var(--{c})">{escape(d)}</text>')
        words, lines, cur = t.split(), [], ""
        for w in words:
            if len(cur) + len(w) > 15:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        for j, ln in enumerate(lines[:3]):
            o.append(f'<text x="{x + 9}" y="{ty + 78 + j * 15}" font-size="12.5" fill="var(--ink)">{escape(ln)}</text>')
        o.append("</g></a>")
    o.append("</svg>")
    OUT.write_text("\n".join(o), encoding="utf-8")
    print(OUT.name)


main()
