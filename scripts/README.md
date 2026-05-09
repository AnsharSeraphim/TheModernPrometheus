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
- `audit_docstrings.py`: Produces a Markdown inventory report with documented symbols, missing-docstrings table, and scan-failure table for implementation-vs-documentation parity audits.

## Test profile assets

- `test_profiles/baseline.txt`: Curated baseline test target set for wrapper-driven test runs.

## Wrapper-first policy

- Naked `pytest` execution is blocked by `tests/conftest.py` unless `scripts/run_tests.py` sets the wrapper gate environment variable.

- Use `python scripts/run_precommit_suite.py` instead of naked `pre-commit run` hook aliases.
- Use `python scripts/run_tests.py` instead of naked `pytest` so summary artifacts and scope logic stay consistent.

## Docstring workflow quickstart

- JSON bootstrap payload for automated context ingestion:
  - `python scripts/aggregate_project_docstrings.py --root . --output context/project_docstrings_catalog.json`
- Markdown parity audit for live script behavior checks and narrative alignment:
  - `python scripts/audit_docstrings.py --scan-root scripts --scan-root tests --output build/automation_contract/docstring_inventory.md`

Use the JSON catalog when downstream tooling expects structured machine-readable metadata, and use the Markdown inventory when reviewers need a line-by-line audit table they can quickly compare against implementation notes.

When `interrogate` fails in `run_precommit_suite.py`, the wrapper now auto-runs `audit_docstrings.py` against the same script target set and writes `build/automation_contract/docstring_inventory.md` as follow-up evidence.

## Generated artifact boundaries

- Artifact contracts and commit policies are documented in `docs/generated_artifact_contracts.md`.
- Source-vs-generated boundaries are documented in `docs/source_boundary_manifest.md`.
- Troubleshooting reference: `docs/troubleshooting.md` centralizes failure signatures and wrapper-compliant recovery paths.
- Treat `config/precommit_store/*.json` as generated committed ledgers and `build/automation_contract/*` as local evidence caches.


## Docstring aggregation operational modes

- Full scan: `python scripts/aggregate_project_docstrings.py --root . --output context/project_docstrings_catalog.json`
- Scoped exclusions: add one or more `--exclude <glob>` entries to omit generated/vendor paths during export.
- Output conventions: prefer writing JSON under `context/` for bootstrap payloads and keep review markdown under `build/automation_contract/` for local evidence.
- Downstream consumers: agent bootstrap docs (`docs/agent_bootstrap/README.md`), prompt recipes, and audit workflows should reference the generated JSON schema/keys instead of parsing source files ad hoc.
