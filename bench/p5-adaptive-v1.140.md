# P5 Ensemble adaptive — v1.140 (real app, bench/run.py)

Compared with non-adaptive P5 (bench/p5-v1.132.md): fast notes 0.36 → 0.52, single notes 0.87 → 0.90, onset 92 → 81 ms, band / chords unchanged, no ghosts; wrong notes 13 → 15%, release median 44 → 81 ms.

Settings: speed 3, gate -40 dB, confidence 50, stability 2, mic gain 6 dB. Run 20261119-091005, 132 s.

## Accuracy (F1 on pitch classes, settled = ≥250 ms away from note changes)

| algorithm | band_open | band_palm | band_power | dyads | mono_fast | mono_harmonic | mono_piano | mono_sine | piano_in_noise | sevenths | triads | mono avg | chord avg | band avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P5 Ensemble | 0.96 | 0.92 | 0.93 | 1.00 | 0.52* | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 | 1.00 | **0.90** | **0.99** | **0.93** |

\* no frames are 250 ms away from a note change (fast notes), so this is the overall F1.

## Overall F1 (every frame, including note changes) and before/after Stability

| algorithm | band_open | band_palm | band_power | dyads | mono_fast | mono_harmonic | mono_piano | mono_sine | piano_in_noise | sevenths | triads | avg | avg raw (no Stability) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P5 Ensemble | 0.93 | 0.89 | 0.89 | 0.99 | 0.52 | 0.81 | 0.89 | 0.83 | 0.87 | 0.97 | 0.99 | 0.87 | 0.88 |

## Timing, false notes, cost

| algorithm | notes shown | onset median | onset p90 | release median | ghost: pink noise | ghost: hum | wrong-note share | top wrong interval | detect ms (p95) |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| P5 Ensemble | 100% |   81ms |   91ms |   81ms | 0% | 0% | 15% | M7 (26%) | 3.1 |

## Input level (the same phrase at rising loudness; level after the +6 dB mic gain)

| algorithm | -36 dBFS | -30 dBFS | -24 dBFS | -18 dBFS | -12 dBFS | -6 dBFS | works from |
|---|---:|---:|---:|---:|---:|---:|---:|
| P5 Ensemble | 0.65 | 0.84 | 0.96 | 0.98 | 0.98 | 0.98 | -30 dBFS |

The app's auto-gain keeps the average input between roughly −28 and −13 dBFS rms. "works from" = the quietest level with F1 ≥ 0.70. Mono algorithms (M1–M5) are scored on the phrase's single notes only.

Notes: mono algorithms (M1–M5) can only ever show one note, so their chord recall is capped. "wrong-note share" = shown notes that were not playing (1 − precision) on the note clips; "top wrong interval" = how far those wrong notes were from the real ones (P5/P4 = harmonics).
