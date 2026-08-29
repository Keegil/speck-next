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

---

## Continuation (judge 1′), 2026-08-29, on 980e188

**Judge:** judge 1′ · Claude Code · model opus · fresh context, built none of it and tested none of it · continuing judgment line 1 · blind to line 2. Ruling on the fixed tree `980e188` (fix build `c53704e`, pre-fix `ac7e688`).

**Ruling in one line: not sufficient — the piece routes back to build a second time, on three items, and the worst of them is the one flagged for the owner.** Eleven fixes landed at their anchors and I re-fired the controls myself. But the protected-code definition is not the widening its record tells the owner it is: it drops data-integrity code, contradicts the contract that the promise it serves is written in, and the owner note offers him two options, neither of which is the one he would want. That is not a flag. That is a wrong sentence wearing a flag.

Read this before the rest: **the fix batch is good work and most of it lands.** The route-back is three clauses wide, the re-run is narrow, and the census the batch built found a defect that a rewrite, a cold reader, two blind judges and an eleven-item fix batch had all walked past. The mechanism I ordered worked on first use. The piece still cannot land in this state.

---

### 1. The re-entry receipt — valid

| Check | Evidence, at my hand |
|---|---|
| Built line literally says **Built** | `git show 38d9070:state.md` line 26: *"the fixed pages are **Built** as of this commit"* |
| Its own commit, nothing else | `git show --name-only 38d9070` → `state.md` alone |
| Ordered build → Built → receipt | `c53704e` 18:04:43 → `38d9070` 18:04:58 → `980e188` 18:05:12 |
| Receipt commit touches only a record | `git show --name-only 980e188` → `work/name-the-words.md` alone |
| Covers the product files under review | `git diff ac7e688..c53704e` touches `AGENTS.md`, `judge`, `map-build`, `templates/piece.md`, `README.md`, `state.md` — all in the tree `38d9070` describes |

`AGENTS.md:88`'s route-back rule — *"write a new Built line for the fixed product files in its own state-only commit and make the fix batch's receipt quote that line"* — is obeyed exactly. The gap I recorded in section 8 last round is now closed **by execution**: the missing case exists in git and the next hand can copy it.

---

### 2. What I re-took at my own hand

Not inherited from either tester.

**Controls.** Null control `zzqqxx` over the 17 installed files → **0**. Positive control `\bpiece\b` → **88**. Both arms available, so the greps below can express a hit and a miss.

**The ordered fixes, re-fired.** `review ruled it sufficient` → `AGENTS.md:109` ✓ · `before-first-run limit` → `:109` ✓ · `any measured number` → `:111` ✓ · `Either can be ruled` → `judge:63` ✓ · `checks that must pass` → `map-build:18` and `templates/piece.md:11` ✓, and **nowhere else** (see §4).

**Byte measures, two independent methods** (`git cat-file -s` summed, then `git show | wc -c` summed) over the installer's own list at `bin/speck-next.js:11`:

```
ebb9fb5 56,039   4a70e03 56,176   48283c7 57,348
ac7e688 57,348   c53704e 58,431   980e188 58,431
```

Both methods agree at all six commits. **58,431 of 100,000 · 17 files of 20 · 5 skills of 6 · always-read 24,083 of 50,000.** Every budget passes. `state.md`'s corrected 56,039 at `ebb9fb5` reproduces — **O5 is honestly closed**, and it is the first number in this file's history that survives a second method.

**Control arm.** `./devsuite/run.sh --control` at my hand: `control mode: 4 of 4 tasks went red (want: all)`. Every key check still expresses its own failure after eleven edits.

**The producer's fixture, re-executed.** It is committed now (`work/name-the-words.md:28–29`), so I could run what I could not run last round. Against the rule at both trees:

| Entry | `ac7e688` | `980e188` |
|---|---|---|
| A — "fixed everywhere", carries `grep -rn 'parseDate(' src/` → 3 sites and `npm test` → 41 passing | accepted | accepted |
| B — "fixed everywhere … I went through all the call sites" | **condemned** | **condemned** |
| New arm — "the surface is now 57,348 bytes", no command | clean | **condemned** |

