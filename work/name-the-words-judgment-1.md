# Judgment 1 — Name the words

**Judge:** judge 1 · Claude Code · model opus · fresh context, built none of it and tested none of it · 2026-08-29 · ruling on build `48283c7` at receipt `ac7e688`. Blind to judgment 2.

**Ruling in one line: not sufficient — the piece routes back to build.** The owner's order was executed in full and nothing regressed, but two of the four definitions this piece exists to add are themselves wrong, a third points at a field that does not exist, and the strain the piece was built to kill bit again inside the piece's own build record. Every fix is one sentence. The re-run is cheap and already written.

Read the next paragraph before the rest: **this is not a failure of the owner's call.** He asked for four words defined, two resolved, and a producer for self-reports. All seven landed and a cold reader confirmed each one. The route-back is the kernel policing its own text — three sentences it got wrong on the way — plus one number it claimed without measuring.

---

## 1. The receipt — valid

| Check | Evidence |
|---|---|
| Built line exists and literally says **Built** | `git show 9f6b1c4:state.md` line 26: *"**The live piece: "Name the words" — Built ([work/name-the-words.md](work/name-the-words.md)).**"* |
| Written in a commit containing nothing else | `git show --stat 9f6b1c4` → `state.md \| 1 file changed, 1 insertion(+), 1 deletion(-)` |
| Covers the exact product files under review | `git diff 4a70e03..48283c7` touches `AGENTS.md`, `.claude/skills/judge/SKILL.md`, `.claude/skills/map-build/SKILL.md` — all in the tree `9f6b1c4` describes |
| No build commit lands after it | `48283c7` (build) → `9f6b1c4` (state only) → `ac7e688` (work file only) → `HEAD == ac7e688`. `git show --name-only ac7e688` → `work/name-the-words.md` alone |
| Written before the receipt opened | Built at 17:41:37; the receipt's Built field carries its quote at `ac7e688`, 17:41:46 |
| Work file committed before its product code | `git log --diff-filter=A -1 -- work/name-the-words.md` → `4a70e03`; first product commit `48283c7`. Different commits, work file first |

**One seam worth recording.** `48283c7` already carried a receipt block whose Built field said *"quoted in the commit after the build's."* That is a forward pointer, not a quote — and `AGENTS.md:78` settles it: *"No valid quote means no review."* A receipt with no qualifying quote is not an opened receipt, so the receipt opened at `ac7e688`, after the Built line. The chain is valid. But a builder could read the same two commits as "receipt opened at `48283c7`, Built written after it" and reject their own valid work. One clause would close it: the receipt opens when its Built field carries the quote.

---

## 2. The two exemption clauses — both executed, as ordered

The clause under test (`judge/SKILL.md:24`): *"The exemption holds only when `map.md` has no live piece, **or** when the review's subject is `product.md` or `map.md` itself rather than built work. When in doubt, demand the Built line."*

**Execution A — this repo, mid-build. Must demand the Built line. It did.**

Confirmed from the repo, never from the receipt's label, exactly as the clause orders:

- Does `map.md` have a live piece? Read `map.md` at `ac7e688`: line 9 *"Pieces (in order — exactly one live)"*, line 15 *"6. **Name the words** [live — …]"*. Yes. **Clause 1 fails.**
- Is the review's subject `product.md` or `map.md`? Read from git, not from the record: `git diff --stat 4a70e03..48283c7` → `AGENTS.md`, `judge/SKILL.md`, `map-build/SKILL.md`. Neither file. **Clause 2 fails.**
- Both fail ⇒ exemption **denied** ⇒ Built line demanded. Demanded, and satisfied per section 1.

**Execution B — a review whose subject is `map.md` itself. Must grant the exemption. It did.**

The real case: speck-next's own mapping-exit review, which `map-build/SKILL.md:32` requires — *"A fresh tester probes the map against the owner's record, repo, and independent evidence, then a separate judge challenges and rules."* Subject: `map.md` at `ac7e688`.

- Does `map.md` have a live piece? Yes, the same one. **Clause 1 fails.**
- Is the subject `map.md` itself rather than built work? Yes. **Clause 2 holds.**
- The clauses are joined by **or**, so one is enough ⇒ exemption **granted**. No Built line. Instead: check that the receipt lists the planned probes and was committed before they ran, then go straight to the records.

