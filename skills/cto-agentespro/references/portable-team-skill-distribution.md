# Portable Team Skill Distribution

Use this when sharing CTO-agentespro with another Hermes VPS/profile.

## Required artifacts

- `cto-agentespro.md` — public Markdown reader that another agent can inspect before installing.
- `cto-agentespro-skill.tar.gz` — tarball containing only the skill directory.

## Build

From repo root:

```bash
python3 skills/cto-agentespro/scripts/package_skill.py
```

Publish to the Larvuz public pages repo:

```bash
python3 skills/cto-agentespro/scripts/package_skill.py --publish-dir /root/presentations/public-pages-deploy/skills
```

## Install command for another Hermes environment

```bash
set -euo pipefail
curl -fL https://larvuz2.github.io/skills/cto-agentespro-skill.tar.gz -o /tmp/cto-agentespro-skill.tar.gz
rm -rf /tmp/cto-agentespro
mkdir -p /tmp/cto-agentespro
tar -xzf /tmp/cto-agentespro-skill.tar.gz -C /tmp/cto-agentespro
python3 /tmp/cto-agentespro/cto-agentespro/scripts/install_cto_agentespro.py --target-profile default --create-team-profiles
```

## Verification checklist

Before saying it is ready:

- Public markdown URL returns 200 and contains `CTO-agentespro`.
- Public tarball URL returns 200 and is a gzip archive.
- Tarball extracts to `cto-agentespro/SKILL.md`.
- Installer compiles with `python3 -m py_compile`.
- Installer works into a temp root.
- `--dry-run --create-team-profiles` exits cleanly.
- Re-running installer from installed path does not delete itself.

## Safety

The installer should never silently destroy an existing install. It either backs up the old install or uses `--force` for replacement.
