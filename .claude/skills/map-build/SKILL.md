---
name: map-build
description: Orders build pieces, milestones, and proof when multiple dependencies exist. Skip when a single slice has no ordering problem.
---

# map-build

Use when multiple pieces have real dependencies — or when evidence shows the cut or order is wrong. Not a gate before every build.

Optional rounds in `work/mapping.md`. Prompts in `references/questions.md`. Start `map.md` from `templates/map.md`; keep only useful fields.

Infer routine order from accepted intent, dependencies, and technical constraints. Ask the owner only **consequential** unresolved tradeoffs (what ships first, what promise or risk changes). No mandatory fresh approval for routine mapping.

Bring separate expertise when ordering, value, experience, or feasibility is genuinely uncertain. Record dissent that changes promises, user choices, risk, or order.

When pieces or parallel workers meet at an interface, reuse or agree its observable contract: inputs, outputs, errors, and relevant retry or compatibility behavior. Name one authoritative owner/source and give consumers the actual content and version. Use existing types, examples, or tests when enough; no contract registry is required. Verify both sides together before claiming integration; a mock or matching schema alone cannot prove their behavior. Sequence breaking changes with affected consumers.

## Rules

1. **Pieces from shaped work** — each serves and consumes something real.
2. **Order** — default from dependencies; escalate consequential forks to the owner.
3. **Proof per piece** — runs and checks that matter; scale review to risk.
4. **Milestones** — smallest increments that prove end-to-end value; note when first user surface appears.
5. **Running platform** — consequential platform/care choices in `decisions.md`.
6. **Completion check when non-trivial** — grep/count shaped items vs pieces; report honestly.
7. **Exit** — map is usable for builders; durable direction the owner cares about can be agreed in ordinary conversation — no formal ratification chain.
8. **Re-cut** — record what moved when dependencies change.

Derive summaries from pieces; cite records by file and date.
