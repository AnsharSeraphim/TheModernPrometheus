"""Tests for the docstring catalog aggregation helper."""

from __future__ import annotations

from pathlib import Path
from typing import cast

from scripts.aggregate_project_docstrings import build_catalog


def test_build_catalog_reports_missing_and_flagged_docstrings(tmp_path: Path) -> None:
    """Aggregate summary reflects missing and weak docstring findings."""

    module_path = tmp_path / "sample_module.py"
    module_path.write_text(
        '"""Sample module narrative."""\n\n'
        "def documented() -> int:\n"
        '    """Run quickly."""\n'
        "    return 1\n\n"
        "def undocumented() -> None:\n"
        "    return None\n",
        encoding="utf-8",
    )

    payload = build_catalog(root=tmp_path, excluded_roots=set())

    summary = cast(dict[str, object], payload["summary"])
    assert summary["python_files"] == 1  # nosec B101
    assert summary["missing_docstrings"] == 1  # nosec B101
    assert summary["flagged_docstrings"] == 1  # nosec B101
    assert summary["quality_status"] == "needs_review"  # nosec B101


def test_build_catalog_excludes_requested_roots(tmp_path: Path) -> None:
    """Excluded top-level directories are skipped during catalog scans."""

    included = tmp_path / "included.py"
    excluded_dir = tmp_path / "build"
    excluded_dir.mkdir()
    excluded = excluded_dir / "ignored.py"

    included.write_text('"""Included module."""\n', encoding="utf-8")
    excluded.write_text('"""Excluded module."""\n', encoding="utf-8")

    payload = build_catalog(root=tmp_path, excluded_roots={"build"})
    files = cast(list[dict[str, object]], payload["files"])

    assert len(files) == 1  # nosec B101
    assert files[0]["filename"] == "included.py"  # nosec B101
