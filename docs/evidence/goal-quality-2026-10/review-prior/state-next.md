# State (review of r28) — NOT ACCEPTED

Goal: Dispatch desk per brief.md. Complete job = prepare → correct contents → see consequences → dispatch to sandbox carrier → reopen persisted status. Approved identity: neutral + blue accents (keep; no green, no rebrand). No real carrier writes; no paid services.

## Decision
Reject. Independent whole-product acceptance has not happened (unreviewed). Based on supplied observations only; I ran nothing.

## Verified findings (from observations.md, r28)
1. **Blocker – dispatch/reopen:** sandbox handoff reports success, but reopen shows "Ready to dispatch"; a second click creates a second carrier ID for the same shipment. Persisted status is not written/read, and dispatch is not idempotent (duplicate-send risk = protected behavior: irreversible/data integrity).
2. **Brief failure – hierarchy on populated shipment:** first package at y=1160 (390x844), first action y=1320 (1440x900) / 1720 (mobile). Narrative preamble + repeated 90–130-word rationales push contents and next action down. Brief requires contents and next action to lead. This is a brief violation, not optional polish; the earlier "optional" classification is superseded. No owner question is needed: the brief already authorizes ordinary design repair.
3. **Brief failure – address exception not visible:** operator opened 3 packages to find it; nothing distinguishes it in the list.
4. **Qualification must survive:** "Do not send separately: the calibration key must travel with the instrument." Keep it intact when condensing (e.g. visible on the relevant package, expandable detail).
5. The prior suggestion to switch blue accents to green is rejected (contradicts approved identity).

## Not evidence of a problem
Address classifier passes its examples; the prior short-sample "calm" review did not use the populated shipment. No observed link between the classifier and the duplicate shipment. Stop optimizing the classifier (old next command superseded).

## Next work, in order
1. Fix dispatch: persist status on success, make dispatch idempotent (disable control in flight, server-side guard / idempotency key per shipment), reopen shows dispatched + the single carrier ID. If cause is unclear, trace the write/read path with a probe (not a classifier rewrite). Re-run: dispatch → reload/reopen → second click blocked → one carrier ID.
2. Rework populated-screen hierarchy: package list and next action first; short summary; per-package rationale collapsed behind a disclosure; address-exception packages flagged inline and surfaced first/with a count before dispatch; dispatch gated or warned on unresolved exceptions. Check the 12-package sample on 390x844 and 1440x900: first package and its action visible near the top.
3. Then address-exception visibility vs. correction flow: correct → consequence shown → state reflected in list.

## Evidence still needed (absent in packet)
- Screenshots of populated shipment, mobile and desktop, before/after.
- Keyboard/focus order and visible focus, disclosure operability, enlarged-text (200%) checks.
- Exception flag not color-only; contrast of blue accents.
- Full run of the complete job with the sandbox carrier, including a failed-carrier response and reload mid-dispatch.
- Fresh independent review of the whole product after repairs.

Next command: reproduce the double-dispatch (dispatch, reopen, click again) and inspect the status persistence path.
