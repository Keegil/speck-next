# v6.0.0 first adoption — fresh Codex tester

## Receipt and limits

- Persona: first-time Codex adopter; no contribution to design, code, product roles, or earlier review.
- Source: `/Users/kjetil/Code/speck-next`.
- Exact product candidate: `c2912e738c57218d23b574e5684c3aad026d2c07` (`c2912e7`).
- Built commit: `fff561e7da52c4cec0e385b10b0ba7bc061a585b` (`fff561e`).
- Combined review receipt: `9e8145621e36bff0a5361c1447ff857caf4ddca5` (`9e81456`).
- Started: `2026-09-06T00:38:27+0200`.
- Authorization: exactly one native Codex terminal turn, at most 180 seconds, with no retry, fallback, or owner interruption. A failed turn ends all host calls.
- Exclusions honored: no product-role conclusions read; `work/separated-product-team.md` not opened.
- Required experience instructions read in full from `.claude/skills/experience/SKILL.md` (75 lines) before the run.

## Planned walk

1. Export and `npm pack` the exact candidate into a disposable subject made with `mktemp`; initialize the adoption subject as a Git repository.
2. Seed one harmless owner skill, record its bytes and digest, and install via the packed tarball's `speck-next` npm binary.
3. From a nested directory, make one native Codex turn without manually opening the installed method. Ask which Speck Next workflows are available and for the first honest next action; request no file changes.
4. Inspect the installed product and verify the owner skill, version marker, method digest, five canonical skills, adapter target, package cleanliness, first-step clarity, and absence of duplicate skill bodies.
5. Run one model-free skeptical attack against discovery or coexistence.

## Pre-run observations

Command:

```text
git status --short
git log --oneline -8
git show c2912e7:package.json
```

Meaningful output:

```text
(working tree status was empty)
9e81456 Open the combined v6 release hearing
fff561e Mark the exact v6 candidate Built
28a8ca3 Close the v6 Engineering return
c2912e7 State v6.0.0 status truthfully
...
"name": "speck-next"
"version": "6.0.0"
"bin": { "speck-next": "bin/speck-next.js" }
```

`codex exec --help` was inspected before the run. This was not a model turn; it confirmed `--cd`, `--sandbox read-only`, `--ephemeral`, `--json`, and `--output-last-message` are available. The installed method itself was not opened.

## Run record

### Disposable subject and package

Commands:

```text
mktemp -d /tmp/speck-v6-first-adoption.XXXXXX
mkdir -p /tmp/speck-v6-first-adoption.y52xpK/{pack-source,adopter/deep/inside}
git init -q /tmp/speck-v6-first-adoption.y52xpK/pack-source
git init -q /tmp/speck-v6-first-adoption.y52xpK/adopter
git archive c2912e738c57218d23b574e5684c3aad026d2c07 | tar -x -C /tmp/speck-v6-first-adoption.y52xpK/pack-source
npm pack --json --pack-destination /tmp/speck-v6-first-adoption.y52xpK
```

Subject identity: `/tmp/speck-v6-first-adoption.y52xpK/adopter`, a new Git repository. The pack source is the adjacent new Git repository `/tmp/speck-v6-first-adoption.y52xpK/pack-source`, populated only from the exact candidate archive.

Meaningful pack output:

```text
id: speck-next@6.0.0
filename: speck-next-6.0.0.tgz
size: 652225
unpackedSize: 2193416
shasum: 4dbe4bbe4d169b7bd1d12220801be68e42e20851
integrity: sha512-p6AMtwolPyXS8zp/G7e/I9Y1rMwxI7XpI4fn1U8lcJ9z8tEB6qQJF/z5SLnw39B8lZtAJrnIjquyWGErz0XmWg==
entryCount: 110
local sha256: bf7ff955aba383af1140dc6296e50db042d6c615e6baeb6736778bd560cfe1b2
```

Before installation I added `.agents/skills/owner-compass/SKILL.md`, a 201-byte harmless owner skill whose one action is to answer `north-star intact` when explicitly asked. I committed that baseline as `266c0d4c0e12c3d8cef8e17040e1d8cb092fd644`.

Command and output:

```text
shasum -a 256 .agents/skills/owner-compass/SKILL.md
de63fff4a491e06f0d1e35d60206be58fe9e8227d0c9df68cb058730315c4e5f  .agents/skills/owner-compass/SKILL.md

wc -c .agents/skills/owner-compass/SKILL.md
201 .agents/skills/owner-compass/SKILL.md
```

### Installation through the packed npm binary

Command, run from the adoption subject:

```text
npm exec --yes --package=/tmp/speck-v6-first-adoption.y52xpK/speck-next-6.0.0.tgz -- speck-next install .
```

Meaningful output:

```text
Installed Speck Next 6.0.0 (source checkout not recorded; method surface sha256:1ccba108dcc2eb6f1e15812e53e8e243ee09ee586d69f7b45ac7dad472872d70) into /private/tmp/speck-v6-first-adoption.y52xpK/adopter — 20 installed or carried-forward files on disk.
Installed paths:
.agents/skills/speck-next
.claude/skills/craft/SKILL.md
.claude/skills/experience/SKILL.md
.claude/skills/experience/references/walk.md
.claude/skills/experience/references/worst-day.md
.claude/skills/judge/SKILL.md
.claude/skills/map-build/SKILL.md
.claude/skills/map-build/references/questions.md
.claude/skills/shape-product/SKILL.md
.claude/skills/shape-product/references/questions.md
.claude/speck-next.json
AGENTS.md
CLAUDE.md
map.md
templates/decisions.md
templates/map.md
templates/piece.md
templates/product.md
templates/rounds.md
templates/state.md
Next: open an agent session there and say what you want to build — shaping starts in that conversation.
```

First-person observation: the install was quick and gave me a useful human next step immediately. It also explicitly said which 20 paths it touched or carried forward instead of leaving me to infer the footprint.

### Single native Codex turn

I had not opened `AGENTS.md`, `.claude/speck-next.json`, or any installed canonical skill body before this call.

Command, launched from the nested directory `/tmp/speck-v6-first-adoption.y52xpK/adopter/deep/inside` with a process alarm at 180 seconds:

```text
codex exec --ephemeral --sandbox read-only --json --output-last-message /tmp/speck-v6-first-adoption.y52xpK/codex-last.txt 'You are in a repository that may have Speck Next installed. Without changing any files, answer from the repository native instructions: (1) Which Speck Next workflows are available here? (2) What is the first honest next action for this repository as it stands? (3) A pre-existing owner-compass skill may coexist here; if it is available, use it to report the owner compass. Be concise.'
```

Result: failed in 4.78 seconds, exit code 1. Native session id: `01a073bb-6146-7c71-82f0-a9f68953fa97`. Token usage: not emitted.

Meaningful JSON/event output:

```text
{"type":"thread.started","thread_id":"01a073bb-6146-7c71-82f0-a9f68953fa97"}
{"type":"turn.started"}
startup websocket prewarm setup failed: ... "The 'gpt-6-astra' model requires a newer version of Codex. Please upgrade to the latest app or CLI and try again."
{"type":"turn.failed","error":{"message":"... The 'gpt-6-astra' model requires a newer version of Codex ..."}}
```

The CLI also warned that its model cache lacked `supports_parallel_tool_calls` and treated `gpt-6-astra` as an unknown model. An unrelated configured MCP endpoint returned HTTP 500 during startup. The decisive failure was the model/version rejection; no assistant answer or last-message file was produced.

Authorization response: no retry, model fallback, resumed turn, or further native model-bearing call was made. This leaves native discovery, first-step clarity through Codex, and model-mediated use of the owner skill untested by execution.

Runtime identity, checked after the failed turn without starting another one:

```text
codex-cli 0.147.0
npm 11.4.0
node v24.0.2
codex-last.txt absent
```

### Installed result

**Version marker — works.** `.claude/speck-next.json` says:

```json
{
  "name": "speck-next",
  "version": "6.0.0",
  "sourceCheckout": null,
  "methodSurfaceSha256": "1ccba108dcc2eb6f1e15812e53e8e243ee09ee586d69f7b45ac7dad472872d70",
  "upgradeAssessmentRecord": null,
  "installedAt": "2026-09-05T22:39:59.074Z"
}
```

**Method digest — works.** I independently reapplied the installer's digest framing to the sorted regular files under `AGENTS.md`, `CLAUDE.md`, `.claude/skills`, and `templates`: path, NUL, bytes, NUL for each file.

```text
files=17
1ccba108dcc2eb6f1e15812e53e8e243ee09ee586d69f7b45ac7dad472872d70
```

The computed digest exactly matches both the marker and install output. `AGENTS.md` itself is 25,928 bytes with sha256 `b9e6b7869ca28c05e4c4c0a4146e8a307be0c4119fd6d0a897a398e3d1d57152`; the marker is correctly an aggregate surface digest, not that single-file hash.

**Five canonical skills — works.** Command:

```text
find .claude/skills -name SKILL.md -type f -print | sort
```

Output:

```text
.claude/skills/craft/SKILL.md
.claude/skills/experience/SKILL.md
.claude/skills/judge/SKILL.md
.claude/skills/map-build/SKILL.md
.claude/skills/shape-product/SKILL.md
```

Each installed body was byte-compared with the exact packed candidate and returned `canonical-byte-match`.

**Codex adapter target — works at the filesystem boundary.** Commands and output:

```text
readlink .agents/skills/speck-next
../../.claude/skills

realpath .agents/skills/speck-next
/private/tmp/speck-v6-first-adoption.y52xpK/adopter/.claude/skills
```

The adapter is one relative symbolic link, resolves inside the subject to the canonical skill directory, and did not replace `.agents/skills` or the owner skill beside it.

**Owner-skill preservation and coexistence — works at the byte and discovery-tree boundary.** After install:

```text
git diff --exit-code HEAD -- .agents/skills/owner-compass/SKILL.md
(no output; exit 0)

shasum -a 256 .agents/skills/owner-compass/SKILL.md
de63fff4a491e06f0d1e35d60206be58fe9e8227d0c9df68cb058730315c4e5f  .agents/skills/owner-compass/SKILL.md
```

