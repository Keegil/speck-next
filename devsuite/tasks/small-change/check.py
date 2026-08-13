#!/usr/bin/env python3
"""Small change: fixed and verified, zero method paperwork."""
import os, subprocess, sys

clone = sys.argv[1]
pulse = os.path.join(clone, "examples", "pulse")
env = dict(os.environ, PULSE_FILE=os.path.join(clone, ".check-journal.json"))
ok = True


def note(label, good):
    global ok
    print(f"  [{'ok' if good else 'RED'}] {label}")
    ok = ok and good


out = subprocess.run(["python3", "pulse.py"], cwd=pulse, env=env, capture_output=True, text=True)
note("KEY: empty-state tip has a single space", "Start with: pulse 3" in out.stdout and "Start with:  pulse 3" not in out.stdout)

changed = subprocess.run(["git", "status", "--porcelain"], cwd=clone, capture_output=True, text=True).stdout.splitlines()
changed = [l for l in changed if ".driver.log" not in l and ".check-journal" not in l]
note("only pulse.py touched, no new files", all(l.strip().endswith("examples/pulse/pulse.py") for l in changed) and len(changed) <= 1)
note("no method files written (state.md, work/ untouched)", not any("state.md" in l or "work/" in l for l in changed))

sys.exit(0 if ok else 1)
