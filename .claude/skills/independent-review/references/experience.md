# Reviewing the experience

For products with a user interface. Three separate verdicts — works · feels good · is crafted — each with its own evidence, none allowed to cover for another. Looking and judging is not an optional branch: the axis that's skippable is the axis that silently stays uncovered.

**The walk:**

1. Get the promise in your head: what the product is for, the moments it claims will feel special, the feel it declared, any named restraint rules. If none were declared, say so in the verdict — you're judging general craft only.
2. Run the real build, not the dev server, and record what commit you ran. Start cold: fresh install or cleared storage, logged out, realistic screen.
3. At the first screen, strip everything you know and answer from the pixels alone: What is this? Who's asking? Why now? Why should I care? Confusion here is a blocking finding, not a note.
4. If you can't get in, unblock honestly — a throwaway account, a test route — but reproduce and log the real barrier first, and never fake the thing you're evaluating.
5. Walk the whole job end to end as the user. Screenshot each screen and each meaningful state (loading, empty, error, success). Keep walking after something breaks — downstream defects hide behind the first one.
6. Prove each claim happened: when the product says it saved, sent, or generated, find the mechanism — the request, the changed record, the read-back. A product asserting what didn't happen is the worst defect class: it's lying to the user.
7. Then behave badly: go back mid-flow, background the app, type garbage, kill the network, force an error. Judge the recovery. And check the second person — sign in as someone else on the same install; any trace of the first user is serious.
8. Actually look at every screenshot — open it and write at least two specific, pointed-at-the-pixels observations. "No issues" is a claim you argue, never a default. An unexamined screenshot is fake evidence.
9. Run accessibility and console checks and keep the raw output: contrast, focus order, touch targets, text scaling, keyboard overlap.
10. Judge each promised moment separately: did the trigger fire, did the beats play, and did it feel like the promised thing — or merely technically occur?
11. End with the connoisseur pass on the same screenshots, asking a different question: not "is this clear?" but "is this crafted?" — hierarchy, spacing, color, type, motion, copy, emotional tone.

**Judging feel and taste without becoming a tyrant:**

- Judge against what this product declared it wants to be, never a universal template — the same treatment can be right for a playful product and wrong for a calm one.
- A named, checkable rule broken is an objective defect: block on it. A vibe mismatch is a question for the owner — never an AI veto, and never quietly "fixed" toward your own aesthetic.
- Something can still be blocked-bad with no rule naming it: two or more concrete pixel-level craft violations on a flagship screen cap the verdict — but you must list them.
- Sweep every screen for what specs never encode: clipped or overlapping elements, unreachable primary actions, too many type sizes, accents doing unrelated jobs, ragged alignment, placeholder-sounding copy, and whether the mood on screen matches the mood declared.
- "The automation couldn't reach it" is a finding about the product until proven otherwise — an unreachable control is often unreachable for assistive tech too.
- Hand the owner real choices, triaged hard: three genuine taste forks, not thirty.

**Worth keeping as evidence:** what you ran (commit, real build), one judged screenshot per screen and state, raw accessibility output, timings where speed is part of the feel, the mechanism behind each claimed action, the per-screen critique, a ranked defect list, three verdicts, open taste questions. Everything else is ceremony.
