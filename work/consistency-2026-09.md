# Consistency and surface review — September 29, 2026

Request: fix release consistency and ensure all Speck Next elements, including skills and templates, form a coherent, useful method. Baseline: `bab31801c6abf20aea4a41d3c8903042e899d762`, version 7.0.3. This is a compatible patch, 7.0.4; no new runtime service, model campaign, or fixed workflow is needed.

## Scope and findings

Review covers the installed entrypoints, five skill bodies and their references, six templates, CLI messaging and package, default development checks, and current documentation. A separate reader found stale release pins in both README and CLI help, omitted install prerequisites, historical capability rows presented as current, an unlabeled historical example, and an overstated claim that the shelved benchmark was runnable. Templates still used compressed internal labels and implied more structure than the skills require.

The five skill bodies and their conditional references otherwise retain the intended boundaries, scoped protection, and independent substantive acceptance. Their 7.0.3 trials remain evidence about that release, not a new automatic-activation or productivity claim.

## Changes

- Align release instructions and derive CLI help's tag from package version. Document existing Git/Node/npm prerequisites. Distinguish filesystem entries from regular file count.
- Rewrite optional templates around the actual brief, useful evidence, dependencies, decisions, and resumption. Retain existing filenames and omit unnecessary sections. No migration of owner records.
- Keep live state, plan, and capability evidence focused on present work; preserve prior records through immutable Git links. Label the Pulse example and benchmark according to their actual historical status.
- Add cheap checks for versions, skill metadata, local reference reachability, host discovery and installed size, with deliberately broken disposable fixtures. Wire them into the default suite and GitHub Actions without model calls.

Template edits and check implementation have separate file owners. The integrator owns documentation and cross-file agreement. A non-contributor reviews the combined candidate and exercises the relevant template/check behavior before release.

## Evidence

Accepted method candidate: `18f249115a8f9688d9552d83159db0ab7e2ce2d1`. Installed method digest: `1173d762521086f1557fc3a30eaed57f54edf7273a493739d7636fd97c49a739`. The canonical method is 19 regular files / 37,428 bytes, 115 bytes smaller than 7.0.3. The six templates total 2,874 bytes, down from 3,020. A fresh source installation has 20 regular files including its marker, plus one discovery symlink: 37,701 bytes including the link target. The exported snapshot reports 37,696 because its marker has no Git source checkout.

- A non-contributor reviewed the complete exported candidate and accepted it with no blocking findings. The [independent verdict and returned handoff](../docs/reviews/consistency-7.0.4.md) preserve scope and limitations.
- That reviewer ran the default suite once: nine guard-control tests and ten installer tests passed, including 52 version/product combinations. The controls introduce real metadata, version, link, discovery and footprint failures. An additional disposable npm-package omission failed the complete-install comparison as intended.
- [GitHub Actions run 36612678569](https://github.com/Keegil/speck-next/actions/runs/36612678569) passed at the exact candidate SHA on Ubuntu with Node 22 and Python 3.13. The whole hosted job took 27 seconds. Records-only commits and release tags do not repeat the suite; relevant source changes do.
- A forward use of the state template preserved an existing uncommitted stock-filter repair, identified missing case-insensitive selection despite two passing supplied tests, and returned an executed reproduction. The integrator independently read back the subject hash and runtime gap. This is one synthetic handoff, not a completed second-agent implementation or evidence of automatic host activation.
- All five skill manifests passed the skill creator's validator. Pulse's basic log/display/help commands ran against a temporary journal; the optional model path was not exercised or requalified.

Cursor Opus and Claude CLI Opus review attempts both stopped at weekly usage limits before reading files. They supply no review evidence. Acceptance came from a fresh non-contributor in the same model family; cross-model review remains unavailable for this patch.

Static checks do not establish semantic consistency, remote URL availability, arbitrary YAML support, agent productivity, or complete behavior coverage. The review covers the changed composition; earlier skill-use and proportionality trials keep their original versioned scope.

## Distribution

[v7.0.4 is published](https://github.com/Keegil/speck-next/releases/tag/v7.0.4); the remote annotated tag resolves to `561800e7c305493a0eaf230d7088f69f367bd328`. Only evidence records changed after the accepted candidate. The published `npx -y github:Keegil/speck-next#v7.0.4 install` completed in a disposable Git repository. All 19 canonical files match the tag, the marker has the reviewed digest, Codex discovery resolves correctly, and no owner records were generated. The first read-back assertion compared macOS's `/tmp` alias with `/private/tmp`; canonicalizing the verifier's target path resolved that check without changing the installation.

All four existing native adopter checkouts were upgraded, committed and pushed. Each commit changes exactly nine managed paths. Fetched remote commits and an independent integrator read-back confirm all 76 canonical-file comparisons, the reviewed digest, version 7.0.4, discovery links and unchanged owner status.

| Checkout | Branch | Pushed commit |
|---|---|---|
| Odd preparation | `codex/odd-preparation-app` | `e68a5efd3221dc16164851625397490293b9926d` |
| Splang Slack | `main` | `7a5a58cc2596f766b509cfd9aa58ebc0d34f2ee1` |
| Odd review | `codex/odd-p2r-review-resume-20260908` | `8b1df9f65be01769b70409d61c424f90d773eac0` |
| Odd visual | `codex/odd-boka-visual-20260908` | `db04b45c84a5cbbd7a5afd33b1188593828c2c61` |

The fresh preservation baseline covered 2,842 tracked owner files and 14,263 untracked paths. All matched after upgrade and push. Exact index bytes matched immediately after each updater run. Before committing, index bytes had changed for an unestablished reason, while every staged path, mode, blob and stage still matched; no index was restored. Owner index entries remained unchanged through scoped method commits. Odd's existing repair-script edit and `.local/`, Splang's mapping-business edit, and both clean worktrees retain their original statuses. The kernel's unrelated local files were excluded.

The next consumer is ordinary product work in these upgraded checkouts. No further kernel campaign is commissioned by this release.
