#!/usr/bin/env python3
"""verify_ScatterLab_beta2c.py -- ScatterLab beta 2c (19 Oct 2026): the fleet review's D-SL-1.
Built from verify_ScatterLab_beta2b.py; every check is kept and now runs in harness ppl_run_v3e (v3d's
results with home_minus off).  The older programs are read from /home/claude/work/out by absolute path; if
one is absent the script says which and stops before any check, instead of a FileNotFoundError half-way
(review item 22).
Changed old checks:
  R7  the INSTRING first arguments now include nmS (2c's new, guarded site in slNum) -- the old expected
      set was 2b's; the guard list gains slNum's DIM guard;
  G   the 2b-vs-2a record now reads the 2b file (out/ScatterLab_beta2b.txt), not this version.
New checks (part D, 2c), each on beta 2c AND on beta 2b to show the old version failing:
  D1  slNum on the review's values (check_ScatterLab.py section 4): 1.4E11 -> "140000000000" (2b "14"),
      1.23456789E11 -> "123456789000" (2b "123456789"), and the rest unchanged;
  D2  the decimal page for x = 100000, 200000, 300000 (sum x^2 = 1.4E11): "600000 a + 140000000000 b =
      1400000" (2b: "600000 a + 14 b = 1400000"), cas='fail', through the real page;
  D3  a property sweep of slNum over about 2,700 values from 1E-7 to 1E12, both signs: the text is the value
      to its decimals (never a digit lost), no trailing zero after a ".", no trailing "."; 2b fails it;
  D4  the review's own check_ScatterLab.py, its SRC pointed at each version: beta 2c 590 checks, 0
      failures; beta 2b the same 3 failures (the slNum ones);
  D5  n < 3 is still refused (D16 is open): two points give no line, no page, the note;
  G2c beta 2c against beta 2b: only slNum differs (plus the header), and only by the DIM and INSTRING
      guards around the zero strip; the file is pure ASCII; version strings.
(The beta 2b description follows; "v3d" there now means v3e.)

verify_ScatterLab_beta2b.py -- ScatterLab beta 2b (17 Oct 2026): the second emulator round's findings.
Built from verify_ScatterLab_beta2a.py; every check is kept and now runs in harness v3d, which raises
"Invalid input" for INSTRING("", ...) and prints STRING(x, 2, d) in scientific form when 0 < |x| < 10^-d,
as the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09) did on 17 Oct 2026.  New checks (part R):
  R1  slRepl directly: a pattern at the end, at the start, the whole text, an empty pattern, an empty
      text (beta 2a's slRepl stops whenever the text runs out, in v3d);
  R2  slCas, slCxClean and slCxSol on "" and on empty answers: no error;
  R3  Data > Poverty vs crime > tap the equation: the page opens with the CAS answering, b = 2441/2394,
      a = 3186173/191520, exact (CAS); beta 2a stops the same run with the INSTRING error -- the
      emulator's finding; the same through Menu > Least squares as calculus;
  R4  cas='fail' end to end: "decimal", no error; beta 2a fails the same run;
  R5  canned answers: an empty solve ({}), "sla=" with nothing after it, empty strings: no error;
  R6  six data sets built to give small numbers (r near 0, a loaded value finer than the grid, x values
      -2/3, 1/3, 1/3, an axis crossing 0 in steps of 0.1, populations of a million), run through every
      point's note, Resid, the least-squares page, Guess and Reveal, Fit, a far-out point and Quit:
      beta 2b prints no small number in scientific form; beta 2a's are listed;
  R7  static: every STRING(x, 2, d) left with d > 0 is one of the justified sites; every INSTRING's
      first argument is guarded or cannot be empty;
  R10 h.sci_strings from EVERY harness run of beta 2b in this script: no small number;
  G   beta 2b against beta 2a: the routines that differ are exactly the ones in the CHANGES; every
      other routine is byte-identical, comments included; slCas differs only by the DIM guard.
(The beta 2a description follows; "v3b" there now means v3d.)

verify_ScatterLab_beta2a.py -- checks for ScatterLab beta 2a (17 Oct 2026): the CAS call form that
CASProbe beta 1b found on the emulator.  Built from verify_ScatterLab_beta2.py: every check is kept;
Part B runs in harness v3b, which models the calculator's CAS (CAS of a variable unevaluated, the
Prime's printing -- the solve of a system in braces, {[a,b]} -- a CAS string as a PPL string); the
canned-answer check gives the answers in the calculator's form; Part G (new) runs beta 2 itself in
v3b and compares beta 2a with beta 2.  New or changed checks are marked "2a".

The beta 2 checks: ScatterLab beta 2's "least squares as calculus"
page (16 Oct 2026).

The magenta line minimises SSE(a, b) = sum (y - a - b x)^2.  The new page has the CAS write
that SSE out for the points (every number exact: a whole number, or a whole number over a
power of ten, 10.4 = 104/10), put it in order, differentiate it in a and in b, and solve the
two normal equations; the fractions sit beside the program's own decimals (slB0, slB1).

Part A  the CAS templates in desktop Giac (giac_eval: a .giac file run by icas) for eleven
        data sets -- the SYNTHETIC example, integers with tied x, two-decimal data, negative
        values, years against crime-sized counts, n = 3, forty one-decimal points, a perfect
        line, a flat set (every y equal), three-decimal data, and a mixed-precision set --
        against
          * Python fractions: the exact solution of the normal equations;
          * SymPy: the expanded SSE and its two partial derivatives (Giac's answer minus
            SymPy's must simplify to 0);
          * statsmodels OLS and numpy polyfit (to 1e-10 of the exact a, b).
        A data set with a 1/3 in it must produce no CAS text.
Part B  the PPL program in the run harness v3:
          * slCxMake's SSE text = this script's, character for character; the parsed a and b
            = the exact fractions; slB0, slB1 = the fractions to 1e-12;
          * the page end to end, opened from the panel (a tap on the equation) and from the
            menu, with cas='giac' (badge, SSE, derivatives, fractions beside the decimals,
            the "10.4 is 104/10" note) and cas='fail' (decimal badge, the normal equations
            with the program's sums, no error);
          * the cache (the page twice: 4 calls, not 8); a drag of a point makes no CAS call
            and the page afterwards shows the moved points' exact line; fewer than 3 points:
            no page, a note; a 1/3 point: the decimal page, no CAS call; the stale-key run.

Run:  python3 verify_ScatterLab_beta2c.py      (exit status 0 = every check passed)
Roger Metcalf / Claude, 16 Oct 2026 (2b: 17 Oct 2026; 2c: 19 Oct 2026).
"""
import os
import random
import re
import sys
from fractions import Fraction as Fr

import numpy as np
import statsmodels.api as sm
import sympy as sp

sys.path.insert(0, '/home/claude/work/out')
import ppl_run_v3e  # noqa: E402  (2c: harness v3e)
from ppl_run_v3e import Harness, giac_eval, prime_print  # noqa: E402

# 2b: every harness made in this script is remembered with its program, so part R10 can list
# every scientific STRING result of every run (h.sci_strings, harness v3d; now v3e)
ALL_RUNS = []
_h_init = ppl_run_v3e.Harness.__init__


def _h_init_rec(self, *a, **k):
    _h_init(self, *a, **k)
    ALL_RUNS.append((os.path.basename(str(a[0] if a else k.get('path', '?'))), self))


ppl_run_v3e.Harness.__init__ = _h_init_rec

