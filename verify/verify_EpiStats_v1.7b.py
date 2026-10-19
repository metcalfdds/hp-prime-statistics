#!/usr/bin/env python3
"""verify_EpiStats_v1.7b.py -- checks for EpiStats v1.7b (HP Prime PPL), 17 Oct 2026: the two string
rules of emulator round 2 (INSTRING("", ...) is "Invalid input"; STRING(x, 2, d) turns scientific
when 0 < |x| < 10^-d).  Built from verify_EpiStats_v1.7a.py: every check is kept, and every
harness run is now on ppl_run_v3d (which models both rules); E runs the v1.6 suite on v3d too.
New: F (the v1.7b fixes, each against v1.7a in v3d) and G2 (v1.7b against v1.7a), and the list
of every scientific STRING result of every run (h.sci_strings), which must be empty for v1.7b.

(The v1.7a docstring follows; "v3b" there now reads "v3d".)

verify_EpiStats_v1.7a.py -- checks for EpiStats v1.7a (HP Prime PPL), 17 Oct 2026: the CAS call
form that CASProbe beta 1b found on the emulator.  Built from verify_EpiStats_v1.7.py: every check
is kept; B and D run in harness v3b, which models the calculator's CAS (CAS of a variable
unevaluated, the Prime's printing, a CAS string as a PPL string); C also reads every closed form
in the Prime's printing; G (new) runs v1.7 itself in v3b and compares v1.7a with v1.7.  New or
changed checks are marked "1.7a".

  A. The new formulas, written in Python exactly as the PPL computes them, against
     statsmodels / SciPy:
       A1 Clopper-Pearson (es_CPB / es_CPInt) vs proportion_confint(method='beta'),
          every k of n = 1..60 plus n = 100..2000, six levels (11,670 intervals);
       A2 mid-P vs an independent brentq root of the mid-P tail equations;
       A3 the conditional MLE odds ratio and its exact CI (es_NCFill / es_NCEval /
          es_NCRoot / es_CondOR) vs scipy.stats.contingency.odds_ratio(kind=
          'conditional') and confidence_interval(), 460 tables, with each answer's
          residual in its defining equation.
  B. The PPL routines THEMSELVES in the run harness v3 (ppl_run_v3.py): es_CPInt over
     a grid vs statsmodels, mid-P, BINOMIAL calls per interval (the G1 cost), es_CondOR
     vs SciPy, es_BinCheck with a wrong BINOMIAL_CDF argument order, and the routine
     text against CICatcher beta 2's copy.
  C. Every CAS template the program can build, run through desktop Giac (icas), vs
     Python fractions: the derivative and its check (Help F), the exact fraction under
     the root for representative and edge tables, the k = 0 / k = n closed forms.
  D. End to end in the harness, once with cas='giac' and once with cas='fail': module 1
     (page 1 tabs, page 7), EpiStats2x2 for every conditional-OR state, module 2's risk
     bars, module 3's page 6 with taps, Help E and F; the CAS calls logged per event.
  E. The v1.6 verification suite (verify_EpiStats.py, 203 checks) run against v1.7.

  G. 1.7a: v1.7 in harness v3b (its es_Cas returns its own text, which page 6 and Help F would
     have shown as CAS answers), and v1.7a against v1.7 (only es_Cas differs).

  F. 1.7b: es_Cas with a failed CAS call (module 3 page 6 and Help F end to end, cas='fail': the
     decimal and the "decimal" badge, no error; v1.7a in v3d stops with "Invalid input" on the same
     run); targeted tables that push a fixed-decimal display below 10^-d on every page that can
     reach it (v1.7a in v3d prints scientific there, v1.7b never does); the static sweep of every
     STRING(x, 2, d) call and of INSTRING / LEFT / MID / RIGHT.
  G2. 1.7b: the routines that differ from v1.7a, and nothing else.

Run:  python3 verify_EpiStats_v1.7b.py      (numpy, scipy, statsmodels, icas, the harness v3d)
"""
import math, os, re, sys, time, subprocess, tempfile
from fractions import Fraction
import numpy as np
from scipy import stats
from scipy.optimize import brentq
from scipy.stats.contingency import odds_ratio
from scipy.stats import nchypergeom_fisher as NH
from statsmodels.stats.proportion import proportion_confint

HERE = os.path.dirname(os.path.abspath(__file__))
PPL = os.path.join(HERE, 'EpiStats_v1.7b.txt')
V17A = os.path.join(HERE, 'EpiStats_v1.7a.txt')
V17 = os.path.join(HERE, 'EpiStats_v1.7.txt')
CQ = os.path.join(HERE, 'CICatcher_beta2a.txt')
sys.path.insert(0, HERE)
import ppl_run_v3d                                                   # noqa: E402
from ppl_run_v3d import Harness, PPLError, giac_eval, prime_print   # noqa: E402

# 1.7b: every harness made in this run is kept, and every scientific STRING result is
# recorded with the routine that printed it, so the end of the run can list them all
HARNESSES = []
_h_init = Harness.__init__
_h_sh = Harness._string_home


def _init(self, path, *a, **k):
    _h_init(self, path, *a, **k)
    self.vpath = os.path.basename(path)
    self.sci_where = []
    HARNESSES.append(self)


def _sh(self, a):
    n0 = len(self.sci_strings)
    r = _h_sh(self, a)
    if len(self.sci_strings) > n0:
        self.sci_where.append((self._fstack[-1][0] if self._fstack else '?', self.sci_strings[-1][2]))
    return r


Harness.__init__ = _init
Harness._string_home = _sh
say = print

FAILS = []
NCHK = [0]


def check(ok, what):
    NCHK[0] += 1
    print(('  ok    ' if ok else '  FAIL  ') + what)
    if not ok:
        FAILS.append(what)


# ============================================================================ mirrors
CALLS = [0]


def BCDF(n, p, k):
    CALLS[0] += 1
    return stats.binom.cdf(k, n, p)


def BPDF(n, p, k):
    CALLS[0] += 1
    return stats.binom.pmf(k, n, p)


def cpb(k, n, a2, side, mid, guess):
    """es_CPB, line for line"""
    if side == 1 and k <= 0: return 0.0, 0
    if side == 2 and k >= n: return 1.0, 0
    if side == 1 and k >= n: return ((1 + mid) * a2) ** (1.0 / n), 0
    if side == 2 and k <= 0: return 1 - ((1 + mid) * a2) ** (1.0 / n), 0
    lo, hi = 0.0, 1.0
    p = guess if 0 < guess < 1 else k / n
    it = 0
    while True:
        it += 1
        c0 = c1 = 0.0
        if side == 2 or mid == 1: c0 = BCDF(n, p, k)
        if side == 1 or mid == 1: c1 = BCDF(n, p, k - 1)
        if mid == 0:
            if side == 1:
                h = (1 - c1) - a2; d = n * BPDF(n - 1, p, k - 1)
            else:
                h = a2 - c0; d = n * BPDF(n - 1, p, k)
        else:
            d = n * (BPDF(n - 1, p, k) + BPDF(n - 1, p, k - 1)) / 2
            h = (1 - (c0 + c1) / 2) - a2 if side == 1 else a2 - (c0 + c1) / 2
        if h == 0: return p, it
        if h < 0: lo = p
        else: hi = p
        q = -1.0
        if d > 0: q = p - h / d
        go = True
        if d > 0 and abs(q - p) <= 1e-9 * p:
            go = False
        else:
            if q <= lo or q >= hi: q = (lo + hi) / 2
            if hi - lo <= 1e-9 * p: go = False
        if it >= 100: go = False
        p = q
        if not go: return p, it


def cpint(k, n, a2, mid):
    """es_CPInt: the Wilson interval at the same level is the starting guess"""
    if n <= 0: return 0.0, 1.0, 0
    z = stats.norm.ppf(1 - a2); ph = k / n
    den = 1 + z * z / n; cen = (ph + z * z / (2 * n)) / den
    hw = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
    lo, i1 = cpb(k, n, a2, 1, mid, cen - hw)
    hi, i2 = cpb(k, n, a2, 2, mid, cen + hw)
    return lo, hi, max(i1, i2)


def midp_ref(k, n, a2):
    def tails(p):
        c0 = stats.binom.cdf(k, n, p); c1 = stats.binom.cdf(k - 1, n, p) if k > 0 else 0.0
        return 1 - 0.5 * (c0 + c1), 0.5 * (c0 + c1)
    lo = 0.0 if k == 0 else brentq(lambda p: tails(p)[0] - a2, 1e-300, 1, xtol=1e-15, rtol=1e-15)
    hi = 1.0 if k == n else brentq(lambda p: tails(p)[1] - a2, 0, 1 - 1e-16, xtol=1e-15, rtol=1e-15)
    return lo, hi


def nc_fill(a, b, c, d):
    r1 = a + b; c1 = a + c; d0 = d - a
    lo = max(0, -d0); hi = min(r1, c1)
    L = [0.0]
    for i in range(lo, hi):
        L.append(L[-1] + math.log((c1 - i) * (r1 - i) / ((i + 1) * (d0 + i + 1))))
    return L, lo, hi


def nc_eval(L, lo, hi, a, t, count):
    top = hi - lo
    mlo, mhi = 0, top
    while mlo < mhi:
        mm = (mlo + mhi) // 2
        if L[mm + 1] - L[mm] + t > 0: mlo = mm + 1
        else: mhi = mm
    m = mlo; ar = a - lo
    Z = S1 = S2 = PL = L1 = PH = H1 = 0.0
    for direction in (1, 2):
        j = m if direction == 1 else m + 1
        g = (L[j] - L[m]) + (j - m) * t if j <= top else -100
        while g > -46:
            w = math.exp(g); count[0] += 1; dj = j - m
            Z += w; S1 += dj * w; S2 += dj * dj * w
            if j <= ar: PL += w; L1 += dj * w
            if j >= ar: PH += w; H1 += dj * w
            j += -1 if direction == 1 else 1
            g = -100 if (j < 0 or j > top) else (L[j] - L[m]) + (j - m) * t
    E = S1 / Z; V = max(0.0, S2 / Z - E * E)
    return [lo + m + E, V, PL / Z, (lo + m + L1 / PL) if PL > 0 else 0, PH / Z, (lo + m + H1 / PH) if PH > 0 else 0]


def nc_root(L, lo, hi, a, kind, a2, t0, count):
    tl, th = -60.0, 60.0
    t = min(59.0, max(-59.0, t0)); it = 0
    while True:
        it += 1
        v = nc_eval(L, lo, hi, a, t, count)
        f = df = 0.0
        if kind == 1: f = v[0] - a; df = v[1]
        if kind == 2:
            if v[2] > 0: f = math.log(a2) - math.log(v[2]); df = v[0] - v[3]
            else: f = 1000.0
        if kind == 3:
            if v[4] > 0: f = math.log(v[4]) - math.log(a2); df = v[5] - v[0]
            else: f = -1000.0
        if f == 0: return t, it
        if f < 0: tl = t
        else: th = t
        q = tl - 1
        if df > 0: q = t - f / df
        go = True
        if df > 0 and abs(q - t) < 1e-9:
            go = False
        else:
            if q <= tl or q >= th: q = (tl + th) / 2
            if th - tl < 1e-9: go = False
        if it >= 100: go = False
        t = q
        if not go: return t, it


