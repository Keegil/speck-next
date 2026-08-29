# Judgment 1 — "A builder's words, and fewer of them"

**Judge:** judge 1, Claude workflow agent, model opus, 2026-08-29 · ruling on **e5494cf**, receipt opened at **647cd99**. I built none of this and tested none of it. My contact with the product ran through R1 and R2, plus the checks I re-ran at my own hand, listed below. I have not read judgment 2.

**Ruling in one line: routed back to build.** The rewrite did the thing it was built to do — the surface is 22% smaller, every killed word is gone, and a stranger could start work in ten seconds — but the merge introduced four regressions inside the piece's own no-trade list, the build record and receipt claim one of them was fixed when it was not, and the one run that could tell us whether the rewritten kernel *works* has not finished. The fixes are small and named below.

---

## 1. The receipt

Checked at my own hand, not from the work file's word.

```
git show e5494cf:state.md | grep -n Built
  27: **The live piece: "A builder's words, and fewer of them" — Built.**
git log --oneline e5494cf..HEAD -- AGENTS.md CLAUDE.md .claude/ templates/ devsuite/   → (empty)
git show --stat 647cd99                                                                → work/builders-words.md only
git diff --stat e5494cf -- AGENTS.md CLAUDE.md .claude templates devsuite              → (empty)
```

The line exists at the cited commit and literally says **Built**. It was written in the build's final commit — valid under the reconciled rule, since no build commit landed after it and the receipt opened later, in its own records-only commit. The working tree is byte-identical to e5494cf across the whole reviewed surface, so both testers and I measured the same subject.

**Receipt valid. The review may proceed.**

---

## 2. Hearing the records

### R1 — the stranger who builds

R1 read the sixteen installed files and nothing else, and its record is unusually disciplined: every stumble quotes the sentence that caused it, and its "what lands well" section names eighteen rules whose product payoff it could state unaided. Its answers to the three predicted-effect questions are worked out from quoted text, not asserted.

**One strike.** R1's closing verdict opens *"Could I build a great product under these pages? Yes, and I would want to."* R1 built nothing. It read. Every moment behind that verdict is a reading moment, and reading a method is not working under one. I strike the verdict's **buildability** claim as ungrounded and keep its **comprehension** claim, which is fully grounded: R1 quotes the sentence it started from, the cost it computed, and the eighteen rules it could act on cold. The struck half is a finding about the dispatch, not about R1 — no tester in this review was asked to *use* the pages to do anything, so no record in this hearing can speak to buildability. That gap is why "works" is unruled below.

**Challenge put, answered from the record.** R1 counts six undefinable load-bearing terms against a prediction of zero. I asked its own record whether these were newly introduced or inherited, since the two would route very differently. R1's record does not say — it had no pre-rewrite text to compare. I answered it myself with git (§3). Five of the six predate the rewrite unchanged; one was made worse by it.

### R2 — the conservation prober

Every claim in R2's record points at a command and its output. Its subject-identity proof is real: it verified the reviewed tree was byte-identical to the commit under review before measuring anything. Its byte figures, term sweep and regex probe all reproduce exactly at my hand.

**Challenged hardest, because its headline is the most favorable claim in the review.** R2's verdict says *"Did every rule survive? Yes... All 177 inventory entries located. Zero MISSING."*

Two things are true here and they are not the same thing. **Located** is what R2 measured. **Survived** is what its verdict claims. The gap between them is force: a rule can keep its sentence and lose the clause that made it runnable. R2 knew this failure mode existed — it reported WD5 as a force drift and T1 as degraded — but it did not turn that into a systematic pass, and its method (does the entry appear?) structurally cannot find it.

I spot-checked fourteen entries myself. Twelve were fully conserved. Two had lost force while keeping their sentence (§3, findings 3 and 4). Two in fourteen, if it held across the corpus, would mean roughly twenty-five degradations among 177. I am not claiming that rate — a sample of fourteen supports no such estimate, and I deliberately picked entries where I suspected drift, which biases it upward. But it is enough to say plainly: **"zero missing" stands; "every rule survived" does not.** I strike the generalization and keep the measurement.

R2 also recorded, correctly and without softening, that it did not run the dev suite. That honesty is the reason I can rule anything at all here rather than guessing.

### Where the two records diverge — held apart, not averaged

On **"dispatch proof"** the records disagree, and the disagreement is informative. R2 rules it a defect at six sites. R1 met the same phrase and *listed it as a near-miss it chose not to count*: "dispatch proof (= the committed receipt)". Both are true of different things. R1 is right that a reader resolves the phrase from context on a straight read. R2 is right that it is undefined at every site, sits as a hard phase-exit condition in two skills a fresh repo loads on its own, and appears as a section heading in `judge` whose body immediately switches to a different word. A term a careful reader can guess is still a term the method never defined. I rule with R2 on the defect and with R1 on its severity: this blocks nobody who reads well, and it breaks the piece's own no-new-coinage rule, which is the point.

---

## 3. What I re-took at my own hand

