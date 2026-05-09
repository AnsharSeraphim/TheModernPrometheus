# Task-to-Context Trigger Matrix

This matrix tells stateless contributors exactly which context assets to load for common workflows.

## Minimum context packs by workflow

| Workflow | Required load order (minimum) | Optional context assets | Core commands | Evidence/closure expectation |
| --- | --- | --- | --- | --- |
| First-time orientation | `README.md` -> `AGENTS.md` -> `docs/new_user_onboarding.md` -> `Final-Productization-Checklist.md` | `docs/README.md`, `CONTRIBUTING.md` | None required before planning | Contributor can explain wrapper-first policy, checklist ordinality, and session-close gates. |
| Quality remediation loop | `AGENTS.md` -> `scripts/README.md` -> `docs/agent_bootstrap/operator_context_injection.md` -> relevant checklist entries | `context/recipes/quality_remediation_session.md`, `config/README.md` | `python scripts/run_precommit_suite.py --scope paths --paths <files>` | Hook failures remediated or converted into granular checklist entries. |
| Checklist audit / dependency hygiene | `Final-Productization-Checklist.md` -> `AGENTS.md` -> `context/recipes/checklist_audit_session.md` | `docs/new_user_onboarding.md` | `python scripts/run_precommit_suite.py --scope paths --paths Final-Productization-Checklist.md` | Checklist contains only open actionable work with clear dependencies and DONE WHEN criteria. |
| Documentation parity audit | `AGENTS.md` -> `docs/README.md` -> target docs -> referenced implementation files | `context/recipes/documentation_parity_audit_session.md`, `scripts/README.md` | wrapper commands for impacted files + relevant tests | Claims in docs match implementation, links/commands validated, unresolved gaps tracked in checklist. |
| Template bootstrap artifact generation | `docs/agent_bootstrap/README.md` -> `scripts/README.md` -> `AGENTS.md` | `context/README.md` | `python scripts/aggregate_project_docstrings.py ...`; `python scripts/audit_docstrings.py ...` | Artifact contract respected (commit JSON catalog, keep local evidence untracked). |
| Release prep | `docs/release_notes.md` -> `AGENTS.md` -> `CONTRIBUTING.md` | `context/recipes/release_prep_session.md` | `python scripts/run_precommit_suite.py`; `python scripts/run_tests.py` | Release notes + validation evidence updated with unresolved work captured in checklist. |
| PR evidence packaging | `docs/agent_bootstrap/operator_context_injection.md` -> `AGENTS.md` -> `CONTRIBUTING.md` | `context/recipes/pr_evidence_packaging_session.md` | Gather summary blocks from `build/automation_contract/` | PR/session summary includes exact wrapper commands + summary blocks + deferred work links. |
