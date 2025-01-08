<!-- README file in MD for the Multination Retail Data Centre repository-->
<a name="readme-top"></a>
<!--


<!-- PROJECT LOGO -->
<p align="center">
  <br>
  Extract, process, and unify data from multiple sources into a single PostgreSQL database.
</p>


<!-- SHIELDS FOR REPO -->
<p align="center">
    <a>
        <img src="https://img.shields.io/badge/language-Python-red"
            alt="Language"></a>
    <a>
        <img src="https://img.shields.io/badge/license-Apache 2.0-red"
            alt="License"></a>
</p>

<!-- ABOUT THE PROJECT -->
## About the Project

### Summary
In this project, I set up a local PostgreSQL database, integrated data from multiple sources, processed it, designed a database schema, and executed SQL queries.

Key technologies: PostgreSQL, AWS S3, Boto3, REST API, CSV, Python (Pandas).

- `Key platforms and technologies`: PostgreSQL, AWS (S3 Buckets, Amazon RDS), REST API
- `Files parsed`: Structured (JSON, CSV), Unstructured (PDF)
- `Languages`: Python

### Project Utilities
 - Data Extraction: The `data_extraction.py` file contains methods for loading data from various sources into Pandas DataFrames.
- Data Cleaning: In `data_cleaning.py`, I implement the DataCleaning class to clean and preprocess the tables imported via `data_extraction.py`.
- Database Upload: The `database_utils.py` file includes the DatabaseConnector class, which creates a database engine using credentials from a .yml file.
- Main Script: The `main.py` file integrates all functionality, enabling seamless data upload to the local PostgreSQL database.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DATABASE SCHEMA -->
