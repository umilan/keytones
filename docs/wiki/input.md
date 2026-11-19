---
title: Input
summary: Playing notes: on-screen keys, computer keyboard, glide, touch gestures.
sources: [index.html, raw/git-history-v1.93.md]
updated: v1.136
---

# Input

## Computer keyboard (by physical key, `e.code`)
```
 W E   T Y U   O P   ]        ← sharps
A S D F G H J K L ; ' \       ← C D E F G A B C D E F G
              └ next octave ┘
```
Z / X = sound octave down / up (Sound octave). ↑ / ↓ = previous / next algorithm. Works on
QWERTY, QWERTZ, AZERTY…; Cmd/Ctrl/Alt shortcuts and typing in text fields are left alone.

## Glide (draw-playing)
Hold and move across keys, bar columns, the Pi-auto strip or on-screen Launchpad pads: the note
under the pointer plays, the previous one stops. Mouse / touchpad since v1.68; **fingers since
v1.93** (each finger independently; Pi-auto one at a time).

## Touch gestures
- Swipe in from the right screen edge (18 px zone) → open Settings.
- Swipe the panel right, tap ✕ / header → close; on phones (≤760 px) a tap on the app closes it.
- Drag the open panel's left border (±10 px with a mouse, ±24 px with a finger; no visible
  handle) → resize it (240 px – 90% of the
  window, max 900 px); remembered (`keytones-panel-width-v1`). Added v1.100; on iOS fingers use touch events
  (non-passive) since v1.106 — pointer events were cancelled by the panel's scrolling.
- Drag the algorithm strip up/down → resize the keyboard (a press turns into a drag after 8 px).
- Drag the top-bar gain value (right half of the source + gain control) sideways or up/down → change the gain (right / up = louder,
  0.25 dB per px). `initScrubDrag()` locks to the axis that moves first (after 4 px), so
  wobble on the other axis doesn't cancel the drag; fingers use non-passive touch events
  (v1.116) so iOS webviews (MIDI Web) don't scroll instead.

## Mic default
The mic starts on load; audio resumes on the first tap/key (browser autoplay rules).
