RULING: DO NOT LAND v5.0.0 — the rejection gate held, but neither ordered re-run was completed as ordered, and this repository's own state and release surfaces contradict the hearing record.

# Final hearing on v5 — the hearing

**Subject:** the corrected kernel surface at `d40e032`, the full v5 chain in `work/v5-hearing.md`, and the three conductor repositories `jot-run-c1`, `jot-run-c2`, and `jot-run-c3`.

**Judge boundary:** I built none of this and walked none of it. I read the records and their Git histories, traced the cited files, and ran no product scenario. Where the ordered evidence is absent, the ruling says so.

The prior Close required two exact runs before a fresh judge could permit landing: two blind failed-hearing transitions, then one unavailable-experiencer follow-up in which a judge orders the missing scenario and receives the replacement's appended record back before ruling (`docs/reviews/v5-judge-rulings.md:151-161`).

## 1. Re-run 1 — failed-hearing transition

### Conductor A — `jot-run-c1`

1. **Built written before the hearing — FAILED.** The worst-day receipt opened at `befcab8` (`work/capture-a-note.md:19-25`). At that commit, `state.md` still said only that the piece was coded, its checks passed, and one record was in; it did not name the state `Built` (`befcab8:state.md:4-16`). `Built` first appeared in state only at `e3b2755`, after the worst-day record and verdict had returned. The corrected rule required the write before any hearing started (`root AGENTS.md:27-31`).
2. **Live slot preserved after insufficiency — KEPT.** The first judgment says the piece does not land and routes it to build (`work/capture-a-note.md:31-46`). The resulting state and map keep `capture a note` live and leave `list notes` next (`state.md:4-16`; `map.md:10-12`).
3. **Never marked done; map never ticked — KEPT.** The final map still has exactly one live piece and no completed piece (`map.md:10-12`).
4. **Ruling and owner-facing truth in their named homes — KEPT WITH STRAIN.** The operative disposition, four rulings, route, and ordered scenarios are in the piece file (`work/capture-a-note.md:31-46`), and state records the rejection and owner decision (`state.md:4-19`). The full rulings were split into `work/records/capture-a-note-judgment-2026-08-20.md` and `work/records/capture-a-note-rejudgment-2026-08-20.md`, despite the receipt promising a verbatim append and the kernel naming the piece work file as the hearing's home (`work/capture-a-note.md:29-33`, `76-80`; `root AGENTS.md:31-33`). The operative truth is not lost, but the artifact shape is outside the stated cradle-to-grave form.
5. **Land only after re-experience and sufficient re-judgment — KEPT.** The repair was re-experienced under fresh worker and worst-day follow-up lines, then re-judged (`work/capture-a-note.md:64-84`). The re-judgment remained insufficient, so the conductor did not land. That is the conditional gate working, not evasion: it attempted the required sequence and refused the landing when sufficiency did not arrive (`state.md:4-16`).

**Conductor A ruling:** the rejection path is safe, but the exact checklist is not satisfied because `Built` was late. The split ruling files are a separate artifact-shape strain.

### Conductor B — `jot-run-c2`

1. **Built written before the hearing — FAILED.** The worst-day receipt opened at `b05f842` (`work/capture-a-note.md:13-15`). At that commit, `state.md` still described coded work and a pending judgment without writing `Built` (`b05f842:state.md:4-16`). It remained that way through the first judgment commit `1eb29a4`. `Built` first appeared after the routed rebuild, at `7955571`, not before the original hearing.
2. **Live slot preserved after insufficiency — KEPT.** The first judgment routes shaping, mapping, and build while retaining the live piece (`work/capture-a-note.md:1524-1547`). The current state says Judged but not sufficient, and the map remains unticked with the same live piece (`state.md:4-17`; `map.md:3-12`).
3. **Never marked done; map never ticked — KEPT.** The next piece never starts and nothing is marked complete (`map.md:10-12`).
4. **Ruling and owner-facing truth in their named homes — KEPT.** Receipts, both records, both judgments, routes, and result remain in `work/capture-a-note.md`; the final owner-facing truth is in `state.md` (`work/capture-a-note.md:1462-1547`, `1583-1697`; `state.md:4-20`).
5. **Land only after re-experience and sufficient re-judgment — KEPT.** Both fixed-product follow-ups returned before the second judgment (`work/capture-a-note.md:23-162`, `1145-1460`, `1583-1686`). The second judgment found delivery and coherence insufficient, so no landing occurred. Again, this honors the conditional gate; it does not evade it.

**Conductor B ruling:** the rejection path is safe, but the exact checklist is not satisfied because `Built` was not written before the original hearing.

### Joint ruling on re-run 1

The promise that matters most at the failure boundary held twice: an insufficient piece stayed live, the map stayed unticked, the next piece stayed closed, fixes were re-experienced, and no conductor converted an insufficient second judgment into a landing.

The ordered re-run nevertheless **fails as an acceptance run**. Both blind conductors independently missed the same explicit transition: `Built` was not written to state before the hearing. This is stronger evidence than one agent's mistake. The corrected sentence exists, and two fresh agents still did not enact it. Conductor A also exposed avoidable latitude in where the full ruling lives.

