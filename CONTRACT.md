# speck-next · Product contract

Version **v7**. These are outcome-level promises for the installed kernel. Checks in `devsuite/` and fresh review earn or break them; this file does not embed installer parser rules (those live in the package the upgrader ships).

## The job

Help an agent build products **proportionally**: right-sized clarification, planning, records, expertise, verification, and review for each request — from a one-line fix to a multi-month product — without turning every task into a methodology campaign.

## The eight promises

1. **Proportional entry** — Work starts at actual scope. Missing templates or phases never block ordinary questions, analysis, or small builds. *Fails if* agents refuse work solely because `product.md` or `map.md` is absent.

2. **Earliest honest result** — Default is understand enough, then run the smallest useful slice on the real surface (or real dependency) before paperwork expands. *Fails if* planning routinely exceeds building without owner direction.

3. **Owner holds consequential choices** — Product direction, architecture forks, and care-level tradeoffs reach the owner with one recommendation and what each option changes for users. *Fails if* agents hide material choices or re-debate settled decisions.

4. **Real use, honest evidence** — Claims cite what was run, seen, or measured. Harness-only proof does not substitute for the product surface the user gets. *Fails if* reviewable work ships on author testimony alone for substantive changes.

5. **Independent acceptance for substantive deliverables** — Non-contributors review material changes; the same fresh context may exercise and judge when adequate. *Fails if* builders grade their own substantive work without disclosure, or invent independence.

6. **Complete-job integrity** — A concrete integrated failure blocks dependent work until fixed and the affected sequence is re-run; unrelated work may continue. *Fails if* known broken user jobs are built upon without repair.

7. **Risk-scoped protection** — Auth, money, privacy, data integrity, regulation, and irreversibility get applicable least privilege, integrity checks, stand-ins, and rollback evidence on **affected** behavior. *Fails if* "small change" waives required protections.

8. **Small kernel, honest upgrade** — Installed method stays within published size/skill limits; upgrade preserves owner records and refuses unsafe trees; old-Speck conversion remains out of scope until explicitly shipped. *Fails if* install/upgrade corrupts owner bytes or claims unsupported conversion.

## What we refuse to trade away

Fresh independent review for substantive results (scaled, not roster-fixed). Owner control of consequential choices. Repair-and-re-run for concrete integrated failures. Applicable protections on high-consequence behavior. Preservation of owner product records on supported upgrade paths.

## What stays out

Mandatory phase ratification chains; universal four-role ceremonies; fixed minimum testers/judges; token accounting as quality gates; old-Speck markerless conversion (not implemented).

## Until it earns the job

| Limit | Ceiling | Notes |
|---|---|---|
| Installed files | ≤ 20 regular files / 100 KB | Includes the marker; the directory discovery symlink is reported separately. Owner files are not method files. |
| Skills | ≤ 6 | Count actual skill entrypoints; a discovery alias is not another skill. |
| Repository context | `AGENTS.md` + relevant repo context | ≤ 50 KB combined read budget; select further detail for the task rather than loading every record. |
| Method file per piece | ≤ 1 when used | Zero for trivial fixes |

`devsuite/surface-check.py` checks the installed file, byte, and skill ceilings, release versions, metadata, links, and both host entrypoints. The default suite and GitHub Actions run it with negative controls. The combined agent/context budget and whether a work record earns its keep still require judgment; these are not mechanically verified by file counts.

Historical v6 contract text and assessment-parser specification are retired from user-loaded docs; prior proof rows in `capabilities.md` are historical unless marked refreshed for v7.

## Optional toolkit (v7.1)

Graft, ripgrep, jq, ast-grep and RTK are available through an explicit toolkit setup. The method-file ceilings above cover the installed instructions and templates; optional third-party binaries, dependencies and generated indexes have a separate, visible disk footprint. Core install and upgrade remain dependency-free and do not require toolkit setup.

The toolkit pins upstream artifacts and verifies their checksums before installation. It owns its cache, preserves existing installations and project records, and reports failures without claiming setup completed. Its launcher propagates child exit status. Setup does not install global hooks or enable model calls. Tool-generated summaries and graphs support navigation; original output, source and appropriate checks establish consequential claims. Token and latency benefits require comparisons on actual tasks.
