# v6.0.0 second-host experience — Claude builder

## Run identity

- Persona: builder using the supported second host/repository, Claude.
- Freshness: I contributed to none of the design, code, product-team roles, tests, or judgments, and I did not read prior role conclusions.
- Source candidate: `c2912e738c57218d23b574e5684c3aad026d2c07` (`c2912e7`).
- Built commit: `fff561e7da52c4cec0e385b10b0ba7bc061a585b`.
- Receipt commit: `9e8145621e36bff0a5361c1447ff857caf4ddca5`.
- Run date: 2026-09-06, Europe/Oslo.
- Disposable subject: `/tmp/speck-v6-second-host.wdza24/product`; the host was invoked from `/tmp/speck-v6-second-host.wdza24/product/deep/nested`.
- Authorization used: exactly one Claude terminal invocation, 38.81 seconds wall time, no retry, no fallback, and no owner interruption. The host itself reported `num_turns: 8`; this record therefore distinguishes the single terminal invocation from its eight internal host turns.

## Exact candidate, pack, and install

Commands:

```sh
TEST_ROOT=$(mktemp -d /tmp/speck-v6-second-host.XXXXXX)
git clone --no-local --quiet /Users/kjetil/Code/speck-next "$TEST_ROOT/candidate"
git -C "$TEST_ROOT/candidate" -c advice.detachedHead=false switch --detach c2912e7
git -C "$TEST_ROOT/candidate" rev-parse HEAD
PACK_NAME=$(cd "$TEST_ROOT/candidate" && npm pack --silent)
PACK_PATH="$TEST_ROOT/candidate/$PACK_NAME"
mkdir -p "$TEST_ROOT/product/deep/nested"
git -C "$TEST_ROOT/product" init --quiet
npm exec --yes --package="$PACK_PATH" -- speck-next install "$TEST_ROOT/product"
```

Output:

```text
HEAD is now at c2912e7 State v6.0.0 status truthfully
c2912e738c57218d23b574e5684c3aad026d2c07
PACK_NAME=speck-next-6.0.0.tgz
Installed Speck Next 6.0.0 (source checkout not recorded; method surface sha256:1ccba108dcc2eb6f1e15812e53e8e243ee09ee586d69f7b45ac7dad472872d70) into /tmp/speck-v6-second-host.wdza24/product — 20 installed or carried-forward files on disk.
Installed paths:
.agents/skills/speck-next
.claude/skills/craft/SKILL.md
.claude/skills/experience/SKILL.md
.claude/skills/experience/references/walk.md
.claude/skills/experience/references/worst-day.md
.claude/skills/judge/SKILL.md
.claude/skills/map-build/SKILL.md
.claude/skills/map-build/references/questions.md
.claude/skills/shape-product/SKILL.md
.claude/skills/shape-product/references/questions.md
.claude/speck-next.json
AGENTS.md
CLAUDE.md
map.md
templates/decisions.md
templates/map.md
templates/piece.md
templates/product.md
templates/rounds.md
templates/state.md
Next: open an agent session there and say what you want to build — shaping starts in that conversation.
```

Observation: the tarball was packed from the detached exact candidate, and its npm binary installed cleanly into a separate initialized Git repository. The tarball has no Git metadata, so the installer truthfully recorded `sourceCheckout: null`; candidate identity comes from the preceding `rev-parse`, while copied method identity comes from the digest below.

## Installed surface verification

Commands:

```sh
cd /tmp/speck-v6-second-host.wdza24/product
cat .claude/speck-next.json
find .claude/skills -name SKILL.md -type f -print | LC_ALL=C sort
readlink .agents/skills/speck-next
realpath .agents/skills/speck-next
realpath .claude/skills
cmp .agents/skills/speck-next/shape-product/SKILL.md .claude/skills/shape-product/SKILL.md
node -e 'const fs=require("fs"),path=require("path"),crypto=require("crypto"); const root=process.cwd(), surface=["AGENTS.md","CLAUDE.md",path.join(".claude","skills"),"templates"], files=[]; function visit(rel){const abs=path.join(root,rel),st=fs.statSync(abs); if(st.isDirectory()) for(const n of fs.readdirSync(abs).sort()) visit(path.join(rel,n)); else files.push(rel)}; for(const item of surface) visit(item); files.sort(); const h=crypto.createHash("sha256"); for(const rel of files){h.update(rel.split(path.sep).join("/"));h.update("\0");h.update(fs.readFileSync(path.join(root,rel)));h.update("\0")} console.log(`recomputed_method_surface_sha256=${h.digest("hex")}`); console.log(`method_manifest_files=${files.length}`);'
```

