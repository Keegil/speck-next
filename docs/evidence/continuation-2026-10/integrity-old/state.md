# Packing-list continuation

**Status:** Data-loss repair done (unreviewed).

`pack.py` no longer treats invalid JSON as an empty list on `add` or `mark`.
Those commands print a clear error to stderr, exit non-zero, and leave
`items.json` bytes unchanged. `list` reports invalid JSON instead of an
empty list. After the person fixes the file, `add`/`mark`/`list` behave
as before.

**Verified:** Damaged `[{"name": "Toothbrush"` → `add Socks` fails (exit 1),
file unchanged; valid JSON → `add Socks` succeeds.

**Still open (out of scope):** Display heading missing colon; filtered-number
interaction bug.

**Next command:** `python3 pack.py list --pending` on the restored
`items.json` in this checkout.

Owner privacy and data-preservation constraints are in product.md.
