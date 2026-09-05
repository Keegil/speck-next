# v6.0.0 fresh product-builder run

**Tester:** Codex product builder, fresh context `/root/v6_product_builder` · **Date:** 2026-09-06 · **Candidate:** `c2912e738c57218d23b574e5684c3aad026d2c07` · **Built:** `fff561e7da52c4cec0e385b10b0ba7bc061a585b` · **Receipt:** `9e8145621e36bff0a5361c1447ff857caf4ddca5`

I contributed to none of the product roles, implementation, tests, or prior judgments. I read the candidate's `product.md`, `map.md`, `state.md`, installed `AGENTS.md`, five skills, templates, and the source changes in `32b1ba2`, `3a39e3e`, and `c2912e7`. I did not read `work/separated-product-team.md`. I made no model or host call, did not rebuild either Pulse implementation, and wrote no product source.

## Candidate and subjects

I exported the candidate instead of running the controls against the live working tree:

```text
$ git get-tar-commit-id < /tmp/speck-v6-exact.iEwlBH/c2912e7.tar
c2912e738c57218d23b574e5684c3aad026d2c07
$ shasum -a 256 /tmp/speck-v6-exact.iEwlBH/tree/devsuite/tasks/separated-product-team/check.py
ad945d1c9b3bd2f19240be4f4f49d3b2ad045593299e27a5357e0997a43f3b52  /tmp/speck-v6-exact.iEwlBH/tree/devsuite/tasks/separated-product-team/check.py
```

The Built and receipt commits follow the candidate and do not add product implementation:

```text
$ git show --format='%H %s' --name-status --no-renames fff561e
fff561e7da52c4cec0e385b10b0ba7bc061a585b Mark the exact v6 candidate Built

M       state.md
$ git show --format='%H %s' --name-status --no-renames 9e81456
9e8145621e36bff0a5361c1447ff857caf4ddca5 Open the combined v6 release hearing

M       work/separated-product-team.md
```

The preserved products were clean after use. The governed tree's later commit records the failed v0.9 run; `pulse.py` is unchanged from `f439c81`.

```text
$ git -C /tmp/speck-v6-native.PYVE5a/governed-pulse rev-parse HEAD && git -C /tmp/speck-v6-native.PYVE5a/governed-pulse status --short
f87516a0627aa9970b01b30b65fe721cc969b98b
$ git -C /tmp/speck-v6-native.PYVE5a/baseline-pulse rev-parse HEAD && git -C /tmp/speck-v6-native.PYVE5a/baseline-pulse status --short
014deefb52a0041fdc8fafe20698ab5cf078887a
$ git -C /tmp/speck-v6-native.PYVE5a/governed-pulse diff --stat f439c81..HEAD -- pulse.py
[no output]
```

## Fresh journals

I used paired files so each implementation received the same data:

```text
mixed
{"2026-08-31":4,"2026-09-02":2,"2026-09-05":5}

complete
{"2026-08-31":1,"2026-09-01":2,"2026-09-02":3,"2026-09-03":4,"2026-09-04":5,"2026-09-05":4,"2026-09-06":3}

empty
{}
```

The machine date for these runs was:

```text
$ date '+%F %Z'
2026-09-06 CEST
```

Initial hashes were `beeb0d…7609` for each mixed file, `5811b2…e0a` for each complete file, and `ca3d16…356` for each empty file.

## Using `pulse week`

Mixed week:

```text
$ cd /tmp/speck-v6-native.PYVE5a/governed-pulse
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/governed-mixed.json python3 pulse.py --date 2026-09-06 week
Siste sju dager
man 31. aug  4
tir 1. sep  ikke logget
ons 2. sep  2
tor 3. sep  ikke logget
fre 4. sep  ikke logget
lør 5. sep  5
søn 6. sep  ikke logget
[exit 0]

$ cd /tmp/speck-v6-native.PYVE5a/baseline-pulse
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/baseline-mixed.json python3 pulse.py week
Last 7 days · 2026-08-31 to 2026-09-06
▆  ·  ▂  ·  ·  █  ·
m  t  w  t  f  s  s
Logged energy: 2–5. · marks a gap; gaps stay gaps.
[exit 0]
```

Complete week:

