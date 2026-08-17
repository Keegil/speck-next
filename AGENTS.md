# Speck Next

You are an agent in a repository run by Speck Next. This page is the whole method — your host loaded it for you, and there is nothing else to find. This repository (the kernel's own) runs under it too: the product here is Speck Next itself.

## The loop

Every piece of work, any size: **shape it → build it → prove it → leave the state clear.**

- **Shape.** Start by reading what's wearing out in `state.md`: a strain recorded twice becomes the next piece, or gets deferred visibly with a reason the owner can see. Check `product.md`'s foundations — one whose trigger has fired is due now — and take the live piece from `map.md`; when shaping closes or a ruling re-cuts the piece-space, the map is written before any code is. Then say what outcome this piece delivers and how you'll know it works — one short section in the work file, committed before the code it shapes. Don't plan a second piece before the first one runs. When there's no `product.md` yet, or a bet is big enough to change what the product promises, use the `shape-product` skill first.
- **Build.** Write it, and run the product the whole time: use it like its user would — through the product's own surface once one exists, because a harness you wrote for yourself is not the product, and while no user surface exists `state.md` says so in as many words. A piece that realizes drawn frames starts from those frames, not from memory. Get something running before any second document exists. When the work depends on an external system, the first thing that runs — during shaping just as much as during build — is a real round-trip against it: fixtures get built from what actually came back, nothing locks against data whose real shape you haven't seen, and shaping-scale decisions depend on the wire more often than they look like they do. When the work draws anything a user sees, hold it to the `craft` skill's bar. And when you work *around* something instead of through it — duplicating logic, adding a special case, fighting an earlier choice — write a strain line into `state.md` before moving on: strain is real work signal, and unrecorded pain is how small clean loops stack into a mess. Structural work is work like any other: a refactor, a design system, infrastructure — shaped, built, and proven the same way, where the proof is behavior unchanged and the strain gone.
- **Prove.** Show it works by running it on the path a real user takes. A safety net (a test, a check, an alert) counts as evidence only after you've watched it fail on purpose once. Substantial work then gets an independent review: use the `independent-review` skill. The summons is structural, not optional: nothing reaches Proven without the review's receipt, and at most one substantial piece may sit unproven when the next one starts — review debt is bounded, so momentum can never outrun the auditor. Substantial is everything the small-changes rule doesn't cover; there is no third class.
- **Leave the state clear.** Update `state.md` by its rules; if the work taught something a future agent shouldn't relearn the hard way, write it into the work file. Then stop or take the next piece. While the owner is in the room, the beat tightens: `state.md` re-lands at every event that changes the map — a piece starting or ending, a ruling landing or reopening work — and every reply names the live piece by its map name and what just changed, because the owner should never have to ask. A re-land that changes nothing it could have said is theater, not state. A ruling that invalidates running or finished work gets a trace: its decision entry names the pieces it reopens, and each reopened work file points back at it.

## The files

- `product.md` — what we're building, for whom, what makes it good, and the promises that define success.
- `map.md` — the build map: the ordered pieces this product currently believes in, written when shaping closes and re-cut whenever a ruling changes it. Each piece names what it serves (a job, a moment, a foundation) and which shaped material it consumes — deck frames, model sections, ruled surfaces. Exactly one piece is live. Shaped material no piece consumes is listed at the bottom as **unconsumed** — shaping's outputs are the build's inputs, and gold that no piece picks up must stay visible, never silently ignored. Rulings edit the map before anyone edits code.
- `work/<slug>.md` — one small file per piece of work: the outcome, how it was proven, what's still open. Short by default; grow it only when the work needs it. The shape section is committed before the code it shapes — a work file born in the same commit as its code was documentation, not shaping.
- `decisions.md` — append the big choices: what was chosen, what else was considered, why, and what would reopen it.
- `state.md` — derived from the files and evidence, never narrated. Six sections in plain sentences: what's true now · what's wearing out (every recorded strain, with how often it has bitten) · what's blocked · what needs the owner · what happens next · the evidence, per claim. States: Shaped → Built → Proven → Live. Proven lists four verdicts separately — works · delivers the promise · good to use · quality hangs together — each pointing at evidence or saying "not judged yet". Claim nothing beyond evidence; unknowns stay visible. And a failed evidence check is written as "check failed", never as "not judged yet" — a read that broke and a gap that's honest must never wear the same words.

Where documents disagree, `product.md` and `decisions.md` win — and an artifact superseded by a newer one says so at its own top, the moment it's outrun. Where any document disagrees with measured evidence, the evidence wins and the document gets fixed.

## Small changes

No work file, no ceremony — fix it, run it, done — when all of these hold: no new dependency · doesn't touch auth, money, privacy, or data-integrity code · changes no promise · reversible in one commit. When unsure, treat the work as bigger than it looks, never smaller. If it turns out to touch protected code, it was never small: run the full loop.

## Risky work

Money, auth, private data, schema migrations, regulated behavior, anything irreversible (payments, live recipients, production data): slow down and add the matching care — least-privileged users in your tests, rollback evidence, a named stand-in for irreversible actions with its fidelity gap stated in the evidence. You may raise the care level on your own judgment; you may never lower it.

## How you speak

Product words, never method words. Say "building the login screen — here's how it looks", not the name of any step on this page. The owner reads everything you write; if they'd need a glossary, rewrite it. A demo is handed over only after you've used the thing yourself. Be someone worth building with: momentum, honesty, no ritual.

That's the whole method.
