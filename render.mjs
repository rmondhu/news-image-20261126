// Render render.html to entry.png (1024x1024, deterministic).
// Fresh for news-image-20261126. Uses the Playwright install that
// already lives in the shared make.fun tools directory; no network
// is used at render time (fonts are embedded in render.html).
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire("/home/hatch/workspace/makefun/tools/package.json");
const { chromium } = require("playwright");

const dir = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(dir, "render.html");
const outPath = process.argv[2] || path.join(dir, "entry.png");

const browser = await chromium.launch({ args: ["--force-device-scale-factor=1"] });
const page = await browser.newPage({
  viewport: { width: 1024, height: 1024 },
  deviceScaleFactor: 1,
});
await page.goto("file://" + htmlPath, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(150);
await page.screenshot({ path: outPath });
await browser.close();
console.log("wrote " + outPath);
