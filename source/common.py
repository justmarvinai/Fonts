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


HORIZONTAL_TERMINALS = True


def cutline(cx, cy, rx, ry, a, vert, flat=None):
    """Line through the point at angle `a` (deg) on the mid-stroke ellipse.
    Terminals are cut flat (horizontal), grotesque style; with
    HORIZONTAL_TERMINALS off the cut runs radially (vert=0) .. vertically
    (vert=1)."""
    ar = math.radians(a)
    px, py = cx + rx * math.cos(ar), cy + ry * math.sin(ar)
    if (HORIZONTAL_TERMINALS if flat is None else flat):
        # keep the flat cut inside the counter's height so that it always
        # runs straight across the stroke (inner -> outer contour)
        iry = _INNER.get((round(cx, 3), round(cy, 3), round(rx, 3), round(ry, 3)), ry * 0.7)
        py = cy + max(-0.8, min(0.8, math.sin(ar))) * iry
        return (px, py, px + 1.0, py)
    radial = math.degrees(math.atan2(ry * math.sin(ar), rx * math.cos(ar)))
    target = 90.0 if radial >= 0 else -90.0
    d = math.radians(radial + (target - radial) * vert)
    return (px, py, px + math.cos(d), py + math.sin(d))


def side(ln, ref):
    """Half plane bounded by line `ln` that contains point `ref`."""
    x0, y0, x1, y1 = ln
    cross = (x1 - x0) * (ref[1] - y0) - (y1 - y0) * (ref[0] - x0)
    return halfplane(x0, y0, x1, y1) if cross > 0 else halfplane(x1, y1, x0, y0)


_INNER = {}


def mid_radii(ob, ib):
    cx = (ob[0] + ob[2]) / 2.0
    cy = (ob[1] + ob[3]) / 2.0
    rx = ((ob[2] - ob[0]) + (ib[2] - ib[0])) / 4.0
    ry = ((ob[3] - ob[1]) + (ib[3] - ib[1])) / 4.0
    _INNER[(round(cx, 3), round(cy, 3), round(rx, 3), round(ry, 3))] = (ib[3] - ib[1]) / 2.0
    return cx, cy, rx, ry


def dot(cx, cy, d):
    """Square dot (i, j, punctuation, diacritics)."""
    return rect(cx - d / 2.0, cy - d / 2.0, cx + d / 2.0, cy + d / 2.0)


def far(cx, cy, dx, dy):
    return (cx + dx * BIG / 4, cy + dy * BIG / 4)
