"""
Test cases for the configuration builder module.
Creates a sample CSV file, builds a YAML configuration from it,
and verifies the structure and content of the generated YAML.
"""

# Import necessary libraries and set path to normalizer module
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import yaml
from normalizer.config_builder import build_field_rules_config

##################################################

# Create a sample CSV for testing
SAMPLE_CSV_PATH = "tests/sample_config_test.csv"
SAMPLE_YAML_PATH = "tests/generated_test_config.yaml"

##################################################

# Function to set up the test environment with sample CSV data
def setup_module(module):
    """Create a sample CSV before running tests."""
    df = pd.DataFrame([
        {
            "ID": 1,
            "Name": "Alice",
            "Email": "ALICE@EXAMPLE.COM",
            "Resolution Description": "police RESPONDED and left"
        },
        {
            "ID": 2,
            "Name": "Bob",
            "Email": "bob@example.com",
            "Resolution Description": "officers ARRIVED at location"
        }
    ])
    df.to_csv(SAMPLE_CSV_PATH, index=False)

##################################################

# Function to tear down the test environment by removing generated files
def teardown_module(module):
    """Clean up generated test files after tests finish."""
    os.remove(SAMPLE_CSV_PATH)
    if os.path.exists(SAMPLE_YAML_PATH):
        os.remove(SAMPLE_YAML_PATH)

##################################################

# Function to test if the YAML configuration is created and valid
def test_config_yaml_is_created_and_valid():
    # Build YAML config from sample CSV
    build_field_rules_config(SAMPLE_CSV_PATH, SAMPLE_YAML_PATH)

    # Confirm YAML file exists
    assert os.path.exists(SAMPLE_YAML_PATH)

    # Load it and check structure
    with open(SAMPLE_YAML_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Check if the config has expected keys
    field_rules = config.get("field_rules", {})
    assert "Resolution Description" in field_rules
    assert "Name" in field_rules
    assert isinstance(field_rules["Name"], dict)

##################################################

# Function to test if the Resolution Description field is using the sentence case
def test_resolution_description_uses_sentence_case():
    build_field_rules_config(SAMPLE_CSV_PATH, SAMPLE_YAML_PATH)
    with open(SAMPLE_YAML_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    case_setting = config["field_rules"]["Resolution Description"]["normalize_case"]
    assert case_setting == "sentence"

##################################################

# Function to test if all fields in the YAML config have the expected keys
def test_all_fields_have_expected_keys():
    build_field_rules_config(SAMPLE_CSV_PATH, SAMPLE_YAML_PATH)
    with open(SAMPLE_YAML_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    expected_keys = {"ignore", "replace_nulls_with", "trim_whitespace",
                     "normalize_case", "remove_invalid_chars", "fix_date_format"}

    for field_config in config["field_rules"].values():
        assert expected_keys.issubset(set(field_config.keys()))

##################################################