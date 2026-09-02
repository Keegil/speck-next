#!/usr/bin/env python3
"""Separated team: prove selective repository semantics or inspect a governed host run."""
import copy, hashlib, importlib.util, json, os, pathlib, re, subprocess, sys, tempfile
from datetime import date, timedelta


RC1_STATUS = "**Upgrade status:** Unassessed under v6. Historical work keeps its original evidence and is not backfilled as role-shaped. Before the next substantial piece, Product, Business, Experience, and Engineering assess this product in four separate contexts. Reopen Shape only if that assessment finds a wrong promise."
SELECTIVE_STATUS = "**Upgrade status:** Unassessed under Speck Next 6.0.0-rc.2. Historical work keeps its original evidence and is not backfilled as role-shaped. Before the next substantial piece, separate Product, Business, Experience, and Engineering carriers assess the existing product and current map once. Business and Experience then define their observable call conditions, trusted evidence, expiry, and material changes. Reopen Shape only for a wrong promise and Map only for a wrong piece or order."
CONTRIBUTION_FIELDS = {"carrier", "evidence", "conclusion", "assumptions", "proposed_change", "earliest_run"}


def role_facts(**changes):
    facts = {
        "condition": False,
        "evidence_present": True,
        "expired": False,
        "material_change": False,
        "uncertain": False,
        "declared_effect": False,
    }
    facts.update(changes)
    return facts


def required_roles(case):
    required = {"Product", "Engineering"}
    for role in ("Business", "Experience"):
        facts = case["facts"][role]
        if (facts["condition"] or not facts["evidence_present"] or facts["expired"] or
                facts["material_change"] or facts["uncertain"] or facts["declared_effect"]):
            required.add(role)
    if case.get("false_inactive"):
        required.add(case["false_inactive"])
    return required


def make_role_case(name, business=None, experience=None, false_inactive=None, replacement=None):
    case = {
        "name": name,
        "facts": {
            "Business": business or role_facts(),
            "Experience": experience or role_facts(),
        },
        "false_inactive": false_inactive,
    }
    called = required_roles(case)
    carriers = {role: f"carrier-{role.lower()}" for role in called}
    contributions = {
        role: {
            "carrier": carriers[role],
            "evidence": f"direct-{role.lower()}-evidence",
            "conclusion": f"{role} conclusion",
            "assumptions": f"{role} assumptions",
            "proposed_change": f"{role} change",
            "earliest_run": f"{role} informative run",
        }
        for role in called
    }
    replacements = {}
    if replacement:
        original = carriers[replacement]
        new = f"replacement-{replacement.lower()}"
        contributions[replacement]["carrier"] = new
        carriers[replacement] = new
        replacements[replacement] = {
            "original": original,
            "replacement": new,
            "inherited_evidence": contributions[replacement]["evidence"],
            "inherited_prior_contribution": True,
        }
    record = {
        "calls": set(called),
        "inactive": {
            role: {"condition": f"{role} call condition", "evidence": f"current {role} evidence"}
            for role in ("Business", "Experience") if role not in called
        },
        "contributions": contributions,
        "run_exists": set(called),
        "returns": {role: f"return from {carriers[role]}" for role in called},
        "implementation_carrier": carriers["Engineering"],
        "replacements": replacements,
        "excluded": set(carriers.values()) | {r["original"] for r in replacements.values()},
        "testers": {"fresh-tester"},
        "judges": {"fresh-judge"},
    }
    if false_inactive:
        record["repair"] = {
            "stopped": True,
            "route": "piece setup",
            "missed_role_called": false_inactive,
            "product_resynthesized_before_resume": True,
            "invalidated": {"Built", "receipt", "tester verdict", "judgment"},
            "unrelated_evidence_kept": True,
            "changed_work": True,
            "new_built": True,
            "new_receipt": True,
            "mandatory_next_comparable_piece": True,
        }
    case["record"] = record
    return case


