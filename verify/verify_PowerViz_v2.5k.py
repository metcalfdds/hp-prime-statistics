#!/usr/bin/env python3
"""verify_PowerViz_v2.5k.py -- checks PowerViz v2.5k (31 Oct 2026): the Levene power page's first screen, which says
why a Levene F (SPSS's) cannot be worked out from means, SDs and n's and what the page answers instead -- and
everything the earlier scripts checked: v2.5j's test statistic obtained with its df under POWER and the new readout
box in every test; v2.5i's fixes from
Roger's first run on the calculator (a tap on a form's OK read as a tap on Menu; "!=" in pv_FMTP's floor), the box
with a column per group, df, "40, 20"; v2.5h's Levene pages, d on the plot and the reading for students; v2.5g's
fifth test (v2.5g to v2.5j were not committed on their own).

Runs from the repository alone (Lessons Learned s14 rule 18): programs/ and tools/ are found from this file's folder;
v2.5f is read from programs/ if it is still there, else from git history.  Needs hp-prime-kit (HPKIT), Giac's icas,
SciPy, statsmodels, SymPy.

A  tests 1-4 against v2.5f in the harness, 512 states: v2.5j's readout box against v2.5f's (every text but the n and
   mu/p cells, and the table's values), the plot's texts, the engine's numbers; the curve views and the formula
   page; help pages 1-3.  Allowed differences, each checked for what it is: the power = alpha = 0.001 knife-edge
   (v2.5g's mirrored z), v2.5h's d label on the plot and the d cell's colour (magenta), the help titles n/5, help
   page 2's new line, page 3's footer.  The engine's numbers agree to 1E-12.  The tiny-alpha critical z.  The menus.
B  test 5's arithmetic (v2.5g): power, n80, the closed form, the CAS templates, sigma', the ratio rules, extreme
   sigmas, the best split, Welch against z, Cohen's pooled-t warning -- against SciPy, statsmodels, Giac, simulation.
C  test 5's screens and forms (v2.5g), help page 4.
E  Levene's power page: pv_FPow (the exact F test) against SciPy; pv_LvApx against a 40,000-pair simulation where it
   is used (n1 + n2 > 240); pv_LvSim in the harness against the same; pv_RNorm's draws; every page text in five
   cases; the claims on page 2 (the pooled t's alpha with n1 = n2; skewed data fool the F test, not Levene's).
F  the two-samples page: pv_TwoS against SciPy (Levene with means and with medians, both t tests, Welch's df, both
   d's) on the presets and on 200 random pairs of samples; the presets against AnovaLab's lists and the draft data
   against published facts; every page text, D1/D2, the error boxes, the "DISAGREE" line.
G  d on the plot: the arrow and its label, all five tests.
H  v2.5i and v2.5j: a finger still on a form's OK (or a menu item) when the form closes is waited out, not read as a tap; no
   "!=" in the code; pv_FMTP's floor; the readout box, cell by cell, and its tappable rows; the df and the
   statistic obtained, t(df) or z, against SPSS's t for Roger's data.
D  layout: text_overlap_v1's recorder over every screen drawn; v2.5k adds no firm overlap, straddle or overrun.
Run:  python3 verify_PowerViz_v2.5k.py     (exit code 0 = all passed)
"""
import math
import os
import re
import subprocess
import sys
import warnings

import numpy as np
import sympy as sp
from scipy.stats import norm, t as tdist
from statsmodels.stats.power import NormalIndPower

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
TOOLS = os.path.join(REPO, 'tools')
os.environ.setdefault('HPKIT', '/home/claude/kit/hp-prime-kit-HEAD')
sys.path.insert(0, TOOLS)
import ppl_run_v3e  # noqa: E402
from ppl_run_v3e import Harness, ACCEPT, prime_eval  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402

PROG = os.path.join(REPO, 'programs', 'PowerViz_v2.5k.txt')
OLD = os.path.join(REPO, 'programs', 'PowerViz_v2.5f.txt')
if not os.path.exists(OLD):
    # v2.5f has left programs/: take it from the commit before the one that removed it (a shallow clone needs
    # `git fetch --deepen=5` first), into a temporary folder, never into the repository
    import tempfile
    rel = 'programs/PowerViz_v2.5f.txt'
    last = subprocess.run(['git', '-C', REPO, 'rev-list', '-n', '1', 'HEAD', '--', rel],
                          capture_output=True, text=True, check=True).stdout.strip()
    src = subprocess.run(['git', '-C', REPO, 'show', last + '^:' + rel], capture_output=True, text=True)
    if src.returncode != 0:
        src = subprocess.run(['git', '-C', REPO, 'show', 'HEAD:' + rel], capture_output=True, text=True, check=True)
    OLD = os.path.join(tempfile.mkdtemp(), 'PowerViz_v2.5f.txt')
    with open(OLD, 'w', encoding='utf-8') as f:
        f.write(src.stdout)

FAIL = []
NPASS = [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)) if detail != '' else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


def H(path, cas='giac', **kw):
    h = Harness(path, idle_key=4, cas=cas, home_minus=True, **kw)
    h.execute('pv_Init()')
    return h


def put(h, **kv):
    h.globals_.update({k: float(v) for k, v in kv.items()})


def page_texts(pg):
    return sorted((round(t.x, 3), round(t.y, 3), t.font, t.hex, t.text) for t in pg.texts)


def main_texts(pg, new):
    """the main view's texts, less what v2.5h adds on purpose: the d / h label under the arrow (y 47, font 1,
    magenta) is dropped, and the d cell's colour (x 108, y 179) is not compared"""
    out = []
    for t in pg.texts:
        if new and round(t.y) == 47 and t.font == 1 and t.hex == '#C800C8' and t.text[:4] in ('d = ', 'h = '):
            continue
        hx = None if (round(t.x) == 108 and round(t.y) == 179) else t.hex
        tx = t.text
        if new and round(t.y) == 165 and re.fullmatch(r'n = \d+', tx):
            tx = tx + '/grp'                  # v2.5i: "n = 30", not "n = 30/grp" (kept for the old box's cell)
        out.append((round(t.x, 3), round(t.y, 3), t.font, hx, tx))
    return sorted(out)


def cell(pg, x, y):
    """the text drawn at exactly (x, y) on a page, or None"""
    hit = [t.text for t in pg.texts if round(t.x) == x and round(t.y) == y]
    return hit[-1] if hit else None


def table5(pg):
    """test 5's readout table (v2.5i): ((n1, n2), (mu1, mu2), (sigma1, sigma2))"""
    return tuple((cell(pg, 20, y), cell(pg, 80, y)) for y in (165, 178, 191))


def draw(h, **kv):
    put(h, WFIT=1, WHLD=0, **kv)
    h.reset_records()
    h.execute('pv_Setup()')
    h.execute('pv_Draw()')
    return h.pages[-1]


def g(h, k):
    return h.globals_[k]


OV.install()

# ===================================================================== A. tests 1-4 against v2.5f
print('=== A. tests 1-4: v2.5k against v2.5f')
hn, ho = H(PROG), H(OLD)
DEF = {1: dict(MM0=100, MM1=105, SG=15), 2: dict(MM0=100, MM1=105, SG=15),
       3: dict(PP0=0.5, PP1=0.6), 4: dict(PP0=0.5, PP1=0.6)}
EFF = {1: [105, 100, 92.5, 101], 2: [105, 100, 92.5, 101], 3: [0.6, 0.5, 0.35, 0.52], 4: [0.6, 0.5, 0.35, 0.52]}
box_bad = []
plot_bad = []
edges = []
nstate = 0
numdiff = 0.0
REGION = re.compile(r'^(power|β|α) ?[=<>]')     # labels inside the plot's regions: drawn only where they fit


def num_ok(txt, v):
    """a cell's text is v at the decimals it shows"""
    try:
        a_ = float(txt.replace('−', '-'))
    except (AttributeError, ValueError):
        return False
    dec = len(txt.split('.')[1]) if '.' in txt else 0
    return abs(a_ - v) <= 0.5 * 10 ** -dec + 1e-9


for tt in (1, 2, 3, 4):
    for tl in (1, 2):
        for al in (0.001, 0.05, 0.2, 0.6, 0.999):
            if tl == 2 and al > 0.5:
                continue
            for ef in EFF[tt]:
                for nn in (2, 30, 100, 5000):
                    st = dict(DEF[tt], TT=tt, TL=tl, AL=al, NN=nn)
                    st['MM1' if tt <= 2 else 'PP1'] = ef
                    pn, po = draw(hn, **st), draw(ho, **st)
                    nstate += 1
                    # v2.5j: the new box (every test).  Every text of v2.5f's box but its "n = 30/grp" and its
                    # "μ₁ = 105" / "μ₂ = 105" / "p₁ = 0.60" / "p₂ = 0.60" cells is still shown, and the table holds
                    # the values typed
                    nb = [x[4] for x in main_texts(pn, 1)]
                    ob = [x[4] for x in main_texts(po, 0) if x[1] >= 162 and
                          not x[4].startswith(('n = ', 'μ₁ = ', 'μ₂ = ', 'p₁ = ', 'p₂ = '))]
                    v0 = DEF[tt]['MM0'] if tt <= 2 else DEF[tt]['PP0']
                    if tt in (2, 4):
                        tb = table5(pn)
                        tok = (tb[0] == (str(nn), str(nn)) and num_ok(tb[1][0], v0) and num_ok(tb[1][1], ef) and
                               tb[1][0].count('.') == tb[1][1].count('.') and
                               tb[2] == (('15', '15') if tt == 2 else (None, None)))
                    else:
                        tb = tuple(cell(pn, 30, y) for y in (152, 165, 178, 191))
                        tok = (tb[0] == str(nn) and num_ok(tb[1], v0) and num_ok(tb[2], ef) and
                               tb[3] == ('15' if tt == 1 else None))
                    miss = [x for x in ob if x not in nb]
                    if miss:
                        # the floor knife-edge: power exactly 0.001 (no effect, alpha 0.001), and only the
                        # "0.001" / "< 0.001" texts differ
                        if abs(g(hn, 'PW') - 0.001) < 1e-12 and all('0.001' in x for x in miss):
                            edges.append((st, miss))
                            miss = []
                    if miss or not tok:
                        box_bad.append((st, miss, tb))
                    # the plot (it ends 13 px higher now): the same texts, less the region labels, which are
                    # drawn only where they fit
                    pnew = sorted(x[4] for x in main_texts(pn, 1) if x[1] < 150 and not REGION.match(x[4]))
                    pold = sorted(x[4] for x in main_texts(po, 0) if x[1] < 162 and not REGION.match(x[4]))
                    if pnew != pold:
                        plot_bad.append((st, sorted(set(pnew) ^ set(pold))))
                    for k in ('PW', 'ZC', 'XCL', 'XCU', 'N80', 'NCF', 'SE0', 'SE1'):
                        a, b = g(hn, k), g(ho, k)
                        if abs(b) < 1e9:
                            numdiff = max(numdiff, abs(a - b) / max(1.0, abs(b)))
