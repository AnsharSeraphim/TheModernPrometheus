"""Tests for the Markdown docstring audit inventory helper."""

from __future__ import annotations

from pathlib import Path

from scripts.audit_docstrings import build_inventory_markdown, collect_docstrings


def test_collect_docstrings_skips_excluded_directories(tmp_path: Path) -> None:
    """Collector excludes Python files beneath directories like build/ and .venv/."""

    included = tmp_path / "module.py"
    excluded_dir = tmp_path / "build"
    excluded_dir.mkdir()
    excluded = excluded_dir / "ignored.py"

    included.write_text('"""Included module."""\n', encoding="utf-8")
    excluded.write_text('"""Excluded module."""\n', encoding="utf-8")

    collected, missing, failures = collect_docstrings(roots=(tmp_path,))

    assert list(collected) == ["module.py"]  # nosec B101
    assert not missing  # nosec B101
    assert not failures  # nosec B101


def test_build_inventory_markdown_includes_symbol_table(tmp_path: Path) -> None:
    """Rendered inventory contains stable Markdown rows for discovered symbols."""

    module_path = tmp_path / "sample.py"
    module_path.write_text(
        '"""Example module."""\n\ndef helper() -> int:\n    """Return one."""\n    return 1\n',
        encoding="utf-8",
    )

    collected, missing, failures = collect_docstrings(roots=(tmp_path,))
    markdown = build_inventory_markdown(collected=collected, missing=missing, failures=failures)

    assert "| `sample.py` | `sample` | module | 1 | Example module. |" in markdown  # nosec B101
    assert "| `sample.py` | `sample.helper` | function | 3 | Return one. |" in markdown  # nosec B101
    assert "## Scan failures" in markdown  # nosec B101


def test_build_inventory_markdown_marks_incomplete_when_scan_failures_exist(tmp_path: Path) -> None:
    """Coverage summary marks inventory incomplete when scan failures are present."""

    good_path = tmp_path / "good.py"
    bad_path = tmp_path / "bad.py"
    good_path.write_text('"""Good module."""\n', encoding="utf-8")
    bad_path.write_text("def broken(:\n", encoding="utf-8")

    collected, missing, failures = collect_docstrings(roots=(tmp_path,))
    markdown = build_inventory_markdown(collected=collected, missing=missing, failures=failures)

    assert "Coverage status: INCOMPLETE" in markdown  # nosec B101
    assert "`bad.py`" in markdown  # nosec B101
