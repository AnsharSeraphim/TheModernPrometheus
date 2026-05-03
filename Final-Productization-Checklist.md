# Final Productization Checklist

**Use this file to track unresolved quality, tooling, or release-readiness work that should be carried into a later session.**

# **MANDATORY CHECKLIST POLICY**
**FOLLOW THE BELOW DIRECTIVES WHEN ADDRESSING *ANY* ENTRY BELOW**
- Record only open work. When a task is finished, **delete it** so only unresolved entries remain.
- Rewrite partially completed tasks as explicit, actionable “remaining work” items.
- Run remediation loops through `python scripts/run_precommit_suite.py` (never direct hook calls).
- Source of truth for current pylint diagnostics is `config/precommit_store/pylint_failures.json`.
- Each entry should represent a specific action / goal / gap to address in the scope of a session. 
- Every entry should specify the remaining work to be done for that specific task, so that when the work is complete, the entry is addressed and iterative sessions will not continually work on the same entries, annotating progress.


**Entries in `Final-Productization-Checklist.md` can be responsible for task churn, specifically entries that contain the words:**
```
all
continue
every
each
remaining
across
etc
```
Poor wording in these entries can keep each checklist entry from being specific, actionable, and granular in scope, and encourage iterative churn, annotations of incremental progress, and multiple executions inside of a single entry.

## Permanent Checklist Entry - *NEVER CLOSE THIS*
- [ ] For checklist entries that are worded in these nonspecific terms, above, *unless the checklist entry is a scoped audit*, perform the relevant audit so the entry can be expanded with EXACT SCOPE AND STEPS, AFFECTED FILES, AND `DONE WHEN` CRITERIA, each having their OWN entry. You may only proceed to other tasks when this condition is fulfilled. If all entries in this checklist currently adhere to this policy above the `Only Proceed To This Task If No Entries Above Exist` line, then proceed to address entries, as directed.

> CHECK FOR VIOLATIONS OF THE ABOVE ENTRY BEFORE ADVANCING TO ANY OTHER CHECKLIST ENTRIES IN OTHER SECTIONS.

---

## Outstanding Tasks

- [ ] Create `.github/dependabot.yml` with grouped update strategy for ecosystem-specific dependency batching (pip + GitHub Actions), explicit schedules, and reviewer labels so template consumers inherit sane update noise control; DONE WHEN config validates and grouping rules are documented in README/docs.
- [ ] Implement wrapper-level enforcement for naked `pytest` invocations (parity with manual hook warning strategy) so direct pytest execution exits with a redirect to `python scripts/run_tests.py`; DONE WHEN enforcement path is covered by automated tests and documented in `scripts/README.md` + root README.
- [ ] Add `context/README.md` and a generated-schemas note for docstring catalog outputs so agents understand expected JSON assets, lifecycle (generated/not committed policy), and bootstrap usage; DONE WHEN the folder exists with lifecycle documentation and references to `scripts/aggregate_project_docstrings.py`.
- [ ] Create `docs/agent_bootstrap/README.md` plus scoped task list describing how to build skills markdown files, prompt recipes, and task-recipe JSON artifacts from existing repository scripts/workflows; DONE WHEN entries enumerate source files, output locations, acceptance checks, and ownership expectations.
- [ ] Add granular checklist sub-entries under `Documentation Inventory` for every Markdown file currently tracked in the repository (explicit file path per entry) with concrete `DONE WHEN` criteria so stateless agents can close each audit atomically.
- [ ] Expand `CONTRIBUTING.md` to include a "Template onboarding" path that explains repository purpose, wrapper-first commands, evidence artifacts, and checklist maintenance responsibilities for first-time users; DONE WHEN command examples and failure/remediation flow are documented.
- [ ] Add a documentation index page in `docs/` linking operational docs, folder READMEs, and checklist files with intended audiences (maintainers vs template consumers vs agents); DONE WHEN index links resolve and avoids duplicate guidance already present in root README.
- [ ] Evaluate and document `scripts/aggregate_project_docstrings.py` operational modes (full scan, exclusions, output path conventions, and downstream consumption) in `scripts/README.md`; DONE WHEN examples include at least one command that generates context JSON for agent bootstrap.
- [ ] Audit pyproject tooling constraints for template reproducibility notes (Python pinning rationale, dependency caps, strict checker posture) and capture this rationale in docs; DONE WHEN rationale appears in documentation with links to `pyproject.toml` sections.
    
