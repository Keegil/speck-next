# Experiencer record — the worst day

**Persona:** The worst day — everything inconsistent, stale, or self-contradictory arrives at once.

**Subject:** Speck Next kernel surface at commit `586a87a943dde20989142d11973b09f0f4df2b35`.

**Stance:** I had no part in building this surface. I ran the probes, recorded what happened, and make no claim beyond those runs.

## Baseline

Command:

```text
git rev-parse HEAD
```

Output:

```text
586a87a943dde20989142d11973b09f0f4df2b35
```

Command:

```text
git status --short
```

Output: empty. The working tree was clean before this record and `tmp-install/` were created.

## Probe 1 — stale-stance sweep

I searched the source surface named in the dispatch for both dead designs: the v4 verdict ban and the paper-only judge.

Command:

```text
rg -n -i --no-heading 'no verdicts|record carrying no verdicts|rule nothing|never rules|witness|gathers nothing|runs no walks' AGENTS.md CLAUDE.md .claude/skills templates
```

Output:

```text
<no output>
```

Exit status: `1`, meaning no matches.

I repeated the same sweep on the actually installed and upgraded payload produced in Probe 5.

Command:

```text
rg -n -i --no-heading 'no verdicts|record carrying no verdicts|rule nothing|never rules|witness|gathers nothing|runs no walks' tmp-install/AGENTS.md tmp-install/CLAUDE.md tmp-install/.claude/skills tmp-install/templates
```

Output:

```text
<no output>
```

Exit status: `1`, again meaning no matches.

There were no hits to quote or classify. On the exact stale phrases in the dispatch, both the source and installed surfaces are clean.

## Probe 2 — hearing coherence

I read these four files as one process:

- `.claude/skills/experience/SKILL.md`
- `.claude/skills/experience/references/walk.md`
- `.claude/skills/experience/references/worst-day.md`
- `.claude/skills/judge/SKILL.md`

I then pulled the sentences most likely to fight: who concludes, who rules, whether the judge walks, and who closes an evidence gap.

Command:

```text
rg -n --no-heading 'end with (your|their)|Close with your verdict|conclude like|experiencer rules|built nothing and walked nothing|does not walk|sends an experiencer back|Ruling on a gap|Rule\.|four, separately' .claude/skills/experience/SKILL.md .claude/skills/experience/references/walk.md .claude/skills/experience/references/worst-day.md .claude/skills/judge/SKILL.md
```

Output:

```text
.claude/skills/judge/SKILL.md:8:**The judge built nothing and walked nothing — its contact with the product runs through the experiencers it steers.** It reads their records and verdicts, the promises in `product.md`, and the standing rulings in `decisions.md`. It does not walk the product itself, because a head that gathered its own evidence rules on its own work — but it is never at arm's length either: when a ruling needs something no record shows, the judge sends an experiencer back to the product with the exact question ("try opening the list as a member while offline — what happens?") and waits for the run. Ruling on a gap is forbidden; ordering the run that closes it is the job.
.claude/skills/judge/SKILL.md:17:4. **Rule.** Per promise: kept · broken · not judged — each citing the record lines and, where challenged, the answers. Then the four, separately: **works · delivers the promise · good to use · quality hangs together** — no verdict compensates for another, each with evidence or an honest "not judged yet"; a failed check reads "check failed", never "not judged yet". When all four stand on evidence, the work is *proven* — and proven work is what goes Live.
.claude/skills/experience/references/worst-day.md:3:The persona: everything hostile and unlucky arrives at once — the weak user probing doors, the network dying mid-write, the corrupt file, the overlapping run. Every move here was paid for by a real defect that shipped past a green suite. Use what applies; skip what doesn't. Run each move, record exactly what happened and how you got there — then end with your verdict as the person having this day, every claim in it pointing at a move you actually ran. The judge will challenge it; answer from the record.
.claude/skills/experience/references/walk.md:3:For products with a user interface. Live it as your persona, record as you go, and end with your verdicts on three different things — does it work, does it feel good, is it crafted — none skipped: the axis that's skippable is the axis that silently stays uncovered. Each verdict points at screenshots and moments in your own record, and the judge will challenge it.
.claude/skills/experience/references/walk.md:18:12. Close with your verdicts as this persona — works, feels good, crafted — each in your own words, each pointing at the screenshots and moments behind it. A verdict pointing at nothing is void, and the judge challenges the favorable ones hardest.
.claude/skills/experience/SKILL.md:8:**Why this is its own skill:** a real user judges while using — so the experiencer rules, the way a user would. What keeps that honest is not banning the verdict but grounding and challenging it: every verdict must point at a moment actually lived in the experiencer's own record, and a separate judge questions and challenges it before it counts. Live it fully, record it faithfully, conclude like the user you are — and expect to defend it.
```

