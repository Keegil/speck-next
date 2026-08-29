# Three producers — judgment

**Judge:** Claude Code · Opus 5 (`claude-opus-5[1m]`) · session `d6f7954a-06b5-4a3f-a8d2-b18233750afd` · 2026-08-29.
**Under judgment:** the piece "Three producers" at `def1677` (build `77628d1`, pre-build `caf557f`, Built line `fc33a7b`), with records through `5f93870`.
**Built and tested none of it.** Contact with the product ran through T1 and T2, plus checks I re-took myself — every command below was run in this session and its return is quoted.

**Ruling in one line: routed back to build.** The four sentences are sound and two of them already work in a stranger's hands. But the piece was shaped to stop three defect classes *at their source*, and at HEAD the sources are still open: rule 1's own grep cannot find the newest home of the rule it landed beside, rule 3 never reached the page the builder reads, and the session's own `state.md` carries two false statements — one of them a citation to an owner ruling that is not in the file it points to. I am the first judge to execute the `sufficient` sentence this piece wrote, and its second clause — *never silent ones* — is the clause the piece fails.

---

## 1. The receipt — valid

Checked with git, not from the receipt's own label.

| Check | Command | Return |
|---|---|---|
| Built line exists and says **Built** | `git show fc33a7b:state.md \| grep -c 'The live piece "Three producers" is Built as of this commit'` | `1` — literal, matches the receipt's quote token for token |
| Built commit contains nothing else | `git show --stat fc33a7b` | `state.md \| 2 +-` only |
| Written after the build | `77628d1` and `fc33a7b` both 19:20:55; `fc33a7b` is the child | ✓ |
| No build commit lands after it | `git log --format='%h' fc33a7b..HEAD -- AGENTS.md .claude/skills templates bin CLAUDE.md` | empty |
| Receipt opened after the Built line | `def1677` 19:21:25 > `fc33a7b` 19:20:55 | ✓ |
| Work file committed before product code | `git log --diff-filter=A -1 -- work/three-producers.md` → `caf557f` (19:19:14); first product commit `77628d1` (19:20:55) | ✓ different commits, shaping first |
| Receipt lists the planned probes, committed before they ran | `def1677` 19:21:25; T2's record committed `5f93870` 19:30:04 | ✓ |

**The state-truth commit between (`6c22d89`) does not invalidate anything.** It changes `state.md` and nothing else, and the skill's own definition settles it: a commit that changes only records or state is not a build commit. It rewrote the Built sentence into "Built as of commit fc33a7b", which still literally says Built and still names the piece, so nothing was weakened. One hygiene note for the next builder, not a defect: the receipt quotes the `fc33a7b` wording, and `state.md` at HEAD no longer reads that way. The receipt names its commit, so the check passes — but a judge who checks the quote against HEAD instead of the cited commit will see a mismatch. Quote the wording you intend to keep.

**T2's F8 is confirmed and is worth one sentence in the Result.** At `fc33a7b` the same paragraph says both *"The live piece 'Three producers' is Built as of this commit"* and *"**No piece is live.**"* The anchor a judge is told to read contradicts itself. It was healed at `6c22d89`. Nothing to fix at HEAD; write the Built line and its reconciliation in one thought next time.

---

## 2. What the testers found, and where I put pressure

Both records are real: every claim in each points at a command with its return or a passage read. No verdict claim was struck for pointing at nothing, with one exception noted below. Neither tester needed a re-run — the gaps I found were not gaps in their walks but questions neither was sent to ask.

### The disagreement, held open rather than averaged

T1, the cold reader, ruled **"sufficient, with one should-fix."** T2, the conservation prober, ruled **"conservation clean, self-application not clean"** and declined to rule.

They do not disagree about a single fact. They disagree about what the piece is. T1 judged the *sentences* — what a builder meets on the page — and found them sound, quotable, and immediately usable. T2 judged the *producers* — sentences measured by whether they changed behaviour at their first opportunity — and found the evidence negative in the author's own hands.

**Both are true, and the split is the piece's own subject.** T1 is right that a builder arriving at these pages tomorrow gets four good sentences. T2 is right that a rule which no one can reach is a sentence, not a producer. I rule with both: the text passes, the machinery does not yet.

### One verdict claim struck

