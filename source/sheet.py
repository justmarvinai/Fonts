"""Quick multi-weight proof sheet: python3 source/sheet.py out.png size 'line1' 'line2' ..."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from proof import render
from PIL import Image
out, size, lines = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
ws = os.environ.get("W", "Regular,Medium,Bold,Fat").split(",")
ims = []
for w in ws:
    t = out + "." + w + ".png"
    render(f"fonts/otf/Formwerk-{w}.otf", lines, size=size, out=t, width=int(os.environ.get("WIDTH", 2400)))
    ims.append(Image.open(t)); os.remove(t)
H = sum(i.height for i in ims)
c = Image.new("L", (ims[0].width, H), 255)
y = 0
for i in ims:
    c.paste(i, (0, y)); y += i.height
c.save(out)