I found no pair that gives contradictory instructions.

- The experiencer is required to conclude from lived use; the judge is required to challenge that conclusion and make the governing rulings. The shared word “rule” is doing two jobs, but the actions can be performed together: persona verdict first, challenged ruling second.
- “The judge built nothing and walked nothing” does not conflict with dispatch-back. The same sentence says the judge sends an experiencer to run the missing scenario and waits. The judge still performs no walk.
- The UI walk's three persona verdicts (`works`, `feels good`, `crafted`) and the judge's four rulings are different layers, not mutually exclusive instructions. The record can carry three user judgments while the judge rules separately on `works`, `delivers the promise`, `good to use`, and `quality hangs together`.

## Probe 3 — contract and surface consistency

### Persona list

Command:

```text
rg -n --no-heading 'first-timer.*worst day|walk it cold.*worst day' CONTRACT.md AGENTS.md README.md
```

Output:

```text
CONTRACT.md:19:3. **Judged like a user, challenged like a claim — never by the builder.** Nobody grades their own homework, and no verdict lands unchallenged. Fresh experiencers who had no part in building live the product in personas — the first-timer, the real job end to end, the least-privileged user, the worst day — and judge it the way real users judge while using: each record ends in that persona's own verdict, and every verdict must point at a moment actually lived in that record; a verdict pointing at nothing is void. Then a judge who built and walked none of it convenes the hearing: questions and challenges each verdict — the favorable ones hardest — sends an experiencer back to the product when an answer needs another run, holds diverging persona verdicts side by side instead of averaging them, and rules with each ruling citing the records it rests on. At milestones and on risky work a second judge hears the same records independently, and divergence between the two judgments is itself a finding. Reading the code is not experiencing; a record with zero executed runs is itself a defect. A bug counts as caught only when an experiencer reproduced it by running the product, and a safety net counts as evidence only after it has been watched failing on purpose — a net that cannot fail catches nothing, and a tiny kernel check keeps that honest. *Check: the planted-bug tasks (T05–T10), scored per bug type against old Speck's frozen results — each with a clean twin, a matching task with no bug planted, so false alarms lose too — plus the review-integrity task, which fails any verdict lifted without a real dispatch behind it.*
README.md:20:**Five phases, always checkable.** The product moves shape → map → build → experience → judge: shaping is an owner conversation in numbered rounds that produces `product.md` and whatever material the product needs; mapping is the second conversation, cutting the ordered pieces and deciding the substrate; building runs one piece at a time through its own tight micro-loop; experiencing and judging run as one process — fresh experiencers live each finished milestone on the real surface as the first-timer, the real job, a second user, and the worst day, each concluding with their own verdict the way real users judge; then a judge who built none of it hears them, challenges every verdict, sends an experiencer back for another run when an answer needs one, and rules — with you grading how it feels. Every phase has a checkable exit — shaping and mapping close only on your sign-off in your own words, judging closes with your felt grade — transitions fire automatically and are named out loud, and a ruling, finding, or judgment can re-enter any earlier phase, with a trace.
README.md:28:**Nobody grades their own homework — and no verdict lands unchallenged.** Fresh experiencers who had no part in building live the product — walk it cold, do the real job, log in as the least-privileged user, have the worst day — and judge it the way real users do: each writes down exactly what happened and ends with their own verdict, every claim in it pointing at a moment they actually lived. Then a judge who built none of it puts each experiencer on the bench: questions the verdict, challenges the favorable ones hardest, and sends an experiencer back to the product when an answer needs another run. Different personas will disagree — the judge holds that disagreement side by side instead of averaging it, because the tension is usually where the truth is. Reading the code doesn't count as experiencing, and a safety net counts as evidence only after it's been watched failing on purpose.
AGENTS.md:33:- **Experience → judge** — one process, the hearing. *Enter:* a milestone's pieces have all landed. *Runs as:* experiencers — one fresh non-builder context per persona: the first-timer, the real job end to end, the second user, the worst day (`experience` skill) — live the increment on the real surface, each returning the record of what happened with that persona's own verdict at the end, judged the way a real user judges while using. Then the judge, who built and walked none of it (`judge` skill), hears them: questions and challenges every verdict against the record behind it, sends an experiencer back to the product when an answer needs another run, holds the diverging verdicts side by side without averaging them, and rules the four — works · delivers the promise · good to use · quality hangs together — each ruling citing the records. At milestones and on risky pieces a second judge hears the same records independently, and divergence between the two judgments is itself a finding. The owner grades the felt experience, asked on a plain rendering. *Exits when:* the four verdicts are recorded honestly, the owner has graded, and anything ruled insufficient has re-entered its phase — shape, map, build, or another round of experiencing — with a trace; then the next milestone's pieces unlock. When all four verdicts stand on evidence, the work is *proven* — that's the word's whole job here — and proven work is what goes Live.
```

