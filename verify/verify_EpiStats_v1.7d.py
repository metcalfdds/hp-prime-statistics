#!/usr/bin/env python3
"""verify_EpiStats_v1.7d.py -- checks for EpiStats v1.7d (HP Prime PPL), 19 Oct 2026: E1, E2, E3, E4, E6, E7, E8, E9,
E10 and E11 of the fleet review of 19 Oct 2026.  Built from verify_EpiStats_v1.7c.py: every check is kept.  Changed:
  - the files: this script lives in fix19/ beside EpiStats_v1.7d.txt; its predecessors (v1.7c, v1.7b, v1.7a, v1.7),
    the v1.6 suite (verify_EpiStats.py) and the harness are read from /home/claude/work/out by absolute path, and
    part B compares the shared Clopper-Pearson routines with CICatcher beta 2b there (the v1.7c script named the
    superseded CICatcher_beta2a.txt and stopped with FileNotFoundError on a folder of current files: E10, review
    item 22); it skips that comparison cleanly if the file is absent;
  - the harness is ppl_run_v3e (v3d plus the Prime's minus in a scientific exponent, off by default), as the
    brief asks; every v3d-era check gives the same result there;
  - part H (1.7c) keeps checking the v1.7c change set: it compares the v1.7c file with v1.7b, as the v1.7c script's
    G2 kept comparing v1.7b with v1.7a;
  - F4's reason for es_Cnt's bare STRING(x, 2, 1) now names the 0.1 floor (E11).
New:
  I  (1.7d) each fix against v1.7c, end to end: E1 the sample-size edges; E2 an empty row in Risk Analysis; E3 an
     empty column in Sensitivity & Specificity; E4 the 2x2 RD with an empty row; E8 McNemar, the M-H chi-square and
     Breslow-Day as lower tails (in doubles and in the Prime's 12 digits); E6, E9 Incidence Rates; E11 es_Cnt; E10
     and the code: the routine diff against v1.7c, the version strings, the disclaimer line, no comment inside a
     bracket, the new names, INSTRING, LOCAL sizes; I11 E7 (added the same day): Risk Analysis with |RD| below
     0.000001, and the review's own E7 check on v1.7c, on v1.7d before E7 (rebuilt in memory by undoing the three
     E7 edits) and on v1.7d;
  REVIEW  the review's check_EpiStats.py (511 checks) on v1.7d and on v1.7c, with five expectations moved where the
     fix changes what is right (listed in the part; 508 checks with them).
SCI now also lists the review's runs of v1.7d apart (none prints a scientific result since E7).

(The v1.7c docstring follows.)

verify_EpiStats_v1.7c.py -- checks for EpiStats v1.7c (HP Prime PPL), 17 Oct 2026, evening: no "=" before a
relation, and the chi-square p (1 df) as a lower normal tail, never exactly 0.  Built from
verify_EpiStats_v1.7b.py: every check is kept and runs on v1.7c (harness ppl_run_v3d, as before).  Changed:
F3's first run expects "OR = ad/bc < 0.001" (1.7c), and F3's word comparison reads v1.7a's text the v1.7c
way ("= <" -> "<", "0.00000 *" -> "< 0.00001 *", "p=0.0000" -> "p<0.0001"); G2 keeps comparing the v1.7b
and v1.7a files (that change set).  New: H (1.7c):
  H1 every display that read "= <", or a label ending in "=" before a floored value, reached end to end in
     modules 1-6, v1.7c against v1.7b, everything else on those pages unchanged;
  H2 2 NORMALD_CDF(0, 1, -sqrt(x)) against SciPy's chi2.sf(x, 1), and the 2 x 2 page's p-values in doubles
     and in the Prime's 12 digits (CHISQUARE_CDF and NORMALD_CDF rounded to 12 significant digits);
  H3 a sweep of 54 tables through modules 1, 2 and 3;  H4 es_EqLb, es_EqV, es_EqTxt;
  H5 the exact code-line diff, the new names, the version strings, no comment inside a bracket,
     INSTRING as in v1.7b, at most 6 names per LOCAL;  H6 the sites left alone.
SCI (kept) now covers H's runs of v1.7c too.

(The v1.7b docstring follows.)

verify_EpiStats_v1.7b.py -- checks for EpiStats v1.7b (HP Prime PPL), 17 Oct 2026: the two string
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

Run:  python3 verify_EpiStats_v1.7c.py      (numpy, scipy, statsmodels, icas, the harness v3d)
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
OUT = '/home/claude/work/out'                      # 1.7d: the predecessors, the v1.6 suite and the harness live here
PPL = os.path.join(HERE, 'EpiStats_v1.7d.txt')     # 1.7d
V17C = os.path.join(OUT, 'EpiStats_v1.7c.txt')     # 1.7d
V17B = os.path.join(OUT, 'EpiStats_v1.7b.txt')     # 1.7c
V17A = os.path.join(OUT, 'EpiStats_v1.7a.txt')
V17 = os.path.join(OUT, 'EpiStats_v1.7.txt')
CQ = os.path.join(OUT, 'CICatcher_beta2b.txt')     # 1.7d (E10, review item 22): the current CICatcher, not beta 2a
B_CQ = [0]                                         # 1.7d: 1 once part B has compared the shared routines with it
sys.path.insert(0, OUT)
import ppl_run_v3e as ppl_run_v3d                                    # noqa: E402  (1.7d: harness v3e)
from ppl_run_v3e import Harness, PPLError, giac_eval, prime_print   # noqa: E402

# 1.7b: every harness made in this run is kept, and every scientific STRING result is
# recorded with the routine that printed it, so the end of the run can list them all
HARNESSES = []
_h_init = Harness.__init__
_h_sh = Harness._string_home


class _Rec(object):
    """1.7d: what part SCI reads of a harness -- its file and its scientific results -- so that the harness itself
    (every drawing call of its run) can go once the run is over; with the review's 1,000-odd runs added, keeping them
    all ran a shared machine out of memory"""
    def __init__(self, h):
        self.vpath, self.sci_where, self.review = h.vpath, h.sci_where, False


def _init(self, path, *a, **k):
    _h_init(self, path, *a, **k)
    self.vpath = os.path.basename(path)
    self.sci_where = []
    HARNESSES.append(_Rec(self))


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
    # 1.7d: the current CICatcher (beta 2b, in out/); skipped cleanly if it is not there
    if os.path.exists(CQ):
        q = body(CQ, ['cqBinCheck', 'cqCPB', 'cqCPInt'], 'cq')
        B_CQ[0] = 1
        check(all(e) and e == q, 'es_BinCheck / es_CPB / es_CPInt are line for line the same as CICatcher beta 2b\'s cq* copies '
              '(%d lines)' % sum(x.count('\n') for x in e))
    else:
        print('  (CICatcher_beta2b.txt is not in %s: the comparison of the shared routines is skipped)' % OUT)


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
import ppl_run_v3e as ppl_run_v3d
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
        f.write(E_SHIM % OUT)
        shim = f.name
    try:
        r = subprocess.run([sys.executable, shim, os.path.join(OUT, 'verify_EpiStats.py'), PPL],
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
    # 1.7c: v1.7a's text read the v1.7c way first (no "=" before a relation; the chi-square p never 0)
    _17c = {'0.00000 *': '< 0.00001 *', 'p=0.0000': 'p<0.0001'}
    # (a p the harness's doubles still underflow to 0 -- a chi-square above about 1,400 -- stays as it was)
    to = [[(x if x in _17c and x in q else _17c.get(x, x.replace('= < ', '< ').replace('= > ', '> '))) for x in p]
          for p, q in zip(to, tn)]
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
         [('OR = ad/bc < 0.001   (0.00-0.00)', None),   # 1.7c: no "=" before the relation ('Risk if exposed, a/(a+b) = 0.0%', None),
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
_HALF = 'es_Cnt: a whole count (d = 0), or a Haldane half or a person-time of 0.1 or more (d = 1; below 0.1 es_SigTxt, 1.7d E11)'
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
    o, n = open(V17A, encoding='utf-8').read(), open(V17B, encoding='utf-8').read()   # 1.7c: the two files
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
    new_h = [h for h in HARNESSES if h.vpath == os.path.basename(PPL) and not getattr(h, 'review', False)]   # 1.7d
    old_h = [h for h in HARNESSES if h.vpath == os.path.basename(V17A)]
    new_s = sorted(set((r, t) for h in new_h for r, t in h.sci_where))
    old_s = sorted(set((r, t) for h in old_h for r, t in h.sci_where))
    print('  v1.7d: %d harness runs in this script (B, D, F, I), %d scientific results: %s'
          % (len(new_h), len(new_s), new_s or 'none'))
    print('         plus the v1.6 suite (E): %d runs, %d scientific results' % (E_SCI[0], E_SCI[1]))
    print('  v1.7a (F, for comparison): %d runs, %d distinct scientific results, in %s'
          % (len(old_h), len(old_s), ', '.join(sorted(set(r for r, _ in old_s)))))
    for r, t in old_s[:12]:
        print('      %-16s %s' % (r, t))
    check(len(new_h) >= 30 and not new_s and E_SCI[1] == 0,
          '1.7b, 1.7d: no scientific STRING result in any of the %d + %d harness runs of v1.7d (the review\'s own runs: '
          'part REVIEW)' % (len(new_h), E_SCI[0]))


# ============================================================================ H (1.7c)
# (1.7d: these checks keep comparing v1.7c with v1.7b, its own change set)


def _rw17c(s):
    """v1.7b's text written the v1.7c way: "= <" -> "<", "= >" -> ">" (nothing else)"""
    return s.replace('= < ', '< ').replace('= > ', '> ')


def _m1all(t):
    def f(h):
        h.choose(1); grid(h, t); h.press('Down', 'Down'); h.press('Right', 'Right', 'Right', 'Right')
        h.press('Down', 'Down', 'Down', 'Down', 'Down', 'Down'); h.press('Right'); h.press('Down', 'Down', 'Down', 'Down')
        h.press('Right'); h.press('Esc'); h.choose(8)
    return f


def _m3all(t):
    def f(h):
        h.choose(3); grid(h, t); h.press('Right', 'Right', 'Right'); h.press('Enter'); h.press('Right')
        h.press('Down', 'Down', 'Down'); h.press('Esc'); h.choose(8)
    return f


def _m4(v):
    def f(h):
        h.choose(4); h.answer(v); h.press('Right', 'Right', 'Esc'); h.choose(8)
    return f


def _m6(k, v):
    def f(h):
        h.choose(6); h.choose(k); h.answer(v); h.press('Esc'); h.choose(8)
    return f


_SAME = {('p=0.0000', 'p<0.0001'), ('p=< 0.0001', 'p<0.0001'), ('0.00000 *', '< 0.00001 *')}


def _same17c(o, n):
    """v1.7b's text o and v1.7c's n say the same thing the v1.7c way: no "=" before a relation, a split label
    without its closing "=", or a chi-square p that v1.7b printed as 0"""
    return o == n or _rw17c(o) == n or (o.endswith(' =') and o[:-2] == n) or (o, n) in _SAME


def _alltx(h):
    return [t.text for p in h.pages for t in sorted(p.texts, key=lambda t: (t.y, t.x))]


