"""Generate the HTML specimen.

    python3 source/specimen.py                 # specimen/index.html (links ../fonts/webfonts)
    python3 source/specimen.py --embed OUT     # self-contained page with fonts as data URIs
"""

import base64
import html
import os
import sys

from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WEIGHTS = ["Regular", "Medium", "Bold", "Fat"]


def main(argv):
    embed = "--embed" in argv
    tpl = open(os.path.join(HERE, "specimen_template.html"), encoding="utf-8").read()
    font = TTFont(os.path.join(ROOT, "fonts", "ttf", "Formwerk-Regular.ttf"))
    cmap = font.getBestCmap()
    chars = sorted(c for c in cmap if c > 0x20 and c not in (0xA0, 0xAD))
    spans = "".join(f"<span>{html.escape(chr(c))}</span>" for c in chars)
    out = tpl.replace("{{GLYPHSPANS}}", spans).replace("{{GLYPHS}}", str(len(font.getGlyphOrder())))
    for w in WEIGHTS:
        path = os.path.join(ROOT, "fonts", "webfonts", f"Formwerk-{w}.woff2")
        if embed:
            data = base64.b64encode(open(path, "rb").read()).decode("ascii")
            src = "data:font/woff2;base64," + data
        else:
            src = f"../fonts/webfonts/Formwerk-{w}.woff2"
        out = out.replace("{{%s}}" % w, src)
    if embed:
        dest = argv[argv.index("--embed") + 1]
    else:
        dest = os.path.join(ROOT, "specimen", "index.html")
        out = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
               '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
               + out.replace("<style>", "<style>\nbody { margin: 0; }", 1)
               .replace("</style>", "</style>\n</head>\n<body>", 1)
               + "\n</body>\n</html>\n")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(out)
    print("wrote", dest)


if __name__ == "__main__":
    main(sys.argv)
