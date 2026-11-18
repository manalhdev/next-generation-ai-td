# Cross-review of Pair A by Pair B

Reviewer: Tasnim (TasB), Pair B, 18 November 2026. Reviewed: `Orchestrateur.vote_k_sur_n` in [skeleton-multi-llm-en.py](../../skeleton-multi-llm-en.py), lines 609 to 654 (Pair A, commit c01e9a1).

Text sent by Tasnim, in French, and committed by Manal Hassan because Tasnim could not push. Only the formatting was converted from WhatsApp to Markdown and a warning symbol removed; the wording is unchanged.

## Review

J'ai relu le `vote_k_sur_n` de ton fichier (lignes 609 à 654). **La logique est juste**, et elle respecte mieux le contrat que la version A de mon fichier `HANDOFF-TD2.md`. Il reste un point à vérifier avant de committer.

**Ce qui respecte le contrat**

- **Majorité stricte** : `k <= n // 2 or k > n` → `ValueError`. C'est équivalent à `n // 2 < k <= n`.
- **Doublons** : un même couple (provider, model) présent deux fois → `ValueError`.
- **Qui vote** : seules les propositions `executed` qui ont une valeur votent. Une erreur reste dans n mais ne vote pas.
- **Consensus** : la boucle renvoie la première valeur qui atteint k. C'est correct, parce qu'avec une majorité stricte, deux valeurs ne peuvent pas atteindre k en même temps.
- **Abstention** : elle renvoie `value: None` et le plus grand nombre de voix, sans inventer de valeur. Avec `default=0`, le cas où personne ne vote ne plante pas.
- **Format de `models`** : `"provider:model_requested"`, comme le demande la docstring. **Garde ta version et pas la mienne** : ma version A ne mettait que le nom du modèle.

**Le point à vérifier**

Ton code lit les champs avec des attributs (`trace.provider`, `trace.verdict`, `trace.value`). Si `atelier-vote.py` passe des dictionnaires (`{"provider": ..., "verdict": ...}`), tu auras une `AttributeError`. Lance `python3 atelier-vote.py` : si les quatre exemples passent, c'est bon. Sinon, ajoute cette fonction et remplace les accès `trace.x` par `_champ(trace, "x")` :

```python
def _champ(p, nom):
    return p[nom] if isinstance(p, dict) else getattr(p, nom)
```

**Deux détails mineurs**

- `id` masque une fonction intégrée de Python. Renomme la variable en `cle`.
- Les valeurs doivent avoir le même type pour toutes les propositions : `0` (entier) et `"0"` (texte) ne seraient pas comptées ensemble. Le contrat dit « entier en centimes », donc normalement ça va.

Pour les questions du quiz, rien ne change : un modèle en erreur augmente la barre (il compte dans n sans voter), et l'abstention n'invente jamais de valeur.

## Note added at the commit (Manal Hassan)

The point to verify is settled: `atelier-vote.py` passes objects (`SimpleNamespace`), not dictionaries, and its four synthetic examples pass with this version of `vote_k_sur_n` ([td2/C-routing/atelier-vote-td2.txt](../C-routing/atelier-vote-td2.txt)). The two minor details are left to Pair A.
