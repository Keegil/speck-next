#!/usr/bin/env bash
# Plant a double space in pulse's empty-state tip. Control mode = same planting, no agent will fix it.
set -eu
CLONE="$1"
python3 - "$CLONE/examples/pulse/pulse.py" <<'EOF'
import sys
p = sys.argv[1]
s = open(p).read()
assert "Start with: pulse 3" in s or "Start with:  pulse 3" in s
s = s.replace("Start with: pulse 3", "Start with:  pulse 3")
open(p, "w").write(s)
EOF
