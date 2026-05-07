# Checklist Audit Session Recipe

Use this recipe when the goal is to audit checklist quality, dependency order, and actionability before implementation work begins.

## Preconditions

1. Read `AGENTS.md` and `docs/agent_bootstrap/operator_context_injection.md`.
2. Open `Final-Productization-Checklist.md` and inspect entries from top to bottom.
3. Confirm whether unresolved entries contain dependency blockers or non-actionable language.

## Audit workflow

1. Evaluate each open entry for required template fields (`Scope`, `Target Files`, `Dependencies`, `DONE WHEN`).
2. Resolve ordinality first: if a prerequisite task is incomplete, do not execute dependent tasks.
3. Rewrite vague or partially completed entries into explicit remaining-work tasks.
4. Remove entries that are fully complete and verified.
5. If the audit changes scripts/docs, run targeted wrapper checks for edited files:

```bash
python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
```

6. When checklist edits alter execution policy expectations, run scoped tests if behavior-linked files changed:

```bash
python scripts/run_tests.py --scope changed
```

## Stop conditions

Checklist audit work is complete when:

- Every remaining entry is actionable and dependency-aware.
- Completed work has been removed instead of annotated as narrative progress.
- Any newly discovered friction/work gaps are represented by new granular checklist entries.

## Escalation instructions

If an audit exposes implementation gaps too large for one session, create follow-up entries with:

- Scope
- Target Files
- Dependencies
- DONE WHEN
- Audit step describing the command output or file evidence that surfaced the gap
