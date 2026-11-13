# XHN IPA maintenance

This repository is a minimal fork of Paspartame/AltGallery. Upstream MIT license remains in `LICENSE`; retain it and attribute AltGallery and AltGen when redistributing. Python AltGen generates each source, its merge mode merges sources, and the existing Pages site renders the catalog.

The automatic update allowlist is Roam-Control, Lyricify-Mobile, and Swipt only. Keep their `config.toml` files aligned with validated metadata in the companion xhn-ipa seed/catalog and official release feeds. Roam-Control requires `com.roamcontrol` and minimum v0.9.9. Lyricify-Mobile tags use the strict `mobile-vX.Y.Z` form. Swipt tracks the official nightly release (`nightly` tag and `Swipt.ipa`); verify upstream release metadata for version/buildVersion/buildNumber before changing field extraction.

Run `./update.sh`, then `python3 tools/make_proxy.py` for the merged and per-app mirrors, and `python3 tools/build_site.py`. Review every URL in the direct and mirrored sources and verify the staged `_site/`. Never download IPA binaries as part of metadata checks.