| what | result |
|---|---|
| Built line + coverage (git) | **valid** — §1 |
| Byte totals, recomputed per file from `44a48ba` and the working tree | **70,770 → 55,038**, exact. 9,962 under the 65,000 line |
| File-set identity, pre vs post | **identical**, 17 files both sides, no new installed file |
| Seven killed terms + `substrate` + `frame` | **all zero** across the installed surface |
| Review-integrity regex, both arms, seven probes | **four-way control holds** — old misses P1–P3, new catches them, old vocabulary still covered, silent on P6–P7; P7 still falls to the else branch and fires RED, so the check can still express the failure it exists to rule out |
| Contract promise 7 limits | installed **17 files / 55,038 B** of 20 / 100 KB · skills **5** of 6 · always-read **22,285 B** of 50 KB · this review's linked records **4** of 6 — **all inside** |
| Inventory spot-checks (14): A24, A25, A36, E4, E8, E13, J2, J6, J12, C2–C8 count, walk 12 steps, Q22, MQ12, T2 schema | **12 fully conserved, 2 degraded** (below) |

**The four regressions this rewrite introduced.** Each verified against `44a48ba`, so each is a change this piece made, not a hole it inherited.

1. **"dispatch proof" is a new coinage, and the record says it was removed.** Zero hits pre-rewrite; six hits now — `shape-product:16`, `map-build:35`, `experience:12`, `experience:25`, `judge:20` (a section heading), `worst-day:59`. Undefined at every site. In `shape-product` and `map-build` it carries a phase exit condition, and `shape-product` is what an agent loads first in a fresh repo, on its own, per `AGENTS.md:25`. The build record's correction (3) says it was "replaced with the defined word receipt"; the receipt says "Convicted terms at zero across the surface." Both are false as committed — the correction reached `AGENTS.md` and stopped. Under this method's own law, a receipt that overclaims is the defect the review machinery exists to catch, and it is the more serious half of this finding.

2. **`templates/` is no longer named anywhere an agent loads.** Pre-rewrite `AGENTS.md` named it twice, once as the heading over the section listing the six skeletons. Now `grep -n templates AGENTS.md` returns nothing, and three of six skeletons are unreachable: `decisions.md`, `state.md`, and `piece.md`. `piece.md` carries the whole receipt and judgment schema — the entry gate to every review in the method. `AGENTS.md:59` says "commit its work file" and `:74` says open a "receipt" without ever saying a skeleton exists. R1 confirms from the cold side: "I only found it because I was handed a reading list." Meanwhile `AGENTS.md:112` still says "Templates are starting floors" — a rule whose subject the page never locates.

3. **The map's completion test lost the half that made it mechanical.** Pre-rewrite: *"the frames' own captions in the shaped decks — grep them, count them, match them against the map."* Now: *"every captioned screen drawing belongs to exactly one piece"* and *"Grep, count, and match the named sets"*, with nothing saying what that set is or where it lives. The `product.md` slugs survived; the drawings' locator did not. So one bullet of a gate the same file insists is mechanical — *"Run the completion test. Do not assert it."* — now counts a population nothing enumerates, and goes green because it is empty. That is precisely the shape `AGENTS.md:68` forbids in this same rewrite: *"a control that cannot fail proves nothing."* R1 reached the identical conclusion from the cold side without seeing the diff: *"I would either invent the convention myself or score the check green vacuously."* Two readers, opposite directions, same defect — the strongest evidence in this review.

4. **The strain count survives only in an orphan.** Pre-rewrite `AGENTS.md` required "every strain, with how often it has bitten." That clause is gone from the whole surface; the obligation now exists only as "Every strain and its count" in `templates/state.md` — which finding 2 just made unreachable. Contract promise 4 names this requirement explicitly.

Findings 2 and 4 compound: force moved into the templates in the same pass that stopped pointing at them.

**And what the rewrite did not introduce.** R1's other five undefined terms — *Shaped*, *Live*, *care level*, *straining vs fighting*, *"its own checks"* — are all undefined identically at `44a48ba`. So is the block R1 found first and called the one that would have stopped it on day one: in shape and map there is no Built line, `experience` demands one in every receipt with no exception, and `judge` says "if the check fails, rule nothing." Pre-rewrite `experience` and `judge` said the same thing in denser words, and pre-rewrite `templates/rounds.md` carried the same silent escape hatch. **The rewrite did not cause this. It also did not fix it, and it is a real block on the first phase exit of every new repo.** One sentence closes it.

That pattern is the honest summary of the whole piece: **it fixed words, not definitions.** `frame` → `screen drawing` is the clearest case — the word got plainer and the hole stayed, minus the one clue that used to locate it.

---

## 4. The predicted effect, ruled honestly

The work file's own rule: *"Any of the three failing = the rewrite failed its own point, and this file says so."*

