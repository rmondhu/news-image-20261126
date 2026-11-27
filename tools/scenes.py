#!/usr/bin/env python3
"""The 13 rich code-drawn vector scenes for news-image-20261126.

Fresh for this edition, drawn from the ILLUSTRATION lines in news.md.
Each scene is one function taking (w, h, num, label, colour) where
num/label are the stat ribbon text and colour is the region colour.
Scenes are built as lists joined with "".join -- never implicit string
concatenation mixed with + in one return.

Recipe per scene: full environment background + 2-4 layered elements
with contrasting scale + one small detail + a stat ribbon INSIDE the
scene (Oswald, big number + short label). Flat 2-4 colour palette,
no gradients. No photos, no AI images, no icons alone.
"""

import math

# ---------------------------------------------------------------- helpers

def _rect(x, y, w, h, fill, op=""):
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"%s/>' % (
        x, y, w, h, fill, op)


def _circ(x, y, r, fill, op=""):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"%s/>' % (
        x, y, r, fill, op)


def _ell(x, y, rx, ry, fill, op=""):
    return '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"%s/>' % (
        x, y, rx, ry, fill, op)


def _poly(points, fill, op=""):
    pts = " ".join("%.1f,%.1f" % p for p in points)
    return '<polygon points="%s" fill="%s"%s/>' % (pts, fill, op)


def _path(d, fill, op=""):
    return '<path d="%s" fill="%s"%s/>' % (d, fill, op)


def _text(x, y, s, size, fill, fam="Libre Franklin", wt="400", anchor="start",
          extra=""):
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-weight="%s" '
            'font-size="%.1f" fill="%s" text-anchor="%s"%s>%s</text>') % (
                x, y, fam, wt, size, fill, anchor, extra, s)


def _cloud(x, y, s, fill="#ffffff"):
    parts = []
    parts.append(_ell(x, y, 14 * s, 6 * s, fill))
    parts.append(_ell(x + 10 * s, y - 4 * s, 10 * s, 6 * s, fill))
    parts.append(_ell(x + 20 * s, y, 12 * s, 5 * s, fill))
    return "".join(parts)


def _bird(x, y, s, fill="#141414"):
    d = "M%.1f,%.1f q%.1f,%.1f %.1f,%.1f q%.1f,%.1f %.1f,%.1f" % (
        x, y, 3 * s, -3 * s, 6 * s, 0, 3 * s, -3 * s, 6 * s, 0)
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%.1f"/>' % (
        d, fill, 1.2 * s)


def _smoke(x, y, s, fill="#8a8a8a"):
    parts = []
    parts.append(_circ(x, y, 5 * s, fill))
    parts.append(_circ(x + 3 * s, y - 7 * s, 6.5 * s, fill))
    parts.append(_circ(x - 2 * s, y - 14 * s, 8 * s, fill))
    parts.append(_circ(x + 2 * s, y - 22 * s, 9 * s, fill))
    return "".join(parts)


def _flame(x, y, s):
    parts = []
    parts.append(_poly([(x, y), (x + 6 * s, y - 12 * s), (x + 12 * s, y)],
                       "#e8641c"))
    parts.append(_poly([(x + 2 * s, y), (x + 6 * s, y - 7 * s),
                        (x + 10 * s, y)], "#f6c453"))
    return "".join(parts)


def _waves(y, w, fill):
    d = "M0,%.1f " % y
    x = 0.0
    while x < w:
        d += "q5,-3.5 10,0 "
        x += 10
    d += "L%.1f,%.1f L0,%.1f Z" % (w, y + 8, y + 8)
    return _path(d, fill)


def _person(x, y, s, shirt, pants, skin="#e8b98a", helmet=None):
    parts = []
    parts.append(_circ(x, y - 13 * s, 3.2 * s, skin))
    if helmet:
        parts.append(_path("M%.1f,%.1f a%.1f,%.1f 0 0 1 %.1f,0 Z" % (
            x - 3.4 * s, y - 13 * s, 3.4 * s, 3.4 * s, 6.8 * s), helmet))
    parts.append(_rect(x - 3 * s, y - 10 * s, 6 * s, 8 * s, shirt))
    parts.append(_rect(x - 3 * s, y - 2 * s, 2.4 * s, 7 * s, pants))
    parts.append(_rect(x + 0.6 * s, y - 2 * s, 2.4 * s, 7 * s, pants))
    return "".join(parts)


def _ribbon(w, h, num, label, colour, big):
    text = num + "  " + label
    fs = big
    est = 7 + len(text) * fs * 0.52
    rw = min(est, w - 10)
    parts = []
    parts.append(_rect(4, h - 21, rw, 17, colour))
    parts.append(_rect(4, h - 21, rw, 2.5, "#ffffff", ' opacity="0.35"'))
    parts.append(_text(9, h - 8.5, text, fs, "#ffffff", "Oswald", "600"))
    return "".join(parts)


