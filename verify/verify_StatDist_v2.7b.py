#!/usr/bin/env python3
"""verify_StatDist_v2.7b.py -- checks for StatDist v2.7b (17 Oct 2026): a fractional df for the chi-square and
the F distributions (GfxProbe beta 1 T11 on the emulator: CHISQUARE_CDF, CHISQUARE_ICDF, FISHER_CDF and
FISHER_ICDF take whole-number df only), and the shortened INPUT labels.  Built from
verify_StatDist_v2.7a.py: every check is kept and now runs in harness v3c, which raises "Invalid input" for
those four built-ins with a fractional df (and for POISSON_CDF with k < 0), as the emulator did.
Part 5 (2.7b) is new:
  5a the emulator's case end to end: Advanced Continuous -> ChiSquare, df 2.5 -- v2.7a stops with
     "Invalid input", v2.7b shows P(X <= 5) = SciPy's chi2.cdf; the F distribution likewise;
  5b a grid of fractional df: the CDF (st_gammaP, st_betaI), the F density (the formula) and the
     quantiles against SciPy; whole df still use the built-ins, unchanged;
  5c no built-in CDF/ICDF is ever handed a fractional df, POISSON_CDF never a negative k, and no
     F density with a fractional df is asked of FISHER;
  5d no INPUT label is longer than 14 characters; the forms show "df:", "df1:", "df2:" ...;
  5e v2.7b against v2.7a: only the routines named in the CHANGES differ.
(The v2.7a description follows; "v3b" there now means v3c.)

verify_StatDist_v2.7a.py -- checks for StatDist v2.7a (17 Oct 2026): the CAS call form CASProbe beta 1b
found on the emulator, and "no mean" / "no variance" asked as exp(-(integral)) = 0 (the kit now refuses
an infinity).  Built from verify_StatDist_v2.7.py: every check is kept and run in harness v3b, which
models the calculator's CAS (CAS of a variable unevaluated, the Prime's printing -- e^(, the root sign,
the infinity sign -- a CAS string as a PPL string); the SymPy reader takes the Prime's printing.  New
or changed checks are marked "2.7a".


Part 1, every CAS template the program builds, for every family and many parameter sets
  (defaults, other values, moments that do not exist, non-simple parameters that stay
  symbols, the three tails), run through the program in ppl_run_v3 with cas='giac':
  * each CAS answer the page SHOWS is re-evaluated here independently -- Giac's text
    parsed by SymPy, at the user's values -- and compared with SciPy (mean, E[X^2],
    variance, CDF) or exact fractions (discrete): a shown answer that disagrees is a
    FAIL ("never a wrong formula");
  * each answer the page REJECTS is listed with Giac's reason (left undone, wrong);
  * where SymPy can do the same integral quickly, Giac's exact answer is compared with
    SymPy's exactly; discrete answers are compared with Python fractions exactly;
  * the time Giac took.
Part 2, cas='fail': every family shows the program's decimals, "no closed form shown"
  and the "decimal" badge, with no error.
Part 3, the touch and key paths: More, More -> page 3 {Formula, Help, , , Menu, More},
  Formula and Help from it, Enter -> "Formula page (CAS)", the page kept (no CAS call
  the second time), no CAS call in any plot frame or drag, the plot frames identical to
  v2.6's, and the kit's quote stripping.
Part 4 (2.7a): v2.7 in harness v3b (its st_Cas returns its own text: no closed form anywhere), the
  infinity probe on its own, the new glyph refusals in st_FmGood, and v2.7a against v2.7.
The program files are only read.  Run:  python3 verify_StatDist_v2.7a.py
"""
import math
import os
import signal
import sys
from fractions import Fraction

import sympy as sp
from scipy import stats

sys.path.insert(0, '/home/claude/work/out')
import ppl_run_v3c as R  # noqa: E402
from ppl_run_v3c import Harness, prime_eval, PPLError  # noqa: E402
import re  # noqa: E402

PROG = os.environ.get('STATDIST_V27B', '/home/claude/work/out/StatDist_v2.7b.txt')
V27A = '/home/claude/work/out/StatDist_v2.7a.txt'
V27 = '/home/claude/work/out/StatDist_v2.7.txt'
OLD = '/home/claude/work/out/StatDist_v2.6.txt'
FAILS = []
NAMES = {}


def say(*a):
    print(' '.join(str(x) for x in a))


def check(label, ok, extra=''):
    say('  [%s] %s%s' % ('ok' if ok else 'FAIL', label, (' -- ' + extra) if extra else ''))
    if not ok:
        FAILS.append(label)


def dist(i, p):
    a, b, c = p
    return {1: lambda: stats.norm(a, b), 2: lambda: stats.uniform(a, b - a), 3: lambda: stats.expon(scale=1 / a),
            4: lambda: stats.weibull_min(a, scale=b), 5: lambda: stats.lognorm(b, scale=math.exp(a)),
            6: lambda: stats.laplace(a, b), 7: lambda: stats.t(a), 8: lambda: stats.chi2(a),
            9: lambda: stats.f(a, b), 10: lambda: stats.burr12(a, b, scale=c), 11: lambda: stats.gumbel_r(a, b),
            12: lambda: stats.pareto(b, scale=a), 13: lambda: stats.rayleigh(scale=a),
            14: lambda: stats.logistic(a, b), 15: lambda: stats.binom(int(a), b), 16: lambda: stats.poisson(a),
            17: lambda: stats.geom(a), 18: lambda: stats.triang((b - a) / (c - a), loc=a, scale=c - a),
            19: lambda: stats.cauchy(a, b), 20: lambda: stats.invweibull(a, loc=c, scale=b),
            21: lambda: stats.gompertz(a, scale=1 / b), 22: lambda: stats.maxwell(scale=a),
            23: lambda: stats.erlang(int(a), scale=1 / b), 24: lambda: stats.gamma(a, scale=b),
            25: lambda: stats.beta(a, b), 26: lambda: stats.nbinom(int(a), b),
            27: lambda: stats.hypergeom(int(a), int(b), int(c))}[i]()


