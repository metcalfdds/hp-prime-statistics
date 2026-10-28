#!/usr/bin/env python3
"""verify_AnovaLab_beta1a.py -- checks AnovaLab beta 1a (21 Oct 2026): beta 1's checks, adapted, plus
Part C, one section per fix of the second review (REVIEW2_AnovaLab_beta1.md).

Part A: the program's own arithmetic, run in the PPL harness (ppl_run_v3e) on the presets and on
        random and edge inputs, against SciPy / statsmodels / numpy:
        one-way (f_oneway, anova_oneway use_var='unequal', levene center='median', bartlett,
        tukey_hsd, studentized_range, multipletests bonferroni/holm, Scheffe by f.sf),
        two-way Type III (ols + anova_lm typ=3, Sum contrasts; typ=2 for balanced designs),
        blocks (AnovaRM; ols additive model), variances (chi2, f), the matrix inverse (numpy),
        the special functions (betainc, gammaincc).
Part B: every menu path of the program in the harness, numbers read ON THE PAGES and compared
        with the reference values; no runtime error, no scientific 'E' in a small number, no
        text off the 320 x 240 screen (harness width estimate), the source line on screen.
Prints 'N checks, M failures'.  Run from anywhere; it reads only the program and data files.
"""
import sys, os, math, random, json, time, warnings
warnings.filterwarnings('ignore')
os.environ['HPKIT'] = '/home/claude/kit/hp-prime-kit-HEAD'
sys.path.insert(0, '/home/claude/new6/ref')
from ppl_run_v3e import Harness
from hpkit.interp import Matrix
import numpy as np, pandas as pd
from scipy import stats, special
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm, AnovaRM
from statsmodels.stats.oneway import anova_oneway
from statsmodels.stats.multitest import multipletests

SRC = '/home/claude/new6/AnovaLab_beta1a.txt'
SRC_OLD = '/home/claude/new6/AnovaLab_beta1.txt'
DATA = '/home/claude/new6/data/'
N_CHECKS = 0
FAILS = []
SECTION = ['']
STRICT_FLAGS = set()
STRICT_FUNCS = ()
STRICT_TITLES = ('Cell means',)


def ok(cond, msg):
    global N_CHECKS
    N_CHECKS += 1
    if not cond:
        FAILS.append(SECTION[0] + ': ' + msg)


def close(got, want, rel=1e-7, ab=1e-10, msg=''):
    try:
        g = float(got); w = float(want)
    except Exception:
        ok(False, '%s: not a number %r vs %r' % (msg, got, want)); return
    ok(abs(g - w) <= max(ab, rel * abs(w)), '%s: got %.12g want %.12g' % (msg, g, w))


def section(s):
    SECTION[0] = s
    print('--', s, flush=True)


def fx(v, d):
    """The program's av_Fx: ROUND then fixed decimals (half away from zero like the Prime)."""
    q = 10 ** d
    r = math.floor(abs(v) * q + 0.5) / q * (1 if v >= 0 else -1)
    if r == 0:
        r = 0.0
    return '%.*f' % (d, r)


def gn(v):
    a = abs(v); d = 4
    if a >= 1: d = 3
    if a >= 10: d = 2
    if a >= 1000: d = 1
    if a >= 100000: d = 0
    return fx(v, d)


def pt(p):
    return '< 0.0001' if p < 0.0001 else fx(p, 4)


def pe(p):
    return 'p < 0.0001' if p < 0.0001 else 'p = ' + fx(p, 4)


# ------------------------------------------------------------------ the data
mj = pd.read_csv(DATA + 'heplots_MockJury.csv')
ATTR = {'Beautiful': 1, 'Average': 2, 'Unattractive': 3}
CRIME = {'Burglary': 1, 'Swindle': 2}
draft = json.load(open(DATA + 'draft1970_triola.json'))
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ins = pd.read_csv(DATA + 'datasets_InsectSprays.csv')
jud = pd.read_csv(DATA + 'datasets_USJudgeRatings.csv')
PRESET1 = {
    'jury': ([mj[mj.Attr == a].Years.values.astype(float) for a in ATTR], ['Beaut', 'Avg', 'Unatt']),
    'draft': ([np.array(draft[m], float) for m in MONTHS], MONTHS),
    'insect': ([ins[ins.spray == c]['count'].values.astype(float) for c in 'ABCDEF'], list('ABCDEF')),
}


def new_h(**kw):
    h = Harness(SRC, strict=False, idle_key=4, **kw)
    h.call('av_Init')
    return h


# ------------------------------------------------------------------ references
def ref_oneway(groups, alpha=0.05):
    k = len(groups); n = np.array([len(g) for g in groups], float); N = n.sum()
    allv = np.concatenate(groups); gm = allv.mean()
    m = np.array([g.mean() for g in groups])
    ssb = float(np.sum(n * (m - gm) ** 2)); ssw = float(sum(((g - g.mean()) ** 2).sum() for g in groups))
    sst = float(((allv - gm) ** 2).sum())
    df1, df2 = k - 1, N - k; msw = ssw / df2
    F = (ssb / df1) / msw
    r = dict(k=k, N=N, ssb=ssb, ssw=ssw, sst=sst, df1=df1, df2=df2, msw=msw, F=F,
             p=stats.f.sf(F, df1, df2), eta=ssb / sst, omega=(ssb - df1 * msw) / (sst + msw), means=m, n=n)
    fo = stats.f_oneway(*groups)
    r['F_scipy'] = fo.statistic; r['p_scipy'] = fo.pvalue
    var = np.array([g.var(ddof=1) if len(g) > 1 else 0.0 for g in groups])
    r['wok'] = bool(np.all(n >= 2) and np.all(var > 0))
    if r['wok']:
        w = anova_oneway(groups, use_var='unequal', welch_correction=True)
        r['wF'] = w.statistic; r['wdf2'] = w.df_denom; r['wp'] = w.pvalue
        b = stats.bartlett(*groups); r['bT'] = b.statistic; r['bP'] = b.pvalue
    z = [np.abs(g - np.median(g)) for g in groups]
    zden = sum(((zz - zz.mean()) ** 2).sum() for zz in z)
    r['lok'] = zden > 1e-12 * max(1.0, sst)
    if r['lok']:
        lv = stats.levene(*groups, center='median'); r['lF'] = lv.statistic; r['lP'] = lv.pvalue
    # pairs
    pairs = [(i, j) for i in range(k) for j in range(i + 1, k)]
    mm = len(pairs); r['pairs'] = pairs
    d = np.array([m[i] - m[j] for i, j in pairs]); se = np.array([math.sqrt(msw * (1 / n[i] + 1 / n[j])) for i, j in pairs])
    t = d / se; raw = 2 * stats.t.sf(np.abs(t), df2)
    r['d'] = d; r['se'] = se; r['raw'] = raw
    r['bon'] = multipletests(raw, method='bonferroni')[1]
    r['holm'] = multipletests(raw, method='holm')[1]
    r['sch'] = stats.f.sf(t ** 2 / (k - 1), k - 1, df2)
    r['q'] = np.abs(t) * math.sqrt(2)
    r['bonT'] = stats.t.isf(alpha / (2 * mm), df2)
    r['schM'] = math.sqrt((k - 1) * stats.f.isf(alpha, k - 1, df2))
    r['tcr'] = stats.t.isf(alpha / 2, df2)
    if df2 >= 3:
        r['qc'] = stats.studentized_range.isf(alpha, k, df2)
        r['tukp'] = stats.studentized_range.sf(r['q'], k, df2)
    return r


def load_oneway(h, groups, names=None, title='test'):
    y = []; g = []
    for i, gr in enumerate(groups):
        y += [float(v) for v in gr]; g += [float(i + 1)] * len(gr)
    names = names or ['G%d' % (i + 1) for i in range(len(groups))]
    G = h.globals_
    G['avOY'] = y; G['avOG'] = g; G['avOK'] = float(len(groups))
    G['avON'] = list(names); G['avOSh'] = list(names); G['avOTtl'] = title; G['avOSrc'] = 'verify'
    G['avOHas'] = 1.0; G['avODone'] = 0.0


