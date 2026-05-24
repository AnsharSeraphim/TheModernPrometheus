# New User Onboarding: The Modern Prometheus

The Modern Prometheus is a reusable Python repository template designed for mixed human + coding-agent delivery. It is intentionally opinionated about *execution hygiene*: quality gates, checklist discipline, documentation parity, evidence packaging, and carry-forward operational memory are treated as first-class implementation requirements.

If you are new to this repository, this guide explains:

- what this project is for,
- why key controls (wrapper scripts and skip manifests) exist,
- how to run work sessions correctly,
- how to collaborate effectively with coding agents such as **GPT Codex**, **GitHub Copilot**, and **Claude Code**,
- and how to adapt the template for your own multi-contributor context.

## GPT Codex Prompt Generator
If you use GPT Codex to work with this base template in a project, here is a convenient prompt generator for your sessions:
> [Create a GPT Codex Prompt On Demand](https://chatgpt.com/g/g-6a07ac8fb7888191bffd4e74b4431990-gpt-codex-dynamic-prompt-engine)

---

## Table of Contents

- [1) What this repository is and why it exists](#1-what-this-repository-is-and-why-it-exists)
- [2) Quick orientation map](#2-quick-orientation-map)
- [3) Read-first sequence (mandatory bootstrap)](#3-read-first-sequence-mandatory-bootstrap)
- [4) Environment setup and first-run commands](#4-environment-setup-and-first-run-commands)
- [5) Wrapper-first execution model](#5-wrapper-first-execution-model)
- [6) Quality gates and what they enforce](#6-quality-gates-and-what-they-enforce)
- [7) Skip manifests (`config/precommit_store/*.json`) explained](#7-skip-manifests-configprecommit_storejson-explained)
- [8) Session workflow (from task pickup to handoff)](#8-session-workflow-from-task-pickup-to-handoff)
- [9) Checklist system and task ordination](#9-checklist-system-and-task-ordination)
- [10) Agent-specific operating guidance](#10-agent-specific-operating-guidance)
  - [10.1 GPT Codex](#101-gpt-codex)
  - [10.2 GitHub Copilot (Chat/Agent)](#102-github-copilot-chatagent)
  - [10.3 Claude Code](#103-claude-code)
  - [10.4 Other coding agents](#104-other-coding-agents)
- [11) Time/date reliability and timestamp hygiene](#11-timedate-reliability-and-timestamp-hygiene)
- [12) Documentation parity and release-note discipline](#12-documentation-parity-and-release-note-discipline)
- [13) Template customization guidance (single vs multi-contributor)](#13-template-customization-guidance-single-vs-multi-contributor)
- [14) Common mistakes to avoid](#14-common-mistakes-to-avoid)
- [15) What success looks like](#15-what-success-looks-like)

---

## 1) What this repository is and why it exists

Most starter repositories give you a directory tree. The Modern Prometheus gives you an **operating model**.

This matters because modern delivery increasingly involves stateless or semi-stateless coding agents. Those agents can produce large amounts of code quickly, but without repository-local policy they also amplify process drift quickly: stale docs, skipped checks, unverifiable claims, and checklist churn.

This template addresses that with explicit, versioned controls for:

- quality and security gates,
- deterministic wrapper entry points,
- scoped remediation and evidence capture,
- checklist-based carry-forward memory,
- documentation parity,
- and reliable handoff between contributors.

Related high-level references:

- Main project overview: [`README.md`](../README.md)
- Agent charter and mandatory policy: [`AGENTS.md`](../AGENTS.md)
- Operator bootstrap sequence: [`docs/agent_bootstrap/operator_context_injection.md`](agent_bootstrap/operator_context_injection.md)

## 2) Quick orientation map

Use this map to find the right surface quickly:

- **Repository charter/policy**
  - [`AGENTS.md`](../AGENTS.md)
- **Core docs index**
  - [`docs/README.md`](README.md)
- **Wrapper scripts and usage contracts**
  - [`scripts/README.md`](../scripts/README.md)
- **Checklists**
  - Productization backlog: [`Final-Productization-Checklist.md`](../Final-Productization-Checklist.md)
  - Test-latency exceptions: [`Final-Optimization-Checklist.md`](../Final-Optimization-Checklist.md)
- **Security and boundaries**
  - [`docs/security_hygiene.md`](security_hygiene.md)
  - [`docs/source_boundary_manifest.md`](source_boundary_manifest.md)
- **Context/recipe assets for agents**
  - [`context/README.md`](../context/README.md)
  - [`context/recipes/`](../context/recipes)
  - [`context/prompts/`](../context/prompts)
- **Release-change tracking**
  - [`docs/release_notes.md`](release_notes.md)

## 3) Read-first sequence (mandatory bootstrap)

Before editing code, load context in this order:

1. [`AGENTS.md`](../AGENTS.md)
2. [`scripts/README.md`](../scripts/README.md)
3. [`Final-Productization-Checklist.md`](../Final-Productization-Checklist.md)
4. [`docs/agent_bootstrap/operator_context_injection.md`](agent_bootstrap/operator_context_injection.md)
5. [`docs/new_user_onboarding.md`](new_user_onboarding.md) (this guide)

Why this order: it prioritizes policy and wrapper semantics before feature work, reducing avoidable rework and preventing accidental policy violations.

## 4) Environment setup and first-run commands

Install development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Canonical session-close checks:

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

While iterating on specific files:

```bash
python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
python scripts/run_tests.py --scope paths --select <pytest-selector>
```

These wrapper commands are the supported control surfaces. Direct tool invocation is secondary and should not replace wrapper flows.

## 5) Wrapper-first execution model

Primary wrappers:

- Quality/lint/type/security/docstring orchestration: `python scripts/run_precommit_suite.py`
- Test orchestration: `python scripts/run_tests.py`

Why wrappers exist (instead of raw tool-by-tool calls):

- keep pre-commit skip-ledger state authoritative,
- ensure scoped resets are done correctly for touched files,
- preserve consistent failure reporting and summary artifacts,
- align contributor behavior with repository policy,
- reduce “green locally, broken in handoff” outcomes.

See command syntax and wrapper variants in [`scripts/README.md`](../scripts/README.md).

## 6) Quality gates and what they enforce

The repository enforces a strict quality stack that typically includes:

- Ruff format + lint,
- Pylint,
- Interrogate (docstrings),
- MyPy,
- Pyright,
- Deptry,
- Vulture,
- Bandit,
- and repository-specific policy checks.

This stack is intentionally redundant in places. The overlap is a feature: each tool catches different classes of defects or hygiene drift.

For quality-remediation context recipes, see:

- [`context/recipes/quality_remediation_session.md`](../context/recipes/quality_remediation_session.md)

## 7) Skip manifests (`config/precommit_store/*.json`) explained

The `config/precommit_store/` ledger exists to make strict quality gates practical in frequent, short sessions.

High-level behavior:

- each hook tracks per-file state,
- touched paths are reset to be re-evaluated,
- passing files are marked to avoid unnecessary repeated scans,
- wrapper runs maintain consistency across contributors and sessions.

Why this matters:

- **performance** for iterative workflows,
- **continuity** for stateless agents,
- **auditability** of what has been revalidated,
- **predictable remediation loops** without manual JSON editing.

Reference docs:

- [`config/precommit_store/README.md`](../config/precommit_store/README.md)
- [`docs/generated_artifact_contracts.md`](generated_artifact_contracts.md)

### Notes for template adopters (single vs multi-contributor)

If you reuse this template, think about whether current ledger metadata is sufficient for your team topology.

- In **single-contributor** projects, richer ledger metadata (for example mtime/blob/sha bookkeeping) may add JSON growth with little collaboration benefit.
- In **multi-contributor** or heavily agentized projects, adding stronger identity signals (such as content-hash or blob-based provenance) can improve correctness when contributors share branches or rebase frequently.

Tradeoff framing:

- simpler manifest schema -> smaller files, less complexity,
- richer manifest schema -> higher confidence in cross-session validity, but more storage/noise.

Use your project’s branch strategy and contributor concurrency as the deciding factor.

## 8) Session workflow (from task pickup to handoff)

Recommended execution flow:

1. Load read-first context and open checklist dependencies.
2. Pick the highest-priority entry that is actually unblocked.
3. Implement targeted changes.
4. Run scoped wrapper checks for touched files.
5. Run scoped tests for changed behavior.
6. Update docs/release notes/checklist entries affected by the change.
7. Run full closeout suites:
   - `python scripts/run_precommit_suite.py`
   - `python scripts/run_tests.py`
8. Package evidence from generated summary blocks (not partial progress logs).
9. Commit cleanly and hand off with explicit unresolved items if any.

Helpful supporting references:

- [`docs/examples/good_summary_block_usage.md`](examples/good_summary_block_usage.md)
- [`docs/examples/bad_evidence_packaging.md`](examples/bad_evidence_packaging.md)

## 9) Checklist system and task ordination

Checklists are not status journals; they are an execution queue.

- Product work, quality debt, and documentation debt should be captured as actionable entries in [`Final-Productization-Checklist.md`](../Final-Productization-Checklist.md).
- Tests exceeding latency budget should be documented in [`Final-Optimization-Checklist.md`](../Final-Optimization-Checklist.md).
- In `Final-Optimization-Checklist.md`, reserve `✅` strictly for tests with a completed code audit confirming further optimization would compromise fidelity/purpose.
- Keep over-budget tests separated into pending optimization audits versus confirmed justified exceptions; do not mix these states.

Strong checklist entries include:

- **Scope**
- **Target Files**
- **Dependencies**
- **DONE WHEN**
- **Audit step**

Reference examples:

- Good entry: [`docs/examples/good_checklist_entry.md`](examples/good_checklist_entry.md)
- Bad entry: [`docs/examples/bad_checklist_entry.md`](examples/bad_checklist_entry.md)
- Good friction entry: [`docs/examples/good_friction_entry.md`](examples/good_friction_entry.md)

## 10) Agent-specific operating guidance

### 10.1 GPT Codex

Use GPT Codex most effectively by:

- explicitly assigning a bounded checklist entry,
- requiring wrapper-first commands in the prompt,
- requiring end-of-session evidence (pre-commit/test summary blocks),
- requiring documentation parity updates when behavior changes.

Helpful assets:

- [`context/prompts/repo_audit_prompt.md`](../context/prompts/repo_audit_prompt.md)
- [`context/prompts/quality_remediation_prompt.md`](../context/prompts/quality_remediation_prompt.md)
- [`context/prompts/pr_evidence_packaging_prompt.md`](../context/prompts/pr_evidence_packaging_prompt.md)

### 10.2 GitHub Copilot (Chat/Agent)

Copilot can be effective for implementation acceleration, but maintainers should still anchor process in repository policy:

- paste or link the required wrapper commands and do not accept “raw pytest/pre-commit only” flows,
- request explicit checklist updates,
- require citations to changed files and tests in summaries,
- use repository docs as authoritative context to avoid chat-only drift.

Start context from:

- [`README.md`](../README.md)
- [`AGENTS.md`](../AGENTS.md)
- [`docs/README.md`](README.md)

### 10.3 Claude Code

Claude Code sessions generally benefit from strong up-front instruction packets. Provide:

- read order,
- exact wrapper commands,
- checklist dependency constraints,
- and explicit “do not hand-edit skip manifests” language.

If using repo-local Claude guidance, align with:

- [`CLAUDE.md`](../CLAUDE.md)

If using repo-local GitHub Copilot guidance, align with:

- [`COPILOT.md`](../COPILOT.md)

### 10.4 Other coding agents

For any agent platform:

- treat repository files as source of truth,
- enforce wrapper-first quality and testing,
- require checklist hygiene and closeable scope,
- require docs parity and release-note updates for workflow/user-facing changes.

Use [`docs/context_trigger_matrix.md`](context_trigger_matrix.md) to map workflows to required context.

## 11) Time/date reliability and timestamp hygiene

Coding-agent environments are often ephemeral (for example boot-from-image, remote container snapshots, or partially synchronized virtual workspaces). This can produce inaccurate local time perceptions in-session.

Therefore:

- do **not** trust agent-assumed date/time for provenance,
- derive dates/timestamps from trusted sources such as Git metadata,
- use explicit absolute dates in user-facing notes when ambiguity is possible.

This policy protects logs, release notes, and checklist chronology from false aging or future-dated noise.

Related policy references:

- [`AGENTS.md`](../AGENTS.md)
- [`docs/agent_bootstrap/operator_context_injection.md`](agent_bootstrap/operator_context_injection.md)

## 12) Documentation parity and release-note discipline

When behavior changes, docs should change in the same session. Typical touchpoints:

- update folder-level README files,
- update onboarding/process docs when workflow changes,
- update [`docs/release_notes.md`](release_notes.md) for user-facing/tooling behavior changes.

Supporting guidance:

- [`docs/troubleshooting.md`](troubleshooting.md)
- [`docs/template_customization_checklist.md`](template_customization_checklist.md)

## 13) Template customization guidance (single vs multi-contributor)

When adapting this template:

1. Define contributor model early (single maintainer, team, agent-heavy, or hybrid).
2. Decide how strict ledger metadata should be for your concurrency profile.
3. Keep wrapper entry points intact unless you have a documented replacement with equivalent guarantees.
4. Customize prompts/recipes under `context/` for your domain workflows.
5. Keep checklist standards strict to avoid long-term task churn.

This keeps the template’s main benefit intact: reproducible execution quality across contributors with minimal hidden context.

## 14) Common mistakes to avoid

- Running bare `pytest` as the standard surface instead of wrapper flows.
- Running direct hook aliases instead of `scripts/run_precommit_suite.py`.
- Hand-editing `config/precommit_store/*.json`.
- Treating checklist files as journals rather than closeable work queues.
- Ignoring dependency order in checklist execution.
- Letting documentation or release notes drift from implementation reality.
- Committing local evidence/cache outputs that should remain untracked.

## 15) What success looks like

A successful onboarding outcome means a new contributor can read this guide and then:

- navigate the repository confidently,
- run the correct wrapper commands without guesswork,
- understand why strict gates and skip manifests exist,
- collaborate with coding agents without process collapse,
- and leave each session easier for the next contributor to continue.

That is the core promise of The Modern Prometheus: not just scaffolding code, but scaffolding reliable execution.
