# State (next builder) — review of r28

**Decision: NOT ACCEPTED.** Document-based review only; no UI run, no screenshots. Whole product has had no independent acceptance.

## Goal
Brief.md: prepare shipment → correct contents → see consequences → dispatch to sandbox carrier → reopen persisted status. Contents and next action lead on phone and desktop; address exceptions visible before dispatch; explanations available with qualifications intact; neutral + blue identity (keep; no rebrand, no real carrier writes).

## Findings (priority order)
1. **Blocker: dispatch/reopen.** Carrier returns success, but reopen shows "Ready to dispatch". A second click creates a second carrier ID for the same shipment. Likely a persistence or status write-back gap plus no idempotency guard. Cause not yet traced. Sandbox only.
2. **Brief failure: hierarchy on the populated shipment.** The first package is at y=1160 on 390x844, and its first action is at y=1720 (y=1320 on desktop). The narrative preamble and the repeated 90–130-word rationales push contents down. The operator opened three packages to find the address exception, and nothing marks it. This is a core-brief miss, not optional polish. The earlier "optional" classification is superseded. It is an ordinary reversible design repair, so no owner question is needed.
3. **Qualifications.** When condensing explanations, keep qualifiers such as "Do not send separately: the calibration key must travel with the instrument." Collapse the text, don't paraphrase it away.
4. **Unchecked:** keyboard/focus, enlarged text, rendered visuals. The "calm and easy to scan" review used only the two-package sample and doesn't count for the populated case.

## Declined suggestions
- Green accents: personal preference. The blue identity is approved.
- Asking the owner before changing the hierarchy: not needed.
- More classifier optimization: its examples pass, and nothing links it to the duplicate dispatch. Pause it unless a trace implicates it.

## Next work
1. Reproduce the double dispatch. Trace the write path (carrier call → persisted status → reopen read). Fix it so the status persists and dispatch is idempotent or disabled once sent. Add a focused test. Re-run the full job end to end.
2. Redesign the populated view. Put package names, status and the next action first. Mark address exceptions in the list and block or warn at dispatch. Collapse rationales behind on-demand disclosure and trim the preamble. Check 390x844 and 1440x900 with the 12-package sample.
3. Evidence still needed: screenshots at both viewports with the populated sample; a task run where the operator finds the exception without opening packages; keyboard/focus and 200% text checks; a dispatch → reload → reopen run showing one carrier ID.
4. Then get independent review of the whole application, not only the classifier.

## Next command
Reproduce the double dispatch against the sandbox and trace the status write.
