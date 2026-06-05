#!/usr/bin/env python3
"""Build portable CTO-agentespro distribution artifacts.

Outputs:
- dist/cto-agentespro-skill.tar.gz
- dist/cto-agentespro.md

Optional publish target:
  python3 skills/cto-agentespro/scripts/package_skill.py --publish-dir /root/presentations/public-pages-deploy/skills
"""

from __future__ import annotations

import argparse
import shutil
import tarfile
from datetime import datetime, timezone
from pathlib import Path


def build_reader(skill: Path) -> str:
    parts: list[str] = []
    parts.append("# CTO-agentespro — Portable Public Reader\n")
    parts.append(f"Updated: {datetime.now(timezone.utc).isoformat()}\n")
    parts.append("Install package:\n\n```txt\nhttps://larvuz2.github.io/skills/cto-agentespro-skill.tar.gz\n```\n")
    parts.append("Paste this reader URL to another Hermes agent:\n\n```txt\nhttps://larvuz2.github.io/skills/cto-agentespro.md\n```\n")
    parts.append("## One-command install\n\n```bash\nset -euo pipefail\ncurl -fL https://larvuz2.github.io/skills/cto-agentespro-skill.tar.gz -o /tmp/cto-agentespro-skill.tar.gz\nrm -rf /tmp/cto-agentespro\nmkdir -p /tmp/cto-agentespro\ntar -xzf /tmp/cto-agentespro-skill.tar.gz -C /tmp/cto-agentespro\npython3 /tmp/cto-agentespro/cto-agentespro/scripts/install_cto_agentespro.py --target-profile default --create-team-profiles\n```\n")
    parts.append("## Core rule\n\nOne umbrella skill: `CTO-agentespro`. Builder, Reviewer, QA, and DevOps are internal roles/profiles, not separate top-level skills. Default coordination is Hermes Kanban + GitHub + repo context files. Jira is optional, not default.\n")
    parts.append("\n---\n\n")

    paths = [skill / "SKILL.md"]
    for sub in ["references", "templates", "scripts"]:
        paths.extend(sorted((skill / sub).glob("*")))

    for p in paths:
        if not p.is_file() or p.name.endswith(".pyc") or "__pycache__" in p.parts:
            continue
        rel = p.relative_to(skill)
        txt = p.read_text(errors="ignore")
        lang = "markdown" if p.suffix == ".md" else "yaml" if p.suffix in {".yaml", ".yml"} else "python" if p.suffix == ".py" else "text"
        parts.append(f"# File: `{rel}`\n\n```{lang}\n{txt}\n```\n\n---\n\n")
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=None, help="Repo root. Defaults to detected root from script path.")
    ap.add_argument("--publish-dir", default=None, help="Optional directory to copy artifacts into.")
    args = ap.parse_args()

    script = Path(__file__).resolve()
    skill = script.parents[1]
    repo = Path(args.repo).expanduser().resolve() if args.repo else script.parents[3]
    dist = repo / "dist"
    dist.mkdir(parents=True, exist_ok=True)

    tar_path = dist / "cto-agentespro-skill.tar.gz"
    reader_path = dist / "cto-agentespro.md"

    if tar_path.exists():
        tar_path.unlink()
    with tarfile.open(tar_path, "w:gz") as tf:
        tf.add(skill, arcname="cto-agentespro", filter=lambda info: None if "__pycache__" in info.name or info.name.endswith(".pyc") else info)

    reader_path.write_text(build_reader(skill), encoding="utf-8")

    print(f"built: {tar_path} ({tar_path.stat().st_size} bytes)")
    print(f"built: {reader_path} ({reader_path.stat().st_size} bytes)")

    if args.publish_dir:
        publish = Path(args.publish_dir).expanduser().resolve()
        publish.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(tar_path, publish / tar_path.name)
        shutil.copyfile(reader_path, publish / reader_path.name)
        print(f"published artifacts to: {publish}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
