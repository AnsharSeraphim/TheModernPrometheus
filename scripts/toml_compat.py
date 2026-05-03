"""Compatibility TOML parsing helper for wrapper scripts."""

from __future__ import annotations

import importlib
import sys
from typing import Any, cast


def parse_toml_text(text: str) -> object:
    """Parse TOML text using stdlib ``tomllib`` or fallback ``tomli``."""

    module_name = "tomllib" if sys.version_info >= (3, 11) else "tomli"
    parser_module = cast(Any, importlib.import_module(module_name))
    parsed = parser_module.loads(text)
    return parsed
