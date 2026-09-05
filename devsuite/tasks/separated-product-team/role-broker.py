#!/usr/bin/env python3
"""Fixed six-stage transport for the separated-product-team development fixture."""
import hashlib, json, os, pathlib, platform, shutil, signal, subprocess, sys, tempfile, time
import host_proof

ROLES = ("Business", "Experience", "Engineering")
active_processes = []
PACKET_SCHEMA = host_proof.PACKET_SCHEMA
STAGE_ORDER = host_proof.STAGE_ORDER
STAGE_LIMITS = host_proof.STAGE_LIMITS
PROBE_LIMITS = host_proof.PROBE_LIMITS
FULL_LIMITS = host_proof.FULL_LIMITS
SOURCE_PATHS = host_proof.SOURCE_PATHS
ALL_SOURCE_PATHS = host_proof.ALL_SOURCE_PATHS
SOURCE_ALLOWLIST = host_proof.SOURCE_ALLOWLIST
SOURCE_EXCERPT_ALLOWLIST = host_proof.SOURCE_EXCERPT_ALLOWLIST
MANIFEST_EXCERPTS = host_proof.MANIFEST_EXCERPTS
SOLUTION_HINTS = ("seven-day", "mixed-gap", "honest gaps", "no new dependency", "preserving gaps")


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def source_file(root, name):
    root = pathlib.Path(root).resolve()
    relative = pathlib.PurePosixPath(str(name))
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe evidence path: {name}")
    source = (root / pathlib.Path(*relative.parts)).resolve(strict=True)
    try:
        confined = os.path.commonpath((str(root), str(source))) == str(root)
    except ValueError:
        confined = False
    if not confined or not source.is_file():
        raise ValueError(f"evidence path escapes product root: {name}")
    return source


def excerpt_item(root, excerpt, include_content=True):
    selector, name, first_line, last_line = excerpt
    source = source_file(root, name)
    content = source.read_bytes()
    lines = content.splitlines(keepends=True)
    if (type(first_line) is not int or type(last_line) is not int or
            first_line < 1 or last_line < first_line or last_line > len(lines)):
        raise ValueError(f"invalid excerpt lines for {name}: {first_line}-{last_line}")
    start = sum(len(line) for line in lines[:first_line - 1])
    end = start + sum(len(line) for line in lines[first_line - 1:last_line])
    selected = content[start:end]
    try:
        text = selected.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"excerpt is not UTF-8: {name}") from error
    item = {
        "selector": selector, "path": str(pathlib.PurePosixPath(name)),
        "lines": [first_line, last_line], "byte_range": [start, end],
        "bytes": len(selected), "sha256": hashlib.sha256(selected).hexdigest(),
    }
    if not host_proof.excerpt_content_ok(selector, text):
        raise ValueError(f"excerpt selector no longer matches its source: {selector}")
    if include_content:
        item["content"] = text
    return item


def make_packet(root, stage, role, brief, paths, lineage=(), generated=()):
    expected_paths = SOURCE_ALLOWLIST.get((stage, role))
    if expected_paths is None or tuple(paths) != tuple(expected_paths):
        raise ValueError(f"source paths are not the fixed allowlist for {role} {stage}")
    if not all(isinstance(value, str) and len(value) == 64 and
               all(character in "0123456789abcdef" for character in value) for value in lineage):
        raise ValueError("packet lineage contains a malformed digest")
    evidence = [excerpt_item(root, excerpt)
                for excerpt in SOURCE_EXCERPT_ALLOWLIST[(stage, role)]]
    generated_items = []
    for label, content in generated:
        if not isinstance(label, str) or not label or not isinstance(content, str):
            raise ValueError("malformed generated packet input")
        content_bytes = content.encode()
        generated_items.append({"label": label, "bytes": len(content_bytes),
                                "sha256": hashlib.sha256(content_bytes).hexdigest(),
                                "content": content})
    body = {
        "schema": PACKET_SCHEMA, "stage": stage, "role": role, "brief": brief,
        "lineage": list(lineage), "evidence": evidence, "generated": generated_items,
    }
    return {"body": body, "sha256": hashlib.sha256(canonical_json(body)).hexdigest()}


def verify_packet(packet):
    try:
        if set(packet) != {"body", "sha256"}:
            return False
        body = packet["body"]
        if packet.get("sha256") != hashlib.sha256(canonical_json(body)).hexdigest():
            return False
        if set(body) != {"schema", "stage", "role", "brief", "lineage", "evidence", "generated"}:
            return False
        for item in body["evidence"]:
            if set(item) != {"selector", "path", "lines", "byte_range", "bytes", "sha256", "content"}:
                return False
            content = item["content"].encode("utf-8")
            byte_range = item["byte_range"]
            if (not isinstance(item["lines"], list) or len(item["lines"]) != 2 or
                    any(type(value) is not int or value < 1 for value in item["lines"]) or
                    not isinstance(byte_range, list) or len(byte_range) != 2 or
                    any(type(value) is not int or value < 0 for value in byte_range) or
                    byte_range[1] < byte_range[0] or byte_range[1] - byte_range[0] != item["bytes"] or
                    len(content) != item["bytes"] or hashlib.sha256(content).hexdigest() != item["sha256"] or
                    not host_proof.excerpt_content_ok(item["selector"], item["content"])):
                return False
        for item in body["generated"]:
            if set(item) != {"label", "bytes", "sha256", "content"}:
                return False
            content = item["content"].encode()
            if len(content) != item["bytes"] or hashlib.sha256(content).hexdigest() != item["sha256"]:
                return False
        expected = SOURCE_EXCERPT_ALLOWLIST.get((body.get("stage"), body.get("role")))
        return (body.get("schema") == PACKET_SCHEMA and expected is not None and
                tuple((item.get("selector"), item.get("path"), item.get("lines"))
                      for item in body["evidence"]) ==
                tuple((selector, path, [first, last])
                      for selector, path, first, last in expected) and
                len(body["evidence"]) == len(expected) and
                len({item.get("label") for item in body["generated"]}) == len(body["generated"]) and
                all(isinstance(value, str) and len(value) == 64 and
                    all(character in "0123456789abcdef" for character in value)
                    for value in body.get("lineage", [])))
    except (KeyError, TypeError, ValueError):
        return False