```text
$ cd /tmp/speck-v6-native.PYVE5a/governed-pulse
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/governed-complete.json python3 pulse.py --date 2026-09-06 week
Siste sju dager
man 31. aug  1
tir 1. sep  2
ons 2. sep  3
tor 3. sep  4
fre 4. sep  5
lør 5. sep  4
søn 6. sep  3
[exit 0]

$ cd /tmp/speck-v6-native.PYVE5a/baseline-pulse
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/baseline-complete.json python3 pulse.py week
Last 7 days · 2026-08-31 to 2026-09-06
▁  ▂  ▄  ▆  █  ▆  ▄
m  t  w  t  f  s  s
Logged energy: 1–5. · marks a gap; gaps stay gaps.
[exit 0]
```

Empty week:

```text
$ cd /tmp/speck-v6-native.PYVE5a/governed-pulse
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/governed-empty.json python3 pulse.py --date 2026-09-06 week
Nothing logged yet. Start with: pulse 3
[exit 0]

$ cd /tmp/speck-v6-native.PYVE5a/baseline-pulse
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/baseline-empty.json python3 pulse.py week
Nothing logged yet. Start with: pulse 3
[exit 0]
```

### Product moments

- On the mixed journal, the governed result let me answer “what happened Tuesday?” directly: `ikke logget`. I had to decode the baseline's weekday letters and dot positions first.
- On the complete journal, the governed result stayed with the seven recorded facts. The baseline added `Logged energy: 1–5`, a range summary the request did not ask for and which flattens the week's sequence.
- Neither result added streaks, praise, an upsell, or another interaction. Both empty journals returned the same useful logging prompt.
- The governed output felt like a calm journal read-back. The baseline felt like a compact chart legend. I would trust the former faster when checking gaps.

## Legacy behavior and journal integrity

Both help surfaces remained available; only governed help advertises the fixed-date weekly view used above:

```text
$ cd /tmp/speck-v6-native.PYVE5a/governed-pulse && python3 pulse.py --help
usage: pulse [1-5] | pulse | pulse week | pulse innsikt | pulse --date YYYY-MM-DD [1-5|week]
$ cd /tmp/speck-v6-native.PYVE5a/baseline-pulse && python3 pulse.py --help
usage: pulse [1-5] | pulse | pulse week | pulse innsikt | pulse --date YYYY-MM-DD [1-5]
```

The old two-week view matched byte for byte in visible output on the mixed files:

```text
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/governed-mixed.json python3 pulse.py --date 2026-09-06
       ▆ ▂  █ 
mtwtfssmtwtfss
3 of 14 days logged. Gaps are days you skipped — they stay gaps.
[exit 0]

$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/baseline-mixed.json python3 pulse.py --date 2026-09-06
       ▆ ▂  █ 
mtwtfssmtwtfss
3 of 14 days logged. Gaps are days you skipped — they stay gaps.
[exit 0]
```

The no-pattern insight path also matched:

```text
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/governed-complete.json python3 pulse.py innsikt
Ingen tydelige gjentakende mønstre i loggen ennå. Fortsett å logge, så ser vi.
[exit 0]
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/baseline-complete.json python3 pulse.py innsikt
Ingen tydelige gjentakende mønstre i loggen ennå. Fortsett å logge, så ser vi.
[exit 0]
```

Both rejected an invalid value without changing the mixed journals:

```text
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/governed-mixed.json python3 pulse.py --date 2026-09-06 6
pulse: energy is a whole number from 1 (drained) to 5 (flying). Nothing logged.
[exit 1]
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/baseline-mixed.json python3 pulse.py --date 2026-09-06 6
pulse: energy is a whole number from 1 (drained) to 5 (flying). Nothing logged.
[exit 1]
```

On separate empty files, both logged and read back the same day:

```text
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/governed-log.json python3 pulse.py --date 2026-09-03 4
Logged 4 for 2026-09-03.
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/governed-log.json python3 pulse.py --date 2026-09-06
          ▆   
mtwtfssmtwtfss
1 of 14 days logged. Gaps are days you skipped — they stay gaps.

$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/baseline-log.json python3 pulse.py --date 2026-09-03 4
Logged 4 for 2026-09-03.
$ env PULSE_FILE=/tmp/speck-v6-builder.gLBLJu/baseline-log.json python3 pulse.py --date 2026-09-06
          ▆   
mtwtfssmtwtfss
1 of 14 days logged. Gaps are days you skipped — they stay gaps.
$ cmp /tmp/speck-v6-builder.gLBLJu/governed-log.json /tmp/speck-v6-builder.gLBLJu/baseline-log.json
[no output; exit 0]
```

