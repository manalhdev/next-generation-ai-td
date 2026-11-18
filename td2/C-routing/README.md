# Pair C — Step 3: the routing rule

Members: Manal Hassan, to be completed.

## Work

- [family_rates.py](family_rates.py): exact TD 1 accuracy of each model on each question family, from `model-question-comparison-en.csv`; output [family-rates-td2.md](family-rates-td2.md).
- [routing-rule.md](routing-rule.md): the one-page rule (first model, checks per use, course of action when the first model is unavailable), the scenarios R1 to R5, the changes made to the simulator and the analysis of the priority order of `choose`.
- `atelier-routage.py`, at the repository root: `RESOURCES` and `choose` adapted to the rule; every reason cites the TD 1 cells. Outputs [routing-before.txt](routing-before.txt) (supplied version) and [routing-after.txt](routing-after.txt) (adapted version).
- [review-1.md](review-1.md), [review-2.md](review-2.md): cross-reviews by Pair A and Pair B.

## Replay (from the repository root)

```bash
python3 td2/C-routing/family_rates.py
python3 atelier-routage.py
python3 atelier-routage.py --scenario "F2 customer figure"
```

## Result

Period and product questions: four or five models are at 100 % in TD 1, so gpt-oss-20b goes first and a dashboard needs no check. Questions with an age at a reference date: only gpt-oss-120b is at 100 % (8/8); a figure shown to a customer uses a 3-of-5 quorum, an amount paid out a reference query and a human review. Summary: [reports/td2.md](../../reports/td2.md), section 4.
