# R2 — the conservation prober

**Persona:** conservation prober. Executed probes only; every claim below points at a command I ran and its output.
**Subject:** commit `e5494cf`. **Dispatched:** 2026-08-29. **Tool/model/session:** Claude Code workflow subagent, opus, this session.
**Built line read at the cited commit** — `git show e5494cf:state.md | grep -n "Built"` → line 27: `**The live piece: "A builder's words, and fewer of them" — Built.**` The line literally says **Built**.

**Subject-identity proof** (I am measuring the reviewed tree, not a drifted one):

```
$ git rev-parse HEAD
647cd99172b04c20d5795ab1397eca625fe256a8
$ git diff --stat e5494cf HEAD -- AGENTS.md CLAUDE.md .claude/skills templates devsuite
(empty)
$ git diff --stat e5494cf -- AGENTS.md CLAUDE.md .claude/skills templates devsuite
(empty)
```

The installed surface and the dev suite are byte-identical between `e5494cf`, `HEAD`, and my working tree. Everything below measures the reviewed subject.

---

## Probe 3 — budgets, re-measured

```
$ find AGENTS.md CLAUDE.md .claude/skills templates -type f | sort | xargs wc -c
    2720 .claude/skills/craft/SKILL.md
    5757 .claude/skills/experience/SKILL.md
    3555 .claude/skills/experience/references/walk.md
    4446 .claude/skills/experience/references/worst-day.md
    6374 .claude/skills/judge/SKILL.md
    3626 .claude/skills/map-build/SKILL.md
    2007 .claude/skills/map-build/references/questions.md
    4412 .claude/skills/shape-product/SKILL.md
    4497 .claude/skills/shape-product/references/questions.md
   11209 AGENTS.md
      11 CLAUDE.md
     391 templates/decisions.md
     698 templates/map.md
    2330 templates/piece.md
    1247 templates/product.md
    1025 templates/rounds.md
     733 templates/state.md
   55038 total
```

Pre-rewrite, same file set, per-file (`git show 44a48ba:<f> | wc -c`), summed: **70,770**.

| claim | measured | verdict |
|---|---|---|
| pre-rewrite total 70,770 | 70,770 | **true** |
| post-rewrite total 55,038 | 55,038 | **true, to the byte** |
| ≤ 65,000 limit | 55,038 — 9,962 bytes of headroom | **true** |
| skills ≤ 6 | `ls .claude/skills` → craft, experience, judge, map-build, shape-product = **5** | **true** |
| no new files in the installed surface | `diff <(git ls-tree -r --name-only 44a48ba \| grep -E '^(AGENTS\|CLAUDE\|\.claude/skills/\|templates/)') <(find …)` → **no output** | **true — identical file sets, 17 files both sides** |

Every file shrank except `templates/piece.md` (1,889 → 2,330), which grew to carry the widened receipt/judgment schema. That growth is accounted for by NEW-3/4/5.

**Budgets are real.** The claimed numbers are not rounded or approximate; both totals reproduce exactly.

---

## Probe 1 — every inventory entry, located

Entry arithmetic first: 42 (A) + 18 (E) + 14 (J) + 10 (C) + 14 (W) + 13 (WD) + 12 (S) + 22 (Q) + 11 (M) + 12 (MQ) + 4 (T) + 5 (NEW) = **177**. The "177 rules" figure checks out.

I derived coverage from the pages themselves, not from the drafter's report. **Result: 0 entries MISSING.** One entry (T1) survives in content but lost its pointer — reported separately below as DEGRADED, not missing.

### AGENTS.md — A1–A42, NEW-1–NEW-5 (47 entries)

Sample-quoted per section.

**Conductor section (A1–A10)** — all located, lines 9–19.
> A4/A3, line 13: "When the owner must decide, ask a real question. Start with one sentence explaining what each choice changes for users. Give the options, their real costs, and your recommendation. If you cannot write that opening sentence, the question is not ready."

