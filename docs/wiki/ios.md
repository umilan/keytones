---
title: iOS notes
summary: iPhone/iPad specifics: audio session, crackle fixes, notch, text size, caching.
sources: [raw/git-history-v1.93.md]
updated: v1.98
---

# iOS notes

- **Silent switch**: a looping silent `<audio>` on first touch makes Web Audio play even with the
  Ring/Silent switch on (v0, commit 6910373).
- **Dynamic Island / notch**: `viewport-fit=cover` + safe-area spacers; landscape keeps both
  sides clear; the closed Settings panel no longer leaves a strip by the notch (v1.6).
- **Text size**: `-webkit-text-size-adjust: 100%` — iOS enlarged text in landscape and labels
  overlapped (v1.18).
- **Crackle**: limiter bus + click-free release (v1.20); mic opened **before** the AudioContext,
  created at the mic's sample rate (v1.21); Phone call mode off + `audioSession.type` (v1.27).
- **No audio-out choice** (iOS routes itself).
- **Safe-area clipping** (v1.98): the page is clipped to the safe area — fixed black masks
  (`html::before/::after`, `body::before/::after`) cover the status bar / notch / home-indicator
  insets, the spacers are black and `theme-color` is `#000`, so no app colour shows there.
- **Caching**: home-screen apps and in-app browsers (e.g. a MIDI browser app) keep old versions —
  close and reopen, check the version in the title. White corners in such apps come from the
  host app, not from Keytones (page background is `#000`).
- Web MIDI isn't in iOS Safari; use a MIDI-capable browser app for Launchpad use on iPhone.