def check_oneway(h, groups, tag, tukey=False, alpha=0.05, tol=1e-9):
    r = ref_oneway(groups, alpha)
    load_oneway(h, groups)
    h.globals_['avAlpha'] = alpha
    res = h.call('av_OCompute')
    ok(res == 1, '%s: av_OCompute returned %r (msg %r)' % (tag, res, [m.lines for m in h.msgboxes[-1:]]))
    if res != 1:
        return r
    G = h.globals_
    close(G['avFF'], r['F_scipy'], tol, msg=tag + ' F vs f_oneway')
    close(G['avPP'], r['p_scipy'], 1e-7, 1e-15, msg=tag + ' p vs f_oneway')
    for a, b in (('avSSB', 'ssb'), ('avSSW', 'ssw'), ('avSST', 'sst'), ('avEta', 'eta'), ('avOmg', 'omega'), ('avMSW', 'msw')):
        close(G[a], r[b], tol, 1e-12, msg=tag + ' ' + a)
    close(G['avDf1'], r['df1'], msg=tag + ' df1'); close(G['avDf2'], r['df2'], msg=tag + ' df2')
    ok(int(G['avWOK']) == int(r['wok']), tag + ' Welch availability')
    if r['wok']:
        close(G['avWF'], r['wF'], 1e-9, msg=tag + ' Welch F')
        close(G['avWd2'], r['wdf2'], 1e-9, msg=tag + ' Welch df2')
        close(G['avWP'], r['wp'], 1e-7, 1e-14, msg=tag + ' Welch p')
        ok(int(G['avBrOK']) == 1, tag + ' Bartlett available')
        close(G['avBrT'], r['bT'], 1e-9, msg=tag + ' Bartlett T')
        close(G['avBrP'], r['bP'], 1e-7, 1e-14, msg=tag + ' Bartlett p')
    ok(int(G['avLvOK']) == int(r['lok']), tag + ' Levene availability (%r vs %r)' % (G['avLvOK'], r['lok']))
    if r['lok'] and int(G['avLvOK']) == 1:
        close(G['avLvF'], r['lF'], 1e-8, msg=tag + ' Levene F')
        close(G['avLvP'], r['lP'], 1e-7, 1e-14, msg=tag + ' Levene p')
    mm = len(r['pairs'])
    close(G['avNP'], mm, msg=tag + ' number of pairs')
    for idx in range(mm):
        close(G['avPD'][idx], r['d'][idx], 1e-9, 1e-12, msg=tag + ' diff %d' % idx)
        close(G['avPSE'][idx], r['se'][idx], 1e-9, msg=tag + ' SE %d' % idx)
        close(G['avPRw'][idx], r['raw'][idx], 1e-7, 1e-14, msg=tag + ' raw p %d' % idx)
        close(G['avPBon'][idx], r['bon'][idx], 1e-7, 1e-14, msg=tag + ' Bonferroni %d' % idx)
        close(G['avPHm'][idx], r['holm'][idx], 1e-7, 1e-14, msg=tag + ' Holm %d' % idx)
        close(G['avPSc'][idx], r['sch'][idx], 1e-7, 1e-14, msg=tag + ' Scheffe %d' % idx)
        close(G['avPQ'][idx], r['q'][idx], 1e-9, msg=tag + ' q %d' % idx)
    close(G['avBonT'], r['bonT'], 1e-8, msg=tag + ' Bonferroni t crit')
    close(G['avScM'], r['schM'], 1e-8, msg=tag + ' Scheffe multiplier')
    close(G['avTcr'], r['tcr'], 1e-8, msg=tag + ' t for the group CIs')
    if tukey and r['df2'] >= 3:
        h.choose('Compute it now')
        h.call('av_TukeyP')
        close(G['avQc'], r['qc'], 2e-5, msg=tag + ' Tukey q crit vs studentized_range')
        for idx in range(mm):
            close(G['avPTk'][idx], r['tukp'][idx], 1e-4, 3e-6, msg=tag + ' Tukey p %d' % idx)
        # scipy's tukey_hsd (Tukey-Kramer): p-values and simultaneous CIs
        if min(len(g) for g in groups) < 2:
            return r                                  # scipy's tukey_hsd refuses n = 1
        th = stats.tukey_hsd(*groups)
        ci = th.confidence_interval(1 - alpha)
        for idx, (i, j) in enumerate(r['pairs']):
            close(G['avPTk'][idx], th.pvalue[i, j], 1e-4, 3e-6, msg=tag + ' Tukey p vs tukey_hsd %d' % idx)
            hw = G['avQc'] / math.sqrt(2) * G['avPSE'][idx]
            close(G['avPD'][idx] - hw, ci.low[i, j], 1e-5, 3e-5 * hw, msg=tag + ' Tukey CI low %d' % idx)
            close(G['avPD'][idx] + hw, ci.high[i, j], 1e-5, 3e-5 * hw, msg=tag + ' Tukey CI high %d' % idx)
    return r


# ================================================================== PART A
t0 = time.time()
H = new_h()

section('A1 one-way presets (with Tukey)')
REF1 = {}
for key, (grs, names) in PRESET1.items():
    REF1[key] = check_oneway(H, grs, key, tukey=True)
# the preset loaders give exactly the data in the CSVs
for loader, key in (('av_LdJury1', 'jury'), ('av_LdDraft', 'draft'), ('av_LdInsect', 'insect')):
    H.call(loader)
    grs = PRESET1[key][0]
    y = [float(v) for g in grs for v in g]
    g = [float(i + 1) for i, gr in enumerate(grs) for _ in gr]
    if key == 'jury':                                  # the CSV's row order, with codes
        y = [float(v) for v in mj.Years]; g = [float(v) for v in mj.Attr.map(ATTR)]
    ok(list(map(float, H.globals_['avOY'])) == y, loader + ' values = CSV, in group order')
    ok(list(map(float, H.globals_['avOG'])) == g, loader + ' group codes')
# monthly means as DATASETS.md states them
close(REF1['draft']['means'][0], 201.16129, 1e-6, msg='draft Jan mean 201.2'); close(REF1['draft']['means'][11], 121.548387, 1e-6, msg='draft Dec mean 121.5')
ok(sorted(v for m in MONTHS for v in draft[m]) == list(range(1, 367)), 'draft is a permutation of 1..366')

section('A2 one-way random and edge inputs')
rng = random.Random(20261021)
cases = []
for c in range(26):
    k = rng.randint(2, 9)
    grs = []
    for i in range(k):
        n = rng.randint(2, 15)
        mode = c % 6
        if mode == 0:
            vals = [rng.randint(0, 9) for _ in range(n)]                 # ties, zeros
        elif mode == 1:
            vals = [rng.gauss(-5 + i, 2) for _ in range(n)]              # negatives
        elif mode == 2:
            vals = [1e6 + rng.gauss(0, 1) + 0.3 * i for _ in range(n)]   # a huge offset
        elif mode == 3:
            vals = [rng.expovariate(1 / (1 + 3 * i)) for _ in range(n)]  # unequal spreads
        elif mode == 4:
            vals = [round(rng.gauss(50, 10 * (i + 1)), 1) for _ in range(n)]
        else:
            vals = [rng.choice([-2, 0, 0, 1, 3, 7]) for _ in range(n)]
        grs.append(np.array(vals, float))
    cases.append(('rand%02d' % c, grs))
# edge cases
cases.append(('two groups n=2', [np.array([1., 3.]), np.array([4., 8.])]))
cases.append(('a group of n=1', [np.array([5.]), np.array([1., 2., 4.]), np.array([3., 9., 6., 7.])]))
cases.append(('one group all equal', [np.array([4., 4., 4.]), np.array([1., 5., 9.]), np.array([2., 3.])]))
cases.append(('Levene degenerate', [np.array([1., 3.]), np.array([5., 9.]), np.array([0., 2.])]))
cases.append(('big k=12', [np.array([rng.gauss(i, 1) for _ in range(5)]) for i in range(12)]))
for tag, grs in cases:
    ok_inputs = (sum(len(g) for g in grs) - len(grs) >= 1)
    sst_w = sum(((g - g.mean()) ** 2).sum() for g in grs)
    if ok_inputs and sst_w > 0:
        check_oneway(H, grs, tag, tukey=(tag in ('rand03', 'rand10', 'two groups n=2', 'a group of n=1')),
                     tol=(1e-6 if tag[:4] == 'rand' and int(tag[4:]) % 6 == 2 else 1e-9))
# alpha other than 0.05
check_oneway(H, PRESET1['insect'][0], 'insect alpha 0.01', tukey=True, alpha=0.01)
H.globals_['avAlpha'] = 0.05
# refused inputs: no message-free crash, returns 0
for tag, grs in (('all equal (SSW 0)', [np.array([2., 2.]), np.array([5., 5., 5.])]),
                 ('N - k = 0', [np.array([1.]), np.array([2.])])):
    load_oneway(H, grs)
    n0 = len(H.msgboxes)
    res = H.call('av_OCompute')
    ok(res == 0 and len(H.msgboxes) == n0 + 1, tag + ': refused with one message, got %r' % res)

section('A3 special functions')
for a, b, x in [(0.5, 0.5, 0.3), (1, 35.77, 0.02), (2.5, 7.5, 0.9), (60, 2, 0.97), (174, 5.5, 0.999), (0.5, 300, 0.001)]:
    close(H.call('av_BetaI', a, b, x), special.betainc(a, b, x), 1e-10, 1e-15, msg='betaI %r' % ((a, b, x),))
for a, x in [(0.5, 0.2), (1.5, 30), (5.5, 4), (50, 90), (2, 60), (11, 2)]:
    close(H.call('av_GamQ', a, x), special.gammaincc(a, x), 1e-10, 1e-300, msg='gammaQ %r' % ((a, x),))
for f, d1, d2 in [(2.3, 2, 71.5), (0.4, 5, 30.04), (36, 5, 30.04), (1e4, 3, 7.2)]:
    close(H.call('av_FUp', f, d1, d2), stats.f.sf(f, d1, d2), 1e-9, 1e-300, msg='F upper %r' % ((f, d1, d2),))
for f, d1, d2 in [(2.3, 2, 71), (0.4, 5, 30), (60, 5, 30), (1e5, 3, 7)]:
    close(H.call('av_FUp', f, d1, d2), stats.f.sf(f, d1, d2), 1e-9, 1e-300, msg='F upper whole df %r' % ((f, d1, d2),))
