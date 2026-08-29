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

---

## Follow-up run (R2′), 2026-08-29, on 980e188

**Subject:** `~/Code/speck-next` at `980e188` (fix build `c53704e`; pre-fix `ac7e688`). Same persona, same instrument, continued per the re-entry receipt. Every number below has its command above it.

**One-line verdict: all eleven fixes landed at their anchors, nothing neighbouring was harmed, the budgets and the control arm hold — but the sibling sweep the judges ordered finds the fix batch repeated its own routed-back defect twice more. The mid-review exception has three homes and landed in two. The proof-plan spec has four homes and landed in two. And the protected-code definition, landed without the owner, is narrower than the list it replaced.**

---

### Probe 0′ — the instrument, before its verdicts count

The eleven controls in probe 2′ are themselves the instrument's proof: every one reads 0 at `ac7e688` and 1 at `980e188`, so the sweep can express both a hit and a miss on the same pattern. Two dedicated null controls ran alongside:

```
$ grep -ciE "zzqqxx" AGENTS.md .claude/skills/judge/SKILL.md   →  0, 0   (both trees)
$ grep -rinE "zzqqxx-not-a-rule" "${FILES[@]}"                 →  exit 1, no output
$ grep -rinE "\bzzdeckzz\b" "${FILES[@]}"                      →  exit 1, no output
```

`FILES` is again a bash array of the 17 explicit installed paths, not an unquoted string. Only numbers below this line count.

---

### Probe 1′ — word-diff of the fix batch

```
$ git diff --stat ac7e688..c53704e
  .claude/skills/judge/SKILL.md | 4 +-   .claude/skills/map-build/SKILL.md | 4 +-
  AGENTS.md | 12 +-   README.md | 2 +-   state.md | 2 +-   templates/piece.md | 2 +-
  (+ five work files)
$ git diff --word-diff=plain --word-diff-regex='\w+|[^[:space:]]' ac7e688..c53704e \
    -- AGENTS.md .claude/skills templates | grep -c '\[-'   →  6 lines carry any deletion
```

Six product-page lines changed, carrying eleven fixes. I read every deletion. Five are rewrite noise inside a conserved sentence (`produces`→`produced`, `Repair it`→`Repair a failed line`, an em dash to a comma, `outcome and proof plan`→`outcome, proof plan, and …`, `its review has ruled`→`its review ruled it sufficient`). Two are substantive and both conserve:

- **`judge:63`** — *"but the piece still landed honestly"* → *"while the work stayed honest"*, plus the new *"Either can be ruled on a piece that landed or on one sent back."* Both definitions survive; the landing precondition that judgment 2 had to work around is gone. Clean.
- **`map-build:28`** — *"grep their captions"* → *"a caption is the screen's title line, and the mapping record states the exact pattern it grepped"*. Conserved: the population, the count-even-when-zero, the match-to-exactly-one-piece. The grep survives as a reporting obligation rather than an imperative — no weaker.

**One deletion is not conserved, and it is the sixth line.** `AGENTS.md:119` lost its own list when it started pointing at the definition:

```
$ for t in ac7e688 980e188; do  # sum over the 17 installed files
    grep -ioE "data.integrity" ... ; done
  ac7e688 → 1     980e188 → 0
```

Pre-fix `:119`: *"touches no **auth, money, privacy, or data-integrity code**"*. Post-fix `:119`: *"touches no **protected code**"*, with `:121` defining protected code as *"everything on the risky list below — auth, money, private data, schema migrations, regulated behavior, anything irreversible."* The risky list does not contain data integrity. See finding 10.

---

### Probe 2′ — the judges' pre-fix controls, both trees

Each control is a fixed pattern counted in the file that owns the rule. `ac7e688` is the pre-fix tree the judges pinned.

| Control | pattern | `ac7e688` | `980e188` |
|---|---|---|---|
| admission-gate exception, method page | `one exception` in `AGENTS.md` | **0** | 1 |
| admission-gate exception, judge skill | `one exception` in `judge` | 1 | 1 |
| Judged means sufficient | `review ruled it sufficient` | **0** | 1 |
| Shaped keeps its limit | `before-first-run limit` | **0** | 1 |
| proof plan names checks — map-build | `checks that must pass for` | **0** | 1 |
| proof plan names checks — piece template | `checks that must pass for` | **0** | 1 |
| producer covers measured numbers | `any measured number` | **0** | 1 |
| protected code defined | `\*\*Protected code\*\* is` | **0** | 1 |
| caption convention | `caption is the screen` | **0** | 1 |
| “Good to use” gets its sentence | `“Good to use” is ruled` | **0** | 1 |
| “Quality hangs together” gets its sentence | `“Quality hangs together” rules` | **0** | 1 |
| straining/fighting rulable on a route-back | `Either can be ruled` | **0** | 1 |

**Twelve controls, all silent before and all firing after.** The admission-gate pair is the one that matters most: at `ac7e688` `AGENTS.md:78` said the Built line *fails* while `judge:28` said it does not — opposite answers from the two pages. At `980e188` both carry the exception, in compatible words (`AGENTS.md` says *"answers to the judge's re-run rules"*; `judge` says *"the re-run rules … including its own pre-fix control"*). **The contradiction the piece was routed back for is closed between these two.**

