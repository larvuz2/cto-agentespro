# GitHub Workflow

## Discovery first

Run:

```bash
git status --short
git branch --show-current
git remote -v
git log --oneline -5
gh auth status 2>/dev/null || true
```

If `gh` is not available, use git and report the limitation.

## Context files

Read in this order when present:

```txt
AGENTS.md
CLAUDE.md
.cursorrules
README.md
package.json / pyproject.toml / requirements.txt / pnpm-lock.yaml
.env.example
```

## Branching

Default base branch:

1. repo default branch if known
2. `main`
3. `master`
4. current branch only if user explicitly asks

Branch names:

```txt
feature/<task-id>-short-name
fix/<task-id>-short-name
chore/<task-id>-short-name
```

Client ticket IDs can be included:

```txt
feature/ACME-123-payment-flow
fix/ACME-456-login-timeout
```

## PR body

```txt
## Goal
## Changes
## Tests / Verification
## Screenshots / Evidence
## Risks
## Human approval needed
```

## Merge rule

Agents prepare PRs. Humans merge production branches.

Never auto-merge protected branches unless the user explicitly configured that for a non-production repo.
