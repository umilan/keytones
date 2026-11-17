---
title: Overview
summary: What Keytones is, who it's for, and the main moving parts.
sources: [raw/git-history-v1.93.md, index.html]
updated: v1.93
---

# Overview

Keytones is a single-file web app (PWA) that **shows which notes are being played** —
from a microphone, the app's own synth, an audio file, a MIDI keyboard or a Novation
Launchpad / Launchkey — as bars over a piano keyboard, or on an on-screen Launchpad.
It also plays notes (on-screen keys, computer keyboard, MIDI in, Launchpad pads) and
lights connected controllers to match.

Live: <https://umilan.github.io/keytones/> · repo `umilan/keytones` · everything is in
[`index.html`](../../index.html). (Formerly "Keymap", renamed in v1.1.)

## Main parts
- **Input / sound** — notes you play: on-screen keys, computer keyboard, MIDI in,
  Launchpad pads, finger / mouse glide → [Input](input.md)
- **Detection** — what the detector hears (Listen to: mic, app sound, audio file),
  9 algorithms, Gain / Gate / Speed / Confidence / Stability → [Detection](detection.md),
  [Algorithms](algorithms.md), [Audio sources](audio-sources.md)
- **Visualisation** — View (Piano / Pi-auto / LP), Bars show (Live / Time / Count / Chroma),
  Decay, colours, newest notes, flashing → [Views](views.md), [Colors](colors.md)
- **Controllers** — Launchpad Mini MK3 programmer mode, Launchkey MK3/MK4 DAW mode,
  plain MIDI out → [Launchpad](launchpad.md), [Launchkey](launchkey.md), [MIDI](midi.md)
- **Settings** — every option with its meaning → [Settings](settings.md)
- **Platform quirks** — iPhone audio, notch, caching → [iOS](ios.md)
- **How it's built and shipped** → [Architecture](architecture.md), [Versioning & deploy](versioning-and-deploy.md),
  [Detection bench](bench.md)