def _windows(x, y, cols, rows, cw, ch, gx, gy, fill="#f6c453"):
    parts = []
    for r in range(rows):
        for c in range(cols):
            if (r * cols + c) % 3 != 2:
                parts.append(_rect(x + c * (cw + gx), y + r * (ch + gy),
                                   cw, ch, fill))
    return "".join(parts)


# ---------------------------------------------------------------- 1 KUWAIT
def scene_kuwait(w, h, num, label, colour):
    p = []
    p.append(_rect(0, 0, w, h * 0.62, "#eec27f"))          # dusk sky
    p.append(_circ(w * 0.78, h * 0.20, 11, "#f6e3b8"))      # low sun
    p.append(_cloud(w * 0.12, h * 0.14, 0.8, "#f7e8c8"))
    p.append(_bird(w * 0.42, h * 0.16, 0.9))
    p.append(_rect(0, h * 0.62, w, h * 0.38, "#7fa8b8"))    # gulf water
    p.append(_waves(h * 0.66, w, "#a8c4cc"))
    p.append(_rect(0, h * 0.58, w * 0.62, h * 0.10, "#c9a06a"))  # shore
    # concrete air-defence station + radar dish
    p.append(_rect(w * 0.10, h * 0.52, w * 0.30, h * 0.16, "#b9b3a4"))
    p.append(_rect(w * 0.10, h * 0.48, w * 0.30, h * 0.05, "#8f887a"))
    p.append(_rect(w * 0.22 - 1, h * 0.30, 3, h * 0.18, "#6f6a5e"))
    p.append(_path("M%.1f,%.1f a11,11 0 0 1 22,0 Z" % (
        w * 0.22 - 11, h * 0.30), "#fdfdf8",
        ' stroke="#6f6a5e" stroke-width="1.2"'))
    p.append(_path("M%.1f,%.1f L%.1f,%.1f" % (
        w * 0.22, h * 0.30, w * 0.22 + 8, h * 0.22),
        "none", ' stroke="#6f6a5e" stroke-width="1.2"'))
    p.append(_smoke(w * 0.52, h * 0.50, 0.9))
    # small drone in the pale sky
    p.append(_rect(w * 0.58, h * 0.22, 12, 2.5, "#141414"))
    p.append(_circ(w * 0.58, h * 0.235, 2.2, "#141414"))
    p.append(_circ(w * 0.58 + 12, h * 0.235, 2.2, "#141414"))
    p.append(_rect(w * 0.61, h * 0.26, 5, 4, "#a31621"))
    # technician with helmet, tiny Italian flag patch on it
    p.append(_person(w * 0.68, h * 0.66, 1.0, "#3a5a7a", "#262626",
                     helmet="#e8e4d8"))
    p.append(_rect(w * 0.68 - 1.5, h * 0.66 - 17.5, 3, 2.2, "#009246"))
    p.append(_rect(w * 0.68 + 1.5, h * 0.66 - 17.5, 3, 2.2, "#ce2b37"))
    p.append(_ribbon(w, h, num, label, colour, 13))
    return "".join(p)


# ---------------------------------------------------------------- 2 GAZA
def scene_gaza(w, h, num, label, colour):
    p = []
    p.append(_rect(0, 0, w, h * 0.55, "#f6d9a8"))          # dawn sky
    p.append(_circ(w * 0.16, h * 0.18, 10, "#e8641c"))      # dawn sun
    p.append(_cloud(w * 0.55, h * 0.12, 0.8, "#fdf3d8"))
    p.append(_bird(w * 0.38, h * 0.10, 0.9))
    # apartment blocks along the beach
    p.append(_rect(w * 0.06, h * 0.30, w * 0.16, h * 0.34, "#c9b48a"))
    p.append(_windows(w * 0.08, h * 0.33, 2, 3, 5, 4, 6, 5))
    p.append(_rect(w * 0.26, h * 0.22, w * 0.18, h * 0.42, "#a89a72"))
    p.append(_windows(w * 0.285, h * 0.25, 2, 4, 5, 4, 7, 5, "#f6e3b8"))
    p.append(_rect(w * 0.48, h * 0.34, w * 0.15, h * 0.30, "#c9b48a"))
    p.append(_windows(w * 0.50, h * 0.37, 2, 3, 5, 4, 6, 5))
    # open schoolbook on the rooftop of the tall block
    p.append(_poly([(w * 0.30, h * 0.215), (w * 0.335, h * 0.19),
                    (w * 0.37, h * 0.215), (w * 0.335, h * 0.235)],
                   "#ffffff"))
    p.append(_rect(w * 0.333, h * 0.19, 0.8, h * 0.045, "#a31621"))
    # smoke plume from one building
    p.append(_smoke(w * 0.55, h * 0.34, 1.0))
    # sand + sea + tents
    p.append(_rect(0, h * 0.64, w, h * 0.12, "#e8d5a0"))
    p.append(_rect(0, h * 0.76, w, h * 0.24, "#5e8fa3"))
    p.append(_waves(h * 0.80, w, "#8fb6c4"))
    p.append(_poly([(w * 0.70, h * 0.76), (w * 0.76, h * 0.64),
                    (w * 0.82, h * 0.76)], "#fdf6e0"))
    p.append(_poly([(w * 0.84, h * 0.76), (w * 0.89, h * 0.66),
                    (w * 0.94, h * 0.76)], "#e8e0c0"))
    p.append(_ribbon(w, h, num, label, colour, 13))
    return "".join(p)


