# speck-next · Product contract

The promises Speck Next makes, each with the check that can fail it. (v0.5 — how this document has been attacked and revised lives in [docs/reviews/](docs/reviews/).)

## The job

Given a product intent, help an agent understand what matters, build the next valuable piece, prove it works by running it, and leave the repository clearer than it found it. The owner brings intent, judgment, and product decisions. The method stays out of sight.

**What we optimize: great, shipped product per minute of owner attention.**

The whole method lives in four files, plus one page: `product.md` (what we're building, for whom, and what makes it good) · one small work file per piece of work · `decisions.md` (the big choices and why) · `state.md` (generated, never hand-written: what's true right now). The one page is `AGENTS.md` — the method itself, placed where every agent host loads it automatically; on-demand procedures are ordinary skills. The method ships only in forms agents natively load — never as documents an agent must be told about.

## The eight promises

Every promise names its check, and every check can fail.

1. **Iterative to the bone.** Work happens in small steps that each end in something you can run. The agent itself uses the product constantly while building — runs it, clicks through it, reads what it prints — and fixes what it finds. That loop is the engine; a demo reaches the owner only after the agent has used the thing itself, and owner steering rides on top of the loop, never replaces it. There is a hard budget on thinking-before-running: the minutes, tokens, and files spent before the product first runs are capped for every piece of work. When running for real would be irreversible (payments, live recipients, production data), the run happens against a named stand-in and the evidence says how faithful the stand-in is. *Check: the small-feature, bug-fix, and fuzzy-idea tasks (T02–T04) and the real-data task (T09) — budget held, proof of agent-run sessions before every demo, a logged owner steer that visibly changed the next step.*
2. **Small changes stay small.** A typo-sized change writes no method files at all, takes minutes, and touches `state.md` only if something true actually changed. Typo-sized is defined up front, not felt out: no new dependency, no auth, money, privacy, or data-integrity code touched, no promise rewritten, reversible in one commit. The agent may treat work as bigger than it looks, never smaller — and a change that turns out to touch protected code was never typo-sized; it gets the full loop, billed to that task, because the minutes-promise covers changes that really are small, not ones that pretended. When the call is genuinely unclear, the independent reviewer makes it, not the builder. *Check: the typo tasks (T01, T14) and the trap (T15) — a prompt that looks like a typo but sits on protected auth code; treating it as a typo is a scored miss.*
3. **Proof by running, judged by someone else.** Nobody grades their own homework. Every substantial piece of work is checked by a fresh reviewer that had no part in building it, and that reviewer runs the product — walks the flow, calls the API as the least-privileged user, tries to break it. Reading the code is not reviewing; a review with zero executed checks is itself a defect. A bug counts as caught only when it was reproduced by running the product, and a safety net counts as evidence only after it has been watched failing on purpose — a net that cannot fail catches nothing, and a tiny kernel check keeps that honest. *Check: the planted-bug tasks (T05–T10), scored per bug type against old Speck's frozen results — each with a clean twin, a matching task with no bug planted, so false alarms lose too.*
4. **The state file tells the truth.** `state.md` answers five questions in plain sentences: what is true now, what is blocked, what needs the owner, what happens next, and what evidence backs all of that. Four states: Shaped, Built, Proven, Live. Proven spells out the four verdicts separately — it works · it delivers the promise · it's good to use · the quality hangs together — each pointing at evidence or saying honestly "not judged yet", because one green word must never hide a taste failure. Overclaiming is a bug, and a small mechanical check hunts the flaggable kind: any state line claiming a verdict without pointing at evidence, and any phrase the product's own copy rules ban. *Check: the closing state of every task is audited; T17 probes a repo whose state file went stale.*
5. **Upgrading is 100% seamless, from any Speck version.** One command upgrades any Speck repository, from any era, in any condition — including mid-flight work. Concretely:
   - The upgrade never asks a human to fix anything by hand, and it never pretends: promises, decisions, open bugs, and unfinished work all come along.
   - Anything that can't be mapped cleanly is listed openly in `state.md` with a pointer to where it came from. Nothing lost, nothing silently dropped — a messy repository arrives as an honestly messy state.
   - Nothing already proven gets re-proven unless new claims outgrow the old evidence.
   - The upgrade is one commit that never sweeps in unrelated work, retries safely, and reverts cleanly; it leaves one marker the kernel refuses to run past until the upgrade is complete.
   - The only thing the upgrader may refuse is a repository whose era it genuinely cannot determine — and then it says exactly what it saw and what would settle the question, which is a short conversation, not repo surgery. Every repository that exists today is covered by test, so this case should never fire in practice.
   - Every piece of old-Speck knowledge lives inside the upgrader; the kernel carries none of it.

   *Check: the upgrade tasks (T11–T14, T18) on all five real repositories — including `odd` mid-epic, exactly as messy as it really is — plus constructed old-era repositories, verified against independent lists of everything alive in each repo, written before the upgrader existed.*
