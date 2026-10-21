import csv, sqlite3
from datetime import date

con = sqlite3.connect("file:data/boutique.sqlite?mode=ro", uri=True)
print("Produits :", [r[0] for r in con.execute("SELECT product_id FROM product ORDER BY 1")])
print("Nés un 29 février :", con.execute("SELECT COUNT(*) FROM customers WHERE birth_date LIKE '%-02-29'").fetchone()[0])
print("Dates des commandes :", con.execute("SELECT MIN(date), MAX(date) FROM orders").fetchone())

BASE = ("SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents FROM orders o "
        "JOIN product p ON p.product_id = o.product_id JOIN customers c ON c.customer_id = o.customer_id WHERE ")
AGE_0925 = "2026 - CAST(substr(c.birth_date, 1, 4) AS INTEGER) - ('09-25' < substr(c.birth_date, 6, 5)) = 25"

SQL = {
    # mes questions
    "C15": BASE + "o.date >= '2026-03-01 00:00:00' AND o.date < '2026-06-01 00:00:00' AND " + AGE_0925,
    "C16": BASE + "o.product_id IN ('a', 'b', 'c') AND " + AGE_0925,
    "C19": BASE + "o.product_id = 'd' AND o.date >= '2026-09-01 00:00:00' AND o.date < '2026-10-01 00:00:00' AND " + AGE_0925,
    # questions à vérifier (écrites par axel)
    "C02": BASE + AGE_0925,
    "C13": BASE + "o.product_id IN ('a', 'c') AND o.date >= '2026-04-01 00:00:00' AND o.date < '2026-05-01 00:00:00'",
    "C14": BASE + "o.product_id IN ('a', 'b', 'c') AND o.date >= '2026-10-01 00:00:00' AND o.date < '2026-12-01 00:00:00'",
}

# Calcul indépendant sur les CSV, sans SQL
def lire(nom):
    with open(f"data/{nom}.csv", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))
prix = {r["product_id"]: int(r["price"]) for r in lire("product")}
naiss = {r["customer_id"]: date.fromisoformat(r["birth_date"]) for r in lire("customers")}
lignes = lire("orders")

def age(n, d):
    return d.year - n.year - ((d.month, d.day) < (n.month, n.day))
def ca(filtre):
    return sum(int(o["quantity_product"]) * prix[o["product_id"]] for o in lignes if filtre(o))
def entre(o, debut, fin):
    return debut <= o["date"] < fin
def a25(o):
    return age(naiss[o["customer_id"]], date(2026, 9, 25)) == 25

CSV = {
    "C15": ca(lambda o: entre(o, "2026-03-01 00:00:00", "2026-06-01 00:00:00") and a25(o)),
    "C16": ca(lambda o: o["product_id"] in ("a", "b", "c") and a25(o)),
    "C19": ca(lambda o: o["product_id"] == "d" and entre(o, "2026-09-01 00:00:00", "2026-10-01 00:00:00") and a25(o)),
    "C02": ca(a25),
    "C13": ca(lambda o: o["product_id"] in ("a", "c") and entre(o, "2026-04-01 00:00:00", "2026-05-01 00:00:00")),
    "C14": ca(lambda o: o["product_id"] in ("a", "b", "c") and entre(o, "2026-10-01 00:00:00", "2026-12-01 00:00:00")),
}

for cas, sql in SQL.items():
    v = con.execute(sql).fetchone()[0]
    print(f"{cas}: SQL = {v}  |  CSV = {CSV[cas]}  ->  {'OK' if v == CSV[cas] else 'DIFFERENT'}")