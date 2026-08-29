# Judgment 2 — "A builder's words, and fewer of them"

**Judge:** judge 2 · Claude workflow agent · model opus · 2026-08-29 · ruling on the build at `e5494cf`, opened under the receipt committed at `647cd99`. Blind to judgment 1; I did not open `builders-words-judgment-1.md`.

**What I did and did not do.** I built none of this and tested none of it. I read the piece's work file, both tester records, `CONTRACT.md`, `product.md`, the 2026-08-29 entries in `decisions.md`, the rewritten `AGENTS.md` in full, the rewritten `experience`, `judge`, `shape-product`, `map-build` and `templates/piece.md`, and the diff `44a48ba..e5494cf`. I then re-took every checkable claim at my own hand: re-measured the bytes, re-ran the killed-term sweep, spot-verified inventory entries in `AGENTS.md`, `experience`, `judge`, `map-build` against the pre-rewrite text, wrote my own probe strings for the review-integrity regex and ran both versions, and checked the receipt's commit ordering with git. Checking is not using; where a ruling rests on a tester's run rather than mine, I say so.

---

## 1. The receipt

**Valid.** Checked myself, not taken from the record.

```
$ git show e5494cf:state.md | grep -n "Built"
27:**The live piece: "A builder's words, and fewer of them" — Built.**
```

The quoted line exists at the cited commit and literally says **Built**.

