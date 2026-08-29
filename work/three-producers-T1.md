# Three producers — cold reader T1

**Tester:** T1, cold reader. Never seen Speck. A builder deciding whether to run a real product under these pages, and a judge-to-be who will have to apply them.
**Subject:** `~/Code/speck-next` at commit `def1677` (build `77628d1`, Built line `fc33a7b`).
**Date:** 2026-08-29.

## What I read and ran

Read in full, on disk: `AGENTS.md` (127 lines), `.claude/skills/judge/SKILL.md` (98 lines), `templates/state.md`, `templates/piece.md`, `state.md`, `work/three-producers.md`. Read in part: `.claude/skills/experience/SKILL.md` (receipt lines only), `README.md` and `CONTRACT.md` (grep hits only).

Commands run, with what they returned, are quoted inline at every finding that rests on one.

**Disclosure — the loaded copy is not the copy on disk.** My host preloaded an `AGENTS.md` into my context that opens `# Speck Next / You are an agent in a repository run by Speck Next` and contains a section called "The conductor — law in every session." That is not the file at `def1677`; the file on disk opens "You are building a product with Speck Next" and has no such section. Every reading below is against the file I opened with Read, not the one my host handed me. This is the same trap the previous cold reader disclosed on the definitions piece. It has now bitten two cold readers in a row on two different pieces — see Finding 3.

---

## Job 1 — census delta on the additions

**Method.** I took the additions mechanically, not by eye:

```
git diff caf557f..77628d1 --word-diff=porcelain -- AGENTS.md .claude/skills | grep '^+' | grep -v '^+++'
```

returned exactly five added spans and nothing else — the two-sentence rule 1 paragraph, the rule 2 clause, the `sufficient` clause in `AGENTS.md`, the `sufficient` sentence in judge, and the two-sentence control rule in judge.

Then I built the pre-image vocabulary (`AGENTS.md` + all five skills at `caf557f`, lowercased, split on non-letters, sorted unique = **1170 words**) and subtracted it from the additions' vocabulary. Words appearing in the additions and **nowhere** in the pre-image pages, all 16:

> defective · define · deliver · executes · **home** · **homes** · items · ones · pages · requirement · **silent** · **site** · stated · surfaced · trips · word

Of those, four carry a rule — a reader must know the word's extension to obey the sentence. The rest are plain English or verb forms of words already on the pages. I then hand-checked the rule-carrying words that are *not* new to the corpus but are load-bearing in the new sentences, because rule 2's second branch ("use one these pages already define") only holds if the pages actually define them.

### The census table

| Word | New? | Defining sentence |
|---|---|---|
| **sufficient** | no (used 5× undefined) | **Defined by this piece.** judge:59 — "Sufficient means the piece delivers what it was shaped to deliver — you may land it with open items, never silent ones: `state.md` names each item and its destination." Same rule at AGENTS.md:111. |
| **home / homes** | yes | AGENTS.md:70 — "Before changing a rule that is stated in more than one file, grep for its words and find every home." Defined by apposition: a home is a file that states the rule. Thin — the sentence never says "a home is…" — but it is the only reading available and I took it on one pass. **DEFINED.** |
| **silent** | yes | judge:59 — "…never silent ones: `state.md` names each item and its destination." The colon supplies it: silent = not named there. **DEFINED in its first sentence.** |
| **site** | yes | judge:92 — "never only the site where the defect surfaced." Glossed in the same breath. **DEFINED.** |
| **pages** ("these pages") | yes | AGENTS.md:3 — "This page and the five skills it names are the whole method — there is nothing else to load or look for." Fixes the set at six files and correctly excludes `README.md`, `CONTRACT.md`, and `templates/`. **DEFINED**, and the scoping matters: it stops an author citing a definition an agent never loads. |
| **population** | no (map-build:33, :39) | Self-glossed at judge:92: "names its whole population — every home, file, or case in the class." **DEFINED in its first sentence.** |
| **control** | no | judge:92, pre-existing first sentence: "Keep the original reproduction for every fixed finding as its control." **DEFINED.** |
| **floor** ("its floor, not its scope") | no | AGENTS.md:115 "Templates are starting floors, not limits" and four template headers "A floor, not a form." Same sense — a minimum that may be exceeded. **DEFINED, and reused correctly.** |
| **open item** | no (AGENTS.md:113) | AGENTS.md:113 is a use, not a definition ("A closure without runnable proof is an open item wearing a label"), but the new sentence gives it operational content and the phrase is plain English. **DEFINED enough.** |
| **class** ("in the class") | no, but in unrelated senses | Pre-existing hits are "no middle class" (AGENTS.md:92, piece size) and "first-class work" (:115) — neither is this sense. The new sentence self-glosses by enumeration ("every home, file, or case"). **DEFINED in its first sentence**, not by inheritance. |
| **destination** | no (judge:75) | **COLLISION — see below.** |