def source_manifest(root, prompt_sha256):
    entries = []
    for name in ALL_SOURCE_PATHS:
        content = source_file(root, name).read_bytes()
        entries.append({"path": name, "bytes": len(content),
                        "sha256": hashlib.sha256(content).hexdigest()})
    excerpts = [excerpt_item(root, excerpt, include_content=False) for excerpt in MANIFEST_EXCERPTS]
    body = {"schema": PACKET_SCHEMA, "prompt_sha256": prompt_sha256,
            "evidence": entries, "excerpts": excerpts}
    return {**body, "sha256": hashlib.sha256(canonical_json(body)).hexdigest()}


def reservation_plan():
    return {stage: {**limits, "status": "reserved"} for stage, limits in STAGE_LIMITS.items()}


def can_start(plan, stage):
    if stage not in STAGE_ORDER or set(plan) != set(STAGE_ORDER):
        return False
    index = STAGE_ORDER.index(stage)
    for position, name in enumerate(STAGE_ORDER):
        expected_status = "complete" if position < index else "reserved"
        expected = {**STAGE_LIMITS[name], "status": expected_status}
        if plan.get(name) != expected:
            return False
    return True


def write_json(path, value):
    path = pathlib.Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def stop(_signum=None, _frame=None):
    for process in list(active_processes):
        if process.poll() is None:
            process.terminate()
    deadline = time.monotonic() + 3
    for process in list(active_processes):
        try:
            process.wait(timeout=max(0, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            process.kill()
    raise SystemExit(143)


def sha256_text(value):
    return hashlib.sha256(value.encode()).hexdigest()


def runner_sha256(kernel_root):
    root = pathlib.Path(kernel_root).resolve()
    paths = (
        "devsuite/run.sh",
        "devsuite/tasks/separated-product-team/role-broker.py",
        "devsuite/tasks/separated-product-team/host_proof.py",
        "devsuite/tasks/separated-product-team/check.py",
    )
    digest = hashlib.sha256()
    for relative in paths:
        content = (root / relative).read_bytes()
        digest.update(relative.encode() + b"\0" + len(content).to_bytes(8, "big") + content)
    return digest.hexdigest()


def git_output(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def admission_identity(source_root, candidate_root, driver, model, prompt_path, kernel_root):
    prompt_digest = hashlib.sha256(pathlib.Path(prompt_path).read_bytes()).hexdigest()
    manifest = source_manifest(source_root, prompt_digest)
    identity = {
        "driver": driver,
        "host": platform.node(),
        "model": model,
        "candidate": git_output(candidate_root, "rev-parse", "HEAD"),
        "runner_sha256": runner_sha256(kernel_root),
        "packet_schema": PACKET_SCHEMA,
        "source_manifest_sha256": manifest["sha256"],
    }
    return identity, manifest


def parse_object(text, label):
    candidate = text.strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            candidate = "\n".join(lines[1:-1])
    try:
        value = json.loads(candidate)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"{label} did not return one JSON object: {error}") from error
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} did not return one JSON object")
    return value


def packet_prompt(stage, role, packet):
    prefix = (
        f"You are the separate {role} carrier. Use only the verified excerpts and generated evidence below. "
        "Do not inspect other files, delegate, or act as another role.\n\n"
    )
    instructions = {
        "product_select": (
            "Select the relevant evidence and issue one specific brief for each of Business, Experience, and "
            "Engineering. Return JSON only with keys selection and role_briefs; role_briefs must contain exactly "
            "Business, Experience, and Engineering, and each brief must name its direct source and bounded question."
        ),
        "contribution": (
            {
                "Business": "Decide only whether the requested weekly view earns one bounded build now and whether any price claim is supported.",
                "Experience": "Decide only what the requested weekly view must show to preserve the product promises in its evidence.",
                "Engineering": "Decide only the smallest safe implementation seam, its exact regression proof, and any existing promise it could trade away.",
            }[role] +
            f" Return exactly these labeled lines: `Role: {role}`, `Direct evidence:`, `Conclusion:`, "
            "`Assumptions:`, `Proposed change:`, `Consequence:`, and `Earliest disconfirming run:`. "
            "In Direct evidence, cite one supplied excerpt exactly as `path@[start,end)` using its byte_range, "
            "then state the concrete claim the excerpt supports. Answer the immediate decision; do not write a "
            "strategy or edit a file."
        ),
        "product_synthesis": (
            "Integrate the three contributions without flattening dissent. Return JSON only with keys "
            "record_markdown and implementation_brief. record_markdown must be a complete piece record headed "
            "`# Weekly view`, include `## Active pre-code contributions`, a Markdown table with one row each "
            "for Product, Business, Experience, and Engineering whose columns are Carrier, direct evidence, "
            "conclusion, assumptions, proposed change, and active decision, and one `**Product synthesis:**` line. "
            "Copy every host-issued carrier exactly from carrier_manifest. Make and state the Product decision "
            "from the supplied briefs and contributions; the controller supplies no solution."
        ),
        "implement": (
            "Continue as Engineering implementation owner after the committed Product synthesis. Implement only "
            "examples/pulse/pulse.py according to the exact product_synthesis and implementation_brief generated "
            "evidence. Do not edit product or work records. Return `Role: Engineering`, the changed path, and commit."
        ),
        "run": (
            "Continue as Engineering. Run one smallest direct CLI scenario that tests the committed implementation "
            "against Product's exact handoff. Do not edit files. Return `Role: Engineering`, exact command, exit "
            "status, and output; narration without an authoritative command result is incomplete."
        ),
        "return": (
            f"Continue as the same {role} carrier at the supplied real run. Return a line exactly `Role: {role}`, "
            "the observed evidence, what changed or held, and the resulting product change. " +
            ("Include exactly one binding `Business ruling: kept`, `Business ruling: broken`, or "
             "`Business ruling: not judged` with its reason." if role == "Business" else "")
        ),
        "product_close": (
            "Continue as Product and close the product record from the actual implementation and returns. "
            "Return JSON only with key append_markdown. It must begin `## Informative role returns`, record all "
            "three role returns, restate the exact verdict as `**Business ruling:** kept — reason` (or broken/not "
            "judged as returned), include contributor exclusions, and one integrated "
            "owner-facing recommendation. Do not claim review, judgment, Built, or release."
        ),
    }[stage]
    if stage in ("contribution", "product_synthesis", "implement", "run") and any(
            hint in instructions.lower() for hint in SOLUTION_HINTS):
        raise RuntimeError("controller instruction supplied the Product solution")
    return prefix + instructions + "\n\nVerified packet:\n" + canonical_json(packet).decode()


def observed_carrier(driver, rows):
    values = []
    if driver == "codex":
        values = [row.get("thread_id") for row in rows if row.get("type") == "thread.started"]
    else:
        for row in rows:
            if row.get("type") == "result" and row.get("session_id"):
                values.append(row["session_id"])
            elif row.get("type") == "system" and row.get("session_id"):
                values.append(row["session_id"])
    unique = list(dict.fromkeys(value for value in values if value))
    if len(unique) > 1:
        raise RuntimeError("one invocation emitted conflicting carrier identities")
    return unique[0] if unique else None


def invocation_output(driver, rows, output_path):
    if driver == "codex":
        canonical = [row for row in rows if row.get("type") == "turn.completed"]
        failed = [row for row in rows if row.get("type") == "turn.failed"]
        legacy = [row for row in rows if row.get("type") == "event_msg" and
                  row.get("payload", {}).get("type") == "task_complete"]
        if failed or (canonical and len(canonical) != 1) or (not canonical and len(legacy) != 1):
            return ""
        if canonical:
            values = [row.get("item", {}).get("text") for row in rows
                      if row.get("type") == "item.completed" and
                      row.get("item", {}).get("type") == "agent_message" and
                      isinstance(row.get("item", {}).get("text"), str)]
            if len(values) == 1:
                return values[0]
        else:
            value = legacy[0].get("payload", {}).get("last_agent_message")
            if isinstance(value, str) and value:
                return value
        return output_path.read_text(errors="ignore") if output_path.is_file() else ""
    values = [row.get("result") for row in rows
              if row.get("type") == "result" and row.get("subtype") == "success" and
              isinstance(row.get("result"), str)]
    return values[-1] if len(values) == 1 else ""


def invocation_complete(usage, output, returncode, terminated_by_group):
    return (isinstance(usage, dict) and usage.get("responses") == 1 and
            isinstance(output, str) and bool(output.strip()) and
            (returncode == 0 or terminated_by_group is True))


def invocation_limits(group_limits):
    return {**group_limits, "responses": 1}


def observe_completion(item, driver, rows, output_path, now, now_at):
    if "completed" in item:
        return
    try:
        usage = (host_proof.codex_usage_rows(rows) if driver == "codex"
                 else host_proof.claude_usage_rows(rows))
    except ValueError:
        return
    output = invocation_output(driver, rows, output_path)
    if usage.get("responses") == 1 and output.strip():
        item["completed"] = now
        item["completed_at"] = now_at


def _result_text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(item.get("text", "") for item in value
                         if isinstance(item, dict) and isinstance(item.get("text"), str))
    return ""


def command_evidence(driver, rows):
    values = []
    if driver == "codex":
        for row in rows:
            item = row.get("item", {})
            if (row.get("type") == "item.completed" and item.get("type") == "command_execution" and
                    isinstance(item.get("command"), str) and type(item.get("exit_code")) is int):
                values.append({"command": item["command"], "exit_code": item["exit_code"],
                               "output": item.get("aggregated_output", "")})
    else:
        uses = {}
        for row in rows:
            message = row.get("message", {})
            content = message.get("content", []) if isinstance(message, dict) else []
            if not isinstance(content, list):
                continue
            for item in content:
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "tool_use" and item.get("name") == "Bash" and item.get("id"):
                    command = item.get("input", {}).get("command")
                    if isinstance(command, str):
                        uses[item["id"]] = command
                elif item.get("type") == "tool_result" and item.get("tool_use_id") in uses:
                    values.append({"command": uses[item["tool_use_id"]],
                                   "exit_code": 1 if item.get("is_error") is True else 0,
                                   "output": _result_text(item.get("content"))})
    if not values:
        return None
    value = values[-1]
    value["sha256"] = hashlib.sha256(canonical_json(value)).hexdigest()
    return value


def driver_command(driver, model, effort, sandbox, cwd, root, output, prompt, carrier=None):
    if driver == "codex":
        command = [
            "codex", "exec", "--json", "--sandbox", sandbox, "--skip-git-repo-check",
            "--ignore-user-config", "-m", model, "-c", f'model_reasoning_effort="{effort}"',
            "-c", "features.multi_agent=false", "-C", str(cwd), "-o", str(output),
        ]
        if sandbox == "workspace-write":
            command += ["--add-dir", str(root)]
        return command + (["resume", carrier, prompt] if carrier else [prompt])
    if driver == "claude":
        tools = "Bash,Read,Edit,Write" if sandbox == "workspace-write" else ""
        command = ["claude", "-p", prompt]
        if carrier:
            command += ["--resume", carrier]
        command += ["--output-format", "stream-json", "--verbose", "--model", model,
                    "--effort", effort, "--setting-sources", "user", "--tools", tools]
        if sandbox == "workspace-write":
            command += ["--add-dir", str(root)]
        return command
    raise RuntimeError(f"unsupported driver: {driver}")


def carrier_home_prefix(role):
    if role not in ("Product", *ROLES):
        raise RuntimeError(f"unknown carrier role: {role}")
    return f"speck-piece9-{role.lower()}-home."


def recognized_carrier_home(path, role):
    resolved = pathlib.Path(path).resolve()
    return (resolved.parent == pathlib.Path(tempfile.gettempdir()).resolve() and
            resolved.name.startswith(carrier_home_prefix(role)))


def ensure_carrier_home(state, role, auth_source=None):
    if state.get("driver") != "codex":
        return None
    existing = state.setdefault("driver_homes", {}).get(role)
    if existing:
        path = pathlib.Path(existing).resolve()
        if not recognized_carrier_home(path, role) or not (path / "auth.json").is_file():
            raise RuntimeError(f"invalid persisted Codex home for {role}")
        return path
    source = pathlib.Path(auth_source) if auth_source else pathlib.Path.home() / ".codex" / "auth.json"
    if not source.is_file():
        raise RuntimeError("Codex auth source is unavailable")
    control = pathlib.Path(state["control"]).resolve()
    suffix = hashlib.sha256(str(control).encode()).hexdigest()[:16]
    path = pathlib.Path(tempfile.gettempdir()).resolve() / f"{carrier_home_prefix(role)}{suffix}"
    state["driver_homes"][role] = str(path)
    state["auth_removed"] = False
    write_json(control / "state.json", state)
    try:
        path.mkdir(mode=0o700)
        shutil.copyfile(source, path / "auth.json")
        os.chmod(path / "auth.json", 0o600)
    except BaseException:
        if path.exists():
            subprocess.run(["trash", str(path)], check=False)
        state["driver_homes"].pop(role, None)
        state["auth_removed"] = not state["driver_homes"]
        write_json(control / "state.json", state)
        raise
    return path


def start_invocation(state, spec, limits):
    role, stage = spec["role"], spec["stage"]
    stem = spec["receipt_name"]
    packet = spec["packet"]
    packet_path = pathlib.Path(state["control"]) / "packets" / f"{stem}.json"
    packet_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(packet_path, packet)
    events = pathlib.Path(state["control"]) / "events" / f"{stem}.jsonl"
    stderr = pathlib.Path(state["control"]) / "events" / f"{stem}.stderr.log"
    output = pathlib.Path(state["control"]) / "outputs" / f"{stem}.md"
    events.parent.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    carrier = state["carriers"].get(role)
    sandbox = spec.get("sandbox", "read-only")
    cwd = (pathlib.Path(state["root"]) if role == "Engineering" and stage in ("implement", "run", "return")
           else pathlib.Path(state["role_cwd"]))
    command = driver_command(state["driver"], state["model"], state["effort"], sandbox,
                             cwd, state["root"], output, packet_prompt(stage, role, packet), carrier)
    env = dict(os.environ)
    if state["driver"] == "codex":
        env["CODEX_HOME"] = str(ensure_carrier_home(state, role))
    event_handle = events.open("w")
    error_handle = stderr.open("w")
    started_at = time.time()
    started = time.monotonic()
    print(f"piece9 packet {stem}: canonical_bytes={len(canonical_json(packet))}", flush=True)
    process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                               stdout=event_handle, stderr=error_handle, text=True)
    active_processes.append(process)
    return {**spec, "process": process, "events": events, "stderr": stderr, "output_path": output,
            "event_handle": event_handle, "error_handle": error_handle,
            "started": started, "started_at": started_at, "limits": invocation_limits(limits)}