After every weekly, legacy, insight, and invalid-input read, the six source-journal hashes were unchanged:

```text
$ shasum -a 256 /tmp/speck-v6-builder.gLBLJu/governed-mixed.json /tmp/speck-v6-builder.gLBLJu/baseline-mixed.json /tmp/speck-v6-builder.gLBLJu/governed-complete.json /tmp/speck-v6-builder.gLBLJu/baseline-complete.json /tmp/speck-v6-builder.gLBLJu/governed-empty.json /tmp/speck-v6-builder.gLBLJu/baseline-empty.json
beeb0d7d6926ec1e80d4319e3610fa3f99e634abca5749ce18ca7090d89a7609  /tmp/speck-v6-builder.gLBLJu/governed-mixed.json
beeb0d7d6926ec1e80d4319e3610fa3f99e634abca5749ce18ca7090d89a7609  /tmp/speck-v6-builder.gLBLJu/baseline-mixed.json
5811b2b4f5e4fba014325ccb4affd27911ebbe58b7623111b11c9fcfbae91e0a  /tmp/speck-v6-builder.gLBLJu/governed-complete.json
5811b2b4f5e4fba014325ccb4affd27911ebbe58b7623111b11c9fcfbae91e0a  /tmp/speck-v6-builder.gLBLJu/baseline-complete.json
ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356  /tmp/speck-v6-builder.gLBLJu/governed-empty.json
ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356  /tmp/speck-v6-builder.gLBLJu/baseline-empty.json
```

## Result-disposition controls

I ran the standalone population on the exported `c2912e7` tree:

```text
$ python3 devsuite/tasks/separated-product-team/check.py --result-disposition-controls
  [ok] disposition clean: exact v0.9 evidence stays reviewable / failed / closed
  [ok] disposition clean: low-token incomplete product cannot enter review
  [ok] disposition clean: material result above estimate stays reviewable with a cost finding
  [ok] disposition clean: fresh use and independent judgment establish product sufficiency
  [ok] disposition clean: concrete fresh-review product finding can authorize another build
  [ok] disposition clean: genuinely new product claim can authorize another build
  [ok] disposition clean: sixth model turn closes further model work
  [ok] disposition clean: extra context closes further model work
  [ok] disposition clean: retry overflow closes further model work
  [ok] disposition clean: fallback overflow closes further model work
  [ok] disposition clean: elapsed-time overflow closes further model work
  [ok] disposition clean: owner-interruption overflow closes further model work
  [ok] disposition clean: pre-run-time overflow closes further model work
  [ok] disposition clean: pre-run-file overflow closes further model work
  [ok] disposition mutant rejected: v0.9 cost failure rescued (cost_experiment says 'passed'; evidence says 'failed')
  [ok] disposition mutant rejected: v0.9 further spend reopened (further_model_work says True; evidence says False)
  [ok] disposition mutant rejected: low-token incomplete work admitted (reviewable says True; evidence says False)
  [ok] disposition mutant rejected: cost green converted to product sufficiency (product_sufficient says True; evidence says False)
  [ok] disposition mutant rejected: above-estimate cost finding erased (cost_finding says False; evidence says True)
  [ok] disposition mutant rejected: existing result duplicated without product reason (further_model_work says True; evidence says False)
  [ok] disposition mutant rejected: sixth model turn closes further model work mutant reopens spend (further_model_work says True; evidence says False)
  [ok] disposition mutant rejected: extra context closes further model work mutant reopens spend (further_model_work says True; evidence says False)
  [ok] disposition mutant rejected: retry overflow closes further model work mutant reopens spend (further_model_work says True; evidence says False)
  [ok] disposition mutant rejected: fallback overflow closes further model work mutant reopens spend (further_model_work says True; evidence says False)
  [ok] disposition mutant rejected: elapsed-time overflow closes further model work mutant reopens spend (further_model_work says True; evidence says False)
  [ok] disposition mutant rejected: owner-interruption overflow closes further model work mutant reopens spend (further_model_work says True; evidence says False)
  [ok] disposition mutant rejected: pre-run-time overflow closes further model work mutant reopens spend (further_model_work says True; evidence says False)
  [ok] disposition mutant rejected: pre-run-file overflow closes further model work mutant reopens spend (further_model_work says True; evidence says False)
  [measure] result-disposition subjects=28 clean=14 mutants=14
[exit 0]
```

