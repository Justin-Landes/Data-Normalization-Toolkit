"""
The Normalizer Rules are the brains of the cleaning logic.
They define how to transform raw data into a clean, usable format.
The normalizer performs the following tasks on the data:
1. Whitespace Handling: Strips leading and trailing whitespace from strings.
2. Case Normalization: Converts strings to case (lower, upper, title, sentence).
3. Character Sanitization: Removes unwanted characters from strings.
4. Date Format Conversion: Converts date strings from one format to another.
"""

# Import Regular Expressions and datetime for date handling
import re
from datetime import datetime

##################################################

# Define the function to handle whitespace stripping
def strip_whitespace(val):
    # If  value is a string, remove leading and trailing whitespace
    if isinstance(val, str):
        return val.strip()
    # If not a string, return the value unchanged
    # Prevents errors when non-string types are passed
    return val

##################################################

# Define the function to normalize case
def normalize_case(val, case_type="title"):
    # If value is a string, convert to specified case
    # Case type can be 'lower', 'upper', 'title', or 'sentence'
    if not isinstance(val, str):
        return val
    if case_type == "lower":         # Example 'hello world'
        return val.lower()
    elif case_type == "upper":       # Example 'HELLO WORLD'
        return val.upper()
    elif case_type == "title":       # Example 'Hello World'
        return val.title()
    elif case_type == "sentence":    # Example 'Hello world from over here'
        return val[:1].upper() + val[1:].lower()
    # If case_type is not recognized, return the original value
    return val

##################################################

# Define the function to remove unwanted characters
def remove_invalid_chars(val):
    # If value is a string, remove unwanted characters
    # Using REGEX to keep A-Z, a-z, 0-9, whitespace, hyphen, at sign, and period/dot
    # Removing special characters such as !@#$%^&*()_+={}[]|\:;"'<>,?/`~
    if isinstance(val, str):
        # Using regex to keep only wanted characters:
        # ^ means 'not these characters'
        # \w matches alphanumeric characters and underscores
        # \s matches whitespace characters
        # \- matches hyphen
        # @ matches at sign
        # \. matches period/dot
        return re.sub(r"[^\w\s\-@\.]", "", val)
    # If not a string, return the value unchanged
    # Prevents errors when non-string types are passed
    return val

##################################################

# Define the function to fix date formats
def fix_date_format(val, input_format="%m/%d/%Y", output_format="%Y-%m-%d"):
    # If value is string, converts date strings from one format to another.
    # Returns original value if conversion fails.
    if not isinstance(val, str):
        return val 
    try:
        # Tries to parse a string into a datetime object using the input_format
        dt = datetime.strptime(val, input_format)
        # If successful, formats it into a string using the output_format
        return dt.strftime(output_format)
    # If parsing fails, due to invalidate date or format mismatch,
    # It will raise a ValueError, which is caught, and returns the original value
    except ValueError:
        return val
    
##################################################