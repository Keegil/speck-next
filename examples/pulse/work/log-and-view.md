# Log and view

**Outcome:** `pulse 4` records today's energy as 4. `pulse` prints the last 14 days — logged days as bars, skipped days as gaps. Works from an empty start.

**How I'll know it works:** run it — log a value, view the chart, re-log the same day (last write wins), try nonsense input (clear error, nothing stored), view with nothing logged (friendly, not broken), and confirm a skipped day shows as a gap. The never-lose-a-day promise gets checked by breaking the storage on purpose once and watching the guard complain.

**Status:** see [state.md](../state.md).
