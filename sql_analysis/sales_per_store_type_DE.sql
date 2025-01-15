-- Sales per store type in Germany, descending order

SELECT ROUND(CAST(SUM(orders.product_quantity * products.product_price) AS numeric),2) AS total_sales,
    stores.store_type,
    stores.country_code
FROM orders_table AS orders
JOIN dim_store_details AS stores 
    ON orders.store_code = stores.store_code
JOIN dim_products AS products 
    ON orders.product_code = products.product_code
WHERE stores.country_code = 'DE'
GROUP BY stores.store_type,
    stores.country_code
ORDER BY total_sales DESC;