check('A1 main view, %d states of tests 1-4: the new box (v2.5j) shows every text of v2.5f\'s box but its n and '
      'mu/p cells, and its table holds the values typed (n; both means or p\'s to the decimals shown; sigma); %d '
      'state(s) at the floor knife-edge' % (nstate, len(edges)), not box_bad, box_bad[:3])
check('A1 main view, %d states: the plot shows the same texts as v2.5f\'s (less the labels inside the regions, '
      'drawn where they fit; the plot is 13 px shorter)' % nstate, not plot_bad, plot_bad[:3])
for e in edges:
    print('   knife-edge (power = alpha = 0.001 exactly; v2.5f "< 0.001", v2.5j "0.001"):', e)
check('A1 engine numbers PW ZC XCL XCU N80 NCF SE0 SE1 agree with v2.5f (largest relative difference %.1e)'
      % numdiff, numdiff < 1e-12)

# views: Pow-n, Pow-effect, the formula page with and without the CAS
nview = 0
vdiff = []
for cas in ('giac', 'fail'):
    hn2, ho2 = H(PROG, cas=cas), H(OLD, cas=cas)
    for tt in (1, 2, 3, 4):
        for tl in (1, 2):
            for al in (0.05, 0.6):
                if tl == 2 and al > 0.5:
                    continue
                st = dict(DEF[tt], TT=tt, TL=tl, AL=al, NN=30 if tt <= 2 else 100)
                for rt in ('pv_PowNView()', 'pv_PowEView()', 'pv_Formula()'):
                    if cas == 'fail' and rt != 'pv_Formula()':
                        continue
                    out = []
                    for hh in (hn2, ho2):
                        put(hh, WFIT=1, WHLD=0, **st)
                        hh.execute('pv_Setup()')
                        hh.reset_records()
                        hh.execute(rt)
                        pt = [page_texts(p) for p in hh.pages]
                        if hh is hn2:
                            # v2.5i: "n = 30 per group" (tests 2, 4) and "n = 30" (one sample) for "n = 30/grp"
                            pt = [[(a, b, c, d, re.sub(r'^n = (\d+)( per group)?, α', r'n = \1/grp, α', e))
                                   for (a, b, c, d, e) in pg] for pg in pt]
                        out.append(pt)
                    nview += 1
                    if out[0] != out[1]:
                        vdiff.append((cas, tt, tl, al, rt))
check('A2 Pow-n, Pow-effect and the formula page (CAS and no CAS), %d runs of tests 1-4: identical to v2.5f but '
      '"n = 30 per group" / "n = 30" for "n = 30/grp" (v2.5i)'
      % nview, not vdiff, vdiff[:3])

# help pages 1-3: only the titles and page 3's footer may differ
for hh in (hn, ho):
    hh.reset_records()
    hh.execute('pv_ShowHelp()')
hp_n = [p.lines() for p in hn.pages]
hp_o = [p.lines() for p in ho.pages]
ok = len(hp_n) == 5 and len(hp_o) == 3
diffs = []
for i in range(3):
    a = [x.replace('1/5', '1/3').replace('2/5', '2/3').replace('3/5', '3/3') for x in hp_n[i]]
    if i == 1:
        a = [x for x in a if x != 'magenta arrow: the effect, d (or h), on the plot']
        # v2.5i: the readout taps, for the two-group tests' new box
        a = [x.replace('n = type n;  μ, p, d or h = type the effect', 'n = type n;  μ₁, p₁, d or h = type the effect')
              .replace('α, zcrit = the α ladder;  σ, μ₀, p₀ = Edit form', 'α or zcrit = pick α from the ladder') for x in a]
    if i == 0:
        # v2.5j: one SE line, and a line for the statistic obtained
        a = [x.replace("SE₀ = the H₀ curve's SE, from σ (or p) and n", 'SE₀ = the standard error of the H₀ curve, worked')
              .replace('t(df) = t obtained if a sample had these values', 'out from your σ (or p) and n') for x in a]
    if i == 2:
        a = [x.replace('any key or tap = next page', 'any key or tap = back') for x in a]
    if a != hp_o[i]:
        diffs.append(i + 1)
check('A3 help pages 1-3 equal to v2.5f apart from the "n/5" titles, page 1\'s SE and t lines and page 2\'s '
      'readout lines (v2.5i, v2.5j), page 2\'s d-arrow line, and page 3\'s footer; '
      'pages 4 and 5 new', ok and not diffs, diffs)

# a typed alpha of 1E-17: v2.5f's ICDF(1 - alpha) against v2.5g's mirrored form (1 - 1E-17 is 1 in a double, as
# 1 - 1E-13 is 1 in the Prime's 12 digits)
put(ho, WFIT=1, WHLD=0, TT=1, TL=1, AL=1e-17, NN=30, MM0=100, MM1=105, SG=15)
err = ''
try:
    ho.execute('pv_Model(30)')
except Exception as e:
    err = type(e).__name__
put(hn, WFIT=1, WHLD=0, TT=1, TL=1, AL=1e-17, NN=30, MM0=100, MM1=105, SG=15)
hn.execute('pv_Model(30)')
zc = g(hn, 'ZC')
check('A4 alpha 1E-17: v2.5f asks NORMALD_ICDF(0,1,1) (%s in the harness; infinity on the G1); v2.5g ZC = %.6f'
      % (err or 'no error', zc), err != '' and abs(zc - norm.isf(1e-17)) < 1e-6)
put(hn, WFIT=1, WHLD=0, TT=1, TL=1, AL=1e-13, NN=30, MM0=100, MM1=105, SG=15)
hn.execute('pv_Model(30)')
check('A4 alpha 1E-13 (where the Prime\'s 1 - alpha is already 1): v2.5g ZC = %.4f' % g(hn, 'ZC'),
      abs(g(hn, 'ZC') - norm.isf(1e-13)) < 1e-6)
for al in (0.001, 0.05, 0.2, 0.6, 0.999):
    for tl in (1, 2):
        if tl == 2 and al > 0.5:
            continue
        put(hn, TT=1, TL=tl, AL=al)
        hn.execute('pv_Model(30)')
        put(ho, TT=1, TL=tl, AL=al)
        ho.execute('pv_Model(30)')
        if abs(g(hn, 'ZC') - g(ho, 'ZC')) > 1e-12:
            check('A4 ZC mirror = old form at alpha %g, %d-sided' % (al, tl), False, (g(hn, 'ZC'), g(ho, 'ZC')))
check('A4 at ordinary alphas the mirrored ZC equals v2.5f\'s to 1E-12', True)
srcn = open(PROG, encoding='utf-8').read()
code_icdf = [ln for ln in srcn.split('\n') if 'NORMALD_ICDF' in ln.split('//')[0]]
check('A4 no NORMALD_ICDF(0,1,1-...) left in code; five mirrored sites',
      not any('1-AL' in ln.split('//')[0] for ln in code_icdf) and
      sum('-NORMALD_ICDF(0,1,AL/TL)' in ln for ln in code_icdf) == 5, len(code_icdf))

# ===================================================================== B. test 5 arithmetic
print('=== B. test 5: the arithmetic, routine by routine')
h5 = H(PROG)


def rhu(x):          # ROUND(x, 0): halves away from zero (Lessons Learned s3)
    return math.floor(x + 0.5)


def n2_rule(n1, n2t, n1t):
    return max(2, rhu(n1 * n2t / n1t))


def zpow(d, s1, s2, n1, n2, a, tails):
    se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
    z = norm.isf(a / tails)
    m = abs(d) / se
    return norm.sf(z - m) + (norm.cdf(-z - m) if tails == 2 else 0.0)


def set5(h, mu1, mu2, s1, s2, n1, n2t, n1t, al, tl):
    put(h, TT=5, MM0=mu1, MM1=mu2, SG=s1, SG2=s2, NN=n1, NN2=n2t, KN1=n1t, AL=al, TL=tl, WFIT=1, WHLD=0)


rng = np.random.default_rng(20261031)
worst = 0.0
worst_sm = 0.0
cnt = 0
grid = []
for d in (5, -5, 0.5, 12):
    for s1, s2 in ((10, 20), (15, 15), (20, 6), (2.5, 7.5)):
        for n1, n2t in ((40, 20), (30, 45), (12, 6), (200, 600), (2, 2)):
            for al, tl in ((0.05, 1), (0.05, 2), (0.01, 1), (0.2, 2)):
                grid.append((d, s1, s2, n1, n2t, al, tl))
for d, s1, s2, n1, n2t, al, tl in grid:
    set5(h5, 100, 100 + d, s1, s2, n1, n2t, n1, al, tl)
    h5.execute('pv_Model(%d)' % n1)
    n2 = n2_rule(n1, n2t, n1)
    ref = zpow(d, s1, s2, n1, n2, al, tl)
    worst = max(worst, abs(g(h5, 'PW') - ref))
    se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
    ses = math.sqrt(1 / n1 + 1 / n2)
    smv = NormalIndPower().power(effect_size=abs(d) / se * ses, nobs1=n1, alpha=al, ratio=n2 / n1,
                                 alternative='larger' if tl == 1 else 'two-sided')
    worst_sm = max(worst_sm, abs(g(h5, 'PW') - smv))
    cnt += 1
check('B1 pv_Model power, %d states (both directions, both tails): = the z formula in SciPy (max |diff| %.1e)'
      % (cnt, worst), worst < 1e-12)
check('B1 = statsmodels NormalIndPower with the SE mapped (max |diff| %.1e)' % worst_sm, worst_sm < 1e-9)

# a simulation of the z test itself, 200,000 trials each
mcok = []
for d, s1, s2, n1, n2, al, tl in ((5, 10, 20, 40, 20, .05, 1), (5, 10, 20, 20, 40, .05, 2), (-8, 25, 8, 15, 30, .01, 1)):
    set5(h5, 100, 100 + d, s1, s2, n1, n2, n1, al, tl)
    h5.execute('pv_Model(%d)' % n1)
    x = rng.normal(0, s1, (200000, n1)).mean(1)
    y = rng.normal(d, s2, (200000, n2)).mean(1)
    z = (y - x) / math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
    c = norm.isf(al / tl)
    rej = ((z < -c) if d < 0 else (z > c)) if tl == 1 else (np.abs(z) > c)
    p = rej.mean()
    se = math.sqrt(p * (1 - p) / 200000)
    mcok.append((round(g(h5, 'PW'), 4), round(p, 4), abs(p - g(h5, 'PW')) < 4 * se))
check('B1 = a simulation of the z test (200,000 trials, within 4 SE): ' + str(mcok), all(m[2] for m in mcok))

# B2 n80 by brute force
bad = []
nb = 0
for d, s1, s2, n1t, n2t, al, tl in [(5, 10, 20, 40, 20, .05, 1), (5, 10, 20, 40, 20, .05, 2), (3, 15, 15, 30, 30, .05, 2),
                                    (12, 8, 25, 12, 6, .01, 1), (2, 10, 30, 10, 33, .05, 1), (0.6, 1, 2, 7, 70, .05, 2),
                                    (40, 10, 10, 5, 3, .05, 1), (1, 10, 20, 40, 20, .05, 1), (0, 10, 20, 40, 20, .05, 1)]:
    set5(h5, 100, 100 + d, s1, s2, n1t, n2t, n1t, al, tl)
    res = h5.execute('pv_N80()')
    ref = 0
    if d != 0:
        ref = -1
        for n1 in range(2, 5001):
            if zpow(d, s1, s2, n1, n2_rule(n1, n2t, n1t), al, tl) >= 0.8:
                ref = n1
                break
    nb += 1
    if res != ref:
        bad.append((d, s1, s2, n1t, n2t, al, tl, res, ref))
