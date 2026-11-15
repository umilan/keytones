# Keytones detection bench — v1.60

Settings: speed 3, gate -40 dB, confidence 50, stability 2, mic gain 6 dB. Run 20261115-223306, 275 s.

## Accuracy (F1 on pitch classes, settled = ≥250 ms away from note changes)

| algorithm | band_power | band_open | band_palm | mono avg | chord avg | band avg |
|---|---:|---:|---:|---:|---:|---:|
| M1 FFT | 0.67 | 0.50 | 0.67 | **  -  ** | **  -  ** | **0.61** |
| M2 ACF | 0.11 | 0.09 | 0.16 | **  -  ** | **  -  ** | **0.12** |
| M3 AMDF | 0.00 | 0.00 | 0.01 | **  -  ** | **  -  ** | **0.00** |
| M4 YIN | 0.00 | 0.00 | 0.00 | **  -  ** | **  -  ** | **0.00** |
| M5 MPM | 0.01 | 0.01 | 0.04 | **  -  ** | **  -  ** | **0.02** |
| P1 HPCP | 0.88 | 0.76 | 0.82 | **  -  ** | **  -  ** | **0.82** |
| P2 NNLS | 0.83 | 0.91 | 0.90 | **  -  ** | **  -  ** | **0.88** |
| P3 CQT+NMF | 0.87 | 0.85 | 0.89 | **  -  ** | **  -  ** | **0.87** |
| P4 Multi-F0 | 0.92 | 0.95 | 0.89 | **  -  ** | **  -  ** | **0.92** |

\* no frames are 250 ms away from a note change (fast notes), so this is the overall F1.

## v1.58 → v1.60 on the band clips (chord algorithms)

| algorithm | band F1 | onset ms | wrong notes % |
| P1 HPCP | 0.80 → **0.82** | 140 | 3 |
| P2 NNLS | 0.52 → **0.88** | 90 → **141** | 66 → **17** |
| P3 CQT+NMF | 0.43 → **0.87** | 60 → **140** | 72 → **9** |
| P4 Multi-F0 | 0.04 → **0.92** | 710 → **139** | 0 → **12** |

## Where the chord algorithms still go wrong (v1.60)

Most misses are the chord's **fifth** (B in E5), and most extra notes are a **whole step above the root** (F# in E5): the fifth's own fundamental and 2nd harmonic get lost in the crowded low end (distorted guitar + bass + kick), and its 3rd harmonic, left unexplained, reads as a note of its own. Two quick fixes were tried and measured (requiring a fundamental above 150 Hz; a sloped noise-floor fit for crowded octaves): neither beat v1.60, so neither was kept.
