# Execution-quality release 7.1.1

The owner requested publication and upgrades of all relevant repositories after accepting the method change. [v7.1.1](https://github.com/Keegil/speck-next/releases/tag/v7.1.1) is the latest published release, at `0dd97b469caf3919c81c212d08a876764dfdd863`. The reviewed execution-quality guidance is unchanged apart from the current toolkit command pin. Package version, README status and installation examples agree.

## Release verification

All 34 deterministic tests passed locally. [GitHub release checks](https://github.com/Keegil/speck-next/actions/runs/38049288525) passed at the release SHA, including the same tests and fifteen real Linux x64 toolkit checks in 39.638 seconds. The published annotated tag was read back and resolved to that SHA; the GitHub release is published, stable and latest.

A fresh installation through `npx -y github:Keegil/speck-next#v7.1.1 install` used an isolated npm cache. All nineteen canonical files matched the release source, the marker reported 7.1.1 and the Codex link resolved correctly. No product or map record was forced. Method digest: `164991f435aa3e0103e47ef8753311dbf5132228983d4cb35bd7097e0d35d325`. The installed surface remains twenty regular files including its marker, five skills and 43,306 bytes. [Installation observations](../docs/evidence/quality-default-2026-10/release-install.json).

The first published toolkit diagnosis correctly reported the managed cache absent on this Mac. The published setup restored Graft 0.21.1, ripgrep 15.2.0, jq 1.8.2, ast-grep 0.45.3 and RTK 0.50.0. Final published diagnosis reported all five ready. [Tool diagnosis](../docs/evidence/quality-default-2026-10/release-tools.json). The missing cache was an environment finding; toolkit implementation and pins are unchanged.

## Existing repository adoption

The Projects registry, Codex app projects, configured project paths, Code checkouts, managed worktree roots, Documents and Desktop were checked for Speck Next markers and root method headers. They identified four native adoptions plus the source kernel. Temporary test subjects and old-Speck repositories were excluded; unmarked projects were not converted. [Discovery observations](../docs/evidence/quality-default-2026-10/release-discovery.json).

Each native checkout ran the published tagged upgrade. All nineteen canonical files, version marker, digest and Codex discovery matched. Before/after fingerprints preserved 17,740 tracked and nonignored untracked owner paths in total, including file modes and symlink targets. Ignored caches were outside the snapshot. Git index bytes survived each upgrade; pre-existing staged owner entries and dirty status survived the method-only commits. Each commit changed only `AGENTS.md` and `.claude/speck-next.json`. Remote branch heads and marker contents at the exact commits were read back from GitHub. [Rollout observations](../docs/evidence/quality-default-2026-10/release-rollout.json).

| Checkout | Branch | Pushed commit |
|---|---|---|
| Odd | `codex/odd-preparation-app` | `4455a76a00bf06a9bb6aa63c135fb90bb8207c1e` |
| Splang in Slack | `main` | `49d1755a7be4a40f75e9b3b7a5a888f288cfdf05` |
| Odd Boka visual worktree | `codex/odd-boka-visual-20260908` | `83926bbde81cf90df5b43bd5c2445e824cc5a685` |
| Odd p2r review worktree | `codex/odd-p2r-review-resume-20260908` | `91bd43528b539a5c61042ce8848730b88dc6ce11` |

This rollout establishes publication, installation and preservation. Product behavior was not re-tested; the [earlier execution-quality trials and their limits](quality-default-2026-10.md) still apply. Independent acceptance covers the substantive method repair; the subsequent version pins and factual distribution records use targeted checks. The next consumer is ordinary work in these upgraded checkouts. Raw install, initial failed diagnosis, upgrade and read-back observations remain under `.local/quality-default-2026-10-10/`.
