# Mapping — a separated product team

## Round 1 — owner-authorized order

The owner supplied the complete v6 implementation plan and then instructed, verbatim:

> PLEASE IMPLEMENT THIS PLAN

The authorized order is: separate role contributions before code; one live kernel piece; Engineering implements the candidate; Product integrates the first real run; active roles return; the piece becomes Built only after its own checks; four fresh milestone testers and two judges review it; fixes re-run the full requirement; the owner grades and ratifies the rendered method; only then does `6.0.0` release. The candidate is `6.0.0-rc.1`. Existing products are not a pre-release dependency and are not changed by this piece.

## Round 2 — four separate views of the map

The exact carriers and full evidence are recorded in [separated-product-team.md](separated-product-team.md). Their mapping conclusions were:

- **Product `/root`:** one substantial piece is clearer than splitting prose, migration, and proving into separate pieces because none is independently useful. Product keeps integration and records; Engineering owns every installed or executable change.
- **Business `/root/business_role`:** keep role work inside the existing before-first-run limit; measure contexts, time, tokens where available, and owner interruptions; make field value explicitly unproven until a real milestone supplies it.
- **Experience `/root/experience_role`:** test one integrated owner recommendation and one builder-ready handoff; do not expose four status reports or let role contributors contaminate later fresh testing.
- **Engineering `/root/engineering_role`:** use the existing method page, four phase skills, four templates, installer, and development suite; add no installed file or skill; prove context identity from host-issued evidence and migration by repeated runs.

All four are active. Their earliest uncertainties are written on piece 8 in `map.md`. Product resolves the map as one piece because the release is the first useful increment and every claimed benefit depends on the whole path working together.

## Mapping completion test

- Every promise served: yes — the piece amends the existing eight; it adds no ninth.
- Every shaped decision assigned: yes — all role, migration, proving, review, budget, and release decisions belong to piece 8.
- Supporting material consumed or visible: yes — `work/shaping.md` and `work/separated-product-team.md` are consumed by piece 8; none is hidden.
- Every current or future piece names runs, checks, testers, rulings, expected active roles, and its four earliest uncertainties: yes for pieces 8–11. Historical pieces 1–7 keep their pre-v6 evidence and are not backfilled or represented as role-shaped.
- Exactly one live piece: yes — piece 8.
- Running platform: unchanged — plain git, Node for install and upgrade, and the existing supported agent hosts for development tasks.
- Care: milestone treatment with two judges; no protected product code is changed.

## Map review receipt — opened before dispatch

- Candidate: `map.md`, this mapping record, and `work/separated-product-team.md` at the commit containing this receipt.
- Fresh tester: `/root/v6_shape_map_tester` — did not shape, map, build, or contribute a role.
- Judge: `/root/v6_shape_map_judge` — did not shape, map, build, contribute a role, or test.
- Planned probe: verify the map consumes every authorized v6 decision, has one live piece, makes the first useful increment run, assigns four uncertainties, and does not hide a product dependency or extra owner beat.
- Mechanical completion command: `python3 - <<'PY'` probe over `map.md` for one `[LIVE`, all four uncertainty labels, both consumed work records, and pieces 1 through 11 in order; exact command and output will be appended after it runs.
- Dispatched: after this receipt is committed; exact commit will be appended with the verdict.
- Verdict and judgment: pending.

### Mechanical completion run — 2026-08-31

Command:

```sh
python3 - <<'PY'
from pathlib import Path
text = Path('map.md').read_text()
checks = {
    'one live piece': text.count('[LIVE') == 1,
    'all role uncertainties': all(x in text for x in ('Product —', 'Business —', 'Experience —', 'Engineering —')),
    'both work records consumed': all(x in text for x in ('work/shaping.md', 'work/separated-product-team.md')),
    'pieces 1 through 11': all(f'{n}.' in text for n in range(1, 12)),
}
for name, passed in checks.items():
    print(f'{name}: {"PASS" if passed else "FAIL"}')
raise SystemExit(0 if all(checks.values()) else 1)
PY
```

