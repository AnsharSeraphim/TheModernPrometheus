#!/usr/bin/env python3
"""Scan the repository for merge-conflict markers and a few common hygiene issues."""

from __future__ import annotations

import ast
import sys
from collections.abc import Iterable
from pathlib import Path

MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
_SKIP_PARTS = {".git", "__pycache__", "build", "dist", ".venv", "venv", "node_modules"}


def iter_files(root: Path) -> Iterable[Path]:
    """Yield files under ``root`` while skipping generated directories."""

    for path in root.rglob("*"):
        if any(part in _SKIP_PARTS for part in path.parts):
            continue
        if path.is_file() and path.resolve() != Path(__file__).resolve():
            yield path


def find_conflict_markers(path: Path) -> list[str]:
    """Locate merge-conflict marker diagnostics within a repository text file."""

    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return errors
    for line_number, line in enumerate(lines, start=1):
        for marker in MARKERS:
            if marker in line:
                errors.append(f"{path}:{line_number} contains merge conflict marker '{marker}'")
    return errors


def find_duplicate_top_level_definitions(path: Path) -> list[str]:
    """Detect repeated top-level Python class or function definitions in one file."""

    if path.suffix != ".py":
        return []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return []

    seen: dict[str, int] = {}
    errors: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name in seen:
                errors.append(f"{path}:{node.lineno} duplicate definition of '{node.name}'")
            else:
                seen[node.name] = node.lineno
    return errors


def find_python_whitespace_issues(path: Path) -> list[str]:
    """Detect Python trailing whitespace and indentation-style inconsistencies in one file."""

    if path.suffix != ".py":
        return []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []

    indent_style: str | None = None
    errors: list[str] = []
    for line_number, line in enumerate(lines, start=1):
        if line.rstrip(" \t") != line:
            errors.append(f"{path}:{line_number} trailing whitespace")
        stripped = line.lstrip(" \t")
        indent = line[: len(line) - len(stripped)]
        if not indent:
            continue
        if "\t" in indent and " " in indent:
            errors.append(f"{path}:{line_number} mixed tabs and spaces indentation")
            continue
        style = "tabs" if "\t" in indent else "spaces"
        if indent_style is None:
            indent_style = style
        elif indent_style != style:
            errors.append(f"{path}:{line_number} uses {style} but file started with {indent_style}")
    return errors


def main(argv: list[str]) -> int:
    """Execute the repository hygiene scan for conflicts, duplicates, and whitespace issues."""

    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[1]
    errors: list[str] = []
    for file_path in iter_files(root):
        errors.extend(find_conflict_markers(file_path))
        errors.extend(find_duplicate_top_level_definitions(file_path))
        errors.extend(find_python_whitespace_issues(file_path))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(
            f"Found {len(errors)} potential merge conflicts, duplicates, or whitespace issues.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
