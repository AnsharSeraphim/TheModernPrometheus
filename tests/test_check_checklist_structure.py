"""Tests for checklist structure validation utility."""

from __future__ import annotations

from pathlib import Path

from scripts.check_checklist_structure import validate_checklist


def test_validate_checklist_passes_for_required_sections(tmp_path: Path) -> None:
    """Validation succeeds when all required snippets are present."""

    checklist = tmp_path / "Final-Productization-Checklist.md"
    checklist.write_text(
        "\n".join(
            [
                "# **MANDATORY CHECKLIST POLICY**",
                "## Permanent Checklist Entry - *NEVER CLOSE THIS*",
                "### Documentation and Coding Audit",
                "#### Execution quality examples for stateless agents",
                "#### Documentation Parity Rubric (apply per file)",
                "##### Documentation Inventory",
            ]
        ),
        encoding="utf-8",
    )

    assert not validate_checklist(checklist)  # nosec B101


def test_validate_checklist_reports_missing_sections(tmp_path: Path) -> None:
    """Validation reports each required section that is missing."""

    checklist = tmp_path / "Final-Productization-Checklist.md"
    checklist.write_text("# **MANDATORY CHECKLIST POLICY**\n", encoding="utf-8")

    errors = validate_checklist(checklist)

    assert len(errors) == 5  # nosec B101
    assert all("required section is missing" in error for error in errors)  # nosec B101