### Zero UNDEFINABLE. One collision the rule cannot express.

Nothing in the delta is undefined. The target is met. But one word is defined on the pages in a sense that **excludes** the new use, and rule 2 as written cannot say so.

```
grep -rn "destination" AGENTS.md .claude/skills
```

returns three hits. Two are new (AGENTS.md:111, judge:59). The third is the only one that gives the word an extension — judge:75:

> "Name the reason and destination:
> - a wrong promise returns to shape;
> - badly cut pieces return to map;
> - a bad build returns to build; and
> - thin evidence returns to experience."

Destination is defined there by enumeration: one of four route-backs. The new sentence uses it for open items on a piece that **lands** — which by definition routes nowhere. A landed piece's open item goes to the owner, to a later piece, or to a strain line, and not one of those is on judge's list. Worse, a reader meets the new use at judge:59 *before* the definition at judge:75, so the reader who does what rule 2 tells them — look for the definition on the pages — finds one that fits badly.

**This is rule 2's own blind spot, found by applying it to its author.** Rule 2 says: "define it in its first sentence or use one these pages already define." The author took the second branch and satisfied the letter. The rule has no words for *defined here, in a sense that excludes this use* — the failure it most needs to rule out is one it cannot express. That is the same shape as the check-that-cannot-fail already on the page at AGENTS.md:68. The cheap repair is one clause: *…or use one these pages already define **in the sense you mean** — a word defined elsewhere in a narrower sense is undefined here.*

---

## Job 2 — the four sentences, read cold in place

Read in reading order, one pass each, without the work file open.

**AGENTS.md:70 — same edit, every home.** One pass, clean. Concrete verbs (grep, land, list), a named artifact, and a flat closing judgment. **What it buys a builder:** it moves a whole defect class from review time to authoring time. Before this, the page could only catch a one-sided edit after the fact, by refusing the closure claim at :113. Now the procedure runs before the commit exists. The one-line difference between the two is worth naming: :113 condemns the *report*, :70 condemns the *edit*.

**AGENTS.md:113 — a word defines at birth.** One pass. The closing half ("defective when written, not when a reader trips over it") is the sharpest line in the delta — it relocates the defect from the reader to the author and does it in nine words. **What it buys:** it stops the argument a builder always wants to have ("but it's obvious from context"). And it has an enforcement partner already on the page — judge:67, "Use cold-reader testimony on owner-facing prose" — so the author's own judgment of what "carries a rule" is checked by someone else at review. That closes the loop I went looking for.

**AGENTS.md:111 / judge:59 — sufficient.** One pass in both homes. The judge version reads better; the AGENTS.md version is a colon-clause inside an already-long sentence about four states, and it is the only one of the four I had to slow down for — not to understand it, but to find it. **What it buys:** the largest thing in the delta. It converts "sufficient" from a word every builder guesses at into a two-part test they can apply themselves *before* dispatching a judge: did it deliver what it was shaped to deliver, and is everything still open written down with where it went. See Job 4 — I could actually rule with it.

**judge:92 — a control names its population.** Two passes, and the reason is worth reporting. "Every home, file, or case in the class" reads redundant if you have just learned from AGENTS.md:70 that a home *is* a file. I stopped. It resolved only when I applied it to Fixture 2: the triad is not a triad of synonyms, it is three kinds of population member for three kinds of defect — a rule has homes, a stale figure has files, a code defect has cases. That is load-bearing, not sloppy, but it is invisible until you use it. **What it buys:** it names the exact mechanic behind the strain in `state.md`:11 — the builder executes the grep instead of the sentence above it. "The quoted control is its floor, not its scope" is the fix in eight words.

