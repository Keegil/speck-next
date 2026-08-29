# Three producers — T2, the conservation prober

**Subject:** speck-next at `def1677` (build `77628d1`, pre-build `caf557f`, Built line `fc33a7b`). Fresh context; built none of it. Every claim below carries the command that produced it and what it returned, run in this session.

---

## 1. The word-diff — five sites, nothing lost

`git diff --word-diff=plain caf557f 77628d1 -- AGENTS.md .claude/skills/judge/SKILL.md`

Five sites, four sentences, in two files:

| Site | File | Form |
|---|---|---|
| build loop | `AGENTS.md:70` | new paragraph (rule 1 — same edit, every home) |
| ladder | `AGENTS.md:111` | insertion after "sufficient" (rule 4) |
| files section | `AGENTS.md:113` | sentence appended (rule 2 — a new word defines at birth) |
| ruling step | `judge/SKILL.md:59` | sentence appended (rule 4) |
| re-run section | `judge/SKILL.md:92` | sentence appended (rule 3 — a control names its population) |

`git diff --stat caf557f 77628d1` → `AGENTS.md | 6 ++++--`, `judge/SKILL.md | 4 ++--`. The four "deletions" are the two modified lines in each file being rewritten; the word-diff shows only one bracketed removal, `[-sufficient-]{+sufficient: …+}`, which is an insertion at a word boundary, not a loss.

**Mechanical proof that nothing was lost.** I diffed the two files line-by-line and required every token of every changed old line to survive, in order, in the new text:

```
AGENTS.md old lines: 125  new lines: 127  lines whose words did NOT survive: 1
   LOST (109, 'The four states are **Shaped → Built → Judged → Live**. …')
judge/SKILL.md old lines: 98 new lines: 98  lines whose words did NOT survive: 0
```

The one flag was a tokenizer artifact — `sufficient` became `sufficient:`. Re-run with punctuation stripped:

```
old ladder tokens: 111  new: 131  old is an ordered subsequence of new: True
tokens ADDED: 20
insert span: ': the piece delivers what it was shaped to deliver, with every open item
              and its destination named in `state.md`'
```

**Result: pure additions at all five sites. No prior wording deleted, no neighbor touched.** Context lines in the unified diff are byte-identical on both sides.

---

## 2. Sibling sweep — every home the four sentences touch

### 2a. Do the two `sufficient` homes agree?

- `AGENTS.md:111` — "Judged means its review ruled it sufficient: the piece delivers what it was shaped to deliver, with every open item and its destination named in `state.md`"
- `judge/SKILL.md:59` — "Sufficient means the piece delivers what it was shaped to deliver — you may land it with open items, never silent ones: `state.md` names each item and its destination."

Same substance, no contradiction. One asymmetry worth naming: the owner's ratified sentence has two halves — the *definition* and the *permission* ("a judge may land a piece with open items, never with silent ones"). The judge's home carries both. The ladder carries the definition and only implies the permission. Not a conflict; the page every session reads states the requirement without stating the licence. **Noted, not filed as a defect.**

### 2b. Does any other page state the Judged/sufficient rule and now disagree?

Swept `AGENTS.md`, `README.md`, `CONTRACT.md`, `product.md`, `map.md`, `state.md`, `decisions.md`, all six `templates/`, all five skills and their four references.

| Page | What it states | Verdict |
|---|---|---|
| `CONTRACT.md:20` | four states; "Judged spells out the four verdicts separately"; insufficient routes back | consistent — never defines *sufficient*, so nothing to disagree with |
| `README.md:26` | same four-states paragraph, owner-facing | consistent |
| `templates/state.md:6` | "Insufficient work returns without advancing." | consistent |
| `templates/piece.md:29` | "Sent back: [Anything insufficient returns…]" | consistent |
| `AGENTS.md:62, :88, :98` | uses *sufficient* / *insufficient* without definition | see F4 |

No page contradicts the new definition. **The sibling sweep for rule 4 is clean on contradiction** — but see F1, which is a stale sibling *inside* `state.md` itself, and F3, which is about whether the sweep can be re-run at all.

### 2c. Does the population rule conflict with existing control language?

All control language on the loaded surface:

