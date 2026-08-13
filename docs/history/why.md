# Why Speck Next exists

Archive — the case behind the clean sheet, condensed. The living description of Speck Next is the [README](../../README.md); nothing here is needed to use or build it.

Speck (v1–v11, Dec 2025–Aug 2026) kept catching real, serious bugs in the owner's products: a crisis-support path that failed open during an AI outage, a forgeable audit log behind a green test suite, workouts silently not saved behind a "Set logged." toast, a gambling ad classified as editorial because the unit test asserted the bug. Every one of those catches came from the same two moves — someone independent attacking the work, and the real product actually being run.

Everything else grew. By v11.2 the methodology was 70 skills, 130 scripts (43.8k lines, 42% of them tests of the machinery itself), 58 templates, 53 coined terms, and 3.1 MB installed into every product repo. A 50-line feature cost ~53k tokens of process at 18 lines of paperwork per line of code, a typo fix had no path smaller than a full story, and in the owner's five product repos 40% of all commits touched only process files. The heaviest ceremony produced the least: one epic ran four adversarial document passes yielding 183 findings with zero overlap against the 97 real defects, all of which were found by running things. Two disciplined slim-downs (v8, v11) made the system cheaper to load without making it smaller; in the final six weeks, 63% of all fix commits were fixes to the enforcement machinery itself. The owner's verdict on the felt experience: like watching an agent speak a foreign language.

The decision (recorded in [telum-ai/speck#130](https://github.com/telum-ai/speck/issues/130) with two independent reviews): keep the two moves that worked, delete the rest, and rebuild from a one-page kernel in a fresh repository — with old Speck kept intact as the fallback, the failure archive, and the benchmark opponent the successor must beat at full strength.

What happened to each piece of v11 machinery, and where its protection lives now: [what-died.md](what-died.md). How the founding documents were attacked and revised on the way here: [../reviews/](../reviews/).
