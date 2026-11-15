#!/usr/bin/env python3
"""Generate labelled test clips for the Keytones detection bench.

Every clip is a mono 48 kHz 16-bit WAV plus a JSON file with the ground truth:
a list of events {start, end, midi:[...], pcs:[...]} in seconds. Each clip
starts and ends with LEAD seconds of silence. Everything is synthetic and
seeded, so the same clips come out on every machine.

    python3 bench/make_fixtures.py            # writes bench/fixtures/
"""
import json
import os
import wave

import numpy as np

SR = 48000
LEAD = 1.0          # silence before the first and after the last event
PEAK_DBFS = -3.0
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
rng = np.random.default_rng(12345)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env_ar(n, attack=0.01, release=0.03):
    """flat note with short linear attack/release (no clicks)"""
    e = np.ones(n)
    a, r = int(attack * SR), int(release * SR)
    e[:a] = np.linspace(0, 1, a)
    e[-r:] *= np.linspace(1, 0, r)
    return e


def tone_sine(m, dur):
    t = np.arange(int(dur * SR)) / SR
    return np.sin(2 * np.pi * hz(m) * t) * env_ar(len(t))


def tone_harmonic(m, dur, partials=10):
    """organ/voice-like: sustained, harmonic partials with 1/n amplitudes"""
    t = np.arange(int(dur * SR)) / SR
    f0, x = hz(m), np.zeros_like(t)
    for n in range(1, partials + 1):
        if f0 * n > SR / 2 - 1000:
            break
        x += np.sin(2 * np.pi * f0 * n * t + rng.uniform(0, 2 * np.pi)) / n
    return x * env_ar(len(t))


def tone_piano(m, dur, partials=14):
    """piano-like: slightly stretched (inharmonic) partials, fast attack,
    exponential decay that is faster for higher partials and higher notes"""
    t = np.arange(int(dur * SR)) / SR
    f0, x = hz(m), np.zeros_like(t)
    B = 0.0004 * (1 + max(0, m - 60) / 24)               # inharmonicity
    base_decay = 0.6 + 0.04 * max(0, m - 40)
    for n in range(1, partials + 1):
        fn = f0 * n * np.sqrt(1 + B * n * n)
        if fn > SR / 2 - 1000:
            break
        amp = (1 / n ** 1.1) * rng.uniform(0.7, 1.0)
        if m < 48 and n == 1:
            amp *= 0.35                                   # weak fundamental on low notes, like real pianos
        x += amp * np.sin(2 * np.pi * fn * t + rng.uniform(0, 2 * np.pi)) * np.exp(-t * base_decay * (1 + 0.35 * n))
    return x * env_ar(len(t), attack=0.004, release=0.05)


def pink_noise(n):
    white = rng.standard_normal(n)
    f = np.fft.rfft(white)
    k = np.arange(len(f)); k[0] = 1
    p = np.fft.irfft(f / np.sqrt(k), n)
    return p / np.max(np.abs(p))


def hum(n, base=50.0):
    t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * base * k * t) / k for k in range(1, 6))


class Clip:
    def __init__(self, name, desc):
        self.name, self.desc, self.events, self.parts = name, desc, [], []

    def add(self, start, dur, midis, voice, gain=1.0):
        midis = list(midis)
        x = sum(voice(m, dur) for m in midis) / max(1, len(midis)) ** 0.5
        self.parts.append((LEAD + start, x * gain))
        self.events.append({'start': round(LEAD + start, 4), 'end': round(LEAD + start + dur, 4),
                            'midi': midis, 'pcs': sorted({m % 12 for m in midis})})

    def render(self, length=None, noise=None, snr_db=None):
        end = max([s + len(x) / SR for s, x in self.parts] + [LEAD + (length or 0)])
        y = np.zeros(int((end + LEAD) * SR))
        for s, x in self.parts:
            i = int(s * SR); y[i:i + len(x)] += x
        if noise is not None:
            nz = noise(len(y))
            body = slice(int(LEAD * SR), len(y) - int(LEAD * SR))   # noise only between the silences, so alignment still has an edge
            sig_rms = np.sqrt(np.mean(y[body] ** 2)) if np.any(y[body]) else 0.05
            nz_rms = np.sqrt(np.mean(nz[body] ** 2))
            target = sig_rms / (10 ** (snr_db / 20)) if snr_db is not None else 0.01
            mask = np.zeros(len(y)); mask[body] = 1
            ramp = int(0.02 * SR); mask[body.start:body.start + ramp] = np.linspace(0, 1, ramp)
            y += nz * (target / nz_rms) * mask
        y *= 10 ** (PEAK_DBFS / 20) / np.max(np.abs(y))
        return y


