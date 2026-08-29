# Name the words — cold reader T1

**Tester:** T1, first-timer / cold reader. Never seen Speck. A builder about to run a real product under these pages.
**Subject:** `~/Code/speck-next` at commit `ac7e688` (build `48283c7`).
**Date:** 2026-08-29.

## What I read, exactly

- `AGENTS.md` (126 lines)
- `.claude/skills/shape-product/SKILL.md` and `references/questions.md`
- `.claude/skills/map-build/SKILL.md` and `references/questions.md`
- `.claude/skills/craft/SKILL.md`
- `.claude/skills/experience/SKILL.md` and `references/walk.md`, `references/worst-day.md`
- `.claude/skills/judge/SKILL.md`
- `templates/product.md`, `map.md`, `piece.md`, `state.md`, `decisions.md`, `rounds.md`

I also ran four `grep -rn` sweeps across exactly those files, to confirm how often a term appears and whether a definition exists anywhere I had not read carefully. The greps are quoted where they carry a finding.

**Disclosure:** I ran `git log --oneline -1` once, before I understood git history was out of scope. It returned one commit subject line. I did not read it as evidence and nothing below rests on it. No other banned surface was opened — no `work/`, no `decisions.md`, no `docs/`, no `README.md`, no `CONTRACT.md`, no `state.md`, no `product.md`, no `map.md`.

**Note on the loaded copy.** My host loaded an older `AGENTS.md` into context alongside the repo. It is a visibly different document from the one on disk at `ac7e688`. Everything below is judged against the file on disk. Anyone re-running this test should confirm which copy their host handed them first.

---

## Job 1 — the terms test

### How I decided

A term is **UNDEFINABLE** when both of these hold:

1. No sentence in the pages defines it, and
2. A cold builder's plausible readings lead to *different actions* — not just different wording.

A term with no definition sentence but only one sensible reading is a **wobble**: I can act, but the next reader may act differently. I list those separately rather than folding them into the count in either direction.

### Terms the pages recently claimed to have defined — tested hardest

**Shaped — DEFINABLE.**
> "Shaped means the work file is committed with the piece's outcome and proof plan, before any product code." (`AGENTS.md:109`)

Clean, and mechanically checkable — the judge even names the command that checks it (`judge:71`). The old collision between the state *Shaped* and "shaped material" is mostly gone: `AGENTS.md:113` now says "Supporting material", not "shaped material". One residue: `map-build:14` still says "Cut pieces from **shaped work**", meaning the output of the shape phase, not the state. Derivable from position. No action differs.

**care level — DEFINABLE.**
> "The care level is which of these protections are on, plus a second judge; raising it means adding protections — there is no separate scale." (`AGENTS.md:123`)

The protections are enumerated in the same sentence's first half: least-privileged testing, proven rollback, a named stand-in with its fidelity gap. So the care level is a subset of four named switches. That is a real definition and it kills the old "level 3 of what?" problem. I can ask the owner this question cold.

But see hazard H3 below: two pages disagree about whether I may raise it on my own.

**straining vs fighting — DEFINABLE.**
> "Straining means the shape made the work slower or riskier, but the piece still landed honestly; fighting means the shape made the work wrong or forced a workaround before it could land." (`judge:63`)

I tested this on the case most likely to break it. `AGENTS.md:68` says "Record **every** workaround as a strain." So a workaround is routine. But `judge:63` makes "forced a workaround" the marker of *fighting*, which makes structural repair the next piece. Same event, two answers.

It resolves — but only on close reading of the subject of the sentence. The discriminator is *who* forced it: `judge:63` says "**the shape** ... forced a workaround". A workaround forced by a third-party bug is a strain; a workaround forced by our own structure is fighting. That is derivable from the sentence itself, so the term stands. I would still expect a hurried judge to mis-rule here. Logged as hazard H4.

`sound` is defined by residue — neither straining nor fighting. The trichotomy is closed. Fine.

**"its own checks" — DEFINABLE.**
> "Its own checks are the checks named in the piece's proof plan; a plan naming none leaves nothing to pass, so the piece cannot become Built." (`AGENTS.md:61`)

This closes the loophole properly: you cannot become Built by naming nothing. Confirmed consistent at `AGENTS.md:109` ("the checks named in that plan").

But the pointer dangles one level down. The proof plan's own required fields are specified twice, and neither says "checks":
> "Name the runs, the user types who will test it, and what the judge must rule on." (`map-build:18`)
> "Runs · exact user types and number of fresh testers, at least two · judge ... · what each rules on." (`templates/piece.md:11`)

A builder who fills the template exactly has named runs, testers and rulings — and no checks. Read literally, that plan "names none", so the piece can never be Built. The pages self-repair by forward reference (`AGENTS.md:61` tells me the plan names checks, so I write a checks line), and "runs" is a near-certain stand-in. So: term definable, one-word repair available. Hazard H1 — the highest-value repair on this list.

**Live — DEFINABLE, and consistent in three places.**
> "Live means the whole milestone is proven and owner-graded — the first three states belong to each piece; Live belongs to the milestone." (`AGENTS.md:109`)
> "A piece stops at Judged; work goes Live only when its whole milestone is proven and the owner has graded it." (`judge:59`)
> "When all four rulings stand on evidence, the work is proven and can become Live." (`AGENTS.md:96`)

