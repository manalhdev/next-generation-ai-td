# Pair B — Step 2: the wrong consensus

Members: Julia (lorentejla), Tasnim (TasB), Marie (Marieseka).

## Case

C09, from our own TD 1 batch (real cells of 21 October 2026): revenue of the customers aged exactly 25 on 2026-09-26. Reference 487980. cohere/north-mini-code:free and qwen/qwen3.8-27b both return 0.

- Fixed 2-of-3 panel (120B, Cohere, Qwen, k = 2): keeps 0 with 2 votes, a wrong consensus.
- 3-of-5 quorum (k = 3): 487980 and 0 have 2 votes each, Dots returns 47900: abstention.
- Cohere adds an order-date window (`o.date >= '2026-09-26' AND o.date < '2027-09-26'`) that no order falls in. Qwen computes the age at the order date and adds two contradictory month-day conditions. `COALESCE` turns both empty sets into 0.
- Delta query: the six customers born in ]2000-09-26, 2001-09-26] (68 order lines) account for the whole gap of 487980; no row is wrongly added.

Full analysis: [reports/td2.md](../../reports/td2.md), section 3.

## Files

| File | Content |
|---|---|
| [partie_b.sql](partie_b.sql) | Reference, the two model queries, clause tests, delta query per customer, total check, Dots subset |
| [run_partie_b.py](run_partie_b.py) | Runs `partie_b.sql` read-only; output [partie-b-output.txt](partie-b-output.txt) |
| [compte_votes.py](compte_votes.py) | Independent vote count for C09 and C10, to compare with `vote_k_sur_n`; output [compte-votes-td2.txt](compte-votes-td2.txt) |
| [demo_vote.py](demo_vote.py) | DEMO-VOTE: constructed teaching data on a one-row toy table, not an analysis case; output [demo-vote-td2.txt](demo-vote-td2.txt) |
| [internal-check.md](internal-check.md) | Check of Step 2 by Julia and Marie (Pair B), not a cross-review |
| [review-1.md](review-1.md), [review-2.md](review-2.md) | Cross-reviews by Pair A and Pair C |

`partie_b.sql`, `run_partie_b.py`, `compte_votes.py` and `demo_vote.py` are kept as delivered by Pair B, with their French comments. The `c09_check.py` cited by the package was not received: the independent checks of C09 written by Pair C at the merge are in [td2/C-routing/c09_check.py](../C-routing/c09_check.py).

## Replay (from the repository root)

```bash
python3 td2/B-consensus/run_partie_b.py data/boutique.sqlite td2/B-consensus/partie_b.sql
python3 td2/B-consensus/compte_votes.py traces-td1.csv
python3 td2/B-consensus/demo_vote.py
```
