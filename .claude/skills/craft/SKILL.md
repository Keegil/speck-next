---
name: craft
description: Sets the quality bar for anything a user sees. Use while building every screen, component, and user-visible surface.
---

# craft

Correct is not finished until it is crafted. Before building a visible surface, read the declared feel in `product.md`: its adjectives, “feels like X, not Y” lines, restraint rules, and named cheapeners. That feel anchors every choice below.

## Build with character

- **Typography carries the screen.** Create clear display, heading, body, and caption levels through size, weight, spacing, and case. A headline needs presence. One size and weight makes a flat screen.
- **Whitespace shows relationships.** Keep related things close, separate unrelated things, and leave room to breathe. Cramped looks cheap; considered space guides the eye.
- **Design every state.** Cover hover, focus, pressed, disabled, loading, empty, error, and success. Use a skeleton instead of a blank loading screen. Make empty and error states useful. Give focus a visible treatment that belongs to the product.
- **Let motion serve the feel.** Calm products move little and quickly; playful products may choreograph. Motion must communicate something, and reduced-motion preferences always win.
- **Use depth without noise.** Gradients, layered shadows, and texture can add quality, but only in the amount the declared feel allows. Calm products may need almost none.
- **Give color a job.** Keep accents rare enough to matter. Use background shifts to separate sections and color to create deliberate emphasis. One temperature everywhere is bland, not restrained.
- **Make components belong here.** Buttons, cards, and inputs should feel specific to this product. Forms should feel like conversations rather than spreadsheets. In an AI-first product, let the model infer, pre-fill, and ask for confirmation instead of showing fields it can replace.

## Read the complete interaction

After changing copy, read its entire flow as one text. Find repeated ideas, references that no longer point anywhere, and broken transitions at the time of change. An owner once caught a screen still re-arguing what an earlier screen had already taught him — three elements on it, all dead duplicates of what he had just read.

For a substantial user-facing change, called Experience composes the complete user job and meaningful states from the approved drawing and declared feel before code, using the existing drawing or piece work record. Product makes that composition binding in its handoff. One Engineering owner carries it through the integrated run and any finding-driven re-run, even when bounded parts are delegated. Inspect the sequence as a person experiences it, including the transitions and the result that later work will build on. A concrete failure of the integrated experience holds that dependent work until the affected complete sequence is fixed and run again, whoever observes it. Called Experience then reads the changed sequence and decides whether the original finding is resolved; other roles return only when their consequence changed. If authorization runs out first, preserve the failure and stop the affected work. Independent unrelated work and genuine unrelated small changes continue without extra ceremony. A small component repair or unrelated return does not lift the larger hold.

## Look before calling it done

Render the surface and inspect it. Ask whether it embodies the declared feel, whether every state holds up, and whether a demanding stranger would call it crafted. Iterate on every “no” or “not sure.”

When the real runtime renders differently from the code, write the defect’s recognizable signature and the safe pattern into the piece’s work file. The next builder should be able to search for it instead of rediscovering it.
