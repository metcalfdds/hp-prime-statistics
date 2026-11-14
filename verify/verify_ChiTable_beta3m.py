#!/usr/bin/env python3
"""verify_ChiTable_beta3m.py -- checks ChiTable beta 3m (13 Nov 2026): the exact test for the 2 x 3 and 3 x 2 tables
(Roger: "Could we do an exact test for a bigger table?").  Runs from the repository alone (Lessons Learned section 14 rule
18): beta 3l from git, the build script verify/round13/make_chitable_3m.py, the harness from tools/ (HPKIT for the kit).
  T1  the build makes programs/ChiTable_beta3m.txt byte for byte from beta 3l.
  T2  every line that differs from beta 3l is a line of one of the build's replacements.
  X1  csFishRC against a brute-force count of every table with the same totals (Python's exact integers) and against
      R's fisher.test (exact, the network algorithm), on 300 random 2 x 3 and 300 random 3 x 2 tables of small counts,
      60 larger ones, and tables with ties, zero rows and zero columns.  (SciPy 1.18's fisher_exact takes an R x C
      table but answers it by simulation, a different number on every call, so it is not a reference here.)
  X2  more than 10,000 tables returns -1; a table with fewer is counted.
  X3  results page 5: a 2 x 3 and a 3 x 2 table with an expected count below 5 show "exact test (Freeman-Halton): p = ..." with
      csFishRC's p; a table too big to count says to merge cells; a 2 x 2 table points to page 6; a table with every
      E at least 5 keeps beta 3l's line.
  X4  help page 1 names both exact tests; the code is ASCII, has no "!=", and no LOCAL line holds more than 6 names.
  X5  page 5's "Largest surprise" line: a table with no association at all (every O equal to its E) says "just as
      expected" (beta 3l said "MORE than expected", seen on the Virtual Calculator); on 200 random 2 x 2, 2 x 3 and
      3 x 2 tables the line is beta 3l's, word for word, wherever O and E differ at the two decimals shown.
"""
import io, os, re, sys, math, random, subprocess, importlib.util, difflib, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
import shutil, tempfile  # noqa: E402
NEW = os.path.join(REPO, 'programs', 'ChiTable_beta3m.txt')
spec = importlib.util.spec_from_file_location('mk', os.path.join(HERE, 'round13', 'make_chitable_3m.py'))
mk = importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
res = []


def rec(tag, ok, msg):
    res.append(ok)
    print('%-3s %s  %s' % (tag, 'PASS' if ok else 'FAIL', msg), flush=True)


new = io.open(NEW, encoding='utf-8', newline='').read()
rec('T1', mk.build() == new, 'make_chitable_3m.py builds programs/ChiTable_beta3m.txt byte for byte')
old_l, new_l = mk.OLD.split('\n'), new.split('\n')
pieces = set(l for a, b in mk.EDITS for l in (a + '\n' + b).split('\n'))
bad = []
for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old_l, new_l, autojunk=False).get_opcodes():
    if t != 'equal':
        bad += [l for l in old_l[i1:i2] + new_l[j1:j2] if l not in pieces]
rec('T2', not bad, 'every changed line belongs to a replacement' + ('' if not bad else ': ' + repr(bad[:3])))


def brute(t):
    """two-sided p of the exact test, from every table with the same totals, in exact integers"""
    if len(t) == 3:
        t = [[r[0] for r in t], [r[1] for r in t]]
    (x1, x2, x3), (y1, y2, y3) = t
    r1, c = x1 + x2 + x3, (x1 + y1, x2 + y2, x3 + y3)
    n = sum(c)
    def ways(a, b):
        cc = r1 - a - b
        return math.comb(c[0], a) * math.comb(c[1], b) * math.comb(c[2], cc)
    obs = ways(x1, x2); tot = math.comb(n, r1); s = 0
    for a in range(0, min(c[0], r1) + 1):
        for b in range(0, min(c[1], r1 - a) + 1):
            if 0 <= r1 - a - b <= c[2]:
                w = ways(a, b)
                if w <= obs * (1 + 1e-7):
                    s += w
    return s / tot


