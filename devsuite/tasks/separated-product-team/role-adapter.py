#!/usr/bin/env python3
"""Launch one Product-chosen role context and preserve host-issued identity evidence."""
import hashlib, json, os, pathlib, subprocess, sys


def die(message):
    raise SystemExit(f"role adapter: {message}")


if len(sys.argv) != 3:
    die("usage: role-adapter.py ROLE BRIEF_FILE")
role = sys.argv[1]
if role not in ("Business", "Experience", "Engineering"):
    die("ROLE must be Business, Experience, or Engineering")

root = pathlib.Path(os.environ.get("GIT_WORK_TREE", os.getcwd())).resolve()
run_dir = root / ".devsuite-role-runs"
run_dir.mkdir(exist_ok=True)
brief_path = pathlib.Path(sys.argv[2]).resolve()
if run_dir not in brief_path.parents:
    die("brief must live in the clone's task-private .devsuite-role-runs directory")
brief = brief_path.read_text()
if len(brief.strip()) < 80:
    die("brief is too thin to direct an independent contribution")

driver = os.environ.get("SPECK_DEVSUITE_ROLE_DRIVER")
if driver not in ("codex", "claude"):
    die("SPECK_DEVSUITE_ROLE_DRIVER must be codex or claude")

attempt = 1 + len(list(run_dir.glob(f"{role.lower()}-*.events.jsonl")))
stem = f"{role.lower()}-{attempt}"
events_path = run_dir / f"{stem}.events.jsonl"
stderr_path = run_dir / f"{stem}.stderr.log"
contribution_path = run_dir / f"{stem}.contribution.md"
prompt = f"""You are the separate {role} product-building role. You did not author the request or the product.
Read the named primary evidence directly from disk. Do not edit any file and do not act as another role.
Return a compact contribution with a dedicated `Role: {role}` line and name: direct evidence consulted, conclusion,
assumptions, proposed product change, material consequence, and the earliest run that could disprove it.

Product's evidence brief:
{brief}
"""

with events_path.open("w") as events, stderr_path.open("w") as stderr:
    if driver == "codex":
        command = ["codex", "exec", "--json", "--sandbox", "read-only", "--skip-git-repo-check", "-C", str(root),
                   "-o", str(contribution_path), prompt]
    else:
        command = ["claude", "-p", prompt, "--allowedTools", "Bash,Read,Glob,Grep",
                   "--output-format", "stream-json", "--verbose"]
    result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=events, stderr=stderr, text=True)
if result.returncode:
    die(f"{driver} child exited {result.returncode}; see {stderr_path}")

parsed = []
for line in events_path.read_text(errors="ignore").splitlines():
    try:
        parsed.append(json.loads(line))
    except json.JSONDecodeError:
        pass

session_id = None
contribution = contribution_path.read_text(errors="ignore") if contribution_path.exists() else ""
if driver == "codex":
    for event in parsed:
        if event.get("type") == "thread.started" and event.get("thread_id"):
            session_id = event["thread_id"]
            break
else:
    for event in parsed:
        if event.get("session_id"):
            session_id = event["session_id"]
            break
    if not contribution:
        for event in reversed(parsed):
            if event.get("type") == "result" and isinstance(event.get("result"), str):
                contribution = event["result"]
                break
        if contribution:
            contribution_path.write_text(contribution)

if not session_id:
    die("child host emitted no thread/session id")
if not any(line.strip() == f"Role: {role}" for line in contribution.splitlines()):
    die("child emitted no role contribution")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


entry = {
    "role": role,
    "driver": driver,
    "session_id": session_id,
    "brief": str(brief_path.relative_to(root)),
    "brief_sha256": sha(brief_path),
    "events": str(events_path.relative_to(root)),
    "events_sha256": sha(events_path),
    "contribution": str(contribution_path.relative_to(root)),
    "contribution_sha256": sha(contribution_path),
}
with (run_dir / "manifest.jsonl").open("a") as manifest:
    manifest.write(json.dumps(entry, sort_keys=True) + "\n")
print(json.dumps(entry, sort_keys=True))
