# Access checks (preparation, deadline Sunday 18 October 2026)

Each member runs once, from the repository root, with their own keys in environment variables:

    python3 check_access.py | tee ready-for-td1.txt

`ready-for-td1.txt` is git-ignored by the kit. Copy only the OK/KO lines below (never a key).
A check costs 3 Groq + 2 OpenRouter calls, counted outside the 100-cell base batch.

| Date | Member | Local checks | Models OK | KO details (model id, HTTP status, message) | Remaining allowance noted |
|---|---|---|---|---|---|
| TODO | | | /5 | | |
