# Design system — THE WORLD TODAY, 26 November 2026

Same winner system as the 25 November edition (which scored 12/12 in
dev): same tokens, same 8px rhythm, same layout. Only the content and
the 13 scenes are new.

## Palette
| Token | Value | Used for |
|---|---|---|
| `--navy` | #14264d | header band, footer strip, World & Space |
| `--gold` | #d8b45a | header kicker, masthead underline |
| `--accent` | #a31621 | red headline strip, DATE CHECK box, REPORTED pill |
| `--paper` | #f7f1de | page background |
| `--ink` / `--body` | #141414 / #262626 | headlines / body text |
| `--muted` | #5c5540 | map labels, sources |
| `--card` | #fffdf4 | card background |
| `--frame` | #d8cfb0 | card borders, map panel border |
| `--land` | #c9bd93 | map land |
| `--mapbg` | #ece5cb | map sea |

**Region colours (chips, stat ribbons, map dots/badges):**
| Region | Colour | Stories |
|---|---|---|
| Middle East | #c96a1e orange | 4 |
| Europe | #1f5fa8 blue | 14 |
| Africa | #c0392b red | 5 |
| Asia | #1e8a4c green | 5 |
| N. America | #6a4fa3 purple | 3 |
| S. America | #b03a7d magenta | 1 |
| Oceania | #0e7d8c teal | 0 |
| World & Space | #14264d navy | 0 |

## Typography — three fonts, three jobs
| Font | Job | Sizes |
|---|---|---|
| Playfair Display 900 | masthead (42px), lead headlines (14.5px), feature headlines (11.5px) | classic black serif |
| Libre Franklin | labels, body, kicker, footer | clean grotesque |
| Oswald 600 | numbers and labels in stat ribbons | 13px lead / 11px feature, condensed |

All three are Google Fonts (SIL OFL 1.1, free for commercial use),
downloaded fresh as variable woff2 latin into `fonts/` —
`PlayfairDisplay-700.woff2` (38,404 bytes),
`LibreFranklin-400.woff2` (30,892 bytes),
`Oswald-600.woff2` (21,472 bytes). Loaded via `@font-face` with
weight ranges (`700 900` / `400 700` / `500 700`), embedded base64 in
`render.html`. No network at render time.

## Frame & layout
- **Navy header band, full-bleed, gold kicker + gold underline:**
  masthead "THE WORLD TODAY" white Playfair 900 42px; dateline
  "THURSDAY 26 NOVEMBER 2026 • 32 STORIES • 6 CONTINENTS".
- **Red headline strip** below the header: the 3 lead headlines,
  shortened with a city prefix so each fits one line.
- **Region chips** with story counts per region.
- **Every story in a framed box:** 1px `--frame` border on a `--card`
  background — 3 lead cards + 10 feature cards (grid 5×2, label
  "THE DAY IN 10 MORE") + 19 numbered briefs (3 columns) + 2 ALSO
  TODAY items.
- **Stat ribbon in colour inside every scene** (Oswald + short
  label): "2 KILLED", "9 KILLED OVERNIGHT", "12,021 CASES", "80–120
  WARHEADS", "€45bn UKRAINE LOAN", "5th ECB PRESIDENT", "9 INJURED",
  "77,000 NET MIGRATION", "100,000+ TONNES GRAIN", "70% DRONES
  DOWNED", "850,000 NO POWER", "~10,000 KILLED, ICJ FOUND",
  "7,000t DIESEL ABOARD".
- **Verification pill on every card:** OFFICIAL green `#1e7a46`,
  CONFIRMED blue `#1f5fa8`, REPORTED red `#a31621`, CLAIM amber
  `#b7791f` — set honestly from each story's sources (OFFICIAL = on
  the record; CONFIRMED = 2+ outlets; REPORTED = one outlet; CLAIM =
  one side's word only). Definitions in the footer. Kuwait is CLAIM:
  the deaths are confirmed, but the attribution to Iran is one side's
  word and Tehran denies it.
- **Footer, two contrasting bands:** red DATE CHECK box (white text,
  naming the stories deliberately left out for being off-date) above
  a navy sources strip (white text); footer notes "PICTURES AND MAP
  DRAWN IN CODE, NOT PHOTOS".
- Headlines and bodies are sized to fit their cards without clipping;
  briefs are single-line, `white-space:nowrap`, with a one-token
  source.

## Illustrations — 13 rich scenes, drawn in code
Recipe per scene (same as the 25 November edition): full environment
background + 2–4 layered elements with contrasting scale + one small
detail + stat ribbon inside the scene. Flat 2–4 colour palette, no
gradients. Implementation: `tools/scenes.py` — one function per scene
plus helpers (`_cloud`, `_bird`, `_smoke`, `_flame`, `_waves`,
`_person`, `_ribbon`, `_windows`). Scenes are built as lists joined
with `"".join` — never implicit string concatenation mixed with `+`.