check('B2 pv_N80 = brute force over n1 = 2..5000 with n2 = max(2, round(n1 x typed ratio)), %d cases' % nb,
      not bad, bad)

# B3 the closed form
bad = []
nsm = [0, 0]
for d, s1, s2, n1t, n2t, al, tl in grid:
    if d == 0:
        continue
    set5(h5, 100, 100 + d, s1, s2, n1t, n2t, n1t, al, tl)
    ncf = h5.execute('pv_NCF()')
    k = n2t / n1t
    za, zb = norm.isf(al / tl), norm.ppf(0.8)
    ref = (za + zb) ** 2 * (s1 ** 2 + s2 ** 2 / k) / d ** 2
    if abs(ncf - ref) > 1e-9 * ref:
        bad.append((d, s1, s2, n1t, n2t, al, tl, ncf, ref))
    if tl == 1:
        es = abs(d) * math.sqrt(1 + 1 / k) / math.sqrt(s1 ** 2 + s2 ** 2 / k)
        smn = NormalIndPower().solve_power(effect_size=es, nobs1=None, alpha=al, power=0.8, ratio=k,
                                           alternative='larger')
        smn = float(np.asarray(smn).ravel()[0])
        if math.isnan(smn):
            nsm[1] += 1           # statsmodels' root finder gave up (its bracket starts at n = 2)
        else:
            nsm[0] += 1
            if abs(smn - ncf) > 1e-5 * ncf:
                bad.append(('sm', d, s1, s2, n1t, n2t, al, ncf, smn))
check('B3 pv_NCF = (za+zb)^2 (s1^2 + s2^2/k)/delta^2 at every grid state, and = statsmodels solve_power '
      '(1-sided) in the %d states where its root finder converged (%d did not: n below its bracket)' % tuple(nsm),
      not bad and nsm[0] >= 100, bad[:3])

# B4 the CAS templates
h5.globals_['TT'] = 5.0
sym_t = h5.execute('pv_Eq({"pvs","pvd","pvp","pvr","pvm","pvt","pvk"})')
ans = prime_eval('string(%s)' % sym_t).strip('"').strip('{}')
pvza, pvzb, pvs, pvt, pvk, pvd = sp.symbols('pvza pvzb pvs pvt pvk pvd', positive=True)
expr = sp.sympify(re.sub(r'√(\d+)', r'sqrt(\1)', ans).replace('√', 'sqrt').replace('^', '**'),
                  locals=dict(pvza=pvza, pvzb=pvzb, pvs=pvs, pvt=pvt, pvk=pvk, pvd=pvd))
closed = (pvza + pvzb) ** 2 * (pvs ** 2 + pvt ** 2 / pvk) / pvd ** 2
check('B4 symbolic template -> Giac -> SymPy equals (za+zb)^2 (s1^2+s2^2/k)/delta^2: ' + ans,
      sp.simplify(expr - closed) == 0)
h5.globals_['FSY'] = ans
disp = h5.execute('pv_Disp("%s")' % ans)
check('B4 the screen form of it: ' + disp, 'σ₁' in disp and 'σ₂' in disp and 'k' in disp and 'pv' not in disp)
bad = []
nnum = 0
for d, s1, s2, n1t, n2t in ((5, 10, 20, 40, 20), (5.5, 2.5, 7.5, 35, 53), (3, 15, 15, 30, 30), (12, 8, 25, 12, 6),
                            (0.25, 0.5, 1.25, 7, 70)):
    set5(h5, 100, 100 + d, s1, s2, n1t, n2t, n1t, 0.05, 1)
    rs = lambda v: h5.execute('pv_RatS(%r)' % v)
    t = h5.execute('pv_Eq({"%s","(%s-%s)","","","","%s","(%d/%d)"})' % (rs(s1), rs(100 + d), rs(100), rs(s2), n2t, n1t))
    if '.' in t:
        bad.append(('decimal in CAS text', t))
    a = prime_eval('string(%s)' % t).strip('"').strip('{}')
    e = sp.sympify(re.sub(r'√(\d+)', r'sqrt(\1)', a).replace('√', 'sqrt').replace('^', '**'),
                   locals=dict(pvza=pvza, pvzb=pvzb))
    for al, tl in ((0.05, 1), (0.01, 2), (0.2, 1)):
        put(h5, AL=al, TL=tl)
        ncf = h5.execute('pv_NCF()')
        v = float(e.subs({pvza: norm.isf(al / tl), pvzb: norm.ppf(0.8)}))
        nnum += 1
        if abs(v - ncf) > 1e-9 * ncf:
            bad.append((d, s1, s2, n1t, n2t, al, tl, v, ncf))
check('B4 numeric templates (exact ratios, z as symbols) -> Giac -> at the program\'s z = pv_NCF, %d cases' % nnum,
      not bad, bad[:3])

# B5 small helpers
set5(h5, 100, 105, 10, 20, 40, 20, 40, 0.05, 1)
check('B5 pv_SigE = sqrt((s1^2+s2^2)/2) = %.6f (Cohen 1988 p. 44)' % h5.execute('pv_SigE()'),
      abs(h5.execute('pv_SigE()') - math.sqrt(250)) < 1e-12)
check('B5 pv_EffSz = 5/sqrt(250) = %.6f' % h5.execute('pv_EffSz()'), abs(h5.execute('pv_EffSz()') - 5 / math.sqrt(250)) < 1e-12)
check('B5 pv_EffStep = NiceNum(sigma\'/20) = %s' % h5.execute('pv_EffStep()'), h5.execute('pv_EffStep()') == 1)
mono = True
for n2t, n1t in ((20, 40), (45, 30), (53, 35), (7, 70), (700, 70), (3, 2)):
    put(h5, NN2=n2t, KN1=n1t)
    prev = 0
    for n1 in range(2, 400):
        v = h5.execute('pv_N2(%d)' % n1)
        if v != n2_rule(n1, n2t, n1t) or v < prev or v < 2:
            mono = False
        prev = v
check('B5 pv_N2 = max(2, round half up(n1 x n2/n1 typed)), never decreasing, at 6 ratios x n1 2..399', mono)
put(h5, NN2=20, KN1=40)
check('B5 pv_NStr(40) = "40, 20", pv_NStr(45) = "45, 23" (22.5 rounds up; v2.5i: a comma, not "/")',
      h5.execute('pv_NStr(40)') == '40, 20' and h5.execute('pv_NStr(45)') == '45, 23')
# pv_Set5's clamps
cases = []
for a, b, exp_nn, exp_n2, nmsg in ((40, 20, 40, 20, 0), (40, 25, 40, 25, 0), (2, 100, 2, 20, 1), (5000, 2, 5000, 500, 1),
                                   (30.7, 6000, 30, 300, 2), (1, 1, 2, 2, 2), (25, 2, 25, 3, 1)):
    put(h5, NN=40, NN2=20, KN1=40)
    h5.reset_records()
    r = h5.execute('pv_Set5(%r,%r)' % (a, b))
    cases.append(((a, b), (g(h5, 'NN'), g(h5, 'NN2'), g(h5, 'KN1')), len(h5.msgboxes)))
    if not (g(h5, 'NN') == exp_nn and g(h5, 'NN2') == exp_n2 and len(h5.msgboxes) == nmsg):
        check('B5 pv_Set5(%s, %s)' % (a, b), False, cases[-1])
check('B5 pv_Set5: unchanged pair keeps the ratio; n in 2..5000; n2 within 0.1-10 x n1; one box per changed value',
      True, cases)
# opening the form on a stepped n1 and pressing OK keeps the exact ratio
put(h5, NN=45, NN2=20, KN1=40)
h5.execute('pv_Set5(45, %d)' % h5.execute('pv_N2(45)'))
check('B5 OK on an unchanged form after stepping n1 to 45 (n2 23) keeps NN2/KN1 = 20/40, not 23/45',
      g(h5, 'NN2') == 20 and g(h5, 'KN1') == 40)

# extreme sigmas: SE, sigma' and the closed form are scaled by the larger sigma, so squaring a typed 1E-200 or 1E200
# neither underflows nor overflows (in the harness's doubles 1E-200^2 is 0 and 1E200^2 infinite, as 1E-300 and 1E300
# would be on the Prime); power depends on delta/sigma only, so the scaled scene must give the unscaled scene's power
sc = []
for f in (1e-200, 1e200):
    set5(h5, 0, 5 * f, 1 * f, 2 * f, 40, 20, 40, 0.05, 1)
    h5.execute('pv_Model(40)')
    p_s, d_s, c_s = g(h5, 'PW'), h5.execute('pv_EffSz()'), h5.execute('pv_NCF()')
    set5(h5, 0, 5, 1, 2, 40, 20, 40, 0.05, 1)
    h5.execute('pv_Model(40)')
    sc.append((f, abs(p_s - g(h5, 'PW')) < 1e-12, abs(d_s - h5.execute('pv_EffSz()')) < 1e-12,
               abs(c_s - h5.execute('pv_NCF()')) < 1e-9 * h5.execute('pv_NCF()')))
check('B5 sigma 1E-200 and 1E200 (delta scaled with them): power, d and the formula n1 equal the unscaled scene\'s '
      '(no underflow to SE 0, no overflow to infinity)', all(all(x[1:]) for x in sc), sc)

# B6 help page 4's two claims
bs = []
for s1, s2, tot in ((10, 20, 60), (10, 20, 90), (15, 5, 80), (12, 12, 50), (5, 30, 140)):
    best = max(range(2, tot - 1), key=lambda n1: -(s1 ** 2 / n1 + s2 ** 2 / (tot - n1)))
    ideal = tot * s1 / (s1 + s2)
    bs.append((s1, s2, tot, best, round(ideal, 2), abs(best - ideal) <= 1))
check('B6 best split: the n1 that makes s1^2/n1 + s2^2/(N-n1) smallest is N s1/(s1+s2) (n2/n1 = s2/s1) to the '
      'nearest person: ' + str(bs), all(b[-1] for b in bs))
wl = []
for n1, n2 in ((5, 5), (8, 4), (10, 10), (20, 10), (200, 100)):
    d, s1, s2, al = 5, 10, 20, 0.05
    N = 100000
    x = rng.normal(0, s1, (N, n1))
    y = rng.normal(d, s2, (N, n2))
    v1 = x.var(1, ddof=1) / n1
    v2 = y.var(1, ddof=1) / n2
    tt = (y.mean(1) - x.mean(1)) / np.sqrt(v1 + v2)
    df = (v1 + v2) ** 2 / (v1 ** 2 / (n1 - 1) + v2 ** 2 / (n2 - 1))
    pw = (tt > tdist.isf(al, df)).mean()
    zp = zpow(d, s1, s2, n1, n2, al, 1)
    wl.append((n1, n2, round(zp, 3), round(pw, 3)))
