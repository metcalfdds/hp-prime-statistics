# crc_check_v8.py : group 3b
#   estimators 202, Cochran 247-248, Dixon 251, 2 x 2 contingency tables 254-267, Duncan 294-296, Dunnett 297-299
import sys, re, math, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from crc_lib import *
import numpy as np
from scipy import stats, special, optimize

only = set(sys.argv[1:])
def want(n): return (not only) or (n in only)
GX, GW = np.polynomial.legendre.leggauss(400)

# ---------------------------------------------------------------- Cochran's test
def cochran_tail(c, k, v):
    """P(largest variance / sum > c) for k variances of v degrees of freedom each: the first two terms of the
    inclusion-exclusion sum (the first alone is exact for c >= 1/2; the third is of the order alpha^3 / 6)."""
    a = v / 2.0
    p1 = k * stats.beta.sf(c, a, (k - 1) * a)
    if c >= 0.5 or k < 2: return p1
    if k == 2: return p1 - (stats.beta.cdf(1 - c, a, a) - stats.beta.cdf(c, a, a))
    x = 0.5 * (1 - 2 * c) * GX + 0.5; w = 0.5 * (1 - 2 * c) * GW          # x from c to 1 - c
    p2 = np.sum(w * stats.beta.pdf(x, a, (k - 1) * a) * stats.beta.sf(c / (1 - x), a, (k - 2) * a))
    return p1 - k * (k - 1) / 2.0 * p2
def cochran_crit(alpha, k, v, first_only=False):
    c1 = optimize.brentq(lambda c: k * stats.beta.sf(c, v / 2.0, (k - 1) * v / 2.0) - alpha, 1.0 / k + 1e-12, 1 - 1e-12, xtol=1e-13)
    if first_only or c1 >= 0.5: return c1
    f = lambda c: cochran_tail(c, k, v) - alpha          # at c1 this is minus the second term, so the root lies just below c1
    if f(c1) > -1e-14: return c1
    lo = c1
    for _ in range(60):
        lo = lo - 0.01 * (c1 - 1.0 / k)
        if f(lo) > 0: return optimize.brentq(f, lo, c1, xtol=1e-13)
    return c1
if want('cochran'):
    for p in (247, 248):
        cells = []; hdr = None
        for ln in L(p):
            tk = [t for a, b, t in toks(ln)]
            if tk and tk[0] == 'k' and len(tk) > 10: hdr = tk[1:]; continue
            if hdr and len(tk) == len(hdr) + 1 and all(isnum(t) or t == '∞' for t in tk):
                cells.append((tk[0], tk[1:]))
        for alpha in (0.05, 0.01):
            T = Tally('cochran_p%d_at_%g' % (p, alpha), 'Cochran critical values on p.%d (headed alpha = .05), worked at alpha = %g' % (p, alpha))
            T1 = Tally('cochran_p%d_at_%g_firstterm' % (p, alpha), 'the same against the first-term approximation k P(Beta > c) = alpha')
            for k, vals in cells:
                for h, t in zip(hdr, vals):
                    if k == '∞' or h == '∞':
                        tr = 0.0 if k == '∞' else 1.0 / int(k)
                        T.add(p, 'k %s' % k, 'df %s' % h, t, tr); continue
                    T.add(p, 'k %s' % k, 'df %s' % h, t, cochran_crit(alpha, int(k), int(h)))
                    T1.add(p, 'k %s' % k, 'df %s' % h, t, cochran_crit(alpha, int(k), int(h), True))
            T.done(show=4); T1.done(show=0)

# ---------------------------------------------------------------- Dixon's ratios
x = 9 * GX; wx = 9 * GW; t = 9 * (GX + 1); wt = 9 * GW
U, TT = np.meshgrid(x, t, indexing='ij'); WW = np.outer(wx, wt); V = U + TT
pu, pv, Fu, Fv = stats.norm.pdf(U), stats.norm.pdf(V), stats.norm.cdf(U), stats.norm.cdf(V)
def dixon_tail(R, n, kind):
    Fw = stats.norm.cdf(V - R * TT)                          # w = v - R (v - u)
    if kind == 'r10':
        return float(np.sum(WW * n * (n - 1) * pu * pv * (Fw - Fu) ** (n - 2)))
    if kind == 'r11':
        return float(np.sum(WW * n * (n - 1) * (n - 2) * Fu * pu * pv * (Fw - Fu) ** (n - 3)))
    if kind == 'r20':
        m = n - 2
        return float(np.sum(WW * n * (n - 1) * pu * pv * ((Fw - Fu) ** m + m * (Fw - Fu) ** (m - 1) * (Fv - Fw))))
