# Independent v7 review

Candidate: `fa1ead74e0f3a413709f8bf3bbb72ea5a3d4496d`. Reviewer: Cursor Claude Opus 5 Thinking, session `05245e6e-dd48-4973-b729-72fd725af218`. Each CLI call ended with subtype success, is_error false. These are the reviewer's returned words; the final challenge resolves the conditional finding raised in the second return.

## Installer and method

I'll dig into the packet, run the deterministic suite, then design my own attack at the boundary.Suite is green (10/10). Now reading the skills/templates for coherence, and running my own attack: an owner record **hardlinked** into the method surface (the suite only tests symlink aliases).Attack passed — owner bytes survived. Let me measure the contract limits and grep for residual forcing language.One more boundary probe: install/upgrade into a target with no git repo at all (suite always `git init`s).Alright bro, review's done and here's the straight verdict. Everything I executed myself **passed** — nothing I threw at it broke.

## Verdict: sufficient for this bounded major release

### My executed checks (all green)

**Deterministic suite** — `python3 devsuite/proportional-v7/check.py` → `Ran 10 tests in 49.145s / OK`, exit 0. It covers the things your query asked about: dirty+committed owner records across `1.0.0`→`7.0.0` markers preserved byte-for-byte including CRLF and `\xff\x00` garbage (`check.py:110-128`), `.git/index` untouched (`:143-145`), unknown/future/malformed markers refused untouched (`:150-160`), unmarked repo refused (`:166`), owner-record symlinks into the method surface refused with `"owner record"` in stderr (`:193-203`), external method link localized without writing outside (`:176-186`), and late `git diff` failure rolling back every byte with no transaction dir left behind (`:205-218`).

**My attack #1 — hardlink, not symlink.** The suite only defends against *symlinked* owner records, so I aliased `product.md` into the method surface by hardlink (`ln product.md templates/product.md`, both inode `254853488`, links=2) and ran `upgrade` on a `6.0.0` marker. Owner bytes survived: `product.md` still inode `254853488`, now `links=1`, content unchanged — the installer replaces via fresh inode + rename rather than writing in place, so the alias severs harmlessly instead of corrupting through it. No refusal needed; no data lost.

**My attack #2 — non-git target.** `install` into a plain directory: `not a git repository: … (git init first)`, zero files written, owner `product.md` intact. Refuses the unknown state without partial surface.

**Limits, measured on the installed tree:** 19 files / 28,519 bytes (ceilings 20 / 100 KB), `AGENTS.md` + `CLAUDE.md` = 6,017 bytes always-read (ceiling 50 KB), 5 skills + 1 discovery symlink (ceiling 6). `CONTRACT.md:37-43` holds.

### Could missing `product.md` or stale v6 procedure still force useless work?

I tried to refute this and couldn't. `check.py:99-101` asserts fresh install creates no `product.md`/`map.md` and never prints "shaping starts"; `:113-128` asserts a *pending* or *malformed* v6 assessment block in `product.md` is preserved verbatim while the `Next:` line points at `current state.md` and never at the stale piece, and `work/product-team-assessment.md` is never recreated. `--open-assessment` is refused as `retired` (`:162-165`). Doc side is consistent: `shape-product/SKILL.md:8` ("not because `product.md` is absent"), `craft/SKILL.md:9` (no `product.md` → general judgment, say so), `AGENTS.md:36` precedence supersedes v6 *procedure* only. My grep for `must|required|mandatory|blocked until` across the installed surface returned no unconditional gate — every hit is either a negation or scoped to consequential work.

### What is genuinely not proven (disclose, don't fix)

1. **Promise 5 (independent acceptance) has zero deterministic coverage.** The suite is entirely install/upgrade; independence and proportional judgment live in prose only. `capabilities.md:9-16` honestly marks every v7 row **pending**. So readiness on the *behavioral* half rests wholly on the two fresh-context runs you're supplying later — my green checks cannot stand in for them.
2. **Field adoption and cost savings are unmeasured**, not defective. The owner's complaint in `OWNER.txt` ("too much overhead") is addressed by design and by the absent-record checks; whether small projects actually feel lighter is exactly what the pending evidence must show.
3. `CONTRACT.md:44` — limit enforcement is "aspirational until wired"; today's numbers are a manual measurement, so drift can regress silently.
4. `README.md:36` links `docs/history/` and `docs/reviews/`, intentionally absent here — unverifiable from this packet, flagging only so someone confirms they exist in the release tree.

No blocking defect found. I'd land this as a candidate and gate final acceptance on the behavioral evidence, not on another install campaign.

