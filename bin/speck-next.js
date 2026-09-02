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
const REPORTED_PATHS = [...SURFACE, MARKER, "map.md", "product.md"];
const RC1_UNIVERSAL_STATUS = "**Upgrade status:** Unassessed under v6. Historical work keeps its original evidence and is not backfilled as role-shaped. Before the next substantial piece, Product, Business, Experience, and Engineering assess this product in four separate contexts. Reopen Shape only if that assessment finds a wrong promise.";
const SELECTIVE_STATUS = "**Upgrade status:** Unassessed under Speck Next 6.0.0-rc.2. Historical work keeps its original evidence and is not backfilled as role-shaped. Before the next substantial piece, separate Product, Business, Experience, and Engineering carriers assess the existing product and current map once. Business and Experience then define their observable call conditions, trusted evidence, expiry, and material changes. Reopen Shape only for a wrong promise and Map only for a wrong piece or order.";

const cmd = process.argv[2];
const target = path.resolve(process.argv[3] || ".");

function die(msg) { console.error(msg); process.exit(1); }

function sourceCommit() {
  try { return execSync("git rev-parse --short HEAD", { cwd: SRC, stdio: ["ignore", "pipe", "ignore"] }).toString().trim(); }
  catch { return null; }
}

function copySurface() {
  for (const item of SURFACE) {
    const from = path.join(SRC, item), to = path.join(target, item);
    fs.mkdirSync(path.dirname(to), { recursive: true });
    fs.cpSync(from, to, { recursive: true });
  }
  return sourceCommit();
}

function writeMarker(existing, commit) {
  const markerPath = path.join(target, MARKER);
  let installedAt = new Date().toISOString();
  if (existing && existing.version === VERSION && existing.commit === commit && existing.installedAt)
    installedAt = existing.installedAt;
  fs.mkdirSync(path.dirname(markerPath), { recursive: true });
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

function migrationSource(version) {
  const normalized = String(version || "").trim().replace(/^v/i, "");
  const match = normalized.match(/^(\d+)\.(\d+)\.(\d+)(?:-[0-9A-Za-z.-]+)?$/);
  if (!match) return "unknown";
  if (normalized === "6.0.0-rc.1") return "rc.1";
  return Number(match[1]) < 6 ? "pre-v6" : "current";
}

function ensureProductTeamAssessment(source) {
  if (source === "current")
    return "Product team migration: not needed (the repository already carries the selective contract).";
  const productPath = path.join(target, "product.md");
  if (!fs.existsSync(productPath))
    return "Product team migration: product.md is missing, so no product history or assessment was invented.";
  const current = fs.readFileSync(productPath, "utf8");
  if (current.includes(SELECTIVE_STATUS))
    return "Product team migration: the selective unassessed status is already present; product.md was unchanged.";
  if (current.includes(RC1_UNIVERSAL_STATUS)) {
    fs.writeFileSync(productPath, current.replace(RC1_UNIVERSAL_STATUS, SELECTIVE_STATUS));
    return "Product team migration: replaced the exact generated rc.1 universal status with the selective rc.2 status; every other product.md byte was preserved.";
  }
  const prefix = current.endsWith("\n") ? "\n" : "\n\n";
  if (/^##[ \t]+Product team[ \t]*$/im.test(current)) {
    fs.appendFileSync(productPath, prefix + `## Speck Next product-team assessment

${SELECTIVE_STATUS}
`);
    return "Product team migration: preserved the owner-authored Product team section and added one selective unassessed status; historical text was untouched.";
  }
  fs.appendFileSync(productPath, prefix + `## Product team

${SELECTIVE_STATUS}
`);
  return "Product team migration: added one selective unassessed Product team section; historical text was untouched.";
}

function versionWithCommit(version, commit) {
  return commit ? `${version} (${commit})` : `${version} (commit unavailable)`;
}

function installedFiles() {
  const files = [];
  function visit(relative) {
    const absolute = path.join(target, relative);
    if (!fs.existsSync(absolute)) return;
    const stat = fs.statSync(absolute);
    if (stat.isDirectory()) {
      for (const name of fs.readdirSync(absolute).sort()) visit(path.join(relative, name));
    } else files.push(relative);
  }
  for (const root of [...SURFACE, "map.md"]) visit(root);
  files.push(MARKER);
  return files.sort();
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
  const commit = copySurface();
  ensureMap();
  writeMarker(null, commit);
  const files = installedFiles();
  console.log(`Installed Speck Next ${versionWithCommit(VERSION, commit)} into ${target} — ${files.length} files on disk (method files, the version marker, and an empty starter map).`);
  console.log(`Installed paths:\n${files.join("\n")}`);
  console.log("Next: open an agent session there and say what you want to build — shaping starts in that conversation.");
} else if (cmd === "upgrade") {
  const markerPath = path.join(target, MARKER);
  if (!fs.existsSync(markerPath))
    die(`refusing: ${target} doesn't look like a Speck Next repo (no ${MARKER}).\n` +
        `Fresh repo? Use: npx github:Keegil/speck-next install\n` +
        `Old-Speck repo? Converting it is a later version's job. Nothing was touched.`);
  let prior;
  try { prior = JSON.parse(fs.readFileSync(markerPath, "utf8")); }
  catch { die(`refusing: ${MARKER} is not valid JSON. Nothing was touched.`); }
  const source = migrationSource(prior.version);
  if (source === "unknown")
    die(`refusing: ${MARKER} carries an unknown version (${JSON.stringify(prior.version)}). Nothing was touched.`);
  const commit = copySurface();
  retireReplacedSkills();
  ensureMap();
  const migration = ensureProductTeamAssessment(source);
  writeMarker(prior, commit);
  const changes = gitChanges();
  const diff = gitDiff();
  const from = versionWithCommit(prior.version, prior.commit || null);
  const to = versionWithCommit(VERSION, commit);
  console.log(`Upgraded Speck Next ${from} -> ${to} in ${target}.`);
  console.log(migration);
  console.log(changes
    ? `Working-tree changes across the complete installed surface plus product.md:\n${changes}`
    : "Working-tree changes across the complete installed surface plus product.md: none.");
  console.log(diff
    ? `Complete installed-surface plus product.md diff (working tree against HEAD):\n${diff}`
    : "Complete installed-surface plus product.md diff: empty.");
  console.log("Next: review the reported paths and complete diff, commit the upgrade, then run the product-team assessment named in product.md before the next substantial piece.");
} else {
  console.log(`speck-next v${VERSION} — a small kernel for building great products and proving them by running them.

  npx github:Keegil/speck-next install [dir]   place the method into a fresh git repo (default: current dir)
  npx github:Keegil/speck-next upgrade [dir]   refresh the method files in a Speck Next repo

The method itself is one page: AGENTS.md. Everything else is five skills your agent loads on demand, and six file skeletons in templates/.
Pin a released tag, e.g.: npx -y github:Keegil/speck-next#v5.0.0 install  (all tags: github.com/Keegil/speck-next/tags)`);
}