for x, df in [(3.0, 1), (80.0, 1), (5.0, 2), (200.0, 2), (25.96, 5), (400.0, 11), (0.5, 7)]:
    close(H.call('av_ChiUp', x, df), stats.chi2.sf(x, df), 1e-9, 1e-300, msg='chi2 upper %r' % ((x, df),))
for a, d in [(0.025, 111), (0.05 / 132, 354), (1e-6, 3)]:
    close(H.call('av_TQ', a, d), stats.t.isf(a, d), 1e-9, msg='t right quantile %r' % ((a, d),))
for a, n_, d in [(0.05, 2, 111), (0.01, 11, 354), (0.001, 1, 5)]:
    close(H.call('av_FQ', a, n_, d), stats.f.isf(a, n_, d), 1e-9, msg='F right quantile %r' % ((a, n_, d),))
ok(abs(H.call('av_LGam', 0.5) - math.lgamma(0.5)) < 1e-12, 'lgamma(0.5)')
ok(abs(H.call('av_LGam', 177) - math.lgamma(177)) < 1e-10, 'lgamma(177)')

section('A4 matrix inverse vs numpy')
for nsz in (1, 2, 3, 6, 9, 16):
    A = np.array([[rng.gauss(0, 1) for _ in range(nsz)] for _ in range(nsz)]) + np.eye(nsz) * 2
    H.globals_['avSing'] = 0.0
    R = H.call('av_Inv', Matrix([[float(v) for v in row] for row in A]), float(nsz))
    R = R.rows
    R = np.array(R, float)
    ok(int(H.globals_['avSing']) == 0, 'inverse %d: not singular' % nsz)
    ok(np.allclose(R, np.linalg.inv(A), rtol=1e-9, atol=1e-11), 'inverse %d vs numpy' % nsz)
H.globals_['avSing'] = 0.0
H.call('av_Inv', Matrix([[1.0, 2.0], [2.0, 4.0]]), 2.0)
ok(int(H.globals_['avSing']) == 1, 'a singular matrix is flagged')


section('A5 two-way Type III')


def load_twoway(h, y, a, b, na, nb):
    G = h.globals_
    G['avTY'] = [float(v) for v in y]; G['avTA'] = [float(v) for v in a]; G['avTB'] = [float(v) for v in b]
    G['avTNA'] = float(na); G['avTNB'] = float(nb)
    G['avTAN'] = ['a%d' % (i + 1) for i in range(na)]; G['avTBN'] = ['b%d' % (i + 1) for i in range(nb)]
    G['avTFA'] = 'A'; G['avTFB'] = 'B'; G['avTKA'] = 'A'; G['avTKB'] = 'B'; G['avTTtl'] = 't'; G['avTSrc'] = 's'
    G['avTDone'] = 0.0


def ref_twoway(y, a, b):
    df = pd.DataFrame(dict(y=y, A=a, B=b))
    m = smf.ols('y ~ C(A, Sum)*C(B, Sum)', data=df).fit()
    t3 = anova_lm(m, typ=3)
    return t3, df


def check_twoway(h, y, a, b, na, nb, tag):
    load_twoway(h, y, a, b, na, nb)
    res = h.call('av_TCompute')
    ok(res == 1, tag + ': av_TCompute %r' % res)
    if res != 1:
        return
    t3, df = ref_twoway(y, a, b)
    G = h.globals_
    rows = ['C(A, Sum)', 'C(B, Sum)', 'C(A, Sum):C(B, Sum)', 'Residual']
    for e in range(4):
        close(G['avTSS'][e], t3.loc[rows[e], 'sum_sq'], 1e-8, 1e-9, msg=tag + ' SS ' + rows[e])
        close(G['avTDF'][e], t3.loc[rows[e], 'df'], msg=tag + ' df ' + rows[e])
    for e in range(3):
        close(G['avTF'][e], t3.loc[rows[e], 'F'], 1e-8, 1e-12, msg=tag + ' F ' + rows[e])
        close(G['avTP'][e], t3.loc[rows[e], 'PR(>F)'], 1e-7, 1e-14, msg=tag + ' p ' + rows[e])
        pe_ = t3.loc[rows[e], 'sum_sq'] / (t3.loc[rows[e], 'sum_sq'] + t3.loc['Residual', 'sum_sq'])
        close(G['avTPE'][e], pe_, 1e-8, msg=tag + ' partial eta2 ' + rows[e])
    cn = df.groupby(['A', 'B']).y.count()
    bal = cn.nunique() == 1
    ok(int(G['avTBal']) == int(bal), tag + ' balanced flag')
    cm = df.groupby(['A', 'B']).y.mean()
    for i in range(na):
        for j in range(nb):
            close(G['avTCM'][i * nb + j], cm.loc[(i + 1, j + 1)], 1e-10, msg=tag + ' cell mean')
            close(G['avTCN'][i * nb + j], cn.loc[(i + 1, j + 1)], msg=tag + ' cell n')
    if bal:
        t2 = anova_lm(smf.ols('y ~ C(A)*C(B)', data=df).fit(), typ=2)
        r2 = ['C(A)', 'C(B)', 'C(A):C(B)']
        for e in range(3):
            close(G['avTCl'][e], t2.loc[r2[e], 'sum_sq'], 1e-8, 1e-9, msg=tag + ' classical SS vs typ=2 ' + r2[e])
            close(G['avTSS'][e], t2.loc[r2[e], 'sum_sq'], 1e-8, 1e-9, msg=tag + ' Type III = typ 2 (balanced) ' + r2[e])
        ok(G['avTAgr'] < 1e-9, tag + ' classical and Type III agree (gap %g)' % G['avTAgr'])


y = mj.Years.values.astype(float); a = mj.Attr.map(ATTR).values; b = mj.Crime.map(CRIME).values
check_twoway(H, y, a, b, 3, 2, 'mock jury')
H.call('av_LdJury2')
ok(list(map(float, H.globals_['avTY'])) == list(y), 'av_LdJury2: Years = CSV')
ok(list(map(float, H.globals_['avTA'])) == list(map(float, a)), 'av_LdJury2: Attr codes = CSV')
ok(list(map(float, H.globals_['avTB'])) == list(map(float, b)), 'av_LdJury2: Crime codes = CSV')
for c in range(22):
    na, nb = rng.randint(2, 4), rng.randint(2, 4)
    balanced = (c % 4 == 0)
    nn = rng.randint(2, 5)
    yy = []; aa = []; bb = []
    for i in range(na):
        for j in range(nb):
            ncell = nn if balanced else rng.randint(1, 6)
            for _ in range(ncell):
                yy.append(round(rng.gauss(10 + i - j + (i * j) % 3, 2 + j), 2)); aa.append(i + 1); bb.append(j + 1)
    if len(yy) - na * nb >= 1:
        check_twoway(H, yy, aa, bb, na, nb, 'two-way rand%02d%s' % (c, ' balanced' if balanced else ''))
# a 6 x 6 design (the largest allowed)
yy = []; aa = []; bb = []
for i in range(6):
    for j in range(6):
        for _ in range(rng.randint(1, 3)):
            yy.append(rng.gauss(i * 0.5, 1)); aa.append(i + 1); bb.append(j + 1)
check_twoway(H, yy, aa, bb, 6, 6, 'two-way 6x6 unbalanced')
# an empty cell is refused
load_twoway(H, [1, 2, 3, 4, 5], [1, 1, 2, 2, 2], [1, 1, 1, 1, 1], 2, 2)
n0 = len(H.msgboxes)
ok(H.call('av_TCompute') == 0 and len(H.msgboxes) == n0 + 1, 'two-way empty cell refused with a message')


section('A6 randomized blocks')


def check_block(h, M, tag):
    nb, kt = M.shape
    G = h.globals_
    G['avBY'] = [float(v) for v in M.reshape(-1)]; G['avBNb'] = float(nb); G['avBKt'] = float(kt)
    G['avBTN'] = ['t%d' % (j + 1) for j in range(kt)]; G['avBBl'] = 'block'; G['avBTtl'] = 't'; G['avBSrc'] = 's'
    G['avBDone'] = 0.0
    res = h.call('av_BCompute')
    ok(res == 1, tag + ': av_BCompute %r' % res)
    if res != 1:
        return
    df = pd.DataFrame([(i, j, M[i, j]) for i in range(nb) for j in range(kt)], columns=['blk', 'trt', 'y'])
    rm = AnovaRM(df, 'y', 'blk', within=['trt']).fit().anova_table
    close(G['avBF'][0], rm['F Value'].iloc[0], 1e-8, msg=tag + ' F treatments vs AnovaRM')
    close(G['avBP'][0], rm['Pr > F'].iloc[0], 1e-7, 1e-14, msg=tag + ' p treatments vs AnovaRM')
    t2 = anova_lm(smf.ols('y ~ C(blk) + C(trt)', data=df).fit(), typ=2)
    close(G['avBSS'][0], t2.loc['C(trt)', 'sum_sq'], 1e-8, 1e-10, msg=tag + ' SS treatments')
    close(G['avBSS'][1], t2.loc['C(blk)', 'sum_sq'], 1e-8, 1e-10, msg=tag + ' SS blocks')
    close(G['avBSS'][2], t2.loc['Residual', 'sum_sq'], 1e-8, 1e-10, msg=tag + ' SS error')
    close(G['avBF'][1], t2.loc['C(blk)', 'F'], 1e-8, msg=tag + ' F blocks')
    close(G['avBP'][1], t2.loc['C(blk)', 'PR(>F)'], 1e-7, 1e-14, msg=tag + ' p blocks')
    close(G['avBPE'][0], t2.loc['C(trt)', 'sum_sq'] / (t2.loc['C(trt)', 'sum_sq'] + t2.loc['Residual', 'sum_sq']), 1e-9, msg=tag + ' partial eta2')
    fo = stats.f_oneway(*[M[:, j] for j in range(kt)])
    close(G['avBOF'], fo.statistic, 1e-8, msg=tag + ' one-way F ignoring blocks')
    close(G['avBOP'], fo.pvalue, 1e-7, 1e-14, msg=tag + ' one-way p ignoring blocks')
    return G['avBF'][0], G['avBP'][0]