def terminate_invocations(invocations):
    for item in invocations:
        process = item["process"]
        if process.poll() is None:
            process.terminate()
    deadline = time.monotonic() + 3
    for item in invocations:
        process = item["process"]
        remaining = max(0, deadline - time.monotonic())
        try:
            process.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            process.kill()


def partial_usage(driver, events):
    try:
        rows = host_proof.jsonl(events)
        return (host_proof.codex_usage_rows(rows) if driver == "codex"
                else host_proof.claude_usage_rows(rows))
    except ValueError:
        return host_proof.empty_usage()


def finish_group(state, invocations, limits, require_overlap=False):
    stopped = False
    while any(item["process"].poll() is None for item in invocations):
        now, now_at = time.monotonic(), time.time()
        for item in invocations:
            rows = host_proof.jsonl(item["events"])
            observe_completion(item, state["driver"], rows, item["output_path"], now, now_at)
            if item["process"].poll() is not None and "process_ended" not in item:
                item["process_ended"], item["process_ended_at"] = now, now_at
        elapsed = now - min(item["started"] for item in invocations)
        usage = host_proof.add_usage(*(partial_usage(state["driver"], item["events"])
                                       for item in invocations))
        if (elapsed > limits["wall"] or usage["gross"] > limits["gross"] or
                usage["fresh"] > limits["fresh"] or usage["responses"] > limits["responses"]):
            stopped = True
            for item in invocations:
                if item["process"].poll() is None:
                    item["terminated_by_group"] = True
            terminate_invocations(invocations)
            break
        time.sleep(0.1)
    receipts = []
    failures = []
    for item in invocations:
        item["process"].wait()
        item["event_handle"].close()
        item["error_handle"].close()
        if item["process"] in active_processes:
            active_processes.remove(item["process"])
        now, now_at = time.monotonic(), time.time()
        if "process_ended" not in item:
            item["process_ended"], item["process_ended_at"] = now, now_at
        rows = host_proof.jsonl(item["events"])
        observe_completion(item, state["driver"], rows, item["output_path"], now, now_at)
        try:
            usage = (host_proof.codex_usage_rows(rows) if state["driver"] == "codex"
                     else host_proof.claude_usage_rows(rows))
        except ValueError as error:
            usage = host_proof.empty_usage()
            failures.append(str(error))
        observed = observed_carrier(state["driver"], rows)
        expected = state["carriers"].get(item["role"])
        if expected is None:
            if not observed:
                failures.append(f"{item['role']} contribution emitted no carrier identity")
            else:
                state["carriers"][item["role"]] = observed
                expected = observed
        elif observed != expected:
            failures.append(f"{item['role']} carrier changed on resume")
        output = invocation_output(state["driver"], rows, item["output_path"])
        if not output.strip():
            failures.append(f"{item['receipt_name']} emitted no terminal assistant result")
        complete = invocation_complete(usage, output, item["process"].returncode,
                                       item.get("terminated_by_group", False))
        if not complete:
            failures.append(f"{item['receipt_name']} did not complete exactly one response")
        before = state["carrier_usage"].get(item["role"], host_proof.empty_usage())
        after = host_proof.add_usage(before, usage)
        delta = host_proof.usage_delta(after, before)
        state["carrier_usage"][item["role"]] = after
        ended = item["process_ended"]
        ended_at = item["process_ended_at"]
        elapsed = ended - item["started"]
        verdict = host_proof.stage_verdict(delta, elapsed, item["limits"], complete)
        receipt = {
            "name": item["receipt_name"], "role": item["role"], "carrier": expected,
            "observed_carrier": observed, "packet_sha256": item["packet"]["sha256"],
            "packet": item["packet"], "input_lineage": item["packet"]["body"]["lineage"],
            "output": output, "output_sha256": sha256_text(output),
            "interval": [item["started"], ended], "started_at": item["started_at"],
            "ended_at": ended_at, "terminal_completed": item.get("completed"),
            "terminal_completed_at": item.get("completed_at"),
            "process_ended": item["process_ended"], "process_ended_at": item["process_ended_at"],
            "usage_before": before, "usage_after": after, "verdict": verdict,
        }
        if item["receipt_name"] == "engineering_run":
            receipt["command_evidence"] = command_evidence(state["driver"], rows)
            if not host_proof.command_evidence_ok(receipt["command_evidence"]):
                failures.append("engineering_run emitted no successful authoritative command result")
        receipts.append(receipt)
        state["invocations"].append(receipt)
    intervals = [receipt["interval"] for receipt in receipts]
    if require_overlap and not host_proof.intervals_overlap(intervals):
        failures.append("concurrent group had no common monotonic overlap")
    usage = host_proof.add_usage(*(receipt["verdict"]["usage"] for receipt in receipts))
    elapsed = max(end for _, end in intervals) - min(start for start, _ in intervals)
    complete = not failures and all(receipt["verdict"]["status"] == "passed" for receipt in receipts)
    verdict = host_proof.stage_verdict(usage, elapsed, limits, complete)
    if verdict["status"] != "passed":
        failures.append(f"group verdict: {verdict['status']} {','.join(verdict['reasons'])}")
    state["last_group"] = {"verdict": verdict, "failures": failures}
    write_json(pathlib.Path(state["control"]) / "state.json", state)
    if failures:
        raise RuntimeError("; ".join(dict.fromkeys(failures)))
    return receipts, verdict


