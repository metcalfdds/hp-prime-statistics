#!/usr/bin/env python3
"""verify_TrendTest_beta3d.py -- TrendTest beta 3d (19 Oct 2026): the fleet review's TrendTest items.
Built from verify_TrendTest_beta3c.py; every check is kept and now runs in harness v3e (out/ppl_run_v3e.py;
with home_minus off, as here, it prints exactly what v3d printed).  Changed (3d):
  - The sections that compared beta 3b with 3a (G round 2a) and beta 3c with 3b (G 3c) now compare those
    files themselves, as their records; G 3d (new) compares beta 3d with beta 3c.
  - Predecessor files (beta 3c, 3b, 3a, 3) are looked for beside this script, then in its _old and
    _superseded* folders, then in /home/claude/work/out; a comparison that needs one that is not found
    prints SKIP and is not counted (review item 22: the 3c script stopped with FileNotFoundError in a
    folder holding only the current versions).
New (3d), part D, before R10 (so R10's sci_strings audit covers its runs too):
  D1 TR_P keeps its digits: with every statistics built-in rounded to the Prime's 12 significant digits,
     the snoring example's TR_P is 1.5412E-17 (= chi2.sf to 1E-10) in beta 3d and exactly 0 in beta 3c --
     the review's improvement 1 (check_TrendTest.py E1); a sweep of X2 from 1 to 300 likewise; in double
     precision 3d's trPT = chi2.sf on 200 random tables, and every displayed p string is the same as 3c's;
  D2 the trend p is computed in one place: trPT := 2 * NORMALD_CDF(0, 1, -(trX2T^0.5)) in trCompute,
     TR_P := trPT, and every display of the trend p reads trPT; no CHISQUARE_CDF(1, ...) is left;
  D3 C-T1: the header's residual sentence, and its numbers recomputed from the program's own trCompute
     (sum of squared residuals = departure - trend/(N-1): 53.1141 vs 53.1149 for the sleep example);
  D4 C-T2: help page 3 as drawn: which program prints which form, 72.688 = the program's own trend for
     snoring times N/(N-1), every line 46 characters or fewer, Mantel's form still the headline on page 1;
  D5 C-T3: the main menu's "Plot: proportions, trend line" (29) in a run, and item 3 still opens the
     proportions plot; beta 3c showed the 30-character line;
  D6 C-T4: Enter data refuses 24.5 cases or a total of 100.5 with "Cases and totals count people: whole
     numbers only." and loads nothing; whole counts and a fractional SCORE are still accepted; beta 3c
     accepted 24.5;
  D7 the review's own check_TrendTest.py run on beta 3d: every check passes except the two that test for
     what 3d changes on purpose (E2 "the three p-values are 1 - CHISQUARE_CDF", F6 "banner says beta 3c");
     on beta 3c, none fails;
  G 3d beta 3d against beta 3c: only TrendTest, trCompute, trEnter and trHelp differ, each by exactly its
     listed change; every other routine byte-identical, comments included.
(The beta 3c description follows; "v3d" there now means v3e.)

verify_TrendTest_beta3c.py -- TrendTest beta 3c (17 Oct 2026): the second emulator round's findings.
Built from verify_TrendTest_beta3b.py; every check is kept and now runs in harness v3d, which raises
"Invalid input" for INSTRING("", ...) and prints STRING(x, 2, d) in scientific form when 0 < |x| < 10^-d,
as the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09) did on 17 Oct 2026.  New checks (part R):
  R1  trRepl directly: a pattern at the end, at the start, the whole text, an empty pattern, an empty
      text (beta 3b's trRepl stops on the first two that empty the text, in v3d);
  R2  trCas, trCxClean and trCxSol on "" and on empty answers: no error;
  R3  page 4 opens with the CAS answering (Examples > Snoring > Right x 3), exact (CAS); beta 3b stops
      the same run with the INSTRING error -- the emulator's finding;
  R4  cas='fail' end to end: page 4 shows "decimal", no error; beta 3b fails the same run;
  R5  canned answers: an empty solve ({}), "tra=" with nothing after it, an empty string: no error;
  R6  the proportions plot readout for snoring level 1: "(+0.1 SE)"; beta 3b "(+9.6E-2 SE)" (the E a
      small capital), the emulator's line;
  R7  Help: Esc leaves from page 1 and page 2, the footers say so; beta 3b turned the page;
  R8  six tables built to give small numbers (small doses, a dragged extreme, a rare outcome, an almost
      flat table, midranks on a million people, 1/3 scores that cancel), run through every page, both
      plots, the Scores key and Quit: beta 3c prints no scientific number; beta 3b's are listed;
  R9  static: every STRING(x, 2, d) left with d > 0 is one of the justified sites; every INSTRING's
      first argument is guarded or cannot be empty;
  R10 h.sci_strings from EVERY harness run of beta 3c in this script: empty;
  G   beta 3c against beta 3b: the routines that differ are exactly the ones in the CHANGES; every
      other routine is byte-identical, comments included; trCas differs only by the DIM guard.
(The beta 3b description follows; "v3c" there now means v3d.)

verify_TrendTest_beta3b.py -- TrendTest beta 3b (17 Oct 2026): the Examples lines shortened (the emulator
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

Run:  python3 verify_TrendTest_beta3d.py      (exit status 0 = every check passed)
Roger Metcalf / Claude, 16 Oct 2026 (3c: 17 Oct 2026; 3d: 19 Oct 2026).
"""
import os
import re
import sys
from fractions import Fraction as Fr

import numpy as np
import statsmodels.api as sm
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('VERIFY_PRED_DIR', '/home/claude/work/out')   # 3d: where older versions are looked for last
# 3d: harness v3e (the brief's), beside this script or in /home/claude/work/out
for _d in (HERE, OUT, '/home/claude/work/out'):
    if os.path.exists(os.path.join(_d, 'ppl_run_v3e.py')):
        sys.path.insert(0, _d)
        break
import ppl_run_v3e  # noqa: E402
from ppl_run_v3e import Harness, giac_eval, prime_print  # noqa: E402

# 3c: every harness made in this script is remembered with its program, so part R10 can list
# every scientific STRING result of every run (h.sci_strings, harness v3d; 3d: v3e)
ALL_RUNS = []
_h_init = ppl_run_v3e.Harness.__init__


def _h_init_rec(self, *a, **k):
    _h_init(self, *a, **k)
    ALL_RUNS.append((os.path.basename(str(a[0] if a else k.get('path', '?'))), self))


ppl_run_v3e.Harness.__init__ = _h_init_rec

PROG = os.path.join(HERE, 'TrendTest_beta3d.txt')


def find_pred(name):
    """3d: a predecessor file.  Beside this script first, then in its _old folder and any _superseded*
    folder, then in /home/claude/work/out.  None if absent: the comparisons that need it print SKIP."""
    import glob as _glob
    places = [HERE, os.path.join(HERE, '_old')] + sorted(_glob.glob(os.path.join(HERE, '_superseded*'))) + [OUT]
    for d in places:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return None


B3C = find_pred('TrendTest_beta3c.txt')
B3B = find_pred('TrendTest_beta3b.txt')
B3A = find_pred('TrendTest_beta3a.txt')
BETA3 = find_pred('TrendTest_beta3.txt')
SKIPS = []


