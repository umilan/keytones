---
title: Detection
summary: How notes are detected and how Gain, Gate, Speed, Confidence and Stability shape it.
sources: [index.html, bench/README.md, raw/git-history-v1.93.md]
updated: v1.140
---

# Detection

## Pipeline
`source → Gain → AnalyserNode` → every *Speed* ms `runDetection()`:
1. **Gate** — if the frame's RMS is below the gate (dB), nothing is detected
   (chord algorithms included since v1.2; before that P1–P4 fired on pure noise).
2. **Algorithm** — mono (`detectPitch`) returns one `{freq, conf}`; chord
   (`detectPitchPoly`) returns several. See [Algorithms](algorithms.md).
3. **Confidence** — `confThreshold(loose, old, strict)` maps the 0–100% slider onto each
   algorithm's own threshold (50% = the original value).
4. **Stability** — a note must be seen N checks in a row (mono `pendingTicks`, chords `polyStreak`).
   Exception (v1.140): a result marked `instant` skips the wait — P5 Ensemble marks notes all three of
   its methods hear (adaptive stability).
5. Shown: bars, keys, Launchpad, MIDI out; `noteConf[n]` keeps the confidence.

Time-domain algorithms read the **newest** 2048 samples of the analyser buffer (they read the
oldest until v1.42 — ~130 ms of extra lag).

## Speed levels
| level | interval | FFT size | smoothing |
|---|---|---|---|
| 1 | 100 ms | 8192 | 0.80 |
| 2 | 70 ms | 8192 | 0.60 |
| **3 (default)** | 50 ms | 4096 | 0.50 |
| 4 | 35 ms | 4096 | 0.30 |
| 5 | 25 ms | 2048 | 0.20 |
Measured at v1.42: YIN onset ~260 ms → ~95–145 ms at 3; Multi-F0 ~700 ms → ~190 ms at 3, ~75 ms at 5.
Faster = worse low notes and chords (smaller FFT can't separate low semitones).

## Newest notes
Notes starting within `LATEST_CHORD_MS` (250 ms) of each other form one newest chord.
Chord algorithms flicker, so a note only becomes newest after `LATEST_REARM_MS` (600 ms) of
silence. Played notes (keys, keyboard, MIDI in) become newest too; Launchpad pad presses don't.

## Confidence per algorithm (0–1)
FFT: peak height above the gate (/36 dB) · ACF: correlation · AMDF: dip depth · YIN: 1 − d′ ·
MPM: clarity · HPCP / NNLS / CQT: strength vs the strongest · Multi-F0: harmonic score vs the
strongest × its clarity.

## Gain and the gate meter
Gain is applied before detection, so the gate compares the gained signal. The Gate slider's
track is a live meter (same dB scale). Auto-gain (every 10 s, ±3 dB) never goes above +40 dB.

See also: [Detection bench](bench.md) for measured accuracy, [Audio sources](audio-sources.md).
