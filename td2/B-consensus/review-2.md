# Cross-review of Pair B by Pair C

Reviewer: Manal Hassan (Pair C), 18 November 2026, while merging the three deliverables. Checks run with Claude Code ([prompts-ai-assistance.md](../../prompts-ai-assistance.md)).

Reviewed: the two Pair B deliverables, a package with the SQL, the scripts and the text (expected values, not yet run on the database), and a report section with executed outputs.

## Checks run on `data/boutique.sqlite` (read-only)

| Claim of Pair B | Rerun | Result |
|---|---|---|
| Reference of C09 | `partie_b.sql`, query 0 | 487980 |
| Cohere and Qwen queries copied from the traces | queries 1 and 2, compared with the `sql` column of `traces-td1.csv` | 0 and 0; same text as the traces |
| Cohere without its order-date clause | query 3a | 487980 |
| No order of these customers falls in Cohere's window | query 3b | 68 order lines from 2026-01-14 to 2026-09-18, none in the window; the base ends on 2026-09-20 |
| Adding 26 years never changes the month-day | query 3c, births on 29 February | 0 customers concerned, no birth on 29 February |
| Delta per customer and total | queries 4 and 5 | six customers, total delta 487980 for both models |
| Value of Dots | query 6 | 47900 = customer C003, born on 2001-09-26 |
| Nothing wrongly added | `COUNT(*)` of each faulty WHERE clause on the whole base, product prices | 0 rows for each; every price is positive (2990, 1490, 1250, 1990, 2450) |
| Votes counted by hand | `compte_votes.py` against `vote_k_sur_n` | same decisions on C09 and C10 |
| Secondary case C10 | `sql` column of Cohere and Dots | contradictory bounds in both queries, value 0 |

## Changes made at the merge

- The executed outputs replace the expected values of the package; the structure and the delta query of the package are kept.
- `c09_check.py`, cited by the package, was not received: it was rewritten with the same purpose (delta query in another formulation, `COUNT(*)` of the faulty clauses, recomputation in Python without SQL). Pair B can replace it with its original.
- Symbols replaced by words in the report text. The SQL and the scripts are kept as delivered, with their French comments.

## Decision

Accepted and merged into [reports/td2.md](../../reports/td2.md), section 3.
