# speck-next · Product contract

Status: **v0.2 — revised against adversarial review round 1** (three decorrelated reviewers; see [docs/reviews/](docs/reviews/)). No framework code until the round-2 closure check confirms the P0 fixes landed.

## Job

Given a product intent, equip an agent to understand what matters, choose and complete the next valuable unit of work, prove it on the real path, and leave the repository clearer for the next agent. The owner supplies intent, judgment, and product decisions — never methodology operation.

**Optimization target: great, shipped product outcomes per minute of owner attention.**

## Owner constraints (verbatim, 2026-08-13)

1. "Upgrading from any version of Speck to Speck Next is 100% seamless for any project."
2. "Speck Next needs to work more iteratively involving the user. The whole big-bang 'spec the whole thing and build the whole thing' simply doesn't work."

## Promises

1. **Iterative to the bone.** Work ships as small increments that each end in something runnable, and the owner operates the real surface — a demo is handed over, not merely produced. Measured, not asserted: minutes, tokens, and files written **before the product first executes on the real path** are capped per unit of work; an owner steer must be able to materially change the next increment. Where the real action is irreversible (payments, live recipients, production data), the round-trip runs against a named replica and the fidelity gap is disclosed in the evidence. *Acceptance: pre-first-run caps and logged owner touchpoints scored on T02–T04 and T09, not one task.*
2. **A real gear for small.** Trivial changes create zero durable methodology artifacts and take minutes. Trivial is defined ex-ante, not self-served: no new dependency · no auth, data-integrity, money, or privacy path touched · no promise text changed · reversible in one commit. The classification is recorded; the agent may raise rigor on its own judgment but may never lower it; an uncertain classification goes to the independent evaluator. *Acceptance: T01, T14, and trap task T15 (a typo-shaped prompt sitting on a privileged path — failing to escalate is a scored miss).*
3. **Proof stays sharp.** Every substantive unit is evaluated by a fresh context that did not author it — structurally invoked, not waivable by the author — which **executes** the real user or operator path (least-privileged principals where relevant) with at least one control demonstrated able to fail red. A defect counts as caught only when reproduced by execution; a mention without reproduction scores zero and bills as cost. An evaluation containing zero executed observations is itself a defect. A small red-capability probe stays in the kernel so "the control can fail" remains demonstrable. *Acceptance: T05–T10 with per-class scoring, matched clean twins, and a false-positive ceiling — refusing everything cannot win.*
4. **Honest state, small and current.** `state.md` is generated from the work packets, decisions, and evidence — never hand-maintained — and answers five questions: what is true · what is blocked · what needs the owner · what happens next · what evidence backs this. Four plain states — Shaped, Built, Proven, Live — where **Proven carries one line per axis** (works · delivers the promise · good to use), each pointing at evidence or saying "not judged". Overclaiming is a defect class; a tiny deterministic overclaim check stays in the kernel. *Acceptance: closing state audited on every benchmark task; staleness probed by T17.*
5. **Seamless adoption from any Speck.** One command adopts any Speck repository, any era, in any condition — including mid-flight. Seamless means **the adoption itself requires zero manual repair**, not that it launders the repo's health: conversion always completes, and every item that cannot be cleanly mapped lands in `state.md` as a disclosed finding with its source path and original id — *converted with disclosed residue*, never a refusal of a Speck repo, never silent loss. Live truth maps (promises → `product.md`, decisions → `decisions.md`, defects and truth → `state.md`, in-flight work → work packets); states map conservatively, never up, keeping imported evidence per axis so nothing is re-proven unless new claims exceed it; history stays archived in place, quarantined from agent discovery; legacy hooks and instructions are disabled. Era detection: `.speck/VERSION` primary, artifact-shape inference for pre-VERSION repos, and an ambiguous era refuses loudly — the only refusal case. The adoption is one commit that never absorbs unrelated work, is idempotent to retry, and revertible; the adopter writes one marker the kernel refuses to run past until adoption is finalized. All era knowledge lives in the adopter, quarantined from the kernel. *Acceptance: T11–T14 on all four field repos plus the odd mid-epic case and synthetic pre-VERSION eras; a source-ledger oracle written independently of the adopter; pass = residue disclosed and non-lossy.*
6. **Invisible methodology.** The owner states intent, decides, and reads truth in plain language. Measured as comprehension, not word-counting: an owner-proxy with no glossary must answer the five state questions correctly from `state.md`; the frozen owner-facing vocabulary is at most five words. Internal terms may exist in diagnostics; they are not part of the owner interface. *Acceptance: owner-proxy audit on every benchmark task's closing state.*
7. **Small by law.** Hard budgets in this repository's own CI, with positive controls proving each can fail: **framework footprint** installed in a product repo ≤ 25 files / 250 KB, counting the index, rigor packs, host adapter, and every reachable capability, visible or not (the adopted repo's archived history is explicitly outside this budget) · **always-on read set** (doctrine + `state.md` + `product.md`) ≤ 25 KB, so a growing `product.md` is a budget breach, not a project fact · **≤ 1 durable methodology artifact per unit of work** beyond the three shared documents (`product.md`, `decisions.md`, `state.md` — the work packet is that one artifact, and trivial work creates none) · **end-to-end unit cost** ceilings (tokens, minutes, owner interruptions) for the trivial and small-feature classes, enforced by running the benchmark harness in CI. A budget rises only in a new owner-approved contract version that names another budget falling — and a rise can never retroactively pass a falsification already failed.
8. **Anti-accretion with a meter.** The alarm is measured, not remembered: if methodology-maintenance work exceeds **20% of commits or tokens over any trailing month** of kernel development, development stops and subtracts first. One bounded registry in this repository — one row per capability: the frozen failure it prevents · predicted benefit with a measure-by date (measured or retired) · cost · retirement condition · kernel-or-pack placement. No per-consumer metadata, no five-field matrices in product repos, no enforcement layer watching the registry. Every release names its retirement candidates in the release note. Needing a context loader, receipts, or a compliance layer for the kernel itself remains the tripwire.

