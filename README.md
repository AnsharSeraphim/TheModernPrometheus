# The Modern Prometheus
> **A GitHub Repository Template Designed For Working With Coding Agents**

**Initial Design:** Anshar Seraphim  
**ORCID:** [0009-0001-9104-4812](https://orcid.org/0009-0001-9104-4812)

---
**New here?** Start with [New User Onboarding](docs/new_user_onboarding.md) for a plain-language tour of the repository's purpose, wrapper-first workflow, quality gates, checklist discipline, and coding-agent operating model.
---

## Welcome to The Modern Prometheus - Project Description
This GitHub Repository Starter is a reusable repository-bootstrap system for creating agent-ready, quality-controlled Python projects. It packages the instructions, scripts, ledgers, checklists, policies, and automation needed for a repository to begin with disciplined execution rather than acquiring rules later through preventable execution failures.

The starter includes coding-agent directives, contributor instructions, unified pre-commit orchestration, unified test orchestration, strict lint/type/security/docstring checks, UTF-8 policy, release-note practices, checklist templates, and per-hook JSON skip ledgers. The skip-ledger design allows quality-assurance hooks to avoid rechecking the whole repository on every iteration by focusing on touched or not-yet-cleared files.

The system can be extended from single-contributor use to multi-contributor work by adding stronger file identity metadata such as blob hashes, modification times, contributor scope, and manifest reconciliation. Its docstring aggregation and interrogation functions also support rapid conceptual audit: reviewers can inspect what the code claims each module, class, and function is doing without reading the entire repository from scratch. This system also allows .json export of Docstring Manifests for frictionless LLM processing for the purpose of project documentation, user manuals, and conceptual audit.

## Prompting Coding-LLMs
Use the reusable prompt library under `context/prompts/`:

- Start with `context/prompts/README.md` to choose the prompt by task objective.
- Use `context/prompts/quality_remediation_prompt.md` for wrapper-driven lint/type/security remediation loops.
- Use `context/prompts/checklist_audit_prompt.md` for checklist hygiene and dependency-order audits.
- Use `context/prompts/repo_audit_prompt.md` for implementation/documentation parity sweeps.
- Use `context/prompts/template_bootstrap_prompt.md` for first-session template setup work.
- Use `context/prompts/pr_evidence_packaging_prompt.md` for PR notes and summary-block evidence packaging.

This keeps operational prompts versioned and close to the workflows they describe.

**If you use GPT Codex to work with this base template in a project, here is a convenient prompt generator for your sessions:**
> [Create a GPT Codex Prompt On Demand](https://chatgpt.com/g/g-6a07ac8fb7888191bffd4e74b4431990-gpt-codex-dynamic-prompt-engine)

You can use this generic monolithic prompt if you've localized all pending tasks to `Final-Productization-Checklist.md`:
```
# Execute tasks and ensure no precommit script hook violations in project, maintain parity with documentation
* Address tasks described in `Final-Productization-Checklist.md` through remediation/implementation of described issues/goals to the maximum extent allowed by your session (no minimal executions, genuinely address a significant scope, not just checklist updates or diagnostics)  

## Following directives in `AGENTS.md` about pre-commit syntax, perform tasks as below
* Address tasks in `Final-Productization-Checklist.md`, starting with the tasks that must be completed before future tasks and implementation can be addressed.
* Diagnose/Resolve any surfacing failures/warnings/errors related to your execution to keep our progress momentum on any backlog of pre-commit violations.
* If you see multiple checklist entries or items that are easily combined into a single execution, it's helpful to address as many as you can in order to reduce the total number of needed sessions. 
* If you need to break a task into pieces and create new checklist entries for other agents to pick up where you left off, it's permitted, but make a genuine effort to complete work and address as many files as possible listed in the current phase, where possible.
* If, during the course of your work, you discover something that needs implementation, isn't working how it should be, or clearly is just a scaffolded idea that isn't been finished with logic, create new checklist entries for that surfaced task/gap, etc, as well.
* Pay attention to ordinality of tasks. If a task that's lower in the checklist depends on other checklist items to be complete to wire it properly, **DO NOT PROCESS THAT TASK FIRST** 
* If completion of your current task then adds more granularity to an existing checklist entry, update it, if completion surfaces a need for further implementation or steps, ensure that actionable checklist entry is created. 
* DO NOT TAKE SHORTCUTS when addressing problems or implementing design. Remediate issues properly, not by just circumventing or shimming around a problem, our suite is designed to surface problems, you are to remediate those problems, not simply silence warnings, errors, or failures, when something needs addressing. If you find such a workaround in use and a genuine problem is being hidden, remove whatever is silencing warnings, errors, or failures. 
* Only work on `Final-Optimization-Checklist.md` tasks if entries there indicate no current optimization and they exceed a latency budget of 0.30 s, unless directed to, specifically.
* As long as entries exist for tests above the latency budget, do not update them unless you are working on them. Rationale: This keeps you from "updating test times" and calling this an execution.
* Tests may ONLY be marked slow or to skip if rationale and justification is surfaced in `Final-Optimization-Checklist.md`. If you find something undocumented, document it, or release the skip or slow marker so it can be surfaced for remediation.

### Finishing Your Session
* Ensure you've removed checklist entries for completed work or stale entries, transforming entries that are partially addressed into what remains to be done rather than annotation of partial progress, which can lead to task churn. Ensure any updates to existing checklist entries that are affected by your execution are made and that any new tasks that have become evident from your execution are likewise created in the checklist for iterative-progress, needed improvements, and quality documentation.
```

## Repository map

- `scripts/`: Canonical automation entry points and supporting quality/test utilities.
- `tests/`: Verification of wrapper behavior and policy enforcement helpers.
- `config/precommit_store/`: Pre-commit skip ledgers plus cached pylint diagnostics used by wrapper flows.
- `docs/`: Narrative documentation and release history.
- `docs/runtime_target_support_matrix.md`: runtime-by-runtime support boundary, instruction surfaces, and caveats for humans and coding-agent platforms.
- `docs/context_trigger_matrix.md`: workflow-to-context load-order matrix for stateless sessions.
- `docs/generated_artifact_contracts.md`: producer/consumer contracts, commit boundaries, and schema expectations for generated artifacts used by wrappers and audits.
- `docs/source_boundary_manifest.md`: source-of-truth boundary map for hand-authored files vs generated committed ledgers vs local-only evidence.
- `docs/template_customization_checklist.md`: post-clone checklist for replacing template defaults with project-specific governance and metadata.
- `docs/security_hygiene.md`: security and data-boundary guide for secrets, local evidence, and deny-path commit policy.
- `docs/troubleshooting.md`: common wrapper/tooling failure signatures and canonical remediation paths.
- `.gitignore`: Ignore policy for local evidence caches, Python-generated artifacts, virtual environments, and editor-local state.
- `Final-Productization-Checklist.md`: Open, actionable backlog for unresolved template hardening work.
- `Final-Optimization-Checklist.md`: Tracking for tests above the latency budget with explicit rationale.

## Checklist policy quick reference (humans + coding agents)

- `Final-Productization-Checklist.md` stores unresolved, execution-ready work items; remove entries when fully complete and rewrite partial items as explicit remaining scope.
- `Final-Optimization-Checklist.md` governs tests that exceed the 0.20s latency budget and must separate:
  - pending comprehensive optimization audits, and
  - confirmed justified latency exceptions.
- The `✅` marker in `Final-Optimization-Checklist.md` is reserved for exceptions that have completed a test-level code audit proving further optimization would compromise fidelity/purpose.
- Apply the same checklist contract across GPT Codex, Claude Code, GitHub Copilot, and manual human workflows so documentation and execution evidence remain consistent.

## Start here

1. Create and activate a virtual environment.
2. Install dev dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

3. Run the required wrappers (never bypass these at session close):

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

## Wrapper-first contributor policy

- Quality hooks must be driven by `scripts/run_precommit_suite.py` (including checklist-structure validation for `Final-Productization-Checklist.md`).
- Tests must be driven by `scripts/run_tests.py`.
- GitHub validates the same wrapper contract in `.github/workflows/quality-gates.yml` for pull requests and pushes to primary branches, but forces full-check mode with `--scope all --reset-baseline --filter-mode full` so clean checkouts cannot pass by reusing committed skip-ledger state.
- Pull requests should use `.github/PULL_REQUEST_TEMPLATE.md` so scoped commands and final summary blocks are always included.
- Direct/manual invocations (`pre-commit run <hook>`, naked `pytest`) are treated as policy violations because they bypass repository summary artifacts and skip-ledger coordination.

## Timestamp and UTF-8 policy

- Save repository text assets as UTF-8.
- Derive dates/timestamps from trusted sources (for example Git metadata, filesystem metadata, or wrapper output), not model-relative/internal clocks.
- When documenting execution timelines, prefer explicit absolute dates from those trusted sources.

## Dependency and tooling reproducibility posture

- Python runtime is intentionally pinned to `>=3.13,<3.14` in `pyproject.toml` so contributors and automation runners execute under a single interpreter target that matches Ruff, MyPy, Pyright, and Pylint settings.
- Build backend packages (`setuptools`, `wheel`) and development tools use explicit lower and upper bounds (`>=x,<next-major`) to reduce resolver drift while still accepting patch/minor security and stability updates.
- Strict checker posture is intentional: MyPy and Pyright both run in strict modes, Ruff linting selects correctness/simplification rule families, and interrogate enforces 100% docstring coverage.
- Dependabot grouping is configured in `.github/dependabot.yml` to batch Python quality-tooling and GitHub Actions updates separately, reducing review noise while preserving frequent update cadence.

## Docstring automation support

- `scripts/aggregate_project_docstrings.py` exports a monolithic JSON catalog of Python module/class/function docstrings for contextual bootstrap workflows and machine-readable downstream processing.
- `scripts/audit_docstrings.py` generates a human-readable Markdown inventory of discovered docstrings so reviewers can run live implementation-vs-documentation parity audits with line-level symbol visibility.
- Interrogate is configured at 100% coverage in project tooling and is executed via the pre-commit wrapper.

## Documentation expectations for template consumers

- Review `docs/security_hygiene.md` for secret-handling and local-vs-source boundary rules before your first commit.

- Keep folder-level `README.md` files current so new users and stateless agents can navigate assets without hidden context.
- Keep local evidence and local Python runtime artifacts out of source control by relying on the root `.gitignore`; use `git check-ignore -v <path>` when verifying new local-only paths.
- Update `docs/release_notes.md` whenever tooling behavior, quality workflow, or user-facing repository operation changes.
