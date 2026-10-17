#!/usr/bin/env python3
"""verify_ScatterLab_beta2a.py -- checks for ScatterLab beta 2a (17 Oct 2026): the CAS call form that
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

Run:  python3 verify_ScatterLab_beta2a.py      (exit status 0 = every check passed)
Roger Metcalf / Claude, 16 Oct 2026.
"""
import os
import random
import re
import sys
from fractions import Fraction as Fr

import numpy as np
import statsmodels.api as sm
import sympy as sp

sys.path.insert(0, '/home/claude/work/harness')
from ppl_run_v3b import Harness, giac_eval, prime_print  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.join(HERE, 'ScatterLab_beta2a.txt')
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

print('\n==== Part B: the PPL program in the harness (ppl_run_v3b) ====')


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
_b_new = open(PROG, encoding='utf-8').read()


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

print('\n%d failure(s)' % len(FAILS))
sys.exit(1 if FAILS else 0)
