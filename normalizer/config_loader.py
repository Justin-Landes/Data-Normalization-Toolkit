"""
This Script loads the config/config.yaml file
and uses it to clean a sample CSV dataset.
"""

# Import necessary libraries
import yaml

##################################################

# Define function to load a YAML configuration file with error handling
def load_config(path: str) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    # Handle error from missing YAML file
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at path: {path}")
    # Handle error partsing YAML content
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML config: {e}")

##################################################