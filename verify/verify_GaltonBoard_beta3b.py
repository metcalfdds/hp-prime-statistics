#!/usr/bin/env python3
"""verify_GaltonBoard_beta3b.py -- checks for GaltonBoard beta 3b (17 Oct 2026): solid pegs and balls
(GfxProbe beta 1 T09 on the emulator: ARC_P rings leave diagonal holes) and bin-count labels clear of
the overlays (the emulator's "9" half hidden by the magenta line).  Built from
verify_GaltonBoard_beta3a.py; every check is kept and now runs in harness v3c.  New or changed
checks are marked "3b":
  P. pegs and balls: no ARC_P is drawn anywhere; every peg is two grey RECT_P bars covering
     exactly a disc of radius 2, every ball three red RECT_P bars covering exactly a disc of
     radius 3; fewer drawing calls than beta 3a, per frame of a drop and of a pour, and per scene.
  L. labels: for boards R 3-9, p 0.3-0.72, overlays 1 and 2, many n, no count label above a bar
     touches a magenta square, a magenta line or the green curve; beta 3a in the same states
     shows the collisions the emulator saw.
  G. beta 3b against beta 3a: only gbDisc, gbScene, gbBar and the new gbLblTop differ.
(The beta 3a description follows; "harness v3b" there now means v3c.)

  A. Giac (desktop 1.9, icas): the binomial -> Poisson limit needs a NUMERIC k (a symbolic k
     fails), the template's output forms, and "inf" against "+infinity".
  B. The exact bin probability, as THE PROGRAM builds it (gbXBin, captured from the run harness
     with cas='giac'), for every R the board allows (3 to 12), every k, and p = 1/2, 3/10, 37/100,
     1/20, 19/20, 1/4, 3/4, 0.123 (a typed p with three decimals): Giac's fraction == the Python
     Fraction C(R,k) p^k (1-p)^(R-k); its float == scipy.stats.binom.pmf == the PPL BINOMIAL on
     the panel.  A p that is not a simple ratio (0.3333) sends nothing to the CAS.  The cache asks
     once per bar.  The panel's "too long" rule counts the digits right.
  C. The Poisson page: the program's limit text (gbPsLim) for boards giving mu = 4, 3.7, 0.15,
     11.4, 2.4, 6, 0.5 and every k drawn, parsed with SymPy and compared EXACTLY with
     mu^k e^(-mu) / k! (and with scipy.stats.poisson.pmf); the PPL bars (gbPsB) == scipy's
     binom.pmf(k, R, mu/R) for R, 4R, 16R and poisson.pmf; the binomials close in on the Poisson.
  D. End to end in the harness, cas='giac' AND cas='fail': welcome, tap a bar (the panel), the
     Menu soft key -> "Where Poisson comes from", a tap on a bar, Right, Esc, quit.  Then a pour,
     x10 and a single drop: no CAS calls.  The fallback shows the decimal and the "decimal" badge.
  E. The fence: a call-graph check (the CAS is reachable only from gbBinInfo and gbPoisson, never
     from an animation, a drag or a frame routine), and the routines the brief says to keep --
     the #PYTHON block, pour, the drops, the drag, the scene -- byte-identical to beta 2.
  F. Layout: the panel's lines inside the panel, the Poisson page above y 235 and inside x 318.

  G. 3a: beta 3 itself in harness v3b (its gbCas hands back its own text, so every exact line
     falls back), and beta 3a against beta 3: only gbCas, gbPsLim and the new gbIVal differ.

Run:  python3 verify_GaltonBoard_beta3b.py     (needs SciPy, SymPy and Giac's icas; reads files only)
"""
import sys, re, math, subprocess, tempfile, os
from fractions import Fraction as Fr
from scipy import stats
import sympy as sp

sys.path.insert(0, '/home/claude/work/out')
from ppl_run_v3c import Harness, prime_print  # noqa: E402

SRC = '/home/claude/work/out/GaltonBoard_beta3b.txt'
B3A = '/home/claude/work/out/GaltonBoard_beta3a.txt'
OLD = '/home/claude/work/out/GaltonBoard_beta2.txt'
BETA3 = '/home/claude/work/out/GaltonBoard_beta3.txt'
FAILS = []
NPASS = [0]


def check(cond, msg):
    if cond:
        NPASS[0] += 1
    else:
        FAILS.append(msg)
        print('FAIL ' + msg)
    return cond


def say(m):
    print(m)


def giac(lines):
    with tempfile.NamedTemporaryFile('w', suffix='.giac', delete=False) as f:
        f.write(';\n'.join(lines) + ';\n')
        name = f.name
    cp = subprocess.run(['icas', name], capture_output=True, text=True)
    os.unlink(name)
    ans = []
    for ln in (cp.stdout + '\n' + cp.stderr).split('\n'):
        t = ln.strip()
        if not t or t.startswith('// ') or t.startswith('Added ') or t.startswith('Warning'):
            continue
        ans.append(t.rstrip(','))
    return ans


def pfrac(p):
    """The program's rule (gbPFrac): p x 100 or p x 1000 a whole number, else None."""
    for d in (100, 1000):
        m = round(p * d)
        if abs(p * d - m) <= 1e-6:
            return Fr(m, d)
    return None


