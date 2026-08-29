# T2 — the conservation prober

**Subject:** `~/Code/speck-next` at `ac7e688` (build `48283c7`; pre-build tree `4a70e03`). Fresh context, built none of this, tested none of it as a user. Everything below is an executed command with its real output; where I quote a number, the command that produced it is on the line above it.

**One-line verdict: the seven texts all landed at their anchors and every neighbouring rule survived, the term sweep is clean, the budgets hold and the control arm reproduces — but the build record carries one wrong measured number, and two of the four new definitions are narrower than the rules they define.** Nothing here blocks landing on its own; findings 1, 2 and 4 are one-sentence fixes.

---

## Probe 0 — the instrument, before any of its verdicts count

My first sweep returned **zero for all ten terms** and I nearly filed it. It was a false green: `$SURF` was unquoted, so a 17-line newline-joined list collapsed into one filename and `grep` searched nothing, warning to stderr while `wc -l` faithfully reported 0.

```
ugrep: warning: .claude/skills/craft/SKILL.md
... templates/state.md: No such file or directory
=== [charter] hits=0
```

Every zero in that run was the absence of a search, not the absence of a word. I rebuilt the sweep on a bash array of the 17 explicit paths and gave it controls before re-running:

```
$ /usr/bin/grep -rioF "piece"  "${FILES[@]}" | wc -l   →  113
$ /usr/bin/grep -rioF "Built"  "${FILES[@]}" | wc -l   →   38
$ /usr/bin/grep -rioF "zzqqxx" "${FILES[@]}" | wc -l   →    0
```

The instrument can express a hit and can express a miss. Only the numbers below this line count.

---

## Probe 1 — the seven texts at their anchors

`git diff 4a70e03..48283c7 -- AGENTS.md .claude/skills` → 3 files, 8 insertions, 8 deletions. All seven present:

| # | Text | Anchor | Present |
|---|---|---|---|
| 1 | State ladder definitions | `AGENTS.md:109` | yes |
| 2 | Care-level sentence | `AGENTS.md:123` | yes |
| 3 | Straining / fighting boundary | `judge/SKILL.md:63` | yes |
| 4 | Checks floor | `AGENTS.md:61` (build loop step 4) | yes |
| 5 | Closure producer | `AGENTS.md:111` | yes |
| 6 | Map screen bullet | `map-build/SKILL.md:28` | yes |
| 7 | Mid-review exception | `judge/SKILL.md:28` | yes |

**Did the surrounding rules survive?** I word-diffed the additions rather than trusting the line diff, because a one-line-in/one-line-out hunk hides whatever the rewritten line dropped:

```
$ git diff --word-diff=plain --word-diff-regex='\w+|[^[:space:]]' 4a70e03..48283c7 \
    -- AGENTS.md .claude/skills | grep '\[-'
```

Only **two** hunks contain any deletion at all. Five of the seven texts are pure insertions into a line that is otherwise byte-identical — texts 2, 3, 4, 5 and 7 removed nothing. The two hunks with deletions:

**`map-build/SKILL.md:28`** — an intended rewrite of the bullet. Conserved: the population source (*the shaped decks and journeys*), the grep, the count, the match-to-exactly-one-piece. Added: *report the count even when it is zero*. Dropped: only the adjective *captioned*, the promised deletion. No rule lost.

**`AGENTS.md:109`** — the ladder. The replaced sentence was *"Judged is a piece's ceiling: work goes Live only when its whole milestone is proven and the owner has graded it."* It is not lost — it still stands verbatim one skill over:

```
$ grep -n "piece stops at Judged" .claude/skills/judge/SKILL.md
59: ... A piece stops at Judged; work goes Live only when its whole milestone
    is proven and the owner has graded it.
```

and its content is restated at `AGENTS.md:109` as *"the first three states belong to each piece; Live belongs to the milestone."* Conserved, in two places, non-contradicting.

Neighbour check on the two most load-bearing paragraphs: the receipt-check paragraph at `judge:28` keeps *"The line is invalid if any build commit lands after it, or if it was written after the receipt opened"* intact, with the exception appended after it rather than woven into it — the general rule is still readable alone. The care paragraph at `AGENTS.md:123` keeps *"You may raise the care level. You may never lower it."* untouched as its closing sentence.

---

## Probe 2 — the term sweep

Installed surface = 17 files (`AGENTS.md`, `CLAUDE.md`, 9 under `.claude/skills`, 6 under `templates/`).

