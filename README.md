# Next-Generation AI (Trustworthy Generative AI) — TD repository

ESILV, Data & AI major, year 4 — module *Next-Generation AI*, Didier Parisot.
One shared public repository per sub-group, kept from TD 1 (21 Oct 2026) to TD 3 (11 Dec 2026).

## Sub-group

| | |
|---|---|
| Sub-group | **TODO: sub-group name / number** |
| Members (8) | TODO — Manal Hassan, …, …, …, …, …, …, … |

TD 1 roles (protocol allocation): A GPT-OSS 120B (Groq) · B GPT-OSS 20B (Groq) · C Cohere North Mini Code (OpenRouter) · D Qwen 3.8 27B (Groq) · E Dots 3 Note (OpenRouter) · F–H cross-check, traces, summaries. C and E use two different members' OpenRouter accounts.

| Role | Member |
|---|---|
| A | TODO |
| B | TODO |
| C | TODO |
| D | TODO |
| E | TODO |
| F | TODO |
| G | TODO |
| H | TODO |

## Course pack and environment

- Course pack: **2026-10-18-students-1** (student kit dated 18 October 2026; code, database and model selection identical to the 14 October kit, documents updated).
- Database `data/boutique.sqlite`, SHA-256 `0077e235adc2ca647b484e3083c98a6d7cae3ef3655ce366a299caf13398fec2` (seed 20260925), identical to `data/manifest.json`.
- Python 3.10+ (tested with 3.13.9 on macOS), virtual environment with `requests` (only needed by `check_access.py`).
- Free accounts only: Groq Free plan and OpenRouter `:free` routes. No credits purchased.

Required models (14 October kit):

| Provider | Exact model identifier |
|---|---|
| Groq, Free plan | `openai/gpt-oss-120b` |
| Groq, Free plan | `openai/gpt-oss-20b` |
| Groq, Free plan | `qwen/qwen3.8-27b` |
| OpenRouter | `cohere/north-mini-code:free` |
| OpenRouter | `dots-studio/dots-3-note-preview:free` |

## Reproduce

```bash
git clone <this repository URL> && cd <repository>
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install requests

# keys stay in your shell, never in a file of this repository
export GROQ_API_KEY="gsk_..."
export OPENROUTER_API_KEY="sk-or-v1-..."

python3 verify-data.py                      # database integrity, no network
python3 check_access.py --no-network        # local checks only
python3 check_access.py | tee ready-for-td1.txt   # 3 Groq + 2 OpenRouter calls (file is git-ignored)
python3 skeleton-multi-llm-en.py --demo     # simulated models, no key, no network
python3 prep/draft_references.py            # reference queries + independent CSV cross-check

# TD 1, one operator at a time (example: member A)
python3 skeleton-multi-llm-en.py --run --models groq:openai/gpt-oss-120b \
        --cases C01,C02,... --state state-A.jsonl --out traces-A.csv

# after all batches: merge traces, build the comparison CSV, the pivot and the family counts
python3 tools/td1_consolidate.py
```

Windows PowerShell: use `python` instead of `python3`, `.venv\Scripts\Activate.ps1`, `$env:GROQ_API_KEY = "..."` and `Tee-Object` instead of `tee`.

## Contents

| Path | Content |
|---|---|
| `reference-td1.csv` | TD 1 step 1: the twenty reference queries and values, with the member who checked each |
| `traces-td1.csv`, `traces-td1.jsonl` | TD 1 step 2: every attempt (errors and retries included), merged from per-operator files |
| `traces-*.csv`, `state-*.jsonl` | Raw per-operator files, kept as produced |
| `model-question-comparison-en.csv` | One final result per model × question, with explanation and trace pointer |
| `five-model-summary-en.csv` | Five models: public index, dated prices, access, results by family |
| `prompts-en.md` | System message and user template exactly as used |
| `prompts-ai-assistance.md` | Prompts used for AI coding assistance, and the decisions taken |
| `reports/td1.md`, `td2.md`, `td3.md` | Session reports |
| `tools/td1_consolidate.py` | Merges `traces-*.csv` / `state-*.jsonl` into `traces-td1.*`, writes the comparison CSV, `results/pivot-td1.md` and `results/families-td1.md` (AI-assisted, see `prompts-ai-assistance.md`) |
| `prep/` | Preparation work before TD 1: access checks, draft references, demo run (simulated) |
| `kit-docs/` | Assessment, hand-in page, syllabus and templates from the kit |
| everything else | The unmodified kit (`KIT-README.md` describes each file) |

## Status

| Step | Status |
|---|---|
| Preparation (kit, venv, integrity, offline demo) | done 2026-10-16 |
| Access check 5/5 models | Manal Hassan: 5/5 OK on 2026-10-16 (3rd attempt, see `prep/access-checks.md`); other members TODO |
| TD 1 (21 Oct) | in progress — hand-in by Sun 25 Oct 2026 23:59 |
| TD 2 (18 Nov) | not started |
| TD 3 (11 Dec) | not started |

Open blocks: none reported yet.