def validate_role_case(case):
    errors = []
    record = case["record"]
    required = required_roles(case)
    if record["calls"] != required:
        errors.append("calls are not exactly the roles required by current evidence")
    inactive_roles = {role for role in ("Business", "Experience") if role not in required}
    if set(record["inactive"]) != inactive_roles:
        errors.append("inactive rows do not match the roles kept out")
    if any(set(entry) != {"condition", "evidence"} or not all(entry.values())
           for entry in record["inactive"].values()):
        errors.append("an inactive row contains filler or lacks direct evidence")
    if set(record["contributions"]) != required:
        errors.append("active contributions do not match called roles")
    for contribution in record["contributions"].values():
        if set(contribution) != CONTRIBUTION_FIELDS or not all(contribution.values()):
            errors.append("an active contribution is incomplete")
    carriers = [entry["carrier"] for entry in record["contributions"].values()]
    if len(carriers) != len(set(carriers)):
        errors.append("called roles do not have distinct carriers")
    product = record["contributions"].get("Product", {}).get("carrier")
    engineering = record["contributions"].get("Engineering", {}).get("carrier")
    if not product or not engineering or product == engineering:
        errors.append("Product and Engineering are not separated")
    if record.get("implementation_carrier") != engineering or record.get("implementation_carrier") == product:
        errors.append("Engineering alone does not own implementation")
    overdue = record["run_exists"] & required - set(record["returns"])
    if overdue:
        errors.append("an informative return is overdue")
    for role, lineage in record.get("replacements", {}).items():
        contribution = record["contributions"].get(role, {})
        if (contribution.get("carrier") != lineage.get("replacement") or
                contribution.get("evidence") != lineage.get("inherited_evidence") or
                not lineage.get("inherited_prior_contribution")):
            errors.append("replacement did not inherit the evidence and contribution")
        if not {lineage.get("original"), lineage.get("replacement")} <= record["excluded"]:
            errors.append("original and replacement carriers are not both excluded")
    if set(carriers) - record["excluded"]:
        errors.append("a contributor is not excluded")
    if record["excluded"] & (record["testers"] | record["judges"]):
        errors.append("a contributor reappears in review")
    if case.get("false_inactive"):
        repair = record.get("repair", {})
        expected_invalid = {"Built", "receipt", "tester verdict", "judgment"}
        if not (repair.get("stopped") and repair.get("route") in {"Shape", "Map", "piece setup"} and
                repair.get("missed_role_called") == case["false_inactive"] and
                repair.get("product_resynthesized_before_resume") and
                repair.get("invalidated") == expected_invalid and
                repair.get("unrelated_evidence_kept") and repair.get("changed_work") and
                repair.get("new_built") and repair.get("new_receipt") and
                repair.get("mandatory_next_comparable_piece")):
            errors.append("false inactivity did not repair the current evidence chain")
    return errors


def mutate_calls(case, role):
    case["record"]["calls"] = set(case["record"]["calls"]) ^ {role}


def mutate_contribution(case, role):
    changed = dict(case["record"]["contributions"])
    changed.pop(role, None)
    case["record"]["contributions"] = changed


def run_role_controls():
    scenarios = []

    pe = make_role_case("Product + Engineering only")
    scenarios.append((pe, lambda c: mutate_calls(c, "Business")))

    business = make_role_case("Business joins", business=role_facts(condition=True))
    scenarios.append((business, lambda c: mutate_calls(c, "Business")))

    experience = make_role_case("Experience joins", experience=role_facts(material_change=True))
    scenarios.append((experience, lambda c: mutate_calls(c, "Experience")))

    all_four = make_role_case("all four join", business=role_facts(condition=True),
                              experience=role_facts(declared_effect=True))
    scenarios.append((all_four, lambda c: mutate_contribution(c, "Experience")))

    ambiguity = make_role_case("ambiguity calls the relevant role", business=role_facts(uncertain=True))
    scenarios.append((ambiguity, lambda c: c["facts"]["Business"].__setitem__("uncertain", False)))

    expiry = make_role_case("expired evidence calls the relevant role", experience=role_facts(expired=True))
    scenarios.append((expiry, lambda c: c["facts"]["Experience"].__setitem__("expired", False)))

    repair = make_role_case("false inactivity repairs the current piece", false_inactive="Experience")
    scenarios.append((repair, lambda c: c["record"]["repair"].__setitem__("product_resynthesized_before_resume", False)))

    overdue = make_role_case("informative return arrives before landing", business=role_facts(condition=True))
    scenarios.append((overdue, lambda c: c["record"].__setitem__(
        "returns", {k: v for k, v in c["record"]["returns"].items() if k != "Business"})))

    replacement = make_role_case("replacement inherits and both carriers stay excluded",
                                 business=role_facts(condition=True), replacement="Business")
    scenarios.append((replacement, lambda c: c["record"].__setitem__(
        "excluded", set(c["record"]["excluded"]) - {c["record"]["replacements"]["Business"]["original"]})))

    separation = make_role_case("Product and Engineering stay separated")
    scenarios.append((separation, lambda c: c["record"].__setitem__(
        "implementation_carrier", c["record"]["contributions"]["Product"]["carrier"])))

    good = True
    for case, mutate in scenarios:
        clean_errors = validate_role_case(case)
        clean_ok = not clean_errors
        print(f"  [{'ok' if clean_ok else 'RED'}] clean: {case['name']}")
        if clean_errors:
            print("    " + "; ".join(clean_errors))
        mutant = copy.deepcopy(case)
        mutate(mutant)
        mutant_errors = validate_role_case(mutant)
        mutant_ok = bool(mutant_errors)
        print(f"  [{'ok' if mutant_ok else 'RED'}] one-field mutant rejected: {case['name']}" +
              (f" ({mutant_errors[0]})" if mutant_errors else ""))
        good = good and clean_ok and mutant_ok
    print(f"  [measure] role-control subjects={len(scenarios) * 2} clean={len(scenarios)} mutants={len(scenarios)}")
    return good


