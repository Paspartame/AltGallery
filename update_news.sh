#!/usr/bin/env bash
# Compatibility adapter; rendering implementation lives in the project Skill.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "/opt/data/skills/altgallery-news-preview/.venv/bin/python" \
  "/opt/data/skills/altgallery-news-preview/scripts/regenerate_all.py" \
  --root "$SCRIPT_DIR" "$@"
