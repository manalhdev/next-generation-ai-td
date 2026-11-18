# Internal check of Step 2 by Pair B

Authors: Julia (lorentejla) and Marie (Marieseka), Pair B, 18 November 2026. Checked: the analysis of the wrong consensus C09 (Step 2), against `traces-td1.csv` and `reference-td1.csv`.

This is a check of Pair B's own step, not a cross-review. The file was sent with a wrong reviewer name ("Youssef, Pair C"); the names are corrected here and the rest is unchanged. Committed by Manal Hassan because Julia and Marie could not push.

## Checks run (from the repository root)

Checked against `traces-td1.csv` and `reference-td1.csv`:

- [x] Identification: C09 ("exactly 25 years old on 2026-09-26, all orders"), cohere/north-mini-code:free (OpenRouter) = 0 and qwen/qwen3.8-27b (Groq) = 0, both `incorrect`; reference 487980 (lorentejla, peer-checked by axel12334556).
- [x] Quorum verdicts: fixed 2-of-3 panel (120b = 487980, north = 0, qwen = 0) → **consensus on 0, wrong**. 3-of-5 (0: north + qwen; 487980: 120b + 20b; 47900: dots) → **abstention**, 2–2 tie, no value reaches k = 3.
- [x] Root cause, north: correct birth-date window, but an extra filter `o.date >= '2026-09-26 00:00:00' AND o.date < '2027-09-26 00:00:00'` keeps only orders placed after the reference date, while the question asks for all orders.
- [x] Root cause, qwen: age computed against `o.date` instead of the reference date, and `strftime('%m-%d', o.date) >= strftime('%m-%d', c.birth_date) AND strftime('%m-%d', o.date) < strftime('%m-%d', date(c.birth_date, '+26 years'))`: +26 years keeps the month-day (except 29 Feb), so the condition is always false and the set is empty.
- [x] Two different bugs giving the same value: this shows that agreement is not proof of correctness (Lecture 2).
- [x] Second shared wrong value in the batch: C10 (north = 0, dots = 0). Dots is outside the panel, and 3-of-5 is a 2–2 tie (558980: 120b + 20b), so the wrong value wins neither.

Execution on `data/boutique.sqlite`:

- [ ] `sqlite3 data/boutique.sqlite < partie_b.sql`: the delta query (birth_date > '2000-09-26' AND <= '2001-09-26', GROUP BY customer_id) lists the missed rows, and their sum = 487980.
- [ ] `SELECT COUNT(*) FROM orders WHERE date >= '2026-09-26 00:00:00';` = 0 (confirms north's bug).
- [ ] `python3 atelier-vote.py --traces traces-td1.csv --case C09`: same decision as the manual count (consensus on 0 in 2-of-3).

## Findings

- The case is correctly identified from our own batch (`nature = real`), so DEMO-SQL-C11 is not needed.
- The quorum verdicts declared in the report match the traces.
- The two root causes are distinct and correctly located in the WHERE clause.
- To complete if missing: paste the actual output of the delta query (customer_id rows + total) into `reports/td2.md`, and mention C10 as a second shared wrong value.

## Decision

Accepted, provided the delta query output (sum = 487980) is pasted into the report.

## Note added at the commit (Manal Hassan)

Both requests are done in [reports/td2.md](../../reports/td2.md): the output of the delta query (six customers, total 487980) is in section 3.3, and C10 in section 3.6. The three checks on `data/boutique.sqlite`, left unticked in the file sent, were run at the merge: [partie-b-output.txt](partie-b-output.txt), [c09-check-td2.txt](../C-routing/c09-check-td2.txt), [atelier-vote-td2.txt](../C-routing/atelier-vote-td2.txt).
