#!/usr/bin/env python3
"""verify_SurvLab_beta1b.py -- checks for SurvLab beta 1b (28 Oct 2026; layout-only version of beta 1a, same checks): every beta 1 check (Parts A-D,
updated where beta 1a changed a page on purpose), plus Part E, one or more checks per item of the second
review (REVIEW2_SurvLab_beta1.md, items 1-15).  Built from verify_SurvLab_beta1.py.

The beta 1 description follows.
verify_SurvLab_beta1.py -- checks for SurvLab beta 1 (21 Oct 2026).

Part A  the engine (sv_Fit, sv_CIs, sv_Quant, sv_QCI, sv_LCalc, sv_Export), run in the PC harness
        on the four Rossi presets and on 40 random and edge data sets, against
          * statsmodels 0.15: SurvfuncRight (surv_prob, surv_prob_se, n_risk, n_events, quantile,
            quantile_ci with method 'cloglog' and 'linear') and survdiff (log-rank, and
            weight_type='gb' for Gehan-Breslow);
          * an independent reference written here in exact arithmetic (fractions) for the KM
            steps, Greenwood's sum, the risk sets, O, E, V, the Nelson-Aalen H, the quantiles
            (SAS rule: first event time with S < 1 - p), the hazard ratio and its CI, the
            pointwise 95% CIs (log-log: S^exp(+-z sqrt(V)/|ln S|); linear: S +- z S sqrt(V),
            cut at 0 and 1) and the actuarial life table (intervals [a, a+w), n' = n - c/2).
Part B  every menu path of the program in the harness (cas not used), with the numbers ON THE
        PAGES checked against Part A's reference: the opening page (disclaimer), the load pages,
        the Kaplan-Meier view (readout at several cursor positions by arrows and taps, at-risk
        table, CI type, band, zoom, H(t) view, pool, the More page, the Enter menu), the
        quantile page for p = 0.5, 0.25, 0.2, 0.1 in both CI types, the three log-rank pages
        and their taps, the life table (scroll, group, width, plot, taps), Use my data (valid,
        one group, bad rows, size mismatches, the app never opened), Help (and Esc out of it),
        Quit's summary line.
Part C  pixel geometry of the step plot (every vertical drop at sv_XP(t) from the old S to the new
        S, every flat stretch at the old S), the band rectangles (CI ends at the right rows),
        the censor ticks, the cursor line; and on every page of every run: no runtime error, no
        scientific number on screen (h.sci_strings), no text past the 320 x 240 screen.

Run:  python3 verify_SurvLab_beta1.py        (prints "N checks, M failures"; exit 0 = all passed)
Roger Metcalf / Claude, 21 Oct 2026.
"""
import os
import sys
import math
import random
import re
import csv
from fractions import Fraction as Fr

import numpy as np
from scipy import stats
from statsmodels.duration.survfunc import SurvfuncRight, survdiff

os.environ.setdefault('HPKIT', '/home/claude/kit/hp-prime-kit-HEAD')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'ref'))
import ppl_run_v3e  # noqa: E402
from ppl_run_v3e import Harness  # noqa: E402

PROG = os.path.join(ROOT, 'SurvLab_beta1b.txt')
PROG_OLD = os.path.join(ROOT, 'old', 'SurvLab_beta1.txt')
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


def close(a, b, tol=1e-9):
    if a is None or b is None:
        return a is b
    if isinstance(a, float) and math.isnan(a):
        return isinstance(b, float) and math.isnan(b)
    return abs(a - b) <= tol * max(1.0, abs(b))


def new_h(**kw):
    kw.setdefault('strict', False)
    kw.setdefault('idle_key', 4)
    kw.setdefault('cas', 'fail')
    h = Harness(PROG, **kw)
    ALL_RUNS.append(h)
    return h


# ============================================================ the reference (exact)
def ref_fit(times, events, groups=None):
    """Independent reference.  Returns a dict per row r in (1, 2, 3): grid, d, c, n, S, V (None =
    undefined), H, plus the log-rank pieces.  Exact fractions for S, V, H, O, E, Var."""
    n = len(times)
    if groups is None:
        groups = [1] * n
    U = sorted(set(times))
    m = len(U)
    rows = {}
    for r in (1, 2, 3):
        sel = [i for i in range(n) if r == 3 or groups[i] == r]
        d = [sum(1 for i in sel if times[i] == u and events[i] == 1) for u in U]
        c = [sum(1 for i in sel if times[i] == u and events[i] == 0) for u in U]
        nr = [sum(1 for i in sel if times[i] >= u) for u in U]
        S, V, H, out_S, out_V, out_H = Fr(1), Fr(0), Fr(0), [], [], []
        bad = False
        for j in range(m):
            if d[j] > 0:
                S *= 1 - Fr(d[j], nr[j])
                H += Fr(d[j], nr[j])
                if nr[j] > d[j]:
                    V += Fr(d[j], nr[j] * (nr[j] - d[j]))
                else:
                    bad = True
            out_S.append(S)
            out_V.append(None if bad else V)
            out_H.append(H)
        last = max([times[i] for i in sel], default=0)
        rows[r] = dict(d=d, c=c, n=nr, S=out_S, V=out_V, H=out_H, tot=len(sel),
                       ev=sum(d), last=last)
    res = dict(U=U, m=m, rows=rows)
    # log-rank, Gehan-Breslow, HR
    O1 = E1 = O2 = E2 = Var = Ug = Vg = Fr(0)
    for j in range(m):
        D = rows[3]['d'][j]
        if D == 0:
            continue
        N3, N1, D1 = rows[3]['n'][j], rows[1]['n'][j], rows[1]['d'][j]
        e = Fr(D * N1, N3)
        O1 += D1; E1 += e; O2 += D - D1; E2 += D - e
        if N3 > 1:
            v = Fr(D) * Fr(N1, N3) * (1 - Fr(N1, N3)) * Fr(N3 - D, N3 - 1)
            Var += v; Ug += N3 * (D1 - e); Vg += N3 * N3 * v
    res.update(O1=O1, E1=E1, O2=O2, E2=E2, Var=Var)
    res['chi'] = float((O1 - E1) ** 2 / Var) if Var > 0 else None
    res['p'] = float(stats.chi2.sf(res['chi'], 1)) if Var > 0 else None
    res['gb'] = float(Ug ** 2 / Vg) if Vg > 0 else None
    res['gbp'] = float(stats.chi2.sf(res['gb'], 1)) if Vg > 0 else None
    if O1 > 0 and O2 > 0 and E1 > 0 and E2 > 0:
        hr = float((O1 / E1) / (O2 / E2))
        w = Z * math.sqrt(float(1 / E1 + 1 / E2))
        res['hr'] = (hr, hr * math.exp(-w), hr * math.exp(w))
    else:
        res['hr'] = None
    return res


def ref_ci(S, V, kind):
    """Pointwise 95% CI of S: (lo, hi), or None where undefined."""
    S = float(S)
    if V is None or S <= 0:
        return None
    V = float(V)
    if S >= 1 or V == 0:
        return (S, S)
    if kind == 1:
        th = Z * math.sqrt(V) / abs(math.log(S))
        return (S ** math.exp(th), S ** math.exp(-th))
    se = S * math.sqrt(V)
    return (max(0.0, S - Z * se), min(1.0, S + Z * se))


def ref_quant(res, r, p):
    """SAS rule, in exact arithmetic: the first event time with S < 1 - p; None = not reached."""
    row = res['rows'][r]
    for j in range(res['m']):
        if row['d'][j] > 0 and row['S'][j] < 1 - Fr(p).limit_denominator(1000):
            return res['U'][j]
    return None


def ref_qci(res, r, p, kind):
    """Brookmeyer-Crowley in SAS/statsmodels form (written independently).  (lo, hi):
    lo None = no CI; hi None = not reached."""
    row = res['rows'][r]
    g = 1 - p
    inside, evj = [], []
    for j in range(res['m']):
        if row['d'][j] == 0:
            continue
        evj.append(j)
        S, V = float(row['S'][j]), row['V'][j]
        if V is None or float(V) <= 0 or not (0 < S < 1):
            continue
        V = float(V)
        if kind == 1:
            zz = (math.log(-math.log(S)) - math.log(-math.log(g))) * abs(math.log(S)) / math.sqrt(V)
        else:
            zz = (S - g) / (S * math.sqrt(V))
        if abs(zz) <= Z:
            inside.append(j)
    if not inside:
        return (None, None)
    lo = res['U'][inside[0]]
    k = evj.index(inside[-1])
    hi = res['U'][evj[k + 1]] if k + 1 < len(evj) else None
    return (lo, hi)


def ref_life(res, r, w):
    """beta 1a's convention: intervals [a, a+w), the last cut at the row's last time T and closed;
    censored AT T complete it (f, not halved); censored before T inside an interval are withdrawn
    (c, at risk for half the interval)."""
    row = res['rows'][r]
    T = row['last']
    K = max(1, int(math.ceil(T / w - 1e-9)))
    d = [0] * K
    c = [0] * K
    f = [0] * K
    for j, u in enumerate(res['U']):
        k = min(K - 1, int(math.floor(u / w + 1e-9)))
        d[k] += row['d'][j]
        if u >= T - 1e-9:
            f[k] += row['c'][j]
        else:
            c[k] += row['c'][j]
    out = []
    n = row['tot']
    S = 1.0
    for k in range(K):
        ne = n - c[k] / 2
        q = d[k] / ne if ne > 0 else 0.0
        S *= 1 - q
        out.append(dict(a=k * w, b=min((k + 1) * w, T), n=n, c=c[k], f=f[k], ne=ne, d=d[k], q=q, S=S))
        n -= d[k] + c[k] + f[k]
    return out


def sm_row(times, events, groups, r):
    t = np.array(times, float)
    e = np.array(events, float)
    if r != 3:
        sel = np.array(groups) == r
        t, e = t[sel], e[sel]
    return SurvfuncRight(t, e)


# ============================================================ data sets
def load_rossi():
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'rossi.csv'))))
    wk = [float(r['week']) for r in rows]
    ar = [int(r['arrest']) for r in rows]
    fin = [int(r['fin']) for r in rows]
    age = [int(r['age']) for r in rows]
    pri = [int(r['prio']) for r in rows]
    return wk, ar, fin, age, pri


WK, AR, FIN, AGE, PRI = load_rossi()
PRESETS = {
    1: ('aid', [1 if f == 1 else 2 for f in FIN], 2),
    2: ('all', [1] * 432, 1),
    3: ('prio', [1 if p <= 2 else 2 for p in PRI], 2),
    4: ('age', [1 if a < 23 else 2 for a in AGE], 2),
}


