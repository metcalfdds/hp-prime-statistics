#!/usr/bin/env python3
"""verify_ErrorRate_beta1a.py -- checks for ErrorRate Lab beta 1a (HP Prime PPL + MicroPython + CAS),
17 Oct 2026: the CAS call form CASProbe beta 1b found on the emulator.  Built from verify_ErrorRate.py
(beta 1): every check is kept and run in harness v3b, which models the calculator's CAS (CAS of a
variable unevaluated, the Prime's printing -- e^( for exp, the root sign -- a CAS string as a PPL
string); C reads the program's answers in the Prime's printing; G (new) runs beta 1 itself in v3b
and compares beta 1a with beta 1.  New or changed checks are marked "1a".

  A. The statistics, run through the PROGRAM'S OWN routines in the ppl_run_v3 harness and
     compared with SciPy / statsmodels:
       erlBound (upper bound; k = 0 closed form, k > 0 bisection on BINOMIAL_CDF) against
       beta.ppf(1 - alpha, k + 1, n - k) and proportion_confint(k, n, alpha = 2 alpha,
       method = 'beta') -- the TWO-sided interval at level 1 - 2 alpha has the one-sided
       bound as its upper end; erlTail; erlRuleC (Poisson / chi-square); erlLnGam;
       erlBetaCdf / erlBetaQ (Bayes, via the F relation); the posterior densities;
       erlTrP (trawl); the window fit.
  B. Every number quoted on the help pages and in the header comments, recomputed.
  C. Every CAS template the program can build, for representative and edge inputs, sent
     through desktop Giac 1.9 (icas) exactly as built by the program, and Giac's answer
     compared with SymPy / fractions; plus the display transform (erlShow).
  D. The #PYTHON block under CPython with stub hpprime / urandom modules: the 44-value
     payload, the stage marks, and the counts against Binomial(n, p).
  E. The program end to end in the harness, four ways: CAS by Giac and Python working;
     CAS failing (cas='fail') and Python absent; Python stopping part-way; and a k > 0
     session.  Layout: nothing below y 218 on a soft-key page, no text-page line over 46
     characters, no MSGBOX over 5 lines.

  G. 1a: beta 1 in harness v3b (its erlCas returns its own text, which the pages would show as the
     CAS's answers), and beta 1a against beta 1 (erlCas and the Engines page's text differ).

Run:  python3 verify_ErrorRate_beta1a.py   (SciPy, statsmodels, SymPy, desktop Giac; reads files only)
"""
import sys, os, re, math, types, random as pyrandom
from fractions import Fraction
from scipy import stats, special
from statsmodels.stats.proportion import proportion_confint
import sympy as sp

sys.path.insert(0, '/home/claude/work/harness')
from ppl_run_v3b import Harness, ACCEPT, giac_eval  # noqa: E402

SRC = '/home/claude/work/out/ErrorRate_beta1a.txt'
BETA1 = '/home/claude/work/out/ErrorRate_beta1.txt'
FAILS = []


def check(cond, msg):
    print(('PASS ' if cond else 'FAIL ') + msg)
    if not cond:
        FAILS.append(msg)


def fresh(cas='giac', seed=1):
    h = Harness(SRC, cas=cas, seed=seed)
    h.call('erlInit')
    return h


def g(h, name):
    return h.globals_[name]


def setrec(h, n, k, am):
    h.globals_['erlN'] = float(n); h.globals_['erlK'] = float(k); h.globals_['erlAm'] = float(am)
    h.call('erlRecalc')


# ============================================================================ A
print('== A. statistics: the program\'s routines against SciPy / statsmodels ==')
h = fresh()
worst = 0.0
cases = 0
for am in (50, 10, 25, 100, 1, 500):
    a = am / 1000
    for n in (1, 2, 5, 10, 25, 30, 100, 1000, 10000):
        for k in (0, 1, 2, 3, 5, 10):
            if k > n:
                continue
            pu = h.call('erlBound', float(n), float(k), a)
            if k == n:
                ref = 1.0
            else:
                ref = stats.beta.ppf(1 - a, k + 1, n - k)
                sm = proportion_confint(k, n, alpha=2 * a, method='beta')[1]
                worst = max(worst, abs(sm - ref))
            worst = max(worst, abs(pu - ref))
            cases += 1
check(worst < 1e-10, 'erlBound = beta.ppf(1-a, k+1, n-k) = statsmodels beta upper (alpha = 2a), '
      '%d cases, worst |diff| %.1e' % (cases, worst))
for n, want in ((10, 0.2588655508930523), (25, 0.11292814500684323), (100, 0.029513049607039932)):
    pu = h.call('erlBound', float(n), 0.0, 0.05)
    check(abs(pu - want) < 1e-12, 'PCAST examples: 0 errors in %d -> %.4f (PCAST: %s)'
          % (n, pu, {10: '26 percent', 25: 'roughly 1 in 9', 100: '3.0 percent'}[n]))
# the k = 0 closed form agrees with the bisection the program uses for k > 0
lo, hi = 0.0, 1.0
for _ in range(45):
    m = (lo + hi) / 2
    if stats.binom.cdf(0, 30, m) > 0.05: lo = m
    else: hi = m
check(abs((lo + hi) / 2 - (1 - 0.05 ** (1 / 30))) < 1e-12,
      'k = 0: bisection on the binomial CDF gives 1 - 0.05^(1/30) too')

worst = 0.0
for n, p, k in ((30, 0.05, 0), (30, 0.2, 2), (1000, 0.003, 0), (100, 0.07, 5), (10, 0.5, 9), (5000, 0.001, 3)):
    v = h.call('erlTail', float(n), p, float(k))
    worst = max(worst, abs(v - stats.binom.cdf(k, n, p)))
check(worst < 1e-12, 'erlTail = binom.cdf (k = 0 written as (1-p)^n), worst %.1e' % worst)
check(h.call('erlTail', 30.0, 0.0, 0.0) == 1 and h.call('erlTail', 30.0, 1.0, 2.0) == 0,
      'erlTail edges: p = 0 -> 1, p = 1 -> 0 (no BINOMIAL_CDF at the ends)')

