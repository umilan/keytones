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

## [2026-11-18] ingest | v1.101 Chroma from spectral peaks
- Bars show > Chroma (Piano and Pi-auto) now sums only `spectralPeaks()` at their interpolated
  frequency. D3 at Speed 3: before C 24 / C# 87 / D 100 / E 39, after D 100 only.
- Updated: views.

## [2026-11-18] ingest | v1.102 Listen-to picker label
- "Audio file" renamed "File (audio)"; the topbar picker is a mini dropdown: icon + MUTE / MIC /
  APP / M+A / FILE + chevron.
- Updated: audio-sources, settings, overview.

## [2026-11-18] ingest | v1.105 slim file player
- The audio-file player moved from Settings > Detection to a one-row bar below the top bar
  (Load…, name, −15 / play / +15, seek, time); phones hide the file name.
- Updated: audio-sources.

## [2026-11-18] ingest | v1.106 panel resize on iOS
- Finger resize uses its own non-passive touch handlers with a 24 px grab band; pointer
  events stay for mouse / pen.
- Updated: input.

## [2026-11-18] ingest | v1.107 remember the last audio file
- The loaded file is saved in IndexedDB and restored after a refresh; Listen to: File (audio)
  is remembered too.
- Updated: audio-sources, architecture.

## [2026-11-18] ingest | v1.108 Key marks: Dots
- New setting Visualisation > Key marks: Fill / Dots; `body.key-dots` + `.key-dot` per key.
- Updated: views, settings.

## [2026-11-18] ingest | v1.109 dots on the Pi-auto strip
- Key marks: Dots also applies to the Pi-auto strip (pressed and flashing keys).
- Updated: views.

## [2026-11-18] ingest | v1.110 Key marks: Bar, Ring, Name
- Key marks now Fill / Dots / Bar / Ring / Name (a dropdown); body classes `km-alt` + `km-<mode>`.
- Updated: views, settings.

## [2026-11-18] ingest | v1.111 vertical Key marks bar
- Bar is now a vertical column from the top of the key, ending 36 px above the bottom at full length.
- Updated: views.

## [2026-11-18] ingest | v1.112 Key marks: Top edge
- New option: a fixed 5 px line across the top of the key, colours and fading like Dots.
- Updated: views, settings.

## [2026-11-18] ingest | v1.113 darker black keys
- Black key background darker in Piano (gradient #22222F→#121219) and Like bars (+40% black, was 25%).
- Updated: views.

## [2026-11-18] ingest | v1.114 Key marks bar grows upwards
- Bar now starts just above the label (36 px from the bottom) and grows up with confidence.
- Updated: views.

## [2026-11-18] ingest | v1.115 Key marks: Bottom edge (+ name)
- Bottom edge: 5 px line along the key's bottom (`.key-line`, `--mark` / `--glow` at `--press-t`).
  Bottom edge + name = `km-bottom` + `km-name`.
- Updated: views, settings.

## [2026-11-18] ingest | v1.116 GAIN drag: axis lock + touch
- Top-bar GAIN scrub locks to the first axis moved (horizontal or vertical) instead of summing
  dx + dy; touch uses non-passive touch events (window move/end) for iOS.
- Updated: input.

## [2026-11-18] ingest | v1.117 Listen-to menu: checkmark + contrast
- Active option shows a ✓ (`.lm-check`) and bold text; options use high-contrast text instead of `--dim`
  (about 10:1 instead of 3:1); focus outline; ↑/↓ keyboard navigation; focus starts on the active option.
- Updated: audio-sources.

## [2026-11-18] ingest | v1.118 Pi-auto strip marks detected notes
- With a Key marks mode other than Fill, detected notes get the mark on the Pi-auto mini keys too
  (`.pa-key.det`, colour = the note's bar: yellow newest/strongest, red otherwise).
- Updated: views.

## [2026-11-18] ingest | v1.119 Plain app title
- "tones" / "T" in the top-bar title no longer use the sounding-notes red (`.app-title-accent` inherits).
- Updated: colors.

## [2026-11-18] ingest | v1.120 Key marks: Both edges + name
- New Key marks option: top + bottom 5 px lines and the coloured letter (`edges-name` = km-bottom +
  km-edges + km-name); Pi-auto strip shows both edges. Key marks help text updated (Bar description fixed).
- Updated: views, settings.

## [2026-11-18] ingest | v1.121 Readable setting tips
- ⓘ tips render one option per line (bold name, hanging indent) from `\n`-separated `SETTING_INFO`
  texts; long multi-option texts rewritten that way; tip width 300 px.
- Updated: settings.

## [2026-11-18] ingest | v1.122 Tempo (BPM) auto-detection
- New: Settings > Detection > Tempo (BPM) (on). A second analyser on the detector input gives
  spectral flux every 10 ms; 8 s autocorrelation, 60–200 BPM, log-Gaussian prior at 120; median
  of 5; dim while unsure; hidden after 2.5 s without attacks. ♩BPM shown after the version.
- Tested with synthetic files (128 / 90 / 100 / 150 BPM): all correct after ~4–5 s.
- New page: tempo. Updated: settings, index.

## [2026-11-18] ingest | v1.123 Setting tips as tables
- Option lines in ⓘ tips render as a two-column grid (`.tip-grid`: `.tip-term` / `.tip-desc`), term left,
  explanation right (capitalised), row separators; tip width 340 px when it has options.
- Updated: settings.