def run_group(state, specs, limits, require_overlap=False):
    packet_bytes = sum(len(canonical_json(spec["packet"])) for spec in specs)
    prompt_bytes = sum(len(packet_prompt(spec["stage"], spec["role"], spec["packet"]).encode())
                       for spec in specs)
    metric = {"stages": [spec["receipt_name"] for spec in specs],
              "canonical_packet_bytes": packet_bytes, "wire_prompt_bytes": prompt_bytes}
    state.setdefault("packet_groups", []).append(metric)
    write_json(pathlib.Path(state["control"]) / "state.json", state)
    print(f"piece9 packet group {','.join(metric['stages'])}: canonical_bytes={packet_bytes} "
          f"wire_prompt_bytes={prompt_bytes}", flush=True)
    invocations = [start_invocation(state, spec, limits) for spec in specs]
    return finish_group(state, invocations, limits, require_overlap)


def stage_spec(state, receipt_name, stage, role, brief, lineage, generated=(), sandbox="read-only"):
    packet = make_packet(state["source_root"], stage, role, brief,
                         SOURCE_ALLOWLIST[(stage, role)], lineage=lineage, generated=generated)
    if not verify_packet(packet):
        raise RuntimeError(f"runner generated an invalid {receipt_name} packet")
    return {"receipt_name": receipt_name, "stage": stage, "role": role,
            "packet": packet, "sandbox": sandbox}


