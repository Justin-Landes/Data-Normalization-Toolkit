"""
Welcome to the Data Normalization Toolkit (DNT) v1.01.
This tool normalizes a CSV file using customizable rules defined in a YAML config.
The logic flow is as follows:
1. User selects a CSV file from /data/1-CSV-Raw or enters a full path
2. DNT validates the desired file exists
3. DNT checks for an existing YAML config file in /config/, creates if not found
4. User decides to regenerate a fresh config from CSV file or use existing config
5. User confirms the config is acceptable for cleaning to proceed
6. DNT cleans the CSV data according to the YAML config and exports a clean copy
7. User decides if they also want a SQLite table of the cleaned data (optional)
8. DNT exports the cleaned data to a SQLite database using the same name as the CSV
9. DNT produces a detailed log and an HTML report of the cleaning process
"""

# Import necessary libraries
import os                            # For file and directory operations   
import pandas as pd                  # For data manipulation and analysis
import normalizer.file_selector      # Selects input CSV file, supports testing

# Import custom modules
from normalizer.file_selector import get_input_csv_path           # User identifies source CSV file
from normalizer.config_loader import load_config                  # Loads the YAML config file
from normalizer.config_builder import build_field_rules_config    # Creates config from CSV sample
from normalizer.reporter import setup_logger                      # Creates a log file
from normalizer.reporter import summarize_dataframe               # Summarizes the data for logging
from normalizer.reporter import write_html_report                 # Generates HTML report 
from normalizer.cleaner import clean_row                          # Cleans a row based on config
from normalizer.sql_exporter import export_to_sqlite              # Exports clean data to SQLite

##################################################

# Define the main function
def main():
    # Initial program message
    print("Welcome to the Data Normalization Toolkit (DNT) v1.01.")
    print("This tool normalizes a CSV file using customizable rules defined in a YAML config.")
    print("Review the README.md for more details on how to use this tool.")

    # Set up the logger to log to a file in /logs/
    logger = setup_logger()

    # Step 1: Prompt for CSV path
    input_csv = get_input_csv_path()
    if not input_csv:
        # If no CSV path is provided, exit the program
        return
    logger.info(f"Input CSV file: {input_csv}")

    # Step 2: Handle YAML config: create new, regenerate fresh, or use existing as-is
    config_path = "config/config.yaml"
    config_exists = os.path.exists(config_path)
    # If config file doesn't exist, build new by reading the CSV columns
    if not config_exists:
        build_field_rules_config(input_csv, config_path)
        logger.info(f"Generated new config: {config_path}")
    # If config already exists, ask user if they want to regenerate it or retain current config
    else:
        print("A config file already exists.")
        regen = input("Do you want to regenerate a fresh config from the CSV file? (y/n): ").strip().lower()
        if regen == "y":
            # If user chooses to regenerate a new baseline, build a fresh config from CSV columns
            build_field_rules_config(input_csv, config_path)
            logger.info(f"Regenerated fresh config.")
        else:
            # If user chooses not to regenerate, use existing config
            logger.info("Using existing config as-is.")

    # Step 3: Confirm config is acceptable for cleaning
    confirm = input("Is this config acceptable for cleaning the CSV file? (y/n): ").strip().lower()
    if confirm != "y":
        # If user does not confirm, exit the program
        print("Cleaning aborted.")
        return

    # Step 4: Load config and the dirty source CSV
    print(f"Loading: {input_csv}")
    config = load_config(config_path)
    # Read the CSV file into a DataFrame
    # Use low_memory=False to avoid memory warnings on large files
    df = pd.read_csv(input_csv, low_memory=False)

    # Step 5: Log pre-clean summary
    logger.info(summarize_dataframe(df, "Pre-Clean"))

    # Step 6: Clean the rows using YAML config settings
    print("\nCleaning rows...")
    cleaned_rows = []
    # Loop through each row in the DataFrame
    for i, row in df.iterrows():
        cleaned, changes = clean_row(row.to_dict(), config)
        cleaned_rows.append(cleaned)
    # If changes are made to the data, log for post-cleaning review
    if changes:
        logger.info(f"Changes detected in row {i + 1}:")
        for field, diff in changes.items():
            logger.info(f"  {field}: '{diff['from']}' ➜ '{diff['to']}'")
    # Convert cleaned rows back to DataFrame
    cleaned_df = pd.DataFrame(cleaned_rows)

    # Step 7: Post-clean summary
    logger.info(summarize_dataframe(cleaned_df, "Post-Clean"))

    # Step 8: Save cleaned CSV to /data/2-CSV-Export
    output_dir = "data/2-CSV-Export"
    os.makedirs(output_dir, exist_ok=True)
    # Append file name with "_CLEANED" to clearly indicate post-cleaning status
    output_filename = os.path.basename(input_csv).replace(".csv", "_CLEANED.csv")
    output_path = os.path.join(output_dir, output_filename)
    cleaned_df.to_csv(output_path, index=False)
    print(f"Cleaned CSV: {os.path.abspath(output_path)}")

    # Step 9: Ask user if they want to export cleaned data to SQLite
    confirm_sql = input("Export cleaned data to SQLite? (y/n): ").strip().lower()
    # If user confirms, set export_sqlite to True
    if confirm_sql.startswith("y"):
        logger.info("User confirmed SQLite export.")
        print("Exporting cleaned data to SQLite...")
        export_sqlite = True
    # If user declines, set export_sqlite to False
    else:
        logger.info("User declined SQLite export.")
        print("Skipping SQLite export.")
        export_sqlite = False

    # Step 9B: If exporting to SQLite is true, create the directory and export
    db_path = None
    if export_sqlite == True:
        # Ensure the directory exists for SQLite export
        os.makedirs("data/3-SQLite-Export", exist_ok=True)
        # Append "_CLEANED" to the database name to match the cleaned CSV
        db_name = os.path.basename(input_csv).replace(".csv", "_CLEANED.db")
        db_path = os.path.join("data/3-SQLite-Export", db_name)
        export_to_sqlite(cleaned_df, db_path, table_name="cleaned_data")
        absolute_db_path = os.path.abspath(db_path)
        # Log the SQLite export path and print to terminal for user awareness
        message = f"SQLite export: {absolute_db_path}"
        logger.info(message)
        print(message)

    # Step 10: Create the post-cleaning HTML Report for user review
    report_path = write_html_report(
        input_filename=os.path.basename(input_csv),
        config_path=config_path,
        clean_data_path=output_path,
        sqlite_path=db_path if export_sqlite else None,
        pre_summary=summarize_dataframe(df, "Pre-Clean"),
        post_summary=summarize_dataframe(cleaned_df, "Post-Clean"),
        changes=changes if changes else None,
        example_row_number=i + 1 if changes else None
    )

    # Step 11: Print final messages
    print(f"Log file: {logger.handlers[0].baseFilename}")
    print(f"HTML report: {os.path.abspath(report_path)}")

##################################################

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()

##################################################
# End of main.py
