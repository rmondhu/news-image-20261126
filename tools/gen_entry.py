#!/usr/bin/env python3
"""Build render.html for news-image-20261126 from the story data below.

Fresh for this edition. Story text is condensed from news.md (same
facts, same VERIFY pills, same stats). Reads tools/land.svg and the
three woff2 fonts (embedded base64, no network at render time),
draws the 13 scenes via tools/scenes.py, places numbered map badges
with a greedy >=15px collision check, and writes render.html.

Usage: python3 tools/gen_entry.py
"""
import base64
import html
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from scenes import SCENES  # noqa: E402

# ------------------------------------------------------------------ tokens
PAPER = "#f7f1de"
INK = "#141414"
BODY = "#262626"
ACCENT = "#a31621"
NAVY = "#14264d"
GOLD = "#d8b45a"
CARD = "#fffdf4"
FRAME = "#d8cfb0"
MUTED = "#5c5540"
LAND = "#c9bd93"
MAPBG = "#ece5cb"

REGION = {
    "Middle East": "#c96a1e",
    "Europe": "#1f5fa8",
    "Africa": "#c0392b",
    "Asia": "#1e8a4c",
    "N. America": "#6a4fa3",
    "S. America": "#b03a7d",
    "Oceania": "#0e7d8c",
    "World & Space": "#14264d",
}

PILL = {
    "OFFICIAL": "#1e7a46",
    "CONFIRMED": "#1f5fa8",
    "REPORTED": "#a31621",
    "CLAIM": "#b7791f",
}

# Section heights (px) inside the 1024x1024 page; tuned by measure.mjs.
LEAD_H = 178
LEAD_SCENE_H = 82
FEAT_H = 148
FEAT_SCENE_H = 60

# ------------------------------------------------------------------ stories
# n, city, headline, body, stat_num, stat_label, verify, source, region,
# lat, lon. Leads + features carry a scene; briefs carry a one-line body.
LEADS = [
    dict(n=1, city="KUWAIT", headline="Iranian drones kill two Italians at Kuwait air defence station",
         body="Italy and Kuwait blame Iran for the strike; Tehran denies any role in the attack.",
         num="2", label="KILLED", verify="CLAIM", source="REUTERS",
         region="Middle East", lat=29.3759, lon=47.9774),
    dict(n=2, city="GAZA", headline="Israeli strikes kill nine in Gaza overnight",
         body="Deputy education minister Khaled Abu Nada and his wife die in Deir al-Balah; third night of strikes.",
         num="9", label="KILLED OVERNIGHT", verify="CONFIRMED", source="REUTERS",
         region="Middle East", lat=31.4185, lon=34.3519),
    dict(n=3, city="EBOLA", headline="Ebola outbreak in DR Congo passes 12,000 cases",
         body="Nearly half of confirmed cases have died as fighting in Ituri disrupts the response.",
         num="12,021", label="CASES", verify="OFFICIAL", source="REUTERS",
         region="Africa", lat=1.5706, lon=30.2510),
]