def ref_moments(i, p):
    """mean, E[X^2], variance from SciPy; None where a moment does not exist."""
    D = dist(i, p)
    # moments that do not exist, by the textbook conditions (SciPy returns inf/nan, and
    # for Frechet alpha in (1, 2] even a negative variance -- noted in v2.6)
    a, b, c = p
    mean_ok = {7: a > 1, 19: False, 12: b > 1, 9: b > 2, 10: a * b > 1, 20: a > 1}.get(i, True)
    var_ok = {7: a > 2, 19: False, 12: b > 2, 9: b > 4, 10: a * b > 2, 20: a > 2}.get(i, True)
    m = float(D.mean()) if mean_ok else None
    v = float(D.var()) if var_ok and mean_ok else None
    if i == 21:   # SciPy's Gompertz moments by quadrature
        m = D.expect(lambda x: x)
        v = D.expect(lambda x: x * x) - m * m
    e2 = (v + m * m) if (m is not None and v is not None) else None
    return m, e2, v


# ---------------------------------------------------------------- SymPy reading of Giac text
SYMS = {n: sp.Symbol(n) for n in ('stqx', 'stqt', 'stqk', 'stqa', 'stqb', 'stqc')}
LOC = dict(SYMS, Gamma=sp.gamma, Beta=sp.beta, ln=sp.log, exp=sp.exp, sqrt=sp.sqrt, pi=sp.pi,
           euler_gamma=sp.EulerGamma, infinity=sp.oo, comb=sp.binomial)


def giac_sym(t):
    # 2.7a: the Prime's printing -- the root sign before an atom or a bracket, e^( for exp,
    # the infinity sign -- read back into SymPy (e is Euler's number)
    t = re.sub('\u221a([A-Za-z_]\\w*|\\d+)', r'sqrt(\1)', t).replace('\u221a(', 'sqrt(')
    t = t.replace('^', '**').replace('+infinity', 'oo').replace('\u221e', 'oo')
    return sp.sympify(t, locals=dict(LOC, e=sp.E))


class Timeout(Exception):
    pass


def _alarm(*_):
    raise Timeout()


def sympy_int(expr_text, var, lo, hi, secs=20):
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(secs)
    try:
        f = giac_sym(expr_text)
        r = sp.integrate(f, (SYMS[var], giac_sym(lo) if lo not in ('-inf', 'inf') else (-sp.oo if lo == '-inf' else sp.oo),
                             giac_sym(hi) if hi not in ('-inf', 'inf') else (-sp.oo if hi == '-inf' else sp.oo)))
        signal.alarm(0)
        if r.has(sp.Integral):
            return None
        return r
    except Timeout:
        return None
    except Exception:
        signal.alarm(0)
        return None


# ---------------------------------------------------------------- the harness
def harness(mode='giac', path=PROG):
    h = Harness(path, strict=False, cas=mode, stall_limit=20000)
    h.call('st_Init')
    return h


def setup(h, i, tl=1, par=None, x=None, a=None, b=None):
    d = h.call('st_Def', float(i))
    if par:
        d[0:3] = [float(v) for v in par]
    if x is not None:
        d[3] = float(x)
    g = h.globals_
    g['stId'] = float(i); g['stTl'] = float(tl)
    g['stPar'] = d[0:3]; g['stXv'] = d[3]
    ab = h.call('st_DefAB', float(i), d[0:3])
    g['stAv'] = float(a) if a is not None else ab[0]
    g['stBv'] = float(b) if b is not None else ab[1]
    g['stDisc'] = h.call('st_Disc', float(i))
    g['stOvN'] = 0.0; g['stOvC'] = 0.0; g['stOvT'] = 0.0
    h.call('st_Clamp'); h.call('st_Fit', 1.0); h.call('st_Cache')
    return [float(v) for v in d[0:3]], g['stXv'], g['stAv'], g['stBv']


def formula(h, i, **kw):
    p, xv, av, bv = setup(h, i, **kw)
    h.reset_records()
    n0 = len(h.cas_calls)
    h.press('Enter', 'Enter', 'Enter', 'Enter')
    h.call('st_Formula')
    calls = h.cas_calls[n0:]
    lines = [(t.text, t.hex) for pg in h.pages if not pg.has('Asking the CAS') for t in pg.texts if 26 <= t.y < 220]
    badge = [t.text for pg in h.pages for t in pg.texts if t.y == 224 and t.x > 200]
    return p, xv, av, bv, calls, lines, badge


def kind(expr):
    """which quantity a 'simplify(...)' CAS call asks for"""
    if 'sum(seq(stqk*(' in expr:
        return 'mean'
    if 'sum(seq(' in expr:
        return 'prob'
    if expr.startswith('simplify((') and ')^2)' in expr and 'int(' not in expr:
        return 'var'
    if 'stqt' in expr:
        return 'cdf'
    if 'int(stqx^2*(' in expr:
        return 'e2'
    if 'int(stqx*(' in expr:
        return 'mean'
    return 'pmf'


def unwrap(e, a):
    """2.7a: the CAS text without the kit's string(...), the answer without its quotes."""
    if e.startswith('string(') and e.endswith(')'):
        e = e[7:-1]
    if len(a) >= 2 and a[0] == '"' and a[-1] == '"':
        a = a[1:-1]
    return e, a


def pairs(calls):
    """(question, answer, check answer or None, ms) for each 'simplify(' call.
    2.7a: the "no mean" / "no variance" question exp(-(simplify(...))) is reported as its
    simplify(...) with the answer '+infinity' when the CAS said 0 (the probe's meaning)."""
    out = []
    calls = [unwrap(e, a) + (ms,) for e, a, ms in calls]
    for j, (e, a, ms) in enumerate(calls):
        if e.startswith('exp(-(simplify(') and e.endswith('))'):
            out.append((e[len('exp(-('):-2], '+infinity' if a == '0' else '(probe) ' + a, None, ms))
            continue
        if e.startswith('simplify('):
            chk = None
            if j + 1 < len(calls) and calls[j + 1][0].startswith('round(evalf('):
                chk = calls[j + 1][1]
            out.append((e, a, chk, ms + (calls[j + 1][2] if chk is not None else 0)))
    return out


def subs_vals(sym_expr, p, sy, xval=None):
    s = {}
    for nm, v, flag in zip(('stqa', 'stqb', 'stqc'), p, sy):
        if flag:
            s[SYMS[nm]] = sp.nsimplify(v) if abs(v - round(v, 12)) < 1e-15 else v
    if xval is not None:
        s[SYMS['stqx']] = xval
    return complex(sp.N(sym_expr.subs(s), 20)).real


