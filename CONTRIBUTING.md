# Contributing

This repository is a generic Python automation scaffold that can be reused as a baseline for new projects.

All contributors must follow [AGENTS.md](AGENTS.md) and the [Code of Conduct](CODE_OF_CONDUCT.md).

## Local setup

1. Create and activate a Python 3.13 virtual environment (the repository pins `>=3.13,<3.14`).
2. Install the shared development tooling:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements-dev.txt
   ```
3. Optionally install Git hooks:
   ```bash
   pre-commit install
   ```

## Required quality workflow

The repository uses a unified runner so contributors do not need to remember each lint or type-check command individually.

### While iterating on a subset of files

Run the targeted pre-commit suite for every file you touch:

```bash
python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
```

You can focus on a single hook with:

```bash
python scripts/run_precommit_suite.py --only <hook> --scope paths --paths <file1> <file2>
```

### Before opening a pull request

Run the full automation sequence in this order:

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

Each runner writes a copy-ready summary block under `build/automation_contract/`. Use those blocks in PR notes or review summaries instead of copying incomplete progress logs.

## Tooling inventory

The pre-commit suite currently orchestrates:

- Ruff format
- Ruff lint
- Pylint
- Interrogate (100% docstring coverage)
- MyPy
- Pyright
- Deptry
- Vulture
- Bandit
- UTF-8 + Unicode escape policy checks

## Testing expectations

- Use `python scripts/run_tests.py --scope paths --select <test-path-or-nodeid>` for focused runs.
- Keep individual tests fast. If a new or modified test exceeds 0.20 seconds, document the justification in `Final-Optimization-Checklist.md`.
- Use `Final-Productization-Checklist.md` to record unresolved tooling or productization gaps that are out of scope for the current session.

## Release notes

Update [docs/release_notes.md](docs/release_notes.md) whenever tooling, contributor workflow, or user-visible repository behavior changes.

## Template onboarding

If you are using this repository as a starter template, complete this onboarding path before your first PR:

1. Read `README.md` for repository purpose and layout.
2. Read `AGENTS.md` for wrapper-first policy, required quality gates, and checklist governance.
3. Run the canonical command flow:
   - `python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>` while iterating.
   - `python scripts/run_precommit_suite.py` then `python scripts/run_tests.py` before review.
4. Collect evidence artifacts from `build/automation_contract/` and paste the summary blocks in your PR/testing notes.
5. If a failure cannot be fixed in-session, add a granular remaining-work entry to `Final-Productization-Checklist.md` with scope, target files, dependencies, and DONE WHEN criteria.

Failure/remediation flow:
- Wrapper reports failing hook/test target.
- Remediate implementation (never suppress tooling).
- Re-run wrapper on touched paths.
- Re-run full wrappers before handoff.
