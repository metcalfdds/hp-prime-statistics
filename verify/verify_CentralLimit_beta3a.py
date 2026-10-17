#!/usr/bin/env python3
"""verify_CentralLimit_beta3a.py -- checks for CentralLimit beta 3a (17 Oct 2026): the CAS call form
CASProbe beta 1b found on the emulator.  Built from verify_CentralLimit_beta3.py: every check is
kept; part 2 also reads the MGF limit in the Prime's printing and re-feeds it as the program does;
part 3 runs in harness v3b, which models the calculator's CAS; part 4 (new) runs beta 3 itself in
v3b and compares beta 3a with beta 3.  New or changed checks are marked "3a".

Part 1, the numbers the program DRAWS (no harness):
  * cltIH, the Irwin-Hall density by the closed form with the symmetry trick, replayed
    in IEEE double and in 12-digit decimal arithmetic (the Prime's Home reals), against
    exact rationals (fractions), scipy.stats.irwinhall and a numerical convolution, for
    n = 1..12 and every square n to 100: this fixes the n limit (49) of the exact curve;
  * the same without the symmetry, and the CAS's expanded polynomial evaluated in 12
    digits (why the program does not draw from the CAS's coefficients);
  * exact curve against the normal curve, in pixels on the 59-px panel (the "within
    0.2 px above n = 49" claim);
  * the rescaled curve (a flat population with the population's mu and sigma):
    integral 1, mean mu, SD sigma/sqrt n.
Part 2, every CAS template the program can build, through desktop Giac (icas) and
  against SymPy / fractions: the polynomial pieces, the exact peak, the round(...)
  check numbers, the MGF limit and series; with timings.
Part 3, the program end to end in ppl_run_v3 with cas='giac' and cas='fail': the
  exact-curve page for n = 1 ... 100 (and for a non-uniform population), the MGF page,
  the dashboard's dots (against SciPy), the legend, the cache, no CAS call in any frame,
  drag or animation, Help, the menu.
The program file is only read.  Run:  python3 verify_CentralLimit_beta3.py
"""
import math
import os
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

import numpy as np
import sympy as sp
from scipy import stats

sys.path.insert(0, '/home/claude/work/harness')
import ppl_run_v3b as R  # noqa: E402
from ppl_run_v3b import Harness, prime_print  # noqa: E402

PROG = os.environ.get('CLT_BETA3A', '/home/claude/work/out/CentralLimit_beta3a.txt')
BETA3 = '/home/claude/work/out/CentralLimit_beta3.txt'
SQUARES = [k * k for k in range(1, 11)]
FAILS = []


def say(*a):
    print(' '.join(str(x) for x in a))


def check(label, ok, extra=''):
    say('  [%s] %s%s' % ('ok' if ok else 'FAIL', label, (' -- ' + extra) if extra else ''))
    if not ok:
        FAILS.append(label)


# ---------------------------------------------------------------- the program's sum
def ih_exact(n, s):
    s = Fraction(s)
    if s <= 0 or s >= n:
        return Fraction(0)
    if n == 1:
        return Fraction(1)
    tot = Fraction(0)
    for k in range(0, math.floor(s) + 1):
        tot += (-1) ** k * math.comb(n, k) * (s - k) ** (n - 1)
    return tot / math.factorial(n - 1)


def ih_ppl(n, s, num=float, sym=True):
    """cltIH line by line, in the arithmetic `num` (float, or 12-digit Decimal)."""
    s = num(s)
    if s <= 0 or s >= n:
        return num(0)
    if n == 1:
        return num(1)
    v = s
    if sym and v > num(n) / 2:
        v = num(n) - v
    f = num(1)
    for k in range(2, n):
        f = f * k
    t, c, sg, k = num(0), num(1), 1, 0
    while k <= v:
        t = t + sg * c * (v - k) ** (n - 1)
        c = c * (n - k) / (k + 1)
        sg = -sg
        k += 1
    return t / f


