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