FEATURES = [
    dict(n=4, city="PYONGYANG", headline="Kim orders nuclear weapons deployed across more domains",
         body="Kim tours nuclear sites, vows more output; Seoul counts 80–120 warheads.",
         num="80–120", label="WARHEADS", verify="REPORTED", source="REUTERS",
         region="Asia", lat=39.0392, lon=125.7625),
    dict(n=5, city="BRUSSELS", headline="EU leaders split over €1.58tn budget and €45bn Ukraine loan",
         body="Summit opens divided; a deal is aimed for December, before 2027 elections.",
         num="€45bn", label="UKRAINE LOAN", verify="CONFIRMED", source="AP",
         region="Europe", lat=50.8503, lon=4.3517),
    dict(n=6, city="FRANKFURT", headline="Spain's Hernández de Cos picked as next ECB president",
         body="First Spaniard to run the bank; takes over from Lagarde on 7 February 2027.",
         num="5th", label="ECB PRESIDENT", verify="CONFIRMED", source="AP",
         region="Europe", lat=50.1109, lon=8.6821),
    dict(n=7, city="BANGKOK", headline="Explosion and fire at Bangkok refinery injures nine",
         body="Three critically hurt; fire halts all output at the 120,000-barrel-a-day plant.",
         num="9", label="INJURED", verify="CONFIRMED", source="AP",
         region="Asia", lat=13.7563, lon=100.5018),
    dict(n=8, city="LONDON", headline="UK net migration falls to 77,000, lowest since 1997",
         body="Down 62% on the year before and 90% below the 2023 peak, ONS figures show.",
         num="77,000", label="NET MIGRATION", verify="OFFICIAL", source="REUTERS",
         region="Europe", lat=51.5074, lon=-0.1278),
    dict(n=9, city="ODESA", headline="Russia hits two foreign grain ships near Odesa",
         body="Ships carried 100,000+ tonnes of grain, Ukraine's prime minister says.",
         num="100,000+", label="TONNES GRAIN", verify="REPORTED", source="REUTERS",
         region="Europe", lat=46.4825, lon=30.7233),
    dict(n=10, city="KYIV", headline="Zelensky: 'strange' Trump calls Putin 'my friend'",
         body="US 'too focused on the Middle East', Kyiv says; Trump tells Putin to pull back.",
         num="70%", label="DRONES DOWNED", verify="OFFICIAL", source="BBC",
         region="Europe", lat=50.4501, lon=30.5234),
    dict(n=11, city="NEW YORK", headline="Thanksgiving nor'easter lashes US East Coast",
         body="400+ flights cancelled, 1,700 delayed; 850,000 homes lose power.",
         num="850,000", label="NO POWER", verify="CONFIRMED", source="REUTERS",
         region="N. America", lat=40.7128, lon=-74.0060),
    dict(n=12, city="NAYPYIDAW", headline="Myanmar leader rejects ICJ genocide orders",
         body="First comments since the verdict: his government will not fully comply.",
         num="~10,000", label="KILLED, ICJ FOUND", verify="REPORTED", source="REUTERS",
         region="Asia", lat=19.7633, lon=96.0785),
    dict(n=13, city="IBIZA", headline="Diesel tanker capsizes off Ibiza, one crew dead",
         body="Spain activates a pollution plan for up to 7,000 tonnes of diesel aboard.",
         num="7,000t", label="DIESEL ABOARD", verify="CONFIRMED", source="REUTERS",
         region="Europe", lat=38.9806, lon=1.4333),
]

BRIEFS = [
    (14, "WASHINGTON", "Trump demands GDP data probe.", "4.3%", "REUTERS", "N. America", 38.9072, -77.0369),
    (15, "BELGRADE", "Serbia sets early presidential vote.", "27 DEC", "AP", "Europe", 44.7866, 20.4489),
    (16, "BISSAU", "Junta delays elections to Nov 2028.", "~2 YRS", "REUTERS", "Africa", 11.8636, -15.5977),
    (17, "KRASNODAR", "Drone attack hits refinery unit.", "1 UNIT", "REUTERS", "Europe", 45.2561, 38.1247),
    (18, "SANAA", "Saudi airstrikes hit Houthi-held Yemen.", "OVERNIGHT", "AP", "Middle East", 15.3694, 44.1910),
    (19, "CAIRO", "Driver held over crash that killed 31.", "31 KILLED", "AP", "Africa", 30.0444, 31.2357),
    (20, "BOGOR", "13 dead, 13 trapped in gold mine.", "13 DEAD", "REUTERS", "Asia", -6.5971, 106.8060),
    (21, "LONDON", "Britain publishes new UK-EU treaties.", "10-YR", "BBC", "Europe", 51.5074, -0.1278),
    (22, "PARIS", "Depardieu to stand trial for 2018 rape.", "1 TRIAL", "BBC", "Europe", 48.8566, 2.3522),
    (23, "CAMBRIDGE", "Man guilty of 14 attempted murders.", "14", "REUTERS", "Europe", 52.2053, 0.1218),
    (24, "LONDON", "Mandelson kept firm shares as envoy.", "MONTHS", "BBC", "Europe", 51.5074, -0.1278),
    (25, "DETROIT", "Bears stun Lions 39-35, late TD.", "39-35", "SPORTRADAR", "N. America", 42.3314, -83.0458),
    (26, "VIGO", "Ten-man Bournemouth beat Celta 2-1.", "5/5", "REUTERS", "Europe", 42.2406, -8.7207),
    (27, "SEOUL", "South Korea raises base rate to 3.25%.", "3.25%", "REUTERS", "Asia", 37.5665, 126.9780),
    (28, "BRASÍLIA", "Brazil inflation eases to 4.64%.", "4.64%", "REUTERS", "S. America", -15.7939, -47.8828),
    (29, "NAIROBI", "Ebola centre ruled unconstitutional.", "1 RULING", "AP", "Africa", -1.2921, 36.8219),
    (30, "IRBIL", "Thousands protest Baghdad oil seizure.", "1,000S", "AP", "Middle East", 36.1911, 44.0094),
    (31, "KINSHASA", "DR Congo recalls Uganda envoy.", "1 RECALLED", "BBC", "Africa", -4.4419, 15.2663),
    (32, "CORRENS", "Jolie and Pitt settle Miraval battle.", "1 SETTLED", "BBC", "Europe", 43.4861, 6.0797),
]

