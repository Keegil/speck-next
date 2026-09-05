#!/usr/bin/env python3
"""Verify role contexts from runner-owned or canonical host records."""
import json, os, pathlib, re, sys, tempfile

ROLES = ("Business", "Experience", "Engineering")
STAGES = {"Business": ("contribution", "return"), "Experience": ("contribution", "return"),
          "Engineering": ("contribution", "implement", "return")}
NEEDLES = {"Business": "business-evidence.md", "Experience": "experience-evidence.md", "Engineering": "pulse.py"}
USAGE_FIELDS = ("gross", "cached", "fresh", "responses")
PROBE_NAMES = ("contributions", "product", "business", "engineering")
ADMISSION_FIELDS = ("driver", "model", "candidate", "runner_sha256", "packet_schema",
                    "source_manifest_sha256")


def jsonl(path):
    if not path or not pathlib.Path(path).is_file():
        return []
    rows = []
    for line in pathlib.Path(path).read_text(errors="ignore").splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return rows


def empty_usage():
    return {field: 0 for field in USAGE_FIELDS}


def add_usage(*values):
    total = empty_usage()
    for value in values:
        for field in USAGE_FIELDS:
            total[field] += int(value.get(field, 0) or 0)
    return total


def usage_delta(after, before):
    value = {field: int(after.get(field, 0) or 0) - int(before.get(field, 0) or 0)
             for field in USAGE_FIELDS}
    if any(amount < 0 for amount in value.values()):
        raise ValueError("usage counters moved backwards")
    return value


def codex_usage_rows(rows):
    """Return one Codex session's cumulative usage without double-counting reasoning."""
    latest = {}
    responses = 0
    for event in rows:
        payload = event.get("payload", {})
        if event.get("type") == "event_msg" and payload.get("type") == "token_count":
            candidate = payload.get("info", {}).get("total_token_usage", {})
            if candidate:
                latest = candidate
        if ((event.get("type") == "event_msg" and payload.get("type") == "task_complete") or
                event.get("type") == "turn.completed"):
            responses += 1
    input_tokens = int(latest.get("input_tokens", 0) or 0)
    cached = int(latest.get("cached_input_tokens", 0) or 0)
    output = int(latest.get("output_tokens", 0) or 0)
    gross = int(latest.get("total_tokens", input_tokens + output) or 0)
    return {"gross": gross, "cached": cached, "fresh": input_tokens - cached + output,
            "responses": responses}


def claude_usage_rows(rows):
    """Return cumulative Claude usage; cache creation is fresh and cache reads are not."""
    messages = {}
    responses = 0
    for row in rows:
        message = row.get("message", {})
        if isinstance(message, dict) and message.get("role") == "assistant" and message.get("id"):
            messages[message["id"]] = message.get("usage", {})
        if row.get("type") == "result" and row.get("subtype") not in ("error", "error_max_turns"):
            responses += 1
    gross = cached = fresh = 0
    for usage in messages.values():
        uncached = int(usage.get("input_tokens", 0) or 0)
        created = int(usage.get("cache_creation_input_tokens", 0) or 0)
        read = int(usage.get("cache_read_input_tokens", 0) or 0)
        output = int(usage.get("output_tokens", 0) or 0)
        gross += uncached + created + read + output
        cached += read
        fresh += uncached + created + output
    return {"gross": gross, "cached": cached, "fresh": fresh, "responses": responses}


def stage_verdict(usage, elapsed, limits, complete):
    reasons = []
    for field in ("gross", "fresh", "responses"):
        if int(usage.get(field, 0) or 0) > int(limits[field]):
            reasons.append(field)
    if float(elapsed) > float(limits["wall"]):
        reasons.append("wall")
    status = "over" if reasons else ("passed" if complete else "incomplete")
    return {"status": status, "reasons": reasons, "usage": dict(usage), "elapsed": elapsed,
            "limits": dict(limits), "complete": bool(complete)}