def skip(what):
    SKIPS.append(what)
    print('SKIP ' + what)


FAILS = []


NCHK = [0]          # 3d: the checks are counted


def check(name, ok, detail=''):
    NCHK[0] += 1
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

print('\n==== Part B: the PPL program in the harness (ppl_run_v3d) ====')


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
if BETA3 is None:
    skip('G (3a): TrendTest_beta3.txt not found')
else:
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


def _bodies(txt):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)
    c = _re.sub(r'//[^\n]*', '', c)
    out = {}
    for m in _re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, _re.S):
        out[m.group(1)] = _re.sub(r'[ \t]+\n', '\n', m.group(0))
    return out




def _outside(t, names):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\n]*', '', t))
    if names:
        c = _re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
    return _re.sub(r'\s+', ' ', c)


if B3A is None or B3B is None:
    skip('G (round 2a): TrendTest_beta3a.txt or TrendTest_beta3b.txt not found')
else:
    _b_old = open(B3A, encoding='utf-8').read()
    _b_new = open(B3B, encoding='utf-8').read()        # 3c: this section is the 3b-vs-3a record
    _B0, _B1 = _bodies(_b_old), _bodies(_b_new)
    _diff = sorted(n for n in set(_B0) | set(_B1) if _B0.get(n) != _B1.get(n))
    check(_diff == ['trDot', 'trExamples'], 'beta 3b: routines that differ from beta 3a: %s (want trDot, trExamples)' % _diff)
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


# ================================================================ R (3c): the second emulator round
say('\nR. 3c: the second emulator round (harness v3d)')


def err_of(fn):
    """Run fn(); return None, or 'ErrorType: message' if it raised."""
    try:
        fn()
        return None
    except Exception as e:                                   # noqa: BLE001
        return '%s: %s' % (type(e).__name__, str(e)[:90])


def is_instring_err(e):
    return bool(e) and 'INSTRING: Invalid input' in e


# ---- R1: trRepl directly ----
RCASES = [('{[1,2]}', '}', '', '{[1,2]', 'the pattern at the END (solve\'s closing brace)'),
          ('{[1,2]}', '{', '', '[1,2]}', 'the pattern at the START'),
          ('abc', 'abc', '', '', 'the pattern is the WHOLE text'),
          ('abc', 'abc', 'xyz', 'xyz', 'the whole text, replaced'),
          ('abc', '', 'X', 'abc', 'an EMPTY pattern: the text unchanged (no endless loop)'),
          ('', 'a', 'b', '', 'an EMPTY text'),
          ('tra*trb*tra', 'tra', 'a', 'a*trb*a', 'twice, at both ends'),
          ('2*a*b', '*', u'×', u'2×a×b', 'in the middle, twice'),
          ('}}}', '}', '', '', 'only the pattern, three times')]
h = Harness(PROG, strict=True, cas='fail'); h.call('trInit')
for t, o, nw, want, what in RCASES:
    got, e = None, None
    try:
        got = h.call('trRepl', t, o, nw)
    except Exception as ex:                                  # noqa: BLE001
        e = str(ex)[:80]
    ck(e is None and got == want, 'R1 trRepl(%r, %r, %r) = %r: %s' % (t, o, nw, got if e is None else e, what))
if B3B is None:
    skip('R1: beta 3b not found')
else:
    ho = Harness(B3B, strict=True, cas='fail'); ho.call('trInit')
    # (beta 3b's trRepl is not given the empty pattern: INSTRING(s, "") = 1, so it would never stop)
    old_r1 = [(t, o, err_of(lambda t=t, o=o, nw=nw: ho.call('trRepl', t, o, nw)))
              for t, o, nw, _w, _x in (RCASES[0], RCASES[2], RCASES[5], RCASES[8])]
    ok_start = err_of(lambda: ho.call('trRepl', '{[1,2]}', '{', '')) is None
    ck(all(is_instring_err(e) for _t, _o, e in old_r1) and ok_start,
       'R1 beta 3b in v3d: its trRepl stops with the INSTRING error whenever the text runs out -- the pattern at '
       'the end, the whole text, an empty text, only the pattern (%s); a pattern at the start works -- the '
       'emulator\'s page-4 crash' % [(t, o) for t, o, _e in old_r1])

# ---- R2: trCas, trCxClean, trCxSol on empty answers ----
h = Harness(PROG, strict=True, cas='fail'); h.call('trInit')
r_cas = h.call('trCas', 'normal(1+1)')
ck(r_cas == '' and h.error is None, 'R2 trCas with the CAS failing: "" and no error (got %r)' % r_cas)
ck(h.call('trCxClean', '') == '', 'R2 trCxClean("") = "" (no INSTRING on the empty text)')
sols = [('', ('', '')), ('{}', ('', '')), ('[]', ('', '')), ('{[]}', ('', '')),
        ('{[tra=,trb=1/2]}', ('', '')), ('{[1/2,trb=]}', ('', '')), ('{[1/2,3/4]}', ('1/2', '3/4')),
        ('[tra=1/2,trb=3/4]', ('1/2', '3/4')), ('list[[5/7,-2/9]]', ('5/7', '-2/9')),
        ('{[1/2,3/4],[5/6,7/8]}', ('', ''))]
bad = []
for s, want in sols:
    e = err_of(lambda s=s: h.call('trCxSol', s))
    got = (h.globals_['trCxSa'], h.globals_['trCxSb'])
    if e or got != want:
        bad.append((s, got, e))
ck(not bad, 'R2 trCxSol on %d answers (empty, {}, [], "tra=" with nothing after it, two solutions, the Prime\'s '
   'and Giac\'s forms): the right halves, no error %s' % (len(sols), bad))
if B3B is None:
    skip('R2: beta 3b not found')
else:
    ho = Harness(B3B, strict=True, cas='fail'); ho.call('trInit')
    e_old = err_of(lambda: ho.call('trCas', 'normal(1+1)'))
    ck(is_instring_err(e_old), 'R2 beta 3b in v3d: trCas with the CAS failing stops (%s) -- every fallback was broken' % e_old)

# ---- R3, R4: page 4 end to end, Examples > Snoring > Right x 3, with the CAS and without ----
for mode in ('giac', 'fail'):
    def page4_run(path, mode=mode):
        hh = Harness(path, strict=True, cas=mode)
        hh.choose(5).choose(1)
        hh.press('Right').press('Right').press('Right').press('Esc')
        hh.choose(7)
        e = err_of(lambda: hh.call('TrendTest'))
        pg = [p for p in hh.pages if p.has('Least squares as calculus')]
        return hh, e, (pg[-1] if pg else None)
    hn, en, pn = page4_run(PROG)
    ho, eo, po = page4_run(B3B) if B3B is not None else (None, None, None)
    if mode == 'giac':
        want = ['exact (CAS)', 'b = 95339/4757909   (program 0.02003800)', 'a = 80277/4757909   (program 0.01687233)',
                u'dSSE/da = 4968×a+6796×b-220 = 0']
        ck(en is None and pn is not None and all(pn.has(w) for w in want) and len(hn.cas_calls) == 4
           and isinstance(hn.result, str) and hn.result.startswith('TrendTest: X2 trend = 72.6588'),
           'R3 Snoring, results page 4 with the CAS: opens, "exact (CAS)", b = 95339/4757909, a = 80277/4757909, '
           'quit returns the summary (%s)' % en)
        if ho is None:
            skip('R3: beta 3b not found')
        else:
            ck(is_instring_err(eo) and po is None and len(ho.cas_calls) == 4,
               'R3 beta 3b, the same run in v3d: the CAS answers all 4 calls, then "%s" -- the emulator\'s finding'
               % (eo or '')[:60])
    else:
        want = ['decimal', 'The CAS did not answer: no exact fractions.', '  2484 a + 3398 b = 110',
                '  b = 0.02003800,  a = 0.01687233']
        ck(en is None and pn is not None and all(pn.has(w) for w in want) and not pn.has('exact (CAS)'),
           'R4 cas=fail: page 4 shows "decimal" and the normal equations, no error (%s)' % en)
        if ho is None:
            skip('R4: beta 3b not found')
        else:
            ck(is_instring_err(eo), 'R4 beta 3b, the same cas=fail run in v3d: stops (%s)' % (eo or '')[:60])

