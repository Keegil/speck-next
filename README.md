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

**Four phases, always checkable.** The product moves shape → map → build → prove: shaping is an owner conversation in numbered rounds that produces `product.md` and whatever material the product needs; mapping is the second conversation, cutting the ordered pieces and deciding the substrate; building runs one piece at a time through its own tight micro-loop; proving walks each finished milestone on the real surface, and the owner grades how it feels. Every phase has a checkable exit that includes the owner's ratification in his own words, transitions fire automatically and are named out loud, and a ruling or finding can re-enter any earlier phase — with a trace.

**The agent uses the product, constantly.** While building, the agent runs the thing, clicks through it, reads what it prints, and fixes what it finds. That loop is the engine. A demo reaches you only after the agent has used it itself, and your steering rides on top — it never replaces the agent's own testing.

**Everything on disk is five files and a page.** `product.md` — what we're building, for whom, and what makes it good. `map.md` — the ordered build pieces, each naming what it serves and which shaped material it consumes (deck frames, model sections), exactly one live; shaping's outputs are the build's inputs, and unconsumed gold stays visible at the map's bottom. One small work file per piece of work. `decisions.md` — the big choices and why. `state.md` — generated, never hand-written: what's true, what's wearing out, what's blocked, what needs you, what happens next, and the evidence. The page is `AGENTS.md` — the method itself, sitting where every agent host already loads it automatically. On-demand procedures are ordinary skills. There is nothing for an agent to be told to go read.

**Four states, honest ones.** Shaped, Built, Proven, Live. Proven spells out four verdicts separately — it works, it delivers the promise, it's good to use, the quality hangs together — each pointing at evidence or saying plainly "not judged yet". Those four words are the entire vocabulary you need.

**Nobody grades their own homework.** Substantial work is checked by a fresh reviewer that had no part in building it — and the reviewer runs the product: walks the flow, calls the API as the least-privileged user, tries to break it. Reading the code doesn't count. A safety net counts as evidence only after it's been watched failing on purpose.

**Small changes stay small.** A typo-sized fix takes minutes and writes no method files at all. What counts as typo-sized is defined up front (no new dependency; no auth, money, privacy, or data-integrity code; reversible in one commit) — and the agent may treat work as bigger than it looks, never smaller.

**Small loops don't get to stack jank.** Every time work goes *around* something instead of through it, a strain line lands in `state.md` — pain has a place to accumulate, so it survives between sessions. Shaping starts by reading that list: strain recorded twice becomes the next piece or gets deferred where you can see it. The independent reviewer judges the whole's structure, not just the piece — sound, straining, or fighting — and two straining verdicts in a row force structural work, a call that belongs to the reviewer because the builder always has momentum. And predictable foundations (a design system, the data model, real infrastructure) are named at shaping time with the trigger that makes each one due — built when their moment fires, not upfront on fiction, never not at all.

**Extra care exactly where the risk is.** Money, auth, private data, and regulated paths switch on extra-care packs. Risky work never gets to call itself small; everything else stays light.

**Upgrading from any Speck is one command.** Any version, any condition, even mid-work, even a dirty tree. Everything comes along — promises, decisions, open bugs, unfinished work — and anything that can't be mapped cleanly shows up as an open item in `state.md` with a pointer to where it came from. Nothing lost, nothing hidden, no hand-repair, one revertible commit. All knowledge of old Speck lives in the upgrader; the kernel carries none of it.

**It stays small and plain, by law.** Hard limits in the contract: ≤ 15 files installed (today: 17 — v3's templates broke this limit; the trade is on the owner's desk), ≤ 50 KB always read (a deeply-shaped `product.md` earns its weight; narration doesn't, at any size), ≤ 1 method file per piece of work and zero for typos. At most five coined words, ever; four are used. If method-maintenance ever exceeds 20% of a month's work, development stops and subtracts. CI enforcement of the limits is on the open list in [state.md](state.md) — until it lands, the numbers hold by measurement, not by machine. And it's supposed to be fun — you should feel like you're watching a sharp colleague build your product, and you grade that feeling at every milestone.

The full promises, each with the check that can fail it: [CONTRACT.md](CONTRACT.md).

## Status

At v3 — full sequence discipline, built from two real campaign failures and the owner's ratified design — and self-hosted: this repository runs under its own [AGENTS.md](AGENTS.md), so every development session here is a live test of the method. Every dev-suite check is proven able to fail before any green counts ([devsuite/](devsuite/) — including its own honest note on what a green run does and doesn't prove). v1 is accepted on demonstrated confidence — owner decision — with its target the greenfield reboot of a real product; the designed head-to-head contest is shelved but kept ([docs/benchmark/fixtures.md](docs/benchmark/fixtures.md)). Current truth, open list, and next steps: [state.md](state.md). Why the clean sheet: [docs/history/](docs/history/). How these documents were attacked: [docs/reviews/](docs/reviews/).
