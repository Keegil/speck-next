# speck-next

The clean-sheet successor to [Speck](https://github.com/telum-ai/speck): a small agent kernel whose job is to help an agent build great products and prove the result, while keeping methodology operation invisible to the owner.

**Status: pre-code, contract v0.2 under round-2 closure check.** The founding thesis, evidence, and program live in [telum-ai/speck#130](https://github.com/telum-ai/speck/issues/130). No framework code exists, by design: the [product contract](CONTRACT.md) must survive adversarial review, and the successor must then beat Speck v11.2.0 on a benchmark whose raw evidence was frozen before any kernel design existed.

## Why a new repository

Speck's principles repeatedly caught real, serious defects — always through two mechanisms: an independently motivated evaluator, and exercising the real product path with controls demonstrated able to fail. The system around those mechanisms grew into a methodology compliance platform (70 skills, 130 scripts, 53 coined terms, 3.1 MB installed per repo, ~53k tokens of process per 50-line feature) whose dominant recent activity was maintaining itself. Two disciplined subtraction attempts (v8, v11) cut context cost while the mechanism count kept growing. The full diagnosis is in #130 and its reviews.

## The program

1. **Lock 1 — raw evidence frozen** before design: [docs/benchmark/fixtures.md](docs/benchmark/fixtures.md) (snapshots, defect classes, task intents and observables; integrity rules, custodian role, non-compensatory gates).
2. **Product contract** — [CONTRACT.md](CONTRACT.md), with the [deletion manifest](docs/deletion-manifest.md) naming what does not cross and what replaces it.
3. **Adversarial review** — round 1 complete (three decorrelated reviewers; verdict: fixable, not survivable as written — [docs/reviews/](docs/reviews/)); v0.2 responds finding-by-finding; round-2 closure check verifies the P0 fixes.
4. **Lock 2** — executable task manifests and plantings authored by an independent custodian; v11.2.0 baseline measured and frozen; rubric locked and hashed by a decorrelated reviewer.
5. **Vertical slice** — judged against Speck v11.2.0 on the frozen tasks, n ≥ 3, per-class scoring, decorrelated judge.
6. **Decide with data** — the contract's falsification clause includes a use-it-in-anger deadline: if no consumer repo is doing real work on speck-next by 2026-10-01, the thesis has failed regardless of benchmark score.

While the experiment runs, the v11 line takes honest-freeze fixes only, so the fallback cannot rot.

## Non-negotiables carried from the field record

- The author never certifies their own substantive work, and the evaluator executes — reading is not evaluation.
- Proof means the real path ran, with controls seen failing red.
- Promises are conserved: work that quietly stops delivering the promise cannot be called done.
- State is honest and generated: what is true, what is blocked, what needs the owner, what happens next.
- Upgrading from any version of Speck is 100% seamless for any project: adoption itself needs zero manual repair, and anything unmappable becomes disclosed residue — never a refusal, never silent loss.
- The loop is iterative and involves the owner through working demos and real decisions — never a big-bang spec.