PARSETS = []
for i in range(1, 28):
    PARSETS.append((i, {}))
PARSETS += [
    (3, dict(par=[0.5, 0, 0], x=1.5)), (1, dict(par=[100, 15, 0], x=130)), (4, dict(par=[2.5, 3, 0], x=2)),
    (5, dict(par=[0.5, 0.25, 0])), (6, dict(par=[1, 2, 0])), (7, dict(par=[1, 0, 0])), (7, dict(par=[2, 0, 0])),
    (7, dict(par=[5, 0, 0])), (8, dict(par=[3, 0, 0])), (8, dict(par=[2.5, 0, 0])), (9, dict(par=[4, 6, 0])),
    (9, dict(par=[4, 2, 0])), (10, dict(par=[3, 2.5, 2])), (10, dict(par=[1, 1, 1])), (12, dict(par=[5, 1.5, 0], x=6)),
    (12, dict(par=[1, 1, 0], x=2)), (12, dict(par=[2, 2.5, 0], x=3)), (13, dict(par=[2, 0, 0])),
    (14, dict(par=[1, 2, 0])), (18, dict(par=[2, 2, 12])), (18, dict(par=[0, 10, 10])), (19, dict(par=[3, 0.5, 0])),
    (20, dict(par=[1.5, 2, 1])), (22, dict(par=[2, 0, 0])), (23, dict(par=[2, 0.5, 0])), (24, dict(par=[0.5, 1, 0])),
    (24, dict(par=[3, 2, 0])), (25, dict(par=[0.5, 0.5, 0])), (25, dict(par=[0.3, 4, 0])),
    (2, dict(par=[-1.5, 4, 0])), (11, dict(par=[2, 3, 0])),
    # non-simple parameters: they stay symbols
    (3, dict(par=[1 / 3, 0, 0], x=1.5)), (1, dict(par=[2, 1 / 3, 0], x=2)), (4, dict(par=[2, 1 / 3, 0], x=0.2)),
    (12, dict(par=[1, 1 / 3, 0], x=2)), (13, dict(par=[math.pi, 0, 0])), (24, dict(par=[2, 1 / 3, 0])),
    # the discrete families, every tail
    (15, dict(tl=2, par=[20, 0.5, 0], x=10)), (15, dict(tl=3, par=[20, 0.37, 0], a=7, b=12)),
    (15, dict(par=[5, 1 / 3, 0], x=2)), (16, dict(tl=2, par=[5, 0, 0], x=3)), (16, dict(tl=3, par=[2.5, 0, 0], a=1, b=4)),
    (16, dict(par=[1 / 3, 0, 0], x=2)), (17, dict(tl=2, par=[0.3, 0, 0], x=3)), (26, dict(tl=3, par=[3, 0.4, 0], a=1, b=6)),
    (27, dict(tl=2, par=[50, 40, 6], x=5)), (27, dict(par=[1000, 400, 50], x=20)), (15, dict(par=[500, 0.5, 0], x=250)),
    # continuous, other tails (the CDF is then taken at b)
    (3, dict(tl=3, par=[0.5, 0, 0], a=1, b=3)), (12, dict(tl=2, par=[1, 3, 0], x=2)),
]


def part1():
    say('== Part 1: the Formula page, cas = giac, %d parameter sets ==' % len(PARSETS))
    h = harness('giac')
    shown = rejected = wrong = exact_ok = exact_n = 0
    total_ms = 0.0
    slowest = (0, '')
    per_family = {}
    for i, kw in PARSETS:
        p, xv, av, bv, calls, lines, badge = formula(h, i, **kw)
        NAMES[i] = h.call('st_Name', float(i))
        sy = h.globals_['stFmSy']
        tl = int(h.globals_['stTl'])
        disc = i in (15, 16, 17, 26, 27)
        m, e2, v = ref_moments(i, p) if not disc else (float(dist(i, p).mean()), None, None)
        D = dist(i, p)
        ms_all = sum(c[2] for c in calls)
        total_ms += ms_all
        if ms_all > slowest[0]:
            slowest = (ms_all, '%s %s' % (NAMES[i], p))
        tags = []
        g = h.globals_
        for e, a, chk, ms in pairs(calls):
            k = kind(e)
            xx = bv if tl == 3 else xv
            # the reference value of this quantity, from SciPy (independent of the program)
            if disc:
                if k == 'prob':
                    refv = D.cdf(xv) if tl == 1 else (D.sf(xv) if tl == 2 else D.cdf(bv) - D.cdf(av - 1))
                elif k == 'pmf':
                    refv = D.pmf(xv)
                else:
                    refv = m
            else:
                refv = {'mean': m, 'e2': e2, 'var': v, 'cdf': D.cdf(xx) if k == 'cdf' else None}[k]
            # replay the program's own decision: st_FmGood, then its check against its value
            if a.strip() in ('+infinity', 'infinity'):
                tags.append('%s infinite' % k)
                if refv is not None and math.isfinite(refv):
                    wrong += 1
                    tags.append('(WRONG: SciPy has %s)' % refv)
                else:
                    shown += 1
                continue
            good = h.call('st_FmGood', a) == 1
            prog = None
            if k == 'mean':
                prog = g['stMu']
            elif k == 'e2':
                prog = g['stVr'] + g['stMu'] ** 2 if not isinstance(g['stVr'], str) else None
            elif k == 'var':
                prog = g['stVr']
            elif k == 'cdf':
                prog = h.call('st_cdf', float(i), g['stPar'], float(xx))
            elif k == 'prob':
                prog = h.call('st_Prob')
            else:
                prog = h.call('st_pdf', float(i), g['stPar'], float(xv))
            on_page = False
            if good and chk is not None and chk.lstrip('-').isdigit() and not isinstance(prog, str):
                E = h.call('st_Scale', float(prog))
                c = int(chk) / 10 ** E
                on_page = abs(c - prog) <= 1e-6 * max(abs(prog), 1e-9)
            if not on_page:
                rejected += 1
                why = 'left undone' if a and any(w in a for w in ('integrate', 'sum(')) else (
                    'CAS failed' if not a else 'disagreed with the program (%s)' % a[:24])
                tags.append('%s not shown: %s' % (k, why))
                continue
            # SHOWN: judge it independently, Giac's text read by SymPy at the user's values
            try:
                val = subs_vals(giac_sym(a), p, sy, sp.nsimplify(xx) if k == 'cdf' else None)
            except Exception:
                val = None
            ok = val is not None and refv is not None and abs(val - refv) <= 1e-6 * max(abs(refv), 1e-9)
            if ok:
                shown += 1
                tags.append('%s ok' % k)
            else:
                wrong += 1
                tags.append('%s WRONG? %s = %s vs SciPy %s' % (k, a[:30], val, refv))
            # exact comparisons
            if disc and not any(sy):
                fr = exact_discrete(i, p, tl, k, xv, av, bv)
                if fr is not None:
                    exact_n += 1
                    same = (sp.simplify(giac_sym(a) - fr) == 0) if i == 16 else (Fraction(a) == fr)
                    exact_ok += same
                    if not same:
                        tags.append('EXACT MISMATCH')
            if not disc and k in ('mean', 'e2', 'cdf') and not any(sy) and i in SYMPY_OK:
                seg = e[len('simplify('):]
                if seg.startswith('int(') and '+int(' not in seg:
                    parts = split_top(seg[4:seg.rindex(')') - 0].rsplit(')', 0)[0])
                    body = seg[4:]
                    body = body[:body.rindex(')')]
                    body = body[:body.rindex(')')] if body.endswith(')') and body.count('(') < body.count(')') else body
                    parts = split_top(body)
                    if len(parts) == 4:
                        rs = sympy_int(parts[0], parts[1], parts[2], parts[3])
                        if rs is not None:
                            exact_n += 1
                            # equal to 40 digits (SymPy does not always simplify Beta
                            # or Gamma identities, e.g. Gamma(1/5) Gamma(4/5) = pi/sin(pi/5))
                            # (a CDF still holds x: compare at x = 7/5)
                            at = {SYMS['stqx']: sp.Rational(7, 5)}
                            dd = sp.N((giac_sym(a) - rs).subs(at), 40)
                            same = abs(complex(dd)) < 1e-30 * max(1.0, abs(complex(sp.N(rs.subs(at), 40))))
                            exact_ok += same
                            if not same:
                                tags.append('SYMPY MISMATCH %s vs %s' % (a, rs))
        fam = per_family.setdefault(i, [])
        fam.append(tags)
        say('  %-18s %-26s tail %d  badge %-13s %4.0f ms  %s' % (NAMES[i], str([round(v, 4) for v in p]), tl,
            badge[-1] if badge else '?', ms_all, '; '.join(tags) if tags else '(no CAS: %s)' % (
                lines[2][0] if len(lines) > 2 else '')))
    say('')
    check('every CAS answer the page shows agrees with SciPy (no wrong formula)', wrong == 0,
          '%d shown and correct, %d rejected, %d wrong' % (shown, rejected, wrong))
    check('exact comparisons (fractions / SymPy integrals) agree', exact_ok == exact_n, '%d of %d' % (exact_ok, exact_n))
    say('  Giac time over all %d pages: %.1f s; slowest page %.0f ms (%s)' % (len(PARSETS), total_ms / 1000, slowest[0],
                                                                            slowest[1]))


