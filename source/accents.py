"""Diacritical marks and accented letters (built as merged outlines)."""

import geom
from geom import (U, D, I, rect, ring, para, poly, move, flipx, flipy, band,
                  bounds, rightof, leftof, above, below)
from lower import dot_d, dot_y, vshape
from common import dot


def _t(p, cap):
    return (p.CV * 0.92 if cap else p.V * 0.98)


def acute(p, cap):
    t = _t(p, cap)
    h = 128 if cap else 166
    h += 0.12 * p.dv
    wb = t * 1.25
    sh = h * 0.42
    return para(-wb / 2 - sh, wb / 2 - sh, 0, -wb / 2 + sh, wb / 2 + sh, h)


def grave(p, cap):
    return flipx(acute(p, cap), 0)


def circumflex(p, cap):
    t = _t(p, cap) * 0.92
    w = p.w(300, 0.75) * (1.08 if cap else 1.0)
    h = (120 if cap else 156) + 0.12 * p.dv
    s, _ = vshape(p, w, h, t, t * 0.42)
    s = flipy(s, h / 2)
    return move(s, -w / 2, 0)


def caron(p, cap):
    t = _t(p, cap) * 0.92
    w = p.w(300, 0.75) * (1.08 if cap else 1.0)
    h = (120 if cap else 156) + 0.12 * p.dv
    s, _ = vshape(p, w, h, t, t * 0.42)
    return move(s, -w / 2, 0)


def dieresis(p, cap):
    d = dot_d(p) * (0.9 if cap else 1.0)
    g = d + 46 + 0.55 * p.V
    return U(dot(-g / 2, d / 2, d), dot(g / 2, d / 2, d))


def dotaccent(p, cap):
    d = dot_d(p) * (0.98 if cap else 1.0)
    return dot(0, d / 2, d)


def ringacc(p, cap):
    dr = p.w(190, 0.85) * (0.95 if cap else 1.0)
    t = _t(p, cap) * 0.66
    return ring((-dr / 2, 0, dr / 2, dr), (-dr / 2 + t, t, dr / 2 - t, dr - t))


def tilde(p, cap):
    from symbols import _wave
    w = p.w(330, 1.45)
    t = _t(p, cap) * 0.78
    s = _wave(p, w, t, 0)
    b = bounds(s)
    sc = (0.8 if cap else 1.0)
    s = geom.scale(s, 1.0, sc)
    b = bounds(s)
    return move(s, -w / 2, -b[1])


def macron(p, cap):
    w = p.w(300, 0.7)
    H = (p.CH if cap else p.H) * 0.95
    return rect(-w / 2, 0, w / 2, H)


def breve(p, cap):
    w = p.w(290, 0.7)
    t = _t(p, cap) * 0.86
    h = (110 if cap else 140) + 0.1 * p.dv
    r = ring((-w / 2, h * 0.0 - h, w / 2, h), (-w / 2 + t, -h + t * 0.9, w / 2 - t, h - t * 0.9), 0.56, 0.58)
    r = I(r, below(h * 0.0 + 0.0001 + h * 0.0))
    b = bounds(r)
    return move(r, 0, -b[1])


def hungarumlaut(p, cap):
    a = acute(p, cap)
    g = _t(p, cap) * 0.95 + 40
    return U(move(a, -g), move(a, g))


def cedilla(p, cap):
    t = _t(p, cap) * 0.95
    return poly([(-t * 0.42, 6), (t * 0.48, 6), (t * 0.12, -175 - 0.1 * p.dv), (-t * 0.92, -175 - 0.1 * p.dv)])


MARKS = {
    "acute": acute, "grave": grave, "circumflex": circumflex, "caron": caron,
    "dieresis": dieresis, "dotaccent": dotaccent, "ring": ringacc, "tilde": tilde,
    "macron": macron, "breve": breve, "hungarumlaut": hungarumlaut, "cedilla": cedilla,
}

# name: (codepoint, base, mark)
COMPOSITES = {}


def _add(spec):
    for name, cp, base, mark in spec:
        COMPOSITES[name] = (cp, base, mark)


