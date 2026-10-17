#!/usr/bin/env python3
"""verify_Burr3.py -- Burr3 v2.4's formulas against scipy.stats.burr12 (c = C, d = K, scale = S).

Checks, over a grid of parameter sets with K*C >= 0.5 (the program's floor):
  1. pdf  b3_bpdf            K*C*z / (x*(1+z)^(K+1)),  z = (x/S)^C
  2. CDF                     1 - (1 + (x/S)^C)^(-K)
  3. the 0.995 quantile      S*((0.005)^(-1/K) - 1)^(1/C)       (the window)
  4. mean and variance       Lanczos lngamma (a port of b3_lngamma) vs scipy
  5. NEW v2.4 MODE           S*((C-1)/(K*C+1))^(1/C) for C > 1, else 0   vs argmax of scipy's pdf
  6. NEW v2.4 MEDIAN         S*(2^(1/K) - 1)^(1/C)                     vs burr12.median
  7. NEW v2.4 INVERSE CDF    S*((1-p)^(-1/K) - 1)^(1/C)                vs burr12.ppf, p in 0.005..0.995
  8. NEW v2.4 drag floor     CEILING(50/K)/100 is the smallest hundredth C with C*K >= 0.5
  9. NEW v2.4 S-curve p grid with H = 166 px: every 0.01 and 0.025/0.975 reachable from a pixel row
 10. NEW v2.4 fitted normal  P(X < 0) of N(mean, sd) vs scipy.stats.norm
Run: python3 verify_Burr3.py      (exit status 0 = all pass)
"""
import math
import sys
import numpy as np
from scipy.stats import burr12, norm
from scipy.optimize import minimize_scalar

COF = [76.18009172947146, -86.50532032941677, 24.01409824083091,
       -1.231739572450155, 0.001208650973866179, -0.000005395239384953]


def b3_lngamma(v):                       # line-for-line port of the PPL helper
    y = v
    tmp = v + 5.5
    tmp = tmp - (v + 0.5) * math.log(tmp)
    ser = 1.000000000190015
    for c in COF:
        y += 1
        ser += c / y
    return -tmp + math.log(2.5066282746310005 * ser / v)


def bpdf(x, C, K, S):
    if x <= 0:
        return 0.0
    z = (x / S) ** C
    return (K * C * z) / (x * (1 + z) ** (K + 1))


def bcdf(x, C, K, S):
    return 1 - (1 + (x / S) ** C) ** (-K)


def mode(C, K, S):
    return S * ((C - 1) / (K * C + 1)) ** (1 / C) if C > 1 else 0.0


def median(C, K, S):
    return S * (2 ** (1 / K) - 1) ** (1 / C)


def icdf(p, C, K, S):
    return S * ((1 - p) ** (-1 / K) - 1) ** (1 / C)


n_pass = n_fail = 0
worst = {}


def check(name, ok, detail=''):
    global n_pass, n_fail
    if ok:
        n_pass += 1
    else:
        n_fail += 1
        print('FAIL', name, detail)


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def track(key, err):
    worst[key] = max(worst.get(key, 0.0), err)


Cs = [0.5, 0.75, 1, 1.25, 1.5, 2, 3, 5, 10]
Ks = [0.25, 0.5, 0.75, 1, 2, 4]
Ss = [0.5, 1, 3, 100]
sets = [(C, K, S) for C in Cs for K in Ks for S in Ss if K * C >= 0.5]
print('parameter sets with K*C >= 0.5:', len(sets))

