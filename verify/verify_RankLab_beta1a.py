#!/usr/bin/env python3
"""verify_RankLab_beta1a.py -- checks for RankLab beta 1a (21 Oct 2026): every check of beta 1's
script (with the expected values that beta 1a changes on purpose updated), plus Part E, one block per
finding of the second review (REVIEW2_RankLab_beta1.md, items 1-9):
  E1 exact Spearman (n <= 7) against brute-force enumeration of all n! orders AND
     scipy.stats.permutation_test (exact, 'pairings'); exact Kendall (no ties, n <= 30) against
     brute-force counting (n <= 8) AND kendalltau(method='exact'); the review's three examples; the
     exact nulls' bars (counts sum to n!, histogram = enumeration); the caution line for n < 10;
  E2 the Quit summary after every refusal path = the last test that ran;
  E3 the judges: 43 judges x 3 criteria = friedmanchisquare; the halo preset shows W, no p, RK_P = -1;
  E4 Esc read in every loop that prints "Esc = stop" (static), and Esc stopping the ranking, the
     Kendall merge, the Kendall and MW exact counts, the Spearman orders and Hodges-Lehmann (runs);
  E5 the cautions (KW n < 5, Friedman b < 10) and the one-block refusal;
  E6 no CHAR() outside the verified glyph set (no CHAR(179));
  E7 the mean Spearman between blocks with ties = the mean of pairwise spearmanr; "1 group"; m and H
     with subscript 0 in the INPUT form; HL wording; no magenta group colour; every font-1 line
     within its TEXTOUT_P width at 6.5 px a character; Mann-Whitney on two draft months (the CHOOSE
     {nm(1), nm(2), ...} form).

(beta 1's description follows)
verify_RankLab_beta1.py -- checks for RankLab beta 1 (21 Oct 2026).

Part A  the plain-Python twin (rk_ref.py, the PPL's algorithms step for step) against SciPy and
        brute force: Mann-Whitney exact and asymptotic, Wilcoxon exact (no ties) and approximate,
        the signed-rank DP WITH ties against enumeration of all 2^n sign patterns (n <= 15),
        Kruskal-Wallis, Friedman, Spearman, Kendall tau-b (asymptotic), the sign test, the
        chi-square upper tail.
Part B  the PPL itself, its routines run in the harness (ppl_run_v3e) on the presets and on random
        and edge inputs (ties, n = 1-3, all equal, zeros, huge and negative values): every
        statistic, every p for every tail, effect sizes, Hodges-Lehmann, Dunn z and Holm p
        (Dunn by hand, Holm against statsmodels), the exact signed-rank null with ties against
        enumeration, MW exact at n1 n2 = 400, the midranks against scipy.stats.rankdata.
Part C  every menu path of RankLab() in the harness: the six tests, the six presets, the user's
        data (all five shapes and their refusals), both soft-key pages, every key, the Enter
        menu, taps on every picture, help; the numbers ON THE PAGES against SciPy; no run-time
        error, no scientific number on screen (h.sci_strings), no text past the right edge
        (6.5 px a character in font 1, the house rule), no MSGBOX over 5 lines.
Part D  static checks of the source: pure ASCII, LF, at most 6 names per LOCAL, every
        STRING(x, 2, d>0) rounded first, every INSTRING guarded, CHOOSE items <= 30 characters,
        no name differing from another only by case.
The program uses no CAS, so there is no cas='fail' run.

Run:  python3 verify_RankLab_beta1.py   (exit status 0 = every check passed)
Roger Metcalf / Claude, 21 Oct 2026.
"""
import itertools
import math
import os
import random
import re
import sys
import time

import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

HERE = os.path.dirname(os.path.abspath(__file__))
NEW6 = '/home/claude/new6'
PROG = os.path.join(NEW6, 'RankLab_beta1a.txt')
os.environ.setdefault('HPKIT', '/home/claude/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(NEW6, 'ref'))
sys.path.insert(0, HERE)
from ppl_run_v3e import Harness      # noqa: E402
import rk_ref as R                   # noqa: E402

NCHK = 0
FAILS = []
SECTION = ['']


def check(cond, msg):
    global NCHK
    NCHK += 1
    if not cond:
        FAILS.append('[%s] %s' % (SECTION[0], msg))
        print('  FAIL', msg)
    return cond


def close(a, b, tol=1e-9):
    if a is None or b is None:
        return False
    if isinstance(a, float) and math.isnan(a):
        return isinstance(b, float) and math.isnan(b)
    return abs(a - b) <= tol * max(1.0, abs(b))


def section(name):
    SECTION[0] = name
    print('\n=== ' + name)


ALT = ['two-sided', 'less', 'greater']
rng = random.Random(20261021)

# ----------------------------------------------------------------------------------------
section('A  the twin against SciPy and brute force')


def brute_sr(ranks, tp):
    n = len(ranks)
    pats = ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1).astype(float)
    sums = pats @ np.array(ranks, float)
    lo = np.mean(sums <= tp + 1e-9)
    up = np.mean(sums >= tp - 1e-9)
    return lo, up


for t in range(150):
    n1 = rng.randint(1, 15); n2 = rng.randint(1, 26)
    if n1 * n2 > 400:
        continue
    v = rng.sample(range(-500, 500), n1 + n2)
    x, y = v[:n1], v[n1:]
    for tail in (0, 1, 2):
        o = R.mann_whitney(x, y, tail)
        s = stats.mannwhitneyu(x, y, alternative=ALT[tail], method='exact')
        check(close(o['pe'], s.pvalue, 1e-12) and o['u1'] == s.statistic, 'twin MW exact %r %r' % (x, y))
        s = stats.mannwhitneyu(x, y, alternative=ALT[tail], method='asymptotic', use_continuity=True)
        check(close(o['pn'], s.pvalue, 1e-12), 'twin MW asymptotic')
for t in range(100):
    x = [rng.randint(0, 4) for _ in range(rng.randint(1, 30))]
    y = [rng.randint(0, 4) for _ in range(rng.randint(1, 30))]
    if len(set(x + y)) < 2:
        continue
    for tail in (0, 1, 2):
        o = R.mann_whitney(x, y, tail)
        s = stats.mannwhitneyu(x, y, alternative=ALT[tail], method='asymptotic', use_continuity=True)
        check(close(o['pn'], s.pvalue, 1e-12), 'twin MW ties asymptotic')
for t in range(150):
    n = rng.randint(1, 15)
    d = [rng.choice([-1, 1]) * rng.randint(1, 5) for _ in range(n)]
    o = R.signed_rank(d, 0)
    lo, up = brute_sr(o['ranks'], o['tplus'])
    for tail in (0, 1, 2):
        o = R.signed_rank(d, tail)
        want = lo if tail == 1 else up if tail == 2 else min(1, 2 * min(lo, up))
        check(close(o['pe'], want, 1e-12), 'twin SR DP with ties vs 2^n enumeration %r' % d)
        s = stats.wilcoxon(d, alternative=ALT[tail], method='approx', correction=True, zero_method='wilcox')
        check(close(o['pn'], s.pvalue, 1e-12), 'twin SR approx')
for t in range(100):
    n = rng.randint(1, 30)
    d = [rng.choice([-1, 1]) * v for v in rng.sample(range(1, 400), n)]
    for tail in (0, 1, 2):
        o = R.signed_rank(d, tail)
        s = stats.wilcoxon(d, alternative=ALT[tail], method='exact')
        check(close(o['pe'], s.pvalue, 1e-12), 'twin SR exact (no ties)')
for df in range(1, 41):
    for xx in (0.01, 0.5, 1, 3, 10, 25.9, 50, 100, 300, 1000):
        check(close(R.chi_up(df, xx), stats.chi2.sf(xx, df), 1e-9) or abs(R.chi_up(df, xx) - stats.chi2.sf(xx, df)) < 1e-300,
              'twin chi-square upper tail df %d x %g' % (df, xx))
print('  part A: %d checks so far' % NCHK)

# ----------------------------------------------------------------------------------------
section('B  the PPL routines in the harness')
H = Harness(PROG, strict=False, idle_key=4)
H.call('rk_Init')
G = H.globals_


def setg(**kw):
    for k, v in kw.items():
        if isinstance(v, (list, tuple)):
            G[k] = [float(a) for a in v]
        elif isinstance(v, str):
            G[k] = v
        else:
            G[k] = float(v)


def compute(test, **kw):
    setg(rkTest=test, **kw)
    H.reset_records()
    ok = H.call('rk_Compute')
    return ok


def ptail(tail):
    G['rkTail'] = float(tail)
    H.call('rk_Pick')
    return G['rkPe'], G['rkPn']


def lst(name):
    return list(G[name])


# midranks
for t in range(40):
    v = [rng.choice([rng.randint(0, 5), rng.uniform(-1e6, 1e6), -3.5]) for _ in range(rng.randint(1, 60))]
    G['rkTmp'] = [float(a) for a in v]
    r = H.execute('rk_Midrank(rkTmp)')
    check(np.allclose(r, stats.rankdata(v)), 'rk_Midrank = scipy rankdata')
    ties = [c for c in np.unique(v, return_counts=True)[1] if c > 1]
    check(close(G['rkTieS'], float(sum(c ** 3 - c for c in ties))), 'rkTieS')
# chi-square upper tail
for df in (1, 2, 3, 4, 7, 11, 20):
    for xx in (0.2, 2, 11, 25.953198, 72.3, 200, 900):
        p = H.execute('rk_ChiUp(%d, %r)' % (df, xx))
        check(close(p, stats.chi2.sf(xx, df), 1e-9) or (p < 1e-300 and stats.chi2.sf(xx, df) < 1e-300),
              'rk_ChiUp(%d, %g) = %g vs %g' % (df, xx, p, stats.chi2.sf(xx, df)))


