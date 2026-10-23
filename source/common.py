"""Glyph registry and shared construction helpers."""

import math

from geom import (U, D, I, rect, ellipse, ring, halfplane, rightof, leftof,
                  above, below, poly, circle, move, BIG)

REGISTRY = {}  # name -> (codepoint or None, function)
ORDER = []


def glyph(name, cp=None):
    def deco(fn):
        REGISTRY[name] = (cp, fn)
        ORDER.append(name)
        return fn
    return deco


class G:
    """A constructed glyph: outline + sidebearings (relative to ink)."""

    def __init__(self, shape, l, r, top_anchor=None, adv=None, xoff=None):
        self.shape = shape
        self.l = l
        self.r = r
        self.top_anchor = top_anchor  # x of accent anchor in shape coords
        self.adv = adv  # fixed advance (tabular / spaces); else from ink
        self.xoff = xoff  # with adv: x offset of the shape


# ---------------------------------------------------------------------------
# terminal cuts


def cutline(cx, cy, rx, ry, a, vert):
    """Line through the point at angle `a` (deg) on the mid-stroke ellipse.
    The cut runs radially (vert=0) .. vertically (vert=1)."""
    ar = math.radians(a)
    px, py = cx + rx * math.cos(ar), cy + ry * math.sin(ar)
    radial = math.degrees(math.atan2(ry * math.sin(ar), rx * math.cos(ar)))
    target = 90.0 if radial >= 0 else -90.0
    d = math.radians(radial + (target - radial) * vert)
    return (px, py, px + math.cos(d), py + math.sin(d))


def side(ln, ref):
    """Half plane bounded by line `ln` that contains point `ref`."""
    x0, y0, x1, y1 = ln
    cross = (x1 - x0) * (ref[1] - y0) - (y1 - y0) * (ref[0] - x0)
    return halfplane(x0, y0, x1, y1) if cross > 0 else halfplane(x1, y1, x0, y0)


def mid_radii(ob, ib):
    cx = (ob[0] + ob[2]) / 2.0
    cy = (ob[1] + ob[3]) / 2.0
    rx = ((ob[2] - ob[0]) + (ib[2] - ib[0])) / 4.0
    ry = ((ob[3] - ob[1]) + (ib[3] - ib[1])) / 4.0
    return cx, cy, rx, ry


def dot(cx, cy, d):
    return circle(cx, cy, d / 2.0, 0.5523)


def far(cx, cy, dx, dy):
    return (cx + dx * BIG / 4, cy + dy * BIG / 4)
