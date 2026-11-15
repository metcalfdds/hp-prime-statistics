# -*- coding: utf-8 -*-
"""crc_check_v2.py -- part 2 of the comparison of Zwillinger & Kokoska (2000) with SciPy: the critical values of F (PDF pages
141 to 146), the cumulative binomial (96 to 100) and the cumulative Poisson (114 to 118).  Same rules as crc_check_v1.py.
  python3 -I tools/crc_check_v2.py work/all.txt work/part2.json"""
import sys, re, io, json, math
from scipy import stats
pages = io.open(sys.argv[1], encoding='utf-8', errors='replace').read().split('\f')
NUM = r'[−-]?\d*\.\d+|[−-]?\d+|∞'
def nums(l): return [x.replace('−', '-') for x in re.findall(NUM, l)]
def dec(s): return len(s.split('.')[1]) if '.' in s else 0
def verdict(printed, true):
    d = dec(printed); p = float(printed); unit = 10.0 ** (-d)
    if abs(p - true) <= 0.5 * unit * (1 + 1e-9) + 1e-12: return 'ok'
    if abs(p - true) <= 1.0 * unit * (1 + 1e-9): return 'last digit'
    return 'DIFFERS'
res = {'tables': {}, 'cells': [], 'odd': []}
def note(table, page, where, printed, true):
    v = verdict(printed, true); t = res['tables'].setdefault(table, {'cells': 0, 'ok': 0, 'last digit': 0, 'DIFFERS': 0}); t['cells'] += 1; t[v] += 1
    if v != 'ok': res['cells'].append([table, page, where, printed, round(float(true), dec(printed) + 3), v])
def fcrit(a, v1, v2):
    if v1 == math.inf and v2 == math.inf: return 1.0
    if v2 == math.inf: return stats.chi2.isf(a, v1) / v1
    if v1 == math.inf: return v2 / stats.chi2.ppf(a, v2)
    return stats.f.isf(a, v1, v2)
I = lambda s: math.inf if s == '∞' else int(s)
for p, a in zip(range(141, 147), (0.1, 0.05, 0.025, 0.01, 0.005, 0.001)):
    cols = None
    for l in pages[p - 1].split('\n'):
        if 'ν1' in l and '=' in l: cols = [I(x) for x in nums(l.split('=')[1])]
        elif cols:
            n = nums(l)
            if len(n) == len(cols) + 1 and ('.' not in n[0]):
                for c, x in zip(cols, n[1:]):
                    if x != '∞': note('F critical, alpha %g' % a, p, 'v1=%s v2=%s' % (c, n[0]), x, fcrit(a, c, I(n[0])))
            elif n and '.' not in n[0] and len(n) > 3: res['odd'].append(['F', p, l.strip()[:90]])
# cumulative binomial
for p in range(96, 101):
    ps = None; ncur = None
    for l in pages[p - 1].split('\n'):
        if 'p =' in l: ps = [float(x) for x in nums(l.split('p =')[1])]; continue
        if not ps: continue
        n = nums(l)
        vals = [x for x in n if '.' in x]; ints = [x for x in n if '.' not in x]
        if len(vals) == len(ps) and len(ints) in (1, 2) and n[:len(ints)] == ints:
            if len(ints) == 2: ncur = int(ints[0])
            x = int(ints[-1])
            if ncur is None: res['odd'].append(['binomial', p, l.strip()[:80]]); continue
            for pr, v in zip(ps, vals): note('binomial cdf', p, 'n=%d x=%d p=%g' % (ncur, x, pr), v, stats.binom.cdf(x, ncur, pr))
        elif vals: res['odd'].append(['binomial', p, l.strip()[:80]])
# cumulative Poisson: the header gives the x of each column; a row stops when the cdf has reached 1.000
for p in range(114, 119):
    xs = None
    for l in pages[p - 1].split('\n'):
        if 'x =' in l or 'x=' in l:
            xs = [int(x) for x in nums(l.split('=')[1])]; continue
        if not xs: continue
        n = nums(l)
        if len(n) >= 2 and '.' in n[0] and all(dec(v) == 3 for v in n[1:]) and len(n) - 1 <= len(xs):
            lam = float(n[0])
            # a row that begins at a later column is indented: place the values by their text columns is not possible here, so
            # take the alignment that fits best (the leading columns of a row may be blank only if they are 0.000, which is printed)
            for x, v in zip(xs, n[1:]): note('Poisson cdf', p, 'lambda=%s x=%d' % (n[0], x), v, stats.poisson.cdf(x, lam))
        elif n and '.' in n[0] and len(n) > 2: res['odd'].append(['Poisson', p, l.strip()[:80]])
json.dump(res, open(sys.argv[2], 'w'), indent=0)
for k, v in res['tables'].items(): print('%-26s %s' % (k, v))
print('odd lines not read:', len(res['odd']), res['odd'][:6])
shown = 0
for c in res['cells']:
    if c[5] == 'DIFFERS' and shown < 25: print('  ', c[:5]); shown += 1
