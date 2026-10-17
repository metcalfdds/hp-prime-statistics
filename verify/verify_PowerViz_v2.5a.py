#!/usr/bin/env python3
"""verify_PowerViz_v2.5a.py -- checks PowerViz v2.5a (17 Oct 2026): the CAS call form that
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
import os
import subprocess
import sys

import warnings

import sympy as sp
from scipy.stats import norm
from statsmodels.stats.power import NormalIndPower, normal_sample_size_one_tail
from statsmodels.stats.proportion import samplesize_proportions_2indep_onetail

sys.path.insert(0, '/home/claude/work/harness')
from ppl_run_v3b import Harness, ACCEPT, giac_eval, prime_eval   # noqa: E402

warnings.filterwarnings('ignore')       # statsmodels' solver warnings when n is in the thousands
PROG = '/home/claude/work/out/PowerViz_v2.5a.txt'
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
print('\n== B. the program in the harness (ppl_run_v3b) ==')


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
print('\n== B12. v2.4\'s verify_PowerViz.py run against v2.5a (harness v3b) ==')
old = open('/home/claude/work/out/verify_PowerViz.py', encoding='utf-8').read()
old = old.replace("from ppl_run_v1 import Harness, ACCEPT", "from ppl_run_v3b import Harness, ACCEPT")
# the one script change v2.5 needs ON PURPOSE: help now has THREE pages (the n formula),
# so the help check needs one more key to get past page 3
HELP24 = "hh.choose(1).answer(ACCEPT).tap(300, 230).choose('Help').press('Enter').press('Enter').press('Esc')"
assert old.count(HELP24) == 1
old = old.replace(HELP24, "hh.choose(1).answer(ACCEPT).tap(300, 230).choose('Help').press('Enter').press('Enter')"
                          ".press('Enter').press('Esc')")
reg = os.path.join(SCR, 'verify_PowerViz_on_v25a.py')
open(reg, 'w', encoding='utf-8').write(old)
res = subprocess.run([sys.executable, reg], capture_output=True, text=True, env=dict(os.environ, POWERVIZ=PROG))
lines = res.stdout.split('\n')
fails = [ln for ln in lines if ln.startswith('FAIL')]
npass = sum(1 for ln in lines if ln.startswith('PASS'))
print('   %d PASS, %d FAIL%s' % (npass, len(fails), ('   (stderr: ' + res.stderr.strip().split('\n')[-1] + ')')
                                if res.returncode and not fails else ''))
for ln in fails:
    print('   ' + ln)
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

print('\n%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
sys.exit(1 if FAIL else 0)