worst = 0.0
for k in range(0, 8):
    for a in (0.05, 0.01, 0.1, 0.025):
        r = h.call('erlRuleC', float(k), a)
        ref = -math.log(a) if k == 0 else stats.chi2.ppf(1 - a, 2 * k + 2) / 2
        pois = stats.poisson.cdf(k, ref)
        worst = max(worst, abs(r - ref), abs(pois - a))
check(worst < 1e-9, 'erlRuleC: P(Poisson(mu) <= k) = alpha at mu = chi2.ppf(1-a, 2k+2)/2 (k = 0: -ln a)')
print('   Poisson rules at alpha 0.05: ' + ', '.join('k=%d %.4f' % (k, h.call('erlRuleC', float(k), 0.05))
                                                    for k in range(6)))

worst = 0.0
for v in (0.5, 1, 1.5, 2.5, 10.5, 31, 61.5, 1000.5, 10001):
    worst = max(worst, abs(h.call('erlLnGam', float(v)) - special.gammaln(v)) / max(1, abs(special.gammaln(v))))
check(worst < 1e-9, 'erlLnGam (Lanczos) = gammaln, worst relative %.1e' % worst)

worst = 0.0
for a2, b2, x in ((2, 62, 0.05), (1, 61, 0.02), (21, 41, 0.3), (5, 2001, 0.003), (1, 1, 0.9), (200, 3, 0.97)):
    worst = max(worst, abs(h.call('erlBetaCdf', float(a2), float(b2), x) - stats.beta.cdf(x, a2 / 2, b2 / 2)))
check(worst < 1e-10, 'erlBetaCdf = beta.cdf via FISHER_CDF(2a, 2b, b x/(a(1-x))), worst %.1e' % worst)
worst = 0.0
for a2, b2, q in ((2, 62, 0.95), (1, 61, 0.95), (5, 57, 0.99), (1, 2001, 0.95), (41, 21, 0.9)):
    worst = max(worst, abs(h.call('erlBetaQ', float(a2), float(b2), q) - stats.beta.ppf(q, a2 / 2, b2 / 2)))
check(worst < 1e-12, 'erlBetaQ = beta.ppf (50 halvings), worst %.1e' % worst)

# Bayes on the default record: uniform and Jeffreys
setrec(h, 30, 0, 50)
h.call('erlFit', 0.0)
for a2, b2, name in ((2, 2, 'uniform'), (1, 1, 'Jeffreys')):
    h.globals_['erlBa2'] = float(a2); h.globals_['erlBb2'] = float(b2)
    h.call('erlBayesCalc')
    A, B = a2 / 2, b2 / 2 + 30
    check(abs(g(h, 'erlBMean') - A / (A + B)) < 1e-15 and abs(g(h, 'erlBUp') - stats.beta.ppf(0.95, A, B)) < 1e-12,
          '%s prior, 0 of 30: mean %s = %.5f, 95 %% credible bound %.5f (SciPy %.5f); CAS fraction %r'
          % (name, Fraction(a2, a2 + b2 + 60), g(h, 'erlBMean'), g(h, 'erlBUp'), stats.beta.ppf(0.95, A, B), g(h, 'erlCaB')))
    bmax = g(h, 'erlBMax'); W = g(h, 'erlPW')
    i = 40
    x = bmax * (i + 0.5) / (W + 1)
    check(abs(g(h, 'erlBD')[i] - stats.beta.pdf(x, A, B)) < 1e-9 * max(1, stats.beta.pdf(x, A, B)),
          '   posterior density at column 41 = beta.pdf (%.6f)' % stats.beta.pdf(x, A, B))
p0 = 0.05
check(abs((1 - stats.beta.cdf(p0, 1, 31)) - 0.95 ** 31) < 1e-12,
      'uniform prior, 0 of 30: P(rate > 5 %%) = 0.95^31 = %.4f (the Bayes page line)' % 0.95 ** 31)
check(abs(stats.beta.ppf(0.95, 1, 31) - (1 - 0.05 ** (1 / 31))) < 1e-12,
      'uniform-prior bound for 0 of n = Clopper-Pearson bound for 0 of n + 1 (1 - 0.05^(1/31))')

# the trawl: 1 - (1 - r)^N, against log1p / expm1
worst = 0.0
for m in range(3, 10):
    h.globals_['erlTm'] = float(m)
    r = 10.0 ** -m
    for N in (1, 7, 100, 12345, 10 ** 6, 3 * 10 ** 7, 10 ** 8):
        exact = -math.expm1(N * math.log1p(-r))
        worst = max(worst, abs(h.call('erlTrP', float(N)) - exact) / exact)
check(worst < 1e-9, 'erlTrP = -expm1(N log1p(-RMP)) for RMP 1E-3..1E-9, N 1..1E8, worst relative %.1e' % worst)
h.globals_['erlTm'] = 6.0
print('   RMP 1E-6: N = 1E6 -> P = %.6f (1 - 1/e = %.6f); half-way N = %.0f'
      % (h.call('erlTrP', 1e6), 1 - math.exp(-1), math.log(2) / -math.log1p(-1e-6)))

# the window fit
for n, k, want in ((30, 0, 0.2), (10, 0, 1.0), (100, 0, 0.1), (1000, 0, 0.01), (30, 2, 0.5), (5, 0, 1.0), (300, 0, 0.02)):
    setrec(h, n, k, 50)
    h.globals_['erlP0'] = 0.0
    h.call('erlFit', 0.0)
    check(abs(g(h, 'erlPmax') - want) < 1e-12, 'window for %d errors in %d: 0 to %g %% (step %g %%)'
          % (k, n, 100 * g(h, 'erlPmax'), 100 * g(h, 'erlStp')))

