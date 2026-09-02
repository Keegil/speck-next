#!/usr/bin/env python3
"""Separated team: prove selective repository semantics or inspect a governed host run."""
import copy, hashlib, importlib.util, json, os, pathlib, re, shutil, subprocess, sys, tempfile
from datetime import date, timedelta


RC1_STATUS = "**Upgrade status:** Unassessed under v6. Historical work keeps its original evidence and is not backfilled as role-shaped. Before the next substantial piece, Product, Business, Experience, and Engineering assess this product in four separate contexts. Reopen Shape only if that assessment finds a wrong promise."
REJECTED_RC2_STATUS = "**Upgrade status:** Unassessed under Speck Next 6.0.0-rc.2. Historical work keeps its original evidence and is not backfilled as role-shaped. Before the next substantial piece, separate Product, Business, Experience, and Engineering carriers assess the existing product and current map once. Business and Experience then define their observable call conditions, trusted evidence, expiry, and material changes. Reopen Shape only for a wrong promise and Map only for a wrong piece or order."
ASSESSMENT_HEADING = "## Speck Next upgrade assessment"
ASSESSMENT_RECORD = "work/product-team-assessment.md"
ASSESSMENT_RECORD_LINE = f"**Record:** `{ASSESSMENT_RECORD}`"
ASSESSMENT_PENDING = "**Speck Next upgrade assessment:** pending"
ASSESSMENT_BLOCK = f"{ASSESSMENT_HEADING}\n\n{ASSESSMENT_PENDING}\n{ASSESSMENT_RECORD_LINE}\n"
ASSESSMENT_COMPLETE_SHAPE = "**Speck Next upgrade assessment:** complete — Shape reopened"
ASSESSMENT_COMPLETE_MAP = "**Speck Next upgrade assessment:** complete — Map reopened"
NEXT_MISSING_CHANGED = "Next: review the reported paths and complete diff, commit the upgrade, then open Shape to create and ratify product.md before Map or any substantial work."
NEXT_MISSING_CLEAN = "Next: there are no upgrade changes to commit; open Shape to create and ratify product.md before Map or any substantial work."
NEXT_PENDING_CHANGED = f"Next: review the reported paths and complete diff, commit the upgrade, then complete {ASSESSMENT_RECORD} by following “Finish an upgrade” in AGENTS.md."
NEXT_PENDING_CLEAN = f"Next: there are no upgrade changes to commit; complete {ASSESSMENT_RECORD} by following “Finish an upgrade” in AGENTS.md."
NEXT_CURRENT_CHANGED = "Next: review the reported paths and complete diff, commit the upgrade, then resume current work from state.md."
NEXT_CURRENT_CLEAN = "Next: there are no upgrade changes to commit; resume current work from state.md."
CONTRIBUTION_FIELDS = {"carrier", "evidence", "conclusion", "assumptions", "proposed_change", "earliest_run"}
ASSESSMENT_FIELDS = {"carrier", "evidence", "conclusion", "assumptions", "proposed_change", "active_decision"}


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
    if case.get("handled_miss"):
        required.add(case["handled_miss"])
    return required


