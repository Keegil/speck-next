#!/usr/bin/env python3
"""Pulse — a one-command energy journal. `pulse 4` logs today; `pulse` shows two weeks."""
import fcntl, json, os, sys, tempfile
from datetime import date, timedelta

DATA = os.path.realpath(os.environ.get("PULSE_FILE", os.path.expanduser("~/.pulse.json")))
BLOCKS = {1: "▁", 2: "▂", 3: "▄", 4: "▆", 5: "█"}
USAGE = "usage: pulse [1-5] | pulse | pulse innsikt | pulse --date YYYY-MM-DD [1-5]"
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


def innsikt():
    entries = load()
    if len(entries) < 5:
        print("Innsikt trenger minst fem loggede dager. Logg litt til, så ses vi.")
        return
    days = ", ".join(f"{['','man','tir','ons','tor','fre','lør','søn'][date.fromisoformat(d).isoweekday()]} {d[8:]}.{int(d[5:7])}: {v}" for d, v in sorted(entries.items()))
    prompt = (
        "Energilogg, 1=tom 5=full. Svar på norsk, to korte avsnitt: "
        "1) én observasjon (maks to setninger) om et mønster som GJENTAR seg over flere uker "
        "(for eksempel samme ukedag lav eller høy uke etter uke) — nevn ukedagene og verdiene. "
        "2) ett vennlig spørsmål eller lite eksperiment (maks to setninger). "
        "Ingen utropstegn, ingen diagnoser, ingen råd uten data. Finnes ikke noe gjentakende mønster: si det ærlig.\n\n"
        f"Logg: {days}\n"
    )
    print("tenker – dette kan ta noen minutter ...")
    import subprocess as sp
    try:
        r = sp.run(["ollama", "run", "normistral:latest", prompt], capture_output=True, text=True, timeout=300)
    except (FileNotFoundError, sp.TimeoutExpired):
        print("pulse: fikk ikke kontakt med modellen (ollama). Ingen innsikt i dag.")
        return
    import re
    text = re.sub(r"<think>.*?</think>", "", r.stdout, flags=re.S).strip()
    if r.returncode != 0 or not text:
        print("pulse: fikk ikke svar fra modellen. Ingen innsikt i dag.")
        return
    # the observation must trace to real logged values: at least one real date, weekday or value from the journal
    real_bits = set()
    for d in entries:
        dt = date.fromisoformat(d)
        real_bits.add(d)
        real_bits.add(["", "mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"][dt.isoweekday()])
    grounded = any(bit in text.lower() for bit in real_bits)
    if not grounded or "!" in text or len(text) > 700:
        print("pulse: fikk ikke noe fornuftig ut av dette i dag. Prøv igjen i morgen.")
        return
    print()
    print(text)


def main(argv):
    if len(argv) > 1 and argv[1] in ("--help", "-h", "help"):
        print(USAGE)
        return
    if len(argv) == 2 and argv[1] == "innsikt":
        innsikt()
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
