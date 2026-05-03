# New User Onboarding: The Modern Prometheus

The Modern Prometheus is a reusable GitHub repository template for creating Python projects that are ready for both human contributors and coding agents from the first commit. It is not just a folder scaffold. It is a repository-governance system: a project starter that brings execution discipline, quality gates, documentation expectations, agent operating rules, and carry-forward task memory into the repository itself.

Most starter repositories give you files and then leave you to discover the missing process later, usually at the exact moment something breaks and everyone begins practicing folk archaeology in Slack threads. This template takes the opposite approach. It encodes the operating model directly into the repository so contributors and stateless coding agents can find the rules, run the correct commands, preserve evidence, and hand off work cleanly.

## Who this is for

Use this template when you want a new Python project to begin with serious operational discipline rather than improvised habits.

It is especially useful for:

- agent-driven development workflows using tools such as GPT Codex, Claude Code, or other coding agents;
- research repositories that need reproducible checks, documentation parity, and audit trails;
- internal tools that may be modified by many short-lived contributor sessions;
- compliance-sensitive prototypes where quality, security, and documentation cannot be treated as decorative confetti;
- documentation-heavy systems where future maintainers need clear context without interviewing the original author;
- projects where checklists, release notes, docstrings, and automation artifacts matter as much as raw feature code.

This template does not impose a product architecture. It gives a project an execution skeleton: the rules for how work should be modified, checked, documented, reviewed, and handed off.

## The core idea

Modern repositories are increasingly operated by stateless or semi-stateless coding agents. These agents do not automatically know the maintainer's preferences, hidden scripts, quality expectations, release-note habits, or test conventions. If the repository does not make those rules explicit, the agent will infer, improvise, bypass, or minimize. Humanity, having learned nothing from every process failure ever, will then pretend this was surprising.

The Modern Prometheus makes the repository self-orienting by including:

- a root `AGENTS.md` charter that defines coding-agent operating rules;
- canonical wrapper scripts for quality and test execution;
- strict lint, type, security, dependency, docstring, and encoding gates;
- checklist files that preserve open work as scoped, closeable tasks;
- skip-ledger state for efficient quality checks across sessions;
- documentation expectations for humans and agents;
- docstring aggregation tools for fast implementation audit;
- release-note and dependency-maintenance practices;
- repository maps and folder-level orientation conventions.

The result is a template where project law is not trapped in one person's head. It lives in the repo.

## What to read first

Start with these files in this order:

1. `README.md` gives the main project summary, repository map, setup commands, and reusable coding-agent prompt pattern.
2. `AGENTS.md` defines the operating rules for coding agents and contributors working in the repository.
3. `Final-Productization-Checklist.md` tracks unresolved quality, tooling, documentation, or release-readiness work.
4. `Final-Optimization-Checklist.md`, when present, tracks tests that exceed the latency budget and explains why they are temporarily accepted.
5. `docs/release_notes.md`, when present, records user-facing or workflow-relevant changes.

A new contributor should not begin by randomly running tools or editing files. Read the operating law first. It is cheaper than fixing the preventable mess later, allegedly.

## First setup

Create and activate a virtual environment, then install the development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

After setup, the canonical closing checks are:

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

Those wrapper commands matter. Do not replace them with naked `pre-commit`, direct hook aliases, or bare `pytest` unless the repository documentation explicitly authorizes that path.

## The wrapper-first rule

The most important operating rule in this repository is wrapper-first execution.

Quality checks must run through:

```bash
python scripts/run_precommit_suite.py
```

Tests must run through:

```bash
python scripts/run_tests.py
```

These wrappers are the repository's control surface. Individual tools such as Ruff, Pylint, MyPy, Pyright, Bandit, Vulture, Deptry, Interrogate, and pytest are implementation details underneath that surface.

Direct tool calls are discouraged because they can bypass repository-specific behavior, including:

- scoped file handling;
- skip-ledger refresh logic;
- cached Pylint diagnostics;
- summary artifact generation;
- policy-aware test invocation;
- checklist validation;
- wrapper-level enforcement against stale or incomplete evidence.

