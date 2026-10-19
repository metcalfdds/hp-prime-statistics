#!/usr/bin/env python3
"""verify_StatDist_v2.7d.py -- checks for StatDist v2.7d (17 Oct 2026, evening): no "=" before a relation,
and the normal approximation's right tail as a lower tail.  Built from verify_StatDist_v2.7c.py: every check
is kept and runs on v2.7d (harness ppl_run_v3d, as before); the help title is v2.7d; 6g keeps comparing the
v2.7c and v2.7b files (that change set).  Part 7 (2.7d) is new:
  7a every display that read "= <": the panel, the Numbers page and the summary, on both versions;
  7b the normal approximation's right tail against SciPy, in doubles and in the Prime's 12 digits
     (NORMALD_CDF rounded to 12 significant digits): v2.7c read "= 0.0000", v2.7d "< 0.0001";
  7c 27 families x 3 tails x 4 settings, and st_ParStr with tiny parameters: v2.7d is v2.7c written
     without "= <", and nothing else;
  7d st_Eq;  7e the Formula page's check lines with the CAS answering;
  7f the exact code-line diff, the new names, the version strings, no comment inside a bracket,
     INSTRING as in v2.7c, at most 6 names per LOCAL;
  7g what was seen and not changed (the 1 - CDF right tail of every family);
  7h no scientific STRING result in any run of v2.7d.
(The v2.7c description follows.)

verify_StatDist_v2.7c.py -- checks for StatDist v2.7c (17 Oct 2026): the two string rules of emulator
round 2 (INSTRING("", ...) is "Invalid input"; STRING(x, 2, d) prints scientific when 0 < |x| < 10^-d).
Built from verify_StatDist_v2.7b.py: every check is kept and now runs in harness v3d, which models both
rules.  Part 5's 5e still compares v2.7b with v2.7a (that change set); Part 6 (2.7c) is new:
  6a st_Cas called directly (and v2.7b's, which stops when the CAS fails);
  6b the Formula page through the soft keys with cas='fail': v2.7c shows "decimal", v2.7b stops;
  6c the replace loop with the CAS answering: Pareto(1, 1)'s CDF (stqx-1)/stqx ends in a replaced name
     and stopped v2.7b's Formula page; every Part 1 answer read through st_FmShow in both versions;
  6d st_Repl on a pattern at the end, at the start, the whole text, an empty pattern, an empty text;
  6e st_fmtx: rounded first, never scientific, never "-0";
  6f the static sweep of STRING(x, 2, d), INSTRING, LEFT, MID and RIGHT;
  6g v2.7c against v2.7b: only st_Cas, st_Repl, st_fmtx and st_show_help differ;
  6h every scientific STRING result (h.sci_strings) of every v2.7c run: none.
(The v2.7b description follows; "v3c" there now means v3d.)

verify_StatDist_v2.7b.py -- checks for StatDist v2.7b (17 Oct 2026): a fractional df for the chi-square and
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
The program files are only read.  Run:  python3 verify_StatDist_v2.7d.py
"""
import math
import os
import signal
import sys
from fractions import Fraction

import sympy as sp
from scipy import stats

sys.path.insert(0, '/home/claude/work/out')
import ppl_run_v3d as R  # noqa: E402
from ppl_run_v3d import Harness, prime_eval, PPLError  # noqa: E402
import re  # noqa: E402

PROG = os.environ.get('STATDIST_V27D', '/home/claude/work/out/StatDist_v2.7d.txt')
V27C = '/home/claude/work/out/StatDist_v2.7c.txt'   # 2.7d
V27B = '/home/claude/work/out/StatDist_v2.7b.txt'
V27A = '/home/claude/work/out/StatDist_v2.7a.txt'
V27 = '/home/claude/work/out/StatDist_v2.7.txt'
OLD = '/home/claude/work/out/StatDist_v2.6.txt'
FAILS = []
NAMES = {}
P1_ANSWERS = []          # 2.7c: every CAS answer Part 1 saw, for 6c