def H(cas='giac', seed=1):
    h = Harness(SRC, cas=cas, seed=seed)
    h.call('gbInit')
    return h


def board(h, R, p):
    h.globals_['gbR'] = float(R)
    h.globals_['gbP'] = float(p)
    h.call('gbLayout'); h.call('gbClear'); h.call('gbTheory')


# ================================================================ A
say('A. Giac 1.9 (desktop icas)')
# one expression per icas run, so an error on stderr cannot shift the answers
E = ['limit(comb(gbq,gbk)*(2/gbq)^gbk*(1-2/gbq)^(gbq-gbk),gbq,inf)',
     'simplify(limit(comb(gbq,3)*((4/1)/gbq)^3*(1-(4/1)/gbq)^(gbq-3),gbq,inf))',
     'simplify(limit(comb(gbq,3)*((37/10)/gbq)^3*(1-(37/10)/gbq)^(gbq-3),gbq,inf))',
     'simplify(limit(comb(gbq,3)*((4/1)/gbq)^3*(1-(4/1)/gbq)^(gbq-3),gbq,+infinity))',
     'comb(8,4)*(1/2)^4*(1/2)^4']
a = [' '.join(giac([e])) for e in E]
say('  symbolic k:                 %s' % a[0][:100])
check('Error' in a[0] or 'unable' in a[0].lower(), 'a symbolic k should fail in Giac: %s' % a[0])
say('  numeric k = 3, mu = 4:      %s' % a[1])
say('  numeric k = 3, mu = 37/10:  %s' % a[2])
say('  "+infinity" instead of inf: %s' % a[3])
say('  comb(8,4)*(1/2)^4*(1/2)^4:  %s' % a[4])
check(a[1] == '32/(3*exp(1)^4)' and a[1] == a[3], 'inf and +infinity agree')
check(a[2] == '50653*exp(-37/10)/6000', 'mu = 37/10, k = 3')
check(a[4] == '35/128', 'R = 8, k = 4 is 35/128')
# 3a: what the Prime prints for the same answers (CASProbe beta 1b): e^( where Giac writes exp(
check(prime_print(a[1]) == '32/(3*(e^(1))^4)' and 'exp' not in prime_print(a[2]),
      '3a: the Prime prints %s, %s' % (prime_print(a[1]), prime_print(a[2])))
say('  3a, in the Prime\'s printing: %s ; %s' % (prime_print(a[1]), prime_print(a[2])))

# ================================================================ B
say('\nB. the exact bin probability (gbXBin), every R and k, against Fraction and SciPy')
h = H('giac')
PS = [0.5, 0.3, 0.37, 0.05, 0.95, 0.25, 0.75, 0.123]
nb = 0
for p in PS:
    for R in range(3, 13):
        board(h, R, p)
        pf = pfrac(p)
        for k in range(0, R + 1):
            n0 = len(h.cas_calls)
            t = h.call('gbXBin', float(k))
            ex = math.comb(R, k) * pf ** k * (1 - pf) ** (R - k)
            check(t == str(ex), 'R %d p %s k %d: %s != %s' % (R, p, k, t, ex))
            check(abs(float(ex) - stats.binom.pmf(k, R, p)) < 1e-12, 'float vs scipy R %d k %d' % (R, k))
            check(len(h.cas_calls) == n0 + 1, 'one CAS call per new bar')
            t2 = h.call('gbXBin', float(k))
            check(t2 == t and len(h.cas_calls) == n0 + 1, 'the same bar again asks the CAS nothing')
            nb += 1
say('  %d bins (R 3..12, every k, p in %s): fraction == Fraction, float == binom.pmf' % (nb, PS))
board(h, 8, 0.5)
check(h.call('gbXBin', 4.0) == '35/128', 'the brief: 35/128 for R = 8, k = 4')
for p in (0.3333, 1 / 7):
    board(h, 8, p)
    n0 = len(h.cas_calls)
    check(h.call('gbXBin', 3.0) == '' and len(h.cas_calls) == n0, 'p = %s is not a simple ratio: no CAS call' % p)
say('  p = 0.3333 and 1/7: not simple ratios -> no CAS call, decimal only')
# the panel's lines, tapped through gbBinInfo
for (R, p, k, want) in ((8, 0.5, 4, '  = 35/128 = 0.2734'), (10, 0.3, 3, None), (12, 0.37, 5, None), (12, 0.123, 6, None)):
    board(h, R, p); h.call('gbScene')
    h.press('Esc'); h.reset_records(); h.call('gbBinInfo', float(k))
    pg = h.pages[-1]
    line = [x for x in pg.lines() if x.startswith('  = ')]
    ex = math.comb(R, k) * pfrac(p) ** k * (1 - pfrac(p)) ** (R - k)
    full = '  = %s = %.4f' % (ex, float(ex))
    if len(full) <= 33:
        exp_line = full
    else:
        exp_line = '  = %.4f (exact: %d digits)' % (float(ex), len(str(ex.numerator)) + len(str(ex.denominator)))
    check(line and line[0] == exp_line, 'panel R %d p %s k %d: %s != %s' % (R, p, k, line, exp_line))
    if want:
        check(line and line[0] == want, 'panel line for 35/128')
    form = [x for x in pg.lines() if x.startswith('P(')]
    say('  panel R = %2d, p = %-5s, k = %d:  %-40s %s' % (R, p, k, form[0] if form else '?', line[0] if line else '?'))
    check(any(x == 'exact (CAS)' for x in pg.lines()), 'panel badge (giac)')