If a tool fails, remediate the issue. Do not weaken settings, hand-edit skip ledgers, silence checks, or route around the wrapper. The point of the suite is to surface problems while they are still cheap enough to fix.

## Quality gates included in the template

The scaffold is configured for strict Python quality expectations. Depending on the current project state, the quality suite may coordinate:

- Ruff formatting;
- Ruff linting;
- Pylint;
- Interrogate docstring coverage;
- MyPy;
- Pyright;
- Deptry;
- Vulture;
- Bandit;
- merge-conflict checks;
- checklist-structure validation;
- UTF-8 and Unicode-escape validation.

The default posture treats lint, type safety, docstring coverage, dependency hygiene, security scanning, and text-encoding health as ordinary project hygiene. They are not final-week polish. They are part of how the repository stays usable by future humans and agents.

## Skip ledgers: why quality checks can stay usable

Strict tooling can become expensive if every short session must recheck an entire repository. The Modern Prometheus addresses that with per-hook JSON skip ledgers under:

```text
config/precommit_store/
```

Each major hook can track whether a file has already passed. When a file is touched, the wrapper can reset its skip flag and revalidate it. When that file passes, the ledger records the passing state so later sessions do not have to repeat unnecessary work.

This design is especially useful for coding-agent workflows because agents often operate in short, iterative sessions. The ledger lets the project preserve audit state without pretending that every agent should repeatedly scan everything forever, which is a fine way to turn software quality into performance art.

Important rules:

- use the wrapper to refresh ledgers;
- do not hand-edit `config/precommit_store/*.json`;
- commit relevant updated JSON state when the wrapper changes it;
- treat `config/precommit_store/pylint_failures.json` as the source of truth for current cached Pylint diagnostics;
- run a full suite before session close unless the repository gives a narrower approved closure rule.

## Checklist hygiene

`Final-Productization-Checklist.md` is carry-forward memory for open work. It is not a journal, not a vibes board, and not a graveyard for vague intentions.

Good checklist entries are:

- scoped;
- actionable;
- tied to explicit target files;
- ordered around dependencies;
- verifiable through clear `DONE WHEN` criteria;
- removed when complete;
- rewritten when only part of the work remains.

Bad checklist entries use vague terms such as "all," "continue," "every," "each," "remaining," "across," or "etc." in ways that make the task impossible to close cleanly. These entries create task churn because every future agent can "make progress" without actually finishing the work. Apparently ambiguity can be renewable energy if you feed it to enough agents.

When creating new checklist work, use the required template:

```markdown
- [ ] **Task title**
  - Scope: <one bounded task>
  - Target Files: `<path1>`, `<path2>`
  - Dependencies: <entry title or `None`>
  - DONE WHEN: <verifiable outcome>
```

If an issue is discovered during implementation and cannot be completed in the same session, create a new scoped checklist entry. If the issue is completed, do not leave a fossilized note pretending it is still open.

## Documentation parity

Documentation in this template is operational. It should help a human or coding agent execute, validate, audit, or continue work without hidden context.

Good documentation should answer:

- What does this file, folder, script, or workflow do?
- When should someone use it?
- What command should they run?
- What inputs and outputs should they expect?
- What failure modes matter?
- What implementation paths or tests support the claim?
- What should be updated when behavior changes?

Folder-level `README.md` files should stay current. Release notes should be updated when tooling behavior, quality workflow, or user-facing repository operation changes. Documentation should not claim future behavior as implemented fact; speculative plans belong in roadmap language or checklist entries.

## Docstring automation

The template includes docstring tooling so a project can expose its implementation claims in a compact, reviewable format.

The aggregation script:

```bash
python scripts/aggregate_project_docstrings.py
```

exports a monolithic JSON catalog of module, class, and function docstrings. This is useful for LLM context bootstrapping, reviewer orientation, documentation generation, and conceptual audits.

The audit script:

```bash
python scripts/audit_docstrings.py
```

can produce a human-readable Markdown inventory of discovered docstrings. Reviewers can use that inventory to compare what the implementation claims against what the surrounding documentation says.

The practical point is simple: docstrings become a project-understanding substrate, not just polite decoration glued above functions because a linter demanded tribute.

## How a normal work session should flow

A disciplined session usually follows this shape:

1. Read `AGENTS.md` and the relevant checklist entries.
2. Identify the highest-priority open task that can be completed without violating dependency order.
3. Edit the target files.
4. Run the targeted wrapper command for touched files when appropriate, for example:

   ```bash
   python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>
   ```

5. Run relevant tests through the test wrapper, for example:

   ```bash
   python scripts/run_tests.py --scope changed
   ```

6. Update docs, release notes, checklists, or manifests affected by the change.
7. Run the full closing suites:

   ```bash
   python scripts/run_precommit_suite.py
   python scripts/run_tests.py
   ```

8. Capture the final result blocks from the automation summaries, not partial progress output.
9. Delete completed checklist entries or rewrite partially completed entries into explicit remaining work.

That flow gives the next contributor or coding agent a clean continuation point.

## Guidance for coding agents

Coding agents should treat the repository as the source of truth. Do not infer a different process because it is shorter.

A coding agent working in this template should:

- read `AGENTS.md` before acting;
- respect checklist ordination and dependencies;
- use wrapper commands rather than direct tool calls;
- wait for wrapper completion instead of interrupting based on progress percentages;
- fix surfaced failures instead of weakening gates;
- update release notes when user-facing or workflow-facing behavior changes;
- preserve generated JSON or manifest changes when the repository expects them;
- avoid editing automation evidence directories that are meant to remain untracked;
- leave the checklist cleaner than it found it.

The goal is not to make agents obedient in some theatrical sense. The goal is to make agent work reproducible, auditable, and less likely to collapse into "I changed something and the terminal looked green for three seconds."

## Guidance for human maintainers

Human maintainers should use this template by making the desired operating model explicit before feature work begins.

At minimum, customize:

- project name and description in `README.md`;
- package metadata in `pyproject.toml`;
- first actionable tasks in `Final-Productization-Checklist.md`;
- release-note conventions in `docs/release_notes.md`;
- any folder-level `README.md` files that need project-specific orientation;
- agent instructions in `AGENTS.md` if the project has special constraints.

For agent-driven work, seed the checklist with clear project-building tasks. Then direct coding agents to address those entries in order while following `AGENTS.md`. The reusable metaprompt in `README.md` is designed for that iterative workflow.

## Common mistakes to avoid

Do not use bare `pytest` as the normal test surface. Use `python scripts/run_tests.py`.

Do not call individual hooks directly as the normal quality surface. Use `python scripts/run_precommit_suite.py`.

Do not interrupt the pre-commit wrapper because a progress percentage looks stuck. The percentage is informational and may be stale.

Do not hand-edit skip ledgers to hide failures. Use the wrapper and fix the underlying issue.

Do not leave vague checklist entries for future agents to reinterpret. Make the scope explicit or split the work into smaller entries.

Do not update optimization checklists for unchanged tests just to look productive. That is not execution; it is administrative fog.

Do not let documentation drift away from implementation. If behavior changes, update the relevant docs and release notes.

Do not commit binary assets unless the repository specifically allows them. Share screenshots, videos, and archives separately when needed.

## What makes this strategically useful

The value of The Modern Prometheus is the operating pattern it makes reusable:

- encode project law in `AGENTS.md`;
- route execution through wrappers;
- preserve quality state in ledgers;
- maintain closeable checklists;
- enforce documentation parity;
- export docstring context for LLM ingestion;
- capture release-facing changes;
- make every session easier for the next operator.

This turns a GitHub template into a cloneable repository-control system for serious coding-agent-compatible projects. The repository does not merely tell agents what to build. It teaches them how not to damage the project while building it, which is tragically necessary and therefore useful.
