"""Build a monolithic JSON catalog of Python docstrings keyed by filename.

The catalog is designed for export workflows where agents need one payload that captures
module purpose, narrative role context, and all available Python docstrings.
"""

from __future__ import annotations

import argparse
import ast
import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast


@dataclass(frozen=True)
class DocstringEntry:
    """Represent one extracted docstring and its source location metadata."""

    symbol: str
    kind: str
    line: int
    docstring: str


@dataclass(frozen=True)
class FileDocstringRecord:
    """Capture export-ready docstring details for one Python source file."""

    filename: str
    role_description: str
    docstrings: list[DocstringEntry]
    completeness: dict[str, object]
    quality_audit: dict[str, object]


def parse_args() -> argparse.Namespace:
    """Parse CLI options for repository scan and JSON output destination."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repository root to scan for Python files (default: current directory).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("context/project_docstrings_catalog.json"),
        help="Destination JSON file for the monolithic docstring catalog.",
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[".git", ".venv", "build", "dist", "__pycache__"],
        help="Top-level directory names to exclude while scanning.",
    )
    return parser.parse_args()


def _module_role_description(module_docstring: str | None, relative_path: str) -> str:
    """Generate a 1-3 sentence narrative role description for the module entry."""

    module_text = (module_docstring or "").strip()
    if module_text:
        first_line = module_text.splitlines()[0].strip().rstrip(".")
        return (
            f"This module at `{relative_path}` orchestrates a focused part of the repository workflow. "
            f"Its own top-level narration describes it as: {first_line}. "
            "The remaining symbols implement and enforce that responsibility in executable form."
        )
    stem_name = Path(relative_path).stem.replace("_", " ")
    return (
        f"This module at `{relative_path}` contributes {stem_name} behavior to the repository workflow. "
        "The file currently lacks a module-level narrative docstring, so this role description is inferred from "
        "its location and filename."
    )


DocstringNode = ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef


def _iter_symbols(tree: ast.Module) -> list[tuple[str, str, DocstringNode]]:
    """Collect module/class/function symbols in source order for docstring extraction."""

    symbols: list[tuple[str, str, DocstringNode]] = [("module", "module", tree)]

    class Visitor(ast.NodeVisitor):  # pylint: disable=invalid-name
        """Track nesting so extracted symbol names preserve dotted qualification."""

        def __init__(self) -> None:
            """Initialize an empty stack for class/function scope traversal."""
            self.stack: list[str] = []

        def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802  # pylint: disable=invalid-name
            """Record class symbols and recurse into nested members."""
            symbol = ".".join([*self.stack, node.name])
            symbols.append((symbol, "class", node))
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802  # pylint: disable=invalid-name
            """Record sync function symbols and recurse into nested members."""
            symbol = ".".join([*self.stack, node.name])
            symbols.append((symbol, "function", node))
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802  # pylint: disable=invalid-name
            """Record async function symbols and recurse into nested members."""
            symbol = ".".join([*self.stack, node.name])
            symbols.append((symbol, "function", node))
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

    Visitor().visit(tree)
    return symbols


def _quality_notes(text: str) -> list[str]:
    """Return heuristic quality findings for one docstring body."""

    lowered = text.strip().casefold()
    notes: list[str] = []
    if len(text.strip()) < 24:
        notes.append("very_short")
    weak_prefixes = ("run ", "return ", "define ", "model ")
    if lowered.startswith(weak_prefixes):
        notes.append("generic_prefix")
    if lowered.endswith("results.") or lowered.endswith("behavior."):
        notes.append("non_specific_suffix")
    return notes


def _collect_file_record(root: Path, path: Path) -> FileDocstringRecord:
    """Parse one file and return extracted docstrings plus completeness and quality audit."""

    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(path))
    symbols = _iter_symbols(tree)

    entries: list[DocstringEntry] = []
    missing_symbols: list[str] = []
    weak_symbols: list[dict[str, object]] = []

    for symbol, kind, node in symbols:
        docstring = ast.get_docstring(node, clean=True)
        line = 1 if kind == "module" else int(getattr(node, "lineno", 1))
        if docstring is None:
            missing_symbols.append(symbol)
            continue
        quality_flags = _quality_notes(docstring)
        if quality_flags:
            weak_symbols.append({"symbol": symbol, "flags": quality_flags})
        entries.append(DocstringEntry(symbol=symbol, kind=kind, line=line, docstring=docstring))

    relative_path = str(path.relative_to(root))
    module_docstring = ast.get_docstring(tree, clean=True)
    completeness: dict[str, object] = {
        "symbols_total": len(symbols),
        "symbols_with_docstrings": len(entries),
        "missing_symbols": missing_symbols,
        "missing_count": len(missing_symbols),
    }
    quality_audit: dict[str, object] = {
        "flagged_entries": weak_symbols,
        "flagged_count": len(weak_symbols),
        "status": "pass" if not weak_symbols else "needs_review",
    }
    return FileDocstringRecord(
        filename=relative_path,
        role_description=_module_role_description(module_docstring, relative_path),
        docstrings=entries,
        completeness=completeness,
        quality_audit=quality_audit,
    )


def _is_excluded(path: Path, excluded_roots: set[str]) -> bool:
    """Return True when a path should be skipped from the scan."""

    return any(part in excluded_roots for part in path.parts)


def build_catalog(root: Path, excluded_roots: set[str]) -> dict[str, object]:
    """Aggregate all Python docstrings under the repository root into one payload."""

    files = sorted(path for path in root.rglob("*.py") if not _is_excluded(path, excluded_roots))
    records = [_collect_file_record(root, path) for path in files]

    payload_records: list[dict[str, object]] = []
    total_symbols = 0
    total_missing = 0
    total_flagged = 0

    for record in records:
        payload_records.append(
            {
                "filename": record.filename,
                "role_description": record.role_description,
                "docstrings": [
                    {
                        "symbol": entry.symbol,
                        "kind": entry.kind,
                        "line": entry.line,
                        "docstring": entry.docstring,
                    }
                    for entry in record.docstrings
                ],
                "completeness": record.completeness,
                "quality_audit": record.quality_audit,
            }
        )
        total_symbols += cast(int, record.completeness["symbols_total"])
        total_missing += cast(int, record.completeness["missing_count"])
        total_flagged += cast(int, record.quality_audit["flagged_count"])

    return {
        "summary": {
            "python_files": len(records),
            "symbols_total": total_symbols,
            "missing_docstrings": total_missing,
            "flagged_docstrings": total_flagged,
            "quality_status": "pass" if total_flagged == 0 else "needs_review",
        },
        "files": payload_records,
    }


def main() -> int:
    """Generate the catalog and write it as UTF-8 JSON for export."""

    args = parse_args()
    root = args.root.resolve()
    output_path = args.output.resolve()
    payload = build_catalog(root=root, excluded_roots=set(args.exclude))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = cast(dict[str, object], payload["summary"])
    try:
        display_path = output_path.relative_to(root)
    except ValueError:
        display_path = output_path
    print(
        "Wrote docstring catalog "
        f"for {summary['python_files']} files to {display_path} "
        f"(missing={summary['missing_docstrings']}, flagged={summary['flagged_docstrings']})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