_V = [("A", "a"), ("E", "e"), ("I", "dotlessi"), ("O", "o"), ("U", "u")]
_tbl = [
    ("Agrave", 0xC0, "A", "grave"), ("Aacute", 0xC1, "A", "acute"), ("Acircumflex", 0xC2, "A", "circumflex"),
    ("Atilde", 0xC3, "A", "tilde"), ("Adieresis", 0xC4, "A", "dieresis"), ("Aring", 0xC5, "A", "ring"),
    ("Ccedilla", 0xC7, "C", "cedilla"),
    ("Egrave", 0xC8, "E", "grave"), ("Eacute", 0xC9, "E", "acute"), ("Ecircumflex", 0xCA, "E", "circumflex"),
    ("Edieresis", 0xCB, "E", "dieresis"),
    ("Igrave", 0xCC, "I", "grave"), ("Iacute", 0xCD, "I", "acute"), ("Icircumflex", 0xCE, "I", "circumflex"),
    ("Idieresis", 0xCF, "I", "dieresis"),
    ("Ntilde", 0xD1, "N", "tilde"),
    ("Ograve", 0xD2, "O", "grave"), ("Oacute", 0xD3, "O", "acute"), ("Ocircumflex", 0xD4, "O", "circumflex"),
    ("Otilde", 0xD5, "O", "tilde"), ("Odieresis", 0xD6, "O", "dieresis"),
    ("Ugrave", 0xD9, "U", "grave"), ("Uacute", 0xDA, "U", "acute"), ("Ucircumflex", 0xDB, "U", "circumflex"),
    ("Udieresis", 0xDC, "U", "dieresis"), ("Yacute", 0xDD, "Y", "acute"),
    ("agrave", 0xE0, "a", "grave"), ("aacute", 0xE1, "a", "acute"), ("acircumflex", 0xE2, "a", "circumflex"),
    ("atilde", 0xE3, "a", "tilde"), ("adieresis", 0xE4, "a", "dieresis"), ("aring", 0xE5, "a", "ring"),
    ("ccedilla", 0xE7, "c", "cedilla"),
    ("egrave", 0xE8, "e", "grave"), ("eacute", 0xE9, "e", "acute"), ("ecircumflex", 0xEA, "e", "circumflex"),
    ("edieresis", 0xEB, "e", "dieresis"),
    ("igrave", 0xEC, "dotlessi", "grave"), ("iacute", 0xED, "dotlessi", "acute"),
    ("icircumflex", 0xEE, "dotlessi", "circumflex"), ("idieresis", 0xEF, "dotlessi", "dieresis"),
    ("ntilde", 0xF1, "n", "tilde"),
    ("ograve", 0xF2, "o", "grave"), ("oacute", 0xF3, "o", "acute"), ("ocircumflex", 0xF4, "o", "circumflex"),
    ("otilde", 0xF5, "o", "tilde"), ("odieresis", 0xF6, "o", "dieresis"),
    ("ugrave", 0xF9, "u", "grave"), ("uacute", 0xFA, "u", "acute"), ("ucircumflex", 0xFB, "u", "circumflex"),
    ("udieresis", 0xFC, "u", "dieresis"), ("yacute", 0xFD, "y", "acute"), ("ydieresis", 0xFF, "y", "dieresis"),
    ("Ydieresis", 0x178, "Y", "dieresis"),
    ("Amacron", 0x100, "A", "macron"), ("amacron", 0x101, "a", "macron"),
    ("Abreve", 0x102, "A", "breve"), ("abreve", 0x103, "a", "breve"),
    ("Cacute", 0x106, "C", "acute"), ("cacute", 0x107, "c", "acute"),
    ("Ccaron", 0x10C, "C", "caron"), ("ccaron", 0x10D, "c", "caron"),
    ("Dcaron", 0x10E, "D", "caron"),
    ("Emacron", 0x112, "E", "macron"), ("emacron", 0x113, "e", "macron"),
    ("Edotaccent", 0x116, "E", "dotaccent"), ("edotaccent", 0x117, "e", "dotaccent"),
    ("Ecaron", 0x11A, "E", "caron"), ("ecaron", 0x11B, "e", "caron"),
    ("Gbreve", 0x11E, "G", "breve"), ("gbreve", 0x11F, "g", "breve"),
    ("Imacron", 0x12A, "I", "macron"), ("imacron", 0x12B, "dotlessi", "macron"),
    ("Idotaccent", 0x130, "I", "dotaccent"),
    ("Lacute", 0x139, "L", "acute"), ("lacute", 0x13A, "l", "acute"),
    ("Nacute", 0x143, "N", "acute"), ("nacute", 0x144, "n", "acute"),
    ("Ncaron", 0x147, "N", "caron"), ("ncaron", 0x148, "n", "caron"),
    ("Omacron", 0x14C, "O", "macron"), ("omacron", 0x14D, "o", "macron"),
    ("Ohungarumlaut", 0x150, "O", "hungarumlaut"), ("ohungarumlaut", 0x151, "o", "hungarumlaut"),
    ("Racute", 0x154, "R", "acute"), ("racute", 0x155, "r", "acute"),
    ("Rcaron", 0x158, "R", "caron"), ("rcaron", 0x159, "r", "caron"),
    ("Sacute", 0x15A, "S", "acute"), ("sacute", 0x15B, "s", "acute"),
    ("Scedilla", 0x15E, "S", "cedilla"), ("scedilla", 0x15F, "s", "cedilla"),
    ("Scaron", 0x160, "S", "caron"), ("scaron", 0x161, "s", "caron"),
    ("Tcaron", 0x164, "T", "caron"),
    ("Umacron", 0x16A, "U", "macron"), ("umacron", 0x16B, "u", "macron"),
    ("Uring", 0x16E, "U", "ring"), ("uring", 0x16F, "u", "ring"),
    ("Uhungarumlaut", 0x170, "U", "hungarumlaut"), ("uhungarumlaut", 0x171, "u", "hungarumlaut"),
    ("Zacute", 0x179, "Z", "acute"), ("zacute", 0x17A, "z", "acute"),
    ("Zdotaccent", 0x17B, "Z", "dotaccent"), ("zdotaccent", 0x17C, "z", "dotaccent"),
    ("Zcaron", 0x17D, "Z", "caron"), ("zcaron", 0x17E, "z", "caron"),
]
_add(_tbl)
# stylistic-set single-storey a with accents
for _n, (_cp, _b, _m) in list(COMPOSITES.items()):
    if _b == "a":
        COMPOSITES[_n + ".ss01"] = (None, "a.ss01", _m)