**Why clause 2 has to exist, now demonstrated rather than asserted.** Without it, a mapping review that runs while any piece is live deadlocks: clause 1 refuses the exemption, and no Built line can ever exist for `map.md`, because `map.md` is a record and never a build commit. Clause 2 is the only thing that lets the map be reviewed during an in-flight build.

**The adversarial case I added, unprompted.** Could a build review launder itself through clause 2 by calling itself "a review of the map gate"? This very review is the test — one of its seven texts lives in `map-build/SKILL.md`. The clause names two **files**, `product.md` and `map.md`. `.claude/skills/map-build/SKILL.md` is not `map.md`. The clause correctly refuses. Its narrowness by filename is what makes it safe, and that is worth keeping when anyone rewrites it.

**Honest limit on this execution.** This is a prose gate. Its execution is a fresh context reading it and applying it, which is what I did in both directions plus one attack. There is no runnable check behind it, and I am not claiming one.

**The residual hole, and it is real.** T1 found it and I confirm it: a piece whose product is a *document* — a domain model, a journey study — fails both clauses (it is the live piece, and it is not `product.md` or `map.md`), so the judge must demand a Built line for something that does not obviously "run." `AGENTS.md:113` makes such material first-class and orders *"test and judge it."* The escape exists — give the document piece runnable checks in its proof plan, which is exactly what **this** piece did with the dev suite and the greps — but no page says so, and *"When in doubt, demand the Built line"* pushes an unsure judge toward the deadlock. One sentence closes it.

---

## 3. What I re-took at my own hand

Re-run at `ac7e688`, not inherited from either tester.

**Term greps.** Over the installer's own surface — the 17 files at `bin/speck-next.js:12`, `["AGENTS.md", "CLAUDE.md", ".claude/skills", "templates"]` — with a `zzqqxx` control returning 0 and a `piece` control returning hits, so the instrument can express both:

| Term | Sites | Defined? |
|---|---|---|
| `protected code` / `protected-code` | `AGENTS.md:121`, `AGENTS.md:98` | no |
| `caption` | `map-build:28` (×2), `craft:12` | no — and `craft:12` is a different sense (type size) |
| `good to use` | `judge:54`, `AGENTS.md:94`, `piece.md:27`, `state.md:6` | no |
| `quality hangs together` | `judge:55`, `piece.md:27`, `state.md:6` | no |
| `screen drawing` | 6 sites | no |
| `captioned` | 0 | dead, as promised |
| `gates` | `judge:59` only | no |

**Byte measure**, two independent methods — `git show $c:$f | wc -c` summed, then re-done with `git cat-file -s` on the blob:

```
ebb9fb5  56,039      2569c04  56,039      4a70e03  56,176      48283c7 / ac7e688  57,348
```

**+1,172 bytes across this build. 1.1 KB, not the 2.1 KB the build record claims.** No baseline in the repo yields 2.1 KB. Always-read set: 23,240 of 50,000. 17 files of 20, 5 skills of 6.

**Control arm.** `./devsuite/run.sh --control` at `ac7e688`: `control mode: 4 of 4 tasks went red (want: all)`. Reproduces the build record and T2 exactly.

