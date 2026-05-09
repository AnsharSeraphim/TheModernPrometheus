# Generated Artifact Contracts

This document defines repository contracts for generated artifacts so contributors and coding agents can distinguish committed ledgers from local evidence caches.

## Contract table

| Artifact family | Producer(s) | Consumer(s) | Commit policy | Stability expectations | Schema/shape notes |
| --- | --- | --- | --- | --- | --- |
| `context/project_docstrings_catalog.json` | `python scripts/aggregate_project_docstrings.py --root . --output context/project_docstrings_catalog.json` | Agent bootstrap workflows, prompt recipes, maintainers auditing docstring surface area | **Commit required when regenerated as part of meaningful source/doc updates** because it is a machine-consumable repository asset, not local evidence | Stable top-level object with deterministic symbol inventory ordering expected by downstream tooling | JSON object includes per-module records and symbol metadata emitted by `scripts/aggregate_project_docstrings.py`; treat key renames/removals as a breaking contract update that requires release-note callouts |
| `build/automation_contract/precommit_summary_block.txt` and `build/automation_contract/test_summary_block.txt` | `python scripts/run_precommit_suite.py`, `python scripts/run_tests.py` | PR notes and local session summaries | **Do not commit** (local evidence cache only) | Ephemeral, run-specific outputs; safe to overwrite each run | Plain-text copy-ready summary snippets; content reflects latest local run only |
| `build/automation_contract/docstring_inventory.md` | `python scripts/audit_docstrings.py --scan-root ... --output build/automation_contract/docstring_inventory.md` | Human parity audits, interrogate remediation loops | **Do not commit** (local evidence cache only) | Ephemeral generated report; table content changes with source edits | Markdown report with `Documented symbols` and `Missing docstrings` sections used to drive remediation scope |
| `config/precommit_store/*.json` | `python scripts/run_precommit_suite.py` (including targeted/path/all scopes and resets) | Pre-commit filter workflow, stateless session continuity, pylint failure cache consumers | **Commit required when changed by wrapper runs** | Ledger schema is intentionally stable (`skip` flags and hook/path mappings) so wrapper state remains portable across sessions | Includes per-hook ledgers and `pylint_failures.json`; never hand-edit JSON—use wrapper commands (`--scope`, `--only`, `--reset-baseline`) |

## Producer/consumer boundaries

- Wrapper scripts under `scripts/` are the only supported producers for these artifacts.
- Human edits are only allowed for docs that describe contracts; generated files themselves should be produced by commands, not hand-authored.
- If a generated artifact format changes, update this contract doc and `docs/release_notes.md` in the same commit.

## Verification workflow

1. Regenerate artifacts with canonical wrappers/utilities.
2. Confirm commit boundaries:
   - `context/project_docstrings_catalog.json` and changed `config/precommit_store/*.json` should be staged when updated.
   - `build/automation_contract/` outputs should stay untracked.
3. Validate ignore coverage with `git check-ignore -v build/automation_contract/precommit_summary_block.txt` when needed.

## Failure modes and remediation

- **Symptom:** Wrapper reports success/failure but no summary block appears.
  - **Action:** rerun the wrapper command and inspect local filesystem permissions under `build/automation_contract/`.
- **Symptom:** `config/precommit_store/*.json` changes were made manually.
  - **Action:** discard manual edits, rerun `python scripts/run_precommit_suite.py` in appropriate scope so ledgers are regenerated from tool output.
- **Symptom:** Docstring catalog exists but appears stale relative to Python source.
  - **Action:** rerun `scripts/aggregate_project_docstrings.py` and commit the refreshed JSON.

## Related calibration examples

- See `docs/examples/good_summary_block_usage.md` for canonical summary-block evidence packaging.
- See `docs/examples/bad_evidence_packaging.md` for anti-patterns that should not appear in PR notes or final session summaries.
- See `docs/examples/good_checklist_entry.md` and `docs/examples/good_friction_entry.md` for checklist and friction-entry quality expectations.
