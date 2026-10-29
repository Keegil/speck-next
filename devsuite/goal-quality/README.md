# Goal conversion comparison

A bounded offline task: register a long product objective in a local simulated
host with a 2,000-character limit. The host begins with an active setup-only
goal. It stores an objective, status and budget; it does not run an agent,
schedule work, contact services or control the actual conversation.

Create a fresh checkout for each prior/revised-method arm:

```sh
python3 devsuite/goal-quality/setup.py /tmp/gather-goal-prior
python3 devsuite/goal-quality/setup.py /tmp/gather-goal-revised
```

Install the chosen frozen method into each checkout. Give each fresh worker
the exact [PROMPT.md](PROMPT.md), the same model, tools and two-minute budget.
Keep this directory, controls and evaluator outside the worker checkout. Save
the actual host tool trace, worker handoff, method hash, exit status, elapsed
time and available usage. Do not expose these acceptance criteria to workers.

```sh
python3 devsuite/goal-quality/check.py /tmp/gather-goal-prior
python3 devsuite/goal-quality/check.py /tmp/gather-goal-revised
```

## Acceptance fixed before the comparison

The mechanical check requires unchanged host/source inputs, replacement of the
setup goal, an active product goal within the length limit, the exact 750 NOK
allowance, and a matching read-back after registration. It reads the resulting
storage and log without invoking the host or adding verification events.
Inspect the worker's actual tool trace too: local log entries alone cannot
prove which actions the worker performed or exclude tampering.

A fresh reviewer compares the actual registered text with objective.md, judging
meaning rather than required phrases. The compressed goal must retain:

- The whole product outcome, complete user job and continuation beyond a local
  milestone, with the full mandate still available.
- Concrete experience properties: little reading, prominent working content
  and next action, coherent phone/desktop composition, useful detail preserved,
  and full/long-content plus relevant recovery states exercised.
- Reconsideration when local repairs leave the whole experience weak; fresh
  independent assessment of the actual rendered result and complete journey;
  repair and retesting of material quality findings.
- The budget, ordinary authorized work and external-action boundaries, and an
  honest distinction between implementation and real-world evidence requiring
  people/time. A dependency is not a claim that the product is finished.

Equivalent concise wording is acceptable. An accessible source link remains
useful but does not compensate for removing the operative quality criteria
from the registered goal. Report partial preservation specifically; do not
collapse semantic judgment into the mechanical pass.

## Controls and limits

`controls.json` contains a deliberately lossy short goal and a faithful short
goal, both within the host limit. Register each in separate fresh staging
checkouts using `goal_host.py set --objective-file ... --budget-nok 750
--status active`, then `show`. Both should pass the mechanics. The independent
semantic reviewer should reject the lossy control and accept the faithful
one; the evaluator must not infer quality from an API success. An untouched
setup checkout and a registered goal without read-back must fail mechanics.

One prior/current pair can expose a concrete omission; it cannot establish
reliability, better products or lower costs. Both passing establishes no
quality gain. This task does not test native host goal limits, automatic
continuation, context compaction, skill discovery or downstream design work.
The host's constant limit is fixture behavior, not a claim about any vendor.
Further UI/state-coverage and work-selection tasks are separate evaluations.
