"""Draft reference queries for TD 1 (AI-assisted, prepared 2026-10-16, BEFORE the session).

Each question gets:
  1. a SQLite SELECT run on data/boutique.sqlite opened read-only;
  2. an independent pure-Python computation on the CSV files (no SQL).
Both values must agree. This is a DRAFT: in TD 1 each query must still be
re-checked independently by a second member and validated with the instructor.

Usage (from the repository root):  python3 prep/draft_references.py
Writes prep/draft-reference-td1.csv (it does NOT overwrite reference-td1.csv).
"""
import csv
import sqlite3
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "boutique.sqlite"

# Completed age on day D (text 'YYYY-MM-DD...') of someone born on birth_date:
# year difference, minus 1 if the anniversary (month-day) has not yet occurred.
def age_sql(day_expr):
    return (f"(CAST(strftime('%Y', {day_expr}) AS INTEGER) - CAST(strftime('%Y', c.birth_date) AS INTEGER)"
            f" - (strftime('%m-%d', {day_expr}) < strftime('%m-%d', c.birth_date)))")

BASE = ("SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents "
        "FROM orders o JOIN product p ON p.product_id = o.product_id "
        "JOIN customers c ON c.customer_id = o.customer_id")

# (case_id, start, end, age_ref, age_at_order, products)
SPECS = [
    ("C01", "2026-03-01 00:00:00", "2026-06-01 00:00:00", None, False, None),
    ("C02", None, None, "2026-09-25", False, None),
    ("C03", "2026-01-01 00:00:00", "2026-07-01 00:00:00", None, False, "abc"),
    ("C04", "2026-01-01 00:00:00", "2026-10-01 00:00:00", None, False, None),
    ("C05", "2026-06-01 00:00:00", "2026-06-02 00:00:00", None, False, None),
    ("C06", "2025-01-01 00:00:00", "2026-01-01 00:00:00", None, False, None),
    ("C07", "2026-05-31 00:00:00", "2026-06-01 00:00:00", None, False, None),
    ("C08", None, None, "2026-09-24", False, None),
    ("C09", None, None, "2026-09-26", False, None),
    ("C10", None, None, None, True, None),
    ("C11", None, None, "2026-12-01", False, None),
    ("C12", None, None, None, False, "abc"),
    ("C13", "2026-04-01 00:00:00", "2026-05-01 00:00:00", None, False, "ac"),
    ("C14", "2026-10-01 00:00:00", "2026-12-01 00:00:00", None, False, "abc"),
    ("C15", "2026-03-01 00:00:00", "2026-06-01 00:00:00", "2026-09-25", False, None),
    ("C16", None, None, "2026-09-25", False, "abc"),
    ("C17", "2026-01-01 00:00:00", "2026-07-01 00:00:00", "2026-09-25", False, "abc"),
    ("C18", "2026-05-01 00:00:00", "2026-06-01 00:00:00", None, True, None),
    ("C19", "2026-09-01 00:00:00", "2026-10-01 00:00:00", "2026-09-25", False, "d"),
    ("C20", "2026-06-01 00:00:00", "2026-09-01 00:00:00", None, False, None),
]


def build_sql(start, end, age_ref, at_order, products):
    where = []
    if start:
        where.append(f"o.date >= '{start}' AND o.date < '{end}'")
    if age_ref:
        where.append(f"{age_sql(repr(age_ref))} = 25")
    if at_order:
        where.append(f"{age_sql('o.date')} = 25")
    if products:
        where.append("o.product_id IN (" + ", ".join(f"'{x}'" for x in products) + ")")
    return BASE + (" WHERE " + " AND ".join(where) if where else "")


def python_value(start, end, age_ref, at_order, products, rows, prices, births):
    def age(birth, day):
        b, d = date.fromisoformat(birth), date.fromisoformat(day[:10])
        return d.year - b.year - ((d.month, d.day) < (b.month, b.day))
    total = 0
    for r in rows:
        if start and not (start <= r["date"] < end):
            continue
        if age_ref and age(births[r["customer_id"]], age_ref) != 25:
            continue
        if at_order and age(births[r["customer_id"]], r["date"]) != 25:
            continue
        if products and r["product_id"] not in products:
            continue
        total += int(r["quantity_product"]) * prices[r["product_id"]]
    return total


def main():
    read = lambda name: list(csv.DictReader(open(ROOT / "data" / name, newline="", encoding="utf-8")))
    prices = {r["product_id"]: int(r["price"]) for r in read("product.csv")}
    births = {r["customer_id"]: r["birth_date"] for r in read("customers.csv")}
    rows = read("orders.csv")
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    out, ok = [], True
    for case_id, *spec in SPECS:
        sql = build_sql(*spec)
        sql_val = con.execute(sql).fetchone()[0]
        py_val = python_value(*spec, rows, prices, births)
        match = sql_val == py_val
        ok &= match
        print(f"{case_id}  sql={sql_val:>9}  csv-python={py_val:>9}  {'OK' if match else 'MISMATCH'}")
        out.append({"case_id": case_id, "sql": sql, "revenue_cents": sql_val})
    with open(ROOT / "prep" / "draft-reference-td1.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["case_id", "sql", "revenue_cents"])
        w.writeheader()
        w.writerows(out)
    print("all match" if ok else "MISMATCHES FOUND")


if __name__ == "__main__":
    main()
