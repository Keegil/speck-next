# Piece 9 pre-code blind product test

**Receipt:** [work/separated-product-team.md](separated-product-team.md), “Pre-code blind product receipt,” committed at `ee9f5b2` before dispatch.

**Tester:** first-time Pulse user · Codex collaboration context `/root/result_blind_tester` · inherited current model · 2026-09-05.

**Boundary:** The tester worked only in a neutral temporary directory containing `PROMISE.md`, `A/pulse.py`, and `B/pulse.py`. It did not inspect either implementation, provenance, git history, role record, Speck repository, or source directory. It chose before Product revealed the assignment.

## Run record

The tester read the product promise: show the recent journal at a glance, gaps and all; never invent or lose data; keep missing days calm facts; honesty outranks polish.

The mixed journal contained `2026-08-30: 1`, `2026-09-01: 3`, and `2026-09-05: 5`. The complete journal contained one value on every day from 2026-08-30 through 2026-09-05. The empty journal was `{}`.

### Help

```sh
python3 A/pulse.py --help
python3 B/pulse.py --help
```

A returned:

```text
usage: pulse [1-5] | pulse | pulse week | pulse innsikt | pulse --date YYYY-MM-DD [1-5|week]
```

B returned:

```text
usage: pulse [1-5] | pulse | pulse week | pulse innsikt | pulse --date YYYY-MM-DD [1-5]
```

### Mixed seven-day journal

```sh
HOME="$PWD/fixtures/mixed" python3 "$PWD/A/pulse.py" --date 2026-09-05 week
HOME="$PWD/fixtures/mixed" python3 "$PWD/B/pulse.py" --date 2026-09-05 week
```

A exited zero:

```text
Siste sju dager
søn 30. aug  1
man 31. aug  ikke logget
tir 1. sep  3
ons 2. sep  ikke logget
tor 3. sep  ikke logget
fre 4. sep  ikke logget
lør 5. sep  5
```

B exited one:

```text
pulse: energy is a whole number from 1 (drained) to 5 (flying). Nothing logged.
```

The tester could verify A's bounds, three values, and four gaps in one glance. B treated a requested view as an invalid logging attempt and showed no journal.

### Complete seven-day journal

The same commands against the complete fixture made A list all seven exact dates and values. B again exited one with the same logging error. A was quick to scan vertically; B never reached the viewing job.

### Empty journal

The same commands against `{}` made A return:

```text
Nothing logged yet. Start with: pulse 3
```

B again returned the logging error. The tester found A calm and actionable; B's energy-value correction was confusing because the request was to view a week.

### Existing fourteen-day view

```sh
HOME="$PWD/fixtures/mixed" python3 "$PWD/A/pulse.py"
HOME="$PWD/fixtures/mixed" python3 "$PWD/B/pulse.py"
HOME="$PWD/fixtures/mixed" python3 "$PWD/A/pulse.py" --date 2026-09-05
HOME="$PWD/fixtures/mixed" python3 "$PWD/B/pulse.py" --date 2026-09-05
```

All four runs returned the same output:

```text
       ▁ ▄   █
smtwtfssmtwtfs
3 of 14 days logged. Gaps are days you skipped — they stay gaps.
```

The old dense view remained fastest for the rough energy shape but did not let a first-time user verify exact boundary dates. A introduced no visible regression.

### Data integrity

SHA-256 hashes for all three journal files and their lock files were identical before and after every A and B run. Neither product changed a fixture byte.

## Blind verdict

**Selection locked before provenance: A.**

A worked for every tested job: exact dates, trustworthy gaps, calm empty state, and unchanged legacy behavior. B's legacy view worked, but its fixed-date week command failed for mixed, complete, and empty journals. The tester would keep A.

The difference was materially large enough that an expensive separated product-team method could plausibly have earned its cost. It was not cosmetic: the core historical-week scenario moved from exit one to a complete auditable week without regressing the old surface. This test does not establish that the method was necessary or cheapest, only that the resulting difference is material.

The deal-breaker was B rejecting `--date 2026-09-05 week` and offering an irrelevant logging correction. A's remaining rough edge was language inconsistency—Norwegian week output versus English help, default, and empty state—but it did not break comprehension or trust in these runs.

## Unblinding

After the selection and verdict were final, Product revealed the assignment kept outside the tester's environment:

- A SHA-256 `4a0d1450676614bf7b32f6eb3722062f586bdcc8e4391277e025125b50046394` = governed separated-team product commit `f439c81`.
- B SHA-256 `20863fd2c43b868ee32680da30000a877bbc98b10696522818748e863edded88` = ungoverned strong-control product commit `014deef`.

The result supports material product difference. It does not change any historical cost verdict or authorize another Pulse build.
