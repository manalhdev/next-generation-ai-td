"""Independent cross-check of C03, C06 and C07 (written by ines729, checked by Daiki4529).

Method: plain Python on data/orders.csv and data/product.csv, no SQL and no database.
Dates are parsed with datetime, periods are closed on the left and open on the right,
revenue is quantity * price in euro cents excluding VAT, 0 when nothing matches.

Run: python td1/crosscheck_c03_c06_c07.py
"""
import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FMT = "%Y-%m-%d %H:%M:%S"

# case_id: (start, end, products or None for all products)
CASES = {
    "C03": ("2026-01-01 00:00:00", "2026-07-01 00:00:00", {"a", "b", "c"}),
    "C06": ("2025-01-01 00:00:00", "2026-01-01 00:00:00", None),
    "C07": ("2026-05-31 00:00:00", "2026-06-01 00:00:00", None),
}


def read_csv(name):
    with open(ROOT / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def revenue(orders, prices, start, end, products):
    start, end = datetime.strptime(start, FMT), datetime.strptime(end, FMT)
    total = 0
    for o in orders:
        if not (start <= datetime.strptime(o["date"], FMT) < end):
            continue
        if products is not None and o["product_id"] not in products:
            continue
        total += int(o["quantity_product"]) * prices[o["product_id"]]
    return total


def main():
    prices = {p["product_id"]: int(p["price"]) for p in read_csv("product.csv")}
    orders = read_csv("orders.csv")
    with open(ROOT / "reference-td1.csv", newline="", encoding="utf-8") as f:
        reference = {r["case_id"]: r["revenue_cents"] for r in csv.DictReader(f)}

    for case_id, (start, end, products) in CASES.items():
        mine = revenue(orders, prices, start, end, products)
        theirs = reference.get(case_id, "")
        if not theirs:
            verdict = "no reference value yet"
        elif int(theirs) == mine:
            verdict = "MATCH"
        else:
            verdict = "DIFFERENT, tell ines729"
        print(f"{case_id}: csv check = {mine}, reference-td1.csv = {theirs or '-'} -> {verdict}")


if __name__ == "__main__":
    main()
