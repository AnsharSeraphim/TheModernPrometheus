#!/usr/bin/env python3
"""Pytest orchestrator with canonical summary output."""

from __future__ import annotations

# pylint: disable=wrong-import-position
import argparse
import importlib
import importlib.util
import io
import os
import sys
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, cast

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
from scripts.pytest_guard import WRAPPER_ENV_VAR
from scripts.toml_compat import parse_toml_text

REPO_ROOT = Path(__file__).resolve().parent.parent
SUMMARY_DIR = REPO_ROOT / "build" / "automation_contract"
PYTEST_RAW_LOG = SUMMARY_DIR / "pytest_output.log"
PYTEST_SUMMARY = SUMMARY_DIR / "test_summary_block.txt"
SUMMARY_WIDTH = 118
DEFAULT_DURATIONS = 10
DEFAULT_DURATIONS_MIN = 0.2
DEFAULT_MAXFAIL = 1
PROFILE_DIR = REPO_ROOT / "scripts" / "test_profiles"
_REQUIRED_TEST_MODULES: dict[str, str] = {"pytest": "pytest", "pytest-xdist": "xdist"}


class Scope(Enum):
    """Execution scope options for the test suite."""

    ALL = "all"
    PATHS = "paths"
    CHANGED = "changed"


@dataclass(frozen=True)
class TestSelection:
    """Resolved pytest selection metadata."""

    scope: Scope
    targets: list[str]
    pattern: str | None


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
    """Load development dependency specs from ``pyproject.toml``."""

    loaded_specs = load_dev_dependency_specs(
        pyproject_path=REPO_ROOT / "pyproject.toml",
        toml_loader=_parse_toml,
        missing_optional_error="[tooling] Missing [project.optional-dependencies] in pyproject.toml.",
        missing_group_error="[tooling] Missing dev dependency group in pyproject.toml.",
    )
    return {str(key): str(value) for key, value in loaded_specs.items()}


def _parse_toml(text: str) -> dict[str, object]:
    """Parse TOML text with the repository's supported standard-library loader."""

    return cast(dict[str, object], parse_toml_text(text))


def _ensure_test_toolchain() -> None:
    """Install missing pytest-related dependencies declared in the dev group."""

    dependency_map = _load_dev_dependency_specs()
    missing = gather_missing_dependencies(
        required_modules=_REQUIRED_TEST_MODULES,
        dependency_map=dependency_map,
        find_spec=importlib.util.find_spec,
        unresolved_error_template=("[tooling] Missing testing dependencies in pyproject.toml dev group: {packages}."),
    )
    if not missing:
        return
    print("Installing missing testing dependencies via pip:", ", ".join(missing))
    run_command(build_pip_install_command(missing), cwd=REPO_ROOT, check=True)


def _collect_changed_paths(*, diff_target: str, include_untracked: bool) -> list[Path]:
    """Collect changed repository paths using git diff commands."""

    lines: list[str] = []
    for command in build_git_diff_commands(diff_target, include_untracked=include_untracked):
        completed = run_command(command, cwd=REPO_ROOT, check=False)
        lines.extend((completed.stdout or "").splitlines())
    normalized_paths = normalize_repository_paths(lines, repo_root=REPO_ROOT)
    return [Path(path) for path in normalized_paths]


