---
title: Launchpad
summary: Launchpad Mini MK3 programmer-mode support: layouts, colours, buttons, on-screen mirror.
sources: [index.html, raw/git-history-v1.93.md]
updated: v1.93
---

# Launchpad

Target: **Launchpad Mini MK3** (`LP_DEVICE_ID 0x0D`; X / Pro MK3 differ). Picked automatically
(MIDI in/out, the plain MIDI port). Selecting it switches the device into **Programmer Mode**
(SysEx `F0 00 20 29 02 0D 0E 01 F7`); colours are sent as RGB SysEx (`…03 03 led r g b F7`),
not the 128-colour palette. `setLaunchpadRGB()` also updates the on-screen Launchpad (`lpLeds`).

## Layouts (Keys / User buttons)
- **Piano** (default): 4 two-row octave bands (bottom row white keys, top row sharps, gaps at
  E–F / B–C). Each row ends with the **next octave's C** (fixed v1.37).
- **Fretboard**: isomorphic guitar-like grid.
Arrows: ▲▼ octave shift, ◀▶ transpose (each arrow lights in proportion to its own steps).

## What lights up
- Sounding notes: every octave of the note, fading with Decay.
- Full range: the newest note's exact-octave pad in the Newest colour.
- Notes played from keys / keyboard / MIDI in: their exact-octave pad in Pad press.
- Physical pad press: Pad press colour while held (none = off).
- Idle: C pads, ♯/♭ and natural glow sliders; unused pads off.
- Side column: waveform buttons (selected = Sounding colour, idle grey), bottom
  **Stop Solo Mute = reset** (white, ✕ on screen).

Pressing pads plays notes; layout / arrow / waveform / reset buttons work as on the device.
Fades are repainted at most every 50 ms; flashing sends updates every 100 ms.
