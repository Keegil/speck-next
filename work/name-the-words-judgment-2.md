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

---

## Continuation (judge 2′), 2026-08-29, on 980e188

**Judge 2′ · Claude Code · model opus · continuing judgment line 2 on the fixed tree.** Built and tested none of it. Blind to line 1. I read judgment 2, the fix batch (`ac7e688..980e188`), the two follow-up runs, and the work file's correction, fix-batch and receipt sections. Every number below has a command behind it that I ran at this hand.

**Ruling in one line: route back to build — narrowly, four clauses.** The two defects that routed this piece back are genuinely closed, and I re-fired the controls to prove it. But the fix batch repeated its own routed-back defect — an edit landing in some of a rule's homes and not all — five more times, and one of those repeats **removed a protection from the protected-code rule while the record told the owner it added one**. That single fact is the ruling. Everything else on this tree I would have landed flagged.

---

### 0. The receipt, and the instrument

**Re-entry receipt: valid.** `c53704e` (build) → `38d9070` (`state.md` only, 1 file; line 26 reads *"the fixed pages are **Built** as of this commit"*) → `980e188` (work file only). `git diff --stat 980e188..HEAD` returns two work files and nothing else, so no build commit lands after the Built line. The quote literally says Built.

**Instrument, before its zeros count.** Over the 17 installed files: `zzqqxx` → **0** (negative), `\bpiece\b` → **88** (positive). It can express a hit and a miss. **Control arm, re-run by me at `980e188`: 4 of 4 tasks red.** Budgets, from the installer's own `SURFACE` list: installed **58,431** of 100,000 across 17 files and 5 skills; always-read (`AGENTS.md`+`state.md`+`product.md`+`map.md`) **24,083** of 50,000. `tot ebb9fb5` → **56,039**, so `state.md`'s corrected figure reproduces at my hand.

---

### 1. Did every route close? Five of nine, and I fired all nine

| # | Scenario from §7 | At `980e188`, my hand |
|---|---|---|
| 1 | admission gate says one thing on both pages | **CLOSED** between `AGENTS.md:78` and `judge:28`, in compatible words. But the rule has a **third** home — `templates/piece.md:15` — still absolute: *"No build commit may land after it… **Otherwise stop**, write Built in a new state-only commit, and open a new receipt."* `grep -ci "one exception"`: `ac7e688` → judge 1, AGENTS 0; `980e188` → judge 1, AGENTS 1, template 0. |
| 2 | Shaped and Judged match their steps | **CLOSED.** `:109` now reads *"outcome, proof plan, and before-first-run limit"* and *"its review ruled it sufficient — a review that sends it back leaves the state where it was."* Both re-read against `:59` and `:111`; no contradiction survives. |
| 3 | the four survivors get defining sentences | **CLOSED.** All four define, and R1′ tested each against a hard case rather than checking presence. The good-to-use / quality-hangs-together split by **source of evidence** (felt moments vs workmanship inspection) is a better repair than the one I asked for. |
| 4 | `screen drawing` defined or re-anchored | **NOT CLOSED.** `grep -ionF "screen drawing"` → **6**, unchanged from `ac7e688`, defining sentence at none. |
| 5 | every number carries its command and reproduces | **HALF CLOSED.** `state.md:7` corrected with its command, and it reproduces. But see §3 — the correction landed in one of the figure's three sites, and the version fix went the wrong way. |
| 6 | the planted-claims fixture committed | **CLOSED.** Both entries verbatim in the work file at `c53704e`; `git grep parseDate c53704e -- work/name-the-words.md` returns them. A later hand can re-run the catch. |
| 7 | straining/fighting rulable on a route-back | **CLOSED.** `judge:63` now adds *"Either can be ruled on a piece that landed or on one sent back."* I ruled structure below without the workaround my predecessor needed — the fix is proved by use. |
| 8 | `judge:24` clause B cannot cover the map *skill* | **NOT CLOSED.** Text unchanged: *"`product.md` or `map.md` itself"*, in a repo whose product is the method. |
| 9 | `AGENTS.md:96` Live condition with the grade; README matches `package.json` | **NOT CLOSED, both halves.** `:96` still ends *"the work is proven and can become Live"* with no grade. README went from one version behind to one version **ahead** — see §3. |

Scenario 9 I marked optional and will not press. Scenarios 4 and 8 I did not mark optional; they are unfixed and I am filing rather than blocking on them, for the reason in §5.

---

### 2. The re-staked prediction: **failed by one, and worth more than the round that passed nothing**

The stake was *zero undefinable terms against a mechanically enumerated population*. R1′ returned **1 against 124**.

I did not re-run a 124-term census, but I audited the producer, which is the part that decides whether the number means anything:

- `cat "${FILES[@]}" | grep -c '[a-zA-Z]'` → **406**. R1′'s claim to have read all 406 is a claim about a real denominator, and the denominator reproduces exactly.
- The membership rule is stated and behavioural (two readings must make an agent *do* different things), and two mechanical extractors ran as a **coverage check on the read** — they found nothing the read missed.
- R1′ then ran a **recall control on its own instrument**, which is the best work in this round: rebuilt `ac7e688`, ran the count-one filter against four defects known to be there, and scored **0 of 4**. The half of the producer that looks like a producer has never found a real defect on this corpus. The census is the producer; the grep is not.

