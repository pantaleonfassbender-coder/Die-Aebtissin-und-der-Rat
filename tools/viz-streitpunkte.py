"""Draw assets/viz/streitpunkte.svg: where Melanchthon and the abbess agreed and
where not, as Caritas reports it, set against the positions of the council's
side (Nützel, Linck, the articles of June). Every row links to its unit.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz" / "streitpunkte.svg"

# question, abbess, Melanchthon (per Caritas), council side, href, href of council source
ROWS = [
    ("Gnade oder Werke?", "Grund allein in Gottes Gnade", "einig", "Vorwurf: sie bauten auf Werke", "#/text/melanchthon/besuch/3", "#/text/sindflut/supplik/4"),
    ("Kann man im Kloster selig werden?", "ja", "ja, wenn man nichts auf die Gelübde hält", "nein, es sei ‚des Teufels‘", "#/text/melanchthon/besuch/3", "#/text/sindflut/anfang/2"),
    ("Binden die Gelübde?", "ja, sie gelten Gott", "nein", "nein, sie gelten nichts", "#/text/melanchthon/besuch/3", "#/text/prediger/artikel/2"),
    ("Töchter gegen ihren Willen herausholen?", "nein", "nein, große Sünde (nach Hörensagen)", "ja, Gehorsam gegen die Eltern", "#/text/melanchthon/besuch/4", "#/text/prediger/artikel/1"),
    ("Klöster zerstören?", "nein", "nein, in ihrem Wesen lassen (nach Hörensagen)", "erwogen: Alte zusammenlegen, Junge hinaus", "#/text/melanchthon/besuch/4", "#/text/melanchthon/besuch/4"),
    ("Soll der Pfleger bleiben?", "ja, ‚unsertwegen keine Kündigung‘", "ja, er rät es Nützel", "Nützel drohte zu kündigen", "#/text/melanchthon/besuch/6", "#/text/melanchthon/besuch/5"),
]
AGREE = [True, True, False, True, True, True]
W, top, rh = 900, 112, 58
H = top + len(ROWS) * rh + 56
C = [16, 250, 470, 690]


def wrap(t, n):
    words, lines, cur = t.split(), [], ""
    for w in words:
        if len(cur) + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return lines[:3]


def main():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="sp-t sp-d" font-family="var(--serif)">',
         '<title id="sp-t">Worin die Äbtissin und Melanchthon übereinstimmten</title>',
         '<desc id="sp-d">Sechs Streitfragen von 1525 mit den Positionen der Äbtissin, Melanchthons nach Caritas’ Bericht und der Seite des Rates. Nur in der Frage der Gelübde waren Äbtissin und Melanchthon uneins.</desc>',
         '<text x="16" y="30" font-size="17" font-weight="bold" fill="var(--ink)">Worin sie übereinstimmten, und worin nicht</text>',
         '<text x="16" y="50" font-size="13" fill="var(--ink2)">Melanchthons Positionen nach Caritas’ Bericht; seine eigenen Worte sind hier nicht überliefert.</text>']
    heads = [("FRAGE", "ink2"), ("DIE ÄBTISSIN", "konvent"), ("MELANCHTHON", "reform"), ("RAT, PFLEGER, PREDIGER", "rat")]
    for (h, c), x in zip(heads, C):
        o.append(f'<text x="{x + (8 if x > 16 else 0)}" y="{top - 14}" font-size="12" font-weight="bold" fill="var(--{c})">{h}</text>')
    for i, (q, a, m, r, href, rhref) in enumerate(ROWS):
        y = top + i * rh
        ok = AGREE[i]
        o.append(f'<rect x="8" y="{y}" width="{W - 16}" height="{rh - 6}" rx="6" fill="var(--panel)" stroke="var(--line)"/>')
        if not ok:
            o.append(f'<rect x="{C[1]}" y="{y}" width="{C[3] - C[1] - 6}" height="{rh - 6}" rx="6" fill="none" stroke="var(--rat)" stroke-width="2" stroke-dasharray="5 3"/>')
        else:
            o.append(f'<rect x="{C[1]}" y="{y}" width="{C[3] - C[1] - 6}" height="{rh - 6}" rx="6" fill="var(--familien)" opacity="0.10"/>')
        for j, ln in enumerate(wrap(q, 28)):
            o.append(f'<text x="{C[0] + 6}" y="{y + 20 + j * 16}" font-size="13.5" font-weight="bold" fill="var(--ink)">{escape(ln)}</text>')
        for col, txt, link in ((1, a, href), (2, m, href), (3, r, rhref)):
            o.append(f'<a href="{link}">')
            for j, ln in enumerate(wrap(txt, 27)):
                o.append(f'<text x="{C[col] + 8}" y="{y + 20 + j * 16}" font-size="13" fill="var(--ink)" text-decoration="underline">{escape(ln)}</text>')
            o.append("</a>")
    o.append(f'<rect x="16" y="{H - 34}" width="14" height="14" fill="var(--familien)" opacity="0.25"/><text x="36" y="{H - 22}" font-size="12.5" fill="var(--ink2)">Äbtissin und Melanchthon einig</text>')
    o.append(f'<rect x="280" y="{H - 34}" width="14" height="14" fill="none" stroke="var(--rat)" stroke-width="2" stroke-dasharray="4 2"/><text x="300" y="{H - 22}" font-size="12.5" fill="var(--ink2)">uneins: ‚nur der Gelübde halb kunten wir nit eins werden‘</text>')
    o.append("</svg>")
    OUT.write_text("\n".join(o), encoding="utf-8")
    print(OUT.name)


main()