def intervals_overlap(intervals):
    if not intervals or any(len(interval) != 2 or interval[1] < interval[0] for interval in intervals):
        return False
    return max(interval[0] for interval in intervals) < min(interval[1] for interval in intervals)


def continuity_ok(expected, observed):
    return bool(expected) and set(expected) == set(observed) and all(
        expected[role] and expected[role] == observed[role] for role in expected)


def admission_ok(receipt, expected):
    if not all(receipt.get(field) == expected.get(field) and expected.get(field)
               for field in ADMISSION_FIELDS):
        return False
    probes = receipt.get("probes", {})
    return set(probes) == set(PROBE_NAMES) and all(
        isinstance(probes[name], dict) and probes[name].get("status") == "passed"
        for name in PROBE_NAMES)


def root_identity(driver, events_path):
    for event in jsonl(events_path):
        if driver == "codex" and event.get("type") == "thread.started" and event.get("thread_id"):
            return event["thread_id"]
        value = event.get("session_id") or event.get("sessionId")
        if driver == "claude" and value:
            return value
    return None


def codex_usage(path):
    return codex_usage_rows(jsonl(path))["gross"]


def codex_meta(path):
    rows = jsonl(path)
    if rows and rows[0].get("type") == "session_meta":
        return rows[0].get("payload", {})
    return {}


def codex_root_path(root_id, sessions_root=None):
    base = pathlib.Path(sessions_root or pathlib.Path.home() / ".codex" / "sessions")
    matches = list(base.rglob(f"*{root_id}.jsonl")) if root_id and base.exists() else []
    return next((path for path in matches if codex_meta(path).get("id") == root_id), None)


def codex_session_blobs(path):
    outputs, direct, received = [], [], []
    for event in jsonl(path):
        payload = event.get("payload", {})
        if event.get("type") == "event_msg" and payload.get("type") in ("agent_message", "task_complete"):
            text = payload.get("message") or payload.get("last_agent_message")
            if isinstance(text, str):
                outputs.append(text)
        if event.get("type") == "response_item" and payload.get("type") in ("custom_tool_call", "function_call"):
            value = payload.get("input") or payload.get("arguments")
            if isinstance(value, str):
                direct.append(value)
        if event.get("type") == "response_item" and payload.get("type") == "agent_message":
            author = payload.get("author")
            text = json.dumps(payload.get("content", []), ensure_ascii=False)
            if author and isinstance(text, str):
                received.append((author, text))
    return "\n".join(outputs), "\n".join(direct), received


