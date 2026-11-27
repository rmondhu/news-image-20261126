// Entry runner for news-image-20261126.
// Validates entry.png (1024x1024 PNG, at most 1 MiB) and copies it
// byte-for-byte into MAKEFUN_OUTPUT_DIR (default /output), creating
// the directory when needed. Standard library only: no network,
// no clock, no dependencies.
import * as fs from "node:fs";
import * as path from "node:path";

const ENTRY = "entry.png";
const MAX_BYTES = 1024 * 1024;

function fail(message: string): never {
  console.error("main.ts: " + message);
  process.exit(1);
}

const here = path.dirname(new URL(import.meta.url).pathname);
const src = path.join(here, ENTRY);

if (!fs.existsSync(src)) {
  fail(ENTRY + " not found next to main.ts");
}
const buf = fs.readFileSync(src);
if (buf.length > MAX_BYTES) {
  fail(ENTRY + " is " + buf.length + " bytes, over the 1 MiB limit");
}
const pngSig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (buf.length < 33 || !buf.subarray(0, 8).equals(pngSig)) {
  fail(ENTRY + " is not a PNG file");
}
if (buf.toString("ascii", 12, 16) !== "IHDR") {
  fail(ENTRY + " has no IHDR chunk");
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  fail(ENTRY + " is " + width + "x" + height + ", expected 1024x1024");
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
fs.mkdirSync(outDir, { recursive: true });
const dest = path.join(outDir, ENTRY);
fs.copyFileSync(src, dest);
console.log("main.ts: copied " + ENTRY + " (" + buf.length + " bytes, 1024x1024) to " + dest);
