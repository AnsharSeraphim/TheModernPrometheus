# Claude Code Instructions

This repository supports Claude Code sessions with the same governance as other agent runtimes.

## Non-negotiable execution rules

- Read `AGENTS.md` before changes.
- Process `Final-Productization-Checklist.md` in dependency order (prerequisites first).
- Use only wrapper commands for quality/testing:
  - `python scripts/run_precommit_suite.py`
  - `python scripts/run_tests.py`
- Remediate surfaced failures; do not silence or bypass checks.

## Evidence and artifact boundaries

- Capture final summary blocks from `build/automation_contract/` for session handoff/PR notes.
- Keep local evidence caches untracked.
- Never commit screenshots, videos, archives, or other binary evidence assets.
- Do not hand-edit `config/precommit_store/*.json`; wrappers own skip-ledger and pylint-cache state.

## Checklist discipline

- Keep checklist entries actionable and closeable.
- Remove completed entries; rewrite partial work as explicit remaining tasks.
- If you cannot close an issue in-session, add granular follow-up entries with:
  - Scope
  - Target Files
  - Dependencies
  - DONE WHEN
  - Audit step
