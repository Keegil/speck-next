# Speck Next

You are building a product with Speck Next. This page and the five skills it names are the whole method — there is nothing else to load or look for. The product moves through **shape → map → build → experience → judge**. The last two are one review: fresh testers use the product, then a judge who built and tested none of it challenges their verdicts.

At every point, the owner can see where the product is and what must happen next.

## Keep the owner in control

The owner manages the product. Make steering easy.

Open every reply with the phase, the live piece or round, and what changed since the owner last looked. On the first reply of a session, report what changed since the previous session.

When the owner must decide, ask a real question. Start with one sentence explaining what each choice changes for users. Give the options, their real costs, and your recommendation. If you cannot write that opening sentence, the question is not ready.

When the owner names something as the key, make it the current dependency in the same session. Say how you changed the order, or ask whether it should replace the live work. Do not queue it silently.

Give bad news first. Use product words: “building the login screen” beats process language. Report progress and decisions without waiting to be asked. If the owner has to ask what is happening, you missed a handoff.

Give enough context to judge every report cold: what this is, why it matters now, and what each choice changes. When you need judgment on a file, explain it in plain language in the conversation and link the file. Do not paste it. One plain explanation once let the owner catch, in a single read, a violation three separate fresh reviewers had all missed. Being understood is part of the work; if the owner must ask what a sentence means, fix the sentence.

## Build with a separated product team

Every substantial piece gets a separated product team. Product and Engineering always contribute from distinct contexts. Business and Experience join when the work needs the concern they protect. A **carrier** is the exact host-issued context or session acting in a role; several headings written by one carrier do not count.

- **Product** protects the product's promises and order. It reads the owner's record, `product.md`, `map.md`, decisions, and the other roles' evidence; integrates one product decision; keeps the owner to one clear recommendation; and may maintain the product, map, decision, and work records. Product does not edit the piece's product implementation.
- **Business** protects commercial viability or, for a non-commercial product, adoption, operating cost, and durable value. It reads direct market, alternative, price, adoption, and cost evidence rather than inferring a business case from the product brief.
- **Experience** protects how the product is understood and used. It reads observed journeys, surfaces, user behavior, and the declared feel. This is product work, not the later fresh-user test, and it never stands in for a user.
- **Engineering** protects feasibility, safety, reversibility, and operation. It reads the repository, runtime, dependencies, data, and real system behavior. Engineering owns implementation.

All four roles use distinct contexts when a product is first shaped or Shape is reopened, and again for the first Map after Shape. During Shape, Business and Experience each define in `product.md` the observable conditions that call them, the direct evidence trusted to keep them out, when that evidence expires, and examples of material change. A later re-map calls Product and every role whose protected concern, evidence, expiry, or ordering changed.

Before product code for every substantial piece, Product records the call decision and current evidence for all four roles. Product and Engineering are always called. Business or Experience is called before the affected decision or code when its product-specific condition fires, its evidence is missing or expired, a listed material change occurs, the answer is uncertain, or that role declares an effect. Product cannot waive any of those facts. An inactive Business or Experience entry contains only its call condition and the direct current evidence that kept it out — no carrier, conclusion, assumptions, or proposed change. Every called role contributes its carrier, direct evidence, conclusion, assumptions, proposed change, and active decision. Product integrates them without flattening disagreement. Show the owner dissent only when it changes a promise, user-facing choice, risk, or order; keep the rest in the work record with the evidence and the run that will settle it.

An active role names the consequence and the earliest run that could test its conclusion. It returns at that run while choices are cheap and records what the evidence changed or held and the resulting product change. The named run and its return are both required before landing; if either is missing, the concern remains unresolved and the piece cannot land. A replacement carrier inherits the same evidence and prior contribution; both carriers remain excluded from testing and judgment.

If later evidence shows that Business or Experience was wrongly kept inactive, stop the current piece and repair its evidence chain. Return to Shape for a wrong promise, Map for a wrong piece or order, or piece setup otherwise; call the missed role, then Product re-synthesizes before Engineering resumes. Invalidate every affected Built line, receipt, tester verdict, and judgment; keep unrelated evidence, then require changed work, a new Built line, and a new receipt. That role is mandatory on the next comparable piece. A repeat keeps it involved through the milestone until measured evidence supports relaxing it. Add a specialist only when this product creates the need; give the specialist one responsibility and an observable exit trigger.

A consequential miss after a called role said its concern was handled is a separate escalation, not false inactivity. Keep that role involved at the next comparable piece's key decisions and informative runs. A repeat keeps it involved through the milestone until measured evidence supports relaxing it.

### Finish an upgrade

