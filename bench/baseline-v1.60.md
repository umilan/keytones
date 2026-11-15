# Keytones detection bench — v1.59

Settings: speed 3, gate -40 dB, confidence 50, stability 2, mic gain 6 dB. Run 20261115-210235 + 20261115-215128, 1273 s.

## Accuracy (F1 on pitch classes, settled = ≥250 ms away from note changes)

| algorithm | dyads | mono_fast | mono_harmonic | mono_piano | mono_sine | piano_in_noise | sevenths | triads | mono avg | chord avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M1 FFT | 0.67 | 0.21* | 1.00 | 1.00 | 0.99 | 1.00 | 0.40 | 0.50 | **0.84** | **0.52** |
| M2 ACF | 0.09 | 0.60* | 1.00 | 0.95 | 1.00 | 1.00 | 0.09 | 0.26 | **0.91** | **0.14** |
| M3 AMDF | 0.14 | 0.58* | 1.00 | 0.95 | 1.00 | 1.00 | 0.00 | 0.17 | **0.90** | **0.10** |
| M4 YIN | 0.18 | 0.59* | 1.00 | 0.95 | 1.00 | 1.00 | 0.00 | 0.17 | **0.91** | **0.12** |
| M5 MPM | 0.20 | 0.60* | 1.00 | 0.95 | 1.00 | 1.00 | 0.00 | 0.22 | **0.91** | **0.14** |
| P1 HPCP | 1.00 | 0.27* | 1.00 | 1.00 | 1.00 | 1.00 | 0.86 | 0.96 | **0.85** | **0.94** |
| P2 NNLS | 1.00 | 0.35* | 1.00 | 0.89 | 1.00 | 0.94 | 0.99 | 0.99 | **0.84** | **0.99** |
| P3 CQT+NMF | 1.00 | 0.60* | 1.00 | 0.98 | 1.00 | 0.99 | 0.97 | 1.00 | **0.91** | **0.99** |
| P4 Multi-F0 | 1.00 | 0.31* | 1.00 | 1.00 | 1.00 | 1.00 | 0.99 | 1.00 | **0.86** | **1.00** |

\* no frames are 250 ms away from a note change (fast notes), so this is the overall F1.

## Overall F1 (every frame, including note changes) and before/after Stability

| algorithm | dyads | mono_fast | mono_harmonic | mono_piano | mono_sine | piano_in_noise | sevenths | triads | avg | avg raw (no Stability) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M1 FFT | 0.62 | 0.21 | 0.67 | 0.80 | 0.67 | 0.81 | 0.38 | 0.48 | 0.58 | 0.68 |
| M2 ACF | 0.14 | 0.60 | 0.90 | 0.90 | 0.91 | 0.88 | 0.08 | 0.26 | 0.58 | 0.67 |
| M3 AMDF | 0.14 | 0.58 | 0.92 | 0.90 | 0.92 | 0.95 | 0.00 | 0.16 | 0.57 | 0.65 |
| M4 YIN | 0.17 | 0.59 | 0.88 | 0.89 | 0.90 | 0.94 | 0.00 | 0.16 | 0.57 | 0.65 |
| M5 MPM | 0.20 | 0.60 | 0.88 | 0.90 | 0.89 | 0.92 | 0.00 | 0.21 | 0.58 | 0.66 |
| P1 HPCP | 0.96 | 0.27 | 0.80 | 0.91 | 0.80 | 0.84 | 0.85 | 0.94 | 0.80 | 0.86 |
| P2 NNLS | 0.96 | 0.35 | 0.81 | 0.82 | 0.80 | 0.78 | 0.96 | 0.96 | 0.81 | 0.85 |
| P3 CQT+NMF | 0.97 | 0.60 | 0.82 | 0.91 | 0.80 | 0.87 | 0.95 | 0.98 | 0.86 | 0.92 |
| P4 Multi-F0 | 0.97 | 0.31 | 0.79 | 0.87 | 0.80 | 0.83 | 0.97 | 0.97 | 0.81 | 0.86 |

## Timing, false notes, cost

