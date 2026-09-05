#!/usr/bin/env node
// Speck Next installer/upgrader. Run from anywhere:
//   npx github:Keegil/speck-next install [dir]
//   npx github:Keegil/speck-next upgrade [dir]
//   npx github:Keegil/speck-next upgrade [dir] --open-assessment
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { spawnSync } = require("child_process");

const SRC = path.join(__dirname, "..");
const VERSION = require(path.join(SRC, "package.json")).version;
const SURFACE = ["AGENTS.md", "CLAUDE.md", path.join(".claude", "skills"), "templates"];
const MARKER = path.join(".claude", "speck-next.json");
const BASE_REPORTED_PATHS = [...SURFACE, MARKER, "map.md", "product.md"];
const STALE_SKILL = path.join(".claude", "skills", "independent-review");
const PRESERVE_ROOT_PREFIX = ".speck-next-preserved";
const MAP_TEMPLATE = "# Map\n\nNo map yet. When shaping closes, the ordered build pieces land here — each naming what it serves and which shaped material it consumes, exactly one live, unconsumed shaped material listed at the bottom.\n";
const RC1_UNIVERSAL_STATUS = "**Upgrade status:** Unassessed under v6. Historical work keeps its original evidence and is not backfilled as role-shaped. Before the next substantial piece, Product, Business, Experience, and Engineering assess this product in four separate contexts. Reopen Shape only if that assessment finds a wrong promise.";
const REJECTED_RC2_STATUS = "**Upgrade status:** Unassessed under Speck Next 6.0.0-rc.2. Historical work keeps its original evidence and is not backfilled as role-shaped. Before the next substantial piece, separate Product, Business, Experience, and Engineering carriers assess the existing product and current map once. Business and Experience then define their observable call conditions, trusted evidence, expiry, and material changes. Reopen Shape only for a wrong promise and Map only for a wrong piece or order.";
const ASSESSMENT_HEADING = "## Speck Next upgrade assessment";
const ASSESSMENT_RECORD = "work/product-team-assessment.md";
const ASSESSMENT_RECORD_LINE = `**Record:** \`${ASSESSMENT_RECORD}\``;
const ASSESSMENT_PENDING = "**Speck Next upgrade assessment:** pending";
const PRODUCT_TEAM_HEADING = "## Product team";
const PRODUCT_TEAM_ROLES = ["Product", "Business", "Experience", "Engineering"];
const CONDITIONAL_ROLE_FIELDS = [
  "Protects", "Call when", "May stay out when", "Evidence expires", "Material changes",
];
const TRIVIAL_PRODUCT_TEAM_VALUES = new Set(["tbd", "todo", "none", "n/a", "placeholder"]);
const ASSESSMENT_BLOCK = `${ASSESSMENT_HEADING}\n\n${ASSESSMENT_PENDING}\n${ASSESSMENT_RECORD_LINE}\n`;
const RECOVERABLE_FIELDLESS_VERSION = "6.0.0-rc.2";
const NULL_DEVICE = process.platform === "win32" ? "NUL" : "/dev/null";
const REPORT_TIMEOUT_MS = 10000;
const GENERATED_FILE_MODE = 0o644;

function die(msg) { console.error(msg); process.exit(1); }
function transactionError(message) {
  const error = new Error(message);
  error.speckMessage = message;
  throw error;
}

function parseCli(argv) {
  const [command, ...args] = argv.slice(2);
  if (command === "--open-assessment")
    die("refusing: --open-assessment is available only with upgrade. No target was accessed and nothing was touched.");
  if (command && command.startsWith("-") && !["--help", "-h"].includes(command))
    die(`refusing: unknown option ${JSON.stringify(command)}. No target was accessed and nothing was touched.`);
  const paths = [];
  let openAssessment = false;
  for (const argument of args) {
    if (argument === "--open-assessment") {
      if (openAssessment)
        die("refusing: --open-assessment may appear only once. No target was accessed and nothing was touched.");
      openAssessment = true;
    } else if (argument.startsWith("-")) {
      die(`refusing: unknown option ${JSON.stringify(argument)}. No target was accessed and nothing was touched.`);
    } else {
      paths.push(argument);
    }
  }
  if (paths.length > 1)
    die("refusing: install and upgrade accept at most one target directory. No target was accessed and nothing was touched.");
  if (openAssessment && command !== "upgrade")
    die("refusing: --open-assessment is available only with upgrade. No target was accessed and nothing was touched.");
  return { command, target: path.resolve(paths[0] || "."), openAssessment };
}

const { command: cmd, target: requestedTarget, openAssessment } = parseCli(process.argv);
const targetDisplay = requestedTarget;
const target = (cmd === "install" || cmd === "upgrade") && fs.existsSync(requestedTarget)
  ? fs.realpathSync.native(requestedTarget)
  : requestedTarget;

function resolvedTarget() { return target; }

function sourceCommit() {
  const run = spawnSync("git", [
    "--no-pager",
    "--literal-pathspecs",
    "-c", "core.fsmonitor=false",
    "-c", "core.hooksPath=",
    "-c", "diff.external=",
    "rev-parse", "--short", "HEAD",
  ], {
    cwd: SRC,
    encoding: "utf8",
    env: gitReportEnv(),
    timeout: REPORT_TIMEOUT_MS,
  });
  if (run.error || run.signal || run.status !== 0 || String(run.stderr || "").trim()) return null;
  return String(run.stdout || "").trim() || null;
}

function normalizedRelative(relative) {
  return relative.split(path.sep).join("/");
}

function reportedPaths(extra = []) {
  return [...new Set([...BASE_REPORTED_PATHS, ...extra.map(normalizedRelative)])];
}

function lstatOptional(absolute) {
  try { return fs.lstatSync(absolute); }
  catch (error) {
    if (error.code === "ENOENT" || error.code === "ENOTDIR") return null;
    throw error;
  }
}

function statOptional(absolute) {
  try { return fs.statSync(absolute); }
  catch (error) {
    if (error.code === "ENOENT" || error.code === "ENOTDIR") return null;
    throw error;
  }
}

function readlinkOptional(absolute) {
  try { return fs.readlinkSync(absolute); }
  catch (error) {
    if (error.code === "EINVAL" || error.code === "ENOENT" || error.code === "ENOTDIR") return null;
    throw error;
  }
}