# ---------------------------------------------------------------- 3 EBOLA
def scene_ebola(w, h, num, label, colour):
    p = []
    p.append(_rect(0, 0, w, h * 0.50, "#bcd9e8"))          # pale sky
    p.append(_circ(w * 0.82, h * 0.16, 10, "#f6e3b8"))
    p.append(_cloud(w * 0.10, h * 0.12, 0.8))
    # green hills behind
    p.append(_poly([(0, h * 0.50), (w * 0.30, h * 0.30), (w * 0.60, h * 0.50)],
                   "#7fae62"))
    p.append(_poly([(w * 0.45, h * 0.50), (w * 0.75, h * 0.26),
                    (w, h * 0.50)], "#5d8f47"))
    p.append(_rect(0, h * 0.50, w, h * 0.50, "#c9b48a"))   # dry ground
    # white health tent with red cross
    p.append(_poly([(w * 0.30, h * 0.78), (w * 0.30, h * 0.52),
                    (w * 0.52, h * 0.40), (w * 0.74, h * 0.52),
                    (w * 0.74, h * 0.78)], "#fdfdf8"))
    p.append(_rect(w * 0.48, h * 0.62, w * 0.08, h * 0.16, "#8f887a"))
    p.append(_rect(w * 0.505, h * 0.44, 4, 12, "#a31621"))
    p.append(_rect(w * 0.50, h * 0.485, 14, 4, "#a31621"))
    # line of figures in protective suits
    for i, x in enumerate((0.08, 0.15, 0.22)):
        p.append(_person(w * x, h * 0.86, 1.0, "#fdfdf8", "#dce8f0",
                         helmet="#dce8f0"))
    p.append(_person(w * 0.86, h * 0.86, 1.0, "#fdfdf8", "#dce8f0",
                     helmet="#dce8f0"))
    # tiny vaccine cooler box at the tent door
    p.append(_rect(w * 0.585, h * 0.74, 10, 7, "#1f5fa8"))
    p.append(_rect(w * 0.585, h * 0.74, 10, 2.5, "#ffffff"))
    p.append(_rect(w * 0.588, h * 0.755, 3, 3, "#a31621"))
    p.append(_ribbon(w, h, num, label, colour, 13))
    return "".join(p)


# ---------------------------------------------------------------- 4 PYONGYANG
def scene_pyongyang(w, h, num, label, colour):
    p = []
    p.append(_rect(0, 0, w, h, "#8f8f8f"))                # factory hall
    p.append(_rect(0, 0, w, h * 0.08, "#6f6f6f"))
    p.append(_rect(0, h * 0.86, w, h * 0.14, "#5d5d5d"))  # floor
    # rows of silver centrifuges
    for r in range(2):
        for c in range(5):
            x = w * (0.06 + c * 0.135)
            y = h * (0.22 + r * 0.26)
            p.append(_rect(x, y, w * 0.09, h * 0.20, "#d8d8d8"))
            p.append(_rect(x, y, w * 0.09, 3, "#b9b9b9"))
            p.append(_circ(x + w * 0.045, y + h * 0.10, 3, "#8f8f8f"))
    # small red-nosed warhead on a stand, centre right
    p.append(_rect(w * 0.72, h * 0.62, 3, h * 0.16, "#3a3a3a"))
    p.append(_rect(w * 0.68, h * 0.60, w * 0.10, 3, "#3a3a3a"))
    p.append(_poly([(w * 0.73, h * 0.30), (w * 0.765, h * 0.44),
                    (w * 0.695, h * 0.44)], "#c9c9c9"))
    p.append(_poly([(w * 0.73, h * 0.30), (w * 0.745, h * 0.36),
                    (w * 0.715, h * 0.36)], "#a31621"))
    # lone figure in a dark suit
    p.append(_person(w * 0.58, h * 0.80, 1.1, "#262626", "#262626"))
    # tiny red star on the wall
    p.append(_poly([(w * 0.88, h * 0.10), (w * 0.885, h * 0.125),
                    (w * 0.91, h * 0.125), (w * 0.89, h * 0.14),
                    (w * 0.895, h * 0.165), (w * 0.88, h * 0.15),
                    (w * 0.865, h * 0.165), (w * 0.87, h * 0.14),
                    (w * 0.85, h * 0.125), (w * 0.875, h * 0.125)],
                   "#a31621"))
    p.append(_ribbon(w, h, num, label, colour, 11))
    return "".join(p)


