SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON o.product_id = p.product_id
WHERE o.date >= '2026-05-31'
  AND o.date < '2026-06-01';