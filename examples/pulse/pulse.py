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
    try:
        with open(DATA) as f:
            entries = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
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


WEEKDAYS = ["", "mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"]


def _spread(day_value_pairs):
    per_day = {}
    for wd, v in day_value_pairs:
        per_day.setdefault(wd, []).append(v)
    avgs = {wd: sum(vs) / len(vs) for wd, vs in per_day.items() if len(vs) >= 2}
    if len(avgs) < 2:
        return None, None, 0.0
    lo, hi = min(avgs, key=avgs.get), max(avgs, key=avgs.get)
    return lo, hi, avgs[hi] - avgs[lo]


def weekday_pattern(entries):
    # the machine does the counting; the model only gets to phrase what is true.
    # a pattern counts only if it beats chance: the real weekday spread must exceed
    # the 95th percentile of 200 shuffles of the same values over the same days.
    import random
    pairs = [(date.fromisoformat(d).isoweekday(), v) for d, v in sorted(entries.items())]
    lo, hi, real = _spread(pairs)
    if lo is None or real < 1.0:
        return None
    rng = random.Random(0)
    values = [v for _, v in pairs]
    beaten = 0
    for _ in range(200):
        rng.shuffle(values)
        _, _, s = _spread([(wd, v) for (wd, _), v in zip(pairs, values)])
        if real > s:
            beaten += 1
    if beaten < 190:  # not clearly better than chance
        return None
    per_day = {}
    for wd, v in pairs:
        per_day.setdefault(wd, []).append(v)
    lo_avg = sum(per_day[lo]) / len(per_day[lo])
    hi_avg = sum(per_day[hi]) / len(per_day[hi])
    return (f"{WEEKDAYS[lo]}ene ligger på {lo_avg:.1f} i snitt, "
            f"{WEEKDAYS[hi]}ene på {hi_avg:.1f} ({len(per_day[lo])} uker logget)")


def innsikt():
    entries = load()
    if len(entries) < 5:
        print("Innsikt trenger minst fem loggede dager. Logg litt til, så ses vi.")
        return
    fact = weekday_pattern(entries)
    if fact is None:
        print("Ingen tydelige gjentakende mønstre i loggen ennå. Fortsett å logge, så ser vi.")
        return
    prompt = (
        "Si dette videre til en venn, varmt og tørt, på norsk: først observasjonen i maks to setninger, "
        "så ett vennlig spørsmål eller lite eksperiment i maks to setninger. Svar direkte, ikke gjenta "
        "denne oppgaven, ingen utropstegn, ingen andre tall eller dager enn i observasjonen.\n\n"
        f"Observasjonen: {fact}\n"
    )
    print("tenker – dette kan ta et minutt ...")
    import subprocess as sp
    try:
        r = sp.run(["ollama", "run", "--think=false", "normistral:latest", prompt], capture_output=True, text=True, timeout=180)
    except (OSError, sp.TimeoutExpired):
        r = None
    import re
    text = re.sub(r"<think>.*?</think>", "", r.stdout, flags=re.S).strip() if r and r.returncode == 0 else ""
    text = re.sub(r"\*+", "", text)  # terminal, not markdown
    low = text.lower()
    # every weekday and every number in the output must exist in the computed fact — nothing invented
    weekdays_ok = any(WEEKDAYS[wd] in low for wd in range(1, 8)) and all(
        WEEKDAYS[wd] not in low or WEEKDAYS[wd] in fact for wd in range(1, 8))
    fact_numbers = set(re.findall(r"\d+(?:[.,]\d+)?", fact.replace(",", ".")))
    numbers_ok = all(n in fact_numbers for n in re.findall(r"\d+(?:[.,]\d+)?", low.replace(",", ".")))
    banned = ("optimaliser", "din reise", "reisen din", "ai-drevet", "angst", "depresjon", "deprimert", "utbrent")
    clean = not any(w in low for w in banned) and not any(ord(ch) >= 0x2190 for ch in text)
    echoed = any(w in low for w in ("oppgaven", "observasjonen:", "maks to setninger", "«"))
    if not text or not weekdays_ok or not numbers_ok or not clean or echoed or "?" not in text or "!" in text or len(text) > 600:
        if text:
            with open(DATA + ".rejected", "w") as f:  # kept for debugging; never shown to the user
                f.write(text)
        # the computed truth, plainly — real data, never canned
        print()
        print(f"{fact[0].upper()}{fact[1:]}.")
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