**T1's planted-claims reasoning, against the actual page text.** I verified the governing sentence verbatim at `AGENTS.md:111` and applied it myself. Entry B — *"fixed everywhere — I went through all the call sites"* — trips the trigger (*done everywhere*), carries no command and no return, and is memory, which the rule excludes by name. **Condemned.** Entry A carries `grep -rn 'parseDate(' src/` with its return and `npm test` with its return. **Accepted as a claim.** My reading matches T1's, independently. The rule can express a pass and a failure — the control has both arms.

---

## 4. Hearing the records

### T1, the cold reader

**What I struck.** T1 writes that `protected code` *"appears exactly once in the whole corpus (verified by grep)"* — then quotes a second site three lines later. My grep finds two on the pages (`AGENTS.md:98` hyphenated, `AGENTS.md:121` not) and a third in `CONTRACT.md:18`. **The count is struck.** The finding is not: none of the three sites defines it.

**Challenge — the favorable half, hardest.** T1's headline is *"I could run a product under these pages tomorrow, and I would."* What did that assume but not test? It assumed the pages are read by a builder who has time. T1's own H4 concedes the opposite case — *"I would still expect a hurried judge to mis-rule here"* — and its H1 deadlock was found only *"by working backwards."* So the verdict is true of a careful reader with time to reconcile across files, and T1 says so itself. I record it that way rather than as a general grade. It still stands: T1 named specific mechanics it could act on cold, and I checked three of them at their cited lines and found them exactly as quoted.

**Challenge — findings #3 and #4.** T1's own criterion for UNDEFINABLE requires that plausible readings *"lead to different actions."* For `good to use` / `quality hangs together` T1 then argues only that *"what differs is which head a finding lands under"* — which under non-compensation blocks the piece either way, so **that stated rationale does not meet T1's own bar.** I strike the rationale and substitute one that does: under one reading a clumsy-but-polished flow lands under `good to use`; under another it lands under neither, because "usable" and "internally coherent" both let it through. That fork changes whether a piece lands. **The count of 4 stands, on repaired reasoning for two of the four.**

**First-hand corroboration I did not expect to produce.** Ruling this piece, I had to rule `good to use` and `quality hangs together` separately with no definition on any page, so I invented the mapping myself and disclose it in section 5. And classifying my own ordered fix, I had to decide whether a state-ladder definition is "protected code" — the exact undefined word T1 filed first. **Two of T1's four findings bit the instrument the findings are about, inside this judgment.** That is stronger evidence than anything in T1's record, and it is why I am not softening them.

**T1's job 3 — the document-piece jam.** Traced independently. Confirmed. Filed as an ordered item in section 9.

**The four terms' shared shape, which T1 named and I confirm.** *"Every one of them is a leaf that no rule points back at."* The build ran down the six **stated** terms and hit all six. What survived is the vocabulary nobody put on the list.

### T2, the conservation prober

T2 disclosed a false green before any verdict counted — an unquoted variable that made `grep` search nothing while `wc -l` reported 0 — rebuilt the sweep on an explicit array, and gave it a positive and a negative control before re-running. That is the right order and I am counting its numbers because of it.

**Every number I re-took reproduces exactly.** 57,348; 56,176 at `4a70e03`; +1,172; 56,039 at `2569c04`; 23,240 always-read; 17 files; 5 skills; `captioned` at 0; `screen drawing` at 6; control arm 4/4 red.

**What I struck.** T2 reports *"57,348 bytes ≤ 65,000 — pass, with 7,652 to spare"* and presents 65,000 as *"a 65,000 bar."* No such bar exists in `CONTRACT.md`; 65,000 was the **previous piece's own outcome target** (`work/builders-words.md:7`). Not false, but unsourced in a probe report whose value is sourcing. T2 also cites the real ceiling correctly two clauses later (100 KB). Struck as a stated bar, kept as a historical target.

**Challenge — the favorable half, hardest.** T2's strongest claim is *"every neighbouring rule survived."* What did it assume? That a word-diff over `AGENTS.md` and `.claude/skills` covers the blast radius. I read the full diff myself: only two hunks contain any deletion, and both conserve — the `map-build:28` rewrite keeps the population source, the grep, the count and the match-to-one-piece and drops only *captioned*; the `AGENTS.md:109` rewrite drops one sentence that still stands verbatim at `judge/SKILL.md:59`. **Confirmed.** But the sweep covered the installed surface only. `README.md`, `CONTRACT.md` and `state.md` all carry the same vocabulary and were not word-diffed. T2 caught two of those by luck (`README:44`, and `hearing` alive in `CONTRACT.md`) rather than by sweep. Narrow, and it did not cost anything here.

**One thing I found that neither tester did.** `state.md:7` claims the installed surface is *"55,157 (measured at ebb9fb5, −22%)."* Measured two ways at `ebb9fb5` on the installer's own file list: **56,039**. It does not reproduce, and the previous piece's records give three different numbers for the same measurement (55,038 in judgment 1 and R2, 55,775 in R2, 55,157 in `state.md`). Inherited text, not written by this build — so not this piece's defect. But it sits four lines above `state.md:12`, which names *"byte-exact self-measurements in this file"* as an open strain, and `CONTRACT.md` promise 4 says *"Overclaiming is a bug."* The strain is not merely recorded; it is currently wrong in the file that records it.

### Where the two records disagree — held apart, not averaged

T1 says the piece missed its target by four terms. T2 says the texts landed intact and the budgets hold. **Both are true and they are about different things.** T2 measured what the seven texts did at their anchors; T1 measured what the corpus still lacks. Neither reaches the other's ground. The one place they touch is `map-build:28` — T1's `caption` and T2's `screen drawing` are the same defect seen from two sides, so per `judge:44` I record **one** finding, in section 9.

---

## 5. The four rulings

Two of these four heads have no definition on any page. I ruled them anyway and I state my mapping so it can be argued with: **good to use** = can a fresh agent act correctly from these pages; **quality hangs together** = do the pages agree with themselves.

### Works — **yes**, on runs I executed

The seven texts are at their anchors (my own read of `git diff 4a70e03..48283c7`). Nothing was displaced: five of seven are pure insertions, and both rewrites conserve every rule, with the one deleted sentence standing verbatim at `judge:59`. `./devsuite/run.sh --control` at `ac7e688` returns 4 of 4 red at my hand — every key check can still express the failure it exists to catch. Both exemption clauses execute correctly in both directions, plus one adversarial case they correctly refuse.

**Stated limit:** the green arm was not run at this commit — the build record cites the control arm only. So "works" covers the gates' ability to fail, the texts' presence, and the clauses' behavior. It does not cite a green-arm run at `ac7e688`.

### Delivers the promise — **broken**

Three layers, because they give three different answers and collapsing them would be dishonest.

**Against the owner's ratified call — delivered, 7 of 7.** `decisions.md:3` records it: *"Define the words (Recommended)" — the next kernel piece defines the undefined load-bearing words (four defined, two deleted per promise 8's consider-deleting-first) and gives self-reports a producer.* Four defined: Shaped, care level, straining/fighting, "its own checks" — T1 tested each hardest and ruled each definable. Two resolved: Live consistent in three places, *captioned* at zero. The producer installed at `AGENTS.md:111` and watched discriminating both ways. Every item landed.