function pathInside(base, candidate) {
  const relative = path.relative(base, candidate);
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

function ensureTargetRelative(relative) {
  const root = resolvedTarget();
  const absolute = path.resolve(root, relative);
  if (!pathInside(root, absolute))
    transactionError(`refusing: internal write target escaped the selected product (${normalizedRelative(relative)}). Nothing was touched.`);
  return absolute;
}

function snapshotPathState(relative) {
  const absolute = ensureTargetRelative(relative);
  const stat = lstatOptional(absolute);
  if (!stat) return { state: "missing" };
  if (stat.isSymbolicLink()) return { state: "link", mode: stat.mode, target: fs.readlinkSync(absolute) };
  if (stat.isDirectory()) return { state: "dir", mode: stat.mode, entries: listTreeEntries(absolute) };
  if (stat.isFile()) return { state: "file", mode: stat.mode, bytes: fs.readFileSync(absolute) };
  return { state: `other:${stat.mode}` };
}

function listTreeEntries(root) {
  const entries = [];
  function visit(relative) {
    const absolute = relative ? path.join(root, relative) : root;
    const stat = fs.lstatSync(absolute);
    const label = relative ? normalizedRelative(relative) : ".";
    if (stat.isSymbolicLink()) {
      entries.push([label, `link:${stat.mode}`, Buffer.from(fs.readlinkSync(absolute))]);
      return;
    }
    if (stat.isDirectory()) {
      entries.push([label, `directory:${stat.mode}`, Buffer.alloc(0)]);
      for (const name of fs.readdirSync(absolute).sort()) visit(relative ? path.join(relative, name) : name);
      return;
    }
    if (stat.isFile()) {
      entries.push([label, `file:${stat.mode}`, fs.readFileSync(absolute)]);
      return;
    }
    entries.push([label, `other:${stat.mode}`, Buffer.alloc(0)]);
  }
  if (fs.existsSync(root)) visit("");
  return entries;
}

function snapshotRoot(relative, expectedKind) {
  const absolute = ensureTargetRelative(relative);
  const stat = lstatOptional(absolute);
  if (!stat) return { state: "missing" };
  if (stat.isSymbolicLink()) {
    const targetText = fs.readlinkSync(absolute);
    const followed = statOptional(absolute);
    if (!followed) return { state: "dangling-link", target: targetText };
    if (expectedKind === "dir") {
      return { state: followed.isDirectory() ? "linked-dir" : "linked-non-dir", target: targetText };
    }
    return { state: followed.isFile() ? "linked-file" : "linked-non-file", target: targetText };
  }
  if (expectedKind === "dir") {
    if (stat.isDirectory()) return { state: "dir" };
    return { state: stat.isFile() ? "file" : "non-directory-path" };
  }
  if (stat.isFile()) return { state: "file" };
  return { state: stat.isDirectory() ? "dir" : "non-file-path" };
}

function sameSnapshot(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

function applyMode(absolute, mode) {
  fs.chmodSync(absolute, mode & 0o7777);
}

function copyLogicalTree(source, destination, deferredDirectoryModes = null) {
  const stat = fs.lstatSync(source);
  if (stat.isSymbolicLink()) {
    ensureParent(destination);
    fs.symlinkSync(fs.readlinkSync(source), destination);
    return;
  }
  if (stat.isDirectory()) {
    fs.mkdirSync(destination, { recursive: true });
    for (const name of fs.readdirSync(source).sort())
      copyLogicalTree(path.join(source, name), path.join(destination, name), deferredDirectoryModes);
    if (deferredDirectoryModes) deferredDirectoryModes.set(destination, stat.mode);
    else applyMode(destination, stat.mode);
    return;
  }
  if (!stat.isFile())
    transactionError(`refusing: ${normalizedRelative(path.relative(resolvedTarget(), source))} contains an unsupported filesystem entry. Nothing was touched.`);
  ensureParent(destination);
  fs.copyFileSync(source, destination);
  applyMode(destination, stat.mode);
}

function safeLinkedDirectorySource(transaction, relative) {
  const absolute = ensureTargetRelative(relative);
  const resolved = fs.realpathSync.native(absolute);
  const product = resolvedTarget();
  if (pathInside(resolved, product) || pathInside(resolved, transaction.stageRoot) || pathInside(resolved, transaction.backupRoot))
    transactionError(`refusing: ${normalizedRelative(relative)} points into the selected product or its private transaction roots, so Speck Next cannot safely localize it. Nothing was touched.`);
  for (const root of transaction.primaryRoots) {
    const planned = ensureTargetRelative(root.relative);
    if (pathInside(planned, resolved) || pathInside(resolved, planned))
      transactionError(`refusing: ${normalizedRelative(relative)} points into another planned method root (${normalizedRelative(root.relative)}), so Speck Next cannot keep that linked destination unchanged. Nothing was touched.`);
  }
  return resolved;
}

function copyDirectoryChildren(source, destination, excluded = new Set(), deferredDirectoryModes = null) {
  for (const name of fs.readdirSync(source).sort()) {
    if (excluded.has(name)) continue;
    copyLogicalTree(path.join(source, name), path.join(destination, name), deferredDirectoryModes);
  }
}

function removeExisting(pathname) {
  const stat = lstatOptional(pathname);
  if (!stat) return;
  if (stat.isDirectory() && !stat.isSymbolicLink()) {
    makeTreeRemovable(pathname);
    fs.rmSync(pathname, { recursive: true, force: true });
    return;
  }
  fs.unlinkSync(pathname);
}

function makeTreeRemovable(pathname) {
  const stat = lstatOptional(pathname);
  if (!stat || stat.isSymbolicLink() || !stat.isDirectory()) return;
  applyMode(pathname, stat.mode | 0o700);
  for (const name of fs.readdirSync(pathname))
    makeTreeRemovable(path.join(pathname, name));
}

function renamePreservingMode(source, destination) {
  const stat = fs.lstatSync(source);
  const directoryMode = stat.isDirectory() && !stat.isSymbolicLink() ? stat.mode : null;
  if (directoryMode !== null) applyMode(source, directoryMode | 0o700);
  try {
    fs.renameSync(source, destination);
  } catch (error) {
    if (directoryMode !== null && lstatOptional(source)) applyMode(source, directoryMode);
    throw error;
  }
  if (directoryMode !== null) applyMode(destination, directoryMode);
}

function writeMarkerLast(bytes) {
  const marker = ensureTargetRelative(MARKER);
  const parent = path.dirname(marker);
  const parentStat = fs.lstatSync(parent);
  const parentMode = parentStat.mode;
  applyMode(parent, parentMode | 0o700);
  try {
    fs.writeFileSync(marker, bytes);
    applyMode(marker, GENERATED_FILE_MODE);
  } finally {
    applyMode(parent, parentMode);
  }
}

function hashPathTree(absolute) {
  const digest = crypto.createHash("sha256");
  function visit(current, relative) {
    const stat = fs.lstatSync(current);
    digest.update(normalizedRelative(relative));
    digest.update("\0");
    if (stat.isSymbolicLink()) {
      digest.update("link\0");
      digest.update(Buffer.from(fs.readlinkSync(current)));
      digest.update("\0");
      return;
    }
    if (stat.isDirectory()) {
      digest.update(`dir:${stat.mode}\0`);
      for (const name of fs.readdirSync(current).sort())
        visit(path.join(current, name), relative ? path.join(relative, name) : name);
      return;
    }
    if (stat.isFile()) {
      digest.update(`file:${stat.mode}\0`);
      digest.update(fs.readFileSync(current));
      digest.update("\0");
      return;
    }
    digest.update(`other:${stat.mode}\0`);
  }
  visit(absolute, "");
  return digest.digest("hex").slice(0, 12);
}

function ensureParent(absolute) {
  fs.mkdirSync(path.dirname(absolute), { recursive: true });
}

function preservedEntryName(relative) {
  const label = normalizedRelative(relative)
    .replace(/^\.+/, "")
    .replace(/[\\/]/g, "__")
    .replace(/[^A-Za-z0-9._-]+/g, "-");
  return label || "root";
}

function ensureStageDirectory(transaction, root, stagePath, relative) {
  const stat = lstatOptional(stagePath);
  if (!stat) {
    const targetRelative = path.join(root.relative, relative);
    const existing = snapshotRoot(targetRelative, "dir");
    if (existing.state.startsWith("linked-") || existing.state === "dangling-link")
      transaction.noteLocalization(targetRelative, existing.target || readlinkOptional(ensureTargetRelative(targetRelative)));
    fs.mkdirSync(stagePath, { recursive: true });
    if (existing.state === "dir") {
      const source = ensureTargetRelative(targetRelative);
      transaction.deferStageMode(stagePath, fs.lstatSync(source).mode);
      copyDirectoryChildren(source, stagePath, new Set(), transaction.stageDirectoryModes);
    }
    if (existing.state === "linked-dir") {
      const source = safeLinkedDirectorySource(transaction, targetRelative);
      transaction.deferStageMode(stagePath, fs.statSync(source).mode);
      copyDirectoryChildren(source, stagePath, new Set(), transaction.stageDirectoryModes);
    }
    return;
  }
  if (stat.isDirectory()) return;
  if (!stat.isSymbolicLink()) {
    transaction.planPreservation(path.join(root.relative, relative), stagePath);
    removeExisting(stagePath);
    fs.mkdirSync(stagePath, { recursive: true });
    return;
  }
  const targetRelative = path.join(root.relative, relative);
  const existing = snapshotRoot(targetRelative, "dir");
  transaction.noteLocalization(targetRelative, existing.target || readlinkOptional(ensureTargetRelative(targetRelative)));
  removeExisting(stagePath);
  fs.mkdirSync(stagePath, { recursive: true });
  if (existing.state === "linked-dir") {
    const source = safeLinkedDirectorySource(transaction, targetRelative);
    transaction.deferStageMode(stagePath, fs.statSync(source).mode);
    copyDirectoryChildren(source, stagePath, new Set(), transaction.stageDirectoryModes);
  }
}

function overlayFile(transaction, root, relative, entry) {
  const stagePath = path.join(root.stage, relative);
  const parent = path.dirname(relative);
  if (parent !== ".") {
    const parts = parent.split(path.sep);
    let walked = "";
    let current = root.stage;
    for (const part of parts) {
      walked = walked ? path.join(walked, part) : part;
      current = path.join(current, part);
      ensureStageDirectory(transaction, root, current, walked);
    }
  }
  const existing = lstatOptional(stagePath);
  if (existing) {
    if (existing.isSymbolicLink()) {
      transaction.noteLocalization(path.join(root.relative, relative), fs.readlinkSync(stagePath));
      removeExisting(stagePath);
    } else if (existing.isDirectory()) {
      transaction.planPreservation(path.join(root.relative, relative), stagePath);
      removeExisting(stagePath);
    } else {
      removeExisting(stagePath);
    }
  }
  ensureParent(stagePath);
  fs.writeFileSync(stagePath, entry.bytes);
  applyMode(stagePath, entry.mode);
}

function removeStagePath(transaction, root, relative) {
  const stagePath = path.join(root.stage, relative);
  const stat = lstatOptional(stagePath);
  if (stat && stat.isSymbolicLink())
    transaction.noteRetiredLink(path.join(root.relative, relative), fs.readlinkSync(stagePath));
  removeExisting(stagePath);
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
    const parts = relative.split(path.sep);
    let walked = root;
    for (let index = 0; index < parts.length - 1; index += 1) {
      walked = path.join(walked, parts[index]);
      const stat = fs.lstatSync(walked);
      if (!stat.isDirectory() || stat.isSymbolicLink())
        transactionError(`refusing: the staged method path ${normalizedRelative(relative)} is not a fully local directory chain. Nothing was touched.`);
    }
    const absolute = path.join(root, relative);
    const leaf = fs.lstatSync(absolute);
    if (!leaf.isFile() || leaf.isSymbolicLink())
      transactionError(`refusing: the staged method file ${normalizedRelative(relative)} is not a local regular file. Nothing was touched.`);
    digest.update(relative.split(path.sep).join("/"));
    digest.update("\0");
    digest.update(fs.readFileSync(absolute));
    digest.update("\0");
  }
  return digest.digest("hex");
}

function desiredWrites(migration, markerBytes) {
  const sourceCheckout = sourceCommit();
  const manifest = surfaceManifest(SRC);
  const methodSurfaceSha256 = surfaceDigest(SRC, manifest);
  const writes = new Map();
  for (const relative of manifest)
    writes.set(relative, {
      kind: "file",
      bytes: fs.readFileSync(path.join(SRC, relative)),
      mode: fs.statSync(path.join(SRC, relative)).mode,
      source: "method",
    });
  const targetMap = path.join(target, "map.md");
  const mapEntry = lstatOptional(targetMap);
  const linkedMapTarget = mapEntry && mapEntry.isSymbolicLink() ? statOptional(targetMap) : null;
  if (!mapEntry || (!mapEntry.isFile() && !(mapEntry.isSymbolicLink() && linkedMapTarget && linkedMapTarget.isFile())))
    writes.set("map.md", { kind: "file", bytes: Buffer.from(MAP_TEMPLATE), mode: GENERATED_FILE_MODE, source: "map" });
  if (migration.productContent !== null)
    writes.set("product.md", {
      kind: "file",
      bytes: Buffer.from(migration.productContent),
      mode: lstatOptional(path.join(target, "product.md")).mode,
      source: "product",
    });
  writes.set(MARKER, { kind: "file", bytes: markerBytes, mode: GENERATED_FILE_MODE, source: "marker" });
  return { sourceCheckout, manifest, methodSurfaceSha256, writes };
}

function candidateRoots(plan) {
  const roots = [
    { relative: "AGENTS.md", kind: "file" },
    { relative: "CLAUDE.md", kind: "file" },
    { relative: ".claude", kind: "dir" },
    { relative: "templates", kind: "dir" },
  ];
  if (plan.writes.has("map.md")) roots.push({ relative: "map.md", kind: "file" });
  if (plan.writes.has("product.md")) roots.push({ relative: "product.md", kind: "file" });
  return roots;
}

function plannedRoot(candidate) {
  const parts = candidate.relative.split(path.sep);
  let prefix = "";
  let firstMissing = null;
  for (let index = 0; index < parts.length; index += 1) {
    prefix = prefix ? path.join(prefix, parts[index]) : parts[index];
    const absolute = ensureTargetRelative(prefix);
    const stat = lstatOptional(absolute);
    if (!stat) {
      if (!firstMissing) firstMissing = prefix;
      continue;
    }
    const walkingFurther = index < parts.length - 1;
    if (stat.isSymbolicLink()) {
      const expectedKind = walkingFurther ? "dir" : candidate.kind;
      snapshotRoot(prefix, expectedKind);
      return { relative: prefix, kind: expectedKind };
    }
    if (walkingFurther && !stat.isDirectory())
      return { relative: prefix, kind: "dir" };
    if (!walkingFurther) {
      if (candidate.kind === "dir" && !stat.isDirectory())
        return { relative: prefix, kind: "dir" };
      if (candidate.kind === "file" && !stat.isFile())
        return { relative: prefix, kind: "file" };
    }
  }
  if (candidate.kind === "dir" && firstMissing)
    return { relative: firstMissing, kind: "dir" };
  return { relative: candidate.relative, kind: candidate.kind };
}

function localizeCarriedMapAlias(plan, roots) {
  if (plan.writes.has("map.md")) return false;
  const mapAbsolute = ensureTargetRelative("map.md");
  const mapEntry = lstatOptional(mapAbsolute);
  if (!mapEntry || !mapEntry.isSymbolicLink()) return false;
  const linkTarget = fs.readlinkSync(mapAbsolute);
  const linkedPath = path.resolve(path.dirname(mapAbsolute), linkTarget);
  const resolvedReferent = fs.realpathSync.native(mapAbsolute);
  for (const root of roots) {
    const planned = ensureTargetRelative(root.relative);
    const overlaps = [linkedPath, resolvedReferent].some(candidate =>
      pathInside(planned, candidate) || pathInside(candidate, planned)
    );
    if (!overlaps) continue;
    const logical = fs.statSync(mapAbsolute);
    plan.writes.set("map.md", {
      kind: "file",
      bytes: fs.readFileSync(mapAbsolute),
      mode: logical.mode,
      source: "carried-map",
      linkTarget,
      overlappingRoot: normalizedRelative(root.relative),
    });
    return true;
  }
  return false;
}

function markerSourceCheckout(marker) {
  return marker && (marker.sourceCheckout || marker.commit) || null;
}

function markerBytes(existing, provenance, assessmentRecord) {
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
  return Buffer.from(JSON.stringify(next, null, 2) + "\n");
}

function transactionPlan(existingMarker, migration) {
  const plan = desiredWrites(migration, Buffer.alloc(0));
  const marker = markerBytes(existingMarker, plan, migration.assessmentRecord);
  plan.writes.set(MARKER, { kind: "file", bytes: marker, source: "marker" });
  const primaryRoots = new Map();
  for (const candidate of candidateRoots(plan)) {
    const root = plannedRoot(candidate);
    const key = normalizedRelative(root.relative);
    if (!primaryRoots.has(key)) primaryRoots.set(key, { relative: root.relative, kind: root.kind, members: [] });
    primaryRoots.get(key).members.push(candidate.relative);
  }
  if (localizeCarriedMapAlias(plan, [...primaryRoots.values()])) {
    const mapRoot = plannedRoot({ relative: "map.md", kind: "file" });
    const key = normalizedRelative(mapRoot.relative);
    if (!primaryRoots.has(key)) primaryRoots.set(key, { ...mapRoot, members: [] });
    primaryRoots.get(key).members.push("map.md");
  }
  const markerRoot = plannedRoot({ relative: MARKER, kind: "file" });
  return {
    ...plan,
    markerBytes: marker,
    primaryRoots: [...primaryRoots.values()].sort((left, right) => normalizedRelative(left.relative).localeCompare(normalizedRelative(right.relative))),
    markerRoot,
  };
}

function gitReportEnv(reportIndex = null) {
  const env = { ...process.env };
  for (const key of Object.keys(env)) {
    if (key.startsWith("GIT_")) delete env[key];
  }
  env.GIT_OPTIONAL_LOCKS = "0";
  env.GIT_NO_LAZY_FETCH = "1";
  env.GIT_CONFIG_NOSYSTEM = "1";
  env.GIT_CONFIG_GLOBAL = NULL_DEVICE;
  env.GIT_PAGER = "cat";
  env.PAGER = "cat";
  env.LC_ALL = "C";
  if (reportIndex !== null) {
    if (!path.isAbsolute(reportIndex))
      transactionError("refusing: the private Git reporting index was not absolute. Nothing was touched.");
    env.GIT_INDEX_FILE = reportIndex;
  }
  return env;
}

function targetGitIndexPath() {
  const run = spawnSync("git", [
    "--no-pager",
    "--literal-pathspecs",
    "-c", "core.fsmonitor=false",
    "-c", "core.splitIndex=false",
    "-c", "core.hooksPath=",
    "-c", "diff.external=",
    "rev-parse", "--git-path", "index",
  ], {
    cwd: resolvedTarget(),
    encoding: "utf8",
    env: gitReportEnv(),
    timeout: REPORT_TIMEOUT_MS,
  });
  if (run.error || run.signal || run.status !== 0 || String(run.stderr || "").trim())
    transactionError("refusing: git index-path inspection failed before upgrade reporting. Nothing was touched.");
  let output = String(run.stdout || "");
  if (output.endsWith("\r\n")) output = output.slice(0, -2);
  else if (output.endsWith("\n")) output = output.slice(0, -1);
  if (!output || /[\r\n\0]/.test(output))
    transactionError("refusing: git returned an unreadable index path before upgrade reporting. Nothing was touched.");
  return path.isAbsolute(output) ? path.normalize(output) : path.resolve(resolvedTarget(), output);
}

let gitReportOverridesCache = null;

function gitReportOverrides(reportIndex) {
  if (gitReportOverridesCache) return gitReportOverridesCache;
  const args = [
    "--no-pager",
    "--literal-pathspecs",
    "-c", "core.fsmonitor=false",
    "-c", "core.splitIndex=false",
    "-c", "core.hooksPath=",
    "-c", "diff.external=",
    "config",
    "--null",
    "--name-only",
    "--get-regexp",
    "^filter\\..*\\.(clean|process|required)$",
  ];
  const run = spawnSync("git", args, {
    cwd: resolvedTarget(),
    encoding: "utf8",
    env: gitReportEnv(reportIndex),
    timeout: REPORT_TIMEOUT_MS,
  });
  if (run.error || String(run.stderr || "").trim())
    transactionError("refusing: git config inspection failed while securing upgrade reporting, so Speck Next stopped before reporting a partial result. Nothing was touched.");
  if (![0, 1].includes(run.status))
    transactionError("refusing: git config inspection failed while securing upgrade reporting, so Speck Next stopped before reporting a partial result. Nothing was touched.");
  const prefixes = new Set();
  for (const key of String(run.stdout || "").split("\0").filter(Boolean)) {
    const match = key.match(/^(filter\..*)\.(clean|process|required)$/);
    if (match) prefixes.add(match[1]);
  }
  gitReportOverridesCache = [...prefixes].sort().flatMap(prefix => [
    "-c", `${prefix}.clean=`,
    "-c", `${prefix}.process=`,
    "-c", `${prefix}.required=false`,
  ]);
  return gitReportOverridesCache;
}

function gitReportRun(args, label, reportIndex) {
  const run = spawnSync("git", [
    "--no-pager",
    "--literal-pathspecs",
    "-c", "core.fsmonitor=false",
    "-c", "core.splitIndex=false",
    "-c", "core.hooksPath=",
    "-c", "diff.external=",
    ...gitReportOverrides(reportIndex),
    ...args,
  ], {
    cwd: resolvedTarget(),
    encoding: "utf8",
    env: gitReportEnv(reportIndex),
    timeout: REPORT_TIMEOUT_MS,
  });
  if (run.error || run.signal || run.status === null || String(run.stderr || "").trim())
    transactionError(`refusing: git ${label} failed, so Speck Next rolled the upgrade back instead of reporting a partial result. Nothing was touched.`);
  return run;
}

function gitRead(args, label, reportIndex, allowedStatuses = [0]) {
  const run = gitReportRun(args, label, reportIndex);
  if (!allowedStatuses.includes(run.status))
    transactionError(`refusing: git ${label} failed, so Speck Next rolled the upgrade back instead of reporting a partial result. Nothing was touched.`);
  return String(run.stdout || "").trimEnd();
}

function trackedDiff(paths, reportIndex) {
  return gitRead(["diff", "--no-ext-diff", "--no-textconv", "--no-color", "--", ...paths], "diff", reportIndex);
}

function quotedDiffPath(relative) {
  return normalizedRelative(relative).replace(/\\/g, "\\\\").replace(/\t/g, "\\t").replace(/\n/g, "\\n");
}

function untrackedLinkDiff(relative) {
  const quoted = quotedDiffPath(relative);
  const targetText = fs.readlinkSync(ensureTargetRelative(relative));
  return [
    `diff --git a/${quoted} b/${quoted}`,
    "new file mode 120000",
    "--- /dev/null",
    `+++ b/${quoted}`,
    "@@ -0,0 +1 @@",
    `+${targetText}`,
  ].join("\n");
}

function porcelainZ(args, label, reportIndex, allowedStatuses = [0]) {
  const run = gitReportRun(args, label, reportIndex);
  if (!allowedStatuses.includes(run.status))
    transactionError(`refusing: git ${label} failed, so Speck Next rolled the upgrade back instead of reporting a partial result. Nothing was touched.`);
  return String(run.stdout || "");
}

function reportStatusEntries(paths, reportIndex) {
  const raw = porcelainZ(
    ["status", "--porcelain=v1", "-z", "--ignored=matching", "--untracked-files=all", "--", ...paths],
    "status", reportIndex
  );
  return raw.split("\0").filter(Boolean);
}

function untrackedPaths(paths, reportIndex) {
  const seen = new Set();
  const files = [];
  function addPhysicalLeaves(relative) {
    const absolute = ensureTargetRelative(relative.replace(/\/$/, ""));
    const stat = lstatOptional(absolute);
    if (!stat) return;
    if (stat.isDirectory() && !stat.isSymbolicLink()) {
      for (const name of fs.readdirSync(absolute).sort())
        addPhysicalLeaves(path.join(relative.replace(/\/$/, ""), name));
      return;
    }
    const normalized = normalizedRelative(relative.replace(/\/$/, ""));
    if (seen.has(normalized)) return;
    seen.add(normalized);
    files.push(normalized);
  }
  for (const entry of reportStatusEntries(paths, reportIndex)) {
    if (!/^(?:\?\?|!!) /.test(entry)) continue;
    const file = entry.slice(3);
    addPhysicalLeaves(file);
  }
  return files.sort();
}

function untrackedDiff(paths, reportIndex) {
  const parts = [];
  for (const file of untrackedPaths(paths, reportIndex)) {
    if (fs.lstatSync(ensureTargetRelative(file)).isSymbolicLink()) {
      parts.push(untrackedLinkDiff(file));
      continue;
    }
    const run = gitReportRun(["diff", "--no-index", "--no-ext-diff", "--no-textconv", "--no-color", "--", "/dev/null", file], "diff --no-index", reportIndex);
    if (![0, 1].includes(run.status))
      transactionError("refusing: git diff --no-index failed while reporting untracked upgrade files, so Speck Next rolled the upgrade back instead of reporting a partial result. Nothing was touched.");
    if (run.status === 0) continue;
    const addition = String(run.stdout || "");
    if (!addition.trim())
      transactionError("refusing: git diff --no-index returned no readable output for an untracked upgrade file, so Speck Next rolled the upgrade back instead of reporting a partial result. Nothing was touched.");
    parts.push(addition.trim());
  }
  return parts.join("\n");
}

function gitChanges(paths, reportIndex) {
  return porcelainZ(
    ["status", "--porcelain=v1", "--ignored=matching", "--untracked-files=all", "--", ...paths],
    "status", reportIndex
  ).trimEnd();
}

function gitDiff(paths, reportIndex) {
  const parts = [];
  const tracked = trackedDiff(paths, reportIndex);
  if (tracked) parts.push(tracked);
  const untracked = untrackedDiff(paths, reportIndex);
  if (untracked) parts.push(untracked);
  return parts.join("\n");
}

function installEntries(root, extra = []) {
  const files = [];
  function visit(relative) {
    const absolute = path.join(root, relative);
    const stat = lstatOptional(absolute);
    if (!stat) return;
    if (stat.isDirectory() && !stat.isSymbolicLink()) {
      for (const name of fs.readdirSync(absolute).sort()) visit(path.join(relative, name));
      return;
    }
    files.push(normalizedRelative(relative));
  }
  for (const relative of ["AGENTS.md", "CLAUDE.md", ".claude", "templates", "map.md", ...extra])
    visit(relative);
  return [...new Set(files)].sort();
}

function buildStageRoot(transaction, root) {
  const stagePath = path.join(transaction.stageRoot, root.relative);
  const existing = snapshotRoot(root.relative, root.kind);
  root.before = existing;
  root.beforePath = snapshotPathState(root.relative);
  root.stage = stagePath;
  if (root.kind === "file") {
    const entry = transaction.writes.get(root.relative);
    if (!entry) transactionError(`refusing: internal file plan missing ${normalizedRelative(root.relative)}. Nothing was touched.`);
    if (existing.state.startsWith("linked-") || existing.state === "dangling-link")
      transaction.noteLocalization(
        root.relative,
        entry.linkTarget || existing.target || readlinkOptional(ensureTargetRelative(root.relative)),
        entry.source === "carried-map" ? { kind: "carried-map", overlappingRoot: entry.overlappingRoot } : {}
      );
    else if (existing.state === "dir" || existing.state === "non-file-path")
      transaction.planPreservation(root.relative, ensureTargetRelative(root.relative));
    ensureParent(stagePath);
    fs.writeFileSync(stagePath, entry.bytes);
    applyMode(stagePath, entry.mode);
    return;
  }
  fs.mkdirSync(stagePath, { recursive: true });
  if (existing.state.startsWith("linked-") || existing.state === "dangling-link")
    transaction.noteLocalization(root.relative, existing.target || readlinkOptional(ensureTargetRelative(root.relative)));
  else if (existing.state === "file" || existing.state === "non-directory-path")
    transaction.planPreservation(root.relative, ensureTargetRelative(root.relative));
  let logicalSource = null;
  if (existing.state === "dir") logicalSource = ensureTargetRelative(root.relative);
  if (existing.state === "linked-dir") logicalSource = safeLinkedDirectorySource(transaction, root.relative);
  if (logicalSource) {
    transaction.deferStageMode(
      stagePath,
      (existing.state === "dir" ? fs.lstatSync(logicalSource) : fs.statSync(logicalSource)).mode
    );
    copyDirectoryChildren(logicalSource, stagePath, new Set(), transaction.stageDirectoryModes);
  }
  if (root.relative === ".claude" && (existing.state === "dir" || existing.state === "linked-dir")) {
    const markerLeaf = snapshotRoot(MARKER, "file");
    if (markerLeaf.state.startsWith("linked-") || markerLeaf.state === "dangling-link")
      transaction.noteLocalization(MARKER, markerLeaf.target || readlinkOptional(ensureTargetRelative(MARKER)));
    else if (markerLeaf.state === "dir" || markerLeaf.state === "non-file-path")
      transaction.planPreservation(MARKER, path.join(stagePath, path.basename(MARKER)));
    removeExisting(path.join(stagePath, path.basename(MARKER)));
  }
  for (const [relative, entry] of transaction.writes) {
    if (relative === MARKER) continue;
    if (!relative.startsWith(root.relative + path.sep) && relative !== root.relative) continue;
    const child = relative === root.relative ? "" : path.relative(root.relative, relative);
    overlayFile(transaction, root, child, entry);
  }
  const retired = [STALE_SKILL].filter(relative =>
    relative.startsWith(root.relative + path.sep) || relative === root.relative
  );
  for (const relative of retired) {
    const child = relative === root.relative ? "" : path.relative(root.relative, relative);
    if (child) removeStagePath(transaction, root, child);
  }
  transaction.applyStageModes(stagePath);
}

function Transaction(plan) {
  this.primaryRoots = plan.primaryRoots.map(root => ({ ...root }));
  this.markerRoot = { relative: plan.markerRoot.relative, kind: plan.markerRoot.kind };
  this.writes = plan.writes;
  this.manifest = plan.manifest;
  this.methodSurfaceSha256 = plan.methodSurfaceSha256;
  this.sourceCheckout = plan.sourceCheckout;
  this.markerBytes = plan.markerBytes;
  const root = resolvedTarget();
  const parent = path.dirname(root);
  const rootDev = fs.statSync(root).dev;
  const parentDev = fs.statSync(parent).dev;
  const transactionParent = rootDev === parentDev ? parent : root;
  this.transactionRoot = fs.mkdtempSync(path.join(transactionParent, `.${path.basename(root)}.speck-next-transaction-`));
  try {
    if (fs.statSync(this.transactionRoot).dev !== rootDev)
      transactionError("refusing: Speck Next could not stage the upgrade on the selected product's filesystem. Nothing was touched.");
    this.stageRoot = path.join(this.transactionRoot, "stage");
    this.backupRoot = path.join(this.transactionRoot, "backup");
    this.preserveStageRoot = path.join(this.transactionRoot, "preserve");
    fs.mkdirSync(this.stageRoot, { recursive: true });
    fs.mkdirSync(this.backupRoot, { recursive: true });
    fs.mkdirSync(this.preserveStageRoot, { recursive: true });
  } catch (error) {
    removeExisting(this.transactionRoot);
    throw error;
  }
  this.replacedLinks = [];
  this.replacedLinkSet = new Set();
  this.retiredLinks = [];
  this.retiredLinkSet = new Set();
  this.preserved = [];
  this.preservedSet = new Set();
  this.preserveRoot = null;
  this.applied = [];
  this.appliedPreservations = [];
  this.stageDirectoryModes = new Map();
  this.markerCovered = this.primaryRoots.some(root => MARKER === root.relative || MARKER.startsWith(root.relative + path.sep));
  this.markerBefore = null;
  this.markerBeforePath = null;
  this.reportIndex = null;
}

Transaction.prototype.prepareReportIndex = function prepareReportIndex() {
  const source = targetGitIndexPath();
  const existing = lstatOptional(source);
  if (existing && (existing.isSymbolicLink() || !existing.isFile()))
    transactionError("refusing: the repository's Git index is not a regular file, so Speck Next cannot report this upgrade safely. Nothing was touched.");
  this.reportIndex = path.join(this.transactionRoot, "report-index");
  if (!existing) return;
  try {
    fs.copyFileSync(source, this.reportIndex);
    applyMode(this.reportIndex, existing.mode);
  } catch {
    transactionError("refusing: Speck Next could not copy the Git index into its private reporting transaction. Nothing was touched.");
  }
};

Transaction.prototype.deferStageMode = function deferStageMode(absolute, mode) {
  this.stageDirectoryModes.set(absolute, mode);
};

Transaction.prototype.applyStageModes = function applyStageModes(root) {
  const entries = [...this.stageDirectoryModes.entries()]
    .filter(([absolute]) => pathInside(root, absolute))
    .sort(([left], [right]) => right.split(path.sep).length - left.split(path.sep).length);
  for (const [absolute, mode] of entries) {
    const stat = lstatOptional(absolute);
    if (stat && stat.isDirectory() && !stat.isSymbolicLink()) applyMode(absolute, mode);
    this.stageDirectoryModes.delete(absolute);
  }
};

Transaction.prototype.noteLocalization = function noteLocalization(relative, linkTarget, details = {}) {
  const key = normalizedRelative(relative);
  if (this.replacedLinkSet.has(key)) return;
  this.replacedLinkSet.add(key);
  this.replacedLinks.push({ relative: key, target: linkTarget || "(dangling link)", ...details });
};

Transaction.prototype.noteRetiredLink = function noteRetiredLink(relative, linkTarget) {
  const key = normalizedRelative(relative);
  if (this.retiredLinkSet.has(key)) return;
  this.retiredLinkSet.add(key);
  this.retiredLinks.push({ relative: key, target: linkTarget || "(dangling link)" });
};

Transaction.prototype.planPreservation = function planPreservation(relative) {
  const key = normalizedRelative(relative);
  if (this.preservedSet.has(key)) return;
  const source = arguments.length > 1 ? arguments[1] : ensureTargetRelative(relative);
  const stat = lstatOptional(source);
  if (!stat || stat.isSymbolicLink()) return;
  const preserveSource = path.join(this.preserveStageRoot, relative);
  ensureParent(preserveSource);
  copyLogicalTree(source, preserveSource);
  this.preservedSet.add(key);
  this.preserved.push({
    relative: key,
    entryName: `${preservedEntryName(relative)}--${hashPathTree(source)}`,
    destinationRelative: null,
    preserveSource,
  });
};

Transaction.prototype.choosePreserveRoot = function choosePreserveRoot() {
  if (!this.preserved.length) return;
  for (let index = 1; index < 1000; index += 1) {
    const relative = index === 1 ? PRESERVE_ROOT_PREFIX : `${PRESERVE_ROOT_PREFIX}-${index}`;
    const absolute = ensureTargetRelative(relative);
    const stat = lstatOptional(absolute);
    if (stat && (stat.isSymbolicLink() || !stat.isDirectory())) continue;
    let usable = true;
    for (const entry of this.preserved) {
      if (lstatOptional(path.join(absolute, entry.entryName))) {
        usable = false;
        break;
      }
    }
    if (!usable) continue;
    this.preserveRoot = {
      relative,
      beforePath: snapshotPathState(relative),
      existed: Boolean(stat && stat.isDirectory()),
    };
    for (const entry of this.preserved)
      entry.destinationRelative = normalizedRelative(path.join(relative, entry.entryName));
    return;
  }
  transactionError("refusing: Speck Next could not find a usable .speck-next-preserved root for incompatible owner bytes. Nothing was touched.");
};

Transaction.prototype.prepare = function prepare() {
  for (const root of this.primaryRoots) buildStageRoot(this, root);
  if (!this.markerCovered) {
    this.markerBefore = snapshotRoot(MARKER, "file");
    this.markerBeforePath = snapshotPathState(MARKER);
    if (this.markerBefore.state.startsWith("linked-") || this.markerBefore.state === "dangling-link")
      this.noteLocalization(MARKER, this.markerBefore.target || readlinkOptional(ensureTargetRelative(MARKER)));
    else if (this.markerBefore.state === "dir" || this.markerBefore.state === "non-file-path")
      this.planPreservation(MARKER);
  }
  this.choosePreserveRoot();
  const stagedDigest = surfaceDigest(this.stageRoot, this.manifest);
  if (stagedDigest !== this.methodSurfaceSha256)
    transactionError("refusing: the staged method bytes do not match the source method surface. Nothing was touched.");
  if (this.writes.has("product.md")) {
    const stagedProduct = fs.readFileSync(path.join(this.stageRoot, "product.md"));
    if (!stagedProduct.equals(this.writes.get("product.md").bytes))
      transactionError("refusing: the staged product bytes do not match the planned product migration. Nothing was touched.");
  }
  if (this.writes.has("map.md")) {
    const stagedMap = fs.readFileSync(path.join(this.stageRoot, "map.md"));
    if (!stagedMap.equals(this.writes.get("map.md").bytes))
      transactionError("refusing: the staged map bytes do not match the planned migration. Nothing was touched.");
  }
};

Transaction.prototype.planSummary = function planSummary() {
  return {
    roots: this.primaryRoots.map(root => ({
      relative: normalizedRelative(root.relative),
      kind: root.kind,
      before: root.before ? root.before.state : snapshotRoot(root.relative, root.kind).state,
    })),
    markerRoot: { relative: normalizedRelative(this.markerRoot.relative), kind: this.markerRoot.kind },
    localizedLinks: this.replacedLinks.slice(),
    retiredLinks: this.retiredLinks.slice(),
    preserved: this.preserved.slice(),
  };
};

Transaction.prototype.revalidate = function revalidate() {
  for (const root of this.primaryRoots) {
    const current = snapshotPathState(root.relative);
    if (!sameSnapshot(current, root.beforePath))
      transactionError(`refusing: ${normalizedRelative(root.relative)} changed while Speck Next was staging the upgrade, so it stopped before replacing anything. Nothing was touched.`);
  }
  if (!this.markerCovered) {
    const currentMarker = snapshotPathState(MARKER);
    if (!sameSnapshot(currentMarker, this.markerBeforePath))
      transactionError(`refusing: ${normalizedRelative(MARKER)} changed while Speck Next was staging the upgrade, so it stopped before replacing anything. Nothing was touched.`);
  }
  if (this.preserveRoot) {
    const currentPreserveRoot = snapshotPathState(this.preserveRoot.relative);
    if (!sameSnapshot(currentPreserveRoot, this.preserveRoot.beforePath))
      transactionError(`refusing: ${normalizedRelative(this.preserveRoot.relative)} changed while Speck Next was staging the upgrade, so it stopped before replacing anything. Nothing was touched.`);
  }
};

Transaction.prototype.swapRoot = function swapRoot(relative) {
  const absolute = ensureTargetRelative(relative);
  const backup = path.join(this.backupRoot, relative);
  fs.mkdirSync(path.dirname(backup), { recursive: true });
  if (lstatOptional(absolute)) {
    renamePreservingMode(absolute, backup);
    this.applied.push({ relative, backup, existed: true });
  } else {
    this.applied.push({ relative, backup, existed: false });
  }
};

Transaction.prototype.apply = function apply() {
  this.revalidate();
  for (let index = 0; index < this.primaryRoots.length; index += 1) {
    const root = this.primaryRoots[index];
    this.swapRoot(root.relative);
    const stagePath = path.join(this.stageRoot, root.relative);
    fs.mkdirSync(path.dirname(ensureTargetRelative(root.relative)), { recursive: true });
    renamePreservingMode(stagePath, ensureTargetRelative(root.relative));
  }
  if (!this.markerCovered)
    this.swapRoot(MARKER);
  if (this.preserveRoot) {
    const preserveRootAbsolute = ensureTargetRelative(this.preserveRoot.relative);
    if (!this.preserveRoot.existed) fs.mkdirSync(preserveRootAbsolute, { recursive: true });
    for (const entry of this.preserved) {
      if (!lstatOptional(entry.preserveSource))
        transactionError(`refusing: ${entry.relative} disappeared before it could be preserved. Nothing was touched.`);
      const destination = ensureTargetRelative(entry.destinationRelative);
      ensureParent(destination);
      renamePreservingMode(entry.preserveSource, destination);
      this.appliedPreservations.push({ source: entry.preserveSource, destination });
    }
  }
  ensureParent(ensureTargetRelative(MARKER));
  writeMarkerLast(this.markerBytes);
  this.appliedMarkerOnly = !this.markerCovered;
};

Transaction.prototype.rollback = function rollback() {
  for (let index = this.appliedPreservations.length - 1; index >= 0; index -= 1) {
    const entry = this.appliedPreservations[index];
    fs.mkdirSync(path.dirname(entry.source), { recursive: true });
    if (lstatOptional(entry.destination)) renamePreservingMode(entry.destination, entry.source);
  }
  if (this.preserveRoot && !this.preserveRoot.existed) {
    const absolute = ensureTargetRelative(this.preserveRoot.relative);
    if (lstatOptional(absolute) && fs.readdirSync(absolute).length === 0) fs.rmdirSync(absolute);
  }
  this.appliedPreservations = [];
  for (let index = this.applied.length - 1; index >= 0; index -= 1) {
    const entry = this.applied[index];
    const absolute = ensureTargetRelative(entry.relative);
    removeExisting(absolute);
    if (entry.existed) {
      fs.mkdirSync(path.dirname(absolute), { recursive: true });
      renamePreservingMode(entry.backup, absolute);
    }
  }
  this.applied = [];
  this.cleanup();
};

Transaction.prototype.cleanup = function cleanup() {
  let failure = null;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    try {
      removeExisting(this.transactionRoot);
      return;
    } catch (error) {
      if (!lstatOptional(this.transactionRoot)) return;
      failure = error;
    }
  }
  throw failure;
};