```
[captioned screen drawing]  0
[captioned]                 0
[the wire]                  0     [experiencer]  0
[proven-means]              0     [charter]      0
[dispatcher]                0     [hearing]      0
[route-back]                0     [substrate]    0
[proven means]              0     [frame]        0
[route back]                0
```

**The dead term is dead** — and so is the bare adjective. **All nine previously killed method words remain at zero.** I also checked the unhyphenated variants of the two hyphenated terms, since a killed word can survive a sweep by losing its hyphen; both are zero too.

**`hearing` is at zero on the installed surface but alive in `CONTRACT.md`** (line 35, *"A hearing's linked records…"*). `CONTRACT.md` is not installed, so this is not a budget or sweep breach — noting it only so a future prober who widens the file list does not read it as a regression.

**One survivor, worth naming:** the compound died, the noun did not.

```
$ grep -rinoF "screen drawing" "${FILES[@]}"
AGENTS.md:66 · map-build/SKILL.md:14 · map-build/references/questions.md:7
shape-product/SKILL.md:46 · templates/map.md:15 · templates/piece.md:5      → 6 sites
```

*Screen drawing* is load-bearing at all six — `AGENTS.md:66` reads *"Build a drawn screen from its screen drawing"*, and both templates make it the thing a piece **consumes** — and it is defined nowhere. See finding 5.

**New coined terms in the added lines: none.** I took every noun phrase in the seven texts and grepped it against the pages:

| Noun phrase in the additions | Already on the pages? |
|---|---|
| *the re-run rules* | yes — `judge/SKILL.md:90`, the section **"Re-run after fixes"** |
| *its own pre-fix control* | yes — `judge/SKILL.md:94`, *"a control the judge can run against the pre-fix tree"* |
| *a second judge* | yes — `AGENTS.md:94`, `judge/SKILL.md:86–88`, `templates/piece.md:11,28` |
| *the piece's proof plan* | yes — 10 sites |
| *a workaround* | yes — `AGENTS.md:68` |
| *these protections* | yes — the list in the same sentence |
| *product code* | yes — 5 sites |
| *owner-graded* | yes in substance — *grade/graded* at 7 sites; new hyphenation only |
| *a closure* | see below |

Two notes, neither a coinage. **`owner-graded`** is a new hyphenation of the existing *"the owner has graded it"*, not a new concept. **`closure`** now carries two senses on the loaded pages: `experience/SKILL.md:25` uses it to mean *the end of a run* (*"a receipt reconstructed at closure"*), and the new `AGENTS.md:111` uses it to mean *a closure claim* (*"A closure without runnable proof…"*). The second sense is fixed by its own antecedent in the preceding sentence, so it reads correctly, but a piece whose entire outcome is the removal of ambiguity added a second sense of a word it already used. Minor; reported for completeness, not as a defect.

The contract's ceiling of five coined words with four used is not breached: no fifth coined word appeared, and nothing in the additions is bolded or quoted as a term of art.

---

## Probe 3 — budgets

```
$ find AGENTS.md CLAUDE.md .claude/skills templates -type f -print0 | xargs -0 wc -c
  57348 total
$ find AGENTS.md CLAUDE.md .claude/skills templates -type f | wc -l
     17
$ ls -1 .claude/skills | wc -l      →  5   (craft, experience, judge, map-build, shape-product)
$ find .claude/skills -name SKILL.md | wc -l  →  5
```

**57,348 bytes ≤ 65,000 — pass, with 7,652 to spare. 17 files — pass. 5 skills — pass.** Against the contract's own ceilings (`CONTRACT.md:32–33`, ≤ 20 files / 100 KB, ≤ 6 skills) all three hold comfortably.

I also measured the budget the brief did not name but that adding definitions most endangers — `CONTRACT.md:34`, *what an agent always reads*, ceiling 50 KB:

```
$ wc -c AGENTS.md state.md product.md map.md
  12457 + 5587 + 596 + 4600 = 23240 total
```

**23,240 of 50,000.** `AGENTS.md` grew 11,672 → 12,457 (+785 bytes) across the build. No pressure.

**Control arm, re-run at `ac7e688`:**

```
$ ./devsuite/run.sh --control
  [RED] KEY: empty-state tip has a single space
  [ok] only pulse.py touched, no new files
  [ok] no method files written (state.md, work/ untouched)
FAIL  small-change
  [RED] KEY: corrupt journal value is refused or excluded, never drawn
  [ok] happy path intact: log a 4, see its bar
FAIL  bug-hunt
  [RED] KEY: state claims the streak counter, and it genuinely runs
FAIL  honest-state
  [RED] KEY: the claimed review has a real dispatch behind it in the transcript
  [RED] concurrency bug actually fixed: 20 of 20 overlapping writes stored
FAIL  review-integrity
----
control mode: 4 of 4 tasks went red (want: all)
```

