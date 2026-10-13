import argparse
import json
import sys
from pathlib import Path

p = argparse.ArgumentParser(description="A private packing list")
p.add_argument("command", choices=["list", "mark", "add"])
p.add_argument("value", nargs="?")
p.add_argument("--pending", action="store_true")
a = p.parse_args()
store = Path("items.json")
damaged = False
try:
    items = json.loads(store.read_text())
except FileNotFoundError:
    items = []
except json.JSONDecodeError:
    damaged = True
    items = None

if damaged:
    print(
        "Could not use items.json: file is not valid JSON. "
        "Repair it manually; your data was left unchanged.",
        file=sys.stderr,
    )
    sys.exit(1)

if a.command == "list":
    visible = [x for x in items if not a.pending or not x["packed"]]
    print("Packing list")
    for number, item in enumerate(visible, 1):
        print(f'{number}. {item["name"]} [{"packed" if item["packed"] else "pending"}]')
elif a.command == "mark":
    items[int(a.value) - 1]["packed"] = True
    store.write_text(json.dumps(items, indent=2) + "\n")
    print("Packed")
else:
    items.append({"name": a.value, "packed": False})
    store.write_text(json.dumps(items, indent=2) + "\n")
    print("Added")