def _pair(script, cas='fail'):
    hn, en = _run_quiet(V17C, script, cas)            # 1.7d: H checks the v1.7c change set
    ho, eo = _run_quiet(V17B, script, cas)
    return hn, en, ho, eo


def part_h():
    print('\n' + '=' * 78)
    print('H. 1.7c: no "=" before a relation; the chi-square p never 0 (v1.7c against v1.7b, harness v3d)')
    print('=' * 78)
    # H1. every display that read "= <" (or a label ending "=" before a floored value), reached end to end
    # (case, script, the v1.7c lines that must be there, the v1.7b lines they replace)
    H1 = [
        ('module 1, cohort 1 99999 50 50', _m1all([1, 99999, 50, 50]),
         ['RR = Re/Ru < 0.001   (0.00-0.00)', 'OR = ad/bc < 0.001   (0.00-0.00)'],
         ['RR = Re/Ru = < 0.001   (0.00-0.00)', 'OR = ad/bc = < 0.001   (0.00-0.00)']),
        ('module 1, 1 2000 2000 1 (page 7)', _m1all([1, 2000, 2000, 1]),
         ['Sample OR = ad/bc < 0.000001, Woolf CI (0.00-0.00)', 'LR+ = sens/(1-spec) < 0.01,  LR- = 2000.000'],
         ['Sample OR = ad/bc = < 0.000001, Woolf CI (0.00-0.00)', 'LR+ = sens/(1-spec) = < 0.01,  LR- = 2000.000']),
        ('module 1, 9999 1 1 9999 (diagnostic tab)', _m1all([9999, 1, 1, 9999]),
         ['LR+ = sens/(1-spec) = 9999,  LR- < 0.001'], ['LR+ = sens/(1-spec) = 9999,  LR- = < 0.001']),
        ('module 1, 80 10 10 80 (chi-square 113)', _m1all([80, 10, 10, 80]), ['< 0.00001 *'], ['0.00000 *']),
        ('module 2, 1 99999 50 50 (page 2)', _s_m2([1, 99999, 50, 50]), ['RR = Re / Ru', 'OR = (a×d)/(b×c)'],
         ['RR = Re / Ru =', 'OR = (a×d)/(b×c) =']),
        ('module 2, 5002 4998 5000 5000 (ERR 0.0004)', _s_m2([5002, 4998, 5000, 5000]), ['ERR = RR - 1'],
         ['ERR = RR - 1 =']),
        ('module 3, 1 1000 999 10 (ROC, page 3)', _m3all([1, 1000, 999, 10]), [' = 0.001/0.990 < 0.01', 'p<0.0001'],
         [' = 0.001/0.990 = < 0.01', 'p=0.0000']),
        ('module 3, 9999 1 1 9999 (ROC)', _m3all([9999, 1, 1, 9999]), [' = 0.000/1.000 < 0.001'],
         [' = 0.000/1.000 = < 0.001']),
        ('module 4, 1 50 200000 100', _m4([1, 50, 200000, 100]), ['< 0.01 per 1,000 person-time', 'IRR = IRe / IRu'],
         ['= < 0.01 per 1,000 person-time', 'IRR = IRe / IRu =']),
        ('module 4, 10001 10000 1E9 1E9', _m4([10001, 10000, 1e9, 1e9]),
         ['< 0.001 per 1,000 PT', 'ERR = IRR - 1', 'IRD = IRe - IRu'], ['= < 0.001 per 1,000 PT', 'ERR = IRR - 1 =',
                                                                       'IRD = IRe - IRu =']),
        ('module 4, 100 0 1 1 (NNT 0.01)', _m4([100, 0, 1, 1]), ['PT-NNH = 1/IRD'], ['PT-NNH = 1/IRD =']),
        ('module 5 OR, two strata 1 9999 1000 1000', _s_m5(1, [1, 9999, 1000, 1000], [1, 9999, 1000, 1000]),
         ['OR₁ < 0.001  (0.00-0.00)', 'Crude OR < 0.001  (0.00-0.00)', 'M-H OR < 0.001  (0.00-0.00)',
          'M-H OR < 0.001  (0.00-0.00), both'],
         ['OR₁ = < 0.001  (0.00-0.00)', 'Crude OR = < 0.001  (0.00-0.00)', 'M-H OR = < 0.001  (0.00-0.00)',
          'M-H OR = < 0.001  (0.00-0.00), both']),
        ('module 6, two proportions, power 0.5001', _m6(1, [0.5, 0.3, 0.05, 0.5001]), ['z_α/2 = 1.960   z_β < 0.001'],
         ['z_α/2 = 1.960   z_β = < 0.001']),
        ('module 6, two proportions, power 0.4999', _m6(1, [0.5, 0.3, 0.05, 0.4999]), ['z_β > -0.001'], ['z_β = > -0.001']),
        ('module 6, two means, delta 0.0001', _m6(2, [0.0001, 1, 0.05, 0.8]), ["Effect size (Cohen's d) < 0.001"],
         ["Effect size (Cohen's d) = < 0.001"]),
        ('module 6, one proportion, alpha 0.99999', _m6(3, [0.5, 0.05, 0.99999]), ['z_α/2 < 0.0001'],
         ['z_α/2 = < 0.0001']),
        ('module 6, one mean, alpha 0.99999', _m6(4, [10, 2, 0.99999]), ['z_α/2 < 0.0001'], ['z_α/2 = < 0.0001']),
    ]
    for label, script, wn, wo in H1:
        hn, en, ho, eo = _pair(script)
        tn, to = _alltx(hn), _alltx(ho)
        only_o, only_n = sorted(set(to) - set(tn)), sorted(set(tn) - set(to))
        print('    %s\n      v1.7b only: %s\n      v1.7c only: %s' % (label, only_o[:6], only_n[:6]))
        lab_ok = all(any(w == s or w in s for s in tn) for w in wn) and all(any(w == s or w in s for s in to) for w in wo)
        check(en is None and eo is None and lab_ok and len(tn) == len(to)
              and not any('= <' in s or '= >' in s or 'p=< ' in s for s in tn),
              '1.7c: %s -- v1.7c reads %s (v1.7b: %s)' % (label, '; '.join(repr(w) for w in wn),
                                                        '; '.join(repr(w) for w in wo)))
        # nothing else changed: each v1.7b text is the v1.7c one, through the rewrite, or one of the named lines
        rest = [(o, n) for o, n in zip(to, tn) if not _same17c(o, n) and o not in wo]
        check(not rest, '1.7c: %s -- every other text is v1.7b\'s, or v1.7b\'s without "= <"' % label)
        if rest:
            print('      differs:', rest[:3])

    # H2. the chi-square p with 1 df: 2 NORMALD_CDF(0, 1, -sqrt(x)) against SciPy's chi2.sf, and the Prime's 12 digits
    print('\n  H2. the chi-square p (1 df), as the lower normal tail')
    h = new('fail')
    bad = []
    for x in [0, 0.001, 0.5, 1, 3.841459, 6.63, 10, 25, 52, 75, 113, 400, 1000]:
        g = h.execute('2 * NORMALD_CDF(0, 1, -(%r^0.5))' % float(x))
        w = stats.chi2.sf(x, 1)
        if abs(g - w) > 1e-12 * w + 1e-15:
            bad.append((x, g, w))
    check(not bad, '1.7c: 2 NORMALD_CDF(0, 1, -sqrt(x)) = chi2.sf(x, 1) to 1E-12 relative, x from 0 to 1000 (13 values)'
          + (' %s' % bad[:2] if bad else ''))
    _C0 = ppl_run_v3d._StatFns.CHISQUARE_CDF

    def _c12(self, a):
        v = _C0(self, a)
        return float('%.12g' % v) if v == v else v
    _N0 = ppl_run_v3d._StatFns.NORMALD_CDF

    def _n12(self, a):
        v = _N0(self, a)
        return float('%.12g' % v) if v == v else v
    for digits in (False, True):
        if digits:
            ppl_run_v3d._StatFns.CHISQUARE_CDF, ppl_run_v3d._StatFns.NORMALD_CDF = _c12, _n12
        rows = []
        for t in ([30, 10, 10, 30], [40, 10, 10, 40], [60, 10, 10, 60], [80, 10, 10, 80]):
            hn, en, ho, eo = _pair(_s_m1(t))
            gn = [s for s in _alltx(hn) if s.endswith(' *') or s.endswith('*')][:2]
            go = [s for s in _alltx(ho) if s.endswith(' *') or s.endswith('*')][:2]
            a, b, c, d = t
            n = a + b + c + d
            x2 = n * (a * d - b * c) ** 2 / ((a + b) * (c + d) * (a + c) * (b + d))
            rows.append((t, x2, stats.chi2.sf(x2, 1), go, gn))
        ppl_run_v3d._StatFns.CHISQUARE_CDF, ppl_run_v3d._StatFns.NORMALD_CDF = _C0, _N0
        print('    %s:' % ('the Prime\'s 12 digits' if digits else 'doubles'))
        for t, x2, w, go, gn in rows:
            print('      %s  chi-square %.1f, SciPy p %.2g:  v1.7b %s;  v1.7c %s' % (t, x2, w, go, gn))
        check(all(len(gn) == 2 and not any(s.startswith('0.00000') for s in gn) for _, _, _, _, gn in rows)
              and all(s.startswith('< 0.00001') for r in rows[1:] for s in r[4]),
              '1.7c (%s): the 2 x 2 page\'s two p-values never read "0.00000" for a chi-square from %.0f to %.0f '
              '("< 0.00001 *" from 36 up)'
              % ('12 digits' if digits else 'doubles', rows[0][1], rows[-1][1]))
        zeros = [r for r in rows if any(s.startswith('0.00000') for s in r[3])]
        print('      v1.7b read "0.00000 *" in %d of the %d' % (len(zeros), len(rows)))
        if digits:
            check(len(zeros) > (1 if True else 0),
                  '1.7c (12 digits): v1.7b read "0.00000 *" (1 - CHISQUARE_CDF exactly 0) where a smaller chi-square '
                  'read "< 0.00001 *" (%d of the %d tables)' % (len(zeros), len(rows)))
    # ordinary p-values unchanged
    same = []
    for t in ([10, 20, 30, 40], [12, 5, 7, 14], [5, 5, 5, 5], [30, 10, 10, 30], [1, 2, 3, 4]):
        hn, en, ho, eo = _pair(_s_m1(t))
        same.append(_alltx(hn) == _alltx(ho))
    check(all(same), '1.7c: five ordinary tables (chi-square below 50): module 1 is unchanged, every page')

    # H3. a sweep of tables through modules 1, 2, 3 and 5: v1.7c = v1.7b written without "= <", and the
    # split labels that lose their "=" only where their value is floored
    print('\n  H3. a sweep')
    tables = [[a, b, c, d] for a in (1, 10, 500) for b in (1, 99, 5000) for c in (1, 50) for d in (1, 50, 9999)]
    nsame = nrw = 0
    odd = []
    rewrites = set()
    for t in tables:
        for sc in (_s_m1(t), _s_m2(t), _s_m3(t)):
            hn, en, ho, eo = _pair(sc)
            tn, to = _alltx(hn), _alltx(ho)
            if en or eo or len(tn) != len(to):
                odd.append((t, en, eo, len(tn), len(to)))
                continue
            if tn == to:
                nsame += 1
                continue
            ok = True
            for o, n in zip(to, tn):
                if o == n:
                    continue
                if _same17c(o, n):
                    rewrites.add((o, n))
                else:
                    ok = False
                    odd.append((t, o, n))
            nrw += ok
    print('    %d tables x 3 modules: %d identical, %d differ only as above, %d otherwise' % (len(tables), nsame, nrw,
                                                                                         len(odd)))
    for o, n in sorted(rewrites)[:14]:
        print('      "%s"  ->  "%s"' % (o, n))
    print('      (%d distinct rewritten lines)' % len(rewrites))
    check(not odd and nrw > 0, '1.7c: %d runs of modules 1, 2 and 3: v1.7c is v1.7b without "= <" (and the p-value '
          'and label forms above), nothing else' % (3 * len(tables)) + (' %s' % odd[:3] if odd else ''))

    # H4. the helpers
    print('\n  H4. es_EqLb, es_EqV, es_EqTxt')
    h = new('fail')
    for fn, args, want in (('es_EqLb', ('IRR = IRe / IRu', '1.250'), 'IRR = IRe / IRu ='),
                           ('es_EqLb', ('IRR = IRe / IRu', '< 0.001'), 'IRR = IRe / IRu'),
                           ('es_EqLb', ('ERR = IRR - 1', '> -0.001'), 'ERR = IRR - 1'),
                           ('es_EqLb', ('ERR = IRR - 1', ''), 'ERR = IRR - 1 ='),
                           ('es_EqV', ('0.50',), '= 0.50'), ('es_EqV', ('< 0.01',), '< 0.01'),
                           ('es_EqV', ('',), '= '), ('es_EqTxt', ('RR = Re/Ru', '< 0.001'), 'RR = Re/Ru < 0.001'),
                           ('es_EqTxt', ('RR = Re/Ru', '3.000'), 'RR = Re/Ru = 3.000')):
        g = h.call(fn, *args)
        check(g == want, '1.7c: %s%s = "%s"' % (fn, args, g))

    # H5. the code
    print('\n  H5. the code')
    import difflib
    src_b, src_c = open(V17B, encoding='utf-8').read(), open(V17C, encoding='utf-8').read()   # 1.7d: the v1.7c file
    cb = [l.strip() for l in (_strip_comment(x) for x in src_b.split('\n')) if l.strip()]
    cc = [l.strip() for l in (_strip_comment(x) for x in src_c.split('\n')) if l.strip()]
    rem, add = [], []
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, cb, cc, autojunk=False).get_opcodes():
        if op != 'equal':
            rem += cb[a1:a2]
            add += cc[b1:b2]
    print('    code lines removed %d, added %d' % (len(rem), len(add)))
    helpers = ['es_EqLb(lbL, lbS)', 'BEGIN', 'IF DIM(lbS) > 0 THEN',
               'IF LEFT(lbS, 1) == "<" OR LEFT(lbS, 1) == ">" THEN RETURN lbL; END;', 'END;', 'RETURN lbL + " =";',
               'END;', 'es_EqV(evS)', 'BEGIN', 'IF DIM(evS) > 0 THEN',
               'IF LEFT(evS, 1) == "<" OR LEFT(evS, 1) == ">" THEN RETURN evS; END;', 'END;', 'RETURN "= " + evS;',
               'END;']
    vers = {'"EpiStats v1.7b ══════════",': '"EpiStats v1.7c ══════════",', '{"EpiStats v1.7b",': '{"EpiStats v1.7c",'}
    sites = 0
    exp = list(helpers)
    for l in rem:
        n = l
        for a, b in vers.items():
            n = n.replace(a, b)
        n = re.sub(r'1 - CHISQUARE_CDF\(1, (\w+)\)', r'2 * NORMALD_CDF(0, 1, -(\1^0.5))', n)
        exp.append(n)
    # the display sites: every removed display line comes back through es_EqTxt / es_EqLb / es_EqV / the p form
    added_disp = [l for l in add if any(k in l for k in ('es_EqTxt(', 'es_EqLb(', 'es_EqV(', '"p<0.0001"'))
                  and l not in helpers]
    sites = sum(l.count('es_EqTxt(') + l.count('es_EqLb(') + l.count('es_EqV(') for l in added_disp) + \
        sum(l.count('"p<0.0001"') for l in added_disp)
    chis = [l for l in add if 'NORMALD_CDF(0, 1, -(' in l]
    other = [l for l in add if l not in helpers and l not in added_disp and l not in chis
             and l not in vers.values() and not any(v in l for v in vers.values())]
    check(len(chis) == 3 and all(re.sub(r'2 \* NORMALD_CDF\(0, 1, -\((\w+)\^0\.5\)\)', r'1 - CHISQUARE_CDF(1, \1)', l)
                                 in rem for l in chis),
          '1.7c: the three chi-square p lines (2603, 2618, 3996) are the only other computing change')
    check(sites == 30 and not other, '1.7c: the added code is the two helpers, the 29 display sites and the p form '
          '(%d), the 3 p lines and the 2 version strings, nothing else%s' % (sites, (' %s' % other[:3]) if other else ''))
    # each changed display line, its new parts written back in v1.7b's form, is v1.7b's line
    def _back(l):
        l = re.sub(r'IFTE\(EP_chisq_p < 0\.0001, "p<0\.0001", "p=" \+ es_FmtNum\(EP_chisq_p, 4\)\)',
                   '"p=" + es_FmtNum(EP_chisq_p, 4)', l)
        l = re.sub(r'es_EqLb\(("[^"]*"), es_FmtNum\([^()]*\)\)', lambda m: m.group(1)[:-1] + ' ="', l)
        l = re.sub(r'es_EqV\((es_FmtNum\([^()]*\))\)', r'"= " + \1', l)
        # es_EqTxt(A, B) -> A + " = " + B, with A and B split at the top-level comma
        while 'es_EqTxt(' in l:
            i = l.index('es_EqTxt(')
            j, dpt, q, cm = i + 9, 1, False, None
            while dpt:
                ch = l[j]
                if ch == '"':
                    q = not q
                elif not q:
                    if ch == '(':
                        dpt += 1
                    elif ch == ')':
                        dpt -= 1
                    elif ch == ',' and dpt == 1 and cm is None:
                        cm = j
                j += 1
            a, b = l[i + 9:cm].strip(), l[cm + 1:j - 1].strip()
            a = a[:-1] + ' = "' if a.endswith('"') else a + ' + " = "'
            l = l[:i] + a + ' + ' + b + l[j:]
        return l.replace('" + " = "', ' = "').replace('" = " + "', '').replace('"" + ', '')
    back = sorted(_back(l) for l in added_disp)
    remd = sorted(l for l in rem if not any(v in l for v in vers) and 'CHISQUARE_CDF' not in l)
    mism = sorted(set(back) ^ set(remd))
    check(back == remd, '1.7c: each changed display line, written back without the helpers, is v1.7b\'s line (%d lines)'
          % len(remd) + (' %s' % mism[:4] if mism else ''))
    names = {w.strip().upper() for w in open('/mnt/user-data/uploads/HP-Prime/HP_Prime_Builtin_Names.txt',
                                             encoding='utf-8') if w.strip()}
    new_names = ['es_EqLb', 'es_EqV', 'lbL', 'lbS', 'evS']
    check(not [x for x in new_names if x.upper() in names] and src_c.count('\nes_EqLb(lbL, lbS)\n') == 1
          and src_c.count('\nes_EqV(evS)\n') == 1
          and src_c.index('\nes_EqLb(lbL, lbS)') < src_c.index('es_EqLb("') and src_c.index('\nes_EqV(evS)') < src_c.index('es_EqV(es_'),
          '1.7c: the new names %s are not built-ins (ignoring case); the two helpers carry the es_ tag, are defined '
          'once, before their first use' % ', '.join(new_names))
    vl = src_c.split('\n')
    check(vl[2] == '// EPISTATS - v1.7c' and src_c.count('"EpiStats v1.7c ══════════"') == 1 and '{"EpiStats v1.7c",' in src_c
          and '// What changed in v1.7c (17 Oct 2026, evening)' in src_c
          and not [l for l in vl if 'v1.7b' in _strip_comment(l)],
          '1.7c: the version reads v1.7c in the banner, the menu title and About; a "What changed in v1.7c" paragraph; '
          'no code line says v1.7b')
    dep, badc = 0, []
    for n, l in enumerate(vl, 1):
        q = False
        for j, ch in enumerate(l):
            if ch == '"':
                q = not q
            elif not q:
                if l[j:j + 2] == '//':
                    if dep:
                        badc.append(n)
                    break
                dep += (ch in '({[') - (ch in ')}]')
    check(not badc, '1.7c: no // comment inside an open bracket' + (' %s' % badc[:5] if badc else ''))
    check(sum('INSTRING(' in l for l in cc) == sum('INSTRING(' in l for l in cb)
          and max(len(m.split(',')) for m in re.findall(r'^\s*LOCAL ([^;(]*);', '\n'.join(cc), re.M)) <= 6,
          '1.7c: INSTRING as in v1.7b; every LOCAL line holds at most 6 names')

    # H6. what was looked at and left alone
    print('\n  H6. left alone')
    from scipy.stats.contingency import odds_ratio
    mle = min(odds_ratio([[1, b], [c, 1]], kind='conditional').statistic for b, c in ((999, 999), (998, 1000), (1500, 498)))
    check(mle > 1e-6, '1.7c: the conditional MLE OR (page 7, the reading) is at least %.3g at N <= 2000 (SciPy), above '
          'es_SigTxt\'s floor 1E-6, so its lines (2139, 2471) never start with "<"' % mle)
    hn, en, ho, eo = _pair(_s_m2([1, 2999, 1, 999]))
    nn = [s for s in _alltx(hn) if s.startswith('NNT')]
    print('    the risk NNT (1/RD, RD at most 1, so NNT >= 1): %s' % nn[:2])
    check(all('< ' not in s for s in nn), '1.7c: the risk module\'s NNT is 1/|RD| >= 1, never floored (3187, 3195 left alone)')


