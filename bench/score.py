"""Scoring for the Keytones detection bench (used by run.py; can also re-score
saved logs:  python3 bench/score.py bench/results/<run>/ ).

Alignment: the fake mic starts playing a little after the page asks for it,
so each log is aligned to its clip by matching the logged input level (rms of
the frame the detector saw) against the clip's own level envelope. align_err_db
is the mean level mismatch after alignment: a few dB is fine, a large value
means the run didn't hear the clip properly.

All metrics are on pitch classes (C..B), since that's what the app shows.
  f1 / precision / recall   every frame inside the clip
  f1_settled                only frames >= SETTLE s away from any note start/end,
                            i.e. accuracy without the latency at note changes
  onset_*                   time from a note's start until the app shows it
  hit_pct                   share of (note, pitch class) the app showed at all
  release_*                 time from a note's end until the app drops it
  ghost_pct                 frames showing a note while nothing is playing
                            (ignoring RELEASE_GRACE s after a note ends; in practice
                            only the noise_only clip has such frames)
"""
import json
import math
import os
import sys
import wave

import numpy as np

SETTLE = 0.25
RELEASE_GRACE = 0.3
TD_WINDOW = 2048           # samples the detectors look at (index.html TD_WINDOW)
CTX_RATE = 44100           # the fake mic / AudioContext rate in headless Chromium
NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
_env_cache = {}


def fmt_ms(v):
    return '  -  ' if v is None else f'{v:4.0f}ms'


def _clip_level(truth):
    """windowed rms of the clip at any time, via cumulative sums"""
    key = truth['name']
    if key not in _env_cache:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', truth['name'] + '.wav')
        with wave.open(path) as w:
            sr = w.getframerate()
            x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float64) / 32768
        _env_cache[key] = (sr, np.concatenate([[0], np.cumsum(x * x)]))
    sr, cs = _env_cache[key]
    win = int(round(TD_WINDOW / CTX_RATE * sr))

    def level(times):
        end = np.clip(np.round(np.asarray(times) * sr).astype(int), 0, len(cs) - 1)
        start = np.clip(end - win, 0, len(cs) - 1)
        return np.sqrt(np.maximum(cs[end] - cs[start], 0) / win)
    return level


def align(log, truth, gain_db=0.0):
    """offset (s) so that clip time = log time - offset"""
    t = np.array([r[0] for r in log]) / 1000
    lv = np.array([r[1] for r in log])
    level = _clip_level(truth)
    db = lambda v: 20 * np.log10(np.maximum(v, 1e-4))
    target = db(lv)
    g = 10 ** (gain_db / 20)

    def cost(off):
        return float(np.mean(np.abs(db(g * level(t - off)) - target)))
    coarse = np.arange(t[0] - 1.0, t[0] + 4.0, 0.005)
    best = min(coarse, key=cost)
    fine = np.arange(best - 0.006, best + 0.006, 0.0005)
    best = min(fine, key=cost)
    return float(best), cost(best)


def truth_at(events, tau):
    s = set()
    for e in events:
        if e['start'] <= tau < e['end']:
            s.update(e['pcs'])
    return s


def pct(a, q):
    return float(np.percentile(a, q)) if len(a) else None


