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
