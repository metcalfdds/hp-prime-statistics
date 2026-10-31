#!/usr/bin/env python3
"""verify_TTestLab_beta1a.py -- checks TTestLab beta 1a (31 Oct 2026; beta 1 the same afternoon, with the examples' sources
named on screen in 1a), the five-step t tests of Roger's lecture note
"Hypothesis Testing: t-Test (with two population means)": pooled-variances, separate-variances (Welch) and
dependent-samples t, with any mix of equal or unequal variances and equal or unequal N.

A  the arithmetic against SciPy: pooled and separate SE, t and df over a grid of equal / unequal N and SD (and SDs
   of 1E-200 and 1E200); paired t from raw pairs and from summary numbers; p in all three tails; t critical for every
   column of the t table, integer and fractional df, and its bisection fallback; the printed table's row rule; the
   lecture's printed t table, cell by cell (A6); Cohen's d.
B  the three examples: the lecture's two (exact values beside the lecture's rounded ones) and Roger's SPSS output.
C  the screens: each step's texts for each example and tails; the flowchart (taps on its boxes and its soft keys,
   Back, OK, Esc); the forms; D1 and D2; the refusals; the menu; help.
E  the "Pooled or separate?" page: the same t when N1 = N2 or s1 = s2; which way the pooled test errs (and a
   simulation of its type I error rate that backs the claim).
F  a finger still on a form's OK when the form closes is waited out (tt_Settle), not read as a tap on Menu; a copy
   without the finger drain reproduces the fault.
G  static: no "!=", every routine tagged tt_, every file-level variable tagged tt, one EXPORT.
D  layout: text_overlap_v1's recorder over every screen drawn above: no firm overlap, frame straddle or overrun.

Needs TTestLab_lecture_t_table_v1.py (the lecture's t table, transcribed) beside this file, the PPL harness ppl_run_v3e.py and text_overlap_v1.py (in ./tools, ../tools, this folder, or $TTL_TOOLS),
hp-prime-kit ($HPKIT), SciPy, NumPy.
Run:  python3 verify_TTestLab_beta1a.py [TTestLab_beta1a.txt]     (exit code 0 = all passed)
"""
import math
import os
import re
import sys
import tempfile
import warnings

import numpy as np
from scipy import stats
from scipy.stats import t as tdist

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HPKIT', '/home/claude/kit/hp-prime-kit-HEAD')
# the harness and the overlap recorder may sit in different folders (in D:\\HP-Prime the harness is at the top and
# text_overlap_v1.py in tools\\): every candidate folder that holds either goes on the path, the first found first
_cands = [c for c in (os.environ.get('TTL_TOOLS', ''), os.path.join(HERE, 'tools'), os.path.join(HERE, '..', 'tools'),
                      HERE, '/home/claude/pv25g/gate/tools') if c]
for cand in reversed(_cands):
    if any(os.path.exists(os.path.join(cand, f)) for f in ('ppl_run_v3e.py', 'text_overlap_v1.py')):
        sys.path.insert(0, cand)
import ppl_run_v3e  # noqa: E402,F401
from ppl_run_v3e import Harness, ACCEPT  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402

PROG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'TTestLab_beta1a.txt')
if not os.path.exists(PROG):
    PROG = os.path.join(HERE, '..', 'programs', 'TTestLab_beta1a.txt')
SRC = open(PROG, encoding='utf-8').read()

FAIL = []
NPASS = [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:400]) if (detail != '' and not ok) else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


def U(s):
    """screen text with the Prime's minus (U+2212) read as a hyphen"""
    return s.replace('−', '-')


def H(app=None, path=PROG):
    h = Harness(path, idle_key=4, home_minus=True, app_data=app)
    h.execute('tt_Init()')
    return h


def put(h, **kv):
    for k, v in kv.items():
        h.globals_[k] = [float(x) for x in v] if isinstance(v, (list, tuple)) else float(v)


def g(h, k):
    return h.globals_[k]


def calc(h, **kv):
    put(h, **kv)
    h.execute('tt_Calc()')
    return h


def page(h, call):
    h.reset_records()
    h.execute(call)
    return h.pages[-1]


def lines(pg):
    return [U(x) for x in pg.lines()]


def has(pg, sub):
    return any(sub in x for x in lines(pg))


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def welch_df(s1, s2, n1, n2):
    a, b = s1 ** 2 / n1, s2 ** 2 / n2
    return (a + b) ** 2 / (a ** 2 / (n1 - 1) + b ** 2 / (n2 - 1))


OV.install()

# ===================================================================== A. arithmetic
print('=== A. the arithmetic against SciPy')
h = H()
worst = [0.0, None]
grid = 0
for n1, n2 in ((10, 10), (10, 40), (40, 10), (44, 31), (270, 146), (2, 2), (5, 1000), (3, 7)):
    for s1, s2 in ((1, 1), (1, 3), (3, 1), (1.45, 1.11), (3.28798, 3.74872), (0.01, 50)):
        for m1, m2 in ((15.89, 16.57), (4.8185, 6.4247), (100, 100.5)):
            put(h, ttM1=m1, ttS1=s1, ttN1=n1, ttM2=m2, ttS2=s2, ttN2=n2)
            for pk, ev in ((1, True), (2, False)):
                se, tt, df, sp_ = h.execute('tt_Ind(%d)' % pk)
                r = stats.ttest_ind_from_stats(m1, s1, n1, m2, s2, n2, equal_var=ev)
                if ev:
                    sp_ref = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
                    se_ref = sp_ref * math.sqrt((n1 + n2) / (n1 * n2))
                    df_ref = n1 + n2 - 2
                else:
                    se_ref = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
                    df_ref = welch_df(s1, s2, n1, n2)
                e = max(rel(se, se_ref), rel(tt, r.statistic), rel(df, df_ref))
                grid += 1
                if e > worst[0]:
                    worst = [e, (n1, n2, s1, s2, m1, m2, pk)]
check('A1 pooled and separate SE, t and df equal SciPy\'s ttest_ind_from_stats (and the textbook formulas) in %d '
      'cases: equal and unequal N, equal and unequal SD, smaller group with the larger SD and the reverse '
      '(worst relative difference %.1e)' % (grid, worst[0]), worst[0] < 1e-12, worst)
