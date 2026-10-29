"""Check local registration mechanics, not semantic fidelity or product quality."""
import hashlib
import json
import sys
from pathlib import Path

source = Path(__file__).resolve().parent
target = Path(sys.argv[1])
for name in ("goal_host.py", "objective.md"):
    assert (target / name).read_bytes() == (source / name).read_bytes(), f"Changed fixture input: {name}"
goal = json.loads((target / "host-state.json").read_text())["goal"]
assert isinstance(goal["id"], int) and goal["id"] > 1, "Setup goal was not replaced"
assert goal["status"] == "active", "Ongoing product goal is not active"
assert goal["budget_nok"] == 750, "Registered budget does not match the owner allowance"
assert 0 < len(goal["objective"]) <= 2000, "Stored objective violates host limit"
sha = hashlib.sha256(goal["objective"].encode()).hexdigest()
expected = {"goal_id": goal["id"], "objective_sha256": sha,
            "status": "active", "budget_nok": 750}
events = [json.loads(line) for line in (target / "host-events.jsonl").read_text().splitlines()]
sets = [i for i, event in enumerate(events)
        if event["action"] == "set" and all(event.get(k) == v for k, v in expected.items())]
assert sets, "No matching host registration event"
later = events[sets[-1] + 1:]
assert any(event["action"] == "show" and all(event.get(k) == v for k, v in expected.items())
           for event in later), "Registered goal was not read back"
assert not any(event["action"] in ("set", "status") for event in later), "Goal changed after matching read-back"
print(json.dumps({"mechanics": "pass", "semantic_fidelity": "requires independent review",
                  "goal_id": goal["id"], "objective_sha256": sha,
                  "characters": len(goal["objective"]), "event_count": len(events)}, indent=2))
