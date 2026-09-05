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
ACTIVE_DRIVER_PID=""; ACTIVE_BROKER_PID=""; ACTIVE_BROKER_STATE=""; ACTIVE_BROKER_TOOL=""
cleanup_role_home() {
  if [ -n "$ACTIVE_DRIVER_PID" ]; then kill "$ACTIVE_DRIVER_PID" 2>/dev/null || true; wait "$ACTIVE_DRIVER_PID" 2>/dev/null || true; fi
  if [ -n "$ACTIVE_BROKER_PID" ]; then kill "$ACTIVE_BROKER_PID" 2>/dev/null || true; wait "$ACTIVE_BROKER_PID" 2>/dev/null || true; fi
  if [ -n "$ACTIVE_BROKER_STATE" ] && [ -f "$ACTIVE_BROKER_STATE" ] && [ -n "$ACTIVE_BROKER_TOOL" ]; then
    python3 "$ACTIVE_BROKER_TOOL" cleanup "$ACTIVE_BROKER_STATE" >/dev/null 2>&1 || true
  fi
  ACTIVE_DRIVER_PID=""; ACTIVE_BROKER_PID=""; ACTIVE_BROKER_STATE=""; ACTIVE_BROKER_TOOL=""
}
trap cleanup_role_home EXIT
trap 'cleanup_role_home; exit 130' INT TERM
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
  unset GIT_DIR GIT_WORK_TREE SPECK_DEVSUITE_ROLE_DRIVER SPECK_DEVSUITE_BROKER_STATE
  BROKER_PID=""; BROKER_CONTROL=""
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
      printf '\n.devsuite-git/\n.devsuite-role-ipc/\n.driver.log\n.driver.events.jsonl\n.driver.stderr.log\n.driver.metrics.json\n' >> "$CLONE/.git/info/exclude"
      mv "$CLONE/.git" "$CLONE/.devsuite-git"
      export GIT_DIR="$CLONE/.devsuite-git"
      export GIT_WORK_TREE="$CLONE"
      export SPECK_DEVSUITE_ROLE_DRIVER="$DRIVER"
      if [ "$UNGOVERNED" = 0 ]; then
        if [ "$DRIVER" = "codex" ]; then
          BROKER_CONTROL="$(mktemp -d "$RUNS/.role-broker.XXXXXX")"
          python3 "$T/role-broker.py" serve "$CLONE" "$BROKER_CONTROL" > "$BROKER_CONTROL/broker.log" 2> "$BROKER_CONTROL/broker.stderr.log" & BROKER_PID=$!
          BROKER_READY=0
          for _ in 1 2 3 4 5 6 7 8 9 10; do
            if [ -f "$BROKER_CONTROL/state.json" ] && python3 -c 'import json,sys; raise SystemExit(0 if json.load(open(sys.argv[1])).get("startup_phase") == "ready" else 1)' "$BROKER_CONTROL/state.json" 2>/dev/null; then BROKER_READY=1; break; fi
            sleep 0.2
          done
          ACTIVE_BROKER_PID="$BROKER_PID"; ACTIVE_BROKER_STATE="$BROKER_CONTROL/state.json"; ACTIVE_BROKER_TOOL="$T/role-broker.py"
          if [ "$BROKER_READY" != 1 ]; then
            echo "FAIL  $task (role broker failed before credential-safe state existed)"; fail=$((fail+1)); cleanup_role_home; continue
          fi
          PROMPT="$PROMPT

This governed fixture ends after working behavior and the active roles' first-run returns. Do not open Experience testing, judgment, or review. Use exactly one Business, one Experience, and one Engineering context; never retry, fall back, or create another context.

This task's files and method are the complete context; do not load optional skills or investigate the harness. Before model work, record its 250,000-token aggregate estimate and this hard authorization: four host contexts total (Product plus the same Business, Experience, and Engineering carriers), 900 elapsed seconds, zero retries, zero fallbacks, zero owner interruptions, and no more than 300 seconds or 30 files read before the first product run. Exhaustion forbids another model turn. Gross, cached, and fresh tokens are measured Business cost evidence; crossing the estimate is a cost finding, not a product verdict. You elect each context through synchronous file IPC. Write all three initial request JSON files before waiting for any response. Each is shaped {\"role\":\"Business\",\"stage\":\"contribution\",\"brief\":\"at least 80 characters naming direct product evidence and the bounded question\"} at \`.devsuite-role-ipc/requests/business-contribution.json\`, with equivalent Experience and Engineering files. Wait once for all three matching response files. The runner transports your exact briefs to fresh host contexts and returns each host-issued \`carrier\` and verbatim \`contribution\`; it chooses neither. Record the returned carriers and use the contributions. Do not invoke Codex or another agent from the shell.

