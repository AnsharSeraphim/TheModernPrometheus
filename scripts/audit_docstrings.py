#!/usr/bin/env python3
"""Build a Markdown docstring inventory for documentation-versus-implementation audits."""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path

DocstringNode = ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_PATH = REPO_ROOT / "build" / "automation_contract" / "docstring_inventory.md"
DEFAULT_SCAN_ROOTS = (REPO_ROOT / "scripts", REPO_ROOT / "tests")
EXCLUDED_DIRECTORY_NAMES = {".git", ".venv", "build", "dist", "__pycache__"}


@dataclass(frozen=True)
class DocstringEntry:
    """Represent one discovered docstring with location metadata."""

    symbol: str
    kind: str
    line_number: int
    docstring: str


@dataclass(frozen=True)
class MissingDocstringEntry:
    """Represent one module/class/function symbol that lacks a docstring."""

    symbol: str
    kind: str
    line_number: int


@dataclass(frozen=True)
class ScanFailureEntry:
    """Represent one file-level parse/read failure encountered during scanning."""

    file_path: str
    error_type: str
    message: str


class _DocstringCollector(ast.NodeVisitor):
    """Collect module, class, and function docstrings from an AST."""

    def __init__(self, module_path: str) -> None:
        """Initialize collector state for one module path."""

        self._module_path = module_path
        self._stack: list[str] = []
        self.entries: list[DocstringEntry] = []
        self.missing_entries: list[MissingDocstringEntry] = []

    def visit_Module(self, node: ast.Module) -> None:  # noqa: N802  # pylint: disable=invalid-name
        """Visit a module node and capture its docstring."""

        self._record_docstring(node=node, kind="module", name=self._module_path)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802  # pylint: disable=invalid-name
        """Visit a class node and capture class-level docstrings."""

        self._visit_symbol_node(node=node, kind="class")

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802  # pylint: disable=invalid-name
        """Visit a function node and capture function docstrings."""

        self._visit_symbol_node(node=node, kind="function")

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802  # pylint: disable=invalid-name
        """Visit an async function node and capture function docstrings."""

        self._visit_symbol_node(node=node, kind="function")

    def _visit_symbol_node(self, *, node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef, kind: str) -> None:
        """Capture one non-module symbol and recurse into its children."""

        self._stack.append(node.name)
        try:
            dotted_name = ".".join((self._module_path, *self._stack))
            self._record_docstring(node=node, kind=kind, name=dotted_name)
            self.generic_visit(node)
        finally:
            self._stack.pop()

    def _record_docstring(self, *, node: DocstringNode, kind: str, name: str) -> None:
        """Record a docstring entry for the provided AST node when present."""

        docstring = ast.get_docstring(node)
        if not docstring:
            self.missing_entries.append(
                MissingDocstringEntry(symbol=name, kind=kind, line_number=getattr(node, "lineno", 1))
            )
            return
        self.entries.append(
            DocstringEntry(
                symbol=name,
                kind=kind,
                line_number=getattr(node, "lineno", 1),
                docstring=docstring.strip(),
            )
        )


def _is_excluded(path: Path) -> bool:
    """Identify paths that pass through directories excluded from docstring inventory scans."""

    return any(part in EXCLUDED_DIRECTORY_NAMES for part in path.parts)


def _iter_python_files(*, roots: tuple[Path, ...]) -> list[Path]:
    """Enumerate sorted Python files beneath the configured audit scan roots."""

    files: list[Path] = []
    for root in roots:
        if _is_excluded(root):
            continue
        if root.is_file() and root.suffix == ".py":
            files.append(root)
            continue
        if root.is_dir():
            files.extend(path for path in root.rglob("*.py") if not _is_excluded(path))
    return sorted(files)


def _relative_display_path(*, file_path: Path, roots: tuple[Path, ...]) -> str:
    """Derive stable inventory display paths for repository and ad hoc scan roots."""

    if file_path.is_relative_to(REPO_ROOT):
        return file_path.relative_to(REPO_ROOT).as_posix()
    for root in roots:
        if root.is_dir() and file_path.is_relative_to(root):
            return file_path.relative_to(root).as_posix()
        if root.is_file() and file_path == root:
            return root.name
    return file_path.as_posix()