def cond_or(a, b, c, d, a2=0.025):
    """es_CondOR: {MLE, low, high, state}, plus iterations and EXP terms"""
    N = a + b + c + d
    if N > 2000: return (0, 0, 0, 4), 0, 0
    if min(a + b, c + d, a + c, b + d) == 0: return (0, 0, 0, 3), 0, 0
    L, lo, hi = nc_fill(a, b, c, d)
    h = 0.5 if a * b * c * d == 0 else 0.0
    lor = math.log((a + h) * (d + h) / ((b + h) * (c + h)))
    se = math.sqrt(1 / (a + h) + 1 / (b + h) + 1 / (c + h) + 1 / (d + h))
    cnt = [0]; its = 0
    st = 1 if a == lo else (2 if a == hi else 0)
    mle = lw = up = 0.0
    if st == 0:
        t, i = nc_root(L, lo, hi, a, 1, a2, lor, cnt); mle = math.exp(t); its = max(its, i)
    if a < hi:
        t, i = nc_root(L, lo, hi, a, 2, a2, lor + 1.959964 * se, cnt); up = math.exp(t); its = max(its, i)
    if a > lo:
        t, i = nc_root(L, lo, hi, a, 3, a2, lor - 1.959964 * se, cnt); lw = math.exp(t); its = max(its, i)
    return (mle, lw, up, st), its, cnt[0]


def sigtxt(v):
    if v <= 0: return '0'
    if v < 1e-6: return '< 0.000001'
    d = max(0, min(6, 2 - math.floor(math.log10(v))))
    return '%.*f' % (d, v)


def pct_ci(lo, hi):
    return '(%.1f-%.1f%%)' % (100 * lo, 100 * hi)