def _load_profile(name: str) -> list[str]:
    """Load a curated test profile by name."""

    profile_path = PROFILE_DIR / f"{name}.txt"
    if not profile_path.exists():
        raise SystemExit(f"Unknown profile '{name}'. Expected file: {profile_path}")
    entries = [
        line.strip()
        for line in profile_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if not entries:
        raise SystemExit(f"Profile '{name}' contains no test targets.")
    return entries


def normalize_select_path(raw: str) -> str | None:
    """Normalize a test path or nodeid path component to a repository-relative path."""

    nodeid_path, _, _ = raw.partition("::")
    if not nodeid_path:
        return None
    candidate = Path(nodeid_path)
    if not candidate.is_absolute():
        candidate = (REPO_ROOT / candidate).resolve()
    if REPO_ROOT not in candidate.parents and candidate != REPO_ROOT:
        return None
    if not candidate.exists():
        return None
    return candidate.relative_to(REPO_ROOT).as_posix()


def resolve_selection(
    *,
    scope_value: str,
    select_paths: list[str],
    pattern: str | None,
    diff_target: str,
    include_untracked: bool,
) -> TestSelection:
    """Resolve CLI test-selection inputs into a concrete pytest scope."""

    normalized_select = [normalize_select_path(entry) for entry in select_paths]
    normalized = [entry for entry in normalized_select if entry]

    if scope_value == "auto":
        if normalized or pattern:
            return TestSelection(scope=Scope.PATHS, targets=normalized, pattern=pattern)
        return TestSelection(scope=Scope.ALL, targets=[], pattern=pattern)
    if scope_value == Scope.ALL.value:
        return TestSelection(scope=Scope.ALL, targets=[], pattern=pattern)
    if scope_value == Scope.PATHS.value:
        if not normalized and not pattern:
            raise SystemExit("--scope paths requires at least one --select argument or a pattern.")
        return TestSelection(scope=Scope.PATHS, targets=normalized, pattern=pattern)

    changed_tests = [
        path.as_posix()
        for path in _collect_changed_paths(diff_target=diff_target, include_untracked=include_untracked)
        if path.as_posix().startswith("tests/")
    ]
    if not changed_tests:
        print("No changed tests detected; defaulting to the full suite.")
        return TestSelection(scope=Scope.ALL, targets=[], pattern=pattern)
    return TestSelection(scope=Scope.PATHS, targets=changed_tests, pattern=pattern)


def _build_pytest_command(
    selection: TestSelection,
    *,
    durations: int,
    duration_threshold: float,
    max_fail: int,
    extra_args: Sequence[str],
) -> list[str]:
    """Build the canonical pytest command for the resolved selection."""

    command: list[str] = [
        sys.executable,
        "-m",
        "pytest",
        "--durations",
        str(durations),
        "--durations-min",
        f"{duration_threshold:.3f}",
        "--maxfail",
        str(max_fail),
        "-q",
    ]
    if selection.pattern:
        command.extend(["-k", selection.pattern])
    command.extend(selection.targets)
    command.extend(arg for arg in extra_args if arg != "--")
    return command


def _run_pytest(command: Sequence[str]) -> tuple[int, str, float]:
    """Execute pytest in a subprocess and persist its combined output plus duration."""

    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    env = dict(os.environ)
    env[WRAPPER_ENV_VAR] = "1"
    completed = run_command(command, cwd=REPO_ROOT, env=env, check=False)
    duration = time.perf_counter() - start
    output = (completed.stdout or "") + (completed.stderr or "")
    PYTEST_RAW_LOG.write_text(output, encoding="utf-8")
    return completed.returncode, output, duration


def _supports_inline_execution(selection: TestSelection, extra_args: Sequence[str]) -> bool:
    """Decide whether a lightweight single-target pytest run can execute inline safely."""

    return (
        selection.scope == Scope.PATHS
        and len(selection.targets) == 1
        and not [arg for arg in extra_args if arg != "--"]
    )


def _run_pytest_inline(command: Sequence[str]) -> tuple[int, str, float]:
    """Execute pytest inline for focused single-target selections with wrapper gating."""

    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    if list(command[:3]) != [sys.executable, "-m", "pytest"]:
        raise ValueError("Inline pytest execution requires a canonical pytest command vector.")

    pytest_module = cast(Any, importlib.import_module("pytest"))
    main_callable = cast(Callable[[Sequence[str]], int], pytest_module.main)
    capture = io.StringIO()
    start = time.perf_counter()
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = capture
    sys.stderr = capture
    previous_env = os.environ.get(WRAPPER_ENV_VAR)
    os.environ[WRAPPER_ENV_VAR] = "1"
    try:
        exit_code = int(main_callable(command[3:]))
    finally:
        if previous_env is None:
            os.environ.pop(WRAPPER_ENV_VAR, None)
        else:
            os.environ[WRAPPER_ENV_VAR] = previous_env
        sys.stdout = original_stdout
        sys.stderr = original_stderr
    duration = time.perf_counter() - start
    output = capture.getvalue()
    PYTEST_RAW_LOG.write_text(output, encoding="utf-8")
    return exit_code, output, duration


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the pytest runner."""

    parser = argparse.ArgumentParser(description="Run pytest with canonical summary output.", allow_abbrev=False)
    parser.add_argument("--pattern", help="Pytest -k expression for targeted selection.")
    parser.add_argument("--select", action="append", default=[], help="Explicit test path or nodeid.")
    parser.add_argument("--profile", help="Optional curated test profile name.")
    parser.add_argument(
        "--scope",
        choices=["auto", *(scope.value for scope in Scope)],
        default="auto",
        help="Execution scope: auto, all, paths, or changed.",
    )
    parser.add_argument("--diff-target", default="HEAD", help="Git reference used for --scope changed.")
    add_include_untracked_argument(parser, help_text="Include untracked files when resolving --scope changed.")
    parser.add_argument("--durations", type=int, default=DEFAULT_DURATIONS, help="Number of slow tests to report.")
    parser.add_argument(
        "--duration-threshold",
        type=float,
        default=DEFAULT_DURATIONS_MIN,
        help="Minimum runtime in seconds for slow-test reporting.",
    )
    parser.add_argument("--maxfail", type=int, default=DEFAULT_MAXFAIL, help="Abort after this many failures.")
    parser.add_argument(
        "--skip-dependency-check",
        action="store_true",
        help="Skip verification that pytest tooling is installed.",
    )
    parser.add_argument("pytest_args", nargs=argparse.REMAINDER, help="Additional arguments passed to pytest.")
    return parser.parse_args()


def main() -> int:
    """Execute the test suite workflow and write summary artifacts."""

    args = parse_args()
    select_paths = list(args.select)
    if args.profile:
        profile_name = args.profile.lower()
        if profile_name == "full":
            select_paths.clear()
        else:
            select_paths.extend(_load_profile(profile_name))

    selection = resolve_selection(
        scope_value=args.scope,
        select_paths=select_paths,
        pattern=args.pattern,
        diff_target=args.diff_target,
        include_untracked=args.include_untracked,
    )

    if selection.targets:
        print(
            f"Resolved execution scope: {selection.scope.value} with {len(selection.targets)} target"
            f"{'s' if len(selection.targets) != 1 else ''}."
        )
    else:
        print(f"Resolved execution scope: {selection.scope.value} (full suite).")

    if not args.skip_dependency_check:
        _ensure_test_toolchain()
    else:
        print("Dependency verification skipped.")

    command = _build_pytest_command(
        selection,
        durations=args.durations,
        duration_threshold=args.duration_threshold,
        max_fail=args.maxfail,
        extra_args=list(args.pytest_args),
    )

    if _supports_inline_execution(selection, args.pytest_args):
        print("Using inline pytest execution for a lightweight single-target run.")
        exit_code, output, duration = _run_pytest_inline(command)
    else:
        exit_code, output, duration = _run_pytest(command)

    status = "PASSED" if exit_code == 0 else "FAILED"
    label = f"slow tests >= {args.duration_threshold:.2f}s"
    summary_lines = [_format_banner(label)]
    trimmed_output = output.rstrip()
    if trimmed_output:
        summary_lines.append(trimmed_output)
    summary_lines.append(_format_banner(f"Pytest suite {status}"))
    summary_lines.append(
        f"Pytest suite {status} in {duration:.2f}s (wall clock). Copy this block into PR notes or review summaries."
    )
    summary_text = "\n".join(summary_lines) + "\n"
    PYTEST_SUMMARY.write_text(summary_text, encoding="utf-8")
    print(summary_text)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
