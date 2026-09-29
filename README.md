# Speck Next

Speck Next is a small kernel — one page of instructions, five on-demand skills, optional templates — that helps an agent build products **proportionally**. The owner says what they want; the method scales from a typo fix to a multi-month product without forcing the same ceremony every time.

## What a session feels like

> **You:** People keep asking if the app can show who's coming to tomorrow's classes.
>
> **Agent:** Smallest real version: a "Tomorrow" list on the studio dashboard. Building it now.
> …It runs — I've been clicking through as a studio owner. Long names overflow on phones; fixed. Try tomorrow's view.
>
> **You:** Sort by class time, not alphabetically.
>
> **Agent:** Done, re-checked in the app. Fresh eyes walked it cold; nothing blocking. Landed.

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

Current version: **7.0.1**, with a method that scales to the request. The patch adds concise guidance for usable feedback, session continuity, and evidence-based harness changes. [Research and limits](work/harness-refresh-2026-09.md). This repository dogfoods [AGENTS.md](AGENTS.md). History: [docs/history/](docs/history/). Reviews: [docs/reviews/](docs/reviews/).

## Install and check

```sh
npx -y github:Keegil/speck-next#v7.0.1 install /path/to/repo
npx -y github:Keegil/speck-next#v7.0.1 upgrade /path/to/repo
```

For development, `bash devsuite/run.sh` runs deterministic installation, upgrade, preservation and refusal tests without model calls. Historical model campaigns require `--legacy`; their old fixed-team expectations do not govern v7.
