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
- Treat `Final-Productization-Checklist.md` as the unresolved implementation/documentation/tooling backlog and `Final-Optimization-Checklist.md` as the over-budget test ledger.
- In `Final-Optimization-Checklist.md`, use `✅` only for exceptions backed by a completed test-level code audit showing further optimization would harm fidelity/purpose.
- Keep checklist policy parity with `AGENTS.md`, `README.md`, and onboarding docs; if one source changes, update the others in the same session.