Returned:

```text
one live piece: PASS
all role uncertainties: PASS
both work records consumed: PASS
pieces 1 through 11: PASS
```

### Tester round 1 — sent back

The fresh tester at `/root/v6_shape_map_tester` read commit `d0860fe` and sent Map back. Shape was still open while the map claimed a live Shaped piece; queued pieces 9–11 lacked milestones and v6 role fields; the first real user surface was unnamed; the completion claim exceeded its command; and the public-detail scan was missing from the live proof plan. Product returned piece 8 to `next`, added the milestones and future-piece fields without backfilling historical work, named the first surface, narrowed the completion claim, and added the scan. The completion command is expanded below and the same tester must re-run before judgment.

### Mechanical completion re-run — 2026-08-31

Command:

```sh
python3 - <<'PY'
from pathlib import Path
text = Path('map.md').read_text()
lines = text.splitlines()
pieces = {n: next((line for line in lines if line.startswith(f'{n}. ')), '') for n in range(1, 12)}
future = [pieces[n] for n in range(8, 12)]
checks = {
    'no live piece before ratification': text.count('[LIVE') == 0,
    'future pieces have role fields': all('expected active roles:' in line and 'earliest uncertainty:' in line for line in future),
    'future pieces have proof plans': all('proof plan:' in line for line in future),
    'all pieces covered by milestones': all(name in '\n'.join(lines[4:11]) for name in (
        'v3 discipline', 'v4 experience→judge', 'v5 the hearing', 'the campaigns land',
        "a builder's words and fewer of them", 'name the words', 'three producers',
        'a separated product team', 'v11 converter', 'CI limit enforcement', 'promise-conservation check')),
    'first real user surface named': 'first real user surface' in text,
    'both work records consumed': all(x in text for x in ('work/shaping.md', 'work/separated-product-team.md')),
    'pieces 1 through 11': all(pieces.values()),
}
for name, passed in checks.items():
    print(f'{name}: {"PASS" if passed else "FAIL"}')
raise SystemExit(0 if all(checks.values()) else 1)
PY
```

Returned:

```text
no live piece before ratification: PASS
future pieces have role fields: PASS
future pieces have proof plans: PASS
all pieces covered by milestones: PASS
first real user surface named: PASS
both work records consumed: PASS
pieces 1 through 11: PASS
```

### Tester round 2 — sent back behind Shape

The same tester re-read commit `674a7db`. Every original Shape blocker closed, but Map correctly remained sent back while Shape awaited judgment. The tester also found that pieces 10 and 11 did not name their exact acceptance rulings, the mechanical check tested only for a `proof plan:` label, and `state.md` plus this record contradicted the map about whether piece 8 was live. Shape has since closed at `0680580`. Product made piece 8 live, named the exact rulings on pieces 8–11, aligned state and mapping, and expanded the completion check below. The same tester must run every Map control plus one free attack before the judge hears it.

### Mechanical completion after Shape closed — 2026-08-31

Command:

```sh
python3 - <<'PY'
from pathlib import Path
text = Path('map.md').read_text()
state = Path('state.md').read_text()
lines = text.splitlines()
pieces = {n: next((line for line in lines if line.startswith(f'{n}. ')), '') for n in range(1, 12)}
future = [pieces[n] for n in range(8, 12)]
quality = ('works', 'delivers the promise', 'good to use', 'quality hangs together', 'structure')
checks = {
    'one live piece and it is piece 8': text.count('[LIVE') == 1 and '[LIVE — Shaped]' in pieces[8],
    'future pieces have role fields': all('expected active roles:' in line and 'earliest uncertainty:' in line for line in future),
    'future pieces have proof plans': all('proof plan:' in line for line in future),
    'future pieces name exact quality rulings': all('acceptance rulings:' in line and all(q in line for q in quality) for line in future),
    'milestones requiring Business name it': all('Business' in pieces[n] for n in (8, 9, 11)),
    'all pieces covered by milestones': all(name in '\n'.join(lines[4:12]) for name in (
        'v3 discipline', 'v4 experience→judge', 'v5 the hearing', 'the campaigns land',
        "a builder's words and fewer of them", 'name the words', 'three producers',
        'a separated product team', 'v11 converter', 'CI limit enforcement', 'promise-conservation check')),
    'first real user surface named': 'first real user surface' in text,
    'both work records consumed': all(x in text for x in ('work/shaping.md', 'work/separated-product-team.md')),
    'pieces 1 through 11': all(pieces.values()),
    'state agrees piece 8 is live': 'one live Shaped piece' in state and 'No piece is live' not in state,
}
for name, passed in checks.items():
    print(f'{name}: {"PASS" if passed else "FAIL"}')
raise SystemExit(0 if all(checks.values()) else 1)
PY
```

