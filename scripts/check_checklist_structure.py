#!/usr/bin/env python3
"""Validate required checklist governance sections remain intact."""

from __future__ import annotations

import argparse
from pathlib import Path

_REQUIRED_SNIPPETS: tuple[str, ...] = (
    "# **MANDATORY CHECKLIST POLICY**",
    "## Permanent Checklist Entry - *NEVER CLOSE THIS*",
    "### Documentation and Coding Audit",
    "#### Execution quality examples for stateless agents",
    "#### Documentation Parity Rubric (apply per file)",
    "##### Documentation Inventory",
)
_DEFAULT_PATH = Path("Final-Productization-Checklist.md")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for checklist structure validation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--path",
        type=Path,
        default=_DEFAULT_PATH,
        help="Checklist file path to validate (default: Final-Productization-Checklist.md).",
    )
    return parser.parse_args()


def validate_checklist(path: Path) -> list[str]:
    """Identify missing governance sections in the required productization checklist."""

    if not path.exists():
        return [f"Missing checklist file: {path}"]

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for snippet in _REQUIRED_SNIPPETS:
        if snippet not in text:
            errors.append(f"{path}: required section is missing: {snippet}")
    return errors


def main() -> int:
    """Execute checklist structure validation and report the resulting process status."""

    args = parse_args()
    errors = validate_checklist(args.path)
    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"Checklist structure validated: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
