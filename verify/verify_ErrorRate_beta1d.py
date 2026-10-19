#!/usr/bin/env python3
"""verify_ErrorRate_beta1d.py -- checks for ErrorRate Lab beta 1d, 19 Oct 2026: the fleet review's E1, E2, E4, E5
and Roger's disclaimer (19 Oct, 12:48).  Built from verify_ErrorRate_beta1c.py: every check below runs on beta 1d
(SRC), on harness v3e.  Where an old check's expected value changes with beta 1d, it says so in its message:
  R5  the routines that differ from beta 1a now include beta 1d's seven (ErrorRate, erlCasDraw, erlDrawText,
      erlEngPage, erlPoiTerms, erlRuleEq new, erlTrExact, erlWelcome; erlCasDraw and erlTrExact were already listed).
  T5  1b's text is written the 1d way too ("  P(at least one) = " -> "  P(1 or more) = ", E1), and the welcome
      page's new disclaimer line is set aside before the comparison (it is checked in U5).
  T6  checks the 1b -> 1c diff, so it now reads beta 1c's own file (BETA1C); U6 checks 1c -> 1d.
  T7  INSTRING and the bracket-comment check read beta 1d; the version strings are beta 1d's.
New section U (beta 1d against beta 1c, both run in the harness):
  U1 E1   the trawl's Exact page for every RMP on the menu, CAS answering and failing: 14 lines, the answer on one
          line, "RMP values are illustrative, not casework." on the page; beta 1c loses it at 1 in a billion.
  U2 E2   the rule line at 100 % or more (panel, "Why 3" page, the summary to Home) and a sweep of 6 alphas x
          n 1..60 and 4 large n x 6 k: never a rate of 100 % or more, never "= >".
  U3 E4   the Engines page's CAS line after a k > 6 "Why 3" page, the Bayes page, the trawl, nothing, k = 0.
  U4 E5   erlPoiTerms unchanged for k = 1..6; a copy of each file whose FOR runs once when its finish is below
          its start (a Prime that did so): beta 1c's k = 1 text gains a false factor, beta 1d's does not.
  U5      the disclaimer: in the header, and on the opening page (beta 1c has neither).
  U6      the routine diff and the code-line diff, 1c -> 1d; the #PYTHON block byte-identical.
  U7      names, LOCAL sizes, INSTRING, bracket comments, ASCII, version strings.
  U8      the review's own check_ErrorRate.py run on beta 1c (1 failure, E1) and on beta 1d (0).
  U9      h.sci_strings from every beta 1d run in this script.

(beta 1c's docstring follows.)

verify_ErrorRate_beta1c.py -- checks for ErrorRate Lab beta 1c, 17 Oct 2026, evening: no "=" before a relation
(erlEq), the Bayes page's P(true rate > x) as the mirrored Beta's lower tail, "N = 1 profile searched".
Built from verify_ErrorRate_beta1b.py: every check below runs on beta 1c, on harness v3e (the same results as v3d
for this script; its README), and R5's list of routines that differ from beta 1a now includes beta 1c's five and
erlEq.  The new section T checks beta 1c against beta 1b:
  T1. each fixed display, beta 1b -> 1c, reached in the harness; ordinary values unchanged.
  T2. the mirrored Beta tail = 1 - erlBetaCdf = SciPy; 0 of 1000 at 30 %: kept, not 0.
  T3. erlEq.  T4. the sites left alone cannot reach erlPctS's ends.  T5. two whole sessions, 1b and 1c text for
      text once 1b's "= <" is written the 1c way.  T6. the routine diff and the line diff.  T7. names, INSTRING,
      version strings, comments.  T8. no scientific fixed decimals in any beta 1c run.

(beta 1b's docstring follows.)

verify_ErrorRate_beta1b.py -- checks for ErrorRate Lab beta 1b, 17 Oct 2026: the string fixes after the
second emulator round (INSTRING("", ...) is "Invalid input" on the Prime; STRING(x, 2, d) prints scientific
when 0 < |x| < 10^-d).  Built from verify_ErrorRate_beta1a.py: every check below is kept and now runs on
harness v3d (/home/claude/work/out/ppl_run_v3d.py), which models both facts; G compares beta 1 with beta 1a
as before, and the new section R checks beta 1b:
  R1. erlCas after a failed CAS call returns "" with no error; beta 1a in v3d stops there.
  R2. cas='fail', page by page (Why 3 for k = 0 and k = 2, Bayes, trawl Exact, Engines) and the whole
      session: every CAS page completes with the "decimal" badge and no error; beta 1a in v3d stops on
      every one of them with "INSTRING: Invalid input".
  R3. erlRepl directly: a pattern at the end, at the start, the whole string, an empty pattern, an
      empty text, a pattern that is not there.
  R4. the small-number displays: erlFix rounds; the trawl at N = 1, RMP 1 in a billion reads
      "N x RMP = 0.000" and "mu = 0.000"; a typed rate of 0.02 % and the Bayes page's first step read
      through erlPctS, not "0.0 %"; beta 1a shows the scientific forms there.
  R5. beta 1b against beta 1a: the routines that differ are exactly erlCas, erlFix, erlRateS and
      erlRepl; outside them only comments differ; the #PYTHON block is byte-identical.
  R6. h.sci_strings from EVERY harness run of beta 1b in this script: empty.

(beta 1a's docstring follows.)

verify_ErrorRate_beta1a.py -- checks for ErrorRate Lab beta 1a (HP Prime PPL + MicroPython + CAS),
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

sys.path.insert(0, '/home/claude/work/out')
import ppl_run_v3e as ppl_run_v3d  # noqa: E402   (1c: harness v3e)
from ppl_run_v3e import Harness, ACCEPT, giac_eval  # noqa: E402

SRC = '/home/claude/work/fix19/ErrorRate_beta1d.txt'
BETA1C = '/home/claude/work/out/ErrorRate_beta1c.txt'
BETA1A = '/home/claude/work/out/ErrorRate_beta1a.txt'
BETA1 = '/home/claude/work/out/ErrorRate_beta1.txt'

# 1b: every harness made in this script is remembered, so R6 can list h.sci_strings from all of them
ALLH = []
_h_init = ppl_run_v3d.Harness.__init__


def _h_track(self, *a, **k):
    _h_init(self, *a, **k)
    ALLH.append((a[0] if a else k.get('paths'), self))


ppl_run_v3d.Harness.__init__ = _h_track
FAILS = []


_NCHK = [0]                      # 1d: the number of checks run, for the summary line


def check(cond, msg):
    _NCHK[0] += 1
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
_b_new = open(BETA1A, encoding='utf-8').read()


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

# ================================================================ R (1b)
print('\n== R. 1b: the round-2 string fixes (harness v3d) ==')
INV = 'INSTRING: Invalid input'


def stops(fn):
    """Run fn(); return the error text if the program stopped, else None."""
    try:
        fn()
        return None
    except Exception as e:      # the harness raises the PPL run-time error
        return str(e)


# R1. erlCas after a failed call
hf = Harness(SRC, cas='fail'); hf.call('erlInit')
r1 = stops(lambda: hf.call('erlCas', '50/1000'))
check(r1 is None and hf.call('erlCas', '1/2+1/3') == '', 'R1 1b: a failed CAS call -> erlCas returns "" with no error')
ho = Harness(BETA1A, cas='fail'); ho.call('erlInit')
r1o = stops(lambda: ho.call('erlCas', '50/1000'))
check(r1o is not None and INV in r1o, 'R1 beta 1a in v3d: the same call stops the program: %s' % (r1o or '')[:60])
hq = Harness(SRC, cas={'string(q1)': '""', 'string(q2)': '"undef"', 'string(q3)': '"7/2"'}); hq.call('erlInit')
check(hq.call('erlCas', 'q1') == '' and hq.call('erlCas', 'q2') == '' and hq.call('erlCas', 'q3') == '7/2',
      'R1 1b: an empty CAS string -> "" (no INSTRING on it), undef -> "", 7/2 kept')


# R2. cas='fail', page by page, beta 1b and beta 1a
def page_run(path, which):
    h = Harness(path, cas='fail', seed=3)
    h.call('erlInit')
    if which == 'why3':
        h.press('Esc'); fn = lambda: h.call('erlCasPage')
    elif which == 'why3k2':
        h.globals_['erlK'] = 2.0; h.call('erlRecalc'); h.call('erlFit', 0.0)
        h.press('Esc'); fn = lambda: h.call('erlCasPage')
    elif which == 'bayes':
        h.press('Esc'); fn = lambda: h.call('erlBayesPage')
    elif which == 'exact':
        h.press('Enter'); fn = lambda: h.call('erlTrExact')
    else:
        h.press('Enter'); fn = lambda: h.call('erlEngPage')
    return h, stops(fn)


PAGES = (('why3', 'Where the 3 comes from', 'decimal'), ('why3k2', 'The equation for k > 0', 'decimal'),
         ('bayes', None, 'decimal'), ('exact', 'Exact and approximate', 'decimal'),
         ('eng', 'Engines: who did what', 'no answer (the CAS call failed)'))
for which, title, want in PAGES:
    h, err = page_run(SRC, which)
    shown = [t.text for s in h.screens for t in s.texts]
    ok = err is None and any(want in x for x in shown) and (title is None or title in shown)
    check(ok, 'R2 1b cas=fail, page %-6s: opens, shows %r, no error' % (which, want))
    _, erro = page_run(BETA1A, which)
    check(erro is not None and INV in erro, 'R2 beta 1a in v3d, cas=fail, page %-6s: stops (%s)' % (which, (erro or 'no error')[:40]))

# the whole lecture with the CAS failing (section E's script), old and new
hn = Harness(SRC, cas='fail', seed=3); session(hn); rn = stops(lambda: hn.call('ErrorRate'))
check(rn is None and hn.result.startswith('ErrorRate: 0 errors in 30 tests'), 'R2 1b cas=fail: the whole E session runs to Quit')
ho = Harness(BETA1A, cas='fail', seed=3); session(ho); ro = stops(lambda: ho.call('ErrorRate'))
first = [s for s in ho.pages if s.func == 'erlDrawMain']
check(ro is not None and INV in ro, 'R2 beta 1a in v3d, cas=fail: the same session stops (%s), after %d main frames'
      % ((ro or '')[:40], len(first)))

# R3. erlRepl, directly (beta 1b)
hr = Harness(SRC); hr.call('erlInit')
for s, o, n, want in (('a*b', '*', 'x', 'axb'), ('ab*', '*', 'x', 'abx'), ('*ab', '*', 'x', 'xab'),
                      ('*', '*', 'x', 'x'), ('erlq', 'erlq', 'p', 'p'), ('abc', '', 'x', 'abc'),
                      ('', '*', 'x', ''), ('', '', 'x', ''), ('abc', 'z', 'x', 'abc'),
                      ('2*erlq*erlq', 'erlq', 'p', '2*p*p'), ('**', '*', '', '')):
    try:
        val = hr.call('erlRepl', s, o, n)
    except Exception as e:
        val = 'ERROR ' + str(e)
    check(val == want, 'R3 erlRepl(%r, %r, %r) = %r' % (s, o, n, val))
check(hr.call('erlShow', 'erlq*erlq', 'p') == 'p×p', 'R3 erlShow at the end and the start of the text: p×p')

# R4. small numbers
h = Harness(SRC); h.call('erlInit')
check(h.call('erlFix', 1e-9, 3.0) == '0.000' and h.call('erlFix', 0.0004, 3.0) == '0.000'
      and h.call('erlFix', 0.0996, 3.0) == '0.100' and h.call('erlFix', 2.9957, 4.0) == '2.9957',
      'R4 erlFix rounds first: 1E-9 -> 0.000, 0.0004 -> 0.000, 0.0996 -> 0.100, 2.9957 -> 2.9957')
ho = Harness(BETA1A); ho.call('erlInit')
check(ho.call('erlFix', 1e-9, 3.0) == '1.000ᴇ-9','R4 beta 1a in v3d: erlFix(1E-9, 3) = %r (the finding)' % ho.call('erlFix', 1e-9, 3.0))


def trawl_tiny(path):
    h = Harness(path, cas='giac'); h.call('erlInit')
    h.globals_['erlTm'] = 9.0; h.globals_['erlTN'] = 1.0
    h.call('erlTrDraw')
    h.press('Enter'); h.call('erlTrExact')
    return h, [t.text for s in h.screens for t in s.texts]


h, txt = trawl_tiny(SRC)
check('expected chance matches N × RMP = 0.000' in txt and any(x.endswith('μ = 0.000.') for x in txt)
      and not h.sci_strings, 'R4 1b trawl, N = 1, RMP 1 in a billion: "N × RMP = 0.000", "μ = 0.000", no scientific')
ho, txto = trawl_tiny(BETA1A)
check(any('1.000ᴇ-9' in x for x in txto), 'R4 beta 1a in v3d, the same trawl: %r'
      % [x for x in txto if 'ᴇ' in x][:1])


def rate_tiny(path):
    h = Harness(path); h.call('erlInit')
    h.globals_['erlP0'] = 0.0
    h.call('erlFit', 0.0)                         # 0 of 30: window 0-20 %, rate step 0.1 %
    h.call('erlSetP0', 0.0002)                    # a typed rate of 0.02 %
    return h, h.call('erlRateS', 0.0002), h.call('erlRateS', 0.05), h.call('erlRateS', 0.0)


h, a, b, c = rate_tiny(SRC)
check(a == '0.0200 %' and b == '5.0 %' and c == '0.0 %' and not h.sci_strings,
      'R4 1b erlRateS at 1 decimal: 0.0002 -> %r (erlPctS), 0.05 -> %r, 0 -> %r' % (a, b, c))
ho, a0, b0, c0 = rate_tiny(BETA1A)
check(a0 == '2.0ᴇ-2 %', 'R4 beta 1a in v3d: erlRateS(0.0002) = %r (the finding)' % a0)
# 0 of 50 tests: main window 0-20 % (rate step 0.1 %, one decimal), Bayes window 0-10 % (step 0.05 %).
# A typed rate of 0.02 % (main frame and Bayes page), then a drag on the Bayes page to its first step,
# 0.05 %, which one decimal cannot hold.
for path, tag in ((SRC, '1b'), (BETA1A, 'beta 1a')):
    h = Harness(path, cas='giac', seed=2)
    h.press('Enter')                                                 # welcome
    h.press('Enter'); h.choose(1); h.answer({'akN': 50, 'akK': 0, 'akA': 0.05})
    h.press('Enter'); h.choose(2); h.answer({'arP': 0.0002})        # menu > Set the true rate: 0.02 %
    h.tap(190, 230)                                                  # Bayes
    h.drag([(31, 100), (31, 101)])                                   # the Bayes page's first step
    h.tap(240, 230)                                                  # Back
    h.press('Esc')
    stops(lambda: h.call('ErrorRate'))
    ex = [t.text for s in h.pages for t in s.texts if 'true rate' in t.text]
    sci = sorted({t.text for s in h.pages for t in s.texts if 'ᴇ' in t.text})
    bmax = g(h, 'erlBMax'); pmax = g(h, 'erlPmax')
    if tag == '1b':
        check(h.error is None and not sci and not h.sci_strings and bmax == 0.1 and pmax == 0.2
              and any(x.startswith('An examiner whose true rate is 0.0200 %') for x in ex)
              and any(x.startswith('P(true rate > 0.0200 %)') for x in ex)
              and any(x.startswith('P(true rate > 0.1 %)') for x in ex),
              'R4 1b, 0 of 50, typed rate 0.02 %%, Bayes drag to 0.05 %%: no scientific text; %r'
              % sorted({x[:32] for x in ex})[:4])
    else:
        check(any('2.0ᴇ-2 %' in x for x in sci) and any('5.0ᴇ-2 %' in x for x in sci),
              'R4 beta 1a in v3d, the same session: %r' % [x[:34] for x in sci][:3])

# R5. beta 1b against beta 1a
_n1a = open(BETA1A, encoding='utf-8').read()
_n1b = open(SRC, encoding='utf-8').read()
_C0, _C1 = _bodies(_n1a), _bodies(_n1b)
_d = sorted(n for n in set(_C0) | set(_C1) if _C0.get(n) != _C1.get(n))
check(_d == ['ErrorRate', 'erlBayesDraw', 'erlCas', 'erlCasDraw', 'erlDrawText', 'erlEngPage', 'erlEq', 'erlFix',
             'erlPoiTerms', 'erlRateS', 'erlRepl', 'erlRuleEq', 'erlSimDraw', 'erlTrDraw', 'erlTrExact', 'erlWelcome'],
      'R5 1b (and 1c: + erlBayesDraw, erlCasDraw, erlEq, erlSimDraw, erlTrDraw, erlTrExact; 1d: + ErrorRate, '
      'erlDrawText, erlEngPage, erlPoiTerms, erlRuleEq, erlWelcome): routines that differ from beta 1a: %s' % _d)
check(_outside(_n1a, _d) == _outside(_n1b, _d), 'R5 1b: outside those routines only comments differ')
check(_re.findall(r'(?s)#PYTHON.*?#END', _n1a) == _re.findall(r'(?s)#PYTHON.*?#END', _n1b),
      'R5 1b: the #PYTHON block is byte-identical')
_ok = True
for nm in _C1:
    if nm not in _d and _C0.get(nm) != _C1[nm]:
        _ok = False
check(_ok, 'R5 1b: every other routine is identical to beta 1a (comments stripped)')
_raw0 = re.findall(r'(?ms)^(\w+)\([^\n]*\)\s*\nBEGIN\n.*?^END;', _n1a)
_body = lambda txt, nm: re.search(r'(?ms)^%s\([^\n]*\)\s*\nBEGIN\n.*?^END;' % nm, txt).group(0)
_same = [nm for nm in set(_raw0) if nm not in _d and _body(_n1a, nm) == _body(_n1b, nm)]
# 1d: 13 of the 16 names above are 1a routines this pattern reads (erlEq and erlRuleEq are new; ErrorRate is an
# EXPORT, which it does not read), so the count is 13 below 1a's, not 9
check(len(_same) == len(set(_raw0)) - 13, 'R5 1b: %d untouched routines are byte-identical, comments included' % len(_same))
print('  INSTRING sites in beta 1b: ' + ', '.join(str(i + 1) for i, l in enumerate(_n1b.splitlines()) if 'INSTRING(' in l and not l.strip().startswith('//')))

# R6. scientific STRING results, every run
mine = [(p, hh) for p, hh in ALLH if p == SRC]
sci = sorted({(round(v, 12), d, r) for p, hh in mine for v, d, r in hh.sci_strings})
other = sorted({(round(v, 12), d, r) for p, hh in ALLH if p != SRC for v, d, r in hh.sci_strings})
print('  harness runs: %d of beta 1c, %d of beta 1 / 1a' % (len(mine), len(ALLH) - len(mine)))
print('  h.sci_strings, beta 1c: %r' % sci)
print('  h.sci_strings, beta 1 / 1a (for comparison): %r' % other[:8])
check(not sci, 'R6 1b: no scientific STRING(x, 2, d) result in any of the %d beta 1c runs' % len(mine))

# ================================================================ T (1c)
print('\n== T. 1c: no "=" before a relation; the Bayes tail; "1 profile" (harness v3e) ==')
BETA1B = '/home/claude/work/out/ErrorRate_beta1b.txt'


def t_fresh(path, seed=1):
    h = Harness(path, cas='giac', seed=seed)
    h.call('erlInit')
    return h


def t_rec(h, n, k, am):
    h.globals_['erlN'] = float(n); h.globals_['erlK'] = float(k); h.globals_['erlAm'] = float(am)
    h.call('erlRecalc')


def t_bayes(path, n, k, rate):
    h = t_fresh(path); t_rec(h, n, k, 50); h.call('erlSetP0', rate); h.call('erlBayesCalc'); h.call('erlBayesDraw')
    return [t.text for t in h.texts if t.text.startswith('P(true rate >')][0]


def t_sim(path, n, k, rate):
    h = t_fresh(path); t_rec(h, n, k, 50); h.call('erlSetP0', rate)
    h.press('Esc'); h.call('erlSimPage')
    return [t.text for t in h.texts if t.text.startswith('exact chance')][0]


def t_trawl(path, tm, N):
    h = t_fresh(path); h.globals_['erlTm'] = float(tm); h.globals_['erlTN'] = float(N); h.call('erlTrDraw')
    h.press('Enter'); h.call('erlTrExact')
    tx = [t.text for t in h.texts]
    return ([x for x in tx if 'searched' in x][0], [x for x in tx if x.startswith('P(at least one chance')][0],
            [x for x in tx if x.startswith('At N = ')][0], [x for x in tx if x.startswith('1-e^(-')][0])


def t_cas(path, n, k, am):
    h = t_fresh(path); t_rec(h, n, k, am); h.press('Esc'); h.call('erlCasPage')
    return [t.text for t in h.texts if t.text.startswith('   p = ') or t.text.startswith('     = ')]


# T1. each display, beta 1b -> beta 1c
for args, old, new in (
        ((30, 0, 0.5), 'P(true rate > 50.0 %) = < 0.0001 %  (drag)', 'P(true rate > 50.0 %) < 0.0001 %  (drag)'),
        ((1000, 0, 0.3), 'P(true rate > 30.0 %) = 0 %  (drag)', 'P(true rate > 30.0 %) < 0.0001 %  (drag)'),
        ((30, 0, 1e-9), 'P(true rate > < 0.0001 %) = > 99.9999 %  (drag)', 'P(true rate > < 0.0001 %) > 99.9999 %  (drag)'),
        ((30, 0, 0.0), 'P(true rate > 0.0 %) = 100.0 %  (drag)', 'P(true rate > 0.0 %) = 100.0 %  (drag)'),
        ((30, 0, 0.05), None, None), ((50, 2, 0.04), None, None)):
    a, b = t_bayes(BETA1B, *args), t_bayes(SRC, *args)
    if old is None:
        check(a == b and ' = ' in b, 'T1 Bayes page %r: an ordinary value is unchanged: %r' % (args, b))
    else:
        check(a == old and b == new, 'T1 Bayes page n, k, rate = %r: beta 1b %r -> 1c %r' % (args, a, b))
for args, old, new in (
        ((30, 0, 0.5), 'exact chance (1 - p)^30 = < 0.0001 %', 'exact chance (1 - p)^30 < 0.0001 %'),
        ((30, 2, 0.6), 'exact chance (BINOMIAL_CDF) = < 0.0001 %', 'exact chance (BINOMIAL_CDF) < 0.0001 %'),
        ((1, 0, 1e-9), 'exact chance (1 - p)^1 = > 99.9999 %', 'exact chance (1 - p)^1 > 99.9999 %'),
        ((5, 1, 1e-7), 'exact chance (BINOMIAL_CDF) = > 99.9999 %', 'exact chance (BINOMIAL_CDF) > 99.9999 %'),
        ((30, 0, 0.05), 'exact chance (1 - p)^30 = 21.5 %', 'exact chance (1 - p)^30 = 21.5 %'),
        ((30, 2, 0.05), None, None)):
    a, b = t_sim(BETA1B, *args), t_sim(SRC, *args)
    if old is None:
        check(a == b and ' = ' in b, 'T1 simulation %r: an ordinary value is unchanged: %r' % (args, b))
    else:
        check(a == old and b == new, 'T1 simulation n, k, rate = %r: beta 1b %r -> 1c %r' % (args, a, b))
for args, old, new in (
        ((9, 1), ('N = 1 profiles searched', 'P(at least one chance match) = < 0.0001 %', 'At N = 1: P = < 0.0001 % exactly,',
                  '1-e^(-μ) = < 0.0001 %, μ = 0.000.'),
                 ('N = 1 profile searched', 'P(at least one chance match) < 0.0001 %', 'At N = 1: P < 0.0001 % exactly,',
                  '1-e^(-μ) < 0.0001 %, μ = 0.000.')),
        ((9, 2), ('N = 2 profiles searched', 'P(at least one chance match) = < 0.0001 %', 'At N = 2: P = < 0.0001 % exactly,',
                  '1-e^(-μ) = < 0.0001 %, μ = 0.000.'),
                 ('N = 2 profiles searched', 'P(at least one chance match) < 0.0001 %', 'At N = 2: P < 0.0001 % exactly,',
                  '1-e^(-μ) < 0.0001 %, μ = 0.000.')),
        ((3, 20000), ('N = 20,000 profiles searched', 'P(at least one chance match) = > 99.9999 %',
                      'At N = 20,000: P = > 99.9999 % exactly,', '1-e^(-μ) = > 99.9999 %, μ = 20.000.'),
                     ('N = 20,000 profiles searched', 'P(at least one chance match) > 99.9999 %',
                      'At N = 20,000: P > 99.9999 % exactly,', '1-e^(-μ) > 99.9999 %, μ = 20.000.')),
        ((6, 1000000), None, None)):
    a, b = t_trawl(BETA1B, *args), t_trawl(SRC, *args)
    if old is None:
        check(a == b and b[1] == 'P(at least one chance match) = 63.2 %',
              'T1 trawl RMP 1E-%d, N = %d: an ordinary panel is unchanged: %r' % (args + (b,)))
    else:
        check(a == old and b == new, 'T1 trawl RMP 1E-%d, N = %d: beta 1b %r -> 1c %r' % (args + (a, b)))
a, b = t_cas(BETA1B, 10000, 9999, 1), t_cas(SRC, 10000, 9999, 1)
check(a == ['   p = 1.00000 = > 99.9999 %'] and b == ['   p = 1.00000 > 99.9999 %'],
      'T1 "No closed form" page, 9999 errors in 10000 tests, alpha 0.001: beta 1b %r -> 1c %r' % (a, b))
for args in ((30, 2, 50), (100, 5, 10), (10000, 9998, 500)):
    a, b = t_cas(BETA1B, *args), t_cas(SRC, *args)
    check(a == b and all(' = ' in x for x in b), 'T1 "No closed form" page %r: ordinary, unchanged: %r' % (args, b))
a, b = t_cas(BETA1B, 10000, 0, 500), t_cas(SRC, 10000, 0, 500)
check(a == b == ['   p = 1-(1/2)^(1/10000)', '     = 0.00007 = 0.0069 %', '     = 0.6931'],
      'T1 "Where the 3 comes from" (k = 0), the smallest bound n 10000, alpha 0.5: unchanged %r' % b)

# T2. the Bayes tail: the mirrored Beta's lower tail is the same number as 1 - erlBetaCdf, and SciPy's
hb = t_fresh(SRC)
worst = 0.0
for a2, b2 in ((2, 62), (1, 61), (2, 2), (4, 98), (21, 41), (2, 2002), (200, 20)):
    for x in (0.001, 0.01, 0.05, 0.2, 0.5, 0.9):
        lo = hb.call('erlBetaCdf', float(b2), float(a2), 1 - x)
        hi = 1 - hb.call('erlBetaCdf', float(a2), float(b2), x)
        sf = stats.beta.sf(x, a2 / 2, b2 / 2)
        if sf > 1e-10:
            worst = max(worst, abs(lo - sf) / sf, abs(hi - lo))
check(worst < 1e-9, 'T2 P(Beta(a, b) > x) as erlBetaCdf(2b, 2a, 1 - x) = 1 - erlBetaCdf(2a, 2b, x) = SciPy '
      'beta.sf, 42 cases (worst %.1e)' % worst)
lo, sf = hb.call('erlBetaCdf', 2002.0, 2.0, 0.7), stats.beta.sf(0.3, 1, 1001)
check(abs(lo / sf - 1) < 1e-6 and 1 - hb.call('erlBetaCdf', 2.0, 2002.0, 0.3) == 0,
      'T2 0 of 1000, x = 30 %%: the mirrored tail is %.4g (SciPy %.4g); 1 - erlBetaCdf is exactly 0 even in doubles'
      % (lo, sf))
check(hb.call('erlBetaCdf', 62.0, 2.0, 1.0) == 1 and hb.call('erlBetaCdf', 62.0, 2.0, 0.0) == 0,
      'T2 the ends: P(rate > 0) = 1 and P(rate > 1) = 0, as before')

# T3. erlEq
e = [hb.call('erlEq', s) for s in ('< 0.0001 %', '> 99.9999 %', '2.15 %', '', '0 %', '100.0 %')]
check(e == [' < 0.0001 %', ' > 99.9999 %', ' = 2.15 %', ' = ', ' = 0 %', ' = 100.0 %'],
      'T3 erlEq: "< 0.0001 %%" -> " < 0.0001 %%", "> 99.9999 %%" -> " > 99.9999 %%", "2.15 %%" -> " = 2.15 %%", '
      '"" -> " = " (no error), "0 %%", "100.0 %%" -> " = ...": %r' % e)

# T4. the sites left alone cannot reach erlPctS's ends (the allowed inputs: n 1-10000, k 0-n, alpha 0.001-0.5,
# a and b 0.5-100 in halves, the simulation's M at most 10,000)
ht = t_fresh(SRC)
lo_r, hi_r, lo_u, hi_u = 1e9, 0, 1e9, 0
for am in (1, 2, 5, 10, 25, 50, 100, 250, 500):
    for n in (1, 2, 3, 4, 5, 6, 7, 10, 30, 100, 1000, 10000):
        t_rec(ht, n, 0, am)
        r = ht.globals_['erlRuleM'] / n
        lo_r, hi_r = min(lo_r, r), max(hi_r, r if r < 1 else 0)
        u = ht.globals_['erlPU']
        lo_u, hi_u = min(lo_u, u), max(hi_u, u)
check(lo_r > 1e-6 and lo_u > 1e-6 and hi_u < 0.999999 and hi_r < 0.999999,
      'T4 k = 0: the rule n / bound (%.2g to %.6f, or past 1) and the bound (%.2g to %.6f) stay inside erlPctS\'s '
      'ends, so "Rule: ... = ", "     = ... = " and the summary keep their "="' % (lo_r, hi_r, lo_u, hi_u))
bmin = 0.5 / (0.5 + 100 + 10000)
bmax = (100 + 10000) / (100 + 0.5 + 10000)
check(bmin > 1e-6 and bmax < 0.999999, 'T4 the Bayes mean (a+k)/(a+b+n) runs %.2g to %.6f: never past the ends'
      % (bmin, bmax))
check(1 / 10000 > 1e-6 and 9999 / 10000 < 0.999999, 'T4 a simulated share is 0, 1 or a multiple of 1/10000: '
      'never past the ends ("0 errors: ... = " keeps its "=")')

# T5. a whole session, beta 1b and 1c side by side: every text the same once 1b's "= <" / "= >" and
# "1 profiles" are written the 1c way
def t_rw(s):
    s2 = re.sub(r' = ([<>] )', r' \1', s)
    s2 = s2.replace('N = 1 profiles searched', 'N = 1 profile searched')
    s2 = s2.replace('  P(at least one) = ', '  P(1 or more) = ')        # 1d: E1
    return s2


T_DISC = 'Teaching aid; not for casework or legal use.'                  # 1d: the welcome page's new line


for seed in (3, 11):
    h0 = Harness(BETA1B, cas='giac', seed=seed); session(h0); stops(lambda: h0.call('ErrorRate'))
    h1 = Harness(SRC, cas='giac', seed=seed); session(h1); stops(lambda: h1.call('ErrorRate'))
    t0 = [t_rw(t.text) for t in h0.texts]
    t1 = [t.text for t in h1.texts if t.text != T_DISC]
    nrw = sum(1 for t in h0.texts if t_rw(t.text) != t.text)
    check(t0 == t1 and h0.result == h1.result and len(t1) > 100,
          'T5 the E session (seed %d): %d texts, identical to beta 1b\'s once %d "= <" / "= >" are written the 1c way'
          % (seed, len(t1), nrw))

# T6. the routine diff and the line diff, beta 1b -> 1c (1d: read from beta 1c's own file; U6 checks 1c -> 1d)
_n1c = open(BETA1C, encoding='utf-8').read()
_n1d = open(SRC, encoding='utf-8').read()
_n1b_ = open(BETA1B, encoding='utf-8').read()
_D0, _D1 = _bodies(_n1b_), _bodies(_n1c)
_dd = sorted(n for n in set(_D0) | set(_D1) if _D0.get(n) != _D1.get(n))
check(_dd == ['erlBayesDraw', 'erlCasDraw', 'erlEq', 'erlSimDraw', 'erlTrDraw', 'erlTrExact'],
      'T6 routines that differ from beta 1b: %s (erlEq new)' % _dd)
check(_outside(_n1b_, _dd) == _outside(_n1c, _dd), 'T6 outside them only comments differ')
check(_re.findall(r'(?s)#PYTHON.*?#END', _n1b_) == _re.findall(r'(?s)#PYTHON.*?#END', _n1c),
      'T6 the #PYTHON block is byte-identical')


def t_code(txt):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)
    out = []
    for l in c.split('\n'):
        o, ins = [], False
        for i, ch in enumerate(l):
            if ch == '"':
                ins = not ins
            if not ins and l[i:i + 2] == '//':
                break
            o.append(ch)
        s = ''.join(o).strip()
        if s:
            out.append(s)
    return out


import difflib as _dl
_mi, _pl = [], []
for op, i1, i2, j1, j2 in _dl.SequenceMatcher(None, t_code(_n1b_), t_code(_n1c), autojunk=False).get_opcodes():
    if op in ('replace', 'delete'):
        _mi += t_code(_n1b_)[i1:i2]
    if op in ('replace', 'insert'):
        _pl += t_code(_n1c)[j1:j2]
want_minus = [
    'erlAdd("   p = " + erlFix(erlPU, 5) + " = " + erlPctS(erlPU), erlRED);',
    'bwV := 1 - erlBetaCdf(bwA2, bwB2, erlP0);',
    'TEXTOUT_P("P(true rate > " + erlRateS(erlP0) + ") = " + erlPctS(bwV) + "  (drag)", G1, 2, 205, 1, erlORNG, 316);',
    'TEXTOUT_P("exact chance (1 - p)^" + erlIStr(erlSmN) + " = " + erlPctS(erlTail(erlSmN, erlSmP, 0)), G1, 2, 189, 1, erlMAG, 316);',
    'TEXTOUT_P("exact chance (BINOMIAL_CDF) = " + erlPctS(erlTail(erlSmN, erlSmP, erlSmK)), G1, 2, 189, 1, erlMAG, 316);',
    'TEXTOUT_P("N = " + erlComma(erlTN) + " profiles searched", G1, 2, 181, 1, erlRED, 316);',
    'TEXTOUT_P("P(at least one chance match) = " + erlPctS(twP), G1, 2, 193, 1, erlBLUE, 316);',
    'erlAdd("At N = " + erlComma(erlTN) + ": P = " + erlPctS(erlTrP(erlTN)) + " exactly,", erlRED);',
    'erlAdd("1-e^(-" + erlMuS + ") = " + erlPctS(1 - EXP(-teM)) + ", " + erlMuS + " = " + erlFix(teM, 3) + ".", erlRED);']
want_plus = [
    'erlEq(eqS)', 'BEGIN', 'IF DIM(eqS) > 0 THEN',
    'IF LEFT(eqS, 1) == "<" OR LEFT(eqS, 1) == ">" THEN RETURN " " + eqS; END;', 'END;', 'RETURN " = " + eqS;', 'END;',
    'erlAdd("   p = " + erlFix(erlPU, 5) + erlEq(erlPctS(erlPU)), erlRED);',
    'bwV := erlBetaCdf(bwB2, bwA2, 1 - erlP0);',
    'TEXTOUT_P("P(true rate > " + erlRateS(erlP0) + ")" + erlEq(erlPctS(bwV)) + "  (drag)", G1, 2, 205, 1, erlORNG, 316);',
    'TEXTOUT_P("exact chance (1 - p)^" + erlIStr(erlSmN) + erlEq(erlPctS(erlTail(erlSmN, erlSmP, 0))), G1, 2, 189, 1, erlMAG, 316);',
    'TEXTOUT_P("exact chance (BINOMIAL_CDF)" + erlEq(erlPctS(erlTail(erlSmN, erlSmP, erlSmK))), G1, 2, 189, 1, erlMAG, 316);',
    'TEXTOUT_P("N = " + erlComma(erlTN) + IFTE(erlTN == 1, " profile searched", " profiles searched"), G1, 2, 181, 1, erlRED, 316);',
    'TEXTOUT_P("P(at least one chance match)" + erlEq(erlPctS(twP)), G1, 2, 193, 1, erlBLUE, 316);',
    'erlAdd("At N = " + erlComma(erlTN) + ": P" + erlEq(erlPctS(erlTrP(erlTN))) + " exactly,", erlRED);',
    'erlAdd("1-e^(-" + erlMuS + ")" + erlEq(erlPctS(1 - EXP(-teM))) + ", " + erlMuS + " = " + erlFix(teM, 3) + ".", erlRED);']
check(sorted(_mi) == sorted(want_minus) and sorted(_pl) == sorted(want_plus),
      'T6 the code lines that changed are exactly the 9 listed (and erlEq\'s 7): -%r +%r'
      % ([x for x in _mi if x not in want_minus], [x for x in _pl if x not in want_plus]))

# T7. names, INSTRING, version strings, comments
BIN = set(l.strip().lower() for l in open('/home/claude/work/gate_r2/HP_Prime_Builtin_Names.txt', encoding='utf-8')
          if l.strip() and not l.startswith('#'))
check(not any(n.lower() in BIN for n in ('erlEq', 'eqS')) and 'erlEq'.startswith('erl'),
      'T7 the new names erlEq and eqS are not built-ins (case ignored); erlEq carries the erl tag')
ins_b = [l for l in t_code(_n1b_) if 'INSTRING(' in l]
ins_c = [l for l in t_code(_n1d) if 'INSTRING(' in l]        # 1d: beta 1d's lines
check(ins_b == ins_c and len(ins_c) == 3, 'T7 INSTRING: the same 3 guarded lines as beta 1b (erlRepl 2, erlCas 1); '
      'erlEq reads LEFT(eqS, 1) inside IF DIM(eqS) > 0')
# 1d: the version strings are beta 1d's now (the expected text moved with the version)
L1d = _n1d.split('\n')
check(L1d[3] == '// ERRORRATE LAB - beta 1d' and 'Beta 1b, 1c and 1d have not run there yet' in _n1d
      and '(beta 1d has run only\n//   in the PC harness)' in _n1d
      and 'in the ppl_run_v3e harness (verify_ErrorRate_beta1d.py).' in _n1d
      and '// Companion files: ErrorRate_beta1d_CHANGES.md (beta 1d),' in _n1d
      and '//   ErrorRate_beta1c_CHANGES.md (beta 1c),' in _n1d and '// beta 1c (17 Oct 2026):' in _n1d
      and '// What changed in beta 1d (19 Oct 2026): E1, E2, E4, E5 (fleet' in _n1d
      and 'verify_ErrorRate_beta1c.py' not in _n1d,
      'T7 version strings (1d: beta 1d\'s): the banner, the tested-on line, the harness and verify names, the companion '
      'files, the beta 1d paragraph')
def t_comment_in_bracket(src):
    depth, bad = 0, []
    for n_, l in enumerate(src.split('\n'), 1):
        ins, start = False, depth
        for i, ch in enumerate(l):
            if ch == '"':
                ins = not ins
            elif not ins:
                if l[i:i + 2] == '//':
                    if start > 0:
                        bad.append(n_)
                    break
                if ch in '({[':
                    depth += 1
                elif ch in ')}]':
                    depth -= 1
    return bad


check(not t_comment_in_bracket(_re.sub(r'(?s)#PYTHON.*?#END', '', _n1d)),
      'T7 no // comment inside an open bracket (the Prime rejects it; 1d: beta 1d): %r' % t_comment_in_bracket(_n1d)[:5])

# T8. scientific fixed decimals in the 1c runs of this section
mine2 = [(p, hh) for p, hh in ALLH if p == SRC]
sci2 = sorted({(round(v, 12), d, r) for p, hh in mine2 for v, d, r in hh.sci_strings})
check(not sci2, 'T8 no scientific STRING(x, 2, d) result in any of the %d beta 1c runs (section T included)' % len(mine2))


# ================================================================ U (1d)
print('\n== U. 1d: fleet review E1, E2, E4, E5; the disclaimer (harness v3e) ==')
import subprocess as _sp


def u_fresh(path, cas='giac', seed=1, text=None):
    h = Harness(path, cas=cas, seed=seed) if text is None else Harness(text=text, cas=cas, seed=seed)
    h.call('erlInit')
    return h


def u_pagelines(h):
    """the font-1 lines of the last text page (title, badge and footer left out)"""
    return [t.text for t in h.pages[-1].texts if t.font == 1 and t.y not in (10, 220)]


# U1 (E1). The trawl's Exact page, every RMP the menu offers (1 in 1,000 ... 1 in 1 billion: erlTm 3..9),
# CAS answering (giac) and failing.  The review's check 3c, as a regression test.
_rmp_menu = _re.search(r'CHOOSE\(arI, "Random match probability", \{(.*?)\}\);', _n1d, _re.S).group(1)
check(_rmp_menu.count('"1 in ') == 7 and 'erlTm := arI + 2;' in _n1d,
      'U1 the RMP menu offers 7 values, erlTm = 3 .. 9 (1 in 1,000 ... 1 in 1 billion)')
for path, tag in ((BETA1C, '1c'), (SRC, '1d')):
    for cas in ('giac', 'fail'):
        lost, rows = [], []
        for tm in range(3, 10):
            for tn in (1.0, 1e6, 1e8):
                h = u_fresh(path, cas)
                h.globals_['erlTm'] = float(tm); h.globals_['erlTN'] = tn
                h.press('Enter'); h.call('erlTrExact')
                ls = u_pagelines(h)
                pl = [l for l in ls if l.startswith('  P(at least one) = ') or l.startswith('  P(1 or more) = ')]
                ok = (any(l == 'RMP values are illustrative, not casework.' for l in ls) and len(pl) == 1
                      and pl[0].endswith('^N') and h.globals_['erlPgN'] == 14 and all(len(l) <= 46 for l in ls))
                if not ok:
                    lost.append((tm, tn, h.globals_['erlPgN'], pl[:1]))
                if tn == 1e6:
                    rows.append(pl[0] if pl else None)
        if tag == '1c' and cas == 'giac':
            check(len(lost) == 3 and all(x[0] == 9 for x in lost),
                  'U1 beta 1c, CAS answering: at RMP 1 in a billion (any N) the answer wraps and "RMP values are '
                  'illustrative, not casework." is dropped (the review\'s E1): %r' % lost[:1])
        else:
            check(not lost, 'U1 beta %s, CAS %s: 7 RMPs x N 1 / 1E6 / 1E8: 14 lines, the answer on ONE line, the '
                  'closing line present, every line 46 characters or fewer %r' % (tag, 'answering' if cas == 'giac'
                                                                                   else 'failing', lost[:2]))
        if tag == '1d':
            print('   1d, CAS %s: %s' % (cas, rows[-1]))
# a Prime that printed the answer the other way round, -(999999999/1000000000)^N+1 (27 characters), still fits
h = u_fresh(SRC)
h.call('erlPgReset'); h.call('erlAddW', '  P(1 or more) = ', '-(999999999/1000000000)^N+1', 0.0)
check(h.globals_['erlPgN'] == 1, 'U1 the prefix leaves 27 characters: a 27-character answer '
      '"-(999999999/1000000000)^N+1" still takes one line')

# U2 (E2). The rule line at 100 % or more.
def u_panel(path, n, k, am):
    h = u_fresh(path, 'fail')
    setrec(h, n, k, am); h.call('erlFit', 0.0); h.call('erlDrawMain', 1.0)
    return [t.text for t in h.pages[-1].texts if t.y == 205][0]


for n, k, am, old, new in (
        (30, 29, 50, '39.54/n = 131.8 %, n × bound = 29.95 → 39.54', '39.54/n is 100 % or more: no use at this k, n'),
        (1, 0, 50, '3/n = 300.0 %, n × bound = 0.95 → 3.00', '3/n is 100 % or more: no use at this k, n'),
        (2, 0, 50, '3/n = 150.0 %, n × bound = 1.55 → 3.00', '3/n is 100 % or more: no use at this k, n'),
        (3, 0, 50, '3/n = 100.0 %, n × bound = 1.89 → 3.00', '3/n is 100 % or more: no use at this k, n'),
        (4, 1, 50, '4.74/n = 118.6 %, n × bound = 3.01 → 4.74', '4.74/n is 100 % or more: no use at this k, n'),
        (4, 0, 50, '3/n = 75.0 %, n × bound = 2.11 → 3.00', None),
        (30, 0, 50, '3/n = 10.0 %, n × bound = 2.85 → 3.00', None),
        (750, 2, 10, '8.41/n = 1.12 %, n × bound = 8.37 → 8.41', None)):
    a, b = u_panel(BETA1C, n, k, am), u_panel(SRC, n, k, am)
    if new is None:
        check(a == old and b == old, 'U2 panel, %d errors in %d, alpha %.3f: ordinary, unchanged: %r' % (k, n, am / 1000, b))
    else:
        check(a == old and b == new, 'U2 panel, %d errors in %d: beta 1c %r -> 1d %r' % (k, n, a, b))
for n, old, new in ((1, 'Rule: 3/n = 300.0 %.  n × bound = 0.950.', 'Rule: 3/n is 100 % or more: no use here.'),
                    (3, 'Rule: 3/n = 100.0 %.  n × bound = 1.895.', 'Rule: 3/n is 100 % or more: no use here.'),
                    (4, 'Rule: 3/n = 75.0 %.  n × bound = 2.109.', None)):
    rr = []
    for path in (BETA1C, SRC):
        h = u_fresh(path, 'giac'); setrec(h, n, 0, 50); h.call('erlCasFill'); h.call('erlCasDraw')
        rr.append([l for l in u_pagelines(h) if l.startswith('Rule: ')][0])
    check(rr == [old, new or old], 'U2 "Why 3" page, 0 errors in %d: beta 1c %r -> 1d %r' % (n, rr[0], rr[1]))
# alpha 0.001 (6.91/n) at n = 6: the longest k = 0 Rule line
h = u_fresh(SRC, 'giac'); setrec(h, 6, 0, 1); h.call('erlCasFill'); h.call('erlCasDraw')
rl = [l for l in u_pagelines(h) if l.startswith('Rule: ')][0]
check(rl == 'Rule: 6.91/n is 100 % or more: no use here.' and len(rl) <= 46, 'U2 alpha 0.001, n = 6: %r' % rl)
# the summary returned to Home
sm = []
for path in (BETA1C, SRC):
    h = Harness(path, cas='fail', seed=1)
    h.press('Enter'); h.tap(20, 230); h.answer({'akN': 30, 'akK': 29, 'akA': 0.05}); h.press('Esc')
    h.call('ErrorRate'); sm.append(h.result)
check(sm == ['ErrorRate: 29 errors in 30 tests -> 95 % upper bound 99.8 % (39.54/n = 131.8 %); see ER_UPPER',
             'ErrorRate: 29 errors in 30 tests -> 95 % upper bound 99.8 % (39.54/n is 100 % or more); see ER_UPPER'],
      'U2 the summary to Home at 29 errors in 30: beta 1c %r -> 1d %r' % tuple(sm))
# the sweep: every alpha the menu offers x n 1..60 (and 4 large n) x k: erlRuleEq never prints a rate of 100 % or more,
# and never "= >"; beta 1c printed one in the states counted below
h = u_fresh(SRC, 'fail')
h0 = u_fresh(BETA1C, 'fail')
bad, n_over, n_st = [], 0, 0
for am in (1, 10, 25, 50, 100, 500):
    for n in list(range(1, 61)) + [100, 1000, 9999, 10000]:
        for k in sorted({0, 1, 2, 5, n - 1}):
            if k < 0 or k >= n:
                continue
            setrec(h, n, k, am)
            r = h.globals_['erlRuleM'] / h.globals_['erlN']
            s = h.call('erlRuleEq')
            n_st += 1
            if r >= 1:
                n_over += 1
                ok = s == ' is 100 % or more'
                setrec(h0, n, k, am)
            else:
                pct = re.search(r'([\d.]+) %', s)
                ok = (s.startswith(' = ') or s.startswith(' > ')) and ' = >' not in s and ' = <' not in s \
                    and pct is not None and float(pct.group(1)) < 100
            if not ok:
                bad.append((am, n, k, s))
check(not bad and n_over > 0, 'U2 sweep of %d records (6 alphas, n 1..60 and 100..10000): the %d whose rule is 100 %% or '
      'more say so, the rest print a rate below 100 %% with "=" or ">" alone %r' % (n_st, n_over, bad[:3]))
h.globals_['erlRuleM'] = 0.9999995; h.globals_['erlN'] = 1.0
h0.globals_['erlRuleM'] = 0.9999995; h0.globals_['erlN'] = 1.0
old_s = ' = ' + h0.call('erlPctS', 0.9999995)
check(h.call('erlRuleEq') == ' > 99.9999 %' and old_s == ' = > 99.9999 %',
      'U2 a rule just under 100 %% reads " > 99.9999 %%" (beta 1c\'s form would be %r)' % old_s)
# the widest panel line: 9999 errors in 10000 tests at alpha 0.001
pl = u_panel(SRC, 10000, 9999, 1)
check(pl.endswith(' is 100 % or more: no use at this k, n') and 2 + 5.5 * len(pl) <= 318,
      'U2 the widest rule line (9999 of 10000, alpha 0.001): %r, %d characters' % (pl, len(pl)))

# U3 (E4). The Engines page's CAS line.
def u_eng(path, cas, before):
    h = u_fresh(path, cas)
    before(h)
    h.press('Enter'); h.call('erlEngPage')
    return [t.text for t in h.pages[-1].texts if t.text.startswith('CAS (exact text): ')][0]


def u_k7(h):
    setrec(h, 30, 7, 50); h.call('erlCasFill')


def u_k0(h):
    setrec(h, 30, 0, 50); h.call('erlCasFill')


def u_bayes(h):
    h.call('erlBayesCalc')


def u_trawl(h):
    h.press('Enter'); h.call('erlTrExact')


for tag, cas, fn, old, new in (
        ('nothing opened', 'giac', lambda h: None, 'not called yet', 'not called yet'),
        ('nothing opened, CAS failing', 'fail', lambda h: None, 'not called yet', 'not called yet'),
        ('"Why 3" at k = 7 (asks for alpha, shows no CAS lines)', 'giac', u_k7, 'not called yet',
         'called, no Why 3 CAS lines'),
        ('the Bayes page only', 'giac', u_bayes, 'not called yet', 'called, no Why 3 CAS lines'),
        ('the trawl\'s Exact page only, CAS failing', 'fail', u_trawl, 'not called yet', 'called, no Why 3 CAS lines'),
        ('"Why 3" at k = 0', 'giac', u_k0, 'exact on the last page', 'exact on the last page'),
        ('"Why 3" at k = 0, CAS failing', 'fail', u_k0, 'FAILED on the last page', 'FAILED on the last page')):
    a, b = u_eng(BETA1C, cas, fn), u_eng(SRC, cas, fn)
    check(a == 'CAS (exact text): ' + old and b == 'CAS (exact text): ' + new and len(b) <= 46,
          'U3 Engines page after %s: beta 1c %r -> 1d %r' % (tag, a, b))

# U4 (E5). erlPoiTerms.
pt = {}
for path, tag in ((BETA1C, '1c'), (SRC, '1d')):
    h = u_fresh(path, 'fail')
    for k in range(1, 7):
        setrec(h, 30, k, 50)
        pt[(tag, k)] = h.call('erlPoiTerms')
check(all(pt[('1c', k)] == pt[('1d', k)] for k in range(1, 7))
      and pt[('1d', 1)] == '(1-erll/erlq)^erlq+erlq/1*(erll/erlq)^1*(1-erll/erlq)^(erlq-1)',
      'U4 erlPoiTerms: beta 1d\'s text = beta 1c\'s for k = 1..6 (k = 1: %r)' % pt[('1d', 1)])
# a Prime whose FOR ran once when its finish is below its start: modelled by MAX(1, finish) in a copy of each file
FOR_OLD = 'FOR ptI FROM 1 TO ptJ - 1 DO'
FOR_ONE = 'FOR ptI FROM 1 TO MAX(1, ptJ - 1) DO'
mt = {}
for path, tag in ((BETA1C, '1c'), (SRC, '1d')):
    txt = open(path, encoding='utf-8').read()
    assert txt.count(FOR_OLD) == 1
    h = u_fresh(None, 'giac', text=txt.replace(FOR_OLD, FOR_ONE))
    for k in range(1, 7):
        setrec(h, 30, k, 50)
        mt[(tag, k)] = h.call('erlPoiTerms')
    setrec(h, 30, 1, 50); h.call('erlCasFill'); h.call('erlCasDraw')
    mt[(tag, 'badge')] = [t.text for t in h.pages[-1].texts if t.x == 236]
    mt[(tag, 'ca3')] = h.globals_['erlCa3']
check(mt[('1c', 1)] != pt[('1c', 1)] and '*(erlq-1)/1*' in mt[('1c', 1)],
      'U4 beta 1c with a FOR that runs once: the k = 1 text gains a false factor: %r' % mt[('1c', 1)])
check(all(mt[('1d', k)] == pt[('1d', k)] for k in range(1, 7)) and mt[('1d', 'badge')] == ['exact (CAS)']
      and mt[('1d', 'ca3')] == 'e^(-erll)*(erll+1)',
      'U4 beta 1d with the same FOR: every k = 1..6 text unchanged; the k = 1 page still exact, %r (beta 1c\'s copy: '
      'erlCa3 = %r, badge %r)' % (mt[('1d', 'ca3')], mt[('1c', 'ca3')], mt[('1c', 'badge')]))

# U5. The disclaimer (Roger, 19 Oct 2026, 12:48): in the header, and on the opening page.
DISC = ('DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely '
        'on its results for legal purposes.')


def u_header(txt):
    hdr = txt.split('// Run ErrorRate() from the Program Catalog.')[0]
    return ' '.join(l.lstrip('/').strip() for l in hdr.split('\n') if l.startswith('//'))


check(DISC in u_header(_n1d) and DISC not in u_header(_n1c),
      'U5 the header carries the disclaimer, word for word, beside the distribution terms (beta 1c: no)')
wl = []
for path in (BETA1C, SRC):
    h = u_fresh(path, 'fail'); h.press('Enter'); h.call('erlWelcome')
    wl.append([t for t in h.pages[-1].texts])
d1 = [t for t in wl[1] if t.text == T_DISC]
check(len(d1) == 1 and not [t for t in wl[0] if t.text == T_DISC] and d1[0].font == 1 and d1[0].y == 29
      and 14 + 6.5 * len(T_DISC) <= 14 + 296 and d1[0].hex == '#FF0000',
      'U5 the opening page shows "%s" (font 1, red, y 29, %d characters: within the 296-px width at 6.5 px a '
      'character); beta 1c does not' % (T_DISC, len(T_DISC)))
others = [t for t in wl[1] if t.text != T_DISC]
check([(t.text, t.y) for t in others] == [(t.text, t.y) for t in wl[0]] and
      max(t.y for t in others if t.y < 29) == 10 and min(t.y for t in others if t.y > 29) == 44,
      'U5 the rest of the opening page is unchanged; the line sits between the title (y 10, font 4) and y 44')
h = Harness(SRC, cas='fail', seed=1); h.press('Enter', 'Esc'); h.call('ErrorRate')
check(any(t.text == T_DISC for t in h.pages[0].texts) and h.pages[0].func == 'erlWelcome',
      'U5 ErrorRate() shows it on its first screen')
check('"RMP values are illustrative, not casework."' in _n1d, 'U5 the trawl page keeps "RMP values are illustrative, '
      'not casework."')

# U6. The routine diff and the code-line diff, beta 1c -> 1d.
_E0, _E1 = _bodies(_n1c), _bodies(_n1d)
_ed = sorted(n for n in set(_E0) | set(_E1) if _E0.get(n) != _E1.get(n))
check(_ed == ['ErrorRate', 'erlCasDraw', 'erlDrawText', 'erlEngPage', 'erlPoiTerms', 'erlRuleEq', 'erlTrExact', 'erlWelcome'],
      'U6 routines that differ from beta 1c: %s (erlRuleEq new)' % _ed)
check(_outside(_n1c, _ed) == _outside(_n1d, _ed), 'U6 outside them only comments differ')
check(_re.findall(r'(?s)#PYTHON.*?#END', _n1c) == _re.findall(r'(?s)#PYTHON.*?#END', _n1d),
      'U6 the #PYTHON block is byte-identical')
_mi, _pl = [], []
for op, i1, i2, j1, j2 in _dl.SequenceMatcher(None, t_code(_n1c), t_code(_n1d), autojunk=False).get_opcodes():
    if op in ('replace', 'delete'):
        _mi += t_code(_n1c)[i1:i2]
    if op in ('replace', 'insert'):
        _pl += t_code(_n1d)[j1:j2]
want_minus = [
    'txS := erlRuleS() + " = " + erlPctS(erlRuleM / erlN) + ", n " + erlTms + " bound = " + erlFix(erlN * erlPU, 2) + " " + erlArr + " " + erlFix(erlRul, 2);',
    'erlAdd("Rule: " + erlRuleS() + " = " + erlPctS(erlRuleM / erlN) + ".  n " + erlTms + " bound = " + erlFix(erlN * erlPU, 3) + ".", erlBLK);',
    'erlAddW("  P(at least one) = ", teS, erlMAG);',
    'RETURN "ErrorRate: " + erlRecS() + " -> " + erlLvS() + " % upper bound " + erlPctS(erlPU) + " (" + erlRuleS() + " = " + erlPctS(erlRuleM / erlN) + "); see ER_UPPER";']
want_plus = [
    'erlRuleEq()', 'BEGIN', 'IF erlRuleM / erlN >= 1 THEN RETURN " is 100 % or more"; END;',
    'RETURN erlEq(erlPctS(erlRuleM / erlN));', 'END;',
    'IF erlRuleM / erlN >= 1 THEN', 'txS := erlRuleS() + erlRuleEq() + ": no use at this k, n";', 'ELSE',
    'txS := erlRuleS() + erlRuleEq() + ", n " + erlTms + " bound = " + erlFix(erlN * erlPU, 2) + " " + erlArr + " " + erlFix(erlRul, 2);',
    'END;',
    'IF ptJ > 1 THEN', 'END;',
    'IF erlRuleM / erlN >= 1 THEN', 'erlAdd("Rule: " + erlRuleS() + erlRuleEq() + ": no use here.", erlBLK);', 'ELSE',
    'erlAdd("Rule: " + erlRuleS() + erlRuleEq() + ".  n " + erlTms + " bound = " + erlFix(erlN * erlPU, 3) + ".", erlBLK);',
    'END;',
    'erlAddW("  P(1 or more) = ", teS, erlMAG);',
    'LOCAL egN0;', 'egN0 := erlCasN;', 'IF egN0 > 0 THEN egS := "called, no Why 3 CAS lines"; END;',
    'TEXTOUT_P("Teaching aid; not for casework or legal use.", G1, 14, 29, 1, erlRED, 296);',
    'RETURN "ErrorRate: " + erlRecS() + " -> " + erlLvS() + " % upper bound " + erlPctS(erlPU) + " (" + erlRuleS() + erlRuleEq() + "); see ER_UPPER";']
check(sorted(_mi) == sorted(want_minus) and sorted(_pl) == sorted(want_plus),
      'U6 the code lines that changed are exactly the 4 removed and the 23 added listed here: -%r +%r'
      % ([x for x in _mi if x not in want_minus], [x for x in _pl if x not in want_plus]))
check(_n1d.index('\nerlRuleEq()') > _n1d.index('\nerlEq(eqS)') and _n1d.index('\nerlRuleEq()') > _n1d.index('\nerlPctS(')
      and _n1d.index('\nerlRuleEq()') < _n1d.index('erlRuleEq()', _n1d.index('\nerlRuleEq()') + 5),
      'U6 erlRuleEq is defined after erlPctS and erlEq and before its first use')

# U7. Names and static rules.
check(not any(n.lower() in BIN for n in ('erlRuleEq', 'egN0')) and 'erlRuleEq'.startswith('erl'),
      'U7 the new names erlRuleEq and egN0 are not built-ins (case ignored); erlRuleEq carries the erl tag')
_loc = [l for l in t_code(_n1d) if l.startswith('LOCAL ')]
_big = [l for l in _loc if len([x for x in l[6:].rstrip(';').split(',') if x.strip()]) > 6 and ':=' not in l]
check(not _big, 'U7 no LOCAL line declares more than 6 names: %r' % _big[:2])
check(not t_comment_in_bracket(_re.sub(r'(?s)#PYTHON.*?#END', '', _n1d)),
      'U7 no // comment inside an open bracket')
check(all(ord(c) < 128 for c in _n1d), 'U7 the file is still pure ASCII (glyphs are built with CHAR())')
check([l for l in t_code(_n1d) if 'INSTRING(' in l] == [l for l in t_code(_n1c) if 'INSTRING(' in l],
      'U7 INSTRING: the same guarded lines as beta 1c')
check(not _re.search(r'MAKELIST\([^)]*,\s*K\s*,', '\n'.join(_pl)), 'U7 no new MAKELIST uses Home\'s K')

# U8. The review's own check script (review/check_ErrorRate.py), run on beta 1c and on beta 1d.
_chk = open('/home/claude/work/review/check_ErrorRate.py', encoding='utf-8').read()
_chk = _chk.replace("HERE = os.path.dirname(os.path.abspath(__file__))", "HERE = '/home/claude/work/review'")
rv = {}
for path, tag in ((BETA1C, '1c'), (SRC, '1d')):
    src_ = _chk.replace("SRC = os.path.join(FLEET, 'ErrorRate_beta1c.txt')", 'SRC = %r' % path)
    assert src_ != _chk
    out = _sp.run([sys.executable, '-'], input=src_, capture_output=True, text=True, timeout=1800).stdout
    rv[tag] = (re.search(r'(\d+) checks failed', out).group(1), [l for l in out.split('\n') if l.startswith('FAIL ')])
print('   review check_ErrorRate.py: beta 1c %s failed %r; beta 1d %s failed %r' % (rv['1c'][0], rv['1c'][1], rv['1d'][0],
                                                                                    rv['1d'][1]))
check(rv['1c'][0] == '1' and 'illustrative' in rv['1c'][1][0] and rv['1d'][0] == '0',
      'U8 the review\'s check_ErrorRate.py: beta 1c fails its E1 check (1 failure), beta 1d passes all of it')

# U9. Scientific fixed decimals: every beta 1d run in this script.
mine3 = [(p, hh) for p, hh in ALLH if p == SRC or (p is None and hh.files == [])]
sci3 = sorted({(round(v, 12), d, r) for p, hh in ALLH if p == SRC for v, d, r in hh.sci_strings})
print('   h.sci_strings over the %d beta 1d runs: %r' % (len([1 for p, hh in ALLH if p == SRC]), sci3))
check(not sci3, 'U9 no scientific STRING(x, 2, d) result in any beta 1d run of this script (sections A-U)')

if FAILS:
    print('\n%d FAILED' % len(FAILS))
    for f in FAILS:
        print('  - ' + f)
    sys.exit(1)
print('\n%d checks, ALL PASS' % _NCHK[0])
