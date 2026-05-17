"""Tests for pytest wrapper guard messaging."""

from __future__ import annotations

from scripts.pytest_guard import WRAPPER_ENV_VAR, render_pytest_wrapper_warning


def test_pytest_guard_mentions_wrapper_commands() -> None:
    """Include wrapper execution guidance and diagnostic environment details."""
    message = render_pytest_wrapper_warning()

    if "scripts/run_tests.py" not in message:
        raise AssertionError("Expected wrapper command guidance in pytest warning.")
    if WRAPPER_ENV_VAR not in message:
        raise AssertionError("Expected environment variable to be discoverable in guard output for diagnostics.")
