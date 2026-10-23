"""Punctuation, symbols, currency, arrows."""

import copy
import math

from geom import (U, D, I, rect, ellipse, ring, poly, para, hwidth, line,
                  above, below, leftof, rightof, band, flipx, flipy, rot180,
                  rotate, move, scale, bounds, wedge, circle, halfplane, skew)
from common import glyph, G, cutline, side, mid_radii, far, dot
import lower
import upper
import figures
from lower import TV, solve_w, dot_d, s_build


def axis(p):
    """Math / punctuation axis height."""
    return p.xh * 0.5 + 18


def pd(p):
    """Punctuation dot diameter."""
    return dot_d(p) * 1.06


def heavier(p, f):
    """Copy of the params with strokes multiplied by f (for small forms
    that get scaled down afterwards)."""
    q = copy.copy(p)
    for k in ("V", "H", "CV", "CH", "D", "CD"):
        setattr(q, k, getattr(p, k) * f)
    q.dv = q.V - 86.0
    q.joint = p.joint * f
    return q


def small(p, fn, s, f=None):
    """Glyph `fn` drawn with heavier strokes, scaled by s."""
    f = f if f is not None else (0.78 / s)
    q = heavier(p, f)
    q.dv = p.dv  # keep proportions of this weight
    g = fn(q)
    return scale(g.shape, s, s)


def sx(shape):
    b = bounds(shape)
    return move(shape, -b[0])


# ---------------------------------------------------------------------------
# dots & commas


def comma_shape(p, d=None):
    d = pd(p) if d is None else d
    r = d / 2
    tail = poly([(d * 0.99, r * 1.0), (d * 0.62, -d * 0.95), (d * 0.14, -d * 0.95), (d * 0.3, r * 0.3)])
    return U(dot(r, r, d), tail)


@glyph("period", 0x2E)
def period(p):
    d = pd(p)
    return G(dot(d / 2, d / 2, d), p.sb * 0.8, p.sb * 0.8)


@glyph("comma", 0x2C)
def comma(p):
    return G(comma_shape(p), p.sb * 0.8, p.sb * 0.8)


@glyph("colon", 0x3A)
def colon(p):
    d = pd(p)
    return G(U(dot(d / 2, d / 2, d), dot(d / 2, p.xh - d / 2, d)), p.sb * 0.9, p.sb * 0.9)


@glyph("semicolon", 0x3B)
def semicolon(p):
    d = pd(p)
    return G(U(comma_shape(p), dot(d / 2, p.xh - d / 2, d)), p.sb * 0.9, p.sb * 0.9)


@glyph("ellipsis", 0x2026)
def ellipsis(p):
    d = pd(p)
    g = d * 0.75 + 30
    return G(U(*[dot(d / 2 + i * (d + g), d / 2, d) for i in range(3)]), p.sb * 0.8, p.sb * 0.8)


@glyph("periodcentered", 0xB7)
def periodcentered(p):
    d = pd(p)
    return G(dot(d / 2, axis(p) + 20, d), p.sb * 0.8, p.sb * 0.8)


@glyph("bullet", 0x2022)
def bullet(p):
    d = pd(p) * 1.5 + 30
    return G(dot(d / 2, axis(p) + 20, d), p.sb, p.sb)


@glyph("exclam", 0x21)
def exclam(p):
    d = pd(p)
    V = p.CV * 1.02
    gap = d * 0.45 + 40
    cx = d / 2
    stem = rect(cx - V / 2, d + gap, cx + V / 2, p.cap)
    return G(U(stem, dot(cx, d / 2, d)), p.sb, p.sb)


def _qmark(p):
    d = pd(p)
    V, H, cap, os = p.CV, p.CH, p.cap, p.cos
    W = p.w(410, 0.9)
    gap = d * 0.45 + 40
    h = cap * 0.56 + 0.1 * p.dv
    ob = (0, cap + os - h, W, cap + os)
    ib = (V * 0.95, cap + os - h + H, W - V, cap + os - H)
    r = ring(ob, ib, p.ko, p.ki)
    cx, cy, rx, ry = mid_radii(ob, ib)
    r = D(r, I(leftof(cx), below(cy)))
    r = D(r, I(leftof(cx), side(cutline(cx, cy, rx, ry, 160, TV), far(cx, cy, -1, -1))))
    sx_ = cx - V * 0.5 + V * 0.05
    stem = rect(sx_, d + gap, sx_ + V * 0.95, ob[1] + H)
    return U(r, stem, dot(sx_ + V * 0.475, d / 2, d))


