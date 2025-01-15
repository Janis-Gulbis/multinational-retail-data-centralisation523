<!-- README file in MD for the Multination Retail Data Centre repository-->
<a name="readme-top"></a>

# Extracting, Integrating, and Transforming  Data from Diverse Sources into a Unified PostgreSQL Database.

<!-- SHIELDS FOR REPO -->
<p align="left">
    <a>
        <img src="https://img.shields.io/badge/language-Python-red"
            alt="Language"></a>
   
</p>

<!-- ABOUT THE PROJECT -->
## About the Project

### Summary
In this project, I set up a local PostgreSQL database, integrated data from multiple sources, processed it, designed a database schema, and executed SQL queries.

Key technologies: PostgreSQL, AWS S3, Boto3, REST API, CSV, Python (Pandas).

- `Key platforms and technologies`: PostgreSQL, AWS (S3 Buckets, Amazon RDS), REST API
- `Files parsed`: Structured (JSON, CSV), Unstructured (PDF)
- `Languages`: Python

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Project Utilities
 - Data Extraction: The `data_extraction.py` file contains methods for loading data from various sources into Pandas DataFrames.
- Data Cleaning: In `data_cleaning.py`, I implement the DataCleaning class to clean and preprocess the tables imported via `data_extraction.py`.
- Database Upload: The `database_utils.py` file includes the DatabaseConnector class, which creates a database engine using credentials from a .yml file.
- Main Script: The `main.py` file integrates all functionality, enabling seamless data upload to the local PostgreSQL database.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DATABASE SCHEMA -->