A5 (owner's named key re-sequences the same session) → line 15, intact including "Do not queue it silently." A6/A7 → 17. A8/A9/A10 → 19.

**Where-to-start section (A11–A18)** — all located, lines 23–36.
> A11, line 23: "Choose the phase from completed evidence, not instinct or the presence of a file."
> A17, lines 32–34: "A wrong promise goes back to shape. Badly cut pieces go back to map. / A bad build stays in build. Thin evidence calls for another test run, not a ruling on a gap."
> A18, line 36: "*Ratified* means the owner agreed in their own words in that phase's dated record, after seeing a plain-language explanation. Nothing else counts."

**Phase sections (A19, A20)** — lines 38–52, both with the fresh-tester + separate-judge + receipt + ratification exit.
> A20, line 52: "Mapping ends only when its mechanical completion test passes, the running platform is decided, a fresh tester has probed the map and a separate judge has ruled — receipts committed before they ran — and the owner has ratified the order."

**Build loop (A21–A32, NEW-1, NEW-2, NEW-3, NEW-4, NEW-5)** — lines 56–90.
> A22 + NEW-1, line 59: "Before product code, commit its work file with the outcome, the proof plan, and a hard limit on time, tokens, and files read before the first run." — and line 60 gives the cap teeth: "If planning has gone on for a long time and nothing has run, the limit has failed: stop planning and get the smallest honest part running."
> A24, line 68: "A safety net counts only after you deliberately watched it fail. A check counts only if it can show the failure it claims to prevent; a control that cannot fail proves nothing about the product."
> NEW-2, line 70: "Checking one piece deliberately costs several fresh sessions: at least two testers and one judge, and more for risky work. The piece's work file states the exact number and roles."
> NEW-3, line 76: "A 'build commit' changes the product itself, such as code, screens, or data; commits that change only records or state are not build commits."
> NEW-4, line 78: "It fails if any build commit lands after it, or if it was written after the receipt opened."
> NEW-5, line 88: "After the fix lands, write a new Built line for the fixed product files in its own state-only commit and make the fix batch's receipt quote that line."

A23's seven sub-clauses all present: running-the-whole-time (60), product's own surface + harness-is-not-the-product + "no user surface" in state.md (64), drawn screens from screen drawings (66), real round-trip (66), `craft` for user-visible (66), workaround → strain line (68), Built written before review (61).

**Milestone section (A33, A34)** — lines 94–98. A34's three sub-clauses all survive:
> line 98: "A rewrite that changes no available fact is theater. Owner approval never replaces a judge's ruling. You may batch ordinary changes into one review, but review protected-code changes before shipping."
The old umbrella phrasing ("the owner in the room never switches the hearing off") is gone, but all three operative clauses it introduced are present. Conserved.

**Files section (A35–A39)** — lines 102–114.
> A35 citation rule, line 104: "Cite a record by its name and date, never by a bare round number."
> A39, line 114: "When files disagree, `product.md` and `decisions.md` win. Measured evidence beats every document, so fix the losing document and cite the finding."

**Small/risky (A40–A42)** — lines 118–124, including "You may raise the care level. You may never lower it." and the learn-before-stopping line.

### experience skill — E1–E18 (18 entries), all located

> E2, line 12: "Use a separate context. A walk done by the builder is void."
> E5, line 25: "A receipt reconstructed at closure is exactly what a builder writes when nothing forced the capture — it does not count, twice proven."
> E8, lines 33–39: the three-step identity proof, verbatim in force.
> E9/E10, lines 43–45: "Open every screenshot and give at least two observations that point to its pixels." … "Mark anything you could not run as untested; never turn it into a pass or omit it."
> E16, line 64: "Different users should sometimes disagree. Never soften one verdict toward another; the judge needs the difference intact."

E14's "a role, not an extra dispatch" force is carried by "One of these testers **also** receives…" (line 60); E15's by "one rostered tester" (line 62). Both conserved.

### judge skill — J1–J14 (14 entries), all located

> J3, line 12: "When the needed experience is missing, order an exact run and wait for it. Never rule on a gap."
> J6, line 26: "Use git to prove that the Built line covers the exact product files under review."
> J10, line 57: "'Delivers the promise' is judged against the jobs and promises in `product.md`; the piece's work file may narrow the work under review but cannot replace the product promise."
> J11, line 61: "Two straining rulings in a row, or one fighting ruling, makes structural repair the next piece. The judge makes that call because the builder has momentum to protect."
> J14, line 90: "A fix made during the review, before another tester can walk it, needs a control the judge can run against the pre-fix tree. 'The builder watched it fail' is a claim, not a control."

### craft — C1–C10 (10 entries), all located

C2–C8 are seven bullets, lines 12–18 (typography · whitespace · every state · motion · depth · color · component character with AI-first forms) — count verified as seven.
> C9, line 22: "After changing copy, read its entire flow as one text."
> C10, line 28: "When the real runtime renders differently from the code, write the defect's recognizable signature and the safe pattern into the piece's work file."

### walk.md — W1–W14 (14 entries), all located

Twelve numbered steps map 1:1 onto W1–W12; W13 is the section "Judge taste without imposing your own"; W14 is "Return a useful record."
> W8, step 8: "Open every screenshot. Write at least two observations pointing to its pixels. 'No issues' needs evidence; an unexamined screenshot proves nothing."
> W13: "Do not disguise your taste as an objective rule or quietly redesign toward it."

Two clauses moved out of walk.md rather than dying: "a verdict pointing at nothing is void" now lives in experience E10 and judge J7 (`judge` line 30, "Strike any claim that does not"); "the judge challenges the favorable ones hardest" lives in judge J8 (line 34). Both are per-rule conserved.

### worst-day.md — WD1–WD13 (13 entries), all located

Thirteen sections, 1:1.
> WD3: "Break each guarded behavior, watch its check fail, then restore it."
> WD7: "The reverse direction has the highest historical yield and is the least intuitive."
> WD12: four numbered git reads, count verified as four.
> WD13: "Record every move you could not run as untested. Never turn it into a pass or omit it."

### shape-product — S0–S11 (12 entries), all located

S0 across lines 8/14/16; S1–S11 are the eleven numbered rules.
> S3, rule 3: "A canned substitute breaks the promise; it is not a harmless stub."
> S10, rule 10: "Never present a paraphrase as the owner's quote. That is fabricated evidence."
> S11, rule 11: "Before any substantial shaping material reaches the owner, a fresh tester probes it against independent evidence with the `experience` skill, and a separate `judge` challenges the verdict and rules."

### map-build — M0–M10 (11 entries), all located

M0 at line 8; M1–M10 are the ten numbered rules plus the trailing accounting paragraph (M8's second half).
> M6, rule 6: the five completion-test bullets, plus "Grep, count, and match the named sets. Report every population and result to the owner."
> M8, line 39: "Derive the map's accounting summary from its pieces; regenerate it instead of editing two copies. State the full population behind every count."

### Q1–Q22 and MQ1–MQ12 (34 entries), all located, 1:1 by number

I diffed both question files old-vs-new in full. Every number 1–22 and 1–12 survives with the same subject and the same force. Nothing was merged, dropped, or renumbered.

One compression worth naming, not a loss of an entry: old MQ7 read "which personas experience it **(the worst day included where it matters)**"; new MQ7 reads "which user types test it." The parenthetical prompt to include the worst-day persona is gone from the mapping questions — but the rule it prompted survives at `experience` line 53 ("A milestone uses all four") and `AGENTS.md` line 94.

### T1–T4 (4 entries)

T1 — six skeletons, each opening with its floor line. Verified by reading all six: every one opens `[A floor, not a form: …]`. **Content present; discoverability degraded — see the free pass below.**
T2 — `templates/piece.md` encodes the receipt and judgment fields and must stay in sync with E4/J6. Checked field by field: Built quote ✓ · testers with persona/tool/model/session ✓ · dispatched date + commit ✓ · planned walks and commands, with batch-from-commit-range ✓ · run owner ✓ · empty record ✓ · records and verdicts ✓. Judgment block carries judge receipt line, challenges, the per-promise + four rulings + structure ruling, second judge, sent-back trace. **In sync.**
T3 — `templates/state.md` six sections, verified present and in order.
T4 — rounds / product / map / decisions skeletons all present.

---

## Probe 2 — scar facts, diffed clause by clause

Method: extracted every sentence containing a scar marker (`once|twice|two rounds|three rounds|a dozen|five rounds|18 days|three years|0.60|0.21|431|609|months|have shipped|have been gamed`) from all seventeen files at `44a48ba` and at `e5494cf`, then paired them.

| scar | pre-rewrite fact | post-rewrite fact | verdict |
|---|---|---|---|
| parallel dispatch | "two runs once executed one dispatch in parallel, neither knowing of the other" | identical | **unchanged** |
| reconstructed receipt | "it does not count, twice proven" | identical | **unchanged** |
| shared environment | "two rounds were once destroyed in a day: the conductor measuring inside a live run, then two parallel runs walking each other's subjects" | "Two rounds were once destroyed in a day: the dispatching session measuring inside a live run, then two parallel runs walking each other's subjects." | **unchanged** (only `conductor`→`dispatching session`) |
| hand-written batch list | "once omitted the exact delta an experiencer then walked into blind" | "once omitted the exact change a tester then walked into blind" | **unchanged** (vocabulary only) |
| silent plant | "Three rounds of production runs were once void because a plant failed silently and every run confidently walked a stranger's session — a wrong-subject run still renders screens." | identical | **unchanged** |
| truthful machine | "five rounds once perfected a truthful machine that missed its jobs" | "Five rounds once perfected a truthful machine that missed its jobs." | **unchanged** |
| the owner's one read | "the owner's one read of a rendered page caught what a dozen fresh contexts missed" | identical | **unchanged** |
| re-arguing screen | "three elements on it, all dead duplicates of what he had just read" | identical | **unchanged** |
| confidence floor | "a confidence floor of 0.60 once met a real corpus scoring 0.21, structurally, not tunably" | identical | **unchanged** |
| denominators | "431 deliveries … 431 of 609 … once 609 is a measured fact" | "Read 431 deliveries — still reading" / "'431 of 609' is honest only after measuring 609." | **unchanged** (431, 609 intact) |
| fixture blindness | "every fixture's gap was 18 days; the real outlier's was three years" | identical | **unchanged** |
| fail-closed | "fail-closed paths have shipped failing open" | identical | **unchanged** |
| gamed benchmarks | "entire benchmarks have been gamed through one test-harness hook" | "Entire benchmarks have been gamed through one test-harness hook." | **unchanged** |
| clipped overflows | "real overflows have clipped content for months behind perfect scores" | identical | **unchanged** |
| "no model here" piece | "once quietly owned three judgments the owner's ruling gives to the model" | identical, in **both** judge and map-build | **unchanged** |
| reference price | "once locked its price against a competitor's paid tier when the true reference price was zero" | identical | **unchanged** |
| AI-first core traded | "while every checklist row stayed green, because the property owned no row" / "a passing test literally enforced the model's absence" | both identical | **unchanged** |

**Zero altered facts, numbers, or counts. The scars are unfalsified.**

Three scar or provenance clauses were **removed entirely** rather than altered. Removal is compression, not falsification, but I record them so the loss is visible rather than silent:

1. `AGENTS.md` — "One plain rendering once let the owner catch, in a single read, a violation that three separate fresh checking agents had all missed." Gone from the whole surface (`grep -r "three separate fresh"` → no hits). The rule it justified (A9/A10) survives at line 19; only the evidence for it is gone. This is the scar that argues *why* the plain rendering is a defense layer rather than politeness, and it is the one most likely to be traded away by a future agent who no longer sees what it cost.
2. `shape-product/references/questions.md` — "Earned over eight months of real products." Provenance, not a rule.
3. `worst-day.md` — "Every move here was paid for by a real defect that shipped past a green suite." Provenance, not a rule.

One **force drift**, flagged as an observation: old WD5 was a prohibition — "No threshold that judges real behavior locks before its measured distribution exists"; new WD5 is a description — "A threshold for real behavior is a hypothesis until you measure the real distribution." The prohibition form survives, relocated, in `templates/product.md` line 28: "Measure real distributions before setting judging numbers." Since `templates/product.md` is reachable (named by `shape-product`), the force is conserved — but it now lives in a template rather than the persona reference where the tester reads it.

---

## Probe 4 — term sweep

```
$ for t in "the wire" "proven-means" "proven means" "dispatcher" "route-back" "routed back" "experiencer" "charter" "hearing"; do grep -rin -- "$t" AGENTS.md CLAUDE.md .claude/skills templates; done
=== TERM: the wire ===     (no hits)
=== TERM: proven-means === (no hits)
=== TERM: proven means === (no hits)
=== TERM: dispatcher ===   (no hits)
=== TERM: route-back ===   (no hits)
=== TERM: routed back ===  (no hits)
=== TERM: experiencer ===  (no hits)
=== TERM: charter ===      (no hits)
=== TERM: hearing ===      (no hits)
```

**All seven named killed terms are at zero across the installed surface.** No legitimate-English hits to judge — there were none of either kind.

Their replacements are all defined or plainly self-describing: `hearing` → *review*; `experiencer` → *tester*; `proven-means` → *proof plan* (defined at `map-build` rule 3 and templated in `templates/map.md`); `charter` → *piece plan* / *work file*; `the wire` → *the product* / *real dependency*; `substrate` → *running platform*; `frame` → *screen drawing*; `dispatcher` → the "Know where to start" section.

**But a new coinage got in.** See the next probe.

---

## Probe 5 — the four merge corrections

### (i) Built may ride in the build's final commit OR a records-only commit after it — consistent in all three places: **CONFIRMED**

- `AGENTS.md` line 61: "write **Built** in `state.md` — in the build's final commit, or right after it in a commit that changes nothing else."
- `AGENTS.md` line 78: "It fails if any build commit lands after it, or if it was written after the receipt opened."
- `.claude/skills/judge/SKILL.md` line 26: "It may ride in the build's final commit, or in a records-only commit just after it. The line is invalid if any build commit lands after it, or if it was written after the receipt opened."
- `templates/piece.md`: "written in the build's final commit, or in a records-only commit just after it. No build commit may land after it, and the receipt must open after the Built line was written."

Three statements of the same rule, same permission, same two invalidation conditions, no drift between them. The repair path is records-only in all three (`AGENTS.md` 78, judge 28, piece.md), which is correct — a repair happens after the build, so the "final build commit" option is no longer available. The rule is internally consistent and does not outlaw the pattern the previous piece's judges validated.

### (ii) The whole-method sentence near the top of AGENTS.md: **CONFIRMED**

`AGENTS.md` line 3, first paragraph, second sentence:
> "This page and the five skills it names are the whole method — there is nothing else to load or look for."

Five skills verified on disk: `ls .claude/skills` → craft, experience, judge, map-build, shape-product. The sentence's count is true.

### (iii) "dispatch proof" appears nowhere: **REFUTED — this is a defect**

```
$ grep -rn "dispatch proof\|dispatch-proof\|dispatch-time proof" AGENTS.md CLAUDE.md .claude/skills templates
.claude/skills/shape-product/SKILL.md:16:… a fresh tester has probed it with dispatch proof, a separate judge …
.claude/skills/experience/SKILL.md:12:Claiming fresh users without written dispatch proof is fabricated evidence.
.claude/skills/experience/SKILL.md:25:… Without dispatch-time proof, there is no record for the judge.
.claude/skills/map-build/SKILL.md:35:… then a separate judge challenges and rules; dispatch proof must exist.
.claude/skills/judge/SKILL.md:20:### 1. Check the dispatch proof
```

Plus a sixth, near-variant, that the exact-phrase grep misses:
```
.claude/skills/experience/references/worst-day.md:59:3. Does every piece past Built have dispatch and review proof?
```

**Six sites across five of the six skill files.** The correction was applied to `AGENTS.md` only (`grep -n "dispatch" AGENTS.md` → no hits) and never propagated to the skills. The build record's claim — "'dispatch proof,' an undefined new coinage, replaced with the defined word receipt" — and the review receipt's "Convicted terms at zero across the surface" both overclaim.

Why this is a real defect and not a nit:

- The term is **undefined at every site.** `receipt` is defined once, at `experience` line 16: "commit a **receipt**: written proof of who was asked to test what." "dispatch proof" is never defined anywhere.
- It is used **before** that definition in its own file: `experience` line 12 uses "dispatch proof"; the definition of the thing it means arrives at line 16 under a different name.
- `judge` uses it as a **section heading** — "### 1. Check the dispatch proof" — then the body immediately switches vocabulary: "Start with the receipt's Built field." A reader who does not already know the method meets a heading naming one thing and a body naming another.
- `shape-product` and `map-build` use it **with no local definition and no cross-reference**. An agent that loads only `shape-product` (the correct skill for a fresh repo, per `AGENTS.md` line 25) meets "dispatch proof" as a hard exit condition it cannot define from anything it has been given.
- This lands squarely on the piece's own whole-property 2 — "No new coinage — the owner's word budget stays 4 of 5" — and on judge J11, "Undefined jargon that carries a rule is a defect because the owner cannot judge what they cannot understand." The rule it carries is a phase exit condition. It is load-bearing.

The fix is mechanical: replace with `receipt` at all six sites (and "a receipt to show it" or similar at the two exit-condition sites), heading included.

### (iv) The widened review-integrity check matches a tester-vocabulary claim: **CONFIRMED by executed probe**

The diff (`git diff 82fbddb e5494cf -- devsuite/tasks/review-integrity/check.py`) adds `tester` to the fresh/independent alternation, adds `tester` to the witness alternation, adds `used|tested` to its verb set, and makes `review` an alternative to `hearing` before `convened|ran|held`.

I ran both regexes myself against seven probe strings:

```
probe                                                   OLD    NEW
P1 NEW-VOCAB claim (AGENTS.md words: fresh testers)   False   True  <-- WIDENED
P2 NEW-VOCAB minimal (piece.md words)                 False   True  <-- WIDENED
P3 NEW-VOCAB 'the review ran'                         False   True  <-- WIDENED
P4 OLD-VOCAB claim (pre-rewrite words)                 True   True
P5 OLD-VOCAB hearing convened                          True   True
P6 NEGATIVE: no review claimed at all                 False  False
P7 NEGATIVE tricky: lifted verdict, no reviewer       False  False
```

P1: `"fresh testers used the piece and returned a record; the judge found it sufficient."`
P2: `"testers: persona, tool, model, session. the tester used the product and returned a verdict."`
P3: `"the review ran on built work and every verdict pointed at a lived moment."`
P4: `"a fresh experiencer walked the piece and the judge ruled it sufficient in the hearing."`
P7: `"this piece is proven and works well."`

The four-way positive control claimed in the build record holds exactly: **old misses the new-vocab claim (P1–P3 old=False), new catches it (P1–P3 new=True), old vocabulary still covered (P4–P5 both True), silent when no review is claimed (P6–P7 both False).**

The instrument can also still express the failure it exists to rule out: P7 falls to the `else` branch, where `re.search(r"\b(proven|judged)\b", claim_text)` matches "proven" and `"not judged"` is absent, so `note(..., good=False)` fires RED. A lifted verdict with no reviewer behind it is still caught. The check is not a control that cannot fail.

Note: the check's regex is also blind-guarded (`assert n_walked > 0, "instrument error: walked zero method files"`), so a zero-subject run reports as an instrument error rather than a green.

**I did not run the dev suite itself.** The build record's "control arm 4/4 red after everything" and the receipt's pending green-arm result are **untested by me** — not converted to a pass, not omitted. Someone must read that arm back before landing is asked.

---

## Probe 6 — free skeptical pass: is every installed file still reachable from the pages an agent loads?

I chose this because a rewrite that renames sections is exactly where a pointer dies without any rule dying — the failure shape no inventory entry would catch, since each entry asks whether a *rule* survived, never whether a *file* is still findable.

```
$ for t in templates/*.md; do b=$(basename $t); grep -rq "templates/$b" AGENTS.md .claude/skills \
    && echo "  REACHABLE  $t" || echo "  ORPHAN     $t"; done
  ORPHAN     templates/decisions.md
  REACHABLE  templates/map.md
  ORPHAN     templates/piece.md
  REACHABLE  templates/product.md
  REACHABLE  templates/rounds.md
  ORPHAN     templates/state.md

$ grep -n "templates" AGENTS.md
  (no hits)
```

Against the pre-rewrite page:

```
$ git show 44a48ba:AGENTS.md | grep -n "templates"
37:## The files — skeletons in `templates/`
45:… The skeletons in `templates/` are starting points: expanding their sections, adding new sections,
   and creating whole new materials is expected and encouraged …
```

**Finding — T1 DEGRADED (pointer lost, content intact).** Pre-rewrite, `AGENTS.md` named the `templates/` directory twice, once as the heading over the very section that lists the six files. Post-rewrite the string `templates/` appears nowhere in `AGENTS.md`. The only surviving pointers are the three individual ones in `shape-product` and `map-build`, which cover the shape and map phases. Nothing in the loaded surface tells a builder that `templates/piece.md`, `templates/state.md`, or `templates/decisions.md` exist.

The sharpest instance: **`templates/piece.md` carries the entire receipt and judgment field schema** — inventory entry T2, and the concrete form of A25, E4, J6, and all three of NEW-3/4/5. It is now reachable only by an agent who guesses the directory. `AGENTS.md` line 59 tells a builder to "commit its work file" and line 74 to write a "receipt," but never says a skeleton for either exists or where. The build phase is the one phase whose skeletons became invisible.

Related: `AGENTS.md` line 112 still says "Templates are starting floors, not limits; expand them when the product needs more" — a rule (A38) whose subject the same page never locates.

Low-cost fix: restore the directory name to the files section, e.g. "The skeletons for these files are in `templates/`," which costs about 50 bytes against 9,962 of headroom.

**Also checked, all clean:** `references/walk.md` and `references/worst-day.md` are both named from `experience` (lines 55, 58); `references/questions.md` is named from both `shape-product` (line 10) and `map-build` (line 10); `CLAUDE.md` is `@AGENTS.md`, one line, correct.

---

## Verdict

**Did every rule survive?** Yes, by my own derivation from the pages. All 177 inventory entries located — A1–A42, E1–E18, J1–J14, C1–C10, W1–W14, WD1–WD13, S0–S11, Q1–Q22, M0–M10, MQ1–MQ12, T1–T4, NEW-1–NEW-5. **Zero MISSING.** Q1–Q22 and MQ1–MQ12 verified 1:1 by full old/new diff. One entry, **T1, is DEGRADED**: the six skeletons exist and each carries its floor line, but half of them — including `piece.md`, which holds the receipt schema — became undiscoverable from the loaded surface when `AGENTS.md` stopped naming `templates/`.

**Are the scars unfalsified?** Yes. Seventeen scar clauses diffed against `44a48ba`; **zero altered facts, numbers, or counts.** Every number is intact: three elements, two runs, two rounds in a day, three rounds void, five rounds, a dozen contexts, 0.60/0.21, 431/609, 18 days/three years, three judgments, months. Three clauses were removed entirely rather than altered — compression, not falsification — of which one is a genuine scar (`AGENTS.md`'s "three separate fresh checking agents"), now gone from the surface with the rule it justified left standing unevidenced.

**Are the budgets real?** Yes, to the byte. 70,770 → **55,038**, reproduced exactly; 9,962 bytes under the 65,000 line; five skills, not six; seventeen files before and seventeen after, identical set, no new file in the installed surface.

**One defect found.** Merge correction (iii) is refuted: **"dispatch proof" survives at six sites across five skill files** — `shape-product:16`, `map-build:35`, `experience:12`, `experience:25`, `judge:20` (a section heading), `worst-day:59` — undefined at every one of them, used before the definition of `receipt` in its own file, and carrying a phase exit condition in two of them. The correction reached `AGENTS.md` and stopped there. Both the build record's "replaced with the defined word receipt" and the receipt's "convicted terms at zero across the surface" overclaim against the text as committed. Judge J11 names this class directly: undefined jargon that carries a rule is a defect.

**Not tested by me, recorded as untested:** the dev suite's control arm (claimed 4/4 red) and green arm (pending in the receipt). I probed the review-integrity check's regex by hand and it behaves as claimed; I did not execute the suite.
