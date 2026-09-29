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

Candidate validation and independent review pending. This is a research-grounded guidance correction, **unbenchmarked** for software quality, task success, time, and token savings. Prior v7 use trials retain their original scope. The published studies motivate these changes; they do not validate Speck's implementation.
