"""Side-by-side proof: python3 source/compare.py out.png size font1 font2 ... -- line1 line2"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from proof import render
from PIL import Image
a = sys.argv[1:]
out, size = a[0], int(a[1])
k = a.index("--")
fonts, lines = a[2:k], a[k + 1:]
ims = []
for f in fonts:
    render(f, lines, size=size, out=out + ".tmp.png", width=int(os.environ.get("WIDTH", 2400)))
    ims.append(Image.open(out + ".tmp.png").copy())
os.remove(out + ".tmp.png")
c = Image.new("L", (ims[0].width, sum(i.height for i in ims)), 255)
y = 0
for i in ims:
    c.paste(i, (0, y)); y += i.height
c.save(out)
