"""Global pytest policy hooks for repository tests."""

from __future__ import annotations

import os

import pytest

from scripts.pytest_guard import WRAPPER_ENV_VAR, render_pytest_wrapper_warning


def pytest_sessionstart(session: pytest.Session) -> None:
    """Block direct pytest execution unless wrapper opt-in is present."""

    del session
    if os.environ.get(WRAPPER_ENV_VAR) == "1":
        return
    raise pytest.UsageError(render_pytest_wrapper_warning())
