#!/usr/bin/env python3
"""verify_SeizureLab_beta1a.py -- checks for SeizureLab beta 1a (21 Oct 2026).

beta 1a applies the second review (REVIEW2_SeizureLab_beta1.md, items 1-13).  This script is
verify_SeizureLab_beta1.py run on beta 1a, with its expected screen texts updated to beta 1a's
wording, its references updated to the beta 1a rules (the tie tolerance of item 4, the weight
factor of item 2), and a part R with one block per review item:
  R1  the Bayesian least-n searches: bisection = a full scan on the grid and on the reviewer's
      slow cases; the number of sums stays within 2 log2(top) + 3; Esc (pressed during the
      sums) stops Set up, Prior and the Tables page with "stopped" and no error
  R2  the weight factor sqrt((N - n)/N); ENFSI section 7's worked example typed in: half-width
      0.8728 g (ENFSI prints 0.873 g, factor 0.877)
  R3  the Bayesian page shows this-N and N -> inf least n side by side, and the ENFSI line;
      help page 6 with its live numbers
  R4  the tie tolerance 1E-6 relative to 1 - c; the reviewer's flip case N = 5000, p0 = 0.0501,
      c = 0.95 in a 12-digit decimal emulation of the program's own arithmetic, and in the
      harness: least n = 1, as in exact arithmetic
  R5  the OC drags end on a key and on an off-screen (phantom) reading; no frame without a change
  R6  the observed bar's outline: four red LINE_P, no red RECT_P
  R7  no CHAR(8592) or CHAR(8645) in the source
  R8  every text line within its width budget (font 1: 6.5 px, font 2: 8 px a character) at
      the defaults and at the reviewer's extreme inputs; help lines <= 45 characters
  R9  each page's key legend names the keys that page reads
  R10 the set-up form says what it clamped or rounded (negatives, prior a and b)
  R11 the header and help cite the ENFSI guideline with the UNODC link, mention Stoel & Bolck,
      mark the unread papers
  R12 the ENFSI tables 1-5 (427 cells, transcribed by the second reviewer from ENFSI DWG,
      Guidelines on Representative Drug Sampling, UNODC ST/NAR/38, 2009,
      https://www.unodc.org/documents/scientific/Drug_Sampling.pdf; his enfsi_cmp.py): 426 agree;
      the one that differs, Table 2 N = 90, 99%, k = 0.7, 2 negatives, prints 21 where exact
      arithmetic gives 22 (P(X >= 19 | 90, 62, 21) = 0.011150 > 0.01; at n = 22, 0.007561)
  R13 the szWRNG comment; "confidence bound" wording
  G   beta 1a against beta 1: every routine the CHANGES file does not name is byte-identical

The beta 1 description follows.

verify_SeizureLab_beta1.py -- checks for SeizureLab beta 1 (21 Oct 2026).

Every number the program computes is checked against an independent reference:
SciPy (stats.hypergeom, binom, betabinom, beta, t; special.betainc, gammaln), exact
rational arithmetic (fractions.Fraction with math.comb), and brute-force scans.
The program's own routines are called in the PC harness (ppl_run_v3e), so what is
checked is the PPL source itself, run with double arithmetic.

Part A  the numerics, called directly:
  A1  sz_LnG against gammaln (0.1 .. 1E6)
  A2  sz_HypS against exact fractions (N <= 300) and hypergeom (N to 1E6)
  A3  sz_BBS against betabinom pmf sums (unimodal, monotone, U-shaped, m to 20000)
  A4  sz_BinS against binom pmf sums
  A5  sz_IBeta against betainc
  A6  sz_KrOf: Kr = ceiling(p0 N) exactly (Fractions), p0 N whole and not
  A7  sz_HypMin against a brute-force scan in exact fractions (grid N 1..60 and more,
      c, p0, d), and against scipy for N to 10000
  A8  sz_BinMin against a scan with binom.cdf
  A9  sz_LowB against a scan with exact fractions / hypergeom.sf
  A10 sz_BayP against betabinom.sf, and the uniform-prior closed form
      1 - C(Kr, n+1)/C(N+1, n+1) in exact fractions
  A11 sz_BayMin against a full scan (grid), sz_BayMinL against a scan of beta.sf;
      monotonicity of the posterior probability in n over the grid
  A12 sz_BayL against beta.sf
  A13 the sums never cancel: every term of every sum is positive (static, and
      a run that records the minimum term sign); N = 1E6 runs without overflow
Part B  every menu path in the harness, the numbers ON THE PAGES against SciPy:
  B1  opening page (disclaimer, the red count), menu strings <= 30 characters
  B2  set-up form: defaults, edge values, refusals (MSGBOX <= 5 lines)
  B3  hypergeometric page: every soft key and key, a bar tap, P and the bound
  B4  binomial page: Neg -/+, N / 10, N x 10, a tap; both curves vs SciPy
  B5  Bayesian page: n, x, Prior; P (finite N) and P(theta >= p0) vs SciPy
  B6  OC page: the curves at 20 columns vs SciPy, a drag of n, a drag of theta,
      keys; worst-case line
  B7  weight page: example, typed summary, D1 (good, missing, bad, too many);
      T, SE, CI, bound vs scipy.stats.t with the finite-population factor
  B8  tables page and its plot: every entry vs the brute-force scans
  B9  enter-a-result form, help (all pages, Esc), quit summary, Home exports
  B10 N = 10000 and N = 1 through every page; stale-key mode
  B11 every page: the one-line disclaimer, no scientific number (h.sci_strings),
      no text past x = 320 or below y = 240, no runtime error
Part C  static: pure ASCII, LF, header lines, LOCAL lines <= 6 names, the version.

Run:  python3 verify_SeizureLab_beta1.py   (exit status 0 = every check passed)
"""
import math
import os
import random
import re
import sys
import time
from fractions import Fraction as Fr

import numpy as np
from scipy import special, stats

os.environ.setdefault('HPKIT', '/home/claude/kit/hp-prime-kit-HEAD')
sys.path.insert(0, '/home/claude/new6/ref')
from ppl_run_v3e import Harness  # noqa: E402

SRC = '/home/claude/new6/SeizureLab_beta1a.txt'
SRC1 = '/home/claude/new6/SeizureLab_beta1.txt'
DISC = 'Teaching aid; not a laboratory sampling plan.'

NCHK = 0
NFAIL = 0
FAILS = []


def check(cond, label, detail=''):
    global NCHK, NFAIL
    NCHK += 1
    if not cond:
        NFAIL += 1
        FAILS.append(label + ('  ' + str(detail) if detail else ''))
        if len(FAILS) <= 60:
            print('  FAIL', label, detail)
    return cond


def close(a, b, rel=1e-9, ab=1e-14):
    return abs(a - b) <= max(ab, rel * abs(b))


def section(t):
    print('\n' + '=' * 70 + '\n' + t + '\n' + '=' * 70)


def harness(**kw):
    kw.setdefault('strict', False)
    kw.setdefault('idle_key', 4)
    h = Harness(SRC, **kw)
    return h


H = harness()
H.call('sz_Init')


def ex(expr):
    return H.execute(expr)


