# TD 2 report — The quorum, then the routing rule

Sub-group 1. Session of 18 November 2026. Course pack `2026-11-18-students-5` (code identical to the TD 1 kit; documents updated). No new network call: everything below uses the stored TD 1 traces (`traces-td1.csv`: 100 real cells, 5 models x C01 to C20, one attempt each, all HTTP 200) and `reference-td1.csv`.

Members (GitHub accounts): Manal Hassan (manalhdev), axel12334556, ines729, Marieseka, TasB (TazBrks), Daiki4529, lorentejla.

## 1. What we attempted and completed

| Step | Pair | Deliverable | Status |
|---|---|---|---|
| 1. k-of-n vote, 2-of-3 against 3-of-5 | A | `vote_k_sur_n` in `skeleton-multi-llm-en.py`, twenty-question table, folder [td2/A-quorum](../td2/A-quorum/README.md) | done |
| 2. Wrong consensus | B | case C09 from our own batch, SQL root causes, delta query run on `data/boutique.sqlite`, folder [td2/B-consensus](../td2/B-consensus/README.md) | done |
| 3. Routing rule | C | [routing rule](../td2/C-routing/routing-rule.md), rates, simulator before and after, checks of Steps 1 and 2 made at the merge, folder [td2/C-routing](../td2/C-routing/README.md) | done |

Layout: one folder per pair under [td2/](../td2/README.md), each with its README and its two cross-reviews. The course kit (`skeleton-multi-llm-en.py`, `atelier-vote.py`, `atelier-routage.py`, `data/`, `traces-td1.csv`, `reference-td1.csv`) stays at the repository root, where the course commands run.

Replay, from the repository root:

```bash
python3 atelier-vote.py                                     # four synthetic examples
python3 atelier-vote.py --traces traces-td1.csv --case C09  # real traces of one question
python3 td2/C-routing/analyse_votes.py                      # twenty-question table recomputed with vote_k_sur_n
python3 td2/B-consensus/run_partie_b.py data/boutique.sqlite td2/B-consensus/partie_b.sql
python3 td2/C-routing/c09_check.py data/boutique.sqlite
python3 td2/B-consensus/compte_votes.py traces-td1.csv
python3 td2/B-consensus/demo_vote.py
python3 td2/C-routing/family_rates.py
python3 atelier-routage.py
```

## 2. Step 1 — The vote (Pair A)

**Implementation.** `Orchestrateur.vote_k_sur_n` follows the contract of its docstring: only executed proposals with a value vote, an error stays in n without voting; k must satisfy `n // 2 < k <= n`, otherwise `ValueError`; a duplicate (provider, model) raises `ValueError`; a value with at least k votes is returned with its votes and the `provider:model` of its voters; otherwise the method abstains (`value: None`, `votes`: largest count) and never invents a value. Because k is a strict majority, at most one value can reach k. `atelier-vote.py` maps the trace verdicts `correct` and `incorrect` with a value to `executed`, and `sql_invalid` to `error`.

Two versions were written in the sub-group. The one kept is the version committed to the repository (c01e9a1): it reads the proposals as objects (`trace.provider`), which is what `atelier-vote.py` passes. The hand-off version read them as dictionaries (`t["provider"]`) and fails with `TypeError` on the objects built by `atelier-vote.py`.

Outputs of `atelier-vote.py` ([td2/C-routing/atelier-vote-td2.txt](../td2/C-routing/atelier-vote-td2.txt), run at the merge): agreement keeps 100 with 2 votes; disagreement abstains (max 1); one available member out of three abstains (max 1); the synthetic wrong consensus [0, 0, 100] keeps 0 with 2 votes, which does not match the reference 100.

**Twenty-question comparison.** 2-of-3 panel: gpt-oss-120b, cohere/north-mini-code:free, qwen/qwen3.8-27b, k = 2. 3-of-5 quorum: the five TD 1 models, k = 3. Table of the Pair A hand-off note, recomputed at the merge by Pair C with `vote_k_sur_n` (`td2/C-routing/analyse_votes.py`, on the proposals built by `atelier-vote.py`; [vote-td2.md](../td2/C-routing/vote-td2.md), [vote-td2.csv](../td2/C-routing/vote-td2.csv)): same twenty decisions. The reference is compared after the decision. Bold: wrong value.

