# XHN IPA maintenance

This repository is a minimal fork of Paspartame/AltGallery. Upstream MIT license remains in `LICENSE`; retain it and attribute AltGallery and AltGen when redistributing. Python AltGen generates each source, its merge mode merges sources, and the existing Pages site renders the catalog.

The automatic update allowlist is Roam-Control, Lyricify-Mobile, and Swipt only. Keep their `config.toml` files aligned with validated metadata in the companion xhn-ipa seed/catalog and official release feeds. Roam-Control requires `com.roamcontrol` and minimum v0.9.9. Lyricify-Mobile tags use the strict `mobile-vX.Y.Z` form. Swipt tracks the official nightly release (`nightly` tag and `Swipt.ipa`); verify upstream release metadata for version/buildVersion/buildNumber before changing field extraction.

Run `./update.sh`, then `python3 tools/make_proxy.py` for the merged and per-app mirrors, and `python3 tools/build_site.py`. Review every URL in the direct and mirrored sources and verify the staged `_site/`. Swipt uses upstream AltGen version_source=ipa and downloads its IPA to inspect Info.plist.

## Recent Updates preview images

Hermes renders `apps/<App>/images/news.png` on demand with the single canonical implementation in `/opt/data/skills/altgallery-news-preview/scripts/`. The project Skill uses its isolated `.venv`; no image generation is part of GitHub Actions. This repository is trusted for project-level skills via `hermes skills trust <repo-root>`. `tools/render_news.py` and `update_news.sh` are compatibility adapters only; do not maintain a second renderer; the Skill is installed locally only and is not committed.

When adding an App, verify its upstream repository and official releases, IPA asset naming, Bundle ID, minimum iOS version, and official icon. Add `apps/<App>/config.toml`, `icon.png`, and concise name/tagline in `news.toml` (optional `[colors].accent` only when icon auto-detection is unsuitable). Add the folder to the hard-coded allowlist and all-app merge inputs in `update.sh`; touch app-specific metadata handling only when necessary. Run the existing AltGen flow for that App and review `apps.json` and the merge result. Render only the new App:

```bash
/opt/data/skills/altgallery-news-preview/.venv/bin/python \
  /opt/data/skills/altgallery-news-preview/scripts/regenerate_all.py \
  --root <repo-root> --only <App-directory>
```

Check the 1600×1200 PNG, text/layout/colors/icon, and that its path matches `apps.json` `imageURL`. Use `--dry-run` to check metadata resolution without writing images. Keep display copy in `news.toml`, never generated `apps.json`. Do not add rendering to `.github/workflows/update.yml`, `.github/workflows/pages.yml`, or any other workflow.