# ---- R5: canned answers: an empty solve, "tra=", empty strings ----
x, a, n = EXAMPLES[0][1:]
E = sse_text(x, a, n)
CALLS = ['normal(' + E + ')', 'normal(diff(' + E + ',tra))', 'normal(diff(' + E + ',trb))',
         'solve([diff(' + E + ',tra)=0,diff(' + E + ',trb)=0],[tra,trb])']
good = ['"' + prime_print(v) + '"' for v in GI[E]]
for label, answers, exact in (('solve gives {} (no solution)', good[:3] + ['"{}"'], False),
                              ('solve gives {[tra=,trb=1/2]}', good[:3] + ['"{[tra=,trb=1/2]}"'], False),
                              ('every answer an empty string', ['""'] * 4, False),
                              ('the Prime\'s own answers (control)', good, True)):
    canned = {'string(' + c + ')': v for c, v in zip(CALLS, answers)}
    res = []
    for path in ((PROG, B3B) if B3B is not None else (PROG,)):
        hh = load(x, a, n, cas=canned) if path == PROG else None
        if hh is None:
            hh = Harness(B3B, strict=True, cas=canned); hh.call('trInit'); g = hh.globals_
            g['trK'] = 4.0; g['trOX'] = [float(v) for v in x]; g['trOA'] = [float(v) for v in a]
            g['trA'] = [float(v) for v in a]; g['trTot'] = [float(v) for v in n]; g['trScM'] = 0.0; g['trSel'] = 1.0
            hh.call('trSetX'); hh.call('trCompute')
        hh.press('Right').press('Right').press('Right').press('Esc')
        e = err_of(lambda hh=hh: hh.call('trView', 1.0))
        pg = hh.pages[-1] if hh.pages else None
        res.append((e, pg))
    (en, pn), (eo, po) = res if len(res) == 2 else (res[0], (None, None))
    okn = en is None and pn is not None and (pn.has('exact (CAS)') if exact else (pn.has('decimal') and pn.has(
        'The CAS did not answer: no exact fractions.')))
    ck(okn, 'R5 canned, %s: beta 3d %s, no error; beta 3b: %s' % (
        label, 'the exact page' if exact else 'the decimal page',
        'not run' if B3B is None else ('runs' if eo is None else eo[:50])))

# ---- R6: the proportions plot readout, snoring level 1 ----
def plot_readout(path):
    hh = Harness(path, strict=False, idle_key=4, cas='fail')
    hh.choose(5).choose(1)
    hh.tap(26, 230)                          # Prop (slot 1): the proportions plot, level 1 selected
    hh.choose(7)                             # the idle Esc leaves the plot; then Quit
    e = err_of(lambda: hh.call('TrendTest'))
    lines = [t.text for p in hh.pages for t in p.texts if t.text.startswith('L1: x = 0')]
    return e, (lines[-1] if lines else None), hh.sci_strings
en, ln, sn = plot_readout(PROG)
ck(en is None and ln == 'L1: x = 0, 24/1379 = 0.017, line 0.017 (+0.1 SE)' and not sn,
   'R6 the proportions plot, snoring level 1: %r, no scientific form' % ln)
if B3B is None:
    skip('R6: beta 3b not found')
else:
    eo, lo, so = plot_readout(B3B)
    ck(lo == u'L1: x = 0, 24/1379 = 0.017, line 0.017 (+9.6ᴇ-2 SE)' and any(d == 1 for _v, d, _r in so),
       'R6 beta 3b, the same run: %r -- the emulator\'s line, character for character' % lo)

# ---- R7: Help, Esc ----
HELP1, HELP2, HELP3 = 'Chi-square for trend: the idea', 'Reading the plots', 'Keys, and the same test elsewhere'


def help_run(path, keys):
    hh = Harness(path, strict=False, idle_key=4, cas='fail')
    hh.choose(6)
    for kname in keys:
        hh.press(kname)
    hh.choose(7)
    e = err_of(lambda: hh.call('TrendTest'))
    shown = [p for p in hh.pages if p.has(HELP1) or p.has(HELP2) or p.has(HELP3)]
    seen_pg = [1 if p.has(HELP1) else 2 if p.has(HELP2) else 3 for p in shown]
    return e, seen_pg, shown, hh


e1, s1, sh1, h1 = help_run(PROG, ['Esc'])
e2, s2, sh2, h2 = help_run(PROG, ['Enter', 'Esc'])
e3, s3, sh3, h3 = help_run(PROG, ['Enter', 'Right', 'Plus'])
ck(e1 is None and s1 == [1] and len(h1.chooses) == 2 and h1.result == 'TrendTest: no table',
   'R7 Help, Esc on page 1: back to the menu (pages seen %s)' % s1)
ck(e2 is None and s2 == [1, 2] and len(h2.chooses) == 2, 'R7 Help, a key then Esc on page 2: back to the menu (pages seen %s)' % s2)
ck(e3 is None and s3 == [1, 2, 3] and len(h3.chooses) == 2, 'R7 Help, any keys: pages 1, 2, 3, then the menu (%s)' % s3)
foot = [[t.text for t in p.texts if t.y == 220] for p in sh3]
ck(foot == [['any key = page 2, Esc = menu'], ['any key = page 3, Esc = menu'], ['any key = menu']],
   'R7 the help footers say it: %s' % foot)
if B3B is None:
    skip('R7: beta 3b not found')
else:
    eo1, so1, _sh, _h = help_run(B3B, ['Esc'])
    ck(so1 == [1, 2, 3], 'R7 beta 3b: Esc on help page 1 turned the page (pages seen %s, the idle Esc then turns the rest) '
       '-- the emulator\'s finding' % so1)

# ---- R8: tables built to give small numbers, through every view ----


