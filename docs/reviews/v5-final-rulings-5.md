RULING: DO NOT RELEASE v5.0.0 OR UPGRADE THE GOVERNED PRODUCT REPOSITORY — commit `05cf9aa` atomically landed the ordered status correction, and the candidate/release surfaces agree, but `state.md:22` calls the fourth and fifth refusals the third and fourth, so the named surfaces still do not tell one chronology.

# Fifth final judgment — v5, status-only

**Subject:** the fourth judgment's Close in `docs/reviews/v5-final-rulings-4.md:72-89`, correction commit `05cf9aa`, the fifth-pass receipt at `5003f28`, and the current named repository surfaces at HEAD.

**Judge boundary:** I built none of this, walked none of it, and gathered no new product evidence. Per the fourth judgment's route, I did not re-hear the Built gate, c6/c7/c8, or the one-home rule. I checked only the ordered commit and whether the current status, hearing tail, state, map, decision, package, README, CLI pin, and tag tell one story.

## 1. The ordered correction commit

**PASS.** `git show 05cf9aa` verifies that one commit:

1. rewrote the top `Status` in `work/v5-hearing.md` from the first refusal's future route to the current five-refusal, status-only state;
2. replaced the fourth-pass placeholder with the returned fourth ruling;
3. re-landed `state.md` and `map.md` at five refusals and the pending status-only judgment; and
4. added `docs/reviews/v5-final-rulings-4.md` as the full ruling linked by the work file.

The required Status rewrite, fourth-pass append, state rewrite, and map rewrite are therefore one transaction. Commit `5003f28` subsequently changes only `work/v5-hearing.md` to open this fifth-pass receipt; it does not claim a release or advance the piece.

## 2. Whether the repository tells one story

### Current posture and release truth — PASS

The current surfaces agree on the large story:

- The work file's top Status says five refusals, all mechanism grounds closed, and one status-only judgment pending; its tail records the fourth-pass result as the fifth refusal and opens exactly that fifth pass (`work/v5-hearing.md:7,118-130`).
- `state.md:5,22` and `map.md:11` keep v5 live, unreleased, at five refusals, awaiting this judgment.
- `decisions.md:3` calls v5 a release candidate and visibly corrects its former premature release claim.
- `package.json:3` is `5.0.0-rc.1`.
- `README.md:42-44` calls v4.0.0 the latest tag, v5 a candidate, and the hearing still running.
- The CLI prints candidate version `5.0.0-rc.1` and gives `v4.0.0` as its example released pin (`bin/speck-next.js:80-86`).
- The latest tag is `v4.0.0` at `b8e14cb`; HEAD `5003f28` has no tag and no v5 tag exists.

Nothing in those surfaces describes v5 as released, and nothing describes this status-only judgment as already complete.

### Refusal chronology — CHECK FAILED

`state.md:22` says:

> The third refusal was state and map lagging; the fourth was the work file's own top Status still describing the first refusal as current — both corrected, each in one commit with its judgment's append.

That numbering is one behind the hearing record. The third **final pass** was the **fourth refusal** (`work/v5-hearing.md:108-110`), and the fourth final pass was the **fifth refusal** (`work/v5-hearing.md:118-120`). The work file's top Status and `map.md:11` both correctly say five refusals. The quoted current-state sentence instead labels those same two events the third and fourth refusals.

The repository therefore does not yet tell one chronology. This is the only failed item in the status-only scope.

## 3. The four on v5

### Works — KEPT

The prior judgments' closed evidence stands: c6 ran the judge-first continuation in the required six-commit order, and the piece hearing has one authoritative home (`docs/reviews/v5-final-rulings-2.md:47-70,105-107`). The literal-Built rule rejects the c4/c5 condition, accepts c6's explicit Built state, and c7/c8 each wrote Built before reopening a receipt (`docs/reviews/v5-final-rulings-3.md:13-56,81-83`). Commit `05cf9aa` also performed the fourth judgment's ordered transaction exactly. The remaining defect is not a failure of the hearing mechanism.

### Delivers the promise — KEPT

The accumulated judgments establish grounded persona verdicts, a separate challenging judge, held divergence, cited rulings, backward routing, judge continuity, the one-home destination, conditional landing, and the literal-Built precondition (`docs/reviews/v5-final-rulings-3.md:85-87`; `docs/reviews/v5-final-rulings-4.md:48-54`). This status-only check adds that every release-facing surface remains honestly prerelease. The hearing promise is delivered on the standing evidence.

### Good to use — KEPT

The Built check sits at the conductor's and judge's natural action point and made c7/c8 independently perform the missing transition (`docs/reviews/v5-final-rulings-3.md:89-91`). The ordered truth transaction also landed cleanly. No closed usability ground needs another run.

### Quality hangs together — CHECK FAILED

The release posture and current phase posture hang together, but the current state file misnumbers the two refusals whose corrections it summarizes. A reader cannot reconcile "five refusals" with that sentence without reconstructing the whole hearing chronology. The first three verdicts do not compensate for this fourth one, so the piece is not proven.

### Structure

Repository truth is **FIGHTING**. This is the same current-truth synchronization seam that the third and fourth final judgments routed: the atomic correction landed, but one sentence inside a named current-state surface still lagged the record it summarized. The hearing mechanism itself remains sound on the closed evidence.

**Whole ruling: FIGHTING.**

## 4. Close

**May v5.0.0 release now? No. May the governed product repository upgrade? No.**

Route back to **build**, on repository truth only:

1. Correct this exact sentence in `state.md:22`:

   > The third refusal was state and map lagging; the fourth was the work file's own top Status still describing the first refusal as current — both corrected, each in one commit with its judgment's append.

   Its two ordinals must be **fourth** and **fifth**.
2. This ruling is now the sixth refusal. In one commit, append this fifth-pass result to `work/v5-hearing.md`, rewrite that file's top Status, and re-land `state.md` and the live v5 line in `map.md` at six refusals with one last status-only judgment pending. Keep package `5.0.0-rc.1`, README candidate status, decisions candidate language, CLI pin `v4.0.0`, and latest tag `v4.0.0` unchanged.
3. Convene one fresh final judge on that status-only correction. Do not re-run or re-hear the Built gate, c6/c7/c8, the one-home rule, or any product mechanism.
4. Only a sufficient judgment may open the already-defined single release commit: package `5.0.0`, README status, `state.md`, `map.md`, the CLI released-pin example, and the hearing result together; tag that exact commit `v5.0.0`. Only then may the governed product repository upgrade.
