# tests/

This folder validates the repository's automation wrappers and policy helpers.

## Current test modules

- `test_run_tests.py`: Coverage for pytest-wrapper selection logic and execution utilities.
- `test_precommit_filter.py`: Coverage for skip-ledger filtering behaviors.
- `test_manual_hook_warning.py`: Coverage for redirect messaging when direct hook invocations occur.
- `test_check_unicode_escapes.py`: Coverage for UTF-8 and symbolic Unicode-escape policy checks.

## Execution policy

Run tests through:

```bash
python scripts/run_tests.py
```

For targeted execution, prefer wrapper scope/path selection instead of direct `pytest` invocation.
