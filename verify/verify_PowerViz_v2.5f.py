#!/usr/bin/env python3
"""verify_PowerViz_v2.5d.py -- checks PowerViz v2.5d (19 Oct 2026): the fleet review's P1 (no closed-form n when
its bracket is not positive) and the "POWER > 0.999" top floor in pv_FMTP, and Roger's disclaimer (19 Oct).  Built
from verify_PowerViz_v2.5c.py: every check below runs on v2.5d (PROG), on harness v3e.  Where an old check's
expected value moves with v2.5d it says so:
  R5  the routines that differ from v2.5a now include v2.5d's pv_FMTP, pv_Formula, pv_NCF, pv_ShowHelp.
  T1  a probability that rounds to 1 now prints "> 0.999": the exit box's "POWER = 1.0000" is "POWER > 0.9999",
      and beta 0.9998 on the panel "β > 0.999" (it read "β = 1.000").
  T5  checks the v2.5b -> v2.5c diff, so it reads v2.5c's own file (V25C); U5 checks v2.5c -> v2.5d.  Its version
      strings, bracket and INSTRING checks read v2.5d.
New section U (v2.5d against v2.5c, both in the harness):
  U1  P1: the closed-form n where zα u + zβ w is not positive (a 1-sided alpha above 0.5), all four tests: no
      bracket on the panel, the formula page says there is no root and why; a sweep of 4 tests x 2 tails x 10 alphas
      x 4 effects against the replica; ordinary cases unchanged.
  U2  the top floor: pv_FMTP at its edges; the big POWER, the exit box, the plot labels and the Pow-n readout;
      a sweep: no display reads POWER 1.000 or "= >" / "= <".
  U3  the disclaimer: in the header, and on help page 1.
  U4  the review's own check_PowerViz.py on v2.5c and on v2.5d.
  U5  the routine diff and the code-line diff, v2.5c -> v2.5d; names; version strings.
  U6  h.sci_strings from every v2.5d run.

(v2.5c's docstring follows.)

verify_PowerViz_v2.5c.py -- checks PowerViz v2.5c (17 Oct 2026, evening): no "=" before a relation (pv_Rel) and
beta as a probability of its own (pv_BetaS), never 1 - PW = 0.  Built from verify_PowerViz_v2.5b.py: every check
below runs on v2.5c, on harness v3e (v3d's results; its README); R5's list of routines that differ from v2.5a
now includes v2.5c's.  The new section T checks v2.5c against v2.5b:
  T1. each fixed display reached in the harness, before and after (the panel, the tails hint, the exit box, both
      curve views); ordinary values unchanged.  T2. pv_BetaS over 1152 states: v2.5b's text wherever 1 - PW had
      its digits, else the floor; beta itself against SciPy.  T3. pv_Rel.  T4. the sites left alone: the drag
      clamp, and the plot labels never drawn below 0.01.  T5. the routine and line diff, names, version strings,
      comments, INSTRING.  T6. no scientific fixed decimals in any v2.5c run.

(v2.5b's docstring follows.)

verify_PowerViz_v2.5b.py -- checks PowerViz v2.5b (17 Oct 2026): the string fixes after the second
emulator round (INSTRING("", ...) is "Invalid input" on the Prime; STRING(x, 2, d) prints scientific when
0 < |x| < 10^-d).  Built from verify_PowerViz_v2.5a.py: every check below is kept and now runs on harness
v3d (/home/claude/work/out/ppl_run_v3e.py), which models both facts -- B12 runs v2.4's script on v2.5b in
v3d too; G compares v2.5 with v2.5a as before.  The new section R checks v2.5b:
  R1. pv_Cas after a failed CAS call returns "" with no error; v2.5a in v3d stops there.
  R2. cas='fail', end to end: the formula page for every test (both tails for test 2), the menu route and
      the no-effect case open with "decimal" and the textbook form, no error; v2.5a in v3d stops on
      every one of them ("INSTRING: Invalid input").
  R3. pv_Rep directly: a pattern at the end, at the start, the whole string, an empty pattern, an empty
      text, absent, repeated; pv_Strip on "", "{}", "list[...]"; and the formula page with a canned CAS
      answer that ENDS with a CAS name (the emulator's TrendTest / ScatterLab crash): v2.5b shows it,
      v2.5a stops.  The page that answers with the CAS (cas='giac') is B2, for every test and tail.
  R4. the small-number displays: pv_FMT / pv_NumS / pv_NumD round first; with a typed mu1 of 100.001
      (d = 0.0000667) the power-vs-effect view reads "at d = 0.00" and the Esc summary "d = 0.000"
      (v2.5a: "6.67E-5", "6.667E-5"); a typed sigma of 0.0004 reads "0.000" in the SE line
      (v2.5a: "4.000E-4").
  R5. v2.5b against v2.5a: the routines that differ are exactly pv_Cas, pv_FMT, pv_NumD, pv_NumS, pv_Rep
      and pv_Strip; outside them only comments differ.
  R6. h.sci_strings from EVERY harness run of v2.5b in this script (and in B12's subprocess): empty.

(v2.5a's docstring follows.)

verify_PowerViz_v2.5a.py -- checks PowerViz v2.5a (17 Oct 2026): the CAS call form that
CASProbe beta 1b found on the emulator.  Built from verify_PowerViz_v2.5.py: every check is kept;
Part A still checks the mathematics of every template in desktop Giac, and A6 (new) reads the
templates as pv_Cas receives them on the calculator (prime_eval of string(...): braces, the root
sign); Part B runs in harness v3b, which models the calculator's CAS.  New or changed checks are
marked "2.5a".

Part A (desktop Giac 1.9 against SymPy, SciPy and statsmodels):
  A1 the four symbolic templates (built exactly as pv_Eq builds them) -> Giac -> SymPy:
     the CAS's n equals ((za*u + zb*w)/delta)^2 with the program's u, w for each test.
  A2 the numeric templates (the student's sigma, means, proportions as whole-number ratios,
     z kept as symbols) over a grid -> Giac -> evaluated at the program's z values for every
     alpha on the ladder and both tails -> equal to the PPL closed form (pv_NCF replica)
     and to statsmodels (normal_sample_size_one_tail, NormalIndPower.solve_power,
     samplesize_proportions_2indep_onetail).
  A3 ceiling(closed form) against the brute-force n80 of the program's own power model
     (SciPy): equal for every 1-sided case; for 2-sided n80 is never larger and is one
     smaller only in a few cases (the far tail); ceil(statsmodels two-sided) = n80.
  A4 no CAS text holds a decimal point; the ratio writer is exact.
  A5 why there is no factor(): Giac 1.9's factor on the symbolic one-proportion form
     gives a wrong expression (shown numerically).
Part B (the program, harness ppl_run_v3, cas='giac' / 'fail' / canned):
  the panel's "n80 = 56 (55.6)" for all tests and tails, the formula page line by line,
  the CAS asked only when the page opens and only for changed inputs (alpha and n never
  need it: z stays symbolic), no CAS call at all during drags, the fallback, the 2-sided
  difference, no effect, the menu item, the Pow-n label, help page 3, quoted and decimal
  answers, stale-key mode, the layout, and a regression run of v2.4's verification.

Part G (2.5a): v2.5 in harness v3b (its pv_Cas returns its own text: the page falls back), and
  v2.5a against v2.5 (only pv_Cas differs).

Run:  python3 verify_PowerViz_v2.5a.py     (exit code 0 = all passed)
"""
import math
import re
import os
import subprocess
import sys

import warnings

import sympy as sp
from scipy.stats import norm
from statsmodels.stats.power import NormalIndPower, normal_sample_size_one_tail
from statsmodels.stats.proportion import samplesize_proportions_2indep_onetail

sys.path.insert(0, '/home/claude/work/out')
import ppl_run_v3e   # noqa: E402
from ppl_run_v3e import Harness, ACCEPT, giac_eval, prime_eval   # noqa: E402

# 2.5b: every harness made in this script is remembered, so R6 can list h.sci_strings from all of them
ALLH = []
_h_init = ppl_run_v3e.Harness.__init__


def _h_track(self, *a, **k):
    _h_init(self, *a, **k)
    ALLH.append((a[0] if a else k.get('paths'), self))


ppl_run_v3e.Harness.__init__ = _h_track

warnings.filterwarnings('ignore')       # statsmodels' solver warnings when n is in the thousands
PROG = '/home/claude/new6/PowerViz_v2.5f.txt'
V25C = '/home/claude/work/out/PowerViz_v2.5c.txt'
V25A = '/home/claude/work/out/PowerViz_v2.5a.txt'
V25 = '/home/claude/work/out/PowerViz_v2.5.txt'
SCR = '/tmp/claude-0/-home-claude/6157958e-03ce-51f4-bf77-e038db8d37e9/scratchpad'
FAIL = []
NPASS = [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + detail) if detail else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


def hround(x, d=0):
    m = 10 ** d
    return math.copysign(math.floor(abs(x) * m + 0.5), x) / m


# ------------------------------------------------------------ replicas of the program
def istr(n):
    return str(int(hround(n)))


def rats(v):
    """pv_RatS: '(n/10^d)' or '(n)', '' beyond 6 decimals."""
    for d in range(7):
        s = v * 10 ** d
        if abs(s - hround(s)) < 1e-6:
            return '(' + istr(s) + ')' if d == 0 else '(' + istr(s) + '/' + istr(10 ** d) + ')'
    return ''


def eq(tt, L):
    """pv_Eq({sigma, delta, pa, pb, pm})."""
    if tt == 1:
        u = w = '' + L[0]
    if tt == 2:
        u = w = L[0] + '*sqrt(2)'
    if tt == 3:
        u = 'sqrt(' + L[2] + '*(1-' + L[2] + '))'
        w = 'sqrt(' + L[3] + '*(1-' + L[3] + '))'
    if tt == 4:
        u = 'sqrt(2*' + L[4] + '*(1-' + L[4] + '))'
        w = 'sqrt(' + L[2] + '*(1-' + L[2] + ')+' + L[3] + '*(1-' + L[3] + '))'
    return 'solve((' + L[1] + '-pvza*' + u + '/sqrt(pvn))/(' + w + '/sqrt(pvn))=pvzb,pvn)'


def numeric_template(tt, mm0, mm1, sg, pp0, pp1):
    """the template pv_Formula builds with the student's numbers ('' when it skips)."""
    if tt <= 2:
        if mm1 == mm0 or not (rats(sg) and rats(mm0) and rats(mm1)):
            return ''
        return eq(tt, [rats(sg), '(' + rats(max(mm0, mm1)) + '-' + rats(min(mm0, mm1)) + ')', '', '', ''])
    if pp1 == pp0 or not (rats(pp0) and rats(pp1)):
        return ''
    a, b = rats(pp0), rats(pp1)
    return eq(tt, ['', '(' + rats(max(pp0, pp1)) + '-' + rats(min(pp0, pp1)) + ')', a, b,
                   '((' + a + '+' + b + ')/2)'])


def uw(tt, sg, pp0, pp1):
    if tt == 1:
        return sg, sg
    if tt == 2:
        return sg * 2 ** .5, sg * 2 ** .5
    if tt == 3:
        return (pp0 * (1 - pp0)) ** .5, (pp1 * (1 - pp1)) ** .5
    pb = (pp0 + pp1) / 2
    return (2 * pb * (1 - pb)) ** .5, (pp0 * (1 - pp0) + pp1 * (1 - pp1)) ** .5


def ncf(tt, tl, al, mm0, mm1, sg, pp0, pp1):
    """pv_NCF."""
    za, zb = norm.ppf(1 - al / tl), norm.ppf(0.8)
    d = (mm1 - mm0) if tt <= 2 else (pp1 - pp0)
    if d == 0:
        return -1
    u, w = uw(tt, sg, pp0, pp1)
    return ((za * u + zb * w) / abs(d)) ** 2