Coverage, under the reconciled rule the work file states (the line may ride in the build's final commit, or in a records-only commit just after it; invalid if any build commit lands after it, or if it was written after the receipt opened):

```
$ git log --oneline --name-only 44a48ba..647cd99
647cd99  work/builders-words.md                    ← receipt only
e5494cf  AGENTS.md, 5 skills, 4 references, 6 templates, devsuite check, state.md, work file
82fbddb  CONTRACT.md
c99cc21  work/builders-words.md
24d9f52  work/builders-words.md
```

`e5494cf` is the build's final commit and it carries the Built line. Exactly one commit lands after it, `647cd99`, and it touches only `work/builders-words.md` — a records file, not a build commit under the definition the same rewrite added ("a build commit changes the product itself, such as code, screens, or data"). The receipt opened in that later commit, after the Built line was written. Every condition holds.

One thing worth saying out loud, since I am the first judge to run this rule in its new form: the reconciled rule is what saved this receipt. Under Sol's stricter draft — Built in its own empty commit — this receipt would have been invalid, and the merge correction that loosened it is the reason a hearing could open at all. The correction was right and the ordering check still bites: `647cd99` being records-only is a fact I proved with git, not a fact I read.

---

## 2. Hearing the records

### R1 — the stranger who builds

I sustain most of R1's record and I strike part of its headline.

**Struck.** R1's verdict opens: *"Could I build a great product under these pages? Yes, and I would want to."* The record behind it contains no build. R1 read sixteen files, chose a phase, and computed a cost. It never wrote a work file, never wrote a Built line, never opened a receipt, never dispatched anyone, never ran a piece loop. Under my own §1 — every verdict claim points at a moment in that record — the part of that claim covering build-loop execution is ungrounded and I strike it.

**What survives, and it is substantial.** R1 grounded three things in moments it actually lived: it reached the correct first move from the dispatcher in one pass (Part 3(a)); it computed the cost of reviewing a piece from the pages alone and landed on three fresh sessions (Part 3(b)); and it produced eighteen located stumbles with quotes. Those are real reading moments and they carry the record.

**The strike is a finding about the dispatch, not about R1.** The persona was named "the stranger who builds" and the dispatch bought a stranger who reads. That gap matters because the pages' actual job is to be executed by an agent, not parsed by one. The strongest "works" evidence this hearing could have produced — a fresh context running one full piece loop in a scratch product under nothing but these sixteen files — was never bought. Recorded for the next pages-rewrite hearing.

**Challenging the favourable parts hardest.** R1's Part 2 lists fifteen things it could execute cold. I put the load-bearing one to the test myself rather than take it: R1 claims the cost sentence at `AGENTS.md:70` is computable and matches. I checked the arithmetic against the pages — `experience` line 53 (at least the first two personas for a substantial piece) plus `judge` line 14 (a fresh context per piece) gives three, and `AGENTS.md:70` says "at least two testers and one judge." It matches. That one holds at my hand, not just R1's.

### R2 — the conservation prober

Every executed claim I re-took reproduced. I sustain the record, and I qualify one headline.

**Re-taken and confirmed:**

| R2's claim | my own measurement | verdict |
|---|---|---|
| pre-rewrite surface 70,770 bytes | summed all 17 files at `44a48ba` → **70,770** | confirmed to the byte |
| post-rewrite 55,038 | `wc -c` over the same 17 files → **55,038** | confirmed to the byte |
| ≤ 65,000 target | 9,962 bytes of headroom | confirmed |
| seven killed terms at zero | my own sweep: *the wire* 0 · *proven-means* 0 · *dispatcher* 0 · *route-back* 0 · *experiencer* 0 · *charter* 0 · *hearing* 0 · *substrate* 0 · *frame* 0 | confirmed, and two terms beyond R2's list are also at zero |
| "dispatch proof" at six sites | my own grep: `shape-product:16`, `map-build:35`, `experience:12`, `experience:25`, `judge:20`, `worst-day:59` | confirmed, and see §3 — I found an aggravating fact R2 did not |
| three scar clauses removed | `grep "three separate fresh"` → 0 hits (1 hit pre-rewrite); same for both provenance lines | confirmed |
| widened check catches new-vocabulary claims | my own probe strings, both regexes — see §4 | confirmed with one nuance |

**Qualified.** R2 reports "**0 entries MISSING**" across all 177. For the two question files R2 did a full old-vs-new diff, which is strong evidence. For `AGENTS.md`, `experience`, `judge`, `craft`, `walk`, `worst-day`, `shape-product` and `map-build`, R2 sampled — "sample-quoted per section" — and asserted section coverage. I spot-verified five entries myself against the pre-rewrite text (A5, A34, J12, J14, M6) plus the E-section receipt and identity-proof clauses. Four of the five are cleanly conserved. **The fifth is not**, and R2's method could not have seen it:

> **M6 lost its locator.** Pre-rewrite: *"the frames' own captions **in the shaped decks** — grep them, count them, match them against the map."* Post-rewrite: *"every captioned screen drawing belongs to exactly one piece"* … *"Grep, count, and match the named sets."* The phrase that told you **where the population lives** is gone, inside a gate whose own next sentence insists it is mechanical ("Do not assert it").

So R2's headline stands **at rule granularity** and needs a qualifier **at sub-clause granularity**. That qualifier is the most useful thing this hearing produced and I give it its own section below.

### Holding the two records apart

R1 and R2 disagree on one thing and I am not averaging them.

On "dispatch proof": **R2 calls it a load-bearing defect.** **R1 explicitly declined to count it** — listing it among "near-misses I decided not to count, since proximity binds them well enough: … *dispatch proof* (= the committed receipt)."

Both are true of what each measured. R1 is true of *comprehension*: a careful reader can resolve the term from context in one pass, so it does not stop a builder. R2 is true of *consistency*: the term is a second, undefined name for the method's most load-bearing artifact, introduced by a rewrite whose whole claim is one consistent register. R1 was asked whether the pages are understandable; R2 was asked whether the rewrite kept its contract. The term passes the first test and fails the second. I rule on the second, because it is the one this piece staked.

---

## 3. The finding that routes this piece back

**"dispatch proof" is not a surviving old term. It is a new coinage this rewrite created.**

R2 established that it exists at six sites and that the build record's claim to have removed it is false. I checked something R2 did not, and it changes the severity:

```
$ for f in <all 17 installed files at 44a48ba>; do
    git show 44a48ba:"$f" | grep -iE "dispatch[- ]?(time )?proof"
  done
  (no output)
```

**Zero occurrences before the rewrite.** The pre-rewrite pages used `receipt`, sometimes modified ("a dispatch-time receipt" at `shape-product:8`) — always the defined word. This rewrite invented "dispatch proof" and planted it at six sites, five of them skill files, for a thing the same rewrite bolds and defines one paragraph away (`experience:16` — "commit a **receipt**: written proof of who was asked to test what").

Why this is a route-back and not a note:

- **It violates the piece's own staked property.** Whole-property 2: *"No new coinage — the owner's word budget stays 4 of 5."* This is a new coinage, and it is the piece's own instrument that says so.
- **It violates the law this very skill states.** `judge` §5: *"Undefined jargon that carries a rule is a defect because the owner cannot judge what they cannot understand."* The rule it carries is a phase exit condition at `shape-product:16` and `map-build:35`.
- **It is worst exactly where it does most damage.** `judge:20` is a section heading — "### 1. Check the dispatch proof" — and the body's first sentence switches vocabulary: "Start with the **receipt's** Built field." A heading naming one thing over a body naming another, in the file that outlaws the pattern.
- **The record overclaims against the committed text.** The build record says the coinage was *"replaced with the defined word receipt."* The receipt says *"Convicted terms at zero across the surface."* Both are false as committed. The builder correctly identified the defect, fixed it in `AGENTS.md`, and never propagated it to the five skill files — then wrote the claim as though it had. Under `state.md`'s own law, claim nothing beyond the evidence.

This is a remediation that closed in one artifact and was reported as closed in all of them. That is a distinct failure from the coinage itself and it must be fixed in the record whatever else happens.

---

## 4. The predicted effect — measured, honestly

The piece staked three falsifiable claims and said: *"Any of the three failing = the rewrite failed its own point, and this file says so."*

**(a) R1 answers the three questions correctly — HELD.**

- *What do I do first in a fresh repo?* R1 reached the dispatcher, fired the first bullet, and named the concrete first move: a message to the owner opening with the phase, asking the outcome question, with `work/shaping.md` and `product.md` started from their templates. Correct, in one pass.
- *What does checking one piece cost?* R1 computed three fresh sessions for an ordinary substantial piece, four for risky, six for a milestone, six for one rejection cycle, and seven from empty repo to first landed piece. I re-derived the floor from the pages myself and it matches, and it matches the headline sentence at `AGENTS.md:70`. Correct, unaided.
- *What do the four state words mean?* R1 defined Built and Judged crisply from the pages, quoted Live's condition while reporting honestly that Live's *meaning* is never stated, and reported that Shaped cannot be defined at all. Two clean, one partial, one absent — and R1 said so rather than guessing. That is a correct answer about the pages, and the deficit belongs to (b).

**(b) Zero undefinable load-bearing terms — FAILED as written. Held against every term it named.**

R1 flagged six: *Shaped* · *Live, and its boundary with Judged* · *care level* · *straining vs fighting* · *screen drawing* · *"its own checks"*. I verified all six myself by grepping the loaded surface; every one is genuinely undefined there. Six against a target of zero. **The prediction failed.**

Two facts make the failure legible rather than just bad.

First, **the three terms the prediction actually named are gone.** The stated baseline was *"three — 'the wire', 'charter', 'frame' — plus an uncomputable cost."* My own sweep: *the wire* 0 hits, *charter* 0 hits, *frame* 0 hits. And the cost is now computable — R1 computed it exactly, unaided, and it matched. Against its own enumerated baseline the rewrite went four for four.

Second, **five of R1's six are pre-existing gaps this rewrite conserved faithfully.** I checked each against `44a48ba`: the shape-phase judge told to check a Built line that cannot exist (R1's S1) is word-for-word the same trap in the old `judge` skill; *Shaped*, *care level*, *straining/fighting*, *"its own checks"*, and the Judged/Live altitude collision all predate the rewrite. The rewrite did not create them. It made them **visible** — which is why a stranger found them in a single read, and which is the rewrite working, not failing.

