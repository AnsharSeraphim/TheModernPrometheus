# Task Recipe Schema

This document defines the machine-readable schema for stateless workflow recipes in `context/task_recipes/`.

## Purpose

Task recipes let routers and advanced stateless agents consume workflow guidance without parsing long prose files. Recipes capture the same closure semantics enforced by checklist policy and wrapper-first execution rules.

## Canonical files

- Schema: `context/task_recipes/schema.json`
- Starter assets:
  - `context/task_recipes/quality_remediation.json`
  - `context/task_recipes/checklist_audit.json`

## Required fields

Each recipe must include these top-level keys:

- `task_id`: stable lowercase identifier (`[a-z0-9_-]+`).
- `title`: short human-readable name.
- `scope`: bounded execution objective.
- `target_files`: explicit files and/or globs the workflow acts on.
- `dependencies`: prerequisite task IDs (empty array if none).
- `commands`: ordered command steps with `name`, `command`, and `purpose`.
- `validations`: verification checks with `name`, `method`, and `pass_condition`.
- `done_when`: objective closure criteria as a checklist-style list.

Optional keys:

- `context_sources`: paths to documents an agent should ingest before executing the task.

## Command guidance

Recipe command entries should use canonical wrappers:

- `python scripts/run_precommit_suite.py ...`
- `python scripts/run_tests.py ...`

Do not encode direct hook aliases or bare `pytest` calls unless a repository policy explicitly permits them.

## Validation workflow

1. Load `context/task_recipes/schema.json`.
2. Validate each recipe JSON under `context/task_recipes/`.
3. Reject assets with unknown keys (schema sets `additionalProperties: false`).
4. Keep recipe `done_when` semantics aligned with checklist `DONE WHEN` expectations.

The reference validation snippet imports `jsonschema.Draft202012Validator`; install repository development dependencies before running it.

## Maintenance notes

- Update this document when schema keys, constraints, or workflow expectations change.
- When adding recipes, include the new file in `context/task_recipes/README.md` and reference it from bootstrap docs if it is part of the default operator context.
