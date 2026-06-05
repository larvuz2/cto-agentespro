# CTO-agentespro

A plug-and-play Hermes software team system, originally built for agentesPRO but designed to work for any software repo.

**What it does:** installs one orchestrator skill plus reusable software-team profiles for planning, implementation, review, QA, DevOps, GitHub, databases, deployments, and Kanban monitoring.

This is **not** a Jira workflow. Jira is optional. The default source of truth is **Hermes Kanban + GitHub + repo context files**.

## Requirements

- Hermes Agent installed
- Python 3.10+
- Git available
- Optional: GitHub CLI `gh` for GitHub PR/repo automation

## Quickstart: one URL install

Paste this into another Hermes environment:

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

Public reader URL:

```txt
https://larvuz2.github.io/skills/cto-agentespro.md
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
