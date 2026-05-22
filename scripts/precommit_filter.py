"""Lightweight manifest filter for the unified pre-commit suite."""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Generator, Iterable, Mapping, MutableMapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import cast

from scripts._automation_shared import run_command

REPO_ROOT = Path(__file__).resolve().parent.parent
STORE_ROOT = REPO_ROOT / "config" / "precommit_store"
SKIP_FLAG_TRUE = "Y"
GLOBAL_SENTINEL = "<GLOBAL>"
_IGNORED_MANIFEST_STEMS: tuple[str, ...] = ("pylint_failures",)


class FilterMode(Enum):
    """Supported filtering strategies for hook execution."""

    AUTO = "auto"
    FULL = "full"
    OFF = "off"


@dataclass(frozen=True)
class FilterMetadata:
    """Static configuration for a hook that participates in manifest filtering."""

    hook_id: str
    global_hook: bool = False


@dataclass(slots=True)
class _FilterRuntimeState:
    """Mutable state container used during a single filtering session."""

    hook_state: dict[str, dict[str, bool]]
    inventory: list[Path]
    manifest_log: list[str]
    targeted_paths: set[Path] | None
    session_active: bool
    dirty_hooks: set[str]
    pending_manifests: dict[str, tuple[Path, str]]


class PrecommitFilter:
    """Skip tracking for pre-commit hooks using JSON manifests."""

    def __init__(self, *, mode: FilterMode = FilterMode.AUTO) -> None:
        """Initialize filter state and load any existing manifests."""

        self.mode = mode
        STORE_ROOT.mkdir(parents=True, exist_ok=True)
        self.metadata: dict[str, FilterMetadata] = {}
        self._state = _FilterRuntimeState(
            hook_state={},
            inventory=[],
            manifest_log=[],
            targeted_paths=None,
            session_active=False,
            dirty_hooks=set(),
            pending_manifests={},
        )
        self._load_existing_manifests()

    @contextmanager
    def session_guard(self) -> Generator[PrecommitFilter]:
        """Provide rollback-safe mutation for a single suite execution."""

        runtime = self._state
        if runtime.session_active:
            raise RuntimeError("PrecommitFilter session already active")
        runtime.session_active = True
        snapshot = {hook: state.copy() for hook, state in runtime.hook_state.items()}
        dirty_snapshot = runtime.dirty_hooks.copy()
        log_snapshot = list(runtime.manifest_log)
        pending_snapshot = dict(runtime.pending_manifests)
        try:
            yield self
        except Exception:
            runtime.hook_state = {hook: state.copy() for hook, state in snapshot.items()}
            runtime.dirty_hooks = dirty_snapshot
            runtime.manifest_log = log_snapshot
            runtime.pending_manifests = pending_snapshot
            raise
        else:
            if runtime.pending_manifests:
                self._commit_pending_manifests()
                runtime.pending_manifests.clear()
        finally:
            runtime.session_active = False

    def configure_checks(self, metadata: Mapping[str, FilterMetadata]) -> None:
        """Register hook metadata used by the filter."""

        self.metadata = dict(metadata)
        for hook_id in self.metadata:
            self._state.hook_state.setdefault(hook_id, {})

    def set_targeted_paths(self, paths: Sequence[Path] | None) -> None:
        """Record explicit paths for the current run, if any."""

        self._state.targeted_paths = set(paths) if paths else None

    def build_repository_inventory(self) -> list[Path]:
        """Enumerate tracked Python files for hook-scoped pre-commit filtering."""

        completed = run_command(["git", "ls-files"], cwd=REPO_ROOT, check=False)
        if completed.returncode != 0:
            self._state.inventory = []
            return []

        inventory: list[Path] = []
        for entry in (completed.stdout or "").splitlines():
            if not entry.strip():
                continue
            relative = Path(entry.strip())
            if relative.suffix in {".py", ".pyi"}:
                inventory.append(relative)
        inventory.sort()
        self._state.inventory = inventory
        return list(inventory)

    def sync_manifest(self) -> None:
        """Ensure configured manifests match the current Python inventory."""

        runtime = self._state
        for hook_id in self.metadata:
            state = runtime.hook_state.setdefault(hook_id, {})
            for key in list(state):
                if key == GLOBAL_SENTINEL:
                    continue
                if not (REPO_ROOT / key).exists():
                    del state[key]
                    runtime.dirty_hooks.add(hook_id)
                    runtime.manifest_log.append(f"[{hook_id}] Removed missing file: {key}")
            for path in runtime.inventory:
                key = path.as_posix()
                if key not in state:
                    state[key] = False
                    runtime.dirty_hooks.add(hook_id)
                    runtime.manifest_log.append(f"[{hook_id}] Added file: {key}")

    def flush_manifest_log(self) -> None:
        """Print the accumulated manifest change log."""

        if not self._state.manifest_log:
            return
        for entry in self._state.manifest_log:
            print(entry)
        self._state.manifest_log.clear()

    def determine_paths(self, hook_id: str, candidates: Sequence[Path]) -> tuple[tuple[Path, ...], bool, str | None]:
        """Resolve the concrete repository paths selected for one filtered hook run."""

        metadata = self.metadata.get(hook_id)
        if metadata is None:
            selected_candidates = tuple(candidates)
            return selected_candidates, bool(selected_candidates), None

        state = self._state.hook_state.setdefault(hook_id, {})
        normalized = self._normalize_candidates(hook_id, candidates, state, metadata)
        if self._state.targeted_paths is not None:
            if not normalized:
                return tuple(), False, "No targeted files require this hook."
            self._reset_skip_flags(hook_id, normalized, state)
            return tuple(normalized), True, None

        if self.mode in {FilterMode.FULL, FilterMode.OFF}:
            self._reset_skip_flags(hook_id, normalized, state)
            return tuple(normalized), bool(normalized), None

        selected_paths = tuple(path for path in normalized if not state.get(path.as_posix()))
        if not selected_paths:
            return tuple(), False, f"All tracked files already passed {hook_id}; skipping."
        return selected_paths, True, None

    def record_result(self, hook_id: str, paths: Iterable[Path], *, success: bool) -> None:
        """Persist the result of a hook run for ``paths``."""

        state = self._state.hook_state.setdefault(hook_id, {})
        recorded = False
        for path in paths:
            key = path.as_posix()
            if state.get(key) != success:
                state[key] = success
                self._state.dirty_hooks.add(hook_id)
            recorded = True
        if not recorded and state.get(GLOBAL_SENTINEL) != success:
            state[GLOBAL_SENTINEL] = success
            self._state.dirty_hooks.add(hook_id)

    def reset_all_flags(self) -> None:
        """Rebuild manifests from tracked Python files with every skip flag reset."""

        inventory_keys = {path.as_posix() for path in self._state.inventory}
        for hook_id, state in list(self._state.hook_state.items()):
            metadata = self.metadata.get(hook_id)
            rebuilt = {key: False for key in sorted(inventory_keys)}
            if metadata is not None and metadata.global_hook:
                rebuilt[GLOBAL_SENTINEL] = False
            if state != rebuilt:
                self._state.manifest_log.append(f"[{hook_id}] Rebuilt baseline manifest")
                self._state.dirty_hooks.add(hook_id)
            self._state.hook_state[hook_id] = rebuilt

    def save(self) -> None:
        """Persist modified manifests to disk."""

        runtime = self._state
        pending: dict[str, tuple[Path, str]] = {}
        for hook_id, entries in runtime.hook_state.items():
            path = self._manifest_path(hook_id)
            if hook_id not in runtime.dirty_hooks and path.exists():
                continue
            payload: MutableMapping[str, MutableMapping[str, str]] = {}
            for key in sorted(entries):
                payload[key] = {"skip": SKIP_FLAG_TRUE if entries[key] else "N"}
            pending[hook_id] = (path, json.dumps(payload, indent=2, sort_keys=True) + "\n")

        if runtime.session_active:
            runtime.pending_manifests.update(pending)
            return

        for hook_id, (path, serialized) in pending.items():
            _atomic_write_text(path, serialized)
            runtime.dirty_hooks.discard(hook_id)

    def verify_index_clean(self) -> bool:
        """Preserve the historical clean-index compatibility check for wrapper callers."""

        return True

    def set_hook_state(self, hook_id: str, entries: Mapping[str, bool]) -> None:
        """Seed manifest state for ``hook_id``."""

        self._state.hook_state[hook_id] = dict(entries)

    def get_hook_state(self, hook_id: str) -> dict[str, bool]:
        """Expose an isolated copy of persisted manifest state for one hook identifier."""

        return dict(self._state.hook_state.get(hook_id, {}))

    def set_inventory(self, inventory: Sequence[Path]) -> None:
        """Seed repository inventory entries for tests or targeted workflows."""

        self._state.inventory = list(inventory)

    def _normalize_candidates(
        self,
        hook_id: str,
        candidates: Sequence[Path],
        state: dict[str, bool],
        metadata: FilterMetadata,
    ) -> list[Path]:
        """Normalize hook candidates and ensure they are tracked in hook state."""

        normalized: list[Path] = []
        for path in candidates:
            key = path.as_posix()
            if key not in state:
                state[key] = False
                self._state.dirty_hooks.add(hook_id)
                self._state.manifest_log.append(f"[{hook_id}] Added file: {key}")
            normalized.append(path)

        if metadata.global_hook and not normalized and GLOBAL_SENTINEL not in state:
            state[GLOBAL_SENTINEL] = False
            self._state.dirty_hooks.add(hook_id)
        return normalized

    def _reset_skip_flags(self, hook_id: str, paths: Sequence[Path], state: dict[str, bool]) -> None:
        """Reset skip flags to ``False`` for the given hook paths."""

        for path in paths:
            key = path.as_posix()
            if state.get(key):
                state[key] = False
                self._state.dirty_hooks.add(hook_id)

    def _load_existing_manifests(self) -> None:
        """Load previously persisted manifest JSON files into runtime state."""

        for path in STORE_ROOT.glob("*.json"):
            if path.stem in _IGNORED_MANIFEST_STEMS:
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if not isinstance(payload, dict):
                continue
            payload_mapping = cast(dict[str, object], payload)
            parsed: dict[str, bool] = {}
            for key_object, value_object in payload_mapping.items():
                if not isinstance(value_object, dict):
                    continue
                value_mapping = cast(dict[str, object], value_object)
                skip_value = value_mapping.get("skip")
                if isinstance(skip_value, str):
                    parsed[key_object] = skip_value.upper() == SKIP_FLAG_TRUE
            self._state.hook_state[path.stem] = parsed

    def _manifest_path(self, hook_id: str) -> Path:
        """Derive the persisted manifest file path associated with one hook identifier."""

        return STORE_ROOT / f"{hook_id}.json"

    def _commit_pending_manifests(self) -> None:
        """Atomically persist deferred manifests collected during an active session."""

        for hook_id, (path, serialized) in self._state.pending_manifests.items():
            _atomic_write_text(path, serialized)
            self._state.dirty_hooks.discard(hook_id)


def _atomic_write_text(target: Path, payload: str) -> None:
    """Atomically write UTF-8 text to ``target``."""

    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=target.parent) as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
        temp_path = Path(handle.name)
    os.replace(temp_path, target)
