# Prompt Library for Stateless Sessions

This directory centralizes reusable prompts for high-frequency repository workflows.

## How to use these prompts

1. Choose the prompt that matches your task objective.
2. Read the prompt's ingestion order and load the named files before running commands.
3. Execute only canonical wrapper commands from `scripts/`.
4. Capture evidence from `build/automation_contract/` and close or rewrite checklist entries.

## Prompt index

- `repo_audit_prompt.md`: full repository audit of docs + implementation parity.
- `quality_remediation_prompt.md`: wrapper-first remediation for lint/type/security failures.
- `checklist_audit_prompt.md`: backlog hygiene and dependency-order audit.
- `template_bootstrap_prompt.md`: first-session setup for a repo cloned from this template.
- `pr_evidence_packaging_prompt.md`: prepare PR notes with wrapper summary-block evidence.

## Closure requirement

A prompt run is complete only when:

- required wrappers were executed with canonical syntax,
- unresolved issues were moved into granular checklist entries, and
- final evidence blocks were captured from `build/automation_contract/`.
