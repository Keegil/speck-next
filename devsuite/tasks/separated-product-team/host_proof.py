#!/usr/bin/env python3
"""Verify role contexts from runner-owned or canonical host records."""
import json, math, os, pathlib, re, sys, tempfile
import base64, hashlib

ROLES = ("Business", "Experience", "Engineering")
STAGES = {"Business": ("contribution", "return"), "Experience": ("contribution", "return"),
          "Engineering": ("contribution", "implement", "return")}
NEEDLES = {"Business": "business-evidence.md", "Experience": "experience-evidence.md", "Engineering": "pulse.py"}
USAGE_FIELDS = ("gross", "cached", "fresh", "responses")
PROBE_NAMES = ("contributions", "product", "business", "engineering")
ADMISSION_FIELDS = ("driver", "host", "model", "candidate", "runner_sha256", "packet_schema",
                    "source_manifest_sha256")
STAGE_ORDER = ("product_select", "contributions", "product_synthesis", "engineering",
               "returns", "product_close")
STAGE_LIMITS = {
    "product_select": {"gross": 21000, "fresh": 12000, "wall": 45, "responses": 1},
    "contributions": {"gross": 54000, "fresh": 32000, "wall": 90, "responses": 3},
    "product_synthesis": {"gross": 26000, "fresh": 18000, "wall": 60, "responses": 1},
    "engineering": {"gross": 70000, "fresh": 55000, "wall": 360, "responses": 3},
    "returns": {"gross": 40000, "fresh": 24000, "wall": 90, "responses": 2},
    "product_close": {"gross": 24000, "fresh": 19000, "wall": 60, "responses": 1},
}
PROBE_LIMITS = {
    "business": {"gross": 38000, "fresh": 22000, "wall": 180, "responses": 2},
    "contributions": STAGE_LIMITS["contributions"],
    "product": {"gross": 47000, "fresh": 30000, "wall": 105, "responses": 2},
    "engineering": {"gross": 88000, "fresh": 67000, "wall": 450, "responses": 4},
}
FULL_LIMITS = {"gross": 250000, "fresh": 200000, "wall": 900, "responses": 11}
PROBE_STAGES = {
    "contributions": ("business_contribution", "experience_contribution", "engineering_contribution"),
    "product": ("product_select", "product_synthesis"),
    "business": ("business_contribution", "business_return"),
    "engineering": ("engineering_contribution", "engineering_implement",
                    "engineering_run", "engineering_return"),
}
SOURCE_PATHS = {
    "product": "examples/pulse/product.md",
    "business": "examples/pulse/evidence/business-evidence.md",
    "experience": "examples/pulse/evidence/experience-evidence.md",
    "engineering": "examples/pulse/pulse.py",
}
ALL_SOURCE_PATHS = tuple(SOURCE_PATHS.values())
SOURCE_ALLOWLIST = {
    ("source-manifest", "runner"): ALL_SOURCE_PATHS,
    ("product_select", "Product"): ALL_SOURCE_PATHS,
    ("contribution", "Business"): (SOURCE_PATHS["product"], SOURCE_PATHS["business"]),
    ("contribution", "Experience"): (SOURCE_PATHS["product"], SOURCE_PATHS["experience"]),
    ("contribution", "Engineering"): (SOURCE_PATHS["product"], SOURCE_PATHS["engineering"]),
    ("product_synthesis", "Product"): ALL_SOURCE_PATHS,
    ("implement", "Engineering"): (SOURCE_PATHS["product"], SOURCE_PATHS["engineering"]),
    ("run", "Engineering"): (SOURCE_PATHS["product"], SOURCE_PATHS["engineering"]),
    ("return", "Business"): (SOURCE_PATHS["product"], SOURCE_PATHS["business"]),
    ("return", "Experience"): (SOURCE_PATHS["product"], SOURCE_PATHS["experience"]),
    ("return", "Engineering"): (SOURCE_PATHS["product"], SOURCE_PATHS["engineering"]),
    ("product_close", "Product"): ALL_SOURCE_PATHS,
}


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
            total[field] += usage_integer(value, field)
    return total


