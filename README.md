# Speck Next

Speck Next helps an agent build products with as little process as the work needs. One entrypoint, five on-demand skills, and optional templates support anything from a typo fix to a continuing product.

## What a session feels like

> **You:** People keep asking if the app can show who's coming to tomorrow's classes.
>
> **Agent:** Smallest real version: a "Tomorrow" list on the studio dashboard. Building it now.
> …It runs. I checked the flow as a studio owner and fixed overflowing names on phones. An independent reviewer checked the feature. Try tomorrow's view.
>
> **You:** Sort by class time, not alphabetically.
>
> **Agent:** Done. Class-time ordering is checked in the app; the rest of the view still works.

No vocabulary lesson. The agent used the real product while building.

## How it works (v7)

**Intent-led, not phase-led.** Five capabilities (shape, map, build, experience, judge); build is the core loop. Five skills: `shape-product`, `map-build`, `craft`, `experience`, `judge`. Combined, skipped, or revisited on evidence. Missing `product.md` does not force a shaping project.

**Records when they earn their keep.** `product.md`, `map.md`, `state.md`, `decisions.md`, `work/` as needed. Templates are starting examples — keep useful fields only.

**Expertise when uncertainty is costly.** Product, Business, Experience, and Engineering are lenses, not four mandatory meetings per task. Separate judgment before landing **substantive** changes; trivial reversible fixes get a targeted check. More testers, judges, or specialists appear when distinct risk demands them — not as a fixed panel.

**Real use and honest evidence.** Build on the running surface. Independent reviewers may exercise and accept in one fresh context. Token totals inform cost; they do not pass or fail the product.

**Protect what hurts.** Auth, money, privacy, data integrity, regulation, and irreversibility get care on the **affected** behavior — a short diff is not an excuse.

**Upgrade:** `npx -y github:Keegil/speck-next upgrade` on **marker-bearing** Speck Next repos (supported legacy through v7). Preserves owner records; supersedes v6 **procedure** (assessments, mandatory gates) without erasing product findings. **Old Speck** (unmarked v11 and earlier) has **no** converter yet — the command refuses honestly.

Hard limits and promises: [CONTRACT.md](CONTRACT.md). Evidence and limits: [capabilities.md](capabilities.md).

## Status

Current version: **7.1.0**. The optional toolkit bundles Graft, ripgrep, jq, ast-grep and RTK with pinned downloads, a managed cache and the same CLI for Claude and Codex. The five skills, optional records and proportional workflow remain the method. [Toolkit verification](work/toolkit-7.1.md) records current scope and limits. Earlier [consistency](work/consistency-2026-09.md), [skill](work/skills-refresh-2026-09.md) and [research](work/upstream-round-2026-09.md) results retain their measured scope.

## Install and check

Have Node.js/npm and Git available. The target directory must already exist and be a Git repository. For a new project, create it and run `git init` there first. Install into a fresh repository; use upgrade for a repository that already has a Speck Next marker.

```sh
npx -y github:Keegil/speck-next#v7.1.0 install /path/to/repo
npx -y github:Keegil/speck-next#v7.1.0 upgrade /path/to/repo
```

## Optional toolkit

Set up the tools once, then use them where they help. The manager supports macOS and Linux on arm64/x64. It requires Node.js 20 or newer, npm, Git, `tar`, `unzip`, and network access for downloads; Linux needs glibc for some binaries. Graft's native dependencies may require a compiler toolchain and Python. Normal method installation does not download the toolkit. Windows setup is not supported in this release.

```sh
npx -y github:Keegil/speck-next#v7.1.0 tools setup
npx -y github:Keegil/speck-next#v7.1.0 tools doctor
npx -y github:Keegil/speck-next#v7.1.0 tools run rg -- -n 'customerId' src
npx -y github:Keegil/speck-next#v7.1.0 tools run jq -- '.version' package.json
npx -y github:Keegil/speck-next#v7.1.0 tools run graft -- build .
npx -y github:Keegil/speck-next#v7.1.0 tools run graft -- skeleton src/example.ts .
npx -y github:Keegil/speck-next#v7.1.0 tools run ast-grep -- run --lang ts --pattern 'console.log($$$ARGS)' src
npx -y github:Keegil/speck-next#v7.1.0 tools run rtk -- git status
```

| Tool | Useful for |
|---|---|
| [Graft](https://github.com/trailhq/Graft) | Code signatures and caller navigation. Build a missing graph explicitly; use source and tests to check consequential findings. |
| [ripgrep](https://github.com/BurntSushi/ripgrep) | Fast, targeted text searches, including files a code graph cannot index. |
| [jq](https://github.com/jqlang/jq) | Extracting and transforming the JSON fields the task actually needs. |
| [ast-grep](https://github.com/ast-grep/ast-grep) | Structural code searches and reviewed, repeatable rewrites. |
| [RTK](https://github.com/rtk-ai/rtk) | Compact readable summaries of supported command output. Inspect original output for errors, ambiguity and completion evidence. |

Setup owns `~/.cache/speck-next/tools` (or `SPECK_NEXT_TOOL_HOME`) and records provenance. Choose a dedicated real directory; symlinks anywhere in its path and nonempty unowned caches are refused. If your home or `~/.cache` is a symlink, set `SPECK_NEXT_TOOL_HOME` to a fully resolved path. Existing PATH tools are reported without replacement; the launcher uses the managed versions. Downloads are checksum-verified. Graft installs native dependencies with npm lifecycle scripts enabled and retains their resolved lockfile; its pinned tarball does not freeze every transitive dependency across fresh installs.

The launcher preserves child exit status and disables tool telemetry. No PATH edits, global agent configuration or vendor integration hooks are installed. Tools retain their normal runtime behavior: Graft may write `~/.graft` update state and check npm for updates; RTK records local usage. Graft's explicit build writes its repository cache and ignore entry; its paid deep mode is not run automatically. RTK is invoked explicitly, so it does not silently rewrite shell commands. Keep machine-consumed JSON, patches and mutation commands on their original tools.

Setup retains successful installs if another tool fails and reports a nonzero result. Retry `tools setup` to finish missing tools. An interrupted installation is retired on retry once its process and children have exited; a live installation remains protected. Retired stages and locks remain beside the cache; stages can retain hundreds of megabytes until their reported directories are removed.

`tools doctor --json` probes versions and returns machine-readable status, with exit 1 when the complete managed bundle is unavailable. It does not install or repair anything. `tools remove` renames the owned cache to a reported retired directory for recovery; it does not reclaim its disk space or delete existing installations, vendor runtime state or project indexes. Exact versions, sources, licenses and download hashes live in [the manifest](bin/toolkit-manifest.json). Availability and smaller outputs do not establish whole-task token savings.

## Development

`bash devsuite/run.sh` checks release consistency, skill metadata, references, discovery, footprint, toolkit failure paths, and method install/upgrade preservation. These deterministic checks make no model calls or tool downloads. `python3 devsuite/toolkit-smoke.py` exercises the real downloads and all five tools in a temporary cache. Historical model campaigns require `--legacy`; their old fixed-team expectations do not govern v7.
