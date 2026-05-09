# Calibration Examples for Stateless Agents

This directory contains **paired examples** that show what acceptable and unacceptable execution artifacts look like in this repository.

## How to use these examples

1. Read the matching good/bad pair for the artifact you are producing.
2. Compare your draft against the good example's invariants.
3. Use the bad example's failure mode list as a final pre-submit check.

## Example index

- `good_checklist_entry.md`
  - Why this is good: uses bounded scope, explicit dependencies, and a verifiable `DONE WHEN` plus audit step.
- `bad_checklist_entry.md`
  - Why this is bad: includes unbounded wording, no dependency handling, and no objective closure criteria.
- `good_summary_block_usage.md`
  - Why this is good: copies final wrapper summary blocks and avoids progress-log noise.
- `bad_evidence_packaging.md`
  - Why this is bad: mixes partial logs with claims, omits command boundaries, and hides failed checks.
- `good_friction_entry.md`
  - Why this is good: reports reproducible workflow friction with actionable remediation metadata.

## Calibration invariants these examples enforce

- Checklist entries are work items, not session journals.
- Evidence packaging uses canonical wrapper outputs from `build/automation_contract/`.
- Friction entries are reproducible and implementation-directed, not vague complaints.
