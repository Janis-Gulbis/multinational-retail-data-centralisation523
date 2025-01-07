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
    
    def clean_user_data(self, user_data_df):
        #Cleans the user data DataFrame
        user_data_df = self.replace_nulls(user_data_df)
        user_data_df = self.drop_na(user_data_df)
        
        # Converts 'join_date' to datetime and drop rows with invalid dates
        user_data_df['join_date'] = pd.to_datetime(user_data_df['join_date'], errors='coerce')
        return self.drop_na(user_data_df, subset=['join_date'])
    
    def clean_card_data(self, df):
        #Cleans the card data DataFrame
        df = self.replace_nulls(df)
        
        # Ensures 'card_number' column is a string and remove NaN values before checking digits
        df['card_number'] = df['card_number'].astype(str)
        df = df[df['card_number'].notna()]  # Removes rows with NaN card numbers
        df = df[df['card_number'].str.isdigit()]  # Keeps only numeric card numbers
        
        # Removes duplicates based on card_number
        df = df.drop_duplicates(subset=['card_number'], keep='first')
        
        # Converts 'date_payment_confirmed' to datetime and drop rows with invalid dates
        df['date_payment_confirmed'] = pd.to_datetime(df['date_payment_confirmed'], errors='coerce')
        return self.drop_na(df, subset=['date_payment_confirmed'])
    
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
    
    def clean_products_data(self, products_df):
        #Cleans the products data DataFrame
        products_df = self.replace_nulls(products_df)
        products_df = self.drop_na(products_df)

        # Cleans 'product_price' column
        products_df['product_price'] = products_df['product_price'].replace({'£': '', ',': ''}, regex=True)
        products_df['product_price'] = pd.to_numeric(products_df['product_price'], errors='coerce')
        
        # Converts 'date_added' to datetime
        products_df['date_added'] = pd.to_datetime(products_df['date_added'], errors='coerce')
        
        # Cleans 'removed' column
        products_df['removed'] = products_df['removed'].replace({'Still_avaliable': 'Available', 'Removed': 'Not Available'})

        # Ensures 'uuid' column has no erroneous values
        products_df['uuid'] = products_df['uuid'].apply(lambda x: str(x) if isinstance(x, str) else pd.NA)

        # Drop rows with NaN in critical columns
        products_df = self.drop_na(products_df, subset=['product_name', 'product_price', 'date_added', 'uuid'])

        # Convert 'weight' to kg
        def clean_weight(value):
            """Convert weight to kg."""
            try:
                match = re.match(r"([\d.]+)\s*(kg|g|ml)?", str(value).lower())
                if match:
                    weight, unit = float(match.group(1)), match.group(2)
                    if unit == "kg" or unit is None:
                        return weight
                    elif unit == "g":
                        return weight / 1000
                    elif unit == "ml":
                        return weight / 1000
                return pd.NA
            except Exception as e:
                return pd.NA
        
        products_df["weight"] = products_df["weight"].apply(clean_weight)
        return self.drop_na(products_df, subset=["weight"]).astype({'weight': float})
    
    def clean_orders_data(self, orders_data_df):
        #Cleans the orders data DataFrame.
        orders_data_df = self.replace_nulls(orders_data_df)
        
        # Drops unnecessary columns
        columns_to_drop = ['first_name', 'last_name', '1']
        orders_data_df.drop(columns=columns_to_drop, inplace=True, errors='ignore')
        
        # Drops rows with NaN in critical columns
        critical_columns = ['date_uuid', 'user_uuid', 'card_number', 'store_code', 'product_code']
        orders_data_df = self.drop_na(orders_data_df, subset=critical_columns)
        
        # Converts columns to appropriate data types
        orders_data_df['card_number'] = orders_data_df['card_number'].astype(str)
        orders_data_df['date_uuid'] = orders_data_df['date_uuid'].astype(str)
        orders_data_df['user_uuid'] = orders_data_df['user_uuid'].astype(str)
        
        # Remove duplicates
        orders_data_df = orders_data_df.drop_duplicates()
        
        return orders_data_df
    
    def clean_date_data(self, date_data_df):
        #Cleans the date data DataFrame
        date_data_df = self.replace_nulls(date_data_df)
        date_data_df = self.drop_na(date_data_df)
        
        # Convert 'day', 'month', and 'year' columns to numeric
        numeric_columns = ['day', 'month', 'year']
        for col in numeric_columns:
            if col in date_data_df.columns:
                date_data_df[col] = pd.to_numeric(date_data_df[col], errors='coerce')
        
        return self.drop_na(date_data_df, subset=numeric_columns)

#%%