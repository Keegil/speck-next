# Name the words — judgment 2

**Judge 2 · Claude Code · model opus · 2026-08-29 · ruling on build `48283c7` at receipt `ac7e688`.** Built and tested none of it. Blind to judgment 1. Care raised to two judges because the edits changed the review-admission gate — the paragraph that decides whether a review may open at all.

**Ruling in one line: route back to build.** The seven texts landed at their anchors, nothing was quietly lost, the budgets hold and the control arm still goes red four for four — I re-ran all of that myself. But the piece's centrepiece is the four-state ladder, and two of its four definitions say less than the steps they summarise; the build put an exception into the judge's copy of the admission rule and left `AGENTS.md`'s copy of the same rule flatly contradicting it; and the piece's one falsifiable prediction failed its first arm four to nothing. Every fix below is one sentence. This is a close piece, not a broken one — but "close" is not the bar for the release that defines the method's own words.

---

## 1. The receipt check

### The chain, proved with git

| Step | Commit | Time | What it touched |
|---|---|---|---|
| Build | `48283c7` | 17:41:37 | `AGENTS.md`, `judge/SKILL.md`, `map-build/SKILL.md`, `work/name-the-words.md` |
| Built line | `9f6b1c4` | 17:41:37 | `state.md` only — 1 file, 1 insertion, 1 deletion |
| Receipt | `ac7e688` | 17:41:46 | `work/name-the-words.md` only |

`git show 9f6b1c4:state.md` line 26 reads: **"The live piece: 'Name the words' — Built (work/name-the-words.md)."** The quote exists and literally says **Built**. `git show --stat 9f6b1c4` confirms the commit changes nothing else. `git log ac7e688..HEAD` is empty and `HEAD` is `ac7e688`, so no build commit lands after the Built line. The tester records are untracked files written at 17:48–17:49, after the receipt commit at 17:41:46 — the receipt was committed before the probes ran.

**Receipt: valid.** The two other cheap git questions (`judge:71`) also pass: the work file was added at `4a70e03`, a separate and earlier commit than the first product commit `48283c7`, so it shaped the work rather than documented it; and `map.md` keeps exactly one live piece, which is the piece actually being built.

One wrinkle, recorded and not held against the receipt. The build commit `48283c7` already carried a receipt block whose Built field was a forward promise — *"quoted in the commit after the build's"* — and `ac7e688` replaced it with the real quote. So a draft receipt existed before the Built line did. `AGENTS.md:78` invalidates a Built line "written after the receipt opened", and on a strict reading of "opened" this is a hair's breadth. I rule it valid because the operative receipt — the one with a quote in its first field, the one the testers ran against — is `ac7e688`, and it opened nine seconds after the Built line. If the next piece wants this airtight, do not put a receipt block in the build commit at all.

### Exemption clause 1 — this repo, mid-build: **demanded the Built line**

`judge:24`: *"The exemption holds only when `map.md` has no live piece, or when the review's subject is `product.md` or `map.md` itself rather than built work."*

- **Clause A — does `map.md` have a live piece?** Executed: `grep -n "live" map.md` returns line 9 (*"Pieces (in order — exactly one live)"*) and line 15 (*"**Name the words** [live — …]"*). It has one. Clause A **fails**.
- **Clause B — is the subject `product.md` or `map.md`?** Executed: `git show --stat 48283c7` names `AGENTS.md`, `.claude/skills/judge/SKILL.md`, `.claude/skills/map-build/SKILL.md`. None is `product.md` or `map.md`. Clause B **fails**.
- Both fail, so the exemption is denied and the Built line is demanded. It was demanded, supplied, and verified above.

### Exemption clause 2 — a review whose subject is `map.md` itself: **exemption granted**

The never-run clause, run. Case put to it: this repo re-cuts its map to admit the piece the wearing-out list calls for, and a review opens on `map.md`.

- **Clause A** fails exactly as above — `map.md` has a live piece, and a repo mid-build always will.
- **Clause B** holds: the subject is `map.md` itself, not built work.
- The clauses are joined by "or", so B alone grants the exemption. No Built line is demanded; instead the check becomes "the receipt lists the planned probes and was committed before they ran", then straight to the records.

