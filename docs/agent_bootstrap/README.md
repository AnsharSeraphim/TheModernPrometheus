# Agent bootstrap build plan

This folder documents how to create agent-bootstrap artifacts from existing repository automation.

## Scope and ownership

- Audience: maintainers extending this template for new repositories.
- Owners: contributors who modify wrapper scripts or documentation-generation utilities.
- Source-of-truth scripts: `scripts/aggregate_project_docstrings.py`, `scripts/audit_docstrings.py`, `scripts/run_precommit_suite.py`, and `scripts/run_tests.py`.

## Task list

1. Generate docstring catalog JSON for machine-readable context:
   - Command: `python scripts/aggregate_project_docstrings.py --root . --output context/project_docstrings_catalog.json`
   - Output: `context/project_docstrings_catalog.json`
   - Acceptance check: JSON exists, parses, and includes module/function/class entries.
2. Generate parity-focused Markdown inventory for reviewers:
   - Command: `python scripts/audit_docstrings.py --scan-root scripts --scan-root tests --output build/automation_contract/docstring_inventory.md`
   - Output: `build/automation_contract/docstring_inventory.md` (local evidence artifact; do not commit).
   - Acceptance check: table rows enumerate script/test symbols and docstrings.
3. Validate wrapper policy and tests:
   - Commands:
     - `python scripts/run_precommit_suite.py`
     - `python scripts/run_tests.py`
   - Acceptance check: both summary blocks report success.

## Prompt/recipe artifacts

- Skills markdown should reference wrapper-first commands and checklist governance from `AGENTS.md`.
- Prompt recipes should include required quality gates and instructions to attach summary blocks from `build/automation_contract/`.
- Task-recipe JSON should include explicit `scope`, `target_files`, and `done_when` fields mirroring checklist policy.
