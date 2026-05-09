# Bad Evidence Packaging Example

## Failure pattern

- Paste mid-run logs that include only percentage updates.
- Omit the final wrapper completion lines.
- Claim tests passed without including command output boundaries.

## Why this is bad

- Reviewers cannot verify suite completion or scope.
- Streaming logs can hide failing hooks after truncated output.
- Lacks reproducible command/evidence linkage required for stateless continuity.