Commit the Product synthesis before code. Then request \`engineering-implement.json\` with role Engineering, stage implement, and the committed handoff in brief; the same Engineering carrier owns code. After its smallest mixed-gap CLI run, write all three return requests before one wait: \`business-return.json\`, \`experience-return.json\`, and \`engineering-return.json\`, each with stage return and the observed output in its brief. Record what changed or held, Business's binding ruling with evidence, and all contributor exclusions. Then stop immediately."
        else
          PROMPT="$PROMPT

This governed fixture ends after working behavior and the active roles' first-run returns. Before model work, record its 250,000-token aggregate estimate and this hard authorization: four host contexts total (Product plus the same Business, Experience, and Engineering carriers), 900 elapsed seconds, zero retries, zero fallbacks, zero owner interruptions, and no more than 300 seconds or 30 files read before the first product run. Exhaustion forbids another model turn. Gross, cached, and fresh tokens are measured Business cost evidence; crossing the estimate is a cost finding, not a product verdict. Use exactly three native Agent contexts named pulse-business, pulse-experience, and pulse-engineering; never retry or duplicate one. Record each host-issued Agent result \`agentId\` as its carrier. Product commits synthesis before code, the same Engineering agent implements, and the same three agents return to the smallest mixed-gap CLI run. Record what changed or held, Business's binding ruling with evidence, and all exclusions, then stop. Do not open Experience testing, judgment, or review."
        fi
      fi
    fi
    # stdin closed (an open pipe once hung a session for 79 minutes waiting on it),
    # and every task bounded: a driver that exceeds the deadline is killed and scored by its checks.
    DEADLINE="${DEVSUITE_TASK_TIMEOUT:-1500}"
    if [ "$task" = "separated-product-team" ] && [ "$DEADLINE" -gt 900 ]; then DEADLINE=900; fi
    if [ "$task" = "separated-product-team" ]; then
      # This task needs host-issued dispatch evidence. The runner only captures
      # structured events; the governed agent must decide to summon the roles.
      case "$DRIVER" in
        codex)
          if [ -n "$BROKER_CONTROL" ]; then
            ROOT_CODEX_HOME="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["root_home"])' "$BROKER_CONTROL/state.json")"
            CODEX_HOME="$ROOT_CODEX_HOME" codex exec --json --sandbox workspace-write --skip-git-repo-check --ignore-user-config -C "$CLONE" -o "$CLONE/.driver.log" "$PROMPT" < /dev/null > "$CLONE/.driver.events.jsonl" 2> "$CLONE/.driver.stderr.log" & DPID=$!
          else
            codex exec --json --sandbox workspace-write --skip-git-repo-check -C "$CLONE" -o "$CLONE/.driver.log" "$PROMPT" < /dev/null > "$CLONE/.driver.events.jsonl" 2> "$CLONE/.driver.stderr.log" & DPID=$!
          fi ;;
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
    ACTIVE_DRIVER_PID="$DPID"
    SECONDS_WAITED=0
    TOKEN_ESTIMATE=250000
    while kill -0 "$DPID" 2>/dev/null; do
      sleep 5; SECONDS_WAITED=$((SECONDS_WAITED+5))
      if [ "$task" = "separated-product-team" ]; then
        if [ "$DRIVER" = "codex" ] && [ -n "$BROKER_PID" ] && ! kill -0 "$BROKER_PID" 2>/dev/null; then
          echo "  [broker] separated role transport stopped before Product completed — killed"
          kill "$DPID" 2>/dev/null; break
        fi
      fi
      if [ "$SECONDS_WAITED" -ge "$DEADLINE" ]; then
        echo "  [timeout] $task driver exceeded ${DEADLINE}s — killed" ; kill "$DPID" 2>/dev/null; sleep 2; kill -9 "$DPID" 2>/dev/null
        [ -n "$BROKER_PID" ] && kill "$BROKER_PID" 2>/dev/null
        break
      fi
    done
    wait "$DPID" 2>/dev/null
    ACTIVE_DRIVER_PID=""
    if [ -n "$BROKER_CONTROL" ]; then
      touch "$BROKER_CONTROL/stop"
      wait "$BROKER_PID" 2>/dev/null
    fi
    if [ "$task" = "separated-product-team" ]; then
      STATE_ARG="-"; [ -n "$BROKER_CONTROL" ] && STATE_ARG="$BROKER_CONTROL/state.json"
      python3 "$T/host_proof.py" metrics "$DRIVER" "$CLONE" "$CLONE/.driver.events.jsonl" "$STATE_ARG" "$SECONDS_WAITED" "$TOKEN_ESTIMATE" > "$CLONE/.driver.metrics.json"
      TOKEN_REPORT="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); u=d.get("token_usage",{}); print(f"gross={u.get('"'"'gross'"'"',d.get('"'"'tokens'"'"',0))} cached={u.get('"'"'cached'"'"',0)} fresh={u.get('"'"'fresh'"'"',d.get('"'"'tokens'"'"',0))}")' "$CLONE/.driver.metrics.json")"
      echo "  [measure] separated-product-team elapsed=${SECONDS_WAITED}s ${TOKEN_REPORT} gross-estimate=${TOKEN_ESTIMATE}"
    fi
  fi
  if [ -n "$BROKER_CONTROL" ]; then export SPECK_DEVSUITE_BROKER_STATE="$BROKER_CONTROL/state.json"; fi
  if python3 "$T/check.py" "$CLONE"; then
    echo "PASS  $task"; pass=$((pass+1))
  else
    echo "FAIL  $task"; fail=$((fail+1))
  fi
  if [ -n "$BROKER_CONTROL" ] && [ -f "$BROKER_CONTROL/state.json" ]; then
    python3 "$T/role-broker.py" cleanup "$BROKER_CONTROL/state.json" || echo "  [RED] broker credential-home cleanup failed"
  fi
  ACTIVE_DRIVER_PID=""; ACTIVE_BROKER_PID=""; ACTIVE_BROKER_STATE=""; ACTIVE_BROKER_TOOL=""
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
