---
title: Audio sources
summary: Listen to (None (muted) / Mic / App sound / Mic + app sound / File (audio)), devices, phone call mode, synth.
sources: [index.html, raw/git-history-v1.93.md]
updated: v1.107
---

# Audio sources

## Listen to (Settings > Detection, and the topbar mini picker)
| choice | detector hears |
|---|---|
| None (muted) | nothing — detection off |
| Mic | the microphone (default; starts on page load since v1.10) |
| App sound | the app's own synth routed straight in — no mic, no room noise; for checking accuracy on known notes |
| Mic + app sound | both (falls back to app sound without a mic) |
| File (audio) | a loaded audio/video file (wav, mp3, m4a, flac, ogg, mp4, mov, webm… — whatever the browser decodes), also played to the speakers; the player is a slim bar just below the top bar, shown only in this mode (v1.105); the last file is kept in IndexedDB (≤ 500 MB) and is back after a refresh — and File (audio) stays the input if it was (v1.107) |

The topbar picker shows the active source as icon + short name (MUTE / MIC / APP / M+A / FILE)
and opens the menu (v1.102). The status dot left of the title shows the state: green = listening, orange = a note is heard
now, red = error; its tooltip says LIVE / APP / FILE / MUTED (the separate LIVE badge was removed
in v1.95 — muting is *None (muted)* in the Listen-to picker).

## Devices
- **Audio in / out**: with nothing chosen, the device's **built-in** mic/speakers are preferred
  (MacBook… before a Continuity iPhone mic; iPhone mic on iPhone). An explicit "Default" is respected.
  Labels need mic permission, so lists fill after the mic starts.
- iPhone has no audio-out choice (iOS decides the route).

## Phone call mode (off)
Off = mic opened with `echoCancellation/noiseSuppression/autoGainControl: false` (clean input)
and, on iOS 17+, `navigator.audioSession.type = 'playback'` while the mic is off. On = call-style
processing (less of the app's own sound reaches the mic, lower quality).

## Synth
Waveforms: sine, triangle, square, sawtooth, reverse saw, pulse 25/12.5%, organ (custom
PeriodicWaves). Per-waveform peak level; all voices through a **limiter** (v1.20, fixed clipping
crackle). Release is click-free (`cancelAndHoldAtTime` + `setTargetAtTime`).

See [iOS](ios.md) for the crackle history.
