"""Synthetic distorted rock band for the detection bench.

Guitar: every string is an additive plucked tone (pluck-position comb,
higher partials die faster, slight inharmonicity and detune), strummed
with per-string offsets, the whole guitar then goes through a high-pass,
a tanh overdrive (where the intermodulation between strings happens, as
in a real amp) and a cabinet-like low-pass. Bass doubles the chord root an
octave down, drums are a kick / snare / hi-hat groove at 120 bpm.

The truth for each chord is the set of pitch classes the guitar and bass
play; drums and distortion products are not notes.
"""
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
BEAT = 0.5   # 120 bpm

# guitar voicings, standard tuning (E2=40 A2=45 D3=50 G3=55 B3=59 E4=64)
def power(root):              # root on the low E (40..) or A (45..) string: root, fifth, octave
    return [root, root + 7, root + 12]

OPEN = {
    'G': [43, 47, 50, 55, 59, 67], 'D': [50, 57, 62, 66], 'Em': [40, 47, 52, 55, 59, 64],
    'C': [48, 52, 55, 60, 64], 'A': [45, 52, 57, 61, 64], 'E': [40, 47, 52, 56, 59, 64],
    'Am': [45, 52, 57, 60, 64], 'F': [41, 48, 53, 57, 60, 65], 'F#m': [42, 49, 54, 57, 61, 66],
    'Bm': [47, 54, 59, 62, 66], 'B7': [47, 51, 57, 59, 66],
}


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def pluck(m, dur, rng, mute=False, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f0 = hz(m) * 2 ** (rng.normal(0, 4) / 1200)          # a few cents out of tune
    p = rng.uniform(0.12, 0.2)                            # pluck position along the string
    x = np.zeros(n)
    base = 1.2 + 0.03 * max(0, m - 40)
    if mute:
        base *= 9
    for k in range(1, 40):
        fk = f0 * k * np.sqrt(1 + 0.00008 * k * k)
        if fk > 9000:
            break
        amp = abs(np.sin(np.pi * k * p)) / k
        if mute and k > 6:
            amp *= 0.3
        x += amp * np.sin(2 * np.pi * fk * t + rng.uniform(0, 6.3)) * np.exp(-t * base * (1 + 0.15 * k))
    a = int(0.002 * SR); x[:a] *= np.linspace(0, 1, a)
    r = min(int(0.01 * SR), n); x[-r:] *= np.linspace(1, 0, r)
    return x * vel


def guitar_track(chords, total, rng, gain, mute=False):
    """chords: list of (start_s, dur_s, notes, strum_times)"""
    g = np.zeros(int(total * SR))
    for start, dur, notes, strums in chords:
        for j, st in enumerate(strums):
            nxt = strums[j + 1] if j + 1 < len(strums) else start + dur
            up = (j % 2 == 1) and not mute
            order = notes[::-1] if up else notes
            vel = (0.75 if up else 1.0) * rng.uniform(0.9, 1.0)
            for s, m in enumerate(order):
                off = st + s * (0.008 if not mute else 0.003)
                ln = nxt - off + 0.01
                if ln <= 0.02:
                    continue
                x = pluck(m, ln, rng, mute=mute, vel=vel)
                i = int(off * SR); g[i:i + len(x)] += x[:len(g) - i]
    g = sosfilt(butter(2, 90, 'hp', fs=SR, output='sos'), g)
    if mute:
        g = sosfilt(butter(2, 1500, 'lp', fs=SR, output='sos'), g)
    g /= np.max(np.abs(g)) + 1e-9
    g = np.tanh(gain * g) / np.tanh(gain)                 # the amp
    g = sosfilt(butter(4, 4800, 'lp', fs=SR, output='sos'), g)   # the cabinet
    g = sosfilt(butter(1, 110, 'hp', fs=SR, output='sos'), g)
    return g


def bass_track(chords, total, rng):
    b = np.zeros(int(total * SR))
    for start, dur, notes, strums in chords:
        root = min(notes) - 12
        for j, st in enumerate(strums[::2]):              # quarter notes
            ln = min(BEAT, start + dur - st) - 0.01
            t = np.arange(int(ln * SR)) / SR
            f = hz(root)
            x = sum(np.sin(2 * np.pi * f * k * t) / k ** 1.5 for k in range(1, 7)) * np.exp(-t * 2.5)
            x = np.tanh(2.5 * x)
            a = int(0.004 * SR); x[:a] *= np.linspace(0, 1, a)
            r = int(0.01 * SR); x[-r:] *= np.linspace(1, 0, r)
            i = int(st * SR); b[i:i + len(x)] += x[:len(b) - i]
    return sosfilt(butter(2, 1200, 'lp', fs=SR, output='sos'), b)


def drum_track(start, end, total, rng):
    d = np.zeros(int(total * SR))

    def put(t0, x):
        i = int(t0 * SR); d[i:i + len(x)] += x[:len(d) - i]
    t = np.arange(int(0.35 * SR)) / SR
    kick = np.sin(2 * np.pi * (45 * t + 60 * (1 - np.exp(-t * 30)) / 30)) * np.exp(-t * 9)
    kick[:60] += rng.uniform(-0.6, 0.6, 60)
    t2 = np.arange(int(0.25 * SR)) / SR
    snare = (sosfilt(butter(2, [1500, 7000], 'bp', fs=SR, output='sos'), rng.standard_normal(len(t2))) * 2.5
             + 0.6 * np.sin(2 * np.pi * 185 * t2)) * np.exp(-t2 * 16)
    t3 = np.arange(int(0.06 * SR)) / SR
    hat = sosfilt(butter(2, 7000, 'hp', fs=SR, output='sos'), rng.standard_normal(len(t3))) * np.exp(-t3 * 60)
    beat = 0
    tt = start
    while tt < end - 0.01:
        if beat % 4 in (0, 2):
            put(tt, kick)
        if beat % 4 in (1, 3):
            put(tt, snare)
        put(tt, hat * 0.5); put(tt + BEAT / 2, hat * 0.35)
        beat += 1; tt += BEAT
    return d


def song(progression, rng, lead, gain, mute=False, beats_per_chord=4, strum_every=0.5):
    """progression: list of (name, notes). Returns (audio, events)."""
    chords, t = [], lead
    for name, notes in progression:
        dur = beats_per_chord * BEAT
        strums = list(np.arange(t, t + dur - 1e-6, BEAT * strum_every))
        chords.append((t, dur, notes, strums))
        t += dur
    end = t
    total = end + lead + 0.5
    gtr = guitar_track(chords, total, rng, gain, mute)
    bas = bass_track(chords, total, rng)
    drm = drum_track(lead, end, total, rng)
    rms = lambda v: np.sqrt(np.mean(v[int(lead * SR):int(end * SR)] ** 2)) + 1e-12
    y = gtr / rms(gtr) * 0.25 + bas / rms(bas) * 0.12 + drm / rms(drm) * 0.10
    y[int((end + 0.15) * SR):] *= 0                       # band stops together
    events = [{'start': round(c[0], 4), 'end': round(c[0] + c[1], 4), 'midi': sorted(set(c[2]) | {min(c[2]) - 12}),
               'pcs': sorted({m % 12 for m in c[2]}), 'chord': n}
              for c, (n, _) in zip(chords, progression)]
    return y, events
