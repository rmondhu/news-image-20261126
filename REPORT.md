# Report — news-image-20261126 (27 Nov 2026)

**Entry:** `~/workspace/makefun/entries/news-image-20261126/entry.png`
**Size:** 292,276 bytes · PNG 1024×1024 RGB · SHA-256
`4e439cd97c53e0aa7702c5d012a74c6a030fe2f0dd387e554e467fc8e89a3deb`
**Status:** Built, verified, NOT pushed, NOT submitted — awaiting Hap's check.

## The 32 stories — why these

All events happened, or were first reported, on Thursday 26 November
2026. Sources: Reuters, AP, BBC, CNN, AFP, The Guardian, WSJ, ONS,
KCNA via Reuters, UN News, UEFA, Sportradar, FlightAware via Reuters.
Full notes in `news.md`.

**Leads (the three stories a picture editor would lead with):**
1. **KUWAIT** — Iranian drones kill two Italian technicians at a
   Kuwaiti air defence station; Italy and Kuwait blame Iran, Tehran
   denies it. The day's sharpest escalation — and the honest pill is
   CLAIM, because the attribution is one side's word.
2. **GAZA** — Israeli strikes kill nine in Gaza overnight, including
   Hamas deputy education minister Khaled Abu Nada and his wife. The
   day's deadliest single event.
3. **EBOLA** — DR Congo's Ebola outbreak passes 12,000 confirmed
   cases, nearly half dead, as fighting in Ituri disrupts the
   response. The day's biggest toll, from official ministry data.

**Grid (breadth across 6 continents):**
- Middle East (18, 30): Saudi airstrikes on Houthi-held Yemen; Irbil
  protests as Baghdad moves on Kurdish oil.
- Europe (5, 6, 8, 9, 10, 13, 15, 17, 21, 22, 23, 24, 26, 32): EU
  summit split over the €1.58tn budget and €45bn Ukraine loan; first
  Spaniard picked to run the ECB; UK net migration at 77,000; Russian
  strikes on grain ships near Odesa; Zelensky's BBC interview; the
  Ibiza tanker capsize; Serbia's early election; a refinery drone hit
  in Krasnodar; UK-EU treaties; Depardieu trial; the Huntingdon train
  stabbing verdict; Mandelson's shares; Bournemouth in Europe; the
  Miraval settlement.
- Americas (11, 14, 25, 28): the Thanksgiving nor'easter (850,000
  without power); Trump's GDP-data probe; Bears–Lions 39-35; Brazil
  inflation at 4.64%.
- Asia (4, 7, 12, 20, 27): Kim's nuclear deployment order; the
  Bangkok refinery fire; Myanmar's rejection of the ICJ orders; the
  Bogor mine deaths; South Korea's rate rise to 3.25%.
- Africa (16, 19, 29, 31): Guinea-Bissau's delayed elections; the
  Cairo crash driver's detention; the Nairobi Ebola-centre ruling;
  DR Congo recalling Uganda's ambassador.
- **Also today:** Brent $96.57 (+2.1%) on Middle East supply fears;
  Brazil and China push back on the new US tariffs.

**What was left out (alternates and date notes in `news.md`):**
the Macy's parade postponement, FedEx Miami overrun, Trump tariff
proposals, Houthi port strikes, Hormuz mine claim, Netanyahu trial
vote, Cartagena rescue, Canary arrivals, Shenzhou-24 docking,
Poundland collapse, Poland no-fly plan, Rams–Packers game and the
Cairo tanker fire itself — all Wednesday 25 November, not 26
November. The Trump–Putin photo is from 22 November; the Myanmar ICJ
ruling itself is from last week. All are named in the DATE CHECK box.

## Design decisions
- Same winner system as the 25 November edition (12/12 in dev): navy
  header + gold kicker, red headline strip, region colour system,
  framed cards, stat ribbons inside code-drawn scenes, real world
  map, red DATE CHECK footer + navy sources strip, three fonts. See
  `DESIGN.md`.
- All 13 scenes are new, written fresh from the ILLUSTRATION lines in
  `news.md` — nothing copied from yesterday's scenes. Similar scenes
  are kept apart on purpose (Gaza dawn seafront vs Kuwait dusk coast
  vs Bangkok refinery; Brussels vs Frankfurt vs Kyiv).