**Verdict on Job 2:** all four read in one pass except judge:92, which read in two, and the fix there is a two-word gloss, not a rewrite. All four buy something a builder can name.

---

## Job 3 — the two planted fixtures

### Fixture 1: "Fixed the receipt rule in AGENTS.md."

**Premise checked first.** The fixture claims the receipt rule lives in three homes.

```
grep -rln "receipt" AGENTS.md .claude/skills templates
```

returns eight files, including `.claude/skills/experience/SKILL.md` (five hits — line 16, "Before the run starts, commit a **receipt**", and line 18, "Quote the `state.md` Built line") and `templates/piece.md` (line 15, the whole Built-quote rule). Premise confirmed: at minimum three homes, in fact more.

**CONDEMNED.** AGENTS.md:70:

> "Before changing a rule that is stated in more than one file, grep for its words and find every home. Land the same change everywhere in one commit and list the homes in the record; **a one-home fix is not a fix.**"

Three clauses fire independently: the grep was not run, the change did not land everywhere in one commit, and the record lists no homes. The last clause condemns the fixture outright.

**Second, weaker condemnation** — worth reporting because it tells you what rule 1 adds. AGENTS.md:113 already said: "Any claim in these files that something is fixed, closed, or done everywhere … carries the command that produced it and what it returned." The fixture line says *Fixed* and carries no command, so the old rule also condemns it. But it condemns the **sentence**, one round later, at review. Rule 1 condemns the **edit**, before the commit. The piece's claimed outcome — stopping the class at its source — holds here, and the two rules do not overlap.

### Fixture 2: "Control: `grep -c 'stale figure' state.md` returns 0."

**CONDEMNED.** judge:92:

> "When you order a fix and quote a control, the control names its whole population — **every home, file, or case in the class — never only the site where the defect surfaced.** The builder executes the full requirement; the quoted control is its floor, not its scope."

The figure lives in three files; the control names one — the site it surfaced at. Condemned by the middle clause verbatim.

**Note on coverage.** Rule 1 does *not* reach Fixture 2, and should not: it is scoped to "a rule that is stated in more than one file," and a stale figure is not a rule. Only judge:92 reaches it, and only because its population triad is wider than "home." That is what earns the triad, and it is the answer to my Job 2 wobble.

**Both fixtures condemned, each by a sentence quotable verbatim, neither surviving. The prediction in the proof plan holds.**

---

## Job 4 — can a judge-to-be rule from the pages alone?

**The question:** may a piece land with one open, named, routed item? **Concrete case:** the review found a wrong owner-facing word; it is filed to the owner in `state.md`.

**Yes — I can rule this from the pages alone, and here is the chain, four sentences long.**

1. AGENTS.md:88 — "Land only when the judge finds the piece sufficient." So everything turns on the word.
2. judge:59 — "Sufficient means the piece delivers what it was shaped to deliver — you may land it with open items, never silent ones: `state.md` names each item and its destination." So an open item does **not** block landing, on two conditions: the shaped outcome was delivered, and the item is named with its destination.
3. Is a wrong owner-facing word instead a send-back? judge:84 answers directly: "Some findings need the owner's call, **such as their copy**, price, or a product-level promise. Put each in the piece's work file as a self-contained question. … **Do not send the piece back for a decision the builder cannot make.**" Copy is named explicitly, and the page forbids the route-back.
4. Where the item lives: `state.md` has a standing "What needs the owner" section (AGENTS.md:108, `templates/state.md`:13). The filing in the case as posed lands exactly there.

**Ruling: it may land.** And the pages gave me the discriminator for the hard version of the case, which is the part I did not expect to find. If the "wrong word" is one the builder could simply fix — say, an undefined rule-carrying word — then AGENTS.md:113 says it "is defective when written," it is a defect in the delivered thing, and judge:79 routes it: "a bad build returns to build." If it is the owner's word to choose, it is an owner question and the piece lands. The test that separates them is judge:84's own phrase — *a decision the builder cannot make*. That is a clean, applicable line, and before this piece I would have had nothing to draw it with.

