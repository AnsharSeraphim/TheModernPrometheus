# scripts/

This folder is the operational entry point for repository automation.

## Core wrappers

- `run_precommit_suite.py`: Canonical quality gate runner (Ruff, Pylint, Interrogate, MyPy, Pyright, Deptry, Vulture, Bandit, UTF-8 policy checks).
- `run_tests.py`: Canonical pytest wrapper with scope selection and standardized summary artifacts.

## Supporting utilities

- `precommit_filter.py`: Skip-ledger filter logic used by the pre-commit wrapper.
- `manual_hook_warning.py`: Emits a non-zero redirect message when a contributor runs a hook directly instead of using `run_precommit_suite.py`.
- `_automation_shared.py`: Shared helper functions for diff collection, dependency checks, and subprocess execution.
- `check_unicode_escapes.py`: UTF-8 / Unicode-escape policy validator invoked by the quality suite.
- `check_conflicts.py`: Lightweight merge-conflict marker detector.
- `check_checklist_structure.py`: Guards required checklist governance/audit sections from accidental removal.
- `aggregate_project_docstrings.py`: Exports a JSON catalog of module/class/function docstrings for agent context bootstrapping.

## Test profile assets

- `test_profiles/baseline.txt`: Curated baseline test target set for wrapper-driven test runs.

## Wrapper-first policy

- Use `python scripts/run_precommit_suite.py` instead of naked `pre-commit run` hook aliases.
- Use `python scripts/run_tests.py` instead of naked `pytest` so summary artifacts and scope logic stay consistent.
