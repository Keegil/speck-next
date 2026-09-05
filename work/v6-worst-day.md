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

---

# Repaired-candidate continuation — `ca33c64`

**Dispatch:** focused repair receipt committed at `5c214fa`; same worst-day tester and persona, continuing the record without rewriting the original false-green controls.
**Candidate:** exact archive of repair commit `ca33c64`, package `6.0.0`; `bin/speck-next.js` SHA-256 `ea3f2f818763cbb0c2be00090dac3139d1b12a6a81fefcf3b2b0d16598f09674`; `package.json` SHA-256 `0779eace19cf9d67bac5f3ac7c5cfca2a413ad65e29fb34c247a893ce908e413`.
**Execution:** the authentic local `v5.4.1` tag installed the generic starting repository. The live piece, owner history, and dirty unrelated note were the same bytes used by the original record. The measured population ran once in 2.8 seconds with no model, host, Claude, network, retry, fallback, owner interruption, source edit, or product build.

The candidate and v5 source were extracted without modification, then every product action used the repaired real CLI:

```sh
git archive ca33c64 | tar -x -C /tmp/speck-v6-worst-day-repair.aXjeLH/candidate
git archive v5.4.1 | tar -x -C /tmp/speck-v6-worst-day-repair.aXjeLH/v5-kernel
node /tmp/speck-v6-worst-day-repair.aXjeLH/v5-kernel/bin/speck-next.js install /tmp/speck-v6-worst-day-repair.aXjeLH/pre-v6
node /tmp/speck-v6-worst-day-repair.aXjeLH/candidate/bin/speck-next.js upgrade /tmp/speck-v6-worst-day-repair.aXjeLH/<subject>
```

As before, a whole-repository snapshot hashes every non-`.git` path, path kind, mode, and file byte together with `git status --porcelain=v1 -z --untracked-files=all`. Every subject carried dirty `owner-notes.txt` bytes with SHA-256 `7b6c9cb6b9495234f79b0d8ce5f6bff7878dc28e722746fec8b02dae1d88a5f4`.

## Repaired walk 1: pending remains bounded and repeatable

The v5.4.1 upgrade exited `0`, preserved the original product as an exact prefix, and produced exactly one pending assessment. It printed:

```text
Product team migration: preserved historical product bytes and appended one explicit pending upgrade assessment.
Next: review the reported paths and complete diff, commit the upgrade, then complete work/product-team-assessment.md by following “Finish an upgrade” in AGENTS.md.
```

The expected method migration changed the whole snapshot from `ea23e655d104e39720147b373e6dc1068d26d78523182514ed564f0b24302699` to `f5926684b94da94aa4a4a6b585b299db5f088eeddde37b0dee3031e456d7a316`. The owner's surrounding history did not change:

| Subject | Before | After |
|---|---|---|
| `map.md` | `068476502ec08a08178820f16e054cd70ffea5333cef9cb959501dc0361b25e1` | same |
| `state.md` | `bb33b8f40e8a5a350e6838bfbed95b5a7dfb24884f4b0723e428dcdc6caa09d6` | same |
| `work/feature-alpha.md` | `2710b6c927878c46a572085a8b78bccb9506dae7c7d4d9002032a4c415701d3b` | same |
| dirty `owner-notes.txt` | `7b6c9cb6b9495234f79b0d8ce5f6bff7878dc28e722746fec8b02dae1d88a5f4` | same |

The second pending upgrade exited `0`, printed no Shape, Map, or resume route, and left snapshot `f5926684b94da94aa4a4a6b585b299db5f088eeddde37b0dee3031e456d7a316` identical before and after. Its next action remained completion of the one assessment record.

## Repaired walk 2: every invalid completion fails closed

Each invalid subject began from the committed pending migration, a structurally complete `product.md`, the same live Feature Alpha state, and the same dirty unrelated byte. Every command exited `1`, emitted `Nothing in the repository changed.`, preserved its whole-repository snapshot exactly, and contained no instruction to continue Shape, continue Map, or resume anything.