# ============================================================================ B
print('== B. every number the help pages and comments quote ==')
src = open(SRC, encoding='utf-8').read()
quotes = [
    ('0.95^30 = 21.5 %', '%.1f' % (100 * 0.95 ** 30) == '21.5'),
    ('1 - 0.05^(1/30) = 9.50 %', '%.2f' % (100 * (1 - 0.05 ** (1 / 30))) == '9.50'),
    ('2.59 at n = 10', '%.2f' % (10 * (1 - 0.05 ** 0.1)) == '2.59'),
    ('2.85 at 30, 2.95 at 100, 2.99 at 1000',
     ['%.2f' % (n * (1 - 0.05 ** (1 / n))) for n in (30, 100, 1000)] == ['2.85', '2.95', '2.99']),
    ('1 error 4.74/n', '%.2f' % (stats.chi2.ppf(0.95, 4) / 2) == '4.74'),
    ('2 errors 6.30/n, 3 errors 7.75/n',
     ['%.2f' % (stats.chi2.ppf(0.95, 2 * k + 2) / 2) for k in (2, 3)] == ['6.30', '7.75']),
    ('of 1/32 and a 95 % upper bound of 9.21 %',
     Fraction(1, 32) == Fraction(1, 1 + 1 + 30) and '%.2f' % (100 * stats.beta.ppf(0.95, 1, 31)) == '9.21'),
    ('mean 1/62', Fraction(1, 2) / (1 + 30) == Fraction(1, 62)),
    ('bound 6.15 %', '%.2f' % (100 * stats.beta.ppf(0.95, 0.5, 30.5)) == '6.15'),
    ('Clopper-Pearson 3.0 %', '%.1f' % (100 * proportion_confint(0, 100, 0.1, 'beta')[1]) == '3.0'),
    ('Wilson 2.6 %, Agresti-Coull 3.2 %',
     ['%.1f' % (100 * proportion_confint(0, 100, 0.1, m)[1]) for m in ('wilson', 'agresti_coull')] == ['2.6', '3.2']),
    ('Jeffreys 1.9 %', '%.1f' % (100 * proportion_confint(0, 100, 0.1, 'jeffreys')[1]) == '1.9'),
    ('about 2,150 of the 10,000', abs(10000 * 0.95 ** 30 - 2150) < 10),
    ('that is 1, P is 63.2 %', '%.1f' % (100 * (1 - math.exp(-1))) == '63.2'),
]
for text, ok in quotes:
    present = text in src
    check(ok and present, 'quoted "%s"' % text)
print('   SciPy: 0.95^30 = %.5f, 1-0.05^(1/30) = %.5f, ln 20 = %.5f, Jeffreys 0/30 = %.5f'
      % (0.95 ** 30, 1 - 0.05 ** (1 / 30), math.log(20), stats.beta.ppf(0.95, 0.5, 30.5)))
for m in ('beta', 'wilson', 'agresti_coull', 'jeffreys'):
    print('   statsmodels 0 of 100, one-sided 95 %% (alpha = 0.10 two-sided), %-14s upper %.4f'
          % (m, proportion_confint(0, 100, 0.1, m)[1]))

# ============================================================================ C
print('== C. every CAS template through desktop Giac, compared with SymPy ==')
q, mu = sp.symbols('q mu', positive=True)


def giac_to_sympy(txt, subs):
    # 1a: the Prime's printing -- e^( (e is Euler's number) and the root sign -- read back
    t = re.sub('\u221a([A-Za-z_]\\w*|\\d+)', r'sqrt(\1)', txt).replace('\u221a(', 'sqrt(')
    t = re.sub(r'(?<![A-Za-z0-9_])e\^', 'E^', t)
    t = t.replace('^', '**')
    for a, b in subs.items():
        t = t.replace(a, b)
    return sp.sympify(t, locals={'q': q, 'mu': mu, 'N': sp.Symbol('N', positive=True),
                                 'ln': sp.log, 'exp': sp.exp, 'pi': sp.pi, 'E': sp.E, 'sqrt': sp.sqrt})


h = fresh()
ncas = 0
for am in (50, 10, 1, 500, 25):
    for n in (1, 5, 30, 1000, 10000):
        setrec(h, n, 0, am)
        h.globals_['erlCasKey'] = ''
        h.cas_calls.clear()
        h.call('erlCasFill')
        a1, a2, a3 = g(h, 'erlCa1'), g(h, 'erlCa2'), g(h, 'erlCa3')
        ncas += len(h.cas_calls)
        ok1 = Fraction(a1) == Fraction(am, 1000)
        v2 = float(sp.N(giac_to_sympy(a2, {}), 15))
        ok2 = abs(v2 - (1 - (am / 1000) ** (1 / n))) < 1e-12
        v3 = giac_to_sympy(a3, {})
        ok3 = sp.simplify(v3 - sp.log(sp.Rational(1000, am))) == 0
        check(ok1 and ok2 and ok3, 'k = 0, n = %5d, alpha = %s: %s | %s | %s' % (n, Fraction(am, 1000), a1, a2, a3))
print('   (CAS calls made in that loop: %d)' % ncas)
for n, k in ((30, 1), (30, 2), (30, 6), (2, 1), (7, 6), (100, 5), (1000, 3), (10000, 2)):
    setrec(h, n, k, 50)
    h.globals_['erlCasKey'] = ''
    h.call('erlCasFill')
    a2, a3 = g(h, 'erlCa2'), g(h, 'erlCa3')
    poly = giac_to_sympy(a2, {'erlq': 'q'})
    # the program shows (1-p)^(n-k) times the CAS's polynomial: compare the bracket
    # with sympy's, and the whole product with the binomial CDF (exactly for n <= 1000)
    refpoly = sp.expand(sum(sp.binomial(n, j) * q ** j * (1 - q) ** (k - j) for j in range(k + 1)))
    ok2 = sp.expand(poly - refpoly) == 0 and sp.degree(poly, q) <= k and '(-' not in a2   # canonical: no (-q)^j terms
    if n <= 1000:
        ok2 = ok2 and sp.expand((1 - q) ** (n - k) * poly -
                                sum(sp.binomial(n, j) * q ** j * (1 - q) ** (n - j) for j in range(k + 1))) == 0
    ok2 = ok2 and all(abs(float((1 - t) ** (n - k) * poly.subs(q, t)) - stats.binom.cdf(k, n, t)) < 1e-9
                      for t in (0.0001, 0.003, 0.01))
    expr3 = giac_to_sympy(a3, {'erll': 'mu'})
    ref3 = sp.exp(-mu) * sum(mu ** j / sp.factorial(j) for j in range(k + 1))
    ok3 = sp.simplify(expr3 - ref3) == 0
    shown = h.call('erlShow', a2, 'p')
    check(ok2 and ok3, 'k = %d, n = %5d: normal -> %s (%d chars, shown %r) ; Poisson limit -> %s'
          % (k, n, a2[:60], len(a2), shown[:50], a3))
    check(g(h, 'erlCasOK') == 1, '   badge "exact (CAS)" for k = %d, n = %d' % (k, n))
