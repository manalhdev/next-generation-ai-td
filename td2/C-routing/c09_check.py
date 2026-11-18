"""TD 2, check of step 2 by Pair C at the merge: the wrong consensus on C09 (the c09_check.py cited by Pair B was not received).

Usage (from the repository root):  python3 td2/C-routing/c09_check.py data/boutique.sqlite
1. Delta query per customer: revenue of the reference window ]2000-09-26, 2001-09-26] and the part of it
   kept by the WHERE clauses of Cohere and Qwen, as returned in traces-td1.csv.
2. Rows kept by the two faulty WHERE clauses on the whole database (none are wrongly added).
3. Recomputation in Python on the CSV files, without SQL.
"""
import csv
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REFERENCE_DAY = date(2026, 9, 26)

DELTA = """
WITH lines AS (
  SELECT c.customer_id, c.birth_date, o.date, o.quantity_product * p.price AS amount
  FROM orders o
  JOIN customers c ON c.customer_id = o.customer_id
  JOIN product p ON p.product_id = o.product_id
  WHERE c.birth_date > '2000-09-26' AND c.birth_date <= '2001-09-26'
),
per_customer AS (
  SELECT customer_id, birth_date, COUNT(*) AS order_lines, SUM(amount) AS ref_cents,
         SUM(CASE WHEN date >= '2026-09-26 00:00:00' AND date < '2027-09-26 00:00:00'
                  THEN amount ELSE 0 END) AS cohere_cents,
         SUM(CASE WHEN (strftime('%Y', date) - strftime('%Y', birth_date)) = 25
                   AND strftime('%m-%d', date) >= strftime('%m-%d', birth_date)
                   AND strftime('%m-%d', date) < strftime('%m-%d', date(birth_date, '+26 years'))
                  THEN amount ELSE 0 END) AS qwen_cents
  FROM lines GROUP BY customer_id, birth_date
)
SELECT customer_id, birth_date, order_lines, ref_cents, cohere_cents, qwen_cents, ref_cents - cohere_cents AS missed
FROM per_customer
UNION ALL
SELECT 'TOTAL', NULL, SUM(order_lines), SUM(ref_cents), SUM(cohere_cents), SUM(qwen_cents), SUM(ref_cents) - SUM(cohere_cents)
FROM per_customer
"""

KEPT_BY_FAULTY = {
    "Cohere": "c.birth_date <= '2026-09-26' AND c.birth_date > date('2026-09-26', '-26 years') "
              "AND c.birth_date <= date('2026-09-26', '-25 years') AND c.birth_date > date('2026-09-26', '-26 years') "
              "AND o.date >= '2026-09-26 00:00:00' AND o.date < '2027-09-26 00:00:00'",
    "Qwen": "(strftime('%Y', o.date) - strftime('%Y', c.birth_date)) = 25 "
            "AND strftime('%m-%d', o.date) >= strftime('%m-%d', c.birth_date) "
            "AND strftime('%m-%d', o.date) < strftime('%m-%d', date(c.birth_date, '+26 years'))",
}


def read_csv(name):
    with open(ROOT / "data" / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    database = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "data" / "boutique.sqlite")
    con = sqlite3.connect(f"file:{database}?mode=ro", uri=True)

    print("1. Delta query: customer_id | birth_date | order_lines | ref_cents | cohere_cents | qwen_cents | missed")
    for row in con.execute(DELTA):
        print("  ", " | ".join("" if v is None else str(v) for v in row))

    print("2. Rows kept by the faulty WHERE clauses on the whole database")
    for model, where in KEPT_BY_FAULTY.items():
        count = con.execute("SELECT COUNT(*) FROM orders o JOIN customers c ON c.customer_id = o.customer_id "
                            "JOIN product p ON p.product_id = o.product_id WHERE " + where).fetchone()[0]
        print(f"   {model}: {count} row(s)")

    print("3. Recomputation in Python on the CSV files")
    prices = {r["product_id"]: int(r["price"]) for r in read_csv("product.csv")}
    births = {r["customer_id"]: date.fromisoformat(r["birth_date"]) for r in read_csv("customers.csv")}
    total = 0
    for line in read_csv("orders.csv"):
        b = births[line["customer_id"]]
        age = REFERENCE_DAY.year - b.year - ((REFERENCE_DAY.month, REFERENCE_DAY.day) < (b.month, b.day))
        if age == 25:
            total += int(line["quantity_product"]) * prices[line["product_id"]]
    print(f"   revenue of the customers aged 25 on {REFERENCE_DAY}: {total}")


if __name__ == "__main__":
    main()
