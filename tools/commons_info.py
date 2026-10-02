"""Print Wikimedia Commons metadata (size, licence, artist, credit, date,
description) for one or more file titles.

    python tools/commons_info.py "File:Nuremberg chronicles - Nuremberga.png" ...
"""
import json
import re
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (research; Die Aebtissin und der Rat)"}


def info(title):
    q = urllib.parse.urlencode({"action": "query", "titles": title, "prop": "imageinfo",
                                "iiprop": "size|extmetadata", "format": "json"})
    req = urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + q, headers=UA)
    data = json.load(urllib.request.urlopen(req, timeout=60))
    page = next(iter(data["query"]["pages"].values()))
    ii = (page.get("imageinfo") or [{}])[0]
    meta = ii.get("extmetadata", {})
    clean = lambda k: re.sub(r"<[^>]+>", "", meta.get(k, {}).get("value", "")).strip()
    print(f"== {title} {ii.get('width')} x {ii.get('height')}")
    for k in ["LicenseShortName", "Artist", "Credit", "DateTimeOriginal", "ImageDescription"]:
        print(f"   {k} : {clean(k)[:300]}")


if __name__ == "__main__":
    for t in sys.argv[1:]:
        info(t)
