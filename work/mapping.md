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
- Every piece names runs, checks, testers, rulings, expected active roles, and its four earliest uncertainties: yes for the live piece; queued triggered pieces retain their existing proof statements.
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
