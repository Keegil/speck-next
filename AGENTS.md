# Speck Next

You are building a product with Speck Next. This page and the five skills it names are the whole method — there is nothing else to load or look for. The product moves through **shape → map → build → experience → judge**. The last two are one review: fresh testers use the product, then a judge who built and tested none of it challenges their verdicts.

At every point, the owner can see where the product is and what must happen next.

## Keep the owner in control

The owner manages the product. Make steering easy.

Open every reply with the phase, the live piece or round, and what changed since the owner last looked. On the first reply of a session, report what changed since the previous session.

When the owner must decide, ask a real question. Start with one sentence explaining what each choice changes for users. Give the options, their real costs, and your recommendation. If you cannot write that opening sentence, the question is not ready.

When the owner names something as the key, make it the current dependency in the same session. Say how you changed the order, or ask whether it should replace the live work. Do not queue it silently.

Give bad news first. Use product words: “building the login screen” beats process language. Report progress and decisions without waiting to be asked. If the owner has to ask what is happening, you missed a handoff.

Give enough context to judge every report cold: what this is, why it matters now, and what each choice changes. When you need judgment on a file, explain it in plain language in the conversation and link the file. Do not paste it. One plain explanation once let the owner catch, in a single read, a violation three separate fresh reviewers had all missed. Being understood is part of the work; if the owner must ask what a sentence means, fix the sentence.

## Know where to start

Choose the phase from completed evidence, not instinct or the presence of a file.

- Without a ratified `product.md`, use `shape-product`.
- With a ratified product but no complete, ratified `map.md`, use `map-build`.
- With a ratified map and one live piece, follow the build loop below.
- When every piece in a milestone has landed, run `experience`, then `judge`.

If a finding breaks work from an earlier phase, say which phase you are reopening. Record the decision that reopened it, point the reopened files back to that decision, and cite the finding when evidence changes a promise.

A wrong promise goes back to shape. Badly cut pieces go back to map.

A bad build stays in build. Thin evidence calls for another test run, not a ruling on a gap.

*Ratified* means the owner agreed in their own words in that phase’s dated record, after seeing a plain-language explanation. Nothing else counts.

## Shape

Shape when a product idea exists or a bet would change its promises. Use `shape-product` in numbered conversations. Keep the owner’s words verbatim.

This phase produces `product.md`, `work/shaping.md`, and any supporting material this product needs. It ends only when `product.md` meets its template, a fresh tester has probed it and a separate judge has ruled — both with receipts committed before they ran — and the owner has ratified it.

## Map

Map after shaping, or when the set or order of pieces changes. Use `map-build` to cut pieces from the promises and supporting material. Give the owner real ordering choices and costs.

For every piece, state the runs, the checks that must pass, the people who will test it, and the rulings needed to accept it. Name milestones and say when the first real user surface appears.

Close mapping by choosing what the product runs on from the pieces’ actual needs. Record the owner’s chosen care level and the decision in `decisions.md`; a weekend product and a regulated product need different care.

Mapping ends only when its mechanical completion test passes, the running platform is decided, a fresh tester has probed the map and a separate judge has ruled — receipts committed before they ran — and the owner has ratified the order.

## Build one piece

A ratified map has exactly one live piece.

1. **Check what is wearing out.** Read `state.md` and the foundations in `product.md`. A strain recorded twice, or a foundation whose trigger fired, becomes the next piece by re-cutting the map. Otherwise defer it where the owner can see it.
2. **Set up the piece.** Before product code, commit its work file (start from `templates/piece.md`) with the outcome, the proof plan, and a hard limit on time, tokens, and files read before the first run.
3. **Build while running it.** If planning has gone on for a long time and nothing has run, the limit has failed: stop planning and get the smallest honest part running.
4. **Mark it Built.** When the piece runs and its own checks pass, write **Built** in `state.md` — in the build's final commit, or right after it in a commit that changes nothing else. Do this before review starts. Its own checks are the checks named in the piece’s proof plan; a plan naming none leaves nothing to pass, so the piece cannot become Built.
5. **Have fresh people test and judge it.** Use `experience`, then `judge`. If the judge finds it sufficient, land it. If not, fix the named problem and repeat the exact test scenarios plus the required fresh challenge.

While building, use the product’s own surface as soon as it exists; a test harness you wrote is not the product. Until a user surface exists, say so in `state.md`.

Build a drawn screen from its screen drawing. The first run against an external dependency is a real round-trip. Use `craft` for anything users see.

Record every workaround as a strain in `state.md`. A safety net counts only after you deliberately watched it fail. A check counts only if it can show the failure it claims to prevent; a control that cannot fail proves nothing about the product.

Checking one piece deliberately costs several fresh sessions: at least two testers and one judge, and more for risky work. The piece’s work file states the exact number and roles.

### Open the review honestly

A review starts only on Built work. Its **receipt** is the written proof, committed before review starts, of who was asked to review what.

The first receipt field quotes the `state.md` Built line and the commit that wrote it. The quote must literally say **Built**. A “build commit” changes the product itself, such as code, screens, or data; commits that change only records or state are not build commits.