| Invalid completion | Whole snapshot before and after | Specific refusal |
|---|---|---|
| Missing record file | `394c9364c4e1f8046feda3594e3e06cf10510f3b817e709d27a0ef91b5d849c0` | `work/product-team-assessment.md is missing` |
| Duplicate canonical `Record` line | `41b8b21137426c533ac614a5a6ac8f2c8c699a853a09d94b9a96cdb68e37a06f` | canonical assessment must contain exactly one named record line |
| Heading-only record | `9588f8076828c25dd180815ffb5ab8508d47dc75207a539bbb0395f2da3c86d1` | all four role headings, Product synthesis, and Route missing |
| Duplicate Product role | `3c3231f3fec21a359650a869705c9e6ed9328a712fa4e55e74c9fc55e7aa9292` | `Product: duplicate heading (2 current sections)` |
| Four roles, one literal carrier | `51c7efe0726359debc60c1f79349b04bb558b7dd95060e1416b245cdc96e4b03` | all four roles use identity `one-host-session` |
| Disguised shared carrier | `773cb646bca15273444b1d5d3b05a476e55fb831e64e4ed530d005c7f85fd401` | all four roles normalize to identity `shared-carrier` |

The repaired same-carrier path now said:

```text
refusing: the completed upgrade assessment cannot proceed because work/product-team-assessment.md is incomplete or ambiguous:
- Carrier: Product and Business and Experience and Engineering use the same identity "one-host-session"
Nothing in the repository changed.
Next: repair work/product-team-assessment.md with four distinct complete role contributions, one Product synthesis, and one Route matching product.md; commit the assessment, product.md, and state.md together, then run the upgrade again.
```

This is the reverse of the original real-CLI false green: the four deliberately distinct action proposals no longer compensate for one carrier. The heading-only and duplicate-role siblings also reverse their original false greens.

## Skeptical attack: hidden carrier equality

I gave Product carrier `shared-carrier`, Business `shared-` + U+200B ZERO WIDTH SPACE + `carrier` surrounded by a tab and spaces, Experience the literal identity surrounded by spaces and a tab, and Engineering `shared-` + U+2060 WORD JOINER + `carrier`. The record remained otherwise complete.

The CLI normalized all four to `shared-carrier`, exited `1`, printed the four-role collision, printed no affirmative route, and preserved snapshot `773cb646bca15273444b1d5d3b05a476e55fb831e64e4ed530d005c7f85fd401` exactly. The free attack found no bypass.

## Repaired walk 3: four real carriers resume only the live work

After the missing-record refusal, I supplied one complete record with four distinct carriers, one Product synthesis, and `Route: Resume Feature Alpha from state.md.` The same real command exited `0`:

```text
Product team migration: kept the explicit complete upgrade assessment; product.md was unchanged.
Working-tree changes across the complete installed surface plus product.md: none.
Complete installed-surface plus product.md diff: empty.
Next: there are no upgrade changes to commit; resume Feature Alpha from state.md.
```

Snapshot `4eae9830666f18874af5c147cf4b927fc19d56725a0f91fb9623fd42a24e616f` was identical before and after. Product, map, state, live-work, and dirty-note hashes all matched. The CLI reopened neither Shape nor Map, invented no backfill, and named only the live piece already present in `state.md`.

The second resume produced byte-identical stdout, SHA-256 `892912a1f4efb7dee8864905772a599ab2052c9f0df899bac6f4321b69b87a42`, and preserved the same whole snapshot. Valid repair/resume is idempotent.

## Continuation finding

The original concrete product defect is repaired on the exact `ca33c64` CLI. All three prior false-green shapes now refuse on the real path, their missing-record and duplicate-record siblings remain atomic, the normalization attack fails closed, and the valid control still reaches the existing live piece without altering history. This continuation found no new concrete product defect in its focused migration scope. Package transport, native host discovery, concurrent upgrades, remote fetch loss, and filesystem permission loss were not part of this focused receipt and were not re-judged here.

The disposable generic repositories, extracted candidates, and harness were moved to Trash after capture.

## Continuation verdict

**KEEP — the repaired worst-day migration is sufficient on this focused scope.** Walk 2 earns the change in verdict: the exact malformed, duplicate-role, and same-carrier records that the original candidate blessed now refuse before any byte changes or route appears, including the whitespace/default-ignorable disguise. Walks 1 and 3 keep the other half honest: pending remains bounded, and a genuinely complete four-carrier record resumes Feature Alpha twice without changing live work, history, or the dirty unrelated file. The original failure remains in this record as its control; `ca33c64` reverses it without breaking the valid path.
