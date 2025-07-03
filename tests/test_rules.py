"""
Test the rules module of the normalizer package. This module contains 
unit tests for various normalization rules such as stripping whitespace, 
normalizing case, removing invalid characters, and fixing date formats.
"""
# Import necessary modules and set path to normalizer module
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from normalizer import rules

######################################################

# Function to test stripping whitespace from strings
def test_strip_whitespace():
    assert rules.strip_whitespace("  Hello  ") == "Hello"
    assert rules.strip_whitespace(123) == 123

######################################################

# Function to test normalizing case of strings
def test_normalize_case():
    assert rules.normalize_case("john DOE", "upper") == "JOHN DOE"
    assert rules.normalize_case("JOHN doe", "lower") == "john doe"
    assert rules.normalize_case("john doe", "title") == "John Doe"
    assert rules.normalize_case("john DOE from over HERE", "sentence") == "John doe from over here"
    assert rules.normalize_case(12345, "upper") == 12345
    assert rules.normalize_case("mixedCASE", "banana") == "mixedCASE"

######################################################

# Function to test removing invalid characters from strings
def test_remove_invalid_chars():
    assert rules.remove_invalid_chars("hello$%^world!") == "helloworld"
    assert rules.remove_invalid_chars("user@site.com") == "user@site.com"
    assert rules.remove_invalid_chars("abc#123") == "abc123"
    assert rules.remove_invalid_chars(42) == 42

######################################################

# Function to test fixing date formats
def test_fix_date_format():
    assert rules.fix_date_format("05/11/2025") == "2025-05-11"
    assert rules.fix_date_format("12/31/2024") == "2024-12-31"
    assert rules.fix_date_format("2025-05-11") == "2025-05-11"  # already in correct format
    assert rules.fix_date_format("not-a-date") == "not-a-date"  # invalid input
    assert rules.fix_date_format(20250511) == 20250511  # non-string input

######################################################