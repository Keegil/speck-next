# The right roles show up

**Serves:** all eight contract promises through selective product-role separation, honest adoption, and repair of a missed call in the current piece · **Consumes:** the ratified selective promise in `work/shaping.md`, the ratified executable seam in `work/mapping.md`, the failed universal `6.0.0-rc.1` candidate, and the rule-home census below

**Outcome:** A fresh or upgrading repository receives `6.0.0-rc.2` and can decide which independent product lenses the work actually needs. Product and Engineering are always separate on substantial work. Business and Experience join when their own conditions, evidence, expiry, a material change, or uncertainty requires them. An inactive role leaves a factual reason, not a pretend contribution. A missed call stops and repairs the current piece. This piece proves those rules and the migration deterministically; it does not claim that live role carriers finish affordably.

**Before first run:** Set at role dispatch: no more than four carriers and one contribution from each; no more than 90 minutes from the live-piece commit; no more than 120,000 aggregate host-reported tokens; no more than 30 unique repository files read before the first deterministic product run. The carrier and one-contribution limits held. The three non-Product carriers alone used at least 6,822,314 gross and 423,210 fresh tokens, so the token limit failed before Product was counted. The host evidence does not expose a trustworthy normalized file-read total, so that limit is not judged. Planning stops here; Engineering's first action after this commit is the smallest honest run against an exact rc.1 migration fixture.

Token command, reading the last host token record from each role session:

```sh
python3 - <<'PY'
import json
from pathlib import Path
base = Path.home() / ".codex/sessions/2026/09/02"
runs = {
    "Business": "rollout-2026-09-02T18-30-33-01a062f5-3a3a-7da3-bb4d-026a3a7525b9.jsonl",
    "Experience": "rollout-2026-09-02T18-30-45-01a062f5-6783-7242-9370-28d9fa14e2dc.jsonl",
    "Engineering": "rollout-2026-09-02T18-30-58-01a062f5-99e0-7712-90d0-f5c0f8506e63.jsonl",
}
totals = dict(input_tokens=0, cached_input_tokens=0, output_tokens=0, total_tokens=0, fresh_tokens=0)
for role, name in runs.items():
    usage = None
    for line in (base / name).read_text().splitlines():
        payload = json.loads(line).get("payload", {})
        info = payload.get("info") if payload.get("type") == "token_count" else None
        if isinstance(info, dict) and isinstance(info.get("total_token_usage"), dict):
            usage = info["total_token_usage"]
    values = {key: int(usage.get(key, 0)) for key in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")}
    values["fresh_tokens"] = values["input_tokens"] - values["cached_input_tokens"] + values["output_tokens"]
    for key, value in values.items():
        totals[key] += value
    print(role, " ".join(f"{key}={value}" for key, value in values.items()))
print("LOWER_BOUND_THREE_ROLES", " ".join(f"{key}={value}" for key, value in totals.items()))
PY
```

It returned:

```text
Business input_tokens=1293551 cached_input_tokens=1196928 output_tokens=9911 total_tokens=1303462 fresh_tokens=106534
Experience input_tokens=2687604 cached_input_tokens=2575232 output_tokens=19258 total_tokens=2706862 fresh_tokens=131630
Engineering input_tokens=2787732 cached_input_tokens=2626944 output_tokens=24258 total_tokens=2811990 fresh_tokens=185046
LOWER_BOUND_THREE_ROLES input_tokens=6768887 cached_input_tokens=6399104 output_tokens=53427 total_tokens=6822314 fresh_tokens=423210
```

