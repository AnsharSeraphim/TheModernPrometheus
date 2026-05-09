# Documentation Parity Audit Session Recipe

Use this recipe when auditing documentation against current implementation and wrapper policy.

## Ingestion order (required)

1. `AGENTS.md`
2. `scripts/README.md`
3. `Final-Productization-Checklist.md`
4. `docs/new_user_onboarding.md`

Then read the documentation file(s) in scope and any implementation files they reference.

## Parity audit checks

For each targeted document:

1. Validate command/path parity with current wrapper entry points.
2. Cross-check implementation claims against current code or scripts.
3. Verify local anchors, relative links, and table-of-contents integrity.
4. Confirm mechanism depth (inputs, outputs, failure behavior) is sufficient for stateless execution.
5. Remove stale prose or convert speculative statements into explicit roadmap language.

## Command and path validation workflow

When documentation references executable commands or script flags:

```bash
python scripts/run_precommit_suite.py --scope paths --paths <doc1> <doc2>
python scripts/run_tests.py --scope paths --select <pytest-selector>
```

Use targeted code/tests where doc changes describe implementation behavior that requires verification.

## Implementation cross-check rules

- Treat wrapper output and implementation behavior as source of truth when documentation drifts.
- If implementation has defects discovered during audit, create a separate actionable checklist entry for remediation before marking doc parity complete.

## Follow-up checklist requirements

If parity gaps cannot be remediated in-session, create entries in `Final-Productization-Checklist.md` with:

- `Scope`
- `Target Files`
- `Dependencies`
- `DONE WHEN`
- `Audit step`

Entries must define exact remaining work and verification criteria.

## Closure expectations

Before handoff:

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

Capture summary blocks from `build/automation_contract/` and include them in PR/session evidence.
