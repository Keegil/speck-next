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
