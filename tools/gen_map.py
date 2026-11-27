#!/usr/bin/env python3
"""Build tools/land.svg from Natural Earth country outlines.

Fresh for news-image-20261126. Reads tools/countries.geo.json
(180 countries, johan/world.geo.json), projects equirectangular
lon -180..180 -> x 0..984, lat 75..-52 -> y 0..144, simplifies each
ring with Douglas-Peucker (~0.45 degrees), drops Antarctica, and
writes one <path> per country polygon ring into tools/land.svg.

Usage: python3 tools/gen_map.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.dirname(HERE)
SRC = os.path.join(HERE, "countries.geo.json")
OUT = os.path.join(HERE, "land.svg")

W, H = 984, 144
LON_MIN, LON_MAX = -180.0, 180.0
LAT_MAX, LAT_MIN = 75.0, -52.0
TOL = 0.45  # degrees, Douglas-Peucker epsilon
SKIP = {"Antarctica"}


def project(lon, lat):
    x = (lon - LON_MIN) / (LON_MAX - LON_MIN) * W
    y = (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * H
    return (x, y)


def _perp_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    seg = dx * dx + dy * dy
    if seg == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / seg))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def simplify(points, tol):
    """Douglas-Peucker on a list of (lon, lat) points."""
    if len(points) <= 2:
        return list(points)
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = points[a]
        bx, by = points[b]
        worst, worst_i = 0.0, -1
        for i in range(a + 1, b):
            d = _perp_dist(points[i][0], points[i][1], ax, ay, bx, by)
            if d > worst:
                worst, worst_i = d, i
        if worst > tol and worst_i > 0:
            keep[worst_i] = True
            stack.append((a, worst_i))
            stack.append((worst_i, b))
    return [p for p, k in zip(points, keep) if k]


def ring_to_path(ring):
    pts = [project(lon, lat) for lon, lat in ring]
    if len(pts) < 3:
        return ""
    d = ["M%.1f,%.1f" % pts[0]]
    d += ["L%.1f,%.1f" % p for p in pts[1:]]
    d.append("Z")
    return " ".join(d)


def main():
    with open(SRC, encoding="utf-8") as f:
        data = json.load(f)
    paths = []
    skipped = 0
    for feat in data["features"]:
        name = (feat.get("properties") or {}).get("name", "")
        if name in SKIP:
            skipped += 1
            continue
        geom = feat["geometry"]
        polys = []
        if geom["type"] == "Polygon":
            polys = [geom["coordinates"]]
        elif geom["type"] == "MultiPolygon":
            polys = geom["coordinates"]
        else:
            continue
        for poly in polys:
            for ring in poly:
                simp = simplify(ring, TOL)
                d = ring_to_path(simp)
                if d:
                    paths.append(
                        '<path d="%s"/>' % d
                    )
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(paths) + "\n")
    print("countries.geo.json features: %d" % len(data["features"]))
    print("skipped (Antarctica): %d" % skipped)
    print("paths written: %d" % len(paths))
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
