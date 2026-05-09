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

- [ ] **Make CI wrapper validation run in full-check mode instead of skip-ledger no-op mode**
  - Scope: Update remote validation so `.github/workflows/quality-gates.yml` does not rely on committed skip-ledger state for repository-wide checks. The current clean-checkout execution path can report success while every pre-commit hook is skipped because tracked files are already marked passed in `config/precommit_store/*.json`.
  - Target Files: `.github/workflows/quality-gates.yml`, `README.md`, `CONTRIBUTING.md`, `docs/runtime_target_support_matrix.md`, `docs/troubleshooting.md`
  - Dependencies: `None`
  - DONE WHEN: GitHub Actions runs the pre-commit wrapper in an explicit full-validation mode (`--reset-baseline`, `--filter-mode full`, or an equivalent repo-sanctioned mechanism) and the documented remote-validation contract matches actual behavior; a clean-checkout run no longer produces an all-`SKIPPED` hook summary for repository-wide validation.
  - Audit step: Run the exact CI command sequence from a clean checkout and confirm the pre-commit summary shows actual hook execution instead of `All tracked files already passed ...; skipping.` for every hook.
  - Ensure this does *not* affect other types of operations that *do* want to use the Skip Filter by default to not rescan currently passing untouched files.

- [ ] **Commit or explicitly downgrade the missing docstring-catalog bootstrap asset**
  - Scope: Resolve the mismatch between documentation/contracts that treat `context/project_docstrings_catalog.json` as a committed machine-consumable bootstrap asset and the current repository state where that file is absent. Either generate and commit the asset, or revise the contracts/docs so the asset is clearly on-demand rather than baseline-present.
  - Target Files: `context/project_docstrings_catalog.json`, `context/README.md`, `scripts/README.md`, `docs/agent_bootstrap/README.md`, `docs/generated_artifact_contracts.md`, `docs/source_boundary_manifest.md`, `README.md`
  - Dependencies: `None`
  - DONE WHEN: The repo either contains a current `context/project_docstrings_catalog.json` generated from the canonical script, or all documentation/contract language is revised so contributors are not told a committed bootstrap asset exists when it does not.
  - Audit step: Run `python scripts/aggregate_project_docstrings.py --root . --output context/project_docstrings_catalog.json`, verify the JSON parses cleanly, and then confirm that repo docs and commit-policy text match the chosen committed-vs-on-demand behavior.

- [ ] **Make task-recipe validation reproducible from declared dependencies**
  - Scope: Fix the mismatch where `context/task_recipes/README.md` documents a `jsonschema`-based validation workflow, but a fresh environment created from `requirements-dev.txt` cannot import `jsonschema`. This currently makes the published validation contract non-reproducible.
  - Target Files: `requirements-dev.txt`, `pyproject.toml`, `context/task_recipes/README.md`, `docs/task_recipe_schema.md`, optionally `tests/` if regression coverage is added
  - Dependencies: `None`
  - DONE WHEN: A fresh environment created strictly from documented setup can execute the published task-recipe validation flow without missing-module errors, and the dependency surface is documented where operators are told to validate recipes.
  - Audit step: Create a clean virtual environment, install only the repo’s declared development dependencies, run the validation snippet from `context/task_recipes/README.md`, and confirm it succeeds without relying on ambient/global packages.

- [ ] **Reconcile skill assets with actual runtime-consumption semantics**
  - Scope: Resolve the current mismatch between runtime documentation that treats `skills/*/SKILL.md` as directly consumable by Codex-style agent runtimes and the actual implementation, where skills are stored only under `skills/`, lack runtime-spec metadata/front matter, and do not document any vendor-specific mirror or adapter path. The same pass should also clarify shell/tool prerequisites because current skill and task assets rely on `sed`, `cat`, and `rg` without declaring a POSIX/Bash or ripgrep requirement.
  - Target Files: `docs/runtime_target_support_matrix.md`, `skills/README.md`, `skills/checklist-audit/SKILL.md`, `skills/documentation-parity-audit/SKILL.md`, `skills/quality-remediation/SKILL.md`, `skills/template-bootstrap/SKILL.md`, `docs/agent_bootstrap/README.md`, `context/task_recipes/checklist_audit.json`, `docs/new_user_onboarding.md`
  - Dependencies: `None`
  - DONE WHEN: The repo either (a) provides vendor-compliant skill delivery with documented discovery paths/metadata and explicit shell-tool prerequisites, or (b) clearly reclassifies `skills/` as human/advisory workflow assets instead of claiming direct runtime consumption; command assets no longer assume undeclared shell tooling.
  - Audit step: Verify the declared supported runtime can discover or consume the skill assets exactly as documented on a fresh checkout, and verify non-POSIX/non-ripgrep environments are either supported with documented fallbacks or explicitly marked out of scope.

- [ ] **Remove stale pre-implementation wording from the context/runtime matrices**
  - Scope: Clean up matrix rows that still describe recipe/workflow assets as existing only “when added” or workflows as present only “when present,” even though the current template now ships those assets directly. This is a documentation-truthfulness issue, not a missing-asset issue.
  - Target Files: `docs/context_trigger_matrix.md`, `docs/runtime_target_support_matrix.md`
  - Dependencies: `None`
  - DONE WHEN: Both matrices describe the shipped asset set truthfully and use conditional wording only for genuinely optional, external, or organization-specific components.
  - Audit step: Read both matrices against the current tree and confirm every conditional phrase maps to an actually optional/external asset rather than a file already shipped in the repository.

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