# ================================================================ C
say('\nC. the Poisson page: the limit for each k against mu^k e^(-mu) / k!')
gq = sp.Symbol('gbq')
BOARDS = [(8, 0.5), (10, 0.37), (3, 0.05), (12, 0.95), (8, 0.3), (12, 0.5), (10, 0.05)]
for (R, p) in BOARDS:
    board(h, R, p)
    h.call('gbPsCalc')
    g = h.globals_
    mu = Fr(R) * pfrac(p)
    check(Fr(int(g['gbPsMN']), int(g['gbPsMD'])) == mu and math.gcd(int(g['gbPsMN']), int(g['gbPsMD'])) == 1,
          'mu as a fraction in lowest terms for R %d p %s' % (R, p))
    km = int(g['gbPsKm'])
    check(km == min(24, max(5, math.ceil(float(mu) + 3 * math.sqrt(float(mu)) + 1))), 'k max')
    Rs = [int(x) for x in g['gbPsR']]
    check(Rs == [R, 4 * R, 16 * R], 'the three row counts')
    bars = g['gbPsB']
    worst = 0
    dist = [0.0, 0.0, 0.0]
    for k in range(km + 1):
        for j in range(3):
            v = stats.binom.pmf(k, Rs[j], float(mu) / Rs[j]) if k <= Rs[j] else 0.0
            worst = max(worst, abs(bars[4 * k + j] - v))
            dist[j] += abs(bars[4 * k + j] - stats.poisson.pmf(k, float(mu)))
        worst = max(worst, abs(bars[4 * k + 3] - stats.poisson.pmf(k, float(mu))))
    check(worst < 1e-12, 'bars vs scipy, R %d p %s: %g' % (R, p, worst))
    check(dist[0] > dist[1] > dist[2], 'the binomials close in on the Poisson (R %d p %s: %s)' % (R, p, dist))
    nlim = 0
    for k in range(km + 1):
        t = h.call('gbPsLim', float(k))
        target = sp.Rational(mu.numerator, mu.denominator) ** k * sp.exp(-sp.Rational(mu.numerator, mu.denominator)) / sp.factorial(k)
        ok = check(t != '', 'no limit text for mu %s k %d' % (mu, k))
        check('exp' not in t, '3a: the limit text is in the Prime\'s printing (e^): %s' % t)
        if ok:
            # 3a: the Prime's e is Euler's number ((e^(1))^4, e^(-37/10))
            val = sp.sympify(t.replace('^', '**'), locals={'e': sp.E})
            check(sp.simplify(val - target) == 0, 'limit != mu^k e^-mu/k! for mu %s k %d: %s' % (mu, k, t))
            check(abs(float(val) - stats.poisson.pmf(k, float(mu))) < 1e-12, 'limit float vs scipy mu %s k %d' % (mu, k))
            nlim += 1
    tmpl = [c[0] for c in h.cas_calls if c[0].startswith('string(simplify(limit(')][-1]
    say('  R = %2d, p = %-4s mu = %-5s k 0..%-2d: %2d limits == mu^k e^-mu/k! exactly; bars == scipy (%.1e);'
        ' sum|binom - Poisson| %.3f > %.3f > %.3f' % (R, p, mu, km, nlim, worst, dist[0], dist[1], dist[2]))
lim_calls = [c for c in h.cas_calls if c[0].startswith('string(simplify(limit(')]
chk_calls = [c for c in h.cas_calls if c[0].startswith('string(round(evalf(')]
say('  e.g. the last template: %s' % tmpl)
say('       its answer:       %s' % lim_calls[-1][1])
say('  3a: the value check:    %s -> %s' % (chk_calls[-1][0], chk_calls[-1][1]))
check(len(chk_calls) == len(lim_calls), '3a: one value check per limit (%d, %d)' % (len(chk_calls), len(lim_calls)))
# 3a: a WRONG answer is refused by the value check (canned: the limit answers 33/(3e^4))
hw = Harness(SRC, cas={'string(simplify(limit(comb(gbq,3)*((4/1)/gbq)^3*(1-(4/1)/gbq)^(gbq-3),gbq,inf)))': '"33/(3*(e^(1))^4)"',
                       'string(round(evalf(33/(3*(e^(1))^4))*10^(10)))': '"2014771366"'}, seed=1)
hw.call('gbInit'); board(hw, 8, 0.5); hw.call('gbPsCalc')
check(hw.call('gbPsLim', 3.0) == '', '3a: a wrong limit (33/(3e^4)) is refused by its value')
hw2 = Harness(SRC, cas={'string(simplify(limit(comb(gbq,3)*((4/1)/gbq)^3*(1-(4/1)/gbq)^(gbq-3),gbq,inf)))': '"32/(3*(e^(1))^4)"',
                        'string(round(evalf(32/(3*(e^(1))^4))*10^(10)))': '"1953668148"'}, seed=1)
