# Quality in ordinary work

## Outcome and scope

Ordinary requests should receive thoughtful execution without a separate request for polish or best practices. This repair covers the root guidance, existing five skills, and product promises. It preserves scope, budgets, owner choices, protected behavior, independent review, and lightweight entry. No new skill, installed file, or mandatory record is added.

The owner reported repeated disappointing visual and interaction quality, then authorized the recommended method-wide repair with “Do it, bro!” on 10 October 2026. The starting source is `bb49cca11722897d9f741cbd8fc463fb9dbb6f21`. No individual earlier generated app was examined; the reported failure is user evidence, not a measured prevalence estimate.

## Change

The contract includes execution quality alongside function and process. Root guidance makes ordinary quality implicit, routes new UI and interaction/layout changes to craft, and distinguishes an early runnable slice from completion. Craft produces a visual direction for a new app, preserves owner choices, and refines the whole affected interaction. Shape, map, experience, and judge include relevant practices and workmanship in their existing responsibilities. Concrete quality weaknesses are findings within scope; unrelated improvements and taste differences do not force endless work.

Composer 2.5 implemented the bounded document edits; the integrator corrected routing, preserved explicit accessibility and AI-interaction guidance, and removed a blanket preference for fewer increments. Both host entrypoints continue to use the same source files.

## Comparison chosen before candidate runs

Use Composer 2.5 with identical ordinary requests, budgets, tools, and starting materials on old and revised instructions. Two fresh reading-planner builds per version provide a small qualitative comparison. One typo repair per version checks that quality guidance does not force redesign or records. Do not supply a visual reference, design direction, or “make it beautiful” instruction.

Reading-planner request:

> Build a local browser app to plan a weekend reading list. I can add books with a title, author and estimated reading hours, set my available weekend hours, select books for this weekend, see planned time against my available time, and remove books. Keep the list, selection and hour budget after a reload. Use HTML/CSS/JavaScript with no backend or sign-in. Keep it a small complete app. You have at most five minutes. Work in this directory and use its guidance. Leave a runnable result and a short report of what you checked. Do not create a product planning campaign or call another agent. You may use available browser tooling; if unavailable say what was not inspected. Stop at the time budget. Do not commit.

Typo request:

> Fix the misspelling in notice.txt. Keep the wording and punctuation otherwise unchanged. Work in this directory, check your change, then stop. Do not commit. You have at most 90 seconds.

Initial parallel old-instruction runs encountered a shared server port and unreliable shared browser snapshots. They are excluded from comparison. The comparison supplies the same environment note to every arm: use a separately launched Playwright Chromium browser/context and an unused local server port; the shared MCP browser is unavailable for these runs. The available Playwright path is provided equally. Environment repair does not change the requested result.

Runtime checks inspect fresh storage, adding/selecting books, time-budget feedback, persistence, removal, validation, keyboard interaction, and desktop/mobile rendering. Blind visual review compares anonymous results against the request. A separate reviewer assesses the full method change and evidence. Structural checks establish packaging and preservation, not visual quality or effectiveness.

## Evidence and limits

The source change received [independent acceptance](../docs/reviews/quality-default-2026-10.md) from Claude Opus 5.5 at packet `d655d373317202440e90073c43a1cef8aa8e2866`. That review exercised all six anonymous apps, reproduced the reported failures, and added a keyboard-removal probe. It accepted the guidance, not the defective fixture apps or a claim of improved outcomes. The reviewer inspected downscaled screenshots; the integrator also viewed original desktop and mobile captures.

The default deterministic suite passed 34 tests: nine surface controls, fourteen toolkit controls, and eleven installer checks. The final method-only amendments passed a fresh installed-surface check: 19 canonical files plus marker = 20, five skills, 43,306 bytes, and one discovery link reported separately. All five skill manifests validated; the final craft amendment was revalidated. These establish file/fixture integrity and distribution, not product quality.

### Fresh use