def run_path(path, x, a, n, cas='giac', page4=True):
    """Menu > Enter data, then results 1-3 (4), the proportions plot at every level, the OR plot at every
    level, Scores twice (1,2,3, then midranks), the proportions plot again, the results again, Quit."""
    hh = Harness(path, strict=False, idle_key=4, cas=cas)
    k = len(x)
    hh.choose(1).choose(k - 1)
    hh.answer([float(v) for v in x]).answer([float(v) for v in a]).answer([float(v) for v in n])
    hh.press('Right').press('Right')
    if page4:
        hh.press('Right')
    hh.press('Minus')
    for _ in range(k - 1):
        hh.press('Right')
    hh.press('Minus')
    for _ in range(k - 1):
        hh.press('Left')
    hh.press('Plus').press('Plus').press('Minus').press('Esc')
    hh.choose(2)
    hh.press('Right').press('Right')
    if page4:
        hh.press('Right')
    hh.press('Esc')
    hh.choose(7)
    e = err_of(lambda: hh.call('TrendTest'))
    return hh, e


SCEN = [('snoring (the emulator\'s table)', [0, 2, 4, 5], [24, 35, 21, 30], [1379, 638, 213, 254]),
        ('small doses 0, 0.001, 0.005, 0.01', [0, 0.001, 0.005, 0.01], [5, 8, 12, 20], [100, 100, 100, 100]),
        ('a dragged extreme: 50/50, 0/50, 0/50 (OR 0.0001)', [1, 2, 3], [50, 0, 0], [50, 50, 50]),
        ('a rare outcome: 1, 2, 3 of 20000 each', [1, 2, 3], [1, 2, 3], [20000, 20000, 20000]),
        ('almost flat: 100, 101, 100 of 1000', [1, 2, 3], [100, 101, 100], [1000, 1000, 1000]),
        ('midranks on a million people', [1, 2, 3], [2000, 3500, 6500], [200000, 300000, 500000]),
        ('scores -2/3, 1/3, 4/3 (sum n x cancels)', [-2 / 3, 1 / 3, 4 / 3], [3, 5, 2], [11, 10, 3])]
R8_OLD = {}
for nm, x, a, n in SCEN:
    hg, eg = run_path(PROG, x, a, n, 'giac')
    hf, ef = run_path(PROG, x, a, n, 'fail')
    small_new = [s for s in hg.sci_strings + hf.sci_strings if abs(s[0]) < 1]
    big_new = sorted({(s[0], s[2]) for s in hg.sci_strings + hf.sci_strings if abs(s[0]) >= 1e12})
    if B3B is not None:
        ho, eo = run_path(B3B, x, a, n, 'giac', page4=False)
        R8_OLD[nm] = sorted({(round(v, 9), d, r) for v, d, r in ho.sci_strings})
    pg4 = [p for p in hg.pages if p.has('Least squares as calculus')]
    ck(eg is None and ef is None and not small_new and len(hg.pages) > 40 and len(pg4) == 2
       and isinstance(hg.result, str) and hg.result.startswith('TrendTest: X2 trend'),
       'R8 %s: every page, both plots at every level, Scores, page 4 (CAS and cas=fail), Quit -- no error, no '
       'small number in scientific form (%d frames)%s' % (nm, len(hg.pages) + len(hf.pages),
                                                        ('; from 1E12 up: %s' % [r for _v, r in big_new]) if big_new else ''))
if B3B is None:
    skip('R8: beta 3b not found')
else:
    for nm in ('small doses 0, 0.001, 0.005, 0.01', 'a dragged extreme: 50/50, 0/50, 0/50 (OR 0.0001)',
               'a rare outcome: 1, 2, 3 of 20000 each', 'almost flat: 100, 101, 100 of 1000',
               'midranks on a million people', 'scores -2/3, 1/3, 4/3 (sum n x cancels)', 'snoring (the emulator\'s table)'):
        ck(len(R8_OLD[nm]) > 0, 'R8 beta 3b, the same run (pages 1-3 and the plots; its page 4 stops): scientific forms %s'
           % [r for _v, _d, r in R8_OLD[nm]][:6])

# ---- R9: static review ----
def strip_comments(txt):
    """Drop // comments (outside strings) and the #PYTHON blocks."""
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


src = open(PROG, encoding='utf-8').read()
code = strip_comments(src)


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
    """The top-level arguments of NAME(...), split at commas outside brackets and strings."""
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


calls = string_calls(code)
fixed_d = [c for c in calls if len(top_args(c)) == 3 and top_args(c)[1] == '2']
nonzero = sorted({c for c in fixed_d if top_args(c)[2] != '0'})
JUST = {'STRING(fxR, 2, fxD)': 'trFx: rounded first',
        'STRING(psP, 2, 4)': 'trPStr: p >= 0.0001 (below it says "< 0.0001")',
        'STRING(osV, 2, 1)': 'trOrStr: OR >= 100', 'STRING(osV, 2, 2)': 'trOrStr: OR >= 10',
        'STRING(osV, 2, 3)': 'trOrStr: OR >= 0.001 (below it says "< 0.001")',
        'STRING(xsV, 2, 1)': 'trXStr: a half, |x| >= 0.5', 'STRING(xsV, 2, 2)': 'trXStr: |x| >= 0.01',
        'STRING(rnV, 2, DIM(rnD) - 1)': 'trRatNote: trRat chose the fewest decimals d, so |x| >= 10^-d',
        'STRING(cqV, 2, cqDec)': 'page 2 ticks: 0 or whole steps >= 10^-cqDec',
        'STRING(pcCt, 2, 2)': 'the 5% cut-off of chi-square(1), 3.84',
        'STRING(pcCp, 2, 2)': 'the 5% cut-off of chi-square(k-1), >= 3.84',
        'STRING(dpV, 2, trYDec)': 'plot 1 y ticks: 0 or whole steps >= 10^-trYDec',
        'STRING(dpF, 2, 2)': 'the animation fraction k/15: 0 or >= 0.067',
        'STRING(doV, 2, MAX(1, -doD))': 'OR-plot ticks 1, 2, 5 x 10^doD >= 10^-decimals'}
ck(set(nonzero) == set(JUST), 'R9 every STRING(x, 2, d) left with d > 0 (%d) is a justified site; the rest go through '
   'trFx (%d calls): extra %s, missing %s' % (len(nonzero), code.count('trFx('),
                                             sorted(set(nonzero) - set(JUST)), sorted(set(JUST) - set(nonzero))))
zero_args = sorted({top_args(c)[0] for c in fixed_d if top_args(c)[2] == '0'})
WHOLE = {'rsI', 'trA(rsI)', 'trTot(rsI)', 'trK - 1', 'trDFD', 'cqDf', 'enK', 'trK', 'trSum(enN)', 'trSum(enA)',
         'DIM(clT)', 'cfN', 'trSel', 'trA(trSel)', 'trTot(trSel)', 'doV', 'xsV', 'nmV'}
ck(set(zero_args) <= WHOLE, 'R9 every STRING(x, 2, 0) prints a whole number (counts, levels, df, lengths; doV >= 1, '
   'xsV and nmV in their FP = 0 branches): %s' % zero_args)
ins = [(m.group(1).strip()) for m in re.finditer(r'INSTRING\(([^,]+),', code)]
ck(sorted(set(ins)) == sorted({'cR', 'rnR', 'rpS', 'ccR', 'soS', 'trCxSb', 'trCxSa', 'cxX', '"0123456789"'}),
   'R9 INSTRING first arguments: %s' % sorted(set(ins)))
