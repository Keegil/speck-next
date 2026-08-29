---
name: experience
description: Sends fresh testers to use the product as a first-timer, worker, second user, or person on the worst day. Each returns a record and a verdict for the judge. Use after every substantial piece and at every milestone.
---

# experience

A tester decides as a user would, after using the product. Every verdict points to moments in that tester’s record, and a separate judge challenges it before it counts.

## Send a genuinely fresh tester

Use a separate context. A walk done by the builder is void. Claiming fresh users without a committed receipt is fabricated evidence.

Run the tester in a clean clone, never the builder’s working tree. Give them the product files, the promises from `product.md`, and this skill with its references. Do not give them the builder’s summary. Testers read every page from disk at the commit under test — a host may preload an older copy, and two testers on two pieces have caught theirs doing exactly that.

Before the run starts, commit a **receipt**: written proof of who was asked to test what. Record:

- Quote the `state.md` Built line that covers these product files. (Build reviews only: a shaping or mapping review has nothing built yet — its receipt lists the planned probes instead.)
- Name the persona, tool, model, and session.
- Give the dispatch date and commit.
- List the planned walks and commands.
- Name the session that owns this run.
- Tell a later session finding an empty record to re-dispatch under its own named line rather than guess what happened — two runs once executed one dispatch in parallel, neither knowing of the other.

Append or link the returned record. A receipt reconstructed at closure is exactly what a builder writes when nothing forced the capture — it does not count, twice proven. Without a receipt committed before the run, there is no record for the judge.

Runs sharing one browser, device, or live environment run one at a time, each on its own subject, and the dispatching session keeps its hands off that shared environment while a run is live. Two rounds were once destroyed in a day: the dispatching session measuring inside a live run, then two parallel runs walking each other's subjects.

For a review that batches several changes, list them from the commit range. A hand-written batch list once omitted the exact change a tester then walked into blind.

## Prove who the tester is

Any product with accounts or sessions starts with identity proof:

1. Clear state and quote the product’s own identity view; it must show nobody.
2. Establish the test subject through a mechanism that can really do so. An account created through the product’s front door proves itself.
3. Quote the identity view again; it must exactly match the brief.

If either read is wrong, stop and report it. Three rounds of production runs were once void because a plant failed silently and every run confidently walked a stranger's session — a wrong-subject run still renders screens.

## Record the run, then decide

Write the record as the run happens. Include exact commands, what appeared, what changed, and feelings reported in persona. Open every screenshot and give at least two observations that point to its pixels.

Put the verdict last. Say, as this user, whether it works, whether you would keep it, and what breaks the deal. Every claim in the verdict must point to a moment in the same record. Mark anything you could not run as untested; never turn it into a pass or omit it.

The judge will ask questions. Answer from new or recorded runs, never memory or politeness.

A fresh context may continue a tester whose session ended. It inherits the persona and full record, runs the exact scenario the judge ordered, and appends a marked follow-up. It never rewrites the first run.

## Staff the review

A substantial piece uses the people named in its proof plan, with at least the first two below. A milestone uses all four, one fresh tester each.

1. **First-timer:** Start from a fresh install or cleared storage, logged out, knowing nothing. From the first screen alone, answer: What is this? Who is asking? Why now? For a user interface, follow `references/walk.md`.
2. **Worker:** Complete the real job through the product’s own surface. A builder’s harness is not the product. Trace each claimed save, send, or generation to the request, changed record, and read-back.
3. **Second user:** Use a real least-privileged account to try forbidden actions. Then use a second person on the same install and look for traces of the first.
4. **Worst day:** Bring hostile and unlucky conditions together by following `references/worst-day.md`.

One of these testers also receives only `product.md` and the piece’s rendered output, not the work file. The dispatching session must render headless output into something the owner could inspect. Five rounds once perfected a truthful machine that missed its jobs. The owner's one read of a rendered page caught what a dozen fresh contexts missed.

For machinery such as checks, boards, or pipelines, one rostered tester attacks it by running it. The record quotes the commands and output. Without an executed attack, the record is a read, not an experience.

Different users should sometimes disagree. Never soften one verdict toward another; the judge needs the difference intact.

## Test shaping material too

Before a product runs, test `product.md`, domain models, journeys, drawings, and decks against independent subjects: the owner’s verbatim record, the repo, fixtures, or real behavior. Do not prove sibling documents by comparing them only with each other.

Place the artifact’s claim beside what the independent subject says. Read anything owner-facing cold as a smart outsider and record each stumble.

End with a verdict: Could I act on this? Does it say what the owner said? Where does it break? Every claim must point to a probe you ran.

Append the record and verdict to the receipt. The judge then questions it and may send the tester back before ruling.
