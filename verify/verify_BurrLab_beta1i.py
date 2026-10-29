#!/usr/bin/env python3
"""verify_BurrLab_beta1i.py -- checks for BurrLab beta 1i (29 Oct 2026): beta 1h's script with Part H's
pixel-identity checks rewritten for the polyline (every point on beta 1c's one-point-per-column rows, exactly;
the straight line between points within 2 px of them; the point columns 1, 4, ..., 268 plus the pdf peak's two;
buYmax identical; at most half of beta 1h's statements per redraw), Part I's Python curve compared at the same
points (BU_IN has 10 values; BU_YP holds points), and Part L: the instant title and the hourglass on Explore,
Family and Rare, none on a first entry or an x0 move, the fit's blinking hourglass (a few statements, the same
C, K, S and evaluations as beta 1h), the hourglass lit before a PYTHON() fit call, the title clear of it.

verify_BurrLab_beta1g.py -- checks for BurrLab beta 1g (29 Oct 2026; beta 1f's script, the four Terminal messages now point to BU_PZ): beta 1e's script with a STRICT
hpprime stub (hpprime.eval sees only the program's EXPORTed names; any other name comes back as its own
text, so float() fails as it did on the calculator; an assignment to one raises) and Part J (the block reads
and writes only EXPORTed names; beta 1e's block fails under the strict stub, beta 1f's passes; an error
inside the block is caught there: no traceback, BU_PZ "error: ...", BU_OUT(12) = -2, PPL draws, the
readout says "py FAIL, PPL"). Run with BU_PROG=<file> to verify another version (beta 1e: fails).
Beta 1e's script = beta 1d's script (every check on
the PPL path: the harness has no Python) plus Part I: the Python mode-5 curves against the PPL cache
to 1E-9 on 12 shapes through the bridge, the page pixel-identical with either engine, the four
engine settings in the readout, the fallback and the Both comparison. Beta 1d's script = beta 1c's plus Part H: the
fast Explore redraw against beta 1c pixel for pixel (curve, shade edge, texts), the statement and
primitive counts per redraw, the timing readout, the cache invalidation. Beta 1c's script = beta 1b's plus the
text-overlap check on every screen (Part F) and the soft-key selection check. Beta 1b's script (every
check re-run on the PPL path, which is what the harness takes: it has no Python) plus Part E (the
MicroPython engine: the #PYTHON bul block executed under CPython with a stub hpprime against the
PPL engine; the four engine settings with Python answering and with Python absent; badges; BU_PZ).
Beta 1a's Part D
(the second review's findings: the Weibull-limit detection on the reviewer's samples and 20 fresh
ones, the clamped install, bu_Median / bu_Num caps, the simplex as lists, the A-D and Danish text).

Part A  the formulas, by calling the program's own routines in the PC harness (ppl_run_v3e)
        and comparing with SciPy / mpmath / independent NumPy arithmetic:
   A1 special functions: bu_LnGam vs gammaln, bu_Digam / bu_Trigam vs scipy, bu_Log1p,
      bu_Expm1, bu_GamP vs gammainc;
   A2 the Burr XII: pdf, CDF, survival, quantile, hazard, mean, SD, median, mode against
      scipy.stats.burr12(c = C, d = K, scale = S) on a grid that includes C, K up to 400 and
      x from 1E-6 S to 1E6 S (tails compared in logs);
   A3 E[X^r] (bu_Mom) against mpmath's Beta function, r = 1..3;
   A4 maximum likelihood: bu_LLBurr vs the sum of burr12.logpdf; the program's fit (bu_Fit)
      on the three raw presets and 20 random samples against a SciPy Nelder-Mead on the
      same log-likelihood (ln L to 1E-6, interior parameters to 1E-4 relative); the
      Weibull-limit flag on the Rossi weeks (ln L = the Weibull's, lambda = S K^(-1/C));
   A5 standard errors: the program's observed-information SEs against an mpmath (30-digit)
      central-difference Hessian of the same log-likelihood, 1 % tolerance;
   A6 the rivals: exponential, lognormal, Weibull, gamma, Lomax against scipy.stats fits
      (expon, lognorm, weibull_min floc=0, gamma floc=0, lomax floc=0): ln L to 1E-5 and the
      parameters; the Lomax boundary flag against the exponential ln L; AIC and BIC;
   A7 the grouped likelihood bu_GLL against a direct NumPy computation at 12 parameter
      sets, and the grouped fit on the Danish bins against a SciPy Nelder-Mead;
   A8 Anderson-Darling A^2 against the hand formula with burr12.cdf (and against
      scipy.stats.anderson's formula shape on a normal sample, for the shape of the sum);
   A9 the simulation: 1 to 2,000 inverse-CDF draws through the harness with a seeded
      RANDOM, the running mean and median replayed from the same random numbers;
   A10 the CAS page's templates through desktop Giac: simplify(...) agrees with the
      decimal by value; the badge logic with cas='giac' and cas='fail';
   A11 edge inputs through bu_LoadMine + bu_Fit: n = 5, all values equal, ties, a huge
      value, tiny values, n = 1000, a negative value (refused), an empty D1 (refused).
Part B  every menu path of BurrLab() in the harness (cas='giac' and cas='fail', and once in
        stale-key mode): the numbers ON THE PAGES against SciPy, no runtime error, no
        scientific number (h.sci_strings), no text off the 320 x 240 screen or under the
        soft keys (6.5 / 8 / 9.5 px per character), MSGBOX at most 5 lines.
Part C  G1 cost: the objective-evaluation counts per preset, for the NOTES.
Run:  python3 verify_BurrLab_beta1e.py      (exit status 0 = every check passed)
"""
import collections
import csv
import math
import os
import random
import re
import sys
import time
import warnings

