---
name: map-build
description: Plan build order, integration boundaries, and verification for dependent pieces or parallel contributors. Use when sequencing or shared interfaces need decisions; skip a single self-contained change.
---

# Plan dependent work

Produce an order that lets builders make useful progress and integrate their work. Start from the accepted request, existing behavior, constraints, and any relevant product or decision records. A chat brief is sufficient input.

## Choose the pieces and order

- Cut work into increments with observable results, each a coherent user job when possible. Include design and refinement in the work that exposes a surface. For each, identify what it delivers, what it depends on, and the checks that establish behavior and relevant workmanship. Add an owner when delegating.
- Prefer an early complete user job or real dependency round-trip. Put uncertain assumptions where they can be tested cheaply before other work relies on them.
- Resolve routine sequencing from the dependencies. Bring consequential architecture, product scope, or care-level choices to the owner with a recommendation; preserve decisions already made.
- Before closing the plan, compare it with the actual request: what is covered, deferred, or missing? Include existing behavior that a migration must preserve. Counting headings is not evidence of coverage.

If the cut or ordering remains unclear, use the relevant [mapping questions](references/questions.md). Bring specialist judgment only for uncertainty that can change the plan.

## Revisit work that remains incomplete

On resuming partial work, locate the next obstacle to the current requested outcome before reusing an earlier order. For an enabling increment, identify its consumer and the step that turns it into a usable result. Preserve applicable evidence, explicit priorities, pauses, budgets, and settled choices.

If scoped repairs leave the same user job failing, trace the failing sequence across shared mechanisms and contributor boundaries. Decide from that evidence whether a local repair still fits or whether pieces, interfaces, or order need to change. Keep working boundaries that serve the job; a failed patch alone does not justify a rewrite. Resolve consequential scope or architecture changes with the owner before dependent work.

## Make parallel work meet

At a shared interface, reuse or agree the observable contract: inputs, outputs, errors, and relevant retry or compatibility behavior. Name its authoritative owner/source and give consumers the actual content and version. Existing types, examples, or tests can be sufficient; a new registry is unnecessary.

Give contributors bounded responsibilities and identify shared files or runtime state. One integrator owns the complete behavior. Verify both sides together before claiming integration; matching schemas or mocks alone cannot prove it. Sequence breaking changes with their consumers.

## Leave a plan builders can use

Return the ordered pieces, dependencies, integration checks, and any unresolved consequential decision. Use `map.md` when this must survive sessions or coordinate builders; the repository-root `templates/map.md` is optional. Keep only useful fields. Add milestones only when they help track meaningful delivery.

Finish when the next piece is actionable and the remaining order is sufficiently clear. Independent review applies to substantive planning decisions before acceptance, without a separate approval ceremony for routine ordering. Revisit the plan when evidence changes a dependency or promise; update the active plan so future builders can follow the revised order and retain the reason for consequential changes.
