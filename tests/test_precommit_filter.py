"""Tests for pre-commit manifest filtering state transitions."""

from __future__ import annotations

from pathlib import Path

from scripts.precommit_filter import FilterMetadata, FilterMode, PrecommitFilter


def test_targeted_run_resets_skip_flags() -> None:
    """Reset skip flags for explicitly targeted files before rerunning the selected hook."""
    precommit_filter = PrecommitFilter(mode=FilterMode.AUTO)
    precommit_filter.configure_checks({"ruff-format": FilterMetadata(hook_id="ruff-format")})
    precommit_filter.set_hook_state("ruff-format", {"scripts/run_tests.py": True})
    precommit_filter.set_targeted_paths((Path("scripts/run_tests.py"),))

    selected, should_run, note = precommit_filter.determine_paths(
        "ruff-format",
        (Path("scripts/run_tests.py"),),
    )

    if should_run is not True:
        raise AssertionError("Expected the targeted hook to run.")
    if note is not None:
        raise AssertionError(f"Did not expect a skip note: {note}")
    if selected != (Path("scripts/run_tests.py"),):
        raise AssertionError(f"Unexpected selected paths: {selected!r}")
    hook_state = precommit_filter.get_hook_state("ruff-format")
    if hook_state["scripts/run_tests.py"] is not False:
        raise AssertionError("Targeted runs should reset the skip flag.")


def test_reset_all_flags_rebuilds_inventory() -> None:
    """Rebuild hook state from the tracked inventory during baseline reset operations."""
    precommit_filter = PrecommitFilter(mode=FilterMode.AUTO)
    precommit_filter.configure_checks({"pyright": FilterMetadata(hook_id="pyright", global_hook=True)})
    precommit_filter.set_inventory((Path("scripts/run_tests.py"),))
    precommit_filter.set_hook_state("pyright", {"scripts/old.py": True, "<GLOBAL>": True})

    precommit_filter.reset_all_flags()

    expected = {"scripts/run_tests.py": False, "<GLOBAL>": False}
    if precommit_filter.get_hook_state("pyright") != expected:
        raise AssertionError("Baseline reset did not rebuild the expected manifest state.")