**Against the piece's own staked prediction — failed on arm 1.** Staked: *"the cold reader's undefinable-terms count reaches zero."* Result: 4. Arm 2 held.

**Against `CONTRACT.md` promise 6 — broken, and the work file cannot replace it.** Promise 6's bar: *"a smart person who has never seen Speck can follow any document in this repository in one read"* and *"a reviewer who stumbles on our vocabulary files it as a defect."* Its named check is a fresh-reader test. T1 **is** that instrument, and it filed four defects and one mandatory mechanical check it could not execute. By the promise's own words that is a defect count, not a pass.

**The mechanism, and it is the finding that matters.** The prediction's population was **inherited, never re-derived.** The six-term list came from a cold read of the *pre-rewrite* text; this piece closed all six and staked zero against a list that was never the whole population. `decisions.md:5` records that the previous piece staked the identical target and failed it identically: *"six pre-existing undefined load-bearing terms against a target of zero."* **The same prediction, staked twice, failed twice, for the same reason.** A universally-quantified outcome — "no X remains" — was given a detector (a cold reader) and no producer (nothing that enumerates X). The enumerated six all got fixed. The unenumerated four survived a piece whose whole outcome was their absence.

### Good to use — **kept**, with the stumbles named

Evidence from lived moments, not summary: T1 quoted the Built-line rules and called them *"the tightest writing in the corpus — I know exactly what makes a receipt valid, exactly how to repair an invalid one"*; computed the review roster and cost unaided; resolved the straining/fighting boundary from the sentence's own subject without help; correctly applied the brand-new producer rule to a matched pair on first contact. Its verdict: *"I could run a product under these pages tomorrow, and I would."* The four definitions measurably improved this — each was tested hardest and each held.

The cost, in T1's own ranking: four terms it stumbled on, one gate it could not execute, and one deadlock it had to reason backwards out of. T1 places these as things to fix *"before running something regulated"*, not as blockers. I rule with it, on that scope.

### Quality hangs together — **broken**, at four seams

This is the head the defects land under, and every one of them is inside the thing the piece was built to produce.

