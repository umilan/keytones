#!/usr/bin/env python3
"""Window / stability bench: fuse P5's algorithms (P4 Multi-F0, P1 HPCP, P2 NNLS) across
analysis windows and with adaptive stability. Reads a run of

    node bench/ensemble_run.js --algos hpcp,nnls,multif0 --windows 2048,8192

(the app's own window, 4096 at Speed 3, plus 2048 and 8192 on the same frames) and scores
each rule with bench/score.py, as bench/ensemble.py does.

    python3 bench/windows.py bench/results/ensemble-<stamp>/
"""
import json
import os
import sys

import score
from ensemble import per_algo

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
MAIN = '4096'
SRC_ALGOS = ['multif0', 'hpcp', 'nnls']


def sources(frame):
    """{window: {algo: {pc: (conf, oct)}}} for every window of a frame"""
    out = {}
    wins = {MAIN: (frame[2], frame[3])}
    for w, (o, m) in (frame[4] if len(frame) > 4 else {}).items():
        wins[w] = (o, m)
    for w, (o, _m) in wins.items():
        d = {}
        for a, notes in o.items():
            mm = {}
            for pc, conf, octv in notes:
                if pc not in mm or conf > mm[pc][0]:
                    mm[pc] = (conf, octv)
            d[a] = mm
        out[w] = d
    return out


def cost(frame, wins):
    c = sum(frame[3].values()) if MAIN in wins else 0
    for w, (_o, m) in (frame[4] if len(frame) > 4 else {}).items():
        if w in wins:
            c += sum(m.values())
    return c


def p5(src, w):
    """P5 Ensemble on window w: P4's notes that P1 or P2 also hear → {pc: oct}"""
    s = src.get(w, {})
    m, h, n = s.get('multif0', {}), s.get('hpcp', {}), s.get('nnls', {})
    return {pc: v[1] for pc, v in m.items() if pc in h or pc in n}


def votes(src, wins):
    v = {}
    for w in wins:
        for a in SRC_ALGOS:
            for pc in src.get(w, {}).get(a, {}):
                v[pc] = v.get(pc, 0) + 1
    return v


# a rule: frame sources -> (heard set, fast set); fast notes may show on their first frame
def r_p5(w):
    return lambda s: (set(p5(s, w)), set()), [w]


def r_p5_stab1(w):
    return lambda s: (set(p5(s, w)), set(p5(s, w))), [w]


def r_winvote(k):
    def f(s):
        cnt = {}
        for w in ('2048', MAIN, '8192'):
            for pc in p5(s, w):
                cnt[pc] = cnt.get(pc, 0) + 1
        return {pc for pc, c in cnt.items() if c >= k}, set()
    return f, ['2048', MAIN, '8192']


def r_union(ws):
    def f(s):
        u = set()
        for w in ws:
            u |= set(p5(s, w))
        return u, set()
    return f, ws


def r_register(low_w, high_w, split_oct=3):
    """notes at or below octave split_oct from low_w, higher ones from high_w"""
    def f(s):
        lo = {pc for pc, o in p5(s, low_w).items() if o <= split_oct}
        hi = {pc for pc, o in p5(s, high_w).items() if o > split_oct}
        return lo | hi, set()
    return f, [low_w, high_w]


def r_adaptive(k_min, k_fast, wins=('2048', MAIN, '8192'), base_p5=False):
    """heard = at least k_min sources (algorithm × window) agree, or P5 on the main window when
    base_p5; a note shows at once when at least k_fast sources agree, else after Stability frames"""
    def f(s):
        v = votes(s, wins)
        heard = {pc for pc, c in v.items() if c >= k_min}
        if base_p5:
            heard |= set(p5(s, MAIN))
        return heard, {pc for pc in heard if v.get(pc, 0) >= k_fast}
    return f, list(wins)


