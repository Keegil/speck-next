#!/usr/bin/env python3
"""Separated team: prove selective repository semantics or inspect a governed host run."""
import copy, hashlib, importlib.util, json, os, pathlib, re, shlex, shutil, subprocess, sys, tempfile
import tarfile
from datetime import date, timedelta


CHECKER_KERNEL = pathlib.Path(__file__).resolve().parents[3]
CURRENT_VERSION = json.loads((CHECKER_KERNEL / "package.json").read_text())["version"]
RECOVERABLE_FIELDLESS_VERSION = "6.0.0-rc.2"
RC1_STATUS = "**Upgrade status:** Unassessed under v6. Historical work keeps its original evidence and is not backfilled as role-shaped. Before the next substantial piece, Product, Business, Experience, and Engineering assess this product in four separate contexts. Reopen Shape only if that assessment finds a wrong promise."
REJECTED_RC2_STATUS = "**Upgrade status:** Unassessed under Speck Next 6.0.0-rc.2. Historical work keeps its original evidence and is not backfilled as role-shaped. Before the next substantial piece, separate Product, Business, Experience, and Engineering carriers assess the existing product and current map once. Business and Experience then define their observable call conditions, trusted evidence, expiry, and material changes. Reopen Shape only for a wrong promise and Map only for a wrong piece or order."
ASSESSMENT_HEADING = "## Speck Next upgrade assessment"
ASSESSMENT_RECORD = "work/product-team-assessment.md"
ASSESSMENT_RECORD_LINE = f"**Record:** `{ASSESSMENT_RECORD}`"
ASSESSMENT_PENDING = "**Speck Next upgrade assessment:** pending"
ASSESSMENT_BLOCK = f"{ASSESSMENT_HEADING}\n\n{ASSESSMENT_PENDING}\n{ASSESSMENT_RECORD_LINE}\n"
ASSESSMENT_COMPLETE_SHAPE = "**Speck Next upgrade assessment:** complete — Shape reopened"
ASSESSMENT_COMPLETE_MAP = "**Speck Next upgrade assessment:** complete — Map reopened"
PRODUCT_TEAM_FIELDS = ("Protects", "Call when", "May stay out when", "Evidence expires",
                       "Material changes")
NEXT_MISSING_CHANGED = "Next: review the reported paths and complete diff, commit the upgrade, then open Shape to create and ratify product.md before Map or any substantial work."
NEXT_MISSING_CLEAN = "Next: there are no upgrade changes to commit; open Shape to create and ratify product.md before Map or any substantial work."
NEXT_PENDING_CHANGED = f"Next: review the reported paths and complete diff, commit the upgrade, then complete {ASSESSMENT_RECORD} by following “Finish an upgrade” in AGENTS.md."
NEXT_PENDING_CLEAN = f"Next: there are no upgrade changes to commit; complete {ASSESSMENT_RECORD} by following “Finish an upgrade” in AGENTS.md."
NEXT_CURRENT_CHANGED = "Next: review the reported paths and complete diff, commit the upgrade, then resume current work from state.md."
NEXT_CURRENT_CLEAN = "Next: there are no upgrade changes to commit; resume current work from state.md."
AMBIGUITY_RETRY = "Next: run the upgrade again with --open-assessment to conservatively open the one-time assessment. Product work will not resume until that assessment records its route."
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


AUTHORIZATION_FIELDS = (
    "model_turns", "contexts", "elapsed_seconds", "retries", "fallbacks",
    "owner_interruptions", "pre_run_minutes", "pre_run_files",
)
PRODUCT_EVIDENCE_FIELDS = (
    "real_result", "checks_passed", "synthesis_before_implementation",
    "engineering_only_implementation", "active_returns_complete", "business_permits",
)
DISPOSITION_FIELDS = {
    "reviewable", "cost_experiment", "cost_finding", "product_sufficient",
    "further_model_work",
}


def disposition_truth(case):
    errors = []
    token_evidence = case.get("tokens", {})
    estimate = token_evidence.get("estimate", {})
    measured = token_evidence.get("measured", {})
    if not measured or set(measured) != {"gross", "cached", "fresh"}:
        errors.append("gross, cached, and fresh token measurements are all required")
    elif (any(not isinstance(value, (int, float)) or value < 0 for value in measured.values()) or
          measured["gross"] - measured["cached"] != measured["fresh"]):
        errors.append("token measurements are invalid or do not reconcile")
    if (not estimate or not set(estimate) <= {"gross", "cached", "fresh"} or
            any(not isinstance(value, (int, float)) or value < 0 for value in estimate.values())):
        errors.append("at least one non-negative token estimate is required")

    cost_finding = bool(not errors and any(measured[key] > value for key, value in estimate.items()))
    cost_experiment = "failed" if cost_finding else "passed"

    authorization = case.get("authorization", {})
    limits = authorization.get("limits", {})
    used = authorization.get("used", {})
    next_work = authorization.get("next", {})
    if set(limits) != set(AUTHORIZATION_FIELDS) or set(used) != set(AUTHORIZATION_FIELDS):
        errors.append("execution authorization must declare every prospectively knowable field")
        authorization_open = False
    elif any(not isinstance(value, (int, float)) or value < 0
             for value in list(limits.values()) + list(used.values()) + list(next_work.values())):
        errors.append("execution authorization values must be non-negative numbers")
        authorization_open = False
    elif not set(next_work) <= set(AUTHORIZATION_FIELDS):
        errors.append("next model work contains an undeclared authorization field")
        authorization_open = False
    else:
        authorization_open = all(
            used[field] + next_work.get(field, 0) <= limits[field]
            for field in AUTHORIZATION_FIELDS
        )

    product = case.get("product", {})
    if not set(PRODUCT_EVIDENCE_FIELDS) <= set(product):
        errors.append("the product evidence chain is incomplete")
        reviewable = False
    else:
        reviewable = all(bool(product[field]) for field in PRODUCT_EVIDENCE_FIELDS)
    product_sufficient = bool(
        reviewable and product.get("contributor_excluded_fresh_use") and
        product.get("independent_judgment")
    )
    product_reason = bool(
        not product.get("real_result") or product.get("concrete_product_finding") or
        product.get("new_product_claim")
    )
    further_model_work = bool(authorization_open and product_reason)
    return {
        "reviewable": reviewable,
        "cost_experiment": cost_experiment,
        "cost_finding": cost_finding,
        "product_sufficient": product_sufficient,
        "further_model_work": further_model_work,
    }, errors


def make_disposition_case(name, claims, *, token_estimate=None, token_measured=None,
                          limits=None, used=None, next_work=None, product=None):
    default_limits = {
        "model_turns": 5, "contexts": 4, "elapsed_seconds": 900,
        "retries": 0, "fallbacks": 0, "owner_interruptions": 0,
        "pre_run_minutes": 30, "pre_run_files": 20,
    }
    default_used = {
        "model_turns": 2, "contexts": 4, "elapsed_seconds": 300,
        "retries": 0, "fallbacks": 0, "owner_interruptions": 0,
        "pre_run_minutes": 20, "pre_run_files": 12,
    }
    default_product = {
        "real_result": True,
        "checks_passed": True,
        "synthesis_before_implementation": True,
        "engineering_only_implementation": True,
        "active_returns_complete": True,
        "business_permits": True,
        "contributor_excluded_fresh_use": False,
        "independent_judgment": False,
        "concrete_product_finding": False,
        "new_product_claim": False,
    }
    actual_limits = dict(default_limits)
    actual_limits.update(limits or {})
    actual_used = dict(default_used)
    actual_used.update(used or {})
    actual_product = dict(default_product)
    actual_product.update(product or {})
    return {
        "name": name,
        "tokens": {
            "estimate": token_estimate or {"gross": 300, "cached": 100, "fresh": 200},
            "measured": token_measured or {"gross": 250, "cached": 100, "fresh": 150},
        },
        "authorization": {
            "limits": actual_limits,
            "used": actual_used,
            "next": next_work or {"model_turns": 1, "elapsed_seconds": 1},
        },
        "product": actual_product,
        "claims": claims,
    }


def validate_disposition_case(case):
    truth, errors = disposition_truth(case)
    claims = case.get("claims", {})
    if set(claims) != DISPOSITION_FIELDS:
        errors.append("the record does not state product evidence, cost, and further-spend dispositions")
    else:
        for field, expected in truth.items():
            if claims[field] != expected:
                errors.append(f"{field} says {claims[field]!r}; evidence says {expected!r}")
    return errors


def run_result_disposition_controls():
    v09 = make_disposition_case(
        "exact v0.9 evidence stays reviewable / failed / closed",
        {"reviewable": True, "cost_experiment": "failed", "cost_finding": True,
         "product_sufficient": False, "further_model_work": False},
        token_estimate={"fresh": 200000},
        token_measured={"gross": 850035, "cached": 617600, "fresh": 232435},
        limits={"model_turns": 9},
        used={"model_turns": 9, "elapsed_seconds": 402.654, "retries": 1},
    )
    low_token = make_disposition_case(
        "low-token incomplete product cannot enter review",
        {"reviewable": False, "cost_experiment": "passed", "cost_finding": False,
         "product_sufficient": False, "further_model_work": True},
        product={"real_result": False, "checks_passed": False},
    )
    above_estimate = make_disposition_case(
        "material result above estimate stays reviewable with a cost finding",
        {"reviewable": True, "cost_experiment": "failed", "cost_finding": True,
         "product_sufficient": False, "further_model_work": False},
        token_measured={"gross": 350, "cached": 100, "fresh": 250},
    )
    judged = make_disposition_case(
        "fresh use and independent judgment establish product sufficiency",
        {"reviewable": True, "cost_experiment": "passed", "cost_finding": False,
         "product_sufficient": True, "further_model_work": False},
        product={"contributor_excluded_fresh_use": True, "independent_judgment": True},
    )
    product_finding = make_disposition_case(
        "concrete fresh-review product finding can authorize another build",
        {"reviewable": True, "cost_experiment": "passed", "cost_finding": False,
         "product_sufficient": False, "further_model_work": True},
        product={"concrete_product_finding": True},
    )
    new_claim = make_disposition_case(
        "genuinely new product claim can authorize another build",
        {"reviewable": True, "cost_experiment": "passed", "cost_finding": False,
         "product_sufficient": False, "further_model_work": True},
        product={"new_product_claim": True},
    )

    authorization_overflows = [
        ("sixth model turn", {"model_turns": 5}),
        ("extra context", {"contexts": 5}),
        ("retry overflow", {"retries": 1}),
        ("fallback overflow", {"fallbacks": 1}),
        ("elapsed-time overflow", {"elapsed_seconds": 901}),
        ("owner-interruption overflow", {"owner_interruptions": 1}),
        ("pre-run-time overflow", {"pre_run_minutes": 31}),
        ("pre-run-file overflow", {"pre_run_files": 21}),
    ]
    authorization_cases = [
        make_disposition_case(
            f"{label} closes further model work",
            {"reviewable": True, "cost_experiment": "passed", "cost_finding": False,
             "product_sufficient": False, "further_model_work": False},
            used=changes,
            product={"concrete_product_finding": True},
        )
        for label, changes in authorization_overflows
    ]
    clean = [v09, low_token, above_estimate, judged, product_finding, new_claim, *authorization_cases]

    mutants = []
    for label, source, field, value in [
        ("v0.9 cost failure rescued", v09, "cost_experiment", "passed"),
        ("v0.9 further spend reopened", v09, "further_model_work", True),
        ("low-token incomplete work admitted", low_token, "reviewable", True),
        ("cost green converted to product sufficiency", low_token, "product_sufficient", True),
        ("above-estimate cost finding erased", above_estimate, "cost_finding", False),
        ("existing result duplicated without product reason", above_estimate, "further_model_work", True),
    ]:
        mutant = copy.deepcopy(source)
        mutant["name"] = label
        mutant["claims"][field] = value
        mutants.append(mutant)
    for case in authorization_cases:
        mutant = copy.deepcopy(case)
        mutant["name"] = f"{case['name']} mutant reopens spend"
        mutant["claims"]["further_model_work"] = True
        mutants.append(mutant)

    good = True
    for case in clean:
        errors = validate_disposition_case(case)
        passed = not errors
        print(f"  [{'ok' if passed else 'RED'}] disposition clean: {case['name']}")
        if errors:
            print("    " + "; ".join(errors))
        good = good and passed
    for case in mutants:
        errors = validate_disposition_case(case)
        passed = bool(errors)
        print(f"  [{'ok' if passed else 'RED'}] disposition mutant rejected: {case['name']}" +
              (f" ({errors[0]})" if errors else ""))
        good = good and passed
    print(f"  [measure] result-disposition subjects={len(clean) + len(mutants)} "
          f"clean={len(clean)} mutants={len(mutants)}")
    return good


def static_contract_homes(kernel):
    required = {
        "AGENTS.md": ["Product and Engineering are always called", "named run and its return",
                      "token estimate", "Exhausting any part forbids another",
                      "Contributor-excluded fresh use", "duplicate product work",
                      "wrongly kept inactive", "concern was handled", "replacement carrier",
                      "Finish an upgrade", ASSESSMENT_RECORD, "complete — Shape reopened",
                      "complete — Map reopened", "from state.md", "upgradeAssessmentRecord",
                      "does not guess", "before replacing any repository byte",
                      "assessment refusal", "upgrade [dir] --open-assessment",
                      "cannot override any other state",
                      "comment-touched line stays inactive",
                      "multiline inline-code spans", "unmatched backtick run is literal",
                      "only a plain current line can start a multiline span",
                      "unclosed live comment refuses", "exactly one usable row",
                      "Product-team section", "values as opaque", "restore pending",
                      "LF, CRLF, lone CR", "last line ending", "default-ignorable"],
        ".claude/skills/shape-product/SKILL.md": ["observable conditions", "evidence expires"],
        ".claude/skills/shape-product/references/questions.md": ["what observable condition calls the role"],
        ".claude/skills/map-build/SKILL.md": ["first Map after Shape", "later re-map",
                                                    "token estimate", "duplicate product work"],
        ".claude/skills/map-build/references/questions.md": ["Product and Engineering join every substantial piece",
                                                                 "token estimate", "authorization exhaustion"],
        ".claude/skills/experience/SKILL.md": ["Gross, cached, fresh", "duplicate product work"],
        "templates/product.md": ["Call when:", "Evidence expires:"],
        "templates/map.md": ["role calls:", "earliest informative runs:", "model-work boundary:",
                             "concrete fresh-review product finding"],
        "templates/piece.md": ["## Role call decisions", "## Informative role returns",
                               "## False inactive repair", "## Handled-concern miss escalation",
                               "Token estimate:", "Execution authorization:", "Result disposition:"],
        "templates/state.md": ["overdue informative returns", "false inactive call",
                               "cost experiment passed or failed", "duplicate product build"],
        "CONTRACT.md": ["On a later re-map, Product contributes", "named run and its return",
                        "gross, cached, and fresh tokens", "Exhausting any authorization forbids another",
                        "contributor-excluded fresh use", "cannot trigger duplicate product work",
                        "writes the version marker last", "replacement carrier inherits",
                        ASSESSMENT_RECORD, "method-surface digests", "Every fixed marker carries",
                        "before changing any repository byte", "complete non-Git path kinds and bytes",
                        "fieldless-current refusal and explicit recovery",
                        "flag-exclusion and argument-error tables",
                        "inactive-container tables", "top-level `<!-- ... -->` comments",
                        "multiline inline-code spans",
                        "unmatched or wrong-length backtick run is literal",
                        "only a plain current line can start a multiline span",
                        "Product-team required-value and duplicate tables",
                        "completed Map and resume routes", "values as opaque",
                        "LF, CRLF, lone CR", "last existing line ending", "default-ignorable",
                        "Native Codex discovery", "installer-generated symbolic-link entry",
                        "duplicated skill body"],
        "README.md": ["right product-building views", ASSESSMENT_RECORD,
                      "Results and cost stay separate", "crossing the estimate stays visible",
                      "genuinely new product claim permits another build",
                      "source checkout separately", "fieldless current rc.2 marker is unknown",
                      "before any repository byte changes", "upgrade [dir] --open-assessment",
                      "comment-touched line stays inactive", "unclosed live comment refuses",
                      "balanced inline-code span", "unmatched backtick is plain text",
                      "only a plain current line can start a multiline span",
                      "one row per role", "completed Map or resume route",
                      "owner bytes are never generated or normalized",
                      "LF, CRLF, lone CR", "last existing line ending", "default-ignorable",
                      "20 files / 85,618 bytes", "Codex discovery symlink",
                      "47,374 bytes"],
        "capabilities.md": ["Selective product team", "result-disposition subjects",
                            "reviewable / failed / closed",
                            "assessment-control subjects", "complete-target snapshot",
                            "ambiguity-recovery", "inactive-container",
                            "95 path-transaction subjects", "Codex discovery symlink",
                            "20 file-system entries / 85,618 bytes", "47,374 / 50,000 bytes"],
    }
    stale = {
        "AGENTS.md": ["Every substantial piece gets four product-building roles"],
        "templates/map.md": ["expected active roles:"],
        "templates/piece.md": ["## Pre-code product team"],
        "CONTRACT.md": ["four distinct pre-code carriers on substantial work",
                        "On later re-maps and substantial pieces, Product and Engineering always contribute",
                        "v0.9 cost exchange"],
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
    version_ok = version == CURRENT_VERSION
    legacy_ok = RECOVERABLE_FIELDLESS_VERSION == "6.0.0-rc.2"
    print(f"  [{'ok' if version_ok else 'RED'}] current assertions derive package version {CURRENT_VERSION}")
    print(f"  [{'ok' if legacy_ok else 'RED'}] recoverable fieldless legacy stays explicit rc.2")
    return good and version_ok and legacy_ok


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


def run_cli_args(kernel, *arguments, cwd=None, env=None):
    merged_env = None if env is None else dict(os.environ, **env)
    return subprocess.run(["node", str(kernel / "bin/speck-next.js"), *map(str, arguments)],
                          cwd=cwd or kernel, capture_output=True, text=True, env=merged_env)


def run_cli(kernel, command, target, *arguments):
    return run_cli_args(kernel, command, target, *arguments)


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
        mode = info.st_mode & 0o7777
        if item.is_symlink():
            kind, payload = f"link:{mode:o}", os.readlink(item).encode()
        elif item.is_dir():
            kind, payload = f"directory:{mode:o}", b""
        elif item.is_file():
            kind, payload = f"file:{mode:o}", item.read_bytes()
        else:
            kind, payload = f"other:{info.st_mode}", b""
        entries.append((relative.as_posix(), kind, payload))
    return tuple(entries)


def snapshot_digest(root):
    digest = hashlib.sha256()
    for relative, kind, payload in repository_snapshot(root):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0" + payload + b"\0")
    return digest.hexdigest()


def porcelain_v1_z(root):
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update({
        "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull, "GIT_PAGER": "cat", "PAGER": "cat",
        "LC_ALL": "C",
    })
    return subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=root, check=True, capture_output=True, env=env,
    ).stdout


def repo_baseline(root):
    return {
        "tree": repository_snapshot(root),
        "porcelain": porcelain_v1_z(root),
    }


def repo_unchanged(root, before):
    return (
        repository_snapshot(root) == before["tree"] and
        porcelain_v1_z(root) == before["porcelain"]
    )


def refusal_baseline(root):
    return {
        "marker": (root / ".claude/speck-next.json").read_bytes(),
        **repo_baseline(root),
    }


def snapshot_unchanged(root, before):
    return (
        (root / ".claude/speck-next.json").read_bytes() == before["marker"] and
        repo_unchanged(root, before)
    )


def has_resume_instruction(output):
    return any(
        re.search(r"^Next:\s*resume\b|[,;]\s*then\s+resume\b", line, re.IGNORECASE)
        for line in output.splitlines()
    )


def refusal_unchanged(root, before, run):
    return (
        run.returncode != 0 and
        "Nothing in the repository changed." in run.stderr and
        "run the upgrade again" in run.stderr and
        not has_resume_instruction(run.stdout + run.stderr) and
        snapshot_unchanged(root, before)
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
        "version": CURRENT_VERSION,
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
            f"{provenance(prior_version, prior_checkout, prior_digest)} -> {provenance(CURRENT_VERSION, source_checkout, surface_digest)}" in output and
            "Product team migration:" in output and
            "Working-tree changes across the complete installed surface plus product.md:" in output and
            "Complete installed-surface plus product.md diff" in output and
            next_lines == [expected_next] and run.stdout.rstrip().endswith(expected_next))


