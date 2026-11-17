---
title: Colors
summary: Shared palette for screen, Launchpad and Launchkey; colour roles, newest, transitions, flashing.
sources: [index.html (PALETTE, COLOR_DEFAULTS), raw/git-history-v1.93.md]
updated: v1.93
---

# Colors

## One palette, three outputs
`PALETTE` maps each name to **web RGB**, **Launchpad RGB (0–127)** and a **Launchkey palette index**,
so a choice looks the same everywhere: red, orange, yellow, green, cyan, blue, purple, magenta,
white — plus **none** for every role.

| role | default | used for |
|---|---|---|
| Sounding notes (`detected`) | red | bars, key glow, pads of sounding notes; also the "TONES" title accent and LP UI buttons |
| Newest notes (`latest`) | yellow | newest note(s) on keys, bars, pads |
| C pads (`cNote`) | white | idle C pads (octave anchors) on LP / LK |
| Pad press (`pressed`) | magenta | a held pad / key; none = no press lighting |
| Idle ♯/♭ pads, Idle natural pads | sliders | idle LP pad brightness (0–100% of white) |
| Newest fades | 2 s | newest blends into Sounding over time |
| Transition | 0.4 s | cross-fade time for colour changes (keys, bars, pads in 50 ms steps) |

"none" meanings: Sounding → neutral grey bars, pads stay idle · Newest → off · C → like other
pads · Pad press → no press colour. Reset colors restores all.

## Newest note rules
Full range detection: the newest note's **exact-octave** pad and its key show the Newest colour
and fade like other notes; 1 oct: every octave pinned until the next newest. Chords: several
newest notes at once. See [Detection](detection.md#newest-notes).

## Pressed + detected flashing (v1.89–1.90)
A note you hold that detection also hears flashes every **100 ms** (`FLASH_MS`) between Pad press
and its detected colour — keys, bars (Piano and Pi-auto), LP pads (real and on-screen). Colour
fades are skipped while flashing. With single-note algorithms only one held note can be detected.

Removed: Exact octave colour (v1.33), bar hit flash (v1.13).
