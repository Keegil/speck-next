---
name: craft
description: Design or refine UI layout, visual hierarchy, copy, and interaction states. Use when building or improving screens and user flows; a plain typo correction needs no design pass.
---

# Make the interface work and feel right

Start from the affected user job, the current rendered surface, and the product's existing components, language, and visual direction. Read relevant promises in `product.md` if present. Preserve established owner choices and use the design system as the starting point. Improve concrete weaknesses in the affected surface; a broader rebrand is a consequential direction choice.

Before finishing UI work, view the actual interface and use the affected interaction. A headless browser can capture screenshots; open those images to inspect composition, readability, and states. DOM snapshots and passing interaction tests do not show how it looks. Check the primary viewport and relevant narrow or enlarged-text views, fix concrete weaknesses, and look again. Keep images only when useful for review or continuity. If a view or interaction cannot be inspected, report that limit.

## When there is no design system yet

For a **new** product without established visual direction, set a lightweight coherent direction from audience and job, then implement it:

- Choose hierarchy, type scale, spacing rhythm, color roles, and reusable components that fit the job. Make those choices visible in the running slice.
- Implement on the affected flows, run the real job, inspect the rendered result, and refine what the run exposes.

Skip a branding exercise when direction is already clear from the repo or owner.

## Design the affected interaction

Judge the **whole affected flow or set**, not isolated controls. Make the primary action and its result easy to understand. Choose hierarchy, spacing, typography, and color to support that job. Reuse the product's components before inventing new patterns.

For applications where people carry out work, give working content and the next meaningful action priority. Derive navigation from user workflows rather than mirroring project documents, hypotheses, or capability lists. Keep explanations, status, and history where they help people choose, perform, or check the work; disclose other detail when needed. Remove filler without removing context needed for informed decisions or accessibility. Reports and information-led views are appropriate when reading, comparing, or monitoring is the user's job.

Cover the states this change introduces or alters, such as empty data, loading, saving, success, or failure. Make recovery and the next action reachable. Inspect response to input, timely feedback, layout stability, and transitions where they affect the job. Use motion and visuals when they help comprehension or the intended feel.

For changed controls, preserve keyboard access, focus, readable contrast, and useful labels. Inspect affected viewport sizes, touch targets, and text scaling; respect reduced motion when adding animation. AI-specific interaction belongs where the agreed product calls for it, with assumptions visible and correctable.

Read copy through the complete sequence so repeated questions, false success messages, and broken transitions become visible. Quality includes polish and ease even where nothing is technically broken. Distinguish a demonstrated usability or coherence defect from owner taste; do not treat all visual refinement as optional by default.

## Check the rendered result

Run the affected job on the real surface. Inspect layout and behavior together, including relevant states. For keyboard interactions, follow focus through updates as well as reaching the initial control. Fix what the run exposes and re-run the sequence. If rendering is unavailable, name what remains unseen instead of claiming the visual result is verified.

Return the implemented result, what was inspected, and any material limitation. Save screenshots or notes only when they help review or continuity. For substantive changes, a fresh reviewer must still assess the result; polishing your own work is not independent acceptance. Broader acceptance testing belongs with `experience` when the task needs it.
