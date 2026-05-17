"""Tests for UTF-8 and escaped-Unicode policy diagnostics."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts import check_unicode_escapes as unicode_check


def test_scan_candidates_flags_escape_literals(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Report symbolic ``\\u`` escapes as violations without flagging UTF-8 decode errors."""
    file_path = tmp_path / "sample.md"
    escape_literal = "\\" + "u2192"
    file_path.write_text(f"Arrow: {escape_literal}\n", encoding="utf-8")

    monkeypatch.setattr(unicode_check, "REPO_ROOT", tmp_path)

    invalid_utf8, escaped_unicode = unicode_check.scan_candidates([Path("sample.md")])

    if invalid_utf8:
        raise AssertionError(f"Did not expect UTF-8 decode failures: {invalid_utf8}")
    if escaped_unicode != {Path("sample.md"): [1]}:
        raise AssertionError(f"Unexpected escaped Unicode hits: {escaped_unicode}")


def test_scan_candidates_flags_invalid_utf8_bytes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Report decode failures for invalid UTF-8 bytes and no escape-literal findings."""
    file_path = tmp_path / "bad.txt"
    file_path.write_bytes(b"\xff\xfe")

    monkeypatch.setattr(unicode_check, "REPO_ROOT", tmp_path)

    invalid_utf8, escaped_unicode = unicode_check.scan_candidates([Path("bad.txt")])

    if Path("bad.txt") not in invalid_utf8:
        raise AssertionError("Expected an invalid UTF-8 entry for bad.txt.")
    if escaped_unicode:
        raise AssertionError(f"Did not expect escaped Unicode findings: {escaped_unicode}")
