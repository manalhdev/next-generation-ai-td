# TD 2 report — The quorum, then the routing rule

Sub-group 1. Session of 18 November 2026. Course pack `2026-11-18-students-5` (code identical to the TD 1 kit; documents updated). No new network call: everything below uses the stored TD 1 traces ([traces-td1.csv](../traces-td1.csv): 100 real cells, 5 models x C01 to C20, one attempt each, all HTTP 200) and [reference-td1.csv](../reference-td1.csv). The prompts are unchanged since TD 1 ([prompts-en.md](../prompts-en.md)): no model was called in TD 2.

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

### The method

`Orchestrateur.vote_k_sur_n` in [skeleton-multi-llm-en.py](../skeleton-multi-llm-en.py) (line 609) follows the five rules of the contract:

1. it checks that k is a strict majority (`n // 2 < k <= n`), otherwise `ValueError`;
2. it refuses two proposals with the same `(provider, model_requested)` with `ValueError`: a duplicate is not a second vote;
3. only proposals with `verdict == "executed"` and a value (`is not None`, so a value of 0 still votes) are counted; an error stays in n without a vote;
4. a value reaching k votes is returned with its votes and the agreeing models;
5. otherwise it abstains: `value` is `None`, `votes` is the largest count (0 if nobody voted). It never picks a value without a majority.

Checks run with `python3 atelier-vote.py`: the four synthetic examples give agreement → 100 (2 votes), disagreement → abstain (1), unavailable → abstain (1), wrong consensus → 0 (2 votes, wrong against the reference 100). k = 1 or k = 4 out of 3 and a duplicated pair raise `ValueError`; two errors out of three abstain.

### The twenty decisions, 2-of-3 against 3-of-5

Decisions computed by our `vote_k_sur_n` on `traces-td1.csv` (nature real, last attempt per model, same selection as `atelier-vote.py`), then compared with `reference-td1.csv`; the reference is compared only after each decision. Command: `python3 td2/A-quorum/td2_vote_table.py`.

- 2-of-3: the fixed panel of `atelier-vote.py`, gpt-oss-120b (Groq), Cohere north-mini-code (OpenRouter), Qwen 3.8 27B (Groq), k = 2.
- 3-of-5: the five TD 1 models (the panel plus gpt-oss-20b and Dots), k = 3.

| Case | Reference | 2-of-3 decision | value | votes | = ref | 3-of-5 decision | value | votes | = ref | Changed | Values of the five models |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C01 | 792800 | consensus | 792800 | 3 | yes | consensus | 792800 | 5 | yes |  | 120B=792800, Cohere=792800, Qwen=792800, 20B=792800, Dots=792800 |
| C02 | 590320 | consensus | 590320 | 2 | yes | abstain |  | 2 | n/a | **yes** | 120B=590320, Cohere=321340, Qwen=590320, 20B=0, Dots=455320 |
| C03 | 936350 | consensus | 936350 | 3 | yes | consensus | 936350 | 5 | yes |  | 120B=936350, Cohere=936350, Qwen=936350, 20B=936350, Dots=936350 |
| C04 | 2826250 | consensus | 2826250 | 3 | yes | consensus | 2826250 | 5 | yes |  | 120B=2826250, Cohere=2826250, Qwen=2826250, 20B=2826250, Dots=2826250 |
| C05 | 38480 | consensus | 38480 | 3 | yes | consensus | 38480 | 5 | yes |  | 120B=38480, Cohere=38480, Qwen=38480, 20B=38480, Dots=38480 |
| C06 | 0 | consensus | 0 | 2 | yes | consensus | 0 | 4 | yes |  | 120B=0, Cohere=0, Qwen=error, 20B=0, Dots=0 |
| C07 | 13970 | consensus | 13970 | 3 | yes | consensus | 13970 | 5 | yes |  | 120B=13970, Cohere=13970, Qwen=13970, 20B=13970, Dots=13970 |
| C08 | 605580 | consensus | 605580 | 2 | yes | consensus | 605580 | 3 | yes |  | 120B=605580, Cohere=error, Qwen=605580, 20B=605580, Dots=0 |
| C09 | 487980 | consensus | 0 | 2 | **no** | abstain |  | 2 | n/a | **yes** | 120B=487980, Cohere=0, Qwen=0, 20B=487980, Dots=47900 |
| C10 | 558980 | abstain |  | 1 | n/a | abstain |  | 2 | n/a |  | 120B=558980, Cohere=0, Qwen=119410, 20B=558980, Dots=0 |
| C11 | 446690 | consensus | 446690 | 2 | yes | consensus | 446690 | 4 | yes |  | 120B=446690, Cohere=error, Qwen=446690, 20B=446690, Dots=446690 |
| C12 | 1666490 | consensus | 1666490 | 3 | yes | consensus | 1666490 | 5 | yes |  | 120B=1666490, Cohere=1666490, Qwen=1666490, 20B=1666490, Dots=1666490 |
| C13 | 107740 | consensus | 107740 | 3 | yes | consensus | 107740 | 5 | yes |  | 120B=107740, Cohere=107740, Qwen=107740, 20B=107740, Dots=107740 |
| C14 | 0 | consensus | 0 | 3 | yes | consensus | 0 | 5 | yes |  | 120B=0, Cohere=0, Qwen=0, 20B=0, Dots=0 |
| C15 | 168680 | abstain |  | 1 | n/a | abstain |  | 2 | n/a |  | 120B=168680, Cohere=314020, Qwen=0, 20B=168680, Dots=138920 |
| C16 | 376740 | consensus | 376740 | 3 | yes | consensus | 376740 | 4 | yes |  | 120B=376740, Cohere=376740, Qwen=376740, 20B=376740, Dots=1367540 |
| C17 | 258180 | abstain |  | 1 | n/a | abstain |  | 2 | n/a |  | 120B=258180, Cohere=197080, Qwen=248490, 20B=258180, Dots=152730 |
| C18 | 62480 | consensus | 62480 | 3 | yes | consensus | 62480 | 5 | yes |  | 120B=62480, Cohere=62480, Qwen=62480, 20B=62480, Dots=62480 |
| C19 | 1990 | abstain |  | 1 | n/a | consensus | 1990 | 3 | yes | **yes** | 120B=1990, Cohere=71640, Qwen=83580, 20B=1990, Dots=1990 |
| C20 | 1106090 | consensus | 1106090 | 3 | yes | consensus | 1106090 | 5 | yes |  | 120B=1106090, Cohere=1106090, Qwen=1106090, 20B=1106090, Dots=1106090 |

