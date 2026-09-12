# Whole-interaction repair: small-change use

Date: 2026-09-12  
Subject: `.local/whole-experience-loop/subjects/report-typo`  
Scenario identifiers supplied by the controller: receipt `8d9bc8c`; Built line `3467c27`; installed-method digest `9881c10d660b7446d85853aabed941bbc94c2d419c20a23c964dbaea68a79351`.

## Decision

This was a small change. `report.py` changes one success-message spelling, adds no dependency, touches no protected behavior, changes no product promise, and is reversible in one edit. The subject's `state.md` says the formatter runs and that no unresolved product or role concern affects it. The installed method therefore required neither a new work file nor Product, Engineering, Business, or Experience roles.

## Change

`report.py` now returns `Saved report` instead of `Saved reprt`. The report-writing line and command path were left unchanged.

Observed diff:

```diff
-    return "Saved reprt"
+    return "Saved report"
```

## Runs and evidence

Executed from the subject directory:

```sh
python3 report.py && python3 check.py
```

Output:

```text
Saved report
report output preserved
```

Executed exact-message and content probe:

```sh
python3 - <<'PY'
from pathlib import Path
from report import save_report
import tempfile
with tempfile.TemporaryDirectory() as d:
    p = Path(d) / 'report.csv'
    result = save_report(p)
    expected = 'name,amount' + chr(10) + 'beans,3' + chr(10)
    assert result == 'Saved report'
    assert p.read_text(encoding='utf-8') == expected
print('exact message and report contents preserved')
PY
```

Output:

```text
exact message and report contents preserved
```

No new subject work files were created and no roles were asked for this fix. No commit was made. `git diff --check` produced no output and exited successfully for the subject diff.

## Skeptical attack: does the whole-interaction hold block an unrelated typo fix?

Read-only inspection of sibling `odd-return/state.md` found a held real-model portion-change journey: it consumes an unresolved prepared-week interaction. That state is a concrete, dependent product hold. It has no connection to this local formatter, whose subject state expressly says no unresolved concern affects it. The installed method's small-change rule says genuine unrelated repairs keep the cheap path.

Verdict: the method did not impose unnecessary work or interfere with this unrelated small fix. It distinguished the dependent interaction hold from a reversible wording correction; the command and its check ran immediately.
