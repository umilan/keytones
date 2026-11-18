#!/usr/bin/env python3
"""Ensemble bench, part 2: fuse + score. Reads a run of bench/ensemble_run.js
(every chord algorithm on the same frames) and scores fusion rules against the
single algorithms, with bench/score.py's metrics.

Every rule, single algorithms included, goes through the same offline copy of
the app's Stability step (a new note needs `stability` frames in a row; a shown
note stays while heard), so the comparison is like for like. The single-
algorithm rows should land close to the committed baseline (sanity check).

    python3 bench/ensemble.py bench/results/ensemble-<stamp>/
"""
import json
import os
import sys

import score

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
ALGOS = ['hpcp', 'nnls', 'cqtnmf', 'multif0']
SHORT = {'hpcp': 'P1', 'nnls': 'P2', 'cqtnmf': 'P3', 'multif0': 'P4'}


def per_algo(frame_out):
    """{algo: {pc: conf}} — strongest octave per note name"""
    d = {}
    for a, notes in frame_out.items():
        m = {}
        for pc, conf, _oct in notes:
            m[pc] = max(m.get(pc, 0), conf)
        d[a] = m
    return d


def vote(k, algos=ALGOS):
    def f(d):
        cnt = {}
        for a in algos:
            for pc in d.get(a, {}):
                cnt[pc] = cnt.get(pc, 0) + 1
        return {pc for pc, c in cnt.items() if c >= k}
    return f, algos


def conf_sum(th, algos=ALGOS):
    def f(d):
        s = {}
        for a in algos:
            for pc, c in d.get(a, {}).items():
                s[pc] = s.get(pc, 0) + c
        return {pc for pc, v in s.items() if v >= th}
    return f, algos


def single(a):
    return (lambda d: set(d.get(a, {}))), [a]


def anchor_confirm(anchor, others):
    """the anchor's notes, kept only when at least one other algorithm also has them"""
    def f(d):
        return {pc for pc in d.get(anchor, {}) if any(pc in d.get(o, {}) for o in others)}
    return f, [anchor] + others


RULES = {
    'P1 HPCP': single('hpcp'),
    'P2 NNLS': single('nnls'),
    'P3 CQT+NMF': single('cqtnmf'),
    'P4 Multi-F0': single('multif0'),
    'vote 2 of 4': vote(2),
    'vote 3 of 4': vote(3),
    'conf sum ≥ 1.5': conf_sum(1.5),
    'conf sum ≥ 2.0': conf_sum(2.0),
    'conf sum ≥ 2.5': conf_sum(2.5),
    'P4 + 1 other agrees': anchor_confirm('multif0', ['hpcp', 'nnls', 'cqtnmf']),
    'P4 + P1/P2 agrees (no P3)': anchor_confirm('multif0', ['hpcp', 'nnls']),
    'vote 2 of 3 (P1 P2 P4)': vote(2, ['hpcp', 'nnls', 'multif0']),
}


def stabilise(raw_frames, stability):
    shown, streak, out = set(), [0] * 12, []
    for heard in raw_frames:
        for i in range(12):
            streak[i] = streak[i] + 1 if i in heard else 0
        shown = {pc for pc in heard if pc in shown or streak[pc] >= stability}
        out.append(shown)
    return out


def main(run_dir):
    clips = sorted(f[:-5] for f in os.listdir(run_dir) if f.endswith('.json') and not f.startswith('ensemble'))
    res = {}  # rule -> clip -> metrics
    for clip in clips:
        rec = json.load(open(os.path.join(run_dir, clip + '.json')))
        truth = json.load(open(os.path.join(FIX, clip + '.json')))
        frames = rec['frames']
        stab = rec['settings']['stability']
        for name, (fn, used) in RULES.items():
            raws = [fn(per_algo(f[2])) if f[2] else set() for f in frames]
            fins = stabilise(raws, stab)
            log = [[f[0], f[1], sorted(r), sorted(s), round(sum(f[3].get(a, 0) for a in used), 2)]
                   for f, r, s in zip(frames, raws, fins)]
            res.setdefault(name, {})[clip] = score.score(log, truth, rec['gainDb'])

    def avg(rule, clips_, key='f1_settled'):
        v = [res[rule][c][key] if res[rule][c].get(key) is not None else res[rule][c]['f1']
             for c in clips_ if c in res[rule]]
        return sum(v) / len(v) if v else None

    def wrong(rule):
        tp = fp = 0
        for c in score.MONO_CLIPS + score.CHORD_CLIPS + score.BAND_CLIPS:
            m = res[rule].get(c)
            if m and m.get('precision') is not None:
                # precision is per clip; weight equally
                tp += m['precision']; fp += 1
        return 100 * (1 - tp / fp) if fp else None

    def cost(rule):
        v = [res[rule][c]['detect_ms_p95'] for c in res[rule] if res[rule][c].get('detect_ms_p95') is not None]
        return max(v) if v else None

    lines = ['| rule | chord F1 | band F1 | mono F1 | all notes F1 | wrong notes % | ghost noise % | ghost hum % | onset ms | ms/frame p95 |',
             '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for rule in RULES:
        ng = res[rule].get('noise_only', {}).get('ghost_segments', {})
        on = [res[rule][c]['onset_median_ms'] for c in score.CHORD_CLIPS + score.BAND_CLIPS
              if c in res[rule] and res[rule][c].get('onset_median_ms') is not None]
        lines.append('| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |'.format(
            rule, score._f(avg(rule, score.CHORD_CLIPS)), score._f(avg(rule, score.BAND_CLIPS)),
            score._f(avg(rule, score.MONO_CLIPS)),
            score._f(avg(rule, score.MONO_CLIPS + score.CHORD_CLIPS + score.BAND_CLIPS)),
            score._f(wrong(rule), 0), score._f(ng.get('noise'), 0), score._f(ng.get('hum'), 0),
            score._f(sorted(on)[len(on) // 2] if on else None, 0), score._f(cost(rule), 1)))
    lines += ['', '| rule | ' + ' | '.join(clips) + ' |', '|---|' + '---:|' * len(clips)]
    for rule in RULES:
        lines.append(f'| {rule} | ' + ' | '.join(score._f(res[rule][c].get('f1_settled') if res[rule][c].get('f1_settled') is not None else res[rule][c]['f1']) for c in clips) + ' |')
    report = '\n'.join(lines)
    with open(os.path.join(run_dir, 'ensemble.md'), 'w') as f:
        f.write(report + '\n')
    with open(os.path.join(run_dir, 'ensemble.json'), 'w') as f:
        json.dump(res, f)
    print(report)


if __name__ == '__main__':
    main(sys.argv[1])
