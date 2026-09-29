# Independent review

**Decision: acceptable for the requested consistency patch. No blocking findings.**

Reviewed snapshot `18f249115a8f9688d9552d83159db0ab7e2ce2d1`, exported at `/tmp/speck-704-review-18f2491/candidate`, against baseline `bab31801c6abf20aea4a41d3c8903042e899d762` and the owner request in `request.txt`. I did not author the patch. I used the frozen source and task diff, not live author work notes or their conclusions.

## Scope and coherence

Inspected both host entrypoints; all five skill bodies and their six references; all six templates; package and CLI message changes; current README, contract, product, map, state, and capability records; historical-example labels; the new guard, its controls, installer-test changes, and CI workflow.

The release examples now agree with the package and CLI version. Install prerequisites match the implementation. Installed instructions no longer direct adopters to unshipped local README/CONTRACT files. Templates remain optional, distinguish known results from pending work, preserve meaningful constraints, and do not require a fixed staff or sequential ceremonies. Skills still permit bounded work without product/map files while retaining consequential protections, complete-job repair, and independent acceptance for substantive results.

Current records distinguish candidate work, published 7.0.3, and older evidence. Pulse and the shelved benchmark have clear historical limits; they no longer imply accepted current behavior or an executable benchmark. The patch does not change installer transaction behavior beyond messaging.

## Executed checks

Ran `bash devsuite/run.sh` exactly once from the snapshot. Exit status 0:

- Release guard: 19 canonical regular files plus marker = 20/20; one discovery symlink counted separately; 37,696/100,000 bytes; five of six permitted skills; eight local links.
- Nine guard-control tests passed in 13.001 seconds.
- Ten installer tests passed in 37.031 seconds, including 52 version/product combinations, packed/source parity over the whole installed tree and digest, dirty owner-record preservation, refusal, idempotence, and forced rollback.

The meaningful negative controls execute the checker against disposable mutations and assert the expected diagnostic: stale README/version pins, stale help pin, missing and source-only links, invalid/duplicate skill metadata, extra installed files, excess bytes, excess real skills, and broken host imports/discovery. Restored counterparts pass. These are mechanism checks rather than assertions over matching prose.

Ran CLI help and observed the 7.0.4 pin. CI calls the same suite, grants read-only contents, disables checkout credentials, and has a five-minute job bound. The three referenced `actions/*@v7` tags were resolved directly with `git ls-remote`. No hosted Actions run or published 7.0.4 installation was performed in this review; those remain release verification.

## Forward handoff trial

Used the new state template on the paused inventory task and saved only `handoff-state.md` beside this review. Subject: HEAD `7b7213dbbffbc11a3dbb710a70a42084f6f8bb02` plus existing dirty `inventory.py`, SHA-256 `95f01651cb2b0a9fc1df7cc646807e7297f71950e5217effbf4314f911c4c449`.

The two supplied tests passed. A direct combined-behavior probe showed stock filtering working in the dirty repair, while uppercase/mixed-case category selection still failed. The handoff names that unfinished result, warns against losing the uncommitted repair, and supplies an executed reproduction plus the next bounded implementation action. It avoids a new project plan or owner question. Rechecked status/hash: the subject still had only the original modified `inventory.py`, with identical bytes. No code fix or test-file edit was made.

This is one bounded use example, not automatic skill activation, an independent second-agent resumption, a reliability estimate, or comparative productivity evidence. The template was useful because it retained the actual tested working tree and a runnable next step; broader claims remain unmeasured.

## Limits and next action

The guard deliberately checks shipped local paths rather than URL availability, anchors, arbitrary YAML, or semantic consistency. This review is from a non-contributor in the same model family as the integrator. The parent reported that both separately attempted cross-model reviews stopped before tool execution because of weekly usage limits; neither supplies additional acceptance evidence. CI execution, publication, and real-adopter upgrades remain to be read back at their final release SHA. These limits do not require another methodology campaign. Proceed with the already planned release verification and preservation checks.

## Trial handoff, as returned

# State

## Goal and current result

Add case-insensitive category selection to `available(rows, category=None)` while preserving the rule that only positive-stock items are returned. Work is paused. No code was changed during this handoff.

## Evidence and limits

Checkout: `/tmp/speck-704-review-18f2491/handoff-subject`, HEAD `7b7213dbbffbc11a3dbb710a70a42084f6f8bb02`, with an existing unstaged `inventory.py` repair. Its SHA-256 is `95f01651cb2b0a9fc1df7cc646807e7297f71950e5217effbf4314f911c4c449`.

`python3 -B -m unittest -v` passed both existing tests. A direct probe returned IDs `[1, 3]` without a category and `[1]` for `books`; an out-of-stock book stayed excluded. `BOOKS` and `BoOkS` returned `[]`, so the requested behavior is still missing. The existing tests do not cover it. This is a diagnosis, not acceptance of the unfinished feature.

## Open issues

Preserve the unstaged stock-filter repair: committed HEAD incorrectly skips stock filtering when a category is selected. Build on the current working tree. Category matching is still case-sensitive.

## Next action

When work resumes, run this verified reproduction with Python 3; it currently fails on the last assertion. Add regression coverage for mixed-case selection combined with stock filtering, then implement the remaining behavior without discarding the existing repair.

```sh
cd /tmp/speck-704-review-18f2491/handoff-subject
python3 -B - <<'PY'
from inventory import available
rows = [{'id': 1, 'category': 'books', 'stock': 2},
        {'id': 2, 'category': 'books', 'stock': 0},
        {'id': 3, 'category': 'tools', 'stock': 3}]
assert [r['id'] for r in available(rows)] == [1, 3]
assert [r['id'] for r in available(rows, 'books')] == [1]
assert [r['id'] for r in available(rows, 'BoOkS')] == [1], 'case-insensitive selection is still missing'
PY
```
