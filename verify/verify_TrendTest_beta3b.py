#!/usr/bin/env python3
"""verify_TrendTest_beta3b.py -- TrendTest beta 3b (17 Oct 2026): the Examples lines shortened (the emulator
cut "(made up" at the box's edge) and solid dots (GfxProbe beta 1 T09: ARC_P rings leave diagonal holes).
Built from verify_TrendTest_beta3a.py; every check is kept and now runs in harness v3c.  New checks (3b):
  every CHOOSE line is at most 30 characters, and the examples still load the same data; trDot is three
  RECT_P bars covering exactly a radius-3 disc, and no ARC_P of radius 3 or less is drawn except the
  hollow reference circle; beta 3b against beta 3a: only trDot and trExamples differ.
(The beta 3a description follows; "v3b" there now means v3c.)

verify_TrendTest_beta3a.py -- checks for TrendTest beta 3a (17 Oct 2026): the CAS call form that
CASProbe beta 1b found on the emulator.  Built from verify_TrendTest_beta3.py: every check is kept;
Part B runs in harness v3b, which models the calculator's CAS (CAS of a variable unevaluated, the
Prime's printing -- the solve of a system in braces, {[a,b]} -- a CAS string as a PPL string);
Part G (new) runs beta 3 itself in v3b and compares beta 3a with beta 3.  New checks are marked "3a".

The beta 3 checks: TrendTest beta 3's "least squares as calculus"
page (16 Oct 2026).

The program's line is the weighted least-squares line of p_i = a_i/n_i on the score x_i
with weights n_i: it minimises SSE(a, b) = sum n_i (p_i - a - b x_i)^2.  Page 4 has the CAS
write that SSE out for the table (every number exact: whole numbers, or whole numbers over
a power of ten), put it in order, differentiate it in a and in b, and solve the two normal
equations.  This script checks every piece.

Part A  the CAS templates in desktop Giac (giac_eval: a .giac file run by icas), for 13
        tables -- the three examples, each with the three score sets (as entered, 1,2,3...,
        midranks: halves), scores with up to three decimals, negative scores, two levels with
        the same proportion, a zero cell, k = 2, six levels with large prime totals -- against
          * Python fractions: the exact solution of the normal equations;
          * SymPy: the expanded weighted SSE and its two partial derivatives (the Giac answer
            minus SymPy's must simplify to 0);
          * statsmodels WLS(p, [1, x], weights = n) and OLS on all N individual 0/1 outcomes
            (both must equal the exact a, b to 1e-10).
        A table whose score needs more than six decimals (1/3) must produce no CAS text.
Part B  the PPL program in the run harness v3:
          * trCxMake's SSE text = this script's, character for character; its parsed a and b
            = the exact fractions; trB, trA0 (the program's decimals) = the fractions to 1e-12;
          * page 4 end to end with cas='giac' (badge, the SSE, both derivatives, both
            fractions beside the decimals, the "16985/10" note for midranks) and cas='fail'
            (decimal badge, the normal equations with the program's sums, no error);
          * the cache: page 4 twice costs 4 CAS calls, not 8; the Scores key on page 4 asks
            again; a drag on plot 1 makes no CAS call, and page 4 afterwards shows the
            dragged table's exact line; Restore brings the first answer back;
          * a 1/3 score: the decimal page, no CAS call; the stale-key run through the menu.

Run:  python3 verify_TrendTest_beta3b.py      (exit status 0 = every check passed)
Roger Metcalf / Claude, 16 Oct 2026.
"""
import os
import re
import sys
from fractions import Fraction as Fr

import numpy as np
import statsmodels.api as sm
import sympy as sp

sys.path.insert(0, '/home/claude/work/out')
from ppl_run_v3c import Harness, giac_eval, prime_print  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.join(HERE, 'TrendTest_beta3b.txt')
B3A = os.path.join(HERE, 'TrendTest_beta3a.txt')
BETA3 = os.path.join(HERE, 'TrendTest_beta3.txt')
FAILS = []


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('   ' + detail if detail else ''))
    if not ok:
        FAILS.append(name)


# ------------------------------------------------------------ the program's text, in Python
def istr(n):
    v = int(round(abs(n)))
    return ('-' if n < 0 and v else '') + str(v)


