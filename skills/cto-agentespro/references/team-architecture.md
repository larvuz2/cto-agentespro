# CTO-agentesPRO Team Architecture

## Principle

One umbrella: `CTO-agentespro`.

The roles are profiles/prompts under the umbrella, not separate top-level skills.

## Minimal default team

### CTO-agentespro

Orchestrator. Handles objective clarification, technical plan, task decomposition, Kanban management, delegation, integration, final verification, and human-facing status.

### Builder-agentespro

Senior implementation agent. Handles code changes, tests, local verification, commits, PR body draft, and self-review.

Default instruction: implement the smallest complete version that satisfies acceptance criteria.

### Reviewer-agentespro

Review/security agent. Handles diff review, test quality, security risks, maintainability, hidden side effects, and PR comments.

Default instruction: blockers first, suggestions second.

### QA-agentespro

Acceptance QA agent. Handles product behavior verification, browser QA, screenshots if relevant, console/network checks, regression scenarios, and acceptance criteria checklist.

Default instruction: verify like a user, not just like a test runner.

### DevOps-agentespro

Infra/deployment agent. Handles GitHub Actions, Docker/VPS/systemd, DB migrations, env vars/secrets checklist, staging/production deploy plans, and rollback plan.

Default instruction: production changes need human approval.

## Optional profiles

### Designer-agentespro

Use for visual/frontend/UI-heavy work.

### Data-agentespro

Use for database-heavy, analytics, embeddings, ETL, RAG, or AI data pipelines.

### Docs-agentespro

Use for docs-heavy delivery, onboarding, changelog, or client handoff.

## Recommended profile naming

Keep names stable:

```txt
cto-agentespro
builder-agentespro
reviewer-agentespro
qa-agentespro
devops-agentespro
```

For client-specific versions:

```txt
cto-clientname
builder-clientname
reviewer-clientname
qa-clientname
devops-clientname
```

Only create client-specific profiles when there is real recurring client context.
