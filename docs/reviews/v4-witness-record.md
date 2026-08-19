# Witness record — experience → judge redesign

**Subject:** `f86fe5337e03fab15ba1352e5d728d8b33e500e8` and its successor, `0ea35928c9e94d01f41c2ffa513f4adbb5e992b2`  
**Run date:** 2026-08-19  
**Stance:** fresh witness; no part in authoring these commits; observations only. A separate judge owns all rulings.  
**Transcript note:** literal excerpts and command output below contain the method's own judgment vocabulary because probes 2, 6, and 7 require exact source comparison. Those words are quotations, search needles, or raw output, not witness conclusions.

## 1. Cold read

I read `AGENTS.md` from top to bottom before opening `README.md`.

### Commands

```sh
wc -l AGENTS.md README.md && nl -ba AGENTS.md
```

The command reported 54 lines in `AGENTS.md`, 44 in `README.md`, and then printed all 54 numbered lines of `AGENTS.md`.

```sh
nl -ba README.md
```

The command printed all 44 numbered lines of `README.md`.

### Places I stumbled in `AGENTS.md`

| Line | Exact text or phrase | Cold-reader experience |
|---|---|---|
| 3 | “This repository (the kernel's own) runs under it too.” | “Kernel” had not been introduced. I understood it only after `README.md:3` called Speck Next a small kernel. |
| 7 | “Push by default” and “every natural beat” | I could not turn “natural beat” into a checkable trigger from this paragraph. Later lines name map-changing events for `state.md`, but do not define every communication beat. |
| 9 | “the artifact is linked, never pasted” followed by “the ask is made on a plain-language rendering” | I re-read this to decide where the rendering lives. The text says the artifact is linked and the rendering is not the artifact, but it does not name whether the rendering is inline conversation, another file, or generated output. |
| 9 | “three fresh refuters and an independent reviewer had all held green” | “Refuter,” “independent reviewer,” and “held green” appear in the history sentence without definitions. The new witness/judge split is not used in that sentence. |
| 13–20 | Dispatcher derived from “exit conditions” | I had to read forward into the phase section and skills before I could check the dispatcher. The dispatcher itself does not contain all exit details. |
| 20 | “a ruling, a finding, or a judgment” and “record the trace” | I had to separate three near-synonyms and infer which artifact creates each. The rest of the bullet names a reopening decision and reopened files, but “finding” has no source named on this page. |
| 26 | “the shaping review passed with its receipt” | The page does not say here that shaping review is a witness dispatch followed by a separate judge. `.claude/skills/shape-product/SKILL.md:22` supplies that later. |
| 27 | “what proven means per piece” | The outcome use of “proven” is explained at line 30, after this load-bearing use. On first encounter I paused to determine whether it was a state. |
| 27 | “the completion test passes mechanically” | The mechanical test is not on this page. `.claude/skills/map-build/SKILL.md:17` supplies its enumerable sets. |
| 28 | The full build-loop sentence | I had to split one 246-word sentence at each arrow and re-read it as six separate steps. “what's wearing out,” “strain,” “re-lands,” and “the map ticks” carry actions inside the sentence before any of them is explained. |
| 28 and 32 | “`state.md` re-lands” | I could act on “update `state.md`,” but “re-land” is not defined and no command or generator is named. |
| 30 | “the owner grades the felt experience” followed by “the owner has judged” | I re-read this to separate the owner's taste grade from the separate judge's rulings. The second phrase is broader than the first. |
| 40 | “derived, never narrated” | I could not tell what derives the file. The page later instructs the agent to re-land it, but names no derivation mechanism. |
| 42 | “under the same review” | “Review” is generic here even though the redesign assigns observation and ruling to two different contexts. |
| 48 | “When genuinely unclear, the judge decides” | The judge skill enters after experience records exist. This line does not say how to dispatch that judge before work begins when the only question is whether a change is small. |

### Places I stumbled in `README.md`

| Line | Exact text or phrase | Cold-reader experience |
|---|---|---|
| 14 | The example judge names “works, on-promise, good to use on desktop and phone. Nothing open.” | The later four-item list at line 26 also contains “the quality hangs together.” I went back to see whether the example had reported three items or whether “good to use” was meant to carry two. |
| 16 | “the product ran before anyone wrote a plan about it” | The five-phase sequence places mapping before building. I could not tell whether the example assumes an already-running product or whether “plan” means something other than `map.md`. |
| 20 | “Every phase has a checkable exit that includes the owner's ratification in his own words” | `AGENTS.md` explicitly requires ratification for Shape and Map. Experience exits when walks are in; Judge exits after the owner grades; Build lands after witness and judge. I had to compare the files to decide how the universal sentence applies. |
| 20 | Experience personas list “the first-timer, the real job, the worst day” | `AGENTS.md:29` lists four milestone personas and includes “the second user.” The second-user move appears later in `README.md:28` only as a least-privileged login, without the “second person on the same install” wording from the experience skill. |
| 24 | “`state.md` — generated, never hand-written” | No generator is named in the page or CLI usage. `AGENTS.md` tells the agent to re-land the file. I could not identify the action behind “generated.” |
| 24 | “There is nothing for an agent to be told to go read.” | The skills themselves contain explicit read instructions for `references/questions.md`, `product.md`, and `decisions.md`. I read this twice and inferred it means host-native loading, not the absence of read instructions. |
| 26 | “Those four words are the entire vocabulary you need.” | By this point the page had also asked me to understand piece, milestone, substrate, ratification, witness, judge, receipt, strain, and state. The contract later narrows its count to coined words an owner must learn, which is more specific than this sentence. |
| 32 | “Shaping starts by reading that list” | I could not tell whether this means the Shape phase or the “shape it” step inside every Build piece. `AGENTS.md:28` places the read before a piece; the dispatcher enters Shape only when the product promise needs shaping. |
| 36 | “Upgrading from any Speck is one command” | The universal scope is much larger than the local fresh-install/same-version upgrade I could exercise in this run. I marked the remainder in Limits. |
| 38 | “today: 18, measured” | The fresh install command also printed 18. A filesystem count after installation returned 19 regular files outside `.git`, or 18 when `.claude/speck-next.json` was excluded. |
| 44 | “At v4” and later “v1 is accepted” | I had to infer that v4 names the current kernel version while v1 names an earlier acceptance milestone rather than the current package version. |

## 2. Vocabulary sweep

### Command

```sh
rg -n -i --glob '*.md' 'independent-review|unproven|\bProven\b|\bproving\b|\breviewer\b' AGENTS.md CLAUDE.md .claude/skills templates || true
```

### What came back

No line contained `independent-review`, `unproven`, or `proving`. The search returned these lines for `Proven`/`proven` or `reviewer`:

| Location | Surrounding claim observed |
|---|---|
| `AGENTS.md:9` | Calls the owner “the only reviewer who judges the whole product by taste,” then recounts “three fresh refuters and an independent reviewer” as history. |
| `AGENTS.md:27` | Mapping decides “what proven means per piece.” |
| `AGENTS.md:30` | Explicitly licenses *proven* as outcome speech when all four items stand on evidence and says that outcome goes Live. |
| `.claude/skills/judge/SKILL.md:15` | Uses *proven* for the all-four-on-evidence outcome and routes it to Live. |
| `templates/piece.md:9` | Capitalized field heading `**Proven means:**`; the field asks for runs, witness walks, and the judge's subject. It is not shown as a state in the template. |
| `templates/map.md:11` | Per-piece field `proven means:` with runs, walks, and judge subject. |
| `.claude/skills/map-build/SKILL.md:8` | Says mapping decides what proven means per piece. |
| `.claude/skills/map-build/SKILL.md:14` | Requires each piece to state what proven means. |
| `.claude/skills/map-build/SKILL.md:17` | Requires every piece to have a proven-means line. |
| `.claude/skills/map-build/SKILL.md:20` | Historical sentence says the owner's read catches what “every other reviewer missed.” |
| `.claude/skills/experience/SKILL.md:14` | Historical phrase “twice proven” about reconstructed receipts. |
| `.claude/skills/experience/SKILL.md:16` | Names `proven` inside the list of words a witness record never uses. |
| `.claude/skills/experience/SKILL.md:21` | Uses “proving each claimed save/send/generate” for mechanism read-back. |
| `.claude/skills/map-build/references/questions.md:14` | Uses proof/proven as the evidence an ordering unlocks. |
| `.claude/skills/map-build/references/questions.md:17` | Heading `**Proven, per piece:**`. |
| `.claude/skills/map-build/references/questions.md:19` | Says each piece names “what the reviewer attacks” and separately what the experience walk covers. This is the one present-tense instruction where `reviewer` occupies work that the redesigned files elsewhere divide between witness and judge. |
| `.claude/skills/experience/references/worst-day.md:21` | Uses “is proven by” for baseline/action/read-back persistence evidence. |

The sweep found no use of `Proven` as a value in the state ladder. The only capitalized non-sentence use is the “Proven means” piece-template heading; the state templates use `Shaped → Built → Judged → Live`.

## 3. Reference resolution and templates

### Skill names

Command:

```sh
find .claude/skills -mindepth 1 -maxdepth 1 -type d -print | sort
```

Output:

```text
.claude/skills/craft
.claude/skills/experience
.claude/skills/judge
.claude/skills/map-build
.claude/skills/shape-product
```

I then searched each of those names across the installed surface:

```sh
for skill_dir in .claude/skills/*; do skill_name=${skill_dir##*/}; printf '%s\n' "== $skill_name =="; rg -n --glob '*.md' "\`$skill_name\`|name: $skill_name" AGENTS.md CLAUDE.md .claude/skills templates || true; done
```

The mentions resolve to the five directories above: `shape-product`, `map-build`, `craft`, `experience`, and `judge`. I found no sixth skill name in an instruction.

Command:

```sh
nl -ba CLAUDE.md
```

Output:

```text
     1	@AGENTS.md
```

`AGENTS.md` exists beside this reference in both the subject repo and the fresh install.

### Files the skills tell an agent to read

Command:

```sh
for p in product.md decisions.md state.md templates/map.md templates/product.md templates/rounds.md work/mapping.md work/shaping.md .claude/skills/map-build/references/questions.md .claude/skills/shape-product/references/questions.md .claude/skills/experience/references/walk.md .claude/skills/experience/references/worst-day.md; do if [ -e "$p" ]; then printf 'EXISTS %s\n' "$p"; else printf 'MISSING %s\n' "$p"; fi; done
```

Output:

```text
EXISTS product.md
EXISTS decisions.md
EXISTS state.md
EXISTS templates/map.md
EXISTS templates/product.md
EXISTS templates/rounds.md
MISSING work/mapping.md
MISSING work/shaping.md
EXISTS .claude/skills/map-build/references/questions.md
EXISTS .claude/skills/shape-product/references/questions.md
EXISTS .claude/skills/experience/references/walk.md
EXISTS .claude/skills/experience/references/worst-day.md
```

The literal read targets resolve as follows:

| Skill | Instruction | Resolved path | Observation |
|---|---|---|---|
| `craft` | Get declared feel from `product.md` | `product.md` | Exists in this subject repo. |
| `judge` | Read records, `product.md`, `decisions.md`, attached evidence | `product.md`, `decisions.md` | Both exist in this subject repo. |
| `map-build` | Read `references/questions.md`; start from `templates/map.md` | `.claude/skills/map-build/references/questions.md`; `templates/map.md` | Both exist under their stated resolution bases. |
| `shape-product` | Read `references/questions.md`; start from `templates/rounds.md` and `templates/product.md` | `.claude/skills/shape-product/references/questions.md`; both templates | All exist. |
| `experience` | For UI, walk `references/walk.md`; worst-day persona uses `references/worst-day.md` | `.claude/skills/experience/references/walk.md`; `.claude/skills/experience/references/worst-day.md` | Both exist. |

`work/mapping.md` and `work/shaping.md` do not exist in this already-shaped kernel repo. The skills describe them as records to create/write, not files an agent must read before beginning. The fresh install in probe 5 likewise contains no `work/` directory.

I also checked the literal targets in the fresh installed repo after upgrade:

```sh
for p in ./tmp-install/AGENTS.md ./tmp-install/product.md ./tmp-install/map.md ./tmp-install/decisions.md ./tmp-install/state.md ./tmp-install/.claude/skills/map-build/references/questions.md ./tmp-install/.claude/skills/shape-product/references/questions.md ./tmp-install/.claude/skills/experience/references/walk.md ./tmp-install/.claude/skills/experience/references/worst-day.md; do if [ -e "$p" ]; then printf 'EXISTS %s\n' "$p"; else printf 'MISSING %s\n' "$p"; fi; done
```

Output:

```text
EXISTS ./tmp-install/AGENTS.md
MISSING ./tmp-install/product.md
EXISTS ./tmp-install/map.md
MISSING ./tmp-install/decisions.md
MISSING ./tmp-install/state.md
EXISTS ./tmp-install/.claude/skills/map-build/references/questions.md
EXISTS ./tmp-install/.claude/skills/shape-product/references/questions.md
EXISTS ./tmp-install/.claude/skills/experience/references/walk.md
EXISTS ./tmp-install/.claude/skills/experience/references/worst-day.md
```

The skill-relative references exist in the fresh install. The root files that `craft` or `judge` later read are not all born at install: `product.md`, `decisions.md`, and `state.md` are absent, while their skeletons are present. The dispatcher enters shaping before `craft` or `judge`; I did not run an agent session far enough to observe when each missing root file is instantiated.

### Template side-by-side

I printed every template with:

```sh
for f in templates/*.md; do printf '\n===== %s =====\n' "$f"; nl -ba "$f"; done
```

The resulting comparison:

| Surface promise | Template text | Side-by-side observation |
|---|---|---|
| `.claude/skills/experience/SKILL.md:14` requires tool/model/session, date and commit, personas, walks **and commands** planned, run owner, empty-record protocol, and returned record. | `templates/piece.md:11` has witness tool/model/session, date/commit, “personas and walks [planned],” run owner, empty-record protocol, and record. | The piece template has no named field for planned commands. |
| `AGENTS.md:26` and `shape-product/SKILL.md:8` require a shaping review receipt; `shape-product/SKILL.md:22` specifies witness then separate judge. | `templates/rounds.md` contains the conversation and ratification fields only. | No witness receipt or judge line appears in the rounds skeleton used for shaping. |
| `AGENTS.md:27` and `map-build/SKILL.md:18` require a witnessed-and-judged map receipt. | `templates/rounds.md` is also the mapping-record skeleton. | No witness receipt or judge line appears in the mapping rounds skeleton. |
| `.claude/skills/judge/SKILL.md:10` requires judge tool/model/session, when, and ruling what. | `templates/piece.md:13` has judge tool/model/session, ruled date, verdict families, more walks, and routing. | The piece title supplies the subject implicitly; the line does not have a separately named “ruling what” slot. |
| `AGENTS.md:40` names `Shaped → Built → Judged → Live`. | `templates/state.md:6` prints the same ladder. | The strings are identical. |
| `AGENTS.md:30` names four items: works, delivers the promise, good to use, quality hangs together. | `templates/state.md:6` spells all four; `templates/piece.md:13` says only “the four, separately.” | The state skeleton names each item; the piece judgment skeleton refers to the set without listing the four names. |
| The experience and judge skills require a separate witness and judge per substantial piece. | `templates/piece.md:11` has an Experience receipt; line 13 has a separate Judgment entry. | Both contexts have distinct fields in the piece skeleton. |

## 4. Owner record check

Source command:

```sh
sed -n '1,220p' decisions.md
```

The top entry is dated 2026-08-19 and titled “Prove becomes experience → judge.” I compared its three verbatim owner calls with the installed surface.

### Call 1 — worst-day personas live inside experience

Owner record:

> “Inside experience, as worst-day personas”

Surface:

- `AGENTS.md:29` places “the worst day” inside Experience.
- `.claude/skills/experience/SKILL.md:3,19–24` includes the worst day as persona 4.
- `.claude/skills/experience/references/worst-day.md` is nested under the experience skill.
- `CONTRACT.md:19` puts “the worst day” in the witness persona list.
- `README.md:20,28` puts the worst day in experiencing/witnessing.
- `templates/piece.md:11` has a generic personas-and-walks slot and does not name worst-day explicitly.

I found no surface sentence assigning the worst-day walk to the judge. `README.md:20`'s short experience list omits the second user even though `AGENTS.md:29` says milestone experience uses all four personas.

### Call 2 — separate judge per piece

Owner record:

> “Separate judge per piece”

Surface:

- `AGENTS.md:28` says a separate fresh context judges every substantial piece after a fresh witness.
- `.claude/skills/judge/SKILL.md:10` says “A separate fresh context per piece,” never builder and never witness.
- `.claude/skills/experience/SKILL.md:3` says every substantial piece gets experience before judge.
- `templates/piece.md:11,13` gives witness and judge separate fields.
- `CONTRACT.md:19` says never builder and never the same head.
- `README.md:14,28` uses a separate judge in both example and explanation.

Two generic-review remnants sit beside that specificity:

- `AGENTS.md:26–27` calls the shaping and map exits “the shaping review” and “the map review” without naming the two contexts; the corresponding skills name both contexts.
- `.claude/skills/map-build/references/questions.md:19` still asks “what the reviewer attacks,” giving one reviewer an attack role alongside the experience walk.

### Call 3 — Shaped → Built → Judged → Live; proven as outcome speech; routing by grounds

Owner record:

> “'Proven' can easily exist as an OUTCOME ... But something that is proven, becomes Live.”

Surface:

- `AGENTS.md:30,40`, `CONTRACT.md:20`, `README.md:26`, and `templates/state.md:6` all print `Shaped → Built → Judged → Live` and describe proven as the all-four-on-evidence outcome before Live.
- `.claude/skills/judge/SKILL.md:15` uses the same outcome-to-Live wording.
- `AGENTS.md:20,30,40` and `.claude/skills/judge/SKILL.md:21` route by grounds: promise → shaping, piece-space → mapping, implementation → build.
- `templates/state.md:6` says work found insufficient routes back instead of advancing, but does not list the three grounds in the skeleton itself.
- `templates/piece.md:13` has a routing field: “which phase, with the trace.”
- The vocabulary sweep found no `Proven` state value. `templates/piece.md:9` retains “Proven means” as a piece-outcome heading.

## 5. Run it

### 5.1 CLI with no arguments

My first instrumentation wrapper used a zsh-reserved variable:

```sh
node bin/speck-next.js; status=$?; printf '\n[exit=%s]\n' "$status"
```

It printed the CLI usage, then zsh printed:

```text
zsh:1: read-only variable: status
```

I re-ran the requested command without the wrapper:

```sh
node bin/speck-next.js
```

Tool metadata reported exit code 0. Exact stdout:

```text
speck-next v4.0.0 — a small kernel for building great products and proving them by running them.

  npx github:Keegil/speck-next install [dir]   place the method into a fresh git repo (default: current dir)
  npx github:Keegil/speck-next upgrade [dir]   refresh the method files in a Speck Next repo

The method itself is one page: AGENTS.md. Everything else is five skills your agent loads on demand, and six file skeletons in templates/.
Pin a version: npx -y github:Keegil/speck-next#v4.0.0 install
```

### 5.2 Fresh repository and install

Preflight:

```sh
if [ -e ./tmp-install ]; then ls -la ./tmp-install; else printf './tmp-install does not exist\n'; fi
```

Output:

```text
./tmp-install does not exist
```

Repository creation:

```sh
mkdir ./tmp-install && git -C ./tmp-install init
```

Output:

```text
hint: Using 'master' as the name for the initial branch. This default branch name
hint: is subject to change. To configure the initial branch name to use in all
hint: of your new repositories, which will suppress this warning, call:
hint:
hint: 	git config --global init.defaultBranch <name>
hint:
hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
hint: 'development'. The just-created branch can be renamed via this command:
hint:
hint: 	git branch -m <name>
Initialized empty Git repository in /private/tmp/claude-501/-workspace-speck/a0e0d32c-31ec-4aba-a433-2bd88364f16f/scratchpad/v4-witness-U2Pp/repo/tmp-install/.git/
```

Install:

```sh
node bin/speck-next.js install ./tmp-install
```

Tool metadata reported exit code 0. Exact stdout:

```text
Installed Speck Next v4.0.0 into /private/tmp/claude-501/-workspace-speck/a0e0d32c-31ec-4aba-a433-2bd88364f16f/scratchpad/v4-witness-U2Pp/repo/tmp-install (18 files).
Next: open an agent session there and say what you want to build — shaping starts in that conversation.
```

Tree/count/skills command:

```sh
find ./tmp-install -path './tmp-install/.git' -prune -o -type f -print | sort; printf 'file_count='; find ./tmp-install -path './tmp-install/.git' -prune -o -type f -print | wc -l | tr -d ' '; printf '\nskills:\n'; find ./tmp-install/.claude/skills -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort
```

Output:

```text
./tmp-install/.claude/skills/craft/SKILL.md
./tmp-install/.claude/skills/experience/SKILL.md
./tmp-install/.claude/skills/experience/references/walk.md
./tmp-install/.claude/skills/experience/references/worst-day.md
./tmp-install/.claude/skills/judge/SKILL.md
./tmp-install/.claude/skills/map-build/SKILL.md
./tmp-install/.claude/skills/map-build/references/questions.md
./tmp-install/.claude/skills/shape-product/SKILL.md
./tmp-install/.claude/skills/shape-product/references/questions.md
./tmp-install/.claude/speck-next.json
./tmp-install/AGENTS.md
./tmp-install/CLAUDE.md
./tmp-install/map.md
./tmp-install/templates/decisions.md
./tmp-install/templates/map.md
./tmp-install/templates/piece.md
./tmp-install/templates/product.md
./tmp-install/templates/rounds.md
./tmp-install/templates/state.md
file_count=19
skills:
craft
experience
judge
map-build
shape-product
```

The marker contains:

```json
{
  "name": "speck-next",
  "version": "4.0.0",
  "commit": "0ea3592",
  "installedAt": "2026-08-19T18:55:32.188Z"
}
```

A second count made the installer's boundary visible:

```sh
printf 'regular_files_excluding_git='; find ./tmp-install -path './tmp-install/.git' -prune -o -type f -print | wc -l | tr -d ' '; printf '\nregular_files_excluding_git_and_marker='; find ./tmp-install -path './tmp-install/.git' -prune -o -type f ! -path './tmp-install/.claude/speck-next.json' -print | wc -l | tr -d ' '; printf '\n'
```

Output:

```text
regular_files_excluding_git=19
regular_files_excluding_git_and_marker=18
```

The fresh repo remained without a commit; `git status --short` showed the installed paths as untracked.

### 5.3 Plant retired skill and upgrade the same repository

I created `tmp-install/.claude/skills/independent-review/` and added this exact file via `apply_patch`:

```md
---
name: independent-review
description: planted stale skill for the v4 upgrade probe
---

# independent-review

This file was planted before the upgrade command.
```

Upgrade:

```sh
node bin/speck-next.js upgrade ./tmp-install
```

Tool metadata reported exit code 0. Exact stdout:

```text
Upgraded Speck Next 4.0.0 (0ea3592) -> 4.0.0 in /private/tmp/claude-501/-workspace-speck/a0e0d32c-31ec-4aba-a433-2bd88364f16f/scratchpad/v4-witness-U2Pp/repo/tmp-install.
What changed (git has your back — diff or revert as you like):
?? .claude/
?? AGENTS.md
?? CLAUDE.md
```

Post-upgrade inspection:

```sh
if [ -e ./tmp-install/.claude/skills/independent-review/SKILL.md ]; then printf 'stale_skill=PRESENT\n'; else printf 'stale_skill=ABSENT\n'; fi; find ./tmp-install -path './tmp-install/.git' -prune -o -type f -print | sort; printf 'file_count='; find ./tmp-install -path './tmp-install/.git' -prune -o -type f -print | wc -l | tr -d ' '; printf '\nskills:\n'; find ./tmp-install/.claude/skills -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort; printf '\ngit_status:\n'; git -C ./tmp-install status --short
```

Output:

```text
stale_skill=ABSENT
./tmp-install/.claude/skills/craft/SKILL.md
./tmp-install/.claude/skills/experience/SKILL.md
./tmp-install/.claude/skills/experience/references/walk.md
./tmp-install/.claude/skills/experience/references/worst-day.md
./tmp-install/.claude/skills/judge/SKILL.md
./tmp-install/.claude/skills/map-build/SKILL.md
./tmp-install/.claude/skills/map-build/references/questions.md
./tmp-install/.claude/skills/shape-product/SKILL.md
./tmp-install/.claude/skills/shape-product/references/questions.md
./tmp-install/.claude/speck-next.json
./tmp-install/AGENTS.md
./tmp-install/CLAUDE.md
./tmp-install/map.md
./tmp-install/templates/decisions.md
./tmp-install/templates/map.md
./tmp-install/templates/piece.md
./tmp-install/templates/product.md
./tmp-install/templates/rounds.md
./tmp-install/templates/state.md
file_count=19
skills:
craft
experience
judge
map-build
shape-product

git_status:
?? .claude/
?? AGENTS.md
?? CLAUDE.md
?? map.md
?? templates/
```

The retired skill file was absent after upgrade. The CLI's “What changed” output named three untracked roots; the subsequent complete `git status --short` also named `map.md` and `templates/`.

## 6. Stance self-test

### Command

```sh
rg -n -C 1 'verdict|rule|Judge the recovery|observed broken|gathers nothing|runs no walks|collects no observations|orders? that experience|walk every promise|send for more' .claude/skills/experience .claude/skills/judge
```

### Experience side-by-side

The main skill says:

- `.claude/skills/experience/SKILL.md:3`: witnesses write records “with no verdicts in them.”
- `.claude/skills/experience/SKILL.md:16`: “live it, record it, rule nothing,” followed by a literal list of words the record never says.
- `.claude/skills/experience/SKILL.md:27`: “Then the `judge` skill rules. The witness never does.”

The required UI reference also says:

- `.claude/skills/experience/references/walk.md:13`: “Then behave badly: go back mid-flow, background the app, type garbage, kill the network, force an error. **Judge the recovery.**”
- `.claude/skills/experience/references/walk.md:22`: “A named, checkable rule observed **broken** goes in the record with the exact place it broke.” The main skill's line 16 includes that exact word in its list of words a record never says.

The first instruction uses ruling language as an imperative to the witness. The second tells the witness to put a word from the main skill's prohibited list into the record. The surrounding lines say the judge weighs/rules the observations, but neither of these two sentences rewrites its imperative in observational terms.

### Judge side-by-side

The judge skill says:

- `.claude/skills/judge/SKILL.md:8`: “The judge gathers nothing,” “runs no walks,” and “collects no observations of its own.” It may “send for more,” order an experience, and wait.
- `.claude/skills/judge/SKILL.md:3`: “May order more experiences before ruling; never gathers its own.”

One later instruction says:

- `.claude/skills/judge/SKILL.md:19`: “walk every promise and ask what delivers it now.”

“Walk” is the execution term used throughout the experience skill. This sentence does not say whether the judge walks the records or the product. I had to read it against line 8 and infer a record-only trace; the sentence itself does not contain that qualifier. I found no other instruction telling the judge to execute the product, collect an observation, or run a command. The explicit mechanism for an evidence gap is ordering another experience.

## 7. Contract consistency

### Command

```sh
rg -n 'receipt|States:|Shaped|Built|Judged|Live|works|delivers the promise|good to use|quality hangs together|witness|judge' AGENTS.md .claude/skills/experience/SKILL.md .claude/skills/judge/SKILL.md templates/*.md README.md CONTRACT.md
```

### Promise 3 — witness and judge

| Document | Exact claim | Side-by-side observation |
|---|---|---|
| `CONTRACT.md:19` | “Fresh witnesses ... the first-timer, the real job end to end, the least-privileged user, the worst day ... Then a separate judge who gathered none of it rules from the records.” | Names the two contexts and puts worst-day inside witness experience. |
| `AGENTS.md:28–30` | Fresh witness per substantial piece; separate fresh judge; milestone Experience lists first-timer, real job, second user, worst day. | Uses “second user,” while the contract uses “least-privileged user.” |
| `experience/SKILL.md:22–23` | Second user means both a least-privileged account attempting forbidden access **and** a second person on the same install looking for traces. | Expands the two shorter labels into one persona. |
| `README.md:20` | Experience list: first-timer, real job, worst day. | Omits the second-user persona in this phase summary. |
| `README.md:28` | Witnesses “log in as the least-privileged user” and judge is separate. | Restores the least-privileged move but does not mention the second person on the same install. |
| `templates/piece.md:11,13` | Separate Experience receipt and Judgment fields. | Keeps the contexts distinct. |
| `map-build/references/questions.md:19` | “what the reviewer attacks” plus what the experience walk covers. | Uses a present-tense reviewer role where the other surfaces name witness observations and judge rulings separately. |

### Promise 4 — state ladder and four items

| Document | Exact text |
|---|---|
| `CONTRACT.md:20` | “Four states: Shaped, Built, Judged, Live. Judged spells out the four verdicts separately — it works · it delivers the promise · it's good to use · the quality hangs together.” |
| `AGENTS.md:40` | “States: Shaped → Built → Judged → Live; Judged spells its four verdicts separately.” The names are given at line 30 as works · delivers the promise · good to use · quality hangs together. |
| `templates/state.md:6` | “States: Shaped → Built → Judged → Live; Judged spells four verdicts — works · delivers the promise · good to use · quality hangs together.” |
| `README.md:26` | “Four states, honest ones. Shaped, Built, Judged, Live,” followed by the same four items. |

The ladder and four-item names are textually the same across those four normative locations.

One internal README example differs in enumeration:

- `README.md:14`: the judge reports “works, on-promise, good to use on desktop and phone. Nothing open.”
- `README.md:26`: Judged spells four items separately, with “the quality hangs together” as the fourth.

The example does not name the fourth item before saying nothing is open.

### Outcome speech and backward routing

- `CONTRACT.md:20`, `AGENTS.md:30`, `README.md:26`, and `judge/SKILL.md:15` all reserve *proven* for the all-four-on-evidence outcome before Live.
- `templates/state.md:6` uses no `Proven` state and says an insufficient judgment routes backward.
- `AGENTS.md:20` and `judge/SKILL.md:21` name the three grounds and destinations. `CONTRACT.md:20`, `README.md:20`, and `templates/state.md:6` state backward routing without listing all three grounds.
- `templates/piece.md:13` supplies a routing slot naming the phase and trace.

### Owner ratification at every phase

This difference crosses the same documents:

- `CONTRACT.md:11`: each of the five phases has “a checkable exit that includes the owner's ratification.”
- `README.md:20`: “Every phase has a checkable exit that includes the owner's ratification in his own words.”
- `AGENTS.md:26–27`: Shape and Map explicitly require owner ratification.
- `AGENTS.md:28`: Build reaches land after experience and judge; no owner-ratification field is named for the piece.
- `AGENTS.md:29`: Experience exits when walks and records are in.
- `AGENTS.md:30`: Judge exits when verdicts are recorded, the owner has judged, and routed work re-entered. The owner's action here is described as grading felt experience, not as a ratification quote in a round record.
- `templates/piece.md` has no owner-ratification field. `templates/rounds.md` has one for Shaping or Mapping.

### Coined-word count

- `CONTRACT.md:30` defines the count as words an owner must learn, excluding filenames and internal shorthand, and claims four today: Shaped, Built, Judged, Live.
- `README.md:26` says those four words are “the entire vocabulary you need.”
- `AGENTS.md` requires agents to use or expose terms including live piece, ratified, milestone, substrate round, receipt, strain, shaped material, re-cut, and re-land. During the cold read, “strain,” “substrate round,” “receipt,” and “re-land” required later context or remained undefined on that page.

The contract's exclusion rule may place some of those outside the owner count; the README sentence does not state the exclusion rule. I did not find a mechanical coined-word inventory to compare with the claimed count.

## Limits

- **Untested:** UI walks, screenshots, accessibility checks, personas against an interactive product, and the worst-day runtime playbook. The subject supplied documents and a CLI installer, not a user interface.
- **Untested:** remote `npx github:Keegil/speck-next` install/upgrade. I ran the requested local `node bin/speck-next.js` entry point at the checked-out commits.
- **Untested:** an agent session progressing the fresh install through shaping and mapping. I therefore did not observe when the absent root `product.md`, `decisions.md`, and `state.md` files are instantiated from their templates.
- **Untested:** upgrade from old Speck eras, dirty repositories with existing tracked work, interrupted upgrades, retries, and reverts. The executed subject was one fresh empty git repository, then a same-version upgrade with one planted retired skill.
- **Untested:** whether upgrade creates one revertible commit in a repository that already has a baseline commit. The fresh repository had no commit before install; all installed paths remained untracked.
- **Untested:** package behavior at a tag different from the local checkout. The marker recorded version `4.0.0` and commit `0ea3592`.
- **Untested:** the development suite and its controls. No dev-suite command was part of the dispatch.
- **Untested:** whether all owner-facing product repositories use the vocabulary in practice. This run inspected the kernel surface and one fresh install only.
- **Untested:** the original owner conversation beyond the verbatim calls preserved in the top `decisions.md` entry. No separate transcript was supplied in the dispatch.
- **Not performed by stance:** any ruling on the observations above.
