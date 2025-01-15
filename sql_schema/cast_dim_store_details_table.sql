--Cast column datatypes:

ALTER TABLE dim_store_details

    ALTER COLUMN longitude TYPE double precision USING
        CASE WHEN longitude ~ '^[+-]?\d+(\.\d+)?$' THEN longitude::double precision ELSE NULL END,

    ALTER COLUMN latitude TYPE double precision USING
        CASE WHEN latitude ~ '^[+-]?\d+(\.\d+)?$' THEN latitude::double precision ELSE NULL END,
        
    ALTER COLUMN locality TYPE varchar(255),
    ALTER COLUMN store_code TYPE varchar(12),
    ALTER COLUMN staff_numbers TYPE smallint USING staff_numbers::smallint,
    ALTER COLUMN opening_date TYPE date,
    ALTER COLUMN store_type TYPE varchar(255),
    ALTER COLUMN country_code TYPE varchar(3),
    ALTER COLUMN continent TYPE varchar(255);





