hw2.call('gbInit'); board(hw2, 8, 0.5); hw2.call('gbPsCalc')
check(hw2.call('gbPsLim', 3.0) == '32/(3*(e^(1))^4)', '3a: the right limit with the right value is kept')
check(round(stats.poisson.pmf(3, 4) * 1e10) == 1953668148, '3a: the canned value is POISSON(4, 3) x 10^10')
hw3 = Harness(SRC, cas={'string(simplify(limit(comb(gbq,3)*((4/1)/gbq)^3*(1-(4/1)/gbq)^(gbq-3),gbq,inf)))': '"limit(comb(gbq,3),gbq,∞)"'}, seed=1)
hw3.call('gbInit'); board(hw3, 8, 0.5); hw3.call('gbPsCalc')
check(hw3.call('gbPsLim', 3.0) == '' and len(hw3.cas_calls) == 1, '3a: an unevaluated limit (with the infinity sign) is refused, no value asked')
say('  3a: a wrong limit is refused by its value; the right one kept; an unevaluated one refused')

# ================================================================ D
say('\nD. end to end in the harness')


def pages(hh, func):
    return [q for q in hh.pages if q.func == func]


for mode in ('giac', 'fail'):
    hh = Harness(SRC, cas=mode, seed=7)
    hh.press('Enter')                    # past the welcome page
    hh.tap(160, 170)                     # tap bar 4 (R = 8, p = 0.5): the panel
    hh.press('Esc')                      # any key: back to the board
    hh.tap(300, 230)                     # Menu soft key
    hh.choose(14)                        # Where Poisson comes from (CAS)
    hh.tap(92, 100)                      # a tap on the bars at k = 2
    hh.press('Right')                    # k = 3
    hh.press('Esc')                      # back to the board
    hh.press('Esc')                      # leave
    ret = hh.call('GaltonBoard')
    check(hh.error is None, '%s: runtime error %s' % (mode, hh.error))
    pb = pages(hh, 'gbBinInfo')
    pp = pages(hh, 'gbPsDraw')
    check(pb and pp, '%s: pages missing' % mode)
    lines_b = pb[-1].lines()
    ks = [int(re.search(r'P\((\d+)\):', ' '.join(q.lines())).group(1)) for q in pp]
    check(ks[0] == 4 and 2 in ks and ks[-1] == 3, '%s: k went 4 -> 2 -> 3 (%s)' % (mode, ks))
    if mode == 'giac':
        check('  = 35/128 = 0.2734' in lines_b and 'exact (CAS)' in lines_b, 'giac panel')
        last = pp[-1].lines()
        check(any(x.startswith('as R → infinity = 32/(3×(e^(1))^4)') for x in last), 'giac Poisson k = 3 answer (3a: e^)')
        check(any(x.startswith('= μ^k e^(-μ)/k! = 4^3 e^(-4)/3! = 0.1954') for x in last), 'Poisson formula line')
        check('exact (CAS)' in last, 'giac Poisson badge')
        check(any('asking the CAS' in ' '.join(q.lines()) for q in pp), 'the "asking the CAS" frame')
        check(len(hh.cas_calls) == 7, 'giac: %d CAS calls, want 7 (panel, then k = 4, 2, 3 with a value check each, 3a)' % len(hh.cas_calls))
        check(not hh.cas_vars and not any('non-literal' in w for w in hh.warnings),
              '3a: no CAS variable assigned, no CAS call of a variable: %s' % (dict(hh.cas_vars),))
    else:
        check('  = 0.2734' in lines_b and 'decimal' in lines_b and not any('/128' in x for x in lines_b), 'fail panel')
        last = pp[-1].lines()
        check(any('(the CAS did not answer)' in x for x in last) and 'decimal' in last, 'fail Poisson page')
        check(any('= 0.1954' in x for x in last), 'fail Poisson decimal still shown')
        check(len(hh.cas_calls) == 4, 'fail: %d CAS attempts, want 4' % len(hh.cas_calls))
    check(ret.startswith('Galton Board: '), 'summary returned')
    say('  [%s] panel: %s | %s' % (mode, [x for x in lines_b if x.startswith('P(')][0],
                                    [x for x in lines_b if x.startswith('  = ')][0]))
    for x in pp[-1].lines():
        if x.startswith(('μ', 'P(', 'CAS', 'as R', '= ', '⇆')) or x in ('exact (CAS)', 'decimal'):
            say('      pois| ' + x)
    say('      CAS calls: %d; returned "%s"' % (len(hh.cas_calls), ret))

# 3a: every answer now ARRIVES IN QUOTES -- the CAS is asked for string(...), the answer is a PPL
# string, and STRING() of it adds a pair of quotes (CASProbe beta 1b T12) -- and gbCas drops them.
# (beta 3's test added a second pair by hand; in v3b the quotes are the normal path.)
hq = Harness(SRC, cas='giac', seed=7)
hq.press('Enter'); hq.tap(160, 170); hq.press('Esc'); hq.tap(300, 230); hq.choose(14)
hq.press('Right'); hq.press('Esc'); hq.press('Esc')
hq.call('GaltonBoard')
check(hq.error is None, 'quoted answers: runtime error %s' % hq.error)
check(all(c[0].startswith('string(') and c[1].startswith('"') for c in hq.cas_calls),
      '3a: every CAS text asks for string(...), every answer is quoted')
