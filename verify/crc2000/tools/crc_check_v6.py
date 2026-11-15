# crc_check_v6.py : group 2 of the remaining tables
#   normal order statistics 75-76, probability integral of the range 79-86, Kendall 352, one-sample K-S 355-356,
#   Kruskal-Wallis 359-361, runs 362-371, Spearman 375-377, signed ranks 379, Mann-Whitney critical values 385-388,
#   control chart constants 392, factorials 521, Stirling numbers 529-530, sums of powers 531, median k1 k2 211
import sys, re, math, itertools
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from crc_lib import *
import numpy as np
from scipy import stats, special

only = set(sys.argv[1:])
def want(n): return (not only) or (n in only)

GX, GW = np.polynomial.legendre.leggauss(1200)
def gl(f, a, b):
    x = 0.5 * (b - a) * GX + 0.5 * (b + a)
    return 0.5 * (b - a) * np.sum(GW * f(x))

def place(tk, hdr):
    """Cells of one row to the columns of a heading: in order if the row is full, else by nearest centre."""
    if len(tk) == len(hdr): return list(range(len(tk)))
    hc = [(a + b) / 2.0 for a, b, t in hdr]
    return [min(range(len(hc)), key=lambda i: abs(hc[i] - (a + b) / 2.0)) for a, b, t in tk]

# ---------------------------------------------------------------- expected values of normal order statistics
if want('ordstat'):
    T = Tally('order_statistics', 'Expected value of the ith normal order statistic')
    def ex(j, n):                                   # jth largest of n
        c = math.exp(special.gammaln(n + 1) - special.gammaln(j) - special.gammaln(n - j + 1))
        return gl(lambda x: x * c * stats.norm.pdf(x) * stats.norm.cdf(x) ** (n - j) * stats.norm.sf(x) ** (j - 1), -10, 10)
    for p in (75, 76):
        hdr = None
        for ln in L(p):
            tkp = toks(ln)
            tk = [t for a, b, t in tkp]
            if tk and tk[0] == 'j' and ('n' in tk[1:3] or tk[1].startswith('n=')):
                h = [(a, b, t.replace('n=', '')) for a, b, t in tkp[1:] if t not in ('n', '=')]
                hdr = [(a, b, t) for a, b, t in h if t.isdigit()]; continue
            if hdr and tk and tk[0].isdigit() and len(tk) > 1 and all(isnum(t) or t in ('—', '-', '–') for t in tk[1:]):
                j = int(tk[0]); cells = tkp[1:]
                for (a, b, t), ci in zip(cells, place(cells, hdr)):
                    if not isnum(t): continue
                    n = int(hdr[ci][2])
                    T.add(p, 'j %d' % j, 'n %d' % n, t, ex(j, n))
            elif hdr and tk and not tk[0].isdigit(): hdr = None if len(tk) > 3 and not isnum(tk[1]) else hdr
    T.done()

# ---------------------------------------------------------------- probability integral of the range
if want('range'):
    T = Tally('range_integral', 'Probability integral of the range')
    cache = {}
    def F(w, n):
        return n * gl(lambda x: stats.norm.pdf(x) * (stats.norm.cdf(x + w) - stats.norm.cdf(x)) ** (n - 1), -10, 10)
    for p in range(79, 87):
        hdr = None
        for ln in L(p):
            tkp = toks(ln); tk = [t for a, b, t in tkp]
            if tk and tk[0] == 'W':
                hdr = [(a, b, t.replace('n=', '')) for a, b, t in tkp[1:] if t not in ('n', '=')]
                hdr = [(a, b, t) for a, b, t in hdr if t.isdigit()]; continue
            if hdr and len(tk) >= 2 and all(isnum(t) for t in tk) and '.' in tk[0]:
                w = float(tk[0]); cells = tkp[1:]
                for (a, b, t), ci in zip(cells, place(cells, hdr)):
                    T.add(p, 'W %.2f' % w, 'n %s' % hdr[ci][2], t, F(w, int(hdr[ci][2])))
    T.done()

