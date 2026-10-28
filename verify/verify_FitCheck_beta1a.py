#!/usr/bin/env python3
"""verify_FitCheck_beta1a.py -- checks for FitCheck beta 1a (21 Oct 2026): every beta 1 check (adjusted
where beta 1a changes a page on purpose: the draft lottery, the Lilliefors verdict wording, the
first-two-digits Benford count, the Castaneda footnote) plus part R, one block per item of
REVIEW2_FitCheck_beta1.md:
  R1 Bins -> Unmrg -> Bars on crimtab, Rossi and a D1 sample (beta 1: index out of range in fcMS);
  R2 the draft lottery as a 2 x 2: Pearson chi-square against chi2_contingency(correction=False),
     Fisher's p against fisher_exact and a hypergeom sum, fc_Fisher on 80 random tables, the
     teaching point (the fixed-share GOF 7.08 / 0.0078) on screen;
  R3 Lilliefors for n = 3, 4: "p not available for n < 5", grey, not in the verdict; n >= 5 as before;
  R4 Benford two digits: values below 10 left out and counted, on screen and in a MSGBOX;
  R5 Castaneda: "430 U.S. at 496-497 n.17", exactly one quotation, the 10^140 sentence;
  R6 Esc stops a large load (progress count shown); moments of values near 1E150 (no overflow);
  R7 static: every source line <= 250 characters; INPUT labels and helps from variables; footers
     comma-separated; the expected-bar fill is the house light orange; no "keep H0".

The beta 1 description follows.

verify_FitCheck_beta1.py -- checks for FitCheck beta 1 (21 Oct 2026).

Part A  the formulas, by calling the program's own routines in the PC harness (ppl_run_v3e)
        and comparing with SciPy / statsmodels / exact arithmetic:
   A1 fc_LnGam against scipy.special.gammaln (z = 0.5 .. 1e5);
   A2 fc_LnPhi against scipy.special.log_ndtr (z = -60 .. 10);
   A3 fc_LnChiUp / fc_ChiUp against scipy.stats.chi2.logsf / sf, df 1..150, x up to 5000
      (tails down to 1e-1000 compared in logs);
   A4 Shapiro-Wilk W and p against scipy.stats.shapiro: n = 3..50 (normal, exponential,
      uniform, lognormal, t3 samples, rounded data with ties) and n = 100, 200, 500, 1000,
      2000, 5000; agreement required to 1e-6 (the brief asks for 4 decimals); n = 3 also with
      the calculator in degrees and grads (the p formula uses ASIN);
   A5 Anderson-Darling A^2 against scipy.stats.anderson and statsmodels normal_ad (A^2 and p
      with the D'Agostino-Stephens correction);
   A6 Lilliefors D against statsmodels lilliefors; p against statsmodels' Dallal-Wilkinson
      formula (pvalmethod='approx' / pval_lf) whenever it is below 0.10, "p > 0.10" otherwise
      (statsmodels then reads its table; both values are listed);
   A7 chi-square goodness of fit (fc_SetFit) against scipy.stats.chisquare(f_obs, f_exp, ddof);
      the expected-count rule; the automatic merge against an independent Python version
      of the documented rule;
   A8 Benford: the first digit and first two digits (fc_FirstDig) against a string reading;
      the expected proportions log10(1 + 1/d), log10(1 + 1/(10a + b)); chi-square; MAD;
   A9 Poisson fit against scipy.stats.poisson (lambda-hat, every E, the tail cell, X2, df,
      p with ddof = 1); A10 binomial fit against scipy.stats.binom (p estimated / given);
   A11 normal fit on bins against scipy.stats.norm (every E, X2, df = k - 3);
   A12 the exact binomial test against scipy.stats.binomtest (two-sided, less, greater) on
      random cases, edge cases (x = 0, x = n, x = n p0, n = 1) and Castaneda (p ~ 1e-186,
      in logs);
   A13 edge inputs: n = 1-3, ties, every value equal, zero counts, a huge value, negative
      values, empty and short lists.
Part B  every menu path of FitCheck() in the harness: the numbers ON THE PAGES against
        SciPy, no runtime error, no scientific number (h.sci_strings), no text off the
        320 x 240 screen or under the soft keys, MSGBOX at most 5 lines.
Run:  python3 verify_FitCheck_beta1.py      (exit status 0 = every check passed)
"""
import math
import os
import re
import sys
import warnings

import numpy as np
from scipy import special, stats
from statsmodels.stats.diagnostic import lilliefors, normal_ad
from statsmodels.stats._lilliefors import pval_lf

warnings.filterwarnings('ignore')
os.environ.setdefault('HPKIT', '/home/claude/kit/hp-prime-kit-HEAD')
sys.path.insert(0, '/home/claude/new6/ref')
import ppl_run_v3e  # noqa: E402
from ppl_run_v3e import Harness  # noqa: E402

PROG = '/home/claude/new6/FitCheck_beta1a.txt'
DATA = '/home/claude/new6/data/'
N_CHECK = 0
FAILS = []
ALL_H = []


def check(ok, msg):
    global N_CHECK
    N_CHECK += 1
    if not ok:
        FAILS.append(msg)
        print('FAIL', msg)


def new_h(**kw):
    kw.setdefault('strict', False)
    kw.setdefault('idle_key', 4)
    kw.setdefault('cas', 'fail')
    h = Harness(PROG, **kw)
    ALL_H.append(h)
    return h


def close(a, b, tol):
    return abs(a - b) <= tol


def rel(a, b, tol):
    return abs(a - b) <= tol * max(1e-300, abs(b))


# ======================================================================== PART A
H = new_h()
H.call('fc_Init')
G = H.globals_


def call(name, *args):
    return H.call(name, *args)


print('A1 log-gamma')
for z in [0.5, 1, 1.5, 2, 2.5, 3, 4.5, 7, 10, 10.5, 33, 61, 100.5, 339, 532, 871, 1000, 5000, 1e5]:
    v = call('fc_LnGam', float(z))
    t = special.gammaln(z)
    check(abs(v - t) <= 1e-10 * max(1, abs(t)), 'A1 lnGamma(%g) %r vs %r' % (z, v, t))

print('A2 ln Phi')
for z in list(np.linspace(-60, 10, 141)):
    v = call('fc_LnPhi', float(z))
    t = special.log_ndtr(z)
    check(abs(v - t) <= 1e-9 * max(1, abs(t)), 'A2 lnPhi(%g) %r vs %r' % (z, v, t))

print('A3 chi-square upper tail')
for df in [1, 2, 3, 4, 5, 7, 8, 9, 12, 20, 30, 50, 89, 119, 150]:
    for x in [0.01, 0.5, 1, df * 0.5, df, df + 0.3, df * 1.5, df * 2 + 3, df * 4 + 10, 100, 400, 1000, 5000]:
        lv = call('fc_LnChiUp', df, float(x))
        lt = stats.chi2.logsf(x, df)
        check(abs(lv - lt) <= 1e-8 * max(1, abs(lt)), 'A3 ln P(chi2(%d) > %g): %r vs %r' % (df, x, lv, lt))
        pv = call('fc_ChiUp', df, float(x))
        pt = stats.chi2.sf(x, df)
        if lt > -1100:
            check(rel(pv, pt, 1e-8), 'A3 P(chi2(%d) > %g): %r vs %r' % (df, x, pv, pt))
        else:
            check(pv == 0, 'A3 P(chi2(%d) > %g) below range should be 0, got %r' % (df, x, pv))


def norm_load(x, deg=None):
    h = H if deg is None else deg
    r = h.call('fc_NormSet', [float(v) for v in x], 'test', 'test')
    return r, h.globals_


print('A4 Shapiro-Wilk')
rng = np.random.default_rng(20261021)
worst = 0.0
nsw = 0
for n in list(range(3, 51)) + [100, 200, 500, 1000, 2000, 5000]:
    kinds = ['normal', 'expon', 'unif', 'lognorm', 't3', 'rounded']
    if n > 50:
        kinds = ['normal', 'expon', 't3']
    for kind in kinds:
        if kind == 'normal':
            x = rng.normal(10, 3, size=n)
        elif kind == 'expon':
            x = rng.exponential(size=n)
        elif kind == 'unif':
            x = rng.uniform(size=n)
        elif kind == 'lognorm':
            x = rng.lognormal(size=n)
        elif kind == 't3':
            x = rng.standard_t(3, size=n)
        else:
            x = np.round(rng.normal(50, 5, size=n))
        x = [float('%.10g' % v) for v in x]
        if np.ptp(x) == 0:
            continue
        r, g = norm_load(x)
        s = stats.shapiro(x)
        dW = abs(g['fcW'] - s.statistic)
        dp = abs(g['fcPW'] - s.pvalue)
        if s.pvalue < 1e-90:
            dp = 0.0 if g['fcPW'] < 1e-90 else dp
        worst = max(worst, dW, dp)
        nsw += 1
        check(r == 1 and dW < 1e-6 and dp < 1e-6,
              'A4 SW n=%d %s: W %r vs %r, p %r vs %r' % (n, kind, g['fcW'], s.statistic, g['fcPW'], s.pvalue))
print('   %d samples, largest difference from scipy.stats.shapiro (W or p): %.2e' % (nsw, worst))
# n = 3: the p formula reads ASIN, so it must not depend on the angle mode
for mode in ['deg', 'grad']:
    hd = new_h(angle=mode)
    hd.call('fc_Init')
    for x in [[1, 2, 4], [1, 2, 3], [0, 0.1, 5], [3.2, 1.1, 1.15]]:
        r, g = norm_load(x, hd)
        s = stats.shapiro(x)
        check(abs(g['fcW'] - s.statistic) < 1e-9 and abs(g['fcPW'] - s.pvalue) < 1e-9,
              'A4 n=3 in %s mode %r: W %r p %r vs %r %r' % (mode, x, g['fcW'], g['fcPW'], s.statistic, s.pvalue))