ALSO = [
    ("MARKETS", "Brent $96.57 (+2.1%) on Middle East supply fears; US markets closed for Thanksgiving."),
    ("TARIFFS", "Brazil calls new US tariffs “unacceptable”; China calls “overcapacity” a false issue."),
]

DATE_CHECK = ("DATE CHECK — DELIBERATELY LEFT OUT (WRONG DATE): Macy’s parade postponement, "
              "FedEx Miami overrun, Trump tariff proposals, Houthi port strikes, Hormuz mine claim, "
              "Netanyahu trial vote, Cartagena rescue, Canary arrivals, Shenzhou-24 docking, "
              "Poundland collapse, Poland no-fly plan, Rams–Packers game, Cairo tanker fire — "
              "all 25 Nov. Trump–Putin photo 22 Nov; Myanmar ICJ ruling last week.")

SOURCES = ("SOURCES: REUTERS · AP · BBC · CNN · AFP · THE GUARDIAN · WSJ · ONS · KCNA VIA REUTERS · "
           "UN NEWS · UEFA · SPORTRADAR · FLIGHTAWARE VIA REUTERS")

LEGEND = ("PICTURES AND MAP DRAWN IN CODE, NOT PHOTOS — OFFICIAL = ON THE RECORD · "
          "CONFIRMED = 2+ OUTLETS · REPORTED = ONE OUTLET · CLAIM = ONE SIDE’S WORD")


def esc(s):
    return html.escape(s, quote=False)


# ------------------------------------------------------------------ map
MAP_W, MAP_H = 984, 144


def proj(lat, lon):
    x = (lon + 180.0) / 360.0 * MAP_W
    y = (75.0 - lat) / 127.0 * MAP_H
    return (x, y)


def all_stories():
    out = []
    for s in LEADS + FEATURES:
        out.append((s["n"], s["region"], s["lat"], s["lon"]))
    for (n, _c, _h, _st, _s, reg, lat, lon) in BRIEFS:
        out.append((n, reg, lat, lon))
    return sorted(out)


def place_badges():
    """Greedy badge placement: every badge centre >= 15px from every other."""
    cands = [(9, -13), (9, 3), (-24, -13), (-24, 3), (9, -24), (-24, -24),
             (16, 6), (-30, 6), (0, -22), (0, 12), (16, -13), (-30, -13),
             (9, 12), (-24, 12), (20, -22), (-34, -22), (20, 12),
             (-34, 12), (0, -32), (0, 22), (28, 0), (-40, 0), (28, -24),
             (-40, -24)]
    placed = []  # (cx, cy, bw, bh)
    spots = {}
    for (n, reg, lat, lon) in all_stories():
        x, y = proj(lat, lon)
        bw = 17 if n >= 10 else 13
        bh = 11
        best = None
        best_score = -1.0
        for (dx, dy) in cands:
            bx = max(1.0, min(MAP_W - bw - 1.0, x + dx))
            by = max(1.0, min(MAP_H - bh - 1.0, y + dy))
            cx, cy = bx + bw / 2.0, by + bh / 2.0
            ok = True
            mind = 999.0
            for (px, py, pw, ph) in placed:
                d = math.hypot(cx - px, cy - py)
                mind = min(mind, d)
                if d < 15.0:
                    ok = False
                if (abs(cx - px) < (bw + pw) / 2.0
                        and abs(cy - py) < (bh + ph) / 2.0):
                    ok = False
            if ok:
                best = (bx, by)
                break
            if mind > best_score:
                best_score = mind
                best = (bx, by)
        bx, by = best
        spots[n] = (x, y, bx, by, bw, bh, reg)
        placed.append((bx + bw / 2.0, by + bh / 2.0, bw, bh))
    mind_all = 999.0
    for i in range(len(placed)):
        for j in range(i + 1, len(placed)):
            d = math.hypot(placed[i][0] - placed[j][0],
                           placed[i][1] - placed[j][1])
            mind_all = min(mind_all, d)
    return spots, mind_all