# 2.7c: every harness made in this run is kept, and every scientific STRING result is recorded
# with the routine that printed it (part 6h lists them)
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
        P1_ANSWERS.extend(unwrap(c[0], c[1])[1] for c in calls)
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
    check('page 3, Help: the help pages open (2.7d: the title says v2.7d)',
          any(pg.has('Statistical Distributions v2.7d') for pg in h.pages))
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
    say('== Part 4 (2.7a): v2.7 in harness v3d; the infinity probe; the glyph refusals ==')
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
    check('5a v2.7a in v3d: ChiSquare df 2.5 stops with "Invalid input" (the emulator\'s finding)',
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
    check('5a v2.7a in v3d: F(2.5, 7.5) stops with "Invalid input" too', err is not None and 'Invalid input' in err,
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

    # 5e. v2.7b against v2.7a (2.7c: kept as v2.7b's change set; 6g compares v2.7c with v2.7b)
    import re as _re
    t0, t1 = open(V27A, encoding='utf-8').read(), open(V27B, encoding='utf-8').read()

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


# ---------------------------------------------------------------- part 6 (2.7c)
SCI_E = 'ᴇ'


def _code(path):
    """the file's lines with // comments removed (a // inside a string literal is kept)"""
    out = []
    for l in open(path, encoding='utf-8').read().split('\n'):
        q = False
        cut = len(l)
        for j, ch in enumerate(l):
            if ch == '"':
                q = not q
            elif not q and l[j:j + 2] == '//':
                cut = j
                break
        out.append(l[:cut])
    return out


def _calls(name, code):
    """the argument lists of every NAME( call in one line of code (brackets nested, strings kept)"""
    out = []
    for m in re.finditer(r'(?<![A-Za-z_])' + name + r'\(', code):
        if code[:m.start()].count('"') % 2:
            continue
        j = m.end(); d = 1; cur = ''; parts = []; q = False
        while j < len(code) and d > 0:
            c = code[j]
            if c == '"':
                q = not q
            if not q:
                if c in '([{': d += 1
                elif c in ')]}': d -= 1
            if d == 0:
                break
            if c == ',' and d == 1 and not q:
                parts.append(cur.strip()); cur = ''
            else:
                cur += c
            j += 1
        parts.append(cur.strip())
        out.append(parts)
    return out


def _routines(path):
    """line number -> the routine it lies in"""
    lines = open(path, encoding='utf-8').read().split('\n')
    rt, out = '(file)', {}
    for i, l in enumerate(lines, 1):
        m = re.match(r'^(?:EXPORT\s+)?([A-Za-z]\w*)\(.*\)\s*$', l)
        if m and i < len(lines) and lines[i].strip() == 'BEGIN':
            rt = m.group(1)
        out[i] = rt
    return out


def _formula_run(path, cas, i, **kw):
    """the Formula page through the soft keys (More, More, Formula), as Part 3 opens it"""
    h = harness(cas, path)
    setup(h, i, **kw)
    h.reset_records()
    h.tap(300, 228); h.tap(300, 228); h.tap(20, 228)
    h.press('Enter', 'Enter', 'Enter', 'Enter')
    h.press('Esc')
    err = None
    try:
        h.call('st_Plot')
    except Exception as e:
        err = '%s [%s]' % (e, ' > '.join(getattr(e, 'ppl_stack', []) or []))
    return h, err


def part6():
    say('')
    say('== Part 6 (2.7c): the round-2 string rules, v2.7c against v2.7b, both in harness v3d ==')
    # 6a st_Cas
    h = Harness(PROG, strict=False, cas='giac')
    r = [h.call('st_Cas', s) for s in ('1/2+1/3', '1/0', '0/0', '1/(')]
    check('6a st_Cas (cas=giac): 1/2+1/3 -> %r; 1/0, 0/0 and a syntax error -> %r' % (r[0], r[1:]),
          r == ['5/6', '', '', ''])
    h = Harness(PROG, strict=False, cas='fail')
    try:
        r = h.call('st_Cas', '1/2+1/3'); e = None
    except Exception as x:
        r, e = None, x
    check('6a st_Cas with the CAS failing returns "" and no error', e is None and r == '', '%r %s' % (r, e))
    h = Harness(V27B, strict=False, cas='fail')
    try:
        h.call('st_Cas', '1/2+1/3'); e = None
    except Exception as x:
        e = x
    check('6a v2.7b\'s st_Cas with the CAS failing stops: %s' % (str(e)[:60] if e else 'no error'),
          e is not None and 'INSTRING: Invalid input' in str(e))

    # 6b the Formula page with the CAS failing, through the soft keys: v2.7c completes, v2.7b stops
    for i, kw in ((12, dict(par=[1, 1, 0], x=2)), (3, dict(par=[0.5, 0, 0], x=1.5)), (15, dict(tl=2, par=[20, 0.5, 0], x=10))):
        hn, en = _formula_run(PROG, 'fail', i, **kw)
        ho, eo = _formula_run(V27B, 'fail', i, **kw)
        nm = hn.call('st_Name', float(i))
        fp = [pg for pg in hn.pages if pg.has('the formulas')]
        badge = [t.text for pg in fp for t in pg.texts if t.y == 224 and t.x > 200]
        txt = [t.text for pg in fp for t in pg.texts]
        check('6b %s %s, CAS failing: v2.7c shows the Formula page with "decimal" and "no closed form shown", no error'
              % (nm, kw['par']), en is None and bool(fp) and badge[-1:] == ['decimal']
              and any('no closed form shown' in t for t in txt), '%s %s' % (en, badge[-1:]))
        check('6b %s %s, CAS failing: v2.7b stops: %s' % (nm, kw['par'], (eo or 'no error')[:90]),
              eo is not None and 'INSTRING: Invalid input' in eo and 'st_Cas' in eo)

    # 6c the replace loop with the CAS answering: an answer that ENDS in a name it replaces
    hn, en = _formula_run(PROG, 'giac', 12, par=[1, 1, 0], x=2)
    ho, eo = _formula_run(V27B, 'giac', 12, par=[1, 1, 0], x=2)
    fp = [pg for pg in hn.pages if pg.has('the formulas')]
    txt = [t.text for pg in fp for t in pg.texts]
    badge = [t.text for pg in fp for t in pg.texts if t.y == 224 and t.x > 200]
    ans = [a for e, a, ms in hn.cas_calls if 'stqt' in e and e.startswith('string(simplify(int(')]
    check('6c Pareto(1, 1), CAS answering: the CDF comes back as %s (it ends in stqx); v2.7c shows "  F(x) = (x-1)/x" '
          'with "exact (CAS)", no error' % ans, en is None and '  F(x) = (x-1)/x' in txt and badge[-1:] == ['exact (CAS)'],
          '%s %s' % (en, [t for t in txt if 'F(x)' in t]))
    check('6c the same page in v2.7b stops in st_Repl: %s' % (eo or 'no error')[:100],
          eo is not None and 'INSTRING: Invalid input' in eo and 'st_FmShow > st_Repl' in eo)
    # every answer Part 1's pages showed or rejected, through st_FmShow in both versions
    hn = Harness(PROG, strict=False, cas='giac'); hn.call('st_Init')
    ho = Harness(V27B, strict=False, cas='giac'); ho.call('st_Init')
    ends, bad = 0, []
    names = ('stqx', 'stqt', 'stqk', 'stqa', 'stqb', 'stqc', '*', '+infinity')
    for txt in sorted(set(P1_ANSWERS)):
        if not txt:
            continue
        hit = any(txt.endswith(nm) for nm in names)
        try:
            want = ho.call('st_FmShow', txt); eo = None
        except Exception as x:
            want, eo = None, x
        got = hn.call('st_FmShow', txt)
        ref = txt
        for nm, rp in (('*', '×'), ('+infinity', 'infinity'), ('stqx', 'x'), ('stqt', 't'), ('stqk', 'k')):
            ref = ref.replace(nm, rp)
        if hit:
            ends += 1
            if eo is None or 'INSTRING' not in str(eo):
                bad.append(('v2.7b did not stop', txt))
        elif want != got:
            bad.append(('differs', txt, want, got))
        if not any(n in txt for n in ('stqa', 'stqb', 'stqc')) and got != ref:
            bad.append(('wrong', txt, got, ref))
    check('6c every CAS answer of Part 1 (%d) through st_FmShow: v2.7c reads them all; the %d that END in a name it '
          'replaces stopped v2.7b, the others read as in v2.7b' % (len(set(P1_ANSWERS)), ends), not bad and ends > 0,
          str(bad[:3]))

    # 6d st_Repl itself
    h = Harness(PROG, strict=False, cas='giac')
    ho = Harness(V27B, strict=False, cas='giac')
    cases = [(('(stqx-1)/stqx', 'stqx', 'x'), '(x-1)/x', 'at the end'), (('stqx^2+1', 'stqx', 'x'), 'x^2+1', 'at the start'),
             (('stqa', 'stqa', 'a'), 'a', 'the whole text'), (('abc', '', 'z'), 'abc', 'an empty pattern'),
             (('', 'stqx', 'x'), '', 'an empty text'), (('abc', 'z', 'y'), 'abc', 'no match'),
             (('**', '*', '×'), '××', 'two in a row'), (('a*b', '*', '**'), 'a**b', 'the pattern in the new text')]
    for args, want, what in cases:
        got = h.call('st_Repl', *args)
        old = '(not run: v2.7b loops for ever)' if args[1] == '' else None
        if old is None:
            try:
                old = repr(ho.call('st_Repl', *args))
            except Exception as x:
                old = 'stops: ' + str(x)[:40]
        check('6d st_Repl, %s: %r -> %r (v2.7b: %s)' % (what, args, got, old), got == want)

    # 6e st_fmtx: the rounded value, never scientific
    h = Harness(PROG, strict=False, cas='giac')
    ho = Harness(V27B, strict=False, cas='giac')
    for v, want in ((1e-17, '0'), (-1e-17, '0'), (1e-11, '0'), (2.0, '2'), (1.96, '1.96'), (1 / 3, '0.3333'),
                    (0.0004, '0.0004'), (-2.5, '-2.5'), (123.0, '123'), (0.3, '0.3')):
        got = h.call('st_fmtx', v)
        old = ho.call('st_fmtx', v)
        check('6e st_fmtx(%r) = %r (v2.7b: %r)' % (v, got, old), got == want)
    check('6e v2.7b printed 1E-17 as %r, scientific' % ho.call('st_fmtx', 1e-17), SCI_E in ho.call('st_fmtx', 1e-17))

    # 6f the static sweep
    code = _code(PROG)
    rts = _routines(PROG)
    calls = []
    for i, ln in enumerate(code, 1):
        for a in _calls('STRING', ln):
            if len(a) == 3 and a[1] == '2':
                calls.append((rts[i], a[0], a[2]))
    safe = {
        ('st_fmtp', 'thr', 'dg'): 'st_fmtp: thr = 10^-dg itself',
        ('st_fmtp', 'pv', 'dg'): 'st_fmtp: a value below 10^-dg has already become "< 0.000001"',
        ('st_fmtx', 'fxR', 'fxD'): 'st_fmtx: rounded to fxD decimals first (2.7c)',
        ('st_Int', 'IP(rdV)', '0'): 'a whole number (IP)',
        ('st_Draw', 'dwV', 'dwD'): 'an axis label: a multiple of a 1-2-5 step, d = -FLOOR(LOG(step)), -0 set to 0',
        ('st_Draw', '100*stCut(2)', '1'): 'the "% beyond" note: drawn only when the cut is 0.15 % or more',
        ('st_Draw', '100*stCut(1)', '1'): 'the "% beyond" note: drawn only when the cut is 0.15 % or more',
        ('st_Numbers', 'stBv', '0'): 'k, a or b of a discrete family: whole',
        ('st_Numbers', 'stAv - 1', '0'): 'k, a or b of a discrete family: whole',
        ('st_Numbers', 'stAv', '0'): 'k, a or b of a discrete family: whole',
        ('st_Numbers', 'stXv', '0'): 'k, a or b of a discrete family: whole',
        ('st_Numbers', 'stXv + 1', '0'): 'k, a or b of a discrete family: whole',
        ('st_FmBuild', 'stPar(fbI)', '12'): '12 decimals: only a parameter below 1E-12 (the one form that can show it)',
    }
    keys = sorted(set(calls))
    unknown = [k for k in keys if k not in safe]
    stale = [k for k in safe if k not in keys]
    say('  %d STRING(x, 2, d) calls in v2.7c:' % len(calls))
    for k in keys:
        say('    %-12s %-16s d = %-4s %s' % (k[0], k[1], k[2], safe.get(k, 'NOT LISTED')))
    check('6f every STRING(x, 2, d) is rounded first or cannot print scientific (%d calls; unlisted %s, stale %s)'
          % (len(calls), unknown or 'none', stale or 'none'), not unknown and not stale and len(calls) == 16)
    ins = [(i, ln.strip()) for i, ln in enumerate(code, 1) if 'INSTRING(' in ln]
    say('  INSTRING in v2.7c (code lines):')
    for i, ln in ins:
        say('    %5d %-14s %s' % (i, rts[i], ln[:96]))
    firsts = sorted(set(a[0] for i, ln in ins for a in _calls('INSTRING', ln)))
    check('6f INSTRING\'s first argument is a fixed digit string, or a text tested non-empty just before it: %s' % firsts,
          firsts == ['"0123456789"', '"0123456789/-"', 'cR', 'fgT', 'fsS', 'rpT', 'ivC'] or
          firsts == ['"0123456789"', '"0123456789/-"', 'cR', 'fgT', 'fsS', 'rpT'])
    guarded = all(('IF DIM(rpT) > 0 THEN rpP := INSTRING(rpT, rpO);' in ln) for i, ln in ins if 'INSTRING(rpT' in ln)
    cr = [i for i, ln in ins if 'INSTRING(cR' in ln]
    check('6f st_Repl looks only while text is left (2 lines), st_Cas only inside IF DIM(cR) > 0',
          guarded and len([1 for i, ln in ins if 'INSTRING(rpT' in ln]) == 2 and len(cr) == 1
          and code[cr[0] - 2].strip() == 'IF DIM(cR) > 0 THEN')
    lm = [(rts[i], nm, a) for i, ln in enumerate(code, 1) for nm in ('LEFT', 'MID', 'RIGHT') for a in _calls(nm, ln)]
    say('  LEFT / MID / RIGHT in v2.7c: ' + '; '.join('%s %s(%s)' % (r, n, ', '.join(a)) for r, n, a in lm))
    check('6f no RIGHT; every LEFT count is 1, 2 or guarded (rpP - 1 under IF rpP > 1; wrB >= 1); every MID start '
          'is 1 or more', not any(n == 'RIGHT' for r, n, a in lm)
          and all(a[1] in ('1', '2', 'rpP - 1', 'wrB') for r, n, a in lm if n == 'LEFT')
          and all(a[1] in ('DIM(cR)', '2', 'ivI', 'rpP + rpLn', 'wrI', 'wrB + 1', 'dgI', 'frI') for r, n, a in lm if n == 'MID'))

    # 6g v2.7c against v2.7b
    import re as _re
    t0, t1 = open(V27B, encoding='utf-8').read(), open(V27C, encoding='utf-8').read()   # 2.7d: the two files

    def _bodies(txt):
        c = _re.sub(r'(?ms)^#PYTHON.*?^#END', '', txt)
        c = _re.sub(r'//[^\n]*', '', c)
        out = {}
        for m in _re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, _re.S):
            out[m.group(1)] = _re.sub(r'\n\s*\n', '\n', _re.sub(r'[ \t]+\n', '\n', m.group(0)))
        return out
    B0, B1 = _bodies(t0), _bodies(t1)
    diff = sorted(n for n in set(B0) | set(B1) if B0.get(n) != B1.get(n))
    check('6g routines that differ from v2.7b: %s' % diff, diff == ['st_Cas', 'st_Repl', 'st_fmtx', 'st_show_help'])

    def _outside(t, names):
        c = _re.sub(r'(?ms)^#PYTHON.*?^#END', '', _re.sub(r'//[^\n]*', '', t))
        c = _re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
        return _re.sub(r'\s+', ' ', c)
    check('6g outside those routines only comments differ', _outside(t0, diff) == _outside(t1, diff))
    keep = ['    cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + stS + ")" + CHAR(34) + ")"));',
            '  IF DIM(cR) >= 2 THEN',
            '    IF LEFT(cR, 1) == CHAR(34) AND MID(cR, DIM(cR), 1) == CHAR(34) THEN',
            '      cR := MID(cR, 2, DIM(cR) - 2);']
    check('6g st_Cas keeps the IFERR line and the quote strip byte-identical',
          all(k in t0.split('\n') and k in t1.split('\n') for k in keep))
    check('6g the version reads v2.7c in the banner and the help title; no code line says v2.7b',
          t1.split('\n')[3] == '// STATDIST - v2.7c' and '"Statistical Distributions v2.7c"' in t1
          and not any('v2.7b' in ln for ln in _code(V27C)))

    # 6h every scientific STRING result of every run
    new_h = [x for x in HARNESSES if x.vpath == os.path.basename(PROG)]
    old_h = [x for x in HARNESSES if x.vpath == os.path.basename(V27B)]
    new_s = sorted(set((r, t) for x in new_h for r, t in x.sci_where))
    old_s = sorted(set((r, t) for x in old_h for r, t in x.sci_where))
    say('  v2.7c: %d harness runs in this script, %d scientific STRING results: %s' % (len(new_h), len(new_s), new_s or 'none'))
    say('  v2.7b (part 6, for comparison): %d runs, scientific in %s' % (len(old_h), old_s or 'none'))
    check('6h no scientific STRING result in any of the %d harness runs of v2.7c' % len(new_h), not new_s and len(new_h) > 20)



# ---------------------------------------------------------------- part 7 (2.7d)


def rw27d(s):
    """v2.7c's text written the v2.7d way: "= <" -> "<", "= >" -> ">" (nothing else; "<= <" is a typed x
    below 0.0001 inside "P(X <= ...)", which v2.7d keeps)"""
    return re.sub(r'(?<![<>])= ([<>]) ', r'\1 ', s)


def eqrel(s):
    """an "=" directly before a relation (not the "<=" of "P(X <= ...)")"""
    return re.search(r'(?<![<>])= [<>] ', s) is not None


def _set(h, i, tl=1, par=None, x=None, a=None, b=None, ovn=0):
    setup(h, i, tl=tl, par=par, x=x, a=a, b=b)
    h.globals_['stOvN'] = float(ovn)


def panel_t(path, i, **kw):
    h = harness('fail', path)
    _set(h, i, **kw)
    h.reset_records()
    h.call('st_Panel')
    return [t.text for t in h.texts], h


def numbers_t(path, i, **kw):
    h = harness('fail', path)
    _set(h, i, **kw)
    h.reset_records()
    h.press('Esc', 'Esc', 'Esc', 'Esc')
    h.call('st_Numbers')
    return [t.text for pg in h.pages for t in pg.texts]


def part7():
    _R = R   # the harness this script runs (ppl_run_v3d)
    say('')
    say('== Part 7 (2.7d): no "=" before a relation; the normal approximation\'s right tail ==')
    # 7a. every display that read "= <", reached on both versions
    CASES = [
        ('Normal(0, 1), left tail at -6', 1, dict(tl=1, par=[0, 1, 0], x=-6),
         ['f(x) < 0.0001: a density, not a probability', 'P(X <= -6) < 0.000001'], ['P(X <= -6.0000) < 0.000001']),
        ('Normal(0, 1), right tail at 6', 1, dict(tl=2, par=[0, 1, 0], x=6), ['P(X > 6) < 0.000001'],
         ['P(X > 6.0000) < 0.000001']),
        ('Normal(0, 1), between -7 and -6', 1, dict(tl=3, par=[0, 1, 0], a=-7, b=-6),
         ['f(a) < 0.0001, f(b) < 0.0001: densities', 'P(-7 < X < -6) < 0.000001'],
         ['CDF(b) < 0.000001 at b = -6.0000', 'CDF(a) < 0.000001 at a = -7.0000', 'P(-7.0000 < X < -6.0000) < 0.000001']),
        ('Normal(0, 0.001)', 1, dict(tl=1, par=[0, 0.001, 0], x=0), [], ['variance < 0.0001']),
        ('Normal(0.00002, 0.00005)', 1, dict(tl=1, par=[0.00002, 0.00005, 0], x=0),
         ['μ < 0.0001, σ < 0.0001', 'mean < 0.0001, sd < 0.0001'], ['μ < 0.0001, σ < 0.0001', 'mean < 0.0001,  sd < 0.0001']),
        ('Binomial(100, 0.5), right tail at 95, normal approx. on', 15, dict(tl=2, par=[100, 0.5, 0], x=95, ovn=1),
         ['P(X = 95) < 0.000001: the red bar', 'P(X > 95) = P(X >= 96) < 0.000001', 'normal approx. < 0.0001 (continuity corr.)'],
         ['P(X > 95) = P(X >= 96) < 0.000001']),
        ('Binomial(100, 0.5), left tail at 3, normal approx. on', 15, dict(tl=1, par=[100, 0.5, 0], x=3, ovn=1),
         ['P(X <= 3) < 0.000001', 'normal approx. < 0.0001 (continuity corr.)'], ['P(X <= 3) < 0.000001']),
        ('Binomial(100, 0.5), between 0 and 3', 15, dict(tl=3, par=[100, 0.5, 0], a=0, b=3),
         ['P(X = 0) < 0.0001, P(X = 3) < 0.0001', 'P(0 <= X <= 3) < 0.000001'],
         ['CDF(b) = P(X <= 3) < 0.000001', 'P(0 <= X <= 3) < 0.000001']),
        ('Poisson(4), right tail at 30', 16, dict(tl=2, par=[4, 0, 0], x=30), ['P(X > 30) = P(X >= 31) < 0.000001'],
         ['P(X > 30) = P(X >= 31) < 0.000001']),
        ('Normal(0, 1), x = 0.00005', 1, dict(tl=1, par=[0, 1, 0], x=0.00005), [], ['At x < 0.0001:']),
    ]
    for nm, i, kw, wp, wn in CASES:
        pn, hn = panel_t(PROG, i, **kw)
        po, ho = panel_t(V27C, i, **kw)
        nn, no = numbers_t(PROG, i, **kw), numbers_t(V27C, i, **kw)
        fl = lambda L: [s for s in L if '< 0' in s or '> -0' in s]
        say('  %s\n    v2.7c panel %s numbers %s\n    v2.7d panel %s numbers %s' % (nm, fl(po), fl(no), fl(pn), fl(nn)))
        po = [s.replace('normal approx. = 0.0000 ', 'normal approx. < 0.0001 ') for s in po]   # 7b's change
        check('7a %s: the panel and the Numbers page read %s' % (nm, '; '.join(wp + wn)),
              all(w in pn for w in wp) and all(w in nn for w in wn)
              and [rw27d(s) for s in po] == pn and [rw27d(s) for s in no] == nn
              and not any(eqrel(s) for s in pn + nn) and any(eqrel(s) for s in po + no))
        if nm.startswith('Normal(0, 1), left'):
            check('7a %s: the summary returned to Home (stLast) reads "%s"' % (nm, hn.globals_['stLast']),
                  hn.globals_['stLast'] == 'P(X <= -6) < 0.000001' and ho.globals_['stLast'] == 'P(X <= -6) = < 0.000001')

    # 7b. the normal approximation's right tail: the lower tail at 2 mean - (x + 0.5), against SciPy, and the
    # Prime's 12 digits (NORMALD_CDF rounded to 12 significant digits, the one step that matters)
    _C0 = _R._StatFns.NORMALD_CDF

    def _cdf12(self, a):
        v = _C0(self, a)
        return float('%.12g' % v) if v == v else v
    for digits in (None, 12):
        _R._StatFns.NORMALD_CDF = _cdf12 if digits else _C0
        rows = []
        for n, p, x in ((100, 0.5, 80), (100, 0.5, 85), (100, 0.5, 95), (400, 0.3, 200), (50, 0.4, 45)):
            mu, sd = n * p, (n * p * (1 - p)) ** 0.5
            want = stats.norm.sf(x + 0.5, mu, sd)
            ln = [s for s in panel_t(PROG, 15, tl=2, par=[n, p, 0], x=x, ovn=1)[0] if 'approx' in s]
            lo = [s for s in panel_t(V27C, 15, tl=2, par=[n, p, 0], x=x, ovn=1)[0] if 'approx' in s]
            rows.append((n, p, x, want, lo, ln))
        say('  %s:' % ('the Prime\'s 12 digits' if digits else 'doubles'))
        for n, p, x, want, lo, ln in rows:
            say('    Bin(%d, %.1f), x %d: SciPy %.3g;  v2.7c %s;  v2.7d %s' % (n, p, x, want, lo, ln))
        bad = [r for r in rows if not r[5] or ('< 0.0001' in r[5][0]) != (r[3] < 0.0001)]
        check('7b (%s) the right tail is never shown as 0: v2.7d prints the floor exactly where SciPy\'s tail is '
              'below 0.0001' % ('12 digits' if digits else 'doubles'), not bad, str(bad[:2]))
        zero_old = [r for r in rows if r[4] and '0.0000 ' in r[4][0]]
        say('    v2.7c printed "= 0.0000" for %d of the %d' % (len(zero_old), len(rows)))
        check('7b (%s) v2.7c read "normal approx. = 0.0000" (1 - CDF exactly 0) at %s; v2.7d "< 0.0001" there'
              % ('12 digits' if digits else 'doubles',
                 'Bin(100, 0.5) x 95, Bin(400, 0.3) x 200 and Bin(50, 0.4) x 45' if digits
                 else 'Bin(100, 0.5) x 95 and Bin(400, 0.3) x 200'),
              [(r[0], r[2]) for r in zero_old] == ([(100, 95), (400, 200), (50, 45)] if digits else [(100, 95), (400, 200)]))
    _R._StatFns.NORMALD_CDF = _C0
    h = harness('fail', PROG)
    vals = []
    for (mu, sd, x) in ((50, 5, 55.5), (50, 5, 60.5), (120, 9.17, 151.5), (10, 3, 2.5)):
        g = h.execute('NORMALD_CDF(%r, %r, 2*%r - %r)' % (mu, sd, mu, x))
        vals.append(abs(g - stats.norm.sf(x, mu, sd)) <= 1e-12 * max(1e-300, stats.norm.sf(x, mu, sd)) + 1e-15)
    check('7b NORMALD_CDF(m, s, 2m - x) is the upper tail P(Z > x) (4 cases, against SciPy)', all(vals))

    # 7c. every family, every tail, at its defaults and far out: v2.7d = v2.7c written without "= <"
    n_same = n_rw = 0
    rewrites, bad = set(), []
    for i in range(1, 28):
        hh = harness('fail', PROG)
        d = hh.call('st_Def', float(i))
        x0 = d[3]
        for tl in (1, 2, 3):
            for xm in (None, 'far left', 'far right'):
                kw = dict(tl=tl)
                if xm == 'far left':
                    kw['x'] = x0 - 50 if i not in (15, 16, 17, 26, 27) else 0
                elif xm == 'far right':
                    kw['x'] = x0 + 60
                try:
                    pn, _ = panel_t(PROG, i, **kw)
                    po, _ = panel_t(V27C, i, **kw)
                    nn, no = numbers_t(PROG, i, **kw), numbers_t(V27C, i, **kw)
                except Exception as e:
                    bad.append((i, tl, xm, 'ERR ' + str(e)[:60]))
                    continue
                new, old = pn + nn, po + no
                if new == old:
                    n_same += 1
                elif new == [rw27d(s) for s in old]:
                    n_rw += 1
                    rewrites |= set((o, s) for o, s in zip(old, new) if o != s)
                else:
                    bad.append((i, tl, xm, [(o, s) for o, s in zip(old, new) if rw27d(o) != s][:2]))
    say('  27 families x 3 tails x 3 settings: %d identical, %d differ only by the rewrite, %d otherwise'
        % (n_same, n_rw, len(bad)))
    for o, s in sorted(rewrites)[:10]:
        say('    "%s"  ->  "%s"' % (o, s))
    say('    (%d distinct rewritten lines)' % len(rewrites))
    check('7c every family and tail (%d states): v2.7d\'s panel and Numbers page are v2.7c\'s with "= <" written '
          '"<", and nothing else' % (n_same + n_rw + len(bad)), not bad and n_rw > 0, str(bad[:3]))
    check('7c every rewritten line differs only by "= <" -> "<" or "= >" -> ">", and none in v2.7d reads "= <"',
          all(rw27d(o) == s and not eqrel(s) for o, s in rewrites))
    # st_ParStr, every family, at its defaults and with every non-integer parameter 0.00005
    pb = []
    for i in range(1, 28):
        hh, ho = harness('fail', PROG), harness('fail', V27C)
        d = hh.call('st_Def', float(i))[0:3]
        for pl in (d, [0.00005 if (v != int(v)) else v for v in d]):
            sn, so = hh.call('st_ParStr', float(i), [float(v) for v in pl]), ho.call('st_ParStr', float(i), [float(v) for v in pl])
            if sn != rw27d(so) or eqrel(sn):
                pb.append((i, so, sn))
    check('7c st_ParStr, 27 families, defaults and tiny parameters: v2.7c\'s text written without "= <"', not pb, str(pb[:2]))

    # 7d. st_Eq
    h = harness('fail', PROG)
    for arg, want in (('0.158655', ' = 0.158655'), ('< 0.000001', ' < 0.000001'), ('> -0.000001', ' > -0.000001'),
                      ('', ' = '), ('-1.5', ' = -1.5'), ('undef (no mean)', ' = undef (no mean)')):
        g = h.call('st_Eq', arg)
        check('7d st_Eq("%s") = "%s"' % (arg, g), g == want)

    # 7e. the Formula page's check lines, with the CAS answering
    for nm, i, kw, want in (('Normal(0, 0.0005), variance 2.5E-7', 1, dict(par=[0, 0.0005, 0], x=0), "  < 0.000001, the program's value: agree"),
                            ('Exponential(1), x = 0.00005', 3, dict(par=[1, 0, 0], x=0.00005), '  at x < 0.0001: '),
                            ('Normal(0, 1)', 1, dict(par=[0, 1, 0], x=1), "  = 1.000000, the program's value: agree")):
        got = []
        for path in (PROG, V27C):
            hh = harness('giac', path)
            p, xv, av, bv, calls, lines, badge = formula(hh, i, **kw)
            got.append([t for t, c in lines])
        hit = [s for s in got[0] if want in s]
        say('  7e %s: v2.7d %s' % (nm, hit[:2]))
        say('       v2.7c %s' % [s for s in got[1] if want.strip()[:6] in s or 'agree' in s][:2])
        check('7e %s: the Formula page reads "%s", and is v2.7c\'s written without "= <"' % (nm, want.strip()),
              bool(hit) and [rw27d(s) for s in got[1]] == got[0])

    # 7f. the code
    import difflib
    src_c, src_d = open(V27C, encoding='utf-8').read(), open(PROG, encoding='utf-8').read()
    cc = [l.strip() for l in _code(V27C) if l.strip()]
    cd = [l.strip() for l in _code(PROG) if l.strip()]
    rem, add = [], []
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, cc, cd, autojunk=False).get_opcodes():
        if op != 'equal':
            rem += cc[a1:a2]
            add += cd[b1:b2]
    eq_body = ['st_Eq(eqS)', 'BEGIN', 'IF DIM(eqS) > 0 THEN',
               'IF LEFT(eqS, 1) == "<" OR LEFT(eqS, 1) == ">" THEN RETURN " " + eqS; END;', 'END;',
               'RETURN " = " + eqS;', 'END;']
    # every removed line, rewritten: '<label> = " + X' -> '<label>" + st_Eq(X)'
    def _rewrite(l):
        o = l
        l = re.sub(r' = " \+ (ps[ABC])', r'" + \1', l)
        l = l.replace('psA := st_fmtx(dPl(1)); psB := st_fmtx(dPl(2)); psC := st_fmtx(dPl(3));',
                      'psA := st_Eq(st_fmtx(dPl(1))); psB := st_Eq(st_fmtx(dPl(2))); psC := st_Eq(st_fmtx(dPl(3)));')
        l = l.replace('1 - NORMALD_CDF(stMu, pnZ, stXv + 0.5)', 'NORMALD_CDF(stMu, pnZ, 2*stMu - (stXv + 0.5))')
        l = l.replace('"Statistical Distributions v2.7c"', '"Statistical Distributions v2.7d"')
        l = l.replace('st_FmAdd("  = " + st_fmtv(frV, 6)', 'st_FmAdd(" " + st_Eq(st_fmtv(frV, 6))')
        out, k = '', 0
        while True:
            m = re.compile(r' = " \+ (st_fmtp|st_fmtx|st_fmtv|nuM|nuSd|nuX|pnSd)\b').search(l, k)
            if not m:
                out += l[k:]
                break
            pre = l[k:m.start()]
            # 'P(X = ' + x and 'At k = ' + k: the argument, a whole number, not a value
            if l[:m.start()].rsplit('"', 1)[-1].endswith(('P(X', 'At k')):
                out += l[k:m.end()]
                k = m.end()
                continue
            j = m.end()
            if j < len(l) and l[j] == '(':
                dpt, j = 1, j + 1
                while dpt:
                    dpt += {'(': 1, ')': -1}.get(l[j], 0)
                    j += 1
            out += pre + '" + st_Eq(' + l[m.start() + 7:j] + ')'
            k = j
        return out
    want_add = sorted([_rewrite(l) for l in rem] + eq_body)
    check('7f the code lines removed (%d) and added (%d) are exactly the sites above, through st_Eq, the lower '
          'tail, the help title, and st_Eq itself' % (len(rem), len(add)), sorted(add) == want_add,
          str(sorted(set(add) ^ set(want_add))[:4]))
    names = {w.strip().upper() for w in open('/mnt/user-data/uploads/HP-Prime/HP_Prime_Builtin_Names.txt',
                                             encoding='utf-8') if w.strip()}
    check('7f the new names st_Eq and eqS are not built-ins (ignoring case); st_Eq carries the st_ tag and is '
          'defined once, after st_fmtp and before its first use',
          'ST_EQ' not in names and 'EQS' not in names and src_d.count('\nst_Eq(eqS)\n') == 1
          and src_d.index('\nst_fmtp(pv, dg)') < src_d.index('\nst_Eq(eqS)') < src_d.index('st_Eq(st_'))
    vl = src_d.split('\n')
    check('7f the version reads v2.7d in the banner and the help title, a "WHAT CHANGED in v2.7d" paragraph is '
          'there, and no code line says v2.7c',
          vl[3] == '// STATDIST - v2.7d' and '"Statistical Distributions v2.7d"' in src_d
          and '// WHAT CHANGED in v2.7d (17 Oct 2026, evening)' in src_d
          and not any('v2.7c' in ln for ln in _code(PROG)))
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
    check('7f no // comment inside an open bracket', not badc, str(badc[:5]))
    check('7f INSTRING appears in as many code lines as in v2.7c; every LOCAL line holds at most 6 names',
          sum('INSTRING(' in l for l in cd) == sum('INSTRING(' in l for l in cc)
          and max(len(m.split(',')) for m in re.findall(r'^\s*LOCAL ([^;(]*);', '\n'.join(_code(PROG)), re.M)) <= 6)

    # 7g. seen, not changed (reported): the right tail of every family is 1 - CDF
    pn, _ = panel_t(PROG, 1, tl=2, par=[0, 1, 0], x=10)
    po, _ = panel_t(V27C, 1, tl=2, par=[0, 1, 0], x=10)
    say('  7g seen, not changed: Normal(0, 1), P(X > 10): v2.7c %s, v2.7d %s (1 - CDF, st_Prob; SciPy %.2g)'
        % ([s for s in po if s.startswith('P(')], [s for s in pn if s.startswith('P(')], stats.norm.sf(10)))
    pn, _ = panel_t(PROG, 1, tl=1, par=[0, 1, 0], x=0.00005)
    say('  7g seen, not changed: a typed x of 0.00005 reads %s (no "=" before the relation)'
        % [s for s in pn if s.startswith('P(')])

    # 7h. no scientific STRING result in part 7's runs of v2.7d
    new_h = [x for x in HARNESSES if x.vpath == os.path.basename(PROG)]
    new_s = sorted(set((r, t) for x in new_h for r, t in x.sci_where))
    check('7h no scientific STRING result in any of the %d harness runs of v2.7d in this script' % len(new_h),
          not new_s, str(new_s[:4]))

if __name__ == '__main__':
    part1()
    part2()
    part3()
    part4()
    part5()
    part6()
    part7()
    say('')
    say('RESULT: %s' % ('ALL PASS' if not FAILS else '%d FAILED: %s' % (len(FAILS), FAILS)))
