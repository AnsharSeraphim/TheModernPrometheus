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
- If changed quality-ledger JSON files under `config/precommit_store/` are produced by wrapper runs, include them in the commit.
- Do not hand-edit skip manifests or pylint cache files.
- Large workflow changes must be phased when diffs approach repository/platform limits (for example near 100k changed lines).
- A session that commits must also produce a PR message with test evidence summaries.

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