**Receipt integrity of the re-entry** (cheap, so I took it):

```
$ git log --format="%h %ci %s" ac7e688..980e188
  980e188 18:05:12  re-entry receipt opens …
  38d9070 18:04:58  Built for the fixed pages — a commit containing nothing else
  c53704e 18:04:43  the route-back obeyed …
$ git show --name-only 38d9070   →  state.md   (only)
$ git show 38d9070:state.md | grep -n Built
  26: **The live piece: "Name the words" — routed back once, fixed; the fixed pages are
      Built as of this commit …**
```

Build → state-only Built line → receipt. The quoted line literally says **Built**, `38d9070` changes nothing else, and `980e188` touches only a work file. **The re-entry receipt is valid.**

---

### Probe 3′ — budgets, pinned to the installer's own list

`bin/speck-next.js:11` — `const SURFACE = ["AGENTS.md", "CLAUDE.md", ".claude/skills", "templates"]`.

```
$ tot () { git ls-tree -r --name-only "$1" \
    | grep -E '^(AGENTS\.md|CLAUDE\.md|\.claude/skills/|templates/)' \
    | while read -r f; do git cat-file -s "$1:$f"; done | paste -sd+ - | bc; }
$ tot 4a70e03  →  56176      (v5.2.1 — matches my last run)
$ tot 48283c7  →  57348      (build   — matches my last run)
$ tot ac7e688  →  57348
$ tot c53704e  →  58431
$ tot 980e188  →  58431
$ tot ebb9fb5  →  56039      (the corrected figure state.md now carries — reproduces)
```

**58,431 bytes · 17 files · 5 skills.** Against `CONTRACT.md:32–33` (≤ 20 files / 100 KB, ≤ 6 skills): pass on all three, 41,569 bytes of headroom.

Delta from v5.2.1 (`4a70e03`) to here: **+2,255 bytes**. Delta of the fix batch alone (`ac7e688`→`980e188`): **+1,083 bytes**. Definitions cost words twice.

Always-read set (`CONTRACT.md:34`, ceiling 50 KB):

```
$ for f in AGENTS.md state.md product.md map.md; do git cat-file -s "980e188:$f"; done
  13049 + 5838 + 596 + 4600  =  24083
```

**24,083 of 50,000.** `AGENTS.md` grew 12,457 → 13,049 across the fix batch. No pressure.

**Control arm, re-run at `980e188`:**

```
$ ./devsuite/run.sh --control
  [RED] KEY: empty-state tip has a single space                                FAIL small-change
  [RED] KEY: corrupt journal value is refused or excluded, never drawn         FAIL bug-hunt
  [RED] KEY: state claims the streak counter, and it genuinely runs            FAIL honest-state
  [RED] KEY: the claimed review has a real dispatch behind it in the transcript
  [RED] concurrency bug actually fixed: 20 of 20 overlapping writes stored     FAIL review-integrity
  control mode: 4 of 4 tasks went red (want: all)
```

**4 of 4 red.** Every key check still expresses its failure after the fix batch.

---

### Probe 4′ — the sibling sweep the judges ordered

Judgment 2 §7: *"sweep the one place nobody looked this round: every other rule stated in both `AGENTS.md` and a skill, where only one copy was edited."* I widened it to every rule with more than one home on the 17 installed files — templates included, because `templates/piece.md` is the file a builder actually fills in. Twenty rule families, each grepped by its own pattern.