# ---------------------------------------------------------------- 5 BRUSSELS
def scene_brussels(w, h, num, label, colour):
    p = []
    p.append(_rect(0, 0, w, h * 0.55, "#bcd9e8"))          # sky
    p.append(_cloud(w * 0.08, h * 0.10, 0.7))
    p.append(_cloud(w * 0.62, h * 0.08, 0.7))
    # blue EU banner behind
    p.append(_rect(w * 0.05, h * 0.14, w * 0.90, h * 0.28, "#1f3a8a"))
    for i in range(12):
        ang = i * 0.5236
        sx = w * 0.50 + 7.5 * math.cos(ang)
        sy = h * 0.28 + 7.5 * math.sin(ang)
        p.append(_circ(sx, sy, 1.1, "#f6c453"))
    # square floor
    p.append(_rect(0, h * 0.55, w, h * 0.45, "#d8c9a0"))
    # round table with 27 small flags
    p.append(_ell(w * 0.50, h * 0.72, w * 0.34, h * 0.10, "#8f2f2f"))
    p.append(_ell(w * 0.50, h * 0.70, w * 0.34, h * 0.10, "#a31621"))
    for i in range(9):
        x = w * (0.20 + i * 0.075)
        p.append(_rect(x, h * 0.60, 1, h * 0.08, "#6f6a5e"))
        p.append(_rect(x, h * 0.60, 7, 5,
                       ["#1f5fa8", "#c0392b", "#1e8a4c", "#f6c453",
                        "#6a4fa3", "#0e7d8c", "#b03a7d", "#c96a1e",
                        "#14264d"][i]))
    # tall stack of euro banknotes
    for i in range(5):
        p.append(_rect(w * 0.78, h * (0.62 - i * 0.035), w * 0.16, h * 0.03,
                       "#7fae62" if i % 2 == 0 else "#5d8f47"))
    p.append(_text(w * 0.86, h * 0.50, "€", 11, "#ffffff", "Libre Franklin",
                   "700", "middle"))
    # tiny clock showing midnight over the table
    p.append(_circ(w * 0.50, h * 0.52, 5, "#fdfdf8"))
    p.append(_rect(w * 0.495, h * 0.52 - 4, 1, 4, "#141414"))
    p.append(_rect(w * 0.50, h * 0.515, 3.5, 1, "#141414"))
    p.append(_ribbon(w, h, num, label, colour, 11))
    return "".join(p)


# ---------------------------------------------------------------- 6 FRANKFURT
def scene_frankfurt(w, h, num, label, colour):
    p = []
    p.append(_rect(0, 0, w, h * 0.60, "#cfe0ea"))          # sky
    p.append(_circ(w * 0.12, h * 0.14, 9, "#f6e3b8"))
    p.append(_cloud(w * 0.55, h * 0.10, 0.7))
    # skyline blocks
    p.append(_rect(w * 0.02, h * 0.42, w * 0.12, h * 0.30, "#8fa3b0"))
    p.append(_rect(w * 0.16, h * 0.50, w * 0.10, h * 0.22, "#7a8fa0"))
    p.append(_rect(w * 0.86, h * 0.46, w * 0.12, h * 0.26, "#8fa3b0"))
    # ECB tower centre
    p.append(_rect(w * 0.40, h * 0.18, w * 0.20, h * 0.54, "#14264d"))
    p.append(_windows(w * 0.42, h * 0.22, 3, 5, 5, 4, 6, 5, "#f6c453"))
    p.append(_rect(w * 0.475, h * 0.62, w * 0.05, h * 0.10, "#d8b45a"))
    # large euro coin rolling toward the tower
    p.append(_circ(w * 0.80, h * 0.66, 13, "#d8b45a"))
    p.append(_circ(w * 0.80, h * 0.66, 10, "#f6c453"))
    p.append(_text(w * 0.80, h * 0.70, "€", 13, "#8a6d1f",
                   "Libre Franklin", "700", "middle"))
    # three small flags: Spain, France, Germany
    for i, cols in enumerate((("#c60b1e", "#ffc400"),
                              ("#0055a4", "#ffffff"),
                              ("#000000", "#dd0000"))):
        x = w * (0.30 + i * 0.045)
        p.append(_rect(x, h * 0.68, 1, h * 0.10, "#6f6a5e"))
        p.append(_rect(x, h * 0.68, 8, 3, cols[0]))
        p.append(_rect(x, h * 0.68 + 3, 8, 3, cols[1]))
    # tiny key handing over at the tower door
    p.append(_circ(w * 0.545, h * 0.70, 2.2, "#d8b45a"))
    p.append(_rect(w * 0.545, h * 0.70, 6, 1.4, "#d8b45a"))
    p.append(_rect(w * 0.549, h * 0.70, 1.2, 3, "#d8b45a"))
    p.append(_rect(w * 0.552, h * 0.70, 1.2, 3, "#d8b45a"))
    p.append(_rect(0, h * 0.72, w, h * 0.28, "#b9b3a4"))   # street
    p.append(_ribbon(w, h, num, label, colour, 11))
    return "".join(p)


