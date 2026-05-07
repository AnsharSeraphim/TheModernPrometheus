# Quality Remediation Session Recipe

Use this recipe when a session needs to remediate code or documentation while preserving wrapper-ledger integrity.

## Preconditions

1. Read `AGENTS.md`, `docs/agent_bootstrap/operator_context_injection.md`, and `Final-Productization-Checklist.md` in order.
2. Select the highest-ordinal checklist entry that has no unresolved dependency.
3. Confirm target files before editing so scoped wrapper runs can use explicit paths.

## Execution loop

1. Apply implementation and documentation edits for the selected task.
2. Run scoped quality checks for every touched path:

```bash
python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
```

3. If one hook remains noisy, run a targeted hook pass without bypassing the wrapper:

```bash
python scripts/run_precommit_suite.py --only <hook> --scope paths --paths <file1> <file2>
```

4. Run scoped tests that cover the change:

```bash
python scripts/run_tests.py --scope paths --select <pytest-selector>
```

5. Repeat until targeted checks pass without introducing new failures.

## Stop conditions

A session can move to closure only when all of the following are true:

- The selected checklist task is fully complete, or the remaining work has been rewritten into explicit follow-up entries.
- No new warnings/errors introduced by the session remain unresolved.
- Required docs (`docs/release_notes.md`, checklist files, onboarding/bootstrap docs) match implementation changes.

## Session close commands (mandatory)

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

Copy summary blocks from `build/automation_contract/precommit_summary_block.txt` and `build/automation_contract/test_summary_block.txt` into the final report/PR notes.

## Escalation protocol

If remediation cannot be completed in-session, add a granular checklist entry in `Final-Productization-Checklist.md` with:

- Scope
- Target Files
- Dependencies
- DONE WHEN
- Audit step with concrete reproduction/validation instructions