**One correction to the case as posed.** Filed to the owner in `state.md` satisfies judge:59, but judge:84 also requires it to sit "in the piece's work file as a self-contained question" starting with "what the choice changes for users." The case as stated is half-filed. It may land **once both filings exist** — and the pages never say in one place that both are required. That seam is Finding 2 below.

---

## Job 5 — free skeptical pass (three findings, reported as found)

### Finding 1 — the landing commit fails rule 1 on the state template. *(should-fix)*

Rule 1 says to grep for the rule's words and land the change in every home. I ran the grep it prescribes for the rule the piece changed:

```
grep -rn "Judged means\|For Judged\|Judged spells" AGENTS.md .claude/skills templates CONTRACT.md
```

returned three homes: `AGENTS.md:111` (changed by this piece), `templates/state.md:6` (**not changed**), `CONTRACT.md:20` (**not changed**).

`templates/state.md` matters more than the count suggests: it is the skeleton every product's `state.md` starts from, and the new rule places a **new obligation on `state.md`** — "names each item and its destination." The template lists six sections; none of them is open-items-with-destinations, and line 3 says "keep these six questions and add what the owner needs." A builder starting a real product from that template will never learn the obligation exists unless they happen to read AGENTS.md:111 and infer a home for it. Same class, lower weight: `templates/piece.md`:31 asks for "what remains open" with no destination.

Nothing here contradicts the change — the templates are silent, not wrong. But silence is exactly what a one-sided edit looks like from inside, and the rule that forbids it landed in the same commit that committed it.

**There is also a gap between rule 1's two halves.** "Find every home" is the discovery clause; "list the homes in the record" is the report clause. The piece's record (work file line 5) lists the homes it *edited* — and satisfies the report clause perfectly while the discovery clause failed. Rule 1's own neighbour at AGENTS.md:113 already knows the fix: a "done everywhere" claim "carries the command that produced it and what it returned." Rule 1 asks for a grep and never asks to see it. **Repair:** the record lists the grep and every home it returned, each marked edited or not-applicable — one clause, and it closes the hole this finding walked through.

### Finding 2 — rule 1 does not reach a stale sibling in the same file. *(worth a sentence)*

Rule 1 triggers on "a rule that is stated in more than **one file**." A rule stated twice in one file is outside it. That is not hypothetical:

```
grep -n "finds it sufficient\|finds the piece sufficient" AGENTS.md
```

returns `62` and `88` — the landing rule, stated twice in one file.

And the piece's own Built commit contains an instance. `git show fc33a7b:state.md | grep -n Built` returns line 31, which reads, in one paragraph:

> "**The live piece "Three producers" is Built as of this commit** … **No piece is live.** The next kernel piece … is **three producers** … and it waits on the owner's word."

The new bolded sentence was prepended; the stale body around it was left standing, contradicting it in the same breath. The Built line itself is valid and literal, so the receipt survives (I checked: build `77628d1` precedes the Built commit `fc33a7b`, which changes nothing else; the receipt opened later at `def1677`; `6c22d89` is state-only, not a build commit). And it was corrected in the very next commit. But the defect class `state.md`:11 names — "a corrected figure left standing in the file that outranks the corrected one" — is a **same-file** failure, and rule 1 as written covers only the cross-file half. judge:96's sibling sweep covers the rest, but only at re-test time, in the judge's hands, after a finding exists. At authoring time there is nothing. **Repair:** delete "file" from the trigger — "a rule stated in more than one place."

### Finding 3 — the host preloads a stale `AGENTS.md`, and it has now bitten two cold readers. *(environmental, but it belongs to somebody)*

My context was preloaded with a v5.0-era `AGENTS.md` that no longer exists on disk. The previous cold reader disclosed the same thing on the definitions piece. Two testers in a row, two different pieces. A tester who trusts the loaded copy will review a document that is one full rewrite out of date and report findings that are all phantom — and nothing in the pages tells a tester to check. This is not a defect in the four sentences and I do not hold it against them, but it is a live threat to every review this method runs, and after two instances it is a strain, not an accident. It belongs in `state.md`'s wearing-out list with two bites, or in the `experience` skill as one line: *read the pages from disk at the commit under test; do not trust what your host loaded.*

### Checked and clean