# 2c: absolute paths (review item 22: the 2b script opened its predecessors beside itself and stopped
# with FileNotFoundError in a folder holding only the current version)
OUT = '/home/claude/work/out'
PROG = '/home/claude/work/fix19/ScatterLab_beta2c.txt'
B2B = os.path.join(OUT, 'ScatterLab_beta2b.txt')
B2A = os.path.join(OUT, 'ScatterLab_beta2a.txt')
BETA2 = os.path.join(OUT, 'ScatterLab_beta2.txt')
HAVE_OLD = all(os.path.exists(p) for p in (PROG, B2B, B2A, BETA2))
if not HAVE_OLD:
    print('STOP: this script compares beta 2c with betas 2b, 2a and 2 and needs all four files: %s'
          % [p for p in (PROG, B2B, B2A, BETA2) if not os.path.exists(p)])
    sys.exit(2)
FAILS = []
random.seed(161026)


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('   ' + detail if detail else ''))
    if not ok:
        FAILS.append(name)


def istr(n):
    v = int(round(abs(n)))
    return ('-' if n < 0 and v else '') + str(v)


def rat(v):
    """slRat: exact CAS text for a number, or '' (more than six decimals)."""
    for d in range(7):
        s = v * 10 ** d
        n = round(s)
        if abs(s - n) <= 0.000001 + abs(s) * 1e-12:
            if abs(n) >= 1e11:
                return ''
            if d == 0:
                return '(' + istr(n) + ')' if n < 0 else istr(n)
            return '(' + istr(n) + '/' + istr(10 ** d) + ')'
    return ''


def ratfrac(v):
    return Fr(rat(v).strip('()'))


def sse_text(x, y):
    parts = []
    for xi, yi in zip(x, y):
        cx, cy = rat(xi), rat(yi)
        if not (cx and cy):
            return ''
        parts.append('(' + cy + '-sla-slb*' + cx + ')^2')
    return '+'.join(parts)


def exact_line(x, y):
    X = [ratfrac(v) for v in x]
    Y = [ratfrac(v) for v in y]
    n = len(X)
    sx, sy = sum(X), sum(Y)
    sxx = sum(v * v for v in X)
    sxy = sum(u * v for u, v in zip(X, Y))
    b = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    return (sy - b * sx) / n, b


SA, SB = sp.symbols('sla slb')


def sympy_sse(x, y):
    return sp.expand(sum((sp.Rational(ratfrac(yi)) - SA - SB * sp.Rational(ratfrac(xi)))**2 for xi, yi in zip(x, y)))


def parse_giac(t):
    return sp.sympify(t.replace('^', '**'), locals={'sla': SA, 'slb': SB})


def parse_sol(t):
    s = t.replace('list', '')
    for c in '[]{} ':
        s = s.replace(c, '')
    parts = re.split('[,;]', s)
    return tuple(Fr(p.split('=')[-1]) for p in parts) if len(parts) == 2 else None


EX_X = [10.4, 14.9, 7.1, 18.6, 23.0, 25.0, 12.5, 7.5, 14.2, 18.6, 10.8, 19.8, 25.8, 14.0, 16.0, 22.6]
EX_Y = [34.4, 43.5, 22.3, 36.1, 45.2, 35.3, 31.5, 20.2, 26.8, 27.8, 26.2, 41.8, 43.1, 26.0, 30.6, 41.3]
x40 = [round(random.uniform(0, 30), 1) for _ in range(40)]
SETS = [
    ('SYNTHETIC example (16 points, 1 decimal)', EX_X, EX_Y),
    ('integers, tied x', [1, 1, 2, 2, 3, 3, 4], [2, 3, 3, 5, 4, 6, 7]),
    ('two decimals', [round(random.uniform(0, 10), 2) for _ in range(10)], [round(random.uniform(-5, 20), 2) for _ in range(10)]),
    ('negative values', [-5, -3.5, -1, 0, 2.5, 4, 5], [-12.2, -7, -3.1, 0.4, 5.5, 7.9, 11]),
    ('years against crime-sized counts', list(range(2000, 2025)), [random.randint(3000, 6000) for _ in range(25)]),
    ('n = 3', [1, 2, 4], [2, 3, 7]),
    ('forty points, one decimal', x40, [round(0.8 * v + random.gauss(0, 3), 1) for v in x40]),
    ('a perfect line y = 2x + 1 (SSE 0)', [0, 1, 2, 3, 4], [1, 3, 5, 7, 9]),
    ('flat: every y equal', [1, 2, 3, 4], [5, 5, 5, 5]),
    ('three decimals', [0.125, 0.25, 0.375, 0.5, 0.875], [1.001, 1.25, 1.333, 1.5, 2.125]),
    ('mixed precision', [1, 2.5, 3.25, 4.125, 6], [10, 9.5, 7.75, 7.5, 4]),
]

# ============================================================ Part A
print('==== Part A: the CAS templates in desktop Giac, against fractions, SymPy and statsmodels ====')
GI = {}
for nm, x, y in SETS:
    E = sse_text(x, y)
    ea, eb = exact_line(x, y)
    g_sse = giac_eval('normal(' + E + ')')
    g_da = giac_eval('normal(diff(' + E + ',sla))')
    g_db = giac_eval('normal(diff(' + E + ',slb))')
    g_sol = giac_eval('solve([diff(' + E + ',sla)=0,diff(' + E + ',slb)=0],[sla,slb])')
    GI[E] = (g_sse, g_da, g_db, g_sol)
    S = sympy_sse(x, y)
    ok_sse = sp.simplify(parse_giac(g_sse) - S) == 0
    ok_d = sp.simplify(parse_giac(g_da) - sp.diff(S, SA)) == 0 and sp.simplify(parse_giac(g_db) - sp.diff(S, SB)) == 0
    ok_sol = parse_sol(g_sol) == (ea, eb)
    o = sm.OLS(np.array(y, float), sm.add_constant(np.array(x, float))).fit().params
    pf = np.polyfit(np.array(x, float), np.array(y, float), 1)
    tol = lambda u, v: abs(u - float(v)) <= 1e-10 * max(1, abs(float(v)))
    ok_sm = tol(o[0], ea) and tol(o[1], eb) and tol(pf[1], ea) and tol(pf[0], eb)
    check('%-42s SSE %s, d/da d/db %s, solve %s, OLS = polyfit = exact %s' % (
        nm, 'ok' if ok_sse else 'NO', 'ok' if ok_d else 'NO', 'ok' if ok_sol else 'NO', 'ok' if ok_sm else 'NO'),
        ok_sse and ok_d and ok_sol and ok_sm, 'b = %s, a = %s' % (eb, ea))
check('a point at y = 1/3 (more than six decimals): no CAS text at all', sse_text([1, 2, 3], [1 / 3, 1, 2]) == '')
longest = max(len(sse_text(x, y)) for _, x, y in SETS)
check('the longest call (solve: the SSE twice) fits slCasMx = 4000', 2 * longest + 60 <= 4000,
      'SSE text up to %d characters (forty points)' % longest)

# ============================================================ Part B
sol_pr = [prime_print(v[3]) for v in GI.values()]
check('2a: in the Prime\'s printing every solve answer is {[a,b]} (CASProbe T36), the SSE and its derivatives '
      'are unchanged', all(t.startswith('{[') and t.endswith(']}') for t in sol_pr)
      and all(prime_print(v[i]) == v[i] for v in GI.values() for i in (0, 1, 2)), str(sol_pr[:1]))

print('\n==== Part B: the PPL program in the harness (ppl_run_v3d) ====')


def load(x, y, cas='giac'):
    h = Harness(PROG, strict=True, cas=cas)
    h.call('slInit')
    g = h.globals_
    for i in range(40):
        g['slX'][i] = float(x[i]) if i < len(x) else 0.0
        g['slY'][i] = float(y[i]) if i < len(y) else 0.0
    g['slN'] = float(len(x))
    h.call('slAutoWin')
    h.call('slFit')
    return h