The ruling landed. A piece cannot go Live. One outside-word risk: nothing on any page says Live means *deployed to users*. It is a record state. I read it correctly only because the pages never mention shipping; a builder with production instincts may import the deployment meaning. Minor, logged as hazard H8.

**the map's screen count — the *rule* is definable, the *token* is not.**
> "every screen in the shaped decks and journeys belongs to exactly one piece — grep their captions, report the count even when it is zero, and match each caption to one piece" (`map-build:28`)

"Report the count even when it is zero" is exactly the anti-vacuum clause this check needed, and `map-build:39` reinforces it: "State the full population behind every count." The rule's *shape* is now sound.

I still cannot execute it. See UNDEFINABLE #2.

### Undefinable load-bearing terms — the count

**1. `protected code` — UNDEFINABLE.**

It appears exactly once in the whole corpus (verified by grep across `AGENTS.md`, all five skills, both reference sets, all six templates):
> "You may batch ordinary changes into one review, but review protected-code changes before shipping." (`AGENTS.md:98`)

That is a load-bearing rule: it decides whether a change may ride in a batched review or must be reviewed alone before shipping. Nothing defines it. Two candidate extensions are each forced by a different sentence:

- the small-change list — "touches no auth, money, privacy, or data-integrity code" (`AGENTS.md:119`), supported by "Protected code is never a small change" (`AGENTS.md:121`);
- the risky list — "money, auth, private data, schema migrations, regulated behavior, or anything irreversible" (`AGENTS.md:123`).

They differ. A schema migration is on the second list and not the first. Under reading one I may batch a schema migration into a group review; under reading two I may not. That is a real behavioral fork on exactly the class of work the method slows down everywhere else. Cheap repair: use the words "protected code" once inside `AGENTS.md:119` or `:123` so the term has an address.

**2. `caption`, as the grep token of the completion test — UNDEFINABLE.**

`map-build:28` orders me to "grep their captions". No page anywhere says what a caption looks like. There is no naming convention, no example, and no template for a deck, a journey, or a screen drawing.

Contrast is the proof this is a real gap: the same completion test's *first* bullet names `job:`, `moment:`, `claim:` — and those tokens are defined, both by rule ("Give every promise, job, and moment a short stable name, such as `moment: first-paste`", `shape-product:34`) and by literal example in `templates/product.md`. I can grep those. I cannot grep captions, so the second bullet of a mandatory mechanical check is unrunnable, and the honest report is "I could not run it" — which the pages otherwise forbid me from converting into a pass.

It is worse than silence, because grep hits a second sense of the same word: "Create clear display, heading, body, and **caption** levels" (`craft:12`) — a typographic size level, not a label to match to a piece. A cold builder greps "caption", lands in the craft skill, and learns nothing.

Cheap repair: give screens the same treatment as jobs — a `screen:` token with an example — or replace "grep their captions" with the actual string to match.

**3. `good to use` — UNDEFINABLE.**
**4. `quality hangs together` — UNDEFINABLE.**

Grep returns these only as list items, never as sentences. They appear at `AGENTS.md:94`, `judge:54`, `judge:55`, `templates/state.md:6`, `templates/piece.md:27` — five occurrences, zero definitions.

The asymmetry is the tell. Of the four rulings that gate proven work, the judge defines two:
> "'Works' cites at least one real-path run against the real dependency, or states that it covers only the gates. 'Delivers the promise' is judged against the jobs and promises in `product.md`" (`judge:59`)

and then stops. The other two get no line.

This matters because of the sentence directly above: "One cannot compensate for another" (`judge:57`). Non-compensation is only enforceable if I can tell the heads apart. A clumsy flow with beautiful type: does that break *good to use*, or *quality hangs together*, or both? I can construct a mapping — the tester's walk ends in "works, feels good, and crafted" (`walk.md:16`), so feels-good → good to use and crafted → quality hangs together — but no page states that mapping, and the judge is told explicitly not to copy the tester's verdicts ("The judge's four final rulings are separate; do not copy them", `walk.md:16`).

These are the softer two of my four. Any plausible reading still produces a ruling with evidence attached, so nothing jams. What differs is which head a finding lands under, and with non-compensation in force, that changes whether a piece lands. They are undefined, and I am counting them rather than waving them through, but I would fix `protected code` and `caption` first.

Also noted: `AGENTS.md:94` calls the fourth head "holds together as a quality product" while `judge:55` and both templates call it "quality hangs together". Same head, two names. Harmless today, a citation problem later.

**Final count: 4 undefinable load-bearing terms.** Target was zero.

### Everything else I swept — definable

Each of these carries a rule, and each has a sentence I could quote and act on. Abbreviated to the defining source.

