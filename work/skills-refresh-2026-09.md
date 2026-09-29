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

Method candidate: `42680aef4348be509962eb13f14da3763cf80ae9`; surface SHA-256 `202dd85244864649c2978d4f6c54e82c4d1a4f3f6a8b1baa51ed3ffd1e350a6c`.

- All five entrypoints passed the bundled Codex `skill-creator/scripts/quick_validate.py`. Bodies are 284–410 words. This validates format, not behavior.
- `bash devsuite/run.sh`: ten tests passed in 92.854 seconds, including 48 version/product migration combinations, source/packed installs, owner preservation, refusal and rollback.
- Packed install includes the new reference and resolves all local reference links. Source-install read-back matched all 19 canonical files and the Codex discovery link, without generating product/map files. The first smoke commands correctly refused a missing directory and then a non-Git directory; after creating the disposable Git repository, installation succeeded.
- Surface: 19 canonical files / 37,543 bytes. With the marker, the fresh installation has 20 regular files / 37,796 bytes, plus one directory symlink. The installer's 21 reported entries include that alias. This remains within the existing 20-file/100-KB content ceiling; the ceiling has not changed.

### Description selection

Two separate non-contributing contexts received the old or new five-skill metadata and the same 12 requests. They did not read bodies or the other return. Each chose an immediate set and any later skill needed; order within a set is immaterial. These are single metadata-selection simulations, not actual host activation measurements or reliability estimates. The old selector had researched general authoring guidance; the new selector had previously exercised the old shaping method in another task. Neither authored this patch. Their contexts were not experimentally identical.

| Request | Old selection | New selection |
|---|---|---|
| Correct an existing confirmation-label typo | craft | none |
| Short offline, non-AI hiking-log brief in chat | shape → experience + judge | shape |
| Divide an agreed CSV/worker/status flow between contributors, no product file | map → experience + judge | map → judge |
| Review a five-commit PR | judge | judge |
| Improve a cramped settings layout and save/error states | craft → experience + judge | craft → experience + judge |
| Exercise sandbox checkout decline and retry | experience | experience |
| Explain an existing debounce helper without edits | none | none |
| Implement agreed payment-webhook deduplication | implementation → experience + judge | implementation → experience + judge |
| Research whether to keep or stop a project; no build | experience + judge later | shape → judge |
| Independently try and accept a recurring-booking change | experience + judge | experience → judge |
| Add one gitignore entry | none | none |
| Independently review a tenant-isolation proposal | judge | judge |

The useful observations are fewer irrelevant workflow selections on a typo, short brief, and planning task, plus explicit discovery for a product-direction assessment. These examples do not establish a general improvement rate. Substantive deliverables still require independent review under the kernel; the selectors' planned choices are not acceptance records.

### Forward use from raw requests

A non-contributing reviewer received an exported packet pinned to the candidate, the user request, and raw trial materials, without the intended answer, suspected defect, other reviewers' outputs, or author conclusions.

1. **Plan from a chat brief:** it selected `map-build`, returned an actionable CSV-import plan for two contributors, assigned interface ownership and integration, and included real retry/no-duplicate checks. It required no product file, shaping interview, new platform, or routine owner approval. The request supplied no actual application checkout, and the plan did not pretend to inspect one.
2. **Review the delivered working tree:** it selected `judge` and used targeted execution without a separate experience workflow. Fixture base `a5eb37533ca7b0c33fae97ddc625e7e6e43ffd5c`, head `7b7213dbbffbc11a3dbb710a70a42084f6f8bb02`; the final commit only documents the change. The claimed uncommitted function was `return [row for row in rows if row["stock"] > 0 and (category is None or row["category"] == category)]`. The request required case-insensitive category filtering and preservation of stock filtering. Both supplied tests passed; fresh mixed-case probes failed. The reviewer found that defect while correctly recognizing that the uncommitted change had already repaired the committed zero-stock regression. Its source SHA-256 was `95f01651cb2b0a9fc1df7cc646807e7297f71950e5217effbf4314f911c4c449`.

Raw local materials and returns: `/tmp/speck-skills-703/`, with separate catalogs, requests, source smoke, package check, installer log, versioned fixture, and `review-results/`. These are bounded synthetic examples, not a before/after execution comparison. Native Codex contexts were used; a new Claude runtime trial and cross-model review did not run. No general quality, reliability, token, or productivity gain is claimed.

## Release and adoption

Independent reviewer accepted `42680aef4348be509962eb13f14da3763cf80ae9` with no substantive blocker. It also reran the ten installer tests successfully in 33.471 seconds and verified a packaged installation.

[v7.0.3 is published](https://github.com/Keegil/speck-next/releases/tag/v7.0.3). The remote annotated tag resolves to `d7cd35db89560560b60fece5095f2688c5fae2c2`, which changes only validation records after the accepted method candidate. Installation through `npx -y github:Keegil/speck-next#v7.0.3 install` matched all 19 canonical files and the expected digest, resolved the Codex adapter, and generated no product/map files.

All four existing native adopters were upgraded, committed and pushed, with remote SHA read-back:

| Checkout | Upgrade commit |
|---|---|
| `/Users/kjetil/Code/odd` | `7a32764052465f3e7b2ca8c748da6e3e33e218a7` |
| `/Users/kjetil/Code/telum/splang-slack` | `3ea91af6fa5b4a6a77e05e4f17b35f92e85fa9dc` |
| `/Users/kjetil/Code/odd-worktrees/p2r-review-20260908` | `7a0590a8c92c0683ba08ee8f2717c3927b7780ca` |
| `/Users/kjetil/Code/odd-worktrees/boka-visual-20260908` | `1ab44bcac6f7726b075521f2599294cdfe98a3ac` |

The rollout verified 76 canonical byte matches, all markers/digests and both host skill paths. It preserved 2,842 tracked owner fingerprints, 14,263 untracked paths, index state during upgrade, and original dirty statuses. Each commit has nine method paths. The integrator separately rechecked every current canonical file, checkout HEAD, marker version and original status. App tests were not rerun for instruction-only copies. Local proof: `/tmp/speck-skills-703/rollout-verified.json` and `published-smoke.json`.

Next consumer: ordinary work in these checkouts. No further optimization campaign is commissioned.
