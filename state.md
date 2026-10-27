# State

## Goal and current result

The owner requested a new version from [PR #1](https://github.com/Keegil/speck-next/pull/1). Version 7.3.0 is being prepared: `craft` prioritizes working content and the next meaningful action in work applications, and `judge` checks what users must read or navigate through before starting. [Scope and release evidence](work/workflows-7.3.md).

## Evidence and limits

The PR changes two skill instructions. Release metadata and command pins now name 7.3.0. Local checks, fresh independent review, hosted checks and published installation read-back are pending. This guidance has no new downstream UX trial; package checks establish distribution only. No adopter rollout is included in this request.

The previous [7.2.0 release and four-checkout adoption](work/continuation-7.2.md) retain their evidence and limitations. Existing product pauses, budgets, owner decisions and open findings remain applicable.

## Next action

Run `bash devsuite/run.sh`, independently review the complete task diff against `3c6072f`, then merge and publish v7.3.0 when the release checks pass. Verify the published tag and a fresh tagged installation before recording publication as complete.
