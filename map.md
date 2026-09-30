# Build order

The owner approved the complete optional toolkit for v7.1. The method and project installer remain settled; the new cache lifecycle is separate. Current status is in [state.md](state.md).

## Ordered work

1. **Pin and install.** Verify official Graft, ripgrep, jq, ast-grep and RTK artifacts; implement setup, diagnosis, execution and retirement within an owned cache.
2. **Integrate and exercise.** Connect CLI dispatch and selective agent guidance. Test installation failures, preservation, retries and child exit codes, then run all five actual tools on a disposable subject.
3. **Review and distribute.** Review the frozen candidate independently, run hosted checks and published installation, then upgrade existing native adopters while preserving owner files and edits.

## Integration

The manager/test contributor and release-manifest contributor own separate paths. The integrator owns CLI dispatch, installed guidance, real tool checks and publication. The manifest is the package-level source for versions, platforms and verified artifacts. Toolkit setup owns only its cache; method install/upgrade does not download tools.

Evidence and release status: [work/toolkit-7.1.md](work/toolkit-7.1.md) and [state.md](state.md).

## Deferred work

Old-Speck conversion, general promise-conservation automation, and comparative product benchmarks remain deferred. They need their own concrete request or observed failure. Earlier plans and their original owner instructions remain in [history](docs/history/v7.0.3-records.md).