setrec(h, 30, 7, 50); h.globals_['erlCasKey'] = ''; h.cas_calls.clear(); h.call('erlCasFill')
check(len(h.cas_calls) == 1 and g(h, 'erlCasOK') == -1, 'k = 7 > 6: only alpha goes to the CAS; no badge')
setrec(h, 30, 30, 50); h.globals_['erlCasKey'] = ''; h.cas_calls.clear(); h.call('erlCasFill')
check(len(h.cas_calls) == 0 and g(h, 'erlCasOK') == -1, 'k = n: no CAS call (the bound is 100 %)')
# the call routine itself (1a: the BRIEF_CAS_v2 kit -- the CAS is asked for string(...), its answer
# is a PPL string whose quotes STRING() adds and erlCas drops); undef, errors and (new) an infinity
# become ""
hq = Harness(SRC, cas={'string(50/1000)': '"1/20"', 'string(1/2+1/3)': '"5/6"', 'string(q1)': '"undef"',
                       'string(q2)': '"a"', 'string(1/0)': '"\u00b1\u221e"'})
hq.call('erlInit')
check(hq.call('erlCas', '50/1000') == '1/20' and hq.call('erlCas', '1/2+1/3') == '5/6'
      and hq.call('erlCas', 'q1') == '' and hq.call('erlCas', 'q2') == 'a' and hq.call('erlCas', '1/0') == '',
      'erlCas: the quoted answer is unwrapped once, undef -> "", 1a: the infinity sign -> ""')
hf = Harness(SRC, cas='fail'); hf.call('erlInit')
check(hf.call('erlCas', '50/1000') == '', 'erlCas: a failing CAS call (IFERR) -> ""')
# the display transform
for raw, want in (('406*erlq^2+28*erlq+1', '406×p^2+28×p+1'),
                  ('(erlq-1)^28*(406*erlq^2+28*erlq+1)', '(1-p)^28×(406×p^2+28×p+1)'),
                  ('-(erlq-1)^29*(29*erlq+1)', '(1-p)^29×(29×p+1)'),
                  ('(erll^2+2*erll+2)*exp(-erll)/2', '(μ^2+2×μ+2)×e^(-μ)/2'),
                  ('1-(999999/1000000)^erlq', None), ('-exp(-erll)+1', '-e^(-μ)+1'),
                  # 1a: the same answers as the Prime prints them (e^, CASProbe T17)
                  ('(erll^2+2*erll+2)*e^(-erll)/2', '(μ^2+2×μ+2)×e^(-μ)/2'), ('-e^(-erll)+1', '-e^(-μ)+1')):
    got = h.call('erlShow', raw, 'N' if raw.startswith('1-(9') else 'p')
    check(want is None and got == '1-(999999/1000000)^N' or got == want, 'erlShow %r -> %r' % (raw, got))
# Bayes fractions
for a2, b2, k, n in ((2, 2, 0, 30), (1, 1, 0, 30), (1, 1, 3, 100), (2, 38, 1, 50), (199, 3, 7, 10000)):
    h = fresh()
    setrec(h, n, k, 50)
    h.globals_['erlBa2'] = float(a2); h.globals_['erlBb2'] = float(b2)
    h.call('erlBayesCalc')
    want = Fraction(a2 + 2 * k, a2 + b2 + 2 * n)
    check(Fraction(g(h, 'erlCaB')) == want, 'Bayes mean for prior (%s, %s), %d of %d: CAS %s = %s'
          % (a2 / 2, b2 / 2, k, n, g(h, 'erlCaB'), want))
# the trawl templates
h = fresh()
for m in (3, 6, 9):
    h.globals_['erlTm'] = float(m); h.globals_['erlCaTKey'] = ''
    h.call('erlTrCas')
    t1, t2, t3 = g(h, 'erlCaT1'), g(h, 'erlCaT2'), g(h, 'erlCaT3')
    Nn = sp.Symbol('N', positive=True)
    e1 = giac_to_sympy(t1, {'erlq': 'N'})
    ok1 = sp.simplify(e1 - (1 - (1 - sp.Rational(1, 10 ** m)) ** Nn)) == 0
    ok2 = sp.simplify(giac_to_sympy(t2, {'erll': 'mu'}) - (1 - sp.exp(-mu))) == 0
    ok3 = sp.expand(giac_to_sympy(t3, {'erll': 'mu'}) - (mu - mu ** 2 / 2 + mu ** 3 / 6)) == 0
    check(ok1 and ok2 and ok3, 'trawl RMP 1E-%d: %s | %s | %s' % (m, t1, t2, t3))
print('   Giac timings on the PC (ms): ' + ', '.join('%.0f' % c[2] for c in h.cas_calls))

# ============================================================================ D
print('== D. the #PYTHON block under CPython (stub hpprime and urandom) ==')
pyblock = re.search(r'^#PYTHON erlPySim\n(.*?)^#END', src, re.S | re.M).group(1)


def run_pyblock(vals, seed, sink):
    """Run the block; vals answers reads, sink(expr) receives every write."""
    rng = pyrandom.Random(seed)
    hp = types.ModuleType('hpprime')

    def ev(s):
        if s in vals:
            return vals[s]
        return sink(s)
    hp.eval = ev
    ur = types.ModuleType('urandom')
    ur.random = rng.random
    sys.modules['hpprime'], sys.modules['urandom'] = hp, ur
    exec(compile(pyblock, 'erlPySim', 'exec'), {'__name__': '__main__'})


check('from random' not in pyblock and 'import time' not in pyblock and 'from urandom import random' in pyblock,
      'the block imports urandom (MicroPython 1.9.4 has no random, no time)')
check('f"' not in pyblock and ".format(" not in pyblock and 'join(' not in pyblock,
      'no f-strings, no format(), no join: concatenation only (Lessons Learned s9)')
