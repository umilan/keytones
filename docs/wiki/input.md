---
title: Input
summary: Playing notes: on-screen keys, computer keyboard, glide, touch gestures.
sources: [index.html, raw/git-history-v1.93.md]
updated: v1.93
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
- Drag the algorithm strip up/down → resize the keyboard (a press turns into a drag after 8 px).

## Mic default
The mic starts on load; audio resumes on the first tap/key (browser autoplay rules).
