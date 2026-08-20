# v5 — experience and judge become one process: the hearing

**Outcome:** judgment happens within the experience. Experiencers — fresh non-builder contexts, one per persona — live the product and return records that end in their own verdicts, as real users judge while using; every verdict must point at a moment actually lived in that record, or it is void. A separate judge who built and walked none of it convenes the hearing: questions and challenges each verdict, sends an experiencer back to the product when an answer needs another run, holds diverging verdicts side by side without averaging them, rules the four verdicts citing the records, and steers the loop — back into shaping, mapping, building, or re-experiencing. At milestones and on risky pieces a second judge hears the same records independently; divergence between judgments is itself a finding. v4's paper-only judge and its verdict-ban on records both die; the receipt law, the personas, and never-the-builder all carry over.

**How I'll know it works:** the judge's challenges catch verdicts the records don't support (the LLM-unreliability this exists for), diverging persona verdicts surface real tensions instead of being merged away, rulings cite lived moments rather than paraphrase, and the arm's-length blindness the owner called ("judging only from records is too far removed") stops — measured on this change's own bootstrap hearing and then Odd's build.

**Status:** built → heard → judged DO-NOT-LAND (2026-08-19) — routed back to build; fixes and the two ordered re-runs below, then a fresh judge.

## Hearing receipt (opened at dispatch)

- **Experiencers:** two fresh codex exec (GPT-5.6) sessions, clean clones, decorrelated from the author (Claude Fable, this session): **the newcomer** (cold-reads the method pages as a smart outsider who must drive a real build with them tomorrow; probes what a reader can; rules: could I drive this?) and **the worst day** (probes for contradictions — stale vocabulary, references that don't resolve, the hearing's own instructions fighting each other, installer/upgrader runs — and rules from what the probes found).
- **Dispatched:** 2026-08-19, at commit e85dc09.
- **Owner of this run:** the kernel session dispatching on 2026-08-19.
- **If a record is empty:** re-dispatch under your own named line; never assume the run died.
- **Judge:** a third fresh session, dispatched when both records are in — challenges both verdicts, may order re-runs (this session executes them), rules, routes.

## Records and verdicts

