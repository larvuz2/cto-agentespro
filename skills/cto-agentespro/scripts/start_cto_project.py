#!/usr/bin/env python3
"""Start a CTO-agentespro Kanban project.

Creates a Hermes Kanban board (or reuses one), a parent objective card, and the
standard software-team cards for CTO → Builder → Reviewer → QA → DevOps.

Example:
  python3 start_cto_project.py \
    --board my-app \
    --repo /srv/my-app \
    --objective "Add Stripe checkout with tests" \
    --dispatch-dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

TEAM = {
    "cto": "cto-agentespro",
    "builder": "builder-agentespro",
    "reviewer": "reviewer-agentespro",
    "qa": "qa-agentespro",
    "devops": "devops-agentespro",
}


def slugify(value: str, fallback: str = "cto-project") -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:48].strip("-") or fallback


def run(cmd: list[str], *, dry_run: bool = False, json_out: bool = False) -> dict | None:
    print("$", " ".join(cmd))
    if dry_run:
        return None
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    if json_out:
        return json.loads(proc.stdout)
    return None


def ensure_board(board: str, *, name: str, description: str, default_workdir: str | None, dry_run: bool) -> None:
    cmd = [
        "hermes", "kanban", "boards", "create", board,
        "--name", name,
        "--description", description,
        "--icon", "🧠",
        "--color", "#8b5cf6",
        "--switch",
    ]
    if default_workdir:
        cmd += ["--default-workdir", default_workdir]

    print("$", " ".join(cmd))
    if dry_run:
        return
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode == 0:
        if proc.stdout:
            print(proc.stdout, end="")
        return

    combined = (proc.stdout or "") + (proc.stderr or "")
    if "already exists" in combined.lower() or "exists" in combined.lower():
        print(f"board exists, switching: {board}")
        run(["hermes", "kanban", "boards", "switch", board])
        if default_workdir:
            run(["hermes", "kanban", "boards", "set-default-workdir", board, default_workdir])
        return

    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    raise SystemExit(proc.returncode)


def create_task(
    title: str,
    body: str,
    *,
    assignee: str,
    board: str,
    repo: str | None,
    tenant: str,
    key: str,
    parent: str | None = None,
    status: str | None = None,
    priority: int = 0,
    dry_run: bool = False,
) -> str:
    cmd = [
        "hermes", "kanban", "--board", board, "create", title,
        "--body", body,
        "--assignee", assignee,
        "--tenant", tenant,
        "--priority", str(priority),
        "--idempotency-key", key,
        "--skill", "cto-agentespro",
        "--json",
    ]
    if repo:
        cmd += ["--workspace", f"dir:{repo}"]
    if parent:
        cmd += ["--parent", parent]
    if status:
        cmd += ["--initial-status", status]
    data = run(cmd, dry_run=dry_run, json_out=True)
    return data["id"] if data else f"dry-{slugify(title)}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--objective", required=True, help="User objective / build request")
    ap.add_argument("--board", default=None, help="Kanban board slug. Defaults to objective slug.")
    ap.add_argument("--repo", default=None, help="Optional repo path to use as task workspace")
    ap.add_argument("--ticket", default=None, help="Optional ticket/client id for idempotency and branch names")
    ap.add_argument("--name", default=None, help="Human-readable board name")
    ap.add_argument("--dispatch-dry-run", action="store_true", help="Show which tasks would be spawned")
    ap.add_argument("--dispatch", action="store_true", help="Run one real dispatcher pass after creating cards")
    ap.add_argument("--dry-run", action="store_true", help="Print actions without creating cards")
    args = ap.parse_args()

    board = slugify(args.board or args.ticket or args.objective)
    tenant = slugify(args.ticket or board)
    repo_path = str(Path(args.repo).expanduser().resolve()) if args.repo else None
    if repo_path and not Path(repo_path).exists():
        raise SystemExit(f"repo path does not exist: {repo_path}")

    run(["hermes", "kanban", "init"], dry_run=args.dry_run)
    ensure_board(
        board,
        name=args.name or f"CTO {board}",
        description=f"CTO-agentespro software-team board for: {args.objective}",
        default_workdir=repo_path,
        dry_run=args.dry_run,
    )

    key_prefix = slugify(args.ticket or args.objective)

    parent_body = dedent(f"""
    # Objective

    {args.objective}

    # Operating model

    CTO-agentespro owns scope, task routing, integration, and human-facing status.
    Builder implements only after CTO scope is clear.
    Reviewer blocks on security/test/maintainability issues.
    QA verifies product behavior, not just build success.
    DevOps handles CI/deploy/database work and calls out human approvals.

    # Repo

    {repo_path or 'No repo path provided yet.'}

    # Human approval required

    - production merge
    - production deploy
    - destructive database migration
    - GitHub repo deletion
    """).strip()

    parent_id = create_task(
        f"CTO plan: {args.objective[:70]}",
        parent_body,
        assignee=TEAM["cto"],
        board=board,
        repo=repo_path,
        tenant=tenant,
        key=f"{key_prefix}:parent",
        priority=100,
        dry_run=args.dry_run,
    )

    cards = [
        (
            "CTO scope + acceptance criteria",
            TEAM["cto"],
            None,
            90,
            """
            Define the smallest shippable scope for the objective.
            Inspect repo context if available.
            Produce acceptance criteria, risk notes, and the exact Builder task.
            Unblock Builder only when the implementation task is clear.
            """,
        ),
        (
            "Builder implementation + tests",
            TEAM["builder"],
            "blocked",
            80,
            """
            Implement the scoped task only.
            Read AGENTS.md/README/package files first.
            Create or update tests.
            Run verification commands.
            Return files changed, commands run, and PR/branch handle if available.
            """,
        ),
        (
            "Reviewer code/security pass",
            TEAM["reviewer"],
            "blocked",
            70,
            """
            Review the Builder diff/PR against acceptance criteria.
            Check security, test quality, maintainability, regressions, and hidden side effects.
            Output blockers first, then suggestions.
            """,
        ),
        (
            "QA acceptance/browser pass",
            TEAM["qa"],
            "blocked",
            60,
            """
            Verify user-visible behavior.
            For frontend work, run browser QA when available and check console/network errors.
            Report exact reproduction steps for any bugs.
            """,
        ),
        (
            "DevOps CI/deploy/database check",
            TEAM["devops"],
            "blocked",
            50,
            """
            Inspect CI, deployment, database, migrations, environment variables, and rollback needs.
            Do not run production deploys or destructive migrations without explicit human approval.
            """,
        ),
    ]

    child_ids: list[str] = []
    for slug, assignee, status, priority, body in cards:
        child_id = create_task(
            f"{slug}: {args.objective[:55]}",
            dedent(body).strip(),
            assignee=assignee,
            board=board,
            repo=repo_path,
            tenant=tenant,
            key=f"{key_prefix}:{slugify(slug)}",
            parent=parent_id,
            status=status,
            priority=priority,
            dry_run=args.dry_run,
        )
        child_ids.append(child_id)

    if args.dispatch_dry_run:
        run(["hermes", "kanban", "--board", board, "dispatch", "--dry-run", "--max", "2"], dry_run=args.dry_run)
    if args.dispatch:
        run(["hermes", "kanban", "--board", board, "dispatch", "--max", "2"], dry_run=args.dry_run)

    print("\nCTO-agentespro project created")
    print(f"Board: {board}")
    print(f"Parent: {parent_id}")
    print("Children:")
    for child_id in child_ids:
        print(f"- {child_id}")
    print(f"\nWatch: hermes kanban --board {board} list")
    print(f"Dispatch dry-run: hermes kanban --board {board} dispatch --dry-run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