def static_contract_homes(kernel):
    required = {
        "AGENTS.md": ["Product and Engineering are always called", "wrongly kept inactive", "replacement carrier"],
        ".claude/skills/shape-product/SKILL.md": ["observable conditions", "evidence expires"],
        ".claude/skills/shape-product/references/questions.md": ["what observable condition calls the role"],
        ".claude/skills/map-build/SKILL.md": ["first Map after Shape", "later re-map"],
        ".claude/skills/map-build/references/questions.md": ["Product and Engineering join every substantial piece"],
        "templates/product.md": ["Call when:", "Evidence expires:"],
        "templates/map.md": ["role calls:", "earliest informative runs:"],
        "templates/piece.md": ["## Role call decisions", "## Informative role returns", "## False inactive repair"],
        "templates/state.md": ["overdue informative returns", "false inactive call"],
        "CONTRACT.md": ["writes the version marker last", "replacement carrier inherits"],
        "README.md": ["right product-building views", "version-and-commit ends"],
        "capabilities.md": ["Selective product team", "live-host affordability"],
    }
    stale = {
        "AGENTS.md": ["Every substantial piece gets four product-building roles"],
        "templates/map.md": ["expected active roles:"],
        "templates/piece.md": ["## Pre-code product team"],
        "CONTRACT.md": ["four distinct pre-code carriers on substantial work"],
    }
    good = True
    for relative, needles in required.items():
        text = (kernel / relative).read_text()
        present = all(needle.lower() in text.lower() for needle in needles)
        print(f"  [{'ok' if present else 'RED'}] selective contract home: {relative}")
        good = good and present
    for relative, needles in stale.items():
        text = (kernel / relative).read_text()
        absent = all(needle.lower() not in text.lower() for needle in needles)
        print(f"  [{'ok' if absent else 'RED'}] obsolete universal rule absent: {relative}")
        good = good and absent
    version = json.loads((kernel / "package.json").read_text()).get("version")
    version_ok = version == "6.0.0-rc.2"
    print(f"  [{'ok' if version_ok else 'RED'}] package version is 6.0.0-rc.2")
    return good and version_ok


def init_repo(path):
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Piece 8 fixture"], cwd=path, check=True)


def write_file(root, relative, content):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def seed_upgrade_repo(root, version, commit, product=None, extra=None):
    init_repo(root)
    marker = {"name": "speck-next", "version": version, "commit": commit,
              "installedAt": "2026-01-02T03:04:05.000Z"}
    write_file(root, ".claude/speck-next.json", json.dumps(marker, indent=2) + "\n")
    if product is not None:
        write_file(root, "product.md", product)
    for relative, content in (extra or {}).items():
        write_file(root, relative, content)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "fixture baseline"], cwd=root, check=True)


def run_cli(kernel, command, target):
    return subprocess.run(["node", str(kernel / "bin/speck-next.js"), command, str(target)],
                          cwd=kernel, capture_output=True, text=True)


def surface_hash(root):
    digest = hashlib.sha256()
    for relative in ("AGENTS.md", "CLAUDE.md", ".claude", "templates", "map.md", "product.md"):
        path = root / relative
        if not path.exists():
            continue
        paths = sorted(p for p in path.rglob("*") if p.is_file()) if path.is_dir() else [path]
        for item in paths:
            digest.update(str(item.relative_to(root)).encode() + b"\0" + item.read_bytes() + b"\0")
    return digest.hexdigest()


def marker(root):
    return json.loads((root / ".claude/speck-next.json").read_text())