| Q | Reference | 120B | Cohere | Qwen | 20B | Dots | 2-of-3 panel | 3-of-5 quorum | Change |
|---|---|---|---|---|---|---|---|---|---|
| C01 | 792800 | 792800 | 792800 | 792800 | 792800 | 792800 | 792800 (3 votes, correct) | 792800 (5 votes, correct) |  |
| C02 | 590320 | 590320 | **321340** | 590320 | **0** | **455320** | 590320 (2 votes, correct) | abstain (max 2) | yes |
| C03 | 936350 | 936350 | 936350 | 936350 | 936350 | 936350 | 936350 (3 votes, correct) | 936350 (5 votes, correct) |  |
| C04 | 2826250 | 2826250 | 2826250 | 2826250 | 2826250 | 2826250 | 2826250 (3 votes, correct) | 2826250 (5 votes, correct) |  |
| C05 | 38480 | 38480 | 38480 | 38480 | 38480 | 38480 | 38480 (3 votes, correct) | 38480 (5 votes, correct) |  |
| C06 | 0 | 0 | 0 | *sql_invalid* | 0 | 0 | 0 (2 votes, correct) | 0 (4 votes, correct) |  |
| C07 | 13970 | 13970 | 13970 | 13970 | 13970 | 13970 | 13970 (3 votes, correct) | 13970 (5 votes, correct) |  |
| C08 | 605580 | 605580 | *sql_invalid* | 605580 | 605580 | **0** | 605580 (2 votes, correct) | 605580 (3 votes, correct) |  |
| C09 | 487980 | 487980 | **0** | **0** | 487980 | **47900** | 0 (2 votes, WRONG) | abstain (max 2) | yes |
| C10 | 558980 | 558980 | **0** | **119410** | 558980 | **0** | abstain (max 1) | abstain (max 2) |  |
| C11 | 446690 | 446690 | *sql_invalid* | 446690 | 446690 | 446690 | 446690 (2 votes, correct) | 446690 (4 votes, correct) |  |
| C12 | 1666490 | 1666490 | 1666490 | 1666490 | 1666490 | 1666490 | 1666490 (3 votes, correct) | 1666490 (5 votes, correct) |  |
| C13 | 107740 | 107740 | 107740 | 107740 | 107740 | 107740 | 107740 (3 votes, correct) | 107740 (5 votes, correct) |  |
| C14 | 0 | 0 | 0 | 0 | 0 | 0 | 0 (3 votes, correct) | 0 (5 votes, correct) |  |
| C15 | 168680 | 168680 | **314020** | **0** | 168680 | **138920** | abstain (max 1) | abstain (max 2) |  |
| C16 | 376740 | 376740 | 376740 | 376740 | 376740 | **1367540** | 376740 (3 votes, correct) | 376740 (4 votes, correct) |  |
| C17 | 258180 | 258180 | **197080** | **248490** | 258180 | **152730** | abstain (max 1) | abstain (max 2) |  |
| C18 | 62480 | 62480 | 62480 | 62480 | 62480 | 62480 | 62480 (3 votes, correct) | 62480 (5 votes, correct) |  |
| C19 | 1990 | 1990 | **71640** | **83580** | 1990 | 1990 | abstain (max 1) | 1990 (3 votes, correct) | yes |
| C20 | 1106090 | 1106090 | 1106090 | 1106090 | 1106090 | 1106090 | 1106090 (3 votes, correct) | 1106090 (5 votes, correct) |  |

**Totals.** 2-of-3: 16 consensus (15 correct, 1 wrong: C09) and 4 abstentions. 3-of-5: 15 consensus (15 correct, 0 wrong) and 5 abstentions.

**Questions where the decision changes.**