okt = oks = okd = True
det = []
for nm, x, y in SETS:
    h = load(x, y)
    h.call('slCxMake')
    g = h.globals_
    E = sse_text(x, y)
    ea, eb = exact_line(x, y)
    okt = okt and g['slCxK'] == E and g['slCxE'] == GI[E][0]
    got = (Fr(g['slCxSa']), Fr(g['slCxSb'])) if g['slCxSa'] else None
    oks = oks and got == (ea, eb) and g['slCxSt'] == 1
    okd = okd and abs(g['slB1'] - float(eb)) <= 1e-12 * max(1, abs(float(eb))) and \
        abs(g['slB0'] - float(ea)) <= 1e-12 * max(1, abs(float(ea)))
    if got != (ea, eb):
        det.append(nm)
check('slCxMake builds exactly this SSE text, %d data sets' % len(SETS), okt)
check('the PPL reads solve\'s answer: a and b = the exact fractions, every set', oks, str(det))
check('the program\'s slB1, slB0 = the exact fractions to 1e-12', okd)

# the page from the panel, inside a whole run: Data soft key -> example -> tap the equation
DATA_KEY = (4 * 53.4 + 20, 228)
for mode in ('giac', 'fail'):
    h = Harness(PROG, strict=True, cas=mode)
    h.tap(*DATA_KEY)
    h.choose(1)                                   # Poverty vs crime (SYNTHETIC)
    h.tap(262, 70)                                # the equation in the panel
    h.press('Enter')                              # any key: back to the plot
    h.press('Esc')                                # quit
    r = h.call('ScatterLab')
    pg = [p for p in h.pages if p.has('Least squares as calculus')]
    pg = pg[-1] if pg else None
    if mode == 'giac':
        want = ['exact (CAS)', 'SSE = sum (y - a - bx)^2 over all n = 16 points',
                u'SSE = 16×a^2+2608/5×a×b-5321/5×a+119443/25×b^2', '-36841/2×b+373319/20',
                u'dSSE/da = 32×a+2608/5×b-5321/5 = 0', u'dSSE/db = 2608/5×a+238886/25×b-36841/2 = 0',
                'b = 2441/2394   (program 1.019632)', 'a = 3186173/191520   (program 16.63624)',
                'Exact: x = 10.4 is 104/10, so nothing is rounded.', 'any key or tap = back to the plot']
        check('panel tap -> the page (Giac): badge, SSE, derivatives, fractions beside the decimals, the note',
              pg is not None and all(pg.has(w) for w in want), str(pg.lines() if pg else None))
        check('the page: four CAS calls, all answered; the run ends normally',
              len(h.cas_calls) == 4 and isinstance(r, str) and r.startswith('ScatterLab: n = 16'), repr(r))
        check('2a: every text asks for string(...), every answer quoted, the solve in braces; no CAS variable '
              'assigned, no CAS call of a variable',
              all(c[0].startswith('string(') and c[1].startswith('"') for c in h.cas_calls)
              and h.cas_calls[3][1].startswith('"{[') and not h.cas_vars
              and not any('non-literal' in w for w in h.warnings), str(h.cas_calls[3][1][:40]))
    else:
        want = ['decimal', 'The CAS did not answer: no exact fractions.', 'n a + (sum x) b = sum y',
                '  16 a + 260.8 b = 532.1', '(sum x) a + (sum x^2) b = sum x y', '  260.8 a + 4777.72 b = 9210.25',
                '  b = 1.019632,  a = 16.63624']
        check('cas=fail: decimal badge, the normal equations with the program\'s sums, no error',
              pg is not None and all(pg.has(w) for w in want) and not pg.has('exact (CAS)') and h.error is None,
              str(pg.lines() if pg else None))
# the menu path, twice: cached
h = Harness(PROG, strict=True)
h.tap(*DATA_KEY).choose(1)
h.press('Enter').choose(5).press('Enter')        # Enter = menu, item 5 = the page, a key back
h.press('Enter').choose(5).press('Enter')
h.press('Esc')
r = h.call('ScatterLab')
check('Menu > Least squares as calculus, twice: 4 CAS calls, not 8', len(h.cas_calls) == 4, '%d' % len(h.cas_calls))
check('the menu has ten items, the new one fifth', h.chooses[1].items[4] == 'Least squares as calculus'
      and len(h.chooses[1].items) == 10)
# a drag makes no CAS call; the page afterwards fits the moved point exactly.  A whole run:
# Data -> example, open the page (4 calls), drag point 1 down, open the page again.
h0 = load(EX_X, EX_Y)
px, py = h0.call('slPx', 10.4), h0.call('slPy', 34.4)
h = Harness(PROG, strict=True)
h.tap(*DATA_KEY).choose(1)
h.tap(262, 70).press('Enter')                    # the page: 4 CAS calls
h.drag([(px, py), (px, py + 10), (px, py + 20), (px, py + 30)])
h.tap(262, 70).press('Enter')                    # the page again: the points changed
h.press('Esc')
r = h.call('ScatterLab')
g = h.globals_
x2, y2 = list(g['slX'][:16]), list(g['slY'][:16])
ea, eb = exact_line(x2, y2)
pages = [pg for pg in h.pages if pg.has('Least squares as calculus')]
# the drag's frames come between the two pages; the CAS log must show 4 + 4 calls only
check('a drag of point 1 (down 30 px): it moved; 8 CAS calls in all = 4 per page, none in the drag',
      y2[0] != 34.4 and len(h.cas_calls) == 8, 'point 1 now (%g, %g), %d calls' % (x2[0], y2[0], len(h.cas_calls)))
check('the page after the drag: the moved points\' exact line', len(pages) == 2 and pages[1].has('b = %s   (program' % eb),
      str([t.text for t in pages[-1].texts if t.text.startswith('b ')]) + ' want b = %s' % eb)
# the kit's quote strip (2a: canned answers as the calculator gives them -- string(...) answers,
# PPL strings whose quotes STRING() adds and slCas drops, the solve in braces, CASProbe T36)
E = sse_text(EX_X, EX_Y)
calls = ['normal(' + E + ')', 'normal(diff(' + E + ',sla))', 'normal(diff(' + E + ',slb))',
         'solve([diff(' + E + ',sla)=0,diff(' + E + ',slb)=0],[sla,slb])']
canned = {'string(' + c + ')': '"' + prime_print(a) + '"' for c, a in zip(calls, GI[E])}
h = load(EX_X, EX_Y, cas=canned)
h.press('Enter')
h.call('slCxPage')
check('slCas drops one surrounding pair of quotes: the quoted answers still give the exact page',
      h.globals_['slCxSt'] == 1 and h.pages[-1].has('b = 2441/2394   (program 1.019632)')
      and h.pages[-1].has('exact (CAS)'), str(h.globals_['slCxE']))
# fewer than 3 points: no page
h = load([1, 2], [3, 4])
h.call('slCxPage')
check('two points: no page, the note says why, no CAS call',
      h.globals_['slMsg1'] == 'Least squares needs 3 points with different x.' and len(h.cas_calls) == 0 and not h.pages)
# a 1/3 point
h = load([1, 2, 3, 4.5], [1 / 3, 2.5, 2.9, 4.1])
h.press('Enter')
h.call('slCxPage')
check('a point at y = 1/3: "needs over 6 decimals", the decimal page, no CAS call',
      h.pages[-1].has('A value needs over 6 decimals: no exact fractions.') and len(h.cas_calls) == 0)
# the stale-key run: menu -> data -> example -> menu -> the page -> quit
h = Harness(PROG, strict=False, stale_keys=True, idle_key=4)
h.press('Enter').choose(6).choose(1)            # Enter = menu, Data, example
h.press('Enter').choose(5).press('Enter')        # the page, a key back
h.press('Enter').choose(10)                      # Quit (A)
r = h.call('ScatterLab')
check('stale-key run: menu, Data, example, the page, quit (item A); nothing skipped',
      not h.stale_skips and isinstance(r, str) and r.startswith('ScatterLab: n = 16, y-hat = 16.64'),
      'result %r, skips %r' % (r, h.stale_skips))

