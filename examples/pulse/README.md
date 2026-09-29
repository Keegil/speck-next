# Pulse — historical example

Pulse is an energy-journal CLI built while developing an earlier Speck Next method in August 2026. Its product, decisions, state and work files are preserved examples of that period. Their terminology and workflow are not current v7 instructions.

The historical record reports repaired defects but leaves post-fix independent acceptance open. Its `Built` labels and `nothing blocked` line do not establish current acceptance. See [the original state](state.md). The example has not been requalified as evidence for a later method release.

## Try the basic journal

From the repository root, use Python 3 on macOS or Linux and a disposable journal:

```sh
pulse_demo=$(mktemp -d)
PULSE_FILE="$pulse_demo/journal.json" python3 examples/pulse/pulse.py 4
PULSE_FILE="$pulse_demo/journal.json" python3 examples/pulse/pulse.py
```

These commands log and display an entry without touching the default `~/.pulse.json`. `python3 examples/pulse/pulse.py --help` shows the other arguments.

The optional `innsikt` path calls the local `ollama` command with `normistral:latest` when it detects a pattern. That model setup and its quality are separate from the basic journal demonstration and are not verified by a normal Speck Next release check.
