# Kanban Project Launch Template

Use `scripts/start_cto_project.py` to turn a user request into a real Hermes Kanban board.

## Command

```bash
python3 ~/.hermes/skills/software-development/cto-agentespro/scripts/start_cto_project.py \
  --board <project-slug> \
  --repo /absolute/path/to/repo \
  --objective "<what the user wants built>" \
  --dispatch-dry-run
```

## Created graph

- Parent: `CTO plan: <objective>` assigned to `cto-agentespro`
- Child: `CTO scope + acceptance criteria` assigned to `cto-agentespro`, ready
- Child: `Builder implementation + tests` assigned to `builder-agentespro`, blocked
- Child: `Reviewer code/security pass` assigned to `reviewer-agentespro`, blocked
- Child: `QA acceptance/browser pass` assigned to `qa-agentespro`, blocked
- Child: `DevOps CI/deploy/database check` assigned to `devops-agentespro`, blocked

## Human flow

1. CTO scopes and unblocks Builder.
2. Builder implements and returns verification.
3. CTO unblocks Reviewer and QA.
4. Reviewer/QA report blockers or approval.
5. DevOps checks deployment/DB/CI when relevant.
6. Human approves merge/deploy.

## Why this is the default

It avoids spawning every profile at once before scope exists.
It keeps expensive implementation blocked until acceptance criteria are clear.
It creates a visible Kanban cockpit immediately.
