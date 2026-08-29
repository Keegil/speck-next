# Three producers — second judgment (blind)

**Receipt line.** Claude Code · Opus 5 (`claude-opus-5[1m]`) · fresh context, built none of it and tested none of it · 2026-08-29 · piece "Three producers" at `ebad884`, fix build `684e359`, Built line `8e9140e`, re-entry receipt `7bcaf95`.

**Blind by order of the first judge.** I did not open `work/three-producers-judgment.md` or its continuation. I read the piece file (`work/three-producers.md`), both tester records in full including T2′, the two diffs (`caf557f..77628d1`, `def1677..684e359`), and every page from disk at `ebad884`. Where the piece file quotes the first judgment's rulings, I read that quote and formed my own view; I say so at each point. My disagreement with the first line is in §6 and is itself a finding, per `judge:88`.

**Disclosure — the stale-page trap fired on me. This is its fifth bite, and its second on a judge.** My host preloaded an `AGENTS.md` containing a section called "The conductor — law in every session." No such section exists on disk. `git log -S"The conductor — law in every session" -- AGENTS.md` returns `e5494cf` and `5d67cac`: my copy predates the builder's-words rewrite, a full rewrite out of date. I read every page with `Read` against the working tree at `ebad884` instead. `state.md:13` records this strain at "three bites"; T2′ was the fourth and disclosed it; I am the fifth. The law that would have warned me — "Testers read every page from disk at the commit under test" — landed only at `experience/SKILL.md:14`. `grep -rniI "from disk|your host|preload" .claude/skills/judge/SKILL.md` → **0 hits**. I was not covered by it. I caught it only because both testers disclosed theirs first.

---

## 1. The receipt — valid, both chains, proved with git

`judge:20–30` and `AGENTS.md:78–80`. I proved both chains myself rather than accepting either receipt's own account.

**Chain 1 (original build).**

| Commit | Touches | Class |
|---|---|---|
| `caf557f` | `work/three-producers.md` only | shaping |
| `77628d1` | `AGENTS.md`, `judge/SKILL.md` | **build** |
| `fc33a7b` | `state.md` only | Built line |
| `6c22d89` | `state.md` only | records |
| `def1677` | `work/three-producers.md` only | receipt |

`git show fc33a7b:state.md | grep -c 'The live piece "Three producers" is Built as of this commit'` → **1**, literal, says **Built**, at line 31. `git log --oneline fc33a7b..def1677 -- AGENTS.md .claude/skills templates bin CLAUDE.md` → **empty**: no build commit lands after the line. `6c22d89` changes only `state.md` and is not a build commit per `AGENTS.md:78`. **Valid.**

**Chain 2 (the fix, and the one I rule on).**

| Commit | Touches | Class |
|---|---|---|
| `684e359` | `AGENTS.md`, `judge`, `experience`, `templates/{piece,state}.md` + `decisions.md`, `map.md`, `state.md`, work file | **build** (mixed) |
| `8e9140e` | `state.md` only | Built line |
| `7bcaf95` | `work/three-producers.md` only | re-entry receipt |
| `ebad884` | `work/three-producers-T2.md` only | record |

`git show 8e9140e:state.md | grep -c 'the fixed pages are Built as of this commit'` → **1**, literal, says **Built**, at line 27, covering the fixed product files. `git log --oneline 8e9140e..HEAD -- AGENTS.md .claude/skills templates bin CLAUDE.md` → **empty**. The Built line is a records-only commit immediately after the build, exactly as `judge:28` permits, and the receipt opened after it. **Valid.**

**`judge:71`'s three cheap git questions, all clean.** `git log --diff-filter=A -1 -- work/three-producers.md` → `caf557f`, which precedes the first product commit `77628d1` — the file shaped the work, it did not document it. Every review past Built has a receipt committed before it ran (four receipt fields in the work file, both verified above). `map.md` has exactly one `[live]` marker and it is row 7, Three producers — matching reality.

One blemish at the chain-1 anchor, already healed and not disqualifying: at `fc33a7b`, `state.md:31` says both "is **Built** as of this commit" and "**No piece is live.**" in one paragraph. A judge following `judge:28` to the anchor commit reads a contradiction. Reconciled at `6c22d89`. T2 filed it as F8; I confirm it and agree it invalidates nothing.

---

## 2. The records, and what I struck

Both testers' records read in full, verdicts last, per `judge:32`.

**T1 (cold reader, at `def1677`).** Verdict: *sufficient, with one should-fix.* Every claim points to a moment: the mechanical census (`git diff --word-diff=porcelain`, 1170-word pre-image, sixteen new words), both fixtures condemned with the condemning sentence quoted, and a live landing case ruled from the pages alone in four steps. Nothing struck.

**T2 (conservation prober, at `def1677`) and T2′ (re-run, at `7bcaf95`).** Verdict: *conservation clean, self-application not clean.* Token-by-token subsequence proof, budgets with commands, nine routes each executed. Nothing struck for want of a moment.

**Two claims struck on their inference, not their evidence** — both from T2′'s free attack, and both are why a blind second judge earns its cost. T2′ concluded that rule 1 structurally cannot find a rule's homes. I re-ran the procedure with better-chosen keys and it does:

```
grep -rniIl "Built line" AGENTS.md .claude/skills templates
  → AGENTS.md · experience/SKILL.md · judge/SKILL.md · templates/piece.md      (4 of 4 homes)
grep -rniIl "quoted control" AGENTS.md .claude/skills templates
  → AGENTS.md · judge/SKILL.md                                                  (2 of 2 homes)
```

T2′ tested `"literally say"` (3 of 4) and `"floor, not its scope"` (1 of 2), and generalised from two unlucky key choices to a structural claim. **Struck.** Rule 1's procedure works on both real corpora anyone has pointed it at. That materially rehabilitates the piece's central sentence, and no other context in this review had established it.

