# Release Prep Session Recipe

Use this recipe when a session goal includes preparing release-facing documentation and validating that wrapper-governed evidence is ready for handoff.

## Prerequisites

1. Read `AGENTS.md`.
2. Read `docs/agent_bootstrap/operator_context_injection.md`.
3. Read `docs/release_notes.md` and identify the affected release-note sections.
4. Read `Final-Productization-Checklist.md` and confirm dependency order for entries tied to release-prep work.

## Canonical execution flow

1. Implement the release-prep changes (for example docs, policy cross-links, workflow assets).
2. While iterating, run targeted wrapper validation for touched paths:

```bash
python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
```

3. Run scoped tests that cover changed behavior:

```bash
python scripts/run_tests.py --scope paths --select <pytest-selector>
```

4. Before handoff, run full suite closure commands in order:

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

## Required evidence artifacts

- `build/automation_contract/precommit_summary_block.txt`
- `build/automation_contract/test_summary_block.txt`

Copy summary blocks exactly from the generated files (or from the final terminal blocks) without progress log fragments.

## Release-note update contract

- Add entries in `docs/release_notes.md` for tooling or user-facing behavior changes introduced by the session.
- Keep entries implementation-truthful; avoid speculative roadmap text in release notes.
- Use absolute dates from trusted sources when creating dated sections.

## Unresolved-work handoff

If blockers remain:

1. Add or rewrite a granular entry in `Final-Productization-Checklist.md`.
2. Include `Scope`, `Target Files`, `Dependencies`, `DONE WHEN`, and an explicit `Audit step`.
3. Ensure entry wording is actionable remaining work instead of partial-progress notes.

## Session-close checks

- Full wrapper and test suites completed successfully.
- Summary blocks are ready for PR/test evidence notes.
- Release notes capture session changes.
- Any unresolved work is logged as actionable checklist entries.
