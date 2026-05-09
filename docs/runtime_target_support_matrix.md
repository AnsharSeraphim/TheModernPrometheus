# Runtime Target Support Matrix

This matrix defines which contributor runtimes are explicitly supported in this template, which repository assets they are expected to consume, and where support boundaries begin/end.

## Support statuses

- **Supported**: Maintained intentionally; onboarding/docs include direct guidance.
- **Conditionally supported**: Works when users follow wrapper-first/quality policy, but runtime-specific adapters may be minimal.
- **Out of scope**: Not actively supported in this template baseline.

## Runtime matrix

| Runtime target | Status | Instruction surfaces consumed | Required operational caveats | Out-of-scope boundary |
| --- | --- | --- | --- | --- |
| Human local contributors (CLI + editor) | Supported | `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `docs/new_user_onboarding.md`, `.github/workflows/quality-gates.yml`, `.github/PULL_REQUEST_TEMPLATE.md`, wrapper help output | Must run quality/tests via `python scripts/run_precommit_suite.py` and `python scripts/run_tests.py`; do not hand-edit `config/precommit_store/*.json`; do not commit local evidence caches. | IDE-specific plugin setup and per-editor automation are user-managed. |
| Generic terminal coding agents | Supported | `AGENTS.md`, `Final-Productization-Checklist.md`, `docs/agent_bootstrap/operator_context_injection.md`, `skills/*/SKILL.md`, `context/recipes/*` | Must respect checklist dependency ordinality, wrapper-first enforcement, summary-block evidence, and UTF-8/date policy. `skills/*/SKILL.md` files are advisory Markdown playbooks, not vendor-runtime plugin descriptors. | Agent-vendor cloud orchestration semantics are not standardized here. |
| Codex-style agents (Codex/GPT Codex compatible wrappers) | Supported | `AGENTS.md`, `docs/agent_bootstrap/README.md`, `skills/*/SKILL.md`, `context/recipes/*`, `scripts/README.md` | Must use repository wrappers and commit ledger JSON changes produced by wrapper runs when applicable. Skills are consumed by reading Markdown instructions from the repository path; no runtime-specific metadata/front matter contract is required by this template. | Runtime-specific proprietary tool features beyond repository files are not guaranteed. |
| Claude Code | Conditionally supported | `CLAUDE.md`, `.claude/README.md`, `AGENTS.md`, wrapper docs | Claude sessions must follow same wrapper/checklist/evidence rules; no alternate check runner allowed. | Claude cloud configuration/policy management outside repo files is out of scope. |
| GitHub Copilot (IDE + GitHub-native agent modes) | Conditionally supported | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `AGENTS.md`, `scripts/README.md` | Copilot-generated changes remain subject to repository wrappers/checklists and manual review. | Proprietary Copilot routing/model-selection behavior is not controlled by this repo. |
| GitHub PR validation (Actions) | Supported | `.github/workflows/*` (when present), `README.md`, `CONTRIBUTING.md` | Validation must run wrapper scripts in explicit full-check mode (`python scripts/run_precommit_suite.py --scope all --reset-baseline --filter-mode full`) plus `python scripts/run_tests.py`, not ad hoc tool commands. | Organization-wide reusable workflow governance is out of scope for template baseline. |

## Instruction-surface precedence

1. Direct maintainer instructions in-session.
2. `AGENTS.md` and checklist governance.
3. Runtime-specific instruction overlays (`CLAUDE.md`, `.github/copilot-instructions.md`, path instructions).
4. Supporting docs/recipes.

If two sources conflict, contributors should follow this precedence and create a follow-up checklist task to remove the contradiction.

## Shell/tool prerequisite boundary

Repository command assets assume a POSIX-compatible shell and the `rg` (`ripgrep`) executable are available on `PATH`. Environments that cannot provide these tools are out of scope unless maintainers add documented fallback commands.
