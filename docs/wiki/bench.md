---
title: Detection bench
summary: How detection accuracy is measured (bench/) and the headline results.
sources: [bench/README.md, bench/baseline-v1.60.md, raw/git-history-v1.93.md]
updated: v1.93
---

# Detection bench

`bench/` runs the **real app** in headless Chromium with a fake mic playing synthetic, labelled
WAV clips, logs every detection frame and scores it (F1 on pitch classes, onset/release latency,
ghost notes in noise and hum, wrong-note intervals, CPU per frame). Method and commands:
[`bench/README.md`](../../bench/README.md). Committed results: `bench/baseline-v*.md`, `bench/band-v*.md`.

Headline (v1.59/1.60 baseline, settled F1): single-note algorithms ~0.91 mono but ~0.1 on chords;
chord algorithms 0.94–1.00 on chords; P4 Multi-F0 1.00 chord avg. See [Algorithms](algorithms.md).

Use it before/after any detection change: `python3 bench/compare.py OLD NEW`.
