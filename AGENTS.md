# Generic Repository Agent Charter

**Scope:** Applies to the entire repository unless a deeper `AGENTS.md` overrides it.

## Baseline conduct
- Write in American English and save files as UTF-8.
- Do not commit binary assets (screenshots, videos, archives). Share them separately in the session summary if needed.
- Mandatory quality gates: Ruff (format + lint, width 120), Pylint, Interrogate (100% docstring coverage), MyPy, Pyright, Deptry, Vulture, and Bandit. Never skip, weaken, or reconfigure them.
- It is **MANDATORY** that you use `scripts/run_precommit_suite.py` and not just individual invocations of tools for remediation and that you submit .json assets that change during your session so our script and filter do not become stale. See below for syntax on using this script.
- The % of completion notice when using `scripts/run_precommit_suite.py` is displayed for your convenience, so you do not erroneously believe the script to be stalling. Note that the calculation that generates this percentage is based on the last complete run and is not authoritatively accurate. It is not uncommon for the script to actually complete at only 25% or another value if the timing entry is stale. Do **NOT** use visible percentage of completion for the script execution as a rationale for using keyboard interrupt / ^C during the script execution. Be patient and **WAIT** for it to finish. This is **MANDATORY**.
- Respect entry ordination directives in checklists, contextualizing your execution based on other available entries. As a sanity check, always question which tasks must be addressed first for a quality execution. Example: If entry `y` depends on results from entry `x` to actually close the task, addressing entry `x` before entry `y`, whether in the same session or consecutive sessions, is **MANDATORY**, as premature remediation of `y` before `x` will lead an agent to mark outstanding work as complete.
- Surface unresolved quality failures (pre-commit, lint, type checking) in `Final-Productization-Checklist.md`.
- **MANDATORY PRIORITY ORDER:** - Pre-commit/testing wrapper failures, warnings, and errors discovered during a session are higher priority than any other pending checklist entries. Agents must remediate these as a PR blocker before proceeding to lower-priority tasks unless an explicit, actionable deferment entry is added to `Final-Productization-Checklist.md` with scope, impacted files, dependency ordering, and `DONE WHEN` criteria for highest-priority follow-up.
- Document newly discovered work items in the checklists with enough context for another contributor to continue.
- Assume parallel contributors: resolve merge conflicts, stale processes, or wiring drift before finishing.

## **MANDATORY TIME AND DATE POLICY**
- Derive any timestamps or datestamps from **Git metadata** or other *trusted* sources; **NEVER** rely on *GPTCodex's internal clock and calendar*, which is intentionally unsynchronized and will produce **incorrect dates**.
- You **MUST NOT IGNORE THIS DIRECTIVE**, **whether naming a folder** or **dating an entry**. GPTCodex's native time and calendar will literally date logs *a year into the future or the past* if you use it as a source of truth, causing us to mistakenly destroy new logs we believe to be old, replace new provenance with old provenance, and even cause redundant task churn due to misunderstanding of ordinal progression.

## Stateless agent quickstart context pack (read first)
- Read `docs/agent_bootstrap/operator_context_injection.md` before making edits so wrapper syntax and commit/PR discipline are loaded explicitly.
- Use the copy-ready command blocks in that playbook instead of reconstructing CLI syntax from memory.
- If friction appears that cannot be remediated in-session, add granular checklist entries (with `Scope`, `Target Files`, `Dependencies`, `DONE WHEN`, and an **Audit step**) in `Final-Productization-Checklist.md`.

## Quality workflow
1. **While iterating, refresh the skip manifests for every touched file.**
   - Canonical command: `python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>`
     - Run a single hook in targeted mode with `python scripts/run_precommit_suite.py --only <hook> --scope paths --paths <file1> <file2>`.
       The wrapper resets the skip bit for each targeted path before executing so fresh diagnostics are recorded.
     - Run a whole-project sweep with `python scripts/run_precommit_suite.py --scope all`.
   - Useful switches:
     - `--only <hook>` to focus on a single tool.
     - `--scope changed --diff-target <ref>` to scan staged/untracked changes versus a branch.
    - `--reset-baseline` to rebuild each manifest from tracked Python sources, clear all skip flags, and reseed the ledger. Run it
      alone for a full-suite baseline or pair it with `--only` to reset targeted hooks (leaving the rest at `skip="N"` until you
      rerun them or drop their JSON diffs).
     - `--filter-mode full` or `WRAPPER_NO_CACHE=1` to bypass the skip cache temporarily.
   - Each hook stores its state in `config/precommit_store/<hook>.json`. New paths appear automatically with `"skip": "N"`. Passing runs flip the entry for a file to `"skip": "Y"`; targeted runs on edited files reset the flag to `"N"` until the hook succeeds again.
