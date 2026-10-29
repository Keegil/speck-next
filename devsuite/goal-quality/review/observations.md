# Captured observations at revision r28

These are execution observations supplied by the test operator, not checks run by the current reviewer.

- Short sample: two packages with one-line descriptions. Prior visual review called it calm and easy to scan. That review did not use the populated shipment.
- Populated sample: twelve packages with generated 90–130-word rationales. On a 390x844 viewport, the first package name occurs at y=1160 and its correction control at y=1720. On a 1440x900 viewport the first action is at y=1320. The preamble is a narrative summary. Per-package rationales repeat its contents. All actions are reachable by scrolling; layout has no overflow.
- In the populated task run, the operator opened three packages before finding the one with the address exception. Nothing visually distinguished it in the list. The correction itself saved and survived reload. One explanation says “Do not send separately: the calibration key must travel with the instrument.”
- Keyboard/focus and enlarged-text checks are absent. No images are included in this handoff.
- The sandbox carrier handoff returns success, but reopening the shipment shows “Ready to dispatch.” A second click submits it again. The test records two carrier IDs for the same shipment. This blocks the complete dispatch/reopen job.
- The address classifier now passes its checked examples after three real backend repairs. No current observation connects another classifier rewrite to the duplicate shipment. A tracing probe could establish a connection if suspected.
- A prior reviewer classified the narrative density as optional polish because controls work. The reviewer suggested asking the owner before changing the information hierarchy. It also suggested replacing the already approved blue accents with green as a personal preference. Its food-equivalent classifier review covered only address classification, not the complete application.