SYMPY_OK = {1, 2, 3, 4, 5, 8, 12, 13, 18, 22, 23, 24, 25}


def split_top(s):
    out, depth, cur = [], 0, ''
    for ch in s:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if ch == ',' and depth == 0:
            out.append(cur)
            cur = ''
        else:
            cur += ch
    out.append(cur)
    return out


def exact_discrete(i, p, tl, k, xv, av, bv):
    a, b, c = p

    def fr(v):
        return Fraction(v).limit_denominator(10 ** 7)

    if i == 15:
        n, q = int(a), fr(b)
        pmf = lambda j: math.comb(n, j) * q ** j * (1 - q) ** (n - j)   # noqa: E731
        lo, hi_all = 0, n
    elif i == 17:
        q = fr(a)
        pmf = lambda j: q * (1 - q) ** (j - 1)                            # noqa: E731
        lo, hi_all = 1, None
    elif i == 26:
        r, q = int(a), fr(b)
        pmf = lambda j: math.comb(j + r - 1, j) * q ** r * (1 - q) ** j   # noqa: E731
        lo, hi_all = 0, None
    elif i == 27:
        N, K, n = int(a), int(b), int(c)
        pmf = lambda j: Fraction(math.comb(K, j) * math.comb(N - K, n - j), math.comb(N, n))   # noqa: E731
        lo, hi_all = max(0, n - (N - K)), min(n, K)
    elif i == 16:
        lam = sp.nsimplify(a)
        pmf = lambda j: sp.exp(-lam) * lam ** j / sp.factorial(j)        # noqa: E731
        lo, hi_all = 0, None
    else:
        return None
    if k == 'pmf':
        return pmf(int(xv))
    if k == 'mean':
        return sum(j * pmf(j) for j in range(lo, hi_all + 1))
    if tl == 3:
        return sum(pmf(j) for j in range(int(av), int(bv) + 1))
    s = sum(pmf(j) for j in range(lo, int(xv) + 1))
    return s if tl == 1 else 1 - s


def part2():
    say('')
    say('== Part 2: cas = fail, all 27 families at their defaults ==')
    h = harness('fail')
    bad = []
    for i in range(1, 28):
        try:
            p, xv, av, bv, calls, lines, badge = formula(h, i)
            txt = [ln for ln, _ in lines]
            ok = badge and badge[-1] == 'decimal' and any('no closed form shown' in t or 'the program' in t for t in txt)
            if not ok:
                bad.append((i, badge, txt[:4]))
        except Exception as ex:
            bad.append((i, repr(ex)[:80]))
    check('all 27: "decimal" badge, the program\'s decimals, no runtime error', not bad, str(bad)[:300])