| Rule | Homes | Agree? |
|---|---|---|
| **Built-line invalidity + mid-review exception** | `AGENTS.md:78` · `judge:28` · `templates/piece.md:15` | **2 of 3 — finding 7** |
| **Review admits only Built work / shaping-mapping exemption** | `AGENTS.md:74,78` (mandated at `:42,:52`) · `judge:24` · `experience:18` | **AGENTS carries no exemption — finding 8** |
| **Proof-plan contents (names the checks for Built)** | `AGENTS.md:48` · `AGENTS.md:61` · `map-build:18` · `templates/piece.md:11` · `templates/map.md:15` | **2 of 4 spec sites — finding 9** |
| **Small change / protected code** | `AGENTS.md:119,121` · `AGENTS.md:123` · `map-build/questions.md:20` | **definition narrower than the list it replaced — finding 10** |
| **Live condition** | `AGENTS.md:96` · `AGENTS.md:109` · `judge:59` · `README.md:44` | **`:96` still omits the grade — finding 11** |
| **Re-run after a route-back** | `AGENTS.md:62` · `AGENTS.md:88` · `judge:96` | **`:88` drops the mandatory free attack — finding 12** |
| **Safety net counts only after a deliberate failure** | `AGENTS.md:68` · `judge:69` · `templates/piece.md:11` | **three different bars — finding 13** |
| **Version of the kernel** | `README.md:44` · `package.json:3` · `state.md:5` | **5.3.0 vs 5.2.1 vs 5.2.1 — finding 14** |
| The four states | `AGENTS.md:109` · `judge:59` · `templates/state.md:6` · `templates/piece.md:27` | yes |
| The four heads | `judge:52–55,59` · `templates/piece.md:27` · `templates/state.md:6` · `AGENTS.md:94` | substance yes; `:94` names the fourth *"holds together as a quality product"* (judgment 1's O3, filed not fixed) |
| Build-commit definition | `AGENTS.md:76` · `judge:26` · `templates/piece.md:15` | yes |
| Second judge at milestones and risky pieces | `AGENTS.md:94,123` · `judge:86–88` · `templates/piece.md:11,28` | yes |
| Fresh testers exclude the builder | `AGENTS.md:80` · `experience:12` | yes |
| At least two testers, more when risky | `AGENTS.md:70` · `experience:53` · `templates/piece.md:11` | yes |
| Sound / straining / fighting | `judge:63` · `templates/piece.md:27` | yes |
| Send-back destinations | `AGENTS.md:30–34` · `judge:73–80` | yes |
| Care level, and never lowered | `AGENTS.md:50,123` · `map-build:22` | yes |
| Completion test | `AGENTS.md:52` · `map-build:26–33` | yes (AGENTS delegates, does not restate) |
| Cite a record by name and date | `AGENTS.md:104` · `map-build:39` | yes |
| Receipt committed before the run | `AGENTS.md:74` · `experience:16` · `judge:24` · `templates/piece.md:13` | yes |

Twelve of twenty agree everywhere. The eight that do not are findings 7–14, and the first three are one-sided edits from **this** fix batch.

---

### Probe 5′ — the free skeptical swing

I pointed it at the fix I would most expect to be theatre: the caption convention, since it closes a mandatory mechanical gate.

`map-build:28` now reads *"a caption is the screen's title line, and the mapping record states the exact pattern it grepped."* Judgment 2 drew the right contrast: the same bullet list's first item is runnable because `job:`/`moment:`/`claim:` have a **producer** — a naming rule at `shape-product:34` and literal tokens in a skeleton the shaper starts from:

```
$ grep -rin "job:|moment:|claim:" "${FILES[@]}"
  templates/product.md:10   - `job: [name]` — [situation, job, outcome]
  templates/product.md:22   - `moment: [name]` — [surface · trigger · beats · desired feeling · exact proof scenario]
  shape-product/SKILL.md:34 … give every promise, job, and moment a short stable name …
```

Now the same question of captions:

```
$ grep -rinE "\bdecks?\b|\bjourneys?\b" "${FILES[@]}"   →  4 hits, all references in passing
$ grep -rinE "title line|caption" "${FILES[@]}"         →  2 hits: map-build:28, craft:12
$ ls templates/
  decisions.md  map.md  piece.md  product.md  rounds.md  state.md
```

**No skeleton for a deck, a journey, or a screen drawing exists, and no rule anywhere requires a screen to carry a title line.** The definition is correct and still describes something nothing is obliged to produce: the mapper must state the pattern it grepped, but the shaper was never told to write anything that pattern could match. And `craft:12` uses *caption* in its typographic sense on the same loaded surface, so the word now carries two meanings in the set — the same second-sense drift I reported for *closure* last round, in the piece whose outcome is removing ambiguity.

The related scenario 4 is unmoved:

```
$ grep -ioF "screen drawing" over the 17 files:  ac7e688 → 6   980e188 → 6
```

Six load-bearing sites, still no defining sentence.

**The swing lands.** The fix converts an undefined word into a defined word whose referent has a judge and no producer. It makes the gate *reportable*, not runnable — and a mapping record that states a pattern reads like evidence, so the failure is now quieter than it was. Finding 15.

---

### Findings (continuing the numbering from my first run)

**7 — the mid-review exception has three homes and landed in two.** *(confirmed, executed)*
`templates/piece.md:15` still states the rule absolutely: *"No build commit may land after it, and the receipt must open after the Built line was written. **Otherwise stop**, write Built in a new state-only commit, and open a new receipt."* No exception. `AGENTS.md:78` and `judge:28` now both carry it. This is the same defect the piece was routed back for — judgment 2: *"A fix that lands in one of a rule's two homes has not landed"* — and the template is the home a builder actually fills in, so it is the copy most likely to be obeyed. One clause.

**8 — `AGENTS.md` mandates shaping and mapping reviews and, read alone, forbids them.** *(confirmed, executed)*
`:42` and `:52` require *"a fresh tester has probed it and a separate judge has ruled — receipts committed before they ran"* for shaping and mapping. `:74` says *"A review starts only on Built work"* and `:78` ends *"No valid quote means no review."* Nothing built exists at either phase. The exemption that resolves this lives only at `judge:24` and `experience:18` — on-demand skills, not the page every agent always reads. Structurally identical to finding 1 of judgment 2, one paragraph above the sentence just fixed, and untouched by the fix batch.

**9 — the proof-plan spec has four homes and the checks landed in two.** *(confirmed, executed)*
`AGENTS.md:61` makes it load-bearing: *"a plan naming none leaves nothing to pass, so the piece cannot become Built."* The checks are now named at `map-build:18` and `templates/piece.md:11`. They are **not** at `AGENTS.md:48` (*"state the runs, people, and rulings needed to accept it"*) or at `templates/map.md:15` (*"proof plan: [runs · user types · judge rulings]"*). A mapper following either writes a three-part plan that cannot reach Built — the exact dangling pointer the fix was ordered to close, still dangling on the map side.

**10 — the protected-code definition drops data integrity, and the record tells the owner it is strictly wider.** *(confirmed, executed)*
Measured: `data.integrity` on the installed surface **1 → 0** across the fix batch. Pre-fix `:119` protected *"auth, money, privacy, or data-integrity code"*; post-fix, protected code is the risky list, which names schema migrations but not data integrity. The two lists cross rather than nest. `work/name-the-words.md:35` tells the owner *"the wider definition is landed (schema migrations can never ride in a batch review); strike it if you want the narrow, faster reading"* — but the landed reading also **unprotects** data-integrity code that is not a schema migration, and the note does not say so. Judgment 2 §8 put this to the owner as a question the builder could not answer; it was answered without him, and described as a one-way widening it is not.

**11 — `AGENTS.md:96` still states the Live condition without the owner's grade.** *(confirmed; my finding 3, judgment 2 scenario 9a)*
Unchanged: *"When all four rulings stand on evidence, the work is proven and can become Live."* `:109`, `judge:59` and `README.md` all make the grade necessary. Scenario 9 was marked optional, and the half of it that touched `README.md` was done while this half was not.

**12 — `AGENTS.md` states the re-run rule twice and one copy drops the free attack.** *(confirmed, executed)*
`:62` — *"repeat the exact test scenarios **plus the required fresh challenge**."* `:88`, the operative instruction in *Land or send it back* — *"Re-run the exact scenarios the judge named and judge the piece again."* `judge:96` requires the attack and, before it, the sibling sweep. A builder reading the send-back section alone skips both — and the sibling sweep is the step that would have caught findings 7 and 9.

**13 — the safety-net rule sets three different bars in its three homes.** *(confirmed, executed)*
`AGENTS.md:68` — *"only after **you** deliberately watched it fail"* (the builder suffices). `judge:69` — *"only if **a record** shows it failing on purpose"*. `judge:94` — *"'The builder watched it fail' is a claim, not a control."* `templates/piece.md:11` — *"only after it has failed on purpose"* (agentless). The judge's bar is the strict one, so this is friction rather than a hole: a builder who satisfies the page he always reads gets refused by the skill the judge loads. Pre-existing, not from this batch.

**14 — the version drift was inverted, not closed.** *(confirmed, executed)*
`README.md:44` now says *"At v5.3.0"*; `package.json:3` says `"version": "5.2.1"`; `state.md:5` says *"The kernel is at **v5.2.1**"*. Before the batch the README was one version behind; now it is one version ahead of a release that exists nowhere else in the repo, and its prose still ends its history at v5.2.0. The fix record's own line — *"README version current"* — is a closure claim carrying no command, in the same file and the same commit as the rule widened to cover exactly that. The strain's seventh bite.

**15 — the caption convention defines a word whose referent nothing produces.** *(confirmed, executed)*
Detailed under probe 5′. `job:`/`moment:`/`claim:` are greppable because a skeleton produces them; captions have a definition, a reporting duty, and no producer, and no template for a deck, journey, or screen drawing exists. `screen drawing` itself is still undefined at 6 load-bearing sites (scenario 4, unaddressed). The gate is reportable, not runnable — and a mapping record that names a pattern now looks like evidence.

---

### What I confirmed, plainly

Every one of the eleven fixes is at its anchor, and twelve pre-fix controls that were silent at `ac7e688` all fire at `980e188`. The two rewritten sentences conserved their rules. The admission-gate contradiction that routed this piece back is genuinely closed between `AGENTS.md` and the judge skill, in compatible words. The surface is 58,431 bytes of 100,000 across 17 files and 5 skills, the always-read set is 24,083 of 50,000, and all four dev-suite checks still go red on demand. The re-entry receipt's Built line is real, state-only, and correctly ordered.

What I would not sign is the batch as complete. The judges routed this piece back for a rule that landed in one of its two homes. The sweep they ordered finds the same shape twice more in the fix itself — the mid-review exception is in two of three homes, the proof-plan checks in two of four — plus a definition that quietly narrowed protection while its record told the owner it widened, and a version line that was corrected in the wrong direction.

**Verdict: the conservation probes pass and the ordered fixes landed. The sibling sweep does not pass. Findings 7, 9 and 10 are one-sided edits made by this batch and are one clause each; 8 and 11–15 are pre-existing or inherited. The piece is closer, and it repeated its own routed-back defect in the act of fixing it.**

---

## Follow-up run (R″), 2026-08-29, on b8e2ce9

**Subject:** `~/Code/speck-next` at `b8e2ce9` (second fix build `f3e7a62`; pre-fix `980e188`). Same persona, same instrument, continued per the second re-entry receipt. This run is the combined final one: the judges' quoted controls on both trees, conservation, budgets, the sibling sweep of exactly what the batch touched, the owner paragraph read cold, and one free attack. Every number has its command above it.

**One-line verdict: all five second-batch fixes landed, every judge-quoted control fires, conservation is total — zero deletions on the method pages — and the batch did *not* repeat the one-sided-edit defect on the four rules it was ordered to fix. It repeated it on the fifth: the corrected byte figure was corrected in `state.md` and left standing in `decisions.md`, the file `AGENTS.md:115` says wins when files disagree, with its derived percentage still wrong in three more homes.**

---

### Probe 0″ — the instrument, and three false zeros it produced first

My first three sweeps all returned zeros I could have filed. None were real.

```
$ PATHS='AGENTS.md CLAUDE.md .claude/skills templates'
$ git grep -ioF "piece" 980e188 -- $PATHS | wc -l    →  0     (exit 0, no stderr)
```

This shell is **zsh**, which does not word-split an unquoted parameter. `$PATHS` arrived as *one* pathspec — the literal string `AGENTS.md CLAUDE.md .claude/skills templates` — which matches no file. `git grep` reported no hits and exited **0**. T2's original probe 0 caught the mirror-image of this in bash; the zsh form is quieter, because there is no `No such file or directory` warning to see.

Two more in the same run: a typo split a flag from its command (`git grep - icF`, printing `fatal: unable to resolve revision: icF` to stderr while the loop printed `0` for both trees — a false red at HEAD *and* a false green at the pre-fix tree), and `"$T:templates/piece.md"` was eaten by zsh's `:t` history modifier, yielding `980e188emplates/piece.md`.

Rebuilt on an explicit bash array of the 17 installed paths, with controls:

```
$ PATHS=(AGENTS.md CLAUDE.md .claude/skills templates)
tree 980e188:  'piece'=116  'Built'=41  'zzqqxx'=0  ERE 'zzqq[0-9]xx'=0   files searched: 17
tree b8e2ce9:  'piece'=116  'Built'=41  'zzqqxx'=0  ERE 'zzqq[0-9]xx'=0   files searched: 17
```

The instrument expresses a hit and a miss, over the same 17 files on both trees. Only numbers below this line count.

---

### Probe 1″ — the judges' quoted pre-fix controls, both trees

| # | Control (judge's own pattern) | `980e188` | `b8e2ce9` |
|---|---|---|---|
| **M1/B1** | `data.integrity` over the 17 installed files | **0** | **2** |
| **M2/B2** | `checks that must pass` at the four proof-plan homes | **2 of 4** | **4 of 4** |
| **M3** | mid-review exception in `templates/piece.md`'s Built bracket | **0** | **1** |
| **M4a/B3** | the three version strings agree | **no** (5.3.0 / 5.2.1 / 5.2.1) | **yes** (5.2.1 ×3) |
| **M4b** | `grep -c "55,157" state.md` | **3** | **1** |

**M1** — the two hits are exactly the two lists the judges named:

```
AGENTS.md:121  **Protected code** is everything on the risky list below — auth, money,
               private data, data integrity, schema migrations, regulated behavior, …
AGENTS.md:123  For money, auth, private data, data integrity, schema migrations, …
```

**M2** — the two that joined: `AGENTS.md:48` (*"state the runs, the checks that must pass, the people who will test it, and the rulings needed to accept it"*) and `templates/map.md:15` (*"proof plan: [runs · checks that must pass · user types · judge rulings]"*). A mapper following either now writes a plan `AGENTS.md:61` accepts. Null control across the same four files: 0.

**M3** — the exception landed under different words than R2′'s table pattern, so `one exception` reads 0 in the template on both trees and would have filed a false red. On a pattern that can fire (`during the review`): **0 → 1**. The landed clause: *"No build commit may land after it — except a fix landed during the review, which answers to the judge's re-run rules instead — and the receipt must open after the Built line was written."* All three homes now carve out the same case.

**M4a** — and the version they agree on is real: `v5.2.1` is a released tag, cut by `4a70e03`, which moved `package.json`, `README.md` and `state.md` together. The previous state announced a release existing nowhere; this one does not.

**M4b — the one number that does not match the brief, and it is the brief that is stricter than the judge.** I was sent expecting **0**. It is **1**. The survivor is `state.md:7`, which cites the figure as the value it was corrected *from*:

```
$ git grep -nF "55,157" b8e2ce9 -- state.md
state.md:7: … went from 70,770 bytes to 56,039 at its landing commit (… at ebb9fb5 —
            the earlier recorded 55,157 was a working-tree read at the wrong moment,
            corrected under the measured-numbers rule) …
```

Judgment 2 §3c blessed exactly this site by name: *"Line 7 legitimately cites it as the corrected-from value."* The two sites it condemned — line 14 certifying a **retired strain**, line 32 inside **Evidence** — both now carry the pinned measure. **M4b meets the judge's stated condition** (*"No surviving assertion of 55,157"*); it does not meet a literal count of zero, and it should not, because a correction that erased its own provenance would be worse. Reported this way so the judges rule on the right thing.

---

### Probe 2″ — conservation: word-diff of the second batch

```
$ git diff --word-diff=plain --word-diff-regex='\w+|[^[:space:]]' 980e188 f3e7a62 \
    -- AGENTS.md .claude/skills templates | grep -c '\[-'
  0
```

**Zero deletions on the method pages.** Every one of the four page edits is a pure insertion into an otherwise byte-identical line:

- `AGENTS.md:48` — `state the runs, {+the checks that must pass, the+} people {+who will test it+}, and {+the+} rulings…`
- `AGENTS.md:121` and `:123` — `private data, {+data integrity,+} schema migrations…`
- `templates/map.md:15` — `[runs · {+checks that must pass ·+} user types · judge rulings]`
- `templates/piece.md:15` — the exception, inserted between two conserved clauses

Across the whole batch (adding `README.md`, `state.md`) only **three** lines carry any deletion at all, and all three are digit swaps: `5.[-3-]{+2+}.[-0-]{+1+}`, and `5[-5-]{+6+},[-157-]{+039+}` twice. **No neighbouring rule was harmed, and no rule was rewritten** — this is the first batch in the piece whose product-page edits delete nothing.

**No new coined term.** Every added phrase already lived on the pages pre-batch:

```
"checks that must pass"    pre=2  post=4      "re-run rules"            pre=2  post=3
"the risky list"           pre=1  post=1      "landed during the review" pre=1  post=2
"data integrity"           pre=0  post=2   ← restoration: 'data-integrity' = 1 at ac7e688
"people who will test"     pre=0  post=1   ← rephrase of the existing bare "people"
```

Neither of the two zero-pre phrases is a coinage: *data integrity* is the term the first batch dropped, returning unhyphenated to match its list's style, and *people who will test it* expands an existing word rather than minting one. Nothing added is bolded or quoted as a term of art.

---

### Probe 3″ — budgets, pinned to the installer's own list

```
$ tot () { git ls-tree -r --name-only "$1" | grep -E '^(AGENTS\.md|CLAUDE\.md|\.claude/skills/|templates/)' \
    | while read -r f; do git cat-file -s "$1:$f"; done | paste -sd+ - | bc; }
  4a70e03 → 56176    48283c7 → 57348    ac7e688 → 57348    c53704e → 58431
  980e188 → 58431    f3e7a62 → 58636    b8e2ce9 → 58636    ebb9fb5 → 56039
```

**58,636 bytes · 17 files · 5 skills.** Against `CONTRACT.md:32–33` (≤ 20 files / 100 KB, ≤ 6 skills): pass, **41,364 bytes of headroom**. The batch cost **+205 bytes**. Always-read set (`CONTRACT.md:34`, ceiling 50 KB): `AGENTS.md` 13,133 + `state.md` 5,972 + `product.md` 596 + `map.md` 4,600 = **24,301 of 50,000**.

**The pinned figure reproduces under two independent methods** — this matters, because it is the number the batch installed to replace one that did not:

```
$ git archive ebb9fb5 AGENTS.md CLAUDE.md .claude/skills templates | tar -x -C $W
$ find $W -type f -exec cat {} + | wc -c   →  56039   (17 files)
$ tot ebb9fb5                              →  56039
```

**Control arm, run at `b8e2ce9`:**

```
$ ./devsuite/run.sh --control
  [RED] KEY: empty-state tip has a single space                            FAIL small-change
  [RED] KEY: corrupt journal value is refused or excluded, never drawn     FAIL bug-hunt
  [RED] KEY: state claims the streak counter, and it genuinely runs        FAIL honest-state
  [RED] KEY: the claimed review has a real dispatch behind it …
  [RED] concurrency bug actually fixed: 20 of 20 overlapping writes stored FAIL review-integrity
  control mode: 4 of 4 tasks went red (want: all)
```

**4 of 4 red.** Every key check still expresses its failure after the batch.

---

### Probe 4″ — siblings of exactly what the batch touched

Four of the five families the batch edited now agree in every home. The fifth does not.

**Proof plan — 4 of 4 spec homes agree.** I enumerated every occurrence of *proof plan* across the 17 files plus `CONTRACT.md` and `README.md`: eleven sites, of which four are spec enumerations (`AGENTS.md:48`, `map-build:18`, `templates/map.md:15`, `templates/piece.md:11`) and seven are references (`AGENTS.md:59,80,109,113`, `map-build:3,30`, `experience:53`). All four specs now list the same four parts in the same order — runs · checks · user types · judge rulings. **The dangling pointer to `AGENTS.md:61` is closed on every side.**

**Mid-review exception — 3 of 3 homes agree**, in compatible words: `AGENTS.md:78` (*"a fix landed during the review answers to the judge's re-run rules instead of invalidating the line"*), `judge:28` (*"the fix answers to the re-run rules instead, including its own pre-fix control"*), `templates/piece.md:15` (above).

**Version — 3 of 3 agree.** `bin/speck-next.js:86`'s `#v5.0.0` is a *pin example* of a released tag, not a current-version claim; `docs/reviews/**` are historical records, correctly stale.

**Protected code — the homes now nest, and two residuals remain.** Measured element by element at `b8e2ce9`:

| term | `AGENTS.md` | `CONTRACT.md` | `README.md` |
|---|---|---|---|
| auth · money | ✓ | ✓ | ✓ |
| privacy | — | ✓ | ✓ |
| private data | ✓ | — | ✓ |
| data integrity | ✓ (restored) | ✓ (hyphenated) | ✓ (hyphenated) |
| schema migrations · regulated behavior | ✓ | — | — |
| irreversible | ✓ | ✓ | ✓ |

**The crossing that blocked the piece is closed**: `AGENTS.md:121` is now a strict superset on the substantive elements, so the two lists nest instead of crossing. Judge 1's B1 also asked to *"reconcile all three homes — `AGENTS.md:121`, `CONTRACT.md:18`, `README.md:30` — or say in the tree which governs."* That half is not done, and the batch did not touch either file (`README.md` changed only its version digit; `CONTRACT.md` was untouched):

- `CONTRACT.md:18` still enumerates the old four — but the same sentence also says *"a change that turns out to touch protected code was never typo-sized"*, so it self-repairs by reference to the definition that now governs. Harmless.
- **`README.md:30` has no such clause.** Read alone it says typo-sized means *"no new dependency; no auth, money, privacy, or data-integrity code; no promise rewritten; reversible in one commit"* — full stop. A reader of the README alone still concludes a schema migration can be a typo-sized fix. Not installed, so no agent loads it; it is the repo's front page.
- **The fourth old term changed from *privacy* to *private data*.** Pre-first-batch `AGENTS.md:119` read *"auth, money, **privacy**, or data-integrity code"*; the landed protected list reads *"auth, money, **private data**, data integrity, …"*. On a literal reading that narrows: consent capture, a retention-policy toggle, a telemetry opt-out are *privacy* code without being *private data* code. Introduced by the **first** batch, untouched by this one, and flagged by neither judge. Finding 18.

---

### Probe 5″ — the corrected owner paragraph, read cold against the tree

`work/name-the-words.md:35`. I checked each claim against the files rather than against the record.

**Eight claims, verified true:** the first note *"claimed a pure widening and offered strike-it-for-the-narrow-reading"* (verbatim at `980e188`) · *"both halves were wrong, caught by both judges"* (judgment 1 §5, judgment 2 §4) · *"the risky list I anchored on lacked data integrity, so the edit silently dropped protection"* (measured 1 → 0) · *"repaired without needing your call (a strict widening is permitted)"* (`AGENTS.md:123`) · *"the judges recommend it"* — both do, and both mark it as their recommendation (judgment 1 §10 option (a), judgment 2 §8 *"My recommendation is wide"*) · *"both judges converge that the vocabulary needs a standing producer, not more lists"* · *"a mechanically enumerated population"* (124) · *"its free attack proved the cheap version catches nothing"* (0 of 4).

**One claim is not true as written.** *"protected code is now the old four **plus** schema migrations, regulated behavior, and anything irreversible — **nothing lost**, three things added."* Three of the old four survive verbatim; the fourth is *privacy* → *private data* (probe 4″). The magnitude is nothing like last round's — but *"nothing lost"* is the exact phrase whose falsity routed this piece back, in the same sentence position, now false by one term. Finding 18.

**Two things the owner cannot act on as written**, against the conductor law's *"a real question with options, real costs, and your recommendation"* and *"being understood is the deliverable"*:

- The paragraph says *"the old four"* and *"narrow it back to the four"* and **never lists them**. The owner arriving cold cannot see what he is choosing between. Judgment 2 §8 spelled both lists out in full for exactly this reason. And judgment 1 offered **three** options — wide, as-landed, or *"protect data-correctness code only where it can lose or corrupt stored data"*; the paragraph offers two, dropping judge 1's (c). Finding 19.
- **`sufficient` is not in the owner-facing paragraph at all.** Both judges filed it to him — judgment 2 §8 as one of *two* named owner questions, with two options and a recommendation; judgment 1 §11 as a thing to *"settle as a condition, not a consequence."* In the tree it survives only as the first of ten items in the *"Filed for the producer piece or the owner"* list at line 43, and the owner paragraph still opens *"two things."* A question that decides whether work ships, buried in a filed list, is the shape the conductor law names as a defect. Finding 20.

---

### Probe 6″ — the free skeptical attack

I pointed it at the fifth fix, the one whose sibling nobody had swept — the corrected byte figure — because judgment 2's re-test order added, in as many words: *"also sweep for surviving copies of any number the batch corrected."* The batch swept `state.md`. I swept the tree.

```
$ git grep -inF "55,157" b8e2ce9 -- ':!work/' ':!docs/'
  decisions.md:5  … Measured: installed surface 70,770 → 55,157 bytes (−22%, the first
                    shrink in the kernel's history) …
  state.md:7      … the earlier recorded 55,157 was a working-tree read … (the blessed citation)

$ git grep -inE "22%" b8e2ce9 -- ':!work/' ':!docs/'
  README.md:44    … rewritten in a builder's words — 22% smaller with all rules conserved …
  decisions.md:5  … (−22%, the first shrink …) …
  map.md:14       … the surface −22% with all 177 rules conserved …
```

And the arithmetic, against the same 70,770 baseline:

```
70,770 → 55,157  =  −22.1%   (the figure this batch declared wrong)
70,770 → 56,039  =  −20.8%   (the reproducible figure, two independent methods)
```

**The attack lands, and it lands on the method's own tie-break rule.** `AGENTS.md:115`: *"When files disagree, `product.md` and `decisions.md` win. Measured evidence beats every document, so fix the losing document and cite the finding."*

- `decisions.md:5` still asserts **55,157** — the figure the batch declared wrong — **and** its derived **−22%**. So `state.md` now says 56,039 and `decisions.md` says 55,157 about the same measurement, and the kernel's own hierarchy hands the win to the wrong number. The second half of `:115` names the required move exactly — *fix the losing document* — and it was not made.
- `README.md:44` (*"22% smaller"*) and `map.md:14` (*"the surface −22%"*) both carry the derived percentage, wrong by 1.3 points. Under `AGENTS.md:111` **as this very piece widened it** — *"any measured number carries the command that produced it and what it returned, written after the run, never from memory"* — both are uncommanded measured numbers, and both are false.
- Tally: the raw figure survives in **1** authoritative home outside `state.md`; the derived percentage in **3** homes; **0 of 4 corrected**.

This is the same defect shape for the third consecutive round — *a fix that lands in one of a rule's homes has not landed* — and the report-of-itself strain's **eighth** bite, again caught by someone other than the author. It is aggravated in two ways the previous bites were not: the surviving copy sits in the file the method page says **wins**, and the sweep that would have found it was explicitly ordered in the re-test instruction the batch was executing.

**In fairness to the batch:** on the four families it was ordered to fix, it did not repeat the defect. Every home of the proof plan, the exception, the version and the protected list was reached. The miss is on the fifth, and it is a miss of scope — `grep -c "55,157" **state.md**` was the control quoted, and the batch executed the control rather than the requirement above it (*"No surviving assertion of 55,157"*).

---

### Findings (continuing the numbering)

**16 — `decisions.md:5` still asserts the byte figure this batch declared wrong, in the file `AGENTS.md:115` says wins.** *(confirmed, executed)*
55,157 and −22% both stand. `state.md:7` says 56,039. Two files disagree about one measurement and the tie-break rule favours the wrong one. Fix: correct `decisions.md:5` to 56,039 / −20.8% with the pinned command, per `:115`'s own second sentence.

**17 — the derived percentage survives in three homes, uncorrected and uncommanded.** *(confirmed, executed)*
`README.md:44` *"22% smaller"*, `decisions.md:5` *"−22%"*, `map.md:14` *"−22%"*. Correct value −20.8%. All three are measured numbers carrying no command, under the rule this piece installed.

**18 — the owner paragraph's *"nothing lost"* is false by one term.** *(confirmed, text-level)*
*privacy* → *private data* in the protected list. Inherited from the first batch, not created by this one, flagged by neither judge — but it is asserted away by the sentence written to correct exactly this kind of assertion.

**19 — the owner paragraph never lists the four terms it asks him to choose about, and drops one of judge 1's three options.** *(confirmed, text-level)*
Against *"being understood is the deliverable."* One clause fixes it: name the four, and offer (c).

**20 — `sufficient`, filed to the owner by both judges, is not in the owner-facing paragraph.** *(confirmed, text-level)*
It appears only as item 1 of a ten-item filed list; the paragraph still opens *"two things."* Judgment 2 §8 wrote it out as a full owner question with options and a recommendation — that text exists and simply needs to reach the section the owner reads.

---

### What I confirmed, plainly

All five second-batch fixes are at their anchors and every control the judges quoted fires: data integrity is back in both lists, the proof plan names its checks in all four homes, the exception is in all three, the three version strings agree on a version that is really tagged, and `state.md`'s two condemned assertions are replaced by a figure that reproduces under two independent methods. Conservation is total — zero deletions on the method pages, three digit swaps in the whole batch, no new coined word. The surface is 58,636 bytes of 100,000 across 17 files and 5 skills, the always-read set 24,301 of 50,000, and the control arm goes 4 of 4 red. On the four families it was ordered to sweep, the batch reached every home — the first time in this piece that is true.

What I would not sign is that the numbers are now true. The batch corrected the figure where it had been caught and left it standing in `decisions.md`, which the method page says wins, with the percentage derived from it wrong in three more places — the eighth bite of the strain this piece exists to stop, on the one family whose sweep the judges had explicitly added to the order.

**Verdict: conservation, budgets, controls and the ordered sibling sweep all pass. The free attack does not. Findings 16 and 17 are the batch's own scope miss and are one line each; 18–20 are one clause each in the owner paragraph, and 18 is inherited. The piece is one grep from done, and that grep is the one it keeps not running.**
