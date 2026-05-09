# Skill: Checklist Audit

## Description
Audit and normalize `Final-Productization-Checklist.md` entries so remaining work is explicit, dependency-ordered, and actionable.

## When to use
- You need to process outstanding checklist work in dependency order.
- You need to split vague backlog entries into concrete tasks with verifiable completion criteria.

## When not to use
- You are primarily implementing code behavior (use `quality-remediation`).
- You are running documentation parity checks for specific docs (use `documentation-parity-audit`).

## Environment prerequisites
- POSIX-compatible shell.
- `rg` (`ripgrep`) available on `PATH`.

## Required inputs
- Current `Final-Productization-Checklist.md` content.
- Related implementation/docs paths referenced by target entries.

## Canonical commands
- Review checklist and dependency order:
  - `sed -n '1,260p' Final-Productization-Checklist.md`
- Validate implementation/doc references:
  - `rg --files`
  - `rg "<term>" <path>`
- Run wrapper checks for modified files:
  - `python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>`

## Closure criteria
- Completed tasks are removed from the checklist.
- Partial work is rewritten as remaining actionable work.
- New surfaced gaps are added with `Scope`, `Target Files`, `Dependencies`, `DONE WHEN`, and `Audit step`.
