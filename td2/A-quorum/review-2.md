# Cross-review of Pair A by Pair C

Reviewer: Manal Hassan (Pair C), 18 November 2026, while merging the three deliverables. Checks run with Claude Code ([prompts-ai-assistance.md](../../prompts-ai-assistance.md)).

Reviewed: `vote_k_sur_n` as committed in c01e9a1 (Daiki4529), and the Pair A hand-off note (vote code, table script, report text for Step 1).

## Checks run

| Check | Result |
|---|---|
| `python3 atelier-vote.py`, four synthetic examples | agreement keeps 100 with 2 votes; disagreement abstains (largest count 1); one answer out of three abstains (largest count 1), the two errors stay in n; [0, 0, 100] keeps 0 with 2 votes, wrong against the reference 100 |
| k = 1 or k = 4 with n = 3, k = 2 with n = 4 | `ValueError`: k must be a strict majority |
| Two proposals with the same provider and model | `ValueError`: the duplicate is refused |
| [0, 0, 487980, 487980, 47900] with k = 3 | abstention, largest count 2, no value invented |
| Vote code of the hand-off note | reads the proposals as dictionaries (`t["provider"]`) and fails with `TypeError` on the objects passed by `atelier-vote.py` |
| Table script of the hand-off note | counts the votes itself instead of calling `vote_k_sur_n` |
| Twenty decisions recomputed with `vote_k_sur_n` on `traces-td1.csv` | same decisions as the hand-off note: 2-of-3, 15 right, 1 wrong (C09), 4 abstentions; 3-of-5, 15 right, 0 wrong, 5 abstentions; changes on C02, C09 and C19 |

## Changes made at the merge

- The committed version of `vote_k_sur_n` (c01e9a1), which reads objects, is kept; the vote code of the hand-off note is not used.
- The table script of the hand-off note is not used: the table is recomputed by [td2/C-routing/analyse_votes.py](../C-routing/analyse_votes.py), written at the merge, which calls `vote_k_sur_n` through `atelier-vote.py`, as the statement asks for the 3-of-5 quorum.
- Report text: "every failure is an invalid SQL statement" became "the only cells that do not vote are three invalid SQL statements (Cohere C08 and C11, Qwen C06)"; symbols replaced by words.

## Decision

Accepted with the changes above.
