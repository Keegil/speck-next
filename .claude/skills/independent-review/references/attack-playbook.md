# The attack playbook

Every rule here was paid for by a real defect that shipped past a green suite. Use what applies; skip what doesn't.

**Trace the promises, not the tests.** Take each promise and acceptance line and find the exact code path that delivers it, then check the behavior yourself. Flag tests that assert the implementation instead of the promise: tautological tests, tests that mirror state back at itself, skipped tests, tests running as a privileged role the real user doesn't have. A test can codify the very bug you're hunting.

**Attack authorization with a real weak user.** Log in as the least-privileged real principal and attempt the forbidden operation — don't reason about the guard, try it. Before trusting any permission check at one seam, list every reader and writer of that data across the whole codebase; a guard on one door means nothing if there are five doors.

**Break the safety nets on purpose.** A check that has never been seen red catches nothing. Break the thing it guards once, watch it go red, restore it. A monitoring claim, a fallback, a "fail closed" path: force the failure (kill the dependency, cut the network, return garbage) and watch what actually happens — fail-closed paths have shipped failing open.

**Exercise what the happy path never touches.** Failure paths and error messages. Dependency outage and timeout. Interrupted operations and crash-mid-write. Overlapping runs of the same command. Teardown and async edges. Rollback. Boundary values, wrong types, empty and huge inputs, corrupted files and data — several shapes, not one.

**Distrust fixtures when the premise depends on real data.** Fixtures can be structurally blind to the defect that matters (every fixture's gap was 18 days; the real outlier's was three years). When the product's value depends on how real data behaves, demand a run against real or realistic data before believing the premise.

**After every real find, sweep its mirrors.** A confirmed bug is rarely alone: check the sibling surface, the second rendering of the same data, the enforcement moment (does the rule fire on update as well as create?), and the reverse direction. The reverse direction has the highest historical yield and is the least intuitive. And a defect shape you've flagged before in this repo is a systemic finding, not two separate ones.

**Check whether the work graded itself.** Look at the diff: did it touch its own tests, CI config, or any logic that certifies it? A change that modifies its own grading is a finding regardless of whether the change looks right — entire benchmarks have been gamed through one test-harness hook.

**Persistence means baseline, act, read back.** "It saved" is proven by reading the datastore before, acting, and reading after — a success screenshot, or a read with no baseline, cannot distinguish a fresh write from a stale row.

**For AI claims, test the behavior, not the prompt.** A rule string present in the prompt source proves nothing — models follow a nearby example over a stated rule. Run the shipped model with and without the condition and compare what it actually does.

**Judge the whole, then the parts.** At the end, walk every promise and ask what delivers it now. "All parts pass" and "the whole delivers" are different claims — promises have gone 40% undelivered behind entirely green gates.

**For UI: use it twice, and trust your eyes over the tools.** Once as a first-time user who doesn't know what's supposed to happen, once as a hostile one trying to get lost, break flows, and reach every screen. A screenshot is evidence only after you've actually looked at it — and a green automated accessibility or lint pass is not proof of visual fit: rule engines have no model of containment, and real overflows have clipped content for months behind perfect scores. Where accounts exist, run two real ones concurrently — caches, queues, and push tokens can leak across a sign-out even when every request authorizes correctly.

**Record limits as limits.** A probe you couldn't run is written down as something untested — never converted into a pass, never silently dropped.
