"""Geometry toolkit for constructing glyph outlines.

Every glyph in Formwerk is built from a handful of primitives (rectangles,
superellipses, polygons and diagonal strokes) that are combined with boolean
operations (skia-pathops).  The result is a clean, overlap-free outline.
"""

import math

import pathops
from pathops import Path, PathOp
from fontTools.pens.transformPen import TransformPen

BIG = 20000.0


# ---------------------------------------------------------------------------
# primitives


def rect(x0, y0, x1, y1):
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    p = Path()
    p.moveTo(x0, y0)
    p.lineTo(x1, y0)
    p.lineTo(x1, y1)
    p.lineTo(x0, y1)
    p.close()
    return p


def poly(pts):
    p = Path()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    return _norm(p)


def ellipse(x0, y0, x1, y1, k=0.5523):
    """Superellipse-ish oval inscribed in a box.  k=0.5523 is a circle,
    larger values make it squarer."""
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    rx, ry = (x1 - x0) / 2.0, (y1 - y0) / 2.0
    p = Path()
    p.moveTo(x1, cy)
    p.cubicTo(x1, cy + k * ry, cx + k * rx, y1, cx, y1)
    p.cubicTo(cx - k * rx, y1, x0, cy + k * ry, x0, cy)
    p.cubicTo(x0, cy - k * ry, cx - k * rx, y0, cx, y0)
    p.cubicTo(cx + k * rx, y0, x1, cy - k * ry, x1, cy)
    p.close()
    return p


def circle(cx, cy, r, k=0.5523):
    return ellipse(cx - r, cy - r, cx + r, cy + r, k)


def ring(outer, inner, ko=0.5523, ki=0.5523):
    """outer / inner are boxes (x0, y0, x1, y1)."""
    return D(ellipse(*outer, k=ko), ellipse(*inner, k=ki))


def para(xb0, xb1, yb, xt0, xt1, yt):
    """Parallelogram/trapezoid with horizontal bottom and top edges."""
    return poly([(xb0, yb), (xb1, yb), (xt1, yt), (xt0, yt)])


def diag(xb, yb, xt, yt, w):
    """Diagonal stroke with horizontal cuts. (xb,yb) and (xt,yt) are the
    centres of the bottom and top cut, w the horizontal width."""
    return para(xb - w / 2, xb + w / 2, yb, xt - w / 2, xt + w / 2, yt)


def hwidth(t, dx, dy):
    """Horizontal width that gives a stroke of perpendicular thickness t for
    a centre-line running dx horizontally over dy vertically."""
    ang = math.atan2(abs(dy), abs(dx))
    return t / max(math.sin(ang), 0.05)


def line(x0, y0, x1, y1, t):
    """Stroke of perpendicular thickness t along a segment (butt caps)."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * t / 2, dx / L * t / 2
    return poly([(x0 + nx, y0 + ny), (x0 - nx, y0 - ny), (x1 - nx, y1 - ny), (x1 + nx, y1 + ny)])


# ---------------------------------------------------------------------------
# clipping regions


def above(y):
    return rect(-BIG, y, BIG, BIG)


def below(y):
    return rect(-BIG, -BIG, BIG, y)


def leftof(x):
    return rect(-BIG, -BIG, x, BIG)


def rightof(x):
    return rect(x, -BIG, BIG, BIG)


def band(y0, y1):
    return rect(-BIG, y0, BIG, y1)


def wedge(cx, cy, a0, a1):
    """Circular sector (as a polygon) from angle a0 to a1 (degrees, ccw)."""
    while a1 < a0:
        a1 += 360
    pts = [(cx, cy)]
    n = max(2, int(math.ceil((a1 - a0) / 20.0)) + 1)
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * i / (n - 1))
        pts.append((cx + BIG * math.cos(a), cy + BIG * math.sin(a)))
    return poly(pts)


def halfplane(x0, y0, x1, y1):
    """Region to the left of the directed line (x0,y0)->(x1,y1)."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    dx, dy = dx / L, dy / L
    nx, ny = -dy, dx
    a = (x0 - dx * BIG, y0 - dy * BIG)
    b = (x0 + dx * BIG, y0 + dy * BIG)
    return poly([a, b, (b[0] + nx * BIG, b[1] + ny * BIG), (a[0] + nx * BIG, a[1] + ny * BIG)])


# ---------------------------------------------------------------------------
# booleans


def _norm(p):
    q = Path()
    p.draw(q.getPen())
    try:
        q.simplify(fix_winding=True)
    except pathops.PathOpsError:
        pass
    return q


def U(*ps):
    ps = [p for p in ps if p is not None]
    if not ps:
        return Path()
    out = Path()
    pen = out.getPen()
    pathops.union(ps, pen)
    return out


def D(a, *bs):
    for b in bs:
        if b is None:
            continue
        a = pathops.op(a, b, PathOp.DIFFERENCE, fix_winding=True)
    return a


def I(a, *bs):
    for b in bs:
        a = pathops.op(a, b, PathOp.INTERSECTION, fix_winding=True)
    return a


def X(a, b):
    return pathops.op(a, b, PathOp.XOR, fix_winding=True)


# ---------------------------------------------------------------------------
# transforms


def xform(p, m):
    out = Path()
    p.draw(TransformPen(out.getPen(), m))
    return _norm(out)


def move(p, dx, dy=0):
    return xform(p, (1, 0, 0, 1, dx, dy))


def scale(p, sx, sy=None, cx=0, cy=0):
    sy = sx if sy is None else sy
    return xform(p, (sx, 0, 0, sy, cx - sx * cx, cy - sy * cy))


def flipx(p, axis):
    return xform(p, (-1, 0, 0, 1, 2 * axis, 0))


def flipy(p, axis):
    return xform(p, (1, 0, 0, -1, 0, 2 * axis))


def rot180(p, cx, cy):
    return xform(p, (-1, 0, 0, -1, 2 * cx, 2 * cy))


def rotate(p, deg, cx=0, cy=0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return xform(p, (c, s, -s, c, cx - c * cx + s * cy, cy - s * cx - c * cy))


def skew(p, deg, cy=0):
    t = math.tan(math.radians(deg))
    return xform(p, (1, 0, t, 1, -t * cy, 0))


def bounds(p):
    try:
        return p.bounds
    except Exception:
        return (0, 0, 0, 0)


def empty(p):
    b = p.bounds
    return b[2] - b[0] <= 0 or b[3] - b[1] <= 0
