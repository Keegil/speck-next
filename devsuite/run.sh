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
[ ${#TASKS[@]} -eq 0 ] && TASKS=(small-change bug-hunt honest-state review-integrity separated-product-team)
mkdir -p "$RUNS"

pass=0; fail=0
for task in "${TASKS[@]}"; do
  unset GIT_DIR GIT_WORK_TREE SPECK_DEVSUITE_ROLE_DRIVER SPECK_DEVSUITE_ROLE_ADAPTER
  T="$SUITE/tasks/$task"
  CLONE="$RUNS/$task"
  git clone -q "$REPO" "$CLONE"
  if [ "$UNGOVERNED" = 1 ]; then
    rm -f "$CLONE/AGENTS.md" "$CLONE/CLAUDE.md" && rm -rf "$CLONE/.claude"
  fi
  if [ "$CONTROL" = 1 ]; then
    bash "$T/setup.sh" "$CLONE" --control || { echo "FAIL  $task (planting failed — a task on an unplanted repo proves nothing)"; fail=$((fail+1)); continue; }
  else
    bash "$T/setup.sh" "$CLONE" || { echo "FAIL  $task (planting failed — a task on an unplanted repo proves nothing)"; fail=$((fail+1)); continue; }
    PROMPT="$(cat "$T/prompt.txt")"
    if [ "$task" = "separated-product-team" ]; then
      # Git metadata is normally protected by workspace-write. This is a
      # disposable clone, so keep the sandbox and move only its metadata to a
      # regular writable directory inside that clone.
      mkdir -p "$CLONE/.git/info"
      printf '\n.devsuite-git/\n.devsuite-role-runs/\n.driver.log\n.driver.events.jsonl\n.driver.stderr.log\n' >> "$CLONE/.git/info/exclude"
      mv "$CLONE/.git" "$CLONE/.devsuite-git"
      export GIT_DIR="$CLONE/.devsuite-git"
      export GIT_WORK_TREE="$CLONE"
      export SPECK_DEVSUITE_ROLE_DRIVER="$DRIVER"
      export SPECK_DEVSUITE_ROLE_ADAPTER="$CLONE/devsuite/tasks/separated-product-team/role-adapter.py"
      if [ "$UNGOVERNED" = 0 ]; then
        PROMPT="$PROMPT

This governed fixture exposes a task-only role launcher at \`$SPECK_DEVSUITE_ROLE_ADAPTER\`. Decide from the installed method whether separate roles are required. If they are, Product creates \`.devsuite-role-runs/\`, writes a distinct evidence brief there for each role, and elects to invoke \`python3 \$SPECK_DEVSUITE_ROLE_ADAPTER ROLE .devsuite-role-runs/ROLE-brief.md\` once per role. Use each returned child session id as that role's carrier, read its returned contribution before synthesis, and cite the returned contribution path in that role's Direct evidence cell. The launcher captures host evidence; it does not choose roles or conclusions for you."
      fi
    fi
    # stdin closed (an open pipe once hung a session for 79 minutes waiting on it),
    # and every task bounded: a driver that exceeds the deadline is killed and scored by its checks.
    DEADLINE="${DEVSUITE_TASK_TIMEOUT:-1500}"
    if [ "$task" = "separated-product-team" ]; then
      # This task needs host-issued dispatch evidence. The runner only captures
      # structured events; the governed agent must decide to summon the roles.
      case "$DRIVER" in
        codex)  codex exec --json --sandbox workspace-write --skip-git-repo-check -C "$CLONE" -o "$CLONE/.driver.log" "$PROMPT" < /dev/null > "$CLONE/.driver.events.jsonl" 2> "$CLONE/.driver.stderr.log" & DPID=$! ;;
        claude) (cd "$CLONE" && claude -p "$PROMPT" --allowedTools "Bash,Read,Write,Edit,Glob,Grep,Agent" --output-format stream-json --verbose < /dev/null > "$CLONE/.driver.events.jsonl" 2> "$CLONE/.driver.stderr.log") & DPID=$! ;;
        *) echo "unknown driver: $DRIVER"; exit 2 ;;
      esac
    else
      case "$DRIVER" in
        codex)  codex exec --sandbox workspace-write -C "$CLONE" "$PROMPT" < /dev/null > "$CLONE/.driver.log" 2>&1 & DPID=$! ;;
        claude) (cd "$CLONE" && claude -p "$PROMPT" --allowedTools "Bash,Read,Write,Edit,Glob,Grep" < /dev/null > "$CLONE/.driver.log" 2>&1) & DPID=$! ;;
        *) echo "unknown driver: $DRIVER"; exit 2 ;;
      esac
    fi
    SECONDS_WAITED=0
    while kill -0 "$DPID" 2>/dev/null; do
      sleep 5; SECONDS_WAITED=$((SECONDS_WAITED+5))
      if [ "$SECONDS_WAITED" -ge "$DEADLINE" ]; then
        echo "  [timeout] $task driver exceeded ${DEADLINE}s — killed" ; kill "$DPID" 2>/dev/null; sleep 2; kill -9 "$DPID" 2>/dev/null
        break
      fi
    done
    wait "$DPID" 2>/dev/null
  fi
  if python3 "$T/check.py" "$CLONE"; then
    echo "PASS  $task"; pass=$((pass+1))
  else
    echo "FAIL  $task"; fail=$((fail+1))
  fi
  unset GIT_DIR GIT_WORK_TREE SPECK_DEVSUITE_ROLE_DRIVER SPECK_DEVSUITE_ROLE_ADAPTER
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
