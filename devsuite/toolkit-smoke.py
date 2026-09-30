#!/usr/bin/env python3
"""Network smoke of the shipped toolkit; downloads tools but makes no model calls.

Uses a fresh disposable cache with spaces by default. Leaves the retired cache
and fixture under the reported temporary directory for inspection. HOME, PATH,
host hooks and global tool configuration are not changed. Graft may write its
normal upstream update-check cache; telemetry is disabled by the shipped CLI.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time


TOOLS = {"graft", "rg", "jq", "ast-grep", "rtk"}
TOTAL_SECONDS = 540


class SmokeFailure(Exception):
    pass


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", type=Path, default=Path(__file__).resolve().parents[1] / "bin/speck-next.js")
    parser.add_argument("--cache", type=Path, help="Fresh cache to install and retire; must be absent or empty")
    args = parser.parse_args()
    cli = args.cli.resolve()
    if not cli.is_file():
        parser.error(f"CLI does not exist: {cli}")
    node = shutil.which("node")
    if not node:
        parser.error("Node.js is required")
    root = Path(tempfile.mkdtemp(prefix="speck toolkit smoke ")).resolve()
    cache = args.cache.resolve() if args.cache else root / "managed tool cache"
    if cache.exists() and (not cache.is_dir() or any(cache.iterdir())):
        parser.error(f"Use a fresh cache; refusing existing contents: {cache}")
    subject = root / "TypeScript subject"
    subject.mkdir()
    graph = root / "graft graph output"
    witness = root / "unmanaged witness.txt"
    witness.write_text("This file is outside the managed cache and must survive.\n")
    witness_hash = digest(witness)
    inventory = subject / "inventory.ts"
    inventory.write_text(
        "export interface Item { name: string; category: string; stock: number; }\n"
        "export const inventory: Item[] = [\n"
        "  { name: 'pear', category: 'fruit', stock: 4 },\n"
        "  { name: 'apple', category: 'fruit', stock: 0 },\n"
        "  { name: 'carrot', category: 'vegetable', stock: 2 },\n"
        "];\n"
        "export function selectCategory(items: Item[], category: string): Item[] {\n"
        "  return items.filter(item => item.category === category && item.stock > 0);\n"
        "}\n"
        "export function stockedFruit(): Item[] {\n"
        "  return selectCategory(inventory, 'fruit');\n"
        "}\n"
    )
    (subject / "package.json").write_text('{"name":"toolkit-smoke-subject","private":true}\n')
    fixture_hashes = {p.name: digest(p) for p in subject.iterdir()}
    env = dict(os.environ, SPECK_NEXT_TOOL_HOME=str(cache), GRAFT_NO_GITIGNORE="1", GRAFT_NO_IGNORE="1")
    started = time.monotonic()
    report = {"status": "running", "cli": str(cli), "cliSha256": digest(cli),
              "workdir": str(root), "cache": str(cache), "versions": {}, "checks": [],
              "durationsSeconds": {}, "networkRequired": True, "modelCalls": False,
              "homeOverridden": False}

    def run(label, command, expected=0, timeout=30, stdin=None):
        remaining = TOTAL_SECONDS - (time.monotonic() - started)
        if remaining <= 0:
            raise SmokeFailure("Total smoke time budget exhausted")
        before = time.monotonic()
        process = subprocess.Popen(command, cwd=subject, env=env, text=True,
                                   stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   start_new_session=os.name != "nt")
        try:
            stdout, stderr = process.communicate(input=stdin, timeout=min(timeout, remaining))
        except subprocess.TimeoutExpired:
            if os.name != "nt":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
            process.communicate()
            raise SmokeFailure(f"{label}: timed out") from None
        duration = round(time.monotonic() - before, 3)
        report["durationsSeconds"][label] = duration
        (root / f"{label}.stdout.txt").write_text(stdout)
        (root / f"{label}.stderr.txt").write_text(stderr)
        if process.returncode != expected:
            raise SmokeFailure(f"{label}: exit {process.returncode}, expected {expected}; {(stderr or stdout)[-1600:]}")
        return stdout, stderr

    def toolkit(label, *argv, **kwargs):
        return run(label, [node, str(cli), "tools", *argv], **kwargs)

    def tool(label, name, *argv, **kwargs):
        return toolkit(label, "run", name, "--", *argv, **kwargs)

    def check(label, condition, detail=""):
        if not condition:
            raise SmokeFailure(f"{label}: {detail or 'assertion failed'}")
        report["checks"].append(label)

    def receipts(directory):
        return {str(p.relative_to(directory)): p.read_bytes() for p in directory.glob("*/*/.speck-tool.json")}

    try:
        platform, _ = run("platform", [node, "-p", "process.platform + '-' + process.arch"])
        report["platform"] = platform.strip()
        run("git_init", ["git", "-c", "core.hooksPath=", "init", "--quiet"])
        run("git_add", ["git", "-c", "core.hooksPath=", "add", "inventory.ts", "package.json"])
        git_before, _ = run("git_before", ["git", "-c", "core.fsmonitor=false", "status", "--porcelain=v1"])
        toolkit("setup", "setup", timeout=360)
        out, _ = toolkit("doctor", "doctor", "--json", timeout=90)
        doctor = json.loads(out)
        check("doctor_all_five_ready", doctor.get("ready") and
              {t["name"] for t in doctor["tools"]} == TOOLS and
              all(t["managed"]["status"] == "ready" for t in doctor["tools"]))
        report["versions"] = {t["name"]: t["pinnedVersion"] for t in doctor["tools"]}

        out, _ = tool("rg_match", "rg", "--fixed-strings", "selectCategory", "inventory.ts")
        check("rg_finds_source", "export function selectCategory" in out)
        out, err = tool("rg_nonmatch", "rg", "--fixed-strings", "absentSmokeSymbol7331", "inventory.ts", expected=1)
        check("rg_preserves_nonmatch_exit_one", not out and not err)
        out, _ = tool("jq_filter", "jq", "-c", ".items | map(select(.stock > 0) | .name)",
                      stdin='{"items":[{"name":"pear","stock":4},{"name":"apple","stock":0}]}')
        check("jq_filters_json", json.loads(out) == ["pear"])
        out, _ = tool("ast_grep_match", "ast-grep", "run", "--lang", "typescript", "--pattern",
                      "selectCategory($$$ARGS)", "--json", "inventory.ts")
        matches = json.loads(out)
        check("ast_grep_finds_call", isinstance(matches, list) and
              any("selectCategory(inventory, 'fruit')" in match.get("text", "") for match in matches))

        tool("graft_build", "graft", "--dir", str(graph), "build", str(subject),
             "--no-gitignore", "--no-ignore", timeout=90)
        out, _ = tool("graft_skeleton", "graft", "--dir", str(graph), "skeleton", "inventory.ts", str(subject), timeout=60)
        check("graft_structural_skeleton", "selectCategory" in out and graph.is_dir())
        out, _ = tool("rtk_git_status", "rtk", "git", "status")
        check("rtk_summarizes_git_status", bool(out.strip()))
        out, err = tool("rtk_proxy_failure", "rtk", "proxy", node, "-e",
                        "process.stdout.write('raw-out\\n');process.stderr.write('raw-err\\n');process.exit(7)", expected=7)
        check("rtk_proxy_preserves_output_and_exit_seven", out == "raw-out\n" and err == "raw-err\n")

        check("fixture_files_unchanged", {p.name: digest(p) for p in subject.iterdir() if p.is_file()} == fixture_hashes)
        git_after, _ = run("git_after", ["git", "-c", "core.fsmonitor=false", "status", "--porcelain=v1"])
        check("fixture_git_status_unchanged", git_after == git_before)
        original_receipts = receipts(cache)
        check("five_install_receipts", len(original_receipts) == 5)
        toolkit("setup_repeat", "setup", timeout=90)
        check("repeat_setup_preserves_receipts", receipts(cache) == original_receipts)
        retired_before = set(cache.parent.glob(cache.name + ".retired-*"))
        toolkit("remove", "remove")
        retired = set(cache.parent.glob(cache.name + ".retired-*")) - retired_before
        check("remove_retires_managed_cache", not cache.exists() and len(retired) == 1)
        retired_cache = retired.pop()
        check("retired_receipts_preserved", receipts(retired_cache) == original_receipts)
        check("unmanaged_witness_preserved", witness.is_file() and digest(witness) == witness_hash)
        report["retiredCache"] = str(retired_cache)
        report["status"] = "passed"
    except (SmokeFailure, OSError, ValueError, KeyError) as error:
        report["status"] = "failed"
        report["error"] = str(error)
    report["durationsSeconds"]["total"] = round(time.monotonic() - started, 3)
    report["receipt"] = str(root / "receipt.json")
    (root / "receipt.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, separators=(",", ":")))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