**And the one it missed is `sufficient` — the landing gate.** I re-took it. Nine occurrences across the 17 files; four state what an *insufficient* judgment does (`:62`, `:86`, `:96`, `:111`), none states what makes one sufficient. The available forcing, *sufficient = proven*, is blocked by the corpus: `judge:59` proves work when four rulings stand on evidence, while `judge:57` and `AGENTS.md:109` let a head read "not judged yet" and still reach Judged.

I spot-checked whether this is just how the corpus treats gate words. It is not: `ratified` gets a condition sentence at `AGENTS.md:36`, `substantial` at `AGENTS.md:90` (*"anything that does not meet every small-change condition below; there is no middle class"*). `sufficient` is the outlier.

**This is not hypothetical for me.** I am ruling on whether this piece is sufficient, and the pages do not tell me what the word means. I take the reading that `AGENTS.md:96` and `judge:73–79` support — *sufficient is the judge's call that the work may land, ruled head by head with nothing unproven papered over, findings routed onward with a trace* — and I disclose it, because the other reading (any broken head blocks) is equally available and would land this piece differently. **That fork is the finding, and it is the owner's or the kernel's to close, not the builder's** (`judge:79`).

So: the prediction missed by one, and the round still bought the thing it was staked for. Before: four defects, unknown denominator. Now: one defect, a denominator of 124, a stated membership rule, and a measured recall control showing the cheap half of the instrument is worthless. **The vocabulary job is finite, and the finite thing is the census.** That answers the owner's question 2 with evidence.

---

### 3. The fix batch repeated its own routed-back defect five times

The piece was routed back because *a fix that lands in one of a rule's two homes has not landed*. I swept the rules this batch touched. All five confirmed by execution.

**a. The mid-review exception: three homes, landed in two.** `templates/piece.md:15` still says stop-and-reopen, with no exception. The template is the file a builder copies to open a receipt, so it is the copy most likely to be obeyed at the exact moment the rule fires.

**b. The proof-plan checks: four homes, landed in two.** `map-build:18` and `templates/piece.md:11` now name *"the checks that must pass"*. `AGENTS.md:48` still says *"state the runs, people, and rulings needed to accept it"* — three parts — and `templates/map.md:15` still says *"proof plan: [runs · user types · judge rulings]"*. `AGENTS.md:61` makes the checks the gate to Built. So the always-read page contradicts itself thirteen lines apart. The piece template catches it in practice, which makes this a seam rather than a jam — but it is a seam the batch created, on the pointer it was ordered to close.

**c. `state.md`'s corrected figure: three sites, corrected in one.** `grep -c "55,157" state.md`: **3 at `ac7e688`, 3 at `980e188`** — the count did not move. Line 7 legitimately cites it as the corrected-from value. But line 14 still asserts it as fact to certify a **retired strain** (*"bar met and measured: the kernel only grows — 70,770 → 55,157"*), and line 32 still asserts it inside the **Evidence** section. The same commit that declared the number wrong left it standing twice, once in the section whose entire job is to be citable. Neither tester swept for surviving copies of a corrected number; that is the sweep I would add to `judge:96`.

**d. The version fix went the wrong way, and its record is an uncommanded closure claim.** `README.md:44` now says *"At v5.3.0"*; `package.json:3` says `5.2.1`; `state.md:5` says v5.2.1. The scenario asked README to **match**. It was one version behind; it is now one version ahead of a release that exists nowhere else in the repo, and its own prose still ends at v5.2.0. The fix record's line — *"README version current"* — is a closure claim carrying no command, and false, in the same commit as the rule widened to forbid exactly that. Seventh bite of the report-of-itself strain.

**e. The one I will not land.** Detailed next.

---

### 4. Protected code: not a widening, and the flag says it is

**Measured.** `grep -ohiE "data.integrity"` over the 17 installed files: **`ac7e688` → 1, `980e188` → 0.** The phrase is gone from the kernel.

Pre-fix, `AGENTS.md:119`: a change is small only if it *"touches no **auth, money, privacy, or data-integrity code**"*. Post-fix: *"touches no **protected code**"*, with `:121` defining protected code as *"everything on the risky list below — auth, money, private data, schema migrations, regulated behavior, anything irreversible."*

**The two lists cross; they do not nest.** Added to protection: schema migrations, regulated behavior, anything irreversible. Removed from protection: **data-integrity code that is not a schema migration and not irreversible** — a de-duplication routine, a reconciliation job, an aggregation that writes derived state, a constraint enforced in application code. That work was excluded from the small-change path an hour ago. Today it qualifies: no work file, no receipt, no fresh tester, no judge.

Three things compound, and the third is the ruling:

