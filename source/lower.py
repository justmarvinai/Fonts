"""Lowercase letters."""

from geom import (U, D, I, rect, ellipse, ring, poly, para, diag, hwidth,
                  above, below, leftof, rightof, band, flipx, rot180, move,
                  halfplane, bounds)
from common import glyph, G, cutline, side, mid_radii, dot, far

TV = 0.42  # verticality of terminal cuts (0 radial, 1 vertical)


def solve_w(t, span, dy):
    """Horizontal width of a diagonal whose outer edges span `span`."""
    w = t
    for _ in range(30):
        w = hwidth(t, span - w, dy)
    return w


def nW(p):
    return p.w(458, 1.12)


def oW(p):
    return p.w(508, 0.9)


def arch_ry(p):
    return (p.xh + 2 * p.os) / 2.0 * 1.04


def arch(p, x0, x1, top, cy, V=None, H=None, j=None):
    """Top half of a ring springing from a stem at x0..x0+V."""
    V = p.V if V is None else V
    H = p.H if H is None else H
    j = p.joint if j is None else j
    c = p.crotch * (V / p.V)
    ry = top - cy
    outer = ellipse(x0 + j, cy - ry, x1, top, p.ko)
    inner = ellipse(x0 + V - c, cy - (ry - H), x1 - V, top - H, p.ki)
    return I(D(outer, inner), above(cy), rightof(x0))


def bowl(p, x0, x1, y0, y1, V=None, H=None, j=None):
    """Bowl attached to a stem on its left (stem occupies x0..x0+V)."""
    V = p.V if V is None else V
    H = p.H if H is None else H
    j = p.joint if j is None else j
    c = p.crotch * (V / p.V)
    return I(D(ellipse(x0 + j, y0, x1, y1, p.ko),
               ellipse(x0 + V - c, y0 + H, x1 - V, y1 - H, p.ki)), rightof(x0))


def dot_d(p):
    return 1.04 * p.V + 6


def dot_y(p):
    d = dot_d(p)
    return p.xh + 64 + 0.2 * p.V + d / 2


# ---------------------------------------------------------------------------


@glyph("n", 0x6E)
def n(p):
    V, xh, os = p.V, p.xh, p.os
    W = nW(p)
    cy = xh + os - arch_ry(p)
    s = U(rect(0, 0, V, xh), arch(p, 0, W, xh + os, cy), rect(W - V, 0, W, cy))
    return G(s, p.sb, p.sb * 0.94)


@glyph("h", 0x68)
def h(p):
    V, xh, os = p.V, p.xh, p.os
    W = nW(p)
    cy = xh + os - arch_ry(p)
    s = U(rect(0, 0, V, p.asc), arch(p, 0, W, xh + os, cy), rect(W - V, 0, W, cy))
    return G(s, p.sb, p.sb * 0.94)


@glyph("m", 0x6D)
def m(p):
    V, xh, os = p.V, p.xh, p.os
    W = p.w(732, 2.05)
    Vm = V * 0.97
    cy = xh + os - arch_ry(p) * 0.98
    xm = W / 2.0
    s = U(rect(0, 0, V, xh),
          arch(p, 0, xm + Vm / 2, xh + os, cy, j=p.joint * 0.9),
          rect(xm - Vm / 2, 0, xm + Vm / 2, cy),
          arch(p, xm - Vm / 2, W, xh + os, cy, V=Vm, j=p.joint * 0.9),
          rect(W - V, 0, W, cy))
    return G(s, p.sb, p.sb * 0.94)


@glyph("u", 0x75)
def u(p):
    g = n(p)
    b = bounds(g.shape)
    return G(rot180(g.shape, (b[0] + b[2]) / 2, p.xh / 2), p.sb * 0.94, p.sb)


@glyph("r", 0x72)
def r(p):
    V, H, xh, os = p.V, p.H, p.xh, p.os
    W = nW(p) * 0.96
    cy = xh + os - arch_ry(p)
    a = arch(p, 0, W, xh + os, cy)
    ob = (p.joint, cy - arch_ry(p), W, xh + os)
    ib = (V, cy - arch_ry(p) + H, W - V, xh + os - H)
    cx, cyy, rx, ry = mid_radii(ob, ib)
    ln = cutline(cx, cyy, rx, ry, 48, 0.55, flat=False)
    a = D(a, I(rightof(cx), side(ln, far(cx, cy, 1, -0.2))))
    s = U(rect(0, 0, V, xh), a)
    return G(s, p.sb, p.sbd + 6)


