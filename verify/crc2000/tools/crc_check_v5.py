# crc_check_v5.py : group 1 of the remaining tables (prints one line a table, the flagged cells go to work/res_*.json)
#   hypergeometric 105-109, geometric 102, negative binomial 112, chi-square/df 134, critical values 184 and 206,
#   tolerance factors 186, correlation coefficient 193, circular normal 194, t/sqrt(n) 209, medians 212,
#   confidence limits of proportions 215-230, Bessel 513-516, beta 517, gamma 524
import sys, re, math
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from crc_lib import *
import numpy as np
from scipy import stats, special, optimize

only = set(sys.argv[1:])
def want(n): return (not only) or (n in only)

# ---------------------------------------------------------------- hypergeometric
if want('hyper'):
    T = Tally('hypergeometric', 'Hypergeometric probability and distribution functions')
    bad = 0
    for p in range(105, 110):
        for ln in L(p):
            tk = [t for a, b, t in toks(ln)]
            if len(tk) in (6, 12) and all(isnum(t) for t in tk):
                for g in range(0, len(tk), 6):
                    N, n, M, x = [int(t) for t in tk[g:g + 4]]
                    row = 'N=%d n=%d M=%d x=%d' % (N, n, M, x)
                    T.add(p, row, 'F', tk[g + 4], stats.hypergeom.cdf(x, N, M, n))
                    T.add(p, row, 'f', tk[g + 5], stats.hypergeom.pmf(x, N, M, n))
            elif len(tk) >= 5 and sum(isnum(t) for t in tk) >= 5 and 'Hall' not in ln:
                bad += 1
    if bad: T.note('%d lines with numbers were not read' % bad)
    T.done()

# ---------------------------------------------------------------- geometric and negative binomial
def ptable(p, title_re, rowfun, name, title, bypos=False):
    T = Tally(name, title)
    lines = L(p); on = False; cols = None; nrow = 0; cpos = None
    for ln in lines:
        if re.search(title_re, ln): on = True; cols = None; continue
        if not on: continue
        tkp = toks(ln); tk = [t for a, b, t in tkp]
        if not tk: continue
        if 'p' in tk[:3] and '=' in tk[:4]:
            hp = [(a, b, t) for a, b, t in tkp if isnum(t)]
            cols = [float(t) for a, b, t in hp]; cpos = [a for a, b, t in hp]; continue
        if cols is None: continue
        lab = tk[0]; vals = tkp[1:]
        if not vals or not all(isnum(v[2]) for v in vals):
            if nrow: on = False
            continue
        nrow += 1
        for j, (a, b, v) in enumerate(vals):
            if bypos: j = min(range(len(cols)), key=lambda i: abs(cpos[i] - vals[0][0])) + j   # the first cell places the row
            if j < len(cols): T.add(p, lab, 'p=%g' % cols[j], v, rowfun(lab, cols[j]))
    return T

if want('geom'):
    T = ptable(102, r'Probability mass, Geometric', lambda lab, p: p * (1 - p) ** (int(lab) - 1), 'geometric_pmf',
               'Probability mass, Geometric distribution'); T.done()
    T = ptable(102, r'Cumulative.*[Gg]eometric', lambda lab, p: 1 - (1 - p) ** int(lab), 'geometric_cdf',
               'Cumulative probability, Geometric distribution'); T.done()
if want('negbin'):
    def nb(lab, p):
        n, x = [int(v) for v in re.findall(r'\d+', lab)]
        return special.comb(n + x - 1, n - 1) * p ** n * (1 - p) ** x
    T = ptable(112, r'Probability mass, Negative binomial', nb, 'negative_binomial',
               'Probability mass, Negative binomial distribution', bypos=True); T.done(show=12)

# ---------------------------------------------------------------- chi-square over degrees of freedom
if want('chi2df'):
    T = Tally('chi2_over_df', 'Percentage points, chi-square over degrees of freedom')
    for p in (134, 135):
        cols = None
        for ln in L(p):
            tk = [t for a, b, t in toks(ln)]
            if tk and tk[0] in ('ν', 'n') and len(tk) >= 10 and all(isnum(t) for t in tk[1:]):
                cols = [float(t) for t in tk[1:]]; continue
            if cols and len(tk) == len(cols) + 1 and all(isnum(t) for t in tk):
                v = int(tk[0])
                for j, t in enumerate(tk[1:]):
                    T.add(p, 'df %d' % v, '%g%%' % cols[j], t, stats.chi2.ppf(cols[j] / 100.0, v) / v)
    T.done()