# ---------------------------------------------------------------- 7 BANGKOK
def scene_bangkok(w, h, num, label, colour):
    p = []
    p.append(_rect(0, 0, w, h * 0.52, "#e8b98a"))          # hazy sky
    p.append(_circ(w * 0.84, h * 0.14, 9, "#f6e3b8"))
    # skyline behind
    p.append(_rect(w * 0.02, h * 0.40, w * 0.10, h * 0.20, "#a89a72"))
    p.append(_rect(w * 0.88, h * 0.36, w * 0.10, h * 0.24, "#a89a72"))
    # refinery: round tanks + tall distillation tower
    p.append(_rect(0, h * 0.52, w, h * 0.48, "#8f887a"))   # ground
    p.append(_rect(w * 0.06, h * 0.44, w * 0.16, h * 0.22, "#d8d8d8"))
    p.append(_ell(w * 0.14, h * 0.44, w * 0.08, 4, "#b9b9b9"))
    p.append(_rect(w * 0.26, h * 0.48, w * 0.14, h * 0.18, "#c9c9c9"))
    p.append(_ell(w * 0.33, h * 0.48, w * 0.07, 3.5, "#b9b9b9"))
    p.append(_rect(w * 0.48, h * 0.24, w * 0.09, h * 0.42, "#6f6a5e"))
    p.append(_rect(w * 0.48, h * 0.24, w * 0.09, 4, "#3a3a3a"))
    for i in range(4):
        p.append(_rect(w * 0.48, h * (0.30 + i * 0.09), w * 0.09, 2,
                       "#8f887a"))
    # orange flames + black smoke from the tower
    p.append(_flame(w * 0.50, h * 0.26, 1.1))
    p.append(_flame(w * 0.56, h * 0.30, 0.8))
    p.append(_smoke(w * 0.52, h * 0.20, 0.9, "#3a3a3a"))
    # fire crews with hoses
    p.append(_person(w * 0.70, h * 0.78, 1.0, "#c0392b", "#262626",
                     helmet="#f6c453"))
    p.append(_person(w * 0.80, h * 0.78, 1.0, "#c0392b", "#262626",
                     helmet="#f6c453"))
    p.append(_path("M%.1f,%.1f q10,6 22,2" % (w * 0.70, h * 0.74),
                   "none", ' stroke="#1f5fa8" stroke-width="2"'))
    # tiny hard hat on the ground
    p.append(_path("M%.1f,%.1f a5,5 0 0 1 10,0 Z" % (w * 0.60, h * 0.88),
                   "#f6c453"))
    p.append(_ribbon(w, h, num, label, colour, 11))
    return "".join(p)