@glyph("o", 0x6F)
def o(p):
    V, H, xh, os = p.V, p.H, p.xh, p.os
    W = oW(p)
    s = ring((0, -os, W, xh + os), (V, -os + H, W - V, xh + os - H), p.ko, p.ki)
    return G(s, p.sbo, p.sbo)


def _bowl_glyph(p, ascend, descend):
    V, H, xh, os = p.V, p.H, p.xh, p.os
    W = oW(p) * 0.985 + 0.06 * V
    top = p.asc if ascend else xh
    bot = p.desc if descend else 0
    s = U(rect(0, bot, V, top), bowl(p, 0, W, -os, xh + os))
    return s


@glyph("b", 0x62)
def b(p):
    return G(_bowl_glyph(p, True, False), p.sb, p.sbo)


@glyph("p", 0x70)
def p_(p):
    return G(_bowl_glyph(p, False, True), p.sb, p.sbo)


@glyph("d", 0x64)
def d(p):
    s = _bowl_glyph(p, True, False)
    return G(flipx(s, 0), p.sbo, p.sb)


@glyph("q", 0x71)
def q(p):
    s = _bowl_glyph(p, False, True)
    return G(flipx(s, 0), p.sbo, p.sb)


@glyph("c", 0x63)
def c(p):
    V, H, xh, os = p.V, p.H, p.xh, p.os
    W = oW(p) * 0.93
    ob = (0, -os, W, xh + os)
    ib = (V, -os + H, W - V, xh + os - H)
    s = ring(ob, ib, p.ko, p.ki)
    cx, cy, rx, ry = mid_radii(ob, ib)
    ref = far(cx, cy, 1, 0)
    t = cutline(cx, cy, rx, ry, 40, TV)
    bt = cutline(cx, cy, rx, ry, -40, TV)
    s = D(s, I(rightof(cx), side(t, ref), side(bt, ref)))
    return G(s, p.sbo, p.sbo * 0.55)


@glyph("e", 0x65)
def e(p):
    V, xh, os = p.V, p.xh, p.os
    H = p.H * (1 - 0.0008 * p.dv)
    W = oW(p) * 0.95
    ob = (0, -os, W, xh + os)
    ib = (V, -os + H, W - V, xh + os - H)
    s = ring(ob, ib, p.ko, p.ki)
    cx, cy, rx, ry = mid_radii(ob, ib)
    bh = H * (0.9 - 0.0013 * p.dv)
    btop = xh * 0.5 + bh * 0.5 + 6
    bbot = btop - bh
    bt = cutline(cx, cy, rx, ry, -36, TV)
    s = D(s, I(rightof(cx), below(bbot), side(bt, far(cx, bbot, 1, 0))))
    bar = I(rect(V * 0.5, bbot, W, btop), ellipse(*ob, k=p.ko))
    s = U(s, bar)
    return G(s, p.sbo, p.sbo * 0.8)


@glyph("a", 0x61)
def a(p):
    """Double-storey grotesque a."""
    V, H, xh, os = p.V, p.H, p.xh, p.os
    W = p.w(478, 0.95)
    top = xh + os
    ry = arch_ry(p) * 0.92
    cy = top - ry
    ob = (W * 0.04, cy - ry, W, top)
    ib = (W * 0.04 + V * 0.92, cy - ry + H, W - V, top - H)
    hood = I(ring(ob, ib, p.ko, p.ki), above(cy))
    cx, _, rx, rry = mid_radii(ob, ib)
    ln = cutline(cx, cy, rx, rry, 148, 0.25)
    hood = D(hood, I(leftof(cx), side(ln, far(cx, cy, -1, -0.6))))
    # bowl: round on the left, flat top running straight into the stem
    bt = xh * 0.54 + 0.36 * V
    y0 = -os
    R = (bt - y0) / 2.0
    xs = W - V + 1
    k = p.ko + 0.02
    outer = U(rect(R, y0, xs, bt), I(ellipse(0, y0, 2 * R, bt, k), leftof(R + 0.5)))
    tv, th = V * 0.96, H * 0.9
    inner = I(ellipse(tv, y0 + H, xs + (xs - tv) * 0.6, bt - th, 0.7), leftof(xs))
    bowl_ = D(outer, inner)
    s = U(hood, bowl_, rect(W - V, y0, W, cy))
    return G(s, p.sbo * 0.9, p.sb)


@glyph("a.ss01")
def a_ss01(p):
    """Single-storey a (stylistic set 1)."""
    V, H, xh, os = p.V, p.H, p.xh, p.os
    W = oW(p) * 0.985 + 0.06 * V
    s = U(rect(0, 0, V, xh), bowl(p, 0, W, -os, xh + os))
    return G(flipx(s, 0), p.sbo, p.sb)