- **Rule 2 is not self-refuting.** Its own new words (`defective`, `word`, `trips`) are plain English; `pages` is defined at AGENTS.md:3. It does not demand a definition of every word, only rule-carrying ones.
- **Rule 2's soft spot is closed elsewhere.** The author decides what "carries a rule," which is self-judging — but judge:67 sends cold-reader testimony at owner-facing prose, so an outsider checks the call at review. No finding.
- **`floor` is reused in the sense the pages already establish** (AGENTS.md:115, four template headers). Clean reuse, not a new coinage.
- **The four sentences contradict nothing** in `templates/`, `CONTRACT.md`, or the other four skills. Checked by grep on `sufficient`, `receipt`, `population`, `floor`, `open item`.
- **The receipt is valid**, checked against AGENTS.md:78–80 with git: the quote is a literal prefix of `fc33a7b:state.md`:31 and says **Built**; no build commit follows it; it precedes the receipt.

---

## Verdict

**Sufficient, with one should-fix.**

The census delta is clean: zero undefined rule-carrying words, sixteen new words of which four carry rules and all four are defined at first use. Both planted fixtures are condemned, each by a sentence I could quote verbatim without interpretation, and rule 1 and judge:92 divide the work between them without overlapping. All four sentences read in one pass except judge:92, which cost me two and needs a two-word gloss, not a rewrite. And the sufficient sentence does the thing it was written to do: I was handed a concrete case cold and ruled it from the pages alone in four steps, including a discriminator for the hard version that I could not have drawn yesterday.

I would build under these four sentences. I would want two things fixed first, and I would take both as findings against the landing commit rather than the sentences:

1. **Finding 1** — the change owes `templates/state.md` a home, because the new obligation falls on a file whose skeleton has no place for it; and rule 1 should have to show its grep, the way its neighbour at :113 already requires of every "done everywhere" claim. This is the piece's own rule failing on the piece, which is the most useful thing I found and the reason to fix it rather than argue it.
2. **The `destination` collision** — one clause on rule 2 ("in the sense you mean") turns a rule that cannot express its own most likely failure into one that can.

Finding 2 is a sentence-sized sharpening. Finding 3 is not the piece's fault and needs an owner for it anyway.

---

## Follow-up run (E1), 2026-08-29, on 39cdbd8