# G (2a): beta 2 in v3b -- the emulator's finding: its slCas hands back its own text, the solve's
# echo keeps "sla" in it, and the page falls back to the decimals
h = Harness(BETA2, strict=True, cas='giac')
h.tap(*DATA_KEY)
h.choose(1)
h.tap(262, 70)
h.press('Enter')
h.press('Esc')
h.call('ScatterLab')
pg = [p for p in h.pages if p.has('Least squares as calculus')]
check('2a: beta 2 in v3b: the page says "decimal" and gives no fractions -- the emulator\'s finding',
      bool(pg) and pg[-1].has('decimal') and not pg[-1].has('exact (CAS)') and any('non-literal' in w for w in h.warnings))
say = print
_saved_check = check


def _check2(cond, msg):
    _saved_check(msg, cond)


check = _check2

# ================================================================ G (round 2a)
say('\nG. beta 2a: beta 2 in harness v3b, and beta 2a against beta 2')
import re as _re
_b_old = open(BETA2, encoding='utf-8').read()
_b_new = open(B2A, encoding='utf-8').read()          # 2b: this section is the 2a-vs-2 record


def _bodies(txt):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)
    c = _re.sub(r'//[^\n]*', '', c)
    out = {}
    for m in _re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, _re.S):
        out[m.group(1)] = _re.sub(r'[ \t]+\n', '\n', m.group(0))
    return out


_B0, _B1 = _bodies(_b_old), _bodies(_b_new)
_diff = sorted(n for n in set(_B0) | set(_B1) if _B0.get(n) != _B1.get(n))
check(_diff == ['slCas'], 'beta 2a: routines that differ from beta 2: %s (want slCas)' % _diff)


def _outside(t, names):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\n]*', '', t))
    if names:
        c = _re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
    return _re.sub(r'\s+', ' ', c)


check(_outside(_b_old, _diff) == _outside(_b_new, _diff), 'beta 2a: outside those routines only comments differ')
_py0 = _re.findall(r'(?s)#PYTHON.*?#END', _b_old)
_py1 = _re.findall(r'(?s)#PYTHON.*?#END', _b_new)
check(_py0 == _py1, 'beta 2a: the #PYTHON blocks are unchanged')
say('  routines that differ from beta 2: %s; everything else differs only in comments' % ', '.join(_diff))

check = _saved_check


# ================================================================ R (2b): the second emulator round
say('\nR. 2b: the second emulator round (harness v3d; now v3e, run on beta 2c)')


def ck(cond, msg):
    check(msg, cond)


def err_of(fn):
    """Run fn(); return None, or 'ErrorType: message' if it raised."""
    try:
        fn()
        return None
    except Exception as e:                                   # noqa: BLE001
        return '%s: %s' % (type(e).__name__, str(e)[:90])


def is_instring_err(e):
    return bool(e) and 'INSTRING: Invalid input' in e


# ---- R1: slRepl directly ----
RCASES = [('{[1,2]}', '}', '', '{[1,2]', 'the pattern at the END (solve\'s closing brace)'),
          ('{[1,2]}', '{', '', '[1,2]}', 'the pattern at the START'),
          ('abc', 'abc', '', '', 'the pattern is the WHOLE text'),
          ('abc', 'abc', 'xyz', 'xyz', 'the whole text, replaced'),
          ('abc', '', 'X', 'abc', 'an EMPTY pattern: the text unchanged (no endless loop)'),
          ('', 'a', 'b', '', 'an EMPTY text'),
          ('sla*slb*sla', 'sla', 'a', 'a*slb*a', 'twice, at both ends'),
          ('2*a*b', '*', u'×', u'2×a×b', 'in the middle, twice'),
          ('}}}', '}', '', '', 'only the pattern, three times')]
h = Harness(PROG, strict=True, cas='fail'); h.call('slInit')
for t, o, nw, want, what in RCASES:
    got, e = None, None
    try:
        got = h.call('slRepl', t, o, nw)
    except Exception as ex:                                  # noqa: BLE001
        e = str(ex)[:80]
    ck(e is None and got == want, 'R1 slRepl(%r, %r, %r) = %r: %s' % (t, o, nw, got if e is None else e, what))
ho = Harness(B2A, strict=True, cas='fail'); ho.call('slInit')
# (beta 2a's slRepl is not given the empty pattern: INSTRING(s, "") = 1, so it would never stop)
old_r1 = [(t, o, err_of(lambda t=t, o=o, nw=nw: ho.call('slRepl', t, o, nw)))
          for t, o, nw, _w, _x in (RCASES[0], RCASES[2], RCASES[5], RCASES[8])]
ok_start = err_of(lambda: ho.call('slRepl', '{[1,2]}', '{', '')) is None
ck(all(is_instring_err(e) for _t, _o, e in old_r1) and ok_start,
   'R1 beta 2a in v3d: its slRepl stops with the INSTRING error whenever the text runs out -- the pattern at '
   'the end, the whole text, an empty text, only the pattern (%s); a pattern at the start works -- the '
   'emulator\'s crash' % [(t, o) for t, o, _e in old_r1])

# ---- R2: slCas, slCxClean, slCxSol on empty answers ----
h = Harness(PROG, strict=True, cas='fail'); h.call('slInit')
r_cas = h.call('slCas', 'normal(1+1)')
ck(r_cas == '' and h.error is None, 'R2 slCas with the CAS failing: "" and no error (got %r)' % r_cas)
ck(h.call('slCxClean', '') == '', 'R2 slCxClean("") = "" (no INSTRING on the empty text)')
sols = [('', ('', '')), ('{}', ('', '')), ('[]', ('', '')), ('{[]}', ('', '')),
        ('{[sla=,slb=1/2]}', ('', '')), ('{[1/2,slb=]}', ('', '')), ('{[3186173/191520,2441/2394]}',
                                                                      ('3186173/191520', '2441/2394')),
        ('[sla=1/2,slb=3/4]', ('1/2', '3/4')), ('list[[5/7,-2/9]]', ('5/7', '-2/9')),
        ('{[1/2,3/4],[5/6,7/8]}', ('', ''))]
bad = []
for s_, want in sols:
    e = err_of(lambda s_=s_: h.call('slCxSol', s_))
    got = (h.globals_['slCxSa'], h.globals_['slCxSb'])
    if e or got != want:
        bad.append((s_, got, e))
ck(not bad, 'R2 slCxSol on %d answers (empty, {}, [], "sla=" with nothing after it, two solutions, the Prime\'s '
   'and Giac\'s forms): the right halves, no error %s' % (len(sols), bad))
ho = Harness(B2A, strict=True, cas='fail'); ho.call('slInit')
e_old = err_of(lambda: ho.call('slCas', 'normal(1+1)'))
ck(is_instring_err(e_old), 'R2 beta 2a in v3d: slCas with the CAS failing stops (%s) -- every fallback was broken' % e_old)

# ---- R3, R4: Data > Poverty vs crime > tap the equation; and Menu > Least squares as calculus ----
WANT_EXACT = ['exact (CAS)', 'b = 2441/2394   (program 1.019632)', 'a = 3186173/191520   (program 16.63624)',
              u'dSSE/da = 32×a+2608/5×b-5321/5 = 0', 'Exact: x = 10.4 is 104/10, so nothing is rounded.']
WANT_DEC = ['decimal', 'The CAS did not answer: no exact fractions.', '  16 a + 260.8 b = 532.1',
            '  260.8 a + 4777.72 b = 9210.25', '  b = 1.019632,  a = 16.63624']


def eq_run(path, mode, via='tap'):
    hh = Harness(path, strict=True, cas=mode)
    hh.tap(*DATA_KEY).choose(1)
    if via == 'tap':
        hh.tap(262, 70)                       # the equation in the panel
    else:
        hh.press('Enter').choose(5)           # Menu > Least squares as calculus
    hh.press('Enter').press('Esc')
    e = err_of(lambda: hh.call('ScatterLab'))
    pg = [p for p in hh.pages if p.has('Least squares as calculus')]
    return hh, e, (pg[-1] if pg else None)


