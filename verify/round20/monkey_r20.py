#!/usr/bin/env python3
"""monkey_r20.py -- round 20 (27 Nov 2026): the monkey on DataLoad beta 1i with an M1 that ALWAYS has blank cells.

monkey_v1b.py gives M1 a blank in only one run of seven, and one blank in one cell, so the new question ("Column 2 has a
blank inside": pairs, separate groups, or Cancel) is seldom put.  This runs monkey_v1b's own runs (the same random keys,
taps, drags, menu picks, typed values, lists in D1 and D2, the same verdicts) with M1 drawn here instead, from its own
stream: paired columns with blanks in the middle (2 to 9 columns, 3 to 60 rows), the same with 12 columns (the 10th to
12th are not loaded), every row with a blank (no complete row), blanks only at the foot (no question), one column with a
blank inside (no question), and a 1 x n row.  A run REACHED the question when the program put it; the tally counts them.

    python3 verify/round20/monkey_r20.py K0 K1 OUT.jsonl        (seed = 20 x 1000003 + k; resumes a stopped OUT)
"""
import collections
import json
import os
import random
import sys
import warnings
warnings.filterwarnings('ignore')
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import monkey_v1b as M  # noqa: E402

PROG = os.path.join(ROOT, 'programs', 'DataLoad_beta1i.txt')
INF = float('inf')


def holes_matrix(seed):
    mr = random.Random(seed * 11 + 5)
    kind = mr.choice(['pairs', 'pairs', 'pairs', 'wide', 'nofull', 'foot', 'onecol', 'row'])
    if kind == 'row':
        rows = [[float(mr.randrange(0, 100)) for _ in range(mr.randrange(2, 6))]]
        if mr.random() < 0.5:
            rows[0][mr.randrange(len(rows[0]))] = INF
        return M.R.interp.Matrix(rows), kind
    r = mr.randrange(3, 61)
    c = {'pairs': mr.randrange(2, 10), 'wide': 12, 'nofull': mr.randrange(2, 5), 'foot': mr.randrange(2, 6),
         'onecol': 1}[kind]
    rows = [[float(round(mr.uniform(0, 100), mr.choice([0, 1, 2]))) for _ in range(c)] for _ in range(r)]
    if kind in ('pairs', 'wide', 'onecol'):
        for _ in range(mr.randrange(1, 5)):                         # blanks in the middle (a value below each)
            rows[mr.randrange(0, r - 1)][mr.randrange(c)] = INF
    if kind == 'nofull':
        for i in range(r):
            rows[i][mr.randrange(c)] = INF
    if kind == 'foot':
        for j in range(c):
            for i in range(r - mr.randrange(0, r), r):
                rows[i][j] = INF
    return M.R.interp.Matrix(rows), kind


M.random_matrix = holes_matrix
M.WRITES.update({'D', 'C'})
CUR = [None]
_init, _choose = M.Monkey.__init__, M.Monkey._choose


def init(self, *a, **k):
    _init(self, *a, **k)
    self.r20 = 0
    CUR[0] = self


def choose(self, nodes, frame):
    r = _choose(self, nodes, frame)
    t = self.trace[-1][1] if self.trace else ''
    if t.endswith('blank inside') or t.endswith('blanks inside'):
        self.r20 += 1
    return r


M.Monkey.__init__, M.Monkey._choose = init, choose
k0, k1, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
done = set()
if os.path.exists(out):
    done = set(json.loads(x)['k'] for x in open(out) if x.strip())
tally, reached = collections.Counter(), 0
with open(out, 'a') as f:
    for k in range(k0, k1):
        if k in done:
            continue
        seed = 20 * 1000003 + k
        r = M.one_run(PROG, 'DATALOAD()', seed, 150, 30, True)
        rec = {'k': k, 'seed': seed, 'verdict': r['verdict'], 'detail': r['detail'], 'lists': r['lists'],
               'secs': r['secs'], 'reached': CUR[0].r20 if CUR[0] is not None else 0}
        f.write(json.dumps(rec) + '\n')
        f.flush()
        if r['verdict'] != 'OK':
            print('k %d seed %d %s %s' % (k, seed, r['verdict'], r['detail'][:160]))
for x in open(out):
    rec = json.loads(x)
    tally[rec['verdict']] += 1
    reached += rec['reached'] > 0
print('monkey_r20: %d runs %s; the question was put in %d of them' % (sum(tally.values()), dict(tally), reached))