# ---------------------------------------------------------------- Kendall's S
if want('kendall'):
    T = Tally('kendall_S', "Distribution of Kendall's rank correlation coefficient in random rankings")
    def invdist(n):                                  # counts of permutations of n by number of inversions
        c = np.array([1.0])
        for k in range(2, n + 1): c = np.convolve(c, np.ones(k))
        return c
    upper = {}
    for n in range(3, 11):
        c = invdist(n); N = n * (n - 1) // 2
        S = N - 2 * np.arange(N + 1); pr = c / c.sum()
        upper[n] = lambda s, S=S, pr=pr: float(pr[S >= s].sum())
    hdr = None
    for ln in L(352):
        tkp = toks(ln); tk = [t for a, b, t in tkp]
        if tk and tk[0] == 'St' and len(tk) > 4:
            hdr = [(a, b, t.replace('n=', '')) for a, b, t in tkp[1:] if t not in ('n', '=')]
            hdr = [(a, b, t) for a, b, t in hdr if t.isdigit()]; continue
        if hdr and len(tk) >= 2 and tk[0].isdigit() and all(isnum(t) and '.' in t for t in tk[1:]):
            s = int(tk[0]); cells = tkp[1:]
            for (a, b, t), ci in zip(cells, place(cells, hdr)):
                T.add(352, 'S %d' % s, 'n %s' % hdr[ci][2], t, upper[int(hdr[ci][2])](s))
    T.done()

# ---------------------------------------------------------------- one-sample Kolmogorov-Smirnov
if want('ks1'):
    al = [0.10, 0.05, 0.025, 0.01, 0.005]
    T1 = Tally('ks_one_sample_1sided', 'K-S one-sample critical values against the exact one-sided distribution')
    T2 = Tally('ks_one_sample_2sided', 'K-S one-sample critical values against the exact two-sided distribution')
    for p in (355, 356):
        for ln in L(p):
            tk = [t.replace('n=', '') for a, b, t in toks(ln)]
            tk = [t for t in tk if t not in ('n', '=')]
            if len(tk) == 6 and tk[0].isdigit() and all(isnum(t) and '.' in t for t in tk[1:]):
                n = int(tk[0])
                for j, t in enumerate(tk[1:]):
                    T1.add(p, 'n %d' % n, 'one-sided %g' % al[j], t, stats.ksone.ppf(1 - al[j], n))
                    T2.add(p, 'n %d' % n, 'two-sided %g' % (2 * al[j]), t, stats.kstwo.ppf(1 - 2 * al[j], n))
    T1.done(); T2.done()

# ---------------------------------------------------------------- Kruskal-Wallis exact levels
def kw_dist(sizes):
    """Exact null distribution of H for groups of the given sizes (no ties): dict H -> probability."""
    g = len(sizes); N = sum(sizes)
    st = {((0,) * (g - 1), (0,) * (g - 1)): 1}
    for r in range(1, N + 1):
        nx = {}
        for (cnt, sm), w in st.items():
            placed = sum(cnt)
            for i in range(g - 1):
                if cnt[i] < sizes[i]:
                    k = (cnt[:i] + (cnt[i] + 1,) + cnt[i + 1:], sm[:i] + (sm[i] + r,) + sm[i + 1:])
                    nx[k] = nx.get(k, 0) + w
            if (r - 1 - placed) < sizes[-1]:
                nx[(cnt, sm)] = nx.get((cnt, sm), 0) + w
        st = nx
    tot = sum(st.values()); d = {}
    for (cnt, sm), w in st.items():
        rl = N * (N + 1) // 2 - sum(sm)
        h = 12.0 / (N * (N + 1)) * (sum(s * s / float(n) for s, n in zip(sm, sizes[:-1])) + rl * rl / float(sizes[-1])) - 3 * (N + 1)
        h = round(h, 9); d[h] = d.get(h, 0) + w
    return {h: w / float(tot) for h, w in d.items()}
