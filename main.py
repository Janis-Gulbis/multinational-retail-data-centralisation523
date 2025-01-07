
#%%
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

def extract_clean_upload_data(data_extractor, data_cleaning, db_connector, extraction_method, clean_method, table_name, *args, **kwargs):
    
    # A generic function to extract, clean, and upload data to the database
    try:
        # Extracts data using the provided extraction method
        extracted_data = getattr(data_extractor, extraction_method)(*args, **kwargs)

        # Cleans the extracted data using the provided cleaning method
        cleaned_data = getattr(data_cleaning, clean_method)(extracted_data)

        # Uploads cleaned data to the database
        db_connector.upload_to_db(cleaned_data, table_name)
        print(f"Data uploaded successfully to {table_name}")
    except Exception as e:
        print(f"Error processing {table_name}: {e}")

if __name__ == "__main__":
    db_connector = DatabaseConnector()
    data_extractor = DataExtractor()
    data_cleaning = DataCleaning()

    # Extracts, cleans, and uploads data for each data source
    extract_clean_upload_data(data_extractor, data_cleaning, db_connector, 
                              'read_rds_table', 'clean_user_data', 'dim_users', db_connector, 'legacy_users')

    extract_clean_upload_data(data_extractor, data_cleaning, db_connector, 
                              'retrieve_pdf_data', 'clean_card_data', 'dim_card_details', 
                              "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf")

    store_details_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}"
    headers = {"x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
    extract_clean_upload_data(data_extractor, data_cleaning, db_connector, 
                              'retrieve_stores_data', 'clean_store_data', 'dim_store_details', 
                              store_details_endpoint, headers, 451)

    extract_clean_upload_data(data_extractor, data_cleaning, db_connector, 
                              'extract_from_s3', 'clean_products_data', 'dim_products', 
                              "s3://data-handling-public/products.csv")

    extract_clean_upload_data(data_extractor, data_cleaning, db_connector, 
                              'read_rds_table_orders', 'clean_orders_data', 'orders_table', db_connector, 'orders_table')

    extract_clean_upload_data(data_extractor, data_cleaning, db_connector, 
                              'extract_from_s3_link', 'clean_date_data', 'dim_date_times', 
                              "https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json")








  #%%