# extreme SDs: scale-free, so compare with the same case at SD ~ 1
ext = []
for sc in (1e-200, 1e200):
    put(h, ttM1=15.89 * sc, ttS1=1.45 * sc, ttN1=44, ttM2=16.57 * sc, ttS2=1.11 * sc, ttN2=31)
    for pk in (1, 2):
        se, tt, df, _ = h.execute('tt_Ind(%d)' % pk)
        put(h, ttM1=15.89, ttS1=1.45, ttN1=44, ttM2=16.57, ttS2=1.11, ttN2=31)
        se0, tt0, df0, _ = h.execute('tt_Ind(%d)' % pk)
        put(h, ttM1=15.89 * sc, ttS1=1.45 * sc, ttN1=44, ttM2=16.57 * sc, ttS2=1.11 * sc, ttN2=31)
        ext.append((sc, pk, rel(se / sc, se0), rel(tt, tt0), rel(df, df0)))
check('A1 SDs of 1E-200 and 1E200 (divided by the larger before squaring): the same t and df as at SD ~ 1, SE scaled',
      all(max(x[2:]) < 1e-12 for x in ext), ext)

# paired
rng = np.random.default_rng(31)
pw = [0.0, None]
cnt = 0
for n in (2, 3, 5, 12, 30, 200):
    for rep in range(4):
        a = np.round(rng.normal(10, 3, n), 2)
        b = np.round(a + rng.normal(0.4, 1.5, n), 2)
        put(h, ttTY=3, ttSRC=2, ttX1=list(a), ttX2=list(b))
        for tl, alt in ((0, 'two-sided'), (-1, 'less'), (1, 'greater')):
            put(h, ttTL=tl, ttAL=0.05)
            h.execute('tt_Calc()')
            r = stats.ttest_rel(a, b, alternative=alt)
            d = a - b
            e = max(rel(g(h, 'ttT'), r.statistic), rel(g(h, 'ttP'), r.pvalue), abs(g(h, 'ttDF') - (n - 1)),
                    rel(g(h, 'ttSDv'), np.std(d, ddof=1)), rel(g(h, 'ttMD'), d.mean()),
                    rel(g(h, 'ttD'), d.mean() / np.std(d, ddof=1)))
            cnt += 1
            if e > pw[0]:
                pw = [e, (n, rep, tl)]
check('A2 dependent samples from pairs in D1/D2 (tt_Pairs): x-bar D, sD, t, df = N - 1, p in all three tails and '
      'Cohen\'s d (mean / sD) equal SciPy\'s ttest_rel, %d cases, N from 2 to 200 (worst %.1e)' % (cnt, pw[0]),
      pw[0] < 1e-9, pw)
put(h, ttTY=3, ttSRC=1, ttMD=0.182, ttSDv=0.30622, ttNP=5, ttTL=0, ttAL=0.05)
h.execute('tt_Calc()')
ref_t = 0.182 / (0.30622 / math.sqrt(5))
check('A2 dependent samples from the mean and SD of the differences: t = %.6f (by hand %.6f), df 4, SE sD/sqrt(N)'
      % (g(h, 'ttT'), ref_t), rel(g(h, 'ttT'), ref_t) < 1e-12 and g(h, 'ttDF') == 4)

# p values, independent, three tails
pe = [0.0, None]
for (m1, s1, n1, m2, s2, n2) in ((15.89, 1.45, 44, 16.57, 1.11, 31), (4.8185, 3.28798, 270, 6.4247, 3.74872, 146),
                                  (5, 2, 8, 4, 6, 20), (5, 2, 8, 5, 6, 20)):
    for ty, ev in ((1, True), (2, False)):
        for tl, alt in ((0, 'two-sided'), (-1, 'less'), (1, 'greater')):
            calc(h, ttTY=ty, ttSRC=1, ttTL=tl, ttAL=0.05, ttM1=m1, ttS1=s1, ttN1=n1, ttM2=m2, ttS2=s2, ttN2=n2)
            r = stats.ttest_ind_from_stats(m1, s1, n1, m2, s2, n2, equal_var=ev, alternative=alt)
            e = rel(g(h, 'ttP'), r.pvalue)
            if e > pe[0]:
                pe = [e, (m1, n1, ty, tl)]
check('A3 p for H1 mu1 != mu2, mu1 < mu2 and mu1 > mu2 (lower tails only), pooled and separate, equals SciPy '
      '(worst %.1e); t = 0 gives p = 1 two-tailed, not 2 x 0.5 rounded' % pe[0], pe[0] < 1e-9 and
      abs(g(h, 'ttP') - 0.5) < 1 and True, pe)
calc(h, ttTY=1, ttTL=0, ttM1=5, ttM2=5, ttS1=2, ttS2=2, ttN1=10, ttN2=10)
check('A3 equal means: t = 0, p = %s two-tailed' % g(h, 'ttP'), g(h, 'ttT') == 0 and g(h, 'ttP') == 1)

# t critical
ONE = [0.10, 0.05, 0.025, 0.01, 0.005, 0.0005]
TWO = [0.20, 0.10, 0.05, 0.02, 0.01, 0.001]
ce = [0.0, None]
ncrit = 0
for df in (1, 2, 4, 7.5, 30, 60, 73, 265.924, 1000):
    for tl, alist in ((0, TWO), (-1, ONE), (1, ONE)):
        for al in alist:
            put(h, ttTL=tl, ttAL=al)
            v = h.execute('tt_Crit(%r)' % df)
            ref = tdist.isf(al / 2 if tl == 0 else al, df)
            ncrit += 1
            if rel(v, ref) > ce[0]:
                ce = [rel(v, ref), (df, tl, al, v, ref)]
check('A4 t critical (-STUDENT_ICDF of a lower tail, checked by STUDENT_CDF) equals SciPy for every column of the '
      'table, both tails, df 1 to 1000 and fractional df: %d values, worst %.1e' % (ncrit, ce[0]), ce[0] < 1e-10, ce)
# the fallback: STUDENT_ICDF unavailable (renamed so that it raises inside IFERR)
fb_src = SRC.replace('cv := -STUDENT_ICDF(cdf,ca);', 'cv := -STUDENT_ICDFX(cdf,ca);')
fb_path = os.path.join(tempfile.mkdtemp(), 'TTestLab_fallback.txt')
open(fb_path, 'w', encoding='utf-8').write(fb_src)
hf = H(path=fb_path)
fe = [0.0, None]
for df in (1, 4, 7.5, 73, 265.924):
    for tl, alist in ((0, TWO), (1, ONE)):
        for al in alist:
            put(hf, ttTL=tl, ttAL=al)
            v = hf.execute('tt_Crit(%r)' % df)
            ref = tdist.isf(al / 2 if tl == 0 else al, df)
            if rel(v, ref) > fe[0]:
                fe = [rel(v, ref), (df, tl, al, v, ref)]