if want('kw'):
    T = Tally('kruskal_wallis', 'Kruskal-Wallis exact probability levels')
    Th = Tally('kruskal_wallis_h', 'Kruskal-Wallis: the h values printed, against the attainable values of H')
    dist = {}; nogrp = 0
    for p in range(358, 362):
        groups = None
        for ln in L(p):
            ms = list(re.finditer(r'\{ni ?\}\s*=\s*\{([\d, ]+)\}', ln))
            if ms:
                groups = [(m.start(), tuple(int(x) for x in re.findall(r'\d+', m.group(1)))) for m in ms]; continue
            if groups is None: continue
            tkp = toks(ln)
            if not tkp or not all(isnum(t) and '.' in t for a, b, t in tkp) or len(tkp) % 2: continue
            for q in range(0, len(tkp), 2):
                (a, b, hs), (a2, b2, ps) = tkp[q], tkp[q + 1]
                gi = min(range(len(groups)), key=lambda i: abs(groups[i][0] - a))
                sz = groups[gi][1]
                if sum(sz) > 16: nogrp += 1; continue
                if sz not in dist: dist[sz] = kw_dist(sz)
                d = dist[sz]; h = float(hs)
                near = min(d, key=lambda x: abs(x - h))
                Th.add(p, str(sz), 'h', hs, near)
                T.add(p, str(sz), 'P(H>=%s)' % hs, ps, sum(w for x, w in d.items() if x >= near - 1e-7))
    if nogrp: T.note('%d cells of groups with more than 16 values were not worked out' % nogrp)
    T.note('groups: ' + ' '.join(str(k) for k in sorted(dist)))
    Th.done(); T.done()

# ---------------------------------------------------------------- total number of runs
if want('runs'):
    T = Tally('runs', 'Distribution of the total number of runs v in samples of size (m, n)')
    def runs_cdf(m, n):
        tot = special.comb(m + n, m, exact=True); pm = {}
        for v in range(2, m + n + 1):
            k = v // 2
            if v % 2 == 0: c = 2 * special.comb(m - 1, k - 1, exact=True) * special.comb(n - 1, k - 1, exact=True)
            else: c = (special.comb(m - 1, k, exact=True) * special.comb(n - 1, k - 1, exact=True) +
                       special.comb(m - 1, k - 1, exact=True) * special.comb(n - 1, k, exact=True))
            pm[v] = c
        cum = 0; out = {}
        for v in range(2, m + n + 1): cum += pm[v]; out[v] = cum / float(tot)
        return out
    cache = {}
    for p in range(362, 372):
        hdr = None
        for ln in L(p):
            tkp = toks(ln); tk = [t for a, b, t in tkp]
            if tk[:2] == ['m,', 'n'] :
                h = [(a, b, t.replace('v=', '')) for a, b, t in tkp[2:] if t not in ('v', '=')]
                hdr = [(a, b, t) for a, b, t in h if t.isdigit()]; continue
            if hdr and len(tk) >= 3 and re.match(r'^\d+,$', tk[0]) and tk[1].isdigit() and all(isnum(t) and '.' in t for t in tk[2:]):
                m = int(tk[0][:-1]); n = int(tk[1]); cells = tkp[2:]
                if (m, n) not in cache: cache[(m, n)] = runs_cdf(m, n)
                for (a, b, t), ci in zip(cells, place(cells, hdr)):
                    v = int(hdr[ci][2])
                    T.add(p, '%d,%d' % (m, n), 'v %d' % v, t, cache[(m, n)].get(v, 1.0))
    T.done()

