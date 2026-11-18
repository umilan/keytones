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

## [2026-11-18] ingest | v1.98 safe-area clipping
- Page clipped to the safe area with black masks; safe-area spacers black; theme-color #000.
- White corners in wrapper apps (e.g. MIDI browser) come from the host app outside the web view.
- Updated: ios.

## [2026-11-18] ingest | v1.99 no bar glow
- Bar glow / shadow removed (`barGlow()` returns none) in Piano and Pi-auto.
- Updated: views.

## [2026-11-18] ingest | v1.100 resizable Settings panel
- Drag the panel's left border to resize; no visual handle; width remembered.
- Updated: input.
