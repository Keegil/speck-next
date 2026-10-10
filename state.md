# State

## Goal and current result

Execution quality is now part of ordinary scope in the source method. The root page, product contract and five existing skills require deliberate design and relevant practices, actual inspection, scoped refinement, and review of workmanship. New UI work does not need a separate request for polish. Tiny fixes remain small. [Change record](work/quality-default-2026-10.md).

Published version [7.1.1](https://github.com/Keegil/speck-next/releases/tag/v7.1.1) includes the execution-quality repair. Its optional toolkit is unchanged. This increment adds no installed file, skill or runtime dependency. [Release and adoption evidence](work/quality-release-7.1.1.md); prior toolkit evidence remains in [the toolkit record](work/toolkit-7.1.md).

The accepted source was initially pushed at `37a9721`. Release tag v7.1.1 resolves to `0dd97b4`; GitHub checks passed at that SHA. A fresh published installation matched the source. All four existing native checkouts received the tagged upgrade, with owner files and ongoing edits preserved and remote heads and marker contents verified. The missing optional tool cache was restored and all five managed tools diagnosed ready.

## Evidence and limits

Claude Opus 5.5 independently accepted the source change and exercised six frozen trial apps. The deterministic suite passed 34 tests; the final source passed a fresh installed-surface check at 43,306 bytes, twenty regular installed files including the marker, and five skills. Both host entrypoints share the same files. [Review](docs/reviews/quality-default-2026-10.md) and [capabilities](capabilities.md) retain precise scope.

The executed comparisons did not establish quality gains or reliable adherence. Reading and packing builders skipped image inspection and left keyboard-focus defects even after explicit instructions. Tiny typo repairs stayed small. Native Codex attempted real rendering, correctly reported a sandbox limitation, then captured desktop/mobile images in a browser-capable isolated run; the trace does not establish that the author opened them. The integrator viewed those images. These are illustrative uses, not accepted products or general behavioral proof.

## Next action

Use the revised guidance in ordinary work and have review reject concrete workmanship gaps within the requested scope. Treat the current default-quality promise as a requirement whose reliable adoption remains unproved. Further methodology changes need an observed failure or a new owner request; do not restart a synthetic build campaign solely to obtain a favorable score.
