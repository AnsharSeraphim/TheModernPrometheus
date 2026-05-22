#!/usr/bin/env python3
"""Unified pre-commit suite runner for this repository."""

from __future__ import annotations

# pylint: disable=wrong-import-position
import argparse
import importlib.util
import json
import sys
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import cast

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# pylint: disable=wrong-import-position
# pylint: enable=wrong-import-position
from scripts._automation_shared import (  # noqa: E402
    add_include_untracked_argument,
    build_git_diff_commands,
    build_pip_install_command,
    gather_missing_dependencies,
    load_dev_dependency_specs,
    normalize_repository_paths,
    run_command,
)
from scripts.precommit_filter import FilterMetadata, FilterMode, PrecommitFilter  # noqa: E402
from scripts.toml_compat import parse_toml_text

REPO_ROOT = Path(__file__).resolve().parent.parent
SUMMARY_DIR = REPO_ROOT / "build" / "automation_contract"
PRECOMMIT_RAW_LOG = SUMMARY_DIR / "precommit_output.log"
PRECOMMIT_SUMMARY = SUMMARY_DIR / "precommit_summary_block.txt"
DOCSTRING_AUDIT_OUTPUT = SUMMARY_DIR / "docstring_inventory.md"
PYLINT_FAILURE_STORE = REPO_ROOT / "config" / "precommit_store" / "pylint_failures.json"
SUMMARY_WIDTH = 118
_DEFAULT_TARGET_GLOBS: tuple[str, ...] = ("scripts", "tests")
_UTF8_SUFFIXES: tuple[str, ...] = (".py", ".pyi", ".md", ".txt", ".json", ".toml", ".yaml", ".yml", ".ini", ".cfg")
_REQUIRED_TOOL_MODULES: dict[str, str] = {
    "bandit": "bandit",
    "deptry": "deptry",
    "interrogate": "interrogate",
    "mypy": "mypy",
    "pylint": "pylint",
    "pyright": "pyright",
    "ruff": "ruff",
    "vulture": "vulture",
}
FILTER_METADATA: dict[str, FilterMetadata] = {
    "ruff-format": FilterMetadata(hook_id="ruff-format"),
    "ruff-lint": FilterMetadata(hook_id="ruff-lint"),
    "pylint": FilterMetadata(hook_id="pylint"),
    "interrogate": FilterMetadata(hook_id="interrogate"),
    "mypy": FilterMetadata(hook_id="mypy"),
    "pyright": FilterMetadata(hook_id="pyright", global_hook=True),
    "deptry": FilterMetadata(hook_id="deptry", global_hook=True),
    "vulture": FilterMetadata(hook_id="vulture", global_hook=True),
    "bandit": FilterMetadata(hook_id="bandit", global_hook=True),
    "unicode-escapes": FilterMetadata(hook_id="unicode-escapes"),
    "checklist-structure": FilterMetadata(hook_id="checklist-structure", global_hook=True),
}


class Scope(Enum):
    """Supported execution scopes for the quality suite."""

    ALL = "all"
    PATHS = "paths"
    CHANGED = "changed"


@dataclass(frozen=True)
class Check:
    """Metadata describing a single quality check."""

    key: str
    title: str
    command: list[str]
    candidates: tuple[Path, ...]
    global_hook: bool = False


@dataclass(frozen=True)
class CheckResult:
    """Execution metadata for a completed check."""

    check: Check
    status: str
    duration: float
    exit_code: int | None
    note: str | None = None


def _format_banner(label: str, width: int = SUMMARY_WIDTH) -> str:
    """Render a centered summary banner line."""

    text = f" {label} "
    if len(text) >= width:
        return text
    padding = width - len(text)
    left = padding // 2
    right = padding - left
    return "=" * left + text + "=" * right


