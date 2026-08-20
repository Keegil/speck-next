RULING: DO NOT RELEASE v5.0.0 OR UPGRADE THE GOVERNED PRODUCT REPOSITORY — the judge-first continuation is proven, but the exact Built-before-dispatch acceptance run failed again in both blind conductors, and this repository's own record overclaims that closure.

# Second final judgment — v5, the hearing

**Subject:** the corrected kernel at `a153894`; the full chain in `work/v5-hearing.md`; the first final judgment in `docs/reviews/v5-final-rulings-1.md`; and the Git histories and records in the three repeat repositories:

- `c4` — `/private/tmp/claude-501/-workspace-speck/a0e0d32c-31ec-4aba-a433-2bd88364f16f/scratchpad/jot-run-c4`
- `c5` — `/private/tmp/claude-501/-workspace-speck/a0e0d32c-31ec-4aba-a433-2bd88364f16f/scratchpad/jot-run-c5`
- `c6` — `/private/tmp/claude-501/-workspace-speck/a0e0d32c-31ec-4aba-a433-2bd88364f16f/scratchpad/jot-run-c6`

**Judge boundary:** I built none of this, walked none of it, and gathered no new product evidence. I ruled from the supplied records and verified their citations against the files and Git histories.

The first final judgment's Close required four routes back to build and then two exact repeat runs (`docs/reviews/v5-final-rulings-1.md:110-121`). The corrected governing text is clearer. The histories do not support the claim that every route closed.

## 1. The four routes

### Route 1 — mechanize Built before any hearing: STILL OPEN

The governing surface now states the intended gate correctly:

- A piece becomes Built only when it runs and its own checks pass, and that state must be written before the hearing (`AGENTS.md:27-31`).
- A hearing receipt's first field must quote the `state.md` Built line and name the commit that wrote it; without that field there is no receipt and no hearing (`AGENTS.md:30-31`).
- The piece template puts that field first and asks for the quoted Built line and commit (`templates/piece.md:11`).

That is a real improvement over the first failed wording. The exact two-clone acceptance condition nevertheless failed.

#### c4

The deliberately unrecorded starting state at `60e025c:state.md:4` says only: `Piece "capture a note" is coded; the builder's own runs pass.` It does not record the state as Built. Commit `3ff144a` then opens the new worst-day receipt and adds a late `built` field quoting that old line (`c4/work/capture-a-note.md:24-28`). Git shows `3ff144a` changes only `work/capture-a-note.md`; `state.md` is byte-identical to `60e025c` and still does not say Built.

The conductor therefore did not write Built to `state.md` before its first new hearing receipt. It interpreted the old coded/checks-pass sentence as sufficient and proceeded. That is the exact failure the repeat was designed to catch (`work/v5-hearing.md:67-70`).

Later c4 transitions do obey the rule: build pass 2 writes explicit Built at `cdf48a0` before follow-up receipts at `778d65e`; `list notes` writes Built at `3707d05` before receipts at `90fb4ce`. Those later successes show the form is usable when Built is already explicit. They do not repair the planted opening transition.

#### c5

c5 repeats the same failure independently. Its starting state at `60e025c:state.md:4` is the same coded/checks-pass sentence. Commit `afab9b5` opens the new worst-day receipt and adds a retrospective field quoting `60e025c` (`c5/work/capture-a-note.md:11-15`), but changes only `work/capture-a-note.md`; it does not write Built to `state.md` first.

Later c5 hearings do obey the rule: explicit Built lands at `44bb8db` before re-hearing receipts at `4b6746c`, and again at `93be744` before third-hearing receipts at `6babe4a` (`c5/work/capture-a-note.md:35-41,63-73`). The third judge then rules the piece sufficient (`c5/work/capture-a-note.md:81-85`; `c5/work/capture-a-note.judgment3.md:131-149`) and `4fa72c7` lands it, ticks the map, and opens the next piece. This is good positive-gate evidence. It does not satisfy the ordered opening transition.

#### c6

c6 demonstrates the safe response to this defect. The judge sees the original non-Built receipt as invalid, makes no rulings, and orders an explicit Built state plus a replacement receipt (`c6/work/capture-a-note-judgment.md:17-31,42-44`). Built is then written at `cd216c3`; the valid replacement receipt opens later at `c84bffb`, quoting that exact line (`c6/work/capture-a-note.md:11-13`).

**Route 1 ruling:** still open. The receipt field exposes the missing transition to a sufficiently alert judge, but it did not make the two blind conductors perform the transition before dispatch. The summary's claim that all three wrote Built before every new receipt is contradicted by c4 and c5 history (`work/v5-hearing.md:73-75`).

### Route 2 — judge-first unavailable-experiencer continuation: CLOSED

c6 runs the ordered sequence exactly, in the required commit order:

1. `843761a` — the judge receipt opens before any replacement run.
2. `cd216c3` — the judge returns a judgment-so-far with challenges and an exact six-step run, but no rulings; the same commit records Built in state (`c6/work/capture-a-note-judgment.md:1-44`).
3. `c84bffb` — a replacement receipt opens for a fresh context inheriting the worker persona, the prior record, and the judge's exact scenario (`c6/work/capture-a-note.md:13`).
4. `7b7c8a8` — the marked follow-up is appended; it lives the promised `jot` surface and stops on the observed failure (`c6/work/capture-a-note.md:41-71`).
5. `5ef6411` — the receipted judge continuation opens after the append (`c6/work/capture-a-note.md:17`).
6. `d128c73` — only then does the continuation rule, citing the original record and the ordered append (`c6/work/capture-a-note-judgment-2.md:1-31,42-70`).

Every commit is the direct parent of the next. The first judge explicitly withholds every promise, four-verdict, whole, structure, and route ruling until the continuation (`c6/work/capture-a-note-judgment.md:42-44`). The continuation accepts the replacement receipt, holds the two worker truths side by side, and rules only after the append (`c6/work/capture-a-note-judgment-2.md:7-40`).

The governing law now matches the lived path: a one-shot judge writes judgment-so-far with exact orders and no rulings; a fresh context inherits it and rules after receiving the append (`.claude/skills/judge/SKILL.md:8-15`).

**Route 2 ruling:** closed.

### Route 3 — one home for a piece hearing: CLOSED

The ambiguity is resolved openly. `AGENTS.md:31` names the piece work file as the hearing's one home for receipts, verdicts in brief, and operative rulings; full-length records may sit beside it as linked files. `templates/piece.md:11-15` instantiates the same split: the operative hearing and result stay in the piece file, while bulk records may be linked.

c4 and c5 use that shape: their piece files contain dispatch lines, verdicts in brief, operative rulings, and result, while linking the full records and judgments. This is one authoritative hearing home plus linked evidence, not two silent alternatives.

**Route 3 ruling:** closed.

### Route 4 — reset this repository to one release truth: STILL OPEN

The narrow release metadata is now mostly honest:

- `package.json:3` is `5.0.0-rc.1`.
- `README.md:42-44` says v4.0.0 is the latest release and v5.0.0 waits for a permitting judge.
- `bin/speck-next.js:80-86` derives its displayed version from the package and gives v4.0.0 as the released pin.
- Git's latest tag is `v4.0.0` at `b8e14cb`; there is no v5 tag.
- `state.md:5` also calls v4.0.0 the latest release and the main surface a v5 candidate.

The repository as a whole still does not tell one current story:

- `state.md:20-22` and `map.md:8-12` say the repeat runs are still running. The repeat records are complete and this second final judgment is already open (`work/v5-hearing.md:73-82`).
- `work/v5-hearing.md:75` says every conductor wrote Built before every new receipt. c4 and c5 Git history disproves that statement.
- The highest-authority standing record says the hearing design “Landed as v5.0.0” (`decisions.md:3`) while package, README, CLI pin, and tags all say v5.0.0 is not released.

The version number itself is no longer prematurely published, but release truth includes the repository's authoritative decision, current state, map, and hearing record. Those disagree.

**Route 4 ruling:** still open.

## 2. The two ordered repeat runs

### Failed-hearing transition repeat: NOT SATISFIED AS ORDERED

The order was not merely to preserve the rejection gate. It required both new conductors to write Built in `state.md` before the first new receipt opened (`docs/reviews/v5-final-rulings-1.md:114-117`; `work/v5-hearing.md:67-70`). c4 and c5 both opened their first new worst-day receipt while state still contained only the planted coded/checks-pass sentence. Both retrospectively labeled that sentence a Built quote.

The rest of the repeat supplies valuable evidence:

- c4 drives two pieces through rejection, repair, re-experience, sufficient judgment, and landing; its milestone then uses all four personas and two judges dispatched blind (`c4/work/usable-jot.md:7-31`). Their divergence is named and held rather than averaged (`c4/work/usable-jot.md:33-41`), the ordered returns close the agent-side gaps, and the final milestone judgment stops at the owner's felt grade (`c4/work/usable-jot.md:43-64,73-94`).
- c5 lives the negative gate twice and the positive gate once: the first two judgments keep the piece live and unticked; the third judgment is sufficient, then `4fa72c7` lands it and makes `list notes` live (`c5/work/capture-a-note.md:31-39,59-69,81-85`; current `c5/map.md:8-12`).

Those are strong hearing and landing-gate records. They do not satisfy the deliberately planted transition test.

### Judge-first follow-up repeat: SATISFIED AS ORDERED

The c6 chain `843761a → cd216c3 → c84bffb → 7b7c8a8 → 5ef6411 → d128c73` is linear and exact: judge first; judgment-so-far with no rulings; replacement receipt and inherited persona; marked append; receipted continuation; only then operative rulings. No new run is needed for this route.

## 3. The four verdicts on v5

### Works — CHECK FAILED

The hearing's core behavior works in substantial parts. c4 and c5 reject broken work, order exact repairs, re-hear it, and refuse landing until a sufficient judgment; c5 also proves the positive landing direction. c6 proves the one-shot judge continuation. But the acceptance run for the new Built gate failed in both blind conductors. A process whose hearing precondition is skipped twice on the scenario designed to test it does not work end to end.