```
$ grep -rn "control" AGENTS.md .claude/skills/*/SKILL.md .claude/skills/*/references/*.md templates/*.md CONTRACT.md README.md
AGENTS.md:7    "## Keep the owner in control"                     (different sense)
AGENTS.md:68   a control that cannot fail proves nothing
judge:28       a mid-review fix answers to the re-run rules, "including its own pre-fix control"
judge:92       [the new sentence]
judge:94       a mid-review fix needs a control the judge can run against the pre-fix tree
experience/references/walk.md:26  "if automation cannot reach a control"  (UI sense)
```

No conflict. The expressible-failure rule (`AGENTS.md:68`) constrains what a control must be able to *show*; the new rule constrains how wide it must *reach*. They compose: a population-wide control still has to be able to go red. Nothing on the pages says a green control closes a finding, so "floor, not scope" does not under-cut an existing closure rule.

---

## 3. Budgets, with commands

Installed surface = the installer's own list (`bin/speck-next.js:11`: `AGENTS.md`, `CLAUDE.md`, `.claude/skills`, `templates`), summed with `git cat-file -s` at each commit:

```
ebb9fb5 (v5.2.0 landing): 56039     ← reproduces the figure recorded in state.md:7 and decisions.md:7, exactly
cca7841 (v5.3.0 landing): 58648
caf557f (pre-build):      58648
def1677 (HEAD):           59596
```

**This piece costs +948 bytes, +1.6%.** Per file: `AGENTS.md` 13,145 → 13,657 (+512), `judge/SKILL.md` 8,127 → 8,563 (+436). 512 + 436 = 948 — the delta is fully accounted for by the two edited files, nothing landed anywhere else.

Against the contract's limits (`CONTRACT.md:32,34`):

```
installed:    17 files of 20 · 59,596 bytes of 102,400   (58%)
always-read (AGENTS + state + product + map): 25,738 of 51,200  (50%)
              ebb9fb5: 24,198 — reproduces the recorded figure exactly
```

Both budgets healthy. Both previously recorded figures reproduce at their pinned commits, so the measured-numbers convention is holding.

**Dev suite control arm:**

```
$ ./devsuite/run.sh --control
FAIL small-change · FAIL bug-hunt · FAIL honest-state · FAIL review-integrity
control mode: 4 of 4 tasks went red (want: all)
```

4/4 red. The suite can still express failure.

**The four sentences are where the record says they are** — one grep per sentence over the installed surface:

```
"Before changing a rule that is stated in more than one file" → AGENTS.md:1
"when a word carries a rule, define it in its first sentence" → AGENTS.md:1
"the control names its whole population"                     → judge/SKILL.md:1
"the piece delivers what it was shaped to deliver"           → AGENTS.md:1, judge/SKILL.md:1
```

Five hits, five sites, no strays elsewhere in `templates/` or the other four skills. The receipt's "AGENTS.md ×3 sites, judge ×2 sites" is accurate.

---

## 4. The new sentences applied to their own build

This is where the piece stops conserving.

**Rule 1 — homes listed in the record?** Yes: the work file's Outcome names all five, and the receipt repeats the count. **But no grep is recorded** — rule 1's own procedure ("grep for its words and find every home") left no trace, and neither commit body (`77628d1`, `fc33a7b`) carries a command or a return. I re-ran the greps myself and they hold; the finding is the missing receipt, not a false claim. → **F2**

**Rule 2 — no new undefined word?** The additions mint four candidate rule words. Three define themselves in the same breath: *home* ("a rule that is stated in more than one file … find every home"), *population* (glossed immediately as "every home, file, or case"), *silent* (defined by contrast with "names each item and its destination"). *Floor* matches existing usage (`AGENTS.md:115`, "Templates are starting floors"). One is thin: *the class* in judge:92 has no antecedent noun on the page and is a fourth distinct sense of "class" on the loaded surface (`AGENTS.md:92` "no middle class", `:115` "first-class work", `:123` "classification"). → **F7**, minor. Census delta on new undefined terms: **effectively zero, one thin edge.**

**Rule 4 — open items named where they go?** The piece is not Judged yet, so the rule is not yet due. But the same session's `state.md` rewrite left an item silently stale. → **F1**

**Rule 3 — a control naming its population?** The proof plan's Built checks ("grep each", "control arm 4/4 red") name their population correctly. The plan's checks were not written down after running, which is F2 again.

---

## 5. Free swing — can rule 1 actually be re-run?

Rule 1 tells the next agent to "grep for its words and find every home." I tested that procedure against the freshest thing on the pages: the `sufficient` definition this piece just landed in two homes.

