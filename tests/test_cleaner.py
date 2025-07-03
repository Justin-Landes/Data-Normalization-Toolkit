"""
Testing the clean_row function from the normalizer module.
This module contains unit tests for the clean_row function,
which applies various normalization rules to a row of data.
"""

# Import libraries and set path to normalizer module
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from normalizer.cleaner import clean_row

##################################################

# Sample input row of messy data to clean
sample_row = {
    # Whitespaces
    "Name": "  JOHN DOE  ",
    # Case normalization
    "Email": "JOHN@EMAIL.COM",
    # Invalid characters and sentence case normalization
    "Message": "Hello/#$% there!!!",
    # Date format to be fixed
    "Date": "5/2/2025"
}

# Minimal YAML-like config dict to use for testing
sample_config = {
    "field_rules": {
        "Name": {
            "trim_whitespace": True,
            "normalize_case": "title",
            "remove_invalid_chars": False,
            "fix_date_format": None,
            "replace_nulls_with": {"enabled": False, "value": ""},
            "ignore": False
        },
        "Email": {
            "trim_whitespace": True,
            "normalize_case": "lower",
            "remove_invalid_chars": False,
            "fix_date_format": None,
            "replace_nulls_with": {"enabled": False, "value": ""},
            "ignore": False
        },
        "Message": {
            "trim_whitespace": True,
            "normalize_case": "sentence",
            "remove_invalid_chars": True,
            "fix_date_format": None,
            "replace_nulls_with": {"enabled": False, "value": ""},
            "ignore": False
        },
        "Date": {
            "trim_whitespace": True,
            "normalize_case": False,
            "remove_invalid_chars": False,
            "fix_date_format": {
                "input_format": "%m/%d/%Y",
                "output_format": "%Y-%m-%d"
            },
            "replace_nulls_with": {"enabled": False, "value": ""},
            "ignore": False
        }
    }
}

##################################################

# Full test of all standard transformations on a multi-field row
def test_clean_row_transforms_fields():
    cleaned, _ = clean_row(sample_row, sample_config)

    # Assert the cleaned values match expected transformations
    assert cleaned["Name"] == "John Doe"
    assert cleaned["Email"] == "john@email.com"
    assert cleaned["Message"] == "Hello there"
    assert cleaned["Date"] == "2025-05-02"

##################################################

# Test case for replacing null values with a fallback
def test_replace_null_with_fallback():
    row = {"Facility": None}
    config = {
        "field_rules": {
            "Facility": {
                "replace_nulls_with": {"enabled": True, "value": "Not Specified"},
                "trim_whitespace": False,
                "normalize_case": False,
                "remove_invalid_chars": False,
                "fix_date_format": None,
                "ignore": False
            }
        }
    }
    cleaned, _ = clean_row(row, config)
    assert cleaned["Facility"] == "Not Specified"

##################################################

# Test case for case normmalization in a full sentence
def test_sentence_case_normalization():
    row = {"Note": "this is a message"}
    config = {
        "field_rules": {
            "Note": {
                "replace_nulls_with": {"enabled": False, "value": ""},
                "trim_whitespace": True,
                "normalize_case": "sentence",
                "remove_invalid_chars": False,
                "fix_date_format": None,
                "ignore": False
            }
        }
    }
    cleaned, _ = clean_row(row, config)
    assert cleaned["Note"] == "This is a message"

##################################################

# Test case for a field that was skipped and had no transformations applied
def test_ignore_field_skips_all_transforms():
    row = {"Agency": "   NYPD   "}
    config = {
        "field_rules": {
            "Agency": {
                "replace_nulls_with": {"enabled": False, "value": ""},
                "trim_whitespace": True,
                "normalize_case": "lower",
                "remove_invalid_chars": True,
                "fix_date_format": None,
                "ignore": True
            }
        }
    }
    cleaned, _ = clean_row(row, config)
    assert cleaned["Agency"] == "   NYPD   "

##################################################

# Test case for a field with invalid data, including a graceful failure
def test_invalid_date_graceful_fail():
    row = {"Date": "bad-date"}
    config = {
        "field_rules": {
            "Date": {
                "replace_nulls_with": {"enabled": False, "value": ""},
                "trim_whitespace": True,
                "normalize_case": False,
                "remove_invalid_chars": False,
                "fix_date_format": {
                    "input_format": "%m/%d/%Y",
                    "output_format": "%Y-%m-%d"
                },
                "ignore": False
            }
        }
    }
    cleaned, _ = clean_row(row, config)
    assert cleaned["Date"] == "bad-date"  # fails gracefully, unchanged

##################################################

# Test case for a numeric field that should pass through unchanged
def test_numeric_field_pass_through():
    row = {"BBL": 1234567890}
    config = {
        "field_rules": {
            "BBL": {
                "replace_nulls_with": {"enabled": False, "value": ""},
                "trim_whitespace": True,
                "normalize_case": "title",  # should be ignored for int
                "remove_invalid_chars": True,
                "fix_date_format": None,
                "ignore": False
            }
        }
    }
    cleaned, _ = clean_row(row, config)
    assert cleaned["BBL"] == 1234567890

##################################################