- **C02, correct consensus to abstention.** In 2-of-3, 120B and Qwen agree on 590320 (Cohere 321340): 2 votes, k = 2. In 3-of-5, 590320 still has 2 votes only, because 20B returns 0 and Dots 455320: 2 < 3, the quorum abstains. This is the cost of the larger quorum: a correct answer is no longer delivered.
- **C09, wrong consensus to abstention.** In 2-of-3, Cohere and Qwen both return 0: the panel keeps a wrong value (reference 487980). In 3-of-5, 487980 (120B, 20B) and 0 (Cohere, Qwen) have 2 votes each and Dots returns 47900: no value reaches 3, the quorum abstains. Analysed in step 2.
- **C19, abstention to correct consensus.** In 2-of-3, the three values differ (1990, 71640, 83580). In 3-of-5, 20B and Dots join 120B on 1990: 3 votes = k. The two models outside the panel turn the abstention into a correct answer.

**Margin changes only.**

- **C06 and C11.** Qwen on C06 (`no such function: COALESE`) and Cohere on C11 (`syntax error near "AS"`) do not vote but stay in n: the panel passes with exactly 2 votes out of 3, with no margin left; the quorum passes with 4.
- **C08.** Cohere is `sql_invalid` and Dots returns 0: 2 out of 3 for the panel, exactly 3 out of 5 for the quorum.
- **C16.** Dots returns a wrong 1367540: 3 out of 3 for the panel, 4 out of 5 for the quorum.
- **C10, C15, C17.** Both abstain; the largest count goes from 1 to 2 because 120B and 20B agree, which is not enough for k = 3.

No HTTP 429 in this batch: the only cells that do not vote are three invalid SQL statements (Cohere C08 and C11, Qwen C06).

## 3. Step 2 — The wrong consensus (Pair B)

Case from **our own TD 1 batch** (real cells of 21 October 2026, files `traces-C.csv` and `traces-D.csv`), so the historical case DEMO-SQL-C11 is not needed.

**Search in the 100 cells.** Cells with `verdict = incorrect`, grouped by question and value, keeping the groups with at least two models:

| Question | Shared wrong value | Models | Reference | Members of the fixed panel |
|---|---|---|---|---|
| **C09** | **0** | cohere/north-mini-code:free, qwen/qwen3.8-27b | 487980 | both |
| C10 | 0 | cohere/north-mini-code:free, dots-studio/dots-3-note-preview:free | 558980 | Cohere only |

The other wrong values (C02, C15, C17, C19) are all different. C09 is the main case: it is the only one where the wrong value wins a quorum.

### 3.1 Identification and quorum verdict (C09)

C09: revenue excluding VAT, in cents, of the customers who are exactly 25 years old on 2026-09-26, over all their orders. Independent reference 487980 (`reference-td1.csv`, written by lorentejla, checked by axel12334556).

| Model | Provider | Value | Verdict | 2-of-3 panel | 3-of-5 quorum |
|---|---|---|---|---|---|
| openai/gpt-oss-120b | Groq | 487980 | correct | member | member |
| openai/gpt-oss-20b | Groq | 487980 | correct | - | member |
| cohere/north-mini-code:free | OpenRouter | **0** | incorrect | member | member |
| qwen/qwen3.8-27b | Groq | **0** | incorrect | member | member |
| dots-studio/dots-3-note-preview:free | OpenRouter | 47900 | incorrect | - | member |

- **2-of-3 panel (n = 3, k = 2):** 0 gets 2 votes (Cohere, Qwen), 487980 gets 1 (120B): `{"consensus": True, "value": 0, "votes": 2}`. The panel keeps the wrong value and outvotes the only correct member.
- **3-of-5 quorum (n = 5, k = 3):** 487980 gets 2 (120B, 20B), 0 gets 2 (Cohere, Qwen), 47900 gets 1 (Dots): `{"consensus": False, "value": None, "votes": 2}`. The quorum does not keep the wrong value, but it does not return the right one either.

Counted by hand, then checked with `vote_k_sur_n` (`python3 atelier-vote.py --traces traces-td1.csv --case C09`) and with the independent count of Pair B, `td2/B-consensus/compte_votes.py` ([compte-votes-td2.txt](../td2/B-consensus/compte-votes-td2.txt)): same decisions. Moving from 2-of-3 to 3-of-5 turns a silent error into a visible abstention.

### 3.2 Faulty SQL clauses