---

## 3. Challenging the favourable verdicts hardest

**T1 said all four sentences read in one pass. I do not accept that at HEAD.** T1 read `def1677`. The fix batch materially rewrote two of the four surfaces T1 graded: rule 1 gained a case-insensitivity clause, a keyword prohibition, and a record obligation; `AGENTS.md:90` was rewritten from one clause into three. T1's one-pass finding covers rules 2 and 4 (byte-identical at HEAD) and no longer covers rule 1 as written. Nobody has cold-read the fixed text. I will not substitute my own reading — `judge:67` wants cold-reader testimony on this exact question, and `judge:12` forbids ruling on a gap. Ordered as a run in §7.

**T2′ said "six routes closed clean."** I re-ran all nine. Six do close at my hand. But R4 is not a near-miss to be filed and moved past — it is the piece's own rule turned on the piece, and I weigh it in §5 accordingly.

**T1 confirmed fixture 1's premise and moved on. It should not have.** T1 ran `grep -rln "receipt"`, got eight files, and wrote "premise confirmed: at minimum three homes, in fact more." The fixture's committed gloss says the receipt rule "also lives in the experience skill and the piece template; the edit touched **one home of three**." The rule has **four** homes across four files — `AGENTS.md:78,80`, `judge:22,28,30`, `experience:18`, `templates/piece.md:15` — and the one the gloss omits is `judge/SKILL.md`, which both judgments have themselves cited as a home. T2′ caught the undercount; T1 had the evidence in hand and let it pass. This is a defect in a **committed, re-runnable control**, in a piece whose rule 3 is *a control names its whole population*.

**The strongest thing said for the piece, and it holds.** T1 was handed a concrete landing case cold and ruled it from the pages alone in four steps, drawing a discriminator (`judge:84`'s "a decision the builder cannot make") that separates an owner question from a build defect. That is rule 4 working on a real path, on text unchanged at HEAD. It stands.

---

## 4. Disagreement held side by side

T1 says *sufficient*; T2 says *the sentences are sound and the evidence that they change behaviour is negative in their own author's hands*. Both are true and I do not average them (`judge:40`). They are true of different things: **T1 judged the sentences; T2 judged the session that wrote them.** The sentences survive every test anyone has put to them. The session that landed them broke them repeatedly. That split is the whole ruling, and it traces to one moment neither tester had to guess at — the fix batch was handed named sites and swept some of them.

---

## 5. The rulings

### Promises

- **Promise 3 — judged like a user, challenged like a claim, never by the builder: kept.** Two fresh non-builder testers, receipts committed before each run, this judgment blind and fresh, second judge ordered as the map's proof plan requires.
- **Promise 4 — the state file tells the truth: broken.** Four counts, each re-measured at my hand.
  - `state.md:27` claims the four sentences "now reach the readers who commit their defects." False for rule 3: `AGENTS.md:62` — step 5 of the build loop, the first statement of the rule a builder reads — still reads "repeat the exact test scenarios plus the required fresh challenge," with no floor language. `git diff def1677 HEAD -- AGENTS.md | grep -c 'exact test scenarios'` → **0**: untouched.
  - The same sentence claims they are "found by a case-insensitive grep the record carries." The record's four greps are single-file counts (`grep -c … AGENTS.md`); none returns a home set and none marks a home changed or untouched, which is what rule 1 now demands of the record. A done-everywhere-shaped claim carrying no qualifying command, against `AGENTS.md:113`.
  - Strain counts are stale in two homes. "Eight bites" stands at `state.md:11` **and** `map.md:16` after a review that produced more; "Three bites" stands at `state.md:13` when T2′ was the fourth and this judgment is the fifth. `AGENTS.md:108` requires how often each strain has bitten, and `AGENTS.md:58`'s next-piece rule keys on that count — a frozen count silently disarms the trigger.
  - `state.md:23` reads "Nothing waiting" while the previous judgment's three-option owner question was closed by the builder selecting option 1, with no owner response anywhere in the tree.
  - What *did* close: `state.md:5` is corrected and no longer byte-identical to `cca7841` — I diffed both. R1 is genuinely green.
- **Promise 6 — fun to drive, in plain language: kept in part, not judged yet in part.** Kept for rules 2 and 4 on T1's testimony (one pass each, and T1 could say what each buys). **Not judged yet** for rule 1 and `AGENTS.md:90` as rewritten: no fresh reader has read them, and they are the two densest sentences on the page.
- **Promise 7 — small by law: kept.** Re-measured at my hand with `git cat-file -s` summed over the installer's own list at `bin/speck-next.js:11`:

  ```
  ebb9fb5 56,039 · cca7841/caf557f 58,648 · def1677 59,596 · 7bcaf95/HEAD 60,210
  installed:   17 files of 20 · 60,210 of 102,400  (58.8%)
  always-read: 27,206 of 51,200                    (53.1%)
  fix batch +614 B · piece to date +1,562 B (+2.66% on caf557f)
  ```

  The v5.2.0 figure of 56,039 reproduces exactly, so the measured-numbers convention is holding across four commits and three independent hands.
- **Promise 8 — it cannot quietly grow back: broken, narrowly.** The fix batch's own cost is recorded nowhere: `grep -rn "614" state.md work/three-producers.md decisions.md capabilities.md` → nothing. The first build's +948 B was measured by two contexts; the second build's by none, in a piece whose live strain is byte-exact self-measurement and whose neighbouring rule requires every measured number to carry its command. Minor and honest, noted not charged: `capabilities.md:7` pins `AGENTS.md`'s cost to "~11.4 KB, measured at v5.2.0" (11,432 B at `ebb9fb5`, correct); the file is 13,965 B at HEAD, 22% larger. Pinned, so not false — but promise 8's own instrument now reports a smaller kernel than exists.

### The four

**Works — check failed.**

What fires on the real path, verified by execution rather than reading:

- **Rule 4 works.** T1 ruled a live landing case from it in four steps. It also bound this judgment: I ruled sufficiency by its two-part test, and its "never silent ones" clause is what made `state.md`'s overclaims dispositive rather than cosmetic.
- **Rule 3's judge half works, and it worked on me.** The first judgment quoted `grep -c "population\|floor, not its scope" AGENTS.md` → 0 as a control. Rule 3 told me that control is a *floor, not a scope*, so I checked both the floor and the requirement above it and reported them separately. Without the sentence I would have reported one or the other. That is a sentence changing a judge's behaviour, observed in the act.
- **Rule 2 works.** T1's census delta: sixteen new words, four rule-carrying, all four defined at first use. The `destination` collision T1 found is closed by the added clause "in the sense you mean." Zero undefined rule words in the delta, at two hands.
- **Rule 1's procedure works when the key is well chosen** — my §2 refutation: 4 of 4 and 2 of 2.

What fails:

- **Rule 1 forbids the key that would have worked on the very rule under repair.** The sentence says "grep for its distinctive phrase — case-insensitively, **not one keyword**." The two builder-page statements of the send-back rule are `AGENTS.md:62` and `:90`. On the pre-fix tree, the multi-word phrases each return one line — `"exact scenarios"` → 90, `"exact test scenarios"` → 62 — and the single key that returns **both** is `scenarios` → 62, 90. Rule 1 steered its own author away from the only key that finds both homes. This is not a builder excuse; it is a defect in the sentence, cheap to fix, and it explains the miss instead of merely condemning it.
- **Rule 3's builder half reached one of the builder's two statements.** `:90` has it; `:62` does not; the previous judgment named both.
- **R4's quoted control never went green.** `grep -c "population" AGENTS.md` → **0**; `grep -c "floor, not its scope" AGENTS.md` → **0**, at my hand. The requirement is arguably met at `:90` ("with any quoted control as its floor"), but the piece's own sentence calls the quoted control a **floor** — a minimum — and a floor left red is a minimum not met. The piece's rule, applied to the piece, fails.

**Delivers the promise — broken.** Ruled against `product.md` and `CONTRACT.md`, not the work file. Promise 4 broken on four counts; promise 8 broken narrowly; promise 6 only partly judged. The shaped outcome splits: the artifact half delivered — four sentences at their five named homes, findable at my hand, both fixtures condemned by a fresh reader quoting them verbatim, census delta zero, the falsifiable prediction holding on both arms. The effect half did not. The outcome sentence claims each rule "stops a defect class at its source instead of catching it a round later," and the batch built to deliver that stopped nothing at its source: the class fired at R4, at `:62`, in the record's own coverage greps, in the templates, and in two stale strain counts — after a judgment had named the sites.

**Good to use — kept in part, not judged yet in part.** Kept on T1's felt moments for rules 2 and 4: read in one pass, and T1 could name what each buys a builder without the work file open. Not judged yet for rule 1 and `AGENTS.md:90` as rewritten — no tester has read them and I will not rule felt experience from my own reading.

**Quality hangs together — check failed.** Nine workmanship defects, seven of them the piece's own subject matter, and no strength excuses them (`judge:59`):

1. R4's quoted control never green.
2. `AGENTS.md:62` — a site the previous judgment named, unswept.
3. Fixture 1's committed gloss undercounts its own corpus: three homes claimed, four found.
4. Rule 1 forbids the key that finds both homes of the rule under repair.
5. The record's four coverage greps do not meet rule 1's own record obligation — single-file counts, no home set, nothing marked changed or untouched.
6. `grep -rci "home" templates/` → **0 across all six skeletons.** Rule 1's record obligation was *widened* by this batch and has no slot in the template every installed product starts from.
7. Two stale strain counts in three homes.
8. The fix batch's +614 B recorded nowhere.
9. The stale-page law landed on the tester's page only, while the reader it has now bitten twice — the judge — is not addressed. `grep` on `judge/SKILL.md` → 0. Its wording also under-counts its own strain ("two testers on two pieces" against `state.md:13`'s three bites, now five).

