#!/usr/bin/env python3
"""monkey_chunks_v1.py -- the monkey's runs K0 .. K1-1, written as they finish (2 Nov 2026; round 4).

monkey_v1b.py writes its report only at the end, so a job stopped by a time limit leaves nothing (Lessons Learned
v7zi): GaltonBoard's 1,000 runs outlived a two-hour limit for a background task.  This runs the very same runs
(seed = BASE x 1000003 + k, as monkey_v1b's main does, so --replay SEED still repeats any one of them) and appends one
JSON line per run to OUT.jsonl at once, printing each broken run and a tally every 50 runs.  Run again with the same
OUT, it skips the runs already written, so a stopped job resumes; split 1,000 runs into chunks (0 500, then 500 1000)
when one job may outlive its limit.

    python3 tools/monkey_chunks_v1.py PROG CALL BASE K0 K1 OUT.jsonl [--lists] [--writes D,C] [--seconds 30]
                                      [--events 150]
    e.g. python3 tools/monkey_chunks_v1.py programs/GaltonBoard_beta3f.txt "GaltonBoard()" 1 0 500 gb.jsonl \\
             --lists --writes D --seconds 120

The tally of a finished set:  python3 -c "import json,collections; print(collections.Counter(json.loads(l)['verdict']
for l in open('gb.jsonl')))"
"""
import collections
import json
import os
import sys
import warnings

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
a = sys.argv[1:]
sys.argv = ['monkey_v1b.py']
import monkey_v1b as M  # noqa: E402

prog, call, base, k0, k1, out = a[0], a[1], int(a[2]), int(a[3]), int(a[4]), a[5]
lists = '--lists' in a
opt = {'--writes': '', '--seconds': '30', '--events': '150'}
i = 6
while i < len(a):
    if a[i] == '--lists':
        i += 1
        continue
    opt[a[i]] = a[i + 1]
    i += 2
M.WRITES.update(w.strip() for w in opt['--writes'].split(',') if w.strip())
done = set()
if os.path.exists(out):
    for ln in open(out):
        try:
            done.add(json.loads(ln)['k'])
        except Exception:
            pass
tally = collections.Counter()
with open(out, 'a') as fh:
    for k in range(k0, k1):
        if k in done:
            continue
        seed = base * 1000003 + k
        r = M.one_run(prog, call, seed, int(opt['--events']), int(opt['--seconds']), lists)
        r = {'k': k, 'seed': seed, 'verdict': r['verdict'], 'detail': r['detail'], 'secs': r['secs']}
        fh.write(json.dumps(r) + '\n')
        fh.flush()
        tally[r['verdict']] += 1
        if r['verdict'] != 'OK':
            print('k %d seed %d %s %s (%.1f s)' % (k, seed, r['verdict'], r['detail'][:160], r['secs']), flush=True)
        if (k + 1) % 50 == 0:
            print('-- through k = %d: %s' % (k, dict(tally)), flush=True)
print('done %d..%d: %s' % (k0, k1 - 1, dict(tally)), flush=True)