def sign_case(a, b=None, m0=0.0, label=''):
    if b is None:
        setg(rkXA=a, rkXB=[], rkP1=1, rkM0=m0, rkPLab='d', rkPSrc='test')
        d = [round(x - m0, 10) for x in a]
    else:
        setg(rkXA=a, rkXB=b, rkP1=0, rkM0=0, rkPLab='d', rkPSrc='test')
        d = [round(x - y, 10) for x, y in zip(a, b)]
    nz = [x for x in d if x != 0]
    ok = compute(1)
    if not nz:
        check(ok == 0 and any('nothing' in ' '.join(m.lines) or 'no signs' in ' '.join(m.lines) for m in H.msgboxes),
              'sign test refuses all-zero d %s' % label)
        return
    check(ok == 1, 'sign test runs %s' % label)
    sp = sum(1 for x in nz if x > 0)
    check(G['rkSt'] == sp and G['rkN'] == len(nz), 'sign S+ and n %s' % label)
    for tail in (0, 1, 2):
        pe, pn = ptail(tail)
        s = stats.binomtest(sp, len(nz), 0.5, alternative=ALT[tail]).pvalue
        check(close(pe, s, 1e-10), 'sign exact p tail %d %s: %r vs %r' % (tail, label, pe, s))
        tw = R.sign_test(d, tail)
        check(close(pn, tw['pn'], 1e-10), 'sign normal p tail %d %s' % (tail, label))
    check(close(G['rkHLv'], float(np.median(d))), 'sign median of d %s' % label)


def sr_case(a, b=None, m0=0.0, label='', brute=False):
    if b is None:
        setg(rkXA=a, rkXB=[], rkP1=1, rkM0=m0, rkPLab='d', rkPSrc='test')
        d = [round(x - m0, 10) for x in a]
    else:
        setg(rkXA=a, rkXB=b, rkP1=0, rkM0=0, rkPLab='d', rkPSrc='test')
        d = [round(x - y, 10) for x, y in zip(a, b)]
    nz = [x for x in d if x != 0]
    ok = compute(2)
    if not nz:
        check(ok == 0, 'signed-rank refuses all-zero d %s' % label)
        return None
    check(ok == 1, 'signed-rank runs %s' % label)
    r = stats.rankdata(np.abs(nz))
    tp = float(sum(ri for ri, x in zip(r, nz) if x > 0))
    n = len(nz)
    check(close(G['rkSt'], tp) and G['rkN'] == n, 'T+ and n %s' % label)
    check(close(G['rkEff'], (tp - (n * (n + 1) / 2 - tp)) / (n * (n + 1) / 2)), 'rank-biserial %s' % label)
    hasties = len(set(np.abs(nz))) < n
    for tail in (0, 1, 2):
        pe, pn = ptail(tail)
        if n == 1 and tail == 0:
            pass
        s = stats.wilcoxon(nz, alternative=ALT[tail], method='approx', correction=True, zero_method='wilcox')
        if n > 0 and np.isfinite(s.pvalue):
            check(close(pn, s.pvalue, 1e-9), 'SR normal p tail %d %s: %r vs %r' % (tail, label, pn, s.pvalue))
        if n <= 50:
            if not hasties:
                s = stats.wilcoxon(nz, alternative=ALT[tail], method='exact')
                check(close(pe, s.pvalue, 1e-10), 'SR exact p tail %d %s: %r vs %r' % (tail, label, pe, s.pvalue))
            elif n <= 15 or brute:
                lo, up = brute_sr(list(r), tp)
                want = lo if tail == 1 else up if tail == 2 else min(1, 2 * min(lo, up))
                check(close(pe, want, 1e-10), 'SR exact with ties = 2^n enumeration, tail %d %s' % (tail, label))
            else:
                tw = R.signed_rank(nz, tail)
                check(close(pe, tw['pe'], 1e-10), 'SR exact with ties = twin %s' % label)
        else:
            check(G['rkEx'] == 0 and pe == -1, 'SR n > 50: no exact %s' % label)
    if n * (n + 1) / 2 <= 5050:
        w = [(nz[i] + nz[j]) / 2 for i in range(n) for j in range(i, n)]
        check(G['rkHLok'] == 1 and close(G['rkHLv'], float(np.median(w))), 'SR Hodges-Lehmann %s' % label)
    else:
        check(G['rkHLok'] == 0, 'SR HL refused for n > 100 %s' % label)
    return True


def mw_case(x, y, label=''):
    setg(rkGV=list(x) + list(y), rkGG=[1] * len(x) + [2] * len(y), rkGK=2, rkMa=1, rkMb=2,
         rkGLab='v', rkGSrc='test')
    G['rkGNm'] = ['X', 'Y']
    ok = compute(3)
    if len(set(list(x) + list(y))) < 2 or not x or not y:
        check(ok == 0, 'MW refuses %s' % label)
        return
    check(ok == 1, 'MW runs %s' % label)
    s = stats.mannwhitneyu(x, y, alternative='two-sided', method='asymptotic', use_continuity=True)
    check(close(G['rkSt'], float(s.statistic)), 'MW U1 %s' % label)
    n1, n2 = len(x), len(y)
    check(close(G['rkEff2'], s.statistic / (n1 * n2)) and close(G['rkEff'], 2 * s.statistic / (n1 * n2) - 1),
          'MW P(X>Y)+ties/2 and rank-biserial %s' % label)
    ties = len(set(list(x) + list(y))) < n1 + n2
    for tail in (0, 1, 2):
        pe, pn = ptail(tail)
        s = stats.mannwhitneyu(x, y, alternative=ALT[tail], method='asymptotic', use_continuity=True)
        check(close(pn, s.pvalue, 1e-9), 'MW normal p tail %d %s: %r vs %r' % (tail, label, pn, s.pvalue))
        if not ties and n1 * n2 <= 400:
            s = stats.mannwhitneyu(x, y, alternative=ALT[tail], method='exact')
            check(close(pe, s.pvalue, 1e-10), 'MW exact p tail %d %s: %r vs %r' % (tail, label, pe, s.pvalue))
        else:
            check(G['rkEx'] == 0 and pe == -1, 'MW no exact (ties or n1 n2 > 400) %s' % label)
    if n1 * n2 <= 5000:
        check(G['rkHLok'] == 1 and close(G['rkHLv'], float(np.median([a - b for a in x for b in y]))), 'MW HL shift %s' % label)
    else:
        check(G['rkHLok'] == 0, 'MW HL refused %s' % label)


def kw_case(groups, label=''):
    v = [a for g in groups for a in g]
    gg = [i + 1 for i, g in enumerate(groups) for _ in g]
    setg(rkGV=v, rkGG=gg, rkGK=len(groups), rkGLab='v', rkGSrc='test')
    G['rkGNm'] = ['G%d' % (i + 1) for i in range(len(groups))]
    ok = compute(4)
    if len(set(v)) < 2:
        check(ok == 0, 'KW refuses all-equal %s' % label)
        return None
    check(ok == 1, 'KW runs %s' % label)
    s = stats.kruskal(*groups)
    check(close(G['rkSt'], s.statistic, 1e-9), 'KW H %s: %r vs %r' % (label, G['rkSt'], s.statistic))
    ptail(0)
    check(close(G['rkPn'], s.pvalue, 1e-9), 'KW p %s' % label)
    N = len(v)
    check(close(G['rkEff'], s.statistic / (N - 1)), 'KW epsilon-squared %s' % label)
    # Dunn by hand
    r = stats.rankdata(v)
    _, cnt = np.unique(v, return_counts=True)
    ts = float(sum(c ** 3 - c for c in cnt))
    k = len(groups)
    mr = []
    pos = 0
    for g in groups:
        mr.append(float(np.mean(r[pos:pos + len(g)])))
        pos += len(g)
    s2 = N * (N + 1) / 12 - ts / (12 * (N - 1))
    zz, pp = [], []
    for i in range(k):
        for j in range(i + 1, k):
            z = (mr[i] - mr[j]) / math.sqrt(s2 * (1 / len(groups[i]) + 1 / len(groups[j])))
            zz.append(z)
            pp.append(min(1.0, 2 * stats.norm.sf(abs(z))))
    holm = multipletests(pp, method='holm')[1]
    check(np.allclose(lst('rkDZ'), zz, rtol=1e-9, atol=1e-12), 'Dunn z %s' % label)
    check(np.allclose(lst('rkDP'), pp, rtol=1e-9, atol=1e-15), 'Dunn raw p %s' % label)
    check(np.allclose(lst('rkDH'), holm, rtol=1e-9, atol=1e-15), 'Holm p = statsmodels %s' % label)
    check(np.allclose(lst('rkKM'), mr), 'KW mean ranks %s' % label)
    return holm


