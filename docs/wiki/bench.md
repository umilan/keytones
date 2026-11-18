---
title: Detection bench
summary: How detection accuracy is measured (bench/) and the headline results.
sources: [bench/README.md, bench/baseline-v1.60.md, raw/git-history-v1.93.md]
updated: v1.135
---

# Detection bench

`bench/` runs the **real app** in headless Chromium with a fake mic playing synthetic, labelled
WAV clips, logs every detection frame and scores it (F1 on pitch classes, onset/release latency,
ghost notes in noise and hum, wrong-note intervals, CPU per frame). Method and commands:
[`bench/README.md`](../../bench/README.md). Committed results: `bench/baseline-v*.md`, `bench/band-v*.md`, `bench/ensemble-v*.md`, `bench/p5-v*.md`, `bench/windows-v*.md`.

Headline (v1.59/1.60 baseline, settled F1): single-note algorithms ~0.91 mono but ~0.1 on chords;
chord algorithms 0.94–1.00 on chords; P4 Multi-F0 1.00 chord avg. See [Algorithms](algorithms.md).

Use it before/after any detection change: `python3 bench/compare.py OLD NEW`.

## Ensemble test (v1.130)
Question: would running several chord algorithms at once and combining them beat P4 alone?
`bench/ensemble_run.js` records P1–P4 on the same frames; `bench/ensemble.py` fuses them through the
app's Stability rule and scores with `score.py`. Result (`bench/ensemble-v1.130.md`):

| rule | band F1 | all notes F1 | wrong notes % | ms/frame |
|---|---:|---:|---:|---:|
| P4 Multi-F0 alone | 0.92 | 0.91 | 17 | 0.4 |
| vote 2 of 4 | 0.92 | 0.92 | 15 | 6.6 |
| P4, confirmed by P1 or P2 | **0.94** | **0.92** | **13** | 1.2 |

A small gain. The cheap rule (no P3) is as good as all four at a fifth of the cost, so it needs no
workers or CPU calibration. Fast notes (mono_fast, 8/s) stay poor for every rule: a timing problem.
Synthetic clips, one run.

In the real app (`bench/p5-v1.132.md`) P5 confirmed it: band F1 0.91 → 0.93, wrong notes 16% → 13%,
same onset, faster release. P5 became the default in v1.133. If Python Playwright doesn't match the
installed browser, run with `KT_CHROMIUM=/path/to/chrome`.

## Windows and adaptive stability (v1.134)
`ensemble_run.js --windows 2048,8192` + `bench/windows.py` (`bench/windows-v1.134.md`): fast notes
(8/s) are held back by Stability, not by the window. Letting a note through on its first frame when all
three P5 algorithms agree lifts fast notes 0.36 → 0.53 and onset 116 → 81 ms at no extra CPU (wrong notes
13 → 14%, two 50 ms flashes when noise starts). The long window (8192) gives the best band score (0.98) but
loses fast notes entirely; the short one (2048) is worse almost everywhere.
