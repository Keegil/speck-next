#!/usr/bin/env node
// Speck Next installer/upgrader. Run from anywhere:
//   npx github:Keegil/speck-next install [dir]
//   npx github:Keegil/speck-next upgrade [dir]
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFileSync, execSync } = require("child_process");

const SRC = path.join(__dirname, "..");
const VERSION = require(path.join(SRC, "package.json")).version;
const SURFACE = ["AGENTS.md", "CLAUDE.md", path.join(".claude", "skills"), "templates"];
const MARKER = path.join(".claude", "speck-next.json");
const REPORTED_PATHS = [...SURFACE, MARKER, "map.md", "product.md"];
const RC1_UNIVERSAL_STATUS = "**Upgrade status:** Unassessed under v6. Historical work keeps its original evidence and is not backfilled as role-shaped. Before the next substantial piece, Product, Business, Experience, and Engineering assess this product in four separate contexts. Reopen Shape only if that assessment finds a wrong promise.";
const REJECTED_RC2_STATUS = "**Upgrade status:** Unassessed under Speck Next 6.0.0-rc.2. Historical work keeps its original evidence and is not backfilled as role-shaped. Before the next substantial piece, separate Product, Business, Experience, and Engineering carriers assess the existing product and current map once. Business and Experience then define their observable call conditions, trusted evidence, expiry, and material changes. Reopen Shape only for a wrong promise and Map only for a wrong piece or order.";
const ASSESSMENT_HEADING = "## Speck Next upgrade assessment";
const ASSESSMENT_RECORD = "work/product-team-assessment.md";
const ASSESSMENT_RECORD_LINE = `**Record:** \`${ASSESSMENT_RECORD}\``;
const ASSESSMENT_PENDING = "**Speck Next upgrade assessment:** pending";
const ASSESSMENT_BLOCK = `${ASSESSMENT_HEADING}\n\n${ASSESSMENT_PENDING}\n${ASSESSMENT_RECORD_LINE}\n`;

const cmd = process.argv[2];
const target = path.resolve(process.argv[3] || ".");

function die(msg) { console.error(msg); process.exit(1); }

function sourceCommit() {
  try { return execSync("git rev-parse --short HEAD", { cwd: SRC, stdio: ["ignore", "pipe", "ignore"] }).toString().trim(); }
  catch { return null; }
}

function surfaceManifest(root) {
  const files = [];
  function visit(relative) {
    const absolute = path.join(root, relative);
    const stat = fs.statSync(absolute);
    if (stat.isDirectory()) {
      for (const name of fs.readdirSync(absolute).sort()) visit(path.join(relative, name));
    } else files.push(relative);
  }
  for (const item of SURFACE) visit(item);
  return files.sort();
}

function surfaceDigest(root, manifest) {
  const digest = crypto.createHash("sha256");
  for (const relative of manifest) {
    digest.update(relative.split(path.sep).join("/"));
    digest.update("\0");
    digest.update(fs.readFileSync(path.join(root, relative)));
    digest.update("\0");
  }
  return digest.digest("hex");
}

function copySurface() {
  const sourceCheckout = sourceCommit();
  const manifest = surfaceManifest(SRC);
  const methodSurfaceSha256 = surfaceDigest(SRC, manifest);
  for (const item of SURFACE) {
    const from = path.join(SRC, item), to = path.join(target, item);
    fs.mkdirSync(path.dirname(to), { recursive: true });
    fs.cpSync(from, to, { recursive: true });
  }
  const copiedDigest = surfaceDigest(target, manifest);
  if (copiedDigest !== methodSurfaceSha256)
    die(`refusing: copied method bytes do not match the source method surface. The version marker was not changed.`);
  return { sourceCheckout, methodSurfaceSha256 };
}

function markerSourceCheckout(marker) {
  return marker && (marker.sourceCheckout || marker.commit) || null;
}

