# Packing-list continuation

**Status:** Data-loss on damaged `items.json` is fixed in `pack.py` (unreviewed).

**Verified:** Incomplete JSON + `add` exits 1, stderr explains repair, file bytes
unchanged (no `Added`). Valid JSON + `add`/`list`/`mark` behave as before.

**Change:** `JSONDecodeError` no longer becomes `[]`; all commands refuse to run
until the file parses, so nothing overwrites damaged bytes.

**Still open (out of scope):** list heading missing colon; filtered-number `mark`
bug per prior handoff.

**Next command:** Optional — fix heading colon or the pending-filter mark bug if
the owner wants those in a separate slice.

Owner privacy and data-preservation constraints remain in `product.md`.
