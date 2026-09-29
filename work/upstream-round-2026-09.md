# Upstream and blind-spot review — September 29, 2026

The owner pointed out that the first harness scan missed GitHub spec-kit, Speck's original inspiration. The first scan covered model-lab guidance and a few papers. It did not establish coverage of the field. This round examined shipped methods, independent counterevidence, and our own instructions as well.

## Coverage and decisions

| Source checked | What it contributes | What Speck takes, and what it leaves |
|---|---|---|
| [spec-kit v1.0.13](https://github.com/github/spec-kit/releases/tag/v1.0.13), released September 29; source `59ab5434e3dda38ad598038b94b4f23139078a23` | Separate SDD, bug-repair and idea-assessment entry points; a lean preset; extensions, presets, resumable workflows and bundles. Its [own SDLC](https://github.com/github/spec-kit/blob/59ab5434e3dda38ad598038b94b4f23139078a23/docs/guides/agentic-sdlc.md) explicitly mixes agents, ordinary automation and human decisions. | Independent task entry agrees with v7. Clarify that assessment can end without a build. Do not import a workflow engine, fixed artifact sequences, or catalog merely because upstream offers them. |
| spec-kit [converge command](https://github.com/github/spec-kit/blob/59ab5434e3dda38ad598038b94b4f23139078a23/templates/commands/converge.md) and [bug verification](https://github.com/github/spec-kit/blob/59ab5434e3dda38ad598038b94b4f23139078a23/extensions/bug/commands/speckit.bug.test.md) | Completion marks are not proof. Convergence checks missing, partial, contradictory and unrequested work. Bug verification returns to the reported symptom. | Make those checks explicit within existing build/review behavior. No new convergence phase or three-command repair ritual. Code inspection alone still cannot establish runtime correctness. |
| spec-kit [contract-driven development](https://github.com/github/spec-kit/blob/59ab5434e3dda38ad598038b94b4f23139078a23/docs/guides/contract-driven-development.md) | Interfaces need observable obligations, one authoritative source, consumer agreement and verification of real participants. It explicitly does not implement automatic cross-repo orchestration. | Add conditional interface guidance to mapping, reusing existing types/examples/tests. No schema registry or architecture migration. |
| [OpenSpec v1.13.2](https://github.com/Fission-AI/OpenSpec/releases/tag/v1.13.2), September 23; source `d4e1c77ebae0bd96a7c649fa35edef997989450a`, September 28 | Its [reconciliation implementation](https://github.com/Fission-AI/OpenSpec/blob/d4e1c77ebae0bd96a7c649fa35edef997989450a/src/core/specs-apply.ts#L542) detects conflicting operations and lost scenarios; [archive](https://github.com/Fission-AI/OpenSpec/blob/d4e1c77ebae0bd96a7c649fa35edef997989450a/src/core/archive.ts#L1838) validates rebuilt specifications before writing. | Explicitly preserve unrelated promises when revising direction. Our plain-language records have no universal schema, so no claim of equivalent mechanical enforcement; a structural checker is deferred until a real project needs it. |
| [Superpowers v6.4.2](https://github.com/obra/superpowers/releases/tag/v6.4.2), September 25; source `8ca22dba9a94f28898bbce59f2537ff4d87c747d` | Its [review-package helper](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/subagent-driven-development/scripts/review-package) validates base/head ranges and supplies the whole net change. Its [release notes](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/RELEASE-NOTES.md) report cheaper plans from interfaces/assertions instead of code-heavy scripts. | Specify a whole-task review boundary, including working-tree claims and relevant unchanged context. No new helper yet: the existing Git commands suffice. The planning measurements are maintainer reports, not general effectiveness proof. Do not adopt fixed review rounds or controller authority over owner decisions. |
| [METR productivity update](https://metr.org/blog/2026-02-24-uplift-update/), February 24 | Real repository work exposes selection bias and difficulties measuring concurrent agent use. METR says the newer speedup estimates are unreliable; its older slowdown cannot simply describe today's tools. | Harness comparisons claiming effort savings must account for human attention and review/rework, with task selection stated. No speedup or slowdown percentage is generalized to Speck. |
| [SpecBench v2](https://arxiv.org/html/2605.21384v2), September 9 revision | Visible feature tests can pass while compositions of the same specified behavior fail. More visible composition tests did not consistently fix the gap. Deliberate exploits were rare relative to compositional failure. | Exercise fresh combinations when the affected job involves interacting features. Do not claim more tests reliably solve the problem, or label every failure deliberate gaming. These are constructed systems tasks, not product adoption evidence. |
| [SlopCodeBench v2](https://arxiv.org/html/2603.24755v2), May 7 revision; [public runner](https://github.com/SprocketLab/slop-code-bench) | Successive requirements expose degradation missed by one-shot delivery tests. Quality prompting alone did not prevent it in the studied agents. The benchmark deliberately selects hard iterative Python tasks. | Include a subsequent change and retained behavior when evaluating claims about continuing product work. No universal upfront architecture campaign or generalized failure rate. |

External source inspection establishes published mechanisms and results, not effectiveness in Speck. No upstream package or workflow was installed or executed. Sources were selected for ancestry, adjacent implementations, independent evaluation, and direct relevance to the owner's complaint; popularity or recency alone was not the inclusion rule.

## Local findings and repair

1. Source selection was too narrow. Add an on-demand research reference that includes predecessors, working alternatives, independent challenges and local user evidence; report meaningful omissions. This is a conditional tool, not a research gate on ordinary work.
2. The shaping question reference still unconditionally said to rethink products that function without a model. That conflicts with v7's user-intent scope. Make AI-specific questions conditional on agreed product direction, preserving actual AI promises where they exist.
3. Existing review guidance named a commit but did not make the full task boundary explicit. Add base/head and claimed uncommitted scope, plus checks against original intent rather than completion marks.
4. Existing runtime and proportionality rules remain. Clarify bug reproduction, interface obligations, composed behavior, and the human/continuing-work dimensions of harness comparisons within the skills that already own them.

No new skill, phase, scheduler, runtime service, or dependency. One on-demand reference is added. The installer implementation is unchanged; tests retain 7.0.1 as a supported source for the 7.0.2 patch.

## Limits

Coverage remains selective. We did not compare private production harnesses, run a platform/IDE benchmark, inspect every community extension, or validate host-level sandboxing and permission enforcement. Those are distinct runtime concerns; adding prose here cannot establish them. We did not perform a controlled before/after effectiveness comparison. Research-backed guidance is **unbenchmarked**, not a demonstrated quality or productivity improvement.

## Validation

Accepted candidate `ddcbf347e2cc125085b48d1e9eafaeeb737b677d`. The method has 18 files / 34,042 bytes; `AGENTS.md` is 7,489 bytes. Installed SHA-256: `1422a90272fd694f177600eaf8f6239befd3c9f69a325e8f8879f3f0ac421af6`.

A fresh independent reviewer accepted the patch without substantive blockers. It ran the ten installer tests successfully (31.221 seconds, exit 0), including 44 supported-version/product combinations, packed installation, preservation/refusal and rollback. Package inspection and a fresh install verified the added reference, all three incoming links and the Codex discovery link. Its source spot-checks covered spec-kit convergence, the Superpowers review helper and METR's measurement limits. This was a fresh context, not a different model family; it did not independently recheck every release detail.

Two bounded uses ran:

- A fresh shaping context was asked for a short durable brief for an offline personal swimming log, explicitly without AI, accounts or cloud and without building an app. It produced only `product.md`, preserving the requested boundary. The independent reviewer accepted its fit to that raw request. This demonstrates one case, not general proportionality.
- The reviewer exercised a synthetic two-commit taskbook change. Both supplied tests passed, but a fresh combination showed creation-time ordering including completed rows in an open-task list. The defect lived in the first commit; the second changed only README completion claims. The reviewer inspected the full base/head range and rejected completion on the executed result. The fixture stayed unchanged. This tests the full-change/combined-behavior path without claiming a before/after gain over 7.0.1.

Local raw subjects: `/tmp/speck-702-offline-trial/product.md` and `/var/folders/f7/by4sp65x1pj0kyz1rm27085h0000gn/T/speck-702-review-m04f29vl/review-subject`. Fixture base `5a6f8e739788ad26b59c3526b24c0f9b0cd789d2`, reviewed head `b6d6703dd1ee15e9c9dd3a19036017dc95306c2a`. Final-source installation independently matched the expected digest and created no product record.

## Release and adoption

[v7.0.2](https://github.com/Keegil/speck-next/releases/tag/v7.0.2) was published and read back on September 29. The annotated tag resolves to `f84f73d2e556abce98470e18001ea64c225f1a3d`. A fresh `npx -y github:Keegil/speck-next#v7.0.2 install <git-fixture>` matched all 18 canonical files and the reviewed digest, resolved Codex discovery, and created neither product nor map records.

| Checkout | Branch | Pushed commit |
|---|---|---|
| Odd | `codex/odd-preparation-app` | `fecf42636efdbbf61155a1f1f74438f5e3cefb30` |
| Splang Slack | `main` | `9b784bacaba51e14497b1a9135462ca84b8105c7` |
| Odd p2r review | `codex/odd-p2r-review-resume-20260908` | `a0b8a4a5bd24fb8a1aada360b083edc23b920c2f` |
| Odd boka review | `codex/odd-boka-visual-20260908` | `ab2595f8b6187aa4b151f4c37b418434e1894a3c` |

The upgrade worker preserved 2,842 tracked owner fingerprints, 14,263 untracked paths and exact original dirty statuses. The integrator independently compared all 72 installed canonical files, markers/digest, nine-path-only commit scopes, original dirty statuses and remote branch SHAs. No additional native adopter was found; local snapshots and test subjects were excluded. Local evidence: `/tmp/speck-702-rollout-summary.json`, `/tmp/speck-702-rollout.json`, `/tmp/speck-702-rollout-verified.json`. The existing adoption request is fulfilled for this patch.
