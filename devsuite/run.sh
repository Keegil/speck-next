#!/usr/bin/env bash
# Dev suite: measures the kernel on tiny scored tasks. Usage:
#   ./devsuite/run.sh              run all tasks with a live agent (DEVSUITE_DRIVER=codex|claude)
#   ./devsuite/run.sh --control    no agent; every task's KEY check must go RED (proves checks can fail)
#   ./devsuite/run.sh bug-hunt     run one task
set -u
cd "$(dirname "$0")/.."
REPO="$(pwd)"
SUITE="$REPO/devsuite"
RUNS="${DEVSUITE_RUNS:-/tmp/claude-501/devsuite-runs}/run-$(date +%s)"
DRIVER="${DEVSUITE_DRIVER:-codex}"
CONTROL=0
TASKS=()
for arg in "$@"; do
  case "$arg" in
    --control) CONTROL=1 ;;
    *) TASKS+=("$arg") ;;
  esac
done
[ ${#TASKS[@]} -eq 0 ] && TASKS=(small-change bug-hunt honest-state)
mkdir -p "$RUNS"

pass=0; fail=0
for task in "${TASKS[@]}"; do
  T="$SUITE/tasks/$task"
  CLONE="$RUNS/$task"
  git clone -q "$REPO" "$CLONE"
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
