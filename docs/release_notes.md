# Release Notes

## [Unreleased]

### Added
- Added a UTF-8 compliance hook (`scripts/check_unicode_escapes.py`) to the unified pre-commit suite so text assets are validated for UTF-8 decoding and symbolic Unicode escape literals.
- Added an `interrogate` hook to the unified pre-commit suite with `--fail-under=100` so docstring coverage enforcement is explicit and automated.
- Added `.github/dependabot.yml` with grouped weekly update strategies for pip and GitHub Actions dependencies, explicit labels, reviewer defaults, and bounded open-PR limits.

### Changed
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
