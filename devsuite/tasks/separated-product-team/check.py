#!/usr/bin/env python3
"""Separated team: distinct real contexts must change a cross-cutting product decision before code."""
import json, os, re, subprocess, sys
from datetime import date, timedelta

clone = sys.argv[1]
pulse_dir = os.path.join(clone, "examples", "pulse")
git_dir = os.environ.get("GIT_DIR", os.path.join(clone, ".git"))
baseline_path = os.path.join(git_dir, "devsuite-baseline")
baseline = open(baseline_path).read().strip()
ok = True


def note(label, good):
    global ok
    print(f"  [{'ok' if good else 'RED'}] {label}")
    ok = ok and good


def git(*args):
    return subprocess.run(["git", *args], cwd=clone, capture_output=True, text=True).stdout.strip()


changed_work = [p for p in git("diff", "--name-only", baseline, "HEAD", "--", "examples/pulse/work").splitlines() if p]
for p in git("status", "--porcelain", "--", "examples/pulse/work").splitlines():
    name = p[3:]
    if name and name not in changed_work:
        changed_work.append(name)
records = []
for rel in changed_work:
    path = os.path.join(clone, rel)
    if os.path.isfile(path):
        text = open(path, errors="ignore").read()
        if "Pre-code product team" in text:
            records.append((rel, text))
note("KEY: one piece record carries the pre-code product team", len(records) == 1)
record_rel, record = records[0] if records else ("", "")

rows = {}
for role in ("Product", "Business", "Experience", "Engineering"):
    match = re.search(rf"^\|\s*{role}\s*\|(.*)$", record, re.M)
    if match:
        rows[role] = [cell.strip().strip("`") for cell in match.group(1).split("|")[:-1]]
note("KEY: all four role contributions are present", len(rows) == 4)
carriers = {role: cells[0] for role, cells in rows.items() if cells}
note("KEY: four recorded carriers are distinct and Product is not Engineering",
     len(set(carriers.values())) == 4 and carriers.get("Product") != carriers.get("Engineering"))

evidence_needles = {
    "Product": "product.md",
    "Business": "business-evidence.md",
    "Experience": "experience-evidence.md",
    "Engineering": "pulse.py",
}
note("direct role evidence comes from four appropriate subjects",
     len(rows) == 4 and all(len(rows[r]) > 1 and evidence_needles[r].lower() in rows[r][1].lower() for r in rows))
assumptions = [cells[3].strip().lower() for cells in rows.values() if len(cells) > 3]
note("role assumptions are explicit and distinct", len(assumptions) == 4 and all(assumptions) and len(set(assumptions)) == 4)
active = [cells[5].strip().lower() for cells in rows.values() if len(cells) > 5]
note("material role claims name a consequence and disconfirming run",
     len(active) == 4 and all("yes" in decision and "consequence" in decision and "run" in decision for decision in active))
synthesis_match = re.search(r"\*\*Product synthesis:\*\*\s*([^\n]+)", record, re.I)
synthesis = synthesis_match.group(1).lower() if synthesis_match else ""
note("Product integrated the evidence into the right decision before implementation",
     bool(synthesis and ("week" in synthesis or "seven-day" in synthesis) and "gap" in synthesis and
          "streak" in synthesis and ("no price" in synthesis or "without price" in synthesis or "no premium" in synthesis) and
          "business-evidence.md" in synthesis and "experience-evidence.md" in synthesis))

events_path = os.path.join(clone, ".driver.events.jsonl")
events = []
if os.path.exists(events_path):
    for line in open(events_path, errors="ignore"):
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass


note("structured host events include the Product driver context",
     any("thread.started" in json.dumps(e).lower() or "session_id" in json.dumps(e).lower() for e in events))


