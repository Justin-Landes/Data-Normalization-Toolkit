"""
This script builds a YAML configuration file for field rules based on a sample of a CSV file.
It reads the first few rows of the CSV, extracts column names, and generates default rules 
for each field.  It then writes a YAML template for per-column cleaning settings.  This allows 
the user to quickly set up a normalization configuration, which is built dynamically depending
on the columns contained in the input data.
"""

# Import necessary libraries
import pandas as pd
import yaml

##################################################

# Function to build field rules configuration from a CSV file
def build_field_rules_config(input_csv, output_yaml, sample_size=10):
    # Reads the first few rows of the CSV file to determine the columns
    # Uses low_memory=False to avoid dtype warnings and reads only a sample of rows
    df = pd.read_csv(input_csv, low_memory=False).head(sample_size)
    config = {"field_rules": {}}
    for col in df.columns:
        # Initialize default field rules for each column
        config["field_rules"][col] = {
            # Ignore = False so the field is processed
            "ignore": False,
            # Replace Nulls with "Not Specified" by default
            "replace_nulls_with": {
                "enabled": True,
                "value": "Not Specified"
            },
            # Trim whitespace by default
            "trim_whitespace": True,
            # Normalize case to title case by default, unless it's a description field
            "normalize_case": "sentence" if "description" in col.lower() else "title",
            # Remove invalid characters by default
            "remove_invalid_chars": True,
            # Fix date format if applicable, defaulting to US format
            "fix_date_format": {
                "input_format": "%m%d%Y %H%M",
                "output_format": "%Y-%m-%d %H:%M"
            },
        }

    # Creates the yaml.dump output
    with open(output_yaml, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, sort_keys=False)

    # Lets the user know the config was written
    print(f"Field rules config written to {output_yaml}")

##################################################