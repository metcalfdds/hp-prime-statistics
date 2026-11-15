# crc_finney_v1.py : what are the probabilities printed in the 2 x 2 tables (pp.254-267)?  For each cell "b.ppp" the
# cumulative tail P(X <= b) and the single term P(X = b) are worked out for the printed b, and the rule that gives b is tried.
import sys, re, json, collections
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from crc_lib import *
from scipy import stats
E = r'(?:\d+\.\d{3}|[−–-])'
pat = re.compile(r'(?:A\s*=\s*(\d+)\s+)?(?:B\s*=\s*(\d+)\s+)?(\d+)\s+(' + E + r')\s+(' + E + r')\s+(' + E + r')\s+(' + E + r')(?=\s|$)')
levels = [0.05, 0.025, 0.01, 0.005]; A = B = None; cells = []
for p in range(254, 268):
    thr = None; left = []; right = []
    for ln in L(p):
        if thr is None:
            ms = [m.end() for m in re.finditer(r'0\.005', ln)]
            if len(ms) >= 1 and '0.025' in ln: thr = ms[0] - 5
            continue
        for m in pat.finditer(ln): (left if m.start() < thr else right).append(m.groups())
    for g in left + right:
        if g[0]: A = int(g[0])
        if g[1]: B = int(g[1])
        for lev, e in zip(levels, g[3:]):
            cells.append((p, A, B, int(g[2]), lev, e))
def rd(x): return verdict
c = collections.Counter(); brule = collections.Counter(); ex = collections.defaultdict(list); byAB = collections.Counter()
out = []
for p, A, B, a, lev, e in cells:
    tail = lambda b: stats.hypergeom.cdf(b, A + B, B, a + b)
    pmf = lambda b: stats.hypergeom.pmf(b, A + B, B, a + b)
    bt = max([b for b in range(0, B + 1) if tail(b) <= lev * (1 + 1e-9)] or [-1])        # largest b with tail <= level
    bp = max([b for b in range(0, B + 1) if pmf(b) <= lev * (1 + 1e-9) and b * A < a * B] or [-1])   # largest b (below a/A) with single term <= level
    if e in ('−', '–', '-'):
        k = 'dash: tail rule ' + ('agrees' if bt == -1 else 'gives b=%d' % bt)
        c[k if bt == -1 else 'dash where the tail rule gives a b'] += 1
        if bt != -1: ex['dash'].append((p, A, B, a, lev, e, bt, round(float(tail(bt)), 4)))
        continue
    b = int(e.split('.')[0]); pp = '0.' + e.split('.')[1]
    vt = verdict(pp, tail(b)); vp = verdict(pp, pmf(b))
    kb = 'b = tail-rule b' if b == bt else ('b = tail-rule b %+d' % (b - bt))
    brule[kb] += 1
    c['printed p: tail %s / single term %s' % (vt, vp)] += 1
    if b != bt: ex['b'].append((p, A, B, a, lev, e, bt, round(float(tail(bt)), 4) if bt >= 0 else None, round(float(tail(b)), 4)))
    if vt != 'ok': byAB[(vt, 'tail of printed b > level' if tail(b) > lev else 'ok level')] += 1
    out.append([p, A, B, a, lev, e, b, bt, float(tail(b)), float(pmf(b))])
json.dump(out, open(W + '/finney_cells.json', 'w'))
print('cells', len(cells))
for k, v in sorted(c.items(), key=lambda kv: -kv[1]): print('  %5d  %s' % (v, k))
for k, v in sorted(brule.items(), key=lambda kv: -kv[1]): print('  %5d  %s' % (v, k))
print(dict(byAB))
for k in ('dash', 'b'):
    print(k, len(ex[k]), ex[k][:6])
