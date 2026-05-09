# Ownership Map

This document defines default maintainer roles for operational assets in this template repository.

The map is intentionally role-based so template consumers can adopt it immediately and then replace role labels with team-specific identities.

## Role definitions

- **Template Maintainer**: Maintains reusable template behavior and governance defaults.
- **Quality Maintainer**: Maintains quality wrappers, linters, type checks, security checks, and skip-ledger behavior.
- **Documentation Maintainer**: Maintains onboarding, operational docs, and release-note accuracy.
- **CI Maintainer**: Maintains GitHub automation and review-routing policy.

## Ownership matrix

| Asset category | Paths | Owner role |
| --- | --- | --- |
| Core agent and contributor policy | `AGENTS.md`, `CONTRIBUTING.md`, `README.md` | Template Maintainer |
| Productization and optimization backlogs | `Final-Productization-Checklist.md`, `Final-Optimization-Checklist.md` | Template Maintainer |
| Automation wrappers and utilities | `scripts/` | Quality Maintainer |
| Test harness and wrapper contract tests | `tests/` | Quality Maintainer |
| Pre-commit skip ledgers and cached diagnostics | `config/precommit_store/` | Quality Maintainer |
| Operational and onboarding documentation | `docs/` | Documentation Maintainer |
| Context recipes and prompt library | `context/` | Documentation Maintainer |
| GitHub workflow and review templates | `.github/workflows/`, `.github/PULL_REQUEST_TEMPLATE.md` | CI Maintainer |
| CODEOWNERS policy | `.github/CODEOWNERS` | CI Maintainer |

## Review-routing expectation

- Pull requests that change the paths above should request review from the corresponding owner role.
- Template consumers should replace role labels with concrete team slugs or usernames after cloning.