def score(log, truth, gain_db=0.0):
    out = {'frames': len(log)}
    if len(log) < 5 or not any(r[1] > 0 for r in log):
        out.update(f1=0, f1_settled=None, precision=0, recall=0, onset_median_ms=None, ghost_pct=0,
                   align_err_db=99, note='no audio reached the detector')
        return out
    off, err = align(log, truth, gain_db)
    ev = truth['events']
    dur = truth['duration']
    bounds = sorted({e['start'] for e in ev} | {e['end'] for e in ev})
    rows = [((r[0] / 1000) - off, set(r[2]), set(r[3]), r[4]) for r in log]
    rows = [r for r in rows if 0 <= r[0] <= dur]

    tp = fp = fn = 0
    stp = sfp = sfn = 0
    ghost_n = ghost_on = 0
    fp_int = [0] * 12
    raw_tp = raw_fp = raw_fn = 0
    for tau, raw, fin, _ in rows:
        tr = truth_at(ev, tau)
        a, b, c = len(fin & tr), len(fin - tr), len(tr - fin)
        tp, fp, fn = tp + a, fp + b, fn + c
        raw_tp, raw_fp, raw_fn = raw_tp + len(raw & tr), raw_fp + len(raw - tr), raw_fn + len(tr - raw)
        if all(not (bd <= tau < bd + SETTLE) for bd in bounds):
            stp, sfp, sfn = stp + a, sfp + b, sfn + c
        if tr:
            for p in fin - tr:
                fp_int[min((p - q) % 12 for q in tr)] += 1
        elif not any(e['end'] <= tau < e['end'] + RELEASE_GRACE for e in ev):
            ghost_n += 1
            ghost_on += bool(fin)

    def prf(tp_, fp_, fn_):
        p = tp_ / (tp_ + fp_) if tp_ + fp_ else (1.0 if not fn_ else 0.0)
        r = tp_ / (tp_ + fn_) if tp_ + fn_ else 1.0
        f = 2 * p * r / (p + r) if p + r else 0.0
        return p, r, f

    p, r, f = prf(tp, fp, fn)
    _, _, sf = prf(stp, sfp, sfn)
    _, _, rf = prf(raw_tp, raw_fp, raw_fn)

    onsets, releases, hits, total = [], [], 0, 0
    for i, e in enumerate(ev):
        nxt = truth_at(ev, e['end'] + 0.01)
        for pc_ in e['pcs']:
            total += 1
            hit = next((tau for tau, _, fin, _ in rows if e['start'] <= tau < e['end'] + SETTLE and pc_ in fin), None)
            if hit is not None:
                hits += 1
                onsets.append((hit - e['start']) * 1000)
            if pc_ not in nxt and hit is not None:
                gone = next((tau for tau, _, fin, _ in rows if tau >= e['end'] and pc_ not in fin), None)
                if gone is not None:
                    releases.append(min(1000.0, (gone - e['end']) * 1000))

    # per input level (the 'levels' clip): F1 over each level's own stretch of the clip
    # (mono algorithms are scored on the phrase's single notes only: they can't show chords)
    by_level, by_level_single = {}, {}
    for lvl in sorted({e['level_db'] for e in ev if 'level_db' in e}):
        evs = [e for e in ev if e.get('level_db') == lvl]
        for target, sel in ((by_level, evs), (by_level_single, [e for e in evs if len(e['pcs']) == 1])):
            c = [0, 0, 0]
            for tau, _, fin, _ in rows:
                if any(e['start'] <= tau < e['end'] + RELEASE_GRACE for e in sel):
                    tr = truth_at(sel, tau)
                    c[0] += len(fin & tr); c[1] += len(fin - tr); c[2] += len(tr - fin)
            target[str(lvl)] = round(prf(*c)[2], 3)

    ghost_seg = {}
    for sg in truth.get('segments', []):
        fr = [fin for tau, _, fin, _ in rows if sg['start'] + 0.1 <= tau < sg['end'] - 0.1]
        ghost_seg[sg['name']] = round(100 * sum(bool(f) for f in fr) / len(fr), 1) if fr else None

    ticks = np.diff([r[0] for r in log])
    cost_ms = [r[4] for r in log if r[1] > 0]
    out.update(
        offset_s=round(off, 4), align_err_db=round(err, 2),
        precision=round(p, 4), recall=round(r, 4), f1=round(f, 4),
        f1_settled=round(sf, 4) if stp + sfp + sfn else None,
        f1_raw=round(rf, 4),
        hit_pct=round(100 * hits / total, 1) if total else None,
        onset_median_ms=pct(onsets, 50), onset_p90_ms=pct(onsets, 90),
        release_median_ms=pct(releases, 50),
        ghost_pct=round(100 * ghost_on / ghost_n, 1) if ghost_n else 0.0,
        fp_interval_hist=fp_int,
        tick_ms=float(np.median(ticks)) if len(ticks) else None,
        detect_ms_mean=float(np.mean(cost_ms)) if cost_ms else None,
        detect_ms_p95=pct(cost_ms, 95),
        f1_by_level=by_level, f1_by_level_single=by_level_single, ghost_segments=ghost_seg,
        onsets_ms=[round(x, 1) for x in onsets], releases_ms=[round(x, 1) for x in releases],
    )
    return out


