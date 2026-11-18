# Next-Generation AI — TD repository

ESILV, Data & AI, year 4. Module *Next-Generation AI* (Trustworthy Generative AI). TD 1 to TD 3, one repository per sub-group.

## Sub-group

- Sub-group: 1
- Members (GitHub account): Manal Hassan (manalhdev), axel12334556, ines729, Marieseka, TasB (TazBrks), Daiki4529, lorentejla

| Member | TD 1 work |
|---|---|
| manalhdev | repository and security setup; references C10, C17, C18; cross-check of C15, C16, C19; model C run; verification tools |
| axel12334556 | references C02, C13, C14; cross-check of C08, C09, C11; model A run; the 22 failure explanations |
| ines729 | references C03, C06, C07; cross-check of C01, C05, C12; model B run |
| Marieseka | references C01, C05, C12; cross-check of C04, C20; model D run |
| TasB | references C15, C16, C19; cross-check of C02, C13, C14; model E run; `.gitattributes` for data files |
| Daiki4529 | references C04, C20; cross-check of C03, C06, C07; trace consolidation |
| lorentejla | references C08, C09, C11; cross-check of C10, C17, C18; five-model summary |

Details per reference: `td1/verifications-td1.md`. Details per session: `reports/`.

## Environment

- Course pack `2026-10-18-students-1`.
- Database `data/boutique.sqlite`, SHA-256 `0077e235adc2ca647b484e3083c98a6d7cae3ef3655ce366a299caf13398fec2`.
- Python 3.10 or later, run on macOS and Windows. Free Groq and OpenRouter accounts only, no credits.
- Models and call parameters are read from `modeles-autorises.json`. TD 1 used the five proposed models, with no replacement.

## Setup from a fresh clone

```bash
git clone https://github.com/manalhdev/next-generation-ai-td.git
cd next-generation-ai-td
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pre-commit install
cp .env.example .env    # fill in the two keys; .env is git-ignored
```

Windows: `.venv\Scripts\python.exe` instead of `python3`, `copy` instead of `cp`.

## Replay TD 1

Offline, no key needed:

```bash
python3 verify-data.py                       # database integrity
python3 tools/compare_references.py          # runs the 20 reference queries, compares with published values
python3 tools/build_verifications.py         # td1/verifications-td1.md and td1/queries-td1.sql
python3 skeleton-multi-llm-en.py --replay traces-td1.csv --state /tmp/replay.jsonl --out /tmp/replay.csv
python3 tools/td1_consolidate.py             # traces-td1.*, comparison CSV, results/pivot-td1.md
```

The `--replay` line re-scores the stored SQL of the 100 calls; its rows are labelled `replay`.

Real calls, as run on 21 October 2026, one operator at a time:

```bash
python3 check_access.py
python3 skeleton-multi-llm-en.py --run --models groq:openai/gpt-oss-120b --state state-A.jsonl --out traces-A.csv --pause 8
python3 skeleton-multi-llm-en.py --run --models groq:openai/gpt-oss-20b --state state-B.jsonl --out traces-B.csv --pause 8
python3 skeleton-multi-llm-en.py --run --models openrouter:cohere/north-mini-code:free --state state-C.jsonl --out traces-C.csv
python3 skeleton-multi-llm-en.py --run --models groq:qwen/qwen3.8-27b --state state-D.jsonl --out traces-D.csv --pause 8
python3 skeleton-multi-llm-en.py --run --models openrouter:dots-studio/dots-3-note-preview:free --state state-E.jsonl --out traces-E.csv
```

`--pause 8` keeps Groq under its free limit of 8,000 tokens per minute.

## TD 2 (no network call)

```bash
python3 atelier-vote.py             # our vote_k_sur_n on the four synthetic examples
python3 tools/td2_vote_table.py     # 2-of-3 against 3-of-5 on the twenty questions (table in reports/td2.md)
python3 tools/td2_family_rates.py   # TD 1 accuracy per question family -> results/family-rates-td2.md
python3 atelier-routage.py          # routing simulator adapted to td2/routing-rule.md
```

## Contents

| Path | Content |
|---|---|
| `reference-td1.csv` | The 20 reference queries and values, who wrote and who checked each |
| `td1/queries-td1.sql` | The same 20 queries in one readable file |
| `td1/verifications-td1.md` | Who wrote and who checked each reference, method, status, check scripts |
| `td1/crosscheck_*.py`, `refs_TasB.py` | The cross-check scripts |
| `traces-A.csv` to `traces-E.csv`, `state-A.jsonl` to `state-E.jsonl` | Raw traces of each operator |
| `traces-td1.csv`, `traces-td1.jsonl` | All 100 calls merged |
| `model-question-comparison-en.csv` | Final result per model and question, with the cause of each failure |
| `results/pivot-td1.md`, `results/families-td1.md` | Models x questions view, results by question family |
| `five-model-summary-en.csv` | Index, prices, access and results per model |
| `prompts-en.md` | Prompt sent to the models |
| `prompts-ai-assistance.md` | Prompts used for coding assistance |
| `reports/` | One report per session |
| `prep/` | Preparation: access checks, work split, draft reference script |
| `tools/` | Consolidation and verification scripts |
| `kit-docs/` | Assessment, hand-in rules, templates, published TD 1 reference values |

Other files come from the course kit (`KIT-README.md`). `check_access.py` and `skeleton-multi-llm-en.py` were changed only to read keys from `.env`.

## Status

| Session | Status |
|---|---|
| Preparation | Done, 5/5 models reachable on 2026-10-16 |
| TD 1 (21 Oct) | 20/20 references equal to the published values; 100 real calls, no access error, 78/100 correct (A 20, B 19, D 14, E 13, C 12); 22 failures explained; five-model summary filled; report in `reports/td1.md` |
| TD 2 (18 Nov) | Not started |
| TD 3 (11 Dec) | Not started |

Open items: `td1/crosscheck_lorentejla.py`, cited as the check of C10, C17, C18, is not in the repository yet; three explanations to correct (see `reports/td1.md`, section 4).
