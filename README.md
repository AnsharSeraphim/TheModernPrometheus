# Generic Python Repository Scaffold

This repository is a **pre-setup / prebuild baseline** for new Python projects that need strict automation, reproducible quality checks, and contributor-friendly workflows.

## What this scaffold includes

- Unified pre-commit orchestration (`scripts/run_precommit_suite.py`) for:
  - Ruff format
  - Ruff lint
  - Pylint
  - Interrogate (100% docstring coverage)
  - MyPy
  - Pyright
  - Deptry
  - Vulture
  - Bandit
  - UTF-8 + Unicode escape policy check
- Unified test orchestration (`scripts/run_tests.py`)
- Per-hook JSON skip manifests in `config/precommit_store/`
- Contributor workflow policies and checklist templates

## Quick start

1. Create and activate a virtual environment.
2. Install tooling:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

3. Run quality + tests:

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

## Daily workflow

When iterating on specific paths, run targeted quality checks so manifest state stays current:

```bash
python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
```

Run a single hook if needed:

```bash
python scripts/run_precommit_suite.py --only <hook-id> --scope paths --paths <file1> <file2>
```

Before committing or opening a PR, run the full suites:

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

## UTF-8 policy

Text assets must be valid UTF-8 and must not encode symbolic characters using `\uXXXX` or `\UXXXXXXXX` escape literals where direct UTF-8 symbols are appropriate. The policy is enforced via `scripts/check_unicode_escapes.py` and wired into the unified pre-commit suite.

## Notes for template consumers

- Replace placeholder project metadata in `pyproject.toml`.
- Replace this README with project-specific documentation.
- Keep `docs/release_notes.md` updated as workflow or tooling behavior changes.