for n, p, k, w, M in ((30, 0.05, 0, 1, 10000), (30, 0.2, 2, 1, 10000), (1000, 0.003, 0, 1, 10000),
                      (200, 0.3, 4, 3, 10000), (10, 0.5, 0, 1, 50), (30, 0.0, 0, 1, 1000), (30, 1.0, 2, 1, 1000)):
    writes = []
    run_pyblock({'ER_PYN': float(n), 'ER_PYP': p, 'ER_PYM': float(M), 'ER_PYK': float(k), 'ER_PYW': float(w)},
                11, writes.append)
    out = {}
    marks = []
    for s in writes:
        mm = re.fullmatch(r'ER_PYO\((\d+)\):=(\d+)', s)
        if mm:
            out[int(mm.group(1))] = int(mm.group(2))
        else:
            mz = re.fullmatch(r'ER_PYZ:=(\d)', s)
            marks.append(int(mz.group(1)))
    order = [int(re.fullmatch(r'ER_PYO\((\d+)\).*', s).group(1)) for s in writes if s.startswith('ER_PYO')]
    bins = [out[i] for i in range(1, 42)]
    ok = (order == list(range(1, 45)) and marks == [1, 2, 3] and sum(bins) == M and out[43] <= M and out[42] <= out[43])
    if 0 < p < 1:
        # every count against the binomial (bins of width w)
        cdf = lambda x: stats.binom.cdf(x, n, p)
        expv = [M * (cdf(min(n, (j + 1) * w - 1)) - (cdf(j * w - 1) if j > 0 else 0)) for j in range(40)]
        expv.append(M * (1 - cdf(40 * w - 1)))
        keep = [j for j in range(41) if expv[j] >= 5]
        obs = [bins[j] for j in keep]; ex = [expv[j] for j in keep]
        rest_o = M - sum(obs); rest_e = M - sum(ex)
        if rest_e >= 5: obs.append(rest_o); ex.append(rest_e)
        ex = [e * sum(obs) / sum(ex) for e in ex]
        pv = stats.chisquare(obs, ex).pvalue
        z0 = (out[42] - M * (1 - p) ** n) / math.sqrt(M * (1 - p) ** n * (1 - (1 - p) ** n) + 1e-12)
        zk = (out[43] - M * stats.binom.cdf(k, n, p)) / math.sqrt(M * stats.binom.cdf(k, n, p) * stats.binom.sf(k, n, p) + 1e-12)
        mean_ok = abs(out[44] / M - n * p) < 5 * math.sqrt(n * p * (1 - p) / M)
        ok = ok and pv > 0.001 and abs(z0) < 4 and abs(zk) < 4 and mean_ok
        check(ok, 'n=%d p=%.3f k=%d w=%d: 44 writes in order, marks 1-2-3, bins fit Binomial (chi-square p = %.3f), '
              '0 errors %d (exact %.1f), <= k %d (exact %.1f)' % (n, p, k, w, pv, out[42], M * (1 - p) ** n,
                                                                  out[43], M * stats.binom.cdf(k, n, p)))
    else:
        want0 = M if p == 0 else 0
        check(ok and out[42] == want0 and out[44] == (0 if p == 0 else n * M),
              'edge p = %g: %d clean records, %d errors in all' % (p, out[42], out[44]))

# ============================================================================ E
print('== E. the program end to end in the harness ==')


def py_ok(h, seed=5):
    """PYTHON(erlPySim) patched to run the block in CPython, reading and writing the
    harness's own globals through the bridge, as hpprime.eval would on the device."""
    def fake(a):
        def sink(s):
            m1 = re.fullmatch(r'(\w+)\((\d+)\):=(-?\d+)', s)
            if m1:
                h.globals_[m1.group(1)][int(m1.group(2)) - 1] = float(m1.group(3))
                return 0.0
            m2 = re.fullmatch(r'(\w+):=(-?\d+)', s)
            if m2:
                h.globals_[m2.group(1)] = float(m2.group(2))
                return 0.0
            raise ValueError(s)
        vals = {nm: float(h.globals_[nm]) for nm in ('ER_PYN', 'ER_PYP', 'ER_PYM', 'ER_PYK', 'ER_PYW')}
        run_pyblock(vals, seed, sink)
        return 0.0
    h._python = fake


def session(h):
    """One scripted lecture: every page, every soft key, every gesture."""
    h.press('Enter')                                   # welcome
    h.tap(160, 100)                                    # tap the plot: a rate
    h.drag([(100, 100), (110, 100), (130, 100), (148, 100)])   # drag the rate
    h.drag([(315, 120), (315, 100), (315, 80), (315, 60)])     # drag n up the slider
    h.press('Down', 'Up', 'Minus', 'Plus', 'Left', 'Right')
    h.tap(20, 230); h.answer({'akN': 30, 'akK': 0, 'akA': 0.05})   # n, k: back to 0 of 30
    h.tap(80, 230); h.answer({'arP': 0.05})            # Rate: 5 %
    h.tap(130, 230); h.press('Plus', 'Minus'); h.press('Esc')   # Why 3, n 40 and back to 30
    h.tap(190, 230)                                    # Bayes
    h.tap(80, 230)                                     # Jeffreys
    h.drag([(80, 100), (120, 100)])                    # drag the rate on the Bayes page
    h.tap(130, 230); h.answer({'apA': 1, 'apB': 19})   # a, b: a sceptical prior
    h.tap(20, 230)                                     # back to uniform
    h.tap(240, 230)                                    # Back
    h.tap(240, 230)                                    # Sim
    h.tap(20, 230)                                     # Again
    h.tap(130, 230)                                    # Rate+
    h.press('Esc')
    h.tap(300, 230)                                    # More: page 2
    h.tap(20, 230)                                     # Trawl
    h.drag([(100, 100), (200, 100), (222, 100)])       # drag N
    h.tap(20, 230); h.choose(3)                        # RMP 1 in 100,000
    h.tap(80, 230); h.answer({'anN': 1000000})         # N
    h.tap(130, 230); h.press('Enter')                  # Exact page
    h.press('Left', 'Right')
    h.tap(240, 230)                                    # Back
    h.tap(80, 230)                                     # Log y
    h.tap(80, 230)                                     # Lin y
    h.tap(130, 230)                                    # Help
    h.press('Enter', 'Enter', 'Enter', 'Enter', 'Enter', 'Enter', 'Enter', 'Enter', 'Enter')
    h.tap(190, 230); h.press('Enter')                  # Eng
    h.tap(300, 230)                                    # More: page 1
    h.tap(20, 230); h.answer({'akN': 30, 'akK': 0, 'akA': 0.05})   # n, k back to the default
    h.press('Enter'); h.choose(10)                     # menu > Quit


SKPAGES = ('erlDrawMain', 'erlBayesDraw', 'erlSimDraw', 'erlTrDraw')