Being exactly 25 on 2026-09-26 means being born in **]2000-09-26, 2001-09-26]**: born on 2000-09-26 is 26 that day (excluded), born on 2001-09-26 is 25 that day (included). The question takes all the orders: no filter on `o.date`. The two queries below are copied unchanged from `traces-td1.csv`; both run without error and return 0, for two different reasons.

**Cohere (returns 0)**

```sql
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE c.birth_date <= '2026-09-26' AND c.birth_date > date('2026-09-26', '-26 years')
AND c.birth_date <= date('2026-09-26', '-25 years') AND c.birth_date > date('2026-09-26', '-26 years')
AND o.date >= '2026-09-26 00:00:00' AND o.date < '2027-09-26 00:00:00';
```

The birth window is correct (`date('2026-09-26', '-26 years')` is 2000-09-26, `date('2026-09-26', '-25 years')` is 2001-09-26; the other conditions are redundant). **The faulty clause is `AND o.date >= '2026-09-26 00:00:00' AND o.date < '2027-09-26 00:00:00'`**: a period of orders the question never asks for. The 68 order lines of these customers go from 2026-01-14 to 2026-09-18 and none is in that period; the whole base ends on 2026-09-20. The set is empty and `COALESCE` turns the empty sum into 0. Proof: the same query without this clause returns 487980.

**Qwen (returns 0)**

```sql
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE (strftime('%Y', o.date) - strftime('%Y', c.birth_date)) = 25
  AND (strftime('%m-%d', o.date) >= strftime('%m-%d', c.birth_date))
  AND (strftime('%m-%d', o.date) < strftime('%m-%d', date(c.birth_date, '+26 years')));
```

Two errors. First, the age is computed on the order date `o.date` instead of the reference date 2026-09-26, which is the meaning of C10 (age at the order), not of C09. Second, **the faulty clause, enough on its own to give 0, is the pair `strftime('%m-%d', o.date) >= strftime('%m-%d', c.birth_date)` and `strftime('%m-%d', o.date) < strftime('%m-%d', date(c.birth_date, '+26 years'))`**: adding 26 years does not change the month and day (except for a birth on 29 February, and there is none in the base), so the condition reads "md(o) >= md(b) and md(o) < md(b)", which is impossible. On the whole base, the year condition alone keeps 72 order lines; the pair of month-day conditions keeps none, alone or with it.

**Why two different bugs give the same value.** With `COALESCE(SUM(...), 0)`, any filter that keeps no row returns 0, whatever the reason. 0 is also a plausible answer (C06 and C14 really are 0). Agreement on 0 only proves that both filters are empty, not that they are right; without `COALESCE`, the empty sum would be `NULL`, a visible anomaly. Dots (47900) shows the same boundary problem: its conditions keep only the customers born on 26 September 2001, and 47900 is exactly the revenue of customer C003, born on 2001-09-26.

### 3.3 Delta diagnostic query on `data/boutique.sqlite`

Query 4 of [td2/B-consensus/partie_b.sql](../td2/B-consensus/partie_b.sql): for each customer, the revenue counted by the reference query is compared with the revenue counted by the exact WHERE clauses of Cohere and Qwen; only the customers with a gap are listed. Run read-only with `python3 td2/B-consensus/run_partie_b.py data/boutique.sqlite td2/B-consensus/partie_b.sql` ([partie-b-output.txt](../td2/B-consensus/partie-b-output.txt)):

| customer_id | birth_date | ref_cents | Cohere | Qwen | delta Cohere | delta Qwen |
|---|---|---|---|---|---|---|
| C007 | 2000-11-30 | 118740 | 0 | 0 | 118740 | 118740 |
| C009 | 2001-03-10 | 61330 | 0 | 0 | 61330 | 61330 |
| C008 | 2001-05-15 | 99090 | 0 | 0 | 99090 | 99090 |
| C002 | 2001-09-24 | 25920 | 0 | 0 | 25920 | 25920 |
| C001 | 2001-09-25 | 135000 | 0 | 0 | 135000 | 135000 |
| C003 | 2001-09-26 | 47900 | 0 | 0 | 47900 | 47900 |
| **Total** | | **487980** | **0** | **0** | **487980** | **487980** |

