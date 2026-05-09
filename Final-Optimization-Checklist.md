# Final Optimization Checklist

This checklist tracks **new or modified tests** that exceed the per-test latency budget of **0.20 seconds**.

## Purpose and Policy

- Optimize tests whenever latency can be reduced **without compromising fidelity of purpose or coverage**.
- Justification is allowed only when additional optimization would degrade the test's intended behavior, confidence, or coverage quality.
- Prefer batching related test optimizations in one session to capture interaction effects and avoid duplicate work.

## Required Workflow for Agents

1. Run tests through the project wrapper (`python scripts/run_tests.py`) and inspect duration output.
2. For any **new or modified** test over 0.20s:
   - Optimize first.
   - If further optimization is not possible without fidelity loss, add a justification entry in the section below.
3. If a test is over 0.10s and can be improved easily without loss of fidelity, optimize it in-session.
4. When an optimization task is completed, remove its open entry instead of leaving stale progress notes.

## Open Optimization Tasks

- No optimization follow-ups are currently open.

## Justified Latency Exceptions (Over 0.20s)

Use this section only for tests that cannot be reduced to 0.20s or less without reducing fidelity.

Template for each exception:

- **Test:** `<path>::<nodeid>`
- **Observed Duration:** `<seconds>`
- **Why optimization would reduce fidelity:** `<reason>`
- **Attempted optimizations:** `<what was tried>`
- **Scope:** `<module/domain>`
- **Target Files:** `<files involved>`
- **Dependencies:** `<prerequisites or blockers>`
- **DONE WHEN:** `<conditions to remove this exception>`
- **Audit step:** `<exact command(s) to verify>`

Current exceptions:

- None.