**Tester:** E1, fresh cold reader. Never seen this piece, never seen this method. A builder deciding whether to run a real product under these pages.
**Identity:** Claude Code · Opus 5 (`claude-opus-5[1m]`) · session `d6f7954a` · 2026-08-29. (The repo's commit trailer reads *Claude Fable 5* by host convention; this line is the model that actually ran, and the two disagree.)
**Subject:** `~/Code/speck-next` at commit `39cdbd8` (fix builds `684e359` then `0f30c51`, plus the truth commits).
**Ordered by:** the third re-entry receipt in `work/three-producers.md`.

**Disclosure — my host preloaded a stale `AGENTS.md`, third reader in a row.** The copy handed to me in context opens "You are an agent in a repository run by Speck Next. This page is the whole method — your host loaded it for you" and carries a section titled "The conductor — law in every session." No such file exists at `39cdbd8`. `git log -S "your host loaded it for you" -- AGENTS.md` returns `b7bb41c` and `e5494cf` — the loaded copy is the version `e5494cf` replaced. Every reading below is from `Read` against disk. The tester law now on the `experience` page and at `judge:10` is what made me check before reading a word; it worked, and the strain is real — three readers, three pieces, three preloads.

---

### Job 1 — the changed sentences, one pass each, cold

Read in file order, without the work file open.

**`AGENTS.md:61` — step 4, Mark it Built. One pass.** The dash clause offers two placements ("in the build's final commit, or right after it in a commit that changes nothing else") and I had to hold both, but it read once. **What it buys a builder:** it takes "its own checks" away from the builder's discretion at Built time and pins it to the proof plan, which was committed at Shaped before any code. Then the last clause closes the obvious dodge: *"a plan naming none leaves nothing to pass, so the piece cannot become Built."* The cheapest route to Built — name no checks — is the one route explicitly barred. That is a producer, not a detector: it makes the gaming move impossible rather than catchable.

**`AGENTS.md:62` — step 5. One pass, with one stumble I am charging.** *"If not, fix the named problem, then execute the judge's full requirements — a quoted control is a floor, not the scope — plus the required fresh challenge."* **What it buys:** the floor rule now sits on the builder's page, at the exact moment a builder reads after a route-back. Before, it lived only where the judge writes controls, not where the builder executes them; a builder could obey their whole page and still do the one-site fix. That gap is closed and I can see it closed.

**Stumble — `fresh challenge` is an undefined rule word, and it is minted by this batch.**

```
grep -rn "fresh challenge" AGENTS.md .claude/skills templates   -> AGENTS.md:62 only
grep -rniE "free skeptical attack|free attack" AGENTS.md .claude/skills templates
   -> AGENTS.md:90 · .claude/skills/judge/SKILL.md:96
```

The obligation is named "one free skeptical attack of the tester's own choosing, reported either way" in both places that state it. Step 5 calls it "the required fresh challenge" — a third name, defined nowhere, and *required* by nothing the sentence names. I could reconstruct the referent, but reconstruction is the bar rule 2 exists to raise:

> `AGENTS.md:113` — "when a word carries a rule, define it in its first sentence or use one these pages already define **in the sense you mean** — an undefined rule word is defective when written, not when a reader trips over it."

The phrase carries a rule (it is one of two things step 5 orders after a route-back), it is not defined in its first sentence, and the pages do not define it. Rule 2 condemns the sentence that landed beside it. **Repair:** use the name the pages already carry — *"plus one free skeptical attack, reported either way."* Same length, zero new words.

**`AGENTS.md:70` — the same-edit rule. One pass, dense but clean.** **What it buys:** three upgrades I can name against the version this one replaced. (a) *"Before landing a new rule or changing one"* — it now fires when a rule is **born**, which is the case that most needs it and the one a change-only trigger can never reach. (b) *"or must now carry it"* — it reaches files that do not yet state the rule but now owe it, which is how a template gets swept in. (c) *"grep case-insensitively, trying several keys from widest to narrowest, and report the set you used"* — the anti-tautology clause, and the sharpest thing in the delta. A single narrow key returns only the file you just edited; the rule now says so procedurally instead of hoping. `home` is still defined only by apposition — sentence 1's "every place that states it" is the whole definition — but it held on one pass.

**`AGENTS.md:90` — the send-back paragraph. One pass, at the edge.** The closing sentence carries three obligations in one breath (execute the full requirement over its whole population · any quoted control is a floor · one free attack, reported either way). I read it once; a tired builder would read it twice. **What it buys:** it is the entire re-entry procedure in one place — new Built line in its own state-only commit, receipt quoting it, scenarios re-run at full population, free attack. It is the procedure I executed to produce this record, and I assembled it from this paragraph alone. *"reported either way"* is the load-bearing half: it removes the reason to bury an attack that found something.

**`AGENTS.md:111` — the states ladder. One pass to understand, two to locate.** Six sentences in one paragraph; the sufficient definition arrives as a colon clause with a dash clause inside it, mid-paragraph. My predecessor filed exactly this ("not to understand it, but to find it") and it is still true. **What it buys, and it is more than I expected:** it is the only place that says *"the first three states belong to each piece; Live belongs to the milestone."* Before reading it I would have marked a piece Live. It also lets a builder self-test for sufficient before spending a judge.

**`AGENTS.md:113` — the claims/numbers/new-words producers. One pass.** **What it buys:** *"carries the command that produced it and what it returned, written after the run, never from memory"* is the most mechanically useful sentence on the page — it converts every coverage claim into a one-command test, which is exactly what my free attack below is. *"A closure without runnable proof is an open item wearing a label"* is the best-written line in the delta. Locating complaint, not a reading one: four unrelated rules stacked under no heading.

**`judge/SKILL.md:92` — the population sentence. One pass now; my predecessor needed two.** The triad is glossed in place — *"every home of a rule, every file carrying a figure, every case of a defect's class"* — so the three members read as three kinds of population for three kinds of defect instead of three synonyms. That is a measured improvement in the thing that was measured. **What it buys:** it tells a judge how to size a control **before** writing it, and tells the builder the control is a floor.

**`judge/SKILL.md:59` — the sufficient sentence. One pass, cleanest of all four homes.** **What it buys:** it makes landing with open items legal and landing with silent ones illegal. That single distinction is what lets a judge land real work instead of route-backing forever, and it names where the item goes.

**Job 1 verdict:** eight sentences, eight one-pass reads, one at the edge (`:90`), one locating problem (`:111`), and one charged stumble — `fresh challenge` at `:62`.

---

### Job 2 — both planted fixtures, re-run against the fixed pages

**Fixture 1 — the one-sided rule edit: "Fixed the receipt rule in AGENTS.md."**

Premise re-checked at the corrected gloss:

```
grep -rnilE "literally say|Built line that covers" AGENTS.md .claude/skills templates
   -> AGENTS.md · .claude/skills/experience/SKILL.md · .claude/skills/judge/SKILL.md · templates/piece.md
```

Four homes. The edit names one.

**CONDEMNED**, `AGENTS.md:70`, at its current wording:

> "Before landing a new rule or changing one, find every place that states it or must now carry it: grep case-insensitively, trying several keys from widest to narrowest, and report the set you used. Land the same change in every home in one commit; the record carries the greps and everything they returned, each home marked changed or untouched. **A one-home fix is not a fix.**"

Four clauses fire independently: no grep reported, no key set reported, the change did not land in every home in one commit, and the record marks nothing. The last sentence condemns the line without interpretation. Second, weaker condemnation from `AGENTS.md:113` — the word *Fixed* is a closure claim carrying no command — which condemns the sentence at review, one round after `:70` condemns the edit.

**Fixture 2 — the site-scoped control: "Control: `grep -c 'stale figure' state.md` returns 0."**

**CONDEMNED**, `judge/SKILL.md:92`, at its current wording:

> "When you order a fix and quote a control, the control names its whole population — every home of a rule, **every file carrying a figure**, every case of a defect's class — **never only the site where the defect surfaced.** The builder executes the full requirement; the quoted control is its floor, not its scope."

The figure lives in three files; the control names the one it surfaced at. The middle clause condemns it verbatim, and the triad now names *"every file carrying a figure"* explicitly — a stale figure is not a rule, so the old `home`-only wording would have reached it only by stretch. It reaches it directly now.

**And the fixture is now defanged on the builder's side too**, which is the reach fix I was sent to confirm. Even with the bad control quoted, the builder is bound by `AGENTS.md:62` ("a quoted control is a floor, not the scope") and `AGENTS.md:90` ("executing the full requirement each states over its whole population, with any quoted control as its floor"). Two independent builder-page statements. The defect can no longer travel from a lazy judge into a one-file fix.

**Both fixtures condemned, each by a sentence quotable verbatim. Both arms of the piece's falsifiable prediction hold.**

---

### Job 3 — free skeptical attack: run the coverage record's own greps

**Chosen because** the union batch's commit message advertises *"the coverage record finally obeys the rule it certifies."* `AGENTS.md:113` gives me a one-command test for that claim: a coverage claim "carries the command that produced it and what it returned, written after the run, never from memory." So I ran the four commands the record quotes and compared to what it says they returned.

**FINDING — `work/three-producers.md:58` states a returned home that its own quoted command does not return.** *(should-fix)*

The record says:

> "- Rule 3 (`grep -rnilE "floor, not the scope|as its floor"`) → AGENTS.md — changed (both builder statements, step 5 and the send-back paragraph) · **judge/SKILL.md — changed (the population sentence)**."

under a header that fixes the meaning: *"each grep over AGENTS.md, all skills, and templates; every returned home listed and marked."* Run verbatim:

```
grep -rnilE "floor, not the scope|as its floor" AGENTS.md .claude/skills templates
   -> AGENTS.md
```

`judge/SKILL.md` is not returned. **The cause is a one-word drift the record papered over:** rule 3 has three homes in three phrasings — `AGENTS.md:62` "a floor, not **the** scope", `AGENTS.md:90` "as its floor", `judge:92` "its floor, not **its** scope". The record's key matched the two AGENTS.md wordings and missed the judge's by the article, then listed the judge's file anyway. Written from memory of the edit, not from the run. That is precisely what `AGENTS.md:113` forbids: *"carries the command that produced it and what it returned, written after the run, never from memory."*

**And the same record fails the discovery clause of the rule it certifies.** All four keys are strings this piece authored:

```
"one-home fix is not a fix"              -> AGENTS.md          (written by 77628d1)
"in the sense you mean"                  -> AGENTS.md          (written by 684e359)
"floor, not the scope|as its floor"      -> AGENTS.md
"delivers what it was shaped to deliver" -> AGENTS.md · judge/SKILL.md
```

A grep for the fix can only ever return files that already carry the fix. It cannot return an untouched home, so it cannot fail — and `AGENTS.md:68` already rules on that: *"A check counts only if it can show the failure it claims to prevent; a control that cannot fail proves nothing about the product."* Four coverage claims, four controls that cannot fail, zero homes marked untouched, and no wider key attempted — against a rule whose text says *"trying several keys from widest to narrowest, and report the set you used"* and *"each home marked changed or untouched."*

**Material consequence, not just form.** Running the rule as written surfaces a home the narrow keys hid:

```
grep -rniE "undefined|jargon|defines? it" AGENTS.md .claude/skills templates
   -> AGENTS.md:113 · .claude/skills/judge/SKILL.md:67
```

`judge:67` states the same rule in the judge's operative voice — "Undefined jargon that carries a rule is a defect" — without the sense-collision clause rule 2 was sharpened to add. I am **not** charging that judge:67 must change: the defect is committed by the author, and the builder's page is the right home for authoring discipline. I am charging that rule 1 requires this home to be **listed and marked untouched, with the reason**, and the narrow key meant nobody had to decide. That is the whole value of the widest-first clause, unclaimed by the record that certifies it.

**Why this matters more than its size.** This is the third consecutive round in which this piece's own record fails this piece's own rule — the sentence claiming coverage is the sentence that most needs the coverage discipline, and it has now been rewritten twice and failed twice. The repair is not another sentence; `AGENTS.md:70` already says everything needed. The repair is running it. **Repair:** re-run all four coverage claims widest-key-first, paste what each command actually returned, mark every returned home changed or untouched — including `judge:67` under rule 2 and all three phrasings under rule 3 — and fix rule 3's key to something that matches all three homes, e.g. `-iE "floor, not (the|its) scope|as its floor"`.

### Checked and clean

- **Step 5 and `:90` do not contradict each other.** Different wordings of the floor rule, same content; no builder could obey one and violate the other.
- **The `sufficient` definition is now findable by the grep its own rule prescribes.** `grep -ni "sufficient" .claude/skills/judge/SKILL.md` returns `:59`; the capital letter that hid it is neutralised by the case-insensitive clause at `:70`. The defect that routed the previous round is closed by the sentence written to close it.
- **The templates carry the new obligations.** `templates/state.md:17` — "Open items from landed pieces, each named with its destination." `templates/piece.md:31` — the Homes touched slot, "The greps used, every home they returned, each marked changed or untouched." The gap my predecessor filed as Finding 1 is closed at both files.
- **The fixture-1 gloss now tells its true corpus.** Four homes, verified by the command the gloss quotes.
- **Rule 1 reaches Fixture 1 and not Fixture 2; `judge:92` reaches both.** Correct division, unchanged from the first run, and the triad gloss is what earns it.

---

### Verdict (E1)

**Sufficient, with one should-fix and one small stumble.**

Eight changed sentences, eight one-pass reads, and each one buys a builder something I could name without the work file open. The two planted fixtures are condemned at the current wording by sentences I quoted verbatim without interpretation, and Fixture 2 is now condemned on the builder's side as well as the judge's — the reach failure that routed the last two rounds is closed where I can see it closed.

What I would fix before landing, both against the batch rather than the sentences:

1. **The coverage record at `work/three-producers.md:55–59`** states a home its quoted command does not return, and certifies four rules with four controls that cannot fail. The rule that condemns this is the rule the record is certifying. This is the third round of the same recursion, and the sentences are not the problem — the running is.
2. **`fresh challenge` at `AGENTS.md:62`** is an undefined rule word minted in the same batch that landed the rule against undefined rule words. One-word repair to the name the pages already carry.

I would build under these eight sentences.
