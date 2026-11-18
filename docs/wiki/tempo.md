---
title: Tempo (BPM)
summary: Automatic tempo estimate from what the detector hears, shown as "### BPM" in the top bar.
sources: [index.html (tempoStart, tempoTick, tempoEstimate, tempoCalc, showBpm)]
updated: v1.124
---

# Tempo (BPM)

Keytones estimates the tempo of whatever the detector hears (mic, app sound or file, after
Gain) and shows it after the version in the top bar, e.g. **128 BPM** (no icon since v1.124). It's an estimate of the beat
in the last few seconds, not a metronome or beat grid.

| state | looks like |
|---|---|
| sure (recent estimates agree within 4%) | 128 BPM in normal text |
| still unsure | 128 BPM dimmed |
| too quiet / no attack for 2.5 s / Listen to: None / setting off | hidden |

On the narrowest phones (top bar `.micro`) only the number shows; the top bar hides the
version first to make room (`fitTopbar()` re-runs when the tempo appears or disappears).

Setting: **Settings > Detection > Tempo (BPM)**, on by default (`keytones-bpm-v1`).

## How it works
1. **Its own analyser**: `tempoStart()` adds a second AnalyserNode (fftSize 1024, no smoothing,
   −90…−10 dB) to the detector's input: `micGainNode`, `appTap`, `fileTap`. It doesn't touch
   the pitch analyser or Speed.
2. **Onset strength** every 10 ms (`tempoTick`): spectral flux, the sum of rises in the
   byte spectrum (bins up to ~8 kHz) since the previous read. Note attacks and drum hits
   spike it. The last 8 s are kept.
3. **Estimate** every 0.5 s (`tempoEstimate`): the flux goes on a 10 ms grid, the ±150 ms local
   average is removed (only the rises stay), then it's autocorrelated for lags of 60–200 BPM.
   The best local peak, weighted by a log-Gaussian around 120 BPM (σ = 1 octave), wins.
   Parabolic interpolation gives a fractional lag. It needs ≥ 4 s of history and a flux peak ≥ 40.
4. **Shown**: the median of the last 5 estimates (`tempoCalc`). It's "sure" when the peak holds
   > 35% of the onset energy and the last ≥ 3 estimates agree within 4%.

## Accuracy
Synthetic test files played through File (audio) all read correctly after about 4–5 s and
stayed stable: piano chords 128, eighth-note melody 90, drums (kick / snare / hi-hat) 100,
quarter notes 150. An earlier variant that also scored double the lag read the 90 BPM melody
as 60, so that term was removed in v1.122.

Known limits (not measured on real recordings yet):
- Half or double the real tempo can happen with sparse or very busy rhythms.
- Rubato or free playing has no steady beat, so it stays dim or jumps.
- With the mic, room noise and the app's own sound add attacks.