def power(tt, tl, al, mm0, mm1, sg, pp0, pp1, n):
    """pv_Model's power (as v2.4's verification has it)."""
    if tt == 1:
        m0, m1, s0, s1 = mm0, mm1, sg / n ** .5, sg / n ** .5
    elif tt == 2:
        m0, m1, s0 = 0, mm1 - mm0, sg * (2 / n) ** .5
        s1 = s0
    elif tt == 3:
        m0, m1, s0, s1 = pp0, pp1, (pp0 * (1 - pp0) / n) ** .5, (pp1 * (1 - pp1) / n) ** .5
    else:
        pb = (pp0 + pp1) / 2
        m0, m1 = 0, pp1 - pp0
        s0, s1 = (2 * pb * (1 - pb) / n) ** .5, (pp0 * (1 - pp0) / n + pp1 * (1 - pp1) / n) ** .5
    z = norm.ppf(1 - al / tl)
    if tl == 2:
        return norm.cdf(m0 - z * s0, m1, s1) + norm.sf(m0 + z * s0, m1, s1)
    if m1 >= m0:
        return norm.sf(m0 + z * s0, m1, s1)
    return norm.cdf(m0 - z * s0, m1, s1)


def n80(*a):
    lo, hi = 2, 5000
    if power(*a, 5000) < 0.8:
        return -1
    if power(*a, 2) >= 0.8:
        return 2
    while hi - lo > 1:
        md = (lo + hi) // 2
        if power(*a, md) >= 0.8:
            hi = md
        else:
            lo = md
    return hi


za_, zb_, n_, s_, d_ = sp.symbols('pvza pvzb pvn pvs pvd', positive=True)
p_, r_, m_ = sp.symbols('pvp pvr pvm', positive=True)
LOC = {'pvza': za_, 'pvzb': zb_, 'pvn': n_, 'pvs': s_, 'pvd': d_, 'pvp': p_, 'pvr': r_, 'pvm': m_}


def strip(s):
    t = ''.join(c for c in s if c not in '[]{} ')
    return t[4:] if t.startswith('list') else t


def casuse(s):
    return (bool(s) and 'pvza' in s and 'pvzb' in s and 'pvn' not in s and ',' not in s and '.' not in s)


# ====================================================================== PART A
print('== A. the CAS templates through desktop Giac 1.9 ==')
SYMB = {1: (s_, s_), 2: (s_ * sp.sqrt(2), s_ * sp.sqrt(2)), 3: (sp.sqrt(p_ * (1 - p_)), sp.sqrt(r_ * (1 - r_))),
        4: (sp.sqrt(2 * m_ * (1 - m_)), sp.sqrt(p_ * (1 - p_) + r_ * (1 - r_)))}
SYMTXT = {}
for tt in (1, 2, 3, 4):
    txt = eq(tt, ['pvs', 'pvd', 'pvp', 'pvr', 'pvm'])
    got = strip(giac_eval(txt))
    SYMTXT[tt] = got
    u, w = SYMB[tt]
    want = ((za_ * u + zb_ * w) / d_) ** 2
    e = sp.sympify(got, locals=LOC)
    # compare numerically at random positive points (sqrt of p(1-p) needs p in (0, 1))
    import random
    random.seed(tt)
    ok = casuse(got)
    for _ in range(20):
        vals = {za_: random.uniform(0.5, 3.5), zb_: random.uniform(0.2, 2), s_: random.uniform(0.5, 30),
                d_: random.uniform(0.01, 10), p_: random.uniform(0.02, 0.98), r_: random.uniform(0.02, 0.98),
                m_: random.uniform(0.02, 0.98)}
        a, b = float(e.subs(vals)), float(want.subs(vals))
        ok &= abs(a - b) <= 1e-9 * abs(b)
    check('A1 test %d symbolic: Giac solves (delta - za SE0)/SE1 = zb for n -> %s = ((za u + zb w)/delta)^2'
          % (tt, got), ok)

# A2: numeric templates over a grid, at every alpha and both tails
grid = []
for (mm0, mm1, sg) in ((100, 105, 15), (100, 101, 15), (100, 98, 15), (0, 0.5, 1), (100, 100.5, 2.5),
                       (-5, 5, 7), (50, 62, 0.75), (100, 130, 15)):
    grid += [(1, mm0, mm1, sg, 0.5, 0.6), (2, mm0, mm1, sg, 0.5, 0.6)]
for (pp0, pp1) in ((0.5, 0.6), (0.5, 0.55), (0.3, 0.5), (0.2, 0.1), (0.02, 0.98), (0.123, 0.2), (0.6, 0.5),
                   (0.1, 0.3)):
    grid += [(3, 100, 105, 15, pp0, pp1), (4, 100, 105, 15, pp0, pp1)]
LADDER = (0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.20)
bad, n_cmp, decs, sm_bad, n_sm, n_nan = [], 0, [], [], 0, 0
NUMTXT = {}
for (tt, mm0, mm1, sg, pp0, pp1) in grid:
    txt = numeric_template(tt, mm0, mm1, sg, pp0, pp1)
    if '.' in txt:
        decs.append(txt)
    got = strip(giac_eval(txt))
    NUMTXT[(tt, mm0, mm1, sg, pp0, pp1)] = got
    if not casuse(got):
        bad.append(('unusable', tt, mm0, mm1, sg, pp0, pp1, got))
        continue
    e = sp.sympify(got, locals=LOC)
    f = sp.lambdify((za_, zb_), e, 'math')
    for tl in (1, 2):
        for al in LADDER:
            za, zb = norm.ppf(1 - al / tl), norm.ppf(0.8)
            a = f(za, zb)
            b = ncf(tt, tl, al, mm0, mm1, sg, pp0, pp1)
            n_cmp += 1
            if not (abs(a - b) <= 1e-9 * b):           # written so that a NaN fails
                bad.append((tt, tl, al, mm0, mm1, sg, pp0, pp1, a, b))
            # statsmodels, the same closed form (one tail)
            d = (mm1 - mm0) if tt <= 2 else (pp1 - pp0)
            u, w = uw(tt, sg, pp0, pp1)
            if tt in (1, 3):
                ref = normal_sample_size_one_tail(abs(d), 0.8, al / tl, std_null=u, std_alternative=w)
            elif tt == 2:
                ref = NormalIndPower().solve_power(effect_size=abs(d) / sg, alpha=al / tl, power=0.8, ratio=1,
                                                   alternative='larger')
                if math.isnan(ref):
                    # statsmodels' root finder does not converge for n in the thousands: use its
                    # closed-form helper (the same algebra) and count the case
                    n_nan += 1
                    ref = normal_sample_size_one_tail(abs(d), 0.8, al / tl, std_null=u, std_alternative=w)
            else:
                ref = samplesize_proportions_2indep_onetail(pp1 - pp0, pp0, 0.8, alpha=al,
                                                            alternative='two-sided' if tl == 2 else
                                                            ('larger' if pp1 > pp0 else 'smaller'))
            n_sm += 1
            if not (abs(ref - b) <= 1e-6 * b):
                sm_bad.append((tt, tl, al, d, ref, b))
check('A2 %d numeric templates x 7 alphas x 2 tails (%d values): Giac, evaluated at the plot\'s z, = PPL closed form'
      % (len(grid), n_cmp), not bad, str(bad[:2]))
check('A2 the PPL closed form = statsmodels (normal_sample_size_one_tail, NormalIndPower, '
      'samplesize_proportions_2indep_onetail), %d cases (NormalIndPower did not converge in %d, n > 1000: '
      'normal_sample_size_one_tail there)' % (n_sm, n_nan), not sm_bad, str(sm_bad[:2]))
check('A2 no CAS text holds a decimal point (BRIEF_CAS rule 1)', not decs, str(decs[:1]))
for key, want in (((1, 100, 105, 15, 0.5, 0.6), '(3*pvza+3*pvzb)^2'), ((3, 100, 105, 15, 0.5, 0.6),
                  '(5*pvza+2*sqrt(6)*pvzb)^2'), ((4, 100, 105, 15, 0.5, 0.6), '(3*sqrt(22)/2*pvza+7*pvzb)^2'),
                  ((2, 100, 105, 15, 0.5, 0.6), '(3*sqrt(2)*pvza+3*sqrt(2)*pvzb)^2')):
    check('A2 defaults, test %d: the CAS with the numbers gives %s' % (key[0], want), NUMTXT[key] == want, NUMTXT[key])

# A3: the ceiling against brute force
stat = {}
diffs = []
for (tt, mm0, mm1, sg, pp0, pp1) in grid:
    for tl in (1, 2):
        for al in LADDER:
            a = (tt, tl, al, mm0, mm1, sg, pp0, pp1)
            nb = n80(*a)
            c = ncf(*a)
            if nb < 0 or c < 0:
                continue
            cc = max(2, math.ceil(c))
            stat[(tl, cc - nb)] = stat.get((tl, cc - nb), 0) + 1
            if cc != nb:
                diffs.append((a, round(c, 3), cc, nb))
one = {k: v for k, v in stat.items() if k[0] == 1}
two = {k: v for k, v in stat.items() if k[0] == 2}
check('A3 1-sided: ceiling(formula) = brute-force n80 in every case (%d)' % sum(one.values()),
      set(one) == {(1, 0)}, str(one))
check('A3 2-sided: n80 is never larger than the ceiling, and smaller only by 1 or 2 (%s)' %
      ', '.join('%d off by %d' % (v, k[1]) for k, v in sorted(two.items())),
      all(k[1] in (0, 1, 2) for k in two))
print('   the differing cases: ' + '; '.join('test %d %d-sided a %.3g: n* %.3f -> %d, n80 %d' %
                                            (d[0][0], d[0][1], d[0][2], d[1], d[2], d[3]) for d in diffs))
# statsmodels' two-sided solve (both tails) agrees with the brute force
bad, n_ok, n_nc = [], 0, 0
for (tt, mm0, mm1, sg, pp0, pp1) in grid:
    if tt > 2 or mm1 == mm0:
        continue
    for al in LADDER:
        ref = NormalIndPower().solve_power(effect_size=abs(mm1 - mm0) / sg, alpha=al, power=0.8,
                                           ratio=0 if tt == 1 else 1, alternative='two-sided')
        nb = n80(tt, 2, al, mm0, mm1, sg, pp0, pp1)
        if math.isnan(ref):
            n_nc += 1
            continue
        n_ok += 1
        if nb > 0 and max(2, math.ceil(ref - 1e-9)) != nb:
            bad.append((tt, al, mm0, mm1, sg, ref, nb))
check('A3 2-sided means tests: ceil(statsmodels NormalIndPower two-sided, both tails) = brute-force n80 '
      '(%d cases; %d where its solver did not converge, n in the thousands)' % (n_ok, n_nc),
      not bad and n_ok > 30, str(bad[:2]))

# A4: the ratio writer
bad = [(v, rats(v)) for v in (15, 2.5, -5, 0.55, 0.123, 100.5, 0.000001)
       if not rats(v) or abs(float(sp.sympify(rats(v))) - v) > 1e-12]
check('A4 pv_RatS writes 15 (15), 2.5 (25/10), -5 (-5), 0.55 (55/100) ... exactly', not bad, str(bad))
check('A4 pv_RatS gives up beyond 6 decimals (the page then skips the CAS line)', rats(0.1234567) == '')

# A5: why no factor()
fx = strip(giac_eval('factor(' + eq(3, ['pvs', 'pvd', 'pvp', 'pvr', 'pvm']) + ')'))
e = sp.sympify(fx, locals=LOC)
vals = {za_: 1.645, zb_: 0.8416, d_: 0.1, p_: 0.5, r_: 0.6}
truth = float((((za_ * sp.sqrt(p_ * (1 - p_)) + zb_ * sp.sqrt(r_ * (1 - r_))) / d_) ** 2).subs(vals))
check('A5 Giac 1.9 factor() of the symbolic one-proportion form is WRONG (%.2f, not %.2f): the program '
      'does not use factor' % (float(e.subs(vals)), truth), abs(float(e.subs(vals)) - truth) > 1)

# A6 (2.5a): the same templates as pv_Cas receives them on the calculator: string(...) of the
# answer in the Prime's printing (braces for solve, the root sign), its quotes dropped
def cas_text(txt):
    a = prime_eval('string(' + txt + ')')
    return a[1:-1] if len(a) >= 2 and a[0] == a[-1] == '"' else a


def unroot(t):
    """The root sign back to sqrt(), for SymPy: sign + atom, or sign + (...)."""
    return re.sub('\u221a([A-Za-z_]\\w*|\\d+)', r'sqrt(\1)', t).replace('\u221a(', 'sqrt(')


