#!/usr/bin/env python3
"""verify_DataLoad_beta1i.py -- checks DataLoad beta 1i (27 Nov 2026, round 20): blank cells inside paired columns.

beta 1h left the blank cells out of each column separately (dd_Column).  That is right for separate groups of unequal size
and wrong for paired columns (before and after, x and y, raters): one blank in the middle of a column made the rest of that
column slide up a row.  beta 1i was built from beta 1h by verify/round20/make_round20.py (exact replacements).  When two or
more columns are to be loaded and any of them has a blank ABOVE a value, it asks how they go together: "Pairs: keep complete rows" or
"Separate groups: drop blanks" (beta 1h's way), or Cancel.

N  THE NEW QUESTION, driven through DATALOAD() in the PPL harness (a blank is +inf there, as in the beta 1b script):
   who is asked and who is not (blanks only at the foot; one column; a hole only in a column past the ninth); the title
   and the items, and that they fit (a title 31 characters, an item 30); each answer: pairs, separate groups, Cancel,
   Esc; pairs on the Rossi data with holes punched in, row for row against the rows kept; no complete row at all; the
   C lists; lists that already hold data, cleared or kept; the line DataLoad returns, laid out as the Program Catalog's
   box shows it (five lines of about 26 characters).
P  THE HELP: four pages, titled 1/4 to 4/4; page 3 ("Blank cells") says what the program does; pages 1, 2 and 4 are
   beta 1h's pages word for word, but for their titles and page 1's line on blank cells.
S  STATIC: beta 1h's routines are in beta 1i word for word, but for dd_LoadCols and dd_Help; the new routines carry the
   tag dd_; no LOCAL holds more than 6 names; every CHOOSE sets its index to 0 first; no "!="; ASCII code.
R  REGRESSION: the beta 1b script (arithmetic, columns, scores by group, blank cells, replacing, the matrix, the pages,
   static, leftovers, layout) run on beta 1i: every check passes but G6, which reads the help's three titles of beta 1h.
L  LAYOUT: text_overlap_v1's recorder over every screen drawn in N and P: no firm overlap, frame straddle or overrun.
Run from verify/ as it is:  python3 verify_DataLoad_beta1i.py      (exit code 0 = all passed)
Needs ../tools (ppl_run_v3e.py, text_overlap_v1.py, prime_facts_v1.py), hp-prime-kit ($HPKIT), NumPy.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
TOOLS = os.path.join(HERE, '..', 'tools')
sys.path.insert(0, TOOLS)
sys.path.insert(0, os.environ['HPKIT'])
from ppl_run_v3e import Harness  # noqa: E402
from hpkit.interp import Matrix  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()

NAME, OLDNAME = 'DataLoad_beta1i.txt', 'DataLoad_beta1h.txt'
PROG = os.path.join(HERE, '..', 'programs', NAME)
SRC = open(PROG, encoding='utf-8').read()
FAIL, NPASS = [], [0]
INF = float('inf')
ARROW = chr(8594)


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:500]) if (detail != '' and not ok) else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


def older():
    """beta 1h: beside this script, in ../programs, or from git history (the commit that last had it)"""
    for p in (os.path.join(HERE, OLDNAME), os.path.join(HERE, '..', 'programs', OLDNAME)):
        if os.path.exists(p):
            return open(p, encoding='utf-8').read()
    root = os.path.join(HERE, '..')
    for ref in ('HEAD', 'origin/main'):
        out = subprocess.run(['git', '-C', root, 'show', '%s:programs/%s' % (ref, OLDNAME)], capture_output=True)
        if out.returncode == 0:
            return out.stdout.decode('utf-8')
    c = subprocess.run(['git', '-C', root, 'log', '-n', '1', '--format=%H', '--', 'programs/' + OLDNAME],
                       capture_output=True, text=True).stdout.strip()
    if c:
        out = subprocess.run(['git', '-C', root, 'show', '%s^:programs/%s' % (c, OLDNAME)], capture_output=True)
        if out.returncode == 0:
            return out.stdout.decode('utf-8')
    return None


def rossi():
    """the Rossi data (week, arrest, fin, age, prio), 432 rows, from SurvLab's own lists"""
    s = open(os.path.join(HERE, '..', 'programs', 'SurvLab_beta1h.txt'), encoding='utf-8').read()
    cols = []
    for name in ('svRwk', 'svRar', 'svRfin', 'svRage', 'svRpri'):
        m = re.search(name + r'\s*:=\s*\{([^}]*)\}', s)
        body = re.sub(r'//[^\n]*', '', m.group(1))
        cols.append([float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', body)])
    return [list(r) for r in zip(*cols)]


def H(mats=None, app=None):
    """A harness with M0-M9 as the Prime keeps unused matrices (one zero), then the given ones."""
    h = Harness(PROG, idle_key=4, home_minus=True, app_data=app if app is not None else {'D1': [], 'C1': []})
    for k in range(10):
        h.globals_['M%d' % k] = Matrix([[0.0]])
    for k, rows in (mats or {}).items():
        h.globals_[k] = Matrix([[float(x) for x in r] for r in rows])
    h.execute('dd_Init()')
    return h


def L(h, name):
    v = h.globals_.get(name)
    return None if v is None else [float(x) for x in v]


def asked(h):
    """the hole question, if DataLoad put it: (title, items, answer)"""
    q = [d for d in h.chooses if d.title.endswith('blank inside') or d.title.endswith('blanks inside')]
    return (q[0].title, list(q[0].items), q[0].index) if q else None


def run(mats, picks, app=None, esc_lists=True):
    """DATALOAD(): Columns, then the picks for the questions that follow, Esc out of the lists page, quit"""
    h = H(mats, app)
    h.choose(1)                       # Columns
    for p in picks:
        h.choose(p)
    if esc_lists:
        h.press('Esc')                # leave the lists page
    h.choose(7)                       # quit
    ret = h.execute('DATALOAD()')
    return h, ret


def box_lines(name, res, width=26):
    """what a program returns, as the Program Catalog's box shows it after a run (verify_CICatcher_beta2l.py)"""
    out, cur = [], ''
    for w in ('%s "%s"' % (name, res)).split(' '):
        if cur and len(cur) + 1 + len(w) > width:
            out.append(cur)
            cur = w
        else:
            cur = (cur + ' ' + w) if cur else w
    return out + [cur]


OLD = older()
print('=== DataLoad beta 1i (programs/%s) against beta 1h (%s)' % (NAME, 'found' if OLD else 'NOT FOUND'))
if not OLD:
    check('beta 1h found', False)
    sys.exit(1)
OV.install()

# ===================================================================== N
print('=== N. the new question')
pairs = [[1, 10], [2, INF], [3, 30], [4, 40]]               # a before-and-after with one "after" missing in row 2
h, ret = run({'M1': pairs}, [1])
q = asked(h)
check('N1 a blank above a value in column 2 asks, before anything is written: "Column 2 has a blank inside"',
      q is not None and q[0] == 'Column 2 has a blank inside', q)
check('N2 its items: "Pairs: keep complete rows", "Separate groups: drop blanks", "Cancel"',
      q is not None and q[1] == ['Pairs: keep complete rows', 'Separate groups: drop blanks', 'Cancel'], q)
check('N3 pairs: only the complete rows, so D1 = {1, 3, 4} and D2 = {10, 30, 40} still match row for row',
      L(h, 'D1') == [1, 3, 4] and L(h, 'D2') == [10, 30, 40], (L(h, 'D1'), L(h, 'D2')))
check('N4 the line DataLoad returns says so: "DataLoad: M1 -> D1-D2 (4 rows, 3 complete)"',
      ret == 'DataLoad: M1 %s D1-D2 (4 rows, 3 complete)' % ARROW, ret)
check('N5 no harness warnings', not h.warnings, h.warnings[:3])
h, ret = run({'M1': pairs}, [2])
check('N6 separate groups: beta 1h\'s way, each blank left out of its own column (D1 4 values, D2 3)',
      L(h, 'D1') == [1, 2, 3, 4] and L(h, 'D2') == [10, 30, 40] and ret == 'DataLoad: M1 %s D1-D2 (4 rows)' % ARROW,
      (L(h, 'D1'), L(h, 'D2'), ret))
for pick, what in ((3, 'Cancel'), (0, 'Esc')):
    h, ret = run({'M1': pairs}, [pick], esc_lists=False)
    check('N7 %s at the question: nothing written (D1 as it was, D2 never written), "nothing loaded"' % what,
          L(h, 'D1') == [] and h.globals_.get('D2') is None and ret == 'DataLoad: nothing loaded'
          and not [d for d in h.chooses if d.title.endswith('hold data') or d.title.endswith('holds data')], (L(h, 'D1'), ret))
two = [[1, 10, 100], [2, INF, 200], [3, 30, INF], [4, 40, 400]]
h, ret = run({'M1': two}, [1])
q = asked(h)
check('N8 holes in two columns: "2 columns have blanks inside"; pairs keep rows 1 and 4 only',
      q is not None and q[0] == '2 columns have blanks inside' and L(h, 'D1') == [1, 4] and L(h, 'D2') == [10, 40]
      and L(h, 'D3') == [100, 400], (q, L(h, 'D1'), L(h, 'D3')))
pad = [[1, 10, 5], [2, 20, INF], [3, INF, INF], [4, INF, INF]]       # beta 1b's padded columns: blanks at the foot only
h, ret = run({'M1': pad}, [])
check('N9 blanks only at the foot of the columns (groups of unequal size): no question, lengths 4, 2 and 1 as before',
      asked(h) is None and L(h, 'D1') == [1, 2, 3, 4] and L(h, 'D2') == [10, 20] and L(h, 'D3') == [5], asked(h))
h, ret = run({'M1': [[1], [INF], [3], [4]]}, [])
check('N10 one column with a blank inside: no question (a single column has no partner), the blank left out',
      asked(h) is None and L(h, 'D1') == [1, 3, 4], (asked(h), L(h, 'D1')))
wide = [[r * 100 + c for c in range(1, 13)] for r in range(1, 7)]   # 6 rows, 12 columns
wide[2][10] = INF                                                   # a hole in column 11, which is not loaded
h, ret = run({'M1': wide}, [])
check('N11 a hole only in a column past the ninth (not loaded) asks nothing, and the nine lists are whole',
      asked(h) is None and all(len(L(h, 'D%d' % j)) == 6 for j in range(1, 10)), asked(h))
wide[3][2] = INF                                                    # and one in column 3
h, ret = run({'M1': wide}, [1])
check('N12 a hole in column 3 of 12: pairs drop row 4 only; the blank in column 11 (not loaded) drops nothing',
      asked(h) is not None and L(h, 'D1') == [101, 201, 301, 501, 601] and L(h, 'D9') == [109, 209, 309, 509, 609],
      (asked(h), L(h, 'D1')))
h, ret = run({'M1': [[1, INF], [INF, 2], [3, INF], [INF, 4]]}, [1], esc_lists=False)
msgs = [m.text for m in h.msgboxes]
check('N13 pairs with no complete row: a box says so and nothing is written',
      L(h, 'D1') == [] and h.globals_.get('D2') is None and any('no complete row' in m for m in msgs), (msgs, ret))

# the Rossi data with holes punched in: every kept row is a whole row of the original, in order
R = rossi()
check('N14 the Rossi data from SurvLab: 432 rows of 5', len(R) == 432 and all(len(r) == 5 for r in R))
holes = {(7, 1), (19, 3), (102, 4), (250, 0), (251, 2), (431, 1)}  # (row, column), 0-based; row 431 is the last
Rh = [[INF if (i, j) in holes else v for j, v in enumerate(r)] for i, r in enumerate(R)]
h, ret = run({'M1': Rh}, [1])
keep = [i for i in range(432) if not any((i, j) in holes for j in range(5))]
cols = [L(h, 'D%d' % (j + 1)) for j in range(5)]
rows_back = [list(r) for r in zip(*cols)] if all(cols) else []
check('N15 Rossi with 6 blanks in 6 rows: pairs give 426 rows, each a whole row of the original, in file order',
      len(keep) == 426 and rows_back == [R[i] for i in keep], (len(rows_back), ret))
check('N16 the line: "DataLoad: M1 -> D1-D5 (432 rows, 426 complete)"',
      ret == 'DataLoad: M1 %s D1-D5 (432 rows, 426 complete)' % ARROW, ret)
h, ret = run({'M1': Rh}, [2])
check('N17 the same data as separate groups: each column loses only its own blanks (431, 430, 431, 431, 431 values; '
      'column 2 has two, one of them in the last row)',
      [len(L(h, 'D%d' % j)) for j in range(1, 6)] == [431, 430, 431, 431, 431], [len(L(h, 'D%d' % j)) for j in range(1, 6)])
h = H({'M1': pairs})
h.choose(5)                       # Lists: C (Statistics 2Var)
h.choose(1)
h.choose(1)                       # pairs
h.press('Esc')
h.choose(7)
ret = h.execute('DATALOAD()')
check('N18 Statistics 2Var (x, y for ScatterLab): C1 = {1, 3, 4}, C2 = {10, 30, 40}; no D list written',
      L(h, 'C1') == [1, 3, 4] and L(h, 'C2') == [10, 30, 40] and L(h, 'D1') == [] and h.globals_.get('D2') is None,
      (L(h, 'C1'), L(h, 'C2'), ret))
full = {'D1': [5.0, 6.0], 'D2': [7.0], 'D3': [1.0], 'D5': [2.0], 'D7': [3.0], 'D9': [4.0], 'C1': []}
for pick, cleared in ((1, True), (2, False)):
    h = H({'M9': pairs}, app=dict(full))
    h.choose(4)                   # which matrix?
    h.choose(10)                  # M9
    h.choose(1)                   # Columns
    h.choose(1)                   # pairs
    h.choose(pick)                # 1 = fill and clear the rest, 2 = fill and keep
    h.press('Esc')
    h.choose(7)
    ret = h.execute('DATALOAD()')
    rest = [L(h, 'D%d' % k) for k in (3, 5, 7, 9)]
    want = 'DataLoad: M9 %s D1-D2 (4 rows, 3 complete)%s' % (ARROW, ', D3, D5, D7, D9 cleared' if cleared else '')
    check('N19 lists that hold data, %s: the question comes first, then the lists\' own; D3, D5, D7, D9 %s'
          % ('"clear"' if cleared else '"keep"', 'emptied' if cleared else 'kept'),
          L(h, 'D1') == [1, 3, 4] and L(h, 'D2') == [10, 30, 40] and ret == want
          and rest == ([[], [], [], []] if cleared else [[1.0], [2.0], [3.0], [4.0]])
          and [d.title for d in h.chooses].index('Column 2 has a blank inside') < [d.title for d in h.chooses].index('D1-D3, D5, D7, D9 hold data'),
          (ret, rest, [d.title for d in h.chooses]))
# the longest line the pairs load can return: 9,999 rows of which 9,998 complete, M9, two lists, the rest cleared
longest = 'DataLoad: M9 %s D1-D2 (9,999 rows, 9,998 complete), D3, D5, D7, D9 cleared' % ARROW
bl = box_lines('DATALOAD', longest)
print('   the longest return line (%d characters) in the Program Catalog\'s box:' % len(longest))
for x in bl:
    print('     | ' + x)
check('N20 the longest line DataLoad can return after a pairs load is under 100 characters and fits the box\'s 5 lines',
      len(longest) < 100 and len(bl) <= 5, (len(longest), len(bl)))
ttl = ['Column %d has a blank inside' % j for j in range(1, 10)] + ['%d columns have blanks inside' % k for k in range(2, 10)]
check('N21 every title the question can have is 31 characters or fewer, and each item 30 or fewer',
      max(len(t) for t in ttl) <= 31 and max(len(i) for i in ('Pairs: keep complete rows', 'Separate groups: drop blanks')) <= 30,
      max(len(t) for t in ttl))

# ===================================================================== P
print('=== P. the help')
h = H({'M1': pairs})
h.choose(6)                       # Help
h.choose(7)
h.execute('DATALOAD()')
drawn = [t.text for t in h.texts if str(t.text).startswith('DataLoad help')]
check('P1 four pages: "DataLoad help 1/4: What it does", "2/4: Getting data in", "3/4: Blank cells", "4/4: Then run"',
      re.findall(r'dd_Frame\("(DataLoad help [^"]+)"\)', SRC) ==
      ['DataLoad help 1/4: What it does', 'DataLoad help 2/4: Getting data in', 'DataLoad help 3/4: Blank cells',
       'DataLoad help 4/4: Then run'])
p3 = re.search(r'dd_Frame\("DataLoad help 3/4: Blank cells"\);(.*?)dd_WaitAny\(\);', SRC, re.S).group(1)
p3t = re.findall(r'TEXTOUT_P\("([^"]*)"', p3)
check('P2 page 3 says what the program does: a blank at the foot ends its column; a blank above a value asks; pairs '
      'keep the complete rows; separate groups keep their own values',
      'AT THE FOOT OF A COLUMN (groups of unequal sizes):' in p3t and 'ABOVE A VALUE, with two or more columns to load:' in p3t
      and 'rows with a value in every column are kept, so each' in p3t and 'SEPARATE GROUPS: each column keeps all of its own' in p3t, p3t)


def helptext(s):
    m = re.search(r'LOCAL dd_Help\(\)\nBEGIN\n(.*?)\nEND;', s, re.S)
    return m.group(1)


old_h = helptext(OLD).replace('help 1/3', 'help 1/4').replace('help 2/3', 'help 2/4').replace('help 3/3', 'help 4/4')
old_h = old_h.replace('"Blank cells (9.99999999999E499) are left out."', '"Blank cells (9.99999999999E499) are left out: see page 3."')
new_h = helptext(SRC)
new_wo3 = re.sub(r' // beta 1i: the page on blank cells \(Round 20\)\n dd_Frame\("DataLoad help 3/4: Blank cells"\);.*?dd_WaitAny\(\);\n',
                 '', new_h, flags=re.S)
check('P3 pages 1, 2 and 4 are beta 1h\'s pages 1, 2 and 3 word for word, but for the titles and page 1\'s line on blanks',
      new_wo3 == old_h)
check('P4 the help was drawn to its end in the harness: its four pages, in order, and no warnings',
      drawn == ['DataLoad help 1/4: What it does', 'DataLoad help 2/4: Getting data in', 'DataLoad help 3/4: Blank cells',
                'DataLoad help 4/4: Then run'] and not h.warnings, (drawn, h.warnings[:2]))

# ===================================================================== S
print('=== S. static')


def routines(s):
    out = {}
    for m in re.finditer(r'^(?:LOCAL |EXPORT )?(\w+)\(([^)]*)\)\nBEGIN\n(.*?)^END;', s, re.M | re.S):
        out[m.group(1)] = m.group(0)
    return out


ro, rn = routines(OLD), routines(SRC)
changed = sorted(k for k in ro if k in rn and ro[k] != rn[k])
gone = sorted(k for k in ro if k not in rn)
new = sorted(k for k in rn if k not in ro)
check('S1 beta 1h\'s routines are in beta 1i word for word but dd_LoadCols and dd_Help; none is gone',
      changed == ['dd_Help', 'dd_LoadCols'] and not gone, (changed, gone))
check('S2 the four new routines are dd_Holes, dd_Full, dd_Pick and dd_AskHoles, all tagged dd_',
      new == ['dd_AskHoles', 'dd_Full', 'dd_Holes', 'dd_Pick'], new)
locs = re.findall(r'^\s*LOCAL ([^;(]+);', SRC, re.M)
check('S3 no LOCAL statement holds more than 6 names', max(len(x.split(',')) for x in locs) <= 6,
      [x for x in locs if len(x.split(',')) > 6])
bad = []
for m in re.finditer(r'CHOOSE\((\w+),', SRC):
    before = SRC[max(0, m.start() - 200):m.start()]
    if not re.search(r'\b%s := 0;' % m.group(1), before):
        bad.append(m.group(1))
check('S4 every CHOOSE sets its index to 0 first (its own return value is never tested)', not bad, bad)
code = '\n'.join(l.split('//')[0] for l in SRC.split('\n'))
check('S5 no "!=", and the code is ASCII outside its strings',
      '!=' not in code and not any(ord(c) > 127 for c in re.sub(r'"[^"\n]*"', '', code)))
check('S6 the header names beta 1i and keeps the disclaimer', '// DATALOAD - beta 1i' in SRC and 'DISCLAIMER: a teaching' in SRC)
check('S7 dd_Column (each blank out of its own column) is beta 1h\'s, word for word, and dd_LoadGroups too',
      rn.get('dd_Column') == ro.get('dd_Column') and rn.get('dd_LoadGroups') == ro.get('dd_LoadGroups'))

# ===================================================================== R
print('=== R. regression: the beta 1b script on beta 1i')
tmp = tempfile.mkdtemp()
shutil.copy(os.path.join(HERE, 'verify_DataLoad_beta1b.py'), tmp)
shutil.copy(PROG, os.path.join(tmp, NAME))
shutil.copy(os.path.join(HERE, '..', 'programs', 'SurvLab_beta1h.txt'), os.path.join(tmp, 'SurvLab_beta1b.txt'))
env = dict(os.environ, DL_TOOLS=os.path.abspath(TOOLS))
r = subprocess.run([sys.executable, os.path.join(tmp, 'verify_DataLoad_beta1b.py'), os.path.join(tmp, NAME)],
                   capture_output=True, text=True, env=env, timeout=3000)
lines = r.stdout.split('\n')
fails = [x for x in lines if x.startswith('FAIL ')]
passes = [x for x in lines if x.startswith('PASS ')]
print('   beta 1b\'s script on beta 1i: %d PASS, %d FAIL' % (len(passes), len(fails)))
for x in fails:
    print('     ' + x[:160])
check('R1 every check of the beta 1b script passes on beta 1i but G6 (it reads beta 1h\'s three help titles) and L1 '
      '(it reads the layout records under its own program\'s file name; L below reads them for beta 1i)',
      len(passes) > 50 and [x.split()[1] for x in fails] == ['G6', 'L1'], (len(passes), fails[:3], r.stderr[-400:]))

# ===================================================================== L
print('=== L. layout (text_overlap_v1 over every screen above, against beta 1h\'s same pages)')
# beta 1h's help and its padded load, drawn the same way under its own file name, for the findings it already had
oldp = os.path.join(tempfile.mkdtemp(), OLDNAME)
open(oldp, 'w', encoding='utf-8').write(OLD)
ho = Harness(oldp, idle_key=4, home_minus=True, app_data={'D1': [], 'C1': []})
for k in range(10):
    ho.globals_['M%d' % k] = Matrix([[0.0]])
ho.globals_['M1'] = Matrix([[float(x) for x in r] for r in pairs])
ho.execute('dd_Init()')
ho.choose(6)
ho.choose(1)
ho.press('Esc')
ho.choose(7)
ho.execute('DATALOAD()')
rep = OV.report()


def findings(prefix):
    tg = [t for t in rep if t.startswith(prefix)]
    if not tg:
        return None
    f = rep[tg[0]]
    out = [('overlap', c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
    out += [('straddle', x['text'], x['edge']) for x in f['straddles'] if x['firm']]
    out += [('overrun', x['text'], None) for x in f['overruns'] if x['firm']]
    print('   %s: screens %d distinct of %d; firm findings %d' % (tg[0], f['screens_distinct'], f['screens_total'], len(out)))
    return out


fn, fo = findings('DataLoad_beta1i'), findings('DataLoad_beta1h')
new_firm = [x for x in (fn or []) if x not in (fo or [])]
GW = __import__('json').load(open(os.path.join(HERE, 'round11', 'glyph_widths_vc.json')))


def vc_width(s, font=1):
    return sum(GW.get(str(ord(c)), [7, 7, 8])[font - 1] for c in s)


for x in new_firm:
    print('     new firm finding at the average glyph width: %s %r -> %d px at the measured widths' % (x[0], x[1], vc_width(x[1])))
check('L1 no firm overlap or frame straddle on any screen; every firm overrun is either one that beta 1h\'s same page '
      'already had (its lines were measured with the calculator\'s glyphs in round 17) or a new line that fits by the '
      'Virtual Calculator\'s measured glyph widths (x = 8 plus the line, at most 312 px)',
      fn is not None and fo is not None and not [x for x in new_firm if x[0] != 'overrun']
      and all(8 + vc_width(x[1]) <= 312 for x in new_firm), new_firm)
lines_new = [t for t in re.findall(r'TEXTOUT_P\("([^"]*)", G1, 8, \d+, 1,', helptext(SRC)) if t not in helptext(OLD)]
widths = [(8 + vc_width(t), t) for t in lines_new]
print('   the help\'s new lines at the measured widths: widest %d px of 320' % max(w for w, _ in widths))
check('L2 every new help line (page 3\'s twelve and page 1\'s line on blanks) fits by the measured glyph widths, 312 px or less',
      len(lines_new) == 13 and max(w for w, _ in widths) <= 312, (len(lines_new), widths))

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for x in FAIL:
    print('  FAILED: ' + x)
sys.exit(1 if FAIL else 0)
