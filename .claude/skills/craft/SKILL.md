---
name: craft
description: Design or refine UI layout, visual hierarchy, copy, and interaction states. Use when building or improving screens and user flows; a plain typo correction needs no design pass.
---

# Make the interface work and feel right

Start from the affected user job, the current rendered surface, and the product's existing components, language, and visual direction. Read relevant promises in `product.md` if present. Use nearby established patterns when direction is already clear; a missing design document does not require a branding exercise.

## Design the affected interaction

Make the primary action and its result easy to understand. Choose hierarchy, spacing, typography, and color to support that job. Reuse the product's components before inventing new patterns. Preserve owner choices; distinguish a demonstrated usability defect from a stylistic preference.

Cover the states this change introduces or alters, such as empty data, saving, success, or failure. Make recovery and the next action reachable. Read copy through the complete sequence so repeated questions, false success messages, and broken transitions become visible.

For changed controls, preserve keyboard access, focus, readable contrast, and useful labels. Inspect affected viewport sizes and text scaling; respect reduced motion when adding animation. AI-specific interaction belongs only where the product already calls for it, with assumptions visible and correctable.

## Check the rendered result

Run the affected job on the real surface. Inspect layout and behavior together, including relevant states; source code alone cannot establish visual quality. Fix what the run exposes and re-run the sequence. If rendering is unavailable, name what remains unseen instead of claiming the visual result is verified.

Return the implemented result, what was inspected, and any material limitation. Save screenshots or notes only when they help review or continuity. For substantive changes, a fresh reviewer must still assess the result; polishing your own work is not independent acceptance. Broader acceptance testing belongs with `experience` when the task needs it.
