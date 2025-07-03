# Data Normalization Toolkit (DNT) v1.01

## Overview
**DNT** is a professional-grade Python tool designed to batch-clean messy CSV datasets using configurable normalization rules stored in a YAML file. It provides a repeatable, testable, and auditable pipeline for data normalization — ideal for data scientists, engineers, and database professionals.

## Who Should Use This Toolkit?
This tool is ideal for:
- Data scientists preparing raw data for analysis or ML pipelines
- Data engineers integrating inconsistent CSV data into ETL workflows
- Analysts and DBAs needing one-click, rule-driven CSV cleanup

---

## What Problem Does DNT Solve?
CSV datasets in the real world often suffer from:
- Inconsistent casing (`"JOHN DOE"` vs `"  john doe  "`)
- Null values (`-`, `""`, `"N/A"`)
- Malformed dates and time stamps
- Unexpected special characters
- Whitespace errors and formatting mismatches

These issues slow down analysis, break data pipelines, and pollute downstream systems.

**DNT v1.01** solves this with:
- Field-specific cleaning rules stored in a YAML config
- A clear logic path for step-by-step cleaning
- Configurable output options (CSV and SQLite)
- A log file and HTML report showing before/after stats and examples

---

## How It Works: Logic Flow
1. User selects a raw CSV file (from `/data/1-CSV-Raw/` or a full path)
2. DNT builds (or reuses) a YAML config which defines how each field should be cleaned
3. Each row is processed using those field-level rules:
   - Trim whitespace
   - Normalize case (lower/title/sentence)
   - Remove invalid characters
   - Convert date formats
   - Replace nulls
4. Cleaned CSV is saved to `/data/2-CSV-Export/`
5. Optionally, data is exported to a SQLite DB in `/data/3-SQLite-Export/`
6. A full log and HTML report is generated in `/logs/` and `/reports/`

---

## Module Roles and Responsibilities
| Module                        | Purpose                                                              |
|-------------------------------|----------------------------------------------------------------------|
| `main.py`                     | Orchestrates the full cleaning pipeline                              |
| `file_selector.py`            | Lets user select a CSV file to process                               |
| `config_builder.py`           | Auto-generates a baseline YAML config based on the input CSV headers |
| `config_loader.py`            | Loads and parses the YAML cleaning config                            |
| `cleaner.py`                  | Applies the field-level cleaning rules to each row                   |
| `rules.py`                    | Core functions for whitespace, casing, date formatting, etc.         |
| `sql_exporter.py`             | Exports the cleaned data to SQLite                                   |
| `reporter.py`                 | Logs all cleaning actions and creates an HTML summary report         |

---

## Expected Output Files
- `data/2-CSV-Export/yourfile_CLEANED.csv` — Cleaned CSV
- `data/3-SQLite-Export/yourfile_CLEANED.db` — SQLite export (optional)
- `logs/run_<timestamp>.log` — Summary of actions and field-level changes
- `reports/run_<timestamp>.html` — Visual HTML report of before/after stats

---

## Configuration Options (YAML)
Each field in the CSV gets its own ruleset in `config/config.yaml`:
```yaml
field_name:
  ignore: false
  replace_nulls_with:
    enabled: true
    value: "Not Specified"
  trim_whitespace: true
  normalize_case: sentence
  remove_invalid_chars: true
  fix_date_format:
    input_format: "%m/%d/%Y"
    output_format: "%Y-%m-%d"
```

You can adjust these rules per field, save the config, and rerun the tool MULTIPLE TIMES without losing the cleaning configuration.  This enables multiple passes of cleaning to get the output exactly as needed.

---

## Testing
- Test data was obtained 23 June 2025 from "311 Service Requests from 2010 to Present" hosted on NYC OpenData: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9/about_data.
- Unit tests: tests/test_cleaner.py, test_rules.py, test_config_builder.py
- End-to-end test: tests/test_end_to_end.py with real input/output checks
- Run tests using: pytest tests/ to obtain 14 successful tests

## Folder Structure
├── config/               # YAML config file
├── data/
│   ├── 1-CSV-Raw/        # Input CSVs
│   ├── 2-CSV-Export/     # Cleaned CSVs
│   └── 3-SQLite-Export/  # Optional SQLite DB Exports
├── docs/                 # README and CHANGELOG files
├── logs/                 # Log files
├── normalizer/           # All core logic modules
├── reports/              # HTML cleaning reports
├── templates/            # HTML report template
├── tests/                # Unit and E2E tests
└── main.py               # Run this script to start cleaning

## Future Versions
Planned features for DNT v2 and beyond:
- Command-line flags for headless/automated runs
- GUI or Streamlit-based config editor
- Cloud export (Postgres, BigQuery, S3)
- Schema validation + error reporting

## License
Standard MIT license applies.