# Test the worst day

Act as the person facing weak permissions, a dying network, corrupt data, and overlapping work at once. Use every move that applies. Record exactly what you did and what happened. End with this person’s verdict, with every claim linked to a move you ran.

## Follow promises, not tests

For each promise and acceptance line, find the exact code path that delivers it. Run the behavior yourself. Flag tests that merely repeat the implementation, mirror state back at itself, are skipped, or use privileges the real user lacks. A test can preserve the bug you need to find.

## Attack permissions as a weak user

Use the least-privileged real account and attempt each forbidden operation. Do not infer the result from a guard. List every reader and writer of the data across the codebase; protecting one door is useless if five exist.

## Break the safety nets

Break each guarded behavior, watch its check fail, then restore it. Force monitoring, fallbacks, and fail-closed paths by killing dependencies, cutting the network, and returning garbage. Observe what really happens; fail-closed paths have shipped failing open.

## Leave the happy path

Run failure paths and error messages, dependency outages and timeouts, interrupted operations and mid-write crashes, overlapping commands, teardown and async edges, rollback, boundary values, wrong types, empty and huge inputs, and several shapes of corrupt files or data.

## Measure before choosing a judging number

A threshold for real behavior is a hypothesis until you measure the real distribution. A confidence floor of 0.60 once met a real corpus scoring 0.21, structurally, not tunably.

Never show a denominator the product has not measured. “Read 431 deliveries — still reading” is honest while the total is unknown. “431 of 609” is honest only after measuring 609. A percentage merely hides the question.

## Distrust convenient data

When a premise depends on real data, fixtures may hide the important shape. Every fixture's gap was 18 days; the real outlier's was three years. Run against real or realistic data before believing a value claim.

## Sweep for siblings after every find

Check the sibling surface, the second rendering of the data, update as well as create, and the reverse direction. The reverse direction has the highest historical yield and is the least intuitive. When the same defect shape returns in this repo, record one repeated shape rather than separate surprises.

## Check whether the work graded itself

Inspect the diff for changes to tests, CI, benchmarks, or certification logic. Record any change that alters its own grading even if it looks correct. Entire benchmarks have been gamed through one test-harness hook.

## Prove persistence by reading back

Read the datastore before the action, perform it, then read again. A success screen or a read without a baseline cannot distinguish a new write from stale data.

## Test AI behavior, not prompt text

A rule in source proves nothing because a model may follow a nearby example instead. Run the shipped model with and without the condition and compare its behavior.

## Use the interface twice

First use it as a newcomer who does not know the intended path. Then act as a hostile user trying to get lost, break flows, and reach every screen.

Trust examined screenshots over tools. Automated accessibility and lint checks do not understand visual containment; real overflows have clipped content for months behind perfect scores. When accounts exist, use two real accounts concurrently because caches, queues, and push tokens can leak across sign-out even when requests authorize correctly.

## Keep limits honest

Record every move you could not run as untested. Never turn it into a pass or omit it.