| Quorum | Consensus | of which right | of which wrong | Abstentions |
|---|---|---|---|---|
| 2-of-3 | 16 | 15 | 1 (C09) | 4 (C10, C15, C17, C19) |
| 3-of-5 | 15 | 15 | 0 | 5 (C02, C09, C10, C15, C17) |

The decision changes on three questions: C02, C09 and C19.

Commentary:

- **C09, wrong consensus avoided.** Cohere and Qwen, two members of the fixed panel, return the same wrong value 0, so the 2-of-3 quorum keeps it. With five models, the wrong value 0 and the right value 487980 (120B, 20B) each reach only 2 votes out of 5: the 3-of-5 quorum abstains. It does not find the right answer, but it no longer shows a wrong one as certain. This is the case explained in Step 2.
- **C02, right answer lost.** 120B and Qwen agree on the reference, so 2-of-3 is right. Cohere, 20B and Dots each return a different wrong value; they do not agree with each other, but they keep the right value at 2 votes out of 5, so 3-of-5 abstains. A stricter quorum costs answers where the extra models are weak.
- **C19, right answer gained.** The panel is split three ways (1990, 71640, 83580), so 2-of-3 abstains. 20B and Dots join 120B on the reference, so 3-of-5 reaches 3 votes.
- All three changes are on questions with an age at a reference date (family F2). On period and product questions (C01, C03 to C07, C12 to C14, C20) both quorums agree, and agree with the reference.

What we draw from it: on our batch, 3-of-5 removes the only wrong consensus of 2-of-3 and adds none, with the same number of right answers (15), for five calls instead of three. An abstention is a visible "we do not know", sent to a reference or a review; a wrong consensus is a silent error. This supports the routing rule of Pair C: 2-of-3 is enough on F1 and F3, 3-of-5 with abstention sent to review on the age families. Limits: twenty questions and one run per cell; a consensus is still not a proof, since on C09 two models were wrong together, and with five models three could be too.