for mode in ('giac', 'fail'):
    for via in ('tap', 'menu'):
        hn, en, pn = eq_run(PROG, mode, via)
        ho, eo, po = eq_run(B2A, mode, via)
        want = WANT_EXACT if mode == 'giac' else WANT_DEC
        tag = 'R3' if mode == 'giac' else 'R4'
        badge = [t.text for t in pn.texts if t.y in (8, 10)] if pn is not None else []
        ck(en is None and pn is not None and all(pn.has(w) for w in want)
           and badge[-1:] == (['exact (CAS)'] if mode == 'giac' else ['decimal']) and isinstance(hn.result, str)
           and hn.result.startswith('ScatterLab: n = 16, y-hat = 16.64 + 1.020 x, r = 0.7512'),
           '%s %s, cas=%s: the page opens, %s, no error; quit returns the summary (%s)' % (
               tag, 'tap on the equation' if via == 'tap' else 'Menu > Least squares as calculus', mode,
               'b = 2441/2394, a = 3186173/191520, "exact (CAS)"' if mode == 'giac' else '"decimal" and the normal '
               'equations', en))
        ck(is_instring_err(eo) and po is None and (mode == 'fail' or len(ho.cas_calls) == 4),
           '%s beta 2a, the same run in v3d: %s"%s" -- the emulator\'s finding' % (
               tag, 'the CAS answers all 4 calls, then ' if mode == 'giac' else '', (eo or '')[:58]))

# ---- R5: canned answers: an empty solve, "sla=", empty strings ----
E = sse_text(EX_X, EX_Y)
CALLS = ['normal(' + E + ')', 'normal(diff(' + E + ',sla))', 'normal(diff(' + E + ',slb))',
         'solve([diff(' + E + ',sla)=0,diff(' + E + ',slb)=0],[sla,slb])']
good = ['"' + prime_print(v) + '"' for v in GI[E]]
for label, answers, exact in (('solve gives {} (no solution)', good[:3] + ['"{}"'], False),
                              ('solve gives {[sla=,slb=1/2]}', good[:3] + ['"{[sla=,slb=1/2]}"'], False),
                              ('every answer an empty string', ['""'] * 4, False),
                              ('the Prime\'s own answers (control)', good, True)):
    canned = {'string(' + c + ')': v for c, v in zip(CALLS, answers)}
    res = []
    for path in (PROG, B2A):
        hh = Harness(path, strict=True, cas=canned)
        hh.call('slInit')
        g = hh.globals_
        for i in range(40):
            g['slX'][i] = float(EX_X[i]) if i < 16 else 0.0
            g['slY'][i] = float(EX_Y[i]) if i < 16 else 0.0
        g['slN'] = 16.0
        hh.call('slAutoWin'); hh.call('slFit')
        hh.press('Enter')
        e = err_of(lambda hh=hh: hh.call('slCxPage'))
        res.append((e, hh.pages[-1] if hh.pages else None))
    (en, pn), (eo, po) = res
    okn = en is None and pn is not None and (pn.has('exact (CAS)') if exact else (
        pn.has('decimal') and pn.has('The CAS did not answer: no exact fractions.')))
    ck(okn, 'R5 canned, %s: beta 2c %s, no error; beta 2a: %s' % (
        label, 'the exact page' if exact else 'the decimal page', 'runs' if eo is None else eo[:50]))

# ---- R6: data sets built to give small numbers, through every view ----
RESID_KEY, GUESS_KEY = (2 * 53.4 + 26, 228), (3 * 53.4 + 26, 228)


def run_sl(path, xs, ys, cas='giac', page=True):
    """Data > Load from C1, C2; every point selected in turn (its note line); Resid; the least-squares
    page (Menu); Guess, Reveal, back; Fit; a far-out point; Quit."""
    hh = Harness(path, strict=False, idle_key=4, cas=cas)
    hh.globals_['C1'] = [float(v) for v in xs]
    hh.globals_['C2'] = [float(v) for v in ys]
    hh.tap(*DATA_KEY).choose(2)
    for _ in range(len(xs)):
        hh.press('Plus')
    hh.tap(*RESID_KEY)
    if page:
        hh.press('Enter').choose(5).press('Enter')
    hh.tap(*GUESS_KEY).press('Enter').press('Esc')
    hh.press('Zero')
    hh.press('Enter').choose(1)
    hh.press('Plus')
    hh.press('Enter').choose(10)
    e = err_of(lambda: hh.call('ScatterLab'))
    return hh, e


# (the last field: True where beta 2a's page can run too -- no CAS call, so no INSTRING on a CAS answer)
SCEN = [('Poverty vs crime (the emulator\'s data)', EX_X, EX_Y, False),
        ('r near 0 (r = 0.0002, r-squared 5E-8)', [1, 2, 3, 4, 5, 6], [5, 1, 3, 3, 1, 5.002], False),
        ('a loaded value finer than the grid (0.004 on a step of 10)', [0.004, 5, 10, 20, 40],
         [0.003, 2, 4, 8, 16.5], False),
        ('x = -2/3, 1/3, 1/3 (sum x is -1E-12 on the Prime, 0 here)', [-2 / 3, 1 / 3, 1 / 3], [1, 2, 3], True),
        ('x = -2/3, -1/3, 1/3, 2/3 (sum x is -1.1E-16 here)', [-2 / 3, -1 / 3, 1 / 3, 2 / 3], [1, 2, 2, 3], True),
        ('an axis crossing 0 in steps of 0.1', [-0.55, -0.2, 0.15, 0.5], [-0.33, 0.1, 0.2, 0.45], False),
        ('populations of a million (sum x^2 = 8.7E12)', [1000000, 1200000, 1500000, 2000000], [10, 12, 15, 21],
         False)]
R6_OLD = {}
for nm, xs, ys, old_page in SCEN:
    hg, eg = run_sl(PROG, xs, ys, 'giac')
    hf, ef = run_sl(PROG, xs, ys, 'fail')
    ho, eo = run_sl(B2A, xs, ys, 'giac', page=old_page)
    small_new = [q for q in hg.sci_strings + hf.sci_strings if abs(q[0]) < 1]
    big_new = sorted({q[2] for q in hg.sci_strings + hf.sci_strings if abs(q[0]) >= 1e12})
    R6_OLD[nm] = sorted({(round(v, 9), d, r) for v, d, r in ho.sci_strings})
    pgs = [p for p in hg.pages if p.has('Least squares as calculus')]
    notes = [t.text for p in hg.pages for t in p.texts if t.text.startswith('Pt ')]
    ck(eg is None and ef is None and not small_new and len(pgs) == 1 and len(set(notes)) >= len(xs)
       and isinstance(hg.result, str) and hg.result.startswith('ScatterLab: n = %d' % (len(xs) + 1)),
       'R6 %s: every point\'s note, Resid, the page (CAS and cas=fail), Guess, Fit, a far point, Quit -- no error, '
       'no small number in scientific form (%d frames)%s' % (nm, len(hg.pages) + len(hf.pages),
                                                            ('; from 1E12 up: %s' % big_new) if big_new else ''))
for nm, _x, _y, old_page in SCEN:
    say('  R6 beta 2a, the same run%s: %s -> %s' % (
        '' if old_page else ' (its page skipped: it stops there)', nm, [r for _v, _d, r in R6_OLD[nm]][:6] or 'none'))
REACH = [SCEN[1][0], SCEN[2][0], SCEN[4][0]]
ck(all(R6_OLD[nm] for nm in REACH), 'R6 beta 2a prints scientific forms for r near 0 (r, r-squared), the loaded value '
   '(x, y) and the cancelling x (sum x on the decimal page): the sets reach the case.  The axis set and the '
   'populations are checks on beta 2c only (the axis remainder does not arise in the harness either; the '
   'decimal page needs a failed CAS, which stops beta 2a)')
