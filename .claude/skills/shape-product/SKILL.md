---
name: shape-product
description: Turns a product intent into product.md through a short owner conversation. Use when a repo has no product.md, or when a new bet is big enough to change what the product promises.
---

# shape-product

Shaping is a conversation, not a form. The owner talks; you ask one or two sharp questions at a time, fill in what's already known, propose defaults for the rest, and mark honest unknowns. Read `references/questions.md` for the questions that have actually mattered — use the ones this product needs and skip the rest. Then write `product.md` and get building: shaping ends the moment the next valuable piece is clear, because a running first increment teaches more than another section.

Rules that bend for nobody:

1. **Outcome before features.** The first line of `product.md` is what the user gets, as their outcome. If the conversation starts with what to build, restart it from what the person is trying to get done, from first principles.
2. **Ask the 2126 question at every drawn surface.** How would this work in 2126? The model does the work up front, infers and pre-fills, and leaves the user a confirmation — never a blank form, never work the system could have done.
3. **Differentiators fire for real.** Every claim about what makes this product special must literally run on the shipped path — real model, real data. A canned substitute is a lie, and shipping it is a promise-breaking defect, not a stub.
4. **Magic moments name their proof.** Each moment the user should feel "this gets me" gets a name, its trigger and beats, the feeling it must produce, and the exact scenario that will prove it — written before anything is built.
5. **Honest before priced.** No price appears anywhere before an honest answer to: what would this person get from free general-purpose AI, a spreadsheet, or a competitor's free tier — and why would they still pay?
6. **Name what the whole must keep.** The properties no single check can own ("the AI does the work", "calm", "never fabricates") go in `product.md`, and consequential decisions state their effect on each. Trading one away is an explicit owner call, never a side effect.
7. **Short is decided; long is undecided.** One sentence per claim. Every promise, job, and moment carries a short stable name (like `moment: first-paste`) so work and reviews can point at it in plain words. Sections that don't apply are omitted, not filled.
8. **The file passes its own bans.** If `product.md` lists words that must never face a user, the file itself — and everything the owner reads — honors the list.