# ---------------------------------------------------------------- 8 LONDON
def scene_london(w, h, num, label, colour):
    p = []
    p.append(_rect(0, 0, w, h * 0.58, "#bcd9e8"))          # sky
    p.append(_cloud(w * 0.10, h * 0.10, 0.7))
    p.append(_cloud(w * 0.60, h * 0.08, 0.7))
    # rooftops + Thames behind
    p.append(_rect(0, h * 0.58, w, h * 0.10, "#5e8fa3"))
    p.append(_waves(h * 0.60, w, "#8fb6c4"))
    p.append(_rect(0, h * 0.44, w, h * 0.14, "#a89a72"))
    p.append(_rect(w * 0.05, h * 0.40, w * 0.10, 3, "#8f2f2f"))
    p.append(_rect(w * 0.60, h * 0.42, w * 0.12, 3, "#8f2f2f"))
    # departures board with falling arrow
    p.append(_rect(w * 0.30, h * 0.22, w * 0.40, h * 0.24, "#262626"))
    p.append(_text(w * 0.50, h * 0.30, "DEPARTURES", 7, "#f6c453",
                   "Libre Franklin", "700", "middle"))
    p.append(_path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" % (
        w * 0.36, h * 0.36, w * 0.50, h * 0.44, w * 0.64, h * 0.36),
        "none", ' stroke="#e8641c" stroke-width="2.5"'))
    # suitcases stacked by a bus stop
    p.append(_rect(w * 0.08, h * 0.66, 14, 10, "#a31621"))
    p.append(_rect(w * 0.10, h * 0.76, 12, 9, "#1f5fa8"))
    p.append(_rect(w * 0.24, h * 0.70, 10, 8, "#c96a1e"))
    p.append(_rect(w * 0.86, h * 0.60, 2, h * 0.16, "#6f6a5e"))
    p.append(_rect(w * 0.82, h * 0.60, 10, 6, "#d8b45a"))
    # tiny plane taking off over the rooftops
    p.append(_poly([(w * 0.72, h * 0.16), (w * 0.80, h * 0.14),
                    (w * 0.74, h * 0.185)], "#fdfdf8"))
    p.append(_rect(w * 0.70, h * 0.155, 12, 2, "#fdfdf8"))
    p.append(_ribbon(w, h, num, label, colour, 11))
    return "".join(p)


# ---------------------------------------------------------------- 9 ODESA
def scene_odesa(w, h, num, label, colour):
    p = []
    p.append(_rect(0, 0, w, h * 0.55, "#14264d"))          # night sky
    p.append(_circ(w * 0.84, h * 0.14, 7, "#f6e3b8"))      # moon
    for x, y in ((0.10, 0.10), (0.30, 0.06), (0.55, 0.12), (0.68, 0.05)):
        p.append(_circ(w * x, h * y, 1.2, "#ffffff"))
    # missile trail in the sky
    p.append(_path("M%.1f,%.1f q%.1f,%.1f %.1f,%.1f" % (
        w * 0.20, h * 0.30, w * 0.20, -h * 0.12, w * 0.42, -h * 0.16),
        "none", ' stroke="#f6c453" stroke-width="2"'))
    p.append(_circ(w * 0.62, h * 0.14, 3, "#f6c453"))
    # Black Sea
    p.append(_rect(0, h * 0.55, w, h * 0.45, "#1f3a5f"))
    p.append(_waves(h * 0.60, w, "#3a6a8a"))
    p.append(_waves(h * 0.78, w, "#3a6a8a"))
    # two cargo ships with grain silos on deck
    for sx in (0.08, 0.52):
        p.append(_rect(w * sx, h * 0.66, w * 0.30, h * 0.10, "#8f2f2f"))
        p.append(_rect(w * (sx + 0.02), h * 0.58, w * 0.07, h * 0.08,
                       "#d8d8d8"))
        p.append(_rect(w * (sx + 0.11), h * 0.58, w * 0.07, h * 0.08,
                       "#c9c9c9"))
        p.append(_rect(w * (sx + 0.22), h * 0.60, w * 0.06, h * 0.06,
                       "#f6e3b8"))
    # tiny wheat stalk painted on the first ship's funnel
    p.append(_rect(w * 0.115, h * 0.615, 1, 6, "#f6c453"))
    p.append(_ell(w * 0.115, h * 0.61, 2, 1.2, "#f6c453"))
    # lighthouse beam
    p.append(_rect(w * 0.88, h * 0.42, w * 0.05, h * 0.20, "#fdfdf8"))
    p.append(_rect(w * 0.875, h * 0.40, w * 0.06, h * 0.03, "#a31621"))
    p.append(_poly([(w * 0.88, h * 0.44), (w * 0.60, h * 0.38),
                    (w * 0.60, h * 0.50)], "#f6c453",
                   ' opacity="0.45"'))
    p.append(_ribbon(w, h, num, label, colour, 11))
    return "".join(p)