def broker_codex(clone, events_path, state_path, carriers):
    result = {"root": False, "roles": {}, "tokens": 0, **empty_usage(),
              "root_id": None, "extra_contexts": 0}
    root_id = root_identity("codex", events_path)
    result["root_id"] = root_id
    state = json.loads(pathlib.Path(state_path).read_text()) if state_path and pathlib.Path(state_path).is_file() else {}
    home = state.get("home")
    sessions_root = pathlib.Path(home) / "sessions" if home else state.get("evidence_sessions")
    sessions_root = pathlib.Path(sessions_root) if sessions_root else None
    product_home = state.get("root_home")
    root_sessions = pathlib.Path(product_home) / "sessions" if product_home else state.get("evidence_root_sessions")
    root_sessions = pathlib.Path(root_sessions) if root_sessions else None
    root_path = codex_root_path(root_id, root_sessions) if root_sessions else codex_root_path(root_id)
    root_direct = ""
    if root_path:
        meta = codex_meta(root_path)
        result["root"] = pathlib.Path(meta.get("cwd", "")).resolve() == pathlib.Path(clone).resolve()
        _, root_direct, _ = codex_session_blobs(root_path)
    if not state:
        if root_path:
            usage = codex_usage_rows(jsonl(root_path))
            result.update(usage)
            result["tokens"] = usage["gross"]
        return result
    if pathlib.Path(state.get("root", "")).resolve() != pathlib.Path(clone).resolve():
        return result
    session_paths = list(sessions_root.rglob("*.jsonl")) if sessions_root and sessions_root.exists() else []
    root_paths = list(root_sessions.rglob("*.jsonl")) if root_sessions and root_sessions.exists() else []
    all_paths = list(dict.fromkeys(session_paths + root_paths))
    usage = add_usage(*(codex_usage_rows(jsonl(path)) for path in all_paths))
    result.update(usage)
    result["tokens"] = usage["gross"]
    expected_ids = {value for value in (root_id, *state.get("sessions", {}).values()) if value}
    actual_ids = {meta.get("id") for meta in map(codex_meta, all_paths) if meta.get("id")}
    result["extra_contexts"] = len(actual_ids - expected_ids)
    structured_actions = []
    for event in jsonl(events_path):
        item = event.get("item", {})
        if item.get("type") == "command_execution" and isinstance(item.get("command"), str):
            structured_actions.append(item["command"])
        if item.get("type") == "file_change":
            structured_actions.extend(change.get("path", "") for change in item.get("changes", []))
    action_blob = root_direct + "\n" + "\n".join(structured_actions)
    for role in ROLES:
        carrier = state.get("sessions", {}).get(role)
        path = codex_root_path(carrier, sessions_root)
        if not carrier or not path:
            continue
        if carriers and carriers.get(role) != carrier:
            continue
        meta = codex_meta(path)
        outputs, direct, _ = codex_session_blobs(path)
        stages = state.get("events", {}).get(role, {})
        stage_direct = "\n".join(
            event.get("item", {}).get("command", "")
            for stage_path in stages.values() for event in jsonl(stage_path)
            if event.get("item", {}).get("type") == "command_execution")
        requests_ok = True
        for stage in STAGES[role]:
            name = f"{role.lower()}-{stage}.json"
            request_path = pathlib.Path(clone) / ".devsuite-role-ipc" / "requests" / name
            try:
                request = json.loads(request_path.read_text())
            except (OSError, json.JSONDecodeError):
                requests_ok = False
                continue
            requests_ok = (requests_ok and request.get("role") == role and request.get("stage") == stage and
                           name in action_blob and f"{role.lower()}-{stage}" in state.get("handled", []))
        role_line = bool(re.search(rf"(?m)^Role:\s*{role}\s*$", outputs))
        direct_read = NEEDLES[role].lower() in (direct + "\n" + stage_direct).lower()
        returned = bool(re.search(r"first(?:-| )?(?:real )?run", outputs, re.I) and
                        re.search(r"\b(changed|held)\b", outputs, re.I))
        rulings = re.findall(r"Business ruling:\s*(kept|broken|not[- ]judged)\b", outputs, re.I) if role == "Business" else []
        ruling = rulings[-1].lower() if rulings else None
        if role == "Business":
            returned = returned and bool(ruling)
        precode_clean = True
        if role == "Engineering":
            for event in jsonl(stages.get("contribution")):
                item = event.get("item", {})
                if item.get("type") == "file_change" and any(
                        str(change.get("path", "")).startswith(str(pathlib.Path(clone).resolve()))
                        for change in item.get("changes", [])):
                    precode_clean = False
                command = item.get("command", "") if item.get("type") == "command_execution" else ""
                if re.search(r"(?:apply_patch|git\s+(?:add|commit)|sed\s+-i|perl\s+-i|\btee\b|>>)", command):
                    precode_clean = False
        result["roles"][role] = {
            "carrier": carrier,
            "host": meta.get("id") == carrier and
                    pathlib.Path(meta.get("cwd", "")).resolve() == pathlib.Path(state.get("role_cwd", "")).resolve(),
            "contribution": role_line and NEEDLES[role].lower() in outputs.lower(),
            "direct": direct_read,
            "elected": requests_ok and all(stage in stages for stage in STAGES[role]),
            "returned": returned,
            "ruling_permits": role != "Business" or ruling == "kept",
            "precode_clean": precode_clean,
        }
    return result