# ---------------------------------------------------------------- Spearman
def spearman_counts(n):
    """Counts of permutations of n by S = sum of squared rank differences (index S), by a walk over subsets."""
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
if want('spearman'):
    cnt = {n: spearman_counts(n) for n in range(2, 14)}
    T = Tally('spearman_exact', "Exact values for Spearman's rank correlation coefficient (the smaller tail of S)")
    for p in (376, 377):
        hdr = None
        for ln in L(p):
            tkp = toks(ln); tk = [t for a, b, t in tkp]
            if tk and tk[0].startswith('n=') or tk[:2] == ['n', '=']:
                h = [(a, b, t.replace('n=', '')) for a, b, t in tkp if t not in ('n', '=')]
                hdr = [(a, b, t) for a, b, t in h if t.isdigit()]; continue
            if hdr and len(tk) >= 2 and tk[0].isdigit() and all(isnum(t) and '.' in t for t in tk[1:]):
                S = int(tk[0]); cells = tkp[1:]
                for (a, b, t), ci in zip(cells, place(cells, hdr)):
                    n = int(hdr[ci][2]); c = cnt[n]; tot = c.sum(); mid = n * (n * n - 1) / 6.0
                    lo = c[:S + 1].sum() / tot if S < len(c) else 1.0
                    hi = c[S:].sum() / tot if S < len(c) else 0.0
                    T.add(p, 'S %d' % S, 'n %d' % n, t, lo if S <= mid else hi)
    T.done()
    T = Tally('spearman_critical', "Critical values of Spearman's rank correlation coefficient")
    al = None; conv = {'P(rs > c) <= a': 0, 'P(rs >= c) <= a': 0}; ncell = 0; beyond = 0
    for p in (375,):
        for ln in L(p):
            tk = [t for a, b, t in toks(ln)]
            if 'α' in tk and '=' in tk: al = [float(t) for t in tk if isnum(t)]; continue
            if al and len(tk) == len(al) + 1 and tk[0].isdigit():
                n = int(tk[0])
                if n not in cnt: beyond += sum(1 for t in tk[1:] if isnum(t)); continue
                c = cnt[n]; tot = c.sum(); D = n * (n * n - 1)
                for j, t in enumerate(tk[1:]):
                    if not isnum(t): continue
                    a = al[j]; ncell += 1
                    # smallest attainable r with P(rs > r) <= a   (S even, r = 1 - 6S/D)
                    best = None
                    for S in range(0, len(c), 2):
                        if c[:S].sum() / tot <= a: best = S       # P(rs > r_S) = P(S' < S)
                        else: break
                    r1 = 1 - 6.0 * best / D
                    best2 = None
                    for S in range(0, len(c), 2):
                        if c[:S + 1].sum() / tot <= a: best2 = S
                        else: break
                    r2 = None if best2 is None else 1 - 6.0 * best2 / D
                    v1 = verdict(t, r1); conv['P(rs > c) <= a'] += v1 == 'ok'
                    if r2 is not None: conv['P(rs >= c) <= a'] += verdict(t, r2) == 'ok'
                    T.add(p, 'n %d' % n, 'alpha %g' % a, t, r1)
    T.note('rule P(rs > c) <= alpha fits %d of %d cells; rule P(rs >= c) <= alpha fits %d; %d cells for n above 13 not worked out'
           % (conv['P(rs > c) <= a'], ncell, conv['P(rs >= c) <= a'], beyond))
    T.done(show=10)

# ---------------------------------------------------------------- Wilcoxon signed ranks
if want('signedrank'):
    T = Tally('signed_rank_critical', 'Critical values for the Wilcoxon signed-ranks test')
    def sr_cdf(n):
        c = np.array([1.0])
        for k in range(1, n + 1):
            d = np.zeros(len(c) + k); d[:len(c)] += c; d[k:] += c; c = d
        return np.cumsum(c) / c.sum()
    ns = None
    for ln in L(379):
        tkp = toks(ln); tk = [t for a, b, t in tkp]
        if 'sided' in tk and 'n' in tk:
            ns = [int(t) for t in tk[tk.index('=') + 1:]]; continue
        if ns and tk[:2] == ['α', '='] and len(tk) >= 7:
            a1 = float(tk[2]); vals = tk[6:]
            for t, n in zip(reversed(vals), reversed(ns)):        # the rows are filled from the right
                cdf = sr_cdf(n); ok = np.where(cdf <= a1 * (1 + 1e-12))[0]
                T.add(379, 'one-sided %g' % a1, 'n %d' % n, t, ok.max() if len(ok) else -1)
    T.done()

