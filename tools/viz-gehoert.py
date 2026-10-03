"""Draw assets/viz/gehoert.svg: who was heard in the Tetzel affair,
3 February to 3 March 1525. Every row links to its unit.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz" / "gehoert.svg"
L = "#/text/dieb/"

# (date, who asks / acts, text, outcome, href); outcome: ja | nein | still | info
ROWS = [
    ("3. Febr.", "Mutter", "spricht eine Stunde allein mit der Tochter am Kommunionfenster", "ja", "mutter/1"),
    ("Febr.", "Äbtissin", "bittet den Pfleger um Rat: keine soll gegen ihren Willen hinaus", "still", "mutter/3"),
    ("Febr.", "Onkel Fürer", "verlangen die Tochter heraus und wollen sie nicht anhören", "nein", "mutter/4"),
    ("Febr.", "Margaretha", "bittet den Pfleger, die Onkel sollen sie vorher anhören", "nein", "mutter/5"),
    ("Febr.", "Margaretha", "schreibt Sigmund Fürer; Antwort: nicht nötig zu kommen", "nein", "dieb/1"),
    ("Febr.", "Margaretha", "‚verhört man doch einen Dieb, ehe man ihn henkt‘", "info", "dieb/2"),
    ("Febr.", "Äbtissin", "bittet um ein öffentliches Verfahren vor den alten Herren", "vertagt", "dieb/2"),
    ("Febr.", "Pfleger", "rät zu warten: der Rat entscheide nicht ohne Anhörung der Parteien", "info", "dieb/3"),
    ("Febr.", "Mutter", "klagt beim Rat; der Rat schickt die Klage dem Kloster", "ja", "klage/1"),
    ("Febr.", "Konvent", "antwortet schriftlich: man möge Margaretha selbst befragen", "still", "klage/4"),
    ("3. März", "Rat", "Religionsgespräch auf dem Rathaus, ‚meistens gegen die Barfüßer‘", "info", "klage/6"),
]
COL = {"ja": "familien", "nein": "rat", "still": "nachwelt", "vertagt": "nachwelt", "info": "konvent"}
LAB = {"ja": "angehört", "nein": "abgewiesen", "still": "keine Antwort", "vertagt": "vertröstet", "info": ""}

W, top, rh = 900, 92, 44
H = top + len(ROWS) * rh + 150


def main():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="gh-t gh-t2" font-family="var(--serif)">',
         '<title id="gh-t">Wer wurde angehört? Die Sache Tetzel, Februar bis März 1525</title>',
         '<desc id="gh-t2">Elf Schritte vom Besuch der Mutter bis zum Religionsgespräch, jeweils mit dem Ergebnis: angehört, abgewiesen oder keine Antwort.</desc>',
         '<text x="16" y="30" font-size="17" font-weight="bold" fill="var(--ink)">Wer wurde angehört? Februar bis März 1525</text>',
         '<text x="16" y="50" font-size="13" fill="var(--ink2)">Jede Zeile führt zur Stelle. Farbe: was aus der Bitte wurde.</text>']
    lx = [[40, "ja"], [190, "nein"], [345, "still"]]
    for x, k in lx:
        o.append(f'<circle cx="{x}" cy="70" r="7" fill="var(--{COL[k]})"/><text x="{x + 13}" y="75" font-size="13" fill="var(--ink2)">{LAB[k]}</text>')
    o.append(f'<line x1="132" y1="{top - 8}" x2="132" y2="{top + len(ROWS) * rh - 14}" stroke="var(--line)" stroke-width="2"/>')
    for i, (d, who, txt, res, href) in enumerate(ROWS):
        y = top + i * rh
        c = COL[res]
        o.append(f'<a href="{L}{href}"><g>')
        o.append(f'<text x="16" y="{y + 14}" font-size="13" fill="var(--ink2)">{escape(d)}</text>')
        if res == "info":
            o.append(f'<rect x="126" y="{y + 3}" width="12" height="12" fill="var(--panel)" stroke="var(--{c})" stroke-width="2" transform="rotate(45 132 {y + 9})"/>')
        else:
            o.append(f'<circle cx="132" cy="{y + 9}" r="8" fill="var(--{c})"/>')
        bold = ' font-weight="bold"' if who == "Margaretha" else ""
        o.append(f'<text x="152" y="{y + 14}" font-size="14"{bold} fill="var(--ink)">{escape(who)}</text>')
        o.append(f'<text x="262" y="{y + 14}" font-size="14" fill="var(--ink)" text-decoration="underline">{escape(txt)}</text>')
        if LAB[res]:
            o.append(f'<text x="{W - 16}" y="{y + 14}" text-anchor="end" font-size="12.5" fill="var(--{c})">{LAB[res]}</text>')
        o.append("</g></a>")
    y = top + len(ROWS) * rh + 10
    o.append(f'<line x1="16" y1="{y}" x2="{W - 16}" y2="{y}" stroke="var(--line)"/>')
    summ = [("Die Mutter", "angehört: eine Stunde am Fenster; ihre Klage nimmt der Rat an.", "familien"),
            ("Das Kloster", "angehört: schriftlich, aber ohne Bescheid.", "nachwelt"),
            ("Margaretha", "bis zum März von niemandem angehört: nicht von den Onkeln, nicht vom Pfleger, nicht vom Rat.", "rat")]
    for i, (a, b, c) in enumerate(summ):
        yy = y + 30 + i * 26
        o.append(f'<text x="16" y="{yy}" font-size="14.5" font-weight="bold" fill="var(--{c})">{escape(a)}</text>')
        o.append(f'<text x="130" y="{yy}" font-size="14" fill="var(--ink)">{escape(b)}</text>')
    o.append(f'<text x="16" y="{H - 18}" font-size="12.5" fill="var(--ink2)">Alles nach Caritas’ Aufzeichnungen; die Gegenseite spricht nur in den Briefen und der Klage, die sie abschrieb.</text>')
    o.append("</svg>")
    OUT.write_text("\n".join(o), encoding="utf-8")
    print(OUT.name)


main()
