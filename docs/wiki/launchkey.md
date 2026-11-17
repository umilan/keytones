---
title: Launchkey
summary: Launchkey MK3 / MK4 DAW-mode pad lighting (output only).
sources: [index.html, raw/git-history-v1.93.md]
updated: v1.93
---

# Launchkey

Launchkey MK3 and MK4 are supported for **pad lighting only** (no pad input).
- Out: the **DAW** port (`…DAW Out`, on Windows `MIDIOUT2 (…)`); in: the plain MIDI port.
  Both picked automatically.
- DAW mode on: note `0x9F 0x0C 0x7F` (channel 16); pads default to Session layout.
- 2×8 pads = one octave: bottom row white keys 112–119 (C at both ends), top row sharps 96–103
  (gaps 96, 99, 103 off).
- Colours are Launchkey palette indices from `PALETTE[...].lk`; C pads anchor octaves; the
  newest note stays in the Newest colour (pinned in 1 oct).
