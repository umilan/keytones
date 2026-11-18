# Wiki log

Append-only, newest at the bottom. One entry per ingest / query that changed pages / lint.
Format: `## [YYYY-MM-DD] <op> | <subject>` then what changed.

## [2026-11-17] ingest | initial build at v1.93
- Sources: `raw/git-history-v1.93.md` (118 commits), `index.html` (SETTING_INFO, ALGO_INFO,
  PALETTE, defaults), `bench/README.md`, `bench/baseline-v1.60.md`.
- Created: index, overview, settings, views, colors, detection, algorithms, audio-sources,
  input, launchpad, launchkey, midi, ios, architecture, bench, versioning-and-deploy.

## [2026-11-18] ingest | v1.95 top bar
- LIVE / MUTED badge removed from the top bar; "None" in Listen to renamed "None (muted)".
- Updated: architecture, audio-sources, settings.

## [2026-11-18] ingest | v1.96 top bar
- DECAY scrub control removed from the top bar; Decay stays in Settings > Visualisation.
- Updated: architecture.

## [2026-11-18] ingest | v1.97 bigger top bar buttons
- `--ctrl-size` 24 → 32 px (icons 14 → 18 px, GAIN box same height; Listen-to menu rows and
  file-player buttons grow too).
- Updated: architecture.
