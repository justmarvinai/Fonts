"""Capital letters."""

from geom import (U, D, I, rect, ellipse, ring, poly, para, diag, hwidth, line,
                  above, below, leftof, rightof, band, flipx, flipy, rot180,
                  move, halfplane, bounds)
from common import glyph, G, cutline, side, mid_radii, far
from lower import (TV, solve_w, s_build, k_build, vshape, wshape, xshape,
                   zshape)


def OW(p):
    return p.w(742, 1.45)


def dshape(p, x0, x1, y0, y1, R, tv, th, k=None):
    """D-shaped bowl: straight from x0 to x1-R, then a half (super)ellipse.
    The inner counter starts at x0 + tv (the stem)."""
    k = p.ko + 0.03 if k is None else k
    xm = x1 - R
    outer = U(rect(x0, y0, xm + 1, y1), I(ellipse(xm - R, y0, x1, y1, k), rightof(xm)))
    ri = R - tv
    inner = U(rect(x0 + tv, y0 + th, xm + 1, y1 - th),
              I(ellipse(xm - ri, y0 + th, x1 - tv, y1 - th, k + 0.02), rightof(xm)))
    return D(outer, inner)


@glyph("H", 0x48)
def H(p):
    V, CH, cap = p.CV, p.CH, p.cap
    W = p.w(574, 1.35)
    yb = cap * 0.505 - CH / 2
    s = U(rect(0, 0, V, cap), rect(W - V, 0, W, cap), rect(0, yb, W, yb + CH))
    return G(s, p.csb, p.csb)


@glyph("I", 0x49)
def I_(p):
    return G(rect(0, 0, p.CV, p.cap), p.csb, p.csb)


@glyph("L", 0x4C)
def L(p):
    V, CH, cap = p.CV, p.CH, p.cap
    W = p.w(420, 0.95)
    s = U(rect(0, 0, V, cap), rect(0, 0, W, CH))
    return G(s, p.csb, p.sbd + 4)


@glyph("E", 0x45)
def E(p):
    V, CH, cap = p.CV, p.CH, p.cap
    W = p.w(452, 1.0)
    yb = cap * 0.5 - CH / 2
    s = U(rect(0, 0, V, cap), rect(0, cap - CH, W, cap), rect(0, yb, W * 0.93, yb + CH),
          rect(0, 0, W, CH))
    return G(s, p.csb, p.sbd + 18)


@glyph("F", 0x46)
def F(p):
    V, CH, cap = p.CV, p.CH, p.cap
    W = p.w(436, 0.95)
    yb = cap * 0.48 - CH / 2
    s = U(rect(0, 0, V, cap), rect(0, cap - CH, W, cap), rect(0, yb, W * 0.92, yb + CH))
    return G(s, p.csb, p.sbd + 12)


@glyph("T", 0x54)
def T(p):
    V, CH, cap = p.CV, p.CH, p.cap
    W = p.w(520, 1.05)
    s = U(rect(0, cap - CH, W, cap), rect(W / 2 - V / 2, 0, W / 2 + V / 2, cap))
    return G(s, p.sbd + 6, p.sbd + 6)


@glyph("O", 0x4F)
def O(p):
    V, CH, cap, os = p.CV, p.CH, p.cap, p.cos
    W = OW(p)
    s = ring((0, -os, W, cap + os), (V, -os + CH, W - V, cap + os - CH), p.ko, p.ki)
    return G(s, p.csbo, p.csbo)


@glyph("Q", 0x51)
def Q(p):
    V, CH, cap, os = p.CV, p.CH, p.cap, p.cos
    W = OW(p)
    o = ring((0, -os, W, cap + os), (V, -os + CH, W - V, cap + os - CH), p.ko, p.ki)
    tail = line(W * 0.56, cap * 0.2, W * 1.0, -cap * 0.1, p.CV * 0.96)
    tail = I(tail, above(-cap * 0.1 + 2), leftof(W + 0.0))
    return G(U(o, tail), p.csbo, p.csbo * 0.7)


@glyph("C", 0x43)
def C(p):
    V, CH, cap, os = p.CV, p.CH, p.cap, p.cos
    W = OW(p) * 0.93
    ob = (0, -os, W, cap + os)
    ib = (V, -os + CH, W - V, cap + os - CH)
    s = ring(ob, ib, p.ko, p.ki)
    cx, cy, rx, ry = mid_radii(ob, ib)
    ref = far(cx, cy, 1, 0)
    s = D(s, I(rightof(cx), side(cutline(cx, cy, rx, ry, 41, TV), ref),
               side(cutline(cx, cy, rx, ry, -41, TV), ref)))
    return G(s, p.csbo, p.csbo * 0.6)


