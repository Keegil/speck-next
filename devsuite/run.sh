#!/usr/bin/env bash
# Dev suite: measures the kernel on tiny scored tasks. Usage:
#   ./devsuite/run.sh               run all tasks with a live agent (DEVSUITE_DRIVER=codex|claude)
#   ./devsuite/run.sh --control     no agent; every task's KEY check must go RED (proves checks can fail)
#   ./devsuite/run.sh --ungoverned  strip AGENTS.md/CLAUDE.md/.claude from the clone first (control arm)
#   ./devsuite/run.sh --probe NAME separated-product-team  run one isolated Piece 9 admission probe
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
MODEL="${DEVSUITE_MODEL:-}"
EFFORT="${DEVSUITE_EFFORT:-high}"
CONTROL=0
UNGOVERNED=0
PROBE=""
TASKS=()
ACTIVE_DRIVER_PID=""; ACTIVE_BROKER_STATE=""; ACTIVE_BROKER_TOOL=""; ACTIVE_TEMP_HOME=""
cleanup_role_home() {
  if [ -n "$ACTIVE_DRIVER_PID" ]; then kill "$ACTIVE_DRIVER_PID" 2>/dev/null || true; wait "$ACTIVE_DRIVER_PID" 2>/dev/null || true; fi
  if [ -n "$ACTIVE_BROKER_STATE" ] && [ -f "$ACTIVE_BROKER_STATE" ] && [ -n "$ACTIVE_BROKER_TOOL" ]; then
    python3 "$ACTIVE_BROKER_TOOL" cleanup "$ACTIVE_BROKER_STATE" >/dev/null 2>&1 || true
  fi
  if [ -n "$ACTIVE_TEMP_HOME" ] && [ -d "$ACTIVE_TEMP_HOME" ]; then
    case "$ACTIVE_TEMP_HOME" in /tmp/speck-piece9-baseline-home.*|/private/tmp/speck-piece9-baseline-home.*) trash "$ACTIVE_TEMP_HOME" >/dev/null 2>&1 || true ;; esac
  fi
  ACTIVE_DRIVER_PID=""; ACTIVE_BROKER_STATE=""; ACTIVE_BROKER_TOOL=""; ACTIVE_TEMP_HOME=""
}
trap cleanup_role_home EXIT
trap 'cleanup_role_home; exit 130' INT TERM
while [ $# -gt 0 ]; do
  case "$1" in
    --control) CONTROL=1 ;;
    --ungoverned) UNGOVERNED=1 ;;
    --probe) shift; [ $# -gt 0 ] || { echo "--probe requires contributions, product, business, or engineering" >&2; exit 2; }; PROBE="$1" ;;
    *) TASKS+=("$1") ;;
  esac
  shift