small_less = all(w[3] < w[2] - 0.004 for w in wl[:4])
big_close = abs(wl[4][3] - wl[4][2]) < 0.01
check('B6 Welch\'s t (simulated, 100,000 trials) has less power than the z test at small n, about the same at '
      '200/100: ' + str(wl), small_less and big_close)

# Cohen (1988, p. 44): with sigma and n both unequal, the pooled t test's true alpha is far from nominal;
# Welch's is close.  Simulated under H0 (equal means), nominal alpha 0.05, 2-sided.
cw = []
for s1, s2, n1, n2 in ((10, 20, 40, 20), (10, 20, 20, 40), (10, 10, 40, 20)):
    N = 100000
    x = rng.normal(0, s1, (N, n1))
    y = rng.normal(0, s2, (N, n2))
    m = y.mean(1) - x.mean(1)
    sp2 = ((n1 - 1) * x.var(1, ddof=1) + (n2 - 1) * y.var(1, ddof=1)) / (n1 + n2 - 2)
    tp = m / np.sqrt(sp2 * (1 / n1 + 1 / n2))
    ap = (np.abs(tp) > tdist.isf(0.025, n1 + n2 - 2)).mean()
    v1 = x.var(1, ddof=1) / n1
    v2 = y.var(1, ddof=1) / n2
    tw = m / np.sqrt(v1 + v2)
    df = (v1 + v2) ** 2 / (v1 ** 2 / (n1 - 1) + v2 ** 2 / (n2 - 1))
    aw = (np.abs(tw) > tdist.isf(0.025, df)).mean()
    cw.append((s1, s2, n1, n2, round(ap, 3), round(aw, 3)))
check('B6 Cohen\'s warning (help page 4), simulated under H0 at nominal 0.05: the pooled t test\'s true alpha is far '
      'off when sigma and n both differ (the bigger sigma in the smaller group: too high; in the bigger group: too low), '
      'right when only n differs; Welch\'s stays near 0.05: ' + str(cw),
      cw[0][4] > 0.08 and cw[1][4] < 0.03 and abs(cw[2][4] - 0.05) < 0.005 and all(abs(c[5] - 0.05) < 0.006 for c in cw))

# ===================================================================== C. test 5 screens
print('=== C. test 5 in the harness: screens')
hc = Harness(PROG, idle_key=4, cas='giac', home_minus=True)
hc.choose(3)
hc.answer(ACCEPT)
r = hc.execute('POWERVIZ()')
L = hc.pages[0].lines()
want = ['PowerViz  2 Means, σ₁≠σ₂ (z)  1-sided', 'group 1', 'group 2', 'd = 0.32, small', '0.277',
        'SE₀ = 4.74', 'n₈₀ = 223, 112 (222.6)', 'zcrit = 1.645', 'β = 0.723']


check('C1 main view at the defaults: ' + ' | '.join(want), all(w in L for w in want), [x for x in want if x not in L])
check('C1 the readout table (v2.5i): n 40, 20; mu 100, 105; sigma 10, 20 = %s' % (table5(hc.pages[0]),),
      table5(hc.pages[0]) == (('40', '20'), ('100', '105'), ('10', '20')))
check('C1 the test menu: five items, the new one third',
      hc.chooses[0].items == ['One-Sample Mean (z)', 'Two Means, equal σ & n (z)', 'Two Means, unequal σ & n (z)',
                              'One Proportion', 'Two Proportions'], hc.chooses[0].items)
check('C1 every menu item at most 30 characters', max(len(x) for x in hc.chooses[0].items) <= 30)
fm = hc.inputs[0]
check('C2 the Edit form: 7 fields, n grp1 / n grp2 shown as 40 / 20',
      fm.labels == ['μ grp1:', 'μ grp2:', 'σ grp1:', 'σ grp2:', 'n grp1:', 'n grp2:', 'α:'] and
      fm.before.get('e5a') == 40 and fm.before.get('e5b') == 20, (fm.labels, fm.before))
mb = hc.msgboxes[-1].lines
check('C9 exit box: ' + ' / '.join(mb), mb[1].startswith('n₁ = 40, n₂ = 20') and 'POWER = 0.2773' in mb[3]
      and len(mb) <= 5)
check('C9 exports: EP_NPG = n1 = 40, EP_PWR = 0.2773, EP_DELTA = 5',
      g(hc, 'EP_NPG') == 40 and abs(g(hc, 'EP_PWR') - zpow(5, 10, 20, 40, 20, .05, 1)) < 1e-12 and g(hc, 'EP_DELTA') == 5)
check('C9 POWERVIZ returns the power', abs(r - zpow(5, 10, 20, 40, 20, .05, 1)) < 1e-12)

# the Edit form's clamps through the form itself
hc2 = Harness(PROG, idle_key=4, cas='giac', home_minus=True)
hc2.choose(3)
hc2.answer({'SG2': -3, 'e5a': 2, 'e5b': 100})
hc2.execute('POWERVIZ()')
boxes = [m.lines for m in hc2.msgboxes[:-1]]
check('C2 typed n1 2, n2 100, sigma2 -3: n2 set to 20 (10 x n1) and sigma2 to 1, each with its box',
      g(hc2, 'NN') == 2 and g(hc2, 'NN2') == 20 and g(hc2, 'SG2') == 1 and len(boxes) == 2, boxes)

# arrows and a vertical drag keep the ratio
hc3 = Harness(PROG, idle_key=None, cas='giac', home_minus=True)
hc3.choose(3)
hc3.answer(ACCEPT)
hc3.press('Up')
hc3.press('Up')
hc3.press('Down')
hc3.press('Esc')
hc3.execute('POWERVIZ()')
ns = [table5(p)[0] for p in hc3.pages if cell(p, 20, 165)]
check('C3 Up, Up, Down from 40, 20: the n row reads %s (n2 = round(n1 x 1/2), halves up)' % ns,
      ns[:4] == [('40', '20'), ('45', '23'), ('50', '25'), ('45', '23')], ns)
check('C3 the ratio is untouched by the arrows (NN2/KN1 still 20/40)', g(hc3, 'NN2') == 20 and g(hc3, 'KN1') == 40)

hc4 = Harness(PROG, idle_key=None, cas='giac', home_minus=True)
hc4.choose(3)
hc4.answer(ACCEPT)
hc4.drag([(160, 120), (160, 110), (160, 96), (160, 84)])
hc4.press('Esc')
hc4.execute('POWERVIZ()')
hint = [t.text for t in hc4.texts if 'drag up' in t.text]
check('C3 a vertical drag of 36 px: three n steps, the hint "%s"' % (hint[-1] if hint else ''),
      g(hc4, 'NN') == 55 and hint and hint[-1] == 'n = 55, 28: drag up = larger n₁ (n₂ follows)', (g(hc4, 'NN'), hint[-1:]))

# a tap on the n cell: the two-field form
hc5 = Harness(PROG, idle_key=None, cas='giac', home_minus=True)
hc5.choose(3)
hc5.answer(ACCEPT)
hc5.tap(30, 170)
hc5.answer({'env': 30, 'en2': 45})
hc5.press('Esc')
hc5.execute('POWERVIZ()')
f2 = hc5.inputs[-1]
check('C4 tap the n row: the form "Sample sizes" with n grp1 40, n grp2 20; typed 30 / 45 -> n row 30, 45',
      f2.title == 'Sample sizes' and f2.before == {'env': 40, 'en2': 20} and g(hc5, 'NN') == 30 and g(hc5, 'NN2') == 45
      and g(hc5, 'KN1') == 30 and any(table5(p)[0] == ('30', '45') for p in hc5.pages), (f2.title, f2.before))

# H1 drag: mu2 follows on the sigma'/20 grid (step 1 at sigma' = 15.8), through the live loop as on the device
hw = H(PROG)
put(hw, TT=5, MM0=100, MM1=105, SG=10, SG2=20, NN=40, NN2=20, KN1=40, AL=0.05, TL=1, WFIT=1, WHLD=0)
hw.execute('pv_Setup()')
xmn, xmx = g(hw, 'XMN'), g(hw, 'XMX')
p1x = int(round(12 + (5 - xmn) / (xmx - xmn) * 296))
hc6 = Harness(PROG, idle_key=None, cas='giac', home_minus=True)
hc6.choose(3)
hc6.answer(ACCEPT)
hc6.drag([(p1x, 100), (p1x + 15, 101), (p1x + 30, 100)])
hc6.press('Esc')
hc6.execute('POWERVIZ()')
exp = round(xmn + (p1x + 30 - 12) * (xmx - xmn) / 296 + 100)
hint = [t.text for t in hc6.texts if 'follows your finger' in t.text]
check('C10 drag H1 30 px right from x %d: mu2 105 -> %s (expected %d, the whole-number grid), the hint shown'
      % (p1x, g(hc6, 'MM1'), exp), g(hc6, 'MM1') == exp and exp > 105 and bool(hint))

# Pow-n and Pow-effect views
hc6 = H(PROG)
put(hc6, TT=5, MM0=100, MM1=105, SG=10, SG2=20, NN=40, NN2=20, KN1=40, AL=0.05, TL=1, WFIT=1, WHLD=0)
hc6.execute('pv_Setup()')
hc6.reset_records()
hc6.execute('pv_PowNView()')
Lp = hc6.pages[0].lines()
pwc = list(hc6.globals_['PWC'])
pnmx = g(hc6, 'PNMX')
okc = all(abs(pwc[c - 1] - zpow(5, 10, 20, round(2 + c / 250 * (pnmx - 2)), n2_rule(round(2 + c / 250 * (pnmx - 2)), 20, 40), .05, 1)) < 1e-12
          for c in range(1, 251))
check('C5 Pow-n: the 250 cached powers = SciPy at n1 and its n2, every column', okc)
check('C5 Pow-n texts: "n₁   (n₂ = 0.5 × n₁)", "n₈₀ = 223, 112", footer "n = 40, 20: power = 0.277, ..."',
      'n₁   (n₂ = 0.5 × n₁)' in Lp and 'n₈₀ = 223, 112' in Lp and
      'n = 40, 20: power = 0.277, touch = pick n, key = back' in Lp, Lp)
hc7 = Harness(PROG, idle_key=None, cas='giac', home_minus=True)
hc7.execute('pv_Init()')
put(hc7, TT=5, MM0=100, MM1=105, SG=10, SG2=20, NN=40, NN2=20, KN1=40, AL=0.05, TL=1, WFIT=1, WHLD=0)
hc7.execute('pv_Setup()')
hc7.drag([(140, 100), (150, 100), (160, 100)])
hc7.execute('pv_PowNView()')
nsel = round(2 + (160 - 40) / 250 * (g(hc7, 'PNMX') - 2))
check('C5 Pow-n: a finger lifted at x 160 adopts n1 = %d; n2 follows (%d)' % (nsel, n2_rule(nsel, 20, 40)),
      g(hc7, 'NN') == nsel and hc7.execute('pv_N2(%d)' % nsel) == n2_rule(nsel, 20, 40))
