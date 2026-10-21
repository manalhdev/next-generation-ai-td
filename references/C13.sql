-- C13: products a and c, 2026-04-01 <= date < 2026-05-01
-- written_by: axel12334556 | value: 107740 cents
-- checks: alt SQL + Python on CSV agree (peer check: pending)
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents FROM orders o JOIN product p ON p.product_id = o.product_id JOIN customers c ON c.customer_id = o.customer_id WHERE o.product_id IN ('a', 'c') AND o.date >= '2026-04-01 00:00:00' AND o.date < '2026-05-01 00:00:00';

-- independent alternative query (same value):
-- SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents FROM orders o JOIN product p ON p.product_id = o.product_id JOIN customers c ON c.customer_id = o.customer_id WHERE (o.product_id = 'a' OR o.product_id = 'c') AND substr(o.date, 1, 7) = '2026-04';