# ---------------------------------------------------------------- Table 7.1 (p.184) and Table 9.1 (p.206)
if want('crit'):
    T = Tally('normal_critical_7_1', 'Table 7.1 Common critical values')
    for ln in L(184):
        tk = [t for a, b, t in toks(ln)]
        if len(tk) in (4, 6) and all(isnum(t) for t in tk) and tk[0].startswith('.'):
            for g in range(0, len(tk), 2):
                T.add(184, 'alpha ' + tk[g], 'z', tk[g + 1], stats.norm.isf(float(tk[g])))
    T.done()
    T = Tally('critical_9_1', 'Table 9.1 Common critical values used with confidence intervals')
    al = [0.10, 0.05, 0.01, 0.001, 0.0001]
    for ln in L(206):
        tk = [t for a, b, t in toks(ln)]
        vals = [t for t in tk if isnum(t) and '.' in t]
        if len(vals) != 5: continue
        lab = tk[0]
        m = re.search(r',(\d+)$', lab)
        for j, v in enumerate(vals):
            a = al[j]
            if lab.startswith('t'): tr = stats.t.isf(a / 2, int(m.group(1)))
            elif lab.startswith('z'): tr = stats.norm.isf(a / 2)
            elif lab.startswith('χ21−'): tr = stats.chi2.ppf(a / 2, int(m.group(1)))
            elif lab.startswith('χ2α'): tr = stats.chi2.isf(a / 2, int(m.group(1)))
            else: continue
            T.add(206, lab, 'alpha %g' % a, v, tr)
    T.done()

# ---------------------------------------------------------------- tolerance factors (two-sided, normal)
def tol_exact(n, P, g):
    """Two-sided tolerance factor: with confidence g, at least P of a normal population lies in xbar +- k s."""
    nu = n - 1
    x, w = np.polynomial.legendre.leggauss(160)
    z = 4.5 * (x + 1); w = 4.5 * w                       # z from 0 to 9
    r2 = stats.ncx2.ppf(P, 1, (z / math.sqrt(n)) ** 2)
    pz = 2 * stats.norm.pdf(z) * w
    f = lambda k: float(np.sum(pz * stats.chi2.sf(nu * r2 / k ** 2, nu))) - g
    return optimize.brentq(f, 0.3, 5000.0, xtol=1e-10)
def tol_ww(n, P, g):
    """The Wald-Wolfowitz approximation, with which the classical tables were worked out."""
    nu = n - 1
    r = math.sqrt(stats.ncx2.ppf(P, 1, 1.0 / n))
    return r * math.sqrt(nu / stats.chi2.ppf(1 - g, nu))
if want('tol'):
    # the page heads each part "P = .90" (.95, .99) and its columns "alpha = .10 .05 .01 .001"
    cells = []; H = None
    for ln in L(186):
        m = re.match(r'\s*P\s*=\s*(\.\d+)\s*$', ln)
        if m: H = float(m.group(1)); continue
        tk = [t for a, b, t in toks(ln)]
        if H and len(tk) == 10 and all(isnum(t) for t in tk):
            for g in (0, 5):
                cells.append((H, int(tk[g]), tk[g + 1:g + 5]))
    al = [0.10, 0.05, 0.01, 0.001]
    read = {'headed': lambda H, j: (H, 1 - al[j]),          # (proportion P, confidence): the book's own definitions
            'exchanged': lambda H, j: (1 - al[j], H)}       # the heading is the confidence, the columns 1 - P
    for nm, fn in read.items():
        for meth, f in (('exact', tol_exact), ('WaldWolf', tol_ww)):
            T = Tally('tolerance_%s_%s' % (nm, meth), 'Tolerance factors, read as ' + nm + ', ' + meth)
            for H, n, vals in cells:
                for j, v in enumerate(vals):
                    P, g = fn(H, j)
                    T.add(186, 'part %.2f n %d' % (H, n), 'col %d' % (j + 1), v, f(n, P, g))
            T.done(show=2)

