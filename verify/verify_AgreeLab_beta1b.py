"""verify_AgreeLab_beta1b.py -- checks AgreeLab beta 1b (28 Oct 2026; layout-only version of beta 1a, same checks) in the PC harness.  Built from verify_AgreeLab_beta1a.py, whose description follows:

Part A: every formula, by calling the program's own routines through the
harness (Lessons Learned 14, rule 19), against
  - ag_ref.py (written from the papers, independently of the PPL),
  - statsmodels.stats.inter_rater (cohens_kappa with its SEs, weighted
    kappa, fleiss_kappa), pingouin.intraclass_corr, scipy, and
  - published numbers (Shrout & Fleiss 1979 / Howell; Bland & Altman 1986;
    R irr's z for Fleiss' data, recorded in statsmodels' tests),
  - brute force (kappa max over every table with the given margins; the
    per-category Fleiss kappa = Fleiss kappa of the collapsed 2-category
    table),
on the presets and on random and edge inputs.
Part B: every menu path in the harness, the numbers ON THE PAGES checked
against the references, no runtime error, no scientific-notation string,
no text estimated off the 320 x 240 screen or past its TEXTOUT_P width, no
MSGBOX over 5 lines.
Prints "N checks, M failures".  Run from anywhere:
  python3 verify_AgreeLab_beta1.py > verify_AgreeLab_beta1_output.txt
"""
import os, sys, math, random, itertools
from decimal import Decimal, ROUND_HALF_UP
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
os.environ.setdefault('HPKIT', '/home/claude/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(ROOT, 'ref'))
sys.path.insert(0, HERE)
import numpy as np
from scipy import stats
import pandas as pd
from statsmodels.stats.inter_rater import cohens_kappa, fleiss_kappa
import pingouin as pg
from ppl_run_v3e import Harness
import ag_ref as R

SRC = os.path.join(ROOT, 'AgreeLab_beta1b.txt')
N_CHECK = 0
FAILS = []


def check(cond, what):
    global N_CHECK
    N_CHECK += 1
    if not cond:
        FAILS.append(what)
        print('FAIL', what)


def close(a, b, tol, what):
    ok = (a is not None and b is not None and abs(a - b) <= tol * max(1.0, abs(b)))
    check(ok, '%s: program %r vs reference %r' % (what, a, b))


def fx(v, d):
    """ag_Fx: ROUND half away from zero, fixed d decimals, -0 -> 0."""
    q = Decimal(repr(float(v))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    if q == 0:
        q = abs(q)
    return '%.*f' % (d, q) if d > 0 else '%d' % int(q)


def gn(v):
    a = abs(v)
    d = 4
    if a >= 1: d = 3
    if a >= 10: d = 2
    if a >= 1000: d = 1
    if a >= 100000: d = 0
    return fx(v, d)


def pe_(p):
    return 'p < 0.0001' if p < 0.0001 else 'p = ' + fx(p, 4)


def H():
    return Harness(SRC, strict=False, idle_key=4)


def G(h, n):
    return h.globals_[n]


# ======================================================================
# PART A: formulas through the routines
# ======================================================================
print('PART A: formulas')
h = H()
h.execute('ag_Init()')


def load_table(h, tab):
    k = len(tab)
    h.globals_.update({'agK': float(k), 'agT': [float(x) for row in tab for x in row]})
    h.execute('ag_TCompute()')


def check_cohen(h, tab, tag):
    load_table(h, tab)
    t = np.asarray(tab, float)
    N = t.sum()
    tok = G(h, 'agTOK')
    if N == 0:
        check(tok == 0, tag + ' empty table -> agTOK 0')
        return
    r = R.cohen(tab) if True else None
    pe = r['pe']
    if pe > 0.999999999:
        check(tok == 2, tag + ' pe = 1 -> agTOK 2')
        return
    check(tok == 1, tag + ' agTOK 1')
    for name, key in [('agPo', 'po'), ('agPe', 'pe'), ('agKa', 'kappa'), ('agSE', 'se'),
                      ('agSE0', 'se0'), ('agKmx', 'kmax'), ('agPab', 'pabak')]:
        close(G(h, name), r[key], 1e-9, tag + ' ' + name)
    # beta 1a: the CI clipped to [-1, 1]; no inference for N < 10, an empty margin or SE = 0
    lo, hi = max(-1.0, r['lo']), min(1.0, r['hi'])
    close(G(h, 'agLo'), lo, 1e-9, tag + ' clipped lower')
    close(G(h, 'agHi'), hi, 1e-9, tag + ' clipped upper')
    check(G(h, 'agTClp') == (1 if (r['lo'] < -1 or r['hi'] > 1) else 0), tag + ' clip flag')
    inf = 1 if (N >= 10 and t.sum(0).min() > 0 and t.sum(1).min() > 0 and r['se'] > 0) else 0
    check(G(h, 'agTInf') == inf, tag + ' inference flag %r (want %r)' % (G(h, 'agTInf'), inf))
    if r['se0'] > 0:
        close(G(h, 'agZ'), r['z'], 1e-9, tag + ' z')
        close(G(h, 'agP'), r['p'], 1e-7, tag + ' p')
    # statsmodels, independent code
    sm = cohens_kappa(t)
    close(G(h, 'agKa'), sm.kappa, 1e-9, tag + ' kappa vs statsmodels')
    close(G(h, 'agSE'), sm.std_kappa, 1e-8, tag + ' SE vs statsmodels')
    close(G(h, 'agSE0'), sm.std_kappa0, 1e-8, tag + ' SE0 vs statsmodels')
    if len(tab) == 2:
        close(G(h, 'agPI'), (t[0, 0] - t[1, 1]) / N, 1e-12, tag + ' prevalence index')
        close(G(h, 'agBI'), (t[0, 1] - t[1, 0]) / N, 1e-12, tag + ' bias index')
    for w, wt in [(1, 'linear'), (2, 'quadratic')]:
        rw = R.wkappa(tab, wt)
        if rw['pe'] > 0.999999999:
            continue
        smw = cohens_kappa(t, wt=wt)
        close(G(h, 'agWK')[w - 1], smw.kappa, 1e-9, tag + ' weighted %s vs statsmodels' % wt)
        close(G(h, 'agWSE')[w - 1], smw.std_kappa, 1e-8, tag + ' weighted %s SE vs statsmodels' % wt)
        close(G(h, 'agWSE0')[w - 1], smw.std_kappa0, 1e-8, tag + ' weighted %s SE0 vs statsmodels' % wt)
        close(G(h, 'agWK')[w - 1], rw['kappa'], 1e-9, tag + ' weighted %s vs ag_ref' % wt)
        if rw['se0'] > 0:
            close(G(h, 'agWP')[w - 1], rw['p'], 1e-7, tag + ' weighted %s p' % wt)


MSW = [[38, 5, 0, 1], [33, 11, 3, 0], [10, 14, 5, 6], [3, 7, 3, 10]]
MSN = [[5, 3, 0, 0], [3, 11, 4, 0], [2, 13, 3, 4], [1, 2, 4, 14]]
PAR1 = [[80, 10], [5, 5]]
PAR2 = [[40, 10], [5, 45]]
for tab, tag in [(MSW, 'MS Winnipeg'), (MSN, 'MS New Orleans'), (PAR1, 'paradox 1'), (PAR2, 'paradox 2')]:
    check_cohen(h, tab, tag)
# the paradox tables: same po, different kappa (help page 3's numbers)
close(R.cohen(PAR1)['po'], 0.85, 1e-12, 'paradox 1 po')
close(R.cohen(PAR2)['po'], 0.85, 1e-12, 'paradox 2 po')
check(fx(R.cohen(PAR1)['kappa'], 2) == '0.32' and fx(R.cohen(PAR2)['kappa'], 2) == '0.70', 'help page 3 kappas 0.32 and 0.70')

# random and edge tables
rng = random.Random(20261026)
edge = [
    [[0, 0], [0, 0]],                      # empty
    [[5, 0], [0, 0]],                      # one cell: pe = 1
    [[3, 0], [2, 0]],                      # rater B one category
    [[0, 4], [6, 0]],                      # total disagreement
    [[7, 0, 0], [0, 5, 0], [0, 0, 9]],     # perfect
    [[1, 0], [0, 1]],                      # N = 2
    [[1, 1], [1, 0]],                      # N = 3
    [[99999, 3], [2, 99999]],              # huge counts
    [[0, 0, 0], [0, 4, 1], [0, 2, 3]],     # an empty category
    [[2] * 6 for _ in range(6)],           # uniform 6 x 6
]
for i, tab in enumerate(edge):
    check_cohen(h, tab, 'edge %d' % i)
# beta 1a (review item 6): the review's tables
check_cohen(h, [[0, 12], [9, 0]], 'review 0/12/9/0')
check(G(h, 'agTClp') == 1 and G(h, 'agLo') == -1, 'review 0/12/9/0: CI clipped at -1')
check(h.execute('ag_PE(agP)') == 'p > 0.9999', 'review 0/12/9/0: p > 0.9999 (%r)' % h.execute('ag_PE(agP)'))
check_cohen(h, [[1, 0], [0, 1]], 'review N = 2 perfect')
check(G(h, 'agTInf') == 0 and G(h, 'agTWhy') == 'N < 10', 'review N = 2: no SE, CI or p (N < 10)')
check(h.execute('ag_PE(0.99996)') == 'p > 0.9999' and h.execute('ag_PE(0.99994)') == 'p = 0.9999', 'ag_PE boundary')
for big in (1.234e11, -5e15, 3.3e30):
    s_ = h.execute('ag_Fx(%r, 2)' % big)
    check('E' in s_ and chr(7431) not in s_ and abs(float(s_.replace(chr(8722), '-')) / big - 1) < 1e-3, 'ag_Fx(%g) by hand: %r' % (big, s_))

for i in range(40):
    k = rng.randint(2, 6)
    tab = [[rng.choice([0, 0, 1, 2, 3, 5, 8, 20, 50]) for _ in range(k)] for _ in range(k)]
    for d in range(k):
        tab[d][d] += rng.randint(0, 30)
    check_cohen(h, tab, 'random %d (k=%d)' % (i, k))

# kappa max: brute force over every table with the same margins
def all_tables(rows, cols):
    k = len(rows)
    if k == 1:
        if sum(cols) == rows[0]:
            yield [list(cols)]
        return
    def rowfill(j, left, colsleft, acc):
        if j == len(colsleft) - 1:
            if left <= colsleft[j]:
                yield acc + [left]
            return
        for v in range(0, min(left, colsleft[j]) + 1):
            yield from rowfill(j + 1, left - v, colsleft, acc + [v])
    for r0 in rowfill(0, rows[0], cols, []):
        rest = [c - v for c, v in zip(cols, r0)]
        for t in all_tables(rows[1:], rest):
            yield [r0] + t

for i in range(30):
    k = rng.randint(2, 3)
    N = rng.randint(3, 9 if k == 3 else 14)
    tab = [[0] * k for _ in range(k)]
    for _ in range(N):
        tab[rng.randrange(k)][rng.randrange(k)] += 1
    rows = [sum(r) for r in tab]
    cols = [sum(tab[i][j] for i in range(k)) for j in range(k)]
    best = max(sum(t[d][d] for d in range(k)) for t in all_tables(rows, cols)) / N
    pe = sum(rows[d] * cols[d] for d in range(k)) / N ** 2
    load_table(h, tab)
    if pe < 0.999999999:
        close(G(h, 'agKmx'), (best - pe) / (1 - pe), 1e-9, 'kappa max brute force %d' % i)
    close(G(h, 'agPoMx'), best, 1e-12, 'po max brute force %d' % i)

# ---------------- Fleiss ----------------
DIAG = [[0, 0, 0, 6, 0], [0, 3, 0, 0, 3], [0, 1, 4, 0, 1], [0, 0, 0, 0, 6], [0, 3, 0, 3, 0], [2, 0, 4, 0, 0],
        [0, 0, 4, 0, 2], [2, 0, 3, 1, 0], [2, 0, 0, 4, 0], [0, 0, 0, 0, 6], [1, 0, 0, 5, 0], [1, 1, 0, 4, 0],
        [0, 3, 3, 0, 0], [1, 0, 0, 5, 0], [0, 2, 0, 3, 1], [0, 0, 5, 0, 1], [3, 0, 0, 1, 2], [5, 1, 0, 0, 0],
        [0, 2, 0, 4, 0], [1, 0, 2, 0, 3], [0, 0, 0, 0, 6], [0, 1, 0, 5, 0], [0, 2, 0, 1, 3], [2, 0, 0, 4, 0],
        [1, 0, 0, 4, 1], [0, 5, 0, 1, 0], [4, 0, 0, 0, 2], [0, 2, 0, 4, 0], [1, 0, 5, 0, 0], [0, 0, 0, 0, 6]]


def check_fleiss(h, cnt, tag):
    c = np.asarray(cnt, float)
    N, q = c.shape
    m = c[0].sum()
    h.globals_.update({'agF': [float(x) for x in c.flatten()], 'agFN': float(N), 'agFQ': float(q), 'agFM': float(m)})
    h.execute('ag_FCompute()')
    r = R.fleiss(cnt)
    if r['Pe'] > 0.999999999:
        check(G(h, 'agFOK') == 2, tag + ' Pe = 1 -> agFOK 2')
        return
    check(G(h, 'agFOK') == 1, tag + ' agFOK 1')
    close(G(h, 'agFK'), fleiss_kappa(c), 1e-9, tag + ' kappa vs statsmodels')
    close(G(h, 'agFPb'), r['Pbar'], 1e-12, tag + ' P-bar')
    close(G(h, 'agFPe'), r['Pe'], 1e-12, tag + ' Pe')
    close(G(h, 'agFSE0'), r['se0'], 1e-9, tag + ' SE0')
    close(G(h, 'agFSEj'), r['sej'], 1e-12, tag + ' SE0 per category')
    close(G(h, 'agFP'), r['p'], 1e-7, tag + ' p')
    for j in range(q):
        col = c[:, j]
        coll = np.column_stack([col, m - col])
        pj = col.sum() / (N * m)
        if 0 < pj < 1:
            # per-category kappa = Fleiss kappa of "category j vs the rest"
            close(G(h, 'agFKj')[j], fleiss_kappa(coll), 1e-9, tag + ' kappa_%d vs collapsed table' % (j + 1))
        else:
            check(G(h, 'agFKj')[j] == 99, tag + ' kappa_%d undefined flag' % (j + 1))
    for i in range(N):
        close(G(h, 'agFPi')[i], r['Pi'][i], 1e-12, tag + ' P_%d' % (i + 1))


check_fleiss(h, DIAG, 'Fleiss diagnoses')
close(G(h, 'agFK'), 0.4302445, 1e-6, 'Fleiss diagnoses kappa vs R irr 0.4302445')
close(G(h, 'agFZ'), 17.65183, 1e-5, 'Fleiss diagnoses z vs R irr 17.65183')
# the two sources of the preset agree (R irr .rda vs statsmodels' copy)
try:
    import pyreadr
    df = pyreadr.read_r(os.path.join(HERE, 'dl', 'diagnoses.rda'))['diagnoses']
    a = np.array([[int(str(v)[0]) for v in row] for row in df.values])
    cnt = [[int((r_ == cc).sum()) for cc in range(1, 6)] for r_ in a]
    check(cnt == DIAG, 'Fleiss preset = R irr diagnoses.rda counts')
except Exception as e:
    print('note: irr .rda not read:', e)
for i in range(25):
    N = rng.randint(1, 40)
    q = rng.randint(2, 9)
    m = rng.randint(2, 12)
    cnt = []
    for _ in range(N):
        row = [0] * q
        bias = rng.randrange(q)
        for _ in range(m):
            row[bias if rng.random() < 0.6 else rng.randrange(q)] += 1
        cnt.append(row)
    check_fleiss(h, cnt, 'Fleiss random %d (N=%d q=%d m=%d)' % (i, N, q, m))
check_fleiss(h, [[3, 0], [3, 0], [3, 0]], 'Fleiss all one category')
check_fleiss(h, [[1, 1], [2, 0]], 'Fleiss N=2 m=2')

# ---------------- ICC ----------------
SF = [[9, 2, 5, 8], [6, 1, 3, 2], [8, 4, 6, 8], [7, 1, 2, 6], [10, 5, 6, 9], [6, 2, 4, 7]]
PEF = [[494, 512], [395, 430], [516, 520], [434, 428], [476, 500], [557, 600], [413, 364], [442, 380], [650, 658],
       [433, 445], [417, 432], [656, 626], [267, 260], [478, 477], [178, 259], [423, 350], [427, 451]]
KEYS = ['ICC1', 'ICC2', 'ICC3', 'ICC1k', 'ICC2k', 'ICC3k']
PGT = ['ICC(1,1)', 'ICC(A,1)', 'ICC(C,1)', 'ICC(1,k)', 'ICC(A,k)', 'ICC(C,k)']


def load_y(h, Y, names=None):
    Y = np.asarray(Y, float)
    n, k = Y.shape
    h.globals_.update({'agY': [float(x) for x in Y.flatten()], 'agYN': float(n), 'agYK': float(k),
                       'agYRN': names or ['R%d' % (j + 1) for j in range(k)], 'agYU': '', 'agBA': 1.0, 'agBB': 2.0})


def icc_points(Y):
    """Point estimates with the beta 1a rules: sums of squares below 1E-10 of
    the total are 0; a denominator at or below 1E-10 of the largest MS is 0
    (undefined, None)."""
    Y = np.asarray(Y, float)
    n, k = Y.shape
    g = Y.mean()
    sst = ((Y - g) ** 2).sum()
    ssr = k * ((Y.mean(1) - g) ** 2).sum()
    ssc = n * ((Y.mean(0) - g) ** 2).sum()
    sse = max(0.0, sst - ssr - ssc)
    tol = 1e-10 * max(sst, 1e-300)
    ssr, ssc, sse = [0.0 if x <= tol else x for x in (ssr, ssc, sse)]
    MR, MC, ME = ssr / (n - 1), ssc / (k - 1), sse / ((n - 1) * (k - 1))
    MW = (ssc + sse) / (n * (k - 1))
    t = 1e-10 * max(MR, MC, ME, MW)
    def f(num, den):
        return num / den if den > t else None
    pts = [f(MR - MW, MR + (k - 1) * MW), f(MR - ME, MR + (k - 1) * ME + k * (MC - ME) / n),
           f(MR - ME, MR + (k - 1) * ME), f(MR - MW, MR), f(MR - ME, MR + (MC - ME) / n), f(MR - ME, MR)]
    return sst, (MR, MC, ME, MW), pts


def check_icc(h, Y, tag, pgcheck=True):
    load_y(h, Y)
    h.execute('ag_ICompute()')
    Y = np.asarray(Y, float)
    n, k = Y.shape
    sst, (MR, MC, ME, MW), pts = icc_points(Y)
    if sst <= 0:
        check(G(h, 'agIOK') == 2, tag + ' all ratings equal -> agIOK 2')
        return
    check(G(h, 'agIOK') == 1, tag + ' agIOK 1')
    for i, key in enumerate(KEYS):
        if pts[i] is None:
            check(G(h, 'agIDf')[i] == 0 and G(h, 'agIC')[i] == -99 and G(h, 'agINo')[i] == 'undefined (denominator 0)',
                  tag + ' ' + key + ' undefined (denominator 0)')
        else:
            check(G(h, 'agIDf')[i] == 1, tag + ' ' + key + ' defined')
            close(G(h, 'agIC')[i], pts[i], 1e-9, tag + ' ' + key)
    full = MR > 0 and ME > 0 and MW > 0
    if not full:
        # the reasons for a missing interval
        for i in (0, 3):
            if pts[i] is not None:
                want = 'no F interval (within MS = 0)' if MW == 0 else ('no F interval (target MS = 0)' if MR == 0 else None)
                if want:
                    check(G(h, 'agICf')[i] == 0 and G(h, 'agINo')[i] == want, tag + ' %s reason %r got %r' % (KEYS[i], want, G(h, 'agINo')[i]))
        for i in (2, 5):
            if pts[i] is not None:
                want = 'no F interval (error MS = 0)' if ME == 0 else ('no F interval (target MS = 0)' if MR == 0 else None)
                if want:
                    check(G(h, 'agICf')[i] == 0 and G(h, 'agINo')[i] == want, tag + ' %s reason %r got %r' % (KEYS[i], want, G(h, 'agINo')[i]))
        return
    r = R.icc(Y)
    L2 = r['ICC2'][1]
    U2 = r['ICC2'][2]
    for i, key in enumerate(KEYS):
        if pts[i] is None:
            continue
        if G(h, 'agICf')[i] == 1:
            lo, hi = r[key][1], r[key][2]
            if key == 'ICC2k':
                if 1 + L2 * (k - 1) <= 0:
                    lo = -1e99
                if 1 + U2 * (k - 1) <= 0:
                    hi = -1e99
            close(G(h, 'agIL')[i], lo, 2e-6, tag + ' ' + key + ' lower')
            close(G(h, 'agIU')[i], hi, 2e-6, tag + ' ' + key + ' upper')
        else:
            check(key in ('ICC2', 'ICC2k') and not (-1 < r['ICC2'][0] < 1 and r['v'] >= 1), tag + ' ' + key + ' has no CI')
        close(G(h, 'agIPv')[i], r[key][6], 1e-7, tag + ' ' + key + ' F test p')
    if pgcheck and n * k >= 5:
        df = pd.DataFrame([(i, j, Y[i, j]) for i in range(n) for j in range(k)], columns=['t', 'r', 'y'])
        p = pg.intraclass_corr(df, 't', 'r', 'y').set_index('Type')
        for i, t in enumerate(PGT):
            if pts[i] is None:
                continue
            close(G(h, 'agIC')[i], p.loc[t, 'ICC'], 1e-9, tag + ' ' + t + ' vs pingouin')
            if G(h, 'agICf')[i] == 1 and G(h, 'agIL')[i] > -1e90 and G(h, 'agIU')[i] > -1e90:
                lo, hi = p.loc[t, 'CI95']
                check(abs(round(G(h, 'agIL')[i], 2) - lo) < 0.0101 and abs(round(G(h, 'agIU')[i], 2) - hi) < 0.0101,
                      tag + ' ' + t + ' CI vs pingouin (2 dp): %r %r vs %r' % (G(h, 'agIL')[i], G(h, 'agIU')[i], (lo, hi)))
            close(G(h, 'agIF')[i], p.loc[t, 'F'], 1e-9, tag + ' ' + t + ' F vs pingouin')


check_icc(h, SF, 'Shrout-Fleiss')
# Shrout & Fleiss's own values (via Howell's page and R irr/psych): .17 .29 .71 .44 .62 .91
pub = ['0.17', '0.29', '0.71', '0.44', '0.62', '0.91']
check([fx(v, 2) for v in G(h, 'agIC')] == pub, 'Shrout-Fleiss ICCs = published .17 .29 .71 .44 .62 .91')
check(fx(G(h, 'agIL')[0], 3) == '-0.133' and fx(G(h, 'agIU')[0], 3) == '0.723', 'ICC(1,1) CI = Howell/psych -0.133 to 0.723')
check_icc(h, PEF, 'peak flow')
for i in range(25):
    n = rng.randint(2, 30)
    k = rng.randint(2, 9)
    base = [rng.gauss(50, 10) for _ in range(n)]
    off = [rng.gauss(0, rng.choice([0.5, 3, 10])) for _ in range(k)]
    Y = [[round(base[a] + off[b] + rng.gauss(0, rng.choice([1, 5, 20])), rng.choice([0, 1, 3])) for b in range(k)] for a in range(n)]
    check_icc(h, Y, 'ICC random %d (n=%d k=%d)' % (i, n, k))
check_icc(h, [[5, 5], [5, 5], [5, 5]], 'ICC all equal', pgcheck=False)
check_icc(h, [[1, 3], [2, 4], [5, 7]], 'ICC offset only (MSE = 0)', pgcheck=False)
# beta 1a (review item 3): the review's constant offset {1,6},{2,7},{3,8},{4,9}
check_icc(h, [[1, 6], [2, 7], [3, 8], [4, 9]], 'ICC review offset', pgcheck=False)
check(fx(G(h, 'agIC')[2], 3) == '1.000' and fx(G(h, 'agIC')[1], 3) == '0.118' and fx(G(h, 'agIC')[0], 3) == '-0.579',
      'review offset: ICC(3,1) 1, ICC(2,1) 0.118, ICC(1,1) -0.579: %r' % G(h, 'agIC')[:3])
check(G(h, 'agICf')[1] == 1, 'review offset: ICC(2,1) still has its Satterthwaite interval')
check_icc(h, [[3, 3, 3], [5, 5, 5], [9, 9, 9]], 'ICC perfect agreement', pgcheck=False)
check(all(fx(x, 3) == '1.000' for x in G(h, 'agIC')), 'perfect agreement: every ICC = 1')
check_icc(h, [[1, 2], [2, 1], [1, 2], [2, 1]], 'ICC target MS = 0', pgcheck=False)
# beta 1a (review item 4): ICC(2,k) denominator 0
check_icc(h, [[1, 2, 1], [2, 1, 2], [1, 2, 1], [2, 1, 2]], 'ICC(2,k) denominator 0', pgcheck=False)
check(G(h, 'agIDf')[4] == 0, 'review 4: ICC(2,k) undefined')
for i in range(15):
    n = rng.randint(2, 6); k = rng.randint(2, 4)
    Y = [[rng.choice([1, 2, 3]) for _ in range(k)] for _ in range(n)]
    check_icc(h, Y, 'ICC small integer %d' % i, pgcheck=False)
check_icc(h, [[1, 2], [2, 1], [1, 2]], 'ICC n=3 k=2 negative', pgcheck=True)
check_icc(h, [[1e6, 1.1e6], [2e6, 1.9e6], [3e6, 3.2e6], [-5e5, -4e5]], 'ICC huge and negative', pgcheck=True)

# the fractional-df F quantile against SciPy
for i in range(30):
    a = rng.choice([0.025, 0.05, 0.001, 0.2])
    d1 = rng.choice([1, 2, 5, 17, 40]) + rng.choice([0, 0.37, 0.9])
    d2 = rng.choice([1.5, 3.3, 8.8, 25.1, 160.7, 999.5, 2500.3])
    h.execute('ag_FQ(%r, %r, %r)' % (a, d1, d2))
    v = h.execute('ag_FQ(%r, %r, %r)' % (a, d1, d2))
    close(v, stats.f.isf(a, d1, d2), 1e-4 if max(d1, d2) > 1000 else 2e-7, 'ag_FQ(%g, %g, %g)' % (a, d1, d2))
for i in range(15):
    f = rng.choice([0.2, 1, 3.5, 12, 80])
    d1 = rng.choice([2, 5.5, 13.2])
    d2 = rng.choice([4, 7.7, 30.4])
    v = h.execute('ag_FUp(%r, %r, %r)' % (f, d1, d2))
    close(v, stats.f.sf(f, d1, d2), 1e-8, 'ag_FUp(%g, %g, %g)' % (f, d1, d2))

# ---------------- Bland-Altman ----------------


def check_ba(h, Y, a, b, tag):
    load_y(h, Y)
    h.globals_.update({'agBA': float(a), 'agBB': float(b)})
    h.execute('ag_BCompute()')
    Y = np.asarray(Y, float)
    if len(Y) < 3:
        check(G(h, 'agBOK') == 2, tag + ' n < 3 refused')
        return
    r = R.bland(Y[:, a - 1], Y[:, b - 1])
    check(G(h, 'agBOK') == 1, tag + ' agBOK')
    for nm, key in [('agBDb', 'dbar'), ('agBS', 's'), ('agBLo', 'lo'), ('agBHi', 'hi'), ('agBT', 't'),
                    ('agBSeb', 'seb'), ('agBSL', 'sel')]:
        close(G(h, nm), r[key], 1e-9, tag + ' ' + nm)
    m = (Y[:, a - 1] + Y[:, b - 1]) / 2
    d = Y[:, a - 1] - Y[:, b - 1]
    if np.ptp(m) > 0:
        lr = stats.linregress(m, d)
        close(G(h, 'agB1'), lr.slope, 1e-8, tag + ' slope vs scipy linregress')
        if np.isnan(lr.stderr):
            check(G(h, 'agBSe1') == 0 and G(h, 'agBPb') == -1, tag + ' zero residual: no trend p')
            return
        close(G(h, 'agBSe1'), lr.stderr, 1e-8, tag + ' slope SE vs linregress')
        if lr.stderr > 0:
            close(G(h, 'agBPb'), lr.pvalue, 1e-7, tag + ' slope p vs linregress')


check_ba(h, PEF, 1, 2, 'peak flow')
# Bland & Altman (1986) printed: bias -2.1, s 38.8, SE of bias 9.4, CI -22.0 to 17.8 (t = 2.12),
# 2s limits -79.7 and 75.5
check(fx(G(h, 'agBDb'), 1) == '-2.1' and fx(G(h, 'agBS'), 1) == '38.8', 'B&A 1986 bias -2.1, s 38.8')
check(fx(G(h, 'agBSeb'), 1) == '9.4', 'B&A 1986 SE of bias 9.4')
check(fx(G(h, 'agBT'), 2) == '2.12', 'B&A 1986 t = 2.12')
lo_ = G(h, 'agBDb') - G(h, 'agBT') * G(h, 'agBSeb')
hi_ = G(h, 'agBDb') + G(h, 'agBT') * G(h, 'agBSeb')
check(fx(lo_, 1) == '-22.0' and fx(hi_, 1) == '17.8', 'B&A 1986 bias CI -22.0 to 17.8 (%r %r)' % (lo_, hi_))
# B&A printed -79.7 and 75.5 from the ROUNDED -2.1 and 38.8 (-2.1 -/+ 77.6); unrounded they are -79.6 and 75.4
check(fx(round(G(h, 'agBDb'), 1) - 2 * round(G(h, 'agBS'), 1), 1) == '-79.7' and fx(round(G(h, 'agBDb'), 1) + 2 * round(G(h, 'agBS'), 1), 1) == '75.5', 'B&A 1986 2s limits (from their rounded bias and s)')
check_ba(h, SF, 1, 2, 'Shrout-Fleiss J1-J2')
check_ba(h, SF, 3, 4, 'Shrout-Fleiss J3-J4')
check_ba(h, [[1, 1], [2, 2], [3, 3]], 1, 2, 'BA identical raters')
check_ba(h, [[1, 2], [2, 3]], 1, 2, 'BA n = 2')
for i in range(20):
    n = rng.randint(3, 60)
    Y = [[x, x + rng.gauss(rng.choice([0, 5]), 3) * (1 + rng.choice([0, 0.02]) * x)] for x in [rng.uniform(-50, 500) for _ in range(n)]]
    check_ba(h, Y, 1, 2, 'BA random %d (n=%d)' % (i, n))

# ---------------- the presets against their downloaded sources ----------------
DL = os.path.join(HERE, 'dl')
try:
    import csv, re as _re
    rows = list(csv.reader(open(os.path.join(DL, 'MSPatients.csv'))))
    W_ = [[int(x) for x in r_[1:5]] for r_ in rows[1:]]
    N_ = [[int(x) for x in r_[5:9]] for r_ in rows[1:]]
    check(W_ == MSW and N_ == MSN, 'MS presets = Rdatasets vcd MSPatients CSV')
    sas = open(os.path.join(DL, 'msdiag.sas')).read()
    nums = [int(x) for x in _re.findall(r'-?\d+', sas.split('datalines;')[1].split(';')[0])]
    check(nums[:16] == sum(MSW, []) and nums[16:32] == sum(MSN, []), "MS presets = Friendly's msdiag.sas")
    import pyreadr
    pf = pyreadr.read_r(os.path.join(DL, 'PEFR.rda'))['PEFR']
    w_ = list(pf[(pf.meth == 'Wright') & (pf.repl == 1)].sort_values('item').y)
    m_ = list(pf[(pf.meth == 'Mini') & (pf.repl == 1)].sort_values('item').y)
    check([[int(a_), int(b_)] for a_, b_ in zip(w_, m_)] == PEF, 'peak flow preset = MethComp PEFR replicate 1')
    ba = open(os.path.join(DL, 'ba.txt')).read()
    tb = [[int(x) for x in _re.findall(r'\d+', L)] for L in ba.split('\n') if _re.match(r'\s+\d+\s+\d{3}\s+\d{3}\s+\d{3}\s+\d{3}\s*$', L)]
    check(len(tb) == 17 and [[r_[1], r_[3]] for r_ in tb] == PEF, 'peak flow preset = Bland & Altman 1986 Table 1 (first readings)')
    icc_rd = open(os.path.join(DL, 'ICC.Rd')).read()
    blk = icc_rd.split('sf <- matrix(c(')[1].split(')')[0]
    check([int(x) for x in _re.findall(r'\d+', blk)] == sum(SF, []), 'Shrout-Fleiss preset = psych ICC.Rd example')
except Exception as e:
    check(False, 'source files could not be compared: %s' % e)

# ======================================================================
# PART B: the pages
# ======================================================================
print('PART B: pages')
SK = lambda s: (int((s - 1) * 53.4 + 26), 228)
ALLPAGES = []


def run(script, label, stale=False):
    """script(h) queues events; then AgreeLab runs to Quit."""
    h = Harness(SRC, strict=False, idle_key=4, stale_keys=True) if stale else H()
    script(h)
    try:
        res = h.call('AgreeLab')
    except Exception as e:
        check(False, label + ': runtime error %s %s' % (e, getattr(e, 'ppl_stack', '')))
        return h, None
    check(h.error is None, label + ': error ' + str(h.error))
    if stale:
        check(not h.stale_skips, label + ': pages skipped by a left-over key ' + str(h.stale_skips[:3]))
    check(not h.sci_strings, label + ': scientific strings ' + str(h.sci_strings[:3]))
    for mb in h.msgboxes:
        check(not mb.over_five, label + ': MSGBOX over 5 lines: ' + ' / '.join(mb.lines))
    for p in h.pages:
        ALLPAGES.append((label, p))
    return h, res


def lines_of(p):
    return [t.text for t in p.texts]


def has(p, s):
    return any(s in t for t in lines_of(p))


def page_with(h, s, last=True):
    if not last:
        ps = [p for p in h.pages if has(p, s)]
        return ps[0] if ps else None
    ps = [p for p in h.pages if has(p, s)]
    return (ps[-1] if last else ps[0]) if ps else None


def expect(h, marker, wants, label, last=True):
    p = page_with(h, marker, last)
    check(p is not None, label + ': page with ' + repr(marker))
    if p is None:
        return
    for w in wants:
        check(has(p, w), label + ': ' + repr(w) + ' on the page (' + marker + ')')


# B1: two raters, MS Winnipeg (the default table): Tiles, Kappa, Null, Weights
r = R.cohen(MSW)
rl = R.wkappa(MSW, 'linear')
rq = R.wkappa(MSW, 'quadratic')


def s1(h):
    h.press('Enter')
    h.choose('Two raters: categories')
    h.tap(*SK(2))                     # Kappa
    h.tap(*SK(3))                     # Null
    h.tap(160, 100)                   # tap the curve: a message
    h.tap(*SK(4))                     # Weights (linear)
    h.tap(22 + 31 + 15, 34 + 15)      # a weight tile (1, 2): message
    h.press('Plus')                   # quadratic
    h.tap(*SK(4))                     # Wts on the weights page: back to linear
    h.press('Right')                  # pages wrap: 4 -> 1
    h.press('Esc')
    h.choose('Quit')


h1, res = run(s1, 'B1 MS Winnipeg')
expect(h1, 'agree po =', ['N = 149', 'agree po = ' + fx(r['po'], 3), 'chance pe = ' + fx(r['pe'], 3),
                          'kappa = ' + fx(r['kappa'], 3), fx(r['lo'], 3) + ' to ' + fx(r['hi'], 3),
                          'kappa max = ' + fx(r['kmax'], 3), 'PABAK = ' + fx(r['pabak'], 3),
                          '1-sided z = ' + fx(r['z'], 2), pe_(r['p']), 'Data: Landis & Koch 1977'], 'B1 tiles', last=False)
expect(h1, 'kappa = (po - pe)/(1 - pe)', [
    'observed agreement po = ' + fx(r['po'], 3), 'chance agreement pe = ' + fx(r['pe'], 3),
    'kappa = (po - pe)/(1 - pe) = ' + fx(r['kappa'], 3),
    '95% CI ' + fx(r['lo'], 3) + ' to ' + fx(r['hi'], 3) + ' (SE ' + fx(r['se'], 3),
    ' = ' + fx(r['se0'], 3) + ', z = ' + fx(r['z'], 2), 'one-sided ' + pe_(r['p']),
    'kappa max for these margins = ' + fx(r['kmax'], 3), 'PABAK = (k po - 1)/(k - 1) = ' + fx(r['pabak'], 3),
    'linear ' + fx(rl['kappa'], 3) + ', quadratic ' + fx(rq['kappa'], 3), '"fair": their convention, not a test',
    'Landis & Koch 1977 (Biometrics 33:159-174):'], 'B1 kappa page')
expect(h1, 'Null curve', ['SE' + chr(8320) + ' = ' + fx(r['se0'], 3), 'kappa = ' + fx(r['kappa'], 3) + ' (red): z = ' + fx(r['z'], 2)], 'B1 null page')
expect(h1, 'linear weights', ['linear = ' + fx(rl['kappa'], 3), 'quadratic = ' + fx(rq['kappa'], 3),
                              'SE ' + fx(rl['se'], 3) + ', 95% CI', fx(rl['lo'], 3) + ' to ' + fx(rl['hi'], 3),
                              '1-sided z = ' + fx(rl['z'], 2), 'unweighted = ' + fx(r['kappa'], 3)], 'B1 weights linear')
expect(h1, 'quadratic weights', ['SE ' + fx(rq['se'], 3) + ', 95% CI', fx(rq['lo'], 3) + ' to ' + fx(rq['hi'], 3),
                                 '1-sided z = ' + fx(rq['z'], 2)], 'B1 weights quadratic')
pw = page_with(h1, 'Weights: ordered')
check(pw is not None and any(t.text == '.67' for t in pw.texts), 'B1 weight .67 drawn on a tile')
check(len(h1.msgboxes) == 2, 'B1 two messages (curve, weight tile)')
check(res is not None and res.startswith('AgreeLab: Cohen') and fx(r['kappa'], 3) in res, 'B1 Home summary ' + str(res))

# B2: drag a count, keys, More page actions, typed count, clear
T2 = [row[:] for row in MSW]
T2[1][0] -= 1; T2[1][1] += 1           # drag A2,B1 -> A2,B2
T3 = [row[:] for row in T2]
T3[2][2] += 1                          # select A3,B3 with arrows, then +
T4 = [row[:] for row in T3]
T4[2][0] -= 1; T4[2][2] += 1           # select A3,B1 then ToDiag
T5 = [row[:] for row in T4]
T5[2][2] -= 1; T5[2][0] += 1           # FromDg
T6 = [row[:] for row in T5]
T6[2][0] = 25                          # Type 25 into A3,B1


def s2(h):
    h.press('Enter')
    h.choose('Two raters: categories')
    h.drag([(37, 80), (55, 80), (69, 80)])         # A2,B1 -> A2,B2
    h.press('Down'); h.press('Right')              # A3,B3 (selection was A2,B2)
    h.press('Plus')
    h.press('Left'); h.press('Left')               # A3,B1
    h.tap(*SK(6))                                  # More
    h.tap(*SK(1))                                  # ToDiag
    h.tap(*SK(2))                                  # FromDg
    h.tap(*SK(3))                                  # Type
    h.answer({'ttV': 25.0})
    h.tap(250, 50)                                 # panel: chance pe -> message
    h.tap(150, 180)                                # the bar -> message
    h.press('Enter'); h.choose('Clear the table')
    h.tap(37, 49)                                  # select A1,B1
    h.press('Plus')                                # A1,B1 = 1: N = 1, pe = 1
    h.press('Esc')
    h.choose('Quit')


h2, res = run(s2, 'B2 edits')
for tab, mark, tag in [(T2, '1 moved A2,B1 to A2,B2', 'drag'), (T3, 'tile A3,B3 now', 'plus'),
                       (T4, '1 moved A3,B1 to A3,B3', 'ToDiag'), (T5, '1 moved A3,B3 to A3,B1', 'FromDg'),
                       (T6, 'tile A3,B1 set to 25', 'Type')]:
    rr = R.cohen(tab)
    expect(h2, mark, ['kappa = ' + fx(rr['kappa'], 3), 'N = ' + str(int(np.sum(tab))), 'agree po = ' + fx(rr['po'], 3)], 'B2 ' + tag)
expect(h2, '1 moved A2,B1 to A2,B2', [': kappa ' + fx(r['kappa'], 3) + ' ' + chr(8594) + ' ' + fx(R.cohen(T2)['kappa'], 3)], 'B2 drag message')
expect(h2, 'Cleared:', ['The table is empty:'], 'B2 cleared')
expect(h2, 'tile A1,B1 now 1', ['kappa undefined:'], 'B2 one count: pe = 1')
check(len(h2.msgboxes) == 2, 'B2 two messages (pe, bar)')

# B3: paradox tables (2 x 2 indices) and New Orleans, from the presets menu
for idx, tab, nm in [(3, PAR1, 'lopsided'), (4, PAR2, 'balanced'), (2, MSN, 'New Orleans')]:
    rr = R.cohen(tab)
    N = np.sum(tab)

    def s3(h, idx=idx):
        h.press('Enter')
        h.choose('Load a preset'); h.choose(idx)
        h.tap(*SK(2))
        h.press('Esc')
        h.choose('Quit')
    h3, _ = run(s3, 'B3 ' + nm)
    wants = ['kappa = (po - pe)/(1 - pe) = ' + fx(rr['kappa'], 3), 'kappa max for these margins = ' + fx(rr['kmax'], 3)]
    if len(tab) == 2:
        wants += ['PABAK = 2po - 1 = ' + fx(rr['pabak'], 3) + '; prevalence index ' + fx((tab[0][0] - tab[1][1]) / N, 2),
                  'bias index (b - c)/N = ' + fx((tab[0][1] - tab[1][0]) / N, 2), 'Data: illustrative numbers, not data']
    expect(h3, 'kappa = (po - pe)', wants, 'B3 ' + nm)
    if len(tab) == 2:
        expect(h3, 'agree po =', ['ILLUSTRATIVE NUMBERS, not data'], 'B3 ' + nm + ' tiles label')

# B4: many raters
rf = R.fleiss(DIAG)


def s4(h):
    h.press('Enter')
    h.choose('Many raters')
    h.tap(150, 60)                       # chance line: message
    h.tap(*SK(2))                        # categories
    h.tap(34 + int(276 / 5 * 1.5), 120)  # bar 2
    h.press('Plus')                      # bar 3
    h.tap(*SK(3))                        # subjects
    h.tap(34 + int(276 / 30 * 6.5), 100) # subject 7
    h.press('Minus')                     # subject 6
    h.tap(*SK(4))                        # help (page 5)
    h.press('Esc')
    h.press('Enter'); h.choose('Kappa: overall')
    h.tap(*SK(6))                        # back
    h.choose('Quit')


h4, res = run(s4, 'B4 Fleiss')
expect(h4, 'mean subject agreement', ['30 subjects, 6 ratings each, 5 categories', 'mean subject agreement = ' + fx(rf['Pbar'], 3),
                                      ' = ' + fx(rf['Pe'], 3) + ' (magenta)', "Fleiss' kappa = " + fx(rf['kappa'], 3),
                                      'SE under H' + chr(8320) + ': ' + fx(rf['se0'], 4), 'z = ' + fx(rf['z'], 2) + ', one-sided ' + pe_(rf['p']),
                                      '"moderate": their convention, not a test', 'Data: Fleiss 1971'], 'B4 kappa page')
for j in (2, 3):
    kj = rf['kj'][j - 1]
    zj = kj / rf['sej']
    expect(h4, '%d %s: share p = ' % (j, ['Depression', 'Personality disorder', 'Schizophrenia'][j - 1]) + fx(rf['pj'][j - 1], 3),
           ['kappa = ' + fx(kj, 3) + ', z = ' + fx(zj, 2) + ', one-sided ' + pe_(stats.norm.sf(zj))], 'B4 category %d' % j)
for s in (7, 6):
    row = DIAG[s - 1]
    agree = sum(v * (v - 1) // 2 for v in row)
    expect(h4, 'subject %d: counts ' % s + ', '.join(str(v) for v in row),
           ['%d of 15 rater pairs agree: P = ' % agree + fx(rf['Pi'][s - 1], 3)], 'B4 subject %d' % s)
check(len(h4.msgboxes) == 1, 'B4 one message')
check(res is not None and "Fleiss' kappa = " + fx(rf['kappa'], 3) in res, 'B4 Home summary ' + str(res))

# B5: continuous: the peak-flow preset (default), ICC page, data, BA, stats, pairs
rp = R.icc(PEF)
rb = R.bland([a for a, b in PEF], [b for a, b in PEF])


def s5(h):
    h.press('Enter')
    h.choose('Continuous')
    h.tap(150, 36 + 19 + 5)               # row 2: ICC(2,1)
    h.press('Down')                       # row 3
    h.tap(*SK(2))                         # data
    h.tap(42, 78)                         # target 1, Wright (494): x 42, y 78
    h.tap(*SK(3))                         # BA
    h.tap(*SK(4))                         # stats
    h.tap(*SK(5))                         # help (BA, page 7)
    h.press('Esc')
    h.press('Enter'); h.choose('Help: ICC'); h.press('Esc')
    h.tap(*SK(6))
    h.choose('Quit')


h5, res = run(s5, 'B5 peak flow')
wants = ['n = 17 targets, k = 2 raters; MS: targets ' + gn(rp['MS'][0]) + ',', 'raters ' + gn(rp['MS'][1]) + ', error ' + gn(rp['MS'][2])]
for i, key in enumerate(KEYS):
    wants.append(fx(rp[key][0], 3))
expect(h5, 'ICC: Peak flow', wants, 'B5 ICC page')
expect(h5, 'ICC(2,1) = ' + fx(rp['ICC2'][0], 3) + ', 95% CI ' + fx(rp['ICC2'][1], 3) + ' to ' + fx(rp['ICC2'][2], 3), [], 'B5 ICC(2,1) CI line')
expect(h5, 'ICC(3,1) = ' + fx(rp['ICC3'][0], 3) + ', 95% CI ' + fx(rp['ICC3'][1], 3) + ' to ' + fx(rp['ICC3'][2], 3), [], 'B5 ICC(3,1) CI line')
check(any(('F = ' + fx(rp['ICC2'][3], 2) + ' on 16, 16 df, ' + pe_(rp['ICC2'][6])) in ' '.join(m.lines) for m in h5.msgboxes), 'B5 ICC(2,1) message F and p')
expect(h5, 'target 1, Wright = 494', [], 'B5 data tap')
expect(h5, 'bias ' + gn(rb['dbar']) + ', 95% limits ' + gn(rb['lo']) + ' to ' + gn(rb['hi']) + ' l/min', [], 'B5 BA header')
expect(h5, 'Bland-Altman: the numbers', [
    'bias = mean d = ' + gn(rb['dbar']) + ' l/min, SD of d: s = ' + gn(rb['s']),
    '95% CI for the bias: ' + gn(rb['bias_ci'][0]) + ' to ' + gn(rb['bias_ci'][1]) + ' (t = ' + fx(rb['t'], 3) + ')',
    'limits = bias ' + chr(177) + ' 1.96 s: ' + gn(rb['lo']) + ' to ' + gn(rb['hi']) + ' l/min', 'approx. SE of a limit (B & A 1986) = ' + gn(rb['sel']),
    'approximate: too narrow for small n (Help 7)', 'the paper, rounding, prints -79.7 to 75.5',
    'approx. 95% CI, lower limit: ' + gn(rb['lo_ci'][0]) + ' to ' + gn(rb['lo_ci'][1]),
    'approx. 95% CI, upper limit: ' + gn(rb['hi_ci'][0]) + ' to ' + gn(rb['hi_ci'][1]),
    'with 2s (as in 1986): ' + gn(rb['dbar'] - 2 * rb['s']) + ' to ' + gn(rb['dbar'] + 2 * rb['s']),
    'slope ' + fx(rb['b1'], 4) + ' (SE ' + fx(rb['seb1'], 4) + ')',
    't = ' + fx(rb['tb'], 2) + ' on 15 df, two-sided ' + pe_(rb['pb']), 'no evidence of a trend', 'Data: Bland & Altman 1986'], 'B5 BA stats')
check(res is not None and 'ICC(2,1) = ' + fx(rp['ICC2'][0], 3) in res, 'B5 Home summary ' + str(res))
check(G(h5, 'agBSel') == 0, 'B5 no point selected on the BA plot before a tap (agBSel = %r)' % G(h5, 'agBSel'))
# a tap on point 9 of the BA plot (positions from the program's own axis state after the run)
px = h5.execute('ag_PX(agBM(9))'); py = h5.execute('ag_PY(agBD(9))')
h5.globals_.update({'agScr': 3.0, 'agTapX': float(px + 2), 'agTapY': float(py - 3)})
h5.execute('ag_CTapPt()')
check(G(h5, 'agBSel') == 9 and G(h5, 'agInfo') == '#9: 650.00 and 658.00, mean 654.00, d = -8.000', 'B5 BA tap reads point 9: %r' % G(h5, 'agInfo'))

# B6: Shrout-Fleiss preset; BA pair stepping and point tap
rs = R.icc(SF)


def s6(h):
    h.press('Enter')
    h.choose('Load a preset'); h.choose('Shrout-Fleiss')
    h.tap(*SK(3))                     # BA J1 - J2
    h.press('Plus')                   # J1 - J3
    h.press('Minus')                  # back to J1 - J2
    h.press('Minus')                  # J3 - J4 (wraps)
    h.press('Esc')
    h.choose('Quit')


h6, _ = run(s6, 'B6 Shrout-Fleiss')
expect(h6, 'ICC: Shrout', [fx(rs[k][0], 3) for k in KEYS], 'B6 ICC page')
Ysf = np.array(SF, float)
for a, b in [(1, 3), (3, 4)]:
    rr = R.bland(Ysf[:, a - 1], Ysf[:, b - 1])
    expect(h6, 'Bland-Altman: J%d - J%d' % (a, b), ['bias ' + gn(rr['dbar']) + ', 95% limits ' + gn(rr['lo']) + ' to ' + gn(rr['hi'])], 'B6 BA J%d-J%d' % (a, b))
check(G(h6, 'AG_ICC') == G(h6, 'agIC'), 'B6 AG_ICC export')

# B7: your own data (D1-D9), every kind, with checks and refusals


def s7(h):
    h.globals_.update({'D1': [1., 2., 2., 3., 1., 1., 3.], 'D2': [1., 2., 3., 3., 2., 1., 1.]})
    h.press('Enter')
    h.choose('Use my data'); h.choose('Two raters')
    h.press('Esc')
    h.choose('Quit')


h7, _ = run(s7, 'B7 my two raters')
T7 = [[2, 1, 0], [0, 1, 1], [1, 0, 1]]
expect(h7, 'agree po =', ['kappa = ' + fx(R.cohen(T7)['kappa'], 3), 'N = 7', 'Data: Statistics 1Var lists D1, D2'], 'B7 tiles')

FD = [[3, 1, 0], [0, 4, 0], [2, 2, 0], [1, 3, 0]]


def s8(h):
    cols = list(zip(*FD))
    h.globals_.update({'D1': [float(x) for x in cols[0]], 'D2': [float(x) for x in cols[1]], 'D3': [float(x) for x in cols[2]]})
    h.press('Enter')
    h.choose('Use my data'); h.choose('Many raters')
    h.tap(*SK(2))
    h.press('Plus'); h.press('Plus'); h.press('Plus')   # category 3: never used -> n/a
    h.tap(*SK(6))
    h.choose('Quit')


h8, _ = run(s8, 'B8 my many raters')
rf8 = R.fleiss(FD)
expect(h8, 'mean subject agreement', ["Fleiss' kappa = " + fx(rf8['kappa'], 3), '4 subjects, 4 ratings each, 3 categories'], 'B8')
expect(h8, 'Fleiss: kappa for each', ['n/a'], 'B8 n/a bar')
expect(h8, '3 D3: share p = 0.000', ['kappa undefined: no rating, or every rating, is here'], 'B8 empty category')

YC = [[10, 12, 11], [20, 19, 22], [30, 33, 29], [15, 15, 17], [25, 24, 27]]


def s9(h):
    cols = list(zip(*YC))
    h.globals_.update({'D1': [float(x) for x in cols[0]], 'D2': [float(x) for x in cols[1]], 'D3': [float(x) for x in cols[2]]})
    h.press('Enter')
    h.choose('Use my data'); h.choose('Continuous')
    h.tap(*SK(3)); h.press('Plus'); h.tap(*SK(4))
    h.tap(*SK(6))
    h.choose('Quit')


h9, _ = run(s9, 'B9 my continuous')
r9 = R.icc(YC)
expect(h9, 'ICC: Your data', [fx(r9[k][0], 3) for k in KEYS] + ['n = 5 targets, k = 3 raters'], 'B9 ICC')
Y9 = np.array(YC, float)
r9b = R.bland(Y9[:, 0], Y9[:, 2])
expect(h9, 'Bland-Altman: the numbers', ['bias = mean d = ' + gn(r9b['dbar']), 'd = D1 - D3 for each of 5 targets'], 'B9 BA stats D1-D3')

# refusals: empty lists, unequal lengths, bad codes, unequal row sums, too few
bad_cases = [
    ({}, 'Two raters', 'two lists of the same length'),
    ({'D1': [1., 2.], 'D2': [1.]}, 'Two raters', 'two lists of the same length'),
    ({'D1': [1., 7.], 'D2': [1., 2.]}, 'Two raters', 'is not a whole code 1 to 6'),
    ({'D1': [1., 2.5], 'D2': [1., 2.]}, 'Two raters', 'is not a whole code 1 to 6'),
    ({'D1': [2., 1.], 'D2': [1., 1.]}, 'Many raters', 'every subject needs the same number'),
    ({'D1': [1., 1.], 'D2': [0., 0.]}, 'Many raters', 'Each subject needs 2 or more ratings'),
    ({'D1': [1., 1.]}, 'Many raters', 'at least 2 lists'),
    ({'D1': [1., 2.], 'D2': [1., 2.]}, 'Continuous', '2 or more lists of 3 or more'),
    ({'D1': [1., 2., 3.], 'D2': [1., 2.]}, 'Continuous', 'has a different length'),
    ({'D1': [float(i) for i in range(751)], 'D2': [float(i) for i in range(751)]}, 'Continuous', 'More than 1500 values'),
    ({'D1': [1.] * 201, 'D2': [1.] * 201}, 'Many raters', 'More than 200 subjects'),
]
for i, (dl, item, msg) in enumerate(bad_cases):
    def sb(h, dl=dl, item=item):
        h.globals_.update(dl)
        h.press('Enter')
        h.choose('Use my data'); h.choose(item)
        h.choose('Quit')
    hb, _ = run(sb, 'B10 refusal %d' % i)
    check(any(msg in ' '.join(m.lines) for m in hb.msgboxes), 'B10 refusal %d says %r: %s' % (i, msg, [m.lines for m in hb.msgboxes]))

# degenerate data on the pages: all ratings equal (ICC undefined), all in one category (Fleiss undefined)


def s11(h):
    h.globals_.update({'D1': [5., 5., 5.], 'D2': [5., 5., 5.]})
    h.press('Enter')
    h.choose('Use my data'); h.choose('Continuous')
    for s in (2, 3, 4):
        h.tap(*SK(s))
    h.tap(*SK(6))
    h.choose('Use my data'); h.choose('Many raters')   # D1 = 5,5,5; D2 = 5,5,5: m = 10, two categories
    h.tap(*SK(2)); h.tap(*SK(3))
    h.tap(*SK(6))
    h.choose('Quit')


h11, _ = run(s11, 'B11 degenerate')
expect(h11, 'ICCs not computed:', ['every rating is the same: nothing to correlate'], 'B11 ICC undefined')
expect(h11, 'bias 0.0000, 95% limits 0.0000 to 0.0000', [], 'B11 BA with zero spread')
expect(h11, 'No trend test: every mean is the same.', [], 'B11 no trend test')


def s12(h):
    h.globals_.update({'D1': [3., 3.], 'D2': [0., 0.]})
    h.press('Enter')
    h.choose('Use my data'); h.choose('Many raters')
    h.tap(*SK(2)); h.tap(*SK(3))
    h.tap(*SK(6))
    h.choose('Quit')


h12, _ = run(s12, 'B12 Fleiss one category')
expect(h12, 'Every rating is in one category', [], 'B12 Fleiss undefined')
expect(h12, 'kappa is undefined for these data.', [], 'B12 categories page')

# new table, a typed k, then the main-menu Help through all nine pages


def s13(h):
    h.press('Enter')
    h.choose('New two-rater table')
    h.answer({'ntK': 2.0})
    h.tap(*SK(2)); h.tap(*SK(3)); h.tap(*SK(4))
    h.press('Esc')
    h.choose('Help')
    for _ in range(9):
        h.press('Enter')
    h.choose('Quit')


h13, _ = run(s13, 'B13 new table + help')
expect(h13, 'The table is empty:', [], 'B13 empty tiles')
expect(h13, 'The table is empty: nothing to compute.', [], 'B13 empty kappa page')
expect(h13, 'Nothing to draw', [], 'B13 empty null page')
for k in range(1, 10):
    check(page_with(h13, '%d/9 ' % k) is not None, 'B13 help page %d shown' % k)

# a refused k and the INPUT cancel


def s14(h):
    h.press('Enter')
    h.choose('New two-rater table'); h.answer({'ntK': 7.0})
    h.choose('Quit')


h14, _ = run(s14, 'B14 k = 7 refused')
check(any('k must be a whole number from 2 to 6' in ' '.join(m.lines) for m in h14.msgboxes), 'B14 refusal message')

# every preset loads and shows its source line
for i, (nm, mark) in enumerate([('MS diagnosis: Winnipeg', 'Data: Landis & Koch 1977'), ('MS diagnosis: New Orleans', 'Data: Landis & Koch 1977'),
                                ('Paradox: lopsided', 'ILLUSTRATIVE NUMBERS'), ('Paradox: balanced', 'ILLUSTRATIVE NUMBERS'),
                                ('Fleiss 1971', 'Data: Fleiss 1971'), ('Peak flow', 'bias '), ('Shrout-Fleiss', 'ICC: Shrout')]):
    def sp(h, i=i):
        h.press('Enter')
        h.choose('Load a preset'); h.choose(i + 1)
        h.press('Esc')
        h.choose('Quit')
    hp, _ = run(sp, 'B15 preset %s' % nm)
    check(page_with(hp, mark) is not None, 'B15 preset %s shows %r' % (nm, mark))

# ---------------- beta 1a: the review's findings on the pages ----------------
# item 1: a 1-px drift across a tile edge is a tap, not a move; a real drag moves
def s17(h):
    h.press('Enter')
    h.choose('Two raters: categories')
    h.drag([(52, 80), (53, 80)])                   # A2,B1 -> A2,B2 by 1 px: a tap (selects A2,B1)
    h.drag([(37, 50), (44, 50), (52, 50), (53, 50)])   # 16 px from A1,B1 into A1,B2 (>= MAX(8, 15.5)): a move
    h.tap(*SK(2))
    h.press('Esc')
    h.choose('Quit')


h17, res17 = run(s17, 'B17 drift')
check(G(h17, 'agT')[:2] == [37.0, 6.0] and G(h17, 'agT')[4:6] == [33.0, 11.0], 'B17 the 1-px drift moved nothing, the 16-px drag moved one: %r' % G(h17, 'agT')[:6])
check(len(h17.inputs) == 0, 'B17 the drift (on an unselected tile) only selected it')
# the threshold itself, by routine: travel just under and at MAX(8, cz/2) (cz = 31 at k = 4)
hh = H(); hh.execute('ag_Init()'); hh.execute('ag_LdMSW()'); hh.execute('ag_TGeom()')
for d_, want in [(1, 38.0), (15, 38.0), (16, 37.0)]:
    hh.execute('ag_LdMSW()'); hh.execute('ag_TGeom()')
    hh.globals_.update({'agSel': 2.0, 'agSelJ': 2.0, 'agTapX': 50.0, 'agTapY': 50.0, 'agRelX': 50.0 + d_, 'agRelY': 50.0})
    hh.execute('ag_TTap()')
    check(G(hh, 'agT')[0] == want, 'B17 travel %d px: A1,B1 = %r (want %r)' % (d_, G(hh, 'agT')[0], want))
# k = 6 (cz = 21): threshold MAX(8, 10.5) = 10.5
hh.globals_.update({'agK': 6.0, 'agT': [5.0] * 36}); hh.execute('ag_TCompute()'); hh.execute('ag_TSet("t", "s", 0, 1, "s")'); hh.execute('ag_TGeom()')
for d_, want in [(10, 5.0), (11, 4.0)]:
    hh.globals_.update({'agT': [5.0] * 36, 'agSel': 3.0, 'agSelJ': 3.0, 'agTapX': 40.0, 'agTapY': 40.0, 'agRelX': 40.0 + d_, 'agRelY': 40.0})
    hh.execute('ag_TTap()')
    check(G(hh, 'agT')[0] == want, 'B17 k = 6, travel %d px: A1,B1 = %r (want %r)' % (d_, G(hh, 'agT')[0], want))

# item 2: an edited preset says "edited from"
check(page_with(h17, 'edited from Landis & Koch 1977') is not None, 'B17 tiles page says edited from Landis & Koch 1977')
check(page_with(h17, 'MS: 149 Winnipeg patients (edited)') is not None, 'B17 title says (edited)')
check(res17 is not None and res17.endswith('(MS: 149 Winnipeg patients (edited)), edited from Landis & Koch 1977'), 'B17 Home summary: %r' % res17)


def s18(h):
    h.press('Enter')
    h.choose('Two raters: categories')
    h.press('Plus')
    h.tap(*SK(2))
    h.press('Esc')
    h.choose('Load a preset'); h.choose('MS diagnosis: Winnipeg')   # reloaded: published again
    h.tap(*SK(2))
    h.press('Esc')
    h.choose('Quit')


h18, res18 = run(s18, 'B18 edited then reloaded')
pk = [p for p in h18.pages if has(p, 'kappa = (po - pe)')]
check(len(pk) == 2 and has(pk[0], 'edited from Landis & Koch 1977') and has(pk[1], 'Data: Landis & Koch 1977'), 'B18 Kappa page source edited, then published again')
check(res18 is not None and 'edited' not in res18, 'B18 Home summary after reload %r' % res18)

# item 6 on the pages: a clipped CI and a refused SE


def s19(h):
    h.globals_.update({'D1': [1.] * 12 + [2.] * 9, 'D2': [2.] * 12 + [1.] * 9})
    h.press('Enter')
    h.choose('Use my data'); h.choose('Two raters')
    h.tap(*SK(2))
    h.press('Esc')
    h.choose('Quit')


def s19b(h):
    h.globals_.update({'D1': [1., 2.], 'D2': [1., 2.]})
    h.press('Enter')
    h.choose('Use my data'); h.choose('Two raters')
    h.tap(*SK(2)); h.tap(*SK(3)); h.tap(*SK(4))
    h.press('Esc')
    h.choose('Quit')


r19 = R.cohen([[0, 12], [9, 0]])
h19, _ = run(s19, 'B19 kappa 0/12/9/0')
expect(h19, 'kappa = (po - pe)/(1 - pe) = ' + fx(r19['kappa'], 3), ['95% CI -1.000 to ' + fx(r19['hi'], 3) + ', clipped (SE', 'one-sided p > 0.9999'], 'B19 0/12/9/0 kappa page')
expect(h19, 'agree po = 0.000', ['95% CI (clipped):', '-1.000 to ' + fx(r19['hi'], 3)], 'B19 0/12/9/0 tiles', last=False)
h19b, _ = run(s19b, 'B19 kappa N = 2')
expect(h19b, 'kappa = (po - pe)/(1 - pe) = 1.000', ['No SE, CI or p here: N < 10'], 'B19 N = 2 kappa page')
expect(h19b, 'N = 2', ['no SE, CI or p:', 'N < 10'], 'B19 N = 2 tiles', last=False)
expect(h19b, 'Null curve', ['No SE, CI or p here: N < 10'], 'B19 N = 2 null page')
expect(h19b, 'Weights: ordered', ['no SE, CI or p'], 'B19 N = 2 weights')

# items 3, 4 on the pages: the offset case and the ICC(2,k) zero denominator


def s20(h, Y):
    cols = list(zip(*Y))
    h.globals_.update({'D%d' % (j + 1): [float(x) for x in cols[j]] for j in range(len(cols))})
    h.press('Enter')
    h.choose('Use my data'); h.choose('Continuous')
    for r_ in range(6):
        h.tap(150, 36 + 19 * r_ + 5)
    h.tap(*SK(6))
    h.choose('Quit')


h20, _ = run(lambda h: s20(h, [[1, 6], [2, 7], [3, 8], [4, 9]]), 'B20 ICC offset')
expect(h20, 'ICC: Your data', ['1.000', '0.118', '-0.579', 'no F interval (error MS = 0)'], 'B20 ICC offset page')
check(any('F is infinite' in ' '.join(m.lines) for m in h20.msgboxes), 'B20 ICC(3,1) message: F is infinite')
h21, _ = run(lambda h: s20(h, [[1, 2, 1], [2, 1, 2], [1, 2, 1], [2, 1, 2]]), 'B21 ICC(2,k) denominator 0')
expect(h21, 'ICC: Your data', ['--', 'undefined (denominator 0)'], 'B21 ICC page')
expect(h21, 'ICC(2,k): undefined (denominator 0)', [], 'B21 info line')
for p in h21.pages:
    for sh in p.shapes:
        nm_ = repr(sh).split('(')[0]
        xs = [float(a_) for a_ in list(sh.args)[:(2 if nm_ == 'PIXON_P' else 4)]] if hasattr(sh, 'args') else []
        if xs:
            check(min(xs) > -400 and max(xs) < 720, 'B21 no off-screen shape: %r' % (sh,))
check(not h21.sci_strings, 'B21 no scientific notation')
h22, _ = run(lambda h: s20(h, [[3, 3, 3], [5, 5, 5], [9, 9, 9]]), 'B22 ICC perfect')
expect(h22, 'ICC: Your data', ['no F interval (within MS = 0)', 'no F interval (error MS = 0)'], 'B22 perfect agreement page')

# item 5: Help page 7 says the limit CIs are approximate, with the simulated coverage
expect(h13, '7/9  Bland-Altman', ['APPROXIMATE (Bland & Altman 1986 SE). In a', 'about 92% at n = 3-5 and 94% at n = 17.'], 'B13 help page 7')
# item 7 and low items in the source
src_ = open(SRC).read()
check('  ag_KDrain();\n  ag_Drain();\n  REPEAT\n    poK := GETKEY;' in src_, 'ag_Poll drains a finger before it waits')
expect(h1, 'agree po =', ['+/- = count, drag = move, Ent = menu, Esc = back'], 'B1 tiles footer', last=False)

# stale-key mode: every dialog leaves its own key behind (Lessons Learned 7);
# no page may be skipped by it
for scr, lab in [(s1, 'B16 stale B1'), (s2, 'B16 stale B2'), (s4, 'B16 stale B4'), (s5, 'B16 stale B5'),
                 (s8, 'B16 stale B8'), (s13, 'B16 stale B13')]:
    run(scr, lab, stale=True)

# ======================================================================
# Screen geometry over every page captured
# ======================================================================
print('GEOMETRY over %d pages' % len(ALLPAGES))
seen = set()
for label, p in ALLPAGES:
    for t in p.texts:
        key = (t.text, t.x, t.y, t.width)
        if key in seen:
            continue
        seen.add(key)
        ew = getattr(t, 'est_width', 0) or 0
        check(t.x >= 0 and t.y >= 0 and t.y <= 228 and t.x + min(ew, t.width or ew) <= 321,
              'off screen: %r at (%d, %d) [%s]' % (t.text, t.x, t.y, label))
        check(not t.clipped, 'clipped (est %.0f px > %s): %r at (%d, %d) [%s]' % (ew, t.width, t.text, t.x, t.y, label))

print('%d checks, %d failures' % (N_CHECK, len(FAILS)))
