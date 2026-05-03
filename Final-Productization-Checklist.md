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

- [ ] **Documentation audit: AGENTS.md**
  - Scope: Validate policy language matches current wrapper commands and checklist governance behavior.
  - Target Files: `AGENTS.md`
  - Dependencies: None
  - DONE WHEN: Commands, policy directives, and referenced file paths remain accurate against implementation.
- [ ] **Documentation audit: README.md**
  - Scope: Verify quickstart and policy claims match current scripts and enforcement behavior.
  - Target Files: `README.md`, `scripts/run_tests.py`, `tests/conftest.py`
  - Dependencies: Documentation audit: AGENTS.md
  - DONE WHEN: README command guidance and enforcement language are implementation-true.
- [ ] **Documentation audit: CONTRIBUTING.md**
  - Scope: Audit contributor workflow for wrapper-first parity and evidence capture.
  - Target Files: `CONTRIBUTING.md`, `scripts/README.md`
  - Dependencies: Documentation audit: README.md
  - DONE WHEN: Onboarding and remediation instructions are complete and non-duplicative.
- [ ] **Documentation audit: docs/release_notes.md**
  - Scope: Ensure release-note entries reflect current behavior changes and omit stale claims.
  - Target Files: `docs/release_notes.md`
  - Dependencies: None
  - DONE WHEN: Release notes capture all user-facing/tooling-facing changes from latest merged work.
- [ ] **Documentation audit: docs/README.md**
  - Scope: Validate documentation index links and audience segmentation.
  - Target Files: `docs/README.md`
  - Dependencies: Documentation audit: README.md
  - DONE WHEN: Every listed link resolves and index avoids duplicating canonical command instructions.
- [ ] **Documentation audit: docs/agent_bootstrap/README.md**
  - Scope: Validate bootstrap task list against script capabilities and artifact policy.
  - Target Files: `docs/agent_bootstrap/README.md`, `scripts/aggregate_project_docstrings.py`, `scripts/audit_docstrings.py`
  - Dependencies: Documentation audit: docs/README.md
  - DONE WHEN: Source files, output paths, and acceptance checks are executable and accurate.
- [ ] **Documentation audit: scripts/README.md**
  - Scope: Confirm script inventory and command examples match current automation behavior.
  - Target Files: `scripts/README.md`, `scripts/run_precommit_suite.py`, `scripts/run_tests.py`
  - Dependencies: None
  - DONE WHEN: Every listed utility exists and wrapper guidance reflects enforced behavior.
- [ ] **Documentation audit: scripts/test_profiles/README.md**
  - Scope: Verify profile format guidance aligns with parser behavior in test wrapper.
  - Target Files: `scripts/test_profiles/README.md`, `scripts/run_tests.py`
  - Dependencies: Documentation audit: scripts/README.md
  - DONE WHEN: Profile syntax rules match runtime parsing and error handling.
- [ ] **Documentation audit: tests/README.md**
  - Scope: Validate test inventory and execution guidance against current tests and wrappers.
  - Target Files: `tests/README.md`, `tests/`
  - Dependencies: Documentation audit: scripts/README.md
  - DONE WHEN: File list and command guidance reflect actual test modules and policy hooks.
- [ ] **Documentation audit: config/README.md**
  - Scope: Verify config folder descriptions and ledger behavior remain correct.
  - Target Files: `config/README.md`, `config/precommit_store/README.md`, `scripts/precommit_filter.py`
  - Dependencies: None
  - DONE WHEN: Config docs accurately describe manifests, caches, and maintenance expectations.
- [ ] **Documentation audit: config/precommit_store/README.md**
  - Scope: Audit skip-ledger and pylint failure cache explanations for accuracy.
  - Target Files: `config/precommit_store/README.md`, `config/precommit_store/pylint_failures.json`
  - Dependencies: Documentation audit: config/README.md
  - DONE WHEN: Documentation matches live JSON ledger roles and update workflow.
- [ ] **Documentation audit: Final-Productization-Checklist.md**
  - Scope: Ensure checklist wording remains actionable and policy-compliant.
  - Target Files: `Final-Productization-Checklist.md`
  - Dependencies: None
  - DONE WHEN: Open items are explicit, scoped, and free of session-journal phrasing.
- [ ] **Documentation audit: Final-Optimization-Checklist.md**
  - Scope: Confirm optimization ledger entries remain actionable and latency-policy aligned.
  - Target Files: `Final-Optimization-Checklist.md`
  - Dependencies: None
  - DONE WHEN: Every open entry has scope, rationale, and measurable completion conditions.
- [ ] **Documentation audit: CODE_OF_CONDUCT.md**
  - Scope: Verify policy references and contact/conduct language remain current.
  - Target Files: `CODE_OF_CONDUCT.md`
  - Dependencies: None
  - DONE WHEN: Conduct guidance is internally consistent and free of stale links.
- [ ] **Documentation audit: context/README.md**
  - Scope: Validate generated-artifact lifecycle guidance and bootstrap command parity.
  - Target Files: `context/README.md`, `scripts/aggregate_project_docstrings.py`
  - Dependencies: Documentation audit: docs/agent_bootstrap/README.md
  - DONE WHEN: Lifecycle policy and command examples remain accurate.

---

## Only Proceed Below This Checklist Area If No Entries Above Exist
> Entries and instructions below this section are for iterative improvement as needed by Agents with no pending tasks.

---
