# GitHub Copilot Repository Instructions

Follow these rules when generating or editing code/docs in this repository:

1. Use wrapper-first commands:
   - `python scripts/run_precommit_suite.py`
   - `python scripts/run_tests.py`
2. Do not bypass wrappers with direct `pytest` or ad hoc pre-commit hook runs.
3. Treat `Final-Productization-Checklist.md` as ordered, dependency-aware open work; complete prerequisite items first.
4. Keep evidence packaging intact: preserve and report final summary blocks from `build/automation_contract/`.
5. Never commit binary evidence artifacts.
6. Do not hand-edit `config/precommit_store/*.json`; let wrapper scripts manage these files.
7. If a failure cannot be remediated in-session, add a granular checklist entry with Scope, Target Files, Dependencies, DONE WHEN, and Audit step.
