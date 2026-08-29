# State

## What's true now

The kernel is at **v5.3.0**, and its vocabulary is defined: a full census of the 124 rule-carrying terms across the loaded pages leaves exactly one word undefined — `sufficient`, which is the owner's sentence to write (below). Every page an agent loads is written in a builder's words: the method page (`AGENTS.md`), five skills — `shape-product`, `map-build`, `craft`, `experience`, `judge` — with four references, six template skeletons, and the installer. The method's shape: five phases, shape → map → build → experience → judge, where the last two are one review — fresh testers use the product and decide as users do, and a judge who built and tested nothing challenges every verdict before it counts. States: Shaped → Built → Judged → Live, with *proven* as plain speech for all four rulings standing on evidence.

The rewrite piece ("A builder's words, and fewer of them") is **landed**: the installed surface went from 70,770 bytes to 56,039 at its landing commit (the sum of `git cat-file -s` over the installer's own file list at ebb9fb5 — the earlier recorded 55,157 was a working-tree read at the wrong moment, corrected under the measured-numbers rule), mean sentence length from 24.4 to 13.3 words, all 177 operative rules conserved and verified by executed probes, nine old method words at zero, and the sentences the last piece's judges ordered are in: the thinking cap, the honest cost line, the three receipt-gate fixes. The contract stands at v0.7 (hearing records counted separately, capped at six per review, re-hearings extend records). A cold reader who had never seen Speck ruled the pages "buildable, and I would want to build under it," computed the full review cost unaided, and named `craft` the plainest file in the set.

## What's wearing out

- **The piece's report of itself.** Eight bites across three pieces, every one caught by a fresh context or a judge, never by the author — false closure claims, uncommanded numbers, one-sided edits reported as complete, a corrected figure left standing in the file that outranks the corrected one. The producer landed by the definitions piece (claims and measured numbers carry their commands) already caught three of the later bites; judge 2″ named the residue exactly: **the judge's quoted control becomes the builder's requirement** — every one-sided edit traces to executing the quoted grep instead of the sentence above it. The three-producers piece is this strain's repair.
- **Byte-exact self-measurements in this file.** Stale the moment this file is rewritten; figures are pinned to the commit they were measured at; a computed check would retire the strain for good.

Retired by the rewrite piece, bar met and measured: **the kernel only grows** — 70,770 → 56,039 bytes at its landing commit (`git cat-file -s` summed over the installer's file list at ebb9fb5), the first shrink in the kernel's history. Retired earlier the same day: the receipt law and the stdin-hanging dispatches (bitten twice pre-v4, held through every review since).

## What's blocked

Nothing.

## What needs the owner

Two questions, filed by both of the definitions piece's judgment lines with full context in [work/name-the-words.md](work/name-the-words.md):

1. **Protected code — how wide is the wall?** Keep the wide list (every schema change and irreversible action reviewed on its own — both lines recommend it), narrow back to the old four, or judge 1's middle (protect data-correctness code only where it can lose or corrupt stored records).
2. **What makes a judgment "sufficient"?** The one undefined word left, and it decides whether work ships. Both lines recommend: the judge may land a piece while naming, in this file, everything that stays open and where it went.

Standing, non-blocking: the v5-era fixture milestone's felt grade ([work/v5-hearing.md](work/v5-hearing.md)).

## What happens next

**"Name the words" is landed — both judgment lines closed sufficient after two obeyed route-backs ([work/name-the-words.md](work/name-the-words.md)).** Ten definitions across three rounds, the self-report producer in law (claims and measured numbers carry their commands), the document-piece deadlock gone, the review-admission gate failing closed on a verified anchor, and the mid-review rules agreeing in all three homes. **No piece is live.** The next kernel piece, converged by both judgment lines and all four tester runs, is **three producers** — the same edit lands in every home a rule lives in · a new load-bearing word gets its sentence when written · a judge's control names its population, never just the site the defect surfaced at — and it waits on the owner's word, alongside his two questions below.

Then: the milestone's proving continues on Pilot's build — which still carries the open ordered runs from the v5 era: a real four-persona piece with a user interface, and a full fresh-install lifecycle with one deliberately insufficient judgment sent back. Queued behind their triggers: the v11 converter · CI limit enforcement · the promise-conservation check.

## Evidence

- **The rewrite piece**, all of it in [work/builders-words.md](work/builders-words.md) and its four linked records (two testers, two judgment lines — extended, never rewritten, per contract v0.7): the 177-entry inventory committed before the first draft · Sol's draft in an isolated clone, merged with conductor corrections · review at e5494cf (both lines route back) · fix batches with every pre-fix control quoted and later re-executed by fresh hands · re-test and cold reads appended as follow-ups · both lines closing SUFFICIENT (line 1′ at 42f25e1; line 2″ at ebb9fb5, commit 29cc299) · dev suite: control arm 4/4 red re-run at three different hands; green arm 4/4 PASS on a clone pinned at e5494cf with a live codex driver, re-verified by three judges against the preserved runs · budgets at ebb9fb5: installed 17 files copied / 56,039 bytes of 100 KB by the pinned measure above (19 on disk of 20 after install writes the marker and starter map), always-read 24,198 bytes of 50 KB, 5 skills of 6, owner vocabulary 4 of 5 · the piece's falsifiable prediction recorded with its failed arm: first-move and cost questions held, the green arm held, the zero-undefined-terms target failed (six pre-existing terms made visible; every baseline term fixed).
- **The definitions piece (v5.3.0)**, all of it in [work/name-the-words.md](work/name-the-words.md) and its four linked records: ten definitions across three rounds, each surviving a fresh cold read · the 124-term census with its enumeration procedure in the tester's record · twenty fresh-context runs, two obeyed route-backs, both judgment lines closing sufficient on b8e2ce9 with their conditions carried in the release commit · every figure pinned to its command · control arm 4/4 red at every round, at three different hands.
- **The campaign adoption (v5.1.0)**: [work/campaign-adoption.md](work/campaign-adoption.md) and its records.
- **v5.0.0 and earlier**: [work/v5-hearing.md](work/v5-hearing.md), [docs/reviews/](docs/reviews/), the owner's verbatim rulings in [decisions.md](decisions.md).
