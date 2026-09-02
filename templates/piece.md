# [Piece name]

[A floor, not a form: grow this file when the piece needs more.]

**Serves:** [job/moment/foundation] · **Consumes:** [screen drawings/sections/material]

**Outcome:** [What works when this lands. Commit this before product code.]

**Before first run:** [Hard limit on planning time, tokens, and files read.]

**Proof plan and review cost:** [Runs · the checks that must pass for Built · exact user types and number of fresh testers, at least two · judge, plus second judge when risky or at a milestone · what each rules on. A safety net counts only after it has failed on purpose.]

## Role call decisions

[Decide before the affected decision or code. Product and Engineering are always called from distinct carriers. Call Business or Experience when its `product.md` condition fires, current evidence is missing or expired, a listed material change occurs, the answer is uncertain, or the role declares an effect. Product cannot waive those facts.]

| Role | Call | Product-specific condition | Direct current evidence |
|---|---|---|---|
| Product | called | always on substantial work | [owner record, product, map, decisions] |
| Business | [called/inactive] | [condition from `product.md`] | [evidence and expiry; when inactive, this factual row is the whole record — no carrier or contribution] |
| Experience | [called/inactive] | [condition from `product.md`] | [evidence and expiry; when inactive, this factual row is the whole record — no carrier or contribution] |
| Engineering | called | always on substantial work | [repo, runtime, dependencies, data, and real behavior] |

## Active pre-code contributions

[Include every called role and no inactive-role filler.]

| Role | Carrier | Direct evidence | Conclusion | Assumptions | Proposed change | Active decision |
|---|---|---|---|---|---|---|
| Product | [host-issued context/session] | [owner record, product, map, decisions] | | | | [consequence · earliest informative run] |
| Engineering | [distinct from Product] | [repo, runtime, dependencies, data, and real behavior] | | | | [consequence · earliest informative run] |
| [Business or Experience, only when called] | [distinct carrier] | [role-owned direct evidence] | | | | [consequence · earliest informative run] |

**Product synthesis:** [One resolved outcome and builder-ready handoff. Product preserves dissent and does not implement.]

**Preserved dissent:** [Consequence · evidence · earliest settling run. Show the owner only when it changes a promise, user-facing choice, risk, or order.]

## Informative role returns

[For every active role: carrier · named earliest informative run · run evidence · what changed or held · resulting product change. Once that run exists, a missing return leaves the concern unresolved and blocks landing.]

[A replacement is a new carrier that inherits the same evidence and prior contribution. Record the lineage; both original and replacement stay excluded from testing and judgment.]

## False inactive repair

[If evidence shows Business or Experience was wrongly inactive, stop. Route a wrong promise to Shape, a wrong piece or order to Map, or anything else to piece setup. Call the missed role and have Product re-synthesize before Engineering resumes. Name every affected Built line, receipt, tester verdict, and judgment as invalid; keep unrelated evidence. Require changed work, a new Built line, and a new receipt. Make the role mandatory on the next comparable piece; a repeat keeps it through the milestone. Otherwise: not triggered, with evidence.]

**Business ruling:** [Required for a business-changing piece and every milestone: `kept / broken / not judged` with evidence. The latter two block. Otherwise: not required, with reason.]

**Review receipt** *(commit before any tester runs)*:

- Built: [Quote the `state.md` line and its commit. It must literally say **Built** and cover the exact product files — written in the build's final commit, or in a records-only commit just after it. No build commit may land after it — except a fix landed during the review, which answers to the judge's re-run rules instead — and the receipt must open after the Built line was written. Otherwise stop, write Built in a new state-only commit, and open a new receipt. A build commit changes product code, screens, or data, not only records or state. After a rejected piece is fixed, quote a new Built line covering the fixed product files.]
- Testers: [For each: persona, tool, model, session.]
- Excluded contributors: [Every Product, Business, Experience, Engineering, specialist, and builder carrier, including original and replacement carriers. None may test or judge.]
- Dispatched: [Date and product commit under test.]
- Planned walks and commands: [List. For a batch, enumerate changes from the commit range.]
- Run owner: [Dispatching session.]
- Empty record: [A later session re-dispatches under its own named line.]
- Records and verdicts: [One link per tester; every verdict points to lived moments.]

**Judgment** *(fresh context that built and tested none of it)*:

- Judge: [Tool, model, session · date · piece and commit under judgment.]
- Challenges: [Questions, ordered re-runs, answers. Add a fresh follow-up context under the original tester’s receipt and append its run to that record.]
- Rulings: [Each promise: kept/broken/not judged · works · delivers the promise · good to use · quality hangs together · structure: sound/straining/fighting.]
- Second judge: [Required for milestones and risky pieces; rulings and disagreement.]
- Sent back: [Anything insufficient returns to shape, map, build, or more testing, with the trace.]

**Homes touched** *(for any rule landed or changed)*: [The greps used, every home they returned, each marked changed or untouched.]

**Result:** [What happened, what review changed, what remains open and where each open item went, and what the next builder should not relearn.]
