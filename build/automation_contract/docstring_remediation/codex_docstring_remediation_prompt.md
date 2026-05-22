# Codex Prompt: Apply TheModernPrometheus Docstring Remediation

You are working in the repository root for TheModernPrometheus. Use the uploaded remediation assets exactly as provided.

## Assets to upload/place

Place these files at:

- `build/automation_contract/docstring_remediation/docstring_remediation_manifest.json`
- `build/automation_contract/docstring_remediation/apply_docstring_remediation.py`
- `build/automation_contract/docstring_remediation/aggregated_docstrings_enriched.json`

## Task

Apply the generated docstring remediation manifest. It contains 42 replacement targets: 42 existing docstring quality upgrades and 0 missing insertions.

## Required execution

```bash
python build/automation_contract/docstring_remediation/apply_docstring_remediation.py \
  --repo-root . \
  --manifest build/automation_contract/docstring_remediation/docstring_remediation_manifest.json
python scripts/aggregate_project_docstrings.py
python scripts/audit_docstrings.py
python scripts/audit_docstrings.py --scan-root scripts --scan-root tests --output build/automation_contract/docstring_inventory_all_roots.md
python -m compileall -q scripts tests
```

## Acceptance criteria

- The applicator exits with status 0 and reports zero skipped targets.
- `context/project_docstrings_catalog.json` reports `flagged_docstrings: 0` and `missing_docstrings: 0`.
- Both audit inventories report 100% documented symbols.
- `python -m compileall -q scripts tests` passes.
- Do not hand-edit generated JSON ledgers unless rerunning the same scripts updates them.
