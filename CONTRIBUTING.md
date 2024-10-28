# Contributing

## Setup

```bash
git clone https://github.com/genin402privacy/Genin402.git
cd Genin402
pip install -e ".[dev]"
```

## Tests

```bash
pytest tests/ -v
```

All 106+ tests must pass.

## Code Rules

- Python 3.10+ with type hints
- Dataclasses only in core (no Pydantic outside server.py)
- Analyzer scores: `float` in `[0.0, 100.0]`
- `_SHADOW_PATTERNS` lambdas accept `ShadowTransfer` → return `bool`

## Pull Requests

1. Branch from `main` — name: `feature/`, `fix/`, `chore/`
2. One change per PR
3. Tests required for all new logic
4. Conventional Commits

## Issues

Open a GitHub Issue with wallet context, expected vs actual verdict, and Python version.
