"""
This module provides the function to export cleaned DataFrames to SQLite.
This export allows users to save their cleaned data for further analysis, 
reporting, or integration with other database systems.
"""

# Import necessary libraries
import pandas as pd
import sqlite3

##################################################

# Define function to export DataFrame to SQLite
def export_to_sqlite(df: pd.DataFrame, db_path: str, table_name: str = "cleaned_data"):
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

##################################################