# spacing accents
SPACING = {"acute": 0xB4, "grave": 0x60, "dieresis": 0xA8, "macron": 0xAF, "cedilla": 0xB8,
           "circumflex": 0x2C6, "caron": 0x2C7, "ring": 0x2DA, "tilde": 0x2DC, "breve": 0x2D8,
           "dotaccent": 0x2D9, "hungarumlaut": 0x2DD}


def _is_cap(name):
    return name[0].isupper()


def _band_center(shape, y0, y1):
    sl = I(shape, band(y0, y1))
    b = bounds(sl)
    if b[2] - b[0] <= 0:
        b = bounds(shape)
    return (b[0] + b[2]) / 2


def place(p, base_shape, base_name, mark_name, anchor=None):
    cap = _is_cap(base_name)
    mk = MARKS[mark_name](p, cap)
    bb = bounds(base_shape)
    if mark_name == "cedilla":
        x = _band_center(base_shape, -20, 60)
        return U(base_shape, move(mk, x, 0))
    if cap:
        top = p.cap
        gap = 36 + 0.12 * p.CV
        x = _band_center(base_shape, top - 90, top + 30)
    else:
        top = p.xh
        if bb[3] > p.xh + 80:
            top = p.asc
        gap = 52 + 0.34 * p.V
        x = _band_center(base_shape, top - 120, top + 30)
    if anchor is not None:
        x = anchor
    y = top + gap
    if mark_name in ("dieresis", "dotaccent") and not cap and top == p.xh:
        y = dot_y(p) - dot_d(p) / 2
    if mark_name == "ring" and cap and base_name == "A":
        y = top + gap * 0.55
    return U(base_shape, move(mk, x, y))


def build_composites(p, glyphs, cmap, info):
    for name, (cp, base, mark) in COMPOSITES.items():
        if base not in glyphs:
            continue
        shape, adv = glyphs[base]
        s = place(p, shape, base, mark, info.get(base, {}).get("anchor"))
        glyphs[name] = (s, adv)
        if cp is not None:
            cmap[cp] = name
    # spacing marks
    for mname, cp in SPACING.items():
        mk = MARKS[mname](p, False)
        b = bounds(mk)
        sb = 40 + 0.2 * p.V
        if mname == "cedilla":
            mk = move(mk, sb - b[0], 0)
        else:
            mk = move(mk, sb - b[0], p.xh + 52 + 0.34 * p.V - b[1])
        adv = int(round((b[2] - b[0]) + 2 * sb))
        nm = {"ring": "ringspacing", "tilde": "tildespacing", "circumflex": "circumflexspacing",
              "caron": "caronspacing", "breve": "brevespacing", "dotaccent": "dotaccentspacing",
              "hungarumlaut": "hungarumlautspacing", "acute": "acutespacing", "grave": "gravespacing",
              "dieresis": "dieresisspacing", "macron": "macronspacing", "cedilla": "cedillaspacing"}[mname]
        glyphs[nm] = (mk, adv)
        cmap[cp] = nm
    # nbsp
    if "space" in glyphs:
        glyphs["nbspace"] = glyphs["space"]
        cmap[0xA0] = "nbspace"
