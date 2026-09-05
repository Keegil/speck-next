#!/usr/bin/env python3
"""Fixed six-stage transport for the separated-product-team development fixture."""
import base64, hashlib, json, os, pathlib, platform, shutil, signal, subprocess, sys, tempfile, time
import host_proof

ROLES = ("Business", "Experience", "Engineering")
STAGES = {
    "Business": ("contribution", "return"),
    "Experience": ("contribution", "return"),
    "Engineering": ("contribution", "implement", "return"),
}
current = None
active_processes = []
home = None
root_home = None
startup_ready = False
PACKET_SCHEMA = "piece9-packet-v1"
STAGE_ORDER = host_proof.STAGE_ORDER
STAGE_LIMITS = host_proof.STAGE_LIMITS
PROBE_LIMITS = host_proof.PROBE_LIMITS
FULL_LIMITS = host_proof.FULL_LIMITS
SOURCE_PATHS = host_proof.SOURCE_PATHS
ALL_SOURCE_PATHS = host_proof.ALL_SOURCE_PATHS
SOURCE_ALLOWLIST = host_proof.SOURCE_ALLOWLIST


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def make_packet(root, stage, role, brief, paths, lineage=(), generated=()):
    root = pathlib.Path(root).resolve()
    expected_paths = SOURCE_ALLOWLIST.get((stage, role))
    if expected_paths is None or tuple(paths) != tuple(expected_paths):
        raise ValueError(f"source paths are not the fixed allowlist for {role} {stage}")
    if not all(isinstance(value, str) and len(value) == 64 and
               all(character in "0123456789abcdef" for character in value) for value in lineage):
        raise ValueError("packet lineage contains a malformed digest")
    evidence = []
    seen = set()
    for name in paths:
        relative = pathlib.PurePosixPath(str(name))
        if relative.is_absolute() or ".." in relative.parts or str(relative) in seen:
            raise ValueError(f"unsafe or duplicate evidence path: {name}")
        seen.add(str(relative))
        source = (root / pathlib.Path(*relative.parts)).resolve(strict=True)
        try:
            confined = os.path.commonpath((str(root), str(source))) == str(root)
        except ValueError:
            confined = False
        if not confined or not source.is_file():
            raise ValueError(f"evidence path escapes product root: {name}")
        content = source.read_bytes()
        evidence.append({
            "path": str(relative), "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
            "content_base64": base64.b64encode(content).decode("ascii"),
        })
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
    return {"body": body, "sha256": hashlib.sha256(canonical_json(body)).hexdigest(),
            **body}


def verify_packet(packet):
    try:
        body = packet["body"]
        if packet.get("sha256") != hashlib.sha256(canonical_json(body)).hexdigest():
            return False
        if any(packet.get(key) != value for key, value in body.items()):
            return False
        for item in body["evidence"]:
            content = base64.b64decode(item["content_base64"], validate=True)
            if len(content) != item["bytes"] or hashlib.sha256(content).hexdigest() != item["sha256"]:
                return False
        for item in body["generated"]:
            content = item["content"].encode()
            if len(content) != item["bytes"] or hashlib.sha256(content).hexdigest() != item["sha256"]:
                return False
        expected = SOURCE_ALLOWLIST.get((body.get("stage"), body.get("role")))
        return (body.get("schema") == PACKET_SCHEMA and expected is not None and
                tuple(item.get("path") for item in body["evidence"]) == tuple(expected) and
                all(isinstance(value, str) and len(value) == 64 and
                    all(character in "0123456789abcdef" for character in value)
                    for value in body.get("lineage", [])))
    except (KeyError, TypeError, ValueError):
        return False


def source_manifest(root, prompt_sha256):
    packet = make_packet(root, "source-manifest", "runner", "immutable fixture sources",
                         ALL_SOURCE_PATHS, lineage=(prompt_sha256,))
    entries = [{key: item[key] for key in ("path", "bytes", "sha256")}
               for item in packet["evidence"]]
    body = {"schema": PACKET_SCHEMA, "prompt_sha256": prompt_sha256, "evidence": entries}
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


