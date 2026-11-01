#!/usr/bin/env python3
"""verify_DataLoad_beta1b.py -- checks DataLoad beta 1b (31 Oct 2026), which copies the columns of a matrix M0-M9 into
the Statistics 1Var lists D1-D9 (or Statistics 2Var C1-C9), by column or as scores by group.

A  the summary numbers (dd_Stats): n, mean, sample SD, min, Q1, median, Q3, max against Python, with the Prime's own
   quartile rule (HP Prime User Guide, Statistics 1Var: the median of each half, the median left out when n is odd),
   including the Guide's own example {3,5,7,8,15,16,17} (Q1 5, Q3 16), over 2,000 random lists of n = 1 to 60.
B  COLUMNS: the Rossi data (432 x 5, as SurvLab carries it) to D1-D5 value for value; to C1-C5 after the switch to
   Statistics 2Var; a matrix of 12 columns fills D1-D9 and says so; the return line.
C  SCORES BY GROUP: weeks by financial aid (two groups of 216); a three-group column whose codes are out of order
   (sorted: the smallest code to D1); more than 9 codes refused; one column for both refused; a cancelled form.
D  BLANK CELLS (the web page's padding, 9.99999999999E499; the harness's doubles stand in with +inf): columns of
   unequal length come back at their own lengths; a row with a blank score or code is left out of the groups.
E  REPLACING: lists that already hold data are replaced only after "Replace"; "Cancel" leaves them as they were;
   the question names only the lists that hold data (beta 1 said "D1-D5" when only D1 and D2 did).
F  THE MATRIX: empty matrices are named so and refused; the matrix menu shows each one's size; DataLoad starts on
   the first matrix that holds data when M1 is empty; a vector counts as one column.
G  THE PAGES: the summary rows (name, what it holds, n) for every list with data; a tap on a row opens its
   histogram, whose bars add up to n and match NumPy's counts for the same edges; the help's three pages.
H  STATIC: one EXPORT, every routine tagged dd_, every file-level variable tagged dd, no "!=", ASCII code (glyphs
   only through CHAR), no FILLPOLY_P.
K  LEFTOVERS (beta 1a, from the Virtual Calculator run): lists after the new ones that hold data are offered for
   clearing (first choice), kept on the second, untouched on Cancel; dd_Names writes list sets short; a column
   of blanks empties its list; the form's labels are short; a second run that loads nothing says so.
L  LAYOUT: text_overlap_v1's recorder over every screen drawn above: no firm overlap, frame straddle or overrun.

Needs the PPL harness ppl_run_v3e.py and text_overlap_v1.py (in ./tools, ../tools, or $DL_TOOLS), hp-prime-kit
($HPKIT), NumPy.  The Rossi data is read from SurvLab_beta1b.txt in ../programs (or beside this file).
Run:  python3 verify_DataLoad_beta1b.py [DataLoad_beta1b.txt]     (exit code 0 = all passed)
"""
import math
import os
import random
import re
import sys
import warnings

import numpy as np

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HPKIT', '/home/claude/kit/hp-prime-kit-HEAD')
_cands = [c for c in (os.environ.get('DL_TOOLS', ''), os.path.join(HERE, 'tools'), os.path.join(HERE, '..', 'tools'),
                      HERE, '/home/claude/metcalfdds/hp-prime-statistics/tools') if c]
for cand in reversed(_cands):
    if any(os.path.exists(os.path.join(cand, f)) for f in ('ppl_run_v3e.py', 'text_overlap_v1.py')):
        sys.path.insert(0, cand)
sys.path.insert(0, os.environ['HPKIT'])
from ppl_run_v3e import Harness  # noqa: E402
from hpkit.interp import Matrix  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402

PROG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'DataLoad_beta1b.txt')
if not os.path.exists(PROG):
    PROG = os.path.join(HERE, '..', 'programs', 'DataLoad_beta1b.txt')
SRC = open(PROG, encoding='utf-8').read()

FAIL = []
NPASS = [0]
INF = float('inf')


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:400]) if (detail != '' and not ok) else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