def page_checks(h, tag):
    bad = []
    for s in h.pages:
        if s.func in SKPAGES:
            low = [t for t in s.texts if t.y + 11 > 218]
            if low:
                bad.append('%s: %s' % (s.func, low[0].text))
    check(not bad, '%s: no text reaches the soft keys (y + 11 <= 218) on any soft-key page %s' % (tag, bad[:2]))
    long = [t.text for s in h.pages if s.func == 'erlPage' for t in s.texts
            if t.font == 1 and t.y not in (10, 220) and len(t.text) > 46]
    check(not long, '%s: every text-page line is 46 characters or fewer %s' % (tag, long[:2]))
    check(all(not m.over_five for m in h.msgboxes), '%s: no MSGBOX over five lines' % tag)


# E1. CAS by Giac, Python working
h = Harness(SRC, cas='giac', seed=3)
py_ok(h)
session(h)
r = h.call('ErrorRate')
check(r == 'ErrorRate: 0 errors in 30 tests -> 95 % upper bound 9.50 % (3/n = 10.0 %); see ER_UPPER',
      'E1 (CAS on, Python on): returns %r' % r)
check(not any(h.leftover()), 'E1: the whole script was used (%r)' % (h.leftover(),))
main0 = [s for s in h.pages if s.func == 'erlDrawMain'][0]
waits = [s for s in h.screens if s.reason == 'wait' and s.menu]
lines = main0.lines()
check('95 % upper bound on the error rate: 9.50 %' in lines and
      '0 errors in 30 tests 21.5 % of the time.' in lines and
      '3/n = 10.0 %, n × bound = 2.85 → 3.00' in lines,
      'E1: the opening frame says 9.50 %, 21.5 % at a 5.0 % rate, 3/n = 10.0 %, n x bound 2.85')
check(waits[0].menu == ['n, k', 'Rate', 'Why 3', 'Bayes', 'Sim', 'More'], 'E1: soft keys page 1 %r' % waits[0].menu)
pg2 = [s for s in waits if s.menu[0] == 'Trawl']
check(pg2 and pg2[0].menu == ['Trawl', 'Log y', 'Help', 'Eng', 'Quit', 'More'], 'E1: More -> page 2 %r' % (pg2[0].menu if pg2 else None))
check(any(s.menu == ['Trawl', 'Lin y', 'Help', 'Eng', 'Quit', 'More'] for s in waits), 'E1: Log y turns into Lin y')
menus = {tuple(s.menu) for s in waits}
for want in (('Unif', 'Jeff', 'a, b', '', 'Back', ''), ('Again', 'Rate-', 'Rate+', '', 'Back', ''),
             ('RMP', 'N', 'Exact', '', 'Back', '')):
    check(want in menus, 'E1: soft keys %r shown' % (want,))
drag = [s for s in h.pages if s.func == 'erlDrawMain' and any('An examiner whose true rate' in t.text for t in s.texts)]
rates = sorted({t.text for s in drag for t in s.texts if t.text.startswith('An examiner')})
check(len(rates) >= 5, 'E1: the rate drag redrew live (%d different rates shown)' % len(rates))
ns = sorted({t.text for s in h.pages if s.func == 'erlDrawMain' for t in s.texts if t.y == 1})
check(len(ns) >= 6, 'E1: the n slider and keys showed %d different records' % len(ns))
sims = [s for s in h.pages if s.func == 'erlSimDraw']
badge = [t.text for s in sims for t in s.texts if t.text.startswith('engine:')]
check(sims and all(b.startswith('engine: MicroPython, 10,000 in') for b in badge),
      'E1: the simulation ran in (patched) MicroPython: %r' % badge[:1])
def sim_check(s, M, tag):
    head = [t.text for t in s.texts if t.y == 1][0]
    rate = float(re.search(r'rate ([0-9.]+) %', head).group(1)) / 100
    n = int(re.search(r'takes (\d+) tests', [t.text for t in s.texts if t.y == 13][0]).group(1))
    z = [t.text for t in s.texts if t.text.startswith('0 errors:')][0]
    zc = int(z.split(':')[1].split('of')[0].replace(',', ''))
    ex = (1 - rate) ** n
    check(abs(zc - M * ex) < 4 * math.sqrt(M * ex * (1 - ex)),
          '%s: %r at rate %.3f, n %d (exact %.1f of %d)' % (tag, z, rate, n, M * ex, M))
    want = 'exact chance (1 - p)^%d = %s' % (n, ('%.1f %%' if ex >= 0.1 else '%.2f %%') % (100 * ex))
    check(any(t.text == want for t in s.texts), '%s: %r' % (tag, want))


sim_check(sims[0], 10000, 'E1')
casp = [s for s in h.pages if s.func == 'erlPage' and any(t.text == 'Where the 3 comes from' for t in s.texts)]
check(casp and all(any(t.text == 'exact (CAS)' for t in s.texts) for s in casp), 'E1: Why 3 pages carry "exact (CAS)"')
check(any('   p = 1-(1/20)^(1/30)' == t.text for t in casp[0].texts) and any('ln(20)' in t.text for t in casp[0].texts),
      'E1: Why 3 shows p = 1-(1/20)^(1/30) and the limit ln(20)')
bay = [s for s in h.pages if s.func == 'erlBayesDraw']
check(any(t.text == 'mean (a+k)/(a+b+n) = 1/62 = 1.61 %' for s in bay for t in s.texts),
      'E1: Jeffreys mean 1/62 = 1.61 % from the CAS')
check(any(t.text in ('mean (a+k)/(a+b+n) = 1/32 = 3.13 %', 'mean (a+k)/(a+b+n) = 1/32 = 3.12 %')
          for s in bay for t in s.texts) and
      any(t.text.startswith('95 % credible bound 9.21 % (CP 9.50 %)') for s in bay for t in s.texts),
      'E1: uniform mean 1/32 = 3.13 %, credible bound 9.21 % beside CP 9.50 %')
check(any(t.text.startswith('Bayes: prior Beta(1, 19), your prior') for s in bay for t in s.texts),
      'E1: the a, b form gives Beta(1, 19)')
tr = [s for s in h.pages if s.func == 'erlTrDraw']
check(any(t.text == 'P(at least one chance match) = 63.2 %' for s in tr for t in s.texts),
      'E1: trawl at RMP 1E-6, N = 1E6: 63.2 %')