So the honest verdict on (b): the instrument was an enumeration of three terms, and it could not see terms nobody had enumerated. The prediction was scored against a list; the property lives outside any list. The rewrite cleared the list and the property still failed. That is the exact shape of an unenumerated property, firing on this piece's own instrument.

**(c) Dev suite green arm 4/4 on the rewritten kernel — NOT YET MEASURED.**

I checked at my own hand rather than reporting the receipt's "pending":

```
$ git -C <scratchpad>/green-subject rev-parse HEAD
e5494cf6d1af60b988f65671bd2d1baaa597fed7          ← correctly pinned
$ cat .../tasks/b5bkinge4.output
e5494cf                                            ← 8 bytes: the clone's SHA, no suite result yet
$ pgrep -fl "devsuite/run.sh"        → alive
$ ls /tmp/claude-501/devsuite-runs/run-1788011626/
bug-hunt  honest-state  review-integrity  small-change     ← task 4 of 4 still driving
```

The green arm is running on a clone correctly pinned at `e5494cf`, and it is on its fourth and last task. Its result does not exist yet.

**Everything I rule below about `works` is conditional on that arm.** If it returns 4/4, my works ruling stands as written. If it returns anything less, that ruling converts to "check failed" and the piece routes to build on that ground in addition to the ones below. Landing must not be asked before that number is read back and written into this file.