**Proof plan and review cost:** Before edits, reproduce the known rc.1 migration failure on an exact generated fixture. Then run deterministic clean and broken twins for Product-plus-Engineering only, Business active, Experience active, all four active, ambiguity, expiry, false inactivity and current-piece repair, an overdue informative return, replacement-carrier lineage and exclusions, and Product/Engineering separation. Run fresh install plus v5, generated rc.1, custom-section, missing-product, dirty-worktree, failure-and-retry, and second-upgrade fixtures. Every clean subject must pass and every one-field mutation must fail with its subject count printed. `node --check`, Python compilation without cache writes, the existing separated-team control, the complete home census, exact installed/always-read/file/skill budgets, `git diff --check`, and the public-detail scan must pass. No governed Codex or Claude run, broker run, host proof, or component model probe belongs to this piece. After Built, two fresh testers use the candidate: one first-time builder routes contrasting pieces, and one mid-product upgrader resumes real work. One independent judge challenges both records and rules that it works, delivers the promise, is good to use, hangs together as a quality product, and has sound structure. Business rules separately before landing. The second milestone judge remains in Piece 9's milestone hearing unless this piece's evidence makes the work risky.

## Role call decisions

| Role | Decision | Product-specific reason | Earliest informative run |
|---|---|---|---|
| Product | Active | Always active on substantial work; this piece resolves the installed promise, migration behavior, and proof boundary. | The contrasting deterministic fixtures select exactly the required roles and reject false inactivity. |
| Business | Active | The piece changes adoption, owner attention, token and time cost, maintenance, and durable method value. | The no-model fresh/v5/rc.1/custom/missing/dirty/idempotent matrix completes with zero owner repair, bounded footprint, and honest output. |
| Experience | Active | The piece changes always-read wording, templates, role selection, upgrade output, builder handoff, comprehension, and trust. | A disposable fresh install and mid-product upgrade let a builder route contrasting pieces, leave no fake inactive-role prose, and understand what blocks landing. |
| Engineering | Active | Always active and separate from Product; this piece changes installed rules, migration, reversibility, reporting, and deterministic proof. | An exact generated rc.1 fixture first reproduces the obsolete universal contract, then crosses to rc.2 twice while preserving every unrelated byte. |

## Pre-code contributions

### Product

- **Carrier:** `/root`.
- **Direct evidence:** the owner's ratified “Lock selective separation!” and “Do it!”; `product.md`; `map.md`; `decisions.md`; the repaired Shape and Map records; the 266,484-gross-token failed governed run; and the three contributions below.
- **Conclusion:** Install one selective contract everywhere, repair both v5 and obsolete rc.1 repositories honestly, and prove repository semantics without reopening live-host cost in this piece.
- **Assumptions:** deterministic fixtures can prove routing, record, migration, reporting, and footprint behavior but cannot prove live carrier obedience or cost; Piece 9 owns that claim; old-Speck conversion and the already-running external product remain out of scope.
- **Proposed change:** make Product and Engineering the substantial-piece floor; call Business and Experience through their authored conditions and evidence; record current-piece repair and informative returns; migrate to rc.2 marker-last and byte-stably; keep host transport untouched.
- **Active decision:** active. A wrong integration either loses a needed lens or preserves the universal ceremony already disproved by cost. The selection fixture is the earliest disconfirming run.

### Business

- **Carrier:** `/root/piece8_business`.
- **Direct evidence:** the stopped governed run at 266,484 gross tokens in 110 seconds; the current major-only upgrader classification; the current universal checker; disposable fresh-install and pre-v6 fixtures; installed and always-read footprint measurements; and `capabilities.md`'s open host and field claims.
- **Conclusion:** this is a useful, low-cost adoption boundary, but the installed rc.1 candidate remains Business broken until the deterministic migration and routing evidence exists. Piece 8 cannot turn the failed host run green.
- **Assumptions:** local Node fixtures faithfully test install, migration, reporting, idempotence, selection, and current-piece repair; exact generated rc.1 text can be distinguished from owner-authored text; no installed file, skill, owner beat, or host proof is added.
- **Proposed change:** replace the universal contract in every home; migrate v5 and rc.1 to rc.2; replace only the exact generated universal paragraph; preserve custom and historical bytes; report the exact version/commit span, paths, diff, and footprint.
- **Active decision:** active. A bad selector loses a business concern; a bad upgrader leaves existing products on the costly universal cadence. The migration and selection matrix is the earliest disconfirming run.
- **Pre-code ruling:** deterministic and local implementation may proceed. This is not a `kept` ruling for the finished piece, release, or live-host execution.

