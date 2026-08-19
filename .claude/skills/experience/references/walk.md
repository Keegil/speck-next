# The walk

For products with a user interface. The walk gathers what the judge needs to rule on three different things — whether it works, how it feels, whether it's crafted — so the record covers all three, none skipped: the axis that's skippable is the axis that silently stays uncovered. You report; the judge rules.

**The walk:**

1. Get the promise in your head: what the product is for, the moments it claims will feel special, the feel it declared, any named restraint rules. If none were declared, say so in the record — the judge will be ruling on general craft only.
2. Run the real build, not the dev server, and record what commit you ran. Start cold: fresh install or cleared storage, logged out, realistic screen.
3. At the first screen, strip everything you know and answer from the pixels alone: What is this? Who's asking? Why now? Why should I care? Record the confusion exactly as felt — it's front-page material, not a footnote.
4. If you can't get in, unblock honestly — a throwaway account, a test route — but reproduce and log the real barrier first, and never fake the thing you're evaluating.
5. Walk the whole job end to end as the user. Screenshot each screen and each meaningful state (loading, empty, error, success). Keep walking after something breaks — downstream defects hide behind the first one.
6. Chase each claim: when the product says it saved, sent, or generated, find the mechanism — the request, the changed record, the read-back — and record what you found or couldn't find. A product asserting what didn't happen is lying to the user; the mechanism trail is what lets the judge see it.
7. Then behave badly: go back mid-flow, background the app, type garbage, kill the network, force an error. Judge the recovery. And check the second person — sign in as someone else on the same install; any trace of the first user is serious.
8. Actually look at every screenshot — open it and write at least two specific, pointed-at-the-pixels observations. "No issues" is a claim you argue, never a default. An unexamined screenshot is fake evidence.
9. Run accessibility and console checks and keep the raw output: contrast, focus order, touch targets, text scaling, keyboard overlap.
10. Live each promised moment separately and record it: did the trigger fire, did the beats play, and did it feel like the promised thing — or merely technically occur? Report the feeling as felt, in persona.
11. End with the connoisseur pass on the same screenshots, asking a different question: not "is this clear?" but "how is this made?" — record specific observations on hierarchy, spacing, color, type, motion, copy, emotional tone, pointed at the pixels.

**Reporting feel and taste without ruling:**

- Read the product against what it declared it wants to be, never a universal template — the same treatment can be right for a playful product and wrong for a calm one; record the declared feel next to the felt one.
- A named, checkable rule observed broken goes in the record with the exact place it broke. A vibe mismatch goes in as a felt report for the owner's taste call — never quietly "fixed" toward your own aesthetic, never converted into a verdict.
- Sweep every screen for what specs never encode: clipped or overlapping elements, unreachable primary actions, too many type sizes, accents doing unrelated jobs, ragged alignment, placeholder-sounding copy, and whether the mood on screen matches the mood declared. List them concretely; the judge weighs them.
- "The automation couldn't reach it" goes in the record as its own observation — an unreachable control is often unreachable for assistive tech too.
- Where taste genuinely forks, record the fork as a real choice with what each option costs — the owner is the taste judge, and three genuine forks beat thirty.

**The record the judge needs:** what you ran (commit, real build), one examined screenshot per screen and state with its written observations, raw accessibility output, timings where speed is part of the feel, the mechanism behind each claimed action, the per-screen critique, everything you couldn't reach or run, and the open taste forks for the owner. Everything else is ceremony.
