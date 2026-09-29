# Evaluate an agent, skill, or harness

Use a small set of real tasks, including the failure being repaired and a simpler case that should stay cheap. Compare with the prior setup; isolate the effect of individual changes when practical. Choose examples before tuning the instructions and keep separate examples for a later check when optimizing repeatedly.

For skills, separate discovery from execution. Try direct and indirect requests that should activate the skill, plus realistic adjacent requests that should not. Test the available descriptions together when skills overlap. Explicitly naming a skill checks its execution, not automatic discovery. A catalog-selection exercise is not proof that a host actually loaded the skill.

For execution, give a fresh context the request, skill, and minimum raw materials without the intended answer or author conclusions. Inspect its actual result and relevant tool actions. Check that it preserved scope, used needed resources, stopped appropriately, and avoided unnecessary work. Metadata validation alone cannot establish this behavior.

Name task selection, model, tools, budget, starting state, outcomes, and available elapsed/token costs. Track human intervention and review/rework separately when claiming effort savings. For continuing product work, include a follow-up change on the produced checkout and check retained behavior.

Judge behavior and data, not a prescribed tool sequence or the agent's success report. Inspect traces for misleading grades and environment failures; keep trials isolated. Repeat when variability could change the decision, within the agreed budget. A single successful run is an example, not a reliability estimate. If no comparison ran, label effectiveness unbenchmarked. Token counts are cost, not quality.

When external research informs the comparison, use the [research guidance](../../shape-product/references/research.md). Retain useful evidence in the existing work record; a new evaluation framework is not a prerequisite for a bounded change.
