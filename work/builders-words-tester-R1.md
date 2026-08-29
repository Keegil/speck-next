# R1 — the stranger who builds

**What I read, in this order, and nothing else:** `AGENTS.md`; `.claude/skills/shape-product/SKILL.md`, `.claude/skills/map-build/SKILL.md`, `.claude/skills/craft/SKILL.md`, `.claude/skills/experience/SKILL.md`, `.claude/skills/judge/SKILL.md`; `.claude/skills/shape-product/references/questions.md`, `.claude/skills/map-build/references/questions.md`, `.claude/skills/experience/references/walk.md`, `.claude/skills/experience/references/worst-day.md`; `templates/product.md`, `templates/map.md`, `templates/state.md`, `templates/piece.md`, `templates/rounds.md`, `templates/decisions.md`.

I did not open `work/`, `decisions.md`, `docs/`, `CONTRACT.md`, `README.md`, `map.md`, `state.md`, `product.md`, `capabilities.md`, git history, or anything outside this repo. I listed the repo's directories once to find the files I was told to read. I have never seen Speck before. Everything below comes from those sixteen files.

---

## Part 1 — Stumbles

### S1. A judge in the shape phase is ordered to start from a field that cannot exist

This is the one that would have stopped me on day one.

`AGENTS.md` requires a review before shaping can end: *"It ends only when `product.md` meets its template, a fresh tester has probed it and a separate judge has ruled — both with receipts committed before they ran — and the owner has ratified it."*

`experience` tells me what a receipt must contain, with no phase exception: *"Before the run starts, commit a **receipt**: written proof of who was asked to test what. Record: - Quote the `state.md` Built line that covers these product files."*

In shaping, nothing is built. There is no Built line and there are no product files. And the judge is told: *"Start with the receipt's Built field. Read `state.md` at the cited commit. The quoted line must exist and literally say **Built**."* followed by *"If the check fails, rule nothing."*

Read literally, a shape-phase judge must rule nothing, forever, and shaping can never exit. The only thing that rescues me is `templates/rounds.md`, whose receipt line quietly drops the Built field: *"**Review receipt:** tester [tool, model, session] · dispatched [date, commit] · probes [...]"*. So the escape hatch exists — but it lives in a template, unannounced, and no prose sentence in `AGENTS.md`, `experience`, or `judge` says "the Built field applies to build-phase reviews only." Same problem in the map phase.

### S2. "Screen drawing" is inside a mechanical gate and is never defined or commissioned

The map's completion test is explicitly mechanical — *"Run the completion test. Do not assert it."* — and one of its five checks counts a population I cannot enumerate: *"every captioned screen drawing belongs to exactly one piece"*.

Nothing tells me what a screen drawing is, what "captioned" means, or which step produces one. `shape-product` says *"Create any supporting material the product needs, such as a domain model, journey, or deck"* — deck, not screen drawing. The shaping questions have a heading called *"## Drawn surfaces"* whose three questions never ask for a drawing. `templates/product.md` has no drawings section. `craft` never mentions the term. Yet `AGENTS.md` builds on it — *"Build a drawn screen from its screen drawing"* — and both `templates/map.md` and `templates/piece.md` list *"consumes: [screen drawings/...]"*.

So I am asked to grep and count a set that the method never creates. I would either invent the convention myself or score the check green vacuously, and green-because-empty is exactly the failure mode this repo warns about elsewhere.

### S3. "Its own checks" is the entry condition for the entire review machine, and it is vacuously satisfiable

*"When the piece runs and its own checks pass, write **Built** in `state.md`"*.

Which checks? Never defined. The proof plan names *"the runs, the user types who will test it, and what the judge must rule on"* — not the piece's own checks. If I write no checks, I have no failing checks, so the condition is met and I may write Built. Thirty-five lines of law then defend the integrity of that Built line, and the thing the line attests to has no floor. `AGENTS.md` does constrain check *quality* — *"A check counts only if it can show the failure it claims to prevent"* — but that is a property, not a population.

### S4. "Care level" is a quantity with no values, and a rule about moving it

*"Record the owner's chosen care level and the decision in `decisions.md`; a weekend product and a regulated product need different care."* Then, later: *"You may raise the care level. You may never lower it."*

I cannot raise or lower something with no scale. The mapping questions add *"The owner picks a care level"* and no enumeration. I do not know whether to write "high", a sentence, or a checklist, and I cannot tell later whether I moved it in the forbidden direction. This is one of the few rules in the pages I could break without knowing.

### S5. "Straining" vs "fighting" re-cuts the map, and neither is defined

