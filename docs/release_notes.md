# Release Notes

## [Unreleased]

### Added
- Added a UTF-8 compliance hook (`scripts/check_unicode_escapes.py`) to the unified pre-commit suite so text assets are validated for UTF-8 decoding and symbolic Unicode escape literals.
- Added an `interrogate` hook to the unified pre-commit suite with `--fail-under=100` so docstring coverage enforcement is explicit and automated.

### Changed
- Converted repository documentation to generic scaffold language suitable for use as a pre-setup baseline for new repositories.
- Aligned `pyproject.toml` quality-tool settings with the standardized hook profile (line width 120, Python target 3.13, strict lint/type tooling defaults).
- Upgraded development dependency version floors and compatible caps in `pyproject.toml` and `requirements-dev.txt`.
- Added interrogate dependency/config parity across tooling docs and dependency assets.
- Added folder-level README coverage for `config/`, `docs/`, `scripts/`, `scripts/test_profiles/`, and `tests/` to improve template navigation for new users and stateless agents.
- Added coverage tests for `scripts/aggregate_project_docstrings.py` to verify missing-docstring accounting and excluded-directory behavior.
- Expanded root README orientation with wrapper-first execution policy, repository map, and docstring automation context.