qb, qp = pages(hq, 'gbBinInfo')[-1].lines(), pages(hq, 'gbPsDraw')[-1].lines()
check('  = 35/128 = 0.2734' in qb and 'exact (CAS)' in qb, 'quoted answers: panel shows 35/128')
check(any(x.startswith('as R → infinity = ') and 'e^(' in x for x in qp) and 'exact (CAS)' in qp,
      'quoted answers: Poisson limit shown without quotes')
check(not any('"' in x for x in qb + qp), 'a quote mark reached the screen')
say('  [quoted] answers arrive as \'"..."\' (e.g. %s): gbCas dropped the quotes; panel "%s"' % (
    hq.cas_calls[0][1], [x for x in qb if x.startswith('  = ')][0]))

# the animations ask nothing: pour (hold the funnel), x10, one drop, x100, Drop 100,000 (PPL fallback)
hh = Harness(SRC, cas='giac', seed=8)
hh.press('Enter')
hh.tap(160, 18, hold=900)                # hold the funnel: pour
hh.tap(80, 230)                          # x10
hh.tap(26, 230)                          # Drop: one ball
hh.tap(130, 230)                         # x100
hh.tap(150, 80, lift=False)              # a tap on the pegs: one ball
hh.press('Esc')
hh.call('GaltonBoard')
check(hh.error is None, 'animations run: error %s' % hh.error)
check(len(hh.cas_calls) == 0, 'the pour, x10, drop and x100 made %d CAS calls' % len(hh.cas_calls))
say('  pour (held), x10, Drop, x100, a peg tap: n = %d balls, 0 CAS calls' % int(hh.globals_['gbN']))
hh = H('giac', 9)
n = hh.call('gbBigDrop', 300.0)
check(len(hh.cas_calls) == 0, 'Drop 100,000 made CAS calls')

# ================================================================ E
say('\nE. the fence')
src = open(SRC, encoding='utf-8').read()
old = open(OLD, encoding='utf-8').read()
code = re.sub(r'(?s)#PYTHON.*?#END', '', src)
code = re.sub(r'//[^\n]*', '', code)
code = re.sub(r'"[^"\n]*"', '""', code)
defs = [(m.group(1), m.start()) for m in re.finditer(r'(?m)^(?:EXPORT\s+)?([A-Za-z]\w*)\(([^()]*)\)\s*\nBEGIN', code)]
bodies = {}
for i, (nm, s0) in enumerate(defs):
    e = defs[i + 1][1] if i + 1 < len(defs) else len(code)
    bodies[nm] = code[s0:e]
names = set(bodies)
graph = {nm: {m for m in re.findall(r'\b([A-Za-z]\w*)\s*\(', b[b.index('BEGIN'):]) if m in names and m != nm}
         for nm, b in bodies.items()}


def reach(nm, seen=None):
    seen = set() if seen is None else seen
    for m in graph.get(nm, ()):
        if m not in seen:
            seen.add(m)
            reach(m, seen)
    return seen


callers = sorted(nm for nm in names if 'gbCas' in graph[nm])
check(callers == ['gbPsLim', 'gbXBin'], 'gbCas is called by %s' % callers)
check(sorted(nm for nm in names if 'gbXBin' in graph[nm]) == ['gbBinInfo'], 'gbXBin callers')
check(sorted(nm for nm in names if 'gbPsLim' in graph[nm]) == ['gbPoisson'], 'gbPsLim callers')
check(code.count('CAS(') == 0 and src.count('EXPR("CAS(" + CHAR(34) + "string(" + gbS + ")" + CHAR(34) + ")")') == 1,
      '3a: one CAS call site, the EXPR form, and no CAS( on a variable')
check(':=' not in ''.join(re.findall(r'gbCas\(([^;]*)\);', code)), '3a: no CAS text assigns a CAS variable')
for f in ('gbPour', 'gbDropAnim', 'gbBallStep', 'gbLattice', 'gbPress', 'gbDropFast', 'gbBigDrop', 'gbScene',
          'gbFrame', 'gbLand', 'gbCol', 'gbBar', 'gbTheory', 'gbRefresh', 'gbPsDraw', 'gbPsCalc', 'gbHelp'):
    check('gbCas' not in reach(f), '%s can reach gbCas' % f)
say('  gbCas <- %s; gbXBin <- gbBinInfo (a tap on a bar); gbPsLim <- gbPoisson (a new k);'
    ' no animation, drag or frame routine reaches it' % callers)


def body(txt, name):
    m = re.search(r'(?m)^' + re.escape(name) + r'\([^\n]*\)\nBEGIN\n.*?^END;', txt, re.S)
    return m.group(0) if m else None


