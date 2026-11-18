# TD 2 report — The quorum, then the routing rule

Sub-group 1. Session of 18 November 2026. Course pack `2026-11-18-students-5` (code identical to the TD 1 kit; documents updated). No new network call: everything below uses the stored TD 1 traces.

Members (GitHub accounts): Manal Hassan (manalhdev), axel12334556, ines729, Marieseka, TasB (TazBrks), Daiki4529, lorentejla.

## 1. What we attempted and completed

| Step | Pair | Deliverable | Status |
|---|---|---|---|
| 1. k-of-n vote, 2-of-3 against 3-of-5 | A | `vote_k_sur_n` in `skeleton-multi-llm-en.py`, twenty-question table below | done |
| 2. Wrong consensus | B | case, SQL root cause, delta query on `data/boutique.sqlite` | to be completed by Pair B |
| 3. Routing rule | C | [td2/routing-rule.md](../td2/routing-rule.md), rates, simulator before and after | done |

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

Decisions computed by our `vote_k_sur_n` on `traces-td1.csv` (nature real, last attempt per model, same selection as `atelier-vote.py`), then compared with `reference-td1.csv`; the reference is compared only after each decision. Command: `python3 tools/td2_vote_table.py`.

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

## 3. Step 2 — The wrong consensus (Pair B)

To be completed by Pair B.

## 4. Step 3 — The routing rule (Pair C)

- TD 1 rates per family: [results/family-rates-td2.md](../results/family-rates-td2.md) (`python3 tools/td2_family_rates.py`).
- The one-page rule, the scenario table R1 to R5, the changes made to the simulator and the analysis of the priority order of `choose`: [td2/routing-rule.md](../td2/routing-rule.md).
- Simulator outputs: before adaptation [results/routing-before.txt](../results/routing-before.txt), after [results/routing-after.txt](../results/routing-after.txt) (`python3 atelier-routage.py`).

Main findings:

- Period (F1) and product (F3) questions: four or five models are at 100 % in TD 1, so gpt-oss-20b goes first and a dashboard needs no check.
- Every question with an age at a reference date (8 cells): only gpt-oss-120b is at 100 % (8/8); gpt-oss-20b fails C02 with a silent wrong value, Qwen, Cohere and Dots fail 4, 7 and 6 of them.
- The 2-of-3 panel is not enough on the age families: on C09, two panel members (Cohere and Qwen) returned the same wrong value 0. Customer figures on these families use a 3-of-5 quorum, payouts a reference query and a human review.

Limits: twenty questions and one run per cell; some families have one or two cells only (F2b: C10, C18), so their rates are weak evidence. Resource availability and refill times in the simulator are scenario assumptions, not measurements. The paid cost uses the portfolio price of 2026-09-29 and the TD 1 median tokens.

## 5. Division of work

| Pair | Members | Step |
|---|---|---|
| A | to be completed | 1 |
| B | to be completed | 2 |
| C | Manal Hassan, to be completed | 3 |

AI-assisted code and its prompts: [prompts-ai-assistance.md](../prompts-ai-assistance.md).

## 6. Next steps

To be completed at the cross-review.
