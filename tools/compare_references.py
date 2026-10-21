"""Compare reference-td1.csv with the values published by the instructors during TD 1.

Usage (from the repository root):  python3 tools/compare_references.py
Source of the published values: kit-docs/reference-values-td1-en.md (course site, 21 Oct 2026).
"""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

published = dict(re.findall(r"^\| (C\d\d) \|.*?\| (\d+) \|[^|]*\|\s*$",
                            (ROOT / "kit-docs" / "reference-values-td1-en.md").read_text(encoding="utf-8"), re.M))
with open(ROOT / "reference-td1.csv", newline="", encoding="utf-8") as f:
    ours = {r["case_id"]: r for r in csv.DictReader(f)}

counts = {"OK": 0, "DIFFERENT": 0, "MISSING": 0}
for case_id in sorted(published):
    row = ours.get(case_id, {})
    value = (row.get("revenue_cents") or "").strip()
    status = "MISSING" if not value else ("OK" if value == published[case_id] else "DIFFERENT")
    if status == "MISSING" or not (row.get("sql") or "").strip():
        status = "MISSING" if not value else status + " (no query)"
    counts[status.split()[0]] += 1
    print(f"{case_id}  ours={value or '-':>8}  published={published[case_id]:>8}  {status:<16} "
          f"written_by={row.get('written_by', '')}  checked_by={row.get('checked_by', '')}")
print(f"\n{counts['OK']} OK, {counts['DIFFERENT']} different, {counts['MISSING']} missing, out of {len(published)}")