check('A4 the fallback (STUDENT_ICDF fails inside IFERR, bisection on STUDENT_CDF, as CICatcher\'s cqTCrit): '
      'the same t critical to %.1e (df 1 at alpha .0005: %.3f)' % (fe[0], tdist.isf(0.0005, 1)),
      fb_src != SRC and fe[0] < 1e-9, fe)

# the table's row rule
rows = {1: 1, 4: 4, 4.5: 4, 4.6: 5, 29.6: 30, 30: 30, 30.4: 30, 35: 30, 35.1: 40, 50: 40, 50.1: 60, 73: 60, 90: 60,
        90.1: 120, 119: 120, 265.924: 120, 5000: 120}
got = {df: h.execute('tt_TabDF(%r)' % df) for df in rows}
check('A5 the printed table\'s row (the lecture: "the value that is closest to it", df 73 -> 60; a tie to the '
      'smaller row; rows 1-30, 40, 60, 120): %s' % {k: int(v) for k, v in got.items()},
      all(got[k] == v for k, v in rows.items()), [(k, got[k], v) for k, v in rows.items() if got[k] != v])

# the lecture's printed table, cell by cell
sys.path.insert(0, HERE)
from TTestLab_lecture_t_table_v1 import TABLE  # noqa: E402
odd = {(2, 5): 31.598, (3, 5): 12.941, (5, 5): 6.859, (7, 5): 5.405, (23, 5): 3.767}
mism, ncell, prog_mis = [], 0, []
for df, row in TABLE.items():
    for j, v in enumerate(row):
        ncell += 1
        ex = round(tdist.isf(ONE[j], df), 3)
        if abs(ex - v) > 1e-9:
            mism.append((df, ONE[j], v, ex))
        for tl, al in ((0, TWO[j]), (1, ONE[j])):
            calc(h, ttTY=3, ttSRC=1, ttTL=tl, ttAL=al, ttMD=1, ttSDv=1, ttNP=df + 1)
            if g(h, 'ttDFT') != df or abs(g(h, 'ttTB') - v) > 1e-9:
                prog_mis.append((df, tl, al, g(h, 'ttDFT'), g(h, 'ttTB'), v))
check('A6 the lecture\'s t table (appendix 1, transcribed): %d of %d cells equal the exact value to 3 decimals; the '
      'other %d, all in the .0005 one-tailed (.001 two-tailed) column, are %s' %
      (ncell - len(mism), ncell, len(mism), [(m[0], m[2], m[3]) for m in mism]),
      sorted((m[0], 5) for m in mism) == sorted(odd))
check('A6 TTestLab\'s "t table" value (ttTB) is the lecture\'s printed figure in every one of the %d cells, both '
      'tails, the five odd cells included (tt_BookCell)' % ncell, not prog_mis, prog_mis[:5])
pg = None
calc(h, ttTY=3, ttSRC=1, ttTL=0, ttAL=0.001, ttMD=1, ttSDv=1, ttNP=4)
pg = page(h, 'tt_Step3()')
check('A6 step 3, row 3 at alpha .001 two-tailed: "t table, row df = 3: t crit = ±12.941" and "(Row 3 exact: '
      '12.924; lecture\'s table: 12.941.)"', has(pg, 't table, row df = 3:  t crit = ±12.941') and
      has(pg, "(Row 3 exact: 12.924; lecture's table: 12.941.)"), lines(pg))
calc(h, ttTY=3, ttSRC=1, ttTL=0, ttAL=0.05, ttNP=4)
pg = page(h, 'tt_Step3()')
check('A6 the note is absent where the table is right (row 3, alpha .05)', not has(pg, "lecture's table:"),
      lines(pg))

# ===================================================================== B. the examples
print('=== B. the three examples')
h = H()
h.execute('tt_Example(1)')
h.execute('tt_Calc()')
r1 = stats.ttest_ind_from_stats(15.89, 1.45, 44, 16.57, 1.11, 31, equal_var=True)
check('B1 example 1 (age at arrest, pooled, two-tailed .05): t = %.4f (SciPy %.4f), df 73, table row 60 = 2.000, '
      'exact t crit %.3f, reject; p %.4f; d %.3f' % (g(h, 'ttT'), r1.statistic, g(h, 'ttTC'), g(h, 'ttP'), g(h, 'ttD')),
      rel(g(h, 'ttT'), r1.statistic) < 1e-12 and g(h, 'ttDF') == 73 and g(h, 'ttDFT') == 60 and
      g(h, 'ttTB') == 2.0 and abs(g(h, 'ttTC') - tdist.isf(0.025, 73)) < 1e-12 and g(h, 'ttREJ') == 1 and
      g(h, 'ttREJB') == 1 and rel(g(h, 'ttP'), r1.pvalue) < 1e-9)
# the lecture's own arithmetic, reproduced: sqrt(1.74) sqrt(.05) = .29 (to 2 places), -.68/.29 = -2.34
lect_se = round(math.sqrt(1.74) * math.sqrt(0.05), 2)
check('B1 the lecture\'s rounded path gives SE %.2f and t %.2f (it printed .29 and -2.34); exact SE %.4f, t %.2f'
      % (lect_se, -0.68 / lect_se, g(h, 'ttSE'), g(h, 'ttT')),
      lect_se == 0.29 and round(-0.68 / 0.29, 2) == -2.34 and round(g(h, 'ttT'), 2) == -2.20)
p4 = page(h, 'tt_Step4()')
check('B1 step 4 shows the working with the numbers in, the exact t and the lecture\'s note',
      has(p4, '= √[(43 × 1.45² + 30 × 1.11²)/73]') and has(p4, '× √[75/1364]') and
      has(p4, '= √1.745 × √0.05499 = 1.321 × 0.2345') and has(p4, '= 0.3097') and
      has(p4, '= -0.6800/0.3097 = -2.20') and has(p4, 'The lecture rounds √0.05499 to √.05, SE to .29,') and
      has(p4, 'so its t obt is -.68/.29 = -2.34.  Exact: -2.20.'), lines(p4))

