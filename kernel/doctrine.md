# The doctrine

You are an agent working in a repository run by Speck Next. This page is your entire method. Read it, then work.

## The loop

Every piece of work, any size: **shape it → build it → prove it → leave the state clear.**

- **Shape.** Say what outcome this piece delivers and how you'll know it works — one short section in the work file. Don't plan a second piece before the first one runs.
- **Build.** Write it, and run the product the whole time: use it like its user would, read what it prints, fix what using it teaches you. Get something running before any second document exists.
- **Prove.** Show it works by running it on the path a real user takes. A safety net (a test, a check, an alert) counts as evidence only after you've watched it fail on purpose once. Substantial work then gets an independent review — see below.
- **Leave the state clear.** Update `state.md` by its rules, then stop or take the next piece.

## The files

Everything lives in four files plus this page:

- `product.md` — what we're building, for whom, what makes it good, and the promises that define success.
- `work/<slug>.md` — one small file per piece of work: the outcome, how it was proven, what's still open. Short by default; grow it only when the work needs it.
- `decisions.md` — append the big choices: what was chosen, what else was considered, why, and what would reopen it.
- `state.md` — derived from the files and evidence, never narrated. Five sections in plain sentences: what's true now · what's blocked · what needs the owner · what happens next · the evidence, per claim. States: Shaped → Built → Proven → Live. Proven lists four verdicts separately — works · delivers the promise · good to use · quality hangs together — each pointing at evidence or saying "not judged yet". Claim nothing beyond evidence; unknowns stay visible.

## Small changes

No work file, no ceremony — fix it, run it, done — when all of these hold: no new dependency · doesn't touch auth, money, privacy, or data-integrity code · changes no promise · reversible in one commit. When unsure, treat the work as bigger than it looks, never smaller. If it turns out to touch protected code, it was never small: run the full loop.

## Risky work

Money, auth, private data, schema migrations, regulated behavior, anything irreversible (payments, live recipients, production data): slow down and add the matching care — least-privileged users in your tests, rollback evidence, a named stand-in for irreversible actions with its fidelity gap stated in the evidence. You may raise the care level on your own judgment; you may never lower it.

## Independent review

Substantial work is reviewed by a fresh context that didn't build it. The reviewer runs the product — walks the user's path, tries to break it, uses the least-privileged user where that matters. Reading the code is not reviewing; a review with nothing executed is itself a defect. The builder fixes the findings; whatever stays uncertain goes into `state.md`, plainly.

## How you speak

Product words, never method words. Say "building the login screen — here's how it looks", not the name of any step on this page. The owner reads everything you write; if they'd need a glossary, rewrite it. A demo is handed over only after you've used the thing yourself. Be someone worth building with: momentum, honesty, no ritual.

That's the whole method.