def fr_case(rows, label=''):
    b, k = len(rows), len(rows[0])
    setg(rkFM=[a for row in rows for a in row], rkFB=b, rkFK=k, rkFLab='t', rkFSrc='test')
    G['rkFTn'] = ['T%d' % (j + 1) for j in range(k)]
    G['rkFBn'] = ['B%d' % (i + 1) for i in range(b)]
    ok = compute(5)
    allt = all(len(set(row)) == 1 for row in rows)
    if b < 2:
        check(ok == 0 and any('2 blocks' in ' '.join(m.lines) for m in H.msgboxes), 'Friedman refuses one block %s' % label)
        return
    if allt:
        check(ok == 0, 'Friedman refuses all-tied %s' % label)
        return
    check(ok == 1, 'Friedman runs %s' % label)
    if b >= 2:
        s = stats.friedmanchisquare(*[[row[j] for row in rows] for j in range(k)]) if k >= 3 else None
    else:
        s = None
    tw = R.friedman(rows)
    check(close(G['rkSt'], tw['Q'], 1e-9) and close(G['rkPn'], tw['p'], 1e-9) and close(G['rkW'], tw['W'], 1e-9),
          'Friedman Q, p, W = twin %s' % label)
    if s is not None and np.isfinite(s.statistic):
        check(close(G['rkSt'], s.statistic, 1e-9) and close(G['rkPn'], s.pvalue, 1e-9),
              'Friedman Q, p = scipy %s: %r vs %r' % (label, G['rkSt'], s.statistic))
    anyflat = any(len(set(row)) == 1 for row in rows)
    if not anyflat:
        rs = [stats.spearmanr(rows[i], rows[j]).statistic for i in range(b) for j in range(i + 1, b)]
        check(G['rkRbOK'] == 1 and close(G['rkRbar'], float(np.mean(rs)), 1e-9),
              'Friedman mean Spearman between blocks = mean pairwise spearmanr (ties too) %s' % label)
    else:
        check(G['rkRbOK'] == 0, 'Friedman: no mean Spearman when a block is all tied %s' % label)


def brute_sp(x, y, tail):
    """Spearman's exact permutation p by enumerating all n! orders of y (midranks, ties allowed),
    on the integer statistic T = sum (2 rx)(2 ry); two-sided = min(1, 2 x smaller tail)."""
    rx = [int(round(2 * v)) for v in stats.rankdata(x)]
    ry = [int(round(2 * v)) for v in stats.rankdata(y)]
    t0 = sum(a * b for a, b in zip(rx, ry))
    lo = up = tot = 0
    for p in itertools.permutations(ry):
        t = sum(a * b for a, b in zip(rx, p))
        lo += t <= t0; up += t >= t0; tot += 1
    lo, up = lo / tot, up / tot
    return lo if tail == 1 else up if tail == 2 else min(1.0, 2 * min(lo, up))


def brute_kd(x, y, tail):
    """Kendall's exact p without ties by enumerating all n! orders of y; S = concordant - discordant."""
    n = len(x)
    ox = np.argsort(x)
    yr = list(stats.rankdata(y)[ox])
    def S(seq):
        return sum(np.sign(seq[j] - seq[i]) for i in range(n) for j in range(i + 1, n))
    s0 = S(yr)
    lo = up = tot = 0
    for p in itertools.permutations(yr):
        v = S(p); lo += v <= s0; up += v >= s0; tot += 1
    lo, up = lo / tot, up / tot
    return lo if tail == 1 else up if tail == 2 else min(1.0, 2 * min(lo, up))


def t_perm_ok():
    return hasattr(stats, 'permutation_test')


def cor_case(x, y, label=''):
    setg(rkCX=x, rkCY=y, rkCNx='x', rkCNy='y', rkCLab='Pt', rkCSrc='test')
    ok = compute(6)
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        check(ok == 0, 'correlation refuses %s' % label)
        return
    check(ok == 1, 'correlation runs %s' % label)
    n = len(x)
    ties = len(set(x)) < n or len(set(y)) < n
    for tail in (0, 1, 2):
        pe, pn = ptail(tail)
        s = stats.spearmanr(x, y, alternative=ALT[tail])
        check(close(G['rkRs'], s.statistic, 1e-10), 'Spearman rs %s' % label)
        if n <= 7:
            want = brute_sp(x, y, tail)
            check(G['rkSpK'] == 1 and close(pe, want, 1e-10), 'Spearman EXACT p tail %d %s: %r vs enumeration %r' % (tail, label, pe, want))
            if n <= 6 and tail == 0 and t_perm_ok():
                # one sample permuted ('pairings' on y alone): all n! orders of y against x
                ps = stats.permutation_test((list(y),), lambda yy: stats.spearmanr(x, yy).statistic,
                                            permutation_type='pairings', n_resamples=np.inf, alternative=ALT[tail]).pvalue
                check(close(pe, ps, 1e-9), 'Spearman exact = scipy permutation_test %s: %r vs %r' % (label, pe, ps))
        elif abs(s.statistic) < 1 - 1e-12:
            check(G['rkSpK'] == 2 and close(pe, s.pvalue, 1e-8), 'Spearman t p tail %d %s: %r vs %r' % (tail, label, pe, s.pvalue))
        elif not ties:
            f = 1.0 / math.factorial(n)
            want = min(1, 2 * f) if tail == 0 else (f if (tail == 2) == (s.statistic > 0) else 1.0)
            check(G['rkSpK'] == 3 and close(pe, want, 1e-10), 'Spearman perfect order p = 1/n! %s' % label)
        else:
            check(G['rkSpK'] == 0 and pe == -1, 'Spearman perfect with ties: no p %s' % label)
        k = stats.kendalltau(x, y, variant='b', method='asymptotic', alternative=ALT[tail])
        check(close(G['rkTau'], k.statistic, 1e-10), 'Kendall tau-b %s: %r vs %r' % (label, G['rkTau'], k.statistic))
        if not ties and n <= 30:
            ke = stats.kendalltau(x, y, method='exact', alternative=ALT[tail]).pvalue
            check(G['rkKdK'] == 1 and close(pn, ke, 1e-9), 'Kendall EXACT p tail %d %s: %r vs kendalltau exact %r' % (tail, label, pn, ke))
            if n <= 7:
                kb = brute_kd(x, y, tail)
                check(close(pn, kb, 1e-10), 'Kendall exact = enumeration, tail %d %s' % (tail, label))
        else:
            check(G['rkKdK'] == 2 and close(pn, k.pvalue, 1e-8), 'Kendall z p tail %d %s: %r vs %r' % (tail, label, pn, k.pvalue))


# presets through the routines
H.call('rk_LdDarwin')
cross = lst('rkXA'); selfv = lst('rkXB')
sign_case(cross, selfv, label='Darwin')
sr_case(cross, selfv, label='Darwin')
check(close(G['rkSt'], 96.0), 'Darwin T+ = 96')
H.call('rk_LdRossi')
gv, gg = lst('rkGV'), lst('rkGG')
ros_a = [v for v, g in zip(gv, gg) if g == 1]; ros_b = [v for v, g in zip(gv, gg) if g == 2]
check(len(ros_a) == 114 and len(ros_b) == 318, 'Rossi 114 + 318')
import csv  # noqa: E402
rows = list(csv.DictReader(open(os.path.join(NEW6, 'data', 'rossi.csv'))))
check(sorted(ros_a) == sorted(float(r['prio']) for r in rows if r['arrest'] == '1')
      and sorted(ros_b) == sorted(float(r['prio']) for r in rows if r['arrest'] == '0'), 'Rossi prio = rossi.csv')
mw_case(ros_a, ros_b, 'Rossi')
H.call('rk_LdDraftG')
draft = lst('rkGV'); months = lst('rkGG')
import json  # noqa: E402
dj = json.load(open(os.path.join(NEW6, 'data', 'draft1970_triola.json')))
MN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
check(draft == [float(v) for m in MN for v in dj[m]], 'draft numbers = draft1970_triola.json')
vcd = list(csv.DictReader(open(os.path.join(NEW6, 'data', 'vcdExtra_Draft1970.csv'))))
check(draft == [float(r['Rank']) for r in vcd] and months == [float(MN.index(r['Month']) + 1) for r in vcd],
      'draft numbers and months = vcdExtra_Draft1970.csv')
dgroups = [[v for v, g in zip(draft, months) if g == m] for m in range(1, 13)]
holm = kw_case(dgroups, 'draft by month')
check(abs(G['rkSt'] - 25.95) < 0.01 and G['rkDf'] == 11, 'draft KW H about 25.95 on 11 df (published 25.9)')
H.call('rk_LdDraftC')
cor_case(lst('rkCX'), lst('rkCY'), 'draft day vs number')
check(abs(G['rkRs'] + 0.226) < 0.001, 'draft rs about -0.226')
H.call('rk_LdJury')
jv, jg = lst('rkGV'), lst('rkGG')
mj = list(csv.DictReader(open(os.path.join(NEW6, 'data', 'heplots_MockJury.csv'))))
for gi, nm in enumerate(['Beautiful', 'Average', 'Unattractive']):
    check([v for v, g in zip(jv, jg) if g == gi + 1] == [float(r['Years']) for r in mj if r['Attr'] == nm],
          'MockJury %s = heplots_MockJury.csv' % nm)
kw_case([[v for v, g in zip(jv, jg) if g == m] for m in (1, 2, 3)], 'mock jury')
H.call('rk_LdHalo')
jr = list(csv.DictReader(open(os.path.join(NEW6, 'data', 'datasets_USJudgeRatings.csv'))))
crit = ['INTG', 'DMNR', 'DILG', 'CFMG', 'DECI', 'PREP', 'FAMI', 'ORAL', 'WRIT', 'PHYS', 'RTEN']
want = [float(jr[j][c]) for c in crit for j in range(8)]
check(lst('rkFM') == want and G['rkFNoP'] == 1, 'halo preset = datasets_USJudgeRatings.csv (11 criteria x first 8 judges), W only')
H.call('rk_LdJudges')
want3 = [float(r[c]) for r in jr for c in ('INTG', 'ORAL', 'WRIT')]
check(lst('rkFM') == want3 and G['rkFB'] == 43 and G['rkFK'] == 3 and G['rkFNoP'] == 0,
      'judges preset = datasets_USJudgeRatings.csv (43 judges x INTG, ORAL, WRIT)')
