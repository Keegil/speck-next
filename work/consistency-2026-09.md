# Consistency and surface review — September 29, 2026

Request: fix release consistency and ensure all Speck Next elements, including skills and templates, form a coherent, useful method. Baseline: `bab31801c6abf20aea4a41d3c8903042e899d762`, version 7.0.3. This is a compatible patch, 7.0.4; no new runtime service, model campaign, or fixed workflow is needed.

## Scope and findings

Review covers the installed entrypoints, five skill bodies and their references, six templates, CLI messaging and package, default development checks, and current documentation. A separate reader found stale release pins in both README and CLI help, omitted install prerequisites, historical capability rows presented as current, an unlabeled historical example, and an overstated claim that the shelved benchmark was runnable. Templates still used compressed internal labels and implied more structure than the skills require.

The five skill bodies and their conditional references otherwise retain the intended boundaries, scoped protection, and independent substantive acceptance. Their 7.0.3 trials remain evidence about that release, not a new automatic-activation or productivity claim.

## Changes

- Align release instructions and derive CLI help's tag from package version. Document existing Git/Node/npm prerequisites. Distinguish filesystem entries from regular file count.
- Rewrite optional templates around the actual brief, useful evidence, dependencies, decisions, and resumption. Retain existing filenames and omit unnecessary sections. No migration of owner records.
- Keep live state, plan, and capability evidence focused on present work; preserve prior records through immutable Git links. Label the Pulse example and benchmark according to their actual historical status.
- Add cheap checks for versions, skill metadata, local reference reachability, host discovery and installed size, with deliberately broken disposable fixtures. Wire them into the default suite and GitHub Actions without model calls.

Template edits and check implementation have separate file owners. The integrator owns documentation and cross-file agreement. A non-contributor reviews the combined candidate and exercises the relevant template/check behavior before release.

## Evidence

Pending final checks and independent review. No claim of improved agent productivity or complete behavior coverage is made by static validation.
