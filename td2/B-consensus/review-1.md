# Cross-review of Pair B by Pair A

Written by Tasnim (TasB) on behalf of Pair A (Jonas, Axel), 18 November 2026: Axel became unavailable during the session. The checks were run with Claude ([prompts-ai-assistance.md](../../prompts-ai-assistance.md)), from the repository root, at commit 6762a79. Pair A may confirm or amend these checks.

Reviewed: [partie_b.sql](partie_b.sql), [run_partie_b.py](run_partie_b.py), [compte_votes.py](compte_votes.py) and section 3 of [reports/td2.md](../../reports/td2.md).

## Checks run (from the repository root)

- [x] **`python3 td2/B-consensus/run_partie_b.py data/boutique.sqlite td2/B-consensus/partie_b.sql`.** Reference 487980, Cohere 0, Qwen 0. Six customers in the delta: C001 135000, C002 25920, C003 47900, C007 118740, C008 99090, C009 61330. Total delta 487980 for both models, `REF OK (487980)`. The output is identical to the stored [partie-b-output.txt](partie-b-output.txt) (`diff` empty).
- [x] **`python3 atelier-vote.py --traces traces-td1.csv --case C09`.** `vote_k_sur_n` (Pair A, n = 3, k = 2) returns `{"consensus": true, "value": 0, "votes": 2, "models": ["openrouter:cohere/north-mini-code:free", "groq:qwen/qwen3.8-27b"]}`, `matches_reference: false`. This is the decision Pair B counted by hand for the 2-of-3 panel. With five models, `td2/A-quorum/td2_vote_table.py` gives an abstention on C09 (largest count 2), also as Pair B states.
- [x] **Why 0 and not `NULL`, and why 0 alone does not reveal the error.** Both faulty WHERE clauses keep no row: Cohere's order-date window contains none of the 68 order lines of these customers (the base ends on 2026-09-20), and Qwen's month-day pair is impossible. `SUM` over an empty set is `NULL`, and the binding convention `COALESCE(SUM(...), 0)` turns it into 0. So the query returns a valid integer with no error. A 0 is also a legitimate answer: C06 and C14 have a true reference of 0. The value alone cannot distinguish "no matching order" from "a filter that wrongly keeps nothing". Only a row count of the filter followed by the reference query can tell them apart, which is the check Pair B proposed to Pair C.

## Findings

- The case comes from our own batch (`nature = real`), so DEMO-SQL-C11 is not needed. The two models, the shared wrong value, the reference and the two quorum decisions match the traces and `vote_k_sur_n`.
- The two root causes are distinct and located precisely: an extra order-date filter for Cohere, a contradictory month-day pair for Qwen. Each one is proved by a query: removing Cohere's date clause gives 487980; the month-day pair keeps 0 rows.
- The delta query accounts for the whole gap (487980 − 0), with no row wrongly added. Dots' value 47900 is explained (customer C003, born on 2001-09-26).

## Decision

Accepted.

## Note added at the commit (Manal Hassan)

Tasnim is a member of Pair B: this review of Pair B was not written by another pair. It is published as sent, with its own statement of authorship; Pair A has not confirmed it yet.
