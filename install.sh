#!/usr/bin/env bash
# Install the Speck Next method surface into a fresh product repository.
# Usage: bash install.sh /path/to/target-repo
set -eu
SRC="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:?usage: install.sh <target-repo>}"
[ -d "$TARGET" ] || { echo "no such directory: $TARGET"; exit 1; }
TARGET="$(cd "$TARGET" && pwd)"
[ -d "$TARGET/.git" ] || { echo "not a git repository: $TARGET (git init first)"; exit 1; }
[ "$TARGET" = "$SRC" ] && { echo "refusing: that's the kernel repo itself"; exit 1; }
if [ -e "$TARGET/AGENTS.md" ] || [ -e "$TARGET/CLAUDE.md" ] || [ -e "$TARGET/.claude/skills" ]; then
  echo "refusing: $TARGET already carries agent instructions — this installer is for fresh repos only."
  echo "Upgrading an existing Speck repo is a later version's job; nothing was touched."
  exit 1
fi
cp "$SRC/AGENTS.md" "$TARGET/AGENTS.md"
cp "$SRC/CLAUDE.md" "$TARGET/CLAUDE.md"
mkdir -p "$TARGET/.claude"
cp -R "$SRC/.claude/skills" "$TARGET/.claude/skills"
files=$(find "$TARGET/AGENTS.md" "$TARGET/CLAUDE.md" "$TARGET/.claude/skills" -type f | wc -l | tr -d ' ')
bytes=$(find "$TARGET/AGENTS.md" "$TARGET/CLAUDE.md" "$TARGET/.claude/skills" -type f -exec cat {} + | wc -c | tr -d ' ')
echo "Installed the Speck Next method surface into $TARGET: $files files, $bytes bytes."
echo "Next: open an agent session there and say what you want to build — shaping starts in that conversation."