def upgrade_report_ok(run, prior_version, prior_commit, source_commit):
    output = run.stdout + run.stderr
    return (run.returncode == 0 and
            f"{prior_version} ({prior_commit}) -> 6.0.0-rc.2 ({source_commit})" in output and
            "Product team migration:" in output and
            "Working-tree changes across the complete installed surface plus product.md:" in output and
            "Complete installed-surface plus product.md diff" in output and
            "Next:" in output)


def run_migration_matrix(kernel):
    source_commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=kernel,
                                   check=True, capture_output=True, text=True).stdout.strip()
    results = []
    details = []

    with tempfile.TemporaryDirectory(prefix="speck-piece8-") as temporary:
        base = pathlib.Path(temporary)

        fresh = base / "fresh"
        fresh.mkdir()
        init_repo(fresh)
        run = run_cli(kernel, "install", fresh)
        installed = [p for p in fresh.rglob("*") if p.is_file() and ".git" not in p.parts]
        fresh_ok = (run.returncode == 0 and marker(fresh)["version"] == "6.0.0-rc.2" and
                    marker(fresh)["commit"] == source_commit and not (fresh / "product.md").exists() and
                    len(installed) <= 20 and sum(p.stat().st_size for p in installed) <= 100_000 and
                    "Installed paths:" in run.stdout and "Next:" in run.stdout)
        results.append(("fresh install reports its surface and leaves product.md missing", fresh_ok))

        v5 = base / "v5"
        v5.mkdir()
        v5_product = "# Existing product\n\nPromise and history stay here.\n"
        seed_upgrade_repo(v5, "5.4.1", "v5fixture", v5_product)
        first = run_cli(kernel, "upgrade", v5)
        first_hash = surface_hash(v5)
        second = run_cli(kernel, "upgrade", v5)
        second_hash = surface_hash(v5)
        migrated_v5 = (upgrade_report_ok(first, "5.4.1", "v5fixture", source_commit) and
                       (v5 / "product.md").read_text().startswith(v5_product) and
                       (v5 / "product.md").read_text().count(SELECTIVE_STATUS) == 1 and
                       marker(v5)["version"] == "6.0.0-rc.2" and first_hash == second_hash and
                       second.returncode == 0 and "6.0.0-rc.2" in second.stdout)
        results.append(("v5 migration is selective and the second upgrade is byte-stable", migrated_v5))
        details.append(f"v5_second_hash={second_hash}")

        rc1 = base / "rc1"
        rc1.mkdir()
        rc1_product = f"# Existing product\n\nHistorical sentence.\n\n## Product team\n\n{RC1_STATUS}\n\nTrailing history.\n"
        expected_rc2 = rc1_product.replace(RC1_STATUS, SELECTIVE_STATUS)
        seed_upgrade_repo(rc1, "6.0.0-rc.1", "rc1fixture", rc1_product)
        first = run_cli(kernel, "upgrade", rc1)
        first_hash = surface_hash(rc1)
        second = run_cli(kernel, "upgrade", rc1)
        second_hash = surface_hash(rc1)
        rc1_ok = (upgrade_report_ok(first, "6.0.0-rc.1", "rc1fixture", source_commit) and
                  (rc1 / "product.md").read_text() == expected_rc2 and RC1_STATUS not in expected_rc2 and
                  first_hash == second_hash and marker(rc1)["version"] == "6.0.0-rc.2")
        results.append(("exact generated rc.1 prose is replaced and retry is byte-stable", rc1_ok))
        details.append(f"rc1_second_hash={second_hash}")

        custom = base / "custom"
        custom.mkdir()
        custom_product = "# Custom product\n\n## Product team\n\nOwner-authored responsibilities.\n"
        seed_upgrade_repo(custom, "5.4.1", "customfixture", custom_product)
        first = run_cli(kernel, "upgrade", custom)
        first_hash = surface_hash(custom)
        second = run_cli(kernel, "upgrade", custom)
        custom_text = (custom / "product.md").read_text()
        custom_ok = (upgrade_report_ok(first, "5.4.1", "customfixture", source_commit) and
                     custom_text.startswith(custom_product) and
                     "## Speck Next product-team assessment" in custom_text and
                     custom_text.count(SELECTIVE_STATUS) == 1 and first_hash == surface_hash(custom) and
                     second.returncode == 0)
        results.append(("custom Product team prose is untouched beside one canonical status", custom_ok))

        missing = base / "missing"
        missing.mkdir()
        seed_upgrade_repo(missing, "5.4.1", "missingfixture")
        run = run_cli(kernel, "upgrade", missing)
        missing_ok = (upgrade_report_ok(run, "5.4.1", "missingfixture", source_commit) and
                      not (missing / "product.md").exists() and "product.md is missing" in run.stdout)
        results.append(("missing product.md stays missing", missing_ok))

        dirty = base / "dirty"
        dirty.mkdir()
        seed_upgrade_repo(dirty, "5.4.1", "dirtyfixture", "# Dirty product\n",
                          {"state.md": "baseline state\n", "work/inflight.md": "baseline work\n"})
        dirty_state = "baseline state\nowner's uncommitted state\n"
        dirty_work = "baseline work\nowner's uncommitted work\n"
        write_file(dirty, "state.md", dirty_state)
        write_file(dirty, "work/inflight.md", dirty_work)
        run = run_cli(kernel, "upgrade", dirty)
        dirty_ok = (upgrade_report_ok(run, "5.4.1", "dirtyfixture", source_commit) and
                    (dirty / "state.md").read_text() == dirty_state and
                    (dirty / "work/inflight.md").read_text() == dirty_work)
        results.append(("dirty unrelated work survives byte for byte", dirty_ok))

        retry = base / "retry"
        retry.mkdir()
        seed_upgrade_repo(retry, "5.4.1", "retryfixture")
        old_marker = (retry / ".claude/speck-next.json").read_bytes()
        (retry / "product.md").mkdir()
        failed = run_cli(kernel, "upgrade", retry)
        marker_held = failed.returncode != 0 and (retry / ".claude/speck-next.json").read_bytes() == old_marker
        (retry / "product.md").rmdir()
        write_file(retry, "product.md", "# Recovered product\n")
        retried = run_cli(kernel, "upgrade", retry)
        retry_ok = (marker_held and upgrade_report_ok(retried, "5.4.1", "retryfixture", source_commit) and
                    marker(retry)["version"] == "6.0.0-rc.2")
        results.append(("failed migration leaves the old marker and a retry completes", retry_ok))

        unknown = base / "unknown"
        unknown.mkdir()
        seed_upgrade_repo(unknown, "mystery", "unknownfixture", "# Unknown era\n")
        before = surface_hash(unknown)
        refused = run_cli(kernel, "upgrade", unknown)
        unknown_ok = (refused.returncode != 0 and "unknown version" in refused.stderr and
                      "Nothing was touched" in refused.stderr and before == surface_hash(unknown))
        results.append(("unknown marker version refuses before touching the repository", unknown_ok))

    good = True
    for label, passed in results:
        print(f"  [{'ok' if passed else 'RED'}] {label}")
        good = good and passed
    for detail in details:
        print(f"  [measure] {detail}")
    print(f"  [measure] migration subjects={len(results)}")
    return good