h.execute('tt_Example(2)')
h.execute('tt_Calc()')
a = np.array([1.30, 1.25, 0.86, 0.94, 2.26])
b = np.array([1.00, 0.76, 0.99, 1.10, 1.85])
r2 = stats.ttest_rel(a, b, alternative='less')
check('B2 example 2 (matched jails, dependent, one-tailed H1 mu1 < mu2, .05): x-bar D %.3f, sum of squares %.5f, '
      'sD %.5f, SE %.5f, t %.4f (SciPy %.4f), df 4, t crit -2.132, retain; p %.4f'
      % (g(h, 'ttMD'), g(h, 'ttSSq'), g(h, 'ttSDv'), g(h, 'ttSE'), g(h, 'ttT'), r2.statistic, g(h, 'ttP')),
      rel(g(h, 'ttT'), r2.statistic) < 1e-12 and g(h, 'ttDF') == 4 and g(h, 'ttTB') == 2.132 and
      g(h, 'ttREJ') == 0 and rel(g(h, 'ttP'), r2.pvalue) < 1e-9 and abs(g(h, 'ttSSq') - 0.37508) < 1e-9)
lect = (round(0.91 / 5, 2), math.sqrt(0.10), round(0.32 / 2.24, 2), round(0.18 / 0.14, 2))
check('B2 the lecture\'s rounded path: x-bar D .18, sqrt(.38/4) taken as sqrt(.10) = %.2f, SE .32/2.24 = %.2f, t '
      '.18/.14 = %.2f (it printed 1.29); exact t %.2f' % (lect[1], lect[2], lect[3], g(h, 'ttT')),
      lect[0] == 0.18 and round(lect[1], 2) == 0.32 and lect[2] == 0.14 and lect[3] == 1.29 and
      round(g(h, 'ttT'), 2) == 1.33)
p4 = page(h, 'tt_Step4()')
check('B2 step 4: the Table 11.4 columns for the five pairs, the sum .3751 ("sum", not the unverified sigma glyph), sD, SE, t obt and the lecture\'s note',
      has(p4, 'sum = 0.3751') and has(p4, 'sD = √(sum/(N-1)) = √(0.3751/4) = 0.3062') and
      has(p4, 'SE = sD/√N = 0.3062/√5 = 0.1369') and has(p4, 'D/SE = 0.1820/0.1369 = 1.33') and
      has(p4, 'The lecture rounds') and has(p4, 'so SE = .14 and t obt = 1.29.  Exact: 1.33.'), lines(p4))
p5 = page(h, 'tt_Step5()')
check('B2 step 5: retain, and the samples differ the other way from H1 (t > 0, H1 predicted < 0)',
      has(p5, 'RETAIN H₀.') and has(p5, 'The samples even differ the other way from H₁.') and
      has(p5, 'Report t(4) = 1.33, p = 0.873, one-tailed'), lines(p5))

h.execute('tt_Example(3)')
h.execute('tt_Calc()')
r3 = stats.ttest_ind_from_stats(4.8185, 3.28798, 270, 6.4247, 3.74872, 146, equal_var=False)
check('B3 example 3 (Roger\'s SPSS output, separate variances): t %.3f, df %.3f, SE %.5f -- SPSS printed -4.351, '
      '265.924, .36918; p %.2e (SciPy %.2e)' % (g(h, 'ttT'), g(h, 'ttDF'), g(h, 'ttSE'), g(h, 'ttP'), r3.pvalue),
      round(g(h, 'ttT'), 3) == -4.351 and round(g(h, 'ttDF'), 3) == 265.924 and round(g(h, 'ttSE'), 5) == 0.36918
      and rel(g(h, 'ttP'), r3.pvalue) < 1e-9 and g(h, 'ttDFT') == 120)
p2 = page(h, 'tt_Step2()')
check('B3 step 2: the Welch-Satterthwaite df worked: a and b, numerator and denominator, 265.92',
      has(p2, 'a = s₁²/N₁ = 0.04004,  b = s₂²/N₂ = 0.09625') and has(p2, '= 265.92'), lines(p2))
p4 = page(h, 'tt_Step4()')
check('B3 step 4: SE = sqrt(3.28798²/270 + 3.74872²/146) = 0.3692, t obt -4.35, and SPSS\'s row quoted',
      has(p4, '= √(3.28798²/270 + 3.74872²/146)') and has(p4, '= 0.3692') and has(p4, '= -4.35') and
      has(p4, 'SPSS, "Equal variances not assumed": t = -4.351,'), lines(p4))
p1 = page(h, 'tt_Step1()')
check('B3 step 1: SPSS\'s SDs shown as typed (3.28798, 3.74872), the groups\' names, the outcome',
      has(p1, 's₁ = 3.28798') and has(p1, 's₂ = 3.74872') and has(p1, 'Male') and has(p1, 'Female') and
      has(p1, 'Outcome: amount of drug use experience (SPSS)'), lines(p1))
put(h, ttTY=1)
h.execute('tt_Calc()')
rp = stats.ttest_ind_from_stats(4.8185, 3.28798, 270, 6.4247, 3.74872, 146, equal_var=True)
p4 = page(h, 'tt_Step4()')
check('B3 the same data pooled: t %.3f on 414 df (SciPy %.3f); step 4 says this is SPSS\'s "assumed" row and that '
      'its Levene p = .009 points to the other' % (g(h, 'ttT'), rp.statistic),
      rel(g(h, 'ttT'), rp.statistic) < 1e-12 and g(h, 'ttDF') == 414 and
      has(p4, 'This is SPSS\'s "Equal variances assumed" row;') and has(p4, 'its Levene p = .009 points to the other row.'), lines(p4))
put(h, ttEX=1, ttTY=2)
h.execute('tt_Calc()')
p4 = page(h, 'tt_Step4()')
check('B the lecture\'s note shows only while the example\'s test is the one on screen (example 1 switched to '
      'separate: no note)', not has(p4, 'The lecture rounds'), lines(p4))

# ===================================================================== C. screens and flows
print('=== C. screens, the flowchart, the forms, D1/D2, refusals, menu, help')


def run(script, app=None, path=PROG):
    h = Harness(path, idle_key=4, home_minus=True, app_data=app)
    script(h)
    try:
        res = h.execute('TTESTLAB()')
        err = None
    except Exception as e:
        res, err = None, '%s: %s' % (type(e).__name__, str(e)[:120])
    return h, res, err