if want('dixon'):
    kind = None; al = None; Ts = {}
    for ln in L(251):
        m = re.search(r'Percentage values for (r\d\d)', ln)
        if m: kind = m.group(1); al = None; continue
        tk = [tt for a, b, tt in toks(ln)]
        if kind and tk[:3] == ['n', 'α', '=']: al = [float(v) for v in tk[3:]]; continue
        if kind and al and len(tk) == len(al) + 1 and all(isnum(v) for v in tk):
            n = int(tk[0])
            T = Ts.setdefault(kind, Tally('dixon_' + kind, 'Percentage values for ' + kind))
            if kind not in ('r10', 'r11', 'r20') or (kind == 'r11' and n < 4) or (kind == 'r20' and n < 4): continue
            for a, v in zip(al, tk[1:]):
                T.add(251, 'n %d' % n, 'alpha %g' % a, v, optimize.brentq(lambda R: dixon_tail(R, n, kind) - a, 1e-9, 1 - 1e-9, xtol=1e-10))
    for T in Ts.values(): T.done(show=6)

# ---------------------------------------------------------------- 2 x 2 contingency tables (Finney)
if want('finney'):
    T = Tally('contingency_2x2_b', '2 x 2 contingency tables: the tabulated b')
    Tp = Tally('contingency_2x2_p', '2 x 2 contingency tables: the probability printed with b')
    E = r'(?:\d+\.\d{3}|[−–-])'
    pat = re.compile(r'(?:A\s*=\s*(\d+)\s+)?(?:B\s*=\s*(\d+)\s+)?(\d+)\s+(' + E + r')\s+(' + E + r')\s+(' + E + r')\s+(' + E + r')(?=\s|$)')
    levels = [0.05, 0.025, 0.01, 0.005]; unread = 0; A = B = None
    for p in range(254, 268):
        thr = None; left = []; right = []
        for ln in L(p):
            if thr is None:
                ms = [m.end() for m in re.finditer(r'0\.005', ln)]
                if len(ms) >= 1 and '0.025' in ln: thr = ms[0] - 5
                continue
            for m in pat.finditer(ln):
                (left if m.start() < thr else right).append(m.groups())
            if re.search(r'\d\.\d{3}', ln) and not pat.search(ln): unread += 1
        for g in left + right:                         # the table runs down the left half, then down the right half
            if g[0]: A = int(g[0])
            if g[1]: B = int(g[1])
            a = int(g[2])
            if A is None or B is None: unread += 1; continue
            for lev, e in zip(levels, g[3:]):
                best = None
                for b in range(0, B + 1):
                    pr = stats.hypergeom.cdf(b, A + B, B, a + b)
                    if pr <= lev * (1 + 1e-9): best = (b, pr)
                    else: break
                row = 'A %d B %d a %d' % (A, B, a)
                if e in ('−', '–', '-'):
                    T.add(p, row, 'level %g' % lev, '-1', -1 if best is None else best[0]); continue
                bp, pp = e.split('.')
                v = T.add(p, row, 'level %g' % lev, bp, -1 if best is None else best[0])
                if v == 'ok': Tp.add(p, row, 'level %g' % lev, '0.' + pp, best[1])
    if unread: T.note('%d lines or rows with numbers were not read' % unread)
    T.done(show=8); Tp.done(show=8)