# ============================================================================ A
def part_a():
    print('=' * 78)
    print('A. The formulas as the PPL computes them, against statsmodels / SciPy')
    print('=' * 78)
    t0 = time.time()
    levels = [0.5, 0.8, 0.9, 0.95, 0.99, 0.999]
    grid = [(k, n) for n in range(1, 61) for k in range(0, n + 1)]
    grid += [(k, n) for n in (100, 200, 500, 1000, 2000)
             for k in sorted(set([0, 1, 2, 3, 5, n // 10, n // 3, n // 2, n - 3, n - 1, n]))]
    print('\nA1. Clopper-Pearson vs proportion_confint(method="beta")')
    print('    level   intervals  worst |diff|   worst rel (low>0)  max passes  mean BINOMIAL calls/interval')
    allw = 0; allit = 0; total = 0
    for L in levels:
        a2 = (1 - L) / 2; w = 0; wr = 0; mi = 0; CALLS[0] = 0
        for k, n in grid:
            lo, hi, it = cpint(k, n, a2, 0)
            rl, rh = proportion_confint(k, n, alpha=1 - L, method='beta')
            rl = 0.0 if np.isnan(rl) else rl; rh = 1.0 if np.isnan(rh) else rh
            w = max(w, abs(lo - rl), abs(hi - rh)); mi = max(mi, it)
            if rl > 0: wr = max(wr, abs(lo - rl) / rl)
        print('    %-6s  %9d  %12.2e  %17.2e  %10d  %8.1f' % (L, len(grid), w, wr, mi, CALLS[0] / len(grid)))
        allw = max(allw, w); allit = max(allit, mi); total += len(grid)
    check(allw < 1e-8, 'Clopper-Pearson: %d intervals, worst |difference| from statsmodels %.1e (target 1E-8)' % (total, allw))
    check(allit <= 20, 'at most %d passes (Newton steps or halvings) per end' % allit)
    print('\nA2. mid-P vs an independent brentq on the mid-P tails (levels 90 %, 95 %, 99 %; n = 1..60)')
    w = 0
    for L in (0.9, 0.95, 0.99):
        for k, n in grid[:1890]:
            ml, mh, _ = cpint(k, n, (1 - L) / 2, 1)
            rl, rh = midp_ref(k, n, (1 - L) / 2)
            w = max(w, abs(ml - rl), abs(mh - rh))
    check(w < 1e-8, 'mid-P: worst |difference| %.1e over 5,490 intervals' % w)
    # mid-P never wider than Clopper-Pearson, Clopper-Pearson never inside Wilson's... check nesting
    bad = 0
    for k, n in grid[:1890]:
        lo, hi, _ = cpint(k, n, 0.025, 0); ml, mh, _ = cpint(k, n, 0.025, 1)
        if ml < lo - 1e-12 or mh > hi + 1e-12: bad += 1
    check(bad == 0, 'mid-P always lies inside Clopper-Pearson (%d exceptions over 1,890 intervals at 95 %%)' % bad)

    print('\nA3. Conditional MLE OR and exact CI vs scipy.stats.contingency.odds_ratio')
    tables = [(12, 5, 8, 30), (3, 1, 1, 3), (1, 9, 11, 3), (10, 4, 4, 10), (7, 15, 58, 472), (40, 60, 20, 80),
              (5, 95, 2, 98), (0, 5, 3, 10), (5, 0, 3, 10), (2, 3, 0, 4), (4, 0, 0, 4), (1, 1, 1, 1),
              (700, 300, 280, 700), (999, 1, 1, 999), (1, 1000, 1000, 1), (15, 5, 30, 30), (40, 30, 20, 60),
              (1, 0, 0, 1), (0, 1, 1, 0), (2, 0, 1, 0), (10, 90, 20, 80), (1, 299, 0, 300)]
    rng = np.random.default_rng(7)
    tables += [tuple(int(x) for x in rng.integers(0, 40, 4)) for _ in range(400)]
    tables += [tuple(int(x) for x in rng.integers(0, 500, 4)) for _ in range(40)]
    worst = 0; worst_res = 0; mx_it = 0; mx_terms = 0; n_ok = 0; bad_res = []; n4 = [0]
    for tb in tables:
        a, b, c, d = tb
        r, its, terms = cond_or(a, b, c, d)
        res = odds_ratio(np.array([[a, b], [c, d]]), kind='conditional')
        ci = res.confidence_interval(0.95)
        if r[3] == 3:
            if not (np.isnan(res.statistic) and ci.low == 0 and math.isinf(ci.high)):
                FAILS.append('state 3 vs scipy %s' % (tb,))
            continue
        if r[3] == 4:                  # N > 2000: not computed, by design (Fisher's cap)
            n4[0] += 1
            continue
        want = (res.statistic, ci.low, ci.high)
        got = (r[0] if r[3] != 2 else math.inf, r[1], r[2] if r[3] != 2 else math.inf)
        M, n_, N_ = a + b + c + d, a + b, a + c
        for nm, g, w_ in zip(('mle', 'low', 'high'), got, want):
            if math.isinf(w_) or w_ == 0:
                if not (g == w_ or (math.isinf(w_) and math.isinf(g))):
                    FAILS.append('edge %s %s: %r vs %r' % (tb, nm, g, w_))
                continue
            rel = abs(g / w_ - 1)
            if rel > worst:
                worst = rel
            if rel > 1e-9:       # say whose answer solves its equation better
                if nm == 'mle': fg, fw = NH.mean(M, n_, N_, g) - a, NH.mean(M, n_, N_, w_) - a
                elif nm == 'high': fg, fw = NH.cdf(a, M, n_, N_, g) - 0.025, NH.cdf(a, M, n_, N_, w_) - 0.025
                else: fg, fw = NH.sf(a - 1, M, n_, N_, g) - 0.025, NH.sf(a - 1, M, n_, N_, w_) - 0.025
                bad_res.append((rel, tb, nm, g, w_, fg, fw))
        mx_it = max(mx_it, its); mx_terms = max(mx_terms, terms); n_ok += 1
    small = [x for x in bad_res if abs(x[5]) > abs(x[6]) * 10 + 1e-14]
    print('    %d tables compared; %d with an empty margin (undefined, CI (0, inf), as SciPy); %d with N > 2000 '
          '(not computed, by design)' % (n_ok, len(tables) - n_ok - n4[0], n4[0]))
    print('    worst relative difference from SciPy: %.2e; max passes per root %d; max EXP terms per table %d'
          % (worst, mx_it, mx_terms))
    for rel, tb, nm, g, w_, fg, fw in sorted(bad_res, reverse=True)[:4]:
        print('      %s %-4s ours %.12g  scipy %.12g  rel %.1e   residual ours %.1e, scipy %.1e'
              % (tb, nm, g, w_, rel, fg, fw))
    check(worst < 1e-6, 'conditional OR: worst relative difference from SciPy %.1e' % worst)
    check(not small, 'wherever the two differ by more than 1E-9, our answer solves its equation at least as well '
          '(%d differ; SciPy\'s brentq stops at an ABSOLUTE 1E-13 in psi)' % len(bad_res))
    check(mx_it <= 10, 'at most %d passes per root (bisection on ln psi with Newton steps)' % mx_it)
    for tb in ((12, 5, 8, 30), (7, 15, 58, 472), (700, 300, 280, 700)):
        r, its, terms = cond_or(*tb)
        res = odds_ratio(np.array([[tb[0], tb[1]], [tb[2], tb[3]]])); ci = res.confidence_interval()
        print('    %-18s MLE %.6f (%.6f-%.6f)  scipy %.6f (%.6f-%.6f)  %d EXP terms'
              % (tb, r[0], r[1], r[2], res.statistic, ci.low, ci.high, terms))
    print('  [A: %.0f s]' % (time.time() - t0))


# ============================================================================ B
def part_b():
    print('\n' + '=' * 78)
    print('B. The PPL routines themselves, in the harness (ppl_run_v3d)')
    print('=' * 78)
    h = Harness(PPL, strict=True, cas='giac')
    w = 0; wm = 0; ncall = []; cnt = 0
    t0 = time.time()
    for L in (0.8, 0.95, 0.999):
        a2 = (1 - L) / 2
        for n in list(range(1, 31)) + [50, 100, 500, 2000]:
            ks = range(n + 1) if n <= 30 else sorted(set([0, 1, 2, n // 7, n // 2, n - 1, n]))
            for k in ks:
                h.stat_calls[:] = []
                lo, hi = h.call('es_CPInt', k, n, a2, 0)
                ncall.append(len([s for s in h.stat_calls if s[0].startswith('BINOMIAL')]))
                rl, rh = proportion_confint(k, n, alpha=1 - L, method='beta')
                rl = 0.0 if np.isnan(rl) else rl; rh = 1.0 if np.isnan(rh) else rh
                w = max(w, abs(lo - rl), abs(hi - rh)); cnt += 1
                if L == 0.95 and n <= 30:
                    ml, mh = h.call('es_CPInt', k, n, a2, 1)
                    rml, rmh = midp_ref(k, n, a2)
                    wm = max(wm, abs(ml - rml), abs(mh - rmh))
    check(w < 1e-8, 'es_CPInt (the PPL) vs statsmodels beta: %d intervals, worst |diff| %.1e' % (cnt, w))
    check(wm < 1e-8, 'es_CPInt mid-P (the PPL) vs brentq: worst |diff| %.1e' % wm)
    print('    BINOMIAL_CDF + BINOMIAL calls per interval: mean %.1f, max %d  [%.0f s]'
          % (np.mean(ncall), max(ncall), time.time() - t0))
    # conditional OR
    worst = 0; tabs = [(12, 5, 8, 30), (3, 1, 1, 3), (1, 9, 11, 3), (7, 15, 58, 472), (0, 5, 3, 10), (5, 0, 3, 10),
                       (700, 300, 280, 700), (999, 1, 1, 999), (1, 999, 999, 1), (2, 3, 0, 4)]
    rng = np.random.default_rng(3)
    tabs += [tuple(int(x) for x in rng.integers(1, 60, 4)) for _ in range(60)]
    states = set()
    t0 = time.time()
    for tb in tabs:
        r = h.call('es_CondOR', *tb)
        states.add(int(r[3]))
        if r[3] >= 3:
            continue
        res = odds_ratio(np.array([[tb[0], tb[1]], [tb[2], tb[3]]])); ci = res.confidence_interval()
        for g, w_ in ((r[0], res.statistic), (r[1], ci.low), (r[2], ci.high)):
            if w_ == 0 or math.isinf(w_):
                continue
            worst = max(worst, abs(g / w_ - 1))
    check(worst < 1e-6, 'es_CondOR (the PPL) vs SciPy: %d tables, worst relative difference %.1e  [%.0f s]'
          % (len(tabs), worst, time.time() - t0))
    check(h.call('es_CondOR', 0, 0, 5, 20)[3] == 3 and h.call('es_CondOR', 700, 300, 600, 500)[3] == 4
          and states >= {0, 1, 2}, 'es_CondOR states: 0 inside, 1 at the bottom, 2 at the top, 3 empty margin, 4 N > 2000')
    # BinCheck: right, and with the arguments read the other way round
    check(h.call('es_BinCheck') == 1, 'es_BinCheck passes with BINOMIAL_CDF(n, p, k)')
    h2 = Harness(PPL, strict=True, cas='giac')
    real = h2._table['BINOMIAL_CDF']
    h2._table['BINOMIAL_CDF'] = lambda a, site: stats.binom.cdf(a[1], a[0], a[2]) if 0 <= a[2] <= 1 else 0.5
    check(h2.call('es_BinCheck') == 0, 'es_BinCheck fails when BINOMIAL_CDF reads (n, k, p): exact CIs say "unavailable"')
    h2._table['BINOMIAL_CDF'] = real
    # the same routine text in CICatcher beta 2
    def body(path, names, tag):
        s = open(path, encoding='utf-8').read(); out = []
        for nm in names:
            m = re.search(r'^' + re.escape(nm) + r'\(.*?\)\nBEGIN\n.*?\nEND;\n', s, re.S | re.M)
            out.append(m.group(0).replace(tag, 'XX') if m else '')
        return out
    e = body(PPL, ['es_BinCheck', 'es_CPB', 'es_CPInt'], 'es_')
    q = body(CQ, ['cqBinCheck', 'cqCPB', 'cqCPInt'], 'cq')
    check(all(e) and e == q, 'es_BinCheck / es_CPB / es_CPInt are line for line the same as CICatcher beta 2a\'s cq* copies '
          '(%d lines)' % sum(x.count('\n') for x in e))


# ============================================================================ C
def giac_many(exprs):
    with tempfile.NamedTemporaryFile('w', suffix='.giac', delete=False) as f:
        for e in exprs:
            f.write(e + ';\n')
        name = f.name
    out = subprocess.run(['icas', name], capture_output=True, text=True, errors='replace', timeout=300).stdout
    os.unlink(name)
    lines = [ln.strip().rstrip(',') for ln in out.split('\n')
             if ln.strip() and not ln.strip().startswith('//') and 'synonyms' not in ln]
    return lines


def setterm(v, h):
    return '1/%d' % v if h == 0 else '2/%d' % (2 * v + 1)


def part_c():
    print('\n' + '=' * 78)
    print('C. Every CAS template, through desktop Giac (icas), against Python fractions')
    print('=' * 78)
    r = giac_many(['diff(ln(esq/(1-esq)),esq)', 'simplify(diff(ln(esq/(1-esq)),esq)-1/(esq*(1-esq)))'])
    print('    diff(ln(esq/(1-esq)),esq)                 ->', r[0])
    print('    simplify(that - 1/(esq*(1-esq)))          ->', r[1])
    import sympy
    q = sympy.Symbol('q')
    gd = sympy.sympify(r[0].replace('esq', 'q'))
    check(sympy.simplify(gd - 1 / (q * (1 - q))) == 0, 'the derivative Giac returns equals 1/(p(1-p)) (SymPy)')
    check(r[1] == '0', 'the check template returns "0" (the page then says "the CAS: the difference is 0")')
    tabs = [(12, 5, 8, 30), (40, 60, 20, 80), (0, 5, 3, 10), (5, 0, 3, 10), (1, 1, 1, 1), (700, 300, 280, 700),
            (1997, 1993, 1999, 1987), (0, 0, 5, 20), (999999, 3, 7, 999998)]
    ex = []
    for a, b, c, d in tabs:
        h = 1 if a * b * c * d == 0 else 0
        ex.append('+'.join(setterm(v, h) for v in (a, b, c, d)))
    r = giac_many(ex)
    for (a, b, c, d), e, g in zip(tabs, ex, r):
        h = 1 if a * b * c * d == 0 else 0
        want = sum(Fraction(1) / (Fraction(v) + Fraction(h, 2)) for v in (a, b, c, d))
        ok = Fraction(g) == want
        shown = len(g) <= 40
        print('    %-36s -> %-28s %s' % (e, g, 'fits' if shown else 'too long: the page says "an exact fraction with %d digits"' % (len(g) - 1)))
        check(ok, 'Help F fraction for %s equals Python Fraction %s' % ((a, b, c, d), want))
    # closed forms for k = 0 and k = n
    ns = list(range(1, 61)) + [100, 200, 500, 1000, 2000]
    ex = []
    for n in ns:
        ex += ['1-(1/40)^(1/%d)' % n, '(1/40)^(1/%d)' % n]
    r = giac_many(ex)
    ev = giac_many(['evalf(%s,20)' % x for x in r])
    bad = []; longest = 0
    for n, i in zip(ns, range(0, 2 * len(ns), 2)):
        for j, want in ((i, 1 - 0.025 ** (1 / n)), (i + 1, 0.025 ** (1 / n))):
            longest = max(longest, len(r[j]))
            if 'Root' in r[j] or 'rror' in r[j] or abs(float(ev[j]) - want) > 1e-12:
                bad.append((n, r[j], ev[j]))
    print('    1-(1/40)^(1/n) and (1/40)^(1/n), n = 1..60, 100..2000: e.g. n = 1 -> %s, n = 2 -> %s, n = 20 -> %s'
          % (r[0], r[2], r[38]))
    check(not bad, 'every closed form evaluates to 1 - 0.025^(1/n) / 0.025^(1/n) (%d templates; longest answer %d '
          'characters; page 6 shows up to 22)' % (2 * len(ns), longest))
    # 1.7a: the same answers as the calculator prints them (the root sign, CASProbe T14b)
    pr = [prime_print(x) for x in r]
    check(pr[2] == '1-\u221a(1/40)' and pr[3] == '\u221a(1/40)' and not any('sqrt' in x for x in pr)
          and max(len(x) for x in pr) <= longest,
          '1.7a: in the Prime\'s printing n = 2 reads %s and %s, no "sqrt" anywhere, none longer than desktop Giac\'s'
          % (pr[2], pr[3]))
    # the trap documented in CHANGES: simplify() on these roots
    r = giac_many(['simplify(1-(1/40)^(1/3))', 'simplify(1-(1/4)^(1/10))'])
    print('    (why simplify() is NOT used: simplify(1-(1/40)^(1/3)) -> %s; simplify(1-(1/4)^(1/10)) -> %s)'
          % (r[0][:40], r[1][:60]))


# ============================================================================ D
def new(cas='giac'):
    return Harness(PPL, strict=True, cas=cas)


def grid(h, cells):
    for i, v in enumerate(cells):
        h.tap(76 + 72 * (i % 2) + 36, 54 + 44 * (i // 2) + 22)
        h.answer([v])
    h.tap(300, 230)


def run(h, label, entry='EpiStats', args=()):
    try:
        r = h.call(entry, *args)
    except Exception as e:
        print('  ERROR in %s: %s %s %s' % (label, type(e).__name__, e, getattr(e, 'ppl_stack', '')))
        FAILS.append(label + ': ' + str(e))
        return None
    left = h.leftover()
    if any(left):
        FAILS.append(label + ': script left over %r' % (left,))
    return r


def pages(h, title):
    return [p for p in h.pages if p.lines() and p.lines()[0] == title]


def show(p, title):
    print('  [%s]' % title)
    for t in sorted(p.texts, key=lambda t: (t.y, t.x)):
        print('    y%3d x%3d f%s %s  %s' % (t.y, t.x, t.font, t.hex, t.text))


def layout(p, label):
    """font-1 lines: within the screen at 6.5 px a character, above the footer"""
    bad = []
    for t in p.texts:
        if t.y >= 218 and t.y < 224:
            bad.append('%s: y %d in the soft-key band' % (t.text, t.y))
        w = len(t.text) * {1: 6.5, 2: 8, 3: 9.5}.get(int(t.font or 1), 6.5)
        if t.x + w > 322 and not (t.width and t.x + t.width <= 320):
            bad.append('%s: %d px from x %d' % (t.text, w, t.x))
    return bad


def part_d():
    print('\n' + '=' * 78)
    print('D. End to end in the harness, cas = giac and cas = fail')
    print('=' * 78)
    a, b, c, d = 12, 5, 8, 30
    layout_bad = []
    for cas in ('giac', 'fail'):
        print('\n--- D1 module 1, 12 5 8 30, cas = %s ---' % cas)
        h = new(cas)
        h.choose(1); grid(h, [a, b, c, d])
        h.tap(160, 35)                         # Diagnostic tab
        h.press('Left')                        # page 1 -> page 7 (round)
        h.press('Esc'); h.choose(8)
        run(h, 'D1 ' + cas)
        rd = pages(h, 'THREE READINGS')
        co, dg = rd[0], rd[1]
        r, _, _ = cond_or(a, b, c, d)
        want = '  cond. MLE OR = %s  (%s-%s): page 7' % (sigtxt(r[0]), sigtxt(r[1]), sigtxt(r[2]))
        t = co.find('cond. MLE OR')
        check(t is not None and t.text == want and t.color == 0xFF4500,
              'cohort tab, under the OR: %r (orange)' % (t.text if t else None))
        check(co.find('Rows = exposure: risks real; worked: page 5.') is not None and len(co.texts) == len(rd[0].texts),
              'cohort tab: the two v1.6 notes share one line')
        ys = sorted(t.y for t in co.texts if t.x == 14)
        check(max(ys) <= 194, 'cohort tab: nine lines, the last at y %d (footer at 224)' % max(ys))
        sl, sh = proportion_confint(a, a + c, 0.05, 'beta'); pl, ph = proportion_confint(d, b + d, 0.05, 'beta')
        want = 'Exact: sens %s, spec %s' % (pct_ci(sl, sh), pct_ci(pl, ph))
        t = dg.find('Exact: sens')
        check(t is not None and t.text == want and t.color == 0xFF4500, 'Diagnostic tab: %r = statsmodels beta' % (t.text if t else None))
        check(dg.find('Sensitivity a/(a+c) = 60.0%  (38.7-78.1%)') is not None, 'Diagnostic tab keeps Wilson on the sensitivity line')
        p7 = pages(h, 'EXACT ODDS RATIO')
        check(len(p7) == 1 and p7[0].find('7/7') is not None, 'page 7/7 is reached (Left from page 1)')
        if p7:
            p = p7[0]
            if cas == 'giac':
                show(p, 'page 7, 12 5 8 30')
            check(p.find('Conditional MLE OR = %s  (%s-%s)' % (sigtxt(r[0]), sigtxt(r[1]), sigtxt(r[2]))) is not None,
                  'page 7: "Conditional MLE OR = 8.56  (2.09-41.3)"')
            check(p.find('Sample OR = ad/bc = 9.00, Woolf CI (2.45-33.11)') is not None, 'page 7: the sample OR beside it')
            bars = [s for s in p.shapes if s.cmd == 'RECT_P' and len(s.args) >= 6 and int(s.args[4]) == 0xFF4500]
            check(len(bars) >= 10, 'page 7: %d orange bars (P(a) at the MLE)' % len(bars))
            check(p.find('grey = P(a) if OR = 1 (page 4); its mean is 6.18') is not None,
                  'page 7: the null mean (a+b)(a+c)/N = 6.18')
            layout_bad += layout(p, 'page 7')
        check(abs(h.globals_['EP_OR_CMLE'] - r[0]) < 1e-9 and abs(h.globals_['EP_OR_CMLE_CI'][1] - r[2]) < 1e-7,
              'EP_OR_CMLE = %.6f, EP_OR_CMLE_CI = {%.6f, %.6f}' % (h.globals_['EP_OR_CMLE'], *h.globals_['EP_OR_CMLE_CI']))
        check(len(h.cas_calls) == 0, 'module 1 needs no CAS at all: %d calls' % len(h.cas_calls))
        layout_bad += layout(co, 'cohort') + layout(dg, 'diagnostic')

    print('\n--- D2 EpiStats2x2: every state of the conditional OR ---')
    for tb, st, txt in (((0, 5, 3, 10), 1, 'MLE 0: your a is the smallest it can be'),
                        ((5, 0, 3, 10), 2, 'MLE infinite: your a is the largest it can be'),
                        ((0, 0, 5, 20), 3, 'A row or column total is 0: with every table'),
                        ((700, 300, 600, 500), 4, 'N > 2000: not computed here, the same cap'),
                        ((700, 300, 280, 700), 0, 'orange = P(a) at the MLE: its mean is your a')):
        h = new()
        h.press('Left', 'Esc')
        r = run(h, 'D2 %s' % (tb,), 'EpiStats2x2', tb)
        p = pages(h, 'EXACT ODDS RATIO')
        ok = bool(p) and p[0].find(txt) is not None
        st_ppl = None
        if p:
            line = p[0].find('Conditional MLE OR = ')
            st_ppl = line.text if line else None
        check(ok, 'EpiStats2x2%s -> page 7: %r; %r' % (tb, txt, st_ppl))
        if p:
            layout_bad += layout(p[0], 'page 7 %s' % (tb,))
    print('\n--- D3 module 2, 40 60 20 80: the risk bars ---')
    h = new()
    h.choose(2); grid(h, [40, 60, 20, 80])
    h.press('Left', 'Left', 'Esc'); h.choose(8)      # 1 -> 5 -> 4
    run(h, 'D3')
    rb = pages(h, 'RISK BARS')
    check(bool(rb), 'module 2 page 4 shown')
    if rb:
        p = rb[0]
        check(p.find('95% CIs: black = Wilson, orange = exact (C-P)') is not None, 'legend names both whiskers')
        org = [s for s in p.shapes if s.cmd == 'LINE_P' and int(s.args[-1]) == 0xFF4500]
        check(len(org) == 8, '%d orange whisker lines (2 bars x 4)' % len(org))
        e1 = proportion_confint(40, 100, 0.05, 'beta'); e2 = proportion_confint(20, 100, 0.05, 'beta')
        g = h.globals_
        check(max(abs(g['EP_risk_exp_CP'][0] - e1[0]), abs(g['EP_risk_exp_CP'][1] - e1[1]),
                  abs(g['EP_risk_unexp_CP'][0] - e2[0]), abs(g['EP_risk_unexp_CP'][1] - e2[1])) < 1e-9,
              'EP_risk_exp_CP {%.4f, %.4f}, EP_risk_unexp_CP {%.4f, %.4f} = statsmodels beta' % (*g['EP_risk_exp_CP'], *g['EP_risk_unexp_CP']))
        # the exact whisker's top at the pixel the scale gives
        top = max(e1[1], e2[1], 0.05)
        layout_bad += layout(p, 'risk bars')

    for cas in ('giac', 'fail'):
        print('\n--- D4 module 3, 12 0 8 30 (spec 30/30, PPV 12/12): page 6, cas = %s ---' % cas)
        h = new(cas)
        h.choose(3); grid(h, [12, 0, 8, 30])
        h.press('Left')                          # 1 -> 6
        h.tap(200, 70)                           # row 2: Specificity 30/30
        h.press('Down')                          # row 3: PPV 12/12
        h.press('Up')                            # row 2 again (cached)
        h.tap(200, 40)                           # row 1
        h.press('Esc'); h.choose(8)
        run(h, 'D4 ' + cas)
        p6 = pages(h, 'EXACT vs WILSON')
        check(len(p6) == 5, 'page 6 drawn 5 times (open, tap, Down, Up, tap): %d' % len(p6))
        if len(p6) < 5:
            continue
        if cas == 'giac':
            show(p6[1], 'page 6, row 2 picked (cas = giac)')
        else:
            show(p6[1], 'page 6, row 2 picked (cas = fail)')
        g = h.globals_
        for nm, k, n, key in (('sens', 12, 20, 'EP_sens_CP'), ('spec', 30, 30, 'EP_spec_CP'),
                              ('ppv', 12, 12, 'EP_ppv_CP'), ('npv', 30, 38, 'EP_npv_CP')):
            rl, rh = proportion_confint(k, n, 0.05, 'beta'); rl = 0 if np.isnan(rl) else rl; rh = 1 if np.isnan(rh) else rh
            if max(abs(g[key][0] - rl), abs(g[key][1] - rh)) > 1e-9:
                FAILS.append('%s %s' % (key, g[key]))
        check(True, 'EP_sens_CP, EP_spec_CP, EP_ppv_CP, EP_npv_CP = statsmodels beta')
        p = p6[1]
        sl, sh = proportion_confint(30, 30, 0.05, 'beta'); sh = 1.0
        ml, mh = midp_ref(30, 30, 0.025)
        wl, wh = proportion_confint(30, 30, 0.05, 'wilson')
        check(p.find('exact %s' % pct_ci(sl, sh)) is not None and p.find('mid-P %s' % pct_ci(ml, mh)) is not None
              and p.find('Wilson %s' % pct_ci(wl, wh)) is not None,
              'panel for Specificity 30/30: Wilson %s, exact %s, mid-P %s' % (pct_ci(wl, wh), pct_ci(sl, sh), pct_ci(ml, mh)))
        if cas == 'giac':
            check(p.find('exact lower = (1/40)^(1/30)') is not None and p.find('exact (CAS)') is not None,
                  'CAS line: "exact lower = (1/40)^(1/30)" with the badge "exact (CAS)"')
            calls = [x[0] for x in h.cas_calls]
            check(calls == ['string((1/40)^(1/30))', 'string((1/40)^(1/12))'],
                  'the CAS is asked once per row with 0 or n, on the tap (1.7a: as string(...)): %r' % calls)
            check(not h.cas_vars and not any('non-literal' in w for w in h.warnings),
                  '1.7a: no CAS variable assigned, no CAS call of a variable')
        else:
            check(p.find('exact lower = (%s/2)^(1/n) = %.4f' % (chr(945), sl)) is not None and p.find('decimal') is not None,
                  'fallback: "exact lower = (alpha/2)^(1/n) = %.4f" with the badge "decimal", no error' % sl)
        sel = [q.find(' = 12/20 = 60.0%') for q in p6]
        check(p6[0].find('Sensitivity a/(a+c) = 12/20 = 60.0%') is not None and p6[4].find('Sensitivity') is not None,
              'the panel follows the picked row (row 1 at open and after the last tap)')
        bars = [s for s in p6[0].shapes if s.cmd == 'LINE_P' and int(s.args[-1]) == 0xFF4500]
        check(len(bars) == 16, '%d orange (exact) bar lines: 4 rows x 4' % len(bars))
        for q in p6[:2]:
            layout_bad += layout(q, 'page 6')
        m3 = pages(h, 'DIAGNOSTIC ACCURACY')
        check(bool(m3) and m3[0].find('CIs above: Wilson.  Exact and mid-P: page 6.') is not None and m3[0].find('1/6'),
              'module 3 page 1 points to page 6 and reads 1/6')

    print('\n--- D5 Help E and F ---')
    for cas in ('giac', 'fail'):
        h = new(cas)
        h.choose(7); h.choose(15); h.press('Enter')        # F with the example table
        h.choose(14); h.press('Enter')                      # E
        h.choose(15); h.press('Enter')                      # F again: nothing new asked
        h.choose(16); h.choose(1); grid(h, [0, 5, 3, 10]); h.press('Esc')   # a table with a zero cell
        h.choose(7); h.choose(15); h.press('Enter'); h.choose(16); h.choose(8)
        run(h, 'D5 ' + cas)
        se = pages(h, 'WHERE THE SE COMES FROM')
        check(len(se) == 3, 'Help F opened three times (%d)' % len(se))
        if len(se) < 3:
            continue
        show(se[0], 'Help F, example table, cas = %s' % cas)
        if cas == 'giac':
            check(se[0].find("CAS: g'(p) = 1/p+1/(1-p)") is not None and se[0].find('(CAS: the difference is 0)') is not None,
                  'Help F: the CAS derivative "1/p+1/(1-p)" and its check')
            check(se[0].find('  = 53/120') is not None and se[0].find('SE = sqrt(53/120) = 0.6646') is not None
                  and se[0].find('exact (CAS)') is not None,
                  'Help F, 12 5 8 30: "= 53/120", "SE = sqrt(53/120) = 0.6646", badge "exact (CAS)"')
            want = sum(Fraction(2, 2 * v + 1) for v in (0, 5, 3, 10))
            check(se[2].find('  = %s' % want) is not None and se[2].find('(+0.5)') is not None,
                  'Help F, 0 5 3 10: 0.5 added, "= %s"' % want)
            calls = [x[0] for x in h.cas_calls]
            check(len(calls) == 4, 'CAS calls: derivative, check, two fractions -- the second open asked nothing (%r)' % calls)
            check(all(c[0].startswith('string(') and c[1].startswith('"') for c in h.cas_calls)
                  and not h.cas_vars and not any('non-literal' in w for w in h.warnings),
                  '1.7a: every CAS text asks for string(...), every answer arrives quoted, no CAS variable assigned')
        else:
            check(se[0].find("g'(p) = 1/p + 1/(1-p)  (textbook form)") is not None and se[0].find('  = 0.441667') is not None
                  and se[0].find('decimal') is not None,
                  'fallback: the textbook form, "= 0.441667", the badge "decimal"')
            check(len(h.cas_calls) == 3, 'with the CAS failing it is asked 3 times in the run, not on every open (%d)'
                  % len(h.cas_calls))
        for q in se:
            layout_bad += layout(q, 'help F')
        he = pages(h, 'EXACT CIs, EXACT OR')
        check(bool(he) and len(he[0].texts) == 14, 'Help E: 12 lines')
        if he:
            layout_bad += layout(he[0], 'help E')
        ch = [c for c in h.chooses if c.title == 'Help & Information']
        check(bool(ch) and len(ch[0].items) == 16 and ch[0].items[13] == 'Exact CIs, Exact OR',
              'the Help menu: list form, 16 items, E = "Exact CIs, Exact OR", F = "Where the SE Comes From"')
    # static checks
    src = open(PPL, encoding='utf-8').read()
    code = '\n'.join(ln.split('//')[0] for ln in src.split('\n'))
    g0 = [ln for ln in code.split('\n') if re.search(r'\bG0\b', ln) and 'BLIT_P(G0' not in ln]
    check(not g0, 'nothing draws on G0 except BLIT_P(G0, ...)')
    casu = [i + 1 for i, ln in enumerate(code.split('\n')) if re.search(r'\bCAS\s*\(', ln)]
    check(len(casu) == 1 and 'cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + esS + ")" + CHAR(34) + ")"));' in code.split('\n')[casu[0] - 1],
          '1.7a: CAS( appears on one code line only, inside es_Cas, in the EXPR form (line %s)' % casu)
    lines = src.split('\n'); callers = set()
    for i, ln in enumerate(lines):
        if 'es_Cas(' in ln.split('//')[0] and not ln.startswith('es_Cas('):
            j = i
            while j > 0 and not (re.match(r'^es_\w+\(.*\)\s*$', lines[j]) and lines[j + 1].strip() == 'BEGIN'):
                j -= 1
            callers.add(lines[j].split('(')[0])
    callers = sorted(callers)
    check(set(callers) <= {'es_Help_SE', 'es_XCas'}, 'es_Cas is called only from es_Help_SE and es_XCas (events): %s' % callers)
    check(not layout_bad, 'layout on the new and changed pages (6.5/8/9.5 px a character): %s' % (layout_bad[:5] or 'no problems'))


# ============================================================================ E
E_SHIM = '''
import sys, runpy, os
sys.path.insert(0, %r)
import ppl_run_v3d
for _n in ('ppl_run_v1', 'ppl_run_v2', 'ppl_run_v3', 'ppl_run_v3a', 'ppl_run_v3b', 'ppl_run_v3c'):
    sys.modules[_n] = ppl_run_v3d
_ALL = []
_i0 = ppl_run_v3d.Harness.__init__
def _i(self, *a, **k):
    _i0(self, *a, **k); _ALL.append(self)
ppl_run_v3d.Harness.__init__ = _i
_s = sys.argv[1]; sys.argv = [_s] + sys.argv[2:]
_rc = 0
try:
    runpy.run_path(_s, run_name='__main__')
except SystemExit as e:
    _rc = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
finally:
    _sci = sorted(set(t for h in _ALL for (_v, _d, t) in h.sci_strings))
    print('V3D-SHIM: %%d harness runs, %%d scientific STRING results %%s' %% (len(_ALL), len(_sci), _sci[:10]))
sys.exit(_rc)
'''


def part_e():
    print('\n' + '=' * 78)
    print('E. The v1.6 verification suite (verify_EpiStats.py) against v1.7b, on harness v3d')
    print('=' * 78)
    t0 = time.time()
    # 1.7b: the v1.6 suite imports ppl_run_v1; a shim answers that import with ppl_run_v3d
    # (INSTRING("") raises, small fixed decimals print scientific) and counts h.sci_strings
    with tempfile.NamedTemporaryFile('w', suffix='_v3d_shim.py', delete=False) as f:
        f.write(E_SHIM % HERE)
        shim = f.name
    try:
        r = subprocess.run([sys.executable, shim, os.path.join(HERE, 'verify_EpiStats.py'), PPL],
                           capture_output=True, text=True)
    finally:
        os.unlink(shim)
    tail = [ln for ln in r.stdout.split('\n') if 'RESULT' in ln or 'layout audit' in ln or 'warnings (' in ln]
    print('  ' + '\n  '.join(tail))
    check(r.returncode == 0 and any('ALL CHECKS PASSED' in ln for ln in tail),
          'verify_EpiStats.py (v1.6: 120 formula checks, 83 harness checks, 28 scripted runs) passes on v1.7b, '
          'harness v3d  [%.0f s]' % (time.time() - t0))
    sh = [ln for ln in r.stdout.split('\n') if ln.startswith('V3D-SHIM')]
    print('  ' + (sh[0] if sh else 'V3D-SHIM line missing'))
    m = re.match(r'V3D-SHIM: (\d+) harness runs, (\d+) scientific', sh[0]) if sh else None
    E_SCI[:] = [int(m.group(1)), int(m.group(2))] if m else [0, -1]
    check(bool(m) and int(m.group(1)) >= 20 and int(m.group(2)) == 0,
          '1.7b: the v1.6 suite\'s %s harness runs on v1.7b print no scientific STRING (v1.7a: 7, in es_FmtCI, '
          'es_ForestDraw and es_RuleTxt)' % (m.group(1) if m else '?'))


E_SCI = [0, -1]


# ============================================================================ G (1.7a)
def part_g():
    print('\n' + '=' * 78)
    print('G. 1.7a: v1.7 in harness v3d, and v1.7a against v1.7 (kept from verify_EpiStats_v1.7a.py)')
    print('=' * 78)
    # v1.7's es_Cas hands back its own text: page 6 would show the input "(1/40)^(1/30)" (right by
    # luck: the input IS the closed form), and Help F the unevaluated derivative and the unadded sum
    h = Harness(V17, strict=True, cas='giac')
    h.choose(7); h.choose(15); h.press('Enter'); h.choose(16); h.choose(8)
    run(h, 'G v1.7 Help F')
    se = pages(h, 'WHERE THE SE COMES FROM')
    ok = bool(se) and se[0].find("CAS: g'(p) = diff(ln(p/(1-p)),p)") is not None \
        and se[0].find('  = 1/12+1/5+1/8+1/30') is not None and se[0].find('(CAS: the difference is 0)') is None \
        and any('non-literal' in w for w in h.warnings)
    check(ok, '1.7a: v1.7 in v3d shows its own CAS text on Help F as if it were the answer '
              '("g\'(p) = diff(ln(p/(1-p)),p)", "= 1/12+1/5+1/8+1/30") -- the emulator\'s finding')
    exec(G_CODE, globals())


G_CODE = "\n# ================================================================ G (round 2a)\nsay('\\nG. v1.7a: v1.7 in harness v3b, and v1.7a against v1.7')\nimport re as _re\n_b_old = open(V17, encoding='utf-8').read()\n_b_new = open(V17A, encoding='utf-8').read()\n\n\ndef _bodies(txt):\n    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)\n    c = _re.sub(r'//[^\\n]*', '', c)\n    out = {}\n    for m in _re.finditer(r'(?m)^(?:EXPORT\\s+|LOCAL\\s+)?([A-Za-z]\\w*)\\(([^()\\n]*)\\)\\s*\\nBEGIN\\n.*?^END;', c, _re.S):\n        out[m.group(1)] = _re.sub(r'[ \\t]+\\n', '\\n', m.group(0))\n    return out\n\n\n_B0, _B1 = _bodies(_b_old), _bodies(_b_new)\n_diff = sorted(n for n in set(_B0) | set(_B1) if _B0.get(n) != _B1.get(n))\ncheck(_diff == ['EpiStats', 'es_Cas', 'es_Help_About'], 'v1.7a: routines that differ from v1.7: %s (want EpiStats, es_Cas, es_Help_About)' % _diff)\n\n\ndef _outside(t, names):\n    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\\n]*', '', t))\n    if names:\n        c = _re.sub(r'(?ms)^(?:EXPORT\\s+|LOCAL\\s+)?(?:%s)\\([^\\n]*\\)\\s*\\nBEGIN\\n.*?^END;' % '|'.join(names), '', c)\n    return _re.sub(r'\\s+', ' ', c)\n\n\ncheck(_outside(_b_old, _diff) == _outside(_b_new, _diff), 'v1.7a: outside those routines only comments differ')\n_py0 = _re.findall(r'(?s)#PYTHON.*?#END', _b_old)\n_py1 = _re.findall(r'(?s)#PYTHON.*?#END', _b_new)\ncheck(_py0 == _py1, 'v1.7a: the #PYTHON blocks are unchanged')\nsay('  routines that differ from v1.7: %s; everything else differs only in comments' % ', '.join(_diff))\n"


# ============================================================================ F (1.7b)
SCI_E = 'ᴇ'          # the small capital E the Prime prints in scientific form


def _run_quiet(path, script, cas='giac', pre=None):
    """One scripted session; returns (harness, error text or None)."""
    h = Harness(path, strict=True, cas=cas)
    if pre:
        pre(h)
    script(h)
    err = None
    try:
        h.call('EpiStats')
    except Exception as e:
        err = '%s: %s [%s]' % (type(e).__name__, e, ' > '.join(getattr(e, 'ppl_stack', []) or []))
    return h, err


def _texts(h):
    return [[t.text for t in sorted(p.texts, key=lambda t: (t.y, t.x))] for p in h.pages]


def _changed(ho, hn):
    """Per page, the texts that are in one version and not the other (a line that only moved, or
    that es_Line2 now fits on one line, is the same text), as words, matched word for word as a
    multiset: every old word left over must be a number printed in scientific form (or one of the
    two reworded phrases, "1/|RD| =" on the NNT page and "=" before the Breslow-Day p), and every
    new word left over a number.  The pages must be the same in number."""
    import collections
    to, tn = _texts(ho), _texts(hn)
    if len(to) != len(tn):
        return ['%d pages against %d' % (len(to), len(tn))]
    odd = []
    for a, b in zip(to, tn):
        ca, cb = collections.Counter(a), collections.Counter(b)
        oa = collections.Counter(' '.join(x for x in a if ca[x] > cb.get(x, 0)).split())
        ob = collections.Counter(' '.join(x for x in b if cb[x] > ca.get(x, 0)).split())
        ra, rb = oa - ob, ob - oa
        bad_old = [w for w in ra.elements() if SCI_E not in w and w not in ('1/|RD|', '=')]
        bad_new = [w for w in rb.elements() if SCI_E in w or not (re.search(r'\d', w) or w == '<')]
        if bad_old or bad_new:
            odd.append((bad_old, bad_new))
    return odd


def _has(h, sub):
    return any(sub in t.text for p in h.pages for t in p.texts)


def _has_re(h, rx):
    return any(re.search(rx, t.text) for p in h.pages for t in p.texts)


def _s_m1(t):
    def f(h):
        h.choose(1); grid(h, t)
        h.press('Down', 'Down')                              # page 1: Diagnostic, Paired tabs
        h.press('Right', 'Right', 'Right', 'Right')          # pages 2 .. 5
        h.press('Down', 'Down', 'Down', 'Down', 'Down', 'Down')   # the OR, RR and RD boxes
        h.press('Right')                                     # 6, the mosaic
        h.press('Down', 'Down', 'Down', 'Down')              # tiles a .. d
        h.press('Right')                                     # 7, the exact OR
        h.press('Esc'); h.choose(8)
    return f


def _s_tile(t):
    def f(h):
        h.choose(1); grid(h, t)
        h.press('Left', 'Left', 'Down', 'Esc'); h.choose(8)  # page 7, 6, tile a
    return f


def _s_cnt(t):
    def f(h):
        h.choose(1); grid(h, t); h.press('Esc'); h.choose(8)
    return f


def _s_m2(t):
    def f(h):
        h.choose(2); grid(h, t)
        h.press('Right', 'Right', 'Right', 'Right')          # pages 2 .. 5 (risk bars, NNT)
        h.press('Esc'); h.choose(8)
    return f


def _s_m3(t):
    def f(h):
        h.choose(3); grid(h, t)
        h.press('Right', 'Right', 'Right')                   # 2, 3, 4 (PPV vs prevalence)
        h.press('Enter')                                     # 4 -> 5, the ROC square
        h.press('Right')                                     # 6, exact vs Wilson
        h.press('Down', 'Down', 'Down')
        h.press('Esc'); h.choose(8)
    return f


def _s_m5(kind, s1, s2):
    def f(h):
        h.choose(5); h.choose(kind); grid(h, s1); grid(h, s2)
        h.press('Right', 'Right')                            # summary, forest plot
        h.press('Esc'); h.choose(8)
    return f


def _s_helpf(h):
    h.choose(7); h.choose(15); h.press('Enter'); h.choose(16); h.choose(8)


def _big_table(h):
    h.globals_['EP_table'] = [1e9, 1e9, 1e9, 1e9]


def part_f():
    print('\n' + '=' * 78)
    print('F. 1.7b: the round-2 string rules, v1.7b against v1.7a, both in harness v3d')
    print('=' * 78)

    # ---- F1 es_Cas itself
    print('\nF1. es_Cas, called directly')
    h = Harness(PPL, strict=True, cas='giac')
    r1 = h.call('es_Cas', '1/2+1/3'); ok1 = h.globals_['esCasOK']
    r2 = h.call('es_Cas', '1/0'); r3 = h.call('es_Cas', '0/0'); r4 = h.call('es_Cas', '1/(')
    ok4 = h.globals_['esCasOK']
    print('    1/2+1/3 -> %r; 1/0 -> %r (the CAS said %s); 0/0 -> %r; a syntax error -> %r'
          % (r1, r2, h.cas_calls[1][1], r3, r4))
    check(r1 == '5/6' and ok1 == 1 and r2 == '' and r3 == '' and r4 == '' and ok4 == 0,
          '1.7b: es_Cas (cas=giac): 5/6 with esCasOK 1; the infinity, undef and a syntax error give "" with esCasOK 0')
    h = Harness(PPL, strict=True, cas='fail')
    try:
        r = h.call('es_Cas', '1/2+1/3'); e = None
    except Exception as x:
        r, e = None, x
    check(e is None and r == '' and h.globals_['esCasOK'] == 0,
          '1.7b: es_Cas with the CAS failing returns "" with esCasOK 0 and no error (%r, %s)' % (r, e))
    h = Harness(V17A, strict=True, cas='fail')
    try:
        h.call('es_Cas', '1/2+1/3'); e = None
    except Exception as x:
        e = x
    check(e is not None and 'INSTRING: Invalid input' in str(e),
          '1.7b: v1.7a\'s es_Cas with the CAS failing stops: %s' % (str(e)[:70] if e else 'no error'))

    # ---- F2 every CAS page end to end with the CAS failing: v1.7b completes, v1.7a stops
    print('\nF2. every CAS page with cas = fail: v1.7b against v1.7a')

    def p6(h):
        h.choose(3); grid(h, [12, 0, 8, 30])
        h.press('Left'); h.tap(200, 70)                     # page 6, the Spec row (30/30)
        h.press('Esc'); h.choose(8)
    sl = proportion_confint(30, 30, 0.05, 'beta')[0]
    for path, tag in ((PPL, 'v1.7b'), (V17A, 'v1.7a')):
        h, err = _run_quiet(path, p6, cas='fail')
        pg = pages(h, 'EXACT vs WILSON')
        line = pg[-1].find('exact lower = ') if pg else None
        print('    %s module 3 page 6: %s' % (tag, err or (line.text if line else '?')))
        if path == PPL:
            check(err is None and line is not None and line.text == 'exact lower = (%s/2)^(1/n) = %.4f' % (chr(945), sl)
                  and pg[-1].find('decimal') is not None and not h.cas_calls[0][1].startswith('"'),
                  '1.7b: module 3 page 6, Spec 30/30, CAS failing: "exact lower = (alpha/2)^(1/n) = %.4f", '
                  '"decimal", no error' % sl)
        else:
            check(err is not None and 'INSTRING: Invalid input' in err and 'es_XCas > es_Cas' in err,
                  '1.7b: v1.7a on the same run stops: %s' % (err or 'no error')[:110])
    for path, tag in ((PPL, 'v1.7b'), (V17A, 'v1.7a')):
        h, err = _run_quiet(path, _s_helpf, cas='fail')
        se = pages(h, 'WHERE THE SE COMES FROM')
        print('    %s Help F: %s' % (tag, err or ' | '.join(se[0].lines()[11:15]) if se else err))
        if path == PPL:
            check(err is None and bool(se) and se[0].find("g'(p) = 1/p + 1/(1-p)  (textbook form)") is not None
                  and se[0].find('  = 0.441667') is not None and se[0].find('SE = sqrt(0.441667) = 0.6646') is not None
                  and se[0].find('decimal') is not None,
                  '1.7b: Help F, CAS failing: the textbook form, "= 0.441667", "SE = sqrt(0.441667) = 0.6646", '
                  '"decimal", no error')
        else:
            check(err is not None and 'INSTRING: Invalid input' in err and 'es_Help_SE > es_Cas' in err,
                  '1.7b: v1.7a on the same run stops: %s' % (err or 'no error')[:110])

    # ---- F3 tables that push a fixed-decimal display below 10^-d
    print('\nF3. tables that push a fixed-decimal display below 10^-d (cas = giac unless said)')
    runs = [
        ('module 1, 1 2999 50 50 (pages 1-7, the three boxes, four tiles)', _s_m1([1, 2999, 50, 50]), 'giac', None,
         {'es_Arith', 'es_FmtCI', 'es_FmtPct', 'es_Mosaic'},
         [('OR = ad/bc = < 0.001   (0.00-0.00)', None), ('Risk if exposed, a/(a+b) = 0.0%', None),
          ('OR = (a×d)/(b×c) = (1×50)/(2999×50) = 0.00', None), ('   = 0.00 to 0.00', None),
          ('   = 0.000 / 0.500 = 0.001', None), ('row % = 0.0 %   (all rows: 1.6 %)', None),
          ('Sample OR = ad/bc = 0.000333, Woolf CI (0.00-0.00)', None)]),
        ('module 1, 500 500 502 501 (the paired reading)', _s_m1([500, 500, 502, 501]), 'giac', None,
         {'es_ReadPage', 'es_Arith', 'es_FmtPct'},
         [('McNemar χ² (cont. corr.) = 0.001, p = 0.9748', None),
          (None, r'^Youden J = sens \+ spec - 1 = -?0\.000$'), (None, r'^Kappa = \(po-pe\)/\(1-pe\) = -?0\.000 \(Poor\)$'),
          ("Yule's Q = (ad-bc)/(ad+bc) = -0.001", None)]),
        ('module 1, 1 1 1 997 (page 7, the mosaic)', _s_m1([1, 1, 1, 997]), 'giac', None,
         {'es_CORPage', 'es_Mosaic'},
         [('grey = P(a) if OR = 1 (page 4); its mean is 0.00', None), ('a: Exposed+, Outcome+: O = 1, E = 0.00', None)]),
        ('module 1, 20000 20000 20000 20001 (a mosaic tile)', _s_tile([20000, 20000, 20000, 20001]), 'giac', None,
         {'es_Sgn', 'es_FmtPct'},
         [('adj. residual = +0.00: about as expected', None)]),
        ('module 1, a count typed as 0.004', _s_cnt([0.004, 5, 8, 30]), 'giac', None,
         {'es_Grid'}, [('MSGBOX', 'Counts are whole numbers: 0.00 was rounded to the nearest one.')]),
        ('module 2, 1 2999 1 999 (risk bars, NNT)', _s_m2([1, 2999, 1, 999]), 'giac', None,
         {'es_NNTIcons', 'es_RiskBars', 'es_FmtPct'},
         [('NNT = 1/0.000667 = 1500.00, round up: 1500', None), ('the outcome is rare here (Ru = 0.1 %).', None)]),
        ('module 2, 3 2997 1 2999 (OR vs RR, rare)', _s_m2([3, 2997, 1, 2999]), 'giac', None,
         {'es_RiskBars'},
         [('OR = 3.00 overstates RR = 3.00 by only 0 %:', None), ('the outcome is rare here (Ru = 0.0 %).', None)]),
        ('module 2, 1 999 600 401 (OR, RR below 0.005)', _s_m2([1, 999, 600, 401]), 'giac', None,
         {'es_RiskBars', 'es_FmtCI'},
         [('OR = 0.00 exaggerates RR = 0.00 by 60 % here', None), ('95% CI: (0.00-0.00)', None),
          ('95% CI: (0.00-0.01)', None)]),
        ('module 3, 1 2999 2 999 (prevalence page)', _s_m3([1, 2999, 2, 999]), 'giac', None,
         {'es_PctTxt', 'es_PrevDraw', 'es_FmtCI', 'es_FmtPct'},
         [('PPV = 0.0 %', None), ('sample: 0.1 %', None), ('p = 0.1 %', None)]),
        ('module 3, 1 1 2999 2999 (the ROC square)', _s_m3([1, 1, 2999, 2999]), 'giac', None,
         {'es_ROCPage', 'es_PrevDraw', 'es_FmtCI'},
         [('TPR = sens = 0.0 %', None), ('FPR = 1-spec = 0.0 %', None), (' = 0.000/0.000 = 1.00', None),
          ('Youden J = sens + spec - 1 = 0.000:', None)]),
        ('module 3, 0 1 60000 1, CAS failing (page 6 decimal)', _s_m3([0, 1, 60000, 1]), 'fail', None,
         None, [('exact upper = 1 - (%s/2)^(1/n) = 0.0001' % chr(945), None)]),
        ('module 5 OR, opposite strata (forest: Breslow-Day p)', _s_m5(1, [10, 2, 2, 10], [2, 10, 10, 2]), 'giac', None,
         {'es_ForestDraw', 'es_FmtCI'},
         [("Breslow-Day p < 0.01: are the strata's ORs alike?", None)]),
        ('module 5 OR, 1 1 1 1 and 500 500 500 500 (forest weights)', _s_m5(1, [1, 1, 1, 1], [500, 500, 500, 500]),
         'giac', None, {'es_ForestDraw'}, [('w = 0 %', None), ('w = 100 %', None)]),
        ('module 5 OR, crude and M-H 0.02 % apart', _s_m5(1, [10, 20, 30, 40], [11, 20, 30, 40]), 'giac', None,
         {'es_RuleTxt'}, [('Crude and M-H differ by 0 % (of the M-H).', None)]),
        ('module 5 RR, M-H chi-square 0.0006', _s_m5(2, [200, 200, 200, 200], [200, 200, 200, 201]), 'giac', None,
         {'es_MHSummary', 'es_RuleTxt'}, [('M-H χ² (1 df) = 0.001, p = 0.9801', None)]),
        ('Help F with EP_table = 1E9 each', _s_helpf, 'giac', _big_table,
         {'es_Help_SE'}, [('SE = sqrt(1/250000000) = 0.0001', None)]),
    ]
    for label, script, cas, pre, want_old, want_new in runs:
        hn, en = _run_quiet(PPL, script, cas, pre)
        ho, eo = _run_quiet(V17A, script, cas, pre)
        old_where = sorted(set(r for r, _ in ho.sci_where))
        print('    %s\n      v1.7a: %s; scientific in %s, e.g. %s\n      v1.7b: %s; scientific: %d'
              % (label, eo or 'ran', old_where or '-', sorted(set(t for _, t in ho.sci_where))[:4],
                 en or 'ran', len(hn.sci_strings)))
        if want_old is not None:
            check(eo is None and want_old <= set(old_where),
                  '1.7b: %s -- v1.7a prints scientific in %s' % (label, ', '.join(sorted(want_old))))
        else:
            check(eo is not None and 'INSTRING' in eo, '1.7b: %s -- v1.7a stops (INSTRING)' % label)
        okn = en is None and not hn.sci_strings
        for sub, rx in want_new:
            if sub == 'MSGBOX':
                okn = okn and any(rx in ' '.join(m.lines) for m in hn.msgboxes)
            elif sub is not None:
                okn = okn and _has(hn, sub)
            else:
                okn = okn and _has_re(hn, rx)
        check(okn, '1.7b: %s -- v1.7b: no scientific STRING, and %s'
              % (label, '; '.join(repr(s if s and s != 'MSGBOX' else r) for s, r in want_new)))
        # nothing else on the screen changed: every text that differs was scientific in
        # v1.7a, or is one of the two reworded lines
        if eo is None:
            odd = _changed(ho, hn)
            check(not odd, '1.7b: %s -- the same pages as v1.7a; every word that changed was a scientific number%s'
                  % (label, (': %r' % odd[:2]) if odd else ''))

    # ---- F4 the static sweep of STRING(x, 2, d)
    print('\nF4. every STRING(x, 2, d) in v1.7b: rounded first, or unable to reach 0 < |x| < 10^-d')
    calls = string_calls(PPL)
    wrapped = [c for c in calls if re.match(r'^ROUND\((.*), ?(\w+)\)$', c[2]) and
               re.match(r'^ROUND\((.*), ?(\w+)\)$', c[2]).group(2) == c[3]]
    bare = [c for c in calls if c not in wrapped]
    got = {}
    for rt, ln, a0, d in bare:
        got.setdefault((rt, a0, d), 0)
        got[(rt, a0, d)] += 1
    reasons = {}
    for key, why in SAFE.items():
        reasons.setdefault(why, []).append(key)
    unknown = sorted(k for k in got if k not in SAFE)
    stale = sorted(k for k in SAFE if k not in got)
    print('    %d calls: %d rounded first (STRING(ROUND(x, d), 2, d)), %d left as they were:' % (len(calls), len(wrapped), len(bare)))
    for why, keys in sorted(reasons.items()):
        n = sum(got.get(k, 0) for k in keys)
        print('      %3d  %s' % (n, why))
    old_calls = string_calls(V17A)
    check(not unknown and not stale,
          '1.7b: every bare STRING(x, 2, d) has a reason it cannot print scientific (unlisted: %s; listed but gone: %s)'
          % (unknown[:3] or 'none', stale[:3] or 'none'))
    check(len(old_calls) == 155 and len(calls) == 154 and len(wrapped) == 86,
          '1.7b: v1.7a has %d such calls; v1.7b %d (the forest plot\'s Breslow-Day p now goes through es_PTxt), '
          '%d of them rounded first' % (len(old_calls), len(calls), len(wrapped)))
    # ---- F5 INSTRING, LEFT, MID, RIGHT
    print('\nF5. INSTRING, LEFT, MID and RIGHT in v1.7b (code only)')
    code = [_strip_comment(ln) for ln in open(PPL, encoding='utf-8').read().split('\n')]
    hits = [(i + 1, ln.strip()) for i, ln in enumerate(code) if re.search(r'\b(INSTRING|LEFT|MID|RIGHT)\(', ln)]
    for i, ln in hits:
        print('    %5d  %s' % (i, ln[:110]))
    ins = [i for i, ln in hits if 'INSTRING(' in ln]
    check(len(ins) == 1 and code[ins[0] - 2].strip() == 'IF DIM(cR) > 0 THEN',
          '1.7b: the one INSTRING line (%s) runs only inside IF DIM(cR) > 0' % ins)
    lefts = [a for _, ln in hits for a in _args_of('LEFT', ln)]
    mids = [a for _, ln in hits for a in _args_of('MID', ln)]
    check(all(a[1] == '1' for a in lefts) and
          sorted(set(a[1] for a in mids)) == ['2', 'DIM(cR)', 'swI'] and not any('RIGHT(' in ln for _, ln in hits),
          '1.7b: every LEFT counts 1 (%d), every MID starts at 2, DIM(cR) >= 2 or swI >= 1 (%d), no RIGHT'
          % (len(lefts), len(mids)))


def _args_of(name, code):
    """The argument lists of every NAME( call in one line of code (brackets nested)."""
    out = []
    for m in re.finditer(r'(?<![A-Za-z_])' + name + r'\(', code):
        j = m.end(); d = 1; cur = ''; parts = []
        while j < len(code) and d > 0:
            c = code[j]
            if c in '([{': d += 1
            elif c in ')]}': d -= 1
            if d == 0: break
            if c == ',' and d == 1: parts.append(cur.strip()); cur = ''
            else: cur += c
            j += 1
        parts.append(cur.strip())
        out.append(parts)
    return out


def _strip_comment(l):
    """A line without its // comment (a // inside a string literal is kept)."""
    q = False
    for j, ch in enumerate(l):
        if ch == '"':
            q = not q
        elif not q and l[j:j + 2] == '//':
            return l[:j]
    return l


def string_calls(path):
    """(routine, line, first argument, digits) of every STRING(x, 2, d) in the code."""
    out = []
    rt = '(file)'
    lines = open(path, encoding='utf-8').read().split('\n')
    for i, l in enumerate(lines, 1):
        m = re.match(r'^(?:EXPORT\s+)?([A-Za-z]\w*)\(.*\)\s*$', l)
        if m and i < len(lines) and lines[i].strip() == 'BEGIN':
            rt = m.group(1)
        code = ''; q = False; j = 0
        while j < len(l):
            ch = l[j]
            if ch == '"': q = not q
            if not q and l[j:j + 2] == '//': break
            code += ch; j += 1
        for m in re.finditer(r'(?<![A-Za-z_])STRING\(', code):
            if code[:m.start()].count('"') % 2: continue
            j = m.end(); d = 1; qq = False
            while j < len(code) and d > 0:
                c = code[j]
                if c == '"': qq = not qq
                if not qq:
                    if c in '([{': d += 1
                    elif c in ')]}': d -= 1
                j += 1
            arg = code[m.end():j - 1]
            parts = []; d = 0; cur = ''; qq = False
            for c in arg:
                if c == '"': qq = not qq
                if not qq:
                    if c in '([{': d += 1
                    if c in ')]}': d -= 1
                if c == ',' and d == 0 and not qq: parts.append(cur.strip()); cur = ''
                else: cur += c
            parts.append(cur.strip())
            if len(parts) == 3 and parts[1] == '2':
                out.append((rt, i, parts[0], parts[2]))
    return out


_CNT = 'a count, a total or a loop index: a whole number, so 0 or at least 1 (d = 0)'
_AX = 'an axis label: a multiple of a 1-2-5 step with d = -FLOOR(LOG(step)), so 0 or at least 10^-d'
_GU = 'guarded by the helper itself (es_PTxt, es_FmtNum, es_SigTxt: values below 10^-d take another form)'
_HALF = 'es_Cnt: a whole count (d = 0) or a Haldane half, x.5 (d = 1)'
_BIG = 'kept above 10^-d by its own range (named in CHANGES)'
SAFE = {
    ('es_PTxt', 'pxT', 'pxD'): _GU, ('es_PTxt', 'pxV', 'pxD'): _GU,
    ('es_SigTxt', 'sfV', 'sfD'): _GU,
    ('es_FmtNum', 'thr', 'dec'): _GU, ('es_FmtNum', 'x', 'dec'): _GU,
    ('es_Cnt', 'cnV', '0'): _HALF, ('es_Cnt', 'cnV', '1'): _HALF,
    ('es_GridDraw', 'esCel(2 * grR - 1) + esCel(2 * grR)', '0'): _CNT, ('es_GridDraw', 'grN', '0'): _CNT,
    ('es_GridDraw', 'esStr', '0'): _CNT,
    ('es_Mosaic', 'moO(moI)', '0'): _CNT, ('es_Mosaic', 'moRT(moR)', '0'): _CNT, ('es_Mosaic', 'moO(esTile)', '0'): _CNT,
    ('es_Mosaic', '100 * moCT(moC) / moN', '0'): 'the mosaic\'s "all" bar: drawn only when its tile is 12 px or more of 112, so 10 % or more',
    ('es_ReadPage', 'rpV(2 * rpI - 1)', '0'): _CNT, ('es_ReadPage', 'rpV(2 * rpI)', '0'): _CNT,
    ('es_ReadPage', 'rpV(2 * rpI - 1) + rpV(2 * rpI)', '0'): _CNT, ('es_ReadPage', 'rpB', '0'): _CNT,
    ('es_ReadPage', 'rpC', '0'): _CNT,
    ('es_HyperPage', 'hgV', 'hgDec'): _AX, ('es_HyperPage', 'hgLb', '0'): _CNT, ('es_HyperPage', 'hgA', '0'): _CNT,
    ('es_HyperPage', 'esQCut', '0'): _CNT, ('es_HyperPage', 'esQN', '0'): _CNT, ('es_HyperPage', 'hgAp', '0'): _CNT,
    ('es_HyperPage', 'hgA + hgB - hgAp', '0'): _CNT, ('es_HyperPage', 'hgA + hgB', '0'): _CNT,
    ('es_HyperPage', 'hgA + hgC - hgAp', '0'): _CNT, ('es_HyperPage', 'hgD - hgA + hgAp', '0'): _CNT,
    ('es_HyperPage', 'hgC + hgD', '0'): _CNT,
    ('es_CORPage', 'cpA', '0'): _CNT, ('es_CORPage', 'cpLb', '0'): _CNT,
    ('es_RiskBars', '100 * rbV', 'MAX(0, -FLOOR(LOG(100 * rbStp)))'): _AX,
    ('es_RiskBars', 'rbA', '0'): _CNT, ('es_RiskBars', 'rbN1', '0'): _CNT, ('es_RiskBars', 'rbC', '0'): _CNT,
    ('es_RiskBars', 'rbN0', '0'): _CNT,
    ('es_RiskBars', '100 * rbRe', '1'): 'Re as the "common" risk: shown only when Re >= 0.1, so 10.0 % or more',
    ('es_NNTIcons', 'ABS(niRD)', '3'): 'the NNT page\'s |RD|: this branch runs only when |RD| >= 0.001',
    ('es_NNTIcons', 'niNNT', '2'): 'the NNT, 1/|RD| with |RD| <= 1: 1 or more',
    ('es_NNTIcons', 'niM', '0'): _CNT,
    ('es_PrevDraw', '25 * pdI', '0'): _CNT,
    ('es_ExactPage', '25 * epI', '0'): _CNT, ('es_ExactPage', 'epK(epI)', '0'): _CNT, ('es_ExactPage', 'epN(epI)', '0'): _CNT,
    ('es_ExactPage', 'epK(epR)', '0'): _CNT, ('es_ExactPage', 'epN(epR)', '0'): _CNT,
    ('es_StratGrids', 'sgS', '0'): _CNT,
    ('es_StratTables', 'tbA + tbB + tbC + tbD', '0'): _CNT, ('es_StratTables', 'tbS', '0'): _CNT,
    ('es_StratTables', 'esSC(1) + esSC(2) + esSC(3) + esSC(4) + esSC(5) + esSC(6) + esSC(7) + esSC(8)', '0'): _CNT,
    ('es_RuleTxt', 'rtM(12)', '2'): 'the Breslow-Day p in the "homogeneous" branch: 0.05 or more',
    ('es_ForestDraw', 'fdV', 'fdW'): _AX, ('es_ForestDraw', 'fdI', '0'): _CNT,
    ('es_Help_SE', 'hsA', '0'): _CNT, ('es_Help_SE', 'hsB', '0'): _CNT, ('es_Help_SE', 'hsC', '0'): _CNT,
    ('es_Help_SE', 'hsD', '0'): _CNT, ('es_Help_SE', 'DIM(esSET) - 1', '0'): _CNT,
}


# ============================================================================ G2 (1.7b)
def part_g2():
    print('\n' + '=' * 78)
    print('G2. 1.7b: v1.7b against v1.7a')
    print('=' * 78)
    o, n = open(V17A, encoding='utf-8').read(), open(PPL, encoding='utf-8').read()
    B0, B1 = _bodies(o), _bodies(n)
    diff = sorted(x for x in set(B0) | set(B1) if B0.get(x) != B1.get(x))
    want = sorted(['EpiStats', 'es_Cas', 'es_FmtPct', 'es_FmtCI', 'es_Sgn', 'es_Grid', 'es_Arith', 'es_Mosaic',
                   'es_ReadPage', 'es_CORPage', 'es_RiskBars', 'es_NNTIcons', 'es_PctTxt', 'es_PrevDraw',
                   'es_ROCPage', 'es_ExactPage', 'es_RuleTxt', 'es_MHSummary', 'es_ForestDraw', 'es_Help_SE',
                   'es_Help_About'])
    print('  routines that differ from v1.7a (%d): %s' % (len(diff), ', '.join(diff)))
    check(diff == want, '1.7b: the routines that differ from v1.7a are exactly the %d listed in CHANGES' % len(want))
    check(_outside(o, diff) == _outside(n, diff), '1.7b: outside them only comments differ')
    # es_Cas: the IFERR line and the quote strip byte-identical; the INSTRING test inside DIM(cR) > 0
    def body(t, name):
        m = re.search(r'(?ms)^' + name + r'\(.*?\)\nBEGIN\n.*?^END;', t)
        return m.group(0) if m else ''
    co, cn = body(o, 'es_Cas'), body(n, 'es_Cas')
    keep = ['    cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + esS + ")" + CHAR(34) + ")"));',
            '  IF DIM(cR) >= 2 THEN',
            '    IF LEFT(cR, 1) == CHAR(34) AND MID(cR, DIM(cR), 1) == CHAR(34) THEN',
            '      cR := MID(cR, 2, DIM(cR) - 2);']
    check(all(k in co.split('\n') and k in cn.split('\n') for k in keep),
          '1.7b: es_Cas keeps the IFERR line and the quote strip byte-identical')
    cl = [ln for ln in cn.split('\n') if not ln.strip().startswith('//')]
    i = [k for k, ln in enumerate(cl) if 'INSTRING(' in ln]
    check(len(i) == 1 and cl[i[0] - 1] == '  IF DIM(cR) > 0 THEN' and cl[i[0] + 1] == '  END;'
          and cl[i[0]].strip() == [ln for ln in co.split('\n') if 'INSTRING(' in ln][0].strip(),
          '1.7b: es_Cas runs the unchanged undef/rror/infinity test only inside IF DIM(cR) > 0 (the brief\'s shape)')
    vs = [ln for ln in n.split('\n') if 'v1.7a' in ln and not ln.startswith('//')]
    check(not vs and n.count('"EpiStats v1.7b ══════════"') == 1 and '{"EpiStats v1.7b",' in n
          and n.split('\n')[2] == '// EPISTATS - v1.7b',
          '1.7b: the version reads v1.7b in the banner, the menu title and About; no code line says v1.7a')


def _bodies(txt):
    c = re.sub(r'(?s)#PYTHON.*?#END', '', txt)
    c = re.sub(r'//[^\n]*', '', c)
    out = {}
    for m in re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, re.S):
        out[m.group(1)] = re.sub(r'[ \t]+\n', '\n', m.group(0))
    return out


def _outside(t, names):
    c = re.sub(r'(?s)#PYTHON.*?#END', '', re.sub(r'//[^\n]*', '', t))
    if names:
        c = re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
    return re.sub(r'\s+', ' ', c)


# ============================================================================ the scientific strings
def part_sci():
    print('\n' + '=' * 78)
    print('SCI. Every scientific STRING result (h.sci_strings) of every harness run')
    print('=' * 78)
    new_h = [h for h in HARNESSES if h.vpath == os.path.basename(PPL)]
    old_h = [h for h in HARNESSES if h.vpath == os.path.basename(V17A)]
    new_s = sorted(set((r, t) for h in new_h for r, t in h.sci_where))
    old_s = sorted(set((r, t) for h in old_h for r, t in h.sci_where))
    print('  v1.7b: %d harness runs in this script (B, D, F), %d scientific results: %s'
          % (len(new_h), len(new_s), new_s or 'none'))
    print('         plus the v1.6 suite (E): %d runs, %d scientific results' % (E_SCI[0], E_SCI[1]))
    print('  v1.7a (F, for comparison): %d runs, %d distinct scientific results, in %s'
          % (len(old_h), len(old_s), ', '.join(sorted(set(r for r, _ in old_s)))))
    for r, t in old_s[:12]:
        print('      %-16s %s' % (r, t))
    check(len(new_h) >= 30 and not new_s and E_SCI[1] == 0,
          '1.7b: no scientific STRING result in any of the %d + %d harness runs of v1.7b' % (len(new_h), E_SCI[0]))

def main():
    t0 = time.time()
    part_a(); part_b(); part_c(); part_d(); part_e(); part_g()
    part_f(); part_g2(); part_sci()
    print('\n' + '=' * 78)
    print('%s: %d checks, %d failures  [%.0f s]' % ('ALL CHECKS PASSED' if not FAILS else 'FAILURES', NCHK[0], len(FAILS), time.time() - t0))
    for f in FAILS:
        print('  -', f)
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