| Term | Defined at |
|---|---|
| Ratified | `AGENTS.md:36` — "the owner agreed in their own words in that phase's dated record, after seeing a plain-language explanation. Nothing else counts." |
| Built | `AGENTS.md:109` + the validity conditions at `:76`–`:78` and `judge:28` |
| Built line coverage | `judge:28` — proven with git; the positional rule (rides in the final build commit or a records-only commit right after, none after it) *is* the coverage mechanism |
| build commit | `AGENTS.md:76` and `judge:27` — "changes the product itself, such as code, screens, or data ... only records or state is not" |
| Judged | `AGENTS.md:109` — "its review has ruled" |
| proven | `AGENTS.md:96`, `judge:59` — all four rulings standing on evidence |
| receipt | `experience:16` + fields at `:17`–`:23`, `templates/piece.md:13`–`:21` |
| fresh (tester) | `experience:10`–`:14` — separate context, not the builder, clean clone, no builder summary; `judge:8` for the judge |
| small change | `AGENTS.md:119` — four enumerated conditions |
| substantial | `AGENTS.md:90` — "anything that does not meet every small-change condition below; there is no middle class" |
| risky | `AGENTS.md:123` — enumerated list |
| strain | `AGENTS.md:68` — a recorded workaround; count and threshold at `:58` (but see H2) |
| foundation / trigger | `shape-product:38`–`:39`, examples at `questions.md:39` |
| whole-product property | `shape-product:32`, `templates/product.md:18` |
| declared feel | `craft:8` — adjectives, "X not Y" lines, restraint rules, cheapeners |
| magic moment | `shape-product:28` — surface, trigger, beats, feeling, proof scenario |
| milestone | `map-build:20` — "the smallest group of pieces that proves a real increment end to end" |
| live piece | `AGENTS.md:56` + `judge:71` — exactly one, and it is the work actually being built |
| land | `AGENTS.md:86` — three named steps |
| proof plan | `map-build:18`, `templates/piece.md:11` (but see H1) |
| supporting material | `AGENTS.md:113` |
| unconsumed material | `templates/map.md:19`, `map-build:29` |
| completion test | `map-build:26`–`:33` — five bullets, "Do not assert it" |
| safety net | `AGENTS.md:68` — counts only after you deliberately watched it fail |
| control | `judge:92`–`:94` — the original reproduction, runnable against the pre-fix tree |
| second judge | `judge:87`–`:88` — same records, first judgment unseen, own receipt line |
| judgment-so-far | `judge:16`–`:17` |
| verdict vs ruling | `walk.md:16` — explicitly separated, and the tester is told not to copy the judge's four |
| identity proof | `experience:33`–`:39` — three numbered steps |
| fabricated evidence | `experience:12`, `judge:14`, `shape-product:44` — defined by its instances |
| sound | `judge:63` by residue |
| piece | no single sentence, but fully specified by its required fields (`map-build:14`, `templates/map.md:15`) — I can build one |

### Hazards — defined, but a second reader may act differently

**H1 · The proof plan never says "checks".** `AGENTS.md:61` defines "its own checks" as the checks named in the proof plan; the proof plan's two specs (`map-build:18`, `templates/piece.md:11`) name runs, testers and rulings. One word in either place closes the loop that gates every Built state in the method.

**H2 · The strain threshold: records or bites?** `AGENTS.md:58` says "A strain recorded twice ... becomes the next piece". `AGENTS.md:106` says state.md reports "every strain, and how often it has **bitten**". `templates/state.md:8` says "Every strain and its count. Twice means next piece." A strain recorded once that has bitten four times: does it fire? "Recorded twice" says no, the bite count says yes. This decides what gets built next.

**H3 · May I raise the care level alone?** `AGENTS.md:123`: "You may raise the care level. You may never lower it." `map-build/references/questions.md:29`: "The owner picks a care level. **Over-engineering past it is the recorded 'we went a bit overboard' failure**, just as under-engineering is." One page grants me unilateral raising; the other records raising past the owner's pick as a named failure. Both are about the same dial.

**H4 · straining/fighting turns on a subject, not a keyword.** Detailed above. The reconciliation is real but easy to miss under time pressure, and the consequence is heavy: "one fighting ruling makes structural repair the next piece."

**H5 · The Built line has no shape.** The receipt must "Quote the `state.md` Built line that covers these product files" (`experience:18`), and the judge must "Use git to prove that the Built line covers the exact product files under review" (`judge:28`). But `templates/state.md` never shows one — it mentions the four states inside a bracket note and stops. A builder working from the template writes something like "Piece 2: Built" and only discovers at receipt time whether it covers anything. One example line in the template removes an entire class of rejected receipts.

**H6 · Two state vocabularies.** `templates/map.md:15` marks pieces `[LIVE/next/done]`; the method's states are `Shaped → Built → Judged → Live`. "Done" is definable — `AGENTS.md:86` says you mark a piece done in map.md after the judge finds it sufficient — but a map showing `done` beside a state ladder ending in `Live` invites a reader to equate the two, which `AGENTS.md:109` explicitly forbids ("Live belongs to the milestone").

**H7 · The tester's verdict has two shapes.** `experience:45` — "whether it works, whether you would keep it, and what breaks the deal". `walk.md:16` — "works, feels good, and crafted". A UI tester following walk.md returns three verdicts; the same skill's body asks for a different three. Resolvable by scope (walk.md is for user interfaces), not stated.

**H8 · "Live" imports an outside meaning.** No page says Live means deployed. See above.

**H9 · `gates` appears once, undefined.** `judge:59` lets the works ruling stand if it "states that it covers only the gates". The word appears nowhere else in the corpus. Near-forced reading: automated checks rather than real-path runs. Kept out of the count because only one reading is sensible, but it is the escape hatch on the strictest ruling in the method, so it deserves a word.

