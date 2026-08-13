#!/usr/bin/env bash
# Plant a double space in pulse's empty-state tip. Fails loudly if the planting didn't land.
set -eu
CLONE="$1"
python3 - "$CLONE/examples/pulse/pulse.py" <<'EOF'
import sys
p = sys.argv[1]
s = open(p).read()
s = s.replace("Start with: pulse 3", "Start with:  pulse 3")
open(p, "w").write(s)
EOF
grep -q "Start with:  pulse 3" "$CLONE/examples/pulse/pulse.py" || { echo "planting failed: double space not present"; exit 1; }
