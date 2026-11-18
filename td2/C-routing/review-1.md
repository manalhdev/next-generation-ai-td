# Cross-review of Pair C by Pair A

Written by Tasnim (TasB) on behalf of Pair A (Jonas, Axel), 18 November 2026: Axel became unavailable during the session. The checks were run with Claude ([prompts-ai-assistance.md](../../prompts-ai-assistance.md)), from the repository root, at commit 6762a79. Pair A may confirm or amend these checks.

Reviewed: [routing-rule.md](routing-rule.md), [family_rates.py](family_rates.py), [analyse_votes.py](analyse_votes.py), and `RESOURCES` and `choose` in [atelier-routage.py](../../atelier-routage.py).

## Checks run (from the repository root)

- [x] **`python3 td2/C-routing/family_rates.py`: each rate quoted in `routing-rule.md` matches `family-rates-td2.md`.** The file regenerates with no change (`git status` clean). F1 6/6, 6/6, 5/6 (Qwen C06), 6/6, 6/6. F3 4/4 for the five models. Age at a reference date (C02, C08, C09, C11, C15, C16, C17, C19): 120B 8/8, 20B 7/8, Qwen 4/8, Cohere 1/8, Dots 2/8. F2b (C10, C18): 2/2, 2/2, 1/2, 1/2, 1/2. These are the rates quoted in the rule.
- [x] **`python3 atelier-routage.py`: the output equals `routing-after.txt` and each reason cites TD 1 cells.** `diff` empty. Every `run`, `defer` and `abstain` reason names the model, its TD 1 ratio and the cells of the family.
- [x] **The checks chosen for the age families use the result of Step 1.** Step 1 shows that the 2-of-3 panel keeps the wrong value 0 on C09, while the 3-of-5 quorum abstains, and that 3-of-5 adds no wrong consensus on the batch (15 right, 0 wrong, 5 abstentions). The rule uses exactly this: a 3-of-5 quorum with abstention sent to human review for a customer figure on F2 and F2b, and the 2-of-3 panel only on F1 and F3, where the panel made no silent error. `checks_for` in the code applies the same split.
- [x] **`python3 td2/C-routing/analyse_votes.py`: the twenty decisions are those of our table.** 2-of-3: 15 right, 1 wrong (C09), 4 abstentions. 3-of-5: 15 right, 0 wrong, 5 abstentions. Changes on C02, C09, C19. These are identical, row by row, to the output of our `td2/A-quorum/td2_vote_table.py`.

## Findings

- The rule is built only from the TD 1 rates and cells, and each check is tied to a cost of error (dashboard, customer, payout), as the statement requires.
- The age families take the lesson of Step 1 into account: C09 is the reason given for 3-of-5 instead of 2-of-3.
- Minor: on C02, moving to 3-of-5 turns a correct consensus of the panel into an abstention. The rule handles this through the abstention sent to human review, but the report could say explicitly that 3-of-5 costs one correct answer (C02) and gains one (C19) on our batch.

## Decision

Accepted.

## Note added at the commit (Manal Hassan)

One precision: the abstention of the 'unknown family' scenario cites no TD 1 cell, because that family has none; every other decision cites its cells. The cost on C02 and the gain on C19 of moving to 3-of-5 are stated in section 2 of the report.