**Prediction verdict: partially held.** (a) held. (b) failed as written, held against its named baseline. (c) unmeasured. The work file must record all three exactly this way.

---

## 5. The four rulings

Ruled separately. None compensates for another.

### Works — **kept, on the pages' own path; one arm outstanding**

The product here is a set of pages an agent loads and executes, so "the real path" is an agent running the method from nothing but those pages.

- **Real-path run 1, and the record does not claim it as one:** R1 *is* the real-path run. A fresh context loaded only the sixteen installed files and executed the method's entry point — chose the phase from the dispatcher, produced the correct first action, and computed the review cost from the pages. That is the product doing its actual job for its actual user. It is the strongest works evidence in this hearing and neither tester framed it that way.
- **Real-path run 2, re-taken by me:** the widened review-integrity check. I wrote my own probe strings and ran both regexes rather than reuse R2's:

  ```
  probe                                      OLD    NEW
  P1 new-vocab with judge ruling            True   True
  P2 new-vocab receipt wording             False   True   <-- widened
  P3 new-vocab "the review ran"            False   True   <-- widened
  P4 new-vocab "a tester tested"           False   True   <-- widened
  P5 old-vocab control                      True   True
  P6 old-vocab "hearing convened"           True   True
  N1 no review claimed                     False  False
  N2 lifted verdict, no reviewer           False  False   -> else-branch RED
  N3 honest "not judged yet"               False  False   -> else-branch GREEN
  ```

  The four-way control holds: old vocabulary still covered, new vocabulary now caught, silent when nothing is claimed, and RED on a lifted verdict with no reviewer behind it. The instrument can still express the failure it exists to rule out.

  **One honest nuance R2's probe did not surface:** my P1 matched the *old* regex too, because any claim mentioning a judge ruling was already caught. The genuine new coverage is claims that name testers without naming a judge. The widening is real and strictly additive; it is narrower than "the old check would have missed the new vocabulary entirely."

- **Outstanding:** the dev suite's four-task green arm, unfinished. Per §4(c) this ruling is conditional on it.

Under my own law I state the reference: this "works" covers the pages' entry path and the gates. It does not cover a full piece loop executed end to end under the rewritten pages, because nobody was dispatched to run one.

### Delivers the promise — **kept, with a named shortfall**

Judged against the owner's verbatim order and `CONTRACT.md` promises 6, 7 and 8.

**The owner's order** — *"turn Speck Next into actual product building language instead of fucking methodology lingo… I don't understand jack shit of what you're saying."*

Delivered in the main, on the best evidence obtainable: a reader who had never seen Speck read the entire installed surface and reported that the spine is executable cold, that `walk.md` and `craft` are the two files they would hand a new teammate, and that "the word 'hearing' is gone — everything is 'review', 'tester', 'judge' — words I already owned." I confirmed the register change myself by reading `AGENTS.md`, `experience` and `judge` end to end: plain declarative sentences throughout, and nine method words at zero occurrences.

Not delivered completely: R1 counted about eight sentences needing a second pass and two needing a third, plus six terms it could not define. Against the owner's own reopening condition — *"if he still has to ask what a sentence means"* — the order is met in the main with a residual the next piece should pay.

**Promise 6 (fun to drive, plain language) — kept, with one defect its own check caught.** The owner's word budget is intact at four (Shaped, Built, Judged, Live); filenames and never-owner-facing shorthand are exempt by the contract's own wording, so "dispatch proof" does not break the budget. It does break promise 6's other clause — *"This repository's own documents are held to the same bar; a reviewer who stumbles on our vocabulary files it as a defect"* — and R2 stumbled and filed it. That is promise 6's check firing exactly as designed, which is worth saying plainly: the promise caught its own violation.

**Promise 7 (small by law) — kept.** Every limit re-measured by me: 17 files ≤ 20 · 55,038 bytes ≤ 100 KB installed · always-read set (`AGENTS.md` + `state.md` + `product.md` + `map.md`) 22,285 bytes ≤ 50 KB · 5 skills ≤ 6 · this hearing's linked records = 4 ≤ 6. The v0.7 amendment paid the price the contract demands of any limit move — it names a compensating tightening (≤ 6 linked records per hearing, and a re-hearing extends records rather than opening files) and carries the owner's approval, verbatim in `decisions.md`. Legal.

