---
title: Algorithms
summary: The 9 detection choices (M1–M5 single-note, P1–P4 chords, T1 test), strengths and weaknesses.
sources: [index.html (ALGO_INFO), bench/baseline-v1.60.md, raw/git-history-v1.93.md]
updated: v1.93
---

# Algorithms

Picked on the algorithm strip (hover / long-press a button for its card) or Settings > Algorithm.
Stars and notes come from `ALGO_INFO` in `index.html`, derived from the [bench](bench.md).

| id | name | kind | best for | watch out |
|---|---|---|---|---|
| fft | M1 FFT Peak | 1 note | clean whistle-like tones | grabs harmonics, reads mains hum |
| acf | M2 Autocorrelation | 1 note | singing / solo, quiet room | notes in broadband noise |
| amdf | M3 AMDF | 1 note | single notes in a noisy room | no chords |
| yin | M4 YIN | 1 note | **best single-note choice** (tuner method) | no chords by design |
| mpm | M5 MPM | 1 note | fast single-note lines | a few false notes in noise |
| hpcp | P1 HPCP | chords | chord colour / key | octave-blind, slower |
| nnls | P2 NNLS | chords | chords, full band | extra note a fifth away |
| cqtnmf | P3 CQT+NMF | chords | chords, quick changes | heaviest CPU |
| multif0 | P4 Multi-F0 | chords | **default, best all-rounder** | fast runs blur; 9th vs 5th in dense distortion |
| chroma-test | T1 | test | walks all 12 notes (0.6 s each) to check outputs | — |
| off | OFF | — | detection off | — |

Since v1.60 the chord algorithms share **noise-floor-relative spectral peaks** (and drop mains
hum on 50/60 Hz multiples): Multi-F0 chord F1 went 0.18 → 1.00 and works at any input level.

Single-note algorithms can only ever show one note, so only one held key can flash
"pressed + detected" with them — see [Colors](colors.md).
