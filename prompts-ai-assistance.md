# AI coding assistance: prompts and decisions

The module accepts AI-assisted code if the prompts are kept and the decisions explained.
A model's numerical answer is never used as a reference value.

## 2026-10-16 — preparation (Claude Code, Claude Opus 5.5), Manal Hassan

**Prompt (translated from French):** "I have a new course called Next Generation AI; they asked us for a lot of
things — do them, and when you can't, guide me." Followed by the two instructor messages of 15 October
(hand-in rules, updated model list).

**What the assistant did:**
- downloaded the 14 October kit from the course site, created a venv, ran `verify-data.py` (ok) and
  `skeleton-multi-llm-en.py --demo` (simulated models only; output in `prep/demo/`, labelled simulated);
- built this repository layout, `README.md`, `prompts-en.md` (copied verbatim from the skeleton), the
  report draft and `prep/draft_references.py`.

**Decisions:**
- `prep/draft_references.py` writes the 20 draft queries to `prep/draft-reference-td1.csv` (git-ignored, so draft values are not public), **not** to
  `reference-td1.csv`: the protocol requires each reference to be written and independently checked by
  members during TD 1. The drafts are a starting point to compare against.
- Completed age is computed as year difference minus 1 when the month-day of the day is before the
  month-day of the birth date (protocol section 1). No customer is born on 29 February, so no leap-day
  convention is needed (checked with a query).
- Each SQL value is cross-checked by a pure-Python computation on the CSV files (no SQL). All 20 agree.
  Limit: both computations were written by the same assistant from the same reading of the conventions,
  so they are not independent on interpretation; a member must check the conventions by hand.
