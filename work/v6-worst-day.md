# v6 worst-day migration record

**Date:** 2026-09-06  
**Persona:** the owner of a generic mid-product repository on a bad day: Feature Alpha is live, its work record matters, an unrelated tracked note is dirty, and the upgrade must either preserve all of that or refuse without leaving residue.  
**Tester:** `/root/v6_worst_day`, the fresh tester named in the committed combined receipt. I contributed to none of the product, implementation, role work, prior tests, or judgments.  
**Product under test:** the real `bin/speck-next.js` at workspace commit `9e8145621e36bff0a5361c1447ff857caf4ddca5`, package `6.0.0`, SHA-256 `2a1058e5fb874aac647d8fe4e9490fd6eb3b248a1b23174e7f92b14e4f9f0888`. `git diff --exit-code c2912e7..HEAD -- bin/speck-next.js package.json` returned zero, so these are the receipt's candidate upgrader and package bytes.  
**Starting product:** a local install made from the repository's authentic `v5.4.1` tag, with generic `product.md`, `map.md`, `state.md`, `work/feature-alpha.md`, and `owner-notes.txt`. The state said Feature Alpha was live. `owner-notes.txt` had an uncommitted unrelated edit before every measured upgrade path. No private product name, fact, or file entered the fixture.

## Authorization and limits

Before the first product run I read 10 repository files: the experience skill and worst-day reference, `AGENTS.md`, the combined receipt, `product.md`, `map.md`, `state.md`, `package.json`, the real upgrader, and the migration-checker source used only to construct a realistic v5 marker and record shape. This stayed below the receipt's 20-file limit. I made no model or nested-host call, used no network fallback, asked the owner nothing, and rebuilt no product. The measured local CLI population completed in 3.1 seconds.

One pre-measure fixture control exposed that Node's recursive copy had rewritten the installed relative Codex-skill link as an absolute link. I excluded that contaminated fixture, changed only the disposable copy operation to preserve the link byte-for-byte, and ran the measured population once. No candidate conclusion below uses the contaminated control.

## Setup and commands

The install and every migration invoked the real CLIs directly, avoiding package-fetch behavior so the subject was the upgrader rather than the network:

```sh
node /tmp/speck-v6-worst-day.YbFmaz/v5-kernel/bin/speck-next.js install /tmp/speck-v6-worst-day.YbFmaz/rerun/pre-v6
node /Users/kjetil/Code/speck-next/bin/speck-next.js upgrade /tmp/speck-v6-worst-day.YbFmaz/rerun/pending
node /Users/kjetil/Code/speck-next/bin/speck-next.js upgrade /tmp/speck-v6-worst-day.YbFmaz/rerun/missing-record
node /Users/kjetil/Code/speck-next/bin/speck-next.js upgrade /tmp/speck-v6-worst-day.YbFmaz/rerun/duplicate-record-line
node /Users/kjetil/Code/speck-next/bin/speck-next.js upgrade /tmp/speck-v6-worst-day.YbFmaz/rerun/malformed-record
node /Users/kjetil/Code/speck-next/bin/speck-next.js upgrade /tmp/speck-v6-worst-day.YbFmaz/rerun/duplicate-role
node /Users/kjetil/Code/speck-next/bin/speck-next.js upgrade /tmp/speck-v6-worst-day.YbFmaz/rerun/same-carrier
```

Each reported repository snapshot hash covers every non-`.git` path, path kind, mode, and file byte plus `git status --porcelain=v1 -z --untracked-files=all`. A matching before/after hash therefore includes the dirty unrelated edit rather than overlooking it.

## Walk 1: v5.4.1 enters one bounded pending assessment

The first `pending` command exited `0`. Its operative output was:

```text
Product team migration: preserved historical product bytes and appended one explicit pending upgrade assessment.
Next: review the reported paths and complete diff, commit the upgrade, then complete work/product-team-assessment.md by following “Finish an upgrade” in AGENTS.md.
```

The original `product.md` bytes, SHA-256 `a11393a993b3c06a0b9b96eb8c09baaa714abba205acff926340b0f92db021bc`, remained the exact prefix of the migrated product. Exactly one assessment heading and one pending status were added. The marker became `6.0.0` and explicitly named `work/product-team-assessment.md`.

The surrounding work stayed byte-identical:

| Subject | Before | After |
|---|---|---|
| `map.md` | `068476502ec08a08178820f16e054cd70ffea5333cef9cb959501dc0361b25e1` | same |
| `state.md` | `bb33b8f40e8a5a350e6838bfbed95b5a7dfb24884f4b0723e428dcdc6caa09d6` | same |
| `work/feature-alpha.md` | `2710b6c927878c46a572085a8b78bccb9506dae7c7d4d9002032a4c415701d3b` | same |
| dirty `owner-notes.txt` | `7b6c9cb6b9495234f79b0d8ce5f6bff7878dc28e722746fec8b02dae1d88a5f4` | same |

Running that same pending command again exited `0`, said it kept the explicit pending assessment, and left the complete snapshot exactly `8576cc1d25f3b85b0204ddaa2a5a04160589a508395d2052c09d066c54b6136a` before and after. As this owner, that felt calm: my live work did not move, history was not rewritten, and the next action was singular.

## Walk 2: missing and duplicate canonical evidence refuse atomically

