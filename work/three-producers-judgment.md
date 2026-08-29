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

---

## Final ruling, 2026-08-29, on 7bcaf95

**Same judge, same line.** Claude Code · Opus 5 (`claude-opus-5[1m]`) · session `d6f7954a-06b5-4a3f-a8d2-b18233750afd`. Built and tested none of it. Blind to the second judge I ordered in §8 — this line is taken independently, and divergence between the two is itself a finding to settle with evidence, not by seniority.

**Under judgment:** the piece at `7bcaf95` (fix batch `684e359`, state-only Built `8e9140e`, receipt `7bcaf95`), with the re-run record at `ebad884`. Every command below was run by me in this session and its return is quoted. Every page was read from disk at the commit under test.

**Ruling in one line: sufficient — the piece lands and releases as v5.4.0, on the conditions in §F inside the landing commit.** The four sentences deliver what the piece was shaped to deliver, and for the first time there is positive evidence that they *produce*: rule 1's grep now returns the home it could not find, rule 3 visibly changed how a fresh tester ran, rule 4 is the sentence I am executing to write this, and all four ship into a real installed product. What remains is reach residue of the same class — paste-sized, fully enumerated, and none of it a defect in any sentence. Structure is **straining** for the second consecutive ruling on this line, which fires `judge:63`: the next piece is the structural repair, and that is where the class goes.

---

## A. The re-entry chain — valid

Checked with git, not from the receipt's label.

| Check | Command | Return |
|---|---|---|
| Fix batch is one commit | `git show --stat 684e359` | 9 files; the five product files (`AGENTS.md`, `judge`, `experience`, both templates) plus `decisions.md`, `map.md`, `state.md`, the work file |
| Built line is state-only | `git show --stat 8e9140e` | `state.md` only, 2 insertions 1 deletion |
| The quote literally says **Built** | `git show 8e9140e:state.md \| grep -c 'the fixed pages are Built as of this commit'` | `1` |
| Receipt quotes that wording token for token | `git show 7bcaf95:work/three-producers.md \| grep -o 'says: "[^"]*"'` | `says: "the fixed pages are Built as of this commit"` |
| Order is a straight line | `git log --format='%h parent=%p'` | `ebad884←7bcaf95←8e9140e←684e359←99ac32a` |
| No product commit after the Built line | `git log 8e9140e..HEAD -- AGENTS.md .claude/skills templates bin CLAUDE.md README.md` | empty |
| Receipt before the re-run | `7bcaf95` 19:42:34 · `ebad884` 19:51:45 | ✓ |

The §1 hygiene note was not taken: `8e9140e`'s wording is again "as of **this** commit", which at HEAD resolves to a records-only commit. The receipt names `8e9140e`, so the check passes on the letter. Quote the wording you intend to keep — third time asked, not a finding.

## B. The nine routes, re-fired at my own hand

Not adopted from T2′. Every cell below is a command I ran at `HEAD` in this session.

| Route | Command | at `def1677` | at `HEAD` | |
|---|---|---|---|---|
| R1 | `diff <(git show cca7841:state.md \| sed -n 5p) <(git show HEAD:state.md \| sed -n 5p)` | identical | **DIFFERS** | green |
| R2 | `grep -c "Land + name" / "Keep the wide wall" / "Run it now" decisions.md` | 0 / 0 / 0 | **1 / 1 / 1** | green |
| R3 | `grep -ni "sufficient" .claude/skills/judge/SKILL.md` | 3, 73 (line 59 invisible) | **3, 59, 73** | green |
| R4 | `grep -c "population\|floor, not its scope" AGENTS.md` | 0 | **0** | **red on the floor** |
| R5 | `grep -c destination templates/state.md` ; `grep -c homes templates/piece.md` | 0 ; 0 | **1 ; 0** | half |
| R6 | `grep -ci "three producers" map.md` | 0 | **2** — row 7, sole `[live` marker, rows renumbered to 10 | green |
| R7 | `grep -c grep work/three-producers.md` | 0 (`$ grep`) | **6**, four of them quoted claims | green on the letter |
| R8 | `git ls-files work/three-producers-{T1,T2,judgment}.md` | T1 untracked | **all three tracked** | green |
| R9 | `grep -n preload state.md` | 0 | **line 13**, with the fix named | green |

