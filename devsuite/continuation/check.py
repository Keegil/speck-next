import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

case, checkout = sys.argv[1:]
with tempfile.TemporaryDirectory() as directory:
    work = Path(directory)
    shutil.copy(Path(checkout) / "pack.py", work / "pack.py")
    def run(*arguments):
        return subprocess.run([sys.executable, "pack.py", *arguments], cwd=work,
                              capture_output=True, text=True, timeout=5)
    data = work / "items.json"
    if case == "packing":
        data.write_text(json.dumps([
            {"name": "Toothbrush", "packed": True},
            {"name": "Passport", "packed": False},
            {"name": "Charger", "packed": False},
        ]))
        before = run("list", "--pending")
        marked = run("mark", "1")
        after = run("list", "--pending")
        stored = json.loads(data.read_text())
        assert all(x.returncode == 0 for x in [before, marked, after])
        assert "1. Passport" in before.stdout, before.stdout
        assert "Passport" not in after.stdout, after.stdout
        assert "Charger" in after.stdout, after.stdout
        assert stored == [
            {"name": "Toothbrush", "packed": True},
            {"name": "Passport", "packed": True},
            {"name": "Charger", "packed": False},
        ], stored
    elif case == "integrity":
        damaged = b'[{"name":"Private medicine","packed":false},\n'
        data.write_bytes(damaged)
        result = run("add", "Charger")
        assert data.read_bytes() == damaged, "Damaged store was overwritten"
        assert result.returncode != 0, "Damaged store was accepted"
        assert "Added" not in result.stdout, result.stdout
        data.write_text('[{"name":"Passport","packed":false}]')
        assert run("add", "Charger").returncode == 0
        assert [x["name"] for x in json.loads(data.read_text())] == ["Passport", "Charger"]
    else:
        raise ValueError(case)
print(f"PASS: {case} complete job")