# ---------------------------------------------------------------- 10 KYIV
def scene_kyiv(w, h, num, label, colour):
    p = []
    p.append(_rect(0, 0, w, h, "#c9b48a"))                # office wall
    p.append(_rect(0, h * 0.78, w, h * 0.22, "#8f887a"))   # floor
    # window showing a grey sky
    p.append(_rect(w * 0.68, h * 0.10, w * 0.26, h * 0.40, "#8fa3b0"))
    p.append(_rect(w * 0.805, h * 0.10, 2, h * 0.40, "#fdfdf8"))
    p.append(_rect(w * 0.68, h * 0.28, w * 0.26, 2, "#fdfdf8"))
    p.append(_cloud(w * 0.72, h * 0.18, 0.5, "#e8e8e8"))
    # framed map of Ukraine on the wall
    p.append(_rect(w * 0.06, h * 0.12, w * 0.24, h * 0.26, "#1f5fa8"))
    p.append(_poly([(w * 0.09, h * 0.20), (w * 0.14, h * 0.16),
                    (w * 0.22, h * 0.17), (w * 0.27, h * 0.22),
                    (w * 0.24, h * 0.30), (w * 0.15, h * 0.33),
                    (w * 0.10, h * 0.28)], "#f6c453"))
    # president at a desk with a microphone
    p.append(_rect(w * 0.30, h * 0.60, w * 0.42, h * 0.18, "#5d3a1a"))
    p.append(_rect(w * 0.30, h * 0.60, w * 0.42, 3, "#7a5230"))
    p.append(_person(w * 0.50, h * 0.62, 1.05, "#14264d", "#262626"))
    p.append(_rect(w * 0.56, h * 0.50, 1.5, h * 0.10, "#262626"))
    p.append(_circ(w * 0.56, h * 0.49, 2.6, "#262626"))
    # tiny phone on the desk showing two leaders embracing
    p.append(_rect(w * 0.66, h * 0.55, 8, 12, "#262626"))
    p.append(_rect(w * 0.665, h * 0.555, 7, 11, "#bcd9e8"))
    p.append(_circ(w * 0.685, h * 0.60, 1.8, "#e8b98a"))
    p.append(_circ(w * 0.695, h * 0.60, 1.8, "#c9a06a"))
    p.append(_ribbon(w, h, num, label, colour, 11))
    return "".join(p)


# ---------------------------------------------------------------- 11 NEW YORK
def scene_newyork(w, h, num, label, colour):
    p = []
    p.append(_rect(0, 0, w, h * 0.60, "#7a8fa0"))          # storm sky
    p.append(_cloud(w * 0.08, h * 0.10, 0.9, "#5d6f7d"))
    p.append(_cloud(w * 0.55, h * 0.07, 0.9, "#5d6f7d"))
    for x in (0.15, 0.35, 0.55, 0.75, 0.90):
        p.append(_path("M%.1f,%.1f l-2,7 M%.1f,%.1f l-2,7" % (
            w * x, h * 0.22, w * x + 0.06, h * 0.30),
            "none", ' stroke="#bcd9e8" stroke-width="1.5"'))
    # skyline, one darkened block
    p.append(_rect(w * 0.04, h * 0.34, w * 0.16, h * 0.34, "#3a4a5a"))
    p.append(_rect(w * 0.24, h * 0.26, w * 0.18, h * 0.42, "#2c3a48"))
    p.append(_windows(w * 0.26, h * 0.30, 2, 4, 4, 3, 6, 5, "#3a4a5a"))
    p.append(_rect(w * 0.46, h * 0.40, w * 0.15, h * 0.28, "#3a4a5a"))
    p.append(_rect(w * 0.65, h * 0.30, w * 0.14, h * 0.38, "#2c3a48"))
    # bent trees + flooded street
    p.append(_rect(0, h * 0.68, w, h * 0.32, "#5e8fa3"))
    p.append(_waves(h * 0.72, w, "#8fb6c4"))
    p.append(_path("M%.1f,%.1f q4,-14 12,-16" % (w * 0.10, h * 0.72),
                   "none", ' stroke="#2c5a2c" stroke-width="2.5"'))
    p.append(_circ(w * 0.135, h * 0.54, 6, "#3a7a3a"))
    # grounded plane at an airport
    p.append(_rect(w * 0.58, h * 0.66, w * 0.30, 3, "#8f887a"))
    p.append(_poly([(w * 0.62, h * 0.64), (w * 0.84, h * 0.64),
                    (w * 0.80, h * 0.60), (w * 0.66, h * 0.60)],
                   "#d8d8d8"))
    p.append(_poly([(w * 0.82, h * 0.60), (w * 0.86, h * 0.56),
                    (w * 0.84, h * 0.60)], "#d8d8d8"))
    # tiny turkey on a windowsill
    p.append(_ell(w * 0.30, h * 0.50, 3.5, 2.5, "#8a5a2b"))
    p.append(_circ(w * 0.315, h * 0.475, 1.6, "#8a5a2b"))
    p.append(_ribbon(w, h, num, label, colour, 11))
    return "".join(p)


