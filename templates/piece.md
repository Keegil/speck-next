# [Piece name]

[A floor, not a form: grow this file when the piece needs more.]

**Serves:** [job/moment/foundation] · **Consumes:** [actual drawing/output reference, sections, material]

**Outcome:** [What works when this lands. Commit this before product code.]

**Token estimate:** [Estimated gross, cached, and fresh tokens; assumptions. This is Business cost evidence, not a product gate.]

**Execution authorization:** [Before any model-bearing work: maximum model turns or contexts · elapsed time · retries · fallbacks · owner interruptions · pre-first-run time · pre-first-run files. Exhaustion forbids another model-bearing turn.]

**Proof plan and review cost:** [Existing real result, if any · runs · the checks that must pass for Built · exact user types and number of fresh testers, at least two · judge, plus second judge when risky or at a milestone · what each rules on. A safety net counts only after it has failed on purpose. Once a real result exists, name the concrete fresh-review product finding or genuinely new product claim that would authorize another build; method or cost findings cannot.]

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

**Product synthesis:** [One resolved outcome and builder-ready handoff. For a substantial user-facing change, called Experience composes the complete user job and meaningful states from the approved drawing and declared feel, using the existing drawing or this work record rather than requiring a new artifact. Name that actual drawing/output reference and the one Engineering carrier that owns integration. Product makes the composition binding, preserves dissent, and does not implement.]

**Preserved dissent:** [Consequence · evidence · earliest settling run. Show the owner only when it changes a promise, user-facing choice, risk, or order.]

## Informative role returns

[For every active role: carrier · named earliest informative run · run evidence · what changed or held · resulting product change. The named run and its return are both required before landing; if either is missing, the concern remains unresolved and the piece cannot land.]

[A replacement is a new carrier that inherits the same evidence and prior contribution. Record the lineage; both original and replacement stay excluded from testing and judgment.]

[For a concrete failure of the integrated experience, whoever observes it: name the failed complete sequence, the dependent work now held, and the independent work that may continue. After the fix, record the affected complete-sequence re-run, called Experience's decision on whether the original concrete finding is resolved, and every other role return whose consequence changed. Product lifts the hold only when that finding is resolved. Authorization exhaustion closes further model work while preserving the failure and hold. This is conditional; do not add a fixed extra return to unaffected runs or summon the team for a genuine unrelated small change. A small component repair or unrelated return does not lift the larger hold.]

## False inactive repair

[If evidence shows Business or Experience was wrongly inactive, stop. Route a wrong promise to Shape, a wrong piece or order to Map, or anything else to piece setup. Call the missed role and have Product re-synthesize before Engineering resumes. Name every affected Built line, receipt, tester verdict, and judgment as invalid; keep unrelated evidence. Require changed work, a new Built line, and a new receipt. Make the role mandatory on the next comparable piece; a repeat keeps it through the milestone. Otherwise: not triggered, with evidence.]

## Handled-concern miss escalation

[If a called role said its concern was handled and a consequential miss later proves otherwise, record the role, prior conclusion, and direct miss evidence. Keep the role involved at the next comparable piece's key decisions and informative runs. A repeat keeps it involved through the milestone until measured evidence supports relaxing it. This does not replace the current-piece repair for false inactivity. Otherwise: not triggered, with evidence.]

**Business ruling:** [Required for a business-changing piece and every milestone: `kept / broken / not judged` with evidence. The latter two block. Otherwise: not required, with reason.]

**Result disposition:** [Record separately: product evidence may enter review / cannot enter review · cost experiment passed / failed / not run, with measured gross, cached, and fresh tokens against the estimate · further model work open / closed against the declared authorization and any concrete product finding or new claim. One disposition cannot rescue or erase another; historical failures stay failed.]

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
