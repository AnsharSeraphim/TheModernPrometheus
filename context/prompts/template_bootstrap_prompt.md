# Template Bootstrap Prompt

## Purpose

Guide first-session customization for repositories created from this template.

## Ingestion order

1. `README.md`
2. `docs/new_user_onboarding.md`
3. `AGENTS.md`
4. `Final-Productization-Checklist.md`
5. `docs/runtime_target_support_matrix.md`

## Canonical commands

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python scripts/run_precommit_suite.py --scope all
python scripts/run_tests.py
```

## Evidence requirements

- Confirm wrapper-first workflows are documented for new contributors.
- Confirm unresolved setup gaps are added to the checklist with explicit dependencies.
- Record final automation summary blocks for onboarding evidence.

## Closure criteria

- Bootstrap docs and checklist are aligned to current implementation.
- First-run validation output exists from both wrappers.
