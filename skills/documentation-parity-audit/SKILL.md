# Skill: Documentation Parity Audit

## Description
Verify documentation is truthful to implementation, operationally actionable, and aligned with wrapper-first workflow policy.

## When to use
- A session is assigned to documentation parity or repo navigation quality.
- You update docs that reference scripts, commands, generated artifacts, or quality policy.

## When not to use
- You are doing feature-only code implementation without docs impact.
- You only need first-session onboarding setup (use `template-bootstrap`).

## Environment prerequisites
- POSIX-compatible shell.
- `rg` (`ripgrep`) available on `PATH`.

## Required inputs
- Target documentation files.
- Referenced implementation files and command entry points.

## Canonical commands
- Inspect docs:
  - `sed -n '1,220p' <doc-path>`
- Validate command/path parity:
  - `python scripts/run_precommit_suite.py --help`
  - `python scripts/run_tests.py --help`
  - `rg "<referenced-command-or-path>"`
- Validate edited docs with wrapper:
  - `python scripts/run_precommit_suite.py --scope paths --paths <doc1> <doc2>`

## Closure criteria
- Edited documentation matches current implementation and wrapper syntax.
- Links and referenced paths resolve.
- Any unresolved parity gap becomes a granular checklist task.