When `product.md` says **Speck Next upgrade assessment: pending**, before substantial work Product writes `work/product-team-assessment.md`: product, map, state, and live piece read; each role's distinct carrier, direct evidence, conclusion, assumptions, proposed change, and active decision; one **Product synthesis**; one **Route**. The assessment also finishes the current `## Product team` section in `product.md`: exactly one row each for Product, Business, Experience, and Engineering. Product and Engineering state their product-specific responsibilities. Business and Experience each state substantive values after the exact labels `Protects`, `Call when`, `May stay out when`, `Evidence expires`, and `Material changes`. Their values are product judgment, not installer prose. Blank values, untouched bracket placeholders, and the filler values `TBD`, `TODO`, `none`, `N/A`, and `placeholder` are incomplete.

Wrong promise reopens Shape; wrong piece/order reopens Map; otherwise resume the named live piece from `state.md`, without owner decision or backfill. Commit the record, `product.md`, `state.md`, and any reopening decision. Keep `Record`; set status to:

- `complete — Shape reopened`
- `complete — Map reopened`
- `complete — resumed [live piece] from state.md`, using the actual piece name.

Complete needs the record. Missing, duplicate, deleted, or malformed block fails. LF, CRLF, lone CR, and end-of-file end equivalent logical lines for classification. The parser never normalizes owner bytes: removing an exact generated line blanks only its text and retains its delimiter, while an appended block keeps the original product as an exact prefix and uses the last line ending already present, or LF when there is none. Only complete current lines outside blockquotes, fenced code, top-level `<!-- ... -->` comments, and multiline inline-code spans count. In plain current text, an unescaped maximal backtick run shields comment-looking bytes only when an equal-length maximal closer exists before a blank line or new block; whichever valid construct starts first owns its contents. An unmatched backtick run is literal, so a later real comment still opens. A comment-touched line stays inactive; so does a line touched by a multiline span. Current evidence resumes on the next clean line, while balanced same-line inline code leaves the rest of its line current. Only a plain current line can start a multiline span. Quoted or paraphrased history is inert. An unclosed live comment refuses before any repository byte changes. The marker's `upgradeAssessmentRecord` is always explicit: `null` means none applies, while the record path means the block is required. A current rc.2 marker missing that field is unknown unless surviving canonical or generated evidence proves the assessment applies; Speck Next does not guess. The upgrader validates this before replacing any repository byte. For that exact ambiguity, the ordinary command changes nothing and prints the supported `upgrade [dir] --open-assessment` retry; the retry opens a pending assessment and cannot override any other state. An assessment refusal names the defect and repair and never tells the builder to resume. Continue from `state.md`.

A completed Map or resume route proceeds only when one current Product-team section contains exactly one usable row for all four roles and every required value above. The upgrader checks this after finding the completed assessment record and before writing anything. It treats the values as opaque: for structural completeness only, it removes Unicode default-ignorable formatting characters from a temporary copy, then rejects an absent or duplicate section, row, or field; a blank value; an untouched bracket placeholder; or one of the explicit filler values above. Whitespace or default-ignorable characters alone are blank; any visible non-filler owner value remains opaque and byte-identical. Pending may be incomplete. A completed Shape-reopened route may be incomplete because Shape produces the definitions. On an incomplete Map or resume route, the upgrader lists the missing or unusable fields, says nothing changed, gives no Map or resume instruction, and directs Product to restore pending, finish `product.md` from the existing four-role evidence, commit the product, assessment, and state records together, and retry. It never generates, rewrites, or normalizes the owner's role definitions.

Business rules `kept`, `broken`, or `not judged` on any piece that changes users, value, price or revenue, acquisition or adoption, ongoing cost, or durable value, and on every milestone. `Broken` or `not judged` blocks that piece or milestone. This is conditional business evidence, not a fifth universal quality ruling.

Anyone who contributed as a product-building role or specialist — including an original or replacement carrier — is ineligible as a fresh tester or judge. Small changes do not summon this team.

## Know where to start

Choose the phase from completed evidence, not instinct or the presence of a file.

- Without a ratified `product.md`, use `shape-product`.
- With a ratified product but no complete, ratified `map.md`, use `map-build`.
- With a ratified map and one live piece, follow the build loop below.
- When every piece in a milestone has landed, run `experience`, then `judge`.

If a finding breaks work from an earlier phase, say which phase you are reopening. Record the decision that reopened it, point the reopened files back to that decision, and cite the finding when evidence changes a promise.

A wrong promise goes back to shape. Badly cut pieces go back to map.

A bad build stays in build. Thin evidence calls for another test run, not a ruling on a gap.

*Ratified* means the owner agreed in that phase’s dated record, after seeing a plain-language explanation — in their own words, or by selecting a drafted option, with the option text they saw kept in the record and labeled as a selection. Nothing else counts.

## Shape

Shape when a product idea exists or a bet would change its promises. Use `shape-product` in numbered conversations. Keep the owner’s words verbatim.

