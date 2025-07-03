"""
This module provides a function to select a CSV file from the /data/1-CSV-Raw directory
or enter a full path manually. It ensures the selected file exists and returns the path.
This version uses basic input() for terminal interaction and supports Pytest automation.
"""

# Import necessary libraries
import os

##########################################################

# Define the function to get the input CSV file path
def get_input_csv_path():
    raw_dir = "data/1-CSV-Raw"

    # Ensure the directory exists
    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir)

    # Get available CSV files in the raw data directory
    csv_files = [
        f for f in os.listdir(raw_dir)
        if f.endswith(".csv") and not f.startswith(".gitkeep")
    ]

    # If running in non-interactive mode for Pytest, return the first CSV file or None
    if os.environ.get("DNT_NO_INTERACTIVE") == "1":
        return os.path.join(raw_dir, csv_files[0]) if csv_files else None

    # User prompt for selecting a CSV file
    print("\nAvailable CSV files in /data/1-CSV-Raw/:")
    if not csv_files:
        print("  [None found]")
    else:
        for i, filename in enumerate(csv_files, start=1):
            print(f"  {i}. {filename}")
    # If no files found, prompt for manual entry of path
    print("  M. Manually enter full path")

    # Ask user for selection
    selection = input("\nChoose a file by number or type 'M' to manually enter path: ").strip()

    # If user selects manual entry
    if selection.lower() == 'm':
        manual_path = input("Enter full path to CSV file: ").strip()
        if os.path.exists(manual_path):
            return manual_path
        else:
            # If the file does not exist, inform the user
            print("File not found.")
            return None
    else:
        # Validate the user's selection
        try:
            index = int(selection) - 1
            if 0 <= index < len(csv_files):
                return os.path.join(raw_dir, csv_files[index])
            else:
                # If the selection is out of range, inform the user
                print("Invalid selection.")
                return None
        except ValueError:
            # If the input is not a valid number, inform the user
            print("Invalid input.")
            return None

##########################################################