I changed the assessment status to `complete — resumed Feature Alpha from state.md`, supplied a structurally complete four-role `product.md`, but omitted the named record. The real command exited `1`:

```text
refusing: the upgrade assessment says complete, but work/product-team-assessment.md is missing.
Nothing in the repository changed.
Next: restore consistent assessment evidence, then run the upgrade again.
```

The full snapshot was `c5bf4d2ff44594c1357b844afa9c119d5b409be8339bdb72f6dc3bfa27c5de00` both before and after. It gave no resume instruction.

I separately duplicated the canonical `**Record:** work/product-team-assessment.md` line while a record file existed. The command exited `1`, said the canonical section must contain exactly that one record line, and left full snapshot `61bb827df9fd5e250bba82aeb72bb84ccfad39991571e2e645354b65c73ce230` unchanged. This also gave no resume instruction. Both refusals preserved the dirty unrelated edit and every existing owner byte.

## Walk 3: repair, resume, and repeat

After the missing-record refusal, I added a complete generic record with four distinct carriers and four distinct evidence/action contributions, then committed only that assessment evidence. The same real CLI command exited `0`:

```text
Product team migration: kept the explicit complete upgrade assessment; product.md was unchanged.
Working-tree changes across the complete installed surface plus product.md: none.
Complete installed-surface plus product.md diff: empty.
Next: there are no upgrade changes to commit; resume Feature Alpha from state.md.
```

The full snapshot was exactly `0cf723e24ce263de18771ecabbc7a85b45eb69e4e8017bf7224ac6d6fade0f0e` before and after. The individual product, map, state, live-work, and dirty-note hashes also matched before and after. The output reopened neither Shape nor Map, asked for no owner decision, created no backfill, and resumed the live piece already named by `state.md`.

A second complete-assessment upgrade produced byte-identical stdout (SHA-256 `a2d114a55432730bcf7cb4946eaee0f8f7a215089347a2becdb45c44ad5bdc13`) and left the same full snapshot unchanged. Repair/retry and the settled resume path are idempotent.

## Walk 4: the real upgrader accepts fabricated separation

I kept `product.md` structurally complete and the resume status valid, then attacked only `work/product-team-assessment.md`.

Three invalid records all exited `0`, were described as an “explicit complete upgrade assessment,” and ended with `resume Feature Alpha from state.md`:

| Record attack | Before/after snapshot | Actual result |
|---|---|---|
| File contains only a heading and “This is not a role assessment record.” | `63a2299d5f11897ae47bd97a01b475371edb5d4ccab256ab06d0fc16d6cefc52` | Accepted |
| Five role sections because Product appears twice | `9faa8cc88ac7a3c356fcce9a637b10613615e32023bfd868c904e1bb74e37c70` | Accepted |
| Exactly four role headings, but every `Carrier:` is `one-host-session` | `cdc6ec236d01c7395a2975b6e8b8afacbeb4c433fddca43096664066faf9a937` | Accepted |

The crucial same-carrier output was:

```text
Product team migration: kept the explicit complete upgrade assessment; product.md was unchanged.
Working-tree changes across the complete installed surface plus product.md: none.
Complete installed-surface plus product.md diff: empty.
Next: there are no upgrade changes to commit; resume Feature Alpha from state.md.
```

That record contained exactly one heading for Product, Business, Experience, and Engineering and four occurrences of the same carrier. To isolate carrier identity from duplicate prose, the four proposed actions were deliberately distinct:

- Product: keep Feature Alpha live and preserve its order.
- Business: keep the existing zero-cost adoption path.
- Experience: preserve the one-step import journey.
- Engineering: resume the existing parser implementation.

The CLI still accepted it. It likewise accepted a record with no contributions at all and one with a duplicated role section. The stable before/after hashes show this is not corruption or transaction residue; it is a false-green admission decision on the real shipped path.

## Finding

**Concrete product defect — release blocker:** a completed mid-product upgrade validates the structural Product-team rows in `product.md` and the existence of `work/product-team-assessment.md`, but it does not validate the assessment record's required fields, one-role-each shape, or distinct carriers. A single context can claim all four roles—or provide no role evidence—and the CLI tells the builder to resume substantial work. This violates the installed promise that four headings from one carrier do not count, and it defeats the upgrade's only gate against fabricated separation. The malformed, duplicated-role, and same-carrier real-CLI runs are three reproductions of one defect class.

Concurrent upgrades, remote package-fetch failure, and a real filesystem-permission loss were outside this receipt's bounded migration walk and remain untested. The direct Node invocation establishes upgrader behavior without claiming network-package behavior.

The disposable generic repositories and harness were moved to Trash after this record was captured.

## Verdict

**SEND BACK.** As the owner on the worst day, I trust the migration's byte preservation, atomic refusals, clear pending state, successful resume, and idempotency because Walks 1–3 ran them and read every relevant byte back. I would not keep or release this v6 candidate yet: Walk 4 shows that the same CLI which correctly blocks a missing file will bless an empty, duplicated, or one-carrier assessment and tell me to resume. That breaks the deal because the milestone's defining product promise is genuine separation, not the presence of a filename. Fix the assessment-record admission on the real upgrader, then re-run this invalid-record population and the preserved valid repair/resume control.