def _load_dev_dependency_specs() -> dict[str, str]:
    """Load the development dependency map from ``pyproject.toml``."""

    loaded_specs = load_dev_dependency_specs(
        pyproject_path=REPO_ROOT / "pyproject.toml",
        toml_loader=_parse_toml,
        missing_optional_error="[tooling] Missing [project.optional-dependencies] in pyproject.toml.",
        missing_group_error="[tooling] Missing dev dependency group in pyproject.toml.",
    )
    return {str(key): str(value) for key, value in loaded_specs.items()}


def _parse_toml(text: str) -> dict[str, object]:
    """Parse TOML text with the standard-library loader."""

    return cast(dict[str, object], parse_toml_text(text))


def _ensure_quality_toolchain() -> None:
    """Install missing quality-tool dependencies declared in the dev group."""

    dependency_map = _load_dev_dependency_specs()
    missing = gather_missing_dependencies(
        required_modules=_REQUIRED_TOOL_MODULES,
        dependency_map=dependency_map,
        find_spec=importlib.util.find_spec,
        unresolved_error_template=("[tooling] Missing quality dependencies in pyproject.toml dev group: {packages}."),
    )
    if not missing:
        return
    print("Installing missing quality tooling via pip:", ", ".join(missing))
    run_command(build_pip_install_command(missing), cwd=REPO_ROOT, check=True)


def _collect_changed_paths(*, diff_target: str, include_untracked: bool) -> list[Path]:
    """Collect changed repository paths from git diff and optional untracked output."""

    lines: list[str] = []
    for command in build_git_diff_commands(diff_target, include_untracked=include_untracked):
        completed = run_command(command, cwd=REPO_ROOT, check=False)
        lines.extend((completed.stdout or "").splitlines())
    normalized_paths = normalize_repository_paths(lines, repo_root=REPO_ROOT)
    return [Path(path) for path in normalized_paths]


def _normalize_cli_paths(paths: Sequence[str]) -> list[Path]:
    """Normalize user-supplied path arguments to repository-relative paths."""

    normalized: list[Path] = []
    for raw in paths:
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = (REPO_ROOT / candidate).resolve()
        if REPO_ROOT not in candidate.parents and candidate != REPO_ROOT:
            continue
        if candidate.exists():
            normalized.append(candidate.relative_to(REPO_ROOT))
    deduplicated = sorted(set(normalized))
    return deduplicated


def _collect_python_files(paths: Sequence[Path]) -> tuple[Path, ...]:
    """Collect Python files from the provided file and directory paths."""

    collected: list[Path] = []
    for path in paths:
        full_path = REPO_ROOT / path
        if full_path.is_dir():
            collected.extend(sorted(subpath.relative_to(REPO_ROOT) for subpath in full_path.rglob("*.py")))
        elif full_path.suffix == ".py":
            collected.append(path)
    return tuple(sorted(set(collected)))


def _default_python_candidates() -> tuple[Path, ...]:
    """Collect default Python files covered by full quality-suite execution."""

    return _collect_python_files([Path(entry) for entry in _DEFAULT_TARGET_GLOBS])


def _script_python_targets(paths: Sequence[Path]) -> tuple[Path, ...]:
    """Filter the current path selection down to Python files under the scripts tree."""

    script_roots: list[Path] = []
    for path in paths:
        full_path = REPO_ROOT / path
        is_script_path = bool(path.parts) and path.parts[0] == "scripts"
        is_script_directory = full_path.is_dir() and is_script_path
        is_script_python_file = full_path.is_file() and full_path.suffix == ".py" and is_script_path
        if is_script_directory or is_script_python_file:
            script_roots.append(path)
    return _collect_python_files(script_roots)


def _default_script_candidates() -> tuple[Path, ...]:
    """Collect default script-module files covered by interrogate docstring checks."""

    return _collect_python_files((Path("scripts"),))