def aggregate_receipts(receipts, limits, concurrent=False):
    usage = host_proof.add_usage(*(receipt["verdict"]["usage"] for receipt in receipts))
    intervals = [receipt["interval"] for receipt in receipts]
    elapsed = ((max(end for _, end in intervals) - min(start for start, _ in intervals))
               if concurrent else sum(end - start for start, end in intervals))
    complete = all(receipt["verdict"]["status"] == "passed" for receipt in receipts)
    return host_proof.stage_verdict(usage, elapsed, limits, complete)


def select_briefs(output):
    value = parse_object(output, "Product selection")
    briefs = value.get("role_briefs")
    if (not isinstance(value.get("selection"), str) or not value["selection"].strip() or
            not isinstance(briefs, dict) or set(briefs) != set(ROLES) or
            any(not isinstance(brief, str) or len(brief.strip()) < 80 for brief in briefs.values())):
        raise RuntimeError("Product selection did not issue three bounded role briefs")
    return value


def commit_product_record(state, output, probe=False):
    value = parse_object(output, "Product synthesis")
    record = value.get("record_markdown")
    brief = value.get("implementation_brief")
    if (not isinstance(record, str) or "## Active pre-code contributions" not in record or
            "**Product synthesis:**" not in record or not isinstance(brief, str) or len(brief.strip()) < 80):
        raise RuntimeError("Product synthesis did not return the required record and handoff")
    path = pathlib.Path(state["root"]) / "examples/pulse/work/weekly-view.md"
    path.write_text(record.rstrip() + "\n")
    git_output(state["root"], "add", "examples/pulse/work/weekly-view.md")
    git_output(state["root"], "commit", "-m", "Record Product synthesis before code")
    state["product_record"] = str(path)
    state["implementation_brief"] = brief
    state["synthesis_commit"] = git_output(state["root"], "rev-parse", "HEAD")
    state["probe_record"] = bool(probe)
    write_json(pathlib.Path(state["control"]) / "state.json", state)
    return value


def close_product_record(state, output):
    value = parse_object(output, "Product close")
    append = value.get("append_markdown")
    if not isinstance(append, str) or not append.lstrip().startswith("## Informative role returns"):
        raise RuntimeError("Product close did not return the required record appendix")
    path = pathlib.Path(state["product_record"])
    with path.open("a") as handle:
        handle.write("\n" + append.rstrip() + "\n")
    git_output(state["root"], "add", "examples/pulse/work/weekly-view.md")
    git_output(state["root"], "commit", "-m", "Close role returns from the first run")
    state["close_commit"] = git_output(state["root"], "rev-parse", "HEAD")


def copy_source_snapshot(root, control):
    snapshot = pathlib.Path(control) / "source-snapshot"
    for relative in ALL_SOURCE_PATHS:
        source = pathlib.Path(root) / relative
        target = snapshot / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    return snapshot


def prepare_controller(root_arg, control_arg, driver, model, effort, prompt_path, kernel_root):
    root = pathlib.Path(root_arg).resolve()
    control = pathlib.Path(control_arg).resolve()
    control.mkdir(parents=True, exist_ok=True, mode=0o700)
    role_cwd = control / "role-cwd"
    role_cwd.mkdir(mode=0o700)
    snapshot = copy_source_snapshot(root, control)
    identity, manifest = admission_identity(snapshot, root, driver, model, prompt_path, kernel_root)
    if driver == "codex":
        auth_source = pathlib.Path.home() / ".codex" / "auth.json"
        if not auth_source.is_file():
            raise RuntimeError("Codex auth source is unavailable")
    state = {
        "protocol": PACKET_SCHEMA, "root": str(root), "control": str(control),
        "source_root": str(snapshot), "role_cwd": str(role_cwd), "driver_homes": {},
        "driver": driver, "model": model, "effort": effort, "identity": identity,
        "source_manifest": manifest, "carriers": {}, "carrier_usage": {}, "invocations": [],
        "reservations": reservation_plan(), "auth_removed": driver != "codex", "status": "starting",
    }
    write_json(control / "state.json", state)
    return state