---

## 6. The structure — sound, and I disagree with the first line

I rule the structure **sound**, and I record the disagreement plainly because `judge:88` and `AGENTS.md:96` make divergence between two judges a finding in itself, to be resolved with evidence and never by rank.

The piece file quotes the first judgment ruling the structure **straining**, on the grounds that "the method has no step that makes a new rule reach the surfaces it must govern." I verified that gap exists and it is real: `grep -rniI "which surfaces|which pages|where the rule|new rule|must govern|carry the rule" AGENTS.md .claude/skills templates` → **zero hits**. Rule 1's trigger is "*Before changing* a rule that is stated in more than one place," so a brand-new rule — which has no homes yet — never fires it. That gap produced findings 6 and 9 above.

I disagree that this is a *structural* strain. `judge:63` defines straining as the shape making the work slower or riskier while the work stayed honest. The shape did neither here. It caught a false citation to `decisions.md`, a false line in `state.md`, and seven reach defects, across two rounds, through its own machinery, using fresh contexts that had built none of it — and it caught the second round's defects at the same rate as the first, which is what a working review looks like when a fix batch is imperfect. The missing step is a gap in the **artifact**, which happens to be a method; it is a build finding, not a verdict on the shape that governed the work. Ruling it straining a second time would trip `judge:63`'s two-in-a-row clause and make structural repair the next piece — and I will not manufacture that arithmetic out of a defect I can route to build.

The repair is not a fifth sentence, which promise 8 forbids. It is inside rule 1's existing sentence: widen its trigger from *changing* to *landing or changing*, drop the "not one keyword" prohibition in favour of trying several keys widest-first, and make the record show the keys and the full returned set with each home marked. Same sentence, no net growth.

