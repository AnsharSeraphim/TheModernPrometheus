# Repository Audit Prompt

## Purpose

Run a full implementation-plus-documentation audit that validates wrapper syntax, checklist hygiene, and documentation parity.

## Ingestion order

1. `AGENTS.md`
2. `docs/agent_bootstrap/operator_context_injection.md`
3. `scripts/README.md`
4. `Final-Productization-Checklist.md`
5. `docs/README.md`

## Canonical commands

```bash
python scripts/run_precommit_suite.py --scope paths --paths <touched-file1> <touched-file2>
python scripts/run_tests.py --scope paths --select <relevant-selector>
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

## Evidence requirements

- Validate command/path claims against implementation.
- Capture final summary blocks from `build/automation_contract/precommit_summary_block.txt` and `build/automation_contract/test_summary_block.txt`.
- Record unresolved gaps as checklist entries with Scope, Target Files, Dependencies, DONE WHEN, and Audit step.

## Closure criteria

- Audit claims are either remediated or represented as granular checklist entries.
- Wrapper/test summaries are available for handoff.
