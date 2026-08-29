---
name: shape-product
description: Turns a product idea into product.md through an owner conversation. Use when product.md is missing or a bet changes what the product promises.
---

# shape-product

Shape the product in conversation. Ask one or two useful questions at a time. Keep numbered rounds in `work/shaping.md`, starting from `templates/rounds.md`, and quote the owner verbatim. Fill what is known, offer defaults for the rest, and mark honest unknowns.

Use the relevant prompts in `references/questions.md`; this is not a questionnaire. Create any supporting material the product needs, such as a domain model, journey, or deck. State each item’s purpose in the record so the map can assign it to a piece.

Start `product.md` from `templates/product.md`. The template is a floor. Add sections and supporting material whenever the product needs them.

Keep shaping while open product questions need real evidence, and let the first increment gather it through runs, probes, or measurements. If no open shaping question remains, move on. Shaping with nothing running kills products on paper; shaping after the questions close only delays the build.

Shaping ends when `product.md` meets its template, a fresh tester has probed it and a separate judge has ruled — both with receipts committed before they ran — and the owner has ratified it in the record. Then use `map-build`.

## Rules

1. **Start with the outcome.** The first line says what the user gets. If the conversation begins with features, return to what the person is trying to achieve and reason from first principles.

2. **Make convention earn its place.** Find the category’s fossils: structures inherited from paper, physical limits, or software that could not think. Use the best human doing this job as the bar. Question the category’s assumed concepts and rebuild from the job, the domain, and the user’s mental model.

   Not every product should reinvent its category, but write down why a convention serves this job. If reinvention is the answer, unplug the model: if the product still basically works, its intelligence is decoration.

3. **Make every differentiator real.** Anything claimed as special must run on the shipped path with the real model and real data. A canned substitute breaks the promise; it is not a harmless stub.

4. **Give every magic moment a test.** Name the moment, its trigger and beats, the feeling it should create, and the exact scenario that will prove it. Do this before building.

5. **Earn the price.** Before writing a price, answer what free general AI, a spreadsheet, or a competitor’s free tier gives this person, and why they would still pay.

6. **Protect what only the whole can carry.** Put properties such as “the AI does the work,” “calm,” and “never fabricates” in `product.md`. Every consequential decision states its effect on each. Only the owner may knowingly trade one away.

7. **Decide by cutting.** Use one sentence per claim. Give every promise, job, and moment a short stable name, such as `moment: first-paste`, so later work can point to it. Omit sections that do not apply.

8. **Obey the product’s own language rules.** If `product.md` bans words from the user experience, the file itself and everything the owner reads must avoid them.

9. **Give foundations triggers.** Name predictable structural work, such as the design system, data model, auth and tenancy, CI, and real infrastructure. State when each becomes due. A fired trigger makes that foundation the next piece.

   Building every foundation from guesses and never building one are both failure modes.

10. **Keep the owner’s words exact.** `work/shaping.md` is an append-only record of the conversation. Later rounds may replace earlier answers; settled choices live in `product.md` and `decisions.md`.

   Reviews compare the product with what the owner actually said, not with sibling documents. Never present a paraphrase as the owner’s quote. That is fabricated evidence.

11. **Test drawings before asking the owner to judge them.** Check every journey, deck, and screen drawing against the domain model, repo, fixtures, or real behavior. Ask whether the evidence behind each element exists. Before any substantial shaping material reaches the owner, a fresh tester probes it against independent evidence with the `experience` skill, and a separate `judge` challenges the verdict and rules.
