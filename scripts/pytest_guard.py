#!/usr/bin/env python3
"""Guardrail that enforces wrapper-first pytest execution."""

from __future__ import annotations

import textwrap

WRAPPER_ENV_VAR = "MODERN_PROMETHEUS_WRAPPED_PYTEST"


def render_pytest_wrapper_warning(*, width: int = 88) -> str:
    """Render the warning that redirects direct pytest usage to the canonical test wrapper."""

    intro = (
        "Direct pytest invocation is disabled for this repository. "
        "Run tests through scripts/run_tests.py so scope resolution and summary artifacts stay consistent."
    )
    diagnostic = f"Wrapper gate environment variable: {WRAPPER_ENV_VAR}=1."
    commands = (
        "python scripts/run_tests.py --scope paths --select <test-path-or-nodeid>",
        "python scripts/run_tests.py --scope changed --diff-target <ref>",
        "python scripts/run_tests.py",
    )
    lines = [textwrap.fill(intro, width=width), "", diagnostic, "", "Recommended commands:"]
    lines.extend(f"  • {command}" for command in commands)
    return "\n".join(lines)
