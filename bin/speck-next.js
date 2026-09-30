#!/usr/bin/env node
// Speck Next installer/upgrader. Run from anywhere:
//   npx github:Keegil/speck-next install [dir]
//   npx github:Keegil/speck-next upgrade [dir]
//   npx github:Keegil/speck-next upgrade [dir] --open-assessment
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { spawnSync } = require("child_process");

// Toolkit setup is separate from project installation: it owns its cache only.
if (process.argv[2] === "tools") {
  require("./toolkit.js").main(process.argv.slice(3)).then(code => {
    process.exitCode = code ?? 0;
  }).catch(error => {
    console.error(error.message);
    process.exitCode = 1;
  });
  return;
}

const SRC = path.join(__dirname, "..");
const VERSION = require(path.join(SRC, "package.json")).version;
const SURFACE = ["AGENTS.md", "CLAUDE.md", path.join(".claude", "skills"), "templates"];
const CODEX_SKILLS_DIR = path.join(".agents", "skills");
const CODEX_ADAPTER_NAME = "speck-next";
const CODEX_ADAPTER_TARGET = "../../.claude/skills";
const MARKER = path.join(".claude", "speck-next.json");
const BASE_REPORTED_PATHS = [...SURFACE, MARKER, "map.md", "product.md"];
const STALE_SKILL = path.join(".claude", "skills", "independent-review");
const PRESERVE_ROOT_PREFIX = ".speck-next-preserved";
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
  if (openAssessment)
    die("refusing: --open-assessment was retired in Speck Next v7. Run upgrade without that flag; historical assessments and product findings are preserved without a mandatory reassessment. No target was accessed and nothing was touched.");
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

function realpathOptional(absolute) {
  try { return fs.realpathSync.native(absolute); }
  catch (error) {
    if (error.code === "ENOENT" || error.code === "ENOTDIR" || error.code === "ELOOP") return null;
    throw error;
  }
}