def run_path_transaction_controls(kernel):
    source_checkout = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=kernel,
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    surface_digest = method_surface_sha256(kernel)
    results = []

    with tempfile.TemporaryDirectory(prefix="speck-piece8-paths-") as temporary:
        base = pathlib.Path(temporary)

        def fresh_repo(name):
            repo = base / name
            repo.mkdir()
            init_repo(repo)
            return repo

        def transaction_dirt(repo):
            sibling = list(repo.parent.glob(f".{repo.name}.speck-next-transaction-*"))
            nested = list(repo.glob(f".{repo.name}.speck-next-transaction-*"))
            return sibling + nested

        def calm_failure(run):
            output = run.stdout + run.stderr
            forbidden = (
                "Installed Speck Next", "Upgraded Speck Next",
                "Working-tree changes across", "Complete installed-surface",
                "commit the upgrade", "Next:",
            )
            return (
                run.returncode != 0 and
                all(item not in output for item in forbidden) and
                not has_resume_instruction(output) and
                "Error:" not in output and " at " not in run.stderr
            )

        def stable_retry(repo, first, retry_kernel=kernel):
            before = repo_baseline(repo)
            retry = run_cli(retry_kernel, "upgrade", repo)
            return (
                first.returncode == 0 and retry.returncode == 0 and
                repo_unchanged(repo, before) and not transaction_dirt(repo)
            )

        def install_report(run):
            summary = re.search(
                r" — (\d+) installed or carried-forward files on disk\.", run.stdout
            )
            listing = re.search(r"Installed paths:\n(.*?)\nNext:", run.stdout, re.DOTALL)
            return (
                int(summary.group(1)) if summary else None,
                listing.group(1).splitlines() if listing else [],
            )

        def codex_adapter(root):
            parent = root / ".agents/skills"
            if not parent.is_dir():
                return None
            candidates = sorted(
                (item for item in parent.iterdir()
                 if re.fullmatch(r"speck-next(?:-(?:[2-9]|[1-9][0-9]+))?", item.name, re.I)),
                key=lambda item: (
                    1 if item.name.lower() == "speck-next" else
                        int(item.name.lower().removeprefix("speck-next-")),
                    item.name.casefold(), item.name,
                ),
            )
            return next(
                (item for item in candidates
                 if item.is_symlink() and
                    (os.readlink(item) == "../../.claude/skills" or
                     (item.resolve() == (root / ".claude/skills").resolve() and
                      item.resolve().is_relative_to(root.resolve())))),
                None,
            )

        def codex_adapter_name(root):
            adapter = codex_adapter(root)
            return adapter.name if adapter is not None else None

        def exact_path_snapshot(path):
            try:
                info = path.lstat()
            except FileNotFoundError:
                return ("missing",)
            mode = info.st_mode & 0o7777
            if path.is_symlink():
                return (f"link:{mode:o}", os.readlink(path).encode())
            if path.is_dir():
                return (f"directory:{mode:o}", repository_snapshot(path))
            if path.is_file():
                return (f"file:{mode:o}", path.read_bytes())
            return (f"other:{info.st_mode}",)

        def git_metadata_env():
            safe = {key: value for key, value in os.environ.items()
                    if not key.startswith("GIT_")}
            safe.update({
                "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull, "GIT_PAGER": "cat", "PAGER": "cat",
                "LC_ALL": "C",
            })
            return safe

        def git_metadata_path(repo, name):
            output = subprocess.run(
                ["git", "--no-pager", "--literal-pathspecs",
                 "-c", "core.fsmonitor=false", "-c", "core.hooksPath=",
                 "-c", "diff.external=", "rev-parse", "--git-path", name],
                cwd=repo, check=True, capture_output=True, text=True,
                env=git_metadata_env(),
            ).stdout.strip()
            result = pathlib.Path(output)
            if not result.is_absolute():
                result = repo / result
            return pathlib.Path(os.path.abspath(result))

        def index_family_snapshot(repo):
            active = git_metadata_path(repo, "index")
            common = subprocess.run(
                ["git", "--no-pager", "--literal-pathspecs", "rev-parse",
                 "--git-common-dir"],
                cwd=repo, check=True, capture_output=True, text=True,
                env=git_metadata_env(),
            ).stdout.strip()
            common_path = pathlib.Path(common)
            if not common_path.is_absolute():
                common_path = repo / common_path
            common_path = pathlib.Path(os.path.abspath(common_path))
            paths = {active, pathlib.Path(str(active) + ".lock")}
            for directory in {active.parent, common_path}:
                paths.update(directory.glob("sharedindex.*"))
            return tuple(
                (str(path), exact_path_snapshot(path))
                for path in sorted(paths, key=lambda item: str(item))
            )

        manifest_files = []
        for manifest_root in ("AGENTS.md", "CLAUDE.md", ".claude/skills", "templates"):
            absolute = kernel / manifest_root
            if absolute.is_dir():
                manifest_files.extend(
                    item.relative_to(kernel).as_posix()
                    for item in absolute.rglob("*") if item.is_file()
                )
            else:
                manifest_files.append(manifest_root)
        manifest_files = sorted(manifest_files)
        manifest_directories = set()
        for relative in manifest_files:
            parent = pathlib.PurePosixPath(relative).parent
            while parent != pathlib.PurePosixPath("."):
                manifest_directories.add(parent.as_posix())
                parent = parent.parent
        manifest_positions = (
            [(relative, "file") for relative in manifest_files] +
            [(relative, "directory") for relative in sorted(manifest_directories)] +
            [(".claude/speck-next.json", "file"), ("map.md", "file"),
             ("product.md", "product"),
             (".claude/skills/independent-review", "retired")]
        )
        manifest_positions = sorted(set(manifest_positions))
        link_forms = (
            "absolute-sibling", "relative-sibling", "dangling",
            "absolute-in-product", "relative-in-product",
        )
        exercised_forms = set()

        def installed_manifest_digest(root):
            digest = hashlib.sha256()
            for relative in manifest_files:
                digest.update(relative.encode() + b"\0" +
                              (root / relative).read_bytes() + b"\0")
            return digest.hexdigest()

        def v5_marker_bytes(label):
            return (json.dumps({
                "name": "speck-next", "version": "5.4.1", "commit": label,
                "installedAt": "2026-01-02T03:04:05.000Z",
            }, indent=2) + "\n").encode()

        def seed_manifest_link_case(index, relative, expected_kind):
            slug = re.sub(r"[^a-z0-9]+", "-", relative.lower()).strip("-") or "root"
            repo = fresh_repo(f"manifest-{index:02d}-{slug}")
            form = link_forms[index % len(link_forms)]
            if relative in {".claude", ".claude/speck-next.json"} and form == "dangling":
                form = "absolute-sibling"
            if relative == "map.md":
                form = "dangling"
            if relative == "product.md" and form == "dangling":
                form = "relative-sibling"
            exercised_forms.add(form)
            target_path = repo / relative
            target_path.parent.mkdir(parents=True, exist_ok=True)
            prior_label = f"manifest-{index:02d}"
            if relative != ".claude" and relative != ".claude/speck-next.json":
                write_file(repo, ".claude/speck-next.json", v5_marker_bytes(prior_label).decode())
            if relative != "product.md":
                write_file(repo, "product.md", f"# Manifest product {index}\n")
            write_file(repo, "owner/tracked.txt", f"tracked owner text {index}\n")
            (repo / "owner/tracked.bin").write_bytes(bytes((0, 255, index % 251, 10)))

            source = None
            link_target = None
            if form == "dangling":
                missing = repo / "owner-link-sources" / f"missing-{index}"
                missing.parent.mkdir(parents=True, exist_ok=True)
                link_target = os.path.relpath(missing, target_path.parent)
            else:
                internal = "in-product" in form
                source = ((repo / "owner-link-sources") if internal else
                          (base / "manifest-referents")) / f"{index:02d}-{slug}"
                source.parent.mkdir(parents=True, exist_ok=True)
                if expected_kind in {"directory", "retired"}:
                    source.mkdir()
                    write_file(source, "owner-sentinel.txt", f"referent directory {index}\n")
                    if relative == ".claude":
                        write_file(source, "speck-next.json", v5_marker_bytes(prior_label).decode())
                else:
                    if relative == ".claude/speck-next.json":
                        source.write_bytes(v5_marker_bytes(prior_label))
                    elif relative == "product.md":
                        source.write_text(f"# Linked manifest product {index}\n")
                    else:
                        source.write_bytes(f"referent file {index}\n".encode() + b"\x00\xff")
                link_target = (str(source.resolve()) if form.startswith("absolute-") else
                               os.path.relpath(source, target_path.parent))
            os.symlink(link_target, target_path)
            commit_fixture(repo, f"manifest link baseline {index}")
            write_file(repo, "owner/untracked.txt", f"untracked owner text {index}\n")
            (repo / "owner/untracked.bin").write_bytes(bytes((255, 0, index % 251, 13, 10)))
            return repo, form, source, prior_label

        generated_position_results = []
        for index, (relative, expected_kind) in enumerate(manifest_positions):
            repo, form, source, prior_label = seed_manifest_link_case(
                index, relative, expected_kind
            )
            target_path = repo / relative
            source_before = exact_path_snapshot(source) if source is not None else None
            selected_before = repo_baseline(repo)
            original_product = (source.read_bytes() if relative == "product.md" and source else
                                (repo / "product.md").read_bytes())
            first = run_cli(kernel, "upgrade", repo)

            if expected_kind == "product":
                failed_cleanly = (
                    first.returncode != 0 and "product.md exists but is not a regular file" in first.stderr and
                    "Installed Speck Next" not in first.stdout and "Upgraded Speck Next" not in first.stdout and
                    "Working-tree changes across" not in first.stdout and
                    "Complete installed-surface" not in first.stdout and
                    "commit the upgrade" not in (first.stdout + first.stderr) and
                    not has_resume_instruction(first.stdout + first.stderr) and
                    "Error:" not in first.stderr and " at " not in first.stderr and
                    repo_unchanged(repo, selected_before) and not transaction_dirt(repo) and
                    (source is None or exact_path_snapshot(source) == source_before)
                )
                target_path.unlink()
                target_path.write_bytes(original_product)
                first = run_cli(kernel, "upgrade", repo)
                expected_disclosure = True
            else:
                failed_cleanly = True
                expected_disclosure = (
                    (f"Removed stale linked method path {relative};" in first.stdout)
                    if expected_kind == "retired" else
                    (f"Localized linked path {relative} into this repository;" in first.stdout)
                )

            target_kind_ok = (
                (expected_kind == "retired" and not target_path.exists() and not target_path.is_symlink()) or
                (expected_kind == "directory" and target_path.is_dir() and not target_path.is_symlink()) or
                (expected_kind in {"file", "product"} and target_path.is_file() and
                 not target_path.is_symlink())
            )
            source_after_first = exact_path_snapshot(source) if source is not None else None
            first_success = (
                first.returncode == 0 and not first.stderr and expected_disclosure and target_kind_ok and
                installed_manifest_digest(repo) == surface_digest and
                marker_ok(repo, source_checkout, surface_digest, ASSESSMENT_RECORD) and
                (repo / "product.md").read_bytes().startswith(original_product) and
                (repo / "owner/tracked.txt").read_text() == f"tracked owner text {index}\n" and
                (repo / "owner/tracked.bin").read_bytes() == bytes((0, 255, index % 251, 10)) and
                (repo / "owner/untracked.txt").read_text() == f"untracked owner text {index}\n" and
                (repo / "owner/untracked.bin").read_bytes() == bytes((255, 0, index % 251, 13, 10)) and
                (source is None or source_after_first == source_before) and
                not transaction_dirt(repo)
            )
            before_retry = repo_baseline(repo)
            retry = run_cli(kernel, "upgrade", repo)
            retry_stable = (
                retry.returncode == 0 and not retry.stderr and repo_unchanged(repo, before_retry) and
                (source is None or exact_path_snapshot(source) == source_before) and
                not transaction_dirt(repo)
            )
            passed = failed_cleanly and first_success and retry_stable
            generated_position_results.append((relative, form, passed))
            label = (f"manifest-derived {form} link at {relative} refuses untouched, then its "
                     "repaired upgrade retries byte-stably" if expected_kind == "product" else
                     f"manifest-derived {form} link at {relative} is contained and its "
                     "successful upgrade retries byte-stably")
            results.append((label, passed))

        results.append((
            "manifest-derived generator covers every copied leaf, ancestor, marker, map, migrated product, stale path, and link form",
            len(manifest_files) == 17 and len(manifest_directories) == 11 and
            len(generated_position_results) == len(manifest_positions) == 32 and
            {relative for relative, _, _ in generated_position_results} ==
            {relative for relative, _ in manifest_positions} and
            exercised_forms == set(link_forms),
        ))

        source_adapter = kernel / ".agents/skills/speck-next"
        results.append((
            "the direct checkout exposes the five canonical skills through one namespaced Codex adapter",
            source_adapter.is_symlink() and
            os.readlink(source_adapter) == "../../.claude/skills" and
            source_adapter.lstat().st_size == len(b"../../.claude/skills") and
            source_adapter.resolve() == (kernel / ".claude/skills").resolve() and
            len(list((kernel / ".claude/skills").glob("*/SKILL.md"))) == 5,
        ))

        truthful_fresh = fresh_repo("truthful-fresh-list")
        truthful_run = run_cli(kernel, "install", truthful_fresh)
        actual_fresh_paths = sorted(
            item.relative_to(truthful_fresh).as_posix()
            for item in truthful_fresh.rglob("*")
            if ".git" not in item.relative_to(truthful_fresh).parts and
            (item.is_file() or item.is_symlink())
        )
        reported_fresh_count, reported_fresh_paths = install_report(truthful_run)
        fresh_adapter = codex_adapter(truthful_fresh)
        fresh_bytes = sum(
            item.lstat().st_size for item in truthful_fresh.rglob("*")
            if ".git" not in item.relative_to(truthful_fresh).parts and
            (item.is_file() or item.is_symlink())
        )
        results.append((
            "fresh install generates one Codex adapter and its exact count, paths, and bytes match the physical product files",
            truthful_run.returncode == 0 and not truthful_run.stderr and
            reported_fresh_count == len(actual_fresh_paths) and
            reported_fresh_paths == actual_fresh_paths and
            ".claude/speck-next.json" in reported_fresh_paths and
            fresh_adapter is not None and fresh_adapter.relative_to(truthful_fresh).as_posix() in reported_fresh_paths and
            reported_fresh_paths.count(fresh_adapter.relative_to(truthful_fresh).as_posix()) == 1 and
            not any(path.startswith(".agents/skills/speck-next/") for path in reported_fresh_paths) and
            fresh_adapter.lstat().st_size == len(b"../../.claude/skills") and
            fresh_adapter.resolve() == (truthful_fresh / ".claude/skills").resolve() and
            fresh_adapter.resolve().is_relative_to(truthful_fresh.resolve()) and
            len(actual_fresh_paths) == 20 and fresh_bytes == 85618,
        ))

        whole_alias = fresh_repo("whole-root-codex-alias")
        write_file(whole_alias, ".claude/skills/owner-skill/SKILL.md",
                   "---\nname: owner-skill\ndescription: owner\n---\n")
        (whole_alias / ".agents").mkdir()
        os.symlink("../.claude/skills", whole_alias / ".agents/skills")
        whole_alias_before = exact_path_snapshot(whole_alias / ".agents/skills")
        whole_alias_run = run_cli(kernel, "install", whole_alias)
        whole_count, whole_paths = install_report(whole_alias_run)
        whole_retry_before = repo_baseline(whole_alias)
        whole_retry = run_cli(kernel, "upgrade", whole_alias)
        results.append((
            "an exact whole-root canonical Codex alias is preserved byte-for-byte and counted once without a recursive child",
            whole_alias_run.returncode == 0 and not whole_alias_run.stderr and
            exact_path_snapshot(whole_alias / ".agents/skills") == whole_alias_before and
            (whole_alias / ".agents/skills").resolve() == (whole_alias / ".claude/skills").resolve() and
            whole_paths.count(".agents/skills") == 1 and
            not any(path.startswith(".agents/skills/") for path in whole_paths) and
            whole_count == len(whole_paths) and
            whole_retry.returncode == 0 and not whole_retry.stderr and
            repo_unchanged(whole_alias, whole_retry_before),
        ))

        occupied_adapter = fresh_repo("occupied-codex-adapter")
        write_file(occupied_adapter, ".agents/skills/owner-skill/SKILL.md",
                   "---\nname: owner-skill\ndescription: owner\n---\n")
        write_file(occupied_adapter, ".agents/skills/speck-next/owner.bin", "owner adapter name\n")
        occupied_before = exact_path_snapshot(occupied_adapter / ".agents/skills/speck-next")
        owner_skill_before = exact_path_snapshot(occupied_adapter / ".agents/skills/owner-skill")
        occupied_run = run_cli(kernel, "install", occupied_adapter)
        occupied_retry_before = repo_baseline(occupied_adapter)
        occupied_retry = run_cli(kernel, "upgrade", occupied_adapter)
        results.append((
            "an occupied adapter name stays owner-exact while one suffixed adapter installs and retries byte-stably",
            occupied_run.returncode == 0 and not occupied_run.stderr and
            exact_path_snapshot(occupied_adapter / ".agents/skills/speck-next") == occupied_before and
            exact_path_snapshot(occupied_adapter / ".agents/skills/owner-skill") == owner_skill_before and
            (occupied_adapter / ".agents/skills/speck-next-2").is_symlink() and
            os.readlink(occupied_adapter / ".agents/skills/speck-next-2") == "../../.claude/skills" and
            occupied_retry.returncode == 0 and not occupied_retry.stderr and
            repo_unchanged(occupied_adapter, occupied_retry_before),
        ))

        collision_file = fresh_repo("occupied-codex-adapter-file")
        (collision_file / ".agents/skills").mkdir(parents=True)
        (collision_file / ".agents/skills/speck-next").write_bytes(b"owner file\x00\xff")
        collision_file_before = exact_path_snapshot(collision_file / ".agents/skills/speck-next")
        collision_file_run = run_cli(kernel, "install", collision_file)
        results.append((
            "a wrong-kind file at the preferred adapter name stays exact while speck-next-2 becomes the adapter",
            collision_file_run.returncode == 0 and not collision_file_run.stderr and
            exact_path_snapshot(collision_file / ".agents/skills/speck-next") == collision_file_before and
            codex_adapter_name(collision_file) == "speck-next-2" and
            stable_retry(collision_file, collision_file_run),
        ))

        collision_case = fresh_repo("occupied-codex-adapter-case-alias")
        write_file(collision_case, ".agents/skills/Speck-Next/OWNER.bin", "owner case alias\n")
        case_alias_before = exact_path_snapshot(collision_case / ".agents/skills/Speck-Next")
        case_aliases_preferred = (collision_case / ".agents/skills/speck-next").exists()
        collision_case_run = run_cli(kernel, "install", collision_case)
        expected_case_name = "speck-next-2" if case_aliases_preferred else "speck-next"
        results.append((
            "a filesystem case-alias of the preferred name stays owner-exact and forces the first logically absent adapter name",
            collision_case_run.returncode == 0 and not collision_case_run.stderr and
            exact_path_snapshot(collision_case / ".agents/skills/Speck-Next") == case_alias_before and
            codex_adapter_name(collision_case) == expected_case_name and
            "Preserved incompatible path .agents/skills/speck-next" not in collision_case_run.stdout and
            stable_retry(collision_case, collision_case_run),
        ))

        reusable_case_link = fresh_repo("reusable-case-variant-codex-adapter")
        write_file(reusable_case_link, ".claude/skills/owner-skill/SKILL.md",
                   "---\nname: owner-skill\ndescription: owner\n---\n")
        (reusable_case_link / ".agents/skills").mkdir(parents=True)
        reusable_case_target = "../../.claude/skills/."
        reusable_case_path = reusable_case_link / ".agents/skills/Speck-Next"
        os.symlink(reusable_case_target, reusable_case_path)
        reusable_case_before = exact_path_snapshot(reusable_case_path)
        reusable_owner_before = exact_path_snapshot(reusable_case_link / ".claude/skills/owner-skill")
        reusable_case_run = run_cli(kernel, "install", reusable_case_link)
        reusable_case_count, reusable_case_paths = install_report(reusable_case_run)
        reusable_case_names = sorted(
            item.name for item in (reusable_case_link / ".agents/skills").iterdir()
            if re.fullmatch(r"speck-next(?:-(?:[2-9]|[1-9][0-9]+))?", item.name, re.I)
        )
        reusable_case_retry_before = repo_baseline(reusable_case_link)
        reusable_case_retry = run_cli(kernel, "upgrade", reusable_case_link)
        results.append((
            "a case-variant child link already resolving to canonical skills is reused byte-for-byte without duplicate discovery",
            reusable_case_run.returncode == 0 and not reusable_case_run.stderr and
            exact_path_snapshot(reusable_case_path) == reusable_case_before and
            os.readlink(reusable_case_path) == reusable_case_target and
            reusable_case_path.resolve() == (reusable_case_link / ".claude/skills").resolve() and
            exact_path_snapshot(reusable_case_link / ".claude/skills/owner-skill") == reusable_owner_before and
            reusable_case_names == ["Speck-Next"] and
            reusable_case_paths.count(".agents/skills/Speck-Next") == 1 and
            reusable_case_count == len(reusable_case_paths) and
            reusable_case_retry.returncode == 0 and not reusable_case_retry.stderr and
            repo_unchanged(reusable_case_link, reusable_case_retry_before),
        ))

        collision_link = fresh_repo("occupied-codex-adapter-link")
        collision_link_outside = base / "occupied-codex-adapter-link-target"
        collision_link_outside.mkdir()
        write_file(collision_link_outside, "owner.bin", "owner linked adapter\n")
        (collision_link / ".agents/skills").mkdir(parents=True)
        os.symlink(collision_link_outside, collision_link / ".agents/skills/speck-next")
        collision_link_before = exact_path_snapshot(collision_link / ".agents/skills/speck-next")
        collision_link_outside_before = exact_path_snapshot(collision_link_outside)
        collision_link_run = run_cli(kernel, "install", collision_link)
        results.append((
            "a noncanonical linked skill at the preferred adapter name and its referent stay exact while speck-next-2 installs",
            collision_link_run.returncode == 0 and not collision_link_run.stderr and
            exact_path_snapshot(collision_link / ".agents/skills/speck-next") == collision_link_before and
            exact_path_snapshot(collision_link_outside) == collision_link_outside_before and
            codex_adapter_name(collision_link) == "speck-next-2" and
            stable_retry(collision_link, collision_link_run),
        ))

        collision_dangling = fresh_repo("occupied-codex-adapter-dangling")
        (collision_dangling / ".agents/skills").mkdir(parents=True)
        os.symlink("../../../missing-owner-skill", collision_dangling / ".agents/skills/speck-next")
        collision_dangling_before = exact_path_snapshot(collision_dangling / ".agents/skills/speck-next")
        collision_dangling_run = run_cli(kernel, "install", collision_dangling)
        results.append((
            "a dangling owner link at the preferred adapter name stays exact while speck-next-2 installs",
            collision_dangling_run.returncode == 0 and not collision_dangling_run.stderr and
            exact_path_snapshot(collision_dangling / ".agents/skills/speck-next") == collision_dangling_before and
            codex_adapter_name(collision_dangling) == "speck-next-2" and
            stable_retry(collision_dangling, collision_dangling_run),
        ))

        collision_sequence = fresh_repo("occupied-codex-adapter-sequence")
        write_file(collision_sequence, ".agents/skills/speck-next/owner.txt", "owner one\n")
        write_file(collision_sequence, ".agents/skills/speck-next-2/owner.txt", "owner two\n")
        collision_one_before = exact_path_snapshot(collision_sequence / ".agents/skills/speck-next")
        collision_two_before = exact_path_snapshot(collision_sequence / ".agents/skills/speck-next-2")
        collision_sequence_run = run_cli(kernel, "install", collision_sequence)
        results.append((
            "the first absent deterministic suffix is selected without changing earlier occupied names",
            collision_sequence_run.returncode == 0 and not collision_sequence_run.stderr and
            codex_adapter_name(collision_sequence) == "speck-next-3" and
            exact_path_snapshot(collision_sequence / ".agents/skills/speck-next") == collision_one_before and
            exact_path_snapshot(collision_sequence / ".agents/skills/speck-next-2") == collision_two_before and
            stable_retry(collision_sequence, collision_sequence_run),
        ))

        collision_ten = fresh_repo("existing-codex-adapter-ten")
        (collision_ten / ".agents/skills").mkdir(parents=True)
        os.symlink("../../.claude/skills", collision_ten / ".agents/skills/speck-next-10")
        collision_ten_before = exact_path_snapshot(collision_ten / ".agents/skills/speck-next-10")
        collision_ten_run = run_cli(kernel, "install", collision_ten)
        results.append((
            "an existing exact multi-digit suffixed adapter is reused before an absent preferred name",
            collision_ten_run.returncode == 0 and not collision_ten_run.stderr and
            exact_path_snapshot(collision_ten / ".agents/skills/speck-next-10") == collision_ten_before and
            not (collision_ten / ".agents/skills/speck-next").exists() and
            codex_adapter_name(collision_ten) == "speck-next-10" and
            stable_retry(collision_ten, collision_ten_run),
        ))

        linked_agents = fresh_repo("linked-agents-ancestor")
        write_file(linked_agents, ".claude/speck-next.json",
                   v5_marker_bytes("linked-agents-fixture").decode())
        write_file(linked_agents, "product.md", "# Linked agents product\n")
        linked_agents_outside = base / "linked-agents-ancestor-target"
        linked_agents_private = "PRIVATE-LINKED-AGENTS-OWNER-3be4263f"
        write_file(linked_agents_outside, "skills/owner-skill/SKILL.md",
                   f"---\nname: owner-skill\ndescription: {linked_agents_private}\n---\n")
        (linked_agents_outside / "private.bin").write_bytes(b"\x00\xfflinked agents\r\n")
        os.symlink(linked_agents_outside, linked_agents / ".agents")
        commit_fixture(linked_agents, "tracked linked .agents fixture")
        linked_agents_outside_before = exact_path_snapshot(linked_agents_outside)
        linked_agents_run = run_cli(kernel, "upgrade", linked_agents)
        linked_agents_output = linked_agents_run.stdout + linked_agents_run.stderr
        results.append((
            "a tracked linked .agents ancestor becomes local transactionally with complete topology reporting and no owner-skill disclosure",
            linked_agents_run.returncode == 0 and not linked_agents_run.stderr and
            "Localized linked path .agents" in linked_agents_run.stdout and
            re.search(r"^[ MADRCU?!]{2} \.agents$", linked_agents_run.stdout, re.MULTILINE) is not None and
            "diff --git a/.agents b/.agents" in linked_agents_run.stdout and
            (linked_agents / ".agents").is_dir() and not (linked_agents / ".agents").is_symlink() and
            linked_agents_private in (linked_agents / ".agents/skills/owner-skill/SKILL.md").read_text() and
            codex_adapter_name(linked_agents) == "speck-next" and
            exact_path_snapshot(linked_agents_outside) == linked_agents_outside_before and
            ".agents/skills/speck-next" in linked_agents_run.stdout and
            linked_agents_private not in linked_agents_output and
            "owner-skill" not in linked_agents_output and "private.bin" not in linked_agents_output and
            stable_retry(linked_agents, linked_agents_run) and
            exact_path_snapshot(linked_agents_outside) == linked_agents_outside_before,
        ))

        linked_skills = fresh_repo("linked-agents-skills-ancestor")
        write_file(linked_skills, ".claude/speck-next.json",
                   v5_marker_bytes("linked-agents-skills-fixture").decode())
        write_file(linked_skills, "product.md", "# Linked agents skills product\n")
        linked_skills_outside = base / "linked-agents-skills-ancestor-target"
        linked_skills_private = "PRIVATE-LINKED-SKILLS-OWNER-d7523d2c"
        write_file(linked_skills_outside, "owner-skill/SKILL.md",
                   f"---\nname: owner-skill\ndescription: {linked_skills_private}\n---\n")
        (linked_skills_outside / "private.bin").write_bytes(b"\xfe\x00linked skills\r\n")
        (linked_skills / ".agents").mkdir()
        os.symlink(linked_skills_outside, linked_skills / ".agents/skills")
        commit_fixture(linked_skills, "tracked linked .agents skills fixture")
        linked_skills_outside_before = exact_path_snapshot(linked_skills_outside)
        linked_skills_run = run_cli(kernel, "upgrade", linked_skills)
        linked_skills_output = linked_skills_run.stdout + linked_skills_run.stderr
        results.append((
            "a tracked linked .agents/skills ancestor becomes local transactionally with complete topology reporting and no owner-skill disclosure",
            linked_skills_run.returncode == 0 and not linked_skills_run.stderr and
            "Localized linked path .agents/skills" in linked_skills_run.stdout and
            re.search(r"^[ MADRCU?!]{2} \.agents/skills$", linked_skills_run.stdout, re.MULTILINE) is not None and
            "diff --git a/.agents/skills b/.agents/skills" in linked_skills_run.stdout and
            (linked_skills / ".agents/skills").is_dir() and not (linked_skills / ".agents/skills").is_symlink() and
            linked_skills_private in (linked_skills / ".agents/skills/owner-skill/SKILL.md").read_text() and
            codex_adapter_name(linked_skills) == "speck-next" and
            exact_path_snapshot(linked_skills_outside) == linked_skills_outside_before and
            ".agents/skills/speck-next" in linked_skills_run.stdout and
            linked_skills_private not in linked_skills_output and
            "owner-skill" not in linked_skills_output and "private.bin" not in linked_skills_output and
            stable_retry(linked_skills, linked_skills_run) and
            exact_path_snapshot(linked_skills_outside) == linked_skills_outside_before,
        ))

        linked_agents_alias = fresh_repo("linked-agents-with-whole-root-alias")
        write_file(linked_agents_alias, ".claude/speck-next.json",
                   v5_marker_bytes("linked-agents-alias-fixture").decode())
        write_file(linked_agents_alias, ".claude/skills/legacy/SKILL.md",
                   "---\nname: legacy\ndescription: legacy\n---\n")
        write_file(linked_agents_alias, "product.md", "# Linked agents alias product\n")
        linked_agents_alias_outside = base / "linked-agents-with-whole-root-alias-target"
        linked_agents_alias_outside.mkdir()
        linked_agents_alias_private = "PRIVATE-LINKED-AGENTS-ALIAS-228d71f0"
        write_file(linked_agents_alias_outside, "owner-skill/SKILL.md",
                   f"---\nname: outside-owner\ndescription: {linked_agents_alias_private}\n---\n")
        os.symlink(str((linked_agents_alias / ".claude/skills").resolve()),
                   linked_agents_alias_outside / "skills")
        os.symlink(linked_agents_alias_outside, linked_agents_alias / ".agents")
        commit_fixture(linked_agents_alias, "tracked linked .agents with canonical child alias")
        linked_agents_alias_outside_before = exact_path_snapshot(linked_agents_alias_outside)
        linked_agents_alias_child_before = exact_path_snapshot(linked_agents_alias / ".agents/skills")
        linked_agents_alias_run = run_cli(kernel, "upgrade", linked_agents_alias)
        linked_agents_alias_output = linked_agents_alias_run.stdout + linked_agents_alias_run.stderr
        results.append((
            "a linked .agents parent localizes while its exact whole-root canonical child alias stays byte-identical and singular",
            linked_agents_alias_run.returncode == 0 and not linked_agents_alias_run.stderr and
            "Localized linked path .agents" in linked_agents_alias_run.stdout and
            re.search(r"^[ MADRCU?!]{2} \.agents$", linked_agents_alias_run.stdout, re.MULTILINE) is not None and
            "diff --git a/.agents b/.agents" in linked_agents_alias_run.stdout and
            (linked_agents_alias / ".agents").is_dir() and not (linked_agents_alias / ".agents").is_symlink() and
            exact_path_snapshot(linked_agents_alias / ".agents/skills") == linked_agents_alias_child_before and
            (linked_agents_alias / ".agents/skills").resolve() ==
                (linked_agents_alias / ".claude/skills").resolve() and
            not (linked_agents_alias / ".agents/skills/speck-next").exists() and
            exact_path_snapshot(linked_agents_alias_outside) == linked_agents_alias_outside_before and
            linked_agents_alias_private not in linked_agents_alias_output and
            "owner-skill" not in linked_agents_alias_output and
            stable_retry(linked_agents_alias, linked_agents_alias_run) and
            exact_path_snapshot(linked_agents_alias_outside) == linked_agents_alias_outside_before and
            not transaction_dirt(linked_agents_alias),
        ))

        carried_map = fresh_repo("carried-owner-map")
        write_file(carried_map, "map.md", "# Existing owner map\n")
        os.chmod(carried_map / "map.md", 0o600)
        carried_map_run = run_cli(kernel, "install", carried_map)
        actual_carried_paths = sorted(
            item.relative_to(carried_map).as_posix()
            for item in carried_map.rglob("*")
            if ".git" not in item.relative_to(carried_map).parts and
            (item.is_file() or item.is_symlink())
        )
        carried_count, carried_paths = install_report(carried_map_run)
        results.append((
            "a pre-existing valid map is carried forward byte-for-byte and included in the exact install list",
            carried_map_run.returncode == 0 and not carried_map_run.stderr and
            (carried_map / "map.md").read_text() == "# Existing owner map\n" and
            (carried_map / "map.md").stat().st_mode & 0o777 == 0o600 and
            carried_count == len(actual_carried_paths) and carried_paths == actual_carried_paths and
            "map.md" in carried_paths,
        ))

        for method_file in ("AGENTS.md", "CLAUDE.md"):
            slug = method_file.lower().replace(".", "-")
            aliased_map = fresh_repo(f"carried-map-aliases-{slug}")
            owner_map_bytes = f"# Owner map formerly at {method_file}\n".encode()
            seed_upgrade_repo(
                aliased_map, "5.4.1", f"carried-map-{slug}-fixture",
                f"# {method_file} alias product\n",
                {method_file: owner_map_bytes.decode()},
            )
            os.chmod(aliased_map / method_file, 0o600)
            os.symlink(method_file, aliased_map / "map.md")
            commit_fixture(aliased_map, f"link carried map to {method_file}")
            aliased_map_run = run_cli(kernel, "upgrade", aliased_map)
            expected_disclosure = (
                "Localized carried map.md into a local regular file; it previously pointed to "
                f'"{method_file}", and its logical contents and mode were made local before the '
                f"overlapping method path {method_file} changed."
            )
            results.append((
                f"the carried map alias control localizes map.md -> {method_file} before the method root changes and retries byte-stably",
                aliased_map_run.returncode == 0 and not aliased_map_run.stderr and
                expected_disclosure in aliased_map_run.stdout and
                (aliased_map / "map.md").is_file() and
                not (aliased_map / "map.md").is_symlink() and
                (aliased_map / "map.md").read_bytes() == owner_map_bytes and
                (aliased_map / "map.md").stat().st_mode & 0o777 == 0o600 and
                (aliased_map / method_file).read_bytes() == (kernel / method_file).read_bytes() and
                stable_retry(aliased_map, aliased_map_run),
            ))

        outside_map = base / "carried-map-outside.md"
        outside_map.write_bytes(b"# Outside owner map\n\x00\xff")
        linked_outside_map = fresh_repo("carried-map-outside")
        seed_upgrade_repo(
            linked_outside_map, "5.4.1", "carried-map-outside-fixture",
            "# Outside-link product\n",
        )
        os.symlink(outside_map, linked_outside_map / "map.md")
        commit_fixture(linked_outside_map, "link carried map outside product")
        outside_map_before = exact_path_snapshot(outside_map)
        outside_map_target = os.readlink(linked_outside_map / "map.md")
        linked_outside_run = run_cli(kernel, "upgrade", linked_outside_map)
        results.append((
            "a carried map linked outside planned roots stays linked and byte-identical through a stable retry",
            linked_outside_run.returncode == 0 and not linked_outside_run.stderr and
            (linked_outside_map / "map.md").is_symlink() and
            os.readlink(linked_outside_map / "map.md") == outside_map_target and
            exact_path_snapshot(outside_map) == outside_map_before and
            "map.md" in linked_outside_run.stdout and
            stable_retry(linked_outside_map, linked_outside_run) and
            exact_path_snapshot(outside_map) == outside_map_before,
        ))

        outside_skills = base / "outside-skills"
        outside_skills.mkdir()
        write_file(outside_skills, "custom/sentinel.txt", "outside skills stay\n")
        linked_skills = fresh_repo("linked-skills")
        (linked_skills / ".claude").mkdir()
        os.symlink(outside_skills, linked_skills / ".claude/skills")
        outside_before = snapshot_digest(outside_skills)
        linked_skills_run = run_cli(kernel, "install", linked_skills)
        results.append((
            "absolute .claude/skills link localizes once, preserves its referent, reports carried files, and retries byte-stably",
            linked_skills_run.returncode == 0 and not linked_skills_run.stderr and
            'Localized linked path .claude/skills into this repository;' in linked_skills_run.stdout and
            ".claude/skills/custom/sentinel.txt" in linked_skills_run.stdout and
            snapshot_digest(outside_skills) == outside_before and
            (linked_skills / ".claude/skills").is_dir() and
            not (linked_skills / ".claude/skills").is_symlink() and
            (linked_skills / ".claude/skills/custom/sentinel.txt").read_text() == "outside skills stay\n" and
            stable_retry(linked_skills, linked_skills_run),
        ))

        relative_templates = fresh_repo("relative-templates")
        relative_outside = base / "relative-template-source"
        relative_outside.mkdir()
        write_file(relative_outside, "custom.txt", "relative referent\n")
        os.symlink("../relative-template-source", relative_templates / "templates")
        relative_before = snapshot_digest(relative_outside)
        relative_run = run_cli(kernel, "install", relative_templates)
        results.append((
            "relative templates link becomes local without changing its sibling referent",
            relative_run.returncode == 0 and not relative_run.stderr and
            'Localized linked path templates into this repository;' in relative_run.stdout and
            snapshot_digest(relative_outside) == relative_before and
            not (relative_templates / "templates").is_symlink() and
            (relative_templates / "templates/custom.txt").read_text() == "relative referent\n" and
            "templates/custom.txt" in relative_run.stdout,
        ))

        grouped_claude = fresh_repo("grouped-claude-path")
        grouped_outside = base / "grouped-claude-source"
        (grouped_outside / "skills/custom").mkdir(parents=True)
        write_file(grouped_outside, "custom.txt", "grouped custom\n")
        write_file(grouped_outside, "skills/custom/note.txt", "custom skill\n")
        write_file(grouped_outside, "speck-next.json", '{"old": true}\n')
        os.symlink(grouped_outside, grouped_claude / ".claude")
        grouped_before = snapshot_digest(grouped_outside)
        grouped_run = run_cli(kernel, "install", grouped_claude)
        results.append((
            "grouped .claude link localizes as one root, forces a local marker, and reports every carried leaf",
            grouped_run.returncode == 0 and not grouped_run.stderr and
            'Localized linked path .claude into this repository;' in grouped_run.stdout and
            ".claude/custom.txt" in grouped_run.stdout and
            ".claude/skills/custom/note.txt" in grouped_run.stdout and
            snapshot_digest(grouped_outside) == grouped_before and
            not (grouped_claude / ".claude").is_symlink() and
            not (grouped_claude / ".claude/speck-next.json").is_symlink() and
            marker(grouped_claude)["version"] == CURRENT_VERSION,
        ))

        non_dir_link = fresh_repo("linked-non-directory")
        outside_file = base / "linked-template-file"
        outside_file.write_bytes(b"outside file bytes\x00\xff")
        os.symlink(outside_file, non_dir_link / "templates")
        outside_file_before = (outside_file.read_bytes(), outside_file.lstat().st_mode)
        non_dir_run = run_cli(kernel, "install", non_dir_link)
        results.append((
            "a directory destination linked to a regular file localizes and discloses without touching the file",
            non_dir_run.returncode == 0 and not non_dir_run.stderr and
            'Localized linked path templates into this repository;' in non_dir_run.stdout and
            (outside_file.read_bytes(), outside_file.lstat().st_mode) == outside_file_before and
            (non_dir_link / "templates").is_dir() and not (non_dir_link / "templates").is_symlink(),
        ))

        dangling = fresh_repo("dangling-links")
        (dangling / ".claude").mkdir()
        os.symlink("../missing-skills", dangling / ".claude/skills")
        os.symlink("missing-templates", dangling / "templates")
        dangling_run = run_cli(kernel, "install", dangling)
        results.append((
            "dangling grouped and direct links become local without raw path errors",
            dangling_run.returncode == 0 and not dangling_run.stderr and
            dangling_run.stdout.count("Localized linked path") == 2 and
            (dangling / ".claude/skills").is_dir() and not (dangling / ".claude/skills").is_symlink() and
            (dangling / "templates").is_dir() and not (dangling / "templates").is_symlink(),
        ))

        self_link = fresh_repo("templates-self-link")
        os.symlink(".", self_link / "templates")
        self_before = repo_baseline(self_link)
        self_run = run_cli(kernel, "install", self_link)
        results.append((
            "templates pointing at the product root refuses without recursion or residue",
            calm_failure(self_run) and "points into the selected product" in self_run.stderr and
            repo_unchanged(self_link, self_before) and not transaction_dirt(self_link),
        ))

        internal_link = fresh_repo("internal-owner-link")
        write_file(internal_link, "owner/templates/custom.txt", "internal owner bytes\n")
        os.symlink("owner/templates", internal_link / "templates")
        internal_before = snapshot_digest(internal_link / "owner")
        internal_run = run_cli(kernel, "install", internal_link)
        results.append((
            "an in-product link outside the method surface localizes without changing its source",
            internal_run.returncode == 0 and not internal_run.stderr and
            snapshot_digest(internal_link / "owner") == internal_before and
            (internal_link / "templates/custom.txt").read_text() == "internal owner bytes\n" and
            not (internal_link / "templates").is_symlink(),
        ))

        cross_root = fresh_repo("cross-method-root-link")
        write_file(cross_root, ".claude/skills/owner.txt", "cross-root owner bytes\n")
        os.symlink(".claude/skills", cross_root / "templates")
        cross_root_before = repo_baseline(cross_root)
        cross_root_source_before = exact_path_snapshot(cross_root / ".claude/skills")
        cross_root_run = run_cli(kernel, "install", cross_root)
        results.append((
            "a linked directory overlapping another planned method root refuses before either side changes",
            calm_failure(cross_root_run) and "another planned method root" in cross_root_run.stderr and
            repo_unchanged(cross_root, cross_root_before) and
            exact_path_snapshot(cross_root / ".claude/skills") == cross_root_source_before and
            not transaction_dirt(cross_root),
        ))

        target_repo = fresh_repo("resolved-target")
        target_link = base / "resolved-target-link"
        os.symlink(target_repo, target_link)
        target_link_run = run_cli(kernel, "install", target_link)
        results.append((
            "a command-target link resolves once to the physical product and remains supported",
            target_link_run.returncode == 0 and not target_link_run.stderr and
            (target_repo / "AGENTS.md").is_file() and target_link.is_symlink() and
            str(target_link) in target_link_run.stdout,
        ))

        disposable_kernel = fresh_repo("kernel-self-copy")
        (disposable_kernel / "bin").mkdir()
        shutil.copy2(kernel / "bin/speck-next.js", disposable_kernel / "bin/speck-next.js")
        shutil.copy2(kernel / "package.json", disposable_kernel / "package.json")
        kernel_link = base / "kernel-target-link"
        os.symlink(disposable_kernel, kernel_link)
        kernel_before = repo_baseline(disposable_kernel)
        kernel_link_run = run_cli(disposable_kernel, "install", kernel_link)
        results.append((
            "a command-target link cannot bypass the kernel-self-install refusal",
            kernel_link_run.returncode != 0 and "kernel repo itself" in kernel_link_run.stderr and
            repo_unchanged(disposable_kernel, kernel_before) and
            not transaction_dirt(disposable_kernel),
        ))

        pack_destination = base / "packed-kernel"
        pack_destination.mkdir()
        pack_run = subprocess.run(
            ["npm", "pack", "--json", "--pack-destination", str(pack_destination)],
            cwd=kernel, capture_output=True, text=True,
        )
        packed_transport_ok = False
        try:
            pack_description = json.loads(pack_run.stdout)
            pack_archive = pack_destination / pack_description[0]["filename"]
            with tarfile.open(pack_archive, "r:gz") as archive:
                packed_names = set(archive.getnames())
                unpacked = base / "unpacked-kernel"
                archive.extractall(unpacked, filter="data")
            packed_kernel = unpacked / "package"
            packed_source_adapter = packed_kernel / ".agents/skills/speck-next"
            packed_product = fresh_repo("packed-product")
            packed_install = run_cli(packed_kernel, "install", packed_product)
            packed_count, packed_paths = install_report(packed_install)
            packed_actual_paths = sorted(
                item.relative_to(packed_product).as_posix()
                for item in packed_product.rglob("*")
                if ".git" not in item.relative_to(packed_product).parts and
                (item.is_file() or item.is_symlink())
            )
            packed_bytes = sum(
                item.lstat().st_size for item in packed_product.rglob("*")
                if ".git" not in item.relative_to(packed_product).parts and
                (item.is_file() or item.is_symlink())
            )
            packed_adapter = codex_adapter(packed_product)
            packed_marker = json.loads((packed_product / ".claude/speck-next.json").read_text())
            packed_transport_ok = (
                pack_run.returncode == 0 and pack_archive.is_file() and
                "package/.agents/skills/speck-next" not in packed_names and
                not packed_source_adapter.exists() and not packed_source_adapter.is_symlink() and
                packed_install.returncode == 0 and not packed_install.stderr and
                packed_count == len(packed_actual_paths) == len(packed_paths) == 20 and
                packed_paths == packed_actual_paths and packed_bytes == 85613 and
                packed_adapter is not None and
                packed_adapter.lstat().st_size == len(b"../../.claude/skills") and
                packed_adapter.resolve() == (packed_product / ".claude/skills").resolve() and
                len(list((packed_product / ".claude/skills").glob("*/SKILL.md"))) == 5 and
                exact_path_snapshot(packed_product / ".claude/skills") ==
                    exact_path_snapshot(packed_kernel / ".claude/skills") and
                packed_marker.get("sourceCheckout") is None and
                stable_retry(packed_product, packed_install, packed_kernel)
            )
        except (FileNotFoundError, IndexError, KeyError, OSError, TypeError, ValueError, tarfile.TarError):
            packed_transport_ok = False
        results.append((
            "npm transport omits the source link while its packed installer generates one adapter with an exact 20-path and 85,613-byte census",
            packed_transport_ok,
        ))

        wrong_claude = fresh_repo("wrong-claude-root")
        (wrong_claude / ".claude").write_bytes(b"owner claude root\x00")
        wrong_claude_run = run_cli(kernel, "install", wrong_claude)
        wrong_claude_preserve = next(wrong_claude.glob(".speck-next-preserved*"), None)
        results.append((
            "a regular .claude root is preserved intact before the local method directory replaces it",
            wrong_claude_run.returncode == 0 and not wrong_claude_run.stderr and
            wrong_claude_preserve is not None and
            any(item.read_bytes() == b"owner claude root\x00" for item in wrong_claude_preserve.iterdir() if item.is_file()) and
            (wrong_claude / ".claude").is_dir() and
            "Preserved incompatible path .claude at" in wrong_claude_run.stdout,
        ))

        wrong_skills = fresh_repo("wrong-skills-ancestor")
        (wrong_skills / ".claude").mkdir()
        (wrong_skills / ".claude/skills").write_bytes(b"owner skills ancestor\x00")
        wrong_skills_run = run_cli(kernel, "install", wrong_skills)
        wrong_skills_preserve = next(wrong_skills.glob(".speck-next-preserved*"), None)
        results.append((
            "a regular .claude/skills ancestor is staged, preserved intact, and replaced calmly",
            wrong_skills_run.returncode == 0 and not wrong_skills_run.stderr and
            wrong_skills_preserve is not None and
            any(item.read_bytes() == b"owner skills ancestor\x00" for item in wrong_skills_preserve.iterdir() if item.is_file()) and
            (wrong_skills / ".claude/skills").is_dir() and
            "Preserved incompatible path .claude/skills at" in wrong_skills_run.stdout,
        ))

        wrong_map = fresh_repo("wrong-generated-map")
        write_file(wrong_map, "map.md/owner.bin", "owner map directory\n")
        wrong_map_run = run_cli(kernel, "install", wrong_map)
        wrong_map_preserve = next(wrong_map.glob(".speck-next-preserved*"), None)
        results.append((
            "a wrong-kind generated map is preserved before a truthful starter map is installed",
            wrong_map_run.returncode == 0 and not wrong_map_run.stderr and
            (wrong_map / "map.md").is_file() and
            (wrong_map / "map.md").read_text().startswith("# Map") and
            wrong_map_preserve is not None and
            any((item / "owner.bin").is_file() for item in wrong_map_preserve.iterdir() if item.is_dir()) and
            "Preserved incompatible path map.md at" in wrong_map_run.stdout,
        ))

        mode_repo = fresh_repo("owner-modes")
        seed_upgrade_repo(
            mode_repo, "5.4.1", "owner-modes-fixture", "# Private product\n",
            {".claude/skills/custom/note.txt": "custom skill\n",
             "templates/custom.txt": "custom template\n"},
        )
        for directory in (mode_repo / ".claude", mode_repo / ".claude/skills", mode_repo / "templates"):
            os.chmod(directory, 0o700)
        os.chmod(mode_repo / "product.md", 0o600)
        mode_run = run_cli(kernel, "upgrade", mode_repo)
        results.append((
            "upgrade preserves owner directory modes and the rewritten product file mode",
            mode_run.returncode == 0 and not mode_run.stderr and
            all((directory.stat().st_mode & 0o777) == 0o700 for directory in
                (mode_repo / ".claude", mode_repo / ".claude/skills", mode_repo / "templates")) and
            (mode_repo / "product.md").stat().st_mode & 0o777 == 0o600,
        ))

        readonly_repo = fresh_repo("readonly-roots")
        write_file(readonly_repo, ".claude/skills/custom/readonly/note.txt", "readonly custom\n")
        for directory in (
            readonly_repo / ".claude/skills/custom/readonly",
            readonly_repo / ".claude/skills/custom",
            readonly_repo / ".claude/skills",
            readonly_repo / ".claude",
        ):
            os.chmod(directory, 0o555)
        readonly_run = run_cli(kernel, "install", readonly_repo)
        results.append((
            "readonly owner directories remain readonly while staging and cleanup stay removable",
            readonly_run.returncode == 0 and not readonly_run.stderr and
            (readonly_repo / ".claude").stat().st_mode & 0o777 == 0o555 and
            (readonly_repo / ".claude/skills").stat().st_mode & 0o777 == 0o555 and
            (readonly_repo / ".claude/skills/custom/readonly/note.txt").read_text() == "readonly custom\n" and
            not transaction_dirt(readonly_repo),
        ))

        preload = base / "path-fault-preload.js"
        preload.write_text(r'''const fs = require("fs");
const path = require("path");
const op = process.env.P8_FAULT || "";
const target = process.env.P8_TARGET ? fs.realpathSync.native(process.env.P8_TARGET) : "";
const log = process.env.P8_FAULT_LOG || "";
const originals = {
  appendFileSync: fs.appendFileSync.bind(fs), copyFileSync: fs.copyFileSync.bind(fs),
  lstatSync: fs.lstatSync.bind(fs), mkdirSync: fs.mkdirSync.bind(fs),
  mkdtempSync: fs.mkdtempSync.bind(fs), readFileSync: fs.readFileSync.bind(fs),
  renameSync: fs.renameSync.bind(fs), rmSync: fs.rmSync.bind(fs), statSync: fs.statSync.bind(fs),
  symlinkSync: fs.symlinkSync.bind(fs), unlinkSync: fs.unlinkSync.bind(fs),
  writeFileSync: fs.writeFileSync.bind(fs),
};
let fired = false;
function text(value) { return String(value); }
function staged(value) { return text(value).includes(".speck-next-transaction-") && text(value).includes(path.sep + "stage" + path.sep); }
function fire(label) {
  if (fired) return false;
  fired = true;
  if (log) originals.appendFileSync(log, label + "\n");
  return true;
}
fs.copyFileSync = function(source, destination, ...rest) {
  if (op === "copy" && staged(destination) && fire("copy")) throw new Error("forced staged copy failure");
  return originals.copyFileSync(source, destination, ...rest);
};
fs.readFileSync = function(file, ...rest) {
  if (op === "digest" && staged(file) && text(file).endsWith(path.sep + "AGENTS.md") && fire("digest"))
    throw new Error("forced staged digest failure");
  return originals.readFileSync(file, ...rest);
};
fs.renameSync = function(source, destination, ...rest) {
  if (op === "record" && staged(source) && log) originals.appendFileSync(log, text(destination) + "\n");
  if (op === "apply" && staged(source) && fire("apply")) throw new Error("forced staged apply failure");
  const result = originals.renameSync(source, destination, ...rest);
  if (op === "adapter-installed-verify" && target &&
      path.resolve(text(destination)) === path.join(target, ".agents") && fire("adapter-installed-verify")) {
    const adapter = path.join(target, ".agents", "skills", "speck-next");
    originals.unlinkSync(adapter);
    originals.symlinkSync("../../../outside-codex-skills", adapter, "dir");
  }
  return result;
};
fs.symlinkSync = function(linkTarget, destination, ...rest) {
  if (staged(destination) && text(destination).endsWith(path.sep + ".agents" + path.sep + "skills" + path.sep + "speck-next")) {
    if (op === "adapter-create" && fire("adapter-create"))
      throw new Error("forced Codex adapter creation failure");
    if (op === "adapter-stage-verify" && fire("adapter-stage-verify"))
      return originals.symlinkSync("../../../outside-codex-skills", destination, ...rest);
  }
  return originals.symlinkSync(linkTarget, destination, ...rest);
};
fs.rmSync = function(file, ...rest) {
  if (op === "cleanup" && text(file).includes(".speck-next-transaction-") &&
      path.basename(text(file)).includes(".speck-next-transaction-") && !fired) {
    const result = originals.rmSync(file, ...rest);
    fire("cleanup");
    throw new Error("forced cleanup completion report failure");
  }
  return originals.rmSync(file, ...rest);
};
fs.writeFileSync = function(file, bytes, ...rest) {
  if (op === "marker" && target && path.resolve(text(file)) === path.join(target, ".claude", "speck-next.json") && fire("marker"))
    throw new Error("forced marker failure");
  return originals.writeFileSync(file, bytes, ...rest);
};
fs.statSync = function(file, ...rest) {
  const result = originals.statSync(file, ...rest);
  if (op === "mount" && target && path.resolve(text(file)) === path.dirname(target)) {
    return new Proxy(result, { get(object, key) {
      if (key === "dev") return Number(object.dev) + 1;
      const value = Reflect.get(object, key, object);
      return typeof value === "function" ? value.bind(object) : value;
    }});
  }
  return result;
};
fs.mkdtempSync = function(prefix, ...rest) {
  if (op === "mount" && log) originals.appendFileSync(log, text(prefix) + "\n");
  return originals.mkdtempSync(prefix, ...rest);
};
''')

        def preload_env(repo, operation, log):
            return {
                "NODE_OPTIONS": f"--require={preload}",
                "P8_FAULT": operation,
                "P8_TARGET": str(repo.resolve()),
                "P8_FAULT_LOG": str(log),
            }

        def full_fault_fixture(name):
            repo = fresh_repo(name)
            prior_label = f"{name}-fixture"
            write_file(repo, ".claude/speck-next.json", v5_marker_bytes(prior_label).decode())
            write_file(repo, ".claude/custom-owner.txt", f"{name} grouped owner text\n")
            write_file(repo, "product.md", f"# {name} product\n")
            write_file(repo, "owner/tracked.txt", f"{name} tracked text\n")
            (repo / "owner/tracked.bin").write_bytes(b"\x00\xfftracked\r\n")
            outside = base / f"{name}-referent"
            outside.mkdir()
            write_file(outside, "sentinel.txt", f"{name} referent text\n")
            (outside / "sentinel.bin").write_bytes(b"\xff\x00referent\n")
            os.symlink(outside, repo / "templates")
            commit_fixture(repo, f"{name} full-state baseline")
            write_file(repo, "owner/untracked.txt", f"{name} untracked text\n")
            (repo / "owner/untracked.bin").write_bytes(b"\xfe\x00untracked\r\n")
            return repo, outside, prior_label

        def full_clean_retry(repo, outside, prior_label, outside_before, index_before):
            clean = run_cli(kernel, "upgrade", repo)
            report_ok = upgrade_report_ok(
                clean, "5.4.1", prior_label, source_checkout, surface_digest,
                NEXT_PENDING_CHANGED,
            )
            clean_ok = (
                report_ok and not clean.stderr and
                exact_path_snapshot(outside) == outside_before and
                (repo / "owner/tracked.bin").read_bytes() == b"\x00\xfftracked\r\n" and
                (repo / "owner/untracked.bin").read_bytes() == b"\xfe\x00untracked\r\n" and
                (repo / ".git/index").read_bytes() == index_before and
                not transaction_dirt(repo)
            )
            stable_ok = stable_retry(repo, clean) if clean_ok else False
            passed = clean_ok and stable_ok and \
                exact_path_snapshot(outside) == outside_before and \
                (repo / ".git/index").read_bytes() == index_before
            return passed

        record_repo = fresh_repo("one-claude-root")
        record_outside = base / "one-claude-source"
        (record_outside / "custom").mkdir(parents=True)
        write_file(record_outside, "custom/note.txt", "record root\n")
        (record_repo / ".claude").mkdir()
        os.symlink(record_outside, record_repo / ".claude/skills")
        record_log = base / "one-claude-renames.log"
        record_run = run_cli_args(kernel, "install", record_repo,
                                  env=preload_env(record_repo, "record", record_log))
        recorded_destinations = record_log.read_text().splitlines() if record_log.exists() else []
        resolved_record_repo = record_repo.resolve()
        claude_destinations = [pathlib.Path(item) for item in recorded_destinations
                               if pathlib.Path(item).is_relative_to(resolved_record_repo / ".claude")]
        results.append((
            "all .claude descendants apply through one .claude transaction root",
            record_run.returncode == 0 and not record_run.stderr and
            claude_destinations == [resolved_record_repo / ".claude"] and
            not any(item == resolved_record_repo / ".claude/skills" for item in claude_destinations),
        ))

        mount_repo = fresh_repo("mount-root-fallback")
        mount_log = base / "mount-root.log"
        mount_run = run_cli_args(kernel, "install", mount_repo,
                                 env=preload_env(mount_repo, "mount", mount_log))
        mount_prefixes = mount_log.read_text().splitlines() if mount_log.exists() else []
        results.append((
            "a product-root mount stages in one hidden in-product transaction and cleans it",
            mount_run.returncode == 0 and not mount_run.stderr and len(mount_prefixes) == 1 and
            pathlib.Path(mount_prefixes[0]).parent == mount_repo.resolve() and
            not transaction_dirt(mount_repo),
        ))

        first_missing = fresh_repo("first-missing-claude-rollback")
        first_missing_outside = base / "first-missing-claude-referent"
        first_missing_outside.mkdir()
        write_file(first_missing_outside, "sentinel.txt", "first missing referent\n")
        os.symlink(first_missing_outside, first_missing / "templates")
        first_missing_before = repo_baseline(first_missing)
        first_missing_source_before = exact_path_snapshot(first_missing_outside)
        first_missing_log = base / "first-missing-marker.log"
        first_missing_run = run_cli_args(
            kernel, "install", first_missing,
            env=preload_env(first_missing, "marker", first_missing_log),
        )
        results.append((
            "a marker failure restores both previously missing .claude and transaction-owned .agents parents to exact absence",
            first_missing_log.exists() and first_missing_log.read_text().splitlines() == ["marker"] and
            calm_failure(first_missing_run) and repo_unchanged(first_missing, first_missing_before) and
            exact_path_snapshot(first_missing_outside) == first_missing_source_before and
            exact_path_snapshot(first_missing / ".claude") == ("missing",) and
            exact_path_snapshot(first_missing / ".agents") == ("missing",) and
            not transaction_dirt(first_missing),
        ))

        for operation in ("adapter-create", "adapter-stage-verify", "adapter-installed-verify"):
            adapter_failure = fresh_repo(operation)
            adapter_failure_before = repo_baseline(adapter_failure)
            adapter_failure_log = base / f"{operation}.log"
            adapter_failed = run_cli_args(
                kernel, "install", adapter_failure,
                env=preload_env(adapter_failure, operation, adapter_failure_log),
            )
            adapter_failure_ok = (
                adapter_failure_log.exists() and
                adapter_failure_log.read_text().splitlines() == [operation] and
                calm_failure(adapter_failed) and
                repo_unchanged(adapter_failure, adapter_failure_before) and
                exact_path_snapshot(adapter_failure / ".agents") == ("missing",) and
                not transaction_dirt(adapter_failure)
            )
            adapter_clean = run_cli(kernel, "install", adapter_failure)
            adapter_retry_ok = not adapter_clean.stderr and stable_retry(adapter_failure, adapter_clean)
            results.append((
                f"injected {operation} failure is atomic with no parent residue before a clean and stable adapter retry",
                adapter_failure_ok and adapter_retry_ok,
            ))

        for operation in ("copy", "digest", "apply", "marker"):
            repo, outside, prior_label = full_fault_fixture(f"fault-{operation}")
            repo_before = repo_baseline(repo)
            outside_before = exact_path_snapshot(outside)
            index_before = (repo / ".git/index").read_bytes()
            fault_log = base / f"fault-{operation}.log"
            failed = run_cli_args(kernel, "upgrade", repo,
                                  env=preload_env(repo, operation, fault_log))
            negative_ok = (
                fault_log.exists() and fault_log.read_text().splitlines() == [operation] and
                calm_failure(failed) and repo_unchanged(repo, repo_before) and
                exact_path_snapshot(outside) == outside_before and
                (repo / ".git/index").read_bytes() == index_before and not transaction_dirt(repo)
            )
            retry_ok = full_clean_retry(
                repo, outside, prior_label, outside_before, index_before
            )
            results.append((
                f"full-state injected {operation} failure rolls back every owner byte and then retries cleanly twice",
                negative_ok and retry_ok,
            ))

        cleanup_repo = fresh_repo("cleanup-reported-failure")
        write_file(cleanup_repo, ".claude/custom.txt", "owner custom survives cleanup\n")
        cleanup_log = base / "fault-cleanup.log"
        cleanup_run = run_cli_args(
            kernel, "install", cleanup_repo,
            env=preload_env(cleanup_repo, "cleanup", cleanup_log),
        )
        results.append((
            "cleanup verifies completed removal before treating a reported removal error as rollback-worthy",
            cleanup_log.exists() and cleanup_log.read_text().splitlines() == ["cleanup"] and
            cleanup_run.returncode == 0 and not cleanup_run.stderr and
            (cleanup_repo / ".claude/custom.txt").read_text() == "owner custom survives cleanup\n" and
            ".claude/custom.txt" in cleanup_run.stdout and not transaction_dirt(cleanup_repo),
        ))

        real_git = shutil.which("git")
        if real_git is None:
            raise AssertionError("git executable not found")
        wrapper_dir = base / "git-failure-wrapper"
        wrapper_dir.mkdir()
        wrapper = wrapper_dir / "git"
        wrapper.write_text(
            "#!/bin/sh\nset -eu\nREAL_GIT=" + shlex.quote(real_git) + "\n" + r'''
command=""
no_index=0
for arg in "$@"; do
  [ "$arg" = "status" ] && command="status"
  [ "$arg" = "diff" ] && command="diff"
  [ "$arg" = "config" ] && command="config"
  [ "$arg" = "--no-index" ] && no_index=1
done
[ -z "${P8_GIT_SEQUENCE_LOG:-}" ] || printf '%s:%s\n' "$command" "$no_index" >> "$P8_GIT_SEQUENCE_LOG"
[ -z "${P8_GIT_INDEX_LOG:-}" ] || printf '%s|%s|%s\n' "$command" "$no_index" "${GIT_INDEX_FILE:-}" >> "$P8_GIT_INDEX_LOG"
case "${P8_GIT_FAILURE:-}" in
  status) [ "$command" = "status" ] && { echo forced status failure >&2; exit 71; } ;;
  tracked) [ "$command" = "diff" ] && [ "$no_index" = 0 ] && { echo forced tracked diff failure >&2; exit 72; } ;;
  untracked) [ "$command" = "diff" ] && [ "$no_index" = 1 ] && { echo forced untracked diff failure >&2; exit 73; } ;;
esac
exec "$REAL_GIT" "$@"
''')
        wrapper.chmod(0o755)

        def private_index_log_ok(log, real_index):
            if not log.exists():
                return False
            records = []
            for line in log.read_text().splitlines():
                parts = line.split("|", 2)
                if len(parts) == 3 and parts[0] in {"config", "status", "diff"}:
                    records.append(parts)
            commands = {command for command, _, _ in records}
            private_paths = {index for _, _, index in records}
            return (
                {"config", "status", "diff"}.issubset(commands) and
                len(private_paths) == 1 and
                all(pathlib.Path(index).is_absolute() for index in private_paths) and
                all(".speck-next-transaction-" in index for index in private_paths) and
                all(pathlib.Path(index) != real_index for index in private_paths) and
                all(not pathlib.Path(index).exists() for index in private_paths)
            )

        for operation in ("status", "tracked", "untracked"):
            repo, outside, prior_label = full_fault_fixture(f"git-fault-{operation}")
            repo_before = repo_baseline(repo)
            outside_before = exact_path_snapshot(outside)
            index_before = (repo / ".git/index").read_bytes()
            failed = run_cli_args(
                kernel, "upgrade", repo,
                env={"PATH": str(wrapper_dir) + os.pathsep + os.environ["PATH"],
                     "P8_GIT_FAILURE": operation},
            )
            negative_ok = (
                calm_failure(failed) and
                ("git status failed" in failed.stderr if operation == "status" else
                 "git diff" in failed.stderr and "failed" in failed.stderr) and
                repo_unchanged(repo, repo_before) and exact_path_snapshot(outside) == outside_before and
                (repo / ".git/index").read_bytes() == index_before and not transaction_dirt(repo)
            )
            retry_ok = full_clean_retry(
                repo, outside, prior_label, outside_before, index_before
            )
            results.append((
                f"full-state checked Git {operation} failure rolls back and then retries cleanly twice",
                negative_ok and retry_ok,
            ))

        map_report_fault = fresh_repo("carried-map-late-report-failure")
        map_report_label = "carried-map-report-fixture"
        map_report_bytes = b"# Owner map behind AGENTS\n"
        write_file(
            map_report_fault, ".claude/speck-next.json",
            v5_marker_bytes(map_report_label).decode(),
        )
        write_file(map_report_fault, "product.md", "# Report-failure product\n")
        (map_report_fault / "AGENTS.md").write_bytes(map_report_bytes)
        os.chmod(map_report_fault / "AGENTS.md", 0o600)
        os.symlink("AGENTS.md", map_report_fault / "map.md")
        write_file(map_report_fault, "owner/tracked.txt", "tracked report dirt\n")
        (map_report_fault / "owner/tracked.bin").write_bytes(b"\x00\xfftracked-report\r\n")
        commit_fixture(map_report_fault, "carried map report-failure baseline")
        write_file(map_report_fault, "owner/untracked.txt", "untracked report dirt\n")
        (map_report_fault / "owner/untracked.bin").write_bytes(b"\xfe\x00untracked-report\r\n")
        map_report_before = repo_baseline(map_report_fault)
        map_report_marker_before = (map_report_fault / ".claude/speck-next.json").read_bytes()
        map_report_product_before = (map_report_fault / "product.md").read_bytes()
        map_report_referent_before = exact_path_snapshot(map_report_fault / "AGENTS.md")
        map_report_link_before = exact_path_snapshot(map_report_fault / "map.md")
        map_report_logical_mode = (map_report_fault / "map.md").stat().st_mode & 0o777
        map_report_index_before = (map_report_fault / ".git/index").read_bytes()
        map_report_failed = run_cli_args(
            kernel, "upgrade", map_report_fault,
            env={"PATH": str(wrapper_dir) + os.pathsep + os.environ["PATH"],
                 "P8_GIT_FAILURE": "status"},
        )
        map_report_rollback_ok = (
            calm_failure(map_report_failed) and "git status failed" in map_report_failed.stderr and
            repo_unchanged(map_report_fault, map_report_before) and
            (map_report_fault / ".claude/speck-next.json").read_bytes() == map_report_marker_before and
            (map_report_fault / "product.md").read_bytes() == map_report_product_before and
            exact_path_snapshot(map_report_fault / "AGENTS.md") == map_report_referent_before and
            exact_path_snapshot(map_report_fault / "map.md") == map_report_link_before and
            (map_report_fault / "map.md").read_bytes() == map_report_bytes and
            (map_report_fault / "map.md").stat().st_mode & 0o777 == map_report_logical_mode and
            (map_report_fault / "owner/tracked.bin").read_bytes() == b"\x00\xfftracked-report\r\n" and
            (map_report_fault / "owner/untracked.bin").read_bytes() == b"\xfe\x00untracked-report\r\n" and
            (map_report_fault / ".git/index").read_bytes() == map_report_index_before and
            not transaction_dirt(map_report_fault)
        )
        map_report_clean = run_cli(kernel, "upgrade", map_report_fault)
        map_report_clean_ok = (
            upgrade_report_ok(
                map_report_clean, "5.4.1", map_report_label,
                source_checkout, surface_digest, NEXT_PENDING_CHANGED,
            ) and not map_report_clean.stderr and
            "Localized carried map.md into a local regular file" in map_report_clean.stdout and
            (map_report_fault / "map.md").is_file() and
            not (map_report_fault / "map.md").is_symlink() and
            (map_report_fault / "map.md").read_bytes() == map_report_bytes and
            (map_report_fault / "map.md").stat().st_mode & 0o777 == map_report_logical_mode and
            (map_report_fault / "AGENTS.md").read_bytes() == (kernel / "AGENTS.md").read_bytes() and
            (map_report_fault / "owner/tracked.bin").read_bytes() == b"\x00\xfftracked-report\r\n" and
            (map_report_fault / "owner/untracked.bin").read_bytes() == b"\xfe\x00untracked-report\r\n" and
            (map_report_fault / ".git/index").read_bytes() == map_report_index_before and
            not transaction_dirt(map_report_fault)
        )
        results.append((
            "a late checked-report failure restores a carried map alias and all owner state before clean and stable retries",
            map_report_rollback_ok and map_report_clean_ok and
            stable_retry(map_report_fault, map_report_clean) and
            (map_report_fault / ".git/index").read_bytes() == map_report_index_before,
        ))

        bridge_report_fault = fresh_repo("carried-map-linked-bridge-index-failure")
        bridge_report_label = "carried-map-linked-bridge-fixture"
        bridge_map_bytes = b"# Owner map through nested outside link\r\n\x00\xff\n"
        bridge_outside = base / "carried-map-linked-bridge-outside"
        bridge_outside.mkdir()
        (bridge_outside / "owner-map.md").write_bytes(bridge_map_bytes)
        os.chmod(bridge_outside / "owner-map.md", 0o641)
        (bridge_outside / "sentinel.bin").write_bytes(b"\xff\x00outside-bridge\r\n")
        write_file(
            bridge_report_fault, ".claude/speck-next.json",
            v5_marker_bytes(bridge_report_label).decode(),
        )
        write_file(bridge_report_fault, "product.md", "# Linked-bridge product\n")
        (bridge_report_fault / "templates").mkdir()
        os.symlink(bridge_outside.resolve(), bridge_report_fault / "templates/bridge")
        os.symlink(
            "templates/bridge/owner-map.md", bridge_report_fault / "map.md"
        )
        write_file(bridge_report_fault, "owner/tracked.txt", "tracked bridge dirt\n")
        (bridge_report_fault / "owner/tracked.bin").write_bytes(b"\x00\xfftracked-bridge\r\n")
        commit_fixture(bridge_report_fault, "linked bridge report-failure baseline")
        write_file(bridge_report_fault, "owner/untracked.txt", "untracked bridge dirt\n")
        (bridge_report_fault / "owner/untracked.bin").write_bytes(b"\xfe\x00untracked-bridge\r\n")
        bridge_repo_before = repo_baseline(bridge_report_fault)
        bridge_outside_before = exact_path_snapshot(bridge_outside)
        bridge_map_link_before = exact_path_snapshot(bridge_report_fault / "map.md")
        bridge_map_mode_before = (bridge_report_fault / "map.md").stat().st_mode & 0o777
        bridge_real_index = git_metadata_path(bridge_report_fault, "index")
        bridge_index_before = index_family_snapshot(bridge_report_fault)
        bridge_sequence_log = base / "carried-map-linked-bridge-git-sequence.log"
        bridge_failure_index_log = base / "carried-map-linked-bridge-failure-index.log"
        bridge_failed = run_cli_args(
            kernel, "upgrade", bridge_report_fault,
            env={"PATH": str(wrapper_dir) + os.pathsep + os.environ["PATH"],
                 "P8_GIT_FAILURE": "untracked",
                 "P8_GIT_SEQUENCE_LOG": str(bridge_sequence_log),
                 "P8_GIT_INDEX_LOG": str(bridge_failure_index_log)},
        )
        bridge_sequence = (bridge_sequence_log.read_text().splitlines()
                           if bridge_sequence_log.exists() else [])
        bridge_tracked_before_untracked = (
            "diff:0" in bridge_sequence and "diff:1" in bridge_sequence and
            bridge_sequence.index("diff:0") < bridge_sequence.index("diff:1")
        )
        bridge_failure_ok = (
            calm_failure(bridge_failed) and "git diff --no-index failed" in bridge_failed.stderr and
            bridge_tracked_before_untracked and
            private_index_log_ok(bridge_failure_index_log, bridge_real_index) and
            repo_unchanged(bridge_report_fault, bridge_repo_before) and
            exact_path_snapshot(bridge_outside) == bridge_outside_before and
            exact_path_snapshot(bridge_report_fault / "map.md") == bridge_map_link_before and
            (bridge_report_fault / "map.md").read_bytes() == bridge_map_bytes and
            (bridge_report_fault / "map.md").stat().st_mode & 0o777 == bridge_map_mode_before and
            index_family_snapshot(bridge_report_fault) == bridge_index_before and
            not transaction_dirt(bridge_report_fault)
        )
        bridge_clean_index_log = base / "carried-map-linked-bridge-clean-index.log"
        bridge_clean = run_cli_args(
            kernel, "upgrade", bridge_report_fault,
            env={"PATH": str(wrapper_dir) + os.pathsep + os.environ["PATH"],
                 "P8_GIT_INDEX_LOG": str(bridge_clean_index_log)},
        )
        bridge_clean_ok = (
            upgrade_report_ok(
                bridge_clean, "5.4.1", bridge_report_label,
                source_checkout, surface_digest, NEXT_PENDING_CHANGED,
            ) and not bridge_clean.stderr and
            private_index_log_ok(bridge_clean_index_log, bridge_real_index) and
            index_family_snapshot(bridge_report_fault) == bridge_index_before and
            exact_path_snapshot(bridge_outside) == bridge_outside_before and
            (bridge_report_fault / "map.md").is_file() and
            not (bridge_report_fault / "map.md").is_symlink() and
            (bridge_report_fault / "map.md").read_bytes() == bridge_map_bytes and
            (bridge_report_fault / "map.md").stat().st_mode & 0o777 == bridge_map_mode_before and
            (bridge_report_fault / "templates/bridge").is_symlink() and
            not transaction_dirt(bridge_report_fault)
        )
        bridge_before_retry = repo_baseline(bridge_report_fault)
        bridge_retry_index_log = base / "carried-map-linked-bridge-retry-index.log"
        bridge_retry = run_cli_args(
            kernel, "upgrade", bridge_report_fault,
            env={"PATH": str(wrapper_dir) + os.pathsep + os.environ["PATH"],
                 "P8_GIT_INDEX_LOG": str(bridge_retry_index_log)},
        )
        bridge_retry_ok = (
            bridge_retry.returncode == 0 and not bridge_retry.stderr and
            private_index_log_ok(bridge_retry_index_log, bridge_real_index) and
            repo_unchanged(bridge_report_fault, bridge_before_retry) and
            index_family_snapshot(bridge_report_fault) == bridge_index_before and
            exact_path_snapshot(bridge_outside) == bridge_outside_before and
            not transaction_dirt(bridge_report_fault)
        )
        results.append((
            "the linked-bridge carried-map attack keeps its real index family exact through late failure, clean upgrade, and stable retry",
            bridge_failure_ok and bridge_clean_ok and bridge_retry_ok,
        ))

        def seed_reporting_index_upgrade(repo, label):
            write_file(
                repo, ".claude/speck-next.json", v5_marker_bytes(label).decode()
            )
            write_file(repo, "product.md", f"# {label} product\n")
            write_file(repo, "owner/tracked.txt", f"{label} tracked text\n")
            (repo / "owner/tracked.bin").write_bytes(b"\x00\xffindex-tracked\r\n")
            commit_fixture(repo, f"{label} tracked baseline")

        def add_reporting_index_untracked(repo, label):
            write_file(repo, "owner/untracked.txt", f"{label} untracked text\n")
            (repo / "owner/untracked.bin").write_bytes(b"\xfe\x00index-untracked\r\n")

        def exercise_reporting_index_variant(name, repo, command, prior_label, setup_ok=True):
            real_index = git_metadata_path(repo, "index")
            repo_before = repo_baseline(repo)
            family_before = index_family_snapshot(repo)
            failure_sequence_log = base / f"{name}-failure-sequence.log"
            failure_index_log = base / f"{name}-failure-index.log"
            failed = run_cli_args(
                kernel, command, repo,
                env={"PATH": str(wrapper_dir) + os.pathsep + os.environ["PATH"],
                     "P8_GIT_FAILURE": "untracked",
                     "P8_GIT_SEQUENCE_LOG": str(failure_sequence_log),
                     "P8_GIT_INDEX_LOG": str(failure_index_log)},
            )
            sequence = (failure_sequence_log.read_text().splitlines()
                        if failure_sequence_log.exists() else [])
            failure_ok = (
                calm_failure(failed) and "git diff --no-index failed" in failed.stderr and
                "diff:0" in sequence and "diff:1" in sequence and
                sequence.index("diff:0") < sequence.index("diff:1") and
                private_index_log_ok(failure_index_log, real_index) and
                repo_unchanged(repo, repo_before) and
                index_family_snapshot(repo) == family_before and
                not transaction_dirt(repo)
            )

            clean_index_log = base / f"{name}-clean-index.log"
            clean = run_cli_args(
                kernel, command, repo,
                env={"PATH": str(wrapper_dir) + os.pathsep + os.environ["PATH"],
                     "P8_GIT_INDEX_LOG": str(clean_index_log)},
            )
            if command == "upgrade":
                report_ok = upgrade_report_ok(
                    clean, "5.4.1", prior_label,
                    source_checkout, surface_digest, NEXT_PENDING_CHANGED,
                )
            else:
                actual_paths = sorted(
                    item.relative_to(repo).as_posix()
                    for item in repo.rglob("*")
                    if ".git" not in item.relative_to(repo).parts and
                    (item.is_file() or item.is_symlink())
                )
                reported_count, reported_paths = install_report(clean)
                report_ok = (
                    clean.returncode == 0 and not clean.stderr and
                    reported_count == len(actual_paths) and reported_paths == actual_paths and
                    marker_ok(repo, source_checkout, surface_digest) and
                    not (repo / "product.md").exists()
                )
            clean_ok = (
                report_ok and not clean.stderr and
                private_index_log_ok(clean_index_log, real_index) and
                index_family_snapshot(repo) == family_before and
                (command == "install" or
                 "diff --git a/AGENTS.md b/AGENTS.md" in clean.stdout) and
                not transaction_dirt(repo)
            )

            before_retry = repo_baseline(repo)
            retry_index_log = base / f"{name}-retry-index.log"
            retry = run_cli_args(
                kernel, "upgrade", repo,
                env={"PATH": str(wrapper_dir) + os.pathsep + os.environ["PATH"],
                     "P8_GIT_INDEX_LOG": str(retry_index_log)},
            )
            retry_ok = (
                retry.returncode == 0 and not retry.stderr and
                private_index_log_ok(retry_index_log, real_index) and
                repo_unchanged(repo, before_retry) and
                index_family_snapshot(repo) == family_before and
                not transaction_dirt(repo)
            )
            results.append((
                f"{name} reporting uses only a private index through late failure, correct success, and stable retry",
                setup_ok and failure_ok and clean_ok and retry_ok,
            ))

        normal_index_repo = fresh_repo("private-report-index-normal")
        normal_index_label = "normal-index-fixture"
        seed_reporting_index_upgrade(normal_index_repo, normal_index_label)
        add_reporting_index_untracked(normal_index_repo, normal_index_label)
        exercise_reporting_index_variant(
            "normal-index", normal_index_repo, "upgrade", normal_index_label
        )

        split_index_repo = fresh_repo("private-report-index-split")
        split_index_label = "split-index-fixture"
        seed_reporting_index_upgrade(split_index_repo, split_index_label)
        subprocess.run(
            ["git", "update-index", "--split-index"], cwd=split_index_repo, check=True
        )
        add_reporting_index_untracked(split_index_repo, split_index_label)
        split_index_path = git_metadata_path(split_index_repo, "index")
        split_index_ready = any(split_index_path.parent.glob("sharedindex.*"))
        exercise_reporting_index_variant(
            "split-index", split_index_repo, "upgrade", split_index_label,
            setup_ok=split_index_ready,
        )

        linked_index_main = fresh_repo("private-report-index-linked-main")
        linked_index_label = "linked-worktree-split-index-fixture"
        seed_reporting_index_upgrade(linked_index_main, linked_index_label)
        linked_index_repo = base / "private-report-index-linked-worktree"
        subprocess.run(
            ["git", "worktree", "add", "-q", "-b", "piece8-private-report-index",
             str(linked_index_repo)],
            cwd=linked_index_main, check=True,
        )
        subprocess.run(
            ["git", "update-index", "--split-index"], cwd=linked_index_repo, check=True
        )
        add_reporting_index_untracked(linked_index_repo, linked_index_label)
        linked_index_path = git_metadata_path(linked_index_repo, "index")
        linked_index_ready = (
            linked_index_path.parent != (linked_index_repo / ".git") and
            any(linked_index_path.parent.glob("sharedindex.*"))
        )
        exercise_reporting_index_variant(
            "linked-worktree-split-index", linked_index_repo, "upgrade",
            linked_index_label, setup_ok=linked_index_ready,
        )

        unborn_index_repo = fresh_repo("private-report-index-unborn")
        unborn_index_path = git_metadata_path(unborn_index_repo, "index")
        exercise_reporting_index_variant(
            "unborn-index", unborn_index_repo, "install", None,
            setup_ok=exact_path_snapshot(unborn_index_path) == ("missing",),
        )

        linked_active_repo = fresh_repo("private-report-index-linked-active")
        linked_active_label = "linked-active-index-fixture"
        seed_reporting_index_upgrade(linked_active_repo, linked_active_label)
        add_reporting_index_untracked(linked_active_repo, linked_active_label)
        linked_active_path = git_metadata_path(linked_active_repo, "index")
        linked_active_outside = base / "private-report-index-linked-active-outside"
        linked_active_outside.mkdir()
        linked_active_referent = linked_active_outside / "index.actual"
        shutil.move(linked_active_path, linked_active_referent)
        os.chmod(linked_active_referent, 0o640)
        (linked_active_outside / "sentinel.bin").write_bytes(
            b"\xff\x00linked-active-index-outside\r\n"
        )
        os.symlink(linked_active_referent.resolve(), linked_active_path)
        linked_precondition_env = git_metadata_env()
        linked_precondition_args = [
            "git", "--no-pager", "--literal-pathspecs",
            "-c", "core.fsmonitor=false", "-c", "core.splitIndex=false",
            "-c", "core.hooksPath=", "-c", "diff.external=",
        ]
        linked_precondition_status = subprocess.run(
            linked_precondition_args + [
                "status", "--porcelain=v1", "-z", "--untracked-files=all",
            ],
            cwd=linked_active_repo, capture_output=True,
            env=linked_precondition_env,
        )
        linked_precondition_diff = subprocess.run(
            linked_precondition_args + [
                "diff", "--no-ext-diff", "--no-textconv", "--no-color", "--",
            ],
            cwd=linked_active_repo, capture_output=True,
            env=linked_precondition_env,
        )
        linked_active_git_ok = (
            linked_precondition_status.returncode == 0 and
            not linked_precondition_status.stderr and
            b"owner/untracked.bin" in linked_precondition_status.stdout and
            linked_precondition_diff.returncode == 0 and
            not linked_precondition_diff.stderr
        )
        linked_active_before = repo_baseline(linked_active_repo)
        linked_active_git_dir_before = exact_path_snapshot(linked_active_repo / ".git")
        linked_active_link_before = exact_path_snapshot(linked_active_path)
        linked_active_referent_before = exact_path_snapshot(linked_active_referent)
        linked_active_outside_before = exact_path_snapshot(linked_active_outside)
        linked_active_family_before = index_family_snapshot(linked_active_repo)
        linked_active_failure_sequence = base / "linked-active-index-failure-sequence.log"
        linked_active_failure_log = base / "linked-active-index-failure-private.log"
        linked_active_failed = run_cli_args(
            kernel, "upgrade", linked_active_repo,
            env={"PATH": str(wrapper_dir) + os.pathsep + os.environ["PATH"],
                 "P8_GIT_FAILURE": "untracked",
                 "P8_GIT_SEQUENCE_LOG": str(linked_active_failure_sequence),
                 "P8_GIT_INDEX_LOG": str(linked_active_failure_log)},
        )
        linked_active_sequence = (
            linked_active_failure_sequence.read_text().splitlines()
            if linked_active_failure_sequence.exists() else []
        )
        linked_active_failure_ok = (
            calm_failure(linked_active_failed) and
            "git diff --no-index failed" in linked_active_failed.stderr and
            "diff:0" in linked_active_sequence and "diff:1" in linked_active_sequence and
            linked_active_sequence.index("diff:0") < linked_active_sequence.index("diff:1") and
            private_index_log_ok(linked_active_failure_log, linked_active_path) and
            repo_unchanged(linked_active_repo, linked_active_before) and
            exact_path_snapshot(linked_active_repo / ".git") == linked_active_git_dir_before and
            exact_path_snapshot(linked_active_path) == linked_active_link_before and
            exact_path_snapshot(linked_active_referent) == linked_active_referent_before and
            exact_path_snapshot(linked_active_outside) == linked_active_outside_before and
            index_family_snapshot(linked_active_repo) == linked_active_family_before and
            not transaction_dirt(linked_active_repo)
        )
        linked_active_clean_log = base / "linked-active-index-clean-private.log"
        linked_active_clean = run_cli_args(
            kernel, "upgrade", linked_active_repo,
            env={"PATH": str(wrapper_dir) + os.pathsep + os.environ["PATH"],
                 "P8_GIT_INDEX_LOG": str(linked_active_clean_log)},
        )
        linked_active_clean_ok = (
            upgrade_report_ok(
                linked_active_clean, "5.4.1", linked_active_label,
                source_checkout, surface_digest, NEXT_PENDING_CHANGED,
            ) and not linked_active_clean.stderr and
            private_index_log_ok(linked_active_clean_log, linked_active_path) and
            exact_path_snapshot(linked_active_repo / ".git") == linked_active_git_dir_before and
            exact_path_snapshot(linked_active_path) == linked_active_link_before and
            exact_path_snapshot(linked_active_referent) == linked_active_referent_before and
            exact_path_snapshot(linked_active_outside) == linked_active_outside_before and
            index_family_snapshot(linked_active_repo) == linked_active_family_before and
            (linked_active_repo / "owner/tracked.bin").read_bytes() == b"\x00\xffindex-tracked\r\n" and
            (linked_active_repo / "owner/untracked.bin").read_bytes() == b"\xfe\x00index-untracked\r\n" and
            not transaction_dirt(linked_active_repo)
        )
        linked_active_after_clean = repo_baseline(linked_active_repo)
        linked_active_product_after_clean = (linked_active_repo / "product.md").read_bytes()
        linked_active_porcelain_after_clean = porcelain_v1_z(linked_active_repo)
        linked_active_retry_log = base / "linked-active-index-retry-private.log"
        linked_active_retry = run_cli_args(
            kernel, "upgrade", linked_active_repo,
            env={"PATH": str(wrapper_dir) + os.pathsep + os.environ["PATH"],
                 "P8_GIT_INDEX_LOG": str(linked_active_retry_log)},
        )
        linked_active_retry_ok = (
            linked_active_retry.returncode == 0 and not linked_active_retry.stderr and
            private_index_log_ok(linked_active_retry_log, linked_active_path) and
            repo_unchanged(linked_active_repo, linked_active_after_clean) and
            porcelain_v1_z(linked_active_repo) == linked_active_porcelain_after_clean and
            (linked_active_repo / "product.md").read_bytes() == linked_active_product_after_clean and
            exact_path_snapshot(linked_active_repo / ".git") == linked_active_git_dir_before and
            exact_path_snapshot(linked_active_path) == linked_active_link_before and
            exact_path_snapshot(linked_active_referent) == linked_active_referent_before and
            exact_path_snapshot(linked_active_outside) == linked_active_outside_before and
            index_family_snapshot(linked_active_repo) == linked_active_family_before and
            not transaction_dirt(linked_active_repo)
        )
        results.append((
            "a supported linked active index is read privately through late failure, clean upgrade, and stable retry without changing its link, referent, or index family",
            linked_active_git_ok and linked_active_failure_ok and
            linked_active_clean_ok and linked_active_retry_ok,
        ))

        def invalid_linked_index_refusal(name, referent_kind):
            repo = fresh_repo(name)
            label = f"{name}-fixture"
            seed_reporting_index_upgrade(repo, label)
            active = git_metadata_path(repo, "index")
            outside = base / f"{name}-outside"
            outside.mkdir()
            shutil.move(active, outside / "original-index.bin")
            if referent_kind == "dangling":
                referent = outside / "missing-index"
            else:
                referent = outside / "index-directory"
                referent.mkdir()
                (referent / "sentinel.bin").write_bytes(
                    b"\xff\x00non-file-index-referent\r\n"
                )
            os.symlink(referent.resolve(), active)
            tree_before = repository_snapshot(repo)
            git_dir_before = exact_path_snapshot(repo / ".git")
            outside_before = exact_path_snapshot(outside)
            link_before = exact_path_snapshot(active)
            family_before = index_family_snapshot(repo)
            product_before = (repo / "product.md").read_bytes()
            marker_before = (repo / ".claude/speck-next.json").read_bytes()
            run = run_cli(kernel, "upgrade", repo)
            return (
                calm_failure(run) and not run.stdout and
                "does not resolve to a readable regular file" in run.stderr and
                repository_snapshot(repo) == tree_before and
                exact_path_snapshot(repo / ".git") == git_dir_before and
                exact_path_snapshot(outside) == outside_before and
                exact_path_snapshot(active) == link_before and
                index_family_snapshot(repo) == family_before and
                (repo / "product.md").read_bytes() == product_before and
                (repo / ".claude/speck-next.json").read_bytes() == marker_before and
                not transaction_dirt(repo)
            )

        results.append((
            "a dangling active-index link refuses atomically before any product or Git byte changes",
            invalid_linked_index_refusal(
                "private-report-index-linked-dangling", "dangling"
            ),
        ))
        results.append((
            "an active-index link to a non-file refuses atomically before any product or Git byte changes",
            invalid_linked_index_refusal(
                "private-report-index-linked-non-file", "non-file"
            ),
        ))

        ignored_repo = fresh_repo("ignored-directory")
        seed_upgrade_repo(ignored_repo, "5.4.1", "ignored-directory-fixture", "# Ignored product\n")
        (ignored_repo / ".git/info").mkdir(parents=True, exist_ok=True)
        write_file(ignored_repo, ".git/info/exclude", "templates/\n")
        ignored_run = run_cli(kernel, "upgrade", ignored_repo)
        results.append((
            "a whole ignored installed directory has complete leaf diffs instead of a directory no-index failure",
            ignored_run.returncode == 0 and not ignored_run.stderr and
            "templates/piece.md" in ignored_run.stdout and
            "diff --git a/templates/piece.md b/templates/piece.md" in ignored_run.stdout,
        ))

        ignored_link_repo = fresh_repo("ignored-symlink")
        seed_upgrade_repo(ignored_link_repo, "5.4.1", "ignored-symlink-fixture", "# Ignored link product\n")
        ignored_link_outside = base / "ignored-symlink-outside"
        ignored_link_outside.mkdir()
        write_file(ignored_link_outside, "sentinel.txt", "ignored link outside\n")
        (ignored_link_repo / ".claude/skills").mkdir(parents=True)
        os.symlink(ignored_link_outside, ignored_link_repo / ".claude/skills/custom-link")
        (ignored_link_repo / ".git/info").mkdir(parents=True, exist_ok=True)
        write_file(ignored_link_repo, ".git/info/exclude", ".claude/skills/custom-link\n")
        ignored_link_before = snapshot_digest(ignored_link_outside)
        ignored_link_run = run_cli(kernel, "upgrade", ignored_link_repo)
        results.append((
            "an ignored untracked symlink is reported as a symlink without dereferencing it",
            ignored_link_run.returncode == 0 and not ignored_link_run.stderr and
            "new file mode 120000" in ignored_link_run.stdout and
            ".claude/skills/custom-link" in ignored_link_run.stdout and
            snapshot_digest(ignored_link_outside) == ignored_link_before and
            (ignored_link_repo / ".claude/skills/custom-link").is_symlink(),
        ))

        ignored_agents = fresh_repo("ignored-agents-clamp")
        seed_upgrade_repo(
            ignored_agents, "5.4.1", "ignored-agents-fixture", "# Ignored agents product\n"
        )
        write_file(ignored_agents, ".git/info/exclude", ".agents/\n")
        private_sentinel = "PRIVATE-OWNER-SKILL-SENTINEL-7d305f9a"
        write_file(
            ignored_agents, ".agents/skills/owner-skill/SKILL.md",
            f"---\nname: owner-skill\ndescription: {private_sentinel}\n---\n",
        )
        write_file(ignored_agents, ".agents/skills/speck-next/owner.txt", "owner collision\n")
        ignored_owner_before = exact_path_snapshot(ignored_agents / ".agents/skills/owner-skill")
        ignored_collision_before = exact_path_snapshot(ignored_agents / ".agents/skills/speck-next")
        ignored_agents_run = run_cli(kernel, "upgrade", ignored_agents)
        ignored_agents_output = ignored_agents_run.stdout + ignored_agents_run.stderr
        results.append((
            "an ignored .agents ancestor reports only the selected adapter without reading owner-skill bytes into output or diff",
            ignored_agents_run.returncode == 0 and not ignored_agents_run.stderr and
            codex_adapter_name(ignored_agents) == "speck-next-2" and
            "!! .agents/skills/speck-next-2" in ignored_agents_run.stdout and
            "diff --git a/.agents/skills/speck-next-2 b/.agents/skills/speck-next-2" in ignored_agents_run.stdout and
            "../../.claude/skills" in ignored_agents_run.stdout and
            private_sentinel not in ignored_agents_output and
            "owner-skill" not in ignored_agents_output and
            exact_path_snapshot(ignored_agents / ".agents/skills/owner-skill") == ignored_owner_before and
            exact_path_snapshot(ignored_agents / ".agents/skills/speck-next") == ignored_collision_before and
            stable_retry(ignored_agents, ignored_agents_run),
        ))

        git_attack = fresh_repo("local-git-attack")
        seed_upgrade_repo(git_attack, "5.4.1", "local-git-attack-fixture", "# Git attack product\n")
        attack_dir = git_attack / "attack"
        attack_dir.mkdir()
        attack_log = base / "local-git-attack.log"
        helper = attack_dir / "helper.sh"
        helper.write_text("#!/bin/sh\necho invoked >> " + shlex.quote(str(attack_log)) + "\ncat\n")
        helper.chmod(0o755)
        attack_referent = base / "local-git-attack-referent"
        attack_referent.mkdir()
        write_file(attack_referent, "sentinel.txt", "git attack referent\n")
        (attack_referent / "sentinel.bin").write_bytes(b"\xff\x00git-attack\n")
        os.symlink(attack_referent, git_attack / "templates")
        write_file(git_attack, ".gitattributes", "*.md diff=attack filter=attack\n")
        commit_fixture(git_attack, "attack fixtures before arming local config")
        write_file(git_attack, "owner/untracked.txt", "git attack untracked\n")
        (git_attack / "owner/untracked.bin").write_bytes(b"\x00\xfeuntracked\n")

        def hostile_porcelain(root):
            safe_env = {key: value for key, value in os.environ.items()
                        if not key.startswith("GIT_")}
            safe_env.update({
                "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull, "GIT_PAGER": "cat", "PAGER": "cat",
                "LC_ALL": "C",
            })
            return subprocess.run([
                real_git, "--no-pager", "--literal-pathspecs",
                "-c", "core.fsmonitor=false", "-c", "core.hooksPath=",
                "-c", "diff.external=", "-c", "diff.attack.textconv=",
                "-c", "filter.attack.clean=", "-c", "filter.attack.process=",
                "-c", "filter.attack.required=false",
                "status", "--porcelain=v1", "-z", "--untracked-files=all",
            ], cwd=root, check=True, capture_output=True, env=safe_env).stdout

        def hostile_repo_baseline(root):
            return {"tree": repository_snapshot(root), "porcelain": hostile_porcelain(root)}

        def hostile_repo_unchanged(root, before):
            return (repository_snapshot(root) == before["tree"] and
                    hostile_porcelain(root) == before["porcelain"])

        for key, value in (
            ("core.fsmonitor", str(helper)),
            ("diff.external", str(helper)),
            ("diff.attack.textconv", str(helper)),
            ("filter.attack.clean", str(helper)),
            ("filter.attack.process", str(helper)),
            ("filter.attack.required", "true"),
        ):
            subprocess.run(["git", "config", key, value], cwd=git_attack, check=True)
        index_path = git_attack / ".git/index"
        index_before = index_path.read_bytes()
        config_before = (git_attack / ".git/config").read_bytes()
        attack_before = hostile_repo_baseline(git_attack)
        attack_referent_before = exact_path_snapshot(attack_referent)
        failed_trace = base / "failed-inherited-git-trace.json"
        git_attack_failed = run_cli_args(
            kernel, "upgrade", git_attack,
            env={
                "PATH": str(wrapper_dir) + os.pathsep + os.environ["PATH"],
                "P8_GIT_FAILURE": "status",
                "GIT_TRACE2_EVENT": str(failed_trace), "GIT_PAGER": str(helper),
            },
        )
        git_attack_failed_ok = (
            calm_failure(git_attack_failed) and "git status failed" in git_attack_failed.stderr and
            hostile_repo_unchanged(git_attack, attack_before) and
            exact_path_snapshot(attack_referent) == attack_referent_before and
            (git_attack / ".git/config").read_bytes() == config_before and
            index_path.read_bytes() == index_before and not attack_log.exists() and
            not failed_trace.exists() and not transaction_dirt(git_attack)
        )
        clean_trace = base / "clean-inherited-git-trace.json"
        git_attack_clean = run_cli_args(
            kernel, "upgrade", git_attack,
            env={"GIT_TRACE2_EVENT": str(clean_trace), "GIT_PAGER": str(helper)},
        )
        clean_before_retry = hostile_repo_baseline(git_attack)
        retry_trace = base / "retry-inherited-git-trace.json"
        git_attack_retry = run_cli_args(
            kernel, "upgrade", git_attack,
            env={"GIT_TRACE2_EVENT": str(retry_trace), "GIT_PAGER": str(helper)},
        )
        results.append((
            "hostile local and inherited Git state stays inert through failure rollback, clean retry, and stable retry",
            git_attack_failed_ok and
            upgrade_report_ok(
                git_attack_clean, "5.4.1", "local-git-attack-fixture",
                source_checkout, surface_digest, NEXT_PENDING_CHANGED,
            ) and not git_attack_clean.stderr and
            upgrade_report_ok(
                git_attack_retry, CURRENT_VERSION, source_checkout,
                source_checkout, surface_digest, NEXT_PENDING_CHANGED,
                prior_digest=surface_digest,
            ) and not git_attack_retry.stderr and
            hostile_repo_unchanged(git_attack, clean_before_retry) and
            not attack_log.exists() and
            not any(path.exists() for path in (failed_trace, clean_trace, retry_trace)) and
            exact_path_snapshot(attack_referent) == attack_referent_before and
            (git_attack / ".git/config").read_bytes() == config_before and
            index_path.read_bytes() == index_before and not transaction_dirt(git_attack),
        ))

        no_test_switches = not re.search(
            r"SPECK_NEXT_(?:TEST|INJECT)|P8_(?:FAULT|TARGET|GIT_FAILURE)",
            (kernel / "bin/speck-next.js").read_text(),
        )
        results.append((
            "production installer has no ambient test or injected-failure switch",
            no_test_switches,
        ))

    good = True
    for label, passed in results:
        print(f"  [{'ok' if passed else 'RED'}] {label}")
        good = good and passed
    print(f"  [measure] path-transaction subjects={len(results)}")
    return good


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

        def product_team(product=None, business=None, experience=None, engineering=None):
            product = "Keeps the promises and product order coherent." if product is None else product
            engineering = ("Keeps feasibility, safety, reversibility, and operation honest."
                           if engineering is None else engineering)
            business = business or {
                "Protects": "sustainable adoption and operating cost",
                "Call when": "a change affects adoption, price, revenue, cost, or durable value",
                "May stay out when": "current measured evidence rules out those effects",
                "Evidence expires": "when that evidence ages past one milestone",
                "Material changes": "a new audience, channel, price, or cost model",
            }
            experience = experience or {
                "Protects": "the journeys, surfaces, behavior, and declared feel",
                "Call when": "a change alters what a person sees, understands, or does",
                "May stay out when": "a current observed journey proves no user-facing effect",
                "Evidence expires": "when the observed journey or surface changes",
                "Material changes": "a new journey, surface, audience, or interaction",
            }
            def conditional_row(role, fields):
                values = " · ".join(f"{field}: {fields[field]}" for field in fields)
                return f"- **{role}** — {values}\n"
            return ("## Product team\n"
                    f"- **Product** — {product}\n" +
                    conditional_row("Business", business) +
                    conditional_row("Experience", experience) +
                    f"- **Engineering** — {engineering}\n")

        def complete_pending(repo, status, route, state, retained_history="",
                             team=None):
            product = (repo / "product.md").read_text().replace(ASSESSMENT_PENDING, status, 1)
            if team is None:
                team = product_team()
            product = product.replace(ASSESSMENT_HEADING, team + "\n" + ASSESSMENT_HEADING, 1)
            if retained_history:
                product += "\n" + retained_history
            write_file(repo, "product.md", product)
            write_file(repo, ASSESSMENT_RECORD, assessment_record(route))
            write_file(repo, "state.md", state)
            commit_fixture(repo, "complete product-team assessment")

        def seeded_pending(name, original="# Existing product\n"):
            repo = base / name
            repo.mkdir()
            seed_upgrade_repo(repo, "5.4.1", f"{name}fixture", original,
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

        def run_atomic_refusal(repo, *arguments, flag_before=False, plant=True):
            if plant:
                plant_refusal_dirt(repo)
            before = refusal_baseline(repo)
            refused = (run_cli_args(kernel, "upgrade", *arguments, repo)
                       if flag_before else run_cli(kernel, "upgrade", repo, *arguments))
            return refused, refusal_unchanged(repo, before, refused)

        missing_field = object()

        def refusal_repo(name, product, version=RECOVERABLE_FIELDLESS_VERSION,
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

        round_five_crlf_original = (
            "# CRLF canonical pending product\r\n\r\n" +
            ASSESSMENT_BLOCK.replace("\n", "\r\n")
        )
        round_five_crlf = refusal_repo(
            "round-five-crlf-canonical-pending", round_five_crlf_original
        )
        round_five_crlf_run = run_cli(kernel, "upgrade", round_five_crlf)
        round_five_crlf_product = (round_five_crlf / "product.md").read_bytes()
        round_five_crlf_ok = (
            upgrade_report_ok(
                round_five_crlf_run, RECOVERABLE_FIELDLESS_VERSION,
                "round-five-crlf-canonical-pendingfixture", source_checkout,
                surface_digest, NEXT_PENDING_CHANGED,
            ) and
            round_five_crlf_product == round_five_crlf_original.encode() and
            round_five_crlf_product.count(ASSESSMENT_HEADING.encode()) == 1 and
            round_five_crlf_product.count(ASSESSMENT_PENDING.encode()) == 1
        )
        if round_five_crlf_run.returncode == 0:
            commit_fixture(round_five_crlf, "accept canonical CRLF pending upgrade")
            flagged, flag_atomic = run_atomic_refusal(
                round_five_crlf, "--open-assessment"
            )
            round_five_crlf_ok = (
                round_five_crlf_ok and flag_atomic and
                "without --open-assessment" in flagged.stderr and
                not has_resume_instruction(flagged.stdout + flagged.stderr)
            )
        results.append((
            "round-five CRLF canonical pending stays single and the flag cannot override it",
            round_five_crlf_ok,
        ))

        def assessment_bytes(ending):
            return ASSESSMENT_BLOCK.replace("\n", ending).encode()

        def appended_product_bytes(original, ending):
            original_bytes = original.encode()
            separator = ending if original.endswith(("\r", "\n")) else ending + ending
            return original_bytes + separator.encode() + assessment_bytes(ending)

        def one_style(data, ending):
            if ending == "\r\n":
                return re.search(br"(?<!\r)\n|\r(?!\n)", data) is None
            if ending == "\r":
                return b"\n" not in data
            return b"\r" not in data

        def fieldless_recovery_with_ending(label, original, ending):
            repo = refusal_repo(label, original)
            refused, refusal_atomic = run_atomic_refusal(repo)
            refusal_ok = (
                refusal_atomic and refused.stderr.rstrip().endswith(AMBIGUITY_RETRY) and
                (repo / "product.md").read_bytes() == original.encode()
            )
            opened = run_cli(kernel, "upgrade", repo, "--open-assessment")
            actual = (repo / "product.md").read_bytes()
            expected = appended_product_bytes(original, ending)
            opened_ok = (
                upgrade_report_ok(
                    opened, RECOVERABLE_FIELDLESS_VERSION, f"{label}fixture", source_checkout,
                    surface_digest, NEXT_PENDING_CHANGED,
                ) and
                "--open-assessment preserved every existing product byte" in opened.stdout and
                not has_resume_instruction(opened.stdout + opened.stderr) and
                actual == expected and actual.startswith(original.encode()) and
                one_style(actual, ending) and
                actual.count(ASSESSMENT_HEADING.encode()) == 1 and
                actual.count(ASSESSMENT_PENDING.encode()) == 1 and
                marker_ok(repo, source_checkout, surface_digest, ASSESSMENT_RECORD)
            )
            results.append((
                f"{label} refuses atomically then appends one byte-exact {ending.encode()!r} block",
                refusal_ok and opened_ok,
            ))

        fieldless_recovery_with_ending(
            "CRLF fieldless recovery with final newline",
            "# CRLF recovery product\r\n\r\nOwner bytes stay fixed.\r\n",
            "\r\n",
        )
        fieldless_recovery_with_ending(
            "CRLF fieldless recovery without final newline",
            "# CRLF recovery without final newline\r\n\r\nOwner bytes stay fixed.",
            "\r\n",
        )

        lone_cr_pending_original = (
            "# Lone-CR canonical pending product\r\r" +
            ASSESSMENT_BLOCK.replace("\n", "\r")
        )
        lone_cr_pending = refusal_repo(
            "lone-cr-canonical-pending", lone_cr_pending_original
        )
        lone_cr_pending_run = run_cli(kernel, "upgrade", lone_cr_pending)
        lone_cr_pending_bytes = (lone_cr_pending / "product.md").read_bytes()
        lone_cr_pending_ok = (
            upgrade_report_ok(
                lone_cr_pending_run, RECOVERABLE_FIELDLESS_VERSION,
                "lone-cr-canonical-pendingfixture", source_checkout,
                surface_digest, NEXT_PENDING_CHANGED,
            ) and
            lone_cr_pending_bytes == lone_cr_pending_original.encode() and
            one_style(lone_cr_pending_bytes, "\r") and
            lone_cr_pending_bytes.count(ASSESSMENT_HEADING.encode()) == 1 and
            lone_cr_pending_bytes.count(ASSESSMENT_PENDING.encode()) == 1
        )
        results.append((
            "lone-CR canonical pending is recognized without a product write or duplicate",
            lone_cr_pending_ok,
        ))
        fieldless_recovery_with_ending(
            "lone-CR fieldless recovery",
            "# Lone-CR recovery product\r\rOwner bytes stay fixed.\r",
            "\r",
        )

        mixed_generated_original = (
            "# Mixed-delimiter generated product\r\n"
            "Owner LF line\n" + REJECTED_RC2_STATUS + "\r"
            "Trailing owner text"
        )
        mixed_generated = refusal_repo(
            "mixed-delimiter-generated-line", mixed_generated_original,
            version="5.4.1",
        )
        mixed_generated_run = run_cli(kernel, "upgrade", mixed_generated)
        mixed_generated_expected_prefix = mixed_generated_original.replace(
            REJECTED_RC2_STATUS, "", 1
        )
        mixed_generated_expected = appended_product_bytes(
            mixed_generated_expected_prefix, "\r"
        )
        mixed_generated_actual = (mixed_generated / "product.md").read_bytes()
        results.append((
            "generated-line removal blanks only matched text and preserves every delimiter byte",
            upgrade_report_ok(
                mixed_generated_run, "5.4.1", "mixed-delimiter-generated-linefixture",
                source_checkout, surface_digest, NEXT_PENDING_CHANGED,
            ) and
            mixed_generated_actual == mixed_generated_expected and
            mixed_generated_actual.startswith(mixed_generated_expected_prefix.encode()) and
            mixed_generated_actual.count(ASSESSMENT_HEADING.encode()) == 1,
        ))

        def recovery_path(name, marker_extra=None, flag_before=False):
            original = f"# {name} product\n\nExisting promises stay byte-identical.\n"
            repo = refusal_repo(name, original, marker_extra=marker_extra)
            refused, refusal_ok = run_atomic_refusal(repo)
            refusal_ok = (
                refusal_ok and refused.stderr.rstrip().endswith(AMBIGUITY_RETRY) and
                (repo / "product.md").read_text() == original
            )
            results.append((f"{name} ordinary ambiguity refuses untouched with executable recovery",
                            refusal_ok))

            state_bytes = (repo / "state.md").read_bytes()
            work_bytes = (repo / "work/refusal-dirt.md").read_bytes()
            if flag_before:
                opened = run_cli_args(kernel, "upgrade", "--open-assessment", repo)
            else:
                opened = run_cli(kernel, "upgrade", repo, "--open-assessment")
            prior_checkout = marker_extra.get("sourceCheckout") if marker_extra else f"{name}fixture"
            prior_digest = marker_extra.get("methodSurfaceSha256") if marker_extra else None
            opened_ok = (
                upgrade_report_ok(opened, RECOVERABLE_FIELDLESS_VERSION, prior_checkout, source_checkout,
                                  surface_digest, NEXT_PENDING_CHANGED, prior_digest) and
                "--open-assessment preserved every existing product byte" in opened.stdout and
                not has_resume_instruction(opened.stdout + opened.stderr) and
                (repo / "product.md").read_text() == expected_product(original) and
                (repo / "state.md").read_bytes() == state_bytes and
                (repo / "work/refusal-dirt.md").read_bytes() == work_bytes and
                marker_ok(repo, source_checkout, surface_digest, ASSESSMENT_RECORD)
            )
            position = "before" if flag_before else "after"
            results.append((f"{name} flag {position} the directory opens one pending assessment",
                            opened_ok))

            commit_fixture(repo, f"accept {name} recovery")
            second_flag, second_flag_ok = run_atomic_refusal(
                repo, "--open-assessment", flag_before=flag_before, plant=False
            )
            ordinary = run_cli(kernel, "upgrade", repo)
            retry_ok = (
                second_flag_ok and "without --open-assessment" in second_flag.stderr and
                upgrade_report_ok(ordinary, CURRENT_VERSION, source_checkout, source_checkout,
                                  surface_digest, NEXT_PENDING_CLEAN, surface_digest) and
                (repo / "product.md").read_text() == expected_product(original)
            )
            results.append((f"{name} rejects a second flag and ordinary retry is byte-stable",
                            retry_ok))

            complete_pending(
                repo,
                "**Speck Next upgrade assessment:** complete — resumed Piece alpha from state.md",
                "Resume Piece alpha from state.md.",
                "# State\n\nPiece alpha is live.\n",
            )
            completed = run_cli(kernel, "upgrade", repo)
            expected_next = "Next: there are no upgrade changes to commit; resume Piece alpha from state.md."
            completed_ok = (
                upgrade_report_ok(completed, CURRENT_VERSION, source_checkout, source_checkout,
                                  surface_digest, expected_next, surface_digest) and
                assessment_record_ok((repo / ASSESSMENT_RECORD).read_text(),
                                     "Resume Piece alpha from state.md.") and
                marker_ok(repo, source_checkout, surface_digest, ASSESSMENT_RECORD)
            )
            results.append((f"{name} recovered assessment completes through the named live route",
                            completed_ok))
            return repo

        def flag_exclusion(name, product, version=RECOVERABLE_FIELDLESS_VERSION,
                           assessment_field=missing_field, record_content=None):
            repo = refusal_repo(
                "flag-exclusion-" + name,
                product,
                version=version,
                assessment_field=assessment_field,
                record_content=record_content,
            )
            refused, unchanged = run_atomic_refusal(repo, "--open-assessment")
            results.append((f"--open-assessment cannot override {name}", unchanged))
            return repo

        snapshot_control = fixed_current("snapshot-positive")
        before_snapshot = repository_snapshot(snapshot_control)
        with (snapshot_control / "AGENTS.md").open("a") as handle:
            handle.write("snapshot positive-control byte\n")
        results.append(("complete-target snapshot detects one changed installed byte",
                        before_snapshot != repository_snapshot(snapshot_control)))

        commented_generated_original = (
            "# Commented generated-status product\n\n"
            "<!--\n" + REJECTED_RC2_STATUS + "\n-->\n"
        )
        commented_generated = refusal_repo(
            "commented-generated-status", commented_generated_original
        )
        refused, commented_generated_refusal = run_atomic_refusal(commented_generated)
        commented_generated_refusal = (
            commented_generated_refusal and
            refused.stderr.rstrip().endswith(AMBIGUITY_RETRY) and
            (commented_generated / "product.md").read_text() ==
            commented_generated_original
        )
        results.append((
            "HTML-commented rejected status refuses untouched with executable recovery",
            commented_generated_refusal,
        ))

        commented_state = (commented_generated / "state.md").read_bytes()
        commented_work = (commented_generated / "work/refusal-dirt.md").read_bytes()
        opened = run_cli(kernel, "upgrade", commented_generated, "--open-assessment")
        commented_generated_opened = (
            upgrade_report_ok(
                opened, RECOVERABLE_FIELDLESS_VERSION, "commented-generated-statusfixture",
                source_checkout, surface_digest, NEXT_PENDING_CHANGED,
            ) and
            "--open-assessment preserved every existing product byte" in opened.stdout and
            not has_resume_instruction(opened.stdout + opened.stderr) and
            (commented_generated / "product.md").read_text() ==
            expected_product(commented_generated_original) and
            (commented_generated / "state.md").read_bytes() == commented_state and
            (commented_generated / "work/refusal-dirt.md").read_bytes() == commented_work and
            marker_ok(commented_generated, source_checkout, surface_digest,
                      ASSESSMENT_RECORD)
        )
        results.append((
            "HTML-commented rejected status recovers to one current pending block",
            commented_generated_opened,
        ))

        commented_complete_original = (
            "# Commented completed-assessment product\n\n"
            "<!--\n" + ASSESSMENT_HEADING + "\n\n"
            "**Speck Next upgrade assessment:** complete — resumed Piece alpha from state.md\n"
            + ASSESSMENT_RECORD_LINE + "\n-->\n"
        )
        commented_complete = refusal_repo(
            "commented-complete-assessment",
            commented_complete_original,
            record_content="# Existing assessment record\n",
        )
        refused, commented_complete_refusal = run_atomic_refusal(commented_complete)
        flagged, commented_complete_flag_refusal = run_atomic_refusal(
            commented_complete, "--open-assessment", plant=False
        )
        commented_complete_ok = (
            commented_complete_refusal and commented_complete_flag_refusal and
            ASSESSMENT_RECORD in refused.stderr and
            not has_resume_instruction(refused.stdout + refused.stderr) and
            not has_resume_instruction(flagged.stdout + flagged.stderr) and
            (commented_complete / "product.md").read_text() ==
            commented_complete_original
        )
        results.append((
            "HTML-commented completed block and orphan record refuse both calls untouched",
            commented_complete_ok,
        ))

        same_line_comment_original = (
            "# Same-line HTML-comment product\n\n"
            "<!-- " + REJECTED_RC2_STATUS + " -->\n"
        )
        same_line_comment = refusal_repo(
            "same-line-comment", same_line_comment_original
        )
        refused, same_line_comment_ok = run_atomic_refusal(same_line_comment)
        same_line_comment_ok = (
            same_line_comment_ok and
            refused.stderr.rstrip().endswith(AMBIGUITY_RETRY) and
            (same_line_comment / "product.md").read_text() ==
            same_line_comment_original
        )
        results.append((
            "same-line HTML comment cannot supply generated assessment evidence",
            same_line_comment_ok,
        ))

        mixed_line_comment_original = (
            "# Mixed-line HTML-comment product\n\n"
            "Visible history before the comment <!--\n"
            + REJECTED_RC2_STATUS + "\n"
            "--> visible history after the comment\n"
        )
        mixed_line_comment = refusal_repo(
            "mixed-line-comment", mixed_line_comment_original
        )
        refused, mixed_line_comment_ok = run_atomic_refusal(mixed_line_comment)
        mixed_line_comment_ok = (
            mixed_line_comment_ok and
            refused.stderr.rstrip().endswith(AMBIGUITY_RETRY) and
            (mixed_line_comment / "product.md").read_text() ==
            mixed_line_comment_original
        )
        results.append((
            "visible text beside a multiline HTML comment cannot activate hidden evidence",
            mixed_line_comment_ok,
        ))

        def current_after_history(name, history):
            product = "# " + name + " product\n\n" + history + "\n" + ASSESSMENT_BLOCK
            repo = refusal_repo(name, product)
            current = run_cli(kernel, "upgrade", repo)
            return (
                upgrade_report_ok(
                    current, RECOVERABLE_FIELDLESS_VERSION, f"{name}fixture", source_checkout,
                    surface_digest, NEXT_PENDING_CHANGED,
                ) and
                not has_resume_instruction(current.stdout + current.stderr) and
                (repo / "product.md").read_text() == product and
                marker_ok(repo, source_checkout, surface_digest, ASSESSMENT_RECORD)
            )

        multiple_comments = (
            "<!-- first closed comment -->\n"
            "<!--\n" + REJECTED_RC2_STATUS + "\n-->"
        )
        results.append((
            "multiple closed HTML comments hand off to current state on the next clean line",
            current_after_history("multiple-closed-comments", multiple_comments),
        ))

        fenced_and_quoted_comments = (
            "```markdown\n"
            "<!--\n" + REJECTED_RC2_STATUS + "\n-->\n"
            "```\n"
            "> <!--\n"
            "> " + ASSESSMENT_HEADING + "\n"
            "> **Speck Next upgrade assessment:** complete — resumed Retired piece from state.md\n"
            "> " + ASSESSMENT_RECORD_LINE + "\n"
            "> -->"
        )
        results.append((
            "comment delimiters inside fences and blockquotes cannot change top-level state",
            current_after_history("fenced-and-quoted-comments",
                                  fenced_and_quoted_comments),
        ))

        outer_comment = (
            "<!--\n"
            "```markdown\n"
            "> quote and fence markers stay inside the comment\n"
            + REJECTED_RC2_STATUS + "\n"
            "-->"
        )
        results.append((
            "fence and quote markers inside an HTML comment cannot escape it",
            current_after_history("outer-comment-precedence", outer_comment),
        ))

        nested_comment = (
            "<!--\n"
            "nested opener content <!-- does not replace the first close\n"
            + REJECTED_RC2_STATUS + "\n"
            "-->"
        )
        results.append((
            "nested HTML-comment opener is inert content until the first close",
            current_after_history("nested-comment-opener", nested_comment),
        ))

        results.append((
            "stray HTML-comment closer is plain text before current state",
            current_after_history("stray-comment-closer", "-->"),
        ))

        unclosed_comment_original = (
            "# Unclosed HTML-comment product\n\n"
            "<!--\n" + REJECTED_RC2_STATUS + "\n"
        )
        unclosed_comment = refusal_repo(
            "unclosed-comment", unclosed_comment_original
        )
        refused, unclosed_ordinary_ok = run_atomic_refusal(unclosed_comment)
        flagged, unclosed_flagged_ok = run_atomic_refusal(
            unclosed_comment, "--open-assessment", plant=False
        )
        unclosed_ok = (
            unclosed_ordinary_ok and unclosed_flagged_ok and
            "unclosed HTML comment" in refused.stderr and
            "unclosed HTML comment" in flagged.stderr and
            not has_resume_instruction(refused.stdout + refused.stderr) and
            not has_resume_instruction(flagged.stdout + flagged.stderr) and
            (unclosed_comment / "product.md").read_text() ==
            unclosed_comment_original
        )
        results.append((
            "unclosed HTML comment makes ordinary and flagged upgrade refuse untouched",
            unclosed_ok,
        ))

        inline_literal_original = (
            "# Inline-code literal product\n\n"
            "The literal opener `<!--` is documentation, not a comment.\n\n"
            + ASSESSMENT_BLOCK
        )
        inline_literal = refusal_repo(
            "inline-code-literal", inline_literal_original,
            assessment_field=ASSESSMENT_RECORD,
        )
        inline_literal_run = run_cli(kernel, "upgrade", inline_literal)
        inline_literal_ok = (
            upgrade_report_ok(
                inline_literal_run, RECOVERABLE_FIELDLESS_VERSION, "inline-code-literalfixture",
                source_checkout, surface_digest, NEXT_PENDING_CHANGED,
            ) and
            (inline_literal / "product.md").read_text() == inline_literal_original and
            marker_ok(inline_literal, source_checkout, surface_digest, ASSESSMENT_RECORD)
        )
        results.append((
            "balanced inline-code literal leaves following current assessment live",
            inline_literal_ok,
        ))

        unmatched_before_comment_original = (
            "# Unmatched inline-code opener product\n\n"
            "`unmatched opener before a real comment <!--\n"
            + REJECTED_RC2_STATUS + "\n-->\n"
        )
        unmatched_before_comment = refusal_repo(
            "unmatched-before-comment", unmatched_before_comment_original
        )
        refused, unmatched_before_comment_ok = run_atomic_refusal(
            unmatched_before_comment
        )
        unmatched_before_comment_ok = (
            unmatched_before_comment_ok and
            refused.stderr.rstrip().endswith(AMBIGUITY_RETRY) and
            (unmatched_before_comment / "product.md").read_text() ==
            unmatched_before_comment_original
        )
        results.append((
            "unmatched backtick exposes a later real comment and refuses ambiguity untouched",
            unmatched_before_comment_ok,
        ))

        results.append((
            "two-backtick span ignores shorter runs and shields comment-looking bytes",
            current_after_history(
                "two-backtick-span",
                "Double ``one ` plus <!-- and --> stay literal`` span.",
            ),
        ))
        results.append((
            "three-backtick span ignores shorter runs and shields comment-looking bytes",
            current_after_history(
                "three-backtick-span",
                "Triple ```one ` and two `` plus <!-- stay literal``` span.",
            ),
        ))
        results.append((
            "balanced multiline inline-code span shields comment-looking bytes",
            current_after_history(
                "multiline-inline-span",
                "Documentation `starts here\ncontinues with <!-- as literal and closes here`.",
            ),
        ))

        hidden_generated_original = (
            "# Inline-hidden generated status product\n\n"
            "Documentation `starts here\n"
            + REJECTED_RC2_STATUS + "\n"
            "and closes here`.\n"
        )
        hidden_generated = refusal_repo(
            "inline-hidden-generated", hidden_generated_original
        )
        refused, hidden_generated_refusal = run_atomic_refusal(hidden_generated)
        hidden_generated_refusal = (
            hidden_generated_refusal and
            refused.stderr.rstrip().endswith(AMBIGUITY_RETRY) and
            (hidden_generated / "product.md").read_text() == hidden_generated_original
        )
        results.append((
            "exact generated status inside multiline inline code stays inactive",
            hidden_generated_refusal,
        ))
        hidden_generated_state = (hidden_generated / "state.md").read_bytes()
        hidden_generated_dirt = (hidden_generated / "work/refusal-dirt.md").read_bytes()
        opened = run_cli(kernel, "upgrade", hidden_generated, "--open-assessment")
        hidden_generated_opened = (
            upgrade_report_ok(
                opened, RECOVERABLE_FIELDLESS_VERSION, "inline-hidden-generatedfixture",
                source_checkout, surface_digest, NEXT_PENDING_CHANGED,
            ) and
            "--open-assessment preserved every existing product byte" in opened.stdout and
            not has_resume_instruction(opened.stdout + opened.stderr) and
            (hidden_generated / "product.md").read_text() ==
            expected_product(hidden_generated_original) and
            (hidden_generated / "state.md").read_bytes() == hidden_generated_state and
            (hidden_generated / "work/refusal-dirt.md").read_bytes() ==
            hidden_generated_dirt and
            marker_ok(hidden_generated, source_checkout, surface_digest,
                      ASSESSMENT_RECORD)
        )
        results.append((
            "inline-hidden generated history recovers without changing its literal bytes",
            hidden_generated_opened,
        ))

        hidden_canonical_original = (
            "# Inline-hidden canonical status product\n\n"
            + ASSESSMENT_HEADING + "\n\n"
            "Documentation `starts here\n"
            + ASSESSMENT_PENDING + "\n"
            "and closes here`.\n"
            + ASSESSMENT_RECORD_LINE + "\n"
        )
        hidden_canonical = refusal_repo(
            "inline-hidden-canonical", hidden_canonical_original,
            assessment_field=ASSESSMENT_RECORD,
        )
        refused, hidden_canonical_ordinary = run_atomic_refusal(hidden_canonical)
        flagged, hidden_canonical_flagged = run_atomic_refusal(
            hidden_canonical, "--open-assessment", plant=False
        )
        results.append((
            "exact canonical status inside multiline inline code refuses both calls untouched",
            hidden_canonical_ordinary and hidden_canonical_flagged and
            "0 status fields" in refused.stderr and
            not has_resume_instruction(refused.stdout + refused.stderr) and
            not has_resume_instruction(flagged.stdout + flagged.stderr) and
            (hidden_canonical / "product.md").read_text() == hidden_canonical_original,
        ))

        escaped_opener_original = (
            "# Backslash-escaped opener product\n\n"
            "An escaped opener \\`<!--` remains plain text.\n"
        )
        escaped_opener = refusal_repo(
            "backslash-escaped-opener", escaped_opener_original
        )
        refused, escaped_opener_ordinary = run_atomic_refusal(escaped_opener)
        flagged, escaped_opener_flagged = run_atomic_refusal(
            escaped_opener, "--open-assessment", plant=False
        )
        results.append((
            "a backslash-escaped backtick cannot shield a real comment",
            escaped_opener_ordinary and escaped_opener_flagged and
            "unclosed HTML comment" in refused.stderr and
            "unclosed HTML comment" in flagged.stderr,
        ))
        results.append((
            "even backslash parity leaves a balanced inline-code opener live",
            current_after_history(
                "even-backslash-parity",
                "Two literal backslashes \\\\`<!--` precede current evidence.",
            ),
        ))
        results.append((
            "backslash inside inline code does not escape its exact closer",
            current_after_history(
                "backslash-before-closer",
                "Inside `<!--\\` the backslash stays literal.",
            ),
        ))

        wrong_length_original = (
            "# Wrong backtick length product\n\n"
            "A two-run ``<!--``` cannot close with a three-run.\n"
        )
        wrong_length = refusal_repo("wrong-backtick-length", wrong_length_original)
        refused, wrong_length_ordinary = run_atomic_refusal(wrong_length)
        flagged, wrong_length_flagged = run_atomic_refusal(
            wrong_length, "--open-assessment", plant=False
        )
        results.append((
            "shorter or longer backtick runs cannot close a code span",
            wrong_length_ordinary and wrong_length_flagged and
            "unclosed HTML comment" in refused.stderr and
            "unclosed HTML comment" in flagged.stderr,
        ))

        multiline_unmatched_original = (
            "# Multiline unmatched opener product\n\n"
            "An unmatched ` opener starts here\n"
            "plain continuation exposes <!-- as a real comment.\n"
        )
        multiline_unmatched = refusal_repo(
            "multiline-unmatched", multiline_unmatched_original
        )
        refused, multiline_unmatched_ordinary = run_atomic_refusal(multiline_unmatched)
        flagged, multiline_unmatched_flagged = run_atomic_refusal(
            multiline_unmatched, "--open-assessment", plant=False
        )
        results.append((
            "unmatched multiline opener cannot hide a real comment",
            multiline_unmatched_ordinary and multiline_unmatched_flagged and
            "unclosed HTML comment" in refused.stderr and
            "unclosed HTML comment" in flagged.stderr,
        ))

        boundary_cases = {
            "blank-line": "Opening `<!--\n\nclosing `",
            "blockquote": "Opening `<!--\n> closing `",
            "fence": "Opening `<!--\n```text\nclosing `\n```",
            "ATX-heading": "Opening `<!--\n## closing `",
            "setext-heading": "Opening `<!--\nHeading\n---\nclosing `",
            "bullet-list": "Opening `<!--\n- closing `",
            "ordered-list": "Opening `<!--\n1. closing `",
            "indented-code": "Opening `<!--\n    closing `",
            "non-comment-HTML": "Opening `<!--\n<div>closing `</div>",
        }
        for boundary_name, body in boundary_cases.items():
            original = f"# {boundary_name} boundary product\n\n{body}\n"
            repo = refusal_repo("inline-boundary-" + boundary_name.lower(), original)
            refused, boundary_ok = run_atomic_refusal(repo)
            results.append((
                f"{boundary_name} boundary cannot close a multiline inline-code span",
                boundary_ok and "unclosed HTML comment" in refused.stderr and
                (repo / "product.md").read_text() == original,
            ))

        comment_first = "<!-- `-->` closes the real comment before backticks can act"
        results.append((
            "comment-first input owns backticks through its first close",
            current_after_history("comment-before-inline", comment_first),
        ))

        comment_then_unmatched_original = (
            "# Comment then unmatched inline opener product\n\n"
            + ASSESSMENT_HEADING + "\n"
            "<!-- retired history --> `unmatched on an inactive line\n"
            + ASSESSMENT_PENDING + "\n"
            + ASSESSMENT_RECORD_LINE + "\n"
        )
        comment_then_unmatched = refusal_repo(
            "comment-then-unmatched-inline", comment_then_unmatched_original,
            assessment_field=ASSESSMENT_RECORD,
        )
        comment_then_unmatched_run = run_cli(
            kernel, "upgrade", comment_then_unmatched
        )
        results.append((
            "a comment-touched line cannot span inline code over later clean evidence",
            upgrade_report_ok(
                comment_then_unmatched_run, RECOVERABLE_FIELDLESS_VERSION,
                "comment-then-unmatched-inlinefixture", source_checkout,
                surface_digest, NEXT_PENDING_CHANGED,
            ) and
            (comment_then_unmatched / "product.md").read_text() ==
            comment_then_unmatched_original and
            marker_ok(comment_then_unmatched, source_checkout, surface_digest,
                      ASSESSMENT_RECORD),
        ))

        comment_then_balanced_original = (
            "# Comment then balanced inline literal product\n\n"
            "<!-- retired history --> `<!-- stays literal -->`\n\n"
            + ASSESSMENT_BLOCK
        )
        comment_then_balanced = refusal_repo(
            "comment-then-balanced-inline", comment_then_balanced_original,
            assessment_field=ASSESSMENT_RECORD,
        )
        comment_then_balanced_run = run_cli(
            kernel, "upgrade", comment_then_balanced
        )
        results.append((
            "same-line code after a comment still shields comment-looking bytes",
            upgrade_report_ok(
                comment_then_balanced_run, RECOVERABLE_FIELDLESS_VERSION,
                "comment-then-balanced-inlinefixture", source_checkout,
                surface_digest, NEXT_PENDING_CHANGED,
            ) and
            (comment_then_balanced / "product.md").read_text() ==
            comment_then_balanced_original and
            marker_ok(comment_then_balanced, source_checkout, surface_digest,
                      ASSESSMENT_RECORD),
        ))

        quoted_and_fenced_inline = (
            "```markdown\n"
            "`<!--` stays fenced\n"
            "```\n"
            "> `<!--` stays quoted"
        )
        results.append((
            "fences and blockquotes isolate inline-code and comment-looking bytes",
            current_after_history("quoted-fenced-inline", quoted_and_fenced_inline),
        ))

        real_comment_after_inline = (
            "Literal `<!--` then real history <!--\n"
            + REJECTED_RC2_STATUS + "\n-->"
        )
        results.append((
            "real comment after a balanced inline span still opens",
            current_after_history("comment-after-inline", real_comment_after_inline),
        ))

        real_comment_after_multiline = (
            "Documentation `starts here\n"
            "continues and closes here` then real history <!--\n"
            + REJECTED_RC2_STATUS + "\n-->"
        )
        results.append((
            "text after a multiline closer is scanned while its touched line stays inactive",
            current_after_history(
                "comment-after-multiline-inline", real_comment_after_multiline
            ),
        ))

        literal_recovery_original = (
            "# Inline-literal recovery product\n\n"
            "The literal opener `<!--` stays byte-identical.\n"
        )
        literal_recovery = refusal_repo(
            "inline-literal-recovery", literal_recovery_original
        )
        refused, literal_recovery_refusal = run_atomic_refusal(literal_recovery)
        literal_recovery_refusal = (
            literal_recovery_refusal and
            refused.stderr.rstrip().endswith(AMBIGUITY_RETRY) and
            (literal_recovery / "product.md").read_text() == literal_recovery_original
        )
        results.append((
            "balanced inline literal preserves ordinary ambiguity refusal",
            literal_recovery_refusal,
        ))
        literal_recovery_state = (literal_recovery / "state.md").read_bytes()
        literal_recovery_dirt = (literal_recovery / "work/refusal-dirt.md").read_bytes()
        opened = run_cli(kernel, "upgrade", literal_recovery, "--open-assessment")
        literal_recovery_opened = (
            upgrade_report_ok(
                opened, RECOVERABLE_FIELDLESS_VERSION, "inline-literal-recoveryfixture",
                source_checkout, surface_digest, NEXT_PENDING_CHANGED,
            ) and
            "--open-assessment preserved every existing product byte" in opened.stdout and
            not has_resume_instruction(opened.stdout + opened.stderr) and
            (literal_recovery / "product.md").read_text() ==
            expected_product(literal_recovery_original) and
            (literal_recovery / "state.md").read_bytes() == literal_recovery_state and
            (literal_recovery / "work/refusal-dirt.md").read_bytes() ==
            literal_recovery_dirt and
            marker_ok(literal_recovery, source_checkout, surface_digest,
                      ASSESSMENT_RECORD)
        )
        results.append((
            "flagged recovery preserves the balanced inline literal and opens pending",
            literal_recovery_opened,
        ))

        completed_inline_status = (
            "**Speck Next upgrade assessment:** complete — resumed Piece alpha from state.md"
        )
        completed_inline_original = (
            "# Completed assessment after inline literal\n\n"
            "The literal opener `<!--` remains documentation.\n\n"
            + product_team() + "\n"
            + ASSESSMENT_HEADING + "\n\n"
            + completed_inline_status + "\n"
            + ASSESSMENT_RECORD_LINE + "\n"
        )
        completed_inline = refusal_repo(
            "completed-after-inline", completed_inline_original,
            assessment_field=ASSESSMENT_RECORD,
            record_content=assessment_record("Resume Piece alpha from state.md."),
        )
        completed_inline_run = run_cli(kernel, "upgrade", completed_inline)
        results.append((
            "balanced inline literal leaves the completed live-piece route current",
            upgrade_report_ok(
                completed_inline_run, RECOVERABLE_FIELDLESS_VERSION,
                "completed-after-inlinefixture", source_checkout, surface_digest,
                "Next: review the reported paths and complete diff, commit the upgrade, then resume Piece alpha from state.md.",
            ) and
            (completed_inline / "product.md").read_text() == completed_inline_original and
            marker_ok(completed_inline, source_checkout, surface_digest,
                      ASSESSMENT_RECORD),
        ))

        recovery_path("commit-only fieldless recovery")
        recovery_path(
            "provenance-laundered fieldless recovery",
            marker_extra={"sourceCheckout": "99a0f38", "methodSurfaceSha256": "a" * 64},
            flag_before=True,
        )

        flag_exclusion("explicit-null", "# Explicit null product\n", assessment_field=None)
        flag_exclusion(
            "valid-required",
            "# Required product\n\n" + ASSESSMENT_BLOCK,
            assessment_field=ASSESSMENT_RECORD,
        )
        flag_exclusion("fieldless-canonical", "# Canonical product\n\n" + ASSESSMENT_BLOCK)
        flag_exclusion("pre-v6", "# Pre-v6 product\n", version="5.4.1")
        flag_exclusion("rc1", f"# rc.1 product\n\n{RC1_STATUS}\n", version="6.0.0-rc.1")
        flag_exclusion("non-rc2-current", "# Later current product\n", version="6.0.0")
        flag_exclusion("generated-status", f"# Generated product\n\n{REJECTED_RC2_STATUS}\n")
        flag_exclusion("missing-product", None)
        flag_exclusion("missing-required-product", None, assessment_field=ASSESSMENT_RECORD)
        flag_exclusion("unsupported-pointer", "# Product\n", assessment_field="work/other.md")
        flag_exclusion("empty-pointer", "# Product\n", assessment_field="")
        flag_exclusion(
            "malformed-canonical",
            f"# Product\n\n{ASSESSMENT_HEADING}\n\n**Speck Next upgrade assessment:** finished\n{ASSESSMENT_RECORD_LINE}\n",
            assessment_field=ASSESSMENT_RECORD,
        )
        flag_exclusion(
            "completed-without-record",
            f"# Product\n\n{ASSESSMENT_HEADING}\n\n**Speck Next upgrade assessment:** complete — resumed Piece alpha from state.md\n{ASSESSMENT_RECORD_LINE}\n",
            assessment_field=ASSESSMENT_RECORD,
        )
        flag_exclusion(
            "duplicate-generated-status",
            f"# Product\n\n{REJECTED_RC2_STATUS}\n{REJECTED_RC2_STATUS}\n",
        )
        orphan_record = flag_exclusion(
            "orphan-record",
            "# Product with orphan record\n",
            record_content="# Orphan assessment record\n",
        )
        refused, unchanged = run_atomic_refusal(orphan_record, plant=False)
        results.append(("ordinary upgrade rejects an orphan assessment record", unchanged))

        directory_product = refusal_repo("flag-exclusion-directory-product", None)
        (directory_product / "product.md").mkdir()
        write_file(directory_product, "product.md/sentinel.txt", "directory product\n")
        commit_fixture(directory_product, "directory product")
        refused, unchanged = run_atomic_refusal(directory_product, "--open-assessment")
        results.append(("--open-assessment cannot override a directory product", unchanged))

        linked_product = refusal_repo("flag-exclusion-linked-product", None)
        (linked_product / "product.md").symlink_to("state.md")
        commit_fixture(linked_product, "linked product")
        refused, unchanged = run_atomic_refusal(linked_product, "--open-assessment")
        results.append(("--open-assessment requires a regular product file", unchanged))
        refused, unchanged = run_atomic_refusal(linked_product, plant=False)
        results.append(("ordinary upgrade rejects a linked product path", unchanged))

        optional_dir = refusal_repo("optional-directory", "# Optional-directory product\n")
        opened = run_cli_args(kernel, "upgrade", "--open-assessment", cwd=optional_dir)
        optional_dir_ok = (
            upgrade_report_ok(opened, RECOVERABLE_FIELDLESS_VERSION, "optional-directoryfixture",
                              source_checkout, surface_digest, NEXT_PENDING_CHANGED) and
            marker_ok(optional_dir, source_checkout, surface_digest, ASSESSMENT_RECORD) and
            (optional_dir / "product.md").read_text() ==
            expected_product("# Optional-directory product\n")
        )
        results.append(("--open-assessment accepts an omitted directory", optional_dir_ok))

        argv_target = refusal_repo("argv-target", "# Argument target\n")
        plant_refusal_dirt(argv_target)
        bad_argv = [
            ("standalone recovery option", ("--open-assessment",)),
            ("command-position unknown option", ("--unknown-option",)),
            ("duplicate option", ("upgrade", argv_target, "--open-assessment", "--open-assessment")),
            ("unknown option", ("upgrade", "--unknown-option", argv_target)),
            ("extra path", ("upgrade", argv_target, base / "second-target")),
            ("install option", ("install", argv_target, "--open-assessment")),
        ]
        for label, arguments in bad_argv:
            before = refusal_baseline(argv_target)
            refused = run_cli_args(kernel, *arguments)
            argv_ok = (
                refused.returncode != 0 and
                "No target was accessed and nothing was touched." in refused.stderr and
                snapshot_unchanged(argv_target, before)
            )
            results.append((f"bad argv rejects {label} before target access", argv_ok))

        fresh = base / "fresh"
        fresh.mkdir()
        init_repo(fresh)
        run = run_cli(kernel, "install", fresh)
        installed = [p for p in fresh.rglob("*") if p.is_file() and ".git" not in p.parts]
        fresh_ok = (run.returncode == 0 and marker(fresh)["version"] == CURRENT_VERSION and
                    marker_ok(fresh, source_checkout, surface_digest) and
                    not (fresh / "product.md").exists() and
                    len(installed) <= 20 and sum(p.stat().st_size for p in installed) <= 100_000 and
                    f"Installed Speck Next {provenance(CURRENT_VERSION, source_checkout, surface_digest)}" in run.stdout and
                    "Installed paths:" in run.stdout and "Next:" in run.stdout)
        results.append(("fresh install reports its surface and leaves product.md missing", fresh_ok))

        real_git = shutil.which("git")
        if real_git is None:
            raise AssertionError("git executable not found")

        def git_wrapper_env(name, body):
            wrapper_dir = base / name
            wrapper_dir.mkdir()
            wrapper = wrapper_dir / "git"
            wrapper.write_text(
                "#!/bin/sh\nset -eu\nREAL_GIT=" + shlex.quote(real_git) + "\n" +
                body.strip() + "\n"
            )
            wrapper.chmod(0o755)
            return {"PATH": str(wrapper_dir) + os.pathsep + os.environ["PATH"]}

        linked_templates = base / "linked-templates"
        linked_templates.mkdir()
        init_repo(linked_templates)
        outside_templates = base / "outside-templates"
        (outside_templates / "piece.md" / "inner").mkdir(parents=True)
        write_file(outside_templates, "piece.md/inner/note.txt", "outside wrong-kind descendant\n")
        write_file(outside_templates, "map.md", "outside templates history\n")
        os.symlink(outside_templates, linked_templates / "templates")
        outside_templates_before = snapshot_digest(outside_templates)
        linked_templates_run = run_cli(kernel, "install", linked_templates)
        preserved_root = next(linked_templates.glob(".speck-next-preserved*"), None)
        results.append((
            "linked templates localize from staged bytes and archive a wrong-kind descendant without touching the referent",
            linked_templates_run.returncode == 0 and
            'Localized linked path templates into this repository;' in linked_templates_run.stdout and
            "Preserved incompatible path templates/piece.md at .speck-next-preserved" in linked_templates_run.stdout and
            snapshot_digest(outside_templates) == outside_templates_before and
            (linked_templates / "templates").is_dir() and
            not (linked_templates / "templates").is_symlink() and
            (linked_templates / "templates" / "piece.md").is_file() and
            preserved_root is not None and
            any(path.name.startswith("templates__piece.md--")
                for path in preserved_root.iterdir()),
        ))

        preserved_retry = base / "preserved-retry"
        preserved_retry.mkdir()
        init_repo(preserved_retry)
        occupied_templates = base / "occupied-templates"
        (occupied_templates / "piece.md").mkdir(parents=True)
        write_file(occupied_templates, "piece.md/note.txt", "wrong kind\n")
        os.symlink(occupied_templates, preserved_retry / "templates")
        write_file(preserved_retry, ".speck-next-preserved", "occupied root\n")
        retry_run = run_cli(kernel, "install", preserved_retry)
        retry_root = preserved_retry / ".speck-next-preserved-2"
        results.append((
            "wrong-kind preservation retries past an occupied .speck-next-preserved root",
            retry_run.returncode == 0 and
            "Preserved incompatible path templates/piece.md at .speck-next-preserved-2/" in retry_run.stdout and
            retry_root.is_dir() and
            any(path.name.startswith("templates__piece.md--")
                for path in retry_root.iterdir()),
        ))

        grouped_claude = base / "grouped-claude"
        grouped_claude.mkdir()
        init_repo(grouped_claude)
        outside_claude = base / "outside-claude"
        (outside_claude / "skills" / "custom" / "readonly" / "deep").mkdir(parents=True)
        write_file(outside_claude, "skills/custom/readonly/deep/note.txt", "custom skill stays\n")
        write_file(outside_claude, "speck-next.json", '{"old": true}\n')
        os.chmod(outside_claude / "skills" / "custom", 0o555)
        os.chmod(outside_claude / "skills" / "custom" / "readonly", 0o555)
        os.chmod(outside_claude / "skills" / "custom" / "readonly" / "deep", 0o555)
        os.symlink(outside_claude, grouped_claude / ".claude")
        grouped_claude_before = snapshot_digest(outside_claude)
        grouped_claude_run = run_cli(kernel, "install", grouped_claude)
        results.append((
            "grouped .claude localization preserves custom skills, tolerates readonly directories, and forces the marker local",
            grouped_claude_run.returncode == 0 and
            'Localized linked path .claude into this repository;' in grouped_claude_run.stdout and
            snapshot_digest(outside_claude) == grouped_claude_before and
            (grouped_claude / ".claude").is_dir() and
            not (grouped_claude / ".claude").is_symlink() and
            (grouped_claude / ".claude" / "speck-next.json").is_file() and
            not (grouped_claude / ".claude" / "speck-next.json").is_symlink() and
            (grouped_claude / ".claude" / "skills" / "custom" / "readonly" / "deep" / "note.txt").read_text() == "custom skill stays\n",
        ))

        readonly_leaf = base / "readonly-leaf"
        readonly_leaf.mkdir()
        init_repo(readonly_leaf)
        readonly_outside = base / "readonly-leaf-outside"
        (readonly_outside / "skills" / "experience" / "references").mkdir(parents=True)
        write_file(readonly_outside, "skills/experience/references/walk.md", "old walk bytes\n")
        os.chmod(readonly_outside / "skills" / "experience" / "references" / "walk.md", 0o444)
        os.symlink(readonly_outside, readonly_leaf / ".claude")
        readonly_leaf_run = run_cli(kernel, "install", readonly_leaf)
        current_walk = (kernel / ".claude/skills/experience/references/walk.md").read_text()
        installed_walk = readonly_leaf / ".claude/skills/experience/references/walk.md"
        results.append((
            "canonical readonly staged files are recreated with current bytes and mode",
            readonly_leaf_run.returncode == 0 and
            installed_walk.read_text() == current_walk and
            (installed_walk.stat().st_mode & 0o777) == 0o644 and
            not installed_walk.is_symlink(),
        ))

        marker_link = base / "marker-link"
        marker_link.mkdir()
        init_repo(marker_link)
        (marker_link / ".claude").mkdir()
        outside_marker = base / "outside-marker.json"
        outside_marker.write_text('{"old": true}\n')
        os.symlink(outside_marker, marker_link / ".claude" / "speck-next.json")
        marker_before = outside_marker.read_text()
        marker_link_run = run_cli(kernel, "install", marker_link)
        results.append((
            "a linked marker localizes into the repository without changing its former target",
            marker_link_run.returncode == 0 and
            'Localized linked path .claude/speck-next.json into this repository;' in marker_link_run.stdout and
            outside_marker.read_text() == marker_before and
            (marker_link / ".claude" / "speck-next.json").is_file() and
            not (marker_link / ".claude" / "speck-next.json").is_symlink() and
            marker(marker_link)["version"] == CURRENT_VERSION,
        ))

        ignored_upgrade = base / "ignored-upgrade"
        ignored_upgrade.mkdir()
        init_repo(ignored_upgrade)
        (ignored_upgrade / ".git" / "info").mkdir(parents=True, exist_ok=True)
        write_file(ignored_upgrade, ".git/info/exclude", "templates/piece.md\n")
        write_file(ignored_upgrade, ".claude/speck-next.json", json.dumps({
            "name": "speck-next",
            "version": "5.4.1",
            "commit": "ignored-upgradefixture",
            "installedAt": "2026-01-02T03:04:05.000Z",
        }, indent=2) + "\n")
        write_file(ignored_upgrade, "product.md", "# Ignored upgrade product\n")
        write_file(ignored_upgrade, "templates/piece.md", "ignored owner bytes\n")
        commit_fixture(ignored_upgrade, "ignored upgrade baseline")
        ignored_run = run_cli(kernel, "upgrade", ignored_upgrade)
        results.append((
            "ignored untracked installed files stay visible in the complete surface status and diff",
            upgrade_report_ok(
                ignored_run, "5.4.1", "ignored-upgradefixture",
                source_checkout, surface_digest, NEXT_PENDING_CHANGED,
            ) and
            "!! templates/piece.md" in ignored_run.stdout and
            "diff --git a/templates/piece.md b/templates/piece.md" in ignored_run.stdout,
        ))

        fresh_report_fail = base / "fresh-report-fail"
        fresh_report_fail.mkdir()
        init_repo(fresh_report_fail)
        fresh_report_before = repo_baseline(fresh_report_fail)
        fail_status_env = git_wrapper_env(
            "git-fail-status",
            """
for arg in "$@"; do
  if [ "$arg" = "status" ]; then
    echo forced status failure >&2
    exit 1
  fi
done
exec "$REAL_GIT" "$@"
""",
        )
        failed_install = run_cli_args(kernel, "install", fresh_report_fail, env=fail_status_env)
        results.append((
            "late install report failures roll back every byte and first-missing ancestor",
            failed_install.returncode != 0 and
            "git status failed" in failed_install.stderr and
            repo_unchanged(fresh_report_fail, fresh_report_before) and
            not (fresh_report_fail / ".claude").exists() and
            not (fresh_report_fail / "templates").exists(),
        ))

        linked_fail = base / "linked-report-fail"
        linked_fail.mkdir()
        init_repo(linked_fail)
        linked_fail_outside = base / "linked-report-fail-outside"
        (linked_fail_outside / "piece.md").mkdir(parents=True)
        write_file(linked_fail_outside, "piece.md/note.txt", "outside bytes\n")
        os.symlink(linked_fail_outside, linked_fail / "templates")
        linked_fail_before = repo_baseline(linked_fail)
        linked_fail_outside_before = snapshot_digest(linked_fail_outside)
        failed_linked = run_cli_args(kernel, "install", linked_fail, env=fail_status_env)
        results.append((
            "late report failures after staged preservation restore the repo and leave linked referents unchanged",
            failed_linked.returncode != 0 and
            "git status failed" in failed_linked.stderr and
            repo_unchanged(linked_fail, linked_fail_before) and
            snapshot_digest(linked_fail_outside) == linked_fail_outside_before and
            (linked_fail / "templates").is_symlink(),
        ))

        git_attack = base / "git-attack"
        git_attack.mkdir()
        seed_upgrade_repo(
            git_attack, "5.4.1", "git-attackfixture",
            "# Git attack product\n",
        )
        attack_scripts = git_attack / "attack"
        attack_scripts.mkdir()
        attack_log = git_attack / "attack.log"
        diff_attack = attack_scripts / "external-diff.sh"
        diff_attack.write_text("#!/bin/sh\necho external-diff >> \"$1\"\n")
        diff_attack.chmod(0o755)
        textconv_attack = attack_scripts / "textconv.sh"
        textconv_attack.write_text("#!/bin/sh\necho textconv >> \"$1\"\ncat \"$2\"\n")
        textconv_attack.chmod(0o755)
        filter_attack = attack_scripts / "filter.sh"
        filter_attack.write_text("#!/bin/sh\necho filter >> \"$1\"\ncat\n")
        filter_attack.chmod(0o755)
        write_file(git_attack, ".gitattributes",
                   "*.md diff=attack\n*.md filter=attack\n")
        commit_fixture(git_attack, "git attack config")
        subprocess.run(["git", "config", "diff.external",
                        f"{diff_attack} {attack_log}"], cwd=git_attack, check=True)
        subprocess.run(["git", "config", "diff.attack.textconv",
                        f"{textconv_attack} {attack_log}"], cwd=git_attack, check=True)
        subprocess.run(["git", "config", "filter.attack.clean",
                        f"{filter_attack} {attack_log}"], cwd=git_attack, check=True)
        subprocess.run(["git", "config", "filter.attack.process",
                        f"{filter_attack} {attack_log}"], cwd=git_attack, check=True)
        subprocess.run(["git", "config", "filter.attack.required", "true"],
                       cwd=git_attack, check=True)
        git_attack_run = run_cli(kernel, "upgrade", git_attack)
        results.append((
            "upgrade reporting ignores local diff, textconv, and filter Git config",
            upgrade_report_ok(
                git_attack_run, "5.4.1", "git-attackfixture",
                source_checkout, surface_digest, NEXT_PENDING_CHANGED,
            ) and
            not attack_log.exists(),
        ))

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
                       upgrade_report_ok(second, CURRENT_VERSION, source_checkout, source_checkout,
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
                  upgrade_report_ok(second, CURRENT_VERSION, source_checkout, source_checkout,
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
        current_ok = (upgrade_report_ok(first, CURRENT_VERSION, source_checkout, source_checkout,
                                        surface_digest, NEXT_CURRENT_CLEAN, surface_digest) and
                      (current / "product.md").read_text() == current_product and
                      marker_ok(current, source_checkout, surface_digest) and
                      upgrade_report_ok(second, CURRENT_VERSION, source_checkout, source_checkout,
                                        surface_digest, NEXT_CURRENT_CLEAN, surface_digest) and
                      first_hash == surface_hash(current))
        results.append(("explicit-null current product resumes without an assessment", current_ok))

        current_missing = fixed_current("current-missing")
        first = run_cli(kernel, "upgrade", current_missing)
        second = run_cli(kernel, "upgrade", current_missing)
        current_missing_ok = (
            upgrade_report_ok(first, CURRENT_VERSION, source_checkout, source_checkout,
                              surface_digest, NEXT_MISSING_CLEAN, surface_digest) and
            "product.md is missing" in first.stdout and not (current_missing / "product.md").exists() and
            marker_ok(current_missing, source_checkout, surface_digest) and
            upgrade_report_ok(second, CURRENT_VERSION, source_checkout, source_checkout,
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
        retry_ok = (refusal_atomic and "product.md exists but is not a regular file" in failed.stderr and
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
        seed_upgrade_repo(rejected, RECOVERABLE_FIELDLESS_VERSION, "rejectedfixture", rejected_product)
        run = run_cli(kernel, "upgrade", rejected)
        repaired_text = (rejected / "product.md").read_text()
        rejected_ok = (
            upgrade_report_ok(run, RECOVERABLE_FIELDLESS_VERSION, "rejectedfixture", source_checkout,
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
            upgrade_report_ok(run, RECOVERABLE_FIELDLESS_VERSION, "fieldless-canonicalfixture",
                              source_checkout, surface_digest, NEXT_PENDING_CHANGED) and
            marker_ok(fieldless_canonical, source_checkout, surface_digest, ASSESSMENT_RECORD) and
            (fieldless_canonical / "product.md").read_text() == "# Current product\n\n" + ASSESSMENT_BLOCK)
        results.append(("fieldless current marker uses surviving canonical evidence",
                        fieldless_canonical_ok))

        fieldless_missing = refusal_repo("fieldless-missing-product", None)
        run = run_cli(kernel, "upgrade", fieldless_missing)
        fieldless_missing_ok = (
            upgrade_report_ok(run, RECOVERABLE_FIELDLESS_VERSION, "fieldless-missing-productfixture",
                              source_checkout, surface_digest, NEXT_MISSING_CHANGED) and
            marker_ok(fieldless_missing, source_checkout, surface_digest) and
            not (fieldless_missing / "product.md").exists())
        results.append(("fieldless current marker with no product safely records null",
                        fieldless_missing_ok))

        atomic_specs = [
            ("exact rejected-rc.2 deletion is ambiguous",
             "# Rejected migration with its generated assessment deleted\n", RECOVERABLE_FIELDLESS_VERSION,
             missing_field),
            ("fieldless current product is ambiguous",
             "# Fieldless current product\n", RECOVERABLE_FIELDLESS_VERSION, missing_field),
            ("unsupported assessment-record value",
             "# Product\n\n" + ASSESSMENT_BLOCK, RECOVERABLE_FIELDLESS_VERSION, "work/other.md"),
            ("empty assessment-record value",
             "# Product\n", RECOVERABLE_FIELDLESS_VERSION, ""),
            ("canonical block missing its status field",
             f"# Product\n\n{ASSESSMENT_HEADING}\n\n{ASSESSMENT_RECORD_LINE}\n",
             RECOVERABLE_FIELDLESS_VERSION, ASSESSMENT_RECORD),
            ("canonical block duplicates its status field",
             f"# Product\n\n{ASSESSMENT_HEADING}\n\n{ASSESSMENT_PENDING}\n{ASSESSMENT_PENDING}\n{ASSESSMENT_RECORD_LINE}\n",
             RECOVERABLE_FIELDLESS_VERSION, ASSESSMENT_RECORD),
            ("canonical block misses its record field",
             f"# Product\n\n{ASSESSMENT_HEADING}\n\n{ASSESSMENT_PENDING}\n",
             RECOVERABLE_FIELDLESS_VERSION, ASSESSMENT_RECORD),
            ("canonical block duplicates its record field",
             f"# Product\n\n{ASSESSMENT_HEADING}\n\n{ASSESSMENT_PENDING}\n{ASSESSMENT_RECORD_LINE}\n{ASSESSMENT_RECORD_LINE}\n",
             RECOVERABLE_FIELDLESS_VERSION, ASSESSMENT_RECORD),
            ("canonical block has the wrong record field",
             f"# Product\n\n{ASSESSMENT_HEADING}\n\n{ASSESSMENT_PENDING}\n**Record:** `work/wrong.md`\n",
             RECOVERABLE_FIELDLESS_VERSION, ASSESSMENT_RECORD),
            ("generated rc.1 fingerprint is duplicated",
             f"# Product\n\n{RC1_STATUS}\n{RC1_STATUS}\n", "6.0.0-rc.1", missing_field),
            ("generated rejected-rc.2 fingerprint is duplicated",
             f"# Product\n\n{REJECTED_RC2_STATUS}\n{REJECTED_RC2_STATUS}\n",
             RECOVERABLE_FIELDLESS_VERSION, missing_field),
        ]
        for label, product_text, version, assessment_field in atomic_specs:
            repo = refusal_repo(
                "atomic-" + re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-"),
                product_text, version, assessment_field,
            )
            refused, atomic = run_atomic_refusal(repo)
            results.append((f"{label} and refuses before every target write", atomic))
            if "ambiguous" not in label:
                flagged, flag_atomic = run_atomic_refusal(
                    repo, "--open-assessment", plant=False
                )
                results.append((f"--open-assessment cannot override {label}", flag_atomic))

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
                upgrade_report_ok(run, CURRENT_VERSION, source_checkout, source_checkout,
                                  surface_digest, expected_next, surface_digest) and
                marker_ok(repo, source_checkout, surface_digest, ASSESSMENT_RECORD) and
                assessment_record_ok((repo / ASSESSMENT_RECORD).read_text(), route) and
                before == surface_hash(repo) and
                (not retained or retained in (repo / "product.md").read_text()))
            results.append((f"completed assessment follows the {name} route", route_ok))

        owner_prose = ("# Owner-shaped product\n\n"
                       "These promises, punctuation, and spacing belong to the owner.\n")
        for name, status, route, state, expected_next, retained in route_specs:
            repo = seeded_pending(f"complete-{name.lower()}-twin", owner_prose)
            complete_pending(repo, status, route, state, retained)
            before = repository_snapshot(repo)
            run = run_cli(kernel, "upgrade", repo)
            twin_ok = (
                upgrade_report_ok(run, CURRENT_VERSION, source_checkout, source_checkout,
                                  surface_digest, expected_next, surface_digest) and
                owner_prose in (repo / "product.md").read_text() and
                before == repository_snapshot(repo)
            )
            results.append((f"canonical {name} twin preserves custom product prose byte for byte",
                            twin_ok))

        def completed_team_repo(name, team, status=None):
            status = status or (
                "**Speck Next upgrade assessment:** complete — resumed Piece alpha from state.md"
            )
            route = ("Map reopened." if status == ASSESSMENT_COMPLETE_MAP else
                     "Shape reopened." if status == ASSESSMENT_COMPLETE_SHAPE else
                     "Resume Piece alpha from state.md.")
            state = ("# State\n\nMap is reopened.\n" if status == ASSESSMENT_COMPLETE_MAP else
                     "# State\n\nShape is reopened.\n" if status == ASSESSMENT_COMPLETE_SHAPE else
                     "# State\n\nPiece alpha is live.\n")
            repo = seeded_pending(name)
            complete_pending(repo, status, route, state, team=team)
            return repo

        def product_team_refusal(label, team, expected, status=None, flagged=False):
            slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
            repo = completed_team_repo("team-refusal-" + slug, team, status)
            refused, atomic = run_atomic_refusal(repo)
            output = refused.stdout + refused.stderr
            accepted = (atomic and all(needle in output for needle in expected) and
                        "finish product.md's Product team section" in output and
                        ASSESSMENT_PENDING in output and
                        "continue Map from state.md" not in output and
                        not has_resume_instruction(output))
            results.append((f"{label} refuses with exact fields and full target unchanged",
                            accepted))
            if flagged:
                flagged_run, flagged_atomic = run_atomic_refusal(
                    repo, "--open-assessment", plant=False
                )
                flagged_output = flagged_run.stdout + flagged_run.stderr
                results.append((
                    f"--open-assessment cannot override {label}",
                    flagged_atomic and all(needle in flagged_output for needle in expected) and
                    "continue Map from state.md" not in flagged_output and
                    not has_resume_instruction(flagged_output),
                ))

        canonical_team = product_team()
        canonical_rows = canonical_team.split("\n", 1)[1]
        product_team_refusal(
            "round-five U+200B-only Product responsibility",
            product_team(product="\u200b"),
            ["Product: responsibility unusable"],
        )
        product_team_refusal(
            "U+2060-only Engineering responsibility",
            product_team(engineering="\u2060"),
            ["Engineering: responsibility unusable"],
        )
        product_team_refusal(
            "invisible-split TBD Product responsibility",
            product_team(product="T\u200bBD"),
            ["Product: responsibility unusable"],
        )
        product_team_refusal(
            "empty Product-team resume",
            "## Product team\n",
            ["Product: responsibility missing", "Business.Protects: missing",
             "Experience.Material changes: missing", "Engineering: responsibility missing"],
            flagged=True,
        )
        product_engineering_only = (
            "## Product team\n"
            "- **Product** — Keeps the promises and product order coherent.\n"
            "- **Engineering** — Keeps safe operation honest.\n"
        )
        product_team_refusal(
            "Product-and-Engineering-only resume",
            product_engineering_only,
            ["Business.Protects: missing", "Experience.Protects: missing"],
        )
        product_team_refusal(
            "empty Product-team Map route",
            "## Product team\n",
            ["Product: responsibility missing", "Business.Protects: missing"],
            status=ASSESSMENT_COMPLETE_MAP,
            flagged=True,
        )

        incomplete_shape = completed_team_repo(
            "incomplete-team-shape", "## Product team\n", ASSESSMENT_COMPLETE_SHAPE
        )
        incomplete_shape_before = repository_snapshot(incomplete_shape)
        incomplete_shape_run = run_cli(kernel, "upgrade", incomplete_shape)
        results.append((
            "an incomplete Product team may proceed only through completed Shape reopened",
            upgrade_report_ok(
                incomplete_shape_run, CURRENT_VERSION, source_checkout, source_checkout,
                surface_digest,
                "Next: there are no upgrade changes to commit; continue Shape from state.md.",
                surface_digest,
            ) and incomplete_shape_before == repository_snapshot(incomplete_shape),
        ))

        def without_role(team, role):
            return "\n".join(
                line for line in team.split("\n")
                if not line.startswith(f"- **{role}** —")
            )

        for role in ("Product", "Engineering"):
            product_team_refusal(
                f"missing {role} responsibility", without_role(canonical_team, role),
                [f"{role}: responsibility missing"],
            )
            for variant, value in (("blank", ""), ("bracket placeholder", "[responsibility]"),
                                   ("filler", "TBD")):
                args = {"product": None, "engineering": None}
                args[role.lower()] = value
                product_team_refusal(
                    f"{variant} {role} responsibility", product_team(**args),
                    [f"{role}: responsibility unusable"],
                )
        for filler in ("TODO", "none", "N/A", "placeholder"):
            product_team_refusal(
                f"explicit filler {filler} Product responsibility",
                product_team(product=filler),
                ["Product: responsibility unusable"],
            )

        canonical_conditional = {
            "Business": {
                "Protects": "sustainable adoption and operating cost",
                "Call when": "a change affects adoption, price, revenue, cost, or durable value",
                "May stay out when": "current measured evidence rules out those effects",
                "Evidence expires": "when that evidence ages past one milestone",
                "Material changes": "a new audience, channel, price, or cost model",
            },
            "Experience": {
                "Protects": "the journeys, surfaces, behavior, and declared feel",
                "Call when": "a change alters what a person sees, understands, or does",
                "May stay out when": "a current observed journey proves no user-facing effect",
                "Evidence expires": "when the observed journey or surface changes",
                "Material changes": "a new journey, surface, audience, or interaction",
            },
        }
        for role in ("Business", "Experience"):
            for field in PRODUCT_TEAM_FIELDS:
                for variant, value in (("missing", None), ("blank", ""),
                                       ("bracket placeholder", f"[{field}]"),
                                       ("filler", "TBD")):
                    values = dict(canonical_conditional[role])
                    if value is None:
                        values.pop(field)
                    else:
                        values[field] = value
                    kwargs = {role.lower(): values}
                    expected_kind = "missing" if value is None else "unusable"
                    product_team_refusal(
                        f"{variant} {role} {field}", product_team(**kwargs),
                        [f"{role}.{field}: {expected_kind}"],
                    )

        invisible_business = dict(canonical_conditional["Business"])
        invisible_business["Protects"] = "\ufe0f"
        product_team_refusal(
            "U+FE0F-only Business Protects",
            product_team(business=invisible_business),
            ["Business.Protects: unusable"],
        )

        visible_product = "Keeps\u200b the owner's visible responsibility."
        visible_team_repo = completed_team_repo(
            "visible-product-with-default-ignorable",
            product_team(product=visible_product),
        )
        visible_before = repository_snapshot(visible_team_repo)
        visible_product_before = (visible_team_repo / "product.md").read_bytes()
        visible_run = run_cli(kernel, "upgrade", visible_team_repo)
        visible_output = visible_run.stdout + visible_run.stderr
        results.append((
            "visible Product text containing U+200B stays accepted and byte-identical",
            upgrade_report_ok(
                visible_run, CURRENT_VERSION, source_checkout, source_checkout,
                surface_digest,
                "Next: there are no upgrade changes to commit; resume Piece alpha from state.md.",
                surface_digest,
            ) and
            repository_snapshot(visible_team_repo) == visible_before and
            (visible_team_repo / "product.md").read_bytes() == visible_product_before and
            visible_product.encode() in visible_product_before and
            "responsibility unusable" not in visible_output,
        ))

        product_team_refusal(
            "duplicate Product-team section", canonical_team + "\n" + canonical_team,
            ["Product team section: duplicate (2 current sections)"],
        )
        for role in ("Product", "Business", "Experience", "Engineering"):
            row = next(line for line in canonical_team.splitlines()
                       if line.startswith(f"- **{role}** —"))
            duplicated = canonical_team.replace(row, row + "\n" + row, 1)
            product_team_refusal(
                f"duplicate {role} row", duplicated, [f"{role}: duplicate row"]
            )

        def duplicate_field_team(role, field):
            team = canonical_team
            row = next(line for line in team.splitlines()
                       if line.startswith(f"- **{role}** —"))
            start = row.index(f"{field}: ")
            end = row.find(" · ", start)
            if end == -1:
                end = len(row)
            changed = row[:end] + f" · {field}: duplicate value" + row[end:]
            return team.replace(row, changed, 1)

        for role in ("Business", "Experience"):
            for field in PRODUCT_TEAM_FIELDS:
                product_team_refusal(
                    f"duplicate {role} {field}", duplicate_field_team(role, field),
                    [f"{role}.{field}: duplicate"],
                )

        inline_role_impostors = canonical_rows.replace("- **", "**")
        hidden_rows = {
            "blockquote": "\n".join("> " + line for line in canonical_rows.splitlines()) + "\n",
            "fence": "```markdown\n" + canonical_rows + "```\n",
            "HTML comment": "<!--\n" + canonical_rows + "-->\n",
            "multiline inline code": ("`hidden role declarations begin\n" +
                                      inline_role_impostors +
                                      "hidden role declarations end`\n"),
        }
        for container, hidden in hidden_rows.items():
            product_team_refusal(
                f"{container} Product-team row impostors",
                "## Product team\n" + hidden,
                ["Product: responsibility missing", "Business.Protects: missing",
                 "Experience.Protects: missing", "Engineering: responsibility missing"],
            )
            live_after = "## Product team\n" + hidden + canonical_rows
            repo = completed_team_repo(
                "live-after-" + re.sub(r"[^a-z0-9]+", "-", container.lower()),
                live_after,
            )
            before = repository_snapshot(repo)
            run = run_cli(kernel, "upgrade", repo)
            results.append((
                f"current Product-team rows after closed {container} remain usable",
                upgrade_report_ok(
                    run, CURRENT_VERSION, source_checkout, source_checkout,
                    surface_digest,
                    "Next: there are no upgrade changes to commit; resume Piece alpha from state.md.",
                    surface_digest,
                ) and before == repository_snapshot(repo),
            ))

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
            flagged, flag_corruption_ok = run_atomic_refusal(
                repo, "--open-assessment", plant=False
            )
            results.append((f"--open-assessment cannot override {name}",
                            flag_corruption_ok))

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
        flagged, missing_record_flag_ok = run_atomic_refusal(
            missing_record, "--open-assessment", plant=False
        )
        results.append(("--open-assessment cannot override missing completed record",
                        missing_record_flag_ok))

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
            provenance(CURRENT_VERSION, checkout_one, digest_one) in first.stdout and
            provenance(CURRENT_VERSION, checkout_two, digest_two) in second.stdout)
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
    dispositions_ok = run_result_disposition_controls()
    paths_ok = run_path_transaction_controls(kernel)
    migration_ok = run_migration_matrix(kernel)
    passed = homes_ok and roles_ok and assessments_ok and dispositions_ok and paths_ok and migration_ok
    print(f"Piece 8 controls: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if len(sys.argv) >= 2 and sys.argv[1] == "--piece-8-path-controls":
    if len(sys.argv) != 3:
        print("usage: check.py --piece-8-path-controls KERNEL", file=sys.stderr)
        sys.exit(2)
    sys.exit(0 if run_path_transaction_controls(pathlib.Path(sys.argv[2]).resolve()) else 1)

if len(sys.argv) >= 2 and sys.argv[1] == "--piece-8-controls":
    if len(sys.argv) != 3:
        print("usage: check.py --piece-8-controls KERNEL", file=sys.stderr)
        sys.exit(2)
    sys.exit(piece8_controls(sys.argv[2]))


if len(sys.argv) >= 2 and sys.argv[1] == "--result-disposition-controls":
    if len(sys.argv) != 2:
        print("usage: check.py --result-disposition-controls", file=sys.stderr)
        sys.exit(2)
    sys.exit(0 if run_result_disposition_controls() else 1)


clone = sys.argv[1]
pulse_dir = os.path.join(clone, "examples", "pulse")
default_git = os.path.join(clone, ".devsuite-git" if os.path.isdir(os.path.join(clone, ".devsuite-git")) else ".git")
git_dir = os.environ.get("GIT_DIR", default_git)
git_env = dict(os.environ, GIT_DIR=git_dir, GIT_WORK_TREE=os.path.abspath(clone))
baseline_path = os.path.join(git_dir, "devsuite-baseline")
baseline = open(baseline_path).read().strip()
ok = run_result_disposition_controls()


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
authorization_text = record.lower()
note("the piece declared the token estimate and prospectively enforceable model-work authorization",
     "token estimate" in authorization_text and "250,000" in authorization_text and
     bool(re.search(r"(?:four|4) host contexts", authorization_text)) and
     "900" in authorization_text and
     bool(re.search(r"(?:zero|0) retries", authorization_text)) and
     bool(re.search(r"(?:zero|0) fallbacks", authorization_text)) and
     bool(re.search(r"(?:zero|0) owner interruptions", authorization_text)) and
     "300" in authorization_text and "30 files" in authorization_text)

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
token_estimate = metrics.get("token_estimate", 250000)
token_usage = host.get("token_usage", {"gross": host.get("tokens", 0), "cached": 0,
                                       "fresh": host.get("tokens", 0)})
cost_finding = token_usage["gross"] > token_estimate
print(f"  [measure] elapsed={metrics.get('elapsed_seconds', 0)}s "
      f"gross={token_usage['gross']} cached={token_usage['cached']} fresh={token_usage['fresh']} "
      f"estimate={token_estimate} cost_finding={'yes' if cost_finding else 'no'}")
note("token use is measured against its estimate as cost evidence, not a product kill",
     token_estimate > 0 and token_usage["gross"] > 0 and
     token_usage["gross"] - token_usage["cached"] == token_usage["fresh"] and
     metrics.get("token_usage") == token_usage)
note("prospective elapsed-time authorization held",
     0 < metrics.get("elapsed_seconds", 0) <= 900)

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