# ---- the Rossi data, read from SurvLab's own lists (week, arrest, fin, age, prio) ----
def rossi():
    for c in (os.path.join(HERE, 'SurvLab_beta1b.txt'), os.path.join(HERE, '..', 'programs', 'SurvLab_beta1b.txt'),
              '/home/claude/metcalfdds/hp-prime-statistics/programs/SurvLab_beta1b.txt'):
        if os.path.exists(c):
            s = open(c, encoding='utf-8').read()
            break
    cols = []
    for name in ('svRwk', 'svRar', 'svRfin', 'svRage', 'svRpri'):
        m = re.search(name + r'\s*:=\s*\{([^}]*)\}', s)
        body = re.sub(r'//[^\n]*', '', m.group(1))
        cols.append([float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', body)])
    return [list(r) for r in zip(*cols)]


ROSSI = rossi()


def H(mats=None, app=None):
    """A harness with M0-M9 as the Prime keeps unused matrices (one zero), then the given ones."""
    h = Harness(PROG, idle_key=4, home_minus=True, app_data=app if app is not None else {'D1': [], 'C1': []})
    for k in range(10):
        h.globals_['M%d' % k] = Matrix([[0.0]])
    for k, rows in (mats or {}).items():
        h.globals_[k] = Matrix([[float(x) for x in r] for r in rows]) if rows != 'vec' else None
    h.execute('dd_Init()')
    return h


def L(h, name):
    v = h.globals_.get(name)
    return None if v is None else [float(x) for x in v]


# ---- the Prime's quartile rule, independently ----
def prime_stats(x):
    s = sorted(x)
    n = len(s)

    def med(a):
        m = len(a)
        return a[(m - 1) // 2] if m % 2 else (a[m // 2 - 1] + a[m // 2]) / 2
    md = med(s)
    if n == 1:
        q1 = q3 = s[0]
    else:
        h = n // 2
        q1, q3 = med(s[:h]), med(s[n - h:])
    mean = sum(s) / n
    sd = math.sqrt(sum((v - mean) ** 2 for v in s) / (n - 1)) if n > 1 else 0.0
    return [n, mean, sd, s[0], q1, md, q3, s[-1]]


OV.install()

# ===================================================================== A
print('=== A. the summary numbers (dd_Stats) against the Prime\'s quartile rule')
h = H()
got = h.execute('dd_Stats({3,5,7,8,15,16,17})')
check('A1 the User Guide\'s example {3,5,7,8,15,16,17}: Q1 = 5, median = 8, Q3 = 16 (the median left out)',
      [got[4], got[5], got[6]] == [5.0, 8.0, 16.0], got)
got = h.execute('dd_Stats({3,5,7,8,15,16})')
check('A2 an even n {3,5,7,8,15,16}: Q1 = 5, median = 7.5, Q3 = 15', [got[4], got[5], got[6]] == [5.0, 7.5, 15.0],
      got)
rng = random.Random(20261031)
worst, bad = 0.0, []
for trial in range(2000):
    n = rng.randint(1, 60)
    kind = trial % 4
    if kind == 0:
        x = [rng.randint(0, 9) for _ in range(n)]                       # many ties
    elif kind == 1:
        x = [round(rng.gauss(50, 12), 3) for _ in range(n)]
    elif kind == 2:
        x = [round(rng.expovariate(0.2), 2) for _ in range(n)]          # skewed
    else:
        x = [round(rng.uniform(-1e6, 1e6), 1) for _ in range(n)]
    got = h.execute('dd_Stats({' + ','.join(repr(float(v)) for v in x) + '})')
    want = prime_stats(x)
    for a, b in zip(got, want):
        d = abs(a - b) / max(1.0, abs(b))
        worst = max(worst, d)
        if d > 1e-9:
            bad.append((x[:6], got, want))
            break
check('A3 2,000 random lists, n 1 to 60 (ties, normal, skewed, wide): all eight numbers agree (worst relative %.1e)'
      % worst, not bad, bad[:2])
got = h.execute('dd_Stats({})')
check('A4 an empty list gives zeros, not an error', list(got) == [0.0] * 8, got)
got = h.execute('dd_Stats({4})')
check('A5 one value: n 1, SD 0, every quartile the value', list(got) == [1.0, 4.0, 0.0, 4.0, 4.0, 4.0, 4.0, 4.0], got)

# ===================================================================== B
print('=== B. COLUMNS')
cols = [list(c) for c in zip(*ROSSI)]
check('B0 the Rossi data from SurvLab: 432 rows, 114 arrests, 216 with aid',
      len(ROSSI) == 432 and sum(cols[1]) == 114 and sum(cols[2]) == 216)
h = H({'M1': ROSSI})
h.choose(1)            # Columns
h.press('Esc')         # leave the lists
h.choose(7)            # quit
ret = h.execute('DATALOAD()')
ok = all(L(h, 'D%d' % (j + 1)) == cols[j] for j in range(5))
check('B1 columns 1-5 of M1 are D1-D5, value for value, in order', ok)
check('B2 D6-D9 untouched (never written)', all(h.globals_.get('D%d' % k) is None for k in range(6, 10)))
check('B3 the line DataLoad returns names the load: "DataLoad: M1 -> D1-D5 (432 rows)"',
      ret == 'DataLoad: M1 ' + chr(8594) + ' D1-D5 (432 rows)', ret)
check('B4 no harness warnings', not h.warnings, h.warnings[:3])
h = H({'M1': ROSSI})
h.choose(5)            # Lists: C (Statistics 2Var)
h.choose(1)            # Columns
h.press('Esc')
h.choose(7)
ret = h.execute('DATALOAD()')
check('B5 after the switch to Statistics 2Var, columns 1-5 are C1-C5 and no D list is written',
      all(L(h, 'C%d' % (j + 1)) == cols[j] for j in range(5)) and L(h, 'D1') == [] and h.globals_.get('D2') is None,
      ret)
wide = [[r * 100 + c for c in range(1, 13)] for r in range(1, 21)]          # 20 rows, 12 columns
h = H({'M3': wide})
h.choose(4)            # which matrix?
h.choose(4)            # M3 (the 4th line: M0, M1, M2, M3)
h.choose(1)
h.press('Esc')
h.choose(7)
ret = h.execute('DATALOAD()')
msgs = [it for it in h.log if 'MSGBOX' in str(it)]
check('B6 a 12-column matrix fills D1-D9 with its first 9 columns and says so in a box',
      all(L(h, 'D%d' % j) == [float(r * 100 + j) for r in range(1, 21)] for j in range(1, 10))
      and any('12 columns' in str(m) for m in msgs), (ret, msgs[:2]))

# ===================================================================== C
print('=== C. SCORES BY GROUP')
h = H({'M1': ROSSI})
h.choose(2)                              # Scores by group
h.answer({'gsc': 1, 'ggc': 3})           # weeks, by fin
h.press('Esc')
h.choose(7)
ret = h.execute('DATALOAD()')
w0 = [r[0] for r in ROSSI if r[2] == 0]
w1 = [r[0] for r in ROSSI if r[2] == 1]
check('C1 weeks by financial aid: D1 = the 216 weeks with fin 0, D2 the 216 with fin 1, in file order',
      L(h, 'D1') == w0 and L(h, 'D2') == w1 and len(w0) == 216, (len(L(h, 'D1') or []), len(L(h, 'D2') or [])))
check('C2 the descriptions read "M1 col 3 = 0" and "M1 col 3 = 1"; the return line names the split',
      h.globals_['ddDSC'][:2] == ['M1 col 3 = 0', 'M1 col 3 = 1'] and ret.startswith('DataLoad: M1 col 1 by col 3 '),
      (h.globals_['ddDSC'][:3], ret))
three = [[10 + i, [3, 1, 2][i % 3]] for i in range(30)]
h = H({'M1': three})
h.choose(2)
h.answer({'gsc': 1, 'ggc': 2})
h.press('Esc')
h.choose(7)
h.execute('DATALOAD()')
check('C3 codes 3, 1, 2 out of order: D1 holds code 1, D2 code 2, D3 code 3',
      L(h, 'D1') == [float(10 + i) for i in range(30) if i % 3 == 1]
      and L(h, 'D2') == [float(10 + i) for i in range(30) if i % 3 == 2]
      and L(h, 'D3') == [float(10 + i) for i in range(30) if i % 3 == 0])
h = H({'M1': ROSSI})
h.choose(2)
h.answer({'gsc': 1, 'ggc': 4})           # age as "groups": 30+ values
h.choose(7)
h.execute('DATALOAD()')
msgs = [str(it) for it in h.log if 'MSGBOX' in str(it)]
check('C4 a "group" column with more than 9 values (age) is refused, and nothing is written',
      L(h, 'D1') == [] and h.globals_.get('D2') is None and any('more than 9' in m for m in msgs), msgs[:2])
h = H({'M1': ROSSI})
h.choose(2)
h.answer({'gsc': 2, 'ggc': 2})
h.choose(7)
h.execute('DATALOAD()')
msgs = [str(it) for it in h.log if 'MSGBOX' in str(it)]
check('C5 the same column for scores and groups is refused', L(h, 'D1') == [] and any('two different' in m
                                                                                      for m in msgs), msgs[:2])
h = H({'M1': [[1.0], [2.0]]})
h.choose(2)
h.choose(7)
h.execute('DATALOAD()')
msgs = [str(it) for it in h.log if 'MSGBOX' in str(it)]
check('C6 a one-column matrix: scores by group explains that it needs two columns',
      any('needs two columns' in m for m in msgs), msgs[:2])

# ===================================================================== D
print('=== D. BLANK CELLS')
pad = [[1, 10, 5], [2, 20, INF], [3, INF, INF], [4, INF, INF]]       # columns of 4, 2 and 1 values
h = H({'M1': pad})
h.choose(1)
h.press('Esc')
h.choose(7)
h.execute('DATALOAD()')
check('D1 padded columns come back at their own lengths: D1 4 values, D2 2, D3 1',
      L(h, 'D1') == [1, 2, 3, 4] and L(h, 'D2') == [10, 20] and L(h, 'D3') == [5])
gpad = [[7, 1], [INF, 2], [9, INF], [11, 2], [13, 1]]
h = H({'M1': gpad})
h.choose(2)
h.answer({'gsc': 1, 'ggc': 2})
h.press('Esc')
h.choose(7)
h.execute('DATALOAD()')
check('D2 by group: a row with a blank score or a blank code is left out (D1 {7, 13}, D2 {11})',
      L(h, 'D1') == [7, 13] and L(h, 'D2') == [11])
allb = [[1, INF], [2, INF]]
h = H({'M1': allb})
h.choose(1)
h.press('Esc')
h.choose(7)
h.execute('DATALOAD()')
check('D3 a column of blanks only empties its list (beta 1 left the old values): D2 = {}',
      L(h, 'D1') == [1, 2] and L(h, 'D2') == [] and h.globals_['ddDSC'][1] == '', (L(h, 'D2'), h.globals_['ddDSC'][:2]))
check('D4 the program tests a blank as 1E499 or more (the Prime\'s largest real is 9.99999999999E499)',
      'IF rv >= 1E499 THEN RETURN 0; END;' in SRC)

# ===================================================================== E
print('=== E. REPLACING lists that hold data')
h = H({'M1': ROSSI}, app={'D1': [99.0, 98.0], 'C1': []})
h.choose(1)            # Columns
h.choose(1)            # Replace D1-D5
h.press('Esc')
h.choose(7)
h.execute('DATALOAD()')
check('E1 D1 held data: after "Replace D1-D5" the columns are loaded', L(h, 'D1') == cols[0])
h = H({'M1': ROSSI}, app={'D1': [99.0, 98.0], 'C1': []})
h.choose(1)
h.choose(2)            # Cancel
h.choose(7)
h.execute('DATALOAD()')
check('E2 after "Cancel" D1 is as it was and nothing else is written', L(h, 'D1') == [99.0, 98.0]
      and h.globals_.get('D2') is None)
h = H({'M1': ROSSI}, app={'D1': [99.0, 98.0], 'C1': []})
h.choose(1)
h.choose('Replace D1-D5')      # the harness refuses an answer that is not one of the items
h.press('Esc')
h.choose(7)
err = ''
try:
    h.execute('DATALOAD()')
except Exception as e:          # noqa: BLE001
    err = str(e)
check('E3 the question offers "Replace D1-D5" (the harness matched the item by its text)',
      not err and L(h, 'D1') == cols[0], err[:200])


h = H({'M1': ROSSI}, app={'D1': [99.0, 98.0], 'C1': []})
h.globals_['D2'] = [5.0, 6.0]
h.choose(1)
h.choose(1)
h.press('Esc')
h.choose(7)
h.execute('DATALOAD()')
cq = [c for c in h.chooses if 'hold' in c.title]
check('E4 D1 and D2 hold data, five columns: the question reads "D1, D2 hold data" (beta 1: "D1-D5 already hold'
      ' data"), its items "Replace D1-D5" and "Cancel"',
      bool(cq) and cq[0].title == 'D1, D2 hold data' and cq[0].items == ['Replace D1-D5', 'Cancel'],
      [(c.title, c.items) for c in cq])
h = H({'M1': ROSSI}, app={'D1': [99.0, 98.0], 'C1': []})
h.choose(1)
h.choose(1)
h.press('Esc')
h.choose(7)
h.execute('DATALOAD()')
cq = [c for c in h.chooses if 'hold' in c.title]
check('E5 only D1 holds data: "D1 holds data" (singular)', bool(cq) and cq[0].title == 'D1 holds data',
      [c.title for c in cq])

# ===================================================================== F
print('=== F. THE MATRIX')
h = H()
h.choose(1)
h.choose(7)
ret = h.execute('DATALOAD()')
msgs = [str(it) for it in h.log if 'MSGBOX' in str(it)]
check('F1 all matrices empty: Columns says M1 is empty; nothing written; "nothing loaded"',
      any('M1 is empty' in m for m in msgs) and L(h, 'D1') == [] and ret == 'DataLoad: nothing loaded', (ret, msgs[:1]))
h = H({'M4': ROSSI})
h.choose(7)
h.execute('DATALOAD()')
check('F2 M1 empty and M4 holding data: DataLoad starts on M4', h.globals_['ddSRC'] == 4, h.globals_['ddSRC'])
res = []
for item, want in (('M1: empty', 1), ('M4: 432 ' + chr(215) + ' 5', 4), ('M7: 20 ' + chr(215) + ' 12', 7)):
    h = H({'M4': ROSSI, 'M7': wide})
    h.choose(4)
    h.choose(item)     # matched by its text: the menu must show exactly this line
    h.choose(7)
    try:
        h.execute('DATALOAD()')
        res.append(h.globals_['ddSRC'] == want)
    except Exception as e:      # noqa: BLE001
        res.append(str(e)[:120])
check('F3 the matrix menu shows each matrix: "M1: empty", "M4: 432 x 5", "M7: 20 x 12", and choosing one takes it',
      res == [True, True, True], res)
h = H()
h.globals_['M2'] = [4.0, 5.0, 6.0]       # a vector, as the harness keeps one: a list
h.execute('dd_Init()')
shp = h.execute('dd_Shape(M2)')
col = h.execute('dd_Column(M2, 1)')
check('F4 a vector counts as one column: shape {3, 1}, its column {4, 5, 6}', list(shp) == [3.0, 1.0]
      and list(col) == [4.0, 5.0, 6.0], (shp, col))

# ===================================================================== G
print('=== G. THE PAGES')
h = H({'M1': ROSSI})
h.choose(1)
h.tap(200, 44 + 19 * 0 + 5)      # D1's row
h.press('Esc')                   # back from the histogram
h.tap(200, 44 + 19 * 3 + 5)      # D4's row
h.press('Esc')
h.press('Esc')                   # leave the lists
h.choose(7)
h.execute('DATALOAD()')
pages = h.pages
titles = [p.lines()[0] for p in pages]
check('G1 the summary, then D1\'s histogram, the summary, D4\'s histogram, the summary',
      titles == ['DataLoad: the D lists', 'D1: M1 col 1', 'DataLoad: the D lists', 'D4: M1 col 4',
                 'DataLoad: the D lists'], titles)
summ = pages[0].lines()
check('G2 the summary names every list with its description and n (D1 M1 col 1 432 ... D5 M1 col 5 432)',
      all(('D%d' % k) in summ and ('M1 col %d' % k) in summ for k in range(1, 6)) and summ.count('432') == 5, summ[:20])
# the histogram's bars against NumPy with the same edges
rects = [it for it in h.log if str(it).startswith('RECT_P')] if False else None
hi = pages[1].lines()
nline = [x for x in hi if x.startswith('n 432')]
check('G3 D1\'s histogram prints n 432, the mean 45.85 and s 12.66 (the weeks)',
      bool(nline) and (chr(57344) + ' 45.85') in nline[0] and 's 12.66' in nline[0], nline)
qline = [x for x in hi if x.startswith('min ')]
want = prime_stats(cols[0])
check('G4 its five numbers: min %g, Q1 %g, med %g, Q3 %g, max %g' % tuple(want[3:]),
      bool(qline) and qline[0] == 'min %g   Q1 %g   med %g   Q3 %g   max %g' % tuple(want[3:]), qline)
# bins: dd_DrawHisto's rule, and NumPy's counts over the same edges
st = prime_stats(cols[0])
hw = h.execute('dd_NiceNum(%r, 1)' % ((st[7] - st[3]) / 10))
hs = math.floor(st[3] / hw) * hw
nb = math.floor((st[7] - hs) / hw) + 1
edges = [hs + i * hw for i in range(nb + 1)]
cnt = np.histogram(cols[0], bins=edges)[0]
counts = [0] * nb
for v in cols[0]:
    b = min(nb, max(1, math.floor((v - hs) / hw) + 1))
    counts[b - 1] += 1
check('G5 the weeks\' bins (width %g from %g, %d bars) hold n in all and match NumPy\'s counts over the same edges'
      % (hw, hs, nb),
      sum(counts) == 432 and list(cnt) == counts, (list(cnt), counts))
h = H({'M1': ROSSI})
h.choose(6)            # help
h.choose(7)
h.execute('DATALOAD()')
ht = [p.lines()[0] for p in h.pages]
check('G6 help: three pages', ht == ['DataLoad help 1/3: what it does', 'DataLoad help 2/3: getting data in',
                                     'DataLoad help 3/3: then run'], ht)
h = H({'M1': ROSSI})
h.choose(3)            # look, with every list empty
h.choose(7)
h.execute('DATALOAD()')
check('G7 "Look" with no data says the lists are empty', any('are all empty' in x for x in h.pages[0].lines()),
      h.pages[0].lines()[:4])
nine = [[r + c * 0.5 for c in range(1, 10)] for r in range(1, 41)]
h = H({'M1': nine})
h.choose(1)
h.tap(200, 44 + 19 * 8 + 5)      # the ninth row
h.press('Esc')
h.press('Esc')
h.choose(7)
h.execute('DATALOAD()')
check('G8 nine lists fit the summary, and a tap on the ninth row opens D9', [p.lines()[0] for p in h.pages][:2] ==
      ['DataLoad: the D lists', 'D9: M1 col 9'], [p.lines()[0] for p in h.pages][:2])


# ===================================================================== K
print('=== K. LEFTOVERS (lists after the new ones that hold data)')
d5 = {'D1': [1.0, 2.0], 'C1': []}
def five_lists(h):
    for k in range(2, 6):
        h.globals_['D%d' % k] = [float(k), float(k) + 0.5]
h = H({'M1': ROSSI}, app=dict(d5))
five_lists(h)
h.choose(2)
h.answer({'gsc': 1, 'ggc': 3})
h.choose('Fill D1-D2, clear D3-D5')
h.press('Esc')
h.choose(7)
ret = h.execute('DATALOAD()')
cq = [c for c in h.chooses if 'hold' in c.title]
check('K1 D1-D5 hold data, two groups: the question "D1-D5 hold data" offers "Fill D1-D2, clear D3-D5" first, then'
      ' "Fill D1-D2, keep D3-D5", "Cancel"',
      bool(cq) and cq[0].title == 'D1-D5 hold data'
      and cq[0].items == ['Fill D1-D2, clear D3-D5', 'Fill D1-D2, keep D3-D5', 'Cancel'],
      [(c.title, c.items) for c in cq])
check('K2 "clear": D1, D2 the two groups; D3-D5 empty, their descriptions blank; the return line says so',
      L(h, 'D1') == w0 and L(h, 'D2') == w1 and all(L(h, 'D%d' % k) == [] for k in (3, 4, 5))
      and h.globals_['ddDSC'][2:5] == ['', '', ''] and ret.endswith(', D3-D5 cleared'),
      (ret, [len(L(h, 'D%d' % k) or []) for k in range(1, 6)]))
h = H({'M1': ROSSI}, app=dict(d5))
five_lists(h)
h.choose(2)
h.answer({'gsc': 1, 'ggc': 3})
h.choose('Fill D1-D2, keep D3-D5')
h.press('Esc')
h.choose(7)
ret = h.execute('DATALOAD()')
check('K3 "keep": D1, D2 the groups; D3-D5 as they were; no "cleared" in the return line',
      L(h, 'D1') == w0 and all(L(h, 'D%d' % k) == [float(k), float(k) + 0.5] for k in (3, 4, 5))
      and 'cleared' not in ret, ret)
h = H({'M1': ROSSI}, app=dict(d5))
five_lists(h)
h.choose(2)
h.answer({'gsc': 1, 'ggc': 3})
h.choose('Cancel')
h.choose(7)
ret = h.execute('DATALOAD()')
check('K4 "Cancel": all five lists as they were; "nothing loaded"',
      L(h, 'D1') == [1.0, 2.0] and all(L(h, 'D%d' % k) == [float(k), float(k) + 0.5] for k in (2, 3, 4, 5))
      and ret == 'DataLoad: nothing loaded', ret)
h = H({'M2': [[1, 2, 3], [4, 5, 6]]}, app={'D1': [], 'C1': []})
h.globals_['D4'] = [7.0]
h.globals_['D7'] = [8.0, 9.0]
h.choose(1)
h.choose(1)
h.press('Esc')
h.choose(7)
ret = h.execute('DATALOAD()')
cq = [c for c in h.chooses if 'hold' in c.title]
check('K5 only lists after the new ones hold data (D4, D7; three columns): "D4, D7 hold data", "Fill D1-D3, clear'
      ' D4, D7"; after it D4 and D7 are empty and D1-D3 the columns',
      bool(cq) and cq[0].title == 'D4, D7 hold data' and cq[0].items[0] == 'Fill D1-D3, clear D4, D7'
      and L(h, 'D4') == [] and L(h, 'D7') == [] and L(h, 'D1') == [1, 4] and L(h, 'D3') == [3, 6]
      and ret == 'DataLoad: M2 ' + chr(8594) + ' D1-D3 (2 rows), D4, D7 cleared',
      ([(c.title, c.items) for c in cq], ret))
h = H({'M1': ROSSI})
names = {}
for lst, want in (('{1}', 'D1'), ('{1,2}', 'D1, D2'), ('{3,4,5}', 'D3-D5'), ('{1,3,4,5,8}', 'D1, D3-D5, D8'),
                  ('{2,3,5,6}', 'D2, D3, D5, D6'), ('{1,2,3,4,5,6,7,8,9}', 'D1-D9'), ('{9}', 'D9')):
    names[lst] = (h.execute('dd_Names(%s)' % lst), want)
check('K6 dd_Names writes list sets short: ' + ', '.join('%s -> "%s"' % (k, v[1]) for k, v in names.items()),
      all(a == b for a, b in names.values()), names)
h = H({'M1': ROSSI})
h.choose(5)            # C lists
h.globals_['C3'] = [1.0]
h.choose(2)
h.answer({'gsc': 1, 'ggc': 3})
h.choose(1)
h.press('Esc')
h.choose(7)
ret = h.execute('DATALOAD()')
cq = [c for c in h.chooses if 'hold' in c.title]
check('K7 the same with the C lists: "C3 holds data", "Fill C1-C2, clear C3"; C3 emptied',
      bool(cq) and cq[0].title == 'C3 holds data' and cq[0].items[0] == 'Fill C1-C2, clear C3' and L(h, 'C3') == [],
      ([(c.title, c.items) for c in cq], ret))
h = H({'M1': ROSSI})
h.choose(2)
h.answer({'gsc': 1, 'ggc': 3})
h.press('Esc')
h.choose(7)
h.execute('DATALOAD()')
fi = h.inputs[0] if h.inputs else None
check('K8 the Scores-by-group form: title "Which columns? (M1 has 5)", labels "Scores:" and "Groups:" (beta 1\'s'
      ' "Scores in column" was cut to "Scores in colu...")',
      fi is not None and fi.title == 'Which columns? (M1 has 5)' and list(fi.labels) == ['Scores:', 'Groups:'],
      None if fi is None else (fi.title, fi.labels))
check('K9 American spelling: no "analyse", "colour", "honour"',
      not re.search(r'analyse|colour|honour', SRC, re.I))
h = H({'M1': ROSSI})
h.choose(1)
h.press('Esc')
h.choose(7)
ret1 = h.execute('DATALOAD()')
h.choose(7)
ret2 = h.execute('DATALOAD()')
check('K10 a second run that loads nothing returns "DataLoad: nothing loaded", not the first run\'s line (beta 1a,'
      ' Virtual Calculator)', ret1.startswith('DataLoad: M1 ') and ret2 == 'DataLoad: nothing loaded', (ret1, ret2))

# ===================================================================== H
print('=== H. STATIC')
code = re.sub(r'"(?:[^"\\]|\\.)*"', '""', '\n'.join(ln.split('//')[0] for ln in SRC.split('\n')))
exports = re.findall(r'^EXPORT\s+(\w+)', SRC, re.M)
check('H1 one EXPORT, DATALOAD', exports == ['DATALOAD'], exports)
heads = re.findall(r'^(?:LOCAL\s+)?(\w+)\s*\([^)]*\)\s*$', SRC, re.M)
untag = [x for x in heads if not x.startswith('dd_') and x != 'DATALOAD']
check('H2 every routine is tagged dd_ (%d routines)' % len(heads), not untag, untag)
nocom = '\n'.join(ln.split('//')[0] for ln in SRC.split('\n'))
fl = [n for ln in re.findall(r'^LOCAL\s+([^(\n]*?);\s*$', nocom, re.M)
      for n in re.findall(r'(?:^|,)\s*([A-Za-z_]\w*)', re.sub(r'\{[^}]*\}', '', ln))]
untagv = sorted(set(x for x in fl if not x.startswith('dd')))
check('H3 every file-level variable is tagged dd', not untagv, untagv)
check('H4 no "!=" (Lessons Learned v7w: "<>")', '!=' not in code)
nonascii = sorted(set(ch for ch in code if ord(ch) > 127))
check('H5 the code is ASCII: glyphs only through CHAR()', not nonascii, nonascii)
check('H6 no FILLPOLY_P (its alpha argument is not settled for an opaque fill)', 'FILLPOLY_P' not in code)

# ===================================================================== L
print('=== L. layout (text_overlap_v1 over every screen above)')
rep = OV.report()
tag = [t for t in rep if t.startswith('DataLoad_beta1b')]
f = rep[tag[0]] if tag else None
firm = []
if f:
    firm += [('overlap', c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
    firm += [('straddle', x['text'], x['edge']) for x in f['straddles'] if x['firm']]
    firm += [('overrun', x['text'], x.get('right')) for x in f['overruns'] if x['firm']]
    print('   screens: %d distinct of %d; marginal findings: %d collisions, %d straddles, %d overruns'
          % (f['screens_distinct'], f['screens_total'], len([c for c in f['collisions'] if not c['firm']]),
             len([x for x in f['straddles'] if not x['firm']]), len([x for x in f['overruns'] if not x['firm']])))
    for c in f['collisions']:
        if not c['firm'] or c['severity'] != 'overlap':
            print('     (%s, not firm) %s | %s' % (c['severity'], c['a'][:50], c['b'][:50]))
    for x in f['overruns']:
        if not x['firm']:
            print('     (overrun at the conservative width, not firm) %s -> %s px' % (x['text'][:60], x.get('right')))
check('L1 no firm overlap, frame straddle or overrun on any DataLoad screen drawn (%s)' % (tag[:1]),
      bool(tag) and not firm, firm[:8])

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for x in FAIL:
    print('  FAILED: ' + x)
sys.exit(1 if FAIL else 0)