function codexAdapterPlan() {
  const skillsRoot = ensureTargetRelative(CODEX_SKILLS_DIR);
  const selectionBefore = snapshotPathState(CODEX_SKILLS_DIR);
  const agentsEntry = lstatOptional(ensureTargetRelative(".agents"));
  const rootEntry = lstatOptional(skillsRoot);
  const canonical = ensureTargetRelative(path.join(".claude", "skills"));
  const resolvedCanonical = realpathOptional(canonical);
  if (rootEntry && rootEntry.isSymbolicLink()) {
    const targetText = fs.readlinkSync(skillsRoot);
    const resolvedRoot = realpathOptional(skillsRoot);
    const linkedAncestor = Boolean(agentsEntry && agentsEntry.isSymbolicLink());
    const resolvedAfterAncestorLocalization = realpathOptional(
      path.resolve(path.dirname(skillsRoot), targetText)
    );
    const keepsCanonicalTarget = !linkedAncestor ||
      (resolvedAfterAncestorLocalization && resolvedAfterAncestorLocalization === resolvedCanonical);
    if (resolvedRoot && resolvedCanonical && resolvedRoot === resolvedCanonical &&
        pathInside(resolvedTarget(), resolvedRoot) && keepsCanonicalTarget) {
      return {
        relative: CODEX_SKILLS_DIR,
        target: targetText,
        wholeRoot: true,
        localizeAncestor: linkedAncestor,
        selectionBefore,
        selectedBefore: selectionBefore,
      };
    }
  }

  let names = new Set();
  const logicalRoot = statOptional(skillsRoot);
  if (logicalRoot && logicalRoot.isDirectory()) {
    try { names = new Set(fs.readdirSync(skillsRoot)); }
    catch {
      transactionError("refusing: Speck Next could not inspect .agents/skills before choosing its Codex discovery adapter. Nothing was touched.");
    }
    const adapters = [...names]
      .map(name => {
        const normalized = name.toLowerCase();
        if (normalized === CODEX_ADAPTER_NAME) return { name, order: 1 };
        const match = normalized.match(/^speck-next-((?:[2-9]|[1-9][0-9]+))$/);
        return match ? { name, order: Number(match[1]) } : null;
      })
      .filter(Boolean)
      .sort((left, right) => left.order - right.order ||
        (left.name < right.name ? -1 : left.name > right.name ? 1 : 0));
    for (const adapter of adapters) {
      const absolute = path.join(skillsRoot, adapter.name);
      const entry = lstatOptional(absolute);
      const targetText = entry && entry.isSymbolicLink() ? fs.readlinkSync(absolute) : null;
      const resolved = targetText === null ? null : realpathOptional(absolute);
      const exactTarget = targetText === CODEX_ADAPTER_TARGET;
      const containedCanonical = Boolean(resolved && resolvedCanonical &&
        resolved === resolvedCanonical && pathInside(resolvedTarget(), resolved));
      if (targetText !== null && (exactTarget || containedCanonical)) {
        const relative = path.join(CODEX_SKILLS_DIR, adapter.name);
        return {
          relative,
          target: targetText,
          wholeRoot: false,
          localizeAncestor: false,
          selectionBefore,
          selectedBefore: snapshotPathState(relative),
        };
      }
    }
  }

  let order = 1;
  let name = CODEX_ADAPTER_NAME;
  while (lstatOptional(path.join(skillsRoot, name))) {
    order += 1;
    name = `${CODEX_ADAPTER_NAME}-${order}`;
  }
  const relative = path.join(CODEX_SKILLS_DIR, name);
  return {
    relative,
    target: CODEX_ADAPTER_TARGET,
    wholeRoot: false,
    localizeAncestor: false,
    selectionBefore,
    selectedBefore: snapshotPathState(relative),
  };
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

function overlayEntry(transaction, root, relative, entry) {
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
      if (entry.kind !== "link")
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
  if (entry.kind === "link") {
    try { fs.symlinkSync(entry.target, stagePath, "dir"); }
    catch {
      transactionError(`refusing: Speck Next could not create its Codex discovery adapter ${normalizedRelative(path.join(root.relative, relative))}. Nothing was touched.`);
    }
    return;
  }
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

function verifyCodexAdapterLink(root, adapter, phase) {
  const absolute = path.join(root, adapter.relative);
  const entry = lstatOptional(absolute);
  const targetText = entry && entry.isSymbolicLink() ? fs.readlinkSync(absolute) : null;
  if (!entry || !entry.isSymbolicLink() || targetText !== adapter.target)
    transactionError(`refusing: the ${phase} Codex discovery adapter ${normalizedRelative(adapter.relative)} did not keep its selected symbolic-link target. Nothing was touched.`);
  return absolute;
}

function verifyCodexAdapter(root, adapter, phase) {
  const absolute = verifyCodexAdapterLink(root, adapter, phase);
  const targetText = fs.readlinkSync(absolute);
  const resolved = targetText === adapter.target ? realpathOptional(absolute) : null;
  const canonical = realpathOptional(path.join(root, ".claude", "skills"));
  if (!resolved || !canonical || resolved !== canonical || !pathInside(root, resolved)) {
    transactionError(`refusing: the ${phase} Codex discovery adapter ${normalizedRelative(adapter.relative)} did not resolve to the selected product's canonical .claude/skills directory. Nothing was touched.`);
  }
}

function desiredWrites(markerBytes) {
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
  const codexAdapter = codexAdapterPlan();
  if (!codexAdapter.wholeRoot)
    writes.set(codexAdapter.relative, {
      kind: "link",
      target: codexAdapter.target,
      source: "codex-adapter",
    });
  writes.set(MARKER, { kind: "file", bytes: markerBytes, mode: GENERATED_FILE_MODE, source: "marker" });
  return { sourceCheckout, manifest, methodSurfaceSha256, writes, codexAdapter };
}

function candidateRoots(plan) {
  const roots = [
    { relative: "AGENTS.md", kind: "file" },
    { relative: "CLAUDE.md", kind: "file" },
    { relative: ".claude", kind: "dir" },
    { relative: "templates", kind: "dir" },
  ];
  if (plan.codexAdapter.wholeRoot && plan.codexAdapter.localizeAncestor)
    roots.push({ relative: ".agents", kind: "dir" });
  else if (!plan.codexAdapter.wholeRoot)
    roots.push({ relative: CODEX_SKILLS_DIR, kind: "dir" });
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

function protectOwnerRecordAliases(roots) {
  // A link into a replaced method directory can change owner records without
  // writing their own paths. map.md has its existing localization transaction.
  const pending = ["product.md", "state.md", "decisions.md", "work"];
  while (pending.length) {
    const relative = pending.pop();
    const absolute = ensureTargetRelative(relative);
    const entry = lstatOptional(absolute);
    if (!entry) continue;
    if (entry.isSymbolicLink()) {
      const destinations = [
        path.resolve(path.dirname(absolute), fs.readlinkSync(absolute)),
        realpathOptional(absolute),
      ].filter(Boolean);
      if (roots.some(root => destinations.some(destination => {
        const replaced = ensureTargetRelative(root.relative);
        return pathInside(replaced, destination) || pathInside(destination, replaced);
      })))
        transactionError(`refusing: owner record ${normalizedRelative(relative)} links into a method path this upgrade replaces. Make that record local while preserving its contents, then retry. Nothing was touched.`);
    } else if (entry.isDirectory()) {
      for (const name of fs.readdirSync(absolute)) pending.push(path.join(relative, name));
    }
  }
}

function markerBytes(existing, provenance) {
  let installedAt = new Date().toISOString();
  if (existing && existing.version === VERSION &&
      markerSourceCheckout(existing) === provenance.sourceCheckout && existing.installedAt)
    installedAt = existing.installedAt;
  const next = {
    name: "speck-next",
    version: VERSION,
    sourceCheckout: provenance.sourceCheckout,
    methodSurfaceSha256: provenance.methodSurfaceSha256,
    upgradeAssessmentRecord: null,
  };
  next.installedAt = installedAt;
  return Buffer.from(JSON.stringify(next, null, 2) + "\n");
}

function transactionPlan(existingMarker) {
  const plan = desiredWrites(Buffer.alloc(0));
  const marker = markerBytes(existingMarker, plan);
  plan.writes.set(MARKER, { kind: "file", bytes: marker, source: "marker" });
  const primaryRoots = new Map();
  for (const candidate of candidateRoots(plan)) {
    const root = plannedRoot(candidate);
    const key = normalizedRelative(root.relative);
    if (!primaryRoots.has(key)) primaryRoots.set(key, { relative: root.relative, kind: root.kind, members: [] });
    primaryRoots.get(key).members.push(candidate.relative);
  }
  protectOwnerRecordAliases([...primaryRoots.values()]);
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

function physicalReportLeaves(relative) {
  const leaves = [];
  function visit(current) {
    const absolute = ensureTargetRelative(current);
    const stat = lstatOptional(absolute);
    if (!stat) return;
    if (stat.isDirectory() && !stat.isSymbolicLink()) {
      for (const name of fs.readdirSync(absolute).sort()) visit(path.join(current, name));
      return;
    }
    leaves.push(normalizedRelative(current));
  }
  visit(relative);
  return leaves;
}

function clampedReportStatusEntries(paths, reportIndex) {
  const requested = [...new Set(paths.map(pathname => normalizedRelative(pathname).replace(/\/$/, "")))];
  const canonical = realpathOptional(ensureTargetRelative(path.join(".claude", "skills")));
  const adapterRoot = normalizedRelative(CODEX_SKILLS_DIR);
  const codexAdapters = requested.filter(item => {
    const childName = item.startsWith(adapterRoot + "/") ? item.slice(adapterRoot.length + 1) : null;
    if (item !== adapterRoot &&
        !(childName && /^speck-next(?:-(?:[2-9]|[1-9][0-9]+))?$/i.test(childName))) return false;
    const absolute = ensureTargetRelative(item);
    const entry = lstatOptional(absolute);
    const resolved = entry && entry.isSymbolicLink() ? realpathOptional(absolute) : null;
    return Boolean(entry && entry.isSymbolicLink() && resolved && canonical &&
      resolved === canonical && pathInside(resolvedTarget(), resolved));
  });
  const output = [];
  const seen = new Set();
  function add(entry) {
    if (!seen.has(entry)) output.push(entry);
    seen.add(entry);
  }
  for (const entry of reportStatusEntries(paths, reportIndex)) {
    if (!/^(?:\?\?|!!) /.test(entry)) {
      add(entry);
      continue;
    }
    const code = entry.slice(0, 2);
    const relative = normalizedRelative(entry.slice(3).replace(/\/$/, ""));
    const stat = lstatOptional(ensureTargetRelative(relative));
    const codexAncestor = relative === ".agents" || relative.startsWith(".agents/");
    if (codexAncestor) {
      const selected = codexAdapters.filter(item =>
        item === relative || item.startsWith(relative + "/") || relative.startsWith(item + "/")
      );
      for (const adapter of selected)
        for (const leaf of physicalReportLeaves(adapter)) add(`${code} ${leaf}`);
      continue;
    }
    const descendants = requested.filter(item => item === relative || item.startsWith(relative + "/"));
    if (stat && stat.isDirectory() && !stat.isSymbolicLink() && descendants.length &&
        !requested.includes(relative)) {
      for (const descendant of descendants)
        for (const leaf of physicalReportLeaves(descendant)) add(`${code} ${leaf}`);
      continue;
    }
    add(entry.replace(/\/$/, ""));
  }
  return output;
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
  for (const entry of clampedReportStatusEntries(paths, reportIndex)) {
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
  return clampedReportStatusEntries(paths, reportIndex).join("\n");
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
    overlayEntry(transaction, root, child, entry);
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
  this.codexAdapter = { ...plan.codexAdapter };
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
  this.reportIndex = path.join(this.transactionRoot, "report-index");
  if (!existing) return;
  let logical;
  try {
    logical = fs.statSync(source);
  } catch {
    transactionError("refusing: the repository's Git index does not resolve to a readable regular file, so Speck Next cannot report this upgrade safely. Nothing was touched.");
  }
  if (!logical.isFile())
    transactionError("refusing: the repository's Git index does not resolve to a readable regular file, so Speck Next cannot report this upgrade safely. Nothing was touched.");
  try {
    fs.copyFileSync(source, this.reportIndex);
    applyMode(this.reportIndex, logical.mode);
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
  if (!sameSnapshot(snapshotPathState(CODEX_SKILLS_DIR), this.codexAdapter.selectionBefore) ||
      !sameSnapshot(snapshotPathState(this.codexAdapter.relative), this.codexAdapter.selectedBefore)) {
    transactionError("refusing: .agents/skills changed while Speck Next was choosing its Codex discovery adapter. Nothing was touched.");
  }
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
  if (!this.codexAdapter.wholeRoot)
    verifyCodexAdapter(this.stageRoot, this.codexAdapter, "staged");
  else if (this.codexAdapter.localizeAncestor)
    verifyCodexAdapterLink(this.stageRoot, this.codexAdapter, "staged");
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
  if (this.codexAdapter.wholeRoot) {
    const currentAdapter = snapshotPathState(this.codexAdapter.relative);
    if (!sameSnapshot(currentAdapter, this.codexAdapter.selectedBefore))
      transactionError(`refusing: ${normalizedRelative(this.codexAdapter.relative)} changed while Speck Next was staging the upgrade, so it stopped before replacing anything. Nothing was touched.`);
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
  verifyCodexAdapter(resolvedTarget(), this.codexAdapter, "installed");
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

function applyInstalledSurface(existingMarker) {
  const plan = transactionPlan(existingMarker);
  const transaction = new Transaction(plan);
  try {
    const productExists = plan.writes.has("product.md") || entryExists(path.join(target, "product.md"));
    transaction.prepareReportIndex();
    transaction.prepare();
    transaction.apply();
    const adapterPath = normalizedRelative(transaction.codexAdapter.relative);
    const localizedPaths = transaction.replacedLinks.map(link => link.relative);
    const installableLocalized = localizedPaths
      .filter(relative => !(adapterPath.startsWith(normalizedRelative(relative) + "/")));
    const installedEntries = installEntries(
      resolvedTarget(), [adapterPath, ...installableLocalized]
    );
    const extraReportPaths = [adapterPath, ...localizedPaths];
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
      codexAdapter: transaction.codexAdapter,
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

function entryExists(absolute) {
  return lstatOptional(absolute) !== null;
}

function migrationSource(version) {
  if (typeof version !== "string") return "unknown";
  const normalized = normalizedVersion(version);
  const match = normalized.match(/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?$/);
  if (!match) return "unknown";
  const source = match.slice(1, 4).map(Number);
  const current = VERSION.split(".").map(Number);
  if (!source.every(Number.isSafeInteger) || source[0] < 1) return "unknown";
  for (let index = 0; index < 3; index += 1) {
    if (source[index] > current[index]) return "future";
    if (source[index] < current[index]) return "supported";
  }
  return "current";
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

function upgradeNext(changes, diff) {
  const continuation = entryExists(path.join(target, "state.md"))
    ? "read current state.md and the user's request, then choose the work and care they need. Historical method assessments do not reopen or resolve product findings."
    : "continue from the user's current request, adding records and care only as the work needs them.";
  return (changes || diff)
    ? `Next: review the reported paths and complete diff, commit the upgrade, then ${continuation}`
    : `Next: there are no upgrade changes to commit; ${continuation}`;
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
    const install = applyInstalledSurface(null);
    for (const line of localizationLines(install.localizedLinks)) console.log(line);
    for (const line of retiredLinkLines(install.retiredLinks)) console.log(line);
    for (const line of preservationLines(install.preserved)) console.log(line);
    console.log(`Installed Speck Next ${versionWithProvenance(VERSION, install.sourceCheckout, install.methodSurfaceSha256)} into ${targetDisplay} — ${install.installedEntries.length} installed or carried-forward entries on disk.`);
    console.log(`Installed paths:\n${install.installedEntries.join("\n")}`);
    console.log("Next: open an agent session there and say what you want to do; the agent chooses the amount of method the request needs.");
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
  if (!prior || typeof prior !== "object" || Array.isArray(prior) ||
      (prior.name !== undefined && prior.name !== "speck-next"))
    die(`refusing: ${MARKER} is not a Speck Next marker object. Nothing was touched.`);
  const source = migrationSource(prior.version);
  if (source === "unknown")
    die(`refusing: ${MARKER} carries an unknown version (${JSON.stringify(prior.version)}). Nothing was touched.`);
  if (source === "future")
    die(`refusing: ${MARKER} carries a future version (${JSON.stringify(prior.version)}); this installer is ${VERSION}. Nothing was touched.`);
  try {
    const upgraded = applyInstalledSurface(prior);
    const from = versionWithProvenance(prior.version, markerSourceCheckout(prior), prior.methodSurfaceSha256 || null);
    const to = versionWithProvenance(VERSION, upgraded.sourceCheckout, upgraded.methodSurfaceSha256);
    for (const line of localizationLines(upgraded.localizedLinks)) console.log(line);
    for (const line of retiredLinkLines(upgraded.retiredLinks)) console.log(line);
    for (const line of preservationLines(upgraded.preserved)) console.log(line);
    console.log(`Upgraded Speck Next ${from} -> ${to} in ${targetDisplay}.`);
    console.log("Upgrade policy: historical product records and findings are preserved; v7 requires no product-team assessment.");
    console.log(upgraded.changes
      ? `Working-tree changes across the complete installed surface plus product.md:\n${upgraded.changes}`
      : "Working-tree changes across the complete installed surface plus product.md: none.");
    console.log(upgraded.diff
      ? `Complete installed-surface plus product.md diff (working tree against HEAD):\n${upgraded.diff}`
      : "Complete installed-surface plus product.md diff: empty.");
    console.log(upgradeNext(upgraded.changes, upgraded.diff));
  } catch (error) {
    die(error.speckMessage || error.message);
  }
} else {
  console.log(`speck-next v${VERSION} — a small kernel for building great products and proving them by running them.

  npx github:Keegil/speck-next install [dir]   place the method into a fresh git repo (default: current dir)
  npx github:Keegil/speck-next upgrade [dir]   refresh the method files in a Speck Next repo
  npx github:Keegil/speck-next tools setup    install the pinned optional toolkit in its own cache
  npx github:Keegil/speck-next tools doctor   inspect managed and existing tool versions
  npx github:Keegil/speck-next tools run <tool> -- <args>
                                                run graft, rg, jq, ast-grep, or rtk
  npx github:Keegil/speck-next tools remove   retire only the managed toolkit cache
  npx github:Keegil/speck-next upgrade [dir] --open-assessment
                                                retired in v7; refuses without changing files

The method starts in AGENTS.md, with five on-demand skills and six optional templates.
Pin this version: npx -y github:Keegil/speck-next#v${VERSION} install  (all tags: github.com/Keegil/speck-next/tags)`);
}
