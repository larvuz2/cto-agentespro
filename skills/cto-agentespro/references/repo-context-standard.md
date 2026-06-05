# Repo Context Standard

Every serious repo should include an `AGENTS.md` file so the software team can work without rediscovering conventions.

## Minimum `AGENTS.md`

```md
# Agent Instructions

## Project
- Name:
- Purpose:
- Owner:
- Production URL:
- Staging URL:

## Stack
- Frontend:
- Backend:
- Database:
- Deployment:

## Commands
- Install:
- Dev:
- Build:
- Test:
- Lint:

## Git
- Base branch:
- Branch naming:
- PR requirements:

## Environment
- Required env vars:
- Where secrets live:
- Never commit:

## QA
- Critical flows:
- Browser/device targets:
- Smoke tests:

## Human approval required
- production merge
- production deploy
- destructive migration
- repo deletion
```

## Why this matters

Repo context saves tokens, prevents repeated questions, and keeps every profile aligned.