LABELS = [
    ("N. AMERICA", 78, 52),
    ("S. AMERICA", 258, 112),
    ("ATLANTIC", 330, 78),
    ("EUROPE", 548, 12),
    ("AFRICA", 512, 100),
    ("MIDDLE EAST", 628, 82),
    ("ASIA", 742, 28),
    ("OCEANIA", 868, 118),
]


def build_map_svg():
    with open(os.path.join(HERE, "land.svg"), encoding="utf-8") as f:
        land = f.read()
    spots, mind = place_badges()
    parts = []
    parts.append('<svg id="map" width="984" height="144" viewBox="0 0 984 144" '
                 'xmlns="http://www.w3.org/2000/svg">')
    parts.append('<rect x="0" y="0" width="984" height="144" fill="%s"/>' % MAPBG)
    parts.append('<g fill="%s" stroke="%s" stroke-width="0.4">%s</g>' % (
        LAND, PAPER, land))
    for (text, lx, ly) in LABELS:
        parts.append('<text x="%d" y="%d" font-family="Libre Franklin" '
                     'font-weight="700" font-size="8" letter-spacing="1.5" '
                     'fill="%s">%s</text>' % (lx, ly, MUTED, text))
    for n in sorted(spots):
        x, y, bx, by, bw, bh, reg = spots[n]
        col = REGION[reg]
        parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                     'stroke="%s" stroke-width="0.8"/>' % (
                         x, y, bx + bw / 2.0, by + bh / 2.0, col))
        parts.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s" '
                     'stroke="#ffffff" stroke-width="0.8"/>' % (x, y, col))
        parts.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" '
                     'fill="%s"/>' % (bx, by, bw, bh, col))
        parts.append('<text x="%.1f" y="%.1f" font-family="Libre Franklin" '
                     'font-weight="700" font-size="8" fill="#ffffff" '
                     'text-anchor="middle">%d</text>' % (
                         bx + bw / 2.0, by + 8.5, n))
    parts.append("</svg>")
    return "".join(parts), mind