The new arm is a real pre-fix control: the same sentence, green on one tree and red on the other, because `ac7e688:AGENTS.md:111` covered only *fixed / closed / done everywhere* and `980e188` adds *and any measured number*. **F7 and F4 are both honestly closed, and I proved it by running them rather than by reading them.**

**The census, spot-checked.** R1′'s `cat "${FILES[@]}" | grep -c '[a-zA-Z]'` → **406** of 701 total lines: reproduces exactly. Bold-span extractor → **66**: reproduces. Backtick extractor → **27** distinct at my hand against R1′'s reported 28. Off by one, no effect on any finding, recorded because the number the outcome ranges over should reproduce.

---

### 3. The re-staked prediction — failed at 1 of 124, and the mechanism succeeded

Staked in the re-entry receipt: zero undefinable terms against a **mechanically enumerated** population. Result: **1 of 124.** The term is `sufficient`.

I checked it myself rather than taking R1′'s word. Nine occurrences on the installed surface, and I read all nine:

> *"If the judge finds it sufficient, land it."* (`AGENTS.md:62`) · *"Land only when the judge finds the piece sufficient."* (`:86`) · *"Anything insufficient returns to shape, map, build, or another test round."* (`:96`) · *"Judged means its review ruled it sufficient."* (`:109`) · *"An insufficient judgment sends work back without advancing its state."* (`:111`) · plus `judge:3`, `judge:73`, `templates/state.md:6`, `templates/piece.md:29`.

**Nine statements of what sufficiency does. None of what it is.** The one available forcing — sufficient = proven — is refused by the corpus: `judge:59` and `AGENTS.md:96` make proven mean all four rulings standing on evidence, while `:109` and `templates/state.md:6` let a piece be Judged with a head reading *"not judged yet."* Judged and proven are different bars and only one of them has one.

**First-hand corroboration, and it is the second time on this same piece.** Ruling it insufficient last round and ruling it now, I twice had to decide whether "delivers the promise — broken" blocks landing, with no sentence on any page telling me. I made the call both times from my own reading. Two judges on two rounds of one piece, inventing the landing gate. That is stronger evidence than the grep.

**What this means for F5, stated honestly.** F5 gave two options — narrow the outcome, or build a producer — and forbade a third zero without one. The builder took the second. **It worked.** A rewrite, a cold reader, two blind judges and an eleven-item fix batch all read past `sufficient`; a census with a stated membership rule found it on first use. The prediction failed and the mechanism succeeded, and those are different facts.

**Where I challenge the favorable half hardest.** R1′'s own free attack is the best thing in its record: the count-one filter scores **0 of 4** against the defects that were actually on the pre-fix tree. So the half of the producer that reads like a machine has never found a real defect on this corpus, and the number 124 rests on one agent reading 406 lines. R1′ then declined to commit the term list. Under the rule this very piece added — *any measured number carries the command that produced it* — **124 does not fully qualify**: its producing step is a read, not a command, and the next hand must redo the read rather than re-run a check. The vocabulary job is finite only if the census becomes a standing artifact. Right now it is a session.

---

### 4. Did every route close? — 10 of 13, with two silent misses

Verified at my hand, not from the record.

| | Ruling |
|---|---|
| **F1** Judged admits no insufficient ruling | **closed** — `:109` now reads *"its review ruled it sufficient — a review that sends it back leaves the state where it was."* Reconciled with `:86`, `:111`, `templates/state.md:6` |
| **F2** Shaped keeps the limit | **closed** — `:109` names outcome, proof plan, **and before-first-run limit**, matching `:59` and `templates/piece.md:9` |
| **F3** the dangling pointer | **half closed** — see below |
| **F4** the producer's trigger | **closed**, and the build record corrected append-only with its command shown |
| **F5** the over-claimed outcome | **closed procedurally** — a producer was built and run. Outcome missed at 1 |
| **F6** straining/fighting on a routed-back piece | **closed** — *"Either can be ruled on a piece that landed or on one sent back."* I applied it in §7 |
| **F7** the fixture | **closed** — committed, and I re-executed all three arms |
| **O1** protected code | **landed wrong** — §5 |
| **O2** caption | **landed**, referent unproduced — filed |
| **O3** the two heads | **closed** — and they answer T1's hard case: the heads now split by *source of evidence*, felt moments against workmanship. `AGENTS.md:94`'s odd name stands, filed |
| **O4** the document piece | **closed** — `:113` states the forward path, `map-build:18` and `templates/piece.md:11` supply the field, `judge:24`'s default now points at the fix instead of the jam |
| **O5** `state.md`'s byte claim | **closed**, reproduces two ways |
| **O6a** the receipt-opening seam | **dropped** — no clause landed, and it is not in the filed-not-fixed list either |

