-- =====================================================================
-- TD 2 - Partie B (Pair B) : faux consensus C09
-- À exécuter en LECTURE SEULE sur data/boutique.sqlite :
--   sqlite3 -readonly data/boutique.sqlite < partie_b.sql
-- Référence C09 (reference-td1.csv) = 487980 centimes
-- Question C09 : CA HT (centimes) des clients qui ont exactement 25 ans
--                le 2026-09-26, sur toutes leurs commandes.
-- =====================================================================
.headers on
.mode column

-- ---------------------------------------------------------------------
-- 0. Requête de référence (reference-td1.csv, C09)  -> attendu 487980
-- ---------------------------------------------------------------------
SELECT 'REF' AS q, COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product p   ON p.product_id = o.product_id
JOIN customers c ON c.customer_id = o.customer_id
WHERE CAST(strftime('%Y', '2026-09-26') AS INTEGER) - CAST(strftime('%Y', c.birth_date) AS INTEGER)
      - (strftime('%m-%d', '2026-09-26') < strftime('%m-%d', c.birth_date)) = 25;

-- ---------------------------------------------------------------------
-- 1. Requête fautive M1 : cohere/north-mini-code:free (trace TD1 -> 0)
--    copiée telle quelle depuis traces-td1.csv
-- ---------------------------------------------------------------------
SELECT 'M1_cohere' AS q, COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE c.birth_date <= '2026-09-26' AND c.birth_date > date('2026-09-26', '-26 years')
AND c.birth_date <= date('2026-09-26', '-25 years') AND c.birth_date > date('2026-09-26', '-26 years')
AND o.date >= '2026-09-26 00:00:00' AND o.date < '2027-09-26 00:00:00';

-- ---------------------------------------------------------------------
-- 2. Requête fautive M2 : qwen/qwen3.8-27b (trace TD1 -> 0)
--    copiée telle quelle depuis traces-td1.csv
-- ---------------------------------------------------------------------
SELECT 'M2_qwen' AS q, COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE (strftime('%Y', o.date) - strftime('%Y', c.birth_date)) = 25
  AND (strftime('%m-%d', o.date) >= strftime('%m-%d', c.birth_date))
  AND (strftime('%m-%d', o.date) < strftime('%m-%d', date(c.birth_date, '+26 years')));

-- ---------------------------------------------------------------------
-- 3. Preuves du diagnostic de clause
-- ---------------------------------------------------------------------
-- 3a. M1 : la fenêtre de naissance de Cohere est JUSTE.
--     Sans la clause o.date, on doit retrouver 487980.
SELECT 'M1_sans_clause_date' AS q, COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE c.birth_date > date('2026-09-26', '-26 years')     -- > 2000-09-26
  AND c.birth_date <= date('2026-09-26', '-25 years');   -- <= 2001-09-26

-- 3b. M1 : dates des commandes des clients de 25 ans -> toutes < 2026-09-26
SELECT 'M1_dates_commandes' AS q,
       COUNT(*) AS nb_lignes, MIN(o.date) AS premiere, MAX(o.date) AS derniere,
       SUM(o.date >= '2026-09-26 00:00:00') AS nb_dans_fenetre_M1
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE c.birth_date > '2000-09-26' AND c.birth_date <= '2001-09-26';

-- 3c. M2 : la 3e condition est une contradiction.
--     md(date(birth,'+26 years')) = md(birth) sauf pour un 29 février.
--     Nombre de clients pour lesquels ce n'est PAS vrai :
SELECT 'M2_clients_md_different' AS q, COUNT(*) AS nb
FROM customers
WHERE strftime('%m-%d', date(birth_date, '+26 years')) <> strftime('%m-%d', birth_date);

-- ---------------------------------------------------------------------
-- 4. REQUÊTE DELTA : lignes customer_id comptées par la référence
--    mais manquées (ou ajoutées à tort) par M1 et M2.
-- ---------------------------------------------------------------------
WITH ref AS (
  SELECT o.customer_id, SUM(o.quantity_product * p.price) AS rev
  FROM orders o
  JOIN product p   ON p.product_id = o.product_id
  JOIN customers c ON c.customer_id = o.customer_id
  WHERE CAST(strftime('%Y', '2026-09-26') AS INTEGER) - CAST(strftime('%Y', c.birth_date) AS INTEGER)
        - (strftime('%m-%d', '2026-09-26') < strftime('%m-%d', c.birth_date)) = 25
  GROUP BY o.customer_id
),
m1 AS (   -- WHERE de Cohere, à l'identique
  SELECT o.customer_id, SUM(o.quantity_product * p.price) AS rev
  FROM customers c
  JOIN orders o  ON o.customer_id = c.customer_id
  JOIN product p ON o.product_id = p.product_id
  WHERE c.birth_date <= '2026-09-26' AND c.birth_date > date('2026-09-26', '-26 years')
    AND c.birth_date <= date('2026-09-26', '-25 years') AND c.birth_date > date('2026-09-26', '-26 years')
    AND o.date >= '2026-09-26 00:00:00' AND o.date < '2027-09-26 00:00:00'
  GROUP BY o.customer_id
),
m2 AS (   -- WHERE de Qwen, à l'identique
  SELECT o.customer_id, SUM(o.quantity_product * p.price) AS rev
  FROM orders o
  JOIN customers c ON o.customer_id = c.customer_id
  JOIN product p   ON o.product_id = p.product_id
  WHERE (strftime('%Y', o.date) - strftime('%Y', c.birth_date)) = 25
    AND (strftime('%m-%d', o.date) >= strftime('%m-%d', c.birth_date))
    AND (strftime('%m-%d', o.date) < strftime('%m-%d', date(c.birth_date, '+26 years')))
  GROUP BY o.customer_id
)
SELECT c.customer_id,
       c.birth_date,
       COALESCE(ref.rev, 0)                        AS ref_cents,
       COALESCE(m1.rev, 0)                         AS m1_cohere_cents,
       COALESCE(m2.rev, 0)                         AS m2_qwen_cents,
       COALESCE(ref.rev, 0) - COALESCE(m1.rev, 0)  AS delta_m1,
       COALESCE(ref.rev, 0) - COALESCE(m2.rev, 0)  AS delta_m2