def rat(v):
    """trRat: exact CAS text for a number, or '' (more than six decimals)."""
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
    t = rat(v)
    return Fr(t.strip('()')) if t else None


def sse_text(x, a, n):
    """trCxMake's SSE: n1*(a1/n1-tra-trb*x1)^2+..."""
    parts = []
    for xi, ai, ni in zip(x, a, n):
        cx, ca, cn = rat(xi), rat(ai), rat(ni)
        if not (cx and ca and cn):
            return ''
        parts.append(cn + '*(' + ca + '/' + cn + '-tra-trb*' + cx + ')^2')
    return '+'.join(parts)


def midranks(n):
    out, c = [], 0
    for ni in n:
        out.append(c + (ni + 1) / 2.0)
        c += ni
    return out


def scores(x, n, mode):
    return list(map(float, x)) if mode == 0 else ([float(i + 1) for i in range(len(x))] if mode == 1 else midranks(n))


def exact_line(x, a, n):
    """the weighted normal equations, solved in fractions: (a0, b)"""
    X = [ratfrac(v) for v in x]
    A = [Fr(int(v)) for v in a]
    N = [Fr(int(v)) for v in n]
    sN, sA = sum(N), sum(A)
    sx = sum(ni * xi for ni, xi in zip(N, X))
    sxx = sum(ni * xi * xi for ni, xi in zip(N, X))
    sxa = sum(xi * ai for xi, ai in zip(X, A))
    b = (sN * sxa - sx * sA) / (sN * sxx - sx * sx)
    return (sA - b * sx) / sN, b


TA, TB = sp.symbols('tra trb')


def sympy_sse(x, a, n):
    return sp.expand(sum(sp.Integer(int(ni)) * (sp.Rational(int(ai), int(ni)) - TA - TB * sp.Rational(ratfrac(xi)))**2
                         for xi, ai, ni in zip(x, a, n)))


def parse_giac(t):
    return sp.sympify(t.replace('^', '**'), locals={'tra': TA, 'trb': TB})


def parse_sol(t):
    s = t.replace('list', '')
    for c in '[]{} ':
        s = s.replace(c, '')
    parts = re.split('[,;]', s)
    if len(parts) != 2:
        return None
    return tuple(Fr(p.split('=')[-1]) for p in parts)


EXAMPLES = [
    ('snoring', [0, 2, 4, 5], [24, 35, 21, 30], [1379, 638, 213, 254]),
    ('sleep U (made up)', [5, 6, 7, 8, 9], [38, 40, 36, 44, 44], [160, 320, 480, 320, 160]),
    ('convictions (made up)', [0, 1, 2, 3], [72, 66, 51, 88], [400, 240, 150, 200]),
]
TABLES = []
for nm, x, a, n in EXAMPLES:
    for mode, mn in ((0, 'as entered'), (1, '1,2,3'), (2, 'midranks')):
        TABLES.append(('%s, %s' % (nm, mn), scores(x, n, mode), a, n))