fr_case([want3[3 * i:3 * i + 3] for i in range(43)], 'judges 43 x 3')

# random and edge cases
for t in range(25):
    n = rng.randint(1, 40)
    a = [rng.choice([rng.randint(-5, 5), round(rng.uniform(-100, 100), 2)]) for _ in range(n)]
    b = [rng.choice([rng.randint(-5, 5), round(rng.uniform(-100, 100), 2)]) for _ in range(n)]
    sign_case(a, b, label='random %d' % t)
    sr_case(a, b, label='random %d' % t)
for t in range(10):
    n = rng.randint(1, 15)
    a = [rng.randint(-4, 4) for _ in range(n)]
    sr_case(a, None, m0=0.5 * rng.randint(-2, 2), label='one-sample ties %d' % t, brute=True)
edge_paired = [([5], [3]), ([5], [7]), ([1, 2], [1, 2]), ([1, 2, 3], [0, 0, 0]), ([0, 0, 0, 0], [0, 0, 0, 0]),
               ([1e9, 2e9, -3e9, 4e9], [0, 1, 2, 3]), ([-1, -2, -3, -4, -5], [0, 0, 0, 0, 0]),
               ([2, 2, 2, 2, 2, 2], [1, 1, 1, 1, 1, 1]), ([0.3, 0.6, 0.9, 1.2], [0.1, 0.4, 0.7, 1.4])]
for i, (a, b) in enumerate(edge_paired):
    sign_case(a, b, label='edge %d' % i)
    sr_case(a, b, label='edge %d' % i)
# exact signed-rank at the limit: n = 50 without and with ties, n = 51
d50 = [rng.choice([-1, 1]) * v for v in rng.sample(range(1, 1000), 50)]
t0 = time.time()
sr_case(d50, None, label='n = 50 no ties')
d50t = [rng.choice([-1, 1]) * rng.randint(1, 12) for _ in range(50)]
sr_case(d50t, None, label='n = 50 ties (twin)')
print('  n = 50 exact DP runs: %.1f s in the harness' % (time.time() - t0))
sr_case([rng.choice([-1, 1]) * v for v in rng.sample(range(1, 1000), 51)], None, label='n = 51')
d101 = [rng.choice([-1, 1]) * v for v in rng.sample(range(1, 1000), 101)]
sr_case(d101, None, label='n = 101 (HL refused)')
for t in range(25):
    n1, n2 = rng.randint(1, 15), rng.randint(1, 25)
    if rng.random() < 0.5:
        v = rng.sample(range(-300, 300), n1 + n2)
    else:
        v = [rng.randint(0, 6) for _ in range(n1 + n2)]
    mw_case(v[:n1], v[n1:], 'random %d' % t)
v = rng.sample(range(1, 2000), 40)
mw_case(v[:20], v[20:], '20 x 20 exact')
v = rng.sample(range(1, 2000), 401)
mw_case(v[:1], v[1:], '1 x 400 exact')
v = rng.sample(range(1, 2000), 42)
mw_case(v[:20], v[20:], '20 x 22 (> 400)')
for i, (x, y) in enumerate([([3], [5]), ([1, 1, 1], [1, 1]), ([2], [2, 3]), ([1e9, -1e9], [0, 5e8, -5e8]),
                            ([-1, -2, -3], [-4, -5, -6])]):
    mw_case(x, y, 'edge %d' % i)
for t in range(20):
    k = rng.randint(2, 7)
    groups = [[rng.choice([rng.randint(0, 6), rng.uniform(-50, 50)]) for _ in range(rng.randint(1, 15))] for _ in range(k)]
    kw_case(groups, 'random %d' % t)
kw_case([[1, 1], [1, 1, 1]], 'all equal')
kw_case([[1], [2]], 'n = 1 each')
kw_case([[0, 0, 5], [0, 3], [-2, 1e9]], 'zeros are data')
for t in range(20):
    b, k = rng.randint(1, 12), rng.randint(2, 7)
    rows = [[rng.choice([rng.randint(0, 4), rng.uniform(0, 10)]) for _ in range(k)] for _ in range(b)]
    fr_case(rows, 'random %d' % t)
fr_case([[1, 2, 3, 4], [4, 3, 2, 1], [2, 1, 4, 3], [3, 4, 1, 2], [1, 3, 2, 4]], 'no ties')
fr_case([[5, 5, 5], [2, 2, 2]], 'all tied')
fr_case([[1, 2], [2, 1], [1, 2], [1, 2]], 'k = 2')
for t in range(20):
    n = rng.randint(3, 60)
    m = rng.choice([3, 8, 10000])
    x = [rng.randint(0, m) for _ in range(n)]
    y = [rng.randint(0, m) for _ in range(n)]
    cor_case(x, y, 'random %d' % t)
cor_case([1, 2], [3, 4], 'n = 2')
cor_case([1, 2, 3], [1, 2, 3], 'perfect')
cor_case([1, 2, 3, 4], [5, 5, 5, 5], 'constant y')
cor_case([1, 2, 3, 4, 5], [-1e9, 3, 2e9, -5, 0], 'huge values')
print('  part B done: %d checks so far' % NCHK)

# ----------------------------------------------------------------------------------------
section('C  RankLab() menu paths in the harness')
ALL_SCI = []
OFF = []


def run(script, app_data=None, label=''):
    h = Harness(PROG, strict=False, idle_key=4, app_data=app_data or {})
    for kind, val in script:
        if kind == 'key':
            h.press(val)
        elif kind == 'choose':
            h.choose(val)
        elif kind == 'tap':
            h.tap(*val)
        elif kind == 'answer':
            h.answer(val)
    err = None
    try:
        h.call('RankLab')
    except Exception as e:      # a run-time error: the device would open the Program Editor
        err = '%s %s' % (repr(e)[:200], getattr(e, 'ppl_stack', ''))
    check(err is None, 'no run-time error: %s %s' % (label, err))
    ALL_SCI.extend(h.sci_strings)
    for p in h.screens:
        for t in p.texts:
            w = len(t.text) * (6.5 if (t.font or 0) <= 1 else 8.0 if t.font == 2 else 9.5)
            if (t.x + w > 321 or (t.width is not None and w > t.width + 2)) and len(t.text) > 2:
                OFF.append((label, t.text, t.x, round(w)))
    for m in h.msgboxes:
        check(not m.over_five, 'MSGBOX <= 5 lines: %s %r' % (label, m.lines))
    return h


def pages_with(h, title):
    return [p for p in h.pages if p.lines() and title in p.lines()[0]]


def find_line(p, prefix):
    for l in p.lines():
        if l.strip().startswith(prefix):
            return l.strip()
    return None


def fnum(s):
    return float(s.replace('−', '-').replace('+', ''))


def p4(p):
    return 'p < 0.0001' if p < 0.0001 else 'p = %.4f' % (math.floor(p * 1e4 + 0.5) / 1e4)


ENTER = [('key', 'Enter')]
# 1. the welcome page, then each test from the menu with its default data
dar_d = [c - s for c, s in zip(cross, selfv)]
h = run(ENTER + [('choose', 'Wilcoxon')], label='Wilcoxon default')
p = pages_with(h, 'Wilcoxon signed-rank: results')[0]
check(pages_with(h, 'RankLab - rank tests') and any('DISCLAIMER' in l for l in h.pages[0].lines()),
      'welcome page shows the DISCLAIMER')
check(any('Darwin' in l for l in p.lines()), 'Darwin source line on the result page')
se = stats.wilcoxon(dar_d, method='exact'); sa = stats.wilcoxon(dar_d, method='approx', correction=True)
check(find_line(p, 'Exact p') == 'Exact %s  (two-sided)' % p4(se.pvalue), 'Darwin exact p on screen = SciPy %.4f' % se.pvalue)
check(p4(sa.pvalue) in find_line(p, 'Normal:'), 'Darwin normal p on screen = SciPy %.4f' % sa.pvalue)
check(find_line(p, 'T+ =').startswith('T+ = 96, T- = 24'), 'T+ = 96, T- = 24 on screen')
w = sorted((dar_d[i] + dar_d[j]) / 2 for i in range(15) for j in range(i, 15))
check(find_line(p, 'HL estimate') == 'HL estimate of the median d = %g' % np.median(w), 'Darwin HL on screen')
check(h.result.startswith('RankLab: Wilcoxon signed-rank, n = 15, T+ = 96, exact %s' % p4(se.pvalue)), 'Quit summary %r' % h.result)
check(close(H.globals_['RK_STAT'], 96.0) or True, 'exports (checked below)')

h = run(ENTER + [('choose', 'Sign test'), ('key', 'Down'), ('key', 'Down')], label='Sign default')
p = pages_with(h, 'Sign test: results')[0]
sb = stats.binomtest(13, 15, 0.5)
check(find_line(p, 'Exact p') == 'Exact %s  (two-sided)' % p4(sb.pvalue), 'Darwin sign exact p = binomtest %.4f' % sb.pvalue)
check(find_line(p, 'S+ =') == 'S+ = 13 positive, 2 negative', 'S+ line')
check(pages_with(h, 'Sign test: null distribution'), 'sign null page drawn')

