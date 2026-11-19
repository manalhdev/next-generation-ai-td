# AI coding assistance: prompts and decisions (TD 1 and TD 2)

The module accepts AI-assisted code if the prompts are kept and the decisions explained.
A model's numerical answer is never used as a reference value.

## Group rule (agreed at the start of TD 1)

The assistant is used for three things only: **explaining** a notion or a command, **diagnosing**
an error or an empty result, and **helping with wording or repository maintenance**. It does not
write the SQL, the reference values, the vote function, the routing rule, the cross-reviews or the
reported figures. Every number in the reports is produced by a member and checked against the
project files. The prompts below are the French originals, with an English gloss in brackets.

---

## 2026-10-21 — TD 1, SQL query clarification (Claude Code, Claude Opus 5.5), Julia

**Prompt (verbatim):** « Explique pourquoi on doit calculer l'âge du client à la date de la
commande au lieu d'utiliser son âge direct ? Aide moi à comprendre l'expression SQL ? »

**What the assistant did:**
- explained the difference between current age and age at a reference date;
- explained the SQL date functions used in the assignment;
- pointed out a possible issue when comparing month and day — this was a **code-reading remark**,
  not an explanation, and Julia treated it as such.

**Decisions:**
- Julia wrote the query and checked the remark against protocol section 1 before deciding whether to
  change anything.
- The assistant did not write or modify the SQL. The final query and its results were checked
  independently.

## 2026-10-31 — TD 1, result verification (Claude Code, Claude Opus 5.5), Marie

**Prompt (verbatim):** « Je comprends pas comment comparer les résultats de nos
différents modèles et identifier quelles colonnes doivent être vérifiées ? »

**What the assistant did:**
- explained how to read the model comparison CSV;
- proposed a checklist of things to look for (missing values, inconsistent values, absent model
  responses);
- clarified the difference between an incorrect answer and a missing model response.

**Decisions:**
- The checklist was used as an **aid**, not as a verdict: Marie ran it line by line and decided for
  each row what counted as a failure.
- The assistant did not calculate or decide the reference answers.
- The final interpretation was checked against the project files.

## 2026-11-18 — TD 2, Pair B, documentation of the cross-review (Claude Code, Claude Opus 5.5), Tasnim

**Prompt (verbatim):** « Peux-tu m'aider à structurer ma contre-revue et à rendre les observations
techniques plus faciles à comprendre sans changer leur sens ? »

**What the assistant did:**
- suggested a clearer organisation (observations / checks / conclusions);
- **corrected the Markdown formatting** of the review file (headings, lists, code blocks);
- pointed out one sentence that could be read two ways.

**Decisions:**
- The technical observations and the conclusions are Tasnim's. The assistant touched **formatting
  only** and flagged one ambiguous sentence; Tasnim rewrote it herself.
- Tasnim remains responsible for the final content of `td2/B-consensus/review-1.md` and
  `td2/C-routing/review-1.md`.

## 2026-11-18 — TD 2, SQL result interpretation (Claude Code, Claude Opus 5.5), Julia

**Prompt (verbatim):** « Ma requête SQL retourne un résultat vide. Peux-tu expliquer les
raisons possibles et comment je peux vérifier si le filtre est trop restrictif ou pas? »

**What the assistant did:**
- explained common reasons a SQL query returns no rows;
- suggested checking each filter condition separately;
- explained the difference between an empty result set and a numerical result equal to zero.

**Decisions:**
- Julia checked the query against the actual database herself.
- The assistant did not modify the project SQL and did not decide whether the result was correct.
- The final interpretation is based on `data/boutique.sqlite` and the assignment requirements.

## 2026-11-18 — TD 2, report wording and consistency (Claude Code, Claude Opus 5.5), Marie

**Prompt (verbatim):** « Vérifie si l'explication de nos résultats est cohérente avec le
tableau et ade moi à rendre le paragraphe plus clair ? »

**What the assistant did:**
- compared the wording of the explanation with the table structure and flagged two places where they
  disagreed;
- suggested clearer formulations for three sentences;
- pointed out sentences that could be ambiguous.

**Decisions:**
- Marie checked every figure and every technical claim herself before accepting or rejecting a
  suggestion. Two suggestions were kept, one was rewritten, one was dropped.
- The assistant did not compute or verify any reported figure.
- Only wording and presentation were changed in the final text.

## 2026-11-18 — TD 2, Git repository maintenance (Claude Code, Claude Opus 5.5), Manal Hassan

**Prompt (verbatim):** «Tu peux m'aider à vérifier quels fichiers sont modifiés, lesquels sont non
suivis et si je peux push ? »

**What the assistant did:**
- explained the output of `git status`;
- helped interpret `git diff`;
- reminded the user to check the staged files before committing.

**Decisions:**
- Manal reviewed the changes herself before committing.
- The push was done manually after checking the branch and repository status. The assistant did not
  run any git command that changes the repository.

---

## Traceability

| Value / artefact | Written by | Checked by |
|---|---|---|
| SQL C10, C18, C17 | Julia | second member |
| `reference-td1.csv` (20 values) | members, TD 1 | second member, per protocol |
| TD 1 comparison CSV | `tools/td1_consolidate.py` + member fill-in | Marie and axel12334556 |
| `reports/td1.md` figures | Manal Hassan | Manal Hassan, against files |
| Pair B SQL and scripts | Pair B | Pair B, outputs kept as executed |
| Pair B cross-reviews | Tasnim | Tasnim, then Manal Hassan (commit, unchanged) |
| `reports/td2.md` figures | members, from script outputs | Manal Hassan, rerun on `traces-td1.csv` |

**What was not delegated to the assistant:** SQL, reference values, vote function, routing rule,
cross-review content, report figures, any git command that writes to the repository.
