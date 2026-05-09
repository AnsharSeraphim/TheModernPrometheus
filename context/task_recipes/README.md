# Task Recipes

This directory stores machine-readable task recipes for high-frequency stateless workflows.

## Files

- `schema.json`: JSON Schema for recipe contracts.
- `quality_remediation.json`: starter recipe for wrapper-first quality remediation loops.
- `checklist_audit.json`: starter recipe for checklist dependency and actionability audits.

## Validation

Use this command to validate each recipe against the schema:

```bash
python - <<'PY'
import json
from jsonschema import Draft202012Validator

with open('context/task_recipes/schema.json', encoding='utf-8') as f:
    schema = json.load(f)

validator = Draft202012Validator(schema)
for path in [
    'context/task_recipes/quality_remediation.json',
    'context/task_recipes/checklist_audit.json',
]:
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    if errors:
        raise SystemExit(f'{path} failed validation: {errors[0].message}')
    print(f'{path}: OK')
PY
```

Dependency note: this validation requires `jsonschema`, which is included in the repository development dependency set (`requirements-dev.txt` and `project.optional-dependencies.dev`).

Each recipe must define `task_id`, `scope`, `target_files`, `dependencies`, wrapper `commands`, explicit `validations`, and `done_when` closure criteria.
