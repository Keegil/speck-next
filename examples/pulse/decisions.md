# Decisions

**Storage: one human-readable JSON file with a write lock** (over sqlite, or one file per day). Zero setup and you can read your own journal in any editor; the lock plus write-then-rename covers the two real loss risks (overlapping runs, crash mid-write). Reopens if multi-device sync ever becomes real — a single file merges badly.