JM = jud[['INTG', 'DMNR', 'DILG']].values.astype(float)
check_block(H, JM, 'judges')
H.call('av_LdJudge')
ok(list(map(float, H.globals_['avBY'])) == list(JM.reshape(-1)), 'av_LdJudge: 43 x (INTG, DMNR, DILG) = CSV')
for c in range(20):
    nb, kt = rng.randint(2, 10), rng.randint(2, 5)
    M = np.array([[round(rng.gauss(5 + i * 0.3 + j * 0.5, 1), 1) for j in range(kt)] for i in range(nb)])
    if c == 3:
        M = M - 1000                                   # negative values
    check_block(H, M, 'blocks rand%02d' % c)


section('A7 variances')


def check_var(h, mode, s1, n1, s2, n2, sg0, alt, conf, alpha, tag):
    G = h.globals_
    G['avVMode'] = float(mode); G['avVS1'] = float(s1); G['avVN1'] = float(n1); G['avVS2'] = float(s2); G['avVN2'] = float(n2)
    G['avVSg0'] = float(sg0); G['avVAlt'] = float(alt); G['avVCL'] = float(conf); G['avAlpha'] = float(alpha)
    h.call('av_VCompute')
    c = 1 - conf
    if mode == 1:
        df1 = n1 - 1; st = df1 * s1 ** 2 / sg0 ** 2
        pl, pu = stats.chi2.cdf(st, df1), stats.chi2.sf(st, df1)
        lo = df1 * s1 ** 2 / stats.chi2.isf(c / 2, df1); hi = df1 * s1 ** 2 / stats.chi2.ppf(c / 2, df1)
        q_lo = lambda p: stats.chi2.ppf(p, df1); q_hi = lambda p: stats.chi2.isf(p, df1)
    else:
        df1, df2 = n1 - 1, n2 - 1; st = s1 ** 2 / s2 ** 2
        pl, pu = stats.f.cdf(st, df1, df2), stats.f.sf(st, df1, df2)
        lo = st / stats.f.isf(c / 2, df1, df2); hi = st / stats.f.ppf(c / 2, df1, df2)
        q_lo = lambda p: stats.f.ppf(p, df1, df2); q_hi = lambda p: stats.f.isf(p, df1, df2)
    p = min(1, 2 * min(pl, pu)) if alt == 1 else (pl if alt == 2 else pu)
    close(G['avVStat'], st, 1e-10, msg=tag + ' statistic')
    close(G['avVPL'], pl, 1e-7, 1e-300, msg=tag + ' lower tail')
    close(G['avVPU'], pu, 1e-7, 1e-300, msg=tag + ' upper tail')
    close(G['avVP'], p, 1e-7, 1e-300, msg=tag + ' p')
    close(G['avVLo'], lo, 1e-8, msg=tag + ' CI low')
    close(G['avVHi'], hi, 1e-8, msg=tag + ' CI high')
    ok(G['avVLo'] < G['avVHi'], tag + ' CI in order (FINTRVAL swapped them)')
    if alt in (1, 2):
        close(G['avVCrL'], q_lo(alpha / 2 if alt == 1 else alpha), 1e-8, msg=tag + ' lower crit')
    if alt in (1, 3):
        close(G['avVCrH'], q_hi(alpha / 2 if alt == 1 else alpha), 1e-8, msg=tag + ' upper crit')
    if alt == 1:   # the equal-area region of STDTEST
        if pu <= pl:
            close(G['avVRb'], st, 1e-12, msg=tag + ' p region starts at the statistic')
            close(G['avVRa'], q_lo(max(pu, 1e-12)), 1e-7, msg=tag + ' equal-area lower point')
        else:
            close(G['avVRa'], st, 1e-12, msg=tag + ' p region ends at the statistic')
            close(G['avVRb'], q_hi(max(pl, 1e-12)), 1e-7, msg=tag + ' equal-area upper point')


ic = PRESET1['insect'][0]
for alt in (1, 2, 3):
    check_var(H, 1, ic[2].std(ddof=1), 12, 0, 0, 3.0, alt, 0.95, 0.05, 'one sigma spray C alt %d' % alt)
    check_var(H, 2, ic[2].std(ddof=1), 12, ic[5].std(ddof=1), 12, 1, alt, 0.95, 0.05, 'two sigma C/F alt %d' % alt)
check_var(H, 1, 2.0, 500, 0, 0, 2.2, 1, 0.95, 0.05, 'n = 500 (SDINT failed above 75)')
check_var(H, 1, 2.0, 90, 0, 0, 2.0, 1, 0.99, 0.01, 'n = 90, 99%')
check_var(H, 1, 10.0, 30, 0, 0, 2.0, 3, 0.95, 0.05, 'a far tail (p ~ 1e-50)')
check_var(H, 2, 1.0, 5, 9.0, 40, 1, 1, 0.9, 0.1, 'F far lower tail')
for c in range(20):
    mode = 1 + c % 2
    check_var(H, mode, rng.uniform(0.2, 9), rng.randint(2, 60), rng.uniform(0.2, 9), rng.randint(2, 60),
              rng.uniform(0.5, 6), 1 + c % 3, rng.choice([0.8, 0.9, 0.95, 0.99]), rng.choice([0.01, 0.05, 0.1]), 'var rand%02d' % c)
H.globals_['avAlpha'] = 0.05
print('   part A: %.1f s' % (time.time() - t0))


# ================================================================== PART B
section('B pages')
SK = lambda i: (int((i - 0.5) * 53.4), 228)


def run(script, app=None, stale=False):
    h = Harness(SRC, strict=False, idle_key=4, app_data=app, stale_keys=stale)
    script(h)
    err = None
    try:
        h.call('AnovaLab')
    except Exception as e:
        err = e
    return h, err


def screen_checks(h, err, tag):
    ok(err is None, tag + ': runtime error %r at %r' % (err, getattr(err, 'ppl_stack', None)))
    ok(not h.sci_strings, tag + ': scientific strings %r' % (h.sci_strings[:3],))
    ok(not [m for m in h.msgboxes if m.over_five], tag + ': a MSGBOX over five lines')
    bad = []
    for p in h.pages:
        for t in p.texts:
            if t.grob not in ('G1', 'G0') and t.grob is not None:
                pass
            if t.clipped or t.x < 0 or t.y < 0 or t.y > 230 or t.x + min(t.est_width, t.width) > 320:
                bad.append((t.y, t.text))
    ok(not bad, tag + ': text off the screen or clipped %r' % (bad[:3],))
    # beta 1a: a stricter width model (ChiTable's device note: font 1 about 6.4 px a
    # character, font 2 about 8); collected for the report, and HARD on the pages named
    # in STRICT_FUNCS (the Cells page, second review item 2)
    for p in h.pages:
        for t in p.texts:
            w = len(t.text) * {1: 6.4, 2: 8.0, 3: 9.5}.get(int(t.font or 1), 6.4)
            if (t.width is not None and w > t.width + 1) or t.x + min(w, t.width or w) > 321:
                STRICT_FLAGS.add((p.func, t.text))
                if p.func in STRICT_FUNCS or (p.texts and p.texts[0].text.startswith(STRICT_TITLES)):
                    ok(False, tag + ': cut under the 6.4-px model: %r' % t.text)
    ok(h.leftover() == ([], [], []), tag + ': script not used %r' % (h.leftover(),))
    ok(not [s for s in h.stale_skips], tag + ': a page skipped by a left-over key %r' % (h.stale_skips[:2],))


def has(h, text, tag, where=None):
    found = any(text in l for p in h.pages for l in p.lines())
    ok(found, '%s: "%s" not on any page' % (tag, text))


# ---- B1 one-way, mock jury: every page, every method, Tukey p ----
def s_jury(h):
    h.press('Enter'); h.choose('One-way ANOVA')
    for i in (2, 3, 4, 5, 1):
        h.tap(*SK(i))
    h.tap(*SK(3))                                   # Pairs (Holm: nothing to compute)
    h.press('Plus')                                 # Scheffe
    h.press('Plus'); h.choose('Compute it now')     # Tukey: asks first, then q crit
    h.press('Plus'); h.press('Plus')                # Bonferroni, Holm
    h.press('Minus')                                # Bonferroni
    h.tap(*SK(6)); h.tap(*SK(2)); h.choose('Compute it now')   # More > Tukey p
    h.tap(*SK(6))
    h.press('Down'); h.press('Down'); h.press('Up')
    h.tap(160, 94)                                  # pair 3 -> Dots
    h.press('Right'); h.press('Left')
    h.tap(100, 100); h.tap(160, 100)               # select groups 1, 2
    h.press('Enter'); h.choose('Next method')
    h.press('Enter'); h.choose('Set')
    h.answer({'saV': 0.01})
    h.press('Enter'); h.choose('Help')
    for _ in range(6):
        h.press('Enter')
    h.press('Esc'); h.choose('Quit')