def s_build(p, W, top, V, H, os, ts_ratio=1.1, ym_ratio=0.515, ta=42, tb=222, tv=0.55):
    ts = H * ts_ratio
    ym = top * ym_ratio
    du = W * 0.035
    # upper ring
    obu = (du, ym - ts / 2, W - du, top + os)
    ibu = (du + V * 0.95, ym + ts / 2, W - du - V * 0.95, top + os - H)
    up = ring(obu, ibu, p.ko, p.ki)
    cx, cyu, rx, ryu = mid_radii(obu, ibu)
    ln = cutline(cx, cyu, rx, ryu, ta, tv)
    up = D(up, I(rightof(cx), side(ln, far(cx, cyu, 0.2, -1))), I(rightof(cx), below(cyu)))
    # lower ring
    obl = (0, -os, W, ym + ts / 2)
    ibl = (V, -os + H, W - V, ym - ts / 2)
    lo = ring(obl, ibl, p.ko, p.ki)
    cx2, cyl, rx2, ryl = mid_radii(obl, ibl)
    ln2 = cutline(cx2, cyl, rx2, ryl, tb, tv)
    lo = D(lo, I(leftof(cx2), side(ln2, far(cx2, cyl, -0.2, 1))), I(leftof(cx2), above(cyl)))
    return U(up, lo)


@glyph("s", 0x73)
def s(p):
    W = p.w(408, 1.05)
    sh = s_build(p, W, p.xh, p.V, p.H * 0.88, p.os, ts_ratio=1.16)
    return G(sh, p.sbo * 0.9, p.sbo * 0.9)


@glyph("t", 0x74)
def t(p):
    V, H, xh, os = p.V, p.H, p.xh, p.os
    tx = p.w(64, 0.25)
    ttop = xh + 150
    W = p.w(300, 0.9)
    # stem with diagonal-sliced top
    stem = rect(tx, 0, tx + V, ttop)
    stem = D(stem, halfplane(tx - 1, ttop - 0.62 * V - 30, tx + V, ttop + 1))
    # hook
    R = p.w(150, 0.6)
    hy = arch_ry(p) * 0.82
    ob = (tx, -os, tx + 2 * R + V * 0.3, -os + 2 * hy)
    ib = (tx + V, -os + H, tx + 2 * R + V * 0.3 - V, -os + 2 * hy - H)
    hk = I(ring(ob, ib, p.ko, p.ki), below((ob[1] + ob[3]) / 2))
    cx, cy, rx, ry = mid_radii(ob, ib)
    ln = cutline(cx, cy, rx, ry, -48, 0.45, flat=False)
    hk = D(hk, I(rightof(cx), side(ln, far(cx, cy, 1, 0.3))))
    stem = U(I(stem, above(cy)), hk)
    bar = rect(0, xh - H, W, xh)
    s = U(stem, bar)
    return G(s, p.sbd + 4, p.sbd + 2)


@glyph("f", 0x66)
def f(p):
    V, H, xh, os = p.V, p.H, p.xh, p.os
    fx = p.w(56, 0.25)
    W = p.w(268, 0.8)
    R = p.w(136, 0.7)
    hy = arch_ry(p) * 0.86
    top = p.asc + os
    ob = (fx, top - 2 * hy, fx + 2 * R + V * 0.3, top)
    ib = (fx + V, top - 2 * hy + H, fx + 2 * R + V * 0.3 - V, top - H)
    hk = I(ring(ob, ib, p.ko, p.ki), above((ob[1] + ob[3]) / 2))
    cx, cy, rx, ry = mid_radii(ob, ib)
    ln = cutline(cx, cy, rx, ry, 44, 0.45, flat=False)
    hk = D(hk, I(rightof(cx), side(ln, far(cx, cy, 1, -0.3))))
    stem = U(rect(fx, 0, fx + V, cy), hk)
    bar = rect(0, xh - H, W, xh)
    s = U(stem, bar)
    return G(s, p.sbd + 4, p.sbd - 4)


@glyph("i", 0x69)
def i(p):
    V = p.V
    s = U(rect(0, 0, V, p.xh), dot(V / 2, dot_y(p), dot_d(p)))
    return G(s, p.sb, p.sb)


@glyph("dotlessi", 0x131)
def dotlessi(p):
    return G(rect(0, 0, p.V, p.xh), p.sb, p.sb)