def _collect_text_files(paths: Sequence[Path]) -> tuple[Path, ...]:
    """Collect text-like files covered by the UTF-8 compliance hook."""

    collected: list[Path] = []
    for path in paths:
        full_path = REPO_ROOT / path
        if full_path.is_dir():
            collected.extend(
                sorted(
                    subpath.relative_to(REPO_ROOT)
                    for subpath in full_path.rglob("*")
                    if subpath.is_file() and subpath.suffix in _UTF8_SUFFIXES
                )
            )
        elif full_path.is_file() and full_path.suffix in _UTF8_SUFFIXES:
            collected.append(path)
    return tuple(sorted(set(collected)))


def _default_text_candidates() -> tuple[Path, ...]:
    """Collect tracked text-like files covered by the UTF-8 compliance hook."""

    completed = run_command(["git", "ls-files"], cwd=REPO_ROOT, check=False)
    if completed.returncode != 0:
        return tuple()
    tracked = [Path(line.strip()) for line in (completed.stdout or "").splitlines() if line.strip()]
    return tuple(sorted(path for path in tracked if path.suffix in _UTF8_SUFFIXES))


def resolve_targeted_paths(
    *,
    scope_value: str,
    cli_paths: Sequence[str],
    diff_target: str,
    include_untracked: bool,
) -> tuple[Scope, tuple[Path, ...] | None]:
    """Resolve CLI scope arguments into a concrete scope and selected repository paths."""

    if scope_value == Scope.ALL.value:
        return Scope.ALL, None
    if scope_value == Scope.PATHS.value:
        if not cli_paths:
            raise SystemExit("--scope paths requires at least one path passed to --paths.")
        return Scope.PATHS, tuple(_normalize_cli_paths(cli_paths))
    changed_paths = _collect_changed_paths(diff_target=diff_target, include_untracked=include_untracked)
    return Scope.CHANGED, tuple(changed_paths)


def _python_targets_for_scope(paths: tuple[Path, ...] | None) -> tuple[Path, ...]:
    """Resolve Python-target candidates for the current scope."""

    return _default_python_candidates() if paths is None else _collect_python_files(paths)


def _text_targets_for_scope(paths: tuple[Path, ...] | None) -> tuple[Path, ...]:
    """Resolve text-target candidates for the current scope."""

    return _default_text_candidates() if paths is None else _collect_text_files(paths)


def _script_targets_for_scope(paths: tuple[Path, ...] | None) -> tuple[Path, ...]:
    """Resolve script-target candidates for interrogate coverage checks."""

    return _default_script_candidates() if paths is None else _script_python_targets(paths)


def _build_checks(
    python_targets: tuple[Path, ...],
    text_targets: tuple[Path, ...],
    script_targets: tuple[Path, ...],
) -> list[Check]:
    """Build check definitions for the current execution scope."""

    python_target_strings = [path.as_posix() for path in python_targets]
    checks = [
        Check(
            key="ruff-format",
            title="Ruff format",
            command=[sys.executable, "-m", "ruff", "format", *python_target_strings],
            candidates=python_targets,
        ),
        Check(
            key="ruff-lint",
            title="Ruff lint",
            command=[sys.executable, "-m", "ruff", "check", "--fix", *python_target_strings],
            candidates=python_targets,
        ),
        Check(
            key="pylint",
            title="Pylint",
            command=[sys.executable, "-m", "pylint", *python_target_strings],
            candidates=python_targets,
        ),
        Check(
            key="interrogate",
            title="Interrogate",
            command=[
                sys.executable,
                "-m",
                "interrogate",
                "--fail-under=100",
                *[path.as_posix() for path in script_targets],
            ],
            candidates=script_targets,
        ),
        Check(
            key="mypy",
            title="MyPy",
            command=[sys.executable, "-m", "mypy", *python_target_strings],
            candidates=python_targets,
        ),
        Check(
            key="pyright",
            title="Pyright",
            command=[sys.executable, "-m", "pyright"],
            candidates=python_targets,
            global_hook=True,
        ),
        Check(
            key="deptry",
            title="Deptry",
            command=[sys.executable, "-m", "deptry", "."],
            candidates=python_targets,
            global_hook=True,
        ),
        Check(
            key="vulture",
            title="Vulture",
            command=[sys.executable, "-m", "vulture", "scripts", "tests"],
            candidates=python_targets,
            global_hook=True,
        ),
        Check(
            key="bandit",
            title="Bandit",
            command=[sys.executable, "-m", "bandit", "-q", "-r", "scripts", "tests"],
            candidates=python_targets,
            global_hook=True,
        ),
        Check(
            key="unicode-escapes",
            title="UTF-8 compliance",
            command=[sys.executable, "scripts/check_unicode_escapes.py"],
            candidates=text_targets,
        ),
        Check(
            key="checklist-structure",
            title="Checklist structure guard",
            command=[sys.executable, "scripts/check_checklist_structure.py"],
            candidates=(Path("Final-Productization-Checklist.md"),),
            global_hook=True,
        ),
    ]
    return checks


