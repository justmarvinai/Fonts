"""Build the Formwerk font family.

    python3 source/build.py            # all weights -> fonts/
    python3 source/build.py Bold       # a single weight
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.ttLib import TTFont

import geom
from params import WEIGHTS, UPM
import common
import lower  # noqa: F401  (registers glyphs)
import upper  # noqa: F401
import figures  # noqa: F401
import symbols  # noqa: F401
import extra  # noqa: F401
import accents
import features

FAMILY = "Formwerk"
VERSION = "1.000"
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "fonts")


def round_path(path):
    """Draw a pathops path into a fresh one with integer coordinates."""
    from fontTools.pens.roundingPen import RoundingPen
    out = geom.Path()
    path.draw(RoundingPen(out.getPen()))
    try:
        out.simplify(fix_winding=True)
    except Exception:
        pass
    return out


def build_glyphs(p):
    glyphs = {}  # name -> (path, advance)
    cmap = {}
    info = {}
    for name in common.ORDER:
        cp, fn = common.REGISTRY[name]
        g = fn(p)
        shape = g.shape
        b = geom.bounds(shape)
        if g.adv is not None:
            dx = g.xoff if g.xoff is not None else 0
            adv = g.adv
        else:
            dx = g.l - b[0]
            adv = g.l + (b[2] - b[0]) + g.r
        shape = geom.move(shape, dx, 0)
        anchor = (g.top_anchor + dx) if g.top_anchor is not None else None
        glyphs[name] = (shape, int(round(adv)))
        info[name] = dict(anchor=anchor)
        if cp is not None:
            cps = cp if isinstance(cp, (list, tuple)) else [cp]
            for c in cps:
                cmap[c] = name
    accents.build_composites(p, glyphs, cmap, info)
    glyphs = {k: (round_path(v[0]), v[1]) for k, v in glyphs.items()}
    return glyphs, cmap


def glyph_order(glyphs):
    order = [".notdef", "space"]
    for n in common.ORDER:
        if n not in order:
            order.append(n)
    for n in glyphs:
        if n not in order:
            order.append(n)
    return order


def notdef(p):
    w = 500
    s = geom.D(geom.rect(50, 0, w - 50, p.cap), geom.rect(50 + 60, 60, w - 110, p.cap - 60))
    return s, w


def make_font(p, flavor):
    glyphs, cmap = build_glyphs(p)
    glyphs[".notdef"] = notdef(p)
    order = glyph_order(glyphs)
    order = [n for n in order if n in glyphs]

    fb = FontBuilder(UPM, isTTF=(flavor == "ttf"))
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)

    metrics = {}
    if flavor == "ttf":
        ttglyphs = {}
        for n in order:
            path, adv = glyphs[n]
            pen = TTGlyphPen(None)
            path.draw(Cu2QuPen(pen, max_err=0.6, reverse_direction=True))
            ttglyphs[n] = pen.glyph()
        fb.setupGlyf(ttglyphs)
        for n in order:
            g = ttglyphs[n]
            g.recalcBounds(fb.font["glyf"]) if hasattr(g, "recalcBounds") else None
            lsb = getattr(g, "xMin", 0) if g.numberOfContours else 0
            metrics[n] = (glyphs[n][1], lsb)
    else:
        charstrings = {}
        for n in order:
            path, adv = glyphs[n]
            pen = T2CharStringPen(adv, None)
            path.draw(pen)
            charstrings[n] = pen.getCharString()
            bp = BoundsPen(None)
            path.draw(bp)
            lsb = int(round(bp.bounds[0])) if bp.bounds else 0
            metrics[n] = (adv, lsb)
        ps_name = f"{FAMILY}-{p.name}"
        fb.setupCFF(ps_name, {"FullName": f"{FAMILY} {p.name}", "FamilyName": FAMILY,
                              "Weight": p.name}, charstrings, {})

    fb.setupHorizontalMetrics(metrics)
    asc, desc = 960, -260
    fb.setupHorizontalHeader(ascent=asc, descent=desc, lineGap=0)
    style = p.name
    is_bold = style == "Bold"
    family_name = FAMILY if style in ("Regular", "Bold") else f"{FAMILY} {style}"
    sub = style if style in ("Regular", "Bold") else "Regular"
    names = {
        "copyright": "Copyright 2026 The Formwerk Project Authors",
        "familyName": family_name,
        "styleName": sub,
        "uniqueFontIdentifier": f"{VERSION};{FAMILY}-{style}",
        "fullName": f"{FAMILY} {style}",
        "version": f"Version {VERSION}",
        "psName": f"{FAMILY}-{style}",
        "typographicFamily": FAMILY,
        "typographicSubfamily": style,
        "designer": "Formwerk Project",
        "description": "Formwerk - a bold industrial grotesque for posters, social ads and text.",
        "licenseDescription": "This Font Software is licensed under the SIL Open Font License, Version 1.1.",
        "licenseInfoURL": "https://openfontlicense.org",
    }
    fb.setupNameTable(names)
    fs = 0
    if is_bold:
        fs |= 1 << 5
    if style == "Regular":
        fs |= 1 << 6
    fs |= 1 << 7  # USE_TYPO_METRICS
    fb.setupOS2(
        usWeightClass=p.weight_class,
        usWidthClass=5,
        fsSelection=fs,
        sTypoAscender=800, sTypoDescender=-240, sTypoLineGap=160,
        usWinAscent=asc, usWinDescent=-desc,
        sxHeight=p.xh, sCapHeight=p.cap,
        achVendID="FMWK",
        fsType=0,
        ulCodePageRange1=(1 << 0) | (1 << 1),
        panose={"bFamilyType": 2, "bSerifStyle": 11, "bWeight": {400: 5, 500: 6, 700: 8, 900: 10}[p.weight_class],
                "bProportion": 3, "bContrast": 2, "bStrokeVariation": 2, "bArmStyle": 2,
                "bLetterForm": 2, "bMidline": 2, "bXHeight": 4},
    )
    fb.font["OS/2"].version = 4
    fb.setupPost(isFixedPitch=0, underlinePosition=-120, underlineThickness=int(p.H * 0.7))
    fb.font["head"].macStyle = 1 if is_bold else 0
    fea = features.build(p, glyphs, cmap, fb.font)
    addOpenTypeFeaturesFromString(fb.font, fea)
    if flavor != "ttf":
        fb.font["CFF "].cff.topDictIndex[0].Private.StdHW = int(p.H)
    return fb.font


def main(argv):
    names = argv[1:] or [w.name for w in WEIGHTS]
    for sub in ("otf", "ttf", "webfonts"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    for p in WEIGHTS:
        if p.name not in names:
            continue
        for flavor in ("otf", "ttf"):
            font = make_font(p, flavor)
            path = os.path.join(OUT, flavor, f"{FAMILY}-{p.name}.{flavor}")
            font.save(path)
            print("wrote", os.path.relpath(path, ROOT))
            if flavor == "ttf":
                hinted = path
                try:
                    import ttfautohint
                    ttfautohint.ttfautohint(in_file=path, out_file=hinted, hinting_range_max=96,
                                            no_info=True)
                except Exception as e:  # pragma: no cover
                    print("  (autohint skipped:", e, ")")
                for wf in ("woff2", "woff"):
                    f = TTFont(hinted)
                    f.flavor = wf
                    wp = os.path.join(OUT, "webfonts", f"{FAMILY}-{p.name}.{wf}")
                    f.save(wp)
                    print("wrote", os.path.relpath(wp, ROOT))


if __name__ == "__main__":
    main(sys.argv)
