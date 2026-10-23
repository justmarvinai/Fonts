"""Per-weight design parameters.

All four weights are generated from the same construction code; only these
numbers change.  Units are font units (UPM = 1000).
"""

UPM = 1000


class Params:
    def __init__(self, name, weight_class, V, hratio=0.86):
        self.name = name
        self.weight_class = weight_class
        self.V = float(V)  # lowercase vertical stem
        self.H = round(V * hratio)  # lowercase horizontal stroke
        self.CV = round(V * 1.07)  # cap vertical stem
        self.CH = round(self.H * 1.05)  # cap horizontal stroke
        self.D = round(V * 0.97)  # diagonal stroke (perpendicular)
        self.CD = round(self.CV * 0.97)

        # vertical metrics
        self.xh = 520
        self.cap = 700
        self.asc = 745
        self.desc = -215
        self.os = 11  # lowercase overshoot
        self.cos = 13  # cap overshoot

        # superellipse tension (0.5523 = circle).  A touch squarer than a
        # circle gives the solid, modern "geometric grotesk" feel.
        self.ko = 0.575
        self.ki = 0.6

        dv = self.V - 86.0
        self.dv = dv

        # how far the arch / bowl leaves the stem (thin, crisp joints)
        self.joint = 0.28 * V

        # spacing
        self.sb = 44 + 0.25 * V - max(0.0, V - 120) * 0.12  # straight sidebearing, lowercase
        self.sbo = self.sb * 0.62  # round sidebearing
        self.sbd = 6 + 0.04 * V  # diagonal sidebearing
        self.csb = self.sb * 1.22  # caps straight sidebearing
        self.csbo = self.csb * 0.6

    def w(self, base, per=1.0):
        """Width that grows with the weight: base width at Regular plus
        `per` units for every unit of extra stem."""
        return base + per * self.dv


WEIGHTS = [
    Params("Regular", 400, 86, hratio=0.86),
    Params("Medium", 500, 112, hratio=0.84),
    Params("Bold", 700, 146, hratio=0.81),
    Params("Fat", 900, 184, hratio=0.76),
]
