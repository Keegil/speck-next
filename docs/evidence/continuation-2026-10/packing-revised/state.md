# Packing-list continuation

**Goal:** Complete trip-preparation job — list pending, mark by displayed number,
reopen pending and see only what remains.

**Verified (this session):** `mark` indexes the pending-visible list (not raw
`items.json` position). List heading is `Packing list:`.

**Quick check:**
```bash
python3 pack.py list --pending | head -1   # → Packing list:
python3 pack.py list --pending
python3 pack.py mark 1
python3 pack.py list --pending               # packed row gone; numbers restart at 1
```

**Data:** `items.json` may differ after checks; Passport/Charger pending baseline
in handoff had Toothbrush already packed.

Owner constraints in `product.md` unchanged. No commits in this repair.