def ntables(t):
    if len(t) == 3:
        t = [[r[0] for r in t], [r[1] for r in t]]
    (x1, x2, x3), (y1, y2, y3) = t
    r1, c1, c2, c3 = x1 + x2 + x3, x1 + y1, x2 + y2, x3 + y3
    return sum(min(c2, r1 - a) - max(0, r1 - a - c3) + 1 for a in range(max(0, r1 - c2 - c3), min(c1, r1) + 1))


H = Harness(NEW, idle_key=4)
def ppl_p(t):
    nr, nc = len(t), len(t[0])
    H.globals_.update({'csNR': float(nr), 'csNC': float(nc), 'csO': [float(v) for row in t for v in row]})
    return H.execute('csFishRC()')


random.seed(13)
cases = [[[random.randint(0, 12) for _ in range(3)] for _ in range(2)] for _ in range(300)]
cases += [[[random.randint(0, 12) for _ in range(2)] for _ in range(3)] for _ in range(300)]
cases += [[[random.randint(0, 60) for _ in range(3)] for _ in range(2)] for _ in range(30)]
cases += [[[random.randint(0, 60) for _ in range(2)] for _ in range(3)] for _ in range(30)]
cases += [[[2, 2, 2], [2, 2, 2]], [[3, 1, 2], [1, 3, 2]], [[5, 0, 0], [0, 5, 0]], [[0, 0, 0], [3, 4, 5]], [[4, 0, 3], [2, 0, 6]],
          [[1, 0], [0, 1], [1, 0]], [[0, 7], [0, 2], [0, 5]], [[6, 6], [6, 6], [6, 6]], [[1, 2, 3], [3, 2, 1]]]
worst, got, rin = 0.0, [], []
for t in cases:
    if ntables(t) > 10000:
        continue
    p = ppl_p(t); b = brute(t)
    worst = max(worst, abs(p - b)); got.append(p)
    if all(sum(r) > 0 for r in t) and all(sum(col) > 0 for col in zip(*t)):
        rin.append((len(got) - 1, t))
rec('X1', worst < 1e-9, '%d tables: largest difference from the brute-force count %.1e' % (len(got), worst))
if shutil.which('Rscript'):
    td = tempfile.mkdtemp(); fn = os.path.join(td, 'tables.txt')
    io.open(fn, 'w').write('\n'.join('%d %d %s' % (len(t), len(t[0]), ' '.join(str(v) for row in t for v in row)) for _, t in rin))
    rs = ('L <- readLines("%s"); for (l in L) { v <- as.numeric(strsplit(l, " ")[[1]]); '
          'm <- matrix(v[-(1:2)], nrow = v[1], byrow = TRUE); cat(sprintf("%%.15g\\n", fisher.test(m)$p.value)) }' % fn)
    out = subprocess.run(['Rscript', '-e', rs], capture_output=True, text=True).stdout.split()
    wr = max(abs(got[i] - float(o)) for (i, _), o in zip(rin, out)) if len(out) == len(rin) else 1.0
    rec('X1', len(out) == len(rin) and wr < 1e-9, "%d tables with no empty row or column: largest difference from R's fisher.test %.1e" % (len(rin), wr))
else:
    print('X1  skipped: R not installed (apt-get install r-base-core)')
big, ok_big = [[60, 60, 60], [60, 60, 60]], [[40, 40, 40], [40, 40, 40]]
rec('X2', ntables(big) > 10000 and ppl_p(big) == -1, 'a 2 x 3 table of 360 cases (%d tables) returns -1' % ntables(big))
rec('X2', ntables(ok_big) <= 10000 and abs(ppl_p(ok_big) - brute(ok_big)) < 1e-9, 'a 2 x 3 table of 240 cases (%d tables) is counted' % ntables(ok_big))


def page5(t, path=NEW, y=181):
    h = Harness(path, idle_key=4)
    h.execute('csInit()')
    h.globals_.update({'csNR': float(len(t)), 'csNC': float(len(t[0])), 'csO': [float(v) for row in t for v in row], 'csHas': 1.0})
    h.execute('csCompute()')
    h.execute('csPageInterp()')
    s = h.screens[-1]
    return [x.text for x in s.text_at(y, 1)], h


