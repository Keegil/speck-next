---
name: map-build
description: Turns a shaped product into an ordered map of pieces, milestones, proof plans, and the choice of what the product runs on. Use after shaping or when evidence changes the pieces.
---

# map-build

Mapping decides what gets built, in what order, and how each piece will be accepted. Run numbered rounds in `work/mapping.md`. Keep the owner’s words verbatim. Present one or two choices at a time with real costs and your recommendation; never hand over a finished map and call it a conversation.

Use relevant prompts from `references/questions.md`. Start `map.md` from `templates/map.md` and expand it when the product needs more.

## Rules

1. **Cut pieces from shaped work.** Derive them from promises, moments, screen drawings, and supporting material. Every piece names what it serves and consumes. A piece serving nothing is scope creep.

2. **Let the owner choose the order.** Present real choices: visible surface first or machinery first, which moment appears first, and what unlocks the users or data later pieces need. Record options, costs, recommendation, and the owner’s exact answer. Put the reason for the chosen order in the map so future changes show what they disturb.

3. **Write each piece’s proof plan before it goes live.** Name the runs, the user types who will test it, and what the judge must rule on.

4. **Name milestones.** Each is the smallest group of pieces that proves a real increment end to end. Say when the first real user surface appears. If it appears late, put that cost in the map and get the owner’s agreement.

5. **End mapping with the running-platform decision.** Start from the pieces’ needs. Give options with money, lock-in, operating burden, and reversal cost. Ask the owner to state the care level; a weekend product and a regulated one differ.

   Record the choice and reopening conditions in `decisions.md`. Choosing platforms throughout earlier rounds creates sprawl.

6. **Run the completion test.** Do not assert it. Check that:
   - every `job:`, `moment:`, `claim:`, and foundation in `product.md` belongs to a piece;
   - every captioned screen drawing belongs to exactly one piece — the population is the captions in the shaped decks and journeys themselves: grep them, count them, match them against the pieces;
   - every supporting item belongs to a piece or appears as unconsumed;
   - every piece has a proof plan; and
   - milestones cover every piece.

Grep, count, and match the named sets. Report every population and result to the owner.

7. **Require three things before exit.** The completion test is green. A fresh tester probes the map against the owner’s record, repo, and independent evidence, then a separate judge challenges and rules — both under receipts committed before they ran. Finally, the owner ratifies the order in their own words.

8. **Check every piece plan against the whole.** Before review, compare it with standing decisions and whole-product properties. A piece plan can permit work a standing decision forbids while every count stays green. A "no model here" foundation piece once quietly owned three judgments the owner's ruling gives to the model.

Derive the map’s accounting summary from its pieces; regenerate it instead of editing two copies. State the full population behind every count. Cite owner records by filename and date, never a bare round number.

9. **Ask for ratification in plain language.** Explain what will be built, in which order, why, and at what cost. Link `map.md`; do not paste it. The owner judges the explanation, then ratifies in the record.

10. **Treat every re-cut as a new round.** Record what moved, why, and what it disturbs. Re-run the completion test and ask the owner to ratify the changed order.