Read against standing decisions (`judge:65`): the four sentences contradict nothing in `decisions.md`, `CONTRACT.md`, or the other four skills — I swept `sufficient`, `population`, `floor`, `quoted control`, and `Built line` across the whole installed surface. The dev suite control arm is honest: `./devsuite/run.sh --control` → **4 of 4 tasks went red**, at my own hand. The suite can still express failure.

---

## 7. Routed back to build

**Not sufficient.** Under the piece's own definition — *sufficient means the piece delivers what it was shaped to deliver* — the four sentences are delivered and the effect they were shaped to produce is not. The deciding fact is not any single defect but this one: **the previous judgment named `AGENTS.md:62` and `:90`; the batch fixed `:90` and left `:62`.** A one-home fix, committed by the piece whose first sentence is *a one-home fix is not a fix*, one round after being told, at a site that was named. That is the class the piece exists to abolish, and it is still authoring itself.

The piece keeps the live slot. `map.md` stays unticked. Destination: **build** for B1–B8, plus **one more round of experiencing** for E1, which is thin evidence and not a build defect (`judge:80`).

Each control below names its whole population, and per rule 3 the control is the floor, not the scope — execute the requirement stated in the sentence, not only the grep.

- **B1 · Rule 3 reaches both builder-page statements.** Population: every statement of the send-back rule on the builder's page — `AGENTS.md:62` and `:90` — not only the one this control greps. Floor: `grep -c "as its floor\|floor, not its scope" AGENTS.md` → currently **1**, want ≥ 2, with `:62` among the hits. Then close R4 honestly: either land the population language on the builder's page so `grep -c "population" AGENTS.md` → ≥ 1, or state in the record why the floor is retired and what replaced it. A quoted control is not closed by doing something else instead.
- **B2 · Rule 1 stops forbidding the key that works.** Replace "not one keyword" with guidance that survives its own corpus: try several keys, widest first, and report the set. Floor: on the pre-fix tree, `grep -niI "scenarios" AGENTS.md` returns 62 and 90 while every multi-word phrase returns one — the new wording must permit the key that found both. Population: rule 1's every home (`grep -rniIl "one-home fix is not a fix"` → currently `AGENTS.md` alone; confirm that is the whole set before editing).
- **B3 · Rule 1's trigger admits new rules.** "Before *changing* a rule stated in more than one place" never fires for a rule being landed for the first time, which is how findings 6 and 9 happened. Widen to landing-or-changing. Floor: `grep -c "landing or changing\|Before landing" AGENTS.md` → currently **0**. No fifth sentence — this is an edit to rule 1.
- **B4 · Fixture 1 states its true population.** The committed gloss says "one home of three." Population: every file stating the receipt/Built rule — `AGENTS.md`, `judge/SKILL.md`, `experience/SKILL.md`, `templates/piece.md`. Floor: `grep -c "one home of three" work/three-producers.md` → currently **1**, want **0**, replaced by the four-home count with the grep that produced it (`grep -rniIl "Built line" AGENTS.md .claude/skills templates` → 4 files). A re-runnable control that misstates its own corpus is not a control.
- **B5 · The record meets rule 1's own record obligation.** Population: all four coverage claims in `work/three-producers.md`, not one. Floor: each claim carries a grep that returns a home **set** across `AGENTS.md .claude/skills templates`, with every home marked changed, added, or untouched — currently zero of four do.
- **B6 · The templates carry the homes slot.** Floor: `grep -rci "home" templates/` → currently **0** across all six; want ≥ 1 in `templates/piece.md`. Population: every skeleton whose file inherits a rule-1 obligation. Every product installed from `templates/` starts without this today.
- **B7 · The stale-page law reaches the judge, and its counts are true.** Population: every page whose reader has committed this defect — `experience/SKILL.md` has it; `judge/SKILL.md` does not (`grep` → 0), and the judge is now two of the five bites. Floor: `grep -rciI "from disk" .claude/skills/judge/SKILL.md` → ≥ 1. Fix the law's own undercount ("two testers on two pieces") in the same commit.
- **B8 · `state.md` tells the truth about this piece.** Population: every claim in `state.md` about this piece and every strain count in every home. Floors: the "reach the readers who commit their defects" and "found by a case-insensitive grep the record carries" claims either carry their commands or come down; `state.md:11` **and** `map.md:16` both move off "eight bites"; `state.md:13` moves off "three bites" to five; `state.md:23` stops saying "Nothing waiting" while §9 is open; and the piece's honest current status — a judgment ruling works *check failed*, delivers *broken*, quality *check failed* — appears in the file, since `grep -ci "check failed\|not judged yet" state.md` → **0** today. Record the fix batch's +614 B with its command.
- **E1 · One fresh cold reader on the changed sentences.** Thin evidence, so this returns to experience, not build. Scenario, exactly: a fresh non-builder context that has not seen this piece reads `AGENTS.md:70`, `:90`, `:113`, `:111` and `judge/SKILL.md:59`, `:92` from disk at the re-fixed commit, one pass each, and reports for each — did it read in one pass, and what does it buy a builder? Rules 2 and 4 are byte-identical to what T1 graded; rule 1 and `:90` are not, and nobody has read them. Then re-run both planted fixtures against the fixed text, since the sentence that condemned fixture 1 has been rewritten since it was last watched condemning anything.

Per `AGENTS.md:90`, the re-run executes the full requirement each of these states with the quoted control as its floor, plus one free skeptical attack of the tester's own choosing, reported either way. Write a new Built line for the fixed files in its own state-only commit and have the next receipt quote it.

---

## 8. Where the piece's own sentences bound me

Asked for, and worth recording, because this is the piece's product being used on the piece.

