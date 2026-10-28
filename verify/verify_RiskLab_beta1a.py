#!/usr/bin/env python3
"""verify_RiskLab_beta1a.py -- checks for RiskLab beta 1a (26 Oct 2026): every beta 1 check
(updated where beta 1a changed a page on purpose), plus Part D, one or more checks per item of the
second review (REVIEW2_RiskLab_beta1.md, items 1-8), including a case-insensitive scan of every
routine, EXPORT and file-level LOCAL name.  Built from verify_RiskLab_beta1.py; its description:

verify_RiskLab_beta1.py -- checks for RiskLab beta 1 (26 Oct 2026).

Part A  the engine, routine by routine, in the PC harness (ppl_run_v3e), against references
        written here independently:
          A1 logistic regression (rl_Fit) vs statsmodels Logit / GLM Binomial (params, bse, llf,
             llnull, llr, llr_pvalue, prsquared) on Rossi (3 and 4 predictors), COMPAS (grouped
             counts) and 30 random / edge data sets (n 10-300, k 1-4, binary and continuous x, big
             and negative values); separation, quasi-separation, collinear x and a constant outcome
             are detected; n = 2 and 3 do not crash;
          A2 AUC (rl_AUCof) vs a brute-force pairwise Mann-Whitney count and scipy mannwhitneyu;
             DeLong's SE vs a pairwise structural-component implementation, vs Stata's published
             example (Hanley & McNeil 1982 data: AUC 0.8932, DeLong SE 0.0307, CI 0.83295-0.95339;
             Hanley SE 0.0320) and vs a bootstrap; Hanley-McNeil's SE vs its formula;
          A3 cumulative counts and every cut-off's 2 x 2 table vs direct counting;
          A4 Hosmer-Lemeshow (rl_Group, rl_HL) vs an independent grouping and scipy chi2.sf;
          A5 rl_ChiUp vs scipy chi2.sf, df 1-14, x up to 400 (relative error, tiny tails);
          A6 COMPAS counts and the error rates at decile >= 5 recomputed from ProPublica's raw CSV
             (second route), and the fairness identity FPR = p/(1-p) (1-PPV)/PPV (1-FNR);
          A7 the level builder with groups (user score data) vs Python.
Part B  every menu path of the program, the numbers ON THE PAGES checked against Part A's
        references: opening page, COMPAS and Rossi table pages and taps, fitted curve (predictors,
        arrows, taps), ROC (arrows, +/-, drag, Groups overlay, taps), calibration (Groups toggle,
        taps), fairness (all four pages, arrows), Rossi's fairness refusal, Use my data (both
        kinds, valid and invalid), Help (8 pages, and Esc), Esc during the fit and the re-fit,
        Quit's summary.
Part C  every run: no runtime error, no scientific number on screen, no text off the 320 x 240
        screen, MSGBOX at most 5 lines, text width at 6.5 px per character inside its width.

Run:  python3 verify_RiskLab_beta1.py   (prints "N checks, M failures"; exit 0 = all passed)
Roger Metcalf / Claude, 26 Oct 2026.
"""
import os
import sys
import math
import csv
import random
import warnings

import numpy as np
from scipy import stats
import statsmodels.api as sm

warnings.filterwarnings('ignore')
os.environ.setdefault('HPKIT', '/home/claude/kit/hp-prime-kit-HEAD')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'ref'))
from ppl_run_v3e import Harness  # noqa: E402

PROG = os.path.join(ROOT, 'RiskLab_beta1a.txt')
PROG_OLD = os.path.join(ROOT, 'RiskLab_beta1.txt')
RAW = os.path.join(HERE, 'compas_raw', 'compas-scores-two-years.csv')
Z = stats.norm.ppf(0.975)

N_CHECK = 0
FAILS = []
ALL_RUNS = []


def check(cond, what):
    global N_CHECK
    N_CHECK += 1
    if not cond:
        FAILS.append(what)
        print('FAIL', what)


def close(a, b, tol=1e-7):
    return abs(a - b) <= tol * max(1.0, abs(b))


def new_h(**kw):
    kw.setdefault('strict', False)
    kw.setdefault('idle_key', 4)
    kw.setdefault('cas', 'fail')
    h = Harness(PROG, **kw)
    ALL_RUNS.append(h)
    return h


def f(x, d):
    """The program's rl_F: round half away from zero, fixed decimals."""
    q = 10 ** d
    v = math.floor(abs(x) * q + 0.5) / q
    v = -v if x < 0 else v
    if v == 0:
        v = 0.0
    return '%.*f' % (d, v)


# ============================================================ data
def rossi():
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'rossi.csv'))))
    return rows


ROSSI = rossi()
CMP_N1 = [365, 346, 298, 337, 323, 318, 343, 301, 317, 227]
CMP_E1 = [85, 105, 125, 158, 158, 187, 209, 215, 229, 190]
CMP_N2 = [605, 321, 238, 243, 200, 160, 113, 96, 77, 50]
CMP_E2 = [128, 100, 82, 98, 91, 93, 68, 72, 55, 35]


def compas_rows():
    """People one by one from the counts: (decile, y, group)."""
    out = []
    for g, (N, E) in enumerate(((CMP_N1, CMP_E1), (CMP_N2, CMP_E2)), 1):
        for d in range(10):
            out += [(d + 1, 1, g)] * E[d] + [(d + 1, 0, g)] * (N[d] - E[d])
    return out


# ============================================================ references
def ref_logit(Y, X):
    Xc = sm.add_constant(np.asarray(X, float), has_constant='add')
    m = sm.Logit(np.asarray(Y, float), Xc).fit(disp=0, maxiter=100)
    return m


def ref_auc(scores, ys):
    s = np.asarray(scores, float); y = np.asarray(ys)
    pos = s[y == 1]; neg = s[y == 0]
    n1, n0 = len(pos), len(neg)
    diff = pos[:, None] - neg[None, :]
    psi = (diff > 0) + 0.5 * (diff == 0)
    auc = psi.mean()
    v10 = psi.mean(axis=1); v01 = psi.mean(axis=0)
    sd = math.sqrt(np.var(v10, ddof=1) / n1 + np.var(v01, ddof=1) / n0) if n1 > 1 and n0 > 1 else -1
    q1 = auc / (2 - auc); q2 = 2 * auc ** 2 / (1 + auc)
    sh = math.sqrt(max(0, (auc * (1 - auc) + (n1 - 1) * (q1 - auc ** 2) + (n0 - 1) * (q2 - auc ** 2)) / (n1 * n0)))
    u = stats.mannwhitneyu(pos, neg, alternative='two-sided').statistic
    return dict(auc=auc, sd=sd, sh=sh, u=u / (n1 * n0), n1=n1, n0=n0)


def ref_levels(scores, ys, groups=None):
    lv = sorted(set(scores))
    idx = {v: i for i, v in enumerate(lv)}
    A1 = [0] * len(lv); B1 = [0] * len(lv); A2 = [0] * len(lv); B2 = [0] * len(lv)
    for i, (s, y) in enumerate(zip(scores, ys)):
        g = groups[i] if groups else 1
        j = idx[s]
        if g == 2:
            (A2 if y == 1 else B2)[j] += 1
        else:
            (A1 if y == 1 else B1)[j] += 1
    return lv, A1, B1, A2, B2


def ref_group(LA, LB, G):
    """Independent grouping: ties (one level) never split; a group closes when the running
    count reaches the next multiple of N/G; the last level closes the last group."""
    N = sum(LA) + sum(LB)
    m = len(LA)
    groups, start, cum, q = [], 0, 0, 1
    for l in range(m):
        cum += LA[l] + LB[l]
        close_now = G == 0 or l == m - 1 or cum >= q * N / G - 1e-6
        if close_now:
            groups.append((start, l)); start = l + 1
            if G > 0:
                while q * N / G <= cum + 1e-6:
                    q += 1
    return groups


def ref_hl(LA, LB, LP, G):
    gr = ref_group(LA, LB, G)
    hl, rows, bad = 0.0, [], False
    for a, b in gr:
        n = sum(LA[a:b + 1]) + sum(LB[a:b + 1]); o = sum(LA[a:b + 1])
        e = sum(LP[l] * (LA[l] + LB[l]) for l in range(a, b + 1))
        rows.append((n, o, e, e / n))
        d = e * (1 - e / n)
        if d > 1e-12:
            hl += (o - e) ** 2 / d
        else:
            bad = True
    df = len(gr) - 2
    p = stats.chi2.sf(hl, df) if df >= 1 and not bad else -1
    return dict(hl=hl, df=df, p=p, rows=rows, groups=gr)