def menus_drawn(h):
    """the soft-key labels of every DRAWMENU call (DRAWMENU paints G0 after the page's BLIT_P)"""
    out = []
    for it in h.log:
        if it[0] == 'DRAWMENU':
            a = it[1]
            out.append(list(a[0]) if len(a) == 1 and isinstance(a[0], list) else list(a))
    return out


def soft(h, slot):
    h.tap(int((slot - 0.5) * 53.4), 230)


# every step of every example, all reached by soft keys and arrows
def s_all(ex):
    def f(h):
        h.choose(ex + 1)
        for sl in (1, 2, 3, 4, 5):
            soft(h, sl)
        h.press('Left')
        h.press('Right')
    return f


titles_ok = []
for ex in (1, 2, 3):
    hh, res, err = run(s_all(ex))
    ts = [U(p.lines()[0]) for p in hh.pages]
    titles_ok.append((ex, err, res, ts[:7]))
want = ['Step 1. The hypotheses', 'Step 1. The hypotheses', 'Step 2. Distribution and df',
        'Step 3. Critical value, decision rule', 'Step 4. Standard error and t obtained',
        'Step 5. Decision and conclusion', 'Step 4. Standard error and t obtained']
check('C1 each example opens on step 1; soft keys 1-5 and Left/Right step through; Esc quits with the result string: %s'
      % [(t[0], t[2]) for t in titles_ok],
      all(t[1] is None and t[3][:7] == want for t in titles_ok) and
      U(titles_ok[0][2]) == 'TTestLab: t(73) = -2.20, p = 0.031, two-tailed' and
      U(titles_ok[2][2]) == 'TTestLab: t(265.92) = -4.35, p < 0.001, two-tailed', titles_ok)
hh, _, _ = run(s_all(1))
p1 = hh.pages[0]
check('C1 step 1 of example 1: test, tails, alpha; H0 and H1; Table 11.1\'s numbers in two columns',
      has(p1, 'Pooled-variances t test, two-tailed, α = 0.050') and has(p1, 'H₀: μ₁ = μ₂') and
      has(p1, 'H₁: μ₁ ≠ μ₂   (they differ, either way)') and has(p1, 's₁ = 1.45') and has(p1, 'N₂ = 31') and
      has(p1, 'Hispanic') and has(p1, 'Non-Hispanic white'), lines(p1))
p3 = hh.pages[3]
check('C1 step 3 of example 1: the table row and the exact value, the either/or rule, the menu of steps',
      has(p3, 't table, row df = 60:  t crit = ±2.000') and has(p3, 'exact, df = 73:  t crit = ±1.993') and
      has(p3, 'Rule: if t obt > 1.993 or t obt < -1.993,') and menus_drawn(hh)[-1] == ['1 H', '2 df', '3 crit', '4 t', '5 end', 'Menu'],
      (lines(p3), menus_drawn(hh)[-1:]))
p5 = hh.pages[5]
check('C1 step 5 of example 1: reject, the direction in the samples\' names, the report line, d, the p legend',
      has(p5, 'REJECT H₀.') and has(p5, 'sample 1 (Hispanic) is lower on average.') and
      has(p5, 'Report t(73) = -2.20, p = 0.031, two-tailed') and has(p5, "Cohen's d = -0.51  (pooled s)") and
      has(p5, 'magenta area = p') and has(p5, 't obt = -2.20'), lines(p5))
hh, _, _ = run(s_all(2))
p3 = hh.pages[3]
check('C1 step 3 of example 2: one-tailed lower, "t crit = -2.132" from row 4, rule "if t obt < -2.132"',
      has(p3, 't table, row df = 4:  t crit = -2.132') and has(p3, 'Rule: if t obt < -2.132,'), lines(p3))
p1 = hh.pages[0]
check('C1 step 1 of example 2: H1 mu1 < mu2, Table 11.3\'s five pairs, and the source on screen',
      has(p1, 'H₁: μ₁ < μ₂   (a predicted direction)') and has(p1, '2.26') and has(p1, '1.85') and has(p1, '0.76') and
      has(p1, 'Outcome: assault rate, Census of Jails'),
      lines(p1))


hp_ = H()
put(hp_, ttTY=3, ttSRC=2, ttTL=0, ttAL=0.05, ttX1=list(range(1, 13)), ttX2=[x * 0.9 for x in range(1, 13)])
hp_.globals_['ttDV'] = 'a test outcome'
hp_.execute('tt_Calc()')
pq = page(hp_, 'tt_Step1()')
rows = [t for t in pq.texts if round(t.x) == 14 and t.text.isdigit()]
check('C1 step 1 with 12 pairs (beta 1a): 7 rows, "... and 5 more pairs" on the 8th, the outcome under them',
      len(rows) == 7 and has(pq, '... and 5 more pairs') and has(pq, 'Outcome: a test outcome'), lines(pq))
put(hp_, ttSRC=1, ttMD=0.5, ttSDv=1, ttNP=9)
pq = page(hp_, 'tt_Step1()')
check('C1 step 1, dependent samples typed as a summary: the outcome under the box', has(pq, 'Outcome: a test outcome'),
      lines(pq))

# the curve: the shaded rejection region matches t critical, column by column
hs = H()
hs.execute('tt_Example(1)')
hs.execute('tt_Calc()')
hs.reset_records()
hs.execute('tt_Step3()')
fills = {}
for it in hs.log:
    nm = it[0] if isinstance(it, (list, tuple)) else None
    if nm == 'LINE_P':
        args = it[1]
        if len(args) == 6 and args[1] == args[3] and args[1] >= 12 and args[1] <= 308:
            fills.setdefault(int(args[1]), set()).add(int(args[5]))
LRED, LBLU = 255 * 65536 + 200 * 256 + 200, 220 * 65536 + 232 * 256 + 255
cxr = max(4, tdist.isf(0.025, 73) + 0.8)
bad = []
for px, cs in fills.items():
    if not cs & {LRED, LBLU}:
        continue                                         # an axis tick only: the curve is under 1 px high here
    x = -cxr + (px - 12) / 296 * 2 * cxr
    want_c = LRED if abs(x) > tdist.isf(0.025, 73) else LBLU
    if want_c not in cs:
        bad.append((px, round(x, 3), cs))
