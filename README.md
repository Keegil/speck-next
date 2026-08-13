# Speck Next

Speck Next is a small kernel — a few files and one page of instructions — that helps an agent build a great product and prove it's great by running it. The owner says what they want and reacts to running product. The method stays out of sight.

## What a session feels like

> **You:** People keep asking if the app can show who's coming to tomorrow's classes.
>
> **Agent:** On it. Smallest real version: a "Tomorrow" list on the studio dashboard. Building it now.
> …It runs — I've been clicking through it as a studio owner. Using it I noticed the list sits empty at midnight before data loads, and long names overflow on phones. Fixed both. Here's the demo — try tomorrow's view.
>
> **You:** *(two minutes of clicking)* Nice. Sort by class time, not alphabetically.
>
> **Agent:** Done, re-checked in the app. A fresh reviewer ran it too — tried to open another studio's list with a member login and couldn't. State: Built; Proven for "works" and "on-promise"; "good to use" checked on desktop and phone; nothing open. The next valuable piece looks like class reminders — want it?

No ceremony visible, no vocabulary to learn, and the product ran before anyone wrote a plan about it.

## How it works

**One loop, any size.** Shape the piece of work, build it, prove it by running it, leave the state clear. The same loop covers a typo, a feature, and a product — there are no separate command families for different sizes of work.

**The agent uses the product, constantly.** While building, the agent runs the thing, clicks through it, reads what it prints, and fixes what it finds. That loop is the engine. A demo reaches you only after the agent has used it itself, and your steering rides on top — it never replaces the agent's own testing.

**Everything on disk is four files and a page.** `product.md` — what we're building, for whom, and what makes it good. One small work file per piece of work. `decisions.md` — the big choices and why. `state.md` — generated, never hand-written: what's true, what's blocked, what needs you, what happens next, and the evidence. Plus the doctrine: the one page of instructions an agent always reads.

**Four states, honest ones.** Shaped, Built, Proven, Live. Proven spells out four verdicts separately — it works, it delivers the promise, it's good to use, the quality hangs together — each pointing at evidence or saying plainly "not judged yet". Those four words are the entire vocabulary you need.

**Nobody grades their own homework.** Substantial work is checked by a fresh reviewer that had no part in building it — and the reviewer runs the product: walks the flow, calls the API as the least-privileged user, tries to break it. Reading the code doesn't count. A safety net counts as evidence only after it's been watched failing on purpose.

**Small changes stay small.** A typo-sized fix takes minutes and writes no method files at all. What counts as typo-sized is defined up front (no new dependency; no auth, money, privacy, or data-integrity code; reversible in one commit) — and the agent may treat work as bigger than it looks, never smaller.

**Extra care exactly where the risk is.** Money, auth, private data, and regulated paths switch on extra-care packs. Risky work never gets to call itself small; everything else stays light.

**Upgrading from any Speck is one command.** Any version, any condition, even mid-work, even a dirty tree. Everything comes along — promises, decisions, open bugs, unfinished work — and anything that can't be mapped cleanly shows up as an open item in `state.md` with a pointer to where it came from. Nothing lost, nothing hidden, no hand-repair, one revertible commit. All knowledge of old Speck lives in the upgrader; the kernel carries none of it.

**It stays small and plain, by law.** Hard CI limits on everything installed (≤ 25 files), on what an agent always reads (≤ 25 KB), and on paperwork per piece of work (≤ 1 file, zero for typos). At most five coined words, ever; four are used. If method-maintenance ever exceeds 20% of a month's work, development stops and subtracts. And it's supposed to be fun — you should feel like you're watching a sharp colleague build your product, and you grade that feeling at every milestone.

The full promises, each with the check that can fail it: [CONTRACT.md](CONTRACT.md).

## Status

Being built — the kernel is taking shape in [kernel/](kernel/), not usable in real products yet. Before Speck Next may replace Speck v11 it must beat it head-to-head on a contest frozen before design started: [docs/benchmark/fixtures.md](docs/benchmark/fixtures.md). The contest can't run until its scoring rules are locked by an independent reviewer, and the planted bugs stay secret from everyone building the kernel. Why the clean sheet, and what happened to v11's machinery: [docs/history/](docs/history/). How these documents have been attacked and revised: [docs/reviews/](docs/reviews/).
