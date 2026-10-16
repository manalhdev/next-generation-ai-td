# Access checks (preparation, deadline Sunday 18 October 2026)

Each member runs once, from the repository root, with their own keys in environment variables:

    python3 check_access.py | tee ready-for-td1.txt

`ready-for-td1.txt` is git-ignored by the kit. Copy only the OK/KO lines below (never a key).
A check costs 3 Groq + 2 OpenRouter calls, counted outside the 100-cell base batch.

| Date | Member | Local checks | Models OK | KO details (model id, HTTP status, message) | Remaining allowance noted |
|---|---|---|---|---|---|
| 2026-10-16 | Manal Hassan | 4/4 OK (python 3.13.9, db sha256 0077e235…3398fec2, sqlite3 3.51.0, csv) | 0/5 | Groq x3 (gpt-oss-120b, gpt-oss-20b, qwen3.8-27b): HTTP 401 `invalid_api_key`. OpenRouter x2 (north-mini-code:free, dots-3-note-preview:free): HTTP 401 `Missing Authentication header` | n/a (requests rejected at authentication) |
| 2026-10-16 | Manal Hassan | 4/4 OK | 2/5 | OpenRouter north-mini-code:free and dots-3-note-preview:free: OK. Groq x3: HTTP 401 `invalid_api_key` | 2 OpenRouter calls consumed; Groq 0 (rejected) |
| 2026-10-16 | Manal Hassan | 4/4 OK | **5/5** | none: gpt-oss-120b, gpt-oss-20b, qwen3.8-27b (Groq) and north-mini-code:free, dots-3-note-preview:free (OpenRouter) all OK | 3 Groq + 2 OpenRouter calls consumed; TODO: read counters in the consoles |

Attempt 1 analysis (2026-10-16). *Observation:* Groq received a key and rejected it; OpenRouter received no key.
*Hypothesis:* the Groq variable held a revoked or mistyped key (the first key was revoked after being exposed in a chat),
and `OPENROUTER_API_KEY` was not set in that shell. *Action:* recreate both keys, re-export, check prefix/length, re-run.

Attempt 2 analysis (2026-10-16). *Observation:* a previous run showed both variables holding a placeholder text
(prefix `nouv…`, checked by prefix/length only, keys never displayed); after re-entering the keys with `read -s`,
OpenRouter passes, Groq still returns 401 `invalid_api_key`. *Hypothesis:* the Groq key entered is the revoked one
or was miscopied. *Action:* create a new Groq key, re-enter it, re-run once.

Attempt 3 (2026-10-16). New Groq key created and entered with `read -s`: **5/5 models OK, prerequisite met.**
Total spent by Manal's preparation, outside the 100-cell base batch: Groq 3 accepted calls, OpenRouter 4 accepted calls.
`ready-for-td1.txt` (git-ignored) and a screenshot are kept locally for the 14:00 opening check.

## Account allowances read on 2026-10-16 (Manal Hassan, after the 5/5 check)

**Groq, Free plan** (console → Settings → Limits, organisation limits, read 2026-10-16):

| Model | Requests/min | Requests/day | Tokens/min | Tokens/day |
|---|---|---|---|---|
| `openai/gpt-oss-120b` | 30 | 1K | 8K | 200K |
| `openai/gpt-oss-20b` | 30 | 1K | 8K | 200K |
| `qwen/qwen3.8-27b` | 30 | 1K | 8K | 200K |

Used so far: 3 accepted calls (one per model, from `check_access.py`). The Limits page shows caps, not consumption.

**OpenRouter** (Activity, past month, read 2026-10-16): 4 requests, 78 tokens, total spend **$0.00**,
models North Mini Code and Dots3-Note Preview only, one key `esilv-td`. No credits purchased.

**Planning note (hypothesis, to verify in TD 1).** The prompt is about 2.5K characters (≈ 600–700 tokens) and
the output cap is 1 000–1 024 tokens, reasoning included, so one call may count up to ≈ 1.7K tokens.
With an 8K tokens/minute cap, about 4–5 calls per minute fit, while the 3-second spacing allows up to 20.
A Groq operator running 20 questions in a row may therefore receive HTTP 429 on tokens per minute even though
requests/day is far from reached. If it happens: read `Retry-After`, wait, use the single allowed retry.
