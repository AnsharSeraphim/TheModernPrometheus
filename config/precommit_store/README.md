This directory stores the unified pre-commit suite's JSON skip ledgers.

Each required hook writes `config/precommit_store/<hook>.json`. Most hooks track Python files (including the interrogate docstring-coverage hook); the UTF-8 compliance hook tracks supported text assets (`.py`, `.pyi`, `.md`, `.txt`, `.json`, `.toml`, `.yaml`, `.yml`, `.ini`, `.cfg`). New files enter manifests with `"skip": "N"` and flip to `"skip": "Y"` after a passing run. Use `python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>` while iterating so the ledgers reflect the latest diagnostics.

Do not hand-edit the JSON files. Rebuild or refresh them through `scripts/run_precommit_suite.py`, including `--reset-baseline` when you need to invalidate every cached pass.
