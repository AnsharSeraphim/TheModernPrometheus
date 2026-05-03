# The Modern Prometheus / GitHub Repository Template

This GitHub Repository Starter is a reusable repository-bootstrap system for creating agent-ready, quality-controlled Python projects. It packages the instructions, scripts, ledgers, checklists, policies, and automation needed for a repository to begin with disciplined execution rather than acquiring rules later through preventable execution failures.

The starter includes coding-agent directives, contributor instructions, unified pre-commit orchestration, unified test orchestration, strict lint/type/security/docstring checks, UTF-8 policy, release-note practices, checklist templates, and per-hook JSON skip ledgers. The skip-ledger design allows quality-assurance hooks to avoid rechecking the whole repository on every iteration by focusing on touched or not-yet-cleared files.

The system can be extended from single-contributor use to multi-contributor work by adding stronger file identity metadata such as blob hashes, modification times, contributor scope, and manifest reconciliation. Its docstring aggregation and interrogation functions also support rapid conceptual audit: reviewers can inspect what the code claims each module, class, and function is doing without reading the entire repository from scratch. This system also allows .json export of Docstring Manifests for frictionless LLM processing for the purpose of project documentation, user manuals, and conceptual audit.

## Repository map

- `scripts/`: Canonical automation entry points and supporting quality/test utilities.
- `tests/`: Verification of wrapper behavior and policy enforcement helpers.
- `config/precommit_store/`: Pre-commit skip ledgers plus cached pylint diagnostics used by wrapper flows.
- `docs/`: Narrative documentation and release history.
- `Final-Productization-Checklist.md`: Open, actionable backlog for unresolved template hardening work.
- `Final-Optimization-Checklist.md`: Tracking for tests above the latency budget with explicit rationale.

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
- Direct/manual invocations (`pre-commit run <hook>`, naked `pytest`) are treated as policy violations because they bypass repository summary artifacts and skip-ledger coordination.

## Docstring automation support

- `scripts/aggregate_project_docstrings.py` exports a monolithic JSON catalog of Python module/class/function docstrings for contextual bootstrap workflows and machine-readable downstream processing.
- `scripts/audit_docstrings.py` generates a human-readable Markdown inventory of discovered docstrings so reviewers can run live implementation-vs-documentation parity audits with line-level symbol visibility.
- Interrogate is configured at 100% coverage in project tooling and is executed via the pre-commit wrapper.

## Documentation expectations for template consumers

- Keep folder-level `README.md` files current so new users and stateless agents can navigate assets without hidden context.
- Update `docs/release_notes.md` whenever tooling behavior, quality workflow, or user-facing repository operation changes.