function applyInstalledSurface(existingMarker, migration) {
  const plan = transactionPlan(existingMarker, migration);
  const transaction = new Transaction(plan);
  try {
    const productExists = plan.writes.has("product.md") || entryExists(path.join(target, "product.md"));
    transaction.prepareReportIndex();
    transaction.prepare();
    transaction.apply();
    const installedEntries = installEntries(
      resolvedTarget(), transaction.replacedLinks.map(link => link.relative)
    );
    const extraReportPaths = transaction.replacedLinks.map(link => link.relative);
    if (transaction.preserveRoot) extraReportPaths.push(transaction.preserveRoot.relative);
    const reportPaths = reportedPaths(extraReportPaths);
    const changes = gitChanges(reportPaths, transaction.reportIndex);
    const diff = gitDiff(reportPaths, transaction.reportIndex);
    transaction.cleanup();
    return {
      sourceCheckout: transaction.sourceCheckout,
      methodSurfaceSha256: transaction.methodSurfaceSha256,
      changes,
      diff,
      localizedLinks: transaction.replacedLinks,
      retiredLinks: transaction.retiredLinks,
      preserved: transaction.preserved,
      installedEntries,
      productExists,
    };
  } catch (error) {
    transaction.rollback();
    throw error;
  } finally {
    transaction.cleanup();
  }
}

