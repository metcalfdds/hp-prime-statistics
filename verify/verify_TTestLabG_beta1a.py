#!/usr/bin/env python3
"""verify_TTestLabG_beta1a.py -- checks TTestLabG beta 1a (1 Nov 2026: rebuilt from TTestLab beta 1c, the monkey test's
two fixes; beta 1 31 Oct 2026, night), the GENERAL version of TTestLab: the
same five-step pooled, separate (Welch) and dependent-samples t tests, built from TTestLab beta 1c by make_tlg1_v2.py,
with separate variances the default, t critical exact for the df (a printed table only a note), the hand shortcut df
for separate variances, a p that rounds to alpha given its 4 significant digits, raw-score means to 4 significant
digits, no lecture references, and four examples: Darwin's 1876 Zea mays pairs, the 1970 draft lottery (Selective
Service), age at arrest (JDCC) and matched jails (Census of Jails).  This script is TTestLab beta 1b's (84 checks,
every cancel and refusal path) with its names changed and its lecture-specific checks replaced, plus section M from
verify_TTestLab_beta1c.py.

A  the arithmetic against SciPy: pooled and separate SE, t and df over a grid of equal / unequal N and SD (and SDs
   of 1E-200 and 1E200); paired t from raw pairs and from summary numbers; p in all three tails; t critical for every
   column of the t table, integer and fractional df, and its bisection fallback; Cohen's d.  A5: step 3's printed-
   table note (whole df past 30, fractional df, none at 30 and below) and step 2's hand-shortcut df and t crit.
B  the four examples against SciPy and NumPy (the draft numbers checked as the numbers 1-366 and against the
   published facts), with their screens; the near-alpha note both ways.
C  the screens: each step's texts for each example; the flowchart (taps on its boxes and its soft keys, Back, OK,
   Esc); the forms; D1 and D2; the refusals; the menu; help.
E  the "Pooled or separate?" page: the same t when N1 = N2 or s1 = s2; which way the pooled test errs (and a
   simulation of its type I error rate that backs the claim).
F  a finger still on a form's OK when the form closes is waited out (tz_Settle), not read as a tap on Menu; a copy
   without the finger drain reproduces the fault.
R  TTestLab's review findings (REVIEW2_TTestLab_beta1a.md), carried into the general version: tails and alpha change
   together or not at all; a refused D1/D2 read or a cancelled form leaves the source, the names and the example as
   they were; "Pooled or separate?" refuses numbers that gave no t; p never prints 0.000; t obt to 3 decimals on the
   decision line; a typed N is whole; t crit past the window; a negative sD; the pairs guard; help's "sample 1"; the
   pairs' decimals; step 4's rows; Help from the start menu returns to it.
N  the general version itself: separate variances the default; the menus; no lecture, figure or SPSS-output words on
   any screen.
M  the monkey test's findings (1 Nov 2026: 1,000 random runs of beta 1, 13 broken), one check each, every one failing
   on beta 1 (read from ../programs or from git history): every form field takes a real number only ({name,[0]});
   a value of 1E50 or more in size in D1 or D2 is refused with a box that names the list and the value, and nothing
   changes; 9.99E49 is accepted; a typed number of 1E50 or more gets a sentence and the menu; a typed N over
   1,000,000 is refused (the Prime's t distribution loses its digits at a huge df); the largest numbers accepted draw
   all five steps for all three tests, with t against SciPy.
G  static: no "!=", every routine tagged tz_, every file-level variable tagged tz, one EXPORT, TTESTLABG.
D  layout: text_overlap_v1's recorder over every screen drawn above: no firm overlap, frame straddle or overrun.

Needs the PPL harness ppl_run_v3e.py and text_overlap_v1.py (in ./tools, ../tools, this folder, or $TTL_TOOLS),
hp-prime-kit ($HPKIT), SciPy, NumPy.
Run:  python3 verify_TTestLabG_beta1.py [TTestLabG_beta1.txt]     (exit code 0 = all passed)
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
from ppl_run_v3e import Harness, ACCEPT, CANCEL  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402

PROG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'TTestLabG_beta1a.txt')
if not os.path.exists(PROG):
    PROG = os.path.join(HERE, '..', 'programs', 'TTestLabG_beta1a.txt')
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
    h.execute('tz_Init()')
    return h


def put(h, **kv):
    for k, v in kv.items():
        h.globals_[k] = [float(x) for x in v] if isinstance(v, (list, tuple)) else float(v)


def g(h, k):
    return h.globals_[k]


def calc(h, **kv):
    put(h, **kv)
    h.execute('tz_Calc()')
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
            put(h, tzM1=m1, tzS1=s1, tzN1=n1, tzM2=m2, tzS2=s2, tzN2=n2)
            for pk, ev in ((1, True), (2, False)):
                se, tt, df, sp_ = h.execute('tz_Ind(%d)' % pk)
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
    put(h, tzM1=15.89 * sc, tzS1=1.45 * sc, tzN1=44, tzM2=16.57 * sc, tzS2=1.11 * sc, tzN2=31)
    for pk in (1, 2):
        se, tt, df, _ = h.execute('tz_Ind(%d)' % pk)
        put(h, tzM1=15.89, tzS1=1.45, tzN1=44, tzM2=16.57, tzS2=1.11, tzN2=31)
        se0, tt0, df0, _ = h.execute('tz_Ind(%d)' % pk)
        put(h, tzM1=15.89 * sc, tzS1=1.45 * sc, tzN1=44, tzM2=16.57 * sc, tzS2=1.11 * sc, tzN2=31)
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
        put(h, tzTY=3, tzSRC=2, tzX1=list(a), tzX2=list(b))
        for tl, alt in ((0, 'two-sided'), (-1, 'less'), (1, 'greater')):
            put(h, tzTL=tl, tzAL=0.05)
            h.execute('tz_Calc()')
            r = stats.ttest_rel(a, b, alternative=alt)
            d = a - b
            e = max(rel(g(h, 'tzT'), r.statistic), rel(g(h, 'tzP'), r.pvalue), abs(g(h, 'tzDF') - (n - 1)),
                    rel(g(h, 'tzSDv'), np.std(d, ddof=1)), rel(g(h, 'tzMD'), d.mean()),
                    rel(g(h, 'tzD'), d.mean() / np.std(d, ddof=1)))
            cnt += 1
            if e > pw[0]:
                pw = [e, (n, rep, tl)]
check('A2 dependent samples from pairs in D1/D2 (tz_Pairs): x-bar D, sD, t, df = N - 1, p in all three tails and '
      'Cohen\'s d (mean / sD) equal SciPy\'s ttest_rel, %d cases, N from 2 to 200 (worst %.1e)' % (cnt, pw[0]),
      pw[0] < 1e-9, pw)
put(h, tzTY=3, tzSRC=1, tzMD=0.182, tzSDv=0.30622, tzNP=5, tzTL=0, tzAL=0.05)
h.execute('tz_Calc()')
ref_t = 0.182 / (0.30622 / math.sqrt(5))
check('A2 dependent samples from the mean and SD of the differences: t = %.6f (by hand %.6f), df 4, SE sD/sqrt(N)'
      % (g(h, 'tzT'), ref_t), rel(g(h, 'tzT'), ref_t) < 1e-12 and g(h, 'tzDF') == 4)

# p values, independent, three tails
pe = [0.0, None]
for (m1, s1, n1, m2, s2, n2) in ((15.89, 1.45, 44, 16.57, 1.11, 31), (4.8185, 3.28798, 270, 6.4247, 3.74872, 146),
                                  (5, 2, 8, 4, 6, 20), (5, 2, 8, 5, 6, 20)):
    for ty, ev in ((1, True), (2, False)):
        for tl, alt in ((0, 'two-sided'), (-1, 'less'), (1, 'greater')):
            calc(h, tzTY=ty, tzSRC=1, tzTL=tl, tzAL=0.05, tzM1=m1, tzS1=s1, tzN1=n1, tzM2=m2, tzS2=s2, tzN2=n2)
            r = stats.ttest_ind_from_stats(m1, s1, n1, m2, s2, n2, equal_var=ev, alternative=alt)
            e = rel(g(h, 'tzP'), r.pvalue)
            if e > pe[0]:
                pe = [e, (m1, n1, ty, tl)]
check('A3 p for H1 mu1 != mu2, mu1 < mu2 and mu1 > mu2 (lower tails only), pooled and separate, equals SciPy '
      '(worst %.1e); t = 0 gives p = 1 two-tailed, not 2 x 0.5 rounded' % pe[0], pe[0] < 1e-9 and
      abs(g(h, 'tzP') - 0.5) < 1 and True, pe)
calc(h, tzTY=1, tzTL=0, tzM1=5, tzM2=5, tzS1=2, tzS2=2, tzN1=10, tzN2=10)
check('A3 equal means: t = 0, p = %s two-tailed' % g(h, 'tzP'), g(h, 'tzT') == 0 and g(h, 'tzP') == 1)

# t critical
ONE = [0.10, 0.05, 0.025, 0.01, 0.005, 0.0005]
TWO = [0.20, 0.10, 0.05, 0.02, 0.01, 0.001]
ce = [0.0, None]
ncrit = 0
for df in (1, 2, 4, 7.5, 30, 60, 73, 265.924, 1000):
    for tl, alist in ((0, TWO), (-1, ONE), (1, ONE)):
        for al in alist:
            put(h, tzTL=tl, tzAL=al)
            v = h.execute('tz_Crit(%r)' % df)
            ref = tdist.isf(al / 2 if tl == 0 else al, df)
            ncrit += 1
            if rel(v, ref) > ce[0]:
                ce = [rel(v, ref), (df, tl, al, v, ref)]
check('A4 t critical (-STUDENT_ICDF of a lower tail, checked by STUDENT_CDF) equals SciPy for every column of the '
      'table, both tails, df 1 to 1000 and fractional df: %d values, worst %.1e' % (ncrit, ce[0]), ce[0] < 1e-10, ce)
# the fallback: STUDENT_ICDF unavailable (renamed so that it raises inside IFERR)
fb_src = SRC.replace('cv := -STUDENT_ICDF(cdf,ca);', 'cv := -STUDENT_ICDFX(cdf,ca);')
fb_path = os.path.join(tempfile.mkdtemp(), 'TTestLabG_fallback.txt')
open(fb_path, 'w', encoding='utf-8').write(fb_src)
hf = H(path=fb_path)
fe = [0.0, None]
for df in (1, 4, 7.5, 73, 265.924):
    for tl, alist in ((0, TWO), (1, ONE)):
        for al in alist:
            put(hf, tzTL=tl, tzAL=al)
            v = hf.execute('tz_Crit(%r)' % df)
            ref = tdist.isf(al / 2 if tl == 0 else al, df)
            if rel(v, ref) > fe[0]:
                fe = [rel(v, ref), (df, tl, al, v, ref)]
check('A4 the fallback (STUDENT_ICDF fails inside IFERR, bisection on STUDENT_CDF, as CICatcher\'s cqTCrit): '
      'the same t critical to %.1e (df 1 at alpha .0005: %.3f)' % (fe[0], tdist.isf(0.0005, 1)),
      fb_src != SRC and fe[0] < 1e-9, fe)

# the printed table as a note on step 3 (the general version claims no row: the books' tables differ past df 30)
nt = {}
for label, kv, want, absent in (
        ('pooled, df 73', dict(tzTY=1, tzSRC=1, tzM1=15.89, tzS1=1.45, tzN1=44, tzM2=16.57, tzS2=1.11, tzN2=31),
         ['Printed table without row 73?  Take the next', 'smaller row it lists (its t crit is larger).'], []),
        ('separate, df 72.44', dict(tzTY=2, tzSRC=1, tzM1=15.89, tzS1=1.45, tzN1=44, tzM2=16.57, tzS2=1.11, tzN2=31),
         ['Printed table?  Round df down to 72; if the', 'table lacks that row, take the next smaller.'], []),
        ('pairs, df 4', dict(tzTY=3, tzSRC=1, tzMD=0.182, tzSDv=0.30622, tzNP=5),
         [], ['Printed table']),
        ('pairs, df 30', dict(tzTY=3, tzSRC=1, tzMD=0.182, tzSDv=0.30622, tzNP=31),
         [], ['Printed table']),
        ('pairs, df 31', dict(tzTY=3, tzSRC=1, tzMD=0.182, tzSDv=0.30622, tzNP=32),
         ['Printed table without row 31?  Take the next'], [])):
    calc(h, tzTL=0, tzAL=0.05, **kv)
    pg = page(h, 'tz_Step3()')
    nt[label] = (all(has(pg, w) for w in want) and not any(has(pg, w) for w in absent), lines(pg))
check('A5 step 3\'s printed-table note: a whole df past 30 takes the next smaller row; a fractional df is rounded '
      'down first; df 30 and below: no note (%s)' % ', '.join(nt),
      all(v[0] for v in nt.values()), [(k, v[1]) for k, v in nt.items() if not v[0]])
calc(h, tzTY=1, tzSRC=1, tzTL=0, tzAL=0.05, tzM1=15.89, tzS1=1.45, tzN1=44, tzM2=16.57, tzS2=1.11, tzN2=31)
pg = page(h, 'tz_Step3()')
check('A5 step 3 gives the exact t crit for the df, nothing from a table row: "t crit = ±1.993   (exact, for df = '
      '73)"', has(pg, 't crit = ±1.993   (exact, for df = 73)') and not has(pg, 't table, row'), lines(pg))
# the hand shortcut for separate variances on step 2: df = the smaller N - 1, and its (larger) t crit
sh = []
for n1, n2, tl, al in ((44, 31, 0, 0.05), (270, 146, 0, 0.05), (5, 1000, 1, 0.01), (3, 7, -1, 0.025)):
    calc(h, tzTY=2, tzSRC=1, tzTL=tl, tzAL=al, tzM1=10, tzS1=2, tzN1=n1, tzM2=9, tzS2=3, tzN2=n2)
    pg = page(h, 'tz_Step2()')
    k = min(n1, n2) - 1
    cv = tdist.isf(al / 2 if tl == 0 else al, k)
    cs = ('±' if tl == 0 else '') + ('%.3f' % (-cv if tl < 0 else cv))
    sh.append((n1, n2, has(pg, 'By hand: df = the smaller of N₁-1, N₂-1 = %d,' % k) and
               has(pg, 't crit = %s: larger, so a safer test.' % cs) and
               cv >= tdist.isf(al / 2 if tl == 0 else al, g(h, 'tzDF')), cs, lines(pg)))
check('A5 step 2, separate variances: the hand shortcut df (the smaller N - 1) and its t crit, larger than at '
      'Welch\'s df, in four cases (both tails and one-tailed either way): %s' % [(x[0], x[1], x[3]) for x in sh],
      all(x[2] for x in sh), [x for x in sh if not x[2]])

# ===================================================================== B. the examples
print('=== B. the four examples')
h = H()
# the draft numbers: the numbers 1-366, once each, and the published facts (Fienberg 1971): 1 went to September 14,
# 2 to April 24, 366 to June 8
dr1 = [int(x) for x in h.execute('tz_Draft(1)')]
dr2 = [int(x) for x in h.execute('tz_Draft(2)')]
allr = dr1 + dr2
check('B0 the draft numbers: 182 dates Jan-Jun, 184 Jul-Dec, the numbers 1-366 once each; 1 on September 14 (day '
      '258), 2 on April 24 (day 115), 366 on June 8 (day 160)',
      len(dr1) == 182 and len(dr2) == 184 and sorted(allr) == list(range(1, 367)) and allr[257] == 1 and
      allr[114] == 2 and allr[159] == 366, (len(dr1), len(dr2), allr[257], allr[114], allr[159]))

# B1 Darwin's Zea mays (dependent, two-tailed .05)
DX = [23.5, 12, 21, 22, 19.125, 21.5, 22.125, 20.375, 18.25, 21.625, 23.25, 21, 22.125, 23, 12]
DY = [17.375, 20.375, 20, 20, 18.375, 18.625, 18.625, 15.25, 16.5, 18, 16.25, 18, 12.75, 15.5, 18]
FISHER = [49, -67, 8, 16, 6, 23, 28, 41, 14, 29, 56, 24, 75, 60, -48]
h.execute('tz_Example(1)')
h.execute('tz_Calc()')
rd = stats.ttest_rel(DX, DY)
check('B1 Darwin\'s pairs (Darwin 1876): 8 x the differences are Fisher\'s 1935 figures %s' % FISHER,
      [round(8 * (x - y)) for x, y in zip(DX, DY)] == FISHER and list(g(h, 'tzX1')) == DX and
      list(g(h, 'tzX2')) == DY)
check('B1 Darwin: t %.4f (SciPy %.4f), df 14, t crit %.4f, reject; p %.5f (SciPy %.5f); d %.3f'
      % (g(h, 'tzT'), rd.statistic, g(h, 'tzTC'), g(h, 'tzP'), rd.pvalue, g(h, 'tzD')),
      rel(g(h, 'tzT'), rd.statistic) < 1e-12 and g(h, 'tzDF') == 14 and g(h, 'tzREJ') == 1 and
      rel(g(h, 'tzP'), rd.pvalue) < 1e-9 and abs(g(h, 'tzTC') - tdist.isf(0.025, 14)) < 1e-12 and
      g(h, 'tzTY') == 3 and g(h, 'tzTL') == 0)
p1 = page(h, 'tz_Step1()')
check('B1 Darwin step 1: the first 7 pairs with 3 decimals each column (19.125), "... and 8 more pairs", the names, '
      'the outcome and its source',
      has(p1, 'Crossed (x₁)') and has(p1, 'Self (x₂)') and has(p1, '23.500') and has(p1, '17.375') and
      has(p1, '... and 8 more pairs') and has(p1, 'Outcome: plant height (inches), Darwin 1876'), lines(p1))
p5 = page(h, 'tz_Step5()')
check('B1 Darwin step 5: reject; p rounds to alpha at 3 decimals, so its 4 significant digits too: "(p = 0.04970: '
      'just below α = 0.050.)"; Report t(14) = 2.15, p = 0.050',
      has(p5, 'REJECT H₀.') and has(p5, '(p = 0.04970: just below α = 0.050.)') and
      has(p5, 'Report t(14) = 2.15, p = 0.050, two-tailed') and has(p5, 't obt = 2.148 is beyond t crit = ±2.145:'),
      lines(p5))

# B2 the 1970 draft lottery (separate, two-tailed .05)
h.execute('tz_Example(2)')
h.execute('tz_Calc()')
rw = stats.ttest_ind(dr1, dr2, equal_var=False)
check('B2 the draft lottery: means %.4f and %.4f, SDs %.4f and %.4f (NumPy %.4f, %.4f, %.4f, %.4f), N 182 and 184'
      % (g(h, 'tzM1'), g(h, 'tzM2'), g(h, 'tzS1'), g(h, 'tzS2'), np.mean(dr1), np.mean(dr2),
         np.std(dr1, ddof=1), np.std(dr2, ddof=1)),
      rel(g(h, 'tzM1'), np.mean(dr1)) < 1e-12 and rel(g(h, 'tzM2'), np.mean(dr2)) < 1e-12 and
      rel(g(h, 'tzS1'), np.std(dr1, ddof=1)) < 1e-12 and rel(g(h, 'tzS2'), np.std(dr2, ddof=1)) < 1e-12 and
      g(h, 'tzN1') == 182 and g(h, 'tzN2') == 184)
check('B2 the draft lottery, separate variances: t %.4f (SciPy %.4f), df %.3f (SciPy %.3f), reject; p %.2e (SciPy '
      '%.2e)' % (g(h, 'tzT'), rw.statistic, g(h, 'tzDF'), rw.df, g(h, 'tzP'), rw.pvalue),
      rel(g(h, 'tzT'), rw.statistic) < 1e-12 and rel(g(h, 'tzDF'), rw.df) < 1e-12 and g(h, 'tzREJ') == 1 and
      rel(g(h, 'tzP'), rw.pvalue) < 1e-9 and g(h, 'tzTY') == 2)
p1 = page(h, 'tz_Step1()')
check('B2 draft step 1: means and SDs worked out from the 366 numbers, to 4 significant digits (206.3, not '
      '206.32418); the names; the outcome and its source',
      has(p1, '\ue000₁ = 206.3') and has(p1, '\ue000₂ = 160.9') and has(p1, 's₁ = 106.1') and has(p1, 's₂ = 100.8') and
      has(p1, 'N₁ = 182') and has(p1, 'N₂ = 184') and has(p1, 'Born Jan-Jun') and has(p1, 'Born Jul-Dec') and
      has(p1, 'Outcome: draft number (Selective Service, 1970)') and not has(p1, '206.32'), lines(p1))
p2 = page(h, 'tz_Step2()')
check('B2 draft step 2: Welch\'s df worked (362.56) and the hand shortcut beside it: df 181, t crit ±%.3f'
      % tdist.isf(0.025, 181),
      has(p2, '= 362.56') and has(p2, 'By hand: df = the smaller of N₁-1, N₂-1 = 181,') and
      has(p2, 't crit = ±%.3f: larger, so a safer test.' % tdist.isf(0.025, 181)), lines(p2))
p3 = page(h, 'tz_Step3()')
check('B2 draft step 3: the exact t crit at df 362.56 and the note "Round df down to 362"',
      has(p3, 't crit = ±%.3f   (exact, for df = 362.56)' % tdist.isf(0.025, rw.df)) and
      has(p3, 'Printed table?  Round df down to 362; if the'), lines(p3))
p4 = page(h, 'tz_Step4()')
check('B2 draft step 4: the SDs and means in the working to 4 significant digits; t obt 4.20',
      has(p4, '   = √(106.1²/182 + 100.8²/184)') and has(p4, '= (206.3 - 160.9)/') and has(p4, '= 4.20'), lines(p4))
p5 = page(h, 'tz_Step5()')
check('B2 draft step 5: reject, sample 1 (born Jan-Jun) higher on average, p < 0.001, no near-alpha note',
      has(p5, 'REJECT H₀.') and has(p5, 'sample 1 (Born Jan-Jun) is higher on average.') and
      has(p5, 'Report t(362.56) = 4.20, p < 0.001, two-tailed') and not has(p5, 'just below'), lines(p5))

# B3 age at arrest (JDCC; pooled, two-tailed .05): the advanced version's example 1, without the lecture's notes
h.execute('tz_Example(3)')
h.execute('tz_Calc()')
r1 = stats.ttest_ind_from_stats(15.89, 1.45, 44, 16.57, 1.11, 31, equal_var=True)
check('B3 age at arrest (pooled, two-tailed .05): t = %.4f (SciPy %.4f), df 73, exact t crit %.3f, reject; p %.4f; '
      'd %.3f' % (g(h, 'tzT'), r1.statistic, g(h, 'tzTC'), g(h, 'tzP'), g(h, 'tzD')),
      rel(g(h, 'tzT'), r1.statistic) < 1e-12 and g(h, 'tzDF') == 73 and
      abs(g(h, 'tzTC') - tdist.isf(0.025, 73)) < 1e-12 and g(h, 'tzREJ') == 1 and rel(g(h, 'tzP'), r1.pvalue) < 1e-9)
p4 = page(h, 'tz_Step4()')
check('B3 step 4 shows the working with the numbers in and the exact t, and no rounding note',
      has(p4, '= √[(43 × 1.45² + 30 × 1.11²)/73]') and has(p4, '× √[75/1364]') and
      has(p4, '= √1.745 × √0.05499 = 1.321 × 0.2345') and has(p4, '= 0.3097') and
      has(p4, '= -0.6800/0.3097 = -2.20') and not has(p4, 'rounds'), lines(p4))
p1 = page(h, 'tz_Step1()')
check('B3 step 1: typed numbers shown as typed (1.45, 1.11), the names, the outcome',
      has(p1, 's₁ = 1.45') and has(p1, 's₂ = 1.11') and has(p1, '\ue000₁ = 15.89') and has(p1, 'Hispanic') and
      has(p1, 'Outcome: age at arrest (years), JDCC'), lines(p1))

# B4 matched jails (Census of Jails; dependent, one-tailed H1 mu1 < mu2, .05)
h.execute('tz_Example(4)')
h.execute('tz_Calc()')
a = np.array([1.30, 1.25, 0.86, 0.94, 2.26])
b = np.array([1.00, 0.76, 0.99, 1.10, 1.85])
r2 = stats.ttest_rel(a, b, alternative='less')
check('B4 matched jails (dependent, one-tailed H1 mu1 < mu2, .05): x-bar D %.3f, sum of squares %.5f, sD %.5f, SE '
      '%.5f, t %.4f (SciPy %.4f), df 4, t crit -2.132, retain; p %.4f'
      % (g(h, 'tzMD'), g(h, 'tzSSq'), g(h, 'tzSDv'), g(h, 'tzSE'), g(h, 'tzT'), r2.statistic, g(h, 'tzP')),
      rel(g(h, 'tzT'), r2.statistic) < 1e-12 and g(h, 'tzDF') == 4 and round(g(h, 'tzTC'), 3) == 2.132 and
      g(h, 'tzREJ') == 0 and rel(g(h, 'tzP'), r2.pvalue) < 1e-9 and abs(g(h, 'tzSSq') - 0.37508) < 1e-9)
p4 = page(h, 'tz_Step4()')
check('B4 step 4: the differences, their deviations and squares, the sum .3751 ("sum", not the unverified sigma '
      'glyph), sD, SE, t obt; no rounding note',
      has(p4, 'sum = 0.3751') and has(p4, 'sD = √(sum/(N-1)) = √(0.3751/4) = 0.3062') and
      has(p4, 'SE = sD/√N = 0.3062/√5 = 0.1369') and has(p4, 'D/SE = 0.1820/0.1369 = 1.33') and
      not has(p4, 'rounds'), lines(p4))
p5 = page(h, 'tz_Step5()')
check('B4 step 5: retain, and the samples differ the other way from H1 (t > 0, H1 predicted < 0)',
      has(p5, 'RETAIN H₀.') and has(p5, 'The samples even differ the other way from H₁.') and
      has(p5, 'Report t(4) = 1.33, p = 0.873, one-tailed'), lines(p5))
# the near-alpha note on the other side: p just above alpha
calc(h, tzTY=1, tzSRC=1, tzTL=0, tzAL=0.05, tzM1=1.2852, tzS1=1, tzN1=6, tzM2=0, tzS2=1, tzN2=6)
p5 = page(h, 'tz_Step5()')
check('B the near-alpha note above alpha: 2.226 vs 2.228 retains with "(p = %.5f: just above α = 0.050.)"'
      % g(h, 'tzP'), has(p5, 'RETAIN H₀.') and has(p5, 'just above α = 0.050.)') and
      has(p5, '(p = %s: just above' % ('%.5f' % g(h, 'tzP'))[:7]), lines(p5))

# ===================================================================== C. screens and flows
print('=== C. screens, the flowchart, the forms, D1/D2, refusals, menu, help')


def run(script, app=None, path=PROG):
    h = Harness(path, idle_key=4, home_minus=True, app_data=app)
    script(h)
    try:
        res = h.execute('TTESTLABG()')
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
for ex in (1, 2, 3, 4):
    hh, res, err = run(s_all(ex))
    ts = [U(p.lines()[0]) for p in hh.pages]
    titles_ok.append((ex, err, res, ts[:7]))
want = ['Step 1. The hypotheses', 'Step 1. The hypotheses', 'Step 2. Distribution and df',
        'Step 3. Critical value, decision rule', 'Step 4. Standard error and t obtained',
        'Step 5. Decision and conclusion', 'Step 4. Standard error and t obtained']
check('C1 each example opens on step 1; soft keys 1-5 and Left/Right step through; Esc quits with the result string: %s'
      % [(t[0], t[2]) for t in titles_ok],
      all(t[1] is None and t[3][:7] == want for t in titles_ok) and
      [U(t[2]) for t in titles_ok] == ['TTestLabG: t(14) = 2.15, p = 0.050, two-tailed',
                                       'TTestLabG: t(362.56) = 4.20, p < 0.001, two-tailed',
                                       'TTestLabG: t(73) = -2.20, p = 0.031, two-tailed',
                                       'TTestLabG: t(4) = 1.33, p = 0.873, one-tailed'], titles_ok)
hh, _, _ = run(s_all(3))
p1 = hh.pages[0]
check('C1 step 1 of example 3 (age at arrest): test, tails, alpha; H0 and H1; the numbers in two columns',
      has(p1, 'Pooled-variances t test, two-tailed, α = 0.050') and has(p1, 'H₀: μ₁ = μ₂') and
      has(p1, 'H₁: μ₁ ≠ μ₂   (they differ, either way)') and has(p1, 's₁ = 1.45') and has(p1, 'N₂ = 31') and
      has(p1, 'Hispanic') and has(p1, 'Non-Hispanic white'), lines(p1))
p3 = hh.pages[3]
check('C1 step 3 of example 3: the exact t crit, the printed-table note, the either/or rule, the menu of steps',
      has(p3, 't crit = ±1.993   (exact, for df = 73)') and has(p3, 'Printed table without row 73?  Take the next') and
      has(p3, 'Rule: if t obt > 1.993 or t obt < -1.993,') and menus_drawn(hh)[-1] == ['1 H', '2 df', '3 crit', '4 t', '5 end', 'Menu'],
      (lines(p3), menus_drawn(hh)[-1:]))
p5 = hh.pages[5]
check('C1 step 5 of example 3: reject, the direction in the samples\' names, the report line, d, the p legend',
      has(p5, 'REJECT H₀.') and has(p5, 'sample 1 (Hispanic) is lower on average.') and
      has(p5, 'Report t(73) = -2.20, p = 0.031, two-tailed') and has(p5, "Cohen's d = -0.51  (pooled s)") and
      has(p5, 'magenta area = p') and has(p5, 't obt = -2.20'), lines(p5))
hh, _, _ = run(s_all(4))
p3 = hh.pages[3]
check('C1 step 3 of example 4 (matched jails): one-tailed lower, "t crit = -2.132" exact for df 4, rule "if t obt < '
      '-2.132", no printed-table note at df 4',
      has(p3, 't crit = -2.132   (exact, for df = 4)') and has(p3, 'Rule: if t obt < -2.132,') and
      not has(p3, 'Printed table'), lines(p3))
p1 = hh.pages[0]
check('C1 step 1 of example 4: H1 mu1 < mu2, the five pairs, and the source on screen',
      has(p1, 'H₁: μ₁ < μ₂   (a predicted direction)') and has(p1, '2.26') and has(p1, '1.85') and has(p1, '0.76') and
      has(p1, 'Outcome: assault rate, Census of Jails'),
      lines(p1))


hp_ = H()
put(hp_, tzTY=3, tzSRC=2, tzTL=0, tzAL=0.05, tzX1=list(range(1, 13)), tzX2=[x * 0.9 for x in range(1, 13)])
hp_.globals_['tzDV'] = 'a test outcome'
hp_.execute('tz_Calc()')
pq = page(hp_, 'tz_Step1()')
rows = [t for t in pq.texts if round(t.x) == 14 and t.text.isdigit()]
check('C1 step 1 with 12 pairs (beta 1a): 7 rows, "... and 5 more pairs" on the 8th, the outcome under them',
      len(rows) == 7 and has(pq, '... and 5 more pairs') and has(pq, 'Outcome: a test outcome'), lines(pq))
put(hp_, tzSRC=1, tzMD=0.5, tzSDv=1, tzNP=9)
pq = page(hp_, 'tz_Step1()')
check('C1 step 1, dependent samples typed as a summary: the outcome under the box', has(pq, 'Outcome: a test outcome'),
      lines(pq))

# the curve: the shaded rejection region matches t critical, column by column
hs = H()
hs.execute('tz_Example(3)')
hs.execute('tz_Calc()')
hs.reset_records()
hs.execute('tz_Step3()')
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
    hh.execute('tz_Settle()')
    got = hh.execute('tz_Flow()')
    fl.append((name, got))
check('C3 the flowchart (two questions): tapped boxes and soft keys give pooled / separate / dependent; Back undoes; '
      'OK waits for an answer: %s' % fl, [f[1] for f in fl] == [1, 2, 3, 2, 3, 1], fl)
hh = H()
hh.press('Esc')
check('C3 Esc leaves the flowchart (returns 0)', hh.execute('tz_Flow()') == 0)
hh = H()
hh.tap(90, 71)
hh.press('Esc')
hh.reset_records()
hh.execute('tz_Flow()')
fp = hh.pages[-1]
check('C3 the flowchart\'s texts and soft keys: its title, both questions, three tests, the hint that separate is the '
      'default ("Not sure ... Answer No")',
      has(fp, 'Which t test?') and not has(fp, 'Figure') and
      has(fp, '1. Are the samples independent?') and has(fp, '2. Are the variances equal?') and
      has(fp, 'Pooled t') and has(fp, 'Separate t') and has(fp, 'Dependent-samples t') and
      has(fp, 'Not sure the variances are equal?  Answer No:') and
      has(fp, 'the separate t needs no such assumption.') and menus_drawn(hh)[-1] == ['Yes', 'No', 'Back', '', '', 'OK'],
      (lines(fp), menus_drawn(hh)[-1:]))


# full flows from the start: flowchart -> data -> tails -> alpha
def s_flow_ind(h):
    h.choose(1)
    for x, y in [(90, 71), (140, 133), (290, 230)]:
        h.tap(x, y)
    h.choose(1)                                          # type the numbers
    h.answer({'tzM1': 4.8185, 'tzS1': 3.28798, 'tzN1': 270, 'tzM2': 6.4247, 'tzS2': 3.74872, 'tzN2': 146})
    h.choose(3)                                          # one-tailed mu1 > mu2
    h.choose(2)                                          # alpha .05


hh, res, err = run(s_flow_ind)
pr = stats.ttest_ind_from_stats(4.8185, 3.28798, 270, 6.4247, 3.74872, 146, equal_var=False, alternative='greater')
check('C4 flowchart -> separate -> typed numbers -> one-tailed mu1 > mu2 -> alpha .05: "%s" (p %.4f)'
      % (U(res or ''), pr.pvalue), err is None and U(res) == 'TTestLabG: t(265.92) = -4.35, p > 0.999, one-tailed' and
      g(hh, 'tzTL') == 1 and g(hh, 'tzAL') == 0.05, (err, res))
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
      'names "D1"/"D2"' % (g(hh, 'tzT'), rr.statistic, g(hh, 'tzP')),
      err is None and rel(g(hh, 'tzT'), rr.statistic) < 1e-12 and rel(g(hh, 'tzP'), rr.pvalue) < 1e-9 and
      g(hh, 'tzG1') == 'D1' and g(hh, 'tzAL') == 0.02, (err, res))


def s_flow_pairs(h):
    h.choose(1)
    h.tap(230, 71)
    h.tap(290, 230)
    h.choose(1)                                          # pairs in D1 and D2
    h.choose(2)                                          # one-tailed mu1 < mu2
    h.choose(2)


hh, res, err = run(s_flow_pairs, app={'D1': [1.30, 1.25, 0.86, 0.94, 2.26], 'D2': [1.00, 0.76, 0.99, 1.10, 1.85]})
check('C6 pairs from D1 and D2 reproduce example 2 (t %.4f, df 4)' % g(hh, 'tzT'),
      err is None and rel(g(hh, 'tzT'), r2.statistic) < 1e-12 and g(hh, 'tzDF') == 4, (err, res))


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
      % g(hh, 'tzT'), err is None and abs(g(hh, 'tzT') - ref_t) < 1e-12 and
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
        ('N 1', {'tzN1': 1}, 'Each group needs N of at least 2.'),
        ('SD < 0', {'tzS1': -1}, 'An SD cannot be negative.'),
        ('both SD 0', {'tzS1': 0, 'tzS2': 0}, 'Both SDs are 0'),):
    def sc(h, vals=vals):
        h.choose(1)
        for x, y in [(90, 71), (40, 133), (290, 230)]:
            h.tap(x, y)
        h.choose(1)
        base = {'tzM1': 5, 'tzS1': 2, 'tzN1': 10, 'tzM2': 4, 'tzS2': 2, 'tzN2': 10}
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
      all(b[1] is None and b[2] and m in b[2][0] and b[3] == ['TTestLabG']
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
    h.choose(4)                                          # example 3, age at arrest (pooled)
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
      err is None and g(hh, 'tzTY') == 2 and g(hh, 'tzM1') == 15.89 and g(hh, 'tzTL') == 0 and
      U(res) == 'TTestLabG: t(72.44) = -2.30, p = 0.024, two-tailed', (err, res, [d.title for d in hh.dialogs]))
hh, res, err = run(lambda h: (h.choose(6), h.press('Enter'), h.press('Enter')))
hp = [lines(p) for p in hh.pages[:2]]
check('C9 help: two pages (keys, with DataLoad for a long data set; the numbers, the printed-table rule, the Inference '
      'app as a check), then back to the start menu',
      err is None and len(hp) == 2 and 'TTestLabG help 1/2: keys' in hp[0][0] and
      any('A long data set: DataLoad fills D1 and D2.' in x for x in hp[0]) and
      any('A printed table: a df it lacks, the next smaller' in x for x in hp[1]) and
      any('Separate variances (the default): Welch' in x for x in hp[1]) and
      any('Check on the Prime: Inference app, Hyp. test,' in x for x in hp[1]) and
      any('Teaching aid; not for clinical or legal use.' in x for x in hp[0]), hp)
hh, res, err = run(lambda h: h.choose(0))
check('C9 the start menu cancelled: "TTestLabG: cancelled"', err is None and res == 'TTestLabG: cancelled', (err, res))

# ===================================================================== E. pooled or separate?
print('=== E. the "Pooled or separate?" page')
cmp_ = []
for name, kv, want in (
        ('N1 = N2', dict(tzN1=20, tzN2=20, tzS1=1, tzS2=4), 'N₁ = N₂: the same t either way; only df differs.'),
        ('s1 = s2', dict(tzN1=10, tzN2=40, tzS1=2, tzS2=2), 's₁ = s₂: the same t either way; only df differs.'),
        ('small n, big s', dict(tzN1=10, tzN2=40, tzS1=4, tzS2=1), 'The SMALLER group has the LARGER SD: the pooled'),
        ('big n, big s', dict(tzN1=10, tzN2=40, tzS1=1, tzS2=4), 'The LARGER group has the LARGER SD: the pooled')):
    hh = H()
    put(hh, tzTY=1, tzTL=0, tzAL=0.05, tzM1=6, tzM2=5, **kv)
    hh.execute('tz_Calc()')
    hh.press('Enter')
    hh.reset_records()
    hh.execute('tz_Compare()')
    pc = hh.pages[-1]
    tp = hh.execute('tz_Ind(1)')
    ts = hh.execute('tz_Ind(2)')
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
put(hh, tzTY=3)
hh.execute('tz_Compare()')
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
    h.choose(4)                                          # example 3, age at arrest (dialog 1)
    soft(h, 6)
    h.choose('Edit the numbers')                         # dialog 2
    h.choose(1)                                          # dialog 3: type the numbers
    h.answer(ACCEPT)                                     # dialog 4: the form, OK tapped ...
    hold_after(h, 4, 290, 230)                           # ... and the finger still on it (= Menu, slot 6)


hh, res, err = run(s_edit_held)
menus = [d.title for d in hh.dialogs].count('TTestLabG')
check('F1 Menu > Edit the numbers > OK with the finger left on OK (soft-key slot 6, Menu): the menu does not open '
      'again (%d menu, %s)' % (menus, err), err is None and menus == 1, [d.title for d in hh.dialogs])
ctl = SRC.replace(' tz_Drain();\n tz_TDrain();\nEND;', ' tz_Drain();\nEND;', 1)
cpath = os.path.join(tempfile.mkdtemp(), 'TTestLabG_ctl.txt')
open(cpath, 'w', encoding='utf-8').write(ctl)
hh, res, err = run(s_edit_held, path=cpath)
menus_c = [d.title for d in hh.dialogs].count('TTestLabG')
check('F1 control: a copy whose tz_Settle drains keys only opens the menu a second time (%d), as PowerViz v2.5h did '
      'on Roger\'s calculator' % menus_c, ctl != SRC and menus_c >= 2, [d.title for d in hh.dialogs])


# ===================================================================== R. the review's findings
print("=== R. the independent review's findings (each check fails on beta 1a)")


def s_tails_cancel(h):
    h.choose(4)                                          # example 3, age at arrest
    h.press('Enter')                                     # the menu
    h.choose(2)                                          # Tails and alpha
    h.choose(2)                                          # one-tailed mu1 < mu2
    h.choose(0)                                          # ... then Esc at the alpha list
    h.press('Enter')
    h.choose(7)


hh, res, err = run(s_tails_cancel)
st1 = [p for p in hh.pages if U(p.lines()[0]).startswith('Step 1')]
check('R1 tails chosen, alpha list cancelled: nothing changes (step 1 still "two-tailed", t crit ±1.993, and the result'
      ' line "p = 0.031, two-tailed")',
      err is None and len(st1) >= 2 and has(st1[-1], 'Pooled-variances t test, two-tailed, α = 0.050') and
      g(hh, 'tzTL') == 0 and U(res) == 'TTestLabG: t(73) = -2.20, p = 0.031, two-tailed', (err, res, lines(st1[-1])[:2] if st1 else None))


def s_tails_ok(h):
    h.choose(4)
    h.press('Enter')
    h.choose(2)
    h.choose(2)                                          # one-tailed mu1 < mu2
    h.choose(2)                                          # alpha .05 (one-tailed list)
    h.press('Enter')
    h.choose(7)


hh, res, err = run(s_tails_ok)
check('R1 tails and alpha both chosen: both change (t crit -1.666, p = 0.016, one-tailed)',
      err is None and g(hh, 'tzTL') == -1 and abs(g(hh, 'tzTC') - tdist.isf(0.05, 73)) < 1e-9 and
      U(res) == 'TTestLabG: t(73) = -2.20, p = 0.016, one-tailed', (err, res))


def s_refused_pairs(h):
    h.choose(1)
    h.tap(230, 71)                                       # dependent
    h.tap(290, 230)                                      # OK
    h.choose(2)                                          # type mean, SD of differences
    h.answer({'dm': 0.5, 'dsd': 1, 'dn': 5})
    h.choose(1)                                          # two-tailed
    h.choose(3)                                          # .05
    h.press('Enter')                                     # the menu
    h.choose(1)                                          # Edit the numbers
    h.choose(1)                                          # pairs in D1 and D2 (empty): refused
    h.press('Enter')
    h.choose(7)


hh, res, err = run(s_refused_pairs, app={'D1': [], 'D2': []})
st1 = [p for p in hh.pages if U(p.lines()[0]).startswith('Step 1')]
check('R2 a typed dependent summary, then a refused D1/D2 pairs read: the source stays "summary" (tzSRC 1), step 1'
      ' draws again with "N pairs = 5", no error',
      err is None and g(hh, 'tzSRC') == 1 and len(st1) >= 2 and has(st1[-1], 'N pairs = 5') and
      any('Put the pairs in D1 and D2' in str(it) for it in hh.log), (err, res, g(hh, 'tzSRC')))

hh = H()
calc(hh, tzTY=1, tzSRC=1, tzM1=4, tzS1=2, tzN1=1, tzM2=2, tzS2=2, tzN2=5)
cerr = None
try:
    hh.execute('tz_Compare()')
except Exception as e:                                   # noqa: BLE001
    cerr = '%s: %s' % (type(e).__name__, str(e)[:80])
check('R3 "Pooled or separate?" with numbers that gave no t (N1 = 1): a box "give no t", no division by zero',
      g(hh, 'tzOK') == 0 and cerr is None and any('give no t' in str(it) for it in hh.log), (cerr, g(hh, 'tzOK')))
hh = H()
calc(hh, tzTY=1, tzSRC=1, tzM1=4, tzS1=0, tzN1=5, tzM2=2, tzS2=0, tzN2=5)
cerr = None
try:
    hh.execute('tz_Compare()')
except Exception as e:                                   # noqa: BLE001
    cerr = '%s: %s' % (type(e).__name__, str(e)[:80])
check('R3 the same with both SDs 0', g(hh, 'tzOK') == 0 and cerr is None, cerr)

hh = H()
fm = {v: hh.execute('tz_FmtP(%r,3)' % v) for v in (0, 1e-320, 0.0004, 0.0005, 0.0314, 0.9994, 0.9996, 1)}
check('R4 tz_FmtP: 0 and an underflow print "< 0.001" (so does 0.0005, below the floor); 1 prints "1.000"; 0.9996 "> 0.999"; 0.0314 "0.031"',
      fm[0] == '< 0.001' and fm[1e-320] == '< 0.001' and fm[0.0004] == '< 0.001' and fm[0.0005] == '< 0.001' and
      fm[0.0314] == '0.031' and fm[0.9994] == '0.999' and fm[0.9996] == '> 0.999' and fm[1] == '1.000', fm)
hh = H()
calc(hh, tzTY=3, tzSRC=1, tzMD=0.5, tzSDv=1, tzNP=10000)
p5 = page(hh, 'tz_Step5()')
check('R4 10,000 pairs at d = 0.5 (t = 50, p underflows): step 5 reports "p < 0.001", never "p = 0.000"',
      has(p5, 'Report t(9999) = 50.00, p < 0.001, two-tailed') and not has(p5, 'p = 0.000'), lines(p5))
hh = H()
calc(hh, tzTY=1, tzSRC=1, tzM1=0, tzS1=1, tzN1=6, tzM2=0, tzS2=1, tzN2=6)
p5 = page(hh, 'tz_Step5()')
check('R4 t = 0: "p = 1.000"', has(p5, 'p = 1.000'), lines(p5))

hh = H()
calc(hh, tzTY=1, tzSRC=1, tzM1=1.2852, tzS1=1, tzN1=6, tzM2=0, tzS2=1, tzN2=6)
p5 = page(hh, 'tz_Step5()')
check('R5 t = 2.2261 on df 10, t crit 2.228: the decision line prints both to 3 decimals ("2.226 is not beyond ±2.228")'
      ' and the Report line keeps 2 ("= 2.23")',
      has(p5, 't obt = 2.226 is not beyond t crit = ±2.228') and has(p5, 'Report t(10) = 2.23'), lines(p5))


def s_cancel_form(h):
    h.choose(4)                                          # example 3, age at arrest
    h.press('Enter')
    h.choose(1)                                          # Edit the numbers
    h.choose(1)                                          # type ...
    h.answer(CANCEL)                                     # ... and cancel the form
    h.press('Enter')
    h.choose(7)


hh, res, err = run(s_cancel_form)
st1 = [p for p in hh.pages if U(p.lines()[0]).startswith('Step 1')]
st4 = None
check('R6 example 3, Edit the numbers, form cancelled: the names ("Hispanic"), the outcome line and the example (tzEX 3)'
      ' are kept',
      err is None and g(hh, 'tzEX') == 3 and g(hh, 'tzG1') == 'Hispanic' and len(st1) >= 2 and
      has(st1[-1], 'Outcome: age at arrest (years), JDCC') and has(st1[-1], 'Hispanic'), (err, g(hh, 'tzEX'), g(hh, 'tzG1')))


def s_dep_cancel(h):
    h.choose(4)                                          # example 3 (pooled)
    h.press('Enter')
    h.choose(4)                                          # Choose the test
    h.tap(230, 71)                                       # dependent
    h.tap(290, 230)                                      # OK
    h.choose(2)                                          # type the differences ...
    h.answer(CANCEL)                                     # ... cancelled: the old test and names stay
    h.press('Enter')
    h.choose(7)


hh, res, err = run(s_dep_cancel)
check('R6 Choose the test -> dependent -> form cancelled: the pooled test, its names and example stay',
      err is None and g(hh, 'tzTY') == 1 and g(hh, 'tzEX') == 3 and g(hh, 'tzG1') == 'Hispanic' and
      U(res) == 'TTestLabG: t(73) = -2.20, p = 0.031, two-tailed', (err, res, g(hh, 'tzTY'), g(hh, 'tzG1')))


def s_frac_n(h):
    h.choose(1)
    h.tap(90, 71)                                        # independent
    h.tap(40, 133)                                       # equal variances
    h.tap(290, 230)                                      # OK
    h.choose(1)                                          # type
    h.answer({'tzM1': 5, 'tzS1': 2, 'tzN1': 10.5, 'tzM2': 4, 'tzS2': 2, 'tzN2': 10})
    h.choose(1)
    h.choose(3)
    soft(h, 2)


hh, res, err = run(s_frac_n)
st2 = [p for p in hh.pages if U(p.lines()[0]).startswith('Step 2')]
check('R7 a typed N1 of 10.5 is 10: df 18 ("= 10 + 10 - 2 = 18"), t(18)',
      err is None and g(hh, 'tzN1') == 10 and g(hh, 'tzDF') == 18 and st2 and has(st2[-1], '= 10 + 10 - 2 = 18') and
      U(res).startswith('TTestLabG: t(18) ='), (err, res, g(hh, 'tzN1'), lines(st2[-1]) if st2 else None))

hh = H()
calc(hh, tzTY=3, tzSRC=2, tzX1=[1, 2.5], tzX2=[1.5, 2])
p3 = page(hh, 'tz_Step3()')
# the dashed line: LINE_P columns at the window's edges, x = 12 (tzPL) and 308 (tzPR), in red
reds = sorted(set(int(sh.args[0]) for sh in p3.shapes if sh.cmd == 'LINE_P' and sh.args[0] == sh.args[2]
                  and sh.args[0] in (12, 308) and sh.args[4] == hh.globals_['tzRED']))
check('R8 2 pairs at .05 (t crit 12.706, beyond the window of ±12): step 3 says so in the rule, draws a "t crit" label at'
      ' each edge, and the dashed line is at the window\'s edge (x = 12 and 308)',
      abs(g(hh, 'tzTC') - 12.7062) < 1e-3 and has(p3, "(t crit lies beyond the plot.)") and
      lines(p3).count('t crit') == 2 and not has(p3, 'Red = the rejection region') and
      reds == [12, 308], (lines(p3), reds))
hh = H()
hh.execute('tz_Example(3)')
hh.execute('tz_Calc()')
p3 = page(hh, 'tz_Step3()')
check('R8 example 3 (t crit 1.993, inside the window): no edge label, the rule still names the red region',
      lines(p3).count('t crit') == 0 and has(p3, 'Red = the rejection region (α).'), lines(p3))

hh = H()
calc(hh, tzTY=3, tzSRC=1, tzMD=1, tzSDv=-1, tzNP=5)
check('R9 a negative typed sD: "An SD cannot be negative."', g(hh, 'tzOK') == 0 and g(hh, 'tzMSG') == 'An SD cannot be negative.',
      g(hh, 'tzMSG'))
hh = H()
calc(hh, tzTY=3, tzSRC=1, tzMD=1, tzSDv=0, tzNP=5)
check('R9 sD = 0 still gets its own message', g(hh, 'tzMSG').startswith('Every pair differs by the same amount'), g(hh, 'tzMSG'))

hh = H()
put(hh, tzTY=3, tzSRC=2, tzX1=[5], tzX2=[3])
cerr = None
try:
    hh.execute('tz_Calc()')
except Exception as e:                                   # noqa: BLE001
    cerr = '%s: %s' % (type(e).__name__, str(e)[:80])
check('R10 one pair in D1/D2 given to tz_Calc directly: refused ("at least 2 pairs"), no division by zero',
      cerr is None and g(hh, 'tzOK') == 0 and 'at least 2 pairs' in g(hh, 'tzMSG'), (cerr, g(hh, 'tzMSG')))

hh = H()
pg = page(hh, 'tz_Help()')
hp1 = hh.pages[0]
check('R11 help 1: "sample 1 (or x₁) in D1, sample 2 (or x₂) in D2"', has(hp1, 'sample 1 (or x₁) in D1, sample 2 (or x₂) in D2'),
      lines(hp1))
hh = H()
hh.execute('tz_Example(4)')
hh.execute('tz_Calc()')
p1 = page(hh, 'tz_Step1()')
check('R11 example 4\'s pairs print with one decimal count per column: 1.30, 1.00, 1.10 beside 1.25 and 0.76',
      all(has(p1, v) for v in ('1.30', '1.25', '0.86', '0.94', '2.26', '1.00', '0.76', '0.99', '1.10', '1.85')) and
      not any(x in ('1.3', '1.1') for x in lines(p1)), lines(p1))
cd = {k: hh.execute('tz_ColDec(%s)' % k) for k in ('{1.30,1.25,0.86}', '{1,2,3}', '{1.5,2,3.25}', '{0.182,1}', '{3.28798,1}')}
check('R11 tz_ColDec: {1.30,1.25,0.86} -> 2, {1,2,3} -> 0, {1.5,2,3.25} -> 2, {0.182,1} -> 3, {3.28798,1} -> 5',
      list(cd.values()) == [2, 0, 2, 3, 5], cd)
check('R11 tz_FixD(2, 0) = "2", tz_FixD(1, 2) = "1.00", tz_FixD(1.3, 2) = "1.30"',
      hh.execute('tz_FixD(2,0)') == '2' and hh.execute('tz_FixD(1,2)') == '1.00' and hh.execute('tz_FixD(1.3,2)') == '1.30')
hh = H()
calc(hh, tzTY=2, tzSRC=1, tzM1=4.8185, tzS1=3.28798, tzN1=270, tzM2=5.5476, tzS2=3.74872, tzN2=146)
p5 = page(hh, 'tz_Step5()')
trl = [x for x in lines(p5) if x.startswith('(Table row')]
check('R11 (the general version) no table-row line on step 5: the exact df decides alone, where TTestLab printed '
      '"(Table row 120, ±1.980, decides the other way.)"', not trl and has(p5, 't obt = -1.975 is beyond t crit = ±1.969:'),
      lines(p5))
hh = H()
calc(hh, tzTY=3, tzSRC=1, tzMD=0.5, tzSDv=1, tzNP=5)
p4 = page(hh, 'tz_Step4()')
ys = {t.text.split(' ')[0]: t.y for t in p4.texts if t.text.startswith('SE = ') or t.text.startswith('t obt')}
check('R11 step 4 for a typed summary: the SE and t lines sit right under the summary (y 60 and 73), not after a 100-px gap',
      ys.get('SE') == 60 and ys.get('t') == 73, ys)
hh = H()
hh.execute('tz_Example(4)')
hh.execute('tz_Calc()')
p4 = page(hh, 'tz_Step4()')
ys = {t.text.split(' ')[0]: t.y for t in p4.texts if t.text.startswith('SE = ') or t.text.startswith('t obt')}
check('R11 step 4 for raw pairs: the SE and t lines stay under the table (y 141 and 154)', ys.get('SE') == 141 and ys.get('t') == 154, ys)


def s_help_start(h):
    h.choose(6)                                          # Help from the start menu
    h.press('Enter')                                     # page 2
    h.press('Enter')                                     # back ...
    h.choose(0)                                          # ... to the start menu: cancel it


hh, res, err = run(s_help_start)
check('R11 Help from the start menu returns to that menu (cancel there gives "TTestLabG: cancelled"; beta 1a went on to'
      ' example 1)', err is None and res == 'TTestLabG: cancelled' and
      [U(p.lines()[0]) for p in hh.pages] == ['TTestLabG help 1/2: keys', 'TTestLabG help 2/2: the numbers'], (err, res))

# ===================================================================== N. the general version
print('=== N. the general version: the default test, the menus, no lecture words')
hh = H()
check('N1 a fresh start holds the separate-variances test (tzTY 2): the default, where TTestLab started pooled',
      g(hh, 'tzTY') == 2)
hh, res, err = run(lambda h: h.choose(0))
sm = hh.chooses[0] if hh.chooses else None
check('N2 the start menu: the flowchart, the four examples, Help',
      sm is not None and sm.title == 'TTestLabG: t tests in 5 steps' and
      sm.items == ['Choose the test (flowchart)', "Example: Darwin's plants", 'Example: draft lottery',
                   'Example: age at arrest', 'Example: matched jails', 'Help'], (sm.title, sm.items) if sm else None)


def s_ex_menu(h):
    h.choose(2)                                          # Darwin
    h.press('Enter')                                     # the menu
    h.choose('Examples')
    h.choose(2)                                          # the draft lottery
    h.press('Enter')
    h.choose('Quit')


hh, res, err = run(s_ex_menu)
em = [c for c in hh.chooses if c.title == 'Examples']
mm_ = [c for c in hh.chooses if c.title == 'TTestLabG']
check('N2 the menu names this program: its last item is "Quit TTestLabG" (beta 1\'s first build, on the Virtual '
      'Calculator, still said "Quit TTestLab")', bool(mm_) and mm_[0].items[-1] == 'Quit TTestLabG',
      [c.items for c in mm_][:1])
check('N2 the menu\'s Examples: Darwin\'s plants, the draft lottery, age at arrest, matched jails; choosing the draft '
      'lottery from Darwin\'s pairs switches test and data: "%s"' % U(res or ''),
      err is None and em and em[0].items == ["Darwin's plants (pairs)", 'Draft lottery (separate)',
                                             'Age at arrest (pooled)', 'Matched jails (pairs)'] and
      g(hh, 'tzTY') == 2 and g(hh, 'tzEX') == 2 and U(res) == 'TTestLabG: t(362.56) = 4.20, p < 0.001, two-tailed',
      (err, res, [c.items for c in em]))
strs = re.findall(r'"([^"\n]*)"', '\n'.join(ln for ln in SRC.split('\n') if not ln.lstrip().startswith('//')))
badw = [s_ for s_ in strs if any(w in s_.lower() for w in ('lecture', 'figure 11', 'table 11', 'drug use', 'levene'))]
check('N3 no string a student can see names the lecture, Figure 11.2, Table 11.x, Levene\'s test or the SPSS drug-use '
      'example (%d strings read)' % len(strs), not badw, badw)

# ===================================================================== M. the monkey test's findings
print("=== M. the monkey test's findings (1 Nov 2026; each check fails on beta 1)")


OLD_FROM = ['']


def older(name):
    """the previous version: beside this script, in ../programs, in an _superseded_* folder beside it (the author's
    D:\\HP-Prime), or from git history (Lessons Learned rule 18)"""
    import glob
    for pth in [os.path.join(HERE, name), os.path.join(HERE, '..', 'programs', name)] + \
            sorted(glob.glob(os.path.join(HERE, '_superseded_*', name)), reverse=True):   # the author's folder
        if os.path.exists(pth):
            return pth
    import subprocess
    root, rel_ = os.path.join(HERE, '..'), 'programs/' + name
    try:
        c = subprocess.run(['git', '-C', root, 'rev-list', '-n', '1', 'HEAD', '--', rel_],
                           capture_output=True, text=True, timeout=60).stdout.strip()
        for ref in ((c + ':' + rel_, c + '^:' + rel_) if c else ()):
            out = subprocess.run(['git', '-C', root, 'show', ref], capture_output=True, timeout=60)
            if out.returncode == 0:
                pth = os.path.join(tempfile.mkdtemp(), name)
                open(pth, 'wb').write(out.stdout)
                OLD_FROM[0] = 'git history (' + ('the commit before the one that removed it' if ref.split(':')[0].endswith('^') else 'the last commit that has it') + ')'
                return pth
    except Exception:
        pass
    return None


OLD = older('TTestLabG_beta1.txt')
print('   beta 1 for the controls: %s' % ((OLD_FROM[0] or os.path.relpath(OLD, HERE)) if OLD else
                                          'NOT FOUND (the controls are reported as failures)'))


def split_top(t):
    out, d, cur = [], 0, ''
    for ch in t:
        if ch in '([{':
            d += 1
        elif ch in ')]}':
            d -= 1
        if ch == ',' and d == 0:
            out.append(cur.strip())
            cur = ''
        else:
            cur += ch
    out.append(cur.strip())
    return out


def input_fields(src):
    """the fields of every INPUT in the code (comments left out): its first argument, split at the top level"""
    code_ = '\n'.join(ln.split('//')[0] for ln in src.split('\n'))
    out = []
    for m in re.finditer(r'\bINPUT\(', code_):
        i = j = m.end()
        d = 0
        while True:
            ch = code_[j]
            if ch in '([{':
                d += 1
            elif ch in ')]}':
                d -= 1
                if d < 0:
                    break
            elif ch == ',' and d == 0:
                break
            j += 1
        a = code_[i:j].strip()
        out.append(split_top(a[1:-1]) if a.startswith('{') else [a])
    return out


def real_only(src):
    ff = input_fields(src)
    return len(ff) == 2 and all(re.fullmatch(r'\{[A-Za-z]\w*,\[0\]\}', x) for f in ff for x in f), ff


ok_new, ff_new = real_only(SRC)
ok_old, ff_old = real_only(open(OLD, encoding='utf-8').read()) if OLD else (True, None)
check('M1 both forms take real numbers only: every field is {name,[0]} (%d and %d fields), so the form refuses a '
      'list typed as a mean; beta 1\'s fields took any type (%s)'
      % (len(ff_new[0]) if ff_new else 0, len(ff_new[1]) if len(ff_new) > 1 else 0, ff_old[0][:2] if ff_old else '-'),
      ok_new and OLD is not None and not ok_old, (ff_new, ff_old))


def box(hh):
    return [U(' '.join(m.lines)) for m in hh.msgboxes]


def both(script, app=None):
    """the run on beta 1a and the same run on beta 1"""
    new = run(script, app=app)
    old = run(script, app=app, path=OLD) if OLD else (None, None, 'no beta 1b')
    return new, old


big = []
for name, sc, app, want in (
        ('independent, 1E300 in D1', s_flow_raw, {'D1': [12, 1E300, 15], 'D2': d2}, 'Value 2 in D1 has more than 50 digits'),
        ('independent, -1E300 last in D2', s_flow_raw, {'D1': d1, 'D2': d2[:-1] + [-1E300]}, 'Value 10 in D2 has more than 50 digits'),
        ('pairs, -1E300 in D2', s_flow_pairs, {'D1': [1.30, 1.25, 0.86, 0.94, 2.26], 'D2': [1.00, 0.76, 0.99, -1E300, 1.85]},
         'Value 4 in D2 has more than 50 digits')):
    (hn, rn, en), (ho, ro, eo) = both(sc, app)
    mb = box(hn)
    big.append((name, en, rn, mb[:1], eo, box(ho)[:1] if ho else None))
    check('M2 %s: a box names the list and the value ("%s ... Check %s in the Statistics 1Var app."), the program '
          'ends cleanly ("%s"); beta 1: %s' % (name, want, want.split(' in ')[1].split(' ')[0], rn, eo or 'no box'),
          en is None and mb and want in mb[0] and 'Statistics 1Var app.' in mb[0] and rn == 'TTestLabG: cancelled' and
          OLD is not None and (eo is not None or not any('50 digits' in x for x in box(ho))), big[-1])
over5 = [m.lines for m in hn.msgboxes if m.over_five]
check('M2 the box fits in 5 lines (Lessons Learned s3)', not over5, over5)

# the line: 1E50 (and -1E50) refused, 9.99E49 accepted
(hn, rn, en) = run(s_flow_raw, app={'D1': d1, 'D2': d2 + [1E50]})
(hm, rm, em) = run(s_flow_raw, app={'D1': [-1E50] + d1, 'D2': d2})
(ha, ra, ea) = run(s_flow_raw, app={'D1': d1, 'D2': d2 + [9.99E49]})
ra_ = stats.ttest_ind(d1, d2 + [9.99E49], equal_var=True)
check('M3 the line is 1E50 in size: 1E50 in D2 refused (%s), -1E50 in D1 refused (%s), 9.99E49 accepted (t %.6g, '
      'SciPy %.6g; no box)' % (box(hn)[:1], box(hm)[:1], g(ha, 'tzT'), ra_.statistic),
      en is None and em is None and ea is None and box(hn) and 'Value 11 in D2' in box(hn)[0] and box(hm) and
      'Value 1 in D1' in box(hm)[0] and not box(ha) and rel(g(ha, 'tzT'), ra_.statistic) < 1e-9,
      (box(hn), box(hm), box(ha), en, em, ea))


def s_refused_from_example(h):
    h.choose(4)                                          # example 3, age at arrest
    h.press('Enter')
    h.choose('Edit the numbers')
    h.choose(2)                                          # raw scores in D1 and D2: refused
    h.press('Esc')


(hn, rn, en) = run(s_refused_from_example, app={'D1': [1E300, 2], 'D2': [3, 4]})
check('M4 example 3, then a D1 holding 1E300 refused: nothing changes (example 3, its names, typed source, its '
      'numbers; "%s")' % U(rn or ''),
      en is None and g(hn, 'tzEX') == 3 and g(hn, 'tzG1') == 'Hispanic' and g(hn, 'tzSRC') == 1 and
      g(hn, 'tzM1') == 15.89 and U(rn) == 'TTestLabG: t(73) = -2.20, p = 0.031, two-tailed', (en, rn))


def s_typed_big(h):
    h.choose(4)                                          # example 3, age at arrest
    h.press('Enter')
    h.choose('Edit the numbers')
    h.choose(1)                                          # type the numbers
    h.answer({'tzM1': 1E60})
    h.choose('Quit')                                     # the menu after the box


TYPED = 'A number you typed has more than 50 digits: too large to work with. Choose Edit the numbers to change it.'
(hn, rn, en), (ho, ro, eo) = both(s_typed_big)
check('M5 a typed Mean 1 of 1E60: "%s", then the menu; the number stays as typed (the form shows it next time); '
      'beta 1 worked a t from it ("%s")' % (TYPED, U(ro or eo or '')),
      en is None and box(hn) == [TYPED] and rn == 'TTestLabG' and g(hn, 'tzM1') == 1E60 and g(hn, 'tzOK') == 0 and
      OLD is not None and not any('50 digits' in x for x in box(ho)), (en, rn, box(hn), ro, eo))
typed = []
for kv in (dict(tzS2=1E50), dict(tzN1=1E50), dict(tzM2=-1E55), dict(tzS1=float('inf'))):
    hh = H()
    put(hh, tzTY=2, tzSRC=1, tzM1=5, tzS1=2, tzN1=10, tzM2=4, tzS2=2, tzN2=10)
    put(hh, **kv)
    hh.execute('tz_Calc()')
    typed.append((list(kv)[0], g(hh, 'tzOK'), g(hh, 'tzMSG') == TYPED))
check('M5 every typed field is checked (SD 2 = 1E50, N 1 = 1E50, Mean 2 = -1E55, an infinite SD 1): %s' % typed,
      all(t[1] == 0 and t[2] for t in typed), typed)


def s_dep_big(h):
    h.choose(1)
    h.tap(230, 71)
    h.tap(290, 230)                                      # dependent
    h.choose(2)                                          # type the mean and SD of the differences
    h.answer({'dm': 0.5, 'dsd': 1, 'dn': 1E50})
    h.choose(1)
    h.choose(3)
    h.choose('Quit')


(hn, rn, en), (ho, ro, eo) = both(s_dep_big)
check('M5 dependent samples, N pairs typed as 1E50: the same sentence; beta 1 worked a t on 1E50 - 1 df ("%s")'
      % U(ro or eo or ''),
      en is None and box(hn) == [TYPED] and rn == 'TTestLabG' and OLD is not None and
      not any('50 digits' in x for x in box(ho)), (en, rn, box(hn), ro, eo))

# a typed N over 1,000,000: the Prime's STUDENT_CDF loses its digits at a huge df (Virtual Calculator, 1 Nov 2026)
NMSG = "N can be at most 1,000,000: the calculator's t distribution loses accuracy far beyond it (and there t equals z)."
ncap = []
for ty, kv, refuse in ((2, dict(tzN1=1000001), True), (1, dict(tzN2=1E12), True), (2, dict(tzN1=1000000), False),
                       (3, dict(tzNP=2000000), True), (3, dict(tzNP=1000000), False)):
    hh = H()
    put(hh, tzTY=ty, tzSRC=1, tzTL=0, tzAL=0.05, tzM1=5, tzS1=2, tzN1=10, tzM2=4, tzS2=2, tzN2=10, tzMD=0.5, tzSDv=1,
        tzNP=5)
    put(hh, **kv)
    hh.execute('tz_Calc()')
    if ty == 3:
        want_t = 0.5 / (1 / g(hh, 'tzNP') ** 0.5)
    else:
        want_t = stats.ttest_ind_from_stats(5, 2, g(hh, 'tzN1'), 4, 2, g(hh, 'tzN2'), equal_var=(ty == 1)).statistic
    ok_ = (g(hh, 'tzOK') == 0 and g(hh, 'tzMSG') == NMSG) if refuse else \
          (g(hh, 'tzOK') == 1 and rel(g(hh, 'tzT'), want_t) < 1e-9)
    ncap.append((ty, kv, 'refused' if g(hh, 'tzOK') == 0 else 't %.4f' % g(hh, 'tzT'), ok_))
check('M7 a typed N may be at most 1,000,000 (N 1 = 1,000,001 and N 2 = 1E12 refused, N 1 = 1,000,000 accepted; '
      'N pairs 2,000,000 refused, 1,000,000 accepted, t against SciPy): %s' % [(c[0], c[2]) for c in ncap],
      all(c[3] for c in ncap), ncap)


def s_typed_bign(h):
    h.choose(1)
    for x, y in [(90, 71), (40, 133), (290, 230)]:
        h.tap(x, y)
    h.choose(1)                                          # type the numbers
    h.answer({'tzM1': 5, 'tzS1': 2, 'tzN1': 10, 'tzM2': 4, 'tzS2': 2, 'tzN2': 1E12})
    h.choose(1)
    h.choose(3)
    h.choose('Quit')


(hn, rn, en), (ho, ro, eo) = both(s_typed_bign)
check('M7 the whole flow with N 2 = 1E12: the box says why, then the menu; beta 1 went on ("%s")' % U(ro or eo or ''),
      en is None and box(hn) == [NMSG] and rn == 'TTestLabG' and OLD is not None and
      not any('1,000,000' in x for x in box(ho)), (en, rn, box(hn), ro, eo))

# the largest numbers accepted: every step draws, for every test, and t agrees with SciPy
mx = []
for ty in (1, 2):
    hh = H()
    put(hh, tzTY=ty, tzSRC=1, tzTL=0, tzAL=0.05, tzM1=9.9E49, tzS1=9.9E49, tzN1=3, tzM2=-9.9E49, tzS2=1E-300, tzN2=4)
    hh.execute('tz_Calc()')
    errp = None
    try:
        for st in range(1, 6):
            hh.execute('tz_Page(%d)' % st)
    except Exception as e:
        errp = str(e)[:100]
    want_t = stats.ttest_ind_from_stats(9.9E49, 9.9E49, 3, -9.9E49, 1E-300, 4, equal_var=(ty == 1)).statistic
    mx.append((ty, g(hh, 'tzOK'), errp, round(g(hh, 'tzT'), 9), round(float(want_t), 9)))
hh = H()
put(hh, tzTY=3, tzSRC=1, tzTL=0, tzAL=0.05, tzMD=9.9E49, tzSDv=9.9E49, tzNP=10)
hh.execute('tz_Calc()')
errp = None
try:
    for st in range(1, 6):
        hh.execute('tz_Page(%d)' % st)
except Exception as e:
    errp = str(e)[:100]
mx.append((3, g(hh, 'tzOK'), errp, round(g(hh, 'tzT'), 9), round(10 ** 0.5, 9)))
hh = H({'D1': [9.9E49, -9.9E49, 9.9E49], 'D2': [-9.9E49, 9.9E49, -9.9E49]})
put(hh, tzTY=3)
hh.choose(1)
hh.execute('tz_AskData()')
hh.execute('tz_Calc()')
errp = None
try:
    for st in range(1, 6):
        hh.execute('tz_Page(%d)' % st)
except Exception as e:
    errp = str(e)[:100]
dd = np.array([9.9E49, -9.9E49, 9.9E49]) - np.array([-9.9E49, 9.9E49, -9.9E49])
mx.append(('pairs', g(hh, 'tzOK'), errp, round(g(hh, 'tzT'), 9), round(float(stats.ttest_1samp(dd, 0).statistic), 9)))
check('M6 the largest numbers accepted (means and SDs of 9.9E49, an SD of 1E-300, pairs of 9.9E49): all five steps '
      'draw for pooled, separate, dependent typed and pairs, and t agrees with SciPy: %s' % mx,
      all(m[1] == 1 and m[2] is None and abs(m[3] - m[4]) < 1e-6 * max(1, abs(m[4])) for m in mx), mx)

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
check('G1 no "!=" in the code (Lessons Learned: "<>" on the device); %d routines, all tagged tz_; %d file-level '
      'variables, all tagged tz; one EXPORT, TTESTLABG' % (len(routines), len(filevars)),
      not ne and routines and all(r.startswith('tz_') for r in routines) and
      all(v.startswith('tz') for v in filevars) and exports == ['TTESTLABG'], (ne, routines, filevars, exports))
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
tag = [t for t in rep if t.startswith(os.path.splitext(os.path.basename(PROG))[0])]
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
    for x in f['straddles']:
        if not x['firm']:
            print('     (straddle, not firm) %s | edge %s' % (x['text'][:60], x.get('edge')))
    for x in f['overruns']:
        if not x['firm']:
            print('     (overrun at the conservative width, not firm) %s -> %s px' % (x['text'][:60], x.get('right')))
check('D1 no firm overlap, frame straddle or overrun on any TTestLabG screen drawn (%s)' % (tag[:1]),
      bool(tag) and not firm, firm[:8])

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for x in FAIL:
    print('  FAILED: ' + x)
sys.exit(1 if FAIL else 0)
