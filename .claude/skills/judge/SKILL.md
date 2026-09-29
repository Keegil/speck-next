---
name: judge
description: Independently review a change or proposal against the user's intent and evidence. Use for substantive code, product decisions, plans, or an explicit acceptance review; obvious typo and formatting fixes need only local checks.
---

# Decide whether the work meets the request

Review a result you did not author or contribute to. If you contributed, your checks help the next reviewer but cannot provide independent acceptance. Judge the actual scope: a proposal can be well supported without an implementation, while a claim of working software needs execution evidence.

## Establish the claim and subject

Read the user's request, applicable promises and decisions, and the result itself. Treat contributor notes as claims to investigate. Missing `product.md` does not prevent review; the request and relevant existing behavior may supply the criteria.

For code, identify the task's base and reviewed head. Inspect the full net diff and any claimed working-tree changes; the last commit alone can hide earlier defects. Keep relevant unchanged code and running behavior available. Tie findings to the version actually inspected.

## Challenge what could make the result wrong

- Compare with user intent: missing or partial behavior, contradictions, regressions, and unrequested changes. Preserve unrelated work when proposing repairs.
- Exercise the uncertainty that matters. Passing author tests and completion marks do not settle whether the agreed job works. Run the smallest probe that closes a consequential evidence gap; use `experience` for a broader workflow or failure walkthrough when needed.
- Check favorable claims against contrary evidence. For proposals, test assumptions against the repository, users, or external evidence instead of only checking documents against each other.
- Keep unresolved disagreements visible. Distinguish a requirement failure from a stylistic preference or optional improvement. Do not weaken agreed expectations to make the result pass.

Use another specialist only for a distinct material risk the current review cannot cover. One fresh context can both exercise the work and decide acceptance.

## Give a usable decision

State whether the requested result is acceptable, needs a concrete repair, or lacks consequential evidence. Name the inspected subject, supporting checks, findings, and limits. Do not imply that untested behavior passed.

For each blocking finding, explain its consequence and the smallest next action: fix the implementation, correct the plan, resolve a promise, or obtain missing evidence. Escalate only consequential owner choices that existing instructions do not settle. Ordinary authorized fixes need no new approval.

After a repair, re-run the affected scenario and inspect other paths sharing the same failing mechanism. Finish when the agreed scope is supported and material open items are explicit; unrelated improvement ideas do not hold acceptance.