def nested_dicts(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from nested_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from nested_dicts(child)


def claude_usage(rows):
    return claude_usage_rows(rows)["gross"]


def canonical_claude_root(root_id, projects_root=None):
    base = pathlib.Path(projects_root or pathlib.Path.home() / ".claude" / "projects")
    matches = list(base.rglob(f"{root_id}.jsonl")) if root_id and base.exists() else []
    return matches[0] if matches else None


def claude_agent_records(rows):
    launches, results = {}, {}
    for row in rows:
        for item in nested_dicts(row):
            if item.get("type") == "tool_use" and item.get("name") == "Agent":
                launches[item.get("id")] = item.get("input", {})
        tool_result = row.get("toolUseResult") or row.get("tool_use_result")
        content = row.get("message", {}).get("content", []) if isinstance(row.get("message"), dict) else []
        if isinstance(tool_result, dict) and isinstance(content, list):
            tool_id = next((x.get("tool_use_id") for x in content if isinstance(x, dict) and x.get("tool_use_id")), None)
            if tool_id:
                results[tool_id] = tool_result
    return launches, results


def native_claude(clone, events_path, carriers, projects_root=None):
    result = {"root": False, "roles": {}, "tokens": 0, **empty_usage(),
              "root_id": root_identity("claude", events_path), "extra_contexts": 0}
    root_path = canonical_claude_root(result["root_id"], projects_root)
    if not root_path:
        return result
    rows = jsonl(root_path)
    result["root"] = any(row.get("sessionId") == result["root_id"] and
                         pathlib.Path(row.get("cwd", "")).resolve() == pathlib.Path(clone).resolve() for row in rows)
    usage_parts = [claude_usage_rows(rows)]
    launches, results = claude_agent_records(rows)
    trusted = pathlib.Path(projects_root or pathlib.Path.home() / ".claude" / "projects").resolve()
    child_records = {}
    pending = [meta.get("outputFile") for meta in results.values() if meta.get("outputFile")]
    while pending:
        output = pending.pop()
        path = pathlib.Path(output).resolve()
        try:
            trusted_path = os.path.commonpath((str(trusted), str(path))) == str(trusted)
        except ValueError:
            trusted_path = False
        if not trusted_path or path in child_records:
            continue
        child_rows = jsonl(path)
        child_records[path] = child_rows
        usage_parts.append(claude_usage_rows(child_rows))
        child_launches, child_results = claude_agent_records(child_rows)
        result["extra_contexts"] += len(child_launches)
        pending.extend(meta.get("outputFile") for meta in child_results.values() if meta.get("outputFile"))
    role_counts = {role: 0 for role in ROLES}
    for call_id, launch in launches.items():
        name = launch.get("name") or launch.get("description")
        role = next((r for r in ROLES if r.lower() in str(name).lower()), None)
        meta = results.get(call_id, {})
        agent_id, output = meta.get("agentId"), meta.get("outputFile")
        if not role:
            continue
        role_counts[role] += 1
        if not agent_id or not output or carriers.get(role) != agent_id:
            continue
        path = pathlib.Path(output).resolve()
        child_rows = child_records.get(path, [])
        child_blob = json.dumps(child_rows, ensure_ascii=False)
        direct = "\n".join(str(item.get("input", "")) for row in child_rows for item in nested_dicts(row)
                           if item.get("type") == "tool_use" and item.get("name") in ("Read", "Glob", "Grep", "Bash"))
        precode_clean = True
        if role == "Engineering":
            for row in child_rows:
                row_blob = json.dumps(row, ensure_ascii=False)
                if re.search(r"Role:\s*Engineering", row_blob):
                    break
                for item in nested_dicts(row):
                    if item.get("type") == "tool_use" and item.get("name") in ("Write", "Edit", "NotebookEdit"):
                        precode_clean = False
                    if item.get("type") == "tool_use" and item.get("name") == "Bash" and re.search(
                            r"(?:apply_patch|git\s+(?:add|commit)|sed\s+-i|perl\s+-i|\btee\b|>>)", str(item.get("input", ""))):
                        precode_clean = False
        returned = bool(re.search(r"first(?:-| )?(?:real )?run", child_blob, re.I) and
                        re.search(r"\b(changed|held)\b", child_blob, re.I))
        rulings = re.findall(r"Business ruling:\s*(kept|broken|not[- ]judged)\b", child_blob, re.I) if role == "Business" else []
        ruling = rulings[-1].lower() if rulings else None
        if role == "Business":
            returned = returned and bool(ruling)
        result["roles"][role] = {
            "carrier": agent_id, "host": bool(child_rows) and all(not row.get("agentId") or row.get("agentId") == agent_id for row in child_rows),
            "contribution": bool(re.search(rf"Role:\s*{role}", child_blob)) and NEEDLES[role] in child_blob,
            "direct": NEEDLES[role] in direct, "elected": True,
            "returned": returned,
            "ruling_permits": role != "Business" or ruling == "kept",
            "precode_clean": precode_clean,
        }
    for role, count in role_counts.items():
        if role in result["roles"] and count != 1:
            result["roles"][role]["host"] = False
    result["extra_contexts"] += max(0, len(launches) - 3)
    usage = add_usage(*usage_parts)
    result.update(usage)
    result["tokens"] = usage["gross"]
    return result


def proof(driver, clone, events_path, carriers, state_path=None):
    return broker_codex(clone, events_path, state_path, carriers) if driver == "codex" else native_claude(clone, events_path, carriers)


def self_test(verbose=True):
    with tempfile.TemporaryDirectory(prefix="speck-host-proof-fixture.") as folder:
        base = pathlib.Path(folder)
        projects = base / "projects"; projects.mkdir()
        clone = base / "clone"; clone.mkdir()
        root_id = "root-session"; agent = "agent-business"
        events = base / "events.jsonl"
        events.write_text(json.dumps({"session_id": root_id}) + "\n")
        root = projects / "encoded" / f"{root_id}.jsonl"; root.parent.mkdir()
        root.write_text(json.dumps({"sessionId": root_id, "cwd": str(clone), "message": {"role": "assistant", "id": "m1", "usage": {"input_tokens": 2}, "content": [{"type": "tool_use", "id": "t1", "name": "Agent", "input": {"name": "pulse-business"}}]}}) + "\n" +
                        json.dumps({"message": {"content": [{"tool_use_id": "t1"}]}, "toolUseResult": {"agentId": agent, "outputFile": str(projects / "child.jsonl")}}) + "\n")
        child = projects / "child.jsonl"
        child.write_text(json.dumps({"agentId": agent, "message": {"role": "assistant", "id": "c1", "usage": {"output_tokens": 3}, "content": [{"type": "tool_use", "name": "Read", "input": {"file_path": "business-evidence.md"}}, {"type": "text", "text": "Role: Business business-evidence.md. First real run held. Business ruling: broken"}]}}) + "\n")
        good = native_claude(clone, events, {"Business": agent}, projects)
        broken_text = child.read_text()
        child.write_text(broken_text.replace("Business ruling: broken", "Business ruling: not judged"))
        not_judged = native_claude(clone, events, {"Business": agent}, projects)
        child.write_text(broken_text)
        grandchild = projects / "grandchild.jsonl"
        grandchild.write_text(json.dumps({"agentId": "agent-helper", "message": {"role": "assistant", "id": "g1", "usage": {"output_tokens": 7}, "content": []}}) + "\n")
        child.write_text(child.read_text() +
                         json.dumps({"agentId": agent, "message": {"role": "assistant", "id": "c2", "content": [{"type": "tool_use", "id": "nested", "name": "Agent", "input": {"name": "helper"}}]}}) + "\n" +
                         json.dumps({"agentId": agent, "message": {"content": [{"tool_use_id": "nested"}]}, "toolUseResult": {"agentId": "agent-helper", "outputFile": str(grandchild)}}) + "\n")
        nested = native_claude(clone, events, {"Business": agent}, projects)
        forged = clone / "forged"; forged.mkdir(); (forged / "child.jsonl").write_text(child.read_text())
        value = json.loads(root.read_text().splitlines()[1]); value["toolUseResult"]["outputFile"] = str(forged / "child.jsonl")
        root.write_text(root.read_text().splitlines()[0] + "\n" + json.dumps(value) + "\n")
        bad = native_claude(clone, events, {"Business": agent}, projects)
        codex_root = base / "codex-root" / "sessions"; codex_root.mkdir(parents=True)
        codex_roles = base / "codex-roles" / "sessions"; codex_roles.mkdir(parents=True)
        codex_events = base / "codex-events.jsonl"
        codex_events.write_text(json.dumps({"type": "thread.started", "thread_id": root_id}) + "\n")
        (codex_root / f"{root_id}.jsonl").write_text(json.dumps({"type": "session_meta", "payload": {"id": root_id, "cwd": str(clone)}}) + "\n")
        role_id = "role-business"
        (codex_roles / f"{role_id}.jsonl").write_text(json.dumps({"type": "session_meta", "payload": {"id": role_id, "cwd": str(base)}}) + "\n")
        (codex_roles / "role-helper.jsonl").write_text(json.dumps({"type": "session_meta", "payload": {"id": "role-helper", "parent_thread_id": role_id, "cwd": str(base)}}) + "\n")
        codex_state = base / "codex-state.json"
        codex_state.write_text(json.dumps({"root": str(clone), "role_cwd": str(base),
                                           "home": str(codex_roles.parent), "root_home": str(codex_root.parent),
                                           "sessions": {"Business": role_id}, "events": {}, "handled": []}))
        codex_nested = broker_codex(clone, codex_events, codex_state, {})
        passed = bool(good["roles"].get("Business", {}).get("host") and
                      good["roles"]["Business"].get("returned") and
                      not good["roles"]["Business"].get("ruling_permits") and
                      not_judged["roles"]["Business"].get("returned") and
                      not not_judged["roles"]["Business"].get("ruling_permits") and
                      nested.get("extra_contexts") == 1 and
                      nested.get("tokens") == 12 and
                      codex_nested.get("extra_contexts") == 1 and
                      not bad["roles"].get("Business", {}).get("host"))
    if verbose:
        print(f"host parser fixtures: {'PASS' if passed else 'FAIL'}; codex_extra={codex_nested.get('extra_contexts')} "
              f"claude_extra={nested.get('extra_contexts')} descendant_tokens={nested.get('tokens')} "
              f"business_returned={good['roles'].get('Business', {}).get('returned')} "
              f"business_permits={good['roles'].get('Business', {}).get('ruling_permits')} "
              f"not_judged_returned={not_judged['roles'].get('Business', {}).get('returned')} forged_host_rejected=True")
    return passed


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        raise SystemExit(0 if self_test() else 1)
    if len(sys.argv) >= 5 and sys.argv[1] == "metrics":
        driver, clone, events = sys.argv[2:5]
        state = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != "-" else None
        value = proof(driver, clone, events, {}, state)
        if len(sys.argv) > 6:
            value["elapsed_seconds"] = int(sys.argv[6])
        if len(sys.argv) > 7:
            value["token_limit"] = int(sys.argv[7])
        print(json.dumps(value, sort_keys=True))
    else:
        raise SystemExit("usage: host_proof.py --self-test | metrics DRIVER CLONE EVENTS [STATE]")