import mpmath
import numpy as np
from scipy import optimize, special, stats

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
os.environ.setdefault('HPKIT', '/home/claude/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(ROOT, 'ref'))
from ppl_run_v3e import Harness  # noqa: E402

PROG = os.environ.get('BU_PROG') or os.path.join(ROOT, 'BurrLab_beta1i.txt')
PROG_H = os.path.join(ROOT, 'BurrLab_beta1h.txt')
PROG_E = os.path.join(ROOT, 'BurrLab_beta1e.txt')
PROG_C = os.path.join(ROOT, 'BurrLab_beta1c.txt')
DATA = os.path.join(ROOT, 'data')
N_CHECK = 0
FAILS = []
SK = [27, 80, 133, 187, 240, 294]


def check(ok, msg):
    global N_CHECK
    N_CHECK += 1
    if not ok:
        FAILS.append(msg)
        print('FAIL', msg)


def rel(a, b, tol):
    return abs(a - b) <= tol * max(1e-300, abs(b))


def new_h(**kw):
    kw.setdefault('strict', False)
    kw.setdefault('idle_key', 4)
    kw.setdefault('cas', 'fail')
    h = Harness(PROG, **kw)
    # RANDSEED is not in the harness: reseed its RANDOM, as the calculator's RANDSEED does
    h._table['RANDSEED'] = lambda a, site: (h.rng.seed(int(a[0])), 0.0)[1]
    return h


# ---------------------------------------------------------------- the data
bjs = sorted(int(r['months']) for r in csv.DictReader(open(os.path.join(DATA, 'crimedatasets_Sentence_tbl_df.csv'))))
rossi = sorted(int(r['week']) for r in csv.DictReader(open(os.path.join(DATA, 'rossi.csv'))) if r['arrest'] == '1')


def prog_list(h, loader):
    h.call(loader)
    return [float(v) for v in h.globals_['buD']]


# ---------------------------------------------------------------- reference maths
def burr_ll(x, C, K, S):
    x = np.asarray(x, float)
    return float(np.sum(stats.burr12.logpdf(x, C, K, scale=S)))


def ref_fit(x, start):
    """SciPy Nelder-Mead on the full 3-parameter log-likelihood (log scale)."""
    x = np.asarray(x, float)
    def f(t):
        t = np.clip(t, -40, 40)
        return -np.sum(stats.burr12.logpdf(x, math.exp(t[0]), math.exp(t[1]), scale=math.exp(t[2])))
    best = None
    for s0 in start:
        r = optimize.minimize(f, [math.log(v) for v in s0], method='Nelder-Mead',
                              options=dict(xatol=1e-9, fatol=1e-11, maxiter=40000, maxfev=40000))
        if best is None or r.fun < best.fun:
            best = r
    return math.exp(best.x[0]), math.exp(best.x[1]), math.exp(best.x[2]), -best.fun


def mp_hessian_se(x, C, K, S):
    mpmath.mp.dps = 30
    xs = [mpmath.mpf(v) for v in x]

    def ll(c, k, s):
        tot = mpmath.mpf(0)
        for v in xs:
            z = (v / s) ** c
            tot += mpmath.log(c * k / s) + (c - 1) * mpmath.log(v / s) - (k + 1) * mpmath.log(1 + z)
        return tot
    th = [mpmath.mpf(C), mpmath.mpf(K), mpmath.mpf(S)]
    H = mpmath.matrix(3, 3)
    hs = [t * mpmath.mpf('1e-5') for t in th]
    f0 = ll(*th)
    for i in range(3):
        for j in range(i, 3):
            if i == j:
                p = list(th); p[i] += hs[i]
                m = list(th); m[i] -= hs[i]
                H[i, i] = (ll(*p) - 2 * f0 + ll(*m)) / hs[i] ** 2
            else:
                pp = list(th); pp[i] += hs[i]; pp[j] += hs[j]
                pm = list(th); pm[i] += hs[i]; pm[j] -= hs[j]
                mp_ = list(th); mp_[i] -= hs[i]; mp_[j] += hs[j]
                mm = list(th); mm[i] -= hs[i]; mm[j] -= hs[j]
                H[i, j] = H[j, i] = (ll(*pp) - ll(*pm) - ll(*mp_) + ll(*mm)) / (4 * hs[i] * hs[j])
    V = (-H) ** -1
    return [float(mpmath.sqrt(V[i, i])) for i in range(3)]


def grouped_ll(edges, counts, sf):
    """sum n_j ln(SF(e_{j-1}) - SF(e_j)), bin 1 from 0, the last open."""
    s0 = 1.0
    tot = 0.0
    for j, n in enumerate(counts):
        s1 = sf(edges[j]) if j < len(edges) else 0.0
        p = s0 - s1
        if n > 0:
            if p <= 0:
                return -1e200
            tot += n * math.log(p)
        s0 = s1
    return tot


def ad_stat(x, C, K, S):
    x = np.sort(np.asarray(x, float))
    n = len(x)
    u = stats.burr12.cdf(x, C, K, scale=S)
    i = np.arange(1, n + 1)
    return float(-n - np.mean((2 * i - 1) * (np.log(u) + np.log1p(-u[::-1]))))


# ================================================================== PART A
print('A1 special functions')
H = new_h()
H.call('bu_Init')
G = H.globals_
for z in [0.3, 0.5, 1, 1.5, 2, 2.5, 3.7, 7, 10.5, 33, 100.5, 532, 1000, 5000]:
    check(abs(H.call('bu_LnGam', float(z)) - special.gammaln(z)) <= 1e-10 * max(1, abs(special.gammaln(z))), 'A1 lnGamma(%g)' % z)
    check(abs(H.call('bu_Digam', float(z)) - special.digamma(z)) < 1e-9 * max(1, abs(special.digamma(z))), 'A1 digamma(%g)' % z)
    check(rel(H.call('bu_Trigam', float(z)), special.polygamma(1, z), 1e-8), 'A1 trigamma(%g)' % z)
for v in [-0.9, -1e-7, -1e-5, 0, 1e-9, 1e-5, 5e-5, 1e-3, 0.5, 3, 40]:
    check(rel(H.call('bu_Log1p', float(v)), math.log1p(v), 1e-11) if v != 0 else H.call('bu_Log1p', 0.0) == 0, 'A1 log1p(%g)' % v)
    check(rel(H.call('bu_Expm1', float(v)), math.expm1(v), 1e-11) if v != 0 else H.call('bu_Expm1', 0.0) == 0, 'A1 expm1(%g)' % v)
for a in [0.3, 0.9, 1.3, 2.5, 7, 37.7]:
    for xx in [0.01, 0.5, a, a + 1.5, 3 * a + 5, 60, 240]:
        check(abs(H.call('bu_GamP', float(a), float(xx)) - special.gammainc(a, xx)) < 1e-10, 'A1 gammainc(%g,%g)' % (a, xx))
        q = special.gammaincc(a, xx)
        check(rel(H.call('bu_GamQ', float(a), float(xx)), q, 1e-9) if q > 1e-290 else H.call('bu_GamQ', float(a), float(xx)) < 1e-280, 'A1 gammaincc(%g,%g) %r vs %r' % (a, xx, H.call('bu_GamQ', float(a), float(xx)), q))

print('A2 the Burr XII against scipy.stats.burr12')
grid = [(2, 1.5, 10), (1, 1, 1), (0.5, 0.7, 3), (0.25, 4, 100), (10.84, 0.898, 150.14), (1.183, 1.079, 0.825),
        (30, 30, 1), (100, 100, 1), (400, 400, 50), (0.2, 0.2, 0.01), (2.047, 500, 20978), (1, 0.3, 5)]
for C, K, S in grid:
    for f in [1e-6, 1e-3, 0.1, 0.5, 1, 1.5, 3, 10, 100, 1e4, 1e6]:
        x = f * S
        lp = stats.burr12.logpdf(x, C, K, scale=S)
        lsf = stats.burr12.logsf(x, C, K, scale=S)
        tag = ' (C=%g K=%g S=%g x=%g)' % (C, K, S, x)
        pl = H.call('bu_LnSF', x, C, K, S)
        check(abs(pl - lsf) <= 1e-9 * max(1, abs(lsf)) + 1e-12, 'A2 lnSF' + tag + ' %r vs %r' % (pl, lsf))
        pp = H.call('bu_Pdf', x, C, K, S)
        if lp > -700:
            check(rel(pp, math.exp(lp), 1e-9), 'A2 pdf' + tag + ' %r vs %r' % (pp, math.exp(lp)))
        else:
            check(pp == 0, 'A2 pdf below range should be 0' + tag)
        if lp > -700:
            check(rel(H.call('bu_LnPdf', x, C, K, S), lp, 1e-9), 'A2 lnpdf' + tag)
        pc = H.call('bu_CDF', x, C, K, S)
        cd = stats.burr12.cdf(x, C, K, scale=S)
        check(abs(pc - cd) <= 1e-9 * max(cd, 1e-12) + 1e-14, 'A2 cdf' + tag + ' %r vs %r' % (pc, cd))
        hz = stats.burr12.pdf(x, C, K, scale=S) / stats.burr12.sf(x, C, K, scale=S) if lsf > -700 and lp > -700 else None
        if hz is not None and hz > 1e-300:
            check(rel(H.call('bu_Haz', x, C, K, S), hz, 1e-8), 'A2 hazard' + tag)
    for p in [1e-10, 1e-6, 0.001, 0.025, 0.5, 0.9, 0.975, 0.999, 1 - 1e-9]:
        q = stats.burr12.ppf(p, C, K, scale=S)
        pq = H.call('bu_Quant', p, C, K, S)
        if np.isfinite(q) and q > 0:
            if math.log(q / S) > 500:
                check(rel(pq, S * math.exp(500), 1e-8), 'A2 capped quantile p=%g C=%g K=%g S=%g' % (p, C, K, S))
            else:
                check(rel(pq, q, 1e-8), 'A2 quantile p=%g C=%g K=%g S=%g %r vs %r' % (p, C, K, S, pq, q))
    mn = stats.burr12.mean(C, K, scale=S) if K * C > 1 else 0
    pm = H.call('bu_Mean', C, K, S)
    check(rel(pm, mn, 1e-8) if K * C > 1 else pm == 0, 'A2 mean C=%g K=%g S=%g %r vs %r' % (C, K, S, pm, mn))
    sd = stats.burr12.std(C, K, scale=S) if K * C > 2 else 0
    ps = H.call('bu_SD', C, K, S)
    check(rel(ps, sd, 1e-6) if K * C > 2 else ps == 0, 'A2 sd C=%g K=%g S=%g %r vs %r' % (C, K, S, ps, sd))
    check(rel(H.call('bu_Median', C, K, S), stats.burr12.median(C, K, scale=S), 1e-9), 'A2 median C=%g K=%g S=%g' % (C, K, S))
    mode = S * ((C - 1) / (K * C + 1)) ** (1 / C) if C > 1 else 0
    check(rel(H.call('bu_Mode', C, K, S), mode, 1e-9) if C > 1 else H.call('bu_Mode', C, K, S) == 0, 'A2 mode C=%g K=%g S=%g' % (C, K, S))
    case = 2 if K * C > 2 else (1 if K * C > 1 else 0)
    check(H.call('bu_MomCase', C, K) == case, 'A2 moment case C=%g K=%g' % (C, K))

print('A3 E[X^r] against mpmath')
mpmath.mp.dps = 30
for C, K, S in grid:
    for r in (1, 2, 3):
        pv = H.call('bu_Mom', r, C, K, S)
        if K * C > r:
            ref = float(mpmath.mpf(S) ** r * K * mpmath.beta(mpmath.mpf(K) - mpmath.mpf(r) / C, 1 + mpmath.mpf(r) / C))
            check(rel(pv, ref, 1e-8), 'A3 E[X^%d] C=%g K=%g S=%g %r vs %r' % (r, C, K, S, pv, ref))
        else:
            check(pv == 0, 'A3 E[X^%d] should not exist C=%g K=%g' % (r, C, K))

print('A4 maximum likelihood')
EVALS = {}
samples = [('BJS', 'bu_LoadBJS', bjs), ('Rossi', 'bu_LoadRossi', rossi), ('Danish300', 'bu_LoadDan300', None)]
rng = np.random.default_rng(20261027)
rand_samples = []
for i in range(20):
    kind = i % 4
    n = int(rng.choice([8, 15, 25, 41, 60, 100, 150]))
    if kind == 0:
        C, K, S = rng.uniform(0.6, 4), rng.uniform(0.4, 3), rng.uniform(0.5, 50)
        x = stats.burr12.rvs(C, K, scale=S, size=n, random_state=rng)
    elif kind == 1:
        x = rng.lognormal(2, 0.7, size=n)
    elif kind == 2:
        x = rng.pareto(1.5, size=n) + 0.2
    else:
        x = rng.gamma(3, 2, size=n)
    x = np.round(x, 4)
    x = np.maximum(x, 0.0001)
    rand_samples.append(('rand%d' % i, None, list(x)))
for name, loader, x in samples + rand_samples:
    h = new_h(app_data={'D1': x} if loader is None else None)
    h.call('bu_Init')
    if loader:
        x = prog_list(h, loader)
    else:
        check(h.call('bu_LoadMine') == 1, 'A4 LoadMine %s' % name)
    x = np.asarray(sorted(x), float)
    h.call('bu_Fit')
    g = h.globals_
    EVALS[name] = (len(x), g['buEvals'])
    C, K, S, LL, flag = g['buFC'], g['buFK'], g['buFS'], g['buFLL'], int(g['buFlag'])
    check(h.error is None, 'A4 fit error %s: %s' % (name, h.error))
    check(rel(h.call('bu_LLBurr', C, K, S), burr_ll(x, C, K, S), 1e-9), 'A4 bu_LLBurr %s' % name)
    check(rel(h.call('bu_LLBurr', 2.0, 1.5, 10.0), burr_ll(x, 2, 1.5, 10), 1e-9), 'A4 bu_LLBurr(2,1.5,10) %s' % name)
    med = float(np.median(x))
    rC, rK, rS, rLL = ref_fit(x, [(1, 1, med), (3, 0.7, med), (0.7, 2, med * 2), (max(0.05, C), max(1e-3, K), S)])
    if flag == 0:
        check(abs(LL - rLL) <= 1e-6 * max(1, abs(rLL)) + 1e-6, 'A4 lnL %s: %r vs SciPy %r' % (name, LL, rLL))
        check(rel(C, rC, 1e-3) and rel(K, rK, 1e-3) and rel(S, rS, 1e-3),
              'A4 parameters %s: (%r,%r,%r) vs SciPy (%r,%r,%r)' % (name, C, K, S, rC, rK, rS))
        # the profile optimum is a true maximum: ln L at the MLE beats SciPy's within tolerance
        check(LL >= rLL - 1e-5, 'A4 %s program lnL below SciPy: %r < %r' % (name, LL, rLL))
    else:
        # at a boundary: the program's ln L is within 1E-3 of the free optimum, and the
        # Weibull limit reproduces the Weibull fit
        check(LL >= rLL - 2e-3, 'A4 %s boundary lnL %r vs free %r' % (name, LL, rLL))
        if flag == 1:
            cw, lw, sw = stats.weibull_min.fit(x, floc=0)
            llw = float(np.sum(stats.weibull_min.logpdf(x, cw, scale=sw)))
            check(abs(LL - llw) < 2e-3, 'A4 %s Weibull limit lnL %r vs Weibull %r' % (name, LL, llw))
            check(rel(C, cw, 2e-3) and rel(S * K ** (-1 / C), sw, 2e-3), 'A4 %s Weibull limit k, lambda' % name)
    print('   %-10s n=%4d flag=%d C=%.5f K=%.5g S=%.5g lnL=%.5f (SciPy %.5f) evals=%d' % (name, len(x), flag, C, K, S, LL, rLL, g['buEvals']))
    check(rel(g['buFAIC'], 6 - 2 * LL, 1e-12) and rel(g['buFBIC'], 3 * math.log(len(x)) - 2 * LL, 1e-12), 'A4 AIC/BIC %s' % name)
    # A5 standard errors
    if flag == 0 and g['buSEOK'] == 1:
        se = mp_hessian_se(x, C, K, S)
        for i, (pse, rse) in enumerate(zip([g['buSE1'], g['buSE2'], g['buSE3']], se)):
            check(rel(pse, rse, 0.01), 'A5 SE%d %s: %r vs mpmath %r' % (i + 1, name, pse, rse))
    # A6 rivals
    n = len(x)
    lx = np.log(x)
    ll_exp = float(np.sum(stats.expon.logpdf(x, scale=x.mean())))
    check(rel(g['buRvL'][0], ll_exp, 1e-9) and rel(g['buRv1'][0], x.mean(), 1e-12), 'A6 exponential %s' % name)
    sg = float(np.sqrt(np.mean((lx - lx.mean()) ** 2)))
    ll_ln = float(np.sum(stats.lognorm.logpdf(x, sg, scale=math.exp(lx.mean()))))
    if sg > 0:
        check(rel(g['buRvL'][1], ll_ln, 1e-9) and rel(g['buRv2'][1], sg, 1e-9), 'A6 lognormal %s' % name)
    cw, lw, sw = stats.weibull_min.fit(x, floc=0)
    llw = float(np.sum(stats.weibull_min.logpdf(x, cw, scale=sw)))
    if g['buRvOK'][2] == 1:
        check(abs(g['buRvL'][2] - llw) <= 1e-5 * max(1, abs(llw)) + 1e-5, 'A6 Weibull lnL %s: %r vs %r' % (name, g['buRvL'][2], llw))
        check(rel(g['buRv1'][2], cw, 2e-3) and rel(g['buRv2'][2], sw, 2e-3), 'A6 Weibull params %s: (%r,%r) vs (%r,%r)' % (name, g['buRv1'][2], g['buRv2'][2], cw, sw))
        check(g['buRvL'][2] >= llw - 1e-5, 'A6 Weibull program lnL below SciPy %s' % name)
    ag, lg, tg = stats.gamma.fit(x, floc=0)
    llg = float(np.sum(stats.gamma.logpdf(x, ag, scale=tg)))
    if g['buRvOK'][3] == 1:
        check(abs(g['buRvL'][3] - llg) <= 1e-6 * max(1, abs(llg)) + 1e-6, 'A6 gamma lnL %s: %r vs %r' % (name, g['buRvL'][3], llg))
        check(g['buRvL'][3] >= llg - 1e-6, 'A6 gamma program lnL below SciPy %s' % name)
        check(rel(g['buRv1'][3], ag, 1e-3) and rel(g['buRv2'][3], tg, 1e-3), 'A6 gamma params %s' % name)
    cl, ll_, sl = stats.lomax.fit(x, floc=0)
    lll = float(np.sum(stats.lomax.logpdf(x, cl, scale=sl)))
    if g['buRvFl'][4] == 1:
        check(g['buRvL'][4] == g['buRvL'][0] and lll <= ll_exp + 1e-3, 'A6 Lomax boundary %s: lnL %r vs exponential %r (SciPy Lomax %r)' % (name, g['buRvL'][4], ll_exp, lll))
    else:
        check(abs(g['buRvL'][4] - lll) <= 1e-5 * max(1, abs(lll)) + 1e-4, 'A6 Lomax lnL %s: %r vs %r' % (name, g['buRvL'][4], lll))
        check(g['buRvL'][4] >= lll - 1e-4, 'A6 Lomax program lnL below SciPy %s' % name)
    for i in range(5):
        if g['buRvOK'][i] == 1:
            check(rel(g['buRvA'][i], 2 * g['buRvP'][i] - 2 * g['buRvL'][i], 1e-12), 'A6 AIC row %d %s' % (i, name))
    best = int(g['buBest'])
    aics = [g['buRvA'][i] for i in range(5) if g['buRvOK'][i] == 1]
    check(best > 0 and g['buRvA'][best - 1] == min(aics), 'A6 best rival %s' % name)
    # A8 Anderson-Darling
    if g['buADOK'] == 1:
        check(rel(g['buAD'], ad_stat(x, C, K, S), 1e-8), 'A8 A2 %s: %r vs %r' % (name, g['buAD'], ad_stat(x, C, K, S)))

print('A7 the grouped likelihood')
h = new_h()
h.call('bu_Init')
h.call('bu_LoadDanBin')
g = h.globals_
edges = [float(v) for v in g['buGEd']]
counts = [int(v) for v in g['buGCnt']]
check(len(edges) == 59 and len(counts) == 60 and sum(counts) == 2156, 'A7 bins shape')
check(all(abs(e - 10 ** (-3 + 0.1 * j)) < 1e-12 * e for j, e in enumerate(edges)), 'A7 edges are 10^(-3+0.1j)')
sets = [(1, 1, 1), (1.138, 1.228, 1.023), (0.5, 2, 3), (2, 0.5, 0.2), (3, 3, 1), (0.7, 0.9, 10), (1.2, 1.2, 1.2),
        (4, 0.2, 0.001), (1, 5, 50), (2.5, 0.4, 0.4), (0.3, 3, 0.05), (6, 0.5, 2)]
for C, K, S in sets:
    pv = h.call('bu_GLL', 1, float(C), float(K), float(S))
    ref = grouped_ll(edges, counts, lambda e: float(stats.burr12.sf(e, C, K, scale=S)))
    check(abs(pv - ref) <= 1e-8 * max(1, abs(ref)), 'A7 GLL Burr (%g,%g,%g) %r vs %r' % (C, K, S, pv, ref))
for m, a, b, sf in [(2, 2.3, 0, lambda e: math.exp(-e / 2.3)), (3, -0.26, 1.49, lambda e: stats.norm.sf(math.log(e), -0.26, 1.49)),
                    (4, 0.67, 1.6, lambda e: math.exp(-(e / 1.6) ** 0.67)), (6, 1.66, 1.57, lambda e: (1 + e / 1.57) ** -1.66),
                    (5, 1.3, 2.6, lambda e: stats.gamma.sf(e, 1.3, scale=2.6))]:
    pv = h.call('bu_GLL', m, float(a), float(b), 0.0)
    ref = grouped_ll(edges, counts, sf)
    check(abs(pv - ref) <= 1e-8 * max(1, abs(ref)), 'A7 GLL model %d %r vs %r' % (m, pv, ref))
h.call('bu_Fit')
EVALS['DanishBin'] = (2156, g['buEvals'])
C, K, S, LL = g['buFC'], g['buFK'], g['buFS'], g['buFLL']
f = lambda t: -grouped_ll(edges, counts, lambda e: float(stats.burr12.sf(e, math.exp(t[0]), math.exp(t[1]), scale=math.exp(t[2]))))
r = optimize.minimize(f, [math.log(1.2), math.log(1.2), math.log(1.0)], method='Nelder-Mead', options=dict(xatol=1e-9, fatol=1e-11, maxiter=20000, maxfev=20000))
check(abs(LL + r.fun) <= 1e-6 * abs(r.fun), 'A7 grouped Burr lnL %r vs SciPy %r' % (LL, -r.fun))
check(rel(C, math.exp(r.x[0]), 2e-3) and rel(K, math.exp(r.x[1]), 2e-3) and rel(S, math.exp(r.x[2]), 2e-3), 'A7 grouped Burr params (%r,%r,%r) vs (%r,%r,%r)' % (C, K, S, math.exp(r.x[0]), math.exp(r.x[1]), math.exp(r.x[2])))
print('   grouped Burr: C=%.5f K=%.5f S=%.5f lnL=%.4f (SciPy %.4f) evals=%d' % (C, K, S, LL, -r.fun, g['buEvals']))
# the grouped rivals against SciPy on the same grouped likelihoods
for i, (nm, dim, f) in enumerate([
        ('exp', 1, lambda t: -grouped_ll(edges, counts, lambda e: math.exp(-e / math.exp(t[0])))),
        ('lognormal', 2, lambda t: -grouped_ll(edges, counts, lambda e: stats.norm.sf(math.log(e), t[0], math.exp(t[1])))),
        ('Weibull', 2, lambda t: -grouped_ll(edges, counts, lambda e: math.exp(-math.exp(math.exp(t[0]) * math.log(e / math.exp(t[1])))))),
        ('Lomax', 2, lambda t: -grouped_ll(edges, counts, lambda e: math.exp(-math.exp(t[0]) * math.log1p(e / math.exp(t[1])))))]):
    row = [0, 1, 2, 4][i]
    x0 = {1: [0.5], 2: [0, 0.3]}[dim]
    r = optimize.minimize(f, x0, method='Nelder-Mead', options=dict(xatol=1e-9, fatol=1e-11, maxiter=20000))
    check(abs(g['buRvL'][row] + r.fun) <= 1e-6 * abs(r.fun), 'A7 grouped %s lnL %r vs SciPy %r' % (nm, g['buRvL'][row], -r.fun))
check(g['buRvOK'][3] == 0 and g['buRvFl'][3] == 2, 'A7 grouped gamma is skipped and flagged')
# the grouped SEs against mpmath on the grouped likelihood
mpmath.mp.dps = 30


def gll_mp(c, k, s):
    s0 = mpmath.mpf(1)
    tot = mpmath.mpf(0)
    for j, n in enumerate(counts):
        s1 = (1 + (mpmath.mpf(edges[j]) / s) ** c) ** (-k) if j < len(edges) else mpmath.mpf(0)
        if n > 0:
            tot += n * mpmath.log(s0 - s1)
        s0 = s1
    return tot


th = [mpmath.mpf(C), mpmath.mpf(K), mpmath.mpf(S)]
Hm = mpmath.matrix(3, 3)
hs = [t * mpmath.mpf('1e-5') for t in th]
f0 = gll_mp(*th)
for i in range(3):
    for j in range(i, 3):
        if i == j:
            p = list(th); p[i] += hs[i]
            m = list(th); m[i] -= hs[i]
            Hm[i, i] = (gll_mp(*p) - 2 * f0 + gll_mp(*m)) / hs[i] ** 2
        else:
            pp = list(th); pp[i] += hs[i]; pp[j] += hs[j]
            pm = list(th); pm[i] += hs[i]; pm[j] -= hs[j]
            mp_ = list(th); mp_[i] -= hs[i]; mp_[j] += hs[j]
            mm = list(th); mm[i] -= hs[i]; mm[j] -= hs[j]
            Hm[i, j] = Hm[j, i] = (gll_mp(*pp) - gll_mp(*pm) - gll_mp(*mp_) + gll_mp(*mm)) / (4 * hs[i] * hs[j])
V = (-Hm) ** -1
for i, pse in enumerate([g['buSE1'], g['buSE2'], g['buSE3']]):
    check(rel(pse, float(mpmath.sqrt(V[i, i])), 0.01), 'A5 grouped SE%d %r vs %r' % (i + 1, pse, float(mpmath.sqrt(V[i, i]))))

print('A8 Anderson-Darling: the hand formula on a normal sample via scipy.stats.anderson')
xn = stats.norm.rvs(size=50, random_state=3)
u = stats.norm.cdf(np.sort(xn), xn.mean(), xn.std(ddof=1))
i = np.arange(1, 51)
a2 = -50 - np.mean((2 * i - 1) * (np.log(u) + np.log1p(-u[::-1])))
check(abs(a2 - stats.anderson(xn, 'norm').statistic) < 1e-9, 'A8 the A2 formula matches scipy.stats.anderson (normal case)')

print('A9 the simulation replayed from the random numbers')
h = new_h()
h.call('bu_Init')
h.rng = random.Random(777)
C, K, S = 2.0, 1.5, 10.0
rep = random.Random(777)
draws = [h.call('bu_Draw') for _ in range(300)]
refd = [stats.burr12.ppf(rep.random(), C, K, scale=S) for _ in range(300)]
check(all(rel(a, b, 1e-9) for a, b in zip(draws, refd)), 'A9 300 inverse-CDF draws replayed')
# the page: 10 draws a frame, stop after a while with an anytime Esc
h = new_h()
h.call('bu_Init')
h.rng = random.Random(4242)
h.press('Esc', anytime=True)
h.call('bu_Sim')
g = h.globals_
check(h.error is None, 'A9 bu_Sim error %s' % h.error)
rep = random.Random(4242)
nsim = int(g['buSimN'])
refd = [stats.burr12.ppf(rep.random(), 2.0, 1.5, scale=10.0) for _ in range(nsim)]
check(nsim >= 10, 'A9 some frames ran (n = %d)' % nsim)
check(all(rel(a, b, 1e-9) for a, b in zip(g['buSimL'], refd)), 'A9 the page draws equal the replay')
cnts = [int(v) for v in g['buSimX']]
for c_, m_, md_ in zip(cnts, g['buRunM'], g['buRunMd']):
    check(rel(m_, float(np.mean(refd[:c_])), 1e-9) and rel(md_, float(np.median(refd[:c_])), 1e-9), 'A9 running mean/median at n = %d' % c_)
# a heavy tail: K C = 0.6, no mean; the page must say so and not fail
h = new_h()
h.call('bu_Init')
h.globals_['buC'] = 0.75; h.globals_['buK'] = 0.8
h.rng = random.Random(9)
h.press('Esc', anytime=True)
h.call('bu_Sim')
check(h.error is None, 'A9 heavy-tail bu_Sim error %s' % h.error)
check(any('NO mean' in t.text for t in h.texts), 'A9 heavy-tail page says NO mean')

print('A10 the CAS templates through Giac')
h = new_h(cas='giac')
h.call('bu_Init')
h.call('bu_CasProbe')
check(h.globals_['buCasOK'] == 1, 'A10 CAS probe (Beta(1,3/2) = 2/3)')
for C, K, S, r in [(2, 1.5, 10, 1), (2, 1.5, 10, 2), (2, 2, 10, 1), (1.5, 1, 10, 1), (10.84, 0.898, 150.138, 1), (1.183, 1.079, 0.825, 1), (3, 1, 7, 2)]:
    tx = '(%s)^%d*(%s)*Beta(%s-%d/(%s),1+%d/(%s))' % (h.call('bu_Frac', float(S)).strip('()'), r, h.call('bu_Frac', float(K)).strip('()'),
                                                      h.call('bu_Frac', float(K)).strip('()'), r, h.call('bu_Frac', float(C)).strip('()'), r, h.call('bu_Frac', float(C)).strip('()'))
    tx = tx.replace('(', '((', 1) if False else tx
    ans = h.call('bu_Cas', 'simplify(' + tx + ')')
    num = h.call('bu_Cas', 'evalf(' + tx + ')')
    Cr, Kr, Sr = round(C, 3), round(K, 3), round(S, 3)
    ref = Sr ** r * Kr * float(special.beta(Kr - r / Cr, 1 + r / Cr))
    check(len(ans) > 0 and len(num) > 0 and rel(float(num), ref, 1e-9), 'A10 CAS E[X^%d] C=%g K=%g S=%g: %r -> %r vs %r' % (r, C, K, S, ans, num, ref))
    print('   E[X^%d] C=%g K=%g S=%g: CAS %s = %s (ref %.6f)' % (r, C, K, S, ans, num, ref))
for cas in ('giac', 'fail'):
    h = new_h(cas=cas)
    h.call('bu_Init')
    h.call('bu_CasProbe')
    h.press('Enter')
    h.call('bu_Moments')
    txt = ' '.join(t.text for t in h.texts)
    check(h.error is None, 'A10 bu_Moments error cas=%s %s' % (cas, h.error))
    if cas == 'giac':
        check('exact (CAS)' in txt and '= 10' in txt and '= 200' in txt, 'A10 giac page shows exact 10 and 200: %s' % txt[:200])
    else:
        check('decimal' in txt and 'exact (CAS)' not in txt, 'A10 fallback page badged decimal')
    check('does not exist' in txt, 'A10 E[X^3] does not exist at K C = 3')

print('A11 edge inputs')
edge = {
    'n5': [1, 2, 3, 4, 5], 'ties': [1, 1, 1, 2, 2, 2, 3, 3, 3, 10, 10, 10],
    'huge': [1, 2, 3, 4, 5, 6, 7, 8, 9, 1e9], 'tiny': [1e-6, 2e-6, 3e-6, 5e-6, 8e-6, 1.3e-5, 2e-5],
    'n1000': list(np.round(stats.burr12.rvs(1.5, 1.2, scale=5, size=1000, random_state=11), 3)),
}
for nm, x in edge.items():
    h = new_h(app_data={'D1': x})
    h.call('bu_Init')
    ok = h.call('bu_LoadMine')
    check(ok == 1, 'A11 %s loads' % nm)
    r = h.call('bu_Fit')
    check(h.error is None, 'A11 %s fit runtime error: %s' % (nm, h.error))
    g = h.globals_
    print('   %-6s n=%d fit=%d flag=%d C=%.4g K=%.4g S=%.4g lnL=%.4f evals=%d' % (nm, len(x), r, g['buFlag'], g['buFC'], g['buFK'], g['buFS'], g['buFLL'], g['buEvals']))
    if nm == 'n1000':
        EVALS['n1000'] = (1000, g['buEvals'])
        xx = np.asarray(sorted(x), float)
        rC, rK, rS, rLL = ref_fit(xx, [(1.5, 1.2, 5)])
        check(abs(g['buFLL'] - rLL) < 1e-5 * abs(rLL), 'A11 n1000 lnL %r vs %r' % (g['buFLL'], rLL))
    for pg in ('bu_Results', 'bu_Table', 'bu_HistPage', 'bu_QQ', 'bu_Surv', 'bu_HazPage', 'bu_ADPage', 'bu_Rare'):
        h.press('Esc')
        h.call(pg)
        check(h.error is None, 'A11 %s page %s error: %s' % (nm, pg, h.error))
    check(not h.sci_strings, 'A11 %s scientific strings: %s' % (nm, h.sci_strings[:3]))
for nm, x in [('negative', [1, 2, -3, 4, 5, 6]), ('short', [1, 2, 3]), ('empty', []), ('equal', [7.0] * 12)]:
    h = new_h(app_data={'D1': x} if x else None)
    h.call('bu_Init')
    check(h.call('bu_LoadMine') == 0 and h.msgboxes and h.error is None, 'A11 %s refused with a message' % nm)

# ================================================================== PART B
print('B the pages')


def run(steps, cas='fail', app_data=None, stale=False, seed=0):
    h = new_h(cas=cas, app_data=app_data, stale_keys=stale)
    h.rng = random.Random(seed)
    h.press('Enter')
    for st in steps:
        k = st[0]
        if k == 'c':
            h.choose(st[1])
        elif k == 'k':
            h.press(st[1])
        elif k == 'ka':
            h.press(st[1], anytime=True)
        elif k == 's':
            h.tap(SK[st[1] - 1], 230)
        elif k == 't':
            h.tap(st[1], st[2])
        elif k == 'd':
            h.drag(st[1])
        elif k == 'i':
            h.answer(st[1])
    h.choose(0)
    res = h.call('BurrLab')
    return h, res


def page_text(p):
    return re.sub(r'\s+', ' ', ' '.join(p.lines())).strip()


def fnum(s):
    return float(s.replace('−', '-').replace(',', ''))


def find_num(txt, pat):
    m = re.search(pat, txt)
    return fnum(m.group(1).rstrip('.')) if m else None


INK = {1: 10, 2: 13, 3: 16}          # the glyphs' ink height: font 1 about 10 px in a 12 px row (emulator screenshots, 28 Oct 2026)


def overlaps(h, tag):
    """beta 1c: no two texts on a screen may overlap (2 px clearance between rows), and on a
    screen with the plot frame no text may straddle the frame's bottom edge."""
    bad = []
    for si, scr in enumerate(h.screens):
        last = {}
        for t in scr.texts:
            if str(t.grob) not in ('G1', 'G3', 'G4') or not t.text.strip():
                continue
            last[(round(t.x), round(t.y), int(t.font or 1))] = t
        items = []
        for t in last.values():
            cw = {1: 6.5, 2: 8.0, 3: 9.5}.get(int(t.font or 1), 6.5)
            w = min(len(t.text) * cw, t.width if t.width is not None else 320)
            items.append((t.x, t.x + w, t.y, t.y + INK[int(t.font or 1)], t.text))
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, b = items[i], items[j]
                if a[0] < b[1] and b[0] < a[1] and a[2] < b[3] + 2 and b[2] < a[3] + 2:
                    bad.append((a[4], b[4], a[2], b[2]))
        frame = [s for s in scr.shapes if str(s).startswith('RECT_P(36.0, 36.0,')]
        if frame:
            fx1, fy1, fx2, pb = [float(v) for v in str(frame[0]).split('(')[1].split(',')[:4]]
            for x0, x1, y0, y1, txt in items:
                if y0 <= pb and y1 > pb and x0 < fx2 and x1 > fx1:
                    bad.append(('straddles the frame', txt, y0))
    check(not bad, 'F overlap %s: %s' % (tag, bad[:5]))


def layout(h, tag):
    overlaps(h, tag)
    bad = []
    for scr in h.screens:
        has_menu = bool(getattr(scr, 'menu', None))
        for t in scr.texts:
            if str(t.grob) not in ('G0', 'G1', 'G3', 'G4', '0', '1', 'None'):
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


# ---- B1 Explore ----
h, res = run([('c', 'Explore'), ('k', 'Right'), ('k', 'Right'), ('s', 2), ('k', 'Up'), ('s', 3), ('k', 'Left'), ('k', 'Plus'),
              ('k', 'Minus'), ('s', 5), ('d', [(100, 100), (140, 100), ( 180, 100)]), ('s', 4), ('t', 200, 120),
              ('s', 6), ('s', 2), ('k', 'Esc'), ('s', 6), ('k', 'Zero'), ('k', 'Enter'), ('c', 'Choose K'), ('k', 'Down'), ('k', 'Esc'),
              ('c', 'Quit')])
layout(h, 'B1 explore')
T = [page_text(p) for p in h.pages]
ex = [t for t in T if t.startswith('C = ')]
check(len(ex) >= 12, 'B1 explore frames: %d' % len(ex))
for t in ex:
    C = find_num(t, r'C = ([0-9.]+)'); K = find_num(t, r'K = ([0-9.]+)'); S = find_num(t, r'S = ([0-9.]+)')
    x0 = find_num(t, r'x₀ = ([0-9.]+) '); pdf = find_num(t, r'pdf = ([0-9.<> ]+?),'); tail = find_num(t, r'P\(X > x₀\) = ([0-9.]+)')
    if None in (C, K, S, x0, tail):
        check(False, 'B1 could not read a frame: %s' % t[:120]); continue
    check(abs(tail - stats.burr12.sf(x0, C, K, scale=S)) < 6e-4, 'B1 P(X > x0) %r vs %r (C=%g K=%g S=%g x0=%g)' % (tail, stats.burr12.sf(x0, C, K, scale=S), C, K, S, x0))
    md = find_num(t, r'median ([0-9.]+)')
    check(md is not None and abs(md - stats.burr12.median(C, K, scale=S)) < 2e-3 * max(1, md), 'B1 median on screen %r' % md)
    mn = find_num(t, r'median [0-9.]+, mean ([0-9.]+)')
    if K * C > 1:
        check(mn is not None and abs(mn - stats.burr12.mean(C, K, scale=S)) < 2e-3 * max(1, mn), 'B1 mean on screen %r vs %r' % (mn, stats.burr12.mean(C, K, scale=S)))
    else:
        check('mean none' in t and 'NO mean' in t, 'B1 no-mean wording')
    kc = find_num(t, r'K×C = ([0-9.]+)')
    check(kc is not None and abs(kc - K * C) < 0.006, 'B1 K x C on screen')
check(any('CDF' in t and '.5' in t for t in ex), 'B1 the CDF view drew its axis')
check('explorer at' in res, 'B1 return line: %s' % res)
# a drag with S chosen changes S; a drag with x0 chosen moves x0; heavy tail wording
h, res = run([('c', 'Explore'), ('s', 3), ('d', [(100, 100), (120, 100), (150, 100), (170, 100)]), ('s', 4), ('d', [(100, 100), (200, 100)]),
              ('s', 1), ('d', [(200, 100), (100, 100)]), ('s', 2), ('d', [(200, 100), (80, 100)]), ('k', 'Esc'), ('c', 'Quit')])
layout(h, 'B1b drags')
T = [page_text(p) for p in h.pages if page_text(p).startswith('C = ')]
check(any('S = 10.00' not in t and 'S = ' in t for t in T), 'B1b S changed by a drag')
check(any('x₀ = 15.00' not in t and 'x₀ = ' in t for t in T), 'B1b x0 moved by a drag')
check(any(': NO mean' in t for t in T), 'B1b heavy-tail label after dragging C and K down: %s' % T[-1][:160])

# ---- B2 Family ----
h, res = run([('c', 'Family'), ('k', 'Right'), ('k', 'Up'), ('s', 1), ('s', 4), ('t', 252, 101), ('d', [(100, 100), (130, 90), (160, 80)]),
              ('s', 5), ('s', 6), ('s', 1), ('s', 2), ('s', 3), ('k', 'Enter'), ('c', 'Weibull'), ('k', 'Minus'), ('k', 'Plus'), ('k', 'Esc'), ('c', 'Quit')])
layout(h, 'B2 family')
T = [page_text(p) for p in h.pages]
check(any('C = 1: Pareto II (Lomax)' in t for t in T), 'B2 Lomax named after the map tap')
check(any('C = K = 1: Lomax and log-logistic at once' in t for t in T), 'B2 C = K = 1 named')
check(any('near Weibull' in t for t in T), 'B2 the Weibull approach named')
wb = [t for t in T if 'near Weibull' in t]
for t in wb:
    K = find_num(t, r'K = ([0-9.]+), S'); S = find_num(t, r', S = ([0-9.]+):'); lam = find_num(t, r'near Weibull\([0-9.]+, ([0-9.]+)\)')
    C = find_num(t, r'C = ([0-9.]+),')
    check(abs(S * K ** (-1 / C) - lam) < 2e-2 * lam, 'B2 S = Sw K^(1/C) on the Weibull frames: S=%g K=%g C=%g lam=%g' % (S, K, C, lam))
check(any('K = 128' in t for t in wb), 'B2 the animation reached K = 128')
check(any('Singh-Maddala' in t for t in T), 'B2 Singh-Maddala named')
check(any('K = 1: log-logistic (Fisk)' in t or 'C = K = 1: Lomax and log-logistic' in t for t in T), 'B2 Fisk named (soft key)')

# ---- B3 the fit path on every preset, both CAS modes ----
for cas in ('giac', 'fail'):
    for label, loader, x in [('BJS', 'bu_LoadBJS', bjs), ('Rossi', 'bu_LoadRossi', rossi), ('300-value', 'bu_LoadDan300', None)]:
        steps = [('c', 'Fit my data'), ('c', label), ('k', 'Enter'), ('s', 1), ('k', 'Enter'), ('s', 2), ('k', 'Plus'), ('k', 'Enter'),
                 ('s', 3), ('t', 200, 100), ('k', 'Left'), ('k', 'Esc'), ('s', 4), ('k', 'Enter'), ('s', 5), ('k', 'Enter'), ('s', 6), ('s', 1),
                 ('k', 'Enter'), ('s', 2), ('k', 'Esc'), ('s', 3), ('t', 200, 100), ('k', 'Right'), ('s', 3), ('i', {'rrV': 200}), ('k', 'Esc'),
                 ('s', 4), ('k', 'Esc'), ('s', 6), ('k', 'Enter'), ('c', 'Anderson'), ('s', 5), ('c', 'Exact'), ('c', 'How rare'), ('k', 'Esc'), ('c', 'Quit')]
        h, res = run(steps, cas=cas)
        tag = 'B3 %s %s' % (label, cas)
        layout(h, tag)
        T = [page_text(p) for p in h.pages]
        hh = new_h(); hh.call('bu_Init')
        xx = np.asarray(prog_list(hh, loader), float)
        hh.call('bu_Fit')
        g = hh.globals_
        resp = [t for t in T if t.startswith('Burr XII fit:')]
        check(len(resp) >= 6, tag + ' results pages: %d' % len(resp))
        t = resp[0]
        if g['buFlag'] == 0:
            C = find_num(t, r'C = ([0-9.]+)'); K = find_num(t, r'K = ([0-9.]+)'); S = find_num(t, r'S = ([0-9.]+)')
            check(C is not None and rel(C, g['buFC'], 2e-3) and rel(K, g['buFK'], 2e-3) and rel(S, g['buFS'], 2e-3), tag + ' C K S on the page: %s' % t[:120])
            se1 = find_num(t, r'C = [0-9.]+ \(SE ([0-9.]+)\)')
            check(se1 is not None and rel(se1, g['buSE1'], 2e-3), tag + ' SE on the page')
        else:
            check('WEIBULL LIMIT' in t and 'K → ∞' in t, tag + ' Weibull limit wording')
        ll = find_num(t, r'ln L = (-?[0-9.]+)'); aic = find_num(t, r'AIC = ([0-9.]+)'); bic = find_num(t, r'BIC = ([0-9.]+)')
        check(ll is not None and abs(ll - g['buFLL']) < 0.006 and abs(aic - g['buFAIC']) < 0.006 and abs(bic - g['buFBIC']) < 0.006, tag + ' lnL AIC BIC on the page')
        check(abs(find_num(t, r'A² = ([0-9.]+)') - g['buAD']) < 6e-4, tag + ' A2 on the results page')
        if label == 'BJS':
            check('n = 41 is small' in t, tag + ' small-n caveat')
        tb = [t for t in T if t.startswith('AIC table:')][0]
        for i, nm in enumerate(['Exponential', 'Lognormal', 'Weibull', 'Gamma', 'Lomax']):
            if g['buRvOK'][i] == 1:
                v = find_num(tb, nm + r' [0-9] (-?[0-9.]+) ')
                check(v is not None and abs(v - g['buRvL'][i]) < 0.006, tag + ' table lnL %s %r vs %r' % (nm, v, g['buRvL'][i]))
        check('best' in tb and 'Burnham' in tb, tag + ' table marks the best and cites the rule')
        if label == 'Rossi':
            check('Weibull limit' in tb and 'exactly 2' in tb, tag + ' table explains the Weibull limit')
        rare = [t for t in T if t.startswith('How rare is this?')]
        check(len(rare) >= 4, tag + ' rare pages: %d' % len(rare))
        for t in rare:
            xv = find_num(t, r'x = ([0-9.]+) ')
            pl = find_num(t, r'P\(X ≤ x\) [=<>] ([0-9.]+),')
            above = find_num(t, r'Data: ([0-9]+) of')
            if xv is None or pl is None:
                check(False, tag + ' rare page unreadable: %s' % t[:140]); continue
            pc = stats.burr12.cdf(xv, g['buC'], g['buK'], scale=g['buS'])   # the shape the page uses (beta 1a: the K = 50 equivalent at the Weibull limit)
            check(abs(pl - pc) < 6e-5 or (pl == 0.9999 and pc > 0.99995) or (pl == 0.0001 and pc < 0.00005), tag + ' rare P(X<=x) at x=%g: %r vs %r' % (xv, pl, pc))
            cnt = int(np.sum(xx > xv))
            check(above == cnt or (abs(above - cnt) <= 1 and np.min(np.abs(xx - xv)) < 0.1), tag + ' rare empirical count at x=%g: %r vs %d' % (xv, above, cnt))
        check(any('x = 200' in t for t in rare), tag + ' typed x = 200 reached the page')
        check(any('Q-Q plot' in t and '#' in t for t in T), tag + ' Q-Q page with a readout')
        qq = [t for t in T if 'Q-Q plot' in t]
        for t in qq:
            i = int(find_num(t, r'#([0-9]+)/')); dv = find_num(t, r': x ([0-9.]+),'); mv = find_num(t, r'model ([0-9.]+), p')
            check(rel(dv, xx[i - 1], 2e-3) and rel(mv, stats.burr12.ppf((i - 0.5) / len(xx), g['buFC'], g['buFK'], scale=g['buFS']), 2e-3), tag + ' Q-Q readout point %d' % i)
        check(any('Survival, log-log' in t and ('slope -K×C' in t or 'Weibull limit: no Pareto line' in t) for t in T), tag + ' survival page')
        check(any('Hazard:' in t for t in T), tag + ' hazard page')
        check(any('A-D statistic' in t and 'NO p-value' in t for t in T), tag + ' A-D page is honest about p')
        check(any('Histogram:' in t and 'density per log10 unit' in t for t in T) and any('Histogram:' in t and ' density ' in t for t in T), tag + ' histogram in both scales')
        mo = [t for t in T if t.startswith('Exact moments')]
        check(len(mo) == 1 and ('exact (CAS)' in mo[0]) == (cas == 'giac'), tag + ' moments badge: %s' % mo[0][:200] if mo else tag + ' no moments page')
        check(res.startswith('BurrLab: ') and 'ln L = ' in res, tag + ' return line: %s' % res)
        EVALS.setdefault(label + ' (page run)', (len(xx), g['buEvals']))

# ---- B4 the grouped preset ----
h, res = run([('c', 'Fit my data'), ('c', 'all 2,156'), ('k', 'Enter'), ('s', 1), ('k', 'Enter'), ('s', 2), ('k', 'Enter'), ('s', 3), ('s', 4), ('k', 'Enter'),
              ('s', 5), ('k', 'Enter'), ('s', 6), ('s', 1), ('k', 'Enter'), ('s', 3), ('k', 'Esc'), ('s', 5), ('c', 'Quit')])
layout(h, 'B4 grouped')
T = [page_text(p) for p in h.pages]
check(any('Grouped maximum likelihood, n = 2156 in 60 bins' in t for t in T), 'B4 grouped wording')
check(any('not fitted on bins' in t for t in T), 'B4 gamma row says not fitted')
check(any('No Q-Q plot for binned counts' in ' '.join(m.lines) for m in h.msgboxes), 'B4 Q-Q refused for bins')
check(any('No A² here' in t for t in T), 'B4 A-D page says no A2 for bins')
check(any('bars: 2156 values in 60 bins' in t for t in T), 'B4 histogram of the bins')
check(any('Bins: about' in t for t in T), 'B4 rare page uses the bin edges')

# ---- B5 the simulation page driven as a student would ----
h, res = run([('c', 'never settles'), ('ka', 'Plus'), ('ka', 'Esc'), ('c', 'never settles'), ('k', 'Enter'), ('c', 'Seed'), ('i', {'smSd': 5}), ('ka', 'Esc'), ('c', 'Quit')], seed=12)
layout(h, 'B5 sim')
T = [page_text(p) for p in h.pages]
check(any('running mean' in t and 'true mean 10.000' in t and 'true median 7.664' in t for t in T), 'B5 sim page labels')
check(any('mean settles at 1/√n speed' in t for t in T), 'B5 moment-case wording (K C = 3)')
check(any('Seed' in d.title for d in h.inputs), 'B5 the seed form opened')

# ---- B6 rare with no data, moments with no fit, help, stale keys, Esc out of a fit ----
h, res = run([('c', 'How rare'), ('k', 'Right'), ('t', 150, 100), ('k', 'Esc'), ('c', 'Exact'), ('c', 'Help'), ('k', 'Right'), ('k', 'Right'), ('k', 'Right'), ('c', 'Quit')], cas='giac')
layout(h, 'B6 misc')
T = [page_text(p) for p in h.pages]
check(any("No data: the explorer's C, K, S are the model." in t for t in T), 'B6 rare page without data')
check(sum(1 for t in T if t.startswith('BurrLab help')) == 3, 'B6 three help pages')
check(any('DISCLAIMER' in t for t in T[:1]), 'B6 the disclaimer on the opening page')
h, res = run([('c', 'Fit my data'), ('c', 'BJS'), ('k', 'Enter'), ('s', 1), ('k', 'Enter'), ('s', 6), ('s', 5), ('c', 'Quit')], stale=True)
layout(h, 'B6 stale keys')
check(not h.stale_skips, 'B6 stale-key skips: %s' % h.stale_skips[:3])
h = new_h(); h.call('bu_Init'); h.call('bu_LoadBJS')
h.press('Esc', anytime=True)
r = h.call('bu_Fit')
check(r == 0 and h.globals_['buFitOK'] == 0 and h.error is None, 'B6 Esc stops the fit cleanly (r=%r)' % r)
h, res = run([('c', 'Fit my data'), ('c', 'Results of the last fit'), ('c', 'Quit')])
check(any('No fit yet' in ' '.join(m.lines) for m in h.msgboxes), 'B6 results without a fit refused')

# ================================================================== PART C
print('C G1 cost (objective evaluations per fit)')
for k, (n, ev) in EVALS.items():
    print('   %-20s n = %5d  evaluations = %d  ~ statements in the data loops = %d' % (k, n, ev, int(ev * (n if n < 2000 else 60) * 3)))


# ================================================================== PART D (beta 1a)
print('D1 the Weibull limit on the reviewer\'s samples and 20 fresh ones')
rev = []
for i in range(12):
    if i < 6:
        x = stats.weibull_min.rvs(2.5, scale=10, size=30, random_state=100 + i)
    else:
        x = stats.gamma.rvs(5, scale=2, size=40, random_state=200 + i)
    rev.append(('rev%d' % i, list(np.round(np.sort(x), 3))))
rev.append(('weib3', list(np.round(stats.weibull_min.rvs(3.0, scale=10, size=30, random_state=7), 3))))
rev.append(('tinyK', [1.0, 1.0001, 1.0002, 1.0003, 1.001, 1.002, 1.5, 2.0, 50.0, 1000.0]))
rev.append(('floor', [100, 100.5, 101, 101.2, 102, 103, 105, 110, 120, 150, 200, 400]))
rev.append(('outlier', [1, 2, 2, 3, 3, 3, 4, 4, 5, 6, 7, 9, 10000.0]))
rng2 = np.random.default_rng(1028)
for i in range(20):
    kind = i % 5
    n = int(rng2.choice([12, 20, 30, 40, 60, 100]))
    if kind == 0:
        x = stats.weibull_min.rvs(rng2.uniform(1.5, 4), scale=rng2.uniform(1, 30), size=n, random_state=rng2)
    elif kind == 1:
        x = stats.gamma.rvs(rng2.uniform(2, 8), scale=2, size=n, random_state=rng2)
    elif kind == 2:
        x = stats.burr12.rvs(rng2.uniform(0.7, 3), rng2.uniform(0.3, 2), scale=5, size=n, random_state=rng2)
    elif kind == 3:
        x = rng2.lognormal(1, 0.5, size=n)
    else:
        x = stats.norm.rvs(50, 5, size=n, random_state=rng2)
    rev.append(('fresh%d' % i, list(np.maximum(np.round(x, 3), 0.001))))
for name, x in rev:
    h = new_h(app_data={'D1': x})
    h.call('bu_Init')
    c0, k0, s0 = h.globals_['buC'], h.globals_['buK'], h.globals_['buS']
    check(h.call('bu_LoadMine') == 1, 'D1 %s loads' % name)
    h.call('bu_Fit')
    g = h.globals_
    check(h.error is None, 'D1 %s runtime error: %s' % (name, h.error))
    xx = np.asarray(sorted(x), float)
    C, K, S, LL, flag = g['buFC'], g['buFK'], g['buFS'], g['buFLL'], int(g['buFlag'])
    cw, lw, sw = stats.weibull_min.fit(xx, floc=0)
    llw = float(np.sum(stats.weibull_min.logpdf(xx, cw, scale=sw)))
    near_w = (LL - llw) <= 1e-4 * (1 + abs(LL)) and K > 100
    print('   %-8s n=%3d flag=%d K=%.3g lnS=%.2f top=%.2f lnL=%.4f Weib=%.4f SEok=%d' % (name, len(xx), flag, K, math.log(S), g['buBoxHi'], LL, llw, g['buSEOK']))
    if flag == 0:
        check(K <= 1e4, 'D1 %s flag 0 with K = %g' % (name, K))
        check(not near_w, 'D1 %s flag 0 but at the Weibull limit (lnL %r vs %r, K %g)' % (name, LL, llw, K))
        check(g['buSEOK'] == 1, 'D1 %s flag 0 without SEs (not positive definite)' % name)
        check(K * C < 1e6, 'D1 %s absurd slope K C = %g' % (name, K * C))
        # the explorer took the fit
        check(g['buC'] == C and g['buK'] == K and g['buS'] == S, 'D1 %s explorer took the fitted shape' % name)
    if flag == 1:
        check(near_w or math.log(S) > g['buBoxHi'] - 0.05, 'D1 %s flag 1 but not near the Weibull (lnL %r vs %r, K %g)' % (name, LL, llw, K))
        check(abs(LL - llw) < 2e-3 and rel(C, cw, 5e-3) and rel(S * K ** (-1 / C), sw, 5e-3), 'D1 %s Weibull limit numbers' % name)
        # the explorer holds the Weibull-equivalent at K = 50 with the same lambda
        lam = S * K ** (-1 / C)
        check(g['buK'] == 50 and rel(g['buC'], C, 1e-12) and rel(g['buS'] * 50 ** (-1 / g['buC']), lam, 1e-9), 'D1 %s explorer at K = 50 with lambda kept' % name)
        check(g['buSEOK'] == 0, 'D1 %s no SEs claimed at the limit' % name)
    if flag >= 2:
        check(g['buC'] == c0 and g['buK'] == k0 and g['buS'] == s0, 'D1 %s explorer left alone at a limit' % name)
    # pages after the fit: no error, no scientific number, no infinity
    for pg in ('bu_Results', 'bu_Table', 'bu_Surv', 'bu_Explore', 'bu_Rare', 'bu_Moments'):
        h.press('Esc')
        h.call(pg)
        check(h.error is None, 'D1 %s page %s error: %s' % (name, pg, h.error))
    check(not h.sci_strings, 'D1 %s scientific strings: %s' % (name, h.sci_strings[:3]))
    txt = ' '.join(t.text for t in h.texts)
    check('∞' not in txt.replace('K → ∞', '').replace('S → ∞', ''), 'D1 %s an infinity on a page' % name)
    check('not positive definite' not in txt, 'D1 %s "not positive definite" shown' % name)
    if flag == 1:
        check('Weibull-equivalent at K = 50' in txt and 'not a power law' in txt, 'D1 %s results page names the K = 50 equivalent' % name)
        check('model: Weibull-equivalent, K = 50' in txt, 'D1 %s rare page names the equivalent' % name)
    if flag >= 2:
        check("The explorer keeps its own shape" in txt and "fit at a limit: the explorer's shape" in txt, 'D1 %s limit wording on results and rare pages' % name)

print('D2 bu_Median / bu_Num caps, the simplex as lists')
h = new_h()
h.call('bu_Init')
for K in (0.0001, 0.0005, 0.0013, 0.0015, 0.01, 0.2, 1, 50):
    v = h.call('bu_Median', 2.0, float(K), 1.0)
    ref = stats.burr12.median(2.0, K, scale=1.0)
    if math.log(2) / K <= 500 and np.isfinite(ref) and ref < math.exp(500):
        check(rel(v, ref, 1e-9), 'D2 median K=%g %r vs %r' % (K, v, ref))
    else:
        check(v == 1e300, 'D2 median K=%g capped (%r)' % (K, v))
check(h.call('bu_Num', 1e300) == 'beyond range' and h.call('bu_Num', 1e12) == 'beyond range' and h.call('bu_Num', 99999.0) == '99999', 'D2 bu_Num cap')
src = open(PROG, encoding='utf-8').read()

check(re.search(r'^LOCAL [^;]*buSx1', src, re.M) is not None and 'buSx1(' in src, 'D2 the simplex is file-level LOCAL lists')
check('MAKEMAT' not in src.split('#PYTHON')[0] + src.split('#END')[-1], 'D2 no MAKEMAT in the PPL text')
h.call('bu_LoadBJS'); h.call('bu_Fit')
check(rel(h.globals_['buFLL'], -191.13744507805, 1e-9), 'D2 the list simplex reproduces the BJS optimum: %r' % h.globals_['buFLL'])

print('D3 text: A-D page, Danish source lines, the help promise')
h = new_h(); h.call('bu_Init'); h.call('bu_LoadBJS'); h.call('bu_Fit'); h.press('Esc'); h.call('bu_ADPage')
txt = ' '.join(t.text for t in h.texts)
check('Stephens (1986' in txt and 'no general table exists' in txt and 'reassuring' not in txt and 'only ranks fits' in txt, 'D3 A-D wording')
for loader in ('bu_LoadDan300', 'bu_LoadDanBin'):
    h = new_h(); h.call('bu_Init'); h.call(loader); h.press('Esc'); h.call('bu_DataPage')
    txt = ' '.join(t.text for t in h.texts)
    check('1980-1990' in txt and '1985 prices' in txt and 'inflation-adjusted' in txt and 'excess over 1M DKK' in txt and 'McNeil (1997)' in txt, 'D3 Danish source lines %s' % loader)
    layout(h, 'D3 ' + loader)
check('tail is not heavy' not in src, 'D3 "not heavy" wording gone')


# ================================================================== PART E (beta 1b)
import types


def pyblock(path=None):
    t = open(path or PROG, encoding='utf-8').read()
    m = re.search(r'^#PYTHON bul\n(.*?)^#END', t, re.S | re.M)
    return m.group(1)


def exports(path=None):
    """The program's EXPORTed variables (EXPORT NAME; at the start of a line) -- all hpprime.eval can see."""
    t = open(path or PROG, encoding='utf-8').read()
    return set(re.findall(r'^EXPORT\s+(\w+)\s*;', t, re.M))


class Store:
    """A stand-in for the PPL side: names -> numbers / lists / strings; hpprime.eval's text.
    beta 1f: STRICT -- only EXPORTed names are visible, as on the calculator (Lessons section 9).
    Reading any other name returns the name as text (float() of it then raises ValueError, the
    beta 1e failure on the device); assigning to one raises NameError."""
    def __init__(self, g, allowed):
        self.g = g
        self.allowed = allowed
        self.evals = 0
        self.refused = []

    def _see(self, name, write=False):
        if name in self.allowed:
            return True
        self.refused.append(name)
        if write:
            raise NameError('hpprime.eval: ' + name + ' is not an exported variable')
        return False

    FAULT_AT = None          # Part K: raise at the n-th call that is not a BU_PZ mark
    DROP_SENTINEL = False    # Part K: an answer without its sentinel

    def eval(self, s):
        self.evals += 1
        if not s.startswith('BU_PZ:='):
            self.nz = getattr(self, 'nz', 0) + 1
            if Store.FAULT_AT is not None and self.nz == Store.FAULT_AT:
                raise RuntimeError('injected fault at call %d' % self.nz)
        m = re.match(r'^(\w+)\((\d+)\):=(.*)$', s)
        if m:
            self._see(m.group(1), True)
            if Store.DROP_SENTINEL and m.group(1) == 'BU_OUT' and m.group(2) == '12':
                return 0
            v = m.group(3)
            assert re.match(r'^-?\d+\.\d{12}(E-?\d+)?$', v) or re.match(r'^-?\d+$', v), v   # fixed decimals, a capital-E mantissa form, or a whole number (a pixel row)
            self.g[m.group(1)][int(m.group(2)) - 1] = float(v)
            return 0
        m = re.match(r'^(\w+):=(.*)$', s)
        if m:
            self._see(m.group(1), True)
            v = m.group(2)
            self.g[m.group(1)] = v[1:-1] if v.startswith('"') else float(v)
            return 0
        m = re.match(r'^SIZE\((\w+)\)$', s)
        if m:
            if not self._see(m.group(1)):
                return 'SIZE(' + m.group(1) + ')'
            return float(len(self.g[m.group(1)]))
        m = re.match(r'^(\w+)\((\d+)\)$', s)
        if m:
            if not self._see(m.group(1)):
                return s
            return self.g[m.group(1)][int(m.group(2)) - 1]
        if not self._see(s):
            return s
        return self.g[s]


def run_block(g, path=None):
    """Run the block; an exception that escapes it is what the calculator prints on the screen as a
    traceback (it does not raise a PPL error), so it is caught here and returned, not raised."""
    hp = types.ModuleType('hpprime')
    st = Store(g, exports(path))
    hp.eval = st.eval
    hp.fillrect = lambda *a: None
    sys.modules['hpprime'] = hp
    ns = {'__name__': 'bul'}
    st.traceback = None
    try:
        exec(compile(pyblock(path), 'bul', 'exec'), ns)
    except Exception as e:                     # the traceback that would flash on the screen
        st.traceback = '%s: %s' % (type(e).__name__, e)
    return st


class Bridge(Harness):
    """PYTHON(bul) runs the real block against this harness's PPL globals."""
    python_ok = True

    def __init__(self, path, *a, **k):
        super().__init__(path, *a, **k)
        self.prog = path
        self.tracebacks = []                   # beta 1f: what the calculator would have printed
        self.refused = []                      # names the strict stub refused
        self.sentinels = []                    # BU_OUT(12) after each block run

    def _python(self, a):
        self.log.append(('PYTHON', a))
        if not self.python_ok:
            return 0.0
        st = run_block(self.globals_, self.prog)
        if st.traceback:
            self.tracebacks.append(st.traceback)
        self.refused.extend(st.refused)
        self.sentinels.append(self.globals_['BU_OUT'][11])
        return 0.0


def new_b(python_ok=True, **kw):
    kw.setdefault('strict', False)
    kw.setdefault('idle_key', 4)
    kw.setdefault('cas', 'fail')
    h = Bridge(PROG, **kw)
    h.python_ok = python_ok
    h._table['RANDSEED'] = lambda a, site: (h.rng.seed(int(a[0])), 0.0)[1]
    return h


print('E1 the Python block under CPython against the PPL engine (same C, K, S, ln L, SEs)')
check(re.search(r'^\s*import (?!hpprime)', pyblock(), re.M) is None and 'from math import' in pyblock(), 'E1 only math and hpprime imported at the top')
check(re.search(r'(?<![\w%.])f["\']', pyblock()) is None and 'numpy' not in pyblock(), 'E1 no f-strings, no numpy (MicroPython 1.9.4)')
E_SETS = [('BJS', 'bu_LoadBJS', None), ('Rossi', 'bu_LoadRossi', None), ('Danish300', 'bu_LoadDan300', None), ('DanishBin', 'bu_LoadDanBin', None)]
E_SETS += [(n, None, x) for n, _, x in rand_samples]
for name, loader, x in E_SETS:
    # the PPL engine alone
    hp_ = new_h(app_data={'D1': x} if loader is None else None)
    hp_.call('bu_Init')
    hp_.globals_['buEng'] = 2.0
    if loader:
        hp_.call(loader)
    else:
        hp_.call('bu_LoadMine')
    hp_.call('bu_Fit')
    gp = hp_.globals_
    # the Python engine, through the bridge, Auto
    hb = new_b(app_data={'D1': x} if loader is None else None)
    hb.call('bu_Init')
    if loader:
        hb.call(loader)
    else:
        hb.call('bu_LoadMine')
    hb.call('bu_Fit')
    gb = hb.globals_
    check(hb.error is None and hp_.error is None, 'E1 %s runtime error %s %s' % (name, hb.error, hp_.error))
    check(gb['buEngUsed'] == 1 and gb['BU_ENGINE'] == 'MicroPython 1.9.4', 'E1 %s Python answered (engine %r, BU_PZ %r)' % (name, gb['BU_ENGINE'], gb['BU_PZ']))
    check(gb['BU_OUT'][11] == 1.0 and str(gb['BU_PZ']).startswith('finished mode'), 'E1 %s sentinel and mark: %r' % (name, gb['BU_PZ']))
    for key in ('buFC', 'buFK', 'buFS', 'buFLL', 'buFlag', 'buSEOK', 'buSE1', 'buSE2', 'buSE3', 'buEvals'):
        a_, b_ = gb[key], gp[key]
        check(abs(a_ - b_) <= 1e-6 * max(1e-300, abs(b_)) or (key in ('buSE1', 'buSE2', 'buSE3') and gp['buSEOK'] == 0), 'E1 %s %s Python %r vs PPL %r' % (name, key, a_, b_))
    print('   %-10s flag=%d  Python C=%.8g K=%.6g S=%.8g lnL=%.8f  PPL lnL=%.8f  evals %d/%d' % (name, gb['buFlag'], gb['buFC'], gb['buFK'], gb['buFS'], gb['buFLL'], gp['buFLL'], gb['buEvals'], gp['buEvals']))

print('E2 the four engine settings with Python answering, and the pages')
for eng, want_badge in ((1, 'engine: MicroPython 1.9.4, '), (2, 'engine: PPL (chosen), '), (3, 'engine: MicroPython 1.9.4, '), (4, 'engine: MicroPython 1.9.4 (compared), ')):
    h = new_b()
    h.call('bu_Init')
    h.globals_['buEng'] = float(eng)
    h.call('bu_LoadBJS')
    h.call('bu_Fit')
    g = h.globals_
    check(h.error is None and g['buFitOK'] == 1, 'E2 engine %d fit error %s' % (eng, h.error))
    check(rel(g['buFLL'], -191.13744507805, 1e-9), 'E2 engine %d lnL %r' % (eng, g['buFLL']))
    h.press('Esc')
    h.call('bu_Results')
    txt = ' '.join(t.text for t in h.texts)
    check(want_badge in txt, 'E2 engine %d badge: %s' % (eng, [t.text for t in h.texts if t.text.startswith('engine')]))
    check(re.search(r'engine: [^,]+, \d+\.\d s', txt) is not None, 'E2 engine %d badge has a time to a tenth' % eng)
    if eng == 4:
        check('same C, K, S to 6 digits' in txt and re.search(r'Py \d+\.\d s, PPL \d+\.\d s:', txt), 'E2 Both line: %s' % g['buCmp'])
    check('engine: ' in str(g['buSum']) and ' s)' in str(g['buSum']), 'E2 engine %d summary carries the engine: %s' % (eng, g['buSum']))
    layout(h, 'E2 engine %d results' % eng)

print('E3 Python absent (the plain harness): Auto falls back, PPL runs, Python only fails cleanly, Both reports')
for eng in (1, 2, 3, 4):
    h = new_h()
    h.call('bu_Init')
    h.globals_['buEng'] = float(eng)
    h.call('bu_LoadBJS')
    r = h.call('bu_Fit')
    g = h.globals_
    check(h.error is None, 'E3 engine %d runtime error %s' % (eng, h.error))
    if eng == 3:
        check(r == 0 and g['buFitOK'] == 0 and any('Python engine failed' in ' '.join(m.lines) for m in h.msgboxes), 'E3 Python only reports the failure: %s' % [m.lines for m in h.msgboxes])
        continue
    check(r == 1 and g['buEngUsed'] == 2 and rel(g['buFLL'], -191.13744507805, 1e-9), 'E3 engine %d PPL answered' % eng)
    h.press('Esc')
    h.call('bu_Results')
    txt = ' '.join(t.text for t in h.texts)
    if eng == 2:
        check('engine: PPL (chosen), ' in txt and g['BU_ENGINE'] == 'PPL (chosen)', 'E3 PPL only badge')
    else:
        check('engine: PPL (Python unavailable), ' in txt and g['BU_ENGINE'] == 'PPL (Python unavailable)', 'E3 engine %d fallback badge' % eng)
    if eng == 4:
        check(g['buCmp'].startswith('Python failed (BU_PZ in Home); PPL alone ') and 'PPL alone' in txt, 'E3 Both reports the failure: %r' % g['buCmp'])
    layout(h, 'E3 engine %d results' % eng)
# the Both line when Python disagrees (a doctored block answer) falls back, Auto
h = new_b()
h.call('bu_Init')
h.call('bu_LoadBJS')
orig = Bridge._python
def bad_python(self, a):
    orig(self, a)
    self.globals_['BU_OUT'][3] = self.globals_['BU_OUT'][3] + 1.0     # a wrong ln L
Bridge._python = bad_python
h.call('bu_Fit')
check(h.globals_['buEngUsed'] == 2 and h.globals_['BU_ENGINE'] == 'PPL (Python unavailable)', 'E3 a disagreeing Python answer is refused (Auto falls back)')
Bridge._python = orig

print('E4 the engine menu, help page 4 and the Home summary through the menus')
h, res = run([('c', 'Fit my data'), ('c', 'Engine'), ('c', 'PPL only'), ('c', 'Fit my data'), ('c', 'BJS'), ('k', 'Enter'), ('s', 6), ('s', 5),
              ('c', 'Help'), ('k', 'Right'), ('k', 'Right'), ('k', 'Right'), ('k', 'Right'), ('c', 'Quit')])
layout(h, 'E4 menus')
T = [page_text(p) for p in h.pages]
check(any('engine: PPL (chosen), ' in t for t in T), 'E4 PPL-only badge after the menu choice')
check(any(t.startswith('BurrLab help (4 of 4)') and 'SAME algorithm' in t for t in T), 'E4 help page 4')
check('engine: PPL (chosen)' in res, 'E4 summary: %s' % res)
check(any('Engine (now: PPL only)' in d.items[6] for d in h.chooses if len(d.items) >= 7), 'E4 the fit menu shows the setting')


print('G the Explore soft keys select, visibly (strip tap through the polling loop)')
for slot, name in ((1, 'C'), (2, 'K'), (3, 'S'), (4, 'x₀')):
    h, res = run([('c', 'Explore'), ('s', slot), ('k', 'Esc'), ('c', 'Quit')])
    T = [page_text(p) for p in h.pages if page_text(p).startswith('C = ')]
    check(len(T) >= 2 and T[-1].count(name + ' chosen: arrows/drag') == 1, 'G soft key %d selects %s: %s' % (slot, name, T[-1][-80:] if T else None))
    last = h.pages[-1] if h.pages else None
# the inverted box: a white RECT_P in the title band on the chosen piece
h, res = run([('c', 'Explore'), ('s', 2), ('k', 'Esc'), ('c', 'Quit')])
scr = [p for p in h.pages if page_text(p).startswith('C = ')][-1]
boxes = [s for s in scr.shapes if str(s).startswith('RECT_P(') and ', 1.0,' in str(s) and ', 17.0,' in str(s)]
check(len(boxes) == 1, 'G one inverted box in the title band: %s' % boxes)
kx = [t.x for t in scr.texts if t.text.startswith('K = ')]
check(kx and abs(float(str(boxes[0]).split('(')[1].split(',')[0]) - (kx[0] - 3)) < 0.01, 'G the box sits under the K piece')
# a key with a visible effect on every page: the simulation speed shows in the status row
h = new_h(); h.call('bu_Init'); h.rng = random.Random(3)
h.tap(SK[2], 230, anytime=True); h.press('Esc', anytime=True)
h.call('bu_Sim')
check(any('(x100)' in t.text for t in h.texts), 'G the x100 soft key shows in the simulation status')


# ================================================================== PART H (beta 1d)
print('H the Explore redraw against beta 1c, pixel for pixel, and its cost')


class Count(Harness):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.nstmt = 0

    def _stmt(self, s, frame):
        self.nstmt += 1
        return super()._stmt(s, frame)


def prims(h):
    c = collections.Counter(str(e[0]) for e in h.log if isinstance(e, tuple))
    return {k: v for k, v in c.items() if k in ('LINE_P', 'PIXON_P', 'RECT_P', 'TEXTOUT_P', 'BLIT_P', 'FILLPOLY_P', 'DIMGROB_P')}


def explore_h(prog, C, K, S, x0, view=0):
    h = Count(prog, strict=False, idle_key=4, cas='fail')
    h.call('bu_Init')
    g = h.globals_
    g['buPB'] = 153.0; g['buSK'] = [["C", "K", "S", "x0", "CDF", "More"], ["Reset", "Help", "", "", "Menu", "More"]]
    g['buC'], g['buK'], g['buS'], g['buX0'], g['buView'] = float(C), float(K), float(S), float(x0), float(view)
    g['buRe'] = 1.0; g['buXmax'] = 0.0
    if 'buFrX' in g:
        g['buFrX'] = -1.0; g['buBase'] = 0.0
    h.reset_records(); h.nstmt = 0
    h.execute('bu_DrawExp()')
    return h


def curve_cols(h, colour, stride_hint):
    """column -> y of the curve from the LINE_P log (any grob); a stride-2 segment's middle
    column is the Bresenham midpoint, which LINE_P draws."""
    ys = {}
    for e in h.log:
        if isinstance(e, tuple) and e[0] == 'LINE_P' and len(e[1]) >= 6 and int(e[1][5]) == colour:
            x1, y1, x2, y2 = [int(round(v)) for v in e[1][1:5]]
            if x1 == x2:
                continue
            if y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    ys[x] = y1                      # a run (beta 1d) or a flat step
            else:
                ys[x1] = y1; ys[x2] = y2
    return ys


BLUE = 0x003CC8; MAG = 0xC800C8
cases = [(2, 1.5, 10, 15, 0), (2, 1.5, 10, 15, 1), (10.84, 0.898, 150.14, 180, 0), (1.183, 1.079, 0.825, 4.5, 0),
         (0.5, 0.7, 3, 2, 0), (0.25, 4, 100, 50, 0), (30, 30, 1, 1.2, 0), (1, 1, 1, 0.5, 1), (0.2, 0.2, 0.01, 0.3, 0),
         (4, 0.3, 20, 60, 0), (1.5, 1, 10, 20, 1), (2, 2, 10, 15, 0), (50, 50, 1, 1, 0), (5, 5, 10, 10, 0)]
worst = 0


def poly_pts(h, colour):
    """beta 1i: the polyline's points and segments from the LINE_P log (the curve colour on G1 or G4;
    a vertical of that colour is a marker, not the curve)."""
    pts, segs = {}, []
    for e in h.log:
        if isinstance(e, tuple) and e[0] == 'LINE_P' and len(e[1]) >= 6 and int(e[1][5]) == colour and str(e[1][0]) in ('G1', 'G4'):
            x1, y1, x2, y2 = [int(round(v)) for v in e[1][1:5]]
            if x1 == x2:
                continue
            segs.append((x1, y1, x2, y2)); pts[x1] = y1; pts[x2] = y2
    return pts, segs


def between_dev(segs, yc, xmin, skip):
    """the largest gap, in pixels, between the straight line through two points (the rows LINE_P lights
    in a column) and beta 1c's row there"""
    dev = 0.0
    for x1, y1, x2, y2 in segs:
        for x in range(x1, x2 + 1):
            if x not in yc or x < xmin or skip(x):
                continue
            lo = y1 + (y2 - y1) * (x - 0.5 - x1) / (x2 - x1); hi = y1 + (y2 - y1) * (x + 0.5 - x1) / (x2 - x1)
            a_, b_ = max(min(lo, hi), min(y1, y2)), min(max(lo, hi), max(y1, y2))
            d = 0.0 if a_ - 0.5 <= yc[x] <= b_ + 0.5 else min(abs(yc[x] - a_), abs(yc[x] - b_))
            dev = max(dev, d)
    return dev


def want_cols(C, K, S, xmax, nc=268):
    """the point columns bu_CachePPL must use: 1, 4, ..., the last, and the pdf peak's two (C > 1)"""
    w = set(min(nc, 1 + 3 * i) for i in range((nc + 1) // 3 + 1))
    if C > 1:
        km = int(S * math.exp(math.log((C - 1) / (K * C + 1)) / C) / (xmax / nc))
        for k in (km, km + 1):
            if 4 <= k < nc and km >= 4:
                w.add(k)
    return w


for C, K, S, x0, view in cases:
    hc = explore_h(PROG_C, C, K, S, x0, view)
    hd = explore_h(PROG, C, K, S, x0, view)
    col = MAG if view else BLUE
    yc = curve_cols(hc, col, 1)
    gc, gd = hc.globals_, hd.globals_
    pts, segs = poly_pts(hd, col)
    xc = 36 + int(x0 / gd['buXmax'] * 268)
    near = lambda x: abs(x - xc) <= 4                                   # the x0 dot's own short lines
    want = set(36 + k for k in want_cols(C, K, S, gd['buXmax']))
    check(set(pts) == want and int(gd['buNPt']) == len(want) and len(gd['buPts']) >= 2 * len(want),
          'H point columns C=%g K=%g S=%g: %d points, want %d (%s)' % (C, K, S, len(pts), len(want), sorted(set(pts) ^ want)[:6]))
    dpt = max([abs(pts[x] - yc[x]) for x in pts if x in yc and not near(x)] or [99])
    check(dpt == 0, "H every point on beta 1c's rows C=%g K=%g S=%g view %d: max %d px" % (C, K, S, view, dpt))
    dev = between_dev(segs, yc, 36 + 6, near)
    worst = max(worst, dev)
    check(dev <= 2, "H the line between points within 2 px of beta 1c's curve C=%g K=%g S=%g view %d: %.1f px" % (C, K, S, view, dev))
    # the texts: the same, apart from the timing readout
    tc = sorted(set(t.text for t in hc.texts if t.text.strip() and not re.match(r'K×C = [0-9.]+: (mean and variance|mean, no variance|NO mean)$', t.text)))   # beta 1e dropped the in-frame line
    td = sorted(set(t.text for t in hd.texts if t.text.strip() and not re.match(r'c \d+ d \d+ w \d+ ms', t.text)))
    check(tc == td, 'H same texts at C=%g K=%g S=%g: %s' % (C, K, S, [t for t in tc if t not in td][:3] + [t for t in td if t not in tc][:3]))
    if view == 0:
        check(abs(gc['buYmax'] - gd['buYmax']) <= 1e-9 * gc['buYmax'], 'H y scale identical C=%g K=%g S=%g: %r vs %r' % (C, K, S, gc['buYmax'], gd['buYmax']))
print('   worst gap between the polyline and beta 1c over %d cases: %.1f px' % (len(cases), worst))
# the cost: statements and primitives per redraw, before and after
hc = explore_h(PROG_C, 2, 1.5, 10, 15); hd = explore_h(PROG, 2, 1.5, 10, 15)
for h_, nm in ((hc, 'beta 1c'), (hd, 'beta 1d')):
    h_.globals_['buRe'] = 1.0; h_.reset_records(); h_.nstmt = 0; h_.execute('bu_DrawExp()')
    print('   %s param redraw: %d statements, primitives %s' % (nm, h_.nstmt, prims(h_)))
    if nm == 'beta 1c':
        s_c, p_c = h_.nstmt, sum(prims(h_).values())
    else:
        s_d, p_d = h_.nstmt, sum(prims(h_).values())
    h_.globals_['buX0'] = 16.0; h_.reset_records(); h_.nstmt = 0; h_.execute('bu_DrawExp()')
    print('   %s x0 move:      %d statements, primitives %s' % (nm, h_.nstmt, prims(h_)))
    if nm == 'beta 1d':
        sx_d, px_d = h_.nstmt, sum(prims(h_).values())
check(s_d <= 5000 and s_d * 2.2 <= s_c, 'H statements per param redraw %d (beta 1c %d)' % (s_d, s_c))
hh = explore_h(PROG_H, 2, 1.5, 10, 15); hh.globals_['buRe'] = 1.0; hh.reset_records(); hh.nstmt = 0; hh.execute('bu_DrawExp()')
print('   beta 1h param redraw: %d statements; beta 1i %d (%.0f %%)' % (hh.nstmt, s_d, 100.0 * s_d / hh.nstmt))
check(s_d * 2 <= hh.nstmt, "H beta 1i: a param redraw takes at most half of beta 1h's statements (%d vs %d)" % (s_d, hh.nstmt))
check(p_d * 3 <= p_c and px_d <= 25, 'H primitives per redraw %d / x0 move %d (beta 1c %d)' % (p_d, px_d, p_c))
check(not any(e[0] == 'PIXON_P' for e in hd.log if isinstance(e, tuple)), 'H no PIXON_P in a redraw')
hd.globals_['buTimOn'] = 1.0; hd.reset_records(); hd.execute('bu_DrawExp()')
check(any(re.match(r'c \d+ d \d+ w \d+ ms, ', t.text) for t in hd.texts), 'H the timing readout is on the page when toggled on')
# the cache invalidation: a view toggle, a parameter step, a reset through the page loop
h, res = run([('c', 'Explore'), ('s', 5), ('k', 'Up'), ('s', 5), ('k', 'Right'), ('s', 6), ('s', 1), ('k', 'Esc'), ('c', 'Quit')])
layout(h, 'H explore loop')
T = [page_text(p) for p in h.pages if page_text(p).startswith('C = ')]
check(any('CDF' in t for t in T) and any('C = 2.10' in t for t in T) and 'C = 2.00 K = 1.50 S = 10.00' in T[-1], 'H view toggle, step and reset through the loop: %s' % T[-1][:60])
# no fixed pause in the arrow path: no WAIT(n > 0) and no TICKS-capped loop in bu_Explore / bu_DrawExp
src_d = open(PROG, encoding='utf-8').read()
seg = src_d[src_d.index('bu_Explore()\nBEGIN'):src_d.index('// 2. FAMILY TREE')]
check('WAIT(' not in seg and 'TICKS - ' not in seg.replace('buTWait := TICKS - buTEv', ''), 'H no WAIT or capped wait in the Explore loop')
# the Family and Rare pages: cost
h2 = Count(PROG, strict=False, idle_key=4, cas='fail'); h2.call('bu_Init')
h2.globals_['buPB'] = 153.0; h2.call('bu_LoadBJS'); h2.call('bu_Fit')
h2.reset_records(); h2.nstmt = 0; h2.execute('bu_DrawRare(200, 230)')
print('   Rare draw: %d statements, primitives %s' % (h2.nstmt, prims(h2)))
check(h2.nstmt <= 5000, 'H Rare redraw statements %d' % h2.nstmt)


# ================================================================== PART I (beta 1e)
print('I the Explore curves from the Python engine against the PPL cache')


class CountB(Bridge):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.nstmt = 0

    def _stmt(self, s, frame):
        self.nstmt += 1
        return super()._stmt(s, frame)


def explore_b(C, K, S, x0, view=0, eng=3, python_ok=True, timing=0, prog=None):
    h = CountB(prog or PROG, strict=False, idle_key=4, cas='fail')
    h.python_ok = python_ok
    h.call('bu_Init')
    g = h.globals_
    g['buPB'] = 153.0; g['buSK'] = [["C", "K", "S", "x0", "CDF", "More"], ["Reset", "Help", "Timing", "", "Menu", "More"]]
    g['buC'], g['buK'], g['buS'], g['buX0'], g['buView'] = float(C), float(K), float(S), float(x0), float(view)
    g['buRe'] = 1.0; g['buXmax'] = 0.0; g['buFrX'] = -1.0; g['buBase'] = 0.0; g['buEng'] = float(eng); g['buTimOn'] = float(timing)
    h.reset_records(); h.nstmt = 0
    h.execute('bu_DrawExp()')
    return h


for C, K, S, x0, view in cases:
    hp = explore_b(C, K, S, x0, view, eng=2)                 # PPL only
    hy = explore_b(C, K, S, x0, view, eng=3)                 # beta 1h: Python only (Auto now draws curves in PPL)
    check(hy.globals_['buCEng'] == 1 and hp.globals_['buCEng'] == 2, 'I engines C=%g K=%g S=%g: py %r PPL %r' % (C, K, S, hy.globals_['buCEng'], hp.globals_['buCEng']))
    check(str(hy.globals_['BU_PZ']) == 'finished mode 5', 'I mark: %r' % hy.globals_['BU_PZ'])
    check(not hy.tracebacks and not hy.refused, 'I strict stub: no traceback, no unexported name C=%g K=%g S=%g (%r %r)' % (C, K, S, hy.tracebacks, sorted(set(hy.refused))))
    pp, py = hp.globals_['buPts'], hy.globals_['buPts']
    check(hp.globals_['buNPt'] == hy.globals_['buNPt'] and all(int(a) == int(b) for a, b in zip(pp, py)), 'I points equal, Python vs PPL C=%g K=%g S=%g (%d vs %d)' % (C, K, S, hp.globals_['buNPt'], hy.globals_['buNPt']))
    check(abs(hp.globals_['buYmax'] - hy.globals_['buYmax']) <= 1e-9 * hp.globals_['buYmax'], 'I y scale equal C=%g K=%g S=%g' % (C, K, S))
    col = MAG if view else BLUE
    yp, yy = curve_cols(hp, col, 1), curve_cols(hy, col, 1)
    check(yp == yy, 'I curve pixel-identical with Python vs PPL C=%g K=%g S=%g' % (C, K, S))
    # the values behind the rows: Python's pdf at column 10 (BU_OUT(2)) against the PPL formula to 1E-9,
    # and every column's value re-derived here against scipy to 1E-9
    xs = [k * hy.globals_['buXmax'] / 268 for k in range(1, 269)]
    ref = (stats.burr12.cdf if view else stats.burr12.pdf)(np.array(xs), C, K, scale=S)
    check(rel(hy.globals_['BU_OUT'][1], ref[9], 1e-9), 'I Python column 10 value vs scipy C=%g K=%g S=%g' % (C, K, S))
    ym = 1.0 if view else hy.globals_['buYmax']
    rows_ref = {36 + k + 1: 153 - int(min(1.0, v / ym) * 117) for k, v in enumerate(ref)}
    ptsy, _ = poly_pts(hy, col)                                    # beta 1i: compare at the points
    off = sum(1 for x, y in ptsy.items() if x in rows_ref and y != rows_ref[x])
    check(off <= 2, 'I Python curve vs scipy-derived rows C=%g K=%g S=%g: %d columns differ (rounding edges)' % (C, K, S, off))
    hc = explore_h(PROG_C, C, K, S, x0, view)
    yc = curve_cols(hc, col, 1)
    xc = 36 + int(x0 / hy.globals_['buXmax'] * 268)
    check(all(yc[x] == ptsy[x] for x in ptsy if x in yc and abs(x - xc) > 4) and len(set(yc) & set(ptsy)) >= 85, "I Python's points on beta 1c's rows C=%g K=%g S=%g" % (C, K, S))
    tp = sorted(set(t.text for t in hp.texts if t.text.strip())); ty = sorted(set(t.text for t in hy.texts if t.text.strip()))
    check(tp == ty, 'I same texts either engine C=%g K=%g S=%g' % (C, K, S))
# the readout names the engine, in each setting, with Python answering and absent
for eng, ok, want in ((1, True, ', PPL'), (2, True, ', PPL'), (3, True, ', py'), (4, True, ', py = PPL'), (1, False, ', PPL'), (2, False, ', PPL'), (3, False, ', py FAIL, PPL'), (4, False, ', py FAIL, PPL')):
    h = explore_b(2, 1.5, 10, 15, 0, eng=eng, python_ok=ok, timing=1)
    txt = [t.text for t in h.texts if re.match(r'c \d+ d \d+ w \d+ ms, ', t.text)]
    check(len(txt) == 1 and txt[0].endswith(want), 'I readout engine %d python %s: %s' % (eng, ok, txt))
    check(h.error is None and h.globals_['buYmax'] > 0, 'I engine %d python %s drew the page' % (eng, ok))
    layout(h, 'I readout engine %d python %s' % (eng, ok))
# Both with a disagreeing Python answer shows the difference; a broken answer is refused
orig = Bridge._python
def bad(self, a):
    orig(self, a)
    if int(self.globals_['BU_JOB']) == 5:
        self.globals_['BU_YP'][5] = self.globals_['BU_YP'][5] + 3.0
Bridge._python = bad
h = explore_b(2, 1.5, 10, 15, 0, eng=4, timing=1)
check(h.globals_['buCEng'] == 4 and any('py-PPL' in t.text for t in h.texts), 'I Both reports a column that differs: %r' % h.globals_['buCDiff'])
def bad2(self, a):
    orig(self, a)
    if int(self.globals_['BU_JOB']) == 5:
        self.globals_['BU_OUT'][1] = -5.0
Bridge._python = bad2
h = explore_b(2, 1.5, 10, 15, 0, eng=3, timing=1)
check(h.globals_['buCEng'] == -1 and any('py FAIL, PPL' in t.text for t in h.texts), 'I a wrong column 10 is refused (Auto falls back)')
Bridge._python = orig
# the cost with Python answering: statements per arrow press
h = explore_b(2, 1.5, 10, 15, 0, eng=3); h.globals_['buRe'] = 1.0; h.reset_records(); h.nstmt = 0; h.execute('bu_DrawExp()')
print('   beta 1f param redraw, Python answering: %d PPL statements, primitives %s' % (h.nstmt, prims(h)))
check(h.nstmt < 1000, 'I PPL statements per redraw with Python answering: %d' % h.nstmt)
# the Family animation and the Rare page take the same path
h = CountB(PROG, strict=False, idle_key=4, cas='fail'); h.call('bu_Init'); h.globals_['buPB'] = 153.0
h.press('Esc', anytime=True); h.call('bu_Family')
check(h.error is None and h.globals_['buCEng'] == 2, 'I beta 1h: the Family page cache is PPL in Auto (%r)' % h.globals_['buCEng'])
h = CountB(PROG, strict=False, idle_key=4, cas='fail'); h.call('bu_Init'); h.globals_['buPB'] = 153.0
h.call('bu_LoadBJS'); h.call('bu_Fit'); h.press('Esc'); h.call('bu_Rare')
check(h.error is None and h.globals_['buCEng'] == 2, 'I beta 1h: the Rare page cache is PPL in Auto (%r)' % h.globals_['buCEng'])
# the Timing toggle through the page loop
h, res = run([('c', 'Explore'), ('s', 6), ('s', 3), ('k', 'Up'), ('s', 3), ('k', 'Esc'), ('c', 'Quit')])
layout(h, 'I timing toggle')
T = [page_text(p) for p in h.pages if page_text(p).startswith('C = ')]
check(any(re.search(r'c \d+ d \d+ w \d+ ms, PPL', t) for t in T) and not re.search(r' ms, ', T[-1]), 'I Timing soft key toggles the readout')

# ================================================================== PART J (beta 1f)
print('J the bridge reads only EXPORTed names (the beta 1e device failure)')
EXP = exports()
blk = pyblock()
used = set()
for pat in (r'num\("(\w+)', r'getlist\("(\w+)', r'putel\("(\w+)', r'putsci\("(\w+)', r'ev\(["\'](\w+)', r'"(\w+)\("\s*\+'):
    used |= set(re.findall(pat, blk))
used |= set(re.findall(r'(?:putel|putsci)\((\w+),', blk)) - {'name'}
used -= {'SIZE'}                                                     # SIZE(BU_X): the built-in, applied to an exported name
print('   names the block hands to hpprime.eval: %s' % ', '.join(sorted(used)))
check(used and used <= EXP and all(n.startswith('BU_') for n in used), 'J every name the block reads or writes is EXPORTed and BU_: %s' % sorted(used - EXP))
check(EXP >= {'BU_JOB', 'BU_IN', 'BU_X', 'BU_GE', 'BU_GC', 'BU_OUT', 'BU_YP', 'BU_PZ'}, 'J the bridge variables are all EXPORTed')
check(not re.search(r'\bbu[A-Z]\w*', blk.split('def run():')[0].split('\n', 1)[1] if 'def run():' in blk else blk), 'J no file-level LOCAL (buXxx) named anywhere in the block')
# the strict stub catches beta 1e's bug: its mode 5 reads buPB/buPT/buPL and dies with a traceback
he = explore_b(2, 1.5, 10, 15, 0, eng=1, timing=1, prog=PROG_E)
check(he.tracebacks and 'ValueError' in he.tracebacks[0] and 'buPB' in he.refused and he.globals_['buCEng'] == -1,
      'J beta 1e FAILS under the strict stub (the device error reproduced): %r, refused %r' % (he.tracebacks[:1], sorted(set(he.refused))))
check(any('py FAIL, PPL' in t.text for t in he.texts), 'J beta 1e under the strict stub: readout "py FAIL, PPL" (PPL drew it)')
# beta 1f under the same stub: every engine setting, fits and curves, no traceback and nothing refused
for eng in (3, 4):
    hf = explore_b(2, 1.5, 10, 15, 0, eng=eng, timing=1)
    check(not hf.tracebacks and not hf.refused and hf.globals_['buCEng'] in (1, 3), 'J beta 1f engine %d: Python answered under the strict stub (%r %r %r)' % (eng, hf.globals_['buCEng'], hf.tracebacks, sorted(set(hf.refused))))
for ld in ('bu_LoadBJS', 'bu_LoadRossi'):
    hf = new_b(); hf.call('bu_Init'); hf.call(ld); hf.call('bu_Fit')
    check(not hf.tracebacks and not hf.refused and hf.globals_['buEngUsed'] == 1, 'J beta 1f fit %s answered by Python under the strict stub (%r %r)' % (ld, hf.tracebacks, sorted(set(hf.refused))))
# an error inside the block is caught THERE: no traceback, BU_PZ "error: ...", BU_OUT(12) = -2, PPL draws
orig = Bridge._python
def short_in(self, a):
    if int(self.globals_['BU_JOB']) == 5:
        self.globals_['BU_IN'] = self.globals_['BU_IN'][:6]          # the beta 1e hand-off: 6 values
    return orig(self, a)
Bridge._python = short_in
for eng, want in ((3, ', py FAIL, PPL'),):
    hf = explore_b(2, 1.5, 10, 15, 0, eng=eng, timing=1)
    txt = [t.text for t in hf.texts if re.match(r'c \d+ d \d+ w \d+ ms, ', t.text)]
    check(not hf.tracebacks, 'J engine %d: the error was caught inside the block (no traceback): %r' % (eng, hf.tracebacks))
    check(str(hf.globals_['BU_PZ']).startswith('error: ') and hf.globals_['BU_OUT'][11] == -2, 'J engine %d: BU_PZ %r, BU_OUT(12) %r' % (eng, hf.globals_['BU_PZ'], hf.globals_['BU_OUT'][11]))
    check(hf.error is None and hf.globals_['buCEng'] == -1 and len(txt) == 1 and txt[0].endswith(want) and hf.globals_['buNPt'] > 0, 'J engine %d: PPL drew the page, readout %r' % (eng, txt))
def quote_err(self, a):                                              # a message with a double quote still marks cleanly
    if int(self.globals_['BU_JOB']) == 5:
        self.globals_['BU_IN'] = self.globals_['BU_IN'][:6]
    return orig(self, a)
Bridge._python = orig
hf = explore_b(2, 1.5, 10, 15, 0, eng=2, timing=1)
check(hf.globals_['buCEng'] == 2 and not any(r for r in hf.log if r[0] == 'PYTHON'), 'J PPL only never calls PYTHON (%r)' % hf.globals_['buCEng'])

# ================================================================== PART K (beta 1f)
print('K a Python failure at each step: back to an interactive page, bounded, fail once')


# beta 1h: Auto now draws the Explore/Family/Rare curves in PPL, so the curve-bridge fault
# tests below run against a copy of the program whose start-up engine is 3 (Python only),
# the setting in which the curve bridge is still used.  The copy differs in that one line.
PROGK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_BurrLab_beta1i_engine3.txt')
_src = open(PROG, encoding='utf-8').read()
assert _src.count('buEng := 1; buEngUsed := 0;') == 1
open(PROGK, 'w', encoding='utf-8', newline='').write(_src.replace('buEng := 1; buEngUsed := 0;', 'buEng := 3; buEngUsed := 0;'))
def run_b(steps, python_ok=True, seed=0, prog=None):
    h = CountB(prog or PROGK, strict=False, idle_key=4, cas='fail')
    h.python_ok = python_ok
    h._table['RANDSEED'] = lambda a, site: (h.rng.seed(int(a[0])), 0.0)[1]
    h.rng = random.Random(seed)
    h.press('Enter')
    for st in steps:
        if st[0] == 'c':
            h.choose(st[1])
        elif st[0] == 'k':
            h.press(st[1])
        elif st[0] == 's':
            h.tap(SK[st[1] - 1], 230)
    h.choose(0)
    res = h.call('BurrLab')
    return h, res


EXPL = [('c', 'Explore'), ('k', 'Up'), ('k', 'Up'), ('k', 'Down'), ('k', 'Esc'), ('c', 'Family'), ('k', 'Esc'), ('c', 'Explore'), ('k', 'Up'), ('k', 'Esc'), ('c', 'Quit')]
hb, rb = run_b(EXPL, python_ok=False)
base = hb.nstmt
npy = sum(1 for r in hb.log if r[0] == 'PYTHON')
print('   Python absent: %d PPL statements for the whole path, %d PYTHON() call(s)' % (base, npy))
check(hb.error is None and npy == 1, 'K Python absent: one PYTHON() call for the whole session, then PPL (%d)' % npy)
hg, rg = run_b(EXPL)
check(hg.error is None and not hg.tracebacks and all(v == 1 for v in hg.sentinels) and sum(1 for r in hg.log if r[0] == 'PYTHON') >= 5, 'K Python healthy: answers every redraw (%d calls)' % len(hg.sentinels))
orig = Bridge._python


def inject(kind):
    def f(self, a):
        g = self.globals_
        if int(g['BU_JOB']) == 5:
            if kind == 'nc':
                g['BU_IN'][4] = 1e9
            elif kind == 'nan':
                g['BU_IN'][0] = float('nan')
            elif kind == 'rows':
                g['BU_IN'][6] = 999.0
            elif kind == 'h0':
                g['BU_IN'][7] = g['BU_IN'][6]
            elif kind == 'view':
                g['BU_IN'][5] = 7.0
        if kind == 'absent':
            self.log.append(('PYTHON', a))
            return 0.0
        r = orig(self, a)
        if kind == 'garbage' and int(g['BU_JOB']) == 5:
            g['BU_OUT'][2] = 1e6
        return r
    return f


KINDS = [('nc', 'bad input: 1E9 columns', 'error: '), ('nan', 'bad input: C = NaN', 'error: '), ('rows', 'bad input: frame bottom 999', 'error: '),
         ('h0', 'bad input: zero frame height', 'error: '), ('view', 'bad input: view 7', 'error: '),
         ('exc2', 'exception reading BU_JOB', 'error: '), ('exc3', 'exception reading BU_IN', 'error: '), ('exc20', 'exception in the column loop region', 'error: '),
         ('exc80', 'exception while writing BU_YP', 'error: '), ('exc170', 'exception late in BU_YP', 'error: '),
         ('nosent', 'missing sentinel', 'finished mode 5'), ('garbage', 'sentinel with a wrong answer', 'finished mode 5'), ('absent', 'PYTHON() returns at once', '')]
for kind, label, pz in KINDS:
    Store.FAULT_AT = int(kind[3:]) if kind.startswith('exc') else None
    Store.DROP_SENTINEL = (kind == 'nosent')
    Bridge._python = inject(kind)
    h, res = run_b(EXPL)
    Store.FAULT_AT = None; Store.DROP_SENTINEL = False; Bridge._python = orig
    ncall = sum(1 for r in h.log if r[0] == 'PYTHON')
    expl = [page_text(p) for p in h.pages if page_text(p).startswith('C = ')]
    check(h.error is None and res is not None, 'K %s: the program ran to Quit (%s)' % (label, h.error))
    check(ncall == 1, 'K %s: fail once -- %d PYTHON() calls in the session' % (label, ncall))
    check(not h.tracebacks, 'K %s: nothing printed (no traceback): %r' % (label, h.tracebacks))
    check(str(h.globals_['BU_PZ']).startswith(pz), 'K %s: BU_PZ %r' % (label, h.globals_['BU_PZ']))
    if pz == 'error: ':
        check(h.sentinels[:1] == [-2.0], 'K %s: the block wrote the failure sentinel -2 (%r)' % (label, h.sentinels[:1]))
    check(len(expl) >= 5, 'K %s: interactive Explore pages after the failure (%d)' % (label, len(expl)))
    check(h.nstmt <= base * 1.05 + 500, 'K %s: bounded -- %d PPL statements vs %d with Python absent' % (label, h.nstmt, base))
ha, ra = run_b(EXPL, prog=PROG)
check(ha.error is None and sum(1 for r in ha.log if r[0] == 'PYTHON') == 0, 'K beta 1h: Auto makes no PYTHON() call on the Explore/Family path (%d)' % sum(1 for r in ha.log if r[0] == 'PYTHON'))
# a failure in the FIT (mode 1) also stops Python for the session; the Explore that follows is PPL
Store.FAULT_AT = 3
h, res = run_b([('c', 'Fit my data'), ('c', 'BJS'), ('k', 'Enter'), ('k', 'Esc'), ('c', 'Explore'), ('k', 'Up'), ('k', 'Esc'), ('c', 'Quit')], prog=PROG)   # beta 1h: Auto
Store.FAULT_AT = None
check(h.error is None and res is not None and sum(1 for r in h.log if r[0] == 'PYTHON') == 1 and not h.tracebacks and h.globals_['buFitOK'] == 1 and h.globals_['BU_ENGINE'] == 'PPL (Python unavailable)',
      'K a fit failure: PPL fitted, one PYTHON() call, no traceback (%d calls)' % sum(1 for r in h.log if r[0] == 'PYTHON'))
# choosing the engine again tries Python again
Store.FAULT_AT = 3
h = CountB(PROGK, strict=False, idle_key=4, cas='fail')   # beta 1h: Python only, where the curve bridge is used
h.call('bu_Init'); h.globals_['buRe'] = 1.0; h.execute('bu_Cache()')
Store.FAULT_AT = None
check(h.globals_['buPyBad'] == 1 and h.globals_['buCEng'] == -1, 'K after a failure buPyBad = 1')
h.globals_['buRe'] = 1.0; h.execute('bu_Cache()')
check(sum(1 for r in h.log if r[0] == 'PYTHON') == 1 and h.globals_['buCEng'] == -1, 'K the next redraw does not call PYTHON()')
h.globals_['buPyBad'] = 0.0                                              # what the Engine item does (checked in the source next)
src = open(PROG, encoding='utf-8').read()
check(re.search(r'IF fmE >= 1 AND fmE <= 4 THEN buEng := fmE; buPyBad := 0; END;', src) is not None, 'K choosing an engine clears buPyBad (source)')
h.globals_['buRe'] = 1.0; h.execute('bu_Cache()')
check(sum(1 for r in h.log if r[0] == 'PYTHON') == 2 and h.globals_['buCEng'] == 1, 'K after the engine is chosen again Python answers')
# no PPL loop waits on a Python result: every read of BU_OUT / BU_PZ / BU_YP is outside a WHILE / REPEAT condition
check(not re.search(r'(WHILE|UNTIL)[^;\n]*(BU_OUT|BU_PZ|BU_YP)', src), 'K no PPL loop condition reads BU_OUT, BU_PZ or BU_YP')

# ================================================================== beta 1h
# Auto draws the curves in PPL: no PYTHON() call on an Explore redraw at engine 1.
h = explore_b(2, 1.5, 10, 15, 0, eng=1, timing=1)
check(h.error is None and h.globals_['buCEng'] == 2 and h.globals_['buNPt'] > 0, 'beta 1h: Auto draws the curve by PPL (buCEng %r)' % h.globals_['buCEng'])

# ================================================================== PART L (beta 1i)
print('L the hourglass, the instant title, the point grid, the blink')


def g0(e):
    return isinstance(e, tuple) and len(e[1]) >= 1 and str(e[1][0]) == 'G0'


def hourglasses(log):
    return [i for i, e in enumerate(log) if isinstance(e, tuple) and e[0] == 'TRIANGLE_P' and g0(e)]


def g0_texts(log):
    return [(i, str(e[1][0])) for i, e in enumerate(log) if isinstance(e, tuple) and e[0] == 'TEXTOUT_P' and len(e[1]) > 1 and str(e[1][1]) == 'G0']


def first(log, pred, start=0):
    for i in range(start, len(log)):
        if pred(log[i]):
            return i
    return None


# L1 Explore: an Up press shows "C = 2.10" on the screen and the hourglass BEFORE the recompute draws
h, res = run([('c', 'Explore'), ('k', 'Up'), ('k', 'Esc'), ('c', 'Quit')])
L = h.log
menus = [i for i, e in enumerate(L) if isinstance(e, tuple) and e[0] == 'DRAWMENU']
check(len(menus) >= 2 and h.error is None, 'L1 two Explore frames drawn (%d)' % len(menus))
before_first = [i for i in hourglasses(L) if i < menus[0]]
check(not before_first and not [i for i, _ in g0_texts(L) if i < menus[0] and 'C = ' in str(L[i][1][0])],
      'L1 the first entry draws no early title or hourglass (it would sit over the main menu)')
hg = [i for i in hourglasses(L) if menus[0] < i < menus[1]]
tt = [i for i, e in enumerate(L) if menus[0] < i < menus[1] and isinstance(e, tuple) and e[0] == 'TEXTOUT_P' and len(e[1]) > 1 and str(e[1][1]) == 'G0' and str(e[1][0]) == 'C = 2.10']
curve = first(L, lambda e: isinstance(e, tuple) and e[0] == 'LINE_P' and len(e[1]) >= 6 and str(e[1][0]) == 'G4' and int(e[1][5]) == BLUE, menus[0])
check(len(hg) == 2 and tt and curve is not None and max(hg) < curve and tt[0] < curve,
      'L1 Up: "C = 2.10" and the hourglass on the screen before the curve is recomputed (%s %s %s)' % (hg, tt[:1], curve))
pg = [p for p in h.pages if page_text(p).startswith('C = 2.10')]
check(pg and not any('TRIANGLE_P' in str(s) for s in pg[-1].shapes), 'L1 the finished frame has no hourglass')
# L2 an x0 move (+) needs no recompute: no hourglass
h, res = run([('c', 'Explore'), ('k', 'Plus'), ('k', 'Esc'), ('c', 'Quit')])
menus = [i for i, e in enumerate(h.log) if isinstance(e, tuple) and e[0] == 'DRAWMENU']
check(h.error is None and not [i for i in hourglasses(h.log) if menus[0] < i < menus[1]], 'L2 an x0 step shows no hourglass')
# L3 a menu action that recomputes (Enter > Reset): the menu is not painted over before the new frame
h, res = run([('c', 'Explore'), ('k', 'Enter'), ('c', 'Reset C, K, S'), ('k', 'Esc'), ('c', 'Quit')])
menus = [i for i, e in enumerate(h.log) if isinstance(e, tuple) and e[0] == 'DRAWMENU']
check(h.error is None and len(menus) >= 2 and not [i for i in hourglasses(h.log) if menus[0] < i < menus[1]],
      'L3 after the Explore menu no early title or hourglass is painted over it')
# L4 Family: C+ shows the new title and the hourglass on the screen before the cache is refilled
h, res = run([('c', 'Family'), ('s', 2), ('k', 'Esc'), ('c', 'Quit')])
L = h.log
menus = [i for i, e in enumerate(L) if isinstance(e, tuple) and e[0] == 'DRAWMENU']
band = [i for i, e in enumerate(L) if len(menus) >= 2 and menus[0] < i < menus[1] and isinstance(e, tuple) and e[0] == 'TEXTOUT_P' and len(e[1]) > 1 and str(e[1][1]) == 'G0' and str(e[1][0]).startswith('Family: C = 2.10')]
hg = [i for i in hourglasses(L) if len(menus) >= 2 and menus[0] < i < menus[1]]
check(h.error is None and band and len(hg) == 2, 'L4 Family C+: the new title and the hourglass at once (%s %s)' % (band[:1], hg))
check(not [i for i in hourglasses(L) if i < menus[0]], 'L4 Family: nothing early on the first entry')
# L5 Rare: no hourglass for an x step that keeps the window
h, res = run([('c', 'Fit my data'), ('c', 'BJS'), ('k', 'Enter'), ('c', 'How rare is this?'), ('k', 'Right'), ('k', 'Esc'), ('k', 'Esc'), ('c', 'Quit')])
check(h.error is None, 'L5 the Rare path runs (%s)' % h.error)
# L6 the fit: the hourglass blinks, costs little, changes nothing.  The harness clock moves 1 ms a
# TICKS reading; here it moves with the work instead, 0.25 ms a statement (4,000 statements a second,
# the slow end of the G1's measured 4,000-6,500), so the blink is seen as the G1 would show it.
class G1Clock(Count):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.blinks = []

    def _ticks(self):
        if self._where() == 'bu_Blink':
            self.blinks.append(self.nstmt)
        return float(int(self.nstmt * 0.25))


fits = {}
for prog, nm in ((PROG_H, '1h'), (PROG, '1i')):
    for loader in ('bu_LoadBJS', 'bu_LoadDan300'):
        hf = G1Clock(prog, strict=False, idle_key=4, cas='fail'); hf.call('bu_Init')
        hf.globals_['buEng'] = 2.0                                       # PPL only: the long path
        hf.call(loader); hf.reset_records(); hf.nstmt = 0; hf.blinks = []; hf.call('bu_Fit')
        g = hf.globals_
        on = len(hourglasses(hf.log)) // 2
        clr = sum(1 for e in hf.log if isinstance(e, tuple) and e[0] == 'RECT_P' and g0(e) and int(e[1][1]) == 302) - on
        gaps = [b - a for a, b in zip([0] + hf.blinks, hf.blinks + [hf.nstmt])]
        fits[(nm, loader)] = (hf.nstmt, g['buFC'], g['buFK'], g['buFS'], g['buEvals'], on, clr, max(gaps) * 0.25 / 1000.0, hf.error)
for loader in ('bu_LoadBJS', 'bu_LoadDan300'):
    a_, b_ = fits[('1h', loader)], fits[('1i', loader)]
    secs = b_[0] * 0.25 / 1000.0
    print('   %s fit, PPL only: beta 1h %d statements, beta 1i %d (+%.2f %%), about %.0f s at 4,000/s; hourglass on %d, off %d; longest stretch without a blink check %.2f s' % (
        loader[7:], a_[0], b_[0], 100.0 * (b_[0] - a_[0]) / a_[0], secs, b_[5], b_[6], b_[7]))
    check(b_[8] is None and a_[1:5] == b_[1:5], 'L6 %s: the same C, K, S and evaluations as beta 1h' % loader)
    check(b_[0] <= a_[0] * 1.03, 'L6 %s: the blink costs at most 3 %% (%d vs %d)' % (loader, b_[0], a_[0]))
    # a toggle at the first check after 0.4 s, and a check at least every evaluation: on average a
    # toggle every 0.4 to 0.8 s, so at least secs / 1.6 lit phases
    check(b_[5] >= secs / 1.6 and b_[6] >= b_[5] - 1, 'L6 %s: the hourglass blinks (on %d, off %d over %.0f s)' % (loader, b_[5], b_[6], secs))
    check(b_[7] <= 1.0, 'L6 %s: never more than 1 s between blink checks on a G1 (%.2f s)' % (loader, b_[7]))
# L7 MicroPython: the hourglass is lit before the PYTHON() call of a fit
hb = new_b(); hb.call('bu_Init'); hb.call('bu_LoadBJS'); hb.call('bu_Fit')
L = hb.log
py = first(L, lambda e: isinstance(e, tuple) and e[0] == 'PYTHON')
check(py is not None and [i for i in hourglasses(L) if i < py] and hb.globals_['buEngUsed'] == 1, 'L7 the hourglass is lit before the Python fit call')
# L8 the title row stays clear of the hourglass (x < 302) on every case, and at the extremes
ext = cases + [(50, 50, 1000000, 999999, 0), (0.2, 50, 0.01, 0.01, 0), (49.99, 0.21, 123456, 654321, 1)]
worst_x = 0
for C, K, S, x0, view in ext:
    hd = explore_h(PROG, C, K, S, x0, view)
    tl = [t for t in hd.texts if str(t.grob) == 'G1' and abs(float(t.y or 0) - 4) < 0.5]
    xr = max(float(t.x) + t.est_width for t in tl) if tl else 0
    worst_x = max(worst_x, xr)
print('   the title row ends by x = %.0f at most (the hourglass starts at 302)' % worst_x)
check(worst_x < 302, 'L8 the title row clear of the hourglass: %.0f' % worst_x)
# L9 the point grid on the Family page (164 columns) and the help sentence
hf = Count(PROG, strict=False, idle_key=4, cas='fail'); hf.call('bu_Init'); g = hf.globals_
g['buPB'] = 153.0; g['buPR'] = 200.0; g['buNC'] = 164.0; g['buRe'] = 1.0; g['buXmax'] = 40.0
hf.execute('bu_CachePPL()')
cols_ = sorted(int(v) - 36 for v in g['buPts'][0::2][:int(g['buNPt'])])
check(cols_ == sorted(want_cols(2.0, 1.5, 10.0, 40.0, 164)), 'L9 the Family grid: %s ... %s' % (cols_[:5], cols_[-4:]))
src = open(PROG, encoding='utf-8').read()
check('A yellow hourglass at the top right: still computing.' in src and 'BurrLab beta 1i: the long right tail' in src, 'L9 help and title texts')

print('%d checks, %d failures' % (N_CHECK, len(FAILS)))
for f in FAILS:
    print('  ', f)
sys.exit(1 if FAILS else 0)