# ---------------------------------------------------------------- 12 NAYPYIDAW
def scene_naypyidaw(w, h, num, label, colour):
    p = []
    p.append(_rect(0, 0, w, h, "#a89a72"))                # courtroom wall
    p.append(_rect(0, 0, w, h * 0.10, "#8f887a"))
    p.append(_rect(0, h * 0.82, w, h * 0.18, "#6f6a5e"))   # floor
    # tall judge's bench
    p.append(_rect(w * 0.14, h * 0.44, w * 0.72, h * 0.38, "#5d3a1a"))
    p.append(_rect(w * 0.14, h * 0.44, w * 0.72, 4, "#7a5230"))
    p.append(_rect(w * 0.30, h * 0.20, w * 0.40, h * 0.24, "#14264d"))
    p.append(_rect(w * 0.32, h * 0.22, w * 0.36, h * 0.20, "#f6e3b8"))
    # gavel on the bench
    p.append(_rect(w * 0.60, h * 0.40, 2, 8, "#5d3a1a"))
    p.append(_rect(w * 0.565, h * 0.385, 12, 5, "#7a5230"))
    # red REJECTED stamp on a document
    p.append(_rect(w * 0.20, h * 0.50, w * 0.22, h * 0.16, "#fdfdf8"))
    p.append(_rect(w * 0.22, h * 0.53, w * 0.18, 1.5, "#8f8f8f"))
    p.append(_rect(w * 0.22, h * 0.56, w * 0.18, 1.5, "#8f8f8f"))
    p.append(_rect(w * 0.225, h * 0.585, w * 0.17, h * 0.055, "#a31621"))
    p.append(_text(w * 0.31, h * 0.625, "REJECTED", 6.5, "#ffffff",
                   "Libre Franklin", "700", "middle"))
    # small flag of Myanmar
    p.append(_rect(w * 0.78, h * 0.46, 1, h * 0.12, "#6f6a5e"))
    p.append(_rect(w * 0.78, h * 0.46, 12, 4, "#f6c453"))
    p.append(_rect(w * 0.78, h * 0.50, 12, 4, "#1e8a4c"))
    p.append(_rect(w * 0.78, h * 0.54, 12, 4, "#a31621"))
    # tiny paper boat on the bench
    p.append(_poly([(w * 0.44, h * 0.435), (w * 0.47, h * 0.40),
                    (w * 0.50, h * 0.435)], "#fdfdf8"))
    p.append(_ribbon(w, h, num, label, colour, 11))
    return "".join(p)


# ---------------------------------------------------------------- 13 IBIZA
def scene_ibiza(w, h, num, label, colour):
    p = []
    p.append(_rect(0, 0, w, h * 0.42, "#bcd9e8"))          # sky
    p.append(_circ(w * 0.80, h * 0.14, 9, "#f6e3b8"))
    p.append(_cloud(w * 0.10, h * 0.10, 0.8))
    p.append(_bird(w * 0.40, h * 0.10, 0.9))
    p.append(_bird(w * 0.52, h * 0.16, 0.8))
    # Mediterranean, deep blue
    p.append(_rect(0, h * 0.42, w, h * 0.58, "#1f5fa8"))
    p.append(_waves(h * 0.48, w, "#5e8fc4"))
    p.append(_waves(h * 0.72, w, "#5e8fc4"))
    # tanker tipped on its side, red hull showing
    p.append(_poly([(w * 0.14, h * 0.52), (w * 0.52, h * 0.46),
                    (w * 0.58, h * 0.60), (w * 0.20, h * 0.66)],
                   "#8f2f2f"))
    p.append(_poly([(w * 0.14, h * 0.52), (w * 0.52, h * 0.46),
                    (w * 0.50, h * 0.52), (w * 0.16, h * 0.58)],
                   "#262626"))
    p.append(_rect(w * 0.44, h * 0.44, 8, 10, "#d8d8d8"))
    p.append(_smoke(w * 0.48, h * 0.42, 0.6, "#8a8a8a"))
    # small orange rescue boat alongside
    p.append(_poly([(w * 0.66, h * 0.66), (w * 0.86, h * 0.66),
                    (w * 0.82, h * 0.74), (w * 0.70, h * 0.74)],
                   "#e8641c"))
    p.append(_rect(w * 0.72, h * 0.60, w * 0.06, h * 0.06, "#fdfdf8"))
    p.append(_person(w * 0.76, h * 0.66, 0.8, "#f6c453", "#262626"))
    # tiny life ring floating on the water
    p.append(_circ(w * 0.60, h * 0.82, 4.5, "#e8641c"))
    p.append(_circ(w * 0.60, h * 0.82, 2.2, "#1f5fa8"))
    p.append(_ribbon(w, h, num, label, colour, 11))
    return "".join(p)


SCENES = {
    1: scene_kuwait,
    2: scene_gaza,
    3: scene_ebola,
    4: scene_pyongyang,
    5: scene_brussels,
    6: scene_frankfurt,
    7: scene_bangkok,
    8: scene_london,
    9: scene_odesa,
    10: scene_kyiv,
    11: scene_newyork,
    12: scene_naypyidaw,
    13: scene_ibiza,
}