Returned ten `PASS` lines: one live piece 8; role fields; proof plans; exact quality rulings; required Business rulings; complete milestone coverage; first real surface; both consumed records; pieces 1–11; and state agreement.

### Tester round 3 — sent back

At `2b9a419`, the tester re-executed both prior failure sets and the expanded ten-check population. Those controls all closed. The full proof-plan read found two new blockers: pieces 10 and 11 each named only one fresh tester instead of the required two, and piece 10 made Business active over cost-versus-drag but deferred its Business ruling to the milestone. Product named at least two exact fresh tester roles for every future piece and made Business binding on piece 10. The completion command now checks those contents rather than the presence of labels.

### Full completion run after tester round 3 — 2026-08-31

Command:

```sh
python3 - <<'PY'
from pathlib import Path
text = Path('map.md').read_text(); state = Path('state.md').read_text(); lines = text.splitlines()
pieces = {n: next((line for line in lines if line.startswith(f'{n}. ')), '') for n in range(1, 12)}
future = [pieces[n] for n in range(8, 12)]
quality = ('works', 'delivers the promise', 'good to use', 'quality hangs together', 'structure')
def tester_count(line):
    roles = line.split('fresh tester roles:', 1)[1].split('· acceptance rulings:', 1)[0]
    return len([x for x in roles.replace(' and ', ',').split(',') if x.strip()])
checks = {
    'one live piece and it is piece 8': text.count('[LIVE') == 1 and '[LIVE — Shaped]' in pieces[8],
    'future pieces have role fields': all('expected active roles:' in x and 'earliest uncertainty:' in x for x in future),
    'future pieces have proof plans': all('proof plan:' in x for x in future),
    'future pieces name at least two tester roles': all('fresh tester roles:' in x and tester_count(x) >= 2 for x in future),
    'future pieces name exact quality rulings': all('acceptance rulings:' in x and all(q in x for q in quality) for x in future),
    'all affected pieces name Business ruling': all('Business `kept / broken / not judged`' in pieces[n] for n in (8, 9, 10, 11)),
    'all pieces covered by milestones': all(name in '\n'.join(lines[4:12]) for name in ('v3 discipline', 'v4 experience→judge', 'v5 the hearing', 'the campaigns land', "a builder's words and fewer of them", 'name the words', 'three producers', 'a separated product team', 'v11 converter', 'CI limit enforcement', 'promise-conservation check')),
    'first real user surface named': 'first real user surface' in text,
    'both work records consumed': all(x in text for x in ('work/shaping.md', 'work/separated-product-team.md')),
    'pieces 1 through 11': all(pieces.values()),
    'state agrees piece 8 is live': 'one live Shaped piece' in state and 'No piece is live' not in state,
}
for name, passed in checks.items(): print(f'{name}: {"PASS" if passed else "FAIL"}')
raise SystemExit(0 if all(checks.values()) else 1)
PY
```

Returned `PASS` for all eleven named checks and exit code 0.

### Final Map re-test and judgment — sufficient