## Whole-property register

Properties no single gate can enumerate, named so decisions can be weighed against them (admission test: *could a decision violate this while every gate stays green?*):

1. **Product excellence** — correct · on-contract · felt-good · tasteful; axes never compensate.
2. **Owner attention and peace** — the optimization target itself; more owner contact is not more virtue, and a decision adding owner touchpoints must show attention saved elsewhere.
3. **Iterative-with-owner** — running product early, steer that matters.
4. **Risk-proportionate rigor** — small stays cheap; privileged paths never self-classify down.
5. **Smallness** — of the kernel, the vocabulary, and the artifact trail.
6. **Seamless adoption** — any Speck repo, any condition, residue disclosed.
7. **Truth-over-theater** — evidence from execution; durability counts (shipped work stays good).

A decision is *consequential* — and must record its effect on each register row — when it defers, simplifies, descopes, adds owner contact, or moves a budget.

## Non-goals

Process-conformance proof · runtime multi-era compatibility (adopter only) · host-adapter zoo (generate the active host) · replacing project-native tests and CI · spec-first big-bang planning · methodology self-management machinery in product repos.

## Inheritance rule

Speck's PROVE **doctrine** and failure corpus cross nearly intact: independent evaluation, real-path execution, least-privileged principals, tautological-test attacks, red-capable controls, user-outcome judgment, visible uncertainty, promise conservation. **No implementation mechanism crosses by default.** Any mechanism wanting in answers six questions: which frozen recurring failure it prevents · why project-native code or tests cannot prevent it · kernel or pack · smallest interface · how measured · what retires it. Where the manifest replaces a mechanism, the replacement row must name its mechanism, its finding id, and its stop power — doctrine alone replaces nothing.

## Falsification

Judged on predeclared vertical slices (task set, attempt counts, and n ≥ 3 runs per task per system fixed at Lock 2; results immutable once run). The greenfield thesis is abandoned and the v11 line resumes as primary if any of:

1. **Truth-detection**: any critical class in the per-class pass/fail table falls below the frozen v11.2.0 baseline, on the frozen or the held-out plantings.
2. **Adoption**: any of T11–T14 or the synthetic-era set fails (lossy residue, manual repair required, or legacy knowledge needed after adoption).
3. **Budgets**: any Promise 7 budget is exceeded at the slice, with quality measured on the four product axes — there is no quality-loss escape clause; an overrun falsifies.
4. **Adoption in anger**: if no consumer repository is doing real product work on speck-next by **2026-10-01**, the thesis has failed regardless of benchmark score. Owner decides continuation explicitly; silence means failure.

While the experiment runs, the v11 line takes honest-freeze fixes only; its four known framework defects are filed, dated, and fixed there so the fallback cannot rot.
