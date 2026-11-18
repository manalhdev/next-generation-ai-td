"""Comptage des voix (contrôle indépendant du comptage à la main) pour C09 et C10.
Applique le contrat de vote_k_sur_n : seules les propositions 'executed' avec
une valeur votent ; une erreur reste dans n sans voter ; aucune valeur inventée.
À remplacer/recouper par Orchestrateur.vote_k_sur_n de la paire A dès livraison.
Usage : python3 compte_votes.py traces-td1.csv
"""
import csv
import sys
from collections import Counter

PANEL_3 = ["openai/gpt-oss-120b", "cohere/north-mini-code:free", "qwen/qwen3.8-27b"]


def vote(props, k):
    n = len(props)
    if not (n // 2 < k <= n):
        raise ValueError("k doit être une majorité stricte")
    voix = Counter(p["value"] for p in props if p["value"] is not None)
    if not voix:
        return {"consensus": False, "value": None, "votes": 0, "models": []}
    v, nb = voix.most_common(1)[0]
    if nb >= k:
        return {"consensus": True, "value": v, "votes": nb,
                "models": [p["model"] for p in props if p["value"] == v]}
    return {"consensus": False, "value": None, "votes": nb, "models": []}


rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
for case in ("C09", "C10"):
    cells = [r for r in rows if r["case_id"] == case]
    ref = int(cells[0]["reference"])
    props = [{"model": r["model_requested"],
              "value": int(r["value"]) if r["value"] not in ("", None) and r["verdict"] in ("correct", "incorrect") else None}
             for r in cells]
    p3 = [p for p in props if p["model"] in PANEL_3]
    print(f"\n{case} (référence {ref})")
    for p in props:
        print(f"   {p['model']:<40} {p['value']}")
    for nom, pp, k in (("2-sur-3 panel fixe", p3, 2), ("3-sur-5 quorum", props, 3)):
        d = vote(pp, k)
        verdict = ("ABSTENTION" if not d["consensus"]
                   else "JUSTE" if d["value"] == ref else "FAUX CONSENSUS")
        print(f"   {nom:<20} -> {d}  => {verdict}")