### Experience

- **Carrier:** `/root/piece8_experience`.
- **Direct evidence:** the current universal `AGENTS.md`, fixed four-row piece template, universal contract and checker; disposable fresh, v5, rc.1, custom-section, and missing-product journeys; and the upgrader's current lack of a clear resume action.
- **Conclusion:** the current fresh and upgrading journeys are broken for selective separation. Builders need a visible factual call decision, full detail only from called roles, immediate repair of a missed lens, and a plain next action after upgrade.
- **Assumptions:** owner-authored bytes remain in order; a generated assessment status can be added beside a custom section without claiming historical assessment; the first informative Experience evidence is a builder journey, not syntax or a technical smoke run.
- **Proposed change:** make role-owned conditions, evidence, expiry, and material-change examples visible in product and map templates; split call decisions from active contributions in the piece; add current-piece repair, informative-return due points, and replacement exclusions; make rc.2 migration distinguish generated rc.1, custom, missing, and already-selective products; finish output with a plain `Next:` action.
- **Active decision:** active. Without the change, builders either fill departmental prose or silently skip a fired lens. Fresh-install and mid-product-upgrade journeys are the earliest disconfirming runs.

### Engineering

- **Carrier:** `/root/piece8_engineering`, distinct from Product and retained for implementation and its return.
- **Direct evidence:** the selective authority in `product.md` and the ratified Shape/Map records; universal cadence in `AGENTS.md`, Shape/Map skills, templates, contract, README, and checker; executable installer defects around major-only v6 detection, heading-based suppression, marker-before-migration, and incomplete reporting; and the commit boundary separating installed semantics from Piece 9 transport.
- **Conclusion:** replace every universal rule home with one selective contract, migrate marker-last and byte-stably to rc.2, and prove it through deterministic controls only.
- **Assumptions:** Piece 8 migration sources are v5.x and exact `6.0.0-rc.1`; custom bytes remain untouched while a canonical unassessed status is added; deterministic proof does not claim host obedience; no new installed file, skill, dependency, state, or owner beat is needed.
- **Proposed change:** update the installed method, Shape/Map prompts, product/map/piece/state templates, eight contract promises, public description and capability claim, package and installer; add a `--piece-8-controls` path to the existing separated-team checker; leave all host runner, broker, host-proof, and live fixture files untouched.
- **Active decision:** active. Otherwise an rc.1 repository silently retains the rejected contract or a false inactive decision leaves tainted Built/review evidence standing. The exact rc.1 before/after/retry fixture is the earliest disconfirming run.

## Product synthesis and Engineering handoff

One installed rule governs the work. All four distinct carriers form or reopen the product and take the first Map after Shape. Later re-maps call Product and every role whose protected concern, evidence, expiry, or ordering changed. Every substantial piece has distinct Product and Engineering carriers. Business and Experience join before the affected decision or code when their authored condition fires, evidence is missing or expired, a listed material change occurs, the answer is uncertain, or the role declares an effect. Product cannot waive those facts.

An inactive Business or Experience role records only its condition and the direct current evidence that kept it out. It has no carrier, conclusion, assumptions, or proposed change. Active roles keep the full contribution. Each active role names the earliest run that can actually test its conclusion and returns there; once that run exists, a missing return leaves the concern unresolved and blocks landing. Replacement carriers inherit the same evidence and prior contribution, and both original and replacement remain excluded from testing and judgment.

False inactivity repairs the current evidence chain first. Work stops and returns to Shape for a wrong promise, Map for a wrong piece or order, or piece setup otherwise. The missed role joins for the rest of the piece, Product re-synthesizes before Engineering resumes, and every affected Built line, receipt, tester verdict, and judgment becomes invalid. New work, a new Built line, and a new receipt are required. Unrelated evidence remains. The role is also mandatory on the next comparable piece; a repeat keeps it through the milestone.

