# Release Notes

## [Unreleased]

### Added
- Added `docs/template_customization_checklist.md` with a concrete post-clone hardening checklist covering metadata replacement, runtime/dependency decisions, ignore-policy verification, checklist seeding, docs parity, and initial wrapper validation.

### Changed
- Raised the Pylint `max-module-lines` threshold from 3400 to 4500 in `pyproject.toml` and aligned Dependabot update grouping so each ecosystem is consolidated into a single weekly PR stream.
- Added missing module/test docstrings in targeted test modules to improve out-of-the-box interrogate quality coverage for template consumers.
- Updated `scripts/run_precommit_suite.py` so interrogate failures now auto-trigger `scripts/audit_docstrings.py` for the same script scope and log the follow-up inventory guidance directly in pre-commit output.
- Hardened `scripts/audit_docstrings.py` with scan-failure reporting (read/syntax errors) so coverage remediation does not silently skip unparseable files.
- Updated docstring-remediation guidance in `scripts/README.md`, `docs/troubleshooting.md`, and `docs/agent_bootstrap/operator_context_injection.md` to reflect wrapper-integrated audit follow-up and scan-failure triage order.
- Updated `.github/workflows/quality-gates.yml` to run pre-commit in explicit repository-wide full-check mode (`--scope all --reset-baseline --filter-mode full`) so CI cannot pass by reusing committed skip-ledger state.
- Aligned remote-validation documentation in `README.md`, `CONTRIBUTING.md`, `docs/runtime_target_support_matrix.md`, and `docs/troubleshooting.md` with the new CI full-check contract.
- Removed the completed `Make CI wrapper validation run in full-check mode instead of skip-ledger no-op mode` entry from `Final-Productization-Checklist.md`.
- Linked the template-customization checklist from `README.md`, `docs/new_user_onboarding.md`, and `docs/README.md` so new template consumers discover it in all primary onboarding paths.
- Added generated-artifact governance documentation via `docs/generated_artifact_contracts.md` and `docs/source_boundary_manifest.md`, then linked those assets from root/bootstrap/scripts/config READMEs so commit boundaries are explicit.
- Removed the completed `Document generated-artifact contracts and source boundaries` entry from `Final-Productization-Checklist.md` so open-work tracking only contains unresolved tasks.
- Added a machine-readable task-recipe system under `context/task_recipes/` with a JSON Schema contract and starter quality-remediation/checklist-audit assets, then documented and indexed it in bootstrap/docs references.
- Removed the completed `Add machine-readable task-recipe schema with starter assets` entry from `Final-Productization-Checklist.md`.

### Added
- Added a UTF-8 compliance hook (`scripts/check_unicode_escapes.py`) to the unified pre-commit suite so text assets are validated for UTF-8 decoding and symbolic Unicode escape literals.
- Added an `interrogate` hook to the unified pre-commit suite with `--fail-under=100` so docstring coverage enforcement is explicit and automated.
- Added `.github/dependabot.yml` with grouped weekly update strategies for pip and GitHub Actions dependencies, explicit labels, reviewer defaults, and bounded open-PR limits.