| Subjects | Observed result | Limit |
|---|---|---|
| Two old and two initial revised reading planners | All authors read craft and completed the core add/select/budget/persistence/remove job. The integrator's 52 assertions passed 48 times. One old app lost a zero-hour budget; one old and both revised apps lost focus on checkbox updates. | No author opened a rendered image in the recorded trace. Visual outputs were coherent in both arms; no quality gain was shown. |
| One old and one final revised packing app | Core add/category/pack/persist/remove checks and mobile containment passed. Sixteen of eighteen assertions passed; both apps lost focus on packing updates. | The revised author read the explicit image-viewing and focus-through-update instructions and still did neither. This is failed adoption, not successful execution of the new guidance. |
| One typo repair per arm | Both changed only `recieve` to `receive` in the supplied sentence, used three tool calls, and added no method records or redesign. Elapsed: 18.14 seconds old, 14.49 revised. | One example per arm; no efficiency or reliability inference. Final UI-only inspection clarification was added afterwards; the typo exemption was unchanged. |
| Native Codex with final instructions | `gpt-5.6-sol`, high effort, CLI 0.162.1. The first workspace-write run correctly reported that sandbox restrictions prevented port binding and Chromium launch. A fresh isolated run with browser-capable permissions executed add/pack/reload/remove checks and captured desktop/mobile screenshots. | No image-opening tool event appears in the native trace; the integrator viewed the captures. No same-host old-instruction control, enlarged-text or screen-reader test, or independent app acceptance. |

Both versions' apps lost focus after removal in the independent reviewer's additional probe. The illustrative fixtures are preserved as failed or incomplete examples, not accepted products. A mid-animation budget bar in the captures should not be treated as its settled state; the reviewer checked that distinction at runtime.

The reading comparison exposed that general wording did not produce visual inspection. The final revision moved the concrete image-viewing procedure near the start of craft, clarified the root instruction, and named keyboard focus through updates. The packing run then failed those explicit expectations. No further prompt tuning or repeated build campaign is justified by these examples alone.

[Requests, frozen app sources, screenshots, traces and observations](../docs/evidence/quality-default-2026-10/runs.json) retain the observations and anonymous-subject mapping. [Runtime assertions](../docs/evidence/quality-default-2026-10/observations.json) and the adjacent `inspect-reading.mjs` / `inspect-packing.mjs` scripts allow replay using the recorded Playwright installation. Supplementary [native runs](../docs/evidence/quality-default-2026-10/native-runs.json) retain the environment failures and token usage. Raw full logs remain in `.local/quality-default-2026-10-10/`.

The comparisons establish that the needed guidance is distributed and can be read, while these models did not reliably follow it. They do not reproduce the owner's original ugly-interface example or establish general quality gains, causation, consistent host activation, production performance, or a cost improvement. Source acceptance and unproved behavioral effectiveness remain separate.

## Distribution

Source commit `37a9721d085b0918f7b84956524e9c15d7a13223` was pushed to main. GitHub's [Release checks](https://github.com/Keegil/speck-next/actions/runs/38047746725) completed successfully at that SHA. This is a source increment; no new version tag was published.

The accepted method was also upgraded, committed and pushed in the four existing native checkouts under the previously authorized adopter rollout. All nineteen canonical method files and the Codex discovery link matched the source. The upgrade preserved each checkout's owner files, index and pre-existing dirty status; commits contained only the eight changed managed paths. Remote branch heads were read back and matched the recorded commits. [Rollout observations](../docs/evidence/quality-default-2026-10/adopter-rollout.json).

| Checkout | Remote commit | Owner paths preserved |
|---|---|---|
| Odd preparation app | `b97590d691e120e1c9ae140ce7b31db56c0ec782` | 16,581 |
| Splang Slack | `8b062b654082fddaa05dda9c6d2a5031d0f674c9` | 68 |
| Odd p2r review | `431e46e135aacc7284a251f562cf057e176b9ddd` | 540 |
| Odd Boka visual | `ff364ca606075502cc1038cf1fadfa59866b1d3b` | 519 |

These are installation and preservation observations. They do not establish downstream product quality. The supplementary native trial and these distribution records were recorded after the independent source review; neither changes the accepted method bytes.