```
$ grep -rn "sufficient" AGENTS.md .claude/skills templates | wc -l
9
$ grep -n "sufficient" .claude/skills/judge/SKILL.md
3:  description: … sends insufficient work back …
73: ### 6. Send insufficient work back
$ grep -ni "sufficient" .claude/skills/judge/SKILL.md | wc -l
3
```

**The judge's definition home is invisible to the case-sensitive word grep.** The sentence starts with a capital *S* ("Sufficient means the piece delivers…"), so line 59 never appears. The file *does* show up in a file-level sweep — but only because the unrelated word "insufficient" is in it, which is worse: an agent opens the file, greps inside it, sees two hits that are both "insufficient", and concludes the judge does not carry the definition. The next change to the sufficient definition, made by an agent obeying rule 1 literally, lands in one home. That is fixture 1, reproduced by the rule written to condemn it.

The phrase grep works (`"the piece delivers what it was shaped to deliver"` → both homes). So the defect is not fatal — it is that rule 1 names a *key* it never defines: "its words" is undefined, and case, morphology (`sufficient` / `insufficient`), and paraphrase all break it. Two cheap fixes: lowercase the judge's home ("A ruling of *sufficient* means…"), and have rule 1 say what a home is greppable *by* — the rule's phrase, not its keyword.

Second half of the same swing: rule 1 creates a record obligation ("list the homes in the record") and `templates/piece.md` — the record's own skeleton — has no field for it. This session complied from memory. → **F6**

---

## Findings, ranked

**F1 · CONFIRMED · the stale third home, live at HEAD.** `state.md:5` still reads: *"a full census of the 124 rule-carrying terms across the loaded pages leaves exactly one word undefined — `sufficient`, which is the owner's sentence to write (below)."* The owner wrote it; it landed at `77628d1`. Lines 22 and 26 say so. Line 5 says the opposite, and its "(below)" pointer sends the reader straight to the contradiction.

```
$ git show cca7841:state.md | sed -n '5p'   # v5.3.0 landing — true then
$ git show def1677:state.md | sed -n '5p'   # HEAD — byte-identical, false now
```

The commit that rewrote state (`6c22d89`, *"state tells tonight's truth"*) touched only the later sections: `2 insertions(+), 7 deletions(-)`. The fact had three homes in one file; the rewrite fixed two. This is fixture 1's exact class, committed in the same session that landed the sentence condemning it — and it is the strain's own signature ("a corrected figure left standing in the file that outranks the corrected one"). Also stale by the same line: the 124-term census predates four new sentences that mint new rule words, and unlike every byte figure in the file, the census count carries no commit pin.

**F2 · CONFIRMED · done-everywhere claims with no command.** `state.md:26` — "his ratified sentence for *sufficient*, **in both its homes**" — and the receipt's "AGENTS.md ×3 sites, judge ×2 sites" are both closure claims about coverage. `AGENTS.md:113` (landed one release ago) requires such claims to carry "the command that produced it and what it returned, written after the run." Neither carries one; no commit body does either. Both claims are **true** — I verified them above — so this is an evidence defect, not a false statement, and it is cheap to close by pasting the four greps into the work file.

**F3 · CONFIRMED · rule 1's grep cannot find the definition it was landed beside.** Section 5. The judge's `sufficient` home is invisible to the obvious sweep.

**F4 · CONFIRMED · `sufficient` is used 49 lines before it is defined.** `AGENTS.md:62` ("If the judge finds it sufficient, land it") and `:88` are the reader's first two encounters; the definition is at `:111`. Rule 2, landed in the same commit at `:113`, says "when a word carries a rule, define it in its first sentence… an undefined rule word is defective when written, not when a reader trips over it." A cold reader still trips at line 62. Fixable in one clause at `:62` or by a forward pointer.

**F5 · PLAUSIBLE · rule 3's builder half sits in a page the builder does not read.** The strain's named root cause is the *builder* executing the quoted control literally. The corrective sentence — "The builder executes the full requirement; the quoted control is its floor, not its scope" — landed only in `judge/SKILL.md:92`. The builder's own homes still read scope-shaped: `AGENTS.md:62` "repeat the exact test scenarios", `AGENTS.md:90` "Re-run the exact scenarios the judge named". The judge-facing half (widen the control) does work on its own, so this is a partial producer, not a dead one — I mark it PLAUSIBLE, not CONFIRMED, because a wider control mechanically widens what a literal builder executes.

**F6 · CONFIRMED · the record obligation has no slot.** `templates/piece.md` carries no homes field; rule 1's "list the homes in the record" runs on memory.