### Delivers the promise — CHECK FAILED

The v5 promise is grounded user verdicts, a separate challenging judge, exact follow-ups when evidence is thin, held divergence, and truthful routing (`CONTRACT.md:17-20`; `decisions.md:3`). The records establish all of those except the claimed Built precondition. c4 and c5 both let a new hearing dispatch proceed without state having recorded Built, and the repository then reported that all three conductors had enacted it. That breaks the truth-and-checkable-exit part of the promise rather than leaving it merely unjudged.

### Good to use — CHECK FAILED

Once Built is explicit, fresh conductors use the receipt form successfully across later hearings. At the planted boundary, however, both blind conductors silently reinterpret `coded; checks pass` as the required Built state instead of performing the transition. The current surface gives an attentive later judge enough information to reject that receipt, as c6 did, but it does not make the ordinary conductor stop before dispatch. The owner-facing state and hearing summary then require Git archaeology to discover the miss. That is not yet good to drive.

### Quality hangs together — CHECK FAILED

The judge continuity law, one-home rule, conditional landing, and prerelease package/README/tag posture agree internally. The Built rule, its two acceptance histories, and the self-hosted report do not. `work/v5-hearing.md:75` calls the exact failed behavior a three-for-three success; `state.md` and `map.md` lag the completed repeats; `decisions.md:3` says v5.0.0 landed while the package, README, CLI, and tags correctly say it did not. The product contract makes truthful state a promise and truth over theater a whole-product property (`CONTRACT.md:20,41-52`). This piece is not proven.

### Structure

- **Sound:** persona verdicts point at lived moments; judges remain non-builders and non-walkers; c6's continuity law works; divergence is preserved; both insufficient and sufficient landing directions have records.
- **Straining:** release and phase truth is distributed across `decisions.md`, `state.md`, `map.md`, and the hearing record, and those copies have drifted again within the same hearing.
- **Fighting:** the Built gate was changed specifically because prose failed twice, yet the replacement mechanism still let both blind acceptance conductors proceed without the required state transition, and the self-hosted record then declared the failure a success.

**Whole ruling: FIGHTING.** One fighting ruling forces structural work before release (`.claude/skills/judge/SKILL.md:17-19`; `decisions.md:28`).

## 4. Close

**May v5.0.0 release now? No. May the governed product repository upgrade? No.**

Route back to **build**, then re-experience only the still-failing ground:

1. **Enforce the Built precondition, rather than adding another sentence.** Before any experiencer or judge dispatch can count, a check must verify that the receipt's first field cites a real ancestor commit whose `state.md` contains the quoted line and records the piece explicitly as Built. It must reject the exact c4/c5 opening condition: `coded; checks pass` is not an explicit Built state. Whatever form this takes, watch it fail against those two histories before its green counts.
2. **Repeat the two-clone failed-hearing transition from the deliberately unrecorded fixture.** In both fresh repositories, Git must show a state commit that writes Built before the first new hearing-receipt commit. A retrospective amendment or a semantic reinterpretation of `coded` does not satisfy the order. The rest of c4/c5 need not be repeated; their rejection, repair, positive landing, milestone, and owner-grade records already stand.
3. **Restore this repository's own truth before the next judge.** Correct the three-for-three claim in `work/v5-hearing.md`; rewrite `state.md` and `map.md` to the actual routed state; and change `decisions.md:3` from released-version language to candidate/design language. Keep `package.json` at `5.0.0-rc.1`, README in candidate status, the CLI pin at v4.0.0, and the latest tag at v4.0.0.
4. **Convene one new fresh final judge on that narrow closure record.** Route 2 and route 3 are closed and need no repeat. If the new Built acceptance run passes and repository truth agrees, that judge may rule the four again.
5. **Only after a sufficient judgment**, make one release commit that updates every release-facing truth together: package version `5.0.0`, README status, `state.md`, `map.md`, the CLI's released-pin example, and the final hearing result. Point tag `v5.0.0` at that exact commit. Only then may the governed product repository upgrade.

What stays honestly open after this release blocker is closed:

- Pilot remains the in-anger proof that the hearing improves a real product campaign rather than only fixtures (`state.md:20-22`; `capabilities.md:8`).
- c4's milestone is proven on its agent records but still blocked on the owner's felt-experience grade; its `jot --help` product fork also remains the fixture owner's choice (`c4/work/usable-jot.md:59-64,73-94`).
- Historical v4 and old-Speck upgrade preservation is not proven by these records; promise 5's converter remains queued (`CONTRACT.md:21-29`; `map.md:12`).
- The fixture evidence is narrow: c5 leaves real login-shell persistence and Linux behavior untested, and c4 does not prove installation beyond checkout-on-`PATH`, real-home peculiarities, disk-full, power loss, or hardware failure. UI, auth, network, regulated behavior, and other product classes are outside these records.
