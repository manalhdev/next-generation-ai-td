"""TD 1 - Step 1 (Axel): compute C02, C13, C14 and cross-check C08, C09, C11.

Usage (from the repo root or from td1/, venv activated):
    python3 crosscheck_references_axel.py          # Windows: python crosscheck_references_axel.py

For every question, three computations that must agree:
  A. the reference SQL (completed-age formula), run on data/boutique.sqlite read-only;
  B. a second, differently written SQL (birth-date interval instead of age formula);
  C. a pure-Python recomputation from the three CSV files.

For C08, C09, C11 (teammates' questions): if their query is already in
reference-td1.csv, it is also run and compared to A/B/C.

Only C02, C13, C14 are written into reference-td1.csv; other rows are kept as they are.

Conventions: period date >= start AND date < end; completed age (year, then
month-day); revenue = SUM(quantity_product * price) in cents excl. VAT; 0, never NULL.
Coding assistance: generated with Claude, read and verified by me (declared in reports/td1.md).
"""

import csv
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Repo root = the folder holding data/ and reference-td1.csv; works from the root or from td1/.
KIT = Path(sys.argv[1]) if len(sys.argv) > 1 else (HERE.parent if HERE.name == "td1" else HERE)
DB = KIT / "data" / "boutique.sqlite"
REF = KIT / "reference-td1.csv"
WRITER = "axel12334556"

BASE = ("SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents "
        "FROM orders o "
        "JOIN product p ON p.product_id = o.product_id "
        "JOIN customers c ON c.customer_id = o.customer_id ")

# Completed age of the customer on a literal date: year difference,
# minus 1 if the birthday (MM-DD) has not happened yet that year.
def age_on(d):
    return (f"(CAST(substr('{d}', 1, 4) AS INTEGER) - CAST(substr(c.birth_date, 1, 4) AS INTEGER)"
            f" - (substr('{d}', 6, 5) < substr(c.birth_date, 6, 5)))")

# A. Reference SQL                         B. Alternative SQL (birth-date interval)
#    Exactly 25 on D  <=>  born in ]D - 26 years ; D - 25 years]
QUESTIONS = {
    # my questions
    "C02": dict(
        mine=True,
        sql=BASE + f"WHERE {age_on('2026-09-25')} = 25",
        alt=BASE + "WHERE c.birth_date > '2000-09-25' AND c.birth_date <= '2001-09-25'",
        py=dict(age_ref="2026-09-25"),
    ),
    "C13": dict(
        mine=True,
        sql=BASE + "WHERE o.product_id IN ('a', 'c') "
                   "AND o.date >= '2026-04-01 00:00:00' AND o.date < '2026-05-01 00:00:00'",
        alt=BASE + "WHERE (o.product_id = 'a' OR o.product_id = 'c') "
                   "AND substr(o.date, 1, 7) = '2026-04'",
        py=dict(products=("a", "c"), period=("2026-04-01 00:00:00", "2026-05-01 00:00:00")),
    ),
    "C14": dict(
        mine=True,
        sql=BASE + "WHERE o.product_id IN ('a', 'b', 'c') "
                   "AND o.date >= '2026-10-01 00:00:00' AND o.date < '2026-12-01 00:00:00'",
        alt=BASE + "WHERE (o.product_id = 'a' OR o.product_id = 'b' OR o.product_id = 'c') "
                   "AND substr(o.date, 1, 7) IN ('2026-10', '2026-11')",
        py=dict(products=("a", "b", "c"), period=("2026-10-01 00:00:00", "2026-12-01 00:00:00")),
    ),
    # questions I cross-check
    "C08": dict(
        sql=BASE + f"WHERE {age_on('2026-09-24')} = 25",
        alt=BASE + "WHERE c.birth_date > '2000-09-24' AND c.birth_date <= '2001-09-24'",
        py=dict(age_ref="2026-09-24"),
    ),
    "C09": dict(
        sql=BASE + f"WHERE {age_on('2026-09-26')} = 25",
        alt=BASE + "WHERE c.birth_date > '2000-09-26' AND c.birth_date <= '2001-09-26'",
        py=dict(age_ref="2026-09-26"),
    ),
    "C11": dict(
        sql=BASE + f"WHERE {age_on('2026-12-01')} = 25",
        alt=BASE + "WHERE c.birth_date > '2000-12-01' AND c.birth_date <= '2001-12-01'",
        py=dict(age_ref="2026-12-01"),
    ),
}


