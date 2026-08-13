# Kernel capabilities

One row per capability, per the contract's anti-accretion promise: what failure it prevents, what it costs, what proof it has earned (or the date it must earn it by, or retire), and what would retire it.

| Capability | Prevents | Costs | Proof earned | Retires when |
|---|---|---|---|---|
| `AGENTS.md` (the method page) | building without running, dishonest state, big-bang spec ceremony | ~3.5 KB always loaded | governance check passed by a fresh cross-vendor agent (2026-08-13, confounded by the owner's global agent instructions — see devsuite note); pulse built under it end to end | a host stops loading it, or a leaner page proves equal in the dev suite |
| `independent-review` skill + playbook + experience reference | self-certified work, promise-breaking defects shipping | ~9 KB on demand | two pulse reviews found seven real promise-breakers the builder missed (2026-08-13); review-integrity dev-suite task guards the dispatch-receipt rule | reviews stop finding what proving runs missed, measured over a real product cycle |
| `shape-product` skill + questions | features-first products, unfalsifiable promises, facade differentiators, blank-form UX | ~7 KB on demand | pulse reshaped under it; its proving-scenario rule forced three innsikt redesigns before the design was honest (2026-08-13) | must show the same effect on the first real product (Pilot) by 2026-10-01 or be rewritten from what that reboot teaches |
| dev suite (`devsuite/`, repo-side, never installed) | kernel regressions shipping unmeasured; the method's claims going untested | ~0 installed; minutes per run | every check proven able to go red before any green counted (2026-08-13) | replaced by a better-instrumented suite, or v1's real-product evidence supersedes it |

Not yet built, tracked in [state.md](state.md): the promise-conservation check (`promise-dropped`), CI enforcement of the contract's size limits, the upgrader, the installer.
