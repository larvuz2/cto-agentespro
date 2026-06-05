# Safety and Human Approval

## Never automatic

Require explicit human approval for:

- deleting GitHub repositories
- merging to production/protected branches
- production deploys when not already approved by project rules
- destructive database migrations
- deleting production data
- rotating or exposing secrets
- changing billing/paid infrastructure

## Allowed by default

Agents may:

- inspect repos
- create branches
- edit code
- run tests/builds
- open PRs
- prepare staging deployments
- write migration files without applying to production
- write deployment plans

## Secret handling

Never paste secrets into prompts, docs, PRs, or logs.

If secret-looking material appears in files or output, redact it as `[REDACTED]`.