import re  # noqa: E402
bad6 = []
for tt in (1, 2, 3, 4):
    txt = eq(tt, ['pvs', 'pvd', 'pvp', 'pvr', 'pvm'])
    pt = cas_text(txt)
    got = strip(pt)
    ok = pt.startswith('{') and pt.endswith('}') and casuse(got) and 'sqrt' not in pt and 'list' not in pt
    ok &= (tt == 1) or ('\u221a' in pt)
    e1 = sp.sympify(unroot(got), locals=LOC)
    e0 = sp.sympify(SYMTXT[tt], locals=LOC)
    vals = {za_: 1.645, zb_: 0.8416, s_: 15, d_: 5, p_: 0.5, r_: 0.6, m_: 0.55}
    ok &= abs(float(e1.subs(vals)) - float(e0.subs(vals))) <= 1e-9 * abs(float(e0.subs(vals)))
    if not ok:
        bad6.append((tt, pt))
    print('   2.5a test %d, as the Prime prints it: %s' % (tt, pt))
for key in NUMTXT:
    pt = cas_text(numeric_template(*key))
    if not (casuse(strip(pt)) and 'sqrt' not in pt):
        bad6.append((key, pt))
check('A6 2.5a: every template (4 symbolic, %d numeric), read as on the calculator, arrives in braces with the '
      'root sign, passes pv_CasUse, and has the value of desktop Giac\'s answer' % len(NUMTXT), not bad6, str(bad6[:2]))

# ====================================================================== PART B
print('\n== B. the program in the harness (ppl_run_v3e; 2.5b) ==')


def run(script, cas='giac', stale=False, prog=PROG):
    h = Harness(prog, strict=True, cas=cas, stale_keys=stale)
    script(h)
    h.call('POWERVIZ')
    return h


def pages(h, func):
    return [s for s in h.pages if s.func == func]


def ncfs(c):
    """pv_NCFS."""
    d = 1
    while d < 4 and hround(c, d) == math.ceil(c) and c < math.ceil(c) - 1e-7:
        d += 1
    return '%.*f' % (d, c)


DEF = {1: (100, 105, 15, 0.5, 0.6, 30), 2: (100, 105, 15, 0.5, 0.6, 30), 3: (100, 105, 15, 0.5, 0.6, 100),
       4: (100, 105, 15, 0.5, 0.6, 100)}
# B1 / B2: every test and both tails
for tt in (1, 2, 3, 4):
    for tl in (1, 2):
        h = run(lambda h: (h.choose(tt).answer(ACCEPT), h.tap(80, 230) if tl == 2 else None,
                           h.tap(260, 210, lift=True), h.press('Enter'), h.press('Esc')))
        mm0, mm1, sg, pp0, pp1, nn = DEF[tt]
        c = ncf(tt, tl, 0.05, mm0, mm1, sg, pp0, pp1)
        nb = n80(tt, tl, 0.05, mm0, mm1, sg, pp0, pp1)
        main = pages(h, 'pv_Draw')[-1]
        want = 'n₈₀ = %d (%s)' % (nb, ncfs(c))
        row = [t for t in main.texts if t.y == 206]
        check('B1 test %d, %d-sided: panel "%s", inside the panel, clear of the SE line' % (tt, tl, want),
              row[-1].text == want and row[-1].x + row[-1].est_width <= 317
              and row[0].x + row[0].est_width + 6 <= row[-1].x, str([(t.text, t.x) for t in row]))
        fp = pages(h, 'pv_Formula')
        L = fp[0].lines() if fp else []
        za = norm.ppf(1 - 0.05 / tl)
        ok = (('  n = %.2f' % c) in ' '.join(L) or ('    = %.2f' % c) in L or any(l.endswith('= %.2f' % c) for l in L))
        ok &= any(l.startswith('Round UP (whole people): n = %d;  trying n: n₈₀ = %d' % (max(2, math.ceil(c)), nb))
                  for l in L)
        ok &= any('z(%s) = %.3f' % (('0.95' if tl == 1 else '0.975'), za) in l for l in L)
        ok &= fp[0].has('exact (CAS)') and fp[0].has('CAS, solved for n:')
        ok &= (fp[0].has('1-sided: the formula is exact, so the two agree.') if tl == 1 else
               fp[0].has('2-sided: the formula drops the far tail; its'))
        over = [t for t in fp[0].texts if t.x + t.est_width > 318 or (t.y > 212 and t.y != 226)]
        check('B2 test %d, %d-sided formula page: CAS solve, CAS numbers, PPL n = %.2f, round up = %d = n80, '
              'the right explanation, layout' % (tt, tl, c, max(2, math.ceil(c))), ok and not over,
              str([(t.text, t.x, t.y) for t in over]) if over else '')
        if tt == 3 and tl == 1:
            check('B2 2.5a test 3: the CAS lines carry the Prime\'s root sign, shown as it is, and no "sqrt"',
                  fp[0].has('  n = (5×zα+2×√6×zβ)^2') and not any('sqrt' in l for l in L), str(L[3:9]))
        if tt == 1 and tl == 1:
            check('B2 2.5a: every CAS text asks for string(...), every answer arrives quoted; no CAS variable '
                  'assigned, no CAS call of a variable',
                  all(c[0].startswith('string(') and c[1].startswith('"') for c in h.cas_calls)
                  and not h.cas_vars and not any('non-literal' in w for w in h.warnings), str(h.cas_calls[:1]))
            for want_l in ('  (μ₁−μ₀ − zα×SE₀)/SE₁ = zβ,  SE₀ = SE₁ = σ/√n', '  n = ((σ×zα+σ×zβ)/(μ₁−μ₀))^2',
                           'CAS, with σ = 15, |μ₁−μ₀| = 5 (z kept exact):', '  n = (3×zα+3×zβ)^2',
                           '  n = ((15×1.645 + 15×0.842)/5)^2 = 55.64'):
                check('B2 test 1 page shows "%s"' % want_l.strip(), want_l in L)

# B3: the CAS only on page open, only for changed inputs
seq = lambda h: (h.choose(1).answer(ACCEPT),
                 h.tap(260, 210, lift=True), h.press('Enter'),       # open: 2 calls
                 h.tap(260, 210, lift=True), h.press('Enter'),       # reopen: 0
                 h.press('Up'), h.tap(260, 210, lift=True), h.press('Enter'),      # n changed: 0
                 h.tap(180, 230), h.tap(260, 210, lift=True), h.press('Enter'),    # alpha+: 0 (z symbolic)
                 h.press('Right'), h.tap(260, 210, lift=True), h.press('Enter'),   # mu1 changed: 1
                 h.press('Esc'))
h = run(seq)
counts = []
k = 0
for s in h.timeline if hasattr(h, 'timeline') else []:
    pass
fp = pages(h, 'pv_Formula')
check('B3 five openings of the page: CAS calls 2 + 0 + 0 + 0 + 1 = 3 (symbolic once; numbers again only when '
      'mu1 changed; n and alpha never, because z stays a symbol)', len(h.cas_calls) == 3 and len(fp) == 5,
      '%d calls: %s' % (len(h.cas_calls), [c[0][:40] for c in h.cas_calls]))
check('B3 after Right (mu1 106) the CAS line reads n = (15/6×zα+15/6×zβ)^2 in some exact form',
      fp[-1].has('CAS, with σ = 15, |μ₁−μ₀| = 6 (z kept exact):'), str(fp[-1].lines()[5:8]))
check('B3 after alpha+ (0.10) the PPL line uses z(0.9) = 1.282', any('z(0.9) = 1.282' in l for l in fp[3].lines()))

# B4: drags never call the CAS (and nor does the main view)
probe = run(lambda h: (h.choose(1).answer(ACCEPT), h.press('Esc')))
g0 = probe.globals_
px = lambda v: 12 + (v - g0['XMN']) / (g0['XMX'] - g0['XMN']) * (308 - 12)
h1x = px(105)
h = run(lambda h: (h.choose(1).answer(ACCEPT), h.drag([(h1x, 90), (h1x + 10, 91), (h1x + 30, 92), (h1x + 50, 93)]),
                   h.drag([(60, 120), (60, 105), (60, 80), (60, 60)]), h.press('Right'), h.press('Up'),
                   h.tap(180, 230), h.press('Esc')))
check('B4 an H1 drag, an n drag, arrows and soft keys: no CAS call at all', len(h.cas_calls) == 0,
      str(len(h.cas_calls)))
fr = pages(h, 'pv_Draw')
g = h.globals_
c = ncf(1, 1, g['AL'], 100, g['MM1'], 15, 0.5, 0.6)
check('B4 the panel\'s formula n follows the drag (PPL): final "(%s)"' % ncfs(c),
      [t for t in fr[-1].texts if t.y == 206][-1].text.endswith('(%s)' % ncfs(c)))

# B5: the fallback
h = run(lambda h: (h.choose(3).answer(ACCEPT), h.tap(260, 210, lift=True), h.press('Enter'), h.press('Esc')),
        cas='fail')
fp = pages(h, 'pv_Formula')[0]
c = ncf(3, 1, 0.05, 100, 105, 15, 0.5, 0.6)
check('B5 cas=fail: no error; the page says "decimal", gives the textbook form, keeps the PPL numbers',
      h.error is None and fp.has('decimal') and fp.has('(no CAS: the formula as textbooks print it)')
      and fp.has('  n = ((zα√(p₀(1−p₀)) + zβ√(p₁(1−p₁)))/(p₁−p₀))^2')
      and fp.has('(no CAS line with p₀ = 0.5, p₁ = 0.6)') and any('= %.2f' % c in l for l in fp.lines()),
      str(fp.lines()[:9]))
check('B5 cas=fail: the panel is the same as with the CAS ("n₈₀ = 153 (152.5)")',
      [t for t in pages(h, 'pv_Draw')[-1].texts if t.y == 206][-1].text == 'n₈₀ = 153 (152.5)')

# B6: the 2-sided far tail makes n80 one smaller (test 1, alpha 0.20, mu1 = 101)
h = run(lambda h: (h.choose(1).answer({'MM1': 101, 'AL': 0.2}), h.tap(80, 230), h.tap(260, 210, lift=True),
                   h.press('Enter'), h.press('Esc')))
fp = pages(h, 'pv_Formula')[0]
c = ncf(1, 2, 0.2, 100, 101, 15, 0.5, 0.6)
check('B6 2-sided, alpha 0.20, mu1 101: n* = %.2f -> 1015, n80 = 1014; the page says n80 stops 1 sooner' % c,
      fp.has('tiny extra power lets n₈₀ stop 1 sooner.') and
      any(l.startswith('Round UP (whole people): n = 1015;  trying n: n₈₀ = 1014') for l in fp.lines()),
      str(fp.lines()[-3:]))
check('B6 panel "n₈₀ = 1014 (1014.27)"',
      [t for t in pages(h, 'pv_Draw')[-1].texts if t.y == 206][-1].text == 'n₈₀ = 1014 (%s)' % ncfs(c))

# B7: no effect
h = run(lambda h: (h.choose(1).answer({'MM1': 100}), h.tap(260, 210, lift=True), h.press('Enter'), h.press('Esc')))
fp = pages(h, 'pv_Formula')
check('B7 no effect (mu1 = mu0): the panel has no bracket, the page says no n is enough, one CAS call',
      [t for t in pages(h, 'pv_Draw')[-1].texts if t.y == 206][-1].text == 'n₈₀: no effect'
      and fp and fp[0].has('No effect (σ = 15, |μ₁−μ₀| = 0): no n is enough.') and len(h.cas_calls) == 1
      and h.error is None, str(fp[0].lines() if fp else None))

# B8: the menu item, the menu, help page 3
h = run(lambda h: (h.choose(2).answer(ACCEPT), h.tap(300, 230), h.choose('Sample-size formula'), h.press('Enter'),
                   h.press('Esc')))
ch = [c for c in h.chooses if c.title == 'PowerViz Menu']
check('B8 Menu has 9 items and "Sample-size formula" opens the page',
      ch and len(ch[0].items) == 9 and len(pages(h, 'pv_Formula')) == 1, str(ch[0].items if ch else None))
