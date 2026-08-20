RULING: MAY RELEASE v5.0.0 AND THEN UPGRADE THE GOVERNED PRODUCT REPOSITORY — the six-entry chronology is faithful, commit `aaa6ae2` atomically removed the counting drift, every current surface tells one honest prerelease story, and all four verdicts are sufficient.

# Sixth final judgment — v5, truth-only

**Subject:** the fifth judgment's route in `docs/reviews/v5-final-rulings-5.md:70-83`, correction commit `aaa6ae2`, the sixth-pass receipt at `0af8711`, and the named repository surfaces at current HEAD.

**Judge boundary:** I built none of this, walked none of it, and gathered no new product evidence. Per the route, I did not re-hear the Built gate, c6/c7/c8, the one-home mechanism, or any other closed product ground. I checked the correction transaction, the six chronology entries against their source judgments and the work file's own sections, and whether the current status, state, map, decision, package, README, CLI pin, and tag tell one story.

## 1. The correction transaction

**PASS.** Commit `aaa6ae2` has parent `5003f28` and changes exactly four files:

1. it adds the returned fifth judgment at `docs/reviews/v5-final-rulings-5.md`;
2. it rewrites the current Status in `work/v5-hearing.md`, installs the six-entry chronology as the only counting surface, and replaces the fifth-pass placeholder with the returned result;
3. it rewrites `state.md` to cite that chronology instead of repeating counts or ordinals; and
4. it rewrites the live v5 line in `map.md` to do the same.

The fifth-pass result, Status correction, chronology, state rewrite, and map rewrite therefore landed as one transaction. The following commit, `0af8711`, changes only `work/v5-hearing.md` to open this sixth truth-only judgment. Opening the receipt neither advances the piece nor claims a release, so it does not require a state or map transition.

## 2. The chronology

All six entries at `work/v5-hearing.md:10-15` match both their source judgments and the work file's longer record:

1. **Bootstrap hearing — DO NOT LAND, 11 routed defects.** `docs/reviews/v5-judge-rulings.md:1,127-153` routes eleven defects and orders two re-runs; the work file records the same result and all eleven fixes at `work/v5-hearing.md:38-44`.
2. **First final judgment — DO NOT LAND, four routes.** `docs/reviews/v5-final-rulings-1.md:1,110-119` refuses landing and names four build routes; the matching work-file result is at `work/v5-hearing.md:64-66`.
3. **Second final judgment — DO NOT RELEASE; c4/c5 fail Built acceptance; judge-first and one-home close.** `docs/reviews/v5-final-rulings-2.md:1,47-70,105-107,135-145` closes the latter two grounds and routes the Built acceptance failure plus repository truth; `work/v5-hearing.md:92-99` says the same.
4. **Third final judgment — DO NOT RELEASE; Built and c7/c8 close; state and map lag.** `docs/reviews/v5-final-rulings-3.md:1,13-56,106-115` verifies both clone orders and routes only the stale current surfaces; `work/v5-hearing.md:108-118` matches it.
5. **Fourth final judgment — DO NOT RELEASE; the work file's top Status lags.** `docs/reviews/v5-final-rulings-4.md:1,19-44,72-81` names that one current-status sentence; `work/v5-hearing.md:120-128` matches it.
6. **Fifth final judgment — DO NOT RELEASE; state ordinals are off by one.** `docs/reviews/v5-final-rulings-5.md:1,20-44,70-83` names and routes that exact sentence; `work/v5-hearing.md:130-138` matches it and records why state and map now speak count-free.

The order, dates, outcomes, and grounds are coherent. Historical passages remain historical; the current Status and tail supersede them without rewriting them.

## 3. One current story

**PASS.** Every named surface describes the same current posture:

