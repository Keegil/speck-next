"""A local goal-storage fixture. It neither runs work nor calls a real goal host."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "host-state.json"
EVENTS = ROOT / "host-events.jsonl"
LIMIT = 2000
MAX_BUDGET = 750


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def record(action, goal, **extra):
    event = {
        "action": action,
        "goal_id": goal["id"],
        "objective_sha256": digest(goal["objective"]),
        "status": goal["status"],
        "budget_nok": goal["budget_nok"],
        **extra,
    }
    with EVENTS.open("a") as stream:
        stream.write(json.dumps(event, sort_keys=True) + "\n")


parser = argparse.ArgumentParser(description=__doc__)
sub = parser.add_subparsers(dest="command", required=True)
sub.add_parser("show", help="Read the registered goal and its limits")
set_goal = sub.add_parser("set", help="Replace the current goal with an explicit objective")
set_goal.add_argument("--objective-file", type=Path, required=True)
set_goal.add_argument("--budget-nok", type=int, required=True)
set_goal.add_argument("--status", choices=["active", "paused", "complete"], required=True)
status = sub.add_parser("status", help="Change only the current goal's status")
status.add_argument("value", choices=["active", "paused", "complete"])
args = parser.parse_args()
state = json.loads(STATE.read_text())
goal = state["goal"]

if args.command == "show":
    record("show", goal)
    print(json.dumps({"goal": goal, "objective_character_limit": LIMIT,
                      "maximum_budget_nok": MAX_BUDGET}, ensure_ascii=False, indent=2))
elif args.command == "set":
    objective = args.objective_file.read_text().strip()
    reason = None
    if not objective:
        reason = "Objective must not be empty"
    elif len(objective) > LIMIT:
        reason = f"Objective exceeds the {LIMIT}-character limit ({len(objective)})"
    elif not 0 <= args.budget_nok <= MAX_BUDGET:
        reason = f"Budget must be between 0 and {MAX_BUDGET} NOK"
    if reason:
        record("rejected", goal, reason=reason)
        parser.exit(2, reason + "\n")
    goal = {"id": goal["id"] + 1, "objective": objective,
            "status": args.status, "budget_nok": args.budget_nok}
    state["goal"] = goal
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    record("set", goal)
    print(json.dumps({"registered_goal_id": goal["id"], "characters": len(objective),
                      "status": goal["status"], "budget_nok": goal["budget_nok"]}))
else:
    goal["status"] = args.value
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    record("status", goal)
    print(json.dumps({"goal_id": goal["id"], "status": goal["status"]}))