def cleanup_controller(state):
    homes = dict(state.get("driver_homes", {}))
    valid = []
    failures = []
    for role, task_home in homes.items():
        path = pathlib.Path(task_home).resolve()
        recognized = (path.parent == pathlib.Path(tempfile.gettempdir()).resolve() and
                      recognized_carrier_home(path, role))
        if recognized:
            valid.append((role, path))
        else:
            failures.append(f"unrecognized controller home for {role}")
    for role, path in valid:
        try:
            auth = path / "auth.json"
            if auth.exists():
                auth.unlink()
            if path.exists():
                subprocess.run(["trash", str(path)], check=True)
            state.get("driver_homes", {}).pop(role, None)
        except (OSError, subprocess.CalledProcessError) as error:
            failures.append(f"could not clean controller home for {role}: {error}")
    state["auth_removed"] = not any((pathlib.Path(value) / "auth.json").exists()
                                    for value in state.get("driver_homes", {}).values())
    write_json(pathlib.Path(state["control"]) / "state.json", state)
    if failures:
        raise RuntimeError("; ".join(failures))


def mark_component(state, name, receipts, verdict):
    if not can_start(state["reservations"], name):
        raise RuntimeError(f"{name} does not have exact immutable downstream reservations")
    if verdict["status"] != "passed":
        raise RuntimeError(f"{name} failed its component envelope")
    state["reservations"][name]["status"] = "complete"
    state.setdefault("components", {})[name] = {"stages": receipts, "verdict": verdict}
    write_json(pathlib.Path(state["control"]) / "state.json", state)


def contribution_specs(state, briefs, lineage):
    return [stage_spec(state, f"{role.lower()}_contribution", "contribution", role, briefs[role],
                       lineage) for role in ROLES]


def product_select(state, request_text, limits):
    lineage = (state["source_manifest"]["sha256"],)
    spec = stage_spec(state, "product_select", "product_select", "Product",
                      "Select direct evidence and issue three role briefs.", lineage,
                      generated=(("fixture_request", request_text),))
    receipts, verdict = run_group(state, [spec], limits)
    selection = select_briefs(receipts[0]["output"])
    selection["receipt"] = receipts[0]
    return receipts, verdict, selection


def product_synthesis(state, selection, contributions, limits, probe=False):
    carrier_manifest = dict(state["carriers"])
    carrier_manifest.update({receipt["role"]: receipt["carrier"] for receipt in contributions
                             if receipt.get("role") and receipt.get("carrier")})
    product_selection = selection["receipt"]["output"]
    generated = (("product_selection", product_selection),) + tuple(
        (receipt["name"], receipt["output"]) for receipt in contributions) + (
            ("carrier_manifest", json.dumps(carrier_manifest, sort_keys=True)),)
    lineage = (state["source_manifest"]["sha256"], selection["receipt"]["output_sha256"],
               *(receipt["output_sha256"] for receipt in contributions))
    spec = stage_spec(state, "product_synthesis", "product_synthesis", "Product",
                      "Integrate the selected evidence and contributions before code.", lineage, generated=generated)
    receipts, verdict = run_group(state, [spec], limits)
    commit_product_record(state, receipts[0]["output"], probe=probe)
    return receipts, verdict


def engineering_sequence(state, contribution, synthesis, limits):
    receipts = []
    previous = synthesis["output_sha256"]
    prompts = (
        ("engineering_implement", "implement", "Implement the committed Product decision only.", "workspace-write"),
        ("engineering_run", "run", "Execute the smallest direct proof of the committed Product decision.", "read-only"),
        ("engineering_return", "return", "Return to the observed run as Engineering.", "read-only"),
    )
    for receipt_name, stage, brief, sandbox in prompts:
        lineage = [state["source_manifest"]["sha256"], contribution["output_sha256"], previous]
        generated = [("prior_stage", previous)]
        if stage == "implement":
            product_synthesis_bytes = synthesis["output"]
            implementation_brief = state.get("implementation_brief")
            if not isinstance(implementation_brief, str) or not implementation_brief.strip():
                raise RuntimeError("Product supplied no exact implementation brief")
            generated = [("product_synthesis", product_synthesis_bytes),
                         ("implementation_brief", implementation_brief)]
            lineage += [sha256_text(product_synthesis_bytes), sha256_text(implementation_brief)]
        if stage in ("run", "return"):
            implementation_path = pathlib.Path(state["root"]) / SOURCE_PATHS["engineering"]
            implementation = implementation_path.read_text()
            implementation_commit = git_output(state["root"], "rev-parse", "HEAD")
            if git_output(state["root"], "status", "--porcelain", "--", SOURCE_PATHS["engineering"]):
                raise RuntimeError("Engineering implementation bytes are not committed")
            if stage == "run":
                synthesis_commit = state.get("synthesis_commit")
                if (not synthesis_commit or implementation_commit == synthesis_commit or
                        SOURCE_PATHS["engineering"] not in git_output(
                            state["root"], "diff", "--name-only", synthesis_commit,
                            implementation_commit, "--", SOURCE_PATHS["engineering"]).splitlines()):
                    raise RuntimeError("Engineering run has no committed implementation change")
                state["implementation_commit"] = implementation_commit
                state["implementation_sha256"] = sha256_text(implementation)
            elif (implementation_commit != state.get("implementation_commit") or
                  sha256_text(implementation) != state.get("implementation_sha256")):
                raise RuntimeError("Engineering implementation changed after its run packet")
            generated += [("current_implementation", implementation),
                          ("implementation_commit", implementation_commit)]
            lineage += [sha256_text(implementation), sha256_text(implementation_commit)]
        if stage == "return":
            command_evidence = receipts[-1].get("command_evidence")
            if not host_proof.command_evidence_ok(command_evidence):
                raise RuntimeError("Engineering run supplied no authoritative command evidence")
            run_evidence = canonical_json(command_evidence).decode()
            generated.append(("run_evidence", run_evidence))
            lineage.append(sha256_text(run_evidence))
        spec = stage_spec(state, receipt_name, stage, "Engineering", brief, lineage,
                          generated=generated, sandbox=sandbox)
        current_receipts, _ = run_group(state, [spec], limits)
        receipts.extend(current_receipts)
        previous = current_receipts[0]["output_sha256"]
        current_verdict = aggregate_receipts(receipts, limits)
        if current_verdict["status"] == "over":
            raise RuntimeError("Engineering crossed its cumulative component envelope")
    verdict = aggregate_receipts(receipts, limits)
    if verdict["status"] != "passed" or verdict["usage"]["responses"] != 3:
        raise RuntimeError("Engineering did not complete its bounded three-response component")
    return receipts, verdict


