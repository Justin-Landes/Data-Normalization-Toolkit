"""
Test case for the full end-to-end data normalization pipeline.
Ensures the pipeline runs successfully by executing the main script:
- Selects a known test CSV file from the raw data directory.
- Executes the main cleaning pipeline as a subprocess.
- Verifies cleaned CSV file output as a key artifact.
- Verifies SQLite export (if requested) as a key artifact.
"""

# Import necessary modules and set path to normalizer module
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import subprocess
from datetime import datetime

###########################################################

# Set the directories for raw and export data
RAW_DIR = "data/1-CSV-Raw"
EXPORT_DIR = "data/2-CSV-Export"

###########################################################

# Define function to test the full cleaning pipeline
def test_full_cleaning_pipeline():
    # Run DNT pipeline using predefined test CSV and checks if output files were generated
    test_filename = "test_input_sample.csv"
    test_input_path = os.path.join(RAW_DIR, test_filename)
    expected_cleaned_csv = os.path.join(EXPORT_DIR, test_filename.replace(".csv", "_CLEANED.csv"))
    expected_sqlite_export = os.path.join("data/3-SQLite-Export", test_filename.replace(".csv", "_CLEANED.db"))
    
    # Assert file exists
    assert os.path.exists(test_input_path), f"Test input file not found: {test_input_path}"

    # Run the pipeline
    result = subprocess.run(
        [sys.executable, "main.py"],
        text=True,
        # Simulate user input: use file, don't regenerate config, proceed, and export SQLite
        input=f"{test_input_path}\nn\ny\ny\n",
        capture_output=True
    )

    # Show debug info if needed
    if result.returncode != 0:
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

    # Validate run success and files were created
    assert result.returncode == 0, "main.py did not run successfully"
    assert os.path.exists(expected_cleaned_csv), "Cleaned CSV not found"
    assert os.path.exists(expected_sqlite_export), "SQLite DB not found"
    
###########################################################