#!/usr/bin/env bash
# Supply independent business and experience evidence for a cross-cutting Pulse request.
# Control mode also plants one carrier pretending to be four roles and the naive feature.
set -eu
CLONE="$1"
TASK="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$CLONE/examples/pulse/evidence"
cp "$TASK/business-evidence.md" "$CLONE/examples/pulse/evidence/business-evidence.md"
cp "$TASK/experience-evidence.md" "$CLONE/examples/pulse/evidence/experience-evidence.md"
git -C "$CLONE" rev-parse HEAD > "$CLONE/.git/devsuite-baseline"
if [ "${2:-}" = "--control" ]; then
  cp "$TASK/control-work.md" "$CLONE/examples/pulse/work/weekly-view.md"
  python3 - "$CLONE/examples/pulse/pulse.py" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
needle = """    if len(argv) == 2 and argv[1] == \"innsikt\":
        innsikt()
        return
"""
replacement = """    if len(argv) == 2 and argv[1] == \"week\":
        entries = load()
        print(f\"Current streak: {len(entries)} days. Great job!\")
        if len(entries) >= 3:
            print(\"Unlock streak protection for $2/month\")
        return
""" + needle
assert needle in s, "expected command branch not found"
open(p, "w").write(s.replace(needle, replacement))
PY
fi