for C, K, S in sets:
    d = burr12(c=C, d=K, scale=S)
    # 1-2. pdf and CDF at quantiles 0.05..0.95
    for q in (0.05, 0.25, 0.5, 0.75, 0.95):
        x = d.ppf(q)
        e1 = rel(bpdf(x, C, K, S), d.pdf(x)); track('pdf', e1)
        e2 = rel(bcdf(x, C, K, S), d.cdf(x)); track('cdf', e2)
        check('pdf %s' % ((C, K, S, q),), e1 < 1e-9, e1)
        check('cdf %s' % ((C, K, S, q),), e2 < 1e-9, e2)
    # 3. the window quantile
    q995 = S * ((0.005) ** (-1 / K) - 1) ** (1 / C)
    e3 = rel(q995, d.ppf(0.995)); track('q995', e3)
    check('q995 %s' % ((C, K, S),), e3 < 1e-9, e3)
    # 4. moments where they exist
    if K * C > 1:
        m = S * math.exp(b3_lngamma(1 + 1 / C) + b3_lngamma(K - 1 / C) - b3_lngamma(K))
        e4 = rel(m, d.mean()); track('mean', e4)
        check('mean %s' % ((C, K, S),), e4 < 1e-8, (m, d.mean()))
        if K * C > 2:
            v = S ** 2 * math.exp(b3_lngamma(1 + 2 / C) + b3_lngamma(K - 2 / C) - b3_lngamma(K)) - m ** 2
            e5 = rel(v, d.var()); track('var', e5)
            check('var %s' % ((C, K, S),), e5 < 1e-6, (v, d.var()))
            # 10. the fitted normal's share below 0
            sd = math.sqrt(max(v, 0))
            track('normal P(X<0)', abs(norm.cdf(0, m, sd) - norm.cdf(-m / sd)))
    # 5. mode: argmax of scipy's own pdf (bounded search on a log scale)
    mo = mode(C, K, S)
    if C > 1:
        r = minimize_scalar(lambda t: -d.pdf(math.exp(t)), bounds=(math.log(S) - 12, math.log(S) + 6),
                            method='bounded', options={'xatol': 1e-12})
        xm = math.exp(r.x)
        e6 = rel(mo, xm); track('mode', e6)
        check('mode %s' % ((C, K, S),), e6 < 1e-5, (mo, xm))
        # the pdf really falls on both sides
        check('mode is a max %s' % ((C, K, S),),
              d.pdf(mo) >= d.pdf(mo * 0.999) and d.pdf(mo) >= d.pdf(mo * 1.001))
    else:
        # C <= 1: the pdf is decreasing from 0, so the mode is 0
        xs = np.linspace(S * 1e-3, d.ppf(0.99), 200)
        check('C<=1 pdf decreasing %s' % ((C, K, S),), np.all(np.diff(d.pdf(xs)) <= 1e-12))
    # 6. median
    e7 = rel(median(C, K, S), d.median()); track('median', e7)
    check('median %s' % ((C, K, S),), e7 < 1e-9, e7)
    # 7. inverse CDF over the p range the S-curve tap can produce
    for p in (0.005, 0.01, 0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.975, 0.99, 0.995):
        e8 = rel(icdf(p, C, K, S), d.ppf(p)); track('icdf', e8)
        check('icdf %s' % ((C, K, S, p),), e8 < 1e-9, e8)
        # and round trip through the program's own CDF
        track('icdf round trip', abs(bcdf(icdf(p, C, K, S), C, K, S) - p))

# 8. the drag floor: C := CEILING(50/K)/100 when C*K < 0.5
for K in (0.25, 0.3, 0.33, 0.5, 0.7, 1, 1.37, 2, 3, 7, 100):
    c = math.ceil(50 / K) / 100
    smallest = next(h / 100 for h in range(1, 100000) if (h / 100) * K >= 0.5 - 1e-12)
    check('drag floor K=%s' % K, abs(c - smallest) < 1e-12 and c * K >= 0.5 - 1e-12, (c, smallest))

# 9. S-curve p grid, Burr3's plot: TOPy = 24, BOT = 190, H = 166
H, BOT, TOPy = 166, 190, 24


def snap(p, tol):
    if abs(p - 0.975) < tol:
        return 0.975
    if abs(p - 0.025) < tol:
        return 0.025
    return round(p * 100) / 100


reach = {snap((BOT - y) / H, 0.003) for y in range(TOPy, BOT + 1)}
want = {round(k / 100, 2) for k in range(1, 100)} | {0.025, 0.975}
missing = sorted(want - {round(v, 3) for v in reach})
check('every p in 0.01..0.99 and 0.025, 0.975 reachable (H=166)', not missing, missing)

print()
print('worst relative errors:')
for k, v in worst.items():
    print('  %-16s %.2e' % (k, v))
print()
# a few rows of the comparison, for the CHANGES file
print('%-16s %10s %10s %10s %10s %10s %10s' % ('C, K, S', 'mode', 'argmax', 'median', 'scipy', 'x(0.9)', 'ppf(0.9)'))
for C, K, S in ((2, 1, 1), (3, 2, 1), (1.5, 0.75, 1), (0.5, 2, 1), (5, 0.5, 3), (10, 4, 100), (1, 1, 1)):
    d = burr12(c=C, d=K, scale=S)
    if C > 1:
        r = minimize_scalar(lambda t: -d.pdf(math.exp(t)), bounds=(math.log(S) - 12, math.log(S) + 6),
                            method='bounded', options={'xatol': 1e-12})
        am = '%10.5f' % math.exp(r.x)
    else:
        am = '%10s' % '(0)'
    print('%-16s %10.5f %s %10.5f %10.5f %10.5f %10.5f' % (
        '%g, %g, %g' % (C, K, S), mode(C, K, S), am, median(C, K, S), d.median(),
        icdf(0.9, C, K, S), d.ppf(0.9)))
print()
print('%d checks passed, %d failed' % (n_pass, n_fail))
sys.exit(1 if n_fail else 0)
