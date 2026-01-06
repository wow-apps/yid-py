---
applyTo: "**/*"
---

# General Project Instructions

## Project Overview

youtube-id is a Python library for generating YouTube-style short IDs from numbers.
Lightweight, fast, and reversible base62 encoder with optional obfuscation.

## Tech Stack

- Python 3.10+
- Poetry for dependency management
- ruff for linting and formatting
- mypy for type checking
- pytest for testing
- pymarkdownlnt for markdown linting

## Quality Requirements

All code must pass automated quality checks before merging:

1. `ruff check .` - no linting errors
2. `ruff format --check .` - no formatting issues
3. `mypy yid_py/` - no type errors
4. `pytest --cov=yid_py --cov-fail-under=95` - tests pass with 95%+ coverage

## Branch Naming

- `feature/` - new features
- `fix/` - bug fixes
- `docs/` - documentation updates
- `refactor/` - code refactoring
- `test/` - test additions

## PR Title Format

Must start with one of: `feature/`, `fix/`, `docs/`, `refactor/`, `test/`
(case-insensitive)

## Important Notes

- Do NOT suggest changes that conflict with ruff formatting
- ruff is the authority for Python code style, not manual preferences
- All Python code must have type hints
- Zero external dependencies in production code
