# Template Customization Checklist

Use this checklist immediately after cloning this repository template to prevent shipping placeholder metadata, stale policy links, or scaffold defaults into a real project.

## 1) Rename and metadata replacement

- [ ] Rename the repository, package/module names, and human-facing project title text.
- [ ] Replace placeholder author/reviewer metadata (for example names, organizations, and contact references).
- [ ] Verify README and docs copy refer to your project domain instead of template framing.
- [ ] Confirm GitHub labels, branch rules, and workflow names use project-specific language where needed.

## 2) Dependency and runtime decisions

- [ ] Review `pyproject.toml` runtime and dependency bounds for your supported deployment targets.
- [ ] Review `requirements-dev.txt` and remove tools your project intentionally does not adopt.
- [ ] Confirm wrapper scripts still reflect your intended quality gates and do not mention removed tooling.
- [ ] Confirm CI runners and local onboarding docs reference the same supported Python runtime window.

## 3) Security and ignore-policy verification

- [ ] Validate root `.gitignore` against your project's generated artifacts, local evidence paths, and cache directories.
- [ ] Add deny-path rules for any project-specific secret-bearing files and local datasets.
- [ ] Verify binary and local-evidence policies are documented in onboarding and contributor docs.
- [ ] Run `git check-ignore -v <path>` for at least one local evidence path and one cache path.

## 4) Checklist and governance seeding

- [ ] Review `Final-Productization-Checklist.md` and remove template-starter entries that do not apply to your project.
- [ ] Seed project-specific checklist entries using the required checklist template fields.
- [ ] Verify dependency order is explicit for tasks that must be completed before downstream work.
- [ ] Confirm unresolved quality/tooling debts are tracked as actionable open entries rather than prose notes.

## 5) Documentation index and onboarding parity

- [ ] Update `README.md` repository map entries to match your project's active folders and workflows.
- [ ] Update `docs/README.md` links so they point to current project docs and remove stale template-only links.
- [ ] Update `docs/new_user_onboarding.md` with project-specific setup and execution context.
- [ ] Add or update folder-level `README.md` files for major directories used by contributors and agents.

## 6) Initial validation pass before first feature work

Run wrapper commands before creating the first project-specific feature PR:

```bash
python scripts/run_precommit_suite.py
python scripts/run_tests.py
```

Then verify:

- [ ] Pre-commit and tests pass without template-only assumptions.
- [ ] Any remaining violations are captured as scoped entries in `Final-Productization-Checklist.md`.
- [ ] `docs/release_notes.md` records template-customization decisions that alter contributor workflow or quality policy.