Scene list (back → front):
- 1 KUWAIT: dusk sky + sun/cloud/bird → Gulf water + waves → shore +
  concrete station + radar dish (white half-disc, dark outline) →
  grey smoke + small drone → technician with helmet, tiny Italian
  flag patch on it.
- 2 GAZA: dawn sky + sun/cloud/bird → apartment blocks + lit windows
  → grey smoke from one building → sand + sea + tents → open
  schoolbook on a rooftop.
- 3 EBOLA: pale sky + sun/cloud → green hills → dry ground → white
  health tent with red cross + door → figures in protective suits →
  tiny vaccine cooler box at the tent door.
- 4 PYONGYANG: grey factory hall → two rows of silver centrifuges →
  small red-nosed warhead on a stand → lone figure in a dark suit →
  tiny red star on the wall.
- 5 BRUSSELS: sky + clouds → blue EU banner with a ring of 12 gold
  stars → square floor → round table with 9 small flags → stack of
  euro banknotes with € → tiny clock showing midnight over the table.
- 6 FRANKFURT: sky + sun/cloud → skyline blocks → navy ECB tower with
  gold windows → large gold euro coin rolling toward it → three small
  flags (Spain, France, Germany) → tiny key at the tower door.
- 7 BANGKOK: hazy sky + sun → skyline → refinery tanks + tall
  distillation tower → orange flames + black smoke → fire crews with
  a hose → tiny hard hat on the ground.
- 8 LONDON: sky + clouds → rooftops + Thames + waves → departures
  board with a red falling arrow → suitcases by a bus stop → tiny
  plane taking off over the rooftops.
- 9 ODESA: night sky + moon/stars → missile trail → Black Sea + waves
  → two cargo ships with grain silos → lighthouse beam → tiny wheat
  stalk on a funnel.
- 10 KYIV: office wall + floor → window with grey sky → framed map of
  Ukraine → president at a desk with a microphone → tiny phone
  showing two leaders embracing.
- 11 NEW YORK: storm sky + clouds + rain → skyline, one darkened
  block → bent tree + flooded street → grounded plane → tiny turkey
  on a windowsill.
- 12 NAYPYIDAW: courtroom wall → judge's bench + blue panel → gavel →
  document with a red REJECTED stamp → small Myanmar flag → tiny
  paper boat on the bench.
- 13 IBIZA: sky + sun/cloud/gulls → deep blue Mediterranean + waves →
  tanker tipped on its side, red hull showing → orange rescue boat →
  tiny life ring floating on the water.

**Similar scenes kept deliberately distinct:** Gaza seafront at dawn
(apartment blocks + smoke + tents + schoolbook) vs Kuwait Gulf coast
at dusk (concrete station + radar dish + drone + flag patch) vs
Bangkok refinery (tanks + tower + flames + fire crews + hard hat).
Brussels (blue EU banner + round table + banknotes) vs Frankfurt
(navy tower + euro coin + three flags) vs Kyiv (office interior +
framed map + phone).

## Map — real country outlines
- Fresh data: Natural Earth via
  https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json
  (180 countries), downloaded to `tools/countries.geo.json`.
- `tools/gen_map.py` (written fresh for this edition): equirectangular
  projection lon −180…180 → x 0…984, lat 75…−52 → y 0…144;
  Douglas–Peucker ~0.45°; Antarctica dropped; 281 paths in
  `tools/land.svg`, embedded verbatim in `render.html`.
- Numbered dots at each story's real lat/lon; badges shifted with
  leader lines; the generator checks every badge pair is ≥ 15px apart
  (result: minimum 15.4px, no rectangle overlap). London appears
  three times (stories 8, 21, 24) — one dot, three badges fanning
  out. Continent labels sit in empty sea/land.
- Map title: "WHERE IT HAPPENED — SCENES 1–13".

## Spacing (measured, Playwright)
- Padding: 0 top, 8px bottom, 20px left/right (header/footer
  full-bleed with margin −20px).
- Section heights: header 78, strip 22, chips 23, leads 178, feature
  label 19, features 304, map 162, briefs label 19, briefs 98,
  ALSO TODAY 29, footer 59. Page is exactly 1024 tall: ALSO TODAY
  bottom y=957 = footer top.

## Bug lessons applied (from the 25 November edition)
- Brief grid columns need `min-width:0` on the column divs, or
  `white-space:nowrap` briefs force the grid wider than the page
  (first render: page scrollWidth 1253).
- Briefs must be short: at 9.5px a column fits ~64 characters
  including number, city, stat and source; two briefs were trimmed
  after the first measure.
- Feature bodies must stay at 2 lines (~76 characters max); two
  bodies wrapped to 3 lines and clipped their cards — trimmed.
- Lead cards need their scene at 82px with tight headline margins or
  the meta row clips by 2px.
- The EU star ring needs a real circle (radius ~7px in a taller
  banner), not a wide flat ellipse, or it reads as a dotted line.
- A radar dish needs a dark outline on a pale sky, or it disappears.
- Never mix implicit string concatenation with `+` in one return —
  scenes are built as lists + `"".join`.
- Elements that must hide behind something are drawn BEFORE the
  element that covers them.
