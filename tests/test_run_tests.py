"""Tests for test-scope selection behavior in the wrapper runner."""

from __future__ import annotations

from scripts.run_tests import Scope, resolve_selection


def test_resolve_selection_uses_paths_for_explicit_select() -> None:
    """Prefer explicit path targeting when ``--select`` arguments are supplied."""
    selection = resolve_selection(
        scope_value="auto",
        select_paths=["tests/test_run_tests.py"],
        pattern=None,
        diff_target="HEAD",
        include_untracked=False,
    )

    if selection.scope is not Scope.PATHS:
        raise AssertionError(f"Expected Scope.PATHS, received {selection.scope!r}.")
    if selection.targets != ["tests/test_run_tests.py"]:
        raise AssertionError(f"Unexpected explicit targets: {selection.targets!r}.")


def test_resolve_selection_uses_all_when_no_selectors() -> None:
    """Fallback to full-suite execution when no selector inputs are provided."""
    selection = resolve_selection(
        scope_value="auto",
        select_paths=[],
        pattern=None,
        diff_target="HEAD",
        include_untracked=False,
    )

    if selection.scope is not Scope.ALL:
        raise AssertionError(f"Expected Scope.ALL, received {selection.scope!r}.")
    if selection.targets:
        raise AssertionError(f"Expected no explicit targets, received {selection.targets!r}.")
