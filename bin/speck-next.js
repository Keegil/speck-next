#!/usr/bin/env node
// Speck Next installer/upgrader. Run from anywhere:
//   npx github:Keegil/speck-next install [dir]
//   npx github:Keegil/speck-next upgrade [dir]
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const SRC = path.join(__dirname, "..");
const VERSION = require(path.join(SRC, "package.json")).version;
const SURFACE = ["AGENTS.md", "CLAUDE.md", path.join(".claude", "skills"), "templates"];
const MARKER = path.join(".claude", "speck-next.json");

const cmd = process.argv[2];
const target = path.resolve(process.argv[3] || ".");

function die(msg) { console.error(msg); process.exit(1); }

function copySurface() {
  for (const item of SURFACE) {
    const from = path.join(SRC, item), to = path.join(target, item);
    fs.mkdirSync(path.dirname(to), { recursive: true });
    fs.cpSync(from, to, { recursive: true });
  }
  let commit = null;
  try { commit = execSync("git rev-parse --short HEAD", { cwd: SRC, stdio: ["ignore", "pipe", "ignore"] }).toString().trim(); } catch {}
  fs.writeFileSync(path.join(target, MARKER),
    JSON.stringify({ name: "speck-next", version: VERSION, commit, installedAt: new Date().toISOString() }, null, 2) + "\n");
}

function retireReplacedSkills() {
  // v4.0.0 migration: independent-review split into the experience and judge skills; copy never deletes, so the upgrader must.
  const old = path.join(target, ".claude", "skills", "independent-review");
  if (fs.existsSync(old)) fs.rmSync(old, { recursive: true });
}

function ensureMap() {
  // v2.0.0 file-contract migration: every governed repo carries map.md; the upgrader owns this.
  const mapPath = path.join(target, "map.md");
  if (!fs.existsSync(mapPath))
    fs.writeFileSync(mapPath, "# Map\n\nNo map yet. When shaping closes, the ordered build pieces land here — each naming what it serves and which shaped material it consumes, exactly one live, unconsumed shaped material listed at the bottom.\n");
}

function gitChanges() {
  try {
    return execSync("git status --short -- AGENTS.md CLAUDE.md .claude", { cwd: target }).toString().trim();
  } catch { return ""; }
}

if (cmd === "install") {
  if (!fs.existsSync(target)) die(`no such directory: ${target}`);
  if (!fs.existsSync(path.join(target, ".git"))) die(`not a git repository: ${target} (git init first)`);
  if (path.resolve(SRC) === target) die("refusing: that's the kernel repo itself");
  if (fs.existsSync(path.join(target, "AGENTS.md")) || fs.existsSync(path.join(target, "CLAUDE.md")))
    die(`refusing: ${target} already carries agent instructions.\n` +
        `If it's a Speck Next repo, use: npx github:Keegil/speck-next upgrade\n` +
        `If it's an old-Speck or custom repo, converting it is a later version's job. Nothing was touched.`);
  copySurface();
  ensureMap();
  const files = execSync(`find AGENTS.md CLAUDE.md .claude templates -type f`, { cwd: target }).toString().trim().split("\n").length;
  console.log(`Installed Speck Next v${VERSION} into ${target} (${files} files).`);
  console.log("Next: open an agent session there and say what you want to build — shaping starts in that conversation.");
} else if (cmd === "upgrade") {
  const markerPath = path.join(target, MARKER);
  if (!fs.existsSync(markerPath))
    die(`refusing: ${target} doesn't look like a Speck Next repo (no ${MARKER}).\n` +
        `Fresh repo? Use: npx github:Keegil/speck-next install\n` +
        `Old-Speck repo? Converting it is a later version's job. Nothing was touched.`);
  const prior = JSON.parse(fs.readFileSync(markerPath));
  copySurface();
  retireReplacedSkills();
  ensureMap();
  const changes = gitChanges();
  const from = prior.commit ? `${prior.version} (${prior.commit})` : prior.version;
  console.log(`Upgraded Speck Next ${from} -> ${VERSION} in ${target}.`);
  console.log(changes
    ? `What changed (git has your back — diff or revert as you like):\n${changes}`
    : "Already up to date — nothing changed.");
} else {
  console.log(`speck-next v${VERSION} — a small kernel for building great products and proving them by running them.

  npx github:Keegil/speck-next install [dir]   place the method into a fresh git repo (default: current dir)
  npx github:Keegil/speck-next upgrade [dir]   refresh the method files in a Speck Next repo

The method itself is one page: AGENTS.md. Everything else is five skills your agent loads on demand, and six file skeletons in templates/.
Pin a version: npx -y github:Keegil/speck-next#v4.0.0 install`);
}