def piece8_controls(kernel_arg):
    kernel = pathlib.Path(kernel_arg).resolve()
    print("Piece 8 deterministic controls")
    homes_ok = static_contract_homes(kernel)
    roles_ok = run_role_controls()
    migration_ok = run_migration_matrix(kernel)
    print(f"Piece 8 controls: {'PASS' if homes_ok and roles_ok and migration_ok else 'FAIL'}")
    return 0 if homes_ok and roles_ok and migration_ok else 1


if len(sys.argv) >= 2 and sys.argv[1] == "--piece-8-controls":
    if len(sys.argv) != 3:
        print("usage: check.py --piece-8-controls KERNEL", file=sys.stderr)
        sys.exit(2)
    sys.exit(piece8_controls(sys.argv[2]))

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
        if "Pre-code product team" in text or "Active pre-code contributions" in text:
            records.append((rel, text))
note("KEY: one piece record carries the pre-code product team", len(records) == 1)
record_rel, record = records[0] if records else ("", "")

contribution_record = record
if "## Active pre-code contributions" in record:
    contribution_record = record.split("## Active pre-code contributions", 1)[1].split("**Product synthesis:**", 1)[0]
rows = {}
for role in ("Product", "Business", "Experience", "Engineering"):
    match = re.search(rf"^\|\s*{role}\s*\|(.*)$", contribution_record, re.M)
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

returns_heading = "## Informative role returns" if "## Informative role returns" in record else "## First real run returns"
returns = record.split(returns_heading, 1)[1].split("**Business ruling:**", 1)[0] if returns_heading in record else ""
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