- `work/v5-hearing.md:7-15,138-148` says all mechanism grounds are closed, six judgments have refused so far, this sixth final judgment is open, and only a sufficient result opens the release transaction.
- `state.md:5,22` says v4.0.0 is the latest release, main is the `5.0.0-rc.1` candidate, v5 is live in its truth-only judgment, and the chronology in the work file is the sole home for counts.
- `map.md:11` keeps v5 live and awaiting this truth-only judgment, with its count and chronology delegated to the work file.
- `decisions.md:3` calls v5 a release candidate, visibly corrects the former premature release wording, and says v5.0.0 releases only when its judge permits.
- `package.json:3` is `5.0.0-rc.1`.
- `README.md:42-44` calls v4.0.0 the latest tag, v5 a candidate, and its hearing still running.
- `bin/speck-next.js:80-86` reports the package's candidate version and gives `v4.0.0` as the example released pin.
- Git's latest tag is `v4.0.0` at `b8e14cb`; current HEAD `0af8711` is untagged and no `v5*` tag exists.

Nothing calls v5 released. Nothing completed is described as still needing to run. “Awaiting” and “next” refer to the result of this already-open judgment, not to a past judgment or repeat. The deliberately count-free state and map are coherent with the work file's one-home chronology.

## 4. The four on v5

### Works — KEPT

The closed mechanism evidence stands. This truth-only pass additionally establishes that the fifth judgment's exact correction route was executed in one commit, and that the receipt which followed did not create new state drift. The release transaction is now gated by a current, coherent judgment surface.

### Delivers the promise — KEPT

The accumulated hearing record already establishes grounded persona verdicts, a separate challenging judge, held divergence, cited rulings, backward routing, judge continuity, the one-home destination, conditional landing, and the literal-Built precondition. The last open promise was honest repository truth. The chronology now has one home, while every release-facing surface correctly remains prerelease.

### Good to use — KEPT

The operative checks remain at the conductor's and judge's natural action points, and the release posture can be understood without reconstructing six passes from several files. A reader gets the full ordered judgment story from one chronology and the current posture from each surface without conflicting counts.

### Quality hangs together — KEPT

Status, chronology, tail, state, map, decision, package, README, CLI pin, and Git tags now agree. The correction removes the repeated drift class instead of merely repairing its latest ordinal: counts live once, and the other current surfaces point to that home. All four verdicts now stand separately on evidence. The v5 piece is sufficient for release.

### Structure

**SOUND.** The hearing mechanism remains sound on the closed evidence. The repository-truth seam is also sound at this snapshot: the chronology owns judgment counts, state and map carry only current posture, and the multi-surface release transition has one explicit atomic commit. The failure-producing duplicate counts and ordinals named by the prior fighting rulings no longer exist; those rulings are historical grounds, not current strain.

**Whole ruling: SOUND.**

## 5. Close

**May v5.0.0 release? Yes. May the governed product repository upgrade? Yes, after that release exists.**

Make one release commit that updates together:

1. `package.json` to `5.0.0`;
2. README status to v5.0.0 released;
3. `state.md` to the post-judgment, post-release truth;
4. `map.md` to land v5 consistently;
5. the CLI's released-pin example to `v5.0.0`; and
6. `work/v5-hearing.md` with this sufficient hearing result.

Tag that exact commit `v5.0.0`. Only after the commit and tag exist may the governed product repository upgrade to v5.0.0.

What stays honestly open:

- Odd remains the in-anger proof that the hearing improves a real product campaign, and `milestone: v5-proven-in-anger` remains open until that experience exists (`map.md:5-11`; `state.md:22`).
- c7 and c8's fixture pieces remain Built and unjudged at their intentional session bound; their narrow purpose was the opening transition, not a completed fixture hearing (`work/v5-hearing.md:101-108`).
- c4's fixture milestone remains proven on its agent records but awaits its owner's felt-experience grade; its `jot --help` fork remains that fixture owner's product call (`docs/reviews/v5-final-rulings-3.md:117-123`).
- Historical v4 and old-Speck upgrade preservation remains unproven; the converter is still queued (`CONTRACT.md:21-29`; `map.md:12`).
- The fixture evidence does not establish the method across UI, auth, network, regulated behavior, historical upgrades, or the environmental and platform limits recorded in the earlier judgments (`docs/reviews/v5-final-rulings-2.md:147-152`).
- The receipt-law and open-stdin strains still await one more real campaign before retirement (`state.md:7-10`).

None of those open grounds contradicts this release. They remain explicit field evidence and later-piece work, not hidden conditions represented as complete.