def collect_docstrings(
    *, roots: tuple[Path, ...]
) -> tuple[dict[str, list[DocstringEntry]], dict[str, list[MissingDocstringEntry]], list[ScanFailureEntry]]:
    """Collect present and missing docstring entries grouped by relative Python file path."""

    collected: dict[str, list[DocstringEntry]] = {}
    missing: dict[str, list[MissingDocstringEntry]] = {}
    failures: list[ScanFailureEntry] = []
    for file_path in _iter_python_files(roots=roots):
        relative_path = _relative_display_path(file_path=file_path, roots=roots)
        try:
            tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=relative_path)
        except (OSError, UnicodeDecodeError, SyntaxError) as error:
            failures.append(
                ScanFailureEntry(
                    file_path=relative_path,
                    error_type=type(error).__name__,
                    message=str(error).strip(),
                )
            )
            continue
        module_symbol = relative_path.removesuffix(".py").replace("/", ".")
        collector = _DocstringCollector(module_path=module_symbol)
        collector.visit(tree)
        if collector.entries:
            collected[relative_path] = collector.entries
        if collector.missing_entries:
            missing[relative_path] = collector.missing_entries
    return collected, missing, failures


def build_inventory_markdown(
    *,
    collected: dict[str, list[DocstringEntry]],
    missing: dict[str, list[MissingDocstringEntry]],
    failures: list[ScanFailureEntry],
) -> str:
    """Render docstring inventory markdown with present/missing coverage context."""

    lines = [
        "# Programmatic Docstring Inventory",
        "",
        "Generated for documentation parity audits. Delete or regenerate this file after the audit session.",
        "",
    ]
    total_documented = sum(len(entries) for entries in collected.values())
    total_missing = sum(len(entries) for entries in missing.values())
    total_symbols = total_documented + total_missing
    failed_files = len(failures)

    if failed_files:
        lines.extend(
            [
                f"Coverage summary: documented {total_documented}/{total_symbols} analyzed symbols "
                f"({((total_documented / total_symbols * 100) if total_symbols else 100):.2f}%).",
                f"Coverage status: INCOMPLETE ({failed_files} file(s) failed scanning).",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "Coverage summary: documented "
                f"{total_documented}/{total_symbols} symbols ({((total_documented / total_symbols * 100) if total_symbols else 100):.2f}%).",
                "Coverage status: COMPLETE (all scanned files parsed successfully).",
                "",
            ]
        )

    if not collected:
        lines.append("No docstrings were found in the selected scan roots.")
    else:
        lines.extend(
            [
                "| File | Symbol | Kind | Line | Summary |",
                "| --- | --- | --- | ---: | --- |",
            ]
        )
        for relative_path, entries in sorted(collected.items()):
            for entry in entries:
                summary = entry.docstring.splitlines()[0].replace("|", "\\|")
                lines.append(
                    f"| `{relative_path}` | `{entry.symbol}` | {entry.kind} | {entry.line_number} | {summary} |"
                )
        lines.append("")

    lines.append("## Missing docstrings")
    lines.append("")
    if not missing:
        lines.append("No missing module/class/function docstrings were detected.")
        lines.append("")
    else:
        lines.extend(["| File | Symbol | Kind | Line |", "| --- | --- | --- | ---: |"])
        for relative_path, missing_entries in sorted(missing.items()):
            for missing_entry in missing_entries:
                lines.append(
                    f"| `{relative_path}` | `{missing_entry.symbol}` | {missing_entry.kind} | {missing_entry.line_number} |"
                )
        lines.append("")
        lines.append(
            "When interrogate fails in the pre-commit wrapper, rerun this script and convert the missing-symbol rows into "
            "granular checklist remediation entries in `Final-Productization-Checklist.md`."
        )
        lines.append("")
    lines.append("## Scan failures")
    lines.append("")
    if not failures:
        lines.append("No scan/parsing failures were detected.")
        lines.append("")
        return "\n".join(lines)

    lines.extend(["| File | Error | Details |", "| --- | --- | --- |"])
    for failure_entry in failures:
        lines.append(
            f"| `{failure_entry.file_path}` | {failure_entry.error_type} | {failure_entry.message.replace('|', '\\|')} |"
        )
    lines.append("")
    lines.append("Resolve scan failures first; symbols in failed files are excluded from coverage tables above.")
    lines.append("")
    return "\n".join(lines)


def _parse_args() -> argparse.Namespace:
    """Parse CLI flags for scan roots and output path overrides."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scan-root",
        action="append",
        dest="scan_roots",
        default=None,
        help="Optional file or directory to scan (repeatable). Defaults to scripts and tests.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Markdown output path for the generated inventory.",
    )
    return parser.parse_args()


def main() -> int:
    """Generate a Markdown inventory of discovered docstrings."""

    args = _parse_args()
    roots = tuple(Path(path).resolve() for path in args.scan_roots) if args.scan_roots else DEFAULT_SCAN_ROOTS
    collected, missing, failures = collect_docstrings(roots=roots)
    output_path = args.output.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        build_inventory_markdown(collected=collected, missing=missing, failures=failures),
        encoding="utf-8",
    )
    print(f"Wrote docstring inventory to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
