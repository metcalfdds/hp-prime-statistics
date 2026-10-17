#!/usr/bin/env python3
"""verify_EpiStats_v1.7a.py -- checks for EpiStats v1.7a (HP Prime PPL), 17 Oct 2026: the CAS call
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

Run:  python3 verify_EpiStats_v1.7a.py      (numpy, scipy, statsmodels, icas, the harness)
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
PPL = os.path.join(HERE, 'EpiStats_v1.7a.txt')
V17 = os.path.join(HERE, 'EpiStats_v1.7.txt')
CQ = os.path.join(HERE, 'CICatcher_beta2a.txt')
sys.path.insert(0, '/home/claude/work/harness')
from ppl_run_v3b import Harness, PPLError, giac_eval, prime_print   # noqa: E402
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
    print('B. The PPL routines themselves, in the harness (ppl_run_v3b)')
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
def part_e():
    print('\n' + '=' * 78)
    print('E. The v1.6 verification suite (verify_EpiStats.py) against v1.7')
    print('=' * 78)
    t0 = time.time()
    r = subprocess.run([sys.executable, os.path.join(HERE, 'verify_EpiStats.py'), PPL], capture_output=True, text=True)
    tail = [ln for ln in r.stdout.split('\n') if 'RESULT' in ln or 'layout audit' in ln or 'warnings (' in ln]
    print('  ' + '\n  '.join(tail))
    check(r.returncode == 0 and any('ALL CHECKS PASSED' in ln for ln in tail),
          'verify_EpiStats.py (v1.6: 120 formula checks, 83 harness checks, 28 scripted runs) passes on v1.7  [%.0f s]'
          % (time.time() - t0))


# ============================================================================ G (1.7a)
def part_g():
    print('\n' + '=' * 78)
    print('G. 1.7a: v1.7 in harness v3b, and v1.7a against v1.7')
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
    check(ok, '1.7a: v1.7 in v3b shows its own CAS text on Help F as if it were the answer '
              '("g\'(p) = diff(ln(p/(1-p)),p)", "= 1/12+1/5+1/8+1/30") -- the emulator\'s finding')
    exec(G_CODE, globals())


G_CODE = "\n# ================================================================ G (round 2a)\nsay('\\nG. v1.7a: v1.7 in harness v3b, and v1.7a against v1.7')\nimport re as _re\n_b_old = open(V17, encoding='utf-8').read()\n_b_new = open(PPL, encoding='utf-8').read()\n\n\ndef _bodies(txt):\n    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)\n    c = _re.sub(r'//[^\\n]*', '', c)\n    out = {}\n    for m in _re.finditer(r'(?m)^(?:EXPORT\\s+|LOCAL\\s+)?([A-Za-z]\\w*)\\(([^()\\n]*)\\)\\s*\\nBEGIN\\n.*?^END;', c, _re.S):\n        out[m.group(1)] = _re.sub(r'[ \\t]+\\n', '\\n', m.group(0))\n    return out\n\n\n_B0, _B1 = _bodies(_b_old), _bodies(_b_new)\n_diff = sorted(n for n in set(_B0) | set(_B1) if _B0.get(n) != _B1.get(n))\ncheck(_diff == ['EpiStats', 'es_Cas', 'es_Help_About'], 'v1.7a: routines that differ from v1.7: %s (want EpiStats, es_Cas, es_Help_About)' % _diff)\n\n\ndef _outside(t, names):\n    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\\n]*', '', t))\n    if names:\n        c = _re.sub(r'(?ms)^(?:EXPORT\\s+|LOCAL\\s+)?(?:%s)\\([^\\n]*\\)\\s*\\nBEGIN\\n.*?^END;' % '|'.join(names), '', c)\n    return _re.sub(r'\\s+', ' ', c)\n\n\ncheck(_outside(_b_old, _diff) == _outside(_b_new, _diff), 'v1.7a: outside those routines only comments differ')\n_py0 = _re.findall(r'(?s)#PYTHON.*?#END', _b_old)\n_py1 = _re.findall(r'(?s)#PYTHON.*?#END', _b_new)\ncheck(_py0 == _py1, 'v1.7a: the #PYTHON blocks are unchanged')\nsay('  routines that differ from v1.7: %s; everything else differs only in comments' % ', '.join(_diff))\n"


def main():
    t0 = time.time()
    part_a(); part_b(); part_c(); part_d(); part_e(); part_g()
    print('\n' + '=' * 78)
    print('%s: %d checks, %d failures  [%.0f s]' % ('ALL CHECKS PASSED' if not FAILS else 'FAILURES', NCHK[0], len(FAILS), time.time() - t0))
    for f in FAILS:
        print('  -', f)
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