**Check by Pair C at the merge.** Manal Hassan recomputed the twenty decisions independently (`python3 td2/C-routing/analyse_votes.py`, [vote-td2.md](../td2/C-routing/vote-td2.md), [vote-td2.csv](../td2/C-routing/vote-td2.csv)) and ran `atelier-vote.py` ([atelier-vote-td2.txt](../td2/C-routing/atelier-vote-td2.txt)): same decisions. Of the two versions of `vote_k_sur_n` received, the committed one (c01e9a1) is kept: it reads the proposals as objects, which is what `atelier-vote.py` passes. Review: [td2/A-quorum/review-2.md](../td2/A-quorum/review-2.md).

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
- A consensus on 0 should be treated as suspect when a non-zero figure is expected: count the filtered rows (`COUNT(*)`) or keep `NULL` without `COALESCE`; an empty set over a non-empty population leads to abstention or review. This check is now part of the routing rule (section 4), with the reference query to confirm an empty set, because the true zeros of C06 and C14 also come from an empty filter.
- The errors of the models are not independent (same prompt, same schema, same date trap), while a quorum assumes independent errors.

## 4. Step 3 — The routing rule (Pair C)

- TD 1 rates per family: [family-rates-td2.md](../td2/C-routing/family-rates-td2.md) (`python3 td2/C-routing/family_rates.py`).
- The one-page rule, the scenario table R1 to R5, the changes made to the simulator and the full analysis of the priority order of `choose`: [td2/C-routing/routing-rule.md](../td2/C-routing/routing-rule.md).
- Simulator outputs: before adaptation [routing-before.txt](../td2/C-routing/routing-before.txt), after [routing-after.txt](../td2/C-routing/routing-after.txt) (`python3 atelier-routage.py`).

Main findings:

- Period (F1) and product (F3) questions: four or five models are at 100 % in TD 1, so gpt-oss-20b goes first and a dashboard needs no check, except for a value of 0.
- Every question with an age at a reference date (8 cells): only gpt-oss-120b is at 100 % (8/8); gpt-oss-20b fails C02 with a silent wrong value, Qwen, Cohere and Dots fail 4, 7 and 6 of them.
- The 2-of-3 panel is not enough on the age families: on C09, two panel members (Cohere and Qwen) returned the same wrong value 0. Customer figures on these families use a 3-of-5 quorum, payouts a reference query and a human review.
- A value of 0 is checked before delivery, as Pair B proposed: a `COUNT(*)` of the filtered rows, then the reference query when no row is kept. In TD 1, the seven wrong zeros and the true zeros of C06 and C14 all come from a filter that keeps no row, so the count alone does not decide; the reference query does.

**Priority order of the supplied `choose`.** The branches are tested in a fixed order: available included capacity (`cash == 0`, which covers a free route and an already paid subscription with `allocation > 0`), then deferral to an exhausted free route that refills before `deadline_minutes` when the request can wait, then a paid route within the budget, then abstention. An available subscription is therefore selected before any deferral: it spends no new money, it answers now, and a deferral is uncertain (a reset time is only an announcement, availability must be measured again at wake-up, the deadline can be missed). The priority should be reversed when the subscription capacity is scarce: an allocation for the period, or a cap shared by the team, that must be kept for requests that cannot wait. Then a request that can wait, with a reliable free refill before its deadline, should defer; in the code, the `waiting` branch would be tested first when `can_wait` is true and the remaining allocation is under a reserve threshold. Our rule has no subscription: on F2, the simulator waits for the free Groq refill before paying the OpenRouter route.

Limits: twenty questions and one run per cell; some families have one or two cells only (F2b: C10, C18), so their rates are weak evidence. Resource availability and refill times in the simulator are scenario assumptions, not measurements. The paid cost uses the portfolio price of 2026-09-29 and the TD 1 median tokens.

## 5. Internal cross-review

Before the report is finalised, each pair walks the other members through its code, SQL and decisions. Each pair folder holds the two reviews written by the other pairs.

| Pair reviewed | review-1.md | review-2.md |
|---|---|---|
| A, quorum | [by Pair B](../td2/A-quorum/review-1.md), Tasnim: the logic keeps to the contract; one point to verify, settled, and two minor details | [by Pair C](../td2/A-quorum/review-2.md): accepted, the vote version that reads objects is kept |
| B, consensus | [by Pair A](../td2/B-consensus/review-1.md): to be written | [by Pair C](../td2/B-consensus/review-2.md): accepted, every figure rerun on the database |
| C, routing | [by Pair A](../td2/C-routing/review-1.md): to be written | [by Pair B](../td2/C-routing/review-2.md): to be written |

Pair B also checked its own Step 2: [td2/B-consensus/internal-check.md](../td2/B-consensus/internal-check.md) (Julia, Marie).

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
- A second member reruns the step 2 scripts on another machine.
- Pairs A and B write the three missing cross-reviews (section 5).