def usage_delta(after, before):
    value = {field: usage_integer(after, field) - usage_integer(before, field)
             for field in USAGE_FIELDS}
    if any(amount < 0 for amount in value.values()):
        raise ValueError("usage counters moved backwards")
    return value


def usage_integer(usage, field):
    if field not in usage or type(usage[field]) is not int or usage[field] < 0:
        raise ValueError(f"missing or malformed usage field: {field}")
    return usage[field]


def codex_usage_rows(rows):
    """Return one Codex session's cumulative usage without double-counting reasoning."""
    latest = None
    responses = 0
    for event in rows:
        payload = event.get("payload", {})
        if event.get("type") == "event_msg" and payload.get("type") == "token_count":
            candidate = payload.get("info", {}).get("total_token_usage", {})
            if candidate:
                latest = candidate
        if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
            latest = event["usage"]
        if ((event.get("type") == "event_msg" and payload.get("type") == "task_complete") or
                event.get("type") == "turn.completed"):
            responses += 1
    if latest is None:
        raise ValueError("Codex stage reported no usage")
    input_tokens = usage_integer(latest, "input_tokens")
    cached = usage_integer(latest, "cached_input_tokens")
    output = usage_integer(latest, "output_tokens")
    gross = input_tokens + output
    if ("total_tokens" in latest and usage_integer(latest, "total_tokens") != gross) or cached > input_tokens:
        raise ValueError("inconsistent Codex usage totals")
    return {"gross": gross, "cached": cached, "fresh": gross - cached,
            "responses": responses}


def claude_usage_rows(rows):
    """Return cumulative Claude usage; cache creation is fresh and cache reads are not."""
    messages = {}
    responses = 0
    for row in rows:
        message = row.get("message", {})
        if isinstance(message, dict) and message.get("role") == "assistant" and message.get("id"):
            messages[message["id"]] = message.get("usage", {})
        if row.get("type") == "result" and row.get("subtype") == "success":
            responses += 1
    gross = cached = fresh = 0
    for usage in messages.values():
        uncached = usage_integer(usage, "input_tokens")
        created = usage_integer(usage, "cache_creation_input_tokens")
        read = usage_integer(usage, "cache_read_input_tokens")
        output = usage_integer(usage, "output_tokens")
        gross += uncached + created + read + output
        cached += read
        fresh += uncached + created + output
    if responses and not messages:
        raise ValueError("Claude stage completed without assistant usage")
    return {"gross": gross, "cached": cached, "fresh": fresh, "responses": responses}


def stage_verdict(usage, elapsed, limits, complete):
    if (set(USAGE_FIELDS) - set(usage) or
            any(type(usage[field]) is not int or usage[field] < 0 for field in USAGE_FIELDS)):
        return {"status": "invalid", "reasons": ["usage"], "usage": dict(usage),
                "elapsed": elapsed, "limits": dict(limits), "complete": bool(complete)}
    if usage["cached"] > usage["gross"] or usage["fresh"] != usage["gross"] - usage["cached"]:
        return {"status": "invalid", "reasons": ["usage"], "usage": dict(usage),
                "elapsed": elapsed, "limits": dict(limits), "complete": bool(complete)}
    if type(elapsed) not in (int, float) or not math.isfinite(elapsed) or elapsed < 0:
        return {"status": "invalid", "reasons": ["wall"], "usage": dict(usage),
                "elapsed": elapsed, "limits": dict(limits), "complete": bool(complete)}
    if type(complete) is not bool:
        return {"status": "invalid", "reasons": ["complete"], "usage": dict(usage),
                "elapsed": elapsed, "limits": dict(limits), "complete": False}
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


def digest_string(value):
    return isinstance(value, str) and bool(re.fullmatch(r"[0-9a-f]{64}", value))


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def expected_packet_identity(stage_name):
    parts = stage_name.split("_", 1)
    role = parts[0].title()
    suffix = parts[1] if len(parts) == 2 else ""
    packet_stage = {"contribution": "contribution", "return": "return",
                    "select": "product_select", "synthesis": "product_synthesis",
                    "implement": "implement", "run": "run", "close": "product_close"}.get(suffix)
    return packet_stage, role