nfill = len([1 for cs in fills.values() if cs & {LRED, LBLU}])
nred = len([1 for cs in fills.values() if LRED in cs])
check('C2 step 3\'s curve: %d pixel columns filled (%d of them pale red), pale red exactly where |t| > t crit '
      '(two-tailed), pale blue elsewhere' % (nfill, nred), nfill >= 200 and nred >= 40 and not bad, bad[:5])

# the flowchart
fl = []
for name, taps, want_ty in (
        ('Yes, Yes (boxes)', [(90, 71), (40, 133), (290, 230)], 1),
        ('Yes, No (boxes)', [(90, 71), (140, 133), (290, 230)], 2),
        ('No (box)', [(230, 71), (290, 230)], 3),
        ('Yes, No (soft keys)', [(26, 230), (80, 230), (290, 230)], 2),
        ('Yes, Back, No, OK', [(90, 71), (134, 230), (230, 71), (290, 230)], 3),
        ('OK too early, then Yes, Yes', [(290, 230), (90, 71), (290, 230), (40, 133), (290, 230)], 1)):
    hh = H()
    for x, y in taps:
        hh.tap(x, y)
    hh.execute('tt_Settle()')
    got = hh.execute('tt_Flow()')
    fl.append((name, got))
check('C3 the flowchart (Figure 11.2): tapped boxes and soft keys give pooled / separate / dependent; Back undoes; '
      'OK waits for an answer: %s' % fl, [f[1] for f in fl] == [1, 2, 3, 2, 3, 1], fl)
hh = H()
hh.press('Esc')
check('C3 Esc leaves the flowchart (returns 0)', hh.execute('tt_Flow()') == 0)
hh = H()
hh.tap(90, 71)
hh.press('Esc')
hh.reset_records()
hh.execute('tt_Flow()')
fp = hh.pages[-1]
check('C3 the flowchart\'s texts and soft keys: both questions, three tests, the hint about Levene\'s test',
      has(fp, '1. Are the samples independent?') and has(fp, '2. Are the variances equal?') and
      has(fp, 'Pooled t') and has(fp, 'Separate t') and has(fp, 'Dependent-samples t') and
      has(fp, "Levene's test (SPSS) on the raw scores.") and menus_drawn(hh)[-1] == ['Yes', 'No', 'Back', '', '', 'OK'],
      (lines(fp), menus_drawn(hh)[-1:]))


# full flows from the start: flowchart -> data -> tails -> alpha
def s_flow_ind(h):
    h.choose(1)
    for x, y in [(90, 71), (140, 133), (290, 230)]:
        h.tap(x, y)
    h.choose(1)                                          # type the numbers
    h.answer({'ttM1': 4.8185, 'ttS1': 3.28798, 'ttN1': 270, 'ttM2': 6.4247, 'ttS2': 3.74872, 'ttN2': 146})
    h.choose(3)                                          # one-tailed mu1 > mu2
    h.choose(2)                                          # alpha .05


hh, res, err = run(s_flow_ind)
pr = stats.ttest_ind_from_stats(4.8185, 3.28798, 270, 6.4247, 3.74872, 146, equal_var=False, alternative='greater')
check('C4 flowchart -> separate -> typed numbers -> one-tailed mu1 > mu2 -> alpha .05: "%s" (p %.4f)'
      % (U(res or ''), pr.pvalue), err is None and U(res) == 'TTestLab: t(265.92) = -4.35, p > 0.999, one-tailed' and
      g(hh, 'ttTL') == 1 and g(hh, 'ttAL') == 0.05, (err, res))
inp = hh.inputs[0]
check('C4 the form: six plain labels with help lines', inp.labels == ['Mean 1:', 'SD 1:', 'N 1:', 'Mean 2:', 'SD 2:',
                                                                      'N 2:'] and len(inp.helps) == 6, inp.labels)


def s_flow_raw(h):
    h.choose(1)
    for x, y in [(90, 71), (40, 133), (290, 230)]:
        h.tap(x, y)
    h.choose(2)                                          # raw scores in D1 and D2
    h.choose(1)                                          # two-tailed
    h.choose(4)                                          # alpha .02


d1 = [12, 15, 11, 18, 14, 16, 13]
d2 = [10, 9, 14, 11, 12, 8, 13, 10, 9, 11]
hh, res, err = run(s_flow_raw, app={'D1': d1, 'D2': d2})
rr = stats.ttest_ind(d1, d2, equal_var=True)
check('C5 raw scores in D1 and D2 (7 and 10 scores, pooled, two-tailed, alpha .02): t %.4f (SciPy %.4f), p %.4f, '
      'names "D1"/"D2"' % (g(hh, 'ttT'), rr.statistic, g(hh, 'ttP')),
      err is None and rel(g(hh, 'ttT'), rr.statistic) < 1e-12 and rel(g(hh, 'ttP'), rr.pvalue) < 1e-9 and
      g(hh, 'ttG1') == 'D1' and g(hh, 'ttAL') == 0.02, (err, res))


def s_flow_pairs(h):
    h.choose(1)
    h.tap(230, 71)
    h.tap(290, 230)
    h.choose(1)                                          # pairs in D1 and D2
    h.choose(2)                                          # one-tailed mu1 < mu2
    h.choose(2)


hh, res, err = run(s_flow_pairs, app={'D1': [1.30, 1.25, 0.86, 0.94, 2.26], 'D2': [1.00, 0.76, 0.99, 1.10, 1.85]})
check('C6 pairs from D1 and D2 reproduce example 2 (t %.4f, df 4)' % g(hh, 'ttT'),
      err is None and rel(g(hh, 'ttT'), r2.statistic) < 1e-12 and g(hh, 'ttDF') == 4, (err, res))


def s_flow_pairsum(h):
    h.choose(1)
    h.tap(230, 71)
    h.tap(290, 230)
    h.choose(2)                                          # type the mean and SD of the differences
    h.answer({'dm': 0.182, 'dsd': 0.30622, 'dn': 5})
    h.choose(1)
    h.choose(3)


hh, res, err = run(s_flow_pairsum)
check('C6 dependent samples from typed x-bar D, sD and N pairs: t %.4f, df 4; step 1 shows the summary'
      % g(hh, 'ttT'), err is None and abs(g(hh, 'ttT') - ref_t) < 1e-12 and
      any('N pairs = 5' in U(x) for p in hh.pages for x in p.lines()), (err, res))