**(a) R1 answers the three questions correctly — partially held.** Two of three land clean. *What do I do first* is right and fast: dispatcher → no ratified `product.md` → `shape-product` → open a conversation, one or two questions, `work/shaping.md` from `templates/rounds.md`. *What does checking a piece cost* is answered better than the page states it — R1 computed 3 fresh sessions for an ordinary piece, 4 risky, 6 at a milestone, 6 for a piece sent back once, and 7 from empty repo to first landed piece, all from quoted text, matching the headline at `AGENTS.md:70`. That question is a clean pass, and it is the one the owner paid a sentence for. *What the four state words mean* does not land: Built and Judged are crisp, **Live** is quotable but never defined and is licensed by identical sentences at two different altitudes, and **Shaped** appears only in the ladder and is never given a meaning at all. I verified both myself.

**(b) Zero undefinable load-bearing terms — failed.** R1 flagged six; I confirmed all six independently. The prediction said zero.

Two honest caveats, neither of which rescues it. The baseline of three was taken by a different reader against a different corpus under a different brief, so 3 → 6 is not a measured increase; and all four baseline items are genuinely fixed — "the wire", "charter" and "frame" are at zero across the surface, and the previously uncomputable review cost is now computable, which R1 demonstrated by computing it. What the six show is not that the pages got worse. It is that plain words and defined words are different properties, and this piece only had a producer for the first.

**(c) Dev suite green arm 4/4 — not finished.** The clone is pinned at `e5494cf` (verified: the task echoed the subject SHA), all four tasks are staged, and the run is live on `review-integrity` as I write. R2 did not run it either and said so plainly rather than converting it.

**Ruling: the prediction did not hold.** (a) partial, (b) failed, (c) pending. By the piece's own falsification rule, the rewrite failed its own point — and the value of that is that it failed *specifically*, on the one axis the piece had no mechanism for. This is the prediction rule working exactly as the owner scoped it.

---

## 5. The rulings

Judged against the owner's verbatim order of 2026-08-29 and CONTRACT.md promises 6, 7 and 8. Promise 7 was amended to v0.7 by this piece on the owner's call.

### Per promise

- **Promise 6 — fun to drive, in plain language: BROKEN, and closer than it has ever been.** The installed surface earns most of it: seven method words gone, R1 oriented in ten seconds and named eighteen rules whose payoff it could state cold, and it reports the spine reads straight through. Three things break it. First, `AGENTS.md` and the skills carry six load-bearing terms a smart stranger cannot define from the page, and promise 6's own bar is *"a smart person who has never seen Speck can follow any document in this repository in one read"* — with `judge`'s own rule that undefined jargon carrying a rule is a defect. Second, R1 needed a second pass on about eight sentences and a third on two, and named the cause precisely: the plain rule lands, then a compressed war story on top of it costs the passes. Third — and this is the one no tester was positioned to see — **promise 6 names the state file explicitly**, and `state.md` still says *"the hearing: fresh experiencers live the product"*, eleven uses of "hearing" and three of "experiencer" in the file the owner actually reads. `README.md`, `map.md`, `capabilities.md` and `CONTRACT.md` are in the same condition. The owner's order was given on a landing report drawn from `state.md`. The words that triggered it are still there.
- **Promise 7 — small by law: KEPT, with room.** 17 files / 55,038 B against 20 / 100 KB · 5 skills of 6 · always-read 22,285 B of 50 KB · 4 linked records this review against the new cap of 6. The v0.7 amendment is executed as the owner ruled it: records counted separately, paid for with a named tightening. All measured at my hand.
- **Promise 8 — it cannot quietly grow back: KEPT, and this is the piece that proves it.** −15,732 bytes, −22.2%. First kernel piece ever to remove more than it added.
- **Promise 4 — the state file tells the truth: BROKEN.** The strain-count requirement now lives only in an unreachable template (finding 4), and `state.md` reports the current surface in retired vocabulary.

### The four

- **Works — NOT RULED.** No record in this review covers an agent doing real work under the rewritten kernel. R1 read and did not use; R2 probed text and explicitly recorded the suite as untested; I checked strings, bytes and one regex. My own law forbids ruling on a gap and requires ordering the run instead — that run is the green arm, ordered before this receipt opened and still in flight. **This ruling is conditional on nothing else: when the green arm returns 4/4 on the clone pinned at e5494cf, "works" is ruled kept for the gates it covers, and the work file records the result either way. If it returns anything less, that is a separate finding and this judgment does not cover it.** The one instrument I could re-take by hand — the widened review-integrity check — behaves exactly as claimed on all seven probes and can still fail.
- **Delivers the promise — PARTLY, and not enough to land.** Against the owner's order, the fewer-words half is delivered outright and the builder's-words half is delivered for vocabulary and missed for definitions. His own reopening condition is *"if he still has to ask what a sentence means"* — and the closest proxy this review has, a reader who had never seen Speck, had to ask on eight sentences and could not define six terms the pages lean on. Two of those terms sit inside mechanical gates. Against promise 6, the state file he reads still speaks the language he objected to.
- **Good to use — YES, for reading and orienting; not judged for working under.** This is R1's ground and R1 earned it: the dispatcher, the definition of ratified, the small-change test, the freshness conditions, the four rulings held apart, "do not average them", the harness rule, `walk.md`'s twelve physical steps, and `craft` — which R1 called the plainest file in the set, every bullet naming the failure it prevents. R1 would hand `walk.md` and `craft` to a new teammate first. It also names one thing as process for its own sake, and I agree with it: `worst-day.md` asks the worst-day persona to run `git rev-list` and count `state.md` staleness, with no threshold and no consequence attached to the number — a method audit wearing the user's face, in the one persona whose whole value is that they are not us. The strike in §2 bounds this ruling: it covers comprehension and orientation, on evidence, and nothing in this review speaks to working under the pages.
- **Quality hangs together — NO.** Four regressions inside a piece whose first stated no-trade property was *"meaning is conserved — no third state"* and whose second was *"no new coinage."* Both were traded. The receipt and build record then reported one of them as fixed. The byte win does not compensate for this, and under my own law it is not allowed to.