*"Rule the structure **sound**, **straining** with the strain named, or **fighting**. Two straining rulings in a row, or one fighting ruling, makes structural repair the next piece."*

That is a real consequence — it changes what gets built next. The boundary between the two words is nowhere. Since two strainings cost the same as one fighting, the choice of word literally decides whether the map re-cuts now or in two pieces' time, and I would be guessing.

### S6. "Shaped" is one of four states and is never defined

*"The four states are **Shaped → Built → Judged → Live**."*

Built is defined (*"When the piece runs and its own checks pass"*). Judged is defined by its gate (*"Nothing becomes Judged without this review"*). Shaped appears twice — in that ladder and in `templates/state.md` — and is never given a meaning. Two readings are available and they disagree: (i) product-level, meaning the shape phase exited; (ii) piece-level, meaning the work file was committed per *"Before product code, commit its work file with the outcome, the proof plan, and a hard limit"*.

The subject of the ladder shifts under me too. Built and Judged are plainly per-piece. Live arrives at milestone level: *"When all four rulings stand on evidence, the work is proven and can become Live."* So the "four states" are not four states of one thing.

### S7. Judged and Live are separated by the same sentence

`judge` licenses Live at the end of a *piece* hearing: *"When all four rulings stand on evidence, the work is proven and may become Live."* `AGENTS.md` licenses Live at the end of a *milestone*: *"When all four rulings stand on evidence, the work is proven and can become Live."*

Identical test, two altitudes. So either a single piece can go Live, or it cannot and one of these sentences is over-reaching. And since the judge rules all four at every piece hearing, Judged is a state a piece passes through in the same breath it leaves — which leaves me unable to say what Judged is *for*.

### S8. "Use git to prove" — the one check with no command

*"Use git to prove that the Built line covers the exact product files under review."*

This is the most consequential mechanical check in the method and it ships without a command. Meanwhile `worst-day.md` hands me exact incantations for a much cheaper hygiene check: *"Run `git rev-list --count $(git log -1 --format=%H -- state.md)..HEAD`"*. The effort is inverted. Ten judges will invent ten different proofs, and "prove" will come to mean "looked at the log."

### S9. One sentence I read three times

*"A \"no model here\" foundation piece once quietly owned three judgments the owner's ruling gives to the model."*

It appears verbatim in both `map-build` and `judge`. My best reconstruction: a piece declared model-free ended up making three decisions the owner had ruled belonged to the model. The lesson around it is stated well — *"A piece plan can permit work a standing decision forbids while every count stays green"* — which is why the compressed war story on top of it costs a stranger three passes and adds nothing the plain sentence did not already say.

### S10. One sentence that contradicts itself on the surface

*"One of these testers also receives only `product.md` and the piece's rendered output, not the work file."*

