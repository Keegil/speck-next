RULING: DO NOT RELEASE v5.0.0 OR UPGRADE THE GOVERNED PRODUCT REPOSITORY — the literal-Built gate and its two-clone opening transition now pass, but `state.md` and `map.md` still report that completed repeat as future or running after this third judgment opened, so repository truth remains broken and the four are not all sufficient.

# Third final judgment — v5, the hearing

**Subject:** the v5 candidate at `9490dd8`; the chain in `work/v5-hearing.md`; the second final judgment in `docs/reviews/v5-final-rulings-2.md`; and the cited histories in `jot-fixture-3`, `jot-run-c4`, `jot-run-c5`, `jot-run-c6`, `jot-run-c7`, and `jot-run-c8`.

The fixture names in this judgment refer to sibling repositories under `/private/tmp/claude-501/-workspace-speck/a0e0d32c-31ec-4aba-a433-2bd88364f16f/scratchpad/`; for example, `jot-run-c7/work/capture-a-note.md` means that file inside the `jot-run-c7` repository.

**Judge boundary:** I built none of this, walked none of it, and gathered no new product evidence. I read the supplied records, heard the two original experiencer verdicts in full, and verified the narrow closure claims against the governing files and Git histories.

The second final judgment left exactly two grounds: make the Built check reject the literal c4/c5 opening condition and pass twice from the planted state; then restore this repository's truth before a fresh judge rules the four again (`docs/reviews/v5-final-rulings-2.md:135-145`). Routes 2 and 3 were closed there and remain closed.

## 1. The Built check

### The rule is executable and has the right boundary

The three governing surfaces agree:

- Build step 3 says that running work becomes **Built** only when that state is written to `state.md` before the hearing (`AGENTS.md:27-30`).
- Opening the receipt is the check: its first field must quote the cited commit's `state.md` line, and the line must literally say **Built**; “coded” or “checks pass” fails (`AGENTS.md:31`).
- The piece template carries that check in the field a conductor fills (`templates/piece.md:11`), and the judge's first duty independently rejects a receipt whose cited line does not literally say **Built** (`.claude/skills/judge/SKILL.md:12-14`).

At `jot-fixture-3` commit `60e025c`, `state.md:4` says: `Piece "capture a note" is coded; the builder's own runs pass.` It does not say **Built**. The current field text therefore rejects it without semantic interpretation.

That is the exact historical failure:

- c4 commit `3ff144a` quoted the `60e025c` coded/checks-pass line and changed only `work/capture-a-note.md`; no Built state commit preceded that receipt.
- c5 commit `afab9b5` did the same and also changed only `work/capture-a-note.md`.

The positive side also passes. c6 commit `cd216c3:state.md:4` says the piece `is Built — it runs and its own checks pass`; the replacement receipt at `c84bffb:work/capture-a-note.md` quotes that line and commit. The field accepts the literal Built state and rejects the two retrospective relabels.

**Watched-fail ruling:** closed. The check was read against the two real condemned histories, not a crafted analogue, and returned the required negative result for each; c6 supplies the positive control (`work/v5-hearing.md:88-91`).

## 2. The two-clone opening transition

### c7 — PASS

Git order is direct and exact:

1. `7f248c0` changes only `state.md`; its line says the piece `is Built` and cites the conductor's real runs.
2. `29e7082` is the direct child of `7f248c0`; only then does it reopen the hearing receipt, quoting that Built line and commit (`jot-run-c7/work/capture-a-note.md:9-12`).

The later receipt is honest about the dead dispatch. Attempt 1 is named with its distinct session, exit 142, empty record, and the explicit statement that nothing from it is citable or reconstructed. Attempt 2 has a new named line and session; the returned record is imported byte-identically under that provenance (`jot-run-c7/work/capture-a-note.md:12-14,22-26`; `jot-run-c7/state.md:19-23`). Git places the void-and-redispatch commit `def2c1c` before the returned-record commit `e677959`.

### c8 — PASS

The same transition occurs independently:

1. `ead938b` changes only `state.md`; its line says the piece `is Built` on recorded real runs.
2. `150a47e` is the direct child of `ead938b`; only then does it reopen the receipt quoting the Built line and commit (`jot-run-c8/work/capture-a-note.md:11-13`).

Attempt 1 is recorded as killed at the 540-second alarm with no experiencer record; the receipt says its partial files are not evidence and that nothing was imported. Attempt 2 is a fresh named context with no inherited record, and its own returned record is linked with a different session (`jot-run-c8/work/capture-a-note.md:15-17,25-32`; `jot-run-c8/state.md:18-21`). Git places `003ded5` before the successful record commit `0f83487`.

Both clones stop honestly at the ordered boundary: Built is recorded, both named persona records are in, and judgment remains pending. The repeat tested the opening transition, not the fixture pieces' later judgments (`work/v5-hearing.md:93-100`).

**Two-clone ruling:** closed. c7 has `7f248c0 → 29e7082`; c8 has `ead938b → 150a47e`. In both, the Built commit is the receipt commit's direct parent.

## 3. Repository truth

The release-facing posture is now honest and consistent:

- The amended v5 decision calls this a release candidate and visibly corrects its former premature “Landed as v5.0.0” language (`decisions.md:3`).
- The package is `5.0.0-rc.1` (`package.json:3`).
- README says v4.0.0 is the latest tag and v5 is a candidate whose hearing is still running (`README.md:42-44`).
- The CLI's released-pin example remains v4.0.0 (`bin/speck-next.js:80-86`).
- `git describe --tags --abbrev=0` returns `v4.0.0`; HEAD has no tag.
- The hearing record visibly corrects its earlier three-for-three overclaim (`work/v5-hearing.md:84-91`).