def part3():
    say('')
    say('== Part 3: the touch and key paths ==')
    h = harness('giac')
    setup(h, 1)
    h.reset_records()
    n0 = len(h.cas_calls)
    # More, More, then Formula (slot 1), a key to leave the page, then Help (slot 2)
    # and three keys through Help, then Menu (slot 5)
    h.tap(300, 228)
    h.tap(300, 228)
    h.tap(20, 228)
    h.press('Enter', 'Enter')
    h.tap(80, 228)
    h.press('Enter', 'Enter', 'Enter', 'Enter')
    h.tap(240, 228)
    h.call('st_Plot')
    menus = [sc.menu for sc in h.screens if sc.menu]
    check('More, More: page 3 is {Formula, Help, , , Menu, More}', ['Formula', 'Help', '', '', 'Menu', 'More'] in menus)
    check('page 2 still {Edit, Numbers, CDF, Refit, Menu, More}', ['Edit', 'Numbers', 'CDF', 'Refit', 'Menu', 'More'] in menus)
    fp = [pg for pg in h.pages if pg.has('the formulas')]
    check('page 3, Formula: the Formula page opens (%d screens) and asks the CAS' % len(fp),
          bool(fp) and len(h.cas_calls) > n0)
    check('page 3, Help: the help pages open (2.7b: the title says v2.7b)',
          any(pg.has('Statistical Distributions v2.7b') for pg in h.pages))
    check('page 3, Menu: leaves the plot', h.error is None)
    # More cycles back to page 1
    h.reset_records()
    setup(h, 1)
    h.tap(300, 228); h.tap(300, 228); h.tap(300, 228)
    h.press('Esc')
    h.call('st_Plot')
    menus = [sc.menu for sc in h.screens if sc.menu]
    check('More three times comes back to page 1', menus[-1] == ['P<=x', 'P>x', 'a<X<b', 'Zoom−', 'Zoom+', 'More'],
          str(menus[-1]))
    # the Enter options: item 2 is the Formula page; the page is kept
    h.reset_records()
    setup(h, 3, par=[0.5, 0, 0], x=1.5)
    h.globals_['stFmK'] = []
    n0 = len(h.cas_calls)
    h.press('Enter')
    h.choose(2)
    h.press('Enter', 'Enter')
    h.press('Enter')
    h.choose(2)
    h.press('Enter', 'Enter')
    h.press('Esc')
    h.call('st_Plot')
    ch = [c for c in h.chooses if c.title == 'Plot options']
    first = [c for c in h.cas_calls[n0:]]
    check('Enter -> "Plot options" item 2 is "Formula page (CAS)"', ch and ch[0].items[1] == 'Formula page (CAS)',
          str(ch[0].items[:3]) if ch else '')
    fp = [pg for pg in h.pages if pg.has('the formulas')]
    check('opened twice from the options: built once (%d CAS calls), shown twice' % len(first),
          len(fp) >= 2 and len(first) == 8)
    # a drag after the Formula page: no CAS call in any frame
    n0 = len(h.cas_calls)
    h.reset_records()
    h.drag([(100, 80), (130, 80), (170, 80), (220, 80)])
    h.press('Esc')
    h.call('st_Plot')
    check('a drag on the plot (%d frames) calls the CAS 0 times' % len(h.pages), len(h.cas_calls) == n0)
    # an edited parameter rebuilds the page
    h.globals_['stPar'] = [0.25, 0.0, 0.0]
    h.call('st_Cache')
    n0 = len(h.cas_calls)
    h.reset_records()
    h.press('Enter', 'Enter', 'Enter')
    h.call('st_Formula')
    check('new parameters: the page is rebuilt (%d CAS calls), mean 4 shown' % (len(h.cas_calls) - n0),
          len(h.cas_calls) > n0 and any(pg.has('  = 4') for pg in h.pages))
    # the plot frames are v2.6's, item for item
    same = True
    for i, kw in ((1, {}), (15, {}), (24, {}), (7, dict(par=[3, 0, 0])), (27, dict(tl=2, par=[50, 40, 6], x=5))):
        frames = []
        for path in (OLD, PROG):
            hh = harness('giac', path)
            setup(hh, i, **kw)
            hh.reset_records()
            hh.call('st_Draw')
            pg = hh.pages[-1]
            menu = [sc.menu for sc in hh.screens if sc.menu]
            frames.append(([(t.text, t.x, t.y, t.hex) for t in pg.texts], [(s.cmd, tuple(s.args)) for s in pg.shapes],
                           menu[-1] if menu else None))
        if frames[0] != frames[1]:
            same = False
            say('    frame differs for id %d' % i)
    check('the plot frame (texts, shapes, soft keys) is identical to v2.6 for 5 distributions', same)
    # the kit's quote stripping (2.7a: the normal path -- the CAS is asked for string(...), the answer
    # is a PPL string, STRING() adds the quotes); undef and (new) an infinity are refused
    hq = Harness(PROG, strict=False, cas={'string(1/2)': '"1/2"', 'string(undef)': '"undef"',
                                         'string(1/0)': '"\u00b1\u221e"', 'string(limit(stqx,stqx,inf))': '"\u221e"'})
    r1 = hq.call('st_Cas', '1/2')
    r2 = hq.call('st_Cas', 'undef')
    r3 = hq.call('st_Cas', '1/0')
    r4 = hq.call('st_Cas', 'limit(stqx,stqx,inf)')
    check('st_Cas drops one surrounding pair of quotes: %r -> %r; "undef" -> %r; 2.7a: the infinity signs -> %r, %r'
          % ('"1/2"', r1, r2, r3, r4), r1 == '1/2' and r2 == '' and r3 == '' and r4 == '')


