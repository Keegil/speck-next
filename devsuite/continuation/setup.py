import json
import shutil
import sys
from pathlib import Path

source = Path(__file__).resolve().parent
case, destination = sys.argv[1:]
assert case in ("packing", "integrity")
target = Path(destination)
target.mkdir(parents=True, exist_ok=False)
shutil.copy(source / "pack.py", target / "pack.py")
shutil.copy(source / f"{case}-state.md", target / "state.md")
(target / "product.md").write_text((source / "product.txt").read_text())
(target / "items.json").write_text(json.dumps([
    {"name": "Toothbrush", "packed": True},
    {"name": "Passport", "packed": False},
    {"name": "Charger", "packed": False},
], indent=2) + "\n")
print(target.resolve())