hc6.reset_records()
hc6.execute('pv_PowEView()')
Le = hc6.pages[0].lines()
pwe = list(hc6.globals_['PWC'])
oke = all(abs(pwe[c - 1] - zpow(c / 250 * 1.5 * math.sqrt(250), 10, 20, 40, 20, .05, 1)) < 1e-12 for c in range(1, 251))
check('C6 Pow-effect: power at d = c/250 x 1.5 with delta = d sigma\', every column = SciPy', oke)
check('C6 Pow-effect subtitle "n = 40, 20; α = 0.050; 1-sided", axis "Cohen\'s d"',
      'n = 40, 20; α = 0.050; 1-sided' in Le and "Cohen's d" in Le, Le)

# the formula page
for cas in ('giac', 'fail'):
    hf = Harness(PROG, idle_key=4, cas=cas, home_minus=True)
    hf.execute('pv_Init()')
    put(hf, TT=5, MM0=100, MM1=105, SG=10, SG2=20, NN=40, NN2=20, KN1=40, AL=0.05, TL=1, WFIT=1, WHLD=0)
    hf.execute('pv_Setup()')
    hf.reset_records()
    hf.execute('pv_Formula()')
    Lf = hf.pages[0].lines()
    print('   formula page (%s):' % cas)
    for x in Lf:
        print('     ' + x)
    if cas == 'giac':
        need = ['exact (CAS)', '  SE = √(σ₁²/n₁ + σ₂²/n₂),  n₂ = k×n₁', 'CAS, solved for n₁:',
                'CAS, with σ₁ = 10, σ₂ = 20, k = 0.5, |μ₂−μ₁| = 5:', '  n₁ = 2×(3×√2×zα+3×√2×zβ)^2',
                '  n₁ = ((1.645 + 0.842)×√(100 + 800)/5)² = 222.57',
                'Round UP: n₁ = 223, n₂ = 112; trying: n₈₀ = 223, 112',
                'Best split of n₁+n₂: n₂/n₁ = σ₂/σ₁ = 2.00 (yours 0.50)']
    else:
        need = ['decimal', '  n₁ = (zα+zβ)²×(σ₁² + σ₂²/k)/(μ₂−μ₁)²', '(no CAS) σ₁ = 10, σ₂ = 20, k = 0.5, |μ₂−μ₁| = 5',
                '  n₁ = ((1.645 + 0.842)×√(100 + 800)/5)² = 222.57', 'Round UP: n₁ = 223, n₂ = 112; trying: n₈₀ = 223, 112']
    check('C7 the formula page, cas=%s: %d expected lines present; at most 15 body lines' % (cas, len(need)),
          all(n in Lf for n in need) and len(Lf) <= 18, [n for n in need if n not in Lf])
    check('C7 cas=%s: the value 222.59 = (za+zb)^2 (100 + 400/0.5)/25 = %.4f' % (cas, (norm.isf(.05) + norm.ppf(.8)) ** 2 * 900 / 25),
          abs(g(hf, 'NCF') - (norm.isf(.05) + norm.ppf(.8)) ** 2 * 900 / 25) < 1e-9)

# help page 4
hh4 = Harness(PROG, idle_key=4, cas='giac', home_minus=True)
hh4.execute('pv_Init()')
hh4.reset_records()
hh4.execute('pv_ShowHelp()')
P4 = hh4.pages[3].lines()
for x in P4:
    print('     ' + x)
check('C8 help page 4: title, SE, ratio, sigma\', best split, Cohen\'s pooled-t warning, Welch, n80',
      P4[0] == 'PowerViz  help  4/5: unequal σ and n' and any('σ₂²/n₂' in x for x in P4) and
      any('σ\' = √((σ₁²+σ₂²)/2)' in x for x in P4) and any('n₂/n₁ = σ₂/σ₁' in x for x in P4) and
      any('Cohen 1988, p. 44' in x for x in P4) and any('Welch' in x for x in P4) and len(P4) == 16, P4)


# ===================================================================== E. Levene's power page
print('=== E. Levene\'s test: the power page')
from scipy import stats as SS
he = H(PROG)


def fpow(s1, s2, n1, n2, al):
    d1, d2, r2 = n1 - 1, n2 - 1, (s2 / s1) ** 2
    return SS.f.cdf(SS.f.ppf(al / 2, d2, d1) / r2, d2, d1) + SS.f.sf(SS.f.isf(al / 2, d2, d1) / r2, d2, d1)


bad = []
nf = 0
for s1, s2 in ((10, 20), (20, 10), (10, 10), (10, 13), (1, 5), (7, 3)):
    for n1, n2 in ((40, 20), (20, 40), (5, 5), (100, 300), (2, 3), (1000, 50)):
        for al in (0.05, 0.01, 0.2, 0.001):
            v = he.execute('pv_FPow(%r,%d,%d,%r)' % ((s2 / s1) ** 2, n1 - 1, n2 - 1, al))
            r = fpow(s1, s2, n1, n2, al)
            nf += 1
            if abs(v - r) > 1e-9:
                bad.append((s1, s2, n1, n2, al, v, r))
check('E1 pv_FPow (the exact two-sided F test of s2^2/s1^2, both tails as lower tails) = SciPy, %d cases' % nf,
      not bad, bad[:3])


def lev_sim_np(s1, s2, n1, n2, al, R=40000):
    x = rng.normal(0, s1, (R, n1))
    y = rng.normal(0, s2, (R, n2))
    z1 = np.abs(x - x.mean(1, keepdims=True))
    z2 = np.abs(y - y.mean(1, keepdims=True))
    N = n1 + n2
    m1, m2 = z1.mean(1), z2.mean(1)
    m = (n1 * m1 + n2 * m2) / N
    ssb = n1 * (m1 - m) ** 2 + n2 * (m2 - m) ** 2
    ssw = ((z1 - m1[:, None]) ** 2).sum(1) + ((z2 - m2[:, None]) ** 2).sum(1)
    return ((ssb / (ssw / (N - 2))) > SS.f.isf(al, 1, N - 2)).mean()


# check the numpy simulator itself against SciPy's levene on a few samples
okl = True
for _ in range(20):
    a = rng.normal(0, 10, 13)
    b = rng.normal(0, 25, 9)
    st = SS.levene(a, b, center='mean')
    za, zb = np.abs(a - a.mean()), np.abs(b - b.mean())
    N = 22
    mz = (za.sum() + zb.sum()) / N
    F = (13 * (za.mean() - mz) ** 2 + 9 * (zb.mean() - mz) ** 2) / ((((za - za.mean()) ** 2).sum() + ((zb - zb.mean()) ** 2).sum()) / (N - 2))
    okl = okl and abs(F - st.statistic) < 1e-9
check('E2 the reference simulator\'s Levene F = scipy.stats.levene(center="mean") on 20 random samples', okl)
apx = []
for s1, s2, n1, n2 in ((10, 15, 150, 91), (10, 12, 300, 200), (10, 11, 1000, 500), (12, 10, 200, 100), (10, 14, 121, 120)):
    he.globals_.update(dict(TT=5.0))
    a = he.execute('pv_LvApx(%r,%r,%d,%d,0.05)' % (s1, s2, n1, n2))
    sm = lev_sim_np(s1, s2, n1, n2, 0.05)
    apx.append((s1, s2, n1, n2, round(a, 3), round(sm, 3), abs(a - sm) < 0.02))
check('E2 pv_LvApx (used only past n1 + n2 = 240) within 0.02 of a 40,000-pair simulation: ' + str(apx),
      all(x[-1] for x in apx))
sims = []
for s1, s2, n1, n2t, al, seed in ((10, 20, 40, 20, 0.05, 3), (10, 13, 40, 20, 0.05, 4), (10, 10, 30, 30, 0.05, 5),
                                  (25, 8, 12, 30, 0.01, 6)):
    hs = Harness(PROG, idle_key=4, cas='giac', home_minus=True, seed=seed)
    hs.execute('pv_Init()')
    put(hs, TT=5, MM0=100, MM1=105, SG=s1, SG2=s2, NN=n1, NN2=n2t, KN1=n1, AL=al, TL=1)
    rr = hs.execute('pv_LvSim(400)')
    est = rr[0] / rr[1]
    ref = lev_sim_np(s1, s2, n1, n2t, al)
    se = math.sqrt(max(ref * (1 - ref), 1e-4) / 400)
    sims.append((s1, s2, n1, n2t, al, round(est, 3), round(ref, 3), abs(est - ref) < 3.5 * se))
check('E3 pv_LvSim (400 pairs in the harness) within 3.5 SE of a 40,000-pair simulation: ' + str(sims),
      all(x[-1] for x in sims))
hs = Harness(PROG, idle_key=4, cas='giac', home_minus=True, seed=11)
hs.execute('pv_Init()')
dr = [hs.execute('pv_RNorm()') for _ in range(20000)]
ks = SS.kstest(dr, 'norm')
check('E4 pv_RNorm: 20,000 draws, mean %.4f, SD %.4f, KS p %.3f (normal)' % (np.mean(dr), np.std(dr), ks.pvalue),
      abs(np.mean(dr)) < 0.03 and abs(np.std(dr) - 1) < 0.03 and ks.pvalue > 0.001)


LV_FIRST = []


def lv_pages(**kv):
    h = Harness(PROG, idle_key=4, cas='giac', home_minus=True, seed=2)
    h.execute('pv_Init()')
    put(h, **dict(dict(TT=5, MM0=100, MM1=105, SG=10, SG2=20, NN=40, NN2=20, KN1=40, AL=0.05, TL=1, WFIT=1, WHLD=0), **kv))
    h.execute('pv_Setup()')
    h.reset_records()
    h.execute('pv_LvPage()')
    pages = [p.lines() for p in h.pages]
    # v2.5k: the page opens with what it is and is not; kept apart here (LV_FIRST), checked in E7
    if pages and len(pages[0]) > 1 and pages[0][1].startswith('A Levene F, as SPSS or R prints it'):
        LV_FIRST.append(pages.pop(0))
    return h, pages, [m.lines for m in h.msgboxes]


h1, P, M = lv_pages()
for i, pg in enumerate(P):
    print('   Levene page %d:' % i)
    for x in pg:
        print('     ' + x)
lv = h1.globals_['pvLvR']
check('E5 defaults: a "simulating" frame, then page 1 with both numbers and page 2 with the reading; %d pairs' % lv[1],
      len(P) == 3 and lv[2] == 1 and lv[1] == 400 and any(x.startswith('Levene (simulated, 400 pairs): ') for x in P[1])
      and 'F test of s₁²/s₂² (exact, normal data): %.2f' % fpow(10, 20, 40, 20, 0.05) in P[1]
      and 'whose α can be far off (Cohen 1988, p. 44).' in P[2] and '(Delacre, Lakens & Leys 2017).' in P[2])
pct = int(round(100 * lv[0]))
check('E5 page 2 says "%d of 100" and "the other %d" from the simulated power' % (pct, 100 - pct),
      'test flags it in about %d of 100 such studies.' % pct in P[2] and
      'In the other %d, a \'Levene first\' rule keeps' % (100 - pct) in P[2])
h1.reset_records()
h1.execute('pv_LvPage()')
check('E5 reopened with nothing changed: the first screen again, then no new simulation (no "simulating" frame), '
      'the same result', len(h1.pages) == 3 and h1.pages[0].lines()[1].startswith('A Levene F') and
      list(h1.globals_['pvLvR']) == list(lv))
