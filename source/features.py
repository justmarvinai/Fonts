"""OpenType features: automatic kerning (outline-profile based) and ss01."""

import string

from geom import I, band, bounds
import accents

STEP = 10
YMIN, YMAX = -260, 1000

PUNCT = ["period", "comma", "quoteright", "quotedblright", "quoteleft", "quotedblleft",
         "quotesingle", "quotedbl", "hyphen", "endash", "quotesinglbase", "quotedblbase", "ellipsis"]

# extra glyphs that share a side with a base letter
LEFT_SIDE_ALIAS = {"AE": "A", "OE": "O", "Oslash": "O", "Dcroat": None, "Eth": None}
RIGHT_SIDE_ALIAS = {"AE": "E", "OE": "E", "Oslash": "O", "Lslash": "L", "Dcroat": "D", "Eth": "D"}


def profiles(path, adv):
    """Left/right ink extremes per horizontal band (None where no ink)."""
    left, right = [], []
    y = YMIN
    b = bounds(path)
    while y < YMAX:
        if b[3] <= y or b[1] >= y + STEP or b[2] <= b[0]:
            left.append(None)
            right.append(None)
        else:
            s = I(path, band(y, y + STEP))
            sb = bounds(s)
            if sb[2] > sb[0]:
                left.append(sb[0])
                right.append(adv - sb[2])  # white to the advance edge
            else:
                left.append(None)
                right.append(None)
        y += STEP
    return left, right


class Kerner:
    def __init__(self, p, glyphs):
        self.p = p
        self.glyphs = glyphs
        self.prof = {}

    def get(self, n):
        if n not in self.prof:
            path, adv = self.glyphs[n]
            self.prof[n] = profiles(path, adv)
        return self.prof[n]

    def measure(self, a, b, cap):
        """Mean (capped) white between a and b over the bands where both
        have ink, plus the minimum gap."""
        ra = self.get(a)[1]
        lb = self.get(b)[0]
        tot, n, mn = 0.0, 0, 1e9
        for x, y in zip(ra, lb):
            if x is None or y is None:
                continue
            g = x + y
            mn = min(mn, g)
            tot += min(g, cap)
            n += 1
        if n == 0:
            return None, None
        return tot / n, mn

    def openness(self, n, side, y0, y1):
        prof = self.get(n)[0 if side == "L" else 1]
        vals = [v for i, v in enumerate(prof) if v is not None and y0 <= YMIN + i * STEP < y1]
        if not vals:
            return 0
        m = min(vals)
        return sum(v - m for v in vals) / len(vals)


def is_cap(n):
    return n[0] in string.ascii_uppercase


def is_lower(n):
    return n[0] in string.ascii_lowercase and n not in PUNCT


def build(p, glyphs, cmap, font):
    lines = ["languagesystem DFLT dflt;", "languagesystem latn dflt;", ""]

    # ---- groups -------------------------------------------------------
    caps = [c for c in string.ascii_uppercase if c in glyphs]
    lows = [c for c in string.ascii_lowercase if c in glyphs] + ["a.ss01", "germandbls"]
    punct = [n for n in PUNCT if n in glyphs]
    bases = caps + lows + punct

    members = {b: [b] for b in bases}
    for name, (cp, base, mark) in accents.COMPOSITES.items():
        if name in glyphs and base in members:
            members[base].append(name)
    members["dotlessi"] = ["dotlessi"]
    for m in list(members["dotlessi"]):
        pass
    # composites built on dotlessi kern like i
    if "i" in members:
        members["i"] += [n for n, (cp, base, mark) in accents.COMPOSITES.items()
                         if base == "dotlessi" and n in glyphs] + ["dotlessi"]
        members.pop("dotlessi")
    left_members = {k: list(v) for k, v in members.items()}   # glyph used on the left of a pair
    right_members = {k: list(v) for k, v in members.items()}  # glyph used on the right of a pair
    for g, b in RIGHT_SIDE_ALIAS.items():
        if g in glyphs and b in left_members:
            left_members[b].append(g)
    for g, b in LEFT_SIDE_ALIAS.items():
        if b and g in glyphs and b in right_members:
            right_members[b].append(g)

    # ---- kerning ------------------------------------------------------
    K = Kerner(p, glyphs)
    C = 3.2 * p.csb + 60
    o_round_cap = K.openness("O", "L", 0, p.cap)
    o_round_low = K.openness("o", "L", 0, p.xh)

    def proxy(n, side):
        if n in punct:
            return n
        if is_cap(n):
            o = K.openness(n, side, 0, p.cap)
            return "O" if 0.55 * o_round_cap <= o < 1.6 * o_round_cap else "H"
        o = K.openness(n, side, 0, p.xh)
        return "o" if 0.55 * o_round_low <= o < 1.6 * o_round_low else "n"

    pairs = {}
    for a in bases:
        for b in bases:
            la, lb = is_lower(a), is_lower(b)
            if la and lb:
                continue  # lowercase spacing is handled by the sidebearings
            if a in punct and b in punct:
                continue
            if la and is_cap(b):
                continue
            pa, pb = proxy(a, "R"), proxy(b, "L")
            m, mn = K.measure(a, b, C)
            r, _ = K.measure(pa, pb, C)
            if m is None or r is None:
                continue
            k = (r - m) * 0.6
            lowpair = la or lb
            clear = (1.3 * p.sb) if lowpair else (1.15 * p.csb)
            if a in punct or b in punct:
                clear = 0.9 * p.sb
            if k < 0:
                k = max(k, -(mn - clear))
                if mn < clear:
                    k = 0
            else:
                k = min(k, 30)
            k = max(k, -220)
            k = int(round(k / 2.0) * 2)
            if abs(k) >= 10:
                pairs[(a, b)] = k

    def cname(side, b):
        return "@K%s_%s" % (side, b.replace(".", "_"))

    used_l = sorted({a for a, _ in pairs})
    used_r = sorted({b for _, b in pairs})
    for b in used_l:
        lines.append("%s = [%s];" % (cname("L", b), " ".join(left_members[b])))
    for b in used_r:
        lines.append("%s = [%s];" % (cname("R", b), " ".join(right_members[b])))
    lines.append("")
    lines.append("feature kern {")
    for (a, b), k in sorted(pairs.items()):
        lines.append("  pos %s %s %d;" % (cname("L", a), cname("R", b), k))
    lines.append("} kern;")
    lines.append("")

    # ---- ss01: single-storey a ---------------------------------------
    subs = [("a", "a.ss01")] + [(n[:-5], n) for n in glyphs if n.endswith(".ss01") and n != "a.ss01"]
    subs = [(a, b) for a, b in subs if a in glyphs and b in glyphs]
    lines.append("feature ss01 {")
    lines.append('  featureNames { name "Single-storey a"; };')
    for a, b in subs:
        lines.append("  sub %s by %s;" % (a, b))
    lines.append("} ss01;")
    lines.append("")
    lines.append("feature salt {")
    for a, b in subs:
        lines.append("  sub %s by %s;" % (a, b))
    lines.append("} salt;")

    fea = "\n".join(lines) + "\n"
    if getattr(p, "dump_fea", None):
        with open(p.dump_fea, "w") as fh:
            fh.write(fea)
    return fea
