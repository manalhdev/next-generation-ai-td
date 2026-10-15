# Access checks (preparation, deadline Sunday 18 October 2026)

Each member runs once, from the repository root, with their own keys in environment variables:

    python3 check_access.py | tee ready-for-td1.txt

`ready-for-td1.txt` is git-ignored by the kit. Copy only the OK/KO lines below (never a key).
A check costs 3 Groq + 2 OpenRouter calls, counted outside the 100-cell base batch.

| Date | Member | Local checks | Models OK | KO details (model id, HTTP status, message) | Remaining allowance noted |
|---|---|---|---|---|---|
| 2026-10-16 | Manal Hassan | 4/4 OK (python 3.13.9, db sha256 0077e235…3398fec2, sqlite3 3.51.0, csv) | 0/5 | Groq x3 (gpt-oss-120b, gpt-oss-20b, qwen3.8-27b): HTTP 401 `invalid_api_key`. OpenRouter x2 (north-mini-code:free, dots-3-note-preview:free): HTTP 401 `Missing Authentication header` | n/a (requests rejected at authentication) |

Attempt 1 analysis (2026-10-16). *Observation:* Groq received a key and rejected it; OpenRouter received no key.
*Hypothesis:* the Groq variable held a revoked or mistyped key (the first key was revoked after being exposed in a chat),
and `OPENROUTER_API_KEY` was not set in that shell. *Action:* recreate both keys, re-export, check prefix/length, re-run.