# ---------------------------------------------------------------- Mann-Whitney critical values
if want('mwcrit'):
    def mw_cdf(m, n, memo={}):
        if (m, n) in memo: return memo[(m, n)]
        f = [[None] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 or j == 0: f[i][j] = np.array([1.0]); continue
                v = np.zeros(i * j + 1)
                a = f[i - 1][j]; v[j:j + len(a)] += a          # the largest value is an x: it beats all j y's
                b = f[i][j - 1]; v[:len(b)] += b
                f[i][j] = v
        memo[(m, n)] = np.cumsum(f[m][n]) / f[m][n].sum(); return memo[(m, n)]
    res = {}
    for p in range(385, 389):
        level = None; ns = None
        for ln in L(p):
            m = re.search(r'α\s*=\s*(0?\.\d+)\s+level', ln)
            if m: level = float(m.group(1)); continue
            tk = [t for a, b, t in toks(ln)]
            if tk[:3] == ['m', 'n', '=']: ns = [int(t) for t in tk[3:]]; continue
            if level and ns and tk and all(t.isdigit() for t in tk) and len(tk) >= 2:
                mm = int(tk[0]); vals = tk[1:]
                for t, n in zip(reversed(vals), reversed(ns)):
                    cdf = mw_cdf(mm, n)
                    for nm, a in (('one-sided', level), ('two-sided', level / 2)):
                        ok = np.where(cdf <= a * (1 + 1e-12))[0]
                        tr = ok.max() if len(ok) else -1
                        res.setdefault((level, nm), []).append((p, mm, n, t, tr))
    for (level, nm), cells in sorted(res.items()):
        T = Tally('mw_critical_%g_%s' % (level, nm), 'Mann-Whitney critical values, alpha %g read as %s' % (level, nm))
        for p, mm, n, t, tr in cells: T.add(p, 'm %d' % mm, 'n %d' % n, t, tr)
        T.done(show=3)

# ---------------------------------------------------------------- control chart constants
if want('control'):
    T = Tally('control_chart', 'Factors for computing control chart lines')
    def rng_moments(n):
        F = lambda w: n * gl(lambda x: stats.norm.pdf(x) * (stats.norm.cdf(x + w) - stats.norm.cdf(x)) ** (n - 1), -10, 10)
        ws = np.linspace(0, 12, 2401); Fv = np.array([F(w) for w in ws])
        m1 = np.trapezoid(1 - Fv, ws); m2 = np.trapezoid(2 * ws * (1 - Fv), ws)
        return m1, math.sqrt(m2 - m1 * m1)
    hdr = None
    for ln in L(392):
        tk = [t for a, b, t in toks(ln)]
        if tk[:3] == ['n', 'A', 'A1']: hdr = tk[1:]; continue
        if hdr and len(tk) == len(hdr) + 1 and all(isnum(t) for t in tk):
            n = int(tk[0]); c2 = math.sqrt(2.0 / n) * math.exp(special.gammaln(n / 2.0) - special.gammaln((n - 1) / 2.0))
            ss = math.sqrt((n - 1.0) / n - c2 * c2); d2, d3 = rng_moments(n)
            tr = {'A': 3 / math.sqrt(n), 'A1': 3 / (c2 * math.sqrt(n)), 'A2': 3 / (d2 * math.sqrt(n)), 'c2': c2,
                  'B1': max(0, c2 - 3 * ss), 'B2': c2 + 3 * ss, 'B3': max(0, 1 - 3 * ss / c2), 'B4': 1 + 3 * ss / c2,
                  'd2': d2, 'D1': max(0, d2 - 3 * d3), 'D2': d2 + 3 * d3, 'D3': max(0, 1 - 3 * d3 / d2), 'D4': 1 + 3 * d3 / d2,
                  'd3': d3}
            for h, t in zip(hdr, tk[1:]):
                if h in tr: T.add(392, 'n %d' % n, h, t, tr[h])
                else: T.note('column %s not worked out' % h)
    T.done(show=10)

# ---------------------------------------------------------------- factorials
if want('fact'):
    T = Tally('factorials', 'Factorials and double factorials with their logarithms')
    def dfact(n):
        r = 1
        while n > 1: r *= n; n -= 2
        return r
    def take(tk, i):
        """one number at tk[i]: an integer, or mantissa x 10^e; returns (kind, printed, exponent, next index)"""
        if i + 2 < len(tk) and tk[i + 1] == '×':
            return 'sci', tk[i], int(tk[i + 2][2:]), i + 3
        return 'int', tk[i], None, i + 1
    for p in (521, 522):
        for ln in L(p):
            tk = [t for a, b, t in toks(ln)]
            if len(tk) < 5 or not tk[0].isdigit() or not all(isnum(t) or t == '×' for t in tk): continue
            n = int(tk[0])
            try:
                k1, v1, e1, i = take(tk, 1); lg1 = tk[i]; k2, v2, e2, i = take(tk, i + 1); lg2 = tk[i]
            except Exception: T.note('line for n %d not read' % n); continue
            for nm, kind, v, e, lg, true in (('n!', k1, v1, e1, lg1, math.factorial(n)), ('n!!', k2, v2, e2, lg2, dfact(n))):
                if kind == 'int': T.add(p, 'n %d' % n, nm, v, true)
                else:
                    T.add(p, 'n %d' % n, nm + ' mantissa', v, float(__import__('fractions').Fraction(true, 10 ** e)))
                    T.add(p, 'n %d' % n, nm + ' exponent', str(e), len(str(true)) - 1)
                T.add(p, 'n %d' % n, 'log10 ' + nm, lg, math.log10(true))
    T.done()

# ---------------------------------------------------------------- Stirling numbers and sums of powers
if want('stirling'):
    s1 = {(0, 0): 1}; s2 = {(0, 0): 1}
    for n in range(1, 30):
        for m in range(0, n + 1):
            s1[(n, m)] = s1.get((n - 1, m - 1), 0) - (n - 1) * s1.get((n - 1, m), 0)
            s2[(n, m)] = s2.get((n - 1, m - 1), 0) + m * s2.get((n - 1, m), 0)
    for p, nm, tab in ((529, 'stirling_first', s1), (530, 'stirling_second', s2)):
        T = Tally(nm, 'Stirling numbers (%s kind)' % nm.split('_')[1])
        ms = None
        for ln in L(p):
            tkp = toks(ln); tk = [clean(t) for a, b, t in tkp]
            if tk and tk[0] == 'n' and len(tk) > 2 and (tk[1].startswith('m=') or tk[1] == 'm'):
                ms = [int(t.replace('m=', '')) for t in tk[1:] if t.replace('m=', '').isdigit()]; continue
            if ms and len(tk) >= 2 and all(re.match(r'^-?\d+$', t) for t in tk):
                n = int(tk[0])
                for j, t in enumerate(tk[1:]):
                    if j < len(ms): T.add(p, 'n %d' % n, 'm %d' % ms[j], t, tab.get((n, ms[j]), 0))
        T.done()
    T = Tally('sums_of_powers', 'Sums of powers of integers')
    for ln in L(531):
        tk = [t for a, b, t in toks(ln)]
        if len(tk) >= 4 and all(t.isdigit() for t in tk):
            n = int(tk[0])
            for j, t in enumerate(tk[1:]):
                T.add(531, 'n %d' % n, 'power %d' % (j + 1), t, sum(k ** (j + 1) for k in range(1, n + 1)))
    T.done()

# ---------------------------------------------------------------- Table 9.6, k1 and k2 for the median (the book's own formula)
if want('medk'):
    T = Tally('median_k1k2', 'Table 9.6: k1 and k2 from the formula of section 9.5.6')
    for ln in L(211):
        tk = [t for a, b, t in toks(ln)]
        if len(tk) in (3, 5) and all(t.isdigit() for t in tk):
            n = int(tk[0]); N = n * (n - 1) / 2.0
            for j, a in enumerate((0.05, 0.01)):
                if 1 + 2 * j + 1 >= len(tk): continue
                z = stats.norm.isf(a / 2); h = z * N / math.sqrt(3.0 * n)
                T.add(211, 'n %d' % n, 'k1 %g' % a, tk[1 + 2 * j], math.floor(N / 2 - h))
                T.add(211, 'n %d' % n, 'k2 %g' % a, tk[2 + 2 * j], math.ceil(N / 2 + h))
    T.done(show=8)
