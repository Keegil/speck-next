---
name: experience
description: Exercise user workflows to gather evidence about behavior, usability, and recovery. Use for acceptance testing, exploratory walkthroughs, or checking interacting features; routine local checks need no separate testing workflow.
---

# Exercise the affected user job

Gather direct evidence about whether someone can complete the requested job and recover from relevant failures. Testing can support a builder or an independent reviewer; it is not acceptance by itself.

## Identify what you are testing

Read the request and relevant promises. Identify the actual build, commit, or working-tree snapshot being evaluated, with the needed entry point and test data. Include uncommitted changes when they are part of the claim. Use isolation when it protects data or makes the result reproducible; a clean clone is useful only if it contains the subject under review.

Choose the smallest set of scenarios that can establish or overturn the claim. One affected flow may be enough. Add accounts, personas, or failure conditions for distinct risks, rather than to fill a roster. Coordinate parallel tests that share mutable state.

## Run the scenarios

Start where the user starts and finish the complete affected job. Check resulting state when the product claims to save, send, or generate something. For account-sensitive behavior, verify which account owns the data and inspect access from the relevant permissions.

Select additional checks only when needed:

- [Workflow walkthrough](references/walk.md): interactions across screens or features, rendering, accessibility, and recovery.
- [Consequential failures](references/worst-day.md): permissions, data integrity, outages, irreversible actions, or other high-consequence behavior.
- [Agent and skill evaluation](references/agent-evaluation.md): testing a methodology, skill, or harness, including activation boundaries and comparisons.

Before a product exists, test a proposal against raw user evidence, repository behavior, or a small fixture. Agreement among its documents alone cannot validate it. Use safe stand-ins for irreversible actions and explain their limits.

## Return evidence someone can assess

Report the subject tested, actions actually run, observed results, reproducible findings, and material gaps. Keep expected behavior separate from observations. Mark unavailable runtime checks as untested. If a failure is repaired, re-run the affected complete sequence before closing that finding.

Stop when the affected scope has adequate evidence or a concrete blocker is identified. For substantive acceptance, the reviewer must not have contributed to the change. That same fresh context may gather evidence and use `judge` to decide acceptance; a second testing context is not inherently necessary.
