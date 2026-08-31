#!/usr/bin/env node
// Speck Next installer/upgrader. Run from anywhere:
//   npx github:Keegil/speck-next install [dir]
//   npx github:Keegil/speck-next upgrade [dir]
const fs = require("fs");
const path = require("path");
const { execFileSync, execSync } = require("child_process");

const SRC = path.join(__dirname, "..");
const VERSION = require(path.join(SRC, "package.json")).version;
const SURFACE = ["AGENTS.md", "CLAUDE.md", path.join(".claude", "skills"), "templates"];
const MARKER = path.join(".claude", "speck-next.json");
const REPORTED_PATHS = [...SURFACE, MARKER, "product.md"];

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
  const markerPath = path.join(target, MARKER);
  let installedAt = new Date().toISOString();
  try {
    const existing = JSON.parse(fs.readFileSync(markerPath, "utf8"));
    if (existing.version === VERSION && existing.commit === commit && existing.installedAt)
      installedAt = existing.installedAt;
  } catch {}
  fs.writeFileSync(markerPath,
    JSON.stringify({ name: "speck-next", version: VERSION, commit, installedAt }, null, 2) + "\n");
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

function isPreV6(version) {
  const major = Number.parseInt(String(version || "").replace(/^v/i, "").split(".")[0], 10);
  return !Number.isFinite(major) || major < 6;
}

function ensureProductTeamAssessment(priorVersion) {
  if (!isPreV6(priorVersion)) return "Product team migration: not needed (already v6 or later).";
  const productPath = path.join(target, "product.md");
  if (!fs.existsSync(productPath))
    return "Product team migration: no product.md exists, so nothing was invented; the v6 template will guide shaping.";
  const current = fs.readFileSync(productPath, "utf8");
  if (/^##[ \t]+Product team[ \t]*$/im.test(current))
    return "Product team migration: existing product.md section preserved.";
  const prefix = current.endsWith("\n") ? "\n" : "\n\n";
  fs.appendFileSync(productPath, prefix + `## Product team

**Upgrade status:** Unassessed under v6. Historical work keeps its original evidence and is not backfilled as role-shaped. Before the next substantial piece, Product, Business, Experience, and Engineering assess this product in four separate contexts. Reopen Shape only if that assessment finds a wrong promise.
`);
  return "Product team migration: added one honest unassessed section to product.md; historical work was untouched.";
}

function gitRead(args) {
  try {
    return execFileSync("git", args, { cwd: target, encoding: "utf8" }).trim();
  } catch { return ""; }
}

function gitChanges() {
  return gitRead(["status", "--short", "--", ...REPORTED_PATHS]);
}

function gitDiff() {
  const parts = [];
  const tracked = gitRead(["diff", "--", ...REPORTED_PATHS]);
  if (tracked) parts.push(tracked);
  const untracked = gitRead(["ls-files", "--others", "--exclude-standard", "--", ...REPORTED_PATHS]);
  for (const file of untracked.split("\n").filter(Boolean)) {
    try {
      execFileSync("git", ["diff", "--no-index", "--", "/dev/null", file], { cwd: target, encoding: "utf8" });
    } catch (err) {
      if (err.status !== 1) continue;
      const addition = String(err.stdout || "").trim();
      if (addition) parts.push(addition);
    }
  }
  return parts.join("\n");
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
  const files = execSync(`find AGENTS.md CLAUDE.md .claude templates map.md -type f`, { cwd: target }).toString().trim().split("\n").length;
  console.log(`Installed Speck Next v${VERSION} into ${target} — ${files} files on disk (method files, the version marker, an empty starter map).`);
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
  const migration = ensureProductTeamAssessment(prior.version);
  const changes = gitChanges();
  const diff = gitDiff();
  const from = prior.commit ? `${prior.version} (${prior.commit})` : prior.version;
  console.log(`Upgraded Speck Next ${from} -> ${VERSION} in ${target}.`);
  console.log(migration);
  console.log(changes
    ? `Changed paths across the complete installed surface plus product.md:\n${changes}`
    : "Already up to date — nothing changed.");
  console.log(diff
    ? `Complete installed-surface plus product.md diff (working tree against HEAD):\n${diff}`
    : "Complete installed-surface plus product.md diff: empty.");
} else {
  console.log(`speck-next v${VERSION} — a small kernel for building great products and proving them by running them.

  npx github:Keegil/speck-next install [dir]   place the method into a fresh git repo (default: current dir)
  npx github:Keegil/speck-next upgrade [dir]   refresh the method files in a Speck Next repo

The method itself is one page: AGENTS.md. Everything else is five skills your agent loads on demand, and six file skeletons in templates/.
Pin a released tag, e.g.: npx -y github:Keegil/speck-next#v5.0.0 install  (all tags: github.com/Keegil/speck-next/tags)`);
}
