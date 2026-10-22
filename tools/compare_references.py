"""Run the twenty reference queries and compare them with the values published during TD 1.

Usage (from the repository root):  python3 tools/compare_references.py
For each question: the query of reference-td1.csv is run on data/boutique.sqlite (read-only), and its
result must equal both the value recorded in reference-td1.csv and the published value.
Source of the published values: kit-docs/reference-values-td1-en.md (course site, 21 Oct 2026).
"""
import csv
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

published = dict(re.findall(r"^\| (C\d\d) \|.*?\| (\d+) \|[^|]*\|\s*$",
                            (ROOT / "kit-docs" / "reference-values-td1-en.md").read_text(encoding="utf-8"), re.M))
with open(ROOT / "reference-td1.csv", newline="", encoding="utf-8") as f:
    ours = {r["case_id"]: r for r in csv.DictReader(f)}
con = sqlite3.connect(f"file:{ROOT / 'data' / 'boutique.sqlite'}?mode=ro", uri=True)

counts = {"OK": 0, "DIFFERENT": 0, "MISSING": 0}
for case_id in sorted(published):
    row = ours.get(case_id, {})
    sql = (row.get("sql") or "").strip()
    value = (row.get("revenue_cents") or "").strip()
    try:
        executed = str(con.execute(sql).fetchone()[0]) if sql else "-"
    except Exception as exc:
        executed = f"error: {exc}"
    if not sql or not value:
        status = "MISSING"
    elif executed == value == published[case_id]:
        status = "OK"
    else:
        status = "DIFFERENT"
    counts[status] += 1
    print(f"{case_id}  query={executed:>8}  recorded={value or '-':>8}  published={published[case_id]:>8}  {status:<9} "
          f"written_by={row.get('written_by', '')}  checked_by={row.get('checked_by', '')}")
print(f"\n{counts['OK']} OK, {counts['DIFFERENT']} different, {counts['MISSING']} missing, out of {len(published)}")
