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
> **Agent:** Done, re-checked in the app. Fresh eyes used it too — a witness walked it cold as a brand-new studio owner and tried to open another studio's list with a member login; a separate judge read that walk and ruled it: works, on-promise, good to use on desktop and phone. Nothing open. The next valuable piece looks like class reminders — want it?

No ceremony visible, no vocabulary to learn, and the product ran before anyone wrote a plan about it.

## How it works

**Five phases, always checkable.** The product moves shape → map → build → experience → judge: shaping is an owner conversation in numbered rounds that produces `product.md` and whatever material the product needs; mapping is the second conversation, cutting the ordered pieces and deciding the substrate; building runs one piece at a time through its own tight micro-loop; experiencing sends fresh witnesses to live each finished milestone on the real surface — the first-timer, the real job, the worst day — writing down what happened without ruling on it; judging is a separate head ruling from those records, and the owner grading how it feels. Every phase has a checkable exit that includes the owner's ratification in his own words, transitions fire automatically and are named out loud, and a ruling, finding, or judgment can re-enter any earlier phase — with a trace.

**The agent uses the product, constantly.** While building, the agent runs the thing, clicks through it, reads what it prints, and fixes what it finds. That loop is the engine. A demo reaches you only after the agent has used it itself, and your steering rides on top — it never replaces the agent's own testing.

**Everything on disk is five files and a page.** `product.md` — what we're building, for whom, and what makes it good. `map.md` — the ordered build pieces, each naming what it serves and which shaped material it consumes (deck frames, model sections), exactly one live; shaping's outputs are the build's inputs, and unconsumed gold stays visible at the map's bottom. One small work file per piece of work. `decisions.md` — the big choices and why. `state.md` — generated, never hand-written: what's true, what's wearing out, what's blocked, what needs you, what happens next, and the evidence. The page is `AGENTS.md` — the method itself, sitting where every agent host already loads it automatically. On-demand procedures are ordinary skills. There is nothing for an agent to be told to go read.

**Four states, honest ones.** Shaped, Built, Judged, Live. Judged spells out four verdicts separately — it works, it delivers the promise, it's good to use, the quality hangs together — each pointing at evidence or saying plainly "not judged yet". When all four stand on evidence, the work is proven — ordinary English, not another state — and proven work is what goes Live. Those four words are the entire vocabulary you need.

**Nobody grades their own homework — and nobody grades what they gathered.** An agent sent to *prove* something bends its evidence toward the verdict, so the job is split in two. Fresh witnesses who had no part in building live the product — walk it cold, do the real job, log in as the least-privileged user, have the worst day — and write down exactly what happened, with no verdicts allowed in the record. Then a separate judge who ran none of it rules from those records, and orders another walk when a ruling would otherwise rest on a gap. Reading the code doesn't count as witnessing, and a safety net counts as evidence only after it's been watched failing on purpose.

**Small changes stay small.** A typo-sized fix takes minutes and writes no method files at all. What counts as typo-sized is defined up front (no new dependency; no auth, money, privacy, or data-integrity code; reversible in one commit) — and the agent may treat work as bigger than it looks, never smaller.

**Small loops don't get to stack jank.** Every time work goes *around* something instead of through it, a strain line lands in `state.md` — pain has a place to accumulate, so it survives between sessions. Shaping starts by reading that list: strain recorded twice becomes the next piece or gets deferred where you can see it. The judge rules on the whole's structure, not just the piece — sound, straining, or fighting — and two straining rulings in a row force structural work, a call that belongs to the judge because the builder always has momentum. And predictable foundations (a design system, the data model, real infrastructure) are named at shaping time with the trigger that makes each one due — built when their moment fires, not upfront on fiction, never not at all.

**Extra care exactly where the risk is.** Money, auth, private data, and regulated paths switch on extra-care packs. Risky work never gets to call itself small; everything else stays light.

**Upgrading from any Speck is one command.** Any version, any condition, even mid-work, even a dirty tree. Everything comes along — promises, decisions, open bugs, unfinished work — and anything that can't be mapped cleanly shows up as an open item in `state.md` with a pointer to where it came from. Nothing lost, nothing hidden, no hand-repair, one revertible commit. All knowledge of old Speck lives in the upgrader; the kernel carries none of it.

**It stays small and plain, by law.** Hard limits in the contract: ≤ 20 files installed (today: 18, measured), ≤ 6 skills (five exist), ≤ 50 KB always read (a deeply-shaped `product.md` earns its weight; narration doesn't, at any size), ≤ 1 method file per piece of work and zero for typos. At most five coined words, ever; four are used. If method-maintenance ever exceeds 20% of a month's work, development stops and subtracts. CI enforcement of the limits is on the open list in [state.md](state.md) — until it lands, the numbers hold by measurement, not by machine. And it's supposed to be fun — you should feel like you're watching a sharp colleague build your product, and you grade that feeling at every milestone.

The full promises, each with the check that can fail it: [CONTRACT.md](CONTRACT.md).

## Status

At v4 — proving redesigned into experience → judge on the owner's ruling that agents sent to prove act dysfunctionally, on top of v3's full sequence discipline — and self-hosted: this repository runs under its own [AGENTS.md](AGENTS.md), so every development session here is a live test of the method. Every dev-suite check is proven able to fail before any green counts ([devsuite/](devsuite/) — including its own honest note on what a green run does and doesn't prove). v1 is accepted on demonstrated confidence — owner decision — with its target the greenfield reboot of a real product; the designed head-to-head contest is shelved but kept ([docs/benchmark/fixtures.md](docs/benchmark/fixtures.md)). Current truth, open list, and next steps: [state.md](state.md). Why the clean sheet: [docs/history/](docs/history/). How these documents were attacked: [docs/reviews/](docs/reviews/).
