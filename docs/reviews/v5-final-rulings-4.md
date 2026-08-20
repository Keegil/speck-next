RULING: DO NOT RELEASE v5.0.0 OR UPGRADE THE GOVERNED PRODUCT REPOSITORY — commit `214bbe5` atomically landed the ordered third-pass result with `state.md` and `map.md`, and every release-facing surface is honestly prerelease, but the current `Status` at `work/v5-hearing.md:7` still describes the first refusal's re-runs and fresh judge as future, so repository truth remains one surface behind.

# Fourth final judgment — v5, truth-only

**Subject:** the repository-truth correction at `214bbe5`, the fourth-pass receipt at `b04b6f9`, the route in `docs/reviews/v5-final-rulings-3.md:106-123`, and the current repository surfaces at HEAD.

**Judge boundary:** I built none of this, walked none of it, and gathered no new product evidence. Per the third judgment's route, I did not re-hear the literal-Built gate, c7/c8's opening transition, c6's judge-first chain, or the one-home rule. I checked only whether the ordered truth correction landed and whether the repository now tells one current story.

## 1. The ordered correction commit

**Item 1 passes.** The required Git check shows:

1. `9490dd8` recorded the completed narrow repeat and opened the third final judgment in `work/v5-hearing.md`.
2. `214bbe5` then changed `work/v5-hearing.md`, `state.md`, and `map.md` in one commit. It appended the third-pass result at the hearing's third-pass placeholder, rewrote state to say the repeat had completed and only a truth-only judgment remained, and rewrote the live map line to the same post-judgment state. The commit also added the third judgment file; that extra receipt does not split the ordered transaction.
3. `b04b6f9` subsequently changed only `work/v5-hearing.md` to open this fourth-pass receipt. It did not move the product to a different release or piece state.

This is the atomic correction the third judgment ordered (`docs/reviews/v5-final-rulings-3.md:110-115`).

## 2. Whether the repository tells one story

### Release posture — PASS

The release-facing surfaces agree:

- `state.md:5` says v4.0.0 is the latest release and main is the v5 candidate at `5.0.0-rc.1`, mid-hearing.
- `map.md:11` keeps v5 live, records four refusals, names all four closed grounds, and awaits the truth-only judgment.
- `decisions.md:3` calls v5 a release candidate and visibly corrects its former premature release claim.
- `package.json:3` is `5.0.0-rc.1`.
- `README.md:42-44` says v4.0.0 is the latest tag, v5 is a candidate whose hearing is running, and v5.0.0 waits for a permitting judge.
- `bin/speck-next.js:80-86` displays the candidate package version but gives v4.0.0 as the example released pin.
- `git describe --tags --abbrev=0` returns `v4.0.0`; HEAD has no tag.
- The hearing's current tail records the third refusal's exact route and this truth-only receipt (`work/v5-hearing.md:108-120`).

No release-facing surface is ahead of or behind another.

### Current hearing status — CHECK FAILED

The hearing file's top current-status field still says:

> `built → heard → judged DO-NOT-LAND (2026-08-19) — routed back to build; fixes and the two ordered re-runs below, then a fresh judge.`

That is `work/v5-hearing.md:7`. The two ordered re-runs it places in the future completed before the first final judgment; the file now contains three repeat rounds, four refusals, the completed c7/c8 transition, the third-pass result, and this fourth-pass receipt (`work/v5-hearing.md:41-120`). The later chronological entries correct the history, but they do not turn a top field labeled **Status** into a historical snapshot.

`state.md:22`, `map.md:11`, and the hearing's own tail are current. The hearing's named status surface is not. The repository therefore still fails item 2's one-story test.

## 3. The four on v5

### Works — KEPT

The prior judgments verified the operative mechanism: c6's judge-first continuation ran in the required six-commit order; the one-home destination is explicit; the literal-Built check rejects c4/c5 and accepts explicit Built; and c7/c8 both wrote Built before reopening their receipts (`docs/reviews/v5-final-rulings-2.md:47-70,98-107`; `docs/reviews/v5-final-rulings-3.md:13-56,81-83`). Commit `214bbe5` also performed the ordered three-surface correction as one transaction. The stale top status does not undo those executable records.

