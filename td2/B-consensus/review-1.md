# Cross-review of Pair B by Pair A

Status: to be written by Pair A.

Reviewers:
Date:

## Checks to run (from the repository root)

- [ ] `python3 td2/B-consensus/run_partie_b.py data/boutique.sqlite td2/B-consensus/partie_b.sql`: reference 487980, Cohere 0, Qwen 0, total delta 487980.
- [ ] `python3 atelier-vote.py --traces traces-td1.csv --case C09`: `vote_k_sur_n` gives the decision counted by Pair B for the 2-of-3 panel.
- [ ] Explain why the two faulty WHERE clauses return 0 and not `NULL`, and why 0 alone does not reveal the error.

## Findings

## Decision
