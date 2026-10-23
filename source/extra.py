"""Extended Latin letters that need their own construction."""

from geom import (U, D, I, rect, ellipse, ring, poly, para, hwidth, line,
                  above, below, leftof, rightof, band, flipx, move, bounds)
from common import glyph, G
import lower
import upper


def _shape(fn, p):
    s = fn(p).shape
    b = bounds(s)
    return move(s, -b[0]), b[2] - b[0]


@glyph("AE", 0xC6)
def AE(p):
    V, CH, cap = p.CV, p.CH, p.cap
    xa = p.w(330, 0.65)
    EW = p.w(420, 0.9)
    wd = solve(p, xa, cap)
    leg = para(0, wd, 0, xa - wd * 0.2, xa + wd * 0.8, cap)
    leg = I(leg, band(0, cap), leftof(xa + V))
    stem_x = xa
    yb = cap * 0.5 - CH / 2
    s = U(leg, rect(stem_x, 0, stem_x + V, cap),
          rect(stem_x, cap - CH, stem_x + EW, cap),
          rect(stem_x, yb, stem_x + EW * 0.92, yb + CH),
          rect(stem_x, 0, stem_x + EW, CH),
          I(rect(0, cap * 0.25, stem_x + 1, cap * 0.25 + CH), rightof(0)))
    s = I(s, U(rightof(stem_x), poly([(0, 0), (xa + wd * 0.8, cap), (xa + wd * 0.8 + 999, cap), (xa + 999, 0)])))
    return G(s, p.sbd, p.sbd + 18)


def solve(p, run, h):
    return hwidth(p.CD, run, h)


@glyph("ae", 0xE6)
def ae(p):
    a, aw = _shape(lower.a, p)
    e, ew = _shape(lower.e, p)
    return G(U(a, move(e, aw - p.V * 1.1)), p.sbo * 0.9, p.sbo * 0.8)


@glyph("OE", 0x152)
def OE(p):
    V, CH, cap, os = p.CV, p.CH, p.cap, p.cos
    W = upper.OW(p) * 0.86
    o = ring((0, -os, W, cap + os), (V, -os + CH, W - V, cap + os - CH), p.ko, p.ki)
    xs = W * 0.5
    o = I(o, leftof(xs + 1))
    EW = p.w(400, 0.9)
    yb = cap * 0.5 - CH / 2
    s = U(o, rect(xs, 0, xs + V, cap), rect(xs - 1, cap - CH, xs + EW, cap),
          rect(xs, yb, xs + EW * 0.92, yb + CH), rect(xs - 1, 0, xs + EW, CH))
    return G(s, p.csbo, p.sbd + 18)


@glyph("oe", 0x153)
def oe(p):
    o, ow = _shape(lower.o, p)
    e, ew = _shape(lower.e, p)
    return G(U(o, move(e, ow - p.V * 1.05)), p.sbo, p.sbo * 0.8)


def _slashed(shape, p, top, t, ext=0.06):
    b = bounds(shape)
    w = b[2] - b[0]
    sl = line(b[0] - w * ext, -top * ext, b[2] + w * ext, top * (1 + ext), t)
    return U(shape, sl)


@glyph("Oslash", 0xD8)
def Oslash(p):
    s = upper.O(p).shape
    return G(_slashed(s, p, p.cap, p.CV * 0.8), p.csbo * 0.6, p.csbo * 0.6)


@glyph("oslash", 0xF8)
def oslash(p):
    s = lower.o(p).shape
    return G(_slashed(s, p, p.xh, p.V * 0.8), p.sbo * 0.6, p.sbo * 0.6)


def _lslash(stem_x, V, ym, t, half):
    return line(stem_x + V / 2 - half, ym - half * 0.55, stem_x + V / 2 + half, ym + half * 0.55, t)


@glyph("Lslash", 0x141)
def Lslash(p):
    s = upper.L(p).shape
    sl = _lslash(0, p.CV, p.cap * 0.48, p.CH * 0.9, p.w(130, 0.4))
    return G(U(s, sl), p.sbd + 10, p.sbd + 4)


@glyph("lslash", 0x142)
def lslash(p):
    s = lower.l(p).shape
    sl = _lslash(0, p.V, p.asc * 0.5, p.H * 0.9, p.w(120, 0.4))
    return G(U(s, sl), p.sbd + 10, p.sbd + 10)


def _dcroat(p):
    s = upper.D_(p).shape
    ym = p.cap * 0.5
    bar_l = p.w(80, 0.3)
    return U(move(s, bar_l), rect(0, ym - p.CH / 2, bar_l + p.CV + p.w(110, 0.3), ym + p.CH / 2))


@glyph("Dcroat", 0x110)
def Dcroat(p):
    return G(_dcroat(p), p.sbd + 10, p.csbo)


@glyph("Eth", 0xD0)
def Eth(p):
    return G(_dcroat(p), p.sbd + 10, p.csbo)


@glyph("dcroat", 0x111)
def dcroat(p):
    s = lower.d(p).shape
    b = bounds(s)
    y = p.asc - 120 - p.H * 0.3
    s = U(s, rect(b[2] - p.V - p.w(110, 0.3), y, b[2] + p.w(40, 0.2), y + p.H * 0.9))
    return G(s, p.sbo, p.sbd + 6)


@glyph("eth", 0xF0)
def eth(p):
    V, H, xh = p.V, p.H, p.xh
    o, ow = _shape(lower.o, p)
    x0 = ow - V
    stem = para(x0, ow, xh * 0.5, x0 - ow * 0.28, ow - ow * 0.28, p.asc)
    stem = I(stem, rightof(ow * 0.3))
    ys = p.asc - (p.asc - xh) * 0.55
    bar = line(ow * 0.32, ys - 40, ow * 0.98, ys + 40, H * 0.85)
    return G(U(o, stem, bar), p.sbo, p.sbo)


@glyph("Thorn", 0xDE)
def Thorn(p):
    V, CH, cap = p.CV, p.CH, p.cap
    W = p.w(540, 1.2)
    y0, y1 = cap * 0.17, cap * 0.82
    bw = upper.dshape(p, 0, W, y0, y1, (y1 - y0) * 0.5, V, CH)
    return G(U(bw, rect(0, 0, V, cap)), p.csb, p.csbo)


@glyph("thorn", 0xFE)
def thorn(p):
    s = lower._bowl_glyph(p, False, True)
    s = U(s, rect(0, 0, p.V, p.asc))
    return G(s, p.sb, p.sbo)
