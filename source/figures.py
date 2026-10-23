"""Lining, tabular figures."""

import math

from geom import (U, D, I, rect, ellipse, ring, poly, para, hwidth, line, ellipse_pts, tangent_pt,
                  above, below, leftof, rightof, band, rot180, move, bounds,
                  wedge)
from common import glyph, G, cutline, side, mid_radii, far
from lower import TV, solve_w


def fadv(p):
    return p.w(600, 1.25)


def fbw(p):
    return p.w(476, 1.05)


def tab(p, shape, nudge=0):
    b = bounds(shape)
    shape = move(shape, -b[0])
    w = b[2] - b[0]
    adv = fadv(p)
    return G(shape, 0, 0, adv=adv, xoff=(adv - w) / 2 + nudge)


def fstem(p):
    return p.CV * 0.97


def fhor(p):
    return p.CH * 0.97


def open_bowl(p, x0, x1, top, a_term=212, vert=0.6, keep_from=90):
    """Lower bowl (used by 3, 5): ring open on the upper left."""
    V, H, os = fstem(p), fhor(p), p.cos
    ob = (x0, -os, x1, top)
    ib = (x0 + V * 0.95, -os + H, x1 - V, top - H)
    bw = ring(ob, ib, p.ko, p.ki)
    cx, cy, rx, ry = mid_radii(ob, ib)
    bw = D(bw, I(leftof(cx), side(cutline(cx, cy, rx, ry, a_term, vert), far(cx, cy, -1, 1))))
    if keep_from <= 90:
        bw = D(bw, I(leftof(cx), above(cy)))
    else:
        bw = D(bw, I(wedge(cx, cy, keep_from, 200), above(cy)))
    return bw, (cx, cy, rx, ry)


@glyph("zero", 0x30)
def zero(p):
    V, H, cap, os = fstem(p), fhor(p), p.cap, p.cos
    W = fbw(p) * 1.04
    s = ring((0, -os, W, cap + os), (V * 1.02, -os + H, W - V * 1.02, cap + os - H), p.ko + 0.02, p.ki + 0.03)
    return tab(p, s)


@glyph("one", 0x31)
def one(p):
    V, H, cap = fstem(p), fhor(p), p.cap
    xs = fbw(p) * 0.36
    stem = rect(xs, 0, xs + V, cap)
    L = fbw(p) * 0.3
    flag = line(xs + V * 0.6, cap - H * 0.62, xs - L, cap - H * 0.62 - L * 0.62, H * 1.12)
    flag = I(flag, below(cap), leftof(xs + V))
    return tab(p, U(stem, flag), nudge=-fbw(p) * 0.03)


@glyph("two", 0x32)
def two(p):
    V, H, cap, os = fstem(p), fhor(p), p.cap, p.cos
    W = fbw(p)
    h2 = cap * 0.6 + 0.2 * p.dv
    ob = (W * 0.02, cap + os - h2, W, cap + os)
    ib = (W * 0.02 + V * 0.95, cap + os - h2 + H * 1.02, W - V, cap + os - H)
    r = ring(ob, ib, p.ko, p.ki)
    cx, cy, rx, ry = mid_radii(ob, ib)
    r = D(r, I(leftof(cx), side(cutline(cx, cy, rx, ry, 162, TV), far(cx, cy, -1, -1))))
    # spine: two lines from the base, tangent to the outer / inner contour
    wd = solve_w(p.CD * 0.98, W * 0.9, cy)
    br = (wd, H * 0.5)
    bl = (0, H * 0.5)
    to = tangent_pt(ellipse_pts(*ob, k=p.ko), br, min, lambda q: q[0] > cx - rx * 0.2 and q[1] < cy + ry * 0.3)
    ti = tangent_pt(ellipse_pts(*ib, k=p.ki), bl, min, lambda q: q[0] > cx - rx * 0.2 and q[1] < cy + ry * 0.3)
    spine = poly([bl, br, to, ti])
    # drop the part of the ring beyond the spine
    r = D(r, I(below(cy), side((ti[0], ti[1], to[0], to[1]), (cx - rx, ob[1]))))
    s = U(r, spine, rect(0, 0, W, H))
    return tab(p, I(s, rightof(0)))