# ---- 1.7d (E7): the three code edits, exactly (old, new).  Part I undoes them (new -> old) to rebuild v1.7d as it
# stood before E7, so that the review's E7 check can be shown failing there and passing on the file.
E7_EDITS = [
    # es_Module_RiskAnalysis: EP_NNT takes the 999 sentinel when |RD| < 0.000001
    ("""    IF RD <> 0 THEN
        NNT := 1 / ABS(RD);
        EP_NNT := NNT;
    ELSE
        NNT := 999;
        EP_NNT := 999;
    END;
""", """    IF RD <> 0 THEN
        NNT := 1 / ABS(RD);
        EP_NNT := NNT;
        // v1.7d (E7): when |RD| is below 0.000001 the NNT is above
        // 1,000,000, no meaningful number of people to treat (and from
        // 1E12 on, STRING printed it in scientific form, "1.00E12").
        // Pages 3 and 5 say so, reading RD itself; NNT keeps its value
        // for them, and EP_NNT takes the 999 "undefined" sentinel that
        // Help > Variables names, as it already did for RD = 0.
        IF ABS(RD) < 0.000001 THEN EP_NNT := 999; END;
    ELSE
        NNT := 999;
        EP_NNT := 999;
    END;
"""),
    # es_Risk_Page3: the NNT block says "> 1,000,000" and why
    ("""    y := y + 18;
    IF RD > 0 THEN
        TEXTOUT_P("NNT (harm) = 1/RD =", G1, 10, y, 2, RGB(0,0,0));
        TEXTOUT_P(es_FmtNum(NNT, 1), G1, 180, y, 2, RGB(255,0,0));
        y := y + 16;
        TEXTOUT_P("Interpretation: For every " + STRING(CEILING(NNT),1,0) + " exposed,", G1, 10, y, 1, RGB(90,90,90));
        y := y + 12;
        TEXTOUT_P("1 additional case occurs due to exposure", G1, 10, y, 1, RGB(90,90,90));
    ELSE
        IF RD < 0 THEN
            TEXTOUT_P("NNT (benefit) = 1/|RD| =", G1, 10, y, 2, RGB(0,0,0));
            TEXTOUT_P(es_FmtNum(NNT, 1), G1, 210, y, 2, RGB(0,140,60));
            y := y + 16;
            TEXTOUT_P("Interpretation: Treat " + STRING(CEILING(NNT),1,0) + " to prevent", G1, 10, y, 1, RGB(90,90,90));
            y := y + 12;
            TEXTOUT_P("1 case", G1, 10, y, 1, RGB(90,90,90));
        ELSE
            TEXTOUT_P("NNT: undefined (RD = 0)", G1, 10, y, 2, RGB(90,90,90));
        END;
    END;
    y := y + 26;
""", """    y := y + 18;
    // v1.7d (E7): |RD| below 0.000001 (but not 0) gives an NNT above
    // 1,000,000, which tells a reader nothing, and from 1E12 on the
    // interpretation's STRING(CEILING(NNT), 1, 0) and es_FmtNum were in
    // scientific form ("For every 1.00000100011E12 exposed").  The line
    // reads "> 1,000,000", with no "=" before it, in its side's colour,
    // and says why.  Every other RD draws what v1.7c drew.
    IF RD <> 0 AND ABS(RD) < 0.000001 THEN
        IF RD > 0 THEN
            TEXTOUT_P("NNT (harm) = 1/RD", G1, 10, y, 2, RGB(0,0,0));
            TEXTOUT_P("> 1,000,000", G1, 180, y, 2, RGB(255,0,0));
        ELSE
            TEXTOUT_P("NNT (benefit) = 1/|RD|", G1, 10, y, 2, RGB(0,0,0));
            TEXTOUT_P("> 1,000,000", G1, 210, y, 2, RGB(0,140,60));
        END;
        y := y + 16;
        TEXTOUT_P("RD near 0 (|RD| < 0.000001): no meaningful NNT;", G1, 10, y, 1, RGB(90,90,90));
        y := y + 12;
        TEXTOUT_P("the two risks are practically equal", G1, 10, y, 1, RGB(90,90,90));
    ELSE
        IF RD > 0 THEN
            TEXTOUT_P("NNT (harm) = 1/RD =", G1, 10, y, 2, RGB(0,0,0));
            TEXTOUT_P(es_FmtNum(NNT, 1), G1, 180, y, 2, RGB(255,0,0));
            y := y + 16;
            TEXTOUT_P("Interpretation: For every " + STRING(CEILING(NNT),1,0) + " exposed,", G1, 10, y, 1, RGB(90,90,90));
            y := y + 12;
            TEXTOUT_P("1 additional case occurs due to exposure", G1, 10, y, 1, RGB(90,90,90));
        ELSE
            IF RD < 0 THEN
                TEXTOUT_P("NNT (benefit) = 1/|RD| =", G1, 10, y, 2, RGB(0,0,0));
                TEXTOUT_P(es_FmtNum(NNT, 1), G1, 210, y, 2, RGB(0,140,60));
                y := y + 16;
                TEXTOUT_P("Interpretation: Treat " + STRING(CEILING(NNT),1,0) + " to prevent", G1, 10, y, 1, RGB(90,90,90));
                y := y + 12;
                TEXTOUT_P("1 case", G1, 10, y, 1, RGB(90,90,90));
            ELSE
                TEXTOUT_P("NNT: undefined (RD = 0)", G1, 10, y, 2, RGB(90,90,90));
            END;
        END;
    END;
    y := y + 26;
"""),
    # es_NNTIcons: no icon array below |RD| = 0.000001; the page says why
    ("""        RETURN 0;
    END;
    niM := CEILING(niNNT);
""", """        RETURN 0;
    END;
    // v1.7d (E7): |RD| below 0.000001 gives an NNT above 1,000,000: no
    // icon array can show it, and from 1E12 on STRING printed it in
    // scientific form (1 999999 1 1000000 drew "NNT = 1/< 0.000001 =
    // 1.00E12, round up: 1E12" and "Expose 1E12 (blue)").  The page
    // says so instead and draws no cells, as it does for RD = 0.
    IF ABS(niRD) < 0.000001 THEN
        TEXTOUT_P("NNT > 1,000,000 (RD near 0: no meaningful NNT).", G1, 12, 44, 1, #000000h, 296);
        TEXTOUT_P("The two risks differ by less than 0.000001, so", G1, 12, 58, 1, #000000h, 296);
        TEXTOUT_P("no icon array is drawn.", G1, 12, 72, 1, #000000h, 296);
        es_DrawFooter(1);
        RETURN 0;
    END;
    niM := CEILING(niNNT);
"""),
]
E7_ROUTINES = ['es_Module_RiskAnalysis', 'es_Risk_Page3', 'es_NNTIcons']