def clean_secret():
    for task_home in (home, root_home):
        if not task_home:
            continue
        auth = pathlib.Path(task_home) / "auth.json"
        if auth.exists():
            auth.unlink()


def discard_startup_homes():
    """Remove only the two exact task homes after a failed startup."""
    temp_root = pathlib.Path(tempfile.gettempdir()).resolve()
    for task_home, prefix in ((home, "speck-role-home."), (root_home, "speck-product-home.")):
        if not task_home:
            continue
        path = pathlib.Path(task_home).resolve()
        if path.parent != temp_root or not path.name.startswith(prefix):
            continue
        auth = path / "auth.json"
        if auth.exists():
            auth.unlink()
        if path.exists():
            moved = subprocess.run(["trash", str(path)], capture_output=True).returncode == 0
            if not moved and path.exists():
                shutil.rmtree(path)


def stop(_signum=None, _frame=None):
    for process in list(active_processes):
        if process.poll() is None:
            process.terminate()
    if current and current.poll() is None:
        current.terminate()
        try:
            current.wait(timeout=3)
        except subprocess.TimeoutExpired:
            current.kill()
    clean_secret()
    raise SystemExit(143)


def session_id(events_path):
    for line in pathlib.Path(events_path).read_text(errors="ignore").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "thread.started" and event.get("thread_id"):
            return event["thread_id"]
    return None


def run_child(root, control, state, role, stage, brief):
    global current
    stem = f"{role.lower()}-{stage}"
    events = control / f"{stem}.events.jsonl"
    stderr = control / f"{stem}.stderr.log"
    output = control / f"{stem}.output.md"
    neutral = pathlib.Path(state["role_cwd"])
    location = f"Product root: {root}. Treat every relative evidence or implementation path as relative to that root and use its absolute path."
    if stage == "contribution":
        prompt = f"""You are the separate {role} role for one bounded product piece. Read only the direct product evidence named below.
Do not load optional skills, review the methodology, edit files, or act as another role. Return a dedicated `Role: {role}`
line, direct evidence consulted, conclusion, assumptions, proposed change, material consequence, and earliest disconfirming run.

{location}\n\nProduct-authored brief:\n{brief}"""
        command = ["codex", "exec", "--json", "--sandbox", "read-only", "--skip-git-repo-check",
                   "--ignore-user-config"]
        command += ["-C", str(neutral), "-o", str(output), prompt]
    else:
        carrier = state["sessions"].get(role)
        if not carrier:
            raise RuntimeError(f"{role} has no contribution session to resume")
        if stage == "implement":
            prompt = f"""Continue as Engineering implementation owner. Product has committed the pre-code synthesis described below.
Edit only the named product implementation, run the smallest honest mixed-gap CLI proof, and commit the implementation.
Do not open review or summon another context. Return `Role: Engineering`, files changed, commands and observed results.

{location}\n\nProduct-authored handoff:\n{brief}"""
            sandbox = "workspace-write"
        else:
            prompt = f"""Return as the same active {role} role to the first real run described below. Do not edit product files or open review.
Return a dedicated `Role: {role}` line, the evidence observed, what changed or held, and the resulting change.
{('Give a binding `Business ruling: kept`, `Business ruling: broken`, or `Business ruling: not judged` with the direct business evidence and reason.' if role == 'Business' else '')}

{location}\n\nProduct-authored run evidence:\n{brief}"""
            sandbox = "read-only"
        command = ["codex", "exec", "--json", "--sandbox", sandbox, "--skip-git-repo-check",
                   "--ignore-user-config"]
        if role == "Engineering" and stage == "implement":
            command += ["--add-dir", str(root)]
        command += ["-C", str(neutral), "-o", str(output), "resume", carrier, prompt]

    env = dict(os.environ, CODEX_HOME=str(home))
    with events.open("w") as out, stderr.open("w") as err:
        current = subprocess.Popen(command, cwd=root, env=env, stdin=subprocess.DEVNULL,
                                   stdout=out, stderr=err, text=True)
        rc = current.wait()
    current = None
    if rc:
        raise RuntimeError(f"{role} {stage} exited {rc}; see runner-owned stderr")
    carrier = session_id(events) or state["sessions"].get(role)
    contribution = output.read_text(errors="ignore") if output.exists() else ""
    if not carrier or not any(line.strip() == f"Role: {role}" for line in contribution.splitlines()):
        raise RuntimeError(f"{role} {stage} returned no verified carrier contribution")
    state["sessions"][role] = carrier
    state["events"].setdefault(role, {})[stage] = str(events)
    write_json(control / "state.json", state)
    return {"role": role, "stage": stage, "carrier": carrier, "contribution": contribution}