FROM customers c
LEFT JOIN ref ON ref.customer_id = c.customer_id
LEFT JOIN m1  ON m1.customer_id  = c.customer_id
LEFT JOIN m2  ON m2.customer_id  = c.customer_id
WHERE COALESCE(ref.rev, 0) <> COALESCE(m1.rev, 0)
   OR COALESCE(ref.rev, 0) <> COALESCE(m2.rev, 0)
ORDER BY c.birth_date, c.customer_id;

-- ---------------------------------------------------------------------
-- 5. Contrôle de bouclage : somme des deltas = référence - valeur fausse
--    attendu sur boutique.sqlite : 487980 - 0 = 487980 pour M1 ET M2.
-- ---------------------------------------------------------------------
WITH ref AS (
  SELECT o.customer_id, SUM(o.quantity_product * p.price) AS rev
  FROM orders o
  JOIN product p   ON p.product_id = o.product_id
  JOIN customers c ON c.customer_id = o.customer_id
  WHERE CAST(strftime('%Y', '2026-09-26') AS INTEGER) - CAST(strftime('%Y', c.birth_date) AS INTEGER)
        - (strftime('%m-%d', '2026-09-26') < strftime('%m-%d', c.birth_date)) = 25
  GROUP BY o.customer_id
),
m1 AS (   -- WHERE de Cohere, à l'identique
  SELECT o.customer_id, SUM(o.quantity_product * p.price) AS rev
  FROM customers c
  JOIN orders o  ON o.customer_id = c.customer_id
  JOIN product p ON o.product_id = p.product_id
  WHERE c.birth_date <= '2026-09-26' AND c.birth_date > date('2026-09-26', '-26 years')
    AND c.birth_date <= date('2026-09-26', '-25 years') AND c.birth_date > date('2026-09-26', '-26 years')
    AND o.date >= '2026-09-26 00:00:00' AND o.date < '2027-09-26 00:00:00'
  GROUP BY o.customer_id
),
m2 AS (   -- WHERE de Qwen, à l'identique
  SELECT o.customer_id, SUM(o.quantity_product * p.price) AS rev
  FROM orders o
  JOIN customers c ON o.customer_id = c.customer_id
  JOIN product p   ON o.product_id = p.product_id
  WHERE (strftime('%Y', o.date) - strftime('%Y', c.birth_date)) = 25
    AND (strftime('%m-%d', o.date) >= strftime('%m-%d', c.birth_date))
    AND (strftime('%m-%d', o.date) < strftime('%m-%d', date(c.birth_date, '+26 years')))
  GROUP BY o.customer_id
)
SELECT 'TOTAL_DELTA' AS q,
       COALESCE((SELECT SUM(rev) FROM ref), 0) AS ref_total,
       COALESCE((SELECT SUM(rev) FROM m1), 0)  AS m1_total,
       COALESCE((SELECT SUM(rev) FROM m2), 0)  AS m2_total,
       COALESCE((SELECT SUM(rev) FROM ref), 0) - COALESCE((SELECT SUM(rev) FROM m1), 0) AS somme_delta_m1,
       COALESCE((SELECT SUM(rev) FROM ref), 0) - COALESCE((SELECT SUM(rev) FROM m2), 0) AS somme_delta_m2,
       CASE WHEN COALESCE((SELECT SUM(rev) FROM ref), 0) = 487980 THEN 'REF OK (487980)' ELSE 'REF DIFFERENTE !' END AS check_ref;

-- ---------------------------------------------------------------------
-- 6. Recoupement indépendant : la valeur fausse de Dots (47900) ne compte
--    que les clients nés EXACTEMENT le 2001-09-26 (année 2001, m-d <= et >= 09-26).
--    Ce sous-ensemble de la référence doit donc valoir 47900.
-- ---------------------------------------------------------------------
SELECT 'SOUS_ENSEMBLE_2001-09-26' AS q,
       COUNT(DISTINCT c.customer_id) AS nb_clients,
       COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents,
       CASE WHEN COALESCE(SUM(o.quantity_product * p.price), 0) = 47900 THEN 'OK = valeur Dots' ELSE 'ECART' END AS check_dots
FROM orders o
JOIN product p   ON p.product_id = o.product_id
JOIN customers c ON c.customer_id = o.customer_id
WHERE c.birth_date = '2001-09-26';
