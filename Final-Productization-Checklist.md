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
> Use the Checklist Entry Template to create new tasks.
- [ ] For checklist entries that are worded in these nonspecific terms, above, *unless the checklist entry is a scoped audit*, perform the relevant audit so the entry can be expanded with EXACT SCOPE AND STEPS, AFFECTED FILES, AND `DONE WHEN` CRITERIA, each having their OWN entry. You may only proceed to other tasks when this condition is fulfilled. If all entries in this checklist currently adhere to this policy above the `Only Proceed To This Task If No Entries Above Exist` line, then proceed to address entries, as directed.

### Checklist Entry Template (Use for every new actionable item)
```
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
```


> CHECK FOR VIOLATIONS OF THE ABOVE ENTRY BEFORE ADVANCING TO ANY OTHER CHECKLIST ENTRIES IN OTHER SECTIONS.

---

## Outstanding Tasks


- [ ] **Create template-customization checklist for new repos**
  - Scope: Add a concrete post-clone checklist so template consumers can turn the scaffold into a project without leaving placeholder metadata, stale policy references, or accidental template residue.
  - Target Files: `docs/template_customization_checklist.md`, `README.md`, `docs/new_user_onboarding.md`, `docs/README.md`
  - Dependencies: `Create runtime-target support matrix`, `Create task-to-context trigger matrix`
  - DONE WHEN: The checklist covers project rename/metadata updates, dependency review, reviewer placeholder replacement, ignore-policy verification, initial checklist seeding, runtime-support decisions, and docs index updates; root/docs onboarding paths link to it.
  - Audit step: Inspect the checklist and verify it names concrete repo placeholders or policy decisions a new consumer must revisit before first real work.

- [ ] **Add GitHub Actions workflow for wrapper-driven validation**
  - Scope: Add remote validation so wrapper/test policy is enforced in GitHub and does not depend only on local contributor discipline.
  - Target Files: `.github/workflows/quality-gates.yml`, `README.md`, `CONTRIBUTING.md`, `docs/runtime_target_support_matrix.md`
  - Dependencies: `Add root ignore rules for local evidence and Python-generated artifacts`
  - DONE WHEN: A GitHub Actions workflow exists for pull requests and relevant branch pushes; it installs the declared Python toolchain; it runs `python scripts/run_precommit_suite.py` and `python scripts/run_tests.py`; repo docs mention the workflow where validation expectations are described.
  - Audit step: Inspect `.github/workflows/quality-gates.yml` and verify the workflow invokes the wrapper scripts instead of raw `pytest` or ad hoc hook commands.

- [ ] **Add GitHub PR template with evidence sections**
  - Scope: Create a PR template that makes the repo’s evidence-packaging requirements easy to follow and hard to omit.
  - Target Files: `.github/PULL_REQUEST_TEMPLATE.md`, `CONTRIBUTING.md`, `docs/README.md`
  - Dependencies: `Add GitHub Actions workflow for wrapper-driven validation`
  - DONE WHEN: The PR template includes checklist task worked, scoped commands run, pasted summary-block sections, unresolved issues, and linked follow-up checklist entries; contributing/docs pages point to the template expectations rather than prose alone.
  - Audit step: Inspect `.github/PULL_REQUEST_TEMPLATE.md` and confirm the required sections map to the evidence rules already described in `CONTRIBUTING.md`.

- [ ] **Document generated-artifact contracts and source boundaries**
  - Scope: Add explicit contracts for machine-consumable/generated artifacts and distinguish hand-authored source assets from generated local evidence, caches, and committed ledgers.
  - Target Files: `docs/generated_artifact_contracts.md`, `docs/source_boundary_manifest.md`, `README.md`, `scripts/README.md`, `docs/agent_bootstrap/README.md`, `config/README.md`
  - Dependencies: `Add root ignore rules for local evidence and Python-generated artifacts`
  - DONE WHEN: The contract doc names producers, consumers, commit policy, schema notes, and stability expectations for `context/project_docstrings_catalog.json`, `build/automation_contract/` summary blocks, `build/automation_contract/docstring_inventory.md`, and `config/precommit_store/*.json`; the source-boundary manifest distinguishes hand-authored source, generated local evidence, generated committed ledgers, and caches.
  - Audit step: Inspect the contract/source-boundary docs and confirm that every generated artifact family already mentioned in repo docs appears with an explicit commit/use boundary.

- [ ] **Create exemplar and anti-exemplar package for agent calibration**
  - Scope: Add concrete examples of good and bad outputs so agent contributors can see what high-fidelity checklist entries, evidence packaging, and friction reports look like without inferring the target shape from prose alone.
  - Target Files: `docs/examples/README.md`, `docs/examples/good_checklist_entry.md`, `docs/examples/bad_checklist_entry.md`, `docs/examples/good_summary_block_usage.md`, `docs/examples/bad_evidence_packaging.md`, `docs/examples/good_friction_entry.md`, `docs/generated_artifact_contracts.md`
  - Dependencies: `Document generated-artifact contracts and source boundaries`, `Create reusable context prompt library for stateless repo workflows`
  - DONE WHEN: The examples directory exists; the listed positive and negative examples are present; the README explains what invariant or failure mode each file demonstrates; linked docs can point to these examples when describing expected output quality.
  - Audit step: Inspect `docs/examples/README.md` and verify that every example has a clearly stated “why this is good/bad” note instead of leaving the calibration burden implicit.