x_note = [t.text for nm, hh in ALL_RUNS for p in hh.pages for t in p.texts
          if nm == os.path.basename(PROG) and t.text.startswith('Pt 1 (0, 0.0)')]
ck(bool(x_note), 'R6 the loaded point (0.004, 0.003) on a 10-by-1 grid reads "%s"' % (x_note[0] if x_note else None))

# ---- R7: static review ----


def strip_comments(txt):
    out = []
    for line in re.sub(r'(?s)#PYTHON.*?#END', '', txt).split('\n'):
        q, cut = False, len(line)
        for i, ch in enumerate(line):
            if ch == '"':
                q = not q
            elif not q and line.startswith('//', i):
                cut = i
                break
        out.append(line[:cut])
    return '\n'.join(out)


def string_calls(txt):
    out = []
    for m in re.finditer(r'(?<![A-Za-z])STRING\(', txt):
        i, d = m.end(), 1
        while d and i < len(txt):
            d += {'(': 1, ')': -1}.get(txt[i], 0)
            i += 1
        out.append(txt[m.start():i])
    return out


def top_args(call):
    inner, out, d, q, cur = call[call.index('(') + 1:-1], [], 0, False, ''
    for ch in inner:
        if ch == '"':
            q = not q
        if not q and ch in '([{':
            d += 1
        if not q and ch in ')]}':
            d -= 1
        if ch == ',' and d == 0 and not q:
            out.append(cur.strip()); cur = ''
        else:
            cur += ch
    out.append(cur.strip())
    return out


code = strip_comments(open(PROG, encoding='utf-8').read())
fixed_d = [c for c in string_calls(code) if len(top_args(c)) == 3 and top_args(c)[1] == '2']
nonzero = sorted({c for c in fixed_d if top_args(c)[2] != '0'})
JUST = {'STRING(fxR, 2, fxD)': 'slFx: rounded first',
        'STRING(sgV, 2, sgD)': 'slSig: |x| >= 0.00001 here (below it prints 0.00) and sgD <= 5',
        'STRING(rnV, 2, DIM(rnD) - 1)': 'slRatNote: slRat chose the fewest decimals d, so |x| >= 10^-d',
        'STRING(slXlo, 2, axD)': 'slAxes, a width only: slXlo is 0 or a whole number of steps',
        'STRING(slXhi, 2, axD)': 'slAxes, a width only: slXhi is a whole number of steps',
        'STRING(slLevH(slSel), 2, 2)': 'the leverage h >= 1/n >= 0.025',
        'STRING(0, 2, 2)': 'slSig: the literal 0 for |x| < 0.00001'}
ck(set(nonzero) == set(JUST), 'R7 every STRING(x, 2, d) left with d > 0 (%d) is a justified site; the rest go through '
   'slFx (%d calls): extra %s, missing %s' % (len(nonzero), code.count('slFx('),
                                             sorted(set(nonzero) - set(JUST)), sorted(set(JUST) - set(nonzero))))
zero_args = sorted({top_args(c)[0] for c in fixed_d if top_args(c)[2] == '0'})
WHOLE = {'slN', 'lcU', 'lcN', 'DIM(clT)', 'cfN', 'hgP', 'hgN', 'slSel', 'nmV', '0'}
ck(set(zero_args) <= WHOLE, 'R7 every STRING(x, 2, 0) prints a whole number (n, counts, page numbers; nmV in its '
   'FP = 0 branch; slSig\'s literal 0): %s' % zero_args)
ins = [m.group(1).strip() for m in re.finditer(r'INSTRING\(([^,]+),', code)]
# 2c: nmS joins the list (slNum's new site, guarded by DIM(nmS) > 0) -- the 2b expected set was without it
ck(sorted(set(ins)) == sorted({'cR', 'rnR', 'rpS', 'ccR', 'soS', 'slCxSb', 'slCxSa', 'cxX', 'cxY', '"0123456789"', 'nmS'}),
   'R7 INSTRING first arguments: %s' % sorted(set(ins)))
guards = [r'IF DIM\(cR\) > 0 THEN\s+IF INSTRING\(cR, "undef"\)',
          r'IF DIM\(rpO\) == 0 THEN RETURN rpT; END;',
          r'rpI := 0; IF DIM\(rpS\) > 0 THEN rpI := INSTRING\(rpS, rpO\); END;\s+WHILE',
          r'rpI := 0; IF DIM\(rpS\) > 0 THEN rpI := INSTRING\(rpS, rpO\); END;\s+END;\s+RETURN rpR \+ rpS;',
          r'IF DIM\(ccR\) == 0 THEN RETURN ""; END;\s+IF INSTRING\(ccR',
          r'IF DIM\(soS\) == 0 THEN RETURN; END;\s+soK := INSTRING\(soS',
          r'IF DIM\(slCxSa\) == 0 OR DIM\(slCxSb\) == 0 THEN [^\n]*\n\s+IF INSTRING\(slCxSa, "sl"\)',
          r'IF DIM\(cxX\) == 0 OR DIM\(cxY\) == 0 THEN',
          r'IF soK < 2 OR soK >= DIM\(soS\) THEN RETURN; END;',
          r'IF DIM\(nmS\) > 0 THEN\s+IF INSTRING\(nmS, "\."\) > 0 THEN']          # 2c: slNum
ck(all(re.search(gd, code) for gd in guards),
   'R7 the guards are in place: cR (slCas), rpS and rpO (slRepl), ccR (slCxClean), soS and the halves (slCxSol); '
   'cxX, cxY are never empty (slCxMake returns first), rnR always holds a "/" (slCxMake calls slRatNote only then), '
   'slCxSb is non-empty (soK < DIM(soS)) %s' % [gd[:30] for gd in guards if not re.search(gd, code)])
say('  LEFT / MID / RIGHT calls in the code (counts and starts reviewed by hand, see the CHANGES): %d / %d / %d'
    % (len(re.findall(r'\bLEFT\(', code)), len(re.findall(r'\bMID\(', code)), len(re.findall(r'\bRIGHT\(', code))))

# ---- G (2b): beta 2b against beta 2a ----
_o, _n = open(B2A, encoding='utf-8').read(), open(B2B, encoding='utf-8').read()   # 2c: the 2b-vs-2a record