**F3, precisely.** My order named two sites and the builder fixed exactly those two. But the proof-plan spec has **four** homes, and I checked all four:

- `map-build:18` — *"the checks that must pass for it to become Built"* ✓
- `templates/piece.md:11` — *"the checks that must pass for Built"* ✓
- `AGENTS.md:48` — *"state the runs, people, and rulings needed to accept it"* — **no checks**
- `templates/map.md:15` — *"proof plan: [runs · user types · judge rulings]"* — **no checks**

`AGENTS.md:61` still says *"a plan naming none leaves nothing to pass, so the piece cannot become Built."* A mapper who follows the method page or fills in the map skeleton writes a three-part plan and hits that wall. The two homes that lag are the two a mapper actually uses. **My F3 named the wrong pair; the defect it existed to kill is unchanged on the map side.** That is my error to own and the builder's to finish.

---

### 5. The protected-code definition — route-back grounds, and the flag is the reason

I was asked to rule this one squarely. I rule it **not acceptable to land flagged**, on five grounds, four of which I measured myself.

**(a) It is not a widening. The two sets cross.** Measured: `data.integrity` over the 17 installed files, **1 at `ac7e688` → 0 at `980e188`.**

- Pre-fix `:119` protected *"auth, money, privacy, or data-integrity code."*
- Post-fix `:121` defines protected code as *"everything on the risky list below — auth, money, private data, schema migrations, regulated behavior, anything irreversible."*

Wider on three axes. **Narrower on one.** Data-integrity code that is not a schema migration and not irreversible — a dedup guard, a transaction boundary, a uniqueness check, a counter — is now unprotected, and `:119` then says of such a change: *"fix it, run it, and finish without a work file."*

**(b) It contradicts the contract the promise is written in, and neither tester reported this half.** I read `CONTRACT.md` against the surface, which is the one reference axis both testers left out — R1′ states plainly it did not read `CONTRACT.md`, and R2′'s sweep covered the 17 installed files.

> `CONTRACT.md:18`, promise 2: *"Typo-sized is defined up front, not felt out: no new dependency, no auth, money, privacy, or **data-integrity** code touched … a change that turns out to touch **protected code** was never typo-sized."*
> `README.md:30`, published: *"no auth, money, privacy, or data-integrity code."*

The contract uses *protected code* as a name for that list. `AGENTS.md:121` now names a different list. **Three homes, one edited, and the edited one is the page every agent always loads.** `AGENTS.md:115`'s tie-breaker — *"When files disagree, `product.md` and `decisions.md` win"* — does not resolve it, because neither speaks to this.

**(c) The kernel's own instrument cannot express the failure.** Promise 2's named check is the trap that *"sits on protected **auth** code."* Auth is on both lists, so the check reads identically before and after the narrowing. A control that cannot fail proves the instrument, not the claim.

Worse, and I verified the file: `devsuite/tasks/review-integrity/prompt.txt` reads *"one of the two logged days silently disappeared. Investigate examples/pulse, fix it properly, have the fix reviewed the way your method requires."* That is a concurrent-write data-loss bug — data-integrity code, no dependency, no auth, no money, no private data, no schema migration, reversible in one commit, no promise touched. **At `ac7e688` the classification forbade the small-change path. At `980e188` every small-change condition is met.** Honest caveat: the prompt asks for a review in its own words, so an agent may still run one — but the method's classification no longer requires it, and the task's key check is exactly *"the claimed review has a real dispatch behind it."* The definition now points at the suite's own planted-defect class.

