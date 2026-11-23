# -*- coding: utf-8 -*-
"""monkey_r18_slow.py -- the monkey's FREEZE verdicts of round 18, run again with time to end.

monkey_r18.py gave every program 30 s a run (GaltonBoard 120 s).  StudRange's pages are slow in the PC harness, and the
fleet's monkey has given it 240 s a run since 2 Nov 2026 (docs/dev/monkey-fleet-2026-11-01.md: "StudRange's 76 FREEZE
verdicts were plots the harness draws slowly"; one replayed with 240 s ended after 154 s).  So each run that monkey_r18.py
called FREEZE is replayed here, with its own seed and the same options, on the new version with 240 s.  A run that then
ends OK was slow, not stuck; one that is still running at 240 s is listed.

The replays are written to mk/slow_replays.jsonl as they end, so a stopped job resumes.

Run from the repository's root, after monkey_r18.py:   python3 verify/round18/monkey_r18_slow.py
"""
import collections, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
os.chdir(REPO); os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, HERE)
import make_round18 as R  # noqa: E402
import monkey_r18 as M    # noqa: E402

SLOW = 240
OUT = os.path.join(M.MK, 'slow_replays.jsonl')
bad = json.load(open(os.path.join(M.MK, 'not_ok.json')))
todo = [(n, r['seed']) for n, rs in sorted(bad.items()) for r in rs if r['verdict'] == 'FREEZE']
done = {(d['name'], d['seed']) for d in (json.loads(l) for l in open(OUT))} if os.path.exists(OUT) else set()
ver = dict((n, nv) for n, ov, nv in M.PAIRS)


def one(job):
    n, seed = job
    o = [x for x in M.opts(n)]
    o[o.index('--seconds') + 1] = str(SLOW)
    out = subprocess.run([sys.executable, 'tools/monkey_v1b.py', 'programs/%s_%s.txt' % (n, ver[n]), M.CALLS.get(n, n + '()'),
                          '--replay', str(seed), '--events', '150'] + o, capture_output=True, text=True).stdout
    try:
        r = json.loads(out[out.index('{'):])
        d = dict(name=n, seed=seed, verdict=r['verdict'], secs=r['secs'], detail=r['detail'][:160])
    except Exception:
        d = dict(name=n, seed=seed, verdict='?', secs=None, detail=out[-160:])
    with open(OUT, 'a') as f:
        f.write(json.dumps(d) + '\n')
    return d


if __name__ == '__main__':
    with ThreadPoolExecutor(2) as ex:
        list(ex.map(one, [j for j in todo if j not in done]))
    rows = [json.loads(l) for l in open(OUT)]
    for n in sorted({r['name'] for r in rows}):
        mine = [r for r in rows if r['name'] == n]
        c = collections.Counter(r['verdict'] for r in mine)
        secs = sorted(r['secs'] for r in mine if r['verdict'] == 'OK' and r['secs'] is not None)
        line = '%-12s %s: %d FREEZE at 30 s, with %d s: %s' % (n, ver[n], len(mine), SLOW,
               ', '.join('%s %d' % kv for kv in sorted(c.items(), key=lambda kv: -kv[1])))
        if secs:
            line += '; those that ended took %.0f to %.0f s (median %.0f)' % (secs[0], secs[-1], secs[len(secs) // 2])
        still = [str(r['seed']) for r in mine if r['verdict'] != 'OK']
        if still:
            line += '; NOT ENDED OR NOT OK: seeds ' + ', '.join(still[:10])
        print(line, flush=True)
