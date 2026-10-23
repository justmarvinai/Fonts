import sys
import uharfbuzz as hb
fp = sys.argv[1]
blob=hb.Blob.from_file_path(fp); face=hb.Face(blob); font=hb.Font(face)
out=[]
for s in sys.argv[2:]:
    r=[]
    for k in (True, False):
        buf=hb.Buffer(); buf.add_str(s); buf.guess_segment_properties(); hb.shape(font,buf,{'kern':k})
        r.append(buf.glyph_positions[0].x_advance)
    out.append(f"{s}:{r[0]-r[1]}")
print(" ".join(out))
