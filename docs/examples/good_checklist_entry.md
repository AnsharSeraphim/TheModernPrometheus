# Good Checklist Entry Example

```markdown
- [ ] **Document wrapper failure signatures for stateless contributors**
  - Scope: Add a troubleshooting section for wrapper invocation mistakes and stale-ledger confusion.
  - Target Files: `docs/troubleshooting.md`, `scripts/README.md`
  - Dependencies: `Create reusable context prompt library for stateless repo workflows`
  - DONE WHEN: Troubleshooting doc includes both failure signatures, remediation commands, and cross-links from `scripts/README.md`.
  - Audit step: Run `rg "stale-ledger|invocation" docs/troubleshooting.md scripts/README.md` and verify both signatures appear with wrapper-first commands.
```

## Why this is good

- The scope is singular and bounded.
- Dependencies are explicit and named.
- `DONE WHEN` can be objectively verified.
- The audit step includes concrete commands and target files.
