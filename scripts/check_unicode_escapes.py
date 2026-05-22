#!/usr/bin/env python3
"""Enforce UTF-8 text encoding and reject symbolic Unicode escape literals."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# pylint: disable=wrong-import-position
from scripts._automation_shared import run_command

# pylint: enable=wrong-import-position

REPO_ROOT = Path(__file__).resolve().parent.parent
ESCAPE_PATTERN = re.compile(r"\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8}")
SCANNED_SUFFIXES = {".py", ".pyi", ".md", ".txt", ".json", ".toml", ".yaml", ".yml", ".ini", ".cfg"}
DEFAULT_EXCLUDES = {
    Path("scripts/check_unicode_escapes.py"),
    Path("scripts/remediate_unicode_escapes.py"),
}


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for repository text-file scanning."""

    parser = argparse.ArgumentParser(
        description=(
            "Check repository text assets for invalid UTF-8 payloads and Unicode escape literals "
            "(for example \\u2192) that should be stored as UTF-8 characters."
        ),
        allow_abbrev=False,
    )
    parser.add_argument("--paths", nargs="*", default=[], help="Optional repository-relative paths to scan.")
    return parser.parse_args()


def _tracked_files() -> list[Path]:
    """Enumerate git-tracked files used as default text-encoding scan candidates."""

    completed = run_command(["git", "ls-files"], cwd=REPO_ROOT, check=False)
    if completed.returncode != 0:
        return []
    files: list[Path] = []
    for line in (completed.stdout or "").splitlines():
        line = line.strip()
        if line:
            files.append(Path(line))
    return files


def _resolve_candidates(paths: list[str]) -> list[Path]:
    """Resolve explicit path inputs or tracked defaults to scannable text assets."""

    if paths:
        candidates: list[Path] = []
        for raw in paths:
            rel = Path(raw)
            if rel.is_absolute():
                try:
                    rel = rel.relative_to(REPO_ROOT)
                except ValueError:
                    continue
            if rel in DEFAULT_EXCLUDES:
                continue
            full = REPO_ROOT / rel
            if full.is_file() and full.suffix in SCANNED_SUFFIXES:
                candidates.append(rel)
            elif full.is_dir():
                candidates.extend(
                    sub.relative_to(REPO_ROOT)
                    for sub in sorted(full.rglob("*"))
                    if sub.is_file() and sub.suffix in SCANNED_SUFFIXES
                )
        return sorted(set(candidates))

    tracked = _tracked_files()
    return sorted(
        {
            path
            for path in tracked
            if path.suffix in SCANNED_SUFFIXES and path not in DEFAULT_EXCLUDES and (REPO_ROOT / path).is_file()
        }
    )


def scan_candidates(candidates: list[Path]) -> tuple[dict[Path, tuple[int, int]], dict[Path, list[int]]]:
    """Inspect candidate text assets for invalid UTF-8 bytes and symbolic Unicode escapes."""

    invalid_utf8: dict[Path, tuple[int, int]] = {}
    escaped_unicode: dict[Path, list[int]] = {}

    for path in candidates:
        payload = (REPO_ROOT / path).read_bytes()
        try:
            content = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            invalid_utf8[path] = (exc.start, exc.end)
            continue

        line_hits: list[int] = []
        for idx, line in enumerate(content.splitlines(), start=1):
            if ESCAPE_PATTERN.search(line):
                line_hits.append(idx)
        if line_hits:
            escaped_unicode[path] = line_hits

    return invalid_utf8, escaped_unicode


def main() -> int:
    """Execute repository text-encoding checks and print remediation guidance on failure."""

    args = parse_args()
    candidates = _resolve_candidates(list(args.paths))

    invalid_utf8, escaped_unicode = scan_candidates(candidates)

    if not invalid_utf8 and not escaped_unicode:
        print("UTF-8 and Unicode escape check passed.")
        return 0

    print("UTF-8 / Unicode policy violation detected.")
    print("Remediation helper:")
    print("  python scripts/remediate_unicode_escapes.py --paths <file1> <file2>")

    if invalid_utf8:
        print("Files with invalid UTF-8 bytes:")
        for path, (start, end) in sorted(invalid_utf8.items()):
            print(f"- {path.as_posix()}: byte range {start}-{end}")

    if escaped_unicode:
        print("Files with symbolic Unicode escape literals (use UTF-8 symbols directly):")
        for path, lines in sorted(escaped_unicode.items()):
            joined = ", ".join(str(number) for number in lines[:10])
            extra = "" if len(lines) <= 10 else f" (+{len(lines) - 10} more)"
            print(f"- {path.as_posix()}: lines {joined}{extra}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