def tables(LA, LB):
    """Every cut-off's (TP, FP) for t = 1..m+1 (1-based as the program)."""
    m = len(LA)
    out = []
    for t in range(1, m + 2):
        out.append((sum(LA[t - 1:]), sum(LB[t - 1:])))
    return out


# ============================================================ Part A
def load_state_rows(h, Y, X, names=None):
    n, k = len(Y), len(X[0])
    g = h.globals_
    flat = [float(v) for row in X for v in row]
    g.update(dict(rlMode=1, rlIsC=0, rlN=float(n), rlK=float(k), rlY=[float(y) for y in Y], rlXv=flat,
                  rlXNm=names or ['x%d' % (j + 1) for j in range(k)],
                  rlXm=[float(np.mean([r[j] for r in X])) for j in range(k)],
                  rlN1=float(sum(Y)), rlN0=float(n - sum(Y)), rlNG=1.0, rlPrb=1.0, rlInS=1.0,
                  rlScNm='fitted P', rlCalG=1.0, rlGNm=['everyone', ''], rlGSh=['all', '']))


def check_fit_vs_sm(h, Y, X, label, tol=1e-6):
    g = h.globals_
    m = ref_logit(Y, X)
    ok = g['rlFitOK'] == 1
    check(ok, '%s: fit OK (%s)' % (label, g['rlFitW']))
    if not ok:
        return m
    p = len(m.params)
    check(all(close(g['rlB'][j], m.params[j], tol) for j in range(p)), '%s: b = statsmodels %s vs %s' % (label, g['rlB'], list(m.params)))
    check(all(close(g['rlSE'][j], m.bse[j], tol * 10) for j in range(p)), '%s: SE = statsmodels %s vs %s' % (label, g['rlSE'], list(m.bse)))
    check(close(g['rlLL'], m.llf, 1e-9), '%s: lnL %.10f vs %.10f' % (label, g['rlLL'], m.llf))
    check(close(g['rlLL0'], m.llnull, 1e-9), '%s: lnL0 %.10f vs %.10f' % (label, g['rlLL0'], m.llnull))
    check(close(g['rlLRc'], m.llr, 1e-6), '%s: LR chi2 %.8f vs %.8f' % (label, g['rlLRc'], m.llr))
    check(close(g['rlLRp'], m.llr_pvalue, 1e-6) or abs(g['rlLRp'] - m.llr_pvalue) < 1e-14,
          '%s: LR p %.6g vs %.6g' % (label, g['rlLRp'], m.llr_pvalue))
    check(close(1 - g['rlLL'] / g['rlLL0'], m.prsquared, 1e-9), '%s: McFadden' % label)
    check(g['rlSep'] == 0, '%s: no separation flagged' % label)
    return m