The skill defines what “second user” means.

Command:

```text
sed -n '20,23p' .claude/skills/experience/SKILL.md
```

Output:

```text
1. **The first-timer** — cold start: real build, fresh install or cleared storage, logged out, knows nothing. At the first screen, answer from the pixels alone: what is this, who's asking, why now? For anything with a user interface, walk `references/walk.md`.
2. **The worker** — the real job, end to end, through the product's own surface (a harness the builder wrote is not the product), reading what it prints, chasing each claimed save/send/generate to its mechanism — the request, the changed record, the read-back.
3. **The second user** — a least-privileged real account attempting what it shouldn't reach, and a second person on the same install looking for traces of the first.
4. **The worst day** — everything hostile and unlucky at once: `references/worst-day.md`.
```

**Mismatch caught:** `CONTRACT.md:19` names “the least-privileged user” as the entire third persona. `AGENTS.md:33` and `README.md:20` name “the second user,” and the skill makes that persona broader: a least-privileged account **and** a second person on the same install. `README.md:28` falls back to the narrower contract wording. A reader following only the contract or that README paragraph can omit the same-install cross-user trace.

### Four ruling names and grounding

Command:

```text
rg -n --no-heading 'works ·|it works, it delivers|works, delivers|verdict.*point|point.*verdict|lived moment|moment.*lived' CONTRACT.md AGENTS.md templates/piece.md templates/rounds.md README.md
```

Output:

```text
AGENTS.md:3:You are an agent in a repository run by Speck Next. This page is the whole method — your host loaded it for you. The product moves through five phases — **shape → map → build → experience → judge** — and between you and the owner, it is always checkable which phase is running and whether it is done. Experience and judge run as one process with two stances: experiencers judge the product the way real users do — verdicts grounded in moments they actually lived — and a judge who built and walked none of it questions and challenges every verdict before it counts, because an agent's unchallenged verdict is how an agent fools itself. Even Speck Next itself is built under this page.
AGENTS.md:31:  4. **Convene its hearing.** Any safety net counts only after it's been watched failing on purpose. Then fresh experiencers — never the builder, in the personas the piece's proven-means names — live the piece per the `experience` skill and return their records, each ending in that persona's own verdict, every verdict pointing at a moment actually lived. A separate judge hears them per the `judge` skill: questions and challenges each verdict, sends an experiencer back to the product when an answer needs another run, holds diverging verdicts side by side, and rules citing the records. Receipts open at dispatch for experiencers and judge alike. Nothing reaches Judged without its hearing. At most one substantial piece sits unjudged when the next starts — and substantial is everything the small-changes rule doesn't cover, no third class.
AGENTS.md:33:- **Experience → judge** — one process, the hearing. *Enter:* a milestone's pieces have all landed. *Runs as:* experiencers — one fresh non-builder context per persona: the first-timer, the real job end to end, the second user, the worst day (`experience` skill) — live the increment on the real surface, each returning the record of what happened with that persona's own verdict at the end, judged the way a real user judges while using. Then the judge, who built and walked none of it (`judge` skill), hears them: questions and challenges every verdict against the record behind it, sends an experiencer back to the product when an answer needs another run, holds the diverging verdicts side by side without averaging them, and rules the four — works · delivers the promise · good to use · quality hangs together — each ruling citing the records. At milestones and on risky pieces a second judge hears the same records independently, and divergence between the two judgments is itself a finding. The owner grades the felt experience, asked on a plain rendering. *Exits when:* the four verdicts are recorded honestly, the owner has graded, and anything ruled insufficient has re-entered its phase — shape, map, build, or another round of experiencing — with a trace; then the next milestone's pieces unlock. When all four verdicts stand on evidence, the work is *proven* — that's the word's whole job here — and proven work is what goes Live.
README.md:14:> **Agent:** Done, re-checked in the app. Fresh eyes used it too — one tried it cold as a brand-new studio owner, another tried to open a rival studio's list with a member login, and each gave their verdict. A judge who built none of it challenged those verdicts — sent the newcomer back to retry the empty-list case — then ruled it: works, delivers the promise, good to use on desktop and phone, and the quality hangs together. Nothing open. The next valuable piece looks like class reminders — want it?
README.md:26:**Four states, honest ones.** Shaped, Built, Judged, Live. Judged spells out four verdicts separately — it works, it delivers the promise, it's good to use, the quality hangs together — each pointing at evidence or saying plainly "not judged yet". When all four stand on evidence, the work is proven — ordinary English, not another state — and proven work is what goes Live. Those four states are the only words Speck Next asks you to learn.
README.md:28:**Nobody grades their own homework — and no verdict lands unchallenged.** Fresh experiencers who had no part in building live the product — walk it cold, do the real job, log in as the least-privileged user, have the worst day — and judge it the way real users do: each writes down exactly what happened and ends with their own verdict, every claim in it pointing at a moment they actually lived. Then a judge who built none of it puts each experiencer on the bench: questions the verdict, challenges the favorable ones hardest, and sends an experiencer back to the product when an answer needs another run. Different personas will disagree — the judge holds that disagreement side by side instead of averaging it, because the tension is usually where the truth is. Reading the code doesn't count as experiencing, and a safety net counts as evidence only after it's been watched failing on purpose.
CONTRACT.md:19:3. **Judged like a user, challenged like a claim — never by the builder.** Nobody grades their own homework, and no verdict lands unchallenged. Fresh experiencers who had no part in building live the product in personas — the first-timer, the real job end to end, the least-privileged user, the worst day — and judge it the way real users judge while using: each record ends in that persona's own verdict, and every verdict must point at a moment actually lived in that record; a verdict pointing at nothing is void. Then a judge who built and walked none of it convenes the hearing: questions and challenges each verdict — the favorable ones hardest — sends an experiencer back to the product when an answer needs another run, holds diverging persona verdicts side by side instead of averaging them, and rules with each ruling citing the records it rests on. At milestones and on risky work a second judge hears the same records independently, and divergence between the two judgments is itself a finding. Reading the code is not experiencing; a record with zero executed runs is itself a defect. A bug counts as caught only when an experiencer reproduced it by running the product, and a safety net counts as evidence only after it has been watched failing on purpose — a net that cannot fail catches nothing, and a tiny kernel check keeps that honest. *Check: the planted-bug tasks (T05–T10), scored per bug type against old Speck's frozen results — each with a clean twin, a matching task with no bug planted, so false alarms lose too — plus the review-integrity task, which fails any verdict lifted without a real dispatch behind it.*
CONTRACT.md:20:4. **The state file tells the truth.** `state.md` answers six questions in plain sentences: what is true now, what is wearing out (every recorded strain — the workaround, the duplication, the piece that fought the structure — with how often it has bitten), what is blocked, what needs the owner, what happens next, and what evidence backs all of that. Four states: Shaped, Built, Judged, Live. Judged spells out the four verdicts separately — it works · it delivers the promise · it's good to use · the quality hangs together — each pointing at evidence or saying honestly "not judged yet", because one green word must never hide a taste failure. When all four stand on evidence the work is proven — plain speech for the loop's outcome, and proven work is what goes Live; a judgment that found the work insufficient routes it back with a trace instead of advancing it, and the state says so. Overclaiming is a bug, and a small mechanical check hunts the flaggable kind: any state line claiming a verdict without pointing at evidence, and any phrase the product's own copy rules ban. *Check: the closing state of every task is audited; T17 probes a repo whose state file went stale.*
templates/piece.md:11:**Hearing receipt** *(opened at dispatch, records appended on return)*: experiencers [per persona: tool, model, session] · dispatched [date, commit] · walks and commands [planned] · owner of this run [which session] · if a record is empty [re-dispatch under your own named line] · records and verdicts [linked — each verdict pointing at lived moments].
templates/piece.md:13:**Judgment** *(a separate fresh context that built and walked none of it)*: judge [tool, model, session] · ruled [date] · ruling on [this piece, at which commit] · challenges [questions put, re-runs ordered and their answers] · verdicts [per promise: kept/broken/not judged · works · delivers the promise · good to use · quality hangs together — separately · structure: sound/straining/fighting] · second judge [milestone/risky only: rulings + any divergence] · routed [anything insufficient → shape, map, build, or re-experiencing, with the trace].
templates/rounds.md:15:**Hearing receipt**: experiencer [tool, model, session] · dispatched [date, commit] · probes [planned — against the owner's record, the wire, the repo; cold read] · owner of this run · if the record is empty [re-dispatch under your own named line] · record and verdict [linked — the verdict pointing at probes actually run].
```

