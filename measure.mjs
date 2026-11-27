// Measure the rendered page with Playwright: section heights,
// horizontal overflow, clipped card text, wrapped/clipped briefs,
// and where the last brief ends relative to the footer top.
// Fresh for news-image-20261126.
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire("/home/hatch/workspace/makefun/tools/package.json");
const { chromium } = require("playwright");

const dir = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(dir, "render.html");

const browser = await chromium.launch({ args: ["--force-device-scale-factor=1"] });
const page = await browser.newPage({
  viewport: { width: 1024, height: 1024 },
  deviceScaleFactor: 1,
});
await page.goto("file://" + htmlPath, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(150);

const report = await page.evaluate(() => {
  const box = (el) => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return { top: Math.round(r.top), bottom: Math.round(r.bottom),
             height: Math.round(r.height) };
  };
  const q = (sel) => document.querySelector(sel);
  const qa = (sel) => Array.from(document.querySelectorAll(sel));
  const pageEl = q(".page");
  const sections = {
    header: box(q("header")),
    strip: box(q(".strip")),
    chips: box(q(".chips")),
    leads: box(q(".leads")),
    featsLabel: box(qa(".seclabel")[0]),
    feats: box(q(".feats")),
    map: box(q(".mapsec")),
    briefsLabel: box(qa(".seclabel")[1]),
    briefs: box(q(".briefcols")),
    also: box(q(".also")),
    footer: box(q("footer")),
    pageScrollW: pageEl.scrollWidth,
    pageScrollH: pageEl.scrollHeight,
    bodyScrollW: document.body.scrollWidth,
  };
  const clippedCards = qa(".card").map((c, i) => ({
    card: i + 1,
    clientH: c.clientHeight,
    scrollH: c.scrollHeight,
    clipped: c.scrollHeight > c.clientHeight + 1,
  })).filter((c) => c.clipped);
  const briefs = qa(".brief").map((b, i) => {
    const r = b.getBoundingClientRect();
    return {
      n: i + 14,
      bottom: Math.round(r.bottom),
      clipped: b.scrollWidth > b.clientWidth + 1,
      wrapped: b.scrollHeight > 15,
    };
  });
  const alsoItems = qa(".also div").map((d) => ({
    text: d.textContent.slice(0, 30),
    clipped: d.scrollWidth > d.clientWidth + 1,
    wrapped: d.scrollHeight > 16,
  }));
  const stripItems = qa(".strip div").map((d) => {
    const r = d.getBoundingClientRect();
    return { lines: Math.round(r.height / 14.4), height: Math.round(r.height) };
  });
  const fonts = {
    playfair: document.fonts.check("900 15px 'Playfair Display'"),
    franklin: document.fonts.check("400 10px 'Libre Franklin'"),
    oswald: document.fonts.check("600 12px Oswald"),
  };
  const lastBriefBottom = Math.max(...briefs.map((b) => b.bottom));
  const alsoBottom = Math.round(q(".also").getBoundingClientRect().bottom);
  const wide = [];
  document.querySelectorAll("*").forEach((el) => {
    const r = el.getBoundingClientRect();
    if (r.right > 1024.5 || r.left < -0.5) {
      wide.push({ tag: el.tagName,
        cls: typeof el.className === "string" ? el.className : "",
        left: Math.round(r.left), right: Math.round(r.right),
        text: (el.textContent || "").slice(0, 40) });
    }
  });
  return { sections, clippedCards, briefs, alsoItems, stripItems, fonts,
           lastBriefBottom, alsoBottom, footerTop: sections.footer.top,
           wide: wide.slice(0, 10) };
});

console.log(JSON.stringify(report, null, 2));
await browser.close();
