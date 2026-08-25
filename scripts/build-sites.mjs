import { cp, mkdir, rm, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outputRoot = path.resolve(root, "dist", "client");
const expectedOutput = `${path.resolve(root, "dist")}${path.sep}`;

if (!outputRoot.startsWith(expectedOutput) || outputRoot === path.resolve(root)) {
  throw new Error("Refusing to build outside the site output folder.");
}

const publicEntries = [
  "index.html",
  "styles.css",
  "app.js",
  "favicon.svg",
  "assets",
  "guide",
  "releases"
];

await rm(outputRoot, { recursive: true, force: true });
await mkdir(outputRoot, { recursive: true });

for (const entry of publicEntries) {
  const source = path.join(root, entry);
  const destination = path.join(outputRoot, entry);
  const sourceStat = await stat(source);
  await cp(source, destination, { recursive: sourceStat.isDirectory() });
}

console.log(`Prepared ${publicEntries.length} public entries in dist/client.`);
