"""TD 1 step 1 - Ines cross-check of C01, C05, C12 (written by Marieseka).

Independent method: no SQL. The three CSV files are read with the csv module and
the revenue is recomputed line by line in Python, then compared with the value
recorded in reference-td1.csv.

Usage (from the repository root):  python3 td1/crosscheck_ines.py   (Windows: .venv\\Scripts\\python.exe td1/crosscheck_ines.py)
Coding assistance: written with Claude, read and run by Ines (see prompts-ai-assistance.md).
"""
import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(name):
    with open(ROOT / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def completed_age(birth, day):
    b, d = date.fromisoformat(birth), date.fromisoformat(day[:10])
    return d.year - b.year - ((d.month, d.day) < (b.month, b.day))


CHECKS = {
    "C01": dict(start="2026-03-01 00:00:00", end="2026-06-01 00:00:00", age_on=None, products=None),
    "C05": dict(start="2026-06-01 00:00:00", end="2026-06-02 00:00:00", age_on=None, products=None),
    "C12": dict(start=None, end=None, age_on=None, products={"a", "b", "c"}),
}


def revenue(orders, prices, births, start, end, age_on, products):
    total = 0
    for line in orders:
        if start and not (start <= line["date"] < end):
            continue
        if age_on and completed_age(births[line["customer_id"]], age_on) != 25:
            continue
        if products and line["product_id"] not in products:
            continue
        total += int(line["quantity_product"]) * prices[line["product_id"]]
    return total


def main():
    prices = {r["product_id"]: int(r["price"]) for r in read("product.csv")}
    births = {r["customer_id"]: r["birth_date"] for r in read("customers.csv")}
    orders = read("orders.csv")
    with open(ROOT / "reference-td1.csv", newline="", encoding="utf-8") as f:
        recorded = {r["case_id"]: r["revenue_cents"] for r in csv.DictReader(f)}
    for case_id, params in CHECKS.items():
        mine = revenue(orders, prices, births, **params)
        theirs = recorded.get(case_id) or "not recorded yet"
        verdict = "OK" if str(mine) == theirs else ("WAITING" if not recorded.get(case_id) else "DIFFERENT")
        print(f"{case_id}  csv-python={mine:>8}  reference-td1.csv={theirs:>16}  {verdict}")


if __name__ == "__main__":
    main()