# ── report ────────────────────────────────────────────────────────────────
ALGO_LABEL = {'fft': 'M1 FFT', 'acf': 'M2 ACF', 'amdf': 'M3 AMDF', 'yin': 'M4 YIN', 'mpm': 'M5 MPM',
              'hpcp': 'P1 HPCP', 'nnls': 'P2 NNLS', 'cqtnmf': 'P3 CQT+NMF', 'multif0': 'P4 Multi-F0',
              'ensemble': 'P5 Ensemble'}
MONO_CLIPS = ['mono_sine', 'mono_harmonic', 'mono_piano', 'mono_fast', 'piano_in_noise']
CHORD_CLIPS = ['dyads', 'triads', 'sevenths']
BAND_CLIPS = ['band_power', 'band_open', 'band_palm']
POLY = {'hpcp', 'nnls', 'cqtnmf', 'multif0', 'ensemble'}
INTERVAL = ['unison', 'm2', 'M2', 'm3', 'M3', 'P4', 'tritone', 'P5', 'm6', 'M6', 'm7', 'M7']


def _f(v, d=2):
    return '  -  ' if v is None else f'{v:.{d}f}'


def report(meta, results):
    by = {(r['algo'], r['clip']): r for r in results}
    algos = [a for a in meta['algos']]
    clips = [c for c in meta['clips'] if c not in ('noise_only', 'levels')]
    s = meta['settings']
    L = [f"# Keytones detection bench — {meta['version']}", '',
         f"Settings: speed {s['speed']}, gate {s['gateDb']} dB, confidence {s['confidence']}, "
         f"stability {s['stability']}, mic gain {meta['gain_db']} dB. Run {meta['started']}, {meta['wall_s']} s.", '',
         '## Accuracy (F1 on pitch classes, settled = ≥250 ms away from note changes)', '',
         '| algorithm | ' + ' | '.join(clips) + ' | mono avg | chord avg | band avg |',
         '|---|' + '---:|' * (len(clips) + 3)]
    for a in algos:
        cells, mono, chord, bnd = [], [], [], []
        for c in clips:
            r = by.get((a, c))
            settled = r is not None and r.get('f1_settled') is not None
            v = None if r is None else (r['f1_settled'] if settled else r['f1'])
            cells.append(_f(v) + ('' if settled or r is None else '*'))
            if v is not None:
                (mono if c in MONO_CLIPS else bnd if c in BAND_CLIPS else chord).append(v)
        L.append(f'| {ALGO_LABEL.get(a, a)} | ' + ' | '.join(cells) +
                 f' | **{_f(np.mean(mono) if mono else None)}** | **{_f(np.mean(chord) if chord else None)}** | **{_f(np.mean(bnd) if bnd else None)}** |')

    L += ['', '\\* no frames are 250 ms away from a note change (fast notes), so this is the overall F1.']
    L += ['', '## Overall F1 (every frame, including note changes) and before/after Stability', '',
          '| algorithm | ' + ' | '.join(clips) + ' | avg | avg raw (no Stability) |',
          '|---|' + '---:|' * (len(clips) + 2)]
    for a in algos:
        rs = [by.get((a, c)) for c in clips]
        L.append(f'| {ALGO_LABEL.get(a, a)} | ' + ' | '.join(_f(r['f1']) if r else '  -  ' for r in rs) +
                 f" | {_f(np.mean([r['f1'] for r in rs if r]))} | {_f(np.mean([r.get('f1_raw', 0) for r in rs if r]))} |")

    L += ['', '## Timing, false notes, cost', '',
          '| algorithm | notes shown | onset median | onset p90 | release median | ghost: pink noise | ghost: hum | wrong-note share | top wrong interval | detect ms (p95) |',
          '|---|---:|---:|---:|---:|---:|---:|---:|---|---:|']
    for a in algos:
        rs = [by[(a, c)] for c in clips if (a, c) in by]
        on = sum((r.get('onsets_ms', []) for r in rs), [])
        rel = sum((r.get('releases_ms', []) for r in rs), [])
        hits = [r['hit_pct'] for r in rs if r.get('hit_pct') is not None]
        nz = by.get((a, 'noise_only'))
        hist = np.sum([r.get('fp_interval_hist', [0] * 12) for r in rs], axis=0) if rs else np.zeros(12)
        tp_fp = [(r['precision']) for r in rs]
        wrong = 1 - np.mean(tp_fp) if tp_fp else None
        top = INTERVAL[int(np.argmax(hist))] + f' ({100 * hist.max() / hist.sum():.0f}%)' if hist.sum() else '-'
        cost = [r['detect_ms_p95'] for r in rs if r.get('detect_ms_p95') is not None]
        L.append(f'| {ALGO_LABEL.get(a, a)} | {_f(np.mean(hits), 0)}% | {fmt_ms(pct(on, 50))} | {fmt_ms(pct(on, 90))} | '
                 f'{fmt_ms(pct(rel, 50))} | {_f(nz["ghost_segments"].get("noise") if nz else None, 0)}% | {_f(nz["ghost_segments"].get("hum") if nz else None, 0)}% | '
                 f'{_f(100 * wrong if wrong is not None else None, 0)}% | {top} | {_f(max(cost) if cost else None, 1)} |')

    lv = [(a, by[(a, 'levels')]['f1_by_level' if a in POLY else 'f1_by_level_single']) for a in algos if (a, 'levels') in by]
    if lv:
        cols = list(lv[0][1].keys())
        gain = meta['gain_db']
        L += ['', f'## Input level (the same phrase at rising loudness; level after the {gain:+g} dB mic gain)', '',
              '| algorithm | ' + ' | '.join(f'{float(c) + gain:+.0f} dBFS' for c in cols) + ' | works from |',
              '|---|' + '---:|' * (len(cols) + 1)]
        for a, d in lv:
            ok = next((f'{float(c) + gain:+.0f} dBFS' for c in cols if d[c] >= 0.7), 'never')
            L.append(f'| {ALGO_LABEL.get(a, a)} | ' + ' | '.join(_f(d[c]) for c in cols) + f' | {ok} |')
        L += ['', 'The app\'s auto-gain keeps the average input between roughly −28 and −13 dBFS rms. '
              '"works from" = the quietest level with F1 ≥ 0.70. Mono algorithms (M1–M5) are scored on the phrase\'s single notes only.']

    bad = [r for r in results if r.get('align_err_db', 0) > 6 or r.get('errors')]
    L += ['', 'Notes: mono algorithms (M1–M5) can only ever show one note, so their chord recall is capped. '
          '"wrong-note share" = shown notes that were not playing (1 − precision) on the note clips; '
          '"top wrong interval" = how far those wrong notes were from the real ones (P5/P4 = harmonics).']
    if bad:
        L += ['', '**Check these runs:** ' + ', '.join(f"{r['clip']}/{r['algo']} (align {r.get('align_err_db')} dB"
                                                          f"{', errors' if r.get('errors') else ''})" for r in bad)]
    return '\n'.join(L) + '\n'