def embedded_packet_ok(stage, expected_name, manifest):
    packet = stage.get("packet")
    if not isinstance(packet, dict) or not isinstance(packet.get("body"), dict):
        return False
    body = packet["body"]
    if packet.get("sha256") != hashlib.sha256(canonical_json(body)).hexdigest():
        return False
    packet_stage, role = expected_packet_identity(expected_name)
    if body.get("stage") != packet_stage or body.get("role") != role:
        return False
    if tuple(item.get("path") for item in body.get("evidence", [])) != SOURCE_ALLOWLIST.get((packet_stage, role)):
        return False
    manifest_items = {item.get("path"): item for item in manifest.get("evidence", [])}
    try:
        for item in body["evidence"]:
            content = base64.b64decode(item["content_base64"], validate=True)
            if (len(content) != item["bytes"] or hashlib.sha256(content).hexdigest() != item["sha256"] or
                    {key: item[key] for key in ("path", "bytes", "sha256")} != manifest_items[item["path"]]):
                return False
        for item in body.get("generated", []):
            content = item["content"].encode()
            if len(content) != item["bytes"] or hashlib.sha256(content).hexdigest() != item["sha256"]:
                return False
    except (KeyError, TypeError, ValueError):
        return False
    return (body.get("schema") == "piece9-packet-v1" and body.get("lineage") == stage.get("input_lineage") and
            stage.get("packet_sha256") == packet.get("sha256") and
            isinstance(stage.get("output"), str) and
            hashlib.sha256(stage["output"].encode()).hexdigest() == stage.get("output_sha256"))


def source_manifest_ok(manifest):
    if not isinstance(manifest, dict):
        return False
    body = {key: manifest.get(key) for key in ("schema", "prompt_sha256", "evidence")}
    evidence = body["evidence"]
    if (body["schema"] != "piece9-packet-v1" or not digest_string(body["prompt_sha256"]) or
            not isinstance(evidence, list) or
            tuple(item.get("path") for item in evidence if isinstance(item, dict)) != ALL_SOURCE_PATHS):
        return False
    if any(set(item) != {"path", "bytes", "sha256"} or
           type(item["bytes"]) is not int or item["bytes"] < 0 or not digest_string(item["sha256"])
           for item in evidence):
        return False
    return manifest.get("sha256") == hashlib.sha256(canonical_json(body)).hexdigest()


def bound_stage_ok(stage, expected_name, manifest):
    if not isinstance(stage, dict) or stage.get("name") != expected_name:
        return False
    if not isinstance(stage.get("carrier"), str) or not stage["carrier"]:
        return False
    if (not digest_string(stage.get("packet_sha256")) or not digest_string(stage.get("output_sha256")) or
            not embedded_packet_ok(stage, expected_name, manifest)):
        return False
    lineage = stage.get("input_lineage")
    if not isinstance(lineage, list) or not lineage or not all(digest_string(value) for value in lineage):
        return False
    interval = stage.get("interval")
    if (not isinstance(interval, list) or len(interval) != 2 or
            any(type(value) not in (int, float) or not math.isfinite(value) for value in interval) or
            interval[1] < interval[0]):
        return False
    verdict = stage.get("verdict")
    if (not isinstance(verdict, dict) or verdict.get("status") != "passed" or
            verdict.get("usage", {}).get("responses") != 1):
        return False
    usage = verdict.get("usage")
    limits = verdict.get("limits")
    return (isinstance(usage, dict) and isinstance(limits, dict) and
            stage_verdict(usage, interval[1] - interval[0], limits, True).get("status") == "passed" and
            verdict.get("complete") is True)


def probe_stage_limits(probe, stage):
    if probe == "product":
        return STAGE_LIMITS["product_select" if stage == "product_select" else "product_synthesis"]
    if probe == "contributions":
        return STAGE_LIMITS["contributions"]
    return PROBE_LIMITS[probe]