h = run(lambda h: (h.choose(1).answer(ACCEPT), h.tap(300, 230), h.choose('Help'), h.press('Enter'),
                   h.press('Enter'), h.press('Enter'), h.press('Esc')))
hp = pages(h, 'pv_ShowHelp')
check('B8 help: three pages, page 3 is the n formula, all text inside x 318',
      len(hp) == 3 and hp[2].has('PowerViz  help  3/3: the n formula')
      and all(t.x + t.est_width <= 318 for s in hp for t in s.texts))

# B9: the power-vs-n view's label
h = run(lambda h: (h.choose(1).answer(ACCEPT), h.tap(240, 230), h.press('Enter'), h.press('Esc')))   # slot 5 = Pow-n
pc = pages(h, 'pv_PCDraw')[0]
check('B9 Pow-n view: "formula: 55.6 → 56" in magenta under the green n80 label',
      any(t.text == 'formula: 55.6 → 56' and t.hex == '#C800C8' for t in pc.texts))

# B10 (2.5a): canned answers as the calculator gives them -- string(...) answers, PPL strings whose
# quotes STRING() adds and pv_Cas drops, the solve in braces (CASProbe beta 1b T18) -- and an
# approximate (decimal) answer
sym1 = 'string(' + eq(1, ['pvs', 'pvd', 'pvp', 'pvr', 'pvm']) + ')'
num1 = 'string(' + numeric_template(1, 100, 105, 15, 0.5, 0.6) + ')'
h = run(lambda h: (h.choose(1).answer(ACCEPT), h.tap(260, 210, lift=True), h.press('Enter'), h.press('Esc')),
        cas={sym1: '"{((pvs*pvza+pvs*pvzb)/pvd)^2}"', num1: '"{(3*pvza+3*pvzb)^2}"'})
fp = pages(h, 'pv_Formula')[0]
check('B10 answers wrapped in quotes: stripped by the kit, the page is exact',
      fp.has('exact (CAS)') and fp.has('  n = (3×zα+3×zβ)^2'))
h = run(lambda h: (h.choose(1).answer(ACCEPT), h.tap(260, 210, lift=True), h.press('Enter'), h.press('Esc')),
        cas={sym1: '"{((pvs*pvza+pvs*pvzb)/pvd)^2}"', num1: '"{9.0*pvza^2+18.0*pvza*pvzb+9.0*pvzb^2}"'})
fp = pages(h, 'pv_Formula')[0]
check('B10 an approximate-mode answer (decimals) is refused: badge "decimal", no CAS number line',
      fp.has('decimal') and fp.has('(no CAS line with σ = 15, |μ₁−μ₀| = 5)'))

# B11: stale-key mode through menu -> formula page
h = run(lambda h: (h.choose(4).answer(ACCEPT), h.press('Enter'), h.choose('Sample-size formula'), h.press('Enter'),
                   h.press('Esc')), stale=True)
check('B11 stale-key mode: the menu\'s Enter does not skip the formula page', not h.stale_skips
      and len(pages(h, 'pv_Formula')) == 1, str(h.stale_skips))

# ---- B12. v2.4's verification run against v2.5 (regression) ----
print('\n== B12. v2.4\'s verify_PowerViz.py run against v2.5b (harness v3d) ==')
old = open('/home/claude/work/out/verify_PowerViz.py', encoding='utf-8').read()
_IMP24 = "sys.path.insert(0, '/home/claude/work/harness')\nfrom ppl_run_v1 import Harness, ACCEPT"
assert old.count(_IMP24) == 1
old = old.replace(_IMP24, "sys.path.insert(0, '/home/claude/work/out')\nimport ppl_run_v3e as _v3d\n"
                          "from ppl_run_v3e import Harness, ACCEPT\n_ALLH = []\n_hi = _v3d.Harness.__init__\n"
                          "def _ht(self, *a, **k):\n    _hi(self, *a, **k); _ALLH.append(self)\n"
                          "_v3d.Harness.__init__ = _ht")
_END24 = "print('\\n%d failure(s)' % len(FAIL))"
assert old.count(_END24) == 1
old = old.replace(_END24, "print('SCI-LIST %r' % sorted({(round(v, 12), d, r) for hh in _ALLH for v, d, r in hh.sci_strings}))\n"
                  + _END24)
# the one script change v2.5 needs ON PURPOSE: help now has THREE pages (the n formula),
# so the help check needs one more key to get past page 3
HELP24 = "hh.choose(1).answer(ACCEPT).tap(300, 230).choose('Help').press('Enter').press('Enter').press('Esc')"
assert old.count(HELP24) == 1
old = old.replace(HELP24, "hh.choose(1).answer(ACCEPT).tap(300, 230).choose('Help').press('Enter').press('Enter')"
                          ".press('Enter').press('Esc')")
reg = os.path.join(SCR, 'verify_PowerViz_on_v25b.py')
open(reg, 'w', encoding='utf-8').write(old)
res = subprocess.run([sys.executable, reg], capture_output=True, text=True, env=dict(os.environ, POWERVIZ=PROG))
lines = res.stdout.split('\n')
fails = [ln for ln in lines if ln.startswith('FAIL')]
npass = sum(1 for ln in lines if ln.startswith('PASS'))
print('   %d PASS, %d FAIL%s' % (npass, len(fails), ('   (stderr: ' + res.stderr.strip().split('\n')[-1] + ')')
                                if res.returncode and not fails else ''))
for ln in fails:
    print('   ' + ln)
B12SCI = [ln for ln in lines if ln.startswith('SCI-LIST ')]
print('   ' + (B12SCI[0] if B12SCI else 'SCI-LIST not printed'))
# v2.4's script ends with "0 failure(s)" or the like; it must run to the end, not stall
# The v2.4 check v2.5 changes ON PURPOSE: 'soft key Menu -> Help: two drawn pages' (now three;
# B8 checks the three).  Every other v2.4 check must pass, and the script must reach its end.
INTENDED = ('FAIL soft key Menu -> Help: two drawn pages',)
unexpected = [f for f in fails if not f.startswith(INTENDED)]
complete = 'Traceback' not in res.stderr and 'failure(s)' in res.stdout
check('B12 v2.4\'s verification runs to the end on v2.5: %d PASS, the only FAIL is the intended help-page count'
      % npass, complete and not unexpected and npass >= 60, str(unexpected))

# ---- G (2.5a). v2.5 in v3b: the emulator's finding; and v2.5a against v2.5 ----
print('\n== G. 2.5a: v2.5 in harness v3b, and v2.5a against v2.5 ==')
h5 = run(lambda h: (h.choose(1).answer(ACCEPT), h.tap(260, 210, lift=True), h.press('Enter'), h.press('Esc')),
         prog=V25)
f5 = pages(h5, 'pv_Formula')[0]
check('G v2.5 in v3b: its pv_Cas hands back its own text, so the page shows the textbook form and "decimal"',
      f5.has('decimal') and not f5.has('exact (CAS)') and any('non-literal' in w for w in h5.warnings))
say = print
SRC = PROG
FAILS = FAIL
_saved_check = check


def _check2(cond, msg):
    _saved_check(msg, cond)


check = _check2

# ================================================================ G (round 2a)
say('\nG. v2.5a: v2.5 in harness v3b, and v2.5a against v2.5')
import re as _re
_b_old = open(V25, encoding='utf-8').read()
_b_new = open(V25A, encoding='utf-8').read()


def _bodies(txt):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)
    c = _re.sub(r'//[^\n]*', '', c)
    out = {}
    for m in _re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, _re.S):
        out[m.group(1)] = _re.sub(r'[ \t]+\n', '\n', m.group(0))
    return out


_B0, _B1 = _bodies(_b_old), _bodies(_b_new)
_diff = sorted(n for n in set(_B0) | set(_B1) if _B0.get(n) != _B1.get(n))
check(_diff == ['pv_Cas'], 'v2.5a: routines that differ from v2.5: %s (want pv_Cas)' % _diff)


def _outside(t, names):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\n]*', '', t))
    if names:
        c = _re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
    return _re.sub(r'\s+', ' ', c)


check(_outside(_b_old, _diff) == _outside(_b_new, _diff), 'v2.5a: outside those routines only comments differ')
_py0 = _re.findall(r'(?s)#PYTHON.*?#END', _b_old)
_py1 = _re.findall(r'(?s)#PYTHON.*?#END', _b_new)
check(_py0 == _py1, 'v2.5a: the #PYTHON blocks are unchanged')
say('  routines that differ from v2.5: %s; everything else differs only in comments' % ', '.join(_diff))

check = _saved_check

# ================================================================ R (2.5b)
print('\n== R. 2.5b: the round-2 string fixes (harness v3d) ==')
INV = 'INSTRING: Invalid input'


def stops(fn):
    """Run fn(); return the error text if the program stopped, else None."""
    try:
        fn()
        return None
    except Exception as e:      # the harness raises the PPL run-time error
        return str(e)


def lone(prog, cas='giac'):
    h = Harness(prog, cas=cas)
    h.call('pv_Init')
    return h


# R1. pv_Cas after a failed call
h = lone(PROG, 'fail')
r1 = stops(lambda: h.call('pv_Cas', '1/2+1/3'))
check('R1 2.5b: a failed CAS call -> pv_Cas returns "" with no error', r1 is None and h.call('pv_Cas', '1/2+1/3') == '')
h = lone(V25A, 'fail')
r1o = stops(lambda: h.call('pv_Cas', '1/2+1/3'))
check('R1 v2.5a in v3d: the same call stops the program', r1o is not None and INV in r1o, (r1o or '')[:60])
h = lone(PROG, {'string(q1)': '""', 'string(q2)': '"undef"', 'string(q3)': '"{7/2}"'})
check('R1 2.5b: an empty CAS string -> "", undef -> "", {7/2} kept',
      h.call('pv_Cas', 'q1') == '' and h.call('pv_Cas', 'q2') == '' and h.call('pv_Cas', 'q3') == '{7/2}')

# R2. cas='fail', the formula page, every test; v2.5a stops on each
TEXTBOOK = {1: '  n = ((zα+zβ)×σ/(μ₁−μ₀))^2', 2: '  n = 2×((zα+zβ)×σ/(μ₂−μ₁))^2',
            3: '  n = ((zα√(p₀(1−p₀)) + zβ√(p₁(1−p₁)))/(p₁−p₀))^2', 4: None}
CASES = [('test %d, 1-sided' % tt, (lambda tt: lambda h: (h.choose(tt).answer(ACCEPT), h.tap(260, 210, lift=True),
                                                         h.press('Enter'), h.press('Esc')))(tt), tt)
         for tt in (1, 2, 3, 4)]
CASES.append(('test 2, 2-sided', lambda h: (h.choose(2).answer(ACCEPT), h.tap(80, 230), h.tap(260, 210, lift=True),
                                            h.press('Enter'), h.press('Esc')), 2))
CASES.append(('test 4, menu route', lambda h: (h.choose(4).answer(ACCEPT), h.press('Enter'),
                                               h.choose('Sample-size formula'), h.press('Enter'), h.press('Esc')), 4))
CASES.append(('no effect', lambda h: (h.choose(1).answer({'MM1': 100}), h.tap(260, 210, lift=True), h.press('Enter'),
                                      h.press('Esc')), 0))
for name, scr, tt in CASES:
    hn = Harness(PROG, strict=True, cas='fail'); scr(hn); en = stops(lambda: hn.call('POWERVIZ'))
    fp = pages(hn, 'pv_Formula')
    ok = en is None and len(fp) == 1 and fp[0].has('decimal') and not fp[0].has('exact (CAS)')
    if tt:
        ok = ok and fp[0].has('(no CAS: the formula as textbooks print it)')
        if TEXTBOOK.get(tt):
            ok = ok and fp[0].has(TEXTBOOK[tt])
    else:
        ok = ok and fp[0].has('No effect (σ = 15, |μ₁−μ₀| = 0): no n is enough.')
    check('R2 2.5b cas=fail, %s: the formula page opens with "decimal" and the textbook form, no error' % name,
          ok, '' if ok else str((en, fp[0].lines()[:6] if fp else None)))
    ho = Harness(V25A, strict=True, cas='fail'); scr(ho); eo = stops(lambda: ho.call('POWERVIZ'))
    check('R2 v2.5a in v3d, cas=fail, %s: stops' % name, eo is not None and INV in eo, (eo or 'no error')[:44])

