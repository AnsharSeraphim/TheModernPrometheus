# Documentation index

Use this index to find operational guidance by audience.

## Maintainers

- [`../AGENTS.md`](../AGENTS.md): authoritative execution policy, quality gates, and session-close workflow.
- [`../Final-Productization-Checklist.md`](../Final-Productization-Checklist.md): open work backlog for unresolved hardening tasks.
- [`../Final-Optimization-Checklist.md`](../Final-Optimization-Checklist.md): latency exceptions and optimization follow-up.
- [`../.github/workflows/quality-gates.yml`](../.github/workflows/quality-gates.yml): CI enforcement for wrapper-driven pre-commit and test suites.
- [`../.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md): PR evidence template requiring scoped commands and summary blocks.
- [`release_notes.md`](release_notes.md): user/tooling change history.
- [`troubleshooting.md`](troubleshooting.md): common wrapper/tooling failure signatures and remediation paths.

## Template consumers

- [`runtime_target_support_matrix.md`](runtime_target_support_matrix.md): runtime coverage, status, and instruction surfaces.
- [`context_trigger_matrix.md`](context_trigger_matrix.md): task-to-context load-order mapping for stateless workflows.
- [`task_recipe_schema.md`](task_recipe_schema.md): machine-readable task-recipe schema contract and starter asset guidance.
- [`template_customization_checklist.md`](template_customization_checklist.md): required post-clone checklist for replacing template defaults with project-specific decisions.
- [`../README.md`](../README.md): repository purpose and quickstart.
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md): onboarding workflow, wrappers, and remediation expectations.
- [`security_hygiene.md`](security_hygiene.md): security and data-boundary policy for secrets, local evidence, and deny-path commit rules.
- [`ownership_map.md`](ownership_map.md): role-based ownership map and CODEOWNERS alignment for operational assets.
- [`../config/README.md`](../config/README.md): precommit-store artifacts and governance.

## Agent operators

- [`agent_bootstrap/README.md`](agent_bootstrap/README.md): recipe for generating bootstrap JSON/markdown artifacts.
- [`../CLAUDE.md`](../CLAUDE.md): Claude Code-specific execution guidance aligned to repository policy.
- [`../COPILOT.md`](../COPILOT.md): GitHub Copilot-specific execution guidance aligned to repository policy.
- [`../scripts/README.md`](../scripts/README.md): wrapper command surfaces and utility behavior.
- [`../tests/README.md`](../tests/README.md): test suite coverage map.
- [`../context/recipes/documentation_parity_audit_session.md`](../context/recipes/documentation_parity_audit_session.md): repeatable rubric for documentation parity audits.
- [`../context/recipes/release_prep_session.md`](../context/recipes/release_prep_session.md): release-prep workflow with release-note and closure checks.
- [`../context/recipes/pr_evidence_packaging_session.md`](../context/recipes/pr_evidence_packaging_session.md): PR evidence packaging workflow for wrapper summary blocks.

## Notes

This index intentionally links to canonical sources instead of duplicating command narratives that already live in root and scripts documentation.