def probe_evidence_ok(name, probe, source_digest):
    stages = probe["stages"]
    intervals = [stage["interval"] for stage in stages]
    if name == "contributions":
        if not intervals_overlap(intervals) or len({stage["carrier"] for stage in stages}) != 3:
            return False
        elapsed = max(end for _, end in intervals) - min(start for start, _ in intervals)
    else:
        if any(left[1] > right[0] for left, right in zip(intervals, intervals[1:])):
            return False
        elapsed = sum(end - start for start, end in intervals)
        if len({stage["carrier"] for stage in stages}) != 1:
            return False
    previous = None
    for stage in stages:
        lineage = stage["input_lineage"]
        if (lineage[0] != source_digest or
                (name != "contributions" and previous is not None and previous not in lineage)):
            return False
        previous = stage["output_sha256"]
    usage = add_usage(*(stage["verdict"]["usage"] for stage in stages))
    verdict = probe["verdict"]
    return (verdict.get("usage") == usage and
            type(verdict.get("elapsed")) in (int, float) and
            math.isclose(verdict["elapsed"], elapsed, rel_tol=0, abs_tol=1e-9) and
            stage_verdict(usage, elapsed, PROBE_LIMITS[name], True).get("status") == "passed")


def admission_ok(receipt, expected):
    if not all(receipt.get(field) == expected.get(field) and expected.get(field)
               for field in ADMISSION_FIELDS):
        return False
    probes = receipt.get("probes", {})
    manifest = receipt.get("source_manifest")
    if (not source_manifest_ok(manifest) or
            manifest.get("sha256") != expected.get("source_manifest_sha256")):
        return False
    if set(probes) != set(PROBE_NAMES):
        return False
    for name in PROBE_NAMES:
        probe = probes[name]
        if (not isinstance(probe, dict) or probe.get("name") != name or
                probe.get("status") != "passed" or
                any(probe.get(field) != expected.get(field) for field in ADMISSION_FIELDS) or
                probe.get("limits") != PROBE_LIMITS[name]):
            return False
        verdict = probe.get("verdict")
        if (not isinstance(verdict, dict) or verdict.get("limits") != PROBE_LIMITS[name] or
                verdict.get("status") != "passed" or verdict.get("complete") is not True or
                stage_verdict(verdict.get("usage", {}), verdict.get("elapsed"), PROBE_LIMITS[name], True).get("status") != "passed"):
            return False
        stages = probe.get("stages")
        if (not isinstance(stages, list) or len(stages) != len(PROBE_STAGES[name]) or
                not all(bound_stage_ok(stage, stage_name, manifest)
                        and stage.get("verdict", {}).get("limits") == probe_stage_limits(name, stage_name)
                        for stage, stage_name in zip(stages, PROBE_STAGES[name]))):
            return False
        if not probe_evidence_ok(name, probe, expected["source_manifest_sha256"]):
            return False
    return True


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


def controller_proof(clone, state_path, carriers):
    state = json.loads(pathlib.Path(state_path).read_text())
    result_data = state.get("result", {})
    usage = result_data.get("verdict", {}).get("usage", empty_usage())
    result = {"root": pathlib.Path(state.get("root", "")).resolve() == pathlib.Path(clone).resolve(),
              "roles": {}, "tokens": usage.get("gross", 0), **usage,
              "root_id": state.get("carriers", {}).get("Product"), "extra_contexts": 0}
    invocations = state.get("invocations", [])
    for role in ROLES:
        stages = [item for item in invocations if item.get("role") == role]
        contribution = next((item for item in stages if item.get("name") == f"{role.lower()}_contribution"), None)
        returned = next((item for item in stages if item.get("name") == f"{role.lower()}_return"), None)
        carrier = state.get("carriers", {}).get(role)
        if not contribution:
            continue
        packet_paths = {item.get("path") for item in contribution.get("packet", {}).get("evidence", [])}
        output = contribution.get("output", "")
        return_output = returned.get("output", "") if returned else ""
        ruling = re.findall(r"Business ruling:\s*(kept|broken|not[- ]judged)\b", return_output, re.I)
        result["roles"][role] = {
            "carrier": carrier,
            "host": bool(carrier) and all(item.get("carrier") == carrier and
                                           item.get("observed_carrier") in (None, carrier) for item in stages),
            "contribution": bool(re.search(rf"(?m)^Role:\s*{role}\s*$", output)),
            "direct": NEEDLES[role] in packet_paths,
            "elected": True,
            "returned": bool(returned and re.search(r"\b(changed|held)\b", return_output, re.I)),
            "ruling_permits": role != "Business" or bool(ruling and ruling[-1].lower() == "kept"),
            "precode_clean": True,
        }
    if carriers and any(result["roles"].get(role, {}).get("carrier") != carrier
                        for role, carrier in carriers.items() if role in ROLES):
        result["roles"] = {}
    return result


