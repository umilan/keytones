---
title: Architecture
summary: How index.html is organised: state, audio graph, render loop, persistence.
sources: [index.html, raw/git-history-v1.93.md]
updated: v1.97
---

# Architecture

Everything — HTML, CSS, JS — lives in one file, [`index.html`](../../index.html) (~5,500 lines),
plus `manifest.json` and icons for the PWA. No build step, no dependencies.

## Layout of the page
- `#topbar` — status dot + title + version, GAIN scrub control, Listen-to mini picker,
  view toggle, settings button (the LIVE / MUTED badge was removed in v1.95, the DECAY control
  in v1.96 — Decay is set in Settings > Visualisation only).
  Icon buttons are `--ctrl-size` = 32 px (18 px icons) since v1.97; the GAIN box matches that height. Shortens labels on narrow screens (KT / DCY / G)
  instead of scrolling (`fitTopbar()`, levels `compact` → `tight` → `tiny`).
- `#bar-area` — the 12 bar columns (Piano), `#pa-view` (Pi-auto) or `#lp-view` (on-screen Launchpad).
- `#mic-strip` — algorithm buttons (or a compact picker); also the drag handle that resizes the keyboard.
- `#keyboard` — 12 keys (one octave, equal-width columns).
- `#settings-panel` — a flex sibling of `#app` that pushes the app aside (not an overlay).

## Audio graph
`AudioContext` (latency hint *balanced*, created **after** the mic opens, at the mic's sample
rate — an iOS crackle fix) →
- synth: per-note `Oscillator → Gain → limiter bus (DynamicsCompressor) → destination`;
- detection: `source (mic / app sound / file) → micGainNode (Gain) → AnalyserNode`;
  `runDetection()` runs every *Speed* ms on the analyser data.

## Core state (selected)
| variable | meaning |
|---|---|
| `mode` | `'outside'` = detection on, `'inner'` = only played notes |
| `lastNote`, `activePolyNotes` | notes detection hears now (mono / chord algorithms) |
| `latestNotes` | the newest note(s) — a set (chords) |
| `lpNoteBrightness`, `lpNotePlaying`, `lpNoteOctave` | per-note glow 0–1 (fades with Decay), shared by Launchpad pads **and** keys |
| `keyHeldOctaves`, `heldNoteCount` | notes held from keys / keyboard / MIDI in |
| `noteConf` | last detection confidence per note (0–1) |
| `detection` | `{gateDb, confidence, stability, speed}` |

## Persistence (localStorage, per browser)
Keys are prefixed `keytones-…-v1` (older `keymap-…` keys are still read for migration):
`colors`, `detection`, `view`, `bars`, `listen`, `call-mode`, `conf-opacity`,
`halftone-glow`, `natural-glow`, `newest-fade`, `color-fade`, `keys-look`; devices in
`keymap-device-prefs-v1`. Every access is wrapped in try/catch.

## Conventions in the code
- Comments explain *why*; settings code is grouped by its Settings section.
- New colour roles go through `PALETTE` (web RGB + Launchpad RGB + Launchkey index) — see [Colors](colors.md).
- Anything that lights a Launchpad goes through `setLaunchpadRGB()`, which also feeds the on-screen Launchpad.
