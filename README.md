# CTO-agentespro

A plug-and-play Hermes software team system, originally built for agentesPRO but designed to work for any software repo.

**What it does:** installs one orchestrator skill plus reusable software-team profiles for planning, implementation, review, QA, DevOps, GitHub, databases, deployments, and Kanban monitoring.

This is **not** a Jira workflow. Jira is optional. The default source of truth is **Hermes Kanban + GitHub + repo context files**.

## Requirements

- Hermes Agent installed
- Python 3.10+
- Git available
- Optional: GitHub CLI `gh` for GitHub PR/repo automation

## Quickstart: simplest install

Paste this URL into another Hermes agent and say: `install this CTO software team`.

```txt
https://larvuz2.github.io/skills/cto-agentespro.md
```

The first instruction inside that public reader tells the target agent to install the full tarball package, because the complete CTO team needs scripts, templates, references, and generated profiles.

If you are installing directly from a terminal instead of asking a Hermes agent, run:

```bash
set -euo pipefail
curl -fL https://larvuz2.github.io/skills/cto-agentespro-skill.tar.gz -o /tmp/cto-agentespro-skill.tar.gz
rm -rf /tmp/cto-agentespro
mkdir -p /tmp/cto-agentespro
tar -xzf /tmp/cto-agentespro-skill.tar.gz -C /tmp/cto-agentespro
python3 /tmp/cto-agentespro/cto-agentespro/scripts/install_cto_agentespro.py --target-profile default --create-team-profiles
```

Then reload skills or start a new Hermes session and ask:

```txt
Use cto-agentespro. Review this repo, create a Kanban plan, and implement the smallest safe fix for <goal>.
```

## Local install

Install into the default Hermes profile/home:

```bash
python3 skills/cto-agentespro/scripts/install_cto_agentespro.py --target-profile default --create-team-profiles
```

Install into a specific Hermes profile:

```bash
python3 skills/cto-agentespro/scripts/install_cto_agentespro.py --target-profile client-name --create-team-profiles
```

Dry run first:

```bash
python3 skills/cto-agentespro/scripts/install_cto_agentespro.py --dry-run --create-team-profiles
```

Legacy direct root install is still supported:

```bash
python3 skills/cto-agentespro/scripts/install_cto_agentespro.py --install-root ~/.hermes
```

## Verify install

Default profile expected path:

```txt
~/.hermes/skills/software-development/cto-agentespro/SKILL.md
```

Specific profile expected path:

```txt
~/.hermes/profiles/<profile>/skills/software-development/cto-agentespro/SKILL.md
```

Smoke test:

```bash
tmpdir="$(mktemp -d)"
python3 skills/cto-agentespro/scripts/install_cto_agentespro.py --install-root "$tmpdir" --source skills/cto-agentespro
test -f "$tmpdir/skills/software-development/cto-agentespro/SKILL.md"
```

## Executive summary

### Core idea

- **CTO-agentespro is a plug-and-play AI software team orchestrator.**
- The user gives it a software objective: build an app, fix a bug, create a repo, connect a database, deploy a site, review code, or ship a feature.
- The CTO does **not** just code immediately.
- It first understands the objective, breaks it into tasks, creates a Kanban board, then delegates work to specialized agent profiles.
- Default source of truth: **Hermes Kanban + GitHub + repo context files**.
- Jira is optional, not required.

### Main role

- **CTO-agentespro = orchestrator / technical lead.**
- It acts like the software team lead.
- It understands what the user wants, inspects the repo/project, defines acceptance criteria, creates tasks, assigns work to the right agent, verifies outputs, and keeps humans in control of risky decisions.

### Default team structure

- **CTO-agentespro** — orchestrator / product-technical owner. Creates plan, scope, architecture, task breakdown, and controls Kanban state.
- **Builder-agentespro** — senior coder. Implements features, fixes bugs, and writes tests.
- **Reviewer-agentespro** — code reviewer. Checks quality, security, architecture, and test coverage.
- **QA-agentespro** — product tester. Runs acceptance tests, browser checks, and regression checks.
- **DevOps-agentespro** — infra/deployment agent. Handles GitHub Actions, CI/CD, deployments, databases, and environment checks.

### How a project starts

- User gives an objective, for example:

```txt
Build a dashboard where users can upload images and generate AI video prompts.
```

- CTO-agentespro creates a Kanban board with structured tasks:
  - CTO plan
  - CTO scope + acceptance criteria
  - Builder implementation + tests
  - Reviewer code/security pass
  - QA acceptance/browser pass
  - DevOps CI/deploy/database check
- The CTO starts first.
- Other agents stay blocked until the scope is clear.
- This prevents chaos and wasted agent work.

