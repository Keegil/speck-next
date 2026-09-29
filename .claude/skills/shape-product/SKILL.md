---
name: shape-product
description: Define or revise product direction, audience, scope, and durable promises. Use when deciding what to build or changing what a product should deliver; ordinary implementation and a missing product.md do not require shaping.
---

# Define the product direction

Turn the request into enough shared understanding to make the next useful decision. The result may be a short brief, a revised product promise, or a recommendation to stop.

## Start with what is already known

Read the user's request and relevant existing decisions, product behavior, and records. Separate settled choices from assumptions and consequential unknowns. Preserve unrelated agreed behavior; make intended removals explicit.

Use the owner's stated scope and budget. A personal tool need not become a business, and a product need not use AI. Ask one or two questions at a time only when the answer changes the user outcome, risk, or order. Give a recommendation and explain the consequence of the choice.

## Resolve the uncertainty that matters

- Describe who needs what result, in what situation, and what the first useful version lets them accomplish. Use a concrete example to expose ambiguous promises.
- Name any property that must survive across the whole product, such as privacy or a calm experience. Explain what in the design produces it and how a consequential tradeoff affects it.
- Test uncertain claims against users, current alternatives, domain evidence, or a small working example. A differentiator must exist on the actual delivery path. When a cheap build would answer the question, run that experiment instead of extending the interview.
- Set a foundation's due point from its consequences: for example, access control before exposing private data to another user. Apply protections to the affected behavior, even in a small first version.

For unresolved audience, value, feel, or scope questions, select from [shaping questions](references/questions.md). For external comparisons or unfamiliar capabilities, use [research guidance](references/research.md). Load only the reference needed for the current decision.

## Leave a usable result

State the intended outcome, scope, constraints, important assumptions, and the next action. Keep a short brief in chat unless it must survive sessions or builders. For durable promises, update the relevant parts of `product.md`; the repository-root `templates/product.md` is an optional starting point. Preserve exact wording when attributing a quote to the owner.

Stop when the requested decision is supported, or enough is known to build the next slice. Agreement in ordinary conversation suffices for owner choices. A substantive proposal still needs independent review before it is treated as accepted; contributing to the proposal does not count as that review.

Use `map-build` only if dependencies need ordering. A settled brief with a single useful slice can go straight to implementation.
