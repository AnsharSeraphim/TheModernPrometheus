---
applyTo: "scripts/**"
---

# Instructions for scripts/

When editing `scripts/`:

- Preserve wrapper-first contract for quality and test execution.
- Ensure any command examples still match wrapper CLI behavior.
- Do not weaken mandatory quality gates (Ruff, Pylint, Interrogate, MyPy, Pyright, Deptry, Vulture, Bandit).
- If script behavior changes, update `scripts/README.md` and `docs/release_notes.md` in the same session.
