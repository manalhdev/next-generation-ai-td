-- What is the revenue excluding VAT, in euro cents, of the orders placed from 2026-06-01 00:00:00 to 2026-09-01 00:00:00?
SELECT SUM(p.price * o.quantity_product) FROM product p
JOIN orders o ON p.product_id = o.product_id
WHERE o.date >= '2026-06-01 00:00:00' AND o.date < '2026-09-01 00:00:00';