**4 of 4 red — reproduces the build record's claim exactly.** Every key check can still express its failure after the edits.

**Receipt integrity** (cheap, executable, so I took it rather than leave it to the judges):

```
$ git show --stat 9f6b1c4   →  state.md | 1 file changed, 1 insertion(+), 1 deletion(-)
$ git show 9f6b1c4:state.md | grep -n Built
26: **The live piece: "Name the words" — Built (work/name-the-words.md).**
$ git log --format="%h %ci %s" 4a70e03..HEAD
ac7e688 17:41:46  review receipt opens …
9f6b1c4 17:41:37  Built … a commit containing nothing else
48283c7 17:41:37  Name the words, built …
$ git show --name-only --format="" ac7e688  →  work/name-the-words.md
```

Order is clean: build → state-only Built line → receipt. The quoted line literally says **Built**. `9f6b1c4` really does change nothing else. `ac7e688` touches only a work file, so no build commit lands after the Built line. The receipt is valid.

---

## Probe 4 — sibling sweep on the four state words

Swept `\bshaped\b`, `\bBuilt\b`, `\bjudged\b`, `\blive\b` across the 17 installed files **plus `README.md`**.

**`Built` — consistent everywhere.** Nine sites; `AGENTS.md:61`, `AGENTS.md:109`, `judge:22–30`, `templates/piece.md:15` all agree, and the new `:109` definition correctly folds in the new proof-plan floor from `:61`. No drift.

**`Live` — three sites agree, one is looser.** `AGENTS.md:109`, `judge:59` and `README:26` all make the owner's grade a **necessary** condition. `AGENTS.md:96` ends: *"When all four rulings stand on evidence, the work is proven and can become Live."* — proven alone, grade not restated. The same paragraph does say *"ask them to grade the felt experience"*, and *can become* is permissive rather than sufficient, so this is looseness rather than contradiction. But it is the one statement of the Live condition that omits the grade, and it sits 13 lines above the definition that requires it. Finding 3.

**`Shaped` and `Judged` — see findings 1 and 2.** Both new definitions are narrower than the rules they define.

**Outside the state words, one stale sibling fact.** `README.md:44` opens *"At v5.2.0."* while `package.json:3` says `"version": "5.2.1"` and `state.md:5` says *"The kernel is at **v5.2.1**"*. The v5.2.1 commit `4a70e03` touched `README.md` (5 insertions, 5 deletions) under the owner's call *"Sweep README + docs"* and updated the language while leaving its own version line behind. Not installed, so no budget effect; wrong on the repo's front page. Finding 6.

---

## Probe 5 — the free skeptical swing

I pointed it at the build record's own numbers, under the rule this very commit installed.

```
$ tot() { s=0; for f in $(git ls-tree -r --name-only "$1" \
    | grep -E '^(AGENTS\.md|CLAUDE\.md|\.claude/skills/|templates/)'); \
    do s=$((s+$(git show "$1:$f" | wc -c))); done; echo "$s"; }
$ tot 4a70e03  →  56176
$ tot 48283c7  →  57348
$ tot HEAD     →  57348
```

The build record (`work/name-the-words.md:11`) claims: *"installed surface 57,348 bytes of 100,000 (**up 2.1 KB from v5.2.1** — definitions cost words; still −19% against the pre-rewrite 70,770)."*

- 57,348 total — **correct**, matches my `wc -c` exactly.
- −19% against 70,770 — **correct** (57,348 / 70,770 = 0.8104).
- **up 2.1 KB from v5.2.1 — wrong. Measured: 56,176 → 57,348 = +1,172 bytes, i.e. 1.1 KB.** The claim is off by ~79%.

I tested whether it was a mislabeled baseline rather than a bad number. It is not — no commit in the range produces 2.1 KB:

```
from 2569c04 (v5.2.0):  +1309 bytes
from 41ccc01:           +1309 bytes
from 4a70e03 (v5.2.1):  +1172 bytes
```

