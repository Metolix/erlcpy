# Contributing

## Setup

```bash
python -m pip install -e ".[dev]"
```

## Checks

```bash
ruff check .
pytest
```

## Pull requests

Keep pull requests focused. Public API changes should include tests and documentation.

Do not include API keys, private server data, or webhook secrets in issues, tests, examples, or commits.