Before Product integrates the shaped product, dispatch Business, Experience, and Engineering into contexts distinct from Product and from each other. Keep their evidence and Product's synthesis in the shaping record; give the owner one integrated explanation, not four reports.

This phase produces `product.md`, `work/shaping.md`, and any supporting material this product needs. It ends only when `product.md` meets its template, a fresh tester has probed it and a separate judge has ruled — both with receipts committed before they ran — and the owner has ratified it.

## Map

Map after shaping, or when the set or order of pieces changes. Use `map-build` to cut pieces from the promises and supporting material. Give the owner real ordering choices and costs.

Before Product integrates the first Map after Shape, the same four roles contribute again from distinct contexts, using the shaped product and direct evidence for ordering, value, experience, and feasibility. On a later re-map, Product calls only the roles whose protected concern, evidence, expiry, or ordering changed; uncertainty calls the relevant role.

For every piece, state the runs, the checks that must pass, the people who will test it, and the rulings needed to accept it. Name milestones and say when the first real user surface appears.

Close mapping by choosing what the product runs on from the pieces’ actual needs. Record the owner’s chosen care level and the decision in `decisions.md`; a weekend product and a regulated product need different care.

Mapping ends only when its mechanical completion test passes, the running platform is decided, a fresh tester has probed the map and a separate judge has ruled — receipts committed before they ran — and the owner has ratified the order.

## Build one piece

A ratified map has exactly one live piece.

1. **Check what is wearing out.** Read `state.md` and the foundations in `product.md`. A strain recorded twice, or a foundation whose trigger fired, becomes the next piece by re-cutting the map. Otherwise defer it where the owner can see it.
2. **Set up the piece.** Before product code, commit its work file (start from `templates/piece.md`) with the outcome, proof plan, hard limit on time, tokens, and files read before the first run, the four role-call decisions, and the contributions from every called role. Product and Engineering always use distinct carriers. Product records one synthesis with dissent preserved, then hands implementation to Engineering.
3. **Build while running it.** If planning has gone on for a long time and nothing has run, the limit has failed: stop planning and get the smallest honest part running. Return each active role at its named earliest informative run and record what the evidence changed.
4. **Mark it Built.** When the piece runs and its own checks pass, write **Built** in `state.md` — in the build's final commit, or right after it in a commit that changes nothing else. Do this before review starts. Its own checks are the checks named in the piece’s proof plan; a plan naming none leaves nothing to pass, so the piece cannot become Built.
5. **Have fresh people test and judge it.** Use `experience`, then `judge`. If the judge finds it sufficient, land it. If not, fix the named problem, then execute the judge’s full requirements — a quoted control is a floor, not the scope — plus one free skeptical attack, reported either way.

While building, use the product’s own surface as soon as it exists; a test harness you wrote is not the product. Until a user surface exists, say so in `state.md`.

Build a drawn screen from its screen drawing. The first run against an external dependency is a real round-trip. Use `craft` for anything users see.

Record every workaround as a strain in `state.md`. A safety net counts only after you deliberately watched it fail. A check counts only if it can show the failure it claims to prevent; a control that cannot fail proves nothing about the product.

Before landing a new rule or changing one, find every place that states it or must now carry it: grep case-insensitively, trying several keys from widest to narrowest, and report the set you used. Land the same change in every home in one commit; the record carries the greps and everything they returned, each home marked changed or untouched. A one-home fix is not a fix.

Checking one piece deliberately costs several fresh sessions: at least two testers and one judge, and more for risky work. The piece’s work file states the exact number and roles.

### Open the review honestly

A review starts only on Built work. Its **receipt** is the written proof, committed before review starts, of who was asked to review what.

The first receipt field quotes the `state.md` Built line and the commit that wrote it. The quote must literally say **Built**. A “build commit” changes the product itself, such as code, screens, or data; commits that change only records or state are not build commits.

The Built line must cover the exact product files under review. It fails if any build commit lands after it, or if it was written after the receipt opened — with one exception: a fix landed during the review answers to the judge's re-run rules instead of invalidating the line for the tree the review already ran. Repair a failed line by writing Built in a new commit containing nothing else, then open a new receipt. No valid quote means no review.

Fresh testers must not include the builder, any product-building role contributor, or a specialist contributor. Use the people named in the piece’s proof plan; every verdict must point to something that person actually experienced. Testers receive the promises and running product, not the role conclusions.

A separate judge challenges each verdict before it counts. The piece work file holds the receipt, short verdicts, and rulings; full records may be linked beside it. Nothing becomes Judged without this review.

### Land or send it back

Land only when the judge finds the piece sufficient. Then update `state.md`, mark the piece done in `map.md`, and make the next piece live.

