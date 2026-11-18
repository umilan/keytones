---
title: Settings
summary: Every setting, its default and what it does, grouped as in the panel.
sources: [index.html (SETTING_INFO), raw/git-history-v1.93.md]
updated: v1.122
---

# Settings

Order in the panel: **Visualisation → Detection → Colors → Audio → MIDI**. Every label has an
ⓘ with the explanation below (`SETTING_INFO` in `index.html` — keep both in sync).
The tip text is split into lines with `\n`: the first line is the lead; a later line `Name: text`
becomes an option row with **Name** in bold and a hanging indent (`infoTipNodes()`, v1.121).
Settings that can't apply right now are greyed out with the reason.

## Visualisation
| setting | default | does |
|---|---|---|
| View | Piano | Piano (12 bars) · Pi-auto (one bar per real note, grows by octaves) · LP (on-screen Launchpad) — also the topbar toggle. See [Views](views.md) |
| Bars show | Live | Live · Time · Count · Chroma — what bar height means. See [Views](views.md) |
| Keys | Piano | Piano (white/black) or Like bars (idle keys take the bar colours) |
| Key marks | Fill | Fill · Dots · Top edge · Bottom edge · Bottom edge + name · Both edges + name · Bar (length = confidence) · Ring · Name — how a lit key shows its colour |
| Decay | 50% | per-second shrink of stopped notes (bars, glows, pads). Sounding notes never shrink; played notes have no afterglow (v1.91) |
| Bar opacity = confidence | off | bar opacity = last detection confidence (Time / Count) |

## Detection
| setting | default | does |
|---|---|---|
| Listen to | Mic | None (muted) · Mic · App sound · Mic + app sound · File (audio). See [Audio sources](audio-sources.md) |
| Tempo (BPM) | on | estimate the tempo of what the detector hears; ♩BPM in the top bar. See [Tempo](tempo.md) |
| Detection | full range | 1 oct / full range — full range marks the exact octave on the Launchpad |
| Algorithm | P4 Multi-F0 | 9 choices, see [Algorithms](algorithms.md) |
| Gain | +50 dB | −40…+100 dB; auto-gain stays ≤ +40 dB |
| Gate | −40 dB | ignore quieter sound; slider shows the live level (white passes / grey blocked) |
| Speed | 3 (50 ms) | 1–5: check interval 100→25 ms, FFT 8192→2048, smoothing 0.8→0.2 |
| Confidence | 50% | scales each algorithm's own threshold; 50% = original values |
| Stability | 2 | checks in a row before a note counts |

Details and trade-offs: [Detection](detection.md).

## Colors
Sounding notes (red) · Newest notes (yellow) · Newest fades (2 s) · Transition (0.4 s) ·
*Pads:* C pads (white) · Pad press (magenta) · Idle ♯/♭ pads · Idle natural pads. Every
colour can be **none**. See [Colors](colors.md).

## Audio
Mic (on) · Phone call mode (off) · Sound (waveform) · Sound octave (3) · Audio in (built-in
mic preferred) · Audio out (built-in speakers preferred; not on iPhone). See
[Audio sources](audio-sources.md), [iOS](ios.md).

## MIDI
MIDI in / out (Launchpad / Launchkey picked automatically) · in channel (omni) · out channel ·
out transpose · monitor in console. See [MIDI](midi.md).
