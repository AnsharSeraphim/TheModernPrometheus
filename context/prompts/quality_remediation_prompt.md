# Quality Remediation Prompt

## Purpose

Resolve surfaced quality-gate failures using the repository wrappers without bypassing ledger behavior.

## Ingestion order

1. `AGENTS.md`
2. `scripts/README.md`
3. `docs/agent_bootstrap/operator_context_injection.md`
4. `Final-Productization-Checklist.md`

## Canonical commands

```bash
python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
python scripts/run_precommit_suite.py --only <hook> --scope paths --paths <file1> <file2>
python scripts/run_precommit_suite.py
python scripts/run_tests.py --scope paths --select <selector>
python scripts/run_tests.py
```

## Evidence requirements

- Use wrapper output to identify failing files.
- Apply implementation fixes (no suppression/config weakening).
- Keep updated `config/precommit_store/*.json` files produced by wrapper runs.

## Closure criteria

- Full pre-commit and test wrappers pass, or residual blockers are captured as granular checklist tasks.
