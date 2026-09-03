#!/usr/bin/env node
// Speck Next installer/upgrader. Run from anywhere:
//   npx github:Keegil/speck-next install [dir]
//   npx github:Keegil/speck-next upgrade [dir]
//   npx github:Keegil/speck-next upgrade [dir] --open-assessment
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
const PRODUCT_TEAM_HEADING = "## Product team";
const PRODUCT_TEAM_ROLES = ["Product", "Business", "Experience", "Engineering"];
const CONDITIONAL_ROLE_FIELDS = [
  "Protects", "Call when", "May stay out when", "Evidence expires", "Material changes",
];
const TRIVIAL_PRODUCT_TEAM_VALUES = new Set(["tbd", "todo", "none", "n/a", "placeholder"]);
const ASSESSMENT_BLOCK = `${ASSESSMENT_HEADING}\n\n${ASSESSMENT_PENDING}\n${ASSESSMENT_RECORD_LINE}\n`;
const RECOVERABLE_FIELDLESS_VERSION = "6.0.0-rc.2";

function die(msg) { console.error(msg); process.exit(1); }

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

const { command: cmd, target, openAssessment } = parseCli(process.argv);

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

function activeMarkdownLines(content) {
  const lines = content.split("\n");
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
  return { lines, active };
}

function assessmentError(message, repair = "Next: restore consistent assessment evidence, then run the upgrade again.") {
  die(`refusing: ${message}\nNothing in the repository changed.\n${repair}`);
}

function unusableProductTeamValue(value) {
  const trimmed = value.trim();
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
  const { lines, active } = activeMarkdownLines(content);
  const matches = lines.flatMap((line, index) => active[index] && line === generated ? [index] : []);
  if (matches.length > 1)
    assessmentError(`product.md contains ${matches.length} current copies of a generated upgrade status; its origin is ambiguous.`);
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
  const migration = planProductTeamAssessment(source, prior, openAssessment);
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
  npx github:Keegil/speck-next upgrade [dir] --open-assessment
                                                conservatively open an ambiguous rc.2 assessment

The method itself is one page: AGENTS.md. Everything else is five skills your agent loads on demand, and six file skeletons in templates/.
Pin a released tag, e.g.: npx -y github:Keegil/speck-next#v5.0.0 install  (all tags: github.com/Keegil/speck-next/tags)`);
}
