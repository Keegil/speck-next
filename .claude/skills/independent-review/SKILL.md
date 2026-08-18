---
name: independent-review
description: Reviews substantial work in a fresh context that did not build it — by running the product, or for shaping artifacts, by refuting them against the owner's record and the wire. Use after proving your own work, and before a substantial shaping artifact reaches the owner.
---

# independent-review

**The review happens in a genuinely separate context, and there is a receipt.** Nothing else here matters if this part is faked: a "review" performed by the builder in its own head is void, cannot lift any verdict, and writing "a reviewer verified this" without the receipt below is fabricated evidence — the worst defect class this method knows.

**Dispatch, concretely.** In Claude Code: launch a subagent (the Agent tool, fresh context, a different model when available). On any host: `codex exec --sandbox workspace-write -C <fresh clone>` or another agent CLI, run against a clean clone — never your working tree. Give the reviewer the product files, the promises from `product.md`, and this skill's files — never your own summary of what you built.

**The receipt opens at dispatch, or it is void.** Before the reviewer runs, the work file records: who is reviewing (tool, model, session), when and at what commit it was dispatched, the reference set it judges against, and the commands planned. Findings and verdicts are appended when it returns, verbatim or linked. A receipt reconstructed at closure is exactly what a builder writes when nothing forced the capture — it does not count, twice proven. A verdict in `state.md` may only cite a review whose receipt was open before the review ran. No dispatch-time receipt, no review, no lifted verdict.

**Substantial shaping artifacts get this review before the owner reads them.** When the work under review is a shaping artifact — a `product.md` draft, a domain model, journeys, a deck; not every conversational round — the product may not run yet, so the *subjects* change and the rule stands: the reviewer still executes, but what it executes are probes against the wire fixtures, greps against the repo, and checks against the owner's verbatim shaping record — never a read of sibling documents against each other, because a document corpus drifts into perfect agreement with itself. Hunt especially: words in the owner's mouth he never said · claims the measured evidence refutes · drawn elements no evidence can back · contradictions between artifacts · artifacts that went stale without a supersession line. The dispatch-and-receipt law applies unchanged, and a shaping review whose transcript shows zero executed checks is discarded like any other.

The reviewer:

1. **Runs the product.** Walks the path a real user takes, end to end. Reading the code is not reviewing; a review with zero executed commands is discarded. If the product has a user interface, also read `references/experience.md` and return its three verdicts — works, feels good, is crafted.
2. **Tries to break it.** Read `references/attack-playbook.md` and run what applies — boundary and hostile inputs, corrupted data, interrupted and overlapping runs, forced dependency failures, real least-privileged users attempting the forbidden.
3. **Distrusts the tests.** A test that asserts current behavior may be asserting a bug. Judge behavior against the promises, not against the test suite.
4. **Judges the structure, not just the piece.** After the increment verdicts: is the whole still sound? Duplication growing across pieces, patterns diverging, this piece fighting the existing shape, strain lines in `state.md` going unaddressed — one structure verdict: **sound**, **straining** (name exactly what), or **fighting**. Two straining verdicts in a row, or one fighting, means the next piece is structural work, not a feature. This call belongs to the reviewer precisely because the builder has momentum — the party that wants to keep building never decides whether building should pause.
5. **Reports only what it reproduced**, with the exact command and what happened, severity-tagged: breaks a promise · real defect · polish. Then one verdict line per promise: kept, broken, or not judged — plus the structure verdict.

The builder fixes the findings and re-proves against the reviewer's exact reproductions. Whatever stays uncertain goes into `state.md` in plain words — including that the fixed build hasn't been independently re-run, if it hasn't.
