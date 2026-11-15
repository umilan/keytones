#!/usr/bin/env python3
"""Before/after comparison of two bench runs (each may be several run dirs joined with '+'):

    python3 bench/compare.py bench/results/OLD bench/results/NEW
    python3 bench/compare.py OLD_MONO+OLD_POLY NEW
"""
import sys

import numpy as np

import score


def summary(meta, results):
    by = {(r['algo'], r['clip']): r for r in results}
    out = {}
    for a in meta['algos']:
        mono, chord, on, wrong = [], [], [], []
        for c in meta['clips']:
            r = by.get((a, c))
            if not r or c in ('noise_only', 'levels'):
                continue
            v = r['f1_settled'] if r.get('f1_settled') is not None else r['f1']
            (chord if c in score.CHORD_CLIPS else mono).append(v)
            on += r.get('onsets_ms', [])
            wrong.append(1 - r['precision'])
        nz = by.get((a, 'noise_only'), {}).get('ghost_segments', {})
        lv = by.get((a, 'levels'))
        works = None
        if lv:
            d = lv['f1_by_level' if a in score.POLY else 'f1_by_level_single']
            works = next((float(k) + meta['gain_db'] for k in d if d[k] >= 0.7), None)
        out[a] = {'mono F1': np.mean(mono) if mono else None, 'chord F1': np.mean(chord) if chord else None,
                  'onset ms': score.pct(on, 50), 'wrong notes %': 100 * np.mean(wrong) if wrong else None,
                  'ghost noise %': nz.get('noise'), 'ghost hum %': nz.get('hum'), 'works from dBFS': works}
    return out


def fmt(k, v):
    if v is None:
        return '-' if 'works' not in k else 'never'
    return f'{v:.2f}' if 'F1' in k else f'{v:.0f}'


def main():
    old = summary(*score.merge(sys.argv[1].split('+')))
    new = summary(*score.merge(sys.argv[2].split('+')))
    keys = ['mono F1', 'chord F1', 'onset ms', 'wrong notes %', 'ghost noise %', 'ghost hum %', 'works from dBFS']
    print('| algorithm | ' + ' | '.join(keys) + ' |')
    print('|---|' + '---|' * len(keys))
    for a in new:
        o = old.get(a, {})
        cells = []
        for k in keys:
            ov, nv = fmt(k, o.get(k)), fmt(k, new[a][k])
            cells.append(nv if ov == nv else f'{ov} → **{nv}**')
        print(f'| {score.ALGO_LABEL.get(a, a)} | ' + ' | '.join(cells) + ' |')


if __name__ == '__main__':
    main()