**H10 · `sufficient` is defined only by implication.** It is the landing gate — "Land only when the judge finds the piece sufficient" (`AGENTS.md:86`) — and no page states a threshold. One promise ruled **broken** with the four heads otherwise green: land, or send back? I read it as "no negative ruling stands", forced by "One cannot compensate for another" (`judge:57`) plus the four-head structure. Kept out of the count on that near-forcing, but a sentence would cost nothing.

---

## Job 2 — the planted claims

**Entry B is condemned. Entry A is accepted as a claim.**

The rule is one sentence, and it decides both:

> "Any claim in these files that something is fixed, closed, or done everywhere carries the command that proves it and what it returned — written after the run, never from memory. **A closure without runnable proof is an open item wearing a label.**" (`AGENTS.md:111`)

**Entry B** — "fixed everywhere — I went through all the call sites and updated each one" — makes exactly the claim the rule names ("done everywhere") and carries no command and no return. "I went through all the call sites" is memory, which the rule excludes by name. It is an open item wearing a label. It is also condemned by "Claim nothing beyond the evidence" (`AGENTS.md:111`) and, if it ever reached a review, by "Claiming fresh users without a committed receipt is fabricated evidence" (`experience:12`) — same disease, different organ.

**Entry A** carries the command (`grep -rn 'parseDate(' src/`), what it returned (3 sites, all on the guarded wrapper), and a second command with its return (`npm test` → 41 passing). It satisfies `AGENTS.md:111`. Accepted.

### But accepted is not closed, and the pages say so themselves

Reading only these pages, I would not let Entry A close the finding. Three of the method's own rules bite:

**No control.** "A check counts only if it can show the failure it claims to prevent; a control that cannot fail proves nothing about the product." (`AGENTS.md:68`) And: "Keep the original reproduction for every fixed finding as its control when possible." (`judge:92`) Forty-one passing tests are consistent with a suite that never contained a date-parsing test at all. Nothing in Entry A fails on the pre-fix tree, so nothing in it is evidence about the bug. If the fix landed mid-review, `judge:94` is explicit: "A fix made during the review ... needs a control the judge can run against the pre-fix tree. 'The builder watched it fail' is a claim, not a control."

**"Everywhere" is really "one pattern, one directory".** `grep -rn 'parseDate(' src/` cannot see `new Date(`, `Date.parse`, a differently-named wrapper, or call sites in `test/`, `scripts/`, or migrations. The judge is ordered to close this gap before re-testing: "Before re-testing, search for the same problem in sibling fields, checks, screens, and repeated copy." (`judge:96`) And `worst-day.md:33`: "The reverse direction has the highest historical yield and is the least intuitive."

**The suite grades itself.** "Inspect the diff for changes to tests, CI, benchmarks, or certification logic. Record any change that alters its own grading even if it looks correct." (`worst-day.md:37`) A green count means nothing until I know whether the same change edited the tests.

So the honest ruling a judge should write on Entry A: the *form* of the claim passes `AGENTS.md:111` — command, return, written after the run — and the *finding* stays open until a control that fails on the pre-fix tree exists and the sibling sweep has run. The pages are layered correctly here: 111 governs how you may write a claim, and the judge's re-run rules govern when a fix is closed. Entry A clears the first bar and not the second. That layering is a strength, and I found it without leaving the pages.

---

## Job 3 — my own skeptical pass

**Chosen attack:** I am a builder whose map's second piece is a *domain model* — a markdown artifact, not code. Can I get it through the loop? I traced it step by step through the pages, expecting to find nothing.

I found a jam.

1. **Is it a piece?** Yes, and the pages insist on it. "Supporting material is first-class work. State its purpose when it is created, **assign it to a piece** or list it as unconsumed, **test and judge it**" (`AGENTS.md:113`). `shape-product:10` names "a domain model, journey, or deck" as material the map assigns.
2. **Is it substantial?** Yes. It changes promises and consumes shaped material, so it fails the small-change test (`AGENTS.md:119`), and "there is no middle class" (`:90`). So it needs the full review.
3. **Can it become Built?** "When the piece runs and its own checks pass, write **Built** in `state.md`" (`AGENTS.md:61`). A markdown domain model does not run.
4. **Does the review have an exemption for it?** This is where it jams. The judge's exemption is narrow and doubly gated:
   > "The exemption holds only when `map.md` has no live piece, **or** when the review's subject is `product.md` or `map.md` itself rather than built work. When in doubt, demand the Built line." (`judge:24`)

   My domain model is the live piece, so `map.md` has one. And its subject is neither `product.md` nor `map.md`. It fails both clauses. So the judge must demand a Built line for an artifact that cannot run.
5. **And without it, nothing moves.** "No valid quote means no review." (`AGENTS.md:78`) "Nothing becomes Judged without this review." (`:82`) "Land only when the judge finds the piece sufficient." (`:86`) The piece cannot be judged, so it cannot land, so it keeps the live slot forever — and "only one substantial piece may be under review at a time" (`:90`).