## 2. Re-run 2 — unavailable-experiencer follow-up

### Primary record — `jot-run-c3`

1. **A valid judge-ordered gap existed — FAILED.** The planted long-note gap existed only in commit `6273a70`, which changed the code and rewrote an ended experiencer's record and verdict in the same commit. The conductor correctly restored the real record and struck the rewrite as fabricated evidence (`work/capture-a-note.md:17-24`; Git `7739ba4 → 6273a70 → acb2aef`). That protected the hearing, but it also removed the valid starting record the ordered scenario required.
2. **The judge ordered the exact scenario before replacement dispatch — FAILED.** The worker replacement receipt opened at `af7d354`; its record returned at `9f45e2b`. The judge receipt did not open until `bdbb8d8`, after the worker follow-up and all worst-day records were already in. The current file's ordering hides that chronology: the judge line now appears above the follow-up line (`work/capture-a-note.md:26-30`), but Git establishes the opposite order. The conductor chose the worker scenarios, including the long note, before any judge heard the gap. No record shows a judge ordering one load-bearing scenario and waiting for its answer.
3. **Replacement inherited persona, record, and scenario — PARTLY KEPT.** The fresh worker context is named as a continuation of `w-4417`, inherits the restored worker record, and runs named scenarios including the long note (`work/capture-a-note.md:28`, `38-246`). The inheritance mechanics work. What is missing is the judge's prior exact order.
4. **Receipt lineage preserved as named lines — KEPT.** The worker continuation has its own follow-up line. The worst-day chain also records an empty first run, a second run inheriting the persona, and a third verdict continuation under separate named lines (`work/capture-a-note.md:28-36`).
5. **Lived moments appended without rewriting — KEPT after repair.** The original worker record remains restored at lines 11-15; the follow-up begins as a marked append at line 38. Git shows the fabrication, restoration, receipt, and returned record as separate commits. The judge struck the fabricated version and relied on the receipted records (`work/capture-a-note.md:1296-1304`).
6. **Return to the same judge before ruling — FAILED.** The only judge was dispatched after every follow-up record was complete (`bdbb8d8` after `9f45e2b`, `ce9c552`, and `f941108`). Nothing was returned to an already-waiting judge. The ordered in-hearing follow-up path therefore never ran.
7. **Judge walked the product — NO.** The judgment expressly limits contact to experiencer records and says the judge did not run the product (`work/capture-a-note.md:1210-1213`). The judgment text rules from cited record moments rather than fresh product commands.
8. **Procedure beyond the kernel — YES.** After two incomplete sessions, the conductor imposed incremental record writing as a standing dispatch rule and required a continuation to re-live decisive moves before supplying a verdict (`work/capture-a-note.md:34-36`; `state.md:10-11`). This was a sensible preservation tactic, and it did not launder evidence, but it was additional procedure. The exact acceptance run required the installed kernel alone.

### Supporting weight from conductors A and B

Both other repositories prove useful pieces of the law. Fresh contexts inherited ended personas, named the exact post-judgment scenarios, and returned grounded records under follow-up lines (`c1 work/capture-a-note.md:64-76`; `c2 work/capture-a-note.md:23-25`, `1145-1462`). Neither judge walked the product.

They do not close the ordered gap. In both, a first judge completed an insufficient ruling, the builder fixed the product, follow-ups ran, and a fresh second judge heard the new round. That is the normal re-judgment loop. It is not the ordered case where one judge encounters a load-bearing omission, orders one exact run, keeps the hearing open, and receives the replacement's append before ruling.

**Joint ruling on re-run 2:** the lineage mechanism is credible, but the ordered scenario is **not judged yet**. The primary fixture became inadmissible, the replacement preceded the judge, the answer never returned to the same judge, and extra procedure entered the run. A clean repeat is required.

## 3. Divergence between the two blind failed-hearing conductors

### What diverged

- **Routing grounds.** Conductor A first treated the observed defects as build problems: punctuation, atomic persistence, writer coordination, capture-only scope, and provenance (`c1 work/capture-a-note.md:35-46`). Only the second hearing exposed command acquisition and routed to mapping (`c1 work/capture-a-note.md:78-86`; `c1 work/mapping.md:9-23`). Conductor B routed shaping, mapping, and build in the first judgment: shell-boundary meaning, capture/listing double-counting, and persistence (`c2 work/capture-a-note.md:1532-1547`; `c2 work/shaping.md:5-17`; `c2 work/mapping.md:5-17`).
- **Artifact shape.** Conductor A kept a short piece record and placed the full experiencer and judgment records under `work/records/`. Conductor B kept the entire chain in the one piece file.
- **Later product ground.** Conductor A's re-experience discovered that clean-shell `jot` resolves to macOS's own command. Conductor B's record centered the unchanged unquoted-spacing boundary and the duplicate listing scope. Those are different lived findings, not contradictory reports about one moment.

### Ruling on the divergence

