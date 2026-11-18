"""DEMO-VOTE : table jouet d'une ligne (matériel pédagogique construit,
pas une sortie de modèle). Montre la borne de date > vs >=."""
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE sales (sale_date TEXT, amount_cents INTEGER)")
con.execute("INSERT INTO sales VALUES ('2026-01-01', 100)")

faux = """SELECT COALESCE(SUM(amount_cents), 0) FROM sales
          WHERE sale_date >  '2026-01-01' AND sale_date < '2026-01-02'"""
juste = """SELECT COALESCE(SUM(amount_cents), 0) FROM sales
           WHERE sale_date >= '2026-01-01' AND sale_date < '2026-01-02'"""

v_faux = con.execute(faux).fetchone()[0]
v_juste = con.execute(juste).fetchone()[0]
propositions = [v_faux, v_faux, v_juste]          # 2 modèles '>' + 1 modèle '>='
print("variante >  :", v_faux)
print("variante >= :", v_juste)
print("propositions:", propositions, "| référence : 100")
gagnant = max(set(propositions), key=propositions.count)
votes = propositions.count(gagnant)
print(f"2-sur-3 : consensus={votes >= 2} valeur={gagnant} voix={votes} -> "
      f"{'FAUX CONSENSUS' if gagnant != 100 else 'ok'}")
