"""Exécute partie_b.sql en LECTURE SEULE et affiche chaque résultat.
Usage :  python3 run_partie_b.py data/boutique.sqlite [partie_b.sql]
"""
import sqlite3
import sys
from pathlib import Path

db = sys.argv[1] if len(sys.argv) > 1 else "data/boutique.sqlite"
sql_file = sys.argv[2] if len(sys.argv) > 2 else str(Path(__file__).with_name("partie_b.sql"))

con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)   # lecture seule
lines = [l for l in Path(sql_file).read_text(encoding="utf-8").splitlines()
         if not l.lstrip().startswith(".")]                # retire .headers/.mode

buf = ""
for line in lines:
    buf += line + "\n"
    if sqlite3.complete_statement(buf):
        stmt = buf.strip()
        buf = ""
        body = "\n".join(l for l in stmt.splitlines() if not l.strip().startswith("--")).strip()
        if not body:
            continue
        cur = con.execute(stmt)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        print("\n" + " | ".join(cols))
        print("-" * 60)
        for r in rows:
            print(" | ".join("" if v is None else str(v) for v in r))
con.close()