RULES = {
    'P5 @4096 (today)': r_p5(MAIN),
    'P5 @2048 (short)': r_p5('2048'),
    'P5 @8192 (long)': r_p5('8192'),
    'P5 @4096, Stability 1': r_p5_stab1(MAIN),
    'P5 in 2 of 3 windows': r_winvote(2),
    'P5 @2048 ∪ @4096': r_union(['2048', MAIN]),
    'low ≤ oct 3 @8192, rest @4096': r_register('8192', MAIN),
    'low ≤ oct 3 @8192, rest @2048': r_register('8192', '2048'),
    'adaptive: P5 @4096, instant if 3/3 algos (no extra window)': r_adaptive(9, 3, wins=(MAIN,), base_p5=True),
    'adaptive: P5 @4096, instant if ≥6/9': r_adaptive(9, 6, base_p5=True),
    'adaptive: P5 @4096, instant if ≥5/9': r_adaptive(9, 5, base_p5=True),
    'adaptive: ≥4/9 heard, instant ≥6/9': r_adaptive(4, 6),
    'adaptive: ≥3/9 heard, instant ≥6/9': r_adaptive(3, 6),
}


def stabilise(frames, stability):
    shown, streak, out = set(), [0] * 12, []
    for heard, fast in frames:
        for i in range(12):
            streak[i] = streak[i] + 1 if i in heard else 0
        shown = {pc for pc in heard if pc in shown or pc in fast or streak[pc] >= stability}
        out.append((heard, shown))
    return out


def main(run_dir):
    clips = sorted(f[:-5] for f in os.listdir(run_dir) if f.endswith('.json') and not f.startswith(('ensemble', 'windows')))
    res = {}
    for clip in clips:
        rec = json.load(open(os.path.join(run_dir, clip + '.json')))
        truth = json.load(open(os.path.join(FIX, clip + '.json')))
        frames, stab = rec['frames'], rec['settings']['stability']
        srcs = [sources(f) if f[2] else None for f in frames]
        for name, (fn, wins) in RULES.items():
            hf = [fn(s) if s else (set(), set()) for s in srcs]
            st = stabilise(hf, stab)
            log = [[f[0], f[1], sorted(h), sorted(sh), round(cost(f, wins), 2) if f[2] else 0]
                   for f, (h, sh) in zip(frames, st)]
            res.setdefault(name, {})[clip] = score.score(log, truth, rec['gainDb'])

    def avg(rule, cl, key='f1_settled'):
        v = [res[rule][c][key] if res[rule][c].get(key) is not None else res[rule][c]['f1'] for c in cl if c in res[rule]]
        return sum(v) / len(v) if v else None

    def wrong(rule):
        v = [1 - res[rule][c]['precision'] for c in score.MONO_CLIPS + score.CHORD_CLIPS + score.BAND_CLIPS if c in res[rule]]
        return 100 * sum(v) / len(v) if v else None

    def med_onset(rule):
        on = [x for c in score.MONO_CLIPS + score.CHORD_CLIPS + score.BAND_CLIPS if c in res[rule] for x in res[rule][c].get('onsets_ms', [])]
        on.sort()
        return on[len(on) // 2] if on else None

    lines = ['| rule | mono_fast F1 | chord F1 | band F1 | mono F1 | all F1 (every frame) | wrong notes % | ghost noise / hum % | onset median ms | ms/frame p95 |',
             '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    allc = score.MONO_CLIPS + score.CHORD_CLIPS + score.BAND_CLIPS
    for rule in RULES:
        ng = res[rule].get('noise_only', {}).get('ghost_segments', {})
        cst = max((res[rule][c].get('detect_ms_p95') or 0) for c in res[rule])
        lines.append('| {} | {} | {} | {} | {} | {} | {} | {} / {} | {} | {} |'.format(
            rule, score._f(res[rule].get('mono_fast', {}).get('f1')), score._f(avg(rule, score.CHORD_CLIPS)),
            score._f(avg(rule, score.BAND_CLIPS)), score._f(avg(rule, score.MONO_CLIPS)),
            score._f(avg(rule, allc, 'f1')), score._f(wrong(rule), 0),
            score._f(ng.get('noise'), 0), score._f(ng.get('hum'), 0), score._f(med_onset(rule), 0), score._f(cst, 1)))
    lines += ['', '| rule | ' + ' | '.join(clips) + ' |', '|---|' + '---:|' * len(clips)]
    for rule in RULES:
        lines.append(f'| {rule} | ' + ' | '.join(score._f(res[rule][c]['f1_settled'] if res[rule][c].get('f1_settled') is not None else res[rule][c]['f1']) for c in clips) + ' |')
    rep = '\n'.join(lines)
    open(os.path.join(run_dir, 'windows.md'), 'w').write(rep + '\n')
    print(rep)


if __name__ == '__main__':
    main(sys.argv[1])