**T2's F4 — "a cold reader still trips at line 62."** T2 is a conservation prober; no moment in T2's record shows anyone tripping at line 62, and the one actual cold reader on this roster read `AGENTS.md` in full and reported no such trip. T1's only slowdown at the `sufficient` site was *finding* it, not understanding it, and T1 then ruled a live case from it in four steps. The "trips" clause points at nothing lived, so it is struck.

What survives F4 is mechanical and real: `grep -n "sufficient" AGENTS.md` returns `62`, `88`, `98` before `111`. Rule 2's second branch ("use one these pages already define") is satisfied at HEAD, so this is not a rule-2 violation. It is a sharpening — a forward pointer at `:62` would cost four words — and I file it as such, not as a finding.

### Challenges I put, and what they returned

**To T1, on Finding 1 (the templates owe a home).** I asked whether this is really rule 1 firing, since rule 1 triggers on *changing a rule stated in more than one file* and `sufficient` had **zero** homes before this piece — nothing was changed, a definition was created. That objection holds, and it makes T1's framing wrong while making the finding stronger. The defect is not a one-sided edit. It is that the piece placed a **new obligation on `state.md`** ("names each item and its destination") and a **new obligation on the record** ("list the homes") without giving either a slot in the skeleton every downstream product starts from. Confirmed at my hand: `grep -c "destination" templates/state.md` → `0`; `grep -c "homes" templates/piece.md` → `0`. For this repo the obligation is discoverable in `AGENTS.md`. For every product installed from `templates/`, it does not exist.

I also re-ran T1's own grep wider and it found a home T1 missed — `README.md:26` states the four states too, so the rule has four homes, not three. A tester deliberately applying rule 1 under-counted the homes. That is not a knock on T1; it is the sharpest available evidence for T2's F3 below, and it arrived independently.

**To T1, on the `destination` collision.** I asked whether this is a real reader's problem or a philologist's. It is real, and I proved it by living it: `grep -n destination` over the loaded pages returns three hits, and the only one that gives the word an extension is `judge:75`, which enumerates four route-back destinations. Writing this judgment, I have open items on a piece I considered landing, and their destinations are *the owner*, *the fix batch*, and *a strain line* — not one of the four. **The first judge to execute the sentence hit the collision on first use.** T1 read it; I ran into it. Confirmed, and promoted from a reading to an executed finding.

**To T2, on F5 (rule 3 sits in a page the builder does not read).** T2 marked it PLAUSIBLE, reasoning that a wider control mechanically widens what a literal builder executes. That mitigation is fair and I credit it — the judge-side half does real work on its own. But the placement fact is harder than T2 tested: `grep -c "population\|floor, not its scope" AGENTS.md` → **`0`**. The builder's page carries none of rule 3, while `AGENTS.md:62` and `:90` still read scope-shaped ("repeat the exact test scenarios", "Re-run the exact scenarios the judge named"). The strain's named root cause is *builder* behaviour — "the judge's quoted control becomes the builder's requirement." The correcting clause landed only on the judge's page. **Upgraded to CONFIRMED** on placement, with T2's partial-producer reading kept.

**To both, on what neither was sent to check.** Two findings are mine, and both sit outside the jobs either tester was given.

---

## 3. Findings I take at my own hand

**J1 · CONFIRMED · the owner's ratification is not in the file that is cited for it.** This is the most serious finding in the review.