- Native Git integration is also available: `pre-commit run --files <path> [...]`.
    - Manual hook aliases (for example `pre-commit run ruff-lint`) now emit guidance that routes you back through `scripts/run_precommit_suite.py` so the skip manifests and pylint failure cache stay authoritative. Use the unified runner instead of the manual aliases.
    - If you cancel the unified pre-commit runner before it completes, the skip manifests roll back to their previous state. Restart the run when you're ready so the JSON ledger reflects the final attempt.
   - Remediation means fixing the files called out by the hook output. Never edit tool settings, ignore lists, or JSON manifests to hide failures.
- Never hand-edit `config/precommit_store/*.json`; use the runner to reset flags instead (see `--reset-baseline`).
- Pylint failures are cached in `config/precommit_store/pylint_failures.json`. When the runner surfaces new diagnostics,
  commit the updated failure manifest alongside the main skip JSON files so subsequent agents see the same cached output.
  Baseline resets (`--reset-baseline`) clear both the skip flags and the failure cache.
2. **Session close:** run the complete automation suites back-to-back before summarizing or opening a PR:
   - `python scripts/run_precommit_suite.py`
   - `python scripts/run_tests.py`
3. **Capture the result blocks, not progress logs.**
 - Each suite writes a ready-to-copy snippet under `build/automation_contract/` (e.g., `precommit_summary_block.txt`, `test_summary_block.txt`).
  - When copying directly from the terminal, start at the final line (`Pre-commit suite …` / `Pytest suite …`) and select upward until you include the banner and table. Do **not** clip intermediate progress (percentages, hook streaming, etc.).
  - Paste these exact blocks into PR summaries, testing notes, and final responses.
- Keep the automation output directories (`build/automation_contract/` and `reports/reasoning/pipeline/`) untracked. They are local evidence caches, not source assets. If they appear in `git status`, delete the tracked files and ensure the root `.gitignore` coverage stays intact.

## Testing expectations
- Run the pytest scope that covers the code you changed (e.g., `python scripts/run_tests.py --scope paths --select <pattern>` or `--scope changed`).
- If you modify a test file or create a new test, the test latency budget is 0.20s. If a new or modified test cannot be optimized to run at this time or under, it must be documented in `Final-Optimization-Checklist.md` with a justification for its latency overage and inability to be further optimized.
- Do not modify `Final-Optimization-Checklist.md` for unchanged tests, unless specifically directed.

## Checklist governance parity (all contributors and all agent runtimes)
- `Final-Productization-Checklist.md` is the canonical backlog for unresolved implementation/documentation/tooling work. Keep entries actionable, dependency-aware, and removable when complete.
- `Final-Optimization-Checklist.md` is the canonical ledger for over-budget tests tied to the 0.20s policy; maintain separate sections for pending optimization audits versus code-audited justified exceptions.
- In `Final-Optimization-Checklist.md`, the `✅` symbol is reserved for confirmed justified exceptions only after an explicit test-level code audit proves additional optimization would compromise test fidelity/purpose.
- Apply checklist policy consistently across human contributors and coding-agent platforms (GPT Codex, Claude Code, GitHub Copilot, and others); do not assume runtime-specific implicit behavior.
- When checklist governance changes, update repository-facing documentation (`README.md`, `docs/new_user_onboarding.md`, agent guidance files) in the same session to preserve instruction parity.

## Operational hygiene
- Update `docs/release_notes.md` when tooling or user-facing behavior changes.
- Keep manifests, release indexes, and evidence logs consistent with your edits.

These directives keep parallel contributors aligned and the automation evidence trustworthy.

## Workflow-friction escalation authorization
- Agents are authorized to add actionable entries in the `Coding-Agent-Surfaced Execution Friction / What Will Make Agents Able To Navigate Your Project More Easily` section of `Final-Productization-Checklist.md` when they discover reproducible workflow/context failures; each entry must include `Scope`, `Target Files`, `Dependencies`, `DONE WHEN`, and an `Audit step`.