def serve(root_arg, control_arg):
    global home, root_home, startup_ready
    root = pathlib.Path(root_arg).resolve()
    control = pathlib.Path(control_arg).resolve()
    control.mkdir(parents=True, exist_ok=True, mode=0o700)
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    state = None
    startup_ready = False
    try:
        home = pathlib.Path(tempfile.mkdtemp(prefix="speck-role-home."))
        root_home = pathlib.Path(tempfile.mkdtemp(prefix="speck-product-home."))
        os.chmod(home, 0o700)
        os.chmod(root_home, 0o700)
        requests = root / ".devsuite-role-ipc" / "requests"
        responses = root / ".devsuite-role-ipc" / "responses"
        neutral = control / "role-cwd"
        state = {"driver": "codex", "root": str(root), "role_cwd": str(neutral), "home": str(home),
                 "root_home": str(root_home), "startup_phase": "homes-created",
                 "sessions": {}, "events": {}, "handled": []}
        write_json(control / "state.json", state)
        auth_source = pathlib.Path.home() / ".codex" / "auth.json"
        for auth_target in (home / "auth.json", root_home / "auth.json"):
            shutil.copyfile(auth_source, auth_target)
            os.chmod(auth_target, 0o600)
        startup_fault = os.environ.get("SPECK_DEVSUITE_INJECT_BROKER_STARTUP_FAILURE")
        if startup_fault == "pause-after-auth-copy":
            (control / "after-auth-copy").touch()
            while True:
                time.sleep(1)
        if startup_fault == "after-auth-copy":
            raise RuntimeError("injected failure after credential copy")
        requests.mkdir(parents=True, exist_ok=True)
        responses.mkdir(parents=True, exist_ok=True)
        neutral.mkdir(mode=0o700)
        state["startup_phase"] = "ready"
        write_json(control / "state.json", state)
        startup_ready = True
        while not (control / "stop").exists():
            progressed = False
            for role in ROLES:
                for stage in STAGES[role]:
                    key = f"{role.lower()}-{stage}"
                    request = requests / f"{key}.json"
                    response = responses / f"{key}.json"
                    if key in state["handled"] or not request.exists():
                        continue
                    expected = STAGES[role][len([x for x in state["handled"] if x.startswith(role.lower() + "-")])]
                    if stage != expected:
                        continue
                    value = json.loads(request.read_text())
                    if value.get("role") != role or value.get("stage") != stage or len(value.get("brief", "").strip()) < 80:
                        raise RuntimeError(f"invalid Product request {request.name}")
                    result = run_child(root, control, state, role, stage, value["brief"])
                    state["handled"].append(key)
                    write_json(control / "state.json", state)
                    write_json(response, result)
                    progressed = True
            if not progressed:
                time.sleep(0.25)
    finally:
        clean_secret()
        if state is not None:
            state["auth_removed"] = not (home / "auth.json").exists() and not (root_home / "auth.json").exists()
            if not startup_ready:
                discard_startup_homes()
                state["home"] = None
                state["root_home"] = None
                state["startup_phase"] = "failed-clean"
            write_json(control / "state.json", state)
        elif not startup_ready:
            discard_startup_homes()