Cheap incomplete work stayed outside review; a green cost result did not become product sufficiency; v0.9 stayed cost-failed and closed; the above-estimate result stayed reviewable without losing its cost finding; and every exhausted authorization dimension kept further work closed.

## Using the team as a builder

The installed words and `templates/piece.md` gave me one usable split: Product owns the decision and record, Engineering alone owns implementation, and Business or Experience is called from observable conditions rather than from a standing attendance rule. A direct probe of the exact checker agreed:

```text
$ python3 /tmp/speck-v6-builder.gLBLJu/selective_probe.py /tmp/speck-v6-exact.iEwlBH/tree/devsuite/tasks/separated-product-team/check.py
settled internal implementation: Engineering,Product
visible command changed: Engineering,Experience,Product
price changed: Business,Engineering,Product
Pulse weekly request: Business,Engineering,Experience,Product
[exit 0]
```

That matches the product without needing the prior role conclusions. The weekly request changes a command and its visible output, and explicitly proposes price, retention, and gamification. Both selective conditions fire. Product and Engineering remain distinct. For settled internal work, the same rule leaves Business and Experience out. Small work skips the team altogether.

The new template is longer, but the three separate fields are actionable: estimate cost, declare the hard execution boundary, then record product reviewability, cost outcome, and further-work authorization separately. The installed method points the current Pulse result to contributor-excluded use and judgment. It does not point a fresh-token miss or method discomfort back into another Pulse build.

## Free skeptical attack: laundering a method concern into a product reason

I called the exact disposition helper with a completed real result and open authorization, but supplied `concrete_product_finding` as the method-only string `the method template feels verbose`. I then claimed that further model work was open:

```text
$ python3 /tmp/speck-v6-builder.gLBLJu/duplicate_attack.py /tmp/speck-v6-exact.iEwlBH/tree/devsuite/tasks/separated-product-team/check.py
{"finding_value": "the method template feels verbose", "truth": {"cost_experiment": "passed", "cost_finding": false, "further_model_work": true, "product_sufficient": false, "reviewable": true}, "truth_errors": [], "validation_errors": []}
ATTACK ACCEPTED
[exit 0]
```

This is a real limit of the deterministic helper: it checks truthiness, not whether the reason came from fresh product use or is genuinely about the product. It therefore cannot by itself prove the provenance implied by “concrete fresh-review product finding.” The installed method and templates do state that provenance in plain language, and this helper is a repo-side test function rather than a builder input or record parser. I would keep the limitation visible as an instrument strain; it does not turn a method complaint into permission to rebuild Pulse. Any claim that these 28 controls mechanically authenticate the finding's meaning would be too broad.

## Untested limits

- No nested model or host call was authorized, so I did not repeat the native four-carrier build, second-host discovery, token measurement, or host-session identity proof.
- I ran the exact 28 result-disposition population, not the 26 routing, eight assessment, 95 path-transaction, or 230 migration/refusal populations already named in the Built line.
- A seven-day journal cannot contain two samples for a weekday, so `pulse innsikt` exercised its no-pattern branch but not the local-model phrasing path.
- I did not test concurrent writers, malformed journals, installation, upgrade, publishing, or a Claude-host build.
- This was a terminal product; there were no screenshots to inspect.

## Verdict

**Works:** Yes for this review boundary. Both preserved products ran on all three fresh journals; the governed result made every day and gap explicit, legacy behavior held, and read-only runs did not mutate data. All 28 declared disposition subjects passed, including the attempts to admit incomplete work, rescue v0.9, erase its cost, or reopen work after an authorization boundary.

**Keep:** Yes. The governed Pulse result is materially easier to trust than the control, and the Product/Engineering split plus selective Business/Experience calls is usable from the installed words and templates. The actual result belongs in fresh review now. Another Pulse build would duplicate working product without a fresh product finding.

**Deal-breaker:** None on the supported builder path. The free attack shows that the deterministic helper cannot authenticate the semantics or provenance of a claimed product finding; that is an explicit untested instrument limit, not evidence that Pulse needs rebuilding. I would block only a release claim that says the helper mechanically proves genuineness. The right next action for the candidate is fresh review, with the semantic limit kept visible for the judge.