No mismatch appeared in the four ruling names or the grounding rule. `CONTRACT.md`, `AGENTS.md`, `templates/piece.md`, and `README.md` use the same four concepts. `templates/rounds.md` correctly grounds artifact verdicts in probes rather than product moments.

### Second judge at milestones and risky work

Command:

```text
rg -n --no-heading 'second judge|each finished milestone.*a judge' CONTRACT.md AGENTS.md templates/piece.md README.md
```

Output:

```text
AGENTS.md:33:- **Experience → judge** — one process, the hearing. *Enter:* a milestone's pieces have all landed. *Runs as:* experiencers — one fresh non-builder context per persona: the first-timer, the real job end to end, the second user, the worst day (`experience` skill) — live the increment on the real surface, each returning the record of what happened with that persona's own verdict at the end, judged the way a real user judges while using. Then the judge, who built and walked none of it (`judge` skill), hears them: questions and challenges every verdict against the record behind it, sends an experiencer back to the product when an answer needs another run, holds the diverging verdicts side by side without averaging them, and rules the four — works · delivers the promise · good to use · quality hangs together — each ruling citing the records. At milestones and on risky pieces a second judge hears the same records independently, and divergence between the two judgments is itself a finding. The owner grades the felt experience, asked on a plain rendering. *Exits when:* the four verdicts are recorded honestly, the owner has graded, and anything ruled insufficient has re-entered its phase — shape, map, build, or another round of experiencing — with a trace; then the next milestone's pieces unlock. When all four verdicts stand on evidence, the work is *proven* — that's the word's whole job here — and proven work is what goes Live.
README.md:20:**Five phases, always checkable.** The product moves shape → map → build → experience → judge: shaping is an owner conversation in numbered rounds that produces `product.md` and whatever material the product needs; mapping is the second conversation, cutting the ordered pieces and deciding the substrate; building runs one piece at a time through its own tight micro-loop; experiencing and judging run as one process — fresh experiencers live each finished milestone on the real surface as the first-timer, the real job, a second user, and the worst day, each concluding with their own verdict the way real users judge; then a judge who built none of it hears them, challenges every verdict, sends an experiencer back for another run when an answer needs one, and rules — with you grading how it feels. Every phase has a checkable exit — shaping and mapping close only on your sign-off in your own words, judging closes with your felt grade — transitions fire automatically and are named out loud, and a ruling, finding, or judgment can re-enter any earlier phase, with a trace.
CONTRACT.md:19:3. **Judged like a user, challenged like a claim — never by the builder.** Nobody grades their own homework, and no verdict lands unchallenged. Fresh experiencers who had no part in building live the product in personas — the first-timer, the real job end to end, the least-privileged user, the worst day — and judge it the way real users judge while using: each record ends in that persona's own verdict, and every verdict must point at a moment actually lived in that record; a verdict pointing at nothing is void. Then a judge who built and walked none of it convenes the hearing: questions and challenges each verdict — the favorable ones hardest — sends an experiencer back to the product when an answer needs another run, holds diverging persona verdicts side by side instead of averaging them, and rules with each ruling citing the records it rests on. At milestones and on risky work a second judge hears the same records independently, and divergence between the two judgments is itself a finding. Reading the code is not experiencing; a record with zero executed runs is itself a defect. A bug counts as caught only when an experiencer reproduced it by running the product, and a safety net counts as evidence only after it has been watched failing on purpose — a net that cannot fail catches nothing, and a tiny kernel check keeps that honest. *Check: the planted-bug tasks (T05–T10), scored per bug type against old Speck's frozen results — each with a clean twin, a matching task with no bug planted, so false alarms lose too — plus the review-integrity task, which fails any verdict lifted without a real dispatch behind it.*
templates/piece.md:13:**Judgment** *(a separate fresh context that built and walked none of it)*: judge [tool, model, session] · ruled [date] · ruling on [this piece, at which commit] · challenges [questions put, re-runs ordered and their answers] · verdicts [per promise: kept/broken/not judged · works · delivers the promise · good to use · quality hangs together — separately · structure: sound/straining/fighting] · second judge [milestone/risky only: rulings + any divergence] · routed [anything insufficient → shape, map, build, or re-experiencing, with the trace].
```

