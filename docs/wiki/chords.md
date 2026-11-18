---
title: Chord names
summary: Names the chord of the sounding notes (detected or held) and shows it in the top bar after the tempo.
sources: [index.html (CHORD_TYPES, chordName, updateChordName, paintChord)]
updated: v1.128
---

# Chord names

Keytones names the chord of the notes sounding now and shows it in the top bar after the
tempo, in the Newest notes colour (e.g. **Cmaj7**, **Am**, **C/E**). After the notes stop, the last
chord stays dimmed for 2 s, then disappears.

Setting: **Settings > Detection > Chord names**, on by default (`keytones-chords-v1`).

## Which notes
The same notes the bars show (`paSoundingNow()`):
- **Listening** (mic / app sound / file): the detected notes. Use a P algorithm to hear chords
  (M algorithms detect one note at a time). Detectors often catch only part of a chord per
  check (multi-F0 on a C major chord: C+E in ~70% of checks, C+E+G in ~25%), so notes are gathered
  over the last **400 ms** (`CHORD_WINDOW_MS`). A note counts only once it has been detected **twice** in
  that window (`CHORD_MIN_HITS`), which drops one-off strays.
- **Muted** (Listen to: None): the keys you hold (on screen, computer keyboard, MIDI).

## Naming (`chordName`)
- At least 3 note names, or a root + fifth (power chord, **C5**). Other two-note intervals and
  single notes aren't named.
- Every note name present is tried as the root, and the set must match a chord type **exactly**:
  maj, m, 5, 7, maj7, m7, dim, aug, sus4, sus2, 6, m6, m7b5, dim7, mMaj7, 7sus4, add9, madd9, 9, maj9, m9,
  plus 7 / maj7 / m7 without the fifth.
- The lowest note is the bass. A root equal to the bass wins (C E G A → **C6**, not Am7/C);
  otherwise it's a slash chord (E G C → **C/E**). Ties go to the commoner type (list order).
- Anything that matches no type (clusters, chords with extra notes) shows nothing.

## Display (`updateChordName`, `paintChord`)
| rule | value |
|---|---|
| a new chord must hold before it's shown | 250 ms (`CHORD_MIN_MS`) |
| a drop-out shorter than this doesn't dim it | 300 ms (`CHORD_GAP_MS`) |
| last chord stays, dimmed, after the notes stop | 2 s (`CHORD_HOLD_MS`) |
| width | fixed 8 characters (6 on 320 px phones, long names end in …) so the top bar doesn't re-flow |

On 320 px phones, while a chord shows, the short title "KT" is hidden to make room.

## Accuracy
Chord naming itself is exact (21 test cases pass: triads, sevenths, sus, slash chords, power chords,
unnamed dyads and clusters). What it shows is only as good as detection: in a headless test of
app sound with multi-F0, C major and G7 read steadily. A minor read correctly most of the time,
but once switched to F when the detector kept reporting a stray F (the bars show it too).
Not measured with real instruments yet.
