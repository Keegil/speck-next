# Questions for mapping

Choose prompts where the work's boundaries, dependencies, or order are uncertain. Start from the accepted request and relevant existing records. Resolve routine technical order yourself; bring the owner tradeoffs that change the result, priorities, risk, or budget.

## When the work needs dividing

- What is the smallest complete increment that someone can use or that proves a necessary dependency? What does each part contribute to that result?
- Which drawings, examples, data, or other supporting material affect the work? Where will they be used, tested, or deliberately deferred?
- Does the proposed work cover the agreed scope? Which behavior is missing, and which additions lack a clear purpose?

## When order could change the outcome

- What must exist to exercise each part: data, accounts, another feature, or an external service? Which order makes those dependencies available soon enough to test the work?
- Which uncertainty could invalidate later work? What is the smallest real probe that could settle it before an expensive commitment?
- When can someone first complete a useful job? What does delaying that result buy, and is it worth the wait?
- If priorities or assumptions change, which work would be costly to undo? Which order preserves useful choices within the budget?

## When parts or workers share an interface

- What observable contract do both sides need: inputs, outputs, errors, and relevant retry or compatibility behavior? Can existing types, examples, or tests express it clearly?
- Who owns the authoritative contract, and do both sides have its actual content and version? How will changes reach affected consumers?
- What run will exercise both sides together? Matching schemas or mocks can help development; which real interaction remains to be proved?
- If the contract changes, in what order can producers and consumers change without breaking the affected job?

## When proof or protection affects the plan

- What complete job will run for each useful increment, and what observations would establish that it works? Which failure or recovery behavior matters to that claim?
- Which parts affect money, access, private data, data integrity, or irreversible actions? What protection and test setup must exist before exposing them?
- What evidence and relevant context will an independent reviewer need for substantive work? Which dependency must be available to obtain that evidence?

## When a platform choice remains open

- What does the work require of its data, latency, reliability, privacy, and operating budget? Which existing setup already meets those needs?
- What would the viable alternatives cost to run, maintain, and replace? Which consequential tradeoff needs the owner's choice, and what evidence would reopen it?
