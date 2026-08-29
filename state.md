# State

## What's true now

The kernel is at **v5.2.1**. Every page an agent loads is written in a builder's words: the method page (`AGENTS.md`), five skills — `shape-product`, `map-build`, `craft`, `experience`, `judge` — with four references, six template skeletons, and the installer. The method's shape: five phases, shape → map → build → experience → judge, where the last two are one review — fresh testers use the product and decide as users do, and a judge who built and tested nothing challenges every verdict before it counts. States: Shaped → Built → Judged → Live, with *proven* as plain speech for all four rulings standing on evidence.

The rewrite piece ("A builder's words, and fewer of them") is **landed**: the installed surface went from 70,770 bytes to 56,039 at its landing commit (the sum of `git cat-file -s` over the installer's own file list at ebb9fb5 — the earlier recorded 55,157 was a working-tree read at the wrong moment, corrected under the measured-numbers rule), mean sentence length from 24.4 to 13.3 words, all 177 operative rules conserved and verified by executed probes, nine old method words at zero, and the sentences the last piece's judges ordered are in: the thinking cap, the honest cost line, the three receipt-gate fixes. The contract stands at v0.7 (hearing records counted separately, capped at six per review, re-hearings extend records). A cold reader who had never seen Speck ruled the pages "buildable, and I would want to build under it," computed the full review cost unaided, and named `craft` the plainest file in the set.

## What's wearing out

- **The piece's report of itself.** Five bites across two pieces, every one caught by a fresh context or judge, never by the author — a false closure claim, an unreproducible control, the piece's own re-entry law unobeyed by its fix batch, a protected-gate fix mislabeled a small change, and this file going stale twice inside one review. The judges' sharpening: the next piece owes a **producer** for self-report and self-classification, not another detector — a classification rule whose only trigger is the builder feeling unsure has no trigger at all.
- **Byte-exact self-measurements in this file.** Stale the moment this file is rewritten; figures are pinned to the commit they were measured at; a computed check would retire the strain for good.

Retired by the rewrite piece, bar met and measured: **the kernel only grows** — 70,770 → 56,039 bytes at its landing commit (`git cat-file -s` summed over the installer's file list at ebb9fb5), the first shrink in the kernel's history. Retired earlier the same day: the receipt law and the stdin-hanging dispatches (bitten twice pre-v4, held through every review since).

## What's blocked

Nothing.

## What needs the owner

Nothing waiting. All seven questions from the two reviews were answered the same day (his calls verbatim in decisions.md, 2026-08-29 night): the next piece defines the words · Live is per milestone · the war stories stay with his scar restored · README and docs swept · the git audit moved to the judge · the kernel-versus-nothing measurement was run rather than queued (3 of 4 without the pages, 4 of 4 with — the miss was scope sprawl on a typo-sized fix). Standing, non-blocking: the v5-era fixture milestone's felt grade ([work/v5-hearing.md](work/v5-hearing.md)).

## What happens next

**The live piece: "Name the words" — routed back twice, fixed both times; the re-fixed pages are Built as of this commit ([work/name-the-words.md](work/name-the-words.md)).** Four words get one-sentence definitions (Shaped · care level · straining versus fighting · "its own checks"), two resolve by ruling or deletion (Live's boundary is ruled; "captioned screen drawing" is the deletion candidate), and self-reports get a producer: a closure claim carries the runnable command that proves it. It consumes the two inherited method items (the never-run exemption clause; the mid-review-fix silence, resolved once on the record).

Then: the milestone's proving continues on Pilot's build — which still carries the open ordered runs from the v5 era: a real four-persona piece with a user interface, and a full fresh-install lifecycle with one deliberately insufficient judgment sent back. Queued behind their triggers: the v11 converter · CI limit enforcement · the promise-conservation check.

## Evidence

- **The rewrite piece**, all of it in [work/builders-words.md](work/builders-words.md) and its four linked records (two testers, two judgment lines — extended, never rewritten, per contract v0.7): the 177-entry inventory committed before the first draft · Sol's draft in an isolated clone, merged with conductor corrections · review at e5494cf (both lines route back) · fix batches with every pre-fix control quoted and later re-executed by fresh hands · re-test and cold reads appended as follow-ups · both lines closing SUFFICIENT (line 1′ at 42f25e1; line 2″ at ebb9fb5, commit 29cc299) · dev suite: control arm 4/4 red re-run at three different hands; green arm 4/4 PASS on a clone pinned at e5494cf with a live codex driver, re-verified by three judges against the preserved runs · budgets at ebb9fb5: installed 17 files copied / 56,039 bytes of 100 KB by the pinned measure above (19 on disk of 20 after install writes the marker and starter map), always-read 24,198 bytes of 50 KB, 5 skills of 6, owner vocabulary 4 of 5 · the piece's falsifiable prediction recorded with its failed arm: first-move and cost questions held, the green arm held, the zero-undefined-terms target failed (six pre-existing terms made visible; every baseline term fixed).
- **The campaign adoption (v5.1.0)**: [work/campaign-adoption.md](work/campaign-adoption.md) and its records.
- **v5.0.0 and earlier**: [work/v5-hearing.md](work/v5-hearing.md), [docs/reviews/](docs/reviews/), the owner's verbatim rulings in [decisions.md](decisions.md).