def run_sql(sql):
    con = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    try:
        con.execute("PRAGMA query_only = 1")
        cur = con.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        if len(rows) != 1 or len(cols) != 1:
            raise ValueError(f"expected 1 row x 1 column, got {len(rows)} x {cols}")
        return rows[0][0]
    finally:
        con.close()


def read_csv(name):
    with open(KIT / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


PRICE = {r["product_id"]: int(r["price"]) for r in read_csv("product.csv")}
BIRTH = {r["customer_id"]: date.fromisoformat(r["birth_date"]) for r in read_csv("customers.csv")}
ORDERS = read_csv("orders.csv")


def completed_age(birth, on):
    return on.year - birth.year - ((on.month, on.day) < (birth.month, birth.day))


def py_check(p):
    total = 0
    for o in ORDERS:
        ts = datetime.strptime(o["date"], "%Y-%m-%d %H:%M:%S")
        if "period" in p:
            start, end = (datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in p["period"])
            if not (start <= ts < end):
                continue
        if "products" in p and o["product_id"] not in p["products"]:
            continue
        if "age_ref" in p and completed_age(BIRTH[o["customer_id"]],
                                            date.fromisoformat(p["age_ref"])) != 25:
            continue
        total += int(o["quantity_product"]) * PRICE[o["product_id"]]
    return total


def main():
    if not DB.exists():
        sys.exit(f"Database not found: {DB}  (run from the kit-td1 folder)")

    print("Products in base:", sorted(PRICE))
    ref_rows = []
    if REF.exists():
        with open(REF, newline="", encoding="utf-8") as f:
            ref_rows = list(csv.DictReader(f))
    teammate = {r["case_id"]: r for r in ref_rows if (r.get("sql") or "").strip()}

    all_ok, results = True, {}
    for cid, q in QUESTIONS.items():
        a, b, c = run_sql(q["sql"]), run_sql(q["alt"]), py_check(q["py"])
        ok = a == b == c
        line = f"{cid}  A(sql)={a}  B(alt sql)={b}  C(python/csv)={c}"
        if not q.get("mine") and cid in teammate:
            t = teammate[cid]
            try:
                t_val = run_sql(t["sql"])
            except Exception as e:  # invalid teammate SQL is a finding, not a crash
                t_val = f"ERROR {e}"
            ok = ok and t_val == a and str(t.get("revenue_cents", "")).strip() == str(a)
            line += f"  teammate sql -> {t_val} (recorded: {t.get('revenue_cents', '')})"
        elif not q.get("mine"):
            line += "  (teammate query not in reference-td1.csv yet)"
        print(("OK       " if ok else "MISMATCH ") + line)
        all_ok &= ok
        results[cid] = a

    if not all_ok:
        sys.exit("\nAt least one mismatch: nothing written. Investigate (or show it to your teammate).")

    # Write my three rows, keep the others untouched.
    if not ref_rows:
        ref_rows = [{"case_id": f"C{i:02d}", "sql": "", "revenue_cents": ""} for i in range(1, 21)]
    fields = list(ref_rows[0].keys())  # keeps the repo's extra columns if present
    for r in ref_rows:
        if r["case_id"] in ("C02", "C13", "C14"):
            r["sql"], r["revenue_cents"] = QUESTIONS[r["case_id"]]["sql"], results[r["case_id"]]
            if "written_by" in fields:
                r["written_by"] = WRITER
            if "check_method" in fields:
                r["check_method"] = "self: 2nd SQL (birth-date interval / month prefix) + Python on CSV; peer check pending"
    with open(REF, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(ref_rows)
    print(f"\nAll checks agree. C02, C13, C14 written into {REF.name}.")


if __name__ == "__main__":
    main()
