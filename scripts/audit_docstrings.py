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


class _DocstringCollector(ast.NodeVisitor):
    """Collect module, class, and function docstrings from an AST."""

    def __init__(self, module_path: str) -> None:
        """Initialize collector state for one module path."""

        self._module_path = module_path
        self._stack: list[str] = []
        self.entries: list[DocstringEntry] = []

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
    """Return True when the path includes an excluded directory name."""

    return any(part in EXCLUDED_DIRECTORY_NAMES for part in path.parts)


def _iter_python_files(*, roots: tuple[Path, ...]) -> list[Path]:
    """Return sorted Python files found beneath the configured scan roots."""

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
    """Return a stable display path relative to repository or requested scan roots."""

    if file_path.is_relative_to(REPO_ROOT):
        return file_path.relative_to(REPO_ROOT).as_posix()
    for root in roots:
        if root.is_dir() and file_path.is_relative_to(root):
            return file_path.relative_to(root).as_posix()
        if root.is_file() and file_path == root:
            return root.name
    return file_path.as_posix()


def collect_docstrings(*, roots: tuple[Path, ...]) -> dict[str, list[DocstringEntry]]:
    """Collect all docstring entries grouped by relative Python file path."""

    collected: dict[str, list[DocstringEntry]] = {}
    for file_path in _iter_python_files(roots=roots):
        relative_path = _relative_display_path(file_path=file_path, roots=roots)
        tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=relative_path)
        module_symbol = relative_path.removesuffix(".py").replace("/", ".")
        collector = _DocstringCollector(module_path=module_symbol)
        collector.visit(tree)
        if collector.entries:
            collected[relative_path] = collector.entries
    return collected


def build_inventory_markdown(*, collected: dict[str, list[DocstringEntry]]) -> str:
    """Render the docstring inventory as Markdown with stable section ordering."""

    lines = [
        "# Programmatic Docstring Inventory",
        "",
        "Generated for documentation parity audits. Delete or regenerate this file after the audit session.",
        "",
    ]
    if not collected:
        lines.append("No docstrings were found in the selected scan roots.")
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            "| File | Symbol | Kind | Line | Summary |",
            "| --- | --- | --- | ---: | --- |",
        ]
    )
    for relative_path, entries in sorted(collected.items()):
        for entry in entries:
            summary = entry.docstring.splitlines()[0].replace("|", "\\|")
            lines.append(f"| `{relative_path}` | `{entry.symbol}` | {entry.kind} | {entry.line_number} | {summary} |")
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
    collected = collect_docstrings(roots=roots)
    output_path = args.output.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_inventory_markdown(collected=collected), encoding="utf-8")
    print(f"Wrote docstring inventory to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