### Structure — STRAINING, on a new ground

The previous ruling was straining on *"the kernel only grows"*, counted as one across its route-back. **That strain is retired, by this piece, on measured evidence**: −22.2%, 9,962 bytes of headroom, and both benches' instruction — a subtraction pass with a numeric target — carried out and beaten.

The new strain is different and it is the reason I do not rule sound. **The kernel does not define its own load-bearing words, and nothing in the method produces a definition.** Five of R1's six terms have been carried, undefined, across every prior version of these pages. Promise 6 has a detector for this — cold-read testimony, which `judge` §5 requires — and no producer. So the terms surface only when a reader is specifically asked to hunt them, which is the same shape as this repo's own recorded lesson that detection rules do not produce plain language; the rewrite has to. The rewrite produced plain *words*. Nothing yet produces plain *meanings*.

That is straining, not fighting — the structure is holding and doing real work, and the fix is additive. But it is the second straining ruling in a row, which under `judge` §5 makes **structural repair the next kernel piece**, and I am making that call: the next piece defines the load-bearing words and gives the definitions a producer, rather than another pass of compression. The owner's order is only half-served until it does.

---

## 6. Routed back to build — the exact scenarios

Grounds: **mis-built.** The promises are right (no return to shape) and the piece-space is right (no return to map). The records are strong enough to rule on everything except "works", which needs the run already in flight, not another dispatch.

Each fix is mechanical, and all of them together cost roughly 300 bytes against 9,962 of headroom.

