# PR Evidence Packaging Prompt

## Purpose

Package high-signal evidence for a review-ready pull request summary.

## Ingestion order

1. `AGENTS.md`
2. `docs/agent_bootstrap/operator_context_injection.md`
3. `CONTRIBUTING.md`
4. `docs/release_notes.md`

## Canonical commands

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

## Evidence requirements

- Copy final summary blocks from `build/automation_contract/`.
- List scoped commands executed during remediation.
- Include unresolved risks with linked checklist entries.
- Confirm release notes were updated for tooling/workflow behavior changes.

## Closure criteria

- PR notes include wrappers run, summary blocks, unresolved work links, and release-note confirmation.
