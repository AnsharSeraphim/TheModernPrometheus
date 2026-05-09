# Security Hygiene and Data Boundary Guide

This repository template is designed to keep source-controlled assets separate from local operational evidence and secrets.

## Never commit secrets

Do not commit:

- API keys, access tokens, passwords, private certificates, or SSH private keys.
- `.env` files with real credentials.
- cloud provider credential exports.
- local authentication caches from developer tools.

If a secret is accidentally committed, rotate it immediately and purge it from Git history according to your organization policy.

## Local evidence stays local

The quality and test wrappers generate local evidence under:

- `build/automation_contract/`
- `reports/reasoning/pipeline/`

These are local verification caches and should remain untracked.

## Binary and archive deny-path guidance

Do not commit binary evidence artifacts (screenshots, recordings, archives) unless your project explicitly requires versioned binary fixtures.

Examples that should remain local for this template:

- screenshots (`.png`, `.jpg`)
- videos (`.mp4`, `.mov`)
- archives (`.zip`, `.tar`, `.gz`)

## Source-vs-local boundaries

Use these boundaries when deciding whether a file belongs in Git:

- **Commit**: source code, tests, policy docs, wrapper scripts, and wrapper-managed ledgers under `config/precommit_store/`.
- **Do not commit**: local virtual environments, cache directories, local evidence outputs, and transient editor/runtime state.

When in doubt, verify ignore coverage with:

```bash
git check-ignore -v <path>
```

## Environment-file policy

Use template environment files (for example `.env.example`) for documentation only.

- Include variable names and safe placeholders.
- Exclude real values and machine-specific paths.

## Practical guardrails for contributors and coding agents

- Run wrapper commands from `scripts/run_precommit_suite.py` and `scripts/run_tests.py` so policy checks are consistently enforced.
- Keep generated local evidence out of commits even when capturing troubleshooting artifacts.
- Prefer least-privilege credentials in local development and CI.
- Treat copied logs as potentially sensitive; redact tokens and internal URLs before sharing externally.
