---
title: MIDI
summary: Web MIDI in/out, auto device selection, channels, transpose, monitor.
sources: [index.html, raw/git-history-v1.93.md]
updated: v1.93
---

# MIDI

- Web MIDI with SysEx (needed for the Launchpad). Permission is only requested when Settings is
  opened, or silently reused if already granted.
- **Auto-select**: with nothing chosen (or the saved device absent) a Launchpad / Launchkey is
  picked, also on hot-plug; an explicit "— None —" is respected. Choices are remembered by id, then name.
- **MIDI in**: notes play and display; channel filter (omni default). A Launchpad as input is
  handled as pads/buttons ([Launchpad](launchpad.md)).
- **MIDI out**: Launchpad → pad lighting; Launchkey → DAW pad lighting; anything else gets
  note on/off on the out channel, shifted by *MIDI out transpose*.
- **Monitor**: logs every message to the browser console.
