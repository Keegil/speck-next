# Harness research refresh — September 29, 2026

The owner asked for a quick check against current harness engineering knowledge. Scope: primary-source scan, small corrections to v7, focused installer verification and one independent review. No new workflow, fixed staffing, or model campaign.

## What the sources support

| Primary source | Finding and boundary | Decision for Speck |
|---|---|---|
| [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/), February 11 | A production-team account emphasizes navigable repository knowledge, inspectable running software, and mechanically checked invariants. It is one team's experience, not a controlled comparison. | Add concise instructions for usable feedback and focused checks when defects recur or consequences justify them. Reuse existing tooling. |
| [Anthropic, Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps), March 24 | Scaffolding useful for one model became unnecessary for a stronger model. The author removed components individually; independent evaluation still found important incomplete behavior. Demonstrations have different scope and spending, so they do not prove a universal architecture. | Keep v7's conditional capabilities and independent acceptance. Revisit scaffolding when models change; measure rather than prescribe more agents. |
| [Anthropic, Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), January 9 | Evaluate actual outcomes, isolate trials, examine traces and grader failures, and use real cases. Following an exact tool sequence is often an unsuitable success criterion. | Add an optional comparison paragraph to `experience`, scoped to agent/harness evaluation. |
| [Fan et al., An Empirical Study of Harness Design for Coding Agents](https://arxiv.org/html/2609.20804v1), September 17 | Planning, context handling, and action-space effects varied by model, benchmark and budget. Tests cover Nemotron-3/Mistral configurations, SWE-Bench Verified and Terminal-Bench 2.1; they do not establish effects for our current Claude/GPT product workflows. | No universal planning, compaction, memory, or tool-count rule. Compare the setup used for the real job. |
| [Gloaguen et al., Evaluating AGENTS.md](https://arxiv.org/html/2602.11988v2), June 23 revision | On the studied repository tasks, instructions did not generally improve task success and increased inference cost. This does not evaluate Speck or establish that owner constraints and continuity records are useless. | Keep additions short, conditional and operational; do not paste research into the installed instructions. |

The September 26 revision of [Harness Tokenomics](https://arxiv.org/html/2609.28919v2) was also considered. Its savings estimates come from emulation rather than a controlled quality-preserving coding trial. No routing or savings claim is adopted.

## Change

Version 7.0.1 adds small, navigable context and verified restart guidance; usable runtime feedback; focused executable checks for recurring failures or consequential invariants; and evidence before claims about a changed harness. The state template gives the next builder a useful command. The experience skill explains a bounded comparison when agent behavior is being evaluated. No new installed files, skills, phases, or mandatory review roles.

The version-dependent installer tests now retain 7.0.0 as a migration source and derive the next unsupported patch version. Installer behavior is unchanged.

## Evidence and limits

Accepted method candidate: `93ce912`. Installed method: 17 files, 29,960 bytes; `AGENTS.md` is 6,869 bytes. SHA-256: `f57becee9e3688f6a0c1e0d08f13ca3a0666b121c0fb382d10b41c97a563119c`.

- Independent Claude Opus reviewed the original patch at `d63687f` from a limited source packet and ran `python3 devsuite/proportional-v7/check.py`: all 10 tests passed in 27.0 seconds, including 40 supported-version/product combinations and packed installation. CLI exit 0 and its terminal success event were verified (session `17040823-9817-4625-8993-9e5986ff4abb`). No blocking findings.
- Its nonblocking notes prompted shorter instructions, explicit preservation of independent acceptance, and conditional isolation of experimental changes. A fresh independent Codex context read the final files and refinement diff at `93ce912` and accepted the typo, recurring-defect, and harness-comparison boundaries. These are text-review findings, not agent-use trials. Cursor had no review quota; Claude's quota prevented a second pass there. No extra credits were purchased.
- A final-source install into a fresh Git fixture returned 7.0.1 and the digest above, matched `AGENTS.md`, resolved the Codex skill link, and created no product record. Installer implementation and tests were unchanged by the prose refinements.

This is a research-grounded guidance correction, **unbenchmarked** for software quality, task success, time, and token savings. Prior v7 use trials retain their original scope. The published studies motivate these changes; they do not validate Speck's implementation. The independent review did not independently verify the research sources; source review was separate.

## Release and adoption

[v7.0.1](https://github.com/Keegil/speck-next/releases/tag/v7.0.1) was published and read back on September 29. The annotated tag resolves to `2173a039fd5c03f68cf4d4376cd055c562cb513b`. `npx -y github:Keegil/speck-next#v7.0.1 install <fresh-git-fixture>` passed; installed version, digest, exact instructions, Codex link, and absence of generated product/map records were verified.

The existing adoption request was carried forward to these four checkouts:

| Checkout | Branch | Pushed commit |
|---|---|---|
| Odd | `codex/odd-preparation-app` | `c6df6900ba16859b49d45d0dc272ae803683d9a4` |
| Splang Slack | `main` | `3c4c13cd0cf9a90260a724f4b9e91e6cbc86273a` |
| Odd p2r review | `codex/odd-p2r-review-resume-20260908` | `7603c815202ab5634736220c18279302c2041616` |
| Odd boka review | `codex/odd-boka-visual-20260908` | `15e3ed749067e6e901ace88b909ce460cc859b2d` |

The upgrade worker compared all 68 installed canonical files and preserved 2,842 tracked owner fingerprints and 14,263 untracked paths, including modes. The integrator independently rechecked all canonical files, markers/digest, exact original dirty statuses, four-file-only commit scopes, and remote branch SHAs. No other native adopter was found under `~/Code`; local snapshots and test subjects were excluded. Raw local evidence: `/tmp/speck-701-rollout.json` and `/tmp/speck-701-rollout-verified.json`. Next use is ordinary product work; no additional harness campaign is scheduled.