`state.md:22` reads: *"both of the definitions piece's questions were answered the same night (**his calls in decisions.md**)."* The work file's Consumes cites *"the owner's 2026-08-29 ratifications ('Land + name what's open' for `sufficient` · 'Run it now')."*

```
$ grep -c "Land + name\|Run it now\|stays wide" decisions.md
0
$ git log --format='%h %ci' -1 -- decisions.md
cca7841 2026-08-29 18:50:49 +0200        # 29 minutes BEFORE the piece was shaped (caf557f, 19:19:14)
```

Exhaustive grep across every `.md` in the repository finds the owner's answers to these two questions **nowhere** — not in `decisions.md`, not in `work/`, not anywhere. `decisions.md` was not touched by any commit in this piece's range. Its most recent entry records the two questions being *filed to the owner*, not answered.

This matters more than a missing transcription, for three reasons. First, `AGENTS.md:36` — the page this piece edits — says *"Ratified means the owner agreed in their own words in that phase's dated record."* By the repo's own law, a ratification with no dated record is not a ratification. Second, the sentence that landed is near-verbatim the recommendation **both previous judgment lines already proposed** (`work/name-the-words-judgment-1.md:652`), which is exactly how a judges' recommendation gets relabelled as an owner's word. Third, the whole fourth sentence — now law in two homes, and the rule I am executing right now — rests on this citation.

I do not conclude the owner said nothing. The likeliest reading by far is that he answered in the session and the transcription never happened; two commit messages say "ratified tonight" and "the owner's two answers recorded", and *recorded* is precisely the claim that fails. But I cannot tell which from the repository, the builder cannot decide it either, and the difference decides whether the sentence returns to shaping. It goes to the owner as a question (§7).

**J2 · CONFIRMED · the piece is not on the map.**

```
$ grep -ci "three producers" map.md
0
```

`map.md`'s header says "(in order — exactly one live)"; it lists nine pieces and marks none live. `AGENTS.md:56` says a ratified map has exactly one live piece. `state.md:26` calls this "the live piece". The piece that was shaped, built, and is being judged right now is invisible to the map. The repo's own precedent is unambiguous — `decisions.md` says of the previous piece, "the map re-cuts to admit it, shaped and live." This one skipped it.

**J3 · CONFIRMED · half the review's evidence is uncommitted.** `git ls-files work/three-producers-T1.md` → empty. The receipt links `[T1](three-producers-T1.md)`; at HEAD that link resolves to nothing for anyone outside this working tree. T2's record was committed at `5f93870`; T1's was not.

**J4 · the host-preloaded stale page has now bitten three contexts, and I am the third.** T1 disclosed it (Finding 3); the previous piece's cold reader disclosed it; my own host preloaded a v5.0-era `AGENTS.md` opening "# Speck Next" with a section called "The conductor — law in every session", which does not exist in the 127-line file on disk. Every reading in this judgment is from disk at the commit under test. Three contexts, three pieces, and a tester who trusts the loaded copy reviews a document one full rewrite out of date. Under promise 4, a strain with three bites belongs in `state.md`'s wearing-out list, and that part is mandatory. The one-line fix in `experience` and `judge` ("read the pages from disk at the commit under test") is cheap and I recommend it, but it costs bytes and I leave the call to the builder rather than mandating a sentence.

---

## 4. The four rulings

Each stands alone. None is allowed to carry another.

### Works — **check failed**, with the passing half named

*Passing, and it is not small.* T1 is a real-path run against the real dependency — a fresh agent that had never seen Speck, reading the pages from disk, obeying them. It condemned both planted fixtures quoting the new sentences verbatim, with the two rules dividing the work without overlapping, and computed a clean census delta mechanically (`git diff --word-diff=porcelain` over the additions, subtracted from a 1170-word pre-image vocabulary): sixteen new words, four rule-carrying, all four defined at first use, **zero undefined**. The piece's single falsifiable prediction — both fixtures condemned by a fresh reader citing the new sentences, census delta zero — **held on both arms**. I re-took the mechanical gates myself: the four sentences at five named sites; installed surface 58,648 → 59,596 bytes summed with `git cat-file -s` over the installer's file list, +948 exactly, fully accounted for by the two edited files; `./devsuite/run.sh --control` → `control mode: 4 of 4 tasks went red`. Every figure T2 recorded reproduced at my hand, including 56,039 at `ebb9fb5`.

*Failing.* Three of the four sentences cannot be reached where they must fire, each confirmed by a command:

```
$ grep -n "sufficient" .claude/skills/judge/SKILL.md
3:  description: … sends insufficient work back …
73: ### 6. Send insufficient work back
```

Rule 1 tells the next agent to "grep for its words and find every home." The definition landed at `judge:59` begins with a capital *S*, so the rule's newest home is invisible to its own prescribed procedure — and worse, the file *does* surface in a file-level sweep on the unrelated word "insufficient", so an agent opens it, greps inside, sees two hits that are both "insufficient", and concludes the judge does not carry the definition. The next change to `sufficient` made by an agent obeying rule 1 literally lands in one home. **That is fixture 1, reproduced by the rule written to condemn it.** T1's own under-count of the homes (three found, four exist) is independent evidence that the grep key is undefined.

```
$ grep -c "population\|floor, not its scope" AGENTS.md
0
$ grep -c "destination" templates/state.md ; grep -c "homes" templates/piece.md
0 / 0
```

Rule 3 addresses a builder defect with a sentence only the judge reads. Rules 1 and 4 place new obligations on `state.md` and on the record without a slot in either skeleton — so for every product installed from `templates/`, the obligations do not exist.

**Ruling: works as text, fails as machinery.** Rule 2 works. Rule 4 works where it is reachable — T1 ruled a live case from it in four steps, and I ruled from it here. Rules 1 and 3 do not yet fire at their source.

### Delivers the promise — **broken**, on promise 4

Judged against `CONTRACT.md`, which `product.md` names as the promises.

- **Promise 6 (fun to drive, in plain language) — kept.** Promise 6's own check is a fresh-reader test, and T1 is it: all four sentences read in one pass except `judge:92` at two, and T1 could say what each buys a builder. "Defective when written, not when a reader trips over it" was named the sharpest line in the delta. Best single piece of evidence in either record: T1 was handed a concrete landing case cold and ruled it from the pages alone, "including a discriminator for the hard version that I could not have drawn yesterday."
- **Promise 7 (small by law) — kept.** Verified at my hand: 17 files of 20; 59,596 bytes of 102,400 (58%); always-read 25,738 of 51,200 (50%).
- **Promise 4 (the state file tells the truth) — BROKEN at HEAD, twice, by this session's own writes.**

```
$ diff <(git show cca7841:state.md | sed -n '5p') <(git show HEAD:state.md | sed -n '5p')
(identical)
```

`state.md:5` still tells the owner that `sufficient` is "the owner's sentence to write (below)" — hours after he wrote it and it shipped at `77628d1`, with lines 22 and 26 of the same file saying the opposite, and its "(below)" pointer sending the reader straight into the contradiction. The commit that rewrote state (`6c22d89`, *"state tells tonight's truth"*) touched only the later sections. The fact had three homes in one file; the rewrite fixed two. That is fixture 1's exact class and the strain's own signature — *a corrected figure left standing in the file that outranks the corrected one* — committed in the session that landed the sentence condemning it.

And `state.md:22` cites `decisions.md` for an owner ruling `decisions.md` does not contain (J1). Promise 4's own words are *"Overclaiming is a bug."* A citation pointing at a record that does not hold the cited thing is its sharpest form.

**Ruling: broken.** Promise 6 kept, promise 7 kept, promise 4 broken. Promise 8's "considered deleting" line is not yet due — it comes with the release entry — and I name it as a landing condition below.

### Good to use — **kept**, with two sharpenings

Ruled from felt moments, not from my own reading. T1: all four read in one pass except `judge:92`; the two-pass cost resolved on use, when applying it to fixture 2 revealed that "every home, file, or case" is not three synonyms but three kinds of population for three kinds of defect. T1's closing is unambiguous: *"I would build under these four sentences."*

Against it, two named moments. `judge:92` cost a second pass and needs a two-word gloss, not a rewrite. And the `AGENTS.md:111` home is a colon-clause inside an already-long four-states sentence — T1 had to slow down to *find* it. Add the `destination` collision, which I hit on first execution: a reader who does what rule 2 tells them and looks for the word on the pages finds `judge:75`'s four route-backs, which fit an open item on a landed piece badly. T1's repair is one clause — *"or use one these pages already define **in the sense you mean**"* — and it turns a rule that cannot express its own likeliest failure into one that can.

**Ruling: kept.** The sentences are good to use where a reader meets them. The sharpenings are cheap and none of them blocks.

### Quality hangs together — **check failed**

This is the ruling the strong artifact is not allowed to carry, and it is where the piece fails hardest. Workmanship across the whole piece, not the sentences alone:

- two false statements live in `state.md` at HEAD (promise 4, above);
- the piece is absent from `map.md` (J2);
- T1's record is uncommitted, so half the evidence is invisible at HEAD (J3);
- both new obligations have no slot in the templates every product starts from;
- rule 3 is absent from the builder's page;
- rule 1's grep cannot find its own newest home;
- every coverage claim the piece makes about itself is uncommanded — `grep -c '\$ grep' work/three-producers.md` → `0`, while `state.md:26` claims "in both its homes" and the receipt claims "AGENTS.md ×3 sites, judge ×2 sites". Both claims are **true** — I verified them — but `AGENTS.md:113`, landed one release ago, requires exactly such claims to carry the command and its return. This is an evidence defect, not a false statement, and it is four pasted greps from closed.

Six of these seven are the piece's own subject matter, failing inside the repair. **Ruling: check failed.**

---

## 5. Structure — **straining**, and the strain has a name

The shape made the work incomplete while it stayed honest. Nothing was forced wrong, and no workaround was needed before anything could proceed, so this is not fighting.

**The strain: the method has no step that makes a new rule reach the surfaces it must govern.** Every reach failure in this review is one missing question, never asked because there is nowhere to ask it — *which audience's page does this rule's defect live on, which templates now owe it a slot, which map row, which record field?* Rule 1 asks "which files state this rule" and stops there. It has no words for "which files must now state it."

**The arithmetic, stated honestly rather than manufactured.** The previous piece's two judgment lines split on structure: line 1 ruled **sound** (`name-the-words-judgment-1.md:640`), line 2 ruled **straining** (`:498`). This piece has one judge, so there is no single line to inherit, and `judge:63`'s "two straining rulings in a row" trigger does **not** fire cleanly. I will not manufacture it.

But I will say plainly what the evidence asks for, and it is not what the last two judges asked for. Both previous benches converged on "producers, not another list." That was right, and this piece built them. **The answer to this strain is not a fifth sentence.** Promise 8 is explicit — *if the kernel ever seems to need a compliance layer for itself, that is the old disease knocking; stop and subtract.* Three producers landed 948 bytes and have not yet demonstrably fired once. The honest next move is to make the three that exist actually reach, and let *that* be the evidence before minting a fourth. That work is not a new piece; it is this piece's fix batch, below.

---

## 6. Sent back — to **build**

The piece keeps the live slot. `map.md` stays unticked (it never got ticked — see J2). `state.md` says what was ruled and where it routed. Every control below is quoted with **its whole population**, per the sentence this piece landed at `judge:92`: the quoted command is the floor, and the builder executes the requirement above it. Each was run by me at `def1677` and each is red.

**R1 · `state.md` tells the truth.**
Control (red now): `diff <(git show cca7841:state.md | sed -n '5p') <(git show HEAD:state.md | sed -n '5p')` → identical, i.e. the line survived a rewrite that made it false.
**Population: every claim in `state.md` whose truth changed at `77628d1` or later — all six sections, not the two lines I found.** Sweep them, and report the sweep.

**R2 · every citation resolves in the file it names.**
Control (red now): `grep -c "Land + name\|Run it now\|stays wide" decisions.md` → `0`, while `state.md:22` says his calls are there and `work/three-producers.md:3` quotes them as ratifications.
**Population: every "his calls in X" / "ratified" / "recorded in X" citation across `state.md`, `map.md`, `decisions.md`, and the work file.** Each must resolve to text that exists in the named file. Gated on the owner's answer in §7.

**R3 · every rule is findable by the procedure rule 1 prescribes.**
Control (red now): `grep -n "sufficient" .claude/skills/judge/SKILL.md` → returns only `3` and `73`, both "insufficient"; the definition at `59` is invisible.
**Population: all four sentences and every home of each — not only the `sufficient` pair.** For each, the rule's own keyword grep must return every home. Run the four greps and show the returns. T2's two repairs are the cheap route: lowercase the judge's home, and have rule 1 say what a home is greppable *by*.

**R4 · each rule sits on the page whose reader commits its defect.**
Control (red now): `grep -c "population\|floor, not its scope" AGENTS.md` → `0`, while the strain's named root cause is builder behaviour and `AGENTS.md:62`/`:90` still read scope-shaped.
**Population: all four sentences, each checked against which audience's page the defect it prevents is committed on.** Rule 3 is the one I found; check the other three yourself.

**R5 · a new obligation reaches the skeleton it falls on.**
Control (red now): `grep -c "destination" templates/state.md` → `0`; `grep -c "homes" templates/piece.md` → `0`.
**Population: all six templates, checked against every obligation this piece created.** Two are known; find the rest.

**R6 · the map names the live piece.**
Control (red now): `grep -ci "three producers" map.md` → `0`.
**Population: `map.md`'s pieces list and its live marker — and generally, every piece past Shaped named on the map with its state.**

**R7 · coverage claims carry their commands.**
Control (red now): `grep -c '\$ grep' work/three-producers.md` → `0`, against "in both its homes" and "AGENTS.md ×3 sites, judge ×2 sites".
**Population: every coverage claim and every measured number in the work file, `state.md`, and the receipt.** Per `AGENTS.md:113`, each carries the command and what it returned.

**R8 · every linked record exists at HEAD.**
Control (red at `def1677`, and this is its recorded return): `git ls-files work/three-producers-T1.md` → empty.
**Population: every record the receipt links.** I committed T1's record myself alongside this judgment rather than leave a review's evidence in an uncommitted file where a clean tree would destroy it. The control's pre-fix return is recorded above and the finding stands; what remains for the builder is the habit, not this one file.

**R9 · the host-page strain is recorded.** Promise 4 requires every strain with its bite count. Three bites, three contexts, three pieces (J4). Recording it is mandatory; the one-line fix in `experience`/`judge` is recommended and left to the builder's judgment on bytes.

**Recommended, not required (cheap and each named by a tester):** the `destination` clause on rule 2 ("in the sense you mean"); a two-word gloss on `judge:92`'s population triad; a forward pointer at `AGENTS.md:62`; T1's repair to rule 1's report clause, so the record shows the grep and every home it returned, marked edited or not-applicable.

**Before re-judging:** sweep siblings for the same problem first, then re-run **every** scenario named above plus one free skeptical attack of the tester's own choosing, reported whether it finds anything or not. The fix batch needs a new Built line covering the fixed files in its own state-only commit, and a new receipt quoting it.

---

## 7. For the owner — one question, and it decides how the fourth sentence lands

**What this changes for you:** the sentence defining when work is finished — *sufficient* — is now law on two pages, and it is the rule every future judgment runs on. The record says you ratified it last night. I cannot find your words anywhere in the repository, so I cannot tell whether the record is describing something you said or something the judges recommended.

**What I found.** `state.md` says your two answers are "his calls in decisions.md". `decisions.md` has neither, and it was last written half an hour before this piece was even started. The sentence that landed is nearly word-for-word what both of the previous piece's judges had already recommended. The likeliest explanation by a wide margin is that you answered in the session and nobody wrote it down — but "wrote it down" is exactly the thing being claimed, so I cannot settle it from the files.

**Your options:**

1. **You said it — transcribe it.** Your actual words for both answers (the `sufficient` definition and the protected-code wall) go into `decisions.md` with the date, the way every other call of yours is recorded, and `state.md`'s citation becomes true. The sentence stays as it is; this is a records fix in the batch above.
2. **You didn't say it, or not in those words.** Then the fourth sentence has no owner behind it and returns to shaping to be asked properly, with a plain-language rendering, before it governs anything. The other three sentences are unaffected and the fix batch proceeds without it.
3. **You said something different.** Tell us what, and the sentence is rewritten to it — same route as option 2, shorter.

Nothing else in the review waits on you. Everything else is the builder's to fix.

---

## 8. Second judge — not now, and here is why

I did not order one. The findings are all mechanically checkable and I re-took every one at my own hand — greps, byte sums, the dev suite's control arm, the git chain — so a second judge would spend a fresh context agreeing with arithmetic. Both testers converge on the facts and differ only on weight, which is a split I can hold open without a tiebreak. And a second judge earns most when a landing is being blessed; this piece is going back.

**The re-judgment after the fix batch gets a second judge, and the reason is specific.** That is where a landing gets blessed, and it is where the owner's answer to §7 arrives. It is also where the instrument-measuring-itself problem bites hardest: this piece edits the judge's own skill, and the sentence I executed to reach this ruling was written by the piece I am ruling on. One judge executing a rule its subject authored is exactly the arrangement a second, independent hearing exists to check. Give it its own receipt line, and treat any divergence from this judgment as a finding to settle with evidence.

---

## Result

**Routed back to build**, on the sentence this piece wrote: *sufficient means the piece delivers what it was shaped to deliver — you may land it with open items, never silent ones.* It was shaped to stop three defect classes at their source. Two sentences reach their source; two do not, and the piece's own records fail the second clause outright — not silent, but false, in the state file at HEAD.

None of that is an argument against the sentences. T1's judgment stands and I adopt it: these are good sentences, a fresh reader condemned both planted fixtures quoting them verbatim, and one of them let a stranger rule a real landing case from the pages alone. Nothing here needs rewriting. The work left is reach — nine controls, every one of them a paste or a line, and the biggest is a question for the owner.

**For the next builder, so it is not relearned:** a rule is not landed when it is written, it is landed when it can be found. Every one of the nine failures above is the same missing question — *which surface must now carry this?* — and rule 1, the sentence written to ask it, asks only which surfaces already do. That gap is the strain, and closing it is worth more than a fifth sentence.