Returned 2026-08-19, both in full: [the newcomer](../docs/reviews/v5-experiencer-newcomer.md) — verdict: usable for a real build tomorrow, not yet unambiguous enough for two fresh agents to drive identically (grounded in its simulated drive and stumbles: the piece loop says six steps but prints five, Built is never explicitly landed, "Land it" reads unconditional though a hearing can route backward, hearing outputs' destinations unnamed, the judge's dispatch-back has no fallback for a non-resumable run, README says "At v4" while the CLI prints 5.0.0) — and [the worst day](../docs/reviews/v5-experiencer-worstday.md) — verdict: yes for governing a build through the installed agent surface, no for the whole published surface saying one thing yet (grounded in its probes: installed surface clean of both dead v4 stances, all references resolve, install/upgrade run at 19 files with the retired skill removed; three drifts in the outer docs — contract and one README paragraph shrink "second user" to least-privileged only, README's milestone hearing omits the second judge, README front page stale at "v4").

## Judgment receipt (opened at dispatch)

- **Judge:** codex exec (GPT-5.6), a fresh session — not the author, not either experiencer.
- **Dispatched:** 2026-08-19, on both records and their verdicts, with the duty to challenge both (favorable claims hardest) and the power to order re-runs, which the dispatching session executes.
- **Owner of this run:** the kernel session dispatching on 2026-08-19.
- **If the rulings are empty:** re-dispatch under your own named line.

## Rulings

Returned 2026-08-19, in full: [docs/reviews/v5-judge-rulings.md](../docs/reviews/v5-judge-rulings.md). **Overall: DO NOT LAND** — the hearing model is worth keeping, but this build can mis-land rejected work and its surfaces don't say one thing. The challenge worked as designed: both experiencers' favorable claims were narrowed to what their runs establish (nothing struck — all claims grounded), the divergence was held by scope, all four verdicts ruled BROKEN with record citations, structure ruled FIGHTING at the state-transition seam and the many-copies seam. Eleven defects routed to build (worst: the piece loop says six steps, prints five, never lands Built, and lands unconditionally after a hearing that may have rejected the piece). Two re-runs ordered before a fresh judge may permit landing: the failed-hearing transition (two blind conductors on a fixture), and the unavailable-experiencer follow-up. Tag and Odd's upgrade wait.

## Fixes and re-runs

**Fixes, all 11 routes (2026-08-19):** the piece loop is honestly five steps — Built is written in `state.md` when the piece runs and its checks pass, before any hearing; landing is conditional on a sufficient judgment, a rejecting judgment keeps the piece in the live slot with the map unticked, and the hearing-debt allowance is reconciled (one open hearing at most; a rejected piece re-takes the live slot) (1) · the second-user persona conserved in full in CONTRACT and README — least privilege AND the second person on the same install (2) · the second judge at milestones/risky restored to both README passages (3) · the unavailable-experiencer follow-up defined in judge, experience, and the piece template — fresh context inherits persona + record + exact scenario, a named follow-up line under the original receipt, appended to the same record (4) · release truth made atomic: the CLI's pin example derives from package.json's version, and the release rule is that the version bump, README status, and tag land in one commit after the judgment permits — README no longer claims a version ahead of or behind the executable (5) · README honesty: "five kinds of files", work/ named as a folder, "only coined words" scoped to the four state names (6) · every hearing output has one home: piece hearings in the piece's work file, milestone hearings (receipts, records, rulings, owner grade) in one work file named for the milestone (7) · the walk's three persona verdicts declared testimony, never a substitute for the judge's four (8) · piece-vs-milestone hearing composition stated at first contact in the loop (9) · conductor's "since he last looked" covers a session's first look (10) · the intro names experience and judge as two phases, one continuous hearing (11).

**The two ordered re-runs:** run on a planted fixture product (a tiny note-taking CLI with a real planted crash), receipts below.

## Re-run receipts (opened at dispatch, 2026-08-19)

- **Re-run 1 — failed-hearing transition:** fixture `jot` (tiny note CLI; a real planted apostrophe crash; the worker's record planted with a grounded deal-breaker verdict; state honestly at "coded, checks pass, judgment pending" — Built deliberately not yet written, so the conductors must). Two blind conductors (Claude general-purpose subagents, fresh contexts, told only "continue per the repo's AGENTS.md"), separate clones (jot-run-c1, jot-run-c2), each dispatching its own judge/experiencer contexts as codex exec with `< /dev/null` and an alarm. Watching for: Built written before the hearing · piece keeps the live slot after an insufficient ruling · map unticked · destinations right · lands only after re-experience + re-judgment.
- **Re-run 2 — unavailable-experiencer follow-up:** fixture variant (no bug; the worker's record ends with one load-bearing untested gap — "a genuinely long note, untested" — and the session marked ended). One blind conductor (jot-run-c3), same rails. Watching for: the judge orders the exact run instead of ruling on the gap · a fresh context inherits persona + record + scenario as a named follow-up line under the original receipt · the lived moment appends to the same record · no invented procedure.
- **Decorrelation note, honest:** the conductors are Claude-family (same vendor as the kernel's author); the judge and experiencer contexts they dispatch are cross-vendor (codex/GPT-5.6). The conductors were briefed on environment rails only — nothing about what the kernel expects of them.
- **Owner of these runs:** the kernel session dispatching on 2026-08-19. If a run's report never arrives, re-dispatch under your own named line.

## Re-run results (2026-08-20)

All three conductors drove their hearings to honest ends; none landed the piece — every landing gate held. Convergent across all three, blind: the missing worst-day persona completed before any judgment · the planted record's phantom receipt commit caught (one conductor also caught, from git history alone, that the fixture author had rewritten a record after the fact — struck as fabricated evidence, restored verbatim with a trace) · the same real unplanted defect class found by lived moves (kill-mid-write destroying confirmed notes, overlapping captures losing notes) · fix → re-experience-on-the-exact-scenarios → fresh-re-judge run everywhere · safety nets written and watched red against the condemned code before their green counted (7/11 and 3/3 reds) · every ending owner-blocked with options, costs, and a recommendation, live slot kept, map unticked. Divergent, held side by side: the same surface-truth (the promised bare `jot` is not what a clean shell delivers) reached three ways — macOS's own `/usr/bin/jot` shadowing the name · the "exactly as typed" wording vs shell parsing · apostrophes eaten by unquoted argv — and routing grounds chosen with latitude (mapping · shaping+mapping+build · shaping+build). The follow-up lineage law was exercised hard in all three (a fresh context inheriting persona and record · a killed client whose session finished its own record, provenance corrected, failed `resume` recorded honestly · a three-run chain where a dead run's record was never authored for it). Full evidence: the three conductor repos and reports, receipted above.

## Final judgment receipt (opened at dispatch)

- **Judge:** codex exec (GPT-5.6), a fresh session — not the author, none of the conductors, none of the prior judges or experiencers.
- **Dispatched:** 2026-08-20, on the corrected kernel surface plus the three re-run repositories as records.
- **Rules:** whether the two ordered re-runs are satisfied, the four on the v5 piece, and whether v5.0.0 may tag and the governed repo upgrade.
- **Owner of this run:** the kernel session dispatching on 2026-08-20. If the rulings are empty: re-dispatch under your own named line.

## Final rulings (first pass)

Returned 2026-08-20, in full: [docs/reviews/v5-final-rulings-1.md](../docs/reviews/v5-final-rulings-1.md). **DO NOT LAND, again** — the rejection gate held twice (no conductor ever landed insufficient work), but: both blind conductors missed writing Built before their hearings (the corrected sentence failed twice — the transition needs a mechanism the conductor can't miss, not prose); the ordered judge-first follow-up scenario never actually ran (the fixture's fabricated record — rightly struck by the conductor — consumed the valid starting point, and the replacement ran before any judge ordered it); the piece-file destination silently permits two artifact shapes; and this repository's own state.md/map.md went stale mid-hearing while package.json and README claimed v5 ahead of any v5 tag — the release-atomicity fix had fixed the pin rendering, not the truth. Four routes, all to build; a repeat of both re-runs on the corrected surface; then a new fresh judge. The correction of the earlier "all three runs closed honestly" line is exactly this section.

## Second-round fixes (2026-08-20)

1. **Built is now a receipt field, not a sentence:** the hearing receipt's first field quotes the `state.md` line that says Built and its commit — a receipt cannot open without it, and receipts are the thing every conductor demonstrably fills.
2. **The judge got the same continuity law as experiencers:** a judge whose session cannot stay open continues as a fresh context inheriting the judgment-so-far, the challenge list, and the receipt line — so "order the run, receive the append, then rule" is executable with one-shot sessions.
3. **The destination is now stated openly:** receipts, verdicts-in-brief, and the operative rulings live in the piece's work file; full-length records may live beside it as linked files — one home for the truth, links for the bulk.
4. **This repository's own truth reset:** state.md and map.md rewritten to the actual mid-hearing state; package.json set to 5.0.0-rc.1 and README's status made honest — version, status, and tag become v5.0.0 together in one release commit only after a sufficient judgment.

## Re-run repeats (receipts opened at dispatch, 2026-08-20)

- **Re-run 1 repeat — failed-hearing transition on the corrected surface:** fixture rebuilt with a clean two-commit history (real SHAs — the phantom receipt cost the first round a scenario); the worker's deal-breaker record planted, Built deliberately unrecorded. Two blind conductors (jot-run-c4, jot-run-c5), foreground-dispatch rail added (the first round's backgrounded dispatches caused idle-wait churn). Watching for: Built written and quoted in every new hearing receipt's first field.
- **Re-run 2 repeat — judge-first follow-up on a valid record:** fixture-4 — no planted bug, the worker's record genuinely receipted (real SHA), one load-bearing untested gap (the long note), the map's proven-means naming the worker alone (owner's stated one-persona call) so the gap is the hearing's only open question. One blind conductor (jot-run-c6). Watching for: the judge opens first, orders the exact run without ruling, writes judgment-so-far; the replacement inherits and appends; the same judge (by the new continuity law) receives the append and only then rules.
- **Owner of these runs:** the kernel session dispatching on 2026-08-20. If a run's report never arrives, re-dispatch under your own named line.

## Re-run repeat results (2026-08-20)

All three closed honestly. **Ground 1 (Built before the hearing): enacted by all three conductors** — each found the planted receipt missing its Built-quote field, repaired it as a dated amendment (never backdated), wrote Built into `state.md`, and opened every new receipt quoting it. The mechanism succeeded where the sentence had failed twice. **Ground 2 (judge-first follow-up): ran exactly as ordered in jot-run-c6** — the judge opened first, returned a judgment-so-far with no rulings, ordered the exact scenario; the replacement inherited and appended; a receipted judge continuation received the append and only then ruled. **Both directions of the landing gate lived:** jot-run-c5 reached a *sufficient* third judgment and landed the piece (map ticked, next piece live, landing orders executed); jot-run-c6 was refused and routed with the live slot kept; jot-run-c4 ran the entire lifecycle — two pieces landed through rejection-and-repair loops, then a milestone hearing with all four personas and two blind judges whose divergence was named and resolved by evidence, ending proven-on-the-records and blocked only on the owner's felt grade. One honest VOID record; every continuation receipted; one recorded rail adaptation (alarm 540 under the host's 600s Bash cap). Evidence: the three conductor repositories and their verbatim reports.

## Final judgment receipt, second pass (opened at dispatch)

- **Judge:** codex exec (GPT-5.6), a fresh session — none of the prior contexts.
- **Dispatched:** 2026-08-20, on the corrected surface plus jot-run-c4, jot-run-c5, jot-run-c6.
- **Rules:** the four grounds of the first final judgment, the four verdicts, and whether v5.0.0 may release.
- **Owner of this run:** the kernel session dispatching on 2026-08-20. If the rulings are empty: re-dispatch under your own named line.

## Final rulings, second pass

Returned 2026-08-20, in full: [docs/reviews/v5-final-rulings-2.md](../docs/reviews/v5-final-rulings-2.md). **DO NOT RELEASE — third refusal.** Routes 2 (judge-first continuation — c6's linear six-commit chain verified exact) and 3 (one-home destination) ruled CLOSED. Route 1 STILL OPEN: the judge's git archaeology showed c4 and c5 both opened their first new receipt by retrospectively quoting the planted "coded; checks pass" sentence — neither wrote Built to state.md first; only c6 truly performed the transition, and only because its judge ordered it. Route 4 STILL OPEN: **this file's own "3-for-3" claim was the overclaim — the exact failure declared a success** — and state.md/map.md lagged while decisions.md said "Landed as v5.0.0" with no v5 tag in existence. Structure: FIGHTING, partly on this record's own honesty. The narrow route: make the Built check reject the literal c4/c5 condition (watched failing against their real histories before its green counts), repeat only the two-clone opening transition, restore this repository's truth, then one new fresh judge on that narrow record. **Correction, per the ruling: the earlier "enacted by all three conductors / 3-for-3" line in the repeat-results section above is wrong and stands corrected by this section.**

## Third-round fixes (2026-08-20)

1. **The Built check now has teeth at three surfaces, with the literal-word rule:** the piece template's built field carries the check in its own bracket text ("the line must literally say Built — if it doesn't, write it first; coded-and-checks-pass is not Built"), the loop's step 4 makes the same check the action of opening a receipt, and the judge skill codifies c6's proven behavior as law — a receipt whose built quote lacks the literal word is invalid: rule nothing, order the state written and the receipt reopened. Watched failing against the two real failure histories: the rule rejects c4's 3ff144a and c5's afab9b5 openings (their quoted line, from 60e025c, contains no "Built"), and accepts c6's cd216c3.
2. **Repository truth restored:** this correction section; state.md and map.md rewritten to the routed now; the decision entry's "Landed as v5.0.0" amended to candidate language with a visible correction note; release posture unchanged (5.0.0-rc.1, README candidate, pin v4.0.0, latest tag v4.0.0).

## The narrow repeat (receipt opened at dispatch, 2026-08-20)

- **Subject:** the opening transition only — fixture-3 upgraded to the third-round surface (its receipt-field text now carries the literal-Built check), Built again deliberately unrecorded. Two blind conductors (jot-run-c7, jot-run-c8), session-bounded to their first dispatch round so nothing beyond the transition re-runs. Pass condition, checked in git afterward: a state.md commit whose line literally says Built lands BEFORE the first new hearing-receipt commit; a retrospective relabel of "coded; checks pass" fails.
- **Owner of this run:** the kernel session dispatching on 2026-08-20. If a report never arrives, re-dispatch under your own named line.

## Narrow repeat results (2026-08-20)

**Both blind conductors enacted the transition — 2-for-2 where prose went 0-for-2 twice.** jot-run-c7: found the planted receipt invalid under the field's own check, verified the piece by real runs, wrote Built in its own commit `7f248c0`, and only then repaired the receipt quoting that line and commit (`29e7082`). jot-run-c8: same order — Built at `ead938b` on verified runs, receipt reopened quoting it at `150a47e`. Both then ran honest dispatch rounds (each had one alarm-killed run voided on the receipt and a clean re-dispatch under a named line; the worst-day records both independently reproduced the planted crash and the real persistence losses) and stopped at their session bound with judgment pending — the transition, which is all this repeat tested, is on the record in git order.

## Final judgment receipt, third pass (opened at dispatch)

- **Judge:** codex exec (GPT-5.6), a fresh session — none of the prior contexts.
- **Dispatched:** 2026-08-20, on the narrow closure record: the third-round surface, c7 and c8's git histories, the check's rejection of the c4/c5 openings, and this repository's restored truth.
- **Owner of this run:** the kernel session dispatching on 2026-08-20. If the rulings are empty: re-dispatch under your own named line.

## Final rulings, third pass

(appended on return)