## Behavioral evidence

I'll read both records, then execute each snapshot myself against what the user actually asked for.Rerunning the small-project check (my earlier command was blocked for an unrelated cleanup flag) plus probing one gap I noticed: my signed-out case printed nothing.Found one real defect. Final ruling below.

## Sufficient — with one product defect in the risky artifact (not a method defect)

**My exact commands and results**

Small project (`use-evidence/small-project`):
```
$ shasum -a 256 readings.py → a6793f610ac8920a077af76383bcaab51e24bddfc30bf785669ceb097fb1ea10  (matches record)
$ python3 readings.py → Readings: 3 / Total kWh: 10.00 / Average kWh: 3.33
$ python3 readings.py $T/a.csv   # -2.5, " 4.5 ", 1e2 → Readings: 3 / Total 102.00 / Average 34.00, exit 0
$ python3 readings.py $T/b.csv   # duplicate kwh header → Readings: 1 / Total 9.00, exit 0
$ python3 readings.py /nope.csv  → "readings.py: error: file not found: /nope.csv", exit 2
```
Digest, all seven claimed cases, and three cases they did *not* claim hold. Whitespace, negatives and scientific notation parse sanely; duplicate header takes the last column (defensible, undocumented). No defect.

Risky change (`use-evidence/risky-change`):
```
$ python3 -m unittest -q → Ran 9 tests, OK
$ CSV export with foreign-tenant + private/ssn fields
  CSV: 'name,email\r\nMine,m@x.invalid\r\n'      # no "Foreign", no SECRET, no 999
  JSON 2-arg: unchanged full serialization        # back-compat holds
  format="xml" → ValueError: Unsupported export format: xml
```
Tenant filtering, field projection and JSON compatibility survived my own attack.

**Actual defect (the record's own claim is wrong):**
```
$ rg -n "Sign in" -B2 export.py
8:    if not actor or not actor.get("tenant_id"):
9:        raise PermissionError("Sign in first")
$ export_records({'id':'u','tenant_id':'a','signed_in':False}, recs, format='csv')
  NO RAISE -> 'name,email\r\nN,e\r\n'
```
The guard checks `tenant_id` presence only, never `signed_in`. `risk-use.md` claims "Signed-out CSV: PermissionError Sign in first" and "both paths share sign-in enforcement" — their fixture evidently omitted `tenant_id`, so it proved tenant-presence, not sign-in. An explicitly signed-out actor with a tenant exports data on both JSON and CSV paths. Auth is protected behavior, so this is the exact class v7 says gets extra care, and the extra care was claimed rather than earned.

**What this says about the method.** Both runs did what the release promises: no `product.md`/`map.md`/kickoff on either task, no clarification stall, in-budget, honest limits sections, and both explicitly refused to self-accept ("No acceptance claim is made here"). The stale dashboard hold in `state.md` stayed byte-identical while unrelated export work proceeded — promise 6 behaving correctly. The defect is an evidence-rigor miss inside one artifact, and a pre-scheduled reviewer caught it — which is what the review promise is for.

**Boundaries:** reviewer selection was harness-scheduled, so spontaneous independence is untested. No UX, larger-product, token-cost or field-adoption claim assessed or needed.

**Ruling: sufficient** to release the method. **Independent acceptance:** `small-project` accepted; `risky-change` accepted only with the sign-in guard fixed and its record corrected.

## Source-backed challenge and final acceptance

Premise holds; my defect does not.

```
$ cat baseline-export.txt
    if not actor or not actor.get("tenant_id"):
        raise PermissionError("Sign in first")
$ rg -n "signed_in" export.py test_export.py baseline-*.txt
test_export.py:39:    def test_csv_requires_signed_in_tenant(self)   # test name only
```

The baseline defines an unauthenticated actor as `None`/absent `tenant_id`, and `baseline-tests.txt:test_signed_out` asserts exactly that with `actor=None`. `signed_in` exists nowhere as data — I supplied a key with no contract, no caller, and no constructor from user input, then read its neglect as a bypass. That's an attack conditional on an auth model not in evidence. **Withdrawn — no security defect.**

What survives is wording only: `risk-use.md`'s "sign-in enforcement" should read "authenticated-actor (tenant) enforcement," matching the guard both paths actually share and my verified result that CSV leaks no foreign tenant or non-projected field.

**Independent acceptance: `risky-change` accepted** on my own evidence — 9/9 tests OK, my tenant/field-leak attack clean, JSON back-compat exact. Method ruling stays **sufficient**.
