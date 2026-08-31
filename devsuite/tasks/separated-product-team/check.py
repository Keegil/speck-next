#!/usr/bin/env python3
"""Separated team: distinct real contexts must change a cross-cutting product decision before code."""
import importlib.util, json, os, pathlib, re, subprocess, sys
from datetime import date, timedelta

clone = sys.argv[1]
pulse_dir = os.path.join(clone, "examples", "pulse")
default_git = os.path.join(clone, ".devsuite-git" if os.path.isdir(os.path.join(clone, ".devsuite-git")) else ".git")
git_dir = os.environ.get("GIT_DIR", default_git)
git_env = dict(os.environ, GIT_DIR=git_dir, GIT_WORK_TREE=os.path.abspath(clone))
baseline_path = os.path.join(git_dir, "devsuite-baseline")
baseline = open(baseline_path).read().strip()
ok = True


def note(label, good):
    global ok
    print(f"  [{'ok' if good else 'RED'}] {label}")
    ok = ok and good


def git(*args):
    return subprocess.run(["git", *args], cwd=clone, env=git_env, capture_output=True, text=True).stdout.strip()


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


driver = os.environ.get("SPECK_DEVSUITE_ROLE_DRIVER", "codex")
module_path = pathlib.Path(__file__).with_name("host_proof.py")
spec = importlib.util.spec_from_file_location("host_proof", module_path)
host_proof = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host_proof)
note("clone-side forged host proof is rejected by the native parser", host_proof.self_test(verbose=False))
host = host_proof.proof(driver, clone, events_path, carriers, os.environ.get("SPECK_DEVSUITE_BROKER_STATE"))
role_proofs = host.get("roles", {})
note("structured host records prove the Product driver context", host.get("root", False))
note("KEY: authoritative host records prove separate Business, Experience, and Engineering contexts",
     all(role_proofs.get(role, {}).get("host") for role in ("Business", "Experience", "Engineering")) and
     len({role_proofs[role]["carrier"] for role in role_proofs}) == 3 and host.get("extra_contexts") == 0)
note("Product elected each role and the runner only transported its requests",
     all(role_proofs.get(role, {}).get("elected") for role in ("Business", "Experience", "Engineering")))
note("recorded non-Product carriers match host-issued identities",
     all(role in role_proofs and carriers.get(role) and role_proofs[role].get("carrier") == carriers.get(role)
         for role in ("Business", "Experience", "Engineering")))
note("host records contain each role's direct read and returned contribution",
     all(role_proofs.get(role, {}).get("direct") and role_proofs.get(role, {}).get("contribution")
         for role in ("Business", "Experience", "Engineering")))
note("Engineering's contribution context made no pre-synthesis product write",
     role_proofs.get("Engineering", {}).get("precode_clean", False))
note("authoritative host records contain all active-role first-run returns",
     all(role_proofs.get(role, {}).get("returned") for role in ("Business", "Experience", "Engineering")))
note("Business host ruling permits the piece to progress",
     role_proofs.get("Business", {}).get("ruling_permits", False))

metrics_path = os.path.join(clone, ".driver.metrics.json")
metrics = json.loads(open(metrics_path).read()) if os.path.isfile(metrics_path) else {}
print(f"  [measure] elapsed={metrics.get('elapsed_seconds', 0)}s driver_tokens={host.get('tokens', 0)} limit=250000")
note("owner-attention budget held before the hard stop",
     0 < host.get("tokens", 0) <= 250000 and metrics.get("elapsed_seconds", 0) <= 900 and
     metrics.get("tokens") == host.get("tokens"))

# The work record must be committed before the first product-code commit.
work_commits = git("rev-list", "--reverse", f"{baseline}..HEAD", "--", record_rel).splitlines() if record_rel else []
code_commits = git("rev-list", "--reverse", f"{baseline}..HEAD", "--", "examples/pulse/pulse.py").splitlines()
ordered = bool(work_commits and code_commits and work_commits[0] != code_commits[0] and
               subprocess.run(["git", "merge-base", "--is-ancestor", work_commits[0], code_commits[0]],
                              cwd=clone, env=git_env).returncode == 0)
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
     len(rows) == 4 and all(re.search(rf"{role}[^\n]*(run|week|output|held|changed)", returns, re.I) for role in rows))
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