_, P, _ = lv_pages(SG=15, SG2=15, NN=30, NN2=30, KN1=30)
check('E5 sigma1 = sigma2: "With σ₁ = σ₂, Levene\'s test still says" ... "that is α."',
      P[2][1].startswith("With σ₁ = σ₂, Levene's test still says") and P[2][2].endswith('studies: that is α.'), P[2][:3])
_, P, _ = lv_pages(NN=30, NN2=30, KN1=30)
check('E5 n1 = n2: "which with n₁ = n₂ stays close to α."', 'which with n₁ = n₂ stays close to α.' in P[2])
_, P, _ = lv_pages(NN=200, NN2=100, KN1=200, SG=10, SG2=12)
check('E5 n1 + n2 = 300 (past 240): the large-sample formula, no simulation, no +-',
      len(P) == 2 and any(x.startswith('Levene (large-sample formula): ') for x in P[0]), P[0][-6:])
_, P, M = lv_pages(TT=2, SG=15)
check('E5 tests other than 5: a box, no page', not P and M and 'Two Means, unequal σ & n' in M[0][0], M)
# v2.5k: the first screen, with Roger's numbers (his SPSS output: Levene F 6.847 from 416 scores)
LV_FIRST.clear()
_, P, _ = lv_pages(MM0=4.8185, MM1=6.4247, SG=3.28798, SG2=3.74872, NN=270, NN2=146, KN1=270, AL=0.05, TL=2)
first = LV_FIRST[0] if LV_FIRST else []
for x in first:
    print('     ' + x)
want1 = ["Would Levene's test notice?", 'A Levene F, as SPSS or R prints it, comes from',
         "every score (here 416): how far each one sits", "from its group's mean. PowerViz has only the",
         "means, SDs and n's, so it cannot work out that", 'F, and it does not try.',
         'This page asks a planning question instead:', 'if the population SDs really are 3.288 and',
         "3.749, how often would Levene's test notice", 'with samples of 270 and 146?',
         'To see a Levene F worked out from data, use', 'Menu > Two samples: data (built-in examples,',
         'or a short list of your own in D1 and D2).', 'any key or tap = go on']
check('E7 the power page opens with what it is and is not (v2.5k), Roger\'s numbers filled in: 416 scores, SDs '
      '3.288 and 3.749, n 270 and 146; then the large-sample page (n1 + n2 > 240)',
      first == want1 and len(P) == 2 and any(x.startswith('Levene (large-sample formula): ') for x in P[0]),
      [x for x in want1 if x not in first] or first)
hm = Harness(PROG, idle_key=4, cas='giac', home_minus=True)
hm.execute('pv_Init()')
hm.choose(0)
hm.execute('pv_MainMenu()')
check('E7 the menu item reads "Would Levene notice?" (was "Levene\'s test: power"), at most 30 characters',
      hm.chooses[0].items[6] == 'Would Levene notice?' and "Levene's test: power" not in hm.chooses[0].items,
      hm.chooses[0].items)
hh5 = Harness(PROG, idle_key=4, cas='giac', home_minus=True)
hh5.execute('pv_Init()')
hh5.reset_records()
hh5.execute('pv_ShowHelp()')
P5 = hh5.pages[4].lines()
check('E7 help page 5 says what the page answers and why it gives no Levene F',
      'MENU, Would Levene notice? (unequal σ test):' in P5 and "  It cannot give SPSS's Levene F: that F needs" in P5
      and '  every score; PowerViz has means, SDs and n.' in P5, P5)

# the claims on page 2
eqn = []
for s1, s2, n in ((10, 20, 20), (10, 20, 40), (10, 30, 10), (10, 20, 5)):
    Rr = 100000
    x = rng.normal(0, s1, (Rr, n))
    y = rng.normal(0, s2, (Rr, n))
    sp_ = np.sqrt((x.var(1, ddof=1) + y.var(1, ddof=1)) / 2)
    tt_ = (y.mean(1) - x.mean(1)) / (sp_ * np.sqrt(2 / n))
    eqn.append((s1, s2, n, round((np.abs(tt_) > SS.t.isf(0.025, 2 * n - 2)).mean(), 4)))
check('E6 "with n₁ = n₂ [the pooled t] stays close to α": simulated true alpha at nominal 0.05, sigma ratio 2-3: '
      + str(eqn), all(0.045 < e[3] < 0.065 for e in eqn))
sk = []
for lab, gen in (('lognormal', lambda sh: np.exp(rng.normal(0, 1, sh))), ('exponential', lambda sh: rng.exponential(1, sh)),
                 ('chi-square 4', lambda sh: rng.chisquare(4, sh))):
    for n1, n2 in ((20, 20), (40, 20)):
        Rr = 40000
        x = gen((Rr, n1))
        y = gen((Rr, n2))
        F = y.var(1, ddof=1) / x.var(1, ddof=1)
        af = ((F < SS.f.ppf(0.025, n2 - 1, n1 - 1)) | (F > SS.f.isf(0.025, n2 - 1, n1 - 1))).mean()
        res = [lab, n1, n2, round(af, 3)]
        for cen in ('mean', 'median'):
            cx = x.mean(1, keepdims=True) if cen == 'mean' else np.median(x, 1, keepdims=True)
            cy = y.mean(1, keepdims=True) if cen == 'mean' else np.median(y, 1, keepdims=True)
            z1, z2 = np.abs(x - cx), np.abs(y - cy)
            N = n1 + n2
            m1, m2 = z1.mean(1), z2.mean(1)
            m = (n1 * m1 + n2 * m2) / N
            FL = (n1 * (m1 - m) ** 2 + n2 * (m2 - m) ** 2) / ((((z1 - m1[:, None]) ** 2).sum(1) + ((z2 - m2[:, None]) ** 2).sum(1)) / (N - 2))
            res.append(round((FL > SS.f.isf(0.05, 1, N - 2)).mean(), 3))
        sk.append(tuple(res))
check('E6 page 2\'s "skewed data fool [the F test] badly. Levene\'s test (means) is fooled less; its median form '
      '(Brown-Forsythe) hardly at all": equal spreads, skewed data, nominal 0.05, true alpha of F, Levene-mean, '
      'Brown-Forsythe: ' + str(sk), all(x[3] > 0.15 and x[3] > x[4] > x[5] and x[4] > 0.08 and x[5] < 0.06 for x in sk))

# ===================================================================== F. the two-samples page
print('=== F. Two samples: data')
import re as _re
an = open(os.path.join(REPO, 'programs', 'AnovaLab_beta1a.txt'), encoding='utf-8').read()
seg = an[an.index('av_LdDraft()\nBEGIN'):]
dv_ = [int(float(x)) for x in _re.search(r'avOY := \{([^}]*)\}', seg).group(1).replace('\n', ' ').split(',')]
hf = H(PROG)
dj = [int(v) for v in hf.execute('pv_Draft(1)')]
dd_ = [int(v) for v in hf.execute('pv_Draft(2)')]
check('F1 pv_Draft(1) + pv_Draft(2) = AnovaLab\'s 366 numbers, number for number (182 + 184)',
      dj + dd_ == dv_ and len(dj) == 182 and len(dd_) == 184)
alld = dj + dd_
dec = alld[335:366]
check('F1 against published facts: a permutation of 1-366; 1 on Sep 14 (day 258), 2 on Apr 24 (day 115); only Dec 2, '
      '12, 15, 17 and 19 above 195 (Wikipedia, Draft lottery (1969))',
      sorted(alld) == list(range(1, 367)) and alld[257] == 1 and alld[114] == 2 and
      [i + 1 for i, v in enumerate(dec) if v > 195] == [2, 12, 15, 17, 19])
segi = an[an.index('av_LdInsect()\nBEGIN'):]
iv = [int(float(x)) for x in _re.search(r'avOY := \{([^}]*)\}', segi).group(1).replace('\n', ' ').split(',')]
pvsrc = open(PROG, encoding='utf-8').read()
check('F1 the insect-spray lists = AnovaLab\'s sprays C and F',
      'dga:={' + ','.join(str(v) for v in iv[24:36]) + '};' in pvsrc and
      'dgb:={' + ','.join(str(v) for v in iv[60:72]) + '};' in pvsrc)