### Kanban as the cockpit

- Kanban is the central control room.
- It tracks what is ready, in progress, blocked, in review, in QA, ready for human merge/deploy, and done.
- Default states:

```txt
Backlog
Ready
In Progress
Review
QA
Ready for Human Merge/Deploy
Done
Blocked
```

### Workflow

- **Understand** — CTO reads the user objective and clarifies the real product/technical goal.
- **Inspect** — checks repo structure and reads context files like `README.md`, `AGENTS.md`, `CLAUDE.md`, package files, and env examples.
- **Scope** — defines acceptance criteria, identifies risks, and splits the work into small tasks.
- **Create Kanban** — parent objective card plus role-specific child cards.
- **Delegate** — Builder implements, Reviewer checks, QA validates, DevOps handles deploy/CI/database concerns.
- **Verify** — tests/builds/browser checks/deployment checks run before success is claimed.
- **Human approval** — agents prepare PRs and deployments; humans approve important merges/deploys.

### GitHub behavior

- CTO-agentespro can organize GitHub work: repo inspection, branch creation, scoped commits, PRs, PR summaries, and test verification.
- Safe defaults:
  - agents do **not** auto-merge production
  - agents do **not** delete repos without explicit written confirmation
  - agents do **not** run destructive production database actions without approval

### Database and deployment behavior

- DevOps-agentespro handles migrations, Supabase/Postgres/SQLite checks, environment variables, CI/CD, GitHub Actions, VPS deployment, staging deploys, and health checks.
- Production-sensitive actions require human approval.

### Why this is better than one generic agent

- One generic agent tries to do everything and loses structure.
- CTO-agentespro separates responsibility:
  - CTO thinks
  - Builder builds
  - Reviewer critiques
  - QA validates
  - DevOps deploys
- This makes work easier to debug, cheaper, safer, more parallel, and more production-ready.

### Cost strategy

- Use expensive reasoning/model effort only for architecture, difficult implementation, and complex debugging.
- Use cheaper/simple passes for Kanban updates, status summaries, lint/test summaries, PR formatting, and basic gate checks.
- Main savings: **gate before coding, scope before delegating, avoid retry loops, and only launch expensive builders when the task is clear.**

### Human control boundaries

- Agents can create branches, commit code, open PRs, run tests, prepare deploys, update Kanban, and report blockers.
- Humans control production merges, repo deletion, destructive database migrations, major architecture decisions, and ambiguous product tradeoffs.

### Plug-and-play goal

```txt
Paste a public URL into another Hermes instance
→ install CTO-agentespro
→ generate all software team profiles
→ start using the CTO team immediately
```

### Simple mental model

```txt
User objective
→ CTO understands and scopes
→ Kanban board is created
→ Builder implements
→ Reviewer checks
→ QA tests
→ DevOps prepares deploy
→ Human approves merge/deploy
→ Done
```

### Positioning

**CTO-agentespro turns any Hermes instance into a Kanban-driven AI software team: one CTO orchestrator, specialized worker profiles, GitHub-safe workflows, QA, DevOps, and human-controlled production decisions.**

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
    init_repo_context.py
    start_cto_project.py
    package_skill.py
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

## Repo bootstrap

In any software repo, create agent context files:

```bash
python3 ~/.hermes/skills/software-development/cto-agentespro/scripts/init_repo_context.py --brief
```

This creates:

- `AGENTS.md`
- `.hermes/project-brief.md`

It does not overwrite existing files unless `--force` is passed.

## Start a real Kanban software-team board

Create the CTO cockpit for a build:

```bash
python3 ~/.hermes/skills/software-development/cto-agentespro/scripts/start_cto_project.py \
  --board my-app \
  --repo /absolute/path/to/repo \
  --objective "Build the requested feature" \
  --dispatch-dry-run
```

This creates:

- parent CTO objective card
- CTO scope/acceptance card
- blocked Builder implementation card
- blocked Reviewer code/security pass
- blocked QA acceptance/browser pass
- blocked DevOps CI/deploy/database check

Watch the board:

```bash
hermes kanban --board my-app list
```

Run one real dispatcher pass when ready:

```bash
hermes kanban --board my-app dispatch --max 2
```

## Human authority rule

Agents can prepare branches, PRs, QA reports, deployment plans, and staging deploys if configured.

Agents do **not** auto-merge to production or delete GitHub repos.

Production merge/deploy requires explicit human approval.

## Packaging / publish

Build local artifacts:

```bash
python3 skills/cto-agentespro/scripts/package_skill.py
```

Publish to the current Larvuz public pages repo:

```bash
python3 skills/cto-agentespro/scripts/package_skill.py --publish-dir /root/presentations/public-pages-deploy/skills
```
