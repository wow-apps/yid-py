---
applyTo: "**/*.md"
---

# Markdown Instructions

## Linting

We use **pymarkdownlnt** for markdown linting.

## Rules

- Headings must have 1 blank line above
- Multiple headings with same content allowed at different levels (MD024)
- No line length limit (MD013 disabled)

## Excluded Files

- `CLAUDE.md` is excluded from linting

## Commands

```bash
# Lint markdown files
pymarkdown --config .pymarkdown scan README.md CONTRIBUTING.md CODE_OF_CONDUCT.md
```

## Configuration

See `.pymarkdown` for linting rules.