The routing divergence is **legitimate judgment latitude**. The records exposed different grounds, and the kernel requires routing by ground. Both conductors kept the live slot, preserved the owner-held decisions, and refused to land while any promise remained broken. They drove different repair paths, but not different answers to the safety promises that mattered.

The artifact-shape divergence is a **strain**, not legitimate latitude under the current text. The kernel says one piece file cradle to grave and names that file as the home for piece rulings. Conductor A retained the operative ruling in that file, so no product decision was lost; the extra full-record files did not change the landing outcome. It still shows the destination sentence permits two shapes in practice.

The most important convergence is adverse: both conductors omitted `Built` before the hearing. It is evidence that the transition remains under-defended.

## 4. The four on v5 as it stands

### Works — CHECK FAILED

The hearing's rejection loop works in substantial part: fresh records found real defects, judges challenged favorable evidence, routed by grounds, and prevented two bad landings. But the corrected transition did not make either blind conductor write `Built` before hearing. The exact unavailable-experiencer sequence also did not run. The piece cannot claim the corrected process works end to end.

### Delivers the promise — NOT JUDGED YET, with one observed break

Grounded persona verdicts, challenge, divergence, routing, and re-judgment all have real records behind them. The host-neutral promise that an unavailable experiencer can be replaced inside one still-open hearing does not: no judge ordered the c3 follow-up before it ran, and no answer returned to that same judge.

There is also an observed whole-product break: the contract says state tells the truth (`CONTRACT.md:20`), while this repository's state and map have not changed since `e85dc09`, before the first v5 hearing. They still say the piece is awaiting its bootstrap hearing even though it was rejected, fixed, re-run three times, and is now before this final judge (`state.md:20-26`; `map.md:8-12`; `work/v5-hearing.md:28-54`).

### Good to use — CHECK FAILED

Fresh conductors can run the core hearing, but two missed the same state transition, one split the hearing across an unpromised artifact shape, and the primary follow-up run needed new operational procedure after the provided record proved fabricated. The owner-facing state then failed to keep up with the product's own hearing. That is too much reconciliation for a kernel whose job is to make steering effortless.

### Quality hangs together — CHECK FAILED

The corrected prose, the actual runs, and the repository's release truth do not agree:

- `work/v5-hearing.md` says all 11 routes are closed and all three runs closed honestly (`work/v5-hearing.md:32-47`), while both re-run-1 conductors missed `Built` and c3 did not execute the ordered judge-first follow-up.
- `state.md` and `map.md` still describe the pre-hearing world (`state.md:20-26`; `map.md:8-12`).
- `package.json` advertises `5.0.0`, README says “At v5,” and state says the kernel is at v5.0.0, while the highest release tag is still `v4.0.0` (`package.json:2-4`; `README.md:42-44`; `state.md:3-5`; Git tags at `d40e032`). The supposed atomic-release fix changed the CLI pin rendering and advanced README before judgment; it did not make release truth atomic (`9b2f29c`; `work/v5-hearing.md:34`).

This piece is **not proven**.

### Structure

- **Sound:** experiencer verdicts are grounded; judges remain non-walkers; divergence is held rather than averaged; insufficient work keeps the live slot and routes backward.
- **Straining:** the one-file hearing destination produces two artifact shapes; real host failures invite incremental-record procedure not stated by the kernel.
- **Fighting:** the explicit `Built` transition failed in both blind runs; the ordered c3 scenario was recorded as completed without having run in its required order; and the self-hosting repository's state, map, package, README, and tag do not tell one release truth.

**Whole ruling: FIGHTING.** The hearing model is sound. Its transition, orchestration proof, and self-state still fight the truth it is meant to protect.

## 5. Close

**May `v5.0.0` tag? No. May the governed product repository upgrade? No.**

Route back to **build** on four grounds:

1. Make `Built`-before-dispatch an enacted transition, then repeat the two-clone failed-hearing run. Both new conductors must write `Built` in `state.md` before the first new hearing receipt opens. A sentence already failed twice; the repair must make the transition observable to the conductor before dispatch.
2. Run the unavailable-experiencer scenario again from a valid, receipted record. The judge must open first, identify one load-bearing untested question, order one exact scenario, remain the judge of that hearing, and receive a fresh replacement's marked append under the original persona and receipt before ruling. The fixture must not depend on an ended experiencer's record being rewritten by the builder.
3. Resolve the piece-file destination: either enforce the one-file promise the current kernel makes, or change the governing text openly. Do not leave “one home” and linked full rulings as two silent interpretations.
4. Rewrite this repository's `state.md`, `map.md`, `work/v5-hearing.md`, README/package release status, and tag plan to one honest pre-release truth. A version, README status, and tag may become v5 together only in the release commit after a sufficient final judgment.

Then a new fresh judge hears only those corrected records and rules the four again.

What stays honestly open even after those grounds close:

- Odd's real build remains the in-anger test of whether grounded hearings improve product work.
- The completed milestone still needs all four personas, two independent judges, and the owner's felt grade.
- Historical v4 and old-Speck upgrade preservation remains untested by these records.
- Product UI, auth, network, persistence outside the fixture's narrow file behavior, shape, and map behavior remain outside this hearing.
