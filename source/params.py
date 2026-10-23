"""Per-weight design parameters.

All four weights are generated from the same construction code; only these
numbers change.  Units are font units (UPM = 1000).
"""

UPM = 1000


class Params:
    def __init__(self, name, weight_class, V, hratio=0.94):
        self.name = name
        self.weight_class = weight_class
        self.V = float(V)  # lowercase vertical stem
        self.H = round(V * hratio)  # lowercase horizontal stroke
        self.CV = round(V * 1.06)  # cap vertical stem
        self.CH = round(self.H * 1.04)  # cap horizontal stroke
        self.D = round(V * 1.0)  # diagonal stroke (perpendicular)
        self.CD = round(self.CV * 0.99)

        # vertical metrics
        self.xh = round(526 + 0.18 * (V - 86))  # x-height grows a little with weight
        self.cap = 720
        self.asc = 752
        self.desc = -212
        self.os = 11  # lowercase overshoot
        self.cos = 13  # cap overshoot

        # superellipse tension (0.5523 = circle).  Clearly squarer than a
        # circle: the rounds of an industrial grotesque.
        self.ko = 0.588
        self.ki = 0.625

        dv = self.V - 86.0
        self.dv = dv

        # arches and bowls: the outer curve starts slightly outside the stem
        # (flush shoulder, no spur) and the counter cuts into the stem
        # (a high crotch that keeps the joint from getting dark).
        self.joint = -0.42 * V
        self.crotch = 0.42 * V

        # spacing
        self.sb = 67 - 0.12 * dv  # straight sidebearing, lowercase
        self.sbo = self.sb * 0.63 - 0.09 * dv  # round sidebearing
        self.sbd = 8 + 0.01 * V  # diagonal sidebearing
        self.csb = self.sb * 1.2  # caps straight sidebearing
        self.csbo = self.csb * 0.58 - 0.09 * dv

    def w(self, base, per=1.0):
        """Width that grows with the weight: base width at Regular plus
        `per` units for every unit of extra stem."""
        return base + per * self.dv * 0.82


WEIGHTS = [
    Params("Regular", 400, 86, hratio=0.87),
    Params("Medium", 500, 113, hratio=0.85),
    Params("Bold", 700, 148, hratio=0.83),
    Params("Fat", 900, 188, hratio=0.80),
]