- **Rule 3** changed a ruling. The first judgment handed me R4 as a quoted control returning 0. Rule 3 told me the control is a floor and the requirement is the sentence above it, so I reported both — floor red, requirement arguably met at `:90` — instead of collapsing to one. Without the sentence I would have written a cleaner and less true line.
- **Rule 4** is the test I ruled by. "Delivers what it was shaped to deliver, with every open item and its destination named" is what let me separate the artifact half (delivered) from the effect half (not), and its "never silent ones" clause is why `state.md`'s omissions are a ruling and not a nit.
- **Rule 1** produced my two best findings by being executed rather than read. Running its procedure is what refuted T2′'s structural claim, and running it on its own corpus is what exposed the "not one keyword" defect.
- **Rule 2** bound my own writing: I introduce no rule-carrying word here that these pages do not already define.
- **`AGENTS.md:68`** — a control that cannot fail proves nothing — is why I ran the control arm myself (4/4 red) rather than citing T2′'s run.
- **`judge:12`** stopped me twice: I did not rule promise 6 or "good to use" on the changed sentences, because no fresh reader has read them, and a judge's own reading is not cold-reader testimony.

---

## 9. For the owner — one question, and it is not blocking

*What this changes for you:* nothing about the product's behaviour. It changes what the word **ratified** means in your repository, and whether one sentence that now governs every future judgment counts as yours.

*What I found:* the method page says "*Ratified* means the owner agreed **in their own words**." Your three calls from 29 August are recorded in `decisions.md` as selections you made from options an agent drafted, with the option text quoted — and the entry says so in as many words: *"these are selections of drafted options, not his own phrasing."* That is honest, and it is the right way to record it. But two other files call the same thing something stronger: the piece's work file says "the owner's 2026-08-29 **ratifications**," and `state.md` says "the owner's **ruling** closed it." One of the three labels matches the record; two overclaim it. This matters more than usual because the sentence in question — what makes work *finished* — is now law on two pages.

*Your options:*
1. **Selection is enough — fix the labels.** The kernel keeps a clear second category: a call you made by picking a drafted option, quoted and dated, honestly labelled as that. The two overclaiming labels come down. Cheapest, and nothing about the sentence changes. *Recommended.*
2. **Say it in your own words.** You re-state what *sufficient* means in your own phrasing, it goes into `decisions.md` as a genuine ratification, and the sentence on both pages is rewritten to match. Costs you a few minutes and makes the kernel's most load-bearing definition unambiguously yours.
3. **Tighten the rule instead.** If picking from drafted options should never count as your word for anything, say so and the method page's definition of *ratified* gets the exception written into it — which would also reopen how several earlier calls are recorded.

Nothing else in this review waits on you. The piece routes back to build regardless of your answer.

---

## Result

**Routed back to build (B1–B8) and to one more round of experiencing (E1), 2026-08-29.** The piece keeps the live slot; the map stays unticked.

What held, at my own hand: both receipt chains valid under git; conservation clean; budgets at 58.8% and 53.1% with every pinned figure reproducing; control arm 4/4 red; the four sentences present and findable at all five named homes; the census delta at zero undefined rule words; both fixtures condemned by a fresh reader quoting them verbatim; the `decisions.md` transcription landed, dated, and honestly labelled; `state.md:5` corrected; the map naming the live piece; and rule 1's procedure vindicated on both real corpora against the record's own sharpest attack.

What routed it: the previous judgment named two sites and the batch swept one. Around that, six more instances of the same class — a quoted floor left red, a control that misstates its own corpus, a record obligation the record does not meet, a skeleton set with no slot for it, strain counts frozen in three homes while the strain kept biting, and a stale-page law living on one page while the judge it has now bitten twice reads a different one.

**For the next builder:** rule 1 is a better sentence than this review nearly concluded — its procedure finds every home when the key is chosen well, and I proved that after two contexts had concluded otherwise. What it lacks is a way to choose the key, and its own prohibition on single keywords is what hid the sibling this batch missed. Fix the sentence, not the reputation. And the one thing no sentence here does yet: nothing in the method asks, when a rule is *born*, which pages' readers must obey it — rule 1 only asks which pages already do.

---

## Final word, 2026-08-29, on 39cdbd8

**Receipt line.** Claude Code · Opus 5 (`claude-opus-5[1m]`) · fresh context, built none of it and tested none of it · 2026-08-29 · piece "Three producers", union fix batch `0f30c51`+`d60e66d`, Built line `2eea8d4`, third re-entry receipt `39cdbd8`, E1's record `e613577`. Still blind: I have not opened `work/three-producers-judgment.md` or its continuation. Where the work file quotes line 1, I read the quote and formed my own view.

**Disclosure — the stale-page trap fired on me again, and this time the law caught it.** My host preloaded an `AGENTS.md` opening "You are an agent in a repository run by Speck Next … your host loaded it for you," with a section called "The conductor — law in every session." `grep -c "The conductor — law in every session" AGENTS.md` → **0**; `git log -S` returns `e5494cf` and `5d67cac`. The file at HEAD opens "You are building a product with Speck Next." Last round I recorded that `judge/SKILL.md` said nothing about this and I was uncovered. This round `judge/SKILL.md:10` says *"Read every page from disk at the commit under judgment — hosts preload stale copies, and judges have been bitten too,"* landed by the batch under review, and it is why I checked before reading a word. **B7's sentence produced the behaviour it was written to produce, on the judge it was written for, in the first session after it landed.** Everything below is read from disk at HEAD.

---

### 1. The third re-entry chain — valid, proved with git

| Commit | Touches | Class |
|---|---|---|
| `0f30c51` | `AGENTS.md`, `judge`, `experience`, `templates/piece.md` + work file | **build** (mixed) |
| `d60e66d` | `map.md`, `state.md`, work file | records |
| `2eea8d4` | `state.md` only | Built line |
| `39cdbd8` | `work/three-producers.md` only | receipt |
| `e613577` | `work/three-producers-T1.md` only | the run |

