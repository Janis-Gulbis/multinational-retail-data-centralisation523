-- Cast table datatypes

ALTER TABLE public.dim_card_details
ALTER COLUMN card_number TYPE VARCHAR(19);

ALTER TABLE public.dim_card_details
ALTER COLUMN expiry_date TYPE VARCHAR(5);

ALTER TABLE public.dim_card_details
ALTER COLUMN date_payment_confirmed TYPE DATE
USING date_payment_confirmed::DATE;

