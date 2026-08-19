# Re-witness record

**Subject:** fixed tree at `0a931e8ea73887412c590308db0fd11c9d3a1a8e`  
**Role:** fresh witness; no part in the build, first witness run, or judgment  
**Walks:** only the four walks named in `docs/reviews/v4-judge-rulings.md` defects 1–7

## 1. Stance self-test

I read each named surface with line numbers and searched sentence by sentence for two things: an instruction for the witness to rule, judge, or put one of the record terms prohibited by the experience stance into its record; and an instruction for the judge to run the product or collect an observation itself.

| Surface | Exact lines checked | What the text says now |
|---|---:|---|
| `.claude/skills/experience/SKILL.md` | 1–27 | No hit observed. Lines 8, 16, 25, and 27 assign gathering and reporting to the witness and rulings to the separate judge. Line 21 asks the worker to chase the request, changed record, and read-back, then record what was or was not found. |
| `.claude/skills/experience/references/walk.md` | 1–27 | No hit observed. Lines 3 and 7 say the record supplies material for the judge. Lines 9–17 and 21–25 ask for observations, mechanism traces, and felt reports. |
| `.claude/skills/judge/SKILL.md` | 1–23 | No hit observed. Line 8 says the judge reads records and attached evidence, runs no walks, and collects no observations. Line 19 says to trace each promise through those records and evidence. Line 23 assigns the exact re-walk to the re-dispatched witness. |
| `.claude/skills/map-build/references/questions.md`, question 7 | 17–20 | No hit observed. Line 19 separates what runs, which walks the witnesses live, and what the judge rules on. |

## 2. Cold read

I read `AGENTS.md` from line 1 through line 60 once, then `README.md` from line 1 through line 44 once.

### Stops in `AGENTS.md`

- Lines 15–17 use `ratified` before line 22 defines it. I paused at line 15, then the later definition resolved the term.
- Line 27 requires a substrate choice at a “stated care level.” The page explains the substrate in the same sentence, but it gives no care-level scale, choices, or pointer. I could not state that level from the page alone.
- Line 31 requires the `craft` bar. The page does not explain that bar or point to the skill that contains it. I could run the rest of step 3, but not apply that named bar from this page alone.

The build loop is presented as six ordered actions at lines 28–34. I could follow their sequence. The unresolved `craft` bar above remains inside step 3.

At a landing, lines 34, 38, and 46 tell me to rewrite `state.md` from current evidence, mark the finished piece on `map.md`, make the next piece live, and fill six named sections. Line 46 also says how to record the four judgment fields and a routed-back judgment.

The plain rendering for the owner lives in the conversation: line 9 says to write it there and link the artifact beside it. Lines 19 and 36 point the dispatcher back to that rendering for the owner's grade.

### Stops in `README.md`

- Line 14 calls the second judgment field `on-promise`; `AGENTS.md` line 36 names that field `delivers the promise`. I stopped to compare whether these were intended as the same field.
- Line 24 says everything on disk is five files and a page; line 38 says an install contains 19 files. I had to re-read line 24 as a description of working artifact kinds rather than a literal tree count. The heading itself does not make that boundary explicit.
- Line 26 says the four state names are the only words Speck Next asks the owner to learn. Line 32 later uses `sound`, `straining`, and `fighting` as named structural calls the owner will encounter. I had to reconcile the “only words” sentence with that later vocabulary.
- Line 30 says the small-change conditions are defined there, but it omits the `AGENTS.md` line 54 condition that the change rewrites no promise. From the README list alone, I could classify a promise-changing edit as small.
- Line 34 introduces “extra-care packs” without contents or a pointer. I could identify the risky areas, but not what actions the pack adds.
- Line 36 says upgrading is one command but does not print or link that command. I could not perform the upgrade from the README instruction alone.

## 3. Consistency grep

### `templates/piece.md` against the two skills

- The experience skill's dispatch fields are at lines 12–16. The piece template line 11 contains witness tool/model/session, dispatch date and commit, planned personas, planned walks and commands, run owner, the empty-record instruction, and the returned record.
- The judge skill's receipt fields are at line 10, and its ruling fields are at lines 12–21. The piece template line 13 contains judge tool/model/session, date, subject and commit, per-promise fields, all four separately named quality fields, structure, additional walks, and backward routing.
- Planned commands are present at piece template line 11. All four quality fields are named at line 13.

### `templates/rounds.md` against the Shape and Map exits

- `AGENTS.md` lines 26–27 require a fresh witness, a separate judge, a receipt, and owner ratification for both Shape and Map.
- The rounds template line 13 opens the phase exit review before the ratification ask. Line 15 contains the witness receipt; line 16 contains the separate judge receipt; line 18 contains the plain-rendering ratification round and the owner's dated verbatim words.

### `README.md` example and personas

- The example at line 14 contains four judgment fields. Its second label is `on-promise`, while the canonical second label appears at `AGENTS.md` line 36 as `delivers the promise`.
- The phase summary at README line 20 names the first-timer, real job, second user, and worst day.
- The fuller explanation at README line 28 mentions the least-privileged account meaning of second user. It does not mention the second-person-on-the-same-install meaning stated in the experience skill at line 22.

### `CONTRACT.md` phase-exit sentence

`CONTRACT.md` line 11 now says Shape and Map exit on owner ratification, Judge exits with the owner's felt grade, and the owner action for Build, Experience, and Judge individually remains an open owner question tracked in `state.md`.

The phase exits in `AGENTS.md` say: Shape ratification at line 26; Map ratification at line 27; the Build landing action at line 34; Experience completion when its walks and records are in at line 35; and the owner's felt grade during Judge at line 36. The contract sentence no longer says every phase receives ratification; it distinguishes the currently named owner actions and names the open question.

## 4. Installer count

I created `./tmp-install`, initialized it as a fresh Git repository, entered it, and ran:

```text
node ../bin/speck-next.js install
```

The installer printed:

```text
Installed Speck Next v4.0.0 into /private/tmp/claude-501/-workspace-speck/a0e0d32c-31ec-4aba-a433-2bd88364f16f/scratchpad/v4-rewitness-97Uk/repo/tmp-install — 19 files on disk (method files, the version marker, an empty starter map).
Next: open an agent session there and say what you want to build — shaping starts in that conversation.
```

I counted regular files while pruning the fresh repository's `.git` directory:

```text
find tmp-install -path 'tmp-install/.git' -prune -o -type f -print | wc -l
```

| Installer's printed count | Witness file count |
|---:|---:|
| 19 | 19 |

The count enumerated these paths:

```text
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
```

## Limits

Nothing inside the four named re-walks was untested. Outside this dispatch, the interactive four-persona product walk, a complete lifecycle with backward re-entry, the development-suite limit controls and their positive controls, remote installs, and historical or interrupted upgrade cases remain untested here; those are separate ordered experiences at `docs/reviews/v4-judge-rulings.md` lines 70–73.
