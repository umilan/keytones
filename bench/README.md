# Detection bench

Measures how well each pitch-detection algorithm finds the right notes, by
running the **real app** on audio whose notes are known.

Headless Chromium opens `index.html` with a fake microphone that plays a WAV
file (`--use-file-for-fake-audio-capture`), so the sound goes through exactly
the same path as a real mic: AudioContext → gain → AnalyserNode → detector →
Stability → shown notes. The app is not modified; the bench wraps
`runDetection()` from outside and logs every detection frame, then compares
the log with the clip's ground truth.

## Run

```sh
pip install playwright numpy && python3 -m playwright install chromium

python3 bench/make_fixtures.py          # writes bench/fixtures/ (≈15 MB, not committed)
python3 bench/run.py                    # every clip × every algorithm, ~15 min (real time)
python3 bench/run.py --algos yin,multif0 --clips triads,levels
python3 bench/run.py --speed 5 --stability 1 --gate -50 --confidence 30 --gain 12
python3 bench/score.py bench/results/<run>/   # re-score saved logs (after changing score.py)
python3 bench/score.py RUN_A RUN_B          # one report from several runs (later runs replace earlier pairs)
python3 bench/compare.py OLD NEW            # before → after per algorithm (OLD/NEW may be RUN_A+RUN_B)
python3 bench/run.py --app /tmp/old-worktree # test another version of index.html (e.g. git worktree add /tmp/old-worktree <commit>)
```

`bench/baseline-v*.md` are the committed reference results for a version.
Each run writes `bench/results/<timestamp>/`: `summary.md` (the tables),
`results.json` (all metrics) and `logs/` (every frame of every run).
Runs are real time, so keep `--parallel` at or below the number of CPU cores.

## Clips (synthetic, seeded — identical on every machine)

The band clips (`band.py`) use additive plucked strings strummed with real guitar voicings, a tanh amp and a cabinet filter, with bass and a kick/snare/hi-hat groove; the truth is the chord's pitch classes (drums and distortion products are not notes).

| clip | what |
|---|---|
| mono_sine | sine tones, chromatic C3–B4 |
| mono_harmonic | sustained harmonic tones (voice/organ-like), E2–D#5 |
| mono_piano | piano-like decaying notes (slightly inharmonic, weak low fundamentals), A1–C6 |
| mono_fast | piano-like scale run, 8 notes/s |
| dyads / triads / sevenths | piano-like 2-, 3-, 4-note chords incl. inversions |
| piano_in_noise | piano-like melody with pink noise at 15 dB SNR |
| noise_only | pink noise, then 50 Hz mains hum (scored separately) — nothing should be shown |
| levels | the same phrase at −42 … −12 dBFS rms, to find the quietest level that still works |
| band_power | distorted band (high gain): power chords + bass + drums, 1 bar each |
| band_open | crunchy band: open chords (G D Em C A E F#m Am F) + bass + drums |
| band_palm | high-gain palm-muted 8th-note chugs, chord change every 2 beats |

## Metrics (pitch classes C…B, as the app shows them)

- **F1 settled** – accuracy on frames at least 250 ms away from any note start/end
- **F1** – every frame, so latency at note changes counts against it; *raw* = before Stability
- **notes shown** – share of played notes the app showed at all
- **onset / release** – time until a note appears / disappears
- **ghost** – frames that show a note while nothing is playing
- **wrong-note share, top wrong interval** – false notes and how far they were from the real ones (P5/P4 usually means a harmonic was mistaken for a note)
- **detect ms** – CPU time per detection frame (headless desktop; phones are slower)

Default settings are the app's defaults (speed 3, gate −40 dB, confidence 50,
stability 2) with a +6 dB mic gain, which puts the clips in the middle of the
range the app's auto-gain aims for. Auto-gain itself is switched off during a
run so the level stays fixed.

## Not covered yet

Real instruments and rooms (labelled recordings, e.g. MAPS / GuitarSet), the
on-screen drawing (bars, decay, Launchpad view), and phone mic processing.