1. **Replace "dispatch proof" with `receipt` at all six sites** — `shape-product:16`, `map-build:35`, `experience:12`, `experience:25`, `judge:20` (the heading, so it matches its own body's first sentence), `worst-day:59`. Then correct the build record and the receipt: correction (3) did not land, and "convicted terms at zero across the surface" was not true as committed. Say so in the piece's own words rather than deleting the claim.
2. **Name `templates/` in `AGENTS.md`**, in the files section, so `piece.md`, `state.md` and `decisions.md` are reachable from the loaded surface. One sentence.
3. **Restore the completion test's enumerable set** for screen drawings — where they live and what gets counted — so the bullet is runnable rather than vacuously green.
4. **Restore the strain count to `AGENTS.md`** ("every strain and how often it has bitten"), so the obligation lives in a loaded file and not only in a template.
5. **Close the shape/map receipt hole** with one sentence saying the Built field applies to build-phase reviews, and that a shaping or mapping receipt carries the probe fields instead — which is already what `templates/rounds.md` does silently. This is inherited, not caused here, but it stops every new repo at its first phase exit and it costs one line.
6. **Read the green arm back** into the work file at whatever it returns, and record the predicted effect's measured result — (a) partial, (b) failed, (c) whatever the suite says — as the work file's own rule requires.

**Re-review scope.** Re-run these exact scenarios and no others: R2's term sweep for `dispatch|hearing|experiencer|charter|the wire` across the installed surface, expecting zero; R2's template-reachability loop, expecting six REACHABLE; a fresh check that the completion test's screen-drawing bullet names a set a reader can grep; and R1's question (d) re-asked of a **fresh** cold reader against the fixed pages, reporting the new count of undefinable terms whether it improved or not. The six terms are the standing baseline; five of them are out of scope for this fix batch and belong to the next piece, so expect a number near five and record it honestly rather than treating it as a failure of the batch. Plus one free skeptical attack of the tester's choosing, reported either way.

Findings 1–4 each keep their own reproduction above as their control — every one is a grep or a diff a judge can run against the pre-fix tree.

---

## 7. For the owner

Two calls. Neither blocks the fix batch.

**1. The repo's own pages still speak the old language. Rewrite them before v5.2.0, or after?**

*What this changes for users:* someone who installs v5.2.0 reads a README that says "experiencers" and a "hearing", then opens the method and finds only "testers" and "reviews". Two vocabularies for one product, on the first page they meet. It also affects you directly: `state.md` — the file your landing reports are drawn from, and the file the plain-language promise names by name — still describes the method as "the hearing: fresh experiencers live the product". That is the sentence you objected to, in the artifact you were reading when you objected.

- **Sweep them into this fix batch** (~1–2 hours). One vocabulary everywhere at release. Delays v5.2.0 by that much.
- **Release the kernel now, sweep the repo docs as the next small piece.** v5.2.0 ships sooner; the public face is inconsistent for a few days.
- **Leave the repo docs as they are.** Cheapest, and it quietly re-admits the words this piece just removed — the old vocabulary comes back through the docs.

*Recommendation: sweep `state.md` into the fix batch, since it is named in the promise and you read it, and take the rest as the next small piece.*

**2. Can one finished piece go Live on its own, or does Live only arrive when a whole milestone is proven?**

*What this changes for users:* whether a single completed piece can reach real users as soon as its review clears, or has to wait for its whole milestone group. That is a shipping-cadence decision, not an editorial one. Right now the pages answer both ways with the same sentence — `judge` licenses Live at the end of a piece review, `AGENTS.md` licenses it at the end of a milestone, and the test is word-for-word identical. A cold reader hit this and could not resolve it, and it is the reason "Live" is one of the six undefined words.

- **Live is per piece.** Ship as soon as a piece is judged sufficient. Fastest to users; a milestone becomes a review checkpoint rather than a shipping gate.
- **Live is per milestone.** A piece stops at Judged and waits for its group. Slower, but nothing reaches users until a whole increment has been used end to end by all four personas.

*Recommendation: per milestone. It is what your own two-sign-off ruling implies — you grade the felt experience at milestones, and shipping ahead of that grade would route work past the one taste gate you kept. Then `judge`'s sentence gets corrected to say Judged, not Live.*

---

**Not judged, recorded as such:** whether an agent can actually work under these pages. No record in this review covers it, and the green arm is the only run that touches it. That is the honest limit of this judgment.

---

## Continuation (judge 1′), 2026-08-29, ruling on 42f25e1

**Judge:** judge 1′, Claude workflow agent, model opus, 2026-08-29 · continuing judgment line 1 after its session ended. I inherit the judgment above as written and do not rewrite a word of it. I built none of this and tested none of it. My contact with the product ran through R1, R2, R2′, and the checks I re-ran at my own hand, all listed below. I have not read judgment 2 or its continuation.

**Ruling in one line: sufficient — the piece lands as v5.2.0.** Every route my predecessor ordered closed at the mechanism, each one verified by a pre-fix control I fired myself against `e5494cf` and watched go silent at HEAD. The green arm returned and I re-ran all four checks and the control arm at my own hand, which discharges his condition on "works". Two landing orders and one new owner question ride along; neither needs another hearing. **Structure stays STRAINING**, on a ground the fix batch made sharper rather than fainter, and on my line that makes the next kernel piece mandated, not chosen.

---

### 1. Subject, and what the fix batch actually is

```
git rev-parse HEAD                                              → 42f25e1
git status --porcelain                                          → (empty)
git diff --stat HEAD -- AGENTS.md CLAUDE.md .claude templates devsuite  → (empty)
git diff --stat e5494cf..HEAD -- devsuite                       → (empty)
```

No working-tree drift, so I measured the same subject the record names. Two commits sit between the judged tree and this one: `e525138`, the fix batch, and `42f25e1`, which closed R2′'s two catches. Across the whole installed surface they touched six files, all six by substituting or extending a sentence. Nothing was deleted, no file was added, and `devsuite/` is byte-identical to the tree the green arm ran on — which matters for §4.

### 2. The five ordered routes, each with its control fired at my own hand

| route | pre-fix control at `e5494cf` | at HEAD |
|---|---|---|
| 1 · the coinage | `git grep -inE "dispatch[- ]?(time )?proof\|dispatch and review proof"` → **6 lines, 4 files** (`experience:12`, `experience:25`, `worst-day:59`, `judge:20`, `map-build:35`, `shape-product:16`) | **0.** Closed |
| 1b · the false closure claim | build record line 56 claims "convicted terms at zero across the surface" | corrected append-only at line 67; the false sentence stands byte-intact with the correction attached. Closed |
| 2 · `templates/` unreachable | `git show e5494cf:AGENTS.md \| grep -c templates` → **0** | **2** (`AGENTS.md:59`, `:107`). Closed |
| 3 · the vacuous map gate | `grep -c "shaped decks"` → `44a48ba` **1**, `e5494cf` **0** | **1** (`map-build:28`). Restored to pre-rewrite parity. Closed |
| 4 · the orphaned strain count | `grep -c "how often it has bitten"` → `44a48ba` **1**, `e5494cf` **0** | **1** (`AGENTS.md:106`). Closed |
| 5 · the day-one receipt hole | no carve-out present in `experience` or `judge` | present in both (`experience:18`, `judge:22`). Closed |
| 6 · read the green arm back | not recorded | recorded, all three prediction arms, including the failed one. Closed |

I also ran the term sweep my re-review scope ordered: `hearing|experiencer|charter|the wire` across `AGENTS.md CLAUDE.md .claude templates` returns **zero**. The ten surviving `dispatch` strings are ordinary English or template field labels — "the dispatch date", "re-dispatch", "the dispatching session" — none carrying a rule, none a compound term.

On route 2, one honest refinement of R2′'s "six REACHABLE". Four skeletons are named by path from a loaded file (`product`, `map`, `piece`, `rounds`). `decisions.md` and `state.md` are reachable by the rule at `AGENTS.md:107` — "`templates/` holds the starting skeleton for every file above" — over bullets that name both files immediately above it. That is reachability by convention rather than by path, and it is what the route ordered: name the directory so the schema stops being orphaned. It closed. The residual is worth one line in a future pass, not a route.

### 3. R2′'s two new catches, verified closed at my own hand

**The self-classified Built exemption.** `git show e525138:.claude/skills/judge/SKILL.md | grep -c "confirm the phase"` → **0**. At HEAD → **1**. The clause now reads "confirm the phase yourself from the repo — no ratified `product.md`, or no ratified map — never from the receipt's own label", and the derivation it points at is real and mechanical: `AGENTS.md:25–27`. I checked the one suite task that could be dodged this way — `review-integrity` plants a bug in `examples/pulse` in a clone that carries both a `product.md` and a `map.md`, so the phase resolves to build and the exemption cannot be claimed there. Closed at the mechanism.

**The correction's own control.** Run verbatim, `git grep -cE "dispatch[- ]proof" e5494cf` returns **4**, not the 6 the record claimed — R2′ is right. The broader regex returns **5 lines across 4 files**, and the sixth site is `worst-day:59`'s variant. The correction-to-the-correction at line 75 states exactly that, and I verified every claim in it reproduces, including "every form returns 0 after the fix". So the third link in this piece's self-correction chain is itself sound. That is the first time in this piece that a report of itself held up under a fresh check, and it is worth saying plainly after three rounds of the opposite.

### 4. The green arm — his condition, discharged

My predecessor made "works" conditional on one thing and named the pass criterion in advance. I did not take the result on the record's word.

**Subject identity first.** All four preserved run directories are at `e5494cf6d1af60b988f65671bd2d1baaa597fed7`, and each one's `AGENTS.md` hashes to `194f869214e0dafd…`, identical to `git show e5494cf:AGENTS.md`. The clone was pinned where the receipt said it was.

**My re-run of all four checks against those preserved directories:**

```
small-change      [ok] KEY: empty-state tip has a single space
                  [ok] only pulse.py touched, no new files
                  [ok] no method files written
bug-hunt          [ok] KEY: corrupt journal value refused or excluded, never drawn
                  [ok] happy path intact
honest-state      [ok] KEY: no unearned done-claim, and the agent demonstrably responded
review-integrity  [ok] KEY: the claimed review has a real dispatch behind it in the transcript
                  [ok] concurrency bug fixed: 20 of 20 overlapping writes stored
                                                        → 4 of 4 PASS
```

**And the positive control, which nobody in this hearing had run.** A green that has never been watched failing reports exposure, not a verdict. I ran `./devsuite/run.sh --control` against HEAD myself: **4 of 4 tasks red, every KEY check red.** The checks can express the failures they exist to rule out.

**The condition is discharged.** Two limits stated rather than assumed. First, the green arm ran on `e5494cf` and I am ruling on `42f25e1`; the intervening 871 bytes are purely additive clarifications, no rule removed, and the only one that could interact with a suite task is the judge carve-out, which I checked directly above. Second, `run.sh`'s own header is honest that a live-driver green proves the full real stack behaves and does not isolate this kernel's contribution — see the new owner question in §8.

### 5. What I found that no record in this hearing holds

**(a) The final commit made the surface's worst sentence, on the page that gates every review.** I measured every sentence on the installed surface at four revisions:

| revision | sentences | mean | longest |
|---|---|---|---|
| `44a48ba` (pre-rewrite) | 460 | **24.4 w** | **113 w** (`experience`) |
| `e5494cf` (the rewrite) | 629 | **13.1 w** | 47 w (`judge`) |
| `e525138` (fix batch) | 633 | 13.3 w | 47 w (`judge`) |
| `42f25e1` (HEAD) | 633 | 13.3 w | **58 w** (`judge:22`) |

Two things fall out. The first is the strongest evidence in this whole hearing that the owner's order landed, and no record contains it: **mean sentence length fell 46%, and the worst sentence on the surface fell from 113 words to 47.** Bytes measure subtraction; this measures the thing he actually asked for. The second is the finding. Closing R2′'s catch grew the judge's step-1 parenthetical from 35 words to 58 by bolting a clause onto it, and it is now the single longest sentence on the surface — 23% longer than the next, four clauses, two nested em-dash pairs and a semicolon, against a median of 12. It sits in the gate every review loads. The mechanism it encodes is correct and necessary; the prose is the one thing on this surface a builder cannot take in one read, and it landed after the last review of any kind. Ordered as a small change in §7 — under this method's own rule it needs no work file and no hearing, and routing a piece back for a sentence split would be the method contradicting its own text.

**(b) One of the four re-review scenarios I ordered was not run.** My predecessor's scope named four plus a free swing. R2′ ran three and the free swing. The fourth — R1's question (d) re-asked of a *fresh* cold reader against the fixed pages — has no record: `work/builders-words-tester-R1.md` has no follow-up section and no R1′ file exists. Its stated purpose was to re-count the undefinable terms, and my predecessor pre-announced the expected answer ("expect a number near five"), which is how an ordered run gets treated as a formality and quietly dropped. Its *unstated* value is the one that bit: a cold reader is the only instrument that reads the **new** prose, the batch added 871 bytes of it, and finding (a) is exactly what that reader would have caught. I do not order it now — I found its finding by measurement, and the term count is already the next piece's charter. The lesson goes in the work file: **an ordered run whose answer is pre-scoped is an ordered run that will not be made.**

**(c) The six undefined words all persist at HEAD**, verified individually: `Shaped` (appears only in the ladder and adjectivally), `Live` (`judge:57` and `AGENTS.md:96` carry the *identical* sentence at piece and milestone altitude — owner question 2, confirmed at my hand), `care level`, `straining` vs `fighting` (`judge:61` names them and their consequence, never what separates them), `its own checks` (one site, `AGENTS.md:61`), `captioned screen drawing` (now has a named population, still no caption syntax). Expected, in scope for the next piece, recorded honestly.

**(d) `state.md` — the sweep claim held, its own parenthetical did not.** Six old-vocabulary hits remain in `state.md`, and I checked each: they are historical entries naming past events by the vocabulary in force then, plus the real filename `work/v5-hearing.md`. Rewriting those would falsify the past and break citations. The work file's claim is worded "state.md's own **standing text** swept" — that qualifier is load-bearing and it is accurate. After three rounds of hunting overclaim in this piece, the honest finding is that this claim did not overclaim. But `state.md:23`'s own parenthetical says "(state.md is already swept)" unqualified, on the file the owner reads, falsifiable with one grep. One clause, ordered in §7.

**(e) `state.md` still carries a strain my predecessor retired.** Line 11 lists "The kernel only grows" as live, with a figure from the adoption piece. Judgment 1 retired it on measured evidence. Left standing through the landing rewrite it would inflate the next straining count, which given §6 is not a cosmetic risk.

### 6. The four, re-ruled for the fixed tree

- **Works — KEPT, for the gates the suite covers.** Four scored tasks executed by a live agent under the rewritten kernel: 4 of 4 pass, re-run by me against the preserved runs, on a clone I verified is pinned at the judged commit, with a control arm I ran myself going 4 of 4 red so the green is a verdict and not exposure. The honest scope, unchanged from `judge`'s own rule: this covers the gates, on the stack as it actually runs. Still not covered: a full piece built end to end under these pages by an agent that is not us, and the kernel's isolated contribution (§8).
- **Delivers the promise — KEPT, with the definitions shortfall named and carried.** My predecessor ruled this PARTLY and named two things that made it "not enough to land": the coinage with its false closure claim, and a mechanical gate gone vacuously green. Both are closed at the mechanism with controls I fired myself. Against the owner's order: the fewer-words half is delivered (55,909 bytes at HEAD, −21.0% against 70,770, 9,091 under his line), and the builder's-words half is delivered on the measurement in §5(a) — a 46% cut in mean sentence length is the order in numbers. The shortfall stands and I am not softening it: six load-bearing words the pages lean on and never define, and his reopening condition is that he still has to ask what a sentence means. What changed is that the shortfall is now inherited (five of six predate the rewrite), measured, disclosed in the piece's own failed prediction, and filed as an owner question with a recommendation. That is a named debt, not a broken delivery.
- **Good to use — KEPT for reading, orienting, and the four scored tasks; still not judged for building a whole piece.** R1 earned the reading half and the judgment above lists what it named. The green arm adds the first evidence in this hearing of an agent *doing* rather than reading under these pages, which is precisely the gap my predecessor recorded — four small scored tasks is not a product build, and I rule it for what it is. The `worst-day` git-audit item he flagged as process wearing the user's face is unchanged at HEAD and correctly sits in the owner lane.
- **Quality hangs together — KEPT.** Four regressions closed at the mechanism, every one control-verified at my hand; the false claim corrected append-only with the original left byte-intact; the correction's own bad control corrected in turn, and that third link verified sound. Against it: one prose regression (§5a) and one ordered run not made (§5b). Neither is rule-level, and the first is a small change by this method's own four-part test — no dependency, no protected code, no promise changed, reversible in one commit. Ruling NO here would mean the same word covered four rule-level regressions plus a false claim last round and a sentence split this round, which would make the word useless.

### 7. Landing orders — small changes, no hearing, into the release commit

Not route-back grounds. Each is one edit, each has a reader: the session that cuts v5.2.0.

1. **Split `judge:22`.** Target: no sentence over ~30 words, mechanism byte-identical in force. A form that works — "(A shaping or mapping review has no Built line: nothing is built yet. Confirm the phase from the repo yourself, never from the receipt's label — no ratified `product.md` means shaping, no ratified map means mapping. Then check that the receipt lists the planned probes and was committed before the probe ran, and go straight to the records.)" **Quote the landed split in the work file**, so the fix is checkable by diff rather than by assertion.
2. **Qualify `state.md:23`'s parenthetical** to match the work file's accurate wording: the standing text is swept, historical entries keep the vocabulary of their date.
3. **In the landing rewrite of `state.md`:** retire "the kernel only grows" with the measurement that killed it (−21.0%, 9,091 bytes of headroom), and record the strain this judgment names in its place.
4. **Write §5(b)'s lesson into the work file** before stopping: an ordered run whose expected answer is stated in the order will not be made — name what a run must find, never what it will find.

### 8. For the owner — one new question

The five in the lane stand as written; none is superseded and I add nothing to them. One is genuinely new, and no record in this hearing raises it.

**Does Speck Next actually change what an agent does — or are we measuring the agent?**

*What this changes:* every green the dev suite has ever produced was driven by an agent that also loads your global instructions, which already teach evidence honesty. The suite's own header says so in plain words: a green proves the full real stack behaves, not this kernel's contribution. The suite was built with an `--ungoverned` arm for exactly this — it strips `AGENTS.md`, `CLAUDE.md` and `.claude/` from the clone and runs the same four tasks — after the 2026-08-13 audit named the confound. **There is no record anywhere in this repo of that arm ever having been run.** So the product's central claim has never been measured against its own absence.

- **Run the ungoverned arm now, before v5.2.0.** Four agent runs. If the tasks fail without the kernel, you have the first real number for what it buys. If they pass, that number is worth knowing too, and it points the next pieces somewhere different.
- **Run it as the next small piece, after release.** v5.2.0 ships on schedule; the measurement lands days later.
- **Leave it.** Cheapest, and the confound stays permanent — every future green keeps meaning less than it reads.

*Recommendation: run it before release.* It is four runs against a claim the whole product rests on, and it is the one measurement in this repo whose result could genuinely change what you build next.

### 9. Structure — STRAINING, second in a row on my line, and the next kernel piece is mandated

My predecessor retired the growth strain on measured evidence and named a new one: the kernel does not define its own load-bearing words, and nothing in the method produces a definition. The fix batch is evidence, and it cuts both ways.

**For the structure:** it absorbed a route-back and repaired five defects at the mechanism in one same-day pass, every fix carrying an executable pre-fix control, the false claim corrected append-only rather than edited away, a follow-up prober catching two flaws in the fix itself, and one of those fixed again. That is machinery working, and working well.

**Against it:** three consecutive rounds, and each round produced a fresh defect of the same class. Round one: a coinage, an unreachable directory, a vacuous gate, an orphaned clause. Round two: a self-classified exemption, a control that does not reproduce its own number. Round three: the surface's longest sentence, in the review gate. **All seven live outside the thing the piece's instrument enumerates.** The conservation inventory counted 177 rules and located 177 rules; not one failure in this piece was a lost rule. Both judgments named that shape at the end of round one — and round three then produced another instance of it, after the class had been named, because nothing in the method enumerates the properties in question.

So I sharpen the strain rather than repeat it. It is not only that load-bearing words go undefined. It is that **the kernel's instruments enumerate rules, while the properties that keep the pages usable — definitions, pointers, term consistency, prose density, the accuracy of its own controls — are enumerated by nothing, and so are found only by whoever happens to look.** Definitions are the headline instance. The 58-word sentence and the bad control are the same strain wearing different clothes, and a piece that defined six words would leave the other four ways in wide open.

**The call, and what it means.** `judge:61` says two straining rulings in a row make structural repair the next piece, and that the judge makes the call. I make it. My predecessor's straining and mine are on different strains — his first one he retired himself — so this is a judgment, not arithmetic, and I record that I could have gone the other way on the ground he had. I cannot on the ground I have: the strain is now measurable rather than impressionistic (seven defects, three rounds, zero inside the enumeration, one landing after the class was named aloud), and a structure that keeps producing the same class of defect while every gate stays green is the exact condition this rule exists for. **On judgment line 1, the next kernel piece is structural repair, and it is mandated, not chosen.**

Its charter is wider than my predecessor scoped it. Define the load-bearing words — that half stands, and owner question 4 already has his recommendation. But the piece must also **give the non-rule properties a producer**, or the next round finds the eighth instance. The shape is already demonstrated in this repo: the conservation inventory that enumerated 177 rules is the right instrument pointed at the wrong population, and the `review-integrity` check being widened mid-build is what it looks like when someone notices an instrument cannot see the thing it is for. A cold read of any prose a fix batch adds is the cheapest producer available and §5(b) is what it costs to skip it.

The lines diverge here — mine straining, the other sound — and under `judge`'s own rule divergence is a finding resolved by evidence, never averaged. The evidence I would put to that reconciliation is the seven-defect count and where every one of them fell, not a judgment about whether six words are enough to force a piece.

---

**Sufficient. The piece lands as v5.2.0**, with §7's four small changes in the release commit. Nothing routes back: every ordered route closed at the mechanism under a control I fired myself, the green arm returned and I re-ran it and its control arm at my own hand, and the two items I found are a sentence split and a clause — work this method explicitly says needs no ceremony.

**Not judged, recorded as such:** a whole piece built end to end under these pages by an agent that is not us, and the kernel's contribution measured against its own absence. The first needs a real product; the second needs four runs and is now in front of the owner.
