from __future__ import annotations

from scripts.manual_hook_warning import render_manual_hook_usage


def test_manual_hook_warning_mentions_runner() -> None:
    message = render_manual_hook_usage("ruff-format")

    if "scripts/run_precommit_suite.py" not in message:
        raise AssertionError("Expected the advisory to reference the unified runner.")
    if "ruff-format" not in message:
        raise AssertionError("Expected the advisory to mention the hook id.")
