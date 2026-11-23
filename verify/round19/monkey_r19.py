# -*- coding: utf-8 -*-
"""monkey_r19.py -- Round 19's monkey runs: 1,000 runs of random keys, taps, menu picks and typed values for each of the
two programs round 19 changed, StatDist v2.7p and EpiStats v1.7o (a copy of verify/round18/monkey_r18.py with base 19).

Each program goes to tools/monkey_chunks_v1.py with base 19 and --lists (seed = 19 x 1000003 + k, so --replay repeats any
run), two programs at a time; the runs are written to mk/<Name>.jsonl as they end, so a stopped job resumes where it was.
The calls are the verify script's; --writes names the Home variables a program is meant to fill (docs/dev/monkey-fleet-
2026-11-01.md: NormExplorer's z-scores into D2, GaltonBoard's bins into D1 and D2, ScatterLab's "Save to C1, C2", FitCheck's
residuals into D, DataLoad's columns into D and C); GaltonBoard, which is paced by the clock, gets 120 s a run.

Then every run that did not end OK is run again, with its own seed, on the version before (from git, make_round19.BASE),
because the round must not have made a run go wrong that went right before.  A run that goes wrong in both versions is the program's as it was, and is listed as such.

Run from the repository's root:   python3 verify/round19/monkey_r19.py            (prints one line a program)
"""
import collections, io, json, os, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
os.chdir(REPO); os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, HERE)
import make_round19 as R19  # noqa: E402
R = R19.R18

RUNS, BASE = 1000, 19
CALLS = {'PowerViz': 'POWERVIZ()', 'TTestLab': 'TTESTLAB()', 'TTestLabG': 'TTESTLABG()', 'DataLoad': 'DATALOAD()',
         'NormExplorer': 'NormExp()', 'Norm3': 'Norm3(100,15,130)', 'EpiStats': 'EpiStats()'}
WRITES = {'NormExplorer': 'D', 'GaltonBoard': 'D', 'ScatterLab': 'C', 'FitCheck': 'D', 'DataLoad': 'D,C'}
SECONDS = {'GaltonBoard': '120', 'StatDist': '240'}      # StatDist: a page that asks the CAS is slow in the harness
PAIRS = sorted([(n, ov, R.nxt(ov)) for n, ov in R19.OLD.items()])
MK = os.path.join(HERE, 'mk'); os.makedirs(MK, exist_ok=True)


def opts(n):
    o = ['--lists']
    if n in WRITES:
        o += ['--writes', WRITES[n]]
    o += ['--seconds', SECONDS.get(n, '30')]
    return o


def runs(n):
    f = os.path.join(MK, n + '.jsonl')
    return [json.loads(l) for l in open(f)] if os.path.exists(f) else []


def job(p):
    n, ov, nv = p
    if len(runs(n)) < RUNS:
        subprocess.run([sys.executable, 'tools/monkey_chunks_v1.py', 'programs/%s_%s.txt' % (n, nv), CALLS.get(n, n + '()'),
                        str(BASE), '0', str(RUNS), os.path.join(MK, n + '.jsonl')] + opts(n),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    L = runs(n)
    c = collections.Counter(r['verdict'] for r in L)
    bad = [r for r in L if r['verdict'] != 'OK']
    # every run that went wrong, again on the version before, with the same seed
    old_txt = subprocess.run(['git', 'show', '%s:programs/%s_%s.txt' % (R19.BASE, n, ov)], capture_output=True).stdout
    tmp = os.path.join(tempfile.mkdtemp(prefix='mk19_'), '%s_%s.txt' % (n, ov)); open(tmp, 'wb').write(old_txt)
    same, new_only = [], []
    for r in bad:
        o = subprocess.run([sys.executable, 'tools/monkey_v1b.py', tmp, CALLS.get(n, n + '()'), '--replay', str(r['seed']),
                            '--events', '150'] + opts(n), capture_output=True, text=True).stdout     # 150: monkey_chunks_v1's events
        try:
            was = json.loads(o[o.index('{'):])['verdict']
        except Exception:
            was = '?'
        (same if was == r['verdict'] else new_only).append(r)
    line = '%-12s %s: %d runs; %s%s' % (n, nv, len(L), ', '.join('%s %d' % kv for kv in sorted(c.items(), key=lambda kv: -kv[1])),
                                        ('; every one that was not OK did the same on %s' % ov if bad and not new_only else '') +
                                        (('; NOT ON %s TOO: seeds %s' % (ov, ', '.join(str(r['seed']) for r in new_only[:8]))) if new_only else ''))
    print(line, flush=True)
    return n, line, [dict(seed=r['seed'], verdict=r['verdict'], detail=r['detail'][:160], also_before=(r not in new_only)) for r in bad]


if __name__ == '__main__':
    with ThreadPoolExecutor(2) as ex:
        out = list(ex.map(job, PAIRS))
    io.open(os.path.join(HERE, 'monkey_r19.txt'), 'w', encoding='utf-8').write(
        'Round 19, the monkey: tools/monkey_chunks_v1.py, base %d, --lists, 1,000 runs a program (verify/round19/monkey_r19.py).\n\n' % BASE + '\n'.join(sorted(l for _, l, _ in out)) + '\n')
    json.dump({n: b for n, _, b in out}, open(os.path.join(MK, 'not_ok.json'), 'w'), indent=1)
    print('written verify/round19/monkey_r19.txt', flush=True)