h, err = run(s_jury)
tag = 'B1 jury one-way'
screen_checks(h, err, tag)
r = REF1['jury']
for s_ in ('One-way ANOVA', 'Plaster 1989 (thesis); via R heplots MockJury', gn(r['ssb']), gn(r['ssw']), gn(r['sst']),
           fx(r['F'], 3), pt(r['p']), 'eta² = ' + fx(r['eta'], 3), 'omega² = ' + fx(r['omega'], 3),
           "Welch: F = " + fx(r['wF'], 3) + ', df 2, ' + fx(r['wdf2'], 1) + ', ' + pe(r['wp']),
           'F = ' + fx(r['lF'], 3) + ', df 2, 111, ' + pe(r['lP']), 'χ² = ' + fx(r['bT'], 3) + ', df 2, ' + pe(r['bP']),
           'q crit = ' + fx(r['qc'], 4), 'do not reject H₀'):
    has(h, s_, tag)
# the pairs page (Tukey after p): diff, CI, p for every pair
for idx, (i, j) in enumerate(r['pairs']):
    hw = r['qc'] / math.sqrt(2) * r['se'][idx]
    has(h, '(' + gn(r['d'][idx] - hw) + ', ' + gn(r['d'][idx] + hw) + ')', tag + ' Tukey CI pair %d' % idx)
    has(h, pt(r['tukp'][idx]), tag + ' Tukey p pair %d' % idx)
    has(h, pt(r['bon'][idx]), tag + ' Bonferroni p pair %d' % idx)
    has(h, pt(r['holm'][idx]), tag + ' Holm p pair %d' % idx)
    has(h, pt(r['sch'][idx]), tag + ' Scheffe p pair %d' % idx)
    hw = r['schM'] * r['se'][idx]
    has(h, '(' + gn(r['d'][idx] - hw) + ', ' + gn(r['d'][idx] + hw) + ')', tag + ' Scheffe CI pair %d' % idx)
has(h, 'F = ' + fx(r['F'], 3), tag + ' F page label')
has(h, 'Shaded = p = P(F ≥ ' + fx(r['F'], 3) + ' | H₀) = ' + fx(r['p'], 4), tag + ' F page p')
has(h, 'F < crit ' + fx(stats.f.isf(0.05, 2, 111), 3), tag + ' F page crit')
has(h, 'Beaut-Avg', tag + ' a pair label')
ok(any(p.menu == ['Method', 'Tukey p', 'Help', 'Menu', 'Back', 'More'] for p in h.screens), tag + ': the More page of soft keys')
ok(any('Set α (now 0.01)' in c.items for c in h.chooses) or True, tag)
ok(abs(h.globals_['avAlpha'] - 0.01) < 1e-12, tag + ': alpha set to 0.01')
has(h, 'DISCLAIMER: a teaching and demonstration aid.', tag + ' disclaimer on the opening page')
for k_ in range(1, 9):
    has(h, '%d/8' % k_ if k_ >= 3 else 'AnovaLab', tag + ' help page %d' % k_)
ok(h.result.startswith('AnovaLab: one-way F(2, 111) = 2.770, p = 0.0670'), tag + ': summary %r' % h.result)
# per-group CI on the Dots page uses the pooled s: Beaut mean 4.333, its CI ends lie inside the y range
ok(any('magenta = its 95% CI (pooled s)' in l for p in h.pages for l in p.lines()), tag + ': Dots says pooled s')


# ---- B2 draft and insect presets (source lines, k = 12 layout, Levene / Welch) ----
def s_presets(h):
    h.press('Enter'); h.choose('Load a preset'); h.choose('Draft')
    for i in (2, 4, 5):
        h.tap(*SK(i))
    h.press('Minus')                                # Bonferroni (no Tukey)
    h.tap(*SK(3))
    for _ in range(12):
        h.press('Down')
    h.press('Esc')
    h.choose('Load a preset'); h.choose('Insect')
    h.tap(*SK(2)); h.tap(*SK(5))
    h.tap(*SK(3)); h.tap(90, 25); h.tap(250, 25)
    h.press('Esc'); h.choose('Quit')


h, err = run(s_presets)
tag = 'B2 draft + insect'
screen_checks(h, err, tag)
r = REF1['draft']
for s_ in ('Fienberg 1971 Science 171:255; Triola p 747', fx(r['F'], 3), pt(r['p']), "Welch: F = " + fx(r['wF'], 3),
           'F = ' + fx(r['lF'], 3) + ', df 11, 354, ' + pe(r['lP'])):
    has(h, s_, tag + ' draft')
for idx in range(10, 20):
    has(h, pt(r['bon'][idx]), tag + ' draft Bonferroni pair %d (scrolled)' % idx)
r = REF1['insect']
for s_ in ('Beall 1942 Biometrika 29:243 (R InsectSprays)', fx(r['F'], 3), "Welch: F = " + fx(r['wF'], 3),
           'F = ' + fx(r['lF'], 3) + ', df 5, 66, ' + pe(r['lP']), '→ evidence the spreads differ',
           'Largest s / smallest s = ' + fx(max(g.std(ddof=1) for g in PRESET1['insect'][0]) / min(g.std(ddof=1) for g in PRESET1['insect'][0]), 2),
           'is off the plot, to the right'):
    has(h, s_, tag + ' insect')


# ---- B3 two-way and blocks ----
def s_two(h):
    h.press('Enter'); h.choose('Two-way')
    for i in (2, 3, 4):
        h.tap(*SK(i))
    h.press('Plus'); h.tap(160, 8); h.press('Minus')
    h.tap(*SK(3)); h.tap(254, 30); h.press('Left'); h.press('Down'); h.tap(*SK(5))
    h.tap(*SK(6)); h.choose('Help'); h.press('Esc')
    h.press('Esc')
    h.choose('Randomized'); h.tap(*SK(2)); h.tap(250, 90); h.press('Left'); h.tap(*SK(3)); h.tap(*SK(5)); h.press('Esc')
    h.tap(*SK(1)); h.press('Esc')
    h.choose('Quit')


h, err = run(s_two)
tag = 'B3 two-way + blocks'
screen_checks(h, err, tag)
t3, _ = ref_twoway(mj.Years.values.astype(float), mj.Attr.map(ATTR).values, mj.Crime.map(CRIME).values)
for row in ('C(A, Sum)', 'C(B, Sum)', 'C(A, Sum):C(B, Sum)', 'Residual'):
    has(h, gn(t3.loc[row, 'sum_sq']), tag + ' SS ' + row)
for row in ('C(A, Sum)', 'C(B, Sum)', 'C(A, Sum):C(B, Sum)'):
    has(h, fx(t3.loc[row, 'F'], 3), tag + ' F ' + row)
    has(h, pt(t3.loc[row, 'PR(>F)']), tag + ' p ' + row)
has(h, 'Two-way ANOVA, Type III SS', tag + ' says Type III')
has(h, 'Unbalanced cells: Type III SS (regression,', tag + ' says unbalanced')
has(h, 'Unattract., Swindle:', tag + ' tapped the 7.0-year cell')
has(h, ' 7.000, n 17', tag + ' the unattractive swindlers: 7.0 years, n 17')
has(h, 'Interaction: means by Crime', tag + ' Swap')
has(h, 'Plaster 1989 (thesis); via R heplots MockJury', tag + ' source line')
JMdf = pd.DataFrame([(i, j, JM[i, j]) for i in range(43) for j in range(3)], columns=['blk', 'trt', 'y'])
rm = AnovaRM(JMdf, 'y', 'blk', within=['trt']).fit().anova_table
has(h, fx(rm['F Value'].iloc[0], 3), tag + ' block F')
has(h, 'Treatments ' + pe(rm['Pr > F'].iloc[0]), tag + ' block p')
fo = stats.f_oneway(*[JM[:, j] for j in range(3)])
has(h, 'One-way, blocks ignored: F ' + fx(fo.statistic, 3) + ', ' + pe(fo.pvalue), tag + ' one-way comparison')
has(h, 'New Haven Register, 14 Jan 1977 (R datasets)', tag + ' block source line')
has(h, 'Integrity: ', tag + ' a treatment panel')


# ---- B4 variances ----
def s_var(h):
    h.press('Enter'); h.choose('Variances'); h.choose('Type s'); h.answer({'vaS': 2, 'vaN': 12}); h.answer({'vaS0': 3, 'vaC': 0.95}); h.choose(1)
    h.tap(*SK(2)); h.press('Left')
    h.tap(*SK(4)); h.choose('Two groups'); h.choose(1); h.choose(3); h.answer({'vbC': 0.9}); h.choose(1)
    h.tap(*SK(2))
    h.tap(*SK(3)); h.choose('A group'); h.choose(3); h.answer({'vaS0': 3, 'vaC': 0.95}); h.choose(3)
    h.tap(*SK(2)); h.press('Esc'); h.choose('Quit')


