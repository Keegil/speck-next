---
name: map-build
description: Plan build order, integration boundaries, and verification for dependent pieces or parallel contributors. Use when sequencing or shared interfaces need decisions; skip a single self-contained change.
---

# Plan dependent work

Produce an order that lets builders make useful progress and integrate their work. Start from the accepted request, existing behavior, constraints, and any relevant product or decision records. A chat brief is sufficient input.

## Choose the pieces and order

- Cut work into increments with observable results. For each, identify what it delivers, what it depends on, and the check that will establish it works. Add an owner when delegating.
- Prefer an early complete user job or real dependency round-trip. Put uncertain assumptions where they can be tested cheaply before other work relies on them.
- Resolve routine sequencing from the dependencies. Bring consequential architecture, product scope, or care-level choices to the owner with a recommendation; preserve decisions already made.
- Before closing the plan, compare it with the actual request: what is covered, deferred, or missing? Include existing behavior that a migration must preserve. Counting headings is not evidence of coverage.

If the cut or ordering remains unclear, use the relevant [mapping questions](references/questions.md). Bring specialist judgment only for uncertainty that can change the plan.

## Make parallel work meet

At a shared interface, reuse or agree the observable contract: inputs, outputs, errors, and relevant retry or compatibility behavior. Name its authoritative owner/source and give consumers the actual content and version. Existing types, examples, or tests can be sufficient; a new registry is unnecessary.

Give contributors bounded responsibilities and identify shared files or runtime state. One integrator owns the complete behavior. Verify both sides together before claiming integration; matching schemas or mocks alone cannot prove it. Sequence breaking changes with their consumers.

## Leave a plan builders can use

Return the ordered pieces, dependencies, integration checks, and any unresolved consequential decision. Use `map.md` when this must survive sessions or coordinate builders; the repository-root `templates/map.md` is optional. Keep only useful fields. Add milestones only when they help track meaningful delivery.

Finish when the next piece is actionable and the remaining order is sufficiently clear. Independent review applies to substantive planning decisions before acceptance, without a separate approval ceremony for routine ordering. Revisit the plan when evidence changes a dependency or promise; record the consequential change where future builders will find it.
