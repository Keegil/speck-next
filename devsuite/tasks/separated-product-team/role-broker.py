#!/usr/bin/env python3
"""Fixed six-stage transport for the separated-product-team development fixture."""
import base64, concurrent.futures, hashlib, json, os, pathlib, shutil, signal, subprocess, sys, tempfile, time

ROLES = ("Business", "Experience", "Engineering")
STAGES = {
    "Business": ("contribution", "return"),
    "Experience": ("contribution", "return"),
    "Engineering": ("contribution", "implement", "return"),
}
current = None
home = None
root_home = None
startup_ready = False
PACKET_SCHEMA = "piece9-packet-v1"
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


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def make_packet(root, stage, role, brief, paths, lineage=()):
    root = pathlib.Path(root).resolve()
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
    body = {
        "schema": PACKET_SCHEMA, "stage": stage, "role": role, "brief": brief,
        "lineage": list(lineage), "evidence": evidence,
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
        return body.get("schema") == PACKET_SCHEMA
    except (KeyError, TypeError, ValueError):
        return False


def source_manifest(root, paths):
    packet = make_packet(root, "source-manifest", "runner", "immutable fixture sources", paths)
    entries = [{key: item[key] for key in ("path", "bytes", "sha256")}
               for item in packet["evidence"]]
    return {"schema": PACKET_SCHEMA, "evidence": entries,
            "sha256": hashlib.sha256(canonical_json(entries)).hexdigest()}


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


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "serve":
        serve(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3 and sys.argv[1] == "cleanup":
        cleanup(sys.argv[2])
    else:
        raise SystemExit("usage: role-broker.py serve CLONE CONTROL | cleanup STATE")
