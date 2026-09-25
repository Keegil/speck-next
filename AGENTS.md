# Speck Next

Speck Next helps an agent build products proportionally: match clarification, planning, records, expertise, verification, and review to each request's intent, uncertainty, consequences, reversibility, breadth, continuity needs, and the owner's stated budget. Ordinary instructions authorize ordinary work. Questions, analysis, and reviews are tasks in their own right — missing `product.md` does not force a project kickoff.

**Five capabilities** — shape, map, build, experience, judge — are usable together, skipped, or revisited on evidence; they are not mandatory sequential gates. **Build** is the core loop (understand enough → earliest useful result → exercise the affected complete job → evidence and continuity). **Five skills** implement parts of that: `shape-product`, `map-build`, `craft`, `experience`, `judge`. There is no separate build skill.

## How to enter

| Situation | Typical path |
|---|---|
| Tiny fix (typo, obvious bug, reversible one-commit change) | Fix, run a targeted check, done. No method files unless continuity needs them. |
| Small new project | Short brief (even in chat); first slice running quickly. Add `product.md` only when promises must survive sessions; add `map.md` only when multiple pieces have real dependencies. |
| Narrow risky change (auth, money, privacy, data integrity, regulation, irreversibility) | Same loop plus protections on **that behavior** (not diff size): least privilege, integrity checks, safe stand-ins, rollback evidence. |
| Larger or uncertain product | `shape-product` / `map-build` when durable direction or dependencies need records; independent review before landing substantive deliverables. |

Ask only when a missing choice changes user-facing behavior, risk, or order — and only if existing instructions do not already authorize the work. Do not re-litigate settled decisions. Consequential product-direction and architecture choices reach the owner with one recommendation and what each option changes for users.

Honor explicit budgets. If planning cost grows past useful work, stop planning and run something small. Bound costly uncertain experiments and retries.

## Stopping

Finish when the agreed outcome has adequate evidence for its scope. Further work needs an actual finding, new request, or unresolved consequential choice — not ceremony. Lack of independent review must be disclosed as **unreviewed**; disclosure does not substitute for independent acceptance of substantive work.

## Records (optional)

- **`product.md`** — durable promises, audience, feel, foundations with triggers.
- **`map.md`** — when multiple build pieces have real dependencies.
- **`state.md`** — resumable ongoing work.
- **`decisions.md`** — consequential forks.
- **`work/`** — useful bounded notes.

`templates/` are starting examples — copy useful fields only; delete the rest.

## Precedence

This page (v7) supersedes **generated procedural obligations** from earlier Speck versions that may still appear in `product.md`, `decisions.md`, or old work files (assessments, mandatory gates, receipt rituals, role call tables). It does **not** supersede explicit current owner promises, constraints, care choices, or evidenced findings. When documents disagree on product truth, `product.md` and `decisions.md` win over other notes. Measured evidence beats documents — fix the loser and cite the finding.

## Concerns, not a fixed staff

**Product**, **Business**, **Experience**, and **Engineering** are lenses — not mandatory separate contexts. Bring expertise when a consequential uncertainty needs it; one integrator owns end-to-end behavior when delegating. Return to a contributor only when a material finding challenges their decision.

## Build and use the product

Run the real product while building user-visible work. First external dependency contact is a real round-trip. Use the `craft` skill where surfaces matter; apply its advice to relevant states only.

Concrete failure of an integrated user job holds dependent work until fixed and the affected complete sequence is re-run. Unrelated work may continue. Do not ceremonially re-review already proved work. Strains worth remembering go in `state.md` when they affect future builders.

## Review

**Substantive** means a change to meaningful behavior, promises, architecture, or decisions whose correctness cannot be settled by an obvious local check — e.g. a one-line typo or formatting fix is not substantive. Substantive delivered work gets fresh independent review (non-contributor; may exercise and accept in one context). Trivial obvious reversible fixes: targeted check only.

Scale extra perspectives to distinct material risk — not a fixed roster. The `experience` and `judge` skills are optional depth; not mandatory headcounts or v6 receipt/Built ceremony unless the owner explicitly requires that governance in current records.

## Protected behavior

Auth, money, privacy, data integrity, regulation, and irreversible actions need applicable care on affected behavior. Do not lower established protections without new evidence and an owner decision where consequences change.

## Upgrade (v7)

`npx -y github:Keegil/speck-next upgrade` on marker-bearing Speck Next repos; preserves owner bytes; supersedes v6 **procedure** only. Old Speck (unmarked) conversion not implemented — see README and CONTRACT.

## Examples

- *"Sort tomorrow's list by class time."* → change, run in app, quick check, done.
- *"New studio check-in app, start small."* → brief, first slice; `product.md` when promises must stick.
- *"Add Stripe checkout."* → sandbox transaction and read-back, least-privilege paths, rollback story; no real charges without authorization; independent review before land.
- *"Whole product over months."* → shape/map as dependencies demand; `state.md` for continuity; review substantive increments.

Communicate in plain language: result, evidence, next step. No required phase prefixes.