def make_role_case(name, business=None, experience=None, false_inactive=None, replacement=None,
                   handled_miss=None, handled_repeat=False):
    case = {
        "name": name,
        "facts": {
            "Business": business or role_facts(),
            "Experience": experience or role_facts(),
        },
        "false_inactive": false_inactive,
        "handled_miss": handled_miss,
        "handled_repeat": handled_repeat,
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
        "landing": True,
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
    if handled_miss:
        record["handled_miss"] = {
            "role": handled_miss,
            "prior_concern_marked_handled": True,
            "consequential_miss": True,
            "mandatory_next_comparable_piece": True,
            "key_decisions": True,
            "informative_runs": True,
            "repeat": handled_repeat,
            "mandatory_through_milestone": handled_repeat,
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
    if record.get("landing"):
        if required - record["run_exists"]:
            errors.append("a named informative run has not happened before landing")
        if required - set(record["returns"]):
            errors.append("an informative return is overdue before landing")
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
    if case.get("handled_miss"):
        escalation = record.get("handled_miss", {})
        if not (escalation.get("role") == case["handled_miss"] and
                escalation.get("prior_concern_marked_handled") and
                escalation.get("consequential_miss") and
                escalation.get("mandatory_next_comparable_piece") and
                escalation.get("key_decisions") and escalation.get("informative_runs") and
                escalation.get("repeat") == case["handled_repeat"] and
                escalation.get("mandatory_through_milestone") == case["handled_repeat"]):
            errors.append("a handled-concern miss did not escalate the role for long enough")
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

    run_due = make_role_case("named informative run happens before landing", business=role_facts(condition=True))
    scenarios.append((run_due, lambda c: c["record"].__setitem__(
        "run_exists", set(c["record"]["run_exists"]) - {"Business"})))

    replacement = make_role_case("replacement inherits and both carriers stay excluded",
                                 business=role_facts(condition=True), replacement="Business")
    scenarios.append((replacement, lambda c: c["record"].__setitem__(
        "excluded", set(c["record"]["excluded"]) - {c["record"]["replacements"]["Business"]["original"]})))

    separation = make_role_case("Product and Engineering stay separated")
    scenarios.append((separation, lambda c: c["record"].__setitem__(
        "implementation_carrier", c["record"]["contributions"]["Product"]["carrier"])))

    handled = make_role_case("handled miss staffs the next comparable piece", handled_miss="Business")
    scenarios.append((handled, lambda c: mutate_calls(c, "Business")))

    repeated = make_role_case("repeated handled miss stays through the milestone",
                              handled_miss="Experience", handled_repeat=True)
    scenarios.append((repeated, lambda c: c["record"]["handled_miss"].__setitem__(
        "mandatory_through_milestone", False)))

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


def make_assessment_case(route):
    roles = ("Product", "Business", "Experience", "Engineering")
    return {
        "inputs": {"product": "product.md", "map": "map.md", "state_live_piece": "Piece alpha"},
        "contributions": {
            role: {
                "carrier": f"assessment-{role.lower()}",
                "evidence": f"direct {role.lower()} evidence",
                "conclusion": f"{role} conclusion",
                "assumptions": f"{role} assumptions",
                "proposed_change": f"{role} proposed change",
                "active_decision": f"{role} active decision",
            }
            for role in roles
        },
        "product_synthesis": "One integrated decision with dissent preserved.",
        "routes": [route],
    }


def validate_assessment_case(case):
    errors = []
    roles = {"Product", "Business", "Experience", "Engineering"}
    if set(case.get("inputs", {})) != {"product", "map", "state_live_piece"} or not all(case["inputs"].values()):
        errors.append("the existing product, current map, state, and live piece were not all read")
    if set(case.get("contributions", {})) != roles:
        errors.append("the assessment does not contain exactly four role contributions")
    for contribution in case.get("contributions", {}).values():
        if set(contribution) != ASSESSMENT_FIELDS or not all(contribution.values()):
            errors.append("an assessment contribution is incomplete")
    carriers = [entry.get("carrier") for entry in case.get("contributions", {}).values()]
    if len(carriers) != len(set(carriers)):
        errors.append("assessment carriers are not distinct")
    if not case.get("product_synthesis"):
        errors.append("Product synthesis is missing")
    routes = case.get("routes", [])
    allowed = {"Shape reopened", "Map reopened", "resumed Piece alpha from state.md"}
    if len(routes) != 1 or routes[0] not in allowed:
        errors.append("the assessment must select exactly one allowed route")
    return errors


def run_assessment_controls():
    clean = [
        ("wrong promise reopens Shape", make_assessment_case("Shape reopened")),
        ("wrong piece or order reopens Map", make_assessment_case("Map reopened")),
        ("no reopen resumes the existing live piece", make_assessment_case("resumed Piece alpha from state.md")),
    ]
    mutants = []
    missing = copy.deepcopy(clean[0][1])
    missing["contributions"].pop("Business")
    mutants.append(("missing contribution", missing))
    duplicate = copy.deepcopy(clean[1][1])
    duplicate["contributions"]["Business"]["carrier"] = duplicate["contributions"]["Product"]["carrier"]
    mutants.append(("duplicate carrier", duplicate))
    no_synthesis = copy.deepcopy(clean[2][1])
    no_synthesis["product_synthesis"] = ""
    mutants.append(("missing Product synthesis", no_synthesis))
    no_route = copy.deepcopy(clean[2][1])
    no_route["routes"] = []
    mutants.append(("zero routes", no_route))
    two_routes = copy.deepcopy(clean[2][1])
    two_routes["routes"] = ["Shape reopened", "Map reopened"]
    mutants.append(("two routes", two_routes))

    good = True
    for label, case in clean:
        errors = validate_assessment_case(case)
        passed = not errors
        print(f"  [{'ok' if passed else 'RED'}] assessment clean: {label}")
        good = good and passed
    for label, case in mutants:
        errors = validate_assessment_case(case)
        passed = bool(errors)
        print(f"  [{'ok' if passed else 'RED'}] assessment mutant rejected: {label}" +
              (f" ({errors[0]})" if errors else ""))
        good = good and passed
    print(f"  [measure] assessment-control subjects={len(clean) + len(mutants)} clean={len(clean)} mutants={len(mutants)}")
    return good


def static_contract_homes(kernel):
    required = {
        "AGENTS.md": ["Product and Engineering are always called", "named run and its return",
                      "wrongly kept inactive", "concern was handled", "replacement carrier",
                      "Finish an upgrade", ASSESSMENT_RECORD, "complete — Shape reopened",
                      "complete — Map reopened", "from state.md", "upgradeAssessmentRecord",
                      "does not guess", "before replacing any repository byte",
                      "assessment refusal"],
        ".claude/skills/shape-product/SKILL.md": ["observable conditions", "evidence expires"],
        ".claude/skills/shape-product/references/questions.md": ["what observable condition calls the role"],
        ".claude/skills/map-build/SKILL.md": ["first Map after Shape", "later re-map"],
        ".claude/skills/map-build/references/questions.md": ["Product and Engineering join every substantial piece"],
        "templates/product.md": ["Call when:", "Evidence expires:"],
        "templates/map.md": ["role calls:", "earliest informative runs:"],
        "templates/piece.md": ["## Role call decisions", "## Informative role returns",
                               "## False inactive repair", "## Handled-concern miss escalation"],
        "templates/state.md": ["overdue informative returns", "false inactive call"],
        "CONTRACT.md": ["On a later re-map, Product contributes", "named run and its return",
                        "writes the version marker last", "replacement carrier inherits",
                        ASSESSMENT_RECORD, "method-surface digests", "Every fixed marker carries",
                        "before changing any repository byte", "complete non-Git path kinds and bytes"],
        "README.md": ["right product-building views", ASSESSMENT_RECORD,
                      "source checkout separately", "fieldless current rc.2 marker is unknown",
                      "before any repository byte changes"],
        "capabilities.md": ["Selective product team", "live-host affordability",
                            "assessment-control subjects", "complete-target snapshot"],
    }
    stale = {
        "AGENTS.md": ["Every substantial piece gets four product-building roles"],
        "templates/map.md": ["expected active roles:"],
        "templates/piece.md": ["## Pre-code product team"],
        "CONTRACT.md": ["four distinct pre-code carriers on substantial work",
                        "On later re-maps and substantial pieces, Product and Engineering always contribute"],
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


def commit_fixture(root, message):
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", message], cwd=root, check=True)


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


def repository_snapshot(root):
    """Every non-Git path kind and byte, including empty directories and links."""
    entries = []
    for item in sorted(root.rglob("*"), key=lambda candidate: candidate.relative_to(root).as_posix()):
        relative = item.relative_to(root)
        if ".git" in relative.parts:
            continue
        info = item.lstat()
        if item.is_symlink():
            kind, payload = "link", os.readlink(item).encode()
        elif item.is_dir():
            kind, payload = "directory", b""
        elif item.is_file():
            kind, payload = "file", item.read_bytes()
        else:
            kind, payload = f"other:{info.st_mode}", b""
        entries.append((relative.as_posix(), kind, payload))
    return tuple(entries)


def porcelain_v1_z(root):
    return subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=root, check=True, capture_output=True,
    ).stdout


def refusal_baseline(root):
    return {
        "marker": (root / ".claude/speck-next.json").read_bytes(),
        "tree": repository_snapshot(root),
        "porcelain": porcelain_v1_z(root),
    }


def refusal_unchanged(root, before, run):
    return (
        run.returncode != 0 and
        "Nothing in the repository changed." in run.stderr and
        "run the upgrade again" in run.stderr and
        "resume" not in (run.stdout + run.stderr).lower() and
        (root / ".claude/speck-next.json").read_bytes() == before["marker"] and
        repository_snapshot(root) == before["tree"] and
        porcelain_v1_z(root) == before["porcelain"]
    )


def method_surface_sha256(root):
    digest = hashlib.sha256()
    files = []
    for relative in ("AGENTS.md", "CLAUDE.md", ".claude/skills", "templates"):
        path = root / relative
        paths = sorted(p for p in path.rglob("*") if p.is_file()) if path.is_dir() else [path]
        files.extend(paths)
    for item in sorted(files, key=lambda candidate: candidate.relative_to(root).as_posix()):
        digest.update(item.relative_to(root).as_posix().encode() + b"\0" + item.read_bytes() + b"\0")
    return digest.hexdigest()


def marker(root):
    return json.loads((root / ".claude/speck-next.json").read_text())


def provenance(version, source_checkout, surface_digest=None):
    surface = f"sha256:{surface_digest}" if surface_digest else "not recorded"
    return f"{version} (source checkout {source_checkout or 'not recorded'}; method surface {surface})"


def marker_ok(root, source_checkout, surface_digest, assessment_record=None):
    actual = marker(root)
    expected = {
        "name": "speck-next",
        "version": "6.0.0-rc.2",
        "sourceCheckout": source_checkout,
        "methodSurfaceSha256": surface_digest,
        "upgradeAssessmentRecord": assessment_record,
    }
    return (all(key in actual and actual[key] == value for key, value in expected.items()) and
            "commit" not in actual)


def upgrade_report_ok(run, prior_version, prior_checkout, source_checkout, surface_digest,
                      expected_next, prior_digest=None):
    output = run.stdout + run.stderr
    next_lines = [line for line in run.stdout.splitlines() if line.startswith("Next:")]
    return (run.returncode == 0 and
            f"{provenance(prior_version, prior_checkout, prior_digest)} -> {provenance('6.0.0-rc.2', source_checkout, surface_digest)}" in output and
            "Product team migration:" in output and
            "Working-tree changes across the complete installed surface plus product.md:" in output and
            "Complete installed-surface plus product.md diff" in output and
            next_lines == [expected_next] and run.stdout.rstrip().endswith(expected_next))


def run_migration_matrix(kernel):
    source_checkout = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=kernel,
                                     check=True, capture_output=True, text=True).stdout.strip()
    surface_digest = method_surface_sha256(kernel)
    results = []
    details = []

    with tempfile.TemporaryDirectory(prefix="speck-piece8-") as temporary:
        base = pathlib.Path(temporary)

        def expected_product(original):
            return original + ("\n" if original.endswith("\n") else "\n\n") + ASSESSMENT_BLOCK

        def assessment_record(route):
            return ("# Product-team assessment\n\n"
                    "**Product read:** product.md\n"
                    "**Map read:** map.md\n"
                    "**State and live piece read:** state.md · Piece alpha\n\n"
                    "## Product\nCarrier: assessment-product\nDirect evidence: product\nConclusion: product\nAssumptions: product\nProposed change: product\nActive decision: product\n\n"
                    "## Business\nCarrier: assessment-business\nDirect evidence: business\nConclusion: business\nAssumptions: business\nProposed change: business\nActive decision: business\n\n"
                    "## Experience\nCarrier: assessment-experience\nDirect evidence: experience\nConclusion: experience\nAssumptions: experience\nProposed change: experience\nActive decision: experience\n\n"
                    "## Engineering\nCarrier: assessment-engineering\nDirect evidence: engineering\nConclusion: engineering\nAssumptions: engineering\nProposed change: engineering\nActive decision: engineering\n\n"
                    "## Product synthesis\nOne integrated decision.\n\n"
                    f"## Route\n{route}\n")

        def assessment_record_ok(content, route):
            roles = ("Product", "Business", "Experience", "Engineering")
            carriers = re.findall(r"^Carrier: (.+)$", content, re.MULTILINE)
            return (
                all(content.count(f"## {role}\n") == 1 for role in roles) and
                len(carriers) == len(roles) == len(set(carriers)) and
                content.count("## Product synthesis\n") == 1 and
                content.count("## Route\n") == 1 and
                content.endswith(f"## Route\n{route}\n")
            )

        def complete_pending(repo, status, route, state, retained_history=""):
            product = (repo / "product.md").read_text().replace(ASSESSMENT_PENDING, status, 1)
            if retained_history:
                product += "\n" + retained_history
            write_file(repo, "product.md", product)
            write_file(repo, ASSESSMENT_RECORD, assessment_record(route))
            write_file(repo, "state.md", state)
            commit_fixture(repo, "complete product-team assessment")

        def seeded_pending(name):
            repo = base / name
            repo.mkdir()
            seed_upgrade_repo(repo, "5.4.1", f"{name}fixture", "# Existing product\n",
                              {"map.md": "# Map\n\n- [ ] Piece alpha — live\n",
                               "state.md": "# State\n\nPiece alpha is live.\n"})
            first = run_cli(kernel, "upgrade", repo)
            if first.returncode != 0:
                raise AssertionError(first.stderr or first.stdout)
            commit_fixture(repo, "accept pending upgrade")
            return repo

        def fixed_current(name, product=None, extra=None):
            repo = base / name
            repo.mkdir()
            init_repo(repo)
            installed = run_cli(kernel, "install", repo)
            if installed.returncode != 0:
                raise AssertionError(installed.stderr or installed.stdout)
            if product is not None:
                write_file(repo, "product.md", product)
            for relative, content in (extra or {}).items():
                write_file(repo, relative, content)
            commit_fixture(repo, "fixed current baseline")
            return repo

        def plant_refusal_dirt(repo):
            with (repo / "AGENTS.md").open("a") as handle:
                handle.write("installed-method refusal sentinel\n")
            state_path = repo / "state.md"
            state_path.parent.mkdir(parents=True, exist_ok=True)
            with state_path.open("a") as handle:
                handle.write("tracked unrelated refusal sentinel\n")
            write_file(repo, "work/refusal-dirt.md", "untracked unrelated refusal sentinel\n")
            write_file(repo, ".claude/skills/independent-review/refusal-dirt.md",
                       "retired skill must survive refusal\n")
            map_path = repo / "map.md"
            if map_path.exists():
                map_path.unlink()

        def run_atomic_refusal(repo):
            plant_refusal_dirt(repo)
            before = refusal_baseline(repo)
            refused = run_cli(kernel, "upgrade", repo)
            return refused, refusal_unchanged(repo, before, refused)

        missing_field = object()

        def refusal_repo(name, product, version="6.0.0-rc.2",
                         assessment_field=missing_field, record_content=None, marker_extra=None):
            repo = fixed_current(name)
            prior = {
                "name": "speck-next", "version": version, "commit": f"{name}fixture",
                "installedAt": "2026-01-02T03:04:05.000Z",
            }
            if assessment_field is not missing_field:
                prior["upgradeAssessmentRecord"] = assessment_field
            if marker_extra:
                prior.update(marker_extra)
                if "sourceCheckout" in marker_extra and "methodSurfaceSha256" in marker_extra:
                    prior.pop("commit", None)
            write_file(repo, ".claude/speck-next.json", json.dumps(prior, indent=2) + "\n")
            write_file(repo, "state.md", "# State\n\nPiece alpha is live.\n")
            if product is not None:
                write_file(repo, "product.md", product)
            if record_content is not None:
                write_file(repo, ASSESSMENT_RECORD, record_content)
            commit_fixture(repo, f"{name} refusal baseline")
            return repo

        snapshot_control = fixed_current("snapshot-positive")
        before_snapshot = repository_snapshot(snapshot_control)
        with (snapshot_control / "AGENTS.md").open("a") as handle:
            handle.write("snapshot positive-control byte\n")
        results.append(("complete-target snapshot detects one changed installed byte",
                        before_snapshot != repository_snapshot(snapshot_control)))

        fresh = base / "fresh"
        fresh.mkdir()
        init_repo(fresh)
        run = run_cli(kernel, "install", fresh)
        installed = [p for p in fresh.rglob("*") if p.is_file() and ".git" not in p.parts]
        fresh_ok = (run.returncode == 0 and marker(fresh)["version"] == "6.0.0-rc.2" and
                    marker_ok(fresh, source_checkout, surface_digest) and
                    not (fresh / "product.md").exists() and
                    len(installed) <= 20 and sum(p.stat().st_size for p in installed) <= 100_000 and
                    f"Installed Speck Next {provenance('6.0.0-rc.2', source_checkout, surface_digest)}" in run.stdout and
                    "Installed paths:" in run.stdout and "Next:" in run.stdout)
        results.append(("fresh install reports its surface and leaves product.md missing", fresh_ok))

        v5 = base / "v5"
        v5.mkdir()
        v5_product = "# Existing product\n\nPromise and history stay here.\n"
        seed_upgrade_repo(v5, "5.4.1", "v5fixture", v5_product)
        first = run_cli(kernel, "upgrade", v5)
        first_hash = surface_hash(v5)
        commit_fixture(v5, "accept first upgrade")
        second = run_cli(kernel, "upgrade", v5)
        second_hash = surface_hash(v5)
        migrated_v5 = (upgrade_report_ok(first, "5.4.1", "v5fixture", source_checkout,
                                         surface_digest, NEXT_PENDING_CHANGED) and
                       (v5 / "product.md").read_text() == expected_product(v5_product) and
                       marker_ok(v5, source_checkout, surface_digest, ASSESSMENT_RECORD) and
                       first_hash == second_hash and
                       upgrade_report_ok(second, "6.0.0-rc.2", source_checkout, source_checkout,
                                         surface_digest, NEXT_PENDING_CLEAN, surface_digest) and
                       "Working-tree changes across the complete installed surface plus product.md: none." in second.stdout and
                       "Complete installed-surface plus product.md diff: empty." in second.stdout)
        results.append(("v5 migration is selective and the second upgrade is byte-stable", migrated_v5))
        details.append(f"v5_second_hash={second_hash}")

        rc1 = base / "rc1"
        rc1.mkdir()
        rc1_product = f"# Existing product\n\nHistorical sentence.\n\n## Product team\n\n{RC1_STATUS}\n\nTrailing history.\n"
        expected_rc2 = expected_product(rc1_product.replace(RC1_STATUS, ""))
        seed_upgrade_repo(rc1, "6.0.0-rc.1", "rc1fixture", rc1_product)
        first = run_cli(kernel, "upgrade", rc1)
        first_hash = surface_hash(rc1)
        second = run_cli(kernel, "upgrade", rc1)
        second_hash = surface_hash(rc1)
        rc1_ok = (upgrade_report_ok(first, "6.0.0-rc.1", "rc1fixture", source_checkout,
                                   surface_digest, NEXT_PENDING_CHANGED) and
                  (rc1 / "product.md").read_text() == expected_rc2 and RC1_STATUS not in expected_rc2 and
                  first_hash == second_hash and
                  upgrade_report_ok(second, "6.0.0-rc.2", source_checkout, source_checkout,
                                    surface_digest, NEXT_PENDING_CHANGED, surface_digest) and
                  marker_ok(rc1, source_checkout, surface_digest, ASSESSMENT_RECORD))
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
        custom_ok = (upgrade_report_ok(first, "5.4.1", "customfixture", source_checkout,
                                      surface_digest, NEXT_PENDING_CHANGED) and
                     custom_text == expected_product(custom_product) and
                     custom_text.count(ASSESSMENT_HEADING) == 1 and
                     first_hash == surface_hash(custom) and
                     marker_ok(custom, source_checkout, surface_digest, ASSESSMENT_RECORD) and
                     second.returncode == 0)
        results.append(("custom Product team prose is untouched before one canonical assessment", custom_ok))

        missing = base / "missing"
        missing.mkdir()
        seed_upgrade_repo(missing, "5.4.1", "missingfixture")
        run = run_cli(kernel, "upgrade", missing)
        missing_ok = (upgrade_report_ok(run, "5.4.1", "missingfixture", source_checkout,
                                       surface_digest, NEXT_MISSING_CHANGED) and
                      marker_ok(missing, source_checkout, surface_digest) and
                      not (missing / "product.md").exists() and "product.md is missing" in run.stdout)
        results.append(("missing pre-v6 product stays missing and routes to Shape", missing_ok))

        current_product = "# Current selective product\n\nThe assessment is complete.\n"
        current = fixed_current(
            "current", current_product, {"state.md": "# State\n\nCurrent work is here.\n"}
        )
        first = run_cli(kernel, "upgrade", current)
        first_hash = surface_hash(current)
        second = run_cli(kernel, "upgrade", current)
        current_ok = (upgrade_report_ok(first, "6.0.0-rc.2", source_checkout, source_checkout,
                                        surface_digest, NEXT_CURRENT_CLEAN, surface_digest) and
                      (current / "product.md").read_text() == current_product and
                      marker_ok(current, source_checkout, surface_digest) and
                      upgrade_report_ok(second, "6.0.0-rc.2", source_checkout, source_checkout,
                                        surface_digest, NEXT_CURRENT_CLEAN, surface_digest) and
                      first_hash == surface_hash(current))
        results.append(("explicit-null current product resumes without an assessment", current_ok))

        current_missing = fixed_current("current-missing")
        first = run_cli(kernel, "upgrade", current_missing)
        second = run_cli(kernel, "upgrade", current_missing)
        current_missing_ok = (
            upgrade_report_ok(first, "6.0.0-rc.2", source_checkout, source_checkout,
                              surface_digest, NEXT_MISSING_CLEAN, surface_digest) and
            "product.md is missing" in first.stdout and not (current_missing / "product.md").exists() and
            marker_ok(current_missing, source_checkout, surface_digest) and
            upgrade_report_ok(second, "6.0.0-rc.2", source_checkout, source_checkout,
                              surface_digest, NEXT_MISSING_CLEAN, surface_digest) and
            not (current_missing / "product.md").exists())
        results.append(("explicit-null current repository with no product stays missing and routes to Shape",
                        current_missing_ok))

        porcelain = base / "porcelain"
        porcelain.mkdir()
        init_repo(porcelain)
        installed = run_cli(kernel, "install", porcelain)
        write_file(porcelain, "product.md", "# Porcelain product\n")
        write_file(porcelain, ".claude/speck-next.json", json.dumps({
            "name": "speck-next", "version": "5.4.1", "commit": "porcelainfixture",
            "installedAt": "2026-01-02T03:04:05.000Z",
        }, indent=2) + "\n")
        commit_fixture(porcelain, "porcelain fixture baseline")
        run = run_cli(kernel, "upgrade", porcelain)
        porcelain_ok = (
            installed.returncode == 0 and
            upgrade_report_ok(run, "5.4.1", "porcelainfixture", source_checkout,
                              surface_digest, NEXT_PENDING_CHANGED) and
            marker_ok(porcelain, source_checkout, surface_digest, ASSESSMENT_RECORD) and
            "Working-tree changes across the complete installed surface plus product.md:\n M .claude/speck-next.json\n" in run.stdout)
        results.append(("first unstaged changed path keeps both porcelain status columns", porcelain_ok))

        dirty = base / "dirty"
        dirty.mkdir()
        seed_upgrade_repo(dirty, "5.4.1", "dirtyfixture", "# Dirty product\n",
                          {"state.md": "baseline state\n", "work/inflight.md": "baseline work\n"})
        dirty_state = "baseline state\nowner's uncommitted state\n"
        dirty_work = "baseline work\nowner's uncommitted work\n"
        write_file(dirty, "state.md", dirty_state)
        write_file(dirty, "work/inflight.md", dirty_work)
        run = run_cli(kernel, "upgrade", dirty)
        dirty_ok = (upgrade_report_ok(run, "5.4.1", "dirtyfixture", source_checkout,
                                     surface_digest, NEXT_PENDING_CHANGED) and
                    marker_ok(dirty, source_checkout, surface_digest, ASSESSMENT_RECORD) and
                    (dirty / "state.md").read_text() == dirty_state and
                    (dirty / "work/inflight.md").read_text() == dirty_work)
        results.append(("dirty unrelated work survives byte for byte", dirty_ok))

        retry = fixed_current("retry")
        write_file(retry, ".claude/speck-next.json", json.dumps({
            "name": "speck-next", "version": "5.4.1", "commit": "retryfixture",
            "installedAt": "2026-01-02T03:04:05.000Z",
        }, indent=2) + "\n")
        write_file(retry, "state.md", "baseline tracked state\n")
        (retry / "product.md").mkdir()
        write_file(retry, "product.md/sentinel.txt", "product path is a directory\n")
        commit_fixture(retry, "product-directory refusal baseline")
        failed, refusal_atomic = run_atomic_refusal(retry)
        (retry / "product.md/sentinel.txt").unlink()
        (retry / "product.md").rmdir()
        write_file(retry, "product.md", "# Recovered product\n")
        retried = run_cli(kernel, "upgrade", retry)
        retry_ok = (refusal_atomic and "product.md exists but is not a file" in failed.stderr and
                    upgrade_report_ok(retried, "5.4.1", "retryfixture", source_checkout,
                                                     surface_digest, NEXT_PENDING_CHANGED) and
                    marker_ok(retry, source_checkout, surface_digest, ASSESSMENT_RECORD))
        results.append(("product-directory refusal is byte-atomic and a repair retries", retry_ok))

        unknown = base / "unknown"
        unknown.mkdir()
        seed_upgrade_repo(unknown, "mystery", "unknownfixture", "# Unknown era\n")
        before = surface_hash(unknown)
        refused = run_cli(kernel, "upgrade", unknown)
        unknown_ok = (refused.returncode != 0 and "unknown version" in refused.stderr and
                      "Nothing was touched" in refused.stderr and before == surface_hash(unknown))
        results.append(("unknown marker version refuses before touching the repository", unknown_ok))

        rejected = base / "rejected-rc2"
        rejected.mkdir()
        rejected_product = ("# Rejected rc.2 product\n\n> " + REJECTED_RC2_STATUS +
                            "\n\n## Product team\n\n" + REJECTED_RC2_STATUS + "\n")
        seed_upgrade_repo(rejected, "6.0.0-rc.2", "rejectedfixture", rejected_product)
        run = run_cli(kernel, "upgrade", rejected)
        repaired_text = (rejected / "product.md").read_text()
        rejected_ok = (
            upgrade_report_ok(run, "6.0.0-rc.2", "rejectedfixture", source_checkout,
                              surface_digest, NEXT_PENDING_CHANGED) and
            repaired_text.count(ASSESSMENT_HEADING) == 1 and
            f"> {REJECTED_RC2_STATUS}" in repaired_text and
            not any(line == REJECTED_RC2_STATUS for line in repaired_text.splitlines()) and
            marker_ok(rejected, source_checkout, surface_digest, ASSESSMENT_RECORD))
        results.append(("rejected rc.2 generated status becomes explicit while its quote stays inert", rejected_ok))

        fieldless_canonical = refusal_repo(
            "fieldless-canonical", "# Current product\n\n" + ASSESSMENT_BLOCK
        )
        run = run_cli(kernel, "upgrade", fieldless_canonical)
        fieldless_canonical_ok = (
            upgrade_report_ok(run, "6.0.0-rc.2", "fieldless-canonicalfixture",
                              source_checkout, surface_digest, NEXT_PENDING_CHANGED) and
            marker_ok(fieldless_canonical, source_checkout, surface_digest, ASSESSMENT_RECORD) and
            (fieldless_canonical / "product.md").read_text() == "# Current product\n\n" + ASSESSMENT_BLOCK)
        results.append(("fieldless current marker uses surviving canonical evidence",
                        fieldless_canonical_ok))

        fieldless_missing = refusal_repo("fieldless-missing-product", None)
        run = run_cli(kernel, "upgrade", fieldless_missing)
        fieldless_missing_ok = (
            upgrade_report_ok(run, "6.0.0-rc.2", "fieldless-missing-productfixture",
                              source_checkout, surface_digest, NEXT_MISSING_CHANGED) and
            marker_ok(fieldless_missing, source_checkout, surface_digest) and
            not (fieldless_missing / "product.md").exists())
        results.append(("fieldless current marker with no product safely records null",
                        fieldless_missing_ok))

        atomic_specs = [
            ("exact rejected-rc.2 deletion is ambiguous",
             "# Rejected migration with its generated assessment deleted\n", "6.0.0-rc.2",
             missing_field),
            ("fieldless current product is ambiguous",
             "# Fieldless current product\n", "6.0.0-rc.2", missing_field),
            ("unsupported assessment-record value",
             "# Product\n\n" + ASSESSMENT_BLOCK, "6.0.0-rc.2", "work/other.md"),
            ("empty assessment-record value",
             "# Product\n", "6.0.0-rc.2", ""),
            ("canonical block missing its status field",
             f"# Product\n\n{ASSESSMENT_HEADING}\n\n{ASSESSMENT_RECORD_LINE}\n",
             "6.0.0-rc.2", ASSESSMENT_RECORD),
            ("canonical block duplicates its status field",
             f"# Product\n\n{ASSESSMENT_HEADING}\n\n{ASSESSMENT_PENDING}\n{ASSESSMENT_PENDING}\n{ASSESSMENT_RECORD_LINE}\n",
             "6.0.0-rc.2", ASSESSMENT_RECORD),
            ("canonical block misses its record field",
             f"# Product\n\n{ASSESSMENT_HEADING}\n\n{ASSESSMENT_PENDING}\n",
             "6.0.0-rc.2", ASSESSMENT_RECORD),
            ("canonical block duplicates its record field",
             f"# Product\n\n{ASSESSMENT_HEADING}\n\n{ASSESSMENT_PENDING}\n{ASSESSMENT_RECORD_LINE}\n{ASSESSMENT_RECORD_LINE}\n",
             "6.0.0-rc.2", ASSESSMENT_RECORD),
            ("canonical block has the wrong record field",
             f"# Product\n\n{ASSESSMENT_HEADING}\n\n{ASSESSMENT_PENDING}\n**Record:** `work/wrong.md`\n",
             "6.0.0-rc.2", ASSESSMENT_RECORD),
            ("generated rc.1 fingerprint is duplicated",
             f"# Product\n\n{RC1_STATUS}\n{RC1_STATUS}\n", "6.0.0-rc.1", missing_field),
            ("generated rejected-rc.2 fingerprint is duplicated",
             f"# Product\n\n{REJECTED_RC2_STATUS}\n{REJECTED_RC2_STATUS}\n",
             "6.0.0-rc.2", missing_field),
        ]
        for label, product_text, version, assessment_field in atomic_specs:
            repo = refusal_repo(
                "atomic-" + re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-"),
                product_text, version, assessment_field,
            )
            refused, atomic = run_atomic_refusal(repo)
            results.append((f"{label} and refuses before every target write", atomic))

        laundered = refusal_repo(
            "atomic-99a-laundered-deletion",
            "# Rejected migration laundered after its assessment was deleted\n",
            marker_extra={"sourceCheckout": "99a0f38", "methodSurfaceSha256": "a" * 64},
        )
        refused, laundered_ok = run_atomic_refusal(laundered)
        results.append(("99a0f38 provenance cannot launder deleted assessment state",
                        laundered_ok))

        route_specs = [
            ("Shape", ASSESSMENT_COMPLETE_SHAPE, "Shape reopened.",
             "# State\n\nShape is reopened.\n", "Next: there are no upgrade changes to commit; continue Shape from state.md.", ""),
            ("Map", ASSESSMENT_COMPLETE_MAP, "Map reopened.",
             "# State\n\nMap is reopened.\n", "Next: there are no upgrade changes to commit; continue Map from state.md.", ""),
            ("resume", "**Speck Next upgrade assessment:** complete — resumed Piece alpha from state.md",
             "Resume Piece alpha from state.md.", "# State\n\nPiece alpha is live.\n",
             "Next: there are no upgrade changes to commit; resume Piece alpha from state.md.",
             f"> {REJECTED_RC2_STATUS}\nHistorical wording paraphrases that an assessment once waited."),
        ]
        for name, status, route, state, expected_next, retained in route_specs:
            repo = seeded_pending(f"complete-{name.lower()}")
            complete_pending(repo, status, route, state, retained)
            before = surface_hash(repo)
            run = run_cli(kernel, "upgrade", repo)
            route_ok = (
                upgrade_report_ok(run, "6.0.0-rc.2", source_checkout, source_checkout,
                                  surface_digest, expected_next, surface_digest) and
                marker_ok(repo, source_checkout, surface_digest, ASSESSMENT_RECORD) and
                assessment_record_ok((repo / ASSESSMENT_RECORD).read_text(), route) and
                before == surface_hash(repo) and
                (not retained or retained in (repo / "product.md").read_text()))
            results.append((f"completed assessment follows the {name} route", route_ok))

        corruptions = {
            "missing product": None,
            "duplicate block": lambda text: text + "\n" + ASSESSMENT_BLOCK,
            "malformed status": lambda text: text.replace(ASSESSMENT_PENDING,
                                                            "**Speck Next upgrade assessment:** finished", 1),
            "deleted block": lambda text: text.replace("\n" + ASSESSMENT_BLOCK, "", 1),
        }
        for name, mutation in corruptions.items():
            repo = seeded_pending("corrupt-" + name.replace(" ", "-"))
            product_path = repo / "product.md"
            if mutation is None:
                product_path.unlink()
            else:
                product_path.write_text(mutation(product_path.read_text()))
            commit_fixture(repo, f"{name} corruption")
            failed, corruption_ok = run_atomic_refusal(repo)
            results.append((f"{name} refuses before every target write", corruption_ok))

        missing_record = seeded_pending("missing-completed-record")
        product_path = missing_record / "product.md"
        product_path.write_text(product_path.read_text().replace(
            ASSESSMENT_PENDING,
            "**Speck Next upgrade assessment:** complete — resumed Piece alpha from state.md", 1))
        commit_fixture(missing_record, "claim completion without its record")
        failed, missing_record_ok = run_atomic_refusal(missing_record)
        missing_record_ok = missing_record_ok and ASSESSMENT_RECORD in failed.stderr
        results.append(("completed assessment without its record refuses before every target write",
                        missing_record_ok))

        provenance_kernel = base / "provenance-kernel"
        provenance_kernel.mkdir()
        for relative in ("package.json", "AGENTS.md", "CLAUDE.md"):
            shutil.copy2(kernel / relative, provenance_kernel / relative)
        shutil.copytree(kernel / "bin", provenance_kernel / "bin")
        shutil.copytree(kernel / ".claude/skills", provenance_kernel / ".claude/skills")
        shutil.copytree(kernel / "templates", provenance_kernel / "templates")
        init_repo(provenance_kernel)
        commit_fixture(provenance_kernel, "provenance checkout one")
        checkout_one = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=provenance_kernel,
                                      check=True, capture_output=True, text=True).stdout.strip()
        install_one = base / "provenance-one"
        install_one.mkdir()
        init_repo(install_one)
        first = run_cli(provenance_kernel, "install", install_one)
        subprocess.run(["git", "commit", "--allow-empty", "-q", "-m", "provenance checkout two"],
                       cwd=provenance_kernel, check=True)
        checkout_two = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=provenance_kernel,
                                      check=True, capture_output=True, text=True).stdout.strip()
        install_two = base / "provenance-two"
        install_two.mkdir()
        init_repo(install_two)
        second = run_cli(provenance_kernel, "install", install_two)
        digest_one = method_surface_sha256(install_one)
        digest_two = method_surface_sha256(install_two)
        provenance_ok = (
            first.returncode == second.returncode == 0 and checkout_one != checkout_two and
            digest_one == digest_two and
            marker_ok(install_one, checkout_one, digest_one) and
            marker_ok(install_two, checkout_two, digest_two) and
            provenance("6.0.0-rc.2", checkout_one, digest_one) in first.stdout and
            provenance("6.0.0-rc.2", checkout_two, digest_two) in second.stdout)
        results.append(("different source checkouts identify one identical installed method surface", provenance_ok))

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
    assessments_ok = run_assessment_controls()
    migration_ok = run_migration_matrix(kernel)
    passed = homes_ok and roles_ok and assessments_ok and migration_ok
    print(f"Piece 8 controls: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


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