### Delivers the promise — KEPT

The accumulated record establishes grounded persona verdicts, a separate challenging judge, held divergence, cited rulings, backward routing, judge continuity, one hearing home, conditional landing, and the literal-Built precondition (`docs/reviews/v5-final-rulings-3.md:85-87`). The truth correction also made the repository's live state, map, hearing tail, candidate version, README, decision, CLI pin, and tag posture agree. The v5 hearing promise is delivered by those records; the remaining defect is the repository's current-status truth.

### Good to use — KEPT

The third judgment found that the Built check sits at the conductor's and judge's natural point of action and made two blind conductors perform the required transition (`docs/reviews/v5-final-rulings-3.md:89-91`). The correction commit likewise followed the requested atomic move without disturbing the prerelease posture. No closed usability route needs another run.

### Quality hangs together — CHECK FAILED

The correction fixed the exact cross-file drift the third judgment named, but it left the hearing file's own current `Status` behind. A reader starting at the work file's status is told that long-completed re-runs and a fresh judge are still next; a reader starting at `state.md`, `map.md`, or the hearing tail sees the truth-only fourth pass already open. Truth at the tail does not compensate for false current status at the top.

The first three verdicts do not compensate for the fourth. The piece is **not proven**.

### Structure

The hearing mechanism remains sound on the closed evidence. Repository truth is still **FIGHTING**: the third judgment narrowed the whole blocker to current-truth synchronization, and the correction transaction updated three surfaces while leaving a fourth named current-status surface at the first refusal. This is the same structural ground inside the correction intended to close it, not a separate product defect or a reason to re-run the hearing mechanisms.

**Whole ruling: FIGHTING.**

## 4. Close

**May v5.0.0 release now? No. May the governed product repository upgrade? No.**

Route back to **build**, on repository truth only:

1. Append this fourth-pass result to `work/v5-hearing.md` and rewrite that file's top `Status` to the actual post-judgment state. In the same commit, rewrite `state.md` and the live v5 line in `map.md` to say five refusals, all mechanism grounds closed, and one last truth-only judgment awaiting the status correction. Do not alter or re-run the Built gate, c7/c8, c6, or the one-home rule.
2. Keep the prerelease posture unchanged: package `5.0.0-rc.1`, README candidate status, decisions candidate language, CLI pin example v4.0.0, and latest tag v4.0.0.
3. Convene one new fresh final judge on that status-only correction. Its only question is whether the current status, hearing tail, state, map, decision, package, README, CLI pin, and tag now tell one story.
4. Only after that judge finds all four sufficient, make one release commit updating together: package version `5.0.0`, README status, `state.md`, `map.md`, the CLI's released-pin example, and the hearing result. Tag that exact commit `v5.0.0`. Only then may the governed product repository upgrade.

What stays honestly open after this blocker closes:

- Odd remains the in-anger proof that the hearing improves a real product campaign rather than only fixtures (`capabilities.md:8`; `map.md:5-11`).
- c7 and c8's fixture pieces remain Built and unjudged at their intentional session bound; that was outside the narrow transition repeat (`work/v5-hearing.md:93-100`).
- c4's milestone remains proven on its agent records but awaits the owner's felt-experience grade, and its `jot --help` fork remains the fixture owner's product call (`docs/reviews/v5-final-rulings-3.md:119-123`).
- Historical v4 and old-Speck upgrade preservation remains unproven; the converter stays queued (`CONTRACT.md:21-29`; `map.md:12`).
- The fixture evidence remains narrow. It does not establish the method across UI, auth, network, regulated behavior, historical upgrades, or the environmental and platform limits recorded by the earlier final judgments (`docs/reviews/v5-final-rulings-2.md:147-152`).