ex = [s for s in h.pages if s.func == 'erlPage' and any(t.text == 'Exact and approximate' for t in s.texts)]
check(ex and any(t.text == 'exact (CAS)' for t in ex[0].texts), 'E1: trawl Exact page badge "exact (CAS)"')
print('   trawl Exact page:'); [print('     ' + t.text) for t in ex[0].texts if t.y > 20]
helps = [s for s in h.pages if s.func == 'erlPage' and s.texts and s.texts[0].font == 2]
titles = [s.texts[0].text for s in helps]
check(all(x in titles for x in ('Zero errors is not a zero rate', 'Honest caveats', 'Three engines')), 'E1: nine help pages reached')
eng = [s for s in h.pages if s.func == 'erlPage' and any(t.text == 'Engines: who did what' for t in s.texts)]
check(eng and any('1/2+1/3 = 5/6' in t.text for t in eng[0].texts) and any('MicroPython answers' in t.text for t in eng[0].texts),
      'E1: Engines page: CAS live check 5/6, Python live check answers')
check(g(h, 'ER_UPPER') == 1 - 0.05 ** (1 / 30) and g(h, 'ER_N') == 30 and abs(g(h, 'ER_RULE') - 0.1) < 1e-15,
      'E1: Home exports ER_UPPER %.6f, ER_N %d, ER_RULE %.3f, ER_SIM %.4f, ER_TRAWL %.4f, ER_BMEAN %.5f'
      % (g(h, 'ER_UPPER'), g(h, 'ER_N'), g(h, 'ER_RULE'), g(h, 'ER_SIM'), g(h, 'ER_TRAWL'), g(h, 'ER_BMEAN')))
page_checks(h, 'E1')
print('   CAS calls in the session: %d, slowest %.0f ms on the PC' % (len(h.cas_calls), max(c[2] for c in h.cas_calls)))
drawn = [c for c in h.cas_calls]
body = lambda t: t[7:-1] if t.startswith('string(') else t     # 1a: the kit asks for string(...)
check(any(body(c[0]).startswith('limit') for c in drawn)
      and all(not body(c[0]).startswith('limit') or ',erlq,inf)' in c[0] for c in drawn),
      'E1: every limit template uses erlInf = "inf"')
check(all(c[0].startswith('string(') and c[1].startswith('"') for c in drawn) and not h.cas_vars
      and not any('non-literal' in w for w in h.warnings),
      'E1 1a: every CAS text asks for string(...), every answer quoted; no CAS variable assigned, no CAS call of a variable')
check(not any('exp(' in t.text or 'sqrt' in t.text for s in h.pages for t in s.texts),
      'E1 1a: no "exp(" or "sqrt" on any page (the Prime\'s printing)')


# E2. CAS failing, Python absent (the harness's PYTHON does nothing, as when Python fails)
h = Harness(SRC, cas='fail', seed=3)
session(h)
r = h.call('ErrorRate')
check(r.startswith('ErrorRate: 0 errors in 30 tests -> 95 % upper bound 9.50 %'), 'E2 (CAS off, Python off): returns %r' % r)
casp = [s for s in h.pages if s.func == 'erlPage' and any(t.text == 'Where the 3 comes from' for t in s.texts)]
check(casp and all(any(t.text == 'decimal' for t in s.texts) for s in casp), 'E2: Why 3 pages say "decimal"')
check(any(t.text == '   p = 1-0.05^(1/30)' for t in casp[0].texts) and any(t.text == '     = 0.09503 = 9.50 %' for t in casp[0].texts),
      'E2: the decimal fallback shows the formula and 0.09503 = 9.50 %')
bay = [s for s in h.pages if s.func == 'erlBayesDraw']
check(any(t.text == 'mean (a+k)/(a+b+n) = 1.61 %' for s in bay for t in s.texts) and
      any(t.text == 'decimal' for s in bay for t in s.texts), 'E2: Bayes mean as a decimal, badge "decimal"')
sims = [s for s in h.pages if s.func == 'erlSimDraw']
badge = [t.text for s in sims for t in s.texts if t.text.startswith('engine:')]
check(sims and all(b.startswith('engine: PPL fallback, 1,000 in') for b in badge), 'E2: simulation fell back to PPL: %r' % badge[:1])
sim_check(sims[0], 1000, 'E2 (PPL fallback)')
ex = [s for s in h.pages if s.func == 'erlPage' and any(t.text == 'Exact and approximate' for t in s.texts)]
check(ex and any(t.text == 'decimal' for t in ex[0].texts), 'E2: trawl Exact page says "decimal"')
eng = [s for s in h.pages if s.func == 'erlPage' and any(t.text == 'Engines: who did what' for t in s.texts)]
check(eng and any('no answer (the CAS call failed)' in t.text for t in eng[0].texts) and
      any('no answer; stage ER_PYZ = 0' in t.text for t in eng[0].texts), 'E2: Engines page reports both failures')
check(not h.error, 'E2: no runtime error anywhere')
page_checks(h, 'E2')

# E3. Python that stops part-way: the validation must refuse it
h = Harness(SRC, cas='giac', seed=4)


def half(a, h=h):
    lst = h.globals_['ER_PYO']
    for i in range(30):
        lst[i] = 300.0
    h.globals_['ER_PYZ'] = 2.0
    return 0.0


h._python = half
h.call('erlInit')
h.call('erlRunSim')
check(g(h, 'erlSmEng') == 2 and g(h, 'erlSmM') == 1000, 'E3: a Python run that stops part-way -> PPL fallback (validation works)')


def wrongsum(a, h=h):
    lst = h.globals_['ER_PYO']
    for i in range(44):
        lst[i] = 1.0
    return 0.0


h._python = wrongsum
h.call('erlRunSim')
check(g(h, 'erlSmEng') == 2, 'E3: a payload whose bins do not add to 10,000 -> PPL fallback')

