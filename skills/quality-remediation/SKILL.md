# Skill: Quality Remediation

## Description
Run implementation changes and quality remediation loops while preserving repository pre-commit ledger semantics.

## When to use
- You are changing Python code/docs and need wrapper-enforced lint/type/security/docstring/test validation.
- You need scoped reruns for touched files before a full closeout sweep.

## When not to use
- You are only auditing checklist wording without changing code or docs.
- You need a documentation parity audit flow (use `documentation-parity-audit`).

## Environment prerequisites
- POSIX-compatible shell.
- `rg` (`ripgrep`) available on `PATH`.

## Required inputs
- Target files being edited.
- Relevant pytest selectors for changed behavior.

## Canonical commands
- Scoped remediation while iterating:
  - `python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>`
- Single-hook focused remediation:
  - `python scripts/run_precommit_suite.py --only <hook> --scope paths --paths <file1> <file2>`
- Scoped tests:
  - `python scripts/run_tests.py --scope paths --select <pytest-selector>`
- Session close:
  - `python scripts/run_precommit_suite.py`
  - `python scripts/run_tests.py`

## Closure criteria
- Touched files pass scoped wrapper checks.
- Full pre-commit and test suites complete successfully or unresolved work is captured in `Final-Productization-Checklist.md` with explicit scope/dependencies/audit step.
