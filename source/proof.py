"""Render proof images with HarfBuzz shaping + FreeType rasterising."""
import sys, os
import uharfbuzz as hb
import freetype
from PIL import Image

def render(fontpath, lines, size=96, out="proof.png", width=2400, margin=40, features=None):
    blob = hb.Blob.from_file_path(fontpath)
    face = hb.Face(blob); font = hb.Font(face)
    upem = face.upem
    ft = freetype.Face(fontpath); ft.set_pixel_sizes(0, size)
    sc = size / upem
    lh = int(size * 1.25)
    img = Image.new("L", (width, margin * 2 + lh * len(lines)), 255)
    y = margin + int(size * 0.95)
    for line in lines:
        buf = hb.Buffer(); buf.add_str(line); buf.guess_segment_properties()
        hb.shape(font, buf, features or {"kern": True, "liga": True})
        x = margin
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            ft.load_glyph(info.codepoint, freetype.FT_LOAD_DEFAULT | freetype.FT_LOAD_NO_HINTING)
            ft.glyph.render(freetype.FT_RENDER_MODE_NORMAL)
            bm = ft.glyph.bitmap
            if bm.width and bm.rows:
                g = Image.frombytes("L", (bm.width, bm.rows), bytes(bm.buffer)) if bm.pitch == bm.width else \
                    Image.frombytes("L", (bm.pitch, bm.rows), bytes(bm.buffer)).crop((0, 0, bm.width, bm.rows))
                gx = int(round(x + pos.x_offset * sc)) + ft.glyph.bitmap_left
                gy = y - ft.glyph.bitmap_top
                inv = Image.eval(g, lambda v: 255 - v)
                img.paste(0, (gx, gy), g)
            x += pos.x_advance * sc
        y += lh
    img.save(out)

if __name__ == "__main__":
    fp = sys.argv[1]; out = sys.argv[2]; size = int(sys.argv[3]); lines = sys.argv[4:]
    render(fp, lines, size=size, out=out)
