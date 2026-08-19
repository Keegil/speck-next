---
name: experience
description: Dispatches fresh witnesses who live the product in personas — the first-timer, the real job, the second user, the worst day — and write records of what happened, with no verdicts in them. For shaping artifacts, the witness probes the artifact against the owner's record and the wire. Use on every substantial piece after building it, and at every milestone, always before the judge.
---

# experience

**Why this is its own skill:** an agent sent to prove something bends its evidence toward the verdict. So the one who lives the product never rules — the witness gathers, and the `judge` skill rules from what came back. Keep the stances apart and both stay honest.

**The witness is a genuinely separate context, and there is a receipt.** Nothing else here matters if this part is faked: a walk performed by the builder in its own head is void, and writing "a fresh witness used this" without the receipt below is fabricated evidence — the worst defect class this method knows.

**Dispatch, concretely.** In Claude Code: launch a subagent (the Agent tool, fresh context, a different model when available). On any host: `codex exec --sandbox workspace-write -C <fresh clone>` or another agent CLI, run against a clean clone — never your working tree. Give the witness the product files, the promises from `product.md`, and this skill's files — never your own summary of what you built.

**The receipt opens at dispatch, or it is void.** Before the witness runs, the work file records: who is witnessing (tool, model, session), when and at what commit it was dispatched, the personas planned, the walks and commands planned — plus two lines that keep receipts from colliding: *who owns this run* (which session dispatched it), and *what a later session does on finding the record empty* (re-dispatch under its own named line, never assume the run died — two witnesses once executed one dispatch in parallel, neither knowing of the other). The record is appended when it returns, verbatim or linked. A receipt reconstructed at closure is exactly what a builder writes when nothing forced the capture — it does not count, twice proven. No dispatch-time receipt, no record, nothing for the judge to rule on.

**The stance: live it, record it, rule nothing.** The record says what was done and what happened — the exact commands, what appeared, what changed where, screenshots actually looked at with at least two pointed-at-the-pixels observations each. Feelings are reported as felt, in persona ("I couldn't tell what this screen wanted from me"), never converted into pass or fail. No verdict words: the record never says kept, broken, passed, failed, good, or proven — a record that rules is void like an unreceipted one, because a witness that grades starts bending what it gathers. Anything the witness couldn't run is recorded as untested — never converted into a pass, never silently dropped. The record must be checkable against its transcript.

**The personas.** A substantial piece gets the first two at least; a milestone gets all four:

1. **The first-timer** — cold start: real build, fresh install or cleared storage, logged out, knows nothing. At the first screen, answer from the pixels alone: what is this, who's asking, why now? For anything with a user interface, walk `references/walk.md`.
2. **The worker** — the real job, end to end, through the product's own surface (a harness the builder wrote is not the product), reading what it prints, chasing each claimed save/send/generate to its mechanism — the request, the changed record, the read-back — and recording what was found or couldn't be found.
3. **The second user** — a least-privileged real account attempting what it shouldn't reach, and a second person on the same install looking for traces of the first.
4. **The worst day** — everything hostile and unlucky at once: `references/worst-day.md`.

**Shaping artifacts get witnessed too.** When the work is a `product.md` draft, a domain model, journeys, a deck — the product may not run yet, so the subjects change and the stance stands: the witness still executes, but what it executes are probes against the wire fixtures, greps against the repo, and checks against the owner's verbatim shaping record — never a read of sibling documents against each other, because a document corpus drifts into perfect agreement with itself. It records side by side what the artifact says and what the record, the wire, or the repo says ("the record of 2026-08-14 has the owner saying X; the artifact says Y") — including a cold read of every owner-facing artifact as a smart outsider, recording each place it stumbled. Contradiction and stumble are observations; whether they break anything is the judge's call. A shaping record whose transcript shows zero executed probes is discarded like any other.

**What comes back:** the record — runs, observations, felt reports in persona, screenshots, mechanisms found or missing, limits hit — appended to the receipt. Then the `judge` skill rules. The witness never does.
