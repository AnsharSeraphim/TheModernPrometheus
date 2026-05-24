# GitHub Copilot Agent Instructions

This file provides repository-local execution guidance for GitHub Copilot (Chat/Agent) sessions.

## Required context load order

1. `AGENTS.md`
2. `scripts/README.md`
3. `Final-Productization-Checklist.md`
4. `Final-Optimization-Checklist.md`
5. `docs/agent_bootstrap/operator_context_injection.md`

## Wrapper-first contract

Use only repository wrappers for validation and remediation:

- `python scripts/run_precommit_suite.py`
- `python scripts/run_tests.py`

Do not replace wrapper execution with direct hook aliases or bare `pytest`.

## Checklist governance contract

- `Final-Productization-Checklist.md` is the canonical open-work backlog for unresolved implementation, documentation, and tooling items.
- `Final-Optimization-Checklist.md` is the canonical ledger for over-budget tests under the 0.20s per-test policy.
- In `Final-Optimization-Checklist.md`, `✅` is reserved only for tests with a completed code audit confirming further optimization would compromise fidelity/purpose.
- Keep pending optimization audits and confirmed justified exceptions in separate sections.
- Remove completed checklist entries; rewrite partially completed entries as explicit remaining work.

## Evidence and handoff

- Capture final suite summary blocks from `build/automation_contract/` for handoff notes.
- Keep local evidence caches untracked.
- Never commit binary evidence assets.
- If wrapper/test failures remain unresolved, create granular checklist follow-ups with `Scope`, `Target Files`, `Dependencies`, `DONE WHEN`, and `Audit step`.