guards = [r'IF DIM\(cR\) > 0 THEN\s+IF INSTRING\(cR, "undef"\)',
          r'IF DIM\(rpO\) == 0 THEN RETURN rpT; END;',
          r'rpI := 0; IF DIM\(rpS\) > 0 THEN rpI := INSTRING\(rpS, rpO\); END;\s+WHILE',
          r'rpI := 0; IF DIM\(rpS\) > 0 THEN rpI := INSTRING\(rpS, rpO\); END;\s+END;\s+RETURN rpR \+ rpS;',
          r'IF DIM\(ccR\) == 0 THEN RETURN ""; END;\s+IF INSTRING\(ccR',
          r'IF DIM\(soS\) == 0 THEN RETURN; END;\s+soK := INSTRING\(soS',
          r'IF DIM\(trCxSa\) == 0 OR DIM\(trCxSb\) == 0 THEN [^\n]*\n\s+IF INSTRING\(trCxSa, "tr"\)',
          r'IF DIM\(cxN\) == 0 OR DIM\(cxA\) == 0 OR DIM\(cxX\) == 0 THEN',
          r'IF soK < 2 OR soK >= DIM\(soS\) THEN RETURN; END;']
ck(all(re.search(gd, code) for gd in guards),
   'R9 the guards are in place: cR (trCas), rpS and rpO (trRepl), ccR (trCxClean), soS and the halves (trCxSol); '
   'cxX is never empty (trCxMake returns first), rnR always holds a "/" (trCxMake calls trRatNote only then), '
   'trCxSb is non-empty (soK < DIM(soS)) %s' % [gd[:30] for gd in guards if not re.search(gd, code)])
say('  LEFT / MID / RIGHT calls in the code (counts and starts reviewed by hand, see the CHANGES): %d / %d / %d'
    % (len(re.findall(r'\bLEFT\(', code)), len(re.findall(r'\bMID\(', code)), len(re.findall(r'\bRIGHT\(', code))))

# ---- G (3c): beta 3c against beta 3b (the record of 3c: 3d compares those two files, not itself) ----