@glyph("three", 0x33)
def three(p):
    V, H, cap, os = fstem(p), fhor(p), p.cap, p.cos
    W = fbw(p)
    ym = cap * 0.555
    i = W * 0.07
    obu = (i, ym - H / 2, W - i, cap + os)
    ibu = (i + V * 0.95, ym + H / 2, W - i - V * 0.95, cap + os - H)
    up = ring(obu, ibu, p.ko, p.ki)
    cx, cyu, rx, ryu = mid_radii(obu, ibu)
    up = D(up, I(leftof(cx), below(cyu)),
           I(leftof(cx), side(cutline(cx, cyu, rx, ryu, 150, TV), far(cx, cyu, -1, -1))))
    obl = (0, -os, W, ym + H / 2)
    ibl = (V, -os + H, W - V, ym - H / 2)
    lo = ring(obl, ibl, p.ko, p.ki)
    cx2, cyl, rx2, ryl = mid_radii(obl, ibl)
    lo = D(lo, I(leftof(cx2), above(cyl)),
           I(leftof(cx2), side(cutline(cx2, cyl, rx2, ryl, 208, TV), far(cx2, cyl, -1, 1))))
    waist = rect(cx - W * 0.17, ym - H / 2, cx + 1, ym + H / 2)
    return tab(p, U(up, lo, waist))


@glyph("four", 0x34)
def four(p):
    V, H, cap = fstem(p), fhor(p), p.cap
    W = fbw(p) * 1.04
    xs = W * 0.78 - V / 2
    yb = cap * 0.2
    stem = rect(xs, 0, xs + V, cap)
    wd = solve_w(p.CD * 0.9, xs + V, cap - yb)
    dg = para(0, wd, yb, xs + V - wd, xs + V, cap)
    dg = I(dg, band(yb, cap), leftof(xs + V))
    bar = rect(0, yb, W, yb + H)
    return tab(p, U(stem, dg, bar))


@glyph("five", 0x35)
def five(p):
    V, H, cap, os = fstem(p), fhor(p), p.cap, p.cos
    W = fbw(p)
    ylt = cap * 0.62
    ob = (0, -os, W, ylt)
    ib = (V * 0.95, -os + H, W - V, ylt - H)
    bw = ring(ob, ib, p.ko, p.ki)
    cx, cy, rx, ry = mid_radii(ob, ib)
    a_s = 138
    bw = D(bw, I(leftof(cx), side(cutline(cx, cy, rx, ry, 212, 0.6), far(cx, cy, -1, 1))))
    bw = D(bw, wedge(cx, cy, a_s, 200))
    ar = math.radians(a_s)
    sx = cx + rx * math.cos(ar)
    xv = max(sx - V * 0.5, W * 0.05)
    sy = cy + ry * math.sin(ar)
    stem = rect(xv, sy - H * 0.2, xv + V, cap)
    top = rect(xv, cap - H, W * 0.94, cap)
    return tab(p, U(bw, stem, top))


def _six(p):
    """Grotesque 6: round bowl plus a curved stroke that rises up the left
    side and ends in a flat terminal at the top right."""
    V, H, cap, os = fstem(p), fhor(p), p.cap, p.cos
    W = fbw(p)
    ylt = cap * 0.6
    ob = (0, -os, W, ylt)
    ib = (V, -os + H, W - V, ylt - H)
    bw = ring(ob, ib, p.ko, p.ki)
    cyl = (ob[1] + ob[3]) / 2
    cy2 = cap * 0.5
    i2 = W * 0.01
    ob2 = (0, 2 * cy2 - (cap + os), W - i2, cap + os)
    ib2 = (V, 2 * cy2 - (cap + os) + H, W - i2 - V * 0.95, cap + os - H)
    arc = I(ring(ob2, ib2, p.ko, p.ki), above(cy2))
    cx2, _, rx2, ry2 = mid_radii(ob2, ib2)
    arc = D(arc, I(rightof(cx2), side(cutline(cx2, cy2, rx2, ry2, 38, TV), far(cx2, cy2, 1, -1))))
    return U(bw, arc, rect(0, cyl, V, cy2 + 1))


@glyph("six", 0x36)
def six(p):
    return tab(p, _six(p))


@glyph("nine", 0x39)
def nine(p):
    s = _six(p)
    b = bounds(s)
    return tab(p, rot180(s, (b[0] + b[2]) / 2, p.cap / 2))


@glyph("seven", 0x37)
def seven(p):
    V, H, cap = fstem(p), fhor(p), p.cap
    W = fbw(p)
    xb = W * 0.16
    wd = solve_w(p.CD * 0.98, W - xb, cap - H)
    dg = para(xb, xb + wd, 0, W - wd, W, cap - H * 0.5)
    return tab(p, U(rect(0, cap - H, W, cap), dg))


@glyph("eight", 0x38)
def eight(p):
    V, H, cap, os = fstem(p), fhor(p), p.cap, p.cos
    W = fbw(p) * 1.02
    ym = cap * 0.545
    lo = ring((0, -os, W, ym + H / 2), (V, -os + H, W - V, ym - H / 2), p.ko, p.ki)
    i = W * 0.06
    up = ring((i, ym - H / 2, W - i, cap + os), (i + V * 0.95, ym + H / 2, W - i - V * 0.95, cap + os - H), p.ko, p.ki)
    return tab(p, U(lo, up))