def D12(x):
    getcontext().prec = 12
    return Decimal(repr(x)) if isinstance(x, float) else Decimal(x)


def conv_density(n, h=1 / 2000.0):
    """the density of the sum of n uniforms by numerical convolution on a grid"""
    one = np.ones(int(round(1 / h)))
    f = one.copy()
    for _ in range(n - 1):
        f = np.convolve(f, one) * h
    xs = (np.arange(len(f)) + 0.5) * h
    return xs, f


def part1():
    say('== Part 1: the exact curve the program draws (cltIH) ==')
    say('  n   12-digit, symmetric   12-digit, no symmetry   double   vs scipy irwinhall   vs convolution  (max |error| / peak)')
    limit_ok = True
    for n in list(range(1, 13)) + [16, 25, 36, 49, 64, 81, 100]:
        sd = math.sqrt(n / 12)
        pts = [Fraction(n, 2) + Fraction(j, 40) * Fraction(int(sd * 10000), 10000) for j in range(-180, 181)]
        pts = [p for p in pts if 0 < p < n]
        peak = float(ih_exact(n, Fraction(n, 2)))
        e12 = ens = edb = esc = 0.0
        for p in pts:
            ex = float(ih_exact(n, p))
            e12 = max(e12, abs(float(ih_ppl(n, D12(float(p)), num=D12)) - ex) / peak)
            ens = max(ens, abs(float(ih_ppl(n, D12(float(p)), num=D12, sym=False)) - ex) / peak)
            edb = max(edb, abs(ih_ppl(n, float(p)) - ex) / peak)
            esc = max(esc, abs(stats.irwinhall.pdf(float(p), n) - ex) / peak)
        econv = float('nan')
        if n <= 12:
            xs, f = conv_density(n)
            sel = np.linspace(0, len(xs) - 1, 400).astype(int)
            econv = max(abs(f[i] - float(ih_exact(n, Fraction(xs[i])))) for i in sel) / peak
        say(' %3d    %9.1e            %9.1e            %8.1e        %8.1e           %8.1e' % (n, e12, ens, edb, esc, econv))
        if n <= 49 and e12 > 5e-4:
            limit_ok = False
        if n == 64 and e12 < 0.01:
            limit_ok = False
    say('  At the peak s = n/2, the 12-digit sum agrees with the exact value to: ' + ', '.join(
        'n=%d %s' % (n, ('%.1f digits' % -math.log10(abs(float(ih_ppl(n, D12(n / 2), num=D12)) - float(ih_exact(n, Fraction(n, 2)))) / float(ih_exact(n, Fraction(n, 2)))))
                     if float(ih_ppl(n, D12(n / 2), num=D12)) != float(ih_exact(n, Fraction(n, 2))) else 'all') for n in (4, 9, 16, 25, 36, 49, 64)))
    check('the device keeps >= 3 digits at the peak up to n = 49 (the page accepts 1E-3)', abs(float(ih_ppl(49, D12(24.5), num=D12)) / float(ih_exact(49, Fraction(49, 2))) - 1) < 1e-3)
    check('12-digit symmetric sum: error < 5E-4 of the peak (0.03 px) up to n = 49, and > 1 % at n = 64 (the n limit is 49)', limit_ok)
    # the CAS's expanded polynomial, evaluated in 12 digits (Horner), for comparison
    say('  The CAS polynomial (whole-number coefficients / (n-1)!) evaluated in 12-digit Horner:')
    for n in (4, 9, 16, 25, 36):
        s = sp.Symbol('s')
        peak = float(ih_exact(n, Fraction(n, 2)))
        worst = 0.0
        for j in range(n):
            poly = sp.Poly(sp.expand(sum((-1) ** k * sp.binomial(n, k) * (s - k) ** (n - 1) for k in range(j + 1))), s)
            co = [D12(int(c)) for c in poly.all_coeffs()]
            fac = D12(math.factorial(n - 1))
            for q in range(1, 10):
                x = j + q / 10.0
                acc = D12(0)
                for c in co:
                    acc = acc * D12(x) + c
                worst = max(worst, abs(float(acc / fac) - float(ih_exact(n, Fraction(x)))) / peak)
        say('    n = %2d: max |error| / peak = %.1e' % (n, worst))
    say('    (the symmetric sum is better at every n: the program draws from the sum, and the CAS polynomial is shown as text)')
    # exact vs normal, in pixels
    say('  Exact curve against the normal curve N(n/2, n/12), in pixels on the 59-px panel:')
    gaps = {}
    for n in SQUARES:
        sd = math.sqrt(n / 12)
        nm_peak = 1 / (sd * math.sqrt(2 * math.pi))
        xs = np.linspace(max(0.0, n / 2 - 5 * sd), min(float(n), n / 2 + 5 * sd), 801)
        diff = max(abs(stats.irwinhall.pdf(x, n) - stats.norm.pdf(x, n / 2, sd)) for x in xs)
        gaps[n] = 59 * diff / nm_peak
        say('    n = %3d: max gap %.3f px; exact peak / normal peak = %.4f' % (n, gaps[n], float(ih_exact(n, Fraction(n, 2))) / nm_peak))
    check('above n = 49 the exact and normal curves are within 0.2 px', all(gaps[n] < 0.2 for n in (64, 81, 100)),
          '%.3f, %.3f, %.3f px' % (gaps[64], gaps[81], gaps[100]))
    # the rescaled curve: a flat population with this mu and sigma
    mu, sg = 4.87, 2.93
    w = 2 * math.sqrt(3) * sg
    a = mu - w / 2
    for n in (1, 4, 16, 49):
        xs = np.linspace(a, a + w, 20001)
        dens = np.array([n / w * ih_ppl(n, n * (x - a) / w) for x in xs])
        integ = np.trapezoid(dens, xs)
        m1 = np.trapezoid(xs * dens, xs)
        sdm = math.sqrt(np.trapezoid((xs - m1) ** 2 * dens, xs))
        check('rescaled n = %d: integral %.5f, mean %.5f (mu %.2f), SD %.5f (sigma/sqrt n %.5f)'
              % (n, integ, m1, mu, sdm, sg / math.sqrt(n)),
              abs(integ - 1) < 2e-3 and abs(m1 - mu) < 1e-3 and abs(sdm - sg / math.sqrt(n)) < 2e-3)


