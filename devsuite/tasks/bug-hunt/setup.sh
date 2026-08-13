#!/usr/bin/env bash
# Plant the chart-invents-data bug: remove value validation on load, then corrupt one journal value.
set -eu
CLONE="$1"
python3 - "$CLONE/examples/pulse/pulse.py" <<'EOF'
import sys
p = sys.argv[1]
s = open(p).read()
needle = """    for day, value in entries.items():
        try:
            date.fromisoformat(day)
        except ValueError:
            raise SystemExit(BAD_JOURNAL)
        if type(value) is not int or value not in BLOCKS:  # bools and floats are not energy
            raise SystemExit(BAD_JOURNAL)
"""
assert needle in s, "expected validation block not found"
open(p, "w").write(s.replace(needle, ""))
# BLOCKS lookup must tolerate the corrupt value being drawn, as the original bug did
s = open(p).read()
old = 'BLOCKS[entries[d.isoformat()]]'
assert old in s
open(p, "w").write(s.replace(old, 'BLOCKS.get(entries[d.isoformat()], "█")'))
EOF
