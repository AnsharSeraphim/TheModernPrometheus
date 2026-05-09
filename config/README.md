# config/

Repository configuration assets that support automation and contributor workflows.

## Contents

- `precommit_store/`: Hook-state ledgers and cached failure context consumed by `scripts/run_precommit_suite.py`.

Do not hand-edit skip-ledger JSON files; refresh them through the unified pre-commit runner.
See `docs/generated_artifact_contracts.md` for producer/consumer and commit-policy details, and `docs/source_boundary_manifest.md` for source boundary classification.