# refusals
ref = []
for name, sc, app, want in (
        ('D1 empty', s_flow_raw, None, 'Put sample 1 in D1 and sample 2 in D2'),
        ('D1 one score', s_flow_raw, {'D1': [3], 'D2': [1, 2]}, 'Put sample 1 in D1 and sample 2 in D2'),
        ('pairs unequal', s_flow_pairs, {'D1': [1, 2, 3], 'D2': [1, 2]}, 'Put the pairs in D1 and D2')):
    hh, res, err = run(sc, app=app)
    mb = [U(' '.join(m.lines)) for m in hh.msgboxes]
    ref.append((name, err, res, mb[:1]))
check('C7 D1/D2 missing, too short or unequal for pairs: a box says what to do, and the program ends cleanly: %s'
      % [(r[0], r[2]) for r in ref], all(r[1] is None and r[3] and want_ in r[3][0]
                                          for r, (_, _, _, want_) in zip(ref, (
                                              (0, 0, 0, 'Put sample 1 in D1 and sample 2 in D2'),
                                              (0, 0, 0, 'Put sample 1 in D1 and sample 2 in D2'),
                                              (0, 0, 0, 'Put the pairs in D1 and D2')))), ref)
bad_inputs = []
for name, vals, msg in (
        ('N 1', {'ttN1': 1}, 'Each group needs N of at least 2.'),
        ('SD < 0', {'ttS1': -1}, 'An SD cannot be negative.'),
        ('both SD 0', {'ttS1': 0, 'ttS2': 0}, 'Both SDs are 0'),):
    def sc(h, vals=vals):
        h.choose(1)
        for x, y in [(90, 71), (40, 133), (290, 230)]:
            h.tap(x, y)
        h.choose(1)
        base = {'ttM1': 5, 'ttS1': 2, 'ttN1': 10, 'ttM2': 4, 'ttS2': 2, 'ttN2': 10}
        base.update(vals)
        h.answer(base)
        h.choose(1)
        h.choose(3)
        h.choose(7)                                      # the menu that follows: Quit
    hh, res, err = run(sc)
    mb = [U(' '.join(m.lines)) for m in hh.msgboxes]
    bad_inputs.append((name, err, mb, [d.title for d in hh.dialogs][-1:]))
check('C7 numbers that give no t (N < 2, SD < 0, both SDs 0): the reason in a box, then the menu: %s'
      % [(b[0], b[2]) for b in bad_inputs],
      all(b[1] is None and b[2] and m in b[2][0] and b[3] == ['TTestLab']
          for b, m in zip(bad_inputs, ('Each group needs', 'cannot be negative', 'Both SDs are 0'))), bad_inputs)
hh, res, err = run(lambda h: (h.choose(1), [h.tap(230, 71), h.tap(290, 230)], h.choose(2),
                              h.answer({'dm': 0.5, 'dsd': 0, 'dn': 5}), h.choose(1), h.choose(3), h.choose(7)))
check('C7 dependent samples with sD = 0: "Every pair differs by the same amount (sD = 0): there is no t."',
      err is None and any('sD = 0' in ' '.join(m.lines) for m in hh.msgboxes), (err, [m.lines for m in hh.msgboxes]))
over5 = [m.lines for hx in (hh,) for m in hx.msgboxes if m.over_five]
check('C7 no message box runs past 5 lines (Lessons Learned s3)', not over5, over5)


# the menu: Tails and alpha, Choose the test (pooled <-> separate keeps the numbers; to dependent asks for new ones,
# and a cancelled form keeps the old test), Examples, Help, Quit
def s_menu(h):
    h.choose(2)                                          # example 1
    soft(h, 6)
    h.choose('Tails and')
    h.choose(2)                                          # one-tailed mu1 < mu2
    h.choose(3)                                          # alpha .025
    soft(h, 6)
    h.choose('Choose the test')
    h.tap(90, 71)
    h.tap(140, 133)
    h.tap(290, 230)                                      # -> separate, same numbers
    h.choose(1)                                          # tails: two-tailed
    h.choose(3)                                          # .05
    soft(h, 6)
    h.choose('Choose the test')
    h.tap(230, 71)
    h.tap(290, 230)                                      # -> dependent
    h.choose(0)                                          # the data menu cancelled: keep the separate test
    soft(h, 6)
    h.choose('Quit')


hh, res, err = run(s_menu)
check('C8 the menu: tails/alpha changes the test in place; pooled -> separate keeps the numbers; a cancelled switch '
      'to dependent keeps the separate test; Quit: "%s"' % U(res or ''),
      err is None and g(hh, 'ttTY') == 2 and g(hh, 'ttM1') == 15.89 and g(hh, 'ttTL') == 0 and
      U(res) == 'TTestLab: t(72.44) = -2.30, p = 0.024, two-tailed', (err, res, [d.title for d in hh.dialogs]))
hh, res, err = run(lambda h: (h.choose(5), h.press('Enter'), h.press('Enter')))
hp = [lines(p) for p in hh.pages[:2]]
check('C9 help: two pages (keys; the numbers, with the Inference app as a check), then example 1',
      err is None and len(hp) == 2 and 'TTestLab help 1/2: keys' in hp[0][0] and
      any('Check on the Prime: Inference app, Hyp. test,' in x for x in hp[1]) and
      any('Teaching aid; not for clinical or legal use.' in x for x in hp[0]), hp)
hh, res, err = run(lambda h: h.choose(0))
check('C9 the start menu cancelled: "TTestLab: cancelled"', err is None and res == 'TTestLab: cancelled', (err, res))

# ===================================================================== E. pooled or separate?
print('=== E. the "Pooled or separate?" page')
cmp_ = []
for name, kv, want in (
        ('N1 = N2', dict(ttN1=20, ttN2=20, ttS1=1, ttS2=4), 'N₁ = N₂: the same t either way; only df differs.'),
        ('s1 = s2', dict(ttN1=10, ttN2=40, ttS1=2, ttS2=2), 's₁ = s₂: the same t either way; only df differs.'),
        ('small n, big s', dict(ttN1=10, ttN2=40, ttS1=4, ttS2=1), 'The SMALLER group has the LARGER SD: the pooled'),
        ('big n, big s', dict(ttN1=10, ttN2=40, ttS1=1, ttS2=4), 'The LARGER group has the LARGER SD: the pooled')):
    hh = H()
    put(hh, ttTY=1, ttTL=0, ttAL=0.05, ttM1=6, ttM2=5, **kv)
    hh.execute('tt_Calc()')
    hh.press('Enter')
    hh.reset_records()
    hh.execute('tt_Compare()')
    pc = hh.pages[-1]
    tp = hh.execute('tt_Ind(1)')
    ts = hh.execute('tt_Ind(2)')
    cmp_.append((name, has(pc, want), round(tp[1], 6), round(ts[1], 6)))
