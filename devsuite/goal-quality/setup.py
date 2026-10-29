"""Create one isolated worker checkout; the evaluator stays outside it."""
import json
import shutil
import sys
from pathlib import Path

source = Path(__file__).resolve().parent
target = Path(sys.argv[1])
target.mkdir(parents=True, exist_ok=False)
for name in ("goal_host.py", "objective.md"):
    shutil.copyfile(source / name, target / name)
state = {"goal": {"id": 1, "objective": "Read objective.md before continuing.",
                  "status": "active", "budget_nok": 0}}
(target / "host-state.json").write_text(json.dumps(state, indent=2) + "\n")
(target / "host-events.jsonl").write_text("")
print(target.resolve())
