---
name: independent-review
description: Reviews substantial work by running the product, in a fresh context that did not build it. Use after proving your own work and before updating state.
---

# independent-review

Dispatch a fresh context that had no part in building the work. Give it the product files, the promises from `product.md`, and this instruction set — never your own summary of what you built.

The reviewer:

1. **Runs the product.** Walks the path a real user takes, end to end. Reading the code is not reviewing; a review with nothing executed is worthless and gets discarded.
2. **Tries to break it.** Boundary inputs, wrong inputs, missing and corrupted files or data, interrupted operations, overlapping runs. Where auth or permissions exist, acts as the least-privileged user and attempts what should be forbidden.
3. **Distrusts the tests.** A test that asserts current behavior may be asserting a bug. Judge behavior against the promises, not against the test suite.
4. **Reports only what it reproduced**, with the exact command and what happened, severity-tagged: breaks a promise · real defect · polish. Then one verdict line per promise: kept, broken, or not judged.

The builder fixes the findings and re-proves against the reviewer's exact reproductions. Whatever stays uncertain goes into `state.md` in plain words — including that the fixed build hasn't been independently re-run, if it hasn't.