TABLES += [
    ('scores with decimals 0.5, 1.25, 2.125, 4', [0.5, 1.25, 2.125, 4.0], [10, 15, 22, 30], [50, 60, 55, 50]),
    ('negative scores -2 .. 2', [-2.0, -1.0, 0.0, 1.0, 2.0], [5, 9, 14, 20, 27], [60, 61, 62, 63, 64]),
    ('two levels with the same p (ties)', [1.0, 2.0, 3.0], [10, 10, 20], [100, 100, 100]),
    ('a zero cell', [1.0, 2.0, 3.0], [0, 5, 10], [20, 20, 20]),
    ('two levels', [1.0, 2.0], [12, 30], [100, 100]),
    ('six levels, large prime totals', [1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [101, 131, 163, 197, 211, 251],
     [1009, 1013, 1019, 1021, 1031, 1033]),
]

# ============================================================ Part A
print('==== Part A: the CAS templates in desktop Giac, against fractions, SymPy and statsmodels ====')
GI = {}
for nm, x, a, n in TABLES:
    E = sse_text(x, a, n)
    ex_a, ex_b = exact_line(x, a, n)
    g_sse = giac_eval('normal(' + E + ')')
    g_da = giac_eval('normal(diff(' + E + ',tra))')
    g_db = giac_eval('normal(diff(' + E + ',trb))')
    g_sol = giac_eval('solve([diff(' + E + ',tra)=0,diff(' + E + ',trb)=0],[tra,trb])')
    GI[E] = (g_sse, g_da, g_db, g_sol)
    S = sympy_sse(x, a, n)
    ok_sse = sp.simplify(parse_giac(g_sse) - S) == 0
    ok_d = sp.simplify(parse_giac(g_da) - sp.diff(S, TA)) == 0 and sp.simplify(parse_giac(g_db) - sp.diff(S, TB)) == 0
    sol = parse_sol(g_sol)
    ok_sol = sol == (ex_a, ex_b)
    p = np.array(a, float) / np.array(n, float)
    X = sm.add_constant(np.array(x, float))
    w = sm.WLS(p, X, weights=np.array(n, float)).fit().params
    xi = np.repeat(np.array(x, float), np.array(n, int))
    yi = np.concatenate([np.r_[np.ones(ai), np.zeros(ni - ai)] for ai, ni in zip(a, n)])
    o = sm.OLS(yi, sm.add_constant(xi)).fit().params
    ok_sm = all(abs(u - float(v)) <= 1e-10 * max(1, abs(float(v))) for u, v in zip(w, (ex_a, ex_b))) and \
        all(abs(u - float(v)) <= 1e-10 * max(1, abs(float(v))) for u, v in zip(o, (ex_a, ex_b)))
    check('%-44s SSE %s, d/da d/db %s, solve %s, WLS = OLS(0/1) = exact %s' % (
        nm, 'ok' if ok_sse else 'NO', 'ok' if ok_d else 'NO', 'ok' if ok_sol else 'NO', 'ok' if ok_sm else 'NO'),
        ok_sse and ok_d and ok_sol and ok_sm, 'b = %s, a = %s' % (ex_b, ex_a))
E_bad = sse_text([1 / 3, 2 / 3, 1.0], [5, 9, 14], [40, 41, 42])
check('a score of 1/3 (more than six decimals): no CAS text at all', E_bad == '')
longest = max(len(sse_text(x, a, n)) for _, x, a, n in TABLES)
check('the longest call (solve: the SSE twice) fits trCasMx = 4000', 2 * longest + 60 <= 4000,
      'SSE text up to %d characters' % longest)

# ============================================================ Part B
sol_pr = [prime_print(v[3]) for v in GI.values()]
check('3a: in the Prime\'s printing every solve answer is {[a,b]} (CASProbe T36), the SSE and its derivatives '
      'are unchanged', all(t.startswith('{[') and t.endswith(']}') for t in sol_pr)
      and all(prime_print(v[i]) == v[i] for v in GI.values() for i in (0, 1, 2)), str(sol_pr[:1]))

print('\n==== Part B: the PPL program in the harness (ppl_run_v3b) ====')


def load(x, a, n, cas='giac', mode=0, base=None):
    h = Harness(PROG, strict=True, cas=cas)
    h.call('trInit')
    g = h.globals_
    k = len(x)
    g['trK'] = float(k)
    g['trOX'] = [float(v) for v in (base or x)]
    g['trOA'] = [float(v) for v in a]
    g['trA'] = [float(v) for v in a]
    g['trTot'] = [float(v) for v in n]
    g['trScM'] = float(mode)
    g['trSel'] = 1.0
    h.call('trSetX')
    h.call('trCompute')
    return h


okt = oks = okd = True
det = []
for nm, x, a, n in TABLES:
    h = load(x, a, n)
    h.call('trCxMake')
    g = h.globals_
    E = sse_text(x, a, n)
    ex_a, ex_b = exact_line(x, a, n)
    okt = okt and g['trCxK'] == E and g['trCxE'] == GI[E][0]
    got = (Fr(g['trCxSa']), Fr(g['trCxSb'])) if g['trCxSa'] else None
    oks = oks and got == (ex_a, ex_b) and g['trCxSt'] == 1 and g['trCasOK'] == 1
    okd = okd and abs(g['trB'] - float(ex_b)) <= 1e-12 * max(1, abs(float(ex_b))) and \
        abs(g['trA0'] - float(ex_a)) <= 1e-12 * max(1, abs(float(ex_a)))
    if got != (ex_a, ex_b):
        det.append(nm)
check('trCxMake builds exactly this SSE text, %d tables' % len(TABLES), okt)
check('the PPL reads solve\'s answer: a and b = the exact fractions, every table', oks, str(det))
check('the program\'s trB, trA0 = the exact fractions to 1e-12 (the decimals beside them)', okd)

# page 4, end to end (snoring): Right x 3 from page 1, then Esc
x, a, n = EXAMPLES[0][1:]
h = load(x, a, n)
h.press('Right').press('Right').press('Right').press('Esc')
h.call('trView', 1.0)
p4 = h.pages[-1]
want = ['exact (CAS)', u'SSE = 2484×a^2+6796×a×b-220×a+12310×b^2-608×b',
        '+63080529409/7933174634', u'dSSE/da = 4968×a+6796×b-220 = 0', u'dSSE/db = 6796×a+24620×b-608 = 0',
        'b = 95339/4757909   (program 0.02003800)', 'a = 80277/4757909   (program 0.01687233)',
        '4/4, ' + u'⇆' + ' or tap = page, Esc = menu']
check('page 4 (Giac), snoring: badge, SSE, both derivatives, both fractions beside the decimals',
      all(p4.has(w) for w in want), str([t.text for t in p4.texts]))
check('page 4: four CAS calls, all answered', len(h.cas_calls) == 4 and all('Error' not in c[1] for c in h.cas_calls))
check('3a: every text asks for string(...), every answer quoted, the solve in braces; no CAS variable assigned, '
      'no CAS call of a variable', all(c[0].startswith('string(') and c[1].startswith('"') for c in h.cas_calls)
      and h.cas_calls[3][1].startswith('"{[') and not h.cas_vars and not any('non-literal' in w for w in h.warnings),
      str(h.cas_calls[3][1][:40]))
check('no text below y 206 on page 4 (the soft keys are at 218)', max(t.y for t in p4.texts) <= 206)
# twice: cached
h = load(x, a, n)
h.press('Right').press('Right').press('Right').press('Left').press('Right').press('Esc')
h.call('trView', 1.0)
check('page 4 twice: 4 CAS calls, not 8 (the answers are kept)', len(h.cas_calls) == 4, '%d' % len(h.cas_calls))
# the Scores key on page 4: midranks, with the 16985/10 note
h = load(x, a, n)
h.press('Right').press('Right').press('Right').press('Plus').press('Plus').press('Esc')
h.call('trView', 1.0)
p4 = h.pages[-1]
mx = midranks(n)
ea, eb = exact_line(mx, a, n)
check('Scores key on page 4 (twice, to midranks): asked again, exact midrank line, the note',
      len(h.cas_calls) == 12 and p4.has('b = %s   (program' % eb) and p4.has('a = %s   (program' % ea)
      and p4.has('Exact: score 1698.5 = 16985/10; nothing rounded.'), str([t.text for t in p4.texts][-6:]))
# a failing CAS
h = load(x, a, n, cas='fail')
h.press('Right').press('Right').press('Right').press('Esc')
r = h.call('trView', 1.0)
p4 = h.pages[-1]
want = ['decimal', 'The CAS did not answer: no exact fractions.', 'N a + (sum n x) b = A', '  2484 a + 3398 b = 110',
        '(sum n x) a + (sum n x^2) b = sum x a', '  3398 a + 12310 b = 304', '  b = 0.02003800,  a = 0.01687233']
check('cas=fail: decimal badge, the normal equations with the program\'s sums, no error',
      all(p4.has(w) for w in want) and not p4.has('exact (CAS)') and h.error is None, str([t.text for t in p4.texts]))
# a drag on plot 1 makes no CAS call; page 4 afterwards shows the dragged table's line; Restore
h = load(x, a, n)
h.press('Right').press('Right').press('Right')         # page 4: 4 calls
h.press('Minus')                                        # - from a results page: the proportions plot
h.press('Esc')
h.call('trView', 1.0)
n0 = len(h.cas_calls)
dx, dy = h.globals_['trDX'], h.globals_['trDY']
h2 = load(x, a, n)
h2.press('Right').press('Right').press('Right').press('Minus')
h2.drag([(dx[2], dy[2]), (dx[2], dy[2] + 12), (dx[2], dy[2] + 24), (dx[2], dy[2] + 36)])
calls_before_page = None
h2.press('Esc')
h2.call('trView', 1.0)
calls_drag = len(h2.cas_calls)
a2 = [int(v) for v in h2.globals_['trA']]
check('a drag on plot 1 (level 3 down): counts changed, NO CAS call during it', a2 != a and calls_drag == 4,
      'cases %s, %d calls' % (a2, calls_drag))
h3 = load(x, a2, n, base=x)
h3.globals_['trOA'] = [float(v) for v in a]
h3.globals_['trEdit'] = 1.0
h3.press('Right').press('Right').press('Right').press('Esc')
h3.call('trView', 1.0)
ea2, eb2 = exact_line(x, a2, n)
check('page 4 after the drag: the dragged table\'s exact line', h3.pages[-1].has('b = %s   (program' % eb2),
      str([t.text for t in h3.pages[-1].texts if t.text.startswith('b ')]))
h3.reset_records()
h3.press('Zero').press('Esc')                            # 0 = Restore, on page 4
h3.call('trView', 6.0)
check('Restore on page 4: the first table\'s line again', h3.pages[-1].has('b = 95339/4757909'))
# a 1/3 score
h = load([1 / 3, 2 / 3, 1.0], [5, 9, 14], [40, 41, 42])
h.press('Right').press('Right').press('Right').press('Esc')
h.call('trView', 1.0)
check('a score of 1/3: "needs over 6 decimals", the decimal page, no CAS call',
      h.pages[-1].has('A value needs over 6 decimals: no exact fractions.') and len(h.cas_calls) == 0)
# stale-key run through the menu: Examples -> snoring -> results -> page 4 -> menu -> quit
h = Harness(PROG, strict=False, stale_keys=True, idle_key=4)
h.choose(5).choose(1)
h.press('Right').press('Right').press('Right').press('Enter')
h.choose(7)
r = h.call('TrendTest')
check('stale-key run: menu, example, pages 1-4, Enter on page 4 = menu, quit; nothing skipped',
      not h.stale_skips and isinstance(r, str) and r.startswith('TrendTest: X2 trend = 72.6588'),
      'result %r, skips %r' % (r, h.stale_skips))

# G (3a): beta 3 in v3b -- the emulator's finding: its trCas hands back its own text, the solve's
# echo keeps "tra" in it, and page 4 falls back to the decimals
x, a, n = EXAMPLES[0][1:]
h = Harness(BETA3, strict=True, cas='giac')
h.call('trInit')
g = h.globals_
g['trK'] = float(len(x)); g['trOX'] = [float(v) for v in x]; g['trOA'] = [float(v) for v in a]
g['trA'] = [float(v) for v in a]; g['trTot'] = [float(v) for v in n]; g['trScM'] = 0.0; g['trSel'] = 1.0
h.call('trSetX'); h.call('trCompute')
h.press('Right').press('Right').press('Right').press('Esc')
h.call('trView', 1.0)
check('3a: beta 3 in v3b: page 4 says "decimal" and gives no fractions -- the emulator\'s finding',
      h.pages[-1].has('decimal') and not h.pages[-1].has('exact (CAS)') and any('non-literal' in w for w in h.warnings))
say = print
_saved_check = check


def _check2(cond, msg):
    _saved_check(msg, cond)


check = _check2

# ================================================================ G (round 2a)
say('\nG. beta 3b against beta 3a')
import re as _re
_b_old = open(B3A, encoding='utf-8').read()
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
check(_diff == ['trDot', 'trExamples'], 'beta 3b: routines that differ from beta 3a: %s (want trDot, trExamples)' % _diff)


def _outside(t, names):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\n]*', '', t))
    if names:
        c = _re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
    return _re.sub(r'\s+', ' ', c)