@glyph("G", 0x47)
def G_(p):
    V, CH, cap, os = p.CV, p.CH, p.cap, p.cos
    W = OW(p) * 0.98
    ob = (0, -os, W, cap + os)
    ib = (V, -os + CH, W - V, cap + os - CH)
    s = ring(ob, ib, p.ko, p.ki)
    cx, cy, rx, ry = mid_radii(ob, ib)
    btop = cap * 0.5 + CH * 0.42
    bbot = btop - CH * 0.98
    up = cutline(cx, cy, rx, ry, 41, TV)
    s = D(s, I(rightof(cx), above(btop), side(up, far(cx, btop, 1, 0))))
    bar = I(rect(cx + W * 0.03, bbot, W, btop), ellipse(*ob, k=p.ko))
    return G(U(s, bar), p.csbo, p.csbo * 0.9)


@glyph("D", 0x44)
def D_(p):
    V, CH, cap = p.CV, p.CH, p.cap
    W = p.w(642, 1.35)
    s = dshape(p, 0, W, 0, cap, cap * 0.5, V, CH)
    return G(U(s, rect(0, 0, V, cap)), p.csb, p.csbo)


@glyph("B", 0x42)
def B(p):
    V, CH, cap = p.CV, p.CH, p.cap
    W = p.w(560, 1.25)
    ym = cap * 0.535
    lo = dshape(p, 0, W, 0, ym + CH / 2, (ym + CH / 2) * 0.5, V * 1.0, CH)
    up = dshape(p, 0, W * 0.9, ym - CH / 2, cap, (cap - ym + CH / 2) * 0.5, V * 0.96, CH)
    return G(U(lo, up, rect(0, 0, V, cap)), p.csb, p.csbo)


def _pbowl(p, W):
    V, CH, cap = p.CV, p.CH, p.cap
    yb = cap * 0.38 - CH * 0.3
    return dshape(p, 0, W, yb, cap, (cap - yb) * 0.5, V, CH), yb


@glyph("P", 0x50)
def P(p):
    W = p.w(548, 1.2)
    bw, yb = _pbowl(p, W)
    return G(U(bw, rect(0, 0, p.CV, p.cap)), p.csb, p.csbo)


@glyph("R", 0x52)
def R(p):
    W = p.w(560, 1.25)
    bw, yb = _pbowl(p, W * 0.97)
    xs = W * 0.5 - p.dv * 0.3
    wl = solve_w(p.CD * 0.98, W - xs, yb + p.CH * 0.5)
    leg = para(W - wl, W, 0, xs, xs + wl, yb + p.CH * 0.5)
    return G(U(bw, rect(0, 0, p.CV, p.cap), leg), p.csb, p.sbd + 4)


@glyph("J", 0x4A)
def J(p):
    V, CH, cap, os = p.CV, p.CH, p.cap, p.cos
    W = p.w(470, 1.1)
    hy = cap * 0.36
    ob = (0, -os, W, -os + 2 * hy)
    ib = (V * 0.95, -os + CH, W - V, -os + 2 * hy - CH)
    hk = I(ring(ob, ib, p.ko, p.ki), below((ob[1] + ob[3]) / 2))
    cx, cy, rx, ry = mid_radii(ob, ib)
    hk = D(hk, I(leftof(cx), side(cutline(cx, cy, rx, ry, 196, 0.5), far(cx, cy, -1, 0.6))))
    s = U(hk, rect(W - V, cy, W, cap))
    return G(s, p.sbd + 10, p.csb)


@glyph("U", 0x55)
def U_(p):
    V, CH, cap, os = p.CV, p.CH, p.cap, p.cos
    W = p.w(590, 1.35)
    hy = W * 0.5
    ob = (0, -os, W, -os + 2 * hy)
    ib = (V, -os + CH, W - V, -os + 2 * hy - CH)
    cy = (ob[1] + ob[3]) / 2
    bot = I(ring(ob, ib, p.ko, p.ki), below(cy))
    s = U(bot, rect(0, cy, V, cap), rect(W - V, cy, W, cap))
    return G(s, p.csb * 0.92, p.csb * 0.92)


@glyph("S", 0x53)
def S(p):
    W = p.w(540, 1.15)
    s = s_build(p, W, p.cap, p.CV, p.CH * (1 - p.dv / 1000), p.cos, ts_ratio=1.08, ym_ratio=0.52, ta=42, tb=222)
    return G(s, p.csbo * 0.9, p.csbo * 0.9)


@glyph("K", 0x4B)
def K(p):
    W = p.w(560, 1.15)
    s = k_build(p, W, p.cap, p.cap, p.CV, p.CD * 0.98, ya_r=0.18, t=0.43)
    return G(s, p.csb, p.sbd)


