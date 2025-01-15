-- Total number of stores in each location, descending order
-- Return top 7

SELECT locality AS locality,
    COUNT (*) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC
LIMIT 7;