# ------------------------------------------------------------------ html
def font_face(name, weight, path):
    with open(os.path.join(ENTRY, path), "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return ("@font-face{font-family:'%s';font-style:normal;font-weight:%s;"
            "font-display:swap;src:url(data:font/woff2;base64,%s) "
            "format('woff2');}") % (name, weight, b64)


def card_html(s, kind):
    col = REGION[s["region"]]
    scene_w = 322 if kind == "lead" else 190
    scene_h = LEAD_SCENE_H if kind == "lead" else FEAT_SCENE_H
    scene = SCENES[s["n"]](scene_w, scene_h, s["num"], s["label"], col)
    cls = "card lead" if kind == "lead" else "card feat"
    h2 = "h2l" if kind == "lead" else "h2f"
    parts = []
    parts.append('<div class="%s">' % cls)
    parts.append('<svg class="scene" width="%d" height="%d" '
                 'viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">%s</svg>'
                 % (scene_w, scene_h, scene_w, scene_h, scene))
    parts.append('<div class="chead">')
    parts.append('<div class="k" style="color:%s">%d · %s · %s</div>' % (
        col, s["n"], esc(s["city"]), esc(s["region"]).upper()))
    parts.append('<div class="%s">%s</div>' % (h2, esc(s["headline"])))
    parts.append('<p>%s</p>' % esc(s["body"]))
    parts.append('<div class="meta"><span class="pill" style="background:%s">'
                 '%s</span><span class="src">%s</span></div>' % (
                     PILL[s["verify"]], s["verify"], esc(s["source"])))
    parts.append("</div></div>")
    return "".join(parts)


def region_counts():
    counts = {}
    for s in LEADS + FEATURES:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    for (_n, _c, _h, _st, _s, reg, _la, _lo) in BRIEFS:
        counts[reg] = counts.get(reg, 0) + 1
    order = ["Middle East", "Europe", "Africa", "Asia", "N. America",
             "S. America"]
    return [(r, counts.get(r, 0)) for r in order]


def build_html():
    css = []
    css.append(font_face("Playfair Display", "700 900",
                         "fonts/PlayfairDisplay-700.woff2"))
    css.append(font_face("Libre Franklin", "400 700",
                         "fonts/LibreFranklin-400.woff2"))
    css.append(font_face("Oswald", "500 700", "fonts/Oswald-600.woff2"))
    css.append("""
*{box-sizing:border-box;margin:0;padding:0}
body{background:#f7f1de}
.page{width:1024px;height:1024px;margin:0 auto;padding:0 20px 8px;
background:#f7f1de;font-family:'Libre Franklin',sans-serif;color:#141414;
overflow:hidden}
header{margin:0 -20px;background:#14264d;color:#fff;text-align:center;
padding:5px 20px 4px;border-bottom:3px solid #d8b45a}
.kicker{font-size:8.5px;letter-spacing:4px;color:#d8b45a;font-weight:700}
h1{font-family:'Playfair Display',serif;font-weight:900;font-size:42px;
line-height:1.02;letter-spacing:1px}
.dateline{font-size:10px;letter-spacing:2.5px;color:#e8e0c0;margin-top:1px}
.strip{margin:0 -20px;background:#a31621;color:#fff;display:flex;
padding:4px 20px;font-family:'Playfair Display',serif;font-weight:700;
font-size:11px;line-height:1.25}
.strip div{flex:1;min-width:0;text-align:center;padding:0 8px}
.strip div+div{border-left:1px solid rgba(255,255,255,.45)}
.chips{display:flex;gap:6px;justify-content:center;padding:3px 0}
.chip{border:1px solid #d8cfb0;background:#fffdf4;border-radius:20px;
padding:2px 9px;font-size:9.5px;font-weight:700;white-space:nowrap}
.chip i{display:inline-block;width:8px;height:8px;border-radius:50%%;
margin-right:5px}
.leads{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:4px}
.leads>div,.feats>div{min-width:0}
.card{background:#fffdf4;border:1px solid #d8cfb0;overflow:hidden}
.card.lead{height:%dpx}
.card.feat{height:%dpx}
svg.scene{display:block;width:100%%}
.chead{padding:3px 7px 4px}
.k{font-size:8.5px;font-weight:700;letter-spacing:1.2px}
.h2l{font-family:'Playfair Display',serif;font-weight:900;font-size:14.5px;
line-height:1.15;margin:1px 0}
.lead p{font-size:10px;line-height:1.25;color:#262626}
.h2f{font-family:'Playfair Display',serif;font-weight:900;font-size:11.5px;
line-height:1.15;margin:2px 0}
.feat p{font-size:9px;line-height:1.25;color:#262626}
.meta{display:flex;justify-content:space-between;align-items:center;
margin-top:2px}
.pill{font-size:8px;font-weight:700;color:#fff;padding:1.5px 6px;
border-radius:2px;letter-spacing:.5px}
.src{font-size:8px;color:#5c5540;letter-spacing:.5px;font-weight:700}
.seclabel{font-size:10px;font-weight:700;letter-spacing:2px;
padding:3px 0 2px;border-bottom:2px solid #14264d;margin:4px 0 3px;
display:flex;justify-content:space-between}
.seclabel span:last-child{letter-spacing:1px;color:#5c5540}
.feats{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}
.mapsec{border:1px solid #d8cfb0;background:#fffdf4;margin-top:4px;
padding:2px 0 0}
.maptitle{font-size:10px;font-weight:700;letter-spacing:2px;padding:0 8px 2px}
.mapsec svg{display:block;margin:0 auto}
.briefcols{display:grid;grid-template-columns:1fr 1fr 1fr;gap:0 10px}
.briefcols>div{min-width:0}
.brief{font-size:9.5px;line-height:14px;white-space:nowrap;overflow:hidden;
padding:0}
.bn{font-weight:700}
.bs{font-size:8px;color:#5c5540;font-weight:700;white-space:nowrap}
.also{border-top:1px solid #d8cfb0;margin-top:3px;padding-top:2px}
.also div{font-size:10px;line-height:13px;white-space:nowrap;overflow:hidden}
.also b{color:#a31621}
footer{margin:0 -20px}
.datecheck{background:#a31621;color:#fff;padding:3px 20px;font-size:9px;
line-height:1.3}
.datecheck b{letter-spacing:1px}
.sources{background:#14264d;color:#fff;padding:3px 20px 4px;font-size:8.5px;
line-height:1.35;text-align:center}
.sources b{color:#d8b45a}
""" % (LEAD_H, FEAT_H))

    h = []
    h.append("<!DOCTYPE html><html><head><meta charset='utf-8'>")
    h.append("<style>%s</style></head><body><div class='page'>" % "".join(css))
    h.append("<header><div class='kicker'>THE WORLD IN ONE PAGE</div>"
             "<h1>THE WORLD TODAY</h1>"
             "<div class='dateline'>THURSDAY 26 NOVEMBER 2026 &bull; "
             "32 STORIES &bull; 6 CONTINENTS</div></header>")
    h.append("<div class='strip'>")
    for s in LEADS:
        short = {"KUWAIT": "KUWAIT — Iranian drones kill two Italians",
                 "GAZA": "GAZA — Israeli strikes kill nine overnight",
                 "EBOLA": "EBOLA — DR Congo passes 12,000 cases"}[s["city"]]
        h.append("<div>%s</div>" % esc(short))
    h.append("</div>")
    h.append("<div class='chips'>")
    for (reg, cnt) in region_counts():
        h.append('<span class="chip"><i style="background:%s"></i>%s %d'
                 "</span>" % (REGION[reg], esc(reg).upper(), cnt))
    h.append("</div>")
    h.append("<div class='leads'>")
    for s in LEADS:
        h.append(card_html(s, "lead"))
    h.append("</div>")
    h.append("<div class='seclabel'><span>THE DAY IN 10 MORE</span>"
             "<span>STORIES 4–13</span></div>")
    h.append("<div class='feats'>")
    for s in FEATURES:
        h.append(card_html(s, "feat"))
    h.append("</div>")
    map_svg, mind = build_map_svg()
    h.append("<div class='mapsec'><div class='maptitle'>WHERE IT HAPPENED "
             "&mdash; SCENES 1&ndash;13</div>%s</div>" % map_svg)
    h.append("<div class='seclabel'><span>THE REST OF THE DAY</span>"
             "<span>STORIES 14–32</span></div>")
    cols = [[], [], []]
    for i, b in enumerate(BRIEFS):
        cols[i * 3 // len(BRIEFS)].append(b)
    h.append("<div class='briefcols'>")
    for col in cols:
        h.append("<div>")
        for (n, city, text, stat, src, _reg, _la, _lo) in col:
            h.append('<div class="brief"><span class="bn">%d.</span> '
                     '<b>%s</b> &mdash; %s <span class="bs">%s &middot; %s'
                     "</span></div>" % (
                         n, esc(city), esc(text), esc(stat), esc(src)))
        h.append("</div>")
    h.append("</div>")
    h.append("<div class='also'>")
    for (tag, text) in ALSO:
        h.append('<div><b>%s</b> &mdash; %s</div>' % (tag, esc(text)))
    h.append("</div>")
    h.append("<footer><div class='datecheck'><b>DATE CHECK</b> &mdash; %s"
             "</div>" % esc(DATE_CHECK[len("DATE CHECK — DELIBERATELY LEFT OUT (WRONG DATE): "):]))
    h.append("<div class='sources'>%s<br>%s</div></footer>" % (
        esc(SOURCES), esc(LEGEND)))
    h.append("</div></body></html>")
    return "".join(h), mind


def main():
    out_html, mind = build_html()
    out = os.path.join(ENTRY, "render.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(out_html)
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))
    print("min badge centre distance: %.1f px (need >= 15)" % mind)
    print("region counts: %s" % (region_counts(),))
    print("total stories: %d" % (len(LEADS) + len(FEATURES) + len(BRIEFS),))


if __name__ == "__main__":
    main()