@glyph("question", 0x3F)
def question(p):
    return G(_qmark(p), p.sbo * 0.8, p.sbo * 0.8)


def _inverted(p, shape):
    b = bounds(shape)
    c = (p.cap + p.desc + 80) / 2
    return rot180(shape, (b[0] + b[2]) / 2, c)


@glyph("exclamdown", 0xA1)
def exclamdown(p):
    return G(_inverted(p, exclam(p).shape), p.sb, p.sb)


@glyph("questiondown", 0xBF)
def questiondown(p):
    return G(_inverted(p, _qmark(p)), p.sbo * 0.8, p.sbo * 0.8)


# ---------------------------------------------------------------------------
# quotes


def _tick(p):
    V = p.CV * 0.92
    h = p.cap * 0.3
    return poly([(0, p.cap), (V, p.cap), (V * 0.86, p.cap - h), (V * 0.14, p.cap - h)])


@glyph("quotesingle", 0x27)
def quotesingle(p):
    return G(_tick(p), p.sb, p.sb)


@glyph("quotedbl", 0x22)
def quotedbl(p):
    V = p.CV * 0.92
    return G(U(_tick(p), move(_tick(p), V + 40 + 0.4 * V)), p.sb, p.sb)


def _q_up(p):
    """Comma raised to the cap height (right quote)."""
    c = comma_shape(p)
    d = pd(p)
    return move(c, 0, p.cap - d)


def _q_down(p):
    c = comma_shape(p)
    d = pd(p)
    b = bounds(c)
    return rot180(move(c, 0, p.cap - d), (b[0] + b[2]) / 2, p.cap - d + (d - (b[1])) / 2 - (d * 0.95 - d) / 2 * 0 + 0) if False else \
        move(rot180(c, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2), 0, p.cap - b[3])


def _pair(p, a):
    d = pd(p)
    return U(a, move(a, d + 30 + 0.3 * p.V))


@glyph("quoteright", 0x2019)
def quoteright(p):
    return G(_q_up(p), p.sb * 0.8, p.sb * 0.8)


@glyph("quoteleft", 0x2018)
def quoteleft(p):
    return G(_q_down(p), p.sb * 0.8, p.sb * 0.8)


@glyph("quotedblright", 0x201D)
def quotedblright(p):
    return G(_pair(p, _q_up(p)), p.sb * 0.8, p.sb * 0.8)


@glyph("quotedblleft", 0x201C)
def quotedblleft(p):
    return G(_pair(p, _q_down(p)), p.sb * 0.8, p.sb * 0.8)


@glyph("quotesinglbase", 0x201A)
def quotesinglbase(p):
    return G(comma_shape(p), p.sb * 0.8, p.sb * 0.8)


@glyph("quotedblbase", 0x201E)
def quotedblbase(p):
    return G(_pair(p, comma_shape(p)), p.sb * 0.8, p.sb * 0.8)


def chevron(w, h, t, y, blunt=0.1):
    """Left-pointing chevron: tip at (0, y), arms reaching x=w at y +- h/2,
    stroke thickness t (perpendicular)."""
    th = math.atan2(h / 2.0, w)
    dx = t / math.sin(th)
    dx = min(dx, w * 0.8)
    dy = dx * math.tan(th)
    pts = [(0, y), (w, y + h / 2), (w, y + h / 2 - dy), (dx, y), (w, y - h / 2 + dy), (w, y - h / 2)]
    return I(poly(pts), rightof(t * blunt))


def _chev(p, w, h, t):
    return chevron(w, h, t, axis(p))


def _guil(p, double, right):
    t = p.V * 0.74
    w = max(p.w(178, 0.0), 2.3 * t)
    h = 1.68 * w
    c = _chev(p, w, h, t)
    if double:
        c = U(c, move(c, w * 0.62 + 30 + 0.25 * p.V))
    if right:
        b = bounds(c)
        c = flipx(c, (b[0] + b[2]) / 2)
    return c


@glyph("guilsinglleft", 0x2039)
def guilsinglleft(p):
    return G(_guil(p, False, False), p.sbd + 20, p.sbd + 20)


