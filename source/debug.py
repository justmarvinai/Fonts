"""Rasterise pathops paths for debugging: python3 debug.py"""
from PIL import Image, ImageDraw
from fontTools.pens.basePen import BasePen

class FlatPen(BasePen):
    def __init__(self):
        super().__init__(None); self.polys = []; self.cur = []
    def _moveTo(self, p): self.cur = [p]
    def _lineTo(self, p): self.cur.append(p)
    def _curveToOne(self, a, b, c):
        p0 = self.cur[-1]
        for i in range(1, 17):
            t = i / 16; mt = 1 - t
            self.cur.append((mt**3*p0[0]+3*mt*mt*t*a[0]+3*mt*t*t*b[0]+t**3*c[0],
                             mt**3*p0[1]+3*mt*mt*t*a[1]+3*mt*t*t*b[1]+t**3*c[1]))
    def _closePath(self): self.polys.append(self.cur); self.cur = []

def draw(paths, out, scale=0.4, w=1200, h=600, base=450, ox=50):
    img = Image.new("RGB", (w, h), "white"); d = ImageDraw.Draw(img)
    cols = [(0,0,0,), (220,40,40), (40,120,220), (40,170,60)]
    for i, (path, dx) in enumerate(paths):
        pen = FlatPen(); path.draw(pen)
        for poly in pen.polys:
            pts = [(ox + (x + dx) * scale, base - y * scale) for x, y in poly]
            if len(pts) > 2: d.polygon(pts, outline=cols[i % 4])
    img.save(out)