# R3. pv_Rep and pv_Strip directly (v2.5b)
h = lone(PROG)
for s, a, b, want in (('pvza+pvzb', 'pvzb', 'zβ', 'pvza+zβ'), ('pvza+pvzb', 'pvza', 'zα', 'zα+pvzb'),
                      ('pvd', 'pvd', 'δ', 'δ'), ('3*pvs*pvs', 'pvs', 'σ', '3*σ*σ'), ('a*b', '', 'x', 'a*b'),
                      ('', 'pvd', 'δ', ''), ('', '', 'x', ''), ('abc', 'pvd', 'δ', 'abc'),
                      ('2*3*', '*', '×', '2×3×'), ('**', '*', '', '')):
    try:
        got = h.call('pv_Rep', s, a, b)
    except Exception as e:
        got = 'ERROR ' + str(e)[:40]
    check('R3 pv_Rep(%r, %r, %r) = %r' % (s, a, b, got), got == want)
for s, want in (('', ''), ('{}', ''), ('list[(3*pvza)^2]', '(3*pvza)^2'), ('{((pvs*pvza+pvs*pvzb)/pvd)^2}',
                                                                          '((pvs*pvza+pvs*pvzb)/pvd)^2'), ('list', '')):
    try:
        got = h.call('pv_Strip', s)
    except Exception as e:
        got = 'ERROR ' + str(e)[:40]
    check('R3 pv_Strip(%r) = %r' % (s, got), got == want)
ho = lone(V25A)
eo = stops(lambda: ho.call('pv_Rep', 'pvza+pvzb', 'pvzb', 'zβ'))
check('R3 v2.5a in v3d: pv_Rep with the pattern at the end stops', eo is not None and INV in eo, (eo or 'no error')[:44])
# the formula page with canned CAS answers whose text ENDS with a CAS name (pvzb, pvd): every
# pv_Rep in pv_Disp then leaves "" behind -- the emulator's TrendTest / ScatterLab crash
sym1 = 'string(' + eq(1, ['pvs', 'pvd', 'pvp', 'pvr', 'pvm']) + ')'
num1 = 'string(' + numeric_template(1, 100, 105, 15, 0.5, 0.6) + ')'
CAN = {sym1: '"{(pvza+pvzb)^2*pvs^2/pvd^2*pvzb/pvzb}"', num1: '"{9*(pvza+pvzb)^2*pvzb/pvzb}"'}
scr = lambda h: (h.choose(1).answer(ACCEPT), h.tap(260, 210, lift=True), h.press('Enter'), h.press('Esc'))
hn = Harness(PROG, strict=True, cas=CAN); scr(hn); en = stops(lambda: hn.call('POWERVIZ'))
fp = pages(hn, 'pv_Formula')
check('R3 2.5b: CAS answers ending in pvzb: the page opens "exact (CAS)" and shows them',
      en is None and fp and fp[0].has('exact (CAS)') and fp[0].has('  n = (zα+zβ)^2×σ^2/(μ₁−μ₀)^2×zβ/zβ')
      and fp[0].has('  n = 9×(zα+zβ)^2×zβ/zβ'), str(fp[0].lines()[3:8] if fp else en))
ho = Harness(V25A, strict=True, cas=CAN); scr(ho); eo = stops(lambda: ho.call('POWERVIZ'))
check('R3 v2.5a in v3d, the same canned answers: stops in pv_Rep', eo is not None and INV in eo, (eo or 'no error')[:44])

# R4. small numbers
h = lone(PROG)
vals = [(h.call('pv_FMT', x, float(d)), w) for x, d, w in ((0.0033, 2, '0.00'), (0.00667, 2, '0.01'), (0.05, 1, '0.1'),
                                                           (2.7755575615628914e-17, 1, '0.0'), (1.645, 3, '1.645'),
                                                           (55.64, 2, '55.64'))]
check('R4 pv_FMT rounds first: %s' % [v for v, _ in vals], all(v == w for v, w in vals))
check('R4 pv_NumS(0.0004) = "0.000", pv_NumS(2.5) = "2.5", pv_NumD(0.00004) = "0.0000", pv_NumD(0.0005) = "0.0005"',
      h.call('pv_NumS', 0.0004) == '0.000' and h.call('pv_NumS', 2.5) == '2.5'
      and h.call('pv_NumD', 0.00004) == '0.0000' and h.call('pv_NumD', 0.0005) == '0.0005')
ho = lone(V25A)
check('R4 v2.5a in v3d: pv_FMT(0.0033, 2) = %r, pv_NumS(0.0004) = %r (the finding)'
      % (ho.call('pv_FMT', 0.0033, 2.0), ho.call('pv_NumS', 0.0004)),
      'ᴇ' in ho.call('pv_FMT', 0.0033, 2.0) and 'ᴇ' in ho.call('pv_NumS', 0.0004))
# mu1 = 100.001 with sigma 15: d = 0.0000667.  The power-vs-effect view's "at d = ..." (2 decimals)
# and the Esc summary's "d = ..." (3 decimals).  sigma = 0.0004 typed: the SE line's "sigma/sqrt n"
# (pv_NumS, 3 decimals).  (The main readout's d was already rounded in v2.5a, pv_DLbl.)
for prog, tag in ((PROG, '2.5b'), (V25A, 'v2.5a')):
    hh = Harness(prog, strict=True, cas='giac')
    hh.choose(1).answer({'MM1': 100.001}); hh.tap(300, 230); hh.choose('Power vs effect size')
    hh.press('Enter'); hh.press('Esc')
    stops(lambda: hh.call('POWERVIZ'))
    ev = [t.text for s in hh.pages for t in s.texts if t.text.startswith('at d = ')]
    sm = [m.text for m in hh.msgboxes if 'Exported' in m.text]
    sml = [l for m in sm for l in m.split('\n') if l.startswith('effect = ')]
    hs = Harness(prog, strict=True, cas='giac')
    hs.choose(1).answer({'SG': 0.0004, 'MM1': 100.0001}); hs.press('Esc')
    stops(lambda: hs.call('POWERVIZ'))
    se = [t.text for s in pages(hs, 'pv_Draw') for t in s.texts if t.text.startswith('SE₀ = ')]
    if tag == '2.5b':
        check('R4 2.5b mu1 = 100.001 (d = 0.0000667): %r, summary %r; sigma 0.0004: %r; no scientific text'
              % (ev[:1], sml[:1], se[:1]), hh.error is None and hs.error is None
              and ev and ev[0].startswith('at d = 0.00: power = ') and sml and sml[0].endswith('d = 0.000')
              and se and se[-1].startswith('SE₀ = σ/√n = 0.000/√30 = ')
              and not hh.sci_strings and not hs.sci_strings
              and not any('ᴇ' in t.text for x in (hh, hs) for s in x.pages for t in s.texts)
              and not any('ᴇ' in m.text for x in (hh, hs) for m in x.msgboxes))
    else:
        check('R4 v2.5a in v3d, the same inputs: %r, %r, %r' % (ev[:1], sml[:1], se[:1]),
              ev and 'ᴇ' in ev[0] and sml and 'ᴇ' in sml[0] and se and 'ᴇ' in se[-1])

# R5. v2.5b against v2.5a
_n0 = open(V25A, encoding='utf-8').read()
_n1 = open(PROG, encoding='utf-8').read()
_C0, _C1 = _bodies(_n0), _bodies(_n1)
_d = sorted(n for n in set(_C0) | set(_C1) if _C0.get(n) != _C1.get(n))
check('R5 2.5b (and 2.5c: + POWERVIZ, pv_BetaS, pv_Draw, pv_PCDraw, pv_Rel, pv_Tails): routines that differ from '
      'v2.5a: %s' % _d,
      _d == ['POWERVIZ', 'pv_BetaS', 'pv_Cas', 'pv_Draw', 'pv_FMT', 'pv_FMTP', 'pv_Formula', 'pv_NCF', 'pv_NumD',
             'pv_NumS', 'pv_PCDraw', 'pv_Rel', 'pv_Rep', 'pv_ShowHelp', 'pv_Strip', 'pv_Tails'])
# (2.5d: + pv_FMTP, pv_Formula, pv_NCF, pv_ShowHelp)
check('R5 2.5b: outside those routines only comments differ', _outside(_n0, _d) == _outside(_n1, _d))
_head = lambda txt, nm: re.search(r'(?ms)^(?:LOCAL\s+|EXPORT\s+)?%s\([^\n]*\)\s*\nBEGIN\n.*?^END;' % nm, txt).group(0)
_names = re.findall(r'(?m)^(?:LOCAL\s+|EXPORT\s+)?([A-Za-z]\w*)\([^\n]*\)\s*$', _n0)
_names = [n for n in dict.fromkeys(_names) if re.search(r'(?ms)^(?:LOCAL\s+|EXPORT\s+)?%s\([^\n]*\)\s*\nBEGIN\n' % n, _n0)]
_same = [n for n in _names if n not in _d and _head(_n0, n) == _head(_n1, n)]
check('R5 2.5b: %d of the %d untouched routines are byte-identical, comments included' % (len(_same), len([n for n in _names if n not in _d])),
      len(_same) == len([n for n in _names if n not in _d]))   # 2.5c: two of _d are new routines, not in v2.5a
print('  INSTRING sites in v2.5b: ' + ', '.join(str(i + 1) for i, l in enumerate(_n1.splitlines())
                                            if 'INSTRING(' in l and not l.strip().startswith('//')))

# R6. scientific STRING results, every run
mine = [(p, hh) for p, hh in ALLH if p == PROG]
sci = sorted({(round(v, 12), d, r) for p, hh in mine for v, d, r in hh.sci_strings})
other = sorted({(round(v, 12), d, r) for p, hh in ALLH if p != PROG for v, d, r in hh.sci_strings})
print('  harness runs: %d of v2.5c here, plus B12\'s subprocess; %d of v2.5 / v2.5a / v2.5b' % (len(mine), len(ALLH) - len(mine)))
print('  h.sci_strings, v2.5b: %r' % sci)
print('  h.sci_strings, B12 (v2.4\'s script on v2.5b): %s' % (B12SCI[0][9:] if B12SCI else 'not reported'))
print('  h.sci_strings, v2.5 / v2.5a (for comparison): %r' % other[:8])
check('R6 2.5b: no scientific STRING(x, 2, d) result in any of the %d v2.5b runs, nor in B12' % len(mine),
      not sci and B12SCI and B12SCI[0] == 'SCI-LIST []')


# ================================================================ T (2.5c)
print('\n== T. 2.5c: no "=" before a relation; beta of its own (harness v3e) ==')
import difflib as _dl
import scipy.stats as stats
V25B = '/home/claude/work/out/PowerViz_v2.5b.txt'
T_KEYS = ('α =', 'α <', 'β =', 'β <', 'power', 'POWER', '2-sided', '1-sided')


def t_run(prog, ans, extra=lambda h: None, tt=1):
    h = Harness(prog, cas='fail')
    h.choose(tt); h.answer(ans); extra(h); h.press('Esc')
    h.call('POWERVIZ')
    pg = [s for s in h.pages if s.func == 'pv_Draw']
    tx = [t.text for t in pg[-1].texts if (t.text.startswith('α') or t.text.startswith('β')) and t.y >= 150] if pg else []
    hint = [t.text for s in h.pages for t in s.texts if t.text.startswith('2-sided: α') or t.text.startswith('1-sided: all')]
    return tx, [m.lines for m in h.msgboxes][-1:], hint[-1:]


