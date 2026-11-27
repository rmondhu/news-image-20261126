# THE WORLD TODAY — 26 November 2026

[![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/rmondhu/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/rmondhu/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

One image summing up Thursday 26 November 2026's world news: 32
stories across 6 continents — the Kuwait drone strike, the Gaza
overnight strikes, and DR Congo's Ebola outbreak passing 12,000
cases lead the front page, with 10 more illustrated stories, a real
world map of where it all happened, 19 briefs, and a DATE CHECK box
naming the stories left out for being off-date.

All pictures and the map are drawn in code (inline SVG), not photos.
Fonts are Google Fonts (SIL OFL 1.1), embedded in `render.html`, so
rendering needs no network.

## Run it

```
python3 tools/gen_map.py    # build tools/land.svg from Natural Earth data
python3 tools/gen_entry.py  # build render.html from the story data
node render.mjs             # render render.html to entry.png (1024x1024)
node measure.mjs            # Playwright layout check (heights, overflow, clipping)
MAKEFUN_OUTPUT_DIR=out node main.ts   # validate entry.png and copy it to out/
```

`main.ts` checks that `entry.png` is a 1024×1024 PNG under 1 MiB and
copies it byte-for-byte into `MAKEFUN_OUTPUT_DIR` (default `/output`).

## Files

- `entry.png` — the front page.
- `render.html` — the page; `render.mjs` screenshots it.
- `tools/gen_entry.py` — story data + page builder (incl. map badges).
- `tools/scenes.py` — the 13 code-drawn scenes.
- `tools/gen_map.py` — country outlines → `tools/land.svg`.
- `news.md` — the 32 stories, sources, and date notes.
- `DESIGN.md`, `REPORT.md`, `TESTS.md` — design system, build report,
  and test log.
