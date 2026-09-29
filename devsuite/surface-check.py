#!/usr/bin/env python3
"""Check the release surface using stdlib and the real Node installer.

Skill frontmatter deliberately supports flat, one-line string fields only, not
general YAML. Link checks cover inline links and reference definitions outside
fenced/inline code; they check shipped paths, not URL availability or anchors.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit


def command(args, cwd=None):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=30)
    if result.returncode:
        raise ValueError(f"{' '.join(map(str, args[:2]))} failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout


def frontmatter(path):
    lines = path.read_text().splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise ValueError("requires opening and closing --- frontmatter lines")
    values = {}
    for line in lines[1:lines[1:].index("---") + 1]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([a-z][a-z0-9_-]*):\s*(.+)", line)
        if not match:
            raise ValueError("supports flat, one-line string fields only; write name: ... and description: ...")
        key, value = match.groups()
        value = value.rstrip()
        if not value:
            raise ValueError(f"{key}: expected a nonempty string")
        if key in values:
            raise ValueError(f"duplicate frontmatter field {key}")
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except ValueError as error:
                raise ValueError(f"{key}: use a complete JSON-style quoted string") from error
        elif value.startswith("'"):
            if not re.fullmatch(r"'(?:[^']|'')*'", value):
                raise ValueError(f"{key}: invalid single-quoted string")
            value = value[1:-1].replace("''", "'")
        elif (value[0] in "|>{[&*!%@`" or ": " in value or " #" in value or
              value.lower() in {"null", "true", "false", "~"} or
              re.fullmatch(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", value)):
            raise ValueError(f"{key}: use a plain one-line string or quote it; general YAML is unsupported")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key}: expected a nonempty string")
        values[key] = value
    for required in ("name", "description"):
        if not values.get(required):
            raise ValueError(f"missing nonempty {required}")
    return values


def prose(text):
    """Remove code examples before inspecting links, keeping ordinary placeholders."""
    output, fence = [], None
    for line in text.splitlines():
        start = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
                fence = None
        elif start:
            fence = start.group(1)
        else:
            output.append(line)
    return re.sub(r"(`+)(.*?)\1", "", "\n".join(output), flags=re.S)


def link_targets(text):
    text = prose(text)
    destination = r"(?:<([^>\n]+)>|((?:\\.|[^\s()])+?(?:\((?:\\.|[^()])*\)(?:\\.|[^\s()])*)*))"
    for pattern in (r"!?\[[^\]\n]*\]\(\s*" + destination + r"(?:\s+[^\n]*?)?\)",
                    r"(?m)^ {0,3}\[[^\]\n]+\]:\s*" + destination + r"(?:\s|$)"):
        for match in re.finditer(pattern, text):
            yield match.group(1) or match.group(2)


def check(root):
    root = root.resolve()
    errors = []
    package = json.loads((root / "package.json").read_text())
    version = package["version"]
    readme = (root / "README.md").read_text()
    current = re.findall(r"(?im)^Current version:\s*(?:\*\*|`)?v?([0-9]+\.[0-9]+\.[0-9]+(?:-[\w.-]+)?)", readme)
    if current != [version]:
        errors.append(f"README.md: Current version must appear once and equal package.json {version}; found {current}")
    canonical = root / ".claude/skills"
    skill_files = sorted(canonical.rglob("SKILL.md"))
    names = set()
    for path in skill_files:
        label = path.relative_to(root)
        try:
            fields = frontmatter(path)
            name = fields["name"]
            if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name != path.parent.name:
                errors.append(f"{label}: name must match folder {path.parent.name!r} in lowercase hyphenated form, at most 64 characters")
            if len(fields["description"]) > 1024:
                errors.append(f"{label}: description exceeds 1024 characters")
            if name in names:
                errors.append(f"{label}: duplicate skill name {name!r}")
            names.add(name)
        except ValueError as error:
            errors.append(f"{label}: {error}")
    if not skill_files or len(skill_files) > 6:
        errors.append(f"canonical skill count {len(skill_files)} must be between 1 and 6")
    for folder in canonical.iterdir():
        if folder.is_dir() and not (folder / "SKILL.md").is_file():
            errors.append(f"{folder.relative_to(root)}: skill directory has no SKILL.md")
    if (root / "CLAUDE.md").read_text().strip() != "@AGENTS.md":
        errors.append("CLAUDE.md must import the canonical method with @AGENTS.md")
    discovery = root / ".agents/skills/speck-next"
    if not discovery.is_symlink() or discovery.resolve() != canonical.resolve():
        errors.append(".agents/skills/speck-next must be a discovery symlink to .claude/skills")

    # Install the actual SURFACE, including its generated marker. No parallel
    # manifest or estimated marker bytes can silently diverge from the CLI.
    with tempfile.TemporaryDirectory(prefix="speck-surface-") as temporary:
        installed = Path(temporary).resolve()
        command(["git", "init", "-q", str(installed)])
        command(["node", str(root / "bin/speck-next.js"), "install", str(installed)])
        files, links = [], []
        for base, directories, filenames in os.walk(installed, followlinks=False):
            directories[:] = [name for name in directories if name != ".git"]
            for name in directories + filenames:
                path = Path(base) / name
                if path.is_symlink():
                    links.append(path)
                elif path.is_file():
                    files.append(path)
        total = sum(path.stat().st_size for path in files)
        link_bytes = sum(len(os.readlink(path).encode()) for path in links)
        marker = installed / ".claude/speck-next.json"
        if marker not in files or json.loads(marker.read_text()).get("version") != version:
            errors.append("installed version marker must be a regular file matching package.json")
        if len(files) > 20:
            errors.append(f"installed regular files including marker: {len(files)} exceeds 20")
        if total + link_bytes > 100000:
            errors.append(f"installed bytes including link targets: {total + link_bytes} exceeds 100000")
        if len(list((installed / ".claude/skills").rglob("SKILL.md"))) != len(skill_files):
            errors.append("installed canonical skill count differs from source")
        installed_discovery = installed / ".agents/skills/speck-next"
        if not installed_discovery.is_symlink() or installed_discovery.resolve() != installed / ".claude/skills":
            errors.append("installed Codex discovery does not resolve to canonical skills")
        if (installed / "CLAUDE.md").read_text().strip() != "@AGENTS.md":
            errors.append("installed CLAUDE.md does not import AGENTS.md")
        texts = [("README.md", readme), ("CLI help", command(["node", str(root / "bin/speck-next.js"), "--help"]))]
        link_count = 0
        for path in files:
            if path.suffix != ".md":
                continue
            relative = path.relative_to(installed)
            text = path.read_text()
            texts.append((str(relative), text))
            for raw in link_targets(text):
                target = re.sub(r"\\([\\() ])", r"\1", raw)
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                # Explicit template substitutions are examples, not shipped paths.
                if re.search(r"\[[^]]+\]|\{[^}]+\}", parsed.path):
                    continue
                link_count += 1
                decoded = unquote(parsed.path)
                resolved = ((installed / decoded.lstrip("/")) if decoded.startswith("/") else path.parent / decoded).resolve()
                if not resolved.is_relative_to(installed) or not resolved.exists():
                    errors.append(f"{relative}: local link {raw!r} does not resolve to a shipped path")
        pin_pattern = r"github:Keegil/speck-next#v?([^\s`]+)\s+(?:install|upgrade)\b"
        for label, text in texts:
            for pinned in re.findall(pin_pattern, text):
                if pinned != version:
                    errors.append(f"{label}: command pins {pinned}, expected package.json {version}")
        metrics = (f"{sum(path != marker for path in files)} canonical regular files + marker = {len(files)}/20; "
                   f"{len(links)} discovery link(s) separate; {total + link_bytes}/100000 bytes; "
                   f"{len(skill_files)}/6 skills; {link_count} local links")
    return errors, metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        errors, metrics = check(args.root)
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        print(f"FAIL release surface: {error}")
        return 1
    print(f"Release surface: {metrics}")
    for error in errors:
        print(f"FAIL {error}")
    if not errors:
        print("PASS release surface")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