function normalizedVersion(version) {
  return String(version || "").trim().replace(/^v/i, "");
}

function migrationSource(version) {
  const normalized = normalizedVersion(version);
  const match = normalized.match(/^(\d+)\.(\d+)\.(\d+)(?:-[0-9A-Za-z.-]+)?$/);
  if (!match) return "unknown";
  if (normalized === "6.0.0-rc.1") return "rc.1";
  return Number(match[1]) < 6 ? "pre-v6" : "current";
}

function backtickRunLength(line, column) {
  let end = column;
  while (line[end] === "`") end += 1;
  return end - column;
}

function escapedBacktickOpener(line, column) {
  let backslashes = 0;
  for (let index = column - 1; index >= 0 && line[index] === "\\"; index -= 1)
    backslashes += 1;
  return backslashes % 2 === 1;
}

const HTML_BLOCK_TAGS = "address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|nav|noframes|ol|optgroup|option|p|param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|track|ul";
const HTML_BLOCK_TAG = new RegExp(`^<\\/?(?:${HTML_BLOCK_TAGS})(?:[ \\t]|\\/?>|$)`, "i");

function startsNonCommentHtmlBlock(line) {
  const start = line.match(/^ {0,3}(.*)$/);
  if (!start || !start[1].startsWith("<") || start[1].startsWith("<!--")) return false;
  const text = start[1];
  return /^(?:<(?:script|pre|style|textarea)(?:[ \t]|>|$)|<\?|<![A-Z]|<!\[CDATA\[)/i.test(text) ||
    HTML_BLOCK_TAG.test(text);
}

function startsNewMarkdownBlock(line) {
  if (/^[ \t]*$/.test(line)) return true;
  if (/^(?: {4}| {0,3}\t)/.test(line)) return true;
  if (/^[ \t]*>/.test(line)) return true;
  if (/^ {0,3}(?:`{3,}|~{3,})/.test(line)) return true;
  if (/^ {0,3}#{1,6}(?:[ \t]+|$)/.test(line)) return true;
  if (/^ {0,3}(?:[-+*](?:[ \t]+|$)|\d{1,9}[.)](?:[ \t]+|$))/.test(line)) return true;
  if (/^ {0,3}(?:=+|-+)[ \t]*$/.test(line)) return true;
  if (/^ {0,3}(?:(?:\*[ \t]*){3,}|(?:_[ \t]*){3,}|(?:-[ \t]*){3,})$/.test(line)) return true;
  return startsNonCommentHtmlBlock(line);
}

function findBalancedCodeSpanEnd(lines, lineIndex, column, runLength, allowMultiline) {
  const endLine = allowMultiline ? lines.length : lineIndex + 1;
  for (let index = lineIndex; index < endLine; index += 1) {
    const line = lines[index];
    if (index !== lineIndex && startsNewMarkdownBlock(line)) return null;
    let cursor = index === lineIndex ? column + runLength : 0;
    while (cursor < line.length) {
      const tick = line.indexOf("`", cursor);
      if (tick === -1) break;
      const length = backtickRunLength(line, tick);
      if (length === runLength) return { line: index, column: tick + length };
      cursor = tick + length;
    }
  }
  return null;
}

function logicalLineRecords(content) {
  const records = [];
  let start = 0;
  for (let index = 0; index < content.length; index += 1) {
    let ending = "";
    if (content[index] === "\r") {
      ending = content[index + 1] === "\n" ? "\r\n" : "\r";
    } else if (content[index] === "\n") {
      ending = "\n";
    } else {
      continue;
    }
    records.push({ text: content.slice(start, index), ending });
    if (ending === "\r\n") index += 1;
    start = index + 1;
  }
  records.push({ text: content.slice(start), ending: "" });
  return records;
}

function joinLogicalLineRecords(records) {
  return records.map(record => record.text + record.ending).join("");
}

function activeMarkdownLines(content) {
  const records = logicalLineRecords(content);
  const lines = records.map(record => record.text);
  const active = Array(lines.length).fill(true);
  let fence = null;
  let htmlComment = false;
  let codeSpanEnd = null;
  for (let lineIndex = 0; lineIndex < lines.length; lineIndex += 1) {
    const line = lines[lineIndex];
    const marker = line.match(/^ {0,3}(`{3,}|~{3,})/);
    if (fence) {
      active[lineIndex] = false;
      if (marker && marker[1][0] === fence[0] && marker[1].length >= fence.length) fence = null;
      continue;
    }
    if (!htmlComment && /^[ \t]*>/.test(line)) {
      active[lineIndex] = false;
      continue;
    }
    if (!htmlComment && marker) {
      fence = marker[1];
      active[lineIndex] = false;
      continue;
    }
    let cursor = codeSpanEnd && codeSpanEnd.line === lineIndex ? codeSpanEnd.column : 0;
    if (codeSpanEnd) {
      active[lineIndex] = false;
      if (codeSpanEnd.line > lineIndex) continue;
      codeSpanEnd = null;
    }
    let commentTouched = htmlComment;
    while (true) {
      if (htmlComment) {
        const close = line.indexOf("-->", cursor);
        if (close === -1) break;
        htmlComment = false;
        commentTouched = true;
        cursor = close + 3;
      } else {
        const open = line.indexOf("<!--", cursor);
        const tick = line.indexOf("`", cursor);
        if (open === -1 && tick === -1) break;
        if (tick !== -1 && (open === -1 || tick < open)) {
          const length = backtickRunLength(line, tick);
          if (escapedBacktickOpener(line, tick)) {
            cursor = tick + length;
            continue;
          }
          // A real comment makes its whole line inactive. Inline code later on
          // that line may shield same-line literals, but cannot reach forward
          // and suppress evidence on the next clean line.
          const close = findBalancedCodeSpanEnd(
            lines, lineIndex, tick, length, !commentTouched
          );
          if (!close) {
            cursor = tick + length;
            continue;
          }
          if (close.line === lineIndex) {
            cursor = close.column;
            continue;
          }
          for (let touched = lineIndex; touched <= close.line; touched += 1)
            active[touched] = false;
          codeSpanEnd = close;
          break;
        }
        htmlComment = true;
        commentTouched = true;
        // Starting at the opener's dashes also handles the valid short forms
        // <!--> and <!---> while the first --> still closes ordinary comments.
        cursor = open + 2;
      }
    }
    if (commentTouched) active[lineIndex] = false;
  }
  if (htmlComment)
    assessmentError(
      "product.md contains an unclosed HTML comment, so its current assessment evidence cannot be determined.",
      "Next: close the HTML comment without changing the intended current assessment fields, then run the upgrade again."
    );
  return { records, lines, active };
}

function assessmentError(message, repair = "Next: restore consistent assessment evidence, then run the upgrade again.") {
  die(`refusing: ${message}\nNothing in the repository changed.\n${repair}`);
}

function unusableProductTeamValue(value) {
  const trimmed = value.replace(/\p{Default_Ignorable_Code_Point}/gu, "").trim();
  return !trimmed || /^\[[^\]]*\]$/.test(trimmed) ||
    TRIVIAL_PRODUCT_TEAM_VALUES.has(trimmed.toLowerCase());
}

function validateCompletedProductTeam(lines, active) {
  const headings = lines.flatMap((line, index) =>
    active[index] && line === PRODUCT_TEAM_HEADING ? [index] : []
  );
  if (headings.length !== 1) {
    const issue = headings.length === 0
      ? "Product team section: missing"
      : `Product team section: duplicate (${headings.length} current sections)`;
    incompleteProductTeamError([issue]);
  }

  const start = headings[0];
  let end = lines.length;
  for (let index = start + 1; index < lines.length; index += 1) {
    if (active[index] && /^##[ \t]+[^#]/.test(lines[index])) { end = index; break; }
  }

  const rows = Object.fromEntries(PRODUCT_TEAM_ROLES.map(role => [role, []]));
  const rolePattern = /^- \*\*(Product|Business|Experience|Engineering)\*\* —(.*)$/;
  for (let index = start + 1; index < end; index += 1) {
    if (!active[index]) continue;
    const match = lines[index].match(rolePattern);
    if (match) rows[match[1]].push(match[2].trim());
  }

  const issues = [];
  for (const role of ["Product", "Engineering"]) {
    if (rows[role].length === 0) issues.push(`${role}: responsibility missing`);
    else if (rows[role].length > 1) issues.push(`${role}: duplicate row`);
    else if (unusableProductTeamValue(rows[role][0]))
      issues.push(`${role}: responsibility unusable`);
  }

  const escapedLabels = CONDITIONAL_ROLE_FIELDS.map(label =>
    label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
  );
  const fieldPattern = new RegExp(
    `(?:^| · )(${escapedLabels.join("|")}):(.*?)(?= · (?:${escapedLabels.join("|")}):|$)`,
    "g"
  );
  for (const role of ["Business", "Experience"]) {
    if (rows[role].length === 0) {
      for (const field of CONDITIONAL_ROLE_FIELDS) issues.push(`${role}.${field}: missing`);
      continue;
    }
    if (rows[role].length > 1) {
      issues.push(`${role}: duplicate row`);
      continue;
    }
    const fields = Object.fromEntries(CONDITIONAL_ROLE_FIELDS.map(field => [field, []]));
    for (const match of rows[role][0].matchAll(fieldPattern)) fields[match[1]].push(match[2]);
    for (const field of CONDITIONAL_ROLE_FIELDS) {
      if (fields[field].length === 0) issues.push(`${role}.${field}: missing`);
      else if (fields[field].length > 1) issues.push(`${role}.${field}: duplicate`);
      else if (unusableProductTeamValue(fields[field][0]))
        issues.push(`${role}.${field}: unusable`);
    }
  }
  if (issues.length) incompleteProductTeamError(issues);
}

function incompleteProductTeamError(issues) {
  assessmentError(
    `the completed upgrade assessment cannot proceed because product.md does not contain one usable Product team definition:\n- ${issues.join("\n- ")}`,
    `Next: restore ${ASSESSMENT_PENDING}, finish product.md's Product team section with the existing four-role assessment evidence, commit product.md, ${ASSESSMENT_RECORD}, and state.md together, then run the upgrade again.`
  );
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
    if (assessment.route === "Map" || assessment.route === "resume")
      validateCompletedProductTeam(lines, active);
  }
  return assessment;
}

function removeGeneratedLine(content, generated) {
  const { records, lines, active } = activeMarkdownLines(content);
  const matches = lines.flatMap((line, index) => active[index] && line === generated ? [index] : []);
  if (matches.length > 1)
    assessmentError(`product.md contains ${matches.length} current copies of a generated upgrade status; its origin is ambiguous.`);
  if (matches.length === 0) return { content, removed: false };
  records[matches[0]].text = "";
  return { content: joinLogicalLineRecords(records), removed: true };
}

function appendAssessment(content) {
  const records = logicalLineRecords(content);
  const ending = records.reduce(
    (nearest, record) => record.ending || nearest,
    "\n"
  );
  const prefix = /[\r\n]$/.test(content) ? ending : ending + ending;
  const block = ASSESSMENT_BLOCK.replace(/\n/g, ending);
  return content + prefix + block;
}

function hasOwn(object, key) {
  return Object.prototype.hasOwnProperty.call(object, key);
}

function entryExists(absolute) {
  try {
    fs.lstatSync(absolute);
    return true;
  } catch (error) {
    if (error.code === "ENOENT") return false;
    throw error;
  }
}

function markerAssessmentDisposition(prior) {
  if (!hasOwn(prior, "upgradeAssessmentRecord")) return { known: false, record: null };
  const record = prior.upgradeAssessmentRecord;
  if (record !== null && record !== ASSESSMENT_RECORD)
    assessmentError(
      `the marker's upgradeAssessmentRecord is ${JSON.stringify(record)}; it must be null or ${JSON.stringify(ASSESSMENT_RECORD)}.`,
      "Next: restore the marker's explicit assessment disposition from version control, then run the upgrade again."
    );
  return { known: true, record };
}

function openAssessmentError() {
  assessmentError(
    "--open-assessment applies only to a current rc.2 repository whose marker is missing upgradeAssessmentRecord and whose regular product.md has no canonical or generated assessment evidence.",
    "Next: run the upgrade again without --open-assessment so the repository's existing evidence determines the route."
  );
}

function planProductTeamAssessment(source, prior, openAssessmentRequested) {
  const productPath = path.join(target, "product.md");
  const disposition = markerAssessmentDisposition(prior);
  if (!entryExists(productPath)) {
    if (disposition.record === ASSESSMENT_RECORD)
      assessmentError(
        `the marker requires ${ASSESSMENT_RECORD}, but product.md is missing.`,
        "Next: restore product.md and its canonical assessment block, then run the upgrade again."
      );
    if (openAssessmentRequested) openAssessmentError();
    return {
      message: "Product team migration: product.md is missing, so no product history or assessment was invented.",
      assessment: null,
      assessmentRecord: null,
      productContent: null,
    };
  }
  if (!fs.lstatSync(productPath).isFile())
    assessmentError(
      "product.md exists but is not a regular file.",
      "Next: restore product.md as a regular file, then run the upgrade again."
    );

  const original = fs.readFileSync(productPath, "utf8");
  const existing = parseAssessment(original, disposition.record === ASSESSMENT_RECORD);
  const rc1 = removeGeneratedLine(original, RC1_UNIVERSAL_STATUS);
  const rejectedRc2 = removeGeneratedLine(rc1.content, REJECTED_RC2_STATUS);
  const generatedAssessment = rc1.removed || rejectedRc2.removed;
  const recordPath = path.join(target, ASSESSMENT_RECORD);
  if (!existing && entryExists(recordPath))
    assessmentError(
      `${ASSESSMENT_RECORD} exists without a canonical assessment block in product.md.`,
      `Next: restore the matching canonical block or move the orphan record aside, then run the upgrade again.`
    );

  if (disposition.known && disposition.record === null) {
    if (existing || generatedAssessment || source !== "current")
      assessmentError(
        "the marker says no upgrade assessment applies, but the repository contains evidence that one is required.",
        "Next: restore the marker and product assessment evidence from the same successful upgrade, then run it again."
      );
    if (openAssessmentRequested) openAssessmentError();
    return {
      message: "Product team migration: not needed (the marker explicitly records that no one-time assessment applies).",
      assessment: null,
      assessmentRecord: null,
      productContent: null,
    };
  }

  if (existing) {
    if (openAssessmentRequested) openAssessmentError();
    return {
      message: `Product team migration: kept the explicit ${existing.state} upgrade assessment; product.md was unchanged.`,
      assessment: existing,
      assessmentRecord: ASSESSMENT_RECORD,
      productContent: null,
    };
  }

  const ambiguousCurrent = source === "current" && !disposition.known && !generatedAssessment;
  const recoverableAmbiguity = ambiguousCurrent &&
    normalizedVersion(prior.version) === RECOVERABLE_FIELDLESS_VERSION;
  if (openAssessmentRequested && !recoverableAmbiguity) openAssessmentError();

  if (ambiguousCurrent && !openAssessmentRequested)
    assessmentError(
      recoverableAmbiguity
        ? "this current rc.2 marker has no upgradeAssessmentRecord field and product.md has no surviving canonical or generated assessment evidence; Speck Next will not guess whether the one-time assessment applied."
        : `this ${JSON.stringify(prior.version)} marker has no upgradeAssessmentRecord field and product.md has no surviving canonical or generated assessment evidence; Speck Next will not guess whether the one-time assessment applied.`,
      recoverableAmbiguity
        ? "Next: run the upgrade again with --open-assessment to conservatively open the one-time assessment. Product work will not resume until that assessment records its route."
        : "Next: restore consistent assessment evidence for this version, then run the upgrade again."
    );

  const productContent = appendAssessment(rejectedRc2.content);
  const assessment = parseAssessment(productContent, true);
  let message = openAssessmentRequested
    ? "Product team migration: --open-assessment preserved every existing product byte and appended one explicit pending upgrade assessment."
    : "Product team migration: preserved historical product bytes and appended one explicit pending upgrade assessment.";
  if (!openAssessmentRequested && rc1.removed)
    message = "Product team migration: removed the exact generated rc.1 status and appended one explicit pending upgrade assessment; every other historical byte was preserved.";
  else if (!openAssessmentRequested && rejectedRc2.removed)
    message = "Product team migration: repaired the rejected rc.2 generated status into one explicit pending upgrade assessment; every other historical byte was preserved.";
  return { message, assessment, assessmentRecord: ASSESSMENT_RECORD, productContent };
}

function versionWithProvenance(version, sourceCheckout, methodSurfaceSha256) {
  return `${version} (source checkout ${sourceCheckout || "not recorded"}; method surface ${methodSurfaceSha256 ? `sha256:${methodSurfaceSha256}` : "not recorded"})`;
}

function localizationLines(localizedLinks) {
  return localizedLinks.map(link => {
    if (link.kind === "carried-map")
      return `Localized carried map.md into a local regular file; it previously pointed to ${JSON.stringify(link.target)}, and its logical contents and mode were made local before the overlapping method path ${link.overlappingRoot} changed.`;
    return `Localized linked path ${link.relative} into this repository; it previously pointed to ${JSON.stringify(link.target)} and that linked destination was left unchanged.`;
  });
}

function retiredLinkLines(retiredLinks) {
  return retiredLinks.map(link =>
    `Removed stale linked method path ${link.relative}; it previously pointed to ${JSON.stringify(link.target)} and that linked destination was left unchanged.`
  );
}

function preservationLines(preserved) {
  return preserved.map(entry =>
    `Preserved incompatible path ${entry.relative} at ${entry.destinationRelative}; the original path now carries the required local Speck Next entry.`
  );
}

function upgradeNext(changes, diff, assessment, productExists) {
  const hasChanges = Boolean(changes || diff);
  if (!productExists) {
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
  if (!fs.existsSync(path.join(target, ".git"))) die(`not a git repository: ${targetDisplay} (git init first)`);
  if (fs.realpathSync.native(SRC) === resolvedTarget()) die("refusing: that's the kernel repo itself");
  if (fs.existsSync(path.join(target, "AGENTS.md")) || fs.existsSync(path.join(target, "CLAUDE.md")))
    die(`refusing: ${targetDisplay} already carries agent instructions.\n` +
        `If it's a Speck Next repo, use: npx github:Keegil/speck-next upgrade\n` +
        `If it's an old-Speck or custom repo, converting it is a later version's job. Nothing was touched.`);
  try {
    const install = applyInstalledSurface(null, { message: "", assessment: null, assessmentRecord: null, productContent: null });
    for (const line of localizationLines(install.localizedLinks)) console.log(line);
    for (const line of retiredLinkLines(install.retiredLinks)) console.log(line);
    for (const line of preservationLines(install.preserved)) console.log(line);
    console.log(`Installed Speck Next ${versionWithProvenance(VERSION, install.sourceCheckout, install.methodSurfaceSha256)} into ${targetDisplay} — ${install.installedEntries.length} installed or carried-forward files on disk.`);
    console.log(`Installed paths:\n${install.installedEntries.join("\n")}`);
    console.log("Next: open an agent session there and say what you want to build — shaping starts in that conversation.");
  } catch (error) {
    die(error.speckMessage || error.message);
  }
} else if (cmd === "upgrade") {
  const markerPath = path.join(target, MARKER);
  if (!fs.existsSync(markerPath))
    die(`refusing: ${targetDisplay} doesn't look like a Speck Next repo (no ${MARKER}).\n` +
        `Fresh repo? Use: npx github:Keegil/speck-next install\n` +
        `Old-Speck repo? Converting it is a later version's job. Nothing was touched.`);
  let prior;
  try { prior = JSON.parse(fs.readFileSync(markerPath, "utf8")); }
  catch { die(`refusing: ${MARKER} is not valid JSON. Nothing was touched.`); }
  const source = migrationSource(prior.version);
  if (source === "unknown")
    die(`refusing: ${MARKER} carries an unknown version (${JSON.stringify(prior.version)}). Nothing was touched.`);
  const migration = planProductTeamAssessment(source, prior, openAssessment);
  try {
    const upgraded = applyInstalledSurface(prior, migration);
    const from = versionWithProvenance(prior.version, markerSourceCheckout(prior), prior.methodSurfaceSha256 || null);
    const to = versionWithProvenance(VERSION, upgraded.sourceCheckout, upgraded.methodSurfaceSha256);
    for (const line of localizationLines(upgraded.localizedLinks)) console.log(line);
    for (const line of retiredLinkLines(upgraded.retiredLinks)) console.log(line);
    for (const line of preservationLines(upgraded.preserved)) console.log(line);
    console.log(`Upgraded Speck Next ${from} -> ${to} in ${targetDisplay}.`);
    console.log(migration.message);
    console.log(upgraded.changes
      ? `Working-tree changes across the complete installed surface plus product.md:\n${upgraded.changes}`
      : "Working-tree changes across the complete installed surface plus product.md: none.");
    console.log(upgraded.diff
      ? `Complete installed-surface plus product.md diff (working tree against HEAD):\n${upgraded.diff}`
      : "Complete installed-surface plus product.md diff: empty.");
    console.log(upgradeNext(upgraded.changes, upgraded.diff, migration.assessment, upgraded.productExists));
  } catch (error) {
    die(error.speckMessage || error.message);
  }
} else {
  console.log(`speck-next v${VERSION} — a small kernel for building great products and proving them by running them.

  npx github:Keegil/speck-next install [dir]   place the method into a fresh git repo (default: current dir)
  npx github:Keegil/speck-next upgrade [dir]   refresh the method files in a Speck Next repo
  npx github:Keegil/speck-next upgrade [dir] --open-assessment
                                                conservatively open an ambiguous rc.2 assessment

The method itself is one page: AGENTS.md. Everything else is five skills your agent loads on demand, and six file skeletons in templates/.
Pin a released tag, e.g.: npx -y github:Keegil/speck-next#v5.0.0 install  (all tags: github.com/Keegil/speck-next/tags)`);
}
