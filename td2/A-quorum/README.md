# Pair A — Step 1: the k-of-n vote

Members: Daiki4529, to be completed.

## Work

- `Orchestrateur.vote_k_sur_n` in [skeleton-multi-llm-en.py](../../skeleton-multi-llm-en.py) (commit c01e9a1): only executed proposals with a value vote; an error stays in n without a vote; k must satisfy `n // 2 < k <= n`; a duplicate (provider, model) is refused; when no value reaches k, the method abstains and returns the largest count, never a value.
- [analyse_votes.py](analyse_votes.py): calls `vote_k_sur_n` on the twenty questions, through the proposals built by `atelier-vote.py`, for the fixed 2-of-3 panel (120B, Cohere, Qwen, k = 2) and for the 3-of-5 quorum (the five TD 1 models, k = 3). The reference is compared after the decision.

## Files

| File | Content |
|---|---|
| [vote-td2.md](vote-td2.md), [vote-td2.csv](vote-td2.csv) | The twenty decisions of both votes and their agreement with `reference-td1.csv` |
| [atelier-vote-td2.txt](atelier-vote-td2.txt) | Output of `atelier-vote.py`: the four synthetic examples, then the real traces of C02, C09 and C19 |
| [review-1.md](review-1.md), [review-2.md](review-2.md) | Cross-reviews by Pair B and Pair C |

## Replay (from the repository root)

```bash
python3 atelier-vote.py
python3 atelier-vote.py --traces traces-td1.csv --case C09
python3 td2/A-quorum/analyse_votes.py
```

## Result

2-of-3 panel: 15 right, 1 wrong (C09), 4 abstentions. 3-of-5 quorum: 15 right, 0 wrong, 5 abstentions. The decision changes on C02 (correct consensus to abstention), C09 (wrong consensus to abstention) and C19 (abstention to correct consensus). Table and commentary: [reports/td2.md](../../reports/td2.md), section 2.
