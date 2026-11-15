# Keytones detection bench — v1.58

Settings: speed 3, gate -40 dB, confidence 50, stability 2, mic gain 6 dB. Run 20261115-210235, 881 s.

## Accuracy (F1 on pitch classes, settled = ≥250 ms away from note changes)

| algorithm | dyads | mono_fast | mono_harmonic | mono_piano | mono_sine | piano_in_noise | sevenths | triads | mono avg | chord avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M1 FFT | 0.67 | 0.21* | 1.00 | 1.00 | 0.99 | 1.00 | 0.40 | 0.50 | **0.84** | **0.52** |
| M2 ACF | 0.09 | 0.60* | 1.00 | 0.95 | 1.00 | 1.00 | 0.09 | 0.26 | **0.91** | **0.14** |
| M3 AMDF | 0.14 | 0.58* | 1.00 | 0.95 | 1.00 | 1.00 | 0.00 | 0.17 | **0.90** | **0.10** |
| M4 YIN | 0.18 | 0.59* | 1.00 | 0.95 | 1.00 | 1.00 | 0.00 | 0.17 | **0.91** | **0.12** |
| M5 MPM | 0.20 | 0.60* | 1.00 | 0.95 | 1.00 | 1.00 | 0.00 | 0.22 | **0.91** | **0.14** |
| P1 HPCP | 0.92 | 0.27* | 0.99 | 0.92 | 0.96 | 1.00 | 0.67 | 0.85 | **0.83** | **0.81** |
| P2 NNLS | 0.73 | 0.29* | 0.59 | 0.56 | 0.61 | 0.59 | 0.73 | 0.83 | **0.53** | **0.76** |
| P3 CQT+NMF | 0.74 | 0.61* | 0.56 | 0.51 | 0.62 | 0.55 | 0.72 | 0.86 | **0.57** | **0.77** |
| P4 Multi-F0 | 0.39 | 0.24* | 0.58 | 0.77 | 0.48 | 0.79 | 0.05 | 0.11 | **0.57** | **0.18** |

\* no frames are 250 ms away from a note change (fast notes), so this is the overall F1.

## Overall F1 (every frame, including note changes) and before/after Stability

| algorithm | dyads | mono_fast | mono_harmonic | mono_piano | mono_sine | piano_in_noise | sevenths | triads | avg | avg raw (no Stability) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M1 FFT | 0.62 | 0.21 | 0.67 | 0.80 | 0.67 | 0.81 | 0.38 | 0.48 | 0.58 | 0.68 |
| M2 ACF | 0.14 | 0.60 | 0.90 | 0.90 | 0.91 | 0.88 | 0.08 | 0.26 | 0.58 | 0.67 |
| M3 AMDF | 0.14 | 0.58 | 0.92 | 0.90 | 0.92 | 0.95 | 0.00 | 0.16 | 0.57 | 0.65 |
| M4 YIN | 0.17 | 0.59 | 0.88 | 0.89 | 0.90 | 0.94 | 0.00 | 0.16 | 0.57 | 0.65 |
| M5 MPM | 0.20 | 0.60 | 0.88 | 0.90 | 0.89 | 0.92 | 0.00 | 0.21 | 0.58 | 0.66 |
| P1 HPCP | 0.89 | 0.27 | 0.79 | 0.84 | 0.76 | 0.85 | 0.68 | 0.83 | 0.74 | 0.80 |
| P2 NNLS | 0.71 | 0.29 | 0.51 | 0.49 | 0.52 | 0.47 | 0.72 | 0.81 | 0.57 | 0.57 |
| P3 CQT+NMF | 0.73 | 0.61 | 0.49 | 0.49 | 0.54 | 0.42 | 0.71 | 0.85 | 0.60 | 0.56 |
| P4 Multi-F0 | 0.46 | 0.24 | 0.52 | 0.68 | 0.42 | 0.70 | 0.09 | 0.21 | 0.41 | 0.48 |

## Timing, false notes, cost

| algorithm | notes shown | onset median | onset p90 | release median | ghost (noise clip) | wrong-note share | top wrong interval | detect ms (p95) |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| M1 FFT | 82% |  140ms |  185ms |  189ms | 42% | 28% | M7 (57%) | 1.1 |
| M2 ACF | 72% |   89ms |   91ms |   41ms | 23% | 28% | M2 (44%) | 3.3 |
| M3 AMDF | 66% |   91ms |   91ms |   41ms | 0% | 33% | m2 (46%) | 3.4 |
| M4 YIN | 64% |   89ms |  129ms |   41ms | 0% | 24% | m2 (41%) | 4.3 |
| M5 MPM | 66% |   81ms |   91ms |   69ms | 10% | 34% | m2 (51%) | 4.4 |
| P1 HPCP | 98% |  139ms |  142ms |   42ms | 0% | 18% | M7 (37%) | 1.6 |
| P2 NNLS | 100% |   89ms |  106ms |   80ms | 86% | 57% | m2 (48%) | 2.5 |
| P3 CQT+NMF | 100% |   89ms |   91ms |   41ms | 86% | 51% | m2 (48%) | 8.6 |
| P4 Multi-F0 | 88% |  139ms |  190ms |   40ms | 0% | 36% | m2 (43%) | 1.4 |

## Input level (the same phrase at rising loudness; level after the +6 dB mic gain)

| algorithm | -36 dBFS | -30 dBFS | -24 dBFS | -18 dBFS | -12 dBFS | -6 dBFS | works from |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1 FFT | 0.18 | 0.87 | 0.83 | 0.75 | 0.72 | 0.72 | -30 dBFS |
| M2 ACF | 0.84 | 0.90 | 0.90 | 0.86 | 0.90 | 0.86 | -36 dBFS |
| M3 AMDF | 0.89 | 0.95 | 0.95 | 0.93 | 0.90 | 0.90 | -36 dBFS |
| M4 YIN | 0.89 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | -36 dBFS |
| M5 MPM | 0.89 | 0.95 | 0.95 | 0.93 | 0.95 | 0.90 | -36 dBFS |
| P1 HPCP | 0.00 | 0.03 | 0.45 | 0.64 | 0.82 | 0.82 | -12 dBFS |
| P2 NNLS | 0.58 | 0.73 | 0.84 | 0.84 | 0.88 | 0.84 | -30 dBFS |
| P3 CQT+NMF | 0.56 | 0.70 | 0.79 | 0.82 | 0.83 | 0.82 | -30 dBFS |
| P4 Multi-F0 | 0.00 | 0.00 | 0.00 | 0.06 | 0.43 | 0.67 | never |

The app's auto-gain keeps the average input between roughly −28 and −13 dBFS rms. "works from" = the quietest level with F1 ≥ 0.70. Mono algorithms (M1–M5) are scored on the phrase's single notes only.

Notes: mono algorithms (M1–M5) can only ever show one note, so their chord recall is capped. "wrong-note share" = shown notes that were not playing (1 − precision) on the note clips; "top wrong interval" = how far those wrong notes were from the real ones (P5/P4 = harmonics).