1. **`AGENTS.md:109` — "Judged means its review has ruled."** Two sentences later, `AGENTS.md:111`: *"An insufficient judgment sends work back without advancing its state."* Read literally, a review that ruled *insufficient* has ruled, so the work is Judged — which `:111`, `:86` and `templates/state.md:6` all deny. **New in this commit**, and it was not even one of the four the owner ordered; it rode along in the ladder sentence. A piece whose subject is definitional precision shipped a definition that contradicts a rule in the same block.
2. **`AGENTS.md:109` — Shaped drops a mandatory field.** `AGENTS.md:59` requires *"the outcome, the proof plan, and a hard limit on time, tokens, and files read before the first run."* The definition names two of three. The limit is its own field at `templates/piece.md:9` and is the referent `AGENTS.md:60` depends on. A piece can now satisfy the ladder's Shaped while violating the step that produces it.
3. **`AGENTS.md:61` — the new definition points at a field that does not exist.** *"Its own checks are the checks named in the piece's proof plan."* Neither proof-plan spec names checks: `map-build:18` says *"the runs, the user types who will test it, and what the judge must rule on"*; `templates/piece.md:11` says *"Runs · exact user types … · judge … · what each rules on."* A builder who fills the template exactly has named no checks — so by the new sentence's own words the piece can never be Built. It self-repairs by forward reference, and the deadlock is one word wide, but this is a **dangling pointer the fix introduced** under the state everything else hangs from.
4. **The build record's byte claim.** *"up 2.1 KB from v5.2.1"*; measured +1,172 both ways. This is the **sixth bite** of the strain `state.md:11` names — *"the piece's report of itself … every one caught by a fresh context or judge, never by the author"* — and it bit **inside the build record of the piece built to stop it**, three sentences from the producer. The cause is mechanical, not careless: the producer's trigger is *fixed, closed, done everywhere*, so a measurement claim sits outside it. In the same paragraph, the two numbers that were measured are right and the one recalled from memory is wrong by nearly double. **The fix is the trigger, not the number.**

---

## 6. The promises, ruled

| Promise | Ruling | Grounds |
|---|---|---|
| 2 — Small changes stay small | **not judged** — but weakened | Promise 2 turns on *"protected code"*, which `CONTRACT.md:18`, `AGENTS.md:98` and `AGENTS.md:121` all use and none defines |
| 4 — The state file tells the truth | **broken**, inherited | `state.md:7`'s 55,157 does not reproduce (56,039, two methods). Promise 4: *"Overclaiming is a bug"* |
| 6 — Fun to drive, in plain language | **broken**, and moved | Six sites closed; four filed by the promise's own fresh-reader check. Owner vocabulary still 4 of 5 — no new coined word entered, confirmed by my sweep |
| 8 — It cannot quietly grow back | **kept** | 57,348 of 100 KB, 17 files of 20, 5 skills of 6, always-read 23,240 of 50 KB. The promised deletion was actually made — `captioned` at 0 |
| 1, 3, 5, 7 | **not judged yet** | Out of this piece's reach |

---

## 7. Structure — **straining**, and the strain named

Applying the boundary this very piece installed (`judge:63`): *"Straining means the shape made the work slower or riskier, but the piece still landed honestly; fighting means the shape made the work wrong or forced a workaround before it could land."*

Not fighting. The shape made nothing wrong — the wrong sentences came from drafting — and no workaround was taken.

Straining, on this ground: **the method has no producer for a universally-quantified outcome.** `AGENTS.md:59` requires an outcome, a proof plan and a limit, and nothing anywhere checks that the proof plan can actually prove the outcome. So a piece may write "no X remains" and prove it with a re-check of an inherited list. That is the shape making the work riskier, and it produced the identical failure one piece ago. Per `worst-day.md:33`, one repeated shape, not two surprises.

**A defect in the boundary text itself, found by executing it.** *"the piece still landed honestly"* presumes landing. It gives no reading for a piece routed back for reasons unrelated to the shape — which is exactly this piece. I ruled on cause instead of on landing. One clause fixes it.