@glyph("guilsinglright", 0x203A)
def guilsinglright(p):
    return G(_guil(p, False, True), p.sbd + 20, p.sbd + 20)


@glyph("guillemotleft", 0xAB)
def guillemotleft(p):
    return G(_guil(p, True, False), p.sbd + 20, p.sbd + 20)


@glyph("guillemotright", 0xBB)
def guillemotright(p):
    return G(_guil(p, True, True), p.sbd + 20, p.sbd + 20)


# ---------------------------------------------------------------------------
# dashes & brackets


@glyph("hyphen", 0x2D)
def hyphen(p):
    H = p.H * 1.05
    y = axis(p) - H / 2
    return G(rect(0, y, p.w(250, 0.6), y + H), p.sbd + 26, p.sbd + 26)


@glyph("endash", 0x2013)
def endash(p):
    H = p.H * 1.05
    y = axis(p) - H / 2
    return G(rect(0, y, 500, y + H), 0, 0, adv=500 + 2 * 30, xoff=30)


@glyph("emdash", 0x2014)
def emdash(p):
    H = p.H * 1.05
    y = axis(p) - H / 2
    return G(rect(0, y, 1000, y + H), 0, 0, adv=1000, xoff=0)


@glyph("underscore", 0x5F)
def underscore(p):
    H = p.H
    return G(rect(0, -150, 520, -150 + H), 0, 0, adv=520, xoff=0)


def _paren(p):
    """Crescent: an oval minus the same oval shifted right."""
    V = p.CV * 0.92
    yb, yt = p.desc + 40, p.cap + 60
    hgt = yt - yb
    W = p.w(170, 0.6)
    e = hgt * 0.06
    o = ellipse(0, yb - e, W * 2.6, yt + e, 0.5523)
    r = D(o, move(o, V, 0))
    return I(r, band(yb, yt), leftof(W))


@glyph("parenleft", 0x28)
def parenleft(p):
    return G(_paren(p), p.sbo + 20, p.sb * 0.7)


@glyph("parenright", 0x29)
def parenright(p):
    return G(flipx(_paren(p), 0), p.sb * 0.7, p.sbo + 20)


def _bracket(p):
    V, H = p.CV * 0.95, p.CH
    yb, yt = p.desc + 40, p.cap + 60
    W = p.w(170, 0.7)
    return U(rect(0, yb, V, yt), rect(0, yt - H, W, yt), rect(0, yb, W, yb + H))


@glyph("bracketleft", 0x5B)
def bracketleft(p):
    return G(_bracket(p), p.sb + 10, p.sbd + 4)


@glyph("bracketright", 0x5D)
def bracketright(p):
    return G(flipx(_bracket(p), 0), p.sbd + 4, p.sb + 10)


def _brace(p):
    V, H = p.CV * 0.92, p.CH
    yb, yt = p.desc + 40, p.cap + 60
    ym = (yb + yt) / 2
    xs = p.w(90, 0.6)
    W = xs + V + p.w(110, 0.5)
    stem = U(rect(xs, yb, xs + V, yt))
    s = U(stem, rect(xs, yt - H, W, yt), rect(xs, yb, W, yb + H),
          rect(0, ym - H / 2, xs + 1, ym + H / 2))
    s = D(s, rect(xs - 1, ym - H / 2 - V * 0.35 - 10, xs + V * 0.45, ym - H / 2 - 10 + 0.01) if False else None)
    return s


@glyph("braceleft", 0x7B)
def braceleft(p):
    return G(_brace(p), p.sbd + 20, p.sbd + 4)


@glyph("braceright", 0x7D)
def braceright(p):
    return G(flipx(_brace(p), 0), p.sbd + 4, p.sbd + 20)


def _slash(p, yb=None, yt=None, W=None):
    yb = -120 if yb is None else yb
    yt = p.cap + 40 if yt is None else yt
    W = p.w(330, 0.9) if W is None else W
    wd = solve_w(p.D * 0.98, W, yt - yb)
    return para(0, wd, yb, W - wd, W, yt)


@glyph("slash", 0x2F)
def slash(p):
    return G(_slash(p), p.sbd + 4, p.sbd + 4)


