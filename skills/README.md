# Repository Skill Pack

This directory contains repository-local `SKILL.md` assets for high-frequency stateless workflows.
These files are human-readable/advisory playbooks stored in source control, not runtime plugin manifests.

## Available skills

- `quality-remediation/SKILL.md`: implementation + wrapper remediation loops.
- `checklist-audit/SKILL.md`: checklist dependency/actionability audits.
- `documentation-parity-audit/SKILL.md`: documentation-to-implementation parity audits.
- `template-bootstrap/SKILL.md`: first-session bootstrap for template consumers.

## Runtime support

These skills are designed for human contributors and terminal coding agents that can read Markdown instructions and execute repository commands.
Runtime support boundaries are defined in `docs/runtime_target_support_matrix.md`.

## Environment prerequisites

- POSIX-compatible shell (examples use `bash` syntax).
- `rg` (`ripgrep`) installed and available on `PATH`.

## Usage contract

1. Read `AGENTS.md` and `docs/agent_bootstrap/operator_context_injection.md` first.
2. Choose one skill matching the session objective.
3. Execute canonical commands exactly as written (wrapper-first).
4. If the task cannot close in-session, create granular checklist follow-up entries.