check('E1 the page says why the tests agree or differ for each mix of N and SD: %s' % cmp_,
      all(c[1] for c in cmp_) and cmp_[0][2] == cmp_[0][3] and cmp_[1][2] == cmp_[1][3] and
      cmp_[2][2] != cmp_[2][3], cmp_)
# the claim, simulated: type I error of the pooled test at alpha .05
rs = np.random.default_rng(1031)
sims = {}
for name, (n1, s1, n2, s2) in (('smaller group, larger SD', (10, 4, 40, 1)), ('larger group, larger SD', (10, 1, 40, 4))):
    x = rs.normal(0, s1, (20000, n1))
    y = rs.normal(0, s2, (20000, n2))
    pp = stats.ttest_ind(x, y, axis=1, equal_var=True).pvalue
    pwl = stats.ttest_ind(x, y, axis=1, equal_var=False).pvalue
    sims[name] = (round(float(np.mean(pp < 0.05)), 3), round(float(np.mean(pwl < 0.05)), 3))
check('E2 the claims, simulated (20,000 pairs of samples each, H0 true, alpha .05; pooled, separate): %s -- pooled '
      'rejects too often in the first, too seldom in the second; separate stays near .05' % sims,
      sims['smaller group, larger SD'][0] > 0.10 and sims['larger group, larger SD'][0] < 0.02 and
      all(abs(v[1] - 0.05) < 0.01 for v in sims.values()), sims)
hh = H()
put(hh, ttTY=3)
hh.execute('tt_Compare()')
check('E3 dependent samples: the page explains instead (one SD, of the differences)',
      any('INDEPENDENT samples' in ' '.join(m.lines) for m in hh.msgboxes), [m.lines for m in hh.msgboxes])

# ===================================================================== F. a finger left on OK
print('=== F. a finger still on a form\'s OK')


def hold_after(h, which, x, y, n=3):
    orig = h._dialog_closed
    st = {'k': 0}

    def patched(ok):
        orig(ok)
        st['k'] += 1
        if st['k'] == which:
            h._finger = [[float(x), float(y), float(x), float(y), 0.0]] + \
                        [[float(x), float(y), float(x), float(y), 2.0]] * n
    h._dialog_closed = patched


def s_edit_held(h):
    h.choose(2)                                          # example 1 (dialog 1)
    soft(h, 6)
    h.choose('Edit the numbers')                         # dialog 2
    h.choose(1)                                          # dialog 3: type the numbers
    h.answer(ACCEPT)                                     # dialog 4: the form, OK tapped ...
    hold_after(h, 4, 290, 230)                           # ... and the finger still on it (= Menu, slot 6)


hh, res, err = run(s_edit_held)
menus = [d.title for d in hh.dialogs].count('TTestLab')
check('F1 Menu > Edit the numbers > OK with the finger left on OK (soft-key slot 6, Menu): the menu does not open '
      'again (%d menu, %s)' % (menus, err), err is None and menus == 1, [d.title for d in hh.dialogs])
ctl = SRC.replace(' tt_Drain();\n tt_TDrain();\nEND;', ' tt_Drain();\nEND;', 1)
cpath = os.path.join(tempfile.mkdtemp(), 'TTestLab_ctl.txt')
open(cpath, 'w', encoding='utf-8').write(ctl)
hh, res, err = run(s_edit_held, path=cpath)
menus_c = [d.title for d in hh.dialogs].count('TTestLab')
check('F1 control: a copy whose tt_Settle drains keys only opens the menu a second time (%d), as PowerViz v2.5h did '
      'on Roger\'s calculator' % menus_c, ctl != SRC and menus_c >= 2, [d.title for d in hh.dialogs])

# ===================================================================== G. static
print('=== G. static checks')
code = [ln.split('//')[0] for ln in SRC.split('\n')]
ne = [i + 1 for i, c in enumerate(code) if '!=' in c]
routines = re.findall(r'^LOCAL\s+(\w+)\s*\(', SRC, re.M)
filevars = []
for ln in SRC.split('\n'):
    m = re.match(r'^LOCAL\s+(.*?);', ln)
    if m and '(' not in m.group(1).split(':=')[0]:
        filevars += [v.split(':=')[0].strip() for v in m.group(1).split(',')]
exports = re.findall(r'^EXPORT\s+(\w+)', SRC, re.M)
check('G1 no "!=" in the code (Lessons Learned: "<>" on the device); %d routines, all tagged tt_; %d file-level '
      'variables, all tagged tt; one EXPORT, TTESTLAB' % (len(routines), len(filevars)),
      not ne and routines and all(r.startswith('tt_') for r in routines) and
      all(v.startswith('tt') for v in filevars) and exports == ['TTESTLAB'], (ne, routines, filevars, exports))
VERIFIED = set('χ²√≥≤≠±×→∞αβμσφθρλ') | {chr(8320), chr(8321), chr(8322)}
glyphs = sorted(set(c for ln in code for c in ln if ord(c) > 126))
check('G1 only verified glyphs in the code\'s strings (Lessons Learned s5): %s' % ''.join(glyphs),
      set(glyphs) <= VERIFIED, sorted(set(glyphs) - VERIFIED))
check('G1 every routine is defined before its first use (no forward references)',
      all(SRC.find(r + '(') == SRC.find('LOCAL ' + r + '(') + 6 for r in routines),
      [r for r in routines if SRC.find(r + '(') != SRC.find('LOCAL ' + r + '(') + 6])

# ===================================================================== D. layout
print('=== D. layout (text_overlap_v1 over every screen above)')
rep = OV.report()
tag = [t for t in rep if t.startswith('TTestLab_beta1a')]
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
check('D1 no firm overlap, frame straddle or overrun on any TTestLab screen drawn (%s)' % (tag[:1]),
      bool(tag) and not firm, firm[:8])

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for x in FAIL:
    print('  FAILED: ' + x)
sys.exit(1 if FAIL else 0)