### Checklist Entry Template (Use for every new actionable item)
- Required fields for each entry:
  - `Scope:` exact problem boundary.
  - `Target Files:` explicit relative paths to edit or audit.
  - `Dependencies:` prerequisite checklist items or `None`.
  - `DONE WHEN:` objective completion condition that can be verified.

Example format:
- [ ] **Task title**
  - Scope: <one bounded task>
  - Target Files: `<path1>`, `<path2>`
  - Dependencies: <entry title or `None`>
  - DONE WHEN: <verifiable outcome>

---

## Only Proceed To This Task If No Entries Above Exist
- [ ] Populate the .md list for the `Create a checklist entry for every .md file in the repository HERE.` entry, below, in the `Documentation Inventory` section, for the `Documentation and Coding Audit` checklist process.

### Documentation and Coding Audit
> For All Files Listed Below, Perform a Coding Audit for any mentioned files and compare implementation to Documentation Copy as per the rubric below. 

#### Execution quality examples for stateless agents
- ☑️ **Minimal unacceptable execution (do not do):** "Skim headings only, run a generic spell-check, update one sentence, and mark audit complete without verifying commands, links, ToC, implementation parity, or cross-document consistency."
- ✅ **Proper execution baseline (required):** "For each target file: verify ToC/anchor integrity, run command and path parity checks against implementation, confirm claims via code/tests, evaluate redundancy/cross-linking, expand mechanism explanations where shallow, and either apply fixes or create granular follow-up checklist entries with reproduction steps."
- ✅ **Coding Audit:** "Where a programmatic file is mentioned, investigate to ensure implmentation and function. If you see areas for improvement or needed fixes, create appropriately actionable granular checklist tasks above the document audit, along with an embedded follow-up to correct documentation with your fix or improvement."

#### Documentation Parity Rubric (apply per file)
- ✅ **Coding Audit:** Where a programmatic file is mentioned, investigate to ensure implmentation and function. If you see areas for improvement or needed fixes, create appropriately actionable granular checklist tasks above the document audit, along with an embedded follow-up to correct documentation with your fix or improvement.
- ✅ **Implementation truthfulness:** If a document is design-only or speculative, rewrite it to describe what is actually implemented now (or clearly move speculation into roadmap language).
- ✅ **Release-note handling:** If a document is iterative release-facing history (for example `docs/releases/CHANGELOG.md`) while the project is still unreleased, clear unreleased-facing content after verifying user-facing docs already capture relevant shipped behavior.
- ✅ **Operational usefulness:** Confirm the document enables a user/agent to execute or validate behavior, not just read a high-level overview.
- ✅ **Mechanism explanation depth:** Expand text to explain what mechanisms do, when to use them, inputs/outputs, and failure modes; not only that components exist.
- ✅ **Redundancy folding:** Merge or cross-link redundant documents and remove stale duplication.
- ✅ **README coverage by folder:** Verify every active top-level and major subfolder has an accurate `README.md`; add/update missing or inaccurate folder READMEs.
- ✅ **Navigation integrity:** Validate table of contents structure, local anchors, relative links, and cross-document references.
- ✅ **Command parity:** Verify documented commands match current CLI/script entry points and wrapper-first policy.
- ✅ **Evidence parity:** Validate claims against implementation paths/tests and remove stale or unverifiable assertions.
- ✅ **Agent continuity:** Ensure next-session contributors can act without hidden context (explicit prerequisites, paths, expected outputs, and remediation instructions).
- ✅ **UTF-8 and style policy:** Ensure text is UTF-8, avoids hidden characters/unintended escapes, and follows repository language/style constraints.

##### Documentation Inventory
> Create entries for the `Documentation Audit` here. Don't forget to follow the rubric above. If you discover issues, remediate them, or create new actionable granular tasks under `Outstanding Tasks / Gaps (Open Work Only)` if you cannot remediate in-session for some reason.

- [ ] Create a checklist entry for every .md file in the repository HERE.

---

## Only Proceed Below This Checklist Area If No Entries Above Exist
> Entries and instructions below this section are for iterative improvement as needed by Agents with no pending tasks.

---
