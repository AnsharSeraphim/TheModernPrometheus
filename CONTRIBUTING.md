# Contributing

This repository is a generic Python automation scaffold that can be reused as a baseline for new projects.

All contributors must follow [AGENTS.md](AGENTS.md), the [Code of Conduct](CODE_OF_CONDUCT.md), and the [security hygiene guide](docs/security_hygiene.md).

## Local setup

1. Create and activate a Python 3.13 virtual environment (the repository pins `>=3.13,<3.14`).
2. Install the shared development tooling:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements-dev.txt
   ```
3. Optionally install Git hooks:
   ```bash
   pre-commit install
   ```

## Required quality workflow

The repository uses a unified runner so contributors do not need to remember each lint or type-check command individually.

### While iterating on a subset of files

Run the targeted pre-commit suite for every file you touch:

```bash
python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
```

You can focus on a single hook with:

```bash
python scripts/run_precommit_suite.py --only <hook> --scope paths --paths <file1> <file2>
```

### Before opening a pull request

Run the full automation sequence in this order:

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

Each runner writes a copy-ready summary block under `build/automation_contract/`. Use those blocks in PR notes or review summaries instead of copying incomplete progress logs.

## Commit and PR segmentation policy

To keep reviews tractable, split work into phases instead of submitting a single oversized diff.

- Never commit binary evidence artifacts (screenshots, videos, archives).
- Keep local evidence caches and Python local-state artifacts untracked via the root `.gitignore`; verify additions with `git check-ignore -v <path>`.
- Commit wrapper-managed ledger changes in `config/precommit_store/*.json` whenever the wrapper updates them.
- Trigger phased execution when either threshold is met:
  - more than 25 files changed in one work unit, or
  - more than 1,200 net changed lines (additions + deletions) in one work unit.
- Keep each phase centered on one checklist task (or one direct prerequisite + dependent pair).

Per-phase validation before each phase commit:

```bash
python scripts/run_precommit_suite.py --scope paths --paths <touched-file1> <touched-file2>
python scripts/run_tests.py --scope paths --select <relevant-selector>
```

Final validation before PR publication:

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

Remote CI runs an explicit full-check variant of the quality wrapper:

```bash
python scripts/run_precommit_suite.py --scope all --reset-baseline --filter-mode full
python scripts/run_tests.py
```

This ensures repository-wide validation executes hooks instead of inheriting committed skip-ledger pass state.

PR evidence expectations:

- Include the final summary blocks from `build/automation_contract/`.
- List the scoped remediation commands executed for the phase.
- If anything remains unresolved, add a checklist entry in `Final-Productization-Checklist.md` and link it in the PR notes.

Use `context/recipes/pr_evidence_packaging_session.md` for a copy-ready evidence packaging workflow, and `context/recipes/release_prep_session.md` when the session includes release-note updates.

## Tooling inventory

The pre-commit suite currently orchestrates:

- Ruff format
- Ruff lint
- Pylint
- Interrogate (100% docstring coverage)
- MyPy
- Pyright
- Deptry
- Vulture
- Bandit
- UTF-8 + Unicode escape policy checks

## Testing expectations

- Use `python scripts/run_tests.py --scope paths --select <test-path-or-nodeid>` for focused runs.
- Keep individual tests fast. If a new or modified test exceeds 0.20 seconds, document the justification in `Final-Optimization-Checklist.md`.
- Use `Final-Productization-Checklist.md` to record unresolved tooling or productization gaps that are out of scope for the current session.

## Release notes

Update [docs/release_notes.md](docs/release_notes.md) whenever tooling, contributor workflow, or user-visible repository behavior changes.

## Template onboarding

If you are using this repository as a starter template, complete this onboarding path before your first PR:

1. Read `README.md` for repository purpose and layout.
2. Read `AGENTS.md` for wrapper-first policy, required quality gates, and checklist governance.
3. Run the canonical command flow:
   - `python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>` while iterating.
   - `python scripts/run_precommit_suite.py` then `python scripts/run_tests.py` before review.
4. Collect evidence artifacts from `build/automation_contract/` and paste the summary blocks in your PR/testing notes.
5. If a failure cannot be fixed in-session, add a granular remaining-work entry to `Final-Productization-Checklist.md` with scope, target files, dependencies, and DONE WHEN criteria.

- Review `docs/troubleshooting.md` for common failure signatures and wrapper-first remediation paths before escalating unresolved issues.

Failure/remediation flow:
- Wrapper reports failing hook/test target.
- Remediate implementation (never suppress tooling).
- Re-run wrapper on touched paths.
- Re-run full wrappers before handoff.

## Pull request evidence template

Use [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) when opening a PR. The template mirrors wrapper-evidence policy by requiring:

- checklist task scope and touched behavior summary,
- scoped remediation commands,
- pasted final summary blocks from `build/automation_contract/`, and
- explicit unresolved follow-up entries in `Final-Productization-Checklist.md`.

Remote CI runs the same wrapper contract through [`.github/workflows/quality-gates.yml`](.github/workflows/quality-gates.yml).
