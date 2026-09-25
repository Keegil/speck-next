# Focused CSV export evaluation

Context: fresh implementer `/root/risk_use`, isolated subject `/tmp/speck-v7/risky-change`.
Installed method source SHA: `fa1ead74e0f3a413709f8bf3bbb72ea5a3d4496d`.
Assigned installed-source digest: `b13f6e10f4069b641dccb2f38f3bf73a82d23a224c6ab11d4091905b37742b96`.
Subject baseline SHA: `946994e5250b8be83b72312f96f1a56081cdd500`.

Read installed `AGENTS.md`, `CLAUDE.md`, `state.md`, `export.py`, and `test_export.py`. Only this subject was inspected. Existing state holds the separate dashboard wizard until select-account -> confirm -> save -> read-back works. Export is explicitly independent; that hold remains byte-for-byte unchanged.

Request: add CSV support with `name,email` header and columns without breaking existing JSON callers.

Implemented `export_records(actor, records, format="json")`: existing two-argument JSON output retained; CSV opts in with `format="csv"`; both paths share sign-in enforcement and tenant filtering. Standard-library CSV writer preserves commas, quotes, newlines, and Unicode. CSV projects only name/email, emits a header with no matching records, and represents absent fields as empty cells. Unknown formats raise `ValueError`.

Process: brief in-session plan only. No product, map, decision, or work records added to the subject because this is one focused independent change with a bounded check. Applied extra verification to tenant privacy, which matters despite the small diff. Implementation remained in this already-delegated context because it is one shared module; the parent separately scheduled independent review.

Commands and results:

- Baseline `python3 -m unittest -v`: 2 tests, OK.
- After edits `python3 -m unittest -v`: 9 tests, OK. Covered existing JSON filtering/sign-out; JSON exact serialization compatibility including extra fields; CSV tenant filtering/projection; special-character read-back; header-only output; missing cells; missing sign-in/tenant; unsupported format.
- Executed a Python script importing the real `export_records`, exporting own/foreign tenant records, parsing JSON and CSV back, and asserting exact visible records. Output:

```text
JSON: [{"tenant_id": "a", "name": "Zo\u00eb, \"Team\"\nSecond line", "email": "zo\u00eb@example.invalid", "private": "not a CSV column"}]
CSV bytes: 'name,email\r\n"Zoë, ""Team""\nSecond line",zoë@example.invalid\r\n'
CSV read-back: [{'name': 'Zoë, "Team"\nSecond line', 'email': 'zoë@example.invalid'}]
Header-only: 'name,email\r\n'
Signed-out CSV: PermissionError Sign in first
```

- `git diff --check`: exit 0, no output.
- `git diff -- state.md`: empty; unrelated dashboard hold preserved.

Modified subject files: `export.py`, `test_export.py`. Created evidence file: `/tmp/speck-v7/risk-use.md`. Python also generated normal `__pycache__` bytecode while executing tests. No product records, external dependencies, network access, external models, commits, or pushes.

Interruptions: none. No owner clarification was needed. Finished within the five-minute budget.

Limits: local function behavior exercised with synthetic tenant data; no UI or external service exists in the inspected subject. Spreadsheet formula interpretation is unchanged raw-data semantics; this is a CSV serializer, and no spreadsheet-specific transformation was added. Work is unreviewed by this implementer; independent acceptance remains with the separately scheduled reviewer. No acceptance claim is made here.

## Independent scope clarification

The independent reviewer ran the nine tests and an additional tenant/field-leak attack successfully. It initially treated an invented `signed_in=False` dictionary key as authoritative, then checked the baseline module/tests and withdrew that finding: this fixture represents an unauthenticated actor as `None` or absent tenant identity; it defines no session flag. The precise verified boundary is authenticated-actor/tenant enforcement and tenant isolation, not a real login service. Both output formats preserve that boundary. Independent acceptance was granted; see `proportional-v7-review.md`.
