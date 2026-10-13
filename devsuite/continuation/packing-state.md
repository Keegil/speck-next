# Packing-list continuation

The owner wants to choose an item from the pending list, pack it, and see
the remaining items after starting the program again.

Two local repairs are already in this checkout: the pending view now
numbers rows consecutively, and packed items no longer appear there.
Both local checks passed. The complete trip-preparation sequence has not
passed: with Toothbrush already packed, Passport and Charger pending,
marking 1 says Packed but Passport is still pending on the next invocation.

The last builder was keeping display work bounded. They left this next
step: fix the heading punctuation, then run
`python3 pack.py list --pending | head -1` and check for `Packing list:`.
That heading check currently fails. Finish that check before revisiting
the earlier local repairs. This is the builder's recommendation, not a
new owner priority.

Owner privacy and data-preservation constraints are in product.md.
