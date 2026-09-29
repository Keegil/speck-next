# Skill composition refresh — September 29, 2026

The owner questioned whether the five skills' terse, awkward instructions and descriptions reflected current skill-authoring practice. The task is to improve discovery and usable guidance while retaining proportional effort. Baseline: `3b3a3814eda7452eb24ea47222a1b4268649f71a` (7.0.2). This is a compatible patch: the five names, host paths, method, and owner records stay compatible.

## Findings and changes

The problem was not short files. Descriptions mixed activation with review policy, bodies compressed decisions into undefined shorthand, and supporting questions reintroduced prerequisites the kernel had removed.

- Give each skill one recognizable job, concrete inputs, useful output, and a stopping condition. Retain judgment where the work is open-ended.
- Distinguish design (`craft`), gathering use evidence (`experience`), and independent acceptance (`judge`). They can share a context when independence permits; selecting one does not force a sequence of loads or dispatches.
- Shape from the actual request and settled choices. A cheap working probe can end an interview. Personal/non-AI products stay personal/non-AI. Independent acceptance of a substantive proposal remains required.
- Map dependencies from an accepted brief without requiring `product.md`, a log, or approval of routine ordering. Compare meaning with the request instead of counting headings.
- Test the delivered subject, including claimed uncommitted changes. An unconditional clean clone could omit the thing under review.
- Load the question banks only for relevant uncertainty. Move specialized agent evaluation to one conditional reference, including the distinction between discovery and execution tests.

Two reference files were revised by a contributor with exclusive ownership; the integrator revised the five entrypoints together because their boundaries depend on each other. Existing walkthrough, failure, and research references remain useful.

## Sources and judgment

Checked live on September 29, with the local Codex `skill-creator` implementation as an additional host example:

- [Agent Skills specification](https://agentskills.io/specification): required metadata and portable format; no compulsory body template. Progressive disclosure is recommended, not a demand to add files.
- [Agent Skills authoring guidance](https://agentskills.io/skill-creation/best-practices): coherent jobs, non-obvious guidance, appropriate freedom, and conditional references.
- [Description optimization](https://agentskills.io/skill-creation/optimizing-descriptions) and [execution evaluation](https://agentskills.io/skill-creation/evaluating-skills): distinguish activation from result quality, include near-misses, and evaluate benefit against cost. A large optimization campaign is not warranted for this bounded patch.
- [OpenAI skill construction](https://developers.openai.com/plugins/build/skills) and [Codex skill evaluation](https://developers.openai.com/blog/eval-skills): recognizable user goals, explicit boundaries, representative requests, and separate implicit invocation tests. The [current host guide](https://learn.chatgpt.com/docs/build-skills) recommends focused jobs and concise descriptions.
- [Anthropic authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) and [actual skill-creator](https://github.com/anthropics/skills/blob/b0cbd3df1533b396d281a6886d5132f623393a9c/skills/skill-creator/SKILL.md): remove unproductive instructions and test real behavior. Its full evaluation UI is an implementation choice, not a dependency to copy.
- [Superpowers writing-skills](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/writing-skills/SKILL.md): a maintainer reports workflow summaries in descriptions leading to skipped body instructions. This supports keeping procedure in the body, but is not controlled evidence of a universal rule.

The guides differ on exact wording and workflow rigidity. We use capability plus trigger and relevant boundary, not a keyword catalog or one universal template. No scripts, invocation-policy changes, mandatory plugin layer, or new skills are needed. Existing names are retained for compatibility; titles explain their job in ordinary language.

## Validation

In progress. Metadata selection will be distinguished from actual host loading, and fresh use from measured comparative effectiveness. No general quality, reliability, token, or productivity gain is claimed.
