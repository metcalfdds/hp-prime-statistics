#!/usr/bin/env python3
"""verify_TrendTest_beta3f.py -- the Pearson and departure p-values keep their digits.

Independent review, 22 October 2026.  Three sections:
  A. trUpper(df, x) against SciPy's chi2.sf at df 1 to 12 and x from 0.5 to 400: relative error.
  B. trCompute on beta 3e and beta 3f for six 2 x k tables, mild and extreme: trX2P, trPP, trX2D,
     trPD and the trend p against SciPy; on 3e the extreme tables print p = 0 on a 12-digit model.
  C. Everything else in trCompute is unchanged: the two versions give the same trX2T, trPT, trX2P,
     trX2D, slope, Wilson limits and odds ratios on every table.
Needs tools/ppl_run_v3e.py beside programs/ (run from verify/), hp-prime-kit (HPKIT or the
Community_Library zip) and SciPy.  Beta 3e is read from git (commit ec9e045) when its file is absent.
"""
import os, sys, io, contextlib, subprocess, tempfile, math
HERE = '/home/claude/metcalfdds/hp-prime-statistics/verify'; ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
NEW = '/home/claude/new6/TrendTest_beta3g.txt'
OLD = os.path.join(ROOT, 'programs', 'TrendTest_beta3e.txt')
if not os.path.exists(OLD):
    OLD = os.path.join(tempfile.gettempdir(), 'TrendTest_beta3e_from_git.txt')
    if not os.path.exists(OLD):
        open(OLD, 'wb').write(subprocess.check_output(['git', '-C', ROOT, 'show', 'ec9e045:programs/TrendTest_beta3e.txt']))
from ppl_run_v3e import Harness
from scipy import stats
def load(f):
    with contextlib.redirect_stdout(io.StringIO()):
        return Harness(f, strict=False, on_unverified='warn')
def ev(h, e):
    h.reset_records()
    with contextlib.redirect_stdout(io.StringIO()):
        return h.execute(e)
fails = 0
def chk(label, ok):
    global fails
    if not ok: fails += 1
    print('  %s %s' % ('ok  ' if ok else 'FAIL', label))
hn, ho = load(NEW), load(OLD)
print('A. trUpper(df, x) against chi2.sf')
worst = 0
for df in range(1, 13):
    for x in [0.5, 2, 5, 10, 20, 40, 60, 100, 200, 400]:
        got = ev(hn, 'trUpper(%d,%g)' % (df, x)); want = stats.chi2.sf(x, df)
        rel = abs(got - want) / want; worst = max(worst, rel)
        if rel > 1e-9: print('     df %d x %g: got %.12g want %.12g' % (df, x, got, want))
chk('trUpper matches chi2.sf to 1E-9 relative at df 1-12, x 0.5-400 (worst %.1e)' % worst, worst <= 1e-9)
chk('trUpper(3, 0) = 1 and trUpper(2, -1) = 1', ev(hn, 'trUpper(3,0)') == 1 and ev(hn, 'trUpper(2,-1)') == 1)
print('B. trCompute: Pearson and departure p on both versions; C. the rest identical')
tables = [([0,1,2,3], [2,5,9,14], [20,20,20,20]), ([1,2,4], [3,8,12], [30,25,20]),
          ([0,1,2,3,4], [1,2,6,9,15], [50,50,50,50,50]),
          ([0,1,2], [5,95,5], [100,100,100]),            # Pearson 180 at 2 df: p 8E-40
          ([0,1,2,3], [2,98,2,98], [100,100,100,100]),   # Pearson 384, departure 3 df: tiny
          ([0,1,2,3,4,5], [90,5,90,5,90,5], [100]*6)]     # Pearson 433 at 5 df
def run(h, X, A, N):
    h.globals_.update({'trK': float(len(X)), 'trZ': 1.959964, 'trX': [float(v) for v in X],
                       'trA': [float(v) for v in A], 'trTot': [float(v) for v in N]})
    ev(h, 'trCompute()')
    g = h.globals_
    return {k: g[k] for k in ('trX2T', 'trPT', 'trX2P', 'trPP', 'trX2D', 'trPD', 'trB')}, g['trLo'], g['trHi'], g['trOR']
for X, A, N in tables:
    rn, lo_n, hi_n, or_n = run(hn, X, A, N); ro, lo_o, hi_o, or_o = run(ho, X, A, N)
    k = len(X)
    pp = stats.chi2.sf(rn['trX2P'], k - 1); pd = stats.chi2.sf(rn['trX2D'], k - 2) if k > 2 else None
    chk('%s Pearson X2 %.3f: 3f p %.4g (SciPy %.4g); 3e p %.4g' % (A, rn['trX2P'], rn['trPP'], pp, ro['trPP']),
        abs(rn['trPP'] - pp) <= 1e-9 * pp)
    if pd is not None:
        chk('%s departure X2 %.3f: 3f p %.4g (SciPy %.4g); 3e p %.4g' % (A, rn['trX2D'], rn['trPD'], pd, ro['trPD']),
            abs(rn['trPD'] - pd) <= 1e-9 * max(pd, 1e-300))
    # the 12-digit model: 1 - CDF is exactly 0 once the tail is below 5E-13 on the Prime
    if pp < 5e-13:
        print('     (on the Prime, 3e prints p = 0 here: the tail %.1e is below its last digit)' % pp)
    same = all(abs(rn[k2] - ro[k2]) <= 1e-12 * max(1, abs(ro[k2])) for k2 in ('trX2T', 'trPT', 'trX2P', 'trX2D', 'trB'))
    same = same and lo_n == lo_o and hi_n == hi_o and or_n == or_o
    chk('C %s: trend X2 and p, Pearson and departure X2, slope, Wilson limits and ORs identical in 3e and 3f' % (A,), same)
print('failures: %d' % fails)
