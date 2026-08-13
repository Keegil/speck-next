#!/usr/bin/env python3
"""Bug hunt: a corrupted journal value must never be drawn as a real bar."""
import json, os, subprocess, sys
from datetime import date

clone = sys.argv[1]
pulse = os.path.join(clone, "examples", "pulse")
journal = os.path.join(clone, ".check-journal.json")
env = dict(os.environ, PULSE_FILE=journal)
ok = True
BLOCKS = "▁▂▄▆█"


def note(label, good):
    global ok
    print(f"  [{'ok' if good else 'RED'}] {label}")
    ok = ok and good


# KEY: corrupt values (true, 3.0, "3") must not render as bars
corrupt = {date.today().isoformat(): True}
open(journal, "w").write(json.dumps(corrupt))
out = subprocess.run(["python3", "pulse.py"], cwd=pulse, env=env, capture_output=True, text=True)
invented = out.returncode == 0 and any(b in out.stdout for b in BLOCKS)
note("KEY: corrupt journal value is refused or excluded, never drawn", not invented)

# happy path must still work
os.remove(journal)
r1 = subprocess.run(["python3", "pulse.py", "4"], cwd=pulse, env=env, capture_output=True, text=True)
r2 = subprocess.run(["python3", "pulse.py"], cwd=pulse, env=env, capture_output=True, text=True)
note("happy path intact: log a 4, see its bar", r1.returncode == 0 and r2.returncode == 0 and "▆" in r2.stdout)

sys.exit(0 if ok else 1)