Engineering owns the implementation listed in its contribution. Product owns only this work record and later product/map/decision/state truth. Engineering must first run the exact generated rc.1 control, then make the smallest installer-and-contract repair and rerun that same fixture twice before widening to the full matrix. The version is `6.0.0-rc.2`. The marker is written only after successful copying and migration. Missing `product.md` stays missing. Exact generated rc.1 prose is replaced; custom prose is preserved and receives one honest unassessed status without suppressing migration. Output names both ends, both commits when known, the migration outcome, working-tree paths across the complete installed surface plus `product.md`, and a plain next action. `capabilities.md` may claim only deterministic routing/migration proof; live hosts and field value stay open.

The home census used the case-insensitive families `product…business…experience…engineering`, `four roles|four separate|all four`, `every substantial piece`, `active|inactive role`, `first real run`, `product team`, `excluded contributors`, and `contributed as` across `AGENTS.md`, every skill and reference, every template, `CONTRACT.md`, `README.md`, `capabilities.md`, the installer, package, and separated-team task. Engineering changes `AGENTS.md`; the Shape and Map skills and question references; `templates/product.md`, `templates/map.md`, `templates/piece.md`, and `templates/state.md`; `CONTRACT.md`; `README.md`; `capabilities.md`; `package.json`; `bin/speck-next.js`; and `devsuite/tasks/separated-product-team/check.py`. It leaves `CLAUDE.md`, Craft, Experience and Judge and their references, `templates/decisions.md`, `templates/rounds.md`, every Product-owned record, and every Piece 9 runner/broker/host fixture untouched. The generic rounds template remains a conversation and receipt floor; the Shape and Map skills own their role-contribution fields.

**Preserved dissent:** Experience considers migration a distinct builder journey and insists on its own proof lane; Product keeps it inside Piece 8 because fresh and upgrading repositories consume the same installed selective contract, while keeping separate fixtures and a separate mid-product tester. Engineering proposed leaving the rounds template untouched; Product agrees after inspecting it because it states no universal attendance rule and delegates phase-specific records to the skills. The failed pre-run cost is not repaired by widening or reinterpreting the limit; it remains a finding for Piece 9's transport and context design.

## Informative returns

- **Product — carrier `/root`:** The contrasting routing subjects selected Product plus Engineering alone, added Business alone, added Experience alone, or called all four from the recorded conditions. Ambiguity, expired evidence, a false inactive call, a missing informative run, a missing return, replacement lineage, Product implementation, and same-carrier Product/Engineering each went red in their focused mutant. The selection rule held. The broader Product review did change the candidate seven times before this return: later re-maps had accidentally kept Engineering universal; a role could avoid returning by never creating its named run; the handled-concern miss rule had disappeared from the always-loaded page; a capability row exposed concrete fixture details; a missing-product upgrade gave an impossible next action; a clean retry told the builder to commit nonexistent changes; and the first porcelain status line lost its leading column. Engineering repaired each finding and the complete matrix passed again. **Resulting product change:** selective delivery now covers later re-maps, both halves of an informative return, both miss paths, abstract public evidence, state-aware upgrade guidance, and exact working-tree status. No Product concern remains unresolved before Built.
- **Business — carrier `/root/piece8_business`:** Eleven migration subjects covered fresh install, v5, exact generated rc.1, custom Product-team prose, missing product, assessed current product, dirty work, failed retry, an unknown version, a clean retry, and exact changed-path output. They completed without an owner question or manual repair; the 19-file / 76,998-byte fresh footprint, five skills, and 46,552-byte always-read surface remained inside the contract. The previous 266,484-gross-token governed run and this piece's 6,822,314-gross-token three-role setup lower bound remain failed evidence, not reclassified success. **Binding ruling: `kept` for Piece 8.** The selective repository and adoption boundary earns its cost and may proceed to Built and review. Live carrier execution, Piece 9, the milestone, and release remain `not judged`; this ruling does not permit any of them.
- **Experience — carrier `/root/piece8_experience`:** The first fresh-install and mid-product-upgrade walk found the core selection flow understandable but returned unresolved at `78857f9`: a repository with no `product.md` was told to run an assessment named in that missing file, and the first unstaged changed path looked staged because one status column was trimmed. At `737959a`, the same journey received one possible next action for every product state: create and ratify a missing product before Map, finish a pending product-and-map assessment, or resume the assessed product from `state.md`; a clean retry explicitly had nothing to commit, and the first porcelain line retained both columns. The selective call records, factual inactive rows, immediate false-inactive repair, and missing-run/return landing blocks also held in the executed subjects. **Result:** sufficient before Built; no Experience concern remains unresolved.
- **Engineering — carrier `/root/piece8_engineering`:** Before edits, an exact generated rc.1 fixture reported rc.1 to rc.1, left one universal paragraph and zero selective paragraphs, and said migration was not needed. After the repair, that fixture crossed to rc.2, replaced only the generated paragraph, preserved adjacent bytes, and stayed byte-stable on retry. The expanded routing and migration matrix, syntax checks, complete diff, home census, footprint, and leak control all passed at `737959a`. Experience's running journey changed Engineering's earlier conclusion and produced the state-aware `Next:` table plus exact porcelain output. **Result:** implementation held; no Engineering concern remains unresolved before Built.

