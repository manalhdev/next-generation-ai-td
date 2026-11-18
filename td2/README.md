# TD 2 — The quorum, then the routing rule

Session of 18 November 2026, sub-group 1. Report: [reports/td2.md](../reports/td2.md). Statement: [enonce-td2-en.md](../enonce-td2-en.md).

The sub-group split into three pairs, one step each (Pair B has three members). Each pair folder holds its work, its README and the two cross-reviews written by the other pairs.

| Folder | Pair | Step | Main result |
|---|---|---|---|
| [A-quorum](A-quorum/README.md) | A: Jonas, Axel | 1. `vote_k_sur_n`, fixed 2-of-3 panel against 3-of-5 quorum on the twenty questions | 2-of-3: 15 right, 1 wrong (C09), 4 abstentions. 3-of-5: 15 right, 0 wrong, 5 abstentions |
| [B-consensus](B-consensus/README.md) | B: Julia, Tasnim, Marie | 2. Wrong consensus | C09: Cohere and Qwen both return 0, reference 487980. The 2-of-3 panel keeps 0, the 3-of-5 quorum abstains |
| [C-routing](C-routing/README.md) | C: Ines, Manal | 3. Routing rule | First model and checks per question family, from the TD 1 rates; simulator adapted |

The course kit stays at the repository root: `skeleton-multi-llm-en.py` (with `vote_k_sur_n`), `atelier-vote.py`, `atelier-routage.py` (adapted by Pair C), `data/boutique.sqlite`, `traces-td1.csv`, `reference-td1.csv`. Every command runs from the root, with no network call and no key:

```bash
python3 atelier-vote.py
python3 td2/A-quorum/analyse_votes.py
python3 td2/B-consensus/run_partie_b.py data/boutique.sqlite td2/B-consensus/partie_b.sql
python3 td2/B-consensus/c09_check.py data/boutique.sqlite
python3 td2/C-routing/family_rates.py
python3 atelier-routage.py
```