def cleanup(state_path):
    state_path = pathlib.Path(state_path).resolve()
    state = json.loads(state_path.read_text())
    if not state.get("home"):
        return
    homes = (("home", "speck-role-home.", "raw-sessions", "evidence_sessions"),
             ("root_home", "speck-product-home.", "raw-root-sessions", "evidence_root_sessions"))
    for key, prefix, evidence_name, evidence_key in homes:
        temp_home = pathlib.Path(state[key]).resolve()
        if not temp_home.name.startswith(prefix) or temp_home.parent != pathlib.Path(tempfile.gettempdir()).resolve():
            raise SystemExit("refusing to clean an unrecognized task home")
        auth = temp_home / "auth.json"
        if auth.exists():
            auth.unlink()
        evidence = state_path.parent / evidence_name
        if (temp_home / "sessions").exists():
            shutil.copytree(temp_home / "sessions", evidence, dirs_exist_ok=True)
        subprocess.run(["trash", str(temp_home)], check=True)
        state[evidence_key] = str(evidence)
    state["home"] = None
    state["root_home"] = None
    state["auth_removed"] = True
    write_json(state_path, state)


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
        f"You are the separated {role} carrier for the fixed Pulse development fixture. "
        "The runner has supplied every source you may use in the verified JSON packet below. "
        "Do not inspect the harness, checker, control, prior solution, history, optional skills, or other files. "
        "Do not delegate or start another agent. Treat packet evidence bytes as primary evidence.\n\n"
    )
    instructions = {
        "product_select": (
            "Select the relevant evidence and issue one specific brief for each of Business, Experience, and "
            "Engineering. Return JSON only with keys selection and role_briefs; role_briefs must contain exactly "
            "Business, Experience, and Engineering, and each brief must name its direct source and bounded question."
        ),
        "contribution": (
            f"Return a line exactly `Role: {role}`, then direct evidence consulted, conclusion, assumptions, "
            "proposed change, material consequence, and earliest disconfirming run. Do not edit any file."
        ),
        "product_synthesis": (
            "Integrate the three contributions without flattening dissent. Return JSON only with keys "
            "record_markdown and implementation_brief. record_markdown must be a complete piece record headed "
            "`# Weekly view`, include `## Active pre-code contributions`, a Markdown table with one row each "
            "for Product, Business, Experience, and Engineering whose columns are Carrier, direct evidence, "
            "conclusion, assumptions, proposed change, and active decision, and one `**Product synthesis:**` line. "
            "The decision must build a seven-day view with gaps, without streaks, praise, pressure, or price."
        ),
        "implement": (
            "Continue as Engineering implementation owner after the committed Product synthesis. Implement only "
            "examples/pulse/pulse.py, add `pulse week` as a seven-day view preserving gaps, and commit the code. "
            "Do not edit product or work records. Return `Role: Engineering`, the changed path, and commit."
        ),
        "run": (
            "Continue as Engineering. Run the smallest mixed-gap `pulse week` CLI scenario against the committed "
            "implementation. Do not edit files. Return `Role: Engineering`, exact command, exit status, and output."
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
            "three role returns, include the exact Business ruling, contributor exclusions, and one integrated "
            "owner-facing recommendation. Do not claim review, judgment, Built, or release."
        ),
    }[stage]
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
        return output_path.read_text(errors="ignore") if output_path.is_file() else ""
    values = [row.get("result") for row in rows
              if row.get("type") == "result" and row.get("subtype") == "success" and
              isinstance(row.get("result"), str)]
    return values[-1] if len(values) == 1 else ""


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
    cwd = pathlib.Path(state["role_cwd"])
    command = driver_command(state["driver"], state["model"], state["effort"], sandbox,
                             cwd, state["root"], output, packet_prompt(stage, role, packet), carrier)
    env = dict(os.environ)
    if state["driver"] == "codex":
        env["CODEX_HOME"] = state["driver_home"]
    event_handle = events.open("w")
    error_handle = stderr.open("w")
    started_at = time.time()
    started = time.monotonic()
    process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                               stdout=event_handle, stderr=error_handle, text=True)
    active_processes.append(process)
    return {**spec, "process": process, "events": events, "stderr": stderr, "output_path": output,
            "event_handle": event_handle, "error_handle": error_handle,
            "started": started, "started_at": started_at, "limits": limits}


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
        elapsed = time.monotonic() - min(item["started"] for item in invocations)
        usage = host_proof.add_usage(*(partial_usage(state["driver"], item["events"])
                                       for item in invocations))
        if elapsed > limits["wall"] or usage["gross"] > limits["gross"] or usage["fresh"] > limits["fresh"]:
            stopped = True
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
        ended, ended_at = time.monotonic(), time.time()
        rows = host_proof.jsonl(item["events"])
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
        elif observed and observed != expected:
            failures.append(f"{item['role']} carrier changed on resume")
        output = invocation_output(state["driver"], rows, item["output_path"])
        if not output.strip():
            failures.append(f"{item['receipt_name']} emitted no terminal assistant result")
        complete = item["process"].returncode == 0 and usage["responses"] == 1 and not stopped
        if not complete:
            failures.append(f"{item['receipt_name']} did not complete exactly one response")
        before = state["carrier_usage"].get(item["role"], host_proof.empty_usage())
        after = host_proof.add_usage(before, usage)
        delta = host_proof.usage_delta(after, before)
        state["carrier_usage"][item["role"]] = after
        elapsed = ended - item["started"]
        verdict = host_proof.stage_verdict(delta, elapsed, limits, complete)
        receipt = {
            "name": item["receipt_name"], "role": item["role"], "carrier": expected,
            "observed_carrier": observed, "packet_sha256": item["packet"]["sha256"],
            "packet": item["packet"], "input_lineage": item["packet"]["lineage"],
            "output": output, "output_sha256": sha256_text(output),
            "interval": [item["started"], ended], "started_at": item["started_at"],
            "ended_at": ended_at, "usage_before": before, "usage_after": after, "verdict": verdict,
        }
        receipts.append(receipt)
        state["invocations"].append(receipt)
    intervals = [receipt["interval"] for receipt in receipts]
    if require_overlap and not host_proof.intervals_overlap(intervals):
        failures.append("concurrent group had no common monotonic overlap")
    usage = host_proof.add_usage(*(receipt["verdict"]["usage"] for receipt in receipts))
    elapsed = max(end for _, end in intervals) - min(start for start, _ in intervals)
    complete = not failures
    verdict = host_proof.stage_verdict(usage, elapsed, limits, complete)
    if verdict["status"] != "passed":
        failures.append(f"group verdict: {verdict['status']} {','.join(verdict['reasons'])}")
    state["last_group"] = {"verdict": verdict, "failures": failures}
    write_json(pathlib.Path(state["control"]) / "state.json", state)
    if failures:
        raise RuntimeError("; ".join(dict.fromkeys(failures)))
    return receipts, verdict