def role_returns(state, roles, contributions, run_output, limits):
    specs = []
    command = run_output.get("command_evidence")
    if not host_proof.command_evidence_ok(command):
        raise RuntimeError("role returns require authoritative command evidence")
    real_run = canonical_json(command).decode()
    for role in roles:
        contribution = next(receipt for receipt in contributions if receipt["role"] == role)
        lineage = (state["source_manifest"]["sha256"], contribution["output_sha256"],
                   sha256_text(real_run))
        spec = stage_spec(state, f"{role.lower()}_return", "return", role,
                          f"Return to the real {run_output['name']} evidence.", lineage,
                          generated=(("contribution", contribution["output"]),
                                     ("real_run", real_run)))
        specs.append(spec)
    return run_group(state, specs, limits, require_overlap=len(specs) > 1)


def product_close(state, selection, synthesis, engineering, returns, limits):
    run_receipt = next((item for item in state["invocations"] if item.get("name") == "engineering_run"), None)
    command = run_receipt.get("command_evidence") if run_receipt else None
    if not host_proof.command_evidence_ok(command):
        raise RuntimeError("Product close requires authoritative command evidence")
    real_run = canonical_json(command).decode()
    implementation = (pathlib.Path(state["root"]) / SOURCE_PATHS["engineering"]).read_text()
    implementation_commit = state.get("implementation_commit", "")
    lineage = (state["source_manifest"]["sha256"], selection["output_sha256"],
               synthesis["output_sha256"], engineering["output_sha256"],
               *(receipt["output_sha256"] for receipt in returns), sha256_text(real_run),
               sha256_text(implementation), sha256_text(implementation_commit))
    generated = (("product_synthesis", synthesis["output"]),
                 ("current_implementation", implementation),
                 ("implementation_commit", implementation_commit),
                 ("run_evidence", real_run),
                 ("engineering_return", engineering["output"])) + tuple(
                     (receipt["name"], receipt["output"]) for receipt in returns)
    spec = stage_spec(state, "product_close", "product_close", "Product",
                      "Close the role record without opening review.", lineage, generated=generated)
    receipts, verdict = run_group(state, [spec], limits)
    close_product_record(state, receipts[0]["output"])
    return receipts, verdict


def probe_path(admission_root, identity):
    key = hashlib.sha256(canonical_json(identity)).hexdigest()[:20]
    directory = pathlib.Path(admission_root).resolve() / key
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    return directory / "admission.json"


def save_probe(state, admission_root, name, receipts, verdict):
    if verdict["status"] != "passed" or verdict["usage"]["responses"] != PROBE_LIMITS[name]["responses"]:
        raise RuntimeError(f"{name} probe did not satisfy its exact response and resource envelope")
    if (not all(host_proof.bound_stage_ok(stage, stage_name, state["source_manifest"]) and
                stage["verdict"]["limits"] == host_proof.probe_stage_limits(name, stage_name)
                for stage, stage_name in zip(receipts, host_proof.PROBE_STAGES[name])) or
            not host_proof.probe_evidence_ok(name, {"stages": receipts, "verdict": verdict},
                                             state["source_manifest"]["sha256"])):
        raise RuntimeError(f"{name} probe evidence is not self-verifying")
    path = probe_path(admission_root, state["identity"])
    if path.is_file():
        value = json.loads(path.read_text())
        if any(value.get(field) != state["identity"][field] for field in host_proof.ADMISSION_FIELDS):
            raise RuntimeError("existing admission identity does not match this probe")
    else:
        value = {**state["identity"], "source_manifest": state["source_manifest"], "probes": {}}
    probe = {**state["identity"], "name": name, "status": "passed", "limits": PROBE_LIMITS[name],
             "verdict": verdict, "stages": receipts}
    value["probes"][name] = probe
    write_json(path, value)
    state["probe"] = probe
    state["admission_path"] = str(path)
    return path


def contribution_probe_briefs():
    briefs = {
        "Business": "Use business-evidence.md and the applicable product excerpt to decide the one bounded value question in the fixture.",
        "Experience": "Use experience-evidence.md and the applicable product excerpts to decide the one bounded experience question in the fixture.",
        "Engineering": "Use the supplied pulse.py excerpts and product promise to decide the smallest safe implementation seam and regression proof.",
    }
    if any(hint in brief.lower() for brief in briefs.values() for hint in SOLUTION_HINTS):
        raise RuntimeError("contribution probe brief supplied the Product solution")
    return briefs