def twos_ref(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    n1, n2 = len(a), len(b)
    m1, m2 = a.mean(), b.mean()
    s1, s2 = a.std(ddof=1), b.std(ddof=1)
    lm = SS.levene(a, b, center='mean')
    lb = SS.levene(a, b, center='median')
    tp = SS.ttest_ind(b, a, equal_var=True)
    tw = SS.ttest_ind(b, a, equal_var=False)
    v1, v2 = s1 ** 2 / n1, s2 ** 2 / n2
    df = (v1 + v2) ** 2 / (v1 ** 2 / (n1 - 1) + v2 ** 2 / (n2 - 1))
    sp_ = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
    return [n1, m1, s1, n2, m2, s2, lm.statistic, lm.pvalue, lb.statistic, lb.pvalue, tp.statistic, n1 + n2 - 2,
            tp.pvalue, tw.statistic, df, tw.pvalue, (m2 - m1) / sp_, (m2 - m1) / math.sqrt((s1 ** 2 + s2 ** 2) / 2)]


def lst(v):
    return '{' + ','.join(repr(float(x)) for x in v) + '}'


worst = 0.0
cases = [(dj, dd_), ([0, 1, 7, 2, 3, 1, 2, 1, 3, 0, 1, 4], [11, 9, 15, 22, 15, 16, 13, 10, 26, 26, 24, 13]),
         (iv[36:48], iv[0:12])]
for _ in range(200):
    n1, n2 = int(rng.integers(2, 40)), int(rng.integers(2, 40))
    cases.append((list(np.round(rng.normal(50, rng.uniform(1, 20), n1), 2)),
                  list(np.round(rng.normal(55, rng.uniform(1, 20), n2), 2))))
for a, b in cases:
    got = hf.execute('pv_TwoS(%s,%s)' % (lst(a), lst(b)))
    ref = twos_ref(a, b)
    for g_, r_ in zip(got, ref):
        worst = max(worst, abs(g_ - r_) / max(1.0, abs(r_)))
check('F2 pv_TwoS = SciPy (levene center mean and median, ttest_ind pooled and Welch, Welch df, d with the pooled s '
      'and with sigma\') on the 3 presets and 200 random pairs of samples (largest relative difference %.1e)' % worst,
      worst < 1e-9)


def data_pages(src, app=None, al=0.05):
    h = Harness(PROG, idle_key=4, cas='giac', home_minus=True, app_data=app or {})
    h.execute('pv_Init()')
    put(h, TT=5, AL=al)
    h.choose(src)
    h.execute('pv_DataPage()')
    return [p.lines() for p in h.pages], [m.lines for m in h.msgboxes]


P, M = data_pages(1)
for i, pg in enumerate(P):
    print('   data page (draft) %d:' % i)
    for x in pg:
        print('     ' + x)
need1 = ['Jan-Jun: n 182, mean 206.32, s 106.14', 'Jul-Dec: n 184, mean 160.92, s 100.76',
         'Levene (means, as SPSS): F = 0.96, p = 0.329', '  (medians, Brown-Forsythe): p = 0.378',
         'Pooled t(364) = −4.20, p < 0.001', 'Welch  t(362.6) = −4.20, p < 0.001', 'd = −0.44', 'Cohen\'s d, pooled s; small']
need2 = ['SPREADS: Levene p = 0.329, above α = 0.050:', '  no clear sign they differ. That is not proof',
         'MEANS: Welch\'s t test, p < 0.001.', '  less than 0.1 % of the time.', '  Pooled and Welch agree about p < α here.',
         'SIZE: d = −0.44. Jul-Dec\'s mean is 0.44 SDs', '  below Jan-Jun\'s: a small difference']
check('F3 the draft lottery: page 1 (strip plot, numbers, d) and page 2 (the reading), every number = SciPy',
      all(x in P[0] for x in need1) and all(x in P[1] for x in need2),
      [x for x in need1 if x not in P[0]] + [x for x in need2 if x not in P[1]])
P, M = data_pages(2)
need = ['Levene (means, as SPSS): F = 16.34, p < 0.001', '  (medians, Brown-Forsythe): p = 0.011',
        'Pooled t(22) = 7.75, p < 0.001', 'Welch  t(13.2) = 7.75, p < 0.001', 'd = 3.16']
check('F3 insect sprays C and F: Levene F 16.34, Brown-Forsythe p 0.011, t 7.75 with df 22 and 13.2, d 3.16; '
      '"the spreads look different. Read Welch\'s t."', all(x in P[0] for x in need) and
      '  the spreads look different. Read Welch\'s t.' in P[1], [x for x in need if x not in P[0]])
P, M = data_pages(3, app={'D1': [3, 5, 4, 6, 5, 4], 'D2': [9, 2, 14, 1, 11]})
ref = twos_ref([3, 5, 4, 6, 5, 4], [9, 2, 14, 1, 11])
check('F4 D1 and D2 from the Statistics 1Var app: read, named D1/D2, numbers = SciPy (Welch df %.1f)' % ref[14],
      P and 'Welch  t(%.1f) = %.2f, p = %.3f' % (ref[14], ref[13], ref[15]) in P[0] and P[0][0] == 'Two samples: D1 and D2', P[0] if P else M)
P, M = data_pages(3)
check('F4 no D1 (app never opened): a box saying where to put the data, no page',
      not P and M and M[0][0].startswith('Put group 1 in D1 and group 2 in D2'), M)
P, M = data_pages(3, app={'D1': [5], 'D2': [1, 2, 3]})
check('F4 one value in D1: the same box', not P and M and M[0][0].startswith('Put group 1 in D1'), M)
P, M = data_pages(3, app={'D1': [4, 4, 4], 'D2': [7, 7]})
check('F4 no spread in either group: a box, no page', not P and M and M[0][0].startswith('Both groups have no spread'), M)
# small spreads (glass refractive indices, blood alcohol levels): means and SDs get 3 significant digits of the
# larger s, 2 decimals at least and 8 at most (the numbers are typed for the test, not a published data set)
dec_res = []
for a_, b_ in (([1.51812, 1.51825, 1.51809, 1.51830, 1.51818], [1.52031, 1.52044, 1.52027, 1.52050]),
               ([0.081, 0.095, 0.078, 0.102, 0.088], [0.121, 0.134, 0.110, 0.142]),
               ([3, 5, 4, 6, 5, 4], [9, 2, 14, 1, 11])):
    P, M = data_pages(3, app={'D1': a_, 'D2': b_})
    r = twos_ref(a_, b_)
    dm = max(2, min(8, 2 - math.floor(math.log10(max(r[2], r[5])))))
    w1 = 'D1: n %d, mean %.*f, s %.*f' % (r[0], dm, r[1], dm, r[2])
    w2 = 'D2: n %d, mean %.*f, s %.*f' % (r[3], dm, r[4], dm, r[5])
    dec_res.append((dm, w1 in P[0], w2 in P[0], w1))
check('F4 the means and SDs print with 3 significant digits of the larger s (6, 4 and 2 decimals for s near '
      '0.0001, 0.01 and 5): ' + str([(d[0], d[3]) for d in dec_res]), [d[0] for d in dec_res] == [6, 4, 2] and
      all(d[1] and d[2] for d in dec_res), dec_res)

# extreme data: pv_TwoS divides values beyond 1E50 or under 1E-50 by a power of 10 first, so t, F, p, df and d
# equal those of the same data at an ordinary scale, and the means and SDs carry the factor
a0 = list(np.round(rng.normal(50, 8, 15), 2))
b0 = list(np.round(rng.normal(56, 14, 9), 2))
ref0 = twos_ref(a0, b0)
worstx = 0.0
for f in (1e100, 1e-100, 1e60, 1e-60, 1e200, 1e-200):
    got = hf.execute('pv_TwoS(%s,%s)' % (lst([x * f for x in a0]), lst([x * f for x in b0])))
    for k, (g_, r_) in enumerate(zip(got, ref0)):
        if k in (1, 2, 4, 5):
            worstx = max(worstx, abs(g_ - r_ * f) / abs(r_ * f))
        else:
            worstx = max(worstx, abs(g_ - r_) / max(1.0, abs(r_)))
check('F2 pv_TwoS on the same samples times 1E100, 1E-100, 1E60, 1E-60, 1E200 and 1E-200: every t, F, p, df and d '
      'as at the ordinary scale, means and SDs times the factor (largest relative difference %.1e)' % worstx,
      worstx < 1e-9)

# a pair where the pooled and Welch t disagree about p < 0.05 (small group with the big spread)
found = None
for _ in range(4000):
    a = list(np.round(rng.normal(0, 1, 30), 1))
    b = list(np.round(rng.normal(rng.uniform(0.5, 2.5), 6, 6), 1))
    r = twos_ref(a, b)
    if (r[12] < 0.05) != (r[15] < 0.05):
        found = (a, b, r)
        break
P, M = data_pages(3, app={'D1': found[0], 'D2': found[1]})
check('F5 a pair where the pooled t says p %.3f and Welch p %.3f: "Pooled and Welch DISAGREE: go with Welch\'s."'
      % (found[2][12], found[2][15]), '  Pooled and Welch DISAGREE: go with Welch\'s.' in P[1], P[1])
mid = [v for v in P[1] if '% of the time' in v]
check('F5 a moderate p is written "about x % of the time" (x = 100 p, one decimal): ' + str(mid),
      mid and (('about %.1f %%' % (100 * found[2][15])) in mid[0] if found[2][15] >= 0.001 else 'less than' in mid[0]))

# robustness: odd data and odd settings must give a page or a box, never a PPL error
errs = []
odd = [([1, 2], [3, 5]), ([1, 1, 1, 2], [5, 5, 5, 5]), ([1e100, 2e100, 3e100], [4e100, 1e100]),
       ([1e-100, 2e-100, 3e-100], [5e-100, 1e-100, 9e-100]), ([-5, -7, -6, -9], [-1, -2, -1]), ([3, 3, 4], [3, 3, 4]),
       (list(range(1, 501)), [250, 251]), ([0, 0, 0, 1], [0, 0, 1, 1, 1])]
for a_, b_ in odd:
    try:
        P, M = data_pages(3, app={'D1': a_, 'D2': b_})
        if not P and not M:
            errs.append(('nothing shown', a_[:3], b_[:3]))
    except Exception as e:
        errs.append((type(e).__name__, str(e)[:60], a_[:3], b_[:3]))
for kv in (dict(SG=1, SG2=1000), dict(SG=1000, SG2=1), dict(NN=2, NN2=2, KN1=2), dict(NN=2, NN2=20, KN1=2),
           dict(NN=5000, NN2=500, KN1=5000), dict(AL=0.999), dict(AL=1e-13), dict(SG=1e-200, SG2=3e-200)):
    try:
        _, P, M = lv_pages(**kv)
        if not P:
            errs.append(('no Levene page', kv))
    except Exception as e:
        errs.append((type(e).__name__, str(e)[:60], kv))
check('F6 robustness: 8 odd data sets (2 values, ties, 1E100, 1E-100, negatives, equal groups, 500 vs 2) and 8 odd '
      'Levene settings (sigma ratio 1000, n 2/2, n 5000/500, alpha 0.999 and 1E-13, sigma 1E-200): a page or a box, '
      'never an error', not errs, errs)

# ===================================================================== G. d on the plot
print('=== G. d on the plot')
gres = []
for tt, kv in ((1, dict(MM0=100, MM1=105, SG=15)), (2, dict(MM0=100, MM1=105, SG=15)), (3, dict(PP0=0.5, PP1=0.6)),
               (4, dict(PP0=0.5, PP1=0.6)), (5, dict(MM0=100, MM1=105, SG=10, SG2=20, NN2=20, KN1=40))):
    hg = H(PROG)
    pg = draw(hg, TT=tt, NN=40 if tt == 5 else 30, AL=0.05, TL=1, **kv)
    lab = [t for t in pg.texts if round(t.y) == 47 and t.font == 1 and t.hex == '#C800C8']
    want = ('d' if tt in (1, 2, 5) else 'h') + ' = %.2f' % round(hg.execute('pv_EffSz()'), 2)
    arrows = [sh for sh in pg.shapes if sh.cmd == 'LINE_P' and len(sh.args) >= 5 and sh.args[1] == 44 and sh.args[3] == 44]
    gres.append((tt, lab[0].text if lab else None, want, len(arrows)))
check('G1 every test: the label under the magenta arrow is d (h for proportions) to 2 decimals, and the arrow is '
      'drawn at y 44: ' + str(gres), all(g[1] == g[2] and g[3] == 1 for g in gres))
hg = H(PROG)
pg = draw(hg, TT=1, NN=30, AL=0.05, TL=1, MM0=100, MM1=100, SG=15)
lab = [t.text for t in pg.texts if round(t.y) == 47 and t.font == 1]
arrows = [sh for sh in pg.shapes if sh.cmd == 'LINE_P' and len(sh.args) >= 5 and sh.args[1] == 44 and sh.args[3] == 44]
check('G1 no effect: no arrow, the label "d = 0.00" beside the centre', not arrows and lab == ['d = 0.00'], (lab, len(arrows)))

# ===================================================================== H. v2.5i and v2.5j
print('=== H. v2.5i and v2.5j: a finger left on OK, "!=", the readout box, the statistic obtained')
import tempfile as _tf


def hold_after(h, which, x, y, n=3):
    """model Roger's run: when dialog number `which` (CHOOSE or INPUT, counted from 1) closes, the finger that tapped
    its OK is still on the glass at (x, y) for n more MOUSE readings"""
    orig = h._dialog_closed
    st = {'k': 0}

    def patched(ok):
        orig(ok)
        st['k'] += 1
        if st['k'] == which:
            h._finger = [[float(x), float(y), float(x), float(y), 0.0]] + [[float(x), float(y), float(x), float(y), 2.0]] * n
    h._dialog_closed = patched


def run_held(path, script):
    h = Harness(path, idle_key=4, cas='giac', home_minus=True)
    script(h)
    try:
        h.execute('POWERVIZ()')
        err = None
    except Exception as e:      # a CHOOSE or INPUT with no answer queued: the stray tap opened something
        err = '%s: %s' % (type(e).__name__, str(e)[:90])
    return h, err


def s_edit(h):                  # Edit soft key, OK tapped, finger still on OK (= Menu, slot 6)
    h.choose(3)
    h.answer(ACCEPT)
    h.tap(30, 230)
    h.answer(ACCEPT)
    hold_after(h, 3, 290, 230)


def s_ncell(h):                 # the n row, its two-field form, OK tapped and held
    h.choose(3)
    h.answer(ACCEPT)
    h.tap(30, 170)
    h.answer(ACCEPT)
    hold_after(h, 3, 290, 230)


def s_enter(h):                 # Enter opens the menu, "Return to plot" tapped, the finger held over the n row
    h.choose(3)
    h.answer(ACCEPT)
    h.press('Enter')
    h.choose('Return to plot')
    hold_after(h, 3, 30, 170)


res = []
for name, sc, bad in (('Edit', s_edit, 'PowerViz Menu'), ('n row', s_ncell, 'PowerViz Menu'), ('Enter', s_enter, 'Sample sizes')):
    h, err = run_held(PROG, sc)
    opened = [d.title for d in h.dialogs]
    res.append((name, err, opened))
check('H1 a finger left on a form\'s OK or a menu item is waited out (pv_TDrain), not read as a tap: Edit, the n row '
      'and Enter -> Return, no stray menu or form: ' + str([(r[0], r[2]) for r in res]),
      all(r[1] is None and r[2].count('PowerViz Menu') == (1 if r[0] == 'Enter' else 0) and 'Sample sizes' not in r[2][3:]
          for r in res), res)
# the control: the same run on a copy without v2.5i's pv_TDrain after Edit reproduces Roger's report
src = open(PROG, encoding='utf-8').read()
ctl = src.replace('pv_EditForm(); pv_Drain(); pv_TDrain(); WFIT:=1; END;   // Edit',
                  'pv_EditForm(); pv_Drain(); WFIT:=1; END;   // Edit')
tdir = _tf.mkdtemp()
cpath = os.path.join(tdir, 'PowerViz_ctl.txt')
with open(cpath, 'w', encoding='utf-8') as f:
    f.write(ctl)
h, err = run_held(cpath, s_edit)
check('H1 control: without that pv_TDrain the held finger opens the PowerViz Menu, as on Roger\'s calculator (%s)'
      % (err or [d.title for d in h.dialogs]), ctl != src and ('PowerViz Menu' in (err or '') or
                                                                 'PowerViz Menu' in [d.title for d in h.dialogs]))
# the sigma row opens the whole Edit form
h = Harness(PROG, idle_key=4, cas='giac', home_minus=True)
h.choose(3)
h.answer(ACCEPT)
h.tap(30, 196)
h.answer(ACCEPT)
h.execute('POWERVIZ()')
check('H1 a tap on test 5\'s sigma row opens the Edit form ("%s")' % h.inputs[-1].title,
      len(h.inputs) == 2 and h.inputs[-1].title == 'Two Means, unequal σ & n')

code_ne = [i + 1 for i, line in enumerate(src.split('\n')) if '!=' in line.split('//')[0]]
check('H2 no "!=" left in the code (pv_FMTP\'s floor reads "xx <> 0"); lines with it: %s' % code_ne,
      not code_ne and 'IF xx <> 0 AND ABS(xx) < thr THEN' in src)
hf2 = H(PROG)
check('H2 pv_FMTP(3.534E-96, 3) = "< 0.001" (Roger\'s panel showed "3.534E-96")',
      hf2.execute('pv_FMTP(3.534E-96,3)') == '< 0.001')

# Roger's numbers (his SPSS output: male n 270, mean 4.8185, SD 3.28798; female 146, 6.4247, 3.74872)
rog = dict(SG=3.28798, SG2=3.74872, NN=270, NN2=146, KN1=270, AL=0.05, TL=2, MM1=6.4247)
hr = H(PROG)
pr = draw(hr, TT=5, MM0=4.8185, **rog)
Lr = pr.lines()
z = (6.4247 - 4.8185) / math.sqrt(3.28798 ** 2 / 270 + 3.74872 ** 2 / 146)
pw = norm.cdf(z - norm.isf(0.025)) + norm.cdf(-z - norm.isf(0.025))
check('H3 Roger\'s data: the table %s, "d = 0.46, small", POWER "%s" (SciPy %.4f), SE0 0.369 (SPSS .36918), '
      'n80 "112, 61"' % (table5(pr), cell(pr, 240, 167), pw),
      table5(pr) == (('270', '146'), ('4.819', '6.425'), ('3.288', '3.749')) and 'd = 0.46, small' in Lr and
      cell(pr, 240, 167) == '%.3f' % pw and 'SE₀ = 0.369' in Lr and 'n₈₀ = 112, 61 (111.96)' in Lr, Lr)
pr2 = draw(hr, TT=5, MM0=14.8185, **rog)
L2 = pr2.lines()
check('H3 his slip (mu grp1 14.8185): the table shows it, d = -2.38, "β < 0.001", "> 0.999", n80 "5, 3 (4.1)"',
      table5(pr2)[1] == ('14.819', '6.425') and 'd = −2.38, large' in L2 and 'β < 0.001' in L2 and
      '> 0.999' in L2 and 'n₈₀ = 5, 3 (4.1)' in L2, L2)
pyb = []
for tt in (1, 2, 3, 4, 5):
    hh = H(PROG)
    pg = draw(hh, TT=tt, MM0=100, MM1=105, SG=10, SG2=20, NN=40, NN2=20, KN1=40, PP0=0.5, PP1=0.6, AL=0.05, TL=1)
    ticks = [t for t in pg.texts if round(t.y) == g(hh, 'PYB') + 5]
    pyb.append((tt, g(hh, 'PYB'), len(ticks), max((t.y for t in ticks), default=0)))
check('H4 the plot ends at y 133 in every test (146 before; tests 2, 4 and 5 from v2.5i, all from v2.5j); its tick labels end above the box at 150: %s'
      % pyb, [p[1] for p in pyb] == [133] * 5 and all(p[2] > 0 and p[3] + 10 <= 150 for p in pyb), pyb)

# the df (v2.5i) and the statistic obtained (v2.5j) under POWER: Welch-Satterthwaite df in test 5, 2n - 2 in test 2,
# n - 1 in test 1; z for the proportions


def welch_df(s1, s2, n1, n2):
    a, b = s1 ** 2 / n1, s2 ** 2 / n2
    return (a + b) ** 2 / (a ** 2 / (n1 - 1) + b ** 2 / (n2 - 1))


hd = H(PROG)
worst_df = 0.0
for s1, s2, n1, n2t in ((3.28798, 3.74872, 270, 146), (10, 20, 40, 20), (15, 15, 2, 2), (1, 7, 300, 30), (1e-200, 3e-200, 50, 80),
                        (1e200, 2e200, 12, 6), (5, 5, 5000, 500)):
    put(hd, TT=5, SG=s1, SG2=s2, NN=n1, NN2=n2t, KN1=n1)
    n2 = hd.execute('pv_N2(%d)' % n1)
    worst_df = max(worst_df, abs(hd.execute('pv_DF()') - welch_df(1.0, s2 / s1, n1, n2)) / welch_df(1.0, s2 / s1, n1, n2))
put(hd, TT=5, SG=3.28798, SG2=3.74872, NN=270, NN2=146, KN1=270)
rdf = hd.execute('pv_DF()')
check('H5 pv_DF, test 5 = Welch-Satterthwaite in 7 cases incl. sigma 1E-200 and 1E200 (largest relative difference '
      '%.1e); Roger\'s data: %.3f (SPSS 265.924)' % (worst_df, rdf), worst_df < 1e-12 and abs(rdf - 265.924) < 0.0005)
dfs = []
for tt, kv in ((5, rog), (2, dict(MM0=100, MM1=105, SG=15, NN=30)), (4, dict(PP0=0.5, PP1=0.6, NN=100)),
               (1, dict(MM0=100, MM1=105, SG=15, NN=30))):
    hh = H(PROG)
    pg = draw(hh, TT=5, MM0=4.8185, **kv) if tt == 5 else draw(hh, TT=tt, AL=0.05, TL=2, **kv)
    dfs.append((tt, [t.text for t in pg.texts if re.match(r'^(t\(|z = )', t.text)], (M1 := g(hh, 'M1v') - g(hh, 'M0v')) / g(hh, 'SE0')))
want_t = [(5, ['t(265.9) = 4.35']), (2, ['t(58) = 1.29']), (4, ['z = 1.42']), (1, ['t(29) = 1.83'])]
spss_t = (6.4247 - 4.8185) / math.sqrt(3.28798 ** 2 / 270 + 3.74872 ** 2 / 146)
check('H5 the statistic obtained under POWER, with its df: %s; Roger\'s Welch t %.3f (SPSS -4.351, group 1 minus '
      'group 2); test 2 5/(15 sqrt(2/30)) = %.3f; test 1 5/(15/sqrt 30) = %.3f'
      % ([d[:2] for d in dfs], spss_t, 5 / (15 * math.sqrt(2 / 30)), 5 / (15 / math.sqrt(30))),
      [d[:2] for d in dfs] == want_t and abs(dfs[0][2] - spss_t) < 1e-9 and abs(spss_t - 4.351) < 0.0005, dfs)
ht = H(PROG)
pg = draw(ht, TT=3, PP0=0.5, PP1=0.6, NN=100, AL=0.05, TL=2)
check('H5 one proportion: "z = 2.00" = 0.1/sqrt(0.25/100), no df', 'z = 2.00' in pg.lines(), pg.lines())

# ===================================================================== D. layout
print('=== D. layout (text_overlap_v1 recorder over every screen above)')
rep = OV.report()


def firm_set(f):
    out = set()
    for c in f['collisions']:
        if c['severity'] == 'overlap' and c['firm']:
            out.add(('overlap', c['a'], c['b']))
    for x in f['straddles']:
        if x['firm']:
            out.add(('straddle', x['text'], x['edge']))
    for x in f['overruns']:
        if x['firm']:
            out.add(('overrun', x['text']))
    return out


tags = list(rep)
tn = [t for t in tags if '2.5k' in t]
to = [t for t in tags if '2.5f' in t]
fn = firm_set(rep[tn[0]]) if tn else set()
fo = firm_set(rep[to[0]]) if to else set()
print('   screens recorded: ' + ', '.join('%s %d distinct / %d' % (t, rep[t]['screens_distinct'], rep[t]['screens_total'])
                                       for t in tags))
print('   firm findings: v2.5f %d, v2.5k %d' % (len(fo), len(fn)))
for x in sorted(fo):
    print('     v2.5f (and v2.5g where shared): ' + str(x)[:150])
newf = sorted(fn - fo)
check('D1 v2.5k has no firm overlap, straddle or overrun that v2.5f does not have (new: %d; screens of v2.5k '
      'recorded: %s)' % (len(newf), tn), bool(tn) and bool(to) and not newf, newf[:6])

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for f in FAIL:
    print('  FAILED: ' + f)
sys.exit(1 if FAIL else 0)