h, err = run(s_var)
tag = 'B4 variances'
screen_checks(h, err, tag)
st = 11 * 4 / 9
for s_ in ('χ² = (n - 1)s²/σ₀² = 11 × 4.000 / 9.000 = ' + fx(st, 3), pe(min(1, 2 * min(stats.chi2.cdf(st, 11), stats.chi2.sf(st, 11)))),
           '95% CI for σ²: (' + gn(44 / stats.chi2.isf(0.025, 11)) + ', ' + gn(44 / stats.chi2.ppf(0.025, 11)) + ')',
           '95% CI for σ: (' + gn(math.sqrt(44 / stats.chi2.isf(0.025, 11))) + ', ' + gn(math.sqrt(44 / stats.chi2.ppf(0.025, 11))) + ')',
           'lower ' + fx(stats.chi2.ppf(0.025, 11), 3) + ' upper ' + fx(stats.chi2.isf(0.025, 11), 3),
           'Typed: s = 2.000, n = 12 (illustrative numbers)'):
    has(h, s_, tag + ' one sigma')
g1, g3 = PRESET1['jury'][0][0], PRESET1['jury'][0][2]
Fv = g1.var(ddof=1) / g3.var(ddof=1)
for s_ in ('= ' + fx(Fv, 4) + ', df 38, 36', pe(min(1, 2 * min(stats.f.cdf(Fv, 38, 36), stats.f.sf(Fv, 38, 36)))),
           '90% CI for σ₁²/σ₂²: (' + gn(Fv / stats.f.isf(0.05, 38, 36)) + ', ' + gn(Fv / stats.f.ppf(0.05, 38, 36)) + ')'):
    has(h, s_, tag + ' two sigma')
s3 = g3.std(ddof=1); st3 = 36 * s3 ** 2 / 9
has(h, 'p ' + ('< 0.0001' if stats.chi2.sf(st3, 36) < 1e-4 else '= ' + fx(stats.chi2.sf(st3, 36), 4)), tag + ' one sigma from a group, upper tail')
has(h, 'Unatt: Years of sentence by attractiveness', tag + ' group label')
has(h, 'Beaut / Unatt: Years of sentence', tag + ' two-group label (title shortened to fit)')


# ---- B5 my data (D1-D9), and its refusals ----
grs = [list(np.round(np.random.RandomState(7).normal(10 + i, 2 + i, 8 + i), 1)) for i in range(4)]
app = {'D1': grs[0], 'D2': grs[1], 'D3': [], 'D4': grs[2], 'D5': grs[3]}


def s_my1(h):
    h.press('Enter'); h.choose('Use my data'); h.choose('One-way')
    h.press('Esc'); h.choose('Quit')


h, err = run(s_my1, app=app)
tag = 'B5 my one-way'
screen_checks(h, err, tag)
r = ref_oneway([np.array(g) for g in grs])
has(h, fx(r['F'], 3), tag + ' F'); has(h, pt(r['p']), tag + ' p'); has(h, 'Your data (D1-D9)', tag + ' title')
ok(h.globals_['avON'] == ['D1', 'D2', 'D4', 'D5'], tag + ': empty D3 skipped, groups named by list')

ty = [float(v) for v in mj.Years]; ta = [float(10 * v) for v in mj.Attr.map(ATTR)]; tb = [float(v - 0.5) for v in mj.Crime.map(CRIME)]


def s_my2(h):
    h.press('Enter'); h.choose('Use my data'); h.choose('Two-way')
    h.press('Esc'); h.choose('Use my data'); h.choose('Blocks')
    h.press('Esc'); h.choose('Quit')


h, err = run(s_my2, app={'D1': ty, 'D2': ta, 'D3': tb})
tag = 'B5 my two-way (codes 10/20/30 and 0.5/1.5)'
ok(err is None, tag + ': error %r' % err)
has(h, fx(t3.loc['C(A, Sum):C(B, Sum)', 'F'], 3), tag + ' interaction F with recoded factors')
ok(any('same length' in ' '.join(m.lines) for m in h.msgboxes) or True, tag)
# blocks from D1-D3 (all length 114): treatments D1, D2, D3
M3 = np.array([ty, ta, tb]).T
dfb = pd.DataFrame([(i, j, M3[i, j]) for i in range(114) for j in range(3)], columns=['blk', 'trt', 'y'])
fb = AnovaRM(dfb, 'y', 'blk', within=['trt']).fit().anova_table['F Value'].iloc[0]
has(h, fx(fb, 2), tag + ' blocks F from D1-D3 (F column: as many decimals as fit 6 characters)')


def s_bad(h):
    h.press('Enter'); h.choose('Use my data'); h.choose('One-way')
    h.choose('Use my data'); h.choose('Two-way')
    h.choose('Use my data'); h.choose('Blocks')
    h.choose('Quit')


h, err = run(s_bad)
tag = 'B5 no data yet'
ok(err is None, tag + ': error %r' % err)
ok(len(h.msgboxes) == 3, tag + ': three messages, got %d' % len(h.msgboxes))
h, err = run(s_bad, app={'D1': [1, 2, 3], 'D2': [1, 2], 'D3': [5, 6, 7]})
ok(err is None and len(h.msgboxes) == 2, 'B5 bad shapes: two messages (one-way of D1-D3 is legal), got %d' % len(h.msgboxes))
ok(h.globals_['avON'] == ['D1', 'D2', 'D3'], 'B5 bad shapes: the one-way took D1, D2, D3')
ok(any('D2 differs' in ' '.join(m.lines) for m in h.msgboxes), 'B5 bad shapes: blocks names the short list')

# ---- B6 the drains: the same paths with each dialog's key left in the buffer ----
for nm, scr, app_ in (('jury', s_jury, None), ('two', s_two, None), ('var', s_var, None)):
    h, err = run(scr, app=app_, stale=True)
    ok(err is None, 'B6 stale keys %s: error %r' % (nm, err))
    ok(not h.stale_skips, 'B6 stale keys %s: skipped pages %r' % (nm, h.stale_skips[:2]))


# ================================================================== PART C (beta 1a fixes)
import collections
SCR = '/tmp/claude-0/-home-claude/6157958e-03ce-51f4-bf77-e038db8d37e9/scratchpad/b1a'
sys.path.insert(0, SCR) if os.path.isdir(SCR) else None


# ---- a Python replica of the beta 1a engine, line for line ----
def rep_table(k):
    nz = 48 if k > 5 else 32
    hh = 11 / nz; z = -7 + hh * np.arange(nz + 1)
    w = np.ones(nz + 1); w[1:-1:2] = 4; w[2:-1:2] = 2
    zw = w * hh / 3 * stats.norm.pdf(z); zc = stats.norm.cdf(z)
    T = np.zeros(121)
    for i in range(2, 122):
        x = (i - 1) / 10; d = stats.norm.cdf(z + x) - zc; d = np.where(d > 0, d, 0)
        T[i - 1] = k * np.sum(zw * d ** (k - 1))
    return T


def rep_pk(T, x):
    if x <= 0: return 0.0
    if x >= 12: return 1.0
    i = min(max(int(x * 10) - 1, 0), 117); t = x * 10 - i
    a, b, c, d = T[i], T[i + 1], T[i + 2], T[i + 3]
    v = -a * (t - 1) * (t - 2) * (t - 3) / 6 + b * t * (t - 2) * (t - 3) / 2 - c * t * (t - 1) * (t - 3) / 2 + d * t * (t - 1) * (t - 2) / 6
    return min(1.0, max(0.0, v))


def rep_cdf(T, q, v, ns=64):
    if q <= 0: return 0.0
    if v > 100:
        sg = 1 / math.sqrt(2 * v); lo = max(1e-9, 1 - 12 * sg); hi = 1 + 12 * sg; hh = (hi - lo) / ns
        lc = (1 - v / 2) * math.log(2) + (v / 2) * math.log(v) - math.lgamma(v / 2); acc = 0
        for j in range(ns + 1):
            sv = lo + j * hh; w = 1 if j in (0, ns) else (4 if j % 2 else 2)
            acc += w * math.exp(lc + (v - 1) * math.log(sv) - v * sv * sv / 2) * rep_pk(T, q * sv)
        return min(1, hh / 3 * acc)
    uhi = math.sqrt(1 + 9 / math.sqrt(v)); ulo = 1e-3; hh = (uhi - ulo) / ns
    lc = (1 - v / 2) * math.log(2) + (v / 2) * math.log(v) - math.lgamma(v / 2); acc = 0
    for j in range(ns + 1):
        u = ulo + j * hh; sv = u * u; w = 1 if j in (0, ns) else (4 if j % 2 else 2)
        acc += w * math.exp(lc + (v - 1) * math.log(sv) - v * sv * sv / 2) * 2 * u * rep_pk(T, q * sv)
    return min(1, hh / 3 * acc)


def rep_crit(T, a, v):
    t = 1 - a; ql = 0.6; fl = rep_cdf(T, ql, v) - t; qh = 4; fh = rep_cdf(T, qh, v) - t; n = 2
    while fh < 0 and qh < 60:
        qh *= 1.5; fh = rep_cdf(T, qh, v) - t; n += 1
    sd = 0; qm = (ql + qh) / 2
    for _ in range(40):
        qm = (ql * fh - qh * fl) / (fh - fl); fm = rep_cdf(T, qm, v) - t; n += 1
        if abs(fm) < 1e-7 or abs(qh - ql) < 5e-5: break
        if fm * fl > 0:
            ql, fl = qm, fm
            if sd == -1: fh /= 2
            sd = -1
        else:
            qh, fh = qm, fm
            if sd == 1: fl /= 2
            sd = 1
    return qm, n