**On the count.** On my line this is the third straining ruling in a row; judgment 1 of the previous piece ruled straining and mandated this piece as the repair, while judgment 2 ruled sound. The lines diverge and that divergence is itself a finding to settle with evidence rather than rank. My evidence for straining over sound is narrow and specific: judgment 2's argument was *"a structure whose gates keep catching its builder is a structure working."* The gates did catch every defect here. But **no gate caught the staked over-claim** — it was found by the outcome simply not being met, twice, after the fact. A failure that recurs identically after being seen once is not the gates working; it is a rule that does not exist.

If judgment 2 also rules straining, the structural repair I would name is one sentence in `AGENTS.md`: an outcome that claims an absence must name what enumerates the population, or be narrowed to a listed one.

---

## 8. The two inherited items

**The never-run exemption clause — honestly closed.** Both clauses executed against real cases (section 2), correct in both directions, plus one adversarial case they correctly refuse, with the reasoning recorded so the next hand inherits behavior rather than a claim. Two honest limits stated rather than papered over: its execution is a fresh context reading it, not a runnable check; and it still deadlocks a document piece.

**The mid-review-fix silence — honestly closed as to the contradiction it names, with one adjacent silence surfaced.** The resolution is written where the contradiction lived (`judge:28`), and it routes the fix to the re-run rules *"including its own pre-fix control"*, which closes the laundering path. What it does not say: `AGENTS.md:88` requires a route-back fix to get **a new Built line in its own state-only commit**, while `judge:28`'s exception protects only *"the tree the review already ran."* So a mid-review fix that is then re-tested has no stated Built-line requirement for the fixed tree. Narrow, one step further out than the item was sent to close. **This route-back exercises `AGENTS.md:88` directly, so the fix batch will produce the missing case as evidence.**

---

## 9. Sent back — to **build**, with the exact fixes and the exact re-runs

Destination: build. A bad build stays in build (`AGENTS.md:34`). The piece keeps the live slot, stays unticked on the map, and `state.md` says what was ruled and where it routed.

### Must fix before landing

**F1 · `AGENTS.md:109`** — "Judged means its review has ruled" must not admit an insufficient ruling. Reconcile with `:86`, `:111` and `templates/state.md:6`.

**F2 · `AGENTS.md:109`** — Shaped's definition must include the hard limit on time, tokens and files read, which `:59` and `templates/piece.md:9` make mandatory and `:60` depends on.

**F3 · the dangling pointer** — either add *checks* to the proof-plan spec in **both** `map-build:18` and `templates/piece.md:11`, or point `AGENTS.md:61` at the fields that actually exist. Fix both sites or the pointer still dangles at one.

**F4 · the producer's trigger** — widen `AGENTS.md:111` so a claimed **measurement** carries the command that produced it, not only a *fixed / closed / done everywhere* claim. Then correct the build record's *"up 2.1 KB"* to the measured **+1,172 bytes**, append-only. The number is the symptom; the trigger is the fix.

**F5 · the over-claimed outcome** — do one of two things, not neither: narrow the outcome and the prediction to the owner's ratified scope (four defined, two resolved, one producer), **or** give the outcome a producer that enumerates its population. T1 hands one over ready to run: `grep -c` every term that carries a rule and read every hit whose count is 1 — all four survivors have that shape. **Do not stake zero a third time without a producer behind it.**

**F6 · `judge:63`** — the straining/fighting boundary gives no reading for a piece that was routed back. One clause.

**F7 · preserve the control** — commit the two planted claim entries as a real fixture file. The producer's control ran on text handed to T1 in its prompt; no such file exists in the repo or in git, so **I could not re-execute it** and neither can the next hand. `judge:92` asks for the original reproduction to be kept. It worked; it just was not conserved.

### Ordered, not blocking — the owner's call on sequence (section 10)

**O1 · `protected code`.** Undefined at three sites (`AGENTS.md:98`, `AGENTS.md:121`, `CONTRACT.md:18`) and it decides whether a schema migration may ride a batched review — on the second list (`:123`) and not the first (`:119`). It bit me in this judgment. Cheapest, highest-consequence.

**O2 · `caption` / `screen drawing` — one finding, two faces.** `map-build:28` orders *"grep their captions"* and no page says what a caption is; `craft:12` uses the word for a type size. The compound *captioned* died and the noun *screen drawing* lives undefined at six sites. The completion test's second bullet is unrunnable, and this piece rewrote that exact bullet. The repair is already modeled by the first bullet: a `screen:` token with an example in the template.

