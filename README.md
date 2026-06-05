# CTO-agentespro

A plug-and-play Hermes software team system for agentesPRO.

**What it does:** installs one orchestrator skill plus a small set of reusable agent profiles for software work: planning, implementation, review, QA, DevOps, GitHub, databases, deployments, and Kanban monitoring.

This is **not** a Jira workflow. Jira is optional. The default source of truth is **Hermes Kanban + GitHub + repo context files**.

## Core idea

`CTO-agentespro` is the umbrella. It owns the workflow.

Internal modules live under the same skill:

```txt
cto-agentespro/
  SKILL.md
  references/
    team-architecture.md
    kanban-workflow.md
    github-workflow.md
    delegation-prompts.md
    repo-context-standard.md
    safety-and-human-approval.md
  templates/
    AGENTS.md
    client-manifest.yaml
    project-brief.md
    github-pr-body.md
  scripts/
    install_cto_agentespro.py
```

Do **not** create separate top-level skills like `dev-agent`, `review-agent`, `pipeline-agent`. Those are internal roles/profiles under the `CTO-agentespro` umbrella.

## Default team

- **CTO-agentespro** — orchestrator. Understands the goal, creates Kanban tasks, delegates work, monitors blockers, reports to the human.
- **Builder-agentespro** — senior implementer. Writes code, tests, docs, commits, PRs.
- **Reviewer-agentespro** — code/security reviewer. Reviews diffs, test quality, security, maintainability.
- **QA-agentespro** — product QA / browser tester. Reproduces, checks UX, screenshots, acceptance criteria.
- **DevOps-agentespro** — deploy/database/CI specialist. Handles envs, Docker, GitHub Actions, DB migrations, deployments.

Optional later roles:

- **Designer-agentespro** — UI/product polish, frontend visual QA.
- **Data-agentespro** — data pipelines, analytics, embeddings, vector stores.
- **Docs-agentespro** — technical docs, onboarding, changelogs.

## Install from local repo

```bash
python3 skills/cto-agentespro/scripts/install_cto_agentespro.py --install-root ~/.hermes
```

Profile-specific install:

```bash
python3 skills/cto-agentespro/scripts/install_cto_agentespro.py --install-root ~/.hermes/profiles/client-name
```

## One-URL install pattern

Once published, another Hermes agent can run:

```bash
curl -L https://larvuz2.github.io/skills/cto-agentespro-skill.tar.gz -o /tmp/cto-agentespro-skill.tar.gz
mkdir -p /tmp/cto-agentespro
 tar -xzf /tmp/cto-agentespro-skill.tar.gz -C /tmp/cto-agentespro
python3 /tmp/cto-agentespro/cto-agentespro/scripts/install_cto_agentespro.py --install-root ~/.hermes --create-profiles
```

Or paste the public reader URL to another Hermes agent:

```txt
https://larvuz2.github.io/skills/cto-agentespro.md
```

## Human authority rule

Agents can prepare branches, PRs, QA reports, deployment plans, and staging deploys if configured.

Agents do **not** auto-merge to production or delete GitHub repos.

Production merge/deploy requires explicit human approval.
