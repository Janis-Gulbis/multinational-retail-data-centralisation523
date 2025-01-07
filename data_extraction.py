#%%
import pandas as pd
import requests
import boto3
from io import StringIO
from tabula import read_pdf
from database_utils import DatabaseConnector

class DataExtractor:

    def read_rds_table(self, db_connector, legacy_users):
        #Reads the legacy_users table from an RDS database
        engine = db_connector.init_db_engine()
        query = f"SELECT * FROM {legacy_users}"
        return pd.read_sql(query, con=engine)
    
    def read_rds_table_orders(self, db_connector, orders_table):
        #Reads the orders_table table from an RDS database
        engine = db_connector.init_db_engine()
        query = f"SELECT * FROM {orders_table}"
        return pd.read_sql(query, con=engine)
    
    def retrieve_pdf_data(self, link):
        #Extracts data from the PDF and returns it as a pandas DataFrame
        try:
            df_list = read_pdf(link, pages="all", multiple_tables=True, lattice=True, pandas_options={'dtype': str})
            if df_list:
                return pd.concat(df_list, ignore_index=True)
            return pd.DataFrame()  # Return an empty DataFrame if no tables were extracted
        except Exception as e:
            print(f"Error extracting PDF data: {e}")
            return pd.DataFrame()
    
    def list_number_of_stores(self, endpoint, headers):
        #Gets the total number of stores from the API
        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            return data.get('number_stores', 0)  # Default to 0 if key is missing
        except requests.exceptions.RequestException as e:
            print(f"Error fetching store count: {e}")
            return 0
    
    def retrieve_stores_data(self, endpoint, headers, total_stores):
        #Gets store data from the API for all stores
        stores_data = []
        for store_number in range(total_stores):
            store_url = endpoint.format(store_number=store_number)
            try:
                response = requests.get(store_url, headers=headers)
                response.raise_for_status()
                store_data = response.json()
                stores_data.append(store_data)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching store data for store {store_number}: {e}")
        return pd.DataFrame(stores_data)
    
    def extract_from_s3(self, s3_address):
        #Downloads a file from an S3 bucket and loads it as a pandas DataFrame
        bucket_name, key = s3_address.replace("s3://", "").split("/", 1)
        s3_client = boto3.client('s3')
        file_name = key.split("/")[-1]
        
        try:
            s3_client.download_file(bucket_name, key, file_name)
            return pd.read_csv(file_name)
        except Exception as e:
            print(f"Error extracting data from S3: {e}")
            return pd.DataFrame()
    
    def extract_from_s3_link(self, s3_link):
        #Extracts data from a JSON file from the S3 link and loads it into a pandas DataFrame
        try:
            response = requests.get(s3_link)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            return pd.DataFrame(data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from S3 link: {e}")
            return pd.DataFrame()

# Initialize DatabaseConnector
db_connector = DatabaseConnector()

# List available tables
tables = db_connector.list_db_tables()
print("Available tables:", tables)

#%%