def raw_bodies(txt):
    out = {}
    for m in re.finditer(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', txt):
        out[m.group(1)] = m.group(0)
    return out


R0, R1b = raw_bodies(_o), raw_bodies(_n)
diff2b = sorted(nm for nm in set(R0) | set(R1b) if R0.get(nm) != R1b.get(nm))
WANT2B = sorted(['ScatterLab', 'slAxes', 'slCas', 'slCxClean', 'slCxSol', 'slDec', 'slFx', 'slNotes', 'slNum',
                 'slPanel', 'slRepl'])
ck(diff2b == WANT2B, 'G 2b: routines that differ from beta 2a (comments included): %s' % diff2b)
same = sorted(set(R0) - set(diff2b))
ck(set(R1b) - set(R0) == {'slFx'} and not set(R0) - set(R1b) and all(R0[nm] == R1b[nm] for nm in same)
   and len(same) + len(diff2b) - 1 == len(R0),
   'G 2b: beta 2a has %d routines; the other %d are byte-identical in beta 2b, comments included; one new '
   '(slFx), none removed' % (len(R0), len(same)))
ck(_outside(_o, diff2b) == _outside(_n, diff2b), 'G 2b: outside those routines only comments differ (the header)')
GUARD = ('  // an empty answer is already a failure; INSTRING("", ...) is "Invalid input" on\n'
         '  // the Prime (emulator, 17 Oct 2026), so the checks run only on a non-empty answer\n'
         '  IF DIM(cR) > 0 THEN\n'
         '    IF INSTRING(cR, "undef") > 0 OR INSTRING(cR, "rror") > 0 OR INSTRING(cR, CHAR(8734)) > 0 THEN cR := ""; END;\n'
         '  END;\n')
OLDL = '  IF INSTRING(cR, "undef") > 0 OR INSTRING(cR, "rror") > 0 OR INSTRING(cR, CHAR(8734)) > 0 THEN cR := ""; END;\n'
ck(GUARD in R1b['slCas'] and R1b['slCas'].replace(GUARD, OLDL) == R0['slCas'],
   'G 2b: slCas = beta 2a\'s with only the brief\'s DIM guard (the IFERR line and the quote strip byte-identical)')
TPL = ['IF DIM(rpO) == 0 THEN RETURN rpT; END;', 'rpR := ""; rpS := rpT; rpK := DIM(rpO);',
       'rpI := 0; IF DIM(rpS) > 0 THEN rpI := INSTRING(rpS, rpO); END;', 'WHILE rpI > 0 DO',
       'IF rpI > 1 THEN rpR := rpR + LEFT(rpS, rpI - 1); END;', 'rpR := rpR + rpN;',
       'IF rpI + rpK > DIM(rpS) THEN rpS := ""; ELSE rpS := MID(rpS, rpI + rpK); END;',
       'rpI := 0; IF DIM(rpS) > 0 THEN rpI := INSTRING(rpS, rpO); END;', 'END;', 'RETURN rpR + rpS;']
body = [l.strip() for l in R1b['slRepl'].split('\n') if l.strip() and not l.strip().startswith('//')]
ck(body == ['slRepl(rpT, rpO, rpN)', 'BEGIN', 'LOCAL rpR, rpS, rpI, rpK;'] + TPL + ['END;'],
   'G 2b: slRepl is the brief\'s replace loop, line for line')
ck(re.findall(r'(?s)#PYTHON.*?#END', _o) == re.findall(r'(?s)#PYTHON.*?#END', _n), 'G 2b: no #PYTHON block, as before')
ck(all(ord(c) < 128 for c in _n), 'G 2b: the file is still pure ASCII (glyphs through CHAR())')

# ================================================================ D (2c): the fleet review's D-SL-1
say('\nD. 2c: slNum strips trailing zeros only from a number with a decimal point (fleet review 19 Oct 2026, '
    'D-SL-1); each test on beta 2c and on beta 2b')
import math  # noqa: E402
import subprocess  # noqa: E402

# D1: the review's values (check_ScatterLab.py section 4)
D1 = [(260.8, '260.8'), (1400.0, '1400'), (2e9, '2000000000'), (1.4e11, '140000000000'),
      (1.23456789e11, '123456789000'), (1.23456789012e11, '123456789012'), (1.4e12, u'1.40000ᴇ12'),
      (-1.4e11, '-140000000000'), (1e11, '100000000000'), (99999999999.5, '99999999999.5'),
      (999999999999.0, '999999999999'), (5e10, '50000000000'), (123.456789, '123.457'), (0.000001, '0.000001')]
hn_ = Harness(PROG, strict=True, cas='fail'); hn_.call('slInit')
ho_ = Harness(B2B, strict=True, cas='fail'); ho_.call('slInit')
old_wrong = []
for v, want in D1:
    got = hn_.call('slNum', float(v))
    ck(got == want, 'D1 slNum(%r) = %r (want %r)' % (v, got, want))
    got_o = ho_.call('slNum', float(v))
    if got_o != want:
        old_wrong.append((v, got_o))
# beta 2b: from 1E11 up STRING(x, 2, 1) has no "." (12 digits), so the strip eats real zeros; below 1E11
# (5E10 -> "50000000000.0") the "." is there and 2b was right
ck(sorted(old_wrong) == sorted([(1.4e11, '14'), (1.23456789e11, '123456789'), (-1.4e11, '-14'), (1e11, '1')]),
   'D1 beta 2b gets exactly the numbers from 1E11 up that end in 0 wrong: %s' % old_wrong)
say('  D1 beta 2c: all %d right; beta 2b: %s' % (len(D1), old_wrong))

# D2: the decimal page itself (the CAS failing, so the page shows the program's sums)
pg_lines = {}
for path in (PROG, B2B):
    hh = Harness(path, strict=True, cas='fail')
    hh.call('slInit')
    g = hh.globals_
    xs, ys = [100000, 200000, 300000], [1, 2, 3]
    for i in range(40):
        g['slX'][i] = float(xs[i]) if i < 3 else 0.0
        g['slY'][i] = float(ys[i]) if i < 3 else 0.0
    g['slN'] = 3.0
    hh.call('slAutoWin'); hh.call('slFit')
    hh.press('Enter')
    hh.call('slCxPage')
    pg_lines[path] = [t.text for t in hh.pages[-1].texts if ' a + ' in t.text] if hh.pages else []
ck(pg_lines[PROG] == ['n a + (sum x) b = sum y', '  3 a + 600000 b = 6', '(sum x) a + (sum x^2) b = sum x y',
                      '  600000 a + 140000000000 b = 1400000'],
   'D2 the decimal page for x = 1E5, 2E5, 3E5 (sum x^2 = 1.4E11), beta 2c: %s' % pg_lines[PROG])
ck('  600000 a + 14 b = 1400000' in pg_lines[B2B], 'D2 beta 2b printed "600000 a + 14 b = 1400000": %s' % pg_lines[B2B])
say('  D2 decimal page: beta 2c "%s"; beta 2b "%s"' % (pg_lines[PROG][-1], pg_lines[B2B][-1]))

# D3: a property sweep over 3,000 values
rng_ = random.Random(191026)
VALS = []
for _ in range(2000):
    e = rng_.uniform(-7, 12)
    v = round(10 ** e, rng_.randint(0, 8))
    if v == 0 or abs(v) >= 1e12:
        continue
    VALS.append(v if rng_.random() < 0.7 else -v)
for _ in range(600):
    VALS.append(float(rng_.randint(1, 999) * 10 ** rng_.randint(7, 9)))       # up to 1E12, trailing zeros
for _ in range(400):
    VALS.append(float(rng_.randint(10 ** 9, 10 ** 12 - 1)))
VALS += [1e9, 1e10, 1e11, 999999999999.0, 100000000000.5, 123456789012.0, 0.1, 0.5, 10.0, 1e-6]


def nm_ok(v, s):
    """slNum's text for v: the value to its decimals (or to 12 significant digits), never a digit lost; no
    trailing zero after a decimal point, no trailing point"""
    if '.' in s and (s.endswith('0') or s.endswith('.')):
        return False
    try:
        f = float(s.replace(u'−', '-'))
    except ValueError:
        return False
    if v == int(v) and abs(v) < 1e9:
        return f == v
    nd = max(1, min(6, 5 - math.floor(math.log10(abs(v)))))
    nd = min(nd, 11 - math.floor(math.log10(abs(v))))           # the Prime's fixed form: 12 digits at most
    # half a unit at the shown decimals, plus one unit in the 12th significant digit: the Prime holds 12
    # digits, and the harness rounds twice in double (ROUND to 1 decimal, then 12 digits), so 872.52 can
    # print 872 here where a 12-digit Prime stores 873 to begin with
    return abs(f - v) <= 0.5 * 10 ** (-nd) + 10 ** (math.floor(math.log10(abs(v))) - 11) * (1 + 1e-9)


bad_n, bad_o = [], []
for v in VALS:
    s = hn_.call('slNum', float(v))
    if not nm_ok(v, s):
        bad_n.append((v, s))
    so = ho_.call('slNum', float(v))
    if not nm_ok(v, so):
        bad_o.append((v, so))
ck(not bad_n, 'D3 slNum over %d values (1E-7 .. 1E12, both signs; whole numbers from 1E9 with trailing zeros): '
   'beta 2c never loses a digit, no trailing zero after "." %s' % (len(VALS), bad_n[:5]))
ck(len(bad_o) > 100 and all(abs(v) >= 1e11 for v, _s in bad_o),
   'D3 beta 2b fails only from 1E11 up, where the 12-digit text has no "." (%d of %d): %s' % (len(bad_o), len(VALS), bad_o[:3]))
say('  D3 %d values: beta 2c 0 wrong; beta 2b %d wrong, every one 1E11 or more (its 12-digit text ends in 0), e.g. %s'
    % (len(VALS), len(bad_o), bad_o[:2]))
ck(not hn_.sci_strings or all(abs(q[0]) >= 1e12 for q in hn_.sci_strings), 'D3 no scientific form below 1E12')

# D4: the review's own check, its SRC pointed at each version
_rv = open('/home/claude/work/review/check_ScatterLab.py', encoding='utf-8').read()
_rv_out = {}
for path in (PROG, B2B):
    _t = _rv.replace("'/home/claude/work/review/fleet/ScatterLab_beta2b.txt'", repr(path))
    cp_ = subprocess.run([sys.executable, '-c', _t], capture_output=True, text=True, cwd='/home/claude/work/review')
    _rv_out[path] = cp_.stdout + cp_.stderr
_tail = lambda s: [l for l in s.split('\n') if l.strip().startswith(('590 checks', 'FAIL'))]  # noqa: E731
ck(_tail(_rv_out[PROG]) == ['590 checks, 0 failures'],
   'D4 the review\'s check_ScatterLab.py on beta 2c: %s' % _tail(_rv_out[PROG]))
ck(_tail(_rv_out[B2B]) == ['590 checks, 3 failures', "  FAIL slNum(1.4e+11) = '140000000000'",
                            "  FAIL slNum(1.23457e+11) = '123456789000'", '  FAIL decimal page shows 140000000000 b'],
   'D4 the same check on beta 2b: the three slNum failures: %s' % _tail(_rv_out[B2B]))
say('  D4 review check_ScatterLab.py: beta 2c "%s"; beta 2b "%s"' % (_tail(_rv_out[PROG])[0], _tail(_rv_out[B2B])[0]))

# D5: n < 3 is still refused (D16 open)
for path in (PROG, B2B):
    for xs, ys in (([1, 2], [3, 5]), ([4], [4]), ([3, 3, 3], [1, 2, 3])):
        hh = load(xs, ys, cas='fail') if path == PROG else None
        if hh is None:
            hh = Harness(path, strict=True, cas='fail'); hh.call('slInit')
            g = hh.globals_
            for i in range(40):
                g['slX'][i] = float(xs[i]) if i < len(xs) else 0.0
                g['slY'][i] = float(ys[i]) if i < len(ys) else 0.0
            g['slN'] = float(len(xs)); hh.call('slAutoWin'); hh.call('slFit')
        hh.reset_records(); hh.call('slDraw')
        note = [t.text for t in hh.texts if t.text.startswith('Need at least')]
        ck(hh.globals_['slOK'] == 0 and note == ['Need at least 3 points with different x.']
           and hh.globals_['SL_B1'] == 0,
           'D5 %s, %s: no line (slOK 0, SL_B1 0), the note says why' % (os.path.basename(path), xs))
say('  D5 two points, one point, three equal x: no line and the note, in beta 2c as in beta 2b')

# G2c: beta 2c against beta 2b
_t2b, _t2c = open(B2B, encoding='utf-8').read(), open(PROG, encoding='utf-8').read()
_Q0, _Q1 = raw_bodies(_t2b), raw_bodies(_t2c)
_dq = sorted(n for n in set(_Q0) | set(_Q1) if _Q0.get(n) != _Q1.get(n))
ck(_dq == ['slNum'] and set(_Q0) == set(_Q1), 'G2c routines that differ from beta 2b (comments included): %s' % _dq)
_code_l = lambda t: [l.strip() for l in strip_comments(t).split('\n') if l.strip()]  # noqa: E731
import difflib  # noqa: E402
_nd = list(difflib.ndiff(_code_l(_Q0['slNum']), _code_l(_Q1['slNum'])))
_rem = [l[2:] for l in _nd if l.startswith('- ')]
_add = [l[2:] for l in _nd if l.startswith('+ ')]
ck(_rem == [] and sorted(_add) == sorted(['IF DIM(nmS) > 0 THEN', 'IF INSTRING(nmS, ".") > 0 THEN', 'END;', 'END;']),
   'G2c slNum: the zero strip is only wrapped in the DIM and INSTRING guards (removed %s, added %s)' % (_rem, _add))
ck(_outside(_t2b, ['slNum']) == _outside(_t2c, ['slNum']), 'G2c outside slNum only comments differ (the header)')
ck(all(ord(c) < 128 for c in _t2c), 'G2c the file is still pure ASCII')
ck(re.search(r'(?m)^// SCATTERLAB - beta 2c$', _t2c) is not None and 'What changed in beta 2c (19 Oct 2026)' in _t2c
   and 'Beta 2c (below) has run only in the PC harness' in _t2c and 'beta 2' not in strip_comments(_t2c),
   'G2c banner, status lines and header say beta 2c; no code line names a version')
_loc2 = [l for l in _code_l(_t2c) if l.startswith('LOCAL ')]
ck(all(len([x for x in l[6:].rstrip(';').split(',') if x.strip()]) <= 6 for l in _loc2), 'G2c every LOCAL line <= 6 names')

# Roger's addition (19 Oct 2026, 12:48): the DISCLAIMER beside the terms of use, a comment only
_hdr = ' '.join(l[2:].strip() for l in _t2c.split('\n')[:40] if l.startswith('//'))
_terms_at = _hdr.find('FREE FOR EDUCATIONAL AND PERSONAL USE')
_disc_at = _hdr.find('DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes.')
ck(_terms_at >= 0 and _disc_at > _terms_at and _disc_at - _terms_at < 400,
      'disclaimer: the exact sentence sits in the header right after the terms of use (%d, %d)' % (_terms_at, _disc_at))
_strs = re.findall(r'"([^"\n]*)"', re.sub(r'//[^\n]*', '', _t2c))
ck(not any('EDUCATIONAL' in x.upper() or 'warranty' in x for x in _strs),
      'disclaimer: no page states the terms of use, so no page needed the short line')
say('  G2c only slNum differs: the strip wrapped in IF DIM(nmS) > 0 / IF INSTRING(nmS, ".") > 0; pure ASCII')

# ---- R10: every scientific STRING result of every beta 2b run in this script ----
sci_new = [(nm, q) for nm, hh in ALL_RUNS if nm == os.path.basename(PROG) for q in hh.sci_strings]
sci_old = sorted({(q[2], nm) for nm, hh in ALL_RUNS if nm != os.path.basename(PROG) for q in hh.sci_strings})
small = [(nm, q) for nm, q in sci_new if abs(q[0]) < 1]
big = sorted({q[2] for _nm, q in sci_new if abs(q[0]) >= 1e12})
ck(not small and all(abs(q[0]) >= 1e12 and q[1] == 5 for _nm, q in sci_new),
   'R10 h.sci_strings over all %d beta 2c runs: %d small (must be 0); from 1E12 up only slNum\'s six significant '
   'digits on the decimal page: %s' % (sum(1 for nm, _h in ALL_RUNS if nm == os.path.basename(PROG)), len(small), big))
say('  beta 2c sci_strings (every run): %s' % ([q[2] for _nm, q in sci_new] or 'none'))
say('  the older versions\' sci_strings in this script (%d distinct): %s' % (len(sci_old), [r for r, _nm in sci_old][:20]))

print('\n%d failure(s)' % len(FAILS))
sys.exit(1 if FAILS else 0)