`git show 2eea8d4:state.md | grep -c "the re-fixed pages are \*\*Built\*\* as of this commit"` → **1**, literal, says **Built**. `git log --oneline 2eea8d4..HEAD -- AGENTS.md .claude/skills templates bin CLAUDE.md` → **empty**: no build commit lands after the line. `map.md` carries exactly one `[live` marker, row 7.

**On the question put to me about the receipt commit: I checked rather than accepted it.** `git show --name-only 39cdbd8` returns `work/three-producers.md` and nothing else — three inserted lines, the receipt. E1's record is a separate commit, `e613577`, touching only `work/three-producers-T1.md`. The receipt was committed **before** the run it orders, not alongside it. The chain is clean and the suggestion that it was not is false. **Valid.**

### 2. My eight controls, re-fired at my own hand

| | Pre-fix | At HEAD | Ruling |
|---|---|---|---|
| **B1** floor `grep -c "as its floor\|floor, not its scope" AGENTS.md` | 1 | **1** | requirement **met**, floor literally red — see below |
| **B1** population `grep -c "population" AGENTS.md` | 0 | **1** (`:90`) | **closed** |
| **B2** `grep -n "not one keyword" AGENTS.md` | 1 | **0** | **closed** |
| **B3** `grep -c "landing or changing\|Before landing" AGENTS.md` | 0 | **1** (`:70`) | **closed** |
| **B4** `grep -c "one home of three" work/three-producers.md` | 1 | **1** | **substance closed, form open** |
| **B5** four coverage claims returning a marked home set | 0 of 4 | **4 of 4 present, 1 mark false** | **half closed** |
| **B6** `grep -rci "home" templates/` | 0 across six | **1** (`templates/piece.md:31`) | **closed** |
| **B7** `grep -rciI "from disk" .claude/skills/judge/SKILL.md` | 0 | **1** (`:10`) | **closed** |
| **B8** `grep -ci "check failed\|not judged yet" state.md` | 0 | **1** (`:27`) | **closed but for the cost figure** |

**B1's floor is red on a word, not on the work, and I rule it green on the requirement — which is what rule 3 tells me to do.** `AGENTS.md:62` now reads "a quoted control is a floor, not **the** scope"; my quoted key said "not **its** scope", the phrasing `judge:92` uses. Both builder-page statements carry the floor rule; the population language landed at `:90`, taking that control from 0 to 1. Rule 3's own sentence — the control is the floor, the requirement is the scope — is what separates a genuine miss from my key being one article too narrow. It is the second consecutive judgment in which this sentence changed my ruling, and this time it protected the builder rather than convicting them.

**B4.** The corrected corpus is now in the file with the command that produced it, and I re-ran it: `grep -rnilE "literally say|Built line that covers" AGENTS.md .claude/skills templates` → four files, exactly as claimed. What did not happen is the fix at the point of use: `work/three-producers.md:12`, inside the committed **Planted fixtures** block, still reads "the edit touched one home of three" with no marker pointing forward to the correction 41 lines below. `AGENTS.md`'s own supersession rule — a superseded artifact says so at its own top the moment it is outrun — is unmet at line 12. Substance right, form wrong, one clause to fix.

**B8.** Both overclaiming sentences came down rather than acquiring commands — `grep -n "case-insensitive grep the record carries\|reach the readers who commit" state.md` → **empty**. Eight bites moved to eleven in both `state.md:11` and `map.md:16`; three bites moved to five at `state.md:13`; "Nothing waiting" became the ratified-word question carrying my recommendation. The cost line is the residue: `state.md:27` says "Piece cost so far, commanded: +1,562 bytes … caf557f 58,648 → 7bcaf95 60,210" while sitting in a file that describes the surface at `2eea8d4`. Measured at my hand over the installer's own `SURFACE` list at `bin/speck-next.js:11`:

```
ebb9fb5 56,039 · caf557f 58,648 · 7bcaf95 60,210 · HEAD 60,591
installed:   60,591 of 102,400  (59.2%)
always-read: 28,313 of  51,200  (55.3%)   [AGENTS+state+product+map, per CONTRACT.md:34]
union batch  7bcaf95 → HEAD  +381 B
piece to date caf557f → HEAD  +1,943 B  (+3.31%)
```

The v5.2.0 pin of 56,039 reproduces for the third time, and my own 7bcaf95 always-read figure of 27,206 reproduces exactly — the measured-numbers convention is holding across five commits and four hands. `grep -rn "60,591\|+381" state.md work/three-producers.md decisions.md` → **nothing**. The union batch's cost is recorded nowhere. This is the same narrow defect I charged last round on the previous batch's +614 B; it has now happened twice.

### 3. E1 — the route is satisfied, and exceeded

My E1 scenario named six sentences from disk at the re-fixed commit, one pass each, what each buys a builder, then both fixtures re-run, then a free attack. E1 read all six plus `AGENTS.md:61` and `:62`, returned a one-pass verdict and a named benefit for each, re-condemned both fixtures quoting the current wording verbatim, and ran a free attack it chose *because* `AGENTS.md:113` gave it a one-command test. It disclosed its own stale preload before reading a word, and disclosed that its commit trailer names a different model than the one that ran. **The route is closed.**

What I could not verify from git is freshness itself — E1's identity line carries a session id matching this workflow's. What I can weigh is that E1's central finding condemns the very claim the batch's own commit message advertises, that it charged the builder rather than clearing them, and that I reproduced the finding independently. A record written to flatter its author does not do those things.

**Struck, one claim, on its inference and not its evidence.** E1 charged `fresh challenge` at `AGENTS.md:62` as "an undefined rule word minted in the same batch that landed the rule against undefined rule words." It was not minted here. `git show caf557f:AGENTS.md | grep -c "fresh challenge"` → **1**, before this piece existed; `git log -S"fresh challenge" -- AGENTS.md` → `e5494cf`, the rewrite piece. The batch rewrote step 5 around the phrase and kept it. Rule 2 fires on the **first** writing of a word, so it condemns `e5494cf`, not `0f30c51`. **The observation is right and useful; the attribution is wrong.** It is an inherited defect on the product surface, and it routes as an open item, not as this piece's failure. This is the same discipline I applied to T2′ last round, applied now to a tester whose verdict favours the piece.