**F7 · minor · "the class"** at judge:92 has no antecedent noun and is a fourth sense of *class* on the loaded pages.

**F8 · minor, already healed · the receipt's anchor is self-contradictory at the SHA it quotes.** At `fc33a7b`, the same `state.md` paragraph says both *"The live piece 'Three producers' is Built as of this commit"* and *"**No piece is live.**"* Reconciled at `6c22d89`. A judge checking the anchor commit, as `judge/SKILL.md:28` instructs, reads the contradiction. Nothing to fix at HEAD; worth a line in the Result so the next builder writes the Built line and the reconciliation in one thought.

---

## Verdict

**Conservation: clean. Self-application: not clean.**

The four sentences landed exactly as the record says — five sites, pure insertions verified token by token, no wording lost, no neighbor disturbed, no stray edit anywhere else on the installed surface. The cost is +948 bytes (+1.6%), fully accounted for by the two files, leaving both budgets at roughly half their ceilings. Every previously recorded figure I could re-measure reproduced exactly, and the control arm is 4/4 red. On the four questions I was sent to answer about the *artifact*, I find nothing wrong.

What I do find is the session's own records failing two of the rules the session landed. `state.md:5` still tells the owner that `sufficient` is undefined and owed by him, hours after he wrote it and it shipped — the fact's third home, missed by the rewrite that claimed to tell tonight's truth. And every coverage claim this piece makes about itself is uncommanded, in a kernel that requires commands for exactly those claims. Both are the strain this piece exists to repair, biting inside the repair. Neither is expensive: one sentence rewritten, four greps pasted.

I do not rule; that is the judge's. My reading is that F1 and F2 are the piece's real test — the sentences are sound, and the evidence that they change behaviour is currently negative in their own author's hands.

---

## Follow-up run (T2′), 2026-08-29, on 7bcaf95

**Subject:** speck-next at `7bcaf95` (fix batch `684e359`, Built line `8e9140e`, pre-fix `def1677`, judgment `99ac32a`). Fresh context; built none of it. Every page read from disk at the commit under test — **my host preloaded a v5.0-era `AGENTS.md`** ("## The conductor — law in every session"), a section that does not exist in the 127-line file on disk. That is the fourth bite of the strain `state.md:13` records as three, and it happened to the tester the new law was written for.

**Re-entry receipt — valid, checked with git.** `git show 8e9140e:state.md | grep -c "the fixed pages are Built as of this commit"` → `1` (literal, says **Built**) · `git show --stat 8e9140e` → `state.md` only · `git log 8e9140e..HEAD -- AGENTS.md .claude/skills templates bin CLAUDE.md` → empty · `7bcaf95` touches `work/three-producers.md` only, and is `8e9140e`'s child.

### 1. The nine routes, each run

| Route | Command | pre-fix | at 7bcaf95 |
|---|---|---|---|
| R1 | `diff <(git show cca7841:state.md \| sed -n 5p) <(git show HEAD:state.md \| sed -n 5p)` | identical | **DIFFERS** ✅ |
| R2 | `grep -c "Land + name" / "Keep the wide wall" / "Run it now" decisions.md` | 0 / 0 / 0 | **1 / 1 / 1** ✅ |
| R3 | `grep -rni "delivers what it was shaped to deliver"` | judge home invisible | **AGENTS.md:111 · judge:59 · state.md:23** ✅ |
| R4 | `grep -c "population\|floor, not its scope" AGENTS.md` | 0 | **0 — still red** ❌ |
| R5 | `grep -c "destination" templates/state.md` ; `grep -c "homes" templates/piece.md` | 0 ; 0 | **1 ; 0 — half red** ❌ |
| R6 | `grep -ci "three producers" map.md` | 0 | **2**, row 7 `[live]`, sole live marker ✅ |
| R7 | `grep -c 'grep' work/three-producers.md` | 3 | **6**, and all four quoted greps verify ✅ |
| R8 | `git ls-files work/three-producers-{T1,T2,judgment}.md` | T1 empty | **all three tracked** ✅ |
| R9 | `grep -c "preload" state.md` | 0 | **1** ✅ |

**R3 in full, by rule 1's own prescribed procedure** (case-insensitive distinctive phrase — run, returns shown):

