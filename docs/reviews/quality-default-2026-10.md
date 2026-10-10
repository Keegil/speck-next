# Independent quality-guidance review

Claude Opus 5.5 reviewed packet `d655d373317202440e90073c43a1cef8aa8e2866` against starting source `bb49cca11722897d9f741cbd8fc463fb9dbb6f21`. The packet contained the complete source delta, affected current guidance, unchanged installer sources, anonymous fixtures A-F, screenshots, requested jobs, and raw runtime observations. The supplementary native run G and final continuity records were not included. No contributor served as this reviewer.

## Reviewer response

Evidence is in; here's the verdict.

## Blind visual judgment
Viewed all 18 screenshots (A–F: empty-desktop, populated-desktop, populated-mobile). The read-budget hook blocked the originals, so I viewed downscaled JPEG copies (300–800px wide, low quality). Fine detail and exact contrast are not judged.

- **Reading (A–D):** all four are coherent, near-identical warm card layouts; none is sloppy. B is the most usable: it shows "Remaining −2 h" directly and has the cleanest list rows. D is next, with a tinted over-budget card and a blank add form.
- **Packing (E–F):** F is slightly ahead, with progress in the reading flow plus a bar. E's floating "still to pack" tile is a preference, not a defect.
- **Defects, not preference:** A, B and C prefill the hours field with a real value (6 or 4) beside placeholder title and author. A and C show a part-filled meter while over budget on desktop, but that is a mid-transition capture: A's bar measured full width and red once settled.

The spread is too small for me to separate old from revised by eye.

## Executions
- **Packet scripts:** ran `inspect-reading.mjs` and `inspect-packing.mjs` on a temp copy; the packet stayed clean. Results reproduce `observations.json` exactly: A, C, D 12/13; B 12/13; E, F 8/9; no page errors.
- **My keyboard probe (all six):** typed and Enter to add, Tab, Space, Enter on Remove.
  - Space on a checkbox drops focus to `<body>` in A, C, D, E and F. A second Space does nothing; in Chromium one Tab returns to the same checkbox.
  - Enter on Remove drops focus to `<body>` in all six, including B. The packet scripts do not test this.
  - B stores a budget of 0, then shows 8 after reload.
  - C leaves focus in the hours field after an add.
  - Only F has a reduced-motion rule; only E and F have `focus-visible` styles.
  - Checkboxes are 18–20px and Remove is 27–36px tall on mobile.

## Source change: acceptable
I read the full `method.diff` and the current `AGENTS.md`, `CONTRACT.md`, craft and judge skills. `product.md`, `README.md` and the experience, map-build and shape-product skills I read only as diff hunks.

- **Intent:** met. Professional execution is now the default in the root page, stopping rule, contract, product promises and the five skills, with no new files or skills and no installer change.
- **Small tasks:** preserved. "Tiny content or typo fixes need no redesign or ceremony", and the craft description still excludes typos.
- **Budgets:** preserved. "Honor explicit budgets" is untouched, and craft says to report views that could not be inspected.
- **Owner control:** preserved. A broader rebrand is named a consequential direction choice, and settled direction stays.
- **Accessibility:** strengthened, with touch targets and following focus through updates added.
- **Independent review and protection:** untouched. Craft still says polishing your own work is not independent acceptance.
- **Size:** I counted 40,148 bytes for `AGENTS.md` plus the skills and references, under the 100 KB ceiling.

Non-blocking:
1. **Promise 9 is worded as an outcome.** Its "fails if… leaving concrete workmanship gaps" clause is one this packet's own trials do not meet. That is honest only while `capabilities.md` says the behavior is unmeasured, and it currently says nothing about this change.
2. **The focus line only detects.** If you want a producer, add one clause to craft: updating a list keeps or restores focus on the control the user acted on, including after removal.

## Do the trials prove improvement? No
- **Focus:** five of six apps lose focus on toggle and all six on remove. The instructions were tightened on exactly this before the packing run, and both E and F still fail, so the revised packing run failed the thing it was told to check.
- **Attribution:** arms are undisclosed, n is 2 per arm for reading and 1 for packing, one model, and reading and packing ran under different instruction versions.
- **Visual quality:** even the old-instruction outputs look decent, so this task does not reproduce your original complaint. The trial could not have shown the gain.

This is insufficient measured effectiveness, not a consequential source flaw. No rule in the diff causes the defects; the guidance was simply not reliably followed or not sufficient.

## Smallest repairs before any behavior claim
- Keep "no general quality gain claimed", and add that focus-through-update was instructed and not achieved in the one final-instruction run.
- Optionally add the craft clause above and rerun one packing trial with the arms unblinded afterwards.

## Limits
- I could not check the 34-test suite or the typo runs; `devsuite/run.sh` and the typo artifacts are not in the packet.
- Chromium headless only; no screen reader, no enlarged-text view, no contrast measurement.
- Agent reports from the trials are not in the packet, so I cannot say whether the agents opened their screenshots.
- The Codex run is not included.

## Integration

The source change is accepted within the reviewer's stated scope. No improvement or reliability claim is made. The optional extra focus instruction is deferred: final guidance already requires preserving and following focus, and the executed examples did not follow it. This is retained as failed behavior, not relabeled as successful guidance adoption. Source acceptance does not accept the defective fixture apps as completed products. Final capabilities and work records state these limits.