**Promise 8 (it cannot quietly grow back) — kept, and this is the piece's strongest result.** 70,770 → 55,038 bytes, −15,732, −22.2%, verified by my own measurement. No new file, no new skill, no new capability. Every prior release "considered deleting" and deleted nothing; this one deleted, at scale, while conserving 177 numbered rules and landing five new sentences. This is the first time the kernel has shrunk.

### Good to use — **kept**

I lean on R1's lived read, which is the only lived read of the surface there is.

R1 named fifteen things executable cold with no second pass, and the ones it singled out are the load-bearing ones: the dispatcher, the definition of *ratified*, the small-change test, the harness rule, the four rulings held apart, "do not average them", and the check-must-be-able-to-fail rule. R1's line about `craft` — "the plainest file in the set. Every bullet names the failure it prevents" — is the shape the whole rewrite was aiming at, and it hit it there.

**The residual, and it is a real pattern, not a list of nits.** R1's own diagnosis: *"the plain rule lands, then a compressed war story on top of it costs the passes."* The three-pass sentences are both scars — the "no model here" foundation piece, and "Five rounds once perfected a truthful machine that missed its jobs." The rewrite compressed the scars harder than it compressed the rules, and compression cost more comprehension per byte on scars than anywhere else. That is a genuine fork with a real trade on both sides, and it goes to the owner rather than back to the builder.

R1 also found one thing it would call process for its own sake, and I agree it is the only one: `worst-day.md` asks the tester to audit the builder's git hygiene, including a staleness count with no threshold and no consequence — and assigns it to the persona whose entire value is that they are a user and not us. R1's phrase for it is exact: "process wearing the product's face."

### Quality hangs together — **not yet**

This is the ruling that routes the piece back, and it is not a ruling about the substance, which is high.

Three defects, each small, and together one shape:

1. **A correction that closed in one file and was reported as closed in six.** "dispatch proof" fixed in `AGENTS.md`, left standing in five skill files, claimed complete in both the build record and the receipt.
2. **Two pointers died while their rules survived.** `templates/` is now named nowhere in `AGENTS.md` — I confirmed it: only `templates/map.md`, `templates/rounds.md` and `templates/product.md` are reachable from any loaded file. `templates/piece.md`, `templates/state.md` and `templates/decisions.md` are unreachable. `piece.md` is the sharpest loss, because it carries the **entire receipt and judgment schema** — the concrete form of the method's heaviest mechanism — and `AGENTS.md:112` still says "Templates are starting floors, not limits" about a directory it never names. R2 found this by grep; R1 found the same hole by cold read (S17), from the opposite direction.
3. **A mechanical gate lost its locator.** M6's "in the shaped decks" is gone, inside a check the same sentence insists is run rather than asserted.

The shape: **the conservation instrument measured rules, and every one of this rewrite's failures was in something that is not a rule.** Pointers, term consistency, locators. The inventory's declared granularity — "one enforceable claim per line" — was coarser than the text's operative granularity, so a sub-clause could die inside an entry marked conserved, and a file could become unfindable without any entry noticing, because every entry asks whether a *rule* survived and none asks whether its *subject* is still reachable. That is the unenumerated-property law firing on the piece's own instrument, and it is the lesson the next rewrite should not relearn.

A rewrite whose defining claim is one consistent register cannot be ruled to hang together while it carries an undefined second name for its most load-bearing artifact at six sites, in the section heading of the very skill that outlaws undefined jargon.

---

## 6. The structure — **sound**

The prior ruling on this kernel was **straining**, with the strain named as growth: *"both benches ruled the growth STRAINING and point the next kernel piece at a subtraction pass with a numeric target"* (`decisions.md`, 2026-08-29). That ruling ordered structural repair as the next piece. This is that piece, and it executed.

**The named strain is relieved, measurably.** −22.2% of the installed surface, first shrink in the kernel's history, zero new files, zero new skills, 177 of 177 rules conserved, five sentences added inside the savings. A strain whose repair was ordered, performed, and measured is a strain relieved.

**The structure did not fight the rewrite.** Every rule moved registers without needing the old vocabulary to exist. Nine method words went to zero and nothing broke. That is evidence the method's substance and the method's jargon were separable — which was the bet, and it paid.

