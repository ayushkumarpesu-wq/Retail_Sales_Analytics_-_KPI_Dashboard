-- Run against data/processed/retail_sales.db.
-- Revenue is net of negative-quantity returns and cancellation invoices.

-- Monthly sales and month-over-month change.
WITH monthly AS (
    SELECT invoice_month, ROUND(SUM(revenue), 2) AS net_revenue
    FROM retail_sales
    GROUP BY invoice_month
)
SELECT invoice_month,
       net_revenue,
       ROUND(
           100.0 * (net_revenue - LAG(net_revenue) OVER (ORDER BY invoice_month))
           / NULLIF(LAG(net_revenue) OVER (ORDER BY invoice_month), 0),
           2
       ) AS mom_growth_pct
FROM monthly
ORDER BY invoice_month;

-- Order count and average net revenue per completed order.
WITH order_totals AS (
    SELECT invoice_no, SUM(revenue) AS order_revenue
    FROM retail_sales
    WHERE is_cancellation = 0
    GROUP BY invoice_no
    HAVING SUM(CASE WHEN quantity > 0 THEN 1 ELSE 0 END) > 0
)
SELECT COUNT(*) AS completed_orders,
       ROUND(SUM(order_revenue), 2) AS net_revenue,
       ROUND(AVG(order_revenue), 2) AS average_order_value
FROM order_totals;

-- Country performance.
SELECT country,
       ROUND(SUM(revenue), 2) AS net_revenue,
       COUNT(DISTINCT CASE
           WHEN is_cancellation = 0 AND quantity > 0 THEN invoice_no
       END) AS completed_orders
FROM retail_sales
GROUP BY country
ORDER BY net_revenue DESC;

-- Product performance (identified by stock code; descriptions are not categories).
SELECT stock_code,
       MAX(description) AS description,
       ROUND(SUM(revenue), 2) AS net_revenue,
       SUM(quantity) AS net_quantity
FROM retail_sales
GROUP BY stock_code
ORDER BY net_revenue DESC
LIMIT 20;

-- Return and cancellation activity. Negative quantities are retained in the data.
SELECT
    SUM(CASE WHEN is_return = 1 THEN 1 ELSE 0 END) AS return_rows,
    SUM(CASE WHEN is_cancellation = 1 THEN 1 ELSE 0 END) AS cancellation_rows,
    ROUND(SUM(CASE WHEN is_return = 1 THEN revenue ELSE 0 END), 2) AS return_value
FROM retail_sales;