6. **Fun to drive, in plain language.** Building with speck-next should feel like watching a sharp colleague build your product, never like watching an agent recite an incantation. Three concrete things follow. Everything the owner reads or watches speaks product, not method: the docs, the state file, and what agents say while they work ("building the login screen — here's how it looks", never method ritual). Everything is understandable: a smart person who has never seen Speck can follow any document in this repository in one read, and the owner can answer the five state questions with no glossary. The system coins at most five words the **owner** must learn — counted as words a product person wouldn't already use; state names count, filenames don't (they're just files you open), and internal shorthand that never reaches the owner doesn't, because comprehension is the real measure. Today the count is four: Shaped, Built, Proven, Live. And fun is measured, not assumed: the owner rates the felt experience at every milestone — momentum, comprehension, enjoyment — and "felt like watching a foreign language" is a failing grade. This repository's own documents are held to the same bar; a reviewer who stumbles on our vocabulary files it as a defect. *Check: a method-speak audit on what agents say in owner-visible narration, a fresh-reader test on the docs, and the owner's felt rating at every milestone.*
7. **Small by law.** Hard limits in this repository's own CI, each with a test proving the limit can actually trip:
   - Installed into a product repo: **≤ 25 files / 250 KB**, counting every reachable capability, visible or not. (An upgraded repo's archived history is its own and sits outside this limit.)
   - What an agent always reads (`AGENTS.md` + `state.md` + `product.md`): **≤ 25 KB** — a swelling `product.md` is a broken limit, not a fact of life.
   - Durable method files per piece of work: **≤ 1** beyond the three shared files — and typo-sized work writes none.
   - End-to-end cost ceilings (tokens, minutes, owner interruptions) for typo-sized and small-feature work, enforced by running the benchmark in CI.

   A limit moves only in a new owner-approved version of this contract that names another limit tightening in exchange — and moving a limit can never rescue an experiment that already failed.
8. **It cannot quietly grow back.** The alarm is a number, not a memory: if more than 20% of a month's commits or tokens go to maintaining the method itself — counted mechanically by path (changes under the kernel and its docs are method work), never by anyone's judgment — development stops and subtracts first. One small table in this repository lists every kernel capability with the failure it prevents, what it costs, what proof it has earned (or the date by which it must earn it or retire), and what would retire it. No paperwork about the table, no copies in product repos. Every release names what it considered deleting. And if the kernel ever seems to need a context loader, receipts, or a compliance layer for itself — that is the old disease knocking; stop and subtract.

## What we refuse to trade away

Eight things no single check can fully capture, written down so every big decision weighs them (the test for each: could a decision quietly violate this while every check stays green?):

1. **Product excellence** — correct, on-promise, good to use, tasteful; strength in one never excuses weakness in another.
2. **Owner attention and peace** — the point of everything; more owner contact is not more virtue, and any decision adding owner touchpoints must show attention saved elsewhere.
3. **Iterative with the owner** — running product early, steering that matters.
4. **Care where the risk is** — small stays cheap, and risky paths never get to call themselves small.
5. **Smallness** — of the kernel, the vocabulary, and the paper trail.
6. **Seamless upgrades** — any Speck repo, any condition, everything carried, everything visible.
7. **Truth over theater** — evidence comes from running the product, and shipped work staying good counts too.
8. **Fun and understandability** — the owner never watches a foreign language; drag is a defect.

A decision is big enough to weigh against this list when it defers, simplifies, descopes, adds owner contact, or moves a limit.

## What stays out

Proving process compliance · carrying old-Speck compatibility in the kernel (the upgrader owns all of it) · installing adapters for every host (generate the one in use) · replacing the project's own tests and CI · writing the whole spec before building anything · shipping method-management machinery into product repos.

## Until it wins

Speck Next replaces Speck v11 only by beating it on the frozen contest in [docs/benchmark/fixtures.md](docs/benchmark/fixtures.md) — five checks that each pass or fail alone, plus one condition outside the benchmark: real use in a real product repository by 2026-10-01, or the thesis is dead regardless of scores. The contest file owns the full failure clause; this contract does not restate it.