function writeMarker(existing, provenance, assessmentRecord) {
  const markerPath = path.join(target, MARKER);
  let installedAt = new Date().toISOString();
  if (existing && existing.version === VERSION &&
      markerSourceCheckout(existing) === provenance.sourceCheckout && existing.installedAt)
    installedAt = existing.installedAt;
  const next = {
    name: "speck-next",
    version: VERSION,
    sourceCheckout: provenance.sourceCheckout,
    methodSurfaceSha256: provenance.methodSurfaceSha256,
    upgradeAssessmentRecord: assessmentRecord,
  };
  next.installedAt = installedAt;
  fs.mkdirSync(path.dirname(markerPath), { recursive: true });
  fs.writeFileSync(markerPath, JSON.stringify(next, null, 2) + "\n");
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

function activeMarkdownLines(content) {
  const lines = content.split("\n");
  const active = [];
  let fence = null;
  for (const line of lines) {
    const marker = line.match(/^ {0,3}(`{3,}|~{3,})/);
    if (fence) {
      active.push(false);
      if (marker && marker[1][0] === fence[0] && marker[1].length >= fence.length) fence = null;
      continue;
    }
    if (marker) {
      fence = marker[1];
      active.push(false);
      continue;
    }
    active.push(!/^[ \t]*>/.test(line));
  }
  return { lines, active };
}

function assessmentError(message, repair = "Restore consistent assessment evidence, then run the upgrade again.") {
  die(`refusing: ${message} Nothing in the repository changed. ${repair}`);
}

function parseAssessment(content, required = false) {
  const { lines, active } = activeMarkdownLines(content);
  const headings = lines.flatMap((line, index) => active[index] && line === ASSESSMENT_HEADING ? [index] : []);
  if (headings.length === 0) {
    if (required) assessmentError(`the marker requires ${ASSESSMENT_HEADING}, but that canonical section is missing.`);
    return null;
  }
  if (headings.length !== 1)
    assessmentError(`product.md contains ${headings.length} canonical upgrade-assessment sections; exactly one is required.`);
  const start = headings[0];
  let end = lines.length;
  for (let index = start + 1; index < lines.length; index += 1) {
    if (active[index] && /^##[ \t]+[^#]/.test(lines[index])) { end = index; break; }
  }
  const statusPrefix = "**Speck Next upgrade assessment:**";
  const statusLines = [];
  const recordLines = [];
  for (let index = start + 1; index < end; index += 1) {
    if (!active[index]) continue;
    if (lines[index].startsWith(statusPrefix)) statusLines.push(lines[index]);
    if (lines[index].startsWith("**Record:**")) recordLines.push(lines[index]);
  }
  if (statusLines.length !== 1)
    assessmentError(`the canonical upgrade-assessment section has ${statusLines.length} status fields; exactly one is required.`);
  if (recordLines.length !== 1 || recordLines[0] !== ASSESSMENT_RECORD_LINE)
    assessmentError(`the canonical upgrade-assessment section must contain exactly ${ASSESSMENT_RECORD_LINE}.`);

  const status = statusLines[0];
  let assessment;
  if (status === ASSESSMENT_PENDING) {
    assessment = { state: "pending", route: null, record: ASSESSMENT_RECORD };
  } else if (status === "**Speck Next upgrade assessment:** complete — Shape reopened") {
    assessment = { state: "complete", route: "Shape", record: ASSESSMENT_RECORD };
  } else if (status === "**Speck Next upgrade assessment:** complete — Map reopened") {
    assessment = { state: "complete", route: "Map", record: ASSESSMENT_RECORD };
  } else {
    const resumed = status.match(/^\*\*Speck Next upgrade assessment:\*\* complete — resumed (.+) from state\.md$/);
    const livePiece = resumed && resumed[1].trim();
    if (!livePiece || /^\[.*\]$/.test(livePiece))
      assessmentError(`the canonical upgrade-assessment status is not pending or one of the three allowed completed routes.`);
    assessment = { state: "complete", route: "resume", livePiece, record: ASSESSMENT_RECORD };
  }
  if (assessment.state === "complete") {
    const recordPath = path.join(target, ASSESSMENT_RECORD);
    if (!fs.existsSync(recordPath) || !fs.statSync(recordPath).isFile())
      assessmentError(`the upgrade assessment says complete, but ${ASSESSMENT_RECORD} is missing.`);
  }
  return assessment;
}

function removeGeneratedLine(content, generated) {
  const { lines, active } = activeMarkdownLines(content);
  const matches = lines.flatMap((line, index) => active[index] && line === generated ? [index] : []);
  if (matches.length > 1)
    assessmentError(`product.md contains ${matches.length} unquoted copies of a generated upgrade status; its origin is ambiguous.`);
  if (matches.length === 1) lines[matches[0]] = "";
  return { content: lines.join("\n"), removed: matches.length === 1 };
}

function appendAssessment(content) {
  const prefix = content.endsWith("\n") ? "\n" : "\n\n";
  return content + prefix + ASSESSMENT_BLOCK;
}

function hasOwn(object, key) {
  return Object.prototype.hasOwnProperty.call(object, key);
}

function markerAssessmentDisposition(prior) {
  if (!hasOwn(prior, "upgradeAssessmentRecord")) return { known: false, record: null };
  const record = prior.upgradeAssessmentRecord;
  if (record !== null && record !== ASSESSMENT_RECORD)
    assessmentError(
      `the marker's upgradeAssessmentRecord is ${JSON.stringify(record)}; it must be null or ${JSON.stringify(ASSESSMENT_RECORD)}.`,
      "Restore the marker's explicit assessment disposition from version control, then run the upgrade again."
    );
  return { known: true, record };
}

function planProductTeamAssessment(source, prior) {
  const productPath = path.join(target, "product.md");
  const disposition = markerAssessmentDisposition(prior);
  if (!fs.existsSync(productPath)) {
    if (disposition.record === ASSESSMENT_RECORD)
      assessmentError(
        `the marker requires ${ASSESSMENT_RECORD}, but product.md is missing.`,
        "Restore product.md and its canonical assessment block, then run the upgrade again."
      );
    return {
      message: "Product team migration: product.md is missing, so no product history or assessment was invented.",
      assessment: null,
      assessmentRecord: null,
      productContent: null,
    };
  }
  if (!fs.statSync(productPath).isFile())
    assessmentError(
      "product.md exists but is not a file.",
      "Restore product.md as a regular file, then run the upgrade again."
    );

  const original = fs.readFileSync(productPath, "utf8");
  const existing = parseAssessment(original, disposition.record === ASSESSMENT_RECORD);
  const rc1 = removeGeneratedLine(original, RC1_UNIVERSAL_STATUS);
  const rejectedRc2 = removeGeneratedLine(rc1.content, REJECTED_RC2_STATUS);
  const generatedAssessment = rc1.removed || rejectedRc2.removed;

  if (disposition.known && disposition.record === null) {
    if (existing || generatedAssessment || source !== "current")
      assessmentError(
        "the marker says no upgrade assessment applies, but the repository contains evidence that one is required.",
        "Restore the marker and product assessment evidence from the same successful upgrade, then run it again."
      );
    return {
      message: "Product team migration: not needed (the marker explicitly records that no one-time assessment applies).",
      assessment: null,
      assessmentRecord: null,
      productContent: null,
    };
  }

  if (existing) {
    return {
      message: `Product team migration: kept the explicit ${existing.state} upgrade assessment; product.md was unchanged.`,
      assessment: existing,
      assessmentRecord: ASSESSMENT_RECORD,
      productContent: null,
    };
  }

  if (source === "current" && !generatedAssessment)
    assessmentError(
      "this current rc.2 marker has no upgradeAssessmentRecord field and product.md has no surviving canonical or generated assessment evidence; Speck Next will not guess whether the one-time assessment applied.",
      "Restore the deleted assessment evidence or the explicit marker disposition from version control, then run the upgrade again."
    );

  const productContent = appendAssessment(rejectedRc2.content);
  const assessment = parseAssessment(productContent, true);
  let message = "Product team migration: preserved historical product bytes and appended one explicit pending upgrade assessment.";
  if (rc1.removed)
    message = "Product team migration: removed the exact generated rc.1 status and appended one explicit pending upgrade assessment; every other historical byte was preserved.";
  else if (rejectedRc2.removed)
    message = "Product team migration: repaired the rejected rc.2 generated status into one explicit pending upgrade assessment; every other historical byte was preserved.";
  return { message, assessment, assessmentRecord: ASSESSMENT_RECORD, productContent };
}

function applyProductTeamAssessment(plan) {
  if (plan.productContent !== null)
    fs.writeFileSync(path.join(target, "product.md"), plan.productContent);
}

function versionWithProvenance(version, sourceCheckout, methodSurfaceSha256) {
  return `${version} (source checkout ${sourceCheckout || "not recorded"}; method surface ${methodSurfaceSha256 ? `sha256:${methodSurfaceSha256}` : "not recorded"})`;
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
    return execFileSync("git", args, { cwd: target, encoding: "utf8" }).trimEnd();
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

function upgradeNext(changes, diff, assessment) {
  const hasChanges = Boolean(changes || diff);
  const productPath = path.join(target, "product.md");
  if (!fs.existsSync(productPath)) {
    return hasChanges
      ? "Next: review the reported paths and complete diff, commit the upgrade, then open Shape to create and ratify product.md before Map or any substantial work."
      : "Next: there are no upgrade changes to commit; open Shape to create and ratify product.md before Map or any substantial work.";
  }
  if (assessment && assessment.state === "pending") {
    return hasChanges
      ? `Next: review the reported paths and complete diff, commit the upgrade, then complete ${ASSESSMENT_RECORD} by following “Finish an upgrade” in AGENTS.md.`
      : `Next: there are no upgrade changes to commit; complete ${ASSESSMENT_RECORD} by following “Finish an upgrade” in AGENTS.md.`;
  }
  if (assessment && assessment.route === "Shape") {
    return hasChanges
      ? "Next: review the reported paths and complete diff, commit the upgrade, then continue Shape from state.md."
      : "Next: there are no upgrade changes to commit; continue Shape from state.md.";
  }
  if (assessment && assessment.route === "Map") {
    return hasChanges
      ? "Next: review the reported paths and complete diff, commit the upgrade, then continue Map from state.md."
      : "Next: there are no upgrade changes to commit; continue Map from state.md.";
  }
  if (assessment && assessment.route === "resume") {
    return hasChanges
      ? `Next: review the reported paths and complete diff, commit the upgrade, then resume ${assessment.livePiece} from state.md.`
      : `Next: there are no upgrade changes to commit; resume ${assessment.livePiece} from state.md.`;
  }
  return hasChanges
    ? "Next: review the reported paths and complete diff, commit the upgrade, then resume current work from state.md."
    : "Next: there are no upgrade changes to commit; resume current work from state.md.";
}

if (cmd === "install") {
  if (!fs.existsSync(target)) die(`no such directory: ${target}`);
  if (!fs.existsSync(path.join(target, ".git"))) die(`not a git repository: ${target} (git init first)`);
  if (path.resolve(SRC) === target) die("refusing: that's the kernel repo itself");
  if (fs.existsSync(path.join(target, "AGENTS.md")) || fs.existsSync(path.join(target, "CLAUDE.md")))
    die(`refusing: ${target} already carries agent instructions.\n` +
        `If it's a Speck Next repo, use: npx github:Keegil/speck-next upgrade\n` +
        `If it's an old-Speck or custom repo, converting it is a later version's job. Nothing was touched.`);
  const provenance = copySurface();
  ensureMap();
  writeMarker(null, provenance, null);
  const files = installedFiles();
  console.log(`Installed Speck Next ${versionWithProvenance(VERSION, provenance.sourceCheckout, provenance.methodSurfaceSha256)} into ${target} — ${files.length} files on disk (method files, the version marker, and an empty starter map).`);
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
  const migration = planProductTeamAssessment(source, prior);
  const provenance = copySurface();
  retireReplacedSkills();
  ensureMap();
  applyProductTeamAssessment(migration);
  writeMarker(prior, provenance, migration.assessmentRecord);
  const changes = gitChanges();
  const diff = gitDiff();
  const from = versionWithProvenance(prior.version, markerSourceCheckout(prior), prior.methodSurfaceSha256 || null);
  const to = versionWithProvenance(VERSION, provenance.sourceCheckout, provenance.methodSurfaceSha256);
  console.log(`Upgraded Speck Next ${from} -> ${to} in ${target}.`);
  console.log(migration.message);
  console.log(changes
    ? `Working-tree changes across the complete installed surface plus product.md:\n${changes}`
    : "Working-tree changes across the complete installed surface plus product.md: none.");
  console.log(diff
    ? `Complete installed-surface plus product.md diff (working tree against HEAD):\n${diff}`
    : "Complete installed-surface plus product.md diff: empty.");
  console.log(upgradeNext(changes, diff, migration.assessment));
} else {
  console.log(`speck-next v${VERSION} — a small kernel for building great products and proving them by running them.

  npx github:Keegil/speck-next install [dir]   place the method into a fresh git repo (default: current dir)
  npx github:Keegil/speck-next upgrade [dir]   refresh the method files in a Speck Next repo

The method itself is one page: AGENTS.md. Everything else is five skills your agent loads on demand, and six file skeletons in templates/.
Pin a released tag, e.g.: npx -y github:Keegil/speck-next#v5.0.0 install  (all tags: github.com/Keegil/speck-next/tags)`);
}
