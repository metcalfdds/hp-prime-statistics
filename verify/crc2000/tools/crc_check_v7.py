# crc_check_v7.py : group 3a
#   covariances of normal order statistics 77-78, circular error probabilities 195, Poisson limits 213,
#   R for the variance test 249, two-sample K-S 357, runs for m = n 371, sign test 373,
#   permutations 506, combinations 507-509, partitions 528
import sys, re, math
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from crc_lib import *
import numpy as np
from scipy import stats, special
from fractions import Fraction

only = set(sys.argv[1:])
def want(n): return (not only) or (n in only)
GX, GW = np.polynomial.legendre.leggauss(500)

# ---------------------------------------------------------------- covariances of normal order statistics
if want('ordcov'):
    T = Tally('order_stat_covariances', 'Variances and covariances of normal order statistics')
    x = 9 * GX; wx = 9 * GW                      # x from -9 to 9
    t = 9 * (GX + 1); wt = 9 * GW                # t = y - x from 0 to 18
    X, TT = np.meshgrid(x, t, indexing='ij'); Wt = np.outer(wx, wt); Y = X + TT
    px, py = stats.norm.pdf(X), stats.norm.pdf(Y); Fx, Fy, Sy = stats.norm.cdf(X), stats.norm.cdf(Y), stats.norm.sf(Y)
    def mean(i, n):
        c = math.exp(special.gammaln(n + 1) - special.gammaln(i) - special.gammaln(n - i + 1))
        f = c * stats.norm.pdf(x) * stats.norm.cdf(x) ** (i - 1) * stats.norm.sf(x) ** (n - i)
        return np.sum(wx * f * x), np.sum(wx * f * x * x)
    def cov(i, j, n):                              # i <= j, ascending order statistics
        mi, m2i = mean(i, n)
        if i == j: return m2i - mi * mi
        mj, _ = mean(j, n)
        c = math.exp(special.gammaln(n + 1) - special.gammaln(i) - special.gammaln(j - i) - special.gammaln(n - j + 1))
        e = np.sum(Wt * c * Fx ** (i - 1) * (Fy - Fx) ** (j - i - 1) * Sy ** (n - j) * px * py * X * Y)
        return e - mi * mj
    nline = 0
    for p in (77, 78):
        cur = {}                                   # per block (three blocks a line): current n and k
        for ln in L(p):
            tkp = toks(ln)
            if not tkp or not all(isnum(tt) for a, b, tt in tkp): continue
            vals = [q for q in tkp if q[2].startswith('.') or re.match(r'^\d\.\d+$', q[2])]
            if not vals: continue
            # split the tokens of the line into the blocks that end with a value
            blocks = []; curb = []
            for q in tkp:
                curb.append(q)
                if q in vals: blocks.append(curb); curb = []
            for bl in blocks:
                key = min(cur, key=lambda s: abs(s - bl[-1][1])) if cur and min(abs(s - bl[-1][1]) for s in cur) < 6 else bl[-1][1]
                st = cur.setdefault(key, {'n': None, 'k': None})
                ints = [int(q[2]) for q in bl[:-1]]
                if len(ints) == 3: st['n'], st['k'], l = ints
                elif len(ints) == 2: st['k'], l = ints
                elif len(ints) == 1: l = ints[0]
                else: continue
                if st['n'] is None or st['k'] is None: continue
                n, k = st['n'], st['k']
                i, j = sorted((n - k + 1, n - l + 1))
                T.add(p, 'n %d' % n, 'k %d l %d' % (k, l), bl[-1][2], cov(i, j, n)); nline += 1
    T.done()

# ---------------------------------------------------------------- circular error probabilities
if want('cep'):
    T = Tally('circular_error', 'Circular error probabilities')
    def P(K, c):
        if c == 0: return 2 * stats.norm.cdf(K) - 1
        lim = K / c
        y = lim * GX; w = lim * GW
        return float(np.sum(w * stats.norm.pdf(y) * (2 * stats.norm.cdf(np.sqrt(np.maximum(K * K - c * c * y * y, 0))) - 1)))
    cols = None
    for ln in L(195):
        tk = [t for a, b, t in toks(ln)]
        if tk and tk[0] == 'K': cols = [float(t) for t in tk[1:] if isnum(t)]; continue
        if cols and len(tk) == len(cols) + 1 and all(isnum(t) for t in tk):
            K = float(tk[0])
            for j, v in enumerate(tk[1:]):
                T.add(195, 'K %g' % K, 'c %g' % cols[j], v, P(K, cols[j]))
    T.note('c taken as the ratio of the smaller standard deviation to the larger, K in units of the larger')
    T.done()