```
"one-home fix is not a fix"              → AGENTS.md:70
"grep for its distinctive phrase"        → AGENTS.md:70
"define it in its first sentence"        → AGENTS.md:113
"in the sense you mean"                  → AGENTS.md:113
"names its whole population"             → judge/SKILL.md:92
"floor, not its scope"                   → judge/SKILL.md:92
"as its floor"                           → AGENTS.md:90
"delivers what it was shaped to deliver" → AGENTS.md:111 · judge/SKILL.md:59 · state.md:23
grep -ni "sufficient" judge/SKILL.md     → 3, 59, 73   (pre-fix: 3, 73 — line 59 was invisible)
```

The judge's `sufficient` home is reachable again — closed by sharpening the rule, not by lowercasing the home. Fixture 1 is no longer reproduced by the sentence written to condemn it.

**Budgets, pinned** (`git cat-file -s` summed over the installer's list, `bin/speck-next.js:11`):

```
ebb9fb5 56,039   cca7841/caf557f 58,648   def1677 59,596   7bcaf95 60,210
installed:  17 files of 20 · 60,210 of 102,400 (58.8%)
always-read: 27,206 of 51,200 (53.1%)   [def1677: 25,738]
fix batch: +614 B · the piece to date: +1,562 B (+2.66% on caf557f)
```

`./devsuite/run.sh --control` → `control mode: 4 of 4 tasks went red (want: all)`.

### 2. Sibling sweep first — where the family still disagrees

**G1 · CONFIRMED · R4's quoted control never went green.** `grep -c "population\|floor, not its scope" AGENTS.md` → `0`. The concept did reach the builder's page — `AGENTS.md:90` now says "with any quoted control as its floor" — so the requirement above the floor is arguably met while the floor itself stays red. The judge's own sentence is *floor*, i.e. a minimum.

**G2 · CONFIRMED · the other builder-page home was left untouched.** The judgment named two scope-shaped sites: `AGENTS.md:62` and `:90`. Only `:90` was fixed.

```
git diff 99ac32a 7bcaf95 -- AGENTS.md | grep -c '^[+-].*exact test scenarios'  → 0
AGENTS.md:62 (byte-identical pre and post): "...fix the named problem and repeat the
exact test scenarios plus the required fresh challenge."
```

Line 62 is step 5 of the numbered build loop — the summary a builder reads first. Rule 3's builder half landed in one of two homes on the builder's own page: fixture 1's exact class, inside the batch that closed fixture 1.

**G3 · CONFIRMED · the newest rule in the batch breaks R4 itself.** The stale-page law landed only at `experience/SKILL.md:14`; `grep -rni "from disk" .claude/skills/judge/SKILL.md` → nothing. The judgment's own J4 records the judge as one of the three bites ("I am the third"), and `judge:10` licenses judges to re-run checks themselves. The rule does not sit on the page whose reader committed the defect. Its wording under-counts too — "two testers on two pieces" against the three bites `state.md:13` records — and I am the fourth bite.

**G4 · CONFIRMED · R5's control is half red.** `grep -c "destination" templates/state.md` → `1` (green); `grep -c "homes" templates/piece.md` → `0`; `grep -rni "home" templates/` → nothing. Rule 4's open-items obligation reached both skeletons. Rule 1's record obligation did not — and the batch *widened* it ("the record carries the grep and everything it returned, each home marked changed or untouched"), so the skeleton gap is larger than when the judge measured it. Every product installed from `templates/` still starts without it.

**G5 · CONFIRMED · the strain's bite count is frozen at eight, in two homes.** `state.md:11` is byte-identical to `def1677`; `map.md:16` repeats "eight bites". The judgment recorded at least three fresh bites of that exact strain (the false census line, the citation to a record that did not hold it, the uncommanded coverage claims). `AGENTS.md:108` and `templates/state.md:9` require how often each strain has bitten, and the twice-rule at `AGENTS.md:58` keys on the count. A stale count left standing through a rewrite that made it stale is the strain's own signature — and with two homes it is also a rule 1 case.

**G6 · CONFIRMED · "ratifications" survives where the record it now cites says "selections".** The transcription is honest and says so itself: *"these are selections of drafted options, not his own phrasing."* `AGENTS.md:36` defines *ratified* as "the owner agreed in **their own words**". Yet `work/three-producers.md:3` still reads "the owner's 2026-08-29 **ratifications**", and `state.md:5` "the owner's **ruling** closed it". The citation resolves — R2 is genuinely green — but the label outruns the text it resolves to, on the one sentence whose authority the judgment turned on.

**G7 · PLAUSIBLE · the owner's question was closed without an owner record.** §7 offered three options and said the answer decides whether the fourth sentence returns to shaping. Option 1 was taken and the entry written by the builder; no owner response exists anywhere in the tree, and `state.md:23` now reads "Nothing waiting". Defensible — the fixing session held the selections and labelled them honestly — but the closure is asserted, not evidenced. This is the second judge's call, not a tester's.

**G8 · CONFIRMED · `state.md` carries no four-ruling line for the live piece.** `grep -ni "check failed\|not judged yet" state.md` → nothing, against `AGENTS.md:111` ("lists the four Judged rulings separately with evidence or 'not judged yet'") and `:113` ("A failed evidence check says 'check failed'"). A judgment exists with *works: check failed · delivers: broken · quality: check failed*. `state.md:27` renders all of it as "reviewed, routed back once, fixed", which reads better than the record does.

**G9 · CONFIRMED · the fix batch's own cost is recorded nowhere.** +614 B measured above; the first build's +948 was recorded by two contexts, the second build's by none. Promise 8 forbids quiet growth and the byte-measurement strain is live.

**G11 · minor · the record does not carry the grep rule 1 now demands.** The four coverage greps in the work file are single-file counts; none returns a full home set and no home is marked changed or untouched. Rule 3's coverage grep names only `judge/SKILL.md`, so the builder-page home it just created is absent from its own coverage claim.

**G12 · minor · "Built as of this commit" reused verbatim after the judge's hygiene note** (§1: *"Quote the wording you intend to keep"*). At HEAD the phrase resolves to `7bcaf95`, a records-only commit; the receipt saves it by naming `8e9140e`.

**G13 · minor · `work/three-producers.md:31` reads false in the present tense** — "`decisions.md` has neither" — inside the preserved §7 block, unmarked. Context carries it; the shape is the piece's own subject.

### 3. Free skeptical attack — the producers against a rule they did not author

I ran rule 1's own procedure on the **receipt/Built rule** — the rule fixture 1 uses as its example, and one the piece never edited. Distinctive phrase, case-insensitive:

```
grep -rni "literally say" AGENTS.md .claude/skills templates
  AGENTS.md:78 · judge/SKILL.md:22 · templates/piece.md:15        → 3 homes
```

The fourth home is `experience/SKILL.md:18` — *"Quote the `state.md` Built line that covers these product files"* — the same rule in different words, invisible to the grep. **Two results, both findings:**

1. **Fixture 1 under-counts the corpus it cites.** Its gloss reads "the edit touched one home of three", naming `AGENTS.md`, the experience skill and the piece template. The receipt rule has **four** homes; the missing one is `judge/SKILL.md:22–30`, which the judgment itself cited as a home (at `:28`). The piece's committed, re-runnable control mis-states the rule it controls for — the same under-count T1 made and the judge called the sharpest evidence for the defect.
2. **The sharpened rule 1 fixes the instance, not the class.** Case-insensitivity closed the capital-*S* miss. It does nothing for a home phrased differently — and the fix batch minted a fresh one: rule 3's two homes now read "the quoted control is its **floor, not its scope**" (`judge:92`) and "with any quoted control **as its floor**" (`AGENTS.md:90`), sharing no distinctive phrase. `grep -rni "floor, not its scope"` returns one home of two. The rule written to stop one-home fixes cannot, at HEAD, find both homes of the rule it was landed beside.

### Verdict (T2′)

**Nine routes: six closed clean, two half-closed, one never went green.** R1, R2, R3, R6, R8, R9 are green at my hand with commands and returns. R7 is green on the letter and thin on the spirit (G11). R5 closed one of its two quoted clauses (G4). R4's quoted control is still `0` (G1), its second builder-page home was never touched (G2), and the batch's own newest rule commits R4's defect a third time by living only on the tester's page (G3).

The batch is real work and most of it landed. What did not change is the thing the judgment named as the strain: *nothing in the method asks which surfaces must now carry a rule.* Three of my findings are that same missing question, asked and missed again inside the fix for it, and my free attack shows rule 1 still returns an incomplete home set on the first real corpus rule I pointed it at. The `sufficient` sentence's authority is now honestly recorded — and the honest record says "selections, not his own phrasing", which the work file still calls ratifications and which `AGENTS.md:36` says is not ratification (G6, G7).

I do not rule. My reading: the sentences are sound and now mostly reachable; the machinery around them is closer than at `def1677` and not yet finished, and the reach failures that remain are the piece's own subject, in its own hands, for the second time.