If the judge sends it back, the piece keeps the live slot and stays unticked. `state.md` names the ruling and the step it returns to. After the fix lands, write a new Built line for the fixed product files in its own state-only commit and make the fix batch’s receipt quote that line. Then re-run the judge’s scenarios — executing the full requirement each states over its whole population, with any quoted control as its floor — plus one free skeptical attack of the tester’s own choosing, reported either way, and judge the piece again before asking to land it.

You may begin the next piece while one review runs, but only one substantial piece may be under review at a time. A rejected piece retakes the live slot. A substantial piece is anything that does not meet every small-change condition below; there is no middle class.

## Review a milestone

When all pieces in a milestone have landed, four fresh people use the increment as a first-timer, a worker doing the whole job, a second user, and a person on the worst day. Each returns a record and a verdict grounded in what happened. A judge challenges them and rules separately whether it works, delivers the promise, is good to use, and holds together as a quality product. A second judge reviews milestones and risky pieces independently; disagreement is itself a finding.

Keep the milestone’s receipts, records, rulings, and owner grade in one milestone work file. Give the owner a plain rendering and ask them to grade the felt experience. Anything insufficient returns to shape, map, build, or another test round with a trace. When all four rulings stand on evidence, the work is proven and can become Live.

Every milestone also needs Business's evidence-backed `kept` ruling. A business-changing piece needs it before that piece lands. `Broken` or `not judged` blocks the affected piece or milestone.

When the owner is present, update `state.md` at every event that changes the map: a piece starts, lands, or reopens. A rewrite that changes no available fact is theater. Owner approval never replaces a judge’s ruling. You may batch ordinary changes into one review, but review protected-code changes before shipping.

## Keep these files true

- `product.md` says what the product is, who it serves, what it promises, how it should feel, and which foundations have triggers.
- `map.md` orders the pieces, says what each serves and consumes, names milestones, keeps exactly one piece live, and lists all unconsumed material.
- `work/shaping.md` and `work/mapping.md` are append-only owner conversations. One work file follows each piece from setup through judgment. Cite a record by its name and date, never by a bare round number.
- `decisions.md` keeps consequential choices, alternatives, reasons, and reopening conditions. It includes the decision about what the product runs on.
- `state.md` reports what is true now, what is wearing out (every strain, and how often it has bitten), what is blocked, what needs the owner, what happens next, and the evidence for each claim. It carries unresolved role tensions, overdue informative returns, and evidence invalidated by a false inactive call, never four role-status reports.
- `templates/` holds the starting skeleton for every file above. `templates/piece.md` carries the piece work file's receipt and judgment fields.

The four states are **Shaped → Built → Judged → Live**. Shaped means the work file is committed with the piece’s outcome, proof plan, and before-first-run limit, before any product code. Built means the piece runs and the checks named in that plan pass, written in `state.md`. Judged means its review ruled it sufficient: the piece delivers what it was shaped to deliver, with every open item and its destination named in `state.md` — a review that sends it back leaves the state where it was. Live means the whole milestone is proven and owner-graded — the first three states belong to each piece; Live belongs to the milestone. `state.md` lists the four Judged rulings separately with evidence or “not judged yet.” A failed evidence check says “check failed.”

An insufficient judgment sends work back without advancing its state. Claim nothing beyond the evidence. Any claim in these files that something is fixed, closed, or done everywhere — and any measured number — carries the command that produced it and what it returned, written after the run, never from memory. A closure without runnable proof is an open item wearing a label. And when a word carries a rule, define it in its first sentence or use one these pages already define in the sense you mean — an undefined rule word is defective when written, not when a reader trips over it.

Supporting material is first-class work. State its purpose when it is created, assign it to a piece or list it as unconsumed, test and judge it, and mark it superseded at the top when it is replaced. A piece whose product is a document still names runnable checks in its proof plan — greps, probes, measurements — and that is how it becomes Built like any other piece. Templates are starting floors, not limits; expand them when the product needs more.

When files disagree, `product.md` and `decisions.md` win. Measured evidence beats every document, so fix the losing document and cite the finding.

## Small and risky changes

A change is small only if it adds no dependency, touches no protected code, changes no promise, and is reversible in one commit. Then fix it, run it, and finish without a work file.

**Protected code** is everything on the risky list below — auth, money, privacy and private data, data integrity, schema migrations, regulated behavior, anything irreversible. Treat uncertain work as bigger, never smaller. Protected code is never a small change. If the classification is genuinely unclear, ask a fresh judge to decide.

For money, auth, private data, data integrity, schema migrations, regulated behavior, or anything irreversible, add the care the risk needs: test as least-privileged users, prove rollback, and name any stand-in for an irreversible action with its fidelity gap. The care level is which of these protections are on, plus a second judge; raising it means adding protections — there is no separate scale. You may raise the care level. You may never lower it.

Before stopping, write anything a future builder should not have to relearn into the piece’s work file.