### Changed
- Added explicit commit/PR phase-splitting thresholds and per-phase validation evidence requirements to `CONTRIBUTING.md`, `docs/new_user_onboarding.md`, and `docs/agent_bootstrap/operator_context_injection.md` to prevent oversized single-diff workflows.
- Completed timestamp/UTF-8 policy parity updates across onboarding/context docs by adding missing guidance in `README.md` and harmonizing friction-entry instructions in `Final-Productization-Checklist.md`.
- Added `context/recipes/quality_remediation_session.md` and `context/recipes/checklist_audit_session.md`, linked from bootstrap docs, and recorded a wrapper-help parity audit in `docs/agent_bootstrap/operator_context_injection.md`.
- Completed a first-pass documentation parity audit across root, scripts, tests, and config READMEs; removed the corresponding completed audit tasks from `Final-Productization-Checklist.md` so only unresolved documentation entries remain.
- Clarified `CONTRIBUTING.md` local setup guidance to match the repository runtime pin (`>=3.13,<3.14`) by explicitly instructing contributors to use Python 3.13 virtual environments.
- Documented the pyproject reproducibility rationale in `README.md`, including Python pinning (`>=3.13,<3.14`), bounded dependency caps, and strict checker posture expectations.
- Enforced wrapper-first pytest execution via a repository-level pytest session guard and wrapper-managed environment variable handshake, with tests covering the warning contract.
- Added `context/README.md` and `docs/agent_bootstrap/README.md` to document docstring-catalog artifact lifecycle, bootstrap outputs, and acceptance checks.
- Reworked `docs/README.md` into an audience-based documentation index and expanded `CONTRIBUTING.md` onboarding/remediation flow for template consumers.
- Expanded `scripts/README.md` with `aggregate_project_docstrings.py` operational modes (full scan, exclusions, output conventions, downstream consumers).
- Added a checklist structure guard script (`scripts/check_checklist_structure.py`) and integrated it into the pre-commit wrapper to prevent accidental removal of mandatory checklist policy/audit sections.
- Converted repository documentation to generic scaffold language suitable for use as a pre-setup baseline for new repositories.
- Aligned `pyproject.toml` quality-tool settings with the standardized hook profile (line width 120, Python target 3.13, strict lint/type tooling defaults).
- Upgraded development dependency version floors and compatible caps in `pyproject.toml` and `requirements-dev.txt`.
- Added interrogate dependency/config parity across tooling docs and dependency assets.
- Added folder-level README coverage for `config/`, `docs/`, `scripts/`, `scripts/test_profiles/`, and `tests/` to improve template navigation for new users and stateless agents.
- Added coverage tests for `scripts/aggregate_project_docstrings.py` to verify missing-docstring accounting and excluded-directory behavior.
- Expanded root README orientation with wrapper-first execution policy, repository map, and docstring automation context.
- Repurposed `scripts/audit_docstrings.py` for this repository with default scan roots (`scripts/`, `tests/`), excluded-directory handling, and Markdown inventory documentation in `scripts/README.md`.

## 2026-05-07

- Added `docs/agent_bootstrap/operator_context_injection.md` to centralize stateless-agent bootstrap context for wrapper syntax, commit/PR discipline, timestamp hygiene, and checklist escalation paths.
- Updated `AGENTS.md` with a quickstart context-pack requirement so agents load operational constraints before editing.

- Enhanced `scripts/audit_docstrings.py` to include documented/missing coverage summaries so interrogate wrapper failures can be converted into scoped remediation checklists without ad-hoc investigation.
- Expanded `docs/agent_bootstrap/operator_context_injection.md` with an explicit interrogate-failure response workflow that prioritizes in-session docstring remediation and defines checklist fallback requirements.

- Aligned interrogate remediation guidance so `operator_context_injection.md` invokes `audit_docstrings.py` with `--scan-root scripts`, matching the wrapper interrogate target scope and avoiding non-actionable `tests/` findings during interrogate triage.
## 2026-05-09
- Added a root `.gitignore` to enforce local evidence and Python artifact ignore boundaries, including wrapper evidence directories and virtualenv/cache paths.
- Updated contributor/bootstrap guidance to reference the root ignore policy and `git check-ignore -v` verification workflow.



## 2026-05-09

- Added a reusable prompt-library under `context/prompts/` with five workflow-specific prompt assets and a dedicated index.
- Updated `README.md` and `context/README.md` to route operators to prompt assets instead of a single embedded metaprompt.
- Removed the now-completed prompt-library backlog entry from `Final-Productization-Checklist.md`.

## 2026-05-09

- Added `context/recipes/release_prep_session.md` and `context/recipes/pr_evidence_packaging_session.md` to make release-prep and PR evidence policy executable via copy-ready workflow steps.
- Added `context/recipes/documentation_parity_audit_session.md` and linked it from docs indexes so documentation parity audits follow a reusable implementation-check workflow.
- Updated `context/README.md`, `docs/README.md`, and `CONTRIBUTING.md` with links to the new recipe assets.
- Added calibration examples under `docs/examples/` covering good/bad checklist entries, evidence packaging, and friction entries for stateless-agent output quality baselining.
- Linked `docs/generated_artifact_contracts.md` to the new examples so evidence-contract guidance points to concrete exemplar/anti-exemplar patterns.
- Removed the completed `Create exemplar and anti-exemplar package for agent calibration` entry from `Final-Productization-Checklist.md`.

## 2026-05-09

- Added `.github/CODEOWNERS` and `docs/ownership_map.md` to define role-based ownership coverage for governance docs, automation scripts, tests, context assets, and CI workflow files.
- Added `docs/security_hygiene.md` with explicit secret-handling, deny-path, local-evidence, and source-boundary guidance for template consumers.
- Linked ownership and security hygiene docs from `README.md`, `CONTRIBUTING.md`, `docs/new_user_onboarding.md`, and `docs/README.md` so policy surfaces appear in first-read onboarding paths.
- Removed the completed ownership/security entries from `Final-Productization-Checklist.md` so only unresolved backlog items remain.