At `f117394`, the fresh tester re-executed every blocker from all three send-backs and the exact full completion command. All eleven named checks returned `PASS`; the tester's free attack found no hidden product dependency or extra owner beat. Verdict: **SUFFICIENT**. The separate judge challenged the favorable result and ruled **SUFFICIENT**: piece 8 is one independently useful increment with its first surface named; pieces 8–11 have the required uncertainties, runs, fresh people, quality rulings, and Business gates; Product stays the owner's single interface; state, map, and the authorized order agree. The owner's recorded implementation authorization ratifies this unchanged order. Map closes.

## Round 3 — selective separation re-cut

The universal piece failed before half its role flow completed. Shape reopened, and the owner later saw the complete repaired promise and selected, verbatim:

> Lock selective separation!

That changes role activation, migration semantics, cost admission, and the live piece's proof order, so Map reopens. The same still-current Shape carriers resumed with the delta only for the first Map after the changed promise.

### Four separate mapping contributions

**Product — carrier `/root` — active.** Evidence: the ratified promise at `66bfb43`, current product and map, the five governed attempts, the eight promises, and the three mapping contributions below. Conclusion: the old piece contains two runnable uncertainties that failed independently—whether repositories receive and apply the right selective contract, and whether real host carriers can execute it inside the limit. Assumptions: a piece must be independently runnable and judgeable, not independently releasable; the v6 milestone remains the release boundary. Proposed change: split at that executable seam, keep Product as the one owner interface, and do not create a third proof-only piece.

**Business — carrier `/root/business_cost_return` — active.** Direct evidence: `product.md`'s adoption and cost conditions, run 5's 266,484-token stop, current upgrader fixtures, and the proof/review cost of extra pieces. Conclusion: two pieces are the smallest useful boundary; Business preferred grouping fresh selective execution first and existing-product migration second so a migration defect cannot force the expensive host path to rerun. Assumptions: fresh adoption and existing-product migration are independently valuable user jobs, and piece hearings add no owner sign-off. Proposed change: cost admission before either full host run, Business binding on both pieces and the milestone, and no release while the installed candidate remains Business broken.

**Experience — carrier `/root/redesign_experience_role` — active.** Direct evidence: the installed words and templates, product-specific Experience conditions, the failed all-role barrier, and the fresh-versus-upgrading builder journeys. Conclusion: keep one piece because runner-only or migration-only work is not an owner-usable release and splitting repeats active roles and review. Assumptions: a piece may carry multiple executed proof lanes, and migration remains one product surface unless measured evidence shows incompatible behavior. Proposed change if Product keeps one piece: order it internally as rules, selection controls, component admission, fresh build, migration, hosts, and review. Earliest informative Experience run is a disposable install where a fresh builder routes contrasting pieces and gives the owner one synthesis.

**Engineering — carrier `/root/redesign_engineering_role` — active.** Direct evidence: the current installed files and runner, `isPreV6()` treating rc.1 as already migrated, the universal template/checker assumptions, and run 5's separate semantic and transport failures. Conclusion: split into two, but keep migration with the contract it installs; fresh install, v5 upgrade, rc.1 repair, idempotence, and deterministic role selection run without live host transport. Assumptions: current Shape carriers can prove the first piece; host evidence remains mandatory for the second; the same shared executable files are changed sequentially. Proposed change: piece 8 owns installed semantics and migration as `6.0.0-rc.2`; piece 9 owns bounded host transport and full cross-host proof.

### Product synthesis and preserved dissent

Product selects Engineering's seam. The installed contract and migration are one product behavior: splitting them could leave rc.1 repositories carrying the obsolete universal promise, and both live in the upgrader's installed surface. Host transport and cost are a different executable uncertainty: they can fail without changing which roles a repository should call. Therefore:

1. **The right roles show up** installs and migrates the selective contract and proves deterministic routing, current-piece repair, idempotence, footprint, and honesty without a costly governed run.
2. **The team finishes inside its limit** consumes that exact Judged contract, then proves real contexts, direct evidence, implementation, informative returns, cost, and both hosts before the milestone hearing.

Business's fresh-versus-migration split is preserved because it isolates a real adoption journey, but Product rejects it at this map: migration installs the same contract and rc.1 is already a demonstrated semantic repair case. Experience's one-piece recommendation is preserved because only the milestone is releasable, but Product rejects it: another host failure would needlessly reopen already-runnable repository semantics and migration. A third proof-only piece is rejected by all useful evidence; it adds a hearing without adding product behavior.

