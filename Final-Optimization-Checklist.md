# Final Optimization Checklist

This checklist tracks **new or modified tests** that exceed the per-test latency budget of **0.20 seconds**.

## Purpose and Policy

- Optimize tests whenever latency can be reduced **without compromising fidelity of purpose or coverage**.
- Justification is allowed only when additional optimization would degrade the test's intended behavior, confidence, or coverage quality.
- Prefer batching related test optimizations in one session to capture interaction effects and avoid duplicate work.
- A checklist exception may be marked with `✅` **only** after a documented, test-level code audit confirms no further optimization is possible without fidelity loss.
- `✅` is reserved exclusively for confirmed exceptions in this file; do not use `[x]` for confirmed latency exceptions.

## Required Workflow for Agents

1. Run tests through the project wrapper (`python scripts/run_tests.py`) and inspect duration output.
2. For any **new or modified** test over 0.20s:
   - Optimize first.
   - If further optimization is not possible without fidelity loss, perform and document a code audit, then add the test to **Confirmed Justified Latency Exceptions (`✅` only)**.
3. For any **new or modified** test over 0.20s that has not yet received a comprehensive code audit, add it to **Pending Comprehensive Optimization Audits** (no `✅`).
4. If a test is over 0.10s and can be improved easily without loss of fidelity, optimize it in-session.
5. Ordinate test entries by **longest runtime to shortest runtime** within each section.
6. When an optimization task is completed, remove its open entry instead of leaving stale progress notes.

## Session Evidence Requirement

- Before editing this checklist for runtime updates, run `python scripts/run_tests.py` to refresh timing evidence.
- Every timing entry must include the run context (command and date source) from trusted execution evidence (wrapper output and/or git metadata); never use model-internal date assumptions.

## Open Optimization Tasks

- No optimization follow-ups are currently open.

## Pending Comprehensive Optimization Audits (No `✅`)

Use this section for tests over 0.20s that still need a real optimization audit.

Template for each pending audit entry:

- **Test:** `<path>::<nodeid>`
- **Observed Duration:** `<seconds>`
- **Why it is currently over budget:** `<initial observation>`
- **Required audit scope:** `<fixtures/mocks/io/setup/parametrization to inspect>`
- **Scope:** `<module/domain>`
- **Target Files:** `<files involved>`
- **Dependencies:** `<prerequisites or blockers>`
- **DONE WHEN:** `<clear completion criteria for optimization or justified exception>`
- **Audit step:** `<exact command(s) to verify>`

Current pending audits:

- None.

## Confirmed Justified Latency Exceptions (`✅` only; over 0.20s)

Use this section only for tests where a completed code audit confirms additional optimization would compromise fidelity.

Template for each confirmed exception:

- ✅ **Test:** `<path>::<nodeid>`
- **Observed Duration:** `<seconds>`
- **Code-audit conclusion (fidelity risk):** `<why optimization would reduce fidelity>`
- **Attempted optimizations:** `<what was tried and measured>`
- **Scope:** `<module/domain>`
- **Target Files:** `<files involved>`
- **Dependencies:** `<prerequisites or blockers>`
- **DONE WHEN:** `<conditions to remove this exception>`
- **Audit step:** `<exact command(s) to verify>`

Current confirmed exceptions:

- None.