def kreq(N, p0s):
    """Kr = ceiling(p0 N) in exact arithmetic; p0 given as a decimal string."""
    v = Fr(p0s) * N
    return -((-v.numerator) // v.denominator)


def hyp_tail_exact(N, K, n, lo, hi):
    lo2 = max(lo, 0, n - (N - K)); hi2 = min(hi, n, K)
    if lo2 > hi2:
        return Fr(0)
    tot = math.comb(N, n)
    return Fr(sum(math.comb(K, k) * math.comb(N - K, n - k) for k in range(lo2, hi2 + 1)), tot)


def rising(x, k):
    r = Fr(1)
    for i in range(k):
        r *= (x + i)
    return r


def bayp_exact(N, n, x, p0s, a, b):
    """P(Y >= Kr - x), Y beta-binomial(N - n, a + x, b + n - x), in exact fractions
    (a, b rational): pmf(y) = C(m, y) (al)_y (be)_(m-y) / (al + be)_m."""
    Kr = kreq(N, p0s); t = Kr - x; m = N - n
    if t <= 0:
        return Fr(1)
    if t > m:
        return Fr(0)
    al = Fr(a) + x; be = Fr(b) + n - x
    den = rising(al + be, m)
    return sum(math.comb(m, y) * rising(al, y) * rising(be, m - y) for y in range(t, m + 1)) / den


def binlow_exact(n, p0s, d):
    """P(at most d negatives), negatives ~ Binomial(n, 1 - p0), exact."""
    q = 1 - Fr(p0s); p = Fr(p0s)
    return sum(math.comb(n, j) * q ** j * p ** (n - j) for j in range(0, min(d, n) + 1))


# ======================================================================
section('A  the numerics, called directly in the harness')
t0 = time.time()

# A1 log-gamma
worst = 0
for z in [0.1, 0.25, 0.5, 0.7, 1, 1.5, 2, 2.5, 3, 7.3, 10, 33.3, 100, 1000.5, 10001, 99999, 1e6]:
    v = ex('sz_LnG(%r)' % z); r = special.gammaln(z)
    e = abs(v - r) / max(1, abs(r)); worst = max(worst, e)
    check(e < 1e-13, 'A1 lnGamma(%g)' % z, (v, r))
print('A1 lnGamma worst relative error %.2e' % worst)

# A2 hypergeometric sums
random.seed(2026)
worst = 0; n_a2 = 0
cases = [(100, 89, 23, 23, 23), (100, 89, 23, 0, 23), (10, 8, 8, 8, 8), (1, 0, 1, 1, 1), (1, 1, 1, 1, 1),
         (5, 5, 5, 0, 5), (5, 0, 3, 0, 0), (20, 17, 12, 10, 12), (300, 150, 300, 150, 150)]
for _ in range(220):
    N = random.choice([random.randint(1, 12), random.randint(1, 60), random.randint(1, 300)])
    K = random.randint(0, N); n = random.randint(0, N)
    lo = random.randint(0, n); hi = random.choice([n, random.randint(lo, n)])
    cases.append((N, K, n, lo, hi))
for (N, K, n, lo, hi) in cases:
    v = ex('sz_HypS(%d,%d,%d,%d,%d)' % (N, K, n, lo, hi)); r = float(hyp_tail_exact(N, K, n, lo, hi))
    ok = close(v, r, 1e-10, 1e-300) if r > 1e-280 else v < 1e-250
    worst = max(worst, abs(v - r) / r if r > 1e-280 else 0)
    n_a2 += 1
    check(ok, 'A2 HypS exact N=%d K=%d n=%d [%d,%d]' % (N, K, n, lo, hi), (v, r))
for _ in range(120):
    N = random.choice([1000, 10000, 100000, 1000000, random.randint(1000, 1000000)])
    K = random.randint(0, N); n = random.choice([random.randint(1, 50), random.randint(1, 3000)])
    n = min(n, N)
    x = random.randint(max(0, n - (N - K)), min(n, K)) if min(n, K) >= max(0, n - (N - K)) else 0
    v = ex('sz_HypS(%d,%d,%d,%d,%d)' % (N, K, n, x, n)); r = stats.hypergeom.sf(x - 1, N, K, n)
    ok = close(v, r, 1e-8, 1e-300) if r > 1e-250 else v < 1e-200
    if r > 1e-250:
        worst = max(worst, abs(v - r) / r)
    n_a2 += 1
    check(ok and v == v and v < 1.0000001, 'A2 HypS scipy N=%d K=%d n=%d x=%d' % (N, K, n, x), (v, r))
print('A2 hypergeometric: %d cases, worst relative error %.2e' % (n_a2, worst))

# A3 beta-binomial sums
worst = 0; n_a3 = 0
cases = [(0, 1, 1, 0, 0), (10, 0.5, 0.5, 0, 10), (10, 0.5, 0.5, 3, 7), (100, 1, 1, 10, 50), (50, 1.5, 0.5, 0, 50),
         (50, 0.5, 1.5, 40, 50), (1000, 24, 1, 900, 1000), (9971, 30, 1, 4971, 9971), (20000, 0.3, 0.4, 0, 20000),
         (77, 2.5, 7.5, 0, 0), (77, 2.5, 7.5, 77, 77)]
for _ in range(200):
    m = random.choice([random.randint(0, 20), random.randint(0, 400), random.randint(0, 5000)])
    al = random.choice([0.5, 1, 1.5, 3, 30.5, round(random.uniform(0.1, 60), 3)])
    be = random.choice([0.5, 1, 2, round(random.uniform(0.1, 60), 3)])
    lo = random.randint(0, m); hi = random.choice([m, random.randint(lo, m)])
    cases.append((m, al, be, lo, hi))
for (m, al, be, lo, hi) in cases:
    v = ex('sz_BBS(%d,%r,%r,%d,%d)' % (m, al, be, lo, hi))
    r = float(stats.betabinom.pmf(np.arange(lo, hi + 1), m, al, be).sum())
    ok = close(v, r, 1e-9, 1e-300) if r > 1e-250 else v < 1e-200
    if r > 1e-250:
        worst = max(worst, abs(v - r) / r)
    n_a3 += 1
    check(ok, 'A3 BBS m=%d a=%g b=%g [%d,%d]' % (m, al, be, lo, hi), (v, r))
print('A3 beta-binomial: %d cases, worst relative error %.2e' % (n_a3, worst))

# A4 binomial sums
worst = 0; n_a4 = 0
cases = [(0, 0.3, 0, 0), (5, 0, 0, 0), (5, 1, 5, 5), (5, 1, 0, 4), (29, 0.1, 0, 0), (1000000, 0.1, 0, 20)]
for _ in range(150):
    n = random.choice([random.randint(1, 30), random.randint(1, 3000), random.randint(1, 200000)])
    p = random.choice([0.5, 0.1, 0.001, 0.999, round(random.uniform(0.001, 0.999), 4)])
    lo = random.choice([0, random.randint(0, n)]); hi = random.choice([n, random.randint(lo, n), min(n, lo + 20)])
    cases.append((n, p, lo, hi))
for (n, p, lo, hi) in cases:
    v = ex('sz_BinS(%d,%r,%d,%d)' % (n, p, lo, hi))
    if p in (0, 1):
        r = float(stats.binom.pmf(np.arange(lo, hi + 1), n, p).sum())
    else:
        r = float(stats.binom.sf(lo - 1, n, p) - stats.binom.sf(hi, n, p)) if hi - lo > 5000 else \
            float(stats.binom.pmf(np.arange(lo, hi + 1), n, p).sum())
    ok = close(v, r, 1e-8, 1e-300) if r > 1e-250 else v < 1e-200
    if r > 1e-250:
        worst = max(worst, abs(v - r) / r)
    n_a4 += 1
    check(ok, 'A4 BinS n=%d p=%g [%d,%d]' % (n, p, lo, hi), (v, r))
print('A4 binomial: %d cases, worst relative error %.2e' % (n_a4, worst))

# A5 incomplete beta
worst = 0
for _ in range(120):
    x = random.choice([0.1, 0.5, 0.9, 0.01, 0.999, random.uniform(0, 1)])
    a = random.choice([0.5, 1, 30, 1000.5, random.uniform(0.1, 200)]); b = random.choice([0.5, 1, 2, random.uniform(0.1, 200)])
    v = ex('sz_IBeta(%r,%r,%r)' % (x, a, b)); r = special.betainc(a, b, x)
    ok = close(v, r, 1e-9, 1e-300) if r > 1e-250 else v < 1e-200
    if r > 1e-250:
        worst = max(worst, abs(v - r) / r)
    check(ok, 'A5 IBeta x=%g a=%g b=%g' % (x, a, b), (v, r))
print('A5 incomplete beta worst relative error %.2e' % worst)

# A6 Kr = ceiling(p0 N)
for N in [1, 7, 10, 15, 100, 101, 1000, 9999, 10000]:
    for p0s in ['0.5', '0.07', '0.29', '0.57', '0.9', '0.95', '0.99', '0.999', '0.001', '0.333', '0.123']:
        v = ex('sz_KrOf(%d,%s)' % (N, p0s))
        check(v == kreq(N, p0s), 'A6 Kr N=%d p0=%s' % (N, p0s), (v, kreq(N, p0s)))
print('A6 Kr checked; e.g. N=100 p0=0.90 -> Kr=%d, K0=%d; N=15 p0=0.90 -> Kr=%d' % (
    ex('sz_KrOf(100,0.9)'), ex('sz_KrOf(100,0.9)') - 1, ex('sz_KrOf(15,0.9)')))


# A7 hypergeometric least n: brute force, exact
TOL = Fr(1, 10 ** 6)     # beta 1a's documented tie tolerance (review item 4), relative to 1 - c


def hyp_min_exact(N, cs, p0s, d):
    K0 = kreq(N, p0s) - 1
    a = 1 - Fr(cs)
    for n in range(d + 1, N + 1):
        if hyp_tail_exact(N, K0, n, n - d, n) <= a * (1 + TOL):
            return n, hyp_tail_exact(N, K0, n, n - d, n)
    return -1, None


ties = 0; n_a7 = 0; near = []
grid_N = list(range(1, 61)) + [75, 99, 100, 101, 137, 150, 200, 250]
for N in grid_N:
    for cs in ['0.9', '0.95', '0.99']:
        for p0s in ['0.5', '0.75', '0.8', '0.9', '0.95', '0.99']:
            for d in (0, 1, 2):
                r, pr = hyp_min_exact(N, cs, p0s, d)
                v = ex('sz_HypMin(%d,%s,%s,%d)' % (N, cs, p0s, d))
                n_a7 += 1
                if pr is not None and abs(float(pr) - (1 - float(cs))) < 1e-9:
                    ties += 1
                check(v == r, 'A7 HypMin N=%d c=%s p0=%s d=%d' % (N, cs, p0s, d), (v, r))
print('A7 hypergeometric least n, exact brute force: %d cases, %d at an exact tie' % (n_a7, ties))
# larger N against scipy
for N in [500, 1000, 2000, 5000, 10000]:
    for cs in ['0.95', '0.99']:
        for p0s in ['0.5', '0.9', '0.99']:
            for d in (0, 1, 2, 5):
                K0 = kreq(N, p0s) - 1
                a = 1 - float(cs)
                ns = np.arange(d + 1, N + 1)
                P = np.array([stats.hypergeom.sf(n - d - 1, N, K0, n) for n in ns[:min(len(ns), 3000)]])
                idx = np.where(P <= a)[0]
                r = int(ns[idx[0]]) if len(idx) else -1
                v = ex('sz_HypMin(%d,%s,%s,%d)' % (N, cs, p0s, d))
                check(v == r, 'A7 HypMin scipy N=%d c=%s p0=%s d=%d' % (N, cs, p0s, d), (v, r))


# A8 binomial least n
def bin_min_scan(cs, p0s, d):
    a = 1 - float(cs); p0 = float(p0s)
    n = d + 1
    while True:
        P = stats.binom.cdf(d, n, 1 - p0)
        if abs(P - a) < 1e-5 * a:          # near a tie: decide in exact arithmetic
            if binlow_exact(n, p0s, d) <= (1 - Fr(cs)) * (1 + TOL):
                return n
        elif P <= a:
            return n
        n += 1


for cs in ['0.8', '0.9', '0.95', '0.99', '0.9999']:
    for p0s in ['0.001', '0.1', '0.5', '0.75', '0.9', '0.95', '0.99', '0.999']:
        for d in (0, 1, 2, 7, 20):
            v = ex('sz_BinMin(%s,%s,%d)' % (cs, p0s, d)); r = bin_min_scan(cs, p0s, d)
            check(v == r, 'A8 BinMin c=%s p0=%s d=%d' % (cs, p0s, d), (v, r))
print('A8 binomial least n: e.g. c=0.95 p0=0.9 d=0,1,2 ->', [ex('sz_BinMin(0.95,0.9,%d)' % d) for d in (0, 1, 2)])

# A9 lower confidence bound
n_a9 = 0
for N in [1, 2, 5, 10, 20, 37, 100]:
    for n in sorted(set(k for k in [1, 2, N // 3 or 1, N // 2 or 1, N] if k <= N)):
        for x in sorted(set([0, 1, n // 2, n - 1, n])):
            if x < 0 or x > n:
                continue
            for cs in ['0.9', '0.95', '0.99']:
                a = 1 - Fr(cs)
                if x == 0:
                    r = 0
                else:
                    r = next(K for K in range(x, N - (n - x) + 1) if hyp_tail_exact(N, K, n, x, n) > a * (1 + TOL))
                v = ex('sz_LowB(%d,%d,%d,%s)' % (N, n, x, cs))
                n_a9 += 1
                check(v == r, 'A9 LowB N=%d n=%d x=%d c=%s' % (N, n, x, cs), (v, r))
for N, n, x in [(1000, 29, 29), (10000, 50, 48), (10000, 300, 290), (5000, 2, 1)]:
    r = next(K for K in range(x, N - (n - x) + 1) if stats.hypergeom.sf(x - 1, N, K, n) > 0.05)
    v = ex('sz_LowB(%d,%d,%d,0.95)' % (N, n, x))
    check(v == r, 'A9 LowB scipy N=%d n=%d x=%d' % (N, n, x), (v, r))
print('A9 lower bound: %d exact cases' % n_a9)

# A10 Bayesian P (finite N)
n_a10 = 0
for _ in range(150):
    N = random.choice([random.randint(1, 30), random.randint(1, 500), random.randint(1, 10000)])
    n = random.randint(0, N); x = random.randint(0, n)
    p0s = random.choice(['0.5', '0.9', '0.95', '0.1', '0.999'])
    a, b = random.choice([(1, 1), (0.5, 0.5), (2, 1), (1, 3), (0.3, 0.4)])
    Kr = kreq(N, p0s); t = Kr - x; m = N - n
    if t <= 0:
        r = 1.0
    elif t > m:
        r = 0.0
    else:
        r = float(stats.betabinom.pmf(np.arange(t, m + 1), m, a + x, b + n - x).sum())
    v = ex('sz_BayP(%d,%d,%d,%s,%r,%r)' % (N, n, x, p0s, a, b))
    ok = close(v, r, 1e-9, 1e-300) if r > 1e-250 else v < 1e-200
    n_a10 += 1
    check(ok, 'A10 BayP N=%d n=%d x=%d p0=%s a=%g b=%g' % (N, n, x, p0s, a, b), (v, r))
# the closed form, uniform prior, all positive: 1 - C(Kr, n+1)/C(N+1, n+1)
for N in [1, 5, 10, 50, 100, 1000, 3000]:
    for p0s in ['0.5', '0.9', '0.99']:
        Kr = kreq(N, p0s)
        for n in sorted(set([0, 1, 5, 22, 23, N // 2, N])):
            if n > N:
                continue
            exact = 1 - Fr(math.comb(Kr, n + 1), math.comb(N + 1, n + 1))
            v = ex('sz_BayP(%d,%d,%d,%s,1,1)' % (N, n, n, p0s))
            n_a10 += 1
            check(close(v, float(exact), 1e-10, 1e-15), 'A10 closed form N=%d n=%d p0=%s' % (N, n, p0s), (v, float(exact)))
print('A10 Bayesian P: %d cases; N=100, n=x=23 -> %.6f (closed form %.6f)' % (
    n_a10, ex('sz_BayP(100,23,23,0.9,1,1)'), float(1 - Fr(math.comb(90, 24), math.comb(101, 24)))))


# A11 Bayesian least n (finite and large N), monotonicity
def bayp_ref(N, n, x, p0s, a, b):
    Kr = kreq(N, p0s); t = Kr - x; m = N - n
    if t <= 0:
        return 1.0
    if t > m:
        return 0.0
    return float(stats.betabinom.pmf(np.arange(t, m + 1), m, a + x, b + n - x).sum())


def bay_ok(N, n, p0s, a, b, cs):
    """P(claim | n all positive) >= c, ties decided in exact arithmetic."""
    P = bayp_ref(N, n, n, p0s, a, b); c = float(cs)
    if abs(P - c) < 1e-5 * (1 - c):
        return bayp_exact(N, n, n, p0s, a, b) >= Fr(cs) - TOL * (1 - Fr(cs))
    return P >= c


nonmono = 0; n_a11 = 0
for N in list(range(1, 41)) + [50, 64, 100, 128, 200, 500, 1000]:
    for cs in ['0.9', '0.95', '0.99']:
        for p0s in ['0.05', '0.5', '0.75', '0.9', '0.95']:
            for (a, b) in [(1, 1), (0.5, 0.5), (2, 1), (1, 3)]:
                vals = [bayp_ref(N, n, n, p0s, a, b) for n in range(N + 1)]
                r = next(n for n in range(N + 1) if bay_ok(N, n, p0s, a, b, cs))
                if any(vals[i + 1] < vals[i] - 1e-9 for i in range(N)):
                    nonmono += 1
                v = ex('sz_BayMin(%d,%s,%s,%r,%r)' % (N, cs, p0s, a, b))
                n_a11 += 1
                check(v == r, 'A11 BayMin N=%d c=%s p0=%s a=%g b=%g' % (N, cs, p0s, a, b), (v, r))
check(nonmono == 0, 'A11 P(claim | n all positive) rises with n on the whole grid', nonmono)
for N in [2000, 10000]:
    for p0s in ['0.5', '0.9']:
        for (a, b) in [(1, 1), (0.5, 0.5)]:
            r = next(n for n in range(N + 1) if bay_ok(N, n, p0s, a, b, '0.95'))
            v = ex('sz_BayMin(%d,0.95,%s,%r,%r)' % (N, p0s, a, b))
            check(v == r, 'A11 BayMin N=%d p0=%s a=%g' % (N, p0s, a), (v, r))
for cs in ['0.9', '0.95', '0.99']:
    for p0s in ['0.01', '0.5', '0.75', '0.9', '0.95', '0.99', '0.999']:
        for (a, b) in [(1, 1), (0.5, 0.5), (2, 1), (1, 3)]:
            n = 0
            while stats.beta.sf(float(p0s), a + n, b) < float(cs) - 1e-6 * (1 - float(cs)):
                n += 1
            v = ex('sz_BayMinL(%s,%s,%r,%r)' % (cs, p0s, a, b))
            check(v == n, 'A11 BayMinL c=%s p0=%s a=%g b=%g' % (cs, p0s, a, b), (v, n))
print('A11 Bayesian least n: %d finite-N grid cases, %d non-monotone' % (n_a11, nonmono))

# A12 P(theta >= p0) as N grows
for _ in range(60):
    n = random.randint(0, 300); x = random.randint(0, n); p0 = random.choice([0.5, 0.9, 0.99, round(random.uniform(0.01, 0.99), 3)])
    a, b = random.choice([(1, 1), (0.5, 0.5), (3, 2)])
    v = ex('sz_BayL(%d,%d,%r,%r,%r)' % (n, x, p0, a, b)); r = stats.beta.sf(p0, a + x, b + n - x)
    ok = close(v, r, 1e-9, 1e-300) if r > 1e-250 else v < 1e-200
    check(ok, 'A12 BayL n=%d x=%d p0=%g' % (n, x, p0), (v, r))

# A13 positive terms only; large N without overflow
src = open(SRC, encoding='utf-8').read()
for fn in ['sz_HypS', 'sz_HypL', 'sz_BBS', 'sz_BinS', 'sz_OCCurve']:
    body = re.search(r'\n%s\(.*?\nEND;' % fn, src, re.S).group(0)
    # every running total is only ever increased by a term, never decreased
    sums = re.findall(r'(\w+S) := \1 ([+-]) ', body)
    check(all(sgn == '+' for _, sgn in sums), 'A13 %s adds terms only' % fn, sums)
for expr in ['sz_HypS(1000000, 900000, 3000, 2700, 3000)', 'sz_HypS(1000000, 999999, 1000000, 0, 1000000)',
             'sz_BBS(100000, 0.5, 0.5, 0, 100000)', 'sz_BBS(1000000, 30, 1, 900000, 1000000)', 'sz_BinS(1000000, 0.5, 0, 1000000)',
             'sz_HypMin(10000, 0.9999, 0.999, 20)', 'sz_LowB(10000, 10000, 10000, 0.95)',
             'sz_BayP(10000, 0, 0, 0.001, 0.1, 0.1)', 'sz_BayMin(10000, 0.9999, 0.999, 0.5, 0.5)']:
    try:
        v = ex(expr); ok = isinstance(v, float) and v == v and abs(v) < 1e300
    except Exception as e:  # noqa
        v = repr(e); ok = False
    check(ok, 'A13 large: ' + expr, v)
print('A13 positive-term sums and large-N calls checked')
print('Part A: %.1f s' % (time.time() - t0))

# ======================================================================
section('B  every menu path in the harness')
t0 = time.time()
SCI = []
ALLPAGES = []


def run(script, **kw):
    """Run the program from the top with a script; return the harness."""
    h = harness(**kw)
    script(h)
    h.call('SeizureLab')
    SCI.extend(h.sci_strings)
    ALLPAGES.extend(h.pages)
    if h.error is not None:
        check(False, 'B runtime error', h.error)
    return h


def page_has(p, sub):
    return any(sub in t.text for t in p.texts)


def result_pages(h):
    return [p for p in h.pages if p.menu]


def gv(h, name):
    return h.execute(name)


# B1 opening page and menu
def s_b1(h):
    h.press('Enter'); h.choose('Quit')


h = run(s_b1)
op = [p for p in h.pages if page_has(p, 'random sample')]
check(len(op) == 1, 'B1 opening page shown once')
if op:
    check(page_has(op[0], 'DISCLAIMER: a teaching and demonstration aid'), 'B1 header disclaimer on the opening page')
    check(page_has(op[0], DISC), 'B1 one-line disclaimer on the opening page')
    check(page_has(op[0], 'the 23 red units'), 'B1 red count = least n (23)')
    reds = [s for s in op[0].shapes if s.cmd == 'RECT_P' and len(s.args) >= 6 and s.args[-1] == 0xFF0000 and s.args[-2] == 0xFF0000]
    check(len(reds) == 23, 'B1 23 red squares drawn', len(reds))
ch = h.chooses[0]
check(all(len(it) <= 30 for it in ch.items), 'B1 menu items <= 30 characters', [it for it in ch.items if len(it) > 30])
check(len(ch.items) == 10, 'B1 ten menu items')
check(h.result.startswith('SeizureLab: N = 100') and 'test 23' in h.result and 'Bayes 22' in h.result, 'B1 quit summary', h.result)
check(h.execute('SZ_N') == 100 and h.execute('SZ_NMIN') == 23, 'B1 Home SZ_N, SZ_NMIN')


# B2 set-up form
def setup_run(vals, then=None):
    def s(h):
        h.press('Enter'); h.choose('Set up'); h.answer(vals)
        if then:
            then(h)
        h.choose('Quit')
    return run(s)


h = setup_run({'suN': 1000, 'suC': 0.99, 'suP': 0.95, 'suD': 1, 'suPa': 0.5, 'suPb': 0.5})
check([gv(h, v) for v in ['szN', 'szC', 'szP0', 'szD', 'szA', 'szB']] == [1000, 0.99, 0.95, 1, 0.5, 0.5], 'B2 form stores the values')
check(gv(h, 'szKr') == 950 and gv(h, 'szK0') == 949, 'B2 Kr, K0 for N=1000 p0=0.95')
hm = [hyp_min_exact(1000, '0.99', '0.95', d)[0] if False else None for d in range(3)]
hmr = []
for d in range(3):
    K0 = 949; ns = np.arange(d + 1, 1001)
    P = np.array([stats.hypergeom.sf(n - d - 1, 1000, K0, n) for n in ns[:400]])
    hmr.append(int(ns[np.where(P <= 0.01)[0][0]]))
check(list(gv(h, 'szHm')) == hmr, 'B2 least n after set-up', (gv(h, 'szHm'), hmr))
check(gv(h, 'szNt') == hmr[1] and gv(h, 'szJ') == 1, 'B2 the plan becomes the result in hand (n = least n for d)')
# refusals and clamps
for vals, msg in [({'suN': 0}, 'N must be'), ({'suN': 10001}, 'N must be'), ({'suC': 1}, 'c must be'),
                  ({'suC': 0}, 'c must be'), ({'suP': 1}, 'must be strictly'), ({'suP': -0.1}, 'must be strictly'),
                  ({'suPa': 0}, 'prior'), ({'suC': 0.3}, 'raised to 0.5'), ({'suC': 0.999999}, 'lowered to 0.9999'),
                  ({'suP': 0.9999}, 'lowered to 0.999'), ({'suP': 0.0001}, 'raised to 0.001')]:
    h = setup_run(vals)
    mb = [' '.join(m.lines) for m in h.msgboxes]
    check(any(msg in m for m in mb), 'B2 form message for %r' % vals, mb)
    check(all(not m.over_five for m in h.msgboxes), 'B2 MSGBOX <= 5 lines %r' % vals)
h = setup_run({'suN': 37.4, 'suD': 33})
check(gv(h, 'szN') == 37 and gv(h, 'szD') == 20, 'B2 N rounded, negatives clamped to 20')


# B3 hypergeometric page
def hyp_ref(N, p0s, cs, n, j):
    K0 = kreq(N, p0s) - 1; x = n - j
    P = float(hyp_tail_exact(N, K0, n, x, n)) if N <= 400 else stats.hypergeom.sf(x - 1, N, K0, n)
    if x == 0:
        LB = 0
    else:
        LB = next(K for K in range(x, N - (n - x) + 1) if (float(hyp_tail_exact(N, K, n, x, n)) if N <= 400 else stats.hypergeom.sf(x - 1, N, K, n)) > 1 - float(cs))
    return P, LB


def pstr(p):
    if p <= 0:
        return '= 0'
    if p >= 1:
        return '= 1'
    if p < 0.0001:
        return '< 0.0001'
    if p > 0.9999:
        return '> 0.9999'
    return '= %.4f' % (round(p, 4) + 0)


def s_b3(h):
    h.press('Enter'); h.choose('Hypergeometric')
    h.tap(10, 230)        # n -
    h.tap(60, 230)        # n +
    h.tap(60, 230)        # n +
    h.tap(120, 230)       # x - (one more negative)
    h.tap(170, 230)       # x +
    h.tap(120, 230)       # x -
    h.tap(230, 230)       # Min n (for 1 negative)
    h.press('Minus'); h.press('Plus'); h.press('Left'); h.press('Right'); h.press('Up'); h.press('Down')
    h.tap(300, 150)       # a bar
    h.tap(300, 230)       # Menu (the page menu)
    h.choose('Main menu')
    h.choose('Quit')


h = run(s_b3)
pg = [p for p in h.pages if page_has(p, 'Hypergeometric: claim K')]
check(len(pg) >= 13, 'B3 hypergeometric frames', len(pg))
seq = [(23, 0), (22, 0), (23, 0), (24, 0), (24, 1), (24, 0), (24, 1), (36, 1), (35, 1), (36, 1), (36, 2), (36, 1), (46, 1), (36, 1), (36, 1)]
for i, p in enumerate(pg[:len(seq)]):
    n, j = seq[i]
    P, LB = hyp_ref(100, '0.9', '0.95', n, j)
    check(page_has(p, 'Tested n = %d: x = %d positive, %d neg' % (n, n - j, j)), 'B3 frame %d shows n=%d x=%d' % (i, n, n - j),
          [t.text for t in p.texts][:5])
    check(page_has(p, 'P(X %s %d) %s' % ('≥', n - j, pstr(P))), 'B3 frame %d P = %s' % (i, pstr(P)), [t.text for t in p.texts][3])
    verdict = 'SUPPORTED' if P <= 0.05 else 'NOT supported'
    check(page_has(p, verdict), 'B3 frame %d verdict %s' % (i, verdict))
    check(page_has(p, 'Lower 95%% confidence bound: K %s %d (%.1f%%)' % ('≥', LB, LB)), 'B3 frame %d bound %d' % (i, LB))
check(page_has(pg[0], 'Least n (0, 1, 2 negatives): 23, 36, 46'), 'B3 least n line')
tapped = [p for p in pg if p.text_at(192) and 'k = ' in ' '.join(t.text for t in p.texts if t.y == 192)]
check(len(tapped) == 1, 'B3 a bar tap writes the info line')
if tapped:
    line = [t.text for t in tapped[0].texts if t.y == 192][0]
    k = int(re.search(r'k = (\d+)', line).group(1))
    n = 36
    pk = float(hyp_tail_exact(100, 89, n, k, k)); tail = float(hyp_tail_exact(100, 89, n, k, n))
    check(pstr(pk) in line and pstr(tail) in line, 'B3 tapped bar k=%d values' % k, line)
check(abs(h.execute('SZ_P') - float(hyp_tail_exact(100, 89, 36, 35, 36))) < 1e-12, 'B3 SZ_P export')
check(h.execute('SZ_LB') == hyp_ref(100, '0.9', '0.95', 36, 1)[1] / 100, 'B3 SZ_LB export')
# the bars on the first frame: heights proportional to the pmf
bars = [s for s in pg[0].shapes if s.cmd == 'RECT_P' and len(s.args) >= 5]
check(len(bars) >= 8, 'B3 bars drawn', len(bars))


# B4 binomial page
def s_b4(h):
    h.press('Enter'); h.choose('Binomial')
    h.tap(150, 120)       # read a point
    h.tap(60, 230)        # Neg +
    h.tap(60, 230)        # Neg +
    h.tap(60, 230)        # Neg + (3: computed)
    h.tap(10, 230)        # Neg -
    h.tap(10, 230); h.tap(10, 230); h.tap(10, 230)   # back to 0 (and one below: stays 0)
    h.tap(200, 230)       # N x 10
    h.tap(150, 230)       # N / 10
    h.tap(150, 230)       # N / 10 -> 10
    h.tap(300, 230); h.choose('Main menu')
    h.choose('Quit')


h = run(s_b4)
pg = [p for p in h.pages if page_has(p, 'Binomial approximation, N =')]
check(len(pg) >= 10, 'B4 binomial frames', len(pg))
p = pg[0]
check(page_has(p, 'Hypergeometric (N = 100): 23, 36, 46'), 'B4 hyper line')
check(page_has(p, 'Binomial (N → ∞): 29, 46, 61'), 'B4 binomial line')
check(page_has(p, 'Your n, x: hyper P = 0.0472, binom P = %.4f' % stats.binom.sf(22, 23, 0.9)), 'B4 both P at n = 23', [t.text for t in p.texts][5])
check(page_has(p, 'Binomial: 6 more (0 neg), the safe side'), 'B4 comparison line')
line = [t.text for t in pg[1].texts if t.y == 192][0]
mt = re.search(r'n = (\d+): hyper P (.*?), binom P (.*)$', line)
check(mt is not None, 'B4 tap reads a point', line)
if mt:
    nn = int(mt.group(1))
    check(mt.group(2) == pstr(float(hyp_tail_exact(100, 89, nn, nn, nn))) and mt.group(3) == pstr(0.9 ** nn), 'B4 tapped values n=%d' % nn, line)
# curves cached in the program: every point vs scipy (state after the run: N = 10, d = 0)
for lab, Nn in [('final', 10)]:
    Hn = list(h.execute('szBnH')); Bn = list(h.execute('szBnB')); M = int(h.execute('szBnM'))
    K0 = kreq(Nn, '0.9') - 1
    bad = 0
    for n in range(1, M + 1):
        rb = stats.binom.cdf(0, n, 0.1)
        if not close(Bn[n - 1], rb, 1e-9, 1e-300):
            bad += 1
        if n <= Nn:
            rh = float(hyp_tail_exact(Nn, K0, n, n, n))
            if not close(Hn[n - 1], rh, 1e-9, 1e-300) and not (rh == 0 and Hn[n - 1] == 0):
                bad += 1
        elif Hn[n - 1] != -1:
            bad += 1
    check(bad == 0, 'B4 both curves = SciPy at every n (N = 10)', bad)
# d = 3 frame: computed least n
f3 = [p for p in pg if page_has(p, 'P(\u2264 3 neg), cut at 0.2')]
check(len(f3) >= 1, 'B4 3 negatives frame')
if f3:
    r3 = hyp_min_exact(100, '0.95', '0.9', 3)[0]; b3 = bin_min_scan('0.95', '0.9', 3)
    check(page_has(f3[0], 'Binomial: %d more (3 neg)' % (b3 - r3)), 'B4 3-negative comparison %d vs %d' % (r3, b3))
f1000 = [p for p in pg if page_has(p, 'Binomial approximation, N = 1000')]
check(len(f1000) == 1, 'B4 N x 10 -> 1000')
if f1000:
    r = [hyp_min_exact(1000, '0.95', '0.9', d)[0] if False else None for d in range(3)]
    rr = []
    for d in range(3):
        ns = np.arange(d + 1, 1001)
        P = np.array([stats.hypergeom.sf(n - d - 1, 1000, 899, n) for n in ns[:200]])
        rr.append(int(ns[np.where(P <= 0.05)[0][0]]))
    check(page_has(f1000[0], 'Hypergeometric (N = 1000): %d, %d, %d' % tuple(rr)), 'B4 N = 1000 least n', rr)
check(h.execute('szN') == 10, 'B4 N / 10 twice from 1000 -> 10')


# B5 Bayesian page
def s_b5(h):
    h.press('Enter'); h.choose('Bayesian')
    h.tap(10, 230)        # n -
    h.tap(120, 230)       # x -
    h.tap(230, 230)       # Prior -> Jeffreys
    h.tap(170, 230)       # x +
    h.tap(60, 230)        # n +
    h.tap(200, 130)       # read the densities
    h.press('Minus'); h.press('Left')
    h.tap(230, 230)       # Prior -> uniform
    h.tap(300, 230); h.choose('Main menu')
    h.choose('Quit')


h = run(s_b5)
pg = [p for p in h.pages if page_has(p, 'Bayes: prior Beta(')]
check(len(pg) >= 9, 'B5 Bayesian frames', len(pg))
seq = [(23, 0, 1, 1), (22, 0, 1, 1), (22, 1, 1, 1), (22, 1, .5, .5), (22, 0, .5, .5), (23, 0, .5, .5), (23, 0, .5, .5),
       (22, 0, .5, .5), (22, 1, .5, .5), (22, 1, 1, 1)]
for i, p in enumerate(pg[:len(seq)]):
    n, j, a, b = seq[i]; x = n - j
    P = bayp_ref(100, n, x, '0.9', a, b); L = stats.beta.sf(0.9, a + x, b + j)
    check(page_has(p, 'n = %d, x = %d: posterior Beta(' % (n, x)), 'B5 frame %d n=%d x=%d' % (i, n, x))
    check(page_has(p, 'P(at least 90 of 100 drug | data) %s' % pstr(P)), 'B5 frame %d P %s' % (i, pstr(P)),
          [t.text for t in p.texts][2])
    check(page_has(p, 'if N were huge %s' % pstr(L)), 'B5 frame %d large-N P %s' % (i, pstr(L)))
    check(page_has(p, 'supported (Bayes)'), 'B5 frame %d verdict' % i)
    ym = next(m for m in range(101) if bay_ok(100, m, '0.9', a, b, '0.95'))
    yl = 0
    while stats.beta.sf(0.9, a + yl, b) < 0.95:
        yl += 1
    check(page_has(p, ': this N %d; N → ∞ %d' % (ym, yl)), 'B5 frame %d least n %d / %d' % (i, ym, yl))
tp = [p for p in pg if any(t.y == 192 and t.text.startswith('θ = ') for t in p.texts)]
check(len(tp) == 1, 'B5 a tap reads theta')
if tp:
    line = [t.text for t in tp[0].texts if t.y == 192][0]
    mt = re.search(r'= ([\d.]+): prior ([\d.]+), posterior ([\d.]+)', line)
    th = float(mt.group(1))
    check(abs(float(mt.group(2)) - round(stats.beta.pdf(th, .5, .5), 2)) < 0.006 and
          abs(float(mt.group(3)) - round(stats.beta.pdf(th, 23.5, 0.5), 2)) < 0.006 + 0.01 * stats.beta.pdf(th, 23.5, 0.5),
          'B5 tapped densities', line)
check(abs(h.execute('SZ_PB') - bayp_ref(100, 22, 21, '0.9', 1, 1)) < 1e-12, 'B5 SZ_PB export')
# the densities cached per column vs scipy
Pr = list(h.execute('szBaPr')); Po = list(h.execute('szBaPo')); W = len(Po)
bad = sum(1 for i in range(W) if not close(Po[i], stats.beta.pdf((i + 0.5) / W, 1 + 21, 1 + 1), 1e-9, 1e-300)
          or not close(Pr[i], 1.0, 1e-12))
check(bad == 0 and W == 282, 'B5 densities = beta.pdf at all %d columns' % W, bad)

# B6 OC page
W_OC = 282


def oc_ref(N, n, d, L=0.0, W=W_OC):
    hy = []; bi = []
    for i in range(1, W + 1):
        th = L + (i - 0.5) / W * (1 - L); K = math.floor(th * N + 1e-9)
        hy.append(stats.hypergeom.sf(n - d - 1, N, K, n) if n - d >= 1 else 1.0)
        bi.append(stats.binom.cdf(d, n, 1 - th))
    return hy, bi


def s_b6(h):
    h.press('Enter'); h.choose('OC curve')
    h.drag([(200, 100), (150, 100), (120, 100)])          # the true proportion
    h.drag([(120, 28), (140, 28), (180, 28), (250, 28)])   # the n knob
    h.press('Up')                                           # 1 negative allowed
    h.tap(300, 230); h.choose('Least n')                    # the page menu: least n
    h.press('Plus'); h.press('Right')
    h.tap(10, 230)                                          # n -
    h.tap(120, 230)                                         # Neg -
    h.tap(230, 230)                                         # Zoom (near p0)
    h.drag([(100, 100), (160, 100)])                        # the true proportion, zoomed
    h.press('Enter'); h.choose('Main menu')
    h.choose('Quit')


h = run(s_b6)
pg = [p for p in h.pages if page_has(p, 'OC curve: N =')]
check(len(pg) >= 10, 'B6 OC frames', len(pg))
# final state: N = 100, n and d from the script; compare the cached curves at 20 columns
n_f = int(h.execute('szNt')); d_f = int(h.execute('szD'))
Hc = list(h.execute('szOcH')); Bc = list(h.execute('szOcB'))
L_f = float(h.execute('szOcL'))
check(abs(L_f - 0.7) < 1e-12, 'B6 Zoom: the axis starts at 0.7 for p0 = 0.90', L_f)
hy, bi = oc_ref(100, n_f, d_f, L_f)
cols = sorted(set([1, W_OC] + [int(round(1 + k * (W_OC - 1) / 19)) for k in range(20)]))
for c in cols:
    check(close(Hc[c - 1], hy[c - 1], 1e-9, 1e-300) or (hy[c - 1] < 1e-280 and Hc[c - 1] < 1e-250),
          'B6 hyper OC col %d (theta %.4f)' % (c, (c - 0.5) / W_OC), (Hc[c - 1], hy[c - 1]))
    check(close(Bc[c - 1], bi[c - 1], 1e-9, 1e-300) or (bi[c - 1] < 1e-280 and Bc[c - 1] < 1e-250),
          'B6 binomial OC col %d' % c, (Bc[c - 1], bi[c - 1]))
check(all(close(Hc[i], hy[i], 1e-9, 1e-280) or hy[i] < 1e-250 for i in range(W_OC)), 'B6 hyper OC every column')
check(all(close(Bc[i], bi[i], 1e-9, 1e-280) or bi[i] < 1e-250 for i in range(W_OC)), 'B6 binomial OC every column')
print('B6 OC final state n = %d, d = %d' % (n_f, d_f))
# 20 points on a large-N curve too, computed directly (the page's routine, N = 10000)
H2 = harness(); H2.call('sz_Init')
H2.execute('sz_Recalc()')
for (Nn, nn, dd, LL) in [(10000, 29, 0, 0.0), (10000, 61, 2, 0.0), (37, 20, 1, 0.0), (5, 3, 0, 0.0),
                         (10000, 29, 0, 0.7), (37, 20, 1, 0.3)]:
    H2.globals_['szN'] = float(Nn); H2.globals_['szNt'] = float(nn); H2.globals_['szD'] = float(dd)
    H2.globals_['szPL'] = 30.0; H2.globals_['szPR'] = 312.0; H2.globals_['szOcL'] = LL
    H2.execute('sz_OCFit()'); H2.execute('sz_OCCurve(1)')
    Hc = list(H2.execute('szOcH')); Bc = list(H2.execute('szOcB'))
    hy, bi = oc_ref(Nn, nn, dd, LL)
    for c in cols:
        check(close(Hc[c - 1], hy[c - 1], 1e-8, 1e-300) or (hy[c - 1] < 1e-250 and Hc[c - 1] < 1e-250),
              'B6 OC N=%d n=%d d=%d L=%g col %d' % (Nn, nn, dd, LL, c), (Hc[c - 1], hy[c - 1]))
        check(close(Bc[c - 1], bi[c - 1], 1e-8, 1e-300) or (bi[c - 1] < 1e-250 and Bc[c - 1] < 1e-250),
              'B6 OC binomial N=%d n=%d d=%d col %d' % (Nn, nn, dd, c), (Bc[c - 1], bi[c - 1]))
    # draft mode (every fourth column): computed columns agree, skipped hold -1, no binomial
    H2.execute('sz_OCCurve(4)')
    Hd = list(H2.execute('szOcH')); Bd = list(H2.execute('szOcB'))
    comp = [i for i in range(W_OC) if Hd[i] >= 0]
    check(comp[0] == 0 and comp[-1] == W_OC - 1 and all(close(Hd[i], hy[i], 1e-8, 1e-300) or hy[i] < 1e-250 for i in comp)
          and len(comp) == len(range(0, W_OC, 4)) + (0 if (W_OC - 1) % 4 == 0 else 1) and all(b_ == -1 for b_ in Bd),
          'B6 draft curve N=%d' % Nn, len(comp))
# readouts on the frames
for p in pg:
    lines = [t.text for t in p.texts]
    tl = [l for l in lines if l.startswith('true θ = ')]
    if not tl:
        continue
    mt = re.search(r'= ([\d.]+) \(K = (\d+)\): P\(support\) (.*)$', tl[0])
    th, K = float(mt.group(1)), int(mt.group(2))
    title = [l for l in lines if l.startswith('OC curve:')][0]
    mn = re.search(r'n = (\d+), ≤ (\d+) neg', title)
    nn, dd = int(mn.group(1)), int(mn.group(2))
    check(K == min(100, math.floor(round(th, 3) * 100 + 1e-9)) or K == math.floor(th * 100), 'B6 K = floor(theta N)', tl[0])
    check(mt.group(3) == pstr(stats.hypergeom.sf(nn - dd - 1, 100, K, nn)), 'B6 readout P(support) n=%d d=%d K=%d' % (nn, dd, K), tl[0])
    wl = [t.text for t in p.texts if t.text.startswith('Worst false claim')][0]
    if True:
        check(wl.endswith(pstr(stats.hypergeom.sf(nn - dd - 1, 100, 89, nn))), 'B6 worst-case line n=%d d=%d' % (nn, dd), wl)
dr = [p for p in pg if any('every 4th column' in t.text for t in p.texts)]
check(len(dr) >= 2, 'B6 the n drag drew draft frames', len(dr))
check(any(page_has(p, 'n = %d, ≤' % n_f) for p in pg), 'B6 title follows n')


# B7 weight page
def wt_ref(w, N, c=0.95):
    w = np.array(w, float); n = len(w); m = w.mean(); s = w.std(ddof=1)
    fpc = math.sqrt((N - n) / N)
    T = N * m; se = N * s / math.sqrt(n) * fpc
    t2 = stats.t.ppf(1 - (1 - c) / 2, n - 1); t1 = stats.t.ppf(c, n - 1)
    return T, se, T - t2 * se, T + t2 * se, T - t1 * se, t2, t1, fpc, m, s


def pround(v, d):
    """ROUND as the Prime does it: halves away from zero (on the decimal value
    of the double, 12 significant digits, as the Prime would hold it)."""
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal('%.12g' % v).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    return float(q) + 0


def wf(v):
    a = abs(v)
    d = 4 if a < 1 else 3 if a < 10 else 2 if a < 1000 else 1 if a < 100000 else 0
    return '%.*f' % (d, pround(v, d))


EXW = [0.512, 0.498, 0.505, 0.521, 0.487, 0.509, 0.515, 0.493, 0.502, 0.511]


def check_wpage(p, w, N, n=None, m=None, s=None, tag=''):
    if w is not None:
        T, se, lo, hi, lb, t2, t1, fpc, m, s = wt_ref(w, N)
        n = len(w)
    else:
        fpc = math.sqrt((N - n) / N); T = N * m; se = N * s / math.sqrt(n) * fpc
        t2 = stats.t.ppf(0.975, n - 1); t1 = stats.t.ppf(0.95, n - 1); lo = T - t2 * se; hi = T + t2 * se; lb = T - t1 * se
    ok = (page_has(p, 'Total = N = %s g, SE = %s g' % (wf(T), wf(se))) and
          page_has(p, '95%% CI: %s to %s g' % (wf(lo), wf(hi))) and
          page_has(p, 'One-sided 95%% lower bound: total ≥ %s g' % wf(lb)) and
          page_has(p, ' = %s g, s = %s g per unit' % (wf(m), wf(s))))
    check(ok, 'B7 weight page %s' % tag, [t.text for t in p.texts][:7])
    return T, lb


def s_b7(h):
    h.press('Enter'); h.choose('Weight'); h.choose('Illustrative')
    h.tap(150, 160)                 # the CI
    h.tap(150, 112)                 # a dot
    h.tap(60, 230); h.answer({'wlN': 12, 'wlM': 0.48, 'wlS': 0.03})   # Type
    h.tap(10, 230)                  # D1
    h.tap(300, 230); h.choose('Main menu')
    h.choose('Quit')


D1 = [0.45, 0.47, 0.52, 0.49, 0.50, 0.51, 0.46, 0.53]
h = run(s_b7, app_data={'D1': D1})
pg = [p for p in h.pages if page_has(p, 'Total net weight: N =')]
check(len(pg) == 5, 'B7 weight frames', len(pg))
T, lb = check_wpage(pg[0], EXW, 100, tag='example')
check(page_has(pg[0], '(illustrative numbers)'), 'B7 the example is labelled illustrative numbers')
il = [t.text for t in pg[1].texts if t.y == 192][0]
r = wt_ref(EXW, 100)
check(il == 't = %.3f (CI), %.3f (bound); FPC = %.4f' % (r[5], r[6], r[7]), 'B7 tap on the interval', il)
il = [t.text for t in pg[2].texts if t.y == 192][0]
check(re.match(r'unit \d+: 0\.\d{4} g \(mean 0\.5053 g\)', il) is not None, 'B7 tap on a dot', il)
check_wpage(pg[3], None, 100, n=12, m=0.48, s=0.03, tag='typed')
check(page_has(pg[3], 'no dots to plot'), 'B7 typed summary note')
T2, lb2 = check_wpage(pg[4], D1, 100, tag='D1')
check(abs(h.execute('SZ_TOT') - T2) < 1e-9 and abs(h.execute('SZ_TLB') - lb2) < 1e-9, 'B7 SZ_TOT, SZ_TLB')
dots = [s for s in pg[4].shapes if s.cmd == 'RECT_P' and s.args[-1] == 0x003CC8]
check(len(dots) == 2 * len(D1), 'B7 one dot per weight (two bars each)', len(dots))


def wrun(app, then):
    def s(h):
        h.press('Enter'); h.choose('Weight'); h.choose('From list D1'); then(h); h.choose('Quit')
    return run(s, app_data=app)


h = wrun(None, lambda h: None)
check(any('list D1' in ' '.join(m.lines) for m in h.msgboxes), 'B7 D1 missing: message, no error')
h = wrun({'D1': [0.5, -0.1, 0.4]}, lambda h: None)
check(any('positive' in ' '.join(m.lines) for m in h.msgboxes), 'B7 D1 with a negative weight refused')
h = wrun({'D1': [0.5] * 120}, lambda h: None)
check(any('raise N' in ' '.join(m.lines) for m in h.msgboxes), 'B7 D1 longer than N refused')
h = wrun({'D1': [0.5, 0.5, 0.5]}, lambda h: h.press('Esc'))
pz = [p for p in h.pages if page_has(p, 'Total net weight')]
check(len(pz) == 1 and page_has(pz[0], 'SE = 0.0000 g') and page_has(pz[0], 'CI: 50.00 to 50.00 g'),
      'B7 equal weights: SE 0, no error')


# n = N: the finite-population factor is 0
def s_b7b(h):
    h.press('Enter'); h.choose('Set up'); h.answer({'suN': 8}); h.choose('Weight'); h.choose('From list D1'); h.press('Esc'); h.choose('Quit')


h = run(s_b7b, app_data={'D1': D1})
pz = [p for p in h.pages if page_has(p, 'Total net weight')]
check(len(pz) == 1 and page_has(pz[0], 'SE = 0.0000 g'), 'B7 every unit weighed: SE = 0')


# B8 tables
def s_b8(h):
    h.press('Enter'); h.choose('Tables'); h.tap(10, 230); h.tap(10, 230); h.press('Left'); h.press('Esc')
    h.choose('Set up'); h.answer({'suPa': 0.5, 'suPb': 0.5}); h.choose('Tables'); h.press('Esc'); h.choose('Quit')


h = run(s_b8)
tb = [p for p in h.pages if page_has(p, 'Least n, all positive, c = 0.95')]
tp = [p for p in h.pages if page_has(p, 'Least n against N (log scale)')]
check(len(tb) == 3 and len(tp) == 2, 'B8 table and plot frames', (len(tb), len(tp)))
NS = [10, 20, 50, 100, 200, 500, 1000]
for pr_i, (a, b) in enumerate([(1, 1), (0.5, 0.5)]):
    p = tb[0] if pr_i == 0 else tb[-1]
    for row, N in enumerate(NS + [None]):
        y = 47 + row * 11
        vals = sorted([t for t in p.texts if t.y == y and t.x > 60], key=lambda t: t.x)
        got = [int(t.text) for t in vals]
        if N is None:
            exp = [bin_min_scan('0.95', '0.9', 0), None, bin_min_scan('0.95', '0.5', 0), None]
            n = 0
            while stats.beta.sf(0.9, a + n, b) < 0.95:
                n += 1
            exp[1] = n
            n = 0
            while stats.beta.sf(0.5, a + n, b) < 0.95:
                n += 1
            exp[3] = n
        else:
            exp = [hyp_min_exact(N, '0.95', '0.9', 0)[0] if N <= 300 else None,
                   next(m for m in range(N + 1) if bay_ok(N, m, '0.9', a, b, '0.95')),
                   hyp_min_exact(N, '0.95', '0.5', 0)[0] if N <= 300 else None,
                   next(m for m in range(N + 1) if bay_ok(N, m, '0.5', a, b, '0.95'))]
            for k, p0s in [(0, '0.9'), (2, '0.5')]:
                if exp[k] is None:
                    K0 = kreq(N, p0s) - 1
                    exp[k] = next(n for n in range(1, N + 1) if stats.hypergeom.sf(n - 1, N, K0, n) <= 0.05)
        check(got == exp, 'B8 table row N=%s prior a=%g' % (N, a), (got, exp))
check(page_has(tb[0], 'N = 10 needs 8 of 10, N = 1000 28'), 'B8 sentence computed from the table')
check(page_has(tb[-1], 'Beta(0.5, 0.5), Jeffreys'), 'B8 Jeffreys prior named')


# B9 enter a result, help, quit
def s_b9(h):
    h.press('Enter')
    h.choose('Enter a result'); h.answer({'obN': 40, 'obX': 38}); h.press('Esc')
    h.choose('Enter a result'); h.answer({'obN': 400, 'obX': 3})
    h.choose('Enter a result'); h.answer({'obN': 10, 'obX': 11})
    h.choose('Help'); h.press('Enter'); h.press('Enter'); h.press('Esc')
    h.choose('Help'); [h.press('Enter') for _ in range(8)]
    h.choose('Quit')


h = run(s_b9)
pg = [p for p in h.pages if page_has(p, 'Hypergeometric: claim K')]
P, LB = hyp_ref(100, '0.9', '0.95', 40, 2)
check(len(pg) == 1 and page_has(pg[0], 'P(X ≥ 38) %s' % pstr(P)) and page_has(pg[0], 'K ≥ %d (' % LB),
      'B9 entered result shown, P and bound', (pstr(P), LB))
check(page_has(pg[0], 'SUPPORTED' if P <= 0.05 else 'NOT supported'), 'B9 verdict for 38 of 40')
mb = [' '.join(m.lines) for m in h.msgboxes]
check(any('n must be a whole number from 1 to N = 100' in m for m in mb) and any('x must be a whole number from 0 to n = 10' in m for m in mb),
      'B9 entry refusals', mb)
hp = [p for p in h.pages if p.func == 'sz_HelpPg']
check(len(hp) == 3 + 8, 'B9 help pages (3 then Esc, then all 8)', len(hp))
h3 = [p for p in hp if page_has(p, 'Why N hardly matters')]
check(h3 and page_has(h3[0], 'least n 8 at N = 10, 23 at') and page_has(h3[0], 'never more than 29'), 'B9 help page 3 numbers computed')
for p in hp:
    n_lines = len([t for t in p.texts if 20 < t.y < 215])
    check(max(t.y for t in p.texts if t.y < 215) <= 212, 'B9 help text above the footer', p.texts[0].text)


# B12 the page menus, reached by Enter (every soft-key action has a key route)
def s_b12(h):
    h.press('Enter')
    h.choose('Hypergeometric'); h.press('Enter'); h.choose('Type the result'); h.answer({'obN': 50, 'obX': 49})
    h.press('Enter'); h.choose('Least n'); h.press('Enter'); h.choose('Back'); h.press('Esc')
    h.choose('Bayesian'); h.press('Enter'); h.choose('Next prior'); h.press('Esc')
    h.choose('Binomial'); h.press('Enter'); h.choose('N ' + '\u00d7'); h.press('Enter'); h.choose('N / 10'); h.press('Esc')
    h.choose('Weight'); h.choose('Illustrative'); h.press('Enter'); h.choose('Type n'); h.answer({'wlN': 5, 'wlM': 1.2, 'wlS': 0.1})
    h.press('Esc')
    h.choose('Tables'); h.press('Enter'); h.choose('Table or plot'); h.press('Enter'); h.choose('Main menu')
    h.choose('OC curve'); h.press('Enter'); h.choose('Zoom'); h.press('Esc')
    h.choose('Quit')


h = run(s_b12)
hp = [p for p in h.pages if page_has(p, 'Hypergeometric: claim K')]
check(any(page_has(p, 'Tested n = 50: x = 49 positive, 1 neg') for p in hp), 'B12 Enter > Type the result')
check(any(page_has(p, 'Tested n = 36: x = 35 positive, 1 neg') for p in hp), 'B12 Enter > Least n (1 negative: 36)')
check(any(page_has(p, 'Bayes: prior Beta(0.5, 0.5), Jeffreys') for p in h.pages), 'B12 Enter > Next prior')
check(any(page_has(p, 'Binomial approximation, N = 1000') for p in h.pages) and h.execute('szN') == 100, 'B12 Enter > N x 10, N / 10')
check(any(page_has(p, 'n = 5 weighed (typed summary)') for p in h.pages), 'B12 Enter > Type n, mean and SD')
check(any(page_has(p, 'Least n against N (log scale)') for p in h.pages), 'B12 Enter > Table or plot')
check(h.execute('szOcL') == 0.7, 'B12 Enter > Zoom')
check(all(len(it) <= 30 for c in h.chooses for it in c.items), 'B12 every CHOOSE line <= 30 characters',
      [it for c in h.chooses for it in c.items if len(it) > 30])


# B10 big and small N, every page; stale-key mode
def every_page(h, opening=True):
    if opening:
        h.press('Enter')
    for it in ['Hypergeometric', 'Binomial', 'Bayesian', 'OC curve', 'Tables']:
        h.choose(it)
        if it == 'OC curve':
            h.drag([(100, 28), (200, 28)])
        h.tap(60, 230); h.tap(10, 230); h.press('Esc')
    h.choose('Weight'); h.choose('Illustrative'); h.press('Esc')
    h.choose('Quit')


for Nn in [10000, 1, 2, 13]:
    def s(h, Nn=Nn):
        h.press('Enter'); h.choose('Set up'); h.answer({'suN': Nn, 'suD': 2})
        every_page(h, opening=False)
    tt = time.time()
    h = run(s)
    check(h.error is None, 'B10 N = %d every page, no error' % Nn, h.error)
    hp1 = [p for p in h.pages if page_has(p, 'Hypergeometric: claim K') and page_has(p, ' of %d' % Nn)]
    if hp1:
        K0 = kreq(Nn, '0.9') - 1
        hm = []
        for d in range(3):
            if Nn <= 300:
                hm.append(hyp_min_exact(Nn, '0.95', '0.9', d)[0])
            else:
                hm.append(next((n for n in range(d + 1, Nn + 1) if stats.hypergeom.sf(n - d - 1, Nn, K0, n) <= 0.05), -1))
        txt = ', '.join('none' if v < 0 else str(v) for v in hm)
        check(page_has(hp1[0], 'Least n (0, 1, 2 negatives): ' + txt), 'B10 N = %d least n' % Nn, txt)
    print('B10 N = %d: %d pages, %.1f s' % (Nn, len(h.pages), time.time() - tt))

h = run(lambda h: every_page(h), stale_keys=True)
check(len(h.stale_skips) == 0, 'B10 stale-key mode: no page skipped', h.stale_skips)

# ======================================================================
section('R  the second review, item by item (beta 1a)')
t0r = time.time()


def bay_ref_bisect(N, cs, p0s, a, b, large=False):
    """The least n by bisection on a SciPy reference (the condition is monotone: A11)."""
    c = float(cs)
    if large:
        ok = lambda n: stats.beta.sf(float(p0s), a + n, b) >= c - 1e-6 * (1 - c)
        lo, hi = -1, 1
        while not ok(hi):
            lo, hi = hi, hi * 2
    else:
        ok = lambda n: bay_ok(N, n, p0s, a, b, cs)
        lo, hi = -1, kreq(N, p0s)
    while hi - lo > 1:
        m = (lo + hi) // 2
        if ok(m):
            hi = m
        else:
            lo = m
    return hi


# R1 the searches: reviewer's slow cases (his SciPy values 5668, 5046, 9746, 323, 957, 142)
slow = [(10000, '0.9999', '0.999', 1, 1, 5668), (10000, '0.9999', '0.999', 0.5, 0.5, 5046),
        (10000, '0.9999', '0.999', 0.1, 100, 9746), (10000, '0.99', '0.99', 0.5, 0.5, 323),
        (10000, '0.95', '0.9', 1, 100, 957), (10000, '0.95', '0.9', 1, 10, 142), (10000, '0.95', '0.9', 0.5, 0.5, 18)]
for (N, cs, p0s, a, b, rv) in slow:
    H.globals_['szPrg'] = 0.0; H.globals_['szStop'] = 0.0
    tt = time.time(); v = ex('sz_BayMin(%d,%s,%s,%r,%r)' % (N, cs, p0s, a, b)); el = time.time() - tt
    sums = H.globals_['szPrg']; top = kreq(N, p0s)
    check(v == rv, 'R1 BayMin N=%d c=%s p0=%s a=%g b=%g = %d (review)' % (N, cs, p0s, a, b, rv), v)
    check(sums <= 2 * math.ceil(math.log2(top + 1)) + 3, 'R1 sums for that search within 2 log2(Kr) + 3', (sums, top))
    print('R1 N=%d c=%s p0=%s prior (%g, %g): n = %d, %d sums, %.2f s in the harness (beta 1 stepped)' % (N, cs, p0s, a, b, v, sums, el))
for (cs, p0s, a, b) in [('0.9999', '0.999', 0.1, 100), ('0.95', '0.9', 1, 100), ('0.95', '0.9', 10, 1), ('0.99', '0.5', 0.5, 0.5)]:
    H.globals_['szPrg'] = 0.0; H.globals_['szStop'] = 0.0
    v = ex('sz_BayMinL(%s,%s,%r,%r)' % (cs, p0s, a, b)); r = bay_ref_bisect(None, cs, p0s, a, b, large=True)
    check(v == r, 'R1 BayMinL c=%s p0=%s a=%g b=%g' % (cs, p0s, a, b), (v, r))
    check(H.globals_['szPrg'] <= 2 * math.ceil(math.log2(max(r, 1) + 1)) + 6, 'R1 BayMinL sums', H.globals_['szPrg'])
check(ex('sz_BayMinL(0.95,0.9,10,1)') == 19, 'R1 ENFSI in-text a = 10, b = 1: 19')
# typed priors on small N: the search = a full scan (and the condition is monotone)
random.seed(77); nm = 0
for _ in range(150):
    N = random.choice([5, 13, 30, 100, 300]); p0s = random.choice(['0.3', '0.5', '0.7', '0.9', '0.95', '0.99'])
    cs = random.choice(['0.8', '0.9', '0.95', '0.99', '0.999'])
    a = round(math.exp(random.uniform(math.log(0.1), math.log(100))), 2); b = round(math.exp(random.uniform(math.log(0.1), math.log(100))), 2)
    vals = [bayp_ref(N, n, n, p0s, a, b) for n in range(N + 1)]
    if any(vals[i + 1] < vals[i] - 1e-9 for i in range(N)):
        nm += 1
    r = next(n for n in range(N + 1) if bay_ok(N, n, p0s, a, b, cs))
    H.globals_['szStop'] = 0.0
    v = ex('sz_BayMin(%d,%s,%s,%r,%r)' % (N, cs, p0s, a, b))
    check(v == r, 'R1 BayMin typed prior N=%d c=%s p0=%s a=%g b=%g' % (N, cs, p0s, a, b), (v, r))
check(nm == 0, 'R1 P(claim | n all +) monotone in n for 150 typed priors', nm)


# Esc during the sums: Set up with a strong prior, then the Tables page with one
def s_r1(h):
    h.press('Enter'); h.choose('Set up'); h.answer({'suN': 10000, 'suPa': 1, 'suPb': 100})
    h.press(4, anytime=True)                       # Esc while Set up computes
    h.choose('Bayesian'); h.press('Esc')
    h.choose('Tables'); h.press(4, anytime=True)   # Esc while the table computes
    h.press('Esc')
    h.choose('Quit')


h = run(s_r1)
check(h.error is None, 'R1 Esc during the sums: no error', h.error)
check(h.execute('szYm') == -2 or h.execute('szYmL') == -2, 'R1 Esc stopped the Bayesian least n (-2)', (h.execute('szYm'), h.execute('szYmL')))
bp = [p for p in h.pages if p.texts and p.texts[0].text.startswith('Bayes: prior Beta(1, 100)')]
check(len(bp) >= 1 and page_has(bp[-1], 'Least n: this N stopped; N \u2192 \u221e stopped'), 'R1 the Bayesian page says "stopped"',
      [p.lines()[:6] for p in bp])
tb = [p for p in h.pages if page_has(p, 'Least n, all positive, c = 0.95')]
check(len(tb) == 1 and page_has(tb[0], 'stopped') and h.execute('szTbKey') == '', 'R1 Esc on the Tables page: "stopped", recomputed next time')
busy = [p for p in h.pages if page_has(p, 'Esc = stop. A large N or strong prior')]
check(len(busy) >= 1, 'R1 the busy box says Esc stops it and that it can take a minute')

# R2 the weight factor; ENFSI section 7's worked example typed in
H.globals_['szN'] = 100.0; H.globals_['szWn'] = 23.0; H.globals_['szWm'] = 0.265; H.globals_['szWs'] = 0.023
H.globals_['szC'] = 0.95; H.execute('sz_WtCalc()'); Wr = list(H.execute('szWr'))
hw = Wr[2] * Wr[1]
ref_hw = 100 * 0.023 / math.sqrt(23) * math.sqrt(77 / 100) * stats.t.ppf(0.975, 22)
check(abs(Wr[7] - math.sqrt(0.77)) < 1e-12 and round(Wr[7], 3) == 0.877, 'R2 FPC = sqrt(77/100) = 0.877 (ENFSI s7)', Wr[7])
check(abs(hw - ref_hw) < 1e-9 and round(hw, 3) == 0.873, 'R2 ENFSI example half-width 0.8728 (ENFSI prints 0.873)', hw)
check(round(100 * 0.023 / math.sqrt(23) * math.sqrt(0.77) * 2.074, 3) == 0.873, 'R2 ENFSI\'s 0.873 = its t 2.074 times the factor sqrt(0.77) = 0.8775')


def s_r2(h):
    h.press('Enter'); h.choose('Weight'); h.choose('Type'); h.answer({'wlN': 23, 'wlM': 0.265, 'wlS': 0.023})
    h.tap(150, 160); h.press('Esc'); h.choose('Quit')


h = run(s_r2)
wp = [p for p in h.pages if page_has(p, 'Total net weight')]
check(len(wp) == 2 and page_has(wp[0], '95% CI: 25.63 to 27.37 g (± 0.8728)') and page_has(wp[0], 'Total = N = 26.50 g'),
      'R2 the page shows 26.50 g, 95% CI 25.63 to 27.37 g (+/- 0.8728)', [t.text for t in wp[0].texts][:7])
check(page_has(wp[0], '√((N - n)/N)'), 'R2 the page names sqrt((N - n)/N)')
check(page_has(wp[1], 'FPC = 0.8775'), 'R2 the tap shows FPC = 0.8775')
src = open(SRC).read()
check('(szN - szWn) / szN)^0.5' in src and '(szN - szWn) / (szN - 1)' not in src, 'R2 the code uses (N - n)/N')

# R3 the Bayesian page and help page 6
h = run(lambda h: (h.press('Enter'), h.choose('Bayesian'), h.press('Esc'), h.choose('Help'),
                   [h.press('Enter') for _ in range(5)], h.press('Esc'), h.choose('Quit')))
bp = [p for p in h.pages if page_has(p, 'Bayes: prior Beta(1, 1)')]
check(bp and page_has(bp[0], 'Least n, all +, P ≥ 0.95: this N 22; N → ∞ 28'), 'R3 both least n side by side')
check(bp and page_has(bp[0], 'ENFSI Table 4 takes N → ∞ (it assumes N ≥ 50)'), 'R3 the ENFSI line')
h6 = [p for p in h.pages if page_has(p, 'Checking against ENFSI')]
check(len(h6) == 1 and page_has(h6[0], 'Its 28 (uniform prior,') and page_has(h6[0], 'beta-binomial gives 22')
      and page_has(h6[0], 'e.g. 23, 36, 46 for N = 100') and page_has(h6[0], '± 0.8728 g; ENFSI prints 26.500 ± 0.873 g'),
      'R3 help page 6 with its live numbers', [t.text for t in h6[0].texts] if h6 else None)
check(h6 and sum(1 for t in h6[0].texts if "'A large seizure is" in t.text) == 1 and sum(1 for t in h6[0].texts if "50).'" in t.text) == 1
      and sum(t.text.count("'") for t in h6[0].texts) == 4, 'R3 one short quotation (ENFSI Table 4 note; the other two apostrophes are possessives)')

# R4 the tie tolerance
check(ex('sz_Le(0.0500000046777, 0.05)') == 1 and ex('sz_Le(0.05000006, 0.05)') == 0, 'R4 sz_Le: 1E-6 relative to 1 - c')
check(ex('sz_Ge(0.95 - 0.00000004, 0.95)') == 1 and ex('sz_Ge(0.95 - 0.00000006, 0.95)') == 0, 'R4 sz_Ge: 1E-6 of 1 - c below c')
check(ex('sz_HypMin(5000,0.95,0.0501,0)') == 1, 'R4 the flip case N = 5000, p0 = 0.0501: least n 1 (exact: 250/5000 = 0.05)')
check(ex('sz_HypMin(10,0.9,0.95,0)') == 9, 'R4 the N = 10 tie: 9')
# 12-digit decimal emulation of the program's arithmetic (adapted from the second reviewer's prime12.py)
from decimal import Decimal as D, getcontext, ROUND_HALF_EVEN
getcontext().prec = 12; getcontext().rounding = ROUND_HALF_EVEN
LC = [+D(x) for x in ['0.99999999999980993', '676.5203681218851', '-1259.1392167224028', '771.32342877765313',
                      '-176.61502916214059', '12.507343278686905', '-0.13857109526572012',
                      '0.0000099843695780195716', '0.00000015056327351493116']]


def lng12(z):
    z = D(z); w = z; s_ = D(0)
    while w < D('0.5'):
        s_ = s_ - w.ln(); w = w + 1
    x = w - 1; a_ = LC[0]
    for i in range(1, 9):
        a_ = a_ + LC[i] / (x + i)
    t_ = x + D('7.5')
    return s_ + D('0.918938533204673') + (x + D('0.5')) * t_.ln() - t_ + a_.ln()


def hyps12(N, K, n, lo, hi):
    L = max(lo, 0, n - (N - K)); Hh = min(hi, n, K)
    if L > Hh:
        return D(0)
    A = min(max(((n + 1) * (K + 1)) // (N + 2), L), Hh)
    lnc = lambda a_, b_: lng12(a_ + 1) - lng12(b_ + 1) - lng12(a_ - b_ + 1)
    t_ = (lnc(K, A) + lnc(N - K, n - A) - lnc(N, n)).exp(); s_ = t_; k = A; t0 = t_
    while k < Hh:
        t_ = t_ * (K - k) * (n - k) / ((k + 1) * (N - K - n + k + 1)); k += 1; s_ = s_ + t_
    t_ = t0; k = A
    while k > L:
        t_ = t_ * k * (N - K - n + k) / ((K - k + 1) * (n - k + 1)); k -= 1; s_ = s_ + t_
    return s_


for (N, K0, a_) in [(5000, 250, '0.05'), (10000, 500, '0.05'), (1000, 50, '0.05'), (2000, 100, '0.05'), (10, 9, '0.1')]:
    n_ = 9 if N == 10 else 1
    p12 = hyps12(N, K0, n_, n_, n_)
    met_new = p12 <= D(a_) * (1 + D('0.000001')); met_old = p12 <= D(a_) * (1 + D('1E-9'))
    check(met_new, 'R4 12-digit tie N=%d: %s counted as met (1E-6)' % (N, p12), (str(p12), met_old))
    print('R4 12-digit emulation N=%5d: P = %s, exact %s, met with 1E-9: %s, with 1E-6: %s' % (N, p12, a_, met_old, met_new))
getcontext().prec = 28

# R5 the OC drags: a phantom reading and a key end them
H5 = []


def s_r5(h):
    h.press('Enter'); h.choose('OC curve')
    h.drag([(120, 28), (2147483647, 0), (250, 28)])        # knob drag, then a phantom reading
    # (a key pressed while the finger is down cannot be modelled: the harness's key polls answer
    # nothing while a finger is down; sz_DragOn's key exit is checked statically and on the device)
    h.press('Esc')
    h.choose('Quit')


h = run(s_r5)
check(h.error is None and not any(h.leftover()), 'R5 drags with a phantom reading and a held finger end; script used', (h.error, h.leftover()))
n120 = 1 + int(round((120 - 30) / 270 * 55)); n140 = 1 + int(round((140 - 30) / 270 * 55))
ocf = [p for p in h.pages if page_has(p, 'OC curve: N =')]
check(any(page_has(p, 'n = %d, ≤' % n120) for p in ocf) and not any(page_has(p, 'n = %d, ≤' % (1 + int(round(220 / 270 * 55)))) for p in ocf),
      'R5 the phantom reading ended the knob drag at n = %d (x = 250 never reached)' % n120)
check(h.execute('szNt') == n120, 'R5 after the phantom reading n stays %d' % n120, h.execute('szNt'))


def s_r5b(h):
    h.press('Enter'); h.choose('OC curve')
    h.drag([(150, 100), (150, 100), (150, 100), (150, 100), (151, 100)])
    h.press('Esc'); h.choose('Quit')


h = run(s_r5b)
ocf = [p for p in h.pages if page_has(p, 'OC curve: N =')]
check(len(ocf) == 4, 'R5 theta drag: a frame only when theta moves (open, 150, 151, after lift)', len(ocf))
src = open(SRC).read()
body = re.search(r'\nsz_DragOn\(\).*?\nEND;', src, re.S).group(0)
check('GETKEY' in body and '319' in body and '239' in body, 'R5 sz_DragOn reads keys and rejects off-screen readings')

# R6 the outline: four red LINE_P, no red-filled RECT_P on the hypergeometric page
h = run(lambda h: (h.press('Enter'), h.choose('Hypergeometric'), h.press('Esc'), h.choose('Quit')))
hp = [p for p in h.pages if page_has(p, 'Hypergeometric: claim K')][0]
redrect = [s for s in hp.shapes if s.cmd == 'RECT_P' and len(s.args) >= 5 and int(s.args[4]) == 0xFF0000]
redline = [s for s in hp.shapes if s.cmd == 'LINE_P' and len(s.args) >= 5 and int(s.args[4]) == 0xFF0000]
check(len(redrect) == 0 and len(redline) == 4, 'R6 observed bar: 4 red LINE_P, no red RECT_P', (len(redrect), len(redline)))
if len(redline) == 4:
    xs = sorted(set([s.args[0] for s in redline] + [s.args[2] for s in redline]))
    ys = sorted(set([s.args[1] for s in redline] + [s.args[3] for s in redline]))
    check(len(xs) == 2 and len(ys) == 2, 'R6 the four lines close a rectangle', (xs, ys))
mag = [s for s in hp.shapes if s.cmd == 'RECT_P' and len(s.args) >= 6 and int(s.args[5]) == 0xC800C8]
check(len(mag) >= 1, 'R6 the observed bar is magenta inside its outline')

# R7 glyphs
check('CHAR(8592)' not in src and 'CHAR(8645)' not in src and 'CHAR(8593)' not in src and 'CHAR(8595)' not in src,
      'R7 no unverified arrow glyphs')

# R8 widths at the defaults and at the reviewer's extremes
FW = {1: 6.5, 2: 8.0}


def width_audit(h, tag):
    bad_ = []
    for p in h.pages:
        for t_ in p.texts:
            txt = t_.text
            if not txt.strip():
                continue
            w = len(txt) * FW.get(int(t_.font or 1), 6.5)
            lim = min(t_.width or 320, 320 - t_.x)
            if w > lim + 0.5 and not re.fullmatch(r'[\d.−-]+', txt):
                bad_.append((txt, t_.font, t_.width, len(txt)))
    check(not bad_, 'R8 every line within its width (%s)' % tag, sorted(set(bad_))[:6])


def s_r8(vals):
    def s(h):
        h.press('Enter'); h.choose('Set up'); h.answer(vals)
        for it in ['Hypergeometric', 'Binomial', 'Bayesian', 'OC curve', 'Tables']:
            h.choose(it)
            if it == 'OC curve':
                h.drag([(100, 28), (290, 28)])
            if it == 'Tables':
                h.tap(20, 230)
            h.tap(60, 230); h.tap(10, 230); h.press('Esc')
        h.choose('Weight'); h.choose('Type'); h.answer({'wlN': min(9999, vals.get('suN', 100)), 'wlM': 12345.678, 'wlS': 2345.6})
        h.press('Esc')
        h.choose('Help'); [h.press('Enter') for _ in range(8)]
        h.choose('Quit')
    return s


for vals in [{}, {'suN': 10000, 'suD': 20, 'suC': 0.9999, 'suP': 0.999},
             {'suN': 9999, 'suD': 17, 'suC': 0.975, 'suP': 0.875, 'suPa': 0.25, 'suPb': 0.75},
             {'suN': 9999, 'suD': 1, 'suPa': 12.34, 'suPb': 99.12}]:
    h = run(s_r8(vals))
    check(h.error is None, 'R8 run %r: no error' % vals, h.error)
    width_audit(h, repr(vals))
hl = [l for l in re.findall(r'hpL := \{(.*?)\};', src, re.S)]
check(len(hl) == 8, 'R8 eight help pages', len(hl))

# R9 each page's key legend
h = run(lambda h: (h.press('Enter'), [ (h.choose(it), h.press('Esc')) for it in ['Hypergeometric', 'Binomial', 'Bayesian', 'OC curve', 'Tables']], h.choose('Quit')))


def legend(title):
    p = [p for p in h.pages if page_has(p, title)][0]
    return [t_.text for t_ in p.texts if t_.y == 192][0]


check(legend('Hypergeometric: claim') == '+/- = n, Left/Right = x, Ent = menu', 'R9 hypergeometric legend', legend('Hypergeometric: claim'))
check(legend('Binomial approximation') == 'Up/Down = neg, Left/Right = N, Ent = menu', 'R9 binomial legend')
check(legend('Bayes: prior') == '+/- = n, Left/Right = x, Ent = menu', 'R9 Bayesian legend')
check(legend('OC curve: N') == '+/- = n, Left/Right = θ, Up/Down = neg', 'R9 OC legend')
check(legend('Least n, all positive') == 'Left/Right = table or plot, Ent = menu', 'R9 tables legend', legend('Least n, all positive'))


def s_r9(h):
    h.press('Enter'); h.choose('Binomial'); h.press('Up'); h.press('Left'); h.press('Esc')
    h.choose('Bayesian'); h.press('Plus'); h.press('Left'); h.press('Esc')
    h.choose('OC curve'); h.press('Up'); h.press('Right'); h.press('Esc')
    h.choose('Quit')


h = run(s_r9)
check(h.execute('szN') == 10 and h.execute('szD') == 2, 'R9 binomial Up and OC Up each add a negative; binomial Left = N / 10', (h.execute('szN'), h.execute('szD')))
ocp = [p for p in h.pages if page_has(p, 'OC curve: N =')]
check(any(page_has(p, '≤ 2 neg') for p in ocp) and any(any(t_.text.startswith('true θ = 0.') for t_ in p.texts) for p in ocp),
      'R9 OC: Up adds a negative, Right moves theta')

# R10 the set-up messages
for vals, msg in [({'suD': 33}, 'Negatives set to 20 (0 to 20)'), ({'suD': -3}, 'Negatives set to 0 (0 to 20)'),
                  ({'suPa': 200}, 'Prior a, b kept in 0.1 to 100'), ({'suPb': 0.01}, 'Prior a, b kept in 0.1 to 100'),
                  ({'suPa': 0.333}, 'Prior a, b rounded to 2 decimals')]:
    h = setup_run(vals)
    mb = [' '.join(m.lines) for m in h.msgboxes]
    check(any(msg in m for m in mb) and all(not m.over_five for m in h.msgboxes), 'R10 message: %s' % msg, mb)
h = setup_run({'suPa': 0.333, 'suPb': 0.666})
check(h.execute('szA') == 0.33 and h.execute('szB') == 0.67, 'R10 a, b rounded to 0.33, 0.67')
h = setup_run({'suN': 0.4, 'suC': 0.2, 'suP': 0.9999, 'suD': 99, 'suPa': 500, 'suPb': 0.333})
check(all(not m.over_five for m in h.msgboxes), 'R10 every clamp at once: still one MSGBOX of at most 5 lines',
      [' '.join(m.lines) for m in h.msgboxes])

# R11 sources
check('https://www.unodc.org/documents/scientific/Drug_Sampling.pdf' in src and 'Stoel RD, Bolck A' in src and 'ST/NAR/38' in src,
      'R11 header: the ENFSI guideline with its UNODC link; Stoel & Bolck')
check('Cited for the METHOD only and NOT checked against the papers here' in src, 'R11 header marks the unread papers')
h = run(lambda h: (h.press('Enter'), h.choose('Help'), [h.press('Enter') for _ in range(8)], h.choose('Quit')))
h8 = [p for p in h.pages if page_has(p, '8  Sources')]
check(h8 and page_has(h8[0], 'unodc.org/documents/scientific/') and page_has(h8[0], 'Drug_Sampling.pdf')
      and page_has(h8[0], 'NOT checked here') and page_has(h8[0], 'Stoel & Bolck'), 'R11 help page 8')

# R12 the ENFSI tables (transcribed by the second reviewer, enfsi_cmp.py; source: ENFSI DWG 2009, UNODC ST/NAR/38)
Ns = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 5000, 10000]
T1 = {10: [3, 5, 8, 4, 6, 9], 20: [4, 6, 12, 5, 9, 15], 30: [4, 7, 15, 6, 10, 20], 40: [4, 7, 18, 6, 10, 23], 50: [4, 8, 19, 6, 11, 26],
      60: [4, 8, 20, 6, 11, 28], 70: [5, 8, 21, 7, 12, 30], 80: [5, 8, 22, 7, 12, 31], 90: [5, 8, 23, 7, 12, 32], 100: [5, 8, 23, 7, 12, 33],
      200: [5, 9, 26, 7, 13, 38], 300: [5, 9, 27, 7, 13, 40], 400: [5, 9, 27, 7, 13, 41], 500: [5, 9, 28, 7, 13, 41], 600: [5, 9, 28, 7, 13, 42],
      700: [5, 9, 28, 7, 13, 42], 800: [5, 9, 28, 7, 13, 42], 900: [5, 9, 28, 7, 13, 43], 1000: [5, 9, 28, 7, 13, 43], 5000: [5, 9, 29, 7, 13, 44],
      10000: [5, 9, 29, 7, 13, 44]}
T2 = {10: [5, 7, 7, 9, 10, -1, 6, 7, 8, 9, 10, -1], 20: [6, 8, 10, 13, 17, 20, 8, 10, 12, 14, 19, 20], 30: [7, 9, 11, 14, 22, 27, 8, 11, 14, 17, 25, 29],
      40: [7, 9, 12, 15, 26, 32, 9, 11, 15, 18, 30, 35], 50: [7, 10, 12, 16, 29, 36, 9, 12, 16, 20, 34, 41], 60: [7, 10, 12, 16, 31, 39, 9, 12, 16, 20, 38, 45],
      70: [7, 10, 13, 17, 32, 41, 10, 12, 17, 21, 40, 48], 80: [7, 10, 13, 17, 34, 43, 10, 12, 17, 21, 42, 51], 90: [7, 10, 13, 17, 35, 45, 10, 13, 17, 21, 44, 54],
      100: [7, 10, 13, 17, 36, 46, 10, 13, 17, 22, 46, 56], 200: [8, 10, 14, 18, 40, 53, 10, 13, 18, 24, 54, 67], 300: [8, 10, 14, 19, 42, 55, 10, 13, 19, 24, 57, 71],
      400: [8, 11, 14, 19, 43, 57, 10, 13, 19, 24, 58, 74], 500: [8, 11, 14, 19, 44, 58, 10, 14, 19, 24, 59, 75], 600: [8, 11, 14, 19, 44, 58, 10, 14, 19, 25, 60, 76],
      700: [8, 11, 14, 19, 44, 59, 11, 14, 19, 25, 61, 77], 800: [8, 11, 14, 19, 44, 59, 11, 14, 19, 25, 61, 77], 900: [8, 11, 14, 19, 45, 59, 11, 14, 19, 25, 61, 78],
      1000: [8, 11, 14, 19, 45, 59, 11, 14, 19, 25, 62, 78], 5000: [8, 11, 14, 19, 46, 61, 11, 14, 20, 25, 64, 81], 10000: [8, 11, 14, 19, 46, 61, 11, 14, 20, 25, 64, 81]}
T3 = {0: [5, 9, 29, 7, 13, 44], 1: [8, 14, 46, 11, 20, 64], 2: [11, 19, 61, 14, 25, 81]}
T4 = {(1, 1): [4, 8, 28, 6, 12, 43], (3, 1): [2, 6, 26, 4, 10, 41], (0.5, 0.5): [3, 6, 18, 5, 10, 32]}
T5 = {'0.5': (5, 5), '0.6': (6, 6), '0.7': (8, 9), '0.8': (12, 14), '0.9': (23, 28), '0.95': (39, 56)}
mism = []; ncell = 0
for N in Ns:
    i = 0
    for cs in ['0.95', '0.99']:
        for k in ['0.5', '0.7', '0.9']:
            g = ex('sz_HypMin(%d,%s,%s,0)' % (N, cs, k)); ncell += 1
            if g != T1[N][i]:
                mism.append(('T1', N, cs, k, 0, g, T1[N][i]))
            i += 1
    i = 0
    for cs in ['0.95', '0.99']:
        for k in ['0.5', '0.7', '0.9']:
            for d in [1, 2]:
                g = ex('sz_HypMin(%d,%s,%s,%d)' % (N, cs, k, d)); ncell += 1
                if g != T2[N][i]:
                    mism.append(('T2', N, cs, k, d, g, T2[N][i]))
                i += 1
for d in T3:
    i = 0
    for cs in ['0.95', '0.99']:
        for k in ['0.5', '0.7', '0.9']:
            g = ex('sz_BinMin(%s,%s,%d)' % (cs, k, d)); ncell += 1
            if g != T3[d][i]:
                mism.append(('T3', cs, k, d, g, T3[d][i]))
            i += 1
for ab in T4:
    i = 0
    for cs in ['0.95', '0.99']:
        for k in ['0.5', '0.7', '0.9']:
            H.globals_['szStop'] = 0.0
            g = ex('sz_BayMinL(%s,%s,%s,%s)' % (cs, k, ab[0], ab[1])); ncell += 1
            if g != T4[ab][i]:
                mism.append(('T4', ab, cs, k, g, T4[ab][i]))
            i += 1
H.globals_['szStop'] = 0.0
g = ex('sz_BayMinL(0.95,0.9,10,1)'); ncell += 1
if g != 19:
    mism.append(('T4ex', g, 19))
for k, (a100, a1000) in T5.items():
    for N, want in [(100, a100), (1000, a1000)]:
        g = ex('sz_HypMin(%d,0.95,%s,0)' % (N, k)); ncell += 1
        if g != want:
            mism.append(('T5', N, k, g, want))
check(ncell == 427 and mism == [('T2', 90, '0.99', '0.7', 2, 22.0, 21)], 'R12 ENFSI tables: 426 of 427 agree; the one is ENFSI\'s misprint', (ncell, mism))
p21 = hyp_tail_exact(90, 62, 21, 19, 21); p22 = hyp_tail_exact(90, 62, 22, 20, 22)
check(kreq(90, '0.7') - 1 == 62 and p21 > Fr(1, 100) and p22 <= Fr(1, 100) and round(float(p21), 6) == 0.01115 and round(float(p22), 6) == 0.007561,
      'R12 exact: P(X >= 19 | 90, 62, 21) = %.6f > 0.01, at n = 22 %.6f: the least n is 22' % (float(p21), float(p22)))
print('R12 ENFSI tables: %d cells, mismatches %r' % (ncell, mism))

# R13 style
check('szWRNG is a deliberately darker red' in src, 'R13 the szWRNG comment')

# G  beta 1a against beta 1: the routines that changed
def routines(path):
    txt = open(path).read()
    out = {}
    for m in re.finditer(r'\n((?:EXPORT )?(sz_\w+|SeizureLab)\([^)]*\)\nBEGIN.*?\nEND;)', txt, re.S):
        out[m.group(2)] = m.group(1)
    return out


r0 = routines(SRC1); r1 = routines(SRC)
changed = sorted(k for k in r1 if k in r0 and r0[k] != r1[k]); added = sorted(k for k in r1 if k not in r0); gone = sorted(k for k in r0 if k not in r1)
EXPECT_CHANGED = ['sz_BayDraw', 'sz_BayMin', 'sz_BayMinL', 'sz_BinDraw', 'sz_BinTap', 'sz_Busy', 'sz_Ge', 'sz_Help', 'sz_HypDraw',
                  'sz_Init', 'sz_Le', 'sz_NStr', 'sz_OCDraw', 'sz_OCFit', 'sz_OCPage', 'sz_Open', 'sz_PrName', 'sz_PrNext',
                  'sz_Recalc', 'sz_Setup',
                  'sz_TabCalc', 'sz_TabDraw', 'sz_TabPlot', 'sz_WtCalc', 'sz_WtDraw']
EXPECT_ADDED = ['sz_BayOK', 'sz_BaySrch', 'sz_DragOn', 'sz_EscHit', 'sz_Fit']
check(changed == EXPECT_CHANGED and added == EXPECT_ADDED and gone == [], 'G routines changed / added are exactly the listed ones',
      (changed, added, gone))
print('G changed: %s\nG added: %s' % (', '.join(changed), ', '.join(added)))
print('Part R: %.1f s' % (time.time() - t0r))

# B11 every page of every run
nres = 0
for p in ALLPAGES:
    if p.func == 'sz_Show':
        nres += 1
        check(page_has(p, DISC), 'B11 disclaimer on a result page', p.texts[0].text if p.texts else '')
    for t in p.texts:
        w = min(t.est_width, t.width) if t.width else t.est_width
        if t.text.strip():
            check(t.x >= 0 and t.x + w <= 321 and 0 <= t.y <= 230, 'B11 text inside the screen', (t.text, t.x, t.y))
check(len(SCI) == 0, 'B11 no scientific number on any page (h.sci_strings)', SCI[:5])
print('B11 %d pages, %d with soft keys; scientific strings: %d' % (len(ALLPAGES), nres, len(SCI)))
print('Part B: %.1f s' % (time.time() - t0))

# ======================================================================
section('C  static')
raw = open(SRC, 'rb').read()
check(all(b < 128 for b in raw), 'C pure ASCII')
check(b'\r' not in raw, 'C LF line endings')
lines = raw.decode().split('\n')
check(lines[0] == '#pragma mode( separator(.,;) integer(h32) )', 'C pragma line')
check('// SEIZURELAB - beta 1a  (21 Oct 2026)' in raw.decode(), 'C version line')
check('// DISCLAIMER: a teaching and demonstration aid. Not validated for' in raw.decode(), 'C header disclaimer')
for i, l in enumerate(lines):
    code = l.split('//')[0]
    if re.match(r'\s*LOCAL\s', code) and '(' not in code:
        nm = [x for x in code.strip()[5:].rstrip(';').split(',') if x.strip()]
        check(len(nm) <= 6, 'C LOCAL <= 6 names line %d' % (i + 1), l)
check(len(re.findall(r'\d\.?\d*e[-+]?\d', '\n'.join(l.split('//')[0] for l in lines))) == 0, 'C no lowercase exponent')
check(re.search(r'\bRETURN\s+mnS;', raw.decode()) is not None and 'PRINT(' not in raw.decode(), 'C ends with RETURN, no PRINT')

# the header's file map points at the section banners
fm = re.findall(r'^//\s+(\d+)-\s*(\d+)\s+(.*)$', raw.decode(), re.M)
check(len(fm) == 11 and int(fm[-1][1]) == len(lines) - (1 if lines[-1] == '' else 0), 'C file map covers the file', fm[-1:])
for lo, hi, what in fm[1:]:
    check(lines[int(lo) - 1].startswith('// ----') and lines[int(lo)].startswith('// '), 'C file map: section at line %s' % lo, lines[int(lo)][:40])
# nice steps in binary: 0.2 must stay 0.2 (0.2/0.1 = 2.0000000000000004)
for v_, r_ in [(0.2, 0.2), (0.05, 0.05), (0.25, 0.5), (2, 2), (7, 10), (0.0125, 0.02), (1, 1)]:
    check(abs(ex('sz_Nice(%r)' % v_) - r_) < 1e-12, 'C sz_Nice(%g) = %g' % (v_, r_), ex('sz_Nice(%r)' % v_))

print('\n%d checks, %d failures' % (NCHK, NFAIL))
if FAILS:
    print('first failures:')
    for f in FAILS[:30]:
        print('  ', f)
sys.exit(1 if NFAIL else 0)
