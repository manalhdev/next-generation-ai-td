# TD 1 report — Comparing models on the same questions

Sub-group 1. Session of 21 October 2026. Course pack `2026-10-18-students-1` (code, database, questions and model list identical to the 14 October kit used for the preparation).

Members (GitHub accounts): Manal Hassan (manalhdev), axel12334556, ines729, Marieseka, TasB (TazBrks), Daiki4529, lorentejla.

## 1. Preparation (before 18 October)

| Date | Who | What | Evidence |
|---|---|---|---|
| 2026-10-16 | Manal Hassan | Downloaded the 14 October kit, venv + `requests`, `verify-data.py` gives `"ok": true` | [README](../README.md) |
| 2026-10-16 | Manal Hassan | Offline demo run (**simulated** models, not real calls) | [prep/demo/](../prep/demo/) |
| 2026-10-16 | Manal Hassan (AI-assisted) | Draft of the 20 reference queries, SQL vs CSV cross-check | [prep/draft_references.py](../prep/draft_references.py), [prompts-ai-assistance.md](../prompts-ai-assistance.md) |
| 2026-10-16 | Manal Hassan | Moodle "TD1 Preparation Check" answered | Moodle |
| 2026-10-16 | Manal Hassan | `check_access.py`: 0/5 (HTTP 401, empty or wrong keys), then 2/5 (Groq 401), then **5/5 OK** | [prep/access-checks.md](../prep/access-checks.md) |
| 2026-10-16 | Manal Hassan | Public repository created | this repository |
| 2026-10-21 | ines729 | `check_access.py` on Windows after installing Git: 5/5 OK | [prep/access-checks.md](../prep/access-checks.md) |

Model availability: the free Ling route of an earlier kit had been replaced by `cohere/north-mini-code:free` in the 14 October kit. We observed no other change: the five proposed models answered on 16 and 21 October, and we used them all, with no replacement.

## 2. What we attempted and completed

- **Step 1, references.** The twenty questions were ranked by difficulty and shared among the seven members ([prep/td1-plan.md](../prep/td1-plan.md)). Each query was written by one member and cross-checked by another with a different method (Python on the CSV files, or a second SQL query). All twenty values are equal to the values published during the session; the published table was only used to compare.
- **Step 2, models.** 100 base cells: 5 models x 20 questions, one operator at a time, with the kit prompt unchanged ([prompts-en.md](../prompts-en.md)). All 100 calls are real calls, all returned HTTP 200, no retry was needed (`attempts` = 1 everywhere), and each question has a single prompt fingerprint shared by the five models.
- **Step 3, analysis.** The traces were merged, the comparison CSV has one row per model and question, and each of the 22 failures has an explanation read from the returned SQL. The five-model summary is filled.
- **Step 4, plenary.** The models x questions pivot was shown.

## 3. What worked

| File | Content |
|---|---|
| [reference-td1.csv](../reference-td1.csv), [td1/queries-td1.sql](../td1/queries-td1.sql) | The 20 queries and values, author and checker of each |
| [td1/verifications-td1.md](../td1/verifications-td1.md) | Who wrote and who checked each reference, method, check scripts |
| [traces-td1.csv](../traces-td1.csv), [traces-td1.jsonl](../traces-td1.jsonl) | The 100 calls; raw files of each operator: `traces-A.csv` to `traces-E.csv`, `state-A.jsonl` to `state-E.jsonl` |
| [model-question-comparison-en.csv](../model-question-comparison-en.csv) | Final result and explanation per model and question |
| [results/pivot-td1.md](../results/pivot-td1.md), [results/families-td1.md](../results/families-td1.md) | Models x questions view, results by question family |
| [five-model-summary-en.csv](../five-model-summary-en.csv) | Public index, prices, access and results per model |

Results of the batch (`tools/compare_references.py` and `tools/td1_consolidate.py` replay them):

| Model (route) | Correct | Wrong value | Invalid SQL | Access error | Age questions | Other questions | Median latency |
|---|---|---|---|---|---|---|---|
| `openai/gpt-oss-120b` (Groq) | 20/20 | 0 | 0 | 0 | 10/10 | 10/10 | 1.2 s |
| `openai/gpt-oss-20b` (Groq) | 19/20 | 1 | 0 | 0 | 9/10 | 10/10 | 0.7 s |
| `qwen/qwen3.8-27b` (Groq) | 14/20 | 5 | 1 | 0 | 5/10 | 9/10 | 0.6 s |
| `dots-studio/dots-3-note-preview:free` (OpenRouter) | 13/20 | 7 | 0 | 0 | 3/10 | 10/10 | 3.4 s |
| `cohere/north-mini-code:free` (OpenRouter) | 12/20 | 6 | 2 | 0 | 2/10 | 10/10 | 2.7 s |

78 cells out of 100 are correct. The questions on a period or a product list alone are answered correctly by every model, except one invalid query of Qwen on C06.

## 4. What failed, evidence and causes

**Observations.** The 22 failures are listed with their cell identifier (`provider:model:case`) and their evidence in the `explanation` column of [model-question-comparison-en.csv](../model-question-comparison-en.csv). 21 of them are on the ten questions with an age condition; the other one is Qwen on C06.