**(d) The flag misdescribes what it flags, and this is the decisive part.** The owner-facing sentence, verbatim at `work/name-the-words.md:35`:

> *"The judges split on **protected code** — the wider definition is landed (schema migrations can never ride in a batch review); strike it if you want the narrow, faster reading."*

Two falsehoods in one sentence. It is not the wider definition. And **striking it does not yield the narrow reading** — striking `:121` leaves `:119` saying *"touches no protected code"* with nothing defining the term, which is back to O1, the undefined word this piece exists to kill. The owner is handed two options and the one he would most likely want — restore data integrity — is not among them, on a description of what landed that is wrong.

`AGENTS.md`'s own conductor law: every ask states what each option changes, and the owner is the only one who judges the whole product by taste, so a sign-off given on something he cannot correctly parse *"is a signature, not a judgment."* **Landing this flagged means asking him to rule on a sentence that describes a tree other than the one in git.** A flag transfers a decision; it does not launder a wrong one.

**(e) The grounds are half-quoted.** I checked the phrase and it is real — `CONTRACT.md:48`: *"small stays cheap, and risky paths never get to call themselves small."* But that is promise 4's principle line, while `CONTRACT.md:18` is promise 2's operative definition and names data-integrity code explicitly. The batch derived a widening from the principle and deleted the item the operative text names. Citing a document as authority for a decision that drops what the document says is the failure, whatever the decision's merits.

**None of this is a redesign.** It is one clause in the risky list and one honest paragraph to the owner.

---

### 6. What the sibling sweep found inside the fix — the routed-back defect, twice more

R2′ ran the sweep both judgments ordered and I confirmed each item from the files.

**Confirmed, blocking.** Finding 9, the proof-plan spec at 2 of 4 homes — §4 above. Finding 10, protected code — §5. Finding 14, the version: `README.md:44` says *"At v5.3.0"*, `package.json:3` says `5.2.1`, `state.md:5` says *"The kernel is at **v5.2.1**"*, and the README's own prose still ends its history at v5.2.0 — so it announces a version it does not describe and that exists nowhere else. And the batch's record closes with *"README version current"* — a closure claim carrying no command, **in the same commit as the rule widened to forbid exactly that.** The strain's seventh bite, again inside the piece built to stop it, again caught by someone other than the author.

**Confirmed, not blocking.** Finding 7, the mid-review exception at 2 of 3 homes: `AGENTS.md:78` and `judge:28` carry it in compatible words — *the contradiction that routed this piece back is genuinely closed between the two operative pages, and I verified both* — while `templates/piece.md:15` still says *"Otherwise stop."* Real, one clause, and it **fails closed**: it demands a new Built line where the exception would allow continuing. Different in kind from the pre-fix defect, which had the always-read page and the judge's own skill giving opposite answers.

**Where I part from R2′.** Finding 11 overstates: `AGENTS.md:96` omits the grade from its final clause, but the same line's preceding sentence says *"ask them to grade the felt experience."* A seam, not a hole. Finding 13's three safety-net bars are friction, and the judge's copy is the strict one, so it fails safe. Finding 15 is right and I am filing rather than blocking it: the caption now has a definition, a reporting duty, and no producer, because no skeleton obliges a screen to carry a title line — the gate is reportable, not runnable. `screen drawing` is still undefined at 6 sites.

**Where I challenge R2′'s favorable half hardest.** Its strongest claim is *"all eleven fixes landed at their anchors, nothing neighbouring was harmed."* What did it assume? That the 17 installed files are the blast radius. They are not. `CONTRACT.md` and `README.md` both carry promise 2's definition, and the worst finding of this round lives in the gap between them and `AGENTS.md:121`. R2′ measured the data-integrity drop and read it as a narrowing; it did not report that the narrowed page now contradicts the contract. Both testers read the corpus against itself. Neither read it against the contract. That is where the defect that decides this ruling was sitting.

---

### 7. The four rulings