But the current phase detail does not tell the same story:

- The hearing record says the narrow repeat completed 2-for-2 and this third final judgment opened (`work/v5-hearing.md:98-106`).
- `state.md` still says “The narrow repeat runs next,” followed by a future fresh judge (`state.md:20-22`).
- `map.md` still calls the narrow Built-transition repeat “running” (`map.md:8-11`).

Those are not historical passages. They are the repository's current-state surfaces. Commit `9490dd8` recorded the repeat result and opened this judgment by changing only `work/v5-hearing.md`; it left `state.md` and `map.md` at the pre-repeat truth written in `2306275`. The product contract makes stale state a failed check, not a documentation nicety (`CONTRACT.md:20`), and this repository says measured evidence beats documents and state must claim nothing beyond evidence (`AGENTS.md:43,47`).

**Repository-truth ruling:** still open. Candidate-versus-release truth is fixed; live hearing truth drifted again at the next event.

## 4. The four on v5

### Works — KEPT on the hearing mechanism

The two previously closed mechanisms still stand: c6 ran the judge-first continuation in the required six-commit order, and the one-home rule is explicit (`docs/reviews/v5-final-rulings-2.md:47-70,105-107`). The remaining Built mechanism now rejects both historical bad receipts, accepts explicit Built, and made two blind conductors perform the transition before dispatch. Both insufficient and sufficient landing directions already have records in c4/c5/c6; no closed route needs repeating (`docs/reviews/v5-final-rulings-2.md:98-107`).

### Delivers the promise — KEPT on the narrow record

The original bootstrap established grounded persona verdicts, a separate challenging judge, held divergence, cited rulings, and backward routing (`docs/reviews/v5-judge-rulings.md:86-99`). Later records supplied the missing judge-first unavailable-session continuation, the one-home destination, the conditional landing directions, and now the literal Built precondition (`docs/reviews/v5-final-rulings-2.md:47-70`; this judgment §§1-2). The v5 hearing promise in `work/v5-hearing.md:3-5` is delivered by the accumulated record.

### Good to use — KEPT on the hearing surface

The check sits where conductors and judges already act: the first receipt field and the judge's first duty. c7 and c8 both stopped at `coded`, wrote Built in its own commit, then reopened the receipt, independently and without a special briefing about the expected move. Each also handled an empty dispatch honestly under the existing receipt rule. This is the ordinary-conductor behavior the earlier prose did not produce.

### Quality hangs together — CHECK FAILED

The governing surface, Built check, candidate version, decision, README, CLI pin, and tags now agree. The repository's live state and map do not agree with its hearing record or Git history. The exact truth ground that the second final judgment required before this judge was restored in `2306275` and made stale by `9490dd8`, the next transition commit. A product whose contract says state tells the truth cannot call all-four quality sufficient while its current state says completed work is still future.

The first three verdicts do not compensate for the fourth. This piece is **not proven**.

### Structure

- **Sound:** the hearing's role separation, challenge, divergence, routing, judge continuity, conditional landing, and literal Built gate now have executable records.
- **Fighting:** live truth is still distributed across the hearing record, state, and map without the event being recorded atomically. The exact seam was named by the second final judgment, corrected once, and drifted again in the very next result commit.

**Whole ruling: FIGHTING.** One fighting ruling forces structural work (`decisions.md:28`; `.claude/skills/judge/SKILL.md:18`). The problem is no longer the hearing mechanism. It is this repository's inability to keep its current hearing truth current across its own transition.

## 5. Close

**May v5.0.0 release now? No. May the governed product repository upgrade? No.**

Route back to **build**, narrowly, on repository truth only:

1. Append this third-pass result to `work/v5-hearing.md`, and in the same commit rewrite `state.md` and the live v5 line in `map.md` to the actual post-judgment state: the literal-Built check and c7/c8 transition are closed; this judgment refused release only because current truth had drifted; v5 remains the live `5.0.0-rc.1` candidate awaiting one last truth-only judgment.
2. Keep the rest of the pre-release posture unchanged: package `5.0.0-rc.1`, README candidate status, CLI pin example v4.0.0, and latest tag v4.0.0.
3. Convene one new fresh final judge on that repository-truth correction. Do not repeat c7/c8, the c6 judge-first chain, or the one-home route; all are closed.
4. Only after that judge finds all four sufficient, make one release commit updating together: package version `5.0.0`, README status, `state.md`, `map.md`, the CLI's released-pin example, and the hearing result. Tag that exact commit `v5.0.0`. Only then may the governed product repository upgrade.

What stays honestly open after this blocker closes:

- Pilot remains the in-anger proof that the hearing improves a real product campaign rather than only fixtures (`capabilities.md:8`; `map.md:5-11`).
- c7 and c8's fixture pieces remain Built and unjudged at their intentional session bound. That is outside the narrow transition repeat, not evidence of a completed fixture hearing (`work/v5-hearing.md:98-100`).
- c4's milestone is proven on its agent records but still awaits the owner's felt-experience grade; its `jot --help` fork remains the fixture owner's product call (`jot-run-c4/work/usable-jot.md:59-64,73-94`).
- Historical v4 and old-Speck upgrade preservation remains unproven; the converter stays queued (`CONTRACT.md:21-29`; `map.md:12`).
- The fixture evidence remains narrow. It does not establish the method across UI, auth, network, regulated behavior, historical upgrades, or the environmental and platform limits listed in the earlier final judgment (`docs/reviews/v5-final-rulings-2.md:147-152`).