# ---------------------------------------------------------------- confidence limits for a Poisson mean
if want('poislim'):
    T = Tally('poisson_limits', 'Confidence limits for the mean of a Poisson distribution')
    for ln in L(213):
        tk = [t for a, b, t in toks(ln)]
        if len(tk) in (5, 10) and all(isnum(t) for t in tk):
            for g in range(0, len(tk), 5):
                xcount = int(tk[g])
                for j, a in enumerate((0.01, 0.05)):
                    lo = 0.0 if xcount == 0 else stats.chi2.ppf(a / 2, 2 * xcount) / 2
                    hi = stats.chi2.ppf(1 - a / 2, 2 * xcount + 2) / 2
                    T.add(213, 'count %d' % xcount, 'lower %g' % a, tk[g + 1 + 2 * j], lo)
                    T.add(213, 'count %d' % xcount, 'upper %g' % a, tk[g + 2 + 2 * j], hi)
    T.done()

# ---------------------------------------------------------------- R = chi2(alpha)/chi2(1-beta), p.249
if want('rvar'):
    T = Tally('variance_R', 'Values of R given n, alpha and beta')
    for ln in L(249):
        tk = [t for a, b, t in toks(ln)]
        if len(tk) == 9 and all(isnum(t) for t in tk) and tk[0].isdigit():
            n = int(tk[0]); q = 1
            for a in (0.01, 0.05):
                for b in (0.01, 0.05, 0.1, 0.5):
                    T.add(249, 'n %d' % n, 'a %g b %g' % (a, b), tk[q], stats.chi2.isf(a, n) / stats.chi2.ppf(b, n)); q += 1
    T.done()

# ---------------------------------------------------------------- two-sample Kolmogorov-Smirnov
def ks2_tail(m, n):
    """P(D >= k/(mn)) for every attainable k, by counting the lattice paths that stay inside."""
    from math import comb
    tot = comb(m + n, m); vals = sorted({abs(i * n - j * m) for i in range(m + 1) for j in range(n + 1)})
    out = {}
    for k in vals:
        if k == 0: out[k] = 1.0; continue
        # paths with |i n - j m| < k throughout
        f = [[0] * (n + 1) for _ in range(m + 1)]; f[0][0] = 1
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 and j == 0: continue
                if abs(i * n - j * m) >= k: f[i][j] = 0; continue
                f[i][j] = (f[i - 1][j] if i else 0) + (f[i][j - 1] if j else 0)
        out[k] = 1 - f[m][n] / float(tot)
    return out
if want('ks2'):
    Ts = {'<=': Tally('ks_two_sample_le', 'Two-sample K-S critical values, least D with P(D >= d) <= alpha'),
          '<': Tally('ks_two_sample_lt', 'Two-sample K-S critical values, least D with P(D >= d) < alpha')}
    n1s = None; cur = None; denbad = []
    for p in (357, 358):
        for ln in L(p):
            tk = [t for a, b, t in toks(ln)]
            if tk[:2] == ['size', 'n2']: n1s = [int(t) for t in tk[2:]]; cur = None; continue
            if not n1s or not tk: continue
            cells = [t for t in tk if t == '∗' or re.match(r'^\d+/\d+$', t)]
            if not cells: continue
            if tk[0].isdigit() and len(cells) == len(tk) - 1: cur = int(tk[0]); a = 0.05; row = cells
            elif len(cells) == len(tk) and cur is not None: a = 0.01; row = cells
            else: continue
            for t, n1 in zip(reversed(row), reversed(n1s)):       # the rows are filled from the right
                tail = ks2_tail(n1, cur)
                for nm, T in Ts.items():
                    ok = [k for k in sorted(tail) if (tail[k] <= a + 1e-12 if nm == '<=' else tail[k] < a - 1e-12)]
                    tr = ok[0] if ok else None
                    if t == '∗':
                        T.add(p, 'n2 %d a %g' % (cur, a), 'n1 %d' % n1, '0', 0 if tr is None else tr)
                    else:
                        num, den = [int(v) for v in t.split('/')]
                        if den != n1 * cur and nm == '<=': denbad.append('n1 %d n2 %d a %g printed %s' % (n1, cur, a, t))
                        T.add(p, 'n2 %d a %g' % (cur, a), 'n1 %d' % n1, str(num), -1 if tr is None else tr)
    for T in Ts.values():
        if denbad: T.note('denominator is not n1 n2 in: ' + '; '.join(denbad[:6]))
        T.done(show=8)

