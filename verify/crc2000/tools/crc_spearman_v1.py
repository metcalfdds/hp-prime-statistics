# crc_spearman_v1.py : the critical values of Spearman's rs (p.375) against the exact distribution, n to 16
import sys, re, math, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from crc_lib import *
import numpy as np
def counts(n):
    M = n * (n * n - 1) // 3
    cur = {0: np.zeros(M + 1)}; cur[0][0] = 1.0
    for i in range(n):
        nx = {}
        for mask, v in cur.items():
            for j in range(n):
                if mask >> j & 1: continue
                d = (i - j) ** 2; m2 = mask | (1 << j)
                if m2 not in nx: nx[m2] = np.zeros(M + 1)
                if d == 0: nx[m2] += v
                else: nx[m2][d:] += v[:-d]
        cur = nx
    return cur[(1 << n) - 1]
al = None; rows = []
for ln in L(375):
    tk = [t for a, b, t in toks(ln)]
    if al is None and 'α' in tk and '=' in tk and sum(isnum(t) for t in tk) >= 3: al = [float(t) for t in tk if isnum(t)]; continue
    if al and len(tk) == len(al) + 1 and tk[0].isdigit(): rows.append((int(tk[0]), tk[1:]))
out = []
for n, vals in rows:
    if n > 16: continue
    c = counts(n); tot = c.sum(); D = n * (n * n - 1); cum = np.cumsum(c) / tot
    for a, t in zip(al, vals):
        if not isnum(t): continue
        Sp = (1 - float(t)) * D / 6.0; S = int(round(Sp))
        exact_gt = max(s for s in range(0, len(c), 2) if (cum[s - 1] if s > 0 else 0.0) <= a)     # P(rs > r_s) <= a
        exact_ge = max([s for s in range(0, len(c), 2) if cum[s] <= a] or [-2])                    # P(rs >= r_s) <= a
        out.append(dict(n=n, alpha=a, printed=t, S_printed=Sp, P_ge=float(cum[S]), P_gt=float(cum[S - 1]) if S > 0 else 0.0,
                        r_rule_gt=1 - 6.0 * exact_gt / D, r_rule_ge=(1 - 6.0 * exact_ge / D) if exact_ge >= 0 else None))
json.dump(out, open(W + '/res_spearman_detail.json', 'w'), indent=0)
fit_gt = sum(1 for o in out if abs(o['r_rule_gt'] - float(o['printed'])) < 5.1e-5)
fit_ge = sum(1 for o in out if o['r_rule_ge'] is not None and abs(o['r_rule_ge'] - float(o['printed'])) < 5.1e-5)
print('cells n<=16:', len(out), ' fit rule P(rs>c)<=a:', fit_gt, ' fit rule P(rs>=c)<=a:', fit_ge)
for o in out:
    g = abs(o['r_rule_gt'] - float(o['printed'])) < 5.1e-5
    if not g or o['n'] >= 12:
        print('n %2d a %-6g printed %s (S %.2f)  P(rs>=c) %.6f  P(rs>c) %.6f  exact c [>] %.4f  [>=] %s' % (
            o['n'], o['alpha'], o['printed'], o['S_printed'], o['P_ge'], o['P_gt'], o['r_rule_gt'],
            '%.4f' % o['r_rule_ge'] if o['r_rule_ge'] is not None else '-'))