I considered ruling straining on the surviving undefined vocabulary and decided against it, for a reason I want on the record because the arithmetic matters. Two straining rulings in a row mechanically make the next piece structural work. The right next piece here is **defining six words and restoring three pointers** — content repair with a cheap, exact scope. Ruling straining would force a structural piece the evidence does not call for, and would spend the method's most expensive lever on a backlog rather than a structure. The residuals are content defects with named fixes, not a structure under load.

**Sound**, with one residual named for the record: the pages now carry six load-bearing terms that no page defines, five of them inherited and one (`dispatch proof`) newly created. Visible, cheap, and owed.

---

## 7. Ruling: **route back to build**

Not sufficient to land as v5.2.0 yet. This is a narrow, mechanical route-back, not a rejection — the rewrite's core claims all reproduced at my own hand, and the piece keeps the live slot.

The cost of this route-back is close to zero, because the piece could not land today regardless: the dev suite's green arm has not returned, and landing cannot be asked before that number is read back. The repairs fit inside the same window.

### Grounds, with the exact scenarios to re-run

**B1 — Remove the new coinage.** Replace "dispatch proof" / "dispatch-time proof" / "dispatch and review proof" with `receipt` at all six sites: `shape-product:16`, `map-build:35`, `experience:12`, `experience:25`, `judge:20` (the section heading), `worst-day:59`. Leave the ordinary verb forms alone — "the dispatch date and commit", "re-dispatch under its own named line", "the dispatching session" are plain English and self-describing.
*Pre-fix control, judge-executable:* `git grep -icE "dispatch[- ]?(time )?proof" <pre-fix-sha> -- AGENTS.md .claude/skills templates` → 6. Post-fix on the same expression → 0.
*Re-run scenario:* re-read `judge` §1 and `shape-product` cold and confirm the heading and the body now name the same thing, and that a reader meeting `receipt` at a phase exit can reach its definition.

**B2 — Restore the templates pointer.** Name `templates/` in `AGENTS.md`'s files section, and point the build loop at `templates/piece.md` where it tells a builder to commit a work file and open a receipt. About 50 bytes against 9,962 of headroom.
*Pre-fix control:* `grep -c "templates/" AGENTS.md` → 0; and `for t in templates/*.md; do grep -rq "templates/$t" AGENTS.md .claude/skills; done` → `decisions.md`, `piece.md`, `state.md` ORPHAN. Post-fix: all six reachable.
*Re-run scenario:* from `AGENTS.md` alone, reach the receipt schema without guessing a directory name.

**B3 — Restore M6's locator.** Say where captioned screen drawings live, so the completion test names a population a grep can find. The pre-rewrite text said "in the shaped decks"; any locator will do, but the gate must name its own population.
*Pre-fix control:* `git show 44a48ba:.claude/skills/map-build/SKILL.md | grep "shaped decks"` → 1 hit; current → 0.
*Re-run scenario:* R1's S2 — attempt to enumerate the population from the pages and report whether it is now findable.

**B4 — Correct the record.** The build record's *"replaced with the defined word receipt"* and the receipt's *"Convicted terms at zero across the surface"* are false against the committed text. Rewrite both to say what was true at `e5494cf` and what the fix changed. This is required regardless of B1–B3: the state law is claim nothing beyond the evidence.

**B5 — Record the measured prediction.** The work file must state, in these terms: (a) held · (b) failed as written, six terms against a target of zero, held against every term its baseline named · (c) the green arm's actual number when it returns. The piece committed to saying so either way.

**Sibling sweep before re-testing** (my own §"Re-run after fixes"): B1 is a term-consistency defect, so sweep for the same shape — any other place where the rewrite introduced a second name for a thing already named. B2 is a reachability defect, so sweep every path referenced in the loaded surface, not just `templates/`.

**Re-testing this fix batch** is cheap and does not need a full four-persona round: the changes are text, the controls are greps, and the scenarios above are named. One tester re-running B1–B3's controls plus one free skeptical attack of its own choosing, reported either way, and a judge re-reading the changed sentences, is proportionate. Under the amended promise 7, the re-hearing **extends** the existing records rather than opening new files.

**Nothing here re-enters shape or map.** The promises are right and the piece-space is right. This is a bad-build ground and it stays in build.

---

## 8. Owner questions

Each is self-contained and starts with what the choice changes for the people using this.

### Q1 — The war stories: keep them and pay a second read, or cut them and lose the reason?