def _jhook(p):
    V, H, xh, os = p.V, p.H, p.xh, p.os
    R = p.w(142, 0.8)
    hy = arch_ry(p) * 0.7
    bot = p.desc - os
    x1 = V
    ob = (x1 - 2 * R - V * 0.2, bot, x1, bot + 2 * hy)
    ib = (ob[0] + V, bot + H, x1 - V, bot + 2 * hy - H)
    hk = I(ring(ob, ib, p.ko, p.ki), below((ob[1] + ob[3]) / 2))
    cx, cy, rx, ry = mid_radii(ob, ib)
    ln = cutline(cx, cy, rx, ry, 222, 0.45, flat=False)
    hk = D(hk, I(leftof(cx), side(ln, far(cx, cy, -1, 0.3))))
    return U(rect(0, cy, V, xh), hk)


@glyph("j", 0x6A)
def j(p):
    s = U(_jhook(p), dot(p.V / 2, dot_y(p), dot_d(p)))
    return G(s, p.sb * 0.95 + bounds(s)[0], p.sb, top_anchor=p.V / 2)


@glyph("dotlessj", 0x237)
def dotlessj(p):
    s = _jhook(p)
    return G(s, p.sb * 0.95 + bounds(s)[0], p.sb)


@glyph("l", 0x6C)
def l(p):
    return G(rect(0, 0, p.V, p.asc), p.sb, p.sb)


def k_build(p, W, top, stem_top, V, D_, ya_r=0.12, t=0.47):
    ya = top * ya_r
    ax0 = V * 0.4 + 0.0
    wa = hwidth(D_, W - V, top - ya)
    ax0 = V * 0.4 + wa / 2 - V * 0.2
    ax1 = W - wa / 2
    arm = diag(ax0, ya, ax1, top, wa)
    arm = I(arm, rightof(0), below(top))
    px = ax0 + (ax1 - ax0) * t
    py = ya + (top - ya) * t
    wl = hwidth(D_ * 1.04, W - px, py)
    dxl = (W - wl / 2) - px
    leg = diag(W - wl / 2, 0, px - dxl * 0.5, py * 1.5, wl)
    leg = I(leg, above(0), halfplane(ax1, top, ax0, ya))
    s = U(rect(0, 0, V, stem_top), arm, leg)
    return I(s, rightof(0))


@glyph("k", 0x6B)
def k(p):
    W = p.w(412, 0.95)
    s = k_build(p, W, p.xh, p.asc, p.V, p.D * 0.96, ya_r=0.27, t=0.45)
    return G(s, p.sb, p.sbd)


def vshape(p, W, H, D_, flat):
    """Two diagonals meeting at a flat vertex at the bottom."""
    cx = W / 2.0
    run = cx - flat / 2
    w = hwidth(D_, run, H)
    l_ = para(cx - flat / 2, cx - flat / 2 + w, 0, 0, w, H)
    r_ = para(cx + flat / 2 - w, cx + flat / 2, 0, W - w, W, H)
    hull = poly([(0, H), (cx - flat / 2, 0), (cx + flat / 2, 0), (W, H)])
    return I(U(l_, r_), hull), w


@glyph("v", 0x76)
def v(p):
    W = p.w(470, 1.05)
    s, _ = vshape(p, W, p.xh, p.D, 0.3 * p.V)
    return G(s, p.sbd, p.sbd)


def wshape(p, W, top, D_, flat):
    q = W / 4.0
    wd = hwidth(D_, q - flat / 2, top)
    f2 = flat / 2
    s1 = para(q - f2, q - f2 + wd, 0, 0, wd, top)
    s2 = para(q + f2 - wd, q + f2, 0, 2 * q - f2, 2 * q - f2 + wd, top)
    s3 = para(3 * q - f2, 3 * q - f2 + wd, 0, 2 * q + f2 - wd, 2 * q + f2, top)
    s4 = para(3 * q + f2 - wd, 3 * q + f2, 0, W - wd, W, top)

    def left_of(x0, x1):  # left of the upward edge (x0,0)->(x1,top)
        return halfplane(x0, 0, x1, top)

    def right_of(x0, x1):
        return halfplane(x1, top, x0, 0)

    s1 = I(s1, left_of(q + f2, 2 * q - f2 + wd))
    s2 = I(s2, right_of(q - f2, 0), left_of(3 * q - f2 + wd, 2 * q + f2))
    s3 = I(s3, right_of(q + f2 - wd, 2 * q - f2), left_of(3 * q + f2, W))
    s4 = I(s4, right_of(3 * q - f2, 2 * q + f2 - wd))
    return I(U(s1, s2, s3, s4), band(0, top))


@glyph("w", 0x77)
def w(p):
    W = p.w(720, 1.75)
    s = wshape(p, W, p.xh, p.D * 0.93, 0.26 * p.V)
    return G(s, p.sbd, p.sbd)


