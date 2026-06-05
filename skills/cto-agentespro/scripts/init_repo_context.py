#!/usr/bin/env python3
"""Bootstrap repo context files for CTO-agentespro.

Run from the root of a software repo:
  python3 ~/.hermes/skills/software-development/cto-agentespro/scripts/init_repo_context.py

It creates:
- AGENTS.md from the CTO-agentespro template if missing
- .hermes/project-brief.md if requested
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def copy_if_missing(src: Path, dest: Path, *, force: bool, dry_run: bool) -> None:
    if dest.exists() and not force:
        print(f"exists, skipped: {dest}")
        return
    print(f"copy {src} -> {dest}")
    if dry_run:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", help="Target repo root. Defaults to current directory.")
    ap.add_argument("--brief", action="store_true", help="Also create .hermes/project-brief.md")
    ap.add_argument("--force", action="store_true", help="Overwrite existing files")
    ap.add_argument("--dry-run", action="store_true", help="Show what would happen")
    args = ap.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    templates = skill_dir / "templates"
    repo = Path(args.repo).expanduser().resolve()

    if not repo.exists():
        print(f"repo does not exist: {repo}")
        return 2

    copy_if_missing(templates / "AGENTS.md", repo / "AGENTS.md", force=args.force, dry_run=args.dry_run)
    if args.brief:
        copy_if_missing(templates / "project-brief.md", repo / ".hermes" / "project-brief.md", force=args.force, dry_run=args.dry_run)

    print("repo context bootstrap complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