1. **The record misdescribes it to the owner.** `work/name-the-words.md:35`: *"the wider definition is landed (schema migrations can never ride in a batch review); strike it if you want the narrow, faster reading."* It is not a widening. And the fork offered is not the fork that exists: "strike it for speed" would in fact *restore* a protection, which the sentence does not say. **The owner cannot make the call he is being handed**, and being understood is the deliverable.
2. **The authority cited forbids the change.** The builder derived it from `CONTRACT.md:48` — *"Care where the risk is — small stays cheap, and risky paths never get to call themselves small."* That clause was cited as warrant for a change that lets one risky path call itself small.
3. **The method's own law is one-directional.** `AGENTS.md:123`: *"You may raise the care level. You may never lower it."* This lowered it, on the highest-care surface in the kernel — the definition of protected code — inside a piece about wording.

My predecessor put this to the owner in §8 as *"a risk-appetite call, not a wording call, which is why it is yours."* It was answered without him and described as something it is not.

**The repair needs no owner at all.** Adding *data integrity* to the risky list at `:121` is a strict widening — permitted unilaterally by `:123`, and it makes the record's sentence true. Only then does the owner's real question (narrow and fast, or wide with every schema migration reviewed alone) become answerable.

A flagged item lands when the flag is true. This flag points the wrong way on protected code. That is why the piece does not land tonight.

---

### 5. The four rulings

**Works — YES.** Fresh non-builder contexts read these pages and acted on them: R1′ read all 406 non-blank lines and produced a census with a recall control; R2′ executed twelve pre-fix controls, all silent at `ac7e688` and all firing at `980e188`. Beside that, at my hand: the receipt chain, the byte measures, the term greps with both controls, the control arm 4 of 4 red. The document-piece deadlock is genuinely gone — `AGENTS.md:113` now states the forward path (*"names runnable checks in its proof plan — greps, probes, measurements"*) and the field it needs exists at `map-build:18` and `templates/piece.md:11`, so `judge:24`'s *"when in doubt, demand the Built line"* now points at the fix instead of the jam. That was the worst inherited defect in the round and it closed cleanly.

**Delivers the promise — BROKEN, and much less broken.** The owner asked for the words to be defined. Ten now are, each tested against a hard case rather than checked for presence, and the population is enumerated for the first time. Against that: the piece's own stated outcome — *no load-bearing word on the loaded pages is undefined* — is missed by one, and the one is the word that decides landings. Under non-compensation that is a broken head, stated plainly, on a piece that delivered most of what it promised.

**Good to use — YES.** R1′ would run a product under these pages *"with more confidence than T1 had"*, and its reasons are specific: the two heads separate by source of evidence, the caption convention is auditable rather than fixed, the widening to measured numbers condemned a sentence that was clean one commit earlier. The new sentences read like a colleague talking. `AGENTS.md` grew 12,457 → 13,049 bytes for eleven fixes; no page got heavier to read.

