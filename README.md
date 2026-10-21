# Next-Generation AI — TD repository

ESILV, Data & AI, year 4. Module *Next-Generation AI* (Trustworthy Generative AI). TD 1 to TD 3, one repository per sub-group.

## Sub-group

- Sub-group: TODO
- Members: Manal Hassan, TODO

| Role (TD 1) | Model | Member |
|---|---|---|
| A | `groq:openai/gpt-oss-120b` | TODO |
| B | `groq:openai/gpt-oss-20b` | TODO |
| C | `openrouter:cohere/north-mini-code:free` | TODO |
| D | `groq:qwen/qwen3.8-27b` | TODO |
| E | `openrouter:dots-studio/dots-3-note-preview:free` | TODO |
| F-H | cross-check, traces, summaries | TODO |

## Environment

- Course pack `2026-10-18-students-1`.
- Database `data/boutique.sqlite`, SHA-256 `0077e235adc2ca647b484e3083c98a6d7cae3ef3655ce366a299caf13398fec2`.
- Python 3.10 or later. Free Groq and OpenRouter accounts only, no credits.
- Models and call parameters are read from `modeles-autorises.json`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pre-commit install
cp .env.example .env    # fill in the two keys; .env is git-ignored
```

## Commands

```bash
python3 verify-data.py                  # database integrity
python3 check_access.py                 # 3 Groq + 2 OpenRouter calls
python3 skeleton-multi-llm-en.py --demo # simulated models, no network
python3 prep/draft_references.py        # draft reference queries, SQL vs CSV check

# one operator at a time, example for role A
python3 skeleton-multi-llm-en.py --run --models groq:openai/gpt-oss-120b \
        --cases C01,C02 --state state-A.jsonl --out traces-A.csv

python3 tools/td1_consolidate.py        # merge traces, comparison CSV, pivot
```

## Contents

| Path | Content |
|---|---|
| `reference-td1.csv` | Reference query and value for each question |
| `traces-td1.csv`, `traces-td1.jsonl` | Every model call, errors and retries included |
| `model-question-comparison-en.csv` | Final result per model and question |
| `five-model-summary-en.csv` | Index, prices, access and results per model |
| `prompts-en.md` | Prompt sent to the models |
| `prompts-ai-assistance.md` | Prompts used for coding assistance |
| `reports/` | One report per session |
| `prep/` | Preparation: access checks, draft reference script |
| `tools/` | Consolidation script |
| `kit-docs/` | Assessment, hand-in rules, templates |

Other files come from the course kit (`KIT-README.md`). `check_access.py` and `skeleton-multi-llm-en.py` were changed only to read keys from `.env`.

## Status

| Session | Status |
|---|---|
| Preparation | Done, 5/5 models reachable on 2026-10-16 |
| TD 1 (21 Oct) | In progress, due 25 Oct 23:59 |
| TD 2 (18 Nov) | Not started |
| TD 3 (11 Dec) | Not started |

Open blocks: none.