@glyph("V", 0x56)
def V_(p):
    W = p.w(640, 1.3)
    s, _ = vshape(p, W, p.cap, p.CD, 0.34 * p.CV)
    return G(s, p.sbd, p.sbd)


@glyph("A", 0x41)
def A(p):
    W = p.w(670, 1.35)
    cap = p.cap
    flat = 0.36 * p.CV
    s, wd = vshape(p, W, cap, p.CD, flat)
    s = flipy(s, cap / 2)
    yb = cap * 0.25
    hull = poly([(0, 0), (W / 2 - flat / 2, cap), (W / 2 + flat / 2, cap), (W, 0)])
    bar = I(rect(0, yb, W, yb + p.CH), hull)
    return G(U(s, bar), p.sbd, p.sbd)


@glyph("W", 0x57)
def W_(p):
    W = p.w(960, 2.3)
    s = wshape(p, W, p.cap, p.CD * 0.94, 0.28 * p.CV)
    return G(s, p.sbd, p.sbd)


@glyph("M", 0x4D)
def M(p):
    V, cap = p.CV * 0.94, p.cap
    W = p.w(740, 1.75)
    flat = 0.34 * p.CV
    cx = W / 2
    wd = hwidth(p.CD * 0.94, cx - flat / 2 - V * 0.5, cap)
    l_ = para(cx - flat / 2, cx - flat / 2 + wd, 0, 0, wd, cap)
    r_ = para(cx + flat / 2 - wd, cx + flat / 2, 0, W - wd, W, cap)
    hull = poly([(0, cap), (cx - flat / 2, 0), (cx + flat / 2, 0), (W, cap)])
    s = U(I(U(l_, r_), hull), rect(0, 0, V, cap), rect(W - V, 0, W, cap))
    return G(s, p.csb, p.csb)


@glyph("N", 0x4E)
def N(p):
    V, cap = p.CV * 0.93, p.cap
    W = p.w(600, 1.35)
    wd = solve_w(p.CD * 1.0, W, cap)
    dg = para(W - wd, W, 0, 0, wd, cap)
    s = U(rect(0, 0, V, cap), rect(W - V, 0, W, cap), dg)
    return G(s, p.csb, p.csb)


@glyph("X", 0x58)
def X_(p):
    W = p.w(620, 1.3)
    return G(xshape(p, W, p.cap, p.CD * 0.98), p.sbd, p.sbd)


@glyph("Y", 0x59)
def Y(p):
    V, cap = p.CV, p.cap
    W = p.w(620, 1.3)
    cx = W / 2
    ym = cap * 0.43
    wd = hwidth(p.CD, cx - V / 2, cap - ym)
    l_ = para(cx - V / 2, cx - V / 2 + wd, ym, 0, wd, cap)
    r_ = para(cx + V / 2 - wd, cx + V / 2, ym, W - wd, W, cap)
    hull = poly([(0, cap), (cx - V / 2, ym - 1), (cx + V / 2, ym - 1), (W, cap)])
    s = U(I(U(l_, r_), hull), rect(cx - V / 2, 0, cx + V / 2, ym + 2))
    return G(s, p.sbd, p.sbd)


@glyph("Z", 0x5A)
def Z(p):
    W = p.w(540, 1.2)
    return G(zshape(p, W, p.cap, p.CH, p.CD * 0.94), p.sbd + 12, p.sbd + 12)


@glyph("Germandbls", 0x1E9E)
def Germandbls(p):
    """Capital sharp s: stem, flat top, diagonal, round lower bowl."""
    V, CH, cap, os = p.CV, p.CH, p.cap, p.cos
    W = p.w(590, 1.25)
    ym = cap * 0.58
    ob = (V * 0.5, -os, W, ym + CH / 2)
    ib = (V * 0.5 + V * 0.95, -os + CH, W - V, ym - CH / 2)
    bw = ring(ob, ib, p.ko, p.ki)
    cx, cy, rx, ry = mid_radii(ob, ib)
    bw = D(bw, I(leftof(cx), above(cy)))
    bw = D(bw, I(leftof(cx), side(cutline(cx, cy, rx, ry, 212, 0.5), far(cx, cy, -1, 1))))
    xt = W * 0.9
    tb = rect(0, cap - CH, xt, cap)
    wd = hwidth(p.CD * 0.94, xt - cx, cap - ym)
    dg = para(cx - wd * 0.35, cx + wd * 0.65, ym - CH / 2, xt - wd, xt, cap)
    dg = I(dg, band(ym - CH / 2, cap))
    s = U(rect(0, 0, V, cap), tb, dg, bw)
    return G(s, p.csb, p.csbo)