done
[ ${#TASKS[@]} -eq 0 ] && TASKS=(small-change bug-hunt honest-state review-integrity separated-product-team)
if [ -n "$PROBE" ] && { [ ${#TASKS[@]} -ne 1 ] || [ "${TASKS[0]}" != "separated-product-team" ] || [ "$CONTROL" = 1 ] || [ "$UNGOVERNED" = 1 ]; }; then
  echo "--probe runs one governed separated-product-team task" >&2; exit 2
fi
if [ -z "$MODEL" ]; then
  case "$DRIVER" in codex) MODEL="gpt-5.6-sol" ;; claude) MODEL="claude-sonnet-4-6" ;; esac
fi
mkdir -p "$RUNS"

pass=0; fail=0
for task in "${TASKS[@]}"; do
  unset GIT_DIR GIT_WORK_TREE SPECK_DEVSUITE_ROLE_DRIVER SPECK_DEVSUITE_BROKER_STATE
  BROKER_CONTROL=""
  T="$SUITE/tasks/$task"
  CLONE="$RUNS/$task"
  git clone -q "$REPO" "$CLONE"
  if [ "$UNGOVERNED" = 1 ]; then
    [ ! -e "$CLONE/AGENTS.md" ] || trash "$CLONE/AGENTS.md"
    [ ! -e "$CLONE/CLAUDE.md" ] || trash "$CLONE/CLAUDE.md"
    [ ! -e "$CLONE/.claude" ] || trash "$CLONE/.claude"
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
      printf '\n.devsuite-git/\n.devsuite-role-ipc/\n.driver.log\n.driver.events.jsonl\n.driver.stderr.log\n.driver.metrics.json\n' >> "$CLONE/.git/info/exclude"
      mv "$CLONE/.git" "$CLONE/.devsuite-git"
      export GIT_DIR="$CLONE/.devsuite-git"
      export GIT_WORK_TREE="$CLONE"
      export SPECK_DEVSUITE_ROLE_DRIVER="$DRIVER"
      if [ "$UNGOVERNED" = 0 ]; then
        BROKER_CONTROL="$(mktemp -d "$RUNS/.piece9-controller.XXXXXX")"
      fi
    fi
    # stdin closed (an open pipe once hung a session for 79 minutes waiting on it),
    # and every task bounded: a driver that exceeds the deadline is killed and scored by its checks.
    DEADLINE="${DEVSUITE_TASK_TIMEOUT:-1500}"
    if [ "$task" = "separated-product-team" ] && [ "$DEADLINE" -gt 900 ]; then DEADLINE=900; fi
    if [ "$task" = "separated-product-team" ]; then
      if [ "$UNGOVERNED" = 0 ]; then
        MODE="full"; [ -n "$PROBE" ] && MODE="probe:$PROBE"
        ADMISSION_ROOT="${DEVSUITE_ADMISSION_DIR:-${DEVSUITE_RUNS:-/tmp/claude-501/devsuite-runs}/piece9-admission}"
        ACTIVE_BROKER_STATE="$BROKER_CONTROL/state.json"
        ACTIVE_BROKER_TOOL="$T/role-broker.py"
        python3 "$T/role-broker.py" controller "$CLONE" "$BROKER_CONTROL" "$MODE" "$DRIVER" "$MODEL" "$EFFORT" "$ADMISSION_ROOT" "$T/prompt.txt" "$REPO" > "$CLONE/.driver.log" 2> "$CLONE/.driver.stderr.log" & DPID=$!
      else
        case "$DRIVER" in
          codex)
            ACTIVE_TEMP_HOME="$(mktemp -d /tmp/speck-piece9-baseline-home.XXXXXX)"
            cp "$HOME/.codex/auth.json" "$ACTIVE_TEMP_HOME/auth.json"
            CODEX_HOME="$ACTIVE_TEMP_HOME" codex exec --json --sandbox workspace-write --skip-git-repo-check --ignore-user-config -m "$MODEL" -c "model_reasoning_effort=\"$EFFORT\"" -c features.multi_agent=false -C "$CLONE" -o "$CLONE/.driver.log" "$PROMPT" < /dev/null > "$CLONE/.driver.events.jsonl" 2> "$CLONE/.driver.stderr.log" & DPID=$! ;;
          claude) (cd "$CLONE" && claude -p "$PROMPT" --output-format stream-json --verbose --model "$MODEL" --effort "$EFFORT" --setting-sources user --tools "Bash,Read,Write,Edit" < /dev/null > "$CLONE/.driver.events.jsonl" 2> "$CLONE/.driver.stderr.log") & DPID=$! ;;
          *) echo "unknown driver: $DRIVER"; exit 2 ;;
        esac
      fi
    else
      case "$DRIVER" in
        codex)  codex exec --sandbox workspace-write -C "$CLONE" "$PROMPT" < /dev/null > "$CLONE/.driver.log" 2>&1 & DPID=$! ;;
        claude) (cd "$CLONE" && claude -p "$PROMPT" --allowedTools "Bash,Read,Write,Edit,Glob,Grep" < /dev/null > "$CLONE/.driver.log" 2>&1) & DPID=$! ;;
        *) echo "unknown driver: $DRIVER"; exit 2 ;;
      esac
    fi
    ACTIVE_DRIVER_PID="$DPID"
    SECONDS_WAITED=0
    TOKEN_LIMIT=250000
    BUDGET_STOP=0
    while kill -0 "$DPID" 2>/dev/null; do
      sleep 5; SECONDS_WAITED=$((SECONDS_WAITED+5))
      if [ "$task" = "separated-product-team" ]; then
        STATE_ARG="-"; [ -n "$BROKER_CONTROL" ] && STATE_ARG="$BROKER_CONTROL/state.json"
        DRIVER_TOKENS="$(python3 "$T/host_proof.py" metrics "$DRIVER" "$CLONE" "$CLONE/.driver.events.jsonl" "$STATE_ARG" 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tokens",0))' 2>/dev/null || echo 0)"
        if [ "${DRIVER_TOKENS:-0}" -ge "$TOKEN_LIMIT" ]; then
          echo "  [budget] $task reached ${DRIVER_TOKENS} aggregate host-reported tokens (limit: ${TOKEN_LIMIT}) — killed"
          BUDGET_STOP=1; kill "$DPID" 2>/dev/null
          sleep 2; kill -9 "$DPID" 2>/dev/null
          break
        fi
      fi
      if [ "$SECONDS_WAITED" -ge "$DEADLINE" ]; then
        echo "  [timeout] $task driver exceeded ${DEADLINE}s — killed" ; kill "$DPID" 2>/dev/null; sleep 2; kill -9 "$DPID" 2>/dev/null
        break
      fi
    done
    wait "$DPID" 2>/dev/null; DRIVER_RC=$?
    ACTIVE_DRIVER_PID=""
    if [ "$task" = "separated-product-team" ]; then
      STATE_ARG="-"; [ -n "$BROKER_CONTROL" ] && STATE_ARG="$BROKER_CONTROL/state.json"
      python3 "$T/host_proof.py" metrics "$DRIVER" "$CLONE" "$CLONE/.driver.events.jsonl" "$STATE_ARG" "$SECONDS_WAITED" "$TOKEN_LIMIT" > "$CLONE/.driver.metrics.json"
      echo "  [measure] separated-product-team elapsed=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("elapsed_seconds",0))' "$CLONE/.driver.metrics.json")s tokens=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("tokens",0))' "$CLONE/.driver.metrics.json") limit=${TOKEN_LIMIT}"
    fi
  fi
  if [ -n "$BROKER_CONTROL" ]; then export SPECK_DEVSUITE_BROKER_STATE="$BROKER_CONTROL/state.json"; fi
  if [ -n "$PROBE" ] && [ "$task" = "separated-product-team" ]; then
    if [ "$DRIVER_RC" = 0 ]; then echo "PASS  $task probe:$PROBE"; pass=$((pass+1)); else echo "FAIL  $task probe:$PROBE"; fail=$((fail+1)); fi
  elif python3 "$T/check.py" "$CLONE"; then
    echo "PASS  $task"; pass=$((pass+1))
  else
    echo "FAIL  $task"; fail=$((fail+1))
  fi
  cleanup_role_home
  unset GIT_DIR GIT_WORK_TREE SPECK_DEVSUITE_ROLE_DRIVER SPECK_DEVSUITE_BROKER_STATE
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
