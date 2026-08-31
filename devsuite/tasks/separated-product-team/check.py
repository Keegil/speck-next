#!/usr/bin/env python3
"""Separated team: distinct real contexts must change a cross-cutting product decision before code."""
import json, os, re, subprocess, sys
from datetime import date, timedelta

clone = sys.argv[1]
pulse_dir = os.path.join(clone, "examples", "pulse")
baseline_path = os.path.join(clone, ".git", "devsuite-baseline")
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


def tool_calls(value):
    found = []
    if isinstance(value, dict):
        name = str(value.get("name") or value.get("tool_name") or "")
        low = name.lower()
        if any(k in low for k in ("spawn_agent", "followup_task")) or low in ("agent", "task"):
            found.append((str(value.get("id") or value.get("call_id") or value.get("tool_use_id") or id(value)), json.dumps(value)))
        for child in value.values():
            found.extend(tool_calls(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(tool_calls(child))
    return found


calls = []
for event in events:
    calls.extend(tool_calls(event))
precode = {}
for role in ("Business", "Experience", "Engineering"):
    precode[role] = {call_id for call_id, blob in calls if role.lower() in blob.lower() and "spawn" in blob.lower() or role.lower() in blob.lower() and '"name": "agent"' in blob.lower()}
note("KEY: structured host events show separate Business, Experience, and Engineering dispatches",
     all(precode.values()) and len(set().union(*precode.values())) >= 3)
note("structured host events include the Product driver context",
     any("thread.started" in json.dumps(e).lower() or "session_id" in json.dumps(e).lower() for e in events))
events_text = json.dumps(events).lower()
note("recorded non-Product carriers match host-issued event identities",
     all(carriers.get(role, "").lower() in events_text for role in ("Business", "Experience", "Engineering")))

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