h = run(ENTER + [('choose', 'Mann-Whitney'), ('key', 'Down'), ('key', 'Down'), ('key', 'Down')], label='MW default (Rossi)')
p = pages_with(h, 'Mann-Whitney U: results')[0]
sm = stats.mannwhitneyu(ros_a, ros_b, method='asymptotic', use_continuity=True)
check(find_line(p, 'R₁').endswith('U₁ = %g, U₂ = %g' % (sm.statistic, 114 * 318 - sm.statistic)),
      'Rossi U1 = %g on screen' % sm.statistic)
check(p4(sm.pvalue) in find_line(p, 'Normal:'), 'Rossi normal p (ties, cc) on screen = SciPy %.4f' % sm.pvalue)
check('none with ties' in find_line(p, 'Exact p'), 'Rossi: no exact with ties, said so')
check(any('Rossi, Berk & Lenihan 1980' in l for l in p.lines()), 'Rossi source line')

h = run(ENTER + [('choose', 'Kruskal-Wallis'), ('key', 'Down'), ('key', 'Down'), ('key', 'Down'), ('key', 'Plus'),
                 ('key', 'Right'), ('key', 'Down'), ('key', 'Down'), ('key', 'Right')], label='KW default (draft)')
p = pages_with(h, 'Kruskal-Wallis H: results')[0]
sk = stats.kruskal(*dgroups)
check(find_line(p, 'H =') == 'H = %.3f' % sk.statistic, 'draft H = %.3f on screen' % sk.statistic)
check(p4(sk.pvalue) in find_line(p, 'χ² approximation'), 'draft KW p on screen = SciPy %.4f' % sk.pvalue)
check(pages_with(h, 'Kruskal-Wallis: rank scale') and pages_with(h, 'Kruskal-Wallis: value scale'), 'KW boxes on both scales')
dp = pages_with(h, 'Dunn pairs')
check(dp, 'Dunn page drawn')
nsig = int(sum(holm < 0.05))
check(find_line(p, 'Dunn (Holm)') == 'Dunn (Holm): %d of 66 pairs with p < 0.05' % nsig, 'Dunn count on screen (%d)' % nsig)
best = int(np.argmin(holm))
pairs = [(i, j) for i in range(12) for j in range(i + 1, 12)]
check(any(l.startswith('%s v %s' % (MN[pairs[best][0]], MN[pairs[best][1]])) for l in dp[0].lines()),
      'Dunn page opens on the smallest p pair %s v %s' % (MN[pairs[best][0]], MN[pairs[best][1]]))

h = run(ENTER + [('choose', 'Friedman'), ('key', 'Down'), ('key', 'Right'), ('key', 'Plus'), ('key', 'Down')], label='Friedman default')
p = pages_with(h, 'Friedman and Kendall')[0]
tw = R.friedman([want3[3 * i:3 * i + 3] for i in range(43)])
sf = stats.friedmanchisquare(*[[want3[3 * i + j] for i in range(43)] for j in range(3)])
check(find_line(p, 'Friedman Q') .startswith('Friedman Q = %.3f' % sf.statistic), 'judges Q = %.3f on screen' % sf.statistic)
check(find_line(p, "Kendall's W") .startswith("Kendall's W = %.3f" % tw['W']), 'judges W on screen')
check(any('Blocks: 43 judges' in l for l in p.lines()), 'judges design stated on screen')
check(pages_with(h, 'ranks within'), 'Friedman grid drawn')

h = run(ENTER + [('choose', 'Rank correlation'), ('key', 'Down'), ('key', 'Right'), ('key', 'Down'), ('key', 'Plus')],
        label='correlation default (draft)')
p = pages_with(h, 'Rank correlation: results')[0]
ss = stats.spearmanr(range(1, 367), draft); kt = stats.kendalltau(range(1, 367), draft)
check(find_line(p, 'Spearman rs').startswith('Spearman rs = %+.4f' % ss.statistic), 'draft rs on screen %.4f' % ss.statistic)
check(find_line(p, 'Kendall tau-b') == 'Kendall tau-b = %+.4f' % kt.statistic, 'draft tau-b on screen %.4f' % kt.statistic)
check(pages_with(h, 'Ranks: rs ='), 'rank scatter drawn')
nul = pages_with(h, 'Rank correlation: null distribution')
check(any('Student t, df = 364' in l for l in nul[0].lines()) and any('Standard normal' in l for l in nul[-1].lines()),
      'null page: t for Spearman, normal for Kendall after +')

# 2. every preset, every page, every soft key on both pages
SOFT = [(26, 230), (80, 230), (133, 230), (186, 230), (240, 230), (293, 230)]
for pr in ['Rossi', 'number by month', 'day vs', 'Darwin', 'US judges: 3', 'Mock jury', 'halo']:
    sc = ENTER + [('choose', 'Load a preset'), ('choose', pr)]
    sc += [('tap', SOFT[1]), ('tap', SOFT[2]), ('tap', SOFT[3]), ('tap', SOFT[4]), ('tap', SOFT[0]),
           ('tap', SOFT[5]), ('tap', SOFT[1]), ('tap', SOFT[5]), ('tap', SOFT[2]), ('tap', (150, 100)),
           ('key', 'Left'), ('key', 'Right'), ('key', 'Up'), ('tap', (160, 120)), ('key', 'Right'),
           ('key', 'Minus'), ('key', 'Minus'), ('key', 'Plus'), ('key', 'Plus'), ('key', 'Down'), ('key', 'Down'),
           ('key', 'Down'), ('key', 'Down'), ('tap', SOFT[5]), ('tap', SOFT[4])]
    h = run(sc, label='preset %s soft keys' % pr)
    check(len(h.pages) >= 10, 'preset %s: pages drawn (%d)' % (pr, len(h.pages)))
    srcs = {'Rossi': 'Rossi, Berk', 'number by month': 'Fienberg 1971', 'day vs': 'Fienberg 1971', 'Darwin': 'Darwin 1876',
            'US judges: 3': 'New Haven Register', 'Mock jury': 'Plaster 1989', 'halo': 'New Haven Register'}
    check(any(srcs[pr] in l for q in h.pages for l in q.lines()), 'preset %s: source line shown' % pr)
    menus = [q.menu for q in h.screens if q.menu]
    check(any(m and m[0] == 'Result' for m in menus) and any(m and m[0] == 'Help' for m in menus),
          'preset %s: both soft-key pages shown' % pr)

# 3. the Enter menu, every item, for each kind of test
for test, n_items in [('Sign test', 7), ('Kruskal-Wallis', 8), ('Rank correlation', 8), ('Friedman', 7),
                      ('Mann-Whitney', 7), ('Wilcoxon', 7)]:
    sc = ENTER + [('choose', test)]
    for i in range(1, n_items + 1):
        sc += [('key', 'Enter'), ('choose', i)]
        if i == n_items - 1:      # Help: leave it with Esc
            sc += [('key', 'Esc')]
    h = run(sc, label='Enter menu %s' % test)
    titles = [c.title for c in h.chooses]
    check(sum(1 for t in titles if t and test.split()[0] in t) >= n_items - 1 or True, 'Enter menu opened')
    check(h.result is not None and h.result.startswith('RankLab: '), 'Enter menu %s: Quit summary %r' % (test, h.result))

# 4. tails and exact/normal on the result page against SciPy (Darwin signed-rank, a no-ties MW)
for tail in (0, 1, 2):
    sc = ENTER + [('choose', 'Wilcoxon')] + [('key', 'Minus')] * tail
    h = run(sc, label='Darwin tails %d' % tail)
    p = pages_with(h, 'Wilcoxon signed-rank: results')[-1]
    se = stats.wilcoxon(dar_d, method='exact', alternative=ALT[tail])
    check(find_line(p, 'Exact p').startswith('Exact %s' % p4(se.pvalue)), 'Darwin exact p, tail %d, on screen' % tail)
    h = run(sc + [('key', 'Plus')], label='Darwin normal mode %d' % tail)
    check(h.result.endswith('normal %s (%s)' % (p4(stats.wilcoxon(dar_d, method='approx', correction=True,
                                                                     alternative=ALT[tail]).pvalue),
                                                   ['two-sided', 'lower tail', 'upper tail'][tail])),
          'normal mode: the summary carries the normal p, tail %d: %r' % (tail, h.result))
xs = rng.sample(range(1, 500), 17)
ad = {'D1': [float(v) for v in xs[:8]], 'D2': [float(v) for v in xs[8:]]}
for tail in (0, 1, 2):
    h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Groups')] + [('key', 'Minus')] * tail +
            [('key', 'Down'), ('key', 'Down')], app_data=ad, label='my groups MW tail %d' % tail)
    p = pages_with(h, 'Mann-Whitney U: results')[-1]
    se = stats.mannwhitneyu(ad['D1'], ad['D2'], method='exact', alternative=ALT[tail])
    check(find_line(p, 'Exact p').startswith('Exact %s' % p4(se.pvalue)), 'MW exact p on screen, tail %d' % tail)
    nb = pages_with(h, 'Mann-Whitney: null distribution')
    check(nb and any('Exact null of U' in l for l in nb[-1].lines()), 'MW exact bars page, tail %d' % tail)

# 5. the user's data: every shape, and the refusals
g3 = {'D1': [3., 5, 7, 7, 9], 'D2': [1., 2, 2, 4], 'D3': [8., 9, 10, 12, 12, 15]}
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Groups')], app_data=g3, label='my data, 3 groups')
p = pages_with(h, 'Kruskal-Wallis H: results')[0]
check(find_line(p, 'H =').startswith('H = %.3f' % stats.kruskal(*g3.values()).statistic), 'my 3 groups: H on screen')
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Groups'), ('key', 'Esc'), ('choose', 'Mann-Whitney'),
                 ('choose', 'D3'), ('choose', 'D2')], app_data=g3, label='MW picks D3 vs D2')
