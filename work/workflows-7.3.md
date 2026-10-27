# User workflows — 7.3

The owner requested a new release from [PR #1](https://github.com/Keegil/speck-next/pull/1). Its complete method change is one paragraph in `craft` and one review criterion in `judge`.

For work applications, working content and the next meaningful action take priority. Navigation follows the user's workflow. Explanations, status and history sit where they help people choose, perform or check work. Context needed for informed decisions and accessibility stays available. Reports remain appropriate when reading, comparison or monitoring is the job.

Review checks what the user must read or navigate through before starting. A visible action button alone does not establish an effective workflow.

Version 7.3.0 distributes this guidance through the existing installer and discovery link for Claude and Codex. The installer, toolkit, five-skill structure and optional records are unchanged. Installation checks can verify distribution; they cannot establish better downstream UX. No comparative product trial or adopter rollout is claimed.

## Validation and review

`bash devsuite/run.sh` passed all 34 deterministic tests: nine surface controls, fourteen toolkit checks and eleven installer/upgrade tests. The installed footprint is 47,287 bytes, nineteen canonical regular files plus marker, five skills and one discovery link. `git diff --check` passed.

Fresh native Sonnet 5.5 independently accepted instruction-package readiness at `e78ba5a7cf460fa38cde921583ce33754c912b59`. [Review scope and limits](../docs/reviews/workflows-7.3.md) distinguish its reading and distribution checks from the integrator's execution evidence. Hosted [branch checks](https://github.com/Keegil/speck-next/actions/runs/40555303381) and [PR checks](https://github.com/Keegil/speck-next/actions/runs/40555313313) both passed at that exact head, including real Linux toolkit commands.

## Publication

PR #1 merged at `ba117e1bc54a49956aeaaea230fb7badda99c1b2`; its tree matches the reviewed head. [Release checks](https://github.com/Keegil/speck-next/actions/runs/40555626647) passed at that exact merge SHA: all 34 deterministic tests and fifteen real Linux x64 toolkit checks. No toolkit pins changed.

[7.3.0](https://github.com/Keegil/speck-next/releases/tag/v7.3.0) was published on 27 October 2026. GitHub read-back confirmed the stable release, and the remote annotated tag resolves to `ba117e1bc54a49956aeaaea230fb7badda99c1b2`.

A fresh installation from the published tag, using an isolated npm cache, matched all nineteen canonical source files. Its marker reported version 7.3.0 and method digest `67e7a25b502dfb1cb714041cc984d641a24a8c02b86120421bc7284c10551867`; the Codex discovery symlink resolved to the canonical skills. Installation created no product records. A subsequent tagged upgrade preserved staged owner files byte-for-byte and the Git index, and all canonical files still matched. The local checker first compared macOS `/var` and `/private/var` aliases without normalization; after normalizing the temporary path, the complete fresh installation and upgrade checks passed. Raw observations and the checker remain in `.local/release-7.3/`.

This record supplies the release's scope and evidence for users considering an upgrade. Adoption in other products and downstream UX outcomes remain unmeasured by this release.
