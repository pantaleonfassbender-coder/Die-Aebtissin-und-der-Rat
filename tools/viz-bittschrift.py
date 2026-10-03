"""Draw assets/viz/bittschrift.svg: the way of the petition, Advent 1524,
and the three ages Caritas gives for the Franciscan order of the convent.

Injected inline by app.js (uses the page's CSS variables); every box links to
the unit that documents it.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz" / "bittschrift.svg"
W, H = 900, 680
L = "#/text/sindflut/"


def box(x, y, w, h, title, lines, href, colour, bold=False):
    t = [f'<a href="{href}"><g>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="var(--panel)" stroke="var(--{colour})" stroke-width="{2.2 if bold else 1.5}"/>',
         f'<text x="{x + w / 2}" y="{y + 21}" text-anchor="middle" font-size="15" font-weight="bold" fill="var(--{colour})">{escape(title)}</text>']
    for i, ln in enumerate(lines):
        t.append(f'<text x="{x + w / 2}" y="{y + 40 + i * 16}" text-anchor="middle" font-size="12.5" fill="var(--ink)">{escape(ln)}</text>')
    t.append("</g></a>")
    return "".join(t)


def arrow(x1, y1, x2, y2, dashed=False):
    d = ' stroke-dasharray="6 4"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="var(--ink2)" stroke-width="1.4"{d} marker-end="url(#bs-a)"/>'


def main():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="bs-t bs-d" font-family="var(--serif)">',
         '<title id="bs-t">Der Weg der Bittschrift, Advent 1524</title>',
         '<desc id="bs-d">Vom Gerücht über den Beschluss des Rates zur Beratung im Konvent, zu drei Briefen an Ratsherren, zur Bittschrift und zur Antwort des Rates; daneben die drei Angaben, wie lange die Franziskaner das Kloster schon betreuten.</desc>',
         '<defs><marker id="bs-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         '<path d="M0,0 L10,5 L0,10 z" fill="var(--ink2)"/></marker></defs>',
         '<text x="16" y="30" font-size="17" font-weight="bold" fill="var(--ink)">Der Weg der Bittschrift, Advent 1524</text>',
         '<text x="16" y="50" font-size="13" fill="var(--ink2)">Jedes Feld führt zur Stelle im Text.</text>']
    # flow, left column (x 16..556)
    o.append(box(16, 70, 260, 66, "Die Verwandten", ["predigen am Sprechfenster:", "‚wir wären alle des Teufels‘"], L + "anfang/2", "familien"))
    o.append(box(296, 70, 260, 66, "Das Gerücht", ["der Rat habe beschlossen,", "die Väter zu nehmen"], L + "anfang/3", "rat"))
    o.append(arrow(146, 136, 230, 170))
    o.append(arrow(426, 136, 340, 170))
    o.append(box(126, 172, 320, 66, "Der Konvent berät", ["alle stimmen für eine Bittschrift,", "‚keine ausgenommen‘"], L + "anfang/3", "konvent", bold=True))
    o.append(arrow(286, 238, 286, 262))
    o.append(box(126, 264, 320, 50, "Die Äbtissin entwirft und liest vor", [], L + "anfang/3", "konvent"))
    for i, (x, t, a, b, n) in enumerate([(16, "an Nützel", "den kranken Pfleger", "‚die Kinder sind unser beider‘", 1),
                                          (201, "an Ebner", "Tochter Katharina", "schreibt den Brief", 2),
                                          (386, "an Geuder", "den Schwager:", "‚lieber einen Henker‘", 3)]):
        o.append(arrow(286, 314, x + 85, 350))
        o.append(box(x, 352, 170, 70, t, [a, b], L + f"briefe/{n}", "konvent"))
        o.append(arrow(x + 85, 422, 286, 470, dashed=True))
    o.append(box(126, 472, 320, 66, "Die Bittschrift an den Rat", ["‚die vnverhört vnser‘:", "ohne uns gehört zu haben"], L + "supplik/1", "konvent", bold=True))
    o.append(arrow(286, 538, 286, 562))
    o.append(box(126, 564, 320, 66, "Die Antwort des Rates", ["‚in rw stellen‘: die Sache ruhen lassen", "‚piß auf weyttern bescheid‘"], L + "supplik/7", "rat", bold=True))
    o.append('<text x="286" y="660" text-anchor="middle" font-size="12.5" fill="var(--ink2)">gestrichelt: Die Briefe sollen der Bittschrift ‚Fortgang‘ verschaffen.</text>')

    # right column: how old is the order? (x 600..884)
    x0, y0 = 600, 80
    o.append(f'<text x="{x0}" y="{y0}" font-size="15" font-weight="bold" fill="var(--ink)">Wie alt ist die Ordnung?</text>')
    o.append(f'<text x="{x0}" y="{y0 + 18}" font-size="12.5" fill="var(--ink2)">Seit wann die Barfüßer das Kloster</text>')
    o.append(f'<text x="{x0}" y="{y0 + 34}" font-size="12.5" fill="var(--ink2)">betreuen, in Jahren bis 1524:</text>')
    bars = [("an Ebner: seit 1295", 229, "briefe/2", ""),
            ("an Nützel: ‚bei 300‘", 300, "briefe/1", ""),
            ("Bittschrift: ‚in 300‘", 300, "supplik/2", ""),
            ("an Geuder: ‚weit über 400‘", 400, "briefe/3", "+")]
    scale = 0.58
    for i, (lab, v, href, plus) in enumerate(bars):
        y = y0 + 64 + i * 62
        o.append(f'<a href="{L}{href}"><text x="{x0}" y="{y}" font-size="13" fill="var(--ink)" text-decoration="underline">{escape(lab)}</text></a>')
        o.append(f'<rect x="{x0}" y="{y + 8}" width="{v * scale:.0f}" height="20" rx="3" fill="var(--konvent)" opacity="{0.55 if plus else 0.8}"/>')
        if plus:
            o.append(f'<path d="M{x0 + v * scale:.0f},{y + 8} l14,10 l-14,10 z" fill="var(--konvent)" opacity="0.55"/>')
        o.append(f'<text x="{x0 + v * scale + (20 if plus else 6):.0f}" y="{y + 23}" font-size="13" fill="var(--ink2)">{v}{plus}</text>')
    yt = y0 + 64 + 4 * 62 + 4
    for i, ln in enumerate(["Gegen jeden Empfänger eine andere Zahl:",
                            "Caritas kam es auf das Alter der Ordnung",
                            "an, nicht auf das Jahr. Die Zahl 1295",
                            "nennt sie dem Ebner, weil ein Ebner",
                            "sie begründet haben soll."]):
        o.append(f'<text x="{x0}" y="{yt + i * 17}" font-size="12.5" fill="var(--ink2)">{escape(ln)}</text>')
    o.append("</svg>")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(o), encoding="utf-8")
    print(OUT.name)


main()
