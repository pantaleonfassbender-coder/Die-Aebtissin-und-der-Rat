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