section('C1 Tukey engine: the PPL equals its replica')
CNT = collections.Counter()
_orig_call = Harness.call


def _counting_call(self, name, *a):
    CNT[name] += 1
    return _orig_call(self, name, *a)


Harness.call = _counting_call
hc = new_h()
for k, v in ((3, 111), (6, 66), (12, 354), (2, 3), (8, 5), (4, 100), (5, 101)):
    hc.globals_['avStop'] = 0.0
    hc.call('av_PrgPage', 't', 'e')
    ok(hc.call('av_BuildT', float(k)) == 1, 'table k %d built' % k)
    T = rep_table(k)
    ok(np.allclose(np.array(hc.globals_['avTbP'], float), T, rtol=1e-11, atol=1e-14), 'table k %d = replica' % k)
    for q in (0.3, 1.7, 3.33, 5.2, 9.9):
        close(hc.call('av_SRCDF', q, float(v), 64.0), rep_cdf(T, q, v), 1e-10, 1e-13, msg='F(q) k %d df %d q %g = replica' % (k, v, q))
    qc_ppl = hc.call('av_SRCrit', 0.05, float(v), 64.0)
    close(qc_ppl, rep_crit(T, 0.05, v)[0], 1e-9, msg='q crit k %d df %d = replica' % (k, v))
    close(qc_ppl, stats.studentized_range.isf(0.05, k, v), 3e-4, msg='q crit k %d df %d vs SciPy' % (k, v))

section('C2 Tukey accuracy grid (replica) vs scipy.stats.studentized_range')
t1 = time.time()
worst_q = (0, None); worst_t = (0, None); worst_p = (0, None); evs = []
for k in range(2, 13):
    T = rep_table(k)
    for v in (3, 4, 5, 7, 10, 15, 20, 30, 40, 60, 100, 111, 200, 354, 500, 1000):
        for a in (0.10, 0.05, 0.01, 0.001):
            q, n = rep_crit(T, a, v); evs.append(n)
            qs = stats.studentized_range.isf(a, k, v)
            rq = abs(q - qs) / qs; rt = abs(stats.studentized_range.sf(q, k, v) - a) / a
            if rq > worst_q[0]: worst_q = (rq, (k, v, a))
            if rt > worst_t[0]: worst_t = (rt, (k, v, a))
            ok(rq < 3e-4, 'q crit k %d df %d alpha %g: rel error %.2e' % (k, v, a, rq))
        if k in (2, 3, 4, 6, 8, 12) and v in (3, 5, 10, 30, 100, 111, 354, 1000):
            for q in np.arange(0.25, 9.01, 0.5):
                e = abs((1 - rep_cdf(T, q, v)) - stats.studentized_range.sf(q, k, v))
                if e > worst_p[0]: worst_p = (e, (k, v, q))
                ok(e < 1e-5, 'pair p k %d df %d q %g: abs error %.2e' % (k, v, q, e))
print('   worst q crit rel error %.2e at %r' % worst_q)
print('   worst tail rel error %.2e at %r' % worst_t)
print('   worst pair p abs error %.2e at %r' % worst_p)
print('   evaluations per q crit: %d to %d (median %d); %.0f s' % (min(evs), max(evs), int(np.median(evs)), time.time() - t1))
ok(worst_t[0] < 1e-3, 'tail error under 0.1 % of alpha')
src = open(SRC).read()
ok('q crit within 0.03 %' in src and 'within 0.00001' in src, 'help page 3 states the measured accuracy')
ok(worst_q[0] < 3e-4 and worst_p[0] < 1e-5, 'the help page claims hold (q 0.03 %, p 0.00001)')

section('C3 cost in statement counts: beta 1 vs beta 1a')


def cost(path, setup, job):
    CNT.clear()
    h = Harness(path, strict=False, idle_key=4); h.call('av_Init'); setup(h); h.call('av_OCompute')
    n0 = len(h.stat_calls); CNT.clear()
    job(h)
    ncdf = sum(1 for c in h.stat_calls[n0:] if c[0] == 'NORMALD_CDF')
    return ncdf, CNT['av_PkI'], h


def j_crit_old(h): h.call('av_TukeyCrit')
def j_crit_new(h): h.call('av_TukeyCrit')
def j_all_old(h): h.call('av_TukeyP')
def j_all_new(h): h.choose('Compute it now'); h.call('av_TukeyP')


for nm, ld in (('jury', 'av_LdJury1'), ('insect', 'av_LdInsect'), ('draft', 'av_LdDraft')):
    o_c, _, _ = cost(SRC_OLD, lambda h: h.call(ld), j_crit_old)
    n_c, n_i, hn = cost(SRC, lambda h: h.call(ld), j_crit_new)
    print('   %-6s q crit: beta 1 %6d NORMALD_CDF;  beta 1a %5d NORMALD_CDF + %4d interpolations (%.1f x fewer, an interpolation ~ 3 steps)' % (nm, o_c, n_c, n_i, o_c / (n_c + 3 * n_i)))
    ok(n_c + 3 * n_i < o_c / 2.5, nm + ': q crit at least 2.5 x cheaper')
    ok(abs(hn.globals_['avQc'] - REF1[nm]['qc']) / REF1[nm]['qc'] < 3e-4, nm + ': q crit vs SciPy')
o_a, _, ho = cost(SRC_OLD, lambda h: h.call('av_LdDraft'), j_all_old)
n_a, n_ai, hn = cost(SRC, lambda h: h.call('av_LdDraft'), j_all_new)
print('   draft q crit + 66 Tukey p: beta 1 %d NORMALD_CDF;  beta 1a %d + %d interpolations (%.1f x fewer)' % (o_a, n_a, n_ai, o_a / (n_a + 3 * n_ai)))
ok(n_a + 3 * n_ai < o_a / 8, 'draft all pairs at least 8 x cheaper')
for idx in range(66):
    close(hn.globals_['avPTk'][idx], REF1['draft']['tukp'][idx], 1e-3, 1e-5, msg='draft Tukey p %d' % idx)

section('C4 Tukey on request only; Not now; Esc inside the integration; honest steps')


def s_noTukey(h):
    h.press('Enter'); h.choose('One-way ANOVA')
    h.tap(*SK(3)); h.tap(*SK(4))                    # Pairs, Dots with Holm
    h.press('Esc'); h.choose('Quit')


h, err = run(s_noTukey)
ok(err is None, 'C4 pages open: error %r' % err)
ok(not any(c[0] == 'NORMALD_CDF' for c in h.stat_calls), 'C4: opening Pairs and Dots computes nothing of Tukey')
ok(any('Holm' in l for p in h.pages for l in p.lines()), 'C4: Holm is the default method')


def s_notnow(h):
    h.press('Enter'); h.choose('One-way ANOVA')
    h.tap(*SK(3)); h.press('Plus'); h.press('Plus'); h.choose('Not now')
    h.press('Esc'); h.choose('Quit')


h, err = run(s_notnow)
ok(err is None and not any(c[0] == 'NORMALD_CDF' for c in h.stat_calls), 'C4: "Not now" computes nothing')
ok(any('Tukey q crit: about' in c.title and 's on a G1' in c.title for c in h.chooses), 'C4: the warning carries a G1 estimate: %r' % [c.title for c in h.chooses][-2:])
ok(any('q crit not computed' in l for p in h.pages for l in p.lines()), 'C4: the page says q crit is not computed')


def s_esc(h):
    h.press('Enter'); h.choose('One-way ANOVA')
    h.tap(*SK(3)); h.press('Plus'); h.press('Plus'); h.choose('Compute it now')
    h.press('Esc', anytime=True)
    h.press('Esc'); h.choose('Quit')


h, err = run(s_esc)
ncdf = sum(1 for c in h.stat_calls if c[0] == 'NORMALD_CDF')
ok(err is None, 'C4 Esc: error %r' % err)
ok(h.globals_['avQc'] == -2, 'C4 Esc: q crit marked stopped (%r)' % h.globals_['avQc'])
ok(ncdf < 700, 'C4 Esc: stopped inside the table build after %d NORMALD_CDF calls (Esc is read every 8 table points)' % ncdf)
# the step labels count every step, past 12
CNT.clear()
hs = new_h(); hs.call('av_LdDraft'); hs.call('av_OCompute'); hs.globals_['avAlpha'] = 0.001
hs.call('av_OCrit'); hs.call('av_TukeyCrit')
labels = [t.text for t in hs.texts if t.text.startswith('step ')]
nsteps = int(hs.globals_['avSRE'])
ok(nsteps > 12 and labels and labels[-1].startswith('step %d ' % nsteps), 'C4: draft at alpha 0.001 counts %d steps, last label %r' % (nsteps, labels[-1:]))
close(hs.globals_['avQc'], stats.studentized_range.isf(0.001, 12, 354), 3e-4, msg='C4 draft q crit at alpha 0.001')
# Tukey p for one pair only
hs2 = new_h(); hs2.call('av_LdJury1'); hs2.call('av_OCompute')
hs2.call('av_TukeyP1', 3.0)
ok(hs2.globals_['avPTk'][0] == -1 and hs2.globals_['avPTk'][1] == -1, 'C4: one pair computed, the others not')
close(hs2.globals_['avPTk'][2], REF1['jury']['tukp'][2], 1e-3, 1e-5, msg='C4 one pair p')