small23, small32 = [[3, 1, 0], [1, 4, 2]], [[3, 1], [0, 4], [2, 2]]
for t in (small23, small32):
    l, h = page5(t)
    want = 'exact test (Freeman-Halton): p = %s' % ('%.4f' % brute(t))
    rec('X3', len(l) == 1 and want in l[0] and 'shaky' in l[0], '%dx%d with E < 5: %r' % (len(t), len(t[0]), l))
l, h = page5([[1250, 1250, 2], [1250, 1250, 2]])
rec('X3', len(l) == 1 and 'too many tables to count: merge cells.' in l[0], 'too big to count: %r' % l)
l, h = page5([[3, 1], [1, 3]])
rec('X3', len(l) == 1 and "see Fisher's exact test, page 6." in l[0], '2x2 with E < 5: %r' % l)
l, h = page5([[30, 20, 25], [20, 30, 25]])
rec('X3', len(l) == 1 and l[0].startswith('Association is not causation'), 'every E at least 5: %r' % l)
help1 = [l for l in new.split('\n') if 'If not, use the exact test (page 6 for a 2x2,' in l or 'page 5 for 2x3 and 3x2) or merge sparse categories.' in l]
rec('X4', len(help1) == 2, 'help page 1 names both exact tests')
code = [l.split('//')[0] for l in new.split('\n')]
rec('X4', all(ord(ch) < 128 for ch in new), 'the file is ASCII')
rec('X4', not any('!=' in c for c in code), 'no "!=" in the code')
rec('X4', all(len(c.split('LOCAL', 1)[1].split(',')) <= 6 for c in code if c.strip().startswith('LOCAL')), 'no LOCAL line holds more than 6 names')
OLDF = os.path.join(tempfile.mkdtemp(), 'ChiTable_beta3l.txt')
io.open(OLDF, 'w', encoding='utf-8', newline='').write(mk.OLD)
flat = [[1250, 1250, 2], [1250, 1250, 2]]
ln, h = page5(flat, NEW, 137)
lo, h = page5(flat, OLDF, 137)
rec('X5', len(ln) == 1 and ln[0].endswith(': just as expected') and lo[0].endswith(': MORE than expected'),
    'no association at all: %r (beta 3l: %r)' % (ln[0] if ln else '', lo[0] if lo else ''))
# one harness for each version, used for every table (a harness for each call ran out of memory)
HN, HO = Harness(NEW, idle_key=4), Harness(OLDF, idle_key=4)


def line137(h, t):
    h.screens.clear()
    h.execute('csInit()')
    h.globals_.update({'csNR': float(len(t)), 'csNC': float(len(t[0])), 'csO': [float(v) for row in t for v in row], 'csHas': 1.0})
    h.execute('csCompute()')
    h.execute('csPageInterp()')
    return [x.text for x in h.screens[-1].text_at(137, 1)], h


random.seed(13)
same = changed = 0; bad5 = []
for k in range(200):
    nr, nc = random.choice(((2, 2), (2, 3), (3, 2)))
    t = [[random.randint(0, 12) for j in range(nc)] for i in range(nr)]
    if min(sum(r) for r in t) == 0 or min(sum(c) for c in zip(*t)) == 0:
        continue
    ln, h = line137(HN, t)
    lo, h = line137(HO, t)
    m = re.match(r'O = ([0-9,]+), E = ([0-9,.]+): ', ln[0]) if ln else None
    eq = bool(m) and float(m.group(1).replace(',', '')) == float(m.group(2).replace(',', ''))
    if ln == lo and not eq:
        same += 1
    elif eq and ln[0].endswith(': just as expected') and lo[0].endswith(': MORE than expected'):
        changed += 1
    else:
        bad5.append((t, ln, lo))
rec('X5', not bad5 and same > 150, '%d random tables: %d lines as in beta 3l, %d "just as expected" where O = E%s'
    % (same + changed + len(bad5), same, changed, '' if not bad5 else '; FAIL ' + repr(bad5[:2])))
print('\n%d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