**The escape exists but is nowhere stated.** Give the document piece a proof plan whose checks are genuinely runnable — grep every entity in the model against the fixtures, run the seed script, count the resolved references — and then "the piece runs and its own checks pass" is true in a defensible sense, and a Built line is honest. That is the right answer, and it is consistent with `AGENTS.md:68`'s "a control that cannot fail proves nothing" and with `experience:62`: "For machinery such as checks, boards, or pipelines, one rostered tester attacks it **by running it**. Without an executed attack, the record is a read, not an experience."

But I only found that by working backwards from a deadlock. Nothing tells a builder in advance that a document piece must be given runnable checks, and `judge:24`'s "When in doubt, demand the Built line" pushes an unsure judge toward the deadlock rather than the escape.

**Suggested repair, one sentence in `AGENTS.md`:** a piece whose product is a document becomes Built the same way as any other — by naming runnable checks in its proof plan and passing them; a piece with no runnable check is shaping material, not a piece.

**Second, smaller thing the same trace turned up.** `experience:17` carves out "(Build reviews only: a shaping or mapping review has nothing built yet — its receipt lists the planned probes instead.)" — so the experience skill classifies reviews by *what is being reviewed*, while the judge classifies by *whether a live piece exists*. My domain-model review is a "shaping review" by subject and a build review by phase. The two skills would file it differently. That is the seam the jam sits in.

---

## Verdict — as the builder who has to run this

**I could run a product under these pages tomorrow, and I would.** That is the headline, and I do not want the four defects below it to read as a rejection.

What convinced me: the mechanics that decide whether evidence is real are tight and mutually reinforcing. The Built-line rules (`AGENTS.md:76`–`:78`, `judge:28`) are the tightest writing in the corpus — I know exactly what makes a receipt valid, exactly how to repair an invalid one, and the judge is told to prove it with git rather than trust a label. *Ratified* is airtight. *Fresh* is airtight. Small versus substantial has no middle class, which is the kind of decision most methods dodge. `Live` belonging to the milestone is stated identically in three places. The pages tell me what to do when things go wrong far more often than they tell me what to do when things go right, which is the correct ratio and rare.

What I would fix before running something regulated:

1. **`protected code`** — one undefined word standing between a schema migration and a batched review. Cheapest, highest-consequence fix on the list.
2. **`caption`** — a mandatory mechanical check I cannot execute, made worse by the word colliding with a typographic term in `craft`.
3. **`good to use` / `quality hangs together`** — two of the four gates to proven, defined only by contrast with the two beside them that *are* defined.
4. **H1, the proof plan that never says "checks"** — not a missing definition, a dangling pointer, and it sits under the Built state that everything else hangs from. One word.

The four undefinable terms have a shared shape worth naming: **every one of them is a leaf that no rule points back at.** `protected code` is used once and defined nowhere. `caption` is a grep target with no token. `good to use` and `quality hangs together` are list items whose two siblings got sentences. The pages' recent work clearly ran down the *stated* rulings — Shaped, care level, straining/fighting, its-own-checks, Live, the screen count — and every one of those landed. What survived is the vocabulary nobody thought to put on the list. That is what a cold reader is for.

**Count of undefinable load-bearing terms: 4.** Target was zero.

## What the next reader should not have to relearn

- The `AGENTS.md` a host loads into context may not be the `AGENTS.md` on disk. Check before quoting line numbers.
- Sweep for terms that appear *once*. All four failures here appear once or only as list items. Frequency is the cheapest defect detector in a prose corpus: `grep -c` every term that carries a rule, and read every hit with a count of 1.
- The completion test's first bullet (`job:`, `moment:`, `claim:`) is the model the second bullet (screens) should copy: a named token, an example in the template, and a grep that anyone can run.

---

## Follow-up run (R1′), 2026-08-29, on 980e188, ordered by both judgments

**Tester:** R1′, a fresh cold reader continuing T1. Never seen Speck. Same stance: a builder about to run a real product under these pages.
**Subject:** `~/Code/speck-next` at `980e188` (fix build `c53704e`, pre-fix tree `ac7e688`).
**Ordered:** enumerate the population before staking a number · re-run the terms test against it, with the four pre-fix controls verified · re-run the planted-claims fixture plus a new arm · re-trace the document-piece deadlock · one free attack.

**Disclosure.** My host loaded an older `AGENTS.md` into context alongside the repo — the same hazard T1 recorded, still live one commit later. Everything below is judged against the file on disk at `980e188`. I read `work/name-the-words.md` and this file, because I was ordered to inherit them; I did not read the other testers' or judges' records, `state.md`, `product.md`, or `map.md`.

---

### Job 1 — the population, before anything was staked

T1's zero would have been a number without a denominator. The judges ordered a producer instead. Here it is, and it is reproducible.

**Membership rule.** A term joins the population when both hold: (1) it is a word or phrase appearing in at least one sentence that carries an obligation or a definition, and (2) two plausible readings of it would make an agent *do* different things, not merely say them. File names (`product.md`, `judge`) are addresses, not terms, and are excluded. Section headings are excluded unless the heading is itself the term.

**Extraction.** Three passes over the seventeen installed files:

1. A full read of every non-blank line. `cat "${FILES[@]}" | grep -c '[a-zA-Z]'` → **406** non-blank lines of 701 total. I read all 406, which is what makes the population a census rather than a sample.
2. Two mechanical extractors, as a check on the read: `grep -oh '\*\*[^*]*\*\*'` → 66 distinct bold spans; `grep -oh '`[^`]*`'` → 28 distinct backticked spans. Every item either sits in the population already or is a file address, a template field label whose term is in the population, or an imperative rule heading. **The extractors found nothing the read had missed** — that is the coverage check, and it is the only reason I will put a number on the read.
3. An occurrence count for every term, one `grep -ohE` per term across all seventeen files.

**Population: 124 rule-carrying terms.** Counts run from 1 (`gates`, `fidelity gap`, `accounting summary`, `threshold`, `we are not`, and 17 others) to 114 (`piece`). **Twenty-two terms appear exactly once, and I read every one of those sites in full**, as ordered. None of the twenty-two is undefinable; five are wobbles, listed under Hazards below.

The term list, the regexes and the counts are reproducible from the procedure above; I have not committed the scratch list, because a list that ages in the repo is worse than a procedure anyone can re-run.

---

### Job 2 — the terms test against the population

#### The four pre-fix controls

All four define now. Quoting the new sentences:

**1. `protected code` — DEFINED.**
> "**Protected code** is everything on the risky list below — auth, money, private data, schema migrations, regulated behavior, anything irreversible." (`AGENTS.md:121`)

This resolves T1's exact fork in the direction T1 said it mattered: a schema migration is protected code, so it can never ride in a batched review under `AGENTS.md:98`. The definition sits two lines after its use at `:119` and twenty-three after `:98`, so both uses are forward references — legible on one page, but the first reader meets the word before the sentence that gives it meaning.

**2. `caption` — DEFINED, and the check is now runnable.**
> "a caption is the screen's title line, and the mapping record states the exact pattern it grepped" (`map-build:28`)

The repair is better than a token convention would have been. A screen's title line is product-specific, so no fixed grep could have worked; requiring the mapping record to state the pattern it actually ran makes the check both executable and auditable. The collision with `craft:12`'s typographic caption survives (three sites total, two senses), but it no longer bites, because the definition now sits at the point of use and nobody needs to grep for it.

**3. `good to use` — DEFINED.**
> "'Good to use' is ruled from the testers' felt moments against the feel the product declared." (`judge:59`)

**4. `quality hangs together` — DEFINED.**
> "'Quality hangs together' rules the whole piece's workmanship: every surface at the declared bar, with no weakness excused by strength somewhere else." (`judge:59`)

I ran T1's own hard case against these two: *a clumsy flow with beautiful type — which head breaks?* The new sentences separate the heads by **source of evidence**, not by subject matter. Good to use is ruled from what testers *felt*; quality hangs together is ruled from *workmanship inspection*. So the clumsy flow breaks good to use, and the beautiful type cannot rescue quality hangs together if any surface sits below the bar — a clause that also restates non-compensation inside the head itself. That is a real discriminator and it answers the question T1 could not.

One residue the repair left: `AGENTS.md:94` still calls this head "holds together as a quality product" while `judge:55`, `templates/piece.md:27` and `templates/state.md:6` all call it "quality hangs together". The definition exists; the name does not agree across pages. T1 flagged this and the fix batch defined the head without renaming its odd sibling.

#### The rest of the 124 — one undefinable term

**`sufficient` — UNDEFINABLE.** Nine occurrences, and it is the landing gate.

T1 filed this as hazard H10 and kept it out of the count on a near-forcing. I ran the forcing and it fails, so I am overturning that call on new evidence rather than re-litigating it.

Every site states what an insufficient judgment *does*, never what makes one:
> "Land only when the judge finds the piece sufficient." (`AGENTS.md:86`)
> "Judged means its review ruled it sufficient — a review that sends it back leaves the state where it was." (`AGENTS.md:109`)
> "An insufficient judgment sends work back without advancing its state." (`AGENTS.md:111`)
> "Anything insufficient returns to shape, map, build, or another test round with a trace." (`AGENTS.md:96`)

Consequence in four places, condition in none.

The one available forcing is *sufficient = proven*, and the corpus blocks it. `judge:59` says "When all four rulings stand on evidence, the work is proven," while `judge:57` permits a head to read "not judged yet" and `AGENTS.md:109` requires `state.md` to list the four Judged rulings "with evidence or 'not judged yet.'" So a piece can be Judged — and therefore, by `:109`, ruled sufficient — with heads not yet judged, which is precisely *not* proven. Sufficient and proven are different words for different bars, and only one of them has a bar.

That leaves two live readings and they land the piece differently:

- **(i) sufficient = no negative ruling stands.** A promise ruled *broken* keeps the live slot.
- **(ii) sufficient = the judge's holistic call.** The judge may land the piece and route the broken promise onward as a finding.

Reading (ii) is not a stretch. `judge:59` explicitly lets "the piece's work file narrow the work under review", so a scoped-narrow piece can deliver its own promise while a product promise stands broken — and nothing ties the promise axis at `judge:48` to the landing gate at `AGENTS.md:86`. Two competent judges, same records, opposite decisions about who holds the live slot.

This is the sharpest thing the population producer bought. `sufficient` appears **nine** times, so no frequency filter would ever have surfaced it. It survived a rewrite, a cold reader, two blind judges and an eleven-item fix batch — because everyone who met the word understood it well enough to keep reading, which is exactly how a gate word goes undefined.

The repair is one sentence beside `AGENTS.md:109`, and it is a decision, not a wording choice: either a broken promise blocks landing, or the judge may land over it with the finding routed. The pages should say which.

**Count against the enumerated population of 124: 1 undefinable term.** Target was zero.

#### Hazards — defined or derivable, but a second reader may act differently

T1's H1 is **closed**: `map-build:18` and `templates/piece.md:11` now both say "the checks that must pass" for Built, so the pointer at `AGENTS.md:61` lands. H2, H3, H5, H6, H7, H8 stand as T1 wrote them, and the piece record files them as known-unfixed. New from this run:

**H11 · `the gates` still has one site and no gloss** (`judge:59`). The fix batch defined `good to use` and `quality hangs together` in that very sentence and walked past the undefined word sitting between them. It is the escape hatch on the strictest ruling in the method: "'Works' cites at least one real-path run against the real dependency, or states that it covers only the gates." Kept out of the count because every plausible reading still forces the judge to write the same thing — a works ruling with its limit stated — but a word that exempts the strictest gate deserves a gloss.

**H12 · `the declared bar` is a new count-one term the repair introduced** (`judge:59`). It resolves only by hopping to `walk.md:5`: "If no feel was declared, say that your craft verdict can use only general craft." So the bar is the declared feel, and general craft when none was declared. Derivable across files, unglossed at its only site. Worth naming because the pattern is the one T1 diagnosed: the pass that defines terms also mints them.

**H13 · `current dependency` is one word doing a fourth job** (`AGENTS.md:15`). "When the owner names something as the key, make it the current dependency in the same session." The corpus already uses *dependency* for an external system (`:66`), a package (`:119`), and the real service a works ruling cites (`judge:59`). The action survives, because the next sentence resolves it — "Say how you changed the order, or ask whether it should replace the live work" separates re-ordering from replacing. But this is the owner-facing sentence in the method's most owner-facing section, and it is carrying the corpus's most overloaded noun.

**H14 · `fidelity gap` and `accounting summary`** each appear once, unglossed, with one sensible reading apiece. `fidelity gap` sits at the risky-work site where the care level is defined; `accounting summary` (`map-build:39`) presupposes a section that `templates/map.md` does not contain, so a builder cannot tell whether the map must grow one.

---

### Job 3 — the planted claims, with the new arm

The rule changed under the fix batch. Pre-fix and post-fix, verified with the command:

```
git show ac7e688:AGENTS.md | grep -c "measured number"   → 0
grep -c "measured number" AGENTS.md                      → 1
```

The rule now reads:
> "Any claim in these files that something is fixed, closed, or done everywhere — **and any measured number** — carries the command that produced it and what it returned, written after the run, never from memory." (`AGENTS.md:111`)

**Both original arms still resolve correctly, and the widening did not disturb either.**

**Entry B — condemned.** "fixed everywhere", no command, and "I went through all the call sites" is memory, which the rule excludes by name. Unchanged by the widening.

**Entry A — accepted as a claim.** It carries `grep -rn 'parseDate(' src/` with its return and `npm test` with its return. The widening actually *strengthens* the pass: Entry A's two measured numbers (3 sites, 41 passing) each already carry the command that produced them, so the new clause bites on the same sentence and finds it clean. And T1's layering holds — accepted as a claim, still open as a closure until a control that fails on the pre-fix tree exists and `judge:96`'s sibling sweep has run.

**The new arm — CONDEMNED.** A work-file sentence reading *"the surface is now 57,348 bytes"* with no command.

It is not a closure claim; nothing is fixed, closed, or done everywhere. Pre-fix, that sentence was **clean** — the rule at `ac7e688` covered only fixed/closed/done-everywhere. Post-fix it fails, because bytes are measured, not planned or chosen, and no command or return sits beside it. So the fixture now has a genuine pre-fix control: the same sentence, red on one tree and green on the other, which is what `AGENTS.md:68` demands of any check ("a control that cannot fail proves nothing about the product").

I checked the one scoping question this arm turns on. `AGENTS.md:111` says "these files", and it sits inside "Keep these files true", whose bullet list at `:104` includes the piece work files. So a work-file sentence is in scope under the section's own reading. No fork.

---

### Job 4 — the document-piece deadlock, re-traced

**It is gone, and it was fixed at the right end.** The trace on the fixed pages:

1. Still a piece — `AGENTS.md:113`, unchanged in that respect.
2. Still substantial — no middle class, `AGENTS.md:90`.
3. **Can it become Built? Yes, and the page now says so before I need it:**
   > "A piece whose product is a document still names runnable checks in its proof plan — greps, probes, measurements — and that is how it becomes Built like any other piece." (`AGENTS.md:113`)
4. The proof plan can carry those checks, because `map-build:18` and `templates/piece.md:11` now name checks as a required field. The escape T1 had to derive backwards from a deadlock is now the stated forward path, and the field it needs exists.
5. `judge:24`'s exemption is no longer the trap it was. Its default — "When in doubt, demand the Built line" — is now the *correct* answer for a document piece, because the Built line is obtainable. The clause that used to point an unsure judge into the deadlock now points them at the fix.
6. The seam T1 found between `experience:17`'s classification by subject and `judge:24`'s by live-piece has closed in practice, and I checked both ends. Material probed during shaping: no map, therefore no live piece, therefore exemption granted, receipt lists planned probes. A document piece in build: live piece exists, Built line demanded, Built line available. The two classifications now agree on both cases.

**One residue, and I want it on the record rather than waved through.** `AGENTS.md:61` still says "When the piece runs and its own checks pass" — the phrase that created the jam. It was not amended. A document does not run, so `:61` and `:113` are reconciled only by specificity: `:113` is the rule for this case and says "like any other piece", which is a direct instruction about how `:61` applies. That reconciliation is available to any careful reader and I made it without strain. It is a seam, not a jam, and it is the last one on this path.

---

### Job 5 — free attack: a positive control on the producer itself

I turned the method's own rule on the instrument this run stakes its number on. `AGENTS.md:68`: "A check counts only if it can show the failure it claims to prevent." My population producer is a check. So: run it against a tree where the answer is known.

I rebuilt the pre-fix corpus and ran the count-one filter against it:

```
git archive ac7e688 | tar -x -C <tmp>
grep -ohiE "<term>" <the 17 files> | wc -l
  protected.code           2   caught by the count-one filter? NO
  caption                  3   caught?  NO
  good to use              4   caught?  NO
  quality hangs together   3   caught?  NO
```

**The count-one filter catches zero of the four defects that were actually there.** Recall on the known-true set is 0/4. The half of the producer that reads like a producer — grep every term, read every count-one hit — has, on this corpus, never once found a real undefinable term. It surfaced five wobbles this run and no defects. My zero-but-one does not rest on it at all; it rests on the census: 124 terms, a stated membership rule, and a read of all 406 non-blank lines.

This matters for the owner's question in the piece record — *is the vocabulary job finite?* It is, but the finite thing is the census, not the grep. A standing producer built on frequency would run green forever while `sufficient` sat undefined at nine occurrences.

**Two more things the control turned up.**

**T1's own grep was wrong, and the rule this piece added would have caught it.** T1 wrote that `protected code` "appears exactly once in the whole corpus (verified by grep across `AGENTS.md`, all five skills, both reference sets, all six templates)". At `ac7e688` it appears **twice** — `AGENTS.md:98` hyphenated as "protected-code" and `AGENTS.md:121` capitalised as "Protected code". T1's grep almost certainly missed one form. The verdict is untouched: both sites *use* the term and neither *defines* it, so T1 was right about the defect and wrong about the count. But "verified by grep" with no command and no return is exactly the sentence `AGENTS.md:111` now forbids — a measured number written from memory. The piece's own producer rule, applied to the piece's own tester record, catches its one factual error. That is the strongest evidence I found all run that the rule is worth its words.

**And the reason the count-one filter missed everything is structural, not accidental.** A term used twice in two senses (`caption`), or used in four places and defined in none (`good to use`), is *more* dangerous than a term used once, because repetition reads as familiarity. Frequency detects rarity. Undefinedness is not rarity.

---

### Verdict — as the cold builder who has to run this

**I would run a product under these pages, and after this run I would do it with more confidence than T1 had.** Eleven fixes landed, four of them the exact terms T1 named, and each one defines under a hard test rather than merely appearing. The two heads that were undefined now separate by source of evidence, which is a better repair than the mapping T1 had to construct for himself. The document piece can become Built by naming greps as its checks, which unjams the one path T1 found blocked end to end. The producer rule now covers measured numbers, and I watched that widening condemn a sentence that was clean one commit earlier.

What I would fix before running something regulated, in order:

1. **`sufficient`** — the landing gate, nine occurrences, no threshold, two readings that hold the live slot differently. One sentence, and it is the owner's or the kernel's call, not a wording tidy-up.
2. **`the gates`** — the exemption on the strictest ruling, still one site, still unglossed, now conspicuous because its two neighbours in the same sentence got sentences.
3. **The name mismatch on the fourth head** — `AGENTS.md:94` says "holds together as a quality product"; everywhere else says "quality hangs together". A citation problem waiting to happen.
4. **`the declared bar` and `current dependency`** — one new unglossed term the repair minted, and one overloaded noun in the most owner-facing sentence on the page.

**Count of undefinable rule-carrying terms: 1, against an enumerated population of 124.** Target was zero. The gap is one word, and it is the word the whole build loop turns on.

### What the next reader should not have to relearn

- **Frequency does not detect undefinedness.** The count-one filter scored 0/4 against the pre-fix tree, and the one term I found this run appears nine times. Read the census; keep the grep as a cheap extra, never as the producer.
- **The pass that defines terms also mints them.** `the declared bar` arrived in the same sentence that defined two heads. Any definition round should end by re-running the extractors on its own diff.
- **A gate word explains itself well enough to keep reading, which is how it stays undefined.** `sufficient` survived a rewrite, a cold reader, two blind judges and an eleven-item fix batch. Sweep the gate words specifically — the words that decide whether work moves — and demand a condition sentence for each, not a consequence sentence.
- **T1's `AGENTS.md` hazard is still live.** My host loaded a stale copy one commit later. Check which copy you were handed before quoting a line number.
- Applying the producer rule to a tester's own record is cheap and it works. It caught T1's miscount in one command.