The final Product readback ran these commands after all returns:

```sh
python3 devsuite/tasks/separated-product-team/check.py --piece-8-controls .
./devsuite/run.sh --control separated-product-team
node --check bin/speck-next.js
python3 -c 'from pathlib import Path; compile(Path("devsuite/tasks/separated-product-team/check.py").read_text(), "check.py", "exec")'
git diff --check ddb62f1..HEAD
node -e 'const p=require("./package.json"); if(p.version!=="6.0.0-rc.2") process.exit(1); console.log(p.version)'
find AGENTS.md CLAUDE.md .claude/skills templates -type f -print0 | sort -z | xargs -0 wc -c
wc -c AGENTS.md product.md map.md state.md
```

They returned `role-control subjects=26 clean=13 mutants=13`, `migration subjects=11`, and `Piece 8 controls: PASS`; the legacy control reported `1 of 1 tasks went red`; syntax, compilation, and diff checks returned zero; the package printed `6.0.0-rc.2`; the installed-method source was 17 files / 76,664 bytes; and the four always-read files totaled 46,552 bytes. A disposable Git repository then ran `node bin/speck-next.js install <fixture>` and returned 19 non-Git files / 76,998 bytes, marker `6.0.0-rc.2`, and no invented `product.md`. The added-line public-detail matcher was first watched matching its planted fixture, then returned zero matches over `capabilities.md` and zero over the complete installed-surface change.

The closing home census repeated the pre-code search families. Changed homes are `AGENTS.md`; Shape and Map skills plus their question references; product, map, piece, and state templates; `CONTRACT.md`; `README.md`; `capabilities.md`; `package.json`; the installer; and the separated-team checker. Inspected and intentionally untouched homes are `CLAUDE.md`; Craft; Experience and Judge plus their references; decisions and rounds templates; Product-owned records; and every Piece 9 runner, broker, host-proof, and live-fixture file. The only remaining exact universal paragraph is the rc.1 migration fingerprint and its control, never an installed rule.

## Review receipt

**Built line and commit:** `state.md` at `946b85a` says:

> **Built — Piece 8 “The right roles show up”:** product commits `10acad3`, `8bf17be`, `78857f9`, and `737959a` cover exactly `AGENTS.md`, `.claude/skills/shape-product/SKILL.md`, `.claude/skills/shape-product/references/questions.md`, `.claude/skills/map-build/SKILL.md`, `.claude/skills/map-build/references/questions.md`, `templates/product.md`, `templates/map.md`, `templates/piece.md`, `templates/state.md`, `CONTRACT.md`, `README.md`, `capabilities.md`, `package.json`, `bin/speck-next.js`, and `devsuite/tasks/separated-product-team/check.py`. The proof-plan commands and returned results recorded in `work/right-roles-show-up.md` pass selective routing and focused broken twins, current-piece repair, informative-run and return blocks, handled-miss escalation, replacement and exclusion, fresh install, eleven honest migration journeys, syntax, complete diff, footprint, and the public-detail boundary; the existing same-context control remains red. No product implementation commit follows `737959a`.

