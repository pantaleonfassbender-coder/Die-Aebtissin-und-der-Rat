"""Draw assets/viz/drei.svg: the three daughters taken out on 14 June 1525,
their ages and years in the convent, and the five days from the fathers'
message to the handover. Every element links to its unit.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz" / "drei.svg"
L = "#/text/toechter/"
W, H = 900, 560

# name, age, years in convent, father, quote, href
D = [
    ("Margaretha Tetzel", 23, 9, "Vater Friedrich Tetzel †, Mutter Ursula, geb. Fürer",
     "zur Äbtissin: ‚o liebe Mutter, treibt uns nicht so von Euch‘", "fronleichnam/5"),
    ("Katharina Ebner", 20, 6, "Vater Hieronymus Ebner, Ratsherr",
     "‚Da stehe ich und will nicht weichen‘", "fronleichnam/6"),
    ("Clara Nützel", 19, 6, "Vater Kaspar Nützel, Pfleger des Klosters",
     "‚du weißt, dass es nicht mein Wille ist‘", "fronleichnam/7"),
]
DAYS = [
    ("Sa 10. Juni", "die Väter lassen es ausrichten", "vorher/1"),
    ("Mo 12. Juni", "vier Mütter am Tor", "vorher/2"),
    ("Di 13. Juni", "Klage vor dem Rat; Befehl", "vorher/3"),
    ("Mi 14. Juni", "Übergabe in der Kapelle", "fronleichnam/3"),
    ("13. Aug.", "Kostgeld angeboten, Töchter zurückverlangt", "danach/2"),
]


def main():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="dr-t dr-d" font-family="var(--serif)">',
         '<title id="dr-t">Die drei Töchter, Juni 1525</title>',
         '<desc id="dr-d">Margaretha Tetzel, Katharina Ebner und Clara Nützel: Alter, Jahre im Kloster, Alter beim Eintritt, ihre Väter und ein Satz jeder von ihnen; darunter die Tage vom 10. Juni bis zum 13. August 1525.</desc>',
         '<text x="16" y="30" font-size="17" font-weight="bold" fill="var(--ink)">Die drei Töchter</text>',
         '<text x="16" y="50" font-size="13" fill="var(--ink2)">Lebensjahre als Balken: hell vor dem Eintritt, dunkel im Kloster. Angaben nach Caritas, Höfler S. 102.</text>']
    x0, scale, top = 210, 20, 76
    for a in range(0, 25, 5):
        x = x0 + a * scale
        o.append(f'<line x1="{x}" y1="{top - 6}" x2="{x}" y2="{top + 3 * 110 - 30}" stroke="var(--line)"/>')
        o.append(f'<text x="{x}" y="{top - 10}" text-anchor="middle" font-size="11.5" fill="var(--ink2)">{a}</text>')
    for i, (name, age, yrs, father, quote, href) in enumerate(D):
        y = top + i * 110
        entry = age - yrs
        o.append(f'<a href="{L}{href}"><g>')
        o.append(f'<text x="16" y="{y + 20}" font-size="15.5" font-weight="bold" fill="var(--konvent)">{escape(name)}</text>')
        o.append(f'<text x="16" y="{y + 38}" font-size="12.5" fill="var(--ink2)">{age} Jahre, {yrs} im Kloster</text>')
        o.append(f'<rect x="{x0}" y="{y + 8}" width="{entry * scale}" height="22" fill="var(--familien)" opacity="0.35"/>')
        o.append(f'<rect x="{x0 + entry * scale}" y="{y + 8}" width="{yrs * scale}" height="22" fill="var(--konvent)"/>')
        o.append(f'<text x="{x0 + entry * scale - 4}" y="{y + 24}" text-anchor="end" font-size="12" fill="var(--ink)">Eintritt mit {entry}</text>')
        o.append(f'<text x="{x0 + age * scale + 8}" y="{y + 24}" font-size="12" fill="var(--rat)">14. Juni 1525</text>')
        o.append(f'<text x="{x0}" y="{y + 52}" font-size="12.5" fill="var(--ink2)">{escape(father)}</text>')
        o.append(f'<text x="{x0}" y="{y + 72}" font-size="14" font-style="italic" fill="var(--ink)" text-decoration="underline">{escape(quote)}</text>')
        o.append("</g></a>")
    y = top + 3 * 110 + 4
    o.append(f'<line x1="16" y1="{y}" x2="{W - 16}" y2="{y}" stroke="var(--line)"/>')
    o.append(f'<text x="16" y="{y + 24}" font-size="14" font-weight="bold" fill="var(--ink)">Die Tage</text>')
    bw = (W - 32) / len(DAYS)
    for i, (d, t, href) in enumerate(DAYS):
        x = 16 + i * bw
        c = "rat" if i == 3 else "ink2"
        o.append(f'<a href="{L}{href}"><g><rect x="{x + 2}" y="{y + 36}" width="{bw - 8}" height="62" rx="6" fill="var(--panel)" stroke="var(--{c})" stroke-width="{2 if i == 3 else 1}"/>'
                 f'<text x="{x + 10}" y="{y + 56}" font-size="13" font-weight="bold" fill="var(--{c})">{escape(d)}</text>')
        words, lines, cur = t.split(), [], ""
        for w in words:
            if len(cur) + len(w) > 22:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        for j, ln in enumerate(lines[:2]):
            o.append(f'<text x="{x + 10}" y="{y + 74 + j * 15}" font-size="12.5" fill="var(--ink)">{escape(ln)}</text>')
        o.append("</g></a>")
    o.append(f'<text x="16" y="{H - 10}" font-size="12.5" fill="var(--ink2)">Die Mütter nannten das Eintrittsalter ‚unverständige Jahre‘; der Konvent antwortete, die Töchter seien inzwischen verständig.</text>')
    o.append("</svg>")
    OUT.write_text("\n".join(o), encoding="utf-8")
    print(OUT.name)


main()