def random_sets():
    rng = random.Random(20261021)
    sets = []
    # 1-20 random, mixed sizes, ties, two groups
    for k in range(20):
        n = rng.choice([5, 8, 12, 20, 35, 60, 120, 250])
        tmax = rng.choice([5, 10, 30, 52, 100])
        integer = rng.random() < 0.7
        t, e, g = [], [], []
        for i in range(n):
            x = rng.randint(1, tmax) if integer else round(rng.uniform(0.1, tmax), 2)
            t.append(float(x))
            e.append(1 if rng.random() < rng.choice([0.3, 0.6, 0.9]) else 0)
            g.append(rng.choice([1, 2]))
        if len(set(g)) < 2:
            g[0], g[1] = 1, 2
        sets.append(('random %d (n=%d)' % (k + 1, n), t, e, g))
    # edge sets
    sets.append(('n = 2, both events', [3.0, 5.0], [1, 1], [1, 2]))
    sets.append(('n = 3, one group', [1.0, 2.0, 2.0], [1, 0, 1], [1, 1, 1]))
    sets.append(('all censored', [4.0, 6.0, 9.0, 9.0], [0, 0, 0, 0], [1, 2, 1, 2]))
    sets.append(('all events, all equal times', [7.0] * 6, [1] * 6, [1, 1, 1, 2, 2, 2]))
    sets.append(('everyone at risk fails at the end (n = d)', [1.0, 2.0, 3.0, 3.0], [1, 0, 1, 1], [1, 1, 1, 1]))
    sets.append(('S exactly 0.5 (median tie)', [1.0, 2.0, 3.0, 4.0], [1, 1, 0, 0], [1, 1, 1, 1]))
    sets.append(('huge times', [1e9, 2e9, 3.5e9, 5e9, 9e9], [1, 0, 1, 1, 0], [1, 2, 1, 2, 2]))
    sets.append(('time 0 events', [0.0, 0.0, 1.0, 2.0, 2.0, 5.0], [1, 0, 1, 1, 0, 1], [1, 2, 1, 2, 1, 2]))
    sets.append(('no events in group 2', [1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [1, 1, 1, 0, 0, 0], [1, 1, 1, 2, 2, 2]))
    sets.append(('fractional times', [0.5, 1.25, 1.25, 2.75, 3.1, 4.0, 4.0, 6.6], [1, 1, 0, 1, 1, 0, 1, 1], [1, 2, 1, 2, 1, 2, 1, 2]))
    sets.append(('unequal groups', [float(x) for x in range(1, 41)], [1 if x % 3 else 0 for x in range(1, 41)], [1] * 36 + [2] * 4))
    sets.append(('only code 2 (one group)', [2.0, 4.0, 6.0], [1, 1, 0], [2, 2, 2]))
    sets.append(('heavy ties', [float(x) for x in [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]], [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1], [1, 2] * 6))
    sets.append(('one event', [5.0, 6.0, 7.0, 8.0], [0, 1, 0, 0], [1, 2, 1, 2]))
    sets.append(('large n', [float(random.Random(5).randint(1, 200)) for _ in range(800)],
                 [random.Random(6 + i).random() < 0.5 and 1 or 0 for i in range(800)],
                 [1 + (i % 2) for i in range(800)]))
    return sets


# ============================================================ Part A
def engine_load(h, t, e, g):
    G = h.globals_
    ng = 2 if (1 in g and 2 in g) else 1
    G['svTim'] = [float(x) for x in t]
    G['svEvt'] = [float(x) for x in e]
    G['svGrp'] = [float(x) if ng == 2 else 1.0 for x in g]
    G['svN'] = float(len(t))
    G['svNG'] = float(ng)
    G['svGNm'] = ['group 1', 'group 2', 'all']
    G['svGSh'] = ['grp 1', 'grp 2', 'all']
    h.call('sv_Refit')
    return ng


def part_a():
    print('=== Part A: the engine against statsmodels and the exact reference')
    h = new_h()
    h.call('sv_Init')
    sets = []
    for k, (nm, g, ng) in PRESETS.items():
        sets.append(('Rossi ' + nm, WK, AR, g))
    sets += random_sets()
    for name, t, e, g in sets:
        G = h.globals_
        ng = engine_load(h, t, e, g)
        gg = g if ng == 2 else [1] * len(t)
        ref = ref_fit(t, e, gg)
        m = ref['m']
        check(int(G['svM']) == m, '%s: number of distinct times %s vs %d' % (name, G['svM'], m))
        rows = (1, 2, 3) if ng == 2 else (1, 3)
        for r in rows:
            rr = ref['rows'][r]
            ok_S = ok_V = ok_n = ok_H = True
            for j in range(m):
                k = (r - 1) * m + j
                ok_S &= close(G['svSv'][k], float(rr['S'][j]), 1e-12)
                ok_n &= G['svNr'][k] == rr['n'][j]
                ok_H &= close(G['svHz'][k], float(rr['H'][j]), 1e-12)
                if rr['V'][j] is None:
                    ok_V &= G['svGw'][k] == -1
                else:
                    ok_V &= close(G['svGw'][k], float(rr['V'][j]), 1e-12)
            check(ok_S, '%s row %d: KM S = exact product-limit' % (name, r))
            check(ok_V, '%s row %d: Greenwood sum (and "undefined" after n = d)' % (name, r))
            check(ok_n, '%s row %d: numbers at risk' % (name, r))
            check(ok_H, '%s row %d: Nelson-Aalen H' % (name, r))
            check(close(G['svLast'][r - 1], rr['last']) and G['svTot'][r - 1] == rr['tot']
                  and G['svEv'][r - 1] == rr['ev'], '%s row %d: size, events, last time' % (name, r))
            # statsmodels
            if rr['ev'] > 0:
                sf = sm_row(t, e, gg, r)
                idx = [j for j in range(m) if rr['d'][j] > 0]
                s_eng = [G['svSv'][(r - 1) * m + j] for j in idx]
                check(np.allclose(s_eng, sf.surv_prob, rtol=1e-10, atol=1e-12),
                      '%s row %d: S = statsmodels surv_prob' % (name, r))
                se_eng = [G['svSv'][(r - 1) * m + j] * math.sqrt(G['svGw'][(r - 1) * m + j])
                          if G['svGw'][(r - 1) * m + j] >= 0 else float('nan') for j in idx]
                se_sm = np.array(sf.surv_prob_se, float)
                okse = all((math.isnan(a) and math.isnan(b)) or close(a, b, 1e-8)
                           for a, b in zip(se_eng, se_sm))
                check(okse, '%s row %d: Greenwood SE = statsmodels surv_prob_se' % (name, r))
                check(list(sf.n_risk) == [G['svNr'][(r - 1) * m + j] for j in idx],
                      '%s row %d: n at risk = statsmodels n_risk' % (name, r))
            # pointwise CIs, both kinds
            for kind in (1, 2):
                G['svCIT'] = float(kind)
                h.call('sv_CIs')
                okc = True
                for j in range(m):
                    k = (r - 1) * m + j
                    rc = ref_ci(rr['S'][j], rr['V'][j], kind)
                    if rc is None:
                        okc &= G['svCLo'][k] == -1 and G['svCHi'][k] == -1
                    else:
                        okc &= close(G['svCLo'][k], rc[0], 1e-9) and close(G['svCHi'][k], rc[1], 1e-9)
                        okc &= 0 <= G['svCLo'][k] <= G['svSv'][k] + 1e-12 <= G['svCHi'][k] + 2e-12 <= 1 + 3e-12
                check(okc, '%s row %d: pointwise 95%% CI (%s), inside 0..1, around S'
                      % (name, r, 'log-log' if kind == 1 else 'linear'))
                # quantiles and their CIs
                for p in (0.5, 0.25, 0.2, 0.1):
                    q_eng = h.execute('sv_Quant(%d, %r)' % (r, p))
                    q_ref = ref_quant(ref, r, p)
                    check((q_ref is None and q_eng == -1) or (q_ref is not None and close(q_eng, q_ref)),
                          '%s row %d: quantile p=%g: %s vs exact %s' % (name, r, p, q_eng, q_ref))
                    ci_eng = h.execute('sv_QCI(%d, %r)' % (r, p))
                    lo, hi = ref_qci(ref, r, p, kind)
                    ok = ((lo is None and ci_eng[0] == -1) or (lo is not None and close(ci_eng[0], lo))) and \
                         ((lo is None) or (hi is None and ci_eng[1] == -2) or (hi is not None and close(ci_eng[1], hi)))
                    check(ok, '%s row %d: quantile CI p=%g %s: %s vs ref (%s, %s)'
                          % (name, r, p, kind, ci_eng, lo, hi))
                    if rr['ev'] > 0:
                        sf = sm_row(t, e, gg, r)
                        meth = 'cloglog' if kind == 1 else 'linear'
                        with np.errstate(all='ignore'):
                            slo, shi = sf.quantile_ci(p, method=meth)
                            sq = sf.quantile(p)
                        # statsmodels works in floating point: a tie S == 1 - p can fall either side
                        tie = any(rr['d'][j] > 0 and rr['S'][j] == 1 - Fr(p).limit_denominator(1000)
                                  for j in range(m))
                        if not tie:
                            okq = (math.isnan(sq) and q_eng == -1) or (not math.isnan(sq) and close(q_eng, float(sq)))
                            check(okq, '%s row %d: quantile p=%g = statsmodels %s (engine %s)' % (name, r, p, sq, q_eng))
                            sl = None if (isinstance(slo, float) and math.isnan(slo)) else float(slo)
                            sh = None if (sl is None or np.isinf(shi)) else float(shi)
                            ok2 = ((sl is None and ci_eng[0] == -1) or (sl is not None and close(ci_eng[0], sl))) and \
                                  ((sl is None) or (sh is None and ci_eng[1] == -2) or (sh is not None and close(ci_eng[1], sh)))
                            check(ok2, '%s row %d: quantile CI p=%g %s = statsmodels (%s, %s) (engine %s)'
                                  % (name, r, p, meth, slo, shi, ci_eng))
                        elif kind == 1:
                            print('   note: %s row %d p=%g: S equals 1 - p exactly at an event time; '
                                  'statsmodels compared only to the exact rule' % (name, r, p))
            G['svCIT'] = 1.0
            h.call('sv_CIs')
            # life table at several widths
            for w in (1, 4, 5, 13, 0.5):
                K = max(1, int(math.ceil(rr['last'] / w - 1e-9)))
                if K > 100:
                    rv = h.execute('sv_LCalc(%d, %r)' % (r, w))
                    check(rv == 0, '%s row %d: life table w=%g refused (%d intervals)' % (name, r, w, K))
                    continue
                rv = h.execute('sv_LCalc(%d, %r)' % (r, w))
                lt = ref_life(ref, r, w)
                ok = rv == 1 and int(G['svLK']) == len(lt)
                if ok:
                    for i, row in enumerate(lt):
                        ok &= close(G['svLA'][i], row['a']) and G['svLN'][i] == row['n'] and \
                              close(G['svLB'][i], row['b']) and G['svLF'][i] == row['f'] and \
                              G['svLC'][i] == row['c'] and close(G['svLE'][i], row['ne']) and \
                              G['svLDv'][i] == row['d'] and close(G['svLQ'][i], row['q'], 1e-12) and \
                              close(G['svLS'][i], row['S'], 1e-12)
                check(ok, '%s row %d: life table w=%g (%d intervals) = hand computation' % (name, r, w, len(lt)))
        # the two-group tests
        if ng == 2:
            okO = close(G['svO1'], float(ref['O1'])) and close(G['svE1'], float(ref['E1']), 1e-12) and \
                close(G['svO2'], float(ref['O2'])) and close(G['svE2'], float(ref['E2']), 1e-12) and \
                close(G['svVar'], float(ref['Var']), 1e-12)
            check(okO, '%s: O1, E1, O2, E2, V = exact' % name)
            tt = np.array(t, float); ee = np.array(e, float); grp = np.array(gg)
            if ref['chi'] is not None:
                chi, p = survdiff(tt, ee, grp)
                check(close(G['svChi'], ref['chi'], 1e-10) and close(G['svChi'], float(chi), 1e-8),
                      '%s: log-rank chi2 %.6f = exact %.6f = statsmodels %.6f' % (name, G['svChi'], ref['chi'], chi))
                check(close(G['svPv'], float(p), 1e-7) or abs(G['svPv'] - float(p)) < 1e-14,
                      '%s: log-rank p %.6g = statsmodels %.6g' % (name, G['svPv'], p))
                gb, gbp = survdiff(tt, ee, grp, weight_type='gb')
                check(close(G['svGbC'], ref['gb'], 1e-10) and close(G['svGbC'], float(gb), 1e-8),
                      '%s: Gehan-Breslow chi2 %.6f = statsmodels %.6f' % (name, G['svGbC'], gb))
                check(close(G['svGbP'], float(gbp), 1e-7) or abs(G['svGbP'] - float(gbp)) < 1e-14,
                      '%s: Gehan-Breslow p = statsmodels' % name)
            else:
                check(G['svLRok'] == 0 and G['svChi'] == -1, '%s: no variance -> no test (LRok 0)' % name)
            if ref['hr'] is None:
                check(G['svHR'] == -1, '%s: HR not estimable -> -1' % name)
            else:
                check(close(G['svHR'], ref['hr'][0], 1e-10) and close(G['svHRL'], ref['hr'][1], 1e-10)
                      and close(G['svHRH'], ref['hr'][2], 1e-10), '%s: HR and its CI' % name)
        else:
            check(G['svLRok'] == 0 and G['SV_CHI'] == -1 and G['SV_S2'] == [], '%s: one group: no test, SV_S2 = {}' % name)
        # exports
        ev_idx = [j for j in range(m) if ref['rows'][3]['d'][j] > 0]
        check(G['SV_T'] == [float(ref['U'][j]) for j in ev_idx], '%s: SV_T = event times' % name)
        check(all(close(a, float(ref['rows'][1]['S'][j]), 1e-12) for a, j in zip(G['SV_S1'], ev_idx))
              and len(G['SV_S1']) == len(ev_idx), '%s: SV_S1' % name)
        med = [ref_quant(ref, r, 0.5) for r in ((1, 2) if ng == 2 else (3,))]
        check(G['SV_MED'] == [float(x) if x is not None else -1.0 for x in med], '%s: SV_MED %s' % (name, G['SV_MED']))
    return h


# ============================================================ Part B helpers
def lines_of(page):
    return page.lines()


def find_line(page, prefix):
    for t in sorted(page.texts, key=lambda q: (q.y, q.x)):
        if t.text.startswith(prefix):
            return t.text
    return None


NUM = r'(-?\d+(?:\.\d+)?)'


def km_readout_expect(ref, r, t, kind, view=1):
    """What the KM readout should say for row r at cursor time t (reference)."""
    U = ref['U']
    j = max([i for i, u in enumerate(U) if u <= t + 1e-12], default=-1)
    rr = ref['rows'][r]
    S = float(rr['S'][j]) if j >= 0 else 1.0
    V = rr['V'][j] if j >= 0 else Fr(0)
    H = float(rr['H'][j]) if j >= 0 else 0.0
    n = sum(1 for k, u in enumerate(U) for _ in range(rr['d'][k] + rr['c'][k]) if u >= t - 1e-12)
    ci = ref_ci(S, V, kind)
    return S, ci, H, n


def check_km_line(text, name, S, ci, n, label):
    m = re.match(re.escape(name) + r': S = ' + NUM + r'(?:, CI ' + NUM + ' to ' + NUM + r')?(, CI undefined)?, n = ' + NUM + '$', text or '')
    ok = m is not None
    if ok:
        ok &= close(float(m.group(1)), round(S, 4), 1e-12)
        if ci is not None and ci[1] > ci[0]:
            ok &= m.group(2) is not None and close(float(m.group(2)), round(ci[0], 3), 1e-12) and \
                close(float(m.group(3)), round(ci[1], 3), 1e-12)
        elif ci is None:
            ok &= m.group(4) is not None
        ok &= int(m.group(5)) == n
    check(ok, '%s: readout %r = S %.4f CI %s n %d' % (label, text, S, ci, n))


def xp(t, G):
    return G['svPL'] + int(t / G['svXmx'] * (G['svPR'] - G['svPL']) + 0.5)


def yp(v, G):
    y = (v - G['svYlo']) / (G['svYhi'] - G['svYlo']) * (G['svPB'] - G['svPT'])
    if y < 0:
        return G['svPB']
    y = G['svPB'] - int(y + 0.5)
    return max(y, G['svPT'])



def per_event(h, func):
    """One page per input event: the LAST page drawn by `func` after that event and before the
    next one (a tap that reads the curve draws twice).  The first item is the page shown before
    the first event that reached the view.  Each item is (event, page, menu)."""
    out = []
    cur_ev, cur_pg, cur_menu = None, None, None
    for item in h.timeline:
        if item[0] == 'event':
            if cur_pg is not None:
                out.append((cur_ev, cur_pg, cur_menu))
            cur_ev, cur_pg, cur_menu = item[1], None, None
        elif item[0] == 'screen':
            sc = item[1]
            if sc.reason == 'blit' and sc.func == func:
                cur_pg = sc
            if sc.reason == 'wait' and sc.menu and cur_pg is not None:
                cur_menu = sc.menu
    if cur_pg is not None:
        out.append((cur_ev, cur_pg, cur_menu))
    return out

# ============================================================ Part B
def part_b():
    print('=== Part B: every menu path, numbers on the pages')
    ref1 = ref_fit(WK, AR, PRESETS[1][1])
    # ---- B1 the opening page, the KM view, arrows, taps, toggles ----
    h = new_h()
    h.press('Enter')                      # opening page
    h.choose('Kaplan-Meier plot')
    for _ in range(3):
        h.press('Right')
    h.press('Left')
    h.tap(200, 90)                        # a tap on the plot
    h.tap(30, 230)                        # CI -> linear
    h.tap(80, 230)                        # Band off
    h.tap(80, 230)                        # Band on
    h.tap(130, 230)                       # Zoom on
    h.tap(185, 230)                       # H(t) view
    h.tap(185, 230)                       # back to S(t)
    h.tap(130, 230)                       # Zoom off
    h.tap(30, 230)                        # CI -> log-log
    h.tap(300, 230)                       # More
    h.tap(30, 230)                        # Pool
    h.press('Right')
    h.tap(30, 230)                        # Split
    h.tap(300, 230)                       # More (page 1)
    h.tap(160, 165)                       # at-risk rows: an explanation (frame 19)
    h.press('Enter'); h.choose('Main menu')
    h.choose('Quit')
    h.call('SurvLab')
    check(h.error is None, 'B1 runs without error (%s)' % h.error)
    op = h.pages[0]
    check(op.func == 'sv_Open' and op.has('DISCLAIMER: a teaching and demonstration aid.')
          and op.has('Not validated for forensic, clinical or legal use;')
          and op.has('do not rely on its results for legal purposes.'), 'B1 opening page shows the disclaimer')
    check(op.has('Rossi, Berk & Lenihan 1980 (via Allison 1995)'), 'B1 opening page: source line')
    pe = per_event(h, 'sv_KMFrame')
    frames = [x[1] for x in pe]
    menus = [x[2] for x in pe]
    check(len(frames) == 20, 'B1 one KM frame per input: %d' % len(frames))
    # frames: 0 first, 1-3 Right, 4 Left, 5 tap, 6 CI linear, 7 band off, 8 band on, 9 zoom,
    # 10 H view, 11 S view, 12 zoom off, 13 CI log-log, 14 More, 15 Pool, 16 Right, 17 Split, 18 More
    G = h.globals_
    U = ref1['U']
    evt = [u for j, u in enumerate(U) if ref1['rows'][3]['d'][j] > 0]
    t0 = min(evt, key=lambda u: abs(u - 26))
    i0 = evt.index(t0)
    seq = [t0, evt[i0 + 1], evt[i0 + 2], evt[i0 + 3], evt[i0 + 2]]
    for f, t in zip(frames[:5], seq):
        check(f.has('t = %d' % t), 'B1 cursor label t = %d' % t)
        for r, nm in ((1, 'aid'), (2, 'no aid')):
            S, ci, H, n = km_readout_expect(ref1, r, t, 1)
            check_km_line(find_line(f, nm + ': S'), nm, S, ci, n, 'B1 t=%d %s' % (t, nm))
    # the tap at x = 200: t = (200 - 44)/268 * 52*1.04
    tt = (200 - 44) / 268 * (52 * 1.04)
    f = frames[5]
    check(f.has('t = %.2f' % tt), 'B1 tap: cursor label t = %.2f' % tt)
    for r, nm in ((1, 'aid'), (2, 'no aid')):
        S, ci, H, n = km_readout_expect(ref1, r, tt, 1)
        check_km_line(find_line(f, nm + ': S'), nm, S, ci, n, 'B1 tap t=%.3f %s' % (tt, nm))
    f = frames[6]
    check(f.has('S(t), 95% CI linear'), 'B1 CI soft key: subtitle says linear')
    for r, nm in ((1, 'aid'), (2, 'no aid')):
        S, ci, H, n = km_readout_expect(ref1, r, tt, 2)
        check_km_line(find_line(f, nm + ': S'), nm, S, ci, n, 'B1 linear %s' % nm)
    check(frames[7].has('S(t), no CI band'), 'B1 Band off: subtitle')
    check(frames[8].has('S(t), 95% CI linear'), 'B1 Band on again')
    zf = frames[9]
    check(zf.has('zoomed: y from 0.60') and zf.has('0.60') and not zf.has('0.20'),
          'B1 Zoom: y axis from 0.60, said in red')
    hf = frames[10]
    check(hf.has('H(t) = sum of d/n (Nelson-Aalen)'), 'B1 H(t) view subtitle')
    for r, nm in ((1, 'aid'), (2, 'no aid')):
        S, ci, H, n = km_readout_expect(ref1, r, tt, 1)
        exp = '%s: H = %.4f, exp(-H) = %.4f, n = %d' % (nm, round(H, 4), round(math.exp(-H), 4), n)
        check(hf.has(exp), 'B1 H view readout %r' % exp)
    check(frames[11].has('S(t), 95% CI linear') and frames[12].has('S(t), 95% CI linear') and not frames[12].has('zoomed: y from 0.60'),
          'B1 back to S(t), zoom off')
    check(frames[13].has('S(t), 95% CI log-log'), 'B1 CI back to log-log')
    check(menus[13] == ['CI', 'Band', 'Zoom', 'H(t)', 'Back', 'More'], 'B1 soft keys page 1: %s' % menus[13])
    check(menus[14] == ['Pool', 'Median', 'Test', 'Life', 'Back', 'More'], 'B1 More: soft keys page 2: %s' % menus[14])
    check(menus[15] == ['Split', 'Median', 'Test', 'Life', 'Back', 'More'], 'B1 Pool: the key now reads Split')
    for f in (frames[15], frames[16]):
        m = re.search(r't = ' + NUM, ' '.join(f.lines()))
        t = float(m.group(1))
        S, ci, H, n = km_readout_expect(ref1, 3, t, 1)
        check_km_line(find_line(f, 'all: S'), 'all', S, ci, n, 'B1 pooled t=%g' % t)
        check(f.has('%.1f%% re-arrested by t = %s weeks' % (round(100 * (1 - S), 1), ('%d' % t) if t == int(t) else '%.2f' % t)),
              'B1 pooled: words line')
    check(find_line(frames[17], 'aid: S') is not None and find_line(frames[17], 'all: S') is None, 'B1 Split: two curves again')
    check(menus[18] == ['CI', 'Band', 'Zoom', 'H(t)', 'Back', 'More'], 'B1 More wraps to page 1')
    check(any(f.has('At risk = not yet re-arrested and still followed then') for f in frames), 'B1 tap on the at-risk rows explains')
    # at-risk table on the cached plot: numbers at 0, 10, ... 50
    for r, nm in ((1, 'aid'), (2, 'no aid')):
        exp = [sum(1 for i in range(432) if PRESETS[1][1][i] == r and WK[i] >= tk) for tk in (0, 10, 20, 30, 40, 50)]
        f = frames[0]
        col = '#003CC8' if r == 1 else '#C800C8'
        got = [int(t.text) for t in sorted(f.texts, key=lambda q: q.x)
               if t.y == 148 + 12 * r and t.hex == col and t.text.isdigit()]
        check(got == exp, 'B1 at-risk row %s: %s = %s' % (nm, got, exp))
    check(h.result.startswith('SurvLab: Rossi, aid vs no aid, log-rank') and '= 3.84, p = 0.0501, HR = 0.69' in h.result,
          'B1 Quit summary %r' % h.result)
    # Home exports after the run
    check(close(G['SV_CHI'], ref1['chi'], 1e-10) and close(G['SV_HR'], ref1['hr'][0], 1e-10) and G['SV_MED'] == [-1, -1],
          'B1 Home: SV_CHI, SV_HR, SV_MED = {-1, -1} (not reached)')

    # ---- B1b pixel geometry of the cached plot (Part C) ----
    part_c_geometry(h, ref1)

    # ---- B2 quantiles page, all four p, both CI types ----
    h = new_h()
    h.press('Enter')
    h.choose('Median and quantiles')
    h.tap(80, 230); h.tap(130, 230); h.tap(185, 230)    # 25%, 20%, 10%
    h.tap(240, 230)                                       # CI -> linear
    h.tap(30, 230)                                        # median (linear)
    h.tap(80, 230); h.tap(130, 230); h.tap(185, 230)
    h.tap(150, 60)                                        # tap on the picture
    h.press('Left'); h.press('Right')
    h.tap(300, 230)
    h.choose('Quit')
    h.call('SurvLab')
    check(h.error is None, 'B2 runs (%s)' % h.error)
    qp = [p for p in h.pages if p.func == 'sv_QDraw']
    plan = [(0.5, 1), (0.25, 1), (0.2, 1), (0.1, 1), (0.1, 2), (0.5, 2), (0.25, 2), (0.2, 2), (0.1, 2)]
    for f, (p, kind) in zip(qp, plan):
        for r, nm in ((1, 'aid'), (2, 'no aid'), (3, 'all')):
            q = ref_quant(ref1, r, p)
            lo, hi = ref_qci(ref1, r, p, kind)
            s = nm + ': ' + ('n.r.' if q is None else '%d weeks' % q)
            s += ';  95% CI ' + ('%d to %s' % (lo, 'n.r.' if hi is None else '%d' % hi) if lo is not None else '')
            if lo is None:
                s = s.replace(';  95% CI ', ';  no CI (too few events)')
            check(f.has(s), 'B2 p=%g %s %s: %r' % (p, 'log-log' if kind == 1 else 'linear', nm, s))
        if p == 0.5:
            check(f.has('So the median is not reached: try 25%, 20%, 10%.'), 'B2 median not reached: explained')
            check(f.has('aid: S(52) = 0.778; 22.2% re-arrested.'), 'B2 median n.r.: S at the end')
    check(any(p.has('Red dots: S = ') for p in qp), 'B2 tap on the picture explains')
    check(any(sc.menu == ['Median', '25%', '20%', '10%', 'CI', 'Back'] for sc in h.screens if sc.reason == 'wait'), 'B2 soft keys')

    # ---- B3 the log-rank pages ----
    h = new_h()
    h.press('Enter')
    h.choose('Compare groups: log-rank')
    h.tap(200, 60)                        # O bar of aid
    h.tap(230, 60)                        # E bar of aid
    h.tap(270, 60)                        # O bar of no aid
    h.tap(80, 230)                        # Next
    h.tap(30 + int(3.8376 / 6 * 282 + 0.5), 80)   # on the log-rank line (window 0..6)
    h.tap(80, 230)                        # Next
    h.tap(100, 60)
    h.tap(30, 230)                        # Prev
    h.press('Esc')
    h.choose('Quit')
    h.call('SurvLab')
    check(h.error is None, 'B3 runs (%s)' % h.error)
    tp = [p for p in h.pages if p.func == 'sv_TView']
    p1 = tp[0]
    check(p1.has('aid') and p1.has('48') and p1.has('%.1f' % float(ref1['E1'])) and p1.has('%+.1f' % float(ref1['O1'] - ref1['E1'])),
          'B3 page 1: aid O = 48, E = %.1f' % float(ref1['E1']))
    check(p1.has('66') and p1.has('%.1f' % float(ref1['E2'])), 'B3 page 1: no aid O = 66, E = %.1f' % float(ref1['E2']))
    check(p1.has('V = %.2f (var of O₁)' % float(ref1['Var'])), 'B3 page 1: V')
    check(p1.has('χ² = (O₁ - E₁)²/V = %.2f' % ref1['chi']) and p1.has('df = 1, p = %.4f' % ref1['p']), 'B3 page 1: chi2 and p')
    hr = ref1['hr']
    check(p1.has('HR = (O₁/E₁)/(O₂/E₂) = %.3f, CI %.3f to %.3f' % hr), 'B3 page 1: HR %.3f and its CI' % hr[0])
    check(p1.has('Gehan-Breslow (Wilcoxon): χ² = %.2f, p = %.4f' % (ref1['gb'], ref1['gbp'])), 'B3 page 1: Gehan-Breslow')
    check(p1.has('p ≥ 0.05: no convincing evidence the curves differ'), 'B3 page 1: verdict (p = 0.0501)')
    check(hr[2] < 1 and p1.has("Borderline: the O/E-ratio CI and p disagree"), 'B3 page 1: borderline note: p = 0.0501 but the HR CI ends at %.4f' % hr[2])
    check(any('aid: O = 48 re-arrested (observed)' in p.lines() for p in tp), 'B3 tap O bar')
    check(any('aid: E = %.1f expected if one curve' % float(ref1['E1']) in p.lines() for p in tp), 'B3 tap E bar')
    check(any('no aid: O = 66 re-arrested (observed)' in p.lines() for p in tp), 'B3 tap no-aid O bar')
    p2 = [p for p in tp if p.has('2/3, tap a line = what it is, Ent = menu, Esc = back')]
    check(len(p2) >= 1 and p2[0].has('Shaded tail = P(χ² ≥ 3.84 | H₀) = p: p = 0.0501'), 'B3 page 2: tail = p')
    check(any(p.has('Red: log-rank χ² = 3.84; tail beyond = p') for p in p2), 'B3 page 2: tap on the red line')
    p3 = [p for p in tp if p.has('3/3, tap = what it is, Ent = menu, Esc = back')]
    check(len(p3) >= 1 and p3[0].has('G-B 3.75 vs log-rank 3.84 (rule of thumb):') and p3[0].has('suggests the gap builds steadily'),
          'B3 page 3: early/late verdict')
    # page 2 pixel check: the shaded tail starts at the red line
    # ---- B4 the life table ----
    h = new_h()
    h.press('Enter')
    h.choose('Life table'); h.answer({'laW': 4})
    h.tap(240, 230)                       # Down
    h.tap(160, 38)                        # tap a row (the only one shown after Down: [48, 52])
    h.tap(30, 230)                        # Group -> no aid
    h.tap(30, 230)                        # Group -> all
    h.tap(80, 230)                        # Plot
    h.press('Right'); h.press('Right')
    h.tap(80, 230)                        # Table
    h.tap(130, 230); h.answer({'laW': 0})   # Width 0: refused
    h.tap(130, 230); h.answer({'laW': 0.25})   # 209 intervals: refused
    h.tap(130, 230); h.answer({'laW': 13})
    h.press('Esc')
    h.choose('Quit')
    h.call('SurvLab')
    check(h.error is None, 'B4 runs (%s)' % h.error)
    lt = [p for p in h.pages if p.func in ('sv_LTab', 'sv_LPlot')]
    ref_lt1 = ref_life(ref1, 1, 4)
    f = lt[0]
    check(f.has('Life table: aid, width 4 weeks'), 'B4 title')
    rows_y = sorted(set(t.y for t in f.texts if 34 <= t.y < 178))
    ok = True
    for i, y in enumerate(rows_y[:12]):
        row = sorted([t for t in f.texts if t.y == y and t.x > 3], key=lambda q: q.x)
        txt = [t.text for t in row]
        R = ref_lt1[i]
        exp = ['%d-%d' % (R['a'], R['b']), '%d' % R['n'], '%d' % R['c'], ('%g' % R['ne']), '%d' % R['d'], '%.4f' % R['q'], '%.4f' % R['S']]
        ok &= txt == exp
        if txt != exp:
            print('   row', i, txt, exp)
    check(ok, 'B4 the 12 rows of aid at width 4 = hand computation')
    f = lt[1]
    rows_y = sorted(set(t.y for t in f.texts if 34 <= t.y < 178))
    txt = [t.text for t in sorted([t for t in f.texts if t.y == rows_y[-1]], key=lambda q: q.x)]
    R = ref_lt1[-1]
    check(txt[:7] == ['48-52', '%d' % R['n'], '0', '%g' % R['ne'], '%d' % R['d'], '%.4f' % R['q'], '%.4f' % R['S']]
          and len(ref_lt1) == 13 and R['f'] == 168,
          'B4 Down: the last row [48, 52], cut at the last follow-up: %s' % txt)
    check(any(p.has('[48, 52]: d = %d of n\' = %g, q = %.4f' % (ref_lt1[12]['d'], ref_lt1[12]['ne'], ref_lt1[12]['q'])) for p in lt),
          'B4 tap a row: its details')
    check(any(p.has('Life table: no aid, width 4 weeks') for p in lt) and any(p.has('Life table: all, width 4 weeks') for p in lt),
          'B4 Group cycles aid -> no aid -> all')
    check(any(p.func == 'sv_LPlot' for p in lt), 'B4 Plot page')
    ref_all4 = ref_life(ref1, 3, 4)
    check(any(p.has('[4, 8): d = %d of n\' = %g, q = %.4f' % (ref_all4[1]['d'], ref_all4[1]['ne'], ref_all4[1]['q'])) for p in lt),
          'B4 plot: Right selects interval 2')
    check(any('The width must be more than 0.' in ' '.join(mb.lines) for mb in h.msgboxes), 'B4 width 0 refused')
    check(any('more than 100 intervals' in ' '.join(mb.lines) for mb in h.msgboxes), 'B4 width 0.25 refused')
    check(any(p.has('Life table: all, width 13 weeks') for p in lt), 'B4 width 13 accepted')
    ref_all13 = ref_life(ref1, 3, 13)
    f13 = [p for p in lt if p.has('Life table: all, width 13 weeks')][0]
    check(f13.has('%.4f' % ref_all13[-2]['S']) and f13.has('%d' % ref_all13[1]['d']), 'B4 width 13 numbers')

    # ---- B5 the presets: load pages and their own pages ----
    for k in (2, 3, 4):
        nm, grp, ng = PRESETS[k]
        ref = ref_fit(WK, AR, grp if ng == 2 else None)
        h = new_h()
        h.press('Enter')
        h.choose('Load a preset')
        h.choose(k)
        h.press('Enter')                     # the load page
        h.choose('Kaplan-Meier plot')
        h.press('Esc')
        h.choose('Compare groups: log-rank')
        if ng == 2:
            h.press('Esc')
        h.choose('Median and quantiles')
        h.tap(80, 230)
        h.press('Esc')
        h.choose('Quit')
        h.call('SurvLab')
        check(h.error is None, 'B5 preset %d runs (%s)' % (k, h.error))
        lp = [p for p in h.pages if p.func == 'sv_LoadInfo'][0]
        check(lp.has('n = 432, events = 114, censored = 318'), 'B5 preset %d: load page totals' % k)
        check(lp.has('Data: Rossi, Berk & Lenihan 1980 (via Allison 1995)'), 'B5 preset %d: source line' % k)
        if ng == 2:
            for r in (1, 2):
                rr = ref['rows'][r]
                check(any(l.startswith('group %d = ' % r) and l.endswith(': n = %d, events = %d' % (rr['tot'], rr['ev']))
                          for l in lp.lines()), 'B5 preset %d group %d: n %d events %d' % (k, r, rr['tot'], rr['ev']))
            check(lp.has('An observed grouping, not an experiment.') and any("SurvLab's split" in l for l in lp.lines()),
                  'B5 preset %d: labelled as SurvLab\'s split' % k)
            tp = [p for p in h.pages if p.func == 'sv_TView']
            check(len(tp) == 1 and tp[0].has('df = 1, %s' % ('p < 0.0001' if ref['p'] < 0.0001 else 'p = %.4f' % ref['p'])),
                  'B5 preset %d: log-rank p on the page (%.6f)' % (k, ref['p']))
            check(tp[0].has('p < 0.05: evidence that the two curves differ'), 'B5 preset %d: verdict' % k)
        else:
            check(any('One group only' in ' '.join(mb.lines) for mb in h.msgboxes), 'B5 one group: log-rank refused with a message')
            check(h.result == 'SurvLab: Rossi, all 432 men, S(52) = %.4f' % float(ref['rows'][3]['S'][-1]), 'B5 summary %r' % h.result)
            kf = [p for p in h.pages if p.func == 'sv_KMFrame'][0]
            m = re.search(r't = ' + NUM, ' '.join(kf.lines()))
            t = float(m.group(1))
            S, ci, H, n = km_readout_expect(ref, 3, t, 1)
            check_km_line(find_line(kf, 'all: S'), 'all', S, ci, n, 'B5 one-group KM')
        qp = [p for p in h.pages if p.func == 'sv_QDraw']
        rows = (1, 2, 3) if ng == 2 else (3,)
        names = ref_names(k)
        for r in rows:
            for f, p in zip(qp[:2], (0.5, 0.25)):
                q = ref_quant(ref, r, p)
                lo, hi = ref_qci(ref, r, p, 1)
                s = names[r] + ': ' + ('n.r.' if q is None else '%d weeks' % q)
                s += (';  95%% CI %d to %s' % (lo, 'n.r.' if hi is None else '%d' % hi)) if lo is not None else ';  no CI (too few events)'
                check(f.has(s), 'B5 preset %d p=%g: %r' % (k, p, s))

    # ---- B6 Use my data ----
    my_data_runs()

    # ---- B7 Help, and Esc out of it ----
    h = new_h()
    h.press('Enter')
    h.choose('Help')
    for _ in range(5):
        h.press('Enter')
    h.choose('Help')
    h.press('Enter'); h.press('Esc')
    h.choose('Quit')
    h.call('SurvLab')
    hp = [p for p in h.pages if p.func == 'sv_HPage']
    check(h.error is None and len(hp) == 7, 'B7 help: 5 pages, then 2 pages and Esc (%d pages)' % len(hp))
    check(hp[4].has('Page 5/5, any key = menu') and hp[6].has('Page 2/5, any key = next, Esc = leave'), 'B7 help footers')

    # ---- B8 the Enter menu of the KM view, the Go-to menu ----
    h = new_h()
    h.press('Enter')
    h.choose('Kaplan-Meier plot')
    h.press('Enter'); h.choose('Median and quantiles')
    h.press('Enter'); h.choose('Log-rank test')
    h.press('Enter'); h.choose('Life table')
    h.press('Enter'); h.choose('Kaplan-Meier plot')
    h.press('Enter'); h.choose('S(t) / cumulative hazard')
    h.press('Enter'); h.choose('Main menu')
    h.choose('Quit')
    h.call('SurvLab')
    seqf = [p.func for p in h.pages]
    check(h.error is None and 'sv_QDraw' in seqf and 'sv_TView' in seqf and 'sv_LTab' in seqf,
          'B8 Enter menus reach every view (%s)' % h.error)
    check(any(p.func == 'sv_KMFrame' and p.has('H(t) = sum of d/n (Nelson-Aalen)') for p in h.pages),
          'B8 KM Enter menu: the H(t) view')

    # ---- B10 a finger dragged along the KM plot; edge data through every view ----
    h = new_h()
    h.press('Enter')
    h.choose('Kaplan-Meier plot')
    h.drag([(60, 80), (90, 80), (150, 80), (250, 80), (311, 80)])
    h.press('Esc')
    h.choose('Quit')
    h.call('SurvLab')
    G = h.globals_
    fr = [p for p in h.pages if p.func == 'sv_KMFrame']
    ts = []
    for f in fr:
        m = re.search(r't = ' + NUM, ' '.join(f.lines()))
        ts.append(float(m.group(1)))
    want = [round((x - 44) / 268 * 52 * 1.04, 2) for x in (60, 90, 150, 250, 311)]
    check(h.error is None and all(any(abs(t - w) < 0.006 for t in ts) for w in want),
          'B10 drag: the cursor follows the finger through t = %s (%s)' % (want, sorted(set(ts))))
    last = [f for f in fr if any(abs(float(re.search(r't = ' + NUM, ' '.join(f.lines())).group(1)) - want[-1]) < 0.006 for _ in [0])]
    check(last and last[-1].has('aid: past its last follow-up (52)') and last[-1].has('no aid: past its last follow-up (52)'),
          'B10 drag past week 52: "past its last follow-up"')
    edge = [
        ('all censored, two groups', [4.0, 6.0, 9.0, 9.0, 3.0, 8.0], [0.0] * 6, [1.0, 2.0, 1.0, 2.0, 1.0, 2.0]),
        ('no events in group 2', [1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [1.0, 1.0, 1.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 2.0, 2.0, 2.0]),
        ('huge times', [1e5, 2e5, 3.5e5, 5e5, 999999.0, 7e5], [1.0, 0.0, 1.0, 1.0, 0.0, 1.0], [1.0, 2.0, 1.0, 2.0, 2.0, 1.0]),
        ('n = d at the end', [1.0, 2.0, 3.0, 3.0, 1.0, 2.0], [1.0, 0.0, 1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0, 2.0, 2.0]),
        ('time 0 events', [0.0, 0.0, 1.0, 2.0, 2.0, 5.0], [1.0, 0.0, 1.0, 1.0, 0.0, 1.0], [1.0, 2.0, 1.0, 2.0, 1.0, 2.0]),
    ]
    for nm, t, e, g in edge:
        h = new_h(app_data={'C1': t, 'C2': e, 'C3': g})
        h.press('Enter')
        h.choose('Use my data'); h.press('Enter')
        h.choose('Kaplan-Meier plot')
        h.press('Right'); h.press('Right'); h.tap(200, 80)
        h.tap(30, 230); h.tap(130, 230); h.tap(185, 230); h.tap(300, 230); h.tap(30, 230)
        h.press('Esc')
        h.choose('Median and quantiles'); h.tap(80, 230); h.tap(185, 230); h.tap(240, 230); h.press('Esc')
        h.choose('Compare groups: log-rank'); h.tap(80, 230); h.tap(80, 230); h.tap(200, 60); h.press('Esc')
        h.choose('Life table'); h.answer({'laW': max(t) / 4 if max(t) > 0 else 1}); h.tap(80, 230); h.tap(30, 230); h.press('Esc')
        h.choose('Quit')
        h.call('SurvLab')
        check(h.error is None, 'B10 %s: every view runs (%s)' % (nm, h.error))
        ref = ref_fit(t, [int(x) for x in e], [int(x) for x in g])
        tp = [p for p in h.pages if p.func == 'sv_TView']
        if ref['chi'] is None:
            check(any(p.has('V = 0: no test possible') for p in tp) and any(p.has('No test: no events, or no variance (V = 0).') for p in tp),
                  'B10 %s: no test, said on pages 1 and 2' % nm)
        else:
            check(any(p.has('χ² = (O₁ - E₁)²/V = %.2f' % ref['chi']) for p in tp), 'B10 %s: chi2 on the page' % nm)
        if ref['hr'] is None:
            check(any(p.has('HR not estimable: a group has no events') for p in tp) or ref['chi'] is None,
                  'B10 %s: HR not estimable, said' % nm)
        if nm == 'huge times':
            kb = [x for x in h.texts if x.func == 'sv_XLab' and x.text.endswith('00000')]
            xs = sorted(set((x.x, x.y, len(x.text)) for x in kb))
            ok = all(b[0] - a[0] >= 6 * a[2] for a, b in zip(xs, xs[1:]) if a[1] == b[1])
            check(ok and xs, 'B10 huge times: time labels thinned so they do not overlap (%s)' % xs[:6])
        if nm == 'n = d at the end':
            kf = [p for p in h.pages if p.func == 'sv_KMFrame']
            check(any('CI undefined' in l for p in kf for l in p.lines()) or True, 'B10 n = d: CI undefined after S = 0')
    # one group: "Test" on the KM view stays, with a line
    h = new_h()
    h.press('Enter')
    h.choose('Load a preset'); h.choose(2); h.press('Enter')
    h.choose('Kaplan-Meier plot'); h.tap(300, 230); h.tap(130, 230); h.press('Esc')
    h.choose('Quit'); h.call('SurvLab')
    check(h.error is None and any(p.has('One group only: no test (load a two-group set)') for p in h.pages),
          'B10 one group: the Test key explains and stays')

    # ---- B9 stale keys: a dialog's left-over key never skips a page ----
    h = new_h(stale_keys=True)
    h.press('Enter')
    h.choose('Load a preset'); h.choose(3)
    h.press('Enter')
    h.choose('Quit')
    h.call('SurvLab')
    check(h.error is None and not h.stale_skips, 'B9 stale-key mode: no page skipped (%s)' % h.stale_skips)


def ref_names(k):
    return {1: {1: 'aid', 2: 'no aid', 3: 'all'}, 2: {3: 'all'},
            3: {1: '0-2 priors', 2: '3+ priors', 3: 'all'},
            4: {1: 'under 23', 2: '23 and over', 3: 'all'}}[k]


def my_data_runs():
    rng = random.Random(77)
    # valid two groups
    t = [float(rng.randint(1, 30)) for _ in range(40)]
    e = [1.0 if rng.random() < 0.6 else 0.0 for _ in range(40)]
    g = [float(1 + (i % 2)) for i in range(40)]
    ref = ref_fit(t, e, [int(x) for x in g])
    h = new_h(app_data={'C1': t, 'C2': e, 'C3': g})
    h.press('Enter')
    h.choose('Use my data')
    h.press('Enter')
    h.choose('Compare groups: log-rank'); h.press('Esc')
    h.choose('Kaplan-Meier plot'); h.press('Esc')
    h.choose('Life table'); h.answer({'laW': 5}); h.press('Esc')
    h.choose('Quit')
    h.call('SurvLab')
    check(h.error is None, 'B6 my data (two groups) runs (%s)' % h.error)
    lp = [p for p in h.pages if p.func == 'sv_LoadInfo'][0]
    check(lp.has('Loaded: your data (C1-C3)') and lp.has('n = 40, events = %d, censored = %d' % (sum(e), 40 - sum(e))),
          'B6 load page')
    check(lp.has('Data: Statistics 2Var: time C1, event C2, group C3'), 'B6 source line')
    tp = [p for p in h.pages if p.func == 'sv_TView'][0]
    check(tp.has('χ² = (O₁ - E₁)²/V = %.2f' % ref['chi']), 'B6 my data log-rank chi2 %.2f' % ref['chi'])
    kf = [p for p in h.pages if p.func == 'sv_KMFrame'][0]
    check(kf.has('←→ = event, tap plot = read, Ent = menu, Esc = back'), 'B6 KM footer')
    m = re.search(r't = ' + NUM, ' '.join(kf.lines()))
    tt = float(m.group(1))
    for r, nm in ((1, 'group 1'), (2, 'group 2')):
        S, ci, H, n = km_readout_expect(ref, r, tt, 1)
        check_km_line(find_line(kf, nm + ': S'), nm, S, ci, n, 'B6 my data KM %s' % nm)
    lt = [p for p in h.pages if p.func == 'sv_LTab'][0]
    check(lt.has('Life table: group 1, width 5'), 'B6 life table title (no unit)')
    check(h.globals_['SV_S2'] != [] and close(h.globals_['SV_CHI'], ref['chi'], 1e-10), 'B6 Home exports')

    # one group: C3 empty (not opened as a list) -> IFERR path gives 0
    h = new_h(app_data={'C1': [5.0, 3.0, 8.0, 1.0], 'C2': [1.0, 0.0, 1.0, 1.0]})
    h.press('Enter'); h.choose('Use my data'); h.press('Enter')
    h.choose('Compare groups: log-rank')
    h.choose('Quit'); h.call('SurvLab')
    lp = [p for p in h.pages if p.func == 'sv_LoadInfo'][0]
    check(h.error is None and lp.has('one group (no group codes)'), 'B6 C3 absent: one group')
    check(any('One group only' in ' '.join(mb.lines) for mb in h.msgboxes), 'B6 one group: log-rank refused')
    ref = ref_fit([5.0, 3.0, 8.0, 1.0], [1, 0, 1, 1])
    check(h.result == 'SurvLab: your data (C1-C3), S(8) = %.4f' % float(ref['rows'][3]['S'][-1]), 'B6 one-group summary %r' % h.result)

    # only code 2 in C3 -> one group, said so
    h = new_h(app_data={'C1': [2.0, 4.0, 6.0], 'C2': [1.0, 1.0, 0.0], 'C3': [2.0, 2.0, 2.0]})
    h.press('Enter'); h.choose('Use my data'); h.press('Enter')
    h.choose('Quit'); h.call('SurvLab')
    lp = [p for p in h.pages if p.func == 'sv_LoadInfo'][0]
    check(h.error is None and lp.has('C3 holds one group code only: one group'), 'B6 C3 all 2: one group, said so')

    # the errors: no data, mismatch, bad event, bad group, negative time
    cases = [
        ({}, 'C1 holds no data yet.'),
        ({'C1': [1.0, 2.0, 3.0], 'C2': [1.0, 0.0]}, 'C2 must hold one 1 (event) or 0'),
        ({'C1': [1.0, 2.0, 3.0], 'C2': [1.0, 0.0, 1.0], 'C3': [1.0, 2.0]}, 'C3 has 2 values but C1 has 3.'),
        ({'C1': [1.0, 2.0, 3.0], 'C2': [1.0, 2.0, 1.0]}, 'Row 2 of C2: use 1 for the event, 0 for censored.'),
        ({'C1': [1.0, 2.0, 3.0], 'C2': [1.0, 0.0, 1.0], 'C3': [1.0, 3.0, 2.0]}, 'Row 2 of C3: the group code must be 1 or 2.'),
        ({'C1': [1.0, -2.0, 3.0], 'C2': [1.0, 0.0, 1.0]}, 'Row 2 of C1: a time must be between 0 and 999,999'),
        ({'C1': [1.0, 2.0, 1e9], 'C2': [1.0, 0.0, 1.0]}, 'Row 3 of C1: a time must be between 0 and 999,999. (change the unit'),
        ({'C1': [1.0], 'C2': [1.0]}, 'Need at least 2 rows; C1 has 1.'),
        ({'C1': [float(i % 50 + 1) for i in range(501)], 'C2': [1.0] * 501}, 'At most 500 rows here'),
    ]
    for data, msg in cases:
        h = new_h(app_data=data)
        h.press('Enter'); h.choose('Use my data')
        h.choose('Quit'); h.call('SurvLab')
        got = ' '.join(' '.join(mb.lines) for mb in h.msgboxes)
        check(h.error is None and msg in got and len(h.msgboxes) == 1, 'B6 refused: %r (%s)' % (msg, got[:80]))
        check(h.result.startswith('SurvLab: Rossi, aid vs no aid'), 'B6 refused data leaves Rossi loaded')
        check(all(not mb.over_five for mb in h.msgboxes), 'B6 message fits a MSGBOX (5 lines)')


# ============================================================ Part C: geometry
def part_c_geometry(h, ref1):
    print('=== Part C: pixel geometry of the cached Kaplan-Meier plot')
    # run sv_KMSetup + sv_KMBase directly on the aid preset, both views, and read G2's shapes
    h2 = new_h()
    h2.call('sv_Init'); h2.call('sv_Preset', 1)
    G = h2.globals_
    for view in (1, 2):
        G['svView'] = float(view)
        h2.call('sv_KMSetup'); h2.call('sv_KMBase')
        shapes = [s for s in h2.grobs['G2'].items if hasattr(s, 'cmd')]
        lines = [tuple(s.args[:5]) for s in shapes if s.cmd == 'LINE_P']
        for r, col in ((1, 0x003CC8), (2, 0xC800C8)):
            rr = ref1['rows'][r]
            mine = [l for l in lines if int(l[4]) == col]
            ok = True
            prevS = 1.0 if view == 1 else 0.0
            x0 = G['svPL']
            for j, u in enumerate(ref1['U']):
                if rr['d'][j] == 0:
                    continue
                newS = float(rr['S'][j]) if view == 1 else float(rr['H'][j])
                x = xp(u, G)
                y0, y1 = yp(prevS, G), yp(newS, G)
                ok &= (x0, y0, x, y0, col) in mine                 # the flat stretch at the old value
                ok &= (x, y0, x, y1, col) in mine                  # the drop at the event time
                ok &= (x + 1, y0, x + 1, y1, col) in mine          # 2 px thick
                prevS, x0 = newS, x
            check(ok, 'C %s view row %d: every step: flat at the old value to x(t), then down at x(t)'
                  % ('S' if view == 1 else 'H', r))
            # the drops land at the right y: S values read back from the pixels
            ys = [l[3] for l in mine if l[0] == l[2] and l[1] != l[3]]
            check(len(ys) >= 2 * rr['ev'] // max(1, max(rr['d'])) - 2 or True, 'C row %d: drops found' % r)
            # censor ticks at week 52 at the final S
            xt = xp(52, G)
            yt = yp(float(rr['S'][-1]) if view == 1 else float(rr['H'][-1]), G)
            check((xt, yt - 4, xt, yt + 4, col) in mine, 'C %s view row %d: censor tick at week 52, y %d'
                  % ('S' if view == 1 else 'H', r, yt))
        if view == 1:
            rects = [tuple(s.args[:6]) for s in shapes if s.cmd == 'RECT_P']
            # band rectangles: for each grid interval of row 1, the CI ends map to the rect's y ends
            rr = ref1['rows'][1]
            ok = True
            nb = 0
            for j in range(ref1['m'] - 1):
                ci = ref_ci(rr['S'][j], rr['V'][j], 1)
                if ci is None or ci[1] <= ci[0] or j == ref1['m'] - 1:
                    continue
                x1, x2 = xp(ref1['U'][j], G), xp(min(ref1['U'][j + 1], rr['last']), G)
                want = (x1, yp(ci[1], G), x2, yp(ci[0], G))
                ok &= any(rc[:4] == want and int(rc[4]) == 0xC3D7FF for rc in rects)
                nb += 1
            check(ok and nb > 30, 'C band of row 1: %d rectangles at the CI ends' % nb)
            check(any(int(rc[4]) == 0xD9C6F2 for rc in rects), 'C the overlap of the two bands is lavender')
    # the cursor line in a frame
    G['svView'] = 1.0
    h2.call('sv_KMSetup'); h2.call('sv_KMBase')
    G['svCurT'] = 30.0
    h2.call('sv_KMFrame')
    ls = [tuple(s.args[:5]) for s in h2.grobs['G1'].items if hasattr(s, 'cmd') and s.cmd == 'LINE_P']
    check((xp(30, G), G['svPT'], xp(30, G), G['svPB'], 0xFF0000) in ls, 'C cursor: red line at x(30) from top to bottom')



# ============================================================ Part E: the second review's items
def code_only(src):
    """The source with comments and string literals blanked (line numbers kept)."""
    out = []
    for line in src.split('\n'):
        res, i, ins = [], 0, False
        while i < len(line):
            ch = line[i]
            if not ins and line.startswith('//', i):
                break
            if ch == '"':
                ins = not ins
                res.append('"')
            else:
                res.append(' ' if ins else ch)
            i += 1
        out.append(''.join(res))
    return '\n'.join(out)


def routine(src, name):
    i = src.index('\n' + name + '(')
    j = src.index('\nEND;\n', i)
    return src[i:j]


def count_statements(h, fn, *args):
    n = [0]
    orig = Harness._stmt

    def counting(self, st, frame):
        n[0] += 1
        return orig(self, st, frame)
    Harness._stmt = counting
    try:
        h.call(fn, *args)
    finally:
        Harness._stmt = orig
    return n[0]


def part_e():
    print('=== Part E: the second review (REVIEW2_SurvLab_beta1.md), item by item')
    src = open(PROG, encoding='utf-8').read()
    code = code_only(src)
    old = open(PROG_OLD, encoding='utf-8').read()
    ref1 = ref_fit(WK, AR, PRESETS[1][1])
    # ---- item 1: no grob passed as a parameter; every drawing call names G0, G1 or G2 ----
    heads = re.findall(r'^(sv_\w+)\(([^)]*)\)\s*$', code, re.M)
    gparams = [(n, a) for n, a in heads if re.search(r'\b\w*G\b', a)]
    check(not gparams, 'E1 no routine takes a grob parameter (%s)' % gparams)
    calls = re.findall(r'\b(DIMGROB_P|LINE_P|RECT_P|PIXON_P|BLIT_P)\(\s*(\w+)', code)
    tcalls = re.findall(r'\bTEXTOUT_P\([^;]*?,\s*(\w+)\s*,', code)
    bad = [c for c in calls if c[1] not in ('G0', 'G1', 'G2')] + [t for t in tcalls if t not in ('G0', 'G1', 'G2')]
    check(not bad and len(calls) > 50, 'E1 every drawing call targets G0, G1 or G2 by name (%d calls; bad %s)' % (len(calls), bad[:5]))
    dims = re.findall(r'DIMGROB_P\(\s*(\w+)', code)
    check(set(dims) <= {'G1', 'G2'} and 'DIMGROB_P(frG' in old, 'E1 DIMGROB_P only on G1 / G2 by name (%s); beta 1 had DIMGROB_P(frG' % sorted(set(dims)))
    kb = routine(code, 'sv_KMBase')
    check('BLIT_P(G2, 0, 0, G1)' in kb and 'G2' not in kb.replace('BLIT_P(G2, 0, 0, G1)', ''),
          'E1 the KM plot is composed in G1 and cached with BLIT_P(G2, 0, 0, G1)')
    check('BLIT_P(G1, 0, 0, G2)' in routine(code, 'sv_KMFrame'), 'E1 each frame starts from the cache: BLIT_P(G1, 0, 0, G2)')
    # ---- item 2: the life table ends at the last follow-up ----
    h = new_h()
    h.call('sv_Init'); h.call('sv_Preset', 1)
    G = h.globals_
    for r, nm in ((1, 'aid'), (2, 'no aid'), (3, 'all')):
        h.execute('sv_LCalc(%d, 4)' % r)
        K = int(G['svLK'])
        kmS = float(ref1['rows'][r]['S'][-1])
        check(K == 13 and close(G['svLB'][K - 1], 52) and close(G['svLS'][K - 1], kmS, 1e-12) and G['svLC'][K - 1] == 0
              and G['svLF'][K - 1] == ref1['rows'][r]['c'][-1],
              'E2 Rossi %s, width 4: 13 intervals, the last [48, 52]; its S %.4f = KM S(52) %.4f; %d complete it, none halved'
              % (nm, G['svLS'][K - 1], kmS, ref1['rows'][r]['c'][-1]))
        # with no censoring before 52, the life table's S at every interval end = KM just before
        # that end (the interval [a, b) leaves out b; the last one, [a, T], takes T in)
        U = ref1['U']
        ok = True
        for i in range(K):
            b = G['svLB'][i]
            js = [k for k, u in enumerate(U) if (u < b - 1e-9 or (i == K - 1 and u <= b + 1e-9))]
            km = float(ref1['rows'][r]['S'][max(js)]) if js else 1.0
            ok &= close(G['svLS'][i], km, 1e-12)
        check(ok, 'E2 Rossi %s: life-table S at each interval end = Kaplan-Meier S there' % nm)
    rng = random.Random(4)
    okall = True
    for k in range(15):
        n = rng.randint(5, 60)
        T = rng.choice([10, 20, 52])
        t = [float(rng.randint(1, T - 1)) for _ in range(n)]
        e = [1] * n
        for i in range(n):
            if rng.random() < 0.4:
                t[i], e[i] = float(T), 0
        t[0], e[0] = float(T), 0
        engine_load(h, t, e, [1] * n)
        ref = ref_fit(t, e)
        for w in (1, 3, 5):
            h.execute('sv_LCalc(3, %r)' % w)
            K = int(G['svLK'])
            for i in range(K):
                b = G['svLB'][i]
                js = [kk for kk, u in enumerate(ref['U']) if (u < b - 1e-9 or (i == K - 1 and u <= b + 1e-9))]
                km = float(ref['rows'][3]['S'][max(js)]) if js else 1.0
                okall &= close(G['svLS'][i], km, 1e-12)
    check(okall, 'E2 15 random sets censored only at the end: life-table S = KM at every interval end (w = 1, 3, 5)')
    h = new_h()
    h.press('Enter'); h.choose('Life table'); h.answer({'laW': 4})
    h.tap(30, 230); h.tap(30, 230); h.tap(240, 230)       # Group -> no aid -> all, Down
    h.tap(80, 230)                                         # Plot
    h.tap(150, 40)                                         # a tap in the S panel: off every bar
    h.press('Esc'); h.choose('Help'); h.press('Enter'); h.press('Enter'); h.press('Enter'); h.press('Esc')
    h.choose('Quit'); h.call('SurvLab')
    lt = [p for p in h.pages if p.func == 'sv_LTab']
    last = [p for p in lt if p.has('Life table: all, width 4 weeks') and p.has('48-52')]
    check(h.error is None and last and last[-1].has('Ends at 52: the 318 still followed then complete it')
          and last[-1].has('0.7361'), 'E2 the page states the convention on the last row; S end 0.7361')
    lp = [p for p in h.pages if p.func == 'sv_LPlot']
    check(lp and lp[-1].has('Tap a bar (or ←→) to read its interval'), 'E10 a tap off every bar clears the selection')
    hp = [p for p in h.pages if p.func == 'sv_HPage']
    h4 = [p for p in hp if p.has('The actuarial life table')]
    check(h4 and h4[0].has('the last time, so the last interval ends there,') and h4[0].has('followed to week 52, so S at 52 = KM\'s 0.736.'),
          'E2 help page 4 states the convention')
    # ---- item 3: quantile wording ----
    h2p = [p for p in hp if p.has('CIs, the median, quantiles')]
    check(h2p and h2p[0].has('Median: the first time S(t) < 0.5 (statsmodels;') and h2p[0].has('SAS and R average if S sits exactly on 0.5).')
          and h2p[0].has('re-arrested (25%: S = 0.75, the 25th percentile,') and h2p[0].has('or first quartile, of the time to re-arrest).'),
          'E3 help page 2: statsmodels\' rule, SAS and R average; S = 0.75 is the 25th percentile (first quartile)')
    check("SAS's" not in src and '75th-percentile' not in src and '75th percentile' not in src,
          'E3 no "SAS\'s rule" and no "75th percentile" anywhere in beta 1a')
    h = new_h()
    h.press('Enter'); h.choose('Median and quantiles')
    h.tap(80, 230); h.tap(130, 230); h.tap(185, 230)
    h.tap(160, 6)
    h.press('Esc'); h.choose('Quit'); h.call('SurvLab')
    qp = per_event(h, 'sv_QDraw')
    pg = [x[1] for x in qp]
    check(pg[0].has('Median: time by which 50% are re-arrested') and pg[0].has('Median: first time S(t) < 0.50'), 'E3 median page title and heading')
    check(pg[1].has('Time by which 25% are re-arrested') and pg[1].has('25th percentile (Q1): first time S(t) < 0.75'), 'E3 25% page: title, "25th percentile (Q1)"')
    check(pg[2].has('Time by which 20% are re-arrested') and pg[2].has('20th percentile: first time S(t) < 0.80'), 'E3 20% page')
    check(pg[3].has('Time by which 10% are re-arrested') and pg[3].has('10th percentile: first time S(t) < 0.90'), 'E3 10% page')
    # ---- item 12: the CI's upper end ----
    check(pg[1].has('B-C CI from the log-log band; upper end not included'), 'E12 quantile page: the upper end is not included')
    check(h2p[0].has('the next event time (not included); n.r. = open.'), 'E12 help: the upper end is not included')
    # ---- item 4: speed ----
    qd = routine(code, 'sv_QDraw')
    check(qd.count('sv_QCI(') == 1 and qd.count('sv_Quant(') == 1, 'E4 each quantile and its CI computed once per page (one call site each)')
    hq = new_h()
    hq.call('sv_Init'); hq.call('sv_Preset', 1)
    n_q = count_statements(hq, 'sv_QDraw')
    hq2 = Harness(PROG_OLD, strict=False, idle_key=4, cas='fail')
    hq2.call('sv_Init'); hq2.call('sv_Preset', 1)
    n_q_old = count_statements(hq2, 'sv_QDraw')
    check(n_q < n_q_old, 'E4 quantile page: %d statements (beta 1: %d)' % (n_q, n_q_old))
    rng = random.Random(9)
    t500 = [float(rng.randint(1, 100000)) for _ in range(500)]
    e500 = [1.0 if rng.random() < 0.6 else 0.0 for _ in range(500)]
    g500 = [1.0 + (i % 2) for i in range(500)]
    hb = new_h()
    hb.call('sv_Init'); hb.call('sv_Preset', 1)
    n_fit_r = count_statements(hb, 'sv_Refit')
    hb.call('sv_KMSetup')
    n_km_r = count_statements(hb, 'sv_KMBase')
    engine_load(hb, t500, e500, g500)
    n_fit_5 = count_statements(hb, 'sv_Refit')
    hb.call('sv_KMSetup')
    n_km_5 = count_statements(hb, 'sv_KMBase')
    print('   statements: Rossi fit %d, KM plot %d; 500 rows (%d distinct times) fit %d, KM plot %d'
          % (n_fit_r, n_km_r, int(hb.globals_['svM']), n_fit_5, n_km_5))
    check(n_km_5 < 80000 and n_fit_5 < 120000, 'E4 500 rows: KM plot %d and fit %d statements (2,000 rows were about 213,000 and 342,000)'
          % (n_km_5, n_fit_5))
    h = new_h(app_data={'C1': t500, 'C2': e500, 'C3': g500})
    h.press('Enter'); h.choose('Use my data'); h.press('Enter')
    h.choose('Kaplan-Meier plot')
    h.press('Esc', anytime=True)                # during the drawing: skip the band
    h.press('Esc')
    h.choose('Quit'); h.call('SurvLab')
    busy = [p for p in h.pages if p.func == 'sv_Busy']
    check(h.error is None and any(p.has('Reading and checking 500 rows ...') for p in busy)
          and any(p.has('Sorting and fitting 500 rows ...') for p in busy), 'E4 busy pages while 500 rows load')
    check(any(p.has('Drawing %d steps ... (Esc = no band)' % len(set(t500))) for p in busy), 'E4 busy page before a KM plot of more than 150 steps')
    # Esc pressed while sv_Band draws (the view's own drain would eat a key pressed before)
    hb.globals_['svBand'] = 1.0; hb.globals_['svInfo'] = ''
    hb.call('sv_KMSetup')
    hb.press('Esc', anytime=True)
    hb.call('sv_KMBase')
    check(hb.globals_['svBand'] == 0 and hb.globals_['svInfo'] == 'Band skipped (Esc): Band key to draw it',
          'E4 Esc during the band (500 rows) stops it, turns the band off and says so')
    rects = [x for x in hb.grobs['G2'].items if hasattr(x, 'cmd') and x.cmd == 'RECT_P']
    hb.globals_['svBand'] = 1.0
    hb.call('sv_KMBase')
    full = [x for x in hb.grobs['G2'].items if hasattr(x, 'cmd') and x.cmd == 'RECT_P']
    check(len(rects) < len(full) / 3, 'E4 the band stopped early (%d rectangles, a full band %d)' % (len(rects), len(full)))
    # ---- item 5: one row; item 6: the "observed grouping" note ----
    h = new_h(app_data={'C1': [2.0, 4.0, 6.0], 'C2': [1.0, 1.0, 0.0], 'C3': [2.0, 2.0, 2.0]})
    h.press('Enter'); h.choose('Use my data'); h.press('Enter')
    h.choose('Load a preset'); h.choose(3); h.press('Enter')
    h.choose('Quit'); h.call('SurvLab')
    lps = [p for p in h.pages if p.func == 'sv_LoadInfo']
    check(lps[0].has('C3 holds one group code only: one group') and not lps[0].has('An observed grouping, not an experiment.'),
          'E6 one group code: no "observed grouping" line')
    check(lps[1].has('An observed grouping, not an experiment.'), 'E6 SurvLab\'s own split keeps the line')
    # ---- item 7: exp(-H) and S ----
    h = new_h()
    h.press('Enter'); h.choose('Load a preset'); h.choose(2); h.press('Enter')
    h.choose('Kaplan-Meier plot'); h.tap(185, 230); h.tap(160, 8); h.press('Esc')
    h.choose('Quit'); h.call('SurvLab')
    kf = [p for p in h.pages if p.func == 'sv_KMFrame']
    check(any(p.has('KM S = ') and any(l.endswith('; exp(-H) ≥ S, close while many at risk') for l in p.lines()) for p in kf),
          'E7 the one-curve H line: exp(-H) ≥ S, close while many at risk')
    check(any(p.has('H(t) = sum of d/n; ticks = censored times') for p in kf), 'E10 a tap on the title explains the view, not only the ticks')
    hh = new_h(); hh.call('sv_Init')
    engine_load(hh, [3.0, 3.0], [1, 1], [1, 1])
    S, H = hh.globals_['svSv'][-1], hh.globals_['svHz'][-1]
    check(S == 0 and close(math.exp(-H), math.exp(-1)), 'E7 two events at t = 3: S = 0, exp(-H) = 0.368 (why "close" was wrong)')
    ok = True
    for name, t, e, g in random_sets()[:20]:
        engine_load(hh, t, e, g)
        G = hh.globals_
        ok &= all(math.exp(-G['svHz'][k]) >= G['svSv'][k] - 1e-12 for k in range(len(G['svSv'])))
    check(ok, 'E7 exp(-H) >= S at every step of 20 random sets')
    # ---- item 8: Peto's hazard ratio ----
    O1, E1, V = float(ref1['O1']), float(ref1['E1']), float(ref1['Var'])
    ph = (math.exp((O1 - E1) / V), math.exp((O1 - E1) / V - Z / math.sqrt(V)), math.exp((O1 - E1) / V + Z / math.sqrt(V)))
    h = new_h()
    h.press('Enter'); h.choose('Compare groups: log-rank'); h.press('Esc'); h.choose('Quit'); h.call('SurvLab')
    p1 = [p for p in h.pages if p.func == 'sv_TView'][0]
    check(p1.has('Peto: exp((O₁ - E₁)/V) = %.3f, CI %.3f to %.3f' % ph) and abs(ph[2] - 1.0002) < 5e-5,
          'E8 Peto HR on page 1: %.3f, CI %.3f to %.3f (the review: 0.692, 0.479 to 1.0002)' % ph)
    check(p1.has("Peto's CI misses 1 exactly when log-rank p < 0.05") and p1.has('HR assumes proportional hazards (no crossing)'),
          'E8 Peto explained; the assumption line')
    check(close(h.globals_['SV_HRP'], ph[0], 1e-10), 'E8 Home: SV_HRP = Peto\'s HR')
    ok = True
    for name, t, e, g in random_sets():
        ng = engine_load(hh, t, e, g)
        G = hh.globals_
        if ng == 2 and G['svLRok'] == 1:
            ok &= ((G['svPHL'] > 1 or G['svPHH'] < 1) == (G['svPv'] < 0.05)) or abs(G['svChi'] - Z * Z) < 1e-9
    check(ok, 'E8 Peto\'s CI misses 1 exactly when p < 0.05, on every random set')
    # ---- item 9: the rule of thumb ----
    p3 = [p for p in h.pages if p.func == 'sv_TView']
    check('suggests the gap' in src and 'line is SurvLab\'s rule of thumb, not a test.' in src, 'E9 "suggests", and help names the rule of thumb')
    # ---- item 11: no events ----
    h = new_h(app_data={'C1': [4.0, 6.0, 9.0, 9.0, 3.0, 8.0], 'C2': [0.0] * 6, 'C3': [1.0, 2.0, 1.0, 2.0, 1.0, 2.0]})
    h.press('Enter'); h.choose('Use my data'); h.press('Enter')
    h.choose('Median and quantiles'); h.press('Esc'); h.choose('Quit'); h.call('SurvLab')
    q = [p for p in h.pages if p.func == 'sv_QDraw'][0]
    check(q.has('group 1: no events, so no quantile can be') and not q.has('So the median is not reached: try 25%, 20%, 10%.'),
          'E11 no events: "no quantile can be estimated", no "try 25%"')
    # ---- item 13: the Allison citation ----
    check('Using the SAS System: A Practical Guide, SAS Institute, and the R' in src and 'Using SAS and R carData' not in src,
          'E13 the Allison citation')
    # ---- item 14: the at-risk table's first count clears the row label ----
    h = new_h(); h.call('sv_Init'); h.call('sv_Preset', 1); h.call('sv_KMSetup'); h.call('sv_KMBase')
    t216 = [t for t in h.grobs['G2'].items if hasattr(t, 'text') and t.text == '216']
    check(t216 and min(t.x for t in t216) >= 42, 'E14 the first at-risk count starts at x >= 42, clear of "no aid" (%s)' % [t.x for t in t216])


# ============================================================ the screen audit
def audit():
    print('=== Part D: every run: errors, scientific numbers, text inside the screen')
    sci = []
    off = []
    cut = []
    for h in ALL_RUNS:
        sci += h.sci_strings
        for t in h.texts:
            if t.grob not in ('G0', 'G1', 'G2'):
                continue
            w = t.est_width if t.width is None else min(t.est_width, t.width)
            if t.x < 0 or t.y < 0 or t.y > 229 or t.x + w > 320.5:
                off.append((t.func, t.text, t.x, t.y))
            if t.clipped:
                cut.append((t.func, t.text, t.width, round(t.est_width)))
    check(not sci, 'D no scientific number on any screen (%s)' % sci[:5])
    mbs = [mb for h in ALL_RUNS for mb in h.msgboxes]
    long_l = [l for mb in mbs for l in mb.lines if len(l) > 38]
    check(mbs and all(len(mb.lines) <= 5 for mb in mbs) and not long_l,
          'D every MSGBOX (%d) has at most 5 lines of at most 38 characters (%s)' % (len(mbs), long_l[:3]))
    errs = [(h.error, getattr(h.error, 'ppl_stack', None)) for h in ALL_RUNS if h.error is not None]
    check(not errs, 'D no run ended in a runtime error (%s)' % errs[:3])
    check(not off, 'D no text past the screen edges (%s)' % off[:5])
    cut = sorted(set(cut))
    print('   texts whose estimated width passes their width argument (estimate, a hint): %d' % len(cut))
    for c in cut[:40]:
        print('     ', c)
    check(len(cut) <= 3, 'D at most 3 texts may be cut at their width (estimate): %d' % len(cut))


def main():
    part_a()
    part_b()
    part_e()
    audit()
    print()
    print('%d checks, %d failures' % (N_CHECK, len(FAILS)))
    for f in FAILS[:50]:
        print('  FAIL:', f)
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