@glyph("backslash", 0x5C)
def backslash(p):
    return G(flipx(_slash(p), 0), p.sbd + 4, p.sbd + 4)


@glyph("bar", 0x7C)
def bar(p):
    return G(rect(0, p.desc + 20, p.V * 0.95, p.cap + 80), p.sb + 20, p.sb + 20)


@glyph("brokenbar", 0xA6)
def brokenbar(p):
    yb, yt = p.desc + 20, p.cap + 80
    ym = (yb + yt) / 2
    g = 40 + 0.3 * p.V
    return G(U(rect(0, yb, p.V * 0.95, ym - g / 2), rect(0, ym + g / 2, p.V * 0.95, yt)), p.sb + 20, p.sb + 20)


# ---------------------------------------------------------------------------
# math


def _mw(p):
    return p.w(470, 0.8)


def _mt(p):
    return p.V * 0.92


@glyph("plus", 0x2B)
def plus(p):
    W, t, y = _mw(p), _mt(p), axis(p)
    s = U(rect(0, y - t / 2, W, y + t / 2), rect(W / 2 - t / 2, y - W / 2, W / 2 + t / 2, y + W / 2))
    return G(s, p.sb, p.sb)


@glyph("minus", 0x2212)
def minus(p):
    W, t, y = _mw(p), _mt(p), axis(p)
    return G(rect(0, y - t / 2, W, y + t / 2), p.sb, p.sb)


@glyph("multiply", 0xD7)
def multiply(p):
    W, t, y = _mw(p) * 0.86, _mt(p), axis(p)
    s = U(rect(0, y - t / 2, W, y + t / 2), rect(W / 2 - t / 2, y - W / 2, W / 2 + t / 2, y + W / 2))
    return G(rotate(s, 45, W / 2, y), p.sb, p.sb)


@glyph("divide", 0xF7)
def divide(p):
    W, t, y = _mw(p), _mt(p), axis(p)
    d = pd(p) * 0.95
    gp = t / 2 + d / 2 + 26 + 0.15 * p.V
    s = U(rect(0, y - t / 2, W, y + t / 2), dot(W / 2, y + gp, d), dot(W / 2, y - gp, d))
    return G(s, p.sb, p.sb)


@glyph("equal", 0x3D)
def equal(p):
    W, t, y = _mw(p), _mt(p) * 0.92, axis(p)
    g = t * 0.6 + 50
    s = U(rect(0, y + g / 2, W, y + g / 2 + t), rect(0, y - g / 2 - t, W, y - g / 2))
    return G(s, p.sb, p.sb)


@glyph("plusminus", 0xB1)
def plusminus(p):
    W, t, y = _mw(p), _mt(p) * 0.94, axis(p) + 60
    a = W / 2 - 20
    s = U(rect(0, y - t / 2, W, y + t / 2), rect(W / 2 - t / 2, y - a, W / 2 + t / 2, y + a),
          rect(0, y - a - 50 - t * 0.6 - t, W, y - a - 50 - t * 0.6))
    return G(s, p.sb, p.sb)


def _angle(p):
    """'<' shape."""
    W = _mw(p) * 0.92
    h = W * 1.2
    return _chev2(p, W, h, _mt(p) * 0.88)


def _chev2(p, w, h, t):
    return chevron(w, h, t, axis(p), blunt=0.15)


@glyph("less", 0x3C)
def less(p):
    return G(_angle(p), p.sb, p.sb)


@glyph("greater", 0x3E)
def greater(p):
    return G(flipx(_angle(p), 0), p.sb, p.sb)


@glyph("asciicircum", 0x5E)
def asciicircum(p):
    W = _mw(p)
    h = p.cap * 0.42
    t = _mt(p)
    s, _ = lower.vshape(p, W, h, t, t * 0.45)
    s = move(flipy(s, h / 2), 0, p.cap - h)
    return G(s, p.sbd + 10, p.sbd + 10)


def _wave(p, W, t, y):
    """Geometric tilde: two half rings."""
    r = W / 4.0
    hgt = r * 1.0
    a = I(ring((0, y - hgt, 2 * r + t / 2, y + hgt), (t, y - hgt + t * 0.9, 2 * r - t / 2, y + hgt - t * 0.9), 0.56, 0.58), above(y))
    b = I(ring((2 * r - t / 2, y - hgt, W, y + hgt), (2 * r + t / 2, y - hgt + t * 0.9, W - t, y + hgt - t * 0.9), 0.56, 0.58), below(y))
    return U(a, b, rect(2 * r - t / 2, y - 1, 2 * r + t / 2, y + 1))