Closing check (query 5): the sum of the deltas is 487980 - 0 = 487980 for both models, so these six customers (68 order lines) account for the whole gap. No row is wrongly added: on the whole base, the WHERE clauses of Cohere and Qwen keep 0 rows, and every price is positive (a 2990, b 1490, c 1250, d 1990, e 2450), so a total of 0 is an empty set.

### 3.4 Independent checks

| Method | Result |
|---|---|
| Reference query of C09 (`reference-td1.csv`, age computed with `strftime`) | 487980 |
| Delta query, birth-date window, another formulation (`td2/C-routing/c09_check.py`) | 487980 |
| Recomputation in Python on the CSV files, no SQL (`td2/C-routing/c09_check.py`) | 487980 |
| TD 1 cross-check of the reference (lorentejla, axel12334556) | 487980 |
| Two correct model queries with different formulations (120B with `date(..., '-26 years')`, 20B with literal bounds) | 487980 |
| Part of the reference for the customers born on 2001-09-26 (query 6) | 47900, the value of Dots |

Outputs: [c09-check-td2.txt](../td2/C-routing/c09-check-td2.txt), [partie-b-output.txt](../td2/B-consensus/partie-b-output.txt). `c09_check.py` was written by Pair C at the merge, because the one cited by Pair B was not received. Database SHA-256 `0077e235adc2ca647b484e3083c98a6d7cae3ef3655ce366a299caf13398fec2`.

### 3.5 Mechanism illustrated: DEMO-VOTE (constructed teaching data, not an analysis case)