def raw_bodies(txt):
    out = {}
    for m in re.finditer(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', txt):
        out[m.group(1)] = m.group(0)
    return out


if B3B is None or B3C is None:
    skip('G (3c): TrendTest_beta3b.txt or TrendTest_beta3c.txt not found')
else:
    _o, _n = open(B3B, encoding='utf-8').read(), open(B3C, encoding='utf-8').read()
    R0, R1b = raw_bodies(_o), raw_bodies(_n)
    diff3c = sorted(nm for nm in set(R0) | set(R1b) if R0.get(nm) != R1b.get(nm))
    WANT3C = sorted(['TrendTest', 'trCas', 'trChiPanel', 'trCxClean', 'trCxSol', 'trDec', 'trDrawProp', 'trFx', 'trHelp',
                     'trNum', 'trOrStr', 'trPage1', 'trPageChi', 'trRepl', 'trWaitAny', 'trXStr'])
    ck(diff3c == WANT3C, 'G 3c: routines that differ from beta 3b (comments included): %s' % diff3c)
    same = sorted(set(R0) - set(diff3c))
    ck(set(R1b) - set(R0) == {'trFx'} and not set(R0) - set(R1b) and all(R0[nm] == R1b[nm] for nm in same)
       and len(same) + len(diff3c) - 1 == len(R0),
       'G 3c: beta 3b has %d routines; the other %d are byte-identical in beta 3c, comments included; one new '
       '(trFx), none removed' % (len(R0), len(same)))
    _outs = lambda t: _outside(t, diff3c)                                   # noqa: E731
    ck(_outs(_o) == _outs(_n), 'G 3c: outside those routines only comments differ (the header)')
    GUARD = ('  // an empty answer is already a failure; INSTRING("", ...) is "Invalid input" on\n'
             '  // the Prime (emulator, 17 Oct 2026), so the checks run only on a non-empty answer\n'
             '  IF DIM(cR) > 0 THEN\n'
             '    IF INSTRING(cR, "undef") > 0 OR INSTRING(cR, "rror") > 0 OR INSTRING(cR, CHAR(8734)) > 0 THEN cR := ""; END;\n'
             '  END;\n')
    OLDL = '  IF INSTRING(cR, "undef") > 0 OR INSTRING(cR, "rror") > 0 OR INSTRING(cR, CHAR(8734)) > 0 THEN cR := ""; END;\n'
    ck(GUARD in R1b['trCas'] and R1b['trCas'].replace(GUARD, OLDL) == R0['trCas'],
       'G 3c: trCas = beta 3b\'s with only the brief\'s DIM guard (the IFERR line and the quote strip byte-identical)')
    TPL = ['IF DIM(rpO) == 0 THEN RETURN rpT; END;', 'rpR := ""; rpS := rpT; rpK := DIM(rpO);',
           'rpI := 0; IF DIM(rpS) > 0 THEN rpI := INSTRING(rpS, rpO); END;', 'WHILE rpI > 0 DO',
           'IF rpI > 1 THEN rpR := rpR + LEFT(rpS, rpI - 1); END;', 'rpR := rpR + rpN;',
           'IF rpI + rpK > DIM(rpS) THEN rpS := ""; ELSE rpS := MID(rpS, rpI + rpK); END;',
           'rpI := 0; IF DIM(rpS) > 0 THEN rpI := INSTRING(rpS, rpO); END;', 'END;', 'RETURN rpR + rpS;']
    body = [l.strip() for l in R1b['trRepl'].split('\n') if l.strip() and not l.strip().startswith('//')]
    ck(body == ['trRepl(rpT, rpO, rpN)', 'BEGIN', 'LOCAL rpR, rpS, rpI, rpK;'] + TPL + ['END;'],
       'G 3c: trRepl is the brief\'s replace loop, line for line')
    ck(_re.findall(r'(?s)#PYTHON.*?#END', _o) == _re.findall(r'(?s)#PYTHON.*?#END', _n), 'G 3c: no #PYTHON block, as before')


# ================================================================ D (3d): the fleet review of 19 Oct 2026
say('\nD. 3d: TR_P as a lower tail (improvement 1), C-T1 to C-T4')
from scipy.stats import chi2 as _chi2, norm as _norm  # noqa: E402

CHI = chr(967) + chr(178)
SNOR = EXAMPLES[0][1:]
SLEEP = EXAMPLES[1][1:]


def load_path(path, x, a, n):
    """Like load(), for any version: the table loaded, trSetX and trCompute run."""
    h = Harness(path, strict=True, cas='fail')
    h.call('trInit')
    g = h.globals_
    g['trK'] = float(len(x)); g['trOX'] = [float(v) for v in x]; g['trOA'] = [float(v) for v in a]
    g['trA'] = [float(v) for v in a]; g['trTot'] = [float(v) for v in n]; g['trScM'] = 0.0; g['trSel'] = 1.0
    h.call('trSetX'); h.call('trCompute')
    return h


# ---- D1: TR_P keeps its digits, under the Prime's 12 significant digits ----
_LOG0 = ppl_run_v3e._StatFns.log


def _log12(self, name, args, val):
    """every statistics built-in answers with 12 significant digits, as the Prime does (the review's
    twelve_digits(), check_StatDist.py); arithmetic stays IEEE double"""
    v = _LOG0(self, name, args, val)
    return float('%.12g' % v) if v == v else v


def twelve(on):
    ppl_run_v3e._StatFns.log = _log12 if on else _LOG0


twelve(True)
try:
    h = load_path(PROG, *SNOR)
    t, tp = h.globals_['trX2T'], h.globals_['TR_P']
    true = _chi2.sf(t, 1)
    ck(abs(tp - true) <= 1e-10 * true and abs(tp - 1.5411626e-17) < 1e-23,
       'D1 12-digit model, snoring: beta 3d TR_P = %.6g, chi2.sf(%.4f, 1) = %.6g (relative error %.1e)'
       % (tp, t, true, abs(tp - true) / true))
    if B3C is None:
        skip('D1: beta 3c not found; its TR_P = 0 is not shown')
    else:
        ho = load_path(B3C, *SNOR)
        ck(ho.globals_['TR_P'] == 0.0 and abs(ho.globals_['trX2T'] - t) < 1e-9,
           'D1 12-digit model, snoring: beta 3c TR_P = %r -- 1 - CHISQUARE_CDF is exactly 0 (the review\'s finding)'
           % ho.globals_['TR_P'])
    # a sweep: 3 levels of 1000, cases 100, 100 + d, 100 + 2d, X2 from 0 to about 300
    worst, zeros_old, xmax_old, n_sw = 0.0, 0, 0.0, 0
    for d in range(0, 121, 4):
        x_, a_, n_ = [1, 2, 3], [100, 100 + d, 100 + 2 * d], [1000, 1000, 1000]
        hn = load_path(PROG, x_, a_, n_)
        tt, pn = hn.globals_['trX2T'], hn.globals_['trPT']
        tr = _chi2.sf(tt, 1)
        if tr > 1e-300:
            worst = max(worst, abs(pn - tr) / tr)
        n_sw += 1
        if B3C is not None:
            po = load_path(B3C, x_, a_, n_).globals_['trPT']
            if po == 0.0 and tr > 0:
                zeros_old += 1
            elif po > 0:
                xmax_old = max(xmax_old, tt)
    ck(worst <= 1e-10, 'D1 12-digit model, %d tables with X2 from 0 to %.0f: beta 3d trPT = chi2.sf to %.1e relative, '
       'every one' % (n_sw, tt, worst))
    if B3C is not None:
        ck(zeros_old > 0, 'D1 the same tables in beta 3c: %d of %d give p = exactly 0 (the largest X2 with p > 0 was %.1f)'
           % (zeros_old, n_sw, xmax_old))
finally:
    twelve(False)
# double precision: 200 random tables, 3d's trPT against chi2.sf, and every displayed p string the same as 3c's
rng = np.random.default_rng(19)
worst, diffs, ntab = 0.0, [], 0
for _ in range(200):
    k = int(rng.integers(2, 7))
    x_ = sorted(set(float(v) for v in rng.choice([0, 0.5, 1, 1.5, 2, 3, 4, 5, 7, 10], size=k, replace=False)))
    k = len(x_)
    n_ = [int(rng.integers(1, 400)) for _ in range(k)]
    a_ = [int(rng.integers(0, ni + 1)) for ni in n_]
    if sum(a_) == 0 or sum(a_) == sum(n_) or sum(n_) < 2:
        continue
    hn = load_path(PROG, x_, a_, n_)
    tt, pn = hn.globals_['trX2T'], hn.globals_['trPT']
    tr = _chi2.sf(tt, 1)
    if tr > 1e-300:
        worst = max(worst, abs(pn - tr) / tr)
    ntab += 1
    if B3C is not None:
        ho = load_path(B3C, x_, a_, n_)
        if hn.call('trPStr', pn) != ho.call('trPStr', ho.globals_['trPT']):
            diffs.append((x_, a_, n_))
ck(worst <= 1e-12, 'D1 double precision, %d random tables: beta 3d trPT = chi2.sf to %.1e relative' % (ntab, worst))
if B3C is not None:
    ck(not diffs, 'D1 the same %d tables: every displayed trend p (trPStr) is the same string in 3d as in 3c %s'
       % (ntab, diffs[:2]))

# ---- D2: the trend p is computed in one place, and every display reads it ----
src3d = open(PROG, encoding='utf-8').read()
code3d = strip_comments(src3d)
ck(code3d.count('trPT := ') == 1 and 'trPT := 2 * NORMALD_CDF(0, 1, -(trX2T^0.5));' in code3d
   and 'TR_P := trPT;' in code3d and 'CHISQUARE_CDF(1,' not in code3d.replace(' ', ''),
   'D2 trPT is set once, as 2 * NORMALD_CDF(0, 1, -(trX2T^0.5)); TR_P := trPT; no CHISQUARE_CDF(1, ...) left')
pargs = sorted(set(re.findall(r'trPStr\(([^()]*)\)', code3d)))
panel = re.findall(r'trChiPanel\(([^;]*)\);', code3d)
ck(pargs == ['cqPv', 'psP', 'trPD', 'trPP', 'trPT'] or pargs == ['cqPv', 'trPD', 'trPP', 'trPT'],
   'D2 trPStr is only ever given trPT (trend), trPP (Pearson), trPD (departure) or the panel\'s cqPv: %s' % pargs)
ck(any(', 1, trX2T, trPT,' in c for c in panel) and all('trPT' in c or 'trPD' in c for c in panel),
   'D2 page 2\'s trend panel is handed trPT: %s' % [c[:40] for c in panel])
h = Harness(PROG, strict=False, idle_key=4, cas='fail')
h.choose(5).choose(1)
h.choose(7)
r = h.call('TrendTest')
ck(isinstance(r, str) and r.startswith('TrendTest: X2 trend = 72.6588 (1 df), p < 0.0001')
   and abs(h.globals_['TR_P'] - _chi2.sf(h.globals_['TR_X2T'], 1)) <= 1e-12 * _chi2.sf(h.globals_['TR_X2T'], 1),
   'D2 Examples > Snoring > Quit: %r; TR_P = %.6g' % (r, h.globals_['TR_P']))

# ---- D3: C-T1, the residual sentence ----
h = load_path(PROG, *SLEEP)
g = h.globals_
N = sum(SLEEP[2])
res = [(g['trP'][i] - (g['trA0'] + g['trB'] * g['trX'][i])) / (g['trPQ'] / g['trTot'][i]) ** 0.5 for i in range(5)]
ss = sum(r_ * r_ for r_ in res)
ck(abs(ss - (g['trX2D'] - g['trX2T'] / (N - 1))) < 1e-9 and round(ss, 4) == 53.1141 and round(g['trX2D'], 4) == 53.1149,
   'D3 C-T1, the sleep example by the program\'s own trCompute: sum of squared residuals %.4f = departure %.4f - '
   'trend/(N-1) %.6f' % (ss, g['trX2D'], g['trX2T'] / (N - 1)))
hdr = src3d.split('// HOME EXPORTS')[0]
ck("Pearson - Armitage's N r^2." in hdr and "Pearson - Mantel's (N-1) r^2" in hdr and '53.1149' in hdr and '53.1141' in hdr
   and 'Pearson - Armitage, i.e. the departure statistic' not in hdr,
   'D3 C-T1: the header says the residuals sum to Pearson - Armitage\'s N r^2, the departure shown is Pearson - '
   'Mantel\'s, with 53.1149 and 53.1141')
if B3C is not None:
    ck('Pearson - Armitage, i.e. the departure statistic' in open(B3C, encoding='utf-8').read(),
       'D3 beta 3c\'s header said "the squared residuals add up to Pearson - Armitage, i.e. the departure statistic"')

# ---- D4: C-T2, help page 3 ----
NEW_P3 = ['Same test elsewhere: Epi Info StatCalc prints', "Mantel's (1963) (N-1) r^2, as this page does;",
          'R prop.trend.test and SAS PROC FREQ / TREND', "print Armitage's (1955) N r^2: 72.688 for",
          'snoring, 72.659 here.  The ratio is N/(N-1).']
e3, s3, sh3, h3 = help_run(PROG, ['Enter', 'Enter'])
p3 = [p for p in sh3 if p.has(HELP3)]
lines3 = [t.text for t in p3[0].texts if 146 <= t.y <= 198] if p3 else []
ck(e3 is None and lines3 == NEW_P3, 'D4 C-T2: help page 3\'s last five lines as drawn: %s' % lines3)
hs = load_path(PROG, *SNOR)
tm = hs.globals_['trX2T']
Ns = sum(SNOR[2])
ck('%.3f' % (tm * Ns / (Ns - 1)) == '72.688' and '%.3f' % tm == '72.659',
   'D4 72.688 is the program\'s own trend for snoring, %.6f, times N/(N-1) = %d/%d: %.6f' % (tm, Ns, Ns - 1, tm * Ns / (Ns - 1)))
allp3 = [t.text for t in p3[0].texts if t.x == 12 and 28 <= t.y <= 206] if p3 else []
ck(lines3 and max(len(l) for l in lines3) <= 46, 'D4 the five new lines are at most 46 characters (longest %d; the page\'s '
   'longest line %d)' % (max(len(l) for l in lines3) if lines3 else -1, max(len(l) for l in allp3) if allp3 else -1))
h1 = Harness(PROG, strict=False, idle_key=4, cas='fail')
h1.choose(5).choose(1).choose(7)
h1.call('TrendTest')
pg1 = [p for p in h1.pages if p.has('Trend (1 df):')]
ck(pg1 and pg1[0].has('Trend (1 df):  ' + CHI + ' = 72.659'), 'D4 page 1\'s headline is still Mantel\'s: "Trend (1 df):  %s = 72.659"' % CHI)
if B3C is not None:
    _e, _s, sh_o, _h = help_run(B3C, ['Enter', 'Enter'])
    p3o = [p for p in sh_o if p.has(HELP3)]
    old3 = [t.text for t in p3o[0].texts if 146 <= t.y <= 198] if p3o else []
    ck(old3 and not any('72.688' in l for l in old3) and any('JMP' in l for l in old3),
       'D4 beta 3c\'s page 3 named R and SAS without saying they print N r^2: %s' % old3[1:3])

# ---- D5: C-T3, the main menu ----


def menu_plot_run(path):
    hh = Harness(path, strict=False, idle_key=4, cas='fail')
    hh.choose(5).choose(1).choose(3).choose(7)
    e = err_of(lambda: hh.call('TrendTest'))
    mains = [c for c in hh.chooses if c.title == 'Chi-square for linear trend']
    return hh, e, mains


hm, em, mains = menu_plot_run(PROG)
items = mains[0].items if mains else []
plot = [p for p in hm.pages if p.has('WLS line, 95% band')]
ck(em is None and items[2:3] == ['Plot: proportions, trend line'] and len(items[2]) == 29
   and max(len(t) for t in items) <= 29, 'D5 C-T3: the main menu\'s third line is %r (%d characters; the longest line %d)'
   % (items[2] if len(items) > 2 else None, len(items[2]) if len(items) > 2 else -1, max(len(t) for t in items) if items else -1))
ck(len(mains) == 3 and mains[1].index == 3 and bool(plot), 'D5 item 3 still opens the proportions plot (%d frames of it)' % len(plot))
if B3C is not None:
    _ho, _eo, mo = menu_plot_run(B3C)
    ck(mo and mo[0].items[2] == 'Plot: proportions + trend line', 'D5 beta 3c showed %r (30 characters)' % (mo[0].items[2] if mo else None))

# ---- D6: C-T4, whole-number counts ----


def enter_run(path, x, a, n):
    hh = Harness(path, strict=False, idle_key=4, cas='fail')
    hh.choose(1).choose(len(x) - 1)
    hh.answer([float(v) for v in x]).answer([float(v) for v in a]).answer([float(v) for v in n])
    hh.choose(7)
    e = err_of(lambda: hh.call('TrendTest'))
    return hh, e


MSG4 = 'Cases and totals count people: whole numbers only.'
for what, x_, a_, n_ in (('24.5 cases', [1, 2, 3], [24.5, 30, 40], [100, 100, 100]),
                         ('a total of 100.5', [1, 2, 3], [24, 30, 40], [100.5, 100, 100])):
    hh, e = enter_run(PROG, x_, a_, n_)
    ck(e is None and hh.msgboxes and hh.msgboxes[-1].text == MSG4 and hh.globals_['trHas'] == 0
       and hh.result == 'TrendTest: no table', 'D6 C-T4, %s: refused with "%s", nothing loaded (%r)'
       % (what, hh.msgboxes[-1].text if hh.msgboxes else None, hh.result))
    if B3C is not None and what == '24.5 cases':
        ho, eo = enter_run(B3C, x_, a_, n_)
        ck(ho.globals_['trHas'] == 1 and (ho.result or '').startswith('TrendTest: X2 trend') and not ho.msgboxes,
           'D6 beta 3c accepted 24.5 cases: %r' % (ho.result or '')[:50])
hh, e = enter_run(PROG, [0.5, 1.5, 2.5], [24, 30, 40], [100, 100, 100])
ck(e is None and not hh.msgboxes and hh.globals_['trHas'] == 1 and (hh.result or '').startswith('TrendTest: X2 trend'),
   'D6 whole counts with fractional scores (0.5, 1.5, 2.5) are still accepted: %r' % (hh.result or '')[:60])

# ---- D7: the review's own check_TrendTest.py on beta 3d and beta 3c ----
rv = None
for d_ in (HERE, '/home/claude/work/review'):
    if os.path.exists(os.path.join(d_, 'check_TrendTest.py')):
        rv = os.path.join(d_, 'check_TrendTest.py')
        break
if rv is None:
    skip('D7: the review\'s check_TrendTest.py not found')
else:
    import subprocess
    import tempfile
    src0 = open(rv, encoding='utf-8').read()
    m = re.search(r"^SRC = '([^']*)'$", src0, re.M)
    out7 = {}
    for nm, path in (('3d', PROG), ('3c', B3C)):
        if path is None:
            continue
        dd = tempfile.mkdtemp()
        p2 = os.path.join(dd, 'check_TrendTest_on_%s.py' % nm)
        open(p2, 'w', encoding='utf-8').write(src0.replace(m.group(0), 'SRC = %r' % path))
        rr = subprocess.run([sys.executable, p2], capture_output=True, text=True,
                            env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        fails = [ln[5:].split('   ')[0].strip() for ln in rr.stdout.split('\n') if ln.startswith('FAIL ')]
        summ = [ln for ln in rr.stdout.split('\n') if 'checks passed' in ln]
        out7[nm] = (rr.returncode, fails, summ[-1] if summ else (rr.stdout + rr.stderr)[-300:])
        say('  check_TrendTest.py on beta %s: %s; failed: %s' % (nm, out7[nm][2], fails))
    BYDESIGN = ['D1 the help page says the two differ by N/(N-1)', 'E2 the three p-values are 1 - CHISQUARE_CDF',
                'F6 banner says beta 3c']
    ck(sorted(out7['3d'][1]) == BYDESIGN,
       'D7 the review\'s check_TrendTest.py on beta 3d: every check passes but the three that test the text 3d changes '
       'on purpose (C-T2\'s line, improvement 1\'s site, the banner): %s' % out7['3d'][1])
    if '3c' in out7:
        ck(out7['3c'][0] == 0 and not out7['3c'][1], 'D7 on beta 3c: %s' % out7['3c'][2])

# ---- G (3d): beta 3d against beta 3c ----
if B3C is None:
    skip('G (3d): TrendTest_beta3c.txt not found')
else:
    _c, _d = open(B3C, encoding='utf-8').read(), open(PROG, encoding='utf-8').read()
    C0, C1 = raw_bodies(_c), raw_bodies(_d)
    diff3d = sorted(nm for nm in set(C0) | set(C1) if C0.get(nm) != C1.get(nm))
    ck(diff3d == ['TrendTest', 'trCompute', 'trEnter', 'trHelp'],
       'G 3d: routines that differ from beta 3c (comments included): %s (want TrendTest, trCompute, trEnter, trHelp)' % diff3d)
    same3d = sorted(set(C0) - set(diff3d))
    ck(set(C0) == set(C1) and all(C0[nm] == C1[nm] for nm in same3d),
       'G 3d: the other %d routines are byte-identical, comments included; none added or removed' % len(same3d))

    def _cut(txt, first, last):
        """the text from the line holding `first` to the line holding `last`, whole lines"""
        i = txt.index(first); i = txt.rindex('\n', 0, i) + 1
        j = txt.index(last, i); j = txt.index('\n', j) + 1
        return txt[i:j]
    # trCompute: the comment block and the one line
    new_blk = _cut(C1['trCompute'], '// beta 3d: the trend p as a LOWER tail', 'trPT := 2 * NORMALD_CDF')
    ck(C1['trCompute'].replace(new_blk, '  trPT := 1 - CHISQUARE_CDF(1, trX2T);\n') == C0['trCompute']
       and new_blk.strip().endswith('trPT := 2 * NORMALD_CDF(0, 1, -(trX2T^0.5));'),
       'G 3d: trCompute = beta 3c\'s with the one trPT line replaced (and its comment)')
    # trEnter: the comment, the FP line, the message line
    e_cmt = _cut(C1['trEnter'], '// beta 3d: cases and totals count people', '// C-T4).  Scores may have fractions')
    e_fp = '    IF FP(enA(enI)) <> 0 OR FP(enN(enI)) <> 0 THEN enBad := 4; END;\n'
    e_msg = '  IF enBad == 4 THEN MSGBOX("%s"); RETURN 0; END;\n' % MSG4
    ck(C1['trEnter'].replace(e_cmt, '').replace(e_fp, '').replace(e_msg, '') == C0['trEnter'],
       'G 3d: trEnter = beta 3c\'s plus the FP check, its message and a comment')
    # trHelp: the five lines (and a comment)
    h_cmt = _cut(C1['trHelp'], '// beta 3d: these five lines now say WHICH form', '// checked).')
    old5 = _cut(C0['trHelp'], 'Elsewhere: Epi Info StatCalc', 'N r^2.  The two differ by N/(N-1) only.')
    new5 = _cut(C1['trHelp'], 'Same test elsewhere: Epi Info StatCalc prints', 'snoring, 72.659 here.')
    ck(C1['trHelp'].replace(h_cmt, '').replace(new5, old5) == C0['trHelp'] and new5.count('TEXTOUT_P(') == 5,
       'G 3d: trHelp = beta 3c\'s with page 3\'s five gray lines replaced (and a comment)')
    # TrendTest: the menu line (and a comment)
    m_cmt = _cut(C1['TrendTest'], '// beta 3d: "Plot: proportions + trend line"', '// list (a Syntax Error on the Prime).')
    ck(C1['TrendTest'].replace(m_cmt, '').replace('"Plot: proportions, trend line"', '"Plot: proportions + trend line"')
       == C0['TrendTest'], 'G 3d: TrendTest = beta 3c\'s with the one menu line (and a comment)')
    ck(_outside(_c, diff3d) == _outside(_d, diff3d), 'G 3d: outside those routines only comments differ (the header, notes)')
    ck('// TRENDTEST - beta 3d' in _d and _re.findall(r'(?s)#PYTHON.*?#END', _d) == [], 'G 3d: banner beta 3d; no #PYTHON block')
    # Roger, 19 Oct 2026: the disclaimer line beside the distribution terms (a comment; no page states the terms)
    ck(_d.split('// Firmware:')[0].endswith('//   warranty.\n' + '// DISCLAIMER: a teaching and demonstration aid. Not validated for\n//   forensic, clinical or legal use; do not rely on its results for\n//   legal purposes.\n' + '//\n')
       and not re.search(r'(?i)educational|personal use|warranty', ' '.join(re.findall(r'"([^"]*)"', re.sub(r'//[^\n]*', '', _d)))),
       'G 3d: the header carries Roger\'s DISCLAIMER line under the terms; no on-screen string states the terms, so no '
       'page needs "Teaching aid; not for legal use."')
    say('  routines that differ from beta 3c: %s; %d byte-identical' % (', '.join(diff3d), len(same3d)))

# ---- R10: every scientific STRING result of every beta 3d run in this script (part D's included) ----
sci_new = [(nm, s) for nm, hh in ALL_RUNS if nm == os.path.basename(PROG) for s in hh.sci_strings]
sci_old = sorted({(s[2], nm) for nm, hh in ALL_RUNS if nm != os.path.basename(PROG) for s in hh.sci_strings})
small = [(nm, s) for nm, s in sci_new if abs(s[0]) < 1]
big = sorted({s[2] for _nm, s in sci_new if abs(s[0]) >= 1e12})
ck(not small and all(abs(s[0]) >= 1e12 and s[1] == 5 for _nm, s in sci_new),
   'R10 h.sci_strings over all %d beta 3d runs: %d small (must be 0); from 1E12 up only trNum\'s six significant '
   'digits on the decimal page: %s' % (sum(1 for nm, _h in ALL_RUNS if nm == os.path.basename(PROG)), len(small), big))
say('  beta 3d sci_strings (every run): %s' % ([s[2] for _nm, s in sci_new] or 'none'))
say('  the older versions\' sci_strings in this script (%d distinct): %s' % (len(sci_old), [r for r, _nm in sci_old][:20]))

print('\n%s: %d checks, %d failure(s), %d skipped' % ('PASS' if not FAILS else 'FAIL', NCHK[0], len(FAILS), len(SKIPS)))
for f_ in FAILS:
    print('  - ' + f_)
for s_ in SKIPS:
    print('  SKIP ' + s_)
sys.exit(1 if FAILS else 0)