check(_outside(_b_old, _diff) == _outside(_b_new, _diff), 'beta 3b: outside those routines only comments differ')
_py0 = _re.findall(r'(?s)#PYTHON.*?#END', _b_old)
_py1 = _re.findall(r'(?s)#PYTHON.*?#END', _b_new)
check(_py0 == _py1, 'beta 3b: the #PYTHON blocks are unchanged')
say('  routines that differ from beta 3a: %s; everything else differs only in comments' % ', '.join(_diff))

check = _saved_check


# ================================================================ W (3b)
say('\nW. 3b: the Examples lines fit; solid dots')


def ck(cond, msg):
    check(msg, cond)


seen, loaded = [], []
for ex in (1, 2, 3):
    h = Harness(PROG, strict=False, idle_key=4, cas='fail')
    h.choose(5).choose(ex)
    h.press('Esc')
    h.choose(7)
    h.call('TrendTest')
    seen += [it for c in h.chooses for it in c.items]
    loaded.append((int(h.globals_['trK']), [int(v) for v in h.globals_['trOA']], h.globals_['trLbl']))
ck(all(len(t) <= 30 for t in seen) and len(seen) > 3,
      '3b: every CHOOSE line shown is 30 characters or fewer (%d seen, longest %d)' % (len(seen), max(len(t) for t in seen)))