# E4. a k > 0 session, alpha 0.01, log scale
h = Harness(SRC, cas='giac', seed=8)
py_ok(h, seed=9)
h.press('Enter')
h.tap(20, 230); h.answer({'akN': 30, 'akK': 2, 'akA': 1})        # alpha typed as a percent
h.drag([(315, 120), (315, 90), (315, 40)])                       # drag n with k = 2 (stride 3)
h.tap(130, 230); h.press('Esc')                                  # Why 3 for k = 2
h.tap(240, 230); h.press('Esc')                                  # Sim with k = 2
h.tap(300, 230); h.tap(80, 230)                                  # log scale
h.tap(240, 230)                                                  # Quit
r = h.call('ErrorRate')
pu = stats.beta.ppf(0.99, 3, g(h, 'erlN') - 2)
check(abs(g(h, 'ER_UPPER') - pu) < 1e-12 and g(h, 'ER_ALPHA') == 0.01,
      'E4 (k = 2, alpha typed as 1): n = %d, bound %.5f = beta.ppf(0.99, 3, n-2); returns %r' % (g(h, 'erlN'), g(h, 'ER_UPPER'), r))
dr = [s for s in h.pages if s.func == 'erlDrawMain']
check(g(h, 'erlCS') == 1, 'E4: after the n drag the curve was rebuilt at full resolution (stride 1)')
casp = [s for s in h.pages if s.func == 'erlPage']
check(any(t.text.startswith('   (1-p)^') and '×(' in t.text for s in casp for t in s.texts), 'E4: the k = 2 CAS page shows (1-p)^(n-k) x the exact polynomial')
logp = [s for s in h.screens if s.reason == 'wait' and s.menu and s.menu[1] == 'Lin y']
lab = sorted({t.text for s in logp for t in s.texts if t.x == 2 and t.font == 1 and t.text in ('1', '.1', '.01', '.001', '1E-4')})
check(lab == ['.001', '.01', '.1', '1'], 'E4: log axis at alpha 0.01 runs 1 to .001 (alpha two-thirds down): %r' % lab)
sims = [s for s in h.pages if s.func == 'erlSimDraw']
check(sims and any(t.text.startswith('at most 2 errors:') for t in sims[0].texts), 'E4: the k = 2 simulation counts "at most 2 errors"')
page_checks(h, 'E4')

# E5. stale keys: a dialog's own Enter left in the buffer must not skip a page
h = Harness(SRC, cas='giac', seed=2, stale_keys=True)
h.press('Enter'); h.tap(20, 230); h.answer(ACCEPT); h.press('Esc')
h.call('ErrorRate')
check(not h.stale_skips, 'E5: stale-key mode: no page skipped by a dialog\'s left-over key (%r)' % (h.stale_skips,))

# E6. the fence and the per-frame cost: drags call no CAS, and count the CDFs per frame
for k in (0, 2):
    h = Harness(SRC, cas='giac', seed=6)
    h.press('Enter')
    if k:
        h.tap(20, 230); h.answer({'akN': 30, 'akK': k, 'akA': 0.05})
    h.press('Esc')
    h.call('ErrorRate')
    h.reset_records(); h.cas_calls.clear(); h.stat_calls.clear()
    h.drag([(60 + 10 * i, 100) for i in range(10)])               # the rate: 10 samples
    h.drag([(315, 150 - 10 * i) for i in range(10)])              # n: 10 samples
    h.press('Esc')
    h.call('erlLoop')
    frames = [s for s in h.pages if s.func == 'erlDrawMain']
    cdf = [c for c in h.stat_calls if c[0] == 'BINOMIAL_CDF']
    check(not h.cas_calls, 'E6 (k = %d): no CAS call during 20 drag samples (the fence: events, never frames)' % k)
    print('   k = %d: %d frames for 20 drag samples, %d BINOMIAL_CDF calls in all (%.0f a frame)'
          % (k, len(frames), len(cdf), len(cdf) / max(1, len(frames))))

# ============================================================================ G (1a)
print('== G. 1a: beta 1 in harness v3b, and beta 1a against beta 1 ==')
h1 = Harness(BETA1, cas='giac', seed=1)
h1.call('erlInit')
setrec(h1, 30, 0, 50)
h1.globals_['erlCasKey'] = ''
h1.call('erlCasFill')
check(g(h1, 'erlCa1') == '50/1000' and g(h1, 'erlCa3').startswith('limit(') and g(h1, 'erlCasOK') == 1
      and any('non-literal' in w for w in h1.warnings),
      '1a: beta 1 in v3b: erlCas hands back its own text ("50/1000", "limit(...)"), and the page would show it '
      'under "exact (CAS)" -- the emulator\'s finding')
h2 = fresh()
setrec(h2, 30, 0, 50)
h2.globals_['erlCasKey'] = ''
h2.call('erlCasFill')
check(g(h2, 'erlCa1') == '1/20' and g(h2, 'erlCa3') == 'ln(20)', '1a: beta 1a: alpha = 1/20 and the limit ln(20)')
say = print
_saved_check = check


def _check2(ok, what):
    _saved_check(ok, what)


check = _check2

# ================================================================ G (round 2a)
say('\nG. beta 1a: beta 1 in harness v3b, and beta 1a against beta 1')
import re as _re
_b_old = open(BETA1, encoding='utf-8').read()
_b_new = open(SRC, encoding='utf-8').read()


def _bodies(txt):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)
    c = _re.sub(r'//[^\n]*', '', c)
    out = {}
    for m in _re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, _re.S):
        out[m.group(1)] = _re.sub(r'[ \t]+\n', '\n', m.group(0))
    return out


_B0, _B1 = _bodies(_b_old), _bodies(_b_new)
_diff = sorted(n for n in set(_B0) | set(_B1) if _B0.get(n) != _B1.get(n))
check(_diff == ['erlCas', 'erlEngPage'], 'beta 1a: routines that differ from beta 1: %s (want erlCas, erlEngPage)' % _diff)


def _outside(t, names):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\n]*', '', t))
    if names:
        c = _re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
    return _re.sub(r'\s+', ' ', c)


check(_outside(_b_old, _diff) == _outside(_b_new, _diff), 'beta 1a: outside those routines only comments differ')
_py0 = _re.findall(r'(?s)#PYTHON.*?#END', _b_old)
_py1 = _re.findall(r'(?s)#PYTHON.*?#END', _b_new)
check(_py0 == _py1, 'beta 1a: the #PYTHON blocks are unchanged')
say('  routines that differ from beta 1: %s; everything else differs only in comments' % ', '.join(_diff))

check = _saved_check

if FAILS:
    print('\n%d FAILED' % len(FAILS))
    for f in FAILS:
        print('  - ' + f)
    sys.exit(1)
print('\nALL PASS')
