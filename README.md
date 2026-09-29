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

Current version: **7.0.4**. Skills and templates share the same proportional workflow, and automated checks catch release, link, discovery, and size drift. [Consistency review and validation](work/consistency-2026-09.md). [Skill design](work/skills-refresh-2026-09.md) and [research](work/upstream-round-2026-09.md) retain their measured scope. This repository uses [AGENTS.md](AGENTS.md). Historical material: [prior records](docs/history/v7.0.3-records.md), [Pulse example](examples/pulse/README.md), and [reviews](docs/reviews/).

## Install and check

Have Node.js/npm and Git available. The target directory must already exist and be a Git repository. For a new project, create it and run `git init` there first. Install into a fresh repository; use upgrade for a repository that already has a Speck Next marker.

```sh
npx -y github:Keegil/speck-next#v7.0.4 install /path/to/repo
npx -y github:Keegil/speck-next#v7.0.4 upgrade /path/to/repo
```

For development, `bash devsuite/run.sh` checks release consistency, skill metadata, packaged references, discovery and size limits, then installation, upgrade, preservation and refusal behavior. It uses no model calls. GitHub Actions runs the same default checks. Historical model campaigns require `--legacy`; their old fixed-team expectations do not govern v7.
