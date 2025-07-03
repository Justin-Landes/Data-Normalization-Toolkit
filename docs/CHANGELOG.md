# Changelog - Data Normalization Toolkit (DNT)

## [v1.0.1] – 2025-07-02
### Fixed
- Added `low_memory=False` to all `pd.read_csv()` calls to suppress dtype warnings.
- Removed duplicate `print()` and `logger` lines during SQLite export.

### Changed
- Simplified program flow to use only interactive mode (no auto-mode).
- Removed all `questionary` dependencies for broader compatibility.
- Converted all terminal outputs to absolute paths.
- Removed YAML preview dump to declutter the cleaning process.

---

## [v1.0.0] – 2025-07-01
### Added
- Initial CLI tool that:
  - Normalizes whitespace, casing, characters, dates, and nulls.
  - Uses YAML config to drive field-specific rules.
  - Generates logs, cleaned CSVs, SQLite DB, and HTML reports.
- Modular architecture with:
  - `cleaner.py`, `config_builder.py`, `reporter.py`, `sql_exporter.py`, `rules.py`
- Unit tests for each module + end-to-end integration test.