All four roles honestly fire on both v6 pieces under the product-specific conditions. The kernel change touches adoption, cost, method wording, templates, migration, builder flow, and host execution. Selectivity is proved through contrasting product fixtures, not by pretending either lens is inactive here.

### Ordering choices for the owner

- **Two pieces at the executable seam (Recommended):** first install and migrate the right contract; then prove real carriers finish inside the limits. Failures stay inside the behavior they can actually invalidate. Cost: one additional piece review, but no additional owner sign-off before the milestone.
- **One integrated piece:** fewer piece records and one review, but any later transport or migration failure can reopen the full rule-and-proof population.
- **Two pieces at the adoption seam:** first fresh selective execution, then migration. It isolates the existing-product journey, but splits the same installed semantics across two pieces and complicates rc.1 repair.

The platform and care decision do not change: plain git plus Node, supported Codex and Claude hosts as proving subjects, no new dependency, milestone treatment with two independent judges, and no protected product code.

### Re-cut completion test

The current candidate must show: zero live pieces before ratification and exactly one `next`; pieces 1–12 in order; pieces 8–12 covered by milestones; every future piece names role calls, earliest informative runs, proof, at least two fresh tester roles, the five quality/structure rulings, and every required Business ruling; both shaped work records consumed; first surface named; no unconsumed supporting material; zero shaped screen captions; and state agreement. The exact command and output follow after the candidate is written.

The first probe compared the capitalized piece name `Promise-conservation check` with the lowercase milestone line and returned one false `FAIL`. Product corrected the check to compare milestone names case-insensitively; no product file changed between the two runs.

Command:

```sh
python3 - <<'PY'
from pathlib import Path
import re
m = Path('map.md').read_text(); p = Path('product.md').read_text(); s = Path('state.md').read_text(); lines = m.splitlines()
pieces = {n: next((line for line in lines if line.startswith(f'{n}. ')), '') for n in range(1, 13)}; future = [pieces[n] for n in range(8, 13)]
quality = ('works', 'delivers the promise', 'good to use', 'quality hangs together', 'structure')
def tester_count(line):
    roles = line.split('fresh tester roles:', 1)[1].split('· acceptance rulings:', 1)[0]
    return len([x for x in roles.replace(' and ', ',').split(',') if x.strip()])
product_sets = {label: len(re.findall(rf'(?mi)^\s*{label}:', p)) for label in ('job', 'moment', 'claim')}
screen_captions = len(re.findall(r'(?mi)^\s*screen:', p + '\n' + Path('work/shaping.md').read_text()))
milestones = '\n'.join(lines[3:12]).lower()
checks = {
    'zero live before ratification': m.count('[LIVE') == 0,
    'exactly one next and it is piece 8': m.count('[next') == 1 and '[next — Map awaiting ratification]' in pieces[8],
    'pieces 1 through 12': all(pieces.values()),
    'future pieces name role calls': all('role calls:' in x for x in future),
    'future pieces name earliest informative runs': all('earliest informative run:' in x for x in future),
    'future pieces have proof plans': all('proof plan:' in x for x in future),
    'future pieces name at least two tester roles': all('fresh tester roles:' in x and tester_count(x) >= 2 for x in future),
    'future pieces name quality and structure rulings': all('acceptance rulings:' in x and all(q in x for q in quality) for x in future),
    'every affected future piece names Business ruling': all('Business `kept / broken / not judged`' in pieces[n] for n in range(8, 13)),
    'milestones cover pieces 8 through 12': all(name.lower() in milestones for name in ('the right roles show up', 'the team finishes inside its limit', 'v11 converter', 'CI limit enforcement', 'Promise-conservation check')),
    'first real user surface named': 'first real user surface' in m,
    'both shaped work records consumed': all(x in m for x in ('work/shaping.md', 'work/separated-product-team.md')),
    'all labeled product sets assigned': sum(product_sets.values()) == 0,
    'all shaped screen captions assigned': screen_captions == 0,
    'unconsumed material explicitly empty': '## Unconsumed shaped material\n- None' in m,
    'state agrees no piece is live': 'No piece is live' in s,
}
print('population: pieces=12 future=5 milestones=5 labeled_product_sets=' + str(product_sets) + f' shaped_screen_captions={screen_captions}')
for name, passed in checks.items(): print(f'{name}: {"PASS" if passed else "FAIL"}')
raise SystemExit(0 if all(checks.values()) else 1)
PY
```