"Also receives only" stopped me twice. It means: one of the rostered testers gets a deliberately narrower briefing — not an extra tester. I only settled it by counting sessions elsewhere. Immediately after comes *"Five rounds once perfected a truthful machine that missed its jobs."* I can guess (a product that never lied but did not do the user's job), but on a cold read this is a private note, not teaching.

### S11. The build-phase batching rule is filed under milestone review

*"You may batch ordinary changes into one review, but review protected-code changes before shipping."*

This sits in the last paragraph of "## Review a milestone", in a paragraph that also carries the state.md cadence rule and the owner-approval rule. Three unrelated obligations, one paragraph, and the one I need most often — how to batch — is where I would never look for it.

### S12. The dispatcher's four bullets miss the state I will be in most often

*"- When every piece in a milestone has landed, run `experience`, then `judge`."*

There is no bullet for "a piece is Built, its review has not started" — the single most common state during a build. It is covered, inside build-loop step 5, but the dispatcher is sold to me as the place I decide where I am: *"Choose the phase from completed evidence, not instinct or the presence of a file."*

### S13. Two names for one thing, one paragraph apart in different files

`AGENTS.md`: *"fix the named problem and repeat the exact test scenarios plus the required fresh challenge."* `judge`: *"re-run every scenario named by the judgment plus one free skeptical attack chosen by the tester."*

"The required fresh challenge" and "one free skeptical attack" are the same obligation under two names. Small, but I checked twice whether I owed one thing or two.

### S14. A parse I had to resolve from a template

*"commit its work file with the outcome, the proof plan, and a hard limit on time, tokens, and files read before the first run."*

Is it a limit on "files read before the first run", or a limit "before the first run" on time/tokens/files? `templates/piece.md` settles it — *"**Before first run:** [Hard limit on planning time, tokens, and files read.]"* — but the prose alone is genuinely two-ways. And then the enforcement drops the crispness the limit was for: *"If planning has gone on for a long time and nothing has run, the limit has failed"*. A hard numeric limit, enforced by "a long time."

### S15. The one thing I would call process for its own sake

`worst-day.md` asks the tester to audit the builder's git hygiene. Two problems.

First, item 2 has no threshold and no consequence: *"How stale is `state.md`? Run `git rev-list --count $(git log -1 --format=%H -- state.md)..HEAD`."* I produce a number. Nothing tells me what number is bad or what to do about it. Compare item 1, which does state its payoff: *"The same commit means the file documented work instead of shaping it."* That one earns its place; the staleness count is a measurement with no decision behind it.

Second, and worse for the product: this whole section is assigned to the worst-day persona, defined two pages earlier as *"the person facing weak permissions, a dying network, corrupt data, and overlapping work at once."* That is a user. Asking that user to run `git rev-list` breaks the only persona in the method whose entire value is that they are not us. The method's own audit needs doing; it should not be done wearing the user's face.

### S16. Rules whose product payoff I can name, but whose weight surprised me

The Built-line rule is stated in four places, in four wordings: `AGENTS.md` step 4, `AGENTS.md` "Open the review honestly" (five sentences), `templates/piece.md`'s receipt bullet (a 100-word paragraph inside a template field), and `judge` §1. I can name the payoff without help — *"An old Built quote cannot cover later work"* — so this is not ceremony. But it is by a wide margin the heaviest single mechanism a new builder meets, and meeting it four times in four shapes made me hunt for the authoritative one. There isn't a marked one.

### S17. Three of the six templates are unreachable from the prose

`shape-product` points at `templates/rounds.md` and `templates/product.md`. `map-build` points at `templates/map.md`. Nothing in `AGENTS.md` or any skill points at `templates/piece.md`, `templates/state.md`, or `templates/decisions.md` — and `piece.md` is the richest of the six, carrying the receipt structure I most need. Build-loop step 2 tells me to *"commit its work file"* without telling me a skeleton exists. I only found it because I was handed a reading list.

### S18. Method shorthand in the section that bans method shorthand

*"When the owner names something as the key, make it the current dependency in the same session."*

"The key" (to what?) and "the current dependency" (of what?) are the two most abstract nouns on the page, and they sit four lines above *"Give bad news first. Use product words."* I can act on the sentence roughly — re-sequence now, say what changed, don't queue silently — but I had to reread it, in the one section where being understood is the stated deliverable.

---

## Part 2 — What lands well

Concretely, these are the parts I could execute cold, with no second pass:

- **The dispatcher.** *"Choose the phase from completed evidence, not instinct or the presence of a file."* Four bullets, each keyed to a committed artifact. I knew where I was in ten seconds.
- **The definition of ratified.** *"*Ratified* means the owner agreed in their own words in that phase's dated record, after seeing a plain-language explanation. Nothing else counts."* No wiggle.
- **The small-change test.** *"A change is small only if it adds no dependency, touches no auth, money, privacy, or data-integrity code, changes no promise, and is reversible in one commit."* Four mechanical conditions, plus *"there is no middle class"* and *"Treat uncertain work as bigger, never smaller."* This kills an entire genre of argument-with-myself.
- **Build commit, defined.** *"A \"build commit\" changes the product itself, such as code, screens, or data; commits that change only records or state are not build commits."*
- **The self-test on my own questions.** *"If you cannot write that opening sentence, the question is not ready."* A rule I can fail against my own output before the owner sees it. Same family: *"if the owner must ask what a sentence means, fix the sentence"* and *"If the owner has to ask what is happening, you missed a handoff."*
- **Identity proof.** Three numbered steps, each mechanical, with the failure named: *"a wrong-subject run still renders screens."* I would have skipped this and been wrong.
- **Freshness, defined operationally.** *"Use a separate context. A walk done by the builder is void."* plus *"Run the tester in a clean clone, never the builder's working tree"* and *"Do not give them the builder's summary."* Three checkable conditions, not an adjective.
- **The four rulings held apart.** *"One cannot compensate for another."* And *"\"Works\" cites at least one real-path run against the real dependency, or states that it covers only the gates."*
- **Disagreement preserved.** *"The first-timer's delight and the worst day's failure can both be true. Do not average them."* This is the rule I would most likely have violated on instinct.
- **Checks that can fail.** *"A check counts only if it can show the failure it claims to prevent; a control that cannot fail proves nothing about the product."* And *"A safety net counts only after you deliberately watched it fail."*
- **The harness rule.** *"use the product's own surface as soon as it exists; a test harness you wrote is not the product."* Six words of it do more than a page of guidance would.
- **`walk.md`.** Twelve numbered steps, each a physical action. *"Run the real build at a named commit, not the dev server."* *"Open every screenshot. Write at least two observations pointing to its pixels."* And the taste discipline: *"Do not disguise your taste as an objective rule or quietly redesign toward it."*
- **`craft`.** The plainest file in the set. Every bullet names the failure it prevents (*"One size and weight makes a flat screen"*, *"Cramped looks cheap"*), and the war story teaches: *"An owner once caught a screen still re-arguing what an earlier screen had already taught him — three elements on it, all dead duplicates of what he had just read."*
- **The sibling sweep, with its yield stated.** *"The reverse direction has the highest historical yield and is the least intuitive."* Surprising and immediately actionable.
- **Self-grading detection.** *"Inspect the diff for changes to tests, CI, benchmarks, or certification logic. Record any change that alters its own grading even if it looks correct."*
- **The honest-denominator rule.** *"Never show a denominator the product has not measured. \"Read 431 deliveries — still reading\" is honest while the total is unknown."* This is product craft, not process, and it arrived where I needed it.
- **The word "hearing" is gone.** Everything is "review", "tester", "judge" — words I already owned.

---

## Part 3 — The four answers

### (a) Fresh repo, these pages installed. What do I do first?

I go to the dispatcher, because it tells me to: *"Choose the phase from completed evidence, not instinct or the presence of a file."* A fresh repo has no ratified `product.md`, so the first bullet fires: *"Without a ratified `product.md`, use `shape-product`."*

Then, from `shape-product`: *"Shape the product in conversation. Ask one or two useful questions at a time. Keep numbered rounds in `work/shaping.md`, starting from `templates/rounds.md`, and quote the owner verbatim."*

So the concrete first move is a message to the owner, not a file. It opens with the phase, per *"Open every reply with the phase, the live piece or round, and what changed since the owner last looked"*, and it asks one or two questions — starting with the one the whole method hangs on: *"In one sentence, what does the user get? Name their outcome, not our feature."* Backed by `shape-product` rule 1: *"Start with the outcome. The first line says what the user gets. If the conversation begins with features, return to what the person is trying to achieve."*

Alongside it I create `work/shaping.md` from `templates/rounds.md` and `product.md` from `templates/product.md` (*"Start `product.md` from `templates/product.md`. The template is a floor."*).

I could answer this in one pass. One gap: nothing tells me the `templates/` directory needs to exist in a product repo or how it gets there — the skills reference the path as if it is simply present.

### (b) What does checking one substantial piece cost?

`AGENTS.md` gives the headline: *"Checking one piece deliberately costs several fresh sessions: at least two testers and one judge, and more for risky work. The piece's work file states the exact number and roles."*

Computing it from the parts:

**Testers.** *"A substantial piece uses the people named in its proof plan, with at least the first two below."* The first two are the first-timer and the worker. → **2 fresh sessions, floor.**

Two clauses that look like they add sessions but do not: *"One of these testers also receives only `product.md` and the piece's rendered output"* and *"For machinery such as checks, boards, or pipelines, one rostered tester attacks it by running it."* Both say "one of these" / "one rostered" — constraints on existing testers.

**Judge.** *"Use a fresh context for each piece."* → **1 fresh session.**

**Floor for an ordinary substantial piece: 3 fresh sessions** — first-timer, worker, judge. Matches the headline exactly.

**Risky piece:** *"At milestones and on risky pieces, a second judge hears the same records without seeing the first judgment."* → **4.**

**Milestone:** *"four fresh people use the increment as a first-timer, a worker doing the whole job, a second user, and a person on the worst day"*, plus judge, plus second judge. → **6.**

**One rejection cycle on an ordinary piece:** *"Re-run the exact scenarios the judge named and judge the piece again before asking to land it."* Read with `judge`'s *"re-run every scenario named by the judgment plus one free skeptical attack"* — that is 2 testers and 1 judge again. → **6 total for a piece that gets sent back once.** A rejected risky piece: **8.**

**Additions I can quote, each a further fresh session:**
- *"If the original context cannot return, a fresh one inherits its persona, full record, and scenario."* → +1 per non-returning tester the judge sends back.
- *"A new context may inherit that record and receipt line, receive the new evidence, and then rule."* → +1 when a judge cannot stay open.
- *"If the classification is genuinely unclear, ask a fresh judge to decide."* → +1 before the piece even starts.

**And the cost before piece one exists.** Shape requires *"a fresh tester has probed it and a separate judge has ruled"*; map requires the same (*"A fresh tester probes the map against the owner's record, repo, and independent evidence, then a separate judge challenges and rules"*). That is 4 more fresh sessions.

**Empty repo to first landed piece: 7 fresh sessions minimum** — 2 for shaping's review, 2 for mapping's, 3 for the piece's — plus two owner ratifications. I can compute that from the pages without guessing, which is the point.

### (c) What do the four state words mean?

*"The four states are **Shaped → Built → Judged → Live**."*

**Built** — clean. *"When the piece runs and its own checks pass, write **Built** in `state.md` — in the build's final commit, or right after it in a commit that changes nothing else."* With its integrity conditions: the line *"must cover the exact product files under review"*, and *"It fails if any build commit lands after it, or if it was written after the receipt opened."* Caveat from S3: "its own checks" has no floor.

**Judged** — mostly clean. *"Nothing becomes Judged without this review"* — the review being fresh non-builder testers plus a separate judge who challenges every verdict. `state.md` must break it out: *"lists the four Judged rulings separately with evidence or \"not judged yet.\""* And a rejection does not reach it: *"An insufficient judgment sends work back without advancing its state."*

**Live** — I can quote the condition but not the meaning. *"When all four rulings stand on evidence, the work is proven and can become Live."* What Live *is* — shipped, deployed, in users' hands — is never said, and the same condition licenses it from a piece hearing and a milestone review (S7). Best defensible reading: Live is the milestone-level state of a proven increment.

**Shaped** — I cannot define it. It appears only in the ladder and in `templates/state.md`. Two readings, both supportable, and they disagree: the product-level reading (shape phase exited, `product.md` ratified) and the piece-level reading (work file committed before code). Under the product-level reading, a live piece mid-build has no state word at all. See S6.

So: two of the four state words are crisp, one is quotable-but-unbounded, and one is undefined.

### (d) Load-bearing terms I could not define from the pages

**Six.**

1. **Shaped** — a named state in the four-state ladder that `state.md` must report, never defined; two readings that disagree, and the ladder's subject shifts between them. (S6)
2. **Live, and its boundary with Judged** — the same sentence licenses it at two altitudes, and its meaning is never stated. (S7)
3. **Care level** — recorded in `decisions.md`, and governed by *"You may raise the care level. You may never lower it."* No scale, no values, no way to tell which direction I moved. (S4)
4. **Straining vs fighting** — a three-valued structural ruling with a real consequence (*"Two straining rulings in a row, or one fighting ruling, makes structural repair the next piece"*) and no boundary between the two loaded values. (S5)
5. **Screen drawing / captioned screen drawing** — a population inside a gate the method insists is mechanical (*"Run the completion test. Do not assert it."*), never defined and never commissioned by any step. (S2)
6. **"Its own checks"** — the condition that produces the Built line, and therefore the entry condition of every review in the method. No population, so vacuously satisfiable by writing none. (S3)

Near-misses I decided not to count, since proximity binds them well enough: *protected code* (the list sits two lines above), *dispatch proof* (= the committed receipt), *strain* (= a recorded workaround, with a count), *substantial* (defined by negation, explicitly no middle class).

The rewrite set itself a target of zero. Four of my six are one sentence's work each — say what Shaped means, say what Live means, give care level three named values, say what separates straining from fighting. The other two are structural: name the artifact a screen drawing is, and give the Built line a check floor.

---

## Verdict, as this builder

**Could I build a great product under these pages?** Yes, and I would want to. Every claim here points at a moment above.

The spine is executable cold. I knew where to start in ten seconds (S-lands, dispatcher). I know exactly what it costs to check a piece and could compute it without a second pass (answer b). The rules that most protect a product are the crisp ones: *"a test harness you wrote is not the product"*, *"A walk done by the builder is void"*, *"A check counts only if it can show the failure it claims to prevent"*, *"Do not average them."* `walk.md` and `craft` are the two files I would hand a new teammate first — twelve physical steps and a bar, with the failure named beside every rule.

What would slow me down is real but narrow: I would have improvised past S1 in the first hour (a shape-phase judge told to start from a Built line that cannot exist), invented my own convention for screen drawings (S2), and produced a Built line with no checks under it without noticing (S3).

**Do they read plain in one pass?** Mostly. `AGENTS.md`, `craft`, `walk.md` and both question sets read straight through. I count about eight sentences that took a second pass — S9, S10, S14, S18, and the three-clause reopening sentence — and two that took a third: *"A \"no model here\" foundation piece once quietly owned three judgments the owner's ruling gives to the model"* and *"One of these testers also receives only `product.md`..."*. The pattern is consistent: the plain rule lands, then a compressed war story on top of it costs the passes. *"Five rounds once perfected a truthful machine that missed its jobs"* is the clearest case — the rule before it was already complete.

The heaviest mechanism, the Built line, is stated four times in four wordings across four files with no marked authority. Its payoff I can name unaided (*"An old Built quote cannot cover later work"*), so it is not ceremony — but it is the one place where the page's weight and my sense of the risk did not match on first read.

**Does anything exist for the methodology's sake?** One clear instance and one near one.

Clear: *"How stale is `state.md`? Run `git rev-list --count $(git log -1 --format=%H -- state.md)..HEAD`."* — a number with no threshold and no consequence, sitting beside a sibling item that does state its payoff. And it is assigned to the wrong person. The whole *"Check whether the team followed the build loop"* section puts a git audit in the hands of the persona defined as *"the person facing weak permissions, a dying network, corrupt data"* — the one tester in the method whose entire value is that they are a user and not us. That is process wearing the product's face.

Near: the same page that says *"Use product words"* asks me to *"make it the current dependency in the same session"* four lines earlier. Small, but it is the section where being understood is the stated deliverable.

Everything else earns its place. The parts I expected to resent — receipts, freshness proof, four separate rulings — each named the failure they prevent, and in three cases named a failure I would have walked into.

---

*Written by R1, a first-time reader, from the sixteen files listed at the top and nothing else.*

---

## Follow-up run (R1′), 2026-08-29, on 714b0fe, ordered by judgment 2's continuation

Same builder, same persona, new session. Nothing above this line is edited.

**What I read this time:** `.claude/skills/judge/SKILL.md` cold; then the diff `e5494cf..HEAD` over `AGENTS.md`, `.claude/skills`, `templates` (added lines only); then, for the free pass, `AGENTS.md`, `.claude/skills/shape-product/SKILL.md`, and this repo's own `product.md`, `map.md`, `state.md`, `decisions.md`, `work/`. I ran two measurements and four greps. Every quote below is copied, not paraphrased.

---

### 1. The cold read of `judge` — one pass, both answers

**(a) What must a judge check before ruling anything?**

The receipt, and specifically its Built field. Three sentences carry it:

> "Start with the receipt's Built field. Read `state.md` at the cited commit. The quoted line must exist and literally say **Built**."

> "Use git to prove that the Built line covers the exact product files under review. It may ride in the build's final commit, or in a records-only commit just after it. The line is invalid if any build commit lands after it, or if it was written after the receipt opened."

> "If the check fails, rule nothing. Order a new Built line in a commit containing nothing else, then order a new receipt."

Then, before any ruling: read the records. *"Now read every tester's record in full and its verdict last. Every verdict claim must point to a moment in that record. Strike any claim that does not."*

One pass. I did not have to reread anything.

**(b) What changes when nothing is built yet, and how does the judge know that's true rather than a label?**

Both halves are answered in one paragraph, the one added by this diff:

> "A shaping or mapping review is different: nothing is built yet, so it has no Built line. Confirm the phase yourself from the repo — no ratified `product.md`, or no ratified map — never from the receipt's own label. Then check that the receipt lists the planned probes and was committed before they ran, and go straight to the records."

So: the Built check is skipped, the committed-before-it-ran check is not, and the trust anchor is the repo rather than the receipt. The second sentence is the whole answer to "how does the judge know" — it names the attack (a receipt labelling itself a shaping review to skip the Built check) and closes it without naming it, which is the right length.

This is the direct fix for **S1**, the one stumble I said would have stopped me on day one. As a *reading*, it is closed: I now have a sentence that says the Built field is build-only, in prose, in the file that enforces it. It also reuses the dispatcher's own vocabulary — *"Without a ratified `product.md`, use `shape-product`"* — so I already owned the test.

One thing the paragraph does not tell me, and I had to fetch from `AGENTS.md`: *how* to confirm a ratification. The answer is there — *"**Ratified** means the owner agreed in their own words in that phase's dated record"* — and `AGENTS.md` names those records as `work/shaping.md` and `work/mapping.md`. That's a one-hop lookup on a page I always have loaded, so I don't count it as a stumble. But see §3: when I actually *ran* this instruction, it failed.

---

### 2. Every sentence changed since `e5494cf`, read as a builder

Twelve added lines. Ten land in one pass. One needs a second. One is heavy but survivable.

**One pass, and each better than what it replaced:**

- *"Claiming fresh users without a committed receipt is fabricated evidence."* — the coinage "dispatch proof" is gone. I checked all six sites: `grep -rn "dispatch"` now returns only ordinary English (dispatch date, dispatching session, re-dispatch). One word for one thing.
- *"Quote the `state.md` Built line that covers these product files. (Build reviews only: a shaping or mapping review has nothing built yet — its receipt lists the planned probes instead.)"* — this is the better half of the S1 fix, because it lands in the *receipt spec itself*, not only in the judge who checks it. The exception now exists where the artifact is authored, not just where it's policed.
- *"Does every piece past Built have a receipt committed before its review ran?"* — replaces "dispatch and review proof". The old form asked a question with no test in it; this one names the test, so the answer is checkable instead of impressionistic.
- *"`templates/` holds the starting skeleton for every file above. `templates/piece.md` carries the piece work file's receipt and judgment fields."* and *"commit its work file (start from `templates/piece.md`)"* — this closes **S17** outright. Three templates were unreachable from the prose; the richest of them is now named twice, once at the exact step where I need it.
- *"A fresh tester probes the map ... then a separate judge challenges and rules — both under receipts committed before they ran."* — clean, dash closed by a full stop.

**The one that needs a second pass — and it's a sibling miss:**

> "Shaping ends when `product.md` meets its template, a fresh tester has probed it and a separate judge has ruled — both under receipts committed before they ran, and the owner has ratified it in the record."

Thirty-six words, and the em dash never closes. So "and the owner has ratified it in the record" reads two ways: a third item of the "Shaping ends when" list, or a continuation of the dashed aside about receipts. The meaning is recoverable — obviously the owner's ratification is a separate exit condition — but I had to decide that, and deciding is a second pass.

What makes it a finding rather than a nit is that the same edit was made at three sites and only this one broke. The other two are correct:

> `AGENTS.md`: "a fresh tester has probed it and a separate judge has ruled — **both with receipts committed before they ran —** and the owner has ratified it."

> `map-build`: "a separate judge challenges and rules — both under receipts committed before they ran. **Finally,** the owner ratifies the order in their own words."

`AGENTS.md` closes the dash pair; `map-build` closes with a period and starts a new sentence; `shape-product` comma-splices out of an open dash. The fix's own skill — *"search for the same problem in sibling fields, checks, screens, and repeated copy"* — is the one that catches this. Repairing it costs one character: close the dash before "and the owner".

(Minor, same family: the three sites say "with receipts", "under receipts", "under receipts". Cosmetic, not worth a commit on its own.)

**The heavy one:**

> "every captioned screen drawing belongs to exactly one piece — the population is the captions in the shaped decks and journeys themselves: grep them, count them, match them against the pieces;"

Thirty-one words, and it is now by some margin the longest of the five bullets in a list whose whole virtue is that it is mechanical. It carries a rule, a definition of the population, a location, and three imperatives in one bullet. I could execute it on one pass, so I am not calling it a defect — but the population sentence is doing different work from the check, and the four sibling bullets stay one clause each.

**The measurement — `judge/SKILL.md`, sentence lengths:**

83 sentences. **Zero over 30 words.** The longest five:

| words | sentence |
|---|---|
| 29 | "Name the reason and destination: a wrong promise returns to shape; badly cut pieces return to map; a bad build returns to build; and thin evidence returns to experience." (renders as a stem plus four bullets) |
| 28 | "'Delivers the promise' is judged against the jobs and promises in `product.md`; the piece's work file may narrow the work under review but cannot replace the product promise." |
| 25 | "If the context cannot stay open while a requested run happens, write a judgment-so-far with what was heard, each challenge, and the exact runs ordered." |
| 23 | "A fix made during the review, before another tester can walk it, needs a control the judge can run against the pre-fix tree." |
| 22 | "Confirm the phase yourself from the repo — no ratified `product.md`, or no ratified map — never from the receipt's own label." |

The 71-word sentence judgment 2 routed the piece back on is gone; the paragraph that replaced it runs 17 / 22 / 21. That order held.

Two sentences added by this diff *outside* `judge` do cross 30: the `shape-product` exit at 36 (above), and `AGENTS.md`'s `state.md` bullet at 34 — *"`state.md` reports what is true now, what is wearing out (every strain, and how often it has bitten), what is blocked, what needs the owner, what happens next, and the evidence for each claim."* That one is a six-item list in sentence form and reads fine; it grew from 26 words to restore a rule that had been dropped, which is a trade I'd take.

---

### 3. Free skeptical pass: I ran the new phase test instead of reading it — it misfires on this repo

I picked the sentence I had just praised, because it is the newest load-bearing instruction on the surface and it had only ever been *read*. So I executed it, as a judge would, against the repository I was standing in:

> "Confirm the phase yourself from the repo — no ratified `product.md`, or no ratified map — never from the receipt's own label."

What the repo answers:

- `product.md` is 5 lines. It contains no ratification, no owner quote, no date. (`grep -in "ratif" product.md` → nothing.)
- There is no `work/shaping.md` and no `work/mapping.md` — the two dated records `AGENTS.md` names as where ratification lives. (`ls` → No such file or directory, both.)
- So by the definition I was sent to — *"the owner agreed in their own words in that phase's dated record"* — **`product.md` is not ratified.**
- The first disjunct fires. The instruction returns: **shaping review. No Built line required. Skip the check.**

And the truth: `map.md` piece 5 is marked `[live — owner-ordered 2026-08-29 …]`, `state.md` says *"The fixed pages are Built as of this commit"*, and the receipt this very run belongs to quotes that Built line. This is a build review in the middle of its second fix batch. The test that exists to stop a receipt from talking its way out of the Built check hands a judge the exemption for free, on the kernel's own repo, with no receipt label involved at all.

Two honest caveats. First, a judge would probably smell it — `state.md` and `map.md` are loud. Second, the misroute is inherited: `AGENTS.md`'s dispatcher runs the identical test (*"Without a ratified `product.md`, use `shape-product`"*) and misroutes here too. That part isn't new. What *is* new is that this diff promoted a routing hint into a security check, and a routing hint that fails safe (an agent shrugs and reads on) fails open when it becomes a gate.

The failure has a shape I'd name for whoever fixes it: **the test is negative.** It asks what is *missing*, so anything missing for an unrelated reason — a thin `product.md`, a repo whose records are named differently, a half-migrated tree — opens the gate. A positive test can't be opened by an absence. The anchor is already in the artifacts: **a review is a build review if `map.md` has a live piece; only a repo with no live piece can be a shaping or mapping review.** I ran that one too — `map.md` piece 5, `[live — …]` — and it returns *build review* on this repo, correctly, in one grep.

I'd also note the shape of how this got through: the fix was validated by re-reading the page. Reading it, it's a good sentence — I said so in §1 and I stand by that. It only fails when someone stands in a repo and does what it says.

**Secondary, reported because I checked it and it isn't clean:** the S2 fix is *partially* closed. The gate now tells me where the population lives — *"the captions in the shaped decks and journeys themselves"* — and I can grep it, which I could not before. But nothing yet says a deck or journey must *contain* captioned screen drawings, so a product with screens can leave shaping with zero drawings and the gate stays green by being empty. Smaller residue than before, and a different one.

**A correction to my own R1 record.** My S2 said screen drawings were "never commissioned by any step." That was too strong, and it was wrong when I wrote it, not because of this diff. `shape-product` rule 11 already read — at `e5494cf`, which is what I reviewed — *"Check every journey, deck, and screen drawing against the domain model, repo, fixtures, or real behavior."* I read that file and missed the clause. Shaping does presume screen drawings exist. What stands from S2 is that the term is never *defined* and never *required*; what falls is "never commissioned."

---

### Verdict, as this builder — R1′

**The pages got better, and the two stumbles I ranked highest are the two that moved.** S1 is closed as prose, in both files that needed it — and closed at the receipt spec, not only at the judge, which is the version that actually reaches an author. S17 is closed outright: `templates/piece.md` is now named at the step where I'd reach for it. S2 is closed halfway, which I'd rather have than the coinage-shaped fix that would have looked complete.

**One sentence needs a second pass:** the `shape-product` exit, 36 words with an unclosed dash, and it's the one site of three where the same edit broke. One character fixes it.

**One new instruction is wrong when executed**, and that's the finding I'd want acted on: the judge's phase check returns "shaping review — skip the Built check" on this repository, today, because `product.md` carries no ratification and no shaping record exists. It reads well and runs wrong, which is exactly the pair a cold read cannot separate. A positive anchor — a live piece in `map.md` — returns the right answer on the same repo in one grep.

**On the ordered measurement:** zero sentences in `judge/SKILL.md` exceed 30 words, longest 29, and the 71-word sentence is gone. That order was carried out.

Would I build a product under these pages? Still yes, and more comfortably than three days ago — the day-one blocker is gone. What I'd want before landing is the dash, and a judge whose phase test can't be opened by something that simply isn't there.

*Written by R1′, the same first-time builder, from the files and the repository named above.*
