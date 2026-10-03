"""Draw assets/viz/forderungen.svg: what the council demanded in spring 1525
and what the convent answered. Every row links to its unit.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz" / "forderungen.svg"
L = "#/text/prediger/"

# (date, demand, answer, status, href)
ROWS = [
    ("19. März", "ein Prediger des Rates", "angenommen: die Schwestern hören die Predigten", "nach", "oculi/2"),
    ("19. März", "ein Beichtvater aus drei Kandidaten des Rates", "abgelehnt; gewählt: Konrad Schrötter, Terziar, mit Erlaubnis des Guardians", "eigen", "prediger/2"),
    ("19. März", "keine Barfüßer mehr", "Protest vor Gott; am selben Abend vollzogen", "durch", "oculi/4"),
    ("7. Juni", "1  alle Gelübde lösen", "abgelehnt: ‚keine hat mir etwas gelobt, sondern Gott‘", "ab", "artikel/2"),
    ("7. Juni", "2  Töchter den Eltern herausgeben", "auch gegen ihren Willen; im Juni mit Gewalt vollzogen", "durch", "artikel/1"),
    ("7. Juni", "3  die Kutten ablegen", "aufgeschoben auf Rat von Freunden im Rat", "auf", "artikel/3"),
    ("7. Juni", "4  Gesichtsfenster, Gespräche ohne Zuhörerin", "ein einziges Gesichtsfenster; allein reden wollen die Schwestern nicht", "nach", "artikel/4"),
    ("7. Juni", "5  das Gut inventarisieren", "in diesem Modul nicht berichtet", "offen", "artikel/1"),
]
ST = {"nach": ("familien", "nachgegeben"), "ab": ("konvent", "verweigert"), "eigen": ("reform", "eigener Weg"),
      "durch": ("rat", "vom Rat durchgesetzt"), "auf": ("nachwelt", "aufgeschoben"), "offen": ("line", "offen")}

W, top, rh = 900, 104, 52
H = top + len(ROWS) * rh + 70


def main():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="fo-t fo-d" font-family="var(--serif)">',
         '<title id="fo-t">Was der Rat 1525 verlangte und was der Konvent antwortete</title>',
         '<desc id="fo-d">Acht Forderungen vom 19. März und 7. Juni 1525 mit der Antwort des Konvents: nachgegeben, verweigert, eigener Weg, aufgeschoben oder vom Rat durchgesetzt.</desc>',
         '<text x="16" y="30" font-size="17" font-weight="bold" fill="var(--ink)">Forderungen und Antworten, März bis Juni 1525</text>',
         '<text x="16" y="50" font-size="13" fill="var(--ink2)">Jede Zeile führt zur Stelle. Farbe: was aus der Forderung wurde.</text>']
    x = 16
    for k in ("nach", "eigen", "ab", "auf", "durch"):
        c, lab = ST[k]
        o.append(f'<rect x="{x}" y="64" width="14" height="14" rx="3" fill="var(--{c})"/><text x="{x + 20}" y="76" font-size="13" fill="var(--ink2)">{lab}</text>')
        x += 40 + len(lab) * 7
    o.append(f'<text x="16" y="{top - 8}" font-size="12" fill="var(--ink2)">DATUM</text><text x="100" y="{top - 8}" font-size="12" fill="var(--ink2)">FORDERUNG DES RATES</text><text x="470" y="{top - 8}" font-size="12" fill="var(--ink2)">ANTWORT DES KONVENTS</text>')
    for i, (d, dem, ans, st, href) in enumerate(ROWS):
        y = top + i * rh
        c, lab = ST[st]
        o.append(f'<a href="{L}{href}"><g>')
        o.append(f'<rect x="8" y="{y}" width="{W - 16}" height="{rh - 6}" rx="6" fill="var(--panel)" stroke="var(--line)"/>')
        o.append(f'<rect x="8" y="{y}" width="6" height="{rh - 6}" rx="3" fill="var(--{c})"/>')
        o.append(f'<text x="22" y="{y + 28}" font-size="13" fill="var(--ink2)">{escape(d)}</text>')
        o.append(f'<text x="100" y="{y + 28}" font-size="14" font-weight="bold" fill="var(--ink)">{escape(dem)}</text>')
        words, lines, cur = ans.split(), [], ""
        for w in words:
            if len(cur) + len(w) > 52:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        for j, ln in enumerate(lines[:2]):
            o.append(f'<text x="470" y="{y + 20 + j * 17}" font-size="13.5" fill="var(--{"ink" if st != "offen" else "ink2"})" text-decoration="underline">{escape(ln)}</text>')
        o.append("</g></a>")
    o.append(f'<text x="16" y="{H - 30}" font-size="12.5" fill="var(--ink2)">Die Forderungen 1–5 vom Pfingstmittwoch sollten in vier Wochen ‚zu Werk gezogen‘ werden.</text>')
    o.append(f'<text x="16" y="{H - 12}" font-size="12.5" fill="var(--ink2)">Wie Artikel 2 im Juni vollzogen wurde, erzählt das nächste Modul, ‚Da stee ich‘.</text>')
    o.append("</svg>")
    OUT.write_text("\n".join(o), encoding="utf-8")
    print(OUT.name)


main()