# ---------------------------------------------------------------- Dunnett
def dunnett_fun(k, v):
    z = 9 * GX; wz = 9 * GW
    lo = math.sqrt(stats.chi2.ppf(1e-13, v) / v); hi = math.sqrt(stats.chi2.isf(1e-13, v) / v)
    s = 0.5 * (hi - lo) * GX + 0.5 * (hi + lo); ws = 0.5 * (hi - lo) * GW
    fs = 2 * v * s * stats.chi2.pdf(v * s * s, v)            # density of s = sqrt(chi2_v / v)
    Z, S = np.meshgrid(z, s, indexing='ij'); Wt = np.outer(wz * stats.norm.pdf(z), ws * fs)
    r2 = math.sqrt(2.0)
    two = lambda d: float(np.sum(Wt * (stats.norm.cdf(Z + r2 * d * S) - stats.norm.cdf(Z - r2 * d * S)) ** k))
    one = lambda d: float(np.sum(Wt * stats.norm.cdf(Z + r2 * d * S) ** k))
    return two, one
if want('dunnett'):
    rows = []                                              # (page, half, n, values)
    for p in (297, 298, 299):
        for ln in L(p):
            tk = [tt for a, b, tt in toks(ln)]
            if len(tk) in (10, 20) and all(isnum(v) or v == '∞' for v in tk) and all('.' in v for v in tk[1:10]):
                for h in range(len(tk) // 10):
                    rows.append((p, h, tk[10 * h], tk[10 * h + 1:10 * h + 10]))
    # each row is placed by its own first value: with one treatment, d is Student's t for that row's degrees of freedom
    groups = {}
    for p, h, n, vals in rows:
        v = 10 ** 7 if n == '∞' else int(n); d1 = float(vals[0])
        cand = {('two-sided', 0.05): stats.t.isf(0.025, v), ('two-sided', 0.01): stats.t.isf(0.005, v),
                ('one-sided', 0.05): stats.t.isf(0.05, v), ('one-sided', 0.01): stats.t.isf(0.01, v)}
        key = min(cand, key=lambda c: abs(cand[c] - d1))
        groups.setdefault(key, []).append((p, n, vals))
    for (side, alpha), rs in sorted(groups.items()):
        T = Tally('dunnett_%s_%g' % (side, alpha), "Dunnett's d, %s, alpha = %g" % (side, alpha))
        for p, n, vals in rs:
            vv = 10 ** 7 if n == '∞' else int(n)
            for k, tt in enumerate(vals, start=1):
                two, one = dunnett_fun(k, vv)
                f = two if side == 'two-sided' else one
                T.add(p, 'df %s' % n, 'k %d' % k, tt, optimize.brentq(lambda d: f(d) - (1 - alpha), 0.5, 40, xtol=1e-9))
        T.note('rows: ' + ' '.join(str(n) for p, n, vals in rs))
        T.done(show=6)

# ---------------------------------------------------------------- Duncan (slow: SciPy's studentized range)
if want('duncan'):
    for p, alpha in ((294, 0.05), (295, 0.01), (296, 0.001)):
        T = Tally('duncan_%g' % alpha, "Critical values for Duncan's test, alpha = %g" % alpha)
        T2 = Tally('duncan_%g_raw' % alpha, 'the same cells where the running maximum applies, against the unadjusted quantile')
        ps = None
        for ln in L(p):
            tk = [tt for a, b, tt in toks(ln)]
            if tk and tk[0] == 'n' and len(tk) > 5 and tk[1].startswith('p'):
                ps = [int(v.replace('p=', '')) for v in tk[1:] if v.replace('p=', '').isdigit()]; continue
            if ps and len(tk) >= 3 and (tk[0].isdigit() or tk[0] == '∞') and all(isnum(v) for v in tk[1:]):
                df = 10 ** 6 if tk[0] == '∞' else int(tk[0])
                run = 0.0                              # Duncan's ranges never decrease with p: each is the larger of its own value and the one before
                for pp in range(2, max(ps) + 1):
                    try: raw = stats.studentized_range.ppf((1 - alpha) ** (pp - 1), pp, df)
                    except Exception: raw = float('nan')
                    run = max(run, raw) if raw == raw else run
                    if pp in ps and ps.index(pp) < len(tk) - 1:
                        v = tk[1 + ps.index(pp)]
                        T.add(p, 'df %s' % tk[0], 'p %d' % pp, v, run)
                        if abs(run - raw) > 1e-9: T2.add(p, 'df %s' % tk[0], 'p %d' % pp, v, raw)
                if len(tk) - 1 != len(ps): T.note('df %s: %d cells for %d columns' % (tk[0], len(tk) - 1, len(ps)))
        T.done(show=6); T2.done(show=0)

# ---------------------------------------------------------------- estimators of the mean and of sigma, p.202
if want('estim'):
    def om(i, n):
        c = math.exp(special.gammaln(n + 1) - special.gammaln(i) - special.gammaln(n - i + 1))
        f = c * stats.norm.pdf(x) * stats.norm.cdf(x) ** (i - 1) * stats.norm.sf(x) ** (n - i)
        return np.sum(wx * f * x), np.sum(wx * f * x * x)
    def covmat(n):
        mu = [om(i, n) for i in range(1, n + 1)]; C = np.zeros((n, n))
        for i in range(1, n + 1):
            C[i - 1, i - 1] = mu[i - 1][1] - mu[i - 1][0] ** 2
            for j in range(i + 1, n + 1):
                c = math.exp(special.gammaln(n + 1) - special.gammaln(i) - special.gammaln(j - i) - special.gammaln(n - j + 1))
                e = np.sum(WW * c * Fu ** (i - 1) * (Fv - Fu) ** (j - i - 1) * stats.norm.sf(V) ** (n - j) * pu * pv * U * V)
                C[i - 1, j - 1] = C[j - 1, i - 1] = e - mu[i - 1][0] * mu[j - 1][0]
        return C
    T = Tally('estimators_mean', 'Estimators of the mean: variance and efficiency (p.202)')
    for ln in L(202):
        m = re.match(r'\s*(\d+)\s+(.*)$', ln)
        if not m or '(x' not in ln or '+' not in ln: continue
        n = int(m.group(1)); rest = m.group(2)
        nums = re.findall(r'(?<![\w.(])(\d?\.\d{3})(?![\w.])', rest)
        ij = re.search(r'\(x(\d+)\s*\+\s*x(\d+)\s*\)', rest)
        if not ij or n > 20: continue
        C = covmat(n); i, j = int(ij.group(1)), int(ij.group(2))
        w_med = np.zeros(n)
        if n % 2: w_med[n // 2] = 1
        else: w_med[n // 2 - 1] = w_med[n // 2] = 0.5
        w_mid = np.zeros(n); w_mid[0] = w_mid[-1] = 0.5
        w_b2 = np.zeros(n); w_b2[i - 1] += 0.5; w_b2[j - 1] += 0.5
        var = lambda w: float(w @ C @ w)
        tr = [var(w_med), (1.0 / n) / var(w_med), var(w_mid), (1.0 / n) / var(w_mid), var(w_b2), (1.0 / n) / var(w_b2)]
        if n > 2:
            w_tr = np.zeros(n); w_tr[1:-1] = 1.0 / (n - 2); tr += [var(w_tr), (1.0 / n) / var(w_tr)]
        names = ['median var', 'median eff', 'midrange var', 'midrange eff', 'best two var', 'best two eff', 'trimmed var', 'trimmed eff']
        if len(nums) != len(tr): T.note('n %d: %d numbers read for %d expected' % (n, len(nums), len(tr)))
        for nm, v, tv in zip(names, nums, tr): T.add(202, 'n %d' % n, nm, v, tv)
    T.done(show=10)
    T = Tally('estimators_range', 'Estimating sigma from the sample range (p.202)')
    for ln in L(202):
        m = re.match(r'\s*(\d+)\s+(\.\d+)w\s+(\.\d+)\s+(1?\.\d+)\s*$', ln)
        if not m: continue
        n = int(m.group(1))
        dens = n * (n - 1) * pu * pv * (Fv - Fu) ** (n - 2)
        m1 = np.sum(WW * dens * TT); m2 = np.sum(WW * dens * TT * TT); d2 = m1; d3 = math.sqrt(m2 - m1 * m1)
        c4 = math.sqrt(2.0 / (n - 1)) * math.exp(special.gammaln(n / 2.0) - special.gammaln((n - 1) / 2.0))
        T.add(202, 'n %d' % n, 'coefficient', m.group(2), 1 / d2)
        T.add(202, 'n %d' % n, 'variance', m.group(3), (d3 / d2) ** 2)
        T.add(202, 'n %d' % n, 'efficiency', m.group(4), ((1 - c4 * c4) / (c4 * c4)) / (d3 / d2) ** 2)
    T.done(show=10)