# ---------------------------------------------------------------- correlation coefficient, rho = 0
if want('corr'):
    T = Tally('correlation_r', 'Percentage points of the correlation coefficient when rho = 0')
    al = None
    for p in (193,):
        for ln in L(p):
            tk = [t for a, b, t in toks(ln)]
            if tk[:2] == ['α', '='] or (tk and tk[0] == 'α='):
                al = [float(t) for t in tk if isnum(t)]; continue
            if al is None: continue
            if tk and tk[0].startswith('ν='): tk = [tk[0][2:]] + tk[1:]
            if tk and tk[0] == 'ν': tk = tk[2:] if len(tk) > 1 and tk[1] == '=' else tk[1:]
            if len(tk) >= 2 and isnum(tk[0]) and '.' not in tk[0]:
                v = int(tk[0]); vals = tk[1:]
                if len(vals) != len(al) or not all(isnum(x) for x in vals):
                    T.note('row df %d not read as plain numbers: %s' % (v, ' '.join(vals))); continue
                for j, x in enumerate(vals):
                    t = stats.t.isf(al[j], v)
                    T.add(p, 'df %d' % v, 'alpha %g' % al[j], x, t / math.sqrt(t * t + v))
    T.done()

# ---------------------------------------------------------------- circular normal probabilities
if want('circ'):
    T = Tally('circular_normal', 'Circular normal probabilities')
    cols = None
    for ln in L(194):
        tk = [t for a, b, t in toks(ln)]
        if tk and tk[0] == 'd/σ': cols = [float(t) for t in tk[1:] if isnum(t)]; continue
        if cols and len(tk) == len(cols) + 1 and all(isnum(t) for t in tk):
            d = float(tk[0])
            for j, x in enumerate(tk[1:]):
                T.add(194, 'd %g' % d, 'R %g' % cols[j], x, stats.ncx2.cdf(cols[j] ** 2, 2, d * d))
    T.done()

# ---------------------------------------------------------------- t over root n, p.209
if want('tn'):
    T = Tally('t_over_root_n', 'Table of t(alpha/2, n-1)/sqrt(n) (p.209)')
    for ln in L(209):
        tk = [t for a, b, t in toks(ln)]
        if len(tk) in (3, 6) and all(isnum(t) for t in tk):
            for g in range(0, len(tk), 3):
                n = int(tk[g])
                T.add(209, 'n %d' % n, '.05', tk[g + 1], stats.t.isf(0.025, n - 1) / math.sqrt(n))
                T.add(209, 'n %d' % n, '.01', tk[g + 2], stats.t.isf(0.005, n - 1) / math.sqrt(n))
    T.done()

# ---------------------------------------------------------------- confidence interval for the median, p.212
if want('med'):
    T = Tally('median_ci', 'Confidence interval for medians: l, u and the actual alpha')
    def best(n, a):
        l = 0
        while 2 * stats.binom.cdf(l, n, 0.5) <= a: l += 1          # l = largest rank with 2 P(B <= l-1) <= a
        return l
    for p in (212, 213):
        hdr = None
        for ln in L(p):
            tk = toks(ln)
            if 'actual' in ln: hdr = [m.start() for m in re.finditer('actual', ln)]; continue
            if hdr is None or not tk or not all(isnum(t) for a, b, t in tk): continue
            n = int(tk[0][2]); rest = tk[1:]
            left = [t for a, b, t in rest if b <= hdr[0] + 16]
            right = [t for a, b, t in rest if b > hdr[0] + 16]
            for nm, grp, a in (('.05', left, 0.05), ('.01', right, 0.01)):
                if len(grp) != 3:
                    if grp: T.note('p%d n %d: %s group read as %s' % (p, n, nm, grp))
                    continue
                l = best(n, a)
                T.add(p, 'n %d' % n, 'l ' + nm, grp[0], l)
                T.add(p, 'n %d' % n, 'u ' + nm, grp[1], n - l + 1)
                T.add(p, 'n %d' % n, 'actual ' + nm, grp[2], 2 * stats.binom.cdf(int(grp[0]) - 1, n, 0.5))
    T.done()

