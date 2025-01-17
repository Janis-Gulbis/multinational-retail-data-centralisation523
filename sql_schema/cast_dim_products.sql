--Remove £ sign from product_price column:
ALTER TABLE dim_products

--Add weight_class column:
ALTER TABLE dim_products 
ADD COLUMN weight_class VARCHAR(255);

UPDATE dim_products 
SET weight_class = 
    CASE 
        WHEN weight_in_kg < 2 THEN 'Light'
        WHEN weight_in_kg >= 2 AND weight_in_kg < 40 THEN 'Mid_Sized'
        WHEN weight_in_kg >= 40 AND weight_in_kg < 140 THEN 'Heavy'
        WHEN weight_in_kg >= 140 THEN 'Truck_Required'
    END;

--Rename and parse 'removed' column:
ALTER TABLE dim_products
RENAME COLUMN removed to still_available;

ALTER TABLE dim_products ALTER still_available TYPE bool USING 
    CASE
        WHEN still_available = 'Still_avaliable' THEN TRUE
        WHEN still_available = 'Removed' THEN FALSE
    END;

-- Cast column datatypes
ALTER TABLE public.dim_products
ALTER COLUMN product_price TYPE NUMERIC
USING product_price::NUMERIC;

ALTER TABLE public.dim_products
ALTER COLUMN weight TYPE NUMERIC
USING weight::NUMERIC;

ALTER TABLE public.dim_products
ALTER COLUMN "EAN" TYPE VARCHAR(18);

ALTER TABLE public.dim_products
ALTER COLUMN product_code TYPE VARCHAR(12);

ALTER TABLE public.dim_products
ALTER COLUMN date_added TYPE DATE
USING date_added::DATE;

ALTER TABLE public.dim_products
ALTER COLUMN uuid TYPE UUID
USING uuid::UUID;

ALTER TABLE public.dim_products
ALTER COLUMN still_available TYPE BOOL
USING still_available::BOOL;

ALTER TABLE public.dim_products
ALTER COLUMN weight_class TYPE VARCHAR(14);

















