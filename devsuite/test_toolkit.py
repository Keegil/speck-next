#!/usr/bin/env python3
"""Managed toolkit controls: local HTTP fixtures, no model or internet calls."""
import functools
import hashlib
import http.server
import io
import json
import os
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

    def cli(self, *args, env=None, options=None):
        self.manifest_file.write_text(json.dumps(self.manifest))
        return subprocess.run(["node", "-e", RUN, str(MODULE), str(self.manifest_file), json.dumps(args),
                               json.dumps({"platform": "linux-x64", **(options or {})})],
                              env=dict(os.environ, SPECK_NEXT_TOOL_HOME=str(self.home), **(env or {})),
                              capture_output=True, text=True, timeout=20)

    def success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def tree(self, directory=None):
        directory = directory or self.home
        return {str(p.relative_to(directory)): p.read_bytes() for p in directory.rglob("*") if p.is_file() and not p.is_symlink()}

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
