# crc_dunnett2_v1.py : the rows of the two-sided 5% Dunnett table (p.297) whose labels the text layer lost.
# Twelve lines hold eight values each (k = 2 .. 9) with no row label; in order they are the rows for 10 .. 20 and 24
# degrees of freedom (checked against the first row found: with 10 df and two treatments Dunnett's value is 2.57).
import sys, re, math
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from crc_lib import *
import numpy as np
from scipy import stats, optimize
GX, GW = np.polynomial.legendre.leggauss(400)
def two(k, v):
    z = 9 * GX; wz = 9 * GW
    lo = math.sqrt(stats.chi2.ppf(1e-13, v) / v); hi = math.sqrt(stats.chi2.isf(1e-13, v) / v)
    s = 0.5 * (hi - lo) * GX + 0.5 * (hi + lo); ws = 0.5 * (hi - lo) * GW
    fs = 2 * v * s * stats.chi2.pdf(v * s * s, v)
    Z, S = np.meshgrid(z, s, indexing='ij'); Wt = np.outer(wz * stats.norm.pdf(z), ws * fs); r2 = math.sqrt(2.0)
    return lambda d: float(np.sum(Wt * (stats.norm.cdf(Z + r2 * d * S) - stats.norm.cdf(Z - r2 * d * S)) ** k))
rows = []
for ln in L(297):
    tk = [t for a, b, t in toks(ln)]
    if len(tk) == 8 and all(re.match(r'^\d\.\d\d$', t) for t in tk): rows.append(tk)
dfs = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24]
T = Tally('dunnett_two-sided_0.05_rows10to24', "Dunnett's d, two-sided, alpha = 0.05, rows 10 to 24 (k = 2 to 9)")
# seventeen such lines stand on the page: the twelve wanted, then the rows for 30, 40, 60, 120 and infinity again (those also stand with their labels)
if len(rows) != 17: T.note('found %d unlabelled lines, expected 17' % len(rows))
else:
    rows = rows[:12]
    for v, tk in zip(dfs, rows):
        for k, t in enumerate(tk, start=2):
            f = two(k, v)
            T.add(297, 'df %d' % v, 'k %d' % k, t, optimize.brentq(lambda d: f(d) - 0.95, 0.5, 40, xtol=1e-9))
T.done(show=4)
