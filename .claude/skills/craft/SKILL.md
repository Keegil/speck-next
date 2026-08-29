---
name: craft
description: The taste bar while building anything a user sees. Use during the build step for every screen, component, or user-visible surface.
---

# craft

**Functionally correct is not done. It's done when it's crafted.** Before building any user-visible surface, get the product's declared feel from `product.md` in your head — the adjectives, the "feels like X, not Y" lines, the restraint rules, the named cheapeners. That declaration is the taste anchor; everything below adapts to it, never overrides it.

The principles that separate crafted from generic, earned across real products:

- **Typography carries the screen.** Real hierarchy — display, heading, body, caption — built from size, weight, spacing, and case, used deliberately. A headline has presence; if all text is one size and weight, the screen is flat and it shows.
- **Whitespace is a design element.** Group the related tightly, separate the unrelated generously, let things breathe. Cramped reads as cheap; generous reads as considered.
- **Every state is designed.** Hover, focus, pressed, disabled, loading, empty, error — all of them, not just the default. Loading gets a skeleton, never a blank; an empty state is an opportunity, not an afterthought; an error is designed, not just red text. Focus is visible and custom, never the browser default.
- **Motion follows the product's philosophy.** Calm products move minimally and instantly; playful ones choreograph. Never animate "because" — motion communicates or it goes. Always respect reduced-motion preferences.
- **Depth over deadness.** Flat single-color everything feels generic; subtle gradients, layered shadows, and surface texture read as quality — in the amount the declared feel allows, which for a calm product is very little.
- **Color has a job.** Accents pop because they're rare; sections separate through background shifts; emphasis is deliberate. All-one-temperature is blandness, not restraint.
- **Components have character.** A button, card, or input should feel like it belongs to this product and no other. Forms feel like conversations, not spreadsheets — and in an AI-first product, most form fields shouldn't exist at all: the model infers, pre-fills, and asks for confirmation.

After any copy change, read the whole flow the change lives in as one text — hunting duplicates, orphaned references, and broken bridges — at the change, not only when the hearing later walks the flow. An owner once caught a screen still re-arguing what an earlier screen had already taught him — three elements on it, all dead duplicates of what he had just read.

Before calling a surface done, look at it — actually render it and look — and ask: does it embody the declared feel, does every state hold up, would a demanding stranger call it crafted? Any "no" or "not sure" means iterate. And when a runtime renders something differently than the code suggests (a pixel bug that only shows on the real device), write the signature and safe form into the work file so the next agent greps instead of rediscovering.
