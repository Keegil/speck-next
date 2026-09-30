#!/usr/bin/env python3
"""Managed toolkit controls: local HTTP fixtures, no model or internet calls."""
import functools
import hashlib
import http.server
import io
import json
import os
import signal
import time
from pathlib import Path
import subprocess
import tarfile
import tempfile
import threading
import unittest

MODULE = Path(__file__).resolve().parents[1] / "bin/toolkit.js"
RUN = "require(process.argv[1]).main(JSON.parse(process.argv[3]),{manifest:JSON.parse(require('fs').readFileSync(process.argv[2])),allowHttp:true,...JSON.parse(process.argv[4])}).then(c=>process.exitCode=c)"
SCRIPT = b'#!/bin/sh\nif [ "$1" = "--version" ]; then echo "fixture 1.2.3"; exit 0; fi\necho "stdout:$*"\necho "stderr:$*" >&2\nif [ "$1" = "fail" ]; then exit 23; fi\n'


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class ToolkitTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="speck toolkit ")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.home = self.root / "managed tools"
        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(self.root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.url = f"http://127.0.0.1:{self.server.server_port}"
        self.manifest = {"schemaVersion": 1, "tools": {"rg": self.artifact()}}
        self.manifest_file = self.root / "manifest.json"

    def artifact(self, data=SCRIPT, format="executable", binary="fixture"):
        (self.root / "artifact").write_bytes(data)
        return {"kind": "archive", "version": "1.2.3", "executable": "rg", "platforms": {
            "linux-x64": {"url": self.url + "/artifact", "sha256": hashlib.sha256(data).hexdigest(), "format": format, "binary": binary}}}

    def cli(self, *args, env=None, options=None, background=False):
        self.manifest_file.write_text(json.dumps(self.manifest))
        invoke = subprocess.Popen if background else subprocess.run
        kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE} if background else {"capture_output": True, "timeout": 20}
        return invoke(["node", "-e", RUN, str(MODULE), str(self.manifest_file), json.dumps(args),
                               json.dumps({"platform": "linux-x64", **(options or {})})],
                              env=dict(os.environ, SPECK_NEXT_TOOL_HOME=str(self.home), **(env or {})),
                              text=True, **kwargs)

    def success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def tree(self, directory=None):
        directory = directory or self.home
        return {str(p.relative_to(directory)): p.read_bytes() for p in directory.rglob("*") if p.is_file() and not p.is_symlink()}

    def wait_for(self, predicate, seconds=10):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if predicate():
                return
            time.sleep(0.05)
        self.fail("Timed out waiting for fixture process")

    def test_failure_still_installs_remaining_tools(self):
        self.manifest["tools"]["bad"] = json.loads(json.dumps(self.manifest["tools"]["rg"]))
        self.manifest["tools"]["bad"]["platforms"]["linux-x64"]["sha256"] = "0" * 64
        self.manifest["tools"] = {"bad": self.manifest["tools"]["bad"], "rg": self.manifest["tools"]["rg"]}
        result = self.cli("setup")
        self.assertEqual(result.returncode, 1)
        self.assertIn("1 tool(s) failed", result.stderr)
        self.assertTrue((self.home / "rg/1.2.3/.speck-tool.json").exists())
        self.success(self.cli("run", "rg", "--", "--version"))

    def interrupted_setup(self, kill_signal, keep_child):
        self.success(self.cli("setup"))
        installed = (self.home / "rg/1.2.3/.speck-tool.json").read_bytes()
        block = self.root / "block"
        started = self.root / "started"
        block.touch()
        slow = b'#!/bin/sh\nif [ -f "$TEST_BLOCK" ]; then touch "$TEST_STARTED"; while [ -f "$TEST_BLOCK" ]; do sleep 0.1; done; fi\necho "fixture 1.2.3"\n'
        self.manifest["tools"]["jq"] = self.artifact(slow)
        child = self.cli("setup", background=True, env={"TEST_BLOCK": str(block), "TEST_STARTED": str(started)})
        self.addCleanup(lambda: child.poll() is None and child.kill())
        self.wait_for(started.exists)
        # A concurrent setup is refused while the parent owns the cache.
        result = self.cli("setup")
        self.assertEqual(result.returncode, 1)
        self.assertIn("busy", result.stderr)
        child.send_signal(kill_signal)
        child.wait(timeout=5)
        stage = next(self.home.glob(".stage-jq-*"))
        (stage / "witness.txt").write_bytes(b"preserve abandoned bytes")
        if keep_child:
            result = self.cli("setup")
            self.assertEqual(result.returncode, 1)
            self.assertIn("subprocess is still running", result.stderr)
            self.assertTrue(stage.exists())
        block.unlink()
        child.communicate(timeout=5)
        # Native descendants may take a moment to exit after termination.
        deadline = time.monotonic() + 10
        while True:
            result = self.cli("setup")
            if result.returncode == 0 or time.monotonic() > deadline:
                break
            self.assertIn("busy", result.stderr)
            time.sleep(0.1)
        self.success(result)
        self.assertEqual((self.home / "rg/1.2.3/.speck-tool.json").read_bytes(), installed)
        retired = list(self.root.glob("managed tools.retired-stage-*"))
        self.assertEqual(len(retired), 1)
        self.assertEqual((retired[0] / "witness.txt").read_bytes(), b"preserve abandoned bytes")
        self.success(self.cli("remove"))

    def test_sigint_setup_recovers_without_manual_cleanup(self):
        self.interrupted_setup(signal.SIGINT, False)

    def test_killed_parent_cannot_recover_while_child_runs(self):
        self.interrupted_setup(signal.SIGKILL, True)

    def test_unknown_staging_is_not_claimed(self):
        self.success(self.cli("setup"))
        stage = self.home / ".stage-graft-user"
        stage.mkdir()
        (stage / "owner.txt").write_bytes(b"keep")
        self.assertEqual(self.cli("setup").returncode, 1)
        self.assertEqual(self.cli("remove").returncode, 1)
        self.assertEqual((stage / "owner.txt").read_bytes(), b"keep")

    def test_setup_preflight_and_help_do_not_write(self):
        for options, message in (({"platform": "win32-x64"}, "unsupported"),
                                 ({"nodeVersion": "18.20.0"}, "Node >=20")):
            result = self.cli("setup", options=options)
            self.assertEqual(result.returncode, 1)
            self.assertIn(message, result.stderr)
            self.assertFalse(self.home.exists())
        self.success(self.cli("--help"))
        self.assertFalse(self.home.exists())

    def test_setup_idempotent_child_exit_and_output(self):
        self.success(self.cli("setup"))
        before = self.tree()
        self.success(self.cli("setup"))
        self.assertEqual(before, self.tree())
        result = self.cli("run", "rg", "--", "fail", "argument with spaces")
        self.assertEqual(result.returncode, 23)
        self.assertIn("stdout:fail argument with spaces", result.stdout)
        self.assertIn("stderr:fail argument with spaces", result.stderr)
        self.assertNotIn("Toolkit:", result.stderr)

    def test_doctor_missing_is_read_only_and_nonzero(self):
        result = self.cli("doctor", "--json")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)["ready"])
        self.assertFalse(self.home.exists())
        result = self.cli("run", "rg", "--", "anything")
        self.assertEqual(result.returncode, 1)
        self.assertIn("tools setup", result.stderr)
        self.assertFalse(self.home.exists())

    def test_integrity_failure_preserves_existing_version(self):
        self.success(self.cli("setup"))
        before = self.tree()
        self.manifest["tools"]["rg"]["version"] = "1.2.4"
        self.manifest["tools"]["rg"]["platforms"]["linux-x64"]["sha256"] = "0" * 64
        result = self.cli("setup")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Integrity check failed", result.stderr)
        self.assertEqual(before, self.tree())
        self.assertFalse(any(p.name.startswith(".stage") for p in self.home.iterdir()))

    def test_unowned_and_symlink_cache_refuse(self):
        self.home.mkdir()
        (self.home / "owner.txt").write_bytes(b"Keep this")
        before = self.tree()
        self.assertEqual(self.cli("setup").returncode, 1)
        self.assertEqual(self.cli("remove").returncode, 1)
        self.assertEqual(before, self.tree())
        self.home.rename(self.root / "owner data")
        self.home.symlink_to(self.root / "owner data", target_is_directory=True)
        result = self.cli("setup")
        self.assertEqual(result.returncode, 1)
        self.assertIn("symlink", result.stderr)
        self.assertEqual((self.root / "owner data/owner.txt").read_bytes(), b"Keep this")

    def test_incompatible_version_does_not_replace_existing_tool(self):
        self.success(self.cli("setup"))
        before = self.tree()
        self.manifest["tools"]["rg"]["version"] = "1.2.4"
        result = self.cli("setup")
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not report pinned version", result.stderr)
        self.assertEqual(before, self.tree())

    def test_archive_traversal_refuses_without_escape(self):
        contents = io.BytesIO()
        with tarfile.open(fileobj=contents, mode="w:gz") as archive:
            for name in ("fixture", "../escape"):
                info = tarfile.TarInfo(name)
                info.size = len(SCRIPT)
                archive.addfile(info, io.BytesIO(SCRIPT))
        self.manifest["tools"]["rg"] = self.artifact(contents.getvalue(), "tar.gz")
        result = self.cli("setup")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Unsafe archive member", result.stderr)
        self.assertFalse((self.root / "escape").exists())

    def test_archive_selected_binary_and_symlink_entry_refusal(self):
        contents = io.BytesIO()
        with tarfile.open(fileobj=contents, mode="w:gz") as archive:
            info = tarfile.TarInfo("folder/fixture")
            info.size = len(SCRIPT)
            archive.addfile(info, io.BytesIO(SCRIPT))
        self.manifest["tools"]["rg"] = self.artifact(contents.getvalue(), "tar.gz", "folder/fixture")
        self.success(self.cli("setup"))
        installed = self.home / "rg/1.2.3/tool"
        installed.unlink()
        installed.symlink_to(self.root / "artifact")
        result = self.cli("run", "rg", "--", "--version")
        self.assertEqual(result.returncode, 1)
        self.assertIn("symlink", result.stderr)

    def test_doctor_reports_external_without_adopting(self):
        external = self.root / "external bin"
        external.mkdir()
        (external / "rg").write_bytes(SCRIPT)
        (external / "rg").chmod(0o755)
        env = {"PATH": str(external) + os.pathsep + os.environ["PATH"]}
        result = self.cli("doctor", "--json", env=env)
        record = json.loads(result.stdout)["tools"][0]
        self.assertEqual(result.returncode, 1)
        self.assertTrue(record["existing"]["matches"])
        self.assertFalse(record["existing"]["adopted"])
        self.assertFalse(self.home.exists())

    def test_remove_retires_only_owned_cache(self):
        self.success(self.cli("setup"))
        (self.home / "owner.txt").write_bytes(b"Unexpected owner file")
        self.assertEqual(self.cli("remove").returncode, 1)
        self.assertEqual((self.home / "owner.txt").read_bytes(), b"Unexpected owner file")
        (self.home / "owner.txt").unlink()
        before = self.tree()
        self.success(self.cli("remove"))
        self.assertFalse(self.home.exists())
        retired = list(self.root.glob("managed tools.retired-*"))
        self.assertEqual(len(retired), 1)
        self.assertEqual(self.tree(retired[0]), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