def run_group(state, specs, limits, require_overlap=False):
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
    driver_home = None
    if driver == "codex":
        driver_home = pathlib.Path(tempfile.mkdtemp(prefix="speck-piece9-codex-home."))
        os.chmod(driver_home, 0o700)
        try:
            auth_source = pathlib.Path.home() / ".codex" / "auth.json"
            if not auth_source.is_file():
                raise RuntimeError("Codex auth source is unavailable")
            shutil.copyfile(auth_source, driver_home / "auth.json")
            os.chmod(driver_home / "auth.json", 0o600)
        except BaseException:
            subprocess.run(["trash", str(driver_home)], check=True)
            raise
    state = {
        "protocol": PACKET_SCHEMA, "root": str(root), "control": str(control),
        "source_root": str(snapshot), "role_cwd": str(role_cwd), "driver_home": str(driver_home) if driver_home else None,
        "driver": driver, "model": model, "effort": effort, "identity": identity,
        "source_manifest": manifest, "carriers": {}, "carrier_usage": {}, "invocations": [],
        "reservations": reservation_plan(), "auth_removed": driver != "codex", "status": "starting",
    }
    write_json(control / "state.json", state)
    return state


def cleanup_controller(state):
    task_home = state.get("driver_home")
    if task_home:
        path = pathlib.Path(task_home).resolve()
        expected_parent = pathlib.Path(tempfile.gettempdir()).resolve()
        if path.parent != expected_parent or not path.name.startswith("speck-piece9-codex-home."):
            raise RuntimeError("refusing to clean an unrecognized controller home")
        auth = path / "auth.json"
        if auth.exists():
            auth.unlink()
        if path.exists():
            subprocess.run(["trash", str(path)], check=True)
        state["driver_home"] = None
        state["auth_removed"] = not path.exists()
    write_json(pathlib.Path(state["control"]) / "state.json", state)


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
    generated = (("selection", selection["selection"]),) + tuple(
        (receipt["name"], receipt["output"]) for receipt in contributions)
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
        ("engineering_run", "run", "Execute the smallest mixed-gap Pulse week proof.", "read-only"),
        ("engineering_return", "return", "Return to the observed run as Engineering.", "read-only"),
    )
    for receipt_name, stage, brief, sandbox in prompts:
        lineage = (state["source_manifest"]["sha256"], contribution["output_sha256"], previous)
        spec = stage_spec(state, receipt_name, stage, "Engineering", brief, lineage,
                          generated=(("prior_stage", previous),), sandbox=sandbox)
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
    for role in roles:
        contribution = next(receipt for receipt in contributions if receipt["role"] == role)
        lineage = (state["source_manifest"]["sha256"], contribution["output_sha256"],
                   run_output["output_sha256"])
        spec = stage_spec(state, f"{role.lower()}_return", "return", role,
                          f"Return to the real {run_output['name']} evidence.", lineage,
                          generated=(("contribution", contribution["output"]),
                                     ("real_run", run_output["output"])))
        specs.append(spec)
    return run_group(state, specs, limits, require_overlap=len(specs) > 1)