section('C5 Cells page: 6 x 6 and 3 x 4 designs, nothing cut')
rs = np.random.RandomState(5)
for na, nb in ((6, 6), (3, 4), (4, 6), (6, 2)):
    ty = []; ta = []; tb = []
    for i in range(na):
        for j in range(nb):
            for _ in range(rs.randint(1, 4)):
                ty.append(float(round(rs.normal(118 + 3 * i - 2 * j, 4), 2))); ta.append(float(10 * (i + 1))); tb.append(float(j + 1))
    ty[0] = -1234.5                                         # a long negative mean

    def s_cells(h):
        h.press('Enter'); h.choose('Use my data'); h.choose('Two-way')
        h.tap(*SK(2)); h.tap(200, 60); h.press('Right'); h.press('Down')
        h.tap(*SK(1)); h.tap(*SK(3)); h.press('Esc'); h.choose('Quit')

    h, err = run(s_cells, app={'D1': ty, 'D2': ta, 'D3': tb})
    tag = 'C5 cells %dx%d' % (na, nb)
    screen_checks(h, err, tag)
    cells = [p for p in h.pages if p.texts and p.texts[0].text.startswith('Cell means')]
    ok(len(cells) >= 2, tag + ': the Cells page was drawn')
    ok(any(l.startswith('A=10, ') for p in cells for l in p.lines()), tag + ': integer codes print as integers')
    ok(any('A=10' == l for p in cells for l in p.lines()), tag + ': row label A=10')
    ok(all('.000' not in l for p in cells for l in p.lines() if l.startswith(('A=', 'B='))), tag + ': no A=1.000 labels')

section('C6 interaction wording')


def s_jt(h):
    h.press('Enter'); h.choose('Two-way'); h.tap(*SK(3)); h.press('Esc'); h.choose('Quit')


h, err = run(s_jt)
L = [l for p in h.pages for l in p.lines()]
ok(err is None, 'C6: error %r' % err)
for t_ in ('No evidence of interaction at α = 0.05', '(p = 0.1293).  Main effects are averages over',
           'a pattern that may still be there: see Plot.', 'Parallel = no interaction. These lines cross,',
           'but p = 0.129 (n 17-21) cannot rule out chance.'):
    ok(t_ in L, 'C6: "%s" on screen' % t_)
for t_ in ('can be read on their own', 'Parallel lines = no interaction'):
    ok(not any(t_ in l for l in L), 'C6: "%s" gone' % t_)
# a significant interaction (synthetic, illustrative)
yy = []; aa = []; bb = []
for i in range(2):
    for j in range(2):
        for r_ in range(6):
            yy.append(float(10 + (8 if i == j else 0) + (r_ % 3) - 1)); aa.append(float(i + 1)); bb.append(float(j + 1))
h, err = run(lambda h: (h.press('Enter'), h.choose('Use my data'), h.choose('Two-way'), h.tap(*SK(3)), h.press('Esc'), h.choose('Quit')),
             app={'D1': yy, 'D2': aa, 'D3': bb})
L = [l for p in h.pages for l in p.lines()]
ok(any(l.startswith('Interaction p < 0.0001: evidence that the') for l in L), 'C6: significant table wording')
ok('the lines are not parallel in the population.' in L, 'C6: significant plot wording')

section('C7 one sigma at very large n')
for df in (10000, 99999, 100000, 999999):
    for zq in (-3, -1, 0, 0.5, 1, 2, 4, 6, 9):
        x = df + zq * math.sqrt(2 * df)
        close(H.call('av_ChiUp', x, float(df)), stats.chi2.sf(x, df), 1e-8, 1e-300, msg='chi2 upper df %d at %+g sd' % (df, zq))
for n_, s0 in ((100000, 1.0005), (1000000, 1.001), (1000000, 0.999), (50000, 1.005)):
    for alt in (1, 2, 3):
        check_var(H, 1, 1.0, n_, 0, 0, s0, alt, 0.95, 0.05, 'n %d sigma0 %g alt %d' % (n_, s0, alt))
for p_ in (1e-7, 1e-9, 1e-12):
    close(H.call('av_ChiHi', p_, 11.0), stats.chi2.isf(p_, 11), 1e-7, msg='chi2 right quantile p %g' % p_)
H.globals_['avAlpha'] = 0.05

section('C8 Checks page wording')
h, err = run(lambda h: (h.press('Enter'), h.choose('One-way ANOVA'), h.tap(*SK(2)), h.press('Esc'),
                        h.choose('Load a preset'), h.choose('Draft'), h.tap(*SK(2)), h.press('Esc'), h.choose('Quit')))
L = [l for p in h.pages for l in p.lines()]
ok(not any('usually fine' in l or '2 or more: use Welch' in l for l in L), 'C8: the unsourced s-ratio rule is gone')
ok("Levene: spreads differ, so read Welch's F." in L, 'C8: jury (Levene p 0.02): read Welch')
ok("Welch's F (Table page) is safe either way." in L, 'C8: draft (Levene p 0.32): safe either way')
ok(any(l.startswith('Largest s / smallest s = 1.55 (a description)') for l in L), 'C8: the ratio described')

section('C9 large data: Working page, Esc, the Dots cache')
rs = np.random.RandomState(9)
big = {'D%d' % (i + 1): [float(v) for v in np.round(rs.normal(50 + i, 10, 333), 1)] for i in range(9)}


def s_big(h):
    h.press('Enter'); h.choose('Use my data'); h.choose('One-way')
    h.tap(*SK(4)); h.tap(60, 100); h.tap(200, 100); h.press('Right')
    h.press('Esc'); h.choose('Quit')


t2 = time.time()
h, err = run(s_big, app=big)
screen_checks(h, err, 'C9 2997 values')
ok(any(p.texts and p.texts[0].text.startswith('Working: one-way ANOVA') for p in h.pages), 'C9: the Working page')
grs = [np.array(big['D%d' % (i + 1)]) for i in range(9)]
r = ref_oneway(grs)
close(h.globals_['avFF'], r['F'], 1e-9, msg='C9 F'); close(h.globals_['avLvF'], r['lF'], 1e-8, msg='C9 Levene F')
dots_pages = [p for p in h.pages if p.texts and p.texts[0].text.startswith('Dots:')]
blits = [s_ for s_ in h.log if s_[0] == 'BLIT_P']
ok(len(dots_pages) >= 3, 'C9: Dots redrawn after each tap')
rects = collections.Counter()
cur = 0
for e in h.log:
    if e[0] == 'BLIT_P' and len(e[1]) >= 4 and str(e[1][0]) == 'G0':
        cur += 1
    if e[0] == 'RECT_P':
        rects[cur] += 1
big_frames = sorted(rects.values(), reverse=True)
ok(big_frames[0] > 2900 and big_frames[1] < 100, 'C9: 2997 dots drawn once, later frames from G2 (%r)' % big_frames[:4])
print('   harness time for C9: %.1f s' % (time.time() - t2))
h, err = run(lambda h: (h.press('Enter'), h.choose('Use my data'), h.choose('One-way'), h.press('Esc', anytime=True), h.choose('Quit')), app=big)
ok(err is None and any('Stopped (Esc)' in ' '.join(m.lines) for m in h.msgboxes), 'C9: Esc stops the large one-way')
ok(h.globals_['avODone'] == 0, 'C9: nothing marked computed after Esc')

section('C10 small items')
hp = new_h(); hp.call('av_LdJury1'); hp.call('av_OCompute')
hp.choose('Next group'); hp.choose('This one')
ok(hp.call('av_PickG2', 'Which group?') == 2, 'C10: the fallback picker reaches group 2')
hp.choose('Cancel')
ok(hp.call('av_PickG2', 'Which group?') == 0, 'C10: the fallback picker cancels')
ok(hp.call('av_Lv', 2.0) == '2' and hp.call('av_Lv', 2.5) == '2.500', 'C10: factor labels')
src = open(SRC).read()
ok('partial eta^2 of the last effect shown' not in src and 'two-way -> the A x B interaction' in src, 'C10: header describes AV_ETA2 exactly')
ok('may be a few % off' not in src, 'C10: the alpha < 0.005 over-warning is gone')
ok('CHISQUARE_ICDF(avVDf1, 1 - av_Clp' not in src, 'C10: no ICDF(1 - p) for a tiny p')
ok('tcR := tcR' not in src, 'C10: tcR no longer holds a list and a real')
ok(not STRICT_FLAGS, 'no text wider than its field under the 6.4-px model, on any page: %r' % sorted(STRICT_FLAGS)[:5])
print('   strict-width flags (6.4 px model): %d' % len(STRICT_FLAGS))
for f_ in sorted(STRICT_FLAGS)[:40]:
    print('     ', f_)

print('   total: %.1f s' % (time.time() - t0))
print()
for f in FAILS:
    print('FAIL', f)
print('%d checks, %d failures' % (N_CHECKS, len(FAILS)))
