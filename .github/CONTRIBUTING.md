# Contributing to Smart BMI Analyzer

Thank you for considering contributing to Smart BMI Analyzer! We welcome improvements, bug fixes, new features, and documentation updates. This document will help you get started.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```
   git clone https://github.com/your-username/BMI_Analyzer_Project.git
   cd BMI_Analyzer_Project
   ```
3. **Create a new branch** for your change:
   ```
   git checkout -b feature/your-feature-name
   ```

4. **Set up the development environment**:
   ```
   pip install -r requirements.txt
   ```

5. **Make your changes**, write tests, and run the test suite:
   ```
   pytest
   ```

## Code Style

- Follow [PEP8](https://peps.python.org/pep-0008/) conventions.
- Use `black` to format code:
   ```
   black .
   ```
- Use `flake8` to lint code:
   ```
   flake8 .
   ```

## Commit Messages

Write clear, concise commit messages in the imperative tense. Example:
```
Fix bug in BMI classification logic for underweight range
```

## Pull Requests

1. Push your branch:
   ```
   git push origin feature/your-feature-name
   ```
2. Open a pull request (PR) on GitHub to the `main` branch.
3. In the PR description:
   - Describe what your change does.
   - Link to any relevant issues (e.g., `Fixes #3`).
   - Add screenshots or logs if appropriate.

## Reporting Bugs or Suggesting Features

Please use the GitHub [Issues](https://github.com/Justin-Landes/BMI_Analyzer_Project/issues) tab. Be specific and include steps to reproduce where relevant.

## Code of Conduct

Please read and adhere to our [Code of Conduct](CODE_OF_CONDUCT.md).

We appreciate your contributions — thank you for helping make this project better!