# ---------------------------------------------------------------- part 4 (2.7a)
def part4():
    say('')
    say('== Part 4 (2.7a): v2.7 in harness v3c; the infinity probe; the glyph refusals ==')
    # v2.7 in v3b: its st_Cas hands back its own text, so every answer fails st_FmGood
    h7 = harness('giac', V27)
    p, xv, av, bv, calls, lines, badge = formula(h7, 3, par=[0.5, 0, 0], x=1.5)
    txt = [ln for ln, _ in lines]
    check('2.7a: v2.7 in v3b shows no closed form (badge %s) -- the emulator\'s finding' % badge[-1:],
          badge[-1:] == ['decimal'] and any('no closed form shown' in t for t in txt)
          and any('non-literal' in w for w in h7.warnings))
    # v2.7a: the same page in v3b, every answer through the kit
    h = harness('giac')
    p, xv, av, bv, calls, lines, badge = formula(h, 3, par=[0.5, 0, 0], x=1.5)
    check('2.7a: Exponential(0.5): exact page, every CAS text asks for string(...), every answer quoted, no CAS '
          'variable assigned, no CAS call of a variable',
          badge[-1:] == ['exact (CAS)'] and all(c[0].startswith('string(') and c[1].startswith('"') for c in calls)
          and not h.cas_vars and not any('non-literal' in w for w in h.warnings))
    # the probe, family by family: "no mean" pages show the CAS line, "mean ok" pages never ask it
    for i, kw, want_m, want_v in ((19, {}, 1, 1), (7, dict(par=[1, 0, 0]), 1, 1), (7, dict(par=[2, 0, 0]), 0, 1),
                                  (9, dict(par=[4, 2, 0]), 1, 1), (10, dict(par=[1, 1, 1]), 1, 1),
                                  (12, dict(par=[1, 1, 0], x=2), 1, 1), (12, dict(par=[5, 1.5, 0], x=6), 0, 1),
                                  (19, dict(par=[3, 0.5, 0]), 1, 1)):
        p, xv, av, bv, calls, lines, badge = formula(h, i, **kw)
        txt = [ln for ln, _ in lines]
        probes = [unwrap(e, a) for e, a, ms in calls if unwrap(e, a)[0].startswith('exp(-(')]
        nm = sum(1 for t in txt if 'So there is NO mean' in t)
        nv = sum(1 for t in txt if 'there is NO variance' in t)
        check('2.7a: %s %s: the probe exp(-(...)) answered %s; "NO mean" %d (want %d), "NO variance" %d (want %d)'
              % (h.call('st_Name', float(i)), p, [a for e, a in probes], nm, want_m, nv, want_v),
              nm == want_m and nv == want_v and all(a == '0' for e, a in probes) and len(probes) == want_m + want_v)
    # the probe's logic in desktop Giac, Prime printing: 0 only for +infinity
    cases = [('simplify(int(stqx*exp(-stqx),stqx,0,inf))', False), ('simplify(int(-stqx/(pi*(1+stqx^2)),stqx,0,inf))', None),
             ('simplify(int(stqx/(pi*(1+stqx^2)),stqx,0,inf))', True), ('simplify(int(stqx/(pi*(1+stqx^2)),stqx,0,1))', False)]
    res = []
    for t, inf in cases:
        a = prime_eval('string(exp(-(%s)))' % t)[1:-1]
        r = h.call('st_FmInf', a) if '\u221e' not in a else 'refused by st_Cas'
        res.append((a, r))
        check('2.7a: exp(-(%s)) = %s -> %s' % (t[:44], a, r),
              (inf is True and r == 1) or (inf is False and r == 0) or (inf is None and r == 'refused by st_Cas'))
    # st_FmGood refuses the glyph forms of an undone integral or sum (not measured on the Prime)
    for g_ in ('\u222b(stqx^2,stqx,0,1)', '\u2211(stqk,stqk,0,5)', '\u03a3(stqk,stqk,0,5)'):
        check('2.7a: st_FmGood refuses %r' % g_, h.call('st_FmGood', g_) == 0)
    check('2.7a: st_FmGood still takes an ordinary closed form', h.call('st_FmGood', '1/2*e^(-1)') == 1)


G_CODE = "\n# ================================================================ G (round 2a)\nsay('\\nG. v2.7a: v2.7 in harness v3b, and v2.7a against v2.7')\nimport re as _re\n_b_old = open(V27, encoding='utf-8').read()\n_b_new = open(PROG, encoding='utf-8').read()\n\n\ndef _bodies(txt):\n    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)\n    c = _re.sub(r'//[^\\n]*', '', c)\n    out = {}\n    for m in _re.finditer(r'(?m)^(?:EXPORT\\s+|LOCAL\\s+)?([A-Za-z]\\w*)\\(([^()\\n]*)\\)\\s*\\nBEGIN\\n.*?^END;', c, _re.S):\n        out[m.group(1)] = _re.sub(r'[ \\t]+\\n', '\\n', m.group(0))\n    return out\n\n\n_B0, _B1 = _bodies(_b_old), _bodies(_b_new)\n_diff = sorted(n for n in set(_B0) | set(_B1) if _B0.get(n) != _B1.get(n))\ncheck(_diff == ['st_Cas', 'st_FmCont', 'st_FmGood', 'st_FmInf', 'st_show_help'], 'v2.7a: routines that differ from v2.7: %s (want st_Cas, st_FmCont, st_FmGood, st_FmInf, st_show_help)' % _diff)\n\n\ndef _outside(t, names):\n    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\\n]*', '', t))\n    if names:\n        c = _re.sub(r'(?ms)^(?:EXPORT\\s+|LOCAL\\s+)?(?:%s)\\([^\\n]*\\)\\s*\\nBEGIN\\n.*?^END;' % '|'.join(names), '', c)\n    return _re.sub(r'\\s+', ' ', c)\n\n\ncheck(_outside(_b_old, _diff) == _outside(_b_new, _diff), 'v2.7a: outside those routines only comments differ')\n_py0 = _re.findall(r'(?s)#PYTHON.*?#END', _b_old)\n_py1 = _re.findall(r'(?s)#PYTHON.*?#END', _b_new)\ncheck(_py0 == _py1, 'v2.7a: the #PYTHON blocks are unchanged')\nsay('  routines that differ from v2.7: %s; everything else differs only in comments' % ', '.join(_diff))\n"