py3 = re.search(r'(?s)#PYTHON gbPyDrop.*?#END', src).group(0)
py2 = re.search(r'(?s)#PYTHON gbPyDrop.*?#END', old).group(0)
check(py3 == py2, 'the #PYTHON block differs from beta 2')
same = []
for f in ('gbPour', 'gbBigDrop', 'gbDropFast', 'gbBallStep', 'gbDropAnim', 'gbNewBall', 'gbPress',
          'gbTheory', 'gbLattice', 'gbLand', 'gbCol', 'gbFrame', 'gbDrain', 'gbWaitAny'):
    if check(body(src, f) is not None and body(src, f) == body(old, f), '%s differs from beta 2' % f):
        same.append(f)
say('  byte-identical to beta 2: the #PYTHON block (Drop 100,000), ' + ', '.join(same))
# 3b: gbScene changed on purpose -- the pegs only (three ARC_P/PIXON_P lines -> two RECT_P lines)
_nc = lambda t: re.sub(r'[ \t]*//[^\n]*', '', t)
_sc_old = _nc(body(old, 'gbScene')).replace('''      ARC_P(G3, scX, scY, 2, gbGRAY);
      ARC_P(G3, scX, scY, 1, gbGRAY);
      PIXON_P(G3, scX, scY, gbGRAY);''', '''      RECT_P(G3, scX - 2, scY - 1, scX + 2, scY + 1, gbGRAY, gbGRAY);
      RECT_P(G3, scX - 1, scY - 2, scX + 1, scY + 2, gbGRAY, gbGRAY);''')
check(re.sub(r'\n\s*\n', '\n', _sc_old) == re.sub(r'\n\s*\n', '\n', _nc(body(src, 'gbScene'))),
      '3b: gbScene differs from beta 2 in the peg lines only')

# ================================================================ F
say('\nF. layout')
hh = H('giac', 10)
for (R, p, k) in ((8, 0.5, 4), (12, 0.37, 5), (3, 0.05, 0), (12, 0.95, 12), (8, 0.3333, 2)):
    board(hh, R, p); hh.call('gbScene'); hh.press('Esc'); hh.reset_records(); hh.call('gbBinInfo', float(k))
    pg = hh.pages[-1]
    panel = [t for t in pg.texts if t.grob == 'G1' and 14 <= t.y <= 127]
    check(all(t.y + 11 <= 127 for t in panel if t.font == 1), 'panel text below its frame (R %d)' % R)
    check(all(t.x + min(t.est_width, t.width or 999) <= 313 for t in panel), 'panel text past x 313 (R %d k %d)' % (R, k))
for (R, p) in BOARDS:
    board(hh, R, p)
    hh.press('Esc'); hh.reset_records(); hh.call('gbPoisson')
    for q in hh.pages:
        for t in q.texts:
            if t.grob != 'G1':
                continue
            check(t.y <= 224 and t.x >= 0, 'Poisson text off the page: %s' % t.text)
            check(t.x + min(t.est_width, t.width or 999) <= 318, 'Poisson text past x 318: "%s" (%d px)' % (t.text, t.est_width))
say('  the bar panel (5 boards) and the Poisson page (7 boards): every line inside its frame')

# ================================================================ G (3a)
say('\nG. beta 3 in harness v3c (its CAS finding stays), and beta 3b against beta 3a')
h3 = Harness(BETA3, cas='giac', seed=1)
h3.call('gbInit'); board(h3, 8, 0.5)
t3 = h3.call('gbXBin', 4.0)
check(t3 == '' and any('non-literal' in w for w in h3.warnings),
      'beta 3 in v3b: gbCas hands back its own text, so 35/128 never shows (got %r)' % t3)
h3.call('gbPsCalc')
check(h3.call('gbPsLim', 3.0) == '', 'beta 3 in v3b: no Poisson limit either')
say('  beta 3 in v3b: gbXBin(4) = %r, gbPsLim(3) = %r: the emulator\'s finding, reproduced' % (t3, ''))
b3 = open(BETA3, encoding='utf-8').read()


def bodies_of(txt):
    c = re.sub(r'(?s)#PYTHON.*?#END', '', txt)
    c = re.sub(r'//[^\n]*', '', c)
    out = {}
    for m in re.finditer(r'(?m)^(?:EXPORT\s+)?([A-Za-z]\w*)\(([^()]*)\)\s*\nBEGIN\n.*?^END;', c, re.S):
        out[m.group(1)] = re.sub(r'[ \t]+\n', '\n', m.group(0))
    return out


b3 = open(B3A, encoding='utf-8').read()          # 3b: compared with beta 3a now
B3, B3a = bodies_of(b3), bodies_of(src)
diff = sorted(n for n in set(B3) | set(B3a) if B3.get(n) != B3a.get(n))
check(diff == ['gbBar', 'gbDisc', 'gbLblTop', 'gbScene'], '3b: routines that differ from beta 3a: %s' % diff)
check('gbLblTop' not in B3, '3b: gbLblTop is new')
nc = lambda t: re.sub(r'(?s)#PYTHON.*?#END', '', re.sub(r'//[^\n]*', '', t))
outside = lambda t, names: re.sub(r'(?ms)^(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', nc(t))
check(re.sub(r'\s+', ' ', outside(b3, diff)) == re.sub(r'\s+', ' ', outside(src, diff)),
      '3b: outside those routines, only comments differ')
