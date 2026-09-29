# State

## Current work — September 29

The owner requested a quick current-research check. The 7.0.1 guidance patch is accepted: independent review, ten installer tests, final refinement review and source-install smoke check completed. Method candidate `93ce912`; digest `f57becee9e3688f6a0c1e0d08f13ca3a0666b121c0fb382d10b41c97a563119c`. See [work/harness-refresh-2026-09.md](work/harness-refresh-2026-09.md) for primary sources, changes, and limits. Next: publish and propagate the accepted patch to existing Speck Next checkouts. No behavioral improvement has been measured.

## Speck Next v7.0.0 released — September 25

**Proportionate work is released as v7.0.0.** The public GitHub release and remote annotated tag were read back successfully; the tag resolves to `3852067d7d4aa1c950db5be3ae5ad57a3130fc4f`. The owner requested a major release because overhead made smaller projects unattractive. The new method chooses planning, records, expertise, checks and review for the task rather than enforcing fixed phases and rosters.

The accepted candidate is `fa1ead7`; installed method SHA-256 is `b13f6e10f4069b641dccb2f38f3bf73a82d23a224c6ab11d4091905b37742b96`. Only release documentation/evidence has changed since it was tested.

## What ran

- The independent reviewer ran `python3 devsuite/proportional-v7/check.py`: ten tests OK, including source/packed installs, owner-record preservation, supported upgrade states, refusal and forced rollback. Its hardlink attack also preserved owner bytes.
- A fresh builder completed a small CLI with one script and no method paperwork. Another added tenant-isolated CSV export with nine tests while preserving an unrelated failed-dashboard hold. Independent review exercised and accepted both results.
- The shipped method source measures 28,271 bytes versus 90,291 at `a1b3840`, a 68.7% reduction. This does not establish runtime cost savings.

Commands, failed interim checks, contributor returns, raw cost fields, method-use records and independent judgment: [work/proportional-v7.md](work/proportional-v7.md). The token estimate was exceeded in reported cached-input categories; the bounded context/elapsed scope held. No further build is commissioned by that cost finding.

## Limits and next action

The owner subsequently requested adoption everywhere already using Speck Next. Odd, Splang Slack and both existing Odd worktree checkouts are now upgraded, committed and pushed; the work record lists their exact branches and commits. Independent verification preserved all project records and pre-existing edits, and GitHub read-back confirms v7.0.0 at each pushed commit. Next consumer: normal product work in these upgraded checkouts. `npx -y github:Keegil/speck-next#v7.0.0 install /tmp/speck-v7/released-install` completed from the published tag; assertions confirmed version 7.0.0, the exact reviewed method digest, working Codex discovery, and no generated product/map files. No further kernel work is started automatically. Independent review was pre-scheduled in the two use trials; spontaneous reviewer recruitment, broader UI/large-product behavior, comparative cost and durable adoption remain unproved. No known blocking defect remains. Old-Speck unmarked conversion is deferred.

The previous v6 and September 12 evidence retains its original scope. A repaired Odd GUI and resolving interaction run remain that product's work, not claims made by this release. Existing untracked local artifacts are unrelated and excluded.
