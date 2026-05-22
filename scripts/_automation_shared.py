"""Shared helpers for repository automation scripts."""

from __future__ import annotations

import re
import subprocess  # nosec B404 - controlled local tooling commands only
import sys
from argparse import ArgumentParser
from collections.abc import Callable, Iterable, Mapping, Sequence
from pathlib import Path
from typing import cast


def _expect_table(source: Mapping[str, object], key: str, error: str) -> dict[str, object]:
    """Validate that a TOML key contains the nested table required by automation loaders."""

    value = source.get(key)
    if isinstance(value, dict):
        return cast(dict[str, object], value)
    raise SystemExit(error)


def _expect_list(source: Mapping[str, object], key: str, error: str) -> list[object]:
    """Validate that a TOML key contains the list required by automation loaders."""

    value = source.get(key)
    if isinstance(value, list):
        return cast(list[object], value)
    raise SystemExit(error)


def load_dev_dependency_specs(
    *,
    pyproject_path: Path,
    toml_loader: Callable[[str], dict[str, object]],
    missing_optional_error: str,
    missing_group_error: str,
) -> dict[str, str]:
    """Extract normalized package specifiers from the project dev dependency group."""

    if not pyproject_path.exists():
        raise SystemExit("pyproject.toml is missing; cannot resolve development dependencies.")

    raw_data = toml_loader(pyproject_path.read_text(encoding="utf-8"))
    project_table = _expect_table(raw_data, "project", "Expected a [project] table in pyproject.toml.")
    optional_table = _expect_table(project_table, "optional-dependencies", missing_optional_error)
    dev_items = _expect_list(optional_table, "dev", missing_group_error)

    pattern = re.compile(r"^([A-Za-z0-9_.-]+)")
    mapping: dict[str, str] = {}
    for entry in dev_items:
        if not isinstance(entry, str):
            continue
        match = pattern.match(entry)
        if match is not None:
            mapping[match.group(1).lower()] = entry
    return mapping


def resolve_missing_dependencies(
    *,
    required_modules: Mapping[str, str],
    dependency_map: Mapping[str, str],
    find_spec: Callable[[str], object | None],
) -> tuple[list[str], list[str]]:
    """Resolve unavailable runtime modules into installable dev dependency specifiers."""

    missing: list[str] = []
    unresolved: list[str] = []
    for package_name, module_name in required_modules.items():
        if find_spec(module_name) is not None:
            continue
        spec = dependency_map.get(package_name)
        if spec is None:
            unresolved.append(package_name)
            continue
        missing.append(spec)
    return missing, unresolved


def raise_for_unresolved_dependencies(unresolved: Sequence[str], *, error_template: str) -> None:
    """Raise ``SystemExit`` if required packages were not declared in ``pyproject.toml``."""

    if not unresolved:
        return
    raise SystemExit(error_template.format(packages=", ".join(sorted(unresolved))))


def gather_missing_dependencies(
    *,
    required_modules: Mapping[str, str],
    dependency_map: Mapping[str, str],
    find_spec: Callable[[str], object | None],
    unresolved_error_template: str,
) -> list[str]:
    """Collect installable dependency specifiers and fail on undeclared required packages."""

    missing, unresolved = resolve_missing_dependencies(
        required_modules=required_modules,
        dependency_map=dependency_map,
        find_spec=find_spec,
    )
    raise_for_unresolved_dependencies(unresolved, error_template=unresolved_error_template)
    return missing


def build_pip_install_command(packages: Sequence[str]) -> list[str]:
    """Compose the interpreter-local pip command used for toolchain self-installation."""

    return [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--root-user-action=ignore",
        "--upgrade-strategy",
        "only-if-needed",
        *packages,
    ]


def run_command(
    command: Sequence[str],
    *,
    cwd: Path,
    env: Mapping[str, str] | None = None,
    check: bool = False,
    capture_output: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Execute ``command`` with predictable text-mode defaults."""

    completed = subprocess.run(
        list(command),
        cwd=str(cwd),
        env=dict(env) if env is not None else None,
        check=check,
        capture_output=capture_output,
        text=True,
    )  # nosec B603 - command vectors are repository-controlled
    return completed


def normalize_repository_paths(lines: Iterable[str], *, repo_root: Path) -> list[Path]:
    """Normalize raw path strings into existing repository-relative paths."""

    normalized: set[Path] = set()
    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            continue
        candidate = Path(stripped)
        if candidate.is_absolute():
            try:
                candidate = candidate.relative_to(repo_root)
            except ValueError:
                continue
        full_path = repo_root / candidate
        if full_path.exists():
            normalized.add(candidate)
    return sorted(normalized)


def build_git_diff_commands(diff_target: str, *, include_untracked: bool) -> list[list[str]]:
    """Compose git queries that enumerate changed, staged, and optional untracked files."""

    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMRTUXB", diff_target],
        ["git", "diff", "--name-only", "--diff-filter=ACMRTUXB", "--staged"],
    ]
    if include_untracked:
        commands.append(["git", "ls-files", "--others", "--exclude-standard"])
    return commands


def add_include_untracked_argument(parser: ArgumentParser, *, help_text: str) -> None:
    """Register the shared ``--include-untracked`` flag."""

    parser.add_argument("--include-untracked", action="store_true", help=help_text)