Output:

```text
{
  "name": "speck-next",
  "version": "6.0.0",
  "sourceCheckout": null,
  "methodSurfaceSha256": "1ccba108dcc2eb6f1e15812e53e8e243ee09ee586d69f7b45ac7dad472872d70",
  "upgradeAssessmentRecord": null,
  "installedAt": "2026-09-05T22:40:09.735Z"
}
.claude/skills/craft/SKILL.md
.claude/skills/experience/SKILL.md
.claude/skills/judge/SKILL.md
.claude/skills/map-build/SKILL.md
.claude/skills/shape-product/SKILL.md
../../.claude/skills
/private/tmp/speck-v6-second-host.wdza24/product/.claude/skills
/private/tmp/speck-v6-second-host.wdza24/product/.claude/skills
adapter_shape_body_cmp=identical
recomputed_method_surface_sha256=1ccba108dcc2eb6f1e15812e53e8e243ee09ee586d69f7b45ac7dad472872d70
method_manifest_files=17
```

Observation: the marker says 6.0.0; the independently recomputed method digest exactly matches it; five canonical skills exist; and `.agents/skills/speck-next` is a relative symbolic link resolving to the same canonical `.claude/skills` directory rather than another copy.

## Cold read of the installed method

Commands and output:

```text
$ wc -l AGENTS.md CLAUDE.md
     172 AGENTS.md
       1 CLAUDE.md
     173 total
$ cat CLAUDE.md
@AGENTS.md
$ sed -n '1,420p' AGENTS.md
[all 172 lines read]
```

As a builder, I could act after one read. The opening names the five phases and the owner relationship; “Know where to start” says that no ratified `product.md` means `shape-product`; and the fresh install contains no competing setup path. The dense “Finish an upgrade” parser rules are a real cold-read slowdown in a fresh repository, but they do not obscure the top-level start instruction. I had not manually read `shape-product/SKILL.md` at this point.

## One Claude invocation from the nested directory

Command:

```sh
cd /tmp/speck-v6-second-host.wdza24/product/deep/nested
pwd
git rev-parse --show-toplevel
command -v claude
/usr/bin/time -p perl -e 'alarm 180; exec @ARGV' claude -p --output-format json --dangerously-skip-permissions '/shape-product'
```

Output:

```text
/tmp/speck-v6-second-host.wdza24/product/deep/nested
/private/tmp/speck-v6-second-host.wdza24/product
/Users/kjetil/.npm-global/bin/claude
{"type":"result","subtype":"success","is_error":false,"api_error_status":null,"duration_ms":35588,"duration_api_ms":34898,"ttft_ms":2188,"num_turns":8,"result":"**Phase:** Shape · **Round:** none yet · **Since last session:** nothing — no `product.md`, no `work/shaping.md`, `map.md` is empty. This is a fresh product.\n\nBefore I open Round 1 in `work/shaping.md`, I need the seed. `/shape-product` starts from an idea — what someone gets from the product, or at minimum a bet you want to test. I don't have that yet, and I won't guess one.\n\nWhat are we shaping? A one-liner is enough — I'll push on outcome, category fossils, and who it serves from there.","stop_reason":"end_turn","session_id":"143db3bc-2866-4dd5-b9f3-75ec1c287d43","total_cost_usd":0.6265625000000001,"usage":{"input_tokens":15,"cache_creation_input_tokens":64104,"cache_read_input_tokens":352425,"output_tokens":1985,"server_tool_use":{"web_search_requests":0,"web_fetch_requests":0},"service_tier":"standard","cache_creation":{"ephemeral_1h_input_tokens":64104,"ephemeral_5m_input_tokens":0},"inference_geo":"","iterations":[{"input_tokens":1,"output_tokens":827,"cache_read_input_tokens":63572,"cache_creation_input_tokens":532,"cache_creation":{"ephemeral_5m_input_tokens":0,"ephemeral_1h_input_tokens":532},"type":"message"}],"speed":"standard"},"modelUsage":{"claude-opus-4-7[1m]":{"inputTokens":15,"outputTokens":1985,"cacheReadInputTokens":352425,"cacheCreationInputTokens":64104,"webSearchRequests":0,"costUSD":0.6265625000000001,"contextWindow":1000000,"maxOutputTokens":64000}},"permission_denials":[],"terminal_reason":"completed","fast_mode_state":"off","uuid":"66dc6ec7-27e8-40c6-8e2d-7c23d453dcfc"}
real 38.81
user 5.23
sys 1.89
```