**R3 in full, by rule 1's own prescribed procedure** — distinctive phrase, case-insensitive, over `AGENTS.md .claude/skills templates README.md state.md map.md`:

```
"one-home fix is not a fix"              → AGENTS.md
"grep for its distinctive phrase"        → AGENTS.md
"define it in its first sentence"        → AGENTS.md
"in the sense you mean"                  → AGENTS.md
"names its whole population"             → .claude/skills/judge/SKILL.md
"floor, not its scope"                   → .claude/skills/judge/SKILL.md
"as its floor"                           → AGENTS.md
"delivers what it was shaped to deliver" → AGENTS.md · judge/SKILL.md · state.md
```

The `sufficient` home was recovered by sharpening the rule, not by lowercasing the home — the harder and better of the two routes T2 offered. Fixture 1 is no longer reproduced by the sentence written to condemn it.

**Budgets, re-measured** (`git cat-file -s` summed over the installer's `SURFACE` list at `bin/speck-next.js:11`; always-read per `CONTRACT.md:34` = `AGENTS.md + state.md + product.md + map.md`):

```
ebb9fb5 56,039   caf557f 58,648   def1677 59,596   7bcaf95 60,210
installed:   17 files of 20 · 60,210 of 102,400 (58.8%)
always-read: 27,206 of 51,200 (53.1%)   [def1677: 25,738]
fix batch +614 B · the piece to date +1,562 B (+2.66% on caf557f)
```

`./devsuite/run.sh --control` → `control mode: 4 of 4 tasks went red (want: all)`. The instrument can still fail.

**R4 and R5, ruled rather than scored.** R4's quoted control is red and the requirement above it is met: `AGENTS.md:90` now reads *"executing the full requirement each states, with any quoted control as its floor"* — rule 3's builder half, on the builder's page, in different words. By the very sentence under judgment, the control is the floor and the requirement is the scope, so I rule the requirement met and the floor's redness a wording artifact — **except at `AGENTS.md:62`**, which was named in the original R4 alongside `:90`, was never touched (`git diff 99ac32a 7bcaf95 -- AGENTS.md | grep -c 'exact test scenarios'` → `0`), and still tells the builder to *"repeat the exact test scenarios."* That is step 5 of the numbered build loop — the line a builder reads first — and the word `exact` is the one the rule exists to correct. R5 closed rule 4's obligation into both skeletons (`templates/state.md` gained "destination"; `templates/piece.md`'s Result line gained "where each open item went") and closed rule 1's record obligation into neither (`grep -rniI home templates/` → `0`).

## C. Three free attacks of my own

Not T2′'s. Run because `AGENTS.md:90` now requires one and because a judge who only re-scores the routed list is grading his own homework.

**Attack 1 — a real-path run against the real dependency: install the product.** No tester on this piece has ever run the installer; both read the source tree. I installed `7bcaf95` into a fresh `git init` directory with `bin/speck-next.js install`.

```
Installed Speck Next v5.3.0 … 19 files on disk
all four sentences present in the installed tree:
  "one-home fix is not a fix"            → AGENTS.md
  "grep for its distinctive phrase"      → AGENTS.md
  "in the sense you mean"                → AGENTS.md
  "floor, not its scope"                 → .claude/skills/judge/SKILL.md
  "as its floor"                         → AGENTS.md
  "delivers what it was shaped to deliver" → AGENTS.md · judge/SKILL.md
  "where each open item went"            → templates/piece.md
  "from disk at the commit under test"   → .claude/skills/experience/SKILL.md
```

**Nothing was lost in transit, and 19 files is inside the 20-file limit.** This is the piece's first real-path run and it passes. It also catches one landing chore: the marker still writes `v5.3.0`, so `package.json` and `README.md:44` must be bumped in the landing commit or every installed product reports the wrong version.