def product_close(state, selection, synthesis, engineering, returns, limits):
    lineage = (state["source_manifest"]["sha256"], selection["output_sha256"],
               synthesis["output_sha256"], engineering["output_sha256"],
               *(receipt["output_sha256"] for receipt in returns))
    generated = (("product_synthesis", synthesis["output"]),
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


def run_probe(state, name, request_text, admission_root):
    source = state["source_manifest"]["sha256"]
    if name == "contributions":
        briefs = {
            "Business": "Use business-evidence.md to test whether this weekly view earns its operating and attention cost.",
            "Experience": "Use experience-evidence.md to test whether this weekly view stays calm, legible, and pressure-free.",
            "Engineering": "Use pulse.py to test the smallest safe seven-day view with honest gaps and no new dependency.",
        }
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
                              "output_sha256": sha256_text(output)})
        synthesized, _ = product_synthesis(state, selection, synthetic,
                                            STAGE_LIMITS["product_synthesis"], probe=True)
        receipts = selected + synthesized
    elif name == "business":
        brief = "Use business-evidence.md to test the bounded weekly view's cost and durable value before any full run."
        contribution, _ = run_group(
            state, [stage_spec(state, "business_contribution", "contribution", "Business", brief, (source,))],
            PROBE_LIMITS[name])
        observed = {"name": "probe_run", "output": "pulse week exited 0 with seven days, visible gaps, and no pressure",
                    "output_sha256": sha256_text("pulse week exited 0 with seven days, visible gaps, and no pressure")}
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
    global home
    if driver not in ("codex", "claude") or not model or not effort:
        raise RuntimeError("controller requires explicit codex|claude driver, model, and effort")
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    state = None
    try:
        state = prepare_controller(root_arg, control_arg, driver, model, effort, prompt_path, kernel_root)
        home = pathlib.Path(state["driver_home"]) if state["driver_home"] else None
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
    elif len(sys.argv) == 4 and sys.argv[1] == "serve":
        serve(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3 and sys.argv[1] == "cleanup":
        cleanup(sys.argv[2])
    else:
        raise SystemExit("usage: role-broker.py controller CLONE CONTROL MODE DRIVER MODEL EFFORT ADMISSION PROMPT KERNEL | serve CLONE CONTROL | cleanup STATE")
