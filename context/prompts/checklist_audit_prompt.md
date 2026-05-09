# Checklist Audit Prompt

## Purpose

Audit `Final-Productization-Checklist.md` for dependency order, stale items, and non-actionable wording.

## Ingestion order

1. `AGENTS.md`
2. `Final-Productization-Checklist.md`
3. `docs/agent_bootstrap/operator_context_injection.md`
4. `context/recipes/checklist_audit_session.md`

## Canonical commands

```bash
python scripts/run_precommit_suite.py --scope paths --paths Final-Productization-Checklist.md
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

## Evidence requirements

- Remove completed entries.
- Rewrite partial entries as precise remaining work.
- Ensure every new item uses Scope, Target Files, Dependencies, DONE WHEN, and Audit step.

## Closure criteria

- Only open actionable tasks remain.
- Checklist structure validation passes through wrapper output.