Host-reported identity and cost evidence only:

- CLI version: not reported; only the executable path was reported by `command -v`.
- Model: `claude-opus-4-7[1m]`.
- Session: `143db3bc-2866-4dd5-b9f3-75ec1c287d43`.
- Usage: 15 input, 1,985 output, 352,425 cache-read, and 64,104 cache-creation tokens; USD 0.6265625. The host also reported eight internal turns.

After that invocation, I read the installed canonical `shape-product/SKILL.md` and its referenced questions. The body says to shape in conversation, ask one or two useful questions at a time, start with the outcome, preserve unknowns honestly, and use `shape-product` when `product.md` is missing. The returned opening matches those behaviors: it identified the fresh state, asked one outcome-seeking seed question, refused to guess a product, and stopped before creating Round 1. It also obeyed the installed page’s required first-line phase/status handoff. “Category fossils” is a small method-language leak in an otherwise plain owner-facing opening; I understood it, but plain wording would be better.

Post-host command and output:

```text
$ test ! -e product.md && test ! -e state.md && test ! -e work && printf 'post_host_product_artifacts=none\n'
post_host_product_artifacts=none
$ git status --short
?? .agents/
?? .claude/
?? AGENTS.md
?? CLAUDE.md
?? map.md
?? templates/
```

The host did not build or rebuild a synthetic product and did not create shaping work.

## Model-free skeptical topology attack

From the nested directory, I tried to falsify the same-body claim by searching for physical skill files under `.agents`, following the adapter separately, resolving both destinations, and comparing the device/inode of one body.

Commands:

```sh
PRODUCT_ROOT=$(git rev-parse --show-toplevel)
ADAPTER="$PRODUCT_ROOT/.agents/skills/speck-next"
CANONICAL="$PRODUCT_ROOT/.claude/skills"
find "$PRODUCT_ROOT/.agents/skills" -type f -name SKILL.md
find -L "$ADAPTER" -type f -name SKILL.md
realpath "$ADAPTER"
realpath "$CANONICAL"
stat -f 'dev:%d inode:%i' "$ADAPTER/shape-product/SKILL.md"
stat -f 'dev:%d inode:%i' "$CANONICAL/shape-product/SKILL.md"
```

Output:

```text
physical_skill_bodies_under_agents=0
reachable_skill_bodies_through_adapter=5
adapter_real=/private/tmp/speck-v6-second-host.wdza24/product/.claude/skills
canonical_real=/private/tmp/speck-v6-second-host.wdza24/product/.claude/skills
adapter_shape_stat=dev:16777231 inode:234026635
canonical_shape_stat=dev:16777231 inode:234026635
skeptical_attack_result=held
```

The attack held: no regular skill body exists under `.agents`; following the adapter reaches five bodies; both paths resolve inside the selected product to the same directory; and the sampled skill is the same filesystem object.

## Unsupported claims and limits

- This run proves one fresh install and the first Shape opening on Claude, not a complete shaping conversation, product build, later phase, upgrade, or repeat invocation.
- The host did not report its CLI version, so none is inferred.
- The marker cannot itself prove `c2912e7` because a packed tarball records no source checkout. The detached clone’s `rev-parse` proves what was packed, and the recomputed digest proves the installed method bytes match the tarball.
- The actual Claude invocation proves nested-directory discovery for this physical path. The model-free attack proves link containment and non-duplication, not Claude behavior under every symlinked or non-Git path.
- Usage is cost evidence only; it neither supplies nor erases the observed product result.

## Verdict — Claude-side builder

**Works:** Yes. I installed the exact v6.0.0 tarball, verified its version, digest, five skills, and shared-body adapter, then invoked `/shape-product` once from two directories below the root. Claude found the method, named the correct fresh state, asked for the missing outcome seed, and made no product changes.

**Keep:** Yes. I would keep this installed in a product repository because the start path is discoverable and the first response keeps me in control instead of fabricating a product. I would trim the fresh-reader burden of the upgrade parser detail and replace “category fossils” in the owner-facing opening when the next method revision has a justified reason to touch those words.

**Deal-breaker:** None observed in this run. A future Claude invocation failing to discover the root from an ordinary nested directory, duplicating host-specific skill bodies, or starting product work before the owner supplies the seed would break the deal; none happened here.
