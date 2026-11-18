# Pair C — Step 3: the routing rule

Members: Ines (ines729), Manal Hassan (manalhdev).

## Work

- [family_rates.py](family_rates.py): exact TD 1 accuracy of each model on each question family, from `model-question-comparison-en.csv`; output [family-rates-td2.md](family-rates-td2.md).
- [routing-rule.md](routing-rule.md): the one-page rule (first model, checks per use, course of action when the first model is unavailable), the scenarios R1 to R5, the changes made to the simulator and the analysis of the priority order of `choose`.
- `atelier-routage.py`, at the repository root: `RESOURCES` and `choose` adapted to the rule; every reason cites the TD 1 cells. Outputs [routing-before.txt](routing-before.txt) (supplied version) and [routing-after.txt](routing-after.txt) (adapted version).
- [review-1.md](review-1.md), [review-2.md](review-2.md): cross-reviews by Pair A and Pair B.

## Checks of Steps 1 and 2, made by Manal Hassan at the merge

- [analyse_votes.py](analyse_votes.py): recomputes the twenty decisions of Step 1 with `vote_k_sur_n`, on the proposals built by `atelier-vote.py`; outputs [vote-td2.md](vote-td2.md) and [vote-td2.csv](vote-td2.csv), same decisions as the Pair A table. It replaces the table script of the Pair A hand-off note, which counted the votes itself.
- [atelier-vote-td2.txt](atelier-vote-td2.txt): output of `atelier-vote.py` with the method of Pair A: the four synthetic examples, then the real traces of C02, C09 and C19.
- [c09_check.py](c09_check.py): independent checks of C09 (delta query in another formulation, rows kept by the faulty clauses, recomputation in Python without SQL); output [c09-check-td2.txt](c09-check-td2.txt). Written because the `c09_check.py` cited by Pair B was not received.

## Replay (from the repository root)

```bash
python3 td2/C-routing/family_rates.py
python3 atelier-routage.py
python3 atelier-routage.py --scenario "F2 customer figure"
python3 td2/C-routing/analyse_votes.py
python3 td2/C-routing/c09_check.py data/boutique.sqlite
```

## Result

Period and product questions: four or five models are at 100 % in TD 1, so gpt-oss-20b goes first and a dashboard needs no check, except for a value of 0. Questions with an age at a reference date: only gpt-oss-120b is at 100 % (8/8); a figure shown to a customer uses a 3-of-5 quorum, an amount paid out a reference query and a human review. A value of 0 is delivered only after a `COUNT(*)` of the filtered rows and, if no row is kept, the reference query (input of Pair B). Summary: [reports/td2.md](../../reports/td2.md), section 4.
