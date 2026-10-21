SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON o.product_id = p.product_id
WHERE o.product_id IN ('a', 'b', 'c')
  AND o.date >= '2026-01-01'
  AND o.date < '2026-07-01';