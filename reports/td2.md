# TD 2 report — The quorum, then the routing rule

Sub-group 1. Session of 18 November 2026. Course pack `2026-11-18-students-5` (code identical to the TD 1 kit; documents updated). No new network call: everything below uses the stored TD 1 traces.

Members (GitHub accounts): Manal Hassan (manalhdev), axel12334556, ines729, Marieseka, TasB (TazBrks), Daiki4529, lorentejla.

## 1. What we attempted and completed

| Step | Pair | Deliverable | Status |
|---|---|---|---|
| 1. k-of-n vote, 2-of-3 against 3-of-5 | A | `vote_k_sur_n` in `skeleton-multi-llm-en.py`, twenty-question table | to be completed by Pair A |
| 2. Wrong consensus | B | case, SQL root cause, delta query on `data/boutique.sqlite` | to be completed by Pair B |
| 3. Routing rule | C | [td2/routing-rule.md](../td2/routing-rule.md), rates, simulator before and after | done |

## 2. Step 1 — The vote (Pair A)

To be completed by Pair A.

## 3. Step 2 — The wrong consensus (Pair B)

To be completed by Pair B.

## 4. Step 3 — The routing rule (Pair C)

- TD 1 rates per family: [results/family-rates-td2.md](../results/family-rates-td2.md) (`python3 tools/td2_family_rates.py`).
- The one-page rule, the scenario table R1 to R5, the changes made to the simulator and the analysis of the priority order of `choose`: [td2/routing-rule.md](../td2/routing-rule.md).
- Simulator outputs: before adaptation [results/routing-before.txt](../results/routing-before.txt), after [results/routing-after.txt](../results/routing-after.txt) (`python3 atelier-routage.py`).

Main findings:

- Period (F1) and product (F3) questions: four or five models are at 100 % in TD 1, so gpt-oss-20b goes first and a dashboard needs no check.
- Every question with an age at a reference date (8 cells): only gpt-oss-120b is at 100 % (8/8); gpt-oss-20b fails C02 with a silent wrong value, Qwen, Cohere and Dots fail 4, 7 and 6 of them.
- The 2-of-3 panel is not enough on the age families: on C09, two panel members (Cohere and Qwen) returned the same wrong value 0. Customer figures on these families use a 3-of-5 quorum, payouts a reference query and a human review.

Limits: twenty questions and one run per cell; some families have one or two cells only (F2b: C10, C18), so their rates are weak evidence. Resource availability and refill times in the simulator are scenario assumptions, not measurements. The paid cost uses the portfolio price of 2026-09-29 and the TD 1 median tokens.

## 5. Division of work

| Pair | Members | Step |
|---|---|---|
| A | to be completed | 1 |
| B | to be completed | 2 |
| C | Manal Hassan, to be completed | 3 |

AI-assisted code and its prompts: [prompts-ai-assistance.md](../prompts-ai-assistance.md).

## 6. Next steps

To be completed at the cross-review.
