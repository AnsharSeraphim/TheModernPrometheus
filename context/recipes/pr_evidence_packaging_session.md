# PR Evidence Packaging Session Recipe

Use this recipe to prepare pull request evidence that matches repository wrapper policy and checklist governance.

## Prerequisites

1. Read `AGENTS.md`.
2. Read `docs/agent_bootstrap/operator_context_injection.md`.
3. Confirm implementation work is complete or residual work is captured in `Final-Productization-Checklist.md`.

## Canonical command sequence

Run wrapper closure commands immediately before packaging evidence:

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

If additional remediation is needed, use targeted wrapper loops before rerunning the full sequence:

```bash
python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
python scripts/run_tests.py --scope paths --select <pytest-selector>
```

## Evidence packaging steps

1. Collect final output blocks from:
   - `build/automation_contract/precommit_summary_block.txt`
   - `build/automation_contract/test_summary_block.txt`
2. In PR notes, include:
   - Checklist entry/task addressed.
   - Scoped remediation commands used.
   - Full-suite summary blocks.
   - Explicit unresolved items, if any.
3. Do not paste streaming progress logs, completion percentages, or partial hook snippets.

## Unresolved-work rules

If evidence shows unresolved failures that cannot close in-session:

1. Add granular checklist entries in `Final-Productization-Checklist.md`.
2. Include exact failing scope and files.
3. Add audit instructions so the next operator can reproduce and verify closure.

## Session-close checks

- PR notes contain both summary blocks and command history.
- Any unresolved failures are represented as actionable checklist entries.
- Local evidence directories remain untracked by Git.