# ---------------------------------------------------------------- part 5 (2.7b)
def part5():
    say('')
    say('== Part 5 (2.7b): a fractional df for the chi-square and F; the INPUT labels ==')

    # 5a. the emulator's case, end to end
    def run(path, dist, tail, ans):
        h = Harness(path, strict=False, cas='fail', idle_key=4, stall_limit=20000)
        h.choose('Advanced Continuous'); h.choose(dist); h.choose(tail); h.answer(ans)
        h.choose('Exit')
        try:
            r = h.call('StatDist')
            return h, r, None
        except PPLError as e:
            return h, None, str(e)
    h, r, err = run(V27A, 'ChiSquare', 'Lower tail', {'df': 2.5, 'x_val': 5})
    check('5a v2.7a in v3c: ChiSquare df 2.5 stops with "Invalid input" (the emulator\'s finding)',
          err is not None and 'Invalid input' in err, str(err)[:120])
    h, r, err = run(PROG, 'ChiSquare', 'Lower tail', {'df': 2.5, 'x_val': 5})
    want = stats.chi2.cdf(5, 2.5)
    check('5a v2.7b: ChiSquare df 2.5, P(X <= 5) = %.6f (SciPy %.6f), no error' % (want, want),
          err is None and r == 'StatDist: P(X <= 5) = %.6f' % want, '%s %s' % (r, err))
    pg = [p for p in h.pages if any('P(X <= 5' in t.text for t in p.texts)]
    check('5a v2.7b: the plot is drawn (the shaded tail and the P readout)', bool(pg), str(len(h.pages)))
    h, r, err = run(PROG, 'ChiSquare', 'Upper tail', {'df': 2.5, 'x_val': 5})
    check('5a v2.7b: ChiSquare df 2.5, P(X > 5) = %.6f' % stats.chi2.sf(5, 2.5),
          err is None and r == 'StatDist: P(X > 5) = %.6f' % stats.chi2.sf(5, 2.5), '%s %s' % (r, err))
    h, r, err = run(V27A, 'Fisher F', 'Lower tail', {'df1': 2.5, 'df2': 7.5, 'x_val': 2})
    check('5a v2.7a in v3c: F(2.5, 7.5) stops with "Invalid input" too', err is not None and 'Invalid input' in err,
          str(err)[:120])
    h, r, err = run(PROG, 'Fisher F', 'Lower tail', {'df1': 2.5, 'df2': 7.5, 'x_val': 2})
    want = stats.f.cdf(2, 2.5, 7.5)
    check('5a v2.7b: F(2.5, 7.5), P(X <= 2) = %.6f (SciPy; the emulator table: 0.80043)' % want,
          err is None and r == 'StatDist: P(X <= 2) = %.6f' % want, '%s %s' % (r, err))
    h, r, err = run(PROG, 'Fisher F', 'Between: P(a < X < b)', {'df1': 4, 'df2': 2.5})
    m = re.search(r'P\(([\d.]+) < X < ([\d.]+)\) = ([\d.]+)', r or '')
    ok = m and abs(float(m.group(3)) - (stats.f.cdf(float(m.group(2)), 4, 2.5) - stats.f.cdf(float(m.group(1)), 4, 2.5))) < 2e-6
    check('5a v2.7b: F(4, 2.5) Between at its default bounds (one df whole, one not) = SciPy: %s' % r,
          err is None and bool(ok), str(err)[:120])
    # whole df: the built-ins, as before
    h, r, err = run(PROG, 'ChiSquare', 'Lower tail', {'df': 4, 'x_val': 5})
    calls = {c[0] for c in h.stat_calls}
    check('5a v2.7b: a whole df still uses CHISQUARE_CDF (the emulator\'s Chi-square(4): 0.712703)',
          r == 'StatDist: P(X <= 5) = 0.712703' and 'CHISQUARE_CDF' in calls, '%s %s' % (r, sorted(calls)))

    # 5b. a grid of fractional df, the program's own routines against SciPy
    h = harness('fail')
    worst = {'chi cdf': 0, 'F cdf': 0, 'F pdf': 0, 'chi q': 0, 'F q': 0, 'chi pdf': 0}
    for df in (0.5, 1.5, 2.5, 3.7, 10.25, 50.5, 0.1):
        for x in (0.05, 0.5, 1, 2.5, 5, 20, 60, 150):
            v = h.call('st_cdf', 8.0, [df, 0.0, 0.0], float(x))
            worst['chi cdf'] = max(worst['chi cdf'], abs(v - stats.chi2.cdf(x, df)))
            d = h.call('st_pdf', 8.0, [df, 0.0, 0.0], float(x))
            worst['chi pdf'] = max(worst['chi pdf'], abs(d - stats.chi2.pdf(x, df)) / max(1e-300, stats.chi2.pdf(x, df)))
        for q in (0.01, 0.25, 0.5, 0.9, 0.995):
            v = h.call('st_icdf', 8.0, [df, 0.0, 0.0], float(q))
            # st_icdf only fits the plot window (st_Fit: the 0.001, 0.25, 0.75, 0.999 points), so an
            # absolute-plus-relative error is the fair measure (df 0.1: the 1 % point is about 1E-40)
            worst['chi q'] = max(worst['chi q'], abs(v - stats.chi2.ppf(q, df)) / (1 + stats.chi2.ppf(q, df)))
    for d1, d2 in ((0.5, 3.5), (2.5, 7.5), (1, 2.5), (10.5, 1), (30.25, 40.75), (3.3, 12), (6, 0.8)):
        for x in (0.05, 0.5, 1, 2, 3, 10, 40):
            v = h.call('st_cdf', 9.0, [float(d1), float(d2), 0.0], float(x))
            worst['F cdf'] = max(worst['F cdf'], abs(v - stats.f.cdf(x, d1, d2)))
            d = h.call('st_pdf', 9.0, [float(d1), float(d2), 0.0], float(x))
            worst['F pdf'] = max(worst['F pdf'], abs(d - stats.f.pdf(x, d1, d2)) / stats.f.pdf(x, d1, d2))
        for q in (0.05, 0.5, 0.9, 0.99):
            v = h.call('st_icdf', 9.0, [float(d1), float(d2), 0.0], float(q))
            worst['F q'] = max(worst['F q'], abs(v - stats.f.ppf(q, d1, d2)) / (1 + stats.f.ppf(q, d1, d2)))
    check('5b chi-square, 7 fractional df x 8 x: CDF = SciPy chi2.cdf within 1E-9 (%.1e)' % worst['chi cdf'],
          worst['chi cdf'] < 1e-9)
    check('5b chi-square, fractional df: the density (the built-in, which takes any df) = SciPy (rel %.1e)'
          % worst['chi pdf'], worst['chi pdf'] < 1e-9)
    check('5b chi-square, fractional df: the quantile (bisection on the new CDF; it fits the window) = chi2.ppf, '
          '|error| / (1 + x) %.1e' % worst['chi q'], worst['chi q'] < 1e-6)
    check('5b F, 7 df pairs (one or both fractional) x 7 x: CDF = SciPy f.cdf within 1E-9 (%.1e)' % worst['F cdf'],
          worst['F cdf'] < 1e-9)
    check('5b F, fractional df: the density by the formula = SciPy f.pdf, rel %.1e' % worst['F pdf'], worst['F pdf'] < 1e-9)
    check('5b F, fractional df: the quantile (bisection, as before) = f.ppf, |error| / (1 + x) %.1e' % worst['F q'],
          worst['F q'] < 1e-6)
    say('  worst: ' + ', '.join('%s %.1e' % kv for kv in worst.items()))
    # 5c. what the built-ins were handed in all of that
    bad = [c for c in h.stat_calls if c[0] in ('CHISQUARE_CDF', 'CHISQUARE_ICDF', 'FISHER_CDF', 'FISHER_ICDF', 'FISHER')
           and any(float(v) != int(v) for v in (c[1][:1] if c[0].startswith('CHI') else c[1][:2]))]
    check('5c no CHISQUARE_CDF/_ICDF, FISHER_CDF/_ICDF or FISHER density call with a fractional df (%d calls checked)'
          % len(h.stat_calls), not bad, str(bad[:3]))
    check('5c no warning about an unmeasured fractional-df F density', not any('fractional df was not measured' in w
                                                                                for w in h.warnings))
    # the whole plot path for a fractional df: Fit, Cache, every tail and the Formula page's decimals
    hp = harness('fail')
    errs = []
    for i, par in ((8, (2.5, 0, 0)), (8, (0.7, 0, 0)), (9, (2.5, 7.5, 0)), (9, (1, 2.5, 0)), (9, (5.5, 3, 0))):
        for tl in (1, 2, 3):
            try:
                setup(hp, i, tl=tl, par=par)
                hp.call('st_Draw')
                hp.call('st_Numbers') if False else None
            except Exception as e:
                errs.append((i, par, tl, repr(e)[:80]))
    check('5c the plot (fit, cache, all three tails) for 5 fractional-df cases: no error', not errs, str(errs[:2]))
    # Erlang and Maxwell keep whole df; Poisson never asks for k < 0
    he = harness('fail')
    setup(he, 23, tl=1, par=(3, 1.5, 0), x=2)
    v = he.call('st_cdf', 23.0, [3.0, 1.5, 0.0], 2.0)
    check('5c Erlang(3, 1.5): CHISQUARE_CDF(6, ...) = SciPy erlang.cdf (%.6f)' % v,
          abs(v - stats.erlang.cdf(2, 3, scale=1 / 1.5)) < 1e-9)
    hpz = harness('fail')
    p0, xv, av, bv = setup(hpz, 16, tl=3, par=(4, 0, 0), a=0, b=5)
    pr = hpz.call('st_Prob')
    check('5c Poisson(4) Between 0 and 5: %.6f = SciPy, no POISSON_CDF(4, -1) (v3c would raise)' % pr,
          abs(pr - stats.poisson.cdf(5, 4)) < 1e-9 and not any(c[0] == 'POISSON_CDF' and c[1][1] < 0
                                                                for c in hpz.stat_calls))

    # 5d. the INPUT labels
    src = re.sub(r'//[^\n]*', '', open(PROG, encoding='utf-8').read())      # code only, not comments
    labs = []
    for m in re.finditer(r'INPUT\(\{[^}]*\},\s*"[^"]*",\s*\{([^}]*)\}', src):
        labs += re.findall(r'"([^"]*)"', m.group(1))
    longest = max(labs, key=len)
    check('5d no INPUT label is longer than 14 characters (%d labels; the longest: "%s", %d)' % (len(labs), longest, len(longest)),
          len(longest) <= 14)
    check('5d "Degrees of freedom:", "Denominator df:", "K (positives in N):" are gone',
          not any(x in src for x in ('"Degrees of freedom:"', '"Denominator df:"', '"K (positives in N):"',
                                     '"k (positives drawn):"', '"N (population):"', '"Scale (gamma):"')))
    h, r, err = run(PROG, 'ChiSquare', 'Lower tail', {'df': 3, 'x_val': 2})
    check('5d the chi-square form reads "df:" and "X value:"', h.inputs and h.inputs[0].labels == ['df:', 'X value:'],
          str(h.inputs[0].labels if h.inputs else None))
    h, r, err = run(PROG, 'Fisher F', 'Lower tail', {'df1': 3, 'df2': 9, 'x_val': 2})
    check('5d the F form reads "df1:", "df2:" with "Numerator df > 0", "Denominator df > 0" under them',
          h.inputs and h.inputs[0].labels == ['df1:', 'df2:', 'X value:']
          and h.inputs[0].helps[:2] == ['Numerator df > 0', 'Denominator df > 0'], str(h.inputs[0].labels if h.inputs else None))

    # 5e. v2.7b against v2.7a
    import re as _re
    t0, t1 = open(V27A, encoding='utf-8').read(), open(PROG, encoding='utf-8').read()

    def _bodies(txt):
        c = _re.sub(r'(?ms)^#PYTHON.*?^#END', '', txt)
        c = _re.sub(r'//[^\n]*', '', c)
        out = {}
        for m in _re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, _re.S):
            out[m.group(1)] = _re.sub(r'\n\s*\n', '\n', _re.sub(r'[ \t]+\n', '\n', m.group(0)))
        return out
    B0, B1 = _bodies(t0), _bodies(t1)
    diff = sorted(n for n in set(B0) | set(B1) if B0.get(n) != B1.get(n))
    want = ['st_ask_cauchy', 'st_ask_chisquare', 'st_ask_fisher', 'st_ask_hypergeom', 'st_ask_student', 'st_cdf',
            'st_pdf', 'st_show_help']
    check('5e routines that differ from v2.7a: %s' % diff, diff == want, 'want %s' % want)

    def _outside(t, names):
        c = _re.sub(r'(?ms)^#PYTHON.*?^#END', '', _re.sub(r'//[^\n]*', '', t))
        c = _re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
        return _re.sub(r'\s+', ' ', c)
    check('5e outside those routines only comments differ', _outside(t0, diff) == _outside(t1, diff))
    check('5e the #PYTHON blocks (if any) are unchanged',
          _re.findall(r'(?ms)^#PYTHON.*?^#END', t0) == _re.findall(r'(?ms)^#PYTHON.*?^#END', t1))
    check('5e st_Cas (the CAS call form) is byte-identical to v2.7a', B0['st_Cas'] == B1['st_Cas'])


if __name__ == '__main__':
    part1()
    part2()
    part3()
    part4()
    part5()
    say('')
    say('RESULT: %s' % ('ALL PASS' if not FAILS else '%d FAILED: %s' % (len(FAILS), FAILS)))