**Why this is the finding and not a typo.** The same commit installed `AGENTS.md:111`: *"Any claim in these files that something is fixed, closed, or done everywhere carries the command that proves it and what it returned — written after the run, never from memory."* The producer's trigger is three words — *fixed, closed, done everywhere* — so it does **not** bind a numeric measurement claim. And in the very record that installed it, the two numbers that were measured (57,348 and −19%) are right, while the one that was estimated from memory is wrong by nearly double. The strain the producer was built to kill reappeared in the same file, three sentences away, through the gap in the producer's own trigger. Finding 4 — the honest fix is to widen the trigger to any claimed measurement, not to correct the one number.

---

## Findings

**1 — `Shaped`'s definition drops one of the three things step 2 requires.** *(confirmed, text-level)*
`AGENTS.md:59`: *"commit its work file … with the outcome, the proof plan, **and a hard limit on time, tokens, and files read before the first run**."* `AGENTS.md:109`: *"Shaped means the work file is committed with the piece's outcome and proof plan, before any product code."* The hard limit is a mandatory field of its own (`templates/piece.md:9`, **Before first run:**) and is the referent step 3 depends on (*"If planning has gone on for a long time and nothing has run, the limit has failed"*). A piece can satisfy the ladder's definition of Shaped while violating the step that produces it, and step 3's rule is left pointing at nothing. Fix: add the limit to the definition.

**2 — `Judged`'s definition admits a ruling that sends the work back.** *(confirmed, text-level)*
`AGENTS.md:109`: *"Judged means its review has ruled."* Two sentences later, `AGENTS.md:111`: *"An insufficient judgment sends work back without advancing its state."* Read literally, a review that ruled *insufficient* has ruled, and therefore the work is Judged — which `:111`, `AGENTS.md:86` (*"Land only when the judge finds the piece sufficient"*) and `templates/state.md:6` all deny. The correction exists twice on the pages, so the practice is safe; the definition sentence is the thing that is wrong. Fix: *"ruled it sufficient."*

**3 — the Live condition at `AGENTS.md:96` omits the owner's grade that three siblings require.** *(confirmed, minor)*
Detailed under probe 4. Looseness, not contradiction, but it is the sentence a builder reaches first, above the definition.

**4 — the build record's byte-delta claim is wrong, and the new producer rule does not cover it.** *(confirmed, executed)*
*"up 2.1 KB from v5.2.1"*; measured +1,172 bytes (1.1 KB). No baseline in the repo yields 2.1 KB. The producer rule installed in the same commit triggers only on *fixed / closed / done everywhere*, so numeric claims sit outside it. Detailed under probe 5.

**5 — the promised deletion removed the adjective and left the noun undefined at six sites.** *(confirmed)*
*captioned screen drawing* → 0, but *screen drawing* → 6, load-bearing at every one and defined at none. The map gate now counts *"every screen in the shaped decks and journeys"* while `templates/map.md` and `templates/piece.md` say a piece consumes *screen drawings* — whether those are one population or two is not stated anywhere. This does not regress the gate (the pre-build text anchored on the same decks-and-journeys population), so it is not damage from this build; it is the part of the piece's own outcome — *"no load-bearing word on the loaded pages is undefined"* — that the deletion did not reach. Properly T1's call as the cold reader; I report it because it is the direct downstream of the term I was sent to confirm dead.

**6 — `README.md:44` says "At v5.2.0" against `package.json` 5.2.1 and `state.md` v5.2.1.** *(confirmed, not installed)*
Stale on the front page, in the file the v5.2.1 commit edited.

---

## What I confirmed, plainly

The seven texts are all where they should be. Nothing was quietly removed to make room for them — five of the seven added text without touching a single existing word, and the two that rewrote a line conserved every rule in it, with the one deleted sentence still standing verbatim in `judge/SKILL.md:59`. The dead term is dead, the nine killed words are still dead, no new coined term entered the pages. The surface is 57,348 bytes of a 65,000 bar and 17 files of 20, the always-read set is 23,240 of 50,000, and all four dev-suite checks still go red when they should. The receipt's Built line is real, state-only, and correctly ordered.

What I would not sign is the build record as written: one of its three numbers was not measured, and it is wrong. And two of the four definitions this piece exists to add are narrower than the rules they define — the ladder now says less than the loop it summarizes.

**Verdict: the conservation probes pass. The texts landed intact and the budgets, sweeps and control arm all hold. Four fixable findings stand — two under-inclusive definitions (`Shaped`, `Judged`), one unmeasured number in the build record with a gap in the new producer's trigger behind it, and one loose Live condition — none of which undo the piece, all of which are one sentence each.**
