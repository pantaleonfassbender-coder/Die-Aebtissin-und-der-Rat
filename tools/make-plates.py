"""Download and scale plate images into assets/plates/<id>.jpg and <id>_t.jpg.

    python tools/make-plates.py            # all plates listed below
    python tools/make-plates.py roswitha1501

Commons files are fetched as 1400-pixel renderings via the API; Internet
Archive page images are fetched directly and cropped (box in per mille).
"""
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "assets" / "plates"
UA = {"User-Agent": "Mozilla/5.0 (research; Die Aebtissin und der Rat)"}

PLATES = {
    "roswitha1501": ("commons", "File:Roswitha van Gandersheim biedt keizer Otto I een exemplaar van haar boek aan, RP-P-OB-1508.jpg", None),
    "celtis1507": ("commons", "File:Hans Burgkmair I, Conrad Celtis, 1507, NGA 39803.jpg", None),
    "pirckheimer1524": ("commons", "File:Albrecht Dürer, Willibald Pirckheimer, 1524, NGA 132982.jpg", None),
    "opera_ode": ("ia", "https://archive.org/download/bub_gb_XFSzOVms1AoC/page/n383_w1400.jpg", (20, 20, 1000, 930)),
    # Modul 2
    "hoefler_s3": ("ia", "https://archive.org/download/11420769bsb/page/n121_w1400.jpg", (60, 290, 900, 935)),
    "nuernberg1493": ("commons", "File:Nuremberg chronicles - Nuremberga.png", None),
    "klara1680": ("commons", "File:Kupferstich - Nürnberg - Königstraße - St Clara - A Graff - 1680.jpg", None),
    "klara_innen1725": ("commons", "File:J. A. Delsenbach St. Klara Nuernberg 1725.jpg", None),
    # Modul 3
    "hoefler_s24": ("ia", "https://archive.org/download/11420769bsb/page/n142_w1400.jpg", (100, 60, 1000, 600)),
    "wappen_tetzel": ("commons", "File:Tetzel Siebmacher205 - Nürnberg.jpg", None),
    "wappen_fuerer": ("commons", "File:Fürer Siebmacher205 - Nürnberg.jpg", None),
    "rathaussaal1730": ("commons", "File:Kupferstich - Rathaussaal Nürnberg - Probst - um 1730.JPG", None),
    # Modul 4
    "hoefler_s33": ("ia", "https://archive.org/download/11420769bsb/page/n151_w1400.jpg", (100, 470, 1000, 960)),
    "hoefler_s51": ("ia", "https://archive.org/download/11420769bsb/page/n169_w1400.jpg", (60, 40, 960, 960)),
    "hoefler_s89": ("ia", "https://archive.org/download/11420769bsb/page/n207_w1400.jpg", (60, 560, 960, 935)),
    "osiander1544": ("commons", "File:Andreas-Osiander.jpg", None),
    "lorenz1685": ("commons", "File:Kupferstich - Nürnberg - Lorenzkirche - von innen - Graff - 1685.jpg", None),
    # Modul 5
    "hoefler_s104": ("ia", "https://archive.org/download/11420769bsb/page/n222_w1400.jpg", (60, 40, 960, 560)),
    "hoefler_s106": ("ia", "https://archive.org/download/11420769bsb/page/n224_w1400.jpg", (60, 330, 1000, 700)),
    "hoefler_s107": ("ia", "https://archive.org/download/11420769bsb/page/n225_w1400.jpg", (60, 650, 960, 960)),
    "obstmarkt1725": ("commons", "File:Kupferstich - Nürnberg - Der Obstmarckt zu Nürnberg - Delsenbach - 1725.jpg", None),
    # Modul 6
    "melanchthon1526": ("commons", "File:Albrecht Dürer, Philip Melanchthon, 1526, NGA 6670.jpg", None),
    "link_portrait": ("commons", "File:Wenzeslaus-Linck.jpg", None),
    "hoefler_s171": ("ia", "https://archive.org/download/11420769bsb/page/n289_w1400.jpg", (60, 300, 960, 960)),
    "hoefler_s133": ("ia", "https://archive.org/download/11420769bsb/page/n251_w1400.jpg", (60, 280, 960, 800)),
    # Modul 7
    "hoefler_s184": ("ia", "https://archive.org/download/11420769bsb/page/n302_w1400.jpg", (60, 160, 960, 960)),
    "hoefler_s189": ("ia", "https://archive.org/download/11420769bsb/page/n307_w1400.jpg", (60, 160, 960, 960)),
    "redwitz": ("commons", "File:Weigand von Redwitz.jpg", None),
    "landsknecht_breu": ("commons", "File:Jörg Breu Landsknecht.jpg", None),
    # Modul 9
    "hoefler_s192": ("ia", "https://archive.org/download/11420769bsb/page/n310_w1400.jpg", (60, 40, 960, 960)),
    "hoefler_s204": ("ia", "https://archive.org/download/11420769bsb/page/n322_w1400.jpg", (60, 40, 960, 700)),
    "hoefler_s206": ("ia", "https://archive.org/download/11420769bsb/page/n324_w1400.jpg", (60, 260, 960, 760)),
    "pillenreuth_boener": ("commons", "File:Johann Alexander Böner Wahrhafte Abriße 169 Kloster Pillenreuth.jpg", None),
    # Modul Willibald
    "pirckheimer1503": ("commons", "File:Dürer, Profilbildnis des Willibald Pirckheimer, 1503, Kohle, 28,2 x 20,8 cm (SMB).jpg", None),
    "exlibris_pirckheimer": ("commons", "File:Dürer, Albrecht Exlibris Wilibald Pirkheimer.jpg", None),
    "opera_s374": ("ia", "https://archive.org/download/bub_gb_XFSzOVms1AoC/page/n414_w1400.jpg", (20, 650, 1000, 960)),
    "opera_s384": ("ia", "https://archive.org/download/bub_gb_XFSzOVms1AoC/page/n424_w1400.jpg", (20, 20, 1000, 520)),
    # Modul Luther und die Nonnen
    "bora1526": ("commons", "File:Lucas Cranach der Ältere - Porträt von Katharina von Bora (unter Beteiligung der Werkstatt), 1526, B 94.jpg", (320, 50, 985, 895)),
    "georg_cranach": ("commons", "File:Lucas Cranach d.Ä. - Bildnis Georgs des Bärtigen, Herzog von Sachsen (Museum der bildenden Künste).jpg", None),
    "wa_s394": ("ia", "https://archive.org/download/werkekritischege11luthuoft/page/n451_w1400.jpg", (60, 40, 960, 520)),
    "wa_s400": ("ia", "https://archive.org/download/werkekritischege11luthuoft/page/n457_w1400.jpg", (60, 380, 960, 655)),
    "hoefler_lxv": ("ia", "https://archive.org/download/11420769bsb/page/n71_w1400.jpg", (60, 60, 960, 535)),
}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()


def commons_url(title):
    q = urllib.parse.urlencode({"action": "query", "titles": title, "prop": "imageinfo",
                                "iiprop": "url", "iiurlwidth": 1400, "format": "json"})
    data = json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))
    page = next(iter(data["query"]["pages"].values()))
    return page["imageinfo"][0]["thumburl"]


def make(pid):
    kind, src, box = PLATES[pid]
    im = Image.open(io.BytesIO(get(commons_url(src) if kind == "commons" else src))).convert("RGB")
    if box:
        W, H = im.size
        im = im.crop((W * box[0] // 1000, H * box[1] // 1000, W * box[2] // 1000, H * box[3] // 1000))
    big = im.copy()
    big.thumbnail((1400, 1600))
    big.save(DEST / f"{pid}.jpg", quality=85, optimize=True)
    t = im.copy()
    t.thumbnail((360, 480))
    t.save(DEST / f"{pid}_t.jpg", quality=82, optimize=True)
    print(pid, big.size, t.size)


if __name__ == "__main__":
    DEST.mkdir(parents=True, exist_ok=True)
    for pid in sys.argv[1:] or PLATES:
        make(pid)