**Opened:** 2026-09-02, after `946b85a` and before either tester was dispatched.

**Candidate:** the exact product implementation ending at `737959a`; later commits `c88dc4a`, `946b85a`, and this receipt change records only role evidence, state, and the review request.

**Fresh tester 1 — first-time builder:** receives `product.md`, the Piece 8 promise and routing cases from `map.md`, and the installed candidate—not the product-role conclusions. They install into a disposable fresh repository, use the loaded method and templates to set up contrasting substantial changes, and decide whether Product/Engineering stay separate, Business/Experience appear only when facts call them, inactive roles leave no invented contribution, uncertainty cannot be waived, and the owner gets one understandable recommendation. They report what they actually ran and saw, the worst confusion, and a verdict.

**Fresh tester 2 — mid-product upgrader:** receives the same product promise plus supported v5, exact generated rc.1, custom-section, missing-product, dirty-work, and clean-retry journeys—not the product-role conclusions. They execute disposable upgrades, follow the printed next action, inspect preserved and changed bytes, and decide whether an existing builder can resume without fabricated history, manual surgery, or a false commit instruction. They report what they actually ran and saw, the worst trust failure, and a verdict.

**Judge:** after both tester records are committed, one fresh judge who built and tested none of this challenges their evidence and the candidate. The judge separately rules whether Piece 8 works, delivers the promise, is good to use, hangs together as a quality product, and has sound structure. A sufficient ruling must name every open item and its destination.

**Excluded contributors and prior readers:** `/root`, `/root/piece8_business`, `/root/piece8_experience`, `/root/piece8_engineering`, `/root/piece8_migration_audit`, `/root/piece8_contract_audit`, `/root/bounded_transport_review`, every earlier Shape or Map contributor/tester/judge, and any honest replacement carrier. Neither fresh tester nor the judge may come from this set, and the judge cannot be either tester.

## Result

The Piece 8 candidate was Built at `946b85a` from product commits `10acad3`, `8bf17be`, `78857f9`, and `737959a`; review opened at `a737eaa`. The first-time-builder verdict was sufficient and the mid-product-upgrader sent it back. The independent judge upheld and strengthened the send-back at round 1: the upgrade assessment has no executable completion/resume transition, quoted historical status can trap a completed assessment as pending, and checkout provenance is presented as though it identifies the installed surface. Piece 8 remains live and returns to build. Host affordability remains Piece 9's unresolved concern and cannot be inferred from Piece 8.

## Fresh testing — round 1

### First-time builder — `/root/piece8_fresh_builder`

**Candidate used:** product implementation through `737959a`; `git diff --exit-code 737959a..HEAD -- AGENTS.md CLAUDE.md bin templates .claude/skills` returned zero before the walk.

**What happened:** `node bin/speck-next.js install <fresh-git-fixture>` installed rc.2 with 19 files. Reading only the installed method and templates, the tester created four contrasting piece setups. The internal change called Product and Engineering; the builder-visible handoff added Experience; the adoption, cost, and journey change called all four; and an ambiguous consequence also called the affected roles. Every setup kept Product and Engineering separate, used one Product synthesis, required a named informative run and return, and left inactive roles with evidence but no carrier or contribution prose. A deliberate invalid setup tried to dismiss uncertain shared-cache consequences with Product's opinion. The installed rule stopped at setup, called both affected roles, withdrew the synthesis, and required a new synthesis before Engineering; because no build existed, no later evidence needed invalidation.

**Worst confusion:** the installer printed the source checkout `a737eaa`, while the last product-changing commit was `737959a`. `git diff --exit-code` proved the installed surface identical, so the tester treated this as provenance wording rather than a functional failure and left it for the judge.

**Verdict: SUFFICIENT.** Selective call decisions were understandable and enforceable from the installed product. Live carrier execution remains Piece 9.

### Mid-product upgrader — `/root/piece8_midproduct_upgrader`