def _undo_e7(src):
    """v1.7d as it stood before E7: each E7 edit undone (new -> old); each must occur exactly once"""
    for o, n in E7_EDITS:
        assert src.count(n) == 1, n[:60]
        src = src.replace(n, o)
    return src


# ============================================================================ I (1.7d)
V17C_VER = 'v1.7c'


def _pair17d(script, cas='fail', pre=None):
    """the same scripted session on v1.7d (PPL) and on v1.7c"""
    hn, en = _run_quiet(PPL, script, cas, pre)
    ho, eo = _run_quiet(V17C, script, cas, pre)
    return hn, en, ho, eo


def _ptexts(h, title):
    return [[t.text for t in sorted(p.texts, key=lambda t: (t.y, t.x))] for p in h.pages if p.lines() and p.lines()[0] == title]


def _s_m2only(t):
    def f(h):
        h.choose(2); grid(h, t); h.choose(8)
    return f


def _s_m1rd(t):
    def f(h):
        h.choose(1); grid(h, t)
        h.press('Left', 'Left', 'Left')                 # page 1 -> 7 -> 6 -> 5 (association measures)
        h.press('Esc'); h.choose(8)
    return f


def _s_m6edge(k, v):
    def f(h):
        h.choose(6); h.choose(k); h.answer(v); h.choose(8)
    return f


def _w7(h):
    """the review's width measure: font 1 at 5.5 px, font 2 at 7, font 3 at 9.5 (no clip width given)"""
    bad = []
    for p in h.pages:
        for t in p.texts:
            px = {1: 5.5, 2: 7.0, 3: 9.5, 4: 11, 5: 14}.get(int(t.font or 1), 6)
            if t.x + len(t.text) * px > 320 and not t.width:
                bad.append('%r f%s x%d: %d px' % (t.text, t.font, t.x, t.x + len(t.text) * px))
    return bad