**Attack 2 — rule 2 applied to the fix batch's own additions**, the same test the piece ran on its first build. Word-diff over `684e359`'s additions to the loaded surface, minus the full pre-image vocabulary at `def1677`, yields sixteen genuinely new tokens: `carrying · case-insensitively · disk · distinctive · executing · figure · host · keyword · mean · older · phrase · preload · sense · theirs · untouched · way`. Of these, one is rule-carrying: **"distinctive phrase"**, the grep key rule 1 now prescribes. It is glossed only by a negation ("not one keyword") and never says what makes a phrase distinctive. Census delta: **zero undefined, one thin.** Rule 2 survives its own sharpening — narrowly.

**Attack 3 — rule 1's *record* clause, applied to the fix batch's own record.** `AGENTS.md:70`, landed in `684e359`, requires: *"the record carries the grep and everything it returned, each home marked changed or untouched."* The same commit edited rule 3, which is stated in two places (`judge:92` and `AGENTS.md:90`).

```
$ grep -c untouched work/three-producers.md
0
$ grep -o 'grep [^·]*' work/three-producers.md | tail -4
grep -c "grep for its distinctive phrase" AGENTS.md` → 1
grep -c "in the sense you mean" AGENTS.md` → 1
grep -c "floor, not its scope" .claude/skills/judge/SKILL.md` → 1
grep -ci "delivers what it was shaped to deliver" AGENTS.md .claude/skills/judge/SKILL.md` → both files
```

Four single-file counts. None returns a home set; none marks a home changed or untouched; and rule 3's coverage claim names only `judge/SKILL.md` while the same commit created its second home at `AGENTS.md:90`. **The fix batch broke the record clause of the rule it was landing, on the rule it was editing.** This is the piece's own subject failing inside the piece for the second time, and it is the sharpest finding in this ruling.