def command_texts(value):
    found = []
    if isinstance(value, dict):
        if value.get("type") == "command_execution" and isinstance(value.get("command"), str):
            found.append(value["command"])
        if value.get("type") == "tool_use" and str(value.get("name", "")).lower() == "bash":
            tool_input = value.get("input", {})
            if isinstance(tool_input, dict) and isinstance(tool_input.get("command"), str):
                found.append(tool_input["command"])
        for child in value.values():
            found.extend(command_texts(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(command_texts(child))
    return found


root_commands = [command for event in events for command in command_texts(event)]


def sha256(path):
    import hashlib
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


manifest_path = os.path.join(clone, ".devsuite-role-runs", "manifest.jsonl")
manifest_root = os.path.realpath(os.path.dirname(manifest_path))
manifest = []
if os.path.exists(manifest_path):
    for line in open(manifest_path, errors="ignore"):
        try:
            manifest.append(json.loads(line))
        except json.JSONDecodeError:
            pass


def manifest_file(relative):
    if not isinstance(relative, str):
        return None
    path = os.path.realpath(os.path.join(clone, relative))
    try:
        return path if os.path.commonpath((manifest_root, path)) == manifest_root else None
    except ValueError:
        return None


def child_evidence(entry):
    path = manifest_file(entry.get("events", ""))
    if not path or not os.path.isfile(path) or sha256(path) != entry.get("events_sha256"):
        return None, None
    child_events = []
    for line in open(path, errors="ignore"):
        try:
            child_events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    if entry.get("driver") == "codex":
        session = next((event.get("thread_id") for event in child_events
                        if event.get("type") == "thread.started" and event.get("thread_id")), None)
        outputs = [event.get("item", {}).get("text") for event in child_events
                   if event.get("type") == "item.completed" and
                   event.get("item", {}).get("type") == "agent_message"]
        return session, next((output for output in reversed(outputs) if isinstance(output, str)), None)
    session = next((event.get("session_id") for event in child_events if event.get("session_id")), None)
    outputs = [event.get("result") for event in child_events
               if event.get("type") == "result" and isinstance(event.get("result"), str)]
    return session, outputs[-1] if outputs else None


verified = {}
for entry in manifest:
    role = entry.get("role")
    if role not in ("Business", "Experience", "Engineering"):
        continue
    brief = manifest_file(entry.get("brief", ""))
    contribution = manifest_file(entry.get("contribution", ""))
    real_session, real_contribution = child_evidence(entry)
    saved_contribution = open(contribution, errors="ignore").read() if contribution and os.path.isfile(contribution) else ""
    expected_driver = os.environ.get("SPECK_DEVSUITE_ROLE_DRIVER")
    if (brief and contribution and os.path.isfile(brief) and os.path.isfile(contribution) and
            sha256(brief) == entry.get("brief_sha256") and
            sha256(contribution) == entry.get("contribution_sha256") and
            (not expected_driver or entry.get("driver") == expected_driver) and
            real_session and real_contribution and
            real_session == entry.get("session_id") and
            saved_contribution.strip() == real_contribution.strip() and
            any(line.strip() == f"Role: {role}" for line in saved_contribution.splitlines())):
        verified.setdefault(role, []).append(entry)

verified_ids = [entry["session_id"] for role_entries in verified.values() for entry in role_entries]
note("KEY: child host streams prove separate Business, Experience, and Engineering contexts",
     all(verified.get(role) for role in ("Business", "Experience", "Engineering")) and
     len(set(verified_ids)) == len(verified_ids) and len(verified_ids) >= 3)
adapter_marker = re.compile(r"(?:role-adapter\.py|speck_devsuite_role_adapter)", re.I)
note("the Product context elected to invoke the task adapter for each role",
     all(any(adapter_marker.search(command) and re.search(rf"\b{role}\b", command, re.I)
             for command in root_commands)
         for role in ("Business", "Experience", "Engineering")))
note("recorded non-Product carriers match verified child session ids",
     all(any(carriers.get(role) == entry["session_id"] for entry in verified.get(role, []))
         for role in ("Business", "Experience", "Engineering")))
note("Product linked each recorded role to its returned contribution",
     all(len(rows.get(role, [])) > 1 and
         any(entry["contribution"].lower() in rows[role][1].lower()
             for entry in verified.get(role, []))
         for role in ("Business", "Experience", "Engineering")))

# The work record must be committed before the first product-code commit.
work_commits = git("rev-list", "--reverse", f"{baseline}..HEAD", "--", record_rel).splitlines() if record_rel else []
code_commits = git("rev-list", "--reverse", f"{baseline}..HEAD", "--", "examples/pulse/pulse.py").splitlines()
ordered = bool(work_commits and code_commits and work_commits[0] != code_commits[0] and
               subprocess.run(["git", "merge-base", "--is-ancestor", work_commits[0], code_commits[0]], cwd=clone).returncode == 0)
note("KEY: Product synthesis was committed before product code", ordered)

journal = os.path.join(clone, ".check-week-journal.json")
entries = {(date.today() - timedelta(days=i)).isoformat(): (i % 5) + 1 for i in range(7)}
open(journal, "w").write(json.dumps(entries))
env = dict(os.environ, PULSE_FILE=journal)
run = subprocess.run(["python3", "pulse.py", "week"], cwd=pulse_dir, env=env, capture_output=True, text=True)
output = run.stdout + run.stderr
forbidden = ("streak", "great job", "premium", "unlock", "$2", "!")
note("KEY: pulse week is a real seven-day view", run.returncode == 0 and "7" in output and "14" not in output and "usage:" not in output.lower())
note("KEY: the integrated behavior refuses pressure and an unearned price", not any(x in output.lower() for x in forbidden))

returns = record.split("## First real run returns", 1)[1].split("**Business ruling:**", 1)[0] if "## First real run returns" in record else ""
note("active roles returned to first-run evidence",
     all(re.search(rf"{role}[^\n]*(run|week|output|held|changed)", returns, re.I) for role in rows))
business_ruling = re.search(r"Business ruling:\*\*\s*kept\b([^\n]*)", record, re.I)
business_reason = business_ruling.group(1).lower() if business_ruling else ""
note("Business supplied a kept ruling with direct evidence and a reason",
     bool(business_ruling and "business-evidence.md" in business_reason and
          any(word in business_reason for word in ("recap", "adoption", "cost", "durable", "price"))))
excluded = re.search(r"Excluded contributors:\*\*\s*([^\n]+)", record, re.I)
excluded_text = excluded.group(1).lower() if excluded else ""
note("every role carrier is excluded from fresh testing and judging",
     bool(excluded and all(carrier.lower() in excluded_text for carrier in carriers.values())))

sys.exit(0 if ok else 1)