def build():
    clips = []

    c = Clip('mono_sine', 'pure sine tones, chromatic C3..B4, 0.4 s each')
    for i, m in enumerate(range(48, 72)):
        c.add(i * 0.5, 0.4, [m], tone_sine)
    clips.append((c, {}))

    c = Clip('mono_harmonic', 'sustained harmonic tones (voice/organ-like), chromatic E2..D#5, 0.4 s each')
    for i, m in enumerate(range(40, 76, 1)):
        c.add(i * 0.5, 0.4, [m], tone_harmonic)
    clips.append((c, {}))

    c = Clip('mono_piano', 'piano-like decaying notes, random A1..C6, 0.5 s each')
    for i, m in enumerate(rng.integers(33, 85, 30)):
        c.add(i * 0.6, 0.5, [int(m)], tone_piano)
    clips.append((c, {}))

    c = Clip('mono_fast', 'fast piano-like scale run, 8 notes/s, C4 major up and down twice')
    scale = [60, 62, 64, 65, 67, 69, 71, 72]
    run = (scale + scale[::-1][1:-1]) * 2
    for i, m in enumerate(run):
        c.add(i * 0.125, 0.12, [m], tone_piano)
    clips.append((c, {}))

    c = Clip('dyads', 'piano-like two-note intervals (3rds, 4ths, 5ths, 6ths), 1 s each')
    for i in range(14):
        root = int(rng.integers(45, 70)); iv = int(rng.choice([3, 4, 5, 7, 8, 9]))
        c.add(i * 1.2, 1.0, [root, root + iv], tone_piano)
    clips.append((c, {}))

    c = Clip('triads', 'piano-like major/minor triads in root position and inversions, 1.2 s each')
    for i in range(14):
        root = int(rng.integers(48, 64)); third = 4 if rng.random() < 0.5 else 3
        notes = [root, root + third, root + 7]
        inv = int(rng.integers(0, 3))
        for k in range(inv):
            notes[k] += 12
        c.add(i * 1.4, 1.2, notes, tone_piano)
    clips.append((c, {}))

    c = Clip('sevenths', 'piano-like 4-note 7th chords (maj7, 7, m7), 1.4 s each')
    shapes = [[0, 4, 7, 11], [0, 4, 7, 10], [0, 3, 7, 10]]
    for i in range(12):
        root = int(rng.integers(45, 60)); sh = shapes[int(rng.integers(0, 3))]
        c.add(i * 1.6, 1.4, [root + s for s in sh], tone_piano)
    clips.append((c, {}))

    c = Clip('noise_only', 'no notes: pink noise at -30 dBFS rms, then mains hum (50 Hz + harmonics); nothing should be detected')
    c_len = 12.0
    def noise_then_hum(n):
        half = n // 2
        a = pink_noise(n); b = hum(n)
        a /= np.sqrt(np.mean(a ** 2)); b /= np.sqrt(np.mean(b ** 2))
        return np.concatenate([a[:half], b[half:]])
    clips.append((c, {'length': c_len, 'noise': noise_then_hum, 'snr_db': None}))

    c = Clip('piano_in_noise', 'the mono_piano melody again, with pink noise at 15 dB SNR')
    rng2 = np.random.default_rng(777)
    for i, m in enumerate(rng2.integers(40, 80, 24)):
        c.add(i * 0.6, 0.5, [int(m)], tone_piano)
    clips.append((c, {'noise': pink_noise, 'snr_db': 15}))

    c = Clip('levels', 'same phrase (3 notes + 2 triads, piano-like) at -42, -36, -30, -24, -18, -12 dBFS rms')
    clips.append((c, {'levels': True}))

    return clips


LEVELS_DB = [-42, -36, -30, -24, -18, -12]


def render_levels(clip):
    """the same phrase repeated at rising loudness; each event gets a level_db tag"""
    r = np.random.default_rng(99)
    phrase = [(0.0, 0.5, [64]), (0.6, 0.5, [57]), (1.2, 0.5, [71]), (1.8, 1.2, [60, 64, 67]), (3.2, 1.2, [57, 60, 64])]
    seg_len = 4.8
    y = np.zeros(int((2 * LEAD + seg_len * len(LEVELS_DB)) * SR))
    for k, lvl in enumerate(LEVELS_DB):
        seg = np.zeros(int(seg_len * SR))
        for st, du, ms in phrase:
            x = sum(tone_piano(m, du) for m in ms) / len(ms) ** 0.5
            i = int(st * SR); seg[i:i + len(x)] += x
        active = seg[np.abs(seg) > 1e-4]
        seg *= 10 ** (lvl / 20) / np.sqrt(np.mean(active ** 2))
        i = int((LEAD + k * seg_len) * SR); y[i:i + len(seg)] += seg
        for st, du, ms in phrase:
            s0 = LEAD + k * seg_len + st
            clip.events.append({'start': round(s0, 4), 'end': round(s0 + du, 4), 'midi': ms,
                                'pcs': sorted({m % 12 for m in ms}), 'level_db': lvl})
    return y


def write_wav(path, y):
    pcm = np.clip(y * 32767, -32768, 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def main():
    os.makedirs(OUT, exist_ok=True)
    for clip, opts in build():
        y = render_levels(clip) if opts.get('levels') else clip.render(**opts)
        if opts.get('noise') is not None and opts.get('snr_db') is None:
            y *= 10 ** (-30 / 20) / np.sqrt(np.mean(y[int(LEAD * SR):-int(LEAD * SR)] ** 2))   # noise_only: -30 dBFS rms
        write_wav(os.path.join(OUT, clip.name + '.wav'), y)
        meta = {'name': clip.name, 'description': clip.desc, 'sample_rate': SR, 'lead': LEAD,
                'duration': round(len(y) / SR, 4), 'events': clip.events}
        if clip.name == 'noise_only':   # first half pink noise, second half hum: scored separately
            mid = round(len(y) / SR / 2, 4)
            meta['segments'] = [{'name': 'noise', 'start': LEAD, 'end': mid}, {'name': 'hum', 'start': mid, 'end': round(len(y) / SR - LEAD, 4)}]
        with open(os.path.join(OUT, clip.name + '.json'), 'w') as f:
            json.dump(meta, f, indent=1)
        print(f'{clip.name:16s} {len(y) / SR:5.1f} s  {len(clip.events):3d} events  {clip.desc}')


if __name__ == '__main__':
    main()