**Confirmed at my hand — E1's finding stands, and it is the real one.** The record at `work/three-producers.md:58` states a returned home its own quoted command does not return:

```
grep -rnilE "floor, not the scope|as its floor" AGENTS.md .claude/skills templates
  → AGENTS.md                                    (judge/SKILL.md is NOT returned)
```

The record lists `judge/SKILL.md — changed`, under a header promising "every returned home listed and marked." Rule 3 does live there — `judge:92` says "its floor, not **its** scope" — so the mark is true about the world and false about the command, which is exactly what `AGENTS.md:113` forbids: *written after the run, never from memory*. The key that actually finds all three homes is `-iE "floor, not (the|its) scope|as its floor"` → `AGENTS.md:62`, `:90`, `judge:92`, and I ran it.

E1's structural half is also correct and I verify it: all four coverage keys are strings this piece authored, so no key can return an untouched home, so no control can fail — `AGENTS.md:68` rules on that directly. And it has a material consequence, not just a formal one. Running rule 1 as written surfaces a home the narrow keys hid:

```
grep -rniE "undefined|jargon|defines? it" AGENTS.md .claude/skills templates
  → AGENTS.md:113 · .claude/skills/judge/SKILL.md:67
```

`judge:67` — "Undefined jargon that carries a rule is a defect" — is a second home of rule 2's subject, and the record never had to decide about it. E1 correctly declined to charge that `judge:67` must change; the charge is that rule 1 requires it be listed and marked. Right on both halves.

### 4. My own probe — rule 2 turned on this batch

Nobody had run the piece's own census rule against the union batch. I did it mechanically: pre-image vocabulary over `AGENTS.md`, all skills and templates at `7bcaf95` (1,571 words), subtracted from the batch's additions.

> execute · homes · hosts · keys · landing · narrowest · night · touched · used · widest

Ten new tokens. `homes`, `landing`, `touched`, `execute`, `used` are inflections of words the pages already carry. `hosts` and `night` are plain English in non-rule positions. `keys`, `widest`, `narrowest` are glossed by the verb of their own sentence — "grep case-insensitively, trying several keys from widest to narrowest" — and E1 read that clause in one pass and called it the sharpest thing in the delta. **Zero new undefined rule-carrying words.** The piece's rule 2 passes on the piece's own repair batch, at a hand that did not write it.

### 5. A finding of my own that neither line has made

**A strain count baked into an installed page is a number guaranteed to go stale, in a file where it was never true for the reader.** `experience/SKILL.md:14` now ships the sentence "five reviewers in one night caught theirs doing exactly that." E1 was the sixth, disclosed at `e613577` — one commit after the number landed. My host preloaded again in this context, making at least seven disclosed instances. The count was stale inside the same night, in the same session, by the next commit.

Worse than staleness: `experience/SKILL.md` **installs**. Every product that runs `npx speck-next install` receives a sentence about this repository's own review history, in their page, about reviewers they never had. That is this repo's strain narrated on the product surface. The law itself — *read every page from disk at the commit under test* — is right and belongs there. The tally does not. It belongs in `state.md`, where the strain is counted and where `state.md:11` already names the mechanism that would end the argument: a computed check. Two of this file's live strains intersect here — the report-of-itself and byte-exact self-measurement — and the answer to both is the same, and it is not another sentence.

### 6. The four

**Works — kept.** Verified by execution, not reading. Rule 3 changed a judge's ruling for the second consecutive round, this time in the builder's favour (§2, B1). `judge:10`'s from-disk law caught my own stale preload before I read a word, the first session after landing. `AGENTS.md:113` chose E1's free attack, and the attack found a real defect. Rule 1's widest-first clause, executed by a fresh reader, surfaced `judge:67` — a home the record's narrow keys hid. Both fixtures condemned at current wording by a fresh reader quoting them verbatim, and fixture 2 now condemned on the **builder's** side as well as the judge's, by two independent builder-page statements — the exact reach failure that routed the last two rounds, closed where a cold reader can see it closed. Census delta zero at my own hand. `./devsuite/run.sh --control` → **4 of 4 tasks went red**, run by me: the suite can still express failure.

**Delivers the promise — kept, with two open items.** Judged against `product.md` and `CONTRACT.md`. Promise 3 kept: three fresh non-builder contexts, receipts committed before every run, two judgment lines, this one blind. Promise 4 kept as of `2eea8d4`: every overclaim I charged either acquired its command or came down, and the file now carries its own rulings in the judgment's words. Promise 6 kept — see below. Promise 7 kept and measured: 59.2% and 55.3%, every pinned figure reproducing. **Promise 8 — broken again, narrowly, and for the second batch running:** +381 B recorded nowhere, in a piece whose live strain is byte-exact self-measurement. One command fixes it and it is a landing condition, not an open item. Noted not charged, unchanged from last round: `capabilities.md:7` pins `AGENTS.md` at "~11.4 KB, measured at v5.2.0" against 14,096 B at HEAD — pinned, so honest, but the instrument reports a smaller kernel than exists.

The shaped outcome — "each stopping a defect class at its source instead of catching it a round later" — I rule delivered, and I say precisely how far. It was not stopped at its source: the record committed the class a third time. It was caught **inside the round, by the piece's own rule, executed by a fresh reader, before any judge saw it.** Last round I caught it a round later. This round the rule caught it in the round. That is the sentence doing its work at one remove from the claim, and I will not pretend it is the full claim.

