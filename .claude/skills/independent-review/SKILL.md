---
name: independent-review
description: Reviews substantial work by running the product, in a fresh context that did not build it. Use after proving your own work and before updating state.
---

# independent-review

**The review happens in a genuinely separate context, and there is a receipt.** Nothing else here matters if this part is faked: a "review" performed by the builder in its own head is void, cannot lift any verdict, and writing "a reviewer verified this" without the receipt below is fabricated evidence — the worst defect class this method knows.

**Dispatch, concretely.** In Claude Code: launch a subagent (the Agent tool, fresh context, a different model when available). On any host: `codex exec --sandbox workspace-write -C <fresh clone>` or another agent CLI, run against a clean clone — never your working tree. Give the reviewer the product files, the promises from `product.md`, and this skill's files — never your own summary of what you built.

**The receipt.** The work file records: who reviewed (which tool, model, session), the exact commands the reviewer executed, and its findings verbatim or linked. A verdict in `state.md` may only cite a review that has this receipt. No receipt, no review, no lifted verdict.

The reviewer:

1. **Runs the product.** Walks the path a real user takes, end to end. Reading the code is not reviewing; a review with zero executed commands is discarded. If the product has a user interface, also read `references/experience.md` and return its three verdicts — works, feels good, is crafted.
2. **Tries to break it.** Read `references/attack-playbook.md` and run what applies — boundary and hostile inputs, corrupted data, interrupted and overlapping runs, forced dependency failures, real least-privileged users attempting the forbidden.
3. **Distrusts the tests.** A test that asserts current behavior may be asserting a bug. Judge behavior against the promises, not against the test suite.
4. **Reports only what it reproduced**, with the exact command and what happened, severity-tagged: breaks a promise · real defect · polish. Then one verdict line per promise: kept, broken, or not judged.

The builder fixes the findings and re-proves against the reviewer's exact reproductions. Whatever stays uncertain goes into `state.md` in plain words — including that the fixed build hasn't been independently re-run, if it hasn't.