@glyph("asciitilde", 0x7E)
def asciitilde(p):
    W = _mw(p)
    return G(_wave(p, W, _mt(p) * 0.92, axis(p)), p.sb, p.sb)


@glyph("logicalnot", 0xAC)
def logicalnot(p):
    W, t, y = _mw(p), _mt(p), axis(p)
    s = U(rect(0, y, W, y + t), rect(W - t, y - W * 0.36, W, y + t))
    return G(s, p.sb, p.sb)


@glyph("degree", 0xB0)
def degree(p):
    d = p.w(250, 0.6)
    t = p.V * 0.8
    s = ring((0, p.cap - d, d, p.cap), (t, p.cap - d + t, d - t, p.cap - t))
    return G(s, p.sb * 0.8, p.sb * 0.8)


@glyph("asterisk", 0x2A)
def asterisk(p):
    L = p.w(180, 0.25)
    t = p.H * 1.0
    cy = p.cap - L
    spokes = [rotate(rect(-t / 2, 0, t / 2, L), a, 0, 0) for a in (0, 72, 144, 216, 288)]
    s = move(U(*spokes), 0, cy)
    return G(s, p.sbd + 14, p.sbd + 14)


@glyph("numbersign", 0x23)
def numbersign(p):
    W = p.w(560, 1.1)
    h = p.cap
    t = p.V * 0.9
    sl = h * 0.16
    v1 = para(W * 0.2, W * 0.2 + t * 1.03, 0, W * 0.2 + sl, W * 0.2 + sl + t * 1.03, h)
    v2 = move(v1, W * 0.36)
    hz = t * 0.92
    y1, y2 = h * 0.27, h * 0.66
    s = U(v1, v2, rect(0, y1, W * 0.94, y1 + hz), rect(W * 0.06, y2, W, y2 + hz))
    s = I(s, rightof(0))
    return G(s, p.sbd + 8, p.sbd + 8)


@glyph("percent", 0x25)
def percent(p):
    V, H = p.V * 0.9, p.H * 0.9
    d = p.w(250, 0.5)
    h = p.cap * 0.42
    o1 = ring((0, p.cap - h, d, p.cap), (V, p.cap - h + H, d - V, p.cap - H), p.ko, p.ki)
    W = d * 2.55
    o2 = move(o1, W - d, -(p.cap - h))
    sl = _slash(p, yb=0, yt=p.cap, W=W * 0.8)
    sl = move(sl, W * 0.1)
    return G(U(o1, o2, sl), p.sbo, p.sbo)


@glyph("ampersand", 0x26)
def ampersand(p):
    V, H, cap, os = p.CV, p.CH, p.cap, p.cos
    W = p.w(640, 1.4)
    # upper loop
    ym = cap * 0.53
    lb = (W * 0.1, ym - H * 0.4, W * 0.62, cap + os)
    loop = ring(lb, (lb[0] + V * 0.9, lb[1] + H, lb[2] - V * 0.9, lb[3] - H), p.ko, p.ki)
    cxl = (lb[0] + lb[2]) / 2
    loop = D(loop, I(rightof(cxl), below((lb[1] + lb[3]) / 2)))
    # lower bowl
    bb = (0, -os, W * 0.8, ym + H * 0.6)
    bowl = ring(bb, (V, -os + H, bb[2] - V, bb[3] - H), p.ko, p.ki)
    cx, cy, rx, ry = mid_radii(bb, (V, -os + H, bb[2] - V, bb[3] - H))
    bowl = D(bowl, wedge(cx, cy, 8, 110))
    bowl = D(bowl, I(rightof(cx), side(cutline(cx, cy, rx, ry, 8, 0.0), far(cx, cy, 1, 1))))
    # leg: from the loop's lower right down to the baseline at the right
    x_top = cxl - V * 0.1
    wd = hwidth(p.CD, W - x_top, ym)
    leg = para(W - wd, W, 0, x_top - wd * 0.5, x_top + wd * 0.5, ym + H * 0.2)
    leg = I(leg, below(ym + H * 0.2), above(0))
    return G(U(loop, bowl, leg), p.sbo, p.sbd)