**What it changes:** whether an agent reading these pages understands *why* a rule exists, at the cost of reading a few sentences twice.

The rewrite compressed the scars harder than it compressed the rules, and that is where every slow sentence turned out to be. The stranger read two of them three times: the "no model here" foundation piece, and "Five rounds once perfected a truthful machine that missed its jobs." Their surrounding rules were already complete without them.

One scar was cut entirely: *"One plain rendering once let the owner catch, in a single read, a violation that three separate fresh checking agents had all missed."* I confirmed it is gone from the whole surface. The rule it justified still stands — but unevidenced, and it is the rule that says explaining things plainly to you is a defense layer rather than politeness. That is the rule most likely to be traded away by a future agent who can no longer see what it cost. It is also your scar.

**Options.** (1) Keep the scars as they are — a second read on about four sentences, and the reasons stay attached. (2) Cut the compressed ones to their plain rule and move the stories into an archive the pages link to — faster reads, reasons one hop away. (3) Restore the plain-rendering scar specifically, cut the other two.
**Recommendation:** (3). The cut one is the one whose absence has teeth; the other two sit on rules that already stand alone.

### Q2 — Six words nothing defines: define them, or delete some of them?

**What it changes:** whether an agent building your product can tell what state its work is in, and whether a gate that claims to be mechanical actually is.

*Shaped* is one of four state words and nothing says what it means. *Live*'s condition is stated twice at two different altitudes, so a single piece and a whole milestone are licensed by the same sentence. *Care level* is something you are asked to set and never lower, with no scale to set it on. *Straining vs fighting* decides whether the map re-cuts now or two pieces from now, with no boundary between the words. *Screen drawing* is counted by a mechanical gate and produced by no step. *"Its own checks"* is the condition that produces every Built line and has no floor — write no checks and none fail.

Five of these predate this rewrite. It did not create them; it made them visible, which is how a stranger found all six in one read.

**Options.** (1) Define all six — one sentence each for four of them, real work for the last two. (2) Define four, and **delete** the other two: promise 8 says consider deleting first, and both are deletion candidates — does *Shaped* earn a slot in the ladder if nothing defines it, and does *captioned screen drawing* earn a row in a mechanical gate if no step produces one? (3) Leave them; they cost a careful reader nothing fatal.
**Recommendation:** (2). Four definitions and two deletions, in the next piece, after this one lands.

### Q3 — Should the user persona audit our own process?

**What it changes:** whether the one tester in the method who exists to *not* be us stays that way.

`worst-day.md` asks the worst-day tester — defined as the person facing weak permissions, a dying network and corrupt data — to run `git rev-list` and audit whether the builder followed the build loop. One of those git reads produces a number with no threshold and no consequence attached. The stranger called it the single clearest case of process for its own sake in the whole surface.

Promise 8 names this shape directly: if the kernel seems to need a compliance layer for itself, stop and subtract.

**Options.** (1) Move the git audit to the judge, where checking claims already belongs, and give the staleness count a threshold or drop it. (2) Delete the audit outright. (3) Keep it.
**Recommendation:** (1) — move it to the judge and drop the number that has no decision behind it.

---

## 9. What the next builder should not relearn

**A conservation inventory conserves what it enumerates, and this one enumerated rules.** Every defect this rewrite shipped was in something that is not a rule: a pointer to a file, a second name for a defined thing, a locator inside a gate. Each of the 177 entries asked "did this rule survive?" and none asked "is its subject still reachable, and is it still called by one name?" Two testers found the same hole from opposite ends — one by grep, one by reading cold — which is what decorrelation is for.

**So the next rewrite's inventory carries three columns, not one:** the rule · the path or artifact it points at · the one name it uses for each defined thing. Then a pointer death and a coinage are both mechanically checkable, and neither depends on someone noticing.

**And a correction applied to one file is not applied.** The coinage was correctly identified during the merge, fixed in `AGENTS.md`, never propagated to five skill files, and then written up as complete in two places. The fix and the claim about the fix were authored in the same pass by the same context. A grep is cheap; write the claim from the grep, not from the intent.

---

*Judgment 2 · Claude workflow agent · opus · 2026-08-29 · on `e5494cf` under receipt `647cd99`. Ruled blind to judgment 1; divergence between us is itself a finding, to be resolved on evidence and never on rank. Every ruling above is conditional as stated in §4(c) on the dev suite green arm, which had not returned when this was written.*
