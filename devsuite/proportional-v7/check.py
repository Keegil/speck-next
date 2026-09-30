#!/usr/bin/env python3
"""Focused v7 install/upgrade checks. No models, dependencies, or historical role gates.

Run: python3 devsuite/proportional-v7/check.py
"""
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tarfile
import tempfile
import unittest

KERNEL = Path(__file__).resolve().parents[2]
VERSION = json.loads((KERNEL / "package.json").read_text())["version"]
MAJOR, MINOR, PATCH = map(int, VERSION.split("."))
FUTURE_PATCH = f"{MAJOR}.{MINOR}.{PATCH + 1}"
FUTURE_MINOR = f"{MAJOR}.{MINOR + 1}.0"
FUTURE_MAJOR = f"{MAJOR + 1}.0.0"


def run(*args, cwd=None, env=None):
    return subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, timeout=60)


def snapshot(root):
    """Observe bytes, modes, and links without following aliases or changing Git."""
    result = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        info = path.lstat()
        if path.is_symlink():
            result[relative] = ("link", os.readlink(path), stat.S_IMODE(info.st_mode))
        elif path.is_file():
            result[relative] = ("file", path.read_bytes(), stat.S_IMODE(info.st_mode))
        else:
            result[relative] = ("dir", stat.S_IMODE(info.st_mode))
    return result


class UpgradeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="speck-v7-")
        cls.base = Path(cls.temporary.name)
        packed = run("npm", "pack", "--json", "--pack-destination", str(cls.base), cwd=KERNEL)
        if packed.returncode:
            raise AssertionError(packed.stderr)
        archive = cls.base / json.loads(packed.stdout)[0]["filename"]
        with tarfile.open(archive) as package:
            package.extractall(cls.base / "packed", filter="data")
        cls.packed = cls.base / "packed/package"
        cls.sequence = 0

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def repo(self, version=None, product=None):
        type(self).sequence += 1
        root = self.base / f"subject-{self.sequence}"
        root.mkdir()
        self.assertEqual(run("git", "init", "-q", str(root)).returncode, 0)
        if version is not None:
            (root / ".claude").mkdir()
            self.write_marker(root, {"name": "speck-next", "version": version})
        if product is not None:
            (root / "product.md").write_bytes(product)
        return root

    def write_marker(self, root, value):
        (root / ".claude/speck-next.json").write_text(json.dumps(value) + "\n")

    def cli(self, command, root, *extra, kernel=KERNEL, env=None):
        return run("node", str(kernel / "bin/speck-next.js"), command, str(root), *extra, env=env)

    def succeeds(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")

    def stable_retry(self, root, kernel=KERNEL):
        before = snapshot(root)
        self.succeeds(self.cli("upgrade", root, kernel=kernel))
        self.assertEqual(snapshot(root), before)

    def refuses_untouched(self, root, *extra):
        before = snapshot(root)
        result = self.cli("upgrade", root, *extra)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("refusing", result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(snapshot(root), before)
        return result

    def test_source_and_packed_fresh_install(self):
        source_surface = source_digest = None
        for kernel in (KERNEL, self.packed):
            with self.subTest(kernel=str(kernel)):
                root = self.repo()
                result = self.cli("install", root, kernel=kernel)
                self.succeeds(result)
                self.assertFalse((root / "map.md").exists())
                self.assertFalse((root / "product.md").exists())
                self.assertNotIn("shaping starts", result.stdout)
                self.assertEqual((root / "AGENTS.md").read_bytes(), (kernel / "AGENTS.md").read_bytes())
                self.assertEqual((root / ".agents/skills/speck-next").resolve(), (root / ".claude/skills").resolve())
                marker = json.loads((root / ".claude/speck-next.json").read_text())
                self.assertEqual(marker["version"], VERSION)
                self.assertIsNone(marker["upgradeAssessmentRecord"])
                # Compare the complete installed result, not just AGENTS.md.
                # Package filters must not silently omit a skill, reference or
                # template. Marker timestamps/provenance legitimately differ.
                installed_surface = {
                    path: value for path, value in snapshot(root).items()
                    if path.split("/")[0] != ".git" and path != ".claude/speck-next.json"
                }
                if kernel == KERNEL:
                    source_surface = installed_surface
                    source_digest = marker["methodSurfaceSha256"]
                else:
                    self.assertEqual(installed_surface, source_surface)
                    self.assertEqual(marker["methodSurfaceSha256"], source_digest)
                self.stable_retry(root, kernel)

    def test_supported_versions_preserve_pending_or_missing_product(self):
        pending = b"# Product\r\n## Speck Next upgrade assessment\r\n**Speck Next upgrade assessment:** pending\r\n**Record:** `work/product-team-assessment.md`\r\n"
        malformed = b"# Owner bytes\r\n<!-- unclosed historical assessment\n\xff\x00"
        stale = b"## Speck Next upgrade assessment\n**Speck Next upgrade assessment:** complete \xe2\x80\x94 resumed STALE-PIECE from state.md\n"
        for version in dict.fromkeys(("1.0.0", "2.0.0", "3.2.0", "4.0.0", "5.4.1", "6.0.0-rc.1", "6.0.0-rc.2", "6.0.0", "7.0.0", "7.0.1", "7.0.2", "7.0.3", "7.0.4", VERSION)):
            for product in (None, pending, malformed, stale):
                with self.subTest(version=version, product=product):
                    root = self.repo(version, product)
                    (root / "state.md").write_bytes(b"# State\nOPEN: fix lost writes. Current request overrides old order.\n")
                    self.write_marker(root, {"version": version, "upgradeAssessmentRecord": {"historical": "malformed"}})
                    result = self.cli("upgrade", root)
                    self.succeeds(result)
                    self.assertFalse((root / "map.md").exists())
                    self.assertEqual((root / "product.md").read_bytes() if product is not None else None, product)
                    self.assertEqual((root / "product.md").exists(), product is not None)
                    next_line = [line for line in result.stdout.splitlines() if line.startswith("Next:")][0]
                    self.assertIn("current state.md", next_line)
                    self.assertNotIn("STALE-PIECE", next_line)
                    self.assertFalse((root / "work/product-team-assessment.md").exists())
                    self.stable_retry(root)

    def test_source_and_packed_toolkit_available_without_setup(self):
        for kernel in (KERNEL, self.packed):
            with self.subTest(kernel=str(kernel)):
                cache = self.repo() / "absent tool cache"
                env = dict(os.environ, SPECK_NEXT_TOOL_HOME=str(cache))
                cli = str(kernel / "bin/speck-next.js")
                result = run("node", cli, "tools", "doctor", "--json", env=env)
                self.assertEqual(result.returncode, 1, result.stderr)
                report = json.loads(result.stdout)
                self.assertFalse(report["ready"])
                self.assertEqual({tool["name"] for tool in report["tools"]},
                                 {"graft", "rg", "jq", "ast-grep", "rtk"})
                self.assertFalse(cache.exists())
                for name in ("toolkit.js", "toolkit-manifest.json"):
                    self.assertEqual((kernel / "bin" / name).read_bytes(),
                                     (KERNEL / "bin" / name).read_bytes())

    def test_packed_upgrade_preserves_dirty_owner_records(self):
        root = self.repo("5.4.1", b"# Product\nAn unresolved promise.\n")
        records = {"map.md": b"# Map\nLive owner work\n", "state.md": b"OPEN: issue 9\n", "decisions.md": b"Do not change pricing\n", "work/piece.md": b"Finding remains open\n", ".claude/settings.json": b'{"owner":true}\n', "unrelated.bin": b"\xff\x00\r\n"}
        for relative, data in records.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.assertEqual(run("git", "add", ".", cwd=root).returncode, 0)
        self.assertEqual(run("git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "owner baseline", cwd=root).returncode, 0)
        (root / "product.md").write_bytes(b"# Dirty product\r\nNo reassessment authorized.\r\n")
        records["product.md"] = (root / "product.md").read_bytes()
        records["state.md"] += b"Uncommitted owner steering\n"
        (root / "state.md").write_bytes(records["state.md"])
        index = (root / ".git/index").read_bytes()
        self.succeeds(self.cli("upgrade", root, kernel=self.packed))
        self.assertEqual((root / ".git/index").read_bytes(), index)
        for relative, data in records.items():
            self.assertEqual((root / relative).read_bytes(), data, relative)
        self.stable_retry(root, self.packed)

    def test_unknown_future_and_malformed_markers_refuse(self):
        markers = [None, [], "not an object", {}, {"version": 7}, {"name": "other", "version": VERSION}]
        markers += [{"version": value} for value in ("0.9.0", "banana", "7", "07.0.0", FUTURE_PATCH, FUTURE_MINOR, FUTURE_MAJOR, "999999999999999999999.0.0")]
        for value in markers:
            with self.subTest(marker=value):
                root = self.repo("6.0.0")
                self.write_marker(root, value)
                self.refuses_untouched(root)
        root = self.repo("6.0.0")
        (root / ".claude/speck-next.json").write_text("{broken")
        self.refuses_untouched(root)

    def test_retired_flag_and_nonmarker_repo_refuse(self):
        root = self.repo("6.0.0", b"# Product\n")
        result = self.refuses_untouched(root, "--open-assessment")
        self.assertIn("retired", result.stderr)
        self.refuses_untouched(self.repo())

    def test_existing_map_directory_is_owner_data(self):
        root = self.repo("5.4.1")
        (root / "map.md").mkdir()
        (root / "map.md/owner.txt").write_bytes(b"Preserve even unusual owner layout")
        before = snapshot(root / "map.md")
        self.succeeds(self.cli("upgrade", root))
        self.assertEqual(snapshot(root / "map.md"), before)

    def test_external_method_link_is_localized_without_external_write(self):
        root = self.repo("6.0.0")
        outside = self.base / f"outside-{self.sequence}"
        outside.mkdir()
        (outside / "owner.md").write_bytes(b"external owner material\n")
        (root / "templates").symlink_to(outside, target_is_directory=True)
        before = snapshot(outside)
        self.succeeds(self.cli("upgrade", root))
        self.assertEqual(snapshot(outside), before)
        self.assertFalse((root / "templates").is_symlink())
        self.assertEqual((root / "templates/owner.md").read_bytes(), b"external owner material\n")

    def test_linked_git_index_refuses_before_writes(self):
        root = self.repo("6.0.0")
        (root / ".git/index").symlink_to(self.base / "missing-index")
        self.refuses_untouched(root)

    def test_owner_record_aliases_into_method_refuse(self):
        for relative in ("product.md", "state.md", "decisions.md", "work/finding.md"):
            with self.subTest(relative=relative):
                root = self.repo("6.0.0")
                (root / "templates").mkdir()
                (root / "templates/product.md").write_bytes(b"An unresolved owner finding\n")
                record = root / relative
                record.parent.mkdir(parents=True, exist_ok=True)
                record.symlink_to(root / "templates/product.md")
                result = self.refuses_untouched(root)
                self.assertIn("owner record", result.stderr)

    def test_late_git_report_failure_rolls_back_every_byte(self):
        root = self.repo("5.4.1", b"owner product\n")
        wrappers = self.base / "git-wrapper"
        wrappers.mkdir(exist_ok=True)
        wrapper = wrappers / "git"
        real_git = shutil.which("git")
        wrapper.write_text('#!/bin/sh\nfor arg in "$@"; do\n  if [ "$arg" = "diff" ]; then exit 73; fi\ndone\nexec "' + real_git + '" "$@"\n')
        wrapper.chmod(0o755)
        before = snapshot(root)
        result = self.cli("upgrade", root, env=dict(os.environ, PATH=str(wrappers) + os.pathsep + os.environ["PATH"]))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("rolled", result.stderr)
        self.assertEqual(snapshot(root), before)
        self.assertEqual(list(root.parent.glob(f".{root.name}.speck-next-transaction-*")), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
