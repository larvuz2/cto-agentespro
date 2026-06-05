#!/usr/bin/env python3
"""Install CTO-agentespro skill and optionally create Hermes profiles.

Usage:
  python3 install_cto_agentespro.py --install-root ~/.hermes
  python3 install_cto_agentespro.py --install-root ~/.hermes --create-profiles
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

TEAM_PROFILES = {
    "cto-agentespro": "Orchestrator profile. Loads cto-agentespro and coordinates Kanban/delegation.",
    "builder-agentespro": "Senior implementation profile for scoped coding tasks.",
    "reviewer-agentespro": "Code/security review profile.",
    "qa-agentespro": "Acceptance/browser QA profile.",
    "devops-agentespro": "Deployment/database/CI profile.",
}


def run(cmd: list[str]) -> int:
    print("$", " ".join(cmd))
    try:
        return subprocess.call(cmd)
    except FileNotFoundError:
        print(f"missing command: {cmd[0]}")
        return 127


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--install-root", default="~/.hermes", help="Hermes home/profile root")
    ap.add_argument("--create-profiles", action="store_true", help="Create Hermes profiles for the software team")
    ap.add_argument("--source", default=None, help="Skill source dir; defaults to parent skill directory")
    args = ap.parse_args()

    install_root = Path(args.install_root).expanduser()
    source = Path(args.source).expanduser() if args.source else Path(__file__).resolve().parents[1]
    dest = install_root / "skills" / "software-development" / "cto-agentespro"

    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, dest)
    print(f"installed skill: {dest}")

    if args.create_profiles:
        for name, desc in TEAM_PROFILES.items():
            code = run(["hermes", "profile", "create", name, "--clone", "default"])
            if code != 0:
                print(f"profile may already exist or Hermes CLI unavailable: {name}")
            note_dir = install_root / "profiles" / name
            note_dir.mkdir(parents=True, exist_ok=True)
            (note_dir / "ROLE.md").write_text(f"# {name}\n\n{desc}\n\nLoad skill: cto-agentespro\n", encoding="utf-8")
        print("profile creation attempted")

    print("next: /reload-skills or start a new Hermes session with -s cto-agentespro")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