Command:

```text
rg -n --no-heading 'second judge' README.md
```

Output:

```text
<no output>
```

Exit status: `1`.

**Mismatch caught:** the contract, governing page, and piece template require a second independent judge at milestones and on risky work. `README.md:20` explicitly describes the finished-milestone hearing but says only “a judge,” and nowhere in README is a second judge named. This is an incomplete public description of a mandatory milestone step. It does not forbid the second judge, but a reader cannot recover the requirement from README.

### Version truth

The install run printed `v5.0.0`, so I checked the source's own version claims.

Command:

```text
rg -n --no-heading 'At v[0-9]+|[0-9]+\.[0-9]+\.[0-9]+' README.md package.json bin/speck-next.js
```

Output:

```text
bin/speck-next.js:32:  // v4.0.0 migration: independent-review split into the experience and judge skills; copy never deletes, so the upgrader must.
bin/speck-next.js:38:  // v2.0.0 file-contract migration: every governed repo carries map.md; the upgrader owns this.
bin/speck-next.js:86:Pin a version: npx -y github:Keegil/speck-next#v5.0.0 install`);
README.md:44:At v4 — proving redesigned into experience → judge on the owner's ruling that agents sent to prove act dysfunctionally, on top of v3's full sequence discipline — and self-hosted: this repository runs under its own [AGENTS.md](AGENTS.md), so every development session here is a live test of the method. Every dev-suite check is proven able to fail before any green counts ([devsuite/](devsuite/) — including its own honest note on what a green run does and doesn't prove). It was accepted for real use on demonstrated confidence — an owner decision, 2026-08-13 — with its first target the greenfield reboot of a real product; the designed head-to-head contest is shelved but kept ([docs/benchmark/fixtures.md](docs/benchmark/fixtures.md)). Current truth, open list, and next steps: [state.md](state.md). Why the clean sheet: [docs/history/](docs/history/). How these documents were attacked: [docs/reviews/](docs/reviews/).
package.json:3:  "version": "5.0.0",
```

**Mismatch caught:** `README.md:44` says the current status is “At v4,” while `package.json`, the CLI help, install output, and upgrade output identify the current kernel as `5.0.0`. The v4 migration comment is historical and fits; the README status does not.

## Probe 4 — references resolve

I enumerated the five shipped skills, every shipped reference named by those skills, and all six templates the method points at.

Command:

```text
speck_targets=(
  .claude/skills/shape-product/SKILL.md
  .claude/skills/map-build/SKILL.md
  .claude/skills/experience/SKILL.md
  .claude/skills/judge/SKILL.md
  .claude/skills/craft/SKILL.md
  .claude/skills/shape-product/references/questions.md
  .claude/skills/map-build/references/questions.md
  .claude/skills/experience/references/walk.md
  .claude/skills/experience/references/worst-day.md
  templates/product.md
  templates/map.md
  templates/piece.md
  templates/state.md
  templates/decisions.md
  templates/rounds.md
)
speck_missing=0
for speck_path in "${speck_targets[@]}"; do
  if [[ -e "$speck_path" ]]; then
    printf 'OK %s\n' "$speck_path"
  else
    printf 'MISSING %s\n' "$speck_path"
    (( speck_missing++ ))
  fi
done
printf 'checked=%d missing=%d\n' "${#speck_targets[@]}" "$speck_missing"
exit "$speck_missing"
```

Output:

```text
OK .claude/skills/shape-product/SKILL.md
OK .claude/skills/map-build/SKILL.md
OK .claude/skills/experience/SKILL.md
OK .claude/skills/judge/SKILL.md
OK .claude/skills/craft/SKILL.md
OK .claude/skills/shape-product/references/questions.md
OK .claude/skills/map-build/references/questions.md
OK .claude/skills/experience/references/walk.md
OK .claude/skills/experience/references/worst-day.md
OK templates/product.md
OK templates/map.md
OK templates/piece.md
OK templates/state.md
OK templates/decisions.md
OK templates/rounds.md
checked=15 missing=0
```

Exit status: `0`. All enumerated instruction targets resolve.

`CLAUDE.md` also resolves its host include:

Command:

```text
nl -ba CLAUDE.md
```

Output:

```text
     1	@AGENTS.md
```

`AGENTS.md` exists and was part of Probes 1–3.

## Probe 5 — run install and upgrade

### Fresh repository

Command:

```text
ls -ld tmp-install
```

Output:

```text
ls: tmp-install: No such file or directory
```

Exit status: `1`; the target did not exist.

Command:

```text
mkdir tmp-install
```

Output: empty. Exit status: `0`.

Command:

```text
git -C tmp-install init
```

Output:

```text
hint: Using 'master' as the name for the initial branch. This default branch name
hint: is subject to change. To configure the initial branch name to use in all
hint: of your new repositories, which will suppress this warning, call:
hint:
hint: 	git config --global init.defaultBranch <name>
hint:
hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
hint: 'development'. The just-created branch can be renamed via this command:
hint:
hint: 	git branch -m <name>
Initialized empty Git repository in /private/tmp/claude-501/-Users-kjetil-Code-speck/a0e0d32c-31ec-4aba-a433-2bd88364f16f/scratchpad/v5-worstday-Fncr/repo/tmp-install/.git/
```

Exit status: `0`.

### Install

Command:

```text
node bin/speck-next.js install ./tmp-install
```

Output:

```text
Installed Speck Next v5.0.0 into /private/tmp/claude-501/-Users-kjetil-Code-speck/a0e0d32c-31ec-4aba-a433-2bd88364f16f/scratchpad/v5-worstday-Fncr/repo/tmp-install — 19 files on disk (method files, the version marker, an empty starter map).
Next: open an agent session there and say what you want to build — shaping starts in that conversation.
```

Exit status: `0`.

Independent count:

Command:

```text
find tmp-install -type f ! -path 'tmp-install/.git/*' | wc -l
```

Output:

```text
      19
```

The printed count and measured count agree.

### Plant and upgrade

I created `tmp-install/.claude/skills/independent-review/` and applied this patch:

```diff
*** Begin Patch
*** Add File: tmp-install/.claude/skills/independent-review/SKILL.md
+# Independent review
+
+Planted file: an upgrade must preserve this unrelated skill directory.
*** End Patch
```

Command:

```text
node bin/speck-next.js upgrade ./tmp-install
```

Output:

```text
Upgraded Speck Next 5.0.0 (586a87a) -> 5.0.0 in /private/tmp/claude-501/-Users-kjetil-Code-speck/a0e0d32c-31ec-4aba-a433-2bd88364f16f/scratchpad/v5-worstday-Fncr/repo/tmp-install.
What changed (git has your back — diff or revert as you like):
?? .claude/
?? AGENTS.md
?? CLAUDE.md
```

Exit status: `0`.

Survival check:

Command:

```text
test -f tmp-install/.claude/skills/independent-review/SKILL.md
```

Output:

```text
<no output>
```

Exit status: `1`.

Command:

```text
sed -n '1,20p' tmp-install/.claude/skills/independent-review/SKILL.md
```

Output:

```text
sed: tmp-install/.claude/skills/independent-review/SKILL.md: No such file or directory
```

Exit status: `1`.

Post-upgrade count:

Command:

```text
find tmp-install -type f ! -path 'tmp-install/.git/*' | wc -l
```

Output:

```text
      19
```

**Result:** the planted directory did not survive. The upgrade returned the payload from 20 files to the canonical 19.

I checked whether that deletion was accidental or the named stale-surface migration.

Command:

```text
rg -n --no-heading 'independent-review|remove|rmSync|stale' bin/speck-next.js
```

Output:

```text
32:  // v4.0.0 migration: independent-review split into the experience and judge skills; copy never deletes, so the upgrader must.
33:  const old = path.join(target, ".claude", "skills", "independent-review");
34:  if (fs.existsSync(old)) fs.rmSync(old, { recursive: true });
```

The removal matches the declared v4 migration: `independent-review` is the retired method skill whose responsibilities were fused into the hearing. On this exact planted path, deletion prevents the dead design from coexisting with `experience` and `judge`.

## Limits

- All five requested probes ran. No requested command was left untested.
- This was a kernel-surface and CLI run. I did not build a downstream product, run a product UI, take screenshots, exercise auth, or simulate network and persistence failures; those product behaviors are untested here.
- I tested the retired `independent-review` path by planting it in a fresh v5 install. I did not run upgrade against an actual historical v4 repository with real work in flight; historical work preservation is untested by this record.
- I did not act as the judge, challenge another persona, or perform a judge-ordered follow-up. This record is ready for that hearing but does not stand in for it.

## Verdict

As the person who had this day: **the agent-loaded governing surface is coherent enough to run a real build, but the repository-wide story is not clean enough to call internally consistent.**

I would trust an agent governed by `AGENTS.md`, the five skills, and the templates to run the fused hearing. Probe 1 found none of the named dead v4 stances in either source or installed output. Probe 2 found a workable division: experiencers conclude from runs, the judge challenges without walking, and dispatch-back closes gaps. Probe 4 resolved every shipped skill, reference, and template. Probe 5 installed and upgraded successfully at the measured 19-file payload, and deliberately removed the retired `independent-review` surface.

I would not trust a reader to reconstruct the same method from the contract and README without first fixing three concrete drifts caught in Probe 3: the contract and one README paragraph shrink the broader “second user” into only a least-privileged user; the README's milestone hearing omits the mandatory second judge; and README calls the current `5.0.0` kernel “v4.” Those are not theoretical style complaints. The first can skip a cross-user leakage probe, the second can skip an independent milestone ruling, and the third makes the current release state stale on its front page.

So my worst-day answer is **yes for governing a build through the installed agent surface; no for claiming the whole published surface says one thing yet.** That split rests on the clean installed sweep and successful run in Probes 1, 4, and 5, and on the three quoted drifts or omissions in Probe 3.
