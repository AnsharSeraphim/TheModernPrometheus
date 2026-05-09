# Troubleshooting Guide

This playbook consolidates the most common repository workflow failures and their canonical remediation paths.

## Scope and intent

Use this guide when wrapper execution, quality tooling, or policy checks fail and you need a fast path to recovery that stays compliant with `AGENTS.md`.

This document is operational and implementation-aligned; it does not replace wrapper output. Always treat wrapper diagnostics as source of truth.

## Failure 1: Missing dependencies or wrong Python runtime

### Symptoms

- Wrapper exits early with missing module/import errors.
- Pre-commit hooks fail before analyzing files.
- Type checkers disagree unexpectedly after environment recreation.

### Root cause

Repository tooling is pinned for Python `>=3.13,<3.14` and expects the development dependency set from `requirements-dev.txt`.

### Remediation

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
```

If your interpreter is outside the supported range, recreate the environment with Python 3.13 and reinstall.

## Failure 2: Wrapper invocation mistakes

### Symptoms

- `pre-commit run <hook>` or `pytest` was used directly.
- Manual hook aliases print redirect guidance.
- Wrapper evidence artifacts are missing after a run.

### Root cause

Direct invocations bypass wrapper-ledger semantics, policy checks, and standard summary output.

### Remediation

Use the canonical wrappers only:

```bash
python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
python scripts/run_tests.py --scope paths --select <pytest-selector>
```

Before handoff/PR, always run full suites in order:

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

## Failure 3: Stale-ledger confusion in `config/precommit_store/`

### Symptoms

- A hook appears to skip files you expected to recheck.
- Diagnostics look inconsistent with recent edits.
- Contributors suspect JSON manifests are stale.

### Root cause

Skip ledgers are generated state managed by the wrapper and are sensitive to run scope.

### Remediation

- Never hand-edit `config/precommit_store/*.json`.
- Re-run the wrapper in path scope for all touched files so skip flags reset automatically.
- If baseline drift is suspected, reset via wrapper controls:

```bash
python scripts/run_precommit_suite.py --reset-baseline
```

Or targeted reset for one hook:

```bash
python scripts/run_precommit_suite.py --reset-baseline --only <hook>
```

For repository-wide remote validation (for example CI), use full-check mode so all hooks execute regardless of prior skip flags:

```bash
python scripts/run_precommit_suite.py --scope all --reset-baseline --filter-mode full
```

## Failure 4: Interrogate/docstring coverage violations

### Symptoms

- Pre-commit summary reports interrogate failure.
- Missing docstrings are not obvious from hook output alone.

### Root cause

Interrogate enforces 100% docstring coverage. Hook output is concise by design.

### Remediation

The pre-commit wrapper automatically generates the inventory report when interrogate fails. Manual regeneration command:

```bash
python scripts/audit_docstrings.py --scan-root scripts --output build/automation_contract/docstring_inventory.md
```

Resolve `## Scan failures` rows first (if any), then use `## Missing docstrings` to remediate impacted files and rerun targeted wrapper checks:

```bash
python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
```

## Failure 5: Test-scope selection mistakes

### Symptoms

- `run_tests.py --scope paths --select ...` returns no tests.
- Wrong node ID/path causes unexpected deselection.
- Session validation misses changed behavior.

### Root cause

Selector mismatch or incorrect scope assumptions.

### Remediation

- Use file paths (`tests/test_x.py`) or explicit node IDs (`tests/test_x.py::test_case`).
- If uncertain, run changed scope or baseline profile through wrapper.
- Always run full suite before final handoff:

```bash
python scripts/run_tests.py
```

## Failure 6: Unresolved failures cannot be remediated in-session

### Symptoms

- A quality/test failure requires larger refactors than session scope.
- Required context/assets are missing to finish safely.

### Root cause

Work exceeds safe session boundary but still needs durable tracking.

### Remediation

Create or update a granular entry in `Final-Productization-Checklist.md` with:

- Scope
- Target Files
- Dependencies
- DONE WHEN
- Audit step

Then keep the checklist entry open and reference it in final summary/PR evidence.

## Quick verification checklist

1. Run path-scoped wrappers during remediation.
2. Run full wrappers before session close.
3. Copy summary blocks from `build/automation_contract/` rather than progress logs.
4. Keep local evidence under ignored paths; never commit binaries.