| algorithm | notes shown | onset median | onset p90 | release median | ghost: pink noise | ghost: hum | wrong-note share | top wrong interval | detect ms (p95) |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| M1 FFT | 82% |  140ms |  185ms |  189ms | 0% | 100% | 28% | M7 (57%) | 1.1 |
| M2 ACF | 72% |   89ms |   91ms |   41ms | 56% | 0% | 28% | M2 (44%) | 3.3 |
| M3 AMDF | 66% |   91ms |   91ms |   41ms | 0% | 0% | 33% | m2 (46%) | 3.4 |
| M4 YIN | 64% |   89ms |  129ms |   41ms | 0% | 0% | 24% | m2 (41%) | 4.3 |
| M5 MPM | 66% |   81ms |   91ms |   69ms | 24% | 0% | 34% | m2 (51%) | 4.4 |
| P1 HPCP | 100% |  139ms |  141ms |   40ms | 0% | 0% | 15% | M2 (34%) | 1.8 |
| P2 NNLS | 100% |   91ms |  140ms |   40ms | 0% | 0% | 20% | P5 (43%) | 2.3 |
| P3 CQT+NMF | 100% |   89ms |  139ms |   40ms | 0% | 0% | 10% | P5 (60%) | 8.9 |
| P4 Multi-F0 | 100% |   91ms |  140ms |   41ms | 0% | 0% | 18% | M2 (18%) | 2.5 |

## Input level (the same phrase at rising loudness; level after the +6 dB mic gain)

| algorithm | -36 dBFS | -30 dBFS | -24 dBFS | -18 dBFS | -12 dBFS | -6 dBFS | works from |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1 FFT | 0.18 | 0.87 | 0.83 | 0.75 | 0.72 | 0.72 | -30 dBFS |
| M2 ACF | 0.84 | 0.90 | 0.90 | 0.86 | 0.90 | 0.86 | -36 dBFS |
| M3 AMDF | 0.89 | 0.95 | 0.95 | 0.93 | 0.90 | 0.90 | -36 dBFS |
| M4 YIN | 0.89 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | -36 dBFS |
| M5 MPM | 0.89 | 0.95 | 0.95 | 0.93 | 0.95 | 0.90 | -36 dBFS |
| P1 HPCP | 0.60 | 0.81 | 0.91 | 0.87 | 0.89 | 0.81 | -30 dBFS |
| P2 NNLS | 0.63 | 0.84 | 0.96 | 0.95 | 0.95 | 0.93 | -30 dBFS |
| P3 CQT+NMF | 0.64 | 0.84 | 0.95 | 0.97 | 0.97 | 0.97 | -30 dBFS |
| P4 Multi-F0 | 0.62 | 0.82 | 0.94 | 0.96 | 0.96 | 0.96 | -30 dBFS |

The app's auto-gain keeps the average input between roughly −28 and −13 dBFS rms. "works from" = the quietest level with F1 ≥ 0.70. Mono algorithms (M1–M5) are scored on the phrase's single notes only.

Notes: mono algorithms (M1–M5) can only ever show one note, so their chord recall is capped. "wrong-note share" = shown notes that were not playing (1 − precision) on the note clips; "top wrong interval" = how far those wrong notes were from the real ones (P5/P4 = harmonics).


## Change from v1.58

| algorithm | mono F1 | chord F1 | onset ms | wrong notes % | ghost noise % | ghost hum % | works from dBFS |
|---|---|---|---|---|---|---|---|
| M1 FFT | 0.84 | 0.52 | 140 | 28 | 0 | 100 | -30 |
| M2 ACF | 0.91 | 0.14 | 89 | 28 | 56 | 0 | -36 |
| M3 AMDF | 0.90 | 0.10 | 91 | 33 | 0 | 0 | -36 |
| M4 YIN | 0.91 | 0.12 | 89 | 24 | 0 | 0 | -36 |
| M5 MPM | 0.91 | 0.14 | 81 | 34 | 24 | 0 | -36 |
| P1 HPCP | 0.83 → **0.85** | 0.81 → **0.94** | 139 | 18 → **15** | 0 | 0 | -12 → **-30** |
| P2 NNLS | 0.53 → **0.84** | 0.76 → **0.99** | 89 → **91** | 57 → **20** | 100 → **0** | 100 → **0** | -30 |
| P3 CQT+NMF | 0.57 → **0.91** | 0.77 → **0.99** | 89 | 51 → **10** | 100 → **0** | 100 → **0** | -30 |
| P4 Multi-F0 | 0.57 → **0.86** | 0.18 → **1.00** | 139 → **91** | 36 → **18** | 0 | 0 | never → **-30** |
