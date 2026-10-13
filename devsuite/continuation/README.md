# Offline continuation cases

This fixture checks two complete jobs of one tiny real Python CLI. It is
an independent product subject, not a modification of Odd or the default
release suite. No model calls or external services are needed to set it up.

From the Speck Next checkout:

```sh
python3 devsuite/continuation/setup.py packing /tmp/continuation-packing
python3 devsuite/continuation/setup.py integrity /tmp/continuation-integrity
python3 devsuite/continuation/check.py packing /tmp/continuation-packing
python3 devsuite/continuation/check.py integrity /tmp/continuation-integrity
```

The two checks must fail before a model repair. Setup refuses an existing
destination, so each arm starts from a fresh copy. Supply the selected
method as AGENTS.md, send its frozen prompt from PROMPTS.md, and evaluate
the resulting checkout with the same check command. The checker copies
only the implementation to an isolated temporary directory and supplies
its own data. It does not inspect instruction wording or heading style.

Baseline reproduction on 2026-10-13: both exited 1. Packing failed because
Passport remained pending after marking visible row 1. Integrity failed
because the damaged store was overwritten. Checker positive controls
passed: selecting from pending rows repaired packing, and propagating the
JSON parse failure preserved damaged data while ordinary adds still worked.
Those controls were applied only to staging copies, not this fixture.

Packing verifies visible selection, persisted state, and the restarted
pending view without changing unrelated items. Integrity verifies that a
damaged private store is preserved, the command reports failure, and an
ordinary add still works once the store is repaired. The latter is a
counterexample to automatically replacing useful infrastructure repair
with visible-interface work.

Reconcile active generated v6 procedure while retaining explicit owner
constraints. This is a separate review observation; the job checker does
not use record keywords as a substitute for functioning behavior.

Record per arm the method SHA/text hash, model, budget, exit status,
elapsed time and usage if available. Both arms passing supports no quality
gain claim. A failure establishes only this case's result, not a general
advantage. No model comparison results are included in this fixture.
