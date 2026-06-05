# Kanban Workflow

Default source of truth: Hermes Kanban.

If Kanban tools are unavailable in the current session, keep a lightweight board in the response or in `.hermes/project-brief.md` until Kanban is available.

Jira/Linear/GitHub Issues are optional adapters, not required.

## Board states

```txt
Backlog
Ready
In Progress
Review
QA
Ready for Human Merge
Ready for Human Deploy
Done
Blocked
```

## Parent task shape

```yaml
title: Build <feature/system>
owner: cto-agentespro
status: In Progress
repo: <owner/repo or local path>
base_branch: main
human_approval_required:
  - production merge
  - production deploy
  - destructive database migration
acceptance_criteria:
  - ...
child_tasks:
  - Builder: implement
  - Reviewer: review
  - QA: acceptance test
  - DevOps: deploy/CI/db if needed
```

## Task slicing rules

Good child tasks: one repo area, one role, verifiable output, clear acceptance criteria, clear files or endpoints when possible.

Bad child tasks: “fix everything,” “make it better,” ambiguous production access, or cross-cutting architecture without a design decision.

## Orchestrator loop

1. Create parent task.
2. Create child tasks.
3. Assign task to profile.
4. Worker completes, blocks, or requests decision.
5. Reviewer/QA verify.
6. CTO integrates and reports.

## Notifications

Telegram summary should be short:

```txt
🧠 CTO-agentespro
Task: <name>
Status: Ready for human merge
PR: <url>
Tests: passed / failed
Decision needed: Merge? Deploy?
```
