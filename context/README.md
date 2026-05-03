# context/

Machine-readable context payloads generated from repository source data.

## Lifecycle policy

- Treat this folder as a generated-artifact staging area.
- JSON outputs from `scripts/aggregate_project_docstrings.py` are bootstrap inputs for agents and review tooling.
- Generated files are **not** committed unless a maintainer explicitly requests a checked-in snapshot for reproducibility.

## Bootstrap usage

Generate a full catalog:

```bash
python scripts/aggregate_project_docstrings.py --root . --output context/project_docstrings_catalog.json
```

Recommended follow-up checks:

```bash
python scripts/run_precommit_suite.py --scope paths --paths scripts/aggregate_project_docstrings.py context/README.md
python scripts/run_tests.py --scope paths --select tests/test_aggregate_project_docstrings.py
```

If you need a committed canonical sample for documentation examples, add a checklist entry first so artifact policy is explicitly reviewed.