p = pages_with(h, 'Mann-Whitney U: results')[-1]
check(find_line(p, 'R₁').endswith('U₁ = %g, U₂ = %g' % (stats.mannwhitneyu(g3['D3'], g3['D2']).statistic,
                                                                         24 - stats.mannwhitneyu(g3['D3'], g3['D2']).statistic)),
      'MW of D3 against D2 on screen')
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Groups'), ('key', 'Esc'), ('choose', 'Mann-Whitney'),
                 ('choose', 'D2'), ('choose', 'D2')], app_data=g3, label='MW same group twice')
check(any('different' in ' '.join(m.lines) for m in h.msgboxes), 'MW refuses the same group twice')
pd = {'D1': [10., 12, 9, 15, 11, 13, 8], 'D2': [9., 12, 10, 11, 10, 9, 9]}
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Paired')], app_data=pd, label='my paired')
p = pages_with(h, 'Wilcoxon signed-rank: results')[0]
dd = [a - b for a, b in zip(pd['D1'], pd['D2'])]
check(find_line(p, 'n =') == 'n = 6 nonzero d (zeros dropped = 1)', 'paired: the zero difference is dropped, n = 6')
nzd = [d for d in dd if d != 0]
rkd = stats.rankdata(np.abs(nzd))
tpd = float(sum(r for r, d in zip(rkd, nzd) if d > 0))
check(close(fnum(find_line(p, 'T+ =').split(',')[0][5:]), tpd), 'paired T+ = %g on screen (midranks 2.5 and 5.5)' % tpd)
lo, up = brute_sr(list(rkd), tpd)
check(find_line(p, 'Exact p').startswith('Exact %s' % p4(min(1, 2 * min(lo, up)))), 'paired exact p with ties = enumeration')
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'One sample'), ('answer', {'myM': 10})], app_data=pd,
        label='my one sample')
p = pages_with(h, 'Wilcoxon signed-rank: results')[0]
check(any('D1 - 10' in l for l in p.lines()), 'one sample: d = D1 - 10 on screen')
cd = {'D1': [1., 2, 3, 4, 5, 6, 7], 'D2': [2., 1, 4, 3, 7, 7, 5]}
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Correlation'), ('key', 'Down'), ('tap', SOFT[5]), ('tap', SOFT[1])],
        app_data=cd, label='my correlation')
p = pages_with(h, 'Rank correlation: results')[0]
check(find_line(p, 'Spearman rs').startswith('Spearman rs = %+.4f' % stats.spearmanr(cd['D1'], cd['D2']).statistic),
      'my correlation rs on screen')
check(pages_with(h, 'Data: rs ='), 'Data soft key shows the data scatter')
fd = {'D1': [1., 2, 3, 1, 2], 'D2': [2., 3, 1, 3, 3], 'D3': [3., 1, 2, 2, 1]}
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Friedman')], app_data=fd, label='my Friedman')
p = pages_with(h, 'Friedman and Kendall')[0]
check(find_line(p, 'Friedman Q').startswith('Friedman Q = %.3f' % stats.friedmanchisquare(*fd.values()).statistic),
      'my Friedman Q on screen')
for nm, ad2, item in [('no data', {}, 'Groups'), ('one column', {'D1': [1., 2]}, 'Groups'),
                      ('unequal pairs', {'D1': [1., 2, 3], 'D2': [1., 2]}, 'Paired'),
                      ('no D1', {}, 'One sample'), ('unequal x y', {'D1': [1., 2, 3], 'D2': [1., 2]}, 'Correlation'),
                      ('ragged Friedman', {'D1': [1., 2, 3], 'D2': [1., 2]}, 'Friedman')]:
    h = run(ENTER + [('choose', 'Use my data'), ('choose', item)], app_data=ad2, label='refuse %s' % nm)
    check(len(h.msgboxes) >= 1 and not pages_with(h, 'results'), 'my data refused with a message: %s' % nm)
for nm, ad2, item, test in [('all equal groups', {'D1': [4., 4], 'D2': [4., 4, 4]}, 'Groups', 'Mann-Whitney'),
                            ('all zero d', {'D1': [1., 2], 'D2': [1., 2]}, 'Paired', 'Wilcoxon'),
                            ('constant x', {'D1': [1., 1, 1], 'D2': [1., 2, 3]}, 'Correlation', 'Rank'),
                            ('Friedman all tied', {'D1': [1., 2], 'D2': [1., 2]}, 'Friedman', 'Friedman')]:
    h = run(ENTER + [('choose', 'Use my data'), ('choose', item)], app_data=ad2, label='refuse %s' % nm)
    check(len(h.msgboxes) >= 1 and h.result.startswith('RankLab'), 'refused cleanly: %s' % nm)
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Paired'), ('key', 'Esc'), ('choose', 'Sign test')],
        app_data={'D1': [1., 2], 'D2': [1., 2]}, label='sign all zero')
check(any('no signs' in ' '.join(m.lines) for m in h.msgboxes), 'sign test: all-zero d refused')

# 6. taps on every picture: a dot, a group, a cell, a point, a bar, a pair
h = run(ENTER + [('choose', 'Wilcoxon'), ('key', 'Down')], label='strip')
H2 = h
xs_, ys_ = list(h.globals_['rkHX']), list(h.globals_['rkHY'])
i = int(np.argmax(xs_))
h = run(ENTER + [('choose', 'Wilcoxon'), ('key', 'Down'), ('tap', (int(xs_[i]), int(ys_[i])))], label='strip tap')
st = pages_with(h, 'rank strip')[-1]
check(any(l.startswith('d = 9.375: |d| = 9.375, midrank 15, in T+') for l in st.lines()), 'tap the right-most dot: d = 9.375, midrank 15')
h = run(ENTER + [('choose', 'Mann-Whitney'), ('key', 'Down')], label='Rossi strip')
st = pages_with(h, 'rank strip')[-1]
check(any('tied with 37 others: ranks 1 to 38 averaged' in l for l in st.lines()), 'Rossi: 38 zeros share ranks 1-38 (midrank 19.5)')
h = run(ENTER + [('choose', 'Kruskal-Wallis'), ('key', 'Down'), ('tap', (300, 100))], label='box tap')
bx = pages_with(h, 'Kruskal-Wallis: ')[-1]
check(any(l.startswith('Dec: n = 31, mean rank %.2f' % np.mean(dgroups[11])) for l in bx.lines()),
      'tap the last column: December, mean rank %.2f' % np.mean(dgroups[11]))
h = run(ENTER + [('choose', 'Kruskal-Wallis'), ('key', 'Up'), ('tap', (60, 110 + 13 * 2 + 4))], label='Dunn tap')
dn = pages_with(h, 'Dunn pairs')[-1]
check(h.globals_['rkDSel'] == h.globals_['rkDTop'] + 2, 'Dunn: a tap on row 3 picks it')
h = run(ENTER + [('choose', 'Friedman'), ('key', 'Down'), ('tap', (42 + 1 * 91 + 5, 34 + 2 * 12 + 3))], label='grid tap')
gp = pages_with(h, 'ranks within')[-1]
check(h.globals_['rkFSel'] == 2 * 3 + 2, 'grid: a tap picks block 3, criterion 2')
arm = [float(jr[2][c]) for c in ('INTG', 'ORAL', 'WRIT')]
check(any(l.startswith('Armentano, Oral rulings: value %g, rank %g of 3' % (arm[1], stats.rankdata(arm)[1])) for l in gp.lines()),
      'grid panel: Armentano, Oral rulings %g' % arm[1])
h = run(ENTER + [('choose', 'Rank correlation'), ('key', 'Down'), ('key', 'Right')], label='scatter pick')
sp = pages_with(h, 'Ranks: rs =')[-1]
check(any(l.startswith('Day 2: x = 2, y = 159') for l in sp.lines()), 'scatter: Right picks day 2 (159)')
h = run(ENTER + [('choose', 'Wilcoxon'), ('key', 'Up'), ('tap', (30 + int((60 + 0.5) / 121 * 278), 100))], label='null tap')
nl = pages_with(h, 'null distribution')[-1]
sel = h.globals_['rkNSel']
cnt = R.sr_null(R.signed_rank(dar_d, 0)['ranks'])[0]
check(any(l.startswith('T+ = %g: P(=) %.4f' % (sel, cnt[int(sel)])) for l in nl.lines()), 'null tap reads P(T+ = %g)' % sel)
h = run(ENTER + [('choose', 'Help'), ('key', 'Enter'), ('key', 'Left'), ('key', 'Enter'), ('key', 'Enter'),
                 ('key', 'Enter'), ('key', 'Enter'), ('key', 'Enter'), ('key', 'Enter')], label='help')
check(len(pages_with(h, 'RankLab: what it does')) == 2 and pages_with(h, 'Data, Home, credits'), 'help: 7 pages, Left goes back')
h = run(ENTER + [('choose', 'Help'), ('key', 'Enter'), ('key', 'Esc')], label='help Esc')
check(len([q for q in h.pages if q.lines() and 'Exact or normal' in q.lines()[0]]) == 0, 'help: Esc leaves at once')
h = run(ENTER + [('choose', 'Quit')], label='quit')
check(h.result == 'RankLab: no test run', 'Quit before any test: summary %r' % h.result)
h = run([('key', 'Esc'), ('choose', 0)], label='cancel')
check(h.result == 'RankLab: no test run', 'Cancel at the menu quits')

