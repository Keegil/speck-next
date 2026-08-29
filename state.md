# State

## What's true now

The kernel is at **v5.2.0**. Every page an agent loads is written in a builder's words: the method page (`AGENTS.md`), five skills — `shape-product`, `map-build`, `craft`, `experience`, `judge` — with four references, six template skeletons, and the installer. The method's shape: five phases, shape → map → build → experience → judge, where the last two are one review — fresh testers use the product and decide as users do, and a judge who built and tested nothing challenges every verdict before it counts. States: Shaped → Built → Judged → Live, with *proven* as plain speech for all four rulings standing on evidence.

The rewrite piece ("A builder's words, and fewer of them") is **landed**: the installed surface went from 70,770 bytes to 55,157 (measured at ebb9fb5, −22%), mean sentence length from 24.4 to 13.3 words, all 177 operative rules conserved and verified by executed probes, nine old method words at zero, and the sentences the last piece's judges ordered are in: the thinking cap, the honest cost line, the three receipt-gate fixes. The contract stands at v0.7 (hearing records counted separately, capped at six per review, re-hearings extend records). A cold reader who had never seen Speck ruled the pages "buildable, and I would want to build under it," computed the full review cost unaided, and named `craft` the plainest file in the set.

## What's wearing out

- **The piece's report of itself.** Five bites across two pieces, every one caught by a fresh context or judge, never by the author — a false closure claim, an unreproducible control, the piece's own re-entry law unobeyed by its fix batch, a protected-gate fix mislabeled a small change, and this file going stale twice inside one review. The judges' sharpening: the next piece owes a **producer** for self-report and self-classification, not another detector — a classification rule whose only trigger is the builder feeling unsure has no trigger at all.
- **Byte-exact self-measurements in this file.** Stale the moment this file is rewritten; figures are pinned to the commit they were measured at; a computed check would retire the strain for good.

Retired by the rewrite piece, bar met and measured: **the kernel only grows** — 70,770 → 55,157 bytes, the first shrink in the kernel's history. Retired earlier the same day: the receipt law and the stdin-hanging dispatches (bitten twice pre-v4, held through every review since).

## What's blocked

Nothing.

## What needs the owner

Seven questions, filed with full context in [work/builders-words.md](work/builders-words.md) and [work/campaign-adoption.md](work/campaign-adoption.md) — none blocked landing:

1. **The next kernel piece** — both judgment lines recommend the same thing: define the six load-bearing words nothing defines (Shaped · Live's boundary · care level · straining-vs-fighting · captioned screen drawing · "its own checks") and give the non-rule properties a producer. They split only on whether it is mandated (line 1: structure straining, second in a row) or your choice (line 2: sound) — which is itself question 6: when blind judges split on straining, what counts?
2. **Does a finished piece go Live alone, or only with its proven milestone?** The pages say both; a real shipping-cadence fork. Judges recommend: per milestone.
3. **The war stories** — every slow sentence in the cold reads was a compressed scar; one was cut entirely (the plain-rendering catch — your catch). Restore that one, keep the rest?
4. **The repo's own README and docs still speak the old vocabulary** — sweep now or as the next small piece? (This file is swept; historical records keep their original words.)
5. **The worst-day tester currently audits our own build loop** — move the git audit to the judge, threshold the staleness count, or drop it?
6. *(folded into 1.)*
7. **What does the kernel actually buy?** The dev suite's `--ungoverned` arm — same tasks, method pages stripped — had never been run in the repo's history; it is running now, and its result lands in the work file as the first measurement of the kernel against its own absence.

Standing, non-blocking: the v5-era fixture milestone's felt grade ([work/v5-hearing.md](work/v5-hearing.md)).

## What happens next

The next kernel piece is the owner's call (question 1 above). Two method items are filed for it so they cannot expire silently: the judge's phase-exemption second clause ("the review's subject is `product.md` or `map.md` itself") has never been run by anyone; and judge's receipt-coverage rule and mid-review-fix rule are silent about which governs a build commit landing mid-review (inherited silence, resolved once on the record by judgment 2″'s reading: coverage governs the tree the review ran against, the fix rule governs the fix).

Then: Pilot upgrades to v5.2.0, and the milestone's proving continues on Pilot's build — which still carries the open ordered runs from the v5 era: a real four-persona piece with a user interface, and a full fresh-install lifecycle with one deliberately insufficient judgment sent back. Queued behind their triggers: the v11 converter · CI limit enforcement · the promise-conservation check.

## Evidence

- **The rewrite piece**, all of it in [work/builders-words.md](work/builders-words.md) and its four linked records (two testers, two judgment lines — extended, never rewritten, per contract v0.7): the 177-entry inventory committed before the first draft · Sol's draft in an isolated clone, merged with conductor corrections · review at e5494cf (both lines route back) · fix batches with every pre-fix control quoted and later re-executed by fresh hands · re-test and cold reads appended as follow-ups · both lines closing SUFFICIENT (line 1′ at 42f25e1; line 2″ at ebb9fb5, commit 29cc299) · dev suite: control arm 4/4 red re-run at three different hands; green arm 4/4 PASS on a clone pinned at e5494cf with a live codex driver, re-verified by three judges against the preserved runs · budgets at ebb9fb5: installed 17 files copied / 55,157 bytes of 100 KB (19 on disk of 20 after install writes the marker and starter map), always-read 24,198 bytes of 50 KB, 5 skills of 6, owner vocabulary 4 of 5 · the piece's falsifiable prediction recorded with its failed arm: first-move and cost questions held, the green arm held, the zero-undefined-terms target failed (six pre-existing terms made visible; every baseline term fixed).
- **The campaign adoption (v5.1.0)**: [work/campaign-adoption.md](work/campaign-adoption.md) and its records.
- **v5.0.0 and earlier**: [work/v5-hearing.md](work/v5-hearing.md), [docs/reviews/](docs/reviews/), the owner's verbatim rulings in [decisions.md](decisions.md).