- Verification pills set honestly: Kuwait = CLAIM (deaths confirmed,
  attribution denied by Tehran); Pyongyang = REPORTED (KCNA via
  Reuters); Odesa = REPORTED (Ukraine PM via Reuters); Naypyidaw =
  REPORTED (Reuters via state media); Ebola = OFFICIAL (DRC health
  ministry data); Kyiv = OFFICIAL (BBC interview, on the record).
- Map rebuilt from fresh data: Natural Earth countries.geo.json
  (180 countries) downloaded for this edition; `tools/gen_map.py`
  written fresh (281 paths); badge positions chosen fresh for this
  edition's 32 locations (London appears three times — stories 8, 21,
  24 share one dot with three badges fanning out).

## Fixes found in the first renders
1. **Horizontal overflow:** the brief grid blew out to 1253px wide —
   `white-space:nowrap` briefs forced the grid columns past the page.
   Added `min-width:0` to the column divs; page scrollWidth is now
   exactly 1024.
2. **Briefs 17 and 20 clipped** after the grid fix (too long for the
   column) → trimmed to "Drone attack hits refinery unit." and
   "13 dead, 13 trapped in gold mine."
3. **Feature bodies 4 and 11 wrapped to 3 lines** and clipped their
   cards by 10px → trimmed to 72 and 66 characters.
4. **Lead cards 1 and 3 clipped by 2px** → scene 90px → 82px and
   tighter headline margins.
5. **Page 53px too tall on the first render** → header, strip
   (one-line headlines with city prefixes), chips, labels, brief
   line-height and footer all tightened; the page now fits exactly
   (footer top y=957, bottom y=1016).
6. **Brussels star ring read as a dotted line** (flat ellipse) →
   rebuilt as a real circle of 12 stars in a taller banner.
7. **Kuwait radar dish invisible on the pale sky** → rebuilt as a
   white half-disc with a dark outline on a mast.

## Verification
- PNG 1024×1024, 292,276 bytes (< 1 MiB). ✔
- `main.ts` run twice (two output dirs) → identical SHA-256
  `4e439cd97c53e0aa7702c5d012a74c6a030fe2f0dd387e554e467fc8e89a3deb`,
  matching entry.png. Deterministic. ✔
- Re-render via `node render.mjs` → identical SHA-256 again. ✔
- `python3 tools/gen_entry.py` → render.html 227,810 bytes; badge
  check: minimum badge centre distance 15.4px (≥ 15), no rectangle
  overlap. ✔
- Layout measurement (Playwright, `measure.mjs`): head 78, strip 22,
  chips 23, leads 178, feats 304, map 162, briefs 98, also 29,
  foot 59; all 19 briefs visible, 0 wrapped, 0 clipped; no clipped
  cards; no horizontal overflow; ALSO TODAY bottom y=957 = footer
  top. ✔
- Visual inspection at full size + 2× leads zoom + 2× features zooms
  + 2× map zoom + Europe cluster zoom: all 13 scenes legible and
  relevant; similar scenes read as different; stat ribbons readable
  inside every scene; no clipped or colliding text; map is real world
  outlines with all 32 badges legible. ✔

## Files
- `entry.png` — the image for Hap to grade.
- `render.html`, `render.mjs`, `measure.mjs`, `main.ts`, `news.md`,
  `DESIGN.md`, `REPORT.md`, `TESTS.md`, `LICENSE`, `README.md`
- `.makefun/owner.json` — payout wallet
- `tools/gen_entry.py` — builds render.html from story data
- `tools/scenes.py` — the 13 rich vector scenes (one function per scene)
- `tools/gen_map.py` — builds tools/land.svg from Natural Earth data
- `tools/countries.geo.json` — 180-country outlines (source data)
- `tools/land.svg` — 281 country paths embedded in render.html
- `fonts/` — PlayfairDisplay-700.woff2, LibreFranklin-400.woff2,
  Oswald-600.woff2 (Google Fonts, SIL OFL 1.1)

## Not done (by design)
- No GitHub repo created, nothing pushed, nothing submitted to make.fun.
- No transcript bundle built (needed only for a real submission).