def part_i():
    print('\n' + '=' * 78)
    print('I. 1.7d: E1, E2, E3, E4, E6, E7, E8, E9, E10, E11 (fleet review, 19 Oct 2026), v1.7d against v1.7c, harness v3e')
    print('=' * 78)

    # ---- I1 (E1) the four sample-size forms refuse alpha and power outside (0, 1) before any NORMALD_ICDF
    print('\nI1. E1: alpha and power outside (0, 1) in the four sample-size forms')
    EDGES = [(1, [0.5, 0.3, 0, 0.8], 'α must be'), (1, [0.5, 0.3, 0.05, 1], 'Power must be'),
             (1, [0.5, 0.3, 0.05, 0], 'Power must be'), (1, [0.5, 0.3, 2, 0.8], 'α must be'),
             (1, [0.5, 0.3, -0.05, 0.8], 'α must be'), (1, [0.5, 0.3, 0.05, 1.5], 'Power must be'),
             (2, [1, 2, 0, 0.8], 'α must be'), (2, [1, 2, 0.05, 1], 'Power must be'), (3, [0.5, 0.05, 0], 'α must be'),
             (3, [0.5, 0.05, 2], 'α must be'), (4, [10, 2, 0], 'α must be'), (4, [10, 2, 2.5], 'α must be'),
             (2, [1, 2, 1, 0.8], 'α must be'), (2, [1, 2, 0.05, -0.2], 'Power must be')]
    for k, v, want in EDGES:
        hn = Harness(PPL, strict=True, cas='fail', on_unverified='raise')
        _s_m6edge(k, v)(hn)
        try:
            hn.call('EpiStats'); en = None
        except Exception as e:
            en = '%s: %s' % (type(e).__name__, e)
        ho = Harness(V17C, strict=True, cas='fail', on_unverified='raise')
        _s_m6edge(k, v)(ho)
        try:
            ho.call('EpiStats'); eo = None
        except Exception as e:
            eo = '%s: %s' % (type(e).__name__, e)
        msg = [' '.join(m.lines) for m in hn.msgboxes]
        icdf = [c for c in hn.stat_calls if c[0] == 'NORMALD_ICDF']
        print('    option %d %s: v1.7c %s; v1.7d %s %s' % (k, v, (eo or 'ran')[:70], en or 'refused', msg))
        # v1.7c either sent NORMALD_ICDF a p outside (0, 1), or (alpha = 1: p = 0.5, z = 0) drew a page with a
        # meaningless n; either way it did not refuse
        old_page = any(p.lines() and p.lines()[0].startswith('SAMPLE SIZE') for p in ho.pages)
        check(en is None and len(msg) == 1 and msg[0].startswith(want) and not icdf
              and not any(p.lines() and p.lines()[0].startswith('SAMPLE SIZE') for p in hn.pages)
              and ((eo is not None and 'NORMALD_ICDF' in eo) or old_page) and not ho.msgboxes,
              '1.7d (E1): option %d %s -- v1.7d refuses it ("%s ...") before any NORMALD_ICDF, no page; v1.7c %s'
              % (k, v, want, 'reached NORMALD_ICDF with p outside (0, 1)' if eo and 'NORMALD_ICDF' in eo
                 else 'drew a page from z_alpha/2 = 0'))
    # inside (0, 1) nothing changed: the same pages, the same n, on both versions
    same = []
    for k, v in ((1, [0.5, 0.3, 0.05, 0.8]), (1, [0.5, 0.3, 0.999999, 0.000001]), (2, [1, 2, 0.01, 0.9]),
                 (3, [0.5, 0.05, 0.05]), (4, [10, 2, 0.1]), (1, [0.5, 0.3, 0.05, 0.5001])):
        def sc(h, k=k, v=v):
            h.choose(6); h.choose(k); h.answer(v); h.press('Esc'); h.choose(8)
        hn, en, ho, eo = _pair17d(sc)
        same.append(en is None and eo is None and _alltx(hn) == _alltx(ho) and not hn.msgboxes)
    check(all(same), '1.7d (E1): six forms with alpha and power inside (0, 1), the extremes 0.999999 and 0.000001 among '
          'them, give the same pages as v1.7c, with no message')

    # ---- I2 (E2) Risk Analysis refuses an empty row; every other table is unchanged
    print('\nI2. E2: an empty row in Risk Analysis')
    for t in ([0, 0, 5, 5], [5, 5, 0, 0], [0, 0, 0, 7], [3, 0, 0, 0], [0, 0, 1, 1999]):
        def pre(h):
            h.globals_['EP_RD'] = 0.123; h.globals_['EP_table'] = [9.0, 9.0, 9.0, 9.0]
        hn, en, ho, eo = _pair17d(_s_m2only(t), pre=pre)
        ho2, eo2 = _run_quiet(V17C, _s_m2(t), 'fail', pre)
        msg = [' '.join(m.lines) for m in hn.msgboxes]
        p1o = _ptexts(ho2, 'RISK ESTIMATES')
        print('    %s: v1.7c page 1 %s; v1.7d %s' % (t, [x for x in (p1o[0] if p1o else []) if '%' in x][:3], msg or en))
        check(en is None and msg == ['A risk needs people in both rows: one row of the table is empty.']
              and not _ptexts(hn, 'RISK ESTIMATES') and hn.globals_['EP_RD'] == 0.123
              and list(hn.globals_['EP_table']) == [9.0, 9.0, 9.0, 9.0]
              and eo2 is None and bool(p1o) and '0.0%' in p1o[0],
              '1.7d (E2): %s -- v1.7d refuses the table with the message and sets no EP_* result; v1.7c printed a risk '
              'of 0.0%% for the empty row' % (t,))
    diffs = []
    for t in ([40, 60, 20, 80], [1, 0, 1, 0], [0, 1, 0, 1], [1, 299, 0, 300], [10, 10, 10, 10], [100, 0, 1, 99]):
        hn, en, ho, eo = _pair17d(_s_m2(t))
        if en or eo or _alltx(hn) != _alltx(ho):
            diffs.append(t)
    check(not diffs, '1.7d (E2): six tables with people in both rows (zero cells among them) -- all five pages as v1.7c %s'
          % (diffs or ''))

    # ---- I3 (E3) Sensitivity & Specificity with an empty column
    print('\nI3. E3: an empty column in Sensitivity & Specificity')
    for t, c1z in (([0, 5, 0, 30], 1), ([12, 0, 8, 0], 0), ([1, 0, 0, 0], 0), ([0, 0, 0, 1], 1), ([0, 1, 0, 0], 1),
                   ([0, 0, 1, 0], 0)):
        hn, en, ho, eo = _pair17d(_s_m3(t))
        pn, po = _ptexts(hn, 'DIAGNOSTIC ACCURACY'), _ptexts(ho, 'DIAGNOSTIC ACCURACY')
        qn, qo = _ptexts(hn, 'AGREEMENT & RISK'), _ptexts(ho, 'AGREEMENT & RISK')
        if not (pn and po and qn and qo):
            check(False, '1.7d (E3): %s pages 1 and 2 shown (%s %s)' % (t, en, eo)); continue
        a = pn[0]
        g = hn.globals_
        why = 'undef (no Disease+)' if c1z else 'undef (no Disease-)'
        se = a[a.index('Sensitivity:') + 1]; sp = a[a.index('Specificity:') + 1]
        lp = a[a.index('LR+ (positive):') + 1]; ln_ = a[a.index('LR- (negative):') + 1]
        fpr = a[a.index('FPR (α):') + 1]; fnr = a[a.index('FNR (β):') + 1]
        yo = qn[0][qn[0].index("Youden's J Index:") + 1]
        po0 = po[0]
        print('    %s: v1.7c sens %r spec %r LR+ %r LR- %r FNR %r FPR %r Youden %r' % (
            t, po0[po0.index('Sensitivity:') + 1], po0[po0.index('Specificity:') + 1], po0[po0.index('LR+ (positive):') + 1],
            po0[po0.index('LR- (negative):') + 1], po0[po0.index('FNR (β):') + 1], po0[po0.index('FPR (α):') + 1],
            qo[0][qo[0].index("Youden's J Index:") + 1]))
        print('    %s  v1.7d sens %r spec %r LR+ %r LR- %r FNR %r FPR %r Youden %r' % (' ' * len(str(t)), se, sp, lp, ln_, fnr, fpr, yo))
        ok = (en is None and eo is None and lp == why and ln_ == why and yo == 'undef'
              and g['EP_LRpos'] == 999 and g['EP_LRneg'] == 999 and g['EP_youden'] == 999)
        ok = ok and ((se == why and fnr == 'undef') if c1z else (sp == why and fpr == 'undef'))
        old_bad = po0[po0.index('Sensitivity:' if c1z else 'Specificity:') + 1] == '0.0%'
        check(ok and old_bad, '1.7d (E3): %s -- %s reads %r, both LRs %r, %s "undef", Youden\'s J "undef"; EP_LRpos, '
              'EP_LRneg, EP_youden = 999 (v1.7c: 0.0%%)' % (t, 'sensitivity' if c1z else 'specificity', why, why,
                                                             'FNR' if c1z else 'FPR'))
        # pages 3 to 6 are v1.7c's
        rest_same = all(_ptexts(hn, ti) == _ptexts(ho, ti) for ti in ('TABLE SUMMARY', 'PPV VS PREVALENCE', 'ROC POINT', 'EXACT vs WILSON'))
        check(rest_same, '1.7d (E3): %s -- pages 3, 4, 5 and 6 are v1.7c\'s' % (t,))
    diffs = []
    for t in ([12, 5, 8, 30], [12, 0, 8, 30], [20, 0, 0, 20], [0, 20, 20, 0], [1, 1, 1, 1], [999, 1, 1, 999], [5, 5, 5, 5]):
        hn, en, ho, eo = _pair17d(_s_m3(t))
        if en or eo or _alltx(hn) != _alltx(ho) or hn.globals_['EP_youden'] != ho.globals_['EP_youden']:
            diffs.append(t)
    check(not diffs, '1.7d (E3): seven tables with both columns filled -- all six pages and EP_youden as v1.7c %s' % (diffs or ''))

    # ---- I4 (E4) module 1, RD with an empty row
    print('\nI4. E4: the 2x2 page\'s RD with an empty row')
    for t in ([0, 0, 0, 5], [5, 0, 0, 0], [0, 5, 0, 0], [0, 0, 5, 0], [1, 1999, 0, 0], [0, 0, 1, 1999]):
        hn, en, ho, eo = _pair17d(_s_m1rd(t))
        rn = [x for p in _ptexts(hn, 'THREE READINGS') for x in p if x.startswith('RD = Re - Ru')]
        ro = [x for p in _ptexts(ho, 'THREE READINGS') for x in p if x.startswith('RD = Re - Ru')]
        an, ao = _ptexts(hn, 'ASSOCIATION MEASURES'), _ptexts(ho, 'ASSOCIATION MEASURES')
        i = an[0].index('Risk Difference (RD):') if an else 0
        print('    %s: v1.7c %r | page 5 %r; v1.7d %r | page 5 %r' % (t, ro[:1], ao[0][i + 1:i + 4] if ao else None,
                                                                   rn[:1], an[0][i + 1:i + 4] if an else None))
        g = hn.globals_
        check(en is None and rn == ['RD = Re - Ru = undef   '] and bool(an) and an[0][i + 1] == 'undef'
              and an[0][i + 3] == '95% CI: ' and g['EP_RD'] == 999 and list(g['EP_RD_CI']) == [0, 0]
              and ro == ['RD = Re - Ru = 0.0%   (-100.0-100.0%)'],
              '1.7d (E4): %s -- the cohort tab reads "RD = Re - Ru = undef", page 5 "undef" with no CI; EP_RD = 999, '
              'EP_RD_CI = {0, 0} (v1.7c: "0.0%%   (-100.0-100.0%%)")' % (t,))
        # nothing else on the pages changed
        tn, to = _alltx(hn), _alltx(ho)
        odd = [(o, n) for o, n in zip(to, tn) if o != n and not ('RD' in o and 'undef' in n)
               and not (o == '0.0%' and n == 'undef') and not (o.startswith('95% CI: (-100') and n == '95% CI: ')]
        check(len(tn) == len(to) and not odd, '1.7d (E4): %s -- every other text on the pages is v1.7c\'s %s' % (t, odd[:2]))
    hn, en, ho, eo = _pair17d(_m1all([12, 5, 8, 30]))
    check(en is None and _alltx(hn) == _alltx(ho), '1.7d (E4): module 1 on 12 5 8 30, every page, as v1.7c')

    # ---- I5 (E8) McNemar, the M-H chi-square and Breslow-Day as lower tails
    print('\nI5. E8: McNemar, M-H chi-square, Breslow-Day p as lower tails')
    from statsmodels.stats.contingency_tables import StratifiedTable
    hn = Harness(PPL, strict=True, cas='fail'); ho = Harness(V17C, strict=True, cas='fail')
    worst = 0; rows = []
    for b, c in ((5, 8), (10, 2), (1, 0), (3, 3), (40, 0), (100, 3), (200, 0), (1000, 10)):
        vn = hn.call('es_McNemar', float(b), float(c)); vo = ho.call('es_McNemar', float(b), float(c))
        w = stats.chi2.sf(vn[0], 1)
        worst = max(worst, abs(vn[1] - w) / max(w, 1e-300))
        rows.append((b, c, vn[0], vo[1], vn[1], w))
    for b, c, x, po_, pn_, w in rows:
        print('    McNemar b %4d c %3d: chi-square %8.3f  v1.7c p %-10.4g v1.7d p %-12.6g chi2.sf %.6g' % (b, c, x, po_, pn_, w))
    check(worst < 1e-12 and rows[6][3] == 0 and rows[6][4] > 1e-45,
          '1.7d (E8): es_McNemar\'s p = chi2.sf(x, 1) to %.1e relative at every b, c; b = 200, c = 0 (chi-square 198) '
          'gives %.3g, where v1.7c gave exactly 0' % (worst, rows[6][4]))
    worst = 0; big = []
    # (chi-squares of about 140 and 90: tails near 1E-32 and 1E-21, far below 1 - CDF's last digit and inside a
    # double's range; at 1,900 the tail is below 1E-308 and the harness's doubles give 0 either way)
    for S in ([(12, 4, 30, 50), (25, 10, 20, 60)], [(60, 10, 10, 60), (60, 10, 10, 60)],
              [(60, 10, 10, 60), (10, 60, 60, 10)], [(10, 2, 2, 10), (2, 10, 10, 2)], [(5, 5, 5, 5), (5, 5, 6, 5)]):
        flat = [float(x) for s in S for x in s]
        vn = hn.call('es_MHCalc', 1.0, flat, [0.0, 0.0]); vo = ho.call('es_MHCalc', 1.0, flat, [0.0, 0.0])
        t = StratifiedTable([np.array([[a, b], [c, d]], float) for a, b, c, d in S])
        for i, nm in ((7, 'M-H p'), (9, 'M-H p (corr.)'), (11, 'Breslow-Day p')):
            x = vn[i - 1]
            if x < 0:
                continue
            w = stats.chi2.sf(x, 1)
            worst = max(worst, abs(vn[i] - w) / max(w, 1e-300))
            if vo[i] == 0 and vn[i] > 0:
                big.append((S[0], nm, x, vn[i]))
        bd = t.test_equal_odds(adjust=False)
        if np.isfinite(bd.pvalue) and bd.pvalue > 1e-300:
            worst = max(worst, abs(vn[11] - bd.pvalue) / bd.pvalue)
        print('    strata %s: M-H chi-square %.3f p %.4g (v1.7c %.4g); BD %.3f p %.4g (v1.7c %.4g)'
              % (S, vn[6], vn[7], vo[7], vn[10], vn[11], vo[11]))
    check(worst < 1e-12 and len(big) >= 3,
          '1.7d (E8): the M-H p (plain and corrected) and the Breslow-Day p = chi2.sf(x, 1) (= statsmodels test_equal_odds) '
          'to %.1e; %d of them were exactly 0 in v1.7c (%s)' % (worst, len(big), ', '.join('%s %.0f' % (b[1], b[2]) for b in big[:3])))
    # end to end: EP_MCN_P, EP_MH_P, EP_BD_P keep their digits
    def sc_mcn(h):
        h.choose(1); grid(h, [10, 200, 0, 10]); h.press('Esc'); h.choose(8)
    hn2, en2, ho2, eo2 = _pair17d(sc_mcn)
    w = stats.chi2.sf(199 ** 2 / 200, 1)
    check(en2 is None and abs(hn2.globals_['EP_MCN_P'] - w) < 1e-12 * w and ho2.globals_['EP_MCN_P'] == 0,
          '1.7d (E8): module 1, 10 200 0 10 -- EP_MCN_P = %.4g = chi2.sf (v1.7c: 0)' % hn2.globals_['EP_MCN_P'])
    hn2, en2, ho2, eo2 = _pair17d(_s_m5(1, [60, 10, 10, 60], [10, 60, 60, 10]))
    g, go = hn2.globals_, ho2.globals_
    print('    module 5 OR, 60 10 10 60 / 10 60 60 10: EP_BD_P v1.7d %.4g (v1.7c %r); EP_MH_P %.4g (v1.7c %r)'
          % (g['EP_BD_P'], go['EP_BD_P'], g['EP_MH_P'], go['EP_MH_P']))
    hn3, en3, ho3, eo3 = _pair17d(_s_m5(1, [60, 10, 10, 60], [60, 10, 10, 60]))
    print('    module 5 OR, 60 10 10 60 twice: EP_MH_P v1.7d %.4g (v1.7c %r)' % (hn3.globals_['EP_MH_P'], ho3.globals_['EP_MH_P']))
    check(en2 is None and en3 is None and g['EP_BD_P'] > 0 and go['EP_BD_P'] == 0 and hn3.globals_['EP_MH_P'] > 0
          and ho3.globals_['EP_MH_P'] == 0 and _alltx(hn2) == _alltx(ho2) and _alltx(hn3) == _alltx(ho3),
          '1.7d (E8): module 5 end to end -- EP_BD_P and EP_MH_P keep their digits where v1.7c\'s were 0; the pages are '
          'v1.7c\'s ("p < 0.0001" either way)')
    # the Prime's 12 digits: 1 - CHISQUARE_CDF is 0 from about 52, the lower tail is not
    _C0 = ppl_run_v3d._StatFns.CHISQUARE_CDF; _N0 = ppl_run_v3d._StatFns.NORMALD_CDF

    def _c12(self, a):
        v = _C0(self, a)
        return float('%.12g' % v) if v == v else v

    def _n12(self, a):
        v = _N0(self, a)
        return float('%.12g' % v) if v == v else v
    ppl_run_v3d._StatFns.CHISQUARE_CDF, ppl_run_v3d._StatFns.NORMALD_CDF = _c12, _n12
    try:
        hn = Harness(PPL, strict=True, cas='fail'); ho = Harness(V17C, strict=True, cas='fail')
        r12 = [(b, c, ho.call('es_McNemar', float(b), float(c))[1], hn.call('es_McNemar', float(b), float(c))[1])
               for b, c in ((60, 0), (70, 1), (100, 3))]
    finally:
        ppl_run_v3d._StatFns.CHISQUARE_CDF, ppl_run_v3d._StatFns.NORMALD_CDF = _C0, _N0
    print('    the Prime\'s 12 digits (CDFs rounded): %s' % ', '.join('b %d c %d: v1.7c %.3g, v1.7d %.3g' % r for r in r12))
    check(all(r[2] == 0 and r[3] > 0 for r in r12),
          '1.7d (E8): with the CDFs rounded to 12 digits, McNemar chi-squares of 58, 65 and 89 give p = 0 in v1.7c and a '
          'positive p in v1.7d')

    # ---- I6 (E6) and I7 (E9) Incidence Rates
    print('\nI6, I7. E6 and E9: Incidence Rates page 3, fractional cases')
    for v in ([1, 1, 1000000, 1000000], [1, 3, 1e7, 2e6]):
        hn, en, ho, eo = _pair17d(_m4(v))
        p3n, p3o = _ptexts(hn, 'CLINICAL MEASURES'), _ptexts(ho, 'CLINICAL MEASURES')
        wn, wo = _w7(hn), _w7(ho)
        print('    %s: v1.7c %s; v1.7d %s; past x 320 (7 px a character): v1.7c %d, v1.7d %d'
              % (v, [x for x in p3o[0] if 'time units' in x][:2], p3n[0][2:5], len(wo), len(wn)))
        check(en is None and not wn and bool(wo) and p3n[0][2] == '─── Mean Waiting Times (time units) ───'
              and not any(x.endswith(' time units') for x in p3n[0]),
              '1.7d (E6): module 4 %s -- page 3 names the unit once, in the heading, and nothing runs past x 320 '
              '(v1.7c: "... time units" from x 200, %d texts past the edge)' % (v, len(wo)))
        # the numbers are v1.7c's, without the unit
        nums_n = [t.text for p in hn.pages if p.lines() and p.lines()[0] == 'CLINICAL MEASURES'
                  for t in sorted(p.texts, key=lambda t: t.y) if t.x == 200][:3]
        nums_o = [x.replace(' time units', '') for x in p3o[0] if x.endswith(' time units')]
        check(nums_n == nums_o, '1.7d (E6): the three waiting times are v1.7c\'s numbers: %s' % nums_n)
    hn, en, ho, eo = _pair17d(_m4([2.5, 8, 1200, 1500]))
    p1n, p1o = _ptexts(hn, 'INCIDENCE RATES'), _ptexts(ho, 'INCIDENCE RATES')
    print('    2.5 cases: v1.7c %r; v1.7d %r, message %s' % ([x for x in p1o[0] if 'cases /' in x][0],
                                                          [x for x in p1n[0] if 'cases /' in x][0], [m.lines for m in hn.msgboxes]))
    check(en is None and [' '.join(m.lines) for m in hn.msgboxes] == ['Cases are whole numbers: the values were rounded.']
          and '3 cases / 1200 person-time' in p1n[0] and abs(hn.globals_['EP_IR_exp'] - 3 / 1200) < 1e-15
          and '2.5 cases / 1200 person-time' in p1o[0],
          '1.7d (E9): module 4 with 2.5 cases -- rounded to 3 with a message (v1.7c: "2.5 cases" as typed)')
    hn, en, ho, eo = _pair17d(_m4([15, 8, 1200.5, 1500]))
    tn, to = _alltx(hn), _alltx(ho)
    odd = [(o, n) for o, n in zip(to, tn) if o != n and not (o.endswith(' time units') and o.replace(' time units', '') == n)
           and not (o == '─── Average Waiting Times ───' and n == '─── Mean Waiting Times (time units) ───')]
    check(en is None and not hn.msgboxes and len(tn) == len(to) and not odd,
          '1.7d (E9): whole cases with a fractional person-time (15, 8, 1200.5, 1500) -- no message; every text is '
          'v1.7c\'s apart from page 3\'s unit (E6) %s' % (odd[:2] or ''))

    # ---- I8 (E11) es_Cnt
    print('\nI8. E11: es_Cnt')
    hn = Harness(PPL, strict=True, cas='fail'); ho = Harness(V17C, strict=True, cas='fail')
    want = [(0.05, '0.0500'), (0.0123, '0.0123'), (1e-7, '< 0.000001'), (12.5, '12.5'), (3.0, '3'), (0.5, '0.5'),
            (1234.5, '1234.5'), (0.0, '0'), (2000.0, '2000')]
    got = [(x, hn.call('es_Cnt', x)) for x, _ in want]
    old = [(x, ho.call('es_Cnt', x)) for x, _ in want[:2]]
    print('    v1.7d %s; v1.7c %s' % (got, old))
    check([g_ for _, g_ in got] == [w for _, w in want] and all(SCI_E in o for _, o in old),
          '1.7d (E11): es_Cnt -- 0.05 -> "0.0500", 0.0123 -> "0.0123" (v1.7c: the scientific form), a Haldane half and '
          'every whole count as before')
    hn, en, ho, eo = _pair17d(_s_m5(3, [1, 0.05, 2, 0.08], [3, 0.5, 1, 0.25]))
    on = sorted(set(t for _, t in ho.sci_where))
    check(en is None and not hn.sci_strings and _has(hn, '0.0500') and _has(hn, '0.0800') and bool(on),
          '1.7d (E11): the stratified rates grid with person-times 0.05 and 0.08 -- v1.7d prints "0.0500", "0.0800" '
          '(v1.7c printed %s)' % on[:2])

    # ---- I9 (E10) and I10 the code
    print('\nI9, I10. E10, the routine diff and the code')
    src_c, src_d = open(V17C, encoding='utf-8').read(), open(PPL, encoding='utf-8').read()
    vl = src_d.split('\n')
    check(vl[2] == '// EPISTATS - v1.7d' and src_d.count('"EpiStats v1.7d ══════════"') == 1 and '{"EpiStats v1.7d",' in src_d
          and '// EpiStats v1.7d - Comprehensive Biostatistics & Epidemiology Calculator' in src_d
          and '// What changed in v1.7d (19 Oct 2026)' in src_d
          and not [l for l in vl if re.search(r'v1\.7[abc]\b', _strip_comment(l))],
          '1.7d (E10): v1.7d in the banner, the comment banner (v1.7c\'s line 304 said v1.7b), the menu title and About; '
          'a "What changed in v1.7d" paragraph; no code line names an older version')
    check('// DISCLAIMER: a teaching and demonstration aid. Not validated for' in src_d
          and '//   forensic, clinical or legal use; do not rely on its results for' in src_d,
          '1.7d: Roger\'s DISCLAIMER line (19 Oct 2026) sits beside the distribution terms in the header (a comment)')
    check(B_CQ[0] == 1, '1.7d (E10, review item 22): part B compared the shared Clopper-Pearson routines with CICatcher '
          'beta 2b in out/ (the v1.7c script named the superseded beta 2a and stopped there)')

    def _routines(txt):
        lines = txt.split('\n'); out = {}; i = 0
        while i < len(lines):
            m = re.match(r'^(?:EXPORT\s+)?([A-Za-z]\w*)\(.*\)\s*$', lines[i])
            if m and i + 1 < len(lines) and lines[i + 1].strip() == 'BEGIN':
                j = i + 1
                while not lines[j].startswith('END;'):
                    j += 1
                out[m.group(1)] = '\n'.join(lines[i:j + 1]); i = j
            i += 1
        return out
    R0, R1 = _routines(src_c), _routines(src_d)
    changed = sorted(n for n in set(R0) & set(R1) if R0[n] != R1[n])
    want = sorted(['EpiStats', 'es_McNemar', 'es_Cnt', 'es_Module_Table2x2', 'es_Module_RiskAnalysis', 'es_Module_SensSpec',
                   'es_SS_Page1', 'es_Module_IncidenceRate', 'es_IR_Page3', 'es_MHCalc', 'es_SS_TwoProportions',
                   'es_SS_TwoMeans', 'es_SS_OneProportion', 'es_SS_OneMean', 'es_Help_About', 'es_Help_Variables',
                   'es_Risk_Page3', 'es_NNTIcons'])                    # the last two: E7
    print('    %d routines; changed (%d): %s' % (len(R1), len(changed), ', '.join(changed)))
    check(changed == want and set(R0) == set(R1),
          '1.7d: the routines that differ from v1.7c are exactly the %d the fixes name (EpiStats and es_Help_About for '
          'the version only); the other %d are byte-identical, none added or removed' % (len(want), len(R1) - len(want)))
    check(R0['EpiStats'].replace('v1.7c', 'v1.7d') == R1['EpiStats'] and R0['es_Help_About'].replace('v1.7c', 'v1.7d') == R1['es_Help_About'],
          '1.7d: EpiStats and es_Help_About differ from v1.7c only in the version string')
    check(_outside(src_c, changed) == _outside(src_d, changed),
          '1.7d: outside those routines only comments differ (the header; the EXPORT list and file-level LOCALs unchanged)')
    cd = [_strip_comment(l) for l in vl]
    check(not any(re.search(r'1\s*-\s*CHISQUARE_CDF', l) for l in cd) and sum('2 * NORMALD_CDF(0, 1, -(' in l for l in cd) == 7,
          '1.7d (E8): no 1 - CHISQUARE_CDF left in the code; seven chi-square p lines are lower normal tails (v1.7c\'s '
          'three, McNemar, the two M-H and Breslow-Day)')
    names = {w.strip().upper() for w in open('/home/claude/work/gate_f19/HP_Prime_Builtin_Names.txt', encoding='utf-8')
             if w.strip() and not w.startswith('#')}
    newn = ['sOK1', 'sOK2', 's1U', 's1S']
    check(not [x for x in newn if x.upper() in names], '1.7d: the new names %s are not built-ins (ignoring case)' % newn)
    dep, badc = 0, []
    for n_, l in enumerate(vl, 1):
        q = False
        for j, ch in enumerate(l):
            if ch == '"':
                q = not q
            elif not q:
                if l[j:j + 2] == '//':
                    if dep:
                        badc.append(n_)
                    break
                dep += (ch in '({[') - (ch in ')}]')
    check(not badc, '1.7d: no // comment inside an open bracket %s' % (badc[:5] or ''))
    lm = max(len(m.split(',')) for m in re.findall(r'^\s*LOCAL ([^;(]*);', '\n'.join(cd), re.M))
    check(sum('INSTRING(' in l for l in cd) == sum('INSTRING(' in _strip_comment(l) for l in src_c.split('\n')) and lm <= 6,
          '1.7d: INSTRING as in v1.7c; every LOCAL line holds at most 6 names (largest %d)' % lm)
    # the help page that names the sentinel
    def sc_var(h):
        h.choose(7); h.choose(8); h.press('Enter'); h.choose(16); h.choose(8)
    hn, en, ho, eo = _pair17d(sc_var)
    vp = _ptexts(hn, 'STORED RESULT VARIABLES')
    check(en is None and bool(vp) and '999 = undefined (EP_RR, EP_RD, EP_LRpos ...)' in vp[0] and len(vp[0]) == len(_ptexts(ho, 'STORED RESULT VARIABLES')[0]) + 1
          and not _w7(hn), '1.7d (E4): Help > Variables names the 999 sentinel on its formerly blank line, within the width')

    # ---- I11 (E7) the NNT when |RD| < 0.000001 (added to v1.7d at the coordinator's request, 19 Oct 2026)
    print('\nI11. E7: Risk Analysis with |RD| below 0.000001 (an NNT above 1,000,000)')
    for t in ([1, 999999, 1, 1000000], [1, 1000000, 1, 999999], [1, 99999, 1, 100000], [1, 200000, 1, 250000]):
        hn, en, ho, eo = _pair17d(_s_m2(t))
        rd = t[0] / (t[0] + t[1]) - t[2] / (t[2] + t[3])
        p3, p5 = _ptexts(hn, 'CLINICAL IMPACT'), _ptexts(hn, 'NNT: ICON ARRAY')
        o3, o5 = _ptexts(ho, 'CLINICAL IMPACT'), _ptexts(ho, 'NNT: ICON ARRAY')
        cells = lambda h: [s for p in h.pages if p.lines() and p.lines()[0] == 'NNT: ICON ARRAY'
                           for s in p.shapes if s.cmd == 'RECT_P' and s.args[2] - s.args[0] == 11]
        side = 'NNT (harm) = 1/RD' if rd > 0 else 'NNT (benefit) = 1/|RD|'
        old_sci = sorted(set(x for _, x in ho.sci_where))
        print('    %s RD %.6g: v1.7c page 5 %s, EP_NNT %.6g, %d cells, scientific %s; v1.7d page 3 %s, page 5 %s, EP_NNT %s'
              % (t, rd, [x for x in (o5[0] if o5 else []) if x.startswith(('NNT =', 'Expose', 'Treat'))][:1],
                 ho.globals_['EP_NNT'], len(cells(ho)), old_sci,
                 [x for x in (p3[0] if p3 else []) if '1,000,000' in x or 'meaningful' in x],
                 [x for x in (p5[0] if p5 else []) if '1,000,000' in x], hn.globals_['EP_NNT']))
        check(en is None and eo is None and bool(p3) and bool(p5)
              and side in p3[0] and '> 1,000,000' in p3[0] and 'RD near 0 (|RD| < 0.000001): no meaningful NNT;' in p3[0]
              and not [x for x in p3[0] if x.startswith(('Interpretation', 'NNT (harm) = 1/RD =', 'NNT (benefit) = 1/|RD| ='))]
              and p5[0][2:5] == ['NNT > 1,000,000 (RD near 0: no meaningful NNT).',
                                 'The two risks differ by less than 0.000001, so', 'no icon array is drawn.']
              and not cells(hn) and hn.globals_['EP_NNT'] == 999 and abs(hn.globals_['EP_RD'] - rd) <= 1e-6 * abs(rd)
              and not hn.sci_where and not _w7(hn) and not [x for x in _alltx(hn) if re.search(r'=\s*[<>]', x)]
              and len(cells(ho)) == 100 and abs(ho.globals_['EP_NNT'] * abs(rd) - 1) < 1e-6,
              '1.7d (E7): %s (RD %.6g) -- page 3 "%s   > 1,000,000" and "no meaningful NNT", page 5 says the same and '
              'draws no cells, EP_NNT = 999 (EP_RD keeps %.6g), no scientific form, within the width; v1.7c drew 100 '
              'cells for an NNT of %.4g%s' % (t, rd, side, rd, ho.globals_['EP_NNT'],
                                              (', in scientific form %s' % old_sci) if old_sci else ''))
    # just above the line, |RD| = 1.000016E-6 (NNT 999,984): every page as v1.7c
    t = [1, 199999, 1, 250000]
    hn, en, ho, eo = _pair17d(_s_m2(t))
    check(en is None and eo is None and _alltx(hn) == _alltx(ho) and hn.globals_['EP_NNT'] == ho.globals_['EP_NNT']
          and 999980 < hn.globals_['EP_NNT'] < 999990 and not hn.sci_where,
          '1.7d (E7): %s, |RD| = 1.000016E-6 just above the line -- all five pages and EP_NNT (%.2f) as v1.7c' % (t, hn.globals_['EP_NNT']))
    # (I2 above: six ordinary tables, all five pages as v1.7c.)
    # the review's own E7 check -- its B3 steps and its scan_texts on 1 999999 1 1000000 -- on v1.7c, on v1.7d as it
    # stood before E7 (rebuilt in memory: the three E7 edits undone), and on v1.7d
    import hashlib
    pre = _undo_e7(src_d)
    Rp = _routines(pre)
    hp = hashlib.sha256('\n'.join(Rp[k] for k in sorted(Rp)).encode()).hexdigest()
    check(hp == PRE_E7_ROUTINES_SHA256 and sorted(n for n in R1 if R1[n] != Rp.get(n)) == sorted(E7_ROUTINES)
          and all(Rp[n] == R0[n] for n in ('es_Risk_Page3', 'es_NNTIcons')),
          '1.7d (E7): undoing the three E7 edits gives back the routines of v1.7d as it stood before E7 (sha256 %s...), '
          'whose es_Risk_Page3 and es_NNTIcons are v1.7c\'s; E7 changed exactly %s' % (hp[:12], ', '.join(E7_ROUTINES)))
    res = {}
    for name, h in (('v1.7c', Harness(V17C, strict=True, cas='giac', on_unverified='warn')),
                    ('v1.7d before E7', _harness_text(pre, 'EpiStats_v1.7d_before_E7 (rebuilt)')),
                    ('v1.7d', Harness(PPL, strict=True, cas='giac', on_unverified='warn'))):
        res[name] = _review_e7(h)
        print('    the review\'s E7 check on %s: %s' % (name, ('FAIL  ' + res[name][1][0][:150]) if res[name][1]
                                                       else ('error %s' % res[name][0]) if res[name][0] else 'passes'))
    check(all(res[k][0] is None for k in res) and res['v1.7c'][1] and res['v1.7d before E7'][1] and not res['v1.7d'][1]
          and all(f.startswith(E7_LABEL) for k in ('v1.7c', 'v1.7d before E7') for f in res[k][1]),
          '1.7d (E7): the review\'s E7 check ("%s ... pages") fails on v1.7c and on v1.7d before E7, and passes on v1.7d'
          % E7_LABEL[:-3])