**The clause is live and does real work.** Clause A can never fire for a map review in a repo that is building anything, so without clause B every map review in an active repo would deadlock against a Built line that cannot exist. That is exactly the block judgment 1 of the previous piece called *"a real block on the first phase exit of every new repo"*, and clause B is what unblocks it. Running it is what proves it is not decoration.

**But running it also found the hole, and it is specific to this repo.** Clause B says "`map.md` itself". In this repository the product *is* the method, so `map.md` (the kernel's own map, at the repo root) and `.claude/skills/map-build/SKILL.md` (built product) are one word apart and one concept apart. This very build edited `map-build/SKILL.md`. A judge reading "the review's subject is the map" quickly could grant itself the exemption on a build that changed the map *skill*, and skip the Built line on genuinely built work. The distinction is correct as written and one careless read from being wrong. It costs four words to close: *"`product.md` or `map.md` itself — the product files, not the skills that write them."* Filed as finding 8.

---

## 2. Hearing the records

I read both in full, verdict last, and re-took every claim I could execute. What follows is only what I ran or read myself.

### What reproduced at my hand

- **The term greps.** Over the exact 17 installed files (`AGENTS.md`, `CLAUDE.md`, 9 under `.claude/skills`, 6 under `templates/`), with `zzqqxx` as a negative control returning 0 and `piece` returning 113 as a positive one — the instrument can express both a hit and a miss before any of its zeros count. `captioned screen drawing` → **0**. `captioned` → **0**. `screen drawing` → **6**, at `AGENTS.md:66`, `map-build/SKILL.md:14`, `map-build/references/questions.md:7`, `shape-product/SKILL.md:46`, `templates/map.md:15`, `templates/piece.md:5`. `caption` → **3**: one typographic in `craft:12`, two in the completion test at `map-build:28`. `protected code` → **1** plus `protected-code` → **1**. `good to use` → **4**, `quality hangs together` → **3**, the variant name *"holds together as a quality product"* → **1**. `gates` → **1**.
- **The byte measure.** Installed surface at `48283c7` and at `ac7e688`: **57,348 bytes**, matching the build record exactly. Always-read set (`AGENTS.md` + `state.md` + `product.md` + `map.md`): **23,240** of the contract's 50 KB. 17 files of 20. 5 skills of 6. All pass with room.
- **The control arm.** I ran `./devsuite/run.sh --control` myself. **4 of 4 tasks went red.** Every key check can still express the failure it claims to prevent after the edits.
- **The conservation of the seven texts.** Read against the raw `git diff 4a70e03..48283c7`: five of the seven are pure additions to lines otherwise byte-identical; two rewrite a line. The `map-build:28` rewrite keeps the population source, the grep, the count and the match-to-one-piece, and drops only the adjective *captioned* — the promised deletion. The `AGENTS.md:109` rewrite drops *"Judged is a piece's ceiling: work goes Live only when its whole milestone is proven and the owner has graded it,"* which still stands verbatim at `judge:59`. Nothing was traded away to make room. T2's conservation probe holds.

### Claims I corrected

- **T1, "`protected code` appears exactly once in the whole corpus."** It appears twice — hyphenated at `AGENTS.md:98` and unhyphenated at `AGENTS.md:121` — and T1's own record quotes the second one three lines later. The count is wrong; the finding survives untouched, because neither occurrence defines the term. Corrected, not struck.
- **T2, "no commit in the range produces 2.1 KB."** True as far as T2 checked, and incomplete: T2 tested three commits and skipped `ebb9fb5`, the commit `state.md:7` pins its own 55,157-byte figure to. `57,348 − 55,157 = 2,191`. The wrong number almost certainly came from subtracting the new measurement from an old one taken over a different population — which is worse than a memory slip and repairs differently. I chased it: measured over the installer's own `SURFACE` list (`bin/speck-next.js:11`), `ebb9fb5` is **56,039**, not 55,157. So `state.md:7` carries a figure that does not reproduce under the definition the installer uses, and this build's record inherited it. See finding 5.
- **T2, "the sibling sweep."** T2 swept the four state words plus `README.md` and reported the piece conserved. It did not sweep the siblings of the *edited rules*, and the highest-care edit in the build — the admission gate — has a sibling in `AGENTS.md` that now contradicts it. That is finding 1, and neither tester was looking there. A gap in the dispatch, not dishonesty in the record: the receipt asked for "the edited paragraphs' neighboring rules unharmed", which reads as neighbours *in the same file*.

Nothing else in either record was struck. Every verdict claim in both points at something the tester actually did.

### Challenging the favourable verdicts

**T1's headline — *"I could run a product under these pages tomorrow, and I would."*** T1's own Job 3 says a builder whose piece is a document hits a deadlock: it cannot run, so it cannot be Built; the exemption denies it on both clauses; without a Built line there is no review, so no Judged, so no landing, and it holds the live slot forever. Both cannot be true of the same reader.

They are true of different readers, and I record both without averaging. A builder who reads the whole corpus finds the escape T1 names — give the document piece genuinely runnable checks — and runs fine. A builder who follows *"when in doubt, demand the Built line"* literally jams. **The escape is not hypothetical: this piece is the proof.** "Name the words" is a document piece, it never ran anything, and it became Built by naming greps and budget measurements as its checks. The kernel has executed the unwritten rule without ever writing it down. That is the strongest possible argument for T1's one-sentence repair, and it costs a sentence.

Two things I will not hold against this build: the deadlock is inherited (the exemption was narrowed at `ebb9fb5`), and surfacing it is the clause doing its job on first execution.

**T1's undefinable count of four — challenged, and it survives, unevenly.** T1's own test is that plausible readings must lead to *different actions*, not different wording. Applying that test myself:

- **`protected code` — stands, hardest of the four.** It decides whether a change may ride in a batched review (`AGENTS.md:98`) and nothing defines it. Two candidate extensions are each forced by a different sentence, and they differ: the small-change list is *"auth, money, privacy, or data-integrity code"* (`:119`), the risky list is *"money, auth, private data, schema migrations, regulated behavior, or anything irreversible"* (`:123`). A schema migration is on the second and not the first. Under one reading it can be batched, under the other it cannot. That is a behavioural fork on exactly the class of work everything else here slows down.
- **`caption` — stands.** `map-build:28` orders "grep their captions" and no page says what a caption looks like. The contrast proves the gap: the *same bullet list's* first item names `job:`, `moment:`, `claim:`, which have a naming rule (`shape-product:34`) and literal examples in `templates/product.md:10,13,22`. Those are greppable. Captions are not, so the second bullet of a mandatory mechanical check is unrunnable, and grep for "caption" lands the reader in `craft:12`'s typographic sense instead.
- **`good to use` and `quality hangs together` — stand, but as the weak two.** T1 concedes "nothing jams", and under non-compensation a blocking finding blocks under either head, so misfiling between two blocking heads does not change whether a piece lands. That nearly demotes them to wobbles. What keeps them in the count is the third option: a judge who cannot tell the heads apart honestly writes "not judged yet", and under `judge:59` work is proven only when all four rulings stand on evidence — so the milestone stops. That is an action difference, and the asymmetry is damning on its own: of the four rulings that gate proven work, `judge:59` defines two and says nothing about the other two.

Even on the most generous reading the count is two, not zero.

---

## 3. The staked prediction

**Arm 1 — "the cold reader's undefinable-terms count reaches zero": FAILED, 4 against a target of 0.** I re-took all four myself and every one holds. The six terms the piece put on its list did get their sentences; the four terms nobody thought to list did not. T1 names the shared shape exactly: each is a leaf no rule points back at.

**Arm 2 — "the planted bare closure claim is caught by the new producer rule": PASSED on the reasoning, with the control not preserved.** I re-took T1's reasoning against the actual page text.

The rule, `AGENTS.md:111`: *"Any claim in these files that something is fixed, closed, or done everywhere carries the command that proves it and what it returned — written after the run, never from memory. A closure without runnable proof is an open item wearing a label."*

- **Entry B** — *"fixed everywhere — I went through all the call sites and updated each one."* Two trigger words present, so the rule binds. No command, no return, and "I went through all the call sites" is memory, which the rule excludes by name. **Condemned, correctly.** The producer fired on the case it was built for.
- **Entry A** — carries `grep -rn 'parseDate(' src/` with its return (3 sites) and `npm test` with its return (41 passing). **Accepted as a claim, correctly.** T1 then refused to let it close the finding, on three rules I verified exist and say what T1 says: `AGENTS.md:68` (a control that cannot fail proves nothing), `judge:92` and `judge:94` (a mid-review fix needs a control the judge can run against the pre-fix tree), `judge:96` (sweep siblings before re-testing). That layering — `:111` governs how a claim may be *written*, the re-run rules govern when a fix is *closed* — is real and T1 found it without leaving the pages.

So the instrument discriminates: it condemns the bare claim and accepts the proven one. That is a positive and a negative control on the same rule, which is what the kernel's own law asks for.

**What is missing is the artifact.** The receipt stakes "a planted false closure claim in a **fixture work file**", and there is no fixture. `grep -rn "Entry A" .` returns only T1's own record; `grep -rn "parseDate" .` returns only T1's own record. The entries were supplied in T1's dispatch, not committed, so no later hand can re-run the one catch this producer has. The `Result` field is still `[pending]`, so no closure claim has been written yet and the rule has not been broken — but the landing write-up will make exactly that claim, and under the rule this piece installed it must carry a command someone else can run. Finding 6.

---

## 4. The four rulings

Each stands or falls on its own; none rescues another.

### Works — **YES**, with one defect named inside a working whole

The real dependency here is an agent reading these pages, and the real-path run is T1's: a fresh non-builder context read every loaded page in one pass and acted on them — defined thirty-odd terms with citations, applied the new producer rule to two claims and got both right, and traced a document piece step by step through the loop. That is a run, not a gate. Beside it: my own re-execution of the term greps with controls, the byte measures, the control arm going 4/4 red, and the git chain. The seven texts are at their anchors, no rule was lost, and the pages still read as one method.

Against it, finding 1 — a scenario nobody has hit yet, which is why this is a defect inside a working thing rather than a failure to work.

### Delivers the promise — **BROKEN**

Judged against `CONTRACT.md` promise 6 (*"a smart person who has never seen Speck can follow any document in this repository in one read… a reviewer who stumbles on our vocabulary files it as a defect"*) and the owner's ratified call, **"Define the words."**

The owner asked for the words to be defined. Six were named, four got sentences, and **two of those four sentences are wrong**:

- *"Shaped means the work file is committed with the piece's outcome and proof plan, before any product code"* (`AGENTS.md:109`) drops the third thing step 2 requires — *"and a hard limit on time, tokens, and files read before the first run"* (`:59`) — which is a mandatory field of its own (`templates/piece.md:9`) and the referent step 3 depends on (*"If planning has gone on for a long time and nothing has run, the limit has failed"*). A piece can satisfy the definition of Shaped while violating the step that produces it.
- *"Judged means its review has ruled"* (`AGENTS.md:109`) is contradicted **two sentences below it in the same block**: *"An insufficient judgment sends work back without advancing its state"* (`:111`). A review that ruled *insufficient* has ruled. Read literally, the work is Judged; read against `:111`, `AGENTS.md:86` and `templates/state.md:6`, it is not. One word fixes it: *ruled it sufficient.*

And the cold reader found four more load-bearing words nobody had listed, against a stated outcome of zero. The piece's outcome was written as a property of the whole corpus — *"no load-bearing word on the loaded pages is undefined"* — while its work enumerated six terms. Producing definitions for six cannot produce a property over all, so the first arm of the prediction was going to fail from the moment the piece was shaped. The enumerated items got a producer; the whole-property got only a detector, which is T1.

Partially delivered, materially short of both its own outcome and the owner's call. **Broken.**

### Good to use — **YES**, with the jam named and routed elsewhere

T1 read the whole corpus cold and could act on it: thirty-plus terms defined with citations, the full review cost computed unaided, and *"the pages tell me what to do when things go wrong far more often than they tell me what to do when things go right, which is the correct ratio and rare."* The new sentences are the plain kind — the care level is *"which of these protections are on"*, no abstract scale; the checks floor says a plan naming none *"leaves nothing to pass"*. Those read like a colleague talking.

The document-piece deadlock is real and it is inherited, not built here. It goes on the next piece's list, not against this one.

### Quality hangs together — **BROKEN**

At the sentence level it holds: five of seven texts are pure additions to byte-identical lines, the two rewrites conserve every rule, no new coined word entered (T2's noun-phrase sweep, which I spot-checked), nothing is bolded as a term of art, the budgets have room and the control arm reproduces.

At the corpus level it does not, and for this piece that is the deliverable failing rather than an incidental defect — the whole point was internal coherence of vocabulary.

1. **The admission gate now says two different things on two loaded pages.** `judge:28` gained *"One exception: a fix landed as a build commit during the review does not invalidate the Built line for the tree the review already ran."* `AGENTS.md:78` still says, unqualified, *"It fails if any build commit lands after it… No valid quote means no review."* `AGENTS.md:115`'s tie-break (`product.md` and `decisions.md` win) resolves nothing, because neither page is those. A fix lands mid-review as a build commit: the judge, holding the judge skill, keeps ruling; the conductor, holding only `AGENTS.md` — which every agent always reads — orders a new Built line and a new receipt. Two agents, opposite actions, on the gate that admits reviews. **Introduced by this build, on the exact surface that raised care to two judges, and missed by both testers.**
2. **The ladder says less than the loop it summarises**, in two of four states — above.
3. **The build record carries a number nobody measured.** *"up 2.1 KB from v5.2.1"*; measured **+1,172 bytes (1.1 KB)**, off by 79%. Traced to differencing against `state.md:7`'s 55,157, a figure that does not reproduce under the installer's own file list (`ebb9fb5` measures 56,039 over the same 17 files). So the strain the producer was built to kill reappeared three sentences from where the producer was installed, through the gap in its own trigger: `:111` fires on *fixed, closed, done everywhere* and not on a measurement.
4. Smaller: `AGENTS.md:96` states the Live condition without the owner's grade that three siblings require; `screen drawing` is load-bearing at six sites and defined at none; `README.md:44` says "At v5.2.0" against `package.json` 5.2.1.

Every one is a sentence. Together they are the seam the piece existed to close.

---

## 5. Structure — **STRAINING**, on judgment line 1's undischarged ground

Using the boundary this build installed: straining is the shape making the work slower or riskier while the piece still lands honestly; fighting is the shape making the work wrong or forcing a workaround before it can land.

Nothing was worked around here, and the texts are not wrong — they are short and, in two places, under-stated. The record reports its failed arm plainly rather than dressing it. That is straining.

**The strain, named.** The previous piece's judgment line 1 mandated structural repair with the strain stated as: *"The kernel does not define its own load-bearing words, and nothing in the method produces a definition… The rewrite produced plain words. Nothing yet produces plain meanings."* This piece is that mandated repair. It produced six definitions and one producer — but the producer it built is for **self-reports**, not for definitions. Nothing was added on the definition axis. The detector is unchanged: a cold reader, asked to hunt. T1 proves the point by finding four terms nobody listed, which no step in the method would have caught. **The enumerated six were produced; the property was left with a detector.** The mandated structural repair addressed the list and left the structure where line 1 found it.

Arithmetic, since it decides the next piece: on **this** line the previous ruling was *sound* (judgment 2 of "A builder's words"), so this is line 2's first straining and triggers nothing mechanically. Line 1's chain is its own. But I will say plainly what I think the evidence asks for: the next kernel piece after this one lands should be **a producer for definitions** — a step that makes a new load-bearing word get its sentence when it is introduced — not a third list of words to define.

**A finding about the boundary itself, found by using it.** *"Straining means… but the piece still landed honestly"* makes landing a precondition of the straining ruling. The structure ruling is made inside the same judgment that may route the piece back, so a judge routing a piece back cannot cleanly rule straining and is pushed toward *fighting* by construction — which mandates structural repair on nothing more than a route-back. I had to read "landed honestly" as "was built and reported honestly" to rule at all. That is text 3 needing one more word. T1's H4 found the sentence's other soft edge (it turns on *who* forced the workaround, a subject buried mid-sentence). Two independent readers, two ambiguities, in a sentence written to remove ambiguity. Finding 7.

---

## 6. The two inherited items

**The never-run exemption clause — honestly closed.** I executed both clauses against real cases (§1). Clause 1 correctly denied this repo its exemption and demanded the Built line. Clause 2 correctly grants it to a `map.md` review, and running it shows the clause is load-bearing rather than decorative: without it, every map review in a repo that is building anything deadlocks. The clause behaves as written. One repair is owed (finding 8, the map/map-skill collision), but the item itself is closed and the closure is honest.

**The mid-review-fix silence — NOT honestly closed.** The build record says the resolution was *"written where the contradiction lived, in the judge's receipt check."* The contradiction lived in **two** places: `judge:28` and `AGENTS.md:78` state the same rule, and only one got the exception. The result is not the silence resolved — it is a louder contradiction, on the review-admission gate, between the page every agent always reads and the skill the judge loads. A fix that lands in one of a rule's two homes has not landed. This is the single reason I would route the piece back even if everything else were clean.

The sentence itself, read on its own, is good: its scope ("during the review"), its effect (the Built line stands for the tree already reviewed), and its obligation (the fix answers to the re-run rules, including its own pre-fix control) are all unambiguous and all point at sections that exist (`judge:90–98`). It also sits consistently with `AGENTS.md:88`, which already requires a new Built line covering the *fixed* files. Nothing about the sentence is wrong. It is in one place and needs to be in two.

It has also never fired — no build commit landed after the Built line in this review — so the rule is correct on the page and unproven in application. That belongs in `state.md` as an open uncertainty, not as a closed item.

---

## 7. Verdict, and what the re-test must show

**Insufficient. Route back to build.** The piece keeps the live slot; `map.md` stays unticked; `state.md` says what was ruled and where it routed. No shape or map re-entry: the owner's call is not mis-shaped and the piece-space is not mis-cut. Everything below is text in the pages the piece already touches.

After the fix batch: write a new Built line covering the fixed files in its own state-only commit, open a new receipt quoting it, then re-run **every scenario named here plus one free skeptical attack of the tester's choosing** — reported whether it finds anything or not. Before re-testing, sweep siblings first (`judge:96`), and sweep the one place nobody looked this round: **every other rule stated in both `AGENTS.md` and a skill, where only one copy was edited.** That sweep is what would have caught finding 1.

Controls are quoted so the next hand can fire them against `ac7e688` and watch them go silent at the fix.

| # | Scenario to re-run | Pre-fix control at `ac7e688` |
|---|---|---|
| 1 | `AGENTS.md:78` and `judge:28` state the same rule with the same exception. A fresh reader given only `AGENTS.md`, asked *"a fix landed as a build commit during a review — is the Built line still valid?"*, answers the same as a reader given only the judge skill. | Read both lines: `AGENTS.md:78` says it fails, `judge:28` says it does not. Opposite answers, both pages loaded. |
| 2 | `Shaped` and `Judged` match the steps they summarise. A fresh reader asked *"a review ruled the piece insufficient — is the piece Judged?"* and *"what three things must a work file carry to be Shaped?"* answers correctly from `AGENTS.md:109` alone. | At `ac7e688`, `:109` says *"Judged means its review has ruled"* while `:111` two sentences down says an insufficient judgment does not advance the state; and `:109` names two of the three things `:59` requires. |
| 3 | A fresh cold reader, pages only, counts the undefinable load-bearing terms. Target zero. The four named — `protected code`, `caption` (or a `screen:` token with a template example, matching how `job:`/`moment:`/`claim:` are done), `good to use`, `quality hangs together` — each have a defining sentence. | T1's count of **4** at `ac7e688`, with its method stated. Re-runnable as written. |
| 4 | `screen drawing` has a definition, or the six sites re-anchor on a population that does. | `grep -rinoF "screen drawing"` over the 17 installed files → **6**; no defining sentence at any of them. |
| 5 | Every number in the build record and in `state.md` carries the command that produced it, and reproduces. Includes correcting `state.md:7`'s 55,157 or stating the population it was measured over. | `tot 4a70e03` → 56,176, so the delta to 57,348 is **+1,172**, not 2.1 KB; `tot ebb9fb5` → **56,039**, not the 55,157 `state.md:7` claims, over the installer's own `SURFACE` list. |
| 6 | The planted-claims fixture is committed — as a file, or the two entries quoted verbatim in the work file — so the producer's one watched catch is re-runnable by a later hand. | `grep -rn "Entry A" .` and `grep -rn "parseDate" .` at `ac7e688` return only T1's own record. Nothing to re-run. |
| 7 | The straining/fighting boundary is rulable by a judge who is routing a piece back, and its discriminator (who forced the workaround) survives a hurried read. | At `ac7e688`, *"but the piece still landed honestly"* makes landing a precondition of straining — as this judgment had to work around — and T1's H4 documents the subject-buried-mid-sentence problem. |
| 8 | `judge:24`'s clause B cannot be read as covering the map *skill*. | At `ac7e688`, *"the review's subject is `product.md` or `map.md` itself"* — in a repo whose product is the method and whose build just edited `map-build/SKILL.md`. |
| 9 | Optional, and cheap while the file is open: `AGENTS.md:96` states the Live condition with the owner's grade; `README.md:44` matches `package.json`. | `:96` ends *"the work is proven and can become Live"* with no grade, 13 lines above the definition that requires one. `README.md:44` says "At v5.2.0"; `package.json:3` says 5.2.1. |

Two of these are worth doing whether or not the rest are: **1** (the gate contradiction) and **2** (the two wrong state definitions). If the owner wants this landed tonight, that is the honest minimum, and the re-test is scenarios 1, 2 and 3.

---

## 8. For the owner — two questions the builder cannot answer

**1. How much review should a database change get before it ships?**

The pages have a rule that says some code is "protected" and must be reviewed on its own rather than batched with ordinary changes. But the pages never say which code that is, and two lists in the same document give different answers. One list is *auth, money, privacy, data integrity*. The other adds *schema migrations, regulated behaviour, and anything irreversible*. A database migration is on the second list and not the first — so today, two agents reading the same page could reach opposite conclusions about whether a migration can ride along in a group review or has to be looked at alone.

Which do you want? The narrower list is faster; the wider one means every schema change gets its own review. It is a risk-appetite call, not a wording call, which is why it is yours.

**2. When is the vocabulary finished?**

This piece was ordered to define the words, and it defined the six on the list. A fresh reader who had never seen Speck then found four more that nobody had listed — because the method has a way to *catch* an undefined word (send in a stranger) and no way to *stop one appearing*. Two ways forward:

- **Fix the ten and call it done.** One more round, bounded, and the answer to "is the vocabulary clean?" becomes "clean against a list of ten."
- **Keep going until a cold reader returns zero.** Open-ended — could be two rounds, could be four — and then build the missing step: something that makes a new load-bearing word get its sentence at the moment it is written, so this never comes back.

My recommendation is the second, and specifically the last part of it. The first option buys a clean list; the second buys a kernel that stays clean without being audited. Cost is the difference between roughly one more session and roughly three.

---

## 9. What `state.md` must carry after the fix batch

- The piece is routed back to build, with this judgment and judgment 1 named, and it keeps the live slot.
- The fixed build has not been re-tested. Scenarios 1–8 above are outstanding.
- The mid-review-fix rule at `judge:28` is correct on the page and **has never been applied** — no build commit landed after a Built line in this review. It is unproven in use.
- The definition producer does not exist. Six words were defined; nothing yet produces the seventh.
- `state.md:7`'s own figure of 55,157 does not reproduce (56,039 over the installer's file list at `ebb9fb5`). This is a live bite of the "byte-exact self-measurements" strain already on the wearing-out list, and it propagated into this piece's build record. Count it.
- The report-of-itself strain took another bite this round: one wrong number in the build record, one incomplete closure claim ("written where the contradiction lived"), both caught by fresh hands and neither by the author. That is six bites across three pieces.

## What the next builder should not have to relearn

- **A rule that lives in two files gets fixed in two files.** The one defect that would have blocked this piece on its own is a sentence added to `judge:28` and not to `AGENTS.md:78`. Before editing any rule, grep the rule's own words across all seventeen installed files and count the homes.
- **Run the clause you are told to run against a real case, not a described one.** Executing exemption clause 2 took four minutes and produced two things reading it never would have: proof it is load-bearing, and the map/map-skill collision that only exists in this repo.
- **When an outcome is a property of the whole and the work is a list, the list will pass and the property will fail.** Say up front what *produces* the property, not what would detect it missing.
- **Frequency is the cheapest defect detector in a prose corpus** — T1's line, and it is right. Every one of the four surviving terms appears once, or only as a list item.
