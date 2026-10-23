"""Lining, tabular figures."""

import math

from geom import (U, D, I, rect, ellipse, ring, poly, para, hwidth, line,
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
    ib = (W * 0.02 + V * 0.95, cap + os - h2 + H * 1.05, W - V, cap + os - H)
    r = ring(ob, ib, p.ko, p.ki)
    cx, cy, rx, ry = mid_radii(ob, ib)
    a1 = -32
    r = D(r, I(leftof(cx), side(cutline(cx, cy, rx, ry, 162, TV), far(cx, cy, -1, -1))))
    r = D(r, wedge(cx, cy, 180, 360 + a1))
    ar = math.radians(a1)
    px, py = cx + rx * math.cos(ar), cy + ry * math.sin(ar)
    tx, ty = -rx * math.sin(ar) * -1, ry * math.cos(ar)  # tangent (clockwise)
    tx, ty = rx * math.sin(ar), -ry * math.cos(ar)
    L = math.hypot(tx, ty)
    tx, ty = tx / L, ty / L
    back = V * 0.35
    dg = line(px - tx * back, py - ty * back, V * 0.45, H * 0.5, p.CD * 0.95)
    dg = I(dg, rightof(0), above(0))
    s = U(r, dg, rect(0, 0, W, H))
    return tab(p, s)


@glyph("three", 0x33)
def three(p):
    V, H, cap, os = fstem(p), fhor(p), p.cap, p.cos
    W = fbw(p)
    ylt = cap * 0.6
    bw, (cx, cy, rx, ry) = open_bowl(p, 0, W, ylt)
    xt = W * 0.94
    tb = rect(W * 0.04, cap - H, xt, cap)
    wd = hwidth(p.CD * 0.94, xt - cx, cap - ylt)
    dg = para(cx - wd * 0.3, cx + wd * 0.7, ylt - H, xt - wd, xt, cap)
    dg = I(dg, band(ylt - H, cap))
    return tab(p, U(bw, tb, dg))


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
    V, H, cap, os = fstem(p), fhor(p), p.cap, p.cos
    W = fbw(p)
    ylt = cap * 0.62
    ob = (0, -os, W, ylt)
    ib = (V, -os + H, W - V, ylt - H)
    r = ring(ob, ib, p.ko, p.ki)
    cx, cy, rx, ry = mid_radii(ob, ib)
    # straight stroke leaving the bowl tangentially towards the top right
    target = W * 0.78
    best = None
    for a10 in range(1100, 1790, 5):
        a = math.radians(a10 / 10)
        px, py = cx + rx * math.cos(a), cy + ry * math.sin(a)
        tx, ty = rx * math.sin(a), -ry * math.cos(a)
        if ty <= 0:
            continue
        xt = px + (cap - py) * tx / ty
        if best is None or abs(xt - target) < abs(best[0] - target):
            best = (xt, px, py, tx, ty)
    xt, px, py, tx, ty = best
    L = math.hypot(tx, ty)
    tx, ty = tx / L, ty / L
    ext = (cap + 200 - py) / ty
    dg = line(px - tx * V, py - ty * V, px + tx * ext, py + ty * ext, p.CD * 0.95)
    dg = I(dg, below(cap), above(cy))
    return U(r, dg)


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
