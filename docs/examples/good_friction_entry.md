# Good Friction Entry Example

```markdown
- [ ] **Add wrapper-command quick reference near checklist header**
  - Scope: Reduce invocation syntax mistakes by placing copy-ready wrapper commands near task instructions.
  - Target Files: `Final-Productization-Checklist.md`, `docs/agent_bootstrap/operator_context_injection.md`
  - Dependencies: None
  - DONE WHEN: Checklist header includes pre-commit and test wrapper command examples and links to the bootstrap playbook.
  - Audit step: Inspect the checklist header and confirm both command examples match `python scripts/run_precommit_suite.py --help` and `python scripts/run_tests.py --help`.
```

## Why this is good

- Captures a reproducible friction symptom and concrete mitigation.
- Keeps scope narrow and implementation-oriented.
- Includes an audit step that checks command parity against live wrapper help.
