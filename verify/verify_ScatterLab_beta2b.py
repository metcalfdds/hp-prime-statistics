#!/usr/bin/env python3
"""verify_ScatterLab_beta2b.py -- ScatterLab beta 2b (17 Oct 2026): the second emulator round's findings.
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

Run:  python3 verify_ScatterLab_beta2b.py      (exit status 0 = every check passed)
Roger Metcalf / Claude, 16 Oct 2026 (2b: 17 Oct 2026).
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
import ppl_run_v3d  # noqa: E402
from ppl_run_v3d import Harness, giac_eval, prime_print  # noqa: E402

# 2b: every harness made in this script is remembered with its program, so part R10 can list
# every scientific STRING result of every run (h.sci_strings, harness v3d)
ALL_RUNS = []
_h_init = ppl_run_v3d.Harness.__init__


def _h_init_rec(self, *a, **k):
    _h_init(self, *a, **k)
    ALL_RUNS.append((os.path.basename(str(a[0] if a else k.get('path', '?'))), self))


ppl_run_v3d.Harness.__init__ = _h_init_rec

HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.join(HERE, 'ScatterLab_beta2b.txt')
B2A = os.path.join(HERE, 'ScatterLab_beta2a.txt')
BETA2 = os.path.join(HERE, 'ScatterLab_beta2.txt')
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
say('\nR. 2b: the second emulator round (harness v3d)')


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
    ck(okn, 'R5 canned, %s: beta 2b %s, no error; beta 2a: %s' % (
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
   'populations are checks on beta 2b only (the axis remainder does not arise in the harness either; the '
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
ck(sorted(set(ins)) == sorted({'cR', 'rnR', 'rpS', 'ccR', 'soS', 'slCxSb', 'slCxSa', 'cxX', 'cxY', '"0123456789"'}),
   'R7 INSTRING first arguments: %s' % sorted(set(ins)))
guards = [r'IF DIM\(cR\) > 0 THEN\s+IF INSTRING\(cR, "undef"\)',
          r'IF DIM\(rpO\) == 0 THEN RETURN rpT; END;',
          r'rpI := 0; IF DIM\(rpS\) > 0 THEN rpI := INSTRING\(rpS, rpO\); END;\s+WHILE',
          r'rpI := 0; IF DIM\(rpS\) > 0 THEN rpI := INSTRING\(rpS, rpO\); END;\s+END;\s+RETURN rpR \+ rpS;',
          r'IF DIM\(ccR\) == 0 THEN RETURN ""; END;\s+IF INSTRING\(ccR',
          r'IF DIM\(soS\) == 0 THEN RETURN; END;\s+soK := INSTRING\(soS',
          r'IF DIM\(slCxSa\) == 0 OR DIM\(slCxSb\) == 0 THEN [^\n]*\n\s+IF INSTRING\(slCxSa, "sl"\)',
          r'IF DIM\(cxX\) == 0 OR DIM\(cxY\) == 0 THEN',
          r'IF soK < 2 OR soK >= DIM\(soS\) THEN RETURN; END;']
ck(all(re.search(gd, code) for gd in guards),
   'R7 the guards are in place: cR (slCas), rpS and rpO (slRepl), ccR (slCxClean), soS and the halves (slCxSol); '
   'cxX, cxY are never empty (slCxMake returns first), rnR always holds a "/" (slCxMake calls slRatNote only then), '
   'slCxSb is non-empty (soK < DIM(soS)) %s' % [gd[:30] for gd in guards if not re.search(gd, code)])
say('  LEFT / MID / RIGHT calls in the code (counts and starts reviewed by hand, see the CHANGES): %d / %d / %d'
    % (len(re.findall(r'\bLEFT\(', code)), len(re.findall(r'\bMID\(', code)), len(re.findall(r'\bRIGHT\(', code))))

# ---- G (2b): beta 2b against beta 2a ----
_o, _n = open(B2A, encoding='utf-8').read(), open(PROG, encoding='utf-8').read()


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

# ---- R10: every scientific STRING result of every beta 2b run in this script ----
sci_new = [(nm, q) for nm, hh in ALL_RUNS if nm == os.path.basename(PROG) for q in hh.sci_strings]
sci_old = sorted({(q[2], nm) for nm, hh in ALL_RUNS if nm != os.path.basename(PROG) for q in hh.sci_strings})
small = [(nm, q) for nm, q in sci_new if abs(q[0]) < 1]
big = sorted({q[2] for _nm, q in sci_new if abs(q[0]) >= 1e12})
ck(not small and all(abs(q[0]) >= 1e12 and q[1] == 5 for _nm, q in sci_new),
   'R10 h.sci_strings over all %d beta 2b runs: %d small (must be 0); from 1E12 up only slNum\'s six significant '
   'digits on the decimal page: %s' % (sum(1 for nm, _h in ALL_RUNS if nm == os.path.basename(PROG)), len(small), big))
say('  beta 2b sci_strings (every run): %s' % ([q[2] for _nm, q in sci_new] or 'none'))
say('  the older versions\' sci_strings in this script (%d distinct): %s' % (len(sci_old), [r for r, _nm in sci_old][:20]))

print('\n%d failure(s)' % len(FAILS))
sys.exit(1 if FAILS else 0)
