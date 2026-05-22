#!/usr/bin/env python3
"""Redirect manual hook invocations to the unified pre-commit runner."""

from __future__ import annotations

import os
import sys
import textwrap
from collections.abc import Iterable

_COMMAND_TEMPLATES: tuple[str, ...] = (
    "python scripts/run_precommit_suite.py --scope paths --paths <file1> <file2>",
    "python scripts/run_precommit_suite.py --only <hook> --scope paths --paths <file1> <file2>",
    "python scripts/run_precommit_suite.py --scope all",
)

_JSON_REMINDER = (
    "Commit any updated JSON ledgers under config/precommit_store/ so future contributors inherit the latest "
    "hook state."
)


def _format_command_block(commands: Iterable[str]) -> str:
    """Format command recommendations as a bullet list block."""

    lines = ["Recommended pre-commit suite commands:"]
    lines.extend(f"  • {command}" for command in commands)
    return "\n".join(lines)


def render_manual_hook_usage(hook_id: str | None, *, width: int = 88) -> str:
    """Render the advisory that redirects direct pre-commit hook usage to the wrapper suite."""

    normalized = hook_id or "quality hook"
    intro = (
        f"The '{normalized}' hook is managed by scripts/run_precommit_suite.py. "
        "Use the unified suite instead of invoking the hook directly so the skip ledger stays in sync."
    )
    body = [textwrap.fill(intro, width=width), "", _format_command_block(_COMMAND_TEMPLATES), ""]
    body.append(textwrap.fill(_JSON_REMINDER, width=width))
    return "\n".join(body)


def main(argv: list[str]) -> int:
    """Print the manual-hook advisory and exit non-zero."""

    hook_id = os.environ.get("PRE_COMMIT_HOOK_ID") or (argv[0] if argv else None)
    print(render_manual_hook_usage(hook_id), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