def xshape(p, W, top, D_):
    inset = W * 0.025
    w1 = solve_w(D_, W - inset, top)
    a_ = para(0, w1, 0, W - inset - w1, W - inset, top)
    b_ = para(W - w1, W, 0, inset, inset + w1, top)
    hull = poly([(0, 0), (W, 0), (W - inset, top), (inset, top)])
    return I(U(a_, b_), hull)


@glyph("x", 0x78)
def x(p):
    W = p.w(440, 1.0)
    s = xshape(p, W, p.xh, p.D * 0.98)
    return G(s, p.sbd, p.sbd)


@glyph("y", 0x79)
def y(p):
    W = p.w(470, 1.05)
    xh = p.xh
    D_ = p.D
    cx = W / 2.0
    flat = 0.3 * p.V
    run = cx - flat / 2
    w_ = hwidth(D_, run, xh)
    # right stroke continues to the descender along the same line
    x_top_r = W - w_ / 2
    x_bot_r = cx + flat / 2 - w_ / 2
    slope = (x_top_r - x_bot_r) / xh
    yd = p.desc
    right = diag(x_bot_r + slope * yd, yd, x_top_r, xh, w_)
    left = para(cx - flat / 2, cx - flat / 2 + w_, 0, 0, w_, xh)
    hull = poly([(0, xh), (cx - flat / 2, 0), (W, xh)])
    s = U(right, I(left, above(0), hull))
    return G(s, p.sbd, p.sbd)


def zshape(p, W, top, H, D_):
    wd = solve_w(D_, W, top - H)
    diag_ = para(0, wd, H * 0.5, W - wd, W, top - H * 0.5)
    return U(rect(0, 0, W, H), rect(W * 0.03, top - H, W, top), diag_)


@glyph("z", 0x7A)
def z(p):
    W = p.w(400, 0.95)
    s = zshape(p, W, p.xh, p.H, p.D * 0.92)
    return G(s, p.sbd + 10, p.sbd + 10)


@glyph("g", 0x67)
def g(p):
    V, H, xh, os = p.V, p.H, p.xh, p.os
    W = oW(p) * 0.985 + 0.06 * V
    bowl_ = bowl(p, 0, W, -os, xh + os)
    # descender hook
    bot = p.desc - os
    hy = arch_ry(p) * 0.78
    ob = (W * 0.06, bot, W, bot + 2 * hy)
    ib = (W * 0.06 + V, bot + H, W - V, bot + 2 * hy - H)
    hk = I(ring(ob, ib, p.ko, p.ki), below((ob[1] + ob[3]) / 2))
    cx, cy, rx, ry = mid_radii(ob, ib)
    ln = cutline(cx, cy, rx, ry, 205, 0.6)
    hk = D(hk, I(leftof(cx), side(ln, far(cx, cy, -1, 0.3))))
    s = U(flipx(U(bowl_, rect(0, cy, V, xh)), W / 2), hk)
    return G(s, p.sbo, p.sb)


@glyph("germandbls", 0xDF)
def germandbls(p):
    V, os = p.V, p.os
    H = p.H * (1 - p.dv / 600)
    top = p.asc
    W = p.w(474, 1.8)
    ym = p.xh * 0.98 - p.dv * 0.6
    xl0 = V * 0.6
    cx = (xl0 + W) / 2
    Wu = 2 * cx
    # upper ring: stem side + shoulder, ends at its bottom centre
    obu = (0, ym - H / 2, Wu, top + os)
    ibu = (V, ym + H / 2, Wu - V, top + os - H)
    up = ring(obu, ibu, p.ko, p.ki)
    cyu = (obu[1] + obu[3]) / 2
    up = D(up, I(leftof(Wu / 2), below(cyu)))
    # lower bowl, open to the lower left
    obl = (xl0, -os, W, ym + H / 2)
    ibl = (xl0 + V, -os + H, W - V, ym - H / 2)
    lo = ring(obl, ibl, p.ko, p.ki)
    cx2, cyl, rx2, ryl = mid_radii(obl, ibl)
    lo = D(lo, I(leftof(cx2), above(cyl)))
    lo = D(lo, I(leftof(cx2), side(cutline(cx2, cyl, rx2, ryl, 236, 0.2), far(cx2, cyl, -1, 1))))
    sh = U(rect(0, 0, V, cyu), up, lo)
    return G(sh, p.sb, p.sbo)


@glyph("space", 0x20)
def space(p):
    return G(rect(0, 0, 0, 0), 0, 0, adv=p.w(240, 0.3))
