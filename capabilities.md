# Capability evidence

Each result below names the version it measured. Historical success does not automatically establish the same behavior after later changes. The current package version is in [package.json](package.json); release status is in [state.md](state.md).

| Area | Evidence | Limits |
|---|---|---|
| Release consistency and footprint | 7.0.4: nine guard-control tests passed independently and on GitHub at candidate `18f2491`. The installed method has 19 canonical files, a marker and one discovery link, within the stated limits. [Record](work/consistency-2026-09.md). | Static checks cannot establish product quality, automatic skill selection, or effective context use. |
| Installation and preservation | 7.0.4: ten installer tests passed, including 52 version/product combinations, complete source/packed parity, owner records, refusal and rollback. [Record](work/consistency-2026-09.md). | Native marker-bearing versions through 7.0.4 were exercised. Old-Speck conversion is not implemented. |
| Template handoff | 7.0.4: a fresh context used the revised state template to record the actual dirty working tree, an uncovered behavior gap and an executed next command. The integrator read back the same result. [Review](docs/reviews/consistency-7.0.4.md). | One synthetic paused task; not a complete second-agent implementation or a general resumption reliability measure. |
| Skill use | 7.0.3: independent use produced an actionable plan without document prerequisites and found a filtering defect while including an uncommitted repair. Five manifests validated. [Record](work/skills-refresh-2026-09.md). | Two synthetic uses. Twelve description-selection examples were simulations, not observed host activation or a reliability estimate. |
| Small and consequential work | 7.0.0: a small CLI used no method paperwork; tenant-isolated CSV export preserved existing behavior and an unrelated failure hold. [Record](work/proportional-v7.md). | CLI and module-boundary examples, not broad UI, production security, or long-running product evidence. |
| Independent review | 7.0.0 used a separate Claude reviewer; later patches used non-contributing native contexts to review scoped changes and execution evidence. [Latest skill review](work/skills-refresh-2026-09.md). | Reviews were arranged explicitly. Spontaneous reviewer recruitment and cross-model consistency remain unproved. |
| Host discovery | Source and packed installation checks resolve Claude and Codex to the same five canonical skills. | Correct files and aliases do not establish how each host selects or follows a skill. |

Run `bash devsuite/run.sh` for current deterministic checks, including fresh installed size. Exact release measurements, candidate SHAs and digests remain with their [versioned records](docs/history/v7.0.3-records.md).

The live product-quality questions are usability, sustained correctness after further changes, owner rework, and total operating cost. They require ordinary product use and suitable comparisons; listing them does not commission another campaign.