One-row toy table (sale on 2026-01-01, 100 cents), period [2026-01-01, 2026-01-02[ (`python3 td2/B-consensus/demo_vote.py`, [demo-vote-td2.txt](../td2/B-consensus/demo-vote-td2.txt)):

| Variant | Condition | Value |
|---|---|---|
| two proposals | `sale_date > '2026-01-01' AND sale_date < '2026-01-02'` | 0 |
| one proposal | `sale_date >= '2026-01-01' AND sale_date < '2026-01-02'` | 100 |

`>` excludes the start bound that the period includes. With [0, 0, 100] and k = 2 out of 3, the vote keeps 0 while the independent reference is 100: a quorum measures agreement, not correctness. C09 reproduces this mechanism on the real base.

### 3.6 Secondary case: C10 (shared wrong value, outvoted)

C10 (age at the time of the order), reference 558980. Cohere and Dots both return 0. Cohere builds text bounds such as `birth_date || '-25-01'` and requires `o.date < X` and `o.date >= X` for the same X; Dots requires `md(o) >= md(b)` and `md(o) < md(b)`, the same contradiction as Qwen on C09. Panel 2-of-3: 558980, 0, 119410, largest count 1, abstention. Quorum 3-of-5: 558980 (120B, 20B) and 0 (Cohere, Dots) have 2 votes each, abstention. The shared wrong value wins neither vote, but it prevents the quorum from validating the right answer.

### 3.7 Consequence for checking

- On the age family F2, two members of the fixed panel are wrong together: the 2-of-3 panel does not protect this family (input of the routing rule of Pair C).
- The 3-of-5 quorum avoids the error on C09 but abstains: it does not replace a correct answer, so an abstention must go to a reference query or a human review.
- A consensus on 0 should be treated as suspect when a non-zero figure is expected: count the filtered rows (`COUNT(*)`) or keep `NULL` without `COALESCE`; an empty set over a non-empty population leads to abstention or review.
- The errors of the models are not independent (same prompt, same schema, same date trap), while a quorum assumes independent errors.

## 4. Step 3 — The routing rule (Pair C)

- TD 1 rates per family: [family-rates-td2.md](../td2/C-routing/family-rates-td2.md) (`python3 td2/C-routing/family_rates.py`).
- The one-page rule, the scenario table R1 to R5, the changes made to the simulator and the full analysis of the priority order of `choose`: [td2/C-routing/routing-rule.md](../td2/C-routing/routing-rule.md).
- Simulator outputs: before adaptation [routing-before.txt](../td2/C-routing/routing-before.txt), after [routing-after.txt](../td2/C-routing/routing-after.txt) (`python3 atelier-routage.py`).

Main findings:

- Period (F1) and product (F3) questions: four or five models are at 100 % in TD 1, so gpt-oss-20b goes first and a dashboard needs no check.
- Every question with an age at a reference date (8 cells): only gpt-oss-120b is at 100 % (8/8); gpt-oss-20b fails C02 with a silent wrong value, Qwen, Cohere and Dots fail 4, 7 and 6 of them.
- The 2-of-3 panel is not enough on the age families: on C09, two panel members (Cohere and Qwen) returned the same wrong value 0. Customer figures on these families use a 3-of-5 quorum, payouts a reference query and a human review.

**Priority order of the supplied `choose`.** The branches are tested in a fixed order: available included capacity (`cash == 0`, which covers a free route and an already paid subscription with `allocation > 0`), then deferral to an exhausted free route that refills before `deadline_minutes` when the request can wait, then a paid route within the budget, then abstention. An available subscription is therefore selected before any deferral: it spends no new money, it answers now, and a deferral is uncertain (a reset time is only an announcement, availability must be measured again at wake-up, the deadline can be missed). The priority should be reversed when the subscription capacity is scarce: an allocation for the period, or a cap shared by the team, that must be kept for requests that cannot wait. Then a request that can wait, with a reliable free refill before its deadline, should defer; in the code, the `waiting` branch would be tested first when `can_wait` is true and the remaining allocation is under a reserve threshold. Our rule has no subscription: on F2, the simulator waits for the free Groq refill before paying the OpenRouter route.

Limits: twenty questions and one run per cell; some families have one or two cells only (F2b: C10, C18), so their rates are weak evidence. Resource availability and refill times in the simulator are scenario assumptions, not measurements. The paid cost uses the portfolio price of 2026-09-29 and the TD 1 median tokens.

## 5. Internal cross-review

Before the report is finalised, each pair walks the other members through its code, SQL and decisions. Each pair folder holds the two reviews written by the other pairs.

| Pair reviewed | review-1.md | review-2.md |
|---|---|---|
| A, quorum | [by Pair B](../td2/A-quorum/review-1.md): to be written | [by Pair C](../td2/A-quorum/review-2.md): accepted, the vote version that reads objects is kept |
| B, consensus | [by Pair A](../td2/B-consensus/review-1.md): to be written | [by Pair C](../td2/B-consensus/review-2.md): accepted, every figure rerun on the database |
| C, routing | [by Pair A](../td2/C-routing/review-1.md): to be written | [by Pair B](../td2/C-routing/review-2.md): to be written |

## 6. Limits

- Twenty questions and one attempt per cell: a hypothesis for this batch, not a general error rate, a permanent ranking or a quorum guarantee.
- The value 0 of C09 depends on the data: with orders after 2026-09-26, Cohere would return a non-zero wrong value and its agreement with Qwen would disappear.
- No second network batch: the vote is evaluated on stored TD 1 traces only.

## 7. Division of work

| Pair | Members | Step |
|---|---|---|
| A | Jonas (Daiki4529), Axel (axel12334556) | 1. Vote |
| B | Julia (lorentejla), Tasnim (TasB), Marie (Marieseka) | 2. Wrong consensus |
| C | Ines (ines729), Manal Hassan (manalhdev) | 3. Routing rule |

The three deliverables were merged by Manal Hassan; the merge choices (which vote version is kept, which delta query, the executed outputs) are explained in the steps above. What was made at the merge (`analyse_votes.py`, `c09_check.py`, the `atelier-vote.py` outputs) is in the folder of Pair C, not in the folders of the pairs it checks. AI-assisted code and its prompts: [prompts-ai-assistance.md](../prompts-ai-assistance.md).

## 8. Next steps

- TD 3: cost of each configuration (single model, 2-of-3, 3-of-5, reference check) for the uses of the routing rule.
- Add to the routing rule the check proposed by Pair B: a consensus on 0 triggers a `COUNT(*)` of the filtered rows.
- A second member reruns the step 2 scripts on another machine.
- Pairs A and B write the four missing cross-reviews (section 5).