cases = (
    ('typed alpha 0.0001, d 0.033', {'MM1': 100.5, 'AL': 0.0001}, lambda h: None,
     (['α = < 0.001', 'β = 1.000'], 'n = 30/group  α = < 0.001  1-sided', 'POWER = 0.0002   (β = 0.9998)'),
     (['α < 0.001', 'β > 0.999'], 'n = 30/group  α < 0.001  1-sided', 'POWER = 0.0002   (β = 0.9998)')),
    ('typed alpha 0.00001, no effect', {'MM1': 100, 'AL': 0.00001}, lambda h: None,
     (['α = < 0.001', 'β = 1.000'], 'n = 30/group  α = < 0.001  1-sided', 'POWER = < 0.0001   (β = 1.0000)'),
     (['α < 0.001', 'β > 0.999'], 'n = 30/group  α < 0.001  1-sided', 'POWER < 0.0001   (β > 0.9999)')),
    ('n 200, d 0.67', {'MM1': 110, 'NN': 200}, lambda h: None,
     (['α = 0.050', 'β = < 0.001'], 'n = 200/group  α = 0.050  1-sided', 'POWER = 1.0000   (β = < 0.0001)'),
     (['α = 0.050', 'β < 0.001'], 'n = 200/group  α = 0.050  1-sided', 'POWER > 0.9999   (β < 0.0001)')),
    ('n 5000, d 0.67', {'MM1': 110, 'NN': 5000}, lambda h: None,
     (['α = 0.050', 'β = 0.000'], 'n = 5000/group  α = 0.050  1-sided', 'POWER = 1.0000   (β = 0.0000)'),
     (['α = 0.050', 'β < 0.001'], 'n = 5000/group  α = 0.050  1-sided', 'POWER > 0.9999   (β < 0.0001)')),
    ('defaults', ACCEPT, lambda h: None,
     (['α = 0.050', 'β = 0.428'], 'n = 30/group  α = 0.050  1-sided', 'POWER = 0.5718   (β = 0.4282)'), None),
    ('2-sided, typed alpha 0.0001', {'MM1': 101, 'AL': 0.0001}, lambda h: h.tap(80, 230),
     (['α = < 0.001', 'β = 1.000'], 'n = 30/group  α = < 0.001  2-sided', 'POWER = 0.0002   (β = 0.9998)'),
     (['α < 0.001', 'β > 0.999'], 'n = 30/group  α < 0.001  2-sided', 'POWER = 0.0002   (β = 0.9998)')))
# (2.5d: the "new" column is v2.5d's -- a probability that rounds to 1 prints "> 0.999" / "> 0.9999")
for tag, ans, ex, old, new in cases:
    a, b = t_run(V25B, ans, ex), t_run(PROG, ans, ex)
    ao = (a[0], a[1][0][1], a[1][0][3])
    bo = (b[0], b[1][0][1], b[1][0][3])
    print('   T1 %s: v2.5b %r  ->  v2.5c %r' % (tag, ao, bo))
    check('T1 %s: v2.5b %r' % (tag, ao), ao == old)
    if new is None:
        check('T1 %s: an ordinary panel and exit box are the same in v2.5c: %r' % (tag, bo), bo == old)
    else:
        check('T1 %s: v2.5c %r' % (tag, bo), bo == new)
a, b = t_run(V25B, {'MM1': 101, 'AL': 0.0001}, lambda h: h.tap(80, 230)), t_run(PROG, {'MM1': 101, 'AL': 0.0001}, lambda h: h.tap(80, 230))
check('T1 the tails hint, typed alpha 0.0001: v2.5b %r -> v2.5c %r' % (a[2], b[2]),
      a[2] == ['2-sided: α = < 0.001 is split, < 0.0001 in each tail,'] and
      b[2] == ['2-sided: α < 0.001 is split, < 0.0001 in each tail,'])


# the two curve views (kind 1 from soft key 5, kind 2 from the menu): title and the power readout
def t_view(prog, ans, kind):
    h = Harness(prog, cas='fail')
    h.choose(1); h.answer(ans)
    if kind == 1:
        h.tap(240, 230); h.press('Enter')
    else:
        h.press('Enter'); h.choose(5); h.press('Enter')
    h.press('Esc')
    h.call('POWERVIZ')
    pg = [s for s in h.pages if s.func == 'pv_PCDraw']
    return [t.text for t in pg[-1].texts if ', α' in t.text or 'power' in t.text] if pg else []


for kind, ans, old, new in (
        (1, {'MM1': 100.5, 'AL': 0.0001},
         (', α = < 0.001, 1-sided', 'at n = 30: power = < 0.001, touch = pick n, key = back'),
         (', α < 0.001, 1-sided', 'at n = 30: power < 0.001, touch = pick n, key = back')),
        (2, {'MM1': 100.5, 'AL': 0.0001},
         ('n = 30/grp, α = < 0.001, 1-sided', 'power = < 0.001, key or tap = back'),
         ('n = 30/grp, α < 0.001, 1-sided', 'power < 0.001, key or tap = back')),
        (1, ACCEPT, None, None)):
    a, b = t_view(V25B, ans, kind), t_view(PROG, ans, kind)
    if old is None:
        check('T1 curve view %d, defaults: the same in v2.5b and v2.5c: %r' % (kind, b), a == b and b)
    else:
        check('T1 curve view %d, typed alpha 0.0001: v2.5b %r -> v2.5c %r' % (kind, a, b),
              len(a) == 2 and a[0].endswith(old[0]) and a[1].endswith(old[1])
              and len(b) == 2 and b[0].endswith(new[0]) and b[1].endswith(new[1]))

# T2. pv_BetaS against 1 - PW (ordinary states: the same text) and against SciPy (every state)
hb = Harness(PROG, cas='fail')
nsame = nst = 0
worst = 0.0
for tt in (1, 2, 3, 4):
    for tl in (1, 2):
        for al in (0.001, 0.01, 0.05, 0.2):
            for nn in (2, 10, 30, 100, 1000, 5000):
                for eff in (-1.0, -0.2, 0.0, 0.1, 0.5, 1.5):
                    hb.globals_['TT'] = float(tt); hb.globals_['TL'] = float(tl); hb.globals_['AL'] = al
                    hb.globals_['NN'] = float(nn); hb.globals_['MM0'] = 100.0; hb.globals_['SG'] = 15.0
                    hb.globals_['MM1'] = 100.0 + eff * 15; hb.globals_['PP0'] = 0.5
                    hb.globals_['PP1'] = min(0.98, max(0.02, 0.5 + eff * 0.3))
                    hb.call('pv_Model', float(nn))
                    g = hb.globals_
                    pw = g['PW']
                    lo, hi = g['XCL'], g['XCU']
                    b_sp = stats.norm.cdf(hi, g['M1v'], g['SE1']) - stats.norm.cdf(lo, g['M1v'], g['SE1'])
                    if (lo + hi) / 2 >= g['M1v']:
                        b_sp = stats.norm.sf(lo, g['M1v'], g['SE1']) - stats.norm.sf(hi, g['M1v'], g['SE1'])
                    for d in (3.0, 4.0):
                        nst += 1
                        s_new = hb.call('pv_BetaS', d)
                        s_old = hb.call('pv_FMTP', 1 - pw, d)
                        if 1 - pw >= 10 ** -d * 1.5 and abs((1 - pw) * 10 ** d - round((1 - pw) * 10 ** d) - 0.5) > 1e-6:
                            nsame += (s_new == s_old)
                        else:
                            nsame += 1 if (s_new.startswith('< ') and b_sp < 10 ** -d) or s_new == s_old else 0
                    if b_sp > 1e-290:
                        F = lambda x: ('%.17g' % x).replace('e', 'E')
                        m_, s_ = F(g['M1v']), F(g['SE1'])
                        if (lo + hi) / 2 >= g['M1v']:
                            v = hb.execute('NORMALD_CDF(%s,%s,%s)-NORMALD_CDF(%s,%s,%s)' % (m_, s_, F(2 * g['M1v'] - lo),
                                                                                         m_, s_, F(2 * g['M1v'] - hi)))
                        else:
                            v = hb.execute('NORMALD_CDF(%s,%s,%s)-NORMALD_CDF(%s,%s,%s)' % (m_, s_, F(hi), m_, s_, F(lo)))
                        worst = max(worst, abs(v - b_sp) / b_sp)