def load_run(d):
    """re-score a saved run from its logs (so old runs use the current scorer)"""
    data = json.load(open(os.path.join(d, 'results.json')))
    fix = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    res = []
    for r in data['results']:
        lg = json.load(open(os.path.join(d, 'logs', f"{r['clip']}__{r['algo']}.json")))
        m = score(lg['log'], json.load(open(os.path.join(fix, r['clip'] + '.json'))), data['meta'].get('gain_db', 0))
        m.update(clip=r['clip'], algo=r['algo'], errors=lg['errors'])
        res.append(m)
    return data['meta'], res


def merge(dirs):
    """several runs as one report: later runs replace earlier (clip, algo) results"""
    meta, by = None, {}
    for d in dirs:
        m, res = load_run(d)
        if meta is None:
            meta = dict(m)
        else:
            meta['algos'] = list(dict.fromkeys(meta['algos'] + m['algos']))
            meta['clips'] = list(dict.fromkeys(meta['clips'] + m['clips']))
            meta['started'] += ' + ' + m['started']; meta['wall_s'] += m['wall_s']
        meta['version'] = m['version']
        for r in res:
            by[(r['clip'], r['algo'])] = r
    order = {a: i for i, a in enumerate(ALGO_LABEL)}
    meta['algos'] = sorted(meta['algos'], key=lambda a: order.get(a, 99))
    return meta, list(by.values())


if __name__ == '__main__':
    # python3 bench/score.py RUN_DIR [MORE_RUN_DIRS...]  — later runs replace earlier (clip, algo) pairs
    print(report(*merge(sys.argv[1:])))