# ---------------------------------------------------------------- runs, m = n above 10
if want('runs2'):
    from math import comb
    def runs_cdf(m, n):
        tot = comb(m + n, m); cum = 0; out = {}
        for v in range(2, m + n + 1):
            k = v // 2
            c = 2 * comb(m - 1, k - 1) * comb(n - 1, k - 1) if v % 2 == 0 else comb(m - 1, k) * comb(n - 1, k - 1) + comb(m - 1, k - 1) * comb(n - 1, k)
            cum += c; out[v] = Fraction(cum, tot)
        return out
    T = Tally('runs_m_equals_n', 'Distribution of the total number of runs in samples of size m = n (percentage points)')
    T2 = Tally('runs_m_equals_n_moments', 'Runs for m = n: mean, variance and standard deviation')
    pct = [0.5, 1.0, 2.5, 5.0, 95.0, 97.5, 99.0, 99.5]; tried = {}
    for ln in L(371):
        tk = [t for a, b, t in toks(ln)]
        if len(tk) == 12 and all(isnum(t) for t in tk) and tk[0].isdigit():
            m = int(tk[0]); cdf = runs_cdf(m, m)
            for j, t in enumerate(tk[1:9]):
                q = Fraction(str(pct[j])) / 100
                # the page: "values of v such that v or fewer runs occur with probability less than the indicated percentage"
                cand = {'largest v with P(V<=v) < q': max([v for v in cdf if cdf[v] < q] or [0]),
                        'largest v with P(V<=v) <= q': max([v for v in cdf if cdf[v] <= q] or [0]),
                        'smallest v with P(V<=v) >= q': min(v for v in cdf if cdf[v] >= q)}
                for nm, tr in cand.items():
                    tried.setdefault(nm, [0, 0]); tried[nm][0] += int(t) == tr; tried[nm][1] += 1
                T.add(371, 'm=n %d' % m, '%g%%' % pct[j], t, cand['largest v with P(V<=v) < q'] if pct[j] < 50 else cand['smallest v with P(V<=v) >= q'])
            mean = 2.0 * m * m / (2 * m) + 1; var = 2.0 * m * m * (2 * m * m - 2 * m) / ((2 * m) ** 2 * (2 * m - 1))
            T2.add(371, 'm=n %d' % m, 'mean', tk[9], mean); T2.add(371, 'm=n %d' % m, 'var', tk[10], var)
            T2.add(371, 'm=n %d' % m, 'sd', tk[11], math.sqrt(var))
    T.note('; '.join('%s: %d of %d' % (k, v[0], v[1]) for k, v in tried.items()))
    T.done(show=8); T2.done()

# ---------------------------------------------------------------- sign test
if want('sign'):
    T = Tally('sign_test', 'Critical values for the sign test: largest k with P(Y <= k) < alpha/2')
    none = 0
    for ln in L(373):
        tk = [t for a, b, t in toks(ln)]
        if len(tk) in (5, 10) and all(t.isdigit() for t in tk):
            for g in range(0, len(tk), 5):
                n = int(tk[g])
                for j, a in enumerate((0.01, 0.025, 0.05, 0.10)):
                    ks = [k for k in range(n + 1) if stats.binom.cdf(k, n, 0.5) < a / 2]
                    if not ks:
                        none += 1
                        if tk[g + 1 + j] != '0': T.add(373, 'n %d' % n, 'a %g' % a, tk[g + 1 + j], -1)
                        continue
                    T.add(373, 'n %d' % n, 'a %g' % a, tk[g + 1 + j], max(ks))
    T.note('%d cells where no k satisfies the rule; the page prints 0 in them' % none)
    T.done()

# ---------------------------------------------------------------- permutations, combinations, partitions
if want('counts'):
    for p0, p1, nm, fn in ((506, 506, 'permutations', lambda n, m: math.perm(n, m)), (507, 509, 'combinations', lambda n, m: math.comb(n, m))):
        T = Tally(nm, nm.capitalize() + ' table')
        for p in range(p0, p1 + 1):
            ms = None
            for ln in L(p):
                tk = [t for a, b, t in toks(ln)]
                if tk and tk[0] == 'n' and len(tk) > 2 and (tk[1].startswith('m=') or tk[1] == 'm'):
                    ms = [int(t.replace('m=', '')) for t in tk[1:] if t.replace('m=', '').isdigit()]; continue
                if ms and len(tk) >= 2 and all(t.isdigit() for t in tk):
                    n = int(tk[0])
                    for j, t in enumerate(tk[1:]):
                        if j < len(ms): T.add(p, 'n %d' % n, 'm %d' % ms[j], t, fn(n, ms[j]))
                elif ms and len(tk) >= 2 and tk[0].isdigit() and any('×' in t or '.' in t for t in tk):
                    T.note('p%d n %s: a row with numbers in another form was not read' % (p, tk[0]))
        T.done()
    T = Tally('partitions', 'Values of the partition function')
    part = [1] + [0] * 400
    for k in range(1, 401):
        for i in range(k, 401): part[i] += part[i - k]
    ns = None
    for ln in L(528):
        tk = [t for a, b, t in toks(ln)]
        if tk and tk[0] == 'n' and all(t.isdigit() for t in tk[1:]): ns = [int(t) for t in tk[1:]]; continue
        if tk and tk[0] == 'p(n)' and ns and len(tk) - 1 == len(ns):
            for n, t in zip(ns, tk[1:]): T.add(528, 'n %d' % n, 'p(n)', t, part[n])
            ns = None
    T.done()