**Good to use — kept.** The half I refused to rule last round is now judged on testimony rather than my own reading. E1 read eight sentences cold, one pass each, and named what each buys a builder without the work file open — including the two nobody had read, rule 1 as rewritten and `AGENTS.md:90`. `judge:92` improved from two passes to one against a measured predecessor. Filed and not fatal: one charged stumble (`fresh challenge` at `:62`, inherited) and one locating complaint (`:111`, four unrelated rules stacked under no heading, filed by both readers).

**Quality hangs together — kept, on three named defects and no strength excusing them.** Last round I listed nine, seven of them the piece's own subject matter. Three remain, all in the record and none in the installed product: the false coverage mark, four fix-keyed controls that cannot fail, and the unmarked superseded gloss at line 12. I am not excusing them by pointing at the count. I am ruling that three record defects, all cheap, all caught inside the round by the mechanism, and all corrected by the landing conditions below, do not break the workmanship of a piece that arrived here with nine.

### 7. Sufficient — the piece lands and releases as v5.4.0

**Sufficient.** Ruled by the piece's own definition, which binds me: *the piece delivers what it was shaped to deliver and everything still open is named in `state.md` with where it went — a judge may land a piece with open items, never with silent ones.*

The deciding fact last round was that a judgment named two sites and the batch swept one. **That did not repeat.** Eight build orders named, eight executed; the experience order delivered in full and exceeded; the two homes I named both carry the rule; the prohibition that hid the sibling is gone; the trigger fires on birth; the templates carry the slot; the judge's page carries the law and it caught me.

I tested the case for a fourth round and rejected it, and the reason is E1's and I verified it: *the repair is not another sentence — `AGENTS.md:70` already says everything needed; the repair is running it.* A route-back orders more writing for a defect whose sentence exists and works. What changed this round is that the mechanism ran and caught the residue itself. Routing the author back a third time is not the repair for an author who is the weak link; naming the open items with their destinations is what rule 4 was written to permit, and applying it to its own piece is the honest test of whether it is a rule or a wish.

**Landing conditions.** These are records corrections and one number; none touches a product file, so none requires a new Built line, and the map tick is the gate.

- **C1 · The coverage record obeys the rule it certifies, once.** Re-run all four claims with keys aimed at the **rule**, not at the fix; paste what each command returned; mark every returned home changed or untouched. Rule 3's key becomes `-iE "floor, not (the|its) scope|as its floor"` (→ `AGENTS.md:62`, `:90`, `judge:92`); rule 2 lists `judge:67` marked untouched with the reason. The false mark — `judge/SKILL.md` listed under a command that does not return it — comes out. **The piece does not land carrying a false statement about what a command returned.**
- **C2 · The batch's cost is commanded.** `state.md:27` carries the current figure: `git cat-file -s` summed over `bin/speck-next.js:11`'s list — caf557f 58,648 → HEAD 60,591, **+1,943 B piece to date, +381 B this batch**; installed 59.2%, always-read 28,313 of 51,200.
- **C3 · Line 12 says it is superseded.** One clause on the fixture block pointing at the corrected gloss, per the kernel's own supersession rule.
- **C4 · `state.md` is rewritten at the landing to match reality** — these four rulings, E1's run done, and the open items below each with its destination.

**Open items, landed with destinations named (rule 4's own bar).**

1. **`fresh challenge` at `AGENTS.md:62`** — an undefined rule word for an obligation the pages name twice as "one free skeptical attack, reported either way." Inherited from `e5494cf`, not minted here. *Destination:* a small change after the tick — no new dependency, no promise touched, one commit to revert.
2. **The bite count on an installed page** (`experience/SKILL.md:14`, "five reviewers in one night") — already stale by at least two, and it ships this repo's history into every installed product. *Destination:* the next kernel piece. The law stays; the tally moves to `state.md`. This is the more valuable of the two and it is where the report-of-itself strain and the self-measurement strain meet.
3. **`AGENTS.md:111`** — four unrelated rules stacked under no heading; two independent cold readers filed the same locating complaint. *Destination:* the next kernel piece, with the density work.
4. **`capabilities.md:7`'s pinned `AGENTS.md` cost**, 23.6% below the file it describes. *Destination:* a computed check, which `state.md:11` already names as the retirement of the self-measurement strain.
5. **The ratified-word question**, unchanged and still the owner's. Filed by both judgment lines with the same recommendation, carried at `state.md:23`. Non-blocking; the piece lands either way.

**Release.** `package.json` reads 5.3.0 and the tags run to `v5.3.0`. On the conditions above executed, the piece ticks on `map.md`, `state.md` is rewritten, and the kernel releases as **v5.4.0** with every release-facing surface in the landing commit.

### 8. For the next builder

Two things, and neither is a sentence to write.

**The record's failure is a running failure, not a writing one.** Three consecutive rounds rewrote the coverage block and three failed it, while the rule they were certifying stayed correct throughout and caught the third failure itself. The tell is mechanical and cheap to check: **if your coverage grep is keyed on the text you just wrote, it cannot return an untouched home, so it cannot fail, so it proves nothing** — `AGENTS.md:68` was already on the page saying so. Key on the rule, not on the fix.

**And the thing rule 1 still does not ask.** Last round I wrote that nothing in the method asks, when a rule is born, which pages' readers must obey it. `AGENTS.md:70` now says "or must now carry it," which is the words for it — and this round the same batch shipped a strain tally into an installing page, which is the mistake in the opposite direction: not a rule that failed to reach a page, but a fact about this repository that reached every future one. The question rule 1 answers is *which pages carry this*. The question it still does not ask is *whose page is this, and is this true for them*.

**Result: sufficient, 2026-08-29, on `39cdbd8` plus `e613577`.** The piece lands and releases as **v5.4.0** on the four conditions in §7; five open items named with destinations; the owner's one question open and non-blocking. Both judgment lines now close sufficient, from different evidence and by different routes, and the divergence that opened at `15fdaad` is resolved by the batch that answered it rather than by rank.
