#%%
import yaml
from sqlalchemy import create_engine, text

class DatabaseConnector:
    def read_source_db_creds(self, filepath='db_creds.yaml'):
        #Reads credentials for the source database
        with open(filepath, 'r') as file:
            creds = yaml.safe_load(file)
        return creds

    def read_target_db_creds(self, filepath='db_creds_upload.yaml'):
        #Reads credentials for the target database
        with open(filepath, 'r') as file:
            creds = yaml.safe_load(file)
        return creds

    def init_db_engine(self):
        #Initialises the engine for the source database
        creds = self.read_source_db_creds()
        engine = create_engine(
            f"postgresql+psycopg2://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}"
        )
        return engine

    def list_db_tables(self):
        #Lists all tables within the source database
        engine = self.init_db_engine()
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            )
            tables = [row[0] for row in result]
        return tables

    def upload_to_db(self, dataframe, table_name, db_name='sales_data'):
        #Uploads data to the target database
        creds = self.read_target_db_creds()
        engine = create_engine(
            f"postgresql+psycopg2://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{db_name}"
        )
        dataframe.to_sql(table_name, engine, if_exists='replace', index=False)

#%%