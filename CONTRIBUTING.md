# Contributing

Thank you for your interest in contributing to yid-py! This guide will help you get started.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) for dependency management

### Setup

1. Fork and clone the repository:

   ```bash
   git clone https://github.com/your-username/yid-py.git
   cd yid-py
   ```

2. Create a virtual environment:

   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   poetry install --with dev
   ```

## Development Workflow

### Making Changes

1. Create a new branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our [Code of Conduct](CODE_OF_CONDUCT.md)

3. Run quality checks:

   ```bash
   # Lint
   ruff check .

   # Format
   ruff format .

   # Type check
   mypy yid_py/

   # Tests with coverage
   pytest --cov=yid_py --cov-report=term-missing
   ```

4. Commit your changes:

   ```bash
   git add .
   git commit -m "Add your descriptive message"
   ```

### Code Quality Requirements

All contributions must:

- Pass `ruff check` with no errors
- Pass `ruff format --check` with no changes needed
- Pass `mypy` strict type checking
- Maintain 95%+ test coverage
- Include type hints for all public functions
- Include tests for new functionality

## Pull Request Process

1. Update documentation if needed
2. Ensure all checks pass
3. Create a pull request with a clear description
4. Link any related issues

### PR Title Format

- `feat: Add new feature`
- `fix: Fix bug description`
- `docs: Update documentation`
- `refactor: Refactor code`
- `test: Add tests`

## Branch Naming

| Prefix      | Purpose          |
|-------------|------------------|
| `feature/`  | New features     |
| `fix/`      | Bug fixes        |
| `docs/`     | Documentation    |
| `refactor/` | Code refactoring |
| `test/`     | Test additions   |

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Minimal code example to reproduce
- Expected vs actual behavior

## Questions?

Feel free to open an issue for any questions or suggestions.
