# Code of Conduct

This document describes the coding standards and best practices for the project.
All code must pass automated quality checks before merging to main.

## Python

We use **ruff** for linting and formatting, **mypy** for type checking.

### Rules

- Python 3.10+ required
- Line length: 88 characters (Black-compatible)
- Use type hints for all public functions
- Use modern Python syntax (match/case, `str | None`, etc.)

### Lint Rules (ruff)

| Code | Description               |
|------|---------------------------|
| E    | pycodestyle errors        |
| F    | pyflakes                  |
| I    | isort (import sorting)    |
| UP   | pyupgrade (modern syntax) |
| B    | bugbear (common bugs)     |
| SIM  | simplify code             |

### Type Checking (mypy)

- Strict mode enabled
- All functions must have type annotations
- No `Any` types without explicit ignore

### Commands

```bash
# Lint check
ruff check .

# Format check
ruff format --check .

# Auto-fix
ruff check --fix .
ruff format .

# Type check
mypy yid_py/
```

### Configuration

See `pyproject.toml` for `[tool.ruff]` and `[tool.mypy]` sections.

### Useful Links

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Mypy Documentation](https://mypy.readthedocs.io/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [PEP 484 Type Hints](https://peps.python.org/pep-0484/)

## Testing

We use **pytest** with **pytest-cov** for testing and coverage.

### Rules

- Minimum 95% code coverage required
- All public functions must have tests
- Use descriptive test names
- Group tests in classes by functionality

### Commands

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=yid_py --cov-report=term-missing

# Run specific test
pytest tests/test_converter.py::TestToAlphanumeric
```

### Configuration

See `pyproject.toml` for `[tool.pytest.ini_options]` section.

### Useful Links

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

## Markdown

We use **pymarkdownlnt** for linting.

### Rules

- Headings must have 1 blank line above
- Multiple headings with same content allowed at different levels
- No line length limit (MD013 disabled)

### Commands

```bash
# Lint markdown files
pymarkdown --config .pymarkdown scan README.md CONTRIBUTING.md CODE_OF_CONDUCT.md
```

### Configuration

See `.pymarkdown` for linting rules.

### Useful Links

- [pymarkdownlnt Documentation](https://github.com/jackdewinter/pymarkdown)
- [Markdown Guide](https://www.markdownguide.org/)

## Git Workflow

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Fix bug" not "Fixes bug")
- Keep first line under 72 characters
- Reference issues when applicable

### Branch Naming

- `feature/` - new features
- `fix/` - bug fixes
- `docs/` - documentation updates
- `refactor/` - code refactoring

## Pre-commit Checklist

Before committing, ensure:

- [ ] `ruff check .` passes
- [ ] `ruff format --check .` passes
- [ ] `mypy yid_py/` passes
- [ ] `pytest --cov=yid_py` passes with 95%+ coverage
- [ ] All new code has type hints
- [ ] All new functions have tests