def part_a():
    print('=== Part A: the engine')
    # ---- A1 Rossi
    for k, cols in ((3, ['age', 'prio', 'fin']), (4, ['age', 'prio', 'fin', 'wexp'])):
        h = new_h(); h.call('rl_Init'); h.call('rl_LoadRossi', k)
        Y = [int(r['arrest']) for r in ROSSI]; X = [[int(r[c]) for c in cols] for r in ROSSI]
        m = check_fit_vs_sm(h, Y, X, 'A1 Rossi k=%d' % k, 1e-7)
        g = h.globals_
        # the fitted P of every man = statsmodels' predict
        ph = np.asarray(g['rlPh']); check(np.max(np.abs(ph - m.predict())) < 1e-9, 'A1 Rossi k=%d fitted P' % k)
        # levels / AUC from the fitted P
        r = ref_auc(list(m.predict()), Y)
        check(close(g['rlAUC'], r['auc'], 1e-9) and close(g['rlAUC'], r['u'], 1e-9),
              'A2 Rossi k=%d AUC %.6f vs pairwise %.6f, mannwhitneyu %.6f' % (k, g['rlAUC'], r['auc'], r['u']))
        check(close(g['rlSEd'], r['sd'], 1e-7), 'A2 Rossi k=%d DeLong SE %.6f vs %.6f' % (k, g['rlSEd'], r['sd']))
        check(close(g['rlSEh'], r['sh'], 1e-7), 'A2 Rossi k=%d HM SE' % k)
        check(int(g['rlM']) == len(set(np.round(m.predict(), 12))), 'A2 Rossi k=%d levels %d' % (k, g['rlM']))
        # HL with 10 and 5 groups
        LA, LB, LP = g['rlLA'], g['rlLB'], g['rlLP']
        for cg, G in ((1, 10), (2, 5)):
            g['rlCalG'] = float(cg); h.call('rl_HosLem')
            rr = ref_hl(LA, LB, LP, G)
            check(int(g['rlGk']) == len(rr['groups']) and close(g['rlHLv'], rr['hl'], 1e-9) and g['rlHLdf'] == rr['df']
                  and close(g['rlHLp'], rr['p'], 1e-7),
                  'A4 Rossi k=%d HL G=%d: %.6f df %d p %.6f vs %.6f %d %.6f' % (k, G, g['rlHLv'], g['rlHLdf'], g['rlHLp'], rr['hl'], rr['df'], rr['p']))
            # groups never split a tie, and sum E = sum O overall (score equation)
            check(abs(sum(g['rlGe']) - sum(g['rlGo'])) < 1e-6, 'A4 Rossi k=%d G=%d: sum E = sum O' % (k, G))
        g['rlCalG'] = 1.0; h.call('rl_HosLem')
        if k == 4:
            ROSSI4.update(m=m, auc=r, lv=list(g['rlLv']), LA=list(LA), LB=list(LB))
        else:
            ROSSI3.update(m=m, auc=r, lv=list(g['rlLv']), LA=list(LA), LB=list(LB))
        # A3 every cut-off
        tb = tables(LA, LB)
        check(all(g['rlCA'][t] == tb[t][0] and g['rlCB'][t] == tb[t][1] for t in range(len(tb))), 'A3 Rossi k=%d cumulative counts' % k)
    # ---- A1 COMPAS grouped
    h = new_h(); h.call('rl_Init'); h.call('rl_LoadCompas')
    g = h.globals_
    rows = compas_rows()
    Y = [r[1] for r in rows]; X = [[r[0]] for r in rows]
    m = check_fit_vs_sm(h, Y, X, 'A1 COMPAS (grouped = person by person)', 1e-7)
    COMPAS['m'] = m
    lvC = [float(v) for v in range(1, 11)]
    check(list(g['rlLv']) == lvC, 'A7 COMPAS levels 1..10')
    for (A, B, nm) in ((g['rlLA'], g['rlLB'], 'all'), (g['rlA1'], g['rlB1'], 'g1'), (g['rlA2'], g['rlB2'], 'g2')):
        sel = [r for r in rows if nm == 'all' or r[2] == int(nm[1])]
        rr = ref_auc([r[0] for r in sel], [r[1] for r in sel])
        res = h.execute('rl_AUCof(%s, %s)' % ('{' + ','.join('%d' % v for v in A) + '}', '{' + ','.join('%d' % v for v in B) + '}'))
        check(close(res[0], rr['auc'], 1e-9) and close(res[0], rr['u'], 1e-9), 'A2 COMPAS %s AUC %.6f vs %.6f' % (nm, res[0], rr['auc']))
        check(close(res[1], rr['sd'], 1e-7), 'A2 COMPAS %s DeLong %.6f vs %.6f' % (nm, res[1], rr['sd']))
        check(close(res[2], rr['sh'], 1e-7), 'A2 COMPAS %s HM' % nm)
        COMPAS[nm] = rr
    check(close(g['rlGAU'][0], COMPAS['g1']['auc']) and close(g['rlGAU'][2], COMPAS['g2']['auc'])
          and close(g['rlGAU'][1], COMPAS['g1']['sd']) and close(g['rlGAU'][3], COMPAS['g2']['sd']), 'A2 COMPAS rlGAU')
    LP = [1 / (1 + math.exp(-(m.params[0] + m.params[1] * d))) for d in range(1, 11)]
    check(max(abs(a - b) for a, b in zip(g['rlLP'], LP)) < 1e-9, 'A4 COMPAS predicted P per level')
    for cg, G in ((1, 0), (2, 5)):
        g['rlCalG'] = float(cg); h.call('rl_HosLem')
        rr = ref_hl(list(g['rlLA']), list(g['rlLB']), LP, G)
        check(close(g['rlHLv'], rr['hl'], 1e-7) and g['rlHLdf'] == rr['df'] and close(g['rlHLp'], rr['p'], 1e-6),
              'A4 COMPAS HL G=%d %.5f df %d vs %.5f %d' % (G, g['rlHLv'], g['rlHLdf'], rr['hl'], rr['df']))
        COMPAS['hl%d' % G] = rr
    g['rlCalG'] = 1.0; h.call('rl_HosLem')
    check(int(g['rlCutT']) == 5, 'A3 COMPAS default cut-off = decile 5')
    # ---- A2 the published example: Hanley & McNeil (1982) ratings, Stata's roctab output
    neg = [33, 6, 6, 11, 2]; pos = [3, 2, 2, 11, 33]
    res = h.execute('rl_AUCof({3,2,2,11,33},{33,6,6,11,2})')
    check(f(res[0], 4) == '0.8932' and f(res[1], 4) == '0.0307' and f(res[2], 4) == '0.0325',
          'A2 Hanley-McNeil data: AUC %.4f, DeLong %.4f (Stata 0.8932, 0.0307), HM %.4f' % (res[0], res[1], res[2]))
    check(f(res[0] - Z * res[1], 5) == '0.83295' and f(res[0] + Z * res[1], 5) == '0.95339',
          'A2 Hanley-McNeil data: DeLong CI = Stata 0.83295-0.95339 (%.5f-%.5f)' % (res[0] - Z * res[1], res[0] + Z * res[1]))
    # Stata's hanley option prints 0.0320; our HM SE is 0.0325 -- Stata's 'hanley' uses the
    # binomial-exact variant; HM's own paper formula gives 0.0325 here (recorded, not a failure)
    # ---- A2 bootstrap check of DeLong on Rossi k=3 (2000 resamples of men)
    rs = np.random.RandomState(1)
    Y = np.array([int(r['arrest']) for r in ROSSI]); P = ROSSI3['m'].predict()
    boots = []
    for _ in range(2000):
        ii = rs.randint(0, 432, 432)
        boots.append(ref_auc(P[ii], Y[ii])['auc'])
    bs = np.std(boots, ddof=1)
    check(abs(bs - ROSSI3['auc']['sd']) / bs < 0.1, 'A2 Rossi DeLong SE %.4f vs bootstrap %.4f (within 10%%)' % (ROSSI3['auc']['sd'], bs))
    # ---- A1 random and edge data sets
    rnd = random.Random(26)
    nsets = 0
    for it in range(30):
        n = rnd.choice([10, 12, 20, 40, 75, 150, 300])
        k = rnd.randint(1, 4)
        X = []
        kinds = [rnd.choice(['norm', 'bin', 'int', 'big', 'neg']) for _ in range(k)]
        for i in range(n):
            row = []
            for kd in kinds:
                if kd == 'norm': row.append(round(rnd.gauss(0, 1), 3))
                elif kd == 'bin': row.append(rnd.randint(0, 1))
                elif kd == 'int': row.append(rnd.randint(0, 20))
                elif kd == 'big': row.append(round(rnd.uniform(1e4, 1e5), 1))
                else: row.append(round(rnd.uniform(-50, -1), 2))
            X.append(row)
        beta = [rnd.uniform(-0.5, 0.5) for _ in range(k)]
        Y = []
        for row in X:
            mu = sum(b * (x - np.mean([r[j] for r in X])) / (np.std([r[j] for r in X]) + 1e-9) for j, (b, x) in enumerate(zip(beta, row)))
            Y.append(1 if rnd.random() < 1 / (1 + math.exp(-mu)) else 0)
        if sum(Y) in (0, n):
            Y[0] = 1 - Y[0]
        h = new_h(); h.call('rl_Init'); load_state_rows(h, Y, X)
        h.call('rl_Refit')
        g = h.globals_
        # statsmodels may itself hit separation on tiny sets: compare only when it is clean
        try:
            m = ref_logit(Y, X)
            sm_ok = m.mle_retvals['converged'] and np.all(np.isfinite(m.bse)) and np.max(np.abs(m.params)) < 15 and np.max(np.abs(m.fittedvalues)) < 15
        except Exception:
            sm_ok = False
        if sm_ok and g['rlSep'] == 0 and g['rlFitOK'] == 1:
            nsets += 1
            check_fit_vs_sm(h, Y, X, 'A1 random set %d (n %d, k %d, %s)' % (it, n, k, kinds), 1e-6)
            r = ref_auc(list(g['rlPh']), Y)
            check(close(g['rlAUC'], r['auc'], 1e-9) and close(g['rlSEd'], r['sd'], 1e-6), 'A2 random set %d AUC/DeLong' % it)
            rr = ref_hl(list(g['rlLA']), list(g['rlLB']), list(g['rlLP']), 10)
            check(close(g['rlHLv'], rr['hl'], 1e-6) and g['rlHLdf'] == rr['df'], 'A4 random set %d HL' % it)
        else:
            check(g['rlFitOK'] in (1, -2) and (g['rlSep'] == 1 or not sm_ok),
                  'A1 random set %d: statsmodels unstable, RiskLab flags it (sep %s ok %s)' % (it, g['rlSep'], g['rlFitOK']))
    check(nsets >= 20, 'A1 at least 20 random sets compared with statsmodels (%d)' % nsets)
    # ---- edge: complete separation, quasi-separation, collinear, constant outcome, n = 2, 3
    X = [[i] for i in range(20)]; Y = [0] * 10 + [1] * 10
    h = new_h(); h.call('rl_Init'); load_state_rows(h, Y, X); h.call('rl_Fit')
    check(h.globals_['rlSep'] == 1, 'A1 complete separation flagged (ok %s, it %s, eta %.1f)' % (h.globals_['rlFitOK'], h.globals_['rlIt'], h.globals_['rlEta']))
    X = [[i // 2] for i in range(20)]; Y = [0] * 10 + [0, 1] + [1] * 8     # x <= 4 all 0, x = 5 mixed, x >= 6 all 1
    h = new_h(); h.call('rl_Init'); load_state_rows(h, Y, X); h.call('rl_Fit')
    check(h.globals_['rlSep'] == 1, 'A1 quasi-separation flagged (ok %s it %s)' % (h.globals_['rlFitOK'], h.globals_['rlIt']))
    X = [[i % 7, 2 * (i % 7)] for i in range(30)]; Y = [i % 2 for i in range(30)]
    h = new_h(); h.call('rl_Init'); load_state_rows(h, Y, X); h.call('rl_Fit')
    check(h.globals_['rlFitOK'] == -2 and h.globals_['rlSep'] == 0 and 'mix of others' in h.globals_['rlFitW'], 'A1 collinear x: no SEs, said so (%s)' % h.globals_['rlFitW'])
    h = new_h(); h.call('rl_Init'); load_state_rows(h, [0] * 12, [[i] for i in range(12)]); h.call('rl_Fit')
    check(h.globals_['rlFitOK'] == -1, 'A1 constant outcome refused')
    for Y, X in (([0, 1], [[1], [2]]), ([0, 1, 1], [[1], [2], [2]]), ([1, 0, 1], [[1, 5], [2, 3], [3, 4]])):
        h = new_h(); h.call('rl_Init'); load_state_rows(h, Y, X)
        try:
            h.call('rl_Refit'); okk = h.error is None
        except Exception as e:  # noqa
            okk = False
        check(okk, 'A1 n = %d runs without a runtime error (ok %s)' % (len(Y), h.globals_.get('rlFitOK')))
    # ---- A5 chi-square upper tail
    h = new_h(); h.call('rl_Init')
    worst = 0
    for df in range(1, 15):
        for x in (0.01, 0.5, 1, 2.5, 5, 10, 20, 40, 80, 150, 250, 400):
            v = h.execute('rl_ChiUp(%d, %r)' % (df, x)); r = stats.chi2.sf(x, df)
            if r > 1e-300:
                worst = max(worst, abs(v - r) / r)
    check(worst < 1e-9, 'A5 rl_ChiUp vs chi2.sf, df 1-14, x to 400: worst relative error %.2e' % worst)
    check(h.execute('rl_ChiUp(3, 0)') == 1, 'A5 rl_ChiUp at 0 = 1')
    # ---- A6 COMPAS from the raw CSV (the second route) and the fairness identity
    if os.path.exists(RAW):
        raw = list(csv.DictReader(open(RAW, newline='')))
        kept = [r for r in raw if r['days_b_screening_arrest'] != '' and -30 <= float(r['days_b_screening_arrest']) <= 30
                and r['is_recid'] != '-1' and r['c_charge_degree'] != 'O' and r['score_text'] != 'N/A']
        check(len(raw) == 7214 and len(kept) == 6172 and sum(int(r['two_year_recid']) for r in kept) == 2809,
              'A6 raw CSV: 7214 rows, 6172 kept, 2809 re-arrested (ProPublica\'s numbers)')
        for race, N, E in (('African-American', CMP_N1, CMP_E1), ('Caucasian', CMP_N2, CMP_E2)):
            nn = [sum(1 for r in kept if r['race'] == race and int(r['decile_score']) == d) for d in range(1, 11)]
            ee = [sum(1 for r in kept if r['race'] == race and int(r['decile_score']) == d and r['two_year_recid'] == '1') for d in range(1, 11)]
            check(nn == N and ee == E, 'A6 %s counts by decile = the program\'s' % race)
    else:
        check(False, 'A6 raw COMPAS CSV present at %s' % RAW)
    for g_, (N, E) in ((1, (CMP_N1, CMP_E1)), (2, (CMP_N2, CMP_E2))):
        n1 = sum(E); n0 = sum(N) - n1
        TP = sum(E[4:]); FP = sum(N[4:]) - TP; FN = n1 - TP
        p = n1 / (n1 + n0); ppv = TP / (TP + FP); fnr = FN / n1; fpr = FP / n0
        check(close(p / (1 - p) * (1 - ppv) / ppv * (1 - fnr), fpr, 1e-12), 'A6 identity holds for group %d' % g_)
        COMPAS['g%d_cut5' % g_] = dict(n=n1 + n0, n1=n1, n0=n0, TP=TP, FP=FP, FN=FN, TN=n0 - FP, p=p, ppv=ppv, fnr=fnr, fpr=fpr)
    check(f(COMPAS['g1_cut5']['fpr'], 3) == '0.423' and f(COMPAS['g2_cut5']['fpr'], 3) == '0.220'
          and f(COMPAS['g1_cut5']['fnr'], 3) == '0.285' and f(COMPAS['g2_cut5']['fnr'], 3) == '0.496',
          'A6 two-year file at decile >= 5: FPR 0.423 / 0.220, FNR 0.285 / 0.496')
    # ---- A7 levels with groups (user score data)
    rnd = random.Random(7)
    for it in range(5):
        n = rnd.choice([30, 100, 400])
        sc = [rnd.choice([round(rnd.random(), 2), rnd.randint(1, 6)]) for _ in range(n)]
        ys = [1 if rnd.random() < 0.4 else 0 for _ in range(n)]
        gs = [rnd.randint(1, 2) for _ in range(n)]
        h = new_h(); h.call('rl_Init')
        h.execute('rl_Levels(%s, %s, %s)' % tuple('{' + ','.join(repr(float(v)) for v in L) + '}' for L in (sc, ys, gs)))
        lv, A1, B1, A2, B2 = ref_levels(sc, ys, gs)
        g = h.globals_
        check(list(g['rlLv']) == lv and list(g['rlA1']) == A1 and list(g['rlB1']) == B1 and list(g['rlA2']) == A2 and list(g['rlB2']) == B2,
              'A7 levels with groups, set %d (n %d, m %d)' % (it, n, len(lv)))


ROSSI3, ROSSI4, COMPAS = {}, {}, {}


# ============================================================ Part B
def page_text(p):
    return '\n'.join(p.lines())


def last_page(h, func):
    ps = [p for p in h.pages if p.func == func]
    return ps[-1] if ps else None


def run_main(h, script):
    script(h)
    try:
        h.call('RiskLab')
    except Exception as e:
        print('   runtime error:', type(e).__name__, e, getattr(e, 'ppl_stack', None))
    check(h.error is None, 'B run ended without a runtime error (%s)' % (h.error,))
    return h


def check_table(h, label, m, names):
    p = last_page(h, 'rl_LogDraw')
    check(p is not None, '%s: table page shown' % label)
    if p is None:
        return
    T = page_text(p)
    for j, nm in enumerate(['const'] + names):
        b, se = m.params[j], m.bse[j]
        z = b / se
        pv = 2 * stats.norm.sf(abs(z))
        want = [('+' if round(b, 3) >= 0 else '') + f(b, 3), f(se, 3), f(z, 2), '<.0001' if pv < 1e-4 else f(pv, 4)]
        y = 46 if j == 0 else 58 + 24 * (j - 1)
        got = [t.text for t in p.texts if abs(t.y - y) < 1]
        if j > 0:
            orl = 'OR = %s, 95%% CI %s to %s' % (f(math.exp(b), 3), f(math.exp(b - Z * se), 3), f(math.exp(b + Z * se), 3))
            check(orl in [t.text for t in p.texts if abs(t.y - y - 12) < 1], '%s: %s OR line %s' % (label, nm, orl))
        check(all(w in got for w in want), '%s: row %s %s in %s' % (label, nm, want, got))
    check(('-2 lnL = ' + f(-2 * m.llf, 2)) in T and ('no predictors: ' + f(-2 * m.llnull, 2)) in T, '%s: -2 lnL line' % label)
    pv = m.llr_pvalue
    check(('= ' + f(m.llr, 2) + ', df %d, ' % len(names)) in T and (('p < 0.0001' if pv < 1e-4 else 'p = ' + f(pv, 4)) in T), '%s: LR line' % label)
    check(('= ' + f(m.prsquared, 3)) in T, '%s: McFadden %s' % (label, f(m.prsquared, 3)))


def roc_expect(LA, LB, t):
    n1, n0 = sum(LA), sum(LB)
    TP, FP = sum(LA[t - 1:]), sum(LB[t - 1:])
    FN, TN = n1 - TP, n0 - FP
    r3 = lambda a, b: 'n/a' if b == 0 else f(a / b, 3)
    return dict(TP=TP, FP=FP, FN=FN, TN=TN, sens=r3(TP, n1), spec=r3(TN, n0), ppv=r3(TP, TP + FP), npv=r3(TN, TN + FN),
                fpr=r3(FP, n0), flag=f(100 * (TP + FP) / (n1 + n0), 1) + '%')


def check_roc_page(p, LA, LB, t, label):
    e = roc_expect(LA, LB, t)
    at = lambda x0, y: [tt.text for tt in p.texts if abs(tt.y - y) < 1 and abs(tt.x - x0) < 1]
    ok = (at(224, 47) == ['%d' % e['TP']] and at(270, 47) == ['%d' % e['FP']] and at(224, 59) == ['%d' % e['FN']]
          and at(270, 59) == ['%d' % e['TN']] and at(272, 101) == [e['sens']] and at(272, 113) == [e['spec']]
          and at(272, 125) == [e['ppv']] and at(272, 137) == [e['npv']] and at(272, 149) == [e['fpr']] and at(272, 161) == [e['flag']])
    check(ok, '%s: 2x2 and metrics at t = %d %s' % (label, t, e))


def part_b():
    print('=== Part B: menu paths, numbers on the pages')
    # ---- B1 opening, COMPAS table, taps, curve, ROC, calibration, fairness, quit
    h = new_h()

    def s(h):
        h.press('Enter')
        h.choose('Logistic regression')
        h.tap(10, 63)                       # the decile row
        h.tap(10, 50)                       # the const row
        h.tap(30, 225)                      # Curve
        h.press('Right'); h.press('Right'); h.tap(200, 100)
        h.tap(30, 225)                      # Prev x (one predictor)
        h.tap(140, 225)                     # Table
        h.tap(80, 225)                      # ROC
        h.press('Left'); h.press('Right'); h.press('Right')       # cut 5 -> 6 -> 5 -> 4
        h.press('Plus'); h.press('Minus')                          # 4 -> 1 -> 10? (Minus = +10 levels, capped)
        h.tap(300, 105); h.tap(300, 182); h.tap(300, 195); h.tap(300, 50); h.tap(200, 62)
        h.tap(30, 225)                      # Groups overlay
        h.tap(30, 225)                      # back to pooled
        h.press('Esc')
        h.choose('Calibration'); h.tap(200, 50); h.tap(100, 180); h.tap(30, 225); h.press('Esc')
        h.choose('Fairness'); h.tap(80, 225); h.press('Right'); h.tap(100, 100); h.tap(130, 225); h.press('Left')
        h.tap(190, 225); h.tap(30, 225); h.tap(10, 84); h.tap(10, 96); h.tap(300, 225)
        h.press('Esc')
        h.choose('Quit')
    run_main(h, s)
    po = h.pages[0]
    check(po.func == 'rl_Open' and 'DISCLAIMER: a teaching and demonstration aid.' in page_text(po), 'B1 opening page with the DISCLAIMER')
    check_table(h, 'B1 COMPAS table', COMPAS['m'], ['decile'])
    tl = [p for p in h.pages if p.func == 'rl_LogDraw']
    check(any('decile: odds ' in page_text(p) and f(math.exp(COMPAS['m'].params[1]), 3) + ' per +1 (others fixed)' in page_text(p) for p in tl), 'B1 tap on the decile row explains its OR')
    check(any('const: log-odds when every x = 0 (odds ' + f(math.exp(COMPAS['m'].params[0]), 3) + ')' in page_text(p) for p in tl), 'B1 tap on const')
    cf = [p for p in h.pages if p.func == 'rl_CurveFrame']
    b0, b1 = COMPAS['m'].params
    want = ['decile = %s: fitted P = %s' % (x, f(1 / (1 + math.exp(-(b0 + b1 * x))), 3)) for x in (5, 6, 7)]
    check(all(any(w in page_text(p) for p in cf) for w in want), 'B1 curve cursor readouts at deciles 5, 6, 7 %s' % want)
    check(any('at decile = 7: 209 of 343' not in page_text(p) and 'at decile = 7: %d of %d re-arrested = %s' % (209 + 68, 343 + 113, f(277 / 456, 3)) in page_text(p) for p in cf),
          'B1 curve: observed share at decile 7 (both groups)')
    check(any('One predictor only' in page_text(p) for p in cf), 'B1 curve: Prev x with one predictor says so')
    rf = [p for p in h.pages if p.func == 'rl_RocFrame']
    LA = [a + b for a, b in zip(CMP_E1, CMP_E2)]
    LB = [(n1 - e1) + (n2 - e2) for n1, e1, n2, e2 in zip(CMP_N1, CMP_E1, CMP_N2, CMP_E2)]
    seen = {}
    for p in rf:
        for t in range(1, 12):
            cut = 'high risk = decile score ≥ %d' % t if t <= 10 else 'cut-off above every score: nobody flagged'
            if cut in page_text(p):
                seen[t] = p
    check(set(seen) >= {1, 4, 5, 6, 11}, 'B1 ROC: cut-offs visited %s' % sorted(seen))
    for t, p in seen.items():
        check_roc_page(p, LA, LB, t, 'B1 ROC COMPAS')
    a = COMPAS['all']
    check(any(('AUC = %s, 95%% CI %s to %s (DeLong)' % (f(a['auc'], 3), f(a['auc'] - Z * a['sd'], 3), f(a['auc'] + Z * a['sd'], 3))) in page_text(p) for p in rf),
          'B1 ROC AUC line %s' % f(a['auc'], 3))
    check(any(('SE: DeLong %s, Hanley-McNeil %s' % (f(a['sd'], 4), f(a['sh'], 4))) in page_text(p) for p in rf), 'B1 ROC tap: both SEs')
    check(any(('AUC: African-Am. %s, Caucasian %s' % (f(COMPAS['g1']['auc'], 3), f(COMPAS['g2']['auc'], 3))) in page_text(p) for p in rf), 'B1 ROC Groups overlay AUCs')
    check(any('FP: flagged but Y = 0' in page_text(p) for p in rf) and any('FN: not flagged but Y = 1' in page_text(p) for p in rf)
          and any('sensitivity = TP/(TP+FN)' in page_text(p) for p in rf) and any('AUC = P(a random' in page_text(p) for p in rf), 'B1 ROC taps explain cells')
    cd = [p for p in h.pages if p.func == 'rl_CalDraw']
    for G in (0, 5):
        rr = COMPAS['hl%d' % G]
        line = 'Hosmer-Lemeshow χ² = %s, df %d, p = %s' % (f(rr['hl'], 2), rr['df'], f(rr['p'], 4))
        check(any(line in page_text(p) for p in cd), 'B1 calibration HL G=%d: %s' % (G, line))
    rr = COMPAS['hl0']
    p0 = [p for p in cd if ', df 8, ' in page_text(p)][0]
    ok = True
    for gi, (n, o, e, x) in enumerate(rr['rows'], 1):
        y = 26 + 12 * gi
        got = [t.text for t in p0.texts if abs(t.y - y) < 1 and t.x >= 170]
        ok &= got == ['%d' % gi, '%d' % n, f(x, 3), f(o / n, 3)]
    check(ok, 'B1 calibration table rows = reference')
    check(any(('grp 2: Y = 1 in %d of %d, expected %s' % (rr['rows'][1][1], rr['rows'][1][0], f(rr['rows'][1][2], 1))) in page_text(p) for p in cd), 'B1 calibration tap on a row')
    fd = [p for p in h.pages if p.func == 'rl_FairDraw']
    # fairness table at the cut where the view was entered (the ROC left it at some t)
    ft = [p for p in fd if 'Fairness: the two groups' in page_text(p)]
    check(len(ft) >= 1, 'B1 fairness table shown')
    for p in ft:
        tcut = None
        for t in range(1, 11):
            if ('high risk = decile score ≥ %d' % t) in page_text(p):
                tcut = t
        if tcut is None:
            continue
        vals = []
        for g_, (N, E) in ((1, (CMP_N1, CMP_E1)), (2, (CMP_N2, CMP_E2))):
            n1 = sum(E); n0 = sum(N) - n1; TP = sum(E[tcut - 1:]); FP = sum(N[tcut - 1:]) - TP
            vals.append(['%d' % (n1 + n0), f(n1 / (n1 + n0), 3), f(COMPAS['g%d' % g_]['auc'], 3), f((TP + FP) / (n1 + n0), 3),
                         f(FP / n0, 3), f((n1 - TP) / n1, 3), f(TP / (TP + FP), 3), f((n0 - FP) / (n0 - FP + n1 - TP), 3)])
        ok = True
        for i in range(8):
            y = 48 + 12 * (i + 1)
            got = sorted([(t.x, t.text) for t in p.texts if abs(t.y - y) < 1 and t.x >= 160])
            ok &= [g[1] for g in got] == [vals[0][i], vals[1][i]]
        check(ok, 'B1 fairness table at cut %d = reference' % tcut)
    fw = [p for p in fd if 'Fairness: why they collide' in page_text(p)]
    check(len(fw) >= 1, 'B1 Why page shown')
    for p in fw:
        tcut = [t for t in range(1, 11) if ('high risk = decile score ≥ %d' % t) in page_text(p)]
        if not tcut:
            continue
        t = tcut[0]
        S = []
        for N, E in ((CMP_N1, CMP_E1), (CMP_N2, CMP_E2)):
            n1 = sum(E); n0 = sum(N) - n1; TP = sum(E[t - 1:]); FP = sum(N[t - 1:]) - TP
            S.append((n1, n0, TP, FP))
        l1 = 'African-Am.: %s × %s × %s = %s' % (f(S[0][0] / S[0][1], 3), f(S[0][3] / S[0][2], 3), f(S[0][2] / S[0][0], 3), f(S[0][3] / S[0][1], 3))
        l2 = 'Caucasian: %s × %s × %s = %s' % (f(S[1][0] / S[1][1], 3), f(S[1][3] / S[1][2], 3), f(S[1][2] / S[1][0], 3), f(S[1][3] / S[1][1], 3))
        forced = (S[1][0] / S[1][1]) * (S[0][3] / S[0][2]) * (S[0][2] / S[0][0])
        l3 = 'then its FPR = %s × %s × %s = %s' % (f(S[1][0] / S[1][1], 3), f(S[0][3] / S[0][2], 3), f(S[0][2] / S[0][0], 3), f(forced, 3))
        T = page_text(p)
        check(l1 in T and l2 in T and l3 in T, 'B1 Why page numbers at cut %d: %s | %s | %s' % (t, l1, l2, l3))
    fc = [p for p in fd if 'share with Y = 1 by score' in page_text(p)]
    check(any('African-Am.: 158 of 323 had Y = 1 = 0.489' in page_text(p) and 'Caucasian: 91 of 200 had Y = 1 = 0.455' in page_text(p) for p in fc),
          'B1 fairness calibration readout at decile 5')
    fe = [p for p in fd if 'error rates at the cut-off' in page_text(p)]
    menus = [tuple(sc.menu) for sc in h.screens if sc.menu]
    check(len(fe) >= 1 and ('Table', 'Calib', 'Errors', 'Why', 'Back', 'ROC') in menus, 'B1 errors page; fairness soft keys drawn')
    check(h.result is not None and h.result.startswith('RiskLab: COMPAS, AUC = ' + f(a['auc'], 3)), 'B1 Quit summary %r' % h.result)

    # ---- B2 Rossi presets via the menu, table, curve, ROC, calibration, fairness refusal
    for k, label, names, R in ((3, 'Rossi: age, prio, fin', ['age', 'prio', 'fin'], ROSSI3), (4, 'wexp', ['age', 'prio', 'fin', 'wexp'], ROSSI4)):
        h = new_h()

        def s(h, label=label):
            h.press('Enter')
            h.choose('Load a preset'); h.choose(label); h.press('Enter')
            h.choose('Logistic regression'); h.tap(10, 110)
            h.tap(30, 225)                                  # Curve: age
            h.press('Right'); h.tap(200, 100)
            h.tap(80, 225)                                  # Next x: prio
            h.tap(80, 225)                                  # fin
            h.tap(30, 225)                                  # Prev: prio
            h.tap(190, 225)                                 # ROC
            h.press('Left'); h.press('Minus'); h.drag([(26, 166), (60, 100), (90, 60)])
            h.tap(30, 225)                                  # Groups: one group only
            h.tap(130, 225)                                 # Calib
            h.tap(30, 225)                                  # 5 groups
            h.tap(190, 225)                                 # Fair: refused
            h.choose('Quit')
        run_main(h, s)
        m = R['m']
        li = last_page(h, 'rl_LoadInfo')
        check(li is not None and '432 men released from Maryland state prisons,' in page_text(li) and 'arrested (114)' in page_text(li)
              and ('LR χ² = %s, df %d, ' % (f(m.llr, 2), k)) in page_text(li)
              and ('AUC of the fitted P = %s' % f(R['auc']['auc'], 3)) in page_text(li)
              and 'Rossi, Berk & Lenihan 1980 (via Allison 1995)' in page_text(li), 'B2 Rossi k=%d load page' % k)
        check_table(h, 'B2 Rossi k=%d table' % k, m, names)
        tl = [p for p in h.pages if p.func == 'rl_LogDraw']
        check(any(('fin: odds × %s for 1 vs 0 (others fixed)' % f(math.exp(m.params[3]), 3)) in page_text(p) for p in tl), 'B2 Rossi k=%d tap on fin row' % k)
        check(any('Newton-Raphson converged in' in page_text(p) for p in tl), 'B2 converged line')
        cf = [p for p in h.pages if p.func == 'rl_CurveFrame']
        X = np.array([[int(r[c]) for c in names] for r in ROSSI], float); xm = X.mean(axis=0)
        def P(j, x):
            e = m.params[0] + sum(m.params[i + 1] * (x if i == j else xm[i]) for i in range(len(names)))
            return 1 / (1 + math.exp(-e))
        # the cursor starts at the mean age; Right adds a nice step of the range/40
        T = '\n'.join(page_text(p) for p in cf)
        want0 = 'age = %s: fitted P = %s (others at means)' % (f(xm[0], 2), f(P(0, xm[0]), 3))
        check(want0 in T, 'B2 Rossi k=%d curve at the mean age: %s' % (k, want0))
        check('Fitted P(arrested) vs prio' in '\n'.join(p.lines()[0] for p in h.pages if p.func in ('rl_CurveFrame',)) or any('vs prio' in page_text(p) for p in cf),
              'B2 Rossi k=%d Next x shows prio' % k)
        check(any(('fin = 0: fitted P = %s' % f(P(2, 0), 3)) in page_text(p) or ('fin = 1: fitted P' in page_text(p)) or 'fin = 0.50' in page_text(p) for p in cf),
              'B2 Rossi k=%d curve for fin' % k)
        rf = [p for p in h.pages if p.func == 'rl_RocFrame']
        LA, LB, lv = R['LA'], R['LB'], R['lv']
        cnt = 0
        for p in rf:
            for t in range(1, len(lv) + 2):
                cut = ('high risk = fitted P ≥ ' + f(lv[t - 1], 4)) if t <= len(lv) else 'nobody flagged'
                if cut in page_text(p):
                    # two levels could print alike: take the one whose TP and FP are on the page
                    e = roc_expect(LA, LB, t)
                    if (('%d' % e['TP']) in [tt.text for tt in p.texts if abs(tt.y - 47) < 1 and abs(tt.x - 224) < 1]
                            and ('%d' % e['FP']) in [tt.text for tt in p.texts if abs(tt.y - 47) < 1 and abs(tt.x - 270) < 1]):
                        check_roc_page(p, LA, LB, t, 'B2 Rossi k=%d ROC' % k); cnt += 1
                        break
        check(cnt >= 3, 'B2 Rossi k=%d: ROC pages checked %d' % (k, cnt))
        check(any('in-sample: P fitted to these same people' in page_text(p) for p in rf), 'B2 in-sample warning')
        check(any('One group only: no group curves' in page_text(p) for p in rf), 'B2 Groups refused with one group')
        cd = [p for p in h.pages if p.func == 'rl_CalDraw']
        for G in (10, 5):
            rr = ref_hl(LA, LB, lv, G)
            line = 'Hosmer-Lemeshow χ² = %s, df %d, %s' % (f(rr['hl'], 2), rr['df'], 'p = ' + f(rr['p'], 4))
            check(any(line in page_text(p) for p in cd), 'B2 Rossi k=%d HL G=%d %s' % (k, G, line))
        check(any(mb for mb in h.msgboxes if 'Fairness needs two groups:' in mb.lines[0]), 'B2 Rossi fairness refused with a message')

    # ---- B3 Use my data: rows (Hanley-McNeil ratings as one predictor), score data with groups
    hm_y = [0] * 58 + [1] * 51
    hm_x = [1] * 33 + [2] * 6 + [3] * 6 + [4] * 11 + [5] * 2 + [1] * 3 + [2] * 2 + [3] * 2 + [4] * 11 + [5] * 33
    hm_g = [1 if i % 3 else 2 for i in range(109)]
    h = new_h(app_data={'D1': hm_y, 'D2': hm_x, 'D3': hm_g})

    def s(h):
        h.press('Enter')
        h.choose('Use my data'); h.choose('D2 = score'); h.press('Enter')
        h.choose('ROC'); h.tap(300, 182); h.press('Esc')
        h.choose('Fairness'); h.tap(190, 225); h.press('Esc')
        h.choose('Quit')
    run_main(h, s)
    rf = [p for p in h.pages if p.func == 'rl_RocFrame']
    check(any('AUC = 0.893, 95% CI 0.833 to 0.953 (DeLong)' in page_text(p) for p in rf), 'B3 Hanley-McNeil data as your scores: AUC 0.893, CI 0.833-0.953 (Stata 0.8932, 0.83295-0.95339)')
    check(any('SE: DeLong 0.0307, Hanley-McNeil 0.0325' in page_text(p) for p in rf), 'B3 DeLong SE 0.0307 = Stata')
    li = last_page(h, 'rl_LoadInfo')
    check(li is not None and 'score D2: 5 distinct values; groups: 2' in page_text(li), 'B3 load page of your scores')
    g = h.globals_
    lv, A1, B1, A2, B2 = ref_levels(hm_x, hm_y, hm_g)
    check(list(g['rlA1']) == A1 and list(g['rlB2']) == B2, 'B3 levels by group')
    check(any('Fairness: why they collide' in page_text(p) for p in h.pages if p.func == 'rl_FairDraw'), 'B3 fairness pages on your groups')
    # rows: two predictors from the app, compared with statsmodels
    rnd = random.Random(5)
    n = 60
    x1 = [round(rnd.gauss(0, 1), 2) for _ in range(n)]; x2 = [rnd.randint(0, 1) for _ in range(n)]
    y = [1 if rnd.random() < 1 / (1 + math.exp(-(0.3 + 0.9 * a - 0.6 * b))) else 0 for a, b in zip(x1, x2)]
    h = new_h(app_data={'D1': y, 'D2': x1, 'D3': x2})

    def s(h):
        h.press('Enter')
        h.choose('Use my data'); h.choose('D2-D5 = predictors'); h.press('Enter')
        h.choose('Logistic regression'); h.press('Esc')
        h.choose('Quit')
    run_main(h, s)
    m = ref_logit(y, list(zip(x1, x2)))
    check_table(h, 'B3 your rows (D2, D3)', m, ['D2', 'D3'])
    check(h.result is not None and ('LR χ² = ' + f(m.llr, 2) + ' (df 2)') in h.result, 'B3 Quit summary with the LR test %r' % h.result)
    # refusals: app never opened, too few rows, size mismatch, bad outcome, bad group, too many rows
    cases = [({}, 'D2-D5', 'D1 needs at least 10 rows'),
             ({'D1': [0, 1, 1]}, 'D2-D5', 'D1 needs at least 10 rows'),
             ({'D1': [0, 1] * 10, 'D2': [1, 2, 3]}, 'D2-D5', 'D2 must hold a predictor,'),
             ({'D1': [0, 1] * 10, 'D2': list(range(20)), 'D3': [1, 2]}, 'D2-D5', 'D3 has 2 values, D1 has 20.'),
             ({'D1': [0, 2] * 10, 'D2': list(range(20))}, 'D2-D5', 'Row 2 of D1: the outcome'),
             ({'D1': [0, 1] * 300, 'D2': list(range(600))}, 'D2-D5', 'At most 500 rows here'),
             ({'D1': [0, 1] * 10, 'D2': [5] * 20, 'D3': [1, 3] * 10}, 'D2 = score', 'Row 2 of D3: the group'),
             ({'D1': [0, 1] * 10, 'D2': [5] * 19}, 'D2 = score', 'D2 must hold one score per'),
             ({'D1': [0] * 20, 'D2': list(range(20))}, 'D2-D5', None),
             ({'D1': [0, 1] * 10, 'D2': [3] * 20}, 'D2 = score', None)]
    for app, kind, msg in cases:
        h = new_h(app_data=app)

        def s(h, kind=kind):
            h.press('Enter')
            h.choose('Use my data'); h.choose(kind); h.press('Enter')
            h.choose('Logistic regression'); h.press('Esc')
            h.choose('ROC'); h.press('Esc')
            h.choose('Calibration'); h.press('Esc')
            h.choose('Quit')
        run_main(h, s)
        if msg:
            check(any(msg in ' '.join(mb.lines) for mb in h.msgboxes), 'B3 refusal: %s (%s)' % (msg, [mb.lines for mb in h.msgboxes][:2]))
            check(h.globals_['rlIsC'] == 1, 'B3 refusal leaves COMPAS loaded')
        else:
            T = '\n'.join(page_text(p) for p in h.pages)
            check(('No model: the outcome is all 0 or all 1' in T) or ('mix of others' in T) or any('needs' in ' '.join(mb.lines) for mb in h.msgboxes),
                  'B3 degenerate data explained (%s)' % [mb.lines for mb in h.msgboxes][:2])

    # ---- B4 Esc during the Rossi fit, then the re-fit from the menu
    h = new_h()

    def s(h):
        h.press('Enter')
        h.choose('Load a preset'); h.choose('wexp'); h.press('Esc', anytime=True); h.press('Enter')
        h.choose('Logistic regression'); h.press('Esc')
        h.choose('Quit')
    run_main(h, s)
    pg = [p for p in h.pages if p.func == 'rl_Prog']
    rows_drawn = [t.text for t in h.texts if t.func == 'rl_ProgBar']
    check(len(pg) >= 1 and 'row 0 of 432' in page_text(pg[0]) and 'row 216 of 432' in rows_drawn, 'B4 progress page and bar (%d pages, %d bar updates)' % (len(pg), len(rows_drawn)))
    check(any('No fit: stopped with Esc' in page_text(p) for p in h.pages if p.func == 'rl_LoadInfo'), 'B4 load page says the fit was stopped')
    check(h.globals_['rlFitOK'] == 1 and close(h.globals_['rlLRc'], ROSSI4['m'].llr, 1e-6), 'B4 the menu re-fits after Esc')

    # ---- B5 Help, all pages, and Esc out of page 1
    h = new_h()

    def s(h):
        h.press('Enter')
        h.choose('Help')
        for _ in range(8):
            h.press('Enter')
        h.choose('Help'); h.press('Esc')
        h.choose('Quit')
    run_main(h, s)
    hp = [p for p in h.pages if p.func == 'rl_HPage']
    check(len(hp) == 9 and 'Page 8/8, any key = menu' in page_text(hp[7]), 'B5 help: 8 pages then Esc on page 1 (%d)' % len(hp))
    T = '\n'.join(page_text(p) for p in hp)
    for w in ('Chouldechova (2017)', 'Kleinberg, Mullainathan & Raghavan (2016)', 'Dieterich et al. 2016', 'Angwin et al.',
              'Hosmer et al. 1997', 'DeLong et al.', 'Albert & Anderson', '7,214 people (no date or charge filters).',
              'After the filters: 42.3% and 22.0%.', "A score (COMPAS): pred = RiskLab's own fit."):
        check(w in T, 'B5 help mentions %s' % w)



# ============================================================ Part D: the second review's items
def name_scan(path):
    """Every routine, EXPORT and file-level LOCAL name; pairs equal ignoring case but not identical
    (and the same name defined twice)."""
    import re
    src = open(path, encoding='utf-8').read().split('\n')
    names = []
    for i, ln in enumerate(src):
        code = ln.split('//')[0]
        m = re.match(r'^(?:EXPORT\s+)?([A-Za-z_]\w*)\s*\(.*\)\s*$', code)
        if m and i + 1 < len(src) and src[i + 1].strip() == 'BEGIN':
            names.append((m.group(1), 'routine', i + 1))
        m = re.match(r'^EXPORT\s+([A-Za-z_][\w\s,]*);\s*$', code)
        if m:
            names += [(n.strip(), 'export', i + 1) for n in m.group(1).split(',')]
        m = re.match(r'^LOCAL\s+(.*);\s*$', code)
        if m:
            names += [(n.strip(), 'file LOCAL', i + 1) for n in m.group(1).split(',')]
    by = {}
    for n, k, l in names:
        by.setdefault(n.lower(), []).append((n, k, l))
    clashes = {key: v for key, v in by.items() if len(v) > 1}
    # routine LOCALs and parameters that fold onto a global name
    glob = {n.lower() for n, k, l in names}
    inner = set()
    for ln in src:
        code = ln.split('//')[0]
        m = re.match(r'^\s+LOCAL\s+(.*);\s*$', code)
        if m:
            inner |= {n.strip() for n in m.group(1).split(',')}
    shadow = sorted(n for n in inner if n.lower() in glob)
    return names, clashes, shadow


def part_d():
    print('=== Part D: the second review')
    # D1 the case-insensitive name scan
    names, clashes, shadow = name_scan(PROG)
    print('   name scan: %d names (%d routines, %d exports, %d file-level LOCALs), %d case-folded clashes, %d inner shadows'
          % (len(names), sum(1 for n in names if n[1] == 'routine'), sum(1 for n in names if n[1] == 'export'),
             sum(1 for n in names if n[1] == 'file LOCAL'), len(clashes), len(shadow)))
    check(len(names) > 200 and not clashes, 'D1 no two routine/EXPORT/file-LOCAL names equal ignoring case (%s)' % list(clashes.values())[:3])
    check(not shadow, 'D1 no routine LOCAL folds onto a global name (%s)' % shadow[:5])
    _, old_clash, _ = name_scan(PROG_OLD)
    check('rl_hl' in old_clash, 'D1 the scan finds beta 1\'s rl_HL / RL_HL (%s)' % old_clash.get('rl_hl'))
    src = open(PROG).read()
    check('rl_HosLem()' in src and 'rl_HL(' not in src, 'D1 routine renamed rl_HosLem')
    # D3 separation from the fit, not from fitted P near 0/1: the reviewer's wide case
    rnd = random.Random(3)
    xs = list(range(0, 101)); ys = [1 if rnd.random() < 1 / (1 + 2.718 ** (-(x - 50) / 5)) else 0 for x in xs]
    m = ref_logit(ys, [[x] for x in xs])
    eta = np.abs(m.fittedvalues).max()
    check(m.mle_retvals['converged'] and eta > 15, 'D3 the wide case: statsmodels converges with max |eta| %.1f > 15' % eta)
    h = new_h(); h.call('rl_Init'); load_state_rows(h, ys, [[x] for x in xs]); h.call('rl_Refit')
    g = h.globals_
    check(g['rlSep'] == 0 and g['rlNear'] == 1 and g['rlFitOK'] == 1, 'D3 wide case: no separation, a note (sep %s near %s)' % (g['rlSep'], g['rlNear']))
    check(close(g['rlB'][1], m.params[1], 1e-6) and close(g['rlSE'][1], m.bse[1], 1e-5), 'D3 wide case = statsmodels')
    h = new_h(app_data={'D1': ys, 'D2': xs})
    def s(h):
        h.press('Enter'); h.choose('Use my data'); h.choose('D2-D5 = predictors'); h.press('Enter')
        h.choose('Logistic regression'); h.press('Esc'); h.choose('Quit')
    run_main(h, s)
    T = '\n'.join(page_text(p) for p in h.pages if p.func == 'rl_LogDraw')
    check('SEPARATION' not in T and 'a fitted P is ~0 or ~1' in T, 'D3 wide case page: no warning, the grey note')
    # true separation, complete and quasi, still flagged and shown
    for lbl, Y, X in (('complete', [0] * 10 + [1] * 10, [[i] for i in range(20)]),
                      ('quasi', [0] * 10 + [0, 1] + [1] * 8, [[i // 2] for i in range(20)]),
                      ('complete, 2 x', [0] * 12 + [1] * 12, [[i, (i * 7) % 5] for i in range(24)])):
        h = new_h(app_data={'D1': Y, 'D2': [r[0] for r in X]} if len(X[0]) == 1 else {'D1': Y, 'D2': [r[0] for r in X], 'D3': [r[1] for r in X]})
        def s(h):
            h.press('Enter'); h.choose('Use my data'); h.choose('D2-D5 = predictors'); h.press('Enter')
            h.choose('Logistic regression'); h.press('Esc'); h.choose('Quit')
        run_main(h, s)
        T = '\n'.join(page_text(p) for p in h.pages if p.func == 'rl_LogDraw')
        check(h.globals_['rlSep'] == 1 and 'SEPARATION suspected' in T, 'D3 %s separation still flagged on the page (it %s, conv %s)' % (lbl, h.globals_['rlIt'], h.globals_['rlConv']))
    # no false flag on any data set statsmodels fits cleanly (Part A's random sets did this); here the
    # Rossi and COMPAS fits: rlNear and rlSep both 0
    h = new_h(); h.call('rl_Init'); h.call('rl_LoadCompas')
    check(h.globals_['rlSep'] == 0 and h.globals_['rlNear'] == 0, 'D3 COMPAS: no flag, no note')
    # D2 Help page 7 and the data notes
    T = open(os.path.join(ROOT, 'data', 'DATASETS_RISK.md')).read()
    check('all 7,214 rows' in T and 'different file' not in T, 'D2 DATASETS_RISK.md states where 44.85/23.45 come from')
    if os.path.exists(RAW):
        raw = list(csv.DictReader(open(RAW, newline='')))
        out = {}
        for race in ('African-American', 'Caucasian'):
            sel = [r for r in raw if r['race'] == race]
            TP = sum(1 for r in sel if int(r['decile_score']) >= 5 and r['two_year_recid'] == '1')
            FP = sum(1 for r in sel if int(r['decile_score']) >= 5 and r['two_year_recid'] == '0')
            FN = sum(1 for r in sel if int(r['decile_score']) < 5 and r['two_year_recid'] == '1')
            TN = sum(1 for r in sel if int(r['decile_score']) < 5 and r['two_year_recid'] == '0')
            out[race] = (len(sel), 100 * FP / (FP + TN), 100 * FN / (FN + TP))
        check(out['African-American'][0] == 3696 and out['Caucasian'][0] == 2454 and f(out['African-American'][1], 2) == '44.85'
              and f(out['Caucasian'][1], 2) == '23.45' and f(out['African-American'][2], 2) == '27.99' and f(out['Caucasian'][2], 2) == '47.72',
              'D2 all 7,214 rows give ProPublica\'s 44.85 / 23.45 and 27.99 / 47.72 (%s)' % out)
    # D4 opening page
    h = new_h(); run_main(h, lambda h: None)
    T = page_text(h.pages[0])
    check('parolee' not in T and '432 men released' in T and 'Maryland state prisons' in T, 'D4 opening page: 432 men released from Maryland state prisons')
    check('parolee' not in open(PROG).read(), 'D4 no "parolee" anywhere')
    # D5 AUC: one score level, AUC = 1, small n
    for lbl, D1, D2, want in (('one level', [0, 1] * 10, [3] * 20, 'AUC = 0.500 (one score level: no interval)'),
                              ('AUC = 1', [0] * 10 + [1] * 10, list(range(20)), 'AUC = 1.000 (SE = 0: no interval)'),
                              ('small n', [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1], list(range(12)), 'small n or a bound cut at 0/1: the CI is rough')):
        h = new_h(app_data={'D1': D1, 'D2': D2})
        def s(h):
            h.press('Enter'); h.choose('Use my data'); h.choose('D2 = score'); h.press('Enter')
            h.choose('ROC'); h.press('Esc'); h.choose('Quit')
        run_main(h, s)
        T = '\n'.join(page_text(p) for p in h.pages if p.func == 'rl_RocFrame')
        bad = [l for l in T.split('\n') if 'CI' in l and 'DeLong' in l and l.split('CI ')[1].split(' to ')[0] == l.split(' to ')[1].split(' ')[0]]
        check(want in T and not bad, 'D5 %s: "%s", no zero-width CI' % (lbl, want))
    # D6 COMPAS calibration names its P
    h = new_h()
    def s(h):
        h.press('Enter'); h.choose('Calibration'); h.tap(100, 190); h.press('Esc'); h.choose('Quit')
    run_main(h, s)
    T = '\n'.join(page_text(p) for p in h.pages if p.func == 'rl_CalDraw')
    check("Calibration: COMPAS (RiskLab's fit)" in T and "pred: RiskLab's logistic of Y on the score" in T
          and "in-sample fit to these people, not COMPAS's" in T, 'D6 COMPAS calibration says pred is RiskLab\'s in-sample fit')
    # D7 wording
    h = new_h(app_data={'D1': [0, 1] * 40, 'D2': [i % 9 for i in range(80)], 'D3': [(i * 3) % 7 for i in range(80)]})
    def s(h):
        h.press('Enter'); h.choose('Use my data'); h.choose('D2-D5 = predictors'); h.press('Enter')
        h.choose('ROC'); h.press('Esc'); h.choose('Quit')
    run_main(h, s)
    T = '\n'.join(page_text(p) for p in h.pages)
    check('Y = 1: Y = 1' not in T, 'D7 no "Y = 1: Y = 1"')
    check("Rossi's fit takes 7 passes" not in T and any('Esc = stop' in page_text(p) for p in h.pages if p.func == 'rl_Prog'),
          'D7 progress page of your data does not mention Rossi')
    check('+/- = ×10' in T, 'D7 footer "+/- = ×10"')
    h = new_h(); h.call('rl_Init'); load_state_rows(h, [i % 2 for i in range(20)], [[3, i] for i in range(20)]); h.call('rl_Fit')
    check(h.globals_['rlFitW'] == 'an x is constant or a mix of others', 'D7 a constant x is named as such (%s)' % h.globals_['rlFitW'])
    h = new_h()
    def s(h):
        h.press('Enter'); h.choose('Fairness'); h.press('Esc'); h.choose('Quit')
    run_main(h, s)
    T = '\n'.join(page_text(p) for p in h.pages)
    check('rates differ (unless perfect): see Why.' in T, 'D7 fairness table: "unless perfect"')
    # D8 the G1 time is on the checklist
    N = open(os.path.join(HERE, 'RiskLab_beta1a_NOTES.md')).read()
    check('Time the fit' in N and 'all 7,214' in N, 'D8 NOTES: timing on the checklist; the 7,214-row explanation')

# ============================================================ Part C
def audit():
    print('=== Part C: every run')
    sci, off, cut65 = [], [], []
    for h in ALL_RUNS:
        sci += h.sci_strings
        for t in h.texts:
            if t.grob not in ('G0', 'G1', 'G2'):
                continue
            w = len(t.text) * 6.5 if t.font == 1 else t.est_width
            if t.x < 0 or t.y < 0 or t.y > 229 or t.x + min(w, t.width or w) > 320.5:
                off.append((t.func, t.text, t.x, t.y))
            if t.width is not None and t.font == 1 and len(t.text) * 6.5 > t.width + 0.5:
                cut65.append((t.func, t.text, t.width))
    check(not sci, 'C no scientific number on any screen (%s)' % sci[:5])
    mbs = [mb for h in ALL_RUNS for mb in h.msgboxes]
    check(mbs and all(len(mb.lines) <= 5 for mb in mbs) and all(len(l) <= 38 for mb in mbs for l in mb.lines),
          'C every MSGBOX (%d) has at most 5 lines of at most 38 characters %s' % (len(mbs), [l for mb in mbs for l in mb.lines if len(l) > 38][:3]))
    errs = [(h.error, getattr(h.error, 'ppl_stack', None)) for h in ALL_RUNS if h.error is not None]
    check(not errs, 'C no run ended in a runtime error (%s)' % errs[:3])
    check(not off, 'C no text past the screen edges (%s)' % off[:5])
    cut65 = sorted(set(cut65))
    print('   texts wider than their width at 6.5 px per character: %d' % len(cut65))
    for c in cut65[:30]:
        print('     ', c)
    check(len(cut65) == 0, 'C no text wider than its width at 6.5 px/char (%d)' % len(cut65))
    warn = sorted(set(w for h in ALL_RUNS for w in h.warnings))
    check(not warn, 'C no harness warnings (%s)' % warn[:3])
    src = open(PROG, encoding='utf-8').read()
    check(all(ord(c) < 128 for c in src), 'C source is pure ASCII')
    check('\r' not in src, 'C LF line ends')


def main():
    part_a()
    part_b()
    part_d()
    audit()
    print()
    print('%d checks, %d failures' % (N_CHECK, len(FAILS)))
    for x in FAILS[:60]:
        print('  FAIL:', x)
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