def run_probe(state, name, request_text, admission_root):
    source = state["source_manifest"]["sha256"]
    if name == "contributions":
        briefs = contribution_probe_briefs()
        receipts, _ = run_group(state, contribution_specs(state, briefs, (source,)),
                                PROBE_LIMITS[name], require_overlap=True)
    elif name == "product":
        selected, _, selection = product_select(state, request_text, STAGE_LIMITS["product_select"])
        synthetic = []
        for role in ROLES:
            output = (f"Role: {role}\nDirect evidence: fixed {role} probe evidence.\nConclusion: preserve gaps "
                      "and remove streaks, praise, pressure, and price.\nAssumption: the fixture is representative.\n"
                      "Proposed change: one seven-day view.\nConsequence: the product remains calm.\n"
                      "Earliest disconfirming run: mixed-gap pulse week.")
            synthetic.append({"name": f"{role.lower()}_contribution", "role": role, "output": output,
                              "output_sha256": sha256_text(output), "carrier": f"fixture-{role.lower()}"})
        synthesized, _ = product_synthesis(state, selection, synthetic,
                                            STAGE_LIMITS["product_synthesis"], probe=True)
        receipts = selected + synthesized
    elif name == "business":
        brief = "Use business-evidence.md to test the bounded weekly view's cost and durable value before any full run."
        contribution, _ = run_group(
            state, [stage_spec(state, "business_contribution", "contribution", "Business", brief, (source,))],
            PROBE_LIMITS[name])
        observed_output = "supplied isolated run evidence"
        observed_command = {"command": "python3 pulse.py week", "exit_code": 0,
                            "output": "seven-day view with visible gaps"}
        observed_command["sha256"] = hashlib.sha256(canonical_json(observed_command)).hexdigest()
        observed = {"name": "probe_run", "output": observed_output,
                    "output_sha256": sha256_text(observed_output), "command_evidence": observed_command}
        returned, _ = role_returns(state, ("Business",), contribution, observed, PROBE_LIMITS[name])
        receipts = contribution + returned
    elif name == "engineering":
        brief = "Use pulse.py to design the smallest safe seven-day view, then implement, run, and return in this carrier."
        contribution, _ = run_group(
            state, [stage_spec(state, "engineering_contribution", "contribution", "Engineering", brief, (source,))],
            PROBE_LIMITS[name])
        synthesis_output = "Committed probe synthesis: build pulse week as a seven-day gap-preserving view without pressure."
        synthesis = {"output": synthesis_output, "output_sha256": sha256_text(synthesis_output)}
        state["implementation_brief"] = synthesis_output
        record = pathlib.Path(state["root"]) / "examples/pulse/work/weekly-view.md"
        record.write_text("# Weekly view\n\n**Product synthesis:** " + synthesis_output + "\n")
        git_output(state["root"], "add", "examples/pulse/work/weekly-view.md")
        git_output(state["root"], "commit", "-m", "Record Engineering probe handoff")
        state["synthesis_commit"] = git_output(state["root"], "rev-parse", "HEAD")
        remaining, _ = engineering_sequence(state, contribution[0], synthesis, PROBE_LIMITS[name])
        receipts = contribution + remaining
    else:
        raise RuntimeError(f"unknown Piece 9 probe: {name}")
    verdict = aggregate_receipts(receipts, PROBE_LIMITS[name], concurrent=name == "contributions")
    path = save_probe(state, admission_root, name, receipts, verdict)
    state["status"] = "passed"
    state["result"] = {"mode": f"probe:{name}", "verdict": verdict, "admission_path": str(path)}


def run_full(state, request_text, admission_root):
    admission = probe_path(admission_root, state["identity"])
    if not admission.is_file():
        raise RuntimeError("full run blocked: no isolated-probe admission exists for this identity")
    receipt = json.loads(admission.read_text())
    if not host_proof.admission_ok(receipt, state["identity"]):
        raise RuntimeError("full run blocked: four exact isolated probe receipts do not admit this identity")
    state["admission_path"] = str(admission)
    started = time.monotonic()

    selected, verdict, selection = product_select(state, request_text, STAGE_LIMITS["product_select"])
    mark_component(state, "product_select", selected, verdict)

    source = state["source_manifest"]["sha256"]
    contributions, verdict = run_group(
        state, contribution_specs(state, selection["role_briefs"],
                                  (source, selected[0]["output_sha256"])),
        STAGE_LIMITS["contributions"], require_overlap=True)
    mark_component(state, "contributions", contributions, verdict)

    synthesized, verdict = product_synthesis(state, selection, contributions,
                                              STAGE_LIMITS["product_synthesis"])
    mark_component(state, "product_synthesis", synthesized, verdict)

    engineering_contribution = next(receipt for receipt in contributions if receipt["role"] == "Engineering")
    engineering, verdict = engineering_sequence(state, engineering_contribution, synthesized[0],
                                                 STAGE_LIMITS["engineering"])
    mark_component(state, "engineering", engineering, verdict)

    returned, verdict = role_returns(state, ("Business", "Experience"), contributions,
                                     engineering[-2], STAGE_LIMITS["returns"])
    mark_component(state, "returns", returned, verdict)

    closed, verdict = product_close(state, selected[0], synthesized[0], engineering[-1], returned,
                                    STAGE_LIMITS["product_close"])
    mark_component(state, "product_close", closed, verdict)

    full_elapsed = time.monotonic() - started
    full_usage = host_proof.add_usage(*(item["verdict"]["usage"] for item in state["invocations"]))
    full_verdict = host_proof.stage_verdict(full_usage, full_elapsed, FULL_LIMITS, True)
    component_usage = host_proof.add_usage(*(entry["verdict"]["usage"]
                                             for entry in state["components"].values()))
    if full_usage != component_usage or full_verdict["status"] != "passed":
        raise RuntimeError("complete run failed its exact aggregate envelope")
    state["status"] = "passed"
    state["result"] = {"mode": "full", "verdict": full_verdict,
                       "component_usage": component_usage, "admission_path": str(admission)}


def controller(root_arg, control_arg, mode, driver, model, effort, admission_root, prompt_path, kernel_root):
    if driver not in ("codex", "claude") or not model or not effort:
        raise RuntimeError("controller requires explicit codex|claude driver, model, and effort")
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    state = None
    try:
        state = prepare_controller(root_arg, control_arg, driver, model, effort, prompt_path, kernel_root)
        request_text = pathlib.Path(prompt_path).read_text()
        if mode.startswith("probe:"):
            run_probe(state, mode.split(":", 1)[1], request_text, admission_root)
        elif mode == "full":
            run_full(state, request_text, admission_root)
        else:
            raise RuntimeError(f"unknown controller mode: {mode}")
    except BaseException as error:
        if state is not None:
            state["status"] = "failed"
            state["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        if state is not None:
            cleanup_controller(state)
    return state


if __name__ == "__main__":
    if len(sys.argv) == 11 and sys.argv[1] == "controller":
        result = controller(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6],
                            sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
        print(json.dumps(result["result"], sort_keys=True))
    elif len(sys.argv) == 3 and sys.argv[1] == "cleanup":
        cleanup_path = pathlib.Path(sys.argv[2]).resolve()
        cleanup_controller(json.loads(cleanup_path.read_text()))
    else:
        raise SystemExit("usage: role-broker.py controller CLONE CONTROL MODE DRIVER MODEL EFFORT ADMISSION PROMPT KERNEL | cleanup STATE")
