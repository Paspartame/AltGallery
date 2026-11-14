#!/usr/bin/env python3
"""Compatibility adapter for the canonical Skill renderer.

The legacy ``--out`` value is an app directory; image creation still uses the
Skill renderer and its curated metadata resolution.
"""
import argparse
from pathlib import Path
import runpy
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--out")
    args, remaining = parser.parse_known_args()
    if args.out is not None and "--icon" not in remaining:
        app_dir = Path(args.out).expanduser().resolve()
        root = next((p for p in (app_dir, *app_dir.parents) if (p / "apps").is_dir()), None)
        if root is None:
            raise SystemExit(f"error: cannot locate repository root for {app_dir}")
        canonical = root / "/opt/data/skills/altgallery-news-preview/scripts/regenerate_all.py"
        sys.argv = [str(canonical), "--root", str(root), "--only", app_dir.name,
                    "--legacy-out", str(app_dir)]
    else:
        canonical = Path(__file__).resolve().parents[1] / "/opt/data/skills/altgallery-news-preview/scripts/render_news.py"
        sys.argv = [str(canonical), *remaining]
    runpy.run_path(str(canonical), run_name="__main__")
