#!/usr/bin/env python3
"""Pulse — a one-command energy journal. `pulse 4` logs today; `pulse` shows two weeks."""
import fcntl, json, os, sys, tempfile
from datetime import date, timedelta

DATA = os.path.realpath(os.environ.get("PULSE_FILE", os.path.expanduser("~/.pulse.json")))
BLOCKS = {1: "▁", 2: "▂", 3: "▄", 4: "▆", 5: "█"}
USAGE = "usage: pulse [1-5] | pulse | pulse --date YYYY-MM-DD [1-5]"
BAD_JOURNAL = f"pulse: {DATA} doesn't look like a pulse journal — not touching it."


def load():
    if not os.path.exists(DATA):
        return {}
    with open(DATA) as f:
        try:
            entries = json.load(f)
        except json.JSONDecodeError:
            raise SystemExit(BAD_JOURNAL)
    if not isinstance(entries, dict):
        raise SystemExit(BAD_JOURNAL)
    for day, value in entries.items():
        try:
            date.fromisoformat(day)
        except ValueError:
            raise SystemExit(BAD_JOURNAL)
        if type(value) is not int or value not in BLOCKS:  # bools and floats are not energy
            raise SystemExit(BAD_JOURNAL)
    return entries


def save(entries):
    # write-then-rename so a crash mid-write can't eat the journal
    d = os.path.dirname(DATA) or "."
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".pulse-")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(entries, f, indent=0, sort_keys=True)
        os.replace(tmp, DATA)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def log(value, day):
    if value not in BLOCKS:
        raise SystemExit("pulse: energy is a whole number from 1 (drained) to 5 (flying). Nothing logged.")
    # one writer at a time, so two overlapping runs can't lose a logged day
    with open(DATA + ".lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        entries = load()
        entries[day.isoformat()] = value
        save(entries)
    note = " (that's in the future — it'll show once the chart reaches it)" if day > date.today() else ""
    print(f"Logged {value} for {day.isoformat()}.{note}")


def view(today):
    entries = load()
    if not entries:
        print("Nothing logged yet. Start with:  pulse 3")
        return
    days = [today - timedelta(days=i) for i in range(13, -1, -1)]
    row = "".join(BLOCKS[entries[d.isoformat()]] if d.isoformat() in entries else " " for d in days)
    labels = "".join("M T W T F S S"[d.weekday() * 2] for d in days)
    logged = [d for d in days if d.isoformat() in entries]
    print(row)
    print(labels.lower())
    print(f"{len(logged)} of 14 days logged. Gaps are days you skipped — they stay gaps.")


def main(argv):
    if len(argv) > 1 and argv[1] in ("--help", "-h", "help"):
        print(USAGE)
        return
    day = date.today()
    if len(argv) > 2 and argv[1] == "--date":  # for logging past days
        try:
            day = date.fromisoformat(argv[2])
        except ValueError:
            raise SystemExit(f"pulse: '{argv[2]}' isn't a date I understand — use YYYY-MM-DD. Nothing logged.")
        argv = [argv[0]] + argv[3:]
    if len(argv) == 1:
        view(day)
    elif len(argv) == 2:
        try:
            value = int(argv[1])
        except ValueError:
            raise SystemExit("pulse: energy is a whole number from 1 (drained) to 5 (flying). Nothing logged.")
        log(value, day)
    else:
        raise SystemExit(USAGE)


if __name__ == "__main__":
    main(sys.argv)