**Candidate used:** a disposable clone detached at `737959a`.

**What held:** Real v5.4.1 and exact generated rc.1 repositories crossed to rc.2; rc.1's generated universal paragraph was replaced exactly once; custom Product-team bytes remained an exact prefix beside one generated status; missing `product.md` stayed missing and routed to Shape; dirty state/work hashes survived; retry was byte-stable; printed scoped status and diff exactly matched Git; the first status entry retained both porcelain columns; and a clean current retry said there was nothing to commit before resuming from `state.md`. An adversarial `product.md` directory left a visibly partial method copy but kept the old marker, so retry honesty held while failure presentation remained rough.

**Blocking experience:** after an ordinary supported upgrade, the generated status and `Next:` line require a product-and-current-map assessment but the installed surface never says which record receives the four carrier contributions, where Product writes the synthesis, what explicit edit completes `Unassessed`, or how the existing live piece resumes. The tester ran `rg -n -i 'upgrade status|product-and-current-map|assess the existing product|unassessed|assessment.*(complete|finish|close|record|replace|remove)|clear.*assessment|migration' AGENTS.md .claude/skills templates product.md`; only the generated paragraph was actionable. Leaving it repeats “finish” forever; deleting it silently changes the upgrader to “resume.”

**Verdict: SEND BACK.** Define the assessment record, its required evidence and synthesis, the explicit status transition, and the return to the existing live piece; then rerun this journey.

## Judgment — round 1

**Judge:** `/root/piece8_judge_round1`, disjoint from both testers and every role, builder, prior reader, and auditor.

**Candidate challenged:** product through `737959a`; Built line `946b85a`; receipt `a737eaa`; tester records `5135238`.

**What the judge ran and found:** A disposable supported v5 upgrade reproduced the printed instruction to run the pending product-and-current-map assessment. A search across installed `AGENTS.md`, skills, templates, `product.md`, and `state.md` found no instruction naming its record, Product synthesis, completion edit, or no-reopen resume path beyond the generated status paragraph. The judge then completed an assessment in natural historical prose while retaining the old status as a quote; the installer's raw exact-sentence search still reported the assessment pending. A fresh install from `5135238` and one from `737959a` produced identical installed method bytes apart from the marker while reporting different commit values, so that field identifies the source checkout rather than the last installed-surface change.

**Tester challenges:** The first-time builder's routing evidence held, but their provenance note is material to exact traceability. The mid-product upgrader's send-back held and the historical-quote attack widened it from missing guidance to a brittle status mechanism.

**Rulings:** works — insufficient · delivers the promise — insufficient · good to use — insufficient · quality hangs together — insufficient · sound structure — insufficient.

**Route back:** Piece 8 build. The product promise and two-piece order still hold. Before Engineering edits, Product integrates the delta with Business, Experience, and Engineering because adoption, handoff, trust, migration safety, and provenance changed after those roles had marked their concerns handled. Their old returns and Business ruling describe `737959a`, not the repaired candidate. This first handled-concern miss makes the affected roles mandatory at the next comparable piece's key decisions and runs; Piece 9 already calls both Business and Experience.

**Required fix and re-run:** Name the upgrade assessment record, the four carrier contributions and Product synthesis it receives, the explicit completion status/action, the wrong-promise and wrong-piece/order reopen paths, and the no-reopen return to the existing live piece. Replace the raw paragraph-presence gate with explicit state that quoted history cannot hold open. Report checkout provenance honestly or separately identify installed-surface provenance. After the fix, rerun the mid-product tester's complete supported-upgrade population; their grep must find executable assessment/resume instructions outside the generated status. Rerun the first-time builder's full contrasting routes and uncertainty-stop mutant if any installed always-read page, template, or output changes. Add the judge's skeptical attack: completed natural historical prose that quotes or paraphrases old status must remain complete. Then write a new Built line, open a new receipt, use fresh testers, and re-judge from a fresh context.

**Open items:** assessment completion/resume and provenance return to this Piece 8 fix batch. Live-host affordability remains Piece 9.