ck({'Sleep: a U shape (made up)', 'Prior convictions (made up)'} <= set(seen), '3b: the shortened Examples lines are shown')
ck(loaded == [(4, [24, 35, 21, 30], 'Example: snoring and heart disease'),
                 (5, [38, 40, 36, 44, 44], 'ILLUSTRATIVE (made-up counts): sleep, illness'),
                 (4, [72, 66, 51, 88], 'ILLUSTRATIVE (made up): convictions, re-arrest')],
      '3b: the three examples still load the same data and labels: %s' % loaded)
src = re.sub(r'//[^\n]*', '', open(PROG, encoding='utf-8').read())
lits = [t for m in re.finditer(r'CHOOSE\([^;]*?\);', src, re.S) for t in re.findall(r'"([^"]*)"', m.group(0))[1:]]
ck(lits and max(len(t) for t in lits) <= 30, '3b: every CHOOSE line in the source is 30 characters or fewer (longest %d)'
      % max(len(t) for t in lits))
# trDot: three RECT_P, exactly a radius-3 disc
h = Harness(PROG, strict=False, cas='fail'); h.call('trInit'); h.reset_records()
h.call('trDot', h.grobs['G1'], 50.0, 60.0, 255.0)
px = set()
for c in h.log:
    if c[0] == 'RECT_P':
        x1, y1, x2, y2 = [int(v) for v in c[1][1:5]]
        px |= {(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)}