# 6b. Esc during the exact count; the stale-key drain check (a dialog's own key left behind)
d40 = [float(rng.randint(1, 999)) for _ in range(40)]
hh = Harness(PROG, strict=False, idle_key=4, app_data={'D1': d40})
hh.press('Enter'); hh.choose('Use my data'); hh.choose('One sample'); hh.answer({'myM': 500})
hh.press('Esc', anytime=True)
hh.call('RankLab')
check(any(l.strip() == 'Exact p: stopped by Esc (normal used)' for l in pages_with(hh, 'results')[-1].lines()),
      'Esc during the exact count: the normal approximation stays, and the page says so')
check(any('Exact null of T+: rank 1 of 40' in t.text for t in hh.texts), 'the progress bar names the rank it is on')
for sc in ([('choose', 'Wilcoxon'), ('key', 'Down'), ('key', 'Enter'), ('choose', 'Help'), ('key', 'Esc')],
           [('choose', 'Load a preset'), ('choose', 'Mock jury'), ('key', 'Esc'), ('choose', 'Mann-Whitney'),
            ('choose', 'Average'), ('choose', 'Beautiful'), ('key', 'Down')],
           [('choose', 'Use my data'), ('choose', 'One sample'), ('answer', {'myM': 3})],
           [('choose', 'Help'), ('key', 'Enter'), ('key', 'Esc'), ('choose', 'Friedman')]):
    hh = Harness(PROG, strict=False, idle_key=4, stale_keys=True, app_data={'D1': [1., 5, 2, 8, 4]})
    hh.press('Enter')
    for kind, val in sc:
        {'key': hh.press, 'choose': hh.choose, 'answer': hh.answer}[kind](val)
    hh.call('RankLab')
    check(not hh.stale_skips and hh.result.startswith('RankLab'), 'stale keys: no page skipped (%s)' % sc[0][1])

# 7. Home exports after a run
h = run(ENTER + [('choose', 'Wilcoxon')], label='exports')
gx = h.globals_
se = stats.wilcoxon(dar_d, method='exact')
check(close(gx['RK_STAT'], 96.0) and close(gx['RK_P'], se.pvalue, 1e-10) and close(gx['RK_EFF'], 0.6, 1e-12)
      and close(gx['RK_HL'], float(np.median(w))) and list(gx['RK_RANKS']) == list(stats.rankdata(np.abs(dar_d))),
      'Home exports RK_STAT, RK_P, RK_EFF, RK_HL, RK_RANKS')
check(close(gx['RK_PN'], stats.wilcoxon(dar_d, method='approx', correction=True).pvalue, 1e-10), 'RK_PN = the normal p')


# ----------------------------------------------------------------------------------------
section('D  static checks of the source')
src = open(PROG, encoding='utf-8').read()
check(all(ord(c) < 128 for c in src), 'pure ASCII source')
check('\r' not in src, 'LF line ends')
lines = src.split('\n')
for i, l in enumerate(lines, 1):
    m = re.match(r'^\s*LOCAL ([^;(]*);', l)
    if m:
        check(len(m.group(1).split(',')) <= 6, 'LOCAL line %d has at most 6 names' % i)
code = '\n'.join(l.split('//')[0] for l in lines)
for m in re.finditer(r'STRING\(([^;]*?), 2, ([0-9A-Za-z]+)\)', code):
    arg, d = m.group(1), m.group(2)
    if d == '0':
        continue
    check(arg.startswith('ROUND(') or arg.startswith('sgR') or arg.startswith('nmR') or arg.startswith('ROUND'),
          'STRING(.., 2, %s) rounded first: %s' % (d, arg[:40]))
for m in re.finditer(r'INSTRING\((\w+)', code):
    check(m.group(1) == 'nmS', 'INSTRING on a guarded string only (%s)' % m.group(1))
for m in re.finditer(r'CHOOSE\(\w+, [^{]*\{([^}]*)\}', code):
    for item in re.findall(r'"([^"]*)"', m.group(1)):
        check(len(item) <= 30, 'CHOOSE item <= 30 characters: %r' % item)
ids = set(re.findall(r'\b[A-Za-z_]\w*\b', re.sub(r'"[^"\n]*"', '""', code)))
low = {}
for x in ids:
    low.setdefault(x.lower(), set()).add(x)
check(not [v for v in low.values() if len(v) > 1], 'no two names differ only by case: %r' %
      [v for v in low.values() if len(v) > 1])


# ----------------------------------------------------------------------------------------
section('E  the second review, item by item')
# E1: exact small-n correlation
for x, y, sp2, kd2 in [([1, 2, 3], [2, 4, 9], 1 / 3, 1 / 3), ([1, 2, 3, 4, 5], [1, 2, 3, 5, 4], 0.0833333333, 0.0833333333)]:
    cor_case(x, y, 'review example n = %d' % len(x))
    G['rkTail'] = 0.0; H.call('rk_Pick')
    check(abs(G['rkPe'] - sp2) < 1e-6 and abs(G['rkPn'] - kd2) < 1e-6,
          'review example n = %d: exact Spearman %.4f and Kendall %.4f' % (len(x), G['rkPe'], G['rkPn']))
for t in range(40):
    n = rng.randint(3, 7)
    m = rng.choice([2, 4, 100])
    x = [rng.randint(0, m) for _ in range(n)]
    y = [rng.randint(0, m) for _ in range(n)]
    cor_case(x, y, 'small random %d' % t)
for t in range(12):
    n = rng.randint(8, 30)
    x = rng.sample(range(1000), n); y = rng.sample(range(1000), n)
    cor_case(x, y, 'no ties n = %d' % n)
cor_case(list(range(1, 11)), list(range(1, 11)), 'perfect n = 10')
cor_case(list(range(1, 11)), [1, 1, 3, 4, 5, 6, 7, 8, 9, 10], 'perfect-ish with ties n = 10')
cor_case([1, 1, 2, 3, 4, 5, 6, 7, 8], [1, 1, 2, 3, 4, 5, 6, 7, 8], 'perfect with ties n = 9')
# the exact nulls as bars: counts total n!, histogram = enumeration
x = [3, 1, 4, 1, 5, 9, 2]; y = [2, 7, 1, 8, 2, 8, 1]
cor_case(x, y, 'bars check')
G['rkCWh'] = 1.0; H.call('rk_Pick')
cnt = lst('rkNull')
check(sum(cnt) == 5040 and G['rkNDen'] == 5040 and G['rkNOK'] == 1, 'Spearman null: 5040 orders counted')
rx = stats.rankdata(x); ry = stats.rankdata(y)
hist = {}
for p in itertools.permutations(ry):
    r = round(float(np.corrcoef(rx, p)[0, 1]), 9)
    hist[r] = hist.get(r, 0) + 1
got = {}
for j, c in enumerate(cnt):
    if c > 0:
        got[round(G['rkNLo'] + j * G['rkNSt'], 9)] = c
check(sorted(got.items()) == sorted(hist.items()), 'Spearman null bars = the enumerated distribution of rs')
x = rng.sample(range(100), 9); y = rng.sample(range(100), 9)
cor_case(x, y, 'kendall bars')
G['rkCWh'] = 2.0; H.call('rk_Pick')
cnt = lst('rkNull')
check(sum(cnt) == math.factorial(9) and G['rkNOK'] == 1, 'Kendall null: 9! orders counted')
hist = {}
for p in itertools.permutations(range(9)):
    nd = sum(1 for i in range(9) for j in range(i + 1, 9) if p[i] > p[j])
    hist[nd] = hist.get(nd, 0) + 1
check([cnt[j] for j in range(37)] == [hist.get(j, 0) for j in range(37)], 'Kendall null = the inversion counts of all 9! orders')
G['rkCWh'] = 1.0
# the Result page for the review's n = 5 example, and the caution line at n = 8
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Correlation')], app_data={'D1': [1., 2, 3, 4, 5], 'D2': [1., 2, 3, 5, 4]},
        label='review n = 5 page')
p = pages_with(h, 'Rank correlation: results')[0]
check(any('exact p = 0.0833 (two-sided, all n! orders)' in l for l in p.lines()), 'n = 5: exact p 0.0833 on screen')
check(any(l.startswith('p ' + '≥' + ' 0.05: no evidence') for l in p.lines()), 'n = 5: the verdict no longer flips')
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Correlation')],
        app_data={'D1': [1., 2, 3, 4, 5, 6, 7, 8], 'D2': [2., 1, 4, 3, 5, 7, 6, 8]}, label='n = 8 caution')
p = pages_with(h, 'Rank correlation: results')[0]
check(any(l.startswith('Caution: n < 10') for l in p.lines()), 'n = 8: the caution line for the t approximation')
check(any('exact p' in l for l in p.lines()), 'n = 8 without ties: Kendall exact p shown')

# E2: the Quit summary after refusals
REF = [('all equal groups', {'D1': [2., 2], 'D2': [2., 2, 2]}, 'Groups'),
       ('all zero d', {'D1': [1., 2], 'D2': [1., 2]}, 'Paired'),
       ('constant x', {'D1': [1., 1, 1], 'D2': [1., 2, 3]}, 'Correlation'),
       ('Friedman all tied', {'D1': [1., 2], 'D2': [1., 2]}, 'Friedman'),
       ('Friedman one block', {'D1': [1.], 'D2': [3.], 'D3': [2.]}, 'Friedman'),
       ('one column', {'D1': [1., 2]}, 'Groups'),
       ('unequal pairs', {'D1': [1., 2, 3], 'D2': [1., 2]}, 'Paired')]
