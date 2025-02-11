-- Total sales per month, descending order
-- Return top 6

SELECT ROUND(CAST(SUM(orders.product_quantity * products.product_price) AS numeric),2) AS total_sales,
    dates.month AS "month"
FROM orders_table AS orders
    JOIN dim_date_times AS dates ON orders.date_uuid = dates.date_uuid
    JOIN dim_products AS products ON orders.product_code = products.product_code
GROUP BY dates.month
ORDER BY total_sales DESC
LIMIT 6;