@glyph("at", 0x40)
def at(p):
    V, H = p.V * 0.86, p.H * 0.82
    R = p.w(420, 0.9)
    cy = p.cap * 0.42
    t = H
    outer = ring((0, cy - R, 2 * R, cy + R), (t * 1.05, cy - R + t, 2 * R - t * 1.05, cy + R - t), p.ko, p.ki)
    cx = R
    # inner single-storey a
    r_in = R * 0.44
    ib = (cx - r_in - V * 0.35, cy - r_in, cx + r_in - V * 0.35, cy + r_in)
    bowl = ring(ib, (ib[0] + V, ib[1] + H, ib[2] - V, ib[3] - H), p.ko, p.ki)
    sx0 = ib[2] - V
    stem = rect(sx0, cy - r_in * 1.15, sx0 + V, cy + r_in)
    # tail joining the outer ring
    ang = math.radians(-28)
    ex = cx + (R - t / 2) * math.cos(ang)
    ey = cy + (R - t / 2) * math.sin(ang)
    tail = I(ring((sx0, ey - (ey - (cy - r_in * 1.15)) - 1, 2 * R - t * 0.0, cy + r_in * 0.2),
                  (sx0 + V, ey - (ey - (cy - r_in * 1.15)) - 1 + H, 2 * R - t, cy + r_in * 0.2 - H), p.ko, p.ki),
             below(cy - r_in * 0.4 + 0.0))
    outer = D(outer, wedge(cx, cy, -28, 2))
    s = U(outer, bowl, stem, I(tail, rightof(sx0)))
    return G(s, p.sbo, p.sbo)


@glyph("section", 0xA7)
def section(p):
    W = p.w(420, 1.0)
    h = p.cap * 0.62
    V, H = p.V, p.H * 0.92
    a = s_build(p, W, h, V, H, p.os)
    b = move(a, 0, -h * 0.4)
    a = move(a, 0, p.cap - h)
    return G(U(a, b), p.sbo, p.sbo)


@glyph("paragraph", 0xB6)
def paragraph(p):
    V, H, cap = p.V, p.H, p.cap
    W = p.w(520, 1.0)
    bw = W * 0.62
    yb = cap * 0.4
    bowlf = U(I(ellipse(0, yb, bw * 2 - V, cap, p.ko), leftof(bw - V / 2)), rect(bw - V, yb, W, cap))
    x2 = W - V
    s = U(bowlf, rect(bw - V, -150, bw, cap), rect(x2, -150, W, cap))
    return G(s, p.sbo, p.sb)


def _ringmark(p):
    R = p.cap * 0.52 + 6
    t = p.H * 0.62
    cy = p.cap / 2
    return ring((0, cy - R, 2 * R, cy + R), (t, cy - R + t, 2 * R - t, cy + R - t), 0.5523, 0.5523), R, cy


@glyph("copyright", 0xA9)
def copyright(p):
    r, R, cy = _ringmark(p)
    c = sx(small(p, upper.C, 0.5, f=1.15))
    b = bounds(c)
    c = move(c, R - (b[2] - b[0]) / 2 + R * 0.04, cy - (b[1] + b[3]) / 2)
    return G(U(r, c), p.sbo, p.sbo)


@glyph("registered", 0xAE)
def registered(p):
    r, R, cy = _ringmark(p)
    c = sx(small(p, upper.R, 0.5, f=1.15))
    b = bounds(c)
    c = move(c, R - (b[2] - b[0]) / 2 + R * 0.04, cy - (b[1] + b[3]) / 2)
    return G(U(r, c), p.sbo, p.sbo)


@glyph("trademark", 0x2122)
def trademark(p):
    s = 0.42
    t = sx(small(p, upper.T, s, f=1.25))
    m = sx(small(p, upper.M, s, f=1.25))
    bt = bounds(t)
    m = move(m, bt[2] + 30)
    tm = move(U(t, m), 0, p.cap - p.cap * s)
    return G(tm, p.sbd + 10, p.sbd + 10)


# ---------------------------------------------------------------------------
# currency