# ---------------------------------------------------------------- confidence limits of proportions
if want('prop'):
    for conf, pr in ((0.95, range(215, 223)), (0.99, range(223, 231))):
        T = Tally('proportion_limits_%d' % round(conf * 100), 'Confidence limits of proportions (coefficient %.2f)' % conf)
        a = 1 - conf; skipped = 0
        for p in pr:
            cols = None; x = None; nline = 0
            for ln in L(p):
                tk = [t for a_, b_, t in toks(ln)]
                if not tk: continue
                if tk[0] == 'x' and len(tk) > 3:
                    cols = tk[1:]; continue
                if cols is None: continue
                if all(isnum(t) and '.' in t for t in tk) and x is not None and nline == 1:
                    vals = tk; kind = 'upper'; nline = 2
                elif (isnum(tk[0]) and '.' not in tk[0]) or tk[0] == '∞':
                    x = tk[0]; vals = tk[1:]; kind = 'lower'; nline = 1
                    if not all(isnum(t) and '.' in t for t in vals): x = None; continue
                else:
                    continue
                if len(vals) != len(cols): skipped += 1; continue
                if x == '∞': continue
                xi = int(x)
                for j, v in enumerate(vals):
                    if cols[j] == '∞': continue
                    n = xi + int(cols[j])
                    if kind == 'lower': tr = 0.0 if xi == 0 else stats.beta.ppf(a / 2, xi, n - xi + 1)
                    else: tr = 1.0 if xi == n else stats.beta.ppf(1 - a / 2, xi + 1, n - xi)
                    T.add(p, 'x %d %s' % (xi, kind), 'n-x %s' % cols[j], v, tr)
        if skipped: T.note('%d lines whose cell count did not match the heading were not read' % skipped)
        T.done()

# ---------------------------------------------------------------- Bessel functions
if want('bessel'):
    T1 = Tally('bessel_JY', 'Bessel functions J0, J1, Y0, Y1'); T2 = Tally('bessel_IK', 'exp(-x) I0, I1 and exp(x) K0, K1')
    for p in range(512, 517):
        txt = '\n'.join(L(p))
        kind = 'J' if 'J0' in txt else ('I' if 'I0' in txt else None)
        if not kind: continue
        for ln in L(p):
            tk = [t for a, b, t in toks(ln)]
            if len(tk) == 5 and isnum(tk[0]) and '.' in tk[0] and sum(isnum(t) for t in tk[1:]) >= 2:
                x = float(tk[0])
                fs = ([special.j0, special.j1, special.y0, special.y1] if kind == 'J' else
                      [special.i0e, special.i1e, special.k0e, special.k1e])
                for j, t in enumerate(tk[1:]):
                    if not isnum(t): continue
                    (T1 if kind == 'J' else T2).add(p, 'x %g' % x, 'f%d' % (j + 1), t, fs[j](x))
    T1.done(); T2.done()

# ---------------------------------------------------------------- beta and gamma functions
if want('beta'):
    T = Tally('beta_function', 'Beta function B(p, q)')
    for p in range(516, 520):
        cols = None
        for ln in L(p):
            tk = [t for a, b, t in toks(ln)]
            if tk[:3] == ['p', 'q', '='] : cols = [float(t) for t in tk[3:]]; continue
            if cols and len(tk) == len(cols) + 1 and all(isnum(t) for t in tk):
                for j, t in enumerate(tk[1:]):
                    T.add(p, 'p %s' % tk[0], 'q %g' % cols[j], t, special.beta(float(tk[0]), cols[j]))
    T.done()
if want('gamma'):
    T = Tally('gamma_function', 'Gamma function')
    for p in range(523, 526):
        if 'Γ(n)' not in '\n'.join(L(p)): continue
        for ln in L(p):
            tk = [t for a, b, t in toks(ln)]
            if len(tk) >= 2 and len(tk) % 2 == 0 and all(isnum(t) for t in tk):
                for g in range(0, len(tk), 2):
                    T.add(p, 'n ' + tk[g], 'Gamma', tk[g + 1], special.gamma(float(tk[g])))
    T.done()