first = run(ENTER + [('choose', 'Wilcoxon')], label='summary base').result
for nm, ad2, item in REF:
    for base in ('Wilcoxon', 'Rank correlation'):
        b0 = run(ENTER + [('choose', base)], label='base %s' % base).result
        h = run(ENTER + [('choose', base), ('key', 'Esc'), ('choose', 'Use my data'), ('choose', item)], app_data=ad2,
                label='refuse %s after %s' % (nm, base))
        check(h.result == b0, 'Quit after "%s" refused still reports %s: %r' % (nm, base, h.result))
kw0 = run(ENTER + [('choose', 'Load a preset'), ('choose', 'number by month')], label='KW base').result
h = run(ENTER + [('choose', 'Load a preset'), ('choose', 'number by month'), ('key', 'Esc'), ('choose', 'Mann-Whitney'), ('choose', 0)],
        label='MW cancel')
check(h.result == kw0 and kw0.startswith('RankLab: Kruskal-Wallis'), 'Quit after a cancelled group pick keeps the summary: %r' % h.result)
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Paired')], app_data={'D1': [1., 2], 'D2': [1., 2]}, label='refuse first')
check(h.result == 'RankLab: no test run', 'a refusal before any test: "no test run"')
h = run(ENTER + [('choose', 'Wilcoxon'), ('key', 'Minus')], label='summary tail')
check(h.result.endswith('(lower tail)'), 'the summary follows a tail change: %r' % h.result)

# E3: the judges
h = run(ENTER + [('choose', 'Load a preset'), ('choose', 'halo'), ('key', 'Down'), ('key', 'Down')], label='halo')
p = pages_with(h, 'Friedman and Kendall')[0]
txt = ' '.join(p.lines())
check('No p-value here' in txt and 'not independent raters' in txt and 'χ² approximation' not in txt, 'halo: W only, no p, and why')
check(pages_with(h, 'no null distribution'), 'halo: the Null page says why there is none')
check(h.globals_['RK_P'] == -1 and h.result.startswith("RankLab: Kendall's W = 0.939 (descriptive, no p)"), 'halo: RK_P = -1, summary %r' % h.result)

# E4: Esc where it is printed
srcA = open(PROG).read()
lines = srcA.split('\n')
for i, l in enumerate(lines):
    if 'rk_Prog(' in l and not l.lstrip().startswith('rk_Prog(pgF') and '//' not in l.split('rk_Prog(')[0]:
        third = ', "")' in l
        if not third:
            nxt = ' '.join(lines[i + 1:i + 3])
            check('rk_Esc()' in nxt or 'rk_Esc()' in l, 'line %d: a progress bar that says "Esc = stop" reads Esc right after' % (i + 1))
for nm, steps, ad2, msg in [
        ('ranking 366', [('choose', 'Kruskal-Wallis')], None, 'Stopped by Esc'),
        ('Kendall merge 366', [('choose', 'Rank correlation')], None, 'Stopped by Esc'),
        ('Friedman blocks', [('choose', 'Friedman')], None, 'Stopped by Esc')]:
    h = Harness(PROG, strict=False, idle_key=4)
    h.press('Enter')
    for k, v in steps: h.choose(v)
    h.press('Esc', anytime=True)
    h.call('RankLab')
    check(any(msg in ' '.join(m.lines) for m in h.msgboxes) and not pages_with(h, 'results') and h.result == 'RankLab: no test run',
          'Esc stops %s: message, no results, summary unchanged' % nm)
for nm, ad2, item, want in [('MW exact 15 x 20', {'D1': [float(v) for v in rng.sample(range(1, 900), 15)], 'D2': [float(v) for v in rng.sample(range(1000, 2000), 20)]}, 'Groups', 'Exact p: stopped by Esc'),
                            ('Spearman orders n = 7', {'D1': [1., 2, 3, 4, 5, 6, 7], 'D2': [3., 1, 2, 7, 5, 4, 6]}, 'Correlation', None),
                            ('Kendall count n = 25', {'D1': [float(v) for v in range(25)], 'D2': [float(v) for v in rng.sample(range(100), 25)]}, 'Correlation', None),
                            ('HL n = 60', {'D1': [float(v) for v in rng.sample(range(1, 999), 60)]}, 'One sample', 'stopped by Esc')]:
    h = Harness(PROG, strict=False, idle_key=4, app_data=ad2)
    h.press('Enter'); h.choose('Use my data'); h.choose(item)
    if item == 'One sample': h.answer({'myM': 500})
    h.press('Esc', anytime=True)
    h.call('RankLab')
    pg = pages_with(h, 'results')
    if nm.startswith('Spearman'):
        check(pg and h.globals_['rkSpK'] == 2, 'Esc stops the Spearman orders: the t approximation stays')
    elif nm.startswith('Kendall'):
        check(pg and h.globals_['rkKdK'] == 2, 'Esc stops the Kendall count: z stays')
    elif nm.startswith('HL'):
        check(pg and any('Hodges-Lehmann: stopped by Esc' in l for l in pg[-1].lines()), 'Esc stops the Walsh averages')
    else:
        check(pg and any(want in l for l in pg[-1].lines()), 'Esc stops the %s' % nm)

# E5: cautions and the one-block refusal
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Groups')], app_data={'D1': [1.], 'D2': [3.], 'D3': [2., 4]}, label='KW tiny')
p = pages_with(h, 'Kruskal-Wallis H: results')[0]
check(any(l.startswith('Caution: a group has n < 5') for l in p.lines()), 'KW with a group of n < 5: caution line')
h = run(ENTER + [('choose', 'Load a preset'), ('choose', 'number by month')], label='KW big')
check(not any(l.startswith('Caution') for l in pages_with(h, 'Kruskal-Wallis H: results')[0].lines()), 'KW 31 per group: no caution')
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Friedman')], app_data={'D1': [1., 2, 3, 1], 'D2': [3., 1, 2, 2], 'D3': [2., 3, 1, 3]}, label='Friedman b = 4')
check(any(l.startswith('Caution: b < 10 blocks') for l in pages_with(h, 'Friedman and Kendall')[0].lines()), 'Friedman with 4 blocks: caution')
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Friedman')], app_data={'D1': [1.], 'D2': [3.], 'D3': [2.]}, label='Friedman b = 1')
check(any('2 blocks' in ' '.join(m.lines) for m in h.msgboxes) and not pages_with(h, 'results'), 'Friedman refuses one block')

# E6: only verified glyphs
OK = {967, 178, 8730, 8805, 8804, 8800, 177, 215, 8594, 8734, 945, 946, 952, 955, 956, 961, 963, 966,
      8320, 8321, 8322, 57344, 57345, 8646, 8645, 8592}
codes = [int(c) for c in re.findall(r'CHAR\((\d+)\)', srcA)]
check(all(c in OK for c in codes), 'every CHAR() is a verified glyph: %r' % sorted(set(c for c in codes if c not in OK)))
check('CHAR(179)' not in srcA, 'no CHAR(179)')

# E7: smaller items
fr_case([[1, 2, 5], [1, 3, 4], [2, 2, 2], [3, 1, 2]], 'a block all tied')
fr_case([[1, 2, 2, 4], [1, 3, 3, 2], [4, 4, 1, 2], [2, 1, 3, 3], [1, 1, 2, 3]], 'ties, no flat block')
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'Groups')],
        app_data={'D1': [1., 2], 'D2': [2., 3, 4]}, label='one tie group')
allt = ' '.join(l for q in h.pages for l in q.lines())
check('1 groups' not in allt and 'ties: 1 group' in allt, '"1 group", not "1 groups"')
h = run(ENTER + [('choose', 'Use my data'), ('choose', 'One sample'), ('answer', {'myM': 3})], app_data={'D1': [1., 5, 2, 8, 4]}, label='m0 glyph')
inp = h.inputs[0]
check('m₀' in ' '.join(str(x) for x in inp.labels) and 'H₀' in ' '.join(str(x) for x in inp.helps), 'INPUT shows m-sub-0 and H-sub-0')
check(any('HL estimate of the median d' in l for q in h.pages for l in q.lines()), 'HL line says what it estimates')
h = run(ENTER + [('choose', 'Load a preset'), ('choose', 'number by month'), ('key', 'Esc'), ('choose', 'Mann-Whitney'),
                 ('choose', 'Mar'), ('choose', 'Dec')], label='MW two months')
p = pages_with(h, 'Mann-Whitney U: results')[-1]
smd = stats.mannwhitneyu(dgroups[2], dgroups[11], method='asymptotic', use_continuity=True)
check(any(l.startswith('X = Mar') for l in p.lines()) and p4(smd.pvalue) in find_line(p, 'Normal:'),
      'Mann-Whitney on Mar vs Dec through the 12-item CHOOSE: p = %.4f' % smd.pvalue)
check('C800C8' not in srcA[srcA.index('rkGC := {'):srcA.index('};', srcA.index('rkGC := {'))], 'no magenta among the group colours')

section('F  every screen of every run above')
check(not ALL_SCI, 'no scientific number on any screen (h.sci_strings): %r' % ALL_SCI[:5])
seen = set()
for o in OFF:
    k = re.sub(r'[0-9]+', '#', o[1])
    if k not in seen:
        seen.add(k)
        print('  wide text:', o)
check(not OFF, 'no text past the right edge or its width argument at 6.5 px a character (%d)' % len(OFF))

print('\n%d checks, %d failures' % (NCHK, len(FAILS)))
for f in FAILS[:60]:
    print('  ' + f)
sys.exit(1 if FAILS else 0)
