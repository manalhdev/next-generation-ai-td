# Pair A — Step 1: the k-of-n vote

Members: Jonas (Daiki4529), Axel (axel12334556).

## Work

- `Orchestrateur.vote_k_sur_n` in [skeleton-multi-llm-en.py](../../skeleton-multi-llm-en.py), at the repository root as the statement requires (commit c01e9a1): only executed proposals with a value vote; an error stays in n without a vote; k must satisfy `n // 2 < k <= n`; a duplicate (provider, model) is refused; when no value reaches k, the method abstains and returns the largest count, never a value.
- The twenty-question table, fixed 2-of-3 panel (120B, Cohere, Qwen, k = 2) against 3-of-5 quorum (the five TD 1 models, k = 3), computed by [td2_vote_table.py](td2_vote_table.py) with our `vote_k_sur_n`, and its commentary: [reports/td2.md](../../reports/td2.md), section 2.

Pair C checked this work at the merge (independent recomputation `analyse_votes.py`, outputs of `atelier-vote.py`): see [td2/C-routing](../C-routing/README.md).

## Files

| File | Content |
|---|---|
| [td2_vote_table.py](td2_vote_table.py) | 2-of-3 against 3-of-5 on the twenty questions, prints the table of the report |
| [review-1.md](review-1.md), [review-2.md](review-2.md) | Cross-reviews by Pair B and Pair C |

## Replay (from the repository root)

```bash
python3 atelier-vote.py                                     # four synthetic examples
python3 atelier-vote.py --traces traces-td1.csv --case C09  # real traces of one question
python3 td2/A-quorum/td2_vote_table.py                      # twenty-question table
```

## Result

2-of-3 panel: 15 right, 1 wrong (C09), 4 abstentions. 3-of-5 quorum: 15 right, 0 wrong, 5 abstentions. The decision changes on C02 (correct consensus to abstention), C09 (wrong consensus to abstention) and C19 (abstention to correct consensus).
