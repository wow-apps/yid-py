---
applyTo: "**/*.py"
---

# Python Code Instructions

## Formatting Authority

**ruff is the single source of truth for code formatting and linting.**

- Do NOT suggest formatting changes that conflict with `ruff format`
- Do NOT suggest style changes based on personal preferences
- Run `ruff format .` to verify formatting before suggesting changes
- Run `ruff check .` to verify linting before suggesting changes

## Code Style

- Python 3.10+ required
- Line length: 88 characters (Black-compatible)
- Use modern Python syntax: `match/case`, `str | None`, `list[str]`
- Use `Enum` with `auto()` for enumerations
- Use type hints for all public functions

## Linting Rules (ruff)

Enabled rule sets:
- `E` - pycodestyle errors
- `F` - pyflakes
- `I` - isort (import sorting)
- `UP` - pyupgrade (modern syntax)
- `B` - bugbear (common bugs)
- `SIM` - simplify code

## Type Checking (mypy)

- Strict mode enabled
- All functions must have type annotations
- No `Any` types without explicit ignore
- Use `str | None` instead of `Optional[str]`

## Testing

- pytest with pytest-cov
- Minimum 95% code coverage required
- All public functions must have tests
- Use descriptive test names

## Commands

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Auto-fix lint issues
ruff check --fix .

# Type check
mypy yid_py/

# Run tests
pytest --cov=yid_py --cov-report=term-missing
```
