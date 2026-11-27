# Tests — news-image-20261126

All checks run from the entry directory
`~/workspace/makefun/entries/news-image-20261126/`.
Every check below passed on the final build (27 Nov 2026).

## 1. Build the page
```
python3 tools/gen_map.py      # tools/land.svg, 281 paths, 180 countries
python3 tools/gen_entry.py    # render.html; prints min badge distance
```
Expected: `min badge centre distance: 15.4 px (need >= 15)`,
`region counts: Middle East 4, Europe 14, Africa 5, Asia 5,
N. America 3, S. America 1`, `total stories: 32`.
Result: pass.

## 2. Render (deterministic)
```
node render.mjs
sha256sum entry.png
node render.mjs
sha256sum entry.png
```
Expected: both runs give the same SHA-256.
Result: pass — both runs
`4e439cd97c53e0aa7702c5d012a74c6a030fe2f0dd387e554e467fc8e89a3deb`.

## 3. Entry file
```
node -e "const b=require('fs').readFileSync('entry.png');
console.log(b.readUInt32BE(16)+'x'+b.readUInt32BE(20), b.length)"
```
Expected: `1024x1024`, under 1,048,576 bytes.
Result: pass — 1024×1024, 292,276 bytes.

## 4. Runner (main.ts, twice, different output dirs)
```
MAKEFUN_OUTPUT_DIR=out1 node main.ts; echo $?
MAKEFUN_OUTPUT_DIR=out2 node main.ts; echo $?
sha256sum out1/entry.png out2/entry.png entry.png
```
Expected: exit 0 both times; all three SHAs identical to entry.png.
Result: pass — exit 0, exit 0, all three
`4e439cd97c53e0aa7702c5d012a74c6a030fe2f0dd387e554e467fc8e89a3deb`.

## 5. Layout measurement (Playwright)
```
node measure.mjs
```
Expected: pageScrollW 1024, pageScrollH 1024 (no overflow); no
clipped cards; all 19 briefs single-line and unclipped; both ALSO
TODAY items single-line and unclipped; strip headlines 1 line each;
all three fonts loaded; ALSO TODAY bottom = footer top.
Result: pass — head 78, strip 22, chips 23, leads 178, feature label
19, features 304, map 162, briefs label 19, briefs 98, also 29,
footer 59 (top 957, bottom 1016); clippedCards []; briefs clipped []
wrapped []; alsoBottom 957 = footerTop 957; fonts all true.

## 6. Visual check
- Full page at 1024×1024, plus 2× crops of the leads, both feature
  rows, the map, the Europe badge cluster, and the briefs/footer.
- Checked: all 13 scenes legible and relevant to their stories; stat
  ribbons readable inside every scene; no clipped or colliding text;
  map is real world outlines with all 32 badges legible; DATE CHECK
  box and sources strip complete above the page bottom.
- Result: pass, after fixes 6 and 7 in REPORT.md (Brussels star ring,
  Kuwait radar dish).

## 7. Content honesty spot-checks
- Kuwait pill is CLAIM (deaths confirmed, attribution denied) — see
  news.md VERIFY line for story 1.
- Ebola figures 12,021 cases / 5,904 dead are the 26 Nov ministry
  figures from news.md, not the 25 Nov counts.
- DATE CHECK box names only off-date stories listed in news.md
  (25 Nov items, Trump–Putin photo 22 Nov, Myanmar ICJ ruling last
  week).
- Result: pass.
