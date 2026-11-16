#!/usr/bin/env python3
"""monkey_reach_v1.py -- how often the monkey's random sessions reach a program's NEW pages (Round 16, 15 Nov 2026).

A monkey test says "1,000 of 1,000 runs OK".  That is worth little for a new page if random keys seldom get there, so this
runs the very same sessions again (seed = BASE x 1000003 + k, monkey_v1b's rule; the same lists and matrix) and counts the
runs in which at least one screen carried a text that matches each pattern.

    python3 verify/round16/monkey_reach_v1.py PROG CALL BASE K0 K1 [--writes D] [--skip REGEX] NAME=REGEX [NAME=REGEX ...]

A screen that matches --skip (a help page, say) is left out of the count.

Prints one line: the runs, the verdicts, and for each NAME the number of runs that reached it (and of screens).
"""
import collections
import os
import random
import re
import signal
import sys
import time
import warnings

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))
a = sys.argv[1:]
sys.argv = ['monkey_v1b.py']
import monkey_v1b as M  # noqa: E402

prog, call, base, k0, k1 = a[0], a[1], int(a[2]), int(a[3]), int(a[4])
rest = a[5:]
if '--writes' in rest:
    i = rest.index('--writes')
    M.WRITES.update(w.strip() for w in rest[i + 1].split(',') if w.strip())
    del rest[i:i + 2]
skip = None
if '--skip' in rest:
    i = rest.index('--skip')
    skip = re.compile(rest[i + 1])
    del rest[i:i + 2]
pats = [(r.split('=', 1)[0], re.compile(r.split('=', 1)[1])) for r in rest]
EVENTS, SECONDS = 150, 30          # monkey_chunks_v1's own settings

runs = collections.Counter()
scr = collections.Counter()
verd = collections.Counter()
t0 = time.time()
for k in range(k0, k1):
    seed = base * 1000003 + k
    rng = random.Random(seed)
    app, kind = M.random_lists(rng)
    h = M.Monkey(prog, rng, app, EVENTS)
    for j in range(10):
        h.globals_.setdefault('M%d' % j, M.R.interp.Matrix([[0.0]]))
    m1, mkind = M.random_matrix(seed)
    if m1 is not None:
        h.globals_['M1'] = m1
    v = 'OK'
    signal.signal(signal.SIGALRM, M._alarm)
    signal.alarm(SECONDS)
    try:
        h.execute(call)
    except BaseException as e:                     # the verdicts are monkey_chunks_v1's business; here only the reach
        if isinstance(e, KeyboardInterrupt):
            raise
        v = type(e).__name__
    finally:
        signal.alarm(0)
    verd[v] += 1
    hit = collections.Counter()
    for s in h.screens:
        txt = ' | '.join(t.text for t in s.texts)
        if skip is not None and skip.search(txt):
            continue
        for name, rx in pats:
            if rx.search(txt):
                hit[name] += 1
    for name, n in hit.items():
        runs[name] += 1
        scr[name] += n
print('%s  runs %d..%d  verdicts %s  reached: %s   (%d s)' % (
    os.path.basename(prog), k0, k1 - 1, dict(verd),
    '; '.join('%s in %d runs (%d screens)' % (n, runs[n], scr[n]) for n, _ in pats), time.time() - t0))
