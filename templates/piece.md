# [Piece name]

[A floor, not a form: grow this file when the piece needs more.]

**Serves:** [job/moment/foundation] · **Consumes:** [screen drawings/sections/material]

**Outcome:** [What works when this lands. Commit this before product code.]

**Before first run:** [Hard limit on planning time, tokens, and files read.]

**Proof plan and review cost:** [Runs · the checks that must pass for Built · exact user types and number of fresh testers, at least two · judge, plus second judge when risky or at a milestone · what each rules on. A safety net counts only after it has failed on purpose.]

**Review receipt** *(commit before any tester runs)*:

- Built: [Quote the `state.md` line and its commit. It must literally say **Built** and cover the exact product files — written in the build's final commit, or in a records-only commit just after it. No build commit may land after it — except a fix landed during the review, which answers to the judge's re-run rules instead — and the receipt must open after the Built line was written. Otherwise stop, write Built in a new state-only commit, and open a new receipt. A build commit changes product code, screens, or data, not only records or state. After a rejected piece is fixed, quote a new Built line covering the fixed product files.]
- Testers: [For each: persona, tool, model, session.]
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

**Result:** [What happened, what review changed, what remains open and where each open item went, and what the next builder should not relearn.]