**O3 · `good to use` / `quality hangs together`.** Two of the four gates to proven, undefined, while their two siblings get sentences at `judge:59`. Plus the naming split: `AGENTS.md:94` says *"holds together as a quality product"*, `judge:55` and both templates say *"quality hangs together"*.

**O4 · the document piece.** One sentence: a piece whose product is a document becomes Built the same way as any other — by naming runnable checks in its proof plan and passing them.

**O5 · `state.md:7`.** 55,157 does not reproduce; measured 56,039 at `ebb9fb5` two ways. Correct it, or state the file list it was measured on.

**O6 · the receipt-opening seam** (section 1) and **the fixed tree's Built line** (section 8). One clause each.

### The exact re-run

**R1 — T1's persona, same scenarios.** Re-run the terms test on the fixed pages. Every fixed sentence carries its **pre-fix control**: quote the `48283c7` text and show the old reading it produced. Then re-run the four survivors and add T1's own free skeptical attack, reported whether it finds anything or not.

**R2 — T2's persona, same probes.** Word-diff the fix batch — the additions must drop no neighboring rule. Re-measure from the installer's own list at `bin/speck-next.js:12`. Re-run `./devsuite/run.sh --control`. Sweep siblings for F1–F3 across `README.md`, `CONTRACT.md` and `state.md`, not the installed surface alone — the gap T2's sweep left.

**R3 — the fixture.** Execute the producer against the committed fixture file from F7, so the control is reproducible by the next hand.

Then judge again. Per `AGENTS.md:88`, the fix batch writes a **new Built line for the fixed product files in its own state-only commit**, and the fix batch's receipt quotes that line.

---

## 10. For the owner — two questions, in plain words

**Q1. "Define the words" has now missed its target twice. Do we keep chasing zero, or change how we aim?**

What happened: both times, we listed the confusing words a fresh reader found, fixed every one, and predicted the next fresh reader would find none. Both times the next reader found new ones nobody had listed. The words we fixed stayed fixed — six last time, six this time. The problem is the list, not the fixing.

- **(a) Stop promising zero.** Each piece fixes the words on its list and says so. Honest, costs nothing, but "define the words" never ends — it just gets smaller each round.
- **(b) Build the list mechanically first.** Before a piece is shaped, sweep every word that carries a rule and count how often it appears; every word appearing once gets read. All four survivors this round have exactly that shape. Costs one extra session per piece and gives the promise something real to stand on. **My recommendation.**
- **(c) Accept the ratchet.** Do nothing, expect three or four more rounds.

What it changes for you: whether this is a finite job or a standing tax.

**Q2. Which of the four remaining words gets fixed next, and does `protected code` jump the queue?**

Three of the four are comprehension problems. One is not. `protected code` decides whether a database change can be reviewed in a batch with everything else or has to be reviewed on its own before shipping — and the two lists the pages offer disagree about exactly that case. It is one sentence to fix and it is the only one with data risk behind it. Recommendation: `protected code` next, in the fix batch; the other three in the round after.

---

## 11. What the next session should not relearn

- **The host may hand you a stale `AGENTS.md`.** T1 caught it and I confirmed it: the copy loaded into my context still used *hearing*, *experiencer*, *dispatcher*, *substrate* — words T2 and I both measured at zero on disk. Read the file from the commit under judgment before quoting a line number.
- **`git cat-file -s` is the second method for a byte claim.** It reproduced `git show | wc -c` exactly at four commits. Two independent methods turn a number from a claim into evidence, cheaply.
- **The installed surface is defined in code, not in prose** — `bin/speck-next.js:12`. Measure against that list and the number is arguable by anyone; measure against a remembered list and you get three different answers for the same commit, which is what the previous piece's records contain.
- **Rule the two undefined heads before complaining about them.** I had to invent a mapping for `good to use` and `quality hangs together` to do my own job, and I had to classify a fix against `protected code` to route it. Two of the four findings bit the instrument. Write the mapping down when you rule, so the next judge argues with it instead of inventing a different one.
- **A prediction is only as good as the population it ranges over.** Detectors find what is on the list. Nothing on this page produces the list.