| Cause read from the returned SQL | Cells |
|---|---|
| Contradictory conditions on the birthday (`<=` and `>` the same value), so the value is 0 | Qwen C15, Dots C08, C10 |
| One branch of the completed age missing: customers born the year before, whose birthday is after the reference date, are forgotten | Cohere C02, Dots C15, C17 |
| Age filter that keeps everybody or "25 or more" instead of "exactly 25" | Cohere C19, Qwen C19, Dots C16 |
| Wrong bounds or boundary day of the age | GPT-OSS 20B C02 (no 25-year offset), Cohere C15, Qwen C10 (24 instead of 26), Qwen C17, Dots C02 (age in days with 365.25-day years), Dots C09 |
| Wrong reference date or period added | Qwen C09 (order date instead of the reference date), Cohere C09 (period invented after the last order), Cohere C10 (dates built as strings) |
| Invalid SQL | Cohere C08, C11 (alias declared inside `WHERE`), Qwen C06 (`COALESE` typo) |
| Wrong string slicing | Cohere C17 (`'MM-YYYY'` compared with `'MM-DD'`) |

For most wrong values, the explanation replays the query on the database: the gap with the reference is exactly the revenue of the customers wrongly excluded or included. For example, for Dots on C02 the gap of 135000 cents is the revenue of the customer born on 2001-09-25.

**Hypotheses (not tested).** The convention of the completed age needs two cases (year difference 25 with the birthday reached, or 26 with the birthday not reached); the smaller models often write only one case, or compare the same day twice. Reasoning is disabled for Qwen, Cohere and Dots in `modeles-autorises.json`, which may play a role; one run per cell does not allow us to check it.

**No failed access.** All 100 calls returned HTTP 200, so the batch contains no access error to distinguish from a wrong answer; an instructor-supplied example is needed for that point. Missing measurements stay empty: `cost_native` is empty for the 60 Groq cells (Groq returns no native cost) and is 0 for the 40 OpenRouter `:free` cells.

**Incomplete.**
- lorentejla's cross-check of C10, C17, C18 cites `td1/crosscheck_lorentejla.py`, which is not in the repository: these three references are correct but their check is marked incomplete (17/20 complete in [td1/verifications-td1.md](../td1/verifications-td1.md)).
- Five-model summary: public index and paid price are N/A for Cohere and Dots (not in the 28 September portfolio), and the paid price is N/A for GPT-OSS 20B and Qwen (no paid route documented there).
- Three explanations need a correction, found by replaying the queries: Dots C16 (the `AND NOT (...)` clause is not a no-op, it wrongly excludes the customer born on 2001-09-25), Dots C17 (operator precedence is not the cause, the birthday condition imposed on the customers born in 2000 is), Qwen C06 (the sentence on reasoning is a hypothesis, not an observation).

## 5. Decisions, limits and uncertainty

**Decisions.**
- The twenty references were shared by difficulty, hardest first, and every reference was checked by another member with a different method.
- Groq operators used `--pause 8` to stay under the free limit of 8,000 tokens per minute; no HTTP 429 occurred.
- The prompt of the kit was kept unchanged, and the five proposed models were kept, so the gaps are attributable to the models.
- Two runs stopped before any call and were simply restarted: model D at first missed its `GROQ_API_KEY` in the operator's environment, and model E first ran with an outdated `reference-td1.csv`. Neither sent a request.
- Keys stay out of the repository: `.env` is git-ignored and loaded with `python-dotenv`, and a gitleaks pre-commit hook checks every commit.

**Limits and uncertainty.** Twenty questions and one run per cell at temperature 0 give an observation of this batch, not an accuracy rate or a ranking of the models; the variability between runs was not measured. The results depend on the free routes as they were on 21 October. Latencies come from one network and one sample per cell.

**Replayed and synthetic data.** `prep/demo/traces-demo.*` are simulated rows of the kit's demo mode and are not used in any result. The `--replay` command of the README re-scores the stored SQL offline (rows labelled `replay`) only to check reproducibility. The draft script of `prep/` was used only to compare, never as a reference value.

## 6. Division of work

| Member | Role | Contribution |
|---|---|---|
| manalhdev (Manal Hassan) | C, coordination | Repository set-up and security, verification and consolidation tools, references C10, C17, C18, cross-check of C15, C16, C19, model C run, this report |
| axel12334556 | A | References C02, C13, C14 with a check script, cross-check of C08, C09, C11, model A run, the 22 failure explanations |
| ines729 | B | References C03, C06, C07, cross-check of C01, C05, C12, model B run |
| Marieseka | D | References C01, C05, C12, cross-check of C04, C20, model D run |
| TasB (TazBrks) | E | References C15, C16, C19, cross-check of C02, C13, C14, model E run, `.gitattributes` keeping the data files byte-identical on Windows |
| Daiki4529 | F | References C04, C20, cross-check of C03, C06, C07, consolidation of the traces, comparison CSV and pivot |
| lorentejla | G | References C08, C09, C11, cross-check of C10, C17, C18, five-model summary |

AI-assisted code and its prompts are listed in [prompts-ai-assistance.md](../prompts-ai-assistance.md).

## 7. Next steps and help needed

- lorentejla commits `td1/crosscheck_lorentejla.py`; the three explanations above are corrected.
- Five-model summary: look for official pages for Cohere and Dots, or keep N/A with the reason.
- TD 2: code `vote_k_sur_n` and test it with `atelier-vote.py`; write the routing rule from this table (age questions to GPT-OSS 120B first, other families to a faster model, with the reference check kept).
- Help: our batch contains no failed access; we would like the instructor's example to explain that case.
