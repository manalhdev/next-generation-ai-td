# Cross-review of Pair A by Pair B

Status: to be written by Pair B (Julia, Tasnim, Marie).

Reviewers:
Date:

## Checks to run (from the repository root)

- [ ] `python3 atelier-vote.py`: the four synthetic examples follow the contract (agreement, disagreement, unavailable member kept in n, wrong consensus).
- [ ] Read `vote_k_sur_n` in `skeleton-multi-llm-en.py`: strict majority `n // 2 < k <= n`, duplicate refused, error kept in n without a vote, abstention without an invented value.
- [ ] `python3 td2/A-quorum/analyse_votes.py`: recount three rows of `vote-td2.md` by hand from `traces-td1.csv`.
- [ ] The decisions of Pair B's own count (`td2/B-consensus/compte_votes.py`) on C09 and C10 are those of `vote_k_sur_n`.

## Findings

## Decision
