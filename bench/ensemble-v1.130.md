# Ensemble bench — v1.130

Can running several chord algorithms at once and combining them beat P4 Multi-F0 alone?
`node bench/ensemble_run.js` ran P1–P4 on **the same detection frames** of every clip (app defaults:
Speed 3, Gate −40 dB, Confidence 50%, Stability 2, gain +6 dB); `python3 bench/ensemble.py <run>` fused
them offline. Every rule, single algorithms included, goes through the same copy of the app's Stability
step, so rows are directly comparable (paired: same frames, no run-to-run variance between rows).

- **chord / band / mono F1**: settled F1 averaged over the chord clips (dyads, triads, sevenths), band clips
  (power, open, palm) and mono clips (sine, harmonic, piano, fast, piano in noise).
- **wrong notes %**: mean over those clips of (1 − precision): shown notes that weren't playing.
- **ms/frame p95**: summed cost of the algorithms the rule needs (headless desktop; phones slower).

| rule | chord F1 | band F1 | mono F1 | all notes F1 | wrong notes % | ghost noise % | ghost hum % | onset ms | ms/frame p95 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 HPCP | 0.94 | 0.82 | 0.85 | 0.87 | 12 | 0 | 0 | 130 | 0.5 |
| P2 NNLS | 0.99 | 0.89 | 0.84 | 0.89 | 19 | 0 | 0 | 130 | 0.4 |
| P3 CQT+NMF | 0.99 | 0.87 | 0.90 | 0.91 | 10 | 0 | 0 | 129 | 5.7 |
| P4 Multi-F0 | 1.00 | 0.92 | 0.86 | 0.91 | 17 | 0 | 0 | 130 | 0.4 |
| vote 2 of 4 | 1.00 | 0.92 | 0.87 | 0.92 | 15 | 0 | 0 | 130 | 6.6 |
| vote 3 of 4 | 0.99 | 0.91 | 0.88 | 0.92 | 11 | 0 | 0 | 130 | 6.6 |
| conf sum ≥ 1.5 | 0.96 | 0.86 | 0.88 | 0.90 | 11 | 0 | 0 | 130 | 6.6 |
| conf sum ≥ 2.0 | 0.94 | 0.82 | 0.85 | 0.87 | 12 | 0 | 0 | 130 | 6.6 |
| conf sum ≥ 2.5 | 0.88 | 0.74 | 0.86 | 0.83 | 11 | 0 | 0 | 130 | 6.6 |
| P4 + 1 other agrees | 1.00 | 0.93 | 0.87 | 0.92 | 14 | 0 | 0 | 130 | 6.6 |
| P4 + P1/P2 agrees (no P3) | 0.99 | 0.94 | 0.87 | 0.92 | 13 | 0 | 0 | 130 | 1.2 |
| vote 2 of 3 (P1 P2 P4) | 0.99 | 0.94 | 0.87 | 0.92 | 13 | 0 | 0 | 130 | 1.2 |

| rule | band_open | band_palm | band_power | dyads | levels | mono_fast | mono_harmonic | mono_piano | mono_sine | noise_only | piano_in_noise | sevenths | triads |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 HPCP | 0.76 | 0.84 | 0.87 | 1.00 | 0.84 | 0.27 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.87 | 0.96 |
| P2 NNLS | 0.91 | 0.92 | 0.83 | 1.00 | 0.91 | 0.35 | 1.00 | 0.90 | 1.00 | 1.00 | 0.94 | 0.99 | 0.99 |
| P3 CQT+NMF | 0.86 | 0.88 | 0.86 | 1.00 | 0.91 | 0.51 | 1.00 | 0.99 | 1.00 | 1.00 | 0.98 | 0.97 | 1.00 |
| P4 Multi-F0 | 0.94 | 0.89 | 0.92 | 1.00 | 0.91 | 0.31 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.99 | 1.00 |
| vote 2 of 4 | 0.94 | 0.93 | 0.90 | 1.00 | 0.91 | 0.36 | 1.00 | 0.99 | 1.00 | 1.00 | 0.98 | 1.00 | 1.00 |
| vote 3 of 4 | 0.91 | 0.89 | 0.93 | 1.00 | 0.91 | 0.42 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.96 | 1.00 |
| conf sum ≥ 1.5 | 0.84 | 0.86 | 0.89 | 1.00 | 0.88 | 0.42 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.89 | 0.99 |
| conf sum ≥ 2.0 | 0.77 | 0.83 | 0.85 | 1.00 | 0.84 | 0.27 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.85 | 0.96 |
| conf sum ≥ 2.5 | 0.66 | 0.77 | 0.78 | 0.98 | 0.79 | 0.28 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.73 | 0.91 |
| P4 + 1 other agrees | 0.95 | 0.92 | 0.94 | 1.00 | 0.91 | 0.36 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.99 | 1.00 |
| P4 + P1/P2 agrees (no P3) | 0.95 | 0.92 | 0.94 | 1.00 | 0.91 | 0.36 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 | 1.00 |
| vote 2 of 3 (P1 P2 P4) | 0.95 | 0.92 | 0.94 | 1.00 | 0.91 | 0.36 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 | 1.00 |

## Reading
- **Combining helps a little, not a lot.** Best rules: band F1 0.92 → 0.94, wrong notes 17% → 13%,
  all-notes F1 0.91 → 0.92. Chord clips were already ~1.00.
- **"P4, confirmed by P1 or P2"** (= "2 of 3 of P1 P2 P4") is the best value: same accuracy as using all
  four, at 1.2 ms per frame instead of 6.6 ms (P3 alone costs 5.7 ms). That's cheap enough for any phone,
  so no workers or CPU calibration are needed for it.
- Summing confidences is worse than voting (the algorithms' confidence scales differ).
- **mono_fast** (8 notes/s) stays poor for every rule (0.27–0.51): a timing problem (window length /
  Stability), not one that voting fixes. That's where shorter analysis windows might help.
- Caveat: synthetic clips, one run. Differences of 0.01 are within what a different clip set could move.