def proof(driver, clone, events_path, carriers, state_path=None):
    if state_path and pathlib.Path(state_path).is_file():
        state = json.loads(pathlib.Path(state_path).read_text())
        if state.get("protocol") == "piece9-packet-v1":
            return controller_proof(clone, state_path, carriers)
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
        root.write_text(json.dumps({"sessionId": root_id, "cwd": str(clone), "message": {"role": "assistant", "id": "m1", "usage": {"input_tokens": 2, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 0}, "content": [{"type": "tool_use", "id": "t1", "name": "Agent", "input": {"name": "pulse-business"}}]}}) + "\n" +
                        json.dumps({"message": {"content": [{"tool_use_id": "t1"}]}, "toolUseResult": {"agentId": agent, "outputFile": str(projects / "child.jsonl")}}) + "\n")
        child = projects / "child.jsonl"
        child.write_text(json.dumps({"agentId": agent, "message": {"role": "assistant", "id": "c1", "usage": {"input_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 3}, "content": [{"type": "tool_use", "name": "Read", "input": {"file_path": "business-evidence.md"}}, {"type": "text", "text": "Role: Business business-evidence.md. First real run held. Business ruling: broken"}]}}) + "\n")
        good = native_claude(clone, events, {"Business": agent}, projects)
        broken_text = child.read_text()
        child.write_text(broken_text.replace("Business ruling: broken", "Business ruling: not judged"))
        not_judged = native_claude(clone, events, {"Business": agent}, projects)
        child.write_text(broken_text)
        grandchild = projects / "grandchild.jsonl"
        grandchild.write_text(json.dumps({"agentId": "agent-helper", "message": {"role": "assistant", "id": "g1", "usage": {"input_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 7}, "content": []}}) + "\n")
        child.write_text(child.read_text() +
                         json.dumps({"agentId": agent, "message": {"role": "assistant", "id": "c2", "usage": {"input_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 0}, "content": [{"type": "tool_use", "id": "nested", "name": "Agent", "input": {"name": "helper"}}]}}) + "\n" +
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
        (codex_root / f"{root_id}.jsonl").write_text(json.dumps({"type": "session_meta", "payload": {"id": root_id, "cwd": str(clone)}}) + "\n" +
                                                            json.dumps({"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "total_tokens": 0}}}}) + "\n")
        role_id = "role-business"
        (codex_roles / f"{role_id}.jsonl").write_text(json.dumps({"type": "session_meta", "payload": {"id": role_id, "cwd": str(base)}}) + "\n" +
                                                        json.dumps({"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "total_tokens": 0}}}}) + "\n")
        (codex_roles / "role-helper.jsonl").write_text(json.dumps({"type": "session_meta", "payload": {"id": "role-helper", "parent_thread_id": role_id, "cwd": str(base)}}) + "\n" +
                                                                json.dumps({"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "total_tokens": 0}}}}) + "\n")
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
        state_path = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != "-" else None
        value = proof(driver, clone, events, {}, state_path)
        controller_elapsed = value.get("elapsed")
        state = json.loads(pathlib.Path(state_path).read_text()) if state_path and pathlib.Path(state_path).is_file() else {}
        if state.get("protocol") == "piece9-packet-v1":
            controller_elapsed = state.get("result", {}).get("verdict", {}).get("elapsed")
        if controller_elapsed is not None:
            value["elapsed_seconds"] = controller_elapsed
        elif len(sys.argv) > 6:
            value["elapsed_seconds"] = int(sys.argv[6])
        if len(sys.argv) > 7:
            value["token_limit"] = int(sys.argv[7])
        print(json.dumps(value, sort_keys=True))
    else:
        raise SystemExit("usage: host_proof.py --self-test | metrics DRIVER CLONE EVENTS [STATE]")
