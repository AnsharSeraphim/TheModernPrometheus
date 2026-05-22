#!/usr/bin/env python3
"""Apply generated docstring replacements from the remediation manifest."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any


def _parse_args() -> argparse.Namespace:
    """Parse repository root and manifest path arguments for remediation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."), help="Repository root to modify.")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("build/automation_contract/docstring_remediation/docstring_remediation_manifest.json"),
        help="Docstring remediation manifest path.",
    )
    return parser.parse_args()


def _doc_node(node: ast.AST) -> ast.Constant | None:
    """Locate the literal docstring node for a module, class, or function symbol."""
    body = getattr(node, "body", None)
    if not body or not isinstance(body, list):
        return None
    first = body[0]
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
        return first.value
    return None


def _iter_symbols(tree: ast.Module) -> dict[tuple[str, str, int], ast.Constant]:
    """Index existing docstring nodes by aggregate symbol identity."""
    nodes: dict[tuple[str, str, int], ast.Constant] = {}
    module_doc = _doc_node(tree)
    if module_doc is not None:
        nodes[("module", "module", 1)] = module_doc

    class Visitor(ast.NodeVisitor):
        """Track nested symbol names while collecting docstring constants."""
        def __init__(self) -> None:
            """Initialize the visitor's dotted symbol stack."""
            self.stack: list[str] = []

        def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802
            """Index class docstrings before visiting nested members."""
            symbol = ".".join([*self.stack, node.name])
            doc = _doc_node(node)
            if doc is not None:
                nodes[(symbol, "class", node.lineno)] = doc
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
            """Index synchronous function docstrings before visiting nested members."""
            symbol = ".".join([*self.stack, node.name])
            doc = _doc_node(node)
            if doc is not None:
                nodes[(symbol, "function", node.lineno)] = doc
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802
            """Index asynchronous function docstrings before visiting nested members."""
            symbol = ".".join([*self.stack, node.name])
            doc = _doc_node(node)
            if doc is not None:
                nodes[(symbol, "function", node.lineno)] = doc
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

    Visitor().visit(tree)
    return nodes


def _abs_offset(lines: list[str], lineno: int, col: int) -> int:
    """Convert one-indexed AST line and zero-indexed column data into a string offset."""
    return sum(len(line) for line in lines[: lineno - 1]) + col


def _quote_docstring(docstring: str, indent: str) -> str:
    """Render a replacement docstring literal with stable triple-double quoting."""
    escaped = docstring.replace("\\", "\\\\").replace('"""', '\"\"\"')
    if "\n" not in escaped and len(escaped) <= 115:
        return f'"""{escaped}"""'
    body = "\n".join(indent + line if line else indent for line in escaped.splitlines())
    return f'"""\n{body}\n{indent}"""'


def _apply_file(repo_root: Path, rel_path: str, targets: list[dict[str, Any]]) -> tuple[int, list[dict[str, Any]]]:
    """Apply all docstring replacements for one Python source file."""
    path = repo_root / rel_path
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    tree = ast.parse(text, filename=rel_path)
    nodes = _iter_symbols(tree)
    replacements: list[tuple[int, int, str]] = []
    skipped: list[dict[str, Any]] = []
    for target in targets:
        key = (target["symbol"], target["kind"], target["line"])
        doc_node = nodes.get(key)
        if doc_node is None:
            skipped.append({**target, "reason": "existing_docstring_not_found"})
            continue
        start = _abs_offset(lines, int(doc_node.lineno), int(doc_node.col_offset))
        end = _abs_offset(lines, int(doc_node.end_lineno), int(doc_node.end_col_offset))
        indent = " " * int(doc_node.col_offset)
        replacements.append((start, end, _quote_docstring(str(target["replacement_docstring"]), indent)))
    for start, end, replacement in sorted(replacements, key=lambda item: item[0], reverse=True):
        text = text[:start] + replacement + text[end:]
    path.write_text(text, encoding="utf-8")
    return len(replacements), skipped


def main() -> int:
    """Apply the remediation manifest and report skipped targets, if any."""
    args = _parse_args()
    repo_root = args.repo_root.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else repo_root / args.manifest
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_file: dict[str, list[dict[str, Any]]] = {}
    for target in manifest["targets"]:
        by_file.setdefault(target["file"], []).append(target)
    applied = 0
    skipped: list[dict[str, Any]] = []
    for rel_path, targets in sorted(by_file.items()):
        applied_count, skipped_entries = _apply_file(repo_root, rel_path, targets)
        applied += applied_count
        skipped.extend(skipped_entries)
    print(f"Applied {applied} docstring remediation target(s).")
    if skipped:
        print(json.dumps({"skipped": skipped}, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