say('  routines that differ from beta 3a: %s; everything else differs only in comments' % ', '.join(diff))


# ================================================================ P (3b)
say('\nP. 3b: solid pegs and balls (GfxProbe T09: ARC_P rings leave diagonal holes)')


def rect_px(a):
    x1, y1, x2, y2 = [int(v) for v in a[:4]]
    return {(x, y) for x in range(min(x1, x2), max(x1, x2) + 1) for y in range(min(y1, y2), max(y1, y2) + 1)}


def disc(cx, cy, r):
    return {(cx + dx, cy + dy) for dx in range(-r, r + 1) for dy in range(-r, r + 1) if dx * dx + dy * dy <= (r + 0.5) ** 2}


hp = H('giac', 3)
GRAY, RED = hp.globals_['gbGRAY'], hp.globals_['gbRED']
for R in (3, 8, 12):
    board(hp, R, 0.5); hp.reset_records(); hp.call('gbScene')
    items = hp.grobs['G3'].items
    arcs = [it for it in items if getattr(it, 'cmd', '') in ('ARC_P', 'PIXON_P') and it.args[-1] == GRAY]
    grey = [it for it in items if getattr(it, 'cmd', '') == 'RECT_P' and it.args[4:6] == [GRAY, GRAY]]
    dy = math.floor((hp.globals_['gbPegBot'] - hp.globals_['gbTop']) / R)
    bad = 0
    for r in range(1, R + 1):
        y = hp.globals_['gbTop'] + r * dy
        for k in range(r):
            x = hp.globals_['gbMidX'] + int((k - (r - 1) / 2) * hp.globals_['gbBw'] + 0.5)   # IP truncates, as PPL
            px = set()
            for it in grey:
                if abs((it.args[0] + it.args[2]) / 2 - x) < 0.6 and abs((it.args[1] + it.args[3]) / 2 - y) < 0.6:
                    px |= rect_px(it.args)
            if px != disc(int(x), int(y), 2):
                bad += 1
    check(not arcs, '3b R %d: no ARC_P or grey PIXON_P in the scene (%d)' % (R, len(arcs)))
    check(len(grey) == R * (R + 1) and bad == 0,
          '3b R %d: %d pegs, each two grey RECT_P covering exactly a radius-2 disc (%d grey rects, %d wrong)'
          % (R, R * (R + 1) // 2, len(grey), bad))
say('  pegs: R 3, 8, 12 -- every peg is two grey RECT_P bars = exactly the pixels of a radius-2 disc')
# one ball, straight from gbDisc
hp.reset_records()
hp.call('gbDisc', hp.grobs['G1'], 100.0, 100.0, RED)
rs = [x[1] for x in hp.log if x[0] == 'RECT_P']
px = set()
for a in rs:
    px |= rect_px(a[1:])
check(len(hp.log) == 3 and px == disc(100, 100, 3) and all(a[5:7] == [RED, RED] for a in rs),
      '3b: gbDisc = three red RECT_P, exactly the pixels of a radius-3 disc (7 px across)')
say('  a ball: three red RECT_P = exactly a radius-3 disc (%d pixels), no ARC_P' % len(px))


def frames(hh):
    """drawing calls between consecutive blits to the screen, per frame"""
    out, n = [], 0
    for c in hh.log:
        if c[0] == 'BLIT_P' and c[1] and getattr(c[1][0], 'name', '') == 'G0':
            out.append(n); n = 0
        elif c[0] in ('RECT_P', 'LINE_P', 'ARC_P', 'PIXON_P', 'TEXTOUT_P', 'FILLPOLY_P'):
            n += 1
    return out


def run_anim(path, script, seed=11):
    hh = Harness(path, cas='fail', seed=seed)
    hh.press('Enter')
    script(hh)
    hh.press('Esc')
    hh.call('GaltonBoard')
    return hh


for nm, script in (('one drop (Drop soft key)', lambda h: h.tap(26, 230)),
                   ('x10 (up to 8 balls in the air)', lambda h: h.tap(80, 230)),
                   ('pour (hold the funnel)', lambda h: h.tap(160, 18, hold=300))):
    ha, hb = run_anim(B3A, script), run_anim(SRC, script)
    fa, fb = frames(ha), frames(hb)
    arcs_b = sum(1 for c in hb.log if c[0] == 'ARC_P')
    arcs_a = sum(1 for c in ha.log if c[0] == 'ARC_P')
    check(len(fa) == len(fb) and all(b <= a for a, b in zip(fa, fb)) and sum(fb) < sum(fa) and arcs_b == 0,
          '3b %s: no ARC_P, and no frame draws more than in beta 3a (%d frames)' % (nm, len(fb)))
    say('  %s: %d frames, %d drawing calls in all (beta 3a: %d, %d of them ARC_P); the busiest frame %d (3a %d)'
        % (nm, len(fb), sum(fb), sum(fa), arcs_a, max(fb), max(fa)))
hs = H('fail', 3)
for R in (8, 12):
    board(hs, R, 0.5); hs.reset_records(); hs.call('gbScene'); nb = len(hs.log)
    ha = Harness(B3A, cas='fail', seed=3); ha.call('gbInit'); board(ha, R, 0.5); ha.reset_records(); ha.call('gbScene')
    check(nb == len(ha.log) - R * (R + 1) // 2,
          '3b R %d: the scene makes one call fewer per peg (%d against %d)' % (R, nb, len(ha.log)))
    say('  scene R %d: %d drawing calls (beta 3a: %d)' % (R, nb, len(ha.log)))

# ================================================================ L (3b)
say('\nL. 3b: the bin counts clear of the overlays (the emulator: a "9" half hidden)')


def label_hits(hh):
    """count labels drawn ABOVE their bars that touch a magenta square/line or the green curve"""
    g = hh.grobs['G3']
    MAG, GRN = hh.globals_['gbMAG'], hh.globals_['gbNCol']
    labels = [t for t in g.items if hasattr(t, 'text') and t.func == 'gbBar']
    shapes = [it for it in g.items if hasattr(it, 'cmd')]
    sq = [it.args for it in shapes if it.cmd == 'RECT_P' and it.args[4] == MAG]
    ln = [it.args for it in shapes if it.cmd == 'LINE_P' and it.args[4] in (MAG, GRN)]
    hits, above = [], 0
    for t in labels:
        # the program's own width rule: 3 px a character either side of the bin's centre
        x1, x2, y1, y2 = t.x, t.x + 6 * len(t.text) - 1, t.y, t.y + 9
        bar = [it.args for it in shapes if it.cmd == 'RECT_P' and it.args[0] <= t.x + 3 * len(t.text) <= it.args[2]
               and it.args[3] == hh.globals_['gbHB'] - 1]
        if bar and t.y >= bar[0][1]:
            continue                                   # inside the bar (no room above): not this check
        above += 1
        hit = any(not (a[2] < x1 or a[0] > x2 or a[3] < y1 or a[1] > y2) for a in sq)
        for a in ln:
            for i in range(41):
                u = i / 40.0
                x, y = a[0] + u * (a[2] - a[0]), a[1] + u * (a[3] - a[1])
                if x1 <= x <= x2 and y1 <= y <= y2:
                    hit = True
        if hit:
            hits.append((t.text, t.x, t.y))
    return hits, above


STATES = [(8, 0.5, 1, 110), (8, 0.5, 2, 110), (8, 0.5, 1, 40), (8, 0.5, 2, 400), (6, 0.3, 1, 50), (6, 0.3, 2, 50),
          (9, 0.5, 1, 500), (9, 0.5, 2, 90), (8, 0.72, 1, 30), (5, 0.5, 2, 20), (3, 0.5, 1, 6), (7, 0.4, 2, 1000),
          (4, 0.6, 1, 12), (9, 0.35, 2, 33)]
tot_b = tot_a = n_above = 0
worst_a = []
for (R, p, ov, n) in STATES:
    for seed in (1, 2, 3):
        res = []
        for path in (SRC, B3A):
            hh = Harness(path, cas='fail', seed=seed)
            hh.call('gbInit'); board(hh, R, p); hh.globals_['gbOvl'] = float(ov)
            hh.call('gbDropFast', float(n)); hh.reset_records(); hh.call('gbScene')
            res.append(label_hits(hh))
        (hb_, ab), (ha_, aa) = res
        tot_b += len(hb_); tot_a += len(ha_); n_above += ab
        if ha_:
            worst_a.append(((R, p, ov, n, seed), ha_[:2]))
        if hb_:
            say('  3b collision: R %d p %.2f overlays %d n %d seed %d: %s' % (R, p, ov, n, seed, hb_))
check(tot_b == 0, '3b: %d count labels above their bars in %d boards: none touches a magenta square, a magenta '
      'line or the green curve (%d collisions)' % (n_above, len(STATES) * 3, tot_b))
check(tot_a > 0, '3b: beta 3a in the same boards: %d labels collide (the emulator\'s finding), e.g. %s'
      % (tot_a, worst_a[:1]))
say('  %d labels above their bars, 0 collisions (beta 3a in the same %d boards: %d collisions, e.g. %s)'
    % (n_above, len(STATES) * 3, tot_a, worst_a[:1]))
# the label still never rises into the pegs: y >= 127 (else it goes inside the bar, as before)
hh = Harness(SRC, cas='fail', seed=4); hh.call('gbInit'); board(hh, 8, 0.5); hh.globals_['gbOvl'] = 2.0
hh.call('gbDropFast', 2000.0); hh.reset_records(); hh.call('gbScene')
lab = [t for t in hh.grobs['G3'].items if hasattr(t, 'text') and t.func == 'gbBar']
check(lab and all(t.y >= 127 for t in lab), '3b: no count label above y 127, where the pegs end')
say('  2000 balls, R 8, overlays 2: every label at y >= 127 (%s)' % sorted({int(t.y) for t in lab}))

say('\n%d checks passed, %d failed' % (NPASS[0], len(FAILS)))
if FAILS:
    say('FAILURES:\n  ' + '\n  '.join(FAILS[:40]))
    sys.exit(1)
say('ALL OK')