Returned exit code 0 and:

```text
population: pieces=12 future=5 milestones=5 labeled_product_sets={'job': 0, 'moment': 0, 'claim': 0} shaped_screen_captions=0
zero live before ratification: PASS
exactly one next and it is piece 8: PASS
pieces 1 through 12: PASS
future pieces name role calls: PASS
future pieces name earliest informative runs: PASS
future pieces have proof plans: PASS
future pieces name at least two tester roles: PASS
future pieces name quality and structure rulings: PASS
every affected future piece names Business ruling: PASS
milestones cover pieces 8 through 12: PASS
first real user surface named: PASS
both shaped work records consumed: PASS
all labeled product sets assigned: PASS
all shaped screen captions assigned: PASS
unconsumed material explicitly empty: PASS
state agrees no piece is live: PASS
```

## Selective Map review receipt — opened before dispatch

- Candidate: `map.md`, this Round 3 record, `product.md`, `state.md`, and the ratified Round 4 Shape record at the commit containing this receipt.
- Fresh tester: `/root/selective_map_tester` — did not shape, map, contribute a product role, implement, or review either v6 candidate.
- Judge: `/root/selective_map_judge` — a separate future carrier that did not shape, map, contribute, implement, test, or review either candidate.
- Planned probe: execute the full re-cut completion population; challenge whether each new piece is independently runnable, whether the seam prevents irrelevant re-runs without hiding an integrated dependency, whether trigger decisions match `product.md`, and whether the proposed order preserves one owner interface and every original release requirement.
- Planned controls: restore the one-piece map and reproduce cross-invalidation; move migration behind host proof and reproduce rc.1 semantic drift; mark Business or Experience inactive on either v6 piece; omit the second piece from the milestone; and try to advance piece 9 before piece 8 is Judged.
- Skeptical attack: find one changed installed or executable home whose ownership or proof falls between the pieces.
- Dispatch: only after this receipt and the completion command are committed.
- Verdict and judgment: pending.

### Selective Map tester round 1 — sent back

At `8be7757`, `/root/selective_map_tester` executed the full 16-check completion population and returned every line green. The one-piece cross-invalidation, migration-after-host, false-inactive role, missing milestone piece, and premature piece-9 controls also held. Its independent home-by-home attack found one seam leak: piece 8 owned `bin/speck-next.js`, but its proof plan did not explicitly require the rc.1→rc.2 version crossing, exact version-span report, or complete changed-path output. Piece 9 could therefore claim to consume an “exact installed contract” whose version had never been proven. Verdict: **SEND BACK**.

Product repaired the current map. Piece 8 now makes `6.0.0-rc.2` part of its outcome, treats both v5 and the obsolete universal rc.1 as migration sources, and requires the marker, exact from→to span, every changed path, and the complete installed-surface plus `product.md` diff to be exercised. Piece 9 explicitly consumes the **Judged `6.0.0-rc.2`** contract. The completion population also gains checks for both facts, so the dependency is no longer held only by prose inspection.

### Expanded completion re-run

Command: the committed re-cut completion command above, plus these two entries in `checks`:

```python
'piece 8 proves rc2 version and output span': all(x in pieces[8] for x in ('`6.0.0-rc.2`', 'exact from→rc.2 version/marker reporting', 'complete changed-path and surface diff output')),
'piece 9 waits for Judged rc2 contract': '[queued — requires piece 8 Judged]' in pieces[9] and 'Judged `6.0.0-rc.2` installed contract' in pieces[9],
```

