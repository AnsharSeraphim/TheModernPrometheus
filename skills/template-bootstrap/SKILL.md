# Skill: Template Bootstrap

## Description
Initialize a new session for template consumers with the minimum context pack and wrapper discipline.

## When to use
- Starting first meaningful work in a freshly cloned template-derived repository.
- Aligning contributors/agents on required ingestion order and evidence packaging policy.

## When not to use
- Mid-session remediation where context is already loaded.
- Narrow checklist-only edits that do not require full onboarding.

## Environment prerequisites
- POSIX-compatible shell.
- `rg` (`ripgrep`) available on `PATH`.

## Required inputs
- Repository root with `AGENTS.md`, docs, scripts, and checklists present.

## Canonical commands
- Required ingestion order:
  - `sed -n '1,220p' AGENTS.md`
  - `sed -n '1,220p' scripts/README.md`
  - `sed -n '1,260p' Final-Productization-Checklist.md`
  - `sed -n '1,220p' docs/new_user_onboarding.md`
- Quality and test closeout:
  - `python scripts/run_precommit_suite.py`
  - `python scripts/run_tests.py`

## Closure criteria
- Session summary cites ingestion order completion.
- Work executes wrapper-first and includes automation summary evidence.
- Deferred work is captured in checklist entries with explicit dependencies.