disc = {(50 + dx, 60 + dy) for dx in range(-3, 4) for dy in range(-3, 4) if dx * dx + dy * dy <= 12.25}
ck(len(h.log) == 3 and all(c[0] == 'RECT_P' for c in h.log) and px == disc,
      '3b: trDot = three RECT_P covering exactly a radius-3 disc (%d px)' % len(px))
# the plots: no small ARC_P except the hollow reference circle (r 3, one per odds-ratio frame)
h = Harness(PROG, strict=False, idle_key=4, cas='fail')
h.choose(5).choose(1)
h.tap(26 + 53, 230)          # the OR soft key (slot 2): the odds-ratio plot
h.press('Esc'); h.press('Esc'); h.choose(7)
h.call('TrendTest')
arcs = [c[1] for c in h.log if c[0] == 'ARC_P']
small = [a for a in arcs if a[3] <= 3]
ck(any(c[0] == 'RECT_P' for c in h.log) and all(a[3] in (3, 6, 7) for a in arcs),
      '3b: the only ARC_P left are the reference circle (r 3) and the selection ring (r 6, 7): %s'
      % sorted({a[3] for a in arcs}))
ck(len(small) <= sum(1 for p in h.pages if p.func and 'OR' in str(p.func)) or len(small) <= len(h.pages),
      '3b: at most one small ARC_P (the hollow reference) per frame (%d in %d frames)' % (len(small), len(h.pages)))
say('  Examples lines seen: %s' % [t for t in seen if 'made up' in t or 'Snoring' in t][:3])

print('\n%d failure(s)' % len(FAILS))
sys.exit(1 if FAILS else 0)
