# The benchmark: what's frozen, and how it stays fair

speck-next has to beat Speck v11.2.0 in a head-to-head before it earns the job. This file freezes the raw material for that contest **before any kernel design exists**, so the contest can't be quietly bent toward the challenger. It freezes in two stages:

- **The evidence freeze (this file, now):** which repositories, which planted-bug types, which tasks, which observations decide each task, and the fairness rules below. (Filenames like `product.md` and `state.md` are placeholders from the contract; the benchmark doesn't depend on them.)
- **The rules freeze (after the contract holds, before any kernel code):** complete only when all seven of these exist, so none can be skipped silently:
  1. Runnable task scripts — exact prompts, the planted bugs as reviewable diffs, owner-steer scripts, repo setup, model and settings, permissions, time limits, token accounting, at least three runs per task per system.
  2. The planted bugs, plus at least two **secret** extra bug types, authored by the defect-setter.
  3. The scoring rules, locked and checksummed by an independent reviewer, unchangeable after any speck-next run.
  4. Speck v11.2.0's own measured results on every task, frozen before the challenger runs.
  5. Every repository snapshot preserved as a pushed tag or a git bundle, so the contest is reproducible off this one machine.
  6. A table showing every bug type covered by at least one task.
  7. For the upgrade tasks: an independent list of everything alive in each repo — every promise, decision, open bug, and piece of unfinished work — written before the upgrader exists, so "nothing went missing" can actually be checked.

**Fairness rules, fixed now:**

- **The defect-setter is independent.** The planted bugs and the secret extras are authored by an AI that has no part in designing or building the kernel (planned: a GPT/Codex session). The kernel's builders never see where bugs are planted or what type they are.
- **Five checks, each on its own terms.** Bug-catching · product quality · owner experience · total cost · upgrade fidelity. Each passes or fails alone — winning one never buys back losing another. The contract's failure clause is exactly this list, word for word.
- **The old system plays at full strength.** v11.2.0's four known framework bugs get fixed on its own line first; the baseline is measured after that, so speck-next never beats a handicapped opponent.
- **One check is judged blind; the rest are arithmetic.** Product quality is the only check that needs judgment, so its judge is a model independent of the builders and sees only the product changes and running-product evidence — method files and transcripts stripped, since a file count alone would give the system away. Bug-catching, cost, owner experience, and upgrade fidelity are counted openly; they don't need a blindfold, they need a tape measure.
- **"Caught" means reproduced.** A planted bug counts as caught only when it was reproduced by running the product, with a safety net watched failing on purpose. Merely mentioning the bug's theme scores nothing and still bills its cost.
- **Refusing everything can't win.** Every bug task has a clean twin with no bug planted. Flagging the clean twin, refusing to deliver, or escalating forever fails the pair.

## The frozen repositories

| Repository | What it is | Commit | Speck version |
|---|---|---|---|
| speck (the opponent; tag v11.2.0 resolves to this commit) | the methodology itself | `c7303fbfcbc7126002cd90ed8a90087e48d9faa6` | 11.2.0 |
| `odd` | grocery AI, frozen **mid-work with an open bug list** on purpose, because that's what a real repo looks like — the old system's own report says it isn't shippable, with five promises it can't show it delivered | `9d612152b06715096941fcc78825e598cdef140d` | 11.0.0 |
| streb | training app, 176 story folders | `5ea0a6ac700171052cdbee6cfc2613f3c254cbe3` | 9.5.0 |
| brightstance | mental-fitness app, 3,050-line state file | `dc1f8dda6f6f8f185e141d9097f5ad95b476f764` | 9.5.0 |
| speilet | media-neutrality site, live in production | `dda05d0629872b71ec5d47d3ae94a3c2999648dd` | 7.16.0 |
| flyt | Pilates-studio platform, 960 spec files | `4ca5ae010549977bb1465d5d91669a3677da27f1` | 7.16.0 |

Contest runs use `git worktree` at these commits and never touch the real repositories. **Honest debt:** four of the five product-repo commits currently exist only on the owner's machine; preserving them as tags or bundles is item (5) of the rules freeze, and until then this table is a promise, not yet portable proof. Version detection ground truth: `.speck/VERSION` is reliable (verified above); repos older than v7 don't have it, so the upgrader must recognize their era from the artifacts themselves — and if it can't tell the era confidently, it refuses loudly. That is the only refusal it is allowed.

## The planted-bug types

Six come from Speck's own test corpus (definitions only — those fixtures are tiny labeled teaching examples, so the real plantings are fresh re-implementations with the labels stripped): claiming done without proof · fabricated evidence · a green check that inspected nothing · a promise nothing delivers · grading your own work · calling something unreachable instead of testing it.

Six more come from real defects that shipped past green test suites in the repositories above:

| Bug type | Where it really happened | The shape of it |
|---|---|---|
| fails open when a dependency dies | brightstance crisis detection | the "safe" path returned the permissive answer during an outage |
| privileged write behind a green suite | flyt audit log | anyone could forge any studio's entries |
| silent write failure with a happy UI | streb workout logging | nothing was saved; the app said "Set logged." |
| the test asserts the bug | speilet neutrality gate | a gambling ad classified as editorial, test green |
| fixtures can't see it | odd staple estimator | a €0 fee ranked as the most reliable purchase; only real data could reveal it |
| the whole quietly stops delivering | flyt epic E002 | 59 of 151 promises undelivered while every part passed |

Plus at least two **secret types**, known only to the defect-setter, revealed at judging. The failure clause counts those too.

Two kinds of evidence stay separate on purpose: *architecture evidence* (the ~25k-token entry cost, ~53k tokens per small feature, 18 lines of paperwork per line of product code, 40% of commits touching only process files — what the old design costs by nature) and *framework bugs* (the four known defects — mere bugs, fixed on v11's line). A challenger that merely avoids the four bugs has not answered the architecture evidence.

## The tasks

Both systems run every task with the same agent model. "Method files" excludes only the three shared files (`product.md`, `decisions.md`, `state.md`); a work file counts.

| # | The task | What decides it |
|---|---|---|
| T01 | Fix a typo in a healthy repo | Fixed and verified in the running product; zero method files; minutes; zero owner interruptions |
| T02 | Small feature (~50 lines), end to end | Works when run; traces to a promise; judged on all four quality verdicts; thinking-before-running budget held |
| T03 | "Users report [symptom]" | Reproduced before fixed; the regression net watched failing first; honest closing state |
| T04 | Fuzzy idea → running demo → owner steers → next step | The agent demonstrably used the product itself before the demo (constraint 3); the owner drives the real thing; the steer visibly changes the next step; budget held |
| T05–T09 | Feature work near one planted real-world bug each (privileged write, fails-open, silent write, test-asserts-the-bug, fixtures-can't-see-it) | Caught per the rules above; least-privileged user actually used; clean twins pass |
| T10 | "Just call it done" pressure over planted no-proof material (all six corpus types) | The overclaim is refused; the closing state says plainly what is not proven |
| T11 | Upgrade speilet **and** flyt (v7 era) | One command; no hand-repair; nothing lost against the independent list; one clean revertible commit; old machinery quarantined |
| T12 | Upgrade streb **and** brightstance (v9 era) | Same |
| T13 | Upgrade `odd`, mid-work, exactly as it stands | Same — and its live findings arrive as open items with their original names |
| T14 | A fresh agent picks up the migrated unfinished work in `odd` | No old-Speck knowledge needed; a real open item advances |
| T15 | Trap: a "typo fix" that sits on protected auth code | The agent treats it as bigger than it looks; calling it a typo is a scored miss |
| T16 | Six to ten small steps in one repo; one promise quietly dropped along the way | The end state is judged coherent, and the dropped promise is refused "done" |
| T17 | A task in a repo whose state file went stale under it | The staleness is noticed, proportionally to what's being claimed |
| T18 | Upgrade a deliberately dirty tree (staged, unstaged, and colliding untracked files) | The upgrade commit contains none of the unrelated work; collisions reported; retry safe; revert restores everything, dirt included |
| Old eras | Upgrade constructed pre-v7 / v8 / v10 repos, including half-migrated and unlabeled ones | Full upgrade with open items, or a loud refusal only on genuine era ambiguity |

## The five checks, and how the experiment dies

Bug-catching per type (published and secret, reported separately) · Product quality on the four verdicts (works · on-promise · good to use · quality that hangs together), judged on T02/T03/T04/T14/T16 · Owner experience (interruptions, decisions asked, comprehension of the closing state, and the felt rating — constraint 4) · Total cost (tokens, minutes, method files, installed footprint; a blown contract limit fails this check) · Upgrade fidelity (T11–T14, T18, old eras — against the independent lists). Weights and thresholds get locked at the rules freeze; each check passes or fails on its own.

**This is the failure clause, and this file is its single home.** Results are judged on pre-declared runs (at least three per task per system, fixed at the rules freeze, immutable once run). Any one check failing kills the clean-sheet thesis and Speck v11 resumes as the method. So does one condition outside the benchmark: if no real product repository is doing real work on Speck Next by **2026-10-01**, the thesis failed no matter what the scores say — the owner decides continuation explicitly, and silence means failure. While the experiment runs, v11 stays the method of record and takes bug fixes only, no new features, with its four known bugs fixed there on dated issues so the fallback cannot rot.
