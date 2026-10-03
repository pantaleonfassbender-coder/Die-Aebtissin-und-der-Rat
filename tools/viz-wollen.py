"""Draw assets/viz/wollen.svg: what the women wanted against what families,
council or prince did, in four fields. Every box links to the unit that
documents it.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz" / "wollen.svg"
T = "#/text/"
W, H = 900, 700
X0, X1, XM = 130, 870, 500
Y0, Y1, YM = 140, 680, 390
BW, BH = 330, 58

# field: (title, [(year, label, colour, href, dashed)])
FIELDS = {
    ("bleiben", "lassen"): ("Bleiben dürfen", [
        ("1523", "Luther: ‚die laß man bleiben‘", "reform", T + "vergleich/ursach/8", False),
        ("1525", "Melanchthon: ‚ebenso wohl im Kloster selig‘", "reform", T + "melanchthon/besuch/3", False),
    ]),
    ("hinaus", "lassen"): ("Gehen dürfen", [
        ("1524", "Konvent: keine ‚mit Gewalt‘ halten", "konvent", T + "sindflut/supplik/5", False),
        ("1528", "Anna Schwarz: ‚geh selbst heraus‘", "familien", T + "ordnung/anna/3", False),
    ]),
    ("bleiben", "zwingen"): ("Herausgeholt", [
        ("1525", "Drei Töchter: ‚Mutter meines Fleisches‘", "familien", T + "toechter/fronleichnam/4", False),
        ("1526", "Herzog Georg: ‚Gewalt und Unrecht‘", "rat", T + "vergleich/georg/2", True),
        ("1539", "Käterlein: will hinein, der Rat holt sie", "konvent", T + "ende/kaeterlein/4", False),
    ]),
    ("hinaus", "zwingen"): ("Festgehalten", [
        ("1523", "Nimbschen: die Eltern sagen nein", "reform", T + "vergleich/ursach/4", False),
        ("1523", "Luther: ‚O der unbarmherzigen Eltern‘", "reform", T + "vergleich/ursach/5", True),
    ]),
}


def main():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="wo-t wo-d" font-family="var(--serif)">',
         '<title id="wo-t">Wer will hinaus, wer darf bleiben</title>',
         '<desc id="wo-d">Vier Felder: waagerecht, ob die Frau bleiben oder hinaus will; senkrecht, ob Familie, Rat oder Fürst sie lassen oder zwingen. Oben links Luthers Satz ‚die laß man bleiben‘ und Melanchthon; oben rechts die Zusage des Konvents von 1524 und Anna Schwarz 1528; unten links die drei Töchter 1525, Herzog Georgs Vorwurf 1526 und das Glaser-Käterlein 1539; unten rechts die Nonnen von Nimbschen 1523.</desc>',
         '<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">Wer will hinaus, wer darf bleiben</text>',
         '<text x="16" y="48" font-size="13" fill="var(--ink2)">Luthers Regel und die Zusage des Konvents stehen beide in der oberen Reihe; gestritten wurde in der unteren.</text>',
         '<text x="16" y="66" font-size="13" fill="var(--ink2)">Gestrichelt: Behauptung oder Vorwurf, nicht ein einzelner Fall.</text>']
    # field backgrounds
    for (fx, fy) in FIELDS:
        x = X0 if fx == "bleiben" else XM
        y = Y0 if fy == "lassen" else YM
        w = (XM - X0) if fx == "bleiben" else (X1 - XM)
        h = (YM - Y0) if fy == "lassen" else (Y1 - YM)
        op = "0.05" if fy == "lassen" else "0.10"
        o.append(f'<rect x="{x + 4}" y="{y + 4}" width="{w - 8}" height="{h - 8}" rx="12" fill="var(--red)" opacity="{op}"/>')
    # axes
    o.append(f'<text x="{(X0 + XM) / 2}" y="{Y0 - 34}" text-anchor="middle" font-size="12.5" fill="var(--ink2)">Die Frau will …</text>')
    o.append(f'<text x="{(X0 + XM) / 2}" y="{Y0 - 14}" text-anchor="middle" font-size="15" font-weight="bold" fill="var(--ink)">bleiben</text>')
    o.append(f'<text x="{(XM + X1) / 2}" y="{Y0 - 34}" text-anchor="middle" font-size="12.5" fill="var(--ink2)">Die Frau will …</text>')
    o.append(f'<text x="{(XM + X1) / 2}" y="{Y0 - 14}" text-anchor="middle" font-size="15" font-weight="bold" fill="var(--ink)">hinaus</text>')
    for (ly, a, b) in ((Y0 + YM) / 2, "die anderen", "lassen sie"), ((YM + Y1) / 2, "die anderen", "zwingen sie"):
        o.append(f'<text transform="translate(52 {ly}) rotate(-90)" text-anchor="middle" font-size="12.5" fill="var(--ink2)">{a}</text>')
        o.append(f'<text transform="translate(74 {ly}) rotate(-90)" text-anchor="middle" font-size="15" font-weight="bold" fill="var(--ink)">{b}</text>')
    o.append(f'<line x1="{XM}" y1="{Y0}" x2="{XM}" y2="{Y1}" stroke="var(--line)" stroke-width="1.5"/>')
    o.append(f'<line x1="{X0}" y1="{YM}" x2="{X1}" y2="{YM}" stroke="var(--line)" stroke-width="1.5"/>')
    # boxes
    for (fx, fy), (title, items) in FIELDS.items():
        x = X0 if fx == "bleiben" else XM
        y = Y0 if fy == "lassen" else YM
        w = (XM - X0) if fx == "bleiben" else (X1 - XM)
        cx = x + w / 2
        o.append(f'<text x="{cx}" y="{y + 30}" text-anchor="middle" font-size="14" font-style="italic" fill="var(--ink2)">{escape(title)}</text>')
        for k, (yr, lab, c, href, dashed) in enumerate(items):
            by = y + 46 + k * (BH + 12)
            d = ' stroke-dasharray="6 4"' if dashed else ""
            o.append(f'<a href="{href}"><g><rect x="{cx - BW / 2}" y="{by}" width="{BW}" height="{BH}" rx="8" fill="var(--panel)" stroke="var(--{c})" stroke-width="1.6"{d}/>'
                     f'<text x="{cx}" y="{by + 23}" text-anchor="middle" font-size="13" font-weight="bold" fill="var(--{c})">{yr}</text>'
                     f'<text x="{cx}" y="{by + 44}" text-anchor="middle" font-size="13" fill="var(--ink)" text-decoration="underline">{escape(lab)}</text></g></a>')
    o.append("</svg>")
    OUT.write_text("\n".join(o), encoding="utf-8")
    print(OUT.name)


main()