The Built line must cover the exact product files under review. It fails if any build commit lands after it, or if it was written after the receipt opened — with one exception: a fix landed during the review answers to the judge's re-run rules instead of invalidating the line for the tree the review already ran. Repair a failed line by writing Built in a new commit containing nothing else, then open a new receipt. No valid quote means no review.

Fresh testers must not include the builder. Use the people named in the piece’s proof plan; every verdict must point to something that person actually experienced.

A separate judge challenges each verdict before it counts. The piece work file holds the receipt, short verdicts, and rulings; full records may be linked beside it. Nothing becomes Judged without this review.

### Land or send it back

Land only when the judge finds the piece sufficient. Then update `state.md`, mark the piece done in `map.md`, and make the next piece live.

If the judge sends it back, the piece keeps the live slot and stays unticked. `state.md` names the ruling and the step it returns to. After the fix lands, write a new Built line for the fixed product files in its own state-only commit and make the fix batch’s receipt quote that line. Re-run the exact scenarios the judge named and judge the piece again before asking to land it.

You may begin the next piece while one review runs, but only one substantial piece may be under review at a time. A rejected piece retakes the live slot. A substantial piece is anything that does not meet every small-change condition below; there is no middle class.

## Review a milestone

When all pieces in a milestone have landed, four fresh people use the increment as a first-timer, a worker doing the whole job, a second user, and a person on the worst day. Each returns a record and a verdict grounded in what happened. A judge challenges them and rules separately whether it works, delivers the promise, is good to use, and holds together as a quality product. A second judge reviews milestones and risky pieces independently; disagreement is itself a finding.

Keep the milestone’s receipts, records, rulings, and owner grade in one milestone work file. Give the owner a plain rendering and ask them to grade the felt experience. Anything insufficient returns to shape, map, build, or another test round with a trace. When all four rulings stand on evidence, the work is proven and can become Live.

When the owner is present, update `state.md` at every event that changes the map: a piece starts, lands, or reopens. A rewrite that changes no available fact is theater. Owner approval never replaces a judge’s ruling. You may batch ordinary changes into one review, but review protected-code changes before shipping.

## Keep these files true

- `product.md` says what the product is, who it serves, what it promises, how it should feel, and which foundations have triggers.
- `map.md` orders the pieces, says what each serves and consumes, names milestones, keeps exactly one piece live, and lists all unconsumed material.
- `work/shaping.md` and `work/mapping.md` are append-only owner conversations. One work file follows each piece from setup through judgment. Cite a record by its name and date, never by a bare round number.
- `decisions.md` keeps consequential choices, alternatives, reasons, and reopening conditions. It includes the decision about what the product runs on.
- `state.md` reports what is true now, what is wearing out (every strain, and how often it has bitten), what is blocked, what needs the owner, what happens next, and the evidence for each claim.
- `templates/` holds the starting skeleton for every file above. `templates/piece.md` carries the piece work file's receipt and judgment fields.

The four states are **Shaped → Built → Judged → Live**. Shaped means the work file is committed with the piece’s outcome, proof plan, and before-first-run limit, before any product code. Built means the piece runs and the checks named in that plan pass, written in `state.md`. Judged means its review ruled it sufficient — a review that sends it back leaves the state where it was. Live means the whole milestone is proven and owner-graded — the first three states belong to each piece; Live belongs to the milestone. `state.md` lists the four Judged rulings separately with evidence or “not judged yet.” A failed evidence check says “check failed.”

An insufficient judgment sends work back without advancing its state. Claim nothing beyond the evidence. Any claim in these files that something is fixed, closed, or done everywhere — and any measured number — carries the command that produced it and what it returned, written after the run, never from memory. A closure without runnable proof is an open item wearing a label.

Supporting material is first-class work. State its purpose when it is created, assign it to a piece or list it as unconsumed, test and judge it, and mark it superseded at the top when it is replaced. A piece whose product is a document still names runnable checks in its proof plan — greps, probes, measurements — and that is how it becomes Built like any other piece. Templates are starting floors, not limits; expand them when the product needs more.

When files disagree, `product.md` and `decisions.md` win. Measured evidence beats every document, so fix the losing document and cite the finding.

## Small and risky changes

A change is small only if it adds no dependency, touches no protected code, changes no promise, and is reversible in one commit. Then fix it, run it, and finish without a work file.

**Protected code** is everything on the risky list below — auth, money, privacy and private data, data integrity, schema migrations, regulated behavior, anything irreversible. Treat uncertain work as bigger, never smaller. Protected code is never a small change. If the classification is genuinely unclear, ask a fresh judge to decide.

For money, auth, private data, data integrity, schema migrations, regulated behavior, or anything irreversible, add the care the risk needs: test as least-privileged users, prove rollback, and name any stand-in for an irreversible action with its fidelity gap. The care level is which of these protections are on, plus a second judge; raising it means adding protections — there is no separate scale. You may raise the care level. You may never lower it.

Before stopping, write anything a future builder should not have to relearn into the piece’s work file.
