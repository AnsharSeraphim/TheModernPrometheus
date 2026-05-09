# Operator Context Injection Playbook

This playbook defines the minimum context pack that stateless coding agents should ingest before making workflow or code changes in this repository template.

## Why this exists

Recent execution friction showed agents were making syntax mistakes for wrapper scripts, skipping required run order, and mishandling commit/PR workflow boundaries. This document centralizes operational guardrails and concrete command recipes so context injection is explicit instead of inferred.

## Bootstrap ingestion order (required)

1. Read `AGENTS.md` for session-wide policy and mandatory quality gates.
2. Read `scripts/README.md` for canonical wrapper entry points and supporting utilities.
3. Read `Final-Productization-Checklist.md` and process entries in order, respecting dependencies.
4. Read `docs/new_user_onboarding.md` for project navigation and role expectations.

If any source appears inconsistent with implementation, treat implementation and wrapper output as source of truth, then create checklist follow-up entries.

## Canonical wrapper syntax (copy-ready)

### Pre-commit suite

- Full suite (session close):

```bash
python scripts/run_precommit_suite.py
```

- Scoped remediations while editing files:

```bash
python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
```

- Single-hook remediation while preserving ledger semantics:

```bash
python scripts/run_precommit_suite.py --only <hook> --scope paths --paths <file1> <file2>
```


### Interrogate violation response (required for stateless quality control)

Interrogate is intentionally surfaced as a concise violation in pre-commit output so wrapper logs stay digestible.

When `python scripts/run_precommit_suite.py` reports an interrogate violation, the wrapper auto-runs:

```bash
python scripts/audit_docstrings.py --scan-root scripts --output build/automation_contract/docstring_inventory.md
```

If the follow-up block indicates that audit generation failed, rerun the same command manually before proceeding.

Use the `## Missing docstrings` table in that report to drive remediation scope for the same interrogate target set (`scripts/`). Resolve any `## Scan failures` rows first:

1. If missing docstrings are in files touched during the current session, remediate in-session and rerun the wrapper in scoped mode.
2. If remediation is genuinely out-of-scope for one session (for example required refactors across multiple modules), add granular checklist entries in `Final-Productization-Checklist.md` that include `Scope`, `Target Files`, `Dependencies`, `DONE WHEN`, and an explicit audit step.
3. Never treat interrogate failures as informational-only; they always require either remediation or checklist action before session close.

### Test suite

- Full suite (session close):

```bash
python scripts/run_tests.py
```

- Scoped test execution for changed behavior:

```bash
python scripts/run_tests.py --scope paths --select <pytest-selector>
```

## Commit/PR discipline contract

- Never commit binary artifacts (images, video, archives).
- Keep local evidence/cache outputs untracked through the root `.gitignore`; validate new local-only paths with `git check-ignore -v <path>`.
- If changed quality-ledger JSON files under `config/precommit_store/` are produced by wrapper runs, include them in the commit.
- Do not hand-edit skip manifests or pylint cache files.
- Phase large changes proactively using repository thresholds:
  - split when a work unit exceeds 25 changed files, or
  - split when net line churn exceeds 1,200 changed lines.
- For hosting/platform hard limits (for example around 100k changed lines), split further into smaller, independently validated phases.
- A session that commits must also produce a PR message with test evidence summaries.

### Per-phase validation and PR evidence

- Before each phase commit:
  - `python scripts/run_precommit_suite.py --scope paths --paths <touched-file1> <touched-file2>`
  - `python scripts/run_tests.py --scope paths --select <relevant-selector>`
- Before PR publication/final phase handoff:
  - `python scripts/run_precommit_suite.py`
  - `python scripts/run_tests.py`
- PR notes must include:
  - the final summary blocks from `build/automation_contract/`,
  - scoped remediation commands executed,
  - explicit references to unresolved checklist entries if any work is deferred.

## Data and timestamp hygiene

- Save text files as UTF-8.
- Never trust model-internal clocks for datestamps; use Git metadata or trusted system sources.
- Use explicit absolute dates in user-facing notes when there is ambiguity.

## Required behavior when friction appears mid-session

1. Attempt direct remediation in-session with wrapper-driven loops.
2. If unresolved, create granular checklist entries with:
   - Scope
   - Target Files
   - Dependencies
   - DONE WHEN
   - An explicit audit step so later agents can expand based on evidence.
3. Keep unresolved entries in `Final-Productization-Checklist.md`; do not leave narrative-only notes.

## Evidence packaging expectations

- Capture final result blocks emitted under `build/automation_contract/`.
- Avoid copying progress percentages or partial logs.
- Report exact commands used and outcomes in final session summary.

## Context-injection parity audit (2026-05-07)

Canonical audit scope: `docs/new_user_onboarding.md`, `docs/README.md`, `scripts/README.md`, `docs/agent_bootstrap/README.md`, and this playbook.

- Wrapper syntax parity: confirmed command parity against `python scripts/run_precommit_suite.py --help` and `python scripts/run_tests.py --help`; no syntax drift detected.
- Wrapper-first policy parity: each scoped document now points contributors to wrapper surfaces instead of direct hook/test calls.
- Recipe coverage remediation: added repository-local recipes for quality remediation and checklist audits under `context/recipes/` and linked them from bootstrap docs.
- Remaining follow-up: none from this parity sweep; create a new checklist entry if future wrapper help output changes.
