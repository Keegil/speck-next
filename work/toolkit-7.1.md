# Toolkit v7.1

The owner approved all five proposed tools: “I think we bundle all these tools in v7.1. Do it!” Baseline is v7.0.4, commit `9b3a9334ce289a7c1036316d211e74b8ee514874`.

## Scope

Ship Graft, ripgrep, jq, ast-grep and RTK as an optional managed toolkit. Provide setup, diagnosis, execution and removal from the existing Speck CLI. Keep the same five method skills and twenty-file installed ceiling. Core method install/upgrade stays independent of tool downloads. Ordinary tasks choose useful tools; setup does not create a new task phase.

The toolkit owns its cache and verifies pinned artifacts. Existing installations, agent settings, owner records and unrelated edits stay intact. No global hooks, paid graph builds or automatic shell rewriting are part of setup. RTK summaries and Graft indexes do not replace original evidence. Do not claim measured overall savings from a shorter output sample.

## Build and verification

The implementation worker owns the toolkit manager and deterministic tests. The upstream researcher owns the verified release manifest. The integrator owns CLI dispatch, task guidance, documentation, real integration checks and release/adopter verification. A non-contributor reviews the complete frozen candidate before release.

Order: verify upstream artifacts and local structural operation; implement cache lifecycle and launcher; exercise all five actual tools plus failure paths; independently review; publish and upgrade the four existing native method checkouts. Toolkit setup is machine-level and need only run once for those checkouts.

## Evidence

The manifest pins Graft 0.21.1, ripgrep 15.2.0, jq 1.8.2, ast-grep 0.45.3 and RTK 0.50.0. All twenty listed platform binaries were downloaded and matched official SHA256 digests; Graft's npm tarball matched its SHA512 integrity. The manager supports macOS/Linux arm64/x64; Windows assets are recorded but Windows setup is explicitly unsupported. Graft's native dependencies resolve during npm installation; their retained lockfile records that installation, not a universally frozen dependency tree.

Ten deterministic toolkit controls passed, covering integrity/version failure preservation, archive traversal, cache ownership/symlinks, setup retries, removal, child output/status and unsupported-runtime preflight. The live macOS arm64 smoke passed fifteen checks in 39.682 seconds, including downloading all five tools, actual search/JSON/structural commands, Graft graph build and retrieval, unchanged fixture files and Git status, repeat setup, and retirement with an outside witness preserved. ripgrep's no-match exit 1 and RTK proxy's separate stdout/stderr with exit 7 survived the launcher. `python3 devsuite/toolkit-smoke.py` reproduces the live check with a new disposable cache.

Telemetry is disabled for managed launches; normal vendor runtime behavior remains. Graft may use `~/.graft` and background update checks, and RTK records local usage. No host HOME override, global agent settings, integration hooks or automatic paid/model operations are part of the manager. Structural graph completeness, automatic host tool selection and whole-task savings are not established by these checks.

The complete deterministic suite passed at `79b56d6`: nine surface controls, fourteen toolkit controls and eleven installer checks, including fifty-six supported-version/product combinations and source/packed toolkit parity. The installed method is 38,852 bytes across nineteen canonical files plus its marker and discovery link.

[Independent review](../docs/reviews/toolkit-7.1.md) first found interrupted-setup recovery broken. The repaired candidate `79b56d6` was accepted after real SIGINT and SIGKILL installations, safe refusal while an orphan installer remained active, successful retries, diagnosis and removal. Setup also continues after individual tool failures. All five tools are installed in the operator's managed cache; retry preserved them and five existing global configuration files remained byte-identical.

## Release and adoption

[v7.1.0](https://github.com/Keegil/speck-next/releases/tag/v7.1.0) was published at `0a53a59e4f9d63d1da765ad32a52d70623ad0e7c`. [GitHub run 36687661422](https://github.com/Keegil/speck-next/actions/runs/36687661422) passed all 34 deterministic tests and fifteen live Linux x64 toolkit checks; the live smoke took 39.62 seconds. macOS arm64 and Linux x64 were executed; other manifest architectures have download verification only. Node 20 is the declared minimum, not a runtime tested in this release's checks.

The published `npx` installer produced all nineteen canonical files byte-identical to the release, the v7.1.0 marker and correct Codex link. Its toolkit diagnosis found all five managed versions ready, and its launcher executed ripgrep 15.2.0. Method digest: `9f85627d906732ab4b182a7e3cf48ee140c23069fecbf37aaba528f7dff5a987`.

All four existing checkouts were upgraded and verified from fetched remote commits:

| Checkout | Pushed commit |
|---|---|
| Odd preparation app | `17d496d9bda30584c4c1cf25061ff7fb07c743ec` |
| Splang Slack | `67a1bd3f4b1a22a3c65ba470383f2795ed605dc9` |
| Odd p2r review | `f35c9d412a4bfb154eada0a231c8da23951bd692` |
| Odd boka visual | `b1f9754f85e455053318d92f905a2453a8c4ecd9` |

Each commit changed only `AGENTS.md` and the version marker. All nineteen canonical files, marker digest and Codex link matched. The rollout preserved 2,842 tracked owner paths and 14,263 nonignored untracked paths, including existing dirty files and staged entries. Ignored caches were outside that snapshot. Exact Git index bytes survived each upgrade; metadata bytes later changed before commit while all indexed paths, modes, blobs and stages remained identical. No index restoration was performed.

Local detailed receipts are under `/tmp/speck-tools-71/`: `published-verification.json`, `rollout-verified.json`, `integrator-readback.json`, `hosted-smoke.json`, and `global-config-final-setup-proof.json`. The last records a direct before/after setup comparison of five global configuration files, all unchanged; it does not claim that other concurrent clients never update their own session state.

## Sources

- [Graft](https://github.com/trailhq/Graft), including its cache, integration and telemetry implementations.
- [ripgrep releases](https://github.com/BurntSushi/ripgrep/releases), [jq releases](https://github.com/jqlang/jq/releases), [ast-grep releases](https://github.com/ast-grep/ast-grep/releases), [RTK releases](https://github.com/rtk-ai/rtk/releases).
- [Spec Kit bundles](https://github.github.io/spec-kit/reference/bundles.html): relevant precedent for versioned components and explicit ownership; no catalog or workflow engine is imported.
