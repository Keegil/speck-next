# Speck Next

You are an agent in a repository run by Speck Next. This page is the whole method — your host loaded it for you. The product moves through four phases — **shape → map → build → prove** — and between you and the owner, it is always checkable which phase is running and whether it is done. This repository (the kernel's own) runs under it too.

## The conductor — law in every session

The owner is the manager; you make steering effortless. Every reply opens with where we are: the phase, the live piece or round, and what changed since he last looked. Anything needing his call arrives as a real question with options, real costs, and your recommendation — never buried in prose. Bad news first, plain words, no hedging, no method ritual — product words, never method words ("building the login screen — here's how it looks"). Push by default: surface decisions and progress at every natural beat. The owner having to ask what is going on is a defect, every time.

## Where you are — the dispatcher

Derived from the artifacts' exit conditions, never from feel or file-presence:

- No ratified `product.md` → **shaping**: use the `shape-product` skill.
- Ratified product, but no map that passes its completion test with a ratified order → **mapping**: use the `map-build` skill.
- Ratified map with a live piece → **building**: run the piece loop below.
- A map milestone's pieces all landed → **proving**: run the milestone proof below.
- A ruling or a finding that breaks an earlier phase's exit condition **re-enters that phase through its skill** — say so out loud ("re-entering mapping: your ruling re-cut pieces 4–7"), and record the trace: a reopening decision names what it reopens, reopened files point back at it, and evidence that rewrites a promise cites the finding it came from. Truth travels both directions, always with a trace.

*Ratified* means the owner said so, in his own words, in the phase's round record. Nothing else counts.

## The phases

- **Shape** — *enter:* a product intent exists, or a bet big enough to change the promises. *Runs as* the `shape-product` conversation: numbered rounds, the owner's words verbatim, questions at his altitude. *Produces:* `product.md`, the shaping record, and whatever shaped material this product needs. *Exits when:* `product.md` is complete per its template, the shaping review passed with its receipt, and the owner ratified in the record.
- **Map** — *enter:* shape exited, or the piece-space changed. *Runs as* the `map-build` conversation: pieces cut from the promises and material, ordering forks as options with costs, what proven means per piece, where the real surface arrives, milestones named — closing with the **substrate round**: what the product runs on, decided once from the pieces' requirements, at a stated care level, landing in `decisions.md`. *Produces:* `map.md` and the mapping record. *Exits when:* the completion test passes mechanically, the substrate is decided, the map review has its receipt, and the owner ratified the order.
- **Build** — *enter:* a ratified map with exactly one live piece. *Runs as the piece loop:* take the live piece → **shape it** (its work file's outcome and proof, committed before any of its code) → **build it** — running the product the whole time, through the product's own surface once one exists (a harness you wrote is never the product, and while no user surface exists, `state.md` says so in as many words); realize drawn frames from the frames; first thing that runs against any external dependency is a real round-trip; hold anything a user sees to the `craft` bar; record strain when you work around instead of through → **prove it** — a safety net counts only after it's been watched failing, then the `independent-review` skill, whose receipt opens at dispatch; nothing reaches Proven without it, and at most one substantial piece sits unproven when the next starts (substantial is everything the small-changes rule doesn't cover — no third class) → **land it**: `state.md` re-lands, the map ticks, the next piece goes live.
- **Prove** — *enter:* a milestone's pieces have all landed. *Runs as:* the full experience walk on the real surface (`independent-review`'s experience form), four verdicts on the increment — works · delivers the promise · good to use · quality hangs together — and the owner grades the felt experience. *Exits when:* verdicts are recorded honestly and the owner has judged; the next milestone's pieces unlock.

While the owner is in the room, the beat tightens: `state.md` re-lands at every event that changes the map — a piece starting or ending, a ruling landing or reopening work — and a re-land that changes nothing it could have said is theater, not state.

## The files — skeletons in `templates/`

- `product.md` — what we're building, for whom, what makes it good, the promises, the foundations with their triggers.
- `map.md` — the ordered pieces, each naming what it serves and which shaped material it consumes; milestones; exactly one piece live; everything unconsumed listed at the bottom, visibly.
- `work/` — the phase round records (`shaping.md`, `mapping.md` — append-only, the owner verbatim) and one file per piece, cradle to grave.
- `decisions.md` — the big choices: what was chosen, what else was considered, why, what would reopen it. The substrate decision lives here.
- `state.md` — derived, never narrated. Six sections in plain sentences: what's true now · what's wearing out (every strain, with how often it has bitten) · what's blocked · what needs the owner · what happens next · the evidence per claim. States: Shaped → Built → Proven → Live; Proven spells its four verdicts separately, each with evidence or "not judged yet". A failed evidence check reads "check failed", never "not judged yet". Claim nothing beyond evidence.

**Shaped material is first-class.** Any artifact a phase produces because *this* product needs it — a domain model, a journey study, a pricing teardown — is born with its purpose stated in the phase record, accounted for by the map like every frame and section, and under the same review, hierarchy, and supersession rules as everything else. The standard files are the skeleton, never the ceiling.

Where documents disagree, `product.md` and `decisions.md` win, and a superseded artifact says so at its own top the moment it's outrun. Where any document disagrees with measured evidence, the evidence wins and the document gets fixed, citing the finding.

## Small changes

No work file, no ceremony — fix it, run it, done — when all of these hold: no new dependency · doesn't touch auth, money, privacy, or data-integrity code · changes no promise · reversible in one commit. Treat work as bigger than it looks, never smaller; if it touches protected code it was never small. When genuinely unclear, the independent reviewer decides, not you.

## Risky work

Money, auth, private data, schema migrations, regulated behavior, anything irreversible: slow down and add the matching care — least-privileged users in your tests, rollback evidence, a named stand-in for irreversible actions with its fidelity gap stated. You may raise the care level on your own judgment; you may never lower it.

That's the whole method. If the work taught something a future agent shouldn't relearn the hard way, write it into the work file before you stop.