Returned exit code 0 with the original 16 `PASS` lines plus:

```text
piece 8 proves rc2 version and output span: PASS
piece 9 waits for Judged rc2 contract: PASS
```

### Selective Map re-test receipt — opened before dispatch

- Candidate: the original full population and controls at `8be7757`, plus the tester's finding, repaired `map.md`, and expanded dependency checks at the commit containing this receipt.
- Re-tester: `/root/selective_map_tester`, replaying the exact seam failure and all prior controls.
- Free attack: try an rc.1 repository with the exact generated universal section and one with owner-authored Product-team content; the former must receive an honest selective assessment, the latter must be preserved without letting the old marker suppress the assessment.
- Judge: `/root/selective_map_judge`, dispatched only after the re-test is sufficient.
- Verdict and judgment: pending.

### Selective Map re-test — sufficient

At `d2b2e66`, `/root/selective_map_tester` replayed the original 16 checks, both new seam checks, all five prior controls, and the two rc.1 migration attacks. All 18 completion checks passed. The exact generated universal rc.1 section is now an explicit migration source; owner-authored Product-team content stays preserved while the old rc.1 marker cannot suppress the required assessment. Restoring one-piece cross-invalidation, moving migration behind host proof, omitting piece 9 from the milestone, or advancing it before piece 8 is Judged each failed the candidate's stated or mechanical dependency. Every original v6 requirement remains consumed across the two pieces. Verdict: **SUFFICIENT**.

### Selective Map judge receipt — opened before dispatch

- Candidate: `d2b2e66` plus the exact re-test verdict above at the commit containing this receipt.
- Judge: `/root/selective_map_judge` — did not shape, map, contribute a role, implement, test, or review either v6 candidate.
- Challenge: try to overturn the tester's favorable verdict against the ratified selective promise, the eight contract promises, both failed Map controls, every original v6 release requirement, and the complete file ownership seam. Judge the three ordering choices and whether Product's recommendation is the smallest independently runnable cut rather than method ceremony.
- Dispatch: only after this receipt is committed.
- Judgment: pending.

### Selective Map final judgment — sufficient

At `2f21837`, `/root/selective_map_judge` replayed both prior release-proof failures, challenged the 21-check population, compared all three cuts again, and attacked the split for an extra owner beat or a piece-level green masquerading as release. The exact milestone roster and rulings now stand; the combined leak scan runs after every piece-9 change; piece 9 cannot start before the Judged rc.2 contract; neither piece can become `6.0.0` without the milestone hearing, Business ruling, two judges, and owner grade; and the split adds one autonomous piece review but no owner sign-off. The judge again found the executable seam smaller and safer than either alternative. Judgment: **SUFFICIENT**.

The only remaining Map condition is the owner's ratification of the reviewed order. If the owner selects the recommended two-piece seam unchanged, no further Map-only re-test is required.

## Round 4 — owner ratifies the executable seam

The owner saw the three reviewed ordering choices in the conversation. Product recommended:

> **Two pieces at the executable seam:** first install and migrate the right contract; then prove real carriers finish inside the limits. Failures stay inside the behavior they can actually invalidate. Cost: one additional piece review, but no additional owner sign-off before the milestone.

**Owner selection, verbatim:**

> Do it!

This selects the recommended two-piece order. Map closes. “The right roles show up” becomes the one live piece; “The team finishes inside its limit” remains queued until piece 8 is Judged. The platform, care, release roster, and owner touchpoints remain unchanged.

### Selective Map judgment round 1 — sent back

At `39ac08c`, `/root/selective_map_judge` challenged the favorable re-test and upheld the executable seam. It found two dropped release obligations. First, piece 9 had reduced the owner's exact four-person milestone roster and release-specific rulings to unnamed fresh people and generic qualities. Second, the public-detail scan sat only in piece 8 even though piece 9 changes executable release files afterward. Either omission could let the split release with less proof than the original authorized piece. Verdict: **SEND BACK**.

