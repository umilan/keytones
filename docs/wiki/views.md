---
title: Views and bars
summary: View (Piano / Pi-auto / LP), Bars show modes, keys, Decay and reset.
sources: [index.html, raw/git-history-v1.93.md]
updated: v1.139
---

# Views and bars

## View
- **Piano** — 12 bars, one per note name, over a one-octave keyboard.
- **Pi-auto** — one bar per real note (C3, C4…) over a piano strip; starts with one octave,
  the first note picks it, notes outside add whole octaves (only grows; title tap resets).
- **LP** — an on-screen Launchpad Mini (9×9 incl. top/side buttons) showing exactly what a real
  one would, and playable (pads, arrows, Keys/User layouts, waveform buttons, ✕ = reset).
  Unlit pads are transparent; no frame or padding. See [Launchpad](launchpad.md).

Topbar toggle switches views; the choice is remembered. Since v1.137 it's a 2-icon toggle (`#view-btn`):
piano keys | Launchpad grid, the current one on a raised plate (v1.139). The keys half returns to the last piano view
(Piano or Pi-auto, its tooltip says which); Pi-auto vs Piano is picked in Settings > View.

## Bars show (default Live)
| mode | bar height |
|---|---|
| Live | notes sounding now, height = detector certainty; yellow = clearly strongest; falls back at the Decay rate |
| Time | how long each note has sounded (held time for played notes) |
| Count | how often each note started |
| Chroma | energy per note name before detection, from real spectral peaks only (v1.101 — low notes no longer leak into neighbouring semitones); detected notes in yellow |

Percent labels = share of the total (Time / Count) or the level (Live / Chroma). Bars have no glow or shadow (removed in v1.99).

## Keys
Keys mirror the detected state: each detected note's key glows in the Sounding colour (Newest
for the newest) and **fades with Decay in step with its Launchpad pads** (v1.92). In Live /
Chroma the key shows the bar colour while sounding. Held keys show the Pad press colour;
held + detected keys flash (see [Colors](colors.md)). *Keys: Like bars* makes idle keys match the bar columns. Black keys are a shade darker than white ones (Piano gradient
`#22222F→#121219`, Like bars = column colour + 40% black; darkened in v1.113).
*Key marks* (v1.108, v1.110): **Fill** (default, the whole key) · **Dots** (14 px dot near the top) · **Top edge** (a fixed 5 px
line across the top, fading like Dots — v1.112) · **Bottom edge** (the same line along the bottom) ·
**Bottom edge + name** (bottom line and coloured letter together — both v1.115) ·
**Both edges + name** (top and bottom lines plus the coloured letter; `km-bottom` + `km-edges` + `km-name`,
`.key-line` draws both edges as inset shadows; the Pi-auto strip gets both edges — v1.120) ·
**Bar** (a column growing **up** from 36 px above the key's bottom — clear of the label — as tall
as the last detection was certain, `--conf`; full length reaches 6 px below the top — v1.114) ·
**Ring** (3 px outline) · **Name** (only the note letter). With anything but Fill the keys keep their
idle look; states set `--mark` (drawn by `.key-dot`), the fading glow reshapes `::after` the same way. The Pi-auto strip
follows it (v1.109): dot, bar or ring on pressed / flashing keys (Name uses a dot there). Since
v1.118 notes detected from mic / app sound / file also get the mark (class `.det`, `--pa-mark` = their
bar's colour: newest/strongest yellow, the rest red); in Fill mode the strip still shows only played keys.

## Decay
Per-second shrink, applied every display frame (smooth, v1.70). Never applies to notes still
sounding (v1.49) and never to released played notes — they go straight back (v1.91).

## Reset
Tap the title, or the Launchpad's Stop Solo Mute (✕): clears bars, glows, pads (real and
on-screen) and newest notes; held / still-heard notes stay.