- [ ] **Add machine-readable task-recipe schema with starter assets**
  - Scope: Create a machine-readable task-recipe format so future routers or advanced stateless agents can consume high-frequency workflows without parsing prose alone.
  - Target Files: `context/task_recipes/README.md`, `context/task_recipes/schema.json`, `context/task_recipes/quality_remediation.json`, `context/task_recipes/checklist_audit.json`, `docs/task_recipe_schema.md`, `docs/agent_bootstrap/README.md`
  - Dependencies: `Create task-to-context trigger matrix`, `Create reusable context prompt library for stateless repo workflows`
  - DONE WHEN: The schema file exists; the two starter task-recipe JSON assets validate against it; `docs/task_recipe_schema.md` explains required fields such as task ID, scope, target files, dependencies, commands, validations, and `done_when`; bootstrap docs link to the schema.
  - Audit step: Inspect `context/task_recipes/` and confirm the starter JSON assets use the documented keys and reference canonical wrapper commands.

- [ ] **Add troubleshooting playbook for wrapper and tooling failures**
  - Scope: Consolidate common failure signatures and remediation paths so agents and maintainers do not have to reconstruct wrapper recovery logic from scattered notes.
  - Target Files: `docs/troubleshooting.md`, `README.md`, `CONTRIBUTING.md`, `docs/README.md`, `scripts/README.md`
  - Dependencies: `Create reusable context prompt library for stateless repo workflows`
  - DONE WHEN: The playbook covers at least missing dependencies, wrapper invocation mistakes, stale-ledger confusion, interrogate/docstring remediation, test-scope selection mistakes, and unresolved-failure escalation into the checklist; docs index/root pages link to it where relevant.
  - Audit step: Inspect `docs/troubleshooting.md` and verify that the covered failure signatures map to repo behavior already described in `AGENTS.md`, `scripts/README.md`, or recipe assets.

- [ ] **Add ownership map / CODEOWNERS coverage for operational assets**
  - Scope: Define who maintains the repo’s operationally sensitive docs, scripts, tests, and context assets so future drift can be detected and review routing can be added where useful.
  - Target Files: `.github/CODEOWNERS`, `docs/ownership_map.md`, `docs/README.md`
  - Dependencies: `Create runtime-target support matrix`
  - DONE WHEN: The repo contains either a meaningful `.github/CODEOWNERS` file plus a human-readable ownership map or an ownership map that explicitly documents why CODEOWNERS is intentionally deferred; docs index links to the ownership map.
  - Audit step: Inspect the ownership assets and confirm they name maintainers or maintainer roles for scripts, tests, docs, context assets, and GitHub workflow files.

- [ ] **Add security hygiene note for template consumers**
  - Scope: Add a lightweight security/data-boundary guide so the template makes explicit what must not be committed, what local evidence should stay local, and how secret-bearing files should be treated.
  - Target Files: `docs/security_hygiene.md`, `README.md`, `CONTRIBUTING.md`, `docs/new_user_onboarding.md`
  - Dependencies: `Add root ignore rules for local evidence and Python-generated artifacts`
  - DONE WHEN: The security note exists; it covers secrets, env files, generated evidence, binaries, deny-path guidance, and basic local-vs-source boundaries; root/onboarding/contributing docs link to it where contributors are first taught repo hygiene.
  - Audit step: Inspect `docs/security_hygiene.md` and confirm it distinguishes policy for secrets and local evidence from the repo’s existing no-binary and wrapper-evidence rules.
  
---

## Only Proceed To This Task If No Entries Above Exist
> **INSTRUCTIONS:** AGENTS MAY NOT DELETE THE BELOW ENTRY OR THE DOCUMENTATION RUBRIC. ONLY THE USER MAY DELETE THIS SECTION. THIS TASK REMAINS OPEN UNTIL PROJECT COMPLETION.
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

- **PLACEHOLDER FOR CHECKLIST ENTRIES FOR DOCUMENTATION AUDIT.** This line will be replaced with entries for all your project documentation when there are no other entries in the checklist. This process will automatically direct Coding-Agents to audit your documentation against your implementation, along with your code, remediating issues as they encounter them or creating entries to correct issues they cannot address in the same session.

---

## Coding-Agent-Surfaced Execution Friction / What Will Make Agents Able To Navigate Your Project More Easily
> **INSTRUCTIONS:** Surface Coding-Agent Execution Friction Entries Here for User Approval. User will migrate entries to higher in the checklist if your suggestions are approved.

**USER INSTRUCTIONS:** `AGENTS.md` currently authorizes Coding-Agents to create entries in this section. Keep that authorization in sync if policy changes.

Example addition to `AGENTS.md`:
```
Agents are expected to create actionable granular scoped checklist entries that follow the checklist template in `Final-Productization-Checklist.md` in the `Coding-Agent-Surfaced Execution Friction` section of the checklist when they encounter problems/friction specific to Agent navigation, script invocation syntax, needed context without investigation, needed prompt recipes, task recipes, workflow diagrams, bootstrapping for context, or other assets that will make project use smoother for Coding Agents. The user agrees to review all checklist entries in that section and move them to actionable tasks, if approved.
```

- Before creating a new friction entry, run a duplicate check against this section and `Outstanding Tasks` to avoid redundant backlog items.
- Create suggestion checklist entries here, if directed by `AGENTS.md`, using the checklist template fields (`Scope`, `Target Files`, `Dependencies`, `DONE WHEN`, and `Audit step`).

---
