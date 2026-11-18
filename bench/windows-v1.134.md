# Windows & adaptive stability bench — v1.134

Can P5 (P4 Multi-F0 confirmed by P1 HPCP or P2 NNLS) do better with other analysis windows, several
windows at once, or a smarter Stability? `node bench/ensemble_run.js --algos hpcp,nnls,multif0
--windows 2048,8192` ran the three algorithms on the app's own window (4096 at Speed 3) and on 2048 / 8192
analysers (same input and smoothing) on the same frames; `python3 bench/windows.py <run>` fused them. App
defaults otherwise (Stability 2). Adaptive rules: a note shows on its first frame when enough sources
(algorithm × window) agree, otherwise after Stability frames.

| rule | mono_fast F1 | chord F1 | band F1 | mono F1 | all F1 (every frame) | wrong notes % | ghost noise / hum % | onset median ms | ms/frame p95 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P5 @4096 (today) | 0.36 | 0.99 | 0.93 | 0.87 | 0.84 | 13 | 0 / 0 | 116 | 1.2 |
| P5 @2048 (short) | 0.43 | 0.89 | 0.59 | 0.89 | 0.75 | 13 | 0 / 14 | 90 | 0.7 |
| P5 @8192 (long) | 0.03 | 1.00 | 0.98 | 0.81 | 0.79 | 20 | 0 / 0 | 140 | 2.5 |
| P5 @4096, Stability 1 | 0.62 | 0.99 | 0.93 | 0.93 | 0.88 | 15 | 0 / 0 | 66 | 1.2 |
| P5 in 2 of 3 windows | 0.37 | 0.99 | 0.94 | 0.87 | 0.85 | 12 | 0 / 0 | 116 | 4.0 |
| P5 @2048 ∪ @4096 | 0.38 | 0.98 | 0.92 | 0.87 | 0.85 | 15 | 0 / 14 | 90 | 1.9 |
| low ≤ oct 3 @8192, rest @4096 | 0.36 | 1.00 | 0.95 | 0.87 | 0.83 | 16 | 0 / 0 | 130 | 3.3 |
| low ≤ oct 3 @8192, rest @2048 | 0.40 | 0.98 | 0.94 | 0.88 | 0.83 | 15 | 0 / 0 | 91 | 3.0 |
| adaptive: P5 @4096, instant if 3/3 algos (no extra window) | 0.53 | 0.99 | 0.94 | 0.91 | 0.87 | 14 | 0 / 0 | 81 | 1.2 |
| adaptive: P5 @4096, instant if ≥6/9 | 0.55 | 0.99 | 0.94 | 0.91 | 0.88 | 14 | 0 / 0 | 81 | 4.0 |
| adaptive: P5 @4096, instant if ≥5/9 | 0.62 | 0.99 | 0.94 | 0.93 | 0.89 | 14 | 0 / 0 | 79 | 4.0 |
| adaptive: ≥4/9 heard, instant ≥6/9 | 0.52 | 1.00 | 0.95 | 0.90 | 0.87 | 15 | 0 / 0 | 81 | 4.0 |
| adaptive: ≥3/9 heard, instant ≥6/9 | 0.49 | 0.99 | 0.95 | 0.88 | 0.85 | 20 | 0 / 14 | 81 | 4.0 |

| rule | band_open | band_palm | band_power | dyads | levels | mono_fast | mono_harmonic | mono_piano | mono_sine | noise_only | piano_in_noise | sevenths | triads |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P5 @4096 (today) | 0.95 | 0.93 | 0.93 | 1.00 | 0.91 | 0.36 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 | 1.00 |
| P5 @2048 (short) | 0.57 | 0.75 | 0.43 | 0.98 | 0.90 | 0.43 | 1.00 | 0.99 | 1.00 | 0.00 | 1.00 | 0.73 | 0.97 |
| P5 @8192 (long) | 0.98 | 0.99 | 0.97 | 1.00 | 0.91 | 0.03 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.99 | 1.00 |
| P5 @4096, Stability 1 | 0.95 | 0.93 | 0.92 | 1.00 | 0.91 | 0.62 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.98 | 1.00 |
| P5 in 2 of 3 windows | 0.95 | 0.94 | 0.94 | 1.00 | 0.91 | 0.37 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 | 1.00 |
| P5 @2048 ∪ @4096 | 0.93 | 0.92 | 0.92 | 0.99 | 0.90 | 0.38 | 1.00 | 0.99 | 1.00 | 0.00 | 1.00 | 0.95 | 0.99 |
| low ≤ oct 3 @8192, rest @4096 | 0.95 | 0.98 | 0.93 | 1.00 | 0.91 | 0.36 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| low ≤ oct 3 @8192, rest @2048 | 0.89 | 0.98 | 0.95 | 1.00 | 0.90 | 0.40 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.96 | 0.98 |
| adaptive: P5 @4096, instant if 3/3 algos (no extra window) | 0.95 | 0.93 | 0.93 | 1.00 | 0.91 | 0.53 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.98 | 1.00 |
| adaptive: P5 @4096, instant if ≥6/9 | 0.95 | 0.94 | 0.93 | 1.00 | 0.91 | 0.55 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.98 | 1.00 |
| adaptive: P5 @4096, instant if ≥5/9 | 0.95 | 0.94 | 0.94 | 1.00 | 0.91 | 0.62 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.98 | 1.00 |
| adaptive: ≥4/9 heard, instant ≥6/9 | 0.96 | 0.96 | 0.95 | 1.00 | 0.91 | 0.52 | 1.00 | 0.99 | 1.00 | 0.00 | 1.00 | 0.99 | 1.00 |
| adaptive: ≥3/9 heard, instant ≥6/9 | 0.95 | 0.97 | 0.94 | 1.00 | 0.90 | 0.49 | 1.00 | 0.93 | 1.00 | 0.00 | 0.96 | 0.97 | 1.00 |

## Reading
- **Fast notes are a Stability problem, not a window problem.** mono_fast (8 notes/s): P5 0.36; Stability 1
  0.62; short window alone only 0.43. Every rule that lets clear notes through on their first frame lifts it.
- **Adaptive, no extra window** (P5, but a note all three algorithms hear shows at once): mono_fast 0.36 → 0.53,
  single notes 0.87 → 0.91, onset 116 → 81 ms, band 0.93 → 0.94, chords unchanged, no extra CPU. Cost: wrong
  notes 13 → 14% and 2 single-frame (50 ms) flashes in 12 s of noise / hum, both when the noise starts.
- **Adaptive with all 3 windows** (instant if ≥ 5 of 9 sources): mono_fast 0.62, onset 79 ms, 1 flash; about
  3× the CPU (4.0 ms/frame desktop).
- **Long window (8192)**: best band F1 (0.98) and chords, but fast notes collapse (0.03) and wrong notes rise
  to 20%. Splitting by register (low notes from 8192) keeps some of the band gain (0.95), not all.
- **Short window (2048)**: worse almost everywhere (band 0.59) and reads mains hum.
- Combining windows by vote (2 of 3) changes little (0.93 → 0.94 band).
- Caveat: synthetic clips, one run.