**Two findings against myself, disclosed because they are evidence.** Looking for the definition of *ratified*, I ran `grep -n "Ratified means\|ratified" AGENTS.md` and got nothing at line 36 — the line reads `*Ratified* means`, and my keys missed it on an italic asterisk and a capital letter. Then, writing condition 2 of §F, I drafted `grep -c "eight bites" state.md map.md` and fired it: `map.md:1 state.md:0`, because `state.md:11` reads "**E**ight bites" — a control written by the judge naming this defect, in the ruling that names it, missing one of the two homes it was aimed at. That makes **four** independent instances in this review of a keyword grep missing a home it was pointed straight at (T1 returned three of four; T2′'s free attack returned three of four; mine returned zero of one and then one of two). It is the strongest evidence available that "distinctive phrase" needs a real definition, and half of it comes from the judge, unprompted, against himself.

## D. The owner's transcription — it answers the question, honestly

`decisions.md` now carries, as its newest entry:

> **2026-08-29 (post-v5.3.0) · Three owner calls, made by selecting from options put to him in the session (recorded here because a judge rightly refused to trust a citation to this file that this file did not carry).** … he selected **"Land + name what's open (Recommended)"** — the option text he was shown: *"A judge may land a piece while writing everything that stays open into state.md — where it went, who owns it. Both judgment lines recommend this…"* … **these are selections of drafted options, not his own phrasing, and are recorded as exactly that. Reopens if he re-words any of the three.**

`grep -c` on each of the three answer keys returns `1 / 1 / 1`; at `def1677` all three returned `0`. **Option 1 of §7 was taken, and executed better than I specified.** I asked for the words with a date; the entry gives the mechanism, the verbatim option text so the provenance is auditable end to end, the explicit limitation in its own voice, and a reopening condition. It does not launder a judges' recommendation as an owner's word — it quotes the option that says the judges recommended it, so any reader can see the chain: judges recommended → drafted as an option with costs → owner selected. That is the opposite of the failure I filed.

**The fourth sentence keeps its authority.** One reservation, and it is not this piece's fault: `AGENTS.md:36` says *"Ratified means the owner agreed in their own words in that phase's dated record… Nothing else counts,"* and a selection is not, literally, his own words. But the method's own conductor law requires asks to arrive as options with costs and a recommendation, and every decision entry in this repository records a selection — the v5.2.1 entry says so in as many words ("His picks on the judges' filed questions, verbatim from the answer sheet"). Those two sentences cannot both be satisfied by any real session. That is a defect in `AGENTS.md:36`, not in this transcription, which is the most honest entry in the file. It goes to the owner as one question (§G) and blocks nothing.

**What does remain is a label that outruns its record.** `work/three-producers.md:3` still says *"the owner's 2026-08-29 **ratifications**"* and `state.md:5` says *"the owner's **ruling** closed it"*, against a record that says "selections, not his own phrasing." The citation resolves and the reader is corrected on arrival, so this is an overclaim of one word in two places, not a false citation. Two word-swaps, in the landing commit.

## E. The four rulings, re-taken

**Works — kept.** At `def1677` this was check failed because two of four rules could not fire at their source. Both are now reachable and one is demonstrably firing. Evidence, all mine: the install round-trip above (first real-path run this piece has had); `grep -ni sufficient judge/SKILL.md` → `59` where it was invisible; the eight-phrase sweep in §B returning every home for seven of eight keys; control arm 4/4 red. And the behavioural evidence, which matters more than any grep: **T2′ ran the re-entry by executing full requirements over quoted controls and appending a free attack, said so in those words, and that manner produced nine findings the quoted controls could not have surfaced** — including G1's reasoning that "the requirement above the floor is arguably met while the floor itself stays red," which is rule 3's own distinction used as a live analytical tool by a context that had just read it. Honest caveat: my §6 ordered the free attack before `AGENTS.md:90` landed the same requirement, so the attack itself is over-determined; the *manner* is not.

**Delivers the promise — broken on promise 4, kept on 6 and 7.** Promise 6: the fix batch's additions read in one pass and the sharpenings T1 asked for landed. Promise 7: 17 files of 20, 60,210 B of 102,400, always-read 27,206 of 51,200 — all measured above. **Promise 4 is broken at HEAD on two counts, both fresh, both the strain biting again:**

- `state.md:11` and `map.md:16` both freeze the report-of-itself strain at **"eight bites"**. My own judgment confirmed at least three further bites of that exact strain (the false census line, the citation to a record that did not hold it, the uncommanded coverage claims), and T2′ found more. `AGENTS.md:108` requires how often each strain has bitten and `AGENTS.md:58` keys the twice-rule on that count. A measured number left standing through a rewrite that made it stale, in two homes, on the strain the piece exists to repair — this is fixture 1 and the strain's signature at once, and neither I nor T2 caught it in the first round.
- `state.md:27` claims the rules now reach their readers *"found by a case-insensitive grep the record carries."* The record carries no such grep (attack 3). The sentence claims exactly the thing rule 1 requires and the record does not do.

Both close in the landing commit, which rewrites `state.md` anyway. They are conditions, not open items.

**Good to use — kept.** Every sharpening I named landed: the `destination` collision I hit on first execution is closed by "in the sense you mean" at `AGENTS.md:113`; `judge:92`'s population triad is glossed into three concrete kinds ("every home of a rule, every file carrying a figure, every case of a defect's class"), which is the two-word gloss asked for, delivered as nine. The `AGENTS.md:62` forward pointer was recommended, not required, and was not taken — it is now part of a condition for a different reason.

**Quality hangs together — check failed.** Six of the seven workmanship defects from `def1677` are closed and verified above. What fails is not the count but the kind: **the piece's own subject failed inside its own fix batch, twice.** Rule 1's record clause was broken by the record of the commit that landed it (attack 3), and rule 3 landed in one of the two builder-page homes the judgment named, leaving `AGENTS.md:62`'s "exact" standing — a one-home fix inside the batch that closed the one-sided-edit fixture. Also open: `templates/piece.md` still carries no home-marking obligation, so every product installed from `templates/` starts without it; the fix batch's `+614 B` is recorded nowhere against promise 8; the stale-page law sits only on the tester's page while the judge was one of its three recorded bites, and its wording says "two testers on two pieces" against a strain line saying three and a fourth bite in `ebad884`. Strength elsewhere does not excuse this, and I am not grading on trend.

## F. Result — sufficient, and what the landing commit must carry

**Sufficient. The piece lands, `map.md` row 7 ticks, and the release goes out as v5.4.0.** Ruled on the sentence the piece itself wrote and I am bound by: *sufficient means the piece delivers what it was shaped to deliver — you may land it with open items, never silent ones.* It was shaped to land four sentences that stop three defect classes at their source. All four are on their named homes, all four ship into a real installed product, three of them have now been observed changing behaviour in a fresh context, and the fourth is the rule producing this ruling. The residue is real and none of it is a defect in a sentence.

I want the reason for landing rather than routing back a second time stated plainly, because it is a judgment and not an arithmetic: **routing back would be declining to execute the rule the piece landed, on the first piece where it applies.** A judge who will not use "land with open items named" when the open items are paste-sized, fully enumerated, and none of them touches the artifact under judgment has decided the sentence is decoration. That is precisely the failure this piece exists to stop.

**Conditions — inside the landing commit, each with its control.**

1. **`AGENTS.md:62` gets rule 3's builder half.** Control: `git diff <landing>^ <landing> -- AGENTS.md | grep -c 'exact test scenarios'` ≥ 1, and the new line does not contain the word "exact" as the scope of the re-run.
2. **The strain's bite count is true in both homes.** `state.md:11` and `map.md:16` carry the real count with the fresh bites named. Control: `grep -ci "eight bites" state.md map.md` → `0 0`. **I wrote this control case-sensitively first and fired it:** `grep -c "eight bites" state.md map.md` → `map.md:1 state.md:0`, because `state.md:11` reads "**E**ight bites". One of the two homes was invisible to a control written, in this ruling, by the judge naming that exact defect — the **fourth** instance in this review, and the second at my own hand. Rule 1's case-insensitivity clause is the only reason the corrected control works, which is the clearest evidence available that the clause was worth its bytes and that "distinctive phrase" still is not defined.
3. **`state.md:27`'s grep claim becomes true or goes away.** Either the record carries a home-set grep with each home marked changed or untouched, or the sentence stops claiming it. Control: `grep -c untouched work/three-producers.md` → ≥ 1, **or** the claim is gone from `state.md`.
4. **The record obeys rule 1's record clause.** The coverage claims in `work/three-producers.md` carry the distinctive-phrase grep and everything it returned, each home marked — including rule 3's second home at `AGENTS.md:90`, which the current record omits.
5. **`templates/piece.md` gains rule 1's record obligation** — one clause, so an installed product starts with it. Control: `grep -rniI "home" templates/` → ≥ 1.
6. **The label matches the record.** `work/three-producers.md:3` "ratifications" → "selections"; `state.md:5` "ruling" → "selection".
7. **The stale-page law's count is corrected** ("two testers on two pieces" → the true count, four bites including `ebad884`). Its placement is an open item, not a condition — see below.
8. **`state.md` lists the four Judged rulings separately**, per `AGENTS.md:111` and `:113`: works kept · delivers the promise broken on promise 4 (with the two conditions above marked closed) · good to use kept · quality hangs together check failed. Control: `grep -c "check failed" state.md` → ≥ 1.
9. **The costs are recorded** against promise 8: fix batch +614 B, piece total +1,562 B (+2.66%), installed 60,210 of 102,400, always-read 27,206 of 51,200 — each with the command that produced it.
10. **Version bumped to 5.4.0** in `package.json` and `README.md:44`, or the installer writes a false marker into every product.
11. **The release entry names what it considered deleting**, per promise 8.

**Open items — named in `state.md` with their destinations, per the sentence this piece landed.**

- **Rule 1 returns an incomplete home set on paraphrased homes.** Three independent demonstrations in this review (T1's three-of-four, T2′'s three-of-four on the receipt rule, my zero-of-one on `*Ratified*`), plus the case the fix batch minted itself: rule 3's two homes now read "floor, not its scope" and "as its floor" and share no distinctive phrase, so rule 1 cannot find both homes of the rule it landed beside. **Destination: the next piece** (below). Not a word-swap — it is the method question.
- **"Distinctive phrase" is glossed only by a negation.** **Destination: the next piece.**
- **The stale-page law lives only on the tester's page** while the judge was one of its recorded bites and `judge:10` licenses judges to re-run checks. **Destination: the next piece** — deciding which surfaces a new rule must reach is exactly the missing step, and doing it ad hoc here would be the behaviour under repair.
- **Fixture 1's gloss under-counts its own corpus** — "one home of three" against the receipt rule's four homes (`AGENTS.md:78 · judge:22 · templates/piece.md:15 · experience:18`). **Destination: the next piece's shaping**, since changing a committed control changes the control.
- **`AGENTS.md:36` vs. every decision entry in the repo.** **Destination: the owner** (§G).
- **The v5-era ordered runs on Pilot's build** — a real four-persona piece with a user interface, a full fresh-install lifecycle with one deliberately insufficient judgment sent back. Standing, unchanged.

## G. Structure — straining, twice in a row, and the trigger fires

`judge:63`: *"Two straining rulings in a row, or one fighting ruling, makes structural repair the next piece. The judge makes that call because the builder has momentum to protect."*

At `def1677` I ruled **straining** and named the strain: *the method has no step that makes a new rule reach the surfaces it must govern.* At `7bcaf95` the strain is unchanged and better evidenced — every remaining open item above is the same unasked question, and this time it was asked and missed *inside the fix for it*. Nothing was forced wrong and no workaround was needed, so it is straining and not fighting. That is two on this line, and I make the call: **structural repair is the next piece.**

In §5 I refused to manufacture this trigger from the previous piece's split lines. I do not have to now — it fires cleanly on this piece's own line, and it is the right answer for a reason `judge:63` anticipates: three consecutive fix batches on this piece would keep producing the same residue, because the missing step is not in this piece's scope. Promise 8 still forbids a fifth sentence. The repair is a step in the loop, not more law: when a rule changes or is minted, the record answers *which surfaces must now carry this* — which audience's page, which templates, which map row, which record field — and rule 1 already asks the near half of that question. Shaping owns the rest.

## H. For the owner — one question

**What this changes for you:** last round I could not find your words for the sentence that now decides when work is finished. That is fixed — `decisions.md` carries all three of your calls, the exact options you were shown, and an honest note that they were selections from drafted options rather than your own phrasing. Nothing is waiting on you for this piece to land.

**What I found while checking it.** The method page says a decision counts only when you agree *"in their own words. Nothing else counts."* But the method also requires us to bring you real options with costs and a recommendation — which is how you actually decide, and how every decision in this repository was made. Those two sentences contradict each other, and if the strict one is taken literally, half the decision record is unauthorized. That is a defect in the method page, not in any of your calls.

**Your options:**

1. **A selection counts (recommended).** The method page says so explicitly: a decision is ratified when you choose from options put to you in plain language, and the record keeps the option text you saw. Costs nothing, matches what already happens, and keeps the record honest about what a selection is. Every existing decision stays standing.
2. **Only your own wording counts.** The method page stays as it is, and we stop calling a selection a ratification anywhere — decisions get recorded as "the owner selected", and anything that must be *ratified* comes back to you for a sentence in your words. More friction on you, sharper authority on the few things that carry it.
3. **Split it.** Selections count for ordinary calls; the things that become law on the pages — like the `sufficient` sentence — need your own wording. Most decisions stay frictionless; the load-bearing ones cost you a sentence each.

## I. The second judge

Ordered in §8 and running blind to this line, for the reason given there: this piece edits the judge's own skill, and the sentence I executed to reach this ruling was written by the piece I am ruling on. That arrangement is exactly what a second, independent hearing exists to check. **If the second line rules differently on the Result, the divergence is a finding and it is settled with evidence, not by which line was written first** — and the specific place to look is whether landing with a "quality hangs together: check failed" ruling is faithful to the `sufficient` sentence or a judge stretching it. I have given my reason in §F in the plainest terms I can, so it can be attacked directly.

## Result

**Sufficient.** The piece lands and releases as **v5.4.0**, with the eleven conditions of §F carried inside the landing commit and the six open items of §F named in `state.md` with their destinations — the sentence this piece landed, executed to the letter on the first piece it governs. Structure: **straining**, twice on this line, so structural repair is the next piece.

**For the next builder, so it is not relearned:** the producers work — a rule reached a fresh tester and visibly changed how they ran, which is more than any of the last three pieces could show. What they cannot do is tell you where a rule must go, and a grep cannot find a home that was paraphrased or capitalised differently. Every failure left in this piece is that one gap, including the four separate greps in this review — two of them the judge's own, one of them inside the sentence naming the defect — that each missed a home they were pointed straight at.