@glyph("dollar", 0x24)
def dollar(p):
    g = upper.S(p)
    sh = g.shape
    b = bounds(sh)
    cx = (b[0] + b[2]) / 2
    t = p.CV * 0.72
    s = U(sh, rect(cx - t / 2, p.cap, cx + t / 2, p.cap + 90), rect(cx - t / 2, -90, cx + t / 2, 0))
    return G(s, p.csbo, p.csbo)


@glyph("cent", 0xA2)
def cent(p):
    sh = lower.c(p).shape
    b = bounds(sh)
    cx = (b[0] + b[2]) / 2 + p.V * 0.2
    t = p.V * 0.72
    s = U(sh, rect(cx - t / 2, p.xh, cx + t / 2, p.xh + 110), rect(cx - t / 2, -110, cx + t / 2, 0))
    return G(s, p.sbo, p.sbo * 0.55)


@glyph("Euro", 0x20AC)
def Euro(p):
    sh = upper.C(p).shape
    b = bounds(sh)
    sh = move(sh, -b[0] + p.w(70, 0.3))
    H = p.CH * 0.86
    W = (b[2] - b[0]) * 0.8
    y1 = p.cap * 0.56
    y2 = p.cap * 0.33
    s = U(sh, rect(0, y1, W, y1 + H), rect(0, y2, W * 0.92, y2 + H))
    return G(s, p.sbd + 4, p.csbo * 0.6)


@glyph("sterling", 0xA3)
def sterling(p):
    V, H, cap, os = p.CV, p.CH, p.cap, p.cos
    W = p.w(500, 1.1)
    xs = p.w(80, 0.35)
    R = W * 0.36
    hy = cap * 0.3
    top = cap + os
    ob = (xs, top - 2 * hy, xs + 2 * R + V * 0.3, top)
    ib = (xs + V, top - 2 * hy + H, xs + 2 * R + V * 0.3 - V, top - H)
    hk = I(ring(ob, ib, p.ko, p.ki), above((ob[1] + ob[3]) / 2))
    cx, cy, rx, ry = mid_radii(ob, ib)
    hk = D(hk, I(rightof(cx), side(cutline(cx, cy, rx, ry, 30, 0.8), far(cx, cy, 1, -0.3))))
    stem = rect(xs, H * 0.5, xs + V, cy)
    yb = cap * 0.4
    s = U(hk, stem, rect(0, yb, W * 0.72, yb + H * 0.95), rect(0, 0, W, H))
    return G(s, p.sbd + 10, p.sbd + 10)


@glyph("yen", 0xA5)
def yen(p):
    sh = upper.Y(p).shape
    b = bounds(sh)
    W = b[2] - b[0]
    H = p.CH * 0.86
    y1 = p.cap * 0.3
    y2 = y1 - H - 40 - 0.2 * p.V
    s = U(sh, rect(b[0] + W * 0.18, y1, b[2] - W * 0.18, y1 + H),
          rect(b[0] + W * 0.18, y2, b[2] - W * 0.18, y2 + H))
    return G(s, p.sbd, p.sbd)


@glyph("currency", 0xA4)
def currency(p):
    d = p.w(380, 0.6)
    t = p.V * 0.86
    y = axis(p)
    r = ring((0, y - d / 2, d, y + d / 2), (t, y - d / 2 + t, d - t, y + d / 2 - t))
    k = d * 0.22
    sp = [line(-k * 0.35, y + d / 2 + k * 0.35, k * 0.6, y + d / 2 - k * 0.6, t * 0.8)]
    s = r
    for a in (0, 90, 180, 270):
        s = U(s, rotate(sp[0], a, d / 2, y))
    return G(s, p.sbo, p.sbo)


# ---------------------------------------------------------------------------
# arrows (handy for posters & ads)


def _arrow(p):
    """Right-pointing arrow on the axis."""
    t = p.V * 0.98
    L = p.w(740, 1.0)
    h = p.w(500, 1.0)
    y = axis(p) + 30
    tip_w = h * 0.5
    head = poly([(L, y), (L - tip_w, y + h / 2), (L - tip_w, y - h / 2)])
    head = I(head, leftof(L - t * 0.1))
    shaft = rect(0, y - t / 2, L - t, y + t / 2)
    return U(shaft, head), y


@glyph("arrowright", 0x2192)
def arrowright(p):
    a, _ = _arrow(p)
    return G(a, p.sb, p.sb)


