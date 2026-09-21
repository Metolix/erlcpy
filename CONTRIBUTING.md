# Contributing

Thanks for contributing to erlcpy.

erlcpy is a small, typed Python client for the ER:LC Private Server API. The project aims to keep its public API predictable, its dependencies small, and its implementation easy to maintain.

## Before you start

For a bug fix, documentation change, or small improvement, open an issue first when the change is likely to affect the public API or overall project direction. For straightforward fixes, you can open a pull request directly.

Please search existing issues and pull requests before opening a new one.

## Development setup

erlcpy supports Python 3.10 and newer.

```bash
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install development dependencies:
```bash
python -m pip install -e ".[dev]"
```

## Running checks
```bash
ruff check .
pytest
```

Run both commands before opening a pull request. Changes to webhook verification, HTTP behavior, models, error handling, or other public behavior should include tests.

## Project structure
```text
src/erlcpy/       Package source
tests/             Test suite
examples/          Usage examples
docs/              API and design documentation
.github/           CI and repository templates
```

Keep implementation code in `src/erlcpy`. Avoid adding scripts or files without a clear maintenance or user-facing purpose.

## Code style
- Follow the existing project structure.
- Keep functions and classes focused.
- Prefer explicit, readable code over clever abstractions.
- Preserve type annotations.
- Keep the public API small and intentional.
- Use the standard library where it is sufficient.
- Avoid unnecessary dependencies.
- Keep error messages useful without exposing credentials or private data.
- Do not silently change existing public behavior.
- Do not add automatic retries to commands unless explicitly designed and documented; repeating a command can have side effects.

Ruff is the project's source of truth for linting.

## API changes

For public API changes:
1. Update the implementation.
2. Add or update tests.
3. Update documentation.
4. Update affected examples.
5. Consider backward compatibility.
6. Keep the change aligned with the official ER:LC API documentation.

If the ER:LC API itself changes, link the relevant official documentation in the pull request description. Do not invent undocumented API behavior when a documented alternative exists.

## Models

Keep API models typed and predictable. Match official API fields closely, handle missing optional data safely, preserve useful raw API data where the existing pattern does so, and add tests for new fields.

Avoid restrictive enums for API values unless the API guarantees those values are stable.

## HTTP behavior

Preserve useful HTTP status information, documented error details, authentication failures, and rate-limit information when changing request handling.

Be especially careful with retries: POST requests execute in-game commands and should not be automatically repeated without an explicit design.

Never log authenticated request headers.

## Webhooks

Webhook changes require tests for valid and invalid signatures.

Use synthetic keys and payloads in tests. Never use production webhook credentials.

Verify changes against the current ER:LC documentation before submitting them.

## Tests

Tests should be deterministic, fast, independent of a live ER:LC server, free of credentials, and focused on observable behavior.

Use mocked HTTP responses for API client tests. The normal test suite must not require a real ER:LC private server.

## Documentation

Document behavior users can actually rely on. Keep examples short and runnable. When a public API changes, update the README or the appropriate page under `docs/`.

## Commits

Use short, descriptive commit messages.

```text
Add queue endpoint
Fix rate limit parsing
Update webhook docs
Test command errors
```

Avoid commit messages that contain unnecessary detail or references to tools used to make the change.

## Pull requests

A good pull request should explain what changed, why it changed, any public API changes, how it was tested, and compatibility or migration considerations.

Keep pull requests focused.

Before opening a pull request:
- [ ] Tests pass.
- [ ] Ruff passes.
- [ ] Documentation is updated when needed.
- [ ] Examples still make sense when affected.
- [ ] No credentials or private server data are included.
- [ ] Public API changes are clearly described.

## Security

Never include ER:LC server keys, global API keys, webhook secrets, access tokens, or private server data in commits, issues, pull requests, examples, or tests.

See [SECURITY.md](SECURITY.md) for vulnerability reporting and security guidance.