"""
The Reporter.py module will log each run of the normalizer to a timestamped
log file in the /logs/ folder. It will also provide a summary of the DataFrame's 
shape (total rows and columns), null counts (to spot missing data), and unique 
values (to detect potential issues like duplicates or outlier values) as an 
HTML report using a Jinja2 template.
"""

# Import necessary libraries
import os                                          # For file and directory operations
import pandas as pd                                # For handling DataFrames
import logging                                     # For logging messages to a file
from datetime import datetime                      # For generating timestamped log files
from jinja2 import Environment, FileSystemLoader   # For rendering HTML reports via templates

##################################################

# Define the function to set up a logger in a timestamped log file
def setup_logger():
    # Sets up a timestamped logger that outputs to the logs/ folder.
    if not os.path.exists("logs"):
        os.makedirs("logs")
    # Create a timestamp for the log file using a formatted datetime stamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    # Define the log file name with the timestamp included
    log_file = f"logs/run_{timestamp}.log"

    # Configure the logging module to write to the log file
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger()

##################################################

# Define the function to log a message
def summarize_dataframe(df: pd.DataFrame, label: str) -> str:
    # Returns a summary of the DataFrame's shape, null counts, and unique values.
    summary = [f"--- {label.upper()} DATA SUMMARY ---"]
    summary.append(f"Shape: {df.shape}")
    summary.append("\nNull Counts:\n" + str(df.isnull().sum()))
    summary.append("\nUnique Value Counts:\n" + str(df.nunique()))
    # Joins the summary list into a single string with newlines
    return "\n".join(summary)

##################################################

# Define the function to generate an HTML report using Jinja2
def write_html_report(
    input_filename: str,
    config_path: str,
    clean_data_path: str,
    sqlite_path: str,
    pre_summary: str,
    post_summary: str,
    changes: str,
    example_row_number: int,  
):

    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    # Create timestamp for unique report name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = f"reports/run_{timestamp}.html"

    # Load the HTML template from templates/ folder
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report_template.html")

    # Render the HTML with dynamic data
    html_content = template.render(
        timestamp=timestamp,
        input_filename=input_filename,
        config_path=config_path,
        clean_data_path=clean_data_path,
        sqlite_path=sqlite_path,
        pre_summary=pre_summary.replace("\n", "<br>"),
        post_summary=post_summary.replace("\n", "<br>"),
        changes=changes,
        example_row_number=example_row_number
    )

    # Write to HTML file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Return the path to the generated HTML report to main.py
    return output_path

##################################################