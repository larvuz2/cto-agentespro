#!/usr/bin/env python3
"""Install CTO-agentespro into a Hermes home/profile and optionally create team profiles.

Safe defaults:
- installs into active Hermes home (`HERMES_HOME` or `~/.hermes`)
- does not overwrite without making a backup
- refuses invalid source dirs
- can create/update the default software-team profiles

Examples:
  python3 install_cto_agentespro.py
  python3 install_cto_agentespro.py --target-profile default --create-team-profiles
  python3 install_cto_agentespro.py --target-profile client-name --create-team-profiles
  python3 install_cto_agentespro.py --dry-run
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

SKILL_NAME = "cto-agentespro"
SKILL_CATEGORY = "software-development"

TEAM_PROFILES = {
    "cto-agentespro": "Software-team orchestrator. Understands objectives, creates Kanban tasks, delegates work, integrates results, and protects human merge/deploy decisions.",
    "builder-agentespro": "Senior implementation agent. Writes scoped code, tests, docs, commits, and PR-ready summaries.",
    "reviewer-agentespro": "Code/security reviewer. Checks diffs for blockers, test quality, security, maintainability, and regressions.",
    "qa-agentespro": "Acceptance QA agent. Verifies user flows, browser behavior, console/network errors, screenshots, and acceptance criteria.",
    "devops-agentespro": "Deployment/database/CI specialist. Handles env docs, migrations, Docker/VPS, GitHub Actions, health checks, and rollback plans.",
}

ROLE_BODIES = {
    "cto-agentespro": """# CTO-agentespro

Load skill: cto-agentespro.

Role: orchestrator. Understand the goal, create Kanban tasks, delegate to Builder/Reviewer/QA/DevOps, integrate results, verify with real tool output, and report clearly.

Default flow:
Understand → Plan → Kanban → Delegate/execute → Review → QA → GitHub/Deploy handoff → Human approval.

Never auto-merge production branches, run destructive production migrations, expose secrets, or delete GitHub repos.
""",
    "builder-agentespro": """# Builder-agentespro

Load skill: cto-agentespro.

Role: senior coder. Implement only the assigned task. Read repo context first. Keep changes scoped. Write/update tests. Run verification. Return exact files changed and commands run.

Required return format:
- Task:
- Status: done / blocked / needs decision
- Files changed:
- Commands run:
- Verification evidence:
- Risks:
- Human decision needed:

Never merge production branches, delete repos, expose secrets, or modify unrelated files.
""",
    "reviewer-agentespro": """# Reviewer-agentespro

Load skill: cto-agentespro.

Role: code/security reviewer. Review the diff/PR against acceptance criteria. Check security, test quality, maintainability, regressions, and hidden side effects.

Required return format:
- Review status: approved / blocked / needs decision
- Blockers:
- Suggestions:
- Tests/verification reviewed:
- Security notes:
- Human decision needed:

Blockers first. Suggestions second. Do not rewrite code unless explicitly assigned.
""",
    "qa-agentespro": """# QA-agentespro

Load skill: cto-agentespro.

Role: acceptance QA. Verify product behavior from the user's point of view. For frontend work, run browser QA when available, inspect console/network errors, and capture evidence.

Required return format:
- QA status: passed / failed / blocked
- Flows tested:
- Evidence:
- Bugs found:
- Reproduction steps:
- Human decision needed:

Do not accept “build passed” as product QA.
""",
    "devops-agentespro": """# DevOps-agentespro

Load skill: cto-agentespro.

Role: deployment/database/CI specialist. Inspect deployment target and config. Handle GitHub Actions, Docker/VPS/systemd, env var docs, migrations, health checks, and rollback plans.

Required return format:
- Infra status: done / blocked / needs approval
- Changes made:
- Commands run:
- Health checks:
- Rollback plan:
- Human approval needed:

Production deploys and destructive migrations need explicit human approval. Never print secrets.
""",
}


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def run(cmd: list[str], *, dry_run: bool = False, env: dict[str, str] | None = None) -> int:
    print("$", " ".join(cmd))
    if dry_run:
        return 0
    try:
        return subprocess.call(cmd, env=env)
    except FileNotFoundError:
        eprint(f"missing command: {cmd[0]}")
        return 127


def profile_root(hermes_home: Path, target_profile: str) -> Path:
    if target_profile == "default":
        return hermes_home
    return hermes_home / "profiles" / target_profile


def skill_dest(root: Path) -> Path:
    return root / "skills" / SKILL_CATEGORY / SKILL_NAME


def validate_source(source: Path) -> None:
    if not source.exists():
        raise SystemExit(f"source does not exist: {source}")
    if not (source / "SKILL.md").is_file():
        raise SystemExit(f"source is not a Hermes skill directory; missing SKILL.md: {source}")


def install_skill(source: Path, dest: Path, *, force: bool, dry_run: bool) -> None:
    source = source.resolve()
    dest = dest.expanduser().resolve()
    validate_source(source)

    if source == dest:
        print(f"already installed: {dest}")
        return

    print(f"source: {source}")
    print(f"destination: {dest}")

    if dry_run:
        print("dry-run: no files copied")
        return

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(f".{dest.name}.tmp-{int(time.time())}")
    backup = dest.with_name(f"{dest.name}.backup-{int(time.time())}")

    shutil.copytree(source, tmp, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))

    if dest.exists():
        if force:
            shutil.rmtree(dest)
        else:
            dest.rename(backup)
            print(f"backup created: {backup}")
    tmp.rename(dest)
    print(f"installed skill: {dest}")


def append_or_replace_role(profile_dir: Path, profile_name: str, *, dry_run: bool) -> None:
    soul = profile_dir / "SOUL.md"
    body = ROLE_BODIES.get(profile_name, f"# {profile_name}\n\nLoad skill: {SKILL_NAME}\n")
    marker_start = "\n<!-- CTO-AGENTESPRO-ROLE-START -->\n"
    marker_end = "\n<!-- CTO-AGENTESPRO-ROLE-END -->\n"
    block = f"{marker_start}{body.rstrip()}\n{marker_end}"

    if dry_run:
        print(f"dry-run: would update {soul}")
        return

    profile_dir.mkdir(parents=True, exist_ok=True)
    existing = soul.read_text(encoding="utf-8") if soul.exists() else ""
    if marker_start in existing and marker_end in existing:
        before = existing.split(marker_start, 1)[0]
        after = existing.split(marker_end, 1)[1]
        new_text = before.rstrip() + block + after
    else:
        new_text = existing.rstrip() + "\n" + block + "\n"
    soul.write_text(new_text, encoding="utf-8")
    print(f"updated profile role: {soul}")


def create_or_update_team_profiles(hermes_home: Path, source: Path, *, clone_from: str, force: bool, dry_run: bool) -> int:
    hermes_bin = shutil.which("hermes")
    if not hermes_bin:
        eprint("Hermes CLI not found; cannot create profiles. Install Hermes or omit --create-team-profiles.")
        return 127

    failures = 0
    hermes_env = dict(os.environ)
    hermes_env["HERMES_HOME"] = str(hermes_home)
    for name, desc in TEAM_PROFILES.items():
        profile_dir = hermes_home / "profiles" / name
        if not profile_dir.exists():
            code = run([
                hermes_bin,
                "profile",
                "create",
                name,
                "--clone",
                "--clone-from",
                clone_from,
                "--description",
                desc,
                "--no-alias",
            ], dry_run=dry_run, env=hermes_env)
            if code != 0:
                eprint(f"failed to create profile {name} (exit {code})")
                failures += 1
                continue
        else:
            print(f"profile exists: {profile_dir}")
            run([hermes_bin, "profile", "describe", name, "--text", desc], dry_run=dry_run, env=hermes_env)

        append_or_replace_role(profile_dir, name, dry_run=dry_run)
        install_skill(source, skill_dest(profile_dir), force=force, dry_run=dry_run)

    return 1 if failures else 0


def main() -> int:
    default_home = os.environ.get("HERMES_HOME", "~/.hermes")
    ap = argparse.ArgumentParser()
    ap.add_argument("--hermes-home", default=default_home, help="Hermes home root. Defaults to HERMES_HOME or ~/.hermes.")
    ap.add_argument("--target-profile", default="default", help="Profile to install into. 'default' installs into Hermes home root.")
    ap.add_argument("--install-root", default=None, help="Legacy override: install directly into this root's skills directory.")
    ap.add_argument("--create-team-profiles", "--create-profiles", action="store_true", help="Create/update the standard software-team Hermes profiles.")
    ap.add_argument("--clone-from", default="default", help="Source Hermes profile for team profile creation.")
    ap.add_argument("--source", default=None, help="Skill source dir; defaults to parent skill directory.")
    ap.add_argument("--force", action="store_true", help="Replace an existing install instead of backing it up.")
    ap.add_argument("--dry-run", action="store_true", help="Print actions without changing files.")
    args = ap.parse_args()

    hermes_home = Path(args.hermes_home).expanduser().resolve()
    source = Path(args.source).expanduser().resolve() if args.source else Path(__file__).resolve().parents[1]
    validate_source(source)

    target_root = Path(args.install_root).expanduser().resolve() if args.install_root else profile_root(hermes_home, args.target_profile)
    install_skill(source, skill_dest(target_root), force=args.force, dry_run=args.dry_run)

    if args.create_team_profiles:
        code = create_or_update_team_profiles(hermes_home, source, clone_from=args.clone_from, force=args.force, dry_run=args.dry_run)
        if code != 0:
            return code

    print("next: reload skills or start a new Hermes session with the target profile")
    print(f"installed path: {skill_dest(target_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