def _targeted_command(check: Check, selected_paths: tuple[Path, ...]) -> list[str]:
    """Narrow a check command to selected paths when the hook supports targeted execution."""

    selected = [path.as_posix() for path in selected_paths]
    command_by_key = {
        "ruff-format": [sys.executable, "-m", "ruff", "format", *selected],
        "ruff-lint": [sys.executable, "-m", "ruff", "check", "--fix", *selected],
        "pylint": [sys.executable, "-m", "pylint", *selected],
        "interrogate": [sys.executable, "-m", "interrogate", "--fail-under=100", *selected],
        "mypy": [sys.executable, "-m", "mypy", *selected],
        "unicode-escapes": [sys.executable, "scripts/check_unicode_escapes.py", "--paths", *selected],
    }
    return command_by_key.get(check.key, list(check.command))


def _filtered_checks(checks: Sequence[Check], *, only: str | None) -> list[Check]:
    """Filter check definitions to a single hook when ``--only`` is provided."""

    if only is None:
        return list(checks)
    matches = [check for check in checks if check.key == only]
    if not matches:
        raise SystemExit(f"Unknown hook '{only}'.")
    return matches


def _load_pylint_failures() -> dict[str, list[str]]:
    """Load cached pylint failures from disk."""

    if not PYLINT_FAILURE_STORE.exists():
        return {}
    try:
        payload = json.loads(PYLINT_FAILURE_STORE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(payload, dict):
        return {}
    payload_mapping = cast(dict[str, object], payload)
    normalized: dict[str, list[str]] = {}
    for key_object, value_object in payload_mapping.items():
        if not isinstance(value_object, list):
            continue
        candidate_lines = cast(list[object], value_object)
        if all(isinstance(item, str) for item in candidate_lines):
            normalized[key_object] = [cast(str, item) for item in candidate_lines]
    return normalized


def _save_pylint_failures(payload: Mapping[str, list[str]]) -> None:
    """Persist pylint failure cache entries to disk."""

    PYLINT_FAILURE_STORE.parent.mkdir(parents=True, exist_ok=True)
    PYLINT_FAILURE_STORE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _update_pylint_failure_store(check: Check, stdout_text: str, success: bool) -> None:
    """Update cached pylint failures for the paths covered by ``check``."""

    failures = _load_pylint_failures()
    relevant_keys = [path.as_posix() for path in check.candidates]
    if success:
        for key in relevant_keys:
            failures.pop(key, None)
    else:
        lines = [line for line in stdout_text.splitlines() if line.strip()]
        for key in relevant_keys:
            failures[key] = lines
    _save_pylint_failures(failures)


def _run_check(check: Check) -> tuple[int, str, float]:
    """Execute one quality check and capture its status, output, and elapsed duration."""

    start = time.perf_counter()
    completed = run_command(check.command, cwd=REPO_ROOT, check=False)
    duration = time.perf_counter() - start
    output = (completed.stdout or "") + (completed.stderr or "")
    return completed.returncode, output, duration


def _run_interrogate_followup(*, failed_check: Check, precommit_lines: list[str]) -> None:
    """Generate a docstring inventory report when the interrogate hook fails."""

    scan_roots = sorted({path.parts[0] for path in failed_check.candidates if path.parts})
    if not scan_roots:
        scan_roots = ["scripts"]
    command = [
        sys.executable,
        "scripts/audit_docstrings.py",
        *[argument for scan_root in scan_roots for argument in ("--scan-root", scan_root)],
        "--output",
        str(DOCSTRING_AUDIT_OUTPUT),
    ]
    completed = run_command(command, cwd=REPO_ROOT, check=False)
    output = (completed.stdout or "") + (completed.stderr or "")
    status = "PASSED" if completed.returncode == 0 else "FAILED"
    guidance = (
        "Use the generated `## Missing docstrings` table to remediate coverage gaps or create granular "
        "checklist follow-up entries."
    )
    _log_block(
        precommit_lines,
        f"Interrogate follow-up audit {status}",
        f"{output.rstrip()}\n{guidance}".strip(),
    )


def _log_block(lines: list[str], label: str, body: str) -> None:
    """Append a labeled output block to the pre-commit raw log buffer."""

    lines.append(_format_banner(label))
    if body.strip():
        lines.append(body.rstrip())


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the pre-commit suite runner."""

    parser = argparse.ArgumentParser(description="Run the repository quality suite.", allow_abbrev=False)
    parser.add_argument("--only", help="Run a single hook by id.")
    parser.add_argument(
        "--scope",
        choices=[scope.value for scope in Scope],
        default=Scope.ALL.value,
        help="Execution scope: all, paths, or changed.",
    )
    parser.add_argument("--paths", nargs="*", default=[], help="Explicit paths used with --scope paths.")
    parser.add_argument("--diff-target", default="HEAD", help="Git reference used for --scope changed.")
    add_include_untracked_argument(parser, help_text="Include untracked files when resolving --scope changed.")
    parser.add_argument(
        "--filter-mode",
        choices=[mode.value for mode in FilterMode],
        default=FilterMode.AUTO.value,
        help="Manifest filter mode: auto, full, or off.",
    )
    parser.add_argument(
        "--reset-baseline",
        action="store_true",
        help="Rebuild the skip manifests from tracked Python files before running checks.",
    )
    parser.add_argument(
        "--skip-dependency-check",
        action="store_true",
        help="Skip verification that quality tooling is installed.",
    )
    return parser.parse_args()


def _should_skip_global_hook(should_run: bool, check: Check, filter_mode: FilterMode) -> bool:
    """Decide whether a global hook is unnecessary for the current targeted run."""

    return not should_run and check.global_hook and filter_mode == FilterMode.AUTO


def _prepare_check(check: Check, selected_paths: tuple[Path, ...]) -> Check:
    """Construct the executable check definition for the current path selection."""

    if check.global_hook:
        return check
    return Check(
        key=check.key,
        title=check.title,
        command=_targeted_command(check, selected_paths),
        candidates=selected_paths,
        global_hook=False,
    )


def _execute_checks(
    *,
    checks: Sequence[Check],
    manifest_filter: PrecommitFilter,
    precommit_lines: list[str],
) -> tuple[list[CheckResult], int]:
    """Execute prepared quality checks and compute the aggregate suite exit code."""

    results: list[CheckResult] = []
    exit_code = 0
    for check in checks:
        selected_paths, should_run, note = manifest_filter.determine_paths(check.key, check.candidates)
        if not should_run and not check.global_hook:
            results.append(CheckResult(check=check, status="SKIPPED", duration=0.0, exit_code=None, note=note))
            continue
        if _should_skip_global_hook(should_run, check, manifest_filter.mode):
            results.append(CheckResult(check=check, status="SKIPPED", duration=0.0, exit_code=None, note=note))
            continue

        applicable_check = _prepare_check(check, selected_paths)
        current_exit, output, duration = _run_check(applicable_check)
        success = current_exit == 0
        manifest_filter.record_result(check.key, applicable_check.candidates, success=success)
        if check.key == "pylint":
            _update_pylint_failure_store(applicable_check, output, success)
        status = "PASSED" if success else "FAILED"
        results.append(CheckResult(check=check, status=status, duration=duration, exit_code=current_exit))
        _log_block(precommit_lines, f"{check.title} {status}", output)
        if not success:
            exit_code = current_exit or 1
            if check.key == "interrogate":
                _run_interrogate_followup(failed_check=applicable_check, precommit_lines=precommit_lines)
    return results, exit_code


def _resolve_scope_targets(
    scope: Scope,
    targeted_paths: tuple[Path, ...] | None,
) -> tuple[tuple[Path, ...], tuple[Path, ...], tuple[Path, ...]]:
    """Resolve Python, text, and script target sets for the requested suite scope."""

    scoped_paths = None if scope == Scope.ALL else targeted_paths
    python_targets = _python_targets_for_scope(scoped_paths)
    text_targets = _text_targets_for_scope(scoped_paths)
    script_targets = _script_targets_for_scope(scoped_paths)
    return python_targets, text_targets, script_targets


def _run_suite(args: argparse.Namespace) -> tuple[list[CheckResult], list[str], int]:
    """Execute checks for parsed args and return results, log lines, and exit code."""

    scope, targeted_paths = resolve_targeted_paths(
        scope_value=args.scope,
        cli_paths=args.paths,
        diff_target=args.diff_target,
        include_untracked=args.include_untracked,
    )
    python_targets, text_targets, script_targets = _resolve_scope_targets(scope, targeted_paths)
    checks = _filtered_checks(_build_checks(python_targets, text_targets, script_targets), only=args.only)
    precommit_lines: list[str] = []
    manifest_filter = PrecommitFilter(mode=FilterMode(args.filter_mode))
    manifest_filter.configure_checks(FILTER_METADATA)
    manifest_filter.build_repository_inventory()
    with manifest_filter.session_guard():
        manifest_filter.sync_manifest()
        manifest_filter.set_targeted_paths(None if scope == Scope.ALL else targeted_paths)
        if args.reset_baseline:
            manifest_filter.reset_all_flags()
        manifest_filter.flush_manifest_log()
        results, exit_code = _execute_checks(
            checks=checks,
            manifest_filter=manifest_filter,
            precommit_lines=precommit_lines,
        )
        manifest_filter.save()
    return results, precommit_lines, exit_code


def main() -> int:
    """Execute the unified pre-commit suite and write wrapper summary artifacts."""

    args = parse_args()
    if not args.skip_dependency_check:
        _ensure_quality_toolchain()
    else:
        print("Dependency verification skipped.")

    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    results, precommit_lines, exit_code = _run_suite(args)

    table_lines = [_format_banner("Pre-commit suite summary")]
    for result in results:
        suffix = f" ({result.note})" if result.note else ""
        table_lines.append(f"- {result.check.key}: {result.status} in {result.duration:.2f}s{suffix}")
    overall_status = "PASSED" if exit_code == 0 else "FAILED"
    table_lines.append(_format_banner(f"Pre-commit suite {overall_status}"))
    table_lines.append(
        f"Pre-commit suite {overall_status} in {sum(result.duration for result in results):.2f}s (wall clock). "
        "Copy this block into PR notes or review summaries."
    )

    full_output = "\n".join(precommit_lines + table_lines) + "\n"
    PRECOMMIT_RAW_LOG.write_text(full_output, encoding="utf-8")
    PRECOMMIT_SUMMARY.write_text("\n".join(table_lines) + "\n", encoding="utf-8")
    print(full_output)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
