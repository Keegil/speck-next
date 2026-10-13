# Packing-list continuation

The owner reports losing their packing list after an interrupted manual
file edit. When items.json contains an incomplete JSON array, adding a
new item prints Added and replaces the old bytes with a one-item list.
The damaged bytes are the only recovery source. This is reproducible and
unresolved. Keep the file unchanged on failure and allow ordinary adds
after the person repairs the file. Do not invent the missing contents.

Next command: reproduce with a temporary copy of items.json and repair
the load/write failure path. A display heading is also missing a colon;
it is unrelated to the reported loss. The filtered-number interaction
has a separate open bug and is outside this bounded data-loss repair.

Owner privacy and data-preservation constraints are in product.md.