The digest and 201-byte size are identical to the sealed pre-install baseline. Its valid `name`, `description`, and `north-star intact` instruction remain readable. The installed discovery tree exposes it beside all five Speck skills. Actual model-mediated invocation is untested because the only authorized Codex turn failed before inference.

**No duplicate skill body — works.** The five canonical skill hashes are all distinct. Following the adapter and hashing every discoverable `.agents/skills/**/SKILL.md` found six bodies total — the five canonical bodies plus `owner-compass` — and `sort | uniq -d | wc -l` returned `0`. Inode checks also showed that adapter paths and their `.claude/skills` counterparts are the same files, not copied bodies; for example both craft paths had inode `234025771` and both experience paths had inode `234025773`.

**First-step clarity — clear in static surfaces, untested in the required native conversation.** The empty adoption subject has no `product.md`; installed `map.md` says `No map yet`. `AGENTS.md` lines 58–65 say to choose from completed evidence and, without a ratified product, use `shape-product`. This agrees with the installer's plain final instruction: `open an agent session there and say what you want to build — shaping starts in that conversation.` I knew what to do next without reading implementation. The required proof that native Codex itself gives that answer is absent because the host rejected its configured model.

One small clarity blemish: `speck-next --help` identifies itself as v6.0.0 but its only pinning example still says `#v5.0.0`. That could send a newcomer intentionally looking for the current released tag back one major version.

**Package cleanliness — broken.** The install footprint itself stayed focused: Git showed only the adapter, `.claude`, `AGENTS.md`, `CLAUDE.md`, `map.md`, and templates as new; it did not copy the packed development archive into the adopter repo. The npm artifact is not a clean runtime distribution, however. It has no `.npmignore`, no `files` allowlist in `package.json`, and contains 110 entries / 2,193,416 unpacked bytes. Top-level counts include:

```text
36 work
21 docs
21 devsuite
9 .claude
6 templates
6 examples
```

This command found 79 entries under `work/`, `docs/reviews/`, `devsuite/`, or the source repo's own `product.md`, `state.md`, `map.md`, and `decisions.md`:

```text
tar -tzf speck-next-6.0.0.tgz | rg '^package/(work/|docs/reviews/|devsuite/|product\.md$|state\.md$|map\.md$|decisions\.md$)' | wc -l
79
```

The names include prior tester and judge records, the live separated-product-team work record, and dev-suite fixtures. I did not open their contents. A path-name scan found no `.git`, `node_modules`, `.DS_Store`, `.env`, PEM, key, or p12 entries, but absence of those common names does not make 79 non-runtime product-development artifacts clean.

### Model-free skeptical attack: nested discovery plus path containment

From `deep/inside`, `git rev-parse --show-toplevel` returned the correct adopter root. I then followed every `.agents/skills` discovery path, required every `SKILL.md` to be a readable regular file, resolved it, checked that it remained inside that root, and checked content hashes for duplicates.

Meaningful output:

```text
/private/tmp/speck-v6-first-adoption.y52xpK/adopter
.agents/skills/owner-compass/SKILL.md
.agents/skills/speck-next/craft/SKILL.md
.agents/skills/speck-next/experience/SKILL.md
.agents/skills/speck-next/judge/SKILL.md
.agents/skills/speck-next/map-build/SKILL.md
.agents/skills/speck-next/shape-product/SKILL.md
duplicate digest count: 0
inside-subject: 6
path escapes: 0
```

The filesystem-level discovery/coexistence attack passes from the same nested starting point. It does not substitute for a successful native Codex discovery turn.

## Untested

- Which workflows native Codex would report, the first action it would choose, and whether it would actually load and obey `owner-compass`; the sole authorized turn failed before an assistant response.
- Package contents for confidential values. I inspected paths and distribution scope only, because reading the product-role/review conclusions was explicitly excluded.
- Upgrade, reinstall, non-Git, Windows, network failure, or destructive-collision paths; they were outside this first-install walk, and I did not rebuild the subject.

## Verdict — first-time adopter

**Works:** Partly, not end to end. Packing and installation work; v6.0.0 provenance, the aggregate digest, all five canonical skills, the relative Codex adapter, nested filesystem discovery, and preservation of my owner skill all checked out. My one real Codex conversation did not work, so I never reached the product's promised first action.

**Keep:** Not this release artifact yet. I would keep the installation approach — it is fast, explicit, and tells me that shaping is next — but I would not keep v6.0.0 installed in a real repo until one compatible native Codex turn proves discovery and the npm tarball is narrowed to what adopters need.

**Deal-breaker:** The product-owned deal-breaker is the dirty package: 79 internal work, review, dev-suite, or source-state entries ride in the adopter tarball. The failed Codex turn is also a practical adoption blocker on this exact host, although the evidence points to host CLI/model compatibility rather than Speck's installed bytes. A clean package and a successful fresh turn on the supported Codex version are the two conditions that would change my verdict.
