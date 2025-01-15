#%%
import pandas as pd
import re

class DataCleaning:
    
    def replace_nulls(self, df):
        # Helper method to replace 'NULL' strings with NaN values
        return df.replace("NULL", pd.NA)
    
    def drop_na(self, df, subset=None):
        #Helper method to drop rows with NaN values. Optionally, specify columns to check
        return df.dropna(subset=subset, how='any')
    
    def clean_store_data(self, store_data_df):
            #Cleans the store data DataFrame
            store_data_df = self.replace_nulls(store_data_df)
            
            # Drops 'lat' column
            store_data_df = store_data_df.drop(columns=['lat'], errors='ignore')
            
            # Removes rows with 10-character codes across multiple columns
            columns_to_check = ['address', 'longitude', 'locality', 'store_code', 'staff_numbers', 'opening_date', 'store_type', 'latitude', 'country_code', 'continent']
            store_data_df = store_data_df[~store_data_df[columns_to_check].apply(lambda x: x.str.match(r'^[A-Za-z0-9]{10}$', na=False)).any(axis=1)]
            
            # Converts 'opening_date' to datetime and drop rows with invalid dates
            store_data_df['opening_date'] = pd.to_datetime(store_data_df['opening_date'], errors='coerce')
            store_data_df = self.drop_na(store_data_df, subset=['opening_date'])
            
            # Cleans 'staff_numbers' column by removing non-digit characters
            store_data_df['staff_numbers'] = store_data_df['staff_numbers'].str.replace(r'[^\d]', '', regex=True)
            
            return store_data_df


from data_extraction import DataExtractor
from database_utils import DatabaseConnector

# Initialize required classes
db_connector = DatabaseConnector()
data_extractor = DataExtractor()

# Step 1: Extract data from the PDF
pdf_link = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"  # Replace with the actual PDF link
raw_pdf_data = data_extractor.retrieve_pdf_data(pdf_link)

print("Raw PDF Data:")
print(raw_pdf_data.head())  # Inspect the extracted data

# Step 2: Upload the raw data to the database
raw_table_name = "raw_card_details"  # Target table for raw data
db_connector.upload_to_db(raw_pdf_data, raw_table_name)

print(f"\nRaw data uploaded to the '{raw_table_name}' table in the database.")

#%%

#%%
import pandas as pd
import re

class DataCleaning:
    def replace_nulls(self, df):
        # Helper method to replace 'NULL' strings with NaN values
        return df.replace("NULL", pd.NA)
    
    def drop_na(self, df, subset=None):
        # Helper method to drop rows with NaN values. Optionally, specify columns to check
        return df.dropna(subset=subset, how='any')
    
    def clean_store_data(self, store_data_df):
        # Cleans the store data DataFrame
        store_data_df = self.replace_nulls(store_data_df)
        
        # Drops 'lat' column if present
        store_data_df = store_data_df.drop(columns=['lat'], errors='ignore')
        
        # Removes rows with 10-character codes across multiple columns
        #columns_to_check = ['address', 'longitude', 'locality', 'store_code', 'staff_numbers', 'opening_date', 'store_type', 'latitude', 'country_code', 'continent']
        #store_data_df = store_data_df[~store_data_df[columns_to_check].apply(lambda x: x.str.match(r'^[A-Za-z0-9]{10}$', na=False)).any(axis=1)]
        
        # Converts 'opening_date' to datetime
        store_data_df['opening_date'] = pd.to_datetime(store_data_df['opening_date'], errors='coerce')
        store_data_df = self.drop_na(store_data_df, subset=['opening_date'])
        
        # Cleans 'staff_numbers' column by removing non-digit characters
        store_data_df['staff_numbers'] = store_data_df['staff_numbers'].str.replace(r'[^\d]', '', regex=True)
        
        return store_data_df


from data_extraction import DataExtractor
from database_utils import DatabaseConnector

# Initialize required classes
db_connector = DatabaseConnector()
data_extractor = DataExtractor()
data_cleaning = DataCleaning()

# API details
store_details_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}"
headers = {"x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
total_stores = 451  # Total number of stores

# Step 1: Extract store data
store_data = data_extractor.retrieve_stores_data(store_details_endpoint, headers, total_stores)

print("Extracted Store Data:")
print(store_data)  # Inspect the extracted store data

# Step 2: Clean the extracted data
cleaned_store_data = data_cleaning.clean_store_data(store_data)

print("Cleaned Store Data:")
print(cleaned_store_data)  # Inspect the cleaned data

# Step 3: Upload the cleaned data to the database
target_table_name = "dim_store_details"  # Target table for cleaned store data
db_connector.upload_to_db(cleaned_store_data, target_table_name)


print(f"\nCleaned store data uploaded to the '{target_table_name}' table in the database.")
#%%