PRE_E7_ROUTINES_SHA256 = '9f552f68186adc812e9547707d3fdc29929ce2589a3c986a16eb58dc9036f442'


def _harness_text(src, label):
    """a harness on source text (v1.7d before E7, rebuilt in memory), kept out of HARNESSES and part SCI"""
    h = Harness.__new__(Harness)
    _h_init(h, None, strict=True, cas='giac', on_unverified='warn', text=src)
    h.vpath, h.sci_where = label, []
    return h


_REV_NS = {}


def _review_ns():
    """the review's check_EpiStats.py, patched as in part REVIEW, loaded once (its helpers; main is not run)"""
    if not _REV_NS:
        import io, contextlib
        s = open(REVIEW, encoding='utf-8').read()
        for o, n in REVIEW_PATCHES:
            assert s.count(o) == 1, o[:80]
            s = s.replace(o, n)
        ns = {'__name__': 'review_check_e7', '__file__': REVIEW, '__PPL__': PPL, '__VER__': 'v1.7d', 'FP_CASES': True}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(s, REVIEW, 'exec'), ns)
        _REV_NS.update(ns)
    return _REV_NS


def _review_e7(h):
    """the review's B3 steps on 1 999999 1 1000000 (module 2, four page taps, the back tap, Esc, Exit) and its
    scan_texts on the pages shown: (run error or None, the review's failures from it)"""
    import io, contextlib
    ns = _review_ns()
    tb = (1, 999999, 1, 1000000)
    h.choose(2); ns['grid'](h, list(tb)); ns['tap_pages'](h, 4); h.tap(300, 205); h.press('Esc'); h.choose(8)
    n0 = len(ns['FAILS'])
    with contextlib.redirect_stdout(io.StringIO()):
        err = ns['run'](h, 'module 2 %s' % (tb,))
        ns['scan_texts'](h, 'B3 %s' % (tb,))
    return err, list(ns['FAILS'][n0:])


# ============================================================================ REVIEW (1.7d): the review's check_EpiStats.py
REVIEW = '/home/claude/work/review/check_EpiStats.py'
REVIEW_PATCHES = [
    # the file under test
    ("PPL = os.path.join(FLEET, 'EpiStats_v1.7c.txt')", "PPL = __PPL__"),
    # D8: the version string on screen is the new one
    ("    check(vers == ['v1.7c'], 'D8 the only version string shown on screen is v1.7c')",
     "    check(vers == [__VER__], 'D8 the only version string shown on screen is ' + __VER__)"),
    # B3 (E2): an empty row is now refused at entry, so there are no result pages to turn; the expectation is the
    # refusal (the review's own check asked for "undefined" instead of 0.0 %, -50 %, NNT 2: E2's fix is the message)
    ("        h = new(unver='warn')\n        h.choose(2); grid(h, list(tb)); tap_pages(h, 4); h.tap(300, 205); h.press('Esc'); h.choose(8)\n",
     "        h = new(unver='warn')\n"
     "        if (tb[0] + tb[1]) * (tb[2] + tb[3]) == 0:\n"
     "            h.choose(2); grid(h, list(tb)); h.choose(8)\n"
     "            err = run(h, 'module 2 %s' % (tb,))\n"
     "            check(err is None and any('one row of the table is empty' in ' '.join(m.lines) for m in h.msgboxes)\n"
     "                  and not pages(h, 'RISK ESTIMATES'),\n"
     "                  'B3 %s: an empty row is 0/0, so the module refuses the table with a message (E2): no risk, RD or NNT' % (tb,))\n"
     "            continue\n"
     "        h.choose(2); grid(h, list(tb)); tap_pages(h, 4); h.tap(300, 205); h.press('Esc'); h.choose(8)\n"),
    # B5 (E9): fractional cases are rounded, so the expected rates use the rounded counts (floor(x + 0.5): halves up)
    ("        ce, cu, pe, pu = vals\n",
     "        ce, cu, pe, pu = vals\n"
     "        if FP_CASES and (ce % 1 or cu % 1):\n"
     "            check(any('Cases are whole numbers' in ' '.join(m.lines) for m in h.msgboxes), 'B5 %s fractional cases: a message (E9)' % (vals,))\n"
     "            ce, cu = float(math.floor(ce + 0.5)), float(math.floor(cu + 0.5))\n"),
    # C5 (E1): the review's check asserted the missing guard ("reaches NORMALD_ICDF ... no guard in the PPL"); with the
    # guard the form is refused with a message and no page, so the Enter that closed the result page is not pressed
    ("        h.choose(6); h.choose(which); h.answer(vals); h.press('Enter'); h.choose(8)\n        err = run(h, 'sample size edge')\n",
     "        h.choose(6); h.choose(which); h.answer(vals); h.choose(8)\n        err = run(h, 'sample size edge')\n"),
    ("        check(err is not None and ('Unverified' in err or 'NORMALD_ICDF' in err),\n"
     "              'C5 option %d %s reaches NORMALD_ICDF with p outside (0,1): no guard in the PPL (device behaviour unknown)' % (which, vals))\n",
     "        check(err is None and any(('must be between 0 and 1' in ' '.join(m.lines)) for m in h.msgboxes)\n"
     "              and not any(c[0] == 'NORMALD_ICDF' for c in h.stat_calls),\n"
     "              'C5 option %d %s refused with a message before any NORMALD_ICDF (E1)' % (which, vals))\n"),
    # B3 (E7): with |RD| below 0.000001 (1 999999 1 1000000: |RD| about 1E-12) EP_NNT holds the 999 sentinel and page 5
    # draws no icon array, saying "NNT > 1,000,000 (RD near 0: no meaningful NNT)."; the review expected 1/|RD| and 100
    # cells.  One check for one, so the count is unchanged.
    ("            if rd != 0:\n                check(close(g['EP_NNT'], 1 / abs(rd), 1e-9),",
     "            if rd != 0 and abs(rd) < 1e-6:\n"
     "                check(g['EP_NNT'] == 999, 'B3 %s EP_NNT = 999 (undefined): |RD| < 0.000001, no meaningful NNT (E7)' % (tb,))\n"
     "            elif rd != 0:\n                check(close(g['EP_NNT'], 1 / abs(rd), 1e-9),"),
    ("            if rd != 0:\n                m = math.ceil(1 / abs(rd))\n",
     "            if rd != 0 and abs(rd) < 1e-6:\n"
     "                check(not cells and any(t.text.startswith('NNT > 1,000,000 (RD near 0') for t in nn.texts),\n"
     "                      'B3 %s icon array: none; \"NNT > 1,000,000 (RD near 0: no meaningful NNT).\" (E7)' % (tb,))\n"
     "            elif rd != 0:\n                m = math.ceil(1 / abs(rd))\n"),
]
E7_LABEL = 'B3 (1, 999999, 1, 1000000): no scientific E, no "= <" on'
REVIEW_RES = {}


def run_review(path, ver):
    import io, contextlib
    s = open(REVIEW, encoding='utf-8').read()
    for o, n in REVIEW_PATCHES:
        assert s.count(o) == 1, o[:80]
        s = s.replace(o, n)
    ns = {'__name__': 'review_check', '__file__': REVIEW, '__PPL__': path, '__VER__': ver, 'FP_CASES': True}
    buf = io.StringIO()
    n0 = len(HARNESSES)
    with contextlib.redirect_stdout(buf):
        exec(compile(s, REVIEW, 'exec'), ns)
        ns['main']()
    for h in HARNESSES[n0:]:
        h.review = True                      # the review's own runs: their scientific strings are listed apart
    return ns['NCHECK'][0], list(ns['FAILS']), buf.getvalue()


def part_review():
    print('\n' + '=' * 78)
    print('REVIEW. The review\'s check_EpiStats.py (511 checks), on v1.7d and on v1.7c, harness v3e')
    print('=' * 78)
    print('  Expectations are moved where a fix changes what is right: D8\'s version string; B3\'s empty-row tables are '
          'now refused (E2); B5\'s 2.5 cases are now rounded (E9); C5\'s twelve forms are now refused (E1: the check '
          'asserted the missing guard); B3\'s EP_NNT and icon array for 1 999999 1 1000000 (|RD| about 1E-12) are now '
          'the 999 sentinel and no cells (E7). With them the script makes 508 checks: a refused empty-row table in B3 has '
          'one check where it had three, and B5 adds the message.')
    t0 = time.time()
    n_new, f_new, out_new = run_review(PPL, 'v1.7d')
    n_old, f_old, out_old = run_review(V17C, 'v1.7d')
    REVIEW_RES['new'] = f_new
    print('  v1.7d: %d checks, %d failed' % (n_new, len(f_new)))
    for f in f_new:
        print('      FAIL  ' + f[:160])
    print('  v1.7c: %d checks, %d failed' % (n_old, len(f_old)))
    for f in f_old:
        print('      FAIL  ' + f[:160])
    print('  [%.0f s]' % (time.time() - t0))
    rv = [h for h in HARNESSES if getattr(h, 'review', False) and h.vpath == os.path.basename(PPL)]
    rs = sorted(set((r, t) for h in rv for r, t in h.sci_where))
    print('  scientific STRING results in the review\'s %d runs of v1.7d: %s' % (len(rv), rs))
    check(len(rv) >= 100 and not rs,
          '1.7d (E7): no scientific STRING result in any of the review\'s %d runs of v1.7d (before E7 the NNT page of '
          '1 999999 1 1000000 printed "1.00E12" and "1E12")' % len(rv))
    # the count: the review's 511, less two for each of B3's two empty-row tables (a refused table has one check, the
    # refusal, where the review had three: "runs five pages", "no scientific E" on its pages, and the 0/0 reading), plus
    # one for B5's new message check: 511 - 4 + 1 = 508, the same on v1.7d and v1.7c
    check(n_new == n_old == 511 - 2 * 2 + 1 and not f_new,
          '1.7d: the review\'s check passes on v1.7d, all %d checks (with the moved expectations), E7\'s among them'
          % n_new + (' %s' % f_new[:3] if f_new else ''))
    old_e = {'E4': [f for f in f_old if f.startswith('B2 (') and 'RD line should say undefined' in f],
             'E2': [f for f in f_old if f.startswith('B3 (') and 'empty row' in f],
             'E3': [f for f in f_old if f.startswith('B4 (') and 'undefined' in f],
             'E6': [f for f in f_old if f.startswith('B width audit')],
             'E8': [f for f in f_old if f.startswith('D1 no "1 - CHISQUARE_CDF"')],
             'E9': [f for f in f_old if f.startswith('B5 ') and ('2.5' in f)],
             'E1': [f for f in f_old if f.startswith('C5 option')],
             'D8': [f for f in f_old if f.startswith('D8 ')],
             'E7': [f for f in f_old if f.startswith('B3 (1, 999999, 1, 1000000)')]}
    print('  v1.7c\'s failures by finding: %s' % ', '.join('%s %d' % (k, len(v)) for k, v in old_e.items()))
    check(len(old_e['E4']) == 6 and len(old_e['E2']) == 2 and len(old_e['E3']) == 6 and len(old_e['E6']) == 1
          and len(old_e['E8']) == 1 and len(old_e['E9']) >= 2 and len(old_e['E1']) == 12 and len(old_e['D8']) == 2
          and len(old_e['E7']) == 3 and any(f.startswith(E7_LABEL) for f in f_old)
          and sum(len(v) for v in old_e.values()) == len(f_old),
          'regression: on v1.7c the same script fails every check these findings name, and nothing else -- E4 x 6, '
          'E2 x 2, E3 x 6, E6, E8, E9, E1 x 12, the two version checks (D8) and E7 x 3 (the scientific form, EP_NNT, '
          'the icon array); on v1.7d none is left')


def main():
    t0 = time.time()
    part_a(); part_b(); part_c(); part_d(); part_e(); part_g()
    part_f(); part_h(); part_g2(); part_i(); part_review(); part_sci()
    print('\n' + '=' * 78)
    print('%s: %d checks, %d failures  [%.0f s]' % ('ALL CHECKS PASSED' if not FAILS else 'FAILURES', NCHK[0], len(FAILS), time.time() - t0))
    for f in FAILS:
        print('  -', f)
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
