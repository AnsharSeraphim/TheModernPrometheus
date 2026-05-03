# Generic Python Repository Scaffold

This repository is a template baseline for teams who want strict, wrapper-first automation from day one.

## Repository map

- `scripts/`: Canonical automation entry points and supporting quality/test utilities.
- `tests/`: Verification of wrapper behavior and policy enforcement helpers.
- `config/precommit_store/`: Pre-commit skip ledgers plus cached pylint diagnostics used by wrapper flows.
- `docs/`: Narrative documentation and release history.
- `Final-Productization-Checklist.md`: Open, actionable backlog for unresolved template hardening work.
- `Final-Optimization-Checklist.md`: Tracking for tests above the latency budget with explicit rationale.

## Start here

1. Create and activate a virtual environment.
2. Install dev dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

3. Run the required wrappers (never bypass these at session close):

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

## Wrapper-first contributor policy

- Quality hooks must be driven by `scripts/run_precommit_suite.py` (including checklist-structure validation for `Final-Productization-Checklist.md`).
- Tests must be driven by `scripts/run_tests.py`.
- Direct/manual invocations (`pre-commit run <hook>`, naked `pytest`) are treated as policy violations because they bypass repository summary artifacts and skip-ledger coordination.

## Docstring automation support

- `scripts/aggregate_project_docstrings.py` exports a monolithic JSON catalog of Python module/class/function docstrings for contextual bootstrap workflows.
- Interrogate is configured at 100% coverage in project tooling and is executed via the pre-commit wrapper.

## Documentation expectations for template consumers

- Keep folder-level `README.md` files current so new users and stateless agents can navigate assets without hidden context.
- Update `docs/release_notes.md` whenever tooling behavior, quality workflow, or user-facing repository operation changes.