**Quality hangs together — BROKEN.** At the sentence level it holds: R2′'s word-diff found six changed product lines carrying eleven fixes, five deletions rewrite-noise inside conserved sentences, two substantive and both conserving. At the corpus level it does not, and for this piece that is the deliverable failing: five one-sided edits in a batch whose route-back reason was a one-sided edit (§3), plus the protected-code crossing (§4). `map-build:28`'s caption is now defined and still has no producer — no template for a deck, journey, or screen drawing exists, and no rule obliges a screen to carry a title line, so the gate is *reportable* rather than runnable, which reads more like evidence than the undefined version did (R2′'s finding 15, confirmed).

---

### 6. Structure — **STRAINING**, and the strain has a name

Using the boundary this batch installed, and I could apply it to a routed-back piece without straining the sentence — the fix works.

Nothing was worked around and nothing was hidden: R2′ reported against its own dispatcher, R1′ overturned T1's count and applied the piece's own new rule to T1's record to do it. The work stayed honest. **Straining.**

**The strain:** *the method detects one-sided edits and does not prevent them.* `judge:96` orders a sibling sweep, and it works — it caught every item in §3. But it fires at **re-test** time, performed by a tester, after the batch is written. Nothing fires at **edit** time, at the builder's hand, when the rule's other homes are one grep away. So the loop's cost for a multi-home rule is a full extra review round, every time. It cost one this round and it is about to cost another.

**Arithmetic, stated honestly rather than manufactured.** On this line the previous piece ruled *sound*, and this continuation completes judgment 2's ruling on the same piece rather than adding a second. That is **one** straining ruling, not two, so `judge:63`'s trigger does **not** fire mechanically. I will not pretend otherwise. But both judges and both testers converged independently on the same next piece, so I will say it plainly: the next kernel piece should be **two producers, not another list** — one that makes a rule's other homes get the same edit when it is written, and one that makes a new load-bearing word get its sentence when it is introduced. R1′'s recall control is the evidence for the second: a frequency filter would run green forever while `sufficient` sat undefined at nine occurrences.

---

### 7. Verdict, and the exact scenarios

**Insufficient. Route back to build.** The piece keeps the live slot, `map.md` stays unticked, `state.md` says what was ruled and where it routed. No shape or map re-entry: the owner's call is not mis-shaped and the piece-space is not mis-cut. Four clauses, all in pages the piece already touches. Then a re-test of these four only, plus one free attack.

I am scoping this hard on purpose. The honest minimum I named last round (scenarios 1, 2, 3) is **done**. What blocks landing is not the unfixed backlog — it is the five defects the batch **created**, and the mandatory set is only the ones that drop a protection or contradict a rule the batch itself edited. Grinding the rest one at a time is the shape that has now failed twice; it belongs to the producer piece.

| # | Must show | Pre-fix control, executable at `980e188` |
|---|---|---|
| **M1** | *data integrity* is on the risky list at `AGENTS.md:121`, and the owner note says what actually changed: schema migrations, regulated behavior and irreversible work were **added** to protection; nothing was removed. | `grep -ohiE "data.integrity"` over the 17 installed files → **0** at `980e188`, **1** at `ac7e688`. `work/name-the-words.md:35` calls the change *"the wider definition"*. |
| **M2** | The proof plan names its checks in all four homes. A mapper reading `AGENTS.md:48` or filling `templates/map.md:15` writes a plan that `AGENTS.md:61` will accept. | `grep -c "checks that must pass"`: `map-build` 1, `templates/piece.md` 1, `AGENTS.md` **0**, `templates/map.md` **0** — while `:61` says a plan naming no checks cannot become Built. |
| **M3** | The mid-review exception is in all three homes. A builder given only `templates/piece.md` answers *"a fix landed as a build commit during the review — is the Built line still valid?"* the same as a reader of `AGENTS.md` or the judge skill. | `templates/piece.md:15` at `980e188`: *"No build commit may land after it… Otherwise stop"* — no exception, opposite answer to `AGENTS.md:78` and `judge:28`. |
| **M4** | The record's own numbers are true. No surviving assertion of 55,157; `README.md` and `package.json` state the same version at the commit they land in; the *"README version current"* line carries its command or goes. | `grep -c "55,157" state.md` → **3** at both trees, with lines 14 and 32 still asserting it (line 32 in **Evidence**). `README.md:44` "v5.3.0" vs `package.json:3` "5.2.1" vs `state.md:5` "v5.2.1". |

Then: a new Built line covering the fixed files in its own state-only commit, a new receipt quoting it, **re-run M1–M4 plus one free skeptical attack of the tester's choosing** — reported whether it finds anything or not — and, before re-testing, sweep siblings (`judge:96`) with one addition this round earned: **also sweep for surviving copies of any number the batch corrected.**

**Filed, not fixed — for the producer piece, not for another grind round.** `sufficient` (the landing gate, §2 — owner's or kernel's call, not the builder's) · `screen drawing`, 6 load-bearing sites, no definition · `judge:24` clause B vs the map *skill* · `AGENTS.md:96`'s Live condition without the grade · the safety net at three different bars (`AGENTS.md:68` "you watched it fail" / `judge:69` "a record shows it" / `templates/piece.md:11` agentless) · `AGENTS.md:88` dropping the free attack that `:62` and `judge:96` require · the fourth head named *"holds together as a quality product"* at `AGENTS.md:94` and *"quality hangs together"* everywhere else · `AGENTS.md:42` and `:52` mandating shaping and mapping reviews that `:74`/`:78`, read alone, forbid · `the gates`, `the declared bar`, `current dependency`, `fidelity gap`, `accounting summary` · the caption's missing producer.

---

### 8. For the owner — two questions, restated so they can be answered

**1. Should a change to data-integrity code get its own review?**

Some code is "protected": it can never be treated as a quick fix, and always gets its own review. The list of what counts just changed, and I am blocking the release over how it changed.

It used to be: anything touching **logins, money, privacy, or the correctness of stored data**. It is now: anything touching **logins, money, private data, database schema changes, regulated behaviour, or anything you cannot undo**.

Read that twice and you will see database changes and irreversible actions were *added* — good — and **the correctness of stored data quietly dropped off**. So a change to the code that keeps records from being double-counted or silently corrupted would today qualify as a quick fix: no write-up, no fresh reviewer, no judge. The note in the work file told you this change was purely a widening. It is not, and I have asked for that fixed before anything ships.

Once it is fixed, your actual question is the one my last judgment asked and the builder answered without you: **do you want the wide list or the narrow one?** Wide means every database schema change gets its own review — slower, safer. Narrow means schema changes can ride along with ordinary work — faster, and one more thing that can go wrong quietly. My recommendation is wide, because this is the one place in the method where being slow is the product.

**2. What makes work good enough to ship?**

The whole method turns on one judge saying a piece is "sufficient" — that is the word that decides whether work ships or goes back. Nowhere do the pages say what sufficient means. Every mention says what happens *after* an insufficient ruling; none says what makes one.

I hit this ruling on this very piece, and I had to pick a reading and tell you which: I took *the judge may ship it and send the remaining problem onward as a tracked finding*. The other honest reading is *any broken part blocks shipping*. Two careful judges, the same evidence, opposite decisions about whether your product ships this week.

Two ways to close it:

- **Say "any broken part blocks."** Simple, strict, and it will hold pieces for problems that were never in their scope.
- **Say "the judge may ship it, and must name what is still open and where it went."** Keeps things moving and puts the weight on the judge's honesty — which is what the rest of the method already assumes.

My recommendation is the second, with the requirement that anything still open is written into `state.md` before landing. It costs one sentence and it is the sentence the whole loop turns on.

---

## What the next builder should not have to relearn

- **Finish the sweep you were routed back for, on the rules you are editing.** This batch was sent back for a rule fixed in one of two homes, and it edited five more rules in some of their homes and not all. The sweep costs one grep per rule and it would have caught every item in §3.
- **A corrected number has to be corrected everywhere it was asserted.** `grep -c` for the old figure returned the same count before and after the correction. Correcting the sentence you were caught on is not correcting the claim.
- **When you answer the owner's question yourself, the flag you leave has to be true.** The protected-code note said "wider" about a change that crossed. A wrong flag is worse than no flag, because it spends the owner's trust to skip his judgment.
- **Widen first, then ask.** Restoring a protection needs no permission (`AGENTS.md:123`). Removing one needs the owner. When a definition swap does both, land the widening and ask about the narrowing — never ship the pair as one "widening".
- **A gate word explains itself well enough to keep reading, which is how it stays undefined.** `sufficient` survived a rewrite, a cold reader, two blind judges, an eleven-item fix batch and two follow-up runs. Meanwhile `ratified` and `substantial` both carry condition sentences. Sweep the words that decide whether work moves, and demand a condition for each, not a consequence.

---

## Final ruling (judge 2″), 2026-08-29, on b8e2ce9

**Judge 2″ · Claude Code · model opus · closing judgment line 2.** Built and tested none of it. Blind to line 1. I read judgment 2 and its continuation, R″'s follow-up, the second fix batch (`980e188..f3e7a62`), and the work file's second-batch and owner sections. Every number below has a command behind it that I ran at this hand.

**Ruling in one line: sufficient. The piece lands, and releases as v5.3.0 — on four conditions that live inside the landing commit itself.** All four clauses I ordered are closed, and I fired every one of them on both trees. The free attack found a real eighth bite of the report-of-itself strain, and I am not routing back for it: the number it found is inherited rather than minted here, the method's own small-change rule says its repair needs no ceremony, and the release commit this ruling authorizes is the one commit that touches all four of its homes. A third route-back for three line-edits is the grind I said had already failed twice.

---

### 0. The chain, and my own instrument

**Second re-entry receipt: valid.** `f3e7a62` (build, 18:28:18 — `AGENTS.md`, `README.md`, `state.md`, two templates, the work file) → `03d8b10` (parent `f3e7a62`, **`state.md` only**, 1 file / 1 insertion / 1 deletion, line 26: *"the re-fixed pages are **Built** as of this commit"*) → `b8e2ce9` (parent `03d8b10`, work file only, 3 insertions). The quote literally says Built. `git diff --stat 03d8b10..HEAD` returns two work files and nothing else, so no build commit lands after the Built line. Working tree clean.

**My instrument, before its zeros count.** Over the 17 installed files on both trees: `zzqqxx` → **0**, `piece` → **116**. It expresses a hit and a miss.

**And it lied to me once first, in the way R″ warned about.** My first sweep for *privacy* and *private data* used `git grep -ionE "\bprivacy\b|..."` and returned **0 and 0 on both trees** — a clean, quiet, wrong answer, because `\b` is not a word boundary in POSIX ERE and git grep defaults to ERE. The text is plainly there. Re-run with `-P` and both controls, it reads 2/2 at `ac7e688` and 1/3 at `b8e2ce9`. Recorded because it is the third false zero this piece has produced from a shell detail, and because a zero I could have filed is exactly what my own §7 asks me to catch before it counts.

**Budgets and control arm, at my hand at `b8e2ce9`.** Installed surface **58,636 bytes** of 100,000 across **17 files** and **5 skills**; always-read set 13,133 + 5,972 + 596 + 4,600 = **24,301** of 50,000. `tot ebb9fb5` → **56,039**, so the figure the batch installed reproduces. `./devsuite/run.sh --control` → **4 of 4 tasks red**. Every key check still expresses the failure it claims to prevent.

---

### 1. The four ordered clauses, fired on both trees

| # | What it had to show | `980e188` | `b8e2ce9` |
|---|---|---|---|
| **M1** | *data integrity* on the protected and risky lists | **0** | **2** — `AGENTS.md:121` and `:123` |
| **M2** | the proof plan names its checks in all four homes | **2 of 4** | **4 of 4** |
| **M3** | the mid-review exception in `templates/piece.md` | **0** | **1** |
| **M4a** | the three version strings agree | **no** (5.3.0 / 5.2.1 / 5.2.1) | **yes** (5.2.1 ×3) |
| **M4b** | no surviving *assertion* of 55,157 in `state.md` | **3** | **1**, and it is the disclaimer |

**M1 — closed, and the protection actually routes.** I traced it rather than counting it: `AGENTS.md:119` conditions a small change on *"touches no protected code"*, `:121` defines protected code as the risky list **including data integrity**, and `:123` carries the same term into the care rule. A de-duplication routine now fails the small-change test through a live pointer, not a hopeful one. This was the single fact that blocked the piece, and it is gone.

**M2 — closed on every side.** All four spec homes now list the same four parts in the same order: `AGENTS.md:48`, `map-build:18`, `templates/map.md:15`, `templates/piece.md:11`. `AGENTS.md:61` — *"Its own checks are the checks named in the piece's proof plan; a plan naming none leaves nothing to pass"* — now points at a field that exists wherever a mapper might be standing. The dangling pointer is closed, which is more than I asked for: I asked for four homes, and what landed is four homes that agree word for word.

**M3 — closed.** The exception is in all three homes in compatible words. Note for the record that R2′'s pattern (`one exception`) reads **0** in the template on *both* trees and would have filed a false red; on a pattern that can fire (`during the review`) it reads **0 → 1**. R″ caught that and reported it as an instrument fault rather than a finding. Correct handling.

**M4a — closed, and the version they agree on is real.** `git tag -l` lists `v5.2.1`. The previous state announced a release that existed nowhere; this one does not.

**M4b — closed on the condition I actually wrote.** My clause was *"no surviving assertion of 55,157"*. The one survivor at `state.md:7` does not assert it — it disclaims it (*"the earlier recorded 55,157 was a working-tree read at the wrong moment, corrected under the measured-numbers rule"*), which is the site my continuation blessed by name. Lines 14 and 32, the two I condemned — one certifying a retired strain, one inside **Evidence** — both now carry the pinned reproducible measure. A correction that erased its own provenance would have been worse.

**Conservation, checked myself.** `git diff --word-diff` over the method pages, `980e188..f3e7a62`: **zero deletions**. Across the whole batch including `README.md` and `state.md`, six deleted tokens, all digits (`5.3.0`→`5.2.1`, `55,157`→`56,039` twice). Every page edit is a pure insertion into an otherwise byte-identical line. No new coined word. **+205 bytes.** This is the first batch in the piece whose product-page edits delete nothing.

**No regression on what I had already closed.** `AGENTS.md` still reads *"ruled it sufficient"* and still carries the before-first-run limit in Shaped; `judge:63` still reads *"landed or on one sent back"*; the planted-claims fixture is still in the work file; the admission gate is in all three homes.

---

### 2. The free attack, taken seriously — and why it does not route the piece back

R″ pointed its free attack at the fifth family, the one my own re-test order named in as many words (*"also sweep for surviving copies of any number the batch corrected"*). I re-took all of it:

- `decisions.md:5` still asserts **70,770 → 55,157 (−22%)**, while `state.md:7` says 56,039. Two files disagree about one measurement, and `AGENTS.md:115` hands the win to `decisions.md`.
- The derived percentage survives in **three** homes: `README.md:44`, `decisions.md:5`, `map.md:14`. The truth is **−20.82%**; 55,157 implies **−22.06%**.
- Both are uncommanded measured numbers under `AGENTS.md:111` **as this very piece widened it**.

The finding is real, it is the strain's eighth bite, and it is aggravated exactly as R″ says: the surviving copy sits in the file the method page says wins, and the sweep that would have found it was written into the order the batch was executing. The batch ran the quoted control (`grep -c "55,157" state.md`) instead of the requirement above it.

**I am still not routing back, and the reasons are structural rather than merciful.**

1. **The batch did not mint this number; it made the tree more truthful.** Before `f3e7a62` the figure was wrong in four places and consistent. After, it is right in the three places the batch touched and wrong in one authoritative file. That is a defect *created* — the disagreement is new — but the falsehood is inherited from the v5.2.0 landing.
2. **The method classifies the repair as needing no ceremony.** Correcting three sentences adds no dependency, touches no protected code, changes no promise, and is reversible in one commit — a small change by `AGENTS.md:119`. Routing a piece back to *build* for work the kernel says needs no work file, no receipt, no tester and no judge would be the method contradicting itself in front of me.
3. **The obligation already binds without my ruling.** `AGENTS.md:115`'s second sentence — *"Measured evidence beats every document, so fix the losing document and cite the finding"* — fires on R″'s measurement, not on my verdict.
4. **The occasion that consumes it is the next commit.** A v5.3.0 release moves `README.md`, `package.json` and `state.md` together, adds a `decisions.md` entry, and ticks the piece on `map.md`. That commit touches every home of the wrong figure. This is not a promise with no reader; it is a correction landing in the commit this ruling authorizes.
5. **The shape I would be repeating has failed twice.** My continuation ruled that grinding one item at a time is the failed shape and the repair is a producer. A third route-back for three line-edits is that shape again.

So it lands as a **condition on the landing commit**, not as a route-back and not as a filing. §6 states it with its check.

---

### 3. Privacy — one word, found late, and it goes in the same commit

R″'s finding 18, re-measured at my hand with `-P` after my own false zero: the pre-first-batch small-change rule read *"auth, money, **privacy**, or data-integrity code"* (`ac7e688:AGENTS.md:119`). The landed protected list reads *"auth, money, **private data**, data integrity, …"*. `privacy` now appears nowhere in `AGENTS.md`; its only site in the installed set is `map-build/references/questions.md:28`, an unrelated sentence.

On a literal reading that narrows. Consent capture, a retention-policy toggle, a telemetry opt-out are privacy work without being private-data work. It is a far smaller crossing than the one I blocked on — *regulated behavior* and *private data*, both added, cover most of the ground, where data integrity had no covering term at all — and it was introduced by the **first** batch, was live when I ruled last round, and I did not name it. It is not in my ordered set and it does not re-block.

But it makes one clause of the owner paragraph false: *"the old four **plus** … — **nothing lost**, three things added."* Three of the old four survive; the fourth was swapped. That is the exact phrase whose falsity routed this piece back, in the same sentence position, now wrong by one term.

The repair needs no owner and costs one word: put *privacy* back on `AGENTS.md:121`. A strict widening is permitted unilaterally by `:123`, and it makes the sentence true rather than requiring the sentence to be softened. Condition C3.

---

### 4. The four rulings

Each stands on its own; none rescues another.

**Works — YES.** Fresh non-builder contexts read these pages and acted on them: R1′'s 124-term census with a measured recall control, R2′'s twelve pre-fix controls, R″'s combined final run with its instrument rebuilt after three false zeros. Beside that, at my own hand: the receipt chain proved with git, the term greps with both controls over 17 files, the budgets, the control arm 4 of 4 red, all four ordered clauses fired on both trees, and the protected-code pointer traced from `:119` through `:121` to a term that is actually there.

**Delivers the promise — YES, with the one remaining word named and routed to the owner.** I ruled this head BROKEN twice, and I am flipping it on the closure of the grounds I actually routed on, not on softened standards. My continuation routed on two things: the piece's own outcome missed by one word, and a protected-code record that told the owner the opposite of what the tree did. The second is repaired and verified. The first is `sufficient`, which my continuation filed **to the owner, not to build** — *"the owner's or the kernel's to close, not the builder's"* (`judge:79`) — and a head cannot stay broken on an item the builder is forbidden to fix. Against the owner's actual call, *"Define the words"*: ten words defined and each tested against a hard case, a mechanically enumerated population of 124 where there was no denominator at all, a producer for self-reports that condemned a planted claim on first contact, and a measured recall control proving the cheap half of the instrument worthless. That is delivered.

**Good to use — YES.** The pages got more usable in the places a builder actually stands: a mapper filling any of four homes now writes a plan the Built gate accepts; a builder holding only the piece template answers the mid-review question the same as the judge; the protected list is a strict superset on every substantive element. Zero deletions, no coinage, +205 bytes. The owner paragraph is the weak surface — it never lists the four terms it asks him to choose between, and it drops one of judge 1's three options — but that is a defect in the **ask**, and the ask has not been made yet. It is a landing condition (§6), not a property of the pages.

**Quality hangs together — YES, and the condition is what makes that honest.** At the sentence level this is the cleanest batch in the piece: zero deletions on the method pages, six digit tokens in the whole diff, no new term of art. At the corpus level, on the four families the batch was ordered to sweep it reached **every home** — the first time that is true in this piece. Against it, one family reached one home of four: the corrected figure, surviving in the file the tie-break favours. I will not call that head broken on an inherited number that the piece's own new rule is what condemns, and I will not call it whole while the number stands. So it is ruled on the landing commit: **the corrections in §6 are part of the commit I am ruling sufficient.** A landing commit without them is not the commit I ruled on, and the head is broken until it carries them.

---

### 5. Structure — **STRAINING**, and the strain has a sharper name than "one-sided edits"

Nothing was worked around, and nothing was hidden. The batch's own record names the strain's seventh bite against itself. R″ reported its own three false zeros before any of its numbers, and reported against its dispatcher. The work stayed honest. **Straining.**

**The strain, named precisely: the quoted control becomes the requirement.** My re-test order gave both a requirement (*"No surviving assertion of 55,157"*) and a control scoped to where the defect was found (`grep -c "55,157" state.md`). The batch executed the control. This is not carelessness and it is not a second instance of "a rule fixed in one home" — it is the mechanism *behind* that pattern, and it is created by the judge, not the builder. A judge writes a control by pointing at the site where the finding surfaced; the builder reads the control as the specification, because the control is the executable thing and the requirement is prose. Every one-sided edit in this piece has this shape.

That has a repair, and it belongs with the two producers already converged on: **a judge's control names its population, not its site.** Had mine read `git grep -inF "55,157" -- ':!work/'` instead of `grep -c "55,157" state.md`, the batch would have swept `decisions.md` while executing the control literally.

**Arithmetic, stated honestly.** On this line the previous piece ruled *sound*, and this closes judgment 2's ruling on the same piece rather than adding a second — one straining ruling, not three. `judge:63`'s trigger does **not** fire mechanically, and I will not manufacture it. But both judgment lines and all four tester runs have now converged on the same next piece, so I will say it plainly: the next kernel piece is **producers, not another list** — one that makes a rule's other homes get the same edit when it is written, one that makes a new load-bearing word get its sentence when it is introduced, and now a third, cheapest of the three: a control carries the population it must be true over.

---

### 6. The landing commit — four conditions, each with its check

Sufficient is granted **on this commit**. Each condition is mechanically checkable, and a landing commit that omits one is not the commit this ruling covers.

| # | Condition | Check that must pass at the landing commit |
|---|---|---|
| **C1** | `decisions.md:5` carries the reproducible figure — 70,770 → **56,039** — with the pinned command, citing this finding, per `AGENTS.md:115`'s own second sentence. | `git grep -inF "55,157" HEAD -- ':!work/' ':!docs/'` returns **only** `state.md:7`, the corrected-from disclaimer. |
| **C2** | The derived percentage is corrected in all three homes — `README.md:44`, `decisions.md:5`, `map.md:14` — to **−20.8%**. | `git grep -inE "22%" HEAD -- ':!work/' ':!docs/'` → **0**. Pre-fix at `b8e2ce9`: **3**. |
| **C3** | *privacy* is back on `AGENTS.md:121`'s protected list — a strict widening, permitted by `:123` without the owner — and the owner paragraph's *"nothing lost"* is true. | `git grep -icP "privacy" HEAD -- AGENTS.md` → **1**. Pre-fix at `b8e2ce9`: **0**. |
| **C4** | `state.md` is rewritten from the evidence at landing, per step 5: the report-of-itself strain reads **eight** bites, and the two judge-filed owner questions (`sufficient`; wide-or-narrow protected code) move out of *"Nothing waiting"* into **What needs the owner**. | `grep -c "Nothing waiting" state.md` → **0**. Pre-fix at `b8e2ce9`: **1**, while two owner questions stood filed by both lines. |

C1 and C2 are the free attack's findings 16 and 17; C3 is finding 18; C4 is step 5's own obligation, which the current file does not meet. All four are one line each, all four land in the release commit that moves the version strings together, and none needs a tester or a judge under `AGENTS.md:119`.

**And a note to the conductor, not a condition, because it governs the ask rather than the tree.** When the owner is asked, `sufficient` arrives as its own question with options and a recommendation — the text exists at §8 of this document — and the protected-code question names the four terms it asks him to choose between and carries judge 1's third option. Right now `sufficient` sits as item 1 of a ten-item filed list under a paragraph that opens *"two things."* A question that decides whether work ships, buried in a list, is the shape the conductor law names as a defect.

---

### 7. For the owner — the same two questions, both now answerable

**1. Should a change to data-correctness code get its own review?** The block is lifted: the protection that had quietly dropped off — *the correctness of stored data* — is back on the list, so nothing is lost any more and three things are added (database schema changes, regulated behaviour, anything you cannot undo). Your real question stands, and it is a risk-appetite call, not a wording one: keep the **wide** wall, where every schema change gets its own review — slower, safer — or narrow it back to the original four, which is faster and lets a schema change ride along with ordinary work. My recommendation is wide, because this is the one place in the method where being slow is the product. Judge 1 offers a third option worth hearing: protect data-correctness code only where it can actually lose or corrupt stored records.

**2. What makes work good enough to ship?** Unchanged from my last judgment, and I hit it again ruling this piece. The pages never say what *sufficient* means; every mention says what happens after an insufficient ruling, none says what makes one. I took the reading that a judge may land a piece while naming what stays open — and you can see me doing exactly that above, landing this piece with four named conditions. The other honest reading is that any broken part blocks. Two careful judges, the same evidence, opposite decisions about whether your product ships this week. My recommendation is the first, with the requirement that anything still open is written into `state.md` before landing. It costs one sentence and it is the sentence the whole loop turns on.

---

## What the next builder should not have to relearn

- **A control names its population, not the site where the defect was found.** Every one-sided edit in this piece traces to a builder executing the judge's quoted control literally when the control was scoped narrower than the requirement above it. That is the judge's fault, not the builder's, and it is fixed on the judge's side for one grep flag.
- **Correcting a number where you were caught is not correcting the number.** Three rounds running, the same shape. The sweep is `git grep` over the whole tree with `':!work/'`, not `grep` over the file the finding named.
- **A widening needs no permission, so take it before asking anything.** *privacy* went back on the list in the same commit as the piece landed, because restoring a protection is always allowed and always makes the owner's question cleaner.
- **Check your own instrument in the shell you are actually in.** `\b` is not a word boundary in git grep's default ERE, and it returns a clean, silent, wrong zero. That is three false zeros in this piece from three different shell details, and every one of them would have been a filed finding.