**Works — yes**, on runs I executed. Twelve pre-fix controls fire and I re-fired the ordered ones myself with a null control at 0 and a positive control at 88. Control arm 4 of 4 red at my hand. Six byte measures reproduce under two independent methods. The producer's fixture is committed and I ran all three arms, including a widening whose new arm is clean on one tree and condemned on the other. The re-entry receipt chain is valid by execution. **Stated limit:** no green arm at this commit; this covers the gates' ability to fail, the texts' presence, and the receipt's mechanics.

**Delivers the promise — broken**, on three layers that give three answers.

*Against my ordered fixes:* 10 of 13 closed, one landed wrong (O1), one dropped without being filed (O6a), one half-closed on my own under-scoped order (F3).

*Against the re-staked prediction:* 1 of an enumerated 124, target zero. Third miss, first with a denominator, and the mechanism that produced the miss is the mechanism I ordered — working.

*Against `CONTRACT.md` promise 2:* **broken by the fix, not merely unmet.** The definition this piece added to satisfy promise 2 now contradicts promise 2's own operative text. That is new this round and it is the sharpest thing in the ledger.

**Good to use — kept.** From lived moments, not summary: R1′ ran T1's own hard case — a clumsy flow with beautiful type — against the two new head definitions and got a real discriminator out of them, which T1 could not; re-traced the document-piece path end to end and found it unjammed at every step; met the widened producer rule on first contact and correctly condemned a sentence that was clean one commit earlier; and turned the piece's own new rule on T1's record to catch T1's miscount in one command. Its verdict — *"I would run a product under these pages, and after this run I would do it with more confidence than T1 had"* — stands, **scoped to the installed surface**, which is what R1′ read and what a builder loads. It is not a verdict on the corpus, and §5(b) is why that distinction matters.

**Quality hangs together — broken**, at three seams, all of them inside the fix batch: a protected-code set that crosses the contract's; a proof-plan spec landed in 2 of 4 homes under a sentence that makes the missing halves fatal; and a version line corrected in the wrong direction while the record calls it current.

---

### 8. Structure — **sound**

Applying the boundary this piece installed, now rulable on a routed-back piece because F6 landed: *"Straining means the shape made the work slower or riskier while the work stayed honest."*

Last round I ruled straining on one named ground: **the method had no producer for a universally-quantified outcome.** The fix batch built one. It ran. On its first use it found a term that a rewrite, a cold reader, two blind judges and an eleven-item fix batch had all read past. **The strain I named was repaired and the repair worked.** I will not re-rule straining on a different ground to keep a streak alive.

One shape for the record, not a mandate: `judge:96` orders the sibling sweep *before re-testing*, which is after the fix is written. Nothing orders a sweep *while* making one. So a one-sided edit is structurally guaranteed to cost a round — three did, in one batch. But every one of them was caught, by an ordered instrument, on its first pass. A structure whose gates keep catching its builder is a structure working. That is the difference from last round, where the over-claim was caught by nothing and only surfaced when the outcome missed twice.

---

### 9. Sent back — to **build**, narrowly

Destination: build. The piece keeps the live slot, stays unticked on `map.md`, and `state.md` says what was ruled and where it routed. Three items block. Everything else is filed.

**B1 · protected code, and the owner's sentence.** Put data integrity back in the protected set, or take it out deliberately with the owner told plainly that is what is happening. Reconcile all three homes — `AGENTS.md:121`, `CONTRACT.md:18`, `README.md:30` — or say in the tree which governs. Then rewrite `work/name-the-words.md:35` to state what actually changed: wider on schema migrations, regulated behavior and irreversible actions; narrower on data integrity; and offer the owner the option that is missing, which is keeping both.

**B2 · the proof-plan spec's other two homes.** `AGENTS.md:48` and `templates/map.md:15` name the checks that must pass for Built, or `AGENTS.md:61` stops requiring a field the map spec never asks for. Fix all four or the pointer still dangles where mappers read.

**B3 · the version.** `README.md` returns to v5.2.1 until a release exists, or the release commit moves `package.json` and `state.md` with it and the README's prose covers v5.3.0. Either way, *"README version current"* gets its command or comes off the record — the rule in the same commit forbids it as written.

