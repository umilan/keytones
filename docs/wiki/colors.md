---
title: Colors
summary: Shared palette for screen, Launchpad and Launchkey; colour roles, newest, transitions, flashing.
sources: [index.html (PALETTE, COLOR_DEFAULTS), raw/git-history-v1.93.md]
updated: v1.126
---

# Colors

## One palette, three outputs
`PALETTE` maps each name to **web RGB**, **Launchpad RGB (0–127)** and a **Launchkey palette index**,
so a choice looks the same everywhere: red, orange, yellow, green, cyan, blue, purple, magenta,
white — plus **none** for every role.

| role | default | used for |
|---|---|---|
| Sounding notes (`detected`) | red | bars, key glow, pads of sounding notes; also the LP UI buttons (the title has no colour accent since v1.119) |
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

## UI hue (v1.125)
The app's own interface colours (not the note colours above) are all built from one root hue
at the top of `:root` in `index.html`:

| token | value | used for |
|---|---|---|
| `--ui-h` | `240` (blue-violet) | root: change it to re-tint the whole UI |
| `--ui-h-text` | `--ui-h` + 5 | light text, menu text, focus ring |
| `--ui-sat` | `1` (0–2) | tint strength: every UI saturation is multiplied by it (v1.126) |

Since v1.126 both are user settings: **Settings > Colors > UI hue** (0–359°, `keytones-ui-hue-v1`) and
**UI tint** (0–200%, `keytones-ui-tint-v1`), applied by `applyUiColor()` on load and by Reset colors.
Only saturation changes, never lightness, so text contrast barely moves: over every hue and tint up to
200% the main text stays ≥ 10:1 on the panel and menu text ≥ 9:1. The cap of 200% keeps every pair
within ~10% of the original contrast. The dark letters on white keys (`--ink`) are fixed (hue 252) and
don't follow the setting: a yellow hue would have dropped them from 3.1 to 2.5:1 on the cream.

Each tinted colour is `hsl(var(--ui-h) <sat> <light>)` with its original saturation and lightness,
so the look didn't change (screenshot diff: identical). Tokens: `--bar-bg`, `--top-bg`, `--strip-bg`,
`--col-bg`, `--key-bg`, `--panel-bg`, `--pop-bg` (menus / tips), `--track-bg` (slider / Gate meter),
`--bk-top` / `--bk-bot` / `--bk-flat` / `--bk-grad` (black keys), `--lp-pad` / `--lp-btn` /
`--lp-logo` (on-screen Launchpad), `--text`, `--dim`, `--text-hsl`, `--pop-text`, `--focus`,
`--chevron-col`. (`--ink`, the letters on white keys, is fixed since v1.126.)

Not tied to the hue: note colours (`--active-bg`, `--latest-bg`, palette), `--ok` / `--err`,
pure black `--bg`, the white-overlay scale (`--surface…`, `--border…`), the cream white keys,
and the chevron inside the native Settings `<select>`s (an SVG background with a fixed colour,
#c8c4ff at 40%).

