# State

## Goal and current result

The owner requested a consistency fix and a quality check across all Speck Next elements. Version 7.0.4 is ready for release: instructions and current records are aligned, all six optional templates are refreshed, and automatic consistency checks pass locally and on GitHub. The five skills retain the boundaries introduced in 7.0.3.

## Evidence and limits

Candidate `18f2491` has independent acceptance, nine passing guard controls, ten passing installer tests including 52 upgrade combinations, and a useful executed handoff trial. GitHub Actions passed at that candidate SHA. The last published and adopted version is 7.0.3; publication proof belongs in [work/consistency-2026-09.md](work/consistency-2026-09.md). [Capabilities](capabilities.md) distinguish current checks from earlier behavioral examples.

Automatic host activation, full-stack Claude/Codex behavior, and comparative productivity remain unmeasured. Existing unrelated local files and adopter edits must remain intact.

## Next action

Publish the patch and verify the four native adopter upgrades against their captured preservation baseline. Earlier release histories and completed plans are preserved in [prior records](docs/history/v7.0.3-records.md).