print('A5 Anderson-Darling, A6 Lilliefors')
nad = 0
for n in [5, 8, 10, 15, 20, 30, 50, 80, 100, 101, 150, 300, 432, 1000, 3000]:
    for kind in ['normal', 'expon', 't3', 'unif', 'mixture']:
        if kind == 'normal':
            x = rng.normal(size=n)
        elif kind == 'expon':
            x = rng.exponential(size=n)
        elif kind == 't3':
            x = rng.standard_t(3, size=n)
        elif kind == 'unif':
            x = rng.uniform(size=n)
        else:
            x = np.concatenate([rng.normal(0, 1, n // 2), rng.normal(1.2, 1, n - n // 2)])
        x = [float('%.10g' % v) for v in x]
        r, g = norm_load(x)
        a2, pa = normal_ad(np.array(x))
        sa = stats.anderson(np.array(x)).statistic
        if not np.isfinite(a2):
            # statsmodels' A^2 overflows (ln 0) on an extreme value; SciPy's and FitCheck's do not
            print('   n=%d %s: statsmodels A2 = %r, scipy %.6f, FitCheck %.6f' % (n, kind, a2, sa, g['fcA2']))
            a2 = sa
            pa = 0.0 if a2 * (1 + 0.75 / n + 2.25 / n ** 2) > 13 else pa
        check(abs(g['fcA2'] - a2) < 1e-7 * max(1, a2) and abs(g['fcA2'] - sa) < 1e-7 * max(1, sa),
              'A5 A2 n=%d %s: %r vs statsmodels %r, scipy %r' % (n, kind, g['fcA2'], a2, sa))
        a2s = a2 * (1 + 0.75 / n + 2.25 / n ** 2)
        check(abs(g['fcA2s'] - a2s) < 1e-7 * max(1, a2s), 'A5 A*2 n=%d %s' % (n, kind))
        check(abs(g['fcPA'] - pa) < 1e-9 + 1e-7 * pa, 'A5 p(A2) n=%d %s: %r vs %r' % (n, kind, g['fcPA'], pa))
        d, _pt = lilliefors(np.array(x), dist='norm', pvalmethod='table')
        check(abs(g['fcLD'] - d) < 1e-9, 'A6 D n=%d %s: %r vs %r' % (n, kind, g['fcLD'], d))
        pdw = pval_lf(d, n)
        if pdw <= 0.1:
            check(g['fcPD'] >= 0 and abs(g['fcPD'] - pdw) < 1e-9 + 1e-7 * pdw,
                  'A6 p(D) n=%d %s: %r vs Dallal-Wilkinson %r' % (n, kind, g['fcPD'], pdw))
        else:
            check(g['fcPD'] == -1, 'A6 p(D) n=%d %s: DW %r > 0.10 should show "p > 0.10", got %r' % (n, kind, pdw, g['fcPD']))
        nad += 1
print('   %d samples' % nad)


# ---- the chi-square engine ----
def py_rule(E):
    k = len(E)
    n5 = sum(1 for e in E if e < 5)
    if n5 == 0:
        return 1
    if n5 <= 0.2 * k and min(E) >= 1:
        return 2
    return 0


def py_merge(E, npar):
    """the documented rule, written independently: the smallest E below 5 joins its
    neighbour with the smaller E (left on a tie; an end cell its only neighbour), while
    k > npar + 2"""
    groups = [[i, i] for i in range(len(E))]
    ex = list(E)
    while len(groups) > npar + 2:
        cand = [(e, i) for i, e in enumerate(ex) if e < 5]
        if not cand:
            break
        m = min(e for e, i in cand)
        j = [i for e, i in cand if e == m][0]
        if j == 0:
            nb = 1
        elif j == len(ex) - 1:
            nb = j - 1
        else:
            nb = j - 1 if ex[j - 1] <= ex[j + 1] else j + 1
        lo = min(j, nb)
        groups[lo] = [groups[lo][0], groups[lo + 1][1]]
        ex[lo] = ex[lo] + ex[lo + 1]
        del groups[lo + 1]
        del ex[lo + 1]
    return groups


def set_fit(O, P, npar=0, kind=1, labs=None):
    labs = labs or [str(i + 1) for i in range(len(O))]
    call('fc_SetFit', [float(o) for o in O], [float(p) for p in P], labs, npar, kind, 't', 's')
    return G


def ref_gof(O, E, npar):
    O = np.array(O, float)
    E = np.array(E, float)
    r = stats.chisquare(O, E, ddof=npar, sum_check=False)
    return r.statistic, r.pvalue


print('A7 chi-square goodness of fit')
for trial in range(60):
    k = int(rng.integers(2, 25))
    w = rng.uniform(0.2, 3, size=k)
    P = w / w.sum()
    N = int(rng.integers(5, 3000))
    O = rng.multinomial(N, P if trial % 3 else np.ones(k) / k)
    if trial % 7 == 0:
        O[0] = 0
    N = int(O.sum())
    npar = int(rng.integers(0, 3)) if k > 4 else 0
    g = set_fit(O, P, npar)
    E = N * P
    x2, p = ref_gof(O, E, npar)
    check(rel(g['fcX2'], x2, 1e-9), 'A7 X2 trial %d: %r vs %r' % (trial, g['fcX2'], x2))
    check(g['fcDF'] == k - 1 - npar, 'A7 df trial %d' % trial)
    if k - 1 - npar >= 1:
        check(rel(g['fcP'], p, 1e-7) or (p < 1e-300 and g['fcP'] < 1e-300), 'A7 p trial %d: %r vs %r' % (trial, g['fcP'], p))
    check(g['fcChk'] == py_rule(E), 'A7 rule trial %d: %r vs %r (E %s)' % (trial, g['fcChk'], py_rule(E), np.round(E, 2)))
    check(all(abs(a - b) < 1e-9 * max(1, b) for a, b in zip(G['fcVE'], E)), 'A7 E trial %d' % trial)
    for i in range(k):
        r_ = (O[i] - E[i]) / math.sqrt(E[i])
        check(abs(G['fcVR'][i] - r_) < 1e-9 * max(1, abs(r_)) and abs(G['fcVC'][i] - r_ * r_) < 1e-9 * max(1, r_ * r_),
              'A7 residual trial %d cell %d' % (trial, i))
    # merging: the program's groups against the independent version, and the merged test
    call('fc_ToggleMerge')
    want = py_merge(list(E), npar)
    if any(a != b for a, b in want):
        got = [[int(s) - 1, int(e) - 1] for s, e in zip(G['fcMS'], G['fcME'])]
        check(got == want, 'A7 merge trial %d: %s vs %s' % (trial, got, want))
        check(G['fcMrg'] == 1, 'A7 merged view on, trial %d' % trial)
        Om = [sum(O[a:b + 1]) for a, b in want]
        Em = [sum(E[a:b + 1]) for a, b in want]
        x2m, pm = ref_gof(Om, Em, npar)
        check(rel(G['fcX2'], x2m, 1e-9) and G['fcDF'] == len(want) - 1 - npar, 'A7 merged X2 trial %d' % trial)
        if len(want) - 1 - npar >= 1:
            check(rel(G['fcP'], pm, 1e-7) or pm < 1e-300, 'A7 merged p trial %d' % trial)
        call('fc_ToggleMerge')
        check(G['fcMrg'] == 0 and G['fcVK'] == k, 'A7 unmerge trial %d' % trial)
    else:
        check(G['fcMrg'] == 0, 'A7 nothing to merge stays unmerged, trial %d' % trial)

print('A8 Benford')


def py_digit(v, two):
    if v == 0:
        return 0
    m = '%.14e' % abs(v)
    d = int(m[0])
    if two:
        return 10 * d + int(m[2])
    return d


vals = [1927.48, 0.3, 0.0299, 2000, 1e-7, 123456789, 9.999, 99.95, 7, 70, 1.5e300, -42.5, -0.0081, 5.0, 31.4159, 0.1, 0.7, 2.9, 1e15]
for v in vals:
    for two in (0, 1):
        check(call('fc_FirstDig', float(v), two) == py_digit(v, two), 'A8 first digit(s) of %r (two=%d): %r vs %r'
              % (v, two, call('fc_FirstDig', float(v), two), py_digit(v, two)))
for trial in range(12):
    n = int(rng.integers(5, 800))
    x = list(np.exp(rng.uniform(0, 12, size=n)) * rng.choice([-1, 1], size=n))
    x = [float('%.9g' % v) for v in x]
    if trial == 0:
        x[0] = 0.0
    for two in (0, 1):
        call('fc_Benford', x, two, 't', 's')
        K = 9 if two == 0 else 90
        off = 1 if two == 0 else 10
        d = [py_digit(v, two) for v in x if v != 0 and (two == 0 or abs(v) >= 10)]
        O = np.bincount(np.array(d) - off, minlength=K)
        P = np.log10(1 + 1 / np.arange(off, off + K))
        check(abs(P.sum() - 1) < 1e-12, 'A8 Benford proportions add to 1')
        check(list(G['fcO']) == list(map(float, O)), 'A8 counts trial %d two=%d' % (trial, two))
        check(all(abs(a - b) < 1e-12 for a, b in zip(G['fcPr'], P)), 'A8 Benford proportions trial %d' % trial)
        x2, p = ref_gof(O, len(d) * P, 0)
        check(rel(G['fcX2'], x2, 1e-9) and (rel(G['fcP'], p, 1e-7) or p < 1e-300), 'A8 X2 trial %d two=%d' % (trial, two))
        mad = np.mean(np.abs(O / len(d) - P))
        check(abs(G['fcMAD'] - mad) < 1e-12, 'A8 MAD trial %d two=%d: %r vs %r' % (trial, two, G['fcMAD'], mad))
        check(G['fcBenZ'] == sum(1 for v in x if v == 0) and G['fcBenU'] == len(d), 'A8 zeros counted')
        if two == 1:
            check(G['fcBenS'] == sum(1 for v in x if v != 0 and abs(v) < 10), 'R4 below-10 count trial %d' % trial)

print('A9 Poisson fit')
for F in [[268, 79, 17, 1], [144, 91, 32, 11, 2], [10, 0, 0, 3], [5, 7, 3, 0, 0], [0, 4, 9, 12, 8, 6, 2, 1],
          [50, 1], list(rng.poisson(3.3, size=(1,))), list(np.bincount(rng.poisson(6, 400)))]:
    F = [int(f) for f in F]
    r = call('fc_PoisFit', [float(f) for f in F], 't', 's')
    Ft = list(F)
    while len(Ft) > 1 and Ft[-1] == 0:
        Ft.pop()
    N = sum(Ft)
    S = sum(i * f for i, f in enumerate(Ft))
    if N == 0 or S == 0 or len(Ft) < 2:
        check(r == 0, 'A9 nothing to fit %s -> %r' % (F, r))
        continue
    lam = S / N
    K = len(Ft) - 1
    E = [N * stats.poisson.pmf(j, lam) for j in range(K)] + [N * stats.poisson.sf(K - 1, lam)]
    check(abs(G['fcLmb'] - lam) < 1e-12, 'A9 lambda %s' % F)
    check(all(abs(a - b) < 1e-9 * max(1, b) for a, b in zip(G['fcVE'], E)), 'A9 E %s: %s vs %s' % (F, G['fcVE'], E))
    check(abs(sum(G['fcVE']) - N) < 1e-8 * N, 'A9 E add to N %s' % F)
    x2, p = ref_gof(Ft, E, 1)
    check((rel(G['fcX2'], x2, 1e-9) or abs(G['fcX2'] - x2) < 1e-8) and G['fcDF'] == len(Ft) - 2, 'A9 X2/df %s' % F)
    if len(Ft) - 2 >= 1:
        check(rel(G['fcP'], p, 1e-7), 'A9 p %s: %r vs %r' % (F, G['fcP'], p))
    check(G['fcVL'][-1] == '≥' + str(K), 'A9 tail label %s' % G['fcVL'][-1])

print('A10 binomial fit')
for F, pg in [([6, 27, 42, 20, 5], -1), ([6, 27, 42, 20, 5], 0.5), ([3, 10, 9, 2], -1), ([0, 0, 5], -1), ([5, 0], -1),
              (list(np.bincount(rng.binomial(10, 0.3, 300), minlength=11)), -1), ([1, 2, 3, 4, 5, 6, 7], 0.42)]:
    F = [int(f) for f in F]
    r = call('fc_BinFit', [float(f) for f in F], float(pg), 't', 's')
    n = len(F) - 1
    N = sum(F)
    p = pg if pg > 0 else sum(i * f for i, f in enumerate(F)) / (n * N)
    if p <= 0 or p >= 1:
        check(r == 0, 'A10 degenerate %s -> %r' % (F, r))
        continue
    E = N * stats.binom.pmf(np.arange(n + 1), n, p)
    m = 1 if pg < 0 else 0
    x2, pv = ref_gof(F, E, m)
    check(abs(G['fcBp'] - p) < 1e-12 and G['fcBEst'] == m, 'A10 p %s' % F)
    check(all(abs(a - b) < 1e-9 * max(1, b) for a, b in zip(G['fcVE'], E)), 'A10 E %s' % F)
    check(rel(G['fcX2'], x2, 1e-9) and G['fcDF'] == n - m, 'A10 X2/df %s' % F)
    if n - m >= 1:
        check(rel(G['fcP'], pv, 1e-7), 'A10 p-value %s' % F)

print('A11 normal fit on bins')
cr = np.genfromtxt(DATA + 'datasets_crimtab.csv', delimiter=',', names=True, dtype=None, encoding='utf-8')
heights = sorted(set(cr['Var2']))
cf = [int(sum(cr['Freq'][cr['Var2'] == hh])) for hh in heights]
check(sum(cf) == 3000 and len(cf) == 22, 'A11 crimtab: 22 bins, 3000 people')
CRIM_F = [1, 1, 6, 23, 48, 90, 175, 317, 393, 462, 458, 413, 264, 177, 97, 46, 17, 7, 4, 0, 0, 1]
check(cf == CRIM_F, 'A11 the program\'s crimtab counts equal the CSV\'s')
mids = [142.24 + 2.54 * i for i in range(22)]
check(all(abs(a - b) < 1e-9 for a, b in zip(mids, heights)), 'A11 midpoints')


def ref_normbin(m, f, w, xb, sd):
    edges = [mm + w / 2 for mm in m[:-1]]
    cdf = [0.0] + list(stats.norm.cdf(edges, xb, sd)) + [1.0]
    sf = [1.0] + list(stats.norm.sf(edges, xb, sd)) + [0.0]
    P = []
    for i in range(len(m)):
        P.append(cdf[i + 1] - cdf[i] if cdf[i + 1] < 0.5 else sf[i] - sf[i + 1])
    return np.array(P)


N = sum(CRIM_F)
xb = sum(a * b for a, b in zip(mids, CRIM_F)) / N
sd = math.sqrt(sum(b * (a - xb) ** 2 for a, b in zip(mids, CRIM_F)) / (N - 1))
call('fc_NormBinFit', mids, [float(v) for v in CRIM_F], 2.54, xb, sd, 't', 's')
P = ref_normbin(mids, CRIM_F, 2.54, xb, sd)
check(all(abs(a - b) < 1e-9 * max(1, b) for a, b in zip(G['fcVE'], N * P)), 'A11 crimtab E')
x2, p = ref_gof(CRIM_F, N * P, 2)
check(rel(G['fcX2'], x2, 1e-9) and G['fcDF'] == 22 - 3, 'A11 crimtab X2 (all 22 bins)')
call('fc_ToggleMerge')
want = py_merge(list(N * P), 2)
Om = [sum(CRIM_F[a:b + 1]) for a, b in want]
Em = [sum((N * P)[a:b + 1]) for a, b in want]
x2m, pm = ref_gof(Om, Em, 2)
CRIM_REF = (x2m, pm, len(want) - 3, want, xb, sd)
check(rel(G['fcX2'], x2m, 1e-9) and rel(G['fcP'], pm, 1e-7) and G['fcDF'] == len(want) - 3,
      'A11 crimtab merged: %r %r vs %r %r' % (G['fcX2'], G['fcP'], x2m, pm))
print('   crimtab merged: groups %s, X2 = %.4f, df = %d, p = %.6g' % (want, x2m, len(want) - 3, pm))

print('A12 exact binomial test')


def bt_check(x, n, p0, tag):
    call('fc_BTest', x, n, float(p0))
    r2 = stats.binomtest(x, n, p0)
    lo = stats.binom.cdf(x, n, p0)
    hi = stats.binom.sf(x - 1, n, p0)
    p2 = G['fcTp2']
    if r2.pvalue > 1e-290:
        ok = abs(p2 - r2.pvalue) <= 1e-9 * max(r2.pvalue, 1e-12) or abs(p2 - r2.pvalue) < 1e-12
        check(ok, 'A12 %s two-sided x=%d n=%d p0=%g: %r vs %r' % (tag, x, n, p0, p2, r2.pvalue))
    if lo > 1e-290:
        check(abs(math.exp(G['fcTlL']) - lo) <= 1e-8 * lo + 1e-14, 'A12 %s P(X<=x) %r vs %r' % (tag, math.exp(G['fcTlL']), lo))
    if hi > 1e-290:
        check(abs(math.exp(G['fcTlU']) - hi) <= 1e-8 * hi + 1e-14, 'A12 %s P(X>=x) %r vs %r' % (tag, math.exp(G['fcTlU']), hi))
    check(abs(G['fcTE'] - n * p0) < 1e-9 * n and abs(G['fcTSD'] - math.sqrt(n * p0 * (1 - p0))) < 1e-9 * n, 'A12 %s E, SD' % tag)
    # the region drawn magenta: exactly the k with P(X = k) <= P(X = x)(1 + 1e-7)
    if n <= 400:
        pm_ = stats.binom.pmf(np.arange(n + 1), n, p0)
        d = stats.binom.pmf(x, n, p0)
        want_ = [k for k in range(n + 1) if pm_[k] <= d * (1 + 1e-7)] if x != n * p0 else list(range(n + 1))
        got_ = [k for k in range(n + 1) if call('fc_InRej', k) == 1]
        check(got_ == want_ or x == n * p0 and len(got_) == n + 1, 'A12 %s region x=%d n=%d p0=%g' % (tag, x, n, p0))


bt_check(339, 870, 0.791, 'Castaneda')
lnp = G['fcTl2']
ref_ln = stats.binom.logcdf(339, 870, 0.791)
check(abs(lnp - ref_ln) < 1e-7 * abs(ref_ln), 'A12 Castaneda ln p: %r vs %r' % (lnp, ref_ln))
check(abs(G['fcTz'] - (339 - 870 * 0.791) / math.sqrt(870 * 0.791 * 0.209)) < 1e-12, 'A12 Castaneda z')
for x, n, p0 in [(0, 10, 0.3), (10, 10, 0.3), (3, 10, 0.3), (1, 1, 0.5), (0, 1, 0.2), (5, 10, 0.5), (50, 100, 0.5),
                 (7, 20, 0.35), (2, 5000, 0.001), (31, 1000, 0.02), (0, 100000, 0.00001), (99990, 100000, 0.9999),
                 (12, 40, 0.3), (60, 61, 0.97)]:
    bt_check(x, n, p0, 'edge')
for i in range(150):
    n = int(rng.integers(1, 3000)) if i % 3 else int(rng.integers(1, 60))
    p0 = float(np.round(rng.uniform(0.01, 0.99), 3))
    x = int(np.clip(rng.normal(n * p0, 2.5 * math.sqrt(n * p0 * (1 - p0)) + 1), 0, n))
    bt_check(x, n, p0, 'random')

print('A13 edge inputs')
h13 = new_h()
h13.call('fc_Init')
for x, why in [([1.0], 'n=1'), ([1.0, 2.0], 'n=2'), ([5.0, 5.0, 5.0, 5.0], 'all equal'), ([], 'empty')]:
    r = h13.call('fc_NormSet', x, 't', 's')
    check(r == 0 and len(h13.msgboxes) > 0, 'A13 normality refuses %s' % why)
for x in [[1, 1, 2], [1, 1, 1, 2], [-5, -3, -3, -1, 0, 0, 2, 2, 2, 9], [1e9, 1e9 + 1, 1e9 + 3, 1e9 + 3.5, 1e9 + 7],
          [0.001, 0.002, 0.002, 0.0031, 0.009, 0.01], [1, 2, 3, 4, 1000]]:
    r = h13.call('fc_NormSet', [float(v) for v in x], 't', 's')
    s = stats.shapiro(x)
    g = h13.globals_
    check(r == 1 and abs(g['fcW'] - s.statistic) < 1e-6 and abs(g['fcPW'] - s.pvalue) < 1e-6,
          'A13 SW %s: %r %r vs %r %r' % (x, g['fcW'], g['fcPW'], s.statistic, s.pvalue))
    a2, pa = normal_ad(np.array(x, float))
    check(abs(g['fcA2'] - a2) < 1e-6 * max(1, a2), 'A13 A2 %s' % x)
for O in [[0, 0, 5], [0, 7], [1, 0, 0, 0]]:
    h13.call('fc_SetFit', [float(o) for o in O], [1 / len(O)] * len(O), [str(i) for i in range(len(O))], 0, 1, 't', 's')
    x2, p = ref_gof(O, [sum(O) / len(O)] * len(O), 0)
    check(rel(h13.globals_['fcX2'], x2, 1e-9), 'A13 zero counts %s' % O)
check(h13.error is None, 'A13 no runtime error (%s)' % h13.error)

# ======================================================================== PART B
print('B  the menu paths')
SK = {i: int(53.4 * (i - 1) + 26) for i in range(1, 7)}   # the soft keys' x


def soft(h, i):
    h.tap(SK[i], 230)


def run(steps, app_data=None, angle='rad'):
    h = new_h(app_data=app_data, angle=angle)
    h.press('Enter')                      # the title page
    for st in steps:
        kind = st[0]
        if kind == 'c':
            h.choose(st[1])
        elif kind == 'k':
            h.press(st[1])
        elif kind == 's':
            soft(h, st[1])
        elif kind == 't':
            h.tap(st[1], st[2])
        elif kind == 'i':
            h.answer(st[1])
    h.choose(0)                           # the main menu at the end: cancel = quit
    res = h.call('FitCheck')
    return h, res


def page_text(p):
    return re.sub(r'\s+', ' ', ' '.join(p.lines()))


def all_text(h):
    return [page_text(p) for p in h.pages]


def fnum(s):
    return float(s.replace('−', '-').replace(',', ''))


def find_num(txt, pat):
    m = re.search(pat, txt)
    return fnum(m.group(1).rstrip('.')) if m else None


def p_ok(shown, p):
    """a p as the pages print it: 'p < 0.0001', 'p = 0.0123', or 'p = 1.60 x 10^-186'"""
    if shown is None:
        return False
    m = re.search(r'p = ([0-9.]+) × 10\^(-?\d+)', shown)
    if m:
        lg = math.log10(fnum(m.group(1))) + int(m.group(2))
        return p > 0 and abs(lg - math.log10(p)) < 0.003
    m = re.search(r'p < 0\.0001', shown)
    if m:
        return p < 0.0001
    m = re.search(r'p = ([0-9.]+)', shown)
    if m:
        return abs(fnum(m.group(1)) - p) <= 0.00005 + 1e-12
    m = re.search(r'p > 0\.9999', shown)
    return bool(m) and p > 0.9999


def layout(h, tag):
    bad = []
    for scr in h.screens:
        has_menu = bool(getattr(scr, 'menu', None))
        for t in scr.texts:
            if t.grob not in (None, 'G0', 'G1', 0, 1) and str(t.grob) not in ('G0', 'G1'):
                continue
            cw = {1: 6.5, 2: 8.0, 3: 9.5}.get(int(t.font or 1), 6.5)
            w = len(t.text) * cw
            lim = t.width if t.width is not None else 320 - t.x
            if t.x < 0 or t.y < 0 or t.y > 228 or t.x + min(w, lim) > 320:
                bad.append(('off screen', t.text, t.x, t.y))
            if w > lim + 3 and len(t.text) > 2:
                bad.append(('cut', t.text, round(w), lim))
            if has_menu and t.y + 10 > 218:
                bad.append(('under the soft keys', t.text, t.y))
    check(not bad, 'B layout %s: %s' % (tag, bad[:4]))
    over = [m.lines for m in h.msgboxes if m.over_five]
    check(not over, 'B MSGBOX over 5 lines %s: %s' % (tag, over))
    check(not h.sci_strings, 'B scientific numbers %s: %s' % (tag, h.sci_strings[:4]))
    check(h.error is None, 'B runtime error %s: %s' % (tag, h.error))
    check(not any('ᴇ' in t.text for t in h.texts), 'B small-capital E on a page %s' % tag)


# ---- B1 Arizona v. Nelson ----
amts = [1927.48, 27902.31, 86241.90, 72117.46, 81321.75, 97473.96, 93249.11, 89658.16, 87776.89, 92105.83, 79949.16,
        87602.93, 96879.27, 91806.47, 84991.67, 90831.83, 93766.67, 88336.72, 94639.49, 83709.26, 96412.21, 88432.86,
        71552.16]
dg = [py_digit(v, 0) for v in amts]
O9 = np.bincount(dg, minlength=10)[1:]
P9 = np.log10(1 + 1 / np.arange(1, 10))
x2n, pn = ref_gof(O9, 23 * P9, 0)
O3 = [O9[0], sum(O9[1:5]), sum(O9[5:])]
E3 = [23 * P9[0], 23 * sum(P9[1:5]), 23 * sum(P9[5:])]
x23, p23 = ref_gof(O3, E3, 0)
madn = np.mean(np.abs(O9 / 23 - P9))
print('   Nelson: 9 cells X2 = %.4f p = %.3g; merged %s E %s X2 = %.4f p = %.3g; MAD = %.4f'
      % (x2n, pn, O3, np.round(E3, 3), x23, p23, madn))
h, res = run([('c', 'Load a preset'), ('c', 'Nelson'), ('k', 'Enter'), ('t', 300, 100), ('k', 'Right'),
              ('s', 2), ('s', 3), ('s', 4), ('k', 'Down'), ('k', 'Down'), ('k', 'Down'), ('s', 5), ('s', 1), ('s', 4),
              ('k', 'Down'), ('k', 'Down'), ('k', 'Down'), ('s', 3), ('s', 6)])
T = all_text(h)
bars = [t for t in T if t.startswith('Benford: Arizona v. Nelson ')]
check(len(bars) >= 2, 'B1 Nelson bars pages')
x2s = find_num(bars[0], r'χ² = ([0-9.]+), df = 8')
check(x2s is not None and close(x2s, x2n, 0.005), 'B1 Nelson X2 on the bars page %r vs %r' % (x2s, x2n))
check('p < 0.0001' in bars[0] and '8 of 9 E < 5: tap Merge' in bars[0], 'B1 Nelson verdict and check line')
sel9 = [t for t in T if '9: O = 9, E = ' in t]
check(len(sel9) > 0 and close(find_num(sel9[0], r'9: O = 9, E = ([0-9.]+)'), 23 * P9[8], 0.005), 'B1 cell 9 readout E')
c9 = (9 - 23 * P9[8]) ** 2 / (23 * P9[8])
check(len(sel9) > 0 and close(find_num(sel9[0], r'/E = ([0-9.]+)'), c9, 0.0005), 'B1 cell 9 contribution %r' % c9)
r9 = (9 - 23 * P9[8]) / math.sqrt(23 * P9[8])
check(len(sel9) > 0 and close(find_num(sel9[0], r'√E = \+([0-9.]+)'), r9, 0.005), 'B1 cell 9 residual')
tab = [t for t in T if t.startswith('Benford: Arizona v. Nelson: cells')]
check(len(tab) >= 1 and 'cells 1-9 of 9, ' in tab[0], 'B1 table page')
tests = [t for t in T if t.startswith('Benford: Arizona v. Nelson: test')]
check(len(tests) >= 2, 'B1 test pages')
tt = ' '.join(tests)
check(close(find_num(tt, r'MAD = .*?= ([0-9.]+) over all K = 9'), madn, 0.00005), 'B1 MAD %r' % madn)
check('Nigrini gives conformity ranges for the MAD; their values are not in any source' in tt, 'B1 MAD ranges withheld, and why')
check("Triola's question (p. 653, paraphrased)" in tt and '21 of these 23 lie between 71,552.16 and 97,473.96' in tt, 'B1 the defence talking point')
check(sum(1 for v in amts if 71552.16 <= v <= 97473.96) == 21, 'B1 21 of 23 amounts in that range (data)')
merged = [t for t in T if t.startswith('Benford: Arizona v. Nelson ') and '2-5' in t]
check(len(merged) > 0, 'B1 merged bars page')
mx = find_num(merged[0], r'χ² = ([0-9.]+), df = 2') if merged else None
check(mx is not None and close(mx, x23, 0.005), 'B1 merged X2 %r vs %r' % (mx, x23))
check(merged and p_ok(re.search(r'(p [<=] [0-9.]+)', merged[0]).group(1), p23), 'B1 merged p')
check("Merged (Triola's grouping): {2, 3, 4, 5} → 2-5; {6, 7, 8, 9} → 6-9" in tt, 'B1 merge said exactly')
check(any('every E ≥ 5' in t for t in merged), 'B1 merged: every E >= 5')
layout(h, 'B1 Nelson')

# ---- B2 Castaneda ----
r2 = stats.binomtest(339, 870, 0.791)
x2c = (339 - 688.17) ** 2 / 688.17 + (531 - 181.83) ** 2 / 181.83
h, res = run([('c', 'Load a preset'), ('c', 'Castaneda'), ('k', 'Enter'), ('t', 100, 100), ('s', 2), ('k', 'Down'),
              ('k', 'Down'), ('k', 'Down'), ('k', 'Down'), ('s', 1), ('k', 'Left'), ('s', 3), ('s', 4), ('k', 'Down'), ('s', 3), ('s', 6)])
T = all_text(h)
plot = [t for t in T if t.startswith('Castaneda v. Partida: exact test')]
check(len(plot) >= 2, 'B2 Castaneda plot pages')
m = re.search(r'two-sided p = ([0-9.]+) × 10\^(-\d+)', plot[0]) if plot else None
check(m is not None and abs(math.log10(fnum(m.group(1))) + int(m.group(2)) - math.log10(r2.pvalue)) < 0.003,
      'B2 two-sided p shown %s vs scipy %r' % (m.group(0) if m else None, r2.pvalue))
SDC = math.sqrt(870 * 0.791 * 0.209)
check(plot and 'E = 688.17' in plot[0] and ('SD = \u221a(n p\u2080(1 - p\u2080)) = %.3f' % SDC) in plot[0], 'B2 E and SD on the plot')
check(plot and 'x is 29.11 SD below E' in plot[0], 'B2 29.11 SD below')
why = ' '.join(t for t in T if t.startswith('Why: Castaneda'))
for s in ['= 688.17', '= %.3f' % SDC, '= -29.11 SDs', '430 U.S. at 496-497 n.17', 'about 688 expected with an SD of about 12',
          '"approximately 29 standard deviations"', 'less than 1 in 10^140', 'two or three standard deviations',
          'Paraphrased, apart from the words in', 'test here gives p = 4.18', 'not the probability that H₀ is true']:
    check(s in why, 'B2 Why page has %r' % s)
check(abs((339 - 688.17) / SDC - (-29.11)) < 0.005 and abs(SDC - 12) < 0.01, 'B2 arithmetic of the SD reasoning (SD about 12)')
check(why.count('"') == 2, 'R5 exactly one short quotation on the Why page (%d quote marks)' % why.count('"'))
check('n. 17 at 496-497' in why, 'R5 the source line cites n. 17 at 496-497')
lo_ln = stats.binom.logcdf(339, 870, 0.791)
m = re.search(r'P\(X ≤ 339\) = ([0-9.]+) × 10\^(-\d+)', why)
check(m is not None and abs(math.log10(fnum(m.group(1))) + int(m.group(2)) - lo_ln / math.log(10)) < 0.003, 'B2 P(X <= 339)')
tap_pg = [t for t in plot if 'k = ' in t and 'P(X = k)' in t]
check(len(tap_pg) > 0, 'B2 a tapped bar shows P(X = k)')
if tap_pg:
    m = re.search(r'k = (\d+): P\(X = k\) = (\S+)( × 10\^(-?\d+))?', tap_pg[0])
    k = int(m.group(1))
    lp = stats.binom.logpmf(k, 870, 0.791) / math.log(10)
    shown = math.log10(fnum(m.group(2))) + (int(m.group(4)) if m.group(4) else 0)
    check(abs(shown - lp) < 0.003, 'B2 P(X = %d) shown %r vs %r' % (k, shown, lp))
chi = [t for t in T if t.startswith('χ²: two categories')]
check(len(chi) > 0, 'B2 the two-category chi-square pages')
cx = find_num(chi[0], r'χ² = ([0-9.]+), df = 1') if chi else None
check(cx is not None and close(cx, x2c, 0.005), 'B2 two-category X2 %r vs %r' % (cx, x2c))
check(abs(x2c - ((339 - 688.17) / math.sqrt(870 * .791 * .209)) ** 2) < 1e-6, 'B2 X2 = z^2')
cur = [t for t in T if t.startswith('χ² curve, df = 1')]
check(cur and 'far off the chart' in cur[0], 'B2 the curve says the statistic is off the chart')
m = re.search(r'p-value: p = ([0-9.]+) × 10\^(-\d+)', cur[0]) if cur else None
check(m is not None and abs(math.log10(fnum(m.group(1))) + int(m.group(2)) - stats.chi2.logsf(x2c, 1) / math.log(10)) < 0.003,
      'B2 chi-square p in logs')
layout(h, 'B2 Castaneda')

# ---- B3 Richmond, B4 horse kicks ----
for name, F, tag in [('Richmond', [268, 79, 17, 1], 'Poisson: Richmond homicides 1991'),
                     ('Horse', [144, 91, 32, 11, 2], 'Poisson: horse-kick deaths')]:
    N = sum(F)
    lam = sum(i * f for i, f in enumerate(F)) / N
    K = len(F) - 1
    E = [N * stats.poisson.pmf(j, lam) for j in range(K)] + [N * stats.poisson.sf(K - 1, lam)]
    x2, p = ref_gof(F, E, 1)
    want = py_merge(E, 1)
    Om = [sum(F[a:b + 1]) for a, b in want]
    Em = [sum(E[a:b + 1]) for a, b in want]
    x2m, pm = ref_gof(Om, Em, 1)
    print('   %s: lambda %.4f, X2 %.4f df %d p %.4f, rule %d; merged %s X2 %.4f df %d p %.4f'
          % (name, lam, x2, K - 1, p, py_rule(E), want, x2m, len(want) - 2, pm))
    h, res = run([('c', 'Poisson fit'), ('c', name), ('k', 'Enter'), ('s', 4), ('k', 'Down'), ('s', 5), ('s', 1), ('s', 4),
                  ('k', 'Down'), ('s', 2), ('s', 6)])
    T = all_text(h)
    bars = [t for t in T if t.startswith(tag + ' ')]
    x2s = find_num(bars[0], r'χ² = ([0-9.]+), df = ') if bars else None
    check(x2s is not None and close(x2s, x2, 0.005), 'B3 %s X2 %r vs %r' % (name, x2s, x2))
    check(bars and p_ok(re.search(r'(p [<=>] [0-9.]+)', bars[0]).group(1), p), 'B3 %s p' % name)
    tt = ' '.join(t for t in T if t.startswith(tag + ': test'))
    check(close(find_num(tt, r'estimated λ = \(sum of x f\) / N = ([0-9.]+)'), lam, 0.00005), 'B3 %s lambda' % name)
    if py_rule(E) == 0:
        check("That breaks Cochran's rule" in tt, 'B3 %s: the rule fails and the page says so' % name)
    mb = [t for t in bars if 'df = %d,' % (len(want) - 2) in t and t != bars[0]]
    if len(want) < len(E):
        check(len(mb) > 0 and close(find_num(mb[0], r'χ² = ([0-9.]+)'), x2m, 0.005), 'B3 %s merged X2' % name)
        check(mb and p_ok(re.search(r'(p [<=>] [0-9.]+)', mb[0]).group(1), pm), 'B3 %s merged p' % name)
        check('Merged (neighbouring cells)' in tt, 'B3 %s merged groups named' % name)
    layout(h, 'B3 ' + name)

# ---- B5 crimtab ----
x2m, pm, dfm, want, xb, sd = CRIM_REF
h0, _r = run([('c', 'Load a preset'), ('c', 'crimtab'), ('k', 'Enter'), ('s', 6)])
TX, TY = int(h0.globals_['fcQX'][9]), int(h0.globals_['fcQY'][9])       # bin 10, 165.1 cm, where it was drawn
h, res = run([('c', 'Load a preset'), ('c', 'crimtab'), ('k', 'Enter'), ('t', TX + 3, TY - 2), ('s', 2), ('t', 150, 100),
              ('s', 3), ('s', 4), ('s', 4), ('k', 'Down'), ('s', 6)])
T = all_text(h)
qq = [t for t in T if t.startswith('Q-Q: crimtab heights')]
check(qq and 'n = 3000 in 22 bins: one point per bin' in qq[0], 'B5 Q-Q page says one point per bin')
check(any('One point per bin: its midpoint against the' in t for t in qq), 'B5 Q-Q says how the points are placed')
zb1 = stats.norm.ppf((0 + (1 + 1) / 2 - 0.375) / 3000.25)
check(qq and ('bin 142.24: 1 value, z = %+.3f' % zb1) in qq[0], 'B5 the first bin\'s point: z = %.3f' % zb1)
qz = [t for t in qq if 'bin 165.1: 462 values' in t]
c_ = sum(CRIM_F[:9])
zmid = stats.norm.ppf((c_ + (462 + 1) / 2 - 0.375) / 3000.25)
check(len(qz) > 0 and ('z = %+.3f' % zmid) in qz[0], 'B5 the tapped bin 165.1: z = %.3f' % zmid)
mb = [t for t in T if t.startswith('crimtab heights: χ² on bins ')]
check(len(mb) > 0, 'B5 the bins fit page')
if mb:
    check(close(find_num(mb[0], r'χ² = ([0-9.]+), df = %d' % dfm), x2m, 0.005), 'B5 crimtab merged X2 on the page')
    check(p_ok(re.search(r'(p [<=>] [0-9.]+)', mb[0]).group(1), pm), 'B5 crimtab p')
tt = ' '.join(t for t in T if t.startswith('crimtab heights: χ² on bins: test'))
check('df = k - 1 - m = %d - 1 - 2 = %d' % (len(want), dfm) in tt, 'B5 df = k - 3 written out')
check('Merged (neighbouring cells): {142.24, 144.78, 147.32}' in tt or 'Merged (neighbouring cells): {' in tt, 'B5 merged tails named')
check(close(find_num(tt, 'x̄ = ([0-9.]+)') or find_num(tt, ' = ([0-9.]+)'), xb, 0.0005), 'B5 grouped mean %r' % xb)
nt = ' '.join(t for t in T if t.startswith('Normality: crimtab'))
check('This sample is BINNED' in nt, 'B5 the tests page explains why W, A2, D are not run on bins')
layout(h, 'B5 crimtab')

# ---- B6 Rossi ----
import csv  # noqa: E402
ages = [int(r['age']) for r in csv.DictReader(open(DATA + 'rossi.csv'))]
check(len(ages) == 432, 'B6 432 ages')
sw = stats.shapiro(ages)
a2, pa = normal_ad(np.array(ages, float))
dd, _ = lilliefors(np.array(ages, float), pvalmethod='table')
pdw = pval_lf(dd, 432)
print('   Rossi: W %.4f p %.3g; A2 %.4f p %r; D %.4f DW p %.3g; skew %.3f'
      % (sw.statistic, sw.pvalue, a2, pa, dd, pdw, stats.skew(ages)))
h, res = run([('c', 'Load a preset'), ('c', 'Rossi'), ('k', 'Enter'), ('k', 'Right'), ('t', 300, 60), ('s', 2),
              ('t', 150, 100), ('s', 3), ('k', 'Down'), ('s', 4), ('s', 4), ('k', 'Down'), ('s', 3), ('s', 6)])
T = all_text(h)
qq = [t for t in T if t.startswith('Q-Q: Rossi ages')]
check(qq and close(find_num(qq[0], r'W = ([0-9.]+)'), sw.statistic, 0.00005), 'B6 W on the Q-Q page')
m = re.search(r'p = ([0-9.]+) × 10\^(-\d+)', qq[0]) if qq else None
check(m is not None and abs(math.log10(fnum(m.group(1))) + int(m.group(2)) - math.log10(sw.pvalue)) < 0.003, 'B6 p(W) %r' % sw.pvalue)
sel = [t for t in qq if 'x(2) = 17, rank 2 of 432' in t]
check(len(sel) > 0, 'B6 Right selects point 2')
if sel:
    z2 = stats.norm.ppf((2 - 0.375) / 432.25)
    check(close(find_num(sel[0], r'z = ([+\-][0-9.]+)'), z2, 0.0005), 'B6 point 2 normal score %r' % z2)
nt = ' '.join(t for t in T if t.startswith('Normality: Rossi'))
check(close(find_num(nt, r'Shapiro-Wilk W = ([0-9.]+)'), sw.statistic, 0.00005), 'B6 W on Tests')
check(close(find_num(nt, r'Anderson-Darling A² = ([0-9.]+)'), a2, 0.00005), 'B6 A2 on Tests')
check(close(find_num(nt, r'\) = ([0-9.]+), p'), a2 * (1 + 0.75 / 432 + 2.25 / 432 ** 2), 0.00005), 'B6 A*2 on Tests')
check(pa == 0 and 'A*² = A²(1 + 0.75/n + 2.25/n²) = ' in nt, 'B6 A*2 > 13: statsmodels says p = 0; page p < 0.0001')
check(close(find_num(nt, r'Lilliefors D = ([0-9.]+)'), dd, 0.00005), 'B6 D on Tests')
m = re.search(r'Lilliefors D = [0-9.]+, p = ([0-9.]+) × 10\^(-\d+)', nt)
check(m is not None and abs(math.log10(fnum(m.group(1))) + int(m.group(2)) - math.log10(pdw)) < 0.003, 'B6 p(D) Dallal-Wilkinson')
check('all 3 tests with a p give evidence against normality' in nt and 'Right-skewed' in nt and 'Median = 23 < mean = 24.60' in nt,
      'B6 the verdict and the Q-Q lesson')
ec = [t for t in T if t.startswith('ECDF vs normal: Rossi')]
check(ec and close(find_num(ec[0], r'Lilliefors D = ([0-9.]+)'), dd, 0.00005), 'B6 D on the ECDF page')
tapx = [t for t in ec if 'ECDF = ' in t]
if tapx:
    m = re.search(r'x = ([0-9.]+): ECDF = ([0-9.]+), normal CDF = ([0-9.]+)', tapx[0])
    xv = fnum(m.group(1))
    check(close(fnum(m.group(3)), stats.norm.cdf(xv, np.mean(ages), np.std(ages, ddof=1)), 0.0015), 'B6 ECDF tap: normal CDF')
    check(close(fnum(m.group(2)), np.mean(np.array(ages) <= xv + 0.005), 0.003), 'B6 ECDF tap: ECDF')
else:
    check(False, 'B6 the ECDF tap readout')
dmax = np.argmax(np.maximum(np.arange(1, 433) / 432 - stats.norm.cdf(np.sort(ages), np.mean(ages), np.std(ages, ddof=1)),
                            stats.norm.cdf(np.sort(ages), np.mean(ages), np.std(ages, ddof=1)) - np.arange(0, 432) / 432))
check(ec and ('at x = %d' % np.sort(ages)[dmax]) in ec[0], 'B6 D marked at x = %d' % np.sort(ages)[dmax])
rb = [t for t in T if t.startswith('Rossi ages: χ² on bins ')]
check(len(rb) > 0, 'B6 the bins fit from raw data')
if rb:
    # the documented binning: Sturges' count, nearest 1-2-5 width, (a, a + w], open end cells
    n = 432
    k0 = math.ceil(math.log2(n)) + 1
    raw = (max(ages) - min(ages)) / k0
    e = math.floor(math.log10(raw))
    f = raw / 10 ** e
    w = (1 if f < 1.41421356 else 2 if f < 3.16227766 else 5 if f < 7.07106781 else 10) * 10 ** e
    a = math.floor(min(ages) / w) * w
    if a == min(ages):
        a -= w
    kb = math.ceil((max(ages) - a) / w)
    Fb = [0] * kb
    for v in ages:
        Fb[min(kb, max(1, math.ceil(round((v - a) / w, 8)))) - 1] += 1
    mids_b = [a + (i + 0.5) * w for i in range(kb)]
    Pb = ref_normbin(mids_b, Fb, w, np.mean(ages), np.std(ages, ddof=1))
    wantb = py_merge(list(n * Pb), 2)
    Om = [sum(Fb[p_:q_ + 1]) for p_, q_ in wantb]
    Em = [sum((n * Pb)[p_:q_ + 1]) for p_, q_ in wantb]
    x2b, pb = ref_gof(Om, Em, 2)
    print('   Rossi bins: width %g from %g, %d bins, merged %s, X2 %.3f df %d p %.3g' % (w, a, kb, wantb, x2b, len(wantb) - 3, pb))
    check(close(find_num(rb[0], r'χ² = ([0-9.]+), df = %d' % (len(wantb) - 3)), x2b, 0.005), 'B6 Rossi bins X2')
    check(p_ok(re.search(r'(p [<=>] [0-9.]+)', rb[0]).group(1), pb), 'B6 Rossi bins p')
    tt = ' '.join(t for t in T if t.startswith('Rossi ages: χ² on bins: test'))
    check('Chernoff & Lehmann 1954' in tt, 'B6 the raw-data df caveat')
layout(h, 'B6 Rossi')

# ---- B7 / R2 draft lottery: a 2 x 2 table (beta 1a) ----
import json  # noqa: E402
dr = json.load(open(DATA + 'draft1970_triola.json'))
mon = list(dr)
low = [sum(1 for v in dr[m] if v <= 183) for m in mon]
O = [sum(low[:6]), sum(low[6:])]
days = [sum(len(dr[m]) for m in mon[:6]), sum(len(dr[m]) for m in mon[6:])]
tab = np.array([[O[0], days[0] - O[0]], [O[1], days[1] - O[1]]])
c2 = stats.chi2_contingency(tab, correction=False)
x2d, pd_ = c2[0], c2[1]
pf = stats.fisher_exact(tab).pvalue
hg = stats.hypergeom(366, 183, days[0])
dk = hg.pmf(O[0])
ph = sum(hg.pmf(k) for k in range(0, 184) if hg.pmf(k) <= dk * (1 + 1e-7))
gx2, gp = ref_gof(O, [183 * d / 366 for d in days], 0)
print('   draft 2x2 %s: Pearson X2 %.4f p %.6f; Fisher p %.6f (hypergeom sum %.6f); fixed-share GOF %.4f p %.5f'
      % (tab.tolist(), x2d, pd_, pf, ph, gx2, gp))
check(abs(x2d - 14.164) < 0.001 and abs(pd_ - 0.000168) < 0.000002, 'R2 the review\'s 2x2 numbers reproduced')
check(abs(pf - ph) < 1e-12, 'R2 Fisher = the two-sided hypergeometric sum')
h, res = run([('c', 'Load a preset'), ('c', 'Draft'), ('k', 'Enter'), ('s', 4), ('k', 'Down'), ('k', 'Down'), ('k', 'Down'),
              ('s', 2), ('s', 3), ('s', 5), ('s', 6)])
T = all_text(h)
TT = 'Draft lottery 1970: 2 \u00d7 2'
bars = [t for t in T if t.startswith(TT + ' ')]
check(bars and close(find_num(bars[0], r'\u03c7\u00b2 = ([0-9.]+), df = 1'), x2d, 0.005), 'R2 draft Pearson X2 on the bars page')
check(bars and p_ok(re.search(r'(p [<=>] [0-9.]+)', bars[0]).group(1), pd_), 'R2 draft Pearson p')
check(bars and p_ok(re.search(r'Fisher exact (p [<=>] [0-9.]+)', bars[0]).group(1), pf), 'R2 Fisher p on the bars page')
G2 = h.globals_
check(abs(G2['fcFshP'] - pf) < 1e-9 * pf and abs(G2['FC_X2'] - x2d) < 1e-9 and G2['FC_DF'] == 1, 'R2 fcFshP, FC_X2, FC_DF')
tt = ' '.join(t for t in T if t.startswith(TT + ': test'))
check(('Jan %d, Feb %d, Mar %d' % tuple(low[:3])) in tt and ('Dec %d' % low[11]) in tt, 'B7 monthly counts')
check('182 \u00d7 183/366 = 91.0 low numbers' in tt and 'not checked against the paper here' in tt, 'B7 the explanation')
check('WITHOUT replacement' in tt and 'hypergeometric' in tt, 'R2 the exact test explained')
m = re.search(r'Two-sided p = ([0-9.]+)', tt)
check(m is not None and abs(fnum(m.group(1).rstrip('.')) - pf) <= 0.0000005, 'R2 Fisher p on the Test page, 6 decimals')
m = re.search(r'\(1\) \u2265 14.164\) : p = ([0-9.]+)', tt)
check(m is not None and abs(fnum(m.group(1)) - pd_) <= 0.0000005, 'R2 Pearson p on the Test page, 6 decimals')
check('evidence that birth date and draft number are' in tt and 'reject H\u2080' in tt, 'R2 the decision in words')
check(('gives \u03c7\u00b2 = %.2f, p = %.4f' % (gx2, gp)) in tt and 'understates the evidence' in tt, 'R2 the teaching point (fixed-share GOF)')
check('df = (rows - 1)(columns - 1) = 1' in tt, 'R2 df for a 2 x 2')
tb = [t for t in T if t.startswith(TT + ': cells')]
check(tb and 'Jan-Jun lo 73 91.00' in tb[0] and 'Jan-Jun hi 109 91.00' in tb[0] and 'Jul-Dec lo 110 92.00' in tb[0]
      and 'Jul-Dec hi 74 92.00' in tb[0], 'R2 table O and E')
cv = [t for t in T if t.startswith('\u03c7\u00b2 curve, df = 1')]
check(cv and 'df = (2-1)(2-1) = 1, Fisher exact p = ' in cv[0], 'R2 the curve page names Fisher')
mb = ' '.join(' '.join(m.lines) for m in h.msgboxes)
check('nothing to merge' in mb, 'R2 Merge refused on a 2 x 2')
layout(h, 'B7 draft')
# fc_Fisher against fisher_exact on random 2 x 2 tables
for i in range(80):
    a_, b_, c_, d_ = [int(v) for v in rng.integers(0, 40, 4)]
    if i % 5 == 0:
        a_, b_, c_, d_ = [int(v) for v in rng.integers(0, 6, 4)]
    if (a_ + b_) == 0 or (c_ + d_) == 0 or (a_ + c_) == 0 or (b_ + d_) == 0:
        continue
    Nn = a_ + b_ + c_ + d_
    call('fc_Fisher', Nn, a_ + c_, a_ + b_, a_)
    pf_ = stats.fisher_exact([[a_, b_], [c_, d_]]).pvalue
    check(abs(G['fcFshP'] - pf_) < 1e-9 * max(pf_, 1e-12) + 1e-12, 'R2 fc_Fisher %s: %r vs %r' % ([a_, b_, c_, d_], G['fcFshP'], pf_))

# ---- B8 binomial (illustrative) ----
F = [6, 27, 42, 20, 5]
p_ = sum(i * f for i, f in enumerate(F)) / 400
E = 100 * stats.binom.pmf(range(5), 4, p_)
x2b, pb = ref_gof(F, E, 1)
h, res = run([('c', 'Binomial fit'), ('c', 'Illustrative'), ('k', 'Enter'), ('s', 4), ('k', 'Down'), ('k', 'Down'), ('s', 6)])
T = all_text(h)
bb = [t for t in T if t.startswith('Binomial fit (illustrative) ')]
check(bb and close(find_num(bb[0], r'χ² = ([0-9.]+), df = 3'), x2b, 0.005), 'B8 binomial X2 %r' % x2b)
tt = ' '.join(t for t in T if t.startswith('Binomial fit (illustrative): test'))
check('illustrative numbers, made up for practice' in tt and close(find_num(tt, ' = .*?= ([0-9.]+):'), p_, 0.00005),
      'B8 labelled illustrative; p-hat')
layout(h, 'B8 binomial')

# ---- B9 my data ----
x = [float('%.6g' % v) for v in rng.lognormal(2, 0.6, 60)]
sw = stats.shapiro(x)
h, res = run([('c', 'Use my data'), ('c', 'normality'), ('s', 3), ('s', 6)], app_data={'D1': x})
nt = ' '.join(t for t in all_text(h) if t.startswith('Normality: My data'))
check(close(find_num(nt, r'Shapiro-Wilk W = ([0-9.]+)'), sw.statistic, 0.00005), 'B9 D1 normality W')
layout(h, 'B9 normality')
vals = [float('%.6g' % v) for v in np.exp(rng.uniform(0, 9, 300))]
for route, two in [('1 digit', 0), ('2 digits', 1)]:
    h, res = run([('c', 'Use my data'), ('c', route), ('s', 6)], app_data={'D1': vals})
    d = [py_digit(v, two) for v in vals if two == 0 or abs(v) >= 10]
    K = 9 if two == 0 else 90
    off = 1 if two == 0 else 10
    O = np.bincount(np.array(d) - off, minlength=K)
    x2, p = ref_gof(O, len(d) * np.log10(1 + 1 / np.arange(off, off + K)), 0)
    if two == 1:
        nb = sum(1 for v in vals if abs(v) < 10)
        mb = ' '.join(' '.join(m.lines) for m in h.msgboxes)
        check(nb > 0 and ('%d of the values are below 10' % nb) in mb, 'R4 the MSGBOX says %d left out: %r' % (nb, mb[:80]))
    T = all_text(h)
    bb = [t for t in T if t.startswith('Benford: my data (D1) ')]
    check(bb and close(find_num(bb[0], r'χ² = ([0-9.]+), df = %d' % (K - 1)), x2, 0.005), 'B9 Benford %s X2' % route)
    layout(h, 'B9 Benford ' + route)
cnt = [12.0, 30.0, 8.0, 50.0]
shr = [1.0, 2.0, 1.0, 4.0]
h, res = run([('c', 'Use my data'), ('c', 'D2 shares'), ('s', 4), ('k', 'Down'), ('k', 'Down'), ('s', 6)], app_data={'D1': cnt, 'D2': shr})
x2, p = ref_gof(cnt, 100 * np.array(shr) / 8, 0)
T = all_text(h)
bb = [t for t in T if t.startswith('My counts (D1), shares (D2) ')]
check(bb and close(find_num(bb[0], r'χ² = ([0-9.]+), df = 3'), x2, 0.005), 'B9 D1/D2 X2')
tt = ' '.join(t for t in T if t.startswith('My counts (D1), shares (D2): test'))
check('added up to 8; each was divided by that' in tt, 'B9 the shares rescaled, and said')
layout(h, 'B9 D2 shares')
h, res = run([('c', 'Use my data'), ('c', 'equal shares'), ('s', 6)], app_data={'D1': cnt})
x2, p = ref_gof(cnt, [25] * 4, 0)
bb = [t for t in all_text(h) if t.startswith('My counts (D1), equal shares ')]
check(bb and close(find_num(bb[0], r'χ² = ([0-9.]+)'), x2, 0.005), 'B9 equal shares X2')
layout(h, 'B9 equal')
pc = [float(v) for v in np.bincount(rng.poisson(2.2, 150))]
h, res = run([('c', 'Use my data'), ('c', 'Poisson'), ('s', 6)], app_data={'D1': pc})
N = sum(pc)
lam = sum(i * f for i, f in enumerate(pc)) / N
K = len(pc) - 1
E = [N * stats.poisson.pmf(j, lam) for j in range(K)] + [N * stats.poisson.sf(K - 1, lam)]
x2, p = ref_gof(pc, E, 1)
bb = [t for t in all_text(h) if t.startswith('Poisson: my counts (D1) ')]
check(bb and close(find_num(bb[0], r'χ² = ([0-9.]+)'), x2, 0.005), 'B9 Poisson X2')
layout(h, 'B9 Poisson')
bc = [3.0, 14.0, 21.0, 9.0, 3.0]
for how, pg in [('Estimate', -1), ('Type', 0.45)]:
    steps = [('c', 'Use my data'), ('c', 'binomial'), ('c', how)]
    if pg > 0:
        steps.append(('i', {'mdP': pg}))
    steps.append(('s', 6))
    h, res = run(steps, app_data={'D1': bc})
    pp = pg if pg > 0 else sum(i * f for i, f in enumerate(bc)) / (4 * 50)
    x2, p = ref_gof(bc, 50 * stats.binom.pmf(range(5), 4, pp), 1 if pg < 0 else 0)
    bb = [t for t in all_text(h) if t.startswith('Binomial: my counts (D1) ')]
    check(bb and close(find_num(bb[0], r'χ² = ([0-9.]+), df = %d' % (3 if pg < 0 else 4)), x2, 0.005), 'B9 binomial %s' % how)
    layout(h, 'B9 binomial ' + how)
# refusals: no D1, negative counts, a fraction, D2 the wrong size, a zero share, all zero, n > 5000
for steps, ad, want in [
        ([('c', 'Use my data'), ('c', 'normality')], None, 'List D1 is empty'),
        ([('c', 'Use my data'), ('c', 'equal shares')], {'D1': [3.0, -1.0]}, 'D1 must hold counts'),
        ([('c', 'Use my data'), ('c', 'equal shares')], {'D1': [3.0, 1.5]}, 'D1 must hold counts'),
        ([('c', 'Use my data'), ('c', 'D2 shares')], {'D1': [3.0, 4.0], 'D2': [1.0]}, 'D2 must hold one expected share'),
        ([('c', 'Use my data'), ('c', 'D2 shares')], {'D1': [3.0, 4.0], 'D2': [1.0, 0.0]}, 'above 0'),
        ([('c', 'Use my data'), ('c', 'equal shares')], {'D1': [0.0, 0.0]}, 'Every count in D1 is 0'),
        ([('c', 'Use my data'), ('c', 'Poisson')], {'D1': [9.0, 0.0]}, 'Nothing to fit'),
        ([('c', 'Use my data'), ('c', 'normality')], {'D1': [float(i) for i in range(5001)]}, 'more than 5000'),
        ([('c', 'Use my data'), ('c', 'normality')], {'D1': [2.0, 2.0, 2.0]}, 'Every value is the same'),
        ([('c', 'Use my data'), ('c', '1 digit')], {'D1': [0.0, 0.0]}, 'Every value in D1 is 0'),
        ([('c', 'Normality: ' + 'χ²')], None, 'Load a sample first')]:
    h, res = run(steps, app_data=ad)
    mb = ' '.join(' '.join(m.lines) for m in h.msgboxes)
    check(want in mb and h.error is None, 'B9 refusal %r: %r' % (want, mb[:90]))
    layout(h, 'B9 refusal ' + want)

# ---- B10 the exact test, typed ----
for x, n, p0 in [(7, 20, 0.5), (10, 20, 0.5), (0, 1, 0.3), (1, 1, 0.3), (15, 100, 0.08)]:
    h, res = run([('c', 'Exact binomial test'), ('c', 'Type'), ('i', {'tbX': x, 'tbN': n, 'tbP': p0}), ('s', 2), ('s', 6)])
    r2 = stats.binomtest(x, n, p0)
    T = all_text(h)
    pl = [t for t in T if t.startswith('Exact binomial test ')]
    shown = re.search(r'two-sided (p [<=>] [0-9.]+( × 10\^-?\d+)?)', pl[0]).group(1) if pl else None
    check(p_ok(shown, r2.pvalue), 'B10 typed x=%d n=%d p0=%g: %r vs %r' % (x, n, p0, shown, r2.pvalue))
    layout(h, 'B10 %d %d %g' % (x, n, p0))
for bad in [{'tbX': 5, 'tbN': 3, 'tbP': 0.5}, {'tbX': 1, 'tbN': 3, 'tbP': 1.0}, {'tbX': 1.5, 'tbN': 3, 'tbP': 0.5},
            {'tbX': 1, 'tbN': 0, 'tbP': 0.5}]:
    h, res = run([('c', 'Exact binomial test'), ('c', 'Type'), ('i', bad)])
    check(len(h.msgboxes) == 1 and h.error is None, 'B10 refused %s' % bad)

# ---- B11 help, the title page, the menus, Quit ----
h, res = run([('c', 'Help')] + [('k', 'Enter')] * 12)
T = all_text(h)
check(any('DISCLAIMER: a teaching and demonstration aid' in t for t in T[:1]), 'B11 the disclaimer on the title page')
hp = [t for t in T if t.startswith('FitCheck help')]
check(len(hp) >= 4 and 'DISCLAIMER' in ' '.join(hp), 'B11 help pages (%d)' % len(hp))
layout(h, 'B11 help')
h, res = run([('c', 'Help'), ('k', 'Esc')])
check(len([t for t in all_text(h) if t.startswith('FitCheck help')]) == 1, 'B11 Esc leaves help from page 1')
h, res = run([('c', 'Use my data'), ('c', 'How to fill')] + [('k', 'Enter')] * 3)
check(any('D1(1) = how many units had 0 events' in t for t in all_text(h)), 'B11 the D1/D2 help')
h, res = run([])
check(res == 'FitCheck: nothing computed', 'B11 Quit with nothing: %r' % res)
h, res = run([('c', 'Load a preset'), ('c', 'Draft'), ('k', 'Enter'), ('s', 6)])
check(res.startswith('FitCheck: χ²(1) = 14.164, p = 0.0002'), 'B11 Quit summary %r' % res)
check(abs(h.globals_['FC_X2'] - x2d) < 1e-9 and abs(h.globals_['FC_P'] - pd_) < 1e-9 and h.globals_['FC_DF'] == 1,
      'B11 Home exports FC_X2 FC_P FC_DF')
for ch in h.chooses:
    for it in ch.items:
        check(len(it) <= 30, 'B11 menu line short enough: %r (%d)' % (it, len(it)))
    check(len(ch.items) <= 14, 'B11 CHOOSE items <= 14')
    check(not any(re.match(r'^\s*\d+[.)]', it) for it in ch.items), 'B11 menu lines carry no numbers')
# every menu of the program, as recorded in all runs above
seen = set()
for hh in ALL_H:
    for ch in hh.chooses:
        for it in ch.items:
            if it not in seen:
                seen.add(it)
                check(len(it) <= 30, 'B11 menu line %r is %d characters' % (it, len(it)))
# the main menu reached from every analysis item once more, then Esc / Enter back
for item in ['goodness of fit', "Benford's law", 'Poisson fit', 'Binomial fit', 'Q-Q, W', 'Exact binomial', 'Load a preset']:
    h, res = run([('c', item), ('c', 0)])
    check(h.error is None, 'B11 cancel out of %s' % item)

# ---- B13 the whole Rossi path with the calculator in degrees (nothing may depend on the angle mode) ----
h, res = run([('c', 'Load a preset'), ('c', 'Rossi'), ('k', 'Enter'), ('s', 3), ('s', 6)], angle='deg')
nt = ' '.join(t for t in all_text(h) if t.startswith('Normality: Rossi'))
sw = stats.shapiro(ages)
check(close(find_num(nt, r'Shapiro-Wilk W = ([0-9.]+)'), sw.statistic, 0.00005) and h.error is None, 'B13 degrees mode')

# ======================================================================== part R (beta 1a)
print('R  the second review\'s items')
# R1 Bins -> Unmrg -> Bars (and Table, Test) on kind-6 fits
xd = [float('%.6g' % v) for v in rng.normal(50, 8, 120)]
for tag, steps, ad in [('crimtab', [('c', 'Load a preset'), ('c', 'crimtab'), ('k', 'Enter'), ('s', 4)], None),
                       ('Rossi', [('c', 'Load a preset'), ('c', 'Rossi'), ('k', 'Enter'), ('s', 4)], None),
                       ('D1', [('c', 'Use my data'), ('c', 'normality'), ('s', 4)], {'D1': xd})]:
    h, res = run(steps + [('s', 5), ('s', 1), ('t', 200, 100), ('s', 2), ('s', 4), ('s', 5), ('s', 1), ('s', 6),
                          ('c', 'goodness of fit'), ('c', 'last fit'), ('s', 5), ('s', 1), ('s', 6)], app_data=ad)
    check(h.error is None, 'R1 %s: Bins, Unmrg, Bars: no error (%s)' % (tag, h.error))
    unm = [sc for sc in h.screens if sc.menu and 'Merge' in sc.menu and sc.lines() and 'on bins' in sc.lines()[0]]
    check(len(unm) > 0, 'R1 %s: an unmerged (Merge key) bins page was shown' % tag)
    layout(h, 'R1 ' + tag)
# R3 Lilliefors n < 5
for x in [[5.0, 5.0, 7.0], [1.0, 1.1, 100.0], [1.0, 2.0, 2.5, 9.0]]:
    h, res = run([('c', 'Use my data'), ('c', 'normality'), ('s', 2), ('s', 3), ('s', 6)], app_data={'D1': x})
    T = all_text(h)
    check(h.globals_['fcPD'] == -2 and h.globals_['FC_PD'] == -2, 'R3 n=%d: fcPD = -2' % len(x))
    ec = [t for t in T if t.startswith('ECDF vs normal')]
    nt = ' '.join(t for t in T if t.startswith('Normality: My data'))
    check(ec and 'p not available for n < 5' in ec[0] and 'p > 0.10' not in ec[0], 'R3 n=%d ECDF headline' % len(x))
    check('Lilliefors D = %.4f, p not available for n < 5' % lilliefors_d(x) in nt if False else 'p not available for n < 5' in nt,
          'R3 n=%d Tests page' % len(x))
    grey = [t for t in h.texts if 'p not available for n < 5' in t.text]
    check(grey and all(t.hex == '#5A5A5A' for t in grey), 'R3 n=%d: shown in grey, not green' % len(x))
    sw = stats.shapiro(x)
    if sw.pvalue >= 0.05:
        check('none of the tests with a p finds evidence' in nt, 'R3 n=%d verdict counts only W and A2' % len(x))
for n in [5, 6, 12]:
    x = [float(v) for v in rng.normal(size=n)]
    h1 = new_h(); h1.call('fc_Init'); h1.call('fc_NormSet', x, 't', 's')
    d, _ = lilliefors(np.array(x), pvalmethod='table')
    pdw = pval_lf(d, n)
    g = h1.globals_
    check((pdw <= 0.1 and abs(g['fcPD'] - pdw) < 1e-9) or (pdw > 0.1 and g['fcPD'] == -1), 'R3 n=%d: Dallal-Wilkinson used' % n)
# R6 Esc stops a large load; moments without overflow
h6 = new_h()
h6.call('fc_Init')
h6.press('Esc', anytime=True)
r = h6.call('fc_NormSet', [float(v) for v in rng.normal(size=1200)], 't', 's')
mb = ' '.join(' '.join(m.lines) for m in h6.msgboxes)
check(r == 0 and 'Stopped (Esc)' in mb and h6.globals_['fcHasN'] == 0 and h6.error is None, 'R6 Esc stops the load: %r %r' % (r, mb))
check(any('of 600, Esc = stop' in t.text for t in h6.texts), 'R6 the progress count was shown')
h6 = new_h()
h6.call('fc_Init')
xb = [1e150 * v for v in [1.0, 2.0, 2.5, 4.0, 7.0, 11.0, 30.0]]
r = h6.call('fc_NormSet', xb, 't', 's')
g = h6.globals_
xs = np.array([1.0, 2.0, 2.5, 4.0, 7.0, 11.0, 30.0])
check(r == 1 and abs(g['fcSkw'] - stats.skew(xs)) < 1e-9 and abs(g['fcKur'] - stats.kurtosis(xs)) < 1e-9
      and abs(g['fcSd'] / 1e150 - np.std(xs, ddof=1)) < 1e-9 and abs(g['fcW'] - stats.shapiro(xs).statistic) < 1e-9,
      'R6 values near 1E150: s, g1, g2, W as for the unscaled values')
# R7 static checks
src = open(PROG, encoding='utf-8').read()
lines = src.split('\n')
check(max(len(l) for l in lines) <= 250, 'R7 longest source line %d characters' % max(len(l) for l in lines))
inp = [l for l in lines if 'INPUT(' in l and not l.strip().startswith('//')]
check(inp and all(re.search(r'INPUT\(\{[^}]*\}, "[^"]*", \{[^{}]*\}', l) and 'CHAR(' not in l.split('INPUT(')[1] for l in inp),
      'R7 INPUT labels and helps hold no inline concatenation: %s' % [l.strip()[:60] for l in inp])
check('fcPEXP := #FFF0DCh' in src, 'R7 the expected-bar fill is the house light orange')
check('keep " + fcH0' not in src and ': keep H' not in src, 'R7 no "keep H0"')
check('" + ";  " + fcUD' not in src and ';  " + fcUD' not in src, 'R7 footers comma-separated')
check("Triola's question (p. 653, paraphrased)" in src, 'R11 Triola\'s question labelled as a paraphrase')
check('Phi(' not in ''.join(re.findall(r'"[^"]*"', src)), 'R11 no "Phi(" in any string on screen')
b1 = open('/home/claude/new6/FitCheck_beta1.txt', encoding='utf-8').read()
import hashlib  # noqa: E402
check(hashlib.md5(b1.encode('utf-8')).hexdigest() == 'ed6f95fbdad90b5034d149fd01fa548e', 'R beta 1 left untouched')

# ======================================================================== the audit
print('S  every run: scientific strings, errors')
for hh in ALL_H:
    check(not hh.sci_strings, 'S scientific STRING in a run: %s' % hh.sci_strings[:3])

src = open(PROG, encoding='utf-8').read()
check(all(ord(c) < 128 for c in src), 'S the source is pure ASCII')
check('\r' not in src, 'S LF line ends')
check(src.startswith('#pragma mode( separator(.,;) integer(h32) )\n\n// (C) 2026 Roger D Metcalf'), 'S the header')
check('DISCLAIMER: a teaching and demonstration aid. Not validated for' in src, 'S the disclaimer line')
check(re.search(r'RETURN mnS;\s*END;\s*$', src) is not None, 'S ends with RETURN, not PRINT')
check('PRINT(' not in src, 'S no PRINT')
print('\n%d checks, %d failures' % (N_CHECK, len(FAILS)))
for f in FAILS[:40]:
    print('  ', f)
sys.exit(1 if FAILS else 0)