Product restored both without changing the pieces or order. Piece 9 now names the four exact milestone experiences: first-time adoption, real product-building work, a second host/repository, and the worst day of missing contexts or mid-product migration. Its two independent judges must challenge the same records and rule the four qualities, milestone Business case, migration honesty, owner-attention cost, and distinct actions rather than duplicate prose. The final case-insensitive public-detail scan now covers the combined release diff after every piece-9 change; piece 8's earlier scan remains an incremental control, not release proof.

### Release-conservation completion run

Command: the 18-check completion command above, plus:

```python
roster = ('first-time adoption', 'real product-building work', 'second host/repository', 'worst day of missing contexts or mid-product migration')
release_rulings = ('works', 'delivers the promise', 'good to use', 'quality hangs together', 'milestone Business case', 'migration honesty', 'owner-attention cost', 'distinct actions rather than duplicate prose')
checks['exact milestone tester roster conserved'] = all(x in pieces[9] for x in roster)
checks['exact milestone rulings conserved'] = 'two independent judges' in pieces[9] and all(x in pieces[9] for x in release_rulings)
checks['combined final public-detail scan'] = 'case-insensitive public-detail scan over the combined release diff after every piece-9 change' in pieces[9]
```

Returned exit code 0 with the prior 18 `PASS` lines plus:

```text
exact milestone tester roster conserved: PASS
exact milestone rulings conserved: PASS
combined final public-detail scan: PASS
```

### Selective Map final re-test receipt — opened before dispatch

- Candidate: the full prior control population plus the judge's two failures, repaired `map.md`, and the three release-conservation checks at the commit containing this receipt.
- Re-tester: `/root/selective_map_tester`, replaying all 21 checks and both dropped-requirement controls.
- Skeptical attack: compare every release condition in the owner's original plan and `work/separated-product-team.md` with the two current pieces; any unmatched condition sends the map back.
- Re-judge: `/root/selective_map_judge`, after a sufficient re-test.
- Verdict and judgment: pending.

### Selective Map final re-test — sufficient

At `0e34587`, `/root/selective_map_tester` replayed all 21 completion checks, the five original controls, both rc.1 attacks, and both dropped-release controls. Every check returned `PASS`. Its skeptical attack matched every condition from the owner's authorized plan and the original one-piece proof plan to pieces 8 or 9: install and migration honesty, version and diff reporting, budgets, controls, Codex, Claude, the ungoverned miss, the exact milestone roster, two judges and their release-specific rulings, owner grade, and the final combined leak scan all have a destination. Verdict: **SUFFICIENT**.

### Selective Map final judgment receipt — opened before dispatch

- Candidate: `0e34587` plus the exact final re-test verdict above at the commit containing this receipt.
- Re-judge: `/root/selective_map_judge`, replaying both prior release-proof failures and challenging the complete conserved population.
- Free attack: find any way a piece-specific green can be mistaken for the final v6 release decision, or any owner touchpoint added by the split.
- Dispatch: only after this receipt is committed.
- Judgment: pending.

## Round 5 — owner ratifies the Piece 9 cost boundary

The first native Piece 9 attempt produced four valid, distinct role contributions but stopped before Product synthesis or code because its 200,484 gross tokens left too little room under the 250,000-gross boundary. Product did not erase or rescue that failure. It showed one versioned exchange: preserve those same carriers and their evidence; count their 56,228 fresh tokens and 112.284 active seconds; allow one continuation up to 200,000 cumulative fresh tokens and 900 cumulative active seconds; and tighten the path to exactly five remaining host turns with no replacement, retry, fallback, helper, or further owner interruption. Gross remains measured and Business-judged.

**Owner selection, verbatim:**

> Approve v0.9

The selection changes Piece 9's cost proof, not the set or order of pieces. Product and Engineering remain distinct; all four roles remain active for the same reasons; the old attempt remains failed; the release roster and rulings are unchanged. The current evidence routes directly back to Piece 9 setup and the five-turn continuation. No new owner beat is added before the final milestone grade and ratification.
