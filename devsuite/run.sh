#!/usr/bin/env bash
# Dev suite: measures the kernel on tiny scored tasks. Usage:
#   ./devsuite/run.sh               run all tasks with a live agent (DEVSUITE_DRIVER=codex|claude)
#   ./devsuite/run.sh --control     no agent; every task's KEY check must go RED (proves checks can fail)
#   ./devsuite/run.sh --ungoverned  strip AGENTS.md/CLAUDE.md/.claude from the clone first (control arm)
#   ./devsuite/run.sh bug-hunt      run one task
#
# Honest measurement note: live drivers also carry the owner's global agent
# instructions (~/.claude, ~/.codex), which themselves teach evidence honesty.
# A green run therefore proves the full real stack behaves — it does not isolate
# this kernel's contribution. The --ungoverned arm removes the repo layer only.
set -u
cd "$(dirname "$0")/.."
REPO="$(pwd)"
SUITE="$REPO/devsuite"
RUNS="${DEVSUITE_RUNS:-/tmp/claude-501/devsuite-runs}/run-$(date +%s)"
DRIVER="${DEVSUITE_DRIVER:-codex}"
CONTROL=0
UNGOVERNED=0
TASKS=()
for arg in "$@"; do
  case "$arg" in
    --control) CONTROL=1 ;;
    --ungoverned) UNGOVERNED=1 ;;
    *) TASKS+=("$arg") ;;
  esac
done
[ ${#TASKS[@]} -eq 0 ] && TASKS=(small-change bug-hunt honest-state review-integrity)
mkdir -p "$RUNS"

pass=0; fail=0
for task in "${TASKS[@]}"; do
  T="$SUITE/tasks/$task"
  CLONE="$RUNS/$task"
  git clone -q "$REPO" "$CLONE"
  if [ "$UNGOVERNED" = 1 ]; then
    rm -f "$CLONE/AGENTS.md" "$CLONE/CLAUDE.md" && rm -rf "$CLONE/.claude"
  fi
  if [ "$CONTROL" = 1 ]; then
    bash "$T/setup.sh" "$CLONE" --control
  else
    bash "$T/setup.sh" "$CLONE"
    PROMPT="$(cat "$T/prompt.txt")"
    case "$DRIVER" in
      codex)  codex exec --sandbox workspace-write -C "$CLONE" "$PROMPT" > "$CLONE/.driver.log" 2>&1 ;;
      claude) (cd "$CLONE" && claude -p "$PROMPT" --allowedTools "Bash,Read,Write,Edit,Glob,Grep" > "$CLONE/.driver.log" 2>&1) ;;
      *) echo "unknown driver: $DRIVER"; exit 2 ;;
    esac
  fi
  if python3 "$T/check.py" "$CLONE"; then
    echo "PASS  $task"; pass=$((pass+1))
  else
    echo "FAIL  $task"; fail=$((fail+1))
  fi
done
echo "----"
if [ "$CONTROL" = 1 ]; then
  # in control mode red is the desired outcome: it proves the checks can fail
  echo "control mode: $fail of $((pass+fail)) tasks went red (want: all)"
  [ "$pass" = 0 ] && exit 0 || exit 1
else
  echo "$pass of $((pass+fail)) tasks passed  (runs kept in $RUNS)"
  [ "$fail" = 0 ] && exit 0 || exit 1
fi