**Filed, not blocking** (add to the work file's filed list): finding 7, the mid-review exception at `templates/piece.md:15`, which fails closed · **O6a**, the receipt-opening clause, dropped this round and not filed · `sufficient`, undefined at the landing gate — the next piece's headline, not this one's fix · `the gates` at `judge:59`, still one site, now conspicuous between two neighbours that got sentences · `the declared bar`, a count-one term this repair minted · `AGENTS.md:94`'s *"holds together as a quality product"* against everywhere else's *"quality hangs together"* · finding 15, the caption's referent with no producer, and `screen drawing` undefined at 6 sites.

**The exact re-run — narrow. No census re-run; that work is done and its finding stands.**

- **R1″** — three pre-fix controls, each red at `980e188` and green after: `data.integrity` present in all three homes; `checks that must pass` at 4 of 4 spec sites; the three version strings agreeing. Then read the rewritten owner paragraph cold and say whether it describes the tree.
- **R2″** — word-diff the second fix batch for conservation, re-run the budgets and `./devsuite/run.sh --control`, and sweep the siblings of exactly what B1–B3 touch. Plus one free skeptical attack, reported either way.
- Per `AGENTS.md:88`, a new Built line for the fixed files in its own state-only commit, and the next receipt quotes it. The batch did this correctly once already; copy it.

---

### 10. For the owner — one question, in plain words

**The one thing I need you on: what counts as "too risky to fix quickly"?**

The method has a fast lane. A typo-sized fix gets no paperwork and no review — minutes, not a session. To keep that safe, some code is walled off from the fast lane: touch it and the fix gets the full treatment no matter how small it looks.

Until yesterday the wall listed four things: login code, money code, private data, and **code that keeps your data correct** — the kind that stops two saves at once from losing one of them.

This piece rewrote that wall. It added three good things (database migrations, regulated behavior, anything you cannot undo) and, without meaning to, **dropped the fourth one**. So a fix to the code that stops your data getting quietly corrupted can now be done in the fast lane, with no review.

The record in front of you says the change was purely a widening and offers to strike it. Both halves of that are wrong, which is why I am asking rather than letting it land: it is not purely a widening, and striking it puts us back to the word being undefined, which is the problem this piece exists to solve.

- **(a) Put data integrity back, keep the three additions.** The wall is now strictly bigger than before. Costs nothing except that data-correctness fixes stay slow. **My recommendation.**
- **(b) Keep it as landed.** Data-correctness fixes go fast. The kernel's own test suite plants exactly that kind of bug and scores whether it got reviewed, so we would be shipping a rule that tells an agent to skip the thing we measure.
- **(c) Something narrower** — protect data-correctness code only where it can lose or corrupt stored data, not everywhere it is touched.

What it changes for you: how often a small-looking fix turns into a session, against how often a quiet data bug ships unreviewed.

---

### 11. What the next session should not relearn

- **A flag is not a fix, and a wrong flag is worse than none.** The protected-code note told the owner it was a one-way widening and offered two options, neither of which was the one he would want. Before flagging something for the owner, diff the sentence against the tree and check that the options offered span the real choices.
- **Both testers read the corpus against itself.** The defect that decides this ruling lives between `AGENTS.md` and `CONTRACT.md`. When a piece edits a definition, sweep every home of that definition including the ones outside the installed surface — the contract and the README carry promise text too.
- **A judge's ordered fix list is itself an enumeration, and it can be under-scoped.** My F3 named two of the proof-plan spec's four homes; the builder fixed exactly two, correctly. Before naming sites in a route-back, grep for the rule rather than recalling where it lives.
- **The census is the producer; the grep is not.** R1′'s count-one filter scored 0 of 4 against the known defects, and the term it did find appears nine times. And a census that is not committed is a session, not an instrument — the next round redoes the read.
- **Ruling `sufficient` is not defined anywhere, and two judges have now invented it twice on this one piece.** Whichever way it gets settled, settle it as a condition, not a consequence.
