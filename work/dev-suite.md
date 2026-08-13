# The development suite

**Outcome:** a handful of tiny scored tasks the kernel can be measured on in minutes, so a method change shows its effect the same day: at least one bug-hunt task (visible planting on a pulse-sized toy), one small-change task (paperwork must stay zero), and one honest-state task (overclaim must be refused) — each with mechanically checkable observables and a one-command runner that prints a small scorecard.

**How I'll know it works:** every check must be seen failing before a pass counts, and live runs must be fresh governed sessions, not the builder.

**Result (2026-08-13):** built at `devsuite/` — runner + three tasks (small-change, bug-hunt, honest-state), Codex driver (Claude driver wired but its CLI login is expired). Red-proof done via control mode: the runner plants each violation with no agent and all three KEY checks went red — this replaced the planned loosen-the-review-skill regression, since it proves the same thing per task and cheaper. Live run: 3 of 3 passed with fresh cross-vendor sessions; the honesty task's agent refused the done-claim in writing after verifying the feature didn't exist. Checks are deterministic; agent runs are n=1 per task so far — repetition counts become interesting only if a task starts flapping.

**Open:** a shaping-quality task (does a governed agent shape a fuzzy product into a real product.md?) once the shaping skill exists; the Claude driver needs `claude login`.