check('T2 pv_BetaS over %d states (4 tests, 2 tails, 4 alphas, n 2-5000, 6 effects; 3 and 4 decimals): the text '
      'v2.5b printed for 1 - PW wherever 1 - PW still had its digits, else the floor where SciPy\'s beta is below it '
      '(%d / %d)' % (nst // 2, nsame, nst), nsame == nst)
check('T2 the beta pv_BetaS computes is SciPy\'s P(XCL < X < XCU) to %.1e relative, down to 1E-290' % worst, worst < 1e-8)
e = [hb.call('pv_Rel', x) for x in ('< 0.001', '> -0.001', '0.050', '')]
check('T3 pv_Rel: "< 0.001" -> " < 0.001", "> -0.001" -> " > -0.001", "0.050" -> " = 0.050", "" -> " = ": %r' % e,
      e == [' < 0.001', ' > -0.001', ' = 0.050', ' = '])
# T4. the sites left alone
src2 = open(PROG, encoding='utf-8').read()
check('T4 the drag clamps alpha to 0.001-0.5 (so the drag and snap hints never reach the floor), unchanged',
      'na:=MIN(0.5,MAX(0.001,na*TL));' in src2 and 'ALAD:={0.001,0.005,0.01,0.02,0.05,0.10,0.20};' in src2)
found = []
for tl in (1, 2):
    for al in (0.001, 0.005, 0.05, 0.0001):
        for mm1 in (100, 101, 104, 110, 120):
            for nn in (2, 30, 200):
                h = Harness(PROG, cas='fail'); h.choose(1); h.answer({'MM1': mm1, 'AL': al, 'NN': nn})
                if tl == 2:
                    h.tap(80, 230)
                h.press('Esc'); h.call('POWERVIZ')
                pg = [s for s in h.pages if s.func == 'pv_Draw']
                for t in pg[-1].texts:
                    if (t.text.startswith('β') or t.text.startswith('power')) and t.y < 150 and '<' in t.text:
                        found.append(t.text)
check('T4 the plot\'s beta and power labels (2 decimals) are never drawn below 0.01 (120 states; v2.5b\'s 960-state '
      'sweep found none either): %r' % found[:3], not found)


# T5. the routine diff and the line diff, v2.5b -> v2.5c
def t_code(txt):
    out = []
    for l in txt.split('\n'):
        o, ins = [], False
        for i, ch in enumerate(l):
            if ch == '"':
                ins = not ins
            if not ins and l[i:i + 2] == '//':
                break
            o.append(ch)
        s_ = ''.join(o).strip()
        if s_:
            out.append(s_)
    return out


s0 = open(V25B, encoding='utf-8').read()
src2c = open(V25C, encoding='utf-8').read()     # 2.5d: the v2.5b -> v2.5c diff is read from v2.5c's own file
D0, D1 = _bodies(s0), _bodies(src2c)
dd = sorted(n for n in set(D0) | set(D1) if D0.get(n) != D1.get(n))
check('T5 routines that differ from v2.5b: %s (pv_BetaS, pv_Rel new)' % dd,
      dd == ['POWERVIZ', 'pv_BetaS', 'pv_Draw', 'pv_PCDraw', 'pv_Rel', 'pv_Tails'])
k0, k1 = t_code(s0), t_code(src2c)
mi, pl = [], []
for op, i1, i2, j1, j2 in _dl.SequenceMatcher(None, k0, k1, autojunk=False).get_opcodes():
    if op in ('replace', 'delete'):
        mi += k0[i1:i2]
    if op in ('replace', 'insert'):
        pl += k1[j1:j2]
wm = ['HB1 := "2-sided: α = "+pv_FMTP(AL,3)+" is split, "+',
      'HB1 := "1-sided: all of α = "+pv_FMTP(AL,3)+" sits in one tail,";',
      'TEXTOUT_P("α = "+pv_FMTP(AL,3),G1,8,193,2,cgry);', 'TEXTOUT_P("β = "+pv_FMTP(1-PW,3),G1,108,193,2,cgry);',
      'lbs:=pv_EffLbl()+", α = "+pv_FMTP(AL,3)+", "+STRING(TL,1,0)+"-sided";',
      'lbs:="n = "+STRING(NN,1,0)+"/grp, α = "+pv_FMTP(AL,3)+", "+STRING(TL,1,0)+"-sided";',
      'lbs:="at n = "+STRING(pv_NofC(selc),1,0)+": power = "+pv_FMTP(PWC(selc),3)+", lift = use this n";',
      'lbs:="at n = "+STRING(NN,1,0)+": power = "+pv_FMTP(PW,3)+", touch = pick n, key = back";',
      'lbs:="at "+IFTE(TT<=2,"d","h")+" = "+pv_FMT(pv_EffSz(),2)+": power = "+pv_FMTP(PW,3)+", key or tap = back";',
      '"n = "+STRING(NN,1,0)+"/group  α = "+pv_FMTP(AL,3)+"  "+STRING(TL,1,0)+"-sided"+nl+',
      '"POWER = "+pv_FMTP(PW,4)+"   (β = "+pv_FMTP(1-PW,4)+")"+nl+']
wp = [l.strip() for l in D1['pv_Rel'].split('\n') if l.strip()] + [l.strip() for l in D1['pv_BetaS'].split('\n') if l.strip()] + [
      'HB1 := "2-sided: α"+pv_Rel(pv_FMTP(AL,3))+" is split, "+',
      'HB1 := "1-sided: all of α"+pv_Rel(pv_FMTP(AL,3))+" sits in one tail,";',
      'TEXTOUT_P("α"+pv_Rel(pv_FMTP(AL,3)),G1,8,193,2,cgry);', 'TEXTOUT_P("β"+pv_Rel(pv_BetaS(3)),G1,108,193,2,cgry);',
      'lbs:=pv_EffLbl()+", α"+pv_Rel(pv_FMTP(AL,3))+", "+STRING(TL,1,0)+"-sided";',
      'lbs:="n = "+STRING(NN,1,0)+"/grp, α"+pv_Rel(pv_FMTP(AL,3))+", "+STRING(TL,1,0)+"-sided";',
      'lbs:="at n = "+STRING(pv_NofC(selc),1,0)+": power"+pv_Rel(pv_FMTP(PWC(selc),3))+", lift = use this n";',
      'lbs:="at n = "+STRING(NN,1,0)+": power"+pv_Rel(pv_FMTP(PW,3))+", touch = pick n, key = back";',
      'lbs:="at "+IFTE(TT<=2,"d","h")+" = "+pv_FMT(pv_EffSz(),2)+": power"+pv_Rel(pv_FMTP(PW,3))+", key or tap = back";',
      '"n = "+STRING(NN,1,0)+"/group  α"+pv_Rel(pv_FMTP(AL,3))+"  "+STRING(TL,1,0)+"-sided"+nl+',
      '"POWER"+pv_Rel(pv_FMTP(PW,4))+"   (β"+pv_Rel(pv_BetaS(4))+")"+nl+']
check('T5 the code lines that changed are exactly the 11 listed (and the two new routines): -%r +%r'
      % ([x for x in mi if x not in wm], [x for x in pl if x not in wp]), sorted(mi) == sorted(wm) and sorted(pl) == sorted(wp))
BIN = set(l.strip().lower() for l in open('/home/claude/work/gate_r2/HP_Prime_Builtin_Names.txt', encoding='utf-8')
          if l.strip() and not l.startswith('#'))
check('T5 the new names pv_Rel, pv_BetaS, rlS, bsD, bsV are not built-ins (case ignored) and carry the pv_ tag',
      not any(n.lower() in BIN for n in ('pv_Rel', 'pv_BetaS', 'rlS', 'bsD', 'bsV')))
check('T5 version strings (2.5d: v2.5d\'s): the banner, the tested-on lines, the v2.5d paragraph above v2.5c\'s',
      src2.split('\n')[3] == '// POWERVIZ - v2.5d' and 'v2.2 to v2.5d have NOT yet been run on a G1 or G2.' in src2
      and 'v2.5b, v2.5c and\n//   v2.5d have not run there yet (v2.5d has run only in the PC\n//   harness)' in src2
      and '// What changed in v2.5d (19 Oct 2026): P1 and the "POWER > 0.999"' in src2
      and '// v2.5c (17 Oct 2026, evening) - what changed' in src2)
depth, bad = 0, []
for n_, l in enumerate(src2.split('\n'), 1):
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
check('T5 no // comment inside an open bracket: %r' % bad[:5], not bad)
check('T5 INSTRING: the same guarded lines as v2.5b (2.5d: in v2.5d too); pv_Rel reads LEFT(rlS, 1) only inside IF DIM(rlS) > 0',
      [l for l in k0 if 'INSTRING(' in l] == [l for l in k1 if 'INSTRING(' in l]
      == [l for l in t_code(src2) if 'INSTRING(' in l])
mine2 = [(p, hh) for p, hh in ALLH if p == PROG]
sci2 = sorted({(round(v, 12), d, r) for p, hh in mine2 for v, d, r in hh.sci_strings})
check('T6 no scientific STRING(x, 2, d) result in any of the %d v2.5c runs (section T included)' % len(mine2), not sci2)


# ================================================================ U (2.5d)
print('\n== U. 2.5d: P1, the top floor, the disclaimer (harness v3e) ==')
import subprocess as _sp
src2d = open(PROG, encoding='utf-8').read()


def u_scene(prog, tt, ans, cas='giac', formula=False, pown=False, tails2=False):
    h = Harness(prog, cas=cas)
    h.choose(tt); h.answer(ans)
    if tails2:
        h.tap(80, 230)
    if formula:
        h.press('Enter'); h.choose(6); h.press('Enter')
    if pown:
        h.tap(240, 230); h.press('Enter')
    h.press('Esc')
    h.call('POWERVIZ')
    return h


def u_panel(h):
    pg = [x for x in h.pages if x.func == 'pv_Draw'][-1]
    return pg


def u_n80line(h):
    return [t.text for t in u_panel(h).texts if t.y == 206 and t.text.startswith('n')][-1]


def u_formula(h):
    fp = [x for x in h.pages if x.func == 'pv_Formula']
    return [t.text for t in fp[-1].texts] if fp else []


# U1. P1 -- four scenes where the bracket is negative (1-sided alpha above 0.5), CAS answering and failing
P1 = ((1, {'MM1': 107.5, 'AL': 0.999}, 20.225, '15×-3.090 + 15×0.842'),
      (2, {'AL': 0.9}, 3.484, '15√2×-1.282 + 15√2×0.842'),
      (3, {'AL': 0.95}, 16.82, '√(0.25)×-1.645 + √(0.24)×0.842'),
      (4, {'AL': 0.99}, 109.746, '√(0.495)×-2.326 + √(0.49)×0.842'))
for tt, ans, ncf_old, frag in P1:
    for cas in ('giac', 'fail'):
        a = u_scene(V25C, tt, ans, cas, formula=True)
        b = u_scene(PROG, tt, ans, cas, formula=True)
        fa, fb = u_formula(a), u_formula(b)
        old_ok = (abs(a.globals_['NCF'] - ncf_old) < 2e-3 and a.globals_['N80'] == 2
                  and any(l.startswith('Round UP (whole people): n = ') for l in fa))
        new_ok = (b.globals_['NCF'] == -1 and b.globals_['N80'] == 2
                  and '    no root: the bracket is 0 or less, and √n > 0' in fb
                  and 'Power is above 0.80 at every n;  trying n: n₈₀ = 2' in fb
                  and '1-sided α above 0.5: the test rejects H₀ more' in fb
                  and 'often than not even when there is no effect.' in fb
                  and not any(l.startswith('Round UP') for l in fb) and not any('-1.00' in l for l in fb)
                  and any(frag in l and not re.search(r'= [\d.]+$', l) for l in fb)
                  and len([x for x in b.pages if x.func == 'pv_Formula'][-1].texts) <= 15 + 4)
        check('U1 P1 test %d, %s, CAS %s: v2.5c NCF %.3f, "Round UP (whole people)" -> v2.5d NCF -1, no value, '
              '"no root", "Power is above 0.80 at every n", and why' % (tt, ans, cas, a.globals_['NCF']),
              old_ok and new_ok, str(fb[-6:]))
    pa, pb = u_n80line(a), u_n80line(b)
    check('U1 P1 test %d: the panel\'s n80 line: v2.5c %r -> v2.5d %r (no bracket)' % (tt, pa, pb),
          pa.startswith('n₈₀ = 2 (') and pb == 'n₈₀ = 2')
# the Pow-n view: no "formula:" label beside n80 when there is no root
for prog, tag in ((V25C, '2.5c'), (PROG, '2.5d')):
    h = u_scene(prog, 1, {'MM1': 107.5, 'AL': 0.999}, 'fail', pown=True)
    fl = [t.text for s_ in h.pages if s_.func == 'pv_PCDraw' for t in s_.texts if t.text.startswith('formula: ')]
    if tag == '2.5c':
        check('U1 P1 Pow-n view, v2.5c: "%s"' % (fl[:1],), bool(fl) and '20.2' in fl[0])
    else:
        check('U1 P1 Pow-n view, v2.5d: no "formula:" label (%r)' % fl[:1], not fl)
# ordinary cases are unchanged: defaults, alpha 0.5 (za = 0), a 1-sided alpha 0.6 (za < 0 but the bracket positive)
for tt, ans in ((1, ACCEPT), (1, {'MM1': 107.5, 'AL': 0.5}), (1, {'MM1': 107.5, 'AL': 0.6}), (3, ACCEPT),
                (4, {'AL': 0.2}), (2, {'AL': 0.05})):
    a = u_scene(V25C, tt, ans, 'giac', formula=True)
    b = u_scene(PROG, tt, ans, 'giac', formula=True)
    check('U1 ordinary: test %d, %s: NCF %.3f, n80 %d, the panel\'s n80 line and the whole formula page are v2.5c\'s'
          % (tt, 'defaults' if ans is ACCEPT else ans, b.globals_['NCF'], b.globals_['N80']),
          a.globals_['NCF'] == b.globals_['NCF'] > 0 and u_n80line(a) == u_n80line(b) and u_formula(a) == u_formula(b))
# the sweep: pv_NCF against the replica with P1's guard, and the claim the page makes
hs = Harness(PROG, cas='fail')
hs.call('pv_Init')
bad, nneg, n2 = [], 0, 0
for tt in (1, 2, 3, 4):
    for tl in (1, 2):
        for al in (0.001, 0.05, 0.3, 0.5, 0.6, 0.8, 0.9, 0.95, 0.99, 0.999):
            for eff in (-0.6, -0.1, 0.1, 0.6):
                mm0, sg, pp0 = 100.0, 15.0, 0.5
                mm1, pp1 = mm0 + eff * sg, min(0.98, max(0.02, pp0 + eff * 0.3))
                g = hs.globals_
                g.update({'TT': float(tt), 'TL': float(tl), 'AL': al, 'MM0': mm0, 'MM1': mm1, 'SG': sg, 'PP0': pp0,
                          'PP1': pp1})
                v = hs.call('pv_NCF')
                za, zb = norm.ppf(1 - al / tl), norm.ppf(0.8)
                u, w = uw(tt, sg, pp0, pp1)
                brk = za * u + zb * w
                if brk <= 0:
                    nneg += 1
                    pw2 = power(tt, tl, al, mm0, mm1, sg, pp0, pp1, 2)
                    if not (v == -1 and tl == 1 and al > 0.5 and pw2 > 0.8):
                        bad.append((tt, tl, al, eff, v, pw2))
                    n2 += 1
                else:
                    if abs(v - ncf(tt, tl, al, mm0, mm1, sg, pp0, pp1)) > 1e-9 * max(1, v):
                        bad.append((tt, tl, al, eff, v, 'ncf'))
check('U1 sweep, 4 tests x 2 tails x 10 alphas x 4 effects: pv_NCF = the closed form wherever the bracket is positive; '
      'in the %d states where it is not, pv_NCF is -1, the test is 1-sided with alpha above 0.5, and power at n = 2 is '
      'already above 0.80 (so "above 0.80 at every n" holds) %r' % (nneg, bad[:3]), not bad and nneg > 0)

# U2. the top floor
hf = Harness(PROG, cas='fail'); hf.call('pv_Init')
hc = Harness(V25C, cas='fail'); hc.call('pv_Init')
cases = ((0.9996, 3, '> 0.999', '1.000'), (1.0, 3, '> 0.999', '1.000'), (0.9994, 3, '0.999', '0.999'),
         (0.99995, 4, '> 0.9999', '1.0000'), (0.99994, 4, '0.9999', '0.9999'), (0.996, 2, '> 0.99', '1.00'),
         (0.5, 3, '0.500', '0.500'), (0.0004, 3, '< 0.001', '< 0.001'), (0.0, 3, '0.000', '0.000'),
         (0.05, 3, '0.050', '0.050'))
got = [(hf.call('pv_FMTP', x, float(d)), hc.call('pv_FMTP', x, float(d))) for x, d, _, _ in cases]
check('U2 pv_FMTP: v2.5d %r (v2.5c %r)' % ([g_[0] for g_ in got], [g_[1] for g_ in got]),
      [g_[0] for g_ in got] == [c[2] for c in cases] and [g_[1] for g_ in got] == [c[3] for c in cases])
check('U2 pv_Rel on the floor: " > 0.999"', hf.call('pv_Rel', hf.call('pv_FMTP', 0.9996, 3.0)) == ' > 0.999')
for ans, big_old, big_new, exit_new in (({'MM1': 107.5, 'NN': 100}, '1.000', '> 0.999', 'POWER = 0.9996   (β = 0.0004)'),
                                         ({'MM1': 110, 'NN': 5000}, '1.000', '> 0.999', 'POWER > 0.9999   (β < 0.0001)'),
                                         ({'MM1': 107.5, 'AL': 0.999}, '1.000', '> 0.999', 'POWER > 0.9999   (β < 0.0001)'),
                                         (ACCEPT, '0.572', '0.572', 'POWER = 0.5718   (β = 0.4282)')):
    a = u_scene(V25C, 1, ans, 'fail'); b = u_scene(PROG, 1, ans, 'fail')
    ba = [t for t in u_panel(a).texts if t.font == 5]; bb = [t for t in u_panel(b).texts if t.font == 5]
    eb = b.msgboxes[-1].lines[3]
    check('U2 the big POWER readout, %s: v2.5c "%s" -> v2.5d "%s" (font 5 from x 222: ends near %d < 317); exit box "%s"'
          % ('defaults' if ans is ACCEPT else ans, ba[0].text, bb[0].text, 222 + 9.5 * len(bb[0].text), eb),
          ba[0].text == big_old and bb[0].text == big_new and 222 + 9.5 * len(bb[0].text) < 317 and eb == exit_new)
# the labels inside the plot's regions (2 decimals) and the Pow-n readout
for ans, lab_old, lab_new in (({'MM1': 107.5, 'AL': 0.5}, 'power = 1.00', 'power > 0.99'),
                              ({'MM1': 100.5, 'AL': 0.0001}, 'β = 1.00', 'β > 0.99'),
                              ({'MM1': 110}, None, None)):
    a = u_scene(V25C, 1, ans, 'fail'); b = u_scene(PROG, 1, ans, 'fail')
    la = [t.text for t in u_panel(a).texts if t.y < 150 and (t.text.startswith('β') or t.text.startswith('power'))]
    lb = [t.text for t in u_panel(b).texts if t.y < 150 and (t.text.startswith('β') or t.text.startswith('power'))]
    if lab_old is None:
        # (at the defaults neither region is wide enough for its label; d 0.67 draws "power = 0.98")
        check('U2 plot labels, an ordinary scene (d 0.67, power 0.978): the same in v2.5c and v2.5d: %r' % lb,
              la == lb and lb == ['power = 0.98'])
    else:
        check('U2 plot label, %s: v2.5c %r -> v2.5d %r' % (ans, la, lb), lab_old in la and lab_new in lb
              and not any(' = >' in x or ' = <' in x for x in lb))
a = u_scene(V25C, 1, {'MM1': 110, 'NN': 200}, 'fail', pown=True)
b = u_scene(PROG, 1, {'MM1': 110, 'NN': 200}, 'fail', pown=True)
ra = [t.text for s_ in a.pages if s_.func == 'pv_PCDraw' for t in s_.texts if t.text.startswith('at n = ')]
rb = [t.text for s_ in b.pages if s_.func == 'pv_PCDraw' for t in s_.texts if t.text.startswith('at n = ')]
check('U2 Pow-n readout at n 200, d 0.67: v2.5c %r -> v2.5d %r' % (ra[-1:], rb[-1:]),
      ra and rb and ra[-1].startswith('at n = 200: power = 1.000') and rb[-1].startswith('at n = 200: power > 0.999'))
# the sweep: every panel, the exit box: never "POWER 1.000" / "power = 1.000", never "= >" or "= <"
badf = []
for tt in (1, 2, 3, 4):
    for tl in (1, 2):
        for al, nn, mm1, pp1 in ((0.05, 5000, 110, 0.7), (0.5, 30, 107.5, 0.65), (0.001, 2, 100.5, 0.52),
                                 (0.2, 200, 104, 0.6), (0.999, 100, 120, 0.9)):
            ans = {'MM1': mm1, 'NN': nn, 'AL': al} if tt <= 2 else {'PP1': pp1, 'NN': nn, 'AL': al}
            h = u_scene(PROG, tt, ans, 'fail', tails2=(tl == 2))
            tx = [t.text for s_ in h.pages for t in s_.texts] + [l for m in h.msgboxes for l in m.lines]
            big = [t.text for t in u_panel(h).texts if t.font == 5]
            if big and big[0] in ('1.000',):
                badf.append((tt, tl, al, nn, 'big 1.000'))
            for x in tx:
                if re.search(r'=\s*[<>]', x) or re.search(r'(POWER|power)\s*=\s*1\.0+\b', x):
                    badf.append((tt, tl, al, nn, x))
check('U2 sweep, 4 tests x 2 tails x 5 scenes (alpha 0.001-0.999, n 2-5000): no POWER 1.000, no "= >" / "= <" %r'
      % badf[:3], not badf)

# U3. the disclaimer
DISC = ('DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely '
        'on its results for legal purposes.')


def u_header(txt):
    hdr = txt.split('// Firmware: written for')[0]
    return ' '.join(l.lstrip('/').strip() for l in hdr.split('\n') if l.startswith('//'))


check('U3 the header carries the disclaimer word for word (v2.5c: no); the old "For academic use only ... not been '
      'rigorously verified" lines stay (D17)',
      DISC in u_header(src2d) and DISC not in u_header(open(V25C, encoding='utf-8').read())
      and 'Results have not been rigorously verified.' in src2d)
hp = []
for prog in (V25C, PROG):
    h = Harness(prog, cas='fail'); h.call('pv_Init'); h.press('Enter', 'Enter', 'Enter'); h.call('pv_ShowHelp')
    hp.append(h.pages)
LINE = 'Teaching aid; not for clinical or legal use.'
p1 = [t for t in hp[1][0].texts if t.text == LINE]
check('U3 help page 1 shows "%s" (font 1, red, y 208: above the footer at 222; %d characters, ends near x %d < 317); '
      'every other line of the three pages is v2.5c\'s' % (LINE, len(LINE), 12 + 6.5 * len(LINE)),
      len(p1) == 1 and p1[0].y == 208 and p1[0].font == 1 and p1[0].hex == '#FF0000' and 12 + 6.5 * len(LINE) < 317
      and [(t.text, t.y) for t in hp[1][0].texts if t.text != LINE] == [(t.text, t.y) for t in hp[0][0].texts]
      and [[(t.text, t.y) for t in pg.texts] for pg in hp[1][1:3]] == [[(t.text, t.y) for t in pg.texts] for pg in hp[0][1:3]])

# U4. the review's own check_PowerViz.py on v2.5c and on v2.5d
_chk = open('/home/claude/work/review/check_PowerViz.py', encoding='utf-8').read()
_chk = _chk.replace("HERE = os.path.dirname(os.path.abspath(__file__))", "HERE = '/home/claude/work/review'")
rv = {}
for prog, tag in ((V25C, '2.5c'), (PROG, '2.5d')):
    c2 = _chk.replace("SRC = os.path.join(FLEET, 'PowerViz_v2.5c.txt')", 'SRC = %r' % prog)
    assert c2 != _chk
    out = _sp.run([sys.executable, '-'], input=c2, capture_output=True, text=True, timeout=3600).stdout
    m = re.search(r'(\d+) checks? failed', out)
    rv[tag] = (m.group(1) if m else out[-300:], [l[5:80] for l in out.split('\n') if l.startswith('FAIL ')])
    print('   review check_PowerViz.py on v%s: %s failed %r' % (tag, rv[tag][0], rv[tag][1]))
check('U4 the review\'s check_PowerViz.py: its one failure on v2.5c (the Pow-n subtitle at sigma = 1E-6, absurd input '
      'the review left "as a FAIL in the log for the record"; not on the fix list) is the only one on v2.5d too',
      rv['2.5c'][0] == '1' and rv['2.5d'][0] == '1' and rv['2.5c'][1] == rv['2.5d'][1]
      and '12 probe scenes' in rv['2.5d'][1][0])

# U5. the routine diff and the code-line diff, v2.5c -> v2.5d
s0c = open(V25C, encoding='utf-8').read()
E0, E1 = _bodies(s0c), _bodies(src2d)
ed = sorted(n for n in set(E0) | set(E1) if E0.get(n) != E1.get(n))
check('U5 routines that differ from v2.5c: %s' % ed, ed == ['pv_Draw', 'pv_FMTP', 'pv_Formula', 'pv_NCF', 'pv_ShowHelp'])
check('U5 outside them only comments differ', _outside(s0c, ed) == _outside(src2d, ed))
k0, k1 = t_code(s0c), t_code(src2d)
mi, pl = [], []
for op, i1, i2, j1, j2 in _dl.SequenceMatcher(None, k0, k1, autojunk=False).get_opcodes():
    if op in ('replace', 'delete'):
        mi += k0[i1:i2]
    if op in ('replace', 'insert'):
        pl += k1[j1:j2]
print('   code lines removed %d, added %d (the formula page\'s 2-sided/1-sided block is re-indented inside an ELSE)'
      % (len(mi), len(pl)))
must_new = ['IF nca*ncu + ncb*ncw <= 0 THEN RETURN -1; END;',
            'IF xx <= 1 AND ROUND(xx, dd) >= 1 THEN RETURN "> " + STRING(1 - thr,2,dd); END;',
            'lbs:="β"+pv_Rel(pv_FMTP(1-PW,2));', 'lbs:="power"+pv_Rel(pv_FMTP(PW,2));',
            'IF NCF < 0 THEN', 'fs1 := CONCAT(pv_Wrap("  n = "+fs3, 54), {"    no root: the bracket is 0 or less, and "+SQG+"n > 0"});',
            'fln := CONCAT(fln, {"Power is above 0.80 at every n"+fs2});',
            'fln := CONCAT(fln, {"1-sided α above 0.5: the test rejects H₀ more",',
            '"often than not even when there is no effect."});',
            'TEXTOUT_P("Teaching aid; not for clinical or legal use.",G1,12,208,1,ccrt);']
gone = ['lbs:="β = "+pv_FMTP(1-PW,2);', 'lbs:="power = "+pv_FMTP(PW,2);']
# every removed line is either one of the two labels or comes back re-indented (same text)
other_mi = [x for x in mi if x not in gone and x not in pl]
check('U5 the changed code lines: the guard, the floor, the two labels, the formula page\'s new branch and the '
      'disclaimer line; every other removed line comes back unchanged (re-indented) %r %r'
      % ([x for x in must_new if x not in pl], other_mi),
      all(x in pl for x in must_new) and all(x in mi for x in gone) and not other_mi)
BIN2 = set(l.strip().lower() for l in open('/home/claude/work/gate_f19/HP_Prime_Builtin_Names.txt', encoding='utf-8')
           if l.strip() and not l.startswith('#'))
check('U5 no new names (the routines and LOCALs are v2.5c\'s); no MAKELIST with K added',
      not [x for x in pl if x.startswith('LOCAL ')] and not [x for x in pl if 'MAKELIST' in x])

# U6. scientific fixed decimals, every v2.5d run
mine3 = [(p, hh) for p, hh in ALLH if p == PROG]
sci3 = sorted({(round(v, 12), d, r) for p, hh in mine3 for v, d, r in hh.sci_strings})
print('   h.sci_strings over the %d v2.5d runs: %r' % (len(mine3), sci3))
check('U6 no scientific STRING(x, 2, d) result in any of the %d v2.5d runs (sections A-U)' % len(mine3), not sci3)

print('\n%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
sys.exit(1 if FAIL else 0)
