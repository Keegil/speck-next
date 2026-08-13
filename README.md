# speck-next

The clean-sheet successor to [Speck](https://github.com/telum-ai/speck): a small kernel that helps an agent build great products and prove they're great — by running them — while the method itself stays out of the owner's way.

**Status: no code yet, on purpose.** The [product contract](CONTRACT.md) is at v0.4 and has survived one round of attack review plus a closure check ([docs/reviews/](docs/reviews/)). Next comes the rules freeze for the benchmark, then the first real build — which has to beat Speck v11.2.0 head-to-head before this thing earns the job. The founding case lives in [telum-ai/speck#130](https://github.com/telum-ai/speck/issues/130).

## Why start over

Speck kept catching real, serious bugs — a crisis-support path that failed open, a forgeable audit log, workouts silently not saved behind a "Set logged." toast. Every single catch came from the same two moves: **someone independent attacking the work, and the real product actually being run.** Everything else grew into a methodology that mostly managed itself: 70 skills, 130 scripts, 53 coined terms, 3 MB installed into every repo, ~53k tokens of process to ship a 50-line feature, and no way to just fix a typo. Two serious slim-down attempts made it cheaper to load without making it smaller. So the two moves that worked keep their job, and everything else starts from zero and has to earn its way back.

## The promises, in one breath

Small steps that always end in something runnable. The agent uses the product itself, constantly — that loop is the engine, and the owner steers on top of it by reacting to running product, never by reading a spec corpus. Typo-sized changes cost minutes and zero paperwork. Independent reviewers run the product and try to break it; nobody grades their own homework. One honest state file. Upgrading from **any** Speck version is one command, keeps everything, hides nothing, and never asks for hand-repair. The whole thing stays small by CI-enforced law, speaks plain language, and is supposed to be **fun** — the owner should feel like they're watching a sharp colleague build their product, never like they're watching an agent speak a foreign language. Full text with the checks behind each: [CONTRACT.md](CONTRACT.md).

## What a session should feel like

A sketch, not a transcript — this is the bar the kernel gets judged against:

> **You:** People keep asking if the app can show who's coming tomorrow.
>
> **Agent:** On it. Smallest real version: a "Tomorrow" list on the studio dashboard. Building it now.
> …It runs — I've been clicking through it as a studio owner. Using it I noticed the list sits empty at midnight before data loads, and long names overflow on phones. Fixed both. Here's the demo — try tomorrow's view.
>
> **You:** *(two minutes of clicking)* Nice. Sort by class time, not alphabetically.
>
> **Agent:** Done, re-checked in the app. A fresh reviewer ran it too — tried to open another studio's list with a member login and couldn't. State: Built; Proven for "works" and "on-promise"; "good to use" checked on desktop and phone; nothing open. The next valuable piece looks like class reminders — want it?

No ceremony visible, no vocabulary to learn, and the product ran before anyone wrote a plan about it.

## The plan

1. **Evidence freeze — done.** Repositories, planted-bug types, tasks, and fairness rules, frozen before any kernel design: [docs/benchmark/fixtures.md](docs/benchmark/fixtures.md).
2. **Contract — done, v0.4.** Attacked by three independent reviewers (one from a different AI vendor) told to tear it apart; every blocking finding closed, and a separate verifier confirmed each fix actually landed. Then the owner failed v0.3 on language — it had started speaking methodology dialect — so v0.4 is the plain-language rewrite, tested on a fresh reader who had never seen Speck. That ruling is now constraint 4. All reviews preserved in full.
3. **Rules freeze — next.** Seven items, enumerated in the fixtures file, including: an independent defect-setter plants the bugs (plus secret extras), the scoring rules get locked and checksummed by an independent reviewer, v11's baseline gets measured at full strength, and the repo snapshots become portable.
4. **First real build,** judged against Speck v11.2.0 on the frozen tasks — at least three runs per task, per-bug-type scoring, an independent judge.
5. **Decide with data.** The contract can fail; its failure clause includes a hard one: if no real product repo is doing real work on speck-next by **2026-10-01**, the thesis is dead no matter what the benchmark says.

While the experiment runs, Speck v11 stays the method of record and takes bug fixes only, no new features, so the fallback can't rot.