# ---------------------------------------------------------------- part 2: Giac
def giac(expr):
    t0 = time.time()
    out = R.giac_eval(expr)
    return out, 1000 * (time.time() - t0)


def part2():
    say('')
    say('== Part 2: every CAS template, desktop Giac (icas) against SymPy / fractions ==')
    s, k, t, nn, u = sp.symbols('cltqs cltqk cltqt cltqn cltqu')
    slow = 0.0
    piece_bad = peak_bad = chk_bad = 0
    count = 0
    for n in list(range(1, 13)) + [16, 25, 36, 49, 64, 81, 100]:
        js = range(n) if n <= 12 else [0, n // 2]
        for j in js:
            expr = ('expand(sum(seq((-1)^cltqk*comb(%d,cltqk)*(cltqs-cltqk)^(%d),cltqk,0,%d)))' % (n, n - 1, j))
            out, ms = giac(expr)
            slow = max(slow, ms)
            mine = sp.expand(sum((-1) ** q * sp.binomial(n, q) * (s - q) ** (n - 1) for q in range(j + 1)))
            if sp.expand(sp.sympify(out.replace('^', '**'), locals={'cltqs': s}) - mine) != 0:
                piece_bad += 1
            # the check the page makes: the piece at the middle of its interval
            sub = 'round(evalf(subst(%s,cltqs,%d/2))*10^(%d))' % (out, 2 * j + 1, 6)
            o2, ms2 = giac(sub)
            want = ih_exact(n, Fraction(2 * j + 1, 2)) * math.factorial(n - 1) * 10 ** 6
            if n <= 25 and abs(int(o2) - want) > max(2, abs(want) * 1e-9):
                chk_bad += 1
            count += 1
        expr = ('sum(seq((-1)^cltqk*comb(%d,cltqk)*(%d/2-cltqk)^(%d),cltqk,0,%d))/(%d)!'
                % (n, n, n - 1, n // 2, n - 1))
        out, ms = giac(expr)
        slow = max(slow, ms)
        if Fraction(out) != ih_exact(n, Fraction(n, 2)):
            peak_bad += 1
        o2, _ = giac('round(evalf(%s)*10^(12))' % out)
        want = round(float(ih_exact(n, Fraction(n, 2))) * 1e12)
        if abs(int(o2) - want) > 2:
            chk_bad += 1
        if n in (1, 4, 9, 16, 49, 100):
            say('  n = %3d: peak %s (%d chars) = %.12f; round(...*10^12) = %s' %
                (n, out if len(out) < 40 else out[:16] + '...', len(out), float(Fraction(out)), o2))
    check('%d polynomial pieces: Giac expand == SymPy expand of the same sum' % count, piece_bad == 0, '%d differ' % piece_bad)
    check('19 exact peaks: Giac == fractions', peak_bad == 0, '%d differ' % peak_bad)
    check('the round(evalf(..)*10^E) check numbers equal the exact values', chk_bad == 0, '%d differ' % chk_bad)
    check('every template under 1 s in desktop Giac', slow < 1000, 'slowest %.0f ms' % slow)
    # the MGF templates
    out, ms = giac('limit(cosh(cltqt/sqrt(cltqn))^cltqn,cltqn,inf)')
    sym = sp.limit(sp.cosh(t / sp.sqrt(nn)) ** nn, nn, sp.oo)
    check('MGF limit: Giac %s == SymPy %s' % (out, sym), sp.simplify(sp.sympify(out.replace('^', '**'),
          locals={'cltqt': t}) - sym) == 0, '%.0f ms' % ms)
    out, ms = giac('expand(cltqn*subst(convert(series(ln(cosh(cltqu)),cltqu,0,5),polynom),cltqu,cltqt/sqrt(cltqn)))')
    ser = sp.expand(nn * sp.series(sp.log(sp.cosh(u)), u, 0, 6).removeO().subs(u, t / sp.sqrt(nn)))
    check('MGF series: Giac %s == SymPy %s' % (out, ser), sp.simplify(sp.sympify(out.replace('^', '**'),
          locals={'cltqt': t, 'cltqn': nn}) - ser) == 0, '%.0f ms' % ms)
    o2, _ = giac('round(evalf(subst(exp(cltqt^2/2),cltqt,1))*10^(9))')
    check('MGF check number at t = 1: %s = round(e^(1/2) 10^9) = %d' % (o2, round(math.exp(0.5) * 1e9)),
          int(o2) == round(math.exp(0.5) * 1e9))
    # 3a: the limit as the Prime prints it (CASProbe beta 1b T17: e^(cxt^2/2)), re-fed as the page does
    lim, _ = giac('limit(cosh(cltqt/sqrt(cltqn))^cltqn,cltqn,inf)')
    pl = prime_print(lim)
    o3, _ = giac('round(evalf(subst(%s,cltqt,1))*10^(9))' % pl)
    check('3a: the MGF limit in the Prime\'s printing is %s (as CASProbe T17 saw), and re-fed it gives %s'
          % (pl, o3), pl == 'e^(cltqt^2/2)' and int(o3) == round(math.exp(0.5) * 1e9))
    say('  numeric: cosh(t/sqrt n)^n -> e^(t^2/2) at t = 2: ' + ', '.join(
        'n=%d %.4f' % (m, math.cosh(2 / math.sqrt(m)) ** m) for m in (1, 4, 16, 100, 10000)) + ', e^2 = %.4f' % math.exp(2))


# ---------------------------------------------------------------- part 3: harness
def new(mode, pop='uniform', seed=7):
    h = Harness(PROG, strict=True, seed=seed, stall_limit=20000, cas=mode)
    if pop == 'uniform':
        h.choose(1).answer({'cpA': 0, 'cpB': 10, 'cpN': 500})
    else:
        h.choose(3).answer({'cpA': 5, 'cpN': 500})
    h.call('cltChoosePop')
    return h


def page_lines(h):
    pgs = [p for p in h.pages if not p.has('Asking the CAS')]
    return [t for p in pgs for t in p.texts]


def layout(h, label):
    bad = 0
    for pg in h.pages:
        for tx in pg.texts:
            w = (6 if tx.font == 1 else 8) * len(tx.text)
            if tx.x < 0 or tx.x + w > 321:
                bad += 1
                say('    [%s] wide: %r at x=%s (%d px)' % (label, tx.text, tx.x, w))
    return bad


def part3():
    say('')
    say('== Part 3: the program in ppl_run_v3b (cas = giac, then cas = fail) ==')
    wide = 0
    for mode in ('giac', 'fail'):
        say('-- cas = %s --' % mode)
        h = new(mode)
        for k in range(1, 11):
            h.globals_['cltK'] = float(k)
            h.reset_records()
            n0 = len(h.cas_calls)
            h.press('Enter', 'Enter')
            h.call('cltExact')
            tx = page_lines(h)
            texts = [x.text for x in tx]
            badge = [x.text for x in tx if x.y == 226 and x.x > 200]
            ex = [x for x in texts if x.strip().startswith('exact:')]
            ag = [x for x in texts if 'agrees to' in x]
            ncas = len(h.cas_calls) - n0
            ms = sum(c[2] for c in h.cas_calls[n0:])
            n = k * k
            say('  exact page n = %3d: %2d lines, %d CAS calls (%4.0f ms), badge %s; %s; %s' %
                (n, len(texts), ncas, ms, badge, ex[0].strip() if ex else 'no exact peak',
                 ag[0].strip() if ag else ''))
            wide += layout(h, 'exact n=%d' % n)
            if mode == 'giac':
                check('n = %d: badge "exact (CAS)" and the exact peak shown' % n, badge == ['exact (CAS)'] and bool(ex))
                if n <= 9:
                    want = ih_exact(n, Fraction(n, 2))
                    check('n = %d: the peak on the page is %s' % (n, want),
                          any((str(want.numerator) + '/' + str(want.denominator)) in x or (want == 1 and 'exact: 1 ' in x)
                              for x in texts))
            else:
                check('n = %d, CAS failing: "decimal" badge, "no closed form shown", no error' % n,
                      badge == ['decimal'] and any('no closed form shown' in x for x in texts))
            # the page is kept: a second opening asks the CAS nothing
            n1 = len(h.cas_calls)
            h.press('Enter', 'Enter')
            h.call('cltExact')
            if mode == 'giac' and k in (2, 3):
                check('n = %d: the page is kept (a second opening makes %d CAS calls)' % (n, len(h.cas_calls) - n1),
                      len(h.cas_calls) == n1)
        # the pieces for n = 4, line by line
        h.globals_['cltK'] = 2.0
        h.globals_['cltExPgN'] = 0.0
        h.reset_records()
        h.press('Enter', 'Enter')
        h.call('cltExact')
        say('  n = 4 page:')
        for x in page_lines(h):
            if 26 <= x.y < 220:
                say('     ' + x.text)
        # a population that is not uniform
        h2 = new(mode, pop='expo')
        h2.globals_['cltK'] = 3.0
        h2.reset_records()
        h2.press('Enter', 'Enter')
        h2.call('cltExact')
        t2 = [x.text for x in page_lines(h2)]
        check('Exponential population: the page says no exact curve is drawn for it',
              any('no exact' in x for x in t2), t2[1] if len(t2) > 1 else '')
        # the MGF page
        h.reset_records()
        n0 = len(h.cas_calls)
        h.press('Enter')
        h.call('cltMgf')
        pg = h.pages[-1]
        cols = {}
        for sh in pg.shapes:
            if sh.cmd == 'LINE_P' and 110 <= sh.args[1] <= 206 and sh.args[0] >= 33:
                cols[sh.args[4]] = cols.get(sh.args[4], 0) + 1
        say('  MGF page: %d CAS calls; lines: %s' % (len(h.cas_calls) - n0,
            [x.text for x in pg.texts if 24 <= x.y < 108]))
        say('    curve segments by colour: %s' % {('#%06X' % int(c)): v for c, v in cols.items()})
        badge = [x.text for x in pg.texts if x.y == 226 and x.x > 200]
        if mode == 'giac':
            check('MGF page: the CAS limit e^(t^2/2) (3a: the Prime\'s printing, no "exp(") and the series shown, '
                  'badge exact (CAS)',
                  pg.has('e^(t^2/2)') and not pg.has('exp(') and pg.has('t^4') and badge == ['exact (CAS)'])
            check('3a: every CAS text asks for string(...), every answer arrives quoted; no CAS variable assigned, '
                  'no CAS call of a variable',
                  all(c[0].startswith('string(') and c[1].startswith('"') for c in h.cas_calls)
                  and not h.cas_vars and not any('non-literal' in w for w in h.warnings))
        else:
            check('MGF page, CAS failing: the decimal M(1) line and the "decimal" badge',
                  pg.has('M(1) =') and badge == ['decimal'])
        # the plotted curves against Python
        seg = [sh for sh in pg.shapes if sh.cmd == 'LINE_P' and sh.args[4] == 0xC800C8 and sh.args[0] > 34]
        worst = 0
        for sh in seg[::25]:
            x1 = sh.args[2]
            tt = -2.5 + (x1 - 34) / 276 * 5
            m = math.cosh(tt / 4) ** 16
            y = 206 - int(min(m, 24) / 24 * 96 + 0.5)
            worst = max(worst, abs(y - sh.args[3]))
        check('MGF page: the n = 16 curve sits on cosh(t/4)^16 (to the pixel)', worst <= 1, 'worst %d px' % worst)
        wide += layout(h, 'mgf')
        # ---- the dashboard: dots, legend, cache, no CAS in frames ----
        h = new(mode, seed=3)
        n0 = len(h.cas_calls)
        for k in (1, 2, 4, 7, 8):
            h.globals_['cltK'] = float(k)
            h.reset_records()
            h.call('cltSample')
            h.call('cltDash', 0)
            pg = h.pages[-1]
            dots = [sh for sh in pg.shapes if sh.cmd == 'PIXON_P' and sh.args[2] == 0 and 94 <= sh.args[1] <= 167]
            leg = [x.text for x in pg.texts if x.y == 96 and x.x > 150]
            n = k * k
            # the cache against SciPy: the mean of n draws from U(mu - sqrt3 sigma, mu + sqrt3 sigma)
            mu, sg = h.globals_['cltMu'], h.globals_['cltSg']
            w = 2 * math.sqrt(3) * sg
            lo = mu - w / 2
            plo, span = h.globals_['cltPLo'], h.globals_['cltPNb'] * h.globals_['cltPW']
            exd = h.globals_['cltExD']
            worst = 0.0
            if n <= 49:
                pk = max(exd)
                for i in range(len(exd)):
                    x = plo + i / 300 * span
                    ref = n / w * stats.irwinhall.pdf(n * (x - lo) / w, n) if lo < x < lo + w else 0.0
                    if abs(x - mu) <= 5 * sg / math.sqrt(n):
                        worst = max(worst, abs(exd[i] - ref) / pk)
            say('  dashboard n = %3d: %3d black dots, legend %s, cache n = %g, max |cache - scipy| / peak %.1e'
                % (n, len(dots), leg, h.globals_['cltExN'], worst))
            if n <= 49:
                check('n = %d: dots drawn, legend "exact & N(...)", cache = SciPy (< 1E-7 of the peak; doubles here,'
                      ' the 12-digit errors are in part 1)' % n, len(dots) > 20 and leg[:1] == ['exact'] and worst < 1e-7)
            else:
                check('n = %d (> 49): no dots, the plain legend' % n, len(dots) == 0 and leg == ['curve = N(μ, σ/√n)'])
        check('no CAS call while sampling and drawing the dashboard (%d)' % (len(h.cas_calls) - n0),
              len(h.cas_calls) == n0)
        # the dots follow the cache: their rows against the panel scale
        h.globals_['cltK'] = 2.0
        h.call('cltSample')
        h.reset_records()
        h.call('cltDash', 0)
        pg = h.pages[-1]
        top = h.call('cltMScale', 2.0)
        sc = h.globals_['cltMade'] * h.globals_['cltMW']
        exd = h.globals_['cltExD']
        bad = 0
        for sh in pg.shapes:
            if sh.cmd == 'PIXON_P' and sh.args[2] == 0 and 94 <= sh.args[1] <= 167:
                i = int(sh.args[0] - 10)
                y = 166 - int(min(exd[i] * sc, top) / top * 59 + 0.5)
                if sh.args[1] not in (y, y - 1):
                    bad += 1
        check('the dots sit where the cache and the panel scale put them', bad == 0, '%d off' % bad)
        # a drag preview: no dots, no CAS
        n0 = len(h.cas_calls)
        h.reset_records()
        h.drag([(60, 50), (72, 50), (120, 52), (200, 55)])
        h.press('Esc')
        h.call('cltDashLoop')
        prev = [p for p in h.pages if p.has('the curve first')]
        pdots = sum(1 for p in prev for sh in p.shapes if sh.cmd == 'PIXON_P' and sh.args[2] == 0 and 94 <= sh.args[1] <= 167)
        check('drag preview: %d frames, no dots, no CAS call' % len(prev), prev and pdots == 0 and len(h.cas_calls) == n0)
        # the one-sample animation makes no CAS call either
        n0 = len(h.cas_calls)
        h.reset_records()
        h.call('cltOneSample', 1)
        check('one-sample animation: no CAS call', len(h.cas_calls) == n0)
        # a non-uniform population: no dots
        h3 = new(mode, pop='expo')
        h3.globals_['cltK'] = 2.0
        h3.call('cltSample')
        h3.reset_records()
        h3.call('cltDash', 0)
        pg = h3.pages[-1]
        d3 = [sh for sh in pg.shapes if sh.cmd == 'PIXON_P' and sh.args[2] == 0 and 94 <= sh.args[1] <= 167]
        check('Exponential population: no exact dots, plain legend', not d3 and pg.has('curve = N('))
        # the Curve toggle turns both off
        h.globals_['cltOver'] = 0.0
        h.reset_records()
        h.call('cltDash', 0)
        pg = h.pages[-1]
        d4 = [sh for sh in pg.shapes if sh.cmd == 'PIXON_P' and sh.args[2] == 0 and 94 <= sh.args[1] <= 167]
        check('curves off: no dots either', not d4)
        h.globals_['cltOver'] = 1.0
        wide += layout(h, 'dashboard')
    # Help and the menu
    h = new('giac')
    h.reset_records()
    h.press('Enter', 'Enter', 'Enter')
    h.call('cltHelp')
    say('  Help: %d pages: %s' % (len(h.pages), [p.texts[0].text for p in h.pages]))
    check('Help has three pages, the third on the exact curve and the MGF', len(h.pages) == 3 and
          h.pages[2].has('UNIFORM population only'))
    wide += layout(h, 'help')
    h.reset_records()
    h.choose(0)
    h.call('cltMenu')
    items = h.chooses[-1].items
    say('  Menu: %d items: %s' % (len(items), items))
    check('the menu has 12 items, the two CAS pages before Help', len(items) == 12 and
          items[8] == 'Exact curve (uniform)' and items[9] == 'Why the bell? (MGF)')
    check('View entries include the two CAS pages', 'cltVExact' in str(h.views) and 'cltVMgf' in str(h.views),
          str(h.views)[:120])
    check('layout: no text runs off the screen on any new page (6 / 8 px a character)', wide == 0, '%d' % wide)


# ---------------------------------------------------------------- part 4 (3a)
def part4():
    say('')
    say('== Part 4 (3a): beta 3 in harness v3b, and beta 3a against beta 3 ==')
    h = Harness(BETA3, strict=True, seed=7, stall_limit=20000, cas='giac')
    h.choose(1).answer({'cpA': 0, 'cpB': 10, 'cpN': 500})
    h.call('cltChoosePop')
    h.globals_['cltK'] = 3.0
    h.press('Enter', 'Enter')
    h.call('cltExact')
    tx = [x.text for p in h.pages for x in p.texts]
    h.press('Enter')
    h.call('cltMgf')
    tm = [x.text for x in h.pages[-1].texts]
    check('3a: beta 3 in v3b: its cltCas hands back its own text, so both pages say "no closed form shown" / the '
          'decimals -- the emulator\'s finding',
          any('no closed form shown' in x for x in tx) and any('M(1) =' in x for x in tm)
          and any('non-literal' in w for w in h.warnings))
    exec(G_CODE, dict(globals(), check=lambda ok, what: check(what, ok)))


G_CODE = "\n# ================================================================ G (round 2a)\nsay('\\nG. beta 3a: beta 3 in harness v3b, and beta 3a against beta 3')\nimport re as _re\n_b_old = open(BETA3, encoding='utf-8').read()\n_b_new = open(PROG, encoding='utf-8').read()\n\n\ndef _bodies(txt):\n    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)\n    c = _re.sub(r'//[^\\n]*', '', c)\n    out = {}\n    for m in _re.finditer(r'(?m)^(?:EXPORT\\s+|LOCAL\\s+)?([A-Za-z]\\w*)\\(([^()\\n]*)\\)\\s*\\nBEGIN\\n.*?^END;', c, _re.S):\n        out[m.group(1)] = _re.sub(r'[ \\t]+\\n', '\\n', m.group(0))\n    return out\n\n\n_B0, _B1 = _bodies(_b_old), _bodies(_b_new)\n_diff = sorted(n for n in set(_B0) | set(_B1) if _B0.get(n) != _B1.get(n))\ncheck(_diff == ['cltCas'], 'beta 3a: routines that differ from beta 3: %s (want cltCas)' % _diff)\n\n\ndef _outside(t, names):\n    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\\n]*', '', t))\n    if names:\n        c = _re.sub(r'(?ms)^(?:EXPORT\\s+|LOCAL\\s+)?(?:%s)\\([^\\n]*\\)\\s*\\nBEGIN\\n.*?^END;' % '|'.join(names), '', c)\n    return _re.sub(r'\\s+', ' ', c)\n\n\ncheck(_outside(_b_old, _diff) == _outside(_b_new, _diff), 'beta 3a: outside those routines only comments differ')\n_py0 = _re.findall(r'(?s)#PYTHON.*?#END', _b_old)\n_py1 = _re.findall(r'(?s)#PYTHON.*?#END', _b_new)\ncheck(_py0 == _py1, 'beta 3a: the #PYTHON blocks are unchanged')\nsay('  routines that differ from beta 3: %s; everything else differs only in comments' % ', '.join(_diff))\n"


if __name__ == '__main__':
    part1()
    part2()
    part3()
    part4()
    say('')
    say('RESULT: %s' % ('ALL PASS' if not FAILS else '%d FAILED: %s' % (len(FAILS), FAILS)))
