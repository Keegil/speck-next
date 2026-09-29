#!/usr/bin/env python3
"""Positive/negative controls on disposable copies of the release surface."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

KERNEL = Path(__file__).resolve().parents[1]
CHECKER = KERNEL / "devsuite/surface-check.py"


class SurfaceControls(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="speck-surface-control-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for relative in ("package.json", "README.md", "AGENTS.md", "CLAUDE.md", "bin", ".claude/skills", "templates", ".agents"):
            source, destination = KERNEL / relative, self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination, symlinks=True)
            else:
                shutil.copy2(source, destination)

    def run_check(self):
        return subprocess.run(["python3", "-B", str(CHECKER), str(self.root)], text=True,
                              capture_output=True, timeout=40)

    def passes(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS release surface", result.stdout)

    def rejected_edit(self, relative, change, diagnostic):
        path = self.root / relative
        original = path.read_bytes()
        path.write_bytes(change(original))
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(diagnostic, result.stdout)
        path.write_bytes(original)
        self.passes()

    def test_current_source_copy_passes(self):
        self.passes()

    def test_stale_readme_version_and_pins(self):
        self.rejected_edit("README.md", lambda b: re.sub(rb"Current version:.*", b"Current version: **0.0.0**", b), "Current version")
        self.rejected_edit("README.md", lambda b: re.sub(rb"speck-next#v[\d.]+ install", b"speck-next#v0.0.0 install", b), "command pins 0.0.0")

    def test_stale_cli_help_pin(self):
        self.rejected_edit("bin/speck-next.js", lambda b: b.replace(b"#v${VERSION} install", b"#v0.0.0 install"), "CLI help: command pins 0.0.0")

    def test_broken_or_unshipped_link(self):
        self.rejected_edit("AGENTS.md", lambda b: b + b"\n[missing](missing-reference.md)\n", "does not resolve to a shipped path")
        (self.root / "source-only.md").write_text("This source file is deliberately outside the installed surface.\n")
        self.rejected_edit("AGENTS.md", lambda b: b + b"\n[source only](source-only.md)\n", "does not resolve to a shipped path")

    def test_skill_metadata(self):
        relative = ".claude/skills/shape-product/SKILL.md"
        self.rejected_edit(relative, lambda b: b.replace(b"name: shape-product", b"name: judge"), "duplicate skill name")
        self.rejected_edit(relative, lambda b: re.sub(rb"description:.*", b"description:", b, count=1), "one-line string fields")
        self.rejected_edit(relative, lambda b: re.sub(rb"description:.*", b"description:   ", b, count=1), "nonempty string")
        self.rejected_edit(relative, lambda b: b.replace(b"description:", b"description: |\n  multiline", 1), "general YAML is unsupported")
        self.rejected_edit(relative, lambda b: re.sub(rb"description:.*", b"description: " + b"x" * 1025, b, count=1), "description exceeds 1024")

    def test_file_and_size_limits(self):
        extra = self.root / "templates/unplanned.md"
        extra.write_text("An extra installed file must count.\n")
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exceeds 20", result.stdout)
        extra.unlink()
        self.passes()
        self.rejected_edit("AGENTS.md", lambda b: b + b"x" * 100000, "exceeds 100000")

    def test_skill_count_uses_actual_directories(self):
        # Two extra skills exceed the six-skill ceiling, regardless of other
        # simultaneous footprint errors; no advertised prose count is consulted.
        for name in ("extra-one", "extra-two"):
            folder = self.root / ".claude/skills" / name
            folder.mkdir()
            (folder / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Control fixture.\n---\n")
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("canonical skill count 7", result.stdout)

    def test_host_imports(self):
        self.rejected_edit("CLAUDE.md", lambda b: b.replace(b"AGENTS.md", b"missing.md"), "CLAUDE.md must import")
        discovery = self.root / ".agents/skills/speck-next"
        discovery.unlink()
        discovery.symlink_to("../../templates")
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("discovery symlink", result.stdout)
        discovery.unlink()
        discovery.symlink_to("../../.claude/skills")
        self.passes()

    def test_external_links_code_and_template_fields_are_not_local_paths(self):
        path = self.root / "templates/piece.md"
        with path.open("a") as output:
            output.write("\n[Optional field]\n[web](https://example.invalid/no-network)\n")
            output.write("[email](mailto:example@example.invalid)\n[local anchor](#example)\n")
            output.write("`[literal](missing.md)`\n```md\n[example](missing.md)\n```\n")
            output.write("[later]({project-path}/result.md)\n")
            output.write("[real](../AGENTS.md)\n[ref]: ../AGENTS.md\n")
        self.passes()


if __name__ == "__main__":
    unittest.main(verbosity=2)