@glyph("arrowleft", 0x2190)
def arrowleft(p):
    a, _ = _arrow(p)
    return G(flipx(a, 0), p.sb, p.sb)


@glyph("arrowup", 0x2191)
def arrowup(p):
    a, y = _arrow(p)
    b = bounds(a)
    cx = (b[0] + b[2]) / 2
    r = rotate(a, 90, cx, y)
    b2 = bounds(r)
    r = move(r, 0, -b2[1] + (p.cap - (b2[3] - b2[1])) / 2)
    return G(r, p.sb, p.sb)


@glyph("arrowdown", 0x2193)
def arrowdown(p):
    a, y = _arrow(p)
    b = bounds(a)
    cx = (b[0] + b[2]) / 2
    r = rotate(a, -90, cx, y)
    b2 = bounds(r)
    r = move(r, 0, -b2[1] + (p.cap - (b2[3] - b2[1])) / 2)
    return G(r, p.sb, p.sb)


def _diag_arrow(p, deg):
    a, y = _arrow(p)
    a = scale(a, 0.86, 0.86)
    b = bounds(a)
    r = rotate(a, deg, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
    b2 = bounds(r)
    return move(r, 0, -b2[1] + (p.cap - (b2[3] - b2[1])) / 2)


@glyph("arrowupright", 0x2197)
def arrowupright(p):
    return G(_diag_arrow(p, 45), p.sbd + 20, p.sbd + 20)


@glyph("arrowdownright", 0x2198)
def arrowdownright(p):
    return G(_diag_arrow(p, -45), p.sbd + 20, p.sbd + 20)


# ---------------------------------------------------------------------------
# superiors, fractions, ordinals


SUPS = 0.6


def _sup(p, fn, raise_to=None):
    s = sx(small(p, fn, SUPS, f=1.3))
    b = bounds(s)
    top = p.cap + 0 if raise_to is None else raise_to
    return move(s, 0, top - b[3] + (p.cos * SUPS if True else 0) - 4)


@glyph("onesuperior", 0xB9)
def onesuperior(p):
    return G(_sup(p, figures.one), p.sbd + 14, p.sbd + 14)


@glyph("twosuperior", 0xB2)
def twosuperior(p):
    return G(_sup(p, figures.two), p.sbd + 14, p.sbd + 14)


@glyph("threesuperior", 0xB3)
def threesuperior(p):
    return G(_sup(p, figures.three), p.sbd + 14, p.sbd + 14)


def _frac(p, num, den):
    n = _sup(p, num)
    d = sx(small(p, den, SUPS, f=1.3))
    bd = bounds(d)
    d = move(d, 0, -bd[1])
    bn = bounds(n)
    W = 540 + 0.5 * p.dv
    sl = _slash(p, yb=-10, yt=p.cap + 10, W=W * 0.62)
    sl = move(sl, (bn[2] - bn[0]) * 0.55)
    bs = bounds(sl)
    d = move(d, bs[2] - (bn[2] - bn[0]) * 0.45 - bd[0])
    return U(n, sl, d)


@glyph("onehalf", 0xBD)
def onehalf(p):
    return G(_frac(p, figures.one, figures.two), p.sbd + 10, p.sbd + 10)


@glyph("onequarter", 0xBC)
def onequarter(p):
    return G(_frac(p, figures.one, figures.four), p.sbd + 10, p.sbd + 10)


@glyph("threequarters", 0xBE)
def threequarters(p):
    return G(_frac(p, figures.three, figures.four), p.sbd + 10, p.sbd + 10)


@glyph("ordfeminine", 0xAA)
def ordfeminine(p):
    a = sx(small(p, lower.a, 0.62, f=1.25))
    b = bounds(a)
    a = move(a, 0, p.cap - b[3])
    return G(a, p.sbd + 14, p.sbd + 14)


@glyph("ordmasculine", 0xBA)
def ordmasculine(p):
    a = sx(small(p, lower.o, 0.62, f=1.25))
    b = bounds(a)
    a = move(a, 0, p.cap - b[3])
    return G(a, p.sbd + 14, p.sbd + 14)


@glyph("mu", 0xB5)
def mu(p):
    sh = lower.u(p).shape
    b = bounds(sh)
    s = U(sh, rect(b[0], p.desc, b[0] + p.V, p.xh))
    return G(s, p.sb, p.sb)
