# The method ships in the form agents actually load

**Outcome:** an agent opening this repository is governed by Speck Next without being told to read anything — the method page is `AGENTS.md` (which every agent host loads on its own; Claude Code via `CLAUDE.md`), on-demand procedure is a real skill (`.claude/skills/independent-review/`), and this repository runs under its own method: product, work files, decisions, and state at root. `kernel/doctrine.md` — a page no host would ever load — is gone.

**How I'll know it works:** the files sit at the exact paths the hosts read (verifiable now), and the next fresh agent session in this repo starts already governed — follows the loop, uses the skill, speaks product — without being pointed at any file (verifiable only next session; open until then).

**Open:** next-session verification. The installer that places `AGENTS.md` into product repos doesn't exist yet — that's the upgrader's work, a separate piece.
