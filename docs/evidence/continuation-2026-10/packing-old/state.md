# Packing-list handoff

Trip-preparation job verified end-to-end on this checkout.

**Fixes in `pack.py`:** pending heading is `Packing list:`; `mark N` targets the
Nth row of the pending list (not raw `items.json` index).

**Verify (fresh pending work):** reset or use items with mixed packed/pending, then:

```bash
python3 pack.py list --pending | head -1    # expect: Packing list:
python3 pack.py list --pending              # numbered pending rows only
python3 pack.py mark 1                      # packs current #1
python3 pack.py list --pending              # #1 gone; rest renumbered
```

**Data after last run:** Toothbrush and Passport packed; Charger pending.

Owner constraints unchanged in `product.md`. No new dependencies or network.
