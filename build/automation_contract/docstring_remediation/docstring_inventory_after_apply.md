# Programmatic Docstring Inventory

Generated for documentation parity audits. Delete or regenerate this file after the audit session.

Coverage summary: documented 181/181 symbols (100.00%).
Coverage status: COMPLETE (all scanned files parsed successfully).

| File | Symbol | Kind | Line | Summary |
| --- | --- | --- | ---: | --- |
| `scripts/__init__.py` | `scripts.__init__` | module | 1 | Automation helpers for the LCDADTMB repository. |
| `scripts/_automation_shared.py` | `scripts._automation_shared` | module | 1 | Shared helpers for repository automation scripts. |
| `scripts/_automation_shared.py` | `scripts._automation_shared._expect_table` | function | 14 | Validate that a TOML key contains the nested table required by automation loaders. |
| `scripts/_automation_shared.py` | `scripts._automation_shared._expect_list` | function | 23 | Validate that a TOML key contains the list required by automation loaders. |
| `scripts/_automation_shared.py` | `scripts._automation_shared.load_dev_dependency_specs` | function | 32 | Extract normalized package specifiers from the project dev dependency group. |
| `scripts/_automation_shared.py` | `scripts._automation_shared.resolve_missing_dependencies` | function | 60 | Resolve unavailable runtime modules into installable dev dependency specifiers. |
| `scripts/_automation_shared.py` | `scripts._automation_shared.raise_for_unresolved_dependencies` | function | 81 | Raise ``SystemExit`` if required packages were not declared in ``pyproject.toml``. |
| `scripts/_automation_shared.py` | `scripts._automation_shared.gather_missing_dependencies` | function | 89 | Collect installable dependency specifiers and fail on undeclared required packages. |
| `scripts/_automation_shared.py` | `scripts._automation_shared.build_pip_install_command` | function | 107 | Compose the interpreter-local pip command used for toolchain self-installation. |
| `scripts/_automation_shared.py` | `scripts._automation_shared.run_command` | function | 122 | Execute ``command`` with predictable text-mode defaults. |
| `scripts/_automation_shared.py` | `scripts._automation_shared.normalize_repository_paths` | function | 143 | Normalize raw path strings into existing repository-relative paths. |
| `scripts/_automation_shared.py` | `scripts._automation_shared.build_git_diff_commands` | function | 163 | Compose git queries that enumerate changed, staged, and optional untracked files. |
| `scripts/_automation_shared.py` | `scripts._automation_shared.add_include_untracked_argument` | function | 175 | Register the shared ``--include-untracked`` flag. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings` | module | 1 | Build a monolithic JSON catalog of Python docstrings keyed by filename. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings.DocstringEntry` | class | 18 | Represent one extracted docstring and its source location metadata. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings.FileDocstringRecord` | class | 28 | Capture export-ready docstring details for one Python source file. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings.parse_args` | function | 38 | Parse CLI options for repository scan and JSON output destination. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._module_role_description` | function | 63 | Generate a 1-3 sentence narrative role description for the module entry. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._iter_symbols` | function | 85 | Collect module/class/function symbols in source order for docstring extraction. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._iter_symbols.Visitor` | class | 90 | Track nesting so extracted symbol names preserve dotted qualification. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._iter_symbols.Visitor.__init__` | function | 93 | Initialize an empty stack for class/function scope traversal. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._iter_symbols.Visitor.visit_ClassDef` | function | 97 | Record class symbols and recurse into nested members. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._iter_symbols.Visitor.visit_FunctionDef` | function | 105 | Record sync function symbols and recurse into nested members. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._iter_symbols.Visitor.visit_AsyncFunctionDef` | function | 113 | Record async function symbols and recurse into nested members. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._quality_notes` | function | 125 | Detect heuristic docstring quality findings for catalog remediation workflows. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._evaluate_symbol_docstring` | function | 140 | Evaluate one symbol and return extracted entry, missing marker, and quality flags. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._build_audit_payloads` | function | 158 | Construct completeness and quality audit payload dictionaries. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._collect_symbol_entries` | function | 180 | Collect docstring entries, missing symbols, and weak-symbol flags. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._collect_file_record` | function | 201 | Parse one file and return extracted docstrings plus completeness and quality audit. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._is_excluded` | function | 222 | Identify paths that belong to excluded repository directories during catalog scans. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._record_to_payload` | function | 228 | Convert one file record into a JSON-serializable payload entry. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings._update_totals` | function | 248 | Accumulate symbol, missing-docstring, and flagged-docstring totals. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings.build_catalog` | function | 261 | Aggregate all Python docstrings under the repository root into one payload. |
| `scripts/aggregate_project_docstrings.py` | `scripts.aggregate_project_docstrings.main` | function | 283 | Generate the catalog and write it as UTF-8 JSON for export. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings` | module | 1 | Build a Markdown docstring inventory for documentation-versus-implementation audits. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings.DocstringEntry` | class | 20 | Represent one discovered docstring with location metadata. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings.MissingDocstringEntry` | class | 30 | Represent one module/class/function symbol that lacks a docstring. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings.ScanFailureEntry` | class | 39 | Represent one file-level parse/read failure encountered during scanning. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings._DocstringCollector` | class | 47 | Collect module, class, and function docstrings from an AST. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings._DocstringCollector.__init__` | function | 50 | Initialize collector state for one module path. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings._DocstringCollector.visit_Module` | function | 58 | Visit a module node and capture its docstring. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings._DocstringCollector.visit_ClassDef` | function | 64 | Visit a class node and capture class-level docstrings. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings._DocstringCollector.visit_FunctionDef` | function | 69 | Visit a function node and capture function docstrings. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings._DocstringCollector.visit_AsyncFunctionDef` | function | 74 | Visit an async function node and capture function docstrings. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings._DocstringCollector._visit_symbol_node` | function | 79 | Capture one non-module symbol and recurse into its children. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings._DocstringCollector._record_docstring` | function | 90 | Record a docstring entry for the provided AST node when present. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings._is_excluded` | function | 109 | Identify paths that pass through directories excluded from docstring inventory scans. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings._iter_python_files` | function | 115 | Enumerate sorted Python files beneath the configured audit scan roots. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings._relative_display_path` | function | 130 | Derive stable inventory display paths for repository and ad hoc scan roots. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings.collect_docstrings` | function | 143 | Collect present and missing docstring entries grouped by relative Python file path. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings.build_inventory_markdown` | function | 174 | Render docstring inventory markdown with present/missing coverage context. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings._parse_args` | function | 265 | Parse CLI flags for scan roots and output path overrides. |
| `scripts/audit_docstrings.py` | `scripts.audit_docstrings.main` | function | 285 | Generate a Markdown inventory of discovered docstrings. |
| `scripts/check_checklist_structure.py` | `scripts.check_checklist_structure` | module | 1 | Validate required checklist governance sections remain intact. |
| `scripts/check_checklist_structure.py` | `scripts.check_checklist_structure.parse_args` | function | 20 | Parse CLI arguments for checklist structure validation. |
| `scripts/check_checklist_structure.py` | `scripts.check_checklist_structure.validate_checklist` | function | 33 | Identify missing governance sections in the required productization checklist. |
| `scripts/check_checklist_structure.py` | `scripts.check_checklist_structure.main` | function | 47 | Execute checklist structure validation and report the resulting process status. |
| `scripts/check_conflicts.py` | `scripts.check_conflicts` | module | 1 | Scan the repository for merge-conflict markers and a few common hygiene issues. |
| `scripts/check_conflicts.py` | `scripts.check_conflicts.iter_files` | function | 15 | Yield files under ``root`` while skipping generated directories. |
| `scripts/check_conflicts.py` | `scripts.check_conflicts.find_conflict_markers` | function | 25 | Locate merge-conflict marker diagnostics within a repository text file. |
| `scripts/check_conflicts.py` | `scripts.check_conflicts.find_duplicate_top_level_definitions` | function | 40 | Detect repeated top-level Python class or function definitions in one file. |
| `scripts/check_conflicts.py` | `scripts.check_conflicts.find_python_whitespace_issues` | function | 61 | Detect Python trailing whitespace and indentation-style inconsistencies in one file. |
| `scripts/check_conflicts.py` | `scripts.check_conflicts.main` | function | 91 | Execute the repository hygiene scan for conflicts, duplicates, and whitespace issues. |
| `scripts/check_unicode_escapes.py` | `scripts.check_unicode_escapes` | module | 1 | Enforce UTF-8 text encoding and reject symbolic Unicode escape literals. |
| `scripts/check_unicode_escapes.py` | `scripts.check_unicode_escapes.parse_args` | function | 28 | Parse CLI arguments for repository text-file scanning. |
| `scripts/check_unicode_escapes.py` | `scripts.check_unicode_escapes._tracked_files` | function | 42 | Enumerate git-tracked files used as default text-encoding scan candidates. |
| `scripts/check_unicode_escapes.py` | `scripts.check_unicode_escapes._resolve_candidates` | function | 56 | Resolve explicit path inputs or tracked defaults to scannable text assets. |
| `scripts/check_unicode_escapes.py` | `scripts.check_unicode_escapes.scan_candidates` | function | 91 | Inspect candidate text assets for invalid UTF-8 bytes and symbolic Unicode escapes. |
| `scripts/check_unicode_escapes.py` | `scripts.check_unicode_escapes.main` | function | 115 | Execute repository text-encoding checks and print remediation guidance on failure. |
| `scripts/manual_hook_warning.py` | `scripts.manual_hook_warning` | module | 1 | Redirect manual hook invocations to the unified pre-commit runner. |
| `scripts/manual_hook_warning.py` | `scripts.manual_hook_warning._format_command_block` | function | 23 | Format command recommendations as a bullet list block. |
| `scripts/manual_hook_warning.py` | `scripts.manual_hook_warning.render_manual_hook_usage` | function | 31 | Render the advisory that redirects direct pre-commit hook usage to the wrapper suite. |
| `scripts/manual_hook_warning.py` | `scripts.manual_hook_warning.main` | function | 44 | Print the manual-hook advisory and exit non-zero. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter` | module | 1 | Lightweight manifest filter for the unified pre-commit suite. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.FilterMode` | class | 24 | Supported filtering strategies for hook execution. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.FilterMetadata` | class | 33 | Static configuration for a hook that participates in manifest filtering. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter._FilterRuntimeState` | class | 41 | Mutable state container used during a single filtering session. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter` | class | 53 | Skip tracking for pre-commit hooks using JSON manifests. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.__init__` | function | 56 | Initialize filter state and load any existing manifests. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.session_guard` | function | 74 | Provide rollback-safe mutation for a single suite execution. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.configure_checks` | function | 100 | Register hook metadata used by the filter. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.set_targeted_paths` | function | 107 | Record explicit paths for the current run, if any. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.build_repository_inventory` | function | 112 | Enumerate tracked Python files for hook-scoped pre-commit filtering. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.sync_manifest` | function | 131 | Ensure configured manifests match the current Python inventory. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.flush_manifest_log` | function | 151 | Print the accumulated manifest change log. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.determine_paths` | function | 160 | Resolve the concrete repository paths selected for one filtered hook run. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.record_result` | function | 185 | Persist the result of a hook run for ``paths``. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.reset_all_flags` | function | 200 | Rebuild manifests from tracked Python files with every skip flag reset. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.save` | function | 214 | Persist modified manifests to disk. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.verify_index_clean` | function | 236 | Preserve the historical clean-index compatibility check for wrapper callers. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.set_hook_state` | function | 241 | Seed manifest state for ``hook_id``. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.get_hook_state` | function | 246 | Expose an isolated copy of persisted manifest state for one hook identifier. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter.set_inventory` | function | 251 | Seed repository inventory entries for tests or targeted workflows. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter._normalize_candidates` | function | 256 | Normalize hook candidates and ensure they are tracked in hook state. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter._reset_skip_flags` | function | 279 | Reset skip flags to ``False`` for the given hook paths. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter._load_existing_manifests` | function | 288 | Load previously persisted manifest JSON files into runtime state. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter._manifest_path` | function | 311 | Derive the persisted manifest file path associated with one hook identifier. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter.PrecommitFilter._commit_pending_manifests` | function | 316 | Atomically persist deferred manifests collected during an active session. |
| `scripts/precommit_filter.py` | `scripts.precommit_filter._atomic_write_text` | function | 324 | Atomically write UTF-8 text to ``target``. |
| `scripts/pytest_guard.py` | `scripts.pytest_guard` | module | 1 | Guardrail that enforces wrapper-first pytest execution. |
| `scripts/pytest_guard.py` | `scripts.pytest_guard.render_pytest_wrapper_warning` | function | 11 | Render the warning that redirects direct pytest usage to the canonical test wrapper. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite` | module | 1 | Unified pre-commit suite runner for this repository. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite.Scope` | class | 69 | Supported execution scopes for the quality suite. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite.Check` | class | 78 | Metadata describing a single quality check. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite.CheckResult` | class | 89 | Execution metadata for a completed check. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._format_banner` | function | 99 | Render a centered summary banner line. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._load_dev_dependency_specs` | function | 111 | Load the development dependency map from ``pyproject.toml``. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._parse_toml` | function | 123 | Parse TOML text with the standard-library loader. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._ensure_quality_toolchain` | function | 129 | Install missing quality-tool dependencies declared in the dev group. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._collect_changed_paths` | function | 145 | Collect changed repository paths from git diff and optional untracked output. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._normalize_cli_paths` | function | 156 | Normalize user-supplied path arguments to repository-relative paths. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._collect_python_files` | function | 172 | Collect Python files from the provided file and directory paths. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._default_python_candidates` | function | 185 | Collect default Python files covered by full quality-suite execution. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._script_python_targets` | function | 191 | Filter the current path selection down to Python files under the scripts tree. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._default_script_candidates` | function | 205 | Collect default script-module files covered by interrogate docstring checks. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._collect_text_files` | function | 211 | Collect text-like files covered by the UTF-8 compliance hook. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._default_text_candidates` | function | 230 | Collect tracked text-like files covered by the UTF-8 compliance hook. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite.resolve_targeted_paths` | function | 240 | Resolve CLI scope arguments into a concrete scope and selected repository paths. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._python_targets_for_scope` | function | 259 | Resolve Python-target candidates for the current scope. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._text_targets_for_scope` | function | 265 | Resolve text-target candidates for the current scope. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._script_targets_for_scope` | function | 271 | Resolve script-target candidates for interrogate coverage checks. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._build_checks` | function | 277 | Build check definitions for the current execution scope. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._targeted_command` | function | 367 | Narrow a check command to selected paths when the hook supports targeted execution. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._filtered_checks` | function | 382 | Filter check definitions to a single hook when ``--only`` is provided. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._load_pylint_failures` | function | 393 | Load cached pylint failures from disk. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._save_pylint_failures` | function | 415 | Persist pylint failure cache entries to disk. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._update_pylint_failure_store` | function | 422 | Update cached pylint failures for the paths covered by ``check``. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._run_check` | function | 437 | Execute one quality check and capture its status, output, and elapsed duration. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._run_interrogate_followup` | function | 447 | Generate a docstring inventory report when the interrogate hook fails. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._log_block` | function | 474 | Append a labeled output block to the pre-commit raw log buffer. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite.parse_args` | function | 482 | Parse CLI arguments for the pre-commit suite runner. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._should_skip_global_hook` | function | 515 | Decide whether a global hook is unnecessary for the current targeted run. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._prepare_check` | function | 521 | Construct the executable check definition for the current path selection. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._execute_checks` | function | 535 | Execute prepared quality checks and compute the aggregate suite exit code. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._resolve_scope_targets` | function | 570 | Resolve Python, text, and script target sets for the requested suite scope. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite._run_suite` | function | 583 | Execute checks for parsed args and return results, log lines, and exit code. |
| `scripts/run_precommit_suite.py` | `scripts.run_precommit_suite.main` | function | 613 | Execute the unified pre-commit suite and write wrapper summary artifacts. |
| `scripts/run_tests.py` | `scripts.run_tests` | module | 1 | Pytest orchestrator with canonical summary output. |
| `scripts/run_tests.py` | `scripts.run_tests.Scope` | class | 49 | Execution scope options for the test suite. |
| `scripts/run_tests.py` | `scripts.run_tests.TestSelection` | class | 58 | Resolved pytest selection metadata. |
| `scripts/run_tests.py` | `scripts.run_tests._format_banner` | function | 66 | Render a centered summary banner line. |
| `scripts/run_tests.py` | `scripts.run_tests._load_dev_dependency_specs` | function | 78 | Load development dependency specs from ``pyproject.toml``. |
| `scripts/run_tests.py` | `scripts.run_tests._parse_toml` | function | 90 | Parse TOML text with the repository's supported standard-library loader. |
| `scripts/run_tests.py` | `scripts.run_tests._ensure_test_toolchain` | function | 96 | Install missing pytest-related dependencies declared in the dev group. |
| `scripts/run_tests.py` | `scripts.run_tests._collect_changed_paths` | function | 112 | Collect changed repository paths using git diff commands. |
| `scripts/run_tests.py` | `scripts.run_tests._load_profile` | function | 123 | Load a curated test profile by name. |
| `scripts/run_tests.py` | `scripts.run_tests.normalize_select_path` | function | 139 | Normalize a test path or nodeid path component to a repository-relative path. |
| `scripts/run_tests.py` | `scripts.run_tests.resolve_selection` | function | 155 | Resolve CLI test-selection inputs into a concrete pytest scope. |
| `scripts/run_tests.py` | `scripts.run_tests._build_pytest_command` | function | 190 | Build the canonical pytest command for the resolved selection. |
| `scripts/run_tests.py` | `scripts.run_tests._run_pytest` | function | 219 | Execute pytest in a subprocess and persist its combined output plus duration. |
| `scripts/run_tests.py` | `scripts.run_tests._supports_inline_execution` | function | 233 | Decide whether a lightweight single-target pytest run can execute inline safely. |
| `scripts/run_tests.py` | `scripts.run_tests._run_pytest_inline` | function | 243 | Execute pytest inline for focused single-target selections with wrapper gating. |
| `scripts/run_tests.py` | `scripts.run_tests.parse_args` | function | 275 | Parse CLI arguments for the pytest runner. |
| `scripts/run_tests.py` | `scripts.run_tests.main` | function | 307 | Execute the test suite workflow and write summary artifacts. |
| `scripts/toml_compat.py` | `scripts.toml_compat` | module | 1 | Compatibility TOML parsing helper for wrapper scripts. |
| `scripts/toml_compat.py` | `scripts.toml_compat.parse_toml_text` | function | 10 | Parse TOML text using stdlib ``tomllib`` or fallback ``tomli``. |
| `tests/conftest.py` | `tests.conftest` | module | 1 | Global pytest policy hooks for repository tests. |
| `tests/conftest.py` | `tests.conftest.pytest_sessionstart` | function | 12 | Block direct pytest execution unless wrapper opt-in is present. |
| `tests/test_aggregate_project_docstrings.py` | `tests.test_aggregate_project_docstrings` | module | 1 | Tests for the docstring catalog aggregation helper. |
| `tests/test_aggregate_project_docstrings.py` | `tests.test_aggregate_project_docstrings.test_build_catalog_reports_missing_and_flagged_docstrings` | function | 11 | Aggregate summary reflects missing and weak docstring findings. |
| `tests/test_aggregate_project_docstrings.py` | `tests.test_aggregate_project_docstrings.test_build_catalog_excludes_requested_roots` | function | 34 | Excluded top-level directories are skipped during catalog scans. |
| `tests/test_audit_docstrings.py` | `tests.test_audit_docstrings` | module | 1 | Tests for the Markdown docstring audit inventory helper. |
| `tests/test_audit_docstrings.py` | `tests.test_audit_docstrings.test_collect_docstrings_skips_excluded_directories` | function | 10 | Collector excludes Python files beneath directories like build/ and .venv/. |
| `tests/test_audit_docstrings.py` | `tests.test_audit_docstrings.test_build_inventory_markdown_includes_symbol_table` | function | 28 | Rendered inventory contains stable Markdown rows for discovered symbols. |
| `tests/test_audit_docstrings.py` | `tests.test_audit_docstrings.test_build_inventory_markdown_marks_incomplete_when_scan_failures_exist` | function | 45 | Coverage summary marks inventory incomplete when scan failures are present. |
| `tests/test_check_checklist_structure.py` | `tests.test_check_checklist_structure` | module | 1 | Tests for checklist structure validation utility. |
| `tests/test_check_checklist_structure.py` | `tests.test_check_checklist_structure.test_validate_checklist_passes_for_required_sections` | function | 10 | Validation succeeds when all required snippets are present. |
| `tests/test_check_checklist_structure.py` | `tests.test_check_checklist_structure.test_validate_checklist_reports_missing_sections` | function | 31 | Validation reports each required section that is missing. |
| `tests/test_check_unicode_escapes.py` | `tests.test_check_unicode_escapes` | module | 1 | Tests for UTF-8 and escaped-Unicode policy diagnostics. |
| `tests/test_check_unicode_escapes.py` | `tests.test_check_unicode_escapes.test_scan_candidates_flags_escape_literals` | function | 12 | Report symbolic ``\u`` escapes as violations without flagging UTF-8 decode errors. |
| `tests/test_check_unicode_escapes.py` | `tests.test_check_unicode_escapes.test_scan_candidates_flags_invalid_utf8_bytes` | function | 28 | Report decode failures for invalid UTF-8 bytes and no escape-literal findings. |
| `tests/test_manual_hook_warning.py` | `tests.test_manual_hook_warning` | module | 1 | Tests for manual-hook guidance messaging. |
| `tests/test_manual_hook_warning.py` | `tests.test_manual_hook_warning.test_manual_hook_warning_mentions_runner` | function | 8 | Mention the wrapper command and the original hook id in the advisory output. |
| `tests/test_precommit_filter.py` | `tests.test_precommit_filter` | module | 1 | Tests for pre-commit manifest filtering state transitions. |
| `tests/test_precommit_filter.py` | `tests.test_precommit_filter.test_targeted_run_resets_skip_flags` | function | 10 | Reset skip flags for explicitly targeted files before rerunning the selected hook. |
| `tests/test_precommit_filter.py` | `tests.test_precommit_filter.test_reset_all_flags_rebuilds_inventory` | function | 33 | Rebuild hook state from the tracked inventory during baseline reset operations. |
| `tests/test_pytest_guard.py` | `tests.test_pytest_guard` | module | 1 | Tests for pytest wrapper guard messaging. |
| `tests/test_pytest_guard.py` | `tests.test_pytest_guard.test_pytest_guard_mentions_wrapper_commands` | function | 8 | Include wrapper execution guidance and diagnostic environment details. |
| `tests/test_run_tests.py` | `tests.test_run_tests` | module | 1 | Tests for test-scope selection behavior in the wrapper runner. |
| `tests/test_run_tests.py` | `tests.test_run_tests.test_resolve_selection_uses_paths_for_explicit_select` | function | 8 | Prefer explicit path targeting when ``--select`` arguments are supplied. |
| `tests/test_run_tests.py` | `tests.test_run_tests.test_resolve_selection_uses_all_when_no_selectors` | function | 24 | Fallback to full-suite execution when no selector inputs are provided. |

## Missing docstrings

No missing module/class/function docstrings were detected.

## Scan failures

No scan/parsing failures were detected.
