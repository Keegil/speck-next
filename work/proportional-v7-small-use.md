# Small-project method-use evidence

Context: fresh implementation context `/root/small_use`, not a contributor to the Speck Next candidate. No kernel work files or conclusions read. No external agents, network, or git push used.

Installed method source SHA supplied by coordinator: `fa1ead74e0f3a413709f8bf3bbb72ea5a3d4496d`.

Installed method digest supplied by coordinator: `b13f6e10f4069b641dccb2f38f3bf73a82d23a224c6ab11d4091905b37742b96`.

Subject: `/tmp/speck-v7/small-project` (physical path `/private/tmp/speck-v7/small-project`). Fixture HEAD: `d70be5b6161517653d2b751353f81a5c70d704a0`.

## Request and actions

Built the requested dependency-free Python CSV summary tool. Read the installed `AGENTS.md` and the supplied `readings.csv`, created only `readings.py` inside the subject, then executed it and tested its terminal errors. Used Python standard-library `argparse`, `csv`, and `decimal`.

No planning or product records were needed: this is a single script, the requirements and input were sufficient, and there are no cross-piece dependencies or ongoing work to resume. No clarification, permission request, or methodology stall occurred. No installed skill was needed for this straightforward terminal task. Implementation and checks finished within the five-minute budget.

## Normal command and actual output

```text
$ python3 readings.py
Readings: 3
Total kWh: 10.00
Average kWh: 3.33
```

```text
$ python3 readings.py --help
usage: readings.py [-h] [path]

Summarize the kwh column of a CSV file.

positional arguments:
  path        CSV file (default: readings.csv)

options:
  -h, --help  show this help message and exit
```

## Executed checks

Ran a Python subprocess assertion harness using temporary CSVs created inside the subject and removed automatically afterward. Every case invoked `python3 /private/tmp/speck-v7/small-project/readings.py <path>`. Checked process exit status and output destination as well as the expected content. Seven cases passed:

| Case | Input | Observed result |
| --- | --- | --- |
| Optional CSV path | Two readings, 1.20 and 2.40 | Exit 0; 2 readings, total 3.60, average 1.80 |
| Missing column | `date,usage` header | Exit 2; stderr says `missing required column: kwh` |
| Invalid number | `nope` | Exit 2; stderr says `line 2: invalid kwh number 'nope'` |
| Blank number | Empty kwh cell | Exit 2; stderr says `line 2: invalid kwh number ''` |
| Nonfinite number | `NaN` | Exit 2; stderr says `line 2: invalid kwh number 'NaN'` |
| Header only | `date,kwh` with no data rows | Exit 0; 0 readings, total 0.00, average 0.00 |
| Missing file | Nonexistent path | Exit 2; stderr names path and says `file not found` |

All failing cases produced no stdout. The temporary harness did not create a permanent test suite.

## Result and limits

Created `readings.py`; SHA-256 `a6793f610ac8920a077af76383bcaab51e24bddfc30bf785669ceb097fb1ea10`. Final `git status --short` showed only `?? readings.py`.

Run it with `python3 readings.py` or `python3 readings.py /path/to/file.csv`. The only required column is `kwh`; unrelated columns, including the sample's date column, are ignored. A header-only CSV reports the explicit zero-readings convention shown above. This is a simple local CLI, with no packaging or installation step. It remains unreviewed: the coordinator's separate independent reviewer is the next consumer of this implementation and evidence. No claim